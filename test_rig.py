import time
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_piezo_speaker_v2 import BrickletPiezoSpeakerV2
from tinkerforge.bricklet_industrial_quad_relay_v2 import BrickletIndustrialQuadRelayV2

HOST = "10.0.0.1"
PORT = 4223

UID_PIEZO = "24Gg"
UID_RELAY = "2io5"

ipcon = IPConnection()
piezo = BrickletPiezoSpeakerV2(UID_PIEZO, ipcon)
relay = BrickletIndustrialQuadRelayV2(UID_RELAY, ipcon)

ipcon.connect(HOST, PORT)

print("Test 1: Piezo ses")
piezo.set_beep(1000, 5, 500)
time.sleep(1)

print("Test 2: Relay CH0 ac (valf)")
relay.set_value([True, False, False, False])
time.sleep(1)
relay.set_value([False, False, False, False])

print("Test 3: Relay CH1 ac (LED)")
relay.set_value([False, True, False, False])
time.sleep(1)
relay.set_value([False, False, False, False])

print("Tum testler tamam!")
ipcon.disconnect()