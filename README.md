# dcca-cc-thermal-cabinet

This repository is an example of application for a thermal cabinet system, composed by an ESP32 as the IoT device for measure temperature and sense the state of a door (open/closed). This sends the measurements to a server (deployed in a cloud platform or any other) which execute an API for receive and process the signals. So, data is sent by HTTP using APIRest (Exists other protocols as MQTT or WebSockets, but in this practice, we pretend to use APIRest).

The server is a hub, processing and serving data to other instances. For data storage, AWS was used, implementing Lambda functions through API-Gateway, which process and sends or retrieves data from DynamoDB.

A client UI was implemented, using Qt PySide6 for the client application. This retrieves the temperature, door state and the last twelve measures of temperature.

If the temperature raises upper than a threshold or the door was opened or closed, a notice message is sent through Telegram, to any group.
