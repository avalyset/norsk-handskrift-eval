# Eksplorativ pilot, ikke preregistrert. Alle 1 562 testlinjer er sett; gjenkjenning kan ikke lenger måles bekreftende på HF-test-splitten.

Beregnet fra rådata (work/hf_nolm.txt, work/hf_lm.txt, work/p20/lm.txt) med scripts/score.py og scripts/score20.py. Rå tekst, jiwer, korpusnivå.

## Del 1: gjenkjenning alene (HF Teklia/NorHand-v3-line test, 1 562 linjer)
| | CER % | WER % | tid | toppminne |
|---|---|---|---|---|
| uten LM | 7.29 | 24.31 | 121 s | 1.29 GB |
| LM vekt 1.0 | 6.28 | 19.31 | 629 s | 1.69 GB |

## Del 2: kjede, 20 sider (seed 20261020), LM vekt 1.0
387 linjer funnet mot 406 i fasit; 3 tomme fragmenter (0.8 %); korpus CER 19.79 / WER 35.80; side-snitt CER 17.24 / WER 35.15; median CER 13.04.
