# dcca-cc-thermal-cabinet

This repository is an example of application for a thermal cabinet system, composed by an ESP32 as the IoT device for measure temperature and sense the state of a door (open/closed). This sends the measurements to a server (deployed in a cloud platform or any other) which execute an API for receive and process the signals. So, data is sent by HTTP using APIRest (Exists other protocols as MQTT or WebSockets, but in this practice, we pretend to use APIRest).

The server is a hub, processing and serving data to other instances. For data storage, AWS was used, implementing Lambda functions through API-Gateway, which process and sends or retrieves data from DynamoDB.

A client UI was implemented, using Qt PySide6 for the client application. This retrieves the temperature, door state and the last twelve measures of temperature.

If the temperature raises upper than a threshold or the door was opened or closed, a notice message is sent through Telegram, to any group.

# Requirements
- An ESP32.
- A server deployed in any cloud or place.
- AWS DynamoDB, Lambda functions and API-Gateway knowledge.

# Install

First, you can clone this repository whit:

```bash
git clone https://github.com/gggfred/dcca-cc-thermal-cabinet/tree/main
```

Next, install the different instances. Let's follow the next instructions:

## 1. Install Server
For this part, you must install some packages in your server, after this copy the files from `server` folder in your server machine, at your prefered platform. Then, you need to configure the server. Here you can find the instructions:

### 1.1 Updating and installing packages
```bash
sudo apt update
sudo apt install python3-venv nginx
```

### 1.2 Copy files to your server
- Copy the folder `myproject` into the home folder at your server.
- Copy `myproject.service` into `/etc/systemd/system` 
- Copy `myproject.conf` into `/etc/nginx/sites-available` 

### 1.3 Config
#### myproject
To config `myproject` you must create a Python virtual environment and then install the `requirements.txt` into this, as follows:

1. Get into the home folder.
```bash
cd ~
```
2. Create the environmet and source it.
```bash
python3 -m venv ./venv
source venv/bin/activate
```
3. Change into project folder and install the required packages
```bash
cd myproject
pip3 install -r requirements.txt
```

After, you must specify the url of the AWS api service, in the file `cloud_services_api.py` by changing the variable `API_GATEWAY_URL` for your url. 

Also, you must specify the `YOUR_BOT_TOKEN` and `CHAT_ID` variables of `telegram.py` with your telegram credentials, for use this service. To achieve this, please refer to the next link https://core.telegram.org/api

Now configure the SystemD daemon and Nginx to brings the public access.

#### SystemD daemon
For config the daemon, you must run the next command:

```bash
sudo systemctl enable myproject.service
sudo systemctl start myproject.service
```

Always you can stop or restart the service with:

```bash
sudo systemctl stop myproject.service
sudo systemctl restart myproject.service
```

#### Nginx
For config Nginx, you must run the next:

```bash
sudo ln -s /etc/nginx/sites-available/myproject.conf /etc/nginx/sites-enabled
```

So, you can restart Nginx by running:

```bash
sudo systemctl restart nginx.service
```

## 2. Install IoT Sensor Device

This practice is focused on IoT devices, so you need to burn the firmware include in `sensor` folder into your ESP32. For this, you need the next:

- Arduino IDE.
- Install the Espressif Systems's esp32 board support.
- Install the Benoit Blanchon's ArduinoJson library.

Then, follow the next steps:

1. Please, change the next variables to customize the application to your needs:
```c
...
const char* ssid = "YOUR_SSID";
const char* password = "YOUR_PASSWORD"; // 0 if the network is open
...
String serverName = "SERVER_URL"; // Replace with your server URL
...
```
2. Connect your ESP32 and upload the firmware.

## 3. Install AWS api


## 4. Install GUI application

This application is going to run in your local PC. It's recommended to create a virtual environment into the app `client` folder and install the packages in `requirements.txt`, to achieve this, you can follow the next steps:

1. Change into the `client` folder and create a virtual enviroment.
```bash
cd ~/myproject/client
python3 -m venv ./venv
source venv/bin/activate
```
2. Install the packages using pip3
```bash
pip3 install -r requirements.txt
```
3. You must change the variable `url` in `api.py` by the url of the server implemented in the section 1, replace `SERVER_URL`.

```bash
url = "SERVER_URL"
```

Now you can run this application with:

```bash
python3 main.py
```