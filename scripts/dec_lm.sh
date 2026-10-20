#!/bin/bash
# usage: dec_lm.sh <segdir> <outprefix> [vekt]
cd /Volumes/Vault/norsk-handskrift; M=$PWD/models/pylaia-norhand-v3; W=${3:-1.0}
scripts/dec.sh $1/lines $1/list.txt $2 --decode.use_language_model true --decode.language_model_path $M/language_model.arpa.gz --decode.tokens_path $M/tokens.txt --decode.lexicon_path $M/lexicon.txt --decode.language_model_weight $W
