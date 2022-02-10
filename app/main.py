# import data modules
import json
import requests
import csv

# import scheduling modules
import threading
import time
import schedule

import pytz

from fastapi import FastAPI,Request,Depends, HTTPException,status

from starlette.middleware.cors import CORSMiddleware

# for OAuth2
from fastapi.security import OAuth2PasswordBearer


from app.config import Config
from app.models import *
from app.security import *

from app.update_canceled_trips import *

from typing import Dict, List


from pydantic import BaseModel, Json, ValidationError
from datetime import date, datetime
from app.gtfs_rt import *

UPDATE_INTERVAL = 300
PATH_TO_CALENDAR_JSON = 'app/data/calendar_dates.json'
PATH_TO_CANCELED_JSON = 'app/data/CancelledTripsRT.json'

app = FastAPI(docs_url="/")
# db = connect(host='', port=0, timeout=None, source_address=None)



# code from https://schedule.readthedocs.io/en/stable/background-execution.html
def run_continuously(interval=UPDATE_INTERVAL):
    cease_continuous_run = threading.Event()
    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)
    
    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run

def background_job():
    run_update()

schedule.every().second.do(background_job)

# Start the background thread
stop_run_continuously = run_continuously()

def csv_to_json(csvFilePath, jsonFilePath):
    jsonArray = []
    headers = []
    header_row = next(csvFilePath)
    for column in header_row:
        headers.append(column)  
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
jsonFilePath = r'app/data/calendar_dates.json'


lactmta_gtfs_rt_url = "https://lacmta.github.io/lacmta-gtfs/data/calendar_dates.txt"
response = requests.get(lactmta_gtfs_rt_url)

cr = csv.reader(response.text.splitlines())
csv_to_json(cr,jsonFilePath)

app = FastAPI()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Begin Routes

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}

@app.get("/calendar_dates/")
async def get_calendar_dates():
    with open(PATH_TO_CALENDAR_JSON, 'r') as file:
        calendar_dates = json.loads(file.read())
        return {"calendar_dates":calendar_dates}

def standardize_string(input_string):
    return input_string.lower().replace(" ", "")

@app.get("/canceled_service_summary/")
async def get_canceled_trip_summary():
    print('get_canceled_trip_summary')
    with open(PATH_TO_CANCELED_JSON, 'r') as file:
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
        ftp_json_file_time = os.path.getmtime(PATH_TO_CANCELED_JSON)
        print('file modified: ' + str(ftp_json_file_time))
        modified_time = datetime.fromtimestamp((ftp_json_file_time)).astimezone(pytz.timezone("America/Los_Angeles"))
        formatted_modified_time = modified_time.strftime('%Y-%m-%d %H:%M:%S')
        return {"canceled_trips_summary":canceled_trips_summary,
                "total_canceled_trips":total_canceled_trips,
                "last_updated":formatted_modified_time}

@app.get("/canceled_service/line/{line}")
async def get_canceled_trip(line):
    with open(PATH_TO_CANCELED_JSON, 'r') as file:
        cancelled_service_json = json.loads(file.read())
        canceled_service = []
        for row in cancelled_service_json["CanceledService"]:
            if row["trp_type"] == "REG" and standardize_string(row["trp_route"]) == line:
                canceled_service.append(CanceledServiceData(
                                                    gtfs_trip_id=row["m_gtfs_trip_id"],
                                                    trip_route=standardize_string(row["trp_route"]),
                                                    stop_description_first=row["stop_description_first"],
                                                    stop_description_last=row["stop_description_last"],
                                                    trip_time_start=row["trp_time_start"],
                                                    trip_time_end=row["trp_time_end"],
                                                    trip_direction=row["trp_direction"]                                                    
                                                    ))
    return {"canceled_data":canceled_service}

@app.get("/canceled_service/all/")
async def get_canceled_trip():
    with open(PATH_TO_CANCELED_JSON, 'r') as file:
        cancelled_service_json = json.loads(file.read())
        canceled_service = cancelled_service_json["CanceledService"]
        return {"canceled_data":canceled_service}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/time")
async def get_time():
    current_time = datetime.now()
    return {current_time}


@app.get("/trip_updates/{service}")
async def trip_updates(service):
    result = get_trip_updates(service)
    return result

@app.get("/alerts/{service}")
async def alerts(service):
    result = get_alerts(service)
    return result

@app.get("/vehicle_positions/{service}")
async def vehicle_positions(service):
    result = get_vehicle_positions(service)
    return result

# @app.get("/agencies/")
# async def root():
#     return {"Metro API Version": "2.0.3"}

@app.get("/")
async def root():
    return {"Metro API Version": "2.0.4"}

