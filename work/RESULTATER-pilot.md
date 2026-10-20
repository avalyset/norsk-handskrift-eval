# Eksplorativ pilot, ikke preregistrert. Alle 1 562 testlinjer er sett; gjenkjenning kan ikke lenger måles bekreftende på HF-test-splitten.

Beregnet fra rådata (work/hf_nolm.txt, work/hf_lm.txt, work/p20/lm.txt) med scripts/score.py og scripts/score20.py. Rå tekst, jiwer, korpusnivå.

## Del 1: gjenkjenning alene (HF Teklia/NorHand-v3-line test, 1 562 linjer)
| | CER % | WER % | tid | toppminne |
|---|---|---|---|---|
| uten LM | 7.29 | 24.31 | 121 s | 1.29 GB |
| LM vekt 1.0 | 6.28 | 19.31 | 629 s | 1.69 GB |

## Del 2: kjede, 20 sider (seed 20261020), LM vekt 1.0
387 linjer funnet mot 406 i fasit; 3 tomme fragmenter (0.8 %); korpus CER 19.78 / WER 35.80; side-snitt CER 17.25 / WER 35.15; median CER 13.04 (kilde: results/chain-norhand.json; tidligere 19.79/17.24 kom fra scripts/score20.py, som bruker jiwer.cer over lister og avviker marginalt).

## Tillegg (20.10, etter funn av CSV-escape i HF-linjefasiten; se docs/UAVKLART.md)
Rå HF-tekst (tabellen over) er ikke endret. Med CSV-escape fjernet fra 75 linjer: uten LM CER 6.74 / WER 22.86; med LM vekt 1.0 CER 5.72 / WER 18.14.
