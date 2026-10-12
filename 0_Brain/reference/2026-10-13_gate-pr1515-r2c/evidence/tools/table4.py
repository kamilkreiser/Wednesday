import sys; sys.path.insert(0, '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/f2077cbf-bb12-49ee-8d59-f5f537b335e0/scratchpad/g3/tools')
import harness
from harness import *
import os, time, json
only = set(sys.argv[1:])
def g(files, arm='complete'):
    dist = ('index.js', 'index.d.ts', 'thing/theThing.js', 'thing/theThing.d.ts') if arm == 'complete' else ('index.js', 'index.d.ts', 'thing/theThing.d.ts')
    f = base(dist=dist)
    f['tsconfig.test.json'] = tsconfig(exclude=['src/garbage'])
    for k, v in files.items(): f['src/garbage/' + k] = v
    return f
big_quotes = "''" * 9_000_000          # 18 MB, 9M string starts (> V8 Set limit 2^23)
big_ok = ("export const s = 'x'; // c\n" * 400_000)   # 11 MB, 400k strings, 400k comments, no specifier
quad = ''.join(f"// c{i}\nconst a{i} = require('@secuura/shared/thing');\n" for i in range(20000))
quad_big = ''.join(f"// c{i}\nconst a{i} = require('@secuura/shared/thing');\n" for i in range(60000))
T = [
 ('G1_unterminated_tokens', g({'u1.ts': "const s = 'abc", 'u2.ts': 'const t = `abc ${ x', 'u3.ts': '/* never closed', 'u4.ts': "const z = 'a\\", 'u5.ts': "import { X } from '@secuura/shared/thing"})),
 ('G2_regex_jsx_bait', g({'r.tsx': "const r = /'/; const q = /`/; const w = /\\/\\//; const v = /\\/*$/;\nexport const el = <div>it's `odd` /* not */ </div>;\nimport { X } from '@secuura/shared/thing';\n"})),
 ('G3_bom_crlf', g({'b.ts': '﻿import { X } from \'@secuura/shared/thing\';\r\n// \'@secuura/shared/thing\'\r\nexport const t = X;\r\n'})),
 ('G4_binary_invalid_utf8', g({'bin.ts': b'\x00\xff\xfe\xc3\x28' * 1000 + b"from '@secuura/shared/thing'" + b'\x00' * 100})),
 ('G4b_binary_runtime_gap', g({'bin.ts': b'\x00\xff\xfe\xc3\x28' * 1000 + b"from '@secuura/shared/thing'" + b'\x00' * 100}, arm='A')),
 ('G5_18MB_of_quotes_set_overflow', g({'big.ts': big_quotes})),
 ('G5b_11MB_ordinary_strings_and_comments', g({'big.ts': big_ok})),
 ('G6_quadratic_20k_comments_20k_specifiers', g({'q.ts': quad})),
 ('G6b_quadratic_60k', g({'q.ts': quad_big})),
]
for n, f in T:
    if only and n not in only: continue
    t = time.time(); measure(n, f, timeout=600); print('   secs', round(time.time() - t))
# FIFO, symlink loop, dangling, dir named .ts, unreadable: build then run by hand
if not only or 'G7' in only:
    f = g({'keep.ts': 'export const k = 1;\n'})
    d = build('G7_special_files', f, symlinks=[('src/garbage/loop.ts', 'loop.ts'), ('src/garbage/dangling.ts', 'nowhere.ts')], fifo=['src/garbage/fifo.ts'])
    os.makedirs(os.path.join(d, 'src/garbage/dir.ts'))
    p = os.path.join(d, 'src/garbage/noread.ts'); open(p, 'w').write("from '@secuura/shared/thing'"); os.chmod(p, 0)
    for k, c in CHECKERS.items():
        t = time.time(); rc, out = run(['node', c, d, '--baseline', os.path.join(d, 'baseline.txt')], timeout=90)
        print('G7_special_files', k, rc, round(time.time() - t), out[:300].replace('\n', ' | '))
    os.chmod(p, 0o644)
    # FIFO alone vs without: rerun with fifo removed to show it is the FIFO
# package.json oddities on the note side (imported package)
if not only or 'G8' in only:
    for label, pj in [('null', 'null'), ('number', '5'), ('exports_string', json.dumps(shared_pkg(exports='./dist/index.js'))),
                      ('exports_array', json.dumps(shared_pkg(exports=['./dist/index.js']))), ('exports_null_entry', json.dumps(shared_pkg(exports={'.': None, './thing': None}))),
                      ('tv_star_null', json.dumps(shared_pkg(typesVersions={'*': None}))), ('tv_string', json.dumps(shared_pkg(typesVersions='x'))),
                      ('main_number', json.dumps(shared_pkg(main=5, exports=None))), ('types_object', json.dumps(shared_pkg(types={'a': 1})))]:
        for arm in ('complete', 'A', 'B'):
            dist = {'complete': ('index.js', 'index.d.ts', 'thing/theThing.js', 'thing/theThing.d.ts'), 'A': ('index.js', 'index.d.ts', 'thing/theThing.d.ts'), 'B': ('index.js', 'index.d.ts', 'thing/theThing.js')}[arm]
            f = base(dist=dist); f[P + 'package.json'] = pj
            measure(f'G8_pkgjson_{label}_{arm}', f)
