


async def get_data(start, end, symbol, suffix = None, tempfile = "/tmp/data.html"):
	url = "https://eodhistoricaldata.com/api/eod/" + symbol + suffix + "?api_token=" + EOD_KEY + "&fmt=json&from=" + start + "&to=" + end


	async with session.get(url, headers=headers) as response:
		html = await response.text()
		if filename != None:
			async with aiofiles.open(filename, mode='w')  as f:
				await f.write(html)
				
		if response.status == 200:
			if api != "newyorkfed":
				return json.loads(html)
			else:					
				return float(ET.fromstring(html)[0][1][2].text)
		elif response.status == 404 and url.startswith(AP_BASE + "/v2/positions/"):
			return {"qty": 0}
		else:
			sys.exit(html)
		
		
		
		
		

# note; INJECTION attack possible. Hence not to be exposed to user input
async def get_historical_data(start, end, symbol, suffix = None):
	
	pkey = "date"
	
	if symbol != "INTEREST":
		cur.execute("CREATE TABLE IF NOT EXISTS " + symbol + "(" + pkey + " primary key, open, high, low, close, volume)")
	else:
		cur.execute("CREATE TABLE IF NOT EXISTS " + symbol + "(" + pkey + " primary key, rate)")


	
	cur.execute("SELECT * FROM " + symbol + " WHERE " + pkey + "=(SELECT max(" + pkey + ") FROM " + symbol + ")")
	last_record = cur.fetchall()
	if len(last_record) == 0:
		http_start = "1970-01-01"
	else:
		end_of_data = last_record[-1][0]
		if end_of_data < end:
			# regardless whether end_of_data is before or after start, fetch from end_of_data to preserve consecutiveness
			http_start = end_of_data
		else:
			cur.execute("SELECT * FROM " + symbol + " WHERE " + pkey + " >= ? and " + pkey + " <= ?", (start, end))
			return cur.fetchall()
	
	
	
	if symbol != "INTEREST":
		url = "https://eodhistoricaldata.com/api/eod/" + symbol + suffix + "?api_token=" + EOD_KEY + "&fmt=json&from=" + http_start + "&to=" + end
	else:
		url = "https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE&interval=daily&apikey=" + AV_KEY
		
	print(url)
	data_list = []
	
	async with session.get(url) as response:
		print("historical api Status:", response.status)
		html = await response.text()
		html = json.loads(html)

		if symbol != "INTEREST":
			for bar in html:
				data_list.append([bar["date"], bar["open"], bar["high"], bar["low"], bar["close"], bar["volume"]])
				# print(bar)
			cur.executemany("INSERT OR IGNORE INTO " + symbol + " (" + pkey + ", open, high, low, close, volume) VALUES (?,?,?,?,?,?)", data_list)
		else:
			for bar in html["data"]:
				data_list.append([bar["date"], bar["value"]])
			
			cur.executemany("INSERT OR IGNORE INTO " + symbol + " (" + pkey + ", rate) VALUES (?,?)", data_list)
		db.commit()
		
		
		
		cur.execute("SELECT * FROM " + symbol + " WHERE " + pkey + " >= ? AND " + pkey + " <= ?", (start, end))
		return cur.fetchall()

