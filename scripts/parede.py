"""Parede segmentererforskjeller på pilotsidene (ADR 0004): korpus-CER (rå) for (Doc-UFCN NorHand − Kraken) og (generic − Kraken).
Paret sidebootstrap: samme sideindekser for begge kjedene; random.Random(20261020), 2 000 trekk, sortert, nedre = v[50], øvre = v[1949]
(samme prosedyre som lib.boot). Hypoteser og segmenteringsmeta som i scripts/presisjon.py og scripts/analyze.py; fasit fra
data/p20/test/page/<side>.xml via lib.parse_gt. Bare pilotsider (fast sti data/p20). Skriver results/parede-segmenterere.json. Kjøres i venv-tools."""
import sys, json, random
import numpy as np
sys.path.insert(0, "scripts"); import lib
KJEDER = {"norhand": ("work/seg/norhand", "work/p20/lm.txt"), "kraken": ("work/seg/kraken", "work/seg/kraken_lm_w1.0.txt"), "generic": ("work/seg/generic", "work/seg/generic_lm_w1.0.txt")}
def side_feil(segdir, hyp):
    meta = json.load(open(f"{segdir}/meta.json")); h = lib.load_hyp(hyp); E = {}; L = {}
    for b, m in sorted(meta.items()):
        ref = " ".join(t for t, _ in lib.parse_gt(f"data/p20/test/page/{b}.xml") if t); hy = " ".join(h.get(i, "") for i in m["order"] if h.get(i, ""))
        E[b], L[b] = lib.edits(ref, hy)
    return E, L
F = {n: side_feil(*v) for n, v in KJEDER.items()}
sider = sorted(F["kraken"][0]); assert all(sorted(F[n][0]) == sider for n in F) and len(sider) == 20
L = np.array([F["kraken"][1][s] for s in sider], float)   # samme referanse for alle kjedene
E = {n: np.array([F[n][0][s] for s in sider], float) for n in F}
cer = lambda e, ix: 100 * e[ix].sum() / L[ix].sum()
out = {"seed": 20261020, "B": 2000, "nedre_indeks": 50, "ovre_indeks": 1949, "enhet": "side (20 pilotsider)", "korpus_cer": {n: cer(E[n], slice(None)) for n in E}}
for a in ("norhand", "generic"):
    rng = random.Random(20261020); v = []
    for _ in range(2000):
        ix = [rng.randrange(len(sider)) for _ in range(len(sider))]; v.append(cer(E[a], ix) - cer(E["kraken"], ix))
    v.sort()
    side = 100 * E[a] / L - 100 * E["kraken"] / L
    out[f"{a}_minus_kraken"] = {"punkt_pp": cer(E[a], slice(None)) - cer(E["kraken"], slice(None)), "nedre": v[50], "ovre": v[1949],
                                "kraken_lavere_side_cer_antall_sider": int((side > 0).sum())}
json.dump(out, open("results/parede-segmenterere.json", "w"), indent=1); print(json.dumps(out, indent=1))
