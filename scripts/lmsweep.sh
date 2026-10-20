#!/bin/bash
cd /Volumes/Vault/norsk-handskrift
for W in 0.25 0.5 0.75 1.0 1.5 2.0; do
  free=$(memory_pressure | grep -o "free percentage: [0-9]*" | grep -o "[0-9]*$"); [ "$free" -lt 20 ] && { echo "VAKTBRUDD minne $free% ved vekt $W" >> work/val1000/sweep.log; exit 3; }
  scripts/dec_lm.sh work/val1000 work/val1000/lm_w$W $W; echo "vekt $W ferdig $(cat work/val1000/lm_w$W.time | head -1)" >> work/val1000/sweep.log
done
