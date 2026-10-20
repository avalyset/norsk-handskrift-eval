#!/usr/bin/env python3
"""norsk-handskrift prereg: ett inngangspunkt (se prereg/METHOD.md).
  verifiser     SHA256 for alle filer i prereg/manifest.json (modeller, skript, heldout-liste, locks); avvik = stopp, kode 2
  manifest      (re)genererer manifest.json (kun før frys)
  kjor          heldout-60: leser BARE work/heldout-60.txt, henter hver side fra Zenodo (range), verifiserer SHA256 mot lista,
                segmenterer -> utklipp 128 px -> gjenkjenning (LM vekt 1,0) -> scoring. Stopper ved avvik. (Ikke kjørt før frys + Eiriks ja.)
  gjenskaping   kjører samme kjede to ganger på gitte PILOTsider (aldri heldout) og sammenligner SHA256 av alle utdata
Kjedeprosessene kjøres som separate prosesser, hver i sitt venv (ADR 0001/0002)."""
import argparse, hashlib, json, os, pathlib, subprocess, sys, shutil, random, time, re
ROT = pathlib.Path(__file__).resolve().parent.parent
HELD = ROT / "work" / "heldout-60.txt"; MAN = ROT / "prereg" / "manifest.json"
PY = {k: str(ROT / f"venv-{k}" / "bin" / "python") for k in ("ufcn", "pylaia", "tools", "kraken")}
ZENODO = "https://zenodo.org/records/10255840/files/norhand_v3.zip?download=1"
SEG = {"venv": "kraken", "modell": "venv-kraken/lib/python3.10/site-packages/kraken/blla.mlmodel", "script": "scripts/seg_kraken.py"}   # ADR 0004 (besluttet av Eirik 20.10.2026)
LM_VEKT = "1.0"                                                                          # ADR 0005
FILER = ["prereg/METHOD.md", "prereg/run.py", "prereg/score.py", "scripts/guard.py", "scripts/lib.py", "scripts/seg_generic.py", "scripts/seg_kraken.py", "scripts/dec.sh", "scripts/dec_lm.sh",
         "work/heldout-60.txt", "scripts/presisjon.py", "scripts/differanser.py", "scripts/csv_escape.py", "scripts/parede.py", "results/parede-segmenterere.json", "prereg/gjenskaping.json", "results/presisjon.json", "results/pilot-differanser.json", "results/csv-escape.json",
         "prereg/kilder/zenodo-10255840-norhand-v3.json", "prereg/kilder/zenodo-10628791-norhand-v2.json", "prereg/kilder/hf-revisjoner.json", "prereg/kilder/github-kraken.txt", "prereg/kilder/eksterne-dokumenter.sha256", "prereg/locks/venv-pylaia.freeze.txt", "prereg/locks/venv-ufcn.freeze.txt", "prereg/locks/venv-kraken.freeze.txt", "prereg/locks/venv-tools.freeze.txt",
         "venv-kraken/lib/python3.10/site-packages/kraken/blla.mlmodel", "models/doc-ufcn-norhand-v1-line/model.pth", "models/doc-ufcn-norhand-v1-line/parameters.yml",
         "models/doc-ufcn-generic-historical-line/model.pth", "models/doc-ufcn-generic-historical-line/parameters.yml",
         "models/pylaia-norhand-v3/weights.ckpt", "models/pylaia-norhand-v3/model", "models/pylaia-norhand-v3/syms.txt", "models/pylaia-norhand-v3/tokens.txt",
         "models/pylaia-norhand-v3/lexicon.txt", "models/pylaia-norhand-v3/language_model.arpa.gz"]
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()
def verifiser():
    m = json.load(open(MAN))["sha256"]; bad = [f for f, s in m.items() if not (ROT / f).exists() or sha(ROT / f) != s]
    if bad: print("AVVIK, stopper:", ", ".join(bad), file=sys.stderr); sys.exit(2)
    print("verifiser: OK,", len(m), "filer")
def manifest():
    d = {"versjon": "prereg-utkast", "seed": 20261020, "bootstrap": {"B": 2000, "metode": "prosentil over sider", "nedre_indeks": 50, "ovre_indeks": 1949},
         "segmenterer": SEG, "lm_vekt": LM_VEKT, "batch": 16, "linjehoyde_px": 128, "sha256": {f: sha(ROT / f) for f in FILER}}
    json.dump(d, open(MAN, "w"), indent=1); print("manifest skrevet,", len(FILER), "filer; sha256(manifest) =", sha(MAN))
def heldout_rows():
    return [l.rstrip("\n").split("\t") for l in open(HELD, encoding="utf8") if l.strip() and not l.startswith("#")]
def _ledig_minne_pst():
    m = re.search(r"free percentage: (\d+)", subprocess.run(["memory_pressure"], capture_output=True, text=True).stdout); return int(m.group(1)) if m else 0
def _swap_mb():
    m = re.search(r"used = ([\d.]+)M", subprocess.run(["sysctl", "vm.swapusage"], capture_output=True, text=True).stdout); return float(m.group(1)) if m else 0.0
SWAP0 = None
def vakt(steg):
    """ressursvakt før hvert steg (METHOD § 10): minne ≥ 20 % ledig, swap ≤ +1 GB mot start, intern disk ≥ 10 GiB. Brudd = pause (sjekk hvert 30. s i opptil 1 t), deretter stopp (kode 5)."""
    global SWAP0
    SWAP0 = _swap_mb() if SWAP0 is None else SWAP0
    for forsok in range(120):
        ok = _ledig_minne_pst() >= 20 and _swap_mb() <= SWAP0 + 1024 and shutil.disk_usage("/").free >= 10 * 2**30
        if ok: return
        print(f"vakt: pause før {steg} (minne/swap/disk utenfor grense)", file=sys.stderr); time.sleep(30)
    print("vakt: ressursgrense brutt i over 1 t, stopper", file=sys.stderr); sys.exit(5)
def sh(cmd, env=None, **kw):
    r = subprocess.run(cmd, cwd=ROT, env={**os.environ, **(env or {})}, **kw)
    if r.returncode: print("FEIL i", cmd[:3], "kode", r.returncode, file=sys.stderr); sys.exit(3)
def kjede(imgdir, xmldir, out, forvent, env=None):
    out = pathlib.Path(out); shutil.rmtree(out, ignore_errors=True); out.mkdir(parents=True)
    rel = lambda p: str(pathlib.Path(p).relative_to(ROT)) if str(p).startswith(str(ROT)) else str(p)
    vakt("segmentering"); sh([PY[SEG["venv"]], "-I", SEG["script"], rel(imgdir), rel(out / "seg")], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    ids = [l.strip() for l in open(out / "seg" / "list.txt") if l.strip()]
    for forsok in (1, 2):   # dekoderfeil: én gjentatt kjøring, deretter stopp (METHOD § 10)
        vakt("dekoding")
        r = subprocess.run(["scripts/dec_lm.sh", rel(out / "seg"), rel(out / "dec"), LM_VEKT], cwd=ROT, env={**os.environ, **(env or {})})
        fikk = {l.split(" ", 1)[0] for l in open(out / "dec.txt", encoding="utf8") if l.strip() and not l.startswith("#")} if (out / "dec.txt").exists() else set()
        if r.returncode == 0 and set(ids) <= fikk: break   # exit-koden er dekoderens, og alle linje-ID-er må være med
        if forsok == 2: print("FEIL: dekoding feilet to ganger, stopper (føres i AVVIK.md)", file=sys.stderr); sys.exit(3)
    # én side uten funne linjer gir tom liste; scoring teller den som CER 100 %
    vakt("scoring"); sh([PY["tools"], "-I", "prereg/score.py", rel(out / "seg"), rel(out / "dec.txt"), rel(xmldir), rel(out / "resultat.json"), str(forvent)], env=env)
def kjor():
    verifiser(); rows = heldout_rows(); assert len(rows) == 60, "heldout-lista skal ha 60 sider"
    from remotezip import RemoteZip  # kjøres med venv-tools
    work = ROT / "work" / "run-heldout"; shutil.rmtree(work, ignore_errors=True); (work / "img").mkdir(parents=True); (work / "xml").mkdir(parents=True)   # tom katalog: ingen rester fra tidligere kjøringer
    z = RemoteZip(ZENODO)
    for pid, hi, hx in rows:
        bi = z.read(f"test/images/{pid}.jpg"); bx = z.read(f"test/page/{pid}.xml")
        if hashlib.sha256(bi).hexdigest() != hi or hashlib.sha256(bx).hexdigest() != hx: print("AVVIK: hash for", pid, file=sys.stderr); sys.exit(2)
        (work / "img" / f"{pid}.jpg").write_bytes(bi); (work / "xml" / f"{pid}.xml").write_bytes(bx)
    kjede(work / "img", work / "xml", work / "ut", 60, env={"NORHAND_HELDOUT_OK": sha(HELD)})
def gjenskaping(sider):
    held = {r[0] for r in heldout_rows()}
    if held & set(sider): print("NEKTER: heldout-side i gjenskapingstest", file=sys.stderr); sys.exit(2)
    pilot = {l.strip().split("/")[-1][:-4] for l in open(ROT / "data/p20/sample.txt") if l.strip()}
    if not set(sider) <= pilot: print("NEKTER: gjenskapingstest bare på 20-utvalget", file=sys.stderr); sys.exit(2)
    kode = {f: sha(ROT / f) for f in ["prereg/run.py", "prereg/score.py", "scripts/seg_kraken.py", "scripts/dec.sh", "scripts/dec_lm.sh", "scripts/guard.py", "scripts/lib.py"]}   # koden testen kjører mot, regnet ved start
    w = ROT / "work" / "run-gjenskaping"; shutil.rmtree(w, ignore_errors=True); (w / "img").mkdir(parents=True); (w / "xml").mkdir()
    for s in sider:
        os.symlink(ROT / f"data/p20/test/images/{s}.jpg", w / "img" / f"{s}.jpg"); shutil.copy(ROT / f"data/p20/test/page/{s}.xml", w / "xml" / f"{s}.xml")
    res = []
    for k in (1, 2):
        kjede(w / "img", w / "xml", w / f"kj{k}", len(sider)); d = {}
        for f in ["dec.txt", "resultat.json", "seg/list.txt"]: d[f] = sha(w / f"kj{k}" / f)
        mt = json.load(open(w / f"kj{k}" / "seg" / "meta.json"))   # veggklokketid ("sec") er ikke utdata og fjernes før hashing
        for v in mt.values(): v.pop("sec", None)
        d["seg/meta.json(uten sec)"] = hashlib.sha256(json.dumps(mt, sort_keys=True).encode()).hexdigest()
        for p in sorted((w / f"kj{k}" / "seg" / "lines").glob("*.png")): d["seg/lines/" + p.name] = sha(p)
        res.append(d)
    diff = [f for f in res[0] if res[0][f] != res[1].get(f)] + [f for f in res[1] if f not in res[0]]
    rapport = {"sider": sider, "filer_sammenlignet": len(res[0]), "ulike": diff, "byte_identisk": not diff, "sha256_dec": res[0]["dec.txt"], "sha256_resultat": res[0]["resultat.json"], "kode_sha256": kode}
    json.dump(rapport, open(ROT / "prereg" / "gjenskaping.json", "w"), indent=1); print(json.dumps(rapport, indent=1)); sys.exit(0 if not diff else 6)
if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("kommando", choices=["verifiser", "manifest", "kjor", "gjenskaping"]); ap.add_argument("--sider", default="")
    a = ap.parse_args()
    {"verifiser": verifiser, "manifest": manifest, "kjor": kjor}.get(a.kommando, lambda: gjenskaping([s for s in a.sider.split(",") if s]))()
