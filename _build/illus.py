# Ilustraciones de los artículos del blog.
# Cada una es HTML + SVG en línea, en el estilo plano de la web.
# En el cuerpo de un artículo se colocan con <!--il:nombre--> y build_site.py las sustituye.
import json, os

_D = os.path.dirname(os.path.abspath(__file__))
_F = {}
for _n in ("foods2.json", "extra.json", "pdfic.json"):
    _F.update(json.load(open(os.path.join(_D, _n))))
food = lambda n: _F[n]

SKIN = "#f3c7a1"; HAIR = "#8a5a2d"; INK = "#262626"; GREEN = "#4a8760"; TERRA = "#c96a47"; GOLD = "#c9962f"; CARD = "#f7f4e8"

def _face(cx, cy, r=13, mouth="smile", fill=SKIN, look=0):
    """Cara de bebé. mouth: smile | o | open | cough | flat"""
    ex = r * .38
    eyes = f'<circle cx="{cx-ex+look}" cy="{cy-1}" r="1.7" fill="{INK}"/><circle cx="{cx+ex+look}" cy="{cy-1}" r="1.7" fill="{INK}"/>'
    m = {
        "smile": f'<path d="M{cx-4} {cy+4.5}q4 3.5 8 0" fill="none" stroke="{INK}" stroke-width="1.8" stroke-linecap="round"/>',
        "o": f'<ellipse cx="{cx+look/2}" cy="{cy+5.5}" rx="2.6" ry="3" fill="{INK}"/>',
        "open": f'<ellipse cx="{cx}" cy="{cy+5.5}" rx="3.6" ry="3.4" fill="#8f3b2c"/>',
        "cough": f'<ellipse cx="{cx}" cy="{cy+5.5}" rx="3.2" ry="2.6" fill="#8f3b2c"/>',
        "flat": f'<path d="M{cx-3} {cy+6}h6" stroke="{INK}" stroke-width="1.8" stroke-linecap="round"/>',
    }[mouth]
    cheeks = f'<circle cx="{cx-r*.6}" cy="{cy+3}" r="2.4" fill="#e88f7a" opacity=".45"/><circle cx="{cx+r*.6}" cy="{cy+3}" r="2.4" fill="#e88f7a" opacity=".45"/>'
    hair = f'<path d="M{cx-2} {cy-r+1}c-1-4 3-6 5-3" fill="none" stroke="{HAIR}" stroke-width="2.2" stroke-linecap="round"/>'
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>{cheeks}{eyes}{m}{hair}'

def _svg(body, vb="0 0 64 64", cls="pic"):
    return f'<svg class="{cls}" viewBox="{vb}" aria-hidden="true">{body}</svg>'

def _figure(inner, caption, label, extra_cls=""):
    cap = f'<figcaption>{caption}</figcaption>' if caption else ""
    return f'<figure class="il {extra_cls}" role="img" aria-label="{label}">{inner}{cap}</figure>'

# ---------- Artículo: cuándo empezar ----------

def edad():
    stops = [
        ("0", "", ""),
        ("4 m", "Nunca antes", "bad"),
        ("6 m", "Hacia aquí", "good"),
        ("+6 m", "No retrasarlo mucho: baja el hierro", "warn"),
    ]
    star = _svg('<polygon points="12,1.5 14.9,8.4 22.4,9.1 16.7,14 18.4,21.4 12,17.5 5.6,21.4 7.3,14 1.6,9.1 9.1,8.4" fill="#fff"/>', "0 0 24 24", "st")
    li = "".join(
        f'<li class="{c}"><span class="dot">{star if c=="good" else ""}</span><b>{m}</b><span>{t}</span></li>'
        for m, t, c in stops)
    return _figure(f'<ol class="tl">{li}</ol>', None,
                   "Línea de tiempo: nunca antes de los 4 meses, hacia los 6 meses es lo recomendado, y no retrasarlo mucho más.")

def senales():
    # 1. Sentado en la trona
    s1 = (f'<path d="M14 58V30a6 6 0 0 1 6-6h24a6 6 0 0 1 6 6v28" fill="none" stroke="{TERRA}" stroke-width="4" stroke-linecap="round"/>'
          f'<rect x="10" y="44" width="44" height="6" rx="3" fill="{TERRA}"/>'
          f'<path d="M22 44V36a10 10 0 0 1 20 0v8z" fill="{GREEN}"/>'
          f'<path d="M20 38c-3 2-4 5-3 7M44 38c3 2 4 5 3 7" stroke="{SKIN}" stroke-width="3.4" fill="none" stroke-linecap="round"/>'
          + _face(32, 18, 11))
    # 2. Mira vuestra comida
    s2 = (_face(22, 30, 13, "o", look=2.4)
          + f'<ellipse cx="50" cy="44" rx="11" ry="4" fill="#fff" stroke="#d8d3bc" stroke-width="1.5"/>'
          + f'<g transform="translate(40 26) scale(.42)">{food("Brócoli")}</g>'
          + f'<path d="M38 12l3-4M44 16l4-2M34 10l0-5" stroke="{GOLD}" stroke-width="2.2" stroke-linecap="round"/>')
    # 3. Coge cosas y se las lleva a la boca
    s3 = (_face(26, 30, 13, "open")
          + f'<g transform="translate(30 12) rotate(25) scale(.55)">{food("Plátano")}</g>'
          + f'<circle cx="44" cy="40" r="6.5" fill="{SKIN}"/><path d="M39 36q-2-4 1-6M42 34q-1-4 2-5" stroke="{SKIN}" stroke-width="3.2" fill="none" stroke-linecap="round"/>')
    # 4. Ya no empuja con la lengua
    s4 = (_face(24, 32, 13, "open")
          + f'<path d="M36 37l20-10" stroke="{GOLD}" stroke-width="3.4" stroke-linecap="round"/>'
          + f'<ellipse cx="35" cy="37.5" rx="5" ry="3.4" fill="{GOLD}" transform="rotate(-26 35 37.5)"/>'
          + f'<circle cx="34.5" cy="37" r="2" fill="#f2cf4a"/>'
          + f'<circle cx="50" cy="12" r="8" fill="{GREEN}"/><path d="M46 12l3 3 5-6" stroke="#fff" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    items = [(s1, "Se sienta con poco apoyo"), (s2, "Le interesa lo que coméis"),
             (s3, "Coge cosas y se las lleva a la boca"), (s4, "Ya no empuja la comida con la lengua")]
    li = "".join(f'<li><span class="n">{i}</span>{_svg(s)}<span>{t}</span></li>' for i, (s, t) in enumerate(items, 1))
    return _figure(f'<ul class="tiles">{li}</ul>', None, "Las 4 señales de que está listo, ilustradas.")

def leche():
    bottle = _svg(
        f'<rect x="22" y="4" width="20" height="8" rx="3" fill="{GOLD}"/>'
        f'<path d="M27 4c0-3 10-3 10 0" fill="#e7b85e"/>'
        f'<rect x="19" y="11" width="26" height="6" rx="2" fill="{TERRA}"/>'
        f'<rect x="17" y="17" width="30" height="44" rx="10" fill="#fff" stroke="#d8d3bc" stroke-width="2"/>'
        f'<path d="M19 30h26v21a8 8 0 0 1-8 8H27a8 8 0 0 1-8-8z" fill="#fbf3dc"/>'
        f'<path d="M37 24v4M37 34v4M37 44v4" stroke="#d8d3bc" stroke-width="2" stroke-linecap="round"/>', cls="pic big")
    bowl = _svg(
        f'<path d="M14 36h36a18 18 0 0 1-36 0z" fill="{GREEN}"/>'
        f'<ellipse cx="32" cy="36" rx="18" ry="4" fill="#f2b630"/>'
        f'<path d="M40 30l10-16" stroke="{GOLD}" stroke-width="3" stroke-linecap="round"/>', cls="pic sm")
    inner = (f'<div class="vs"><div class="side main">{bottle}<b>Leche materna o de fórmula</b><span>Su alimento principal hasta el año, a demanda</span></div>'
             f'<div class="plus">+</div>'
             f'<div class="side">{bowl}<b>La comida</b><span>Complementa. Al principio, muy poquito</span></div></div>')
    return _figure(inner, None, "Hasta el año la leche es lo principal y la comida complementa.")

def plato():
    core = "".join(f'<span>{food(n)}<i>{t}</i></span>' for n, t in [("Pollo", "Carne"), ("Merluza", "Pescado"), ("Huevo", "Huevo"), ("Lentejas", "Legumbres")])
    ring = "".join(f'<span>{food(n)}<i>{t}</i></span>' for n, t in [("Brócoli", "Verdura"), ("Calabaza", "Verdura"), ("Pera", "Fruta"), ("Avena", "Cereales")])
    inner = (f'<div class="plate"><div class="core"><b>Casi a diario: hierro y zinc</b><div class="ics">{core}</div></div>'
             f'<div class="ring"><b>Alrededor</b><div class="ics">{ring}</div></div></div>')
    return _figure(inner, "Bien cocinados, y los cereales mejor integrales.",
                   "Plato: en el centro, alimentos ricos en hierro y zinc casi a diario; alrededor, verdura, fruta y cereales.")

# ---------- Artículo: arcada o atragantamiento ----------

def arcada_vs():
    cough = _svg(_face(28, 34, 16, "cough")
                 + f'<path d="M48 26q4 4 0 8M52 22q7 8 0 16" stroke="{GREEN}" stroke-width="2.6" fill="none" stroke-linecap="round"/>'
                 + f'<path d="M20 31l3 1M33 31l3 1" stroke="#7ab0d9" stroke-width="2"/><circle cx="17" cy="38" r="2" fill="#7ab0d9"/>', cls="pic big")
    choke = _svg(_face(30, 34, 16, "flat", fill="#c7b3e6")
                 + f'<path d="M50 22l8 8M58 22l-8 8" stroke="{TERRA}" stroke-width="3" stroke-linecap="round"/>', cls="pic big")
    col = lambda cls, pic, h, items, act: (
        f'<div class="col {cls}">{pic}<b class="h">{h}</b><ul>' + "".join(f"<li>{x}</li>" for x in items) + f'</ul><p class="act">{act}</p></div>')
    inner = ('<div class="cmp">'
             + col("ok", cough, "Arcada", ["Tose y hace ruido", "Ojos llorosos", "Echa la comida hacia delante"], "Calma. Déjale toser")
             + col("ko", choke, "Atragantamiento", ["No tose, no llora, no respira", "Se pone morado", "Ruido agudo o silencio"], "Actúa ya y llama al 112")
             + '</div>')
    return _figure(inner, None, "Comparación: la arcada tiene tos y ruido; en el atragantamiento no tose ni respira.")

def pasos():
    phone = _svg(f'<rect x="18" y="6" width="28" height="52" rx="7" fill="{INK}"/><rect x="21" y="12" width="22" height="38" rx="3" fill="#fff"/>'
                 f'<text x="32" y="36" text-anchor="middle" font-family="Montserrat,sans-serif" font-weight="800" font-size="11" fill="{TERRA}">112</text>')
    # Boca abajo sobre el antebrazo, cabeza más baja: golpes en la espalda
    back = _svg(f'<path d="M6 28l50 14" stroke="{SKIN}" stroke-width="7" stroke-linecap="round"/>'
                f'<path d="M14 24c4-6 26-2 32 6l-2 6c-10-2-22-4-28-6z" fill="{GREEN}"/>'
                + _face(52, 40, 8, "flat")
                + f'<path d="M26 4l2 10M32 6l-1 9M20 8l4 8" stroke="{TERRA}" stroke-width="2.4" stroke-linecap="round"/>'
                f'<ellipse cx="28" cy="18" rx="7" ry="4" fill="#e9b48f" transform="rotate(12 28 18)"/>')
    # Boca arriba: dos dedos en el centro del pecho
    chest = _svg(f'<rect x="8" y="46" width="50" height="5" rx="2.5" fill="#d8d3bc"/>'
                 f'<path d="M18 46c0-10 6-14 14-14s16 4 16 14z" fill="{GREEN}"/>'
                 + _face(12, 38, 8, "flat")
                 + f'<rect x="29" y="12" width="4.5" height="20" rx="2.2" fill="#e9b48f"/><rect x="34.5" y="10" width="4.5" height="22" rx="2.2" fill="#e9b48f"/>'
                 f'<path d="M24 20l4 4M44 20l-4 4" stroke="{TERRA}" stroke-width="2.4" stroke-linecap="round"/>')
    rep = _svg(f'<path d="M48 26a17 17 0 1 0-2 14" fill="none" stroke="{GREEN}" stroke-width="5" stroke-linecap="round"/>'
               f'<path d="M50 14v13H37" fill="none" stroke="{GREEN}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')
    steps = [(phone, "Llama al 112"), (back, "5 golpes en la espalda"), (chest, "5 compresiones en el pecho"), (rep, "Repite hasta que lo expulse")]
    li = "".join(f'<li><span class="n">{i}</span>{s}<span>{t}</span></li>' for i, (s, t) in enumerate(steps, 1))
    return _figure(f'<ol class="tiles steps">{li}</ol>', "Si pierde el conocimiento, empieza la reanimación (RCP).",
                   "Pasos si se atraganta un menor de 1 año: llamar al 112, 5 golpes en la espalda, 5 compresiones en el pecho y repetir.")

def cortes():
    no = f'<circle cx="54" cy="10" r="8" fill="{TERRA}"/><path d="M50.5 6.5l7 7M57.5 6.5l-7 7" stroke="#fff" stroke-width="2.2" stroke-linecap="round"/>'
    yes = f'<circle cx="54" cy="10" r="8" fill="{GREEN}"/><path d="M50 10l3 3 5-6" stroke="#fff" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    grape = lambda c: f'<ellipse cx="30" cy="36" rx="13" ry="16" fill="{c}"/><path d="M24 28c2-4 5-5 8-5" stroke="#fff" stroke-width="2" opacity=".5" fill="none" stroke-linecap="round"/>'
    quarters = lambda c: "".join(
        f'<path d="M{x} 20c{d*9} 2 {d*9} 30 0 32z" fill="{c}"/>' for x, d in [(16, -1), (25, 1), (39, -1), (48, 1)])
    almond = f'<ellipse cx="30" cy="36" rx="10" ry="15" fill="#b98a5b" transform="rotate(20 30 36)"/><path d="M26 26c2 8 2 16 6 22" stroke="#9a6d43" stroke-width="1.6" fill="none"/>'
    jar = (f'<rect x="16" y="22" width="28" height="32" rx="6" fill="#d9b48a"/><rect x="14" y="16" width="32" height="8" rx="3" fill="{TERRA}"/>'
           f'<path d="M20 36q10-6 20 0v12a4 4 0 0 1-4 4H24a4 4 0 0 1-4-4z" fill="#c69663"/>')
    apple_hard = f'<g transform="translate(6 12) scale(.9)">{food("Manzana")}</g>'
    grated = (f'<path d="M10 52c6-8 12-8 18-2s12 6 18 0" fill="none" stroke="#e8d27a" stroke-width="0"/>'
              + "".join(f'<path d="M{x} {y}l{l} -3" stroke="#f3e2a0" stroke-width="3" stroke-linecap="round"/>'
                        for x, y, l in [(12, 50, 9), (20, 46, 8), (28, 52, 9), (18, 40, 7), (34, 44, 8), (26, 38, 8), (38, 50, 7), (30, 30, 6)])
              + f'<ellipse cx="28" cy="52" rx="20" ry="4" fill="#fff" opacity=".0"/>')
    rows = [
        ("Uvas, tomates cherry y arándanos", grape("#8a5ac8") + no, quarters("#8a5ac8") + yes, "En cuartos a lo largo"),
        ("Frutos secos", almond + no, jar + yes, "En crema o molidos muy finos, hasta los 5 años"),
        ("Manzana y zanahoria", apple_hard + no, grated + yes, "Cocinadas hasta que estén blandas, o ralladas muy finas"),
    ]
    li = "".join(f'<li><b>{t}</b><div class="pair">{_svg(a)}<span class="ar">→</span>{_svg(b)}</div><span>{d}</span></li>' for t, a, b, d in rows)
    return _figure(f'<ul class="cuts">{li}</ul>', None, "Cómo ofrecer uvas, frutos secos y manzana o zanahoria de forma segura.")

IL = {"edad": edad, "senales": senales, "leche": leche, "plato": plato,
      "arcada_vs": arcada_vs, "pasos": pasos, "cortes": cortes}

def apply(body):
    for k, f in IL.items():
        body = body.replace(f"<!--il:{k}-->", f())
    return body

CSS = r"""
/* ilustraciones */
figure.il{margin:30px 0 34px;padding:22px;border-radius:24px;background:var(--card);border:1.5px solid var(--line)}
figure.il figcaption{margin:14px 0 0;color:var(--mute);font-size:.85rem;text-align:center}
figure.il ul,figure.il ol{list-style:none;padding:0;margin:0}figure.il li{margin:0}
figure.il svg.fd{overflow:visible}
.il .pic{display:block;width:72px;height:72px;margin:0 auto 10px;overflow:visible}
.il .pic.big{width:96px;height:96px}.il .pic.sm{width:60px;height:60px}
.il .n{position:absolute;top:10px;left:12px;width:24px;height:24px;border-radius:50%;background:var(--terra);color:#fff;font:800 .8rem/24px Montserrat,sans-serif;text-align:center}
.tl{display:grid;grid-template-columns:repeat(4,1fr);position:relative;padding-top:4px}
.tl::before{content:"";position:absolute;left:12.5%;right:12.5%;top:17px;height:6px;border-radius:3px;background:linear-gradient(90deg,#d9cdb8 0 33%,var(--terra) 33% 34%,#e9c98a 34% 66%,var(--green) 66%)}
.tl li{position:relative;display:flex;flex-direction:column;align-items:center;text-align:center;gap:4px;font-size:.85rem;line-height:1.35;color:var(--mute);padding:0 4px}
.tl .dot{width:32px;height:32px;border-radius:50%;background:#fff;border:3px solid #d9cdb8;display:grid;place-items:center;margin-bottom:6px}
.tl .bad .dot{border-color:var(--terra)}.tl .warn .dot{border-color:var(--gold)}
.tl .good .dot{width:44px;height:44px;margin-top:-6px;background:var(--green);border-color:var(--green)}
.tl .st{width:22px;height:22px}
.tl b{color:var(--ink);font-size:1rem}.tl .bad span{color:var(--terra);font-weight:700}.tl .good span{color:var(--green);font-weight:700}
.tiles{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.tiles li{position:relative;background:#fff;border-radius:18px;padding:22px 10px 16px;text-align:center;font-weight:700;font-size:.85rem;line-height:1.35}
.vs{display:flex;align-items:center;justify-content:center;gap:16px}
.vs .side{flex:1;text-align:center;display:flex;flex-direction:column;align-items:center;gap:4px}
.vs .side span{color:var(--mute);font-size:.88rem;line-height:1.4;max-width:15em}
.vs .side.main b{color:var(--green)}
.vs .plus{font:400 2rem "Luckiest Guy",sans-serif;color:var(--terra)}
.plate{display:grid;grid-template-columns:1.2fr 1fr;gap:12px}
.plate>div{border-radius:20px;padding:16px;text-align:center}
.plate .core{background:#fff;border:2.5px solid var(--green)}.plate .ring{background:#fff}
.plate b{display:block;margin:0 0 10px;font-size:.92rem}.plate .core b{color:var(--green)}
.plate .ics{display:grid;grid-template-columns:repeat(2,1fr);gap:8px}
.plate .ics span{display:flex;flex-direction:column;align-items:center;gap:2px;font-size:.78rem;color:var(--mute);font-weight:600}
.plate .ics svg{width:44px;height:44px}.plate .ics i{font-style:normal}
.cmp{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.cmp .col{background:#fff;border-radius:20px;padding:18px 16px;border-top:6px solid var(--green)}
.cmp .ko{border-top-color:var(--terra)}
.cmp .h{display:block;text-align:center;font-size:1.05rem;margin:0 0 8px;color:var(--green)}.cmp .ko .h{color:var(--terra)}
.cmp ul li{font-size:.88rem;line-height:1.4;padding:5px 0 5px 18px;position:relative}
.cmp ul li::before{content:"";position:absolute;left:2px;top:12px;width:7px;height:7px;border-radius:50%;background:var(--green)}
.cmp .ko ul li::before{background:var(--terra)}
.cmp .act{margin:12px 0 0;padding:8px 10px;border-radius:12px;background:#e6efe6;color:var(--green);font-weight:800;font-size:.88rem;text-align:center}
.cmp .ko .act{background:#f6e1d8;color:#a24f30}
.cuts{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.cuts li{background:#fff;border-radius:18px;padding:16px 10px;text-align:center;display:flex;flex-direction:column;gap:6px}
.cuts b{font-size:.88rem;line-height:1.3}.cuts li>span{color:var(--mute);font-size:.8rem;line-height:1.35}
.cuts .pair{display:flex;align-items:center;justify-content:center;gap:2px}
.cuts .pair svg{width:56px;height:56px;margin:0}.cuts .ar{color:var(--mute);font-weight:800}
@media(max-width:640px){
figure.il{padding:16px;margin:24px -6px 28px}
.tiles{grid-template-columns:repeat(2,1fr)}
.cuts{grid-template-columns:1fr}.cuts li{display:grid;grid-template-columns:1fr auto;grid-template-areas:"t p" "d p";text-align:left;align-items:center;column-gap:8px;padding:12px 14px}
.cuts b{grid-area:t}.cuts li>span{grid-area:d}.cuts .pair{grid-area:p}
.plate{grid-template-columns:1fr}.plate .ics{grid-template-columns:repeat(4,1fr)}
.cmp{grid-template-columns:1fr}
.tl li{font-size:.75rem}.tl b{font-size:.9rem}
.vs{gap:8px}.vs .pic.big{width:76px;height:76px}
}
"""
