# Web de Primeros Alimentos

Home, blog y guía de www.primerosalimentos.com.

Las plantillas, los artículos, los borradores y los scripts que generan el blog están en el repo privado **primeros-alimentos-privado** (`_build/`). Aquí solo está lo publicado. `/borradores/` redirige a admin.primerosalimentos.com, que es donde se ven y se editan.

## Idiomas

- **Home (`index.html`)**: castellano, catalán e inglés. Elige el idioma del dispositivo, se puede cambiar arriba (ES · CA · EN) y se guarda. Enlace directo: `/?lang=ca` o `/?lang=en`. Los textos en catalán e inglés están en el script "Idiomas" del final de `index.html`.
- **Blog**: se escribe y se publica en castellano. `_build/idiomas.py` (repo privado) crea `/ca/blog/` y `/en/blog/` con las traducciones de `_build/traducciones/<idioma>/_comun.json` (o `<slug>.json`). Un artículo sin todas sus traducciones se queda solo en castellano y el script avisa.
  - `python3 _build/idiomas.py pendientes` (desde el repo privado) lista lo que falta por traducir.
  - `python3 _build/idiomas.py` genera las páginas, el selector de idioma, los `hreflang` y el sitemap. `publicar_siguiente.py` ya lo ejecuta al publicar.
