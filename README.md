# Information Extraction from Meeting Transcripts

## Background
This project provides a PoC of extracting meaningful information from Meeting transcripts to assist collaborators/participants to:
- write Meeting Minutes
- find specific details or highlights
... <br/>
by providing the following:<br/>
- a bird's-eye view of what was discussed
- highlights/actionable items of the meeting
- structure of the meeting

## Features
1. Actionable Item Extraction (Two pass - Ensemble approach)
2. Sentiment Analysis
3. NER 
4. Participant's Engagement Breakdown

## Setup

### Install dependencies

Clone library on github and install requirements.

```
git clone https://github.com/ming94539/Meeting-Analysis
cd Meeting-Analysis
pip3 install -r requirements.txt
```
## Running

Run the demo

```
python app.py
```
to port forward on local machine if running on remote ssh server

```
ssh -N -f -L localhost:<local port you want to display on>:localhost:<remote port> -i <private key file> exampleUser0@<IP Address>
```
