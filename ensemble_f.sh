if [ -z $1]
then
	echo "Missing transcript path"
else 
	A="../"
	B="$A$1"
	echo "$B"
	rm sentence-classification/senClass_predictions.txt
	rm email_intent_classification/boxer_predictions.txt
	conda deactivate
	cd email_intent_classification
	conda activate boxer
	python inference.py $B
	conda deactivate
	cd ..
	cd sentence-classification
	conda activate sentence_classification
	python sentence_cnn_save.py models/cnn $B
	conda deactivate
	cd ..
	conda activate boxer
	python ensemble.py $1
	conda deactivate
fi
