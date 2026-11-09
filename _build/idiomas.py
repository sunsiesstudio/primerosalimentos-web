# Blog en catalán e inglés.
#
# El blog se escribe y se publica en castellano (build_site.py y publicar_siguiente.py).
# Este script crea las versiones /ca/blog/ y /en/blog/ a partir de las páginas ya publicadas
# y de las traducciones guardadas en _build/traducciones/<idioma>/<slug>.json
# (y _comun.json para los textos que se repiten en todas las páginas).
#
# Uso:
#   python3 _build/idiomas.py pendientes        lista los textos que faltan por traducir (JSON)
#   python3 _build/idiomas.py                   genera /ca/blog y /en/blog, pone el selector de idioma
#                                               y los hreflang en todas las páginas y rehace el sitemap
#
# Un artículo solo sale en un idioma si tiene TODOS sus textos traducidos; si no, se avisa.
import os,re,sys,json,html,glob

B=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(B)
BASE="https://www.primerosalimentos.com"
LANGS=["ca","en"]
NOMBRE={"es":"Español","ca":"Català","en":"English"}
LOCALE={"es":"es_ES","ca":"ca_ES","en":"en_GB"}
INLANG={"es":"es-ES","ca":"ca-ES","en":"en"}
MESES={"es":["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"],
       "ca":["gener","febrer","març","abril","maig","juny","juliol","agost","setembre","octubre","novembre","desembre"],
       "en":["January","February","March","April","May","June","July","August","September","October","November","December"]}
TR_DIR=f"{B}/traducciones"
MARK="<!--idiomas-->"

def fecha(l,d,m,y):
    if l=="ca":
        mes=MESES["ca"][m-1]; return f"{d} {'d’' if mes[0] in 'ao' else 'de '}{mes} de {y}"
    if l=="en": return f"{d} {MESES['en'][m-1]} {y}"
    return f"{d} de {MESES['es'][m-1]} de {y}"
RE_FECHA=re.compile(r"(\d{1,2}) de ("+"|".join(MESES["es"])+r") de (\d{4})")
RE_MINS=re.compile(r"(\d+) min de lectura")
MINS={"ca":"{} min de lectura","en":"{} min read"}

def publicados(): return sorted(os.path.basename(os.path.dirname(p)) for p in glob.glob(f"{ROOT}/blog/*/index.html"))

# ---------- trocear el HTML en textos traducibles ----------
TAG=re.compile(r"(<!--.*?-->|<script\b.*?</script>|<style\b.*?</style>|<[^>]+>)",re.S)
ATTR=re.compile(r'\b(alt|aria-label|title)="([^"]*)"')
def norm(t): return re.sub(r"\s+"," ",t).strip()

def piezas(s):
    """Devuelve la lista de trozos y, para cada texto, su clave normalizada."""
    out=[]
    for tok in TAG.split(s):
        if not tok: continue
        out.append(tok)
    return out

def es_texto(tok): return not tok.startswith("<")
def traducible(t):
    k=norm(t)
    if not k or not re.search(r"[A-Za-zÀ-ÿ]",k): return None
    if re.fullmatch(r"[\d\s·/|&;#a-z]*",k) and len(k)<4: return None
    return k

def ld_textos(obj,acc):
    if isinstance(obj,dict):
        for k,v in obj.items():
            if k in("headline","description","name","text","recipeCategory","recipeCuisine","keywords","recipeYield") and isinstance(v,str): acc.append(v)
            elif k in("recipeIngredient",) and isinstance(v,list): acc.extend(x for x in v if isinstance(x,str))
            else: ld_textos(v,acc)
    elif isinstance(obj,list):
        for x in obj: ld_textos(x,acc)
def ld_traducir(obj,f):
    if isinstance(obj,dict):
        for k,v in list(obj.items()):
            if k in("headline","description","name","text","recipeCategory","recipeCuisine","keywords","recipeYield") and isinstance(v,str): obj[k]=f(v)
            elif k=="recipeIngredient" and isinstance(v,list): obj[k]=[f(x) if isinstance(x,str) else x for x in v]
            elif k=="inLanguage": pass
            else: ld_traducir(v,f)
    elif isinstance(obj,list):
        for x in obj: ld_traducir(x,f)

def textos(s):
    """Todos los textos de una página que hay que traducir."""
    acc=[]
    for tok in piezas(s):
        if tok.startswith("<script") and "application/ld+json" in tok:
            j=json.loads(tok[tok.index(">")+1:tok.rindex("</script>")]); l=[]; ld_textos(j,l); acc+= [norm(x) for x in l]
        elif tok.startswith("<meta") and re.search(r'(name="description"|property="og:(title|description)")',tok):
            m=re.search(r'content="([^"]*)"',tok); acc.append(norm(html.unescape(m.group(1))))
        elif tok.startswith("<") and not tok.startswith(("<script","<style","<!--")):
            for _,v in ATTR.findall(tok):
                k=traducible(html.unescape(v))
                if k and v not in("Primeros alimentos","Primeros Alimentos"): acc.append(k)
        elif es_texto(tok):
            k=traducible(tok)
            if k: acc.append(k)
    out=[]
    for k in acc:
        k2=RE_MINS.sub("§MINS§",RE_FECHA.sub("§FECHA§",k))
        if k2 not in out and k2 not in("§FECHA§",): out.append(k2)
    return [k for k in out if k not in IGNORAR]

IGNORAR={"Primeros alimentos","Primeros Alimentos","Blog","Instagram","Cookies","BLW","Martina Solés","AEP","/","·"}

def cargar(l,slug):
    p=f"{TR_DIR}/{l}/{slug}.json"
    return json.load(open(p,encoding="utf-8")) if os.path.exists(p) else {}

def dic(l,slug):
    d={}; d.update(cargar(l,"_comun")); d.update(cargar(l,slug)); return d

def falta(l,slug,s):
    s=re.sub(r'<!--idiomas-->.*?<!--/idiomas-->','',s,flags=re.S)
    d=dic(l,slug); return [k for k in textos(s) if k not in d and not re.fullmatch(r"(Por )?Martina Solés · §FECHA§ · §MINS§|§MINS§",k)]

def traducir_texto(l,d,t):
    """Traduce un texto manteniendo los espacios de alrededor."""
    k=traducible(t)
    if not k: return t
    pre=t[:len(t)-len(t.lstrip())]; post=t[len(t.rstrip()):]
    v=tr(l,d,k)
    if v.endswith(("'","’")): post=""  # «de l'» + enlace: sin espacio
    return pre+v+post

def tr(l,d,k):
    k=norm(k)
    m=RE_FECHA.search(k); fe=None
    if m: fe=fecha(l,int(m.group(1)),MESES["es"].index(m.group(2))+1,int(m.group(3)))
    mm=RE_MINS.search(k); mi=MINS[l].format(mm.group(1)) if mm else None
    kk=RE_MINS.sub("§MINS§",RE_FECHA.sub("§FECHA§",k))
    if kk in IGNORAR: return k
    if kk in d: v=d[kk]
    elif kk=="§MINS§": v="§MINS§"
    elif kk=="Por Martina Solés · §FECHA§ · §MINS§": v={"ca":"Per Martina Solés · §FECHA§ · §MINS§","en":"By Martina Solés · §FECHA§ · §MINS§"}[l]
    else: raise KeyError(kk)
    if fe: v=v.replace("§FECHA§",fe)
    if mi: v=v.replace("§MINS§",mi)
    return v

# ---------- enlaces, idioma y selector ----------
def url_de(l,slug=None):
    p="/blog/"+(f"{slug}/" if slug else "")
    return f"{BASE}{p}" if l=="es" else f"{BASE}/{l}{p}"

def alternates(langs,slug):
    out="".join(f'<link rel="alternate" hreflang="{l}" href="{url_de(l,slug)}">' for l in langs)
    return out+f'<link rel="alternate" hreflang="x-default" href="{url_de("es",slug)}">'

SEL_CSS=('<style>.idi{display:flex;justify-content:center;flex-wrap:wrap;gap:4px 18px;margin:0 0 16px}'
 '.idi a{padding:4px 2px;color:rgba(255,255,255,.7);font:500 .8rem Montserrat,sans-serif;text-decoration:none}'
 '.idi a:hover{color:#fff}.idi a[aria-current]{color:#fff;font-weight:700;text-decoration:underline;text-underline-offset:3px}</style>')
def selector(l,langs,slug):
    lab={"es":"Idioma","ca":"Idioma","en":"Language"}[l]
    return (f'<nav class="idi" aria-label="{lab}">'+"".join(
        f'<a href="{url_de(x,slug)}" hreflang="{x}" lang="{x}"'+(' aria-current="true"' if x==l else '')+f'>{NOMBRE[x] if x!="es" else "Castellano"}</a>' for x in ["es","ca","en"] if x in langs)+'</nav>')

def poner_idiomas(s,l,langs,slug):
    """Mete hreflang, el selector y el lang correcto. Se puede repetir sin duplicar."""
    s=re.sub(r'<!--idiomas-->.*?<!--/idiomas-->','',s,flags=re.S)
    s=re.sub(r'<html lang="[a-z]+">',f'<html lang="{l}">',s,count=1)
    if len(langs)>1:
        s=s.replace("</head>",f"{MARK}{alternates(langs,slug)}{SEL_CSS}<!--/idiomas--></head>",1)
        sel=f'{MARK}{selector(l,langs,slug)}<!--/idiomas-->'
        s=re.sub(r'(<div class="links">.*?</div>)',lambda m:m.group(1)+sel,s,count=1,flags=re.S)
    return s

def localizar_enlaces(s,l,trad):
    def rep(m):
        slug=m.group(1)
        if slug=="" : return f'href="{BASE}/{l}/blog/"'
        return f'href="{BASE}/{l}/blog/{slug}/"' if slug in trad else m.group(0)
    s=re.sub(r'href="'+re.escape(BASE)+r'/blog/([a-z0-9-]*)/?"',rep,s)
    # la home: en el idioma de la página
    s=re.sub(r'href="'+re.escape(BASE)+r'/(\?[^"#]*)?(#[^"]*)?"',lambda m:f'href="{BASE}/?lang={l}'+(("&"+m.group(1)[1:]) if m.group(1) else "")+(m.group(2) or "")+'"',s)
    return s

def traducir_pagina(s,l,slug,trad):
    d=dic(l,slug); out=[]
    for tok in piezas(s):
        if tok.startswith("<script") and "application/ld+json" in tok:
            a=tok[:tok.index(">")+1]; j=json.loads(tok[len(a):tok.rindex("</script>")])
            ld_traducir(j,lambda x:tr(l,d,x))
            def inl(o):
                if isinstance(o,dict):
                    for k,v in o.items():
                        if k=="inLanguage": o[k]=INLANG[l]
                        else: inl(v)
                elif isinstance(o,list):
                    for x in o: inl(x)
            inl(j)
            txt=json.dumps(j,ensure_ascii=False)
            txt=txt.replace(f"{BASE}/blog/",f"{BASE}/{l}/blog/")
            out.append(a+txt+"</script>")
        elif tok.startswith("<meta") and re.search(r'(name="description"|property="og:(title|description)")',tok):
            out.append(re.sub(r'content="([^"]*)"',lambda m:'content="'+html.escape(tr(l,d,html.unescape(m.group(1))))+'"',tok))
        elif tok.startswith("<") and not tok.startswith(("<script","<style","<!--")):
            out.append(ATTR.sub(lambda m:f'{m.group(1)}="'+(html.escape(tr(l,d,html.unescape(m.group(2)))) if traducible(html.unescape(m.group(2))) and norm(html.unescape(m.group(2))) not in IGNORAR else m.group(2))+'"',tok))
        elif es_texto(tok) and traducible(tok):
            out.append(traducir_texto(l,d,tok))
        else: out.append(tok)
    s="".join(out)
    s=s.replace('content="es_ES"',f'content="{LOCALE[l]}"')
    s=re.sub(r'<link rel="canonical" href="[^"]*">',f'<link rel="canonical" href="{url_de(l,slug)}">',s,count=1)
    s=re.sub(r'<meta property="og:url" content="[^"]*">',f'<meta property="og:url" content="{url_de(l,slug)}">',s,count=1)
    return localizar_enlaces(s,l,trad)

def main():
    pubs=publicados()
    idx=open(f"{ROOT}/blog/index.html",encoding="utf-8").read()
    if sys.argv[1:2]==["pendientes"]:
        res={}
        for l in LANGS:
            for slug in pubs:
                s=open(f"{ROOT}/blog/{slug}/index.html",encoding="utf-8").read()
                f=falta(l,slug,s)
                if f: res[f"{l}/{slug}"]=f
            f=falta(l,"_indice",idx)
            if f: res[f"{l}/_indice"]=f
        print(json.dumps(res,ensure_ascii=False,indent=1)); return
    trad={l:[] for l in LANGS}
    for l in LANGS:
        for slug in pubs:
            s=open(f"{ROOT}/blog/{slug}/index.html",encoding="utf-8").read()
            f=falta(l,slug,s)
            if f: print(f"AVISO: {slug} sin traducir al {l} ({len(f)} textos). Se queda solo en castellano."); continue
            trad[l].append(slug)
    # artículos
    for slug in pubs:
        langs=["es"]+[l for l in LANGS if slug in trad[l]]
        p=f"{ROOT}/blog/{slug}/index.html"; s=open(p,encoding="utf-8").read()
        s_es=poner_idiomas(s,"es",langs,slug)
        if s_es!=s: open(p,"w",encoding="utf-8").write(s_es)
        base=re.sub(r'<!--idiomas-->.*?<!--/idiomas-->','',s,flags=re.S)
        for l in langs[1:]:
            t=traducir_pagina(base,l,slug,set(trad[l]))
            t=poner_idiomas(t,l,langs,slug)
            os.makedirs(f"{ROOT}/{l}/blog/{slug}",exist_ok=True)
            open(f"{ROOT}/{l}/blog/{slug}/index.html","w",encoding="utf-8").write(t)
    # índices: en ca/en solo salen las tarjetas de los artículos traducidos
    base=re.sub(r'<!--idiomas-->.*?<!--/idiomas-->','',idx,flags=re.S)
    langs_idx=["es"]+[l for l in LANGS if trad[l] and not falta(l,"_indice",base)]
    open(f"{ROOT}/blog/index.html","w",encoding="utf-8").write(poner_idiomas(idx,"es",langs_idx,None))
    for l in langs_idx[1:]:
        s=base
        for m in re.finditer(r'<a class="card" href="'+re.escape(BASE)+r'/blog/([a-z0-9-]+)/".*?</a>',base,re.S):
            if m.group(1) not in trad[l]: s=s.replace(m.group(0),"")
        s=re.sub(r'<h2 class="sec" id="recetas">[^<]*</h2><section class="grid"></section>','',s)
        s=re.sub(r'<h2 class="sec" id="guias">[^<]*</h2><section class="grid"></section>','',s)
        t=traducir_pagina(s,l,"_indice",set(trad[l]))
        t=poner_idiomas(t,l,langs_idx,None)
        os.makedirs(f"{ROOT}/{l}/blog",exist_ok=True)
        open(f"{ROOT}/{l}/blog/index.html","w",encoding="utf-8").write(t)
    # sitemap: lo que ya había más las versiones traducidas
    sm=open(f"{ROOT}/sitemap.xml",encoding="utf-8").read()
    sm=re.sub(r'\s*<url><loc>'+re.escape(BASE)+r'/(ca|en)/[^<]*</loc>.*?</url>','',sm,flags=re.S)
    extra=""
    for l in LANGS:
        if l in langs_idx: extra+=f"  <url><loc>{url_de(l)}</loc></url>\n"
        for slug in trad[l]: extra+=f"  <url><loc>{url_de(l,slug)}</loc></url>\n"
    sm=sm.replace("</urlset>",extra+"</urlset>")
    open(f"{ROOT}/sitemap.xml","w",encoding="utf-8").write(sm)
    for l in LANGS: print(f"{l}: {len(trad[l])} artículos" + (" + índice" if l in langs_idx else " (índice pendiente)"))

if __name__=="__main__": main()
