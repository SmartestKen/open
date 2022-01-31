import json, csv, time


folder = '/home/ken/Downloads/'
json_load_path = folder + "arxiv-metadata-oai-snapshot.json"
csv_save_path = folder + 'arxiv_src.csv'


with open(json_load_path, "r") as f:
	

	csv_data = []
	category_count = dict()
	
	start = "1905"
	end = "2105"
	
	
	for line in f:
		a = json.loads(line)	
		print(a["id"])
		year = a["id"][0:4]
		if year >= start and year <= end:

			for item in a["categories"].split(" "):
				for ok_item in included_list:
					if item.startswith(ok_item):
						if category_count.get(item) == None:
							category_count[item] = 1
						else:
							category_count[item] += 1
					
					
			for item in a["categories"].split(" "):
				if item.startswith("q-fin"):
					csv_data.append([a["id"], a["title"].replace("\n", ""), a["authors_parsed"][0][1] + " " + a["authors_parsed"][0][0], a["categories"]])
					break

total_count = 0
for k,v in sorted(category_count.items(), key=lambda x: x[1], reverse=True):
	print(k, v)
	total_count += v
print("total", total_count)


with open(csv_save_path, 'w') as f:
	writer = csv.writer(f)
	writer.writerows(csv_data)
