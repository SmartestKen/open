



import aiohttp
import aiofiles
import asyncio
import time

import sys
sys.path.append('/home/ken/private')

from api_access import *
import os, csv
folder = "/home/ken/Downloads/"
option = "arxiv"
if option == "arxiv":
	csv_load_path = folder + 'arxiv_src.csv'
	result_path = folder + "arxiv_result.csv"
	cache_dir = "arxiv_result_cache/"
elif option == "ssrn":
	csv_load_path = folder + "ssrn_src.csv"
	result_path = folder + "ssrn_result.csv"
	cache_dir = "ssrn_result_cache/"


temp_html_path = folder + "temp_gs.html"

async def generic_load(index):
	async with aiofiles.open(folder + cache_dir + str(index) + ".html", mode='r') as f:
		html = await f.read()

	first_cite = html.find("<span>Cite</span>")

	# likely ok
	if first_cite != -1:
		second_cite = html[first_cite+10:].find("<span>Cite</span>")
		if second_cite == -1:
			second_cite = len(html)
		else:
			# index offset
			second_cite += first_cite + 10
		start_idx = html.find(">Cited by ")
		
			
		if start_idx != -1 and start_idx < second_cite:
			start_idx = start_idx + 10
			end_idx = start_idx + 1
			while html[end_idx] != "<":
				end_idx += 1
			# print(end_idx)
			# print(html[start_idx:end_idx])
			print("LOAD", index)
			return int(html[start_idx:end_idx])
		# either no cited_by or cited_by after second cite item
		else:
			print("LOAD", index)
			return 0

	elif html.find("did not match any articles") != -1:
		print("LOAD", index)
		return -1


	print("Warning, inconsistent logic")
	time.sleep(200000)




async def generic_write(path, content):
	async with aiofiles.open(path, mode='w') as f:
		await f.write(content)


async def generic_get(url, index):	
	while True:
		async with session.get(url) as response:
			html = await response.text()
			if response.status == 200:

				first_cite = html.find("<span>Cite</span>")
				
				# likely ok
				if first_cite != -1:
					second_cite = html[first_cite+10:].find("<span>Cite</span>")
					if second_cite == -1:
						second_cite = len(html)
					else:
						# index offset
						second_cite += first_cite + 10	
						
						
					start_idx = html.find(">Cited by ")

					if start_idx != -1 and start_idx < second_cite:
						start_idx = start_idx + 10
						end_idx = start_idx + 1
						while html[end_idx] != "<":
							end_idx += 1
						# print(end_idx)
						# print(html[start_idx:end_idx])
						await generic_write(folder + cache_dir + str(index) + ".html", html)
						print("GET", index)
						return int(html[start_idx:end_idx])
					else:
						# either no cited_by or cited_by after second cite item
						await generic_write(folder + cache_dir + str(index) + ".html", html)
						print("GET", index)
						return 0
						
	
				elif html.find("did not match any articles") != -1:
					await generic_write(folder + cache_dir + str(index) + ".html", html)
					print("GET", index)
					return -1

				else:
					# no item, investigate
					print("BAD FILE", index, url)
					await generic_write(temp_html_path, html)
					time.sleep(1)
					continue 
					
			else:	
				print("waiting...", response.status)		
				time.sleep(1)


# connector = aiohttp.TCPConnector(limit=27)
connector = aiohttp.TCPConnector(limit=5)
session = aiohttp.ClientSession(connector=connector)

loop = asyncio.get_event_loop()
csv_data = []


	
# load the result, get latest,
# start at there in original csv. 
# for each batch, add into the result
# write
# note, do not sort by citation yet. can be done later
latest_id = None
import csv
restart = True


if not restart and os.path.isfile(result_path):
	with open(result_path, "r") as f:
		existing_result = list(csv.reader(f, delimiter=',')) 
		if len(existing_result) != 0:
			latest_id = existing_result[-1][0]

if restart:
	result_write_mode = "w"
else:
	result_write_mode = "a"

result = []
batch_size =  800
batch = []
tasks = []

import string
try:
	with open(csv_load_path, "r") as f:
		data = list(csv.reader(f, delimiter=','))
	for item in data:
		item_id = item[0]
		if latest_id == None or item_id > latest_id:
			
			# note item influences the final csv result, hence this part must be shared by both load and get
			if option == "ssrn":
				if item[2].startswith("Dr.") or item[2].startswith("dr."):
					item[2] = item[2][3:]
				temp_author = item[2].split(",")[0].translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
			elif option == "arxiv":
				temp_author = item[2].translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
			
			
			if os.path.isfile(folder + cache_dir + str(item_id) + ".html"):
				tasks.append([item_id])
			else:
				
				# title without punctuation
				temp_title = item[1].translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
	
				# without single letter words
				temp_title = ' '.join(word for word in temp_title.split(' ') if len(word) > 1)
				temp_author = ' '.join(word for word in temp_author.split(' ') if len(word) > 1)

							
				# space to "+"
				gs_title = temp_title.replace(" ", "+")
				# print(item[2], type(item[2]))
				gs_author = temp_author.replace(" ", "+")
				

				gs_url = "https://scholar.google.com/scholar?q="  + gs_title + "+"  + gs_author + "&hl=en"
				url = "http://api.scraperapi.com?api_key=" + SA_KEY + "&url=" + gs_url
				
				print(gs_url)
				
				tasks.append([url, item_id])
			batch.append(item)
				
			
			
			if len(batch) == batch_size or item == data[-1]:
				while True:
					try:
						executable_tasks = []
						for item in tasks:
							if len(item) == 1:
								executable_tasks.append(loop.create_task(generic_load(item[0])))
							elif len(item) == 2:
								executable_tasks.append(loop.create_task(generic_get(item[0], item[1])))
						
						ccounts = loop.run_until_complete(asyncio.gather(*executable_tasks))
						break
					except asyncio.exceptions.TimeoutError or aiohttp.client_exceptions.ServerDisconnectedError:
						print("Error, restarting service")
						loop.run_until_complete(loop.create_task(session.close()))
						connector = aiohttp.TCPConnector(limit=27)
						session = aiohttp.ClientSession(connector=connector)
						time.sleep(1)
						continue
					
				for index, ccount in enumerate(ccounts):
					result.append(batch[index] + [ccount])
					# print(ccount)

				tasks = []
				batch = []
			
				# empty basket
				with open(result_path, result_write_mode) as f:
					writer = csv.writer(f)
					writer.writerows(result)
				result = []
				
	loop.run_until_complete(loop.create_task(session.close()))	
except KeyboardInterrupt:  
	loop.run_until_complete(loop.create_task(session.close()))		
		
		

