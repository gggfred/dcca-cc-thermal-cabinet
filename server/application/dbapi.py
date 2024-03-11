import requests
import json

url = 'API_GATEWAY_URL'

def getHistory(id, qty):
    base_url = f'{url}/history'

    obj = {'qty': qty, 'unique_id' : id}

    response = requests.get(base_url, json=obj)

    if response.status_code == 200:
        data = response.json()

        body = json.loads(data.get('body').encode('utf-8'))
        meas = json.loads(body.get('measures').encode('utf-8'))

        return meas

    else:
        print(f'Error sending message. Status code: {response.status_code}')

def postMeasure(data):
    base_url = f'{url}/measurements'

    response = requests.post(base_url, json=data)

    if response.status_code == 200:
        print(f'API DB: Status code: {response.status_code}')
    else:
        print(f'API DB: Error sending message. Status code: {response.status_code}')