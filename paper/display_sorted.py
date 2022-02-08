import csv

folder = "/home/ken/Downloads/"
option = "arxiv"
if option == "arxiv":
	result_path = folder + "arxiv_result.csv"
	prefix = "https://arxiv.org/abs/"
	sorted_html_path = folder + "/arxiv_sorted/arxiv_result_sorted"
elif option == "ssrn":
	result_path = folder + "ssrn_result.csv"
	prefix = "https://papers.ssrn.com/sol3/papers.cfm?abstract_id="
	sorted_html_path = folder + "/ssrn_sorted/ssrn_result_sorted"


with open(result_path, "r") as f:
	existing_result = list(csv.reader(f, delimiter=',')) 
	
batch_size = 1000
batch = []
batch_count = 0

import time
for index, item in enumerate(sorted(existing_result, key=lambda x: int(x[-1]), reverse=True)):
	
	
	link = prefix + item[0]
	print(link)
	alt_text = "[" + item[3] + "] " + item[1] +  ", " + item[-1]
	if index != 0 and prev_item[1][0:20].lower() == item[1][0:20].lower() and item[-1] == prev_item[-1]:
		continue
		
	if option == "ssrn":
		if len(item[3]) == 4 and item[3].isdigit() and item[3] <= "2019":
			continue
		elif len(item[3]) == 10 and item[3][0:4].isdigit() and item[3] <= "2019":
			continue

	scholar_link = "https://scholar.google.com/scholar?q="  + item[1].replace(" ", "+") + "+"  + item[2].replace(" ", "+") + "&hl=en"
	
	batch.append("<a href=" + scholar_link + ">" + str(index) + "</a> " + 
	"<a href=" + link + ">" + alt_text + "</a>" + "<br/>")
	if len(batch) == batch_size:
		with open(sorted_html_path + str(batch_count) + ".html", "w") as f:
			for line in batch:
				f.write(line)
		batch_count += 1
		batch = []
				

	prev_item = item
	if batch_count >= 3:
		break
