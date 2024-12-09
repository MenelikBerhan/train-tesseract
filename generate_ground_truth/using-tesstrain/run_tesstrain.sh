#!/usr/bin/env bash

python -m tesstrain \
	--lang="amh" \
	--fonts_dir="../../fonts" \
	--langdata_dir="../../data/langdata_lstm" \
	--tessdata_dir="../../data/tessdata_best" \
	--save_box_tiff \
	--linedata_only \
	--fontlist="Droid Sans Ethiopic" \
	--training_text="./text-droid-1" \
	--tmp_dir="./droid-reg-temp-1" \
	--output_dir="./droid-reg-output-1" \

