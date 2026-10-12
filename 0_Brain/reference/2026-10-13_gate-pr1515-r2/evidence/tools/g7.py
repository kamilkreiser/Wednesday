import sys; sys.path.insert(0, '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/ad6cb59d-4a2f-44e5-b355-5685c7d2a2e1/scratchpad/g2/tools')
from harness import *
from table4 import g
import os, time
d = build('G7a_fifo_only', g({'keep.ts': 'export const k = 1;\n'}), fifo=['src/garbage/fifo.ts'])
for k, c in CHECKERS.items():
    t = time.time(); rc, out = run(['node', c, d, '--baseline', os.path.join(d, 'baseline.txt')], timeout=60); print('G7a_fifo_only', k, rc, round(time.time() - t))
d = build('G7b_no_fifo', g({'keep.ts': 'export const k = 1;\n'}), symlinks=[('src/garbage/loop.ts', 'loop.ts'), ('src/garbage/dangling.ts', 'nowhere.ts'), ('src/garbage/dirlink', '..')])
os.makedirs(os.path.join(d, 'src/garbage/dir.ts'))
p = os.path.join(d, 'src/garbage/noread.ts'); open(p, 'w').write("from '@secuura/shared/thing'"); os.chmod(p, 0)
os.chmod(os.path.join(d, 'src/garbage/dir.ts'), 0)
for k, c in CHECKERS.items():
    t = time.time(); rc, out = run(['node', c, d, '--baseline', os.path.join(d, 'baseline.txt')], timeout=60); print('G7b_loop_dangling_dir_noread', k, rc, round(time.time() - t), out[:200].replace('\n', ' | '))
os.chmod(p, 0o644); os.chmod(os.path.join(d, 'src/garbage/dir.ts'), 0o755)
