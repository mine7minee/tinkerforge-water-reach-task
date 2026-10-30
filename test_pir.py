import time
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_motion_detector import BrickletMotionDetector

HOST = "localhost"
PORT = 4223
UID = "kgD"
MIN_ARALIK = 0.3  # saniye — iki dokunma arası minimum süre

ipcon = IPConnection()
md = BrickletMotionDetector(UID, ipcon)
ipcon.connect(HOST, PORT)

dokunma_sayisi = 0
son_dokunma_zamani = 0
son_durum = None
deney_baslangic = time.time()
sureler = []

print("Dokunma sayaci basladi... (Ctrl+C ile cik)")
print(f"Min aralik: {MIN_ARALIK}s")
print("-" * 40)

try:
    while True:
        durum = md.get_motion_detected()
        simdi = time.time()
        gecen = simdi - deney_baslangic

        # Sadece LOW→HIGH geçişini say
        if durum == md.MOTION_DETECTED and son_durum != md.MOTION_DETECTED:
            aralik = simdi - son_dokunma_zamani
            if aralik >= MIN_ARALIK:
                dokunma_sayisi += 1
                son_dokunma_zamani = simdi
                print(f"[{gecen:.1f}s] DOKUNMA #{dokunma_sayisi} "
                      f"(oncekinden {aralik:.2f}s sonra)")

        son_durum = durum
        time.sleep(0.03)

except KeyboardInterrupt:
    pass

print("\n" + "=" * 40)
print("DENEY SONU OZETI")
print("=" * 40)
print(f"Toplam dokunma : {dokunma_sayisi}")
print(f"Deney suresi   : {time.time()-deney_baslangic:.1f} saniye")
if dokunma_sayisi > 1:
    toplam = time.time() - deney_baslangic
    print(f"Ort aralik     : {toplam/dokunma_sayisi:.2f} saniye")
ipcon.disconnect()