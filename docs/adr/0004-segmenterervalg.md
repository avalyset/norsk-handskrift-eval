# 0004. Segmenterervalg

Dato: 2026-10-20. Status: **besluttet av Eirik 20.10.2026: Kraken blla i frysekandidaten.** Doc-UFCN NorHand v1-line (MIT) beholdes som dokumentert fallback.

## Kontekst
Gjenkjenneren (pylaia-norhand-v3) er fast. Tre linjesegmenterere er målt på de samme 20 pilotsidene (406 fasitlinjer), samme utklippsprosedyre (ADR 0003), samme LM-vekt (1,0, ADR 0005), samme scoring. Heldout er ikke rørt.

| Segmenterer | Lisens | Versjon / SHA256 | Linjer funnet (fasit 406) | tomme | korpus-CER % [95 % KI, sider] | median side-CER | WER % | fasitlinjer matchet IoU ≥ 0,5 / ≥ 0,3 |
|---|---|---|---|---|---|---|---|---|
| Doc-UFCN NorHand v1-line (Teklia) | MIT | HF-rev. 43ec7369…; `model.pth` 8e6e5e4f272a9b43a98de036c9164fdc522d2780e2e66dd601bde930bb14a950 | 387 | 3 | 19,78 [11,0; 33,8] | 13,04 | 35,80 | 117 / 338 |
| Doc-UFCN generic-historical-line (Teklia) | MIT | HF-rev. 3338539e…; `model.pth` b5d0659a29638446f573bec8928f3380f8643f4bee5c9ea7b8e64ae813dcc6f5 | 525 | 47 | 25,63 [19,4; 32,4] | 23,94 | 48,08 | 31 / 194 |
| Kraken `blla.mlmodel` (standardmodell) | Apache-2.0 (se «Lisens» under) | `blla.mlmodel` 77a638a83c9e535620827a09e410ed36391e9e8e8126d5796a0f15b978186056 | 520 | 27 | **13,02** [9,9; 16,4] | 14,09 | **26,74** | **359 / 382** |

Teklia har ellers `doc-ufcn-generic-page` og en YOLO-sidemodell (sidenivå, ikke linje) som ikke er prøvd. Parede forskjeller (sidebootstrap, 2 000, seed 20261020), CER-poeng:
Doc-UFCN NorHand − Kraken = +6,76 [−0,22; +18,10]; generic − Kraken = +12,61 [+6,76; +18,55]. Kraken har lavere side-CER på 10 av 20 sider. Forskjellen mot NorHand-modellen drives av få sider (side 198129: 75 → 22 % CER); medianen er lik.

## Lisens for blla.mlmodel (sjekket 20.10.2026)
Filen ligger i Krakens kildetre: `kraken/blla.mlmodel` i GitHub `mittagessen/kraken`. Installert fil (kraken 7.1.1, 5 047 020 byte) har git-blob-hash `f64b630c2b40f132f1acb1ffc90b617d5ada54a4`; samme blob ligger på tag `7.1.1` (tag-objekt `e71c1070…`, commit `a314f84f42da49a34079a4166305a7f378bb9c71`) og ble sist endret i commit `31f195ea5aa2276d70cc7bdc1de0a52fc166b51a` (2022-04-05, «change default segmentation model to one with higher resolution»).
Repoets `LICENSE` (blob `5c304d1a4a7b439f767990bf1360d3283e45d0ee`, uendret mellom tag 7.1.1 og main) er Apache License 2.0; GitHub oppgir `Apache-2.0`. Modellfila er dermed dekket av repoets lisens, så langt det kan avgjøres.
Forbehold: jeg fant ingen separat lisens- eller proveniensnotis for selve modellfila eller for treningsdataene bak den; at repolisensen dekker en binær modellfil er en slutning fra filplasseringen, ikke en uttrykkelig erklæring. `main` har siden en nyere blla-modell (commit `96316a0f…`, 2026-09-21) som **ikke** brukes.

## Anbefaling (besluttet av Eirik, se status)
**Kraken blla** som frosset segmenterer, fordi den (1) gir lavest korpus-CER og høyest linjematching, også ved IoU 0,5, (2) unngår de katastrofale sidene til Doc-UFCN NorHand, og (3) segmenterer også vertikal tekst (Doc-UFCN-skriptet vårt forkaster klasse 2). Mot: (a) forskjellen mot NorHand-modellen er ikke statistisk sikker på 20 sider (KI krysser 0), (b) Kraken finner 520 mot 406 linjer (161 umatchede funne linjer ved IoU 0,5), (c) modellfila er dekket av repoets Apache-2.0 etter plassering i kildetreet, men uten egen lisensnotis (se «Lisens»), (d) Kraken krever eget venv med torch 2.14 og pinnet scipy, (e) determinisme er ikke testet utover gjenskapingstesten i prereg, (f) målt på pilotsider som også er brukt til å velge, så anbefalingen er eksplorativ.
Alternativ ved lisensvegring: Doc-UFCN NorHand v1-line (MIT, samme prosjekt som gjenkjenneren).

## Konsekvenser
- `prereg/run.py` og manifest peker på Kraken (besluttet). Byttes beslutningen, endres `SEG` og manifestet før frys.
- Alle tre kandidater og piloten skal rapporteres i prereg-resultatet (METHOD § kandidater), uavhengig av valg.
- IoU-baserte mål er geometrisk skjeve mellom segmenterere: Doc-UFCN-polygoner er tynne masker og treffer fasitpolygonene dårlig (median beste IoU 0,45), mens Kraken-polygoner ligner fasitens. IoU 0,5 favoriserer derfor Kraken uavhengig av tekstkvalitet.
