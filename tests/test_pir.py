"""
test_pir.py
PIR / touch sensor polling test.
Counts contact events using the Motion Detector Bricklet v1.
Use this to verify the touch pad or PIR sensor wiring.
"""

import time
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_motion_detector import BrickletMotionDetector

HOST = "10.0.0.1"
PORT = 4223
UID  = "XXXX"    # Replace with your Motion Detector Bricklet UID from Brick Viewer

ipcon  = IPConnection()
sensor = BrickletMotionDetector(UID, ipcon)
ipcon.connect(HOST, PORT)

contact_count   = 0
total_duration  = 0.0
onset_time      = None
last_state      = None
session_start   = time.time()

print("PIR / touch sensor started... (Ctrl+C to stop)")
print("-" * 40)

try:
    while True:
        state   = sensor.get_motion_detected()
        elapsed = time.time() - session_start

        if state != last_state:
            if state == sensor.MOTION_DETECTED:
                contact_count += 1
                onset_time     = time.time()
                print(f"[{elapsed:.1f}s] CONTACT #{contact_count} started")
            else:
                if onset_time is not None:
                    duration        = time.time() - onset_time
                    total_duration += duration
                    avg             = total_duration / contact_count
                    print(f"[{elapsed:.1f}s] Released | "
                          f"Duration: {duration:.2f}s | "
                          f"Total: {contact_count} | "
                          f"Avg: {avg:.2f}s")
                    onset_time = None

            last_state = state

        time.sleep(0.05)

except KeyboardInterrupt:
    pass

print("\n" + "=" * 40)
print("SESSION SUMMARY")
print("=" * 40)
print(f"Total contacts   : {contact_count}")
print(f"Total active time: {total_duration:.2f} seconds")
if contact_count > 0:
    print(f"Average duration : {total_duration/contact_count:.2f} seconds")
print(f"Session duration : {time.time()-session_start:.1f} seconds")
ipcon.disconnect()
