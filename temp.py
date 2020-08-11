from deepsegment import DeepSegment
import sys

segmenter = DeepSegment('en')
file_name = sys.argv[1]
f = open(file_name, "r")
lines = f.readlines()
dialogue_str= ""
for line in lines:
    dialogue_str+=line
dialogue_str = dialogue_str.strip().replace("\n"," ")
print(dialogue_str)
output = segmenter.segment_long(dialogue_str)
print(output)
print(len(output))
