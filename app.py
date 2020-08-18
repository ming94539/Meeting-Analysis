from flask import Flask, render_template, request, json
import subprocess
#import keras.models
import sys
import os
from datetime import datetime
from flask_model import inferencing
from sent_analysis import get_speaker_sentiments
from process_transcripts import get_speakers,get_durations,clean_transcript
app = Flask(__name__)

#global model, graph
#model, graph = init()

@app.route('/')#if they are at the main page
def index():
    dataPoints = [
            {'y': 20, 'label': "Example Speaker 1"}
            ]
    dataPoints=json.dumps(dataPoints)
    lineData=[{
            'type':"line",
            'name': "Pallavi",
            'showInLegend': True,
            'dataPoints': [		
                { 'x': 0.1, 'y': .93 },
                { 'x': 0.2, 'y':.5 },
                { 'x': 0.3, 'y': .3 },
                {'x': 0.5, 'y':0.4}
            ]
          },
           {
            'type':"line",
            'name': "Kunal",
            'showInLegend': True,
            'dataPoints': [		
                { 'x': 0.1, 'y': .53 },
                { 'x': 0.2, 'y':.55 },
                { 'x': 0.3, 'y': .34 },
                {'x': 0.5, 'y':0.1}
            ]
          }
           
       ]
    lineData=json.dumps(lineData)
    return render_template('index.html',dataPie=dataPoints,displayPie=0,lineData=lineData)

@app.route('/predict',methods=['GET','POST'])
def predict():
    dataVal = []
    displayPie=0
    lineData = []
    transcriptInput = request.form['transcript']
    #Get speakers and speaker durations
    otemp = transcriptInput.splitlines()
    temp = []
    for line in otemp:
        if len(line) == 2 and '/n' in line:
            continue
        if len(line) == 0:
            continue
        temp.append(line)
    print(temp)
    if "-->" in temp[2] and ":" in temp[3]:#if has speakers and time stamps in proper zoom template
        print('transcript has speaker and timestamp')
        speakers = get_speakers(transcriptInput)
        speakerDurations, total_time = get_durations(transcriptInput,speakers)
        for speaker in speakers:
            dictionary = {}
            dictionary['y']=(speakerDurations[speaker]/total_time)*100
            dictionary['name']=speaker
            dataVal.append(dictionary)
        dataVal=json.dumps(dataVal)
        displayPie=1 
        transcriptInput = clean_transcript(transcriptInput) #clean strip the time stamps, WEBVTT, numbers  
        print(transcriptInput)     
        speaker_sent, speaker_timeline_sent = get_speaker_sentiments(transcriptInput)
        print(speaker_sent)
        print(speaker_timeline_sent)
        for key in speaker_timeline_sent:
            tempDic={}
            tempDic['type']='line'
            tempDic['name']=key
            tempDic['showInLegend']=True
            tempDic['dataPoints'] = []
            for sent in speaker_timeline_sent[key]:
                tempDic['dataPoints'].append({'x':sent,'y':speaker_timeline_sent[key][sent]})
            lineData.append(tempDic)
        lineData=json.dumps(lineData)
    transcriptInput = clean_transcript(transcriptInput)
    results = inferencing(True,True,"models/cnn",transcriptInput)
    num_of_results = len(results)
    return render_template("index.html",results=results,num_of_results=num_of_results,dataPie=dataVal,displayPie=displayPie,lineData=lineData)
    


if __name__ == '__main__':
    #port = int(os.environ.get('PORT',5000))
    app.run(port = 8085)
    




