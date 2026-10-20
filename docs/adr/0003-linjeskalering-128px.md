# 0003. Linjeskalering til 128 px høyde

Dato: 2026-10-20. Status: akseptert.

## Kontekst
Modellkortet for pylaia-norhand-v3 oppgir trening med fast høyde 128 px og bevart sideforhold. HF-datasettet Teklia/NorHand-v3-line oppgir at alle bilder allerede
er skalert til 128 px høyde. PyLaia 1.1.2 avbryter ved avvikende høyde («Input images must have a fixed height ...»); målt 20.10 med utklipp i opprinnelig høyde.

## Beslutning
Segmenteringsutklipp (polygonmaske, hvit bakgrunn utenfor polygonet, avgrenset av omskrevet rektangel) skaleres til høyde 128 px med bredde = round(w·128/h),
`cv2.INTER_AREA`. HF-linjer brukes som de er (de er 128 px høye; vår Lanczos-skalering er identitet).

## Konsekvenser
- Skaleringsmetoden til Teklias treningsdata er ikke dokumentert i primærkildene jeg fant; INTER_AREA er vårt valg, ikke verifisert lik treningens.
- Polygonmaskering hvitt utenfor polygonet kan avvike fra hvordan treningslinjene ble klippet.
