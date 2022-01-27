from tkinter import E
from app.config import Config
import json
import requests

swiftly_api_url = 'https://api.goswift.ly/real-time/lametro-rail/gtfs-rt-trip-updates?format=json'
TARGET_JSON = 'app/data/gtfs_rt.json'
def connect_to_swiftly():
    header_params = {
        "Authorization": Config.SWIFTLY_AUTH_KEY,
        "Content-Type": "application/json"
    }
    
    response = requests.get(swiftly_api_url,headers=header_params)
    with open(TARGET_JSON, 'w') as file:
        json.dump(response.json(), file)

def get_trip_updates():
    connect_to_swiftly()
    with open(TARGET_JSON, 'r') as file:
        trip_updates_json = json.loads(file.read())
        return trip_updates_json
