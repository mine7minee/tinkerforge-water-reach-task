"""
test_rig.py
Full hardware test — runs each component once in sequence.
Run this after wiring to verify everything is connected correctly.

Test sequence:
  1. Piezo Speaker  — plays a 1 kHz beep for 500 ms
  2. Relay CH1      — Blue LED on for 1 second
  3. Relay CH2      — Solenoid valve opens for 1 second
  4. Relay CH3      — Green LED on for 1 second
"""

import time
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_piezo_speaker_v2 import BrickletPiezoSpeakerV2
from tinkerforge.bricklet_industrial_quad_relay_v2 import BrickletIndustrialQuadRelayV2

HOST = "10.0.0.1"
PORT = 4223

UID_PIEZO = "XXXX"   # Replace with your Piezo Speaker UID from Brick Viewer
UID_RELAY = "XXXX"   # Replace with your Quad Relay UID from Brick Viewer

ipcon = IPConnection()
piezo = BrickletPiezoSpeakerV2(UID_PIEZO, ipcon)
relay = BrickletIndustrialQuadRelayV2(UID_RELAY, ipcon)

ipcon.connect(HOST, PORT)

print("=" * 40)
print("Tinkerforge Rig — Hardware Test")
print("=" * 40)

# ── Test 1: Piezo Speaker ─────────────────────────────────────────
print("Test 1: Piezo Speaker (1 kHz beep, 500 ms)")
piezo.set_beep(1000, 5, 500)
time.sleep(1)

# ── Test 2: Blue LED (Relay CH1) ─────────────────────────────────
print("Test 2: Blue LED on (Relay CH1) — 1 second")
relay.set_value([False, True, False, False])
time.sleep(1)
relay.set_value([False, False, False, False])

# ── Test 3: Solenoid Valve (Relay CH2) ───────────────────────────
print("Test 3: Solenoid valve open (Relay CH2) — 1 second")
relay.set_value([False, False, True, False])
time.sleep(1)
relay.set_value([False, False, False, False])

# ── Test 4: Green LED (Relay CH3) ────────────────────────────────
print("Test 4: Green LED on (Relay CH3) — 1 second")
relay.set_value([False, False, False, True])
time.sleep(1)
relay.set_value([False, False, False, False])

print("\nAll tests passed.")
ipcon.disconnect()
