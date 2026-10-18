from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "charts"
OUT.mkdir(parents=True, exist_ok=True)
W, H = 1800, 1000
NAVY = "#102A43"
TEAL = "#0E8A8A"
GOLD = "#E2A93B"
BLUE = "#4F78A8"
RED = "#C75B5B"
MUTED = "#526777"
GRID = "#D9E2E8"
BG = "#FAFCFD"
INK = "#152B3B"
FONT_PATH = r"C:\Windows\Fonts\arial.ttf"
FONT_BOLD_PATH = r"C:\Windows\Fonts\arialbd.ttf"

def f(size, bold=False):
    return ImageFont.truetype(FONT_BOLD_PATH if bold else FONT_PATH, size)

def setup(title, subtitle):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W, 18), fill=TEAL)
    d.text((92, 66), title, font=f(50, True), fill=NAVY)
    d.text((94, 132), subtitle, font=f(27), fill=MUTED)
    return im, d

def footer(d, text="Illustrative synthetic KES case · Partner data would calibrate future estimates"):
    d.line((92, 910, 1708, 910), fill=GRID, width=2)
    d.text((94, 930), text, font=f(20), fill=MUTED)

def tick_label(d, x, y, text, font=None, fill=INK, anchor="mm"):
    d.text((x, y), text, font=font or f(22), fill=fill, anchor=anchor)

# 1: Credible intervals
im, d = setup("Posterior risk factors retain material uncertainty", "Draw-wise calibrated joint expected-loss relativities · 90% credible intervals")
left, right, top, bottom = 420, 1300, 300, 770
lo, hi = 0.4, 2.2
def xscale(v): return left + (v-lo)/(hi-lo)*(right-left)
for v in [0.5, 1.0, 1.5, 2.0]:
    x = xscale(v)
    d.line((x, top, x, bottom), fill=GRID, width=2)
    tick_label(d, x, bottom+36, f"{v:.1f}")
d.line((xscale(1.0), top-30, xscale(1.0), bottom+4), fill=GOLD, width=5)
d.text((xscale(1.0)+12, top-62), "Portfolio mean = 1", font=f(21, True), fill="#9C6B00")
rows = [
    ("Stable", 0.7112, 0.561, 0.859, BLUE, 465),
    ("Volatile", 1.6739, 1.329, 2.023, TEAL, 675),
]
for label, mean, a, b, color, y in rows:
    d.text((110, y-29), label, font=f(30, True), fill=NAVY)
    d.line((xscale(a), y, xscale(b), y), fill=color, width=12)
    d.line((xscale(a), y-23, xscale(a), y+23), fill=color, width=4)
    d.line((xscale(b), y-23, xscale(b), y+23), fill=color, width=4)
    d.ellipse((xscale(mean)-13, y-13, xscale(mean)+13, y+13), fill=NAVY)
    # Exact posterior means and intervals are printed in the accompanying slide callouts.
d.text((left, 815), "Calibrated factor", font=f(24, True), fill=INK)
footer(d)
im.save(OUT / "FIGURE_01_BAYESIAN_RELATIVITIES_90CI.png", dpi=(180, 180))

# 2: Tariff allocation
im, d = setup("Neutral differentiation reallocates the KES 130,000 premium", "Exposure-weighted expected-loss allocation · 70% stable / 30% volatile portfolio")
labels = [("Stable", 113988, BLUE), ("Flat portfolio premium", 130000, GOLD), ("Volatile", 167360, TEAL)]
left, right, top, rowgap = 450, 1570, 270, 180
maxv = 180000
for tick in [0, 50000, 100000, 150000]:
    x = left + tick/maxv*(right-left)
    d.line((x, 245, x, 790), fill=GRID, width=2)
    tick_label(d, x, 815, f"{tick//1000}k" if tick else "0", f(20), MUTED)
for idx, (name, val, color) in enumerate(labels):
    y = top + idx*rowgap
    d.text((100, y+13), name, font=f(28, True), fill=NAVY)
    x1 = left + val/maxv*(right-left)
    d.rounded_rectangle((left, y, x1, y+72), radius=12, fill=color)
    d.text((x1+18, y+13), f"KES {val:,.0f}", font=f(26, True), fill=INK)
d.text((1030, 745), "0.70 × 113,988 + 0.30 × 167,360 ≈ 130,000", font=f(25, True), fill=NAVY, anchor="mm")
footer(d)
im.save(OUT / "FIGURE_02_TARIFF_ALLOCATION_VS_FLAT_PREMIUM.png", dpi=(180, 180))

# 3: Profit interval with point and 90% interval
im, d = setup("Intervention sensitivity improves the mean; downside remains", "Insurer profit after a 10% volatile-group frequency reduction assumption · KES millions")
left, right, top, bottom = 460, 1610, 290, 770
lo, hi = -1.5, 4.0
def xs(v): return left + (v-lo)/(hi-lo)*(right-left)
for v in [-1,0,1,2,3,4]:
    x=xs(v)
    d.line((x,top,x,bottom), fill=GOLD if v==0 else GRID, width=5 if v==0 else 2)
    tick_label(d,x,bottom+35,f"{v:.0f}",f(21),MUTED)
scenarios=[
    ("Flat / neutral",1.307,-1.158,3.434,BLUE,450),
    ("Assumed intervention",1.442,-1.048,3.518,TEAL,650),
]
for label,mean,low,high,color,y in scenarios:
    d.text((110,y-28),label,font=f(28,True),fill=NAVY)
    d.line((xs(low),y,xs(high),y),fill=color,width=14)
    d.line((xs(low),y-24,xs(low),y+24),fill=color,width=4)
    d.line((xs(high),y-24,xs(high),y+24),fill=color,width=4)
    d.ellipse((xs(mean)-14,y-14,xs(mean)+14,y+14),fill=NAVY)
    d.text((xs(mean),y-50),f"Mean {mean:.3f}",font=f(22,True),fill=INK,anchor="mm")
d.text((1040, 815), "Profit after capital charge (KES m)", font=f(23, True), fill=INK, anchor="mm")
footer(d, "Predictive 90% intervals · 8,000 paths · Assumed intervention sensitivity; pilot estimates its effect")
im.save(OUT / "FIGURE_03_INSURER_PROFIT_TEST_WITH_90CI.png", dpi=(180, 180))

# 4: Downtime and driver take-home, separate scales / panels
im, d = setup("Vehicle availability and driver cash move together", "Three separate service assumptions · annual fleet downtime and per-vehicle driver take-home")
scenarios = [
    ("Flat · 12-day repair", 344.95, 136289, BLUE),
    ("Assumed frequency intervention · 12-day repair", 329.61, 138905, TEAL),
    ("Flat · 2-day repair", 58.61, 152651, GOLD),
]
panel_lefts=[120,960]
for pidx,(title,unit,maximum,values_idx) in enumerate([
    ("Fleet downtime", "fleet days / year", 400, 1),
    ("Driver take-home", "KES / vehicle-year", 170000, 2),
]):
    pl=panel_lefts[pidx]; pr=pl+710
    d.text((pl,225),title,font=f(30,True),fill=NAVY)
    d.text((pl,268),unit,font=f(21),fill=MUTED)
    for idx,(name,days,cash,color) in enumerate(scenarios):
        value=days if values_idx==1 else cash
        y=350+idx*160
        d.text((pl,y-37),name,font=f(20,True),fill=INK)
        x1=pl+value/maximum*610
        d.rounded_rectangle((pl,y,x1,y+54),radius=9,fill=color)
        label=f"{value:.1f}" if values_idx==1 else f"{value:,.0f}"
        d.text((x1+12,y+9),label,font=f(22,True),fill=INK)
        d.line((pl,y+76,pr,y+76),fill=GRID,width=1)
footer(d,"Operator contribution is before vehicle capex, debt, tax and depreciation · Repair event counted once")
im.save(OUT / "FIGURE_04_REPAIR_DOWNTIME_AND_DRIVER_CASH.png", dpi=(180, 180))

print("Created:")
for p in sorted(OUT.glob("*.png")):
    print(p.name, p.stat().st_size)

