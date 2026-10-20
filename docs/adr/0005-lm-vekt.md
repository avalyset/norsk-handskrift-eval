# 0005. Språkmodellvekt (`--decode.language_model_weight`)

Dato: 2026-10-20. Status: akseptert, **vekt 1,0**.

## Kontekst
Modellkortet oppgir ingen vekt, og pylaia 1.1.2 krasjer med `TypeError` uten eksplisitt vekt (målt 20.10). Vekten sveipet over {0,25; 0,5; 0,75; 1,0; 1,5; 2,0}.
Litteraturprior: Tarride og Kermorvant (arXiv:2404.19317, §4.3) fant optimal vekt 1,5 for tegn- og subord-LM og 0,5 for ord-LM på NorHand v2 (steg 0,5). Vår LM er en 6-gram tegnmodell, men NorHand v3-parametrene er ikke identiske med v2.

## Målinger (rå tekst, korpus-CER/WER i %)
**A. Validation-splitten, 1 000 linjer, seedet utvalg (seed 20261020) av 22 679** (HF Teklia/NorHand-v3-line, revisjon 113280c8…):

| vekt | 0,25 | 0,5 | 0,75 | 1,0 | 1,5 | 2,0 |
|---|---|---|---|---|---|---|
| CER | 3,601 | 3,438 | 3,412 | **3,373** | 3,524 | 3,834 |
| WER | 13,135 | 12,252 | 11,968 | **11,889** | 12,047 | 12,945 |

Optimum A: **1,0**. Utvalget er 1 000 av 22 679 linjer (ikke hele validation-splitten) fordi full dekoding ville tatt ca. 10 timer per vekt; dette er et avvik fra «sveip over validation-splitten».

**B. Pilotsider, fasitlinjer (20 sider, 406 linjer, punkt 3b-utklipp):**

| vekt | 0,25 | 0,5 | 0,75 | 1,0 | 1,5 | 2,0 |
|---|---|---|---|---|---|---|
| CER | 8,528 | 8,149 | **7,897** | 7,919 | 8,350 | 8,937 |
| WER | 22,822 | 21,124 | 19,991 | **19,861** | 21,254 | 21,646 |

Optimum B (CER): **0,75**. Forskjellen til 1,0 er 0,022 prosentpoeng CER; WER er lavere ved 1,0. Sidebootstrap-KI for CER overlapper nesten helt (0,75: [5,17; 11,13], 1,0: [5,27; 11,09]).

## Beslutning
Vekt **1,0**. Begrunnelse: (1) validation-optimum er 1,0; (2) forskjellen mellom 0,75 og 1,0 i B er støy på 20 sider; (3) kjeden på pilotsidene (punkt 3b/5) er allerede kjørt med 1,0, og alle kandidatsammenligninger er dermed gjort med samme vekt.
Eirik besluttet dette 20.10.2026 etter å ha sett begge optimumene.

## Konsekvenser
- Validation deler dokumenter med train (417 av 502 dokumenter i val (distinkte ikke-tomme `urn`; 353 av 1 078 val-rader har tom `urn`) finnes også i train, målt fra `metadata_*.csv`), og LM-en er trent på train-tekst; A er derfor foreløpig og kan favorisere høyere vekt. Pilotsidene i B deler ingen dokumenter med train/val (0 av 21), men 3 av 21 har skriver i train (2 av 20 i selve 20-utvalget).
- Litteraturpriorens 1,5 er ikke bekreftet: CER ved 1,5 er høyere enn ved 1,0 både i A og B.
- Heldout måles bare med den vekten som er frosset her; den justeres ikke etterpå.
