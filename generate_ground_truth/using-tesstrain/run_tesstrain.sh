#!/usr/bin/env bash

python -m tesstrain \
	--lang="amh" \
	--fonts_dir="../../fonts" \
	--langdata_dir="../../data/langdata_lstm" \
	--tessdata_dir="../../data/tessdata_best" \
	--save_box_tiff \
	--linedata_only \
	--training_text="./text-1" \
	--fontlist="FreeSerif" \
	--tmp_dir="./free-temp" \
	--output_dir="./free-output" \

