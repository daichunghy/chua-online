#!/usr/bin/env python3
"""Assemble trai-nghiem-vinh-trang-v7.html from parts in this dir (v7_parts).
Also writes the TESTLOCAL copy (importmap -> local vendor three.js) for headless verification.
v7: thay toàn bộ nhân vật khối tự chế bằng 3 GLB rigged chuẩn của dự án
(user/files/*-chuyen-dong.glb), nhúng base64 ngay trong HTML để mở bằng
double-click (file://) vẫn nạp được model — GLB ~12,8 MB -> base64 ~17 MB.
modal_lamp.html + modal_arhat.html are NOT included (as in v5/v6)."""
import base64
import os

D = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(D), 'trai-nghiem-vinh-trang-v7.html')
TEST = os.path.join(os.path.dirname(D), 'trai-nghiem-vinh-trang-v7-TESTLOCAL.html')

GLB_FILES = {
    'nu': os.path.expanduser('~/workspace/user/files/nu-phuc-hoi-mau-chuyen-dong.glb'),
    'nam': os.path.expanduser('~/workspace/user/files/nam-chuyen-dong.glb'),
    'tre': os.path.expanduser('~/workspace/user/files/tre-em-chuyen-dong.glb'),
}
b64 = {}
for kind, path in GLB_FILES.items():
    with open(path, 'rb') as f:
        b64[kind] = base64.b64encode(f.read()).decode('ascii')
    print('glb', kind, path, len(b64[kind]), 'b64 chars')
data_script = ('  <script>\n    window.__GLB_B64 = {'
               + ','.join(f'{k}: "{v}"' for k, v in b64.items())
               + '};\n  </script>\n')

parts = []
parts.append(open(os.path.join(D, 'head_css.html'), encoding='utf-8').read())
for p in ['modal_shop.html', 'modal_order.html', 'modal_so.html']:
    parts.append(open(os.path.join(D, p), encoding='utf-8').read())
parts.append(data_script)
parts.append('\n  <script type="module">\n')
for i in range(1, 8):
    if i == 6:
        parts.append(open(os.path.join(D, 'module_6a.js'), encoding='utf-8').read())
        parts.append(open(os.path.join(D, 'module_6b.js'), encoding='utf-8').read())
    else:
        parts.append(open(os.path.join(D, f'module_{i}.js'), encoding='utf-8').read())
parts.append('__MODULE_END__')
parts.append('  <script>\n' + open(os.path.join(D, 'v2.js'), encoding='utf-8').read() + '\n  </script>\n')
parts.append('  <script>\n' + open(os.path.join(D, 'v3.js'), encoding='utf-8').read() + '\n  </script>\n')
parts.append('</body>\n</html>\n')
raw = '\n'.join(parts)

html = raw.replace('__MODULE_END__', '  </script>\n')
open(OUT, 'w', encoding='utf-8').write(html)
print('wrote', OUT, len(html), 'chars')

# HARNESS KIỂM THỬ — chỉ bản TESTLOCAL: tua nhanh tất định qua module_7.tick()
# (logic chạy vẫn là 100% logic vòng lặp thật; bản phát hành KHÔNG có hook này).
HOOK = '''
    // === HARNESS KIỂM THỬ (chỉ TESTLOCAL) ===
    window.__v6ff = (frames) => {
      const n = Math.max(0, Math.min(4000, frames | 0));
      for (let i = 0; i < n; i++) tick(0.05, false);
      tick(0, true);
    };
'''
test = raw.replace('__MODULE_END__', HOOK + '  </script>\n')
test = test.replace(
    '  "three": "https://unpkg.com/three@0.160.0/build/three.module.js",\n  "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/"',
    '  "three": "./v7_parts/vendor/three.module.js",\n  "three/addons/": "./v7_parts/vendor/"')
assert './v7_parts/vendor/three.module.js' in test
assert '__v6ff' in test and '__v6ff' not in html
open(TEST, 'w', encoding='utf-8').write(test)
print('wrote', TEST, len(test), 'chars')
