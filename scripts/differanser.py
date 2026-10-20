"""Differanser fra results/*.json (METHOD § 14): kjede minus kontroll (segmenteringens bidrag) og kontroll minus del 1 (sideutvalgets vanskelighet)."""
import json
k = json.load(open("results/gt-w1.0.json"))["corpus_cer"]
ch = {n: json.load(open(f"results/chain-{n}.json"))["corpus_cer"] for n in ("norhand", "generic", "kraken")}
del1 = {"rå_HF_tekst_LM1.0": 6.28, "uten_csv_escape_LM1.0": 5.72}   # fra work/hf_lm.txt, scripts/score.py (UAVKLART)
o = {"kontroll_cer": k, "kjede_cer": ch, "kjede_minus_kontroll_pp": {n: v - k for n, v in ch.items()}, "del1_cer_linjenivaa": del1,
     "kontroll_minus_del1_pp": {n: k - v for n, v in del1.items()}, "merknad": "kontroll er sidenivå (20 sider, 406 fasitlinjer); del 1 er linjenivå over alle 1 562 HF-testlinjer"}
json.dump(o, open("results/pilot-differanser.json", "w"), indent=1); print(json.dumps(o, indent=1))
