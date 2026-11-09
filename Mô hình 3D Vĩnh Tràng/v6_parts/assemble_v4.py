#!/usr/bin/env python3
"""Assemble trai-nghiem-vinh-trang-v4.html from parts in this dir.
Also writes the TESTLOCAL copy (importmap -> local vendor three.js) for headless verification."""
import os

D = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(D), 'trai-nghiem-vinh-trang-v4.html')
TEST = os.path.join(os.path.dirname(D), 'trai-nghiem-vinh-trang-v4-TESTLOCAL.html')

parts = []
parts.append(open(os.path.join(D, 'head_css.html'), encoding='utf-8').read())
for p in ['modal_lamp.html', 'modal_arhat.html', 'modal_shop.html', 'modal_order.html', 'modal_so.html']:
    parts.append(open(os.path.join(D, p), encoding='utf-8').read())
parts.append('\n  <script type="module">\n')
for i in range(1, 8):
    if i == 6:
        parts.append(open(os.path.join(D, 'module_6a.js'), encoding='utf-8').read())
        parts.append(open(os.path.join(D, 'module_6b.js'), encoding='utf-8').read())
    else:
        parts.append(open(os.path.join(D, f'module_{i}.js'), encoding='utf-8').read())
parts.append('  </script>\n')
parts.append('  <script>\n' + open(os.path.join(D, 'v2.js'), encoding='utf-8').read() + '\n  </script>\n')
parts.append('  <script>\n' + open(os.path.join(D, 'v3.js'), encoding='utf-8').read() + '\n  </script>\n')
parts.append('</body>\n</html>\n')
html = '\n'.join(parts)
open(OUT, 'w', encoding='utf-8').write(html)
print('wrote', OUT, len(html), 'chars')

test = html.replace(
    '  "three": "https://unpkg.com/three@0.160.0/build/three.module.js",\n  "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/"',
    '  "three": "./v4_parts/vendor/three.module.js",\n  "three/addons/": "./v4_parts/vendor/"')
assert './v4_parts/vendor/three.module.js' in test
open(TEST, 'w', encoding='utf-8').write(test)
print('wrote', TEST, len(test), 'chars')
