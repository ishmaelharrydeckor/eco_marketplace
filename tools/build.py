"""Builds index.html: nav panel markup is pulled from a saved copy of the original page (path in argv[1])."""
import re, sys
src = open(sys.argv[1]).read()
CDN = 'https://cdn.prod.website-files.com/67af51ad91d062ee8ef52137/'

body = src[src.find('<body'):]
body = re.sub(r'<script.*?</script>|<svg.*?</svg>|<link rel="noopener"/>', '', body, flags=re.S)
def balanced(html, start_marker):
    i = re.search(start_marker, html).start(); depth = 0
    for t in re.finditer(r'<(/?)div\b[^>]*>', html[i:]):
        depth += -1 if t.group(1) else 1
        if depth == 0:
            return html[i:i + t.end()]
menu = balanced(body, r'<div[^>]*class="nav3-menu"[^>]*>')
menu = menu.replace('src="https://cdn.prod.website-files.com/67af51ad91d062ee8ef52137/', 'src="' + CDN)
menu = re.sub(r'\s(?:data-[\w-]+|href|target|loading|srcset|sizes)="[^"]*"', '', menu)
menu = menu.replace(' w-inline-block', '').replace(' w--current', '')
menu = re.sub(r'<a class="([^"]*)">', r'<a class="\1" href="#">', menu)
tpl = open('tools/template.html').read()
out = tpl.replace('{{CDN}}', CDN).replace('{{NAV_MENU}}', menu)
open('index.html', 'w').write(out)
print('ok', len(out) // 1024, 'KB')
