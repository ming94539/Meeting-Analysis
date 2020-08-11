import sys

file_name = sys.argv[1]

f = open(file_name,"r")
preprocessed_name = "in"
new_f = open(preprocessed_name,"w")
lines = f.readlines()
output=""
# counter = 0
for line in lines:
    previous = 0
    if len(line)>2:
        for i in range(len(line)):
            rightAfterPeriod=False
            if line[i] == '.':
                output+=line[previous: i+1]+"<EOS>"
                previous=i+1
                rightAfterPeriod=True
            elif line[i] == "\n":
                if rightAfterPeriod:
                    rightAfterPeriod=False
                    continue
                else:
                    output+=line[previous: i]+"<EOS>"

# for line in lines:
#     output+=line+"<EOS>"


new_f.write(output)

f.close()
new_f.close()
