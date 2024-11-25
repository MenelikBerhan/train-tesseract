#!/usr/bin/bash
# extract Total & Unassigned Acuuracy results from ocreval accuracy reports for checkpoint traineddata
# assumes ocreval outputs to be in TRIAL_DIRECTORY/my_eval directory

if [ -z "$1" ] ; then
        echo "Error: no trial directory path given"
        exit 1
elif [ ! -d "$1" ] ; then
        echo "Error: no directory found at given path '$1'"
        exit 1
fi

EVALS_DIR="$1"/my_eval
OUTPUT_DIR="$1"/tsv
SUFF=`basename "$1"`

# set windows dir to copy results to
if [ -z "$2" ] ; then
        WIN_DIR="$d/a"
else
        WIN_DIR="$d/$2"
fi

#fls=`ls -rv "$EVALS_DIR"/eval_synth_amh-layer_*_5.log`
#echo -e "LearningIteration\tTrainingIteration\tEvalCER\tCheckpointCER" > "eval_synth_amh-layer_5-$SUFF.tsv"
#for f in $fls ; do \
#        iter=$(echo $f | egrep -o "_[0-9\._]+_" | cut -d '_' -f2-4 --output-delimiter=' ') ; \
#        eval=$(egrep "BCER eval" $f | egrep -o "[0-9\.]+," | tr -d ',');
#        echo $iter $eval | awk '{print $2"\t"$3"\t"$4"\t"$1}' >> "eval_synth_amh-layer_5-$SUFF.tsv" ; \
#done

#fls=`ls -rv "$EVALS_DIR"/eval_synth_amh-layer_*_6.log`
#echo -e "LearningIteration\tTrainingIteration\tEvalCER\tCheckpointCER" > "eval_synth_amh-layer_6-$SUFF.tsv"
#for f in $fls ; do \
#        iter=$(echo $f | egrep -o "_[0-9\._]+_" | cut -d '_' -f2-4 --output-delimiter=' ') ; \
#        eval=$(egrep "BCER eval" $f | egrep -o "[0-9\.]+," | tr -d ',');
#        echo $iter $eval | awk '{print $2"\t"$3"\t"$4"\t"$1}' >> "eval_synth_amh-layer_6-$SUFF.tsv" ; \
#done

fls=`ls -rv "$EVALS_DIR"/acc_amh-layer_*_samples.txt`
echo -e "LearningIteration\tTrainingIteration\tAccuracy\tUnassignedAcc\tCheckpointCER" > "acc_amh-layer_samples-$SUFF.tsv"
for f in $fls ; do \
        iter=$(echo $f | egrep -o "_[0-9\._]+_" | cut -d '_' -f2-4 --output-delimiter=' ') ;
        acc=$(head -20 $f | egrep " +[0-9\.]+%  Accuracy$" | egrep -o [0-9\.]+) ;
        acc_uns=$(head -20 $f | egrep ".*Unassigned$" | egrep -o "[0-9]+\.[0-9]+") ;
        echo $iter $acc $acc_uns | awk '{print $2"\t"$3"\t"$4"\t"$5"\t"$1}' >> "acc_amh-layer_samples-$SUFF.tsv" ;
done

fls=`ls -rv "$EVALS_DIR"/acc_amh-layer_*_kidane.txt`
echo -e "LearningIteration\tTrainingIteration\tAccuracy\tUnassignedAcc\tCheckpointCER" > "acc_amh-layer_kidane-$SUFF.tsv"
for f in $fls ; do \
        iter=$(echo $f | egrep -o "_[0-9\._]+_" | cut -d '_' -f2-4 --output-delimiter=' ') ;
        acc=$(head -20 $f | egrep " +[0-9\.]+%  Accuracy$" | egrep -o [0-9\.]+) ;
        acc_uns=$(head -20 $f | egrep ".*Unassigned$" | egrep -o "[0-9]+\.[0-9]+") ;
        echo $iter $acc $acc_uns | awk '{print $2"\t"$3"\t"$4"\t"$5"\t"$1}' >> "acc_amh-layer_kidane-$SUFF.tsv" ;
done

fls=`ls -rv "$EVALS_DIR"/acc_amh-layer_*_eval_6.txt`
echo -e "LearningIteration\tTrainingIteration\tAccuracy\tUnassignedAcc\tCheckpointCER" > "acc_amh-layer_eval_6-$SUFF.tsv"
for f in $fls ; do \
        iter=$(echo $f | egrep -o "_[0-9\._]+_" | cut -d '_' -f2-4 --output-delimiter=' ') ;
        acc=$(head -20 $f | egrep " +[0-9\.]+%  Accuracy$" | egrep -o [0-9\.]+) ;
        acc_uns=$(head -20 $f | egrep ".*Unassigned$" | egrep -o "[0-9]+\.[0-9]+") ;
        echo $iter $acc $acc_uns | awk '{print $2"\t"$3"\t"$4"\t"$5"\t"$1}' >> "acc_amh-layer_eval_6-$SUFF.tsv" ;
done

cp "eval_synth_amh-layer_5-$SUFF.tsv" "eval_synth_amh-layer_6-$SUFF.tsv" "acc_amh-layer_samples-$SUFF.tsv" "acc_amh-layer_kidane-$SUFF.tsv" "acc_amh-layer_eval_6-$SUFF.tsv" "$WIN_DIR"

mv "eval_synth_amh-layer_5-$SUFF.tsv" "eval_synth_amh-layer_6-$SUFF.tsv" "acc_amh-layer_samples-$SUFF.tsv" "acc_amh-layer_kidane-$SUFF.tsv" "acc_amh-layer_eval_6-$SUFF.tsv" "$OUTPUT_DIR"


