# Publica el siguiente borrador de la cola: pone la fecha de hoy, genera su página,
# actualiza el índice del blog y el sitemap. No toca las páginas ya publicadas.
# Después regenera /borradores/ (vista previa de lo pendiente, sin indexar).
#
# Uso (desde cualquier carpeta):
#   python3 _build/publicar_siguiente.py               publica el siguiente y regenera borradores
#   python3 _build/publicar_siguiente.py --borradores  solo regenera borradores
import os,re,sys,json,html,shutil,subprocess,tempfile,datetime
from zoneinfo import ZoneInfo

B=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(B)

# Orden de publicación, revisado con Martina el 7-11-2026. Uno cada dos días (días impares).
COLA=[
"alergenos-bebe-como-introducirlos","tortitas-platano-avena-bebe",
"consejos-empezar-alimentacion-complementaria","bastones-boniato-horno-bebe",
"alimentos-prohibidos-bebe-antes-del-ano","crema-lentejas-rojas-calabaza-bebe",
"blw-o-pures-cuando-pasar-a-trozos","hummus-sin-sal-bebe-tostada",
"hierro-bebe-alimentos-ricos","albondigas-ternera-calabacin-horno-bebe",
"como-cortar-alimentos-bebe-por-edad","tortilla-calabacin-tiras-bebe",
"pescado-bebe-cual-y-cuando","nuggets-merluza-horno-bebe",
"cuanto-debe-comer-un-bebe","pan-aguacate-huevo-bebe",
"agua-bebe-cuando-y-cuanta","hamburguesitas-lentejas-bebe",
"menu-semanal-bebe-7-9-meses","muffins-calabacin-manzana-bebe",
"que-trona-elegir-bebe","crema-calabacin-pollo-bebe",
"bebe-no-quiere-comer","porridge-avena-pera-bebe",
"baberos-y-accesorios-bebe-por-edad","barritas-avena-platano-horno-bebe",
"legumbres-bebe-como-darlas","pasta-bolonesa-lentejas-bebe",
"gluten-bebe-cuando-introducirlo","mini-tortillas-horno-verduras-bebe",
"lacteos-bebe-yogur-queso-leche-de-vaca","arroz-meloso-pollo-verduras-bebe",
"bebe-vegetariano-alimentacion-complementaria","salmon-horno-patata-brocoli-bebe",
"estrenimiento-bebe-alimentacion-complementaria","bizcocho-manzana-sin-azucar-bebe",
"congelar-comida-bebe-batch-cooking","cuscus-verduras-garbanzos-bebe",
"comer-fuera-de-casa-con-bebe","polos-yogur-fruta-bebe",
"leer-etiquetas-alimentos-infantiles","manzana-pera-asadas-canela-bebe",
"comer-en-la-guarderia-bebe","tarta-primer-cumpleanos-sin-azucar",
"denticion-bebe-que-darle-de-comer","bebe-enfermo-que-darle-de-comer",
"alimentacion-bebe-12-18-meses","desayunos-rapidos-bebe",
]
FUENTES=["articles.py","guides2.py","recipes.py","guides3.py","recipes2.py","guides4.py"]
BASE="https://www.primerosalimentos.com"
MESES=["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"]
fecha=lambda d:f"{d.day} de {MESES[d.month-1]}"

def publicados():
    return sorted(d for d in os.listdir(f"{ROOT}/blog") if os.path.isfile(f"{ROOT}/blog/{d}/index.html"))

def poner_fecha(carpeta,slug,dia):
    for f in FUENTES:
        p=f"{carpeta}/{f}"; s=open(p).read()
        s2,n=re.subn(r'(slug="%s".*?date=")\d{4}-\d{2}-\d{2}(")'%re.escape(slug),r'\g<1>%s\g<2>'%dia,s,count=1,flags=re.S)
        if n: open(p,"w").write(s2); return
    sys.exit(f"ERROR: no encuentro {slug} en {FUENTES}")

def construir(carpeta,pub):
    for j in ["foods2.json","extra.json","pdfic.json"]: shutil.copy(f"{carpeta}/{j}",f"/tmp/{j}")
    out=tempfile.mkdtemp()
    subprocess.run([sys.executable,"build_site.py"],cwd=carpeta,env=dict(os.environ,OUT=out,PUB=",".join(pub)),check=True,stdout=subprocess.DEVNULL)
    return out

def calendario(n,hoy,ultimo):
    # Mismo ritmo que la tarea programada: días impares, nunca dos días seguidos.
    d=hoy+datetime.timedelta(1); res=[]
    while len(res)<n:
        if d.day%2==1 and not(ultimo and (d-ultimo).days==1): res.append(d); ultimo=d
        d+=datetime.timedelta(1)
    return res

def borradores(hoy,publicado_hoy):
    pub=publicados(); pend=[s for s in COLA if s not in pub]
    dest=f"{ROOT}/borradores"; shutil.rmtree(dest,ignore_errors=True); os.makedirs(dest)
    fechas=calendario(len(pend),hoy,hoy if publicado_hoy else None)
    tmp=tempfile.mkdtemp(); shutil.copytree(B,f"{tmp}/b",ignore=shutil.ignore_patterns("__pycache__"))
    for s,d in zip(pend,fechas): poner_fecha(f"{tmp}/b",s,d.isoformat())
    out=construir(f"{tmp}/b",pub+pend) if pend else None
    sys.path.insert(0,f"{tmp}/b"); import importlib
    info={}
    for m,vs in [("articles",["ARTICLES"]),("guides2",["G2"]),("recipes",["R"]),("guides3",["G3"]),("recipes2",["R2"]),("guides4",["G4","R3"])]:
        mod=importlib.import_module(m)
        for v in vs:
            for a in getattr(mod,v): info[a['slug']]={**a,"cat":a.get("cat","guia")}
    for i,(s,d) in enumerate(zip(pend,fechas),1):
        t=open(f"{out}/blog/{s}/index.html").read()
        for o in pend: t=t.replace(f'{BASE}/blog/{o}/',f'{BASE}/borradores/{o}/')
        t=t.replace('<head>','<head><meta name="robots" content="noindex,nofollow">',1)
        t=re.sub(r'<link rel="canonical"[^>]*>','',t)
        aviso=(f'<div style="background:#c96a47;color:#fff;font:700 15px/1.4 Montserrat,sans-serif;padding:12px 16px;text-align:center">'
               f'Borrador · nº {i} de la cola · se publica el {fecha(d)} · <a style="color:#fff" href="{BASE}/borradores/">ver todos</a></div>')
        t=re.sub(r'(<body[^>]*>)',r'\1'+aviso,t,count=1)
        os.makedirs(f"{dest}/{s}"); open(f"{dest}/{s}/index.html","w").write(t)
    filas="".join(f'<li><span>{fecha(d)}</span><a href="{s}/">{html.escape(info[s]["title"])}</a><em>{"Receta" if info[s]["cat"]=="receta" else "Guía"}</em></li>' for s,d in zip(pend,fechas))
    open(f"{dest}/index.html","w").write(f'''<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>Borradores del blog · Primeros Alimentos</title>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;800&display=swap" rel="stylesheet">
<style>body{{margin:0;background:#eeead8;color:#262626;font:400 17px/1.6 Montserrat,system-ui,sans-serif}}main{{width:min(760px,100% - 32px);margin:0 auto;padding:40px 0 80px}}
h1{{font-size:1.8rem;margin:0 0 6px}}p{{color:#6b6a5c;margin:0 0 28px}}ol{{list-style:none;padding:0;margin:0;border-top:1px solid #d8d3bc}}
li{{display:grid;grid-template-columns:110px 1fr auto;gap:12px;align-items:baseline;padding:12px 0;border-bottom:1px solid #d8d3bc}}
li span{{font-weight:700;color:#c96a47;font-size:.9rem}}li a{{color:#262626;font-weight:600}}li em{{font-style:normal;font-size:.8rem;color:#4a8760;font-weight:700}}
@media(max-width:560px){{li{{grid-template-columns:1fr}}}}</style></head><body><main>
<h1>Borradores del blog</h1><p>{len(pend)} artículos en cola. Se publica uno cada dos días. Esta página no aparece en Google ni está enlazada desde la web.</p>
<ol>{filas}</ol></main></body></html>''')
    return pend

hoy=datetime.datetime.now(ZoneInfo("Europe/Madrid")).date()
if "--borradores" in sys.argv:
    print(f"Borradores: {len(borradores(hoy,False))}"); sys.exit(0)

pend=[s for s in COLA if s not in publicados()]
if not pend: print("NADA: la cola está vacía"); borradores(hoy,False); sys.exit(0)
slug=pend[0]

# 1. Fecha de hoy en el borrador
poner_fecha(B,slug,hoy.isoformat())
# 2. Generar (solo lo publicado + el nuevo)
out=construir(B,publicados()+[slug])
# 3. Copiar solo la página nueva, el índice del blog y el sitemap
shutil.copytree(f"{out}/blog/{slug}",f"{ROOT}/blog/{slug}",dirs_exist_ok=True)
shutil.copy(f"{out}/blog/index.html",f"{ROOT}/blog/index.html")
shutil.copy(f"{out}/sitemap.xml",f"{ROOT}/sitemap.xml")
# 4. Borradores al día
borradores(hoy,True)
print(f"PUBLICADO: {slug} ({hoy}). Quedan {len(pend)-1}.")
