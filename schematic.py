import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Polygon
from matplotlib.lines import Line2D
import numpy as np
import os

DOWNLOADS = os.path.join(os.path.expanduser("~"), "Downloads")
PDF_FILE  = os.path.join(DOWNLOADS, "tinkerforge_rig_schematic.pdf")

W, H = 42, 30
fig, ax = plt.subplots(figsize=(W/2.54*2.0, H/2.54*2.0))
ax.set_xlim(0, W); ax.set_ylim(0, H)
ax.set_aspect('equal'); ax.axis('off')
fig.patch.set_facecolor('#FFFFFF')

# ── palette ──────────────────────────────────────────────────────
CP  = '#C0392B'   # +12V
CG  = '#626567'   # GND
CD  = '#1A5276'   # data / bricklet cable
CL  = '#1E8449'   # load / signal
CSP = '#AAB7B8'   # spare
BLK = '#1A1A1A'

def wire(x1,y1,x2,y2,col=BLK,lw=1.2,ls='-'):
    ax.plot([x1,x2],[y1,y2],color=col,lw=lw,ls=ls,
            solid_capstyle='round',zorder=2)

def junc(x,y,col=BLK,r=0.18):
    c = plt.Circle((x,y),r,color=col,zorder=5)
    ax.add_patch(c)

def pwr_sym(x,y,label='+12V',col=CP):
    wire(x,y,x,y+0.7,col,2.0)
    ax.text(x,y+0.85,label,ha='center',va='bottom',
            fontsize=7,fontweight='bold',color=col,zorder=6)

def gnd_sym(x,y,col=CG):
    wire(x,y,x,y-0.5,col,1.8)
    for i,w in enumerate([0.55,0.35,0.15]):
        yy = y-0.5-i*0.22
        wire(x-w,yy,x+w,yy,col,1.8)

def label(x,y,s,fs=7.5,col=BLK,ha='center',va='center',fw='normal',rot=0):
    ax.text(x,y,s,fontsize=fs,color=col,ha=ha,va=va,
            fontweight=fw,rotation=rot,zorder=6)

def ic_box(x,y,w,h,name,sub='',fc='#EBF5FB',ec=CD,lw=1.8,
           name_fs=9, sub_fs=7):
    p = FancyBboxPatch((x,y),w,h,
        boxstyle="square,pad=0",
        fc=fc,ec=ec,lw=lw,zorder=3)
    ax.add_patch(p)
    ty = y+h/2 + (0.3 if sub else 0)
    label(x+w/2, ty, name, name_fs, BLK, fw='bold')
    if sub:
        label(x+w/2, y+h/2-0.4, sub, sub_fs, '#555')

def pin_l(x,y,ic_x,label_txt,num='',col=BLK,lw=1.2):
    """Pin on LEFT side of IC: wire from ic_x leftward to x"""
    wire(ic_x, y, x, y, col, lw)
    if num:
        label(ic_x+0.25, y, num, 6.5, '#444', ha='left')
    label(x-0.15, y, label_txt, 7, col, ha='right')

def pin_r(x,y,ic_x,label_txt,num='',col=BLK,lw=1.2):
    """Pin on RIGHT side of IC: wire from ic_x rightward to x"""
    wire(ic_x, y, x, y, col, lw)
    if num:
        label(ic_x-0.25, y, num, 6.5, '#444', ha='right')
    label(x+0.15, y, label_txt, 7, col, ha='left')

# ══════════════════════════════════════════════════════════════════
# TITLE
# ══════════════════════════════════════════════════════════════════
label(21, 29.3, 'Tinkerforge Sensory Rig — Circuit Schematic', 16, BLK, fw='bold')
label(21, 28.7, 'Water Reaching Task  |  ESP32 Brick + 5 Bricklets  |  12 V DC', 10, '#555')

# ══════════════════════════════════════════════════════════════════
# POWER SECTION  (left)
# ══════════════════════════════════════════════════════════════════

# 12V Adapter
ic_box(0.5,24.5,3.8,2.2,'12 V / 2 A','Bel SWI24-12-E-P5',
       fc='#FDEDEC',ec=CP,lw=2,name_fs=8,sub_fs=6.5)
# + out
wire(4.3,25.8,5.2,25.8,CP,2.0)
pwr_sym(4.3,25.8,'+12V',CP)
# GND out
wire(4.3,24.9,5.2,24.9,CG,1.8)
gnd_sym(4.3,24.9,CG)

# ESP32 Power Supply
ic_box(0.5,21.5,3.8,2.2,'ESP32 PSU','SKU 42 | 7–27V→5V',
       fc='#D6EAF8',ec=CD,lw=1.8,name_fs=8,sub_fs=6.5)
# VIN
wire(4.3,23.0,5.5,23.0,CP,1.8)
label(4.35,23.25,'VIN',7,CP,ha='left')
# GND
wire(0.5,22.0,0.0,22.0,CG,1.8); gnd_sym(0.0,22.0,CG)
# 5V out
wire(4.3,22.2,6.0,22.2,CD,1.8)
label(5.1,22.45,'5V',7.5,CD,fw='bold')
# rails from adapter to PSU
wire(5.2,25.8,5.5,25.8,CP,2.0)
wire(5.5,25.8,5.5,23.0,CP,2.0)
junc(5.5,23.0,CP)

# ══════════════════════════════════════════════════════════════════
# ESP32 BRICK  (center-left IC, portrait)
# ══════════════════════════════════════════════════════════════════
EX,EY,EW,EH = 6.0, 8.0, 5.5, 15.5
ic_box(EX,EY,EW,EH,'ESP32 Brick',
       'SKU 113 | FW 2.3.1\nUID: 226Z',
       fc='#EBF5FB',ec=CD,lw=2.2,name_fs=11,sub_fs=8)

# 5V into ESP32
wire(6.0,22.2,6.0,22.2); wire(6.0,22.2,6.5,22.2,CD,1.8)
wire(6.5,22.2,6.5,23.5,CD,1.8)
ax.annotate('',xy=(6.5,23.5),xytext=(6.5,22.2),
    arrowprops=dict(arrowstyle='-|>',color=CD,lw=1.8,mutation_scale=10),zorder=4)
label(5.5,22.2,'5V',7,CD,ha='right',fw='bold')

# GND of ESP32
wire(EX+0.5,EY,EX+0.5,EY-0.5,CG,1.8)
gnd_sym(EX+0.5,EY-0.5+0.5,CG)
wire(EX+0.5,EY,EX+0.5,EY-0.3)
gnd_sym(EX+0.5,EY)

# USB-C → PC
wire(EX+EW/2,EY,EX+EW/2,EY-1.5,'#8E44AD',1.8)
ic_box(EX+EW/2-1.2,EY-3.0,2.4,1.3,'PC','USB-C',
       fc='#F4ECF7',ec='#8E44AD',lw=1.5,name_fs=8,sub_fs=7)
wire(EX+EW/2,EY-1.5,EX+EW/2,EY-3.0,'#8E44AD',1.8)
label(EX+EW/2+0.2,EY-0.9,'USB-C',7,'#8E44AD',ha='left')

# Port pins on RIGHT side
port_y = {
    'A': EY+EH-2.0,
    'B': EY+EH-4.0,
    'C': EY+EH-6.0,
    'D': EY+EH-8.5,
    'E': EY+EH-11.5,
    'F': EY+EH-13.0,
}
for pname,py in port_y.items():
    col = CSP if pname in ('E','F') else CD
    wire(EX+EW, py, EX+EW+0.5, py, col, 1.8)
    label(EX+EW-0.15, py, f'Port {pname}', 7, col, ha='right', fw='bold')
    label(EX+EW+0.6, py, f'Port {pname}', 7, col, ha='left')

# ══════════════════════════════════════════════════════════════════
# PORT A: DIGITAL IN 4
# ══════════════════════════════════════════════════════════════════
PAX = 13.5
PAY = port_y['A'] - 1.5
PAW, PAH = 5.5, 3.2
ic_box(PAX,PAY,PAW,PAH,
       'Digital In 4  2.0',
       'SKU 2100 | UID: 2hA6\nopto-isolated | 0–2V low, 3–36V high',
       fc='#EAFAF1',ec=CL,lw=1.8,name_fs=8.5,sub_fs=7)

# bricklet cable
wire(EX+EW+0.5, port_y['A'], PAX, port_y['A'], CD, 1.8)
wire(PAX, port_y['A'], PAX, PAY+PAH/2, CD, 1.8)
label(PAX-0.15, port_y['A']-0.25, 'Bricklet cable', 6.5, CD, ha='right')

# CH0 → Camera
pin_r(PAX+PAW+0.5, PAY+2.5, PAX+PAW, 'CH0', '', CL)
wire(PAX+PAW+0.5, PAY+2.5, PAX+PAW+1.5, PAY+2.5, CL, 1.5)
ic_box(PAX+PAW+1.5, PAY+2.1, 4.5, 0.9,
       'Camera BNC sync out','BNC → screw terminal (Adafruit 2889)',
       fc='#EAFAF1',ec=CL,lw=1.2,name_fs=7.5,sub_fs=6)

# CH1-3 spare
pin_r(PAX+PAW+0.5, PAY+1.5, PAX+PAW, 'CH1', '', CSP)
label(PAX+PAW+0.65, PAY+1.5, 'spare', 7, CSP, ha='left')
pin_r(PAX+PAW+0.5, PAY+1.0, PAX+PAW, 'CH2', '', CSP)
label(PAX+PAW+0.65, PAY+1.0, 'spare', 7, CSP, ha='left')
pin_r(PAX+PAW+0.5, PAY+0.5, PAX+PAW, 'CH3', '', CSP)
label(PAX+PAW+0.65, PAY+0.5, 'spare', 7, CSP, ha='left')

# ══════════════════════════════════════════════════════════════════
# PORT B: MULTI TOUCH V2
# ══════════════════════════════════════════════════════════════════
PBX = 13.5
PBY = port_y['B'] - 2.0
PBW, PBH = 5.5, 3.8
ic_box(PBX,PBY,PBW,PBH,
       'Multi Touch  2.0',
       'SKU 2129 | UID: LHs\nMPR121 | 12 electrodes\nsensitivity 5–201',
       fc='#EBF5FB',ec=CD,lw=1.8,name_fs=8.5,sub_fs=7)

wire(EX+EW+0.5, port_y['B'], PBX, port_y['B'], CD, 1.8)
wire(PBX, port_y['B'], PBX, PBY+PBH/2, CD, 1.8)
label(PBX-0.15, port_y['B']-0.25, 'Bricklet cable', 6.5, CD, ha='right')

# Electrode 0 → spout
pin_r(PBX+PBW+0.5, PBY+2.8, PBX+PBW, 'E0', '', CD)
wire(PBX+PBW+0.5, PBY+2.8, PBX+PBW+1.5, PBY+2.8, CD, 1.5)
ic_box(PBX+PBW+1.5, PBY+2.35, 4.5, 0.95,
       'Metal Spout (lick sensor)',
       'Dupont jumper + alligator clip',
       fc='#EBF5FB',ec=CD,lw=1.2,name_fs=7.5,sub_fs=6)

for i,ei in enumerate(['E1','E2','..','E11']):
    pin_r(PBX+PBW+0.5, PBY+2.1-i*0.4, PBX+PBW, ei, '', CSP)
    label(PBX+PBW+0.65, PBY+2.1-i*0.4, 'disabled', 6.5, CSP, ha='left')

# ══════════════════════════════════════════════════════════════════
# PORT C: PIEZO SPEAKER
# ══════════════════════════════════════════════════════════════════
PCX = 13.5
PCY = port_y['C'] - 1.5
PCW, PCH = 5.5, 2.8
ic_box(PCX,PCY,PCW,PCH,
       'Piezo Speaker  2.0',
       'SKU 2145 | UID: 24Gg\n50 Hz–15 kHz | built-in speaker\nno external wiring needed',
       fc='#FDEDEC',ec=CP,lw=1.8,name_fs=8.5,sub_fs=7)

wire(EX+EW+0.5, port_y['C'], PCX, port_y['C'], CD, 1.8)
wire(PCX, port_y['C'], PCX, PCY+PCH/2, CD, 1.8)
label(PCX-0.15, port_y['C']-0.25, 'Bricklet cable', 6.5, CD, ha='right')

# ══════════════════════════════════════════════════════════════════
# PORT D: QUAD RELAY 2.1  (big IC, right side)
# ══════════════════════════════════════════════════════════════════
PDX = 13.5
PDY = 2.5
PDW, PDH = 6.0, 12.5
ic_box(PDX,PDY,PDW,PDH,
       'Quad Relay  2.1',
       'SKU 2102 | UID: 2io5\nsolid-state | max 30V / 600mA\npolarity-sensitive',
       fc='#FEF9E7',ec='#E67E22',lw=2.2,name_fs=10,sub_fs=8)

wire(EX+EW+0.5, port_y['D'], PDX, port_y['D'], CD, 1.8)
wire(PDX, port_y['D'], PDX, PDY+PDH-1.5, CD, 1.8)
label(PDX-0.15, port_y['D']-0.25, 'Bricklet cable', 6.5, CD, ha='right')

# CH0 spare
pin_r(PDX+PDW+0.5, PDY+PDH-2.0, PDX+PDW, 'CH0(+)', '', CSP)
pin_r(PDX+PDW+0.5, PDY+PDH-2.6, PDX+PDW, 'CH0(−)', '', CSP)
label(PDX+PDW+0.65, PDY+PDH-2.3, 'spare', 7.5, CSP, ha='left')

# separator
wire(PDX+0.3, PDY+PDH-3.1, PDX+PDW-0.3, PDY+PDH-3.1, '#CCC', 0.8, '--')

# ── CH1: BLUE LED ────────────────────────────────────────────────
CH1Y_P = PDY+PDH-4.0  # (+) pin y
CH1Y_N = PDY+PDH-4.8  # (−) pin y

label(PDX+PDW/2, (CH1Y_P+CH1Y_N)/2+0.35, 'CH1', 9, '#2980B9', fw='bold')
pin_r(PDX+PDW+0.5, CH1Y_P, PDX+PDW, '(+)', '', CP)
pin_r(PDX+PDW+0.5, CH1Y_N, PDX+PDW, '(−)', '', CL)

# +12V to CH1(+)
pwr_sym(PDX+PDW+0.5, CH1Y_P, '+12V', CP)

# CH1(−) → LED → GND
LEDX = PDX+PDW+1.8
LEDY = CH1Y_N
wire(PDX+PDW+0.5, CH1Y_N, LEDX, LEDY, CL, 1.8)

# LED symbol
def led_sym(x,y,col,lbl,sub):
    # diode triangle
    tri = Polygon([[x,y+0.35],[x,y-0.35],[x+0.7,y]],
                   closed=True, fc=col+'55', ec=col, lw=1.5, zorder=4)
    ax.add_patch(tri)
    wire(x+0.7,y+0.35,x+0.7,y-0.35,col,1.8)
    # arrows for light
    for dy in [0.1,-0.1]:
        ax.annotate('',xy=(x+1.1,y+dy+0.35),xytext=(x+0.85,y+dy+0.15),
            arrowprops=dict(arrowstyle='-|>',color=col,lw=1.0,mutation_scale=7),zorder=4)
    wire(x-0.2,y,x,y,col,1.8)
    wire(x+0.7,y,x+0.9,y,col,1.8)
    label(x+0.35,y+0.65,lbl,8,col,fw='bold')
    label(x+0.35,y-0.6,sub,6.5,col)

led_sym(LEDX, LEDY, '#2980B9', 'BLUE LED','VCC 1092C6-12V')
wire(LEDX+0.9, LEDY, LEDX+1.3, LEDY, CL, 1.8)
gnd_sym(LEDX+1.3, LEDY)

wire(PDX+PDW-0.3, PDY+PDH-5.5, PDX+PDW+0.3, PDY+PDH-5.5,'#CCC',0.8,'--')

# ── CH2: SOLENOID VALVE ──────────────────────────────────────────
CH2Y_P = PDY+PDH-6.5
CH2Y_N = PDY+PDH-7.3

label(PDX+PDW/2, (CH2Y_P+CH2Y_N)/2+0.35, 'CH2', 9, CL, fw='bold')
pin_r(PDX+PDW+0.5, CH2Y_P, PDX+PDW, '(+)', '', CP)
pin_r(PDX+PDW+0.5, CH2Y_N, PDX+PDW, '(−)', '', CL)

pwr_sym(PDX+PDW+0.5, CH2Y_P, '+12V', CP)

# Coil (valve) symbol
VX = PDX+PDW+1.8
VY = CH2Y_N
wire(PDX+PDW+0.5, CH2Y_N, VX-0.2, VY, CL, 1.8)

def coil_sym(x,y,col,lbl,sub):
    n=5; r=0.18
    for i in range(n):
        theta = np.linspace(0,np.pi,20)
        cx = x + i*2*r + r
        xs = cx + r*np.cos(theta)
        ys = y + r*np.sin(theta)
        ax.plot(xs,ys,color=col,lw=1.8,zorder=4)
    total_w = n*2*r
    wire(x,y,x+total_w,y,col,1.8)
    ax.add_patch(plt.Rectangle((x,y-r*1.8),total_w,r*1.2,
        fc='none',ec=col,lw=1.2,zorder=3))
    label(x+total_w/2, y+0.55, lbl, 8, col, fw='bold')
    label(x+total_w/2, y-0.7, sub, 6.5, col)
    return x+total_w

coil_end = coil_sym(VX, VY, CL, 'Solenoid Valve','075P2NC12 | 12V NC | 290mA')

# 1N4007 diode parallel
D1X = VX+0.5; D1Y = VY-0.9
wire(D1X, VY, D1X, D1Y, '#888', 1.2)
wire(D1X+1.0, VY, D1X+1.0, D1Y, '#888', 1.2)
tri2 = Polygon([[D1X,D1Y+0.2],[D1X,D1Y-0.2],[D1X+0.6,D1Y]],
                closed=True, fc='#DDD', ec='#555', lw=1.2, zorder=4)
ax.add_patch(tri2)
wire(D1X+0.6,D1Y+0.2,D1X+0.6,D1Y-0.2,'#555',1.5)
label(D1X+0.85,D1Y,'1N4007',6.5,'#555',ha='left')
label(D1X-0.15,D1Y+0.25,'K',6,'#555',ha='right')

wire(coil_end+0.2, VY, coil_end+0.5, VY, CL, 1.8)
gnd_sym(coil_end+0.5, VY)

wire(PDX+PDW-0.3, PDY+PDH-8.0, PDX+PDW+0.3, PDY+PDH-8.0,'#CCC',0.8,'--')

# ── CH3: GREEN LED ───────────────────────────────────────────────
CH3Y_P = PDY+PDH-9.0
CH3Y_N = PDY+PDH-9.8

label(PDX+PDW/2, (CH3Y_P+CH3Y_N)/2+0.35, 'CH3', 9, CL, fw='bold')
pin_r(PDX+PDW+0.5, CH3Y_P, PDX+PDW, '(+)', '', CP)
pin_r(PDX+PDW+0.5, CH3Y_N, PDX+PDW, '(−)', '', CL)

pwr_sym(PDX+PDW+0.5, CH3Y_P, '+12V', CP)

GLEDX = PDX+PDW+1.8
GLEDY = CH3Y_N
wire(PDX+PDW+0.5, CH3Y_N, GLEDX, GLEDY, CL, 1.8)
led_sym(GLEDX, GLEDY, CL, 'GREEN LED','VCC 1092C6-12V')
wire(GLEDX+0.9, GLEDY, GLEDX+1.3, GLEDY, CL, 1.8)
gnd_sym(GLEDX+1.3, GLEDY)

# ── PORT E & F: SPARE ────────────────────────────────────────────
ic_box(13.5,0.3,5.5,1.8,
       'IO-4 V2  |  Digital Out 4  2.0',
       'Port E (spare)  |  Port F (spare / cam trigger)\nSKU 2124 | general purpose I/O',
       fc='#F4F6F7',ec=CSP,lw=1.3,name_fs=8,sub_fs=6.5)
wire(EX+EW+0.5, port_y['E'], 13.5, port_y['E'], CSP, 1.5)
wire(13.5, port_y['E'], 13.5, 2.1, CSP, 1.5)
wire(EX+EW+0.5, port_y['F'], 13.2, port_y['F'], CSP, 1.5)
wire(13.2, port_y['F'], 13.2, 2.1, CSP, 1.5)

# ══════════════════════════════════════════════════════════════════
# LEGEND  (bottom-left)
# ══════════════════════════════════════════════════════════════════
LX,LY = 0.5, 4.5
p = FancyBboxPatch((LX,LY),5.5,6.0,
    boxstyle="square,pad=0",fc='#FAFAFA',ec='#CCC',lw=1,zorder=2)
ax.add_patch(p)
label(LX+2.75, LY+5.7, 'LEGEND', 9, BLK, fw='bold')
items = [
    (CP,  '+12 V power line'),
    (CG,  'GND line'),
    (CD,  'Bricklet cable (5 V)'),
    (CL,  'Load / signal'),
    (CSP, 'Spare'),
]
for i,(c,lbl) in enumerate(items):
    yi = LY+4.9-i*0.9
    wire(LX+0.3,yi,LX+1.1,yi,c,2.5)
    label(LX+1.3, yi, lbl, 8, '#333', ha='left')

# NOTES
notes = [
    '⚠ Relay 2.1: polarity-sensitive — observe (+)/(−)',
    '⚠ 1N4007: parallel to valve, K(stripe)→+12V side',
    'ℹ Multi Touch: recalibrate sensitivity on final rig',
    'ℹ Piezo: ≤15 kHz; 110 dB max ~1.5 min, low vol.',
]
label(LX+2.75, LY-0.35, 'NOTES', 8.5, BLK, fw='bold')
for i,n in enumerate(notes):
    label(LX+0.1, LY-0.8-i*0.55, n, 7.5, '#555', ha='left', va='center')

# ══════════════════════════════════════════════════════════════════
# BORDER
# ══════════════════════════════════════════════════════════════════
border = FancyBboxPatch((0.1,0.1),W-0.2,H-0.2,
    boxstyle="square,pad=0",fc='none',ec='#CCC',lw=1.5,zorder=1)
ax.add_patch(border)

plt.tight_layout(pad=0.2)
plt.savefig(PDF_FILE, format='pdf', bbox_inches='tight',
            facecolor='white', dpi=250)
print(f"Saved: {PDF_FILE}")
plt.show()