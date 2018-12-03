#include <WiFi.h>
#include <PubSubClient.h>
 
const char* ssid = "Lowi3370";
const char* password =  "F22JH4BDWJD3GH";
const char* mqttServer = "m23.cloudmqtt.com";
const int mqttPort =  17997;
const char* mqttUser = "udwgocyz";
const char* mqttPassword = "lC73EBlF8DAd";

const int rele = 32;
const int sensor = 34;
int estado = LOW;

WiFiClient espClient;
PubSubClient client(espClient);

#define EST_TOPIC    "contacto1/estado"
#define ORD_TOPIC    "contacto1/ordenes" /* H=on, L=off */

void receivedCallback(char* topic, byte* payload, unsigned int length) {
  char orden = (char)payload[0];
  Serial.println(orden);
  switch(orden){
    case  'H':
      digitalWrite(rele, HIGH);
      delay(5);
      break;
    case  'L':
      digitalWrite(rele, LOW);
      delay(5);
      break;
    default:
      break;
  }
}

void mqttconnect() {
  while (!client.connected()) {
    if (client.connect("Rele1" , mqttUser, mqttPassword)) {
      client.subscribe(ORD_TOPIC);
    } else {
      delay(3000);
    }
  }
}

void pubestado() {
  estado = digitalRead(sensor);
  delay(5);
  if(estado == LOW){
    client.publish(EST_TOPIC, "OFF");
  } else {
    client.publish(EST_TOPIC, "ON");
  }
  delay(4000);
}

void setup() {
 
  Serial.begin(115200);
  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  
  pinMode(rele, OUTPUT);
  pinMode(sensor, INPUT);
  client.setServer(mqttServer, mqttPort);
  client.setCallback(receivedCallback);
}

void loop() {
  if (!client.connected()) {
    mqttconnect();
  }
  client.loop();
  pubestado();
}