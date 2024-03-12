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

First, you can clone this repository in your local PC, with:

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

The temperature signals were simulated for this practice, the door state is sense by pin `23` being 0 closed, 1 open.

## 3. Install AWS api

At this point, you should create the database in AWS, using DynamoDB for storage the temperature data, and Lambda functions for save and retrieve the data. 

### Create a role

First, is necessary to create a user role, with the permissions for access to AWS, as follows:

1. Access to `IAM` console.
2. Open `Access management->Roles` tab.
3. Click on `Create role`
4. Step 1 - Select trusted entity: Select Lambda on `Service or use case` and click next.
5. Step 2 - Search by policy name and select:
    - AWSLambda_FullAccess
    - AWSLambdaBasicExecutionRole
    - AWSLambdaDynamoDBExecutionRole
    - AmazonDynamoDBFullAccess
6. Step 3 - Give a name, for example `roleDynamoDB`. To finish click on `Create role`.

### Create a DynamoDB instance

Next, are the steps for install the AWS cloud:

1. Access to DynamoDB Dashboard.
2. Create a DynamoDB Table.
3. Enter `Measurements` as table name.
4. Enter `unique_id` as partition key.
5. Enter `timestamp` as sort key.

### Create Lambda functions

Now, it is necessary to create the Lambda functions, which interacts with DynamoDb by writing and reading data. The code for this functions are in the files `measurement_to_dynamodb.py` and `measurement_from_dynamodb.py`. To achieve this, follow the next steps:

1. Access to Lambda Dashboard.
2. Create a Lambda function.
3. Enter `MeasurementToDynamoDB` as funcion name.
4. Choose Python 3.12 as Runtime.
5. Change the `execution role` to use an existing role, and choose the `roleDynamoDB` role.
6. Open the Lambda function `MeasurementsToDynamoDB` to edit it and select the `Code` tab.
7. Select `lambda_function` tab and paste the code in `measurement_to_dynamodb.py`.

Repeat this process to create other function, using `MeasurementFromDynamoDB` as the name and paste the code in the file `measurement_from_dynamodb.py`.

### API Gateway

For last, it is necessary to create the API as such, by following the next steps:

1. Access to API Gateway.
2. Click on `Create API`.
3. Choose `REST API` to build.
4. Choose `New API` and enter an API name.
5. Click on `Create API`

Once created the API, you should create the resources (endpoints). In the menu `API Gateway->APIs` click on your API name, and create resources as follows:

1. Click on `Create resource`.
2. Select the path (endpoint) on which you want to create the resource.
3. Enter a name for your resource
4. Click on `Create resource`

In this case, the process was repeated three times, in order to create the next endpoints tree:

- /cc_api_final
    - /cc_api_final/history
    - /cc_api_final/measurements

Now it's necessary to create methods for this endpoints. In this case, we should have the next results:

|Path|Method|Lambda Function|
|----|------|--------|
|/cc_api_final/history    |GET   | MeasurementsFromDynamoDB |
|/cc_api_final/measurements    |POST   | MeasurementsToDynamoDB |

To achieve this, we should follow the next steps:

1. Select the resource in which you want to create the method.
2. Click on `Create method`.
3. Select a method type (GET, POST).
4. Select `Lambda function` as integration type.
5. Choose the `Lambda function`.
6. Click on `Create method` to finish.

Once you have created the two methods, you should deploy the API, following the next:

1. Click on `Deploy API`
2. Select a stage or create a new one if you don't have.
3. Click on `Deploy`

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