import sys; sys.path.insert(0, '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/f2077cbf-bb12-49ee-8d59-f5f537b335e0/scratchpad/g3/tools')
from harness import *
from table1 import sa, DT, JT
import json, os, time
only = set(sys.argv[1:])
STALE_B = ('index.js', 'index.d.ts', JT)
NOUSE = lambda dist: base(dist=dist, use=None)
ECHO1 = 'export const e: "a" = "Cannot find module \'@secuura/shared/thing\'";\n'
ECHO2 = 'export type T = `Could not find a declaration file for module \'@secuura/shared/thing\'`; export const e: T = "x";\n'
def g(files, dist=('index.js', 'index.d.ts', 'thing/theThing.js', 'thing/theThing.d.ts'), use="import { X } from '@secuura/shared/thing';\nexport const t: number = X;\n"):
    f = base(dist=dist, use=use); f['tsconfig.test.json'] = tsconfig(exclude=['src/garbage'])
    for k, v in files.items(): f['src/garbage/' + k] = v
    return f
CAP = 4 * 1024 * 1024
T = []  # (name, files, init, fifo)
T.append(('E1_echo_TS2322_unimported_absent', {**NOUSE(STALE_B), 'src/__tests__/echo.test.ts': ECHO1}, None, ()))
T.append(('E1b_echo_baselined', {**NOUSE(STALE_B), 'src/__tests__/echo.test.ts': ECHO1}, 'dev', ()))
T.append(('E1c_echo_complete_build', {**NOUSE(('index.js','index.d.ts',JT,DT)), 'src/__tests__/echo.test.ts': ECHO1}, None, ()))
T.append(('E2_template_literal_7016_phrase', {**NOUSE(STALE_B), 'src/__tests__/echo.test.ts': ECHO2}, None, ()))
T.append(('E4_echo_in_object', {**NOUSE(STALE_B), 'src/__tests__/echo.test.ts': 'export const e: { m: "a" } = { m: "Cannot find module \'@secuura/shared/thing\'" };\n'}, None, ()))
T.append(('E5_echo_prefix_quote', {**NOUSE(STALE_B), 'src/__tests__/echo.test.ts': 'export const e: 1 = "x"; // Cannot find module \'@secuura/shared/thing\'\n'}, None, ()))
T.append(('Z1_genuine_TS7016_armB', base(dist=STALE_B), None, ()))
T.append(('Z2_genuine_TS2307_armD', base(dist=('index.js', 'index.d.ts')), None, ()))
big = "''" * 8_400_000
T.append(('Z4_genuine_armB_plus_16MB_file_and_FIFO', g({'big.ts': big, 'k.ts': 'export const k=1;\n'}, dist=STALE_B), None, ('src/garbage/fifo.ts',)))
T.append(('Z5_genuine_armD_plus_16MB_file_and_FIFO', g({'big.ts': big, 'k.ts': 'export const k=1;\n'}, dist=('index.js','index.d.ts')), None, ('src/garbage/fifo.ts',)))
T.append(('G5_16.8MB_quotes_complete', g({'big.ts': big}), None, ()))
T.append(('G7a_fifo_complete', g({'k.ts': 'export const k=1;\n'}), None, ('src/garbage/fifo.ts',)))
T.append(('G7c_fifo_under_dist_dirs_complete', g({'k.ts': 'export const k=1;\n'}), None, ('src/garbage/sub/deep/fifo.tsx',)))
# cap boundary: file exactly CAP (scanned), CAP+1 (skipped); filler is plain comment text
def padded(n, tail="import { X } from '@secuura/shared/thing';\n"):
    return ('// ' + 'x' * 70 + '\n') * ((n - len(tail)) // 74) + tail
T.append(('B1_cap_file_scanned_armA_gap_expect_note', g({'at.ts': padded(CAP - 100)}, dist=('index.js','index.d.ts',DT), use=None), None, ()))
T.append(('B2_cap_file_over_cap_armA_gap_expect_no_note', g({'over.ts': padded(CAP + 100)}, dist=('index.js','index.d.ts',DT), use=None), None, ()))
# in-cap slowness: 4MiB of comment+specifier pairs (the quadratic inAny)
pair = "//\nfrom'@secuura/shared/thing'\n"
T.append(('Q1_4MiB_comment_specifier_pairs', g({'q.ts': pair * ((CAP - 10) // len(pair))}), None, ()))
pair2 = "//\nrequire('@secuura/a')\n"
T.append(('Q2_4MiB_comment_specifier_pairs_min', g({'q.ts': pair2 * ((CAP - 10) // len(pair2))}), None, ()))
T.append(('Q3_4MiB_of_quote_pairs', g({'q.ts': "''" * ((CAP - 10) // 2)}), None, ()))
T.append(('Q4_4MiB_backtick_pairs', g({'q.ts': "``" * ((CAP - 10) // 2)}), None, ()))
T.append(('Q5_4MiB_slashstar_pairs', g({'q.ts': "/**/" * ((CAP - 10) // 4)}), None, ()))
for n, f, init, fifo in T:
    if only and n not in only: continue
    t = time.time(); measure(n, f, init_with=init, fifo=fifo, timeout=150); print('   secs', round(time.time() - t))
