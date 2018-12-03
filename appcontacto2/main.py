__author__ = "Conex-ON"

import kivy
from kivy.config import Config
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
import mqtt.client as mqttClient
import time

# Config.set('input', 'mouse', 'mouse.multitouch_on_demand')

# Funciones MQTT

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscrito a contacto1/estado ")
	
def on_message(client, userdata, msg):
	mensaje = str(msg.payload)[2:-1]
	print(mensaje)
	global contador
	global im_source
	if mensaje == 'ON':
		im_source = 'encendido.png'
		contador = 0
	elif mensaje == 'OFF':
		im_source = 'apagado.png'
		contador = 0
	else:
		pass
	
def on_connect(client, userdata, flags, rc):
	if rc == 0:	
		print("Conectado al broker")
		global conectado
		conectado = True
		 
	else:	 
		print("Conexión fallida")

def comp_conex():
	global im_source, contador
	contador += 1
	if contador > 20:
		im_source = 'espera.png'
	print(contador)

# Objetos APP
		
class WPrincipal(BoxLayout):
	def __init__(self,**kwargs):
		super(WPrincipal,self).__init__(**kwargs)
		client.connect(broker_address, port=port)
		client.subscribe("contacto1/estado/#", qos=1)
		Clock.schedule_interval(self.update, 1)
	
	def update(self, dt):
		client.loop()
		print('hola')

class WLogo(Image):
	pass
	
class WImagenEstado(BoxLayout):
	def __init__(self,**kwargs):
		super(WImagenEstado,self).__init__(**kwargs)
		global im_source, contador
		Clock.schedule_interval(self.update, 1)
	
	def update(self, dt):
		comp_conex()
		self.clear_widgets()
		self.imagen = Image(source=im_source)
		self.add_widget(self.imagen)

class WBotones(BoxLayout):
	def activar(self, *arg):
		client.publish(topic , 'H')
	def desactivar(self, *arg):
		client.publish(topic , 'L')
	
class MainApp(App):
	title = 'Conex-On'
	def open_settings(*args):
		pass
	def build(self):
		return WPrincipal()

# Variables

conectado = False

broker_address= "m23.cloudmqtt.com"
port = 17997
user = "udwgocyz"
password = "lC73EBlF8DAd"
topic = "contacto1/ordenes"
im_source = 'espera.png'
contador = 100

# Declarar MQTT
			 
client = mqttClient.Client("ContactoAPP")
client.username_pw_set(user, password=password)
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.on_message = on_message

# Programa principal

if __name__ == "__main__":
	MainApp().run()