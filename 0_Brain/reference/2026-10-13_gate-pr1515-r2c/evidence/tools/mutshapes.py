import sys; sys.path.insert(0, '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/f2077cbf-bb12-49ee-8d59-f5f537b335e0/scratchpad/g3/tools')
import harness, json, os
from harness import *
from table1 import sa, DT, JT, T as T1
G = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/f2077cbf-bb12-49ee-8d59-f5f537b335e0/scratchpad/g3'
src = open(G + '/tools/mutants.py').read()
ns = {}
exec(src[:src.index('def score')].replace("assert SHA.startswith", "pass #"), ns)
ORIG = open(G + '/head/Blockchain/Dev/scripts/typecheck-tests/check.cjs').read()
want = ['A11_first_target_only', 'C1_any_module_any_code_TS7016_or_2307', 'C2_TS2307_any_module', 'C4_any_mention_of_specifier', 'C5_ignore_diagnostic_entirely_scan_decides']
for mid, old, new in ns['M']:
    if mid in want:
        assert ORIG.count(old) == 1, mid
        p = G + f'/mut/Blockchain/Dev/scripts/typecheck-tests/mut_{mid}.cjs'
        open(p, 'w').write(ORIG.replace(old, new))
        harness.CHECKERS[mid] = p
STALE_B = ('index.js', 'index.d.ts', JT)
shapes = {k: v for k, v in T1}
S2 = []
# distinguishing shapes
S2.append(('D_R2_star_before_longer', shapes['R2_star_before_longer']))
S2.append(('D_R1_root_types_redirect', shapes['R1_root_types_redirect']))
S2.append(('D_R3_version_range', shapes['R3_version_range']))
S2.append(('D_R9_backslash_target', shapes['R9_backslash_target']))
f = base(); f['node_modules/thirdparty/package.json'] = json.dumps({'name': 'thirdparty', 'main': 'index.js', 'types': 'index.d.ts'}); f['node_modules/thirdparty/index.js'] = 'module.exports={X:1}\n'
f['src/u2.ts'] = "import { X as Y } from 'thirdparty';\nexport const y = Y;\n"
S2.append(('D_thirdparty_types_missing_TS7016', f))
f = base(); f['node_modules/thirdparty/package.json'] = json.dumps({'name': 'thirdparty', 'main': 'index.js', 'types': 'index.d.ts', 'typesVersions': {'*': {'sub': ['dist/sub.d.ts']}}}); f['node_modules/thirdparty/index.js'] = 'module.exports={X:1}\n'
f['src/u2.ts'] = "import { X as Y } from 'thirdparty/sub';\nexport const y = Y;\n"
S2.append(('D_thirdparty_subpath_TS2307', f))
S2.append(('D_echo_no_phrase_TS2322_target_absent', {**base(dist=STALE_B, use=None), 'src/__tests__/echo.test.ts': 'export const e: "a" = "@secuura/shared/thing";\n'}))
S2.append(('D_array_divergence_second_exists', sa({'./sub/*': './dist/sub/*.js'}, {'*': ['dist/x/*', 'dist/nope/*'], 'sub/*': ['dist/sub/*.d.ts']}, ['nope/sub/a.d.ts'], 'sub/a')))
for n, f in S2: measure(n, f)
