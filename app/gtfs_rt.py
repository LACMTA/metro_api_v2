from tkinter import E
from app.config import Config
import json
import requests

SWIFTLY_API_REALTIME = 'https://api.goswift.ly/real-time/'

SERVICE_DICT = {
    'bus': 'lametro',
    'rail': 'lametro-rail'
}


SWIFTLY_GTFS_RT_TRIP_UPDATES = 'gtfs-rt-trip-updates'
SWIFTLY_GTFS_RT_VEHICLE_POSITIONs = 'gtfs-rt-vehicle-positions'

# SWIFTLY_API_REALTIME = 'https://api.goswift.ly/real-time/lametro-rail/gtfs-rt-trip-updates?format=json'
# Swiftly API endpoint format:
# SWIFTLY_API_REALTIME + SERVICE_* + SWIFTLY_GTFS_RT_* + FORMAT

TARGET_FOLDER = 'app/data/'

def connect_to_swiftly(service, endpoint, output_file):
    endpoint = SWIFTLY_API_REALTIME + SERVICE_DICT[service] + '/' + endpoint + '?format=json'
    if (service == 'bus'):
        key = Config.SWIFTLY_AUTH_KEY_BUS
    elif (service == 'rail'):
        key = Config.SWIFTLY_AUTH_KEY_RAIL
    header = { 
        "Authorization": key
    }

    print('endpoint: ' + endpoint)
    try:
        response = requests.get(endpoint, headers=header)
    except Exception as e:
        print('Error connecting to Swiftly API')
        print(e)
        return

    print('response status: ' + str(response.status_code))

    try:
        with open(output_file, 'w') as file:
            print('Writing file: ' + output_file)
            json.dump(response.json(), file)
    except Exception as e:
        print('Error writing to file: ' + output_file)


def get_trip_updates(service):
    print('get_trip_updates called with service: ' + service)
    if (service == 'bus' or service == 'rail'):
        output_file = TARGET_FOLDER + service + '-' + SWIFTLY_GTFS_RT_TRIP_UPDATES + '.json'
        connect_to_swiftly(service, SWIFTLY_GTFS_RT_TRIP_UPDATES, output_file)

        try:
            with open(output_file, 'r') as file:
                print('Reading file: ' + output_file)
                trip_updates_json = json.loads(file.read())
                return trip_updates_json
        except Exception as e:
            print('Error reading file: ' + output_file)
    else:
        print('Invalid service: ' + service)

def get_vehicle_positions(service):
    print('get_vehicle_positions called with service: ' + service)
    if (service == 'bus' or service == 'rail'):
        output_file = TARGET_FOLDER + service + '-' + SWIFTLY_GTFS_RT_VEHICLE_POSITIONs + '.json'
        connect_to_swiftly(service, SWIFTLY_GTFS_RT_VEHICLE_POSITIONs, output_file)

        with open(output_file, 'r') as file:
            vehicle_positions_json = json.loads(file.read())
            return vehicle_positions_json