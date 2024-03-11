import requests

url = "http://ec2-54-81-96-96.compute-1.amazonaws.com"

def getTemperature():
    base_url = f'{url}/measurement'

    json = {
        'measure': 'temperature'
    }

    response = requests.get(base_url, json=json)

    if response.status_code == 200:
        data = response.json()
        return data.get('temperature')
    else:
        print(f'Error sending message. Status code: {response.status_code}')


def getDoorState():
    base_url = f'{url}/door'

    response = requests.get(base_url)

    if response.status_code == 200:
        data = response.json()
        return data.get('state')
    else:
        print(f'Error sending message. Status code: {response.status_code}')


def getHistory(id, qty):
    base_url = f'{url}/history'

    json = {
        'qty': qty,
        'unique_id' : id 
    }

    response = requests.get(base_url, json=json)

    if response.status_code == 200:
        data = response.json()
        return data.get('measurements')
    else:
        print(f'Error sending message. Status code: {response.status_code}')
