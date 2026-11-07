# Escenas ilustradas para cada paso de las recetas.
# Cada paso tiene su escena: el recipiente (bol, sartén, plato, horno...) con lo que hay dentro en ese momento.
# Lienzo 120x84, estilo plano como el resto de la web.
import math, random, zlib
from illus import food

INK = "#262626"; LINE = "#d8d3bc"; TERRA = "#c96a47"; GREEN = "#4a8760"; GOLD = "#c9962f"

def _ic(n, x, y, size):
    """Icono de alimento de la web, centrado en (x,y)."""
    s = size / 64
    return f'<g transform="translate({x-size/2:.1f} {y-size/2:.1f}) scale({s:.3f})">{food(n).replace("<svg ", "<svg width=\"64\" height=\"64\" ", 1)}</g>'

def _sc(rng, cx, cy, rx, ry, n, f, margin=.78):
    """Reparte n piezas dentro de una elipse (determinista)."""
    out = []
    for i in range(n):
        a = i * 2.39996 + rng.random() * .4
        r = math.sqrt((i + .5) / n) * margin
        out.append(f(cx + math.cos(a) * rx * r, cy + math.sin(a) * ry * r, i))
    return "".join(out)

# ---------------------------------------------------------------- piezas (centradas en x,y)
def p_fork(x, y, ang=-145, L=30, s=1):
    """Tenedor con las puntas en (x,y) y el mango hacia arriba a la derecha."""
    c, hl = "#a9a9a9", "#d6d6d6"
    tines = "".join(f'<rect x="{-5.6+i*3.2:.1f}" y="0" width="1.7" height="10" rx=".85" fill="{c}"/>' for i in range(4))
    return (f'<g transform="translate({x} {y}) rotate({ang}) scale({s})">{tines}'
            f'<path d="M-5.6 8.5h11.2v2.5a2 2 0 0 1-.6 1.4L1.9 18h-3.8l-3.1-5.6a2 2 0 0 1-.6-1.4z" fill="{c}"/>'
            f'<rect x="-1.9" y="17" width="3.8" height="{L}" rx="1.9" fill="{c}"/><rect x="-.6" y="20" width="1.1" height="{L-6}" rx=".5" fill="{hl}"/></g>')

def p_banana(x, y, s=1, r=0):
    """Plátano pelado."""
    return (f'<g transform="translate({x} {y}) rotate({r}) scale({s})">'
            f'<path d="M-19 -7C-13 7 11 9 19 -3c1.5-2 4.5-1 3.6 1.6C14 15-13 15-22.6-1.6c-1-2.4 2.6-5 3.6-5.4z" fill="#f6e39a"/>'
            f'<path d="M-16 -2c7 8 22 9 33-1" stroke="#e8cf6e" stroke-width="1.4" fill="none" stroke-linecap="round"/>'
            f'<path d="M-14 3c8 6 20 6 30-2" stroke="#fff6cf" stroke-width="2" fill="none" stroke-linecap="round" opacity=".7"/>'
            f'<ellipse cx="-20.5" cy="-4.5" rx="2.2" ry="2" fill="#ead27a"/></g>')

def p_mash(x, y, c="#f3d36b", w=22):
    return (f'<path d="M{x-w} {y}c2-6 9-8 14-6s8-4 14-2 10 4 9 8-6 6-14 5-10 2-15 0-9-2-8-5z" fill="{c}"/>'
            f'<path d="M{x-w*.5} {y-2}q4-2 8 0M{x+2} {y+1}q4-2 7 0" stroke="#fff" stroke-width="1.4" fill="none" opacity=".55" stroke-linecap="round"/>')
def p_egg(x, y, s=1):
    return (f'<path d="M{x-9*s} {y}c0-6 5-8 9-7 5-2 10 1 9 6 1 5-4 8-9 7-5 1-10-1-9-6z" fill="#fff"/>'
            f'<circle cx="{x+.5}" cy="{y-.5}" r="{4.2*s}" fill="#f2b630"/><circle cx="{x-.8}" cy="{y-2}" r="{1.2*s}" fill="#fff" opacity=".7"/>')
def p_oats(x, y, n=7, c="#e9d7a8", rng=None):
    rng = rng or random.Random(3)
    return "".join(f'<ellipse cx="{x+rng.uniform(-9,9):.1f}" cy="{y+rng.uniform(-3,3):.1f}" rx="2.6" ry="1.6" fill="{c}" stroke="#d9c38a" stroke-width=".6" transform="rotate({rng.randint(-60,60)} {x} {y})"/>' for _ in range(n))
def p_oil(x, y):
    return f'<ellipse cx="{x}" cy="{y}" rx="9" ry="3" fill="#c4cf5a" opacity=".55"/><ellipse cx="{x-2}" cy="{y-.8}" rx="3" ry="1" fill="#fff" opacity=".5"/>'
def p_pancake(x, y, s=1, c="#e8b453", cooked=True):
    top = "#f1c873" if not cooked else "#e9b04f"
    return (f'<ellipse cx="{x}" cy="{y+1.6*s}" rx="{11*s}" ry="{4.6*s}" fill="#c98a33"/>'
            f'<ellipse cx="{x}" cy="{y}" rx="{11*s}" ry="{4.6*s}" fill="{top}"/>'
            f'<ellipse cx="{x-2*s}" cy="{y-1*s}" rx="{4*s}" ry="{1.3*s}" fill="#f6d792" opacity=".8"/>')
def p_ball(x, y, s=1, c="#a5583c", hl="#c97a5a"):
    return f'<circle cx="{x}" cy="{y}" r="{5.5*s}" fill="{c}"/><circle cx="{x-1.8*s}" cy="{y-1.8*s}" r="{1.6*s}" fill="{hl}"/>'
def p_nugget(x, y, s=1, r=0):
    return (f'<g transform="rotate({r} {x} {y})"><rect x="{x-8*s}" y="{y-4*s}" width="{16*s}" height="{8*s}" rx="{4*s}" fill="#d99a45"/>'
            + "".join(f'<circle cx="{x+dx*s}" cy="{y+dy*s}" r=".9" fill="#b97a2c"/>' for dx, dy in [(-4, -1), (0, 1), (4, -1.5), (-1, -2.5), (5, 1.5)]) + '</g>')
def p_patty(x, y, s=1, c="#8a5a3a"):
    return (f'<ellipse cx="{x}" cy="{y+1.4*s}" rx="{8*s}" ry="{3.6*s}" fill="#6e4329"/><ellipse cx="{x}" cy="{y}" rx="{8*s}" ry="{3.6*s}" fill="{c}"/>'
            f'<circle cx="{x-3*s}" cy="{y}" r=".9" fill="#e8892a"/><circle cx="{x+2*s}" cy="{y-1*s}" r=".9" fill="#e8892a"/><circle cx="{x+1*s}" cy="{y+1.2*s}" r=".8" fill="#e8892a"/>')
def p_stick(x, y, s=1, r=-12, c="#ef8a3c", d="#d96f22"):
    return (f'<g transform="rotate({r} {x} {y})"><rect x="{x-10*s}" y="{y-2.6*s}" width="{20*s}" height="{5.2*s}" rx="{2.4*s}" fill="{c}"/>'
            f'<rect x="{x-10*s}" y="{y+.6*s}" width="{20*s}" height="{2*s}" rx="1" fill="{d}" opacity=".6"/></g>')
def p_bar(x, y, s=1, r=0):
    return (f'<g transform="rotate({r} {x} {y})"><rect x="{x-9*s}" y="{y-3.5*s}" width="{18*s}" height="{7*s}" rx="{2*s}" fill="#d9a55a"/>'
            + "".join(f'<ellipse cx="{x+dx*s}" cy="{y+dy*s}" rx="1.4" ry=".8" fill="#f1d9a0"/>' for dx, dy in [(-5, -1), (-1, 1.5), (3, -1.5), (6, 1)]) + '</g>')
def p_muffin(x, y, s=1, top="#d9a55a", dots="#6db35a"):
    return (f'<path d="M{x-6*s} {y}h{12*s}l-{1.6*s} {7*s}h-{8.8*s}z" fill="#f2cf4a"/><path d="M{x-6*s} {y}h{12*s}" stroke="#d9a83a" stroke-width="1"/>'
            f'<path d="M{x-7*s} {y}a{7*s} {6*s} 0 0 1 {14*s} 0z" fill="{top}"/>'
            f'<circle cx="{x-2*s}" cy="{y-3*s}" r=".9" fill="{dots}"/><circle cx="{x+2.5*s}" cy="{y-2*s}" r=".9" fill="{dots}"/>')
def p_strip(x, y, s=1, r=0, c="#f2cf4a", dots="#6db35a"):
    return (f'<g transform="rotate({r} {x} {y})"><rect x="{x-11*s}" y="{y-3*s}" width="{22*s}" height="{6*s}" rx="{2*s}" fill="{c}"/>'
            f'<circle cx="{x-5*s}" cy="{y}" r="1" fill="{dots}"/><circle cx="{x+1*s}" cy="{y-1*s}" r="1" fill="{dots}"/><circle cx="{x+6*s}" cy="{y+1*s}" r="1" fill="{dots}"/></g>')
def p_toast(x, y, s=1, r=0, top=None):
    t = f'<rect x="{x-9*s}" y="{y-3*s}" width="{18*s}" height="{3.4*s}" rx="1.5" fill="{top}"/>' if top else ""
    return (f'<g transform="rotate({r} {x} {y})"><rect x="{x-10*s}" y="{y-3*s}" width="{20*s}" height="{6.5*s}" rx="{2*s}" fill="#d99a52"/>'
            f'<rect x="{x-9*s}" y="{y-2*s}" width="{18*s}" height="{4.5*s}" rx="1.5" fill="#f2d09a"/>{t}</g>')
def p_round(x, y, s=1, c="#6db35a", inner="#d7ecb5"):
    return f'<ellipse cx="{x}" cy="{y}" rx="{4.6*s}" ry="{2.6*s}" fill="{c}"/><ellipse cx="{x}" cy="{y-.3}" rx="{3.2*s}" ry="{1.7*s}" fill="{inner}"/>'
def p_grated(x, y, c="#9bcf6a", n=9, rng=None):
    rng = rng or random.Random(5)
    return "".join(f'<path d="M{x+rng.uniform(-10,10):.1f} {y+rng.uniform(-4,4):.1f}l{rng.uniform(-5,5):.1f} {rng.uniform(-2,2):.1f}" stroke="{c}" stroke-width="1.8" stroke-linecap="round"/>' for _ in range(n))
def p_cube(x, y, s=1, c="#f2cf4a"):
    return f'<rect x="{x-3*s}" y="{y-3*s}" width="{6*s}" height="{6*s}" rx="1.4" fill="{c}"/><rect x="{x-3*s}" y="{y-3*s}" width="{6*s}" height="{2*s}" rx="1" fill="#fff" opacity=".25"/>'
def p_dots(x, y, c, n=14, r=1.5, w=12, h=4, rng=None):
    rng = rng or random.Random(7)
    return "".join(f'<circle cx="{x+rng.uniform(-w,w):.1f}" cy="{y+rng.uniform(-h,h):.1f}" r="{r}" fill="{c}"/>' for _ in range(n))
def p_floret(x, y, s=1):
    return (f'<path d="M{x} {y+2*s}v{4*s}" stroke="#8fbf6a" stroke-width="{2.4*s}" stroke-linecap="round"/>'
            f'<circle cx="{x-2.6*s}" cy="{y}" r="{2.8*s}" fill="#3f8a4e"/><circle cx="{x+2.6*s}" cy="{y}" r="{2.8*s}" fill="#3f8a4e"/><circle cx="{x}" cy="{y-2.2*s}" r="{3*s}" fill="#4a9a5a"/>')
def p_flakes(x, y, c="#f4efe2", e="#e6dcc5", n=6, rng=None):
    rng = rng or random.Random(9)
    return "".join(f'<path d="M{x+dx:.1f} {y+dy:.1f}q3-3 6 0q-3 2-6 0z" fill="{c}" stroke="{e}" stroke-width=".7"/>' for dx, dy in [(rng.uniform(-12, 6), rng.uniform(-3, 3)) for _ in range(n)])
def p_fillet(x, y, s=1, c="#f08a5d"):
    return (f'<path d="M{x-12*s} {y}c4-6 20-6 24 0-4 5-20 5-24 0z" fill="{c}"/>'
            f'<path d="M{x-6*s} {y-3*s}q2 3 0 6M{x} {y-3.4*s}q2 3 0 7M{x+6*s} {y-3*s}q2 3 0 6" stroke="#ffd2bd" stroke-width="1" fill="none"/>')
def p_wedge(x, y, s=1, r=0, c="#e8d27a", skin="#d9483b"):
    return f'<g transform="rotate({r} {x} {y})"><path d="M{x-8*s} {y+3*s}q8-12 16 0z" fill="{c}"/><path d="M{x-8*s} {y+3*s}q8-12 16 0" stroke="{skin}" stroke-width="1.6" fill="none"/></g>'
def p_pop(x, y, s=1, c="#f2a2b1"):
    return (f'<rect x="{x-1.2*s}" y="{y+5*s}" width="{2.4*s}" height="{7*s}" rx="1" fill="#e2c08b"/>'
            f'<rect x="{x-5*s}" y="{y-8*s}" width="{10*s}" height="{14*s}" rx="{4.5*s}" fill="{c}"/><rect x="{x-3*s}" y="{y-6*s}" width="{2*s}" height="{8*s}" rx="1" fill="#fff" opacity=".4"/>')
def p_cake(x, y):
    return (f'<rect x="{x-20}" y="{y-10}" width="40" height="18" rx="4" fill="#d9a55a"/><rect x="{x-20}" y="{y-3}" width="40" height="3" fill="#f6c7cf"/>'
            f'<path d="M{x-21} {y-10}q5-6 10 0t10 0 10 0 10 0v-2h-40z" fill="#f6c7cf"/><ellipse cx="{x}" cy="{y-11}" rx="21" ry="3.4" fill="#f9d8de"/>'
            f'<path d="M{x-12} {y-14}q3-4 6 0z" fill="#e8475a"/><path d="M{x+2} {y-14}q3-4 6 0z" fill="#e8475a"/><circle cx="{x-3}" cy="{y-13}" r="1.6" fill="#5b6bc0"/><circle cx="{x+12}" cy="{y-13}" r="1.6" fill="#5b6bc0"/>'
            f'<rect x="{x-1}" y="{y-24}" width="2" height="10" rx="1" fill="#9fc7e6"/><path d="M{x} {y-28}q2 2 0 4q-2-2 0-4z" fill="#f2b630"/>')
def p_pasta(x, y, s=1, r=0, c="#f2c14e"):
    return f'<g transform="rotate({r} {x} {y})"><path d="M{x-5*s} {y}c0-4 4-4 5-1s5 3 5-1" stroke="{c}" stroke-width="{3.2*s}" fill="none" stroke-linecap="round"/></g>'
def p_steam(x, y):
    return f'<path d="M{x-8} {y}q-3-5 0-10M{x} {y-2}q-3-5 0-10M{x+8} {y}q-3-5 0-10" stroke="#cfc7ad" stroke-width="2" fill="none" stroke-linecap="round"/>'
def p_check(x, y):
    return f'<circle cx="{x}" cy="{y}" r="8" fill="{GREEN}"/><path d="M{x-4} {y}l3 3 5-6" stroke="#fff" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
def p_badge(x, y, t, c=TERRA):
    return (f'<circle cx="{x}" cy="{y}" r="11" fill="{c}"/><text x="{x}" y="{y+3.6}" text-anchor="middle" font-family="Montserrat,sans-serif" '
            f'font-weight="800" font-size="{9 if len(t) < 4 else 7.5}" fill="#fff">{t}</text>')
def p_arrow(x1, y1, x2, y2):
    return (f'<path d="M{x1} {y1}Q{(x1+x2)/2} {min(y1,y2)-10} {x2} {y2}" stroke="{TERRA}" stroke-width="2" fill="none" stroke-linecap="round" stroke-dasharray="3 4"/>'
            f'<circle cx="{x2}" cy="{y2}" r="2" fill="{TERRA}"/>')
def p_heat(x, y, n=3, gap=12):
    return "".join(f'<path d="M{x+(i-(n-1)/2)*gap} {y}c-3-3-2-7 1-9 0 3 3 4 3 7a3.6 3.6 0 0 1-4 2z" fill="#f08a3c"/><path d="M{x+(i-(n-1)/2)*gap+.6} {y-.6}c-1.4-1.4-1-3.4.4-4.4.2 1.6 1.6 2 1.4 3.6z" fill="#ffd27a"/>' for i in range(n))

# ---------------------------------------------------------------- recipientes
def bowl(content="", base="#f3e2b4", tool="whisk", side=()):
    clip = '<clipPath id="CL"><ellipse cx="54" cy="40" rx="37" ry="9.5"/></clipPath>'
    t = ""
    if tool == "whisk":
        t = (f'<path d="M66 42L84 8" stroke="#a7a7a7" stroke-width="3.4" stroke-linecap="round"/>'
             f'<path d="M66 42c-4-8 4-18 10-14M66 42c8-2 14-12 8-16M66 42c-2-10 10-16 10-14" stroke="#a7a7a7" stroke-width="1.6" fill="none"/>')
    elif tool == "spoon":
        t = f'<path d="M64 40L86 10" stroke="#c9962f" stroke-width="4" stroke-linecap="round"/><ellipse cx="62" cy="42" rx="5" ry="3" fill="#c9962f" transform="rotate(-50 62 42)"/>'
    elif tool == "fork":
        t = p_fork(62, 40, -150, 30)
    return (f'{clip}<ellipse cx="54" cy="78" rx="34" ry="4" fill="#000" opacity=".06"/>'
            f'<path d="M14 40h80a40 36 0 0 1-80 0z" fill="{TERRA}"/><path d="M22 52q10 14 30 16" stroke="#fff" stroke-width="2.4" fill="none" opacity=".25" stroke-linecap="round"/>'
            f'<ellipse cx="54" cy="40" rx="40" ry="11" fill="#b55a39"/><ellipse cx="54" cy="40" rx="37" ry="9.5" fill="{base}"/>'
            f'<g clip-path="url(#CL)">{content}</g>{t}' + _side(side))

def plate(content="", side=(), tool=None, steam=False):
    t = ""
    if tool == "fork":
        t = p_fork(74, 52, -148, 34)
    return (f'<ellipse cx="56" cy="62" rx="48" ry="17" fill="#000" opacity=".05"/><ellipse cx="56" cy="58" rx="48" ry="17" fill="#fff" stroke="{LINE}" stroke-width="2"/>'
            f'<ellipse cx="56" cy="57" rx="34" ry="11" fill="#f6f1e2"/>{content}{p_steam(56, 36) if steam else ""}{t}' + _side(side))

def pan(content="", side=(), heat=True):
    return (f'<path d="M92 48l24-9" stroke="#7a4a24" stroke-width="6" stroke-linecap="round"/><path d="M92 48l6-2" stroke="#3b3b3b" stroke-width="6" stroke-linecap="round"/>'
            f'<ellipse cx="52" cy="52" rx="42" ry="15" fill="#2f2f2f"/><ellipse cx="52" cy="50" rx="38" ry="12.5" fill="#4a4a4a"/>'
            f'<ellipse cx="44" cy="46" rx="14" ry="3" fill="#fff" opacity=".06"/>{content}{p_heat(52, 80) if heat else ""}' + _side(side))

def pot(color="#f2b630", content="", side=(), steam=True, lid=False):
    return (f'<path d="M20 34h68v30a12 12 0 0 1-12 12H32a12 12 0 0 1-12-12z" fill="{GREEN}"/><path d="M12 42h8M88 42h8" stroke="#3d7050" stroke-width="5" stroke-linecap="round"/>'
            f'<ellipse cx="54" cy="34" rx="36" ry="8" fill="#3d7050"/><ellipse cx="54" cy="34" rx="32.5" ry="6.5" fill="{color}"/>{content}'
            f'<path d="M30 52q8 10 24 12" stroke="#fff" stroke-width="2.4" fill="none" opacity=".2" stroke-linecap="round"/>'
            + (p_steam(54, 22) if steam else "") + _side(side))

def board(content="", side=(), knife=True):
    k = (f'<path d="M78 40l26-24" stroke="#dcdcdc" stroke-width="7" stroke-linecap="round"/><path d="M78 40l26-24" stroke="#fff" stroke-width="2" stroke-linecap="round" opacity=".6"/>'
         f'<path d="M104 16l9-8" stroke="#3b3b3b" stroke-width="5.6" stroke-linecap="round"/>') if knife else ""
    return (f'<rect x="6" y="42" width="96" height="34" rx="9" fill="#c99a68"/><rect x="6" y="40" width="96" height="32" rx="9" fill="#ddb383"/>'
            f'<circle cx="94" cy="50" r="2.4" fill="#b58757"/>{content}{k}' + _side(side, [(20, 20), (48, 20)]))

def oven(content="", temp=None):
    tb = p_badge(98, 14, f"{temp}°") if temp else ""
    return (f'<rect x="12" y="6" width="88" height="74" rx="9" fill="#efeadb" stroke="#cfc7ad" stroke-width="2"/>'
            f'<path d="M12 15a9 9 0 0 1 9-9h70a9 9 0 0 1 9 9v6H12z" fill="#ddd7c3"/><circle cx="22" cy="14" r="3" fill="{TERRA}"/><circle cx="31" cy="14" r="3" fill="#bdb59a"/><circle cx="40" cy="14" r="3" fill="#bdb59a"/>'
            f'<rect x="20" y="28" width="72" height="44" rx="6" fill="#3b2f2a"/><rect x="24" y="32" width="64" height="36" rx="4" fill="#f2a43a" opacity=".55"/>'
            f'<path d="M28 34h56" stroke="#ffd27a" stroke-width="2" opacity=".8"/><path d="M26 58h60" stroke="#8a8a8a" stroke-width="2.4"/>{content}'
            f'<path d="M30 26h52" stroke="{INK}" stroke-width="3" stroke-linecap="round" opacity=".35"/>{tb}')

def tray(content="", side=()):
    return (f'<g transform="translate(-11 -32) scale(1.2)"><rect x="8" y="50" width="96" height="16" rx="4" fill="#8a8a8a"/><rect x="10" y="48" width="92" height="14" rx="3" fill="#f4efe2"/>'
            f'<path d="M10 48h92" stroke="#bdbdbd" stroke-width="1.4"/>{content}</g>' + _side(side))

def blender(color="#f2cf4a", side=()):
    return (f'<path d="M34 10h40l-6 46H40z" fill="#e3f0f8" stroke="#9fc7e6" stroke-width="2"/><path d="M36.8 30h34.4l-3.4 26H40.2z" fill="{color}"/>'
            f'<path d="M40 36q14 6 28 0" stroke="#fff" stroke-width="1.6" fill="none" opacity=".5"/><rect x="32" y="5" width="44" height="7" rx="3.5" fill="#3b3b3b"/>'
            f'<rect x="30" y="56" width="48" height="20" rx="5" fill="#3b3b3b"/><circle cx="54" cy="66" r="4" fill="{TERRA}"/>'
            f'<path d="M48 48l12-4M48 44l12 4" stroke="#fff" stroke-width="1.6" opacity=".6"/>' + _side(side))

def mold(fill_color=None, items=None, n=6, side=()):
    cups = ""
    for i in range(n):
        cx = 22 + (i % 3) * 32 if n == 6 else 20 + i * 24
        cy = 40 if n != 6 or i < 3 else 60
        cups += f'<ellipse cx="{cx}" cy="{cy}" rx="11" ry="5" fill="#5a5a5a"/>'
        if fill_color: cups += f'<ellipse cx="{cx}" cy="{cy+.6}" rx="9" ry="3.6" fill="{fill_color}"/>'
        if items: cups += items(cx, cy - 2)
    h = 50 if n == 6 else 30
    y0 = 28
    return f'<rect x="4" y="{y0}" width="104" height="{h}" rx="7" fill="#7a7a7a"/>{cups}' + _side(side)

def colander(content="", side=(), water=True):
    w = "".join(f'<path d="M{x} {y}v6" stroke="#7ab0d9" stroke-width="2" stroke-linecap="round" stroke-dasharray="2 3"/>' for x, y in [(38, 4), (50, 2), (62, 4), (74, 3)]) if water else ""
    holes = "".join(f'<circle cx="{x}" cy="{y}" r="1.6" fill="#fff"/>' for x, y in [(32, 56), (44, 62), (56, 64), (68, 62), (80, 56), (38, 68), (52, 72), (66, 70)])
    return (f'{w}<path d="M16 40h80a40 34 0 0 1-80 0z" fill="#9fc7e6"/>{holes}<path d="M8 40h10M94 40h10" stroke="#5f97c4" stroke-width="5" stroke-linecap="round"/>'
            f'<ellipse cx="56" cy="40" rx="40" ry="10" fill="#7fb2db"/><ellipse cx="56" cy="40" rx="36" ry="8" fill="#e3f0f8"/>{content}' + _side(side))

def grater(content="", side=()):
    holes = "".join(f'<path d="M{x} {y}h5" stroke="#9a9a9a" stroke-width="2" stroke-linecap="round"/>' for y in (22, 30, 38, 46) for x in (30, 39, 48))
    return (f'<path d="M28 12h30l7 48H21z" fill="#e5e5e5" stroke="#a7a7a7" stroke-width="2"/>{holes}<rect x="34" y="2" width="18" height="12" rx="6" fill="none" stroke="#a7a7a7" stroke-width="3"/>'
            f'<ellipse cx="66" cy="72" rx="34" ry="7" fill="#fff" stroke="{LINE}" stroke-width="2"/>{content}' + _side(side))

def freezer(content=""):
    flake = "".join(f'<g transform="rotate({a} 96 20)"><path d="M96 8v24" stroke="#7ab0d9" stroke-width="2.6" stroke-linecap="round"/><path d="M92 11l4 4 4-4M92 29l4-4 4 4" stroke="#7ab0d9" stroke-width="2" fill="none" stroke-linecap="round"/></g>' for a in (0, 60, 120))
    return (f'<rect x="6" y="10" width="78" height="68" rx="8" fill="#e3f0f8" stroke="#9fc7e6" stroke-width="2"/><path d="M6 30h78" stroke="#9fc7e6" stroke-width="2"/>'
            f'<path d="M14 18h20" stroke="#9fc7e6" stroke-width="3" stroke-linecap="round"/>{content}{flake}')

def dish(content="", side=(), fill=None):
    f = f'<rect x="20" y="40" width="72" height="20" rx="4" fill="{fill}"/>' if fill else ""
    return (f'<rect x="12" y="38" width="88" height="30" rx="7" fill="#c96a47"/><rect x="16" y="36" width="80" height="26" rx="5" fill="#f4efe2"/>'
            f'<path d="M8 46h6M98 46h6" stroke="#a24f30" stroke-width="5" stroke-linecap="round"/>{f}{content}' + _side(side))
def p_omelette(x, y, rx=28, ry=8.5):
    return (f'<ellipse cx="{x}" cy="{y+1.6}" rx="{rx}" ry="{ry}" fill="#d9a83a"/><ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#f2cf4a"/>'
            + "".join(f'<circle cx="{x+dx}" cy="{y+dy}" r="1.6" fill="#6db35a"/>' for dx, dy in [(-14, -2), (-4, 2), (6, -3), (14, 2), (0, -5), (-20, 2), (19, -2)]))
def p_swirl(x, y, c="#fff"):
    return f'<path d="M{x-14} {y}q7-6 14 0t14 0" stroke="{c}" stroke-width="3" fill="none" stroke-linecap="round" opacity=".9"/>'
def p_dollop(x, y, c="#e7c08a"):
    return f'<path d="M{x-6} {y+2}q0-6 6-6 6 0 6 6z" fill="{c}"/><path d="M{x-2} {y-3}q2-3 4 0" stroke="#fff" stroke-width="1" fill="none" opacity=".6"/>'
def p_drum(x, y, s=1):
    return _ic("Pollo", x, y, 26 * s)
def p_window(items):
    """Cosas dentro del horno (sobre la bandeja)."""
    return items


def _side(items, pos=None):
    """Ingredientes enteros que esperan al lado (icono de la web)."""
    out = ""
    pos = pos or ([(104, 26), (104, 58)] if len(items) > 1 else [(104, 34)])
    for (n, (x, y)) in zip(items, pos):
        out += f'<circle cx="{x}" cy="{y}" r="15" fill="#fff" opacity=".9"/>' + (p_banana(x + 1, y, .55, -20) if n == "Plátano" else _ic(n, x, y, 26))
    return out

# ---------------------------------------------------------------- escenas de cada receta (una por paso)
R = random.Random
def _many(f, pts):
    return "".join(f(x, y, i) for i, (x, y) in enumerate(pts))

PAN5 = [(34, 49), (54, 46), (72, 50), (44, 55), (64, 55)]
PLATE5 = [(40, 56), (56, 53), (72, 57), (48, 61), (64, 61)]

ESC = {
"tortitas-platano-avena-bebe": [
    lambda: plate(p_mash(58, 58, "#f3d36b", 16) + p_banana(36, 53, .9, -8), tool="fork"),
    lambda: bowl(p_mash(46, 40, "#f3d36b", 18) + p_egg(60, 38) + p_oats(42, 41, 8), side=("Huevo", "Avena")),
    lambda: pan(p_oil(46, 48) + p_oil(62, 51)),
    lambda: pan(_many(lambda x, y, i: p_pancake(x, y, .85, cooked=i % 2 == 0), PAN5[:4])),
    lambda: plate(_many(lambda x, y, i: p_pancake(x, y - 5 * i, 1.5), [(56, 60)] * 4) + p_steam(56, 30)),
],
"barritas-avena-platano-horno-bebe": [
    lambda: oven(temp=180),
    lambda: bowl(p_mash(48, 40, "#f3d36b", 18) + p_oats(56, 40, 12) + p_dots(54, 40, "#a5612f", 6, 1), tool="fork", side=("Plátano", "Avena")),
    lambda: dish(p_oats(40, 50, 8, "#efdcae") + p_oats(66, 48, 8, "#efdcae"), fill="#e7c784"),
    lambda: oven(f'<rect x="32" y="48" width="48" height="10" rx="3" fill="#c98a33"/><rect x="34" y="46" width="44" height="8" rx="3" fill="#e0a64e"/>'),
    lambda: board(_many(lambda x, y, i: p_bar(x, y, 1.1, [-6, 4, -2, 6][i]), [(24, 52), (48, 56), (24, 64), (50, 66)])),
],
"hummus-sin-sal-bebe-tostada": [
    lambda: blender("#e8d2a0"),
    lambda: bowl(p_swirl(54, 40, "#f6ead0"), base="#e8d2a0", tool="spoon"),
    lambda: board(_many(lambda x, y, i: p_toast(x, y, 1.2, [-5, 4, -2][i]), [(28, 52), (54, 56), (34, 66)]), side=("Pan",)),
    lambda: plate(_many(lambda x, y, i: p_toast(x, y, 1.15, [-8, 6, -3][i], top="#e8d2a0"), [(42, 54), (70, 56), (56, 62)])),
],
"tortilla-calabacin-tiras-bebe": [
    lambda: grater(p_grated(66, 70, "#9bcf6a", 14), side=("Calabacín",)),
    lambda: bowl(p_grated(48, 40, "#6db35a", 12) + p_egg(64, 39), base="#f6d66a", side=("Huevo",)),
    lambda: pan(p_omelette(52, 48)),
    lambda: plate(p_omelette(56, 56, 26, 8) + p_check(92, 30)),
    lambda: board(_many(lambda x, y, i: p_strip(x, y, 1.15, [-4, 3, -2, 5][i]), [(28, 50), (54, 54), (30, 64), (58, 66)])),
],
"muffins-calabacin-manzana-bebe": [
    lambda: oven(temp=180),
    lambda: grater(p_grated(60, 70, "#9bcf6a", 9) + p_grated(74, 70, "#f1e3a6", 9), side=("Manzana", "Calabacín")),
    lambda: bowl(p_grated(46, 40, "#6db35a", 8) + p_grated(56, 41, "#f6eab8", 8) + p_egg(64, 38), base="#f6d66a", side=("Huevo",)),
    lambda: bowl(p_oats(48, 40, 10, "#f2e3b8") + p_dots(58, 40, "#a5612f", 8, 1) + p_grated(56, 40, "#6db35a", 6), base="#ecd394", tool="spoon", side=("Avena",)),
    lambda: oven(_many(lambda x, y, i: p_muffin(x, y, 1.1), [(38, 50), (56, 50), (74, 50)])),
    lambda: plate(_many(lambda x, y, i: p_muffin(x, y, 1.35), [(40, 54), (60, 50), (76, 56)])),
],
"pan-aguacate-huevo-bebe": [
    lambda: pot("#cfe5f2", '<ellipse cx="48" cy="34" rx="7" ry="5" fill="#fff"/><ellipse cx="62" cy="35" rx="7" ry="5" fill="#fbf7ee"/>', side=("Huevo",)),
    lambda: plate(p_mash(56, 56, "#9cc86a", 18) + p_dots(56, 56, "#7aa94f", 6, 1, 12, 3), tool="fork", side=("Aguacate",)),
    lambda: board(_many(lambda x, y, i: p_toast(x, y, 1.2, [-5, 4, -2][i]), [(28, 52), (54, 56), (34, 66)]), side=("Pan",)),
    lambda: plate(_many(lambda x, y, i: p_toast(x, y, 1.15, [-8, 6, -3][i], top="#9cc86a") + p_dots(x, y - 1.5, "#f2b630", 4, 1.1, 7, 1.2, R(i)), [(42, 54), (70, 56), (56, 62)])),
],
"crema-lentejas-rojas-calabaza-bebe": [
    lambda: colander(p_dots(56, 40, "#e8894a", 40, 1.8, 30, 6)),
    lambda: board(_many(lambda x, y, i: p_cube(x, y, 1.3, "#f2a43a"), [(20, 50), (30, 54), (24, 62), (38, 64)]) + _many(lambda x, y, i: p_round(x, y, 1.2, "#ef8a3c", "#f6b26b"), [(56, 52), (66, 60), (52, 64)]), side=("Calabaza", "Zanahoria")),
    lambda: pot("#f3e6c2", p_dots(54, 34, "#e9d39a", 14, 1.6, 22, 3), steam=False),
    lambda: pot("#f3c27a", p_dots(54, 34, "#e8894a", 26, 1.4, 26, 4) + _many(lambda x, y, i: p_cube(x, y, .9, "#f2a43a"), [(40, 34), (62, 33), (52, 36)])),
    lambda: pot("#ee9e4c", p_dots(54, 34, "#f7c27f", 8, 2, 22, 3)),
    lambda: blender("#f0a04b"),
],
"albondigas-ternera-calabacin-horno-bebe": [
    lambda: oven(temp=190),
    lambda: grater(p_grated(66, 70, "#9bcf6a", 14), side=("Calabacín",)),
    lambda: bowl(p_dots(50, 40, "#b5584a", 30, 2.2, 22, 5) + p_grated(52, 40, "#6db35a", 8) + p_egg(66, 38, .9) + p_oats(40, 41, 5), base="#c97a6a", tool="spoon", side=("Huevo", "Avena")),
    lambda: tray(_many(lambda x, y, i: p_ball(x, y, 1.1, "#c4675a", "#d98a7c"), [(22, 54), (38, 54), (54, 54), (70, 54), (86, 54)])),
    lambda: oven(_many(lambda x, y, i: p_ball(x, y, 1), [(36, 52), (50, 52), (64, 52), (78, 52)])),
    lambda: plate(_many(lambda x, y, i: p_ball(x, y, 1.3), [(44, 55), (58, 52), (70, 57), (52, 61)]) + p_check(94, 32)),
],
"nuggets-merluza-horno-bebe": [
    lambda: pot("#cfe5f2", _many(lambda x, y, i: p_cube(x, y, 1.2, "#f2e2a0"), [(42, 34), (54, 33), (66, 35), (48, 37)]), side=("Patata",)),
    lambda: pot("#e3f0f8", p_fillet(54, 33, .9, "#f4efe2"), side=("Merluza",)),
    lambda: bowl(p_mash(50, 40, "#f2e2a0", 20) + p_flakes(58, 40, n=7) + p_egg(66, 38, .8), tool="spoon", side=("Huevo",)),
    lambda: tray(_many(lambda x, y, i: p_nugget(x, y, 1, [-6, 4, -3, 5][i]), [(26, 54), (46, 55), (66, 54), (86, 55)])) + p_badge(98, 18, "200°"),
    lambda: oven(_many(lambda x, y, i: p_nugget(x, y, .9, [-6, 4, -3][i]), [(40, 52), (56, 52), (72, 52)])),
    lambda: plate(_many(lambda x, y, i: p_nugget(x, y, 1.25, [-10, 8, -4][i]), [(42, 55), (66, 55), (54, 61)]), steam=True),
],
"hamburguesitas-lentejas-bebe": [
    lambda: colander(p_dots(56, 40, "#8a5a3a", 40, 1.9, 30, 6)),
    lambda: grater(p_grated(66, 70, "#ef8a3c", 14), side=("Zanahoria",)),
    lambda: blender("#9a6a45", side=("Avena",)),
    lambda: bowl(p_grated(52, 40, "#ef8a3c", 12), base="#9a6a45", tool="spoon"),
    lambda: tray(_many(lambda x, y, i: p_patty(x, y, 1.2, "#9a6a45"), [(24, 54), (46, 55), (68, 54), (88, 55)])) + p_badge(98, 18, "190°"),
    lambda: oven(_many(lambda x, y, i: p_patty(x, y, 1), [(38, 52), (56, 52), (74, 52)])),
],
"crema-calabacin-pollo-bebe": [
    lambda: board(_many(lambda x, y, i: p_round(x, y, 1.3), [(22, 50), (34, 56), (22, 64)]) + _many(lambda x, y, i: p_cube(x, y, 1.3, "#f2e2a0"), [(50, 52), (58, 60)]) + _many(lambda x, y, i: p_round(x, y, 1.1, "#c5dca0", "#eef5e0"), [(72, 54), (66, 66)]), side=("Calabacín", "Patata")),
    lambda: pot("#cfe5f2", p_drum(50, 32, .9) + _many(lambda x, y, i: p_round(x, y, .8), [(66, 34), (38, 35)]), steam=False, side=("Pollo",)),
    lambda: pot("#e6efc9", p_drum(50, 32, .9) + _many(lambda x, y, i: p_round(x, y, .8), [(66, 34), (38, 35)]) + _many(lambda x, y, i: p_cube(x, y, .9, "#f2e2a0"), [(60, 36), (44, 37)])),
    lambda: plate(p_flakes(56, 56, "#ecc99a", "#d9ad78", 9), tool="fork"),
    lambda: blender("#a8cf6a"),
],
"bastones-boniato-horno-bebe": [
    lambda: oven(temp=200),
    lambda: board(_many(lambda x, y, i: p_stick(x, y, 1.2, [-6, 4, -2, 5][i], "#f6b26b", "#ef8a3c"), [(30, 50), (56, 54), (30, 64), (60, 66)]), side=("Boniato",)),
    lambda: bowl(_many(lambda x, y, i: p_stick(x, y, .9, [-20, 15, 0][i], "#f6b26b", "#ef8a3c"), [(44, 39), (58, 41), (52, 37)]) + p_dots(52, 40, "#c0392b", 8, 1), base="#f4e7c4", tool="spoon"),
    lambda: tray(_many(lambda x, y, i: p_stick(x, y, 1, [-4, 3, -2, 4, -3][i], "#f6b26b", "#ef8a3c"), [(20, 54), (40, 55), (60, 54), (80, 55), (96, 54)][:4])),
    lambda: oven(_many(lambda x, y, i: p_stick(x, y, .9, [-4, 3, -2][i]), [(38, 52), (56, 52), (74, 52)])),
    lambda: plate(_many(lambda x, y, i: p_stick(x, y, 1.2, [-10, 8, -3][i]), [(44, 55), (68, 55), (56, 61)]) + p_check(94, 32)),
],
"porridge-avena-pera-bebe": [
    lambda: pot("#e3f0f8", p_oats(54, 34, 14, "#efdcae"), steam=False, side=("Avena",)),
    lambda: pot("#ead6a6", p_oats(54, 34, 8, "#f4e6c0") + '<path d="M64 34L84 6" stroke="#c9962f" stroke-width="4" stroke-linecap="round"/>'),
    lambda: grater(p_grated(66, 70, "#e6e1a0", 14), side=("Pera",)),
    lambda: pot("#ead6a6", p_swirl(54, 34), steam=False),
    lambda: bowl(p_oats(48, 40, 8, "#f4e6c0") + p_grated(56, 40, "#dcd68a", 8) + p_dollop(62, 38), base="#ead6a6", tool="spoon"),
],
"pasta-bolonesa-lentejas-bebe": [
    lambda: board(_many(lambda x, y, i: p_cube(x, y, 1, ["#f2e6c4", "#ef8a3c"][i % 2]), [(22, 50), (28, 56), (36, 50), (24, 62), (34, 62), (42, 56), (46, 64), (16, 58)])),
    lambda: pan(p_oil(52, 48) + _many(lambda x, y, i: p_cube(x, y, .8, ["#f2e6c4", "#ef8a3c"][i % 2]), [(40, 47), (48, 50), (56, 46), (62, 50), (46, 44), (66, 46)])),
    lambda: pot("#d9483b", p_dots(54, 34, "#e8675a", 10, 1.4, 22, 3) + p_dots(54, 34, "#4a8760", 6, .9, 20, 3, R(2)), side=("Tomate",)),
    lambda: pot("#c9473a", p_dots(54, 34, "#7a4a2a", 26, 1.6, 26, 4)),
    lambda: pot("#cfe5f2", _many(lambda x, y, i: p_pasta(x, y, .9, [0, 40, -30, 70][i]), [(44, 34), (56, 33), (64, 35), (50, 36)])),
    lambda: plate(_many(lambda x, y, i: p_pasta(x, y, 1.2, [0, 40, -30, 70, 15][i]), [(46, 54), (58, 52), (68, 56), (52, 60), (62, 61)]) + p_dots(56, 56, "#d9483b", 18, 1.8, 16, 5), steam=True),
],
"mini-tortillas-horno-verduras-bebe": [
    lambda: oven(temp=180),
    lambda: bowl(p_dots(54, 40, "#6db35a", 8, 1, 24, 5) + p_egg(60, 39), base="#f6d66a", side=("Huevo",)),
    lambda: mold("#f2cf4a", lambda x, y: p_dots(x, y + 2, "#6db35a", 3, 1.2, 4, 1, R(int(x))) + p_dots(x, y + 2, "#e86f4a", 2, 1.2, 4, 1, R(int(x) + 1)), side=("Brócoli",)),
    lambda: oven(_many(lambda x, y, i: p_muffin(x, y, 1, "#f2cf4a", "#6db35a"), [(38, 50), (56, 50), (74, 50)])),
    lambda: plate(_many(lambda x, y, i: p_muffin(x, y, 1.35, "#f2cf4a", "#6db35a"), [(40, 54), (60, 50), (76, 56)])),
],
"arroz-meloso-pollo-verduras-bebe": [
    lambda: board(_many(lambda x, y, i: p_cube(x, y, 1, ["#e74c3c", "#ef8a3c", "#f2e6c4"][i % 3]), [(22, 50), (28, 56), (36, 50), (24, 62), (34, 62), (42, 56), (46, 64), (16, 58), (50, 52)]), side=("Pimiento rojo", "Zanahoria")),
    lambda: pan(_many(lambda x, y, i: p_cube(x, y, 1.1, "#f0d7b0"), [(40, 47), (54, 45), (64, 50)]) + _many(lambda x, y, i: p_cube(x, y, .7, ["#e74c3c", "#ef8a3c"][i % 2]), [(46, 51), (58, 51), (34, 50), (70, 46)]), side=("Pollo",)),
    lambda: pot("#f3e6c2", p_dots(54, 34, "#fff", 30, 1.3, 26, 4) + p_dots(54, 34, "#e74c3c", 5, 1.2, 22, 3, R(3)), steam=False, side=("Arroz",)),
    lambda: pot("#f2d27a", p_dots(54, 34, "#fff8e2", 26, 1.3, 26, 4) + p_dots(54, 34, "#e74c3c", 5, 1.2, 22, 3, R(3))),
    lambda: pot("#f2d27a", p_dots(54, 34, "#fff8e2", 20, 1.3, 26, 4) + p_dots(54, 34, "#6db35a", 12, 1.8, 22, 4, R(4)), side=("Guisantes",)),
    lambda: plate(f'<ellipse cx="56" cy="55" rx="24" ry="8" fill="#f2d27a"/>' + p_dots(56, 54, "#fff8e2", 20, 1.3, 18, 4) + p_dots(56, 54, "#6db35a", 8, 1.6, 16, 4, R(5)) + p_dots(56, 54, "#e74c3c", 5, 1.2, 16, 4, R(6)), steam=True),
],
"polos-yogur-fruta-bebe": [
    lambda: blender("#f2a2b1", side=("Fresas",)),
    lambda: tray(_many(lambda x, y, i: p_pop(x, y, 1.1), [(30, 36), (50, 36), (70, 36), (90, 36)])),
    lambda: freezer(_many(lambda x, y, i: p_pop(x, y, 1), [(24, 50), (44, 50), (64, 50)])),
    lambda: plate(p_pop(56, 44, 1.4)),
],
"salmon-horno-patata-brocoli-bebe": [
    lambda: oven(temp=200),
    lambda: board(_many(lambda x, y, i: p_wedge(x, y, 1.2, [-8, 6, -3][i], "#f2e2a0", "#c99a52"), [(24, 52), (40, 56), (26, 64)]) + _many(lambda x, y, i: p_floret(x, y, 1.3), [(58, 52), (66, 62), (50, 64)]), side=("Patata", "Brócoli")),
    lambda: tray(_many(lambda x, y, i: p_wedge(x, y, 1, [-8, 6, -3, 4][i], "#f2e2a0", "#c99a52"), [(20, 52), (36, 53), (82, 52), (96, 53)]) + _many(lambda x, y, i: p_floret(x, y, 1.1), [(52, 50), (66, 51)]) + p_oil(60, 56)),
    lambda: oven(p_fillet(56, 50, 1) + p_wedge(34, 50, .8, -6, "#f2e2a0", "#c99a52") + p_floret(78, 48, .9), side=("Merluza",)) if False else oven(p_fillet(56, 50, 1) + p_wedge(34, 50, .8, -6, "#f2e2a0", "#c99a52") + p_floret(78, 48, .9)),
    lambda: plate(p_flakes(56, 56, "#f6a27c", "#e08058", 10), tool="fork"),
    lambda: plate(_many(lambda x, y, i: p_wedge(x, y, 1.2, [-8, 6, -3][i], "#f2e2a0", "#c99a52"), [(40, 55), (56, 58), (46, 62)]) + _many(lambda x, y, i: p_floret(x, y, 1.3), [(70, 52), (76, 60)]) + p_check(96, 30)),
],
"bizcocho-manzana-sin-azucar-bebe": [
    lambda: oven(temp=180),
    lambda: board(p_grated(30, 56, "#f1e3a6", 14) + _many(lambda x, y, i: p_wedge(x, y, 1.1, [-10, 0, 10][i]), [(56, 54), (64, 60), (72, 54)]), side=("Manzana",)),
    lambda: bowl(p_mash(48, 40, "#f3d36b", 18) + p_egg(62, 38) + p_egg(52, 43, .8), tool="fork", side=("Plátano", "Huevo")),
    lambda: bowl(p_grated(48, 40, "#f6eab8", 8) + p_dots(56, 40, "#fff", 12, 1.6, 18, 4) + p_dots(60, 40, "#a5612f", 6, 1, 14, 3, R(8)), base="#ecd394", tool="spoon"),
    lambda: dish(_many(lambda x, y, i: p_wedge(x, y, 1.1, [-90, -90, -90, -90][i], "#f6eab8", "#d9483b"), [(30, 49), (46, 49), (62, 49), (78, 49)]), fill="#ecd394"),
    lambda: oven('<rect x="32" y="44" width="48" height="12" rx="4" fill="#c98a33"/><path d="M32 46q24-10 48 0v2H32z" fill="#e0a64e"/>' + _many(lambda x, y, i: f'<ellipse cx="{x}" cy="{y}" rx="4" ry="1.6" fill="#f6eab8"/>', [(40, 44), (52, 42), (64, 42), (74, 44)])),
],
"cuscus-verduras-garbanzos-bebe": [
    lambda: pan(_many(lambda x, y, i: p_cube(x, y, .9, ["#ef8a3c", "#6db35a", "#e74c3c"][i % 3]), [(36, 47), (44, 51), (52, 46), (58, 51), (64, 47), (48, 43), (70, 50), (40, 43), (56, 54)]), side=("Calabacín", "Pimiento rojo")),
    lambda: bowl(p_dots(54, 40, "#e2b84e", 30, 1.3, 30, 6) + p_steam(54, 22), base="#f2d27a"),
    lambda: bowl(p_dots(54, 40, "#e2b84e", 30, 1.3, 30, 6), base="#f6dc8a", tool="fork"),
    lambda: plate(_many(lambda x, y, i: f'<ellipse cx="{x}" cy="{y}" rx="5" ry="3" fill="#e2c08b"/><path d="M{x-3} {y-1}q3-2 6 0" stroke="#c9a06a" stroke-width="1" fill="none"/>', [(44, 55), (54, 52), (64, 55), (50, 60), (60, 60), (70, 59)]), tool="fork"),
    lambda: bowl(p_dots(54, 40, "#e2b84e", 22, 1.3, 30, 6) + _many(lambda x, y, i: p_cube(x, y, .8, ["#ef8a3c", "#6db35a", "#e74c3c"][i % 3]), [(40, 39), (48, 42), (58, 38), (66, 41), (52, 36)]) + _many(lambda x, y, i: f'<ellipse cx="{x}" cy="{y}" rx="3.4" ry="2.2" fill="#e2c08b"/>', [(44, 37), (62, 43), (70, 37)]), base="#f2d27a", tool="spoon"),
],
"manzana-pera-asadas-canela-bebe": [
    lambda: oven(temp=180),
    lambda: board(_many(lambda x, y, i: p_wedge(x, y, 1.3, [-10, 6, -4, 8][i], ["#f6eab8", "#eef0b8"][i % 2], ["#d9483b", "#a8c54a"][i % 2]), [(24, 52), (44, 56), (28, 64), (52, 66)]), side=("Manzana", "Pera")),
    lambda: dish(_many(lambda x, y, i: p_wedge(x, y, 1.1, [-6, 6, -4, 4, 0][i], ["#f6eab8", "#eef0b8"][i % 2], ["#d9483b", "#a8c54a"][i % 2]), [(26, 48), (40, 50), (54, 48), (68, 50), (82, 48)]) + p_dots(54, 48, "#a5612f", 10, 1, 30, 3)),
    lambda: oven(_many(lambda x, y, i: p_wedge(x, y, .9, [-6, 6, -4, 4][i], ["#f0d68a", "#e3e39a"][i % 2], ["#b5403a", "#93ad3e"][i % 2]), [(38, 50), (50, 51), (62, 50), (74, 51)])),
    lambda: plate(_many(lambda x, y, i: p_wedge(x, y, 1.3, [-10, 8, -3][i], ["#f0d68a", "#e3e39a"][i % 2], ["#b5403a", "#93ad3e"][i % 2]), [(42, 55), (66, 55), (54, 60)]), steam=True),
],
"tarta-primer-cumpleanos-sin-azucar": [
    lambda: colander('<path d="M30 40q26 10 52 0" fill="#fff" stroke="#e6e1d0"/><ellipse cx="56" cy="39" rx="26" ry="5" fill="#fbf8f0"/>', water=False),
    lambda: oven(temp=180),
    lambda: bowl(p_mash(46, 40, "#f3d36b", 16) + p_egg(62, 38) + p_grated(52, 42, "#ef8a3c", 9), side=("Plátano", "Zanahoria")),
    lambda: bowl(p_grated(48, 40, "#ef8a3c", 6) + p_dots(56, 40, "#fff", 12, 1.6, 18, 4) + p_dots(60, 40, "#a5612f", 6, 1, 14, 3, R(8)), base="#ecc684", tool="spoon"),
    lambda: oven('<ellipse cx="56" cy="54" rx="22" ry="5" fill="#a87028"/><rect x="34" y="44" width="44" height="10" fill="#c98a33"/><ellipse cx="56" cy="44" rx="22" ry="5" fill="#e0a64e"/>'),
    lambda: bowl(p_swirl(48, 40, "#fff") + _many(lambda x, y, i: '<path d="M%s %sq3-4 6 0q-3 3-6 0z" fill="#e8475a"/>' % (x, y), [(56, 38), (64, 41), (44, 42)]), base="#f6c7cf", tool="spoon", side=("Fresas",)),
    lambda: plate(p_cake(56, 52)),
],
}

def escena(slug, k):
    fs = ESC.get(slug)
    if not fs or k >= len(fs): return None
    uid = f"CL{zlib.crc32(f'{slug}{k}'.encode())}"
    return f'<svg class="sc" viewBox="0 0 120 84" aria-hidden="true">{fs[k]()}</svg>'.replace('id="CL"', f'id="{uid}"').replace("url(#CL)", f"url(#{uid})")
