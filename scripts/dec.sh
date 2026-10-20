#!/bin/bash
# usage: dec.sh <imgdir> <list> <out> [extra args]
cd /Volumes/Vault/norsk-handskrift; M=$PWD/models/pylaia-norhand-v3; D=$1; L=$2; O=$3; shift 3
/usr/bin/time -l venv-pylaia/bin/pylaia-htr-decode-ctc --img_dirs "[$D]" --common.experiment_dirname $M --common.model_filename $M/model --common.checkpoint weights.ckpt --data.batch_size 16 --decode.include_img_ids true --decode.print_line_confidence_scores true --decode.join_string "" --decode.convert_spaces true --decode.input_space "<space>" --decode.output_space " " "$@" $M/syms.txt $L 2>$O.err >$O.txt
grep -E "real|maximum resident" $O.err > $O.time
