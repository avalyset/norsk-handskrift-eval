# norsk-handskrift-eval

Preregistrert evaluering av norsk-handskrift-kjeden: linjesegmentering (Kraken `blla`), utklipp til 128 px og PyLaia NorHand v3 med 6-gram tegn-LM. Estimat av ytelsen på 60 reserverte NorHand v3-testsider.

- Metode: `prereg/METHOD.md` (estimering, ikke hypotesetest; avvik føres i `prereg/AVVIK.md` etter frys).
- Manifest med SHA256 for modeller, skript og heldout-liste: `prereg/manifest.json`; `python prereg/run.py verifiser` kontrollerer det (kode 2 ved avvik).
- Beslutninger: `docs/adr/`. Uavklarte punkter og kontrollfunn: `docs/UAVKLART.md`, `NOTE.md`.
- Pilotresultater: `results/`, `work/RESULTATER-pilot.md` (eksplorative, ikke preregistrert).
- **Datasettet (NorHand v3, Zenodo 10.5281/zenodo.10255840, CC BY 4.0) og modellfilene ligger ikke i repoet.** Bare id-liste og SHA256 for de reserverte sidene (`work/heldout-60.txt`) er med.

Etterskrift (OSF-ID og DOI) legges til etter frys i en egen commit.

KI-erklæring: implementert med Claude Code.
