import sys; sys.path.insert(0, '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/f2077cbf-bb12-49ee-8d59-f5f537b335e0/scratchpad/g3/tools')
from harness import *
DT = 'thing/theThing.d.ts'; JT = 'thing/theThing.js'
def sa(exp, tv, dist, sub, kind='import', **pj):
    p = shared_pkg(exports={'.': './dist/index.js', **exp}, typesVersions={'*': tv}, **pj)
    return base(p, dist=('index.js', 'index.d.ts') + tuple(dist), use=use('@secuura/shared/' + sub, kind))
T = []
# ---- complete-build shapes from round 0 / round 1 (tsc should be happy)
T.append(('L1_1_trailing_star_extless', sa({'./sub/*': './dist/sub/*.js'}, {'sub/*': ['dist/sub/*']}, ['sub/a.d.ts', 'sub/a.js'], 'sub/a')))
T.append(('L1_2_bare_star', sa({'./*': './dist/*.js'}, {'*': ['dist/*']}, ['thing.d.ts', 'thing.js'], 'thing')))
T.append(('L1_3_literal_extless', sa({'./e': './dist/e.js'}, {'e': ['dist/e']}, ['e.d.ts', 'e.js'], 'e')))
T.append(('L1_4_array_first_absent', sa({'./f': './dist/f.js'}, {'f': ['src/f.d.ts', 'dist/f.d.ts']}, ['f.d.ts', 'f.js'], 'f')))
T.append(('dir_target', sa({'./d': './dist/d/index.js'}, {'d': ['dist/d']}, ['d/index.d.ts', 'd/index.js'], 'd')))
p = shared_pkg(types='index.d.ts', typesVersions={'*': {'*': ['dist/*']}})
T.append(('R1_root_types_redirect', base(p, dist=('index.js', 'index.d.ts'), use=use('@secuura/shared', 'root'))))
p = shared_pkg(types='./index.d.ts', typesVersions={'*': {'index.d.ts': ['dist/index.d.ts']}})
T.append(('R1b_root_literal_redirect', base(p, dist=('index.js', 'index.d.ts'), use=use('@secuura/shared', 'root'))))
T.append(('R2_star_before_longer', sa({'./sub/*': './dist/other/*.js'}, {'*': ['dist/*.d.ts'], 'sub/*': ['dist/other/*.d.ts']}, ['other/a.d.ts', 'other/a.js'], 'sub/a')))
p = shared_pkg(exports={'.': './dist/index.js', './thing': './dist/new/thing.js'}, typesVersions={'>=4.0': {'thing': ['dist/new/thing.d.ts']}, '*': {'thing': ['dist/old/thing.d.ts']}})
T.append(('R3_version_range', base(p, dist=('index.js', 'index.d.ts', 'new/thing.d.ts', 'new/thing.js'), use=use('@secuura/shared/thing'))))
T.append(('R9_backslash_target', sa({'./thing': './dist/thing/theThing.js'}, {'thing': ['dist\\thing\\theThing.d.ts']}, [DT, JT], 'thing')))
T.append(('EQ1_mixed_array', sa({'./f': './dist/f.js'}, {'f': ['dist/f', 'src/f.d.ts']}, ['f.d.ts', 'f.js'], 'f')))
# ---- L2: specifier not an import, target genuinely unbuilt
unb = lambda src: {**sa({'./thing': './dist/thing/theThing.js'}, {'thing': ['dist/thing/theThing.d.ts']}, [JT], 'thing'), 'src/u.ts': src}
T.append(('L2_line_comment_unbuilt', unb("// import { X } from '@secuura/shared/thing';\nexport const q = 1;\n")))
T.append(('L2_block_comment_unbuilt', unb("/* import { X } from '@secuura/shared/thing'; */\nexport const q = 1;\n")))
T.append(('L2_nested_string_unbuilt', unb('export const s = "from \'@secuura/shared/thing\'";\n')))
f = unb(use('@secuura/shared/thing')); f['tsconfig.test.json'] = tsconfig(exclude=['src/excl']); f['src/excl/x.ts'] = f.pop('src/u.ts')
T.append(('L2_tsconfig_excluded_unbuilt', f))
T.append(('m5_require_in_function_unbuilt', unb("export function f() { return require('@secuura/shared/thing'); }\n")))
# ---- the four arms (fixture)
T.append(('arm_C_complete', base()))
T.append(('arm_B_decl_missing', base(dist=('index.js', 'index.d.ts', JT))))
T.append(('arm_D_dir_missing', base(dist=('index.js', 'index.d.ts'))))
T.append(('arm_A_runtime_missing', base(dist=('index.js', 'index.d.ts', DT))))
# ---- R4: tv target missing but plain subpath d.ts exists
T.append(('R4_tv_missing_plain_exists', sa({'./thing': './dist/thing/theThing.js'}, {'thing': ['dist/thing/theThing.d.ts']}, [JT, '../thing.d.ts'], 'thing')))
# ---- author's divergence cell + corroboration cells
T.append(('author_divergence_named_exists', sa({'./sub/*': './dist/sub/*.js'}, {'*': ['dist/nope/*'], 'sub/*': ['dist/sub/*.d.ts']}, ['nope/sub/a.d.ts'], 'sub/a')))
T.append(('nonsecuura_TS2307', {**base(), 'src/u2.ts': "import x from 'totally-absent-pkg';\nexport const y = x;\n"}))
# ---- m3 lexer escapes (unbuilt, real imports)
T.append(('m3_regex_quote_same_line_unbuilt', {**base(dist=('index.js', 'index.d.ts', JT)), 'src/u.ts': "const r = /'/; import { X } from '@secuura/shared/thing';\nexport const t: number = X; export const rr = r;\n"}))
T.append(('m3_from_comment_quote_unbuilt', {**base(dist=('index.js', 'index.d.ts', JT)), 'src/u.ts': "import { X } from /* c */ '@secuura/shared/thing';\nexport const t: number = X;\n"}))
if __name__ == '__main__':
    for n, f in T: measure(n, f)
