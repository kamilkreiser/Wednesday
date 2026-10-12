import sys; sys.path.insert(0, '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/f2077cbf-bb12-49ee-8d59-f5f537b335e0/scratchpad/g3/tools')
import harness, json
from harness import *
from table1 import sa
import table6
H = open(S + '/head/Blockchain/Dev/scripts/typecheck-tests/check.cjs').read()
def mk(name, pairs):
    s = H
    for o, n in pairs:
        assert s.count(o) == 1, (name, o); s = s.replace(o, n)
    p = S + f'/head/Blockchain/Dev/scripts/typecheck-tests/mut_{name}.cjs'; os.makedirs(S + '/mutfiles', exist_ok=True)
    open(p, 'w').write(s); return p
T2 = mk('T2', [("} catch {\n  // Advisory only: a note we cannot compute is a note we do not print. Never a failure.\n}", "} catch { process.exit(0); }")])
C1 = mk('C1', [("  /^(?:Cannot find module|Could not find a declaration file for module) '(@secuura\\/[^']+)'/;\nconst SPLIT_SPEC = /^(@secuura\\/[a-z0-9._-]+)(?:\\/(.*))?$/;",
                "  /^(?:Cannot find module|Could not find a declaration file for module) '([^']+)'/;\nconst SPLIT_SPEC = /^((?:@[^/]+\\/)?[^/]+)(?:\\/(.*))?$/;")])
print('anchors landed; sha', hashlib.sha256(open(T2,'rb').read()).hexdigest()[:8], hashlib.sha256(open(C1,'rb').read()).hexdigest()[:8]) if False else None
harness.CHECKERS.clear(); harness.CHECKERS.update({'head': S + '/head/Blockchain/Dev/scripts/typecheck-tests/check.cjs', 'T2': T2, 'C1': C1})
f = table6.nullroot('null'); f['src/__tests__/bad.test.ts'] = 'export const bad: number = "x";\n'
measure('M_T2_N6', f)
f = base(); f['node_modules/thirdparty/package.json'] = json.dumps({'name': 'thirdparty', 'main': 'index.js', 'types': 'index.d.ts'}); f['node_modules/thirdparty/index.js'] = 'module.exports={X:1}\n'
f['src/u2.ts'] = "import { X as Y } from 'thirdparty';\nexport const y = Y;\n"
measure('M_C1_thirdparty_types_missing', f)
