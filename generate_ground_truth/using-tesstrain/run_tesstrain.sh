#!/usr/bin/env bash

python -m tesstrain \
	--lang="amh" \
	--fonts_dir="../../fonts" \
	--langdata_dir="../../data/langdata_lstm" \
	--tessdata_dir="../../data/tessdata_best" \
	--save_box_tiff \
	--linedata_only \
	--training_text="./text-3" \
	--fontlist="Noto Sans Ethiopic Bold" \
	--tmp_dir="./notoB-temp-3" \
	--output_dir="./notoB-output-3" \

