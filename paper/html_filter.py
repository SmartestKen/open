import sys
import operator

paper_list=[]
with open('/home/ken/open/Reading/data_recent.html', 'w') as f1, open('/home/ken/open/Reading/data.txt', 'r') as f2:
    for line in f2:
        tokens=line.rstrip().split("||")
        if tokens[2] == '':
            tokens[2] = 0
        else:
            tokens[2] = int(tokens[2])
       
        if tokens[0].startswith("https://arxiv.org/abs/17") or tokens[0].startswith("https://arxiv.org/abs/18") or tokens[0].startswith("https://arxiv.org/abs/19") or tokens[0].startswith("https://arxiv.org/abs/20") or tokens[0].startswith("https://arxiv.org/abs/21"):
            paper_list.append(tokens)

    f1.write("<!DOCTYPE html><head>")  
    paper_list = sorted(paper_list, key=operator.itemgetter(2), reverse=True)    

    for tokens in paper_list:
        f1.write('<a href=' + tokens[0] + '>' + str(tokens[2]) + ' ' + tokens[1] + '</a>' + "<br />\n")     
    f1.write("</head>")        

  