#!/usr/bin/env python3
"""Edge-case driver for the PR #1515 delta gate.
usage: edge.py <outdir> [case-filter] [--checker NAME=path ...]
For every case: writes a throwaway service with node_modules/@secuura/shared inside it, runs each checker
(--baseline pointing at a zero-floor baseline) and tsc directly, prints one row per case.
"""
import json, os, subprocess, sys, shutil

S = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/ad6cb59d-4a2f-44e5-b355-5685c7d2a2e1/scratchpad/g1515d'
CHECKERS = {
    'base': f'{S}/base/Blockchain/Dev/scripts/typecheck-tests/check.cjs',
    'r0': f'{S}/r0/Blockchain/Dev/scripts/typecheck-tests/check.cjs',
    'head': f'{S}/head/Blockchain/Dev/scripts/typecheck-tests/check.cjs',
}
TSC = f'{S}/head/Blockchain/Dev/node_modules/typescript/bin/tsc'
P = 'node_modules/@secuura/shared/'
D = 'export declare const X: number;\n'
J = 'module.exports = { X: 1 };\n'
USE = lambda sub: f"import {{ X }} from '@secuura/shared/{sub}';\nexport const t: number = X;\n"
TYPEOF = "export type T = typeof import('@secuura/shared/thing');\n"
TSCONF = {'compilerOptions': {'strict': True, 'noEmit': True, 'target': 'ES2022', 'module': 'commonjs',
                              'skipLibCheck': True, 'types': []}, 'include': ['src/**/*']}


def pkg(tv=None, exports=None, dist=(), extra=None, tvraw=None):
    j = {'name': '@secuura/shared', 'version': '0.0.0', 'main': 'dist/index.js', 'types': 'dist/index.d.ts',
         'exports': {'.': './dist/index.js', **(exports or {})}}
    if tvraw is not None:
        j['typesVersions'] = tvraw
    elif tv is not None:
        j['typesVersions'] = {'*': tv}
    if extra:
        for k, v in extra.items():
            if v is None:
                j.pop(k, None)
            else:
                j[k] = v
    f = {P + 'package.json': json.dumps(j), P + 'dist/index.js': 'module.exports = {};\n',
         P + 'dist/index.d.ts': 'export declare const R: number;\n'}
    for rel in dist:
        f[P + rel] = D if rel.endswith(('.d.ts', '.d.mts', '.d.cts')) else J
    return f


THING = dict(tv={'thing': ['dist/thing/theThing.d.ts']}, exports={'./thing': './dist/thing/theThing.js'})
THING_OK = ['dist/thing/theThing.d.ts', 'dist/thing/theThing.js']
THING_STALE = ['dist/thing/theThing.js']  # declaration missing (arm B shape)


def thing(complete):
    return pkg(dist=THING_OK if complete else THING_STALE, **THING)


CASES = []


def case(name, files, tsconf=None, note=''):
    CASES.append((name, files, tsconf, note))


# ---- round-0 table, re-run (complete builds) ----
case('r0-linecomment-mapped-exists', {**thing(True), 'src/u.ts': "// import { X } from '@secuura/shared/thing';\nexport const q = 1;\n"})
case('r0-blockcomment-mapped-exists', {**thing(True), 'src/u.ts': "/* import { X } from '@secuura/shared/thing'; */\nexport const q = 1;\n"})
case('r0-string-unmapped', {**thing(True), 'src/u.ts': "export const s = \"from '@secuura/shared/nope'\";\n"})
case('r0-import-type', {**thing(True), 'src/u.ts': "import type { X } from '@secuura/shared/thing';\nexport type T = typeof X;\n"})
case('r0-typeof-import', {**thing(True), 'src/u.ts': TYPEOF})
case('r0-export-star', {**thing(True), 'src/u.ts': "export * from '@secuura/shared/thing';\n"})
case('r0-dynamic-import', {**thing(True), 'src/u.ts': "export const p = import('@secuura/shared/thing');\n"})
case('r0-require-in-template', {**thing(True), 'src/u.ts': "export const s = `require('@secuura/shared/nope')`;\n"})
case('r0-subpath-with-.js', {**thing(True), 'src/u.ts': "export * from '@secuura/shared/thing.js';\n"})
case('r0-deep-not-in-tv', {**thing(True), 'src/u.ts': "export type T = typeof import('@secuura/shared/dist/thing/theThing');\n"})
case('r0-middle-star-key', {**pkg(tv={'a/*/b': ['dist/a/*/b.d.ts']}, dist=['dist/a/x/b.d.ts', 'dist/a/x/b.js']), 'src/u.ts': USE('a/x/b')})
case('r0-no-typesVersions-root+sub', {**pkg(dist=['dist/thing/theThing.d.ts']), 'src/u.ts': "import { R } from '@secuura/shared';\nexport const r: number = R;\nexport type T = typeof import('@secuura/shared/dist/thing/theThing');\n"})
# ---- the five L1 shapes, complete ----
case('L1-trailing-star-extless', {**pkg(tv={'sub/*': ['dist/sub/*']}, exports={'./sub/*': './dist/sub/*.js'}, dist=['dist/sub/a.d.ts', 'dist/sub/a.js']), 'src/u.ts': USE('sub/a')})
case('L1-bare-star', {**pkg(tv={'*': ['dist/*']}, exports={'./*': './dist/*.js'}, dist=['dist/thing.d.ts', 'dist/thing.js']), 'src/u.ts': USE('thing')})
case('L1-literal-extless', {**pkg(tv={'e': ['dist/e']}, exports={'./e': './dist/e.js'}, dist=['dist/e.d.ts', 'dist/e.js']), 'src/u.ts': USE('e')})
case('L1-dir-index', {**pkg(tv={'d': ['dist/d']}, exports={'./d': './dist/d/index.js'}, dist=['dist/d/index.d.ts', 'dist/d/index.js']), 'src/u.ts': USE('d')})
case('L1-array-first-absent', {**pkg(tv={'f': ['src/f.d.ts', 'dist/f.d.ts']}, exports={'./f': './dist/f.js'}, dist=['dist/f.d.ts', 'dist/f.js']), 'src/u.ts': USE('f')})
# ---- L2 (unbuilt target) ----
case('L2-linecomment-unbuilt', {**thing(False), 'src/u.ts': "// import { X } from '@secuura/shared/thing';\nexport const q = 1;\n"})
case('L2-blockcomment-unbuilt', {**thing(False), 'src/u.ts': "/* import { X } from '@secuura/shared/thing'; */\nexport const q = 1;\n"})
case('L2-nested-string-unbuilt', {**thing(False), 'src/u.ts': "export const s = \"from '@secuura/shared/thing'\";\n"})
case('L2-excluded-file-unbuilt', {**thing(False), 'src/excl/u.ts': USE('thing')},
     tsconf={**TSCONF, 'exclude': ['src/excl']})
# ---- arms on the fixture ----
case('arm-C-complete', {**thing(True), 'src/u.ts': USE('thing')})
case('arm-B-decl-missing', {**thing(False), 'src/u.ts': USE('thing')})
case('arm-D-dir-missing', {**pkg(dist=[], **THING), 'src/u.ts': USE('thing')})
case('arm-A-js-missing', {**pkg(dist=['dist/thing/theThing.d.ts'], **THING), 'src/u.ts': USE('thing')})

# ---- lexer attacks: each in a COMPLETE and an UNBUILT (decl missing) variant; REAL = a genuine import ----
LEX = [
    ('tpl-${}-quotes', "const a = 1;\nexport const s = `${a ? 'x' : \"y\"}`;\n" + TYPEOF, True),
    ('regex-with-quote-sameline', "const r = /'/; export type T = typeof import('@secuura/shared/thing'); export const rr = r;\n", True),
    ('regex-with-quote-nextline', "export const r = /'/;\n" + TYPEOF, True),
    ('regex-with-backtick', "export const r = /`/;\n" + TYPEOF, True),
    ('regex-//-sameline', "const r = /https?:\\/\\//; export type T = typeof import('@secuura/shared/thing'); export const rr = r;\n", True),
    ('regex-slash-star', "export const r = /\\/*$/;\n" + TYPEOF, True),
    ('regex-slash-star-closed-later', "export const r = /\\/*$/;\n" + TYPEOF + "/** doc */\nexport const z = 1;\n", True),
    ('division-then-quote', "const a = 4 / 2; const b = 'x' + a;\n" + TYPEOF + "export const bb = b;\n", True),
    ('escaped-quote', "export const s = 'it\\'s';\n" + TYPEOF, True),
    ('backslash-newline', "export const s = 'a\\\nb';\n" + TYPEOF, True),
    ('url-string-before-import-sameline', "const u = 'http://x'; export type T = typeof import('@secuura/shared/thing'); export const uu = u;\n", True),
    ('blockopen-in-string-sameline', "const u = '/*'; export type T = typeof import('@secuura/shared/thing'); export const uu = u;\n", True),
    ('blockopen-in-string-nextline', "export const u = '/*';\n" + TYPEOF, True),
    ('blockcomment-with-quotes', "/* don't \"x\" `y` */\n" + TYPEOF, True),
    ('nested-template', "const b = 1;\nexport const s = `a ${`b${b}`} c`;\n" + TYPEOF, True),
    ('template-odd-backtick-in-${}', "export const s = `${'`'}`;\n" + TYPEOF, True),
    ('unterminated-string', "export const s = 'abc\n" + TYPEOF, True),
    ('unterminated-block-comment-after', TYPEOF + "/* never closed\n", True),
    ('crlf', ("// a comment\n" + "export const q = 1;\n" + TYPEOF).replace('\n', '\r\n'), True),
    ('crlf-comment-specifier', ("// import { X } from '@secuura/shared/thing';\n" + "export const q = 1;\n").replace('\n', '\r\n'), False),
    ('bom', '﻿' + TYPEOF, True),
    ('import-then-comment-quote', "import { X } from '@secuura/shared/thing' // 'b'\nexport const t: number = X;\n", True),
    ('require-in-function', "declare const require: (s: string) => unknown;\nexport function f() { return require('@secuura/shared/thing'); }\n", False),
    ('import-equals-require', "import M = require('@secuura/shared/thing');\nexport const t: number = M.X;\n", True),
    ('export-star', "export * from '@secuura/shared/thing';\n", True),
    ('side-effect-import', "import '@secuura/shared/thing';\nexport const q = 1;\n", False),
    ('multi-on-one-line', "import { X } from '@secuura/shared/thing'; import { R } from '@secuura/shared';\nexport const t: number = X + R;\n", True),
    ('specifier-after-other-string-same-line', "const a = 'x'; export type T = typeof import('@secuura/shared/thing'); export const aa = a;\n", True),
    ('dq-specifier', 'export type T = typeof import("@secuura/shared/thing");\n', True),
    ('from-newline-quote', "import { X } from\n  '@secuura/shared/thing';\nexport const t: number = X;\n", True),
    ('template-literal-specifier', "export const s = `import { X } from '@secuura/shared/thing'`;\n", False),
]
for (n, src, real) in LEX:
    for complete in (True, False):
        case(f'lex-{n}-{"complete" if complete else "unbuilt"}', {**thing(complete), 'src/u.ts': src}, note='REAL' if real else 'not-import')

# JSX/TSX
JSXCONF = {**TSCONF, 'compilerOptions': {**TSCONF['compilerOptions'], 'jsx': 'preserve'}}
JSXHDR = "declare global { namespace JSX { interface IntrinsicElements { [k: string]: any } } }\n"
for n, body in [('jsx-apostrophe', "export const e = <p>Don't</p>;\n"),
                ('jsx-backtick', "export const e = <p>use ` here</p>;\n"),
                ('jsx-blockopen', "export const e = <p>a /* b</p>;\n")]:
    for complete in (True, False):
        case(f'tsx-{n}-{"complete" if complete else "unbuilt"}', {**thing(complete), 'src/u.tsx': JSXHDR + body + TYPEOF}, tsconf=JSXCONF, note='REAL')

# ---- target-resolution attacks (complete builds unless named) ----
case('R1-types-field-redirected-by-tv-star', {**pkg(tvraw={'*': {'*': ['dist/*']}}, extra={'types': 'index.d.ts'}), 'src/u.ts': "import { R } from '@secuura/shared';\nexport const r: number = R;\n"})
case('R1b-types-field-redirected-literal', {**pkg(tvraw={'*': {'index.d.ts': ['dist/index.d.ts']}}, extra={'types': './index.d.ts'}), 'src/u.ts': "import { R } from '@secuura/shared';\nexport const r: number = R;\n"})
case('R2-star-key-before-longer-key', {**pkg(tv={'*': ['dist/*.d.ts'], 'sub/*': ['dist/other/*.d.ts']}, dist=['dist/other/a.d.ts', 'dist/other/a.js']), 'src/u.ts': USE('sub/a')})
case('R2b-longer-key-before-star', {**pkg(tv={'sub/*': ['dist/other/*.d.ts'], '*': ['dist/*.d.ts']}, dist=['dist/other/a.d.ts', 'dist/other/a.js']), 'src/u.ts': USE('sub/a')})
case('R3-version-range-before-star', {**pkg(tvraw={'>=4.0': {'thing': ['dist/new/thing.d.ts']}, '*': {'thing': ['dist/old/thing.d.ts']}}, dist=['dist/new/thing.d.ts']), 'src/u.ts': USE('thing')})
case('R4-tv-target-missing-plain-path-exists', {**pkg(tv={'thing': ['dist/thing.d.ts']}, dist=[]), P + 'thing.d.ts': D, 'src/u.ts': USE('thing')})
case('R5-array-wildcard-mixed-complete', {**pkg(tv={'sub/*': ['dist/sub/*', 'dist/sub/*.d.ts']}, dist=['dist/sub/a.d.ts']), 'src/u.ts': USE('sub/a')})
case('R5-array-wildcard-mixed-unbuilt', {**pkg(tv={'sub/*': ['dist/sub/*', 'dist/sub/*.d.ts']}, dist=[]), 'src/u.ts': USE('sub/a')})
case('R6-index-target-extless', {**pkg(tv={'d': ['dist/d/index']}, dist=['dist/d/index.d.ts']), 'src/u.ts': USE('d')})
case('R7-dir-target-no-index', {**pkg(tv={'d': ['dist/d']}, dist=['dist/d/other.d.ts']), 'src/u.ts': USE('d')})
case('R8-symlinked-dist', {**pkg(tv={'thing': ['dist/thing.d.ts']}, dist=[]), P + 'real/thing.d.ts': D, '@symlink ' + P + 'dist/thing.d.ts': '../real/thing.d.ts', 'src/u.ts': USE('thing')})
case('R8b-dangling-symlink-decl', {**pkg(tv={'thing': ['dist/thing.d.ts']}, dist=[]), '@symlink ' + P + 'dist/thing.d.ts': 'gone.d.ts', 'src/u.ts': USE('thing')})
case('R9-windows-separators-in-target', {**pkg(tv={'thing': ['dist\\thing\\theThing.d.ts']}, dist=['dist/thing/theThing.d.ts']), 'src/u.ts': USE('thing')})
case('R9b-windows-separators-in-specifier', {**thing(True), 'src/u.ts': "export type T = typeof import('@secuura/shared\\\\thing');\n"})
case('R10-d.mts-target-complete', {**pkg(tv={'thing': ['dist/thing.d.mts']}, dist=['dist/thing.d.mts']), 'src/u.ts': USE('thing')})
case('R10-d.mts-target-unbuilt', {**pkg(tv={'thing': ['dist/thing.d.mts']}, dist=[]), 'src/u.ts': USE('thing')})
case('R11-star-dts-pkgjson-import', {**pkg(tv={'*': ['dist/*.d.ts']}, dist=[]), 'src/u.ts': "import p = require('@secuura/shared/package.json');\nexport const n: string = p.name;\n"},
     tsconf={**TSCONF, 'compilerOptions': {**TSCONF['compilerOptions'], 'resolveJsonModule': True, 'esModuleInterop': True}})
case('R12-typings-field-root', {**pkg(extra={'types': None, 'typings': 'dist/index.d.ts'}), 'src/u.ts': "import { R } from '@secuura/shared';\nexport const r: number = R;\n"})
case('R13-proto-key-subpath', {**thing(True), 'src/u.ts': "export type T = typeof import('@secuura/shared/constructor');\n"})
case('R14-no-tv-sub-via-exports-only', {**pkg(exports={'./thing': './dist/thing.js'}, dist=['dist/thing.js', 'dist/thing.d.ts']), 'src/u.ts': USE('thing')})
case('R15-other-secuura-pkg-healthy', {'node_modules/@secuura/other/package.json': json.dumps({'name': '@secuura/other', 'types': 'dist/index.d.ts', 'typesVersions': {'*': {'x': ['dist/x.d.ts']}}}),
                                     'node_modules/@secuura/other/dist/index.d.ts': D, 'node_modules/@secuura/other/dist/x.d.ts': D,
                                     'src/u.ts': "import { X } from '@secuura/other/x';\nexport const t: number = X;\n"})
case('R16-root-types-array', {**pkg(extra={'types': ['missing.d.ts', 'dist/index.d.ts']}), 'src/u.ts': "import { R } from '@secuura/shared';\nexport const r: number = R;\n"})
case('R17-arms-literal-dts-unbuilt', {**pkg(tv={'thing': ['dist/thing.d.ts']}, dist=['dist/thing.js']), 'src/u.ts': USE('thing')})
# false-negative shapes: L1 forms with the declaration genuinely missing
case('FN-trailing-star-extless-unbuilt', {**pkg(tv={'sub/*': ['dist/sub/*']}, dist=['dist/sub/a.js']), 'src/u.ts': USE('sub/a')})
case('FN-bare-star-unbuilt', {**pkg(tv={'*': ['dist/*']}, dist=['dist/thing.js']), 'src/u.ts': USE('thing')})
case('FN-literal-extless-unbuilt', {**pkg(tv={'e': ['dist/e']}, dist=['dist/e.js']), 'src/u.ts': USE('e')})
case('FN-dir-index-unbuilt', {**pkg(tv={'d': ['dist/d']}, dist=['dist/d/index.js']), 'src/u.ts': USE('d')})
case('FN-array-both-absent', {**pkg(tv={'f': ['src/f.d.ts', 'dist/f.d.ts']}, dist=['dist/f.js']), 'src/u.ts': USE('f')})
case('FN-star-dts-unbuilt', {**pkg(tv={'*': ['dist/*.d.ts']}, dist=['dist/thing.js']), 'src/u.ts': USE('thing')})
case('FN-root-types-unbuilt', {**pkg(extra={}), P + 'dist/index.d.ts': None, 'src/u.ts': "import { R } from '@secuura/shared';\nexport const r: number = R;\n"})
# ---- equivalence probes (outside the author's 14 rows) ----
case('EQ1-mixed-array-extless-resolves-literal-missing', {**pkg(tv={'f': ['dist/f', 'src/f.d.ts']}, dist=['dist/f.d.ts', 'dist/f.js']), 'src/u.ts': USE('f')})
case('EQ1b-mixed-array-star-extless-and-literal', {**pkg(tv={'sub/*': ['dist/sub/*', 'types/sub/*.d.ts']}, dist=['dist/sub/a.d.ts']), 'src/u.ts': USE('sub/a')})
for complete in (True, False):
    sfx = 'complete' if complete else 'unbuilt'
    case(f'EQ2-linecomment-ending-from-then-string-{sfx}', {**thing(complete), 'src/u.ts': "// this subpath is imported from\n'@secuura/shared/thing';\nexport const q = 1;\n"}, note='not-import')
    case(f'EQ3-escaped-quote-sameline-{sfx}', {**thing(complete), 'src/u.ts': "const s = 'it\\'s'; export type T = typeof import('@secuura/shared/thing'); export const ss = s;\n"}, note='REAL')
    case(f'EQ4-block-comment-from-then-string-{sfx}', {**thing(complete), 'src/u.ts': "/* imported from */ '@secuura/shared/thing';\nexport const q = 1;\n"}, note='not-import')
    case(f'FN-from-blockcomment-quote-{sfx}', {**thing(complete), 'src/u.ts': "import { X } from /* c */ '@secuura/shared/thing';\nexport const t: number = X;\n"}, note='REAL')
    case(f'EQ5-unterminated-quote-line-then-import-{sfx}', {**thing(complete), 'src/u.ts': "// ok\nexport const s = \"it's\";\nexport const r = /'/;\n" + TYPEOF}, note='REAL')


def materialise(d, files, tsconf):
    if os.path.exists(d):
        shutil.rmtree(d)
    os.makedirs(d)
    allf = {'tsconfig.test.json': json.dumps(tsconf or TSCONF), 'src/ok.ts': 'export const ok: number = 1;\n',
            'src/__tests__/a.test.ts': 'export const fine: number = 1;\n', 'baseline.txt': 'examined-test-files 0\n', **files}
    for rel, body in allf.items():
        if body is None:
            continue
        if rel.startswith('@symlink '):
            continue
        p = os.path.join(d, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'w', newline='') as fh:
            fh.write(body)
    for rel, body in allf.items():
        if body is None and os.path.exists(os.path.join(d, rel)):
            os.remove(os.path.join(d, rel))
        if rel.startswith('@symlink '):
            p = os.path.join(d, rel[len('@symlink '):])
            os.makedirs(os.path.dirname(p), exist_ok=True)
            os.symlink(body, p)


def first_line(s, keys):
    for ln in s.splitlines():
        for k in keys:
            if k in ln:
                return ln.strip()[:150]
    return ''


def main():
    out = sys.argv[1]
    flt = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else ''
    checkers = dict(CHECKERS)
    if '--checker' in sys.argv:
        checkers = {}
        for a in sys.argv[sys.argv.index('--checker') + 1:]:
            k, v = a.split('=', 1)
            checkers[k] = v
    os.makedirs(out, exist_ok=True)
    rows = []
    for name, files, tsconf, note in CASES:
        if flt and flt not in name:
            continue
        d = os.path.join(out, name)
        materialise(d, files, tsconf)
        t = subprocess.run(['node', TSC, '--noEmit', '--pretty', 'false', '-p', 'tsconfig.test.json'], cwd=d, capture_output=True, text=True)
        codes = sorted(set(w.split(':')[0] for w in t.stdout.split('error ')[1:]))
        res = {}
        for k, c in checkers.items():
            r = subprocess.run(['node', c, d, '--baseline', os.path.join(d, 'baseline.txt')], capture_output=True, text=True)
            o = r.stdout + r.stderr
            tag = ''
            if 'CANNOT RUN' in o:
                tag = 'STALE:' + first_line(o, ['missing declaration target']).replace('missing declaration target:', '').strip()
            elif o.startswith('note:') or '\nnote:' in o:
                tag = 'NOTE'
            elif 'NEW type errors' in o:
                tag = 'NEW'
            res[k] = (r.returncode, tag)
            with open(os.path.join(out, f'{name}.{k}.out'), 'w') as fh:
                fh.write(o)
        with open(os.path.join(out, f'{name}.tsc.out'), 'w') as fh:
            fh.write(t.stdout + t.stderr)
        row = {'case': name, 'note': note, 'tsc': t.returncode, 'tsc_codes': codes, **{k: v for k, v in res.items()}}
        rows.append(row)
        print(json.dumps(row), flush=True)
    with open(os.path.join(out, 'rows.json'), 'w') as fh:
        json.dump(rows, fh, indent=1)


if __name__ == '__main__':
    main()
