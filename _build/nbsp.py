# Evita palabras cortas sueltas al final de línea en los títulos:
# une con espacio duro la palabra corta con la siguiente.
import re
_SHORT = r'(?<![\wáéíóúñÁÉÍÓÚÑ])(sin|con|de|del|la|el|los|las|lo|en|y|o|a|al|un|una|tu|su|ya|que|por|para|te|se|mi|es|qué|más|le|ni)\s+(?=[\wáéíóúñÁÉÍÓÚÑ¿¡])'
def _fix(m):
    inner = m.group(2)
    return m.group(1) + re.sub(_SHORT, lambda k: k.group(1) + '&nbsp;', inner, flags=re.I) + m.group(3)
def titulos(html):
    return re.sub(r'(<h[1-3][^>]*>)([^<]*)(</h[1-3]>)', _fix, html)
