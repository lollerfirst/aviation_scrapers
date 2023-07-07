from datetime import date, timedelta
import requests

KEYPATH = "weather_key.txt"
DBPATH = "weather_db.json"
STATION_ID = 'IPARMA61'
URI = "http://api.weather.com/v2/pws/history/daily?stationId={0}&format=json&numericPrecision=decimal&units=m&date={1}&apiKey={2}"

def main():
	global DBPATH
	global KEYPATH
	global URI
	global STATION_ID

	key = ""
	fd = 0
	try:
		with open(KEYPATH, 'r') as fd:
			key = fd.readline()

	except Exception as e:
		print("[-] COULDN'T OPEN KEY FILE")
		print(e)
		exit(-1)
	
	yesterday = date.today() - timedelta(1)
	URI = URI.format(STATION_ID, date.strftime(yesterday, "%Y%m%d"), key)
	print(URI)
	
	#headers
	headers = requests.utils.default_headers()
	headers.update(
		{
			'User-Agent': 'Mozilla/5.0'
		}
	)
	
	req = 0
	
	try:
		req = requests.get(URI, headers=headers)
	except Exception as e:
		print("[-] REQUEST ERROR")
		print(e)
		exit(-1)
	
	
	body = str(req.content)
	body = body.split("'")[1]
	body = body.replace("\\n", "")
	print(body)
	
	try:
		with open(DBPATH, 'a') as fd:
			fd.write(body)
	except Exception as e:
		print("[-] Coudn't write to db")
		print(e)
		exit(-1)
		
	print("[+] Success")
	
	
main()
