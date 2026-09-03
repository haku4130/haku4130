#!/usr/bin/env python3
"""Redraw assets/banner-{dark,light}.{svg,png}.

Run by hand, not by CI: the banner is set in Avenir Next, which a GitHub runner
does not have, and it is shipped as a PNG precisely so that the typeface is the
one it was designed in rather than whatever the reader's machine substitutes.

    python scripts/render_banner.py && \
      for t in dark light; do rsvg-convert -w 2000 -h 416 assets/banner-$t.svg -o assets/banner-$t.png; done
"""

from pathlib import Path

NAME = 'Andrey Osipov'
ROLE = 'PYTHON BACKEND DEVELOPER'
META = 'Belgrade &#183; aosipov.dev'

THEMES = {
    'dark':  dict(bg='#12222B', name='#F3F6F5', mono='#8FB3AC', line='#2C4854',
                  accent='#E4A33A', node='#5B8089'),
    'light': dict(bg='#E9EEEF', name='#12222B', mono='#4C6C74', line='#B4C6CA',
                  accent='#B8760F', node='#7E9BA1'),
}

# The line of nodes ending in an arrowhead at the role is the point of the
# banner: a request crossing a few hops and arriving at him.
TEMPLATE = '''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="208" viewBox="0 0 1000 208" role="img" aria-label="{name_text} — Python backend developer">
  <rect width="1000" height="208" fill="{bg}"/>

  <text x="64" y="104" font-family="Avenir Next, Avenir, Helvetica Neue, sans-serif"
        font-size="60" font-weight="600" letter-spacing="-0.9" fill="{name}">{name_text}</text>

  <path d="M66 152 H206" stroke="{line}" stroke-width="1.6" fill="none"/>
  <circle cx="66"  cy="152" r="4.2" fill="{node}"/>
  <circle cx="118" cy="152" r="4.2" fill="{node}"/>
  <circle cx="170" cy="152" r="4.2" fill="{node}"/>
  <path d="M206 146 L219 152 L206 158 Z" fill="{accent}"/>

  <text x="237" y="158" font-family="Menlo, DejaVu Sans Mono, monospace"
        font-size="18" letter-spacing="3.2" fill="{mono}">{role}</text>

  <text x="936" y="158" text-anchor="end" font-family="Menlo, DejaVu Sans Mono, monospace"
        font-size="14" letter-spacing="1.4" fill="{mono}">{meta}</text>
</svg>
'''

assets = Path(__file__).resolve().parent.parent / 'assets'
for theme, colors in THEMES.items():
    target = assets / f'banner-{theme}.svg'
    target.write_text(TEMPLATE.format(name_text=NAME, role=ROLE, meta=META, **colors))
    print(target.name)
