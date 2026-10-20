#!/usr/bin/env python3
"""norsk-handskrift prereg: scoringsskript (frysekandidat, ikke frosset; parede IoU-mål er diagnostiske; primærmål er side-CER på tekst). Leser segmenteringsmeta + hypotesefil + PageXML-katalog; skriver bare tall (ingen tekst).
usage: score.py <segdir> <hypfil> <xmldir> <ut.json> [forventet_antall_sider]          (kjøres i venv-tools)
Stopper (kode 4) hvis en linje-ID fra segmenteringen mangler i dekodingsutdata (ingen delvis scoring) eller antall sider avviker fra det forventede.
Primær: rå (sider = linjer slått sammen med ett mellomrom; fasitlinjer får whitespace sammenslått i lib.parse_gt, hypoteselinjer strippes og tomme hoppes over, men mellomrom inne i en hypoteselinje slås ikke sammen). Sekundær: normalisert (norm_text under).
Side uten funne linjer eller med krasj: hypotese = tom tekst -> CER 100 % (ikke ekskludert; primær). Sensitivitet uten krasjsider rapporteres som sekundær.
Fasit leses KUN fra PageXML ({xmldir}/{side}.xml via lib.parse_gt); HF-linjedatasettet (CSV-escape-feil) brukes aldri her."""
import sys, os, json, re, random, unicodedata, statistics as st
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import numpy as np, jiwer
import lib
import guard
from shapely.geometry import Polygon
from scipy.optimize import linear_sum_assignment
SEED = 20261020; B = 2000; IOUS = (0.5, 0.3)
def norm_text(s):
    """Sekundær normalisering: NFC, små bokstaver (str.lower), fjern alle tegn med Unicode-kategori P*, slå sammen whitespace, strip. Sifre og diakritikk beholdes."""
    s = unicodedata.normalize("NFC", s).lower()
    s = "".join(c for c in s if not unicodedata.category(c).startswith("P"))
    return re.sub(r"\s+", " ", s).strip()
def _cat(a, b):
    """kategori for ett tegnpar fra jiwer-justering (a = ref, b = hyp; tom streng = ins/del)"""
    x = a or b
    if any(c and unicodedata.category(c).startswith("P") for c in (a, b)): return "tegnsetting"   # symmetrisk: P* i ref ELLER hyp
    if " " in (a, b): return "mellomrom"
    if a and b:
        if a.lower() == b.lower(): return "store_smaa"
        da = unicodedata.normalize("NFD", a)[0]; db = unicodedata.normalize("NFD", b)[0]
        if (da.lower() == db.lower() and a != b) or {a.lower(), b.lower()} <= set("aå") or {a.lower(), b.lower()} <= set("oø") or {a.lower(), b.lower()} <= set("eæ"): return "diakritikk"
        if a.isdigit() or b.isdigit(): return "siffer"
    elif x.isdigit(): return "siffer"
    return "oevrig"
def char_cats(ref, hyp):
    out = {}
    if not ref or not hyp:   # tom side av paret: alle tegn er hhv. innsettinger/slettinger
        for c in (ref or hyp): out[_cat(c, "") if ref else _cat("", c)] = out.get(_cat(c, "") if ref else _cat("", c), 0) + 1
        return out
    o = jiwer.process_characters(ref, hyp)
    for ch in o.alignments[0]:
        if ch.type == "equal": continue
        ra = ref[ch.ref_start_idx:ch.ref_end_idx]; hb = hyp[ch.hyp_start_idx:ch.hyp_end_idx]
        n = max(len(ra), len(hb))
        for k in range(n):
            c = _cat(ra[k] if k < len(ra) else "", hb[k] if k < len(hb) else "")
            out[c] = out.get(c, 0) + 1
    return out
def ed(ref, hyp, level):
    f = jiwer.process_characters if level == "cer" else jiwer.process_words
    n = len(ref) if level == "cer" else len(ref.split())
    if not ref.strip(): return len(hyp) if level == "cer" else len(hyp.split()), 0
    if not hyp.strip(): return n, n
    o = f(ref, hyp); return o.substitutions + o.deletions + o.insertions, n
def boot(e, l, B=B, seed=SEED):
    n = len(e); rng = random.Random(seed); e = np.array(e, float); l = np.array(l, float); v = []
    for _ in range(B):
        ix = [rng.randrange(n) for _ in range(n)]; v.append(100 * e[ix].sum() / l[ix].sum())
    v.sort(); return [100 * e.sum() / l.sum(), v[50], v[1949]]
def poly(p):
    g = Polygon(p); return g if g.is_valid else g.buffer(0)
def main(segdir, hypf, xmldir, outf, forvent=None):
    meta = json.load(open(segdir + "/meta.json")); hyp = lib.load_hyp(hypf); guard.check(meta.keys())
    if forvent is not None and len(meta) != int(forvent): print("STOPP: forventet", forvent, "sider, fant", len(meta), file=sys.stderr); sys.exit(4)
    mangler = [i for m in meta.values() for i in m["order"] if i not in hyp]
    if mangler: print("STOPP: dekodingsutdata mangler", len(mangler), "linjer, f.eks.", mangler[:3], file=sys.stderr); sys.exit(4)
    pages = sorted(meta); R = {"n_pages": len(pages), "pages": {}}; crash = []
    acc = {k: ([], []) for k in ("cer", "wer", "ncer", "nwer")}; cats = {}
    seg = {t: dict(gt=0, pred=0, mat=0, ung=0, unp=0) for t in IOUS}; uavh = dict(split=0, merge=0, empty=0)
    for b in pages:
        m = meta[b]; gt = lib.parse_gt(f"{xmldir}/{b}.xml"); gtext = [t for t, _ in gt]
        if m.get("n", len(m["order"])) == 0 or "error" in m: crash.append(len(R["pages"]))
        out = [hyp.get(i, "") for i in m["order"]]
        ref = " ".join(t for t in gtext if t); h = " ".join(o for o in out if o)
        for k, (r, hh, lv) in {"cer": (ref, h, "cer"), "wer": (ref, h, "wer"), "ncer": (norm_text(ref), norm_text(h), "cer"), "nwer": (norm_text(ref), norm_text(h), "wer")}.items():
            a, n = ed(r, hh, lv); acc[k][0].append(a); acc[k][1].append(n)
        R["pages"][b] = {"cer": 100 * acc["cer"][0][-1] / max(acc["cer"][1][-1], 1), "gt_lines": len(gt), "found": len(out), "empty_pred": sum(1 for o in out if not o)}
        if not m["polys"]:
            for t in IOUS: seg[t]["gt"] += len(gt); seg[t]["ung"] += len(gt)
            continue
        G = [poly(p) for _, p in gt]; P = [poly(p) for p in m["polys"]]
        I = np.zeros((len(G), len(P))); cg = np.zeros_like(I); cp = np.zeros_like(I)
        for i, g in enumerate(G):
            for j, p in enumerate(P):
                if g.intersects(p):
                    x = g.intersection(p).area; I[i, j] = x / (g.area + p.area - x + 1e-9); cg[i, j] = x / (g.area + 1e-9); cp[i, j] = x / (p.area + 1e-9)
        ri, ci = linear_sum_assignment(-I) if I.size else ([], [])
        uavh["split"] += int(sum(1 for i in range(len(G)) if (cp[i] >= 0.5).sum() >= 2)); uavh["merge"] += int(sum(1 for j in range(len(P)) if (cg[:, j] >= 0.5).sum() >= 2)); uavh["empty"] += sum(1 for o in out if not o)
        for t in IOUS:
            S = seg[t]; pr = [(i, j) for i, j in zip(ri, ci) if I[i, j] >= t]; mg = {i for i, _ in pr}; mp = {j for _, j in pr}
            S["gt"] += len(G); S["pred"] += len(P); S["mat"] += len(pr); S["ung"] += len(G) - len(mg); S["unp"] += len(P) - len(mp)
            if t == IOUS[0]:
                for i, j in pr:
                    for c, n in char_cats(gtext[i], out[j]).items(): cats[c] = cats.get(c, 0) + n
    for k in acc: R[k] = {"korpus": 100 * sum(acc[k][0]) / max(sum(acc[k][1]), 1), "ki95_sider": boot(*acc[k])}
    pc = [v["cer"] for v in R["pages"].values()]; R["median_side_cer"] = st.median(pc); R["snitt_side_cer"] = st.mean(pc)
    rng = random.Random(SEED); mv = sorted(st.median([pc[rng.randrange(len(pc))] for _ in pc]) for _ in range(B)); R["median_side_cer_ki95"] = [mv[50], mv[1949]]
    keep = [i for i in range(len(pc)) if i not in crash]; names = sorted(R["pages"])
    R["sensitivitet_uten_krasjsider"] = {"ekskluderte_sider": [names[i] for i in crash], "n_igjen": len(keep)}
    if keep:
        for k in ("cer", "wer"): R["sensitivitet_uten_krasjsider"][k] = {"korpus": 100 * sum(acc[k][0][i] for i in keep) / max(sum(acc[k][1][i] for i in keep), 1), "ki95_sider": boot([acc[k][0][i] for i in keep], [acc[k][1][i] for i in keep])}
        kp = [pc[i] for i in keep]; R["sensitivitet_uten_krasjsider"]["median_side_cer"] = st.median(kp)
    R["segmentering_uavhengig_av_iou"] = uavh   # S3 splitt, S4 sammenslåing (areal ≥ 50 %), S5 tomt fragment
    R["segmentering"] = {str(t): dict(S, tapt_andel=S["ung"] / max(S["gt"], 1), umatchet_pred_andel=S["unp"] / max(S["pred"], 1)) for t, S in seg.items()}
    R["feilkategorier_tegn_matchede_par_iou0.5"] = cats
    json.dump(R, open(outf, "w"), indent=1, ensure_ascii=False)
if __name__ == "__main__": main(*sys.argv[1:6])
