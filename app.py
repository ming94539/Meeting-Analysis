from flask import Flask, render_template, request, json
import subprocess
#import keras.models
import sys
import os
from datetime import datetime
from flask_model import inferencing
app = Flask(__name__)

#global model, graph
#model, graph = init()

@app.route('/')#if they are at the main page
def index():
    dataPoints=[{'y': 58, 'label': "Google"},
			{'y': 32, 'label': "Bing"},
			{'y': 3, 'label': "Baidu"},
			{'y': 6, 'label': "Yahoo"},
			{'y': 1, 'label': "Others"}
                ]
    dataPoints=json.dumps(dataPoints)
    return render_template('index.html',dataPie=dataPoints)

@app.route('/predict',methods=['GET','POST'])
def predict():
    transcriptInput = request.form['transcript']
    if transcriptInput[:6] == "WEBVTT" and transcriptInput[9] == "1":
        print("Raw Zoom Transcript!")
        transcriptInput=transcriptInput.splitlines()
    
        
    #Writing it into a file
    #print('transcript input:',transcriptInput)
    #dateTimeObj = datetime.now()
    #timestamp = dateTimeObj.strftime("%d-%m-%Y_%H:%M:%S")
    #file_path='flask_transcripts/'+timestamp+'.txt'
    #temp_transcript_file = open(file_path,"w+")
    #temp_transcript_file.write(transcriptInput)
    #temp_transcript_file.close()
    results = inferencing(True,True,"models/cnn",transcriptInput)
    num_of_results = len(results)
    return render_template("index.html",results=results,num_of_results=num_of_results)
    


if __name__ == '__main__':
    #port = int(os.environ.get('PORT',5000))
    app.run(port = 8085)
    




