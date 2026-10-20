#!/bin/bash
# usage: dec.sh <imgdir> <list> <out> [extra args]
cd /Volumes/Vault/norsk-handskrift; M=$PWD/models/pylaia-norhand-v3; D=$1; L=$2; O=$3; shift 3
venv-tools/bin/python -I scripts/guard.py "$L" || exit 9   # heldout-vakt (kode 9)
/usr/bin/time -l venv-pylaia/bin/pylaia-htr-decode-ctc --img_dirs "[$D]" --common.experiment_dirname $M --common.model_filename $M/model --common.checkpoint weights.ckpt --data.batch_size 16 --decode.include_img_ids true --decode.print_line_confidence_scores true --decode.join_string "" --decode.convert_spaces true --decode.input_space "<space>" --decode.output_space " " "$@" $M/syms.txt $L 2>$O.err >$O.txt
rc=$?   # dekoderens (time -l) exit-kode, ikke grep sin
grep -E "real|maximum resident" $O.err > $O.time
exit $rc
