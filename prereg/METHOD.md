# norsk-handskrift: kjedemåling på reserverte NorHand v3-testsider (prereg-utkast)

Status: **UTKAST, ikke frosset, ikke sendt til OSF.** Ingen tagg. Frys krever Eiriks ja og at feltene merket «EIRIK BESTEMMER» er fylt ut.
Strukturen følger `~/dev/norsk-tale/kalibrering/METHOD.md` (prereg-v1). Datert 2026-10-20. Alle tall i dette dokumentet er målt fra data i `work/` og `results/`.

## 1. Formål
Estimere ytelsen til en fast kjede (linjesegmentering, utklipp 128 px, PyLaia-gjenkjenning med 6-gram tegn-LM) på de **60 reserverte testsidene** i NorHand v3 (`work/heldout-60.txt`).
Dette er **estimering, ikke hypotesetest.** Ingen nullhypotese, ingen p-verdi. Resultatet er et punktestimat med 95 %-intervall og beskrivende sekundærmål.

## 2. Mål
- **Primært:** korpus side-CER på rå tekst (§ 6). Σ tegnfeil over alle 60 sider / Σ referansetegn. Bootstrap-KI 95 %, 2 000 resamplinger over **sider**, seed 20261020, prosentil: sorterte verdier, indeks 50 og 1 949 (0-basert). Én side som ikke gir noen linje teller som tom hypotese (CER 100 % for den siden) og ekskluderes aldri.
- **Sekundære:** (a) korpus side-WER (rå), (b) median og snitt av side-CER, (c) korpus CER/WER på normalisert tekst (§ 6), (d) parede linjemål ved polygon-IoU ≥ 0,5 (Hungarian, én-til-én) og ≥ 0,3: andel tapte fasitlinjer, andel umatchede funne linjer, splittede og sammenslåtte linjer, tomme fragmenter (§ 11), (e) tegnfeil per kategori (§ 11).
- Ingen sammenligning mellom heldout og pilot gjøres som test; pilottall står i § 14 bare som kontekst.

## 3. Kjede (frosset ved frys)
1. **Segmentering**, én prosess per kjøring (ADR 0002): foreslått **Kraken `blla.mlmodel`** (ADR 0004, «foreslått»; byttes mot Doc-UFCN NorHand v1-line hvis Eirik vil; beslutningen tas før frys). Polygoner sorteres på y ved linjens venstre 15 % (tolerant for skrå linjer), deretter x.
2. **Utklipp:** polygonmaske (hvitt utenfor), omskrevet rektangel, skalert til høyde 128 px, bredde = round(w·128/h), `cv2.INTER_AREA` (ADR 0003).
3. **Gjenkjenning:** `Teklia/pylaia-norhand-v3`, `pylaia-htr-decode-ctc`, batch 16, **6-gram LM med vekt 1,0** (ADR 0005), `--decode.join_string ""`, `--decode.convert_spaces true`, CPU. Én prosess per kjøring.
4. **Side-tekst** = linjetekster i sorteringsrekkefølge, tomme hoppet over, slått sammen med ett mellomrom.
5. **Fasit** = `TextEquiv/Unicode` for hver `TextLine` i PageXML, i filens rekkefølge, whitespace sammenslått, slått sammen med ett mellomrom. (HF-linjedatasettet brukes ikke: det har CSV-escape-feil i 75 av 1 562 testlinjer, se `docs/UAVKLART.md`.)

## 4. Frosset konfigurasjon
| Del | Verdi |
|---|---|
| Gjenkjenner | `Teklia/pylaia-norhand-v3`, HF-revisjon `6c97d8858f5221e7adefce28c3aa90298f684f9b`, `weights.ckpt` SHA256 `4e49b4233c9bea4cfbe9a35e239e1c25421ceed9b194b07f6ec3d96e1b1a69fc` |
| LM | `language_model.arpa.gz` `43b6a1f11ec090c604566d86058ced36507510b1ec74fb9d1e0c11c5d10a0bae`, `model` `f772db785caeac1d200615acafb57db0539c85d321972d8a65c21404e0d56c9a`, `syms.txt`, `tokens.txt`, `lexicon.txt` (alle i manifestet) |
| Segmenterer (foreslått) | Kraken 7.1.1, `blla.mlmodel` `77a638a83c9e535620827a09e410ed36391e9e8e8126d5796a0f15b978186056` |
| Alternativer (rapporteres, § 12) | Doc-UFCN NorHand v1-line `model.pth` `8e6e5e4f…14a950` (HF `43ec7369…`), Doc-UFCN generic-historical-line `model.pth` `b5d0659a…cc6f5` (HF `3338539e…`) |
| Datasett | NorHand v3, Zenodo versjon v1, DOI 10.5281/zenodo.10255840, `norhand_v3.zip` 11 693 880 999 byte, md5 `2db0cde67448f40882e3168f3c8096c4`, CC BY 4.0. HF-linjedatasett (kun for LM-vektsveip): `Teklia/NorHand-v3-line` revisjon `113280c8fbb7f6df7923ee15a7ba3c97710a8f1c`, MIT |
| Miljø | macOS 27.0.1, Apple M1 Pro, Python 3.10.6, uv 0.11.8; fire venv-er (ADR 0001): pylaia (torch 1.13.1), ufcn (torch 2.1.0), kraken (torch 2.14.0, scipy 1.13.1), tools. Eksakte versjoner: `prereg/locks/venv-*.freeze.txt` (uv pip freeze; det finnes ingen `uv.lock` fordi venv-ene ikke er et uv-prosjekt) |
| Kode | `prereg/run.py`, `prereg/score.py`, `scripts/{guard,lib,seg_kraken,seg_generic}.py`, `scripts/{dec,dec_lm}.sh`; SHA256 i `prereg/manifest.json` |
Alle lisenser: MIT, Apache-2.0 eller CC BY 4.0. Unntak å avklare: lisensen til selve `blla.mlmodel` (pakken er Apache-2.0).

## 5. Data
`work/heldout-60.txt` (SHA256 `d55ddbd3db3f6cdb3b58fd8722c08b6472dc54491c197cda6e2811c420e44f8b`): 60 side-ID-er med SHA256 for bildefil og PageXML-fil. Heldout er de 81 testsidene minus 20 pilotsider (seed 20261020) minus `no-nb_digimanus_252116_0001` (brukt i første enkeltsidemåling).
`run.py kjor` leser bare denne lista, henter hver side fra Zenodo (range-requests), sjekker SHA256 og stopper ved avvik. Skriptene avbryter hvis en heldout-ID kommer inn utenfor `run.py` (`scripts/guard.py`).
Heldout er ikke åpnet, segmentert eller gjenkjent før frys. Forbehold (NOTE.md): en tidligere gjennomgang av NorHand v3-metadata og PageXML (30.07.2026) kan ha berørt testsidene; ikke kontrollerbart.

## 6. Normalisering
- **Primær (rå):** ingen tegnendring. Sidetekster slås sammen med ett mellomrom; sammenhengende whitespace → ett mellomrom; strip. CER = jiwer `process_characters` (S+D+I) / antall referansetegn; WER = jiwer `process_words` (S+D+I) / antall referanseord (whitespace-splittet), begge summert over sider (korpusnivå).
- **Sekundær (normalisert), eksakt:** `unicodedata.normalize("NFC")` → `str.lower()` → fjern alle tegn med Unicode-kategori `P*` → whitespace → ett mellomrom → strip. Sifre, diakritikk (æøå) og symboler (kategori `S*`) beholdes. Implementasjon: `norm_text` i `prereg/score.py`.
- Ingen tallkonvertering, ingen skrivemåtenormalisering (æ/ø/å, dansk-norsk ortografi, abbreviasjoner), ingen korrektor.

## 7. Bootstrap og klynge
Enhet = **side**. Begrunnelse (målt fra `metadata_test.csv`, aggregater): alle 81 testsider er ulike dokumenter (81 `urn`) og ulike skrivere (81 forfattere), så side = dokument = skriver; klynge på dokument/skriver gir samme resampling som side, og en dyp klyngestruktur finnes ikke i testsettet.
Train/val-overlapp (aggregat for alle 81 testsider; heldout-spesifikt er bevisst ikke regnet): 0 testdokumenter finnes i train eller val; 7 av 81 testskrivere finnes i train (4 i val). Det betyr at kjeden kan være noe optimistisk for 7 skrivere. Val deler 418 av 502 dokumenter med train (derfor er LM-vekt valgt på val foreløpig, ADR 0005).

## 8. Presisjon (fra pilotens spredning)
Pilot, 20 sider, Kraken-kjede: korpus-CER 13,02 (§ 14); sidenes CER-spredning er stor (SD side-CER 15,5 pp for Doc-UFCN-kjeden; tung hale). Ved å resample 20 pilotsider til n = 60 (20 000 trekk, seed 20261020) for Doc-UFCN NorHand-kjeden (korpus-CER 19,78) fås SD for korpus-CER ≈ 3,6 pp, altså **95 %-KI-halvbredde ≈ ±7 pp** (persentilintervall 13,1–27,3). Tilsvarende for n = 20 er ±12 pp (observert KI 11,0–33,8).
Dette undervurderer sannsynligvis usikkerheten, fordi resampling fra 20 sider ikke kan gi flere ekstreme sider enn pilotens ene (side 198129). Forventning: KI-bredde på 10–15 pp totalt for primærestimatet; forskjeller mellom konfigurasjoner på under ca. 5 pp kan ikke løses med 60 sider.

## 9. Bruksterskel
**EIRIK BESTEMMER:** forhåndsdefinert terskel for «brukbar» (felt for CER og/eller WER og hvilket estimat/KI-grense som skal sammenlignes: punktestimat, øvre eller nedre KI-grense). Ikke fylt inn. Skal fastsettes før heldout kjøres.
Terskelen brukes bare til å merke utfallet «under/over», ikke til å endre kjede.

## 10. Eksklusjoner (skrevet før kjøring)
| Tilfelle | Behandling |
|---|---|
| Segmenteringen krasjer eller gir 0 linjer for en side | siden **beholdes**: tom hypotese, CER 100 %, WER 100 %; rapporteres separat med antall |
| Dekoding krasjer for en batch | én gjentatt kjøring; feiler den igjen, alle sidens linjer tom hypotese (som over) |
| Hash for bilde/PageXML avviker fra lista | **stopp**, ingen måling; avvik føres i `AVVIK.md` |
| Side uten fasit-linjer | beholdes; referanse tom → feil = antall hypotesetegn; rapporteres separat |
| Ressursvakt (minne < 20 % ledig, swap > +1 GB, intern disk < 10 GiB) | kjøringen pauses/gjenopptas; ikke en eksklusjon |
Ingen side ekskluderes på grunnlag av resultat.

## 11. Forhåndsregistrerte feilkategorier
**Segmenteringsnivå** (fra IoU-parring, ett bilde per side; heldout-primær terskel 0,5, sekundær 0,3): (S1) tapt fasitlinje: ingen funnet linje med IoU ≥ t; (S2) umatchet funnet linje; (S3) splitt: fasitlinje der ≥ 2 funne linjer hver har ≥ 50 % av eget areal inne i fasitlinjen; (S4) sammenslåing: funnet linje der ≥ 2 fasitlinjer hver har ≥ 50 % av eget areal inne i den; (S5) tomt fragment: funnet linje med tom gjenkjent tekst.
**Tegnnivå** (matchede par ved IoU ≥ 0,5; tegnjustering fra jiwer; ett tegn per kategori, prioritert i rekkefølgen): (T1) tegnsetting (Unicode `P*`); (T2) mellomrom; (T3) store/små bokstaver (kun forskjell i case); (T4) diakritikk (samme grunnbokstav etter NFD, eller par a/å, o/ø, e/æ); (T5) siffer; (T6) øvrig. Definisjonen ligger i `_cat` i `prereg/score.py`.
Kategoriene er beskrivende (antall og andel); ingen signifikanstest.

## 12. Alle kandidater og piloten rapporteres
Resultatrapporten skal inneholde, uavhengig av hva som velges: de tre segmentererkandidatene (§ 4; kandidatene som ikke er valgt kjøres på heldout **bare hvis Eirik godkjenner det før frys**; ellers rapporteres de bare på pilotsidene), pilotresultatene (§ 14), LM-vektsveipet (begge optimum, ADR 0005), og kontrollmålet med fasitlinjer på pilotsidene. Ingen kandidat utelates fordi den kom dårlig ut.

## 13. Baseline-gjenkjenner (forslag)
`Teklia/pylaia-norhand-v2` (MIT, HF-revisjon `e21ba7a2b1777a9086f46d1cdfa62b05ea488010`): samme bibliotek og samme forfattergruppe, derfor et rent «forrige versjon»-sammenligningspunkt. **Forbehold:** forholdet mellom v2-treningsdata og v3-testsidene er ikke verifisert (fare for lekkasje fra train). Ikke kjørt, ikke på heldout. Beslutning om å kjøre den hører til Eirik, før frys.

## 14. Pilot (kontekst, ikke del av estimatet; eksplorativ, ikke preregistrert)
Kilder: `results/*.json`, `docs/adr/`, `work/RESULTATER-pilot.md`. 20 sider (seed 20261020), 406 fasitlinjer:
- Fasitlinjer (kontroll, LM 1,0): korpus-CER 7,92, WER 19,86, median side-CER 5,53.
- Kjeder: Doc-UFCN NorHand CER 19,78 [11,0; 33,8]; generic-historical CER 25,63 [19,3; 32,4]; Kraken blla CER 13,02 [9,8; 16,4] (ADR 0004).
- Kontroll minus del 1 (sideutvalgets vanskelighet) og kjede minus kontroll (segmenteringens bidrag) står i `results/` og rapporten.

## 15. Gjenskaping og hasher
`prereg/run.py` er eneste inngangspunkt (`verifiser`, `manifest`, `kjor`, `gjenskaping`). `prereg/manifest.json` har SHA256 for METHOD.md, run.py, score.py (scoringsskriptet), guard.py, lib.py, segmenteringsskript, dekodingsskript, heldout-lista, locks-filene, alle modellfiler (også kandidater) og parametere. `verifiser` stopper med kode 2 ved avvik.
**Gjenskapingstest** (på 2 av de 20 pilotsidene, aldri heldout): kjede kjørt to ganger i separate prosesser; SHA256 av dekodingsutdata, segmenteringspolygoner (uten veggklokketid), alle utklipp og resultat-JSON sammenlignes; resultat i `prereg/gjenskaping.json`. Er utdata ikke byte-identisk, stopper frysen og funnet legges fram.

## 16. Avviksprotokoll
Alle endringer etter frys føres i `prereg/AVVIK.md` **før** de tas i bruk og før scoring: dato, hva (fil/§/felt), begrunnelse, hvilke mål som påvirkes, ny SHA256. Eldre oppføringer endres aldri. Eventuelle avvik fra scoringen føres før scoringsskriptet kjøres på heldout.

## 17. Personvern
Tidsspenn: hele testsplitten har dokumenter fra **1830 til 1940** (4 av 81 uten dato); train/val går til 1950 (metadata har enkelte ugyldige datoer). Skriverne i testsplitten er dermed født lenge før 1930 og er med svært høy sannsynlighet døde; tredjepersoner i brevene (barn, naboer) kan teoretisk leve for dokumenter fra 1930-årene. Data er publisert av Nasjonalbiblioteket via Zenodo under CC BY 4.0.
Vurdering: lav risiko. Regel for denne studien: **bare tall publiseres fra heldout**; ingen bilder, transkripsjoner, linjeeksempler eller navn fra heldout i rapport eller repo. Eksempellinjer hentes fra pilotsider og sjekkes for navn før publisering. Fullstendig juridisk vurdering (GDPR/personopplysningsloven for levende tredjepersoner) er ikke gjort.

## 18. Ekstern gyldighet
Heldout måler **in-distribution**: samme samling (Nasjonalbibliotekets digimanus-brev og dagbøker, 1830–1940), samme digitalisering, Teklias transkripsjonskonvensjoner, og modellene er trent på samme samling. Hver testside har en egen skriver, og 7 av 81 testskrivere finnes i train, så det er skriver-diversitet, men ikke domene-diversitet. Resultatet sier derfor ingenting om ytelse på andre arkiver, andre skannerprofiler eller andre perioder.
Forslag til ekstern samling for et senere sett (ikke hentet, ikke verifisert): norske håndskrevne kilder fra Arkivverket/Digitalarkivet (f.eks. skannede kirkebøker eller folketellingsskjemaer) med manuell fasit. Må sjekkes: lisens på bilder og transkripsjon, om manuell linjenivå-fasit finnes, og at kildene ikke inngår i NorHand-treningen.

## 19. Skjønnsvalg Eirik bør se på før frys
1. Segmenterer: Kraken blla (foreslått) mot Doc-UFCN NorHand (MIT); forskjellen på pilot er ikke sikker (KI krysser 0); lisens for blla-fila uavklart; Kraken-venv med pinnet scipy.
2. LM-vekt 1,0: valgt på validation (foreløpig fordi val deler dokumenter med train) og beholdt framfor pilotoptimum 0,75 (forskjell 0,022 pp CER, støy). Heldout kjøres ikke med annen vekt.
3. Bruksterskel (§ 9): ikke fylt inn.
4. IoU-terskel 0,5 som primær for linjematching: Doc-UFCN-polygoner treffer fasitpolygonene dårlig (median beste IoU 0,45), så terskelen favoriserer Kraken; vurder 0,3 eller en dekningsregel.
5. Rå som primær normalisering; normalisert (case + tegnsetting) som sekundær.
6. Eksklusjonsregelen «tom hypotese = CER 100 %» gjør at én segmenteringskrasj trekker korpusestimatet merkbart.
7. Primær enhet side (ikke dokument/skriver): sammenfaller i testsettet; heldout-spesifikk skriveroverlapp med train er ikke regnet.
8. Om kandidater utenom den valgte skal kjøres på heldout (§ 12), og om baseline (§ 13) skal kjøres.
9. Heldout-eksponering før reservasjon (NOTE.md): tidligere gjennomgang av NorHand-metadata/PageXML (30.07) og at `/Volumes/Vault/norhand_v3.zip` (hele datasettet) ligger lokalt.
10. HF-linjedatasettets escape-feil og at modellkortets 7,52/22,99 og 6,36/18,11 ikke kan reproduseres entydig; ingen heldout-påstand om modellkortets tall.
11. Fasit = PageXML-tekst slik den står (dansk-norsk ortografi, `"`-tegn osv.); modellen er trent på HF-tekster som kan ha andre konvensjoner.
12. Pilotsidene (20 + 252116) er brukt til både valg og tuning; de er ikke uavhengige av valgene i ADR 0004/0005.
