import time
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_motion_detector import BrickletMotionDetector

HOST = "localhost"
PORT = 4223
UID = "kgD"

ipcon = IPConnection()
md = BrickletMotionDetector(UID, ipcon)
ipcon.connect(HOST, PORT)

hareket_sayisi = 0
toplam_sure = 0
baslangic = None
son_durum = None
deney_baslangic = time.time()

print("Motion sayaci basladi... (Ctrl+C ile cik)")
print("-" * 40)

try:
    while True:
        durum = md.get_motion_detected()

        if durum != son_durum:
            simdi = time.time()
            gecen = simdi - deney_baslangic

            if durum == md.MOTION_DETECTED:
                hareket_sayisi += 1
                baslangic = simdi
                print(f"[{gecen:.1f}s] HAREKET #{hareket_sayisi} basladi")

            else:
                if baslangic:
                    sure = simdi - baslangic
                    toplam_sure += sure
                    print(f"[{gecen:.1f}s] Bitti | "
                          f"Sure: {sure:.1f}s | "
                          f"Toplam: {hareket_sayisi} hareket | "
                          f"Ort: {toplam_sure/hareket_sayisi:.1f}s")
                    baslangic = None

            son_durum = durum

        time.sleep(0.05)

except KeyboardInterrupt:
    pass

print("\n" + "=" * 40)
print("DENEY SONU OZETI")
print("=" * 40)
print(f"Toplam hareket : {hareket_sayisi}")
print(f"Toplam sure    : {toplam_sure:.1f} saniye")
if hareket_sayisi > 0:
    print(f"Ortalama sure  : {toplam_sure/hareket_sayisi:.1f} saniye")
print(f"Deney suresi   : {time.time()-deney_baslangic:.1f} saniye")
ipcon.disconnect()
