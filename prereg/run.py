#!/usr/bin/env python3
"""norsk-handskrift prereg: ett inngangspunkt (se prereg/METHOD.md).
  verifiser     SHA256 for alle filer i prereg/manifest.json (modeller, skript, heldout-liste, locks); avvik = stopp, kode 2
  manifest      (re)genererer manifest.json (kun før frys)
  kjor          heldout-60: leser BARE work/heldout-60.txt, henter hver side fra Zenodo (range), verifiserer SHA256 mot lista,
                segmenterer -> utklipp 128 px -> gjenkjenning (LM vekt 1,0) -> scoring. Stopper ved avvik. (Ikke kjørt før frys + Eiriks ja.)
  gjenskaping   kjører samme kjede to ganger på gitte PILOTsider (aldri heldout) og sammenligner SHA256 av alle utdata
Kjedeprosessene kjøres som separate prosesser, hver i sitt venv (ADR 0001/0002)."""
import argparse, hashlib, json, os, pathlib, subprocess, sys, shutil, random
ROT = pathlib.Path(__file__).resolve().parent.parent
HELD = ROT / "work" / "heldout-60.txt"; MAN = ROT / "prereg" / "manifest.json"
PY = {k: str(ROT / f"venv-{k}" / "bin" / "python") for k in ("ufcn", "pylaia", "tools", "kraken")}
ZENODO = "https://zenodo.org/records/10255840/files/norhand_v3.zip?download=1"
SEG = {"venv": "kraken", "modell": "venv-kraken/lib/python3.10/site-packages/kraken/blla.mlmodel", "script": "scripts/seg_kraken.py"}   # ADR 0004 (foreslått, venter Eiriks ok)
LM_VEKT = "1.0"                                                                          # ADR 0005
FILER = ["prereg/METHOD.md", "prereg/run.py", "prereg/score.py", "scripts/guard.py", "scripts/lib.py", "scripts/seg_generic.py", "scripts/seg_kraken.py", "scripts/dec.sh", "scripts/dec_lm.sh",
         "work/heldout-60.txt", "prereg/locks/venv-pylaia.freeze.txt", "prereg/locks/venv-ufcn.freeze.txt", "prereg/locks/venv-kraken.freeze.txt", "prereg/locks/venv-tools.freeze.txt",
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
def sh(cmd, env=None, **kw):
    r = subprocess.run(cmd, cwd=ROT, env={**os.environ, **(env or {})}, **kw)
    if r.returncode: print("FEIL i", cmd[:3], "kode", r.returncode, file=sys.stderr); sys.exit(3)
def kjede(imgdir, xmldir, out, env=None):
    out = pathlib.Path(out); shutil.rmtree(out, ignore_errors=True); out.mkdir(parents=True)
    rel = lambda p: str(pathlib.Path(p).relative_to(ROT)) if str(p).startswith(str(ROT)) else str(p)
    sh([PY[SEG["venv"]], "-I", SEG["script"], rel(imgdir), rel(out / "seg")], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    sh(["scripts/dec_lm.sh", rel(out / "seg"), rel(out / "dec"), LM_VEKT])
    # én side uten funne linjer gir tom liste; scoring teller den som CER 100 %
    sh([PY["tools"], "-I", "prereg/score.py", rel(out / "seg"), rel(out / "dec.txt"), rel(xmldir), rel(out / "resultat.json")])
def kjor():
    verifiser(); rows = heldout_rows(); assert len(rows) == 60, "heldout-lista skal ha 60 sider"
    from remotezip import RemoteZip  # kjøres med venv-tools
    work = ROT / "work" / "run-heldout"; (work / "img").mkdir(parents=True, exist_ok=True); (work / "xml").mkdir(parents=True, exist_ok=True)
    z = RemoteZip(ZENODO)
    for pid, hi, hx in rows:
        bi = z.read(f"test/images/{pid}.jpg"); bx = z.read(f"test/page/{pid}.xml")
        if hashlib.sha256(bi).hexdigest() != hi or hashlib.sha256(bx).hexdigest() != hx: print("AVVIK: hash for", pid, file=sys.stderr); sys.exit(2)
        (work / "img" / f"{pid}.jpg").write_bytes(bi); (work / "xml" / f"{pid}.xml").write_bytes(bx)
    kjede(work / "img", work / "xml", work / "ut", env={"NORHAND_HELDOUT_OK": sha(HELD)})
def gjenskaping(sider):
    held = {r[0] for r in heldout_rows()}
    if held & set(sider): print("NEKTER: heldout-side i gjenskapingstest", file=sys.stderr); sys.exit(2)
    pilot = {l.strip().split("/")[-1][:-4] for l in open(ROT / "data/p20/sample.txt") if l.strip()}
    if not set(sider) <= pilot: print("NEKTER: gjenskapingstest bare på 20-utvalget", file=sys.stderr); sys.exit(2)
    w = ROT / "work" / "run-gjenskaping"; shutil.rmtree(w, ignore_errors=True); (w / "img").mkdir(parents=True); (w / "xml").mkdir()
    for s in sider:
        os.symlink(ROT / f"data/p20/test/images/{s}.jpg", w / "img" / f"{s}.jpg"); shutil.copy(ROT / f"data/p20/test/page/{s}.xml", w / "xml" / f"{s}.xml")
    res = []
    for k in (1, 2):
        kjede(w / "img", w / "xml", w / f"kj{k}"); d = {}
        for f in ["dec.txt", "resultat.json", "seg/list.txt"]: d[f] = sha(w / f"kj{k}" / f)
        mt = json.load(open(w / f"kj{k}" / "seg" / "meta.json"))   # veggklokketid ("sec") er ikke utdata og fjernes før hashing
        for v in mt.values(): v.pop("sec", None)
        d["seg/meta.json(uten sec)"] = hashlib.sha256(json.dumps(mt, sort_keys=True).encode()).hexdigest()
        for p in sorted((w / f"kj{k}" / "seg" / "lines").glob("*.png")): d["seg/lines/" + p.name] = sha(p)
        res.append(d)
    diff = [f for f in res[0] if res[0][f] != res[1].get(f)] + [f for f in res[1] if f not in res[0]]
    rapport = {"sider": sider, "filer_sammenlignet": len(res[0]), "ulike": diff, "byte_identisk": not diff, "sha256_dec": res[0]["dec.txt"], "sha256_resultat": res[0]["resultat.json"]}
    json.dump(rapport, open(ROT / "prereg" / "gjenskaping.json", "w"), indent=1); print(json.dumps(rapport, indent=1)); sys.exit(0 if not diff else 6)
if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("kommando", choices=["verifiser", "manifest", "kjor", "gjenskaping"]); ap.add_argument("--sider", default="")
    a = ap.parse_args()
    {"verifiser": verifiser, "manifest": manifest, "kjor": kjor}.get(a.kommando, lambda: gjenskaping([s for s in a.sider.split(",") if s]))()
