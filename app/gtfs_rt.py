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
SWIFTLY_GTFS_RT_VEHICLE_POSITIONS = 'gtfs-rt-vehicle-positions'

# SWIFTLY_API_REALTIME = 'https://api.goswift.ly/real-time/lametro-rail/gtfs-rt-trip-updates?format=json'
# Swiftly API endpoint format:
# SWIFTLY_API_REALTIME + SERVICE_* + SWIFTLY_GTFS_RT_* + FORMAT

TARGET_FOLDER = 'app/data/'

def connect_to_swiftly(service, endpoint, output_file, output_format):
    swiftly_endpoint = ''

    if not output_format == '':
        swiftly_endpoint = SWIFTLY_API_REALTIME + SERVICE_DICT[service] + '/' + endpoint + '?format=' + output_format
    else:
        swiftly_endpoint = SWIFTLY_API_REALTIME + SERVICE_DICT[service] + '/' + endpoint

    
    if (service == 'bus'):
        key = Config.SWIFTLY_AUTH_KEY_BUS
    elif (service == 'rail'):
        key = Config.SWIFTLY_AUTH_KEY_RAIL
    header = { 
        "Authorization": key
    }

    print('endpoint: ' + swiftly_endpoint)
    try:
        response = requests.get(swiftly_endpoint, headers=header)
    except Exception as e:
        print('Error connecting to Swiftly API')
        print(e)
        return

    print('response status: ' + str(response.status_code))

    try:
        if output_format == 'json':
            with open(output_file, 'w') as file:
                print('Writing file: ' + output_file)
                json.dump(response.json(), file)
        else:
            with open(output_file, 'wb') as file:
                print('Writing file: ' + output_file)
                file.write(response.content).encode('utf8')
    except Exception as e:
        print("Error:" + str(e))
        print('Error writing to file: ' + output_file)

def write_output_file(output_format):
    pass


def get_trip_updates(service, output_format):
    print('get_trip_updates called with service: ' + service)
    if (service == 'bus' or service == 'rail'):
        if (output_format == 'json'):
            output_file = TARGET_FOLDER + service + '-' + SWIFTLY_GTFS_RT_TRIP_UPDATES + '.json'
            connect_to_swiftly(service, SWIFTLY_GTFS_RT_TRIP_UPDATES, output_file, output_format)
            with open(output_file, 'r') as file:
                print('Reading file: ' + output_file)
                trip_updates_json = json.loads(file.read())
                return trip_updates_json
        else:
            output_file = TARGET_FOLDER + service + '-' + SWIFTLY_GTFS_RT_TRIP_UPDATES + '.pb'
            connect_to_swiftly(service, SWIFTLY_GTFS_RT_TRIP_UPDATES, output_file, output_format)
            with open(output_file, 'rb') as file:
                print('Reading file: ' + output_file)
                trip_updates_json = file.read()
                return trip_updates_json
    else:
        print('Invalid service: ' + service)

def get_vehicle_positions(service, output_format):
    print('get_vehicle_positions called with service: ' + service)
    if (service == 'bus' or service == 'rail'):
        if (output_format == 'json'):
            output_file = TARGET_FOLDER + service + '-' + SWIFTLY_GTFS_RT_VEHICLE_POSITIONS + '.json'
            connect_to_swiftly(service, SWIFTLY_GTFS_RT_VEHICLE_POSITIONS, output_file, output_format)
            with open(output_file, 'r') as file:
                print('Reading file: ' + output_file)
                vehicle_positions_json = json.loads(file.read())
                file.close()
                return vehicle_positions_json
        else:
            output_file = TARGET_FOLDER + service + '-' + SWIFTLY_GTFS_RT_VEHICLE_POSITIONS + '.pb'
            connect_to_swiftly(service, SWIFTLY_GTFS_RT_VEHICLE_POSITIONS, output_file, output_format)
            with open(output_file, 'rb') as file:
                print('Reading file: ' + output_file)
                vehicle_positions_proto = file.read()
                file.close()
                return vehicle_positions_proto

def write_output_file(output_format):
    output_file = TARGET_FOLDER + service + '-' + SWIFTLY_GTFS_RT_VEHICLE_POSITIONS + '.json'
    connect_to_swiftly(service, SWIFTLY_GTFS_RT_VEHICLE_POSITIONS, output_file, output_format)
    with open(output_file, 'r') as file:
        vehicle_positions_json = json.loads(file.read())
    return vehicle_positions_json
    # pass

