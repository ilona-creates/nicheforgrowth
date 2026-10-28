#!/usr/bin/env python3
"""Regenerate freeresource/index.html from index.html.

/freeresource/ is the shareable link for the freebie section. It is a full copy of the
home page with its own social preview tags that scrolls to the freebie section on
load, so the address never contains a #. Run this after every edit to index.html:

    python3 scripts/build-freeresource.py
"""
import re, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
src = (root / 'index.html').read_text(encoding='utf-8', newline='')
nl = '\r\n' if '\r\n' in src else '\n'
URL = 'https://ilonamelnychuk.com/freeresource/'
IMG = 'https://ilonamelnychuk.com/og-free-resource.jpg'
TITLE = 'Uncover needs your clients would pay for, with 3 questions'
DESC = 'Not a non-committal desire. A need they’d pay for. Get the free resource from Product-Market-Fit Sprint.'

def sub(pattern, repl, s):
    out, n = re.subn(pattern, lambda m: repl, s, count=1)
    assert n == 1, pattern
    return out

s = src
s = sub(r'<title>.*?</title>', '<title>%s — Product-Market-Fit Sprint</title>' % TITLE, s)
s = sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">' % DESC, s)
s = sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="%s">' % TITLE, s)
s = sub(r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="%s">' % DESC, s)
s = sub(r'<meta property="og:image" content="[^"]*">', '<meta property="og:image" content="%s">' % IMG, s)
s = sub(r'<meta name="twitter:image" content="[^"]*">', '<meta name="twitter:image" content="%s">' % IMG, s)
s = sub(r'<meta property="og:url" content="[^"]*">', '<meta property="og:url" content="%s">' % URL + nl + '<link rel="canonical" href="%s">' % URL, s)
jump = ('<script>history.scrollRestoration="manual";window.addEventListener("load",function(){'
        'var f=document.getElementById("freebie");if(f){f.scrollIntoView({behavior:"instant"});}});</script>')
s = sub(r'</body>', jump + nl + '</body>', s)
(root / 'freeresource').mkdir(exist_ok=True)
(root / 'freeresource' / 'index.html').write_text(s, encoding='utf-8', newline='')
print('wrote freeresource/index.html')
