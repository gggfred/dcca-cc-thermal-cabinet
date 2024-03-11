import requests

# Replace 'YOUR_BOT_TOKEN' with the token you received from BotFather
TOKEN = 'YOUR_BOT_TOKEN'
# Replace 'CHAT_ID' with the chat ID from which you want to read messages
CHAT_ID = 'CHAT_ID'

BOT_TOKEN = f"bot{TOKEN}"

TELEGRAM_API_URL = f'https://api.telegram.org/{BOT_TOKEN}'

def send_telegram_message(message):
    base_url = f'{TELEGRAM_API_URL}/sendMessage'
    json = {
        'chat_id': CHAT_ID,
        'text': message
    }

    response = requests.post(base_url, json=json)

    if response.status_code == 200:
        print('Message sent successfully!')
    else:
        print(f'Error sending message. Status code: {response.status_code}')

def read_telegram_messages():
    base_url = f'{TELEGRAM_API_URL}/getUpdates'
    json = {
        'chat_id': CHAT_ID
    }

    response = requests.get(base_url, json=json)

    if response.status_code == 200:
        data = response.json()
        if data['result']:
            for update in data['result']:
                message = update.get('message', {}).get('text')
                if message:
                    print(f'Received message: {message}')
        else:
            print('No messages found.')
    else:
        print(f'Error reading messages. Status code: {response.status_code}')

# Add a function to delete a message (optional)
def delete_telegram_message(message_id):
    base_url = f'{TELEGRAM_API_URL}/deleteMessage'
    json = {
        'chat_id': CHAT_ID,
        'message_id': message_id
    }

    response = requests.post(base_url, json=json)

    if response.status_code == 200:
        print(f'Message (ID {message_id}) deleted successfully!')
    else:
        print(f'Error deleting message. Status code: {response.status_code}')

