import json
# from serpapi import GoogleSearch
import time
# CO not to tried now as the object are too disconnected from each other
# require pacman -S tk
import pyautogui
# require pacman -S xsel (for copy and paste)
import pyperclip

import glob, os



print("now recording cursor position, you have 5 seconds")
time.sleep(7)
x1, y1 = pyautogui.position()
print(str(x1) + ' ' + str(y1))

# pre clean
os.chdir("/home/ken/Downloads")
for file in glob.glob("/home/ken/Downloads/*.html"):
    os.remove(file)


arxiv_prefix = "https://arxiv.org/abs/"
scholar_prefix = "https://scholar.google.com/scholar?q="
# serpapi_prefix = "https://serpapi.com/search?engine=google_scholar&q="
accept_list = []
start_count=15228
count=1


# this one is only responsible for read from json, grab citation cout and write (do not sort in this file). Use the other file to sort and print as usable html
with open("/home/ken/Downloads/arxiv-metadata-oai-snapshot.json", "r") as f1, open('/home/ken/open/Reading/data.txt', 'a') as f2:
    for line in f1:
        a = json.loads(line)
        
        if a["title"] == "Optimal Transport of Information":
            print(a["categories"])
            import sys
            sys.exit()
        
        for x in a["categories"].split():
            if x.startswith("q-fin") or x.startswith("econ.EM"):
                 
                # set start_count to the index you want to start (beginning at 0)
                if count < start_count:
                    count+=1echo 
                    break
                
                # temp = a["title"]
                a["title"] = a["title"].replace('\n', '').replace('\t','').replace('  ', ' ').rstrip()
                
                embed_arxiv_link = arxiv_prefix + a["id"]
                scholar_link = scholar_prefix + a["title"].replace(" ", "+").replace("&", "%26") + "&hl=en"
                # accept_list.append('<a href=' + embed_arxiv_link +'>' +a['id']+ '</a>' + '&ensp;' + '<a href=' + embed_scholar_link +'>' +'!!!' +a['title'] + '</a>' + "<br />\n")
               
                

                pyautogui.click(x=x1,y=y1)  
                pyperclip.copy(scholar_link)
                pyperclip.paste()

                pyautogui.hotkey('ctrl', 'v', interval = 0.1)
                time.sleep(1)
                pyautogui.hotkey('enter')
                time.sleep(2)
                pyautogui.hotkey('ctrl', 's', interval = 0.1)
                time.sleep(1)
                pyautogui.hotkey('enter')
                time.sleep(2)

                for file in glob.glob("*.html"):
                    if (file[0] == a['title'][0]) + (file[1] == a['title'][1]) + (file[2] == a['title'][2]) + (file[3] == a['title'][3]) + (file[4] == a['title'][4]) >=3 :
                        htmlfile = "/home/ken/Downloads/"+file
                    else:
                        print(file)
                        print(a['title'])
                        import sys
                        sys.exit()
                    break

                with open(htmlfile, "r") as f3:
                    htmlstr = f3.read()
                    start_idx = htmlstr.find("Cited by ") + 9
                    if start_idx != -1:
                        end_idx = start_idx
                        while htmlstr[end_idx].isdigit():
                            end_idx+=1
                        c_count = htmlstr[start_idx:end_idx]
                    else:
                        c_count = -1
                    f2.write(embed_arxiv_link + "||"+ a['title'] + "||"+c_count+'\n')
                # US large-cap etf
                os.remove(htmlfile)
                print(count, ":", c_count)       
                
                # add at the end
                count+=1
                # once first acceptable tag, no longer need to look at tags 
                break
                
