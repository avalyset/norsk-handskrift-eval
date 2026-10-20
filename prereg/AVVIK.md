# Avvik og etterskrifter etter frys (prereg-v1)

Frysen er taggen `prereg-v1` (commit `4b9c09544d56a13512907875adcb7585a1846746`, manifest SHA256 `9233f425e0e43712c8754ca1646b8870f9b2740b7181b1a90cda3349a2a5eac3`). Hver endring etter frysen føres her før den tas i bruk. Eldre oppføringer endres aldri.

| Nr. | Dato | Hva endres | Begrunnelse | Påvirker | SHA256 |
|---|---|---|---|---|---|
| 1 | 2026-10-20 | `prereg/METHOD.md` § 22 (etterskrift med OSF-ID uwz5n og DOI 10.17605/OSF.IO/UWZ5N) og `README.md`. Ingen endring i metode, kode, data, hasher eller mål. | OSF-registreringen ble gjort etter taggen, så ID og DOI kunne ikke stå i den frosne teksten. | Ingen målinger. `python prereg/run.py verifiser` på `main` melder avvik for `prereg/METHOD.md` fordi `prereg/manifest.json` (frosset) har tagg-versjonens hash; frosset tilstand verifiseres på taggen. | METHOD.md i taggen `0670a8ffeb31d588974e0bac46bf0fc1a35c346c4d4a2c0ae5c753ef289dfabc`; ny METHOD.md `f8f9a844d3954af6f4c022561cd71b1857823bf5f5ed75e0eb99489fd6070423` |
