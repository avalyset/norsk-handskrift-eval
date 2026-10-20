#!/bin/bash
cd /Volumes/Vault/norsk-handskrift
for S in norhand generic kraken; do
  free=$(memory_pressure | grep -o "free percentage: [0-9]*" | grep -o "[0-9]*$"); [ "$free" -lt 20 ] && { echo "VAKTBRUDD minne $free% ved $S" >> work/seg/chain_dec.log; exit 3; }
  scripts/dec_lm.sh work/seg/$S work/seg/${S}_lm_w0.75 0.75; echo "$S ferdig $(head -1 work/seg/${S}_lm_w0.75.time) lines $(wc -l < work/seg/$S/list.txt)" >> work/seg/chain_dec.log
done; echo ALLE-FERDIG >> work/seg/chain_dec.log
