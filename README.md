# norsk-handskrift-eval

Preregistrert evaluering av norsk-handskrift-kjeden: linjesegmentering (Kraken `blla`), utklipp til 128 px og PyLaia NorHand v3 med 6-gram tegn-LM. Estimat av ytelsen på 60 reserverte NorHand v3-testsider.

- Metode: `prereg/METHOD.md` (estimering, ikke hypotesetest; avvik føres i `prereg/AVVIK.md` etter frys).
- Manifest med SHA256 for modeller, skript og heldout-liste: `prereg/manifest.json`; `python prereg/run.py verifiser` kontrollerer det (kode 2 ved avvik).
- Beslutninger: `docs/adr/`. Uavklarte punkter og kontrollfunn: `docs/UAVKLART.md`, `NOTE.md`.
- Pilotresultater: `results/`, `work/RESULTATER-pilot.md` (eksplorative, ikke preregistrert).
- **Datasettet (NorHand v3, Zenodo 10.5281/zenodo.10255840, CC BY 4.0) og modellfilene ligger ikke i repoet.** Bare id-liste og SHA256 for de reserverte sidene (`work/heldout-60.txt`) er med.

**Frysen:** tagg `prereg-v1` (commit `4b9c09544d56a13512907875adcb7585a1846746`), manifest SHA256 `9233f425e0e43712c8754ca1646b8870f9b2740b7181b1a90cda3349a2a5eac3`. Kontroller den frosne tilstanden med `git checkout prereg-v1 && python prereg/run.py verifiser`.

**OSF-registrering:** https://osf.io/uwz5n, DOI 10.17605/OSF.IO/UWZ5N (registrert 2026-10-20, offentlig, ingen embargo). Etterskrift: `prereg/METHOD.md` § 22 og `prereg/AVVIK.md`.

KI-erklæring: implementert med Claude Code.
