# 0002. Én prosess per kjøring

Dato: 2026-10-20. Status: akseptert, med forbehold.

## Kontekst
norsk-tale kjører én prosess per ytring fordi gjentatte kall i samme prosess ikke var deterministiske (whisper.cpp). For PyLaia er det ikke testet om gjentatte
dekodinger i samme prosess, eller to kjøringer av samme prosess, gir byte-identisk utdata.

## Beslutning
Hver kjøring er én ny prosess: én `pylaia-htr-decode-ctc` per (segmenterer × LM-vekt × linjeliste), og én segmenteringsprosess per segmenterer × sidemengde.
Ingen gjenbruk av prosess mellom kjøringer, og ingen tilstand mellom dem. Dette er grovere enn norsk-tale (én prosess per ytring): en kjøring dekoder hele linjelisten i batcher à 16.

## Konsekvenser
- Gjenskapingstesten i prereg (`run.py gjenskaping`: kjede kjørt to ganger i separate prosesser på 2 pilotsider, SHA256 sammenlignet for dekodingsutdata `dec.txt`, `resultat.json`, `seg/list.txt`, `seg/meta.json` uten veggklokketid «sec» og alle utklipps-PNG-er; dekoderens logg- og tidsfiler `dec.err` og `dec.time` sammenlignes ikke) er kjørt 20.10.2026; resultat og antall filer står i `prereg/gjenskaping.json` og METHOD § 15. Den dekker bare disse to sidene og én maskin; bredere ikke-determinisme er ikke testet.
- Batch-sammensetning kan påvirke utdata hvis modellen er batch-avhengig (padding/masker); batchstørrelse 16 er derfor fryst.
- Segmenteringen ga byte-identiske utklipp ved to kjøringer 20.10 (387 av 387).
