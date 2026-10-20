#!/bin/bash
cd /Volumes/Vault/norsk-handskrift
while pgrep -f lmsweep.sh >/dev/null; do sleep 10; done
for W in 0.25 0.5 0.75 1.5 2.0; do
  free=$(memory_pressure | grep -o "free percentage: [0-9]*" | grep -o "[0-9]*$"); [ "$free" -lt 20 ] && { echo "VAKTBRUDD minne $free% ved vekt $W" >> work/seg/gt_sweep.log; exit 3; }
  scripts/dec_lm.sh work/seg/gt work/seg/gt_lm_w$W $W; echo "vekt $W ferdig $(head -1 work/seg/gt_lm_w$W.time)" >> work/seg/gt_sweep.log
done
cp work/seg/gt_lm.txt work/seg/gt_lm_w1.0.txt; echo ALLE-FERDIG >> work/seg/gt_sweep.log
