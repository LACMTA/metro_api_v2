from fastapi import FastAPI,Request
from pydantic import BaseModel

from app.config import Config

from app.models import *

from typing import Dict

from typing import List

from pydantic import BaseModel, Json, ValidationError
import json

import requests
import csv


# db = connect(host='', port=0, timeout=None, source_address=None)

def csv_to_json(csvFilePath, jsonFilePath):
    jsonArray = []
    headers = []
    header_row = next(csvFilePath)
    for column in header_row:
        headers.append(column)  
    print(headers)
    #read csv file
    # with open(csvFilePath, 'wb+',encoding='utf-8') as csvf: 
    #     #load csv file data using csv library's dictionary reader
    #     csvReader = csv.DictReader(csvf) 
        #convert each csv row into python dict
    for row in csvFilePath: 
        #add this python dict to json array
        the_data = {header_row[0]:row[0],
                    header_row[1]:row[1],
                    header_row[2]:row[2]}
        jsonArray.append(the_data)
  
    #convert python jsonArray to JSON String and write to file
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf: 
        jsonString = json.dumps(jsonArray, indent=4)
        jsonf.write(jsonString)
          
csvFilePath = r'data.csv'
jsonFilePath = r'../data/calendar_dates.json'

# from datetime import datetime
class CanceledServiceData(BaseModel):
    m_metro_export_trip_id: int
    trp_route: int
    stop_description_first: str
    stop_description_last: str
    trip_time_start: str
    trip_time_end: str
    type: str
    
lactmta_gtfs_rt_url = "https://lacmta.github.io/lacmta-gtfs/data/calendar_dates.txt"
response = requests.get(lactmta_gtfs_rt_url)

cr = csv.reader(response.text.splitlines())
# print(cr)
csv_to_json(cr,jsonFilePath)

app = FastAPI()
print(app)
@app.get("/calendar_dates/")
async def get_calendar_dates():
    with open('../data/calendar_dates.json', 'r') as file:
        calendar_dates = json.loads(file.read())
        return {"calendar_dates":calendar_dates}


@app.get("/canceled_service/{line}/{trip_type}")
async def get_canceled_trip(trip_type):
    with open('../data/CancelledTripsRT.json', 'r') as file:
        cancelled_service_json = json.loads(file.read())
        canceled_service = []
        for row in cancelled_service_json["CanceledService"]:
            if row["trp_type"] == trip_type:
                canceled_service.append(CanceledServiceData(m_metro_export_trip_id=row["m_metro_export_trip_id"],
                                                trp_route=row["stop_description_first"],
                                                stop_description_first=row["stop_description_first"],
                                                stop_description_last=row["stop_description_last"],
                                                trip_time_start=row["trp_time_start"],
                                                trip_time_end=row["trp_time_end"],
                                                type=row["trp_type"]))
    return {"canceled_data":canceled_service}

@app.get("/")
async def root():
    return {"Nina": "Hello World!"}