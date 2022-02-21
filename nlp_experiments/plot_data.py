import sys, aiohttp, aiofiles, json, asyncio
sys.path.append("/home/ken/private")

from api_access import *

async def EOD_get_data(start, end, symbol, suffix = None, tempfile = "/tmp/data.html"):
	url = "https://eodhistoricaldata.com/api/eod/" + symbol + suffix + "?api_token=" + EOD_KEY + "&fmt=json&from=" + start + "&to=" + end

	async with session.get(url, headers=headers) as response:
		html = await response.text()
		async with aiofiles.open(tempfile, mode='w')  as f:
			await f.write(html)
				
		if response.status == 200:
			return json.loads(html)
		else:
			sys.exit(html)
		
		
loop = asyncio.get_event_loop()
bars = loop.run_until_complete(loop.create_task(EOD_get_data("2022-01-01", "2022-02-02", "GPSC", "INDX")))
print(bars)
