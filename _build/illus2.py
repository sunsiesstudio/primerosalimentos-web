# Ilustraciones e infografías para el resto de artículos del blog.
# - Guías: en el cuerpo se colocan con <!--il2:nombre--> (ver ESPEC al final) y se sustituyen al construir.
# - Recetas: receta(a) convierte ingredientes, pasos y "cómo servirlo" en una libreta ilustrada.
# Mismo estilo plano que illus.py, y reutiliza sus caras y los iconos de alimentos.
import html, re
from illus import _face, _svg, _figure, food, SKIN, HAIR, INK, GREEN, TERRA, GOLD, CARD

LINE = "#d8d3bc"; BLUE = "#7ab0d9"; LBLUE = "#dcecf7"; PURPLE = "#8a5ac8"; CREAM = "#fbf3dc"; GREY = "#9a9a9a"

def F(n, x=4, y=4, s=.875):
    """Icono de alimento dentro de un dibujo de 64x64."""
    return f'<g transform="translate({x} {y}) scale({s})">{food(n).replace("<svg ", '<svg width="64" height="64" ', 1)}</g>'

NO = lambda x=54, y=10: f'<circle cx="{x}" cy="{y}" r="8" fill="{TERRA}"/><path d="M{x-3.5} {y-3.5}l7 7M{x+3.5} {y-3.5}l-7 7" stroke="#fff" stroke-width="2.2" stroke-linecap="round"/>'
SI = lambda x=54, y=10: f'<circle cx="{x}" cy="{y}" r="8" fill="{GREEN}"/><path d="M{x-4} {y}l3 3 5-6" stroke="#fff" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
def TXT(x, y, t, size=10, fill=INK, w=800, anchor="middle"):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Montserrat,sans-serif" font-weight="{w}" font-size="{size}" fill="{fill}">{t}</text>'

# ---------------------------------------------------------------- pictogramas (64x64)
P = {}
def pic(name):
    def deco(f): P[name] = f; return f
    return deco

@pic("sal")
def _(): return (f'<rect x="20" y="22" width="24" height="34" rx="7" fill="#fff" stroke="{LINE}" stroke-width="2"/>'
                 f'<path d="M20 28a12 12 0 0 1 24 0z" fill="{GREY}"/><circle cx="28" cy="21" r="1.3" fill="#fff"/><circle cx="32" cy="19" r="1.3" fill="#fff"/><circle cx="36" cy="21" r="1.3" fill="#fff"/>'
                 + TXT(32, 46, "SAL", 9, GREY))
@pic("azucar")
def _(): return (f'<rect x="10" y="30" width="22" height="22" rx="3" fill="#fff" stroke="{LINE}" stroke-width="2"/>'
                 f'<rect x="30" y="22" width="22" height="22" rx="3" fill="#fff" stroke="{LINE}" stroke-width="2" transform="rotate(10 41 33)"/>'
                 f'<path d="M14 36h4M20 44h4M36 30h4M40 38h3" stroke="{LINE}" stroke-width="1.6" stroke-linecap="round"/>')
@pic("miel")
def _(): return (f'<rect x="14" y="20" width="36" height="36" rx="10" fill="{GOLD}"/><rect x="16" y="12" width="32" height="9" rx="3" fill="{TERRA}"/>'
                 f'<path d="M20 30h24" stroke="#f2cf4a" stroke-width="4" stroke-linecap="round"/>' + TXT(32, 46, "MIEL", 8, "#fff"))
@pic("zumo")
def _(): return (f'<path d="M18 16h28v40a4 4 0 0 1-4 4H22a4 4 0 0 1-4-4z" fill="#f2a43a"/><path d="M18 16l6-8h16l6 8z" fill="#e8892a"/>'
                 f'<path d="M38 8l6-6" stroke="{TERRA}" stroke-width="3" stroke-linecap="round"/><circle cx="32" cy="38" r="9" fill="#ffd27a"/><path d="M32 29v18M23 38h18M26 32l12 12M38 32L26 44" stroke="#f2a43a" stroke-width="1.4"/>')
@pic("infusion")
def _(): return (f'<path d="M10 24h38v14a17 17 0 0 1-17 17h-4A17 17 0 0 1 10 38z" fill="#fff" stroke="{LINE}" stroke-width="2"/>'
                 f'<path d="M48 28h4a7 7 0 0 1 0 14h-5" fill="none" stroke="{LINE}" stroke-width="3"/><path d="M13 30h32v8a14 14 0 0 1-14 14h-4a14 14 0 0 1-14-14z" fill="#d9a35b" opacity=".7"/>'
                 f'<path d="M30 24V8" stroke="{GREY}" stroke-width="1.6"/><rect x="34" y="4" width="12" height="10" rx="2" fill="{TERRA}"/><path d="M30 8l4 2" stroke="{GREY}" stroke-width="1.4"/>')
@pic("sangre")
def _(): return (P["panal"]() + f'<path d="M44 26c4 5 6 8 6 10a6 6 0 0 1-12 0c0-2 2-5 6-10z" fill="#d23c3c"/>')
@pic("galleta")
def _(): return (f'<circle cx="32" cy="34" r="22" fill="#d9a35b"/><circle cx="32" cy="34" r="18" fill="#e6b672"/>'
                 + "".join(f'<circle cx="{x}" cy="{y}" r="2.6" fill="#7a4a24"/>' for x, y in [(24, 28), (38, 26), (30, 40), (42, 40), (22, 40), (34, 33)]))
@pic("pantalla")
def _(): return (f'<rect x="8" y="12" width="48" height="34" rx="5" fill="{INK}"/><rect x="12" y="16" width="40" height="26" rx="2" fill="#5b6cd8"/>'
                 f'<path d="M28 23v12l10-6z" fill="#fff"/><rect x="24" y="48" width="16" height="4" rx="2" fill="{INK}"/>')
@pic("reloj")
def _(): return (f'<circle cx="32" cy="34" r="22" fill="#fff" stroke="{GOLD}" stroke-width="4"/>'
                 f'<path d="M32 22v12l8 6" stroke="{GOLD}" stroke-width="3.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
                 f'<rect x="28" y="6" width="8" height="5" rx="2" fill="{GOLD}"/>')
@pic("calendario")
def _(): return (f'<rect x="10" y="14" width="44" height="42" rx="6" fill="#fff" stroke="{LINE}" stroke-width="2"/><path d="M10 20a6 6 0 0 1 6-6h32a6 6 0 0 1 6 6v6H10z" fill="{TERRA}"/>'
                 f'<path d="M20 10v8M44 10v8" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
                 + "".join(f'<rect x="{16+c*9}" y="{31+r*8}" width="6" height="5" rx="1.5" fill="{GREEN if (r,c)==(1,2) else LINE}"/>' for r in range(3) for c in range(4)))
@pic("telefono")
def _(): return (f'<rect x="18" y="6" width="28" height="52" rx="7" fill="{INK}"/><rect x="21" y="12" width="22" height="38" rx="3" fill="#fff"/>' + TXT(32, 36, "112", 11, TERRA))
@pic("termometro")
def _(): return (f'<rect x="27" y="6" width="10" height="40" rx="5" fill="#fff" stroke="{LINE}" stroke-width="2"/><circle cx="32" cy="48" r="9" fill="{TERRA}"/>'
                 f'<rect x="30" y="20" width="4" height="26" fill="{TERRA}"/><path d="M40 14h6M40 22h4M40 30h6" stroke="{LINE}" stroke-width="2" stroke-linecap="round"/>')
@pic("diente")
def _(): return (f'<path d="M14 20c0-10 8-12 12-10 4 2 8 2 12 0 4-2 12 0 12 10 0 8-4 10-5 18-1 8-3 16-7 16-3 0-3-12-6-12s-3 12-6 12c-4 0-6-8-7-16-1-8-5-10-5-18z" fill="#fff" stroke="{LINE}" stroke-width="2"/>'
                 f'<path d="M22 20q4-4 8 0" stroke="#bfe0f2" stroke-width="3" fill="none" stroke-linecap="round"/>')
@pic("cepillo")
def _(): return (f'<rect x="8" y="40" width="40" height="7" rx="3.5" fill="{BLUE}" transform="rotate(-30 28 43)"/>'
                 f'<g transform="rotate(-30 46 26)"><rect x="40" y="22" width="18" height="8" rx="2" fill="#fff" stroke="{LINE}"/>'
                 + "".join(f'<path d="M{42+i*3.2} 22v-7" stroke="#fff" stroke-width="2"/><path d="M{42+i*3.2} 22v-7" stroke="#cfe5f2" stroke-width="1.4"/>' for i in range(5))
                 + f'</g><path d="M40 8c3 0 5 2 5 4" stroke="#fff" stroke-width="5" stroke-linecap="round"/><circle cx="43" cy="9" r="3" fill="#e9f4ff" stroke="{BLUE}"/>')
@pic("trona")
def _(): return (f'<path d="M14 58V30a6 6 0 0 1 6-6h24a6 6 0 0 1 6 6v28" fill="none" stroke="{TERRA}" stroke-width="4" stroke-linecap="round"/>'
                 f'<rect x="10" y="44" width="44" height="6" rx="3" fill="{TERRA}"/><path d="M22 44V36a10 10 0 0 1 20 0v8z" fill="{GREEN}"/>'
                 f'<path d="M20 38c-3 2-4 5-3 7M44 38c3 2 4 5 3 7" stroke="{SKIN}" stroke-width="3.4" fill="none" stroke-linecap="round"/>' + _face(32, 18, 11))
@pic("biberon")
def _(): return (f'<rect x="24" y="4" width="16" height="7" rx="3" fill="{GOLD}"/><rect x="21" y="10" width="22" height="5" rx="2" fill="{TERRA}"/>'
                 f'<rect x="19" y="15" width="26" height="45" rx="9" fill="#fff" stroke="{LINE}" stroke-width="2"/><path d="M21 30h22v20a7 7 0 0 1-7 7h-8a7 7 0 0 1-7-7z" fill="{CREAM}"/>')
@pic("vaso")
def _(): return (f'<path d="M14 12h36l-4 44a5 5 0 0 1-5 4.5H23a5 5 0 0 1-5-4.5z" fill="#fff" stroke="{LINE}" stroke-width="2"/>'
                 f'<path d="M16.5 30q8 4 15.5 0t15.5 0l-2.5 26a3.5 3.5 0 0 1-3.5 3H22.5a3.5 3.5 0 0 1-3.5-3z" fill="#9fc7e6"/>')
@pic("pajita")
def _(): return (f'<path d="M36 22l8-16h8" stroke="{TERRA}" stroke-width="3.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
                 f'<rect x="16" y="20" width="32" height="38" rx="9" fill="#fff" stroke="{LINE}" stroke-width="2"/><path d="M18 34h28v14a8 8 0 0 1-8 8H26a8 8 0 0 1-8-8z" fill="#9fc7e6"/>'
                 f'<rect x="12" y="30" width="6" height="14" rx="3" fill="{GREEN}"/><rect x="46" y="30" width="6" height="14" rx="3" fill="{GREEN}"/>')
@pic("babero")
def _(): return (f'<path d="M20 10a12 10 0 0 0 24 0h8c4 0 6 4 6 8v26c0 8-8 14-26 14S6 52 6 44V18c0-4 2-8 6-8z" fill="{GREEN}"/>'
                 f'<path d="M14 42q18 8 36 0v4q-18 10-36 0z" fill="#3d7050"/><circle cx="24" cy="28" r="2.2" fill="#fff" opacity=".6"/><circle cx="38" cy="24" r="2.2" fill="#fff" opacity=".6"/><circle cx="32" cy="34" r="2.2" fill="#fff" opacity=".6"/>')
@pic("babero_mangas")
def _(): return (f'<path d="M18 12h28l14 20-8 6-6-8v26H18V30l-6 8-8-6z" fill="{BLUE}"/><path d="M26 12a6 5 0 0 0 12 0" fill="#fff"/>'
                 f'<path d="M4 32l8 6M60 32l-8 6" stroke="#5f97c4" stroke-width="3" stroke-linecap="round"/>')
@pic("cuchara")
def _(): return (f'<ellipse cx="20" cy="22" rx="10" ry="13" fill="{GOLD}" transform="rotate(-35 20 22)"/><path d="M26 30l26 26" stroke="{GOLD}" stroke-width="6" stroke-linecap="round"/>')
@pic("plato")
def _(): return (f'<ellipse cx="32" cy="38" rx="27" ry="20" fill="#fff" stroke="{LINE}" stroke-width="2"/><ellipse cx="32" cy="38" rx="17" ry="12" fill="#f4efe0"/>'
                 f'<path d="M4 8v16M8 8v16M12 8v16M8 24v30" stroke="{GREY}" stroke-width="2.4" stroke-linecap="round"/>')
@pic("familia")
def _(): return (_face(16, 22, 10) + _face(48, 20, 11, fill="#e9b48f") + _face(32, 30, 8)
                 + f'<rect x="4" y="44" width="56" height="6" rx="3" fill="{TERRA}"/><path d="M10 50v10M54 50v10" stroke="{TERRA}" stroke-width="4" stroke-linecap="round"/>')
@pic("bebe")
def _(): return _face(32, 34, 20)
@pic("bebe_triste")
def _(): return _face(32, 34, 20, "flat") + f'<path d="M18 30l6 2M40 32l6-2" stroke="{INK}" stroke-width="2" stroke-linecap="round"/>'
@pic("bebe_sueno")
def _(): return _face(28, 36, 18, "flat") + TXT(52, 20, "z", 12, BLUE) + TXT(58, 10, "z", 9, BLUE)
@pic("bebe_malito")
def _(): return (_face(30, 36, 18, "flat") + f'<rect x="38" y="36" width="20" height="6" rx="3" fill="#fff" stroke="{LINE}" transform="rotate(-20 48 39)"/>'
                 f'<circle cx="57" cy="34" r="3.5" fill="{TERRA}"/><path d="M12 14q4-6 8 0" stroke="{BLUE}" stroke-width="2" fill="none"/>')
@pic("mano_tira")
def _(): return (f'<rect x="28" y="4" width="11" height="40" rx="5.5" fill="#f2b630" transform="rotate(12 33 24)"/>'
                 f'<path d="M14 40c0-8 6-12 12-12h14c6 0 10 4 10 10v8c0 8-6 14-14 14H26c-8 0-12-6-12-12z" fill="{SKIN}"/>'
                 f'<path d="M24 36h22M24 42h22M24 48h20" stroke="#e0a983" stroke-width="1.6" stroke-linecap="round"/>')
@pic("pinza")
def _(): return (f'<path d="M8 50c4-14 14-22 26-22l10 2" stroke="{SKIN}" stroke-width="12" fill="none" stroke-linecap="round"/>'
                 f'<path d="M36 22l14 6M36 38l14-4" stroke="{SKIN}" stroke-width="7" stroke-linecap="round"/><circle cx="53" cy="31" r="4.5" fill="#6db35a"/>')
@pic("trocitos")
def _(): return (f'<ellipse cx="32" cy="42" rx="27" ry="12" fill="#fff" stroke="{LINE}" stroke-width="2"/>'
                 + "".join(f'<rect x="{x}" y="{y}" width="7" height="7" rx="2" fill="{c}"/>' for x, y, c in [(16, 36, "#f2b630"), (26, 40, "#6db35a"), (36, 36, "#e86f4a"), (44, 42, "#f2b630"), (22, 45, "#e86f4a"), (34, 46, "#6db35a")]))
@pic("tenedor_bocado")
def _(): return (f'<path d="M40 60V30" stroke="{GREY}" stroke-width="4" stroke-linecap="round"/><path d="M32 6v16q0 8 8 8t8-8V6M40 6v18" stroke="{GREY}" stroke-width="3" fill="none" stroke-linecap="round"/>'
                 f'<rect x="8" y="34" width="16" height="14" rx="4" fill="#e86f4a"/><rect x="12" y="20" width="12" height="11" rx="3" fill="#6db35a"/>')
@pic("panal")
def _(): return (f'<path d="M10 22h44l-4 30a8 8 0 0 1-8 7H22a8 8 0 0 1-8-7z" fill="#fff" stroke="{LINE}" stroke-width="2"/>'
                 f'<path d="M10 22c8 6 36 6 44 0" stroke="{BLUE}" stroke-width="3" fill="none"/><path d="M26 40q6 6 12 0" stroke="{BLUE}" stroke-width="2.4" fill="none" stroke-linecap="round"/>')
@pic("pastilla")
def _(): return (f'<g transform="rotate(-35 32 32)"><rect x="12" y="22" width="40" height="20" rx="10" fill="#fff" stroke="{LINE}" stroke-width="2"/>'
                 f'<path d="M32 22h10a10 10 0 0 1 0 20H32z" fill="{TERRA}"/></g>')
@pic("b12")
def _(): return (f'<rect x="8" y="16" width="48" height="32" rx="16" fill="{TERRA}"/><path d="M32 16h8a16 16 0 0 1 0 32h-8z" fill="#e48a68"/>' + TXT(32, 37, "B12", 13, "#fff"))
@pic("etiqueta")
def _(): return (f'<path d="M8 14h30l18 18-18 18H8z" fill="#fff" stroke="{LINE}" stroke-width="2"/><circle cx="16" cy="32" r="3" fill="{LINE}"/>'
                 f'<path d="M24 24h12M24 32h16M24 40h10" stroke="{GREY}" stroke-width="2.4" stroke-linecap="round"/>')
@pic("lupa")
def _(): return (f'<circle cx="26" cy="26" r="16" fill="#e9f4ff" stroke="{INK}" stroke-width="5"/><path d="M38 38l16 16" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
                 f'<path d="M18 22a8 8 0 0 1 8-6" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round"/>')
@pic("sol")
def _(): return (f'<circle cx="32" cy="32" r="13" fill="#f2b630"/>'
                 + "".join(f'<path d="M32 6v8" stroke="#f2b630" stroke-width="4" stroke-linecap="round" transform="rotate({a} 32 32)"/>' for a in range(0, 360, 45)))
@pic("casa")
def _(): return (f'<path d="M8 30L32 10l24 20v26H8z" fill="#fff" stroke="{LINE}" stroke-width="2"/><path d="M4 32L32 8l28 24" stroke="{TERRA}" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
                 f'<rect x="26" y="38" width="12" height="18" rx="2" fill="{GREEN}"/><rect x="14" y="34" width="8" height="8" rx="1.5" fill="#9fc7e6"/><rect x="42" y="34" width="8" height="8" rx="1.5" fill="#9fc7e6"/>')
@pic("escuela")
def _(): return (P["casa"]() + f'<circle cx="32" cy="24" r="5" fill="{GOLD}"/>'
                 + "".join(f'<circle cx="{x}" cy="58" r="3" fill="{c}"/>' for x, c in [(14, TERRA), (22, BLUE), (44, GREEN), (52, GOLD)]))
@pic("avion")
def _(): return (f'<path d="M6 36l50-18c4-1 6 3 3 5L44 34l4 20-6 2-10-16-14 6 1 8-5 2-4-10-10-4z" fill="#fff" stroke="{BLUE}" stroke-width="2" stroke-linejoin="round"/>')
@pic("nevera_portatil")
def _(): return (f'<rect x="8" y="24" width="48" height="32" rx="6" fill="{BLUE}"/><rect x="8" y="24" width="48" height="10" rx="5" fill="#5f97c4"/>'
                 f'<path d="M20 24v-8h24v8" stroke="{INK}" stroke-width="3.4" fill="none" stroke-linecap="round"/><path d="M26 44l6-4 6 4-6 4z" fill="#fff"/>')
@pic("termo")
def _(): return (f'<rect x="20" y="16" width="24" height="42" rx="7" fill="{GREEN}"/><rect x="18" y="8" width="28" height="10" rx="4" fill="#3d7050"/>'
                 f'<rect x="24" y="28" width="16" height="18" rx="3" fill="#fff" opacity=".85"/><path d="M28 6q-2-3 0-6M36 6q-2-3 0-6" stroke="{LINE}" stroke-width="2" fill="none"/>')
@pic("cruz")
def _(): return (f'<circle cx="32" cy="32" r="24" fill="{TERRA}"/><path d="M32 18v28M18 32h28" stroke="#fff" stroke-width="9" stroke-linecap="round"/>')
@pic("gota")
def _(): return (f'<path d="M32 6c10 14 18 22 18 32a18 18 0 0 1-36 0c0-10 8-18 18-32z" fill="{BLUE}"/><path d="M24 38a8 8 0 0 0 6 8" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round" opacity=".7"/>')
@pic("suero")
def _(): return (f'<rect x="12" y="10" width="40" height="46" rx="5" fill="#fff" stroke="{LINE}" stroke-width="2"/><rect x="12" y="10" width="40" height="12" rx="5" fill="{BLUE}"/>'
                 + TXT(32, 41, "SRO", 11, BLUE) + f'<path d="M20 48h24" stroke="{LINE}" stroke-width="2.4" stroke-linecap="round"/>')
@pic("corazon")
def _(): return f'<path d="M32 54C8 38 6 26 12 18c6-8 16-6 20 2 4-8 14-10 20-2 6 8 4 20-20 36z" fill="{TERRA}"/>'
@pic("estrella")
def _(): return f'<polygon points="32,6 39,23 57,24 43,36 48,54 32,44 16,54 21,36 7,24 25,23" fill="{GOLD}"/>'
@pic("repetir")
def _(): return (f'<path d="M48 26a17 17 0 1 0-2 14" fill="none" stroke="{GREEN}" stroke-width="5" stroke-linecap="round"/>'
                 f'<path d="M50 14v13H37" fill="none" stroke="{GREEN}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')
@pic("manchas")
def _(): return (_face(32, 32, 18) + f'<circle cx="22" cy="24" r="4" fill="#f2b630"/><circle cx="42" cy="40" r="3.5" fill="#e86f4a"/><circle cx="38" cy="20" r="2.6" fill="#6db35a"/><circle cx="18" cy="44" r="3" fill="#e86f4a"/>')
@pic("grumos")
def _(): return (f'<path d="M6 30h52a26 24 0 0 1-52 0z" fill="{GREEN}"/><ellipse cx="32" cy="30" rx="26" ry="6" fill="#f2b630"/>'
                 + "".join(f'<circle cx="{x}" cy="{y}" r="2.6" fill="#d98a1c"/>' for x, y in [(20, 29), (28, 31), (38, 28), (44, 31), (32, 27)]))
@pic("leche_vaca")
def _(): return (f'<path d="M18 18h28v38a4 4 0 0 1-4 4H22a4 4 0 0 1-4-4z" fill="#fff" stroke="{LINE}" stroke-width="2"/><path d="M18 18l6-10h16l6 10z" fill="#e9f4ff" stroke="{LINE}" stroke-width="2"/>'
                 f'<rect x="22" y="30" width="20" height="16" rx="3" fill="{BLUE}"/>' + TXT(32, 41, "LECHE", 6.5, "#fff"))
@pic("yogur")
def _(): return (f'<path d="M16 22h32l-4 34a4 4 0 0 1-4 3H24a4 4 0 0 1-4-3z" fill="#fff" stroke="{LINE}" stroke-width="2"/><rect x="13" y="15" width="38" height="8" rx="3" fill="{GREEN}"/>'
                 f'<path d="M20 38h24" stroke="{BLUE}" stroke-width="6"/>')
@pic("queso")
def _(): return (f'<path d="M6 46L46 18l12 28z" fill="#f2c14e"/><path d="M6 46h52v8H6z" fill="#e0a92e"/>'
                 f'<circle cx="34" cy="38" r="3.4" fill="#e0a92e"/><circle cx="46" cy="32" r="2.4" fill="#e0a92e"/><circle cx="24" cy="42" r="2" fill="#e0a92e"/>')
@pic("bebida_veg")
def _(): return (f'<path d="M20 18h24v38a4 4 0 0 1-4 4H24a4 4 0 0 1-4-4z" fill="#f4ecd8" stroke="{LINE}" stroke-width="2"/><path d="M20 18l4-8h16l4 8z" fill="#e6dcc0"/>'
                 f'<path d="M32 30c-6 4-6 12 0 16 6-4 6-12 0-16z" fill="#8fbf6a"/>')
@pic("carne")
def _(): return (f'<path d="M8 32c0-14 16-20 28-18s22 12 18 24-18 18-30 14S8 44 8 32z" fill="#b5523b"/>'
                 f'<path d="M16 30c4-8 18-10 24-4" stroke="#f3c7a1" stroke-width="3.4" fill="none" stroke-linecap="round"/><circle cx="40" cy="38" r="4.5" fill="#f3c7a1"/>')
@pic("salmon")
def _(): return (f'<path d="M6 36c8-14 42-18 52-6-8 14-42 18-52 6z" fill="#f08a5d"/>'
                 f'<path d="M16 30q4 6 0 12M26 27q4 8 0 16M36 26q4 8 0 16M46 27q4 6 0 13" stroke="#ffd2bd" stroke-width="2" fill="none" stroke-linecap="round"/>')
@pic("harina")
def _(): return (f'<path d="M16 18h32l4 40H12z" fill="#f4efe2" stroke="{LINE}" stroke-width="2"/><path d="M16 18l4-8h24l4 8" fill="#e6dfca" stroke="{LINE}" stroke-width="2"/>'
                 f'<path d="M32 30v20M32 34l-5-4M32 34l5-4M32 40l-5-4M32 40l5-4M32 46l-5-4M32 46l5-4" stroke="{GOLD}" stroke-width="2.2" stroke-linecap="round"/>')
@pic("pasta")
def _(): return "".join(f'<path d="M{x} {y}a10 10 0 0 1 18-6" stroke="#f2c14e" stroke-width="8" fill="none" stroke-linecap="round"/><path d="M{x} {y}a10 10 0 0 1 18-6" stroke="#e0a92e" stroke-width="1.4" fill="none" stroke-dasharray="2 3"/>' for x, y in [(8, 30), (30, 26), (16, 50), (36, 52)])
@pic("cuscus")
def _(): return (f'<path d="M6 30h52a26 24 0 0 1-52 0z" fill="{TERRA}"/><ellipse cx="32" cy="30" rx="26" ry="7" fill="#f2d27a"/>'
                 + "".join(f'<circle cx="{x}" cy="{y}" r="1.4" fill="#d9a83a"/>' for x, y in [(16, 30), (22, 28), (28, 31), (34, 27), (40, 30), (46, 28), (24, 33), (38, 33), (30, 26)]))
@pic("garbanzos")
def _(): return "".join(f'<circle cx="{x}" cy="{y}" r="9" fill="#e2c08b"/><path d="M{x-4} {y-4}q4-3 8 0" stroke="#c9a06a" stroke-width="1.6" fill="none"/>' for x, y in [(20, 40), (38, 42), (28, 26), (46, 26), (30, 52)])
@pic("cebolla")
def _(): return (f'<path d="M32 8c-2 8-20 14-20 30a20 18 0 0 0 40 0c0-16-18-22-20-30z" fill="#e7c38a"/>'
                 f'<path d="M24 26q-6 12 2 24M40 26q6 12-2 24M32 22v30" stroke="#d1a35e" stroke-width="1.6" fill="none"/>')
@pic("ajo")
def _(): return (f'<path d="M32 8c-4 8-18 16-18 28 0 10 8 18 18 18s18-8 18-18c0-12-14-20-18-28z" fill="#f6f1e6" stroke="{LINE}" stroke-width="2"/>'
                 f'<path d="M26 30q-2 12 4 22M38 30q2 12-4 22" stroke="{LINE}" stroke-width="1.6" fill="none"/>')
@pic("limon")
def _(): return f'<ellipse cx="32" cy="34" rx="22" ry="16" fill="#f5d33c"/><path d="M8 34l-4 2M56 34l4-2" stroke="#e0bd25" stroke-width="4" stroke-linecap="round"/>'
@pic("aceite")
def _(): return (f'<rect x="27" y="4" width="10" height="8" rx="2" fill="#3d7050"/><path d="M26 12h12l8 14v28a6 6 0 0 1-6 6H24a6 6 0 0 1-6-6V26z" fill="#c4cf5a" stroke="#9aa73f" stroke-width="2"/>'
                 f'<ellipse cx="32" cy="42" rx="8" ry="6" fill="#6f8b2e"/>')
@pic("canela")
def _(): return (f'<rect x="10" y="26" width="44" height="10" rx="5" fill="#a5612f" transform="rotate(-20 32 31)"/><rect x="12" y="38" width="44" height="10" rx="5" fill="#8a4f24" transform="rotate(-20 34 43)"/>')
@pic("hierbas")
def _(): return (f'<path d="M32 58V24" stroke="#3d7050" stroke-width="3"/>' + "".join(f'<ellipse cx="{x}" cy="{y}" rx="8" ry="4.5" fill="#6db35a" transform="rotate({r} {x} {y})"/>' for x, y, r in [(24, 30, 30), (40, 26, -30), (24, 42, 30), (40, 40, -30), (32, 18, 90)]))
@pic("especias")
def _(): return (f'<rect x="18" y="20" width="28" height="36" rx="6" fill="#fff" stroke="{LINE}" stroke-width="2"/><rect x="18" y="12" width="28" height="10" rx="3" fill="{INK}"/>'
                 f'<path d="M20 36h24v14a4 4 0 0 1-4 4H24a4 4 0 0 1-4-4z" fill="#d9822b"/>')
@pic("bote")
def _(): return (f'<rect x="16" y="22" width="32" height="34" rx="7" fill="#d9b48a"/><rect x="14" y="14" width="36" height="9" rx="3" fill="{TERRA}"/>'
                 f'<path d="M20 38q12-7 24 0v12a5 5 0 0 1-5 5H25a5 5 0 0 1-5-5z" fill="#c69663"/>')
@pic("levadura")
def _(): return (f'<rect x="14" y="14" width="36" height="40" rx="4" fill="#fff" stroke="{LINE}" stroke-width="2"/><path d="M14 22h36" stroke="{TERRA}" stroke-width="4"/>'
                 + "".join(f'<circle cx="{x}" cy="{y}" r="3" fill="#f2cf4a"/>' for x, y in [(26, 36), (36, 32), (32, 44), (40, 42)]))
@pic("caldo")
def _(): return P["olla"]()
@pic("verduras")
def _(): return F("Brócoli", 2, 14, .55) + F("Pimiento rojo", 26, 4, .55) + F("Guisantes", 22, 30, .55)

# --- utensilios de cocina para los pasos
@pic("horno")
def _(): return (f'<rect x="6" y="8" width="52" height="50" rx="7" fill="#efeadb" stroke="#bdb59a" stroke-width="2"/><path d="M6 15a7 7 0 0 1 7-7h38a7 7 0 0 1 7 7v5H6z" fill="#d8d3bc"/>'
                 f'<circle cx="14" cy="14" r="2.4" fill="{TERRA}"/><circle cx="22" cy="14" r="2.4" fill="#bdb59a"/><circle cx="30" cy="14" r="2.4" fill="#bdb59a"/>'
                 f'<rect x="12" y="25" width="40" height="27" rx="4" fill="#3b2f2a"/><rect x="15" y="28" width="34" height="21" rx="3" fill="#f2b630" opacity=".55"/>'
                 f'<path d="M18 44h28" stroke="{TERRA}" stroke-width="2"/><path d="M20 16h30" stroke="{INK}" stroke-width="2" stroke-linecap="round" opacity=".3"/>')
@pic("sarten")
def _(): return (f'<ellipse cx="26" cy="32" rx="22" ry="9" fill="#3b3b3b"/><ellipse cx="26" cy="30" rx="19" ry="6.5" fill="#5a5a5a"/>'
                 f'<path d="M46 31l16-5" stroke="#8a5a2d" stroke-width="5.4" stroke-linecap="round"/>'
                 f'<path d="M14 56q4-5 0-10M26 58q4-5 0-10M38 56q4-5 0-10" stroke="#e8743b" stroke-width="3" fill="none" stroke-linecap="round"/>')
@pic("olla")
def _(): return (f'<path d="M12 30h40v18a8 8 0 0 1-8 8H20a8 8 0 0 1-8-8z" fill="{GREEN}"/><rect x="8" y="26" width="48" height="6" rx="3" fill="#3d7050"/>'
                 f'<path d="M5 36h7M52 36h7" stroke="#3d7050" stroke-width="4" stroke-linecap="round"/>'
                 f'<path d="M22 20q-3-5 0-10M32 20q-3-5 0-10M42 20q-3-5 0-10" stroke="#bdb59a" stroke-width="2.6" fill="none" stroke-linecap="round"/>')
@pic("bol")
def _(): return (f'<path d="M6 32h52a26 22 0 0 1-52 0z" fill="{TERRA}"/><ellipse cx="32" cy="32" rx="26" ry="5.5" fill="#f3d9a4"/>'
                 f'<path d="M38 30L52 6" stroke="{GREY}" stroke-width="3" stroke-linecap="round"/>'
                 f'<path d="M52 6c-7 0-12 8-8 14M52 6c4 5 2 13-6 16" stroke="{GREY}" stroke-width="2" fill="none"/>')
@pic("tenedor")
def _(): return (f'<ellipse cx="28" cy="46" rx="25" ry="9" fill="#fff" stroke="{LINE}" stroke-width="2"/><ellipse cx="28" cy="44" rx="13" ry="4.5" fill="#f2cf4a"/>'
                 f'<path d="M42 38L58 8" stroke="{GREY}" stroke-width="3.6" stroke-linecap="round"/><path d="M36 33l4-8M40 35l4-8M44 37l4-8" stroke="{GREY}" stroke-width="2.2" stroke-linecap="round"/>')
@pic("batidora")
def _(): return (f'<path d="M18 12h28l-4 32H22z" fill="#d9ecf7" stroke="{BLUE}" stroke-width="2"/><path d="M20.5 28h23l-2 16h-19z" fill="#f2b630" opacity=".75"/>'
                 f'<rect x="16" y="7" width="32" height="6" rx="3" fill="#3b3b3b"/><rect x="14" y="44" width="36" height="14" rx="4" fill="#3b3b3b"/><circle cx="32" cy="51" r="3" fill="{TERRA}"/>')
@pic("cuchillo")
def _(): return (f'<rect x="4" y="34" width="50" height="22" rx="6" fill="#d9b48a"/><circle cx="48" cy="40" r="2.5" fill="#b08458"/>'
                 f'<path d="M12 30L46 10" stroke="#d6d6d6" stroke-width="8" stroke-linecap="round"/><path d="M46 10l12-7" stroke="#3b3b3b" stroke-width="6" stroke-linecap="round"/>')
@pic("rallador")
def _(): return (f'<path d="M18 10h28l6 48H12z" fill="#e2e2e2" stroke="{GREY}" stroke-width="2"/><rect x="25" y="2" width="14" height="10" rx="5" fill="none" stroke="{GREY}" stroke-width="3"/>'
                 + "".join(f'<path d="M{x} {y}h4" stroke="{GREY}" stroke-width="2" stroke-linecap="round"/>' for y in (22, 30, 38, 46) for x in (20, 28, 36)))
@pic("colador")
def _(): return (f'<path d="M8 26h48a24 22 0 0 1-48 0z" fill="#9fc7e6"/><path d="M2 26h8M54 26h8" stroke="#5f97c4" stroke-width="4" stroke-linecap="round"/>'
                 + "".join(f'<circle cx="{x}" cy="{y}" r="1.6" fill="#fff"/>' for x, y in [(20, 34), (28, 38), (36, 38), (44, 34), (24, 42), (32, 44), (40, 42)])
                 + f'<path d="M24 4v10M32 2v12M40 4v10" stroke="{BLUE}" stroke-width="2.4" stroke-linecap="round" stroke-dasharray="3 3"/>')
@pic("servir")
def _(): return (f'<ellipse cx="32" cy="46" rx="28" ry="10" fill="#fff" stroke="{LINE}" stroke-width="2"/><ellipse cx="32" cy="44" rx="16" ry="5" fill="#e9c98a"/>'
                 f'<path d="M24 32q-3-5 0-10M32 30q-3-5 0-10M40 32q-3-5 0-10" stroke="#bdb59a" stroke-width="2.4" fill="none" stroke-linecap="round"/>')
@pic("congelador")
def _(): return (f'<circle cx="32" cy="32" r="26" fill="{LBLUE}"/>'
                 + "".join(f'<g transform="rotate({a} 32 32)"><path d="M32 12v40" stroke="{BLUE}" stroke-width="3.4" stroke-linecap="round"/><path d="M26 16l6 6 6-6M26 48l6-6 6 6" stroke="{BLUE}" stroke-width="2.6" fill="none" stroke-linecap="round"/></g>' for a in (0, 60, 120)))
@pic("nevera")
def _(): return (f'<rect x="14" y="4" width="36" height="56" rx="6" fill="#fff" stroke="{LINE}" stroke-width="2"/><path d="M14 24h36" stroke="{LINE}" stroke-width="2"/>'
                 f'<path d="M20 12v6M20 30v10" stroke="{GREY}" stroke-width="3" stroke-linecap="round"/><circle cx="42" cy="44" r="3" fill="{BLUE}"/>')
@pic("molde")
def _(): return (f'<rect x="4" y="24" width="56" height="26" rx="5" fill="#7a7a7a"/>'
                 + "".join(f'<ellipse cx="{x}" cy="30" rx="8" ry="3.5" fill="#5a5a5a"/><path d="M{x-8} 30q8 12 16 0" fill="#f2b630"/>' for x in (15, 32, 49)))
@pic("bandeja")
def _(): return (f'<rect x="2" y="40" width="60" height="6" rx="3" fill="{GREY}"/>'
                 + "".join(f'<rect x="{x}" y="28" width="10" height="13" rx="4" fill="{c}"/>' for x, c in [(8, "#f2b630"), (22, "#e8892a"), (36, "#f2b630"), (50, "#e8892a")]))

def ic(name, cls=""):
    """Pictograma o alimento como <svg> independiente."""
    body = P[name]() if name in P else F(name, 2, 2, .94)
    return _svg(body, cls=f"pic {cls}".strip())

# ---------------------------------------------------------------- componentes
def tiles(items, label, caption=None, num=False, tone=""):
    """items: (icono|svg, título, subtítulo|None, marca 'si'|'no'|None)"""
    out = []
    for i, it in enumerate(items, 1):
        name, t = it[0], it[1]
        sub = it[2] if len(it) > 2 else None
        mark = it[3] if len(it) > 3 else None
        body = (P[name]() if name in P else F(name, 2, 2, .94)) if isinstance(name, str) and not name.startswith("<") else name
        body += NO() if mark == "no" else SI() if mark == "si" else ""
        out.append(f'<li>{f"<span class=n>{i}</span>" if num else ""}{_svg(body)}<b>{t}</b>{f"<span class=s>{sub}</span>" if sub else ""}</li>')
    n = len(out); cols = 3 if n in (3, 5, 6, 9) else 5 if n == 10 else 4
    return _figure(f'<ul class="tiles i2t c{cols} {tone}">{"".join(out)}</ul>', caption, label)

def cmp(ok, ko, label, caption=None):
    """ok/ko: (título, [items], acción|None, icono|None)"""
    def col(cls, d):
        t, items, act = d[0], d[1], d[2] if len(d) > 2 else None
        p = ic(d[3], "big") if len(d) > 3 and d[3] else ""
        return (f'<div class="col {cls}">{p}<b class="h">{t}</b><ul>' + "".join(f"<li>{x}</li>" for x in items) + "</ul>"
                + (f'<p class="act">{act}</p>' if act else "") + "</div>")
    return _figure(f'<div class="cmp">{col("ok", ok)}{col("ko", ko)}</div>', caption, label)

def ages(items, label, caption=None):
    """items: (on?, icono, etiqueta, título, texto)"""
    li = "".join(f'<li class="{"on" if on else ""}">{ic(p)}<span class="m">{m}</span><b>{h}</b><span>{d}</span></li>' for on, p, m, h, d in items)
    return _figure(f'<ol class="ages i2a{len(items)}">{li}</ol>', caption, label)

def groups(gs, label, caption=None):
    """gs: (título, tono 'g'|'t'|'o', [(icono, texto)])"""
    out = "".join(f'<div class="gr {tone}"><b>{t}</b><div class="ch">' + "".join(f'<span>{ic(n)}<i>{x}</i></span>' for n, x in its) + '</div></div>' for t, tone, its in gs)
    return _figure(f'<div class="i2g">{out}</div>', caption, label)

def eq(parts, label, caption=None):
    """parts: [(icono, título, texto)], unidos con + y el último con ="""
    out = []
    for i, (n, t, d) in enumerate(parts):
        if i: out.append(f'<div class="plus">{"=" if i == len(parts) - 1 else "+"}</div>')
        out.append(f'<div class="side{" main" if i == len(parts) - 1 else ""}">{ic(n, "big")}<b>{t}</b><span>{d}</span></div>')
    return _figure(f'<div class="vs i2e">{"".join(out)}</div>', caption, label)

def checklist(items, label, caption=None, title=None):
    """items: (icono, texto)"""
    li = "".join(f'<li>{ic(n)}<span>{t}</span></li>' for n, t in items)
    return _figure((f'<b class="i2ct">{title}</b>' if title else "") + f'<ul class="i2c">{li}</ul>', caption, label)

def bars(items, label, caption=None):
    """items: (icono, título, valor 0-1, texto)"""
    li = "".join(f'<li>{ic(n)}<div><b>{t}</b><span class="bar"><i style="width:{int(v*100)}%"></i></span><span class="s">{d}</span></div></li>' for n, t, v, d in items)
    return _figure(f'<ul class="i2b">{li}</ul>', caption, label)

# ---------------------------------------------------------------- figuras de las guías
FISH = lambda c, k="": (f'<path d="M6 34c8-14 34-16 44-2-10 14-36 16-44 2z" fill="{c}"/><path d="M48 32l12-10v22z" fill="{c}"/>'
                        f'<circle cx="16" cy="31" r="2.4" fill="#fff"/><circle cx="16" cy="31" r="1.2" fill="{INK}"/>' + k)
SWORD = f'<path d="M8 30L-2 28" stroke="#6b7a8c" stroke-width="2.4" stroke-linecap="round"/>'
SHARK_FIN = f'<path d="M24 22l8-14 6 16z" fill="#6b7a8c"/>'

def g_prohibidos():
    it = [("sal", "Sal", "Nada antes del año", "no"), ("azucar", "Azúcar y zumos", "Mejor fruta entera", "no"),
          ("miel", "Miel", "Hasta los 12 meses", "no"), ("leche_vaca", "Leche de vaca", "Como bebida, desde los 12 meses", "no"),
          ("Almendra", "Frutos secos enteros", "Hasta los 5 años: en crema", "no"), ("Uvas", "Uvas enteras", "Siempre en cuartos", "no"),
          (FISH("#6b7a8c", SWORD), "Pescados grandes", "Pez espada, tiburón, atún rojo, lucio", "no"),
          ("Espinacas", "Espinacas y acelgas", "Nada antes de los 12 meses", "no"),
          ("Borraja", "Borraja", "Hasta los 3 años", "no"), ("Arroz", "Bebida de arroz", "Mejor evitarla", "no")]
    return tiles(it, "Lo que no puede comer un bebé antes del año y hasta cuándo.", tone="no")

def g_consejos():
    it = [("trona", "Sentado y erguido"), ("bebe", "Él decide cuánto"), ("biberon", "La leche, lo principal"),
          ("Lentejas", "Hierro casi a diario"), ("sal", "Sin sal ni azúcar"), ("grumos", "Grumos cuanto antes"),
          ("Huevo", "Alérgenos pronto"), ("repetir", "Repetir, repetir"), ("familia", "Juntos y sin pantallas"), ("manchas", "Se va a manchar")]
    return tiles(it, "Diez consejos para empezar a comer, ilustrados.", num=True)

def g_trona():
    seat = P["trona"]()
    it = [(seat, "Sentado y erguido", "Espalda recta, caderas a 90°"),
          (seat + f'<path d="M14 60h36" stroke="{GREEN}" stroke-width="4" stroke-linecap="round"/><path d="M50 52v8" stroke="{GREEN}" stroke-width="3"/>', "Reposapiés", "Que apoye los pies"),
          (f'<rect x="2" y="30" width="60" height="6" rx="3" fill="{TERRA}"/><path d="M8 36v24M56 36v24" stroke="{TERRA}" stroke-width="4"/>' + _face(32, 18, 11) + F("Plátano", 40, 18, .3), "Llega a la mesa", "Come con vosotros"),
          (seat + SI(54, 12), "Estable y segura", "Arnés y patas abiertas"),
          (f'<path d="M10 40h44l-4 14H14z" fill="#9fc7e6"/><circle cx="24" cy="30" r="5" fill="#cfe5f2"/><circle cx="34" cy="24" r="4" fill="#cfe5f2"/><circle cx="42" cy="32" r="3" fill="#cfe5f2"/><rect x="36" y="44" width="18" height="10" rx="3" fill="#f2cf4a"/>', "Fácil de limpiar", "Pocas ranuras")]
    return tiles(it, "Cinco cosas que importan al elegir una trona.", num=True)

def g_baberos():
    return ages([(False, "babero_mangas", "6 a 9 meses", "Babero con mangas", "Le tapa los brazos: es cuando más se mancha"),
                 (True, "babero", "9 a 12 meses", "Babero con bolsillo", "Recoge lo que cae, de silicona y fácil de lavar"),
                 (False, "cuchara", "Desde 12 meses", "Cuchara y vaso", "Practica con sus propios cubiertos y vaso abierto")],
                "Qué babero y accesorios usar según la edad.")

def g_tres_formas():
    pure = P["grumos"]()
    blw = F("Brócoli", 0, 14, .5) + F("Plátano", 26, 4, .5) + F("Huevo", 28, 30, .5)
    mix = P["cuchara"]() + F("Brócoli", 30, 26, .55)
    it = [(pure, "Purés", "Con cuchara, pasando a grumos y trozos"), (blw, "BLW", "Trozos que come él solo desde el principio"),
          (mix, "Mixto", "Un poco de cada, según la comida")]
    return tiles(it, "Las tres formas de empezar: purés, BLW o mixto.", caption="Las tres son válidas si avanza en texturas.")

def g_textura():
    hand = (f'<path d="M2 58c6-14 16-20 26-20" stroke="{SKIN}" stroke-width="13" fill="none" stroke-linecap="round"/>'
            f'<path d="M24 22c10-2 18 2 22 10" stroke="{SKIN}" stroke-width="9" fill="none" stroke-linecap="round"/>'
            f'<path d="M24 46c10 2 18-2 22-8" stroke="{SKIN}" stroke-width="9" fill="none" stroke-linecap="round"/>'
            f'<ellipse cx="50" cy="36" rx="10" ry="4" fill="#f2b630"/><ellipse cx="50" cy="35" rx="6" ry="1.6" fill="#f7cf63"/>'
            f'<path d="M62 30l2-3M62 42l2 3M58 28l1-4" stroke="{GOLD}" stroke-width="2" stroke-linecap="round"/>')
    return _figure(f'<div class="wt">{_svg(hand, cls="pic big")}<div><b>¿Se aplasta entre tus dedos?</b>'
                   f'<span>Si se deshace al apretarlo entre el índice y el pulgar, tiene la textura adecuada para empezar.</span></div></div>',
                   None, "Prueba de textura: el alimento tiene que aplastarse entre el índice y el pulgar.")

def g_alergenos():
    it = [("Huevo", "Huevo", "Bien cocinado"), ("Merluza", "Pescado", "Sin espinas"), ("bote", "Cacahuete y frutos secos", "En crema, nunca enteros"),
          ("Pan", "Gluten", "Pan, pasta, avena"), ("yogur", "Leche", "Yogur o queso fresco"), ("especias", "Sésamo", "Tahini, en hummus")]
    return tiles(it, "Los alérgenos más habituales y cómo ofrecerlos.", tone="si")

def g_alerg_pasos():
    it = [("Huevo", "De uno en uno", "Un alérgeno nuevo cada vez"), ("calendario", "Unos días seguidos", "Por ejemplo, 3 días"),
          ("cuchara", "Poca cantidad", "Y vas aumentando"), ("lupa", "Observa", "Piel, vómitos, hinchazón")]
    return tiles(it, "Cómo introducir un alérgeno, paso a paso.", num=True)

def g_hierro_fuentes():
    return groups([("Origen animal · se absorbe mejor", "g", [("carne", "Ternera"), ("Pollo", "Pollo"), ("Merluza", "Pescado"), ("Huevo", "Yema de huevo")]),
                   ("Origen vegetal", "o", [("Lentejas", "Lentejas"), ("garbanzos", "Garbanzos"), ("Guisantes", "Guisantes"), ("Avena", "Avena")])],
                  "Alimentos ricos en hierro, de origen animal y vegetal.")

def g_hierro_vitc():
    return eq([("Lentejas", "Hierro vegetal", "Lentejas, garbanzos, alubias"), ("Tomate", "Vitamina C", "Tomate, pimiento, kiwi, fresas"),
               ("estrella", "Se absorbe mejor", "Por ejemplo, lentejas con tomate")], "Hierro vegetal más vitamina C: se absorbe mejor.")

def g_pescado():
    si = [(FISH("#e8e2d0"), "Merluza, bacalao, lenguado"), (FISH("#f08a5d"), "Salmón y trucha"), (FISH("#7a93ad"), "Sardina, boquerón, caballa")]
    no = [(FISH("#6b7a8c", SWORD), "Pez espada o emperador"), (FISH("#8c98a4", SHARK_FIN), "Tiburón y cazón"), (FISH("#3e4c7a"), "Atún rojo"), (FISH("#6f8b2e"), "Lucio")]
    ch = lambda xs: "".join(f'<span>{_svg(b)}<i>{t}</i></span>' for b, t in xs)
    inner = (f'<div class="i2g"><div class="gr g"><b>Sí, 2-3 veces por semana</b><div class="ch">{ch(si)}</div></div>'
             f'<div class="gr t"><b>No hasta los 10 años · mucho mercurio</b><div class="ch">{ch(no)}</div></div></div>')
    return _figure(inner, "Alterna pescado blanco y azul, siempre bien cocinado y sin espinas.", "Qué pescados dar al bebé y cuáles evitar por el mercurio.")

def g_reparto():
    tu = f'<rect x="10" y="10" width="44" height="44" rx="10" fill="#fff" stroke="{LINE}" stroke-width="2"/>' + F("Brócoli", 12, 16, .4) + F("Merluza", 32, 14, .4) + F("Pera", 22, 32, .4)
    return _figure(f'<div class="vs"><div class="side main">{_svg(tu, cls="pic big")}<b>Tú decides</b><span>Qué se come, cuándo y dónde</span></div>'
                   f'<div class="plus">+</div><div class="side">{ic("bebe", "big")}<b>Tu bebé decide</b><span>Si come y cuánto</span></div></div>',
                   None, "Reparto de responsabilidades: tú decides qué, cuándo y dónde; tu bebé, si come y cuánto.")

def g_senales_hambre():
    return cmp(("Tiene hambre", ["Abre la boca al acercarle la comida", "Se inclina hacia delante", "Intenta coger el plato", "Se emociona al verlo"], "Ofrécele", "bebe"),
               ("Ya ha terminado", ["Cierra la boca o gira la cara", "Empuja la cuchara o el plato", "Tira o juega con la comida", "Se arquea o quiere bajar"], "Se acaba la comida, sin insistir", "bebe_triste"),
               "Señales de hambre y señales de que ya ha comido suficiente.")

def g_cortes_edad():
    return ages([(False, "mano_tira", "6 a 8 meses", "Tamaño dedo", "Tiras largas que asomen del puño"),
                 (True, "pinza", "9 a 12 meses", "Trocitos", "Del tamaño de un garbanzo, para la pinza"),
                 (False, "tenedor_bocado", "Desde 12 meses", "Bocados", "Casi como el resto de la familia")],
                "Cómo cortar la comida según la edad: tiras, trocitos y bocados.", caption="Siempre blando: que se aplaste entre tus dedos.")

def g_agua_no():
    return tiles([("vaso", "Agua", "Lo único que necesita", "si"), ("zumo", "Zumos", "Mejor la fruta entera", "no"),
                  ("infusion", "Infusiones con azúcar", None, "no"), ("bebida_veg", "Bebidas vegetales", "No sustituyen a la leche", "no")],
                 "Qué beber: agua sí; zumos, infusiones azucaradas y bebidas vegetales, no.")

SEMANA = [("Lun", "Lentejas", "Crema de lentejas", "Calabacín", "Tortilla en tiras"),
          ("Mar", "Merluza", "Merluza con patata", "Aguacate", "Tostada con hummus"),
          ("Mié", "carne", "Albóndigas", "Calabacín", "Crema con huevo"),
          ("Jue", "salmon", "Salmón al horno", "Avena", "Porridge con pera"),
          ("Vie", "pasta", "Boloñesa de lentejas", "Huevo", "Mini tortillas"),
          ("Sáb", "Pollo", "Arroz con pollo", "Lentejas", "Hamburguesitas"),
          ("Dom", "Merluza", "Nuggets de merluza", "Pan", "Pan con aguacate")]
def g_semana():
    li = "".join(f'<li><b>{d}</b><div>{ic(a)}<span><i>Comida</i>{x}</span></div><div>{ic(b)}<span><i>Cena</i>{y}</span></div></li>' for d, a, x, b, y in SEMANA)
    return _figure(f'<ol class="i2w">{li}</ol>', "Fruta de postre cada día, y la leche a demanda.", "Menú semanal ilustrado para un bebé de 7 a 9 meses.")

def g_causas():
    it = [("biberon", "No tiene hambre", "Quizá tomó leche hace poco"), ("diente", "Le salen los dientes", None),
          ("bebe_sueno", "Está cansado", None), ("repetir", "Es nuevo", "Necesita probarlo 8-15 veces"),
          ("mano_tira", "Quiere hacerlo él", "El rechazo es a la cuchara"), ("grumos", "La textura", "Demasiado fina o difícil")]
    return tiles(it, "Causas habituales de que un bebé no quiera comer.")

def g_ayuda():
    return cmp(("Sí ayuda", ["Comer juntos, a la mesa", "Ofrecer sin presionar", "Dejarle tocar y explorar", "Comidas de 20-30 minutos", "Volver a ofrecerlo otro día"], None, "familia"),
               ("No ayuda", ["Forzar o «una cucharada más»", "Pantallas y juguetes", "Premiar o castigar con postre", "Hacerle otro plato a la carta"], None, "pantalla"),
               "Qué ayuda y qué no cuando el bebé no quiere comer.")

def g_veg():
    it = [("b12", "Vitamina B12", "Suplemento siempre si es vegana"), ("Lentejas", "Hierro y zinc", "Legumbre en cada comida"),
          ("Huevo", "Proteína", "Huevo, legumbres, tofu"), ("bote", "Energía", "Cremas de frutos secos, aceite"),
          ("Almendra", "Omega 3", "Nueces o lino molidos"), ("yogur", "Calcio", "Lácteos o tofu con calcio"), ("sal", "Yodo", "Pregunta a tu pediatra")]
    return tiles(it, "Nutrientes a vigilar en una alimentación vegetariana del bebé.", caption="Con seguimiento de tu pediatra.")

def g_lacteos_edad():
    return ages([(False, "biberon", "Hasta los 12 meses", "Su leche", "Materna o de fórmula, a demanda"),
                 (True, "yogur", "Durante el primer año", "Yogur y queso", "Naturales, en poca cantidad"),
                 (False, "leche_vaca", "Desde 12 meses", "Leche de vaca", "Entera, como bebida")],
                "Cuándo dar yogur, queso y leche de vaca.", caption="El momento del yogur y el queso te lo dirá tu pediatra.")

def g_lacteos_cmp():
    return cmp(("Elige", ["Yogur natural sin azúcar, entero", "Queso fresco, requesón, mozzarella", "Pasteurizados y bajos en sal"], None, "yogur"),
               ("Evita", ["Quesos de leche cruda", "Quesos curados y muy salados", "Petit suisse, natillas y postres infantiles"], None, "queso"),
               "Qué lácteos elegir y cuáles evitar.")

def g_legumbres_edad():
    return ages([(False, "batidora", "6 meses", "En crema", "Pasadas por el pasapurés si dan gases"),
                 (True, "Pan", "BLW", "Untadas o en hamburguesitas", "Aplastadas en tostada, en albóndigas"),
                 (False, "garbanzos", "Con la pinza", "Aplastadas", "Garbanzos y alubias aplastados, nunca enteros")],
                "Cómo preparar las legumbres según la edad.")

def g_gases():
    return tiles([("reloj", "Remojo 8-12 h", "Y tira el agua"), ("olla", "Cocción larga", "Muy tiernas"), ("cuchara", "Poca cantidad", "Y ve aumentando"),
                  ("especias", "Comino o laurel", "En la cocción"), ("colador", "Si son de bote", "Lávalas bien")],
                 "Trucos para que las legumbres den menos gases.", num=True)

def g_gluten():
    return tiles([("Pan", "Pan", "Tostado, en tiras"), ("pasta", "Pasta", "Muy cocida"), ("cuscus", "Cuscús y sémola", None),
                  ("Avena", "Avena", "Salvo si es «sin gluten»"), ("harina", "Harina de trigo", "Tortitas, bizcochos")],
                 "Dónde está el gluten: pan, pasta, cuscús, avena y harina.", caption="Hacia los 6 meses, en poca cantidad y aumentando poco a poco.")

def g_estr_cmp():
    blanda = f'<ellipse cx="32" cy="40" rx="20" ry="11" fill="#c08a4a"/><ellipse cx="28" cy="36" rx="6" ry="2.4" fill="#d9a865"/>'
    bolas = "".join(f'<circle cx="{x}" cy="{y}" r="7" fill="#7a4f2a"/>' for x, y in [(20, 42), (34, 44), (27, 31), (44, 34)])
    return _figure('<div class="cmp">'
                   f'<div class="col ok">{_svg(blanda + SI(), cls="pic big")}<b class="h">Normal</b><ul><li>Más consistente y huele más</li><li>Cambia de color con lo que come</li><li>Algún trocito sin digerir</li></ul></div>'
                   f'<div class="col ko">{_svg(bolas + NO(), cls="pic big")}<b class="h">Estreñimiento</b><ul><li>Duras, en bolitas</li><li>Le duele o llora al hacerla</li><li>Mucha menos que antes</li></ul></div></div>',
                   None, "Cómo distinguir los cambios normales de las cacas del estreñimiento.")

def g_estr_ayuda():
    return tiles([("vaso", "Agua", "Con las comidas"), ("Ciruela", "Ciruela", None), ("Pera", "Pera", None), ("Kiwi", "Kiwi", None),
                  ("Lentejas", "Legumbres", None), ("Pan", "Integrales", None), ("aceite", "Aceite de oliva", None),
                  (_face(32, 22, 12) + f'<path d="M14 50l10-12h16l10 12" stroke="{GREEN}" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>', "Movimiento", "Tiempo en el suelo")],
                 "Qué ayuda con el estreñimiento: agua, fruta con fibra, legumbres, integrales, aceite y movimiento.", tone="si")

def g_batch_pasos():
    return tiles([("calendario", "Planifica", "4-5 bases para la semana"), ("horno", "Horno a la vez", "Verduras y albóndigas"),
                  ("olla", "Y el fuego", "Legumbres y cremas"), ("congelador", "Enfría y guarda", "En raciones pequeñas")],
                 "Cómo organizar una sesión de batch cooking.", num=True)

def g_batch_dura():
    return bars([("nevera", "Nevera", .07, "1-2 días, tapado"), ("congelador", "Congelador", 1, "Hasta 1 mes, con nombre y fecha"),
                 ("Arroz", "Arroz cocido", .035, "24 horas en la nevera, enfriado rápido")],
                "Cuánto dura la comida del bebé en la nevera y en el congelador.", caption="Descongela en la nevera y no vuelvas a congelar.")

def g_kit():
    return checklist([("babero", "Su babero"), ("pajita", "Su vaso"), ("cuchara", "Una cuchara"), ("plato", "Mantel de silicona"),
                      ("Plátano", "Algo de casa por si acaso"), ("panal", "Toallitas, muchas")],
                     "El kit para comer fuera de casa con un bebé.", title="Para la bolsa")

def g_transporte():
    return cmp(("Comida fría", ["Bolsa isotérmica con placas de hielo", "Como mucho 2 horas fuera de la nevera"], None, "nevera_portatil"),
               ("Comida caliente", ["Termo para alimentos", "Precaliéntalo con agua hirviendo"], None, "termo"),
               "Cómo transportar la comida del bebé: fría con hielo, caliente en termo.")

def g_etiqueta():
    ing = ["Harina de trigo integral", '<mark>azúcar</mark>', "aceite de girasol", '<mark>jarabe de glucosa</mark>', "leche en polvo",
           '<mark>dextrosa</mark>', "gasificante", "aroma de vainilla"]
    inner = (f'<div class="i2l"><div class="lab"><b>Galletas infantiles «desde 6 meses»</b><p><i>Ingredientes:</i> {", ".join(ing)}.</p></div>'
             f'<div class="ex"><span>{ic("lupa")}</span><p><b>3 nombres de azúcar</b> en un producto «infantil». La lista va de más a menos cantidad.</p></div></div>')
    return _figure(inner, None, "Ejemplo de etiqueta con varios nombres de azúcar marcados.")

def g_sodio():
    x = TXT(32, 42, "× 2,5", 17, TERRA)
    return _figure(f'<div class="vs i2e"><div class="side">{ic("etiqueta", "big")}<b>Sodio</b><span>Lo que pone la etiqueta</span></div>'
                   f'<div class="side">{_svg(x, cls="pic big")}<b>Multiplica</b><span>Por 2,5</span></div>'
                   f'<div class="plus">=</div><div class="side main">{ic("sal", "big")}<b>Sal</b><span>La cantidad real</span></div></div>',
                   None, "Para saber la sal, multiplica el sodio por 2,5.")

def g_guarde():
    return checklist([("olla", "¿Cocinan allí o es catering?"), ("sal", "¿Usan sal o azúcar?"), ("mano_tira", "¿Ofrecen trozos o solo purés?"),
                      ("trona", "¿Cómo se sientan a comer?"), ("bebe", "¿Qué hacen si no quiere comer?")],
                     "Preguntas para la escuela infantil sobre la comida.", title="Antes de empezar, pregunta")

def g_casa_escuela():
    return _figure(f'<div class="vs"><div class="side">{ic("escuela", "big")}<b>En la escuela</b><span>Carne o pescado a mediodía</span></div>'
                   f'<div class="plus">+</div><div class="side main">{ic("casa", "big")}<b>En casa</b><span>Cena con huevo o legumbre, y la verdura que falte</span></div></div>',
                   None, "La cena en casa completa lo que ha comido en la escuela.")

def g_dent():
    return cmp(("Le alivia", ["Comida fría de la nevera", "Polos de yogur y fruta", "Alimentos blandos", "Mordedor de la nevera"], None, "yogur"),
               ("No conviene", ["Collares de ámbar", "Geles anestésicos", "Galletas de dentición", "Fruta cruda dura"], None, "galleta"),
               "Qué alivia la dentición y qué no conviene.")

def g_cepillo():
    return _figure(f'<div class="wt">{ic("cepillo", "big")}<div><b>Desde el primer diente</b>'
                   f'<span>Dos veces al día, con pasta de 1.000 ppm de flúor, la cantidad de un grano de arroz.</span></div></div>',
                   None, "Cepillado desde el primer diente con pasta con flúor.")

def g_liquidos():
    return tiles([("biberon", "Pecho o biberón", "A demanda, más a menudo", "si"), ("vaso", "Agua", "En sorbos frecuentes", "si"),
                  ("suero", "Suero oral", "Si hay vómitos o diarrea", "si"), ("zumo", "Zumos y refrescos", None, "no"), ("olla", "Caldos de sobre", None, "no")],
                 "Qué darle de beber cuando está malito.")

def g_alarma():
    return tiles([("panal", "Moja muchos menos pañales"), ("gota", "Boca seca o llora sin lágrimas"), ("bebe_sueno", "Muy decaído o adormilado"),
                  ("bebe_malito", "Vomita todo lo que bebe"), ("termometro", "Fiebre en menores de 3 meses"), ("sangre", "Sangre en las heces")],
                 "Señales para ir a urgencias o llamar al 112.", tone="no", caption="Ante cualquiera de estas señales: urgencias o 112.")

def g_12_18():
    return cmp(("Cambia", ["La comida pasa a ser lo principal", "Leche de vaca entera", "Miel, poca", "Come lo mismo que la familia", "Poca sal, yodada"], None, "familia"),
               ("Sigue igual", ["Frutos secos: en crema hasta los 5", "Uvas y cherry en cuartos", "Sin pescados grandes", "Nada de borraja", "Azúcar y ultraprocesados, cuanto menos mejor"], None, "Uvas"),
               "Qué cambia y qué sigue igual en la alimentación después del año.")

def g_desayunos():
    it = [("Aguacate", "Tostada con aguacate"), ("garbanzos", "Tostada con hummus"), ("Huevo", "Huevo revuelto"), ("yogur", "Yogur con plátano"),
          ("Melocotón", "Fruta y queso fresco"), ("Plátano", "Plátano con crema de almendra"), ("Avena", "Porridge de avena"),
          ("sarten", "Tortitas de plátano"), ("Tomate", "Pan con tomate"), ("nevera", "Avena remojada"), ("bandeja", "Barritas de avena"), ("Manzana", "Bizcocho de manzana")]
    return tiles(it, "Doce ideas de desayuno sin azúcar para bebés.", num=True)

FIG = {
 "prohibidos": g_prohibidos, "consejos": g_consejos, "trona": g_trona, "baberos": g_baberos, "tres_formas": g_tres_formas,
 "textura": g_textura, "alergenos": g_alergenos, "alerg_pasos": g_alerg_pasos, "hierro_fuentes": g_hierro_fuentes,
 "hierro_vitc": g_hierro_vitc, "pescado": g_pescado, "reparto": g_reparto, "senales_hambre": g_senales_hambre,
 "cortes_edad": g_cortes_edad, "agua_no": g_agua_no, "semana": g_semana, "causas": g_causas, "ayuda": g_ayuda,
 "veg": g_veg, "lacteos_edad": g_lacteos_edad, "lacteos_cmp": g_lacteos_cmp, "legumbres_edad": g_legumbres_edad,
 "gases": g_gases, "gluten": g_gluten, "estr_cmp": g_estr_cmp, "estr_ayuda": g_estr_ayuda, "batch_pasos": g_batch_pasos,
 "batch_dura": g_batch_dura, "kit": g_kit, "transporte": g_transporte, "etiqueta": g_etiqueta, "sodio": g_sodio,
 "guarde": g_guarde, "casa_escuela": g_casa_escuela, "dent": g_dent, "cepillo": g_cepillo, "liquidos": g_liquidos,
 "alarma": g_alarma, "12_18": g_12_18, "desayunos": g_desayunos,
}

# Dónde va cada figura: (slug, figura, sección). Sección = título del <h2> tras cuyo contenido se coloca; None = antes del primer <h2>.
# <!--il:...--> son figuras de illus.py.
ESPEC = [
 ("alimentos-prohibidos-bebe-antes-del-ano", "prohibidos", "La lista"),
 ("alimentos-prohibidos-bebe-antes-del-ano", "il:cortes", "¿Y los alérgenos?"),
 ("consejos-empezar-alimentacion-complementaria", "consejos", None),
 ("que-trona-elegir-bebe", "trona", None),
 ("baberos-y-accesorios-bebe-por-edad", "baberos", None),
 ("blw-o-pures-cuando-pasar-a-trozos", "tres_formas", "Las tres formas de empezar"),
 ("blw-o-pures-cuando-pasar-a-trozos", "textura", "La prueba fácil de la textura"),
 ("alergenos-bebe-como-introducirlos", "alergenos", "Los más habituales"),
 ("alergenos-bebe-como-introducirlos", "alerg_pasos", "Cómo introducirlos"),
 ("hierro-bebe-alimentos-ricos", "hierro_fuentes", "Dónde hay más hierro"),
 ("hierro-bebe-alimentos-ricos", "hierro_vitc", "Cómo ayudarle a absorberlo"),
 ("pescado-bebe-cual-y-cuando", "pescado", "Los que debes evitar"),
 ("cuanto-debe-comer-un-bebe", "reparto", "Un reparto que funciona"),
 ("cuanto-debe-comer-un-bebe", "senales_hambre", "Señales de que ya ha terminado"),
 ("como-cortar-alimentos-bebe-por-edad", "cortes_edad", None),
 ("como-cortar-alimentos-bebe-por-edad", "il:cortes", "Siempre, a cualquier edad"),
 ("agua-bebe-cuando-y-cuanta", "il:agua", "Desde que empieza a comer: con las comidas"),
 ("agua-bebe-cuando-y-cuanta", "agua_no", "Lo que no necesita"),
 ("menu-semanal-bebe-7-9-meses", "il:plato", "Cómo está pensado"),
 ("menu-semanal-bebe-7-9-meses", "semana", "El menú"),
 ("bebe-no-quiere-comer", "causas", "Causas muy habituales"),
 ("bebe-no-quiere-comer", "ayuda", "Qué no ayuda"),
 ("bebe-vegetariano-alimentacion-complementaria", "veg", None),
 ("lacteos-bebe-yogur-queso-leche-de-vaca", "lacteos_edad", None),
 ("lacteos-bebe-yogur-queso-leche-de-vaca", "lacteos_cmp", "Cuáles evitar"),
 ("legumbres-bebe-como-darlas", "legumbres_edad", "Cómo prepararlas según la edad"),
 ("legumbres-bebe-como-darlas", "gases", "Cómo evitar (un poco) los gases"),
 ("gluten-bebe-cuando-introducirlo", "gluten", "Dónde está el gluten"),
 ("estrenimiento-bebe-alimentacion-complementaria", "estr_cmp", "¿Cuándo es estreñimiento?"),
 ("estrenimiento-bebe-alimentacion-complementaria", "estr_ayuda", "Qué ayuda"),
 ("congelar-comida-bebe-batch-cooking", "batch_pasos", "Cómo organizarlo"),
 ("congelar-comida-bebe-batch-cooking", "batch_dura", "Cuánto dura"),
 ("comer-fuera-de-casa-con-bebe", "kit", "Lleva un pequeño kit"),
 ("comer-fuera-de-casa-con-bebe", "transporte", "Transportar comida con seguridad"),
 ("leer-etiquetas-alimentos-infantiles", "etiqueta", "El azúcar tiene muchos nombres"),
 ("leer-etiquetas-alimentos-infantiles", "sodio", "Y la sal"),
 ("comer-en-la-guarderia-bebe", "guarde", "Antes de empezar, pregunta"),
 ("comer-en-la-guarderia-bebe", "casa_escuela", "Completa en casa, no repitas"),
 ("denticion-bebe-que-darle-de-comer", "dent", "Lo que no conviene"),
 ("denticion-bebe-que-darle-de-comer", "cepillo", "A cepillar desde el primer diente"),
 ("bebe-enfermo-que-darle-de-comer", "liquidos", "Lo primero: líquidos"),
 ("bebe-enfermo-que-darle-de-comer", "alarma", "Cuándo ir al médico ya"),
 ("alimentacion-bebe-12-18-meses", "12_18", "Lo que sigue igual"),
 ("desayunos-rapidos-bebe", "desayunos", None),
]

def colocar(a):
    """Inserta en el cuerpo de una guía las marcas de sus figuras, según ESPEC."""
    body = a["body"]
    for slug, fig, sec in ESPEC:
        if slug != a["slug"]: continue
        mark = f"<!--{fig}-->" if fig.startswith("il:") else f"<!--il2:{fig}-->"
        if mark in body: continue
        if sec is None:
            i = body.find("<h2>")
        else:
            h = body.find(f"<h2>{sec}</h2>")
            assert h >= 0, (slug, sec)
            i = body.find("<h2>", h + 4)
            if i < 0: i = len(body)
        body = body[:i] + mark + "\n" + body[i:]
    a["body"] = body

def apply(body):
    for k, f in FIG.items():
        m = f"<!--il2:{k}-->"
        if m in body: body = body.replace(m, f())
    return body

# ---------------------------------------------------------------- recetas: libreta ilustrada
ING = [  # palabra clave → icono, nombre corto
 ("pan rallado", "Pan", "Pan rallado"), ("plátano", "Plátano", "Plátano"), ("huevo", "Huevo", "Huevo"), ("avena", "Avena", "Avena"),
 ("garbanzo", "garbanzos", "Garbanzos"), ("tahini", "bote", "Tahini"), ("limón", "limon", "Limón"), ("pan", "Pan", "Pan"),
 ("calabacín", "Calabacín", "Calabacín"), ("calabacines", "Calabacín", "Calabacín"), ("manzana", "Manzana", "Manzana"),
 ("aguacate", "Aguacate", "Aguacate"), ("lentejas", "Lentejas", "Lentejas"), ("calabaza", "Calabaza", "Calabaza"),
 ("zanahoria", "Zanahoria", "Zanahoria"), ("cebolla", "cebolla", "Cebolla"), ("ternera", "carne", "Ternera"),
 ("merluza", "Merluza", "Merluza"), ("patata", "Patata", "Patata"), ("pollo", "Pollo", "Pollo"), ("puerro", "Puerro", "Puerro"),
 ("boniato", "Boniato", "Boniato"), ("pera", "Pera", "Pera"), ("almendra", "bote", "Crema de almendra"), ("pasta", "pasta", "Pasta"),
 ("tomate", "Tomate", "Tomate"), ("brócoli", "Brócoli", "Brócoli"), ("verduras cocidas", "verduras", "Verduras"),
 ("pimiento", "Pimiento rojo", "Pimiento"), ("guisantes", "Guisantes", "Guisantes"), ("arroz", "Arroz", "Arroz"),
 ("yogur", "yogur", "Yogur"), ("fresas", "Fresas", "Fresas"), ("fruta", "Mango", "Fruta"), ("salmón", "salmon", "Salmón"),
 ("harina", "harina", "Harina"), ("cuscús", "cuscus", "Cuscús"), ("queso", "queso", "Queso"), ("arándanos", "Arándanos", "Arándanos"),
 ("aceite", "aceite", "Aceite"), ("canela", "canela", "Canela"), ("comino", "especias", "Comino"), ("pimentón", "especias", "Pimentón"),
 ("cúrcuma", "especias", "Cúrcuma"), ("ajo", "ajo", "Ajo"), ("perejil", "hierbas", "Perejil"), ("orégano", "hierbas", "Orégano"),
 ("eneldo", "hierbas", "Hierbas"), ("levadura", "levadura", "Levadura"), ("caldo", "olla", "Caldo"), ("agua", "gota", "Agua"),
]
MENOR = {"aceite", "canela", "especias", "ajo", "hierbas", "levadura", "gota", "olla", "limon"}

def _ing_icon(texto):
    t = texto.lower()
    for k, n, _ in ING:
        if re.search(r"(?<![a-záéíóúñ])" + re.escape(k), t): return n
    return "cuchara"

UT = [  # palabra clave en el paso → utensilio
 (r"precalienta|hornea|al horno|horno", "horno"), (r"congela", "congelador"), (r"tritura|tritúra", "batidora"),
 (r"sartén|saltea|por cada lado|cucharadas de masa", "sarten"), (r"remojo|lava |lava\b|escurre|enjuaga|colador", "colador"), (r"ralla", "rallador"),
 (r"aplasta|desmiga", "tenedor"), (r"cuece|cocina |cocínalas|vapor|olla|rehoga|dora |hierve|caldo", "olla"),
 (r"molde|desmolda", "molde"), (r"forma |forma$|bandeja|colócalos|colócala|coloca", "bandeja"),
 (r"corta|trocea|pica |pela|quítale|quita ", "cuchillo"), (r"templ|enfri|sirve|reposar|reposa", "servir"),
 (r"nevera|noche antes", "nevera"), (r"mezcla|bate|añade|incorpora|vierte|reparte|pon ", "bol"),
]

VERBO = {  # primer verbo del paso → utensilio
 "aplasta": "tenedor", "desmiga": "tenedor", "suelta": "tenedor", "unta": "tenedor",
 "añade": "bol", "mezcla": "bol", "mézclalos": "bol", "bate": "bol", "incorpora": "bol", "vierte": "bol",
 "tritura": "batidora", "ralla": "rallador", "lava": "colador", "pela": "cuchillo", "pica": "cuchillo",
 "trocea": "cuchillo", "corta": "cuchillo", "saca": "cuchillo", "tuesta": "cuchillo",
 "cuece": "olla", "rehoga": "sarten", "rehógalos": "sarten", "dora": "sarten", "cuaja": "sarten", "calienta": "sarten",
 "precalienta": "horno", "hornea": "horno", "píntalas": "horno", "píntalos": "horno", "ponlos": "horno",
 "forma": "bandeja", "colócalos": "bandeja", "colócala": "bandeja", "congela": "congelador",
 "extiende": "molde", "reparte": "molde", "comprueba": "servir", "deja": "servir", "antes": "molde",
}
def _paso_pic(texto, ings):
    t = texto.lower()
    v = re.match(r"[a-záéíóúñ]+", t)
    tool = VERBO.get(v.group(0)) if v else None
    if t.startswith("pon cucharadas"): tool = "sarten"
    if t.startswith("pon todo") or t.startswith("pon la avena"): tool = "olla"
    if t.startswith("la noche antes"): tool = "colador"
    if tool == "servir" and "desmoldar" in t: tool = "molde"
    tool = tool or next((n for pat, n in UT if re.search(pat, t)), "bol")
    found = []
    for k, n, _ in ING:
        if n in MENOR or n == tool or k == "fruta": continue
        if re.search(r"(?<![a-záéíóúñ])" + re.escape(k), t) and n not in found: found.append(n)
    found = found[:2]
    temp = re.search(r"(\d{3}) °C", texto)
    if not found and not (tool == "horno" and temp):
        found = [n for n in ings if n not in MENOR][:1]
    body = f'<g transform="translate(0 4) scale(.9)">{P[tool]()}</g>'
    if not found and temp:
        body += (f'<circle cx="75" cy="20" r="18" fill="{TERRA}"/>' + TXT(75, 24, temp.group(1) + "°", 12, "#fff"))
    for i, n in enumerate(found):
        cx, cy = 77, (33 if len(found) == 1 else 17 + i * 32)
        body += f'<circle cx="{cx}" cy="{cy}" r="15.5" fill="#fff" stroke="{LINE}" stroke-width="1.5"/>'
        body += (f'<g transform="translate({cx-13} {cy-13}) scale(.406)">{P[n]()}</g>' if n in P else F(n, cx - 13, cy - 13, .406))
    return _svg(body, vb="0 0 96 66", cls="sc")

def _corto(paso):
    s = re.split(r"(?<=[.:;])\s|,\s(?=[a-záéíóú])| y (?=[a-záéíóú]+[ae]\b)", paso)[0].rstrip(".")
    return s

def receta(a):
    body = a["body"]
    i, j = body.find("<h2>Ingredientes</h2>"), body.find("<h2>Conservar</h2>")
    if i < 0 or j < 0: return body
    ings = [_ing_icon(x) for x in a["ing"]]
    li = "".join(f'<li><span class="bx"></span>{_svg(P[n]() if n in P else F(n, 2, 2, .94), cls="ii")}<span>{x}</span></li>' for n, x in zip(ings, a["ing"]))
    pasos = "".join(f'<li><span class="nn">{k}</span>{_paso_pic(p, ings)}<p>{p}</p></li>' for k, p in enumerate(a["steps"], 1))
    serve = []
    for k, s in enumerate(a["serve"]):
        lab = re.sub(r"<[^>]+>", "", s.split("</strong>")[0]).rstrip(":") if "</strong>" in s else ""
        txt = s.split("</strong>", 1)[1].strip() if "</strong>" in s else s
        n = "mano_tira" if re.search(r"\b6\b|6-", lab) else "pinza" if re.search(r"9", lab) else "tenedor_bocado"
        serve.append(f'<div class="pi p{k%2}">{ic(n)}<b>{lab}</b><span>{txt}</span></div>')
    # pastillas con iconos
    mini = lambda body: _svg(body, cls="mi")
    pills = [(P["bebe"](), a["age"]), (P["cuchillo"](), f'Preparación {a["prep"]} min')]
    if a["cook"]: pills.append((P["horno"]() if re.search(r"horno|hornea", " ".join(a["steps"]).lower()) else P["sarten"]() if "sartén" in " ".join(a["steps"]).lower() else P["olla"]() if any(w in " ".join(a["steps"]).lower() for w in ("cuece", "olla", "cazo")) else P["reloj"](), f'Cocción {a["cook"]} min'))
    else: pills.append((P["reloj"](), "Sin cocción"))
    pills.append((P["servir"](), a["yld"]))
    nueva = '<div class="pills pi2">' + "".join(f"<span>{mini(b)}{t}</span>" for b, t in pills) + "</div>"
    k = body.find('<div class="pills">')
    if k >= 0:
        body = body[:k] + nueva + body[body.find("</div>", k) + 6:]
    ALG = {"Huevo": "Huevo", "Gluten": "Pan", "Leche": "yogur", "Pescado": "Merluza", "Sésamo": "especias", "Frutos secos": "Almendra"}
    def alg_ic(x):
        n = next((v for k2, v in ALG.items() if x.startswith(k2)), None)
        return (mini(P[n]() if n in P else F(n, 2, 2, .94)) if n else "") + x
    k = body.find('<p class="alg">')
    if k >= 0 and a["alg"]:
        body = body[:k] + '<p class="alg alg2"><strong>Alérgenos:</strong> ' + "".join(f"<span>{alg_ic(x)}</span>" for x in a["alg"]) + "</p>" + body[body.find("</p>", k) + 4:]
    i, j = body.find("<h2>Ingredientes</h2>"), body.find("<h2>Conservar</h2>")
    nb = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&display=swap">'
          '<section class="nb"><span class="tape t1"></span><span class="tape t2"></span>'
          f'<h2>Ingredientes</h2><ul class="nb-ing">{li}</ul></section>'
          f'<h2 class="nbh">Paso a paso</h2><ol class="nb-steps">{pasos}</ol>'
          f'<h2 class="nbh">Cómo servirlo según la edad</h2><div class="nb-serve">{"".join(serve)}</div>')
    return body[:i] + nb + body[j:]

CSS = r"""
/* ilustraciones 2 */
.i2t{display:flex!important;flex-wrap:wrap;justify-content:center}.i2t li{flex:0 0 calc(25% - 9px)}.i2t.c3 li{flex-basis:calc(33.333% - 8px)}.i2t.c5 li{flex-basis:calc(20% - 10px);padding-left:6px;padding-right:6px}
.i2t li{display:flex;flex-direction:column;align-items:center}
.i2t li .s{display:block;font-weight:500;color:var(--mute);font-size:.78rem;line-height:1.35;margin-top:4px}
.i2t.no li{border-top:5px solid var(--terra)}.i2t.si li{border-top:5px solid var(--green)}
.i2a2{grid-template-columns:repeat(2,1fr)!important}.i2a4{grid-template-columns:repeat(4,1fr)!important}
.cmp .col .pic{margin:0 auto 6px}
.i2g{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px}
.i2g .gr{background:#fff;border-radius:20px;padding:16px;border-top:6px solid var(--green)}
.i2g .gr.t{border-top-color:var(--terra)}.i2g .gr.o{border-top-color:var(--gold)}
.i2g b{display:block;text-align:center;font-size:.92rem;margin:0 0 10px}.i2g .g b{color:var(--green)}.i2g .t b{color:var(--terra)}.i2g .o b{color:#a5781e}
.i2g .ch{display:grid;grid-template-columns:repeat(auto-fit,minmax(78px,1fr));gap:8px}
.i2g .ch span{display:flex;flex-direction:column;align-items:center;gap:2px;font-size:.78rem;color:var(--mute);font-weight:600;text-align:center;line-height:1.3}
.i2g .ch svg{width:50px;height:50px;margin:0}.i2g i{font-style:normal}
.i2e{flex-wrap:wrap}.i2e .side{min-width:130px}
.wt b{font-size:1.05rem}
.i2ct{display:block;text-align:center;color:var(--green);margin:0 0 12px}
.i2c{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:8px}
.i2c li{display:flex;align-items:center;gap:12px;background:#fff;border-radius:14px;padding:8px 14px;font-weight:600;font-size:.9rem;line-height:1.35}
.i2c .pic{width:42px;height:42px;margin:0;flex:none}
.i2b li{display:flex;align-items:center;gap:14px;background:#fff;border-radius:16px;padding:12px 16px;margin:0 0 8px}
.i2b .pic{width:46px;height:46px;margin:0;flex:none}.i2b div{flex:1}
.i2b b{display:block;font-size:.95rem}.i2b .s{display:block;color:var(--mute);font-size:.82rem;line-height:1.35}
.i2b .bar{display:block;height:12px;border-radius:6px;background:#eeead8;margin:6px 0 4px;overflow:hidden}
.i2b .bar i{display:block;height:100%;min-width:12px;border-radius:6px;background:var(--green)}
.i2w{display:grid;grid-template-columns:repeat(7,1fr);gap:8px}
.i2w li{background:#fff;border-radius:16px;padding:12px 8px;text-align:center;display:flex;flex-direction:column;gap:8px}
.i2w li>b{color:var(--terra);font-size:.85rem;text-transform:uppercase;letter-spacing:.06em}
.i2w li div{display:flex;flex-direction:column;align-items:center;gap:2px}
.i2w .pic{width:44px;height:44px;margin:0}
.i2w span{font-size:.75rem;line-height:1.3;font-weight:600}.i2w span i{display:block;font-style:normal;color:var(--mute);font-weight:500;font-size:.68rem;text-transform:uppercase;letter-spacing:.05em}
.i2l{display:grid;grid-template-columns:1.4fr 1fr;gap:12px;align-items:center}
.i2l .lab{background:#fff;border-radius:14px;padding:16px 18px;border:2px dashed var(--line);font-size:.88rem;line-height:1.5}
.i2l .lab b{display:block;margin:0 0 6px}.i2l .lab p{margin:0}
.i2l mark{background:#f6d8cb;color:#a24f30;font-weight:800;border-radius:4px;padding:0 3px}
.i2l .ex{display:flex;gap:10px;align-items:center}.i2l .ex .pic{width:56px;height:56px;margin:0;flex:none}.i2l .ex p{margin:0;font-size:.9rem;line-height:1.45}
/* recetas: pastillas con iconos */
.pi2 span{display:inline-flex;align-items:center;gap:8px;padding:6px 16px 6px 8px!important}
.pi2 .mi,.alg2 .mi{width:28px;height:28px;flex:none;overflow:visible}
.alg2{display:flex;flex-wrap:wrap;align-items:center;gap:6px 12px}
.alg2 span{display:inline-flex;align-items:center;gap:6px;color:var(--ink);font-weight:600}
.alg2 .mi{width:24px;height:24px}
/* recetas: libreta */
.nb{position:relative;margin:34px 0 10px;padding:30px 22px 22px 64px;background-color:#fffdf6;
 background-image:linear-gradient(90deg,transparent 46px,#f2b1a6 46px,#f2b1a6 48px,transparent 48px),repeating-linear-gradient(transparent 0 39px,#d6e6f2 39px 40px),radial-gradient(circle at 20px 22px,var(--bg) 6px,transparent 7px);
 background-size:100% 100%,100% 40px,100% 40px;border-radius:6px 20px 20px 6px;box-shadow:0 2px 0 #e6dfca,0 14px 30px rgba(0,0,0,.07);transform:rotate(-.4deg)}
.nb .tape{position:absolute;top:-12px;width:96px;height:26px;background:rgba(201,150,47,.32);border-left:2px dashed rgba(255,255,255,.5);border-right:2px dashed rgba(255,255,255,.5)}
.nb .t1{left:18%;transform:rotate(-4deg)}.nb .t2{right:12%;transform:rotate(5deg);background:rgba(74,135,96,.28)}
.nb h2,.nbh{font-family:Caveat,"Comic Sans MS",cursive!important;font-weight:700;font-size:2.3rem;line-height:1;color:var(--terra);margin:0 0 10px;letter-spacing:0}
.nbh{margin:44px 0 16px;color:var(--green)}
.nb-ing{list-style:none;margin:0;padding:0}
.nb-ing li{display:flex;align-items:center;gap:10px;min-height:40px;padding:0;margin:0;line-height:1.3;font-size:1.02rem}
.nb-ing li::marker{content:""}
.nb-ing .bx{flex:none;width:16px;height:16px;border:2px solid var(--ink);border-radius:4px;transform:rotate(-4deg)}
.nb-ing .ii{flex:none;width:40px;height:40px}
.nb-steps{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,1fr);gap:18px}
.nb-steps li{position:relative;margin:0;background:#fffdf6;border-radius:16px;padding:16px 16px 14px;box-shadow:0 2px 0 #e6dfca,0 8px 18px rgba(0,0,0,.05);border:1.5px solid #ece5cf}
.nb-steps li::marker{content:""}
.nb-steps li:nth-child(odd){transform:rotate(-.8deg)}.nb-steps li:nth-child(even){transform:rotate(.8deg)}
.nb-steps .nn{position:absolute;top:-12px;left:-8px;width:40px;height:40px;border-radius:50%;background:var(--terra);color:#fff;font:700 1.7rem/40px Caveat,cursive;text-align:center;box-shadow:0 3px 0 #a24f30}
.nb-steps .sc{display:block;width:100%;max-width:250px;height:auto;aspect-ratio:96/66;margin:4px auto 8px;overflow:visible}
.nb-steps p{margin:0;font-size:.95rem;line-height:1.5}
.nb-serve{display:grid;grid-template-columns:repeat(2,1fr);gap:18px}
.nb-serve .pi{padding:20px 18px 18px;border-radius:4px;box-shadow:0 10px 20px rgba(0,0,0,.08);text-align:center;display:flex;flex-direction:column;align-items:center;gap:4px}
.nb-serve .p0{background:#fbe7a6;transform:rotate(-1.5deg)}.nb-serve .p1{background:#d4ead2;transform:rotate(1.2deg)}
.nb-serve b{font:700 1.7rem/1.1 Caveat,cursive;color:var(--ink)}.nb-serve span{font-size:.92rem;line-height:1.45}
.nb-serve .pic{width:68px;height:68px;margin:0 0 4px}
@media(max-width:640px){
.i2t li,.i2t.c3 li,.i2t.c5 li{flex-basis:calc(50% - 6px)}
.i2w{grid-template-columns:1fr}.i2w li{display:grid;grid-template-columns:44px 1fr 1fr;align-items:center;text-align:left;padding:10px 12px}
.i2w li div{flex-direction:row;gap:8px;align-items:center}.i2w .pic{width:36px;height:36px}
.i2a2,.i2a4{grid-template-columns:1fr!important}
.i2l{grid-template-columns:1fr}
.nb{padding:26px 14px 18px 54px;transform:none;margin-left:-6px;margin-right:-6px}
.nb-steps,.nb-serve{grid-template-columns:1fr}
.nb-steps li{transform:none!important}
}
"""
