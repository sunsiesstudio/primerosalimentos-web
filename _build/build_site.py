import json,os,html,shutil
from articles import ARTICLES as A1,U_AEP
from guides2 import G2
from recipes import R
from guides3 import G3
from recipes2 import R2
import illus
for a in A1: a.setdefault('cat','guia')
ARTICLES=A1+G2+G3+R+R2
import os as _os
_PUB=_os.environ.get('PUB')
if _PUB: ARTICLES=[a for a in ARTICLES if a['slug'] in _PUB.split(',')]
OUT=_os.environ.get('OUT','/home/claude/landing/out')
for a in R+R2: a.setdefault('mins',3); a.setdefault('faq',[])
for a in ARTICLES:
    if 'body' in a: a['body']=illus.apply(a['body'])
BASE="https://www.primerosalimentos.com"
F={**json.load(open('/tmp/foods2.json')),**json.load(open('/tmp/extra.json')),**json.load(open('/tmp/pdfic.json'))}
MESES=["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"]
fecha=lambda d:f"{int(d[8:])} de {MESES[int(d[5:7])-1]} de {d[:4]}"
LOGO='<svg viewBox="0 0 640 215" role="img" aria-label="Primeros alimentos"><defs><path id="arc" d="M10,185 Q320,10 630,185"/></defs><text text-anchor="middle" style="font:400 56px \'Luckiest Guy\',sans-serif;letter-spacing:.03em;fill:#4a8760"><textPath href="#arc" startOffset="50%">Primeros alimentos</textPath></text><g transform="translate(279 112) scale(3.4)" style="fill:#c96a47"><polygon points="12,1.5 14.9,8.4 22.4,9.1 16.7,14 18.4,21.4 12,17.5 5.6,21.4 7.3,14 1.6,9.1 9.1,8.4"/></g></svg>'
CSS=r"""
:root{--bg:#eeead8;--card:#f7f4e8;--ink:#262626;--mute:#6b6a5c;--line:#d8d3bc;--green:#4a8760;--terra:#c96a47;--blue:#3e4cd0;--gold:#c9962f}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:400 18px/1.7 Montserrat,system-ui,sans-serif;-webkit-font-smoothing:antialiased}
a{color:var(--green)}
.disp,h1,h2.t{font-family:"Luckiest Guy","Arial Rounded MT Bold",sans-serif;font-weight:400;letter-spacing:.02em}
.top{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:16px;width:min(1080px,100% - 40px);margin:0 auto;padding:22px 0}
.top .lg{display:block;width:clamp(170px,46vw,250px);flex:none}.top .lg svg{display:block;width:100%;overflow:visible}
.top nav{display:flex;gap:18px;align-items:center;font-weight:700;font-size:.92rem}
.top nav a{color:var(--ink);text-decoration:none}
.top .lg{grid-column:2}.top nav{grid-column:3;justify-self:end}
@media(max-width:640px){.top{display:flex;justify-content:space-between;gap:12px;padding:18px 0 0}}
.btn{white-space:nowrap;display:inline-flex;align-items:center;justify-content:center;min-height:46px;padding:0 20px;border-radius:14px;background:var(--terra);color:#fff!important;font:800 .95rem Montserrat,sans-serif;text-decoration:none;box-shadow:0 4px 0 #a24f30}
.wrap{width:min(1080px,100% - 40px);margin:0 auto}
.hero{padding:56px 0 40px}
.hero .kick{display:block;font-weight:800;font-size:.8rem;letter-spacing:.12em;text-transform:uppercase;color:var(--terra);margin:0 0 10px}
.hero h1{color:var(--green);font-size:clamp(2.2rem,7vw,3.4rem);line-height:1.04;margin:0 0 14px}
.hero p{color:var(--ink);font-size:1.12rem;line-height:1.65;max-width:46em;margin:0}
.grid{display:grid;gap:22px;padding:20px 0 90px}
.card{display:flex;flex-direction:column;gap:12px;padding:26px;border-radius:24px;background:var(--card);border:1.5px solid var(--line);text-decoration:none;color:var(--ink);transition:transform .15s,box-shadow .2s}
.card:hover{transform:translateY(-3px);box-shadow:0 14px 30px rgba(38,38,38,.08)}
.card .ic{width:62px;height:62px;border-radius:50%;display:grid;place-items:center;background:#fff}
.card .ic svg{width:42px;height:42px;overflow:visible}
.card h2{font-size:1.2rem;line-height:1.3;margin:0}
.card p{margin:0;color:var(--mute);font-size:.95rem;line-height:1.55}
.card small{color:var(--terra);font-weight:700;font-size:.8rem}
@media(min-width:760px){.grid{grid-template-columns:repeat(3,1fr)}}
.fd .o{stroke:none}
/* artículo */
.crumbs{font-size:.85rem;color:var(--mute);margin:30px 0 0}.crumbs a{color:var(--mute)}
article{width:min(700px,100% - 40px);margin:0 auto;padding:0 0 60px}
article header{padding:26px 0 30px}
article header .ic{width:84px;height:84px;border-radius:50%;display:grid;place-items:center;background:var(--card);margin:0 0 20px}
article header .ic svg{width:56px;height:56px;overflow:visible}
article h1{color:var(--green);font-size:clamp(2rem,6vw,2.9rem);line-height:1.06;margin:0 0 16px}
.meta{color:var(--mute);font-size:.88rem;font-weight:600}
.lead{font-size:1.15rem;line-height:1.65;margin:22px 0 0}
article h2{font-size:1.45rem;line-height:1.25;margin:48px 0 14px;color:var(--ink);font-weight:800}
article p{margin:0 0 18px}
article ul,article ol{padding-left:24px;margin:0 0 20px}article li{margin:0 0 10px}
article li::marker{color:var(--terra);font-weight:800}
.faq{margin:52px 0 0;padding:28px;border-radius:24px;background:var(--card);border:1.5px solid var(--line)}
.faq h2{margin-top:0}
.faq details{border-top:1px solid var(--line);padding:14px 0}.faq details:first-of-type{border-top:0}
.faq summary{cursor:pointer;font-weight:700;list-style:none}.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";float:right;color:var(--terra);font-weight:800}
.faq details[open] summary::after{content:"–"}
.faq details p{margin:10px 0 0;color:var(--mute)}
.cta{margin:70px 0 0;padding:28px 32px 28px 12px;border-radius:24px;background:var(--green);color:#fff;text-align:left;display:grid;grid-template-columns:46% 1fr;gap:18px;align-items:center}
.cta .mk{display:block;width:100%;height:auto;margin:-64px 0 -36px}
@media(max-width:640px){.cta{grid-template-columns:1fr;text-align:center;padding:0 24px 30px;margin-top:90px}.cta .mk{width:min(300px,82%);margin:-70px auto 0}}
.cta .t{font-size:1.7rem;line-height:1.1;margin:0 0 10px}
.cta p{margin:0 0 20px;color:rgba(255,255,255,.88)}
.rel{margin:52px 0 0}.rel h2{margin-top:0}
.rel a.r{display:flex;align-items:center;gap:14px;padding:14px 0;border-top:1px solid var(--line);text-decoration:none;color:var(--ink);font-weight:700}
.rel a.r svg{width:34px;height:34px;flex:none;overflow:visible}
.note{margin:40px 0 0;font-size:.85rem;color:var(--mute)}
.sec{font-family:"Luckiest Guy",sans-serif;font-weight:400;color:var(--terra);font-size:1.8rem;letter-spacing:.02em;margin:40px 0 0}
.jump{display:flex;gap:10px;margin-top:20px!important}.jump a{padding:8px 16px;border-radius:99px;background:var(--card);border:1.5px solid var(--line);text-decoration:none;color:var(--ink);font-weight:700;font-size:.9rem}
.pills{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 14px}.pills span{padding:6px 14px;border-radius:99px;background:var(--card);border:1.5px solid var(--line);font-weight:700;font-size:.85rem}
.alg{font-size:.95rem;color:var(--mute)}.reel{margin:6px 0 10px}
.ing li::marker{content:"• "}.steps li{padding-left:4px}
.grid{padding-bottom:30px!important}
footer{background:var(--green);color:rgba(255,255,255,.85);text-align:center;padding:44px 24px 50px;font-size:.85rem}
footer a{color:#fff}footer .links{display:flex;justify-content:center;gap:22px;font-weight:700;margin:0 0 14px}
footer p{max-width:36em;margin:0 auto}
footer .soc{display:flex;justify-content:center;flex-wrap:wrap;gap:12px;margin:0 0 26px}
footer .soc a{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:0 18px;border-radius:999px;border:1.5px solid rgba(255,255,255,.5);color:#fff;text-decoration:none;font-weight:700;font-size:.92rem}
footer .soc a:hover{background:rgba(255,255,255,.12)}
footer .soc svg{width:19px;height:19px}
footer .links{margin-bottom:14px;max-width:36em;margin-left:auto!important;margin-right:auto!important;padding-top:22px;border-top:1px solid rgba(255,255,255,.22)}
@media(max-width:480px){.top nav{gap:12px}.top .btn{min-height:40px;padding:0 14px;font-size:.85rem}footer .links{flex-wrap:wrap;gap:12px 20px}}
"""+illus.CSS
HEAD=lambda title,desc,url,extra="":f'''<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article"><meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}/capturas/guia-1.jpg"><meta property="og:locale" content="es_ES">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{BASE}/icon-192.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Luckiest+Guy&family=Montserrat:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{BASE}/blog/blog.css">
{extra}<script src="{BASE}/consent.js" defer></script>
</head><body>
<header class="top"><a class="lg" href="{BASE}/" aria-label="Primeros Alimentos">{LOGO}</a><nav><a class="btn" href="{BASE}/?o=blog">Lista de espera</a></nav></header>
'''
FOOT=f'''<footer><div class="soc"><a href="https://www.instagram.com/primeros.alimentos/" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="17.3" cy="6.7" r="1.3" fill="currentColor"/></svg>Instagram</a><a href="https://www.tiktok.com/" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15.5 3c.4 2.6 2 4.3 4.5 4.6v3.2c-1.7 0-3.2-.5-4.5-1.4v6.3A5.6 5.6 0 1 1 9.9 10v3.3a2.4 2.4 0 1 0 2.4 2.4V3z" fill="currentColor"/></svg>TikTok</a></div><div class="links"><a href="{BASE}/">Primeros Alimentos</a><a href="{BASE}/blog/">Blog</a><a href="{BASE}/privacy.html">Privacidad</a><a href="{BASE}/privacy.html#cookies" data-cookies>Cookies</a></div>
<p>Información orientativa basada en las recomendaciones de la <a href="{U_AEP}" rel="noopener">AEP</a>. No sustituye la consulta con tu pediatra.</p></footer></body></html>'''
ic=lambda n:F.get(n) or F['Plátano']
os.makedirs(f"{OUT}/blog",exist_ok=True)
open(f"{OUT}/blog/blog.css","w").write(CSS)
author={"@type":"Person","name":"Martina Solés","url":"https://www.instagram.com/sunsies.studio/"}
# artículos
for a in ARTICLES:
    url=f"{BASE}/blog/{a['slug']}/"
    ld=[{"@context":"https://schema.org","@type":"BlogPosting","headline":a['title'],"description":a['desc'],"datePublished":a['date'],"dateModified":a.get('updated',a['date']),"inLanguage":"es-ES","author":author,"publisher":{"@type":"Organization","name":"Primeros Alimentos","logo":{"@type":"ImageObject","url":f"{BASE}/icon-512.png"}},"mainEntityOfPage":url,"image":f"{BASE}/capturas/guia-1.jpg"},
        {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":r}} for q,r in a['faq']]},
        {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Blog","item":f"{BASE}/blog/"},{"@type":"ListItem","position":2,"name":a['short'],"item":url}]}]
    extra="".join(f'<script type="application/ld+json">{json.dumps(x,ensure_ascii=False)}</script>\n' for x in ld)
    if a['cat']=='receta':
        rec={"@context":"https://schema.org","@type":"Recipe","name":a['short'],"description":a['desc'],"author":author,"datePublished":a['date'],"recipeYield":a['yld'],"prepTime":f"PT{a['prep']}M","cookTime":f"PT{a['cook']}M","totalTime":f"PT{a['prep']+a['cook']}M","recipeCategory":"Alimentación complementaria","recipeCuisine":"Española","keywords":"BLW, bebé, alimentación complementaria, sin azúcar, sin sal","recipeIngredient":a['ing'],"recipeInstructions":[{"@type":"HowToStep","text":x} for x in a['steps']],"image":f"{BASE}/capturas/guia-1.jpg"}
        if a.get('reel'): rec["video"]={"@type":"VideoObject","name":a['short'],"contentUrl":a['reel'],"embedUrl":a['reel'],"description":a['desc'],"uploadDate":a['date'],"thumbnailUrl":f"{BASE}/capturas/guia-1.jpg"}
        ld[0]=rec
        if not a['faq']: ld.pop(1)
        extra="".join(f'<script type="application/ld+json">{json.dumps(x,ensure_ascii=False)}</script>\n' for x in ld)
        pills=f'<div class="pills"><span>{a["age"]}</span><span>Preparación {a["prep"]} min</span>'+(f'<span>Cocción {a["cook"]} min</span>' if a['cook'] else '')+f'<span>{a["yld"]}</span></div>'
        algs=('<p class="alg"><strong>Alérgenos:</strong> '+", ".join(a['alg'])+'</p>') if a['alg'] else '<p class="alg">Sin alérgenos principales.</p>'
        reel=f'<a class="btn reel" href="{a["reel"]}" target="_blank" rel="noopener">Ver el vídeo de la receta</a>' if a.get('reel') else ''
        a['body']=f'''{pills}{algs}{reel}
<h2>Ingredientes</h2><ul class="ing">'''+"".join(f"<li>{x}</li>" for x in a['ing'])+'''</ul>
<h2>Paso a paso</h2><ol class="steps">'''+"".join(f"<li>{x}</li>" for x in a['steps'])+'''</ol>
<h2>Cómo servirlo según la edad</h2><ul>'''+"".join(f"<li>{x}</li>" for x in a['serve'])+f'''</ul>
<h2>Conservar</h2><p>{a['keep']}</p>
<p>Sin sal ni azúcar añadidos. Antes de servir, comprueba que la temperatura y la textura son las adecuadas: se tiene que poder aplastar entre los dedos.</p>'''
    faq="".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(r)}</p></details>" for q,r in a['faq'])
    pool=[b for b in ARTICLES if b is not a and b['cat']==a['cat']][:3]+[b for b in ARTICLES if b is not a and b['cat']!=a['cat']][:1]
    rel="".join(f'<a class="r" href="{BASE}/blog/{b["slug"]}/">{ic(b["icon"])}<span>{html.escape(b["title"])}</span></a>' for b in pool)
    page=HEAD(f"{a['title']} | Primeros Alimentos",a['desc'],url,extra)+f'''<main><article>
<p class="crumbs"><a href="{BASE}/blog/">Blog</a> / {html.escape(a['short'])}</p>
<header><div class="ic">{ic(a['icon'])}</div><h1>{html.escape(a['title'])}</h1>
<div class="meta">Por Martina Solés · {fecha(a['date'])} · {a['mins']} min de lectura</div>
<p class="lead">{a['lead']}</p></header>
{a['body']}
{('<section class="faq"><h2>Preguntas frecuentes</h2>'+faq+'</section>') if faq else ""}
<section class="cta"><img class="mk" src="{BASE}/capturas/mockup-app.webp?v=2" width="640" height="652" loading="lazy" alt="Dos pantallas de la app Primeros Alimentos: el menú del día y los alimentos que ha probado"><div><p class="t disp">Todo esto, en una app</p><p>Qué darle cada día, lo que ya ha probado y estas dudas resueltas, en el móvil. Sale el 1 de diciembre.</p><a class="btn" style="background:#fff;color:var(--green)!important;box-shadow:0 4px 0 rgba(0,0,0,.15)" href="{BASE}/?o=blog-{a['slug'][:20]}">Apúntate y llévate la guía gratis</a></div></section>
<section class="rel"><h2>Sigue leyendo</h2>{rel}</section>
<p class="note">Fuente: <a href="{U_AEP}" rel="noopener">Recomendaciones de la Asociación Española de Pediatría sobre la alimentación complementaria</a>. Información orientativa: ante cualquier duda, consulta con tu pediatra.</p>
</article></main>'''+FOOT
    os.makedirs(f"{OUT}/blog/{a['slug']}",exist_ok=True)
    open(f"{OUT}/blog/{a['slug']}/index.html","w").write(page)
# portada
card=lambda a:f'<a class="card" href="{BASE}/blog/{a["slug"]}/"><div class="ic">{ic(a["icon"])}</div><small>{(a["age"]+" · "+str(a["prep"]+a["cook"])+" min") if a["cat"]=="receta" else str(a["mins"])+" min de lectura"}</small><h2>{html.escape(a["title"])}</h2><p>{html.escape(a["desc"])}</p></a>'
_g=[a for a in ARTICLES if a['cat']=='guia'];_r=[a for a in ARTICLES if a['cat']=='receta']
cards=(('<h2 class="sec" id="guias">Guías</h2><section class="grid">'+"".join(card(a) for a in _g)+'</section>') if _g else '')+(('<h2 class="sec" id="recetas">Recetas</h2><section class="grid">'+"".join(card(a) for a in _r)+'</section>') if _r else '')
ld={"@context":"https://schema.org","@type":"Blog","name":"Blog de Primeros Alimentos","url":f"{BASE}/blog/","inLanguage":"es-ES"}
idx=HEAD("Blog de alimentación complementaria y BLW | Primeros Alimentos","Artículos sobre alimentación complementaria y BLW: cuándo empezar, qué darle, cómo cortarlo y qué evitar. Según las recomendaciones de la AEP.",f"{BASE}/blog/",f'<script type="application/ld+json">{json.dumps(ld,ensure_ascii=False)}</script>')+f'''<main class="wrap"><section class="hero"><h1>Sus primeros alimentos, paso a paso</h1><p>Las dudas de cuando empiezan a comer, resueltas de forma clara y según las recomendaciones de la Asociación Española de Pediatría.'''+(' Y recetas sin sal ni azúcar para hacer en casa.' if _r else '')+'''</p>''' + ('<p class="jump"><a href="#guias">Guías</a><a href="#recetas">Recetas</a></p>' if _r and _g else '') + f'''</section>
{cards}</main>'''+FOOT
open(f"{OUT}/blog/index.html","w").write(idx)
# sitemap
urls=[(f"{BASE}/","2026-11-06"),(f"{BASE}/blog/",max(a['date'] for a in ARTICLES))]+[(f"{BASE}/blog/{a['slug']}/",a.get('updated',a['date'])) for a in ARTICLES]
open(f"{OUT}/sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"".join(f"  <url><loc>{u}</loc><lastmod>{d}</lastmod></url>\n" for u,d in urls)+'</urlset>\n')
print("ok",len(ARTICLES))
