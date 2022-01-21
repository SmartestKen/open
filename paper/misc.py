
# compare two scrape run
import csv

folder = "/home/ken/Downloads/"
src1_path = folder + "ssrn_src.csv"
src2_path = folder + "ssrn_src1.csv"

with open(src1_path, "r") as f:
	src1 = list(csv.reader(f, delimiter=',')) 
with open(src2_path, "r") as f:
	src2 = list(csv.reader(f, delimiter=',')) 

src1_ids = set([item[0] for item in src1])
src2_ids = set([item[0] for item in src2])

print(src1_ids - src2_ids)
print(src2_ids - src1_ids)

output_html_path = folder + "misc_output.html"

with open(output_html_path, "w") as f:
	for item in src1_ids - src2_ids:
		link = "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=" + item
		alt_text = link
		
		f.write("<a href=" + link + ">" + alt_text + "</a> " + "<br/>")
