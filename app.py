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
    return render_template('index.html',dataPie=0,displayPie=0,lineData=0,barData=0,displayCloud1=0,displayCloud2=1)
#index_without_bar.html
def reformat_sentiment(profile):
    data = []
    tempkey = ''
    for key in profile:
        tempkey = key
        break
    for sent_types in profile[tempkey]:
        tempDict = {}
        tempDict["legendText"]=sent_types
        tempDict['type']='column'
        tempDict['name']=sent_types
        tempDict['showInLegend']=True
        tempDict['axisYType']="secondary"
        tempDict['dataPoints']=[]
        for person_sent in profile: # iterates through each speaker's dictionary
            tempDict['dataPoints'].append({"label":person_sent,"y":(profile[person_sent][sent_types])*100})
        data.append(tempDict)
    return data

def get_line_sentiment(speaker_timeline_sent):
    lineData = []
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
    return lineData

def engagement_pie(transcriptInput,speakers):
    dataVal = []
    speakerDurations, total_time = get_durations(transcriptInput,speakers)
    for speaker in speakers:
        dictionary = {}
        dictionary['y']=(speakerDurations[speaker]/total_time)*100
        dictionary['speaker']=speaker
        dataVal.append(dictionary)
    dataVal=json.dumps(dataVal)
    displayPie=1
    return dataVal,displayPie
    
def create_wordCloud(transcriptInput):
    transcriptInput = transcriptInput.splitlines()
    newlines = []
    print('transcriptINPUT',transcriptInput)
    for line in transcriptInput:
        if line =="\n":
            print('empty line!')
        if line and line != "\n":
            newlines.append(line+",\n")
    newlines.insert(0,"Text,\n")
    print('IN WORDCLOUD',newlines)
    with open("transcript.csv","w") as new_csv:
        new_csv.writelines(newlines)
    from  wordCloud import run_this
    import time
    millis = str(int(round(time.time()*1000)))
    name1 = "Topic0_wordcloud"+millis+".png"
    name2 = "Topic1_wordcloud"+millis+".png"
    run_this(millis)
    return name1,name2
    

@app.route('/predict',methods=['GET','POST'])
def predict():
    dataVal = []
    displayPie=0
    lineData = []
    barData=[]
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
    if "-->" in temp[2] and ":" in temp[3]:#if has speakers and time stamps in proper zoom template
        print('transcript has speaker and timestamp')
        #Create Pie chart
        speakers = get_speakers(transcriptInput)
        dataVal,displayPie = engagement_pie(transcriptInput,speakers)
        #Clean transcript
        transcriptInput = clean_transcript(transcriptInput) #clean strip the time stamps, WEBVTT, numbers  
        #Run thru Sentiment backend
        speaker_sent, speaker_timeline_sent = get_speaker_sentiments(transcriptInput)
        #Create line chart
        lineData = get_line_sentiment(speaker_timeline_sent)
        #Create Bar chart
        sent_profiles=reformat_sentiment(speaker_sent)
        barData=json.dumps(sent_profiles)
    
    transcriptInput = clean_transcript(transcriptInput)    
    #Create Word Cloud
    print('transcript cleaned',transcriptInput)
    displayCloud1,displayCloud2=create_wordCloud(transcriptInput)
    
    results = inferencing(True,True,"models/cnn",transcriptInput)
    num_of_results = len(results)
    return render_template("index.html",results=results,num_of_results=num_of_results,dataPie=dataVal,displayPie=displayPie,lineData=lineData,displayCloud1="static/"+displayCloud1,displayCloud2="static/"+displayCloud2,barData=barData)


if __name__ == '__main__':
    #port = int(os.environ.get('PORT',5000))
    app.run(port = 8085)
    




