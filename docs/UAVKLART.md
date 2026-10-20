# Uavklarte punkter (punkt 6), 20.10.2026

## 81 mot 82 sider: forklart
Zenodo-postens README (record 10255840, `README.md`, md5 9662d02c…) oppgir test = **81 sider**, 81 skrivere (hver testside er skrevet av en annen skriver).
Min tidligere telling på 82 kom fra zip-katalogen: `test/images/` er selv en oppføring i `namelist()`. Etter filtrering på `.jpg`: 81 bilder; `metadata_test.csv` har 81 rader med 81 unike dokumenter (`urn`) og 81 unike forfattere.

## 1 562 mot 1 573 linjer: ikke forklart
| kilde | train | val | test |
|---|---|---|---|
| Zenodo-README (`Lines`) | 230 829 | 23 017 | **1 573** |
| HF-datasettkort `Teklia/NorHand-v3-line` (`num_examples`, og faktiske parquet-rader) | 222 381 | 22 679 | **1 562** |
| Modellkort `pylaia-norhand-v3` («lines» / «horizontal lines») | 224 173 / 223 971 | 22 828 / 22 811 | 1 573 / 1 573 |

- Ingen av kildene jeg har lest forklarer differansen (11 linjer i test; 8 448 i train). Teklias publikasjon bak datasettet (DH2024, Tarride mfl., «A quantitative and qualitative evaluation of large scale handwriting recognition models for Norwegian») var ikke tilgjengelig:
  PDF-lenken på teklia.com gir `AccessDenied`, og publikasjonssiden gir 404; ingen arXiv-versjon funnet. Primærkilden er derfor **ikke lest**.
- Åpen hypotese (ikke testet på heldout): HF-eksporten dropper linjer som ikke er horisontale eller som mangler tekst/polygon. På pilotsidene har 5 av 406 fasitlinjer høyde > bredde (vertikale), men modellkortet oppgir at alle 1 573 er «horizontal», så hypotesen er svekket, ikke bekreftet.
- Modellkortets linjetall ligner Zenodos for test (1 573), men ikke for train/val, så modellkortet er trolig ikke tellet fra HF-datasettet.

## Funn: CSV-escape i HF-linjetekstene
75 av 1 562 HF-testlinjer (4,8 %) har `"` i fasiten, og alle 75 har CSV-stil-escape: teksten er omsluttet av `"…"` og indre `"` er doblet (`"bog: ""Blandt Nordpolens Naboer"""`). PageXML-teksten for samme linje er `bog: "Blandt Nordpolens Naboer"`.
Målt fra pilotsidene: av 406 PageXML-linjer finnes 34 ikke ordrett i HF-test; alle unntatt tre (de er vertikale eller trykt tekst) avviker bare ved denne escapingen.
Modellen produserer aldri `""` (0 av 75 hypoteser). Del 1 (1 562 HF-testlinjer, korpus, rå), med og uten escape-rettelse (rettelse: fjern omsluttende `"` og dobbelt-`"` → `"` når linjen starter og slutter med `"` og inneholder `""`):

| Variant | Uten språkmodell CER / WER | Med språkmodell (vekt 1,0) CER / WER |
|---|---|---|
| Rå HF-tekst (som lastet) | 7,29 / 24,31 | 6,28 / 19,31 |
| Etter escape-rettelse (75 linjer) | 6,74 / 22,86 | 5,72 / 18,14 |
| Modellkortet (oppgitt) | 7,52 / 22,99 | 6,36 / 18,11 |

Tallene i `RESULTATER-pilot.md` (rå HF-tekst) er ikke endret, men escape-korrigerte tall står der ved siden av. **Fasitkilde i prereg:** `prereg/score.py` leser fasit bare fra PageXML (`lib.parse_gt`), aldri fra HF-CSV; ingen HF-data inngår i heldout-scoringen. Kjedemålingene på pilotsidene (fasit fra PageXML) er ikke berørt.
Modellkortets 7,52/22,99 og 6,36/18,11 er derfor ikke sammenlignbare med noen av våre varianter uten at normaliseringen deres er kjent.

## Andre avvik funnet underveis
- Dato i metadata: noen datoer er ugyldige (årstall 1 i `train` og `val`; 374 manglende datoer i train, 36 i val, 4 i test).
- HF-datasettkortet sier «Norwegian Bokmål» (`language: nb`); tekstene er 1736–1950 og mye av det er dansk-norsk skriftspråk. Ikke undersøkt videre.
