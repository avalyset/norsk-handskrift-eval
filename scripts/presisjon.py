"""Presisjon ved n = 60 fra pilotens spredning (METHOD § 8). Resampler 20 pilotsider med tilbakelegging til n = 60;
numpy.random.default_rng(20261020), 20 000 trekk, rng.integers(0, 20, n). Skriver results/presisjon.json."""
import sys, json, numpy as np
sys.path.insert(0, "scripts"); import lib
def side_feil(n, hyp):
    meta = json.load(open(f"work/seg/{n}/meta.json")); h = lib.load_hyp(hyp); E = []; L = []
    for b, m in sorted(meta.items()):
        ref = " ".join(t for t, _ in lib.parse_gt(f"data/p20/test/page/{b}.xml") if t); hy = " ".join(h.get(i, "") for i in m["order"] if h.get(i, ""))
        a, c = lib.edits(ref, hy); E.append(a); L.append(c)
    return np.array(E, float), np.array(L, float)
out = {}
for n, hyp in (("norhand", "work/p20/lm.txt"), ("kraken", "work/seg/kraken_lm_w1.0.txt")):
    E, L = side_feil(n, hyp); rng = np.random.default_rng(20261020); out[n] = {"korpus_cer_pilot": 100 * E.sum() / L.sum(), "side_cer_sd": float((100 * E / L).std(ddof=1))}
    for k in (20, 60):
        v = np.array([100 * E[ix].sum() / L[ix].sum() for ix in (rng.integers(0, 20, k) for _ in range(20000))])
        out[n][f"n{k}"] = {"sd": float(v.std()), "halvbredde_1.96sd": float(1.96 * v.std()), "persentil_2.5_97.5": [float(x) for x in np.percentile(v, [2.5, 97.5])]}
json.dump(out, open("results/presisjon.json", "w"), indent=1); print(json.dumps(out, indent=1))
