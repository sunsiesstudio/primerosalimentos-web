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
    x = f'<circle cx="54" cy="10" r="8" fill="{TERRA}"/><path d="M50.5 6.5l7 7M57.5 6.5l-7 7" stroke="#fff" stroke-width="2.2" stroke-linecap="round"/>'
    star = f'<circle cx="54" cy="10" r="9" fill="{GREEN}"/><polygon transform="translate(46.5 2.5) scale(.62)" points="12,1.5 14.9,8.4 22.4,9.1 16.7,14 18.4,21.4 12,17.5 5.6,21.4 7.3,14 1.6,9.1 9.1,8.4" fill="#fff"/>'
    clock = (f'<circle cx="52" cy="40" r="10" fill="#fff" stroke="{GOLD}" stroke-width="3"/>'
             f'<path d="M52 34v6l4 3" stroke="{GOLD}" stroke-width="2.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    bottle = (f'<rect x="43" y="30" width="12" height="24" rx="5" fill="#fff" stroke="#d8d3bc" stroke-width="1.8"/>'
              f'<rect x="43.9" y="40" width="10.2" height="13" rx="4" fill="#fbf3dc"/>'
              f'<rect x="44" y="25" width="10" height="5" rx="1.5" fill="{TERRA}"/><path d="M46 25c0-4 6-4 6 0" fill="{GOLD}"/>')
    p1 = _svg(_face(26, 38, 12, "o") + bottle + x)
    p2 = _svg(_face(25, 36, 15) + f'<g transform="translate(36 34) scale(.5)">{food("Plátano")}</g>'
              f'<g transform="translate(2 44) scale(.42)">{food("Brócoli")}</g>' + star)
    p3 = _svg(_face(26, 36, 16) + clock)
    items = [("", p1, "Antes de los 4 meses", "Nunca antes", "Solo leche"),
             ("on", p2, "Hacia los 6 meses", "El momento recomendado", "Si ya muestra las señales"),
             ("", p3, "Más allá de los 6", "No lo retrases mucho", "Sus reservas de hierro empiezan a bajar")]
    li = "".join(f'<li class="{c}">{pic}<span class="m">{m}</span><b>{h}</b><span>{d}</span></li>' for c, pic, m, h, d in items)
    return _figure(f'<ol class="ages">{li}</ol>', None,
                   "Cuándo empezar: nunca antes de los 4 meses, hacia los 6 meses es lo recomendado, y no conviene retrasarlo mucho más.")

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
    s3 = (_face(22, 36, 14, "o")
          + f'<path d="M44 22L31 41" stroke="{GOLD}" stroke-width="4.5" stroke-linecap="round"/>'
          + f'<circle cx="30" cy="42.5" r="4" fill="none" stroke="{GREEN}" stroke-width="3"/>'
          + f'<circle cx="49" cy="15" r="10" fill="{TERRA}"/><path d="M40 13a9 9 0 0 1 18 0" fill="none" stroke="#fff" stroke-width="2.4" opacity=".9"/>'
          + f'<circle cx="45" cy="18" r="1.8" fill="#fff"/><circle cx="52" cy="20" r="1.8" fill="#fff"/><circle cx="49" cy="9" r="1.6" fill="#fff" opacity=".8"/>'
          + f'<path d="M58 26l4 2M56 30l3 4M60 18h4" stroke="{GOLD}" stroke-width="2" stroke-linecap="round"/>'
          + f'<ellipse cx="38" cy="32" rx="6" ry="5.2" fill="{SKIN}"/><path d="M34 29.5h7M34.5 32.5h7" stroke="#e0a983" stroke-width="1.2" stroke-linecap="round"/>')
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
        f'<path d="M42 28l12-22" stroke="{GOLD}" stroke-width="4" stroke-linecap="round"/>'
        f'<path d="M4 32h56a28 28 0 0 1-56 0z" fill="{GREEN}"/>'
        f'<ellipse cx="32" cy="32" rx="28" ry="5.5" fill="#f2b630"/>'
        f'<path d="M14 42q6 8 16 9" stroke="#fff" stroke-width="2.4" fill="none" stroke-linecap="round" opacity=".35"/>', cls="pic big")
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

def agua():
    glass = _svg(
        f'<path d="M14 12h36l-4 44a5 5 0 0 1-5 4.5H23a5 5 0 0 1-5-4.5z" fill="#fff" stroke="#d8d3bc" stroke-width="2"/>'
        f'<path d="M16.5 30q8 4 15.5 0t15.5 0l-2.5 26a3.5 3.5 0 0 1-3.5 3H22.5a3.5 3.5 0 0 1-3.5-3z" fill="#9fc7e6"/>'
        f'<path d="M22 36l1.6 16" stroke="#fff" stroke-width="2.6" stroke-linecap="round" opacity=".7"/>'
        f'<path d="M56 18c3 4 4 6 4 8a4 4 0 0 1-8 0c0-2 1-4 4-8z" fill="#7ab0d9"/>', cls="pic big")
    inner = (f'<div class="wt">{glass}<div><b>En vaso, con las comidas</b>'
             f'<span>Desde que empieza a comer. Sin forzar: él decide cuánto bebe.</span></div></div>')
    return _figure(inner, None, "Un vaso de agua: se ofrece con las comidas, sin forzar.")

IL = {"edad": edad, "agua": agua, "senales": senales, "leche": leche, "plato": plato,
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
.ages{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;align-items:center}
.ages li{position:relative;background:#fff;border-radius:20px;padding:18px 12px 18px;text-align:center;display:flex;flex-direction:column;align-items:center;gap:2px;font-size:.85rem;line-height:1.4;color:var(--mute)}
.ages li:not(:last-child)::after{content:"";position:absolute;right:-11px;top:50%;width:10px;height:10px;border-top:2.5px solid var(--line);border-right:2.5px solid var(--line);transform:translate(0,-50%) rotate(45deg);z-index:1}
.ages .m{font-weight:700;font-size:.78rem;letter-spacing:.04em;text-transform:uppercase;color:var(--mute)}
.ages b{color:var(--terra);font-size:1rem}
.ages .on{border:2.5px solid var(--green);padding:24px 12px;box-shadow:0 10px 24px rgba(74,135,96,.14)}
.ages .on b{color:var(--green);font-size:1.08rem}.ages li:last-child b{color:#a5781e}
.ages .pic{margin-bottom:6px}.ages .on .pic{width:84px;height:84px}
.tiles{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.tiles li{position:relative;background:#fff;border-radius:18px;padding:22px 10px 16px;text-align:center;font-weight:700;font-size:.85rem;line-height:1.35}
.vs{display:flex;align-items:center;justify-content:center;gap:16px}
.vs .side{flex:1;text-align:center;display:flex;flex-direction:column;align-items:center;gap:4px}
.vs .side span{color:var(--mute);font-size:.88rem;line-height:1.4;max-width:15em}
.vs .side.main b{color:var(--green)}
.wt{display:flex;align-items:center;justify-content:center;gap:20px}.wt .pic{margin:0;flex:none}
.wt b{display:block;font-size:1.05rem;color:var(--green);margin:0 0 4px}.wt span{color:var(--mute);font-size:.92rem;line-height:1.45}
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
.ages{grid-template-columns:1fr}.ages li{display:grid;grid-template-columns:64px 1fr;grid-template-areas:"p m" "p b" "p d";text-align:left;column-gap:14px;align-items:center;padding:14px 16px}.ages .on{padding:16px}.ages li .pic{grid-area:p;width:64px!important;height:64px!important;margin:0}.ages .m{grid-area:m}.ages b{grid-area:b}.ages li>span:last-child{grid-area:d}.ages li:not(:last-child)::after{right:auto;left:50%;top:auto;bottom:-11px;transform:translate(-50%,0) rotate(135deg)}

.cuts{grid-template-columns:1fr}.cuts li{display:grid;grid-template-columns:1fr auto;grid-template-areas:"t p" "d p";text-align:left;align-items:center;column-gap:8px;padding:12px 14px}
.cuts b{grid-area:t}.cuts li>span{grid-area:d}.cuts .pair{grid-area:p}
.plate{grid-template-columns:1fr}.plate .ics{grid-template-columns:repeat(4,1fr)}
.cmp{grid-template-columns:1fr}
.vs{gap:8px}.vs .pic.big{width:76px;height:76px}
}
"""
