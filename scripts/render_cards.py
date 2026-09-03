#!/usr/bin/env python3
"""Redraw the profile cards in assets/ from live GitHub data.

Fonts are declared as system stacks, not a single family: the SVG text is laid
out by whoever opens the page, so a face that only exists on macOS would be
substituted elsewhere and overflow the card. The banner is a PNG for the same
reason — it is rendered once, with the typeface it was designed in.

Run by .github/workflows/refresh-cards.yml once a day. Needs GITHUB_TOKEN in
the environment; locally `GITHUB_TOKEN=$(gh auth token) python scripts/render_cards.py`
does the job.

The cards are plain files in this repository rather than images fetched from a
rendering service at page-load time: the public github-readme-stats instance
answers 503 often enough that a profile depending on it shows broken images.
"""

import json
import os
import urllib.error
import urllib.request
from pathlib import Path
from xml.sax.saxutils import escape

USER = 'haku4130'
FEATURED = [
    'vendors-platform',
    'ml-malware-detector',
    'vpn-bot',
    'devops-bot',
    'ter-s-gallery-website',
    'hyperos-accessibility-guard',
]

# Palette shared with the banner.
BG = '#12222B'
BG_ALT = '#1B2E39'
BORDER = '#294450'
TITLE = '#E4A33A'
TEXT = '#B7CFCA'
MUTED = '#7E9BA1'
VALUE = '#F3F6F5'

ASSETS = Path(__file__).resolve().parent.parent / 'assets'
TOKEN = os.environ.get('GITHUB_TOKEN', '')


def api(path):
    req = urllib.request.Request(f'https://api.github.com{path}')
    req.add_header('Accept', 'application/vnd.github+json')
    if TOKEN:
        req.add_header('Authorization', f'Bearer {TOKEN}')
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def graphql(query):
    body = json.dumps({'query': query}).encode()
    req = urllib.request.Request('https://api.github.com/graphql', data=body)
    req.add_header('Authorization', f'Bearer {TOKEN}')
    req.add_header('Content-Type', 'application/json')
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def wrap(text, max_chars, max_lines):
    """Greedy word wrap; the last line gets an ellipsis if anything is dropped."""
    words, lines, cur = text.split(), [], ''
    for w in words:
        candidate = f'{cur} {w}'.strip()
        if len(candidate) <= max_chars:
            cur = candidate
        else:
            lines.append(cur)
            cur = w
            if len(lines) == max_lines:
                break
    if cur and len(lines) < max_lines:
        lines.append(cur)
    used = len(' '.join(lines).split())
    if used < len(words):
        lines[-1] = lines[-1].rstrip('.,;—-') + '…'
    return lines


def card(name, description, background):
    lines = wrap(description, 52, 3)
    body = ''.join(
        f'<text x="22" y="{68 + i * 21}" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif" '
        f'font-size="13.5" fill="{TEXT}">{escape(line)}</text>'
        for i, line in enumerate(lines)
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="420" height="140" viewBox="0 0 420 140" role="img" aria-label="{escape(name)}">
  <rect x="0.6" y="0.6" width="418.8" height="138.8" rx="8" fill="{background}" stroke="{BORDER}" stroke-width="1.2"/>
  <text x="22" y="40" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, Liberation Mono, monospace" font-size="15.5" font-weight="700" fill="{TITLE}">{escape(name)}</text>
  {body}
</svg>
'''


# Drawn as paths on a 16x16 grid rather than pulled from an icon font: an SVG
# shown through <img> may not fetch anything external, so everything the card
# needs has to be inside it.
ICONS = {
    # a commit: a node on a line
    'commits': '<path d="M0 8h4.2M11.8 8H16"/><circle cx="8" cy="8" r="3.1"/>',
    # a pull request: a branch that ends in an arrow
    'pulls': ('<circle cx="4" cy="3" r="2"/><path d="M4 5v6"/><circle cx="4" cy="13" r="2"/>'
              '<circle cx="12" cy="3" r="2"/><path d="M12 5v6.6"/>'
              '<path d="M9.7 10.4 12 13.2l2.3-2.8"/>'),
    # a repository: a book seen spine-on
    'repos': '<rect x="2" y="1.8" width="12" height="12.4" rx="1.6"/><path d="M5.2 1.8v12.4"/>',
}


def stats_card(rows):
    """One wide strip under the project grid: three figures side by side."""
    width, height = 856, 126
    body = ''
    for i, (icon, value, label) in enumerate(rows):
        x = 30 + i * 282
        body += (f'<g transform="translate({x} 45) scale(1.25)" fill="none" stroke="{MUTED}" '
                 f'stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">{ICONS[icon]}</g>')
        body += (f'<text x="{x + 32}" y="{65.5}" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif" '
                 f'font-size="30" font-weight="600" fill="{VALUE}">{value}</text>')
        body += (f'<text x="{x}" y="{92}" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif" '
                 f'font-size="13.5" fill="{MUTED}">{escape(label)}</text>')
    dividers = ''.join(
        f'<line x1="{30 + i * 282 - 26}" y1="40" x2="{30 + i * 282 - 26}" y2="102" stroke="{BORDER}" stroke-width="1.2"/>'
        for i in (1, 2))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Activity">
  <rect x="0.6" y="0.6" width="{width - 1.2}" height="{height - 1.2}" rx="8" fill="{BG}" stroke="{BORDER}" stroke-width="1.2"/>
  <text x="30" y="26" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, Liberation Mono, monospace" font-size="13" font-weight="700" letter-spacing="1.6" fill="{TITLE}">ACTIVITY</text>
  {dividers}
  {body}
</svg>
'''


def main():
    ASSETS.mkdir(exist_ok=True)

    for index, name in enumerate(FEATURED):
        repo = api(f'/repos/{USER}/{name}')
        # The cards sit in a two-column grid, so column + row parity gives the
        # checkerboard: (0,0) dark, (0,1) light, (1,0) light, and so on.
        column, row = index % 2, index // 2
        background = BG_ALT if (column + row) % 2 else BG
        (ASSETS / f'card-{name}.svg').write_text(card(name, repo.get('description') or '', background))
        print(f'card-{name}.svg')

    # Counted over public, non-fork, not archived repositories — exactly the
    # population the profile itself shows.
    page = 1
    public_repos = 0
    while True:
        batch = api(f'/users/{USER}/repos?per_page=100&page={page}&type=owner')
        if not batch:
            break
        for repo in batch:
            if repo['fork'] or repo['private'] or repo['archived']:
                continue
            public_repos += 1
        page += 1

    data = graphql(f'''{{ user(login: "{USER}") {{
        contributionsCollection {{ totalCommitContributions totalPullRequestContributions }}
    }} }}''')['data']['user']['contributionsCollection']

    rows = [
        ('commits', str(data['totalCommitContributions']), 'commits, last 12 months'),
        ('pulls', str(data['totalPullRequestContributions']), 'pull requests opened'),
        ('repos', str(public_repos), 'active public repositories'),
    ]
    (ASSETS / 'card-stats.svg').write_text(stats_card(rows))
    print('card-stats.svg')


if __name__ == '__main__':
    main()
