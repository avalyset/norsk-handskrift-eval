"""Teller CSV-escape-feil i HF-linjefasiten og scorer del 1 med/uten rettelse (docs/UAVKLART.md). Skriver results/csv-escape.json."""
import sys, json; sys.path.insert(0, "scripts"); import lib
gt = {f"t{int(l.split(chr(9))[0]):04d}": l.rstrip("\n").split("\t", 1)[1] for l in open("work/hf_gt.tsv", encoding="utf8")}
unesc = lambda t: t[1:-1].replace('""', '"') if (t.startswith('"') and t.endswith('"') and '""' in t) else t
q = [i for i, t in gt.items() if '"' in t]; w = [i for i in q if unesc(gt[i]) != gt[i]]
o = {"linjer": len(gt), "med_anførselstegn": len(q), "csv_escape": len(w)}
for navn in ("nolm", "lm"):
    h = lib.load_hyp(f"work/hf_{navn}.txt")
    for tag, fn in (("raa", lambda t: t), ("rettet", unesc)):
        ce = cl = we = wl = 0
        for i, t in gt.items():
            r = fn(t); a, b = lib.edits(r, h.get(i, "")); c, d = lib.wedits(r, h.get(i, "")); ce += a; cl += b; we += c; wl += d
        o[f"{navn}_{tag}"] = {"cer": 100 * ce / cl, "wer": 100 * we / wl}
json.dump(o, open("results/csv-escape.json", "w"), indent=1); print(json.dumps(o, indent=1))
