import sys; sys.path.insert(0, '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/f2077cbf-bb12-49ee-8d59-f5f537b335e0/scratchpad/g3/tools')
from harness import *
P2 = 'node_modules/@secuura/shared/'
def nullroot(pj):
    return {'tsconfig.test.json': tsconfig(), 'baseline.txt': ZERO, 'src/__tests__/a.test.ts': CLEAN,
            P2 + 'package.json': pj, P2 + 'index.d.ts': 'export declare const X: number;\n', P2 + 'index.js': 'module.exports={X:1};\n',
            'src/u.ts': "import { X } from '@secuura/shared';\nexport const t: number = X;\n"}
def main():
    measure('N1_null_pkgjson_root_import_tsc_happy', nullroot('null'))
    measure('N2_object_pkgjson_root_import_control', nullroot('{"name":"@secuura/shared"}'))
    measure('N3_number_pkgjson_root_import', nullroot('5'))
    measure('N4_array_pkgjson_root_import', nullroot('[]'))
    measure('N5_string_pkgjson_root_import', nullroot('"x"'))
    # note block throws (null package.json, root import, tsc happy about it) AND a real verdict exists elsewhere
    f = nullroot('null'); f['src/__tests__/bad.test.ts'] = 'export const bad: number = "x";\n'
    measure('N6_note_throws_plus_NEW_type_error_expect_1', f)
    f = nullroot('null')
    for rel, body in base(dist=('index.js', 'index.d.ts', 'thing/theThing.js'), pkgdir='node_modules/@secuura/crypto/').items():
        if rel.startswith('node_modules/@secuura/crypto/'): f[rel] = body.replace('@secuura/shared', '@secuura/crypto') if rel.endswith('package.json') else body
    f['src/u2.ts'] = "import { X as Y } from '@secuura/crypto/thing';\nexport const y: number = Y;\n"
    measure('N7_note_throws_plus_genuine_stale_pkg_expect_2', f)
if __name__ == '__main__': main()
