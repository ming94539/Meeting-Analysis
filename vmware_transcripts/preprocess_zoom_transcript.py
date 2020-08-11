import sys

file_name = sys.argv[1]

f = open(file_name,"r")
preprocessed_name = "preprocessed_"+file_name+".story"
new_f = open(preprocessed_name,"w")
lines = f.readlines()
new_lines = []
counter = 0
for line in lines:
    if counter < 2:
        counter+=1
        continue
    if not line[0].isnumeric():
        new_lines.append(line)
new_f.writelines(new_lines)

f.close()
new_f.close()
