/*
  Leonardo Ochoa
  Galo Guzman
  Complete project details at Complete project details at https://RandomNerdTutorials.com/esp32-http-get-post-arduino/
*/

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "time.h"
#include <Arduino.h>

const int pinToRead = 23;  // Pin de entrada para leer el estado
const int ledPin = 2;    // Pin del LED de salida


const char* ssid = "VEKTOR_A330";
const char* password = "12345678";

//Your Domain name with URL path or IP address with path
//String serverName = "http://192.168.1.106:1880/update-sensor";
String serverName = "http://ec2-54-81-96-96.compute-1.amazonaws.com";

// the following variables are unsigned longs because the time, measured in
// milliseconds, will quickly become a bigger number than can be stored in an int.
unsigned long lastTime = 0;
unsigned long timerDelay = 10000;

unsigned long epochTime; 
//unsigned long getTime() {
long getTime() {
  long epochValue;
  HTTPClient http;
  http.begin("http://ec2-54-81-96-96.compute-1.amazonaws.com/epoch");  // Replace with your AWS endpoint URL

  int httpCode = http.GET();
  if (httpCode > 0) {
    String payload = http.getString();

    // Parse JSON using ArduinoJson
    StaticJsonDocument<256> doc;  // Adjust the size based on your JSON response
    DeserializationError error = deserializeJson(doc, payload);

    if (error) {
      Serial.print("Failed to parse JSON: ");
      Serial.println(error.c_str());
    } else {
      // Extract the epoch value
      epochValue = doc["epoch"];
      Serial.print("Epoch value: ");
      Serial.println(epochValue);
    }
  } else {
    Serial.printf("HTTP request failed with error code %d\n", httpCode);
  }

  http.end();
  return epochValue;

}

// CREO EL POST PARA LA PUERTA CERRADA

long postDoorClosed() {
  long doorValue;
  HTTPClient http;
  http.begin("http://ec2-54-81-96-96.compute-1.amazonaws.com/door");  // Replace with your AWS endpoint URL

  http.addHeader("Content-Type", "application/json");
      StaticJsonDocument<200> doc;

      doc["state"] = "closed";
      String requestBody;
      serializeJson(doc, requestBody);
     
      int httpResponseCode = http.POST(requestBody);
  
  return doorValue;

}

// CREO EL POST PARA LA PUERTA ABIERTA
long postDoorOpen() {
  long doorValue;
  HTTPClient http;
  http.begin("http://ec2-54-81-96-96.compute-1.amazonaws.com/door");  // Replace with your AWS endpoint URL

  http.addHeader("Content-Type", "application/json");
      StaticJsonDocument<200> doc;

      doc["state"] = "open";
      String requestBody;
      serializeJson(doc, requestBody);
     
      int httpResponseCode = http.POST(requestBody);
  
  return doorValue;

}



void setup() {
  Serial.begin(115200); 
// Definición de pines de lectura y escritura

  pinMode(pinToRead, INPUT);
  pinMode(ledPin, OUTPUT);



  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());
 
  Serial.println("Timer set to 5 seconds (timerDelay variable), it will take 5 seconds before publishing the first reading.");

}

void loop() {
  //Send an HTTP POST request every 10 minutes
  //epochTime = getTime();
  //getTime();
  //Serial.print("Epoch Time: ");
  //Serial.println(epochTime);
  int pinState = digitalRead(pinToRead);

  // Mostrar el estado del pin en el puerto serie
  Serial.print("Estado del pin ");
  Serial.print(pinToRead);
  Serial.print(": ");
  Serial.println(pinState);
  digitalWrite(ledPin, pinState);
  delay(10000);

  if (pinState == 1) {
    postDoorOpen();
  } else if (pinState == 0) {
    postDoorClosed();
  }



  if ((millis() - lastTime) > timerDelay) {
    //Check WiFi connection status
    if(WiFi.status()== WL_CONNECTED){
      HTTPClient http;

      String serverPath = serverName + "/measurement";
      
      // Your Domain name with URL path or IP address with path
      http.begin(serverPath.c_str());
      
      // Send HTTP GET request
      http.addHeader("Content-Type", "application/json");
      StaticJsonDocument<200> doc;
    // Add values in the document
    //

      long randNumber = random(30,40);
      Serial.println(randNumber);
      //delay(10000);
      doc["temperature"] = randNumber;
      doc["epoch"] = getTime();
      doc["state"] = "open";
      String requestBody;
      serializeJson(doc, requestBody);
     
      int httpResponseCode = http.POST(requestBody);


      
      if (httpResponseCode>0) {
        Serial.print("HTTP Response code: ");
        Serial.println(httpResponseCode);
        String payload = http.getString();
        Serial.println(payload);
      }
      else {
        Serial.print("Error code: ");
        Serial.println(httpResponseCode);
      }
      // Free resources
      http.end();
    }
    else {
      Serial.println("WiFi Disconnected");
    }
    lastTime = millis();
  }
}