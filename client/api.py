import requests

url = SERVER_URL

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


def getHistory(qty):
    base_url = f'{url}/history'

    json = {
        'qty': qty
    }

    response = requests.get(base_url, json=json)

    if response.status_code == 200:
        data = response.json()
        return data.get('measurements')
    else:
        print(f'Error sending message. Status code: {response.status_code}')
