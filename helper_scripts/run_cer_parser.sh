#!/usr/bin/bash
# extracts tab delimited BCER data from training log.
# for eval, in addition to the one from training log combines results
#	from lstmeval (run on checkpoint traineddatas)

LOG="$1"
TRIAL="$2"
LSTMEVAL="$3"	# result of running lstmeval on checkpoint traineddatas

if [ ! -f "$1" ] ; then
	echo "Error: Couldn't Find given Training Log file"
	exit 1

elif [ -z "$2" ] ; then
	echo "Error: No trial Argument"
	exit 1

# check if lstmeval file exists at given or default path
elif [ -z "$3" ] ; then
	LSTMEVAL="$TRIAL"/tsv/lstmeval_"$TRIAL".tsv
	if [ ! -f "$LSTMEVAL" ] ; then
		echo "Error: couldn't find lstmeval.tsv at Default Location $LSTMEVAL"
		exit 1
	fi
elif [ ! -f "$LSTMEVAL" ] ; then
	echo "Error: couldn't find given file $LSTMEVAL"
	exit 1
fi

# BCER per 100 iterations
echo -e 'LearningIteration\tTrainingIteration\tIterationCER' > iteration_"$TRIAL".tsv
egrep "^At iteration .* (wrote checkpoint\.|(margin=|Trial sub_trainer_ from iteration )[0-9\.]+)$" "$LOG" | \
	cut -d , -f1,4 | cut -d ' ' -f3,5 | tr '=' '/' | tr -d '%' | \
	cut -d '/' -f1,2,4  --output-delimiter=' ' | \
	awk '{print $1"\t"$2"\t"$3}' >> iteration_"$TRIAL".tsv

# BCER per 100 iterations for a Subtrainer (If any)
echo -e 'LearningIteration\tTrainingIteration\tSubtrainerCER' > sub_"$TRIAL".tsv
egrep "^UpdateSubtrainer:At iteration" "$LOG" | cut -d , -f1,4 | \
	cut -d ' ' -f3,5| tr '=' '/' | tr -d '%' | \
	cut -d '/' -f1,2,4  --output-delimiter=' ' | \
	awk '{print $1"\t"$2"\t"$3}' >> sub_"$TRIAL".tsv

# best BCER checkpoint files saved
echo -e 'LearningIteration\tTrainingIteration\tCheckpointCER' > checkpoint_"$TRIAL".tsv
egrep ":\.\./data" "$LOG" | cut -d ',' -f1,4 | \
	cut -d ' ' -f3,5 | tr '=' '/' | tr -d '%' | \
	cut -d '/' -f1,2,4  --output-delimiter=' ' | \
	awk '{print $1"\t"$2"\t"$3}' >> checkpoint_"$TRIAL".tsv

# temporary BCER eval (without training iteration)
echo -e 'LearningIteration\tEvalCER' > eval_temp.tsv
egrep "BCER eval" "$LOG" | egrep -o "[0-9\.]+At iteration.*" | \
	cut -d ' ' -f3,7 | tr '=' ',' | cut -d ',' -f1,3 --output-delimiter=' ' | \
	awk '{print $1"\t"$2}'  >> eval_temp.tsv

# BCER eval with training iteration
echo -e 'LearningIteration\tTrainingIteration\tEvalCER' > eval_"$TRIAL".tsv
liter=$(egrep "^[0-9]+" -o eval_temp.tsv)
for l in $liter ; do cer=$(egrep "^"$l eval_temp.tsv | awk '{print $NF}') ; \
	iter=$(egrep -o "^"$l".[0-9]+" iteration_"$TRIAL".tsv) ; \
	echo -e "$iter\t$cer" ; done >> eval_"$TRIAL".tsv

rm eval_temp.tsv

# BCER eval from both lstmeval (run on checkpoint traineddatas) & eval (from lstmtrain log)
echo -e 'LearningIteration\tTrainingIteration\tEvalCER\tCheckpointCER' > eval_all_"$TRIAL".tsv
sort -n eval_"$TRIAL".tsv "$LSTMEVAL" | egrep "^[0-9]+" >> eval_all_"$TRIAL".tsv

# move to windows dir
cp *_"$TRIAL".tsv "$d/a"
mv *_"$TRIAL".tsv "$TRIAL"/tsv
