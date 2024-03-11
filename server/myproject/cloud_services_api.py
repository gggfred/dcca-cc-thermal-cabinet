import requests
import json

import logging
import logging.handlers
my_logger = logging.getLogger('cloud_services_api')
my_logger.setLevel(logging.DEBUG)
handler = logging.handlers.SysLogHandler(address = '/dev/log')
my_logger.addHandler(handler)

url = "API_GATEWAY_URL"

def getHistory(uid, qty):
    base_url = f'{url}/history'

    obj = {"qty": qty, "unique_id" : uid}

    my_logger.debug(f"cloud_services_api: request {base_url}, json: {obj}")

    response = requests.get(base_url, json=obj)

    if response.status_code == 200:
        data = response.json()

        body = json.loads(data.get('body').encode('utf-8'))
        meas = json.loads(body.get('measurements').encode('utf-8'))

        return meas

    else:
        print(f'Error sending message. Status code: {response.status_code}')

def postMeasure(data):
    base_url = f'{url}/measurements'

    my_logger.debug(f"cloud_services_api: request {base_url}, json: {data}")

    response = requests.post(base_url, json=data)

    if response.status_code == 200:
        print(f'API DB: Status code: {response.status_code}')
    else:
        print(f'API DB: Error sending message. Status code: {response.status_code}')