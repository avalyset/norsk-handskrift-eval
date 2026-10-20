"""usage: test_seg_kraken_krasj.py <arbeidskatalog> -- tvunget skrivefeil i scripts/seg_kraken.py (METHOD § 10). Kjøres med venv-kraken fra prosjektroten.
Kjører seg_kraken.py som egen prosess på én pilotside (data/p20/test/images/no-nb_digimanus_194800_0001.jpg, fast sti, aldri heldout) med cv2.imwrite
monkeypatchet til å returnere False på tredje kall. Forventet: n = 0, tom liste, feilmelding i meta.json, ingen utklipp igjen.
Skriver results/test-seg-krasj.txt. <arbeidskatalog> må ikke finnes; skriptet lager den og fjerner bare filene det selv har laget (eksplisitte stier)."""
import sys, os, json, shutil, subprocess, pathlib
SIDE = "no-nb_digimanus_194800_0001"
ROT = pathlib.Path(__file__).resolve().parent.parent
arb = pathlib.Path(sys.argv[1]).resolve(); img = arb / "img"; ut = arb / "ut"
arb.mkdir(parents=True); img.mkdir()
shutil.copy(ROT / f"data/p20/test/images/{SIDE}.jpg", img / f"{SIDE}.jpg")
PATCH = """import sys, runpy, cv2
_orig = cv2.imwrite; _n = [0]
def _imwrite(*a, **k):
    _n[0] += 1
    return False if _n[0] == 3 else _orig(*a, **k)   # tredje kall: tvunget skrivefeil
cv2.imwrite = _imwrite
sys.argv = ["scripts/seg_kraken.py", sys.argv[1], sys.argv[2]]
runpy.run_path("scripts/seg_kraken.py", run_name="__main__")
"""
r = subprocess.run([sys.executable, "-I", "-c", PATCH, str(img), str(ut)], cwd=ROT, capture_output=True, text=True)
meta = json.load(open(ut / "meta.json"))[SIDE]; liste = open(ut / "list.txt").read().split()
igjen = sorted(p.name for p in (ut / "lines").iterdir())
ok = r.returncode == 0 and meta["n"] == 0 and not liste and "error" in meta and not igjen
txt = (f"test_seg_kraken_krasj.py: tvunget skrivefeil (cv2.imwrite -> False på tredje kall), side {SIDE}\n"
       f"exit-kode seg_kraken.py: {r.returncode}\nn: {meta['n']}\nlist.txt tom: {'ja' if not liste else 'nei'}\n"
       f"error i meta.json: {'ja' if 'error' in meta else 'nei'} ({meta.get('error', '')})\nutklipp igjen i lines/: {len(igjen)}\n"
       f"resultat: {'OK' if ok else 'AVVIK'}\n")
open(ROT / "results/test-seg-krasj.txt", "w", encoding="utf8").write(txt); print(txt, end="")
for p in [img / f"{SIDE}.jpg", ut / "meta.json", ut / "list.txt"] + [ut / "lines" / n for n in igjen]: p.unlink()
for d in [img, ut / "lines", ut, arb]: d.rmdir()
sys.exit(0 if ok else 1)
