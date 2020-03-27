from pathlib import Path
import json
import requests
import re
from itertools import chain
from itertools import islice
import collections

YA_SCHED_API_KEY = "49128da9-ddca-428d-84e8-d75d72894965"
YA_SCHED_NEAREST_URL = "https://api.rasp.yandex.net/v3.0/nearest_stations/"

YA_TRANS_INIT_URL = "https://yandex.ru/maps/213/moscow/transport"
YA_TRANS_STATION_URL = "https://yandex.ru/maps/api/masstransit/getStopInfo"

#MOS_OPEN_DATA = "https://apidata.mos.ru/v1/datasets/60662/rows?api_key=9454c7d48e6bbd3ceabc538f898d3543&$skip=1&$top=1"

#    "lat": 55.753785,
#    "lng": 37.558428

MAX_DISPLAY_LINES = 3

def take(n, iterable):
    return list(islice(iterable, n))

def fetch_csrf_token(client):
    r = client.get(YA_TRANS_INIT_URL)
    match = re.search(r'.csrfToken...([a-z0-9\:]+).', r.text)
    (token,) = match.groups(0)
    return token

def fetch_station_data(client, token, station_id):
    params = {
        "ajax": 1,
        "csrfToken": token,
        "id": station_id,
        "lang": "ru",
        "locale": "ru_RU",
        "mode": "prognosis",
#       "sessionId": "1585163059254_673092",
#       "uri": "ymapsbm1%3A%2F%2Ftransit%2Fstop%3Fid%3Dstop__10192834"
    }
    r = client.get(YA_TRANS_STATION_URL, params=params)
    return json.loads(r.text)

def schedule_from_event(schedule, name, event):
    time = event.get('Estimated')
    mode = 'E'
    if not time:
        print("No estimated time")

        # Fallback to scheduled
        time = event['Scheduled']
        mode = 'S'
        if not time:
            print("And even no estimated time")
            return None

    schedule.append({
        "name": name,
        "mode": mode,
        "time": time['text']
    })

def schedule_from_thread(schedule, name, thread):
    bs = thread.get('BriefSchedule')
    if not bs:
        print("No brief schedule")
        return []

    ev = bs.get('Events')
    if not ev:
        print("No events")
        return []
    print("Events ", len(ev))
    [schedule_from_event(schedule, name, x) for x in ev]

def schedule_from_transport(schedule, transport):
    (name,) = transport['name'],
    print("Threads ", len(transport['threads']))
    [schedule_from_thread(schedule, name, x) for x in transport['threads']]

def extract_schedule(station_data):
    schedule = list()
    transports = station_data['data']['transports']
    print("Transports ", len(transports))
    [schedule_from_transport(schedule, t) for t in transports]
    print("SCHED ", schedule)
    return schedule

def to_text(schedule):
    return "\n".join(
        take(MAX_DISPLAY_LINES, [
            "{} - {}{}".format(x['name'], x['mode'], x['time'])
            for x in schedule
    ]))

def fetch_schedule(station_id):
    client = requests.session()
    token = fetch_csrf_token(client)
    station_data = fetch_station_data(client, token, station_id)
    return to_text(extract_schedule(station_data))

def respond_text(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': 'AWS Error' if err else res,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'text/plain'
        }
    }
    
def lambda_handler(event, context):
    try:
        schedule = fetch_schedule("stop__9649375")
        return respond_text(None, schedule)
    except Exception as err:
        traceback.print_exc()
        return respond_text(err)
