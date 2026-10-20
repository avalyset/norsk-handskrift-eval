# 0006. Heldout-reservasjon

Dato: 2026-10-20. Status: akseptert.

## Kontekst
Testsplitten i NorHand v3 har 81 sider. Vår pilot (seed 20261020) trakk 20 av dem. HF-linjetesten (1 562 linjer) er allerede sett i sin helhet og kan ikke lenger gi bekreftende mål.

## Beslutning
De resterende sider er reservert for en preregistrert måling. Siden `no-nb_digimanus_252116_0001` ble brukt i første enkeltsidemåling (før reservasjonen), er den flyttet til
pilotgruppen; heldout er **60 sider**, ikke 61. Fil: `work/heldout-60.txt` (side-ID, SHA256 av bildefil og PageXML-fil; hashet strømmende i minnet, uten å dekodes eller lagres).
SHA256 av selve fila: `d55ddbd3db3f6cdb3b58fd8722c08b6472dc54491c197cda6e2811c420e44f8b`. Skript som tar side- eller linje-ID-er kjører `scripts/guard.py` (`seg_kraken.py`, `seg_generic.py`, `gt_crop.py`, `analyze.py`, `dec.sh` via kommandolinje, `prereg/score.py`); den avbryter hvis en heldout-ID kommer inn. De eldre pilotskriptene `scripts/score.py`, `score20.py`, `score_val.py` og `boot1.py` er ikke vaktet (de tar ikke side-ID-er).

## Konsekvenser
- Uavklart eksponering: en tidligere gjennomgang av «metadata + PageXML» i NorHand v3 (DEV-MAP v1.3, 30.07.2026) kan ha omfattet testsidene. Se NOTE.md. Ikke kontrollerbart fra filene her.
- Forfatter/dato-metadata (`metadata_test.csv`) for alle testsider er lest som aggregat (overlappstall), ikke per heldout-side.
- **Linjenivå-eksponering:** pilot del 1 kjørte gjenkjenneren på alle 1 562 HF-testlinjer, som kommer fra alle 81 testsider inkludert heldout. Heldout er altså ikke blind på linjenivå (bilder og tekst sett, linje-CER over alle 81 sider kjent); sidenivå (segmentering og sidescoring) er urørt. Se METHOD § 5.
- Vakten er et skriptlag, ikke en teknisk sperre: bildene ligger på Zenodo og i /Volumes/Vault/norhand_v3.zip.
