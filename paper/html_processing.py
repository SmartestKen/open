import sys
import operator

paper_list=[]
with open('/home/ken/open/Reading/data.html', 'w') as f1, open('/home/ken/open/Reading/data.txt', 'r') as f2:
    
    for line in f2:
        tokens=line.rstrip().split("||")
        if tokens[2] == '':
            tokens[2] = 0
        else:
            tokens[2] = int(tokens[2])
       
       
        paper_list.append(tokens)

    f1.write("<!DOCTYPE html><head>")  
    paper_list = sorted(paper_list, key=operator.itemgetter(2), reverse=True)    

    for tokens in paper_list:
        f1.write('<a href=' + tokens[0] + '>' + str(tokens[2]) + ' ' + tokens[1] + '</a>' + "<br />\n")     
    f1.write("</head>")        
        
'''       
        .sort(key=operator.itemgetter(3))
    for item in accept_list:
        f.write("%s" % item)
        f.write('<a href=' + item[0] +'>' +  item[1] + ' ' + str(item[2]) + '</a>' + "<br />\n")     
    f.write("</head>")
        

                        if '  ' in a['title']:
                    print(temp)
                    print(a['title'])
                    break
       
                results = GoogleSearch(params).get_dict()
                print(results)
                print(results["organic_results"])
                print(results["organic_results"][0])
                print(results["organic_results"][0]["inline_links"]["cited_by"]["total"])
            
            

with open("/home/ken/public/Reading/arxiv_select.html", "r") as f:

    
    
    
    
        if line == "</head>":
            break
        idx1 = line.index('!!!')
        idx2 = line.index('</a>' + "<br />\n")
        title = line[idx1+3:idx2]
        print(title)
        '''