#!/usr/bin/bash
# extract Total & Unassigned Acuuracy results from ocreval accuracy reports for checkpoint traineddatas
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

fls=`ls -rv "$EVALS_DIR"/eval_synth_amh-scratch_*_5.log`
echo -e "LearningIteration\tTrainingIteration\tEvalCER\tCheckpointCER" > "eval_synth_amh-scratch_5.tsv"
for f in $fls ; do \
	iter=$(echo $f | egrep -o "_[0-9\._]+_" | cut -d '_' -f2-4 --output-delimiter=' ') ; \
	eval=$(egrep "BCER eval" $f | egrep -o "[0-9\.]+," | tr -d ',');
	echo $iter $eval | awk '{print $2"\t"$3"\t"$4"\t"$1}' >> "eval_synth_amh-scratch_5.tsv" ; \
done

fls=`ls -rv "$EVALS_DIR"/eval_synth_amh-scratch_*_6.log`
echo -e "LearningIteration\tTrainingIteration\tEvalCER\tCheckpointCER" > "eval_synth_amh-scratch_6.tsv"
for f in $fls ; do \
	iter=$(echo $f | egrep -o "_[0-9\._]+_" | cut -d '_' -f2-4 --output-delimiter=' ') ; \
	eval=$(egrep "BCER eval" $f | egrep -o "[0-9\.]+," | tr -d ',');
	echo $iter $eval | awk '{print $2"\t"$3"\t"$4"\t"$1}' >> "eval_synth_amh-scratch_6.tsv" ; \
done

fls=`ls -rv "$EVALS_DIR"/acc_amh-scratch_*_samples.txt`
echo -e "LearningIteration\tTrainingIteration\tAccuracy\tUnassignedAcc\tCheckpointCER" > "acc_amh-scratch_samples.tsv"
for f in $fls ; do \
	iter=$(echo $f | egrep -o "_[0-9\._]+_" | cut -d '_' -f2-4 --output-delimiter=' ') ;
	acc=$(head -20 $f | egrep " +[0-9\.]+%  Accuracy$" | egrep -o [0-9\.]+) ;
	acc_uns=$(head -20 $f | egrep ".*Unassigned$" | egrep -o "[0-9]+\.[0-9]+") ;
	echo $iter $acc $acc_uns | awk '{print $2"\t"$3"\t"$4"\t"$5"\t"$1}' >> "acc_amh-scratch_samples.tsv" ;
done

fls=`ls -rv "$EVALS_DIR"/acc_amh-scratch_*_kidane.txt`
echo -e "LearningIteration\tTrainingIteration\tAccuracy\tUnassignedAcc\tCheckpointCER" > "acc_amh-scratch_kidane.tsv"
for f in $fls ; do \
	iter=$(echo $f | egrep -o "_[0-9\._]+_" | cut -d '_' -f2-4 --output-delimiter=' ') ;
	acc=$(head -20 $f | egrep " +[0-9\.]+%  Accuracy$" | egrep -o [0-9\.]+) ;
	acc_uns=$(head -20 $f | egrep ".*Unassigned$" | egrep -o "[0-9]+\.[0-9]+") ;
	echo $iter $acc $acc_uns | awk '{print $2"\t"$3"\t"$4"\t"$5"\t"$1}' >> "acc_amh-scratch_kidane.tsv" ;
done

fls=`ls -rv "$EVALS_DIR"/acc_amh-scratch_*_eval_6.txt`
echo -e "LearningIteration\tTrainingIteration\tAccuracy\tUnassignedAcc\tCheckpointCER" > "acc_amh-scratch_eval_6.tsv"
for f in $fls ; do \
	iter=$(echo $f | egrep -o "_[0-9\._]+_" | cut -d '_' -f2-4 --output-delimiter=' ') ;
	acc=$(head -20 $f | egrep " +[0-9\.]+%  Accuracy$" | egrep -o [0-9\.]+) ;
	acc_uns=$(head -20 $f | egrep ".*Unassigned$" | egrep -o "[0-9]+\.[0-9]+") ;
	echo $iter $acc $acc_uns | awk '{print $2"\t"$3"\t"$4"\t"$5"\t"$1}' >> "acc_amh-scratch_eval_6.tsv" ;
done

cp "eval_synth_amh-scratch_5.tsv" "eval_synth_amh-scratch_6.tsv" "acc_amh-scratch_samples.tsv" "acc_amh-scratch_kidane.tsv" "acc_amh-scratch_eval_6.tsv" "$d"/a

mv "eval_synth_amh-scratch_5.tsv" "eval_synth_amh-scratch_6.tsv" "acc_amh-scratch_samples.tsv" "acc_amh-scratch_kidane.tsv" "acc_amh-scratch_eval_6.tsv" "$OUTPUT_DIR"
