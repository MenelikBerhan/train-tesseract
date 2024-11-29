#!/usr/bin/env bash

python -m tesstrain \
	--fontlist="Noto Sans Ethiopic" \
	--fonts_dir="../../fonts" \
	--tmp_dir="./temp" \
	--lang="amh" \
	--langdata_dir="../../data/langdata" \
	--output_dir="./output" \
	--save_box_tiff \
	--linedata_only \
	--training_text="./amh-layer.training_txt" \
	--tessdata_dir="../../data/tessdata" \

