import kivy
from kivy.config import Config
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
import mqtt.client as mqttClient
import threading
import time

# Config.set('input', 'mouse', 'mouse.multitouch_on_demand')

# Funciones MQTT

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscrito a contacto1/estado/# ")
	
def on_message(client, userdata, msg):
	mensaje = str(msg.payload)[2:-1]
	print(mensaje)
	global im_source
	if mensaje == 'ON':
		im_source = 'encendido.png'
	elif mensaje == 'OFF':
		im_source = 'apagado.png'
	else:
		pass
	
def on_connect(client, userdata, flags, rc):
	if rc == 0:	
		print("Conectado al broker")
		global Conectado
		Conectado = True
		 
	else:	 
		print("Conexión fallida")

# Objetos APP
		
class WPrincipal(BoxLayout):
	pass

class WLogo(Image):
	pass
	
class WImagenEstado(BoxLayout):
	def __init__(self,**kwargs):
		super(WImagenEstado,self).__init__(**kwargs)
		global im_source
		Clock.schedule_interval(self.update, 1)
	
	def update(self, dt):
		self.clear_widgets()
		self.imagen = Image(source=im_source)
		self.add_widget(self.imagen)

class WBotones(BoxLayout):
	def activar(self, *arg):
		client.publish(topic , 'H')
		time.sleep(.1)
		client.publish(topic , 'S')
	def desactivar(self, *arg):
		client.publish(topic , 'L')
		time.sleep(.1)
		client.publish(topic , 'S')
	
class MainApp(App):
	title = 'Conex-On'
	def open_settings(*args):
		pass
	def build(self):
		return WPrincipal()

# Threads de MQTT
	
def conexion():
	client.connect(broker_address, port=port)
	client.subscribe("contacto1/estado/#", qos=1)
	client.publish(topic , 'S')
	client.loop_forever()
	
# Variables MQTT

Conectado = False

broker_address= "m23.cloudmqtt.com"
port = 17997
user = "udwgocyz"
password = "lC73EBlF8DAd"
topic = "contacto1/ordenes"
im_source = 'espera.png'
			 
client = mqttClient.Client("EstadoAPP")
client.username_pw_set(user, password=password)
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.on_message = on_message

# Programa principal

if __name__ == "__main__":
	conn = threading.Thread(target=conexion)
	conn.start()
	MainApp().run()
	conn.join()
	conn.close()