# 0001. To separate venv-er (pylaia og doc-ufcn), pluss én for Kraken

Dato: 2026-10-20. Status: akseptert.

## Kontekst
`pylaia==1.1.2` krever `torch>=1.13,<1.14`. `doc-ufcn==0.1.9` krever `torch==2.1.0`. Målt 20.10.2026: `uv pip install pylaia==1.1.2 doc-ufcn==0.1.9`
avvises som uløsbar. Kraken 7.1.1 trekker torch 2.14 og numpy 2.2.6, og scipy ≥ 1.14 feilet ved dlopen på denne Python 3.10.6-installasjonen (scipy pinnet til 1.13.1 i
venv-kraken og venv-tools).

## Beslutning
- `venv-pylaia` (torch 1.13.1, pylaia 1.1.2, setuptools<81, pip installert fordi pylaia kjører `pip freeze`),
- `venv-ufcn` (torch 2.1.0, doc-ufcn 0.1.9),
- `venv-kraken` (Kraken 7.1.1, kun for segmenteringskandidaten),
- `venv-tools` (jiwer, shapely, scipy, remotezip, pandas; scoring og analyse).
Segmentering og gjenkjenning kjøres som separate prosesser, og linjeutklipp (PNG) er grensesnittet mellom dem.

## Konsekvenser
- Ingen delt minne eller modellgraf mellom segmentering og gjenkjenning; utklipp skrives til disk.
- Pakkeversjoner fryses per venv (uv pip freeze + lock i manifestet).
- Kraken-segmentering kan ikke kjøres i samme prosess som gjenkjenneren.
