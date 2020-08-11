if [ -z $1]
then
	echo "Missing transcript path"
else 
	rm sentence-classification/senClass_predictions.txt
	rm email_intent_classification/boxer_predictions.txt
	conda deactivate
	conda activate boxer
	python email_intent_classification/inference.py $1
	conda deactivate
	conda activate sentence_classification
	python sentence-classification/sentence_cnn_save.py sentence-classification/models/cnn $1
	conda deactivate
	conda activate boxer
	python ensemble.py $1
fi
