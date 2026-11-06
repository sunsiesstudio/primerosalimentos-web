import json
f=json.load(open('/tmp/foods2.json')); x=json.load(open('/tmp/extra.json'))
t=open('template.html').read()
ic=lambda n:f.get(n) or x.get(n)
gift='<svg viewBox="0 0 40 40" aria-hidden="true"><rect x="7" y="5" width="26" height="31" rx="4" fill="#4a8760"/><rect x="11" y="10" width="18" height="3" rx="1.5" fill="#f7f4e8"/><rect x="11" y="16" width="13" height="3" rx="1.5" fill="#f7f4e8" opacity=".7"/><circle cx="27" cy="29" r="7" fill="#c96a47"/><path d="M27 25.5v6M24.5 29.5l2.5 2.5 2.5-2.5" stroke="#fff" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
check='<svg viewBox="0 0 64 64" width="64" height="64" aria-hidden="true" style="display:block;margin:0 auto"><circle cx="32" cy="32" r="30" fill="#4a8760"/><path d="M19 33l9 9 17-18" stroke="#fff" stroke-width="5.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
rep={'__FOODS__':json.dumps(f,ensure_ascii=False),'__GIFTICON__':gift,'__CHECKICON__':check,
'__PH1__':ic('Zanahoria'),'__PH2__':ic('Brócoli'),'__PH3__':ic('Aguacate'),
'__F1__':ic('Brócoli'),'__F2__':ic('Manzana'),'__F3__':ic('Guisantes'),'__F4__':ic('Calabaza'),'__F5__':ic('Huevo'),'__F6__':ic('Fresas'),
}
names=['Plátano','Brócoli','Aguacate','Fresas','Calabaza','Huevo','Zanahoria','Mango','Guisantes','Pera','Merluza','Kiwi']
pdfic=json.load(open('/tmp/pdfic.json'))
icx=lambda n:f.get(n) or x.get(n) or pdfic.get(n)
rep['__MARQ__']=''.join(f'<span>{icx(n)}{n}</span><i></i>' for n in names)
st={'__S1A__':'Fresas','__S1B__':'Plátano','__S2A__':'Brócoli','__S2B__':'Huevo','__S3A__':'Zanahoria','__S3B__':'Aguacate'}
st.update({'__S1C__':'Guisantes','__S1D__':'Kiwi','__S1E__':'Arándanos','__S2C__':'Mango','__S2D__':'Pera','__S2E__':'Uvas','__S3C__':'Calabaza','__S3D__':'Mandarina','__S3E__':'Fresas'})
for k,n in st.items(): rep[k]=icx(n)
rep.update({'__I1__':icx('Brócoli'),'__I2__':icx('Fresas'),'__I3__':icx('Calabaza'),'__I4__':icx('Manzana')})
rep.update({'__M1__':icx('Fresas'),'__M2__':icx('Guisantes'),'__M3__':icx('Plátano'),'__M4__':icx('Brócoli'),'__M5__':icx('Arándanos'),'__M6__':icx('Aguacate'),'__M7__':icx('Pera')})
rep.update({f'__T{k}__':icx(n) for k,n in enumerate(['Plátano', 'Fresas', 'Brócoli', 'Zanahoria', 'Aguacate', 'Kiwi', 'Calabaza', 'Pera', 'Manzana'],1)})
rep.update({'__B1__':icx('Plátano'),'__B2__':icx('Uvas')})
rep['__FROW__']=''.join(icx(n) for n in ['Fresas','Brócoli','Plátano','Zanahoria','Aguacate','Calabaza','Huevo','Pera','Guisantes'])
for k,v in rep.items():
    t=t.replace(k,v)
import re as _r; assert not _r.findall(r'__[A-Z0-9]+__',t)
open('index.html','w').write(t)
