# NOTE

Skript og rådata fra før 20.10.2026 kl. 07 er committet i ettertid, uten historikk. Første commit er gjort 20.10.2026 og
kan ikke vise rekkefølgen arbeidet faktisk ble gjort i. Pilotmålingene (del 1 og del 2) er kjørt 20.10.2026 før reservasjonen
av heldout-sidene (work/heldout-60.txt).

## Heldout: hva er åpnet før reservasjonen
- no-nb_digimanus_252116_0001: brukt i første enkeltsidemåling (segmentert, gjenkjent uten språkmodell, vist i rapport).
  Flyttet ut av heldout og inn i pilotgruppen. Heldout er dermed 60 sider, ikke 61.
- Sidenavn (ikke innhold) for noen testsider ble listet i en terminalutskrift. Ikke flyttet; navn avslører ikke bildeinnhold.
- metadata_test.csv (dato/forfatter for alle testsider) ble hentet til disk; kun to rader ble vist (begge pilotsider).
  Den opprinnelige filen (`data/page/test/metadata_test.csv`) ble slettet, men filen ble hentet på nytt senere samme dag: kopier av alle tre v3-splitter ligger i `data/meta/` og v2-splitter i `data/meta2/` (gitignored, brukt til overlappstall). Opprinnelig påstand «Filen er slettet» var dermed ikke varig sann.
- Linjenivå: pilot del 1 kjørte gjenkjenneren på alle 1 562 HF-testlinjer (fra alle 81 sider, også heldout; det følger av at HF-testsplitten er den offisielle testsplitten, test = 81 sider ifølge Zenodo-README og HF-kortene; linje-til-side-kobling finnes ikke i HF-dataene og er ikke kontrollert) og scoret mot HF-teksten; heldout er dermed delvis eksponert på linjenivå (METHOD § 5, ADR 0006).
- Ikke avklart: /Volumes/Vault/norhand_v3.zip (30.07.2026) og DEV-MAP v1.3 beskriver en tidligere gjennomgang av
  «metadata + PageXML» i NorHand v3 (Winge-søk). Hvilke sider det omfattet, og om fasitteksten i testsettet ble lest,
  kan ikke spores i scripts/, work/ eller shell-historikk. «Port 8-målingen 19.–20.10» er ikke funnet i noen av dem.

## Utilsiktet sletting (20.10.2026)
`work/seg/gt_lm_w0.75.{err,time,txt}` (dekodingen av fasitlinjene med LM-vekt 0,75, punkt 4) ble slettet ved et uhell av meg 20.10.2026
en gang etter kl. 08:20:48 og før ca. 08:25 lokal tid (nøyaktig tidspunkt ikke logget; nedre grense er siste skriving i work/seg/chain_dec.log), med kommandoen `rm -f work/seg/*_lm_w0.75.*`. Mønsteret var ment for en avbrutt omkjøring av kjedene
(`norhand_lm_w0.75.*`), men det traff også `gt_lm_w0.75.*`. Filene regenereres med `scripts/dec_lm.sh work/seg/gt work/seg/gt_lm_w0.75 0.75`
(tidspunkt og sammenligning mot `results/gt-w0.75.json`, CER 7,897, føres her når kjøringen er ferdig). Lærdom: aldri glob-sletting.
Regenerert 20.10.2026 08:40 (dekoding 200,9 s). Korpus-CER fra de regenererte filene er identisk med `results/gt-w0.75.json` (7,896887304063591) til alle sifre.
Byte-sammenligning er ikke mulig, siden originalfilene er borte.
