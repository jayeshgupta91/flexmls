from datetime import datetime
import os
import time
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import schedule


 
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]


creds = ServiceAccountCredentials.from_json_keyfile_name("serviceFileSheet.json", scope)
client = gspread.authorize(creds)
sheetGet = client.open("flexmls").get_worksheet(1)
sheetData = client.open("flexmls").get_worksheet(0)


def next_available_row(worksheet):
            str_list = list(filter(None, worksheet.col_values(1)))
            return str(len(str_list)+1)
# next = next_available_row(sheet)

