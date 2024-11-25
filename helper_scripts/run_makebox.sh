for i in *tif; do b=`basename "$i" .tif`; tesseract "$i" "box/$b" --psm 13 -l amh makebox ; done
