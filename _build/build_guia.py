# Genera la guía en castellano, catalán e inglés (PDF claro) y sus previews (claro y oscuro).
# Uso: python3 build_guia.py   (desde _build; necesita las fuentes en ~/.fonts y Playwright)
import json, random, re, os, asyncio
from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.dirname(HERE)
I = json.load(open(os.path.join(HERE, 'pdfic.json')))
FONTS = os.path.expanduser('~/.fonts')

# --- textos: castellano -> (catalán, inglés) ---
T = [
 ('<html lang="es">', '<html lang="ca">', '<html lang="en">'),
 ('Cómo empezar con la alimentación complementaria', "Com començar amb l'alimentació complementària", 'How to start solid foods'),
 ('Una guía corta para los primeros meses.', 'Una guia curta per als primers mesos.', 'A short guide for the first months.'),
 ('1 · Cuándo empezar', '1 · Quan començar', '1 · When to start'),
 ('Hacia los 6 meses', 'Cap als 6 mesos', 'Around 6 months'),
 ('Se recomienda empezar hacia los 6 meses, y nunca antes de los 4. Más que la fecha exacta, fíjate en si está listo.',
  "Es recomana començar cap als 6 mesos, i mai abans dels 4. Més que la data exacta, fixa't en si està preparat.",
  "It's recommended to start around 6 months, and never before 4. More than the exact date, look at whether they're ready."),
 ('Las señales de que está listo', 'Els senyals que està preparat', "The signs they're ready"),
 ('Se mantiene sentado con poco apoyo y sujeta bien la cabeza.', 'Es manté assegut amb poc suport i aguanta bé el cap.', 'They sit with little support and hold their head steady.'),
 ('Le interesa lo que coméis: mira, abre la boca, intenta cogerlo.', "Li interessa el que mengeu: mira, obre la boca, intenta agafar-ho.", "They're interested in what you eat: they watch, open their mouth, try to grab it."),
 ('Coge cosas con la mano y se las lleva a la boca.', 'Agafa coses amb la mà i se les porta a la boca.', 'They pick things up and bring them to their mouth.'),
 ('Ya no empuja la comida hacia fuera con la lengua.', 'Ja no empeny el menjar cap a fora amb la llengua.', 'They no longer push food out with their tongue.'),
 ('La leche sigue siendo lo principal', 'La llet continua sent el principal', 'Milk is still the main thing'),
 ('Hasta el año, el pecho o el biberón siguen siendo su alimento principal, a demanda. La comida <i>complementa</i>, no sustituye: al principio come poco, y es normal.',
  "Fins a l'any, el pit o el biberó continuen sent el seu aliment principal, a demanda. El menjar <i>complementa</i>, no substitueix: al principi menja poc, i és normal.",
  'Until their first birthday, breast milk or formula is still their main food, on demand. Food <i>complements</i> it, it doesn\'t replace it: at first they eat very little, and that\'s normal.'),
 ('<b>Y agua</b>', '<b>I aigua</b>', '<b>And water</b>'),
 ('Desde que empieza a comer, ofrécele agua en vaso con las comidas. Sin forzar: él decide cuánto bebe.',
  "Des que comença a menjar, ofereix-li aigua en got amb els àpats. Sense forçar: ell decideix quanta en beu.",
  'From the moment they start eating, offer water in a cup with meals. No pressure: they decide how much to drink.'),
 ('2 · Qué ofrecer', '2 · Què oferir', '2 · What to offer'),
 ('Primero, el hierro', 'Primer, el ferro', 'Iron first'),
 ('No hay un orden obligatorio de alimentos. Lo que sí importa es que desde el principio haya hierro y zinc a diario, porque sus reservas bajan a partir de los 6 meses.',
  "No hi ha un ordre obligatori d'aliments. El que sí que importa és que des del principi hi hagi ferro i zinc cada dia, perquè les seves reserves baixen a partir dels 6 mesos.",
  'There is no set order of foods. What does matter is having iron and zinc every day from the start, because their stores drop from 6 months.'),
 ('En casi todas las comidas', 'A gairebé tots els àpats', 'In almost every meal'),
 ('Carne, pescado, huevo o legumbres, bien cocinados. Y alrededor, verdura, fruta y cereales, mejor integrales.',
  'Carn, peix, ou o llegums, ben cuinats. I al voltant, verdura, fruita i cereals, millor integrals.',
  'Meat, fish, egg or pulses, well cooked. And around them, vegetables, fruit and grains, ideally wholegrain.'),
 ('Los alérgenos, pronto y en poca cantidad', 'Els al·lèrgens, aviat i en poca quantitat', 'Allergens: early and in small amounts'),
 ('Retrasarlos pasados los 6 meses no previene la alergia. Los habituales: huevo, pescado, cacahuete y frutos secos (en crema o molidos), lácteos y gluten. Ofrécelos de uno en uno, unos días seguidos y en poca cantidad, mejor entre semana para poder observar.',
  "Endarrerir-los més enllà dels 6 mesos no prevé l'al·lèrgia. Els habituals: ou, peix, cacauet i fruits secs (en crema o molts), lactis i gluten. Ofereix-los d'un en un, uns dies seguits i en poca quantitat, millor entre setmana per poder observar.",
  "Delaying them past 6 months doesn't prevent allergy. The usual ones: egg, fish, peanut and tree nuts (as butter or finely ground), dairy and gluten. Offer them one at a time, a few days in a row and in small amounts, ideally on weekdays so you can keep an eye on them."),
 ('Reacción leve', 'Reacció lleu', 'Mild reaction'),
 ('Ronchas, picor o enrojecimiento', 'Butllofes, picor o envermelliment', 'Hives, itching or redness'),
 ('Algún vómito aislado', 'Algun vòmit aïllat', 'An isolated vomit'),
 ('No lo repitas: anótalo y consulta a tu pediatra', "No el repeteixis: anota-ho i consulta el teu pediatre", "Don't offer it again: note it down and ask your paediatrician"),
 ('Grave: llama al 112', 'Greu: truca al 112', 'Severe: call emergency services'),
 ('Labios, lengua o cara hinchados', 'Llavis, llengua o cara inflats', 'Swollen lips, tongue or face'),
 ('Le cuesta respirar', 'Li costa respirar', 'Difficulty breathing'),
 ('Vómitos repetidos o muy decaído', 'Vòmits repetits o molt decaigut', 'Repeated vomiting or very floppy'),
 ('3 · Texturas y método', '3 · Textures i mètode', '3 · Textures and method'),
 ('De puré a trozos', 'De puré a trossos', 'From purée to pieces'),
 ('Puré espeso o trozos blandos', 'Puré espès o trossos tous', 'Thick purée or soft pieces'),
 ('Grumos y tiras', 'Grumolls i tires', 'Lumps and strips'),
 ('Pinza: trocitos', 'Pinça: trossets', 'Pincer grasp: small pieces'),
 ('Como la familia', 'Com la família', 'Like the family'),
 ('<b>Grumos cuanto antes</b>, nunca más tarde de los 8 o 9 meses. Retrasarlos se asocia a más problemas con la comida y a comer menos fruta y verdura.',
  "<b>Grumolls com més aviat millor</b>, mai més tard dels 8 o 9 mesos. Endarrerir-los s'associa a més problemes amb el menjar i a menjar menys fruita i verdura.",
  '<b>Lumps as early as possible</b>, never later than 8 or 9 months. Delaying them is linked to more feeding problems and eating less fruit and veg.'),
 ('<b>La prueba fácil</b>Si lo aplastas entre el pulgar y el índice, o con la lengua contra el paladar, está bien de textura. Las tiras, del tamaño de un dedo (5-6 cm), para que las coja con el puño.',
  "<b>La prova fàcil</b>Si l'aixafes entre el polze i l'índex, o amb la llengua contra el paladar, la textura és bona. Les tires, de la mida d'un dit (5-6 cm), perquè les agafi amb el puny.",
  '<b>The easy test</b>If you can squash it between your thumb and finger, or with your tongue against the roof of your mouth, the texture is right. Strips the size of a finger (5-6 cm), so they can grab them with their fist.'),
 ('Puré y cuchara', 'Puré i cullera', 'Purée and spoon'),
 ('Puré que va ganando grumos. Tú le das.', 'Puré que va guanyant grumolls. Tu li dones.', 'Purée that gets lumpier over time. You feed them.'),
 ('Trozos blandos. Los coge él y decide cuánto come.', 'Trossos tous. Els agafa ell i decideix quant menja.', 'Soft pieces. They pick them up and decide how much to eat.'),
 ('<h3>Mixto</h3>', '<h3>Mixt</h3>', '<h3>Mixed</h3>'),
 ('Algo de puré en unas comidas y trozos en otras.', 'Una mica de puré en uns àpats i trossos en altres.', 'Some purée at some meals and pieces at others.'),
 ('Ningún método respetuoso con el bebé es mejor que otro. El BLW no se recomienda si hay dificultades neurológicas o motoras, o si no gana peso: habla antes con tu pediatra.',
  "Cap mètode respectuós amb el nadó és millor que un altre. El BLW no es recomana si hi ha dificultats neurològiques o motores, o si no guanya pes: parla'n abans amb el teu pediatre.",
  "No baby-led, responsive method is better than another. BLW isn't recommended if there are neurological or motor difficulties, or if they're not gaining weight: talk to your paediatrician first."),
 ('4 · Seguridad', '4 · Seguretat', '4 · Safety'),
 ('Arcada o atragantamiento', 'Arcada o ennuegament', 'Gagging or choking'),
 ('Siempre <b>sentado y erguido</b>, con un adulto al lado y sin pantallas. Nunca recostado, ni en la hamaca ni en el carrito.',
  'Sempre <b>assegut i dret</b>, amb un adult al costat i sense pantalles. Mai estirat, ni a la gandula ni al cotxet.',
  'Always <b>sitting upright</b>, with an adult beside them and no screens. Never reclined, in a bouncer or in the pram.'),
 ('Arcada: es normal', 'Arcada: és normal', 'Gagging: normal'),
 ('Tose y hace ruido', 'Tus i fa soroll', 'Coughing and making noise'),
 ('Ojos llorosos', 'Ulls plorosos', 'Watery eyes'),
 ('Echa la comida hacia delante', 'Treu el menjar cap endavant', 'Pushing the food forward'),
 ('Calma: no metas los dedos ni le des golpes', "Calma: no hi posis els dits ni li donis cops", "Stay calm: don't put your fingers in or pat their back"),
 ('<h4>Atragantamiento</h4>', '<h4>Ennuegament</h4>', '<h4>Choking</h4>'),
 ('No tose, no llora, no respira', 'No tus, no plora, no respira', 'No coughing, crying or breathing'),
 ('Se pone morado', 'Es posa morat', 'Turning blue'),
 ('Ruido agudo o silencio', 'Soroll agut o silenci', 'High-pitched noise or silence'),
 ('Actúa ya', 'Actua ja', 'Act now'),
 ('Si se atraganta', "Si s'ennuega", 'If they choke'),
 ('<b>Llama al 112</b>o pide que llamen.', '<b>Truca al 112</b>o demana que truquin.', '<b>Call emergency services</b>or ask someone to call.'),
 ('<b>5 golpes en la espalda</b>boca abajo sobre tu antebrazo, con la cabeza más baja.', "<b>5 cops a l'esquena</b>de bocaterrosa sobre el teu avantbraç, amb el cap més baix.", '<b>5 back blows</b>face down along your forearm, head lower than chest.'),
 ('<b>5 compresiones en el pecho</b>boca arriba, con dos dedos.', '<b>5 compressions al pit</b>de panxa enlaire, amb dos dits.', '<b>5 chest thrusts</b>face up, with two fingers.'),
 ('<b>Repite</b>hasta que lo expulse. Si pierde el conocimiento, RCP.', "<b>Repeteix</b>fins que l'expulsi. Si perd el coneixement, RCP.", '<b>Repeat</b>until it comes out. If they lose consciousness, start CPR.'),
 ('Un curso de primeros auxilios pediátricos sirve para cualquier método y da mucha tranquilidad.', 'Un curs de primers auxilis pediàtrics serveix per a qualsevol mètode i dona molta tranquil·litat.', 'A paediatric first aid course is useful whatever the method, and gives real peace of mind.'),
 ('5 · Qué evitar', '5 · Què evitar', '5 · What to avoid'),
 ('Y hasta cuándo', 'I fins quan', 'And until when'),
 ('Todo esto, hasta que tu pediatra diga lo contrario.', 'Tot això, fins que el teu pediatre digui el contrari.', 'All of this, unless your paediatrician says otherwise.'),
 ('Y para el día a día, la app', 'I per al dia a dia, l\'app', 'And for every day, the app'),
 ('Apunta lo que ha probado, ten el menú del día y de la semana, y toda esta información a mano.', "Apunta el que ha tastat, tingues el menú del dia i de la setmana, i tota aquesta informació a mà.", "Log what they've tried, get the day's and the week's menu, and keep all this information at hand."),
 ('Muy pronto en iPhone, Android y web.', 'Molt aviat a iPhone, Android i web.', 'Coming very soon on iPhone, Android and web.'),
 ('Guía orientativa basada en las recomendaciones de la Asociación Española de Pediatría (AEP). No sustituye la valoración de tu pediatra.',
  "Guia orientativa basada en les recomanacions de l'Associació Espanyola de Pediatria (AEP). No substitueix la valoració del teu pediatre.",
  "A general guide based on the recommendations of the Spanish Association of Paediatrics (AEP). It doesn't replace your paediatrician's advice."),
]
X = lambda: '<span class="x">✕</span>'
EV = [
 (X(), ("Sal", "Nunca se añade. Sus riñones aún no la procesan bien."), ("Sal", "No se n'hi afegeix mai. Els seus ronyons encara no la processen bé."), ("Salt", "Never add it. Their kidneys can't handle it well yet.")),
 (X(), ("Azúcar y zumos", "Favorecen las caries y le acostumbran al dulce. Mejor la fruta entera."), ("Sucre i sucs", "Afavoreixen la càries i l'acostumen al dolç. Millor la fruita sencera."), ("Sugar and juices", "They promote tooth decay and a sweet tooth. Whole fruit is better.")),
 (X(), ("Miel", "Nunca antes de los 12 meses: puede llevar esporas de botulismo."), ("Mel", "Mai abans dels 12 mesos: pot portar espores de botulisme."), ("Honey", "Never before 12 months: it can carry botulism spores.")),
 (X(), ("Leche de vaca como bebida", "No antes de los 12 meses. Poco hierro y demasiada proteína para sus riñones."), ("Llet de vaca com a beguda", "No abans dels 12 mesos. Poc ferro i massa proteïna per als seus ronyons."), ("Cow's milk as a drink", "Not before 12 months. Little iron and too much protein for their kidneys.")),
 (I["Almendra"], ("Frutos secos enteros", "Hasta los 5 años, solo en crema o molidos muy finos."), ("Fruits secs sencers", "Fins als 5 anys, només en crema o molts molt fins."), ("Whole nuts", "Until age 5, only as nut butter or very finely ground.")),
 (I["Uvas"], ("Uvas y tomates cherry enteros", "Siempre en cuartos a lo largo. Igual con los arándanos."), ("Raïm i tomàquets cherry sencers", "Sempre en quarts al llarg. Igual amb els nabius."), ("Whole grapes and cherry tomatoes", "Always quartered lengthways. Same with blueberries.")),
 (X(), ("Pescados grandes", "Mucho mercurio: pez espada, emperador, tiburón (cazón, tintorera), atún rojo y lucio."), ("Peixos grans", "Molt mercuri: peix espasa, emperador, tauró (caçó, tintorera), tonyina vermella i lluç de riu."), ("Large fish", "High in mercury: swordfish, shark, bluefin tuna and pike.")),
 (I["Espinacas"], ("Espinacas, acelgas, remolacha, rúcula y apio", "Muchos nitratos. Nada antes de 12 meses; de 1 a 3 años, como mucho una ración al día. Borraja, nada antes de los 3 años."), ("Espinacs, bledes, remolatxa, ruca i api", "Molts nitrats. Res abans dels 12 mesos; d'1 a 3 anys, com a molt una ració al dia. Borratja, res abans dels 3 anys."), ("Spinach, chard, beetroot, rocket and celery", "High in nitrates. None before 12 months; from 1 to 3 years, one portion a day at most. Borage, none before age 3.")),
 (I["Arroz"], ("Bebida de arroz", "Acumula arsénico: mejor evitarla. El arroz y las tortitas de arroz, de vez en cuando."), ("Beguda d'arròs", "Acumula arsènic: millor evitar-la. L'arròs i les galetes d'arròs, de tant en tant."), ("Rice drink", "It builds up arsenic: best avoided. Rice and rice cakes, now and then.")),
]
LI = {'es': 0, 'ca': 1, 'en': 2}

DARK = ''':root{--bg:#1e1d46;--card:#28275a;--ink:#f1f0ff;--mute:#b9b6e6;--line:#3d3b7a;--green:#a29dff;--terra:#ff9f73;--red:#ff7b7b}
.back{background:#2b2a63}.ph img{background:#1c1a4b}'''

def fonts():
    f = lambda p: 'file://' + os.path.join(FONTS, p)
    return ('@font-face{font-family:"Luckiest Guy";src:url(%s)}\n@font-face{font-family:Montserrat;font-weight:100 900;src:url("%s")}\n'
            % (f('LuckiestGuy-Regular.ttf'), f('Montserrat[wght].ttf')))

def html(lang, dark=False):
    t = open(os.path.join(HERE, 'guia_template.html')).read()
    t = re.sub(r'(@font-face\{[^}]*\}\n)+', fonts(), t, count=1)
    k = LI[lang]
    if k:
        for row in T:
            assert row[0] in t, row[0][:60]
            t = t.replace(row[0], row[k])
    # contraportada: dos móviles con las capturas nuevas en vez del mockup antiguo
    sfx = '' if lang == 'es' else '-' + lang
    cap = lambda n: f'file://{WEB}/capturas/captura-{n}{sfx}.jpg'
    t = re.sub(r'<img class="mock" src="[^"]*">',
               f'<div class="phones"><div class="ph p1"><img src="{cap(2)}"></div><div class="ph p2"><img src="{cap(1)}"></div></div>', t)
    t = t.replace('.ph img{width:100%;height:100%;object-fit:cover;object-position:bottom;', '.ph img{width:100%;height:100%;object-fit:cover;object-position:top;')
    t = t.replace('</style>', '.phones{width:122mm;flex:none}\n</style>')
    if dark:
        t = t.replace('</style>', DARK + '\n</style>').replace('fill:#4a8760', 'fill:#a29dff')
    random.seed(4)
    pos = [(8,8),(30,20),(52,6),(74,18),(96,7),(118,16),(14,40),(124,42),(62,30),(37,182.7),(108.3,164.7),(82.4,187.8),(126.9,186.6),(57.1,169.4),(12.2,161.3)]
    names = ['Plátano','Fresas','Brócoli','Mandarina','Kiwi','Aguacate','Guisantes','Uvas','Pera','Zanahoria','Calabaza','Manzana','Fresas','Brócoli','Pera']
    sc = ''.join(I[n].replace('<svg class="fd"', f'<svg class="fd" style="left:{x}mm;top:{y}mm;transform:rotate({random.randint(-25,25)}deg)"') for n, (x, y) in zip(names, pos))
    iron = ''.join(I[n] for n in ["Pollo", "Merluza", "Huevo", "Lentejas"])
    evh = ''.join(f'<div>{r[0]}<span><b>{r[1+k][0]}</b><span>{r[1+k][1]}</span></span></div>' for r in EV)
    for a, b in {'__SCATTER__': sc, '__IRON__': iron, '__EVITAR__': evh}.items():
        assert a in t
        t = t.replace(a, b)
    return t

async def main():
    out = '/tmp/claude-0/guia'
    os.makedirs(out, exist_ok=True)
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        for lang in ['es', 'ca', 'en']:
            sfx = '' if lang == 'es' else '-' + lang
            for dark in [False, True]:
                f = f'{out}/guia_{lang}{"_dark" if dark else ""}.html'
                open(f, 'w').write(html(lang, dark))
                p = await b.new_page(viewport={'width': 560, 'height': 794}, device_scale_factor=1)
                await p.goto('file://' + f); await p.wait_for_timeout(600)
                await p.evaluate('document.fonts.ready')
                if not dark:
                    await p.pdf(path=f'{WEB}/guia-primeros-alimentos{sfx}.pdf', width='148mm', height='210mm', print_background=True)
                # previews de las dos primeras páginas, a 560x794
                await p.add_style_tag(content='.pg{zoom:%f}' % (560 / (148 / 25.4 * 96)))
                await p.wait_for_timeout(200)
                for n in (1, 2):
                    el = p.locator('section.pg').nth(n - 1)
                    await el.screenshot(path=f'{out}/g{n}.png')
                    from PIL import Image
                    Image.open(f'{out}/g{n}.png').convert('RGB').resize((560, 794)).save(
                        f'{WEB}/capturas/guia-{n}{sfx}{"-dark" if dark else ""}.jpg', quality=85, optimize=True, progressive=True)
                await p.close()
        await b.close()

if __name__ == '__main__':
    asyncio.run(main())
