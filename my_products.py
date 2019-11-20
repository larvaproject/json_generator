import gspread
from oauth2client.service_account import ServiceAccountCredentials
from urllib.request import urlopen
import urllib.request
import json
import random

# Get a google sheets conection
def getGoogleSheetsConection():
	scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
	creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
	return gspread.authorize(creds)

# Wirte a python dictionary (json list) into json file
def writeJsonListIntoJsonFile(file_name, json_list):
	f = open(file_name, "w+")
	for _json in json_list:
		f.write(_json)
	f.close()

# return a google sheet
def getGoogleSheet(google_sheets_conector, sheet_name):
	return google_sheets_conector.open(sheet_name)

def main():
	# Connect with google sheets
	google_sheets_conector = getGoogleSheetsConection()
	# Get a google sheet
	google_sheet = getGoogleSheet(google_sheets_conector, "Product Units")
	# Set the current page in the google sheet
	worksheet = google_sheet.get_worksheet(4)
	# Set cols in the google sheet
	products = worksheet.col_values(1)
	autores = worksheet.col_values(3)

	# Open the json file
	with open("my_json.json") as f:
	    data = json.load(f)
	
	count = 0
	json_list = []
	for prod in products:
		url = 'https://csapi.claroshop.com/producto/' + prod
		webUrl = urllib.request.urlopen(url)
		dataCS = json.loads(webUrl.read().decode())
		
		data["name"] = dataCS["data"]["title"]
		data["description"] = dataCS["data"]["description"]
		data["sku"] = str(dataCS["data"]["id"])
		data["mpn"] = str(dataCS["data"]["id"])
		data["brand"]["name"] = dataCS["data"]["attributes"]["marca"] 
		data["offers"]["price"] = str(dataCS["data"]["price"])
		data["offers"]["seller"]["name"] = dataCS["data"]["store"]["name"] 
		data["review"]["author"]["name"] = autores[count]
		data["review"]["reviewRating"]['ratingValue'] = str(round(random.uniform(3.0, 4.0),1))
		data["image"] = []
		for position in range(0,len(dataCS["data"]["images"])):
			data["image"].append(dataCS["data"]["images"][position]["link"])
	
		count += 1
		json_list.append(json.dumps(data))

	# Files names:
	# json_buen_fin
	# json_productos_del_dia
	# json_corner_buen_fin
	# json_black_friday
	writeJsonListIntoJsonFile("json_black_friday.json", json_list)

if __name__ == "__main__":
	main()