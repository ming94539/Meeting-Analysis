from flask import Flask, render_template, request
import subprocess
#import keras.models
import sys
import os
from datetime import datetime

app = Flask(__name__)

#global model, graph
#model, graph = init()

@app.route('/')#if they are at the main page
def index():
    return render_template('index.html')

@app.route('/predict',methods=['GET','POST'])
def predict():
    transcriptInput = request.form['transcript']
    #print('transcript input:',transcriptInput)
    dateTimeObj = datetime.now()
    timestamp = dateTimeObj.strftime("%d-%m-%Y_%H:%M:%S")
    file_path='flask_transcripts/'+timestamp+'.txt'
    temp_transcript_file = open(file_path,"w+")
    temp_transcript_file.write(transcriptInput)
    temp_transcript_file.close()
    os.system("conda activate boxer")
    #subprocess.call("./temp.sh",shell=True)



if __name__ == '__main__':
    #port = int(os.environ.get('PORT',5000))
    app.run(port = 8085)
    




