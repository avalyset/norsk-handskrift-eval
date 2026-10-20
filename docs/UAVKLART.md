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

## Gjenstående funn og mistanker etter kontrollslyngen (20.10.2026)
Kontrollrunder (fersk Opus-agent, endrede linjer ±5, feilklasse a–f): kontroll 1 = 17 verifiserte funn (V1–V17) pluss 4 støttefilfunn (K1–K4); kontroll 2 = 12 verifiserte funn; kontroll 3 = **0 verifiserte funn**. Ingen ytterligere runde er kjørt. Gjeldende manifest-hash står i `prereg/hashes.txt` (første linje).
Mistanker fra kontroll 3 som ikke kunne verifiseres (ikke rettet):
1. `docs/adr/0002-en-prosess-per-kjoring.md:16`: «byte-identiske utklipp ved to kjøringer 20.10 (387 av 387)» gjelder Doc-UFCN NorHand-segmenteren (387 linjer), ikke den frosne Kraken-kjeden (520). Målingen er ikke arkivert; gjenskapingstesten (`prereg/gjenskaping.json`) dekker Kraken-kjeden på to sider.
2. `results/test-seg-krasj.txt` (kjørt 09:42:04) er eldre enn siste endring av `scripts/seg_kraken.py` (09:42:55; bare docstring og kommentar endret, kjørbar kode lik) og oppgir ingen kodehash.
3. `prereg/kilder/hf-NorHand-v3-line-README.md` er hentet fra `raw/main`, ikke fra den pinnede revisjonen `113280c8…`, og har ingen tidsangivelse.
Andre åpne punkter (fra tidligere i dette dokumentet og METHOD § 19/§ 20):
- 1 562 mot 1 573 linjer er ikke forklart; Teklias DH2024-artikkel er ikke lest.
- En tidligere gjennomgang av NorHand v3 (30.07.2026) har ukjent omfang. «Port 8-målingen» ble ikke funnet.
- Lisensen til `blla.mlmodel` er bare dekket av repoets Apache-2.0 etter plassering i kildetreet; ingen egen notis.
- Baseline (`pylaia-norhand-v2`) er utsatt. Presisjon ved n = 60 (±1,9 pp Kraken, ±7 pp Doc-UFCN) er sannsynligvis for lav.
- `run.py kjor` mot heldout er aldri kjørt; bare `verifiser`, `gjenskaping` og scoring er testet.

## Håndtert (20.10.2026)
- **Eksponering av heldout på linjenivå (pilot del 1):** skrevet inn i `prereg/METHOD.md` § 2 («Eksponering på linjenivå») og § 20, med forbehold om at koblingen linje→side ikke er kontrollert og at ca. ni enkeltlinjer ble vist.
- **Datafiler i git:** `work/*` (unntatt heldout-lista, dens hash og `RESULTATER-pilot.md`), bilder, `*.tsv` og `*.parquet` er lagt i `.gitignore`, og historikken er renset med git filter-repo (`.git` 3 896 → 240 KiB; `git log --all` viser ingen datafiler). Filene ligger på disk. Dette omfatter også de sporede loggene `work/val1000/lm_w0.25.err` og `lm_w0.5.err`. Se METHOD § 17.

## Uløste kontrollfunn (kontroll 4, 20.10.2026, ikke rettet; frys ikke utført)
Kontrollen på METHOD/UAVKLART-diffen fant to funn som ikke er ren ordlyd (merket ANNET) og som derfor står uløst:
- `prereg/METHOD.md:21` (§ 3): sier at `work/val1000/lm_w0.25.err` og `lm_w0.5.err` er «sporet i git, lagt inn i commit 99893d3» og at `work/p20/lm.err` er «committet». Etter filter-repo finnes verken commiten eller filene i git (`git ls-files`, `git log --all --name-only`); påstanden motsier METHOD § 17 og UAVKLART «Håndtert».
- Samme linje, andre halvdel av påstanden: kontrollkommandoen «`git ls-files` 20.10.2026» gjelder tilstanden før rensingen.
Rettet i denne runden (ordlyd): METHOD:40 («bare på disk i `work/`» → `work/` og `data/`) og METHOD:119 (kortformen utvidet så den stemmer med § 2).
Ubekreftede mistanker fra kontrollen: antallet «ca. ni enkeltlinjer» har ikke belegg i en prosjektfil (de ble vist i terminalutskrift og i en rapport til Eirik); «3 896 KiB» før rensing kan ikke måles etter på; § 20 beskriver eksponeringen som ukontrollert mens UAVKLART fører punktet som håndtert (dokumentert, ikke løst).
