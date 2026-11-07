import json,random
I=json.load(open('/tmp/pdfic.json'))
t=open('guia_template.html').read()
random.seed(4)
pos=[(8,8),(30,20),(52,6),(74,18),(96,7),(118,16),(14,40),(124,42),(62,30),(37,182.7),(108.3,164.7),(82.4,187.8),(126.9,186.6),(57.1,169.4),(12.2,161.3)]
names=['Plátano','Fresas','Brócoli','Mandarina','Kiwi','Aguacate','Guisantes','Uvas','Pera','Zanahoria','Calabaza','Manzana','Fresas','Brócoli','Pera']
sc=''.join(I[n].replace('<svg class="fd"',f'<svg class="fd" style="left:{x}mm;top:{y}mm;transform:rotate({random.randint(-25,25)}deg)"') for n,(x,y) in zip(names,pos))
iron=''.join(I[n] for n in ["Pollo","Merluza","Huevo","Lentejas"])
X=lambda: '<span class="x">✕</span>'
ev=[(X(),"Sal","Nunca se añade. Sus riñones aún no la procesan bien."),
(X(),"Azúcar y zumos","Favorecen las caries y le acostumbran al dulce. Mejor la fruta entera."),
(X(),"Miel","Nunca antes de los 12 meses: puede llevar esporas de botulismo."),
(X(),"Leche de vaca como bebida","No antes de los 12 meses. Poco hierro y demasiada proteína para sus riñones."),
(I["Almendra"],"Frutos secos enteros","Hasta los 5 años, solo en crema o molidos muy finos."),
(I["Uvas"],"Uvas y tomates cherry enteros","Siempre en cuartos a lo largo. Igual con los arándanos."),
(X(),"Pescados grandes","Mucho mercurio: pez espada, emperador, tiburón (cazón, tintorera), atún rojo y lucio."),
(I["Espinacas"],"Espinacas, acelgas, remolacha, rúcula y apio","Muchos nitratos. Nada antes de 12 meses; de 1 a 3 años, como mucho una ración al día. Borraja, nada antes de los 3 años."),
(I["Arroz"],"Bebida de arroz","Acumula arsénico: mejor evitarla. El arroz y las tortitas de arroz, de vez en cuando.")]
evh=''.join(f'<div>{i}<span><b>{a}</b><span>{b}</span></span></div>' for i,a,b in ev)
for k,v in {'__SCATTER__':sc,'__IRON__':iron,'__EVITAR__':evh}.items():
    assert k in t; t=t.replace(k,v)
open('/tmp/guia.html','w').write(t)
