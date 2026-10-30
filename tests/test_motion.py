"""
test_motion.py
Motion detection test using Motion Detector Bricklet v1.
Counts motion events and reports duration statistics.
Run this to verify the PIR sensor is working before a session.
"""

import time
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_motion_detector import BrickletMotionDetector

HOST = "XX.X.X.X"
PORT = YYYY
UID  = "XXXX"    # Replace with your Motion Detector Bricklet UID from Brick Viewer

ipcon  = IPConnection()
motion = BrickletMotionDetector(UID, ipcon)
ipcon.connect(HOST, PORT)

motion_count   = 0
total_duration = 0.0
onset_time     = None
last_state     = None
session_start  = time.time()

print("Motion counter started... (Ctrl+C to stop)")
print("-" * 40)

try:
    while True:
        state = motion.get_motion_detected()
        elapsed = time.time() - session_start

        if state != last_state:
            if state == motion.MOTION_DETECTED:
                motion_count += 1
                onset_time    = time.time()
                print(f"[{elapsed:.1f}s] MOTION #{motion_count} started")
            else:
                if onset_time is not None:
                    duration       = time.time() - onset_time
                    total_duration += duration
                    avg            = total_duration / motion_count
                    print(f"[{elapsed:.1f}s] Done | "
                          f"Duration: {duration:.1f}s | "
                          f"Total: {motion_count} | "
                          f"Avg: {avg:.1f}s")
                    onset_time = None

            last_state = state

        time.sleep(0.05)

except KeyboardInterrupt:
    pass

print("\n" + "=" * 40)
print("SESSION SUMMARY")
print("=" * 40)
print(f"Total motions    : {motion_count}")
print(f"Total active time: {total_duration:.1f} seconds")
if motion_count > 0:
    print(f"Average duration : {total_duration/motion_count:.1f} seconds")
print(f"Session duration : {time.time()-session_start:.1f} seconds")
ipcon.disconnect()
