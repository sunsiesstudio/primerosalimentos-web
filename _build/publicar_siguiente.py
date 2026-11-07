# Publica el siguiente borrador de la cola: pone la fecha de hoy, genera su página,
# actualiza el índice del blog y el sitemap. No toca las páginas ya publicadas.
# Uso: python3 _build/publicar_siguiente.py   (desde cualquier carpeta)
import os,re,sys,shutil,subprocess,tempfile,datetime
from zoneinfo import ZoneInfo

B=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(B)

# Orden de publicación: guía, receta, guía, receta...
COLA=[
"hierro-bebe-alimentos-ricos","crema-lentejas-rojas-calabaza-bebe",
"pescado-bebe-cual-y-cuando","albondigas-ternera-calabacin-horno-bebe",
"cuanto-debe-comer-un-bebe","nuggets-merluza-horno-bebe",
"como-cortar-alimentos-bebe-por-edad","hamburguesitas-lentejas-bebe",
"agua-bebe-cuando-y-cuanta","crema-calabacin-pollo-bebe",
"menu-semanal-bebe-7-9-meses","bastones-boniato-horno-bebe",
"bebe-no-quiere-comer","porridge-avena-pera-bebe",
"bebe-vegetariano-alimentacion-complementaria","pasta-bolonesa-lentejas-bebe",
"lacteos-bebe-yogur-queso-leche-de-vaca","mini-tortillas-horno-verduras-bebe",
"legumbres-bebe-como-darlas","arroz-meloso-pollo-verduras-bebe",
"gluten-bebe-cuando-introducirlo","polos-yogur-fruta-bebe",
"estrenimiento-bebe-alimentacion-complementaria","salmon-horno-patata-brocoli-bebe",
"congelar-comida-bebe-batch-cooking","bizcocho-manzana-sin-azucar-bebe",
"comer-fuera-de-casa-con-bebe","cuscus-verduras-garbanzos-bebe",
"leer-etiquetas-alimentos-infantiles","manzana-pera-asadas-canela-bebe",
]
FUENTES=["guides3.py","recipes2.py"]

publicados=sorted(d for d in os.listdir(f"{ROOT}/blog") if os.path.isfile(f"{ROOT}/blog/{d}/index.html"))
pendientes=[s for s in COLA if s not in publicados]
if not pendientes: print("NADA: la cola está vacía"); sys.exit(0)
slug=pendientes[0]
hoy=datetime.datetime.now(ZoneInfo("Europe/Madrid")).date().isoformat()

# 1. Fecha de hoy en el borrador
for f in FUENTES:
    p=f"{B}/{f}"; s=open(p).read()
    s2,n=re.subn(r'(slug="%s".*?date=")\d{4}-\d{2}-\d{2}(")'%re.escape(slug),r'\g<1>%s\g<2>'%hoy,s,count=1,flags=re.S)
    if n: open(p,"w").write(s2); break
else: sys.exit(f"ERROR: no encuentro {slug} en {FUENTES}")

# 2. Generar (solo lo publicado + el nuevo)
for j in ["foods2.json","extra.json","pdfic.json"]: shutil.copy(f"{B}/{j}",f"/tmp/{j}")
out=tempfile.mkdtemp()
env=dict(os.environ,OUT=out,PUB=",".join(publicados+[slug]))
subprocess.run([sys.executable,"build_site.py"],cwd=B,env=env,check=True)

# 3. Copiar solo la página nueva, el índice del blog y el sitemap
shutil.copytree(f"{out}/blog/{slug}",f"{ROOT}/blog/{slug}",dirs_exist_ok=True)
shutil.copy(f"{out}/blog/index.html",f"{ROOT}/blog/index.html")
shutil.copy(f"{out}/sitemap.xml",f"{ROOT}/sitemap.xml")
print(f"PUBLICADO: {slug} ({hoy}). Quedan {len(pendientes)-1}.")
