import re

#This file contains all the helper functions called by app.py

#Input: a string for the transcript
#Input: a list of the speakers, use get_speakers for that
#Return: speaker_output: key: speaker value: talking time
#Return: total talking time of all speakers
#Note: Haven't handle the case when there's no speaker tags for some of the utterance blocks (the speaker in this case would be the previous block's speaker)
def get_durations(transcript,speakers):
    lines = transcript.splitlines()
    speaker_output = {}
    total_talking_time=0
    for s in speakers:
        speaker_output[s] = 0
    for i in range(len(lines)):
        line  = lines[i]
        duration = 0
        #If it's a time stamp line
        if (not re.search('[a-zA-Z]',line)) and '-->' in line:
            s_hours = float(line[:2])*60*60
            s_minutes = float(line[3:5])*60
            s_seconds = float(line[6:8])
            starting_seconds = s_hours+s_minutes+s_seconds
            e_hours = float(line[17:19])*60*60
            e_minutes = float(line[20:22])*60
            e_seconds= float(line[23:25])
            end_seconds = e_hours+e_minutes+e_seconds
            duration = end_seconds - starting_seconds
            if i+1 < len(lines) and re.search('[a-zA-Z]', lines[i+1]) and ':' in lines[i+1]:
                split_l = lines[i+1].split(':')
                speaker = split_l[0]
                speaker_output[speaker]+=duration
        total_talking_time+=duration
    return speaker_output, total_talking_time

#Input: a string for the transcript
#Return: list of speakers
def get_speakers(transcript):
    lines = transcript.splitlines()
    list_of_speakers = []
    for line in lines:
        if re.search('[a-zA-Z]',line) and ':' in line:
            split_l = line.split(':')
            speaker = split_l[0]
            if speaker not in list_of_speakers:
                list_of_speakers.append(speaker)
    return list_of_speakers
#Input: a string for the transcript
#Output: remove speakers from lines
def remove_speakers(transcript):
    lines=transcript.splitlines(True)
    output = ""
    for line in lines:
        if ":" in line and not "-->" in line:
            split_l=line.split(':')
            output+=split_l[1]
    return output
#Input: a string for the transcript
#Output: a string for the transcript with time stamps, lines with numbers, and WEBVTT removed (The Zoom Format)
def clean_transcript(transcript):
    lines = transcript.splitlines(True)
    if "WEBVTT" in lines[0]:
        lines = lines[4:]
    cleaned_transcript = ""
    for line in lines:
        if '-->' in line:
            continue
        if line[0].isnumeric():
            continue
        cleaned_transcript+=line
    return cleaned_transcript

#Experimental: Still in developing phase, was going to use this for the task of adding timestamps to the Sent. Analysis line chart
def clean_transcript_numbers(transcript):
    lines = transcript.splitlines(True)
    if "WEBVTT" in lines[0]:
        lines = lines[4:]
    cleaned_transcript = ""
    counter = 0
    for line in lines:
        if '-->' in line:
            continue
        if line[0].isnumeric():
            continue
        if line == False:#if it's just \n
            continue
        if len(line) <3: #if it's '\n'
            continue
        cleaned_transcript+="["+str(counter)+"|"+line
        counter+=1
    return cleaned_transcript



