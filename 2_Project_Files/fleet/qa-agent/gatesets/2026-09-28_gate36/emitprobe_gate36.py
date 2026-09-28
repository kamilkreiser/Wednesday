#!/usr/bin/env python3
"""emitprobe_gate36.py <scratchpad> — the DRAFTER's NO-RUNTIME-CHANGE measurement for gate36's types-only row (#1326 KS-1351 item 1 + item 2): DOES THE
PR CHANGE ANY EMITTED JAVASCRIPT BEYOND `let` -> `const` AT credentialRepo.ts:95? (The gate owes the TS2339 4 -> 0 count over an `exclude: []` program with
packages/shared REBUILT; this probe measures only the emit.) New for gate36 — the lineage's logprobe measured a logger; this row has no runtime surface to
drive, so the instrument is the compiler's own output.

Instrument: each changed file read from the scratch clone at each revision (`git show <rev>:<path>`), transpiled with the checkout's OWN typescript
(`ts.transpileModule`, READ from node_modules) under THAT package's OWN tsconfig.json compilerOptions read at the same revision (packages/shared: ES2022 /
commonjs; services/vc-issuer: es2021 / commonjs — `const` and `let` both survive at these targets, so the one-word change is VISIBLE to the instrument).
Revisions: the merge-base (develop d9ce1403d158, the pin), #1326's head, END_TREE (pins_gate36.json). The emitted JS is compared line by line.
CONTROLS (each must behave, or the verdict is void): (C1) a PLANTED RUNTIME edit (a string literal in credentialRepo.ts changed in the workdir only) must
make the emit DIFFER; (C2) a PLANTED TYPE-ONLY edit (a new exported interface appended to types.ts at the merge-base) must leave the emit IDENTICAL — so
IDENTICAL for types.ts means "types erase", not "the file was not read"; (C3) the head vs itself is IDENTICAL; (C4) types.ts's emit is NON-EMPTY (the
module still emits its runtime exports, if any, and its `exports` preamble) — an empty string on both sides would compare IDENTICAL and prove nothing.
Nothing is written outside <scratchpad>/g36_emitprobe_*; nothing in the checkout is written. Writes emitprobe_gate36.json beside this script."""
import json, os, re, subprocess, sys, datetime, difflib
SP = sys.argv[1] if len(sys.argv) > 1 else ''
if not re.match(r'^/private/tmp/claude-501/.*/scratchpad', SP) or not os.path.isdir(SP): print('usage: emitprobe_gate36.py <scratchpad>'); sys.exit(9)
GS = os.path.dirname(os.path.abspath(__file__))
CL = os.path.join(SP, 'g36_sp', 'clone.git')
CHECKOUT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
TS = CHECKOUT + '/Blockchain/Dev/node_modules/typescript'
PINS = json.load(open(os.path.join(GS, 'pins_gate36.json'), encoding='utf-8'))
N = '1326'
FILES = {'Blockchain/Dev/packages/shared/src/vc/types.ts': 'Blockchain/Dev/packages/shared/tsconfig.json',
         'Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts': 'Blockchain/Dev/services/vc-issuer/tsconfig.json'}
REVS = [('merge-base (develop, the pin)', PINS['prs'][N]['merge_base']), ('#1326 head', PINS['prs'][N]['head']), ('END_TREE', PINS['end_tree'])]
W = os.path.join(SP, 'g36_emitprobe_' + datetime.datetime.now().strftime('%H%M%S')); os.makedirs(W)
def show(rev, p):
    r = subprocess.run(['git', '--git-dir', CL, 'show', '%s:%s' % (rev, p)], capture_output=True, text=True)
    if r.returncode != 0: print('REFUSING: git show %s:%s rc %d' % (rev[:12], p, r.returncode)); sys.exit(1)
    return r.stdout
NODE = r'''
const ts = require(process.argv[2]); const fs = require('fs');
const src = fs.readFileSync(process.argv[3], 'utf8'); const cfgText = fs.readFileSync(process.argv[4], 'utf8');
const parsed = ts.parseConfigFileTextToJson('tsconfig.json', cfgText);
if (parsed.error) { console.error('tsconfig parse error'); process.exit(3); }
const conv = ts.convertCompilerOptionsFromJson(parsed.config.compilerOptions || {}, '.');
if (conv.errors.length) { console.error('compilerOptions errors ' + conv.errors.length); process.exit(4); }
const o = conv.options; delete o.declaration; delete o.declarationMap; delete o.sourceMap; delete o.outDir; delete o.rootDir;
const r = ts.transpileModule(src, { compilerOptions: o, fileName: process.argv[3], reportDiagnostics: true });
if ((r.diagnostics || []).length) { console.error('transpile diagnostics ' + r.diagnostics.length); process.exit(5); }
process.stdout.write(r.outputText);
'''
open(os.path.join(W, 'emit.js'), 'w').write(NODE)
def emit(tag, src, cfg):
    sp_, cp_ = os.path.join(W, tag + '.ts'), os.path.join(W, tag + '.tsconfig.json')
    open(sp_, 'w').write(src); open(cp_, 'w').write(cfg)
    r = subprocess.run(['node', os.path.join(W, 'emit.js'), TS, sp_, cp_], capture_output=True, text=True)
    if r.returncode != 0: print('REFUSING: transpile %s rc %d: %s' % (tag, r.returncode, r.stderr.strip()[:200])); sys.exit(1)
    open(os.path.join(W, tag + '.js'), 'w').write(r.stdout)
    return r.stdout
def delta(a, b):
    return [l for l in difflib.unified_diff(a.split('\n'), b.split('\n'), lineterm='', n=0) if l and l[0] in '+-' and not l.startswith(('+++', '---'))]
tsver = json.load(open(TS + '/package.json'))['version']
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
print('emitprobe_gate36 %s | typescript %s (the checkout\'s, READ) | node %s | workdir %s' % (now, tsver, subprocess.run(['node', '--version'], capture_output=True, text=True).stdout.strip(), W))
RES = {'_measured_at': now, '_typescript': tsver, 'files': {}}
for f, cfgp in FILES.items():
    em = {}
    for lab, rev in REVS:
        em[lab] = emit('%s_%s' % (os.path.basename(f).replace('.ts', ''), rev[:12]), show(rev, f), show(rev, cfgp))
        print('  %-32s %-18s emit %6d bytes, %4d lines' % (lab, os.path.basename(f), len(em[lab]), em[lab].count('\n')))
    d_head = delta(em[REVS[0][0]], em[REVS[1][0]]); d_end = delta(em[REVS[0][0]], em[REVS[2][0]])
    RES['files'][f] = {'emit_bytes': {k: len(v) for k, v in em.items()}, 'delta_mb_to_head': d_head, 'delta_mb_to_end': d_end}
    print('  %s: emitted-JS delta merge-base -> head %s | merge-base -> END_TREE %s' % (os.path.basename(f), d_head or 'NONE (IDENTICAL)', d_end or 'NONE (IDENTICAL)'))
# controls
T, C = 'Blockchain/Dev/packages/shared/src/vc/types.ts', 'Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts'
mb, hd = REVS[0][1], REVS[1][1]
crepo_h = show(hd, C); lit = "'SELECT credential FROM vc_credentials_store WHERE id = $1'"
c1_src = crepo_h.replace(lit, "'SELECT credential FROM vc_credentials_store WHERE id = $2'", 1)
c1 = crepo_h.count(lit) == 1 and bool(delta(emit('C1_head', crepo_h, show(hd, FILES[C])), emit('C1_plant', c1_src, show(hd, FILES[C]))))
types_mb = show(mb, T)
c2 = not delta(emit('C2_mb', types_mb, show(mb, FILES[T])), emit('C2_plant', types_mb + '\nexport interface Gate36EmitProbeControl { planted?: boolean; }\n', show(mb, FILES[T])))
c3 = not delta(emit('C3_a', crepo_h, show(hd, FILES[C])), emit('C3_b', crepo_h, show(hd, FILES[C])))
c4 = all(v > 0 for v in RES['files'][T]['emit_bytes'].values())
CTL = {'C1 a planted runtime edit makes the emit DIFFER': c1, 'C2 a planted type-only edit leaves the emit IDENTICAL': c2, 'C3 head vs itself IDENTICAL': c3, 'C4 types.ts emit non-empty at every revision': c4}
for k, v in CTL.items(): print('  CONTROL %s: %s' % (k, v))
RES['_controls'] = CTL
dT, dC = RES['files'][T]['delta_mb_to_head'], RES['files'][C]['delta_mb_to_head']
only_letconst = len(dC) == 2 and all(re.sub(r'\b(let|const)\b', 'X', x[1:]) == re.sub(r'\b(let|const)\b', 'X', dC[0][1:]) for x in dC) and {x[0] for x in dC} == {'+', '-'}
RES['_summary'] = 'types.ts emitted JS merge-base -> head: %s; credentialRepo.ts emitted JS merge-base -> head: %s (%s); END_TREE deltas equal the head\'s: %s' % (
    'IDENTICAL' if not dT else 'DIFFERS %s' % dT[:4], dC if dC else 'IDENTICAL', 'ONLY let -> const on one line' if only_letconst else 'NOT only let -> const',
    RES['files'][T]['delta_mb_to_end'] == dT and RES['files'][C]['delta_mb_to_end'] == dC)
RES['_verdict_ok'] = (not dT) and only_letconst and all(CTL.values())
print('SUMMARY %s | controls all behaved: %s | NO RUNTIME CHANGE BEYOND let -> const: %s' % (RES['_summary'], all(CTL.values()), RES['_verdict_ok']))
json.dump(RES, open(os.path.join(GS, 'emitprobe_gate36.json'), 'w'), indent=1)
sys.exit(0 if RES['_verdict_ok'] else 1)
