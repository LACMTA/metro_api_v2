# import data modules
from distutils.command.config import config
import http
import json
import requests
import csv
import os 

# import scheduling modules
import threading
import time
import schedule

import pytz

from typing import Dict, List, Optional

from datetime import timedelta, date, datetime

from fastapi import FastAPI, Request, Response, Depends, HTTPException, status
from fastapi.responses import RedirectResponse, HTMLResponse

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel, Json, ValidationError

from starlette.middleware.cors import CORSMiddleware

# for OAuth2
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

# from app.models import *
# from app.security import *
# from app.update_canceled_trips import *

from .utils.log_helper import *

from . import crud, models, security, schemas, update_canceled_trips
from .database import Session, engine, session, get_db
from .config import Config
from .gtfs_rt import *
from pathlib import Path

from logzio.handler import LogzioHandler

UPDATE_INTERVAL = 300
PATH_TO_CALENDAR_JSON = 'app/data/calendar_dates.json'
PATH_TO_CANCELED_JSON = 'app/data/CancelledTripsRT.json'

models.Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url="/")
# db = connect(host='', port=0, timeout=None, source_address=None)

templates = Jinja2Templates(directory="app/frontend")
app.mount("/", StaticFiles(directory="app/frontend"))

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
    update_canceled_trips.run_update()

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

####################
#  Begin Routes
####################

# tokens

@app.get("/verify_email/{email_verification_token}")
async def verify_email_route(email_verification_token: str,db: Session = Depends(get_db)):
    
    if not crud.verify_email(email_verification_token,db):
        return False

    return "email verified"

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    user = crud.authenticate_user(form_data.username, form_data.password,db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}




# end tokens


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/{username}", response_model=schemas.User)
def read_user(username: str, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    db_user = crud.get_user(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# @app.get("/items/")
# async def read_items(token: str = Depends(oauth2_scheme)):
#     return {"token": token}

@app.get("/calendar_dates")
async def get_calendar_dates():
    with open(PATH_TO_CALENDAR_JSON, 'r') as file:
        calendar_dates = json.loads(file.read())
        return {"calendar_dates":calendar_dates}

def standardize_string(input_string):
    return input_string.lower().replace(" ", "")

@app.get("/canceled_service_summary")
async def get_canceled_trip_summary():
    canceled_json_file = Path(PATH_TO_CANCELED_JSON)
    if not canceled_json_file.exists():
        canceled_json_file.touch()

    with open(canceled_json_file, 'r') as file:
        canceled_trips = json.loads(file.read() or 'null')
        
    if canceled_trips is None:
        return {"canceled_trips_summary": "",
                "total_canceled_trips": 0,
                "last_update": ""}
    else:
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
        logger.info('file modified: ' + str(ftp_json_file_time))
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
                canceled_service.append(schemas.CanceledServiceData(
                                                    gtfs_trip_id=row["m_gtfs_trip_id"],
                                                    trip_route=standardize_string(row["trp_route"]),
                                                    stop_description_first=row["stop_description_first"],
                                                    stop_description_last=row["stop_description_last"],
                                                    trip_time_start=row["trp_time_start"],
                                                    trip_time_end=row["trp_time_end"],
                                                    trip_direction=row["trp_direction"]                                                    
                                                    ))
    return {"canceled_data":canceled_service}

@app.get("/canceled_service/all")
async def get_canceled_trip():
    with open(PATH_TO_CANCELED_JSON, 'r') as file:
        cancelled_service_json = json.loads(file.read())
        canceled_service = cancelled_service_json["CanceledService"]
        return {"canceled_data":canceled_service}



@app.get("/time")
async def get_time():
    current_time = datetime.now()
    return {current_time}


@app.get("/trip_updates/{service}")
async def trip_updates(service, output_format: Optional[str] = None):
    result = None
    valid_formats = ["json"]

    if output_format:
        if output_format in valid_formats:
            result = get_trip_updates(service, output_format)
            return result
        else:
            raise HTTPException(status_code=400, detail="Invalid format")
    else:
        result = get_trip_updates(service, '')
        return Response(content=result, media_type="application/x-protobuf")

@app.get("/vehicle_positions/{service}")
async def vehicle_positions(service, output_format: Optional[str] = None):
    # format options:
    # - json
    result = None
    valid_formats = ["json"]
    if output_format:
        if output_format in valid_formats:
            result = get_vehicle_positions(service, output_format)
            return result
        else:
            raise HTTPException(status_code=400, detail="Invalid format")
    else:
        result = get_vehicle_positions(service, '')
        return Response(content=result, media_type="application/x-protobuf")

# @app.get("/agencies/")
# async def root():
#     return {"Metro API Version": "2.0.3"}

# Frontend Routing

@app.get("/login",response_class=HTMLResponse)
def login(request:Request):
    return templates.TemplateResponse("login.html", context= {"request": request})


@app.get("/",response_class=HTMLResponse)
def index(request:Request):
    human_readable_default_update = None
    try:
        default_update = datetime.fromtimestamp(Config.API_LAST_UPDATE_TIME)
        default_update = default_update.astimezone(pytz.timezone("America/Los_Angeles"))
        human_readable_default_update = default_update.strftime('%Y-%m-%d %H:%M')
    except Exception as e:
        logger.exception(type(e).__name__ + ": " + str(e), exc_info=False)
    return templates.TemplateResponse("index.html", context= {"request": request,"api_version":Config.CURRENT_VERSION,"update_time":human_readable_default_update})

class LogFilter(logging.Filter):
    def filter(self, record):
        record.app = "api.metro.net"
        record.env = Config.RUNNING_ENV
        return True

@app.on_event("startup")
async def startup_event():
    print("Starting up...")
    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_error_logger = logging.getLogger("uvicorn.error")
    logger = logging.getLogger("uvicorn.app")
    
    logzio_formatter = logging.Formatter("%(message)s")
    logzio_uvicorn_access_handler = LogzioHandler(Config.LOGZIO_TOKEN, 'uvicorn.access', 5, Config.LOGZIO_URL)
    logzio_uvicorn_access_handler.setLevel(logging.INFO)
    logzio_uvicorn_access_handler.setFormatter(logzio_formatter)

    logzio_uvicorn_error_handler = LogzioHandler(Config.LOGZIO_TOKEN, 'uvicorn.error', 5, Config.LOGZIO_URL)
    logzio_uvicorn_error_handler.setLevel(logging.INFO)
    logzio_uvicorn_error_handler.setFormatter(logzio_formatter)

    logzio_app_handler = LogzioHandler(Config.LOGZIO_TOKEN, 'fastapi.app', 5, Config.LOGZIO_URL)
    logzio_app_handler.setLevel(logging.INFO)
    logzio_app_handler.setFormatter(logzio_formatter)

    uvicorn_access_logger.addHandler(logzio_uvicorn_access_handler)
    uvicorn_error_logger.addHandler(logzio_uvicorn_error_handler)
    logger.addHandler(logzio_app_handler)

    uvicorn_access_logger.addFilter(LogFilter())
    uvicorn_error_logger.addFilter(LogFilter())
    logger.addFilter(LogFilter())

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)
