# Tinkerforge Sensory Rig — Water Reaching Task

**Author:** Meryem Mine Kurum  
**Date:** 29 October 2026  
**System:** Tinkerforge ESP32 Brick + 5 Bricklets | 12 V DC | Windows 11  

---

## What This Is

This repository contains the hardware setup and experiment code for a **water reaching task** behavioural rig built on the [Tinkerforge](https://www.tinkerforge.com) modular electronics platform.

In each trial, the rig:
1. Plays a beep at trial start
2. Lights a random LED (blue or green) at second 3
3. Opens a water valve for 300 ms at second 6 (reward delivery)
4. Turns the LED off at second 9
5. Listens for lick sensor contacts throughout the 15-second trial

All events are logged to a timestamped Excel file saved automatically to the Downloads folder.

---

## Repository Structure

```
tinkerforge-water-reach-task/
│
├── README.md
├── requirements.txt
├── SETUP_WINDOWS.md
│
├── code/
│   └── 29102026_HardwareCode_WaterReachTask_AsliAyaz.py
│
├── hardware/
│   └── Tinkerforge_SensoryRig_WaterReachTask_AsliAyaz.pdf
│
├── schematic/
│   └── schematic.py
│
└── tests/
    ├── test_motion.py
    ├── test_pir.py
    └── test_rig.py
```

---

## Hardware

| Component | Part | SKU | Role |
|---|---|---|---|
| ESP32 Brick | Tinkerforge | 113 | Main controller, WiFi, timer |
| ESP32 Power Supply | Tinkerforge | 42 | 12 V → 5 V for ESP32 |
| Industrial Digital In 4 v2 | Tinkerforge | 2100 | Camera sync input (Port A) |
| Multi Touch Bricklet v2 | Tinkerforge | 2129 | Lick sensor — metal spout (Port B) |
| Piezo Speaker Bricklet v2 | Tinkerforge | 2145 | Acoustic cue (Port C) |
| Industrial Quad Relay v2.1 | Tinkerforge | 2102 | LED + valve switching (Port D) |
| IO-4 Bricklet v2 | Tinkerforge | — | Spare (Port E) |
| Digital Out 4 Bricklet v2 | Tinkerforge | 2124 | Spare / camera trigger (Port F) |
| 12 V / 2 A Adapter | Bel SWI24-12-E-P5 | — | Power supply |
| Solenoid Valve | Bio-Chem 075P2NC12 | — | Water reward delivery |
| Blue LED 12 V | VCC 1092C6-12V | — | Visual cue |
| Green LED 12 V | VCC 1092C6-12V | — | Reward cue |
| 1N4007 Diode | MCC 1N4007-TP | — | Flyback protection for valve |

### Relay Channel Map

| Channel | Device | Purpose |
|---|---|---|
| CH0 | — | Spare |
| CH1 | Blue LED | Visual cue |
| CH2 | Solenoid Valve | Water reward |
| CH3 | Green LED | Reward cue |

---

## Trial Structure

```
 0 s  ── Beep (500 ms)
 3 s  ── LED on  (BLUE or GREEN, random each trial)
 6 s  ── Valve opens (300 ms) → water delivered
 6.3s ── Valve closes / LED stays on
 9 s  ── LED off
15 s  ── Trial ends → next trial (0.5 s inter-trial interval)
```

The lick sensor is active throughout the full 15 seconds.
Every contact is counted and timestamped.

---

## Output Data

After each session, an Excel file is saved automatically to Downloads:

```
deney_YYYYMMDD_HHMMSS.xlsx
```

| Sheet | Contents |
|---|---|
| Trial Data | One row per trial: LED colour, licked, lick count, duration, log |
| Summary | Totals and percentages by LED condition |
| Log | Timestamped event log for every trial |

---

## WiFi Connection

The ESP32 Brick runs as a WiFi access point.
Connect your PC to the ESP32 network before running the experiment.

| Setting | Value |
|---|---|
| Network SSID | printed on your ESP32 Brick |
| Host IP | check Brick Viewer after connecting |
| Port | 4223 |

> WiFi password is stored in the shared lab drive. Do not commit it to this repository.

---

## Configurable Parameters

Open the experiment script and edit these values at the top of the file:

```python
TOTAL_TRIALS = 50     # number of trials
TRIAL_DUR    = 15.0   # trial length in seconds
LED_START    = 3.0    # second at which LED turns on
LED_DUR      = 6.0    # how long LED stays on (seconds)
VALVE_TIME   = 6.0    # second at which valve opens
VALVE_DUR    = 0.3    # valve open duration (300 ms)
```

Also fill in your Bricklet UIDs (found in Brick Viewer):

```python
UID_PIEZO = "XXXX"
UID_RELAY = "XXXX"
UID_TOUCH = "XXXX"
```

---

## Running the Experiment

```
1. Plug in the 12 V adapter
2. Connect PC WiFi to the ESP32 network
3. Open Command Prompt
4. Run:
   cd C:\rig
   tkforge\Scripts\activate
   python code\29102026_HardwareCode_WaterReachTask_AsliAyaz.py
5. Press Enter to start
6. Press Ctrl+C to stop and save summary
```

---

## First Time Setup

See SETUP_WINDOWS.md for full step-by-step installation instructions.

---

## License

For internal lab use only. Do not distribute without permission.
