import json, csv, time


folder = '/home/ken/Downloads/'
json_load_path = folder + "arxiv-metadata-oai-snapshot.json"
csv_save_path = folder + 'arxiv_src.csv'


with open(json_load_path, "r") as f:
	

	csv_data = []

	
	start = "1905"
	
	
	for line in f:
		a = json.loads(line)	
		print(a["id"])
		year = a["id"][0:4]
		if year >= start:				
			for item in a["categories"].split(" "):
				if item.startswith("q-fin"):
					csv_data.append([a["id"], a["title"].replace("\n", ""), a["authors_parsed"][0][1] + " " + a["authors_parsed"][0][0], a["categories"]])
					break


with open(csv_save_path, 'w') as f:
	writer = csv.writer(f)
	writer.writerows(csv_data)
