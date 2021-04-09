import os
import time
from datetime import datetime
import json
import requests

import paho.mqtt.client as mqtt

from telegram.bot import Bot
from telegram.parsemode import ParseMode

# initializing the bot with API_KEY and CHAT_ID
if os.getenv('TELEGRAM_BOT_API_KEY') == None:
	print("Error: Please set the environment variable TELEGRAM_BOT_API_KEY and try again.")
	exit(1)
bot = Bot(os.getenv('TELEGRAM_BOT_API_KEY'))

if os.getenv('TELEGRAM_BOT_CHAT_ID') == None:
	print("Error: Please set the environment variable TELEGRAM_BOT_CHAT_ID and try again.")
	exit(1)
chat_id = os.getenv('TELEGRAM_BOT_CHAT_ID')
api_url = os.getenv('TELSAMATE_MQTT_API_URL') #It should be something like http://127.0.0.1:3040/car/1?api_key=xxxxxxxxxxx
# based on example from https://pypi.org/project/paho-mqtt/
# The callback for when the client receives a CONNACK response from the server.


def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	if rc == 0:
		print("Connected successfully to broker")
		# bot.send_message(
		# 	chat_id,
		# 	text="Connecté au brocker MQTT...",
		# 	parse_mode=ParseMode.HTML,
		# )
	else:
		print("Connection failed")

	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.

	# client.subscribe("teslamate/cars/1/version")
	# client.subscribe("teslamate/cars/1/update_available")
	# client.subscribe("teslamate/cars/1/doors_open")
	# client.subscribe("teslamate/cars/1/usable_battery_level")
	# client.subscribe("teslamate/cars/1/plugged_in")
	client.subscribe("teslamate/cars/1/time_to_full_charge")
	client.subscribe("teslamate/cars/1/locked")
	client.subscribe("teslamate/cars/1/state")
	# client.subscribe("teslamate/cars/1/shift_state")
	# client.subscribe("teslamate/cars/1/latitude")
	# client.subscribe("teslamate/cars/1/longitude")
	# client.subscribe("teslamate/cars/1/speed")
	# client.subscribe("teslamate/cars/1/heading")

# The callback for when a PUBLISH message is received from the server.


def on_message(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload.decode()))
	now = datetime.now()
	today = now.strftime("%d-%m-%Y %H:%M:%S")
	r = requests.get(api_url)
	jsonData = r.json()
	text_energie = "⚡️ : 🔋" if str(jsonData['plugged_in']) == "0" else "⚡️ : 🔌"
	lock_state = "🔐 verrouilée" if str(jsonData['locked']) == "1" else "🔓 déverrouilée"
	doors_state = "fermées" if str(jsonData['doors_open']) == "0" else "ouvertes"
	trunk_state = "fermé" if str(jsonData['trunk_open']) == "0" else "ouvert"
	clim_state = "éteinte" if str(jsonData['is_climate_on']) == "0" else "allumée"
	current_version = str(jsonData['version'])
	text_update = current_version+" ("+str(jsonData['update_version'])+")" if str(jsonData['update_version']) == "1" else current_version+" (à jour)"

	if msg.topic == "teslamate/cars/1/state":
		print("Changement d'état : "+str(msg.payload.decode()))
		if str(msg.payload.decode()) == "online" or str(msg.payload.decode()) == "asleep" or str(msg.payload.decode()) == "suspended":
			if str(msg.payload.decode()) == "online":
				text_state = "en ligne"
			elif str(msg.payload.decode()) == "suspended":
				text_state = "en train de s'endormir..."
			else:
				text_state = "endormie"
		elif str(msg.payload.decode()) == "charging":
			text_state = "en charge"
			temps_restant = float(jsonData['time_to_full_charge']) * float(60)
			if temps_restant > 1:
				texte_temps = "⏳"+str(temps_restant)+" minutes pour être chargée."
			elif temps_restant == 0:
				texte_temps = "Charge terminée."
			else:
				texte_temps = "⏳"+str(temps_restant)+" minute pour être chargée."
			text_energie = "⚡️ : 🔌 "+texte_temps
		elif str(msg.payload.decode()) == "offline":
			text_state = "éteinte"
		elif str(msg.payload.decode()) == "driving":
			text_state = "en conduite"
		else:
			text_state = str(msg.payload.decode())

	if msg.topic == "teslamate/cars/1/time_to_full_charge":
		print("Temps de chargement restant : "+str(msg.payload.decode()))
		if int(jsonData['time_to_full_charge']) > 0:
			text_state = "en charge"
			temps_restant = float(jsonData['time_to_full_charge']) * float(60)
			if temps_restant > 1:
				texte_temps = "⏳"+str(temps_restant)+" minutes pour être chargée."
			elif temps_restant == 0:
				texte_temps = "Charge terminée."
			else:
				texte_temps = "⏳"+str(temps_restant)+" minute pour être chargée."
			text_energie = "⚡️ : 🔌 "+texte_temps

	if msg.topic == "teslamate/cars/1/locked":
		text_state = "verrouilléé" if str(msg.payload.decode()) == "true" else "déverrouilléé"

	text_msg = "🚙 Ma Tesla est <b>"+text_state+"</b> : "+str(today)+"\n🔋 : "+str(jsonData['usable_battery_level'])+"% ("+str(jsonData['est_battery_range_km'])+" km)\n⚡️ : "+text_energie+"\n"+lock_state+"\nPortes : "+doors_state+"\nCoffre : "+trunk_state+"\n🌡 intérieure : "+str(jsonData['inside_temp'])+"c\n🌡 extérieure : "+str(jsonData['outside_temp'])+"c\nClim : "+clim_state+"\nVersion : "+text_update

	bot.send_message(
		chat_id,
		text=str(text_msg),
		parse_mode=ParseMode.HTML,
	)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(os.getenv('MQTT_BROKER_HOST', '127.0.0.1'),
			   int(os.getenv('MQTT_BROKER_PORT', 1883)), 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
# client.loop_forever()


client.loop_start()  # start the loop
try:
	while True:
		time.sleep(1)

except KeyboardInterrupt:

	print("exiting")


client.disconnect()

client.loop_stop()
