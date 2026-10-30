import time
import threading
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_piezo_speaker_v2 import BrickletPiezoSpeakerV2
from tinkerforge.bricklet_industrial_quad_relay_v2 import BrickletIndustrialQuadRelayV2
from tinkerforge.bricklet_multi_touch_v2 import BrickletMultiTouchV2

HOST = "10.0.0.1"
PORT = 4223

UID_PIEZO = "24Gg"
UID_RELAY = "2io5"
UID_TOUCH = "LHs"

ipcon = IPConnection()
piezo = BrickletPiezoSpeakerV2(UID_PIEZO, ipcon)
relay = BrickletIndustrialQuadRelayV2(UID_RELAY, ipcon)
touch = BrickletMultiTouchV2(UID_TOUCH, ipcon)

ipcon.connect(HOST, PORT)

touch.set_electrode_config([True, False, False, False, False, False, False, False, False, False, False, False, False])

# CH0 = Su valfi
# CH1 = Mavi LED
# CH2 = Yeşil LED
# CH3 = Boş

VALF_ACIK_SURE  = 2.0  # saniye — valf açık kalır
VALF_KAPALI_SURE = 2.0  # saniye — valf kapalı kalır

yalama_sayisi = 0
son_touch_durumu = False
deney_baslangic = time.time()
calisıyor = True

def valf_dongusu():
    while calisıyor:
        # Valf aç + Yeşil LED yak
        relay.set_value([True, True, True, False])
        print("  [VALF] Açık")
        time.sleep(VALF_ACIK_SURE)

        if not calisıyor:
            break

        # Valf kapat + Yeşil LED söndür
        relay.set_value([False, True, False, False])
        print("  [VALF] Kapalı")
        time.sleep(VALF_KAPALI_SURE)

def deney_baslat():
    print("\n--- DENEY BAŞLADI ---")
    piezo.set_beep(1000, 5, 200)
    time.sleep(0.3)
    relay.set_value([False, True, False, False])
    print("Mavi LED yandı — görsel uyaran aktif")

def deney_bitir():
    global calisıyor
    calisıyor = False
    print("\n--- DENEY BİTTİ ---")
    relay.set_value([False, False, False, False])
    piezo.set_beep(500, 3, 500)
    time.sleep(0.5)
    print(f"Toplam yalama : {yalama_sayisi}")
    print(f"Deney süresi  : {time.time()-deney_baslangic:.1f} saniye")

print("Sistem hazır. Deney başlıyor...")
time.sleep(1)
deney_baslat()

# Valf döngüsünü ayrı thread'de başlat
valf_thread = threading.Thread(target=valf_dongusu, daemon=True)
valf_thread.start()

print("Emziği yalamasını bekle... (Ctrl+C ile bitir)")

try:
    while True:
        state = touch.get_touch_state()
        elektrod_0 = state[0]

        if elektrod_0 and not son_touch_durumu:
            yalama_sayisi += 1
            gecen = time.time() - deney_baslangic
            print(f"[{gecen:.1f}s] YALAMA #{yalama_sayisi}")

        son_touch_durumu = elektrod_0
        time.sleep(0.05)

except KeyboardInterrupt:
    deney_bitir()
    ipcon.disconnect()
    print("Durduruldu.")