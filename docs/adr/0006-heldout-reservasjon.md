# 0006. Heldout-reservasjon

Dato: 2026-10-20. Status: akseptert.

## Kontekst
Testsplitten i NorHand v3 har 81 sider. Vår pilot (seed 20261020) trakk 20 av dem. HF-linjetesten (1 562 linjer) er allerede sett i sin helhet og kan ikke lenger gi bekreftende mål.

## Beslutning
De resterende sider er reservert for en preregistrert måling. Siden `no-nb_digimanus_252116_0001` ble brukt i første enkeltsidemåling (før reservasjonen), er den flyttet til
pilotgruppen; heldout er **60 sider**, ikke 61. Fil: `work/heldout-60.txt` (side-ID, SHA256 av bildefil og PageXML-fil; hashet strømmende i minnet, uten å dekodes eller lagres).
SHA256 av selve fila: `d55ddbd3db3f6cdb3b58fd8722c08b6472dc54491c197cda6e2811c420e44f8b`. Skript som tar side- eller linje-ID-er kjører `scripts/guard.py` (`seg.py`, `seg20.py`, `seg_kraken.py`, `seg_generic.py`, `gt_crop.py`, `analyze.py`, `dec.sh` via kommandolinje, `prereg/score.py`); den avbryter hvis en heldout-ID kommer inn. Vakten gjelder side-ID-er og linje-ID-er av formen `<side>__NNN`; HF-linje-ID-ene (`t0000`–`t1561`) er ikke koblet til side-ID-er og dekkes ikke, heller ikke av vakten i `dec.sh` (heldout-linjer i HF-testsplitten er mulig eksponert, ikke kontrollert, se under). Ikke vaktet er `scripts/score.py`, `score20.py`, `score_val.py`, `boot1.py`, `csv_escape.py`, `presisjon.py`, `differanser.py` og `parede.py`: de leser HF-linjedata (`score.py`, `boot1.py`, `csv_escape.py`: alle 1 562 HF-testlinjer fra testsplitten, mulig også fra heldout-sidene; ikke kontrollert), validation-linjer (`score_val.py`), pilotdata eller fast pilotsti (`score20.py`: `work/p20/meta.json`; `presisjon.py`, `parede.py`: `work/seg/` og `data/p20/`) eller bare `results/*.json` (`differanser.py`), ikke heldout-sider.

## Konsekvenser
- Uavklart eksponering: en tidligere gjennomgang av «metadata + PageXML» i NorHand v3 (DEV-MAP v1.3, 30.07.2026) kan ha omfattet testsidene. Se NOTE.md. Ikke kontrollerbart fra filene her.
- Forfatter/dato-metadata (`metadata_test.csv`) for alle testsider er lest som aggregat (overlappstall), ikke per heldout-side.
- **Linjenivå-eksponering:** pilot del 1 kjørte gjenkjenneren på alle 1 562 HF-testlinjer, som kommer fra testsplitten (81 sider ifølge `data/meta/metadata_test.csv` og Zenodo-README, `prereg/kilder/zenodo-10255840-README.md`; HF-kortet, `prereg/kilder/hf-NorHand-v3-line-README.md`, oppgir bare `num_examples` 1 562, ikke antall sider). Det er ikke kontrollert at hver av de 81 sidene bidrar med linjer (ingen side-ID i HF-dataene). Heldout må derfor regnes som mulig eksponert på linjenivå, i verste fall slik at alle heldout-sidene bidrar (bilder og tekst kan være sett, linje-CER over HF-testlinjene kjent); sidenivå (segmentering og sidescoring) er urørt. Se METHOD § 5.
- Vakten er et skriptlag, ikke en teknisk sperre: bildene ligger på Zenodo og i /Volumes/Vault/norhand_v3.zip.
