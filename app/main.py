import json

from starlette.middleware.cors import CORSMiddleware

import requests
import csv
import heapq
import itertools


from fastapi import FastAPI,Request

from app.config import Config
from app.models import *
from app.ftp_connector import *

from typing import Dict, List

from pydantic import BaseModel, Json, ValidationError
from datetime import datetime

import pytz


app = FastAPI(docs_url="/")
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

def standardize_string(input_string):
    return input_string.lower().replace(" ", "")

@app.get("/canceled_service_summary/")
async def get_canceled_trip_summary():
    print('get_canceled_trip_summary')
    json_file_path = "../data/CancelledTripsRT.json"
    with open(json_file_path, 'r') as file:
        canceled_trips = json.loads(file.read())
        canceled_trips_summary = {}
        total_canceled_trips = 0
        for trip in canceled_trips["CanceledService"]:
            # route_number = standardize_string(trip["trp_route"])
            route_number = standardize_string(trip["trp_route"])
            if route_number:
                if route_number not in canceled_trips_summary:
                    canceled_trips_summary[route_number] = 1
                else:
                    canceled_trips_summary[route_number] += 1
                total_canceled_trips += 1
        modified_time = datetime.fromtimestamp((ftp_json_file_time)).astimezone(pytz.timezone("America/Los_Angeles"))
        formatted_modified_time = modified_time.strftime('%Y-%m-%d %H:%M:%S')
        return {"canceled_trips_summary":canceled_trips_summary,
                "total_canceled_trips":total_canceled_trips,
                "last_updated":formatted_modified_time}

@app.get("/canceled_service/line/{line}")
async def get_canceled_trip(line):
    with open('../data/CancelledTripsRT.json', 'r') as file:
        cancelled_service_json = json.loads(file.read())
        canceled_service = []
        for row in cancelled_service_json["CanceledService"]:
            if row["trp_type"] == "REG" and standardize_string(row["trp_route"]) == line:
                canceled_service.append(CanceledServiceData(m_metro_export_trip_id=row["m_metro_export_trip_id"],
                                                    trp_route=row["trp_route"],
                                                    stop_description_first=row["stop_description_first"],
                                                    stop_description_last=row["stop_description_last"],
                                                    trip_time_start=row["trp_time_start"],
                                                    trip_time_end=row["trp_time_end"],
                                                    trip_direction=row["trp_direction"],                                                    
                                                    type=row["trp_type"]))
    return {"canceled_data":canceled_service}

@app.get("/canceled_service/all/")
async def get_canceled_trip():
    with open('../data/CancelledTripsRT.json', 'r') as file:
        cancelled_service_json = json.loads(file.read())
        canceled_service = cancelled_service_json["CanceledService"]
        for row in cancelled_service_json["CanceledService"]:
            if row["trp_type"] == "REG":
                canceled_service.append(CanceledServiceData(m_metro_export_trip_id=row["m_metro_export_trip_id"],
                                                    trp_route=standardize_string(row["trp_route"]),
                                                    stop_description_first=row["stop_description_first"],
                                                    stop_description_last=row["stop_description_last"],
                                                    trip_time_start=row["trp_time_start"],
                                                    trip_time_end=row["trp_time_end"],
                                                    trip_direction=row["trp_direction"],
                                                    type=row["trp_type"]))
        return {"canceled_data":canceled_service}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"Metro API Version": "2.0.1"}