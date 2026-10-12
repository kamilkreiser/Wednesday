import sys; sys.path.insert(0, '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/f2077cbf-bb12-49ee-8d59-f5f537b335e0/scratchpad/g3/tools')
from harness import *
from table1 import sa, DT, JT
import json, os
only = set(sys.argv[1:])
T = []
STALE_B = ('index.js', 'index.d.ts', JT)  # decl missing
# ---- (2) attacks: tsc resolves the specifier via a DIFFERENT path while the tv target is absent
f = base(dist=STALE_B); f['src/stub/thing.d.ts'] = 'export declare const X: number;\n'
f['tsconfig.test.json'] = tsconfig({'baseUrl': '.', 'paths': {'@secuura/shared/thing': ['src/stub/thing.d.ts']}})
T.append(('X1_paths_mapping_tv_absent', f))
f = base(dist=STALE_B)
for k, v in base().items():
    if k.startswith(P): f['src/' + k] = v      # a COMPLETE copy nearer the importing file
T.append(('X2_nearer_complete_copy_service_copy_stale', f))
f = base(dist=STALE_B); f['src/__tests__/node_modules/@secuura/shared/package.json'] = json.dumps(shared_pkg())
T.append(('X2b_nearer_STALE_copy_service_copy_complete', {**base(), 'src/node_modules/@secuura/shared/package.json': json.dumps(shared_pkg()), 'src/node_modules/@secuura/shared/dist/index.d.ts': 'export {};\n', 'src/node_modules/@secuura/shared/dist/thing/theThing.js': 'module.exports={}\n'}))
# symlinked package dir, complete / stale
fs_ = base(pkgdir='pkgs/shared/')
T.append(('X3_symlinked_pkg_complete', fs_, [('node_modules/@secuura/shared', '../../pkgs/shared')]))
fs_ = base(pkgdir='pkgs/shared/', dist=STALE_B)
T.append(('X3b_symlinked_pkg_stale', fs_, [('node_modules/@secuura/shared', '../../pkgs/shared')]))
# ambient module shim
f = base(dist=STALE_B); f['src/shim.d.ts'] = "declare module '@secuura/shared/thing' { export const X: number; }\n"
T.append(('X4_ambient_declare_module_shim_tv_absent', f))
# project references: the tv-absent package is consumed via a referenced project? (paths to a composite project's src)
f = base(dist=STALE_B); f['lib/src/thing.ts'] = 'export const X: number = 1;\n'
f['lib/tsconfig.json'] = json.dumps({'compilerOptions': {'composite': True, 'declaration': True, 'outDir': 'out', 'rootDir': 'src', 'module': 'commonjs', 'target': 'ES2022', 'types': []}, 'include': ['src']})
f['tsconfig.test.json'] = json.dumps({'compilerOptions': {'strict': True, 'noEmit': True, 'target': 'ES2022', 'module': 'commonjs', 'skipLibCheck': True, 'types': [], 'baseUrl': '.', 'paths': {'@secuura/shared/thing': ['lib/src/thing.ts']}}, 'include': ['src/**/*'], 'references': [{'path': './lib'}]})
T.append(('X5_project_reference_via_paths_tv_absent', f))
# sibling-prefix package: @secuura/shared-extra installed + stale; import of @secuura/shared (complete)
f = base(); f.update({k.replace('@secuura/shared/', '@secuura/shared-extra/'): v for k, v in base(pj=shared_pkg(name='@secuura/shared-extra'), dist=STALE_B).items() if k.startswith(P)})
f['src/u2.ts'] = "import { X as Y } from '@secuura/shared-extra/thing';\nexport const y: number = Y;\n"
T.append(('X6_sibling_prefix_pkg_stale', f))
T.append(('X6b_sibling_prefix_pkg_only_shared_stale_import_extra_uninstalled', {**base(dist=STALE_B), 'src/u.ts': use('@secuura/shared-extra/thing')}))
# TS7016 for a NON-@secuura module that shares the prefix (JS-only packages)
f = base(); f['node_modules/@secuura-legacy/thing/package.json'] = json.dumps({'name': '@secuura-legacy/thing', 'main': 'index.js'}); f['node_modules/@secuura-legacy/thing/index.js'] = 'module.exports={X:1}\n'
f['src/u2.ts'] = "import { X as Y } from '@secuura-legacy/thing';\nexport const y = Y;\n"
T.append(('X7_TS7016_nonsecuura_prefix_lookalike', f))
f = base(); f['node_modules/@secuurax/shared/package.json'] = json.dumps({'name': '@secuurax/shared', 'main': 'index.js'}); f['node_modules/@secuurax/shared/index.js'] = 'module.exports={X:1}\n'
f['src/u2.ts'] = "import { X as Y } from '@secuurax/shared/thing';\nexport const y = Y;\n"
T.append(('X7b_TS2307_secuurax', f))
# JS-only @secuura package (no types anywhere): TS7016 on an installed @secuura pkg with no declared target
f = base(); f['node_modules/@secuura/jsonly/package.json'] = json.dumps({'name': '@secuura/jsonly', 'main': 'index.js'}); f['node_modules/@secuura/jsonly/index.js'] = 'module.exports={X:1}\n'
f['src/u2.ts'] = "import { X as Y } from '@secuura/jsonly';\nexport const y = Y;\n"
T.append(('X7c_TS7016_secuura_jsonly_no_types', f))
# type-only import / typeof import / export * — stale
T.append(('X8_import_type_stale', {**base(dist=STALE_B), 'src/u.ts': use('@secuura/shared/thing', 'type')}))
T.append(('X8b_typeof_import_stale', {**base(dist=STALE_B), 'src/u.ts': use('@secuura/shared/thing', 'typeof')}))
T.append(('X8c_export_star_stale', {**base(dist=STALE_B), 'src/u.ts': "export * from '@secuura/shared/thing';\n"}))
# skipLibCheck false / noResolve
f = base(); f['tsconfig.test.json'] = tsconfig({'skipLibCheck': False}); T.append(('X9_skipLibCheck_false_complete', f))
f = base(dist=STALE_B); f['tsconfig.test.json'] = tsconfig({'skipLibCheck': False}); T.append(('X9b_skipLibCheck_false_stale', f))
f = base(); f['tsconfig.test.json'] = tsconfig({'noResolve': True}); T.append(('X10_noResolve_complete', f))
f = base(dist=STALE_B); f['tsconfig.test.json'] = tsconfig({'noResolve': True}); T.append(('X10b_noResolve_stale', f))
# many diagnostics + long paths, stale and complete
deep = 'src/' + '/'.join(['d' * 60] * 8) + '/'
many = ''.join(f"export const v{i}: number = 'x{i}';\n" for i in range(4000))
T.append(('X11_4000_errors_longpath_complete', {**base(), deep + 'many.ts': many, deep + 'u.ts': use('@secuura/shared/thing')}, (), 'devinit'))
T.append(('X11b_4000_errors_longpath_stale', {**base(dist=STALE_B), deep + 'many.ts': many, deep + 'u.ts': use('@secuura/shared/thing')}))
# locale / pretty in tsconfig
f = base(dist=STALE_B); f['tsconfig.test.json'] = tsconfig({'locale': 'de'}); T.append(('X12_locale_de_stale', f))
f = base(); f['tsconfig.test.json'] = tsconfig({'locale': 'de'}); T.append(('X12b_locale_de_complete', f))
f = base(dist=STALE_B); f['tsconfig.test.json'] = tsconfig({'pretty': True}); T.append(('X13_pretty_true_in_tsconfig_stale', f))
f = base(); f['tsconfig.test.json'] = tsconfig({'pretty': True}); T.append(('X13b_pretty_true_complete', f))
# Windows separators in the SPECIFIER
T.append(('X14_backslash_specifier_complete', {**base(), 'src/u.ts': "import { X } from '@secuura/shared\\\\thing';\nexport const t: number = X;\n"}))
# diagnostic echo: a NON-2307/7016 diagnostic whose message quotes the phrase; the subpath is NOT imported; its target is absent
echo = 'export const e: number = "Cannot find module \'@secuura/shared/thing\'";\n'
T.append(('X15_echo_TS2322_unimported_target_absent', {**base(dist=STALE_B, use=None), 'src/__tests__/echo.test.ts': echo}))
T.append(('X15b_echo_TS2322_baselined_target_absent', {**base(dist=STALE_B, use=None), 'src/__tests__/echo.test.ts': echo}, (), 'devinit'))
T.append(('X15c_echo_TS2322_complete_build', {**base(use=None), 'src/__tests__/echo.test.ts': echo}))
# author error under a catch-all '*' key (complete build; the subpath simply does not exist)
T.append(('X16_typo_subpath_under_star_key_complete', sa({'./*': './dist/*.js'}, {'*': ['dist/*.d.ts']}, ['thing.d.ts', 'thing.js'], 'thnig')))
# a package map that names a file the build never produces (complete build; rebuild cannot fix)
T.append(('X17_map_names_never_built_file', sa({'./ghost': './dist/ghost.js'}, {'thing': ['dist/thing/theThing.d.ts'], 'ghost': ['dist/ghost.d.ts']}, [DT, JT, 'ghost.js'], 'ghost')))
T.append(('X17b_same_but_error_baselined', sa({'./ghost': './dist/ghost.js'}, {'thing': ['dist/thing/theThing.d.ts'], 'ghost': ['dist/ghost.d.ts']}, [DT, JT, 'ghost.js'], 'ghost'), (), 'devinit'))
# reverse divergence: '*' first names an existing-or-not file; TS uses 'sub/*' whose target is never built
T.append(('X18_reverse_divergence_ts_target_absent', sa({'./sub/*': './dist/sub/*.js'}, {'*': ['dist/*.d.ts'], 'sub/*': ['dist/other/*.d.ts']}, ['sub/a.js'], 'sub/a')))
# version range: TS reads >=4.0 (absent) while '*' target exists
p = shared_pkg(exports={'.': './dist/index.js', './thing': './dist/new/thing.js'}, typesVersions={'>=4.0': {'thing': ['dist/new/thing.d.ts']}, '*': {'thing': ['dist/old/thing.d.ts']}})
T.append(('X19_version_range_stale_new_absent_old_present', base(p, dist=('index.js', 'index.d.ts', 'old/thing.d.ts', 'new/thing.js'))))
# ---- (3) the other side: stale variants
p = shared_pkg(exports=None, typesVersions=None)
T.append(('Y1_no_exports_no_tv_root_types_absent', base(p, dist=('index.js',), use=use('@secuura/shared', 'root'))))
p = shared_pkg(exports=None, typesVersions=None, types=None)
T.append(('Y2_main_only_sibling_dts_absent', base(p, dist=('index.js',), use=use('@secuura/shared', 'root'))))
p = shared_pkg(exports=None, typesVersions=None)
T.append(('Y3_no_exports_no_tv_deep_subpath_stale', base(p, dist=('index.js', 'index.d.ts', JT), use=use('@secuura/shared/dist/thing/theThing'))))
T.append(('Y4_nested_subpath_stale', sa({'./a/b/c': './dist/a/b/c.js'}, {'a/b/c': ['dist/a/b/c.d.ts']}, ['a/b/c.js'], 'a/b/c')))
f = base(); f['node_modules/@secuura/shared/dist/thing/theThing.d.ts'] = "export { X } from './inner';\n"
T.append(('Y5_reexport_chain_inner_dts_missing', f))
f = base(); f['tsconfig.test.json'] = tsconfig({'skipLibCheck': False}); f['node_modules/@secuura/shared/dist/thing/theThing.d.ts'] = "export { X } from './inner';\n"
T.append(('Y5b_reexport_chain_inner_missing_skipLibCheck_false', f))
f = base(); f['node_modules/@secuura/shared/dist/thing/theThing.d.ts'] = "export { X } from '@secuura/shared/inner';\n"
f['node_modules/@secuura/shared/package.json'] = json.dumps(shared_pkg(typesVersions={'*': {'thing': ['dist/thing/theThing.d.ts'], 'inner': ['dist/inner.d.ts']}}))
T.append(('Y5c_reexport_via_secuura_specifier_inner_missing', f))
f = base(); f.update({k.replace('@secuura/shared/', '@secuura/crypto/'): v for k, v in base(pj=shared_pkg(name='@secuura/crypto'), dist=STALE_B).items() if k.startswith(P)})
f['src/u2.ts'] = "import { X as Y } from '@secuura/crypto/thing';\nexport const y: number = Y;\n"
T.append(('Y6_other_secuura_pkg_stale', f))
p = shared_pkg(types='index.d.ts', typesVersions={'*': {'*': ['dist/*']}})
T.append(('Y7_root_types_mapped_through_tv_stale', base(p, dist=('index.js',), use=use('@secuura/shared', 'root'))))
f = base(); f['node_modules/@secuura/shared/dist/thing/theThing.d.ts'] = "import type { Y } from './nested/y';\nexport declare const X: Y;\n"
T.append(('Y8_built_but_nested_dts_missing', f))
T.append(('Y9_ext_less_target_stale', sa({'./sub/*': './dist/sub/*.js'}, {'sub/*': ['dist/sub/*']}, ['sub/a.js'], 'sub/a')))
T.append(('Y10_bare_star_stale', sa({'./*': './dist/*.js'}, {'*': ['dist/*']}, ['thing.js'], 'thing')))
T.append(('Y11_dir_target_stale', sa({'./d': './dist/d/index.js'}, {'d': ['dist/d']}, ['d/index.js'], 'd')))
f = base(dist=STALE_B); f['node_modules/@secuura/shared/dist/thing/theThing.d.ts'] = None
T.append(('Y12_dangling_symlink_decl', base(dist=STALE_B), [('node_modules/@secuura/shared/dist/thing/theThing.d.ts', 'nowhere.d.ts')]))
for row in T:
    n, f = row[0], row[1]
    if only and n not in only: continue
    links = row[2] if len(row) > 2 else ()
    init = 'dev' if (len(row) > 3 and row[3] == 'devinit') else None
    measure(n, f, init_with=init, symlinks=links)
