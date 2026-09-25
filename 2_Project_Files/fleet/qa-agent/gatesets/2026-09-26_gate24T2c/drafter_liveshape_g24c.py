#!/usr/bin/env python3
"""drafter_liveshape_g24c.py — the DRAFTER's own capture of real vitest 4.1.11 `--reporter=default` runs for #1245 ROUND 2 (a PREDICTION instrument
for the kit; the gate re-captures and grades THROUGH THE REAL CODE PATH). Every run goes through Node's `spawnSync` with `encoding: 'utf8'` and a
`timeout`, exactly the mechanism `childSuiteCounts` uses (stdout and stderr PIPED, kept SEPARATE; the VITEST* env vars deleted as the head deletes
them). Fixtures under <kit>/_sp/live2/, OUTSIDE any package; vitest from <kit>/_sp/pkg (npm ci --offline of the #1245 head's own
systemTest/performance lockfile). The reading is done by a BYTE-LIFTED copy of the head's reader block (`interface SuiteCounts` .. the end of
`readSuiteCounts`, sliced from the head blob and run under node's type stripping) — a lift, never evidence.
Shapes: S1-S18 as gate24T2a numbered them, S19 the seat's adversarial shape, and the drafter's HUNT shapes H1-H9 (new real shapes the round-2
rule might misread). Usage: drafter_liveshape_g24c.py   (writes only under <kit>/_sp/live2/ and prints the table)"""
import json, os, subprocess, sys
W = os.path.dirname(os.path.abspath(__file__)); L = os.path.join(W, '_sp', 'live2'); VT = os.path.join(W, '_sp', 'pkg', 'node_modules', '.bin', 'vitest')
CL = os.path.join(W, '_sp', 'g24c_sp', 'clone.git'); HEAD = '65eb964271b0d6895e90fe8f5ffcbbbb9a484050'
F = 'systemTest/performance/tests/unit/utils/unitSuiteSlotIndependence.test.ts'
os.makedirs(L, exist_ok=True)
LOOK = r"' Test Files  1 passed (1)\n      Tests  7 passed (7)'"
FAIL = "it('then fails', () => { expect(1).toBe(2); });"
# (name, {file: source}, extra env, extra args, timeout ms, correct {passed, failed} or None (= no summary: the honest answer is null), note)
SH = [
 ('S01_failonly', {'a.test.ts': FAIL}, {}, [], 60000, {'passed': 0, 'failed': 1}, ''),
 ('S02_skiponly', {'a.test.ts': "it.skip('s', () => {});"}, {}, [], 60000, {'passed': 0, 'failed': 0}, ''),
 ('S03_todoonly', {'a.test.ts': "it.todo('t');"}, {}, [], 60000, {'passed': 0, 'failed': 0}, ''),
 ('S04_xfail_pass', {'a.test.ts': "it.fails('x', () => { throw new Error('b'); }); it('p', () => {});"}, {}, [], 60000, {'passed': 1, 'failed': 0}, ''),
 ('S05_fail_pass_skip', {'a.test.ts': "it.skip('s', () => {}); " + FAIL + " it('p', () => {});"}, {}, [], 60000, {'passed': 1, 'failed': 1}, ''),
 ('S06_passonly', {'a.test.ts': "it('p', () => {});"}, {}, [], 60000, {'passed': 1, 'failed': 0}, ''),
 ('S07_multifile', {'a.test.ts': FAIL + " it.skip('s', () => {});", 'b.test.ts': "it('p', () => {});"}, {}, [], 60000, {'passed': 1, 'failed': 1}, ''),
 ('S08_allfailed', {'a.test.ts': "it('f1', () => { expect(1).toBe(2); }); it('f2', () => { expect(1).toBe(2); }); it('f3', () => { expect(1).toBe(2); });"}, {}, [], 60000, {'passed': 0, 'failed': 3}, ''),
 ('S09_everylabel', {'a.test.ts': "it('f1', () => { expect(1).toBe(2); }); it('f2', () => { expect(1).toBe(2); }); it('p1', () => {}); it('p2', () => {}); it.fails('x', () => { throw new Error('b'); }); it.skip('s1', () => {}); it.skip('s2', () => {}); it.todo('t');"}, {}, [], 60000, {'passed': 2, 'failed': 2}, ''),
 ('S10_orient', {'a.test.ts': "it('f1', () => { expect(1).toBe(2); }); it('f2', () => { expect(1).toBe(2); }); it('p1', () => {}); it('p2', () => {}); it('p3', () => {});"}, {}, [], 60000, {'passed': 3, 'failed': 2}, ''),
 ('S11_xfailonly', {'a.test.ts': "it.fails('x', () => { throw new Error('b'); });"}, {}, [], 60000, {'passed': 0, 'failed': 0}, ''),
 ('S12_beforeall', {'a.test.ts': "describe('d', () => { beforeAll(() => { throw new Error('hook'); }); it('a', () => {}); it('b', () => {}); });"}, {}, [], 60000, {'passed': 0, 'failed': 0}, 'what the line states'),
 ('S13_ctxskip', {'a.test.ts': "it('rs', (ctx) => { ctx.skip(); }); it('p', () => {});"}, {}, [], 60000, {'passed': 1, 'failed': 0}, ''),
 ('S14_xfail_unexpectedpass', {'a.test.ts': "it.fails('x', () => {}); it('p', () => {});"}, {}, [], 60000, {'passed': 1, 'failed': 1}, ''),
 ('S15_notests', {'a.test.ts': "const x = 1;"}, {}, [], 60000, None, 'no counts stated: null is the correct refusal'),
 ('S16_lookalike_stdout', {'a.test.ts': "it('logs', () => { console.log('      Tests  5 passed (5)'); }); " + FAIL}, {}, [], 60000, {'passed': 1, 'failed': 1}, ''),
 ('S17_lookalike_stderr', {'a.test.ts': "it('errors', () => { console.error('      Tests  5 passed (5)'); }); " + FAIL}, {}, [], 60000, {'passed': 1, 'failed': 1}, ''),
 ('S18_diffcontext', {'a.test.ts': "it('d', () => { expect('a\\n      Tests  9 passed (9)\\nb').toBe('a\\n      Tests  9 passed (9)\\nc'); }); it('p', () => {});"}, {}, [], 60000, {'passed': 1, 'failed': 1}, ''),
 ('S19_seat_anchor_stdout', {'a.test.ts': "it('logs', () => { console.log(" + LOOK + "); }); " + FAIL}, {}, [], 60000, {'passed': 1, 'failed': 1}, 'the seat\'s adversarial shape'),
 # --- the drafter's HUNT shapes (new real shapes the round-2 rule might misread) ---
 ('H1_killed_after_lookalike', {'a.test.ts': "it('logs', () => { console.log(" + LOOK + "); }); it('hangs', async () => { await new Promise(() => {}); }, 120000);"}, {}, [], 6000, None,
  'spawnSync timeout (SIGTERM, as childSuiteCounts\' 180 s timeout does) after a test logged the S19 pair: NO real summary exists'),
 ('H1b_killed_after_tests_only', {'a.test.ts': "it('logs', () => { console.log('      Tests  5 passed (5)'); }); it('hangs', async () => { await new Promise(() => {}); }, 120000);"}, {}, [], 6000, None, 'control for H1: killed after a Tests-only lookalike (no anchor)'),
 ('H1c_killed_no_lookalike', {'a.test.ts': "it('p', () => {}); it('hangs', async () => { await new Promise(() => {}); }, 120000);"}, {}, [], 6000, None, 'control for H1: killed, no lookalike'),
 ('H2_late_console_log', {'a.test.ts': "it('p', () => { setTimeout(() => console.log(" + LOOK + "), 300); }); " + FAIL + " it('slow', async () => { await new Promise((r) => setTimeout(r, 50)); });"}, {}, [], 60000, {'passed': 2, 'failed': 1}, 'a timer logs after its test ended'),
 ('H3_late_stdout_write', {'a.test.ts': "it('p', () => { setTimeout(() => process.stdout.write(" + LOOK + " + '\\n'), 300); }); " + FAIL}, {}, [], 60000, {'passed': 1, 'failed': 1}, 'a timer writes to process.stdout after its test ended'),
 ('H4_exit_hook_write', {'a.test.ts': "process.on('exit', () => { process.stdout.write(" + LOOK + " + '\\n'); }); it('p', () => {}); " + FAIL}, {}, [], 60000, {'passed': 1, 'failed': 1}, 'a process exit hook in the test module'),
 ('H5_forcecolor_S17', {'a.test.ts': "it('errors', () => { console.error('      Tests  5 passed (5)'); }); " + FAIL}, {'FORCE_COLOR': '1'}, [], 60000, {'passed': 1, 'failed': 1}, 'FORCE_COLOR=1 in the child env (ANSI on a pipe)'),
 ('H6_unhandled_error', {'a.test.ts': "it('p', () => { setTimeout(() => { throw new Error('late'); }, 0); }); it('q', async () => { await new Promise((r) => setTimeout(r, 50)); });"}, {}, [], 60000, {'passed': 2, 'failed': 0}, 'the Tests line states 2 passed; vitest ALSO prints an Errors line and exits 1: {2,0} is the line, the rc is the caller\'s business'),
 ('H7a_ci_true_S17', {'a.test.ts': "it('errors', () => { console.error('      Tests  5 passed (5)'); }); " + FAIL}, {'CI': 'true'}, [], 60000, {'passed': 1, 'failed': 1}, 'CI=true: does the summary move stream?'),
 ('H7b_silent_S19', {'a.test.ts': "it('logs', () => { console.log(" + LOOK + "); }); " + FAIL}, {}, ['--silent=true'], 60000, {'passed': 1, 'failed': 1}, '--silent=true: does the summary move stream? (liveshape_1 ran `--silent` bare, which swallowed the file argument: VOID)'),
 ('H8_stderr_pair', {'a.test.ts': "it('errors', () => { console.error(" + LOOK + "); }); " + FAIL}, {}, [], 60000, {'passed': 1, 'failed': 1}, 'console.error of BOTH lines: stdout-only reads right; the JOINED claim is the question'),
 ('H8b_diff_pair', {'a.test.ts': "it('d', () => { expect(['h', ' Test Files  9 passed (9)', '      Tests  9 passed (9)', 'x'].join('\\n')).toBe(['h', ' Test Files  9 passed (9)', '      Tests  9 passed (9)', 'y'].join('\\n')); }); it('p', () => {});"}, {}, [], 60000, {'passed': 1, 'failed': 1}, 'a diff whose context carries BOTH lines, no console call: JOINED is the question'),
 ('H9_failing_test_named_testfiles', {'a.test.ts': "it('reads the Test Files line', () => { expect(1).toBe(2); }); it('p', () => {});"}, {}, [], 60000, {'passed': 1, 'failed': 1}, 'a failing test whose NAME carries \' Test Files \''),
]
DRIVE = os.path.join(L, 'drive.mjs')
open(DRIVE, 'w').write("""import { spawnSync } from 'node:child_process';
import { writeFileSync } from 'node:fs';
const [dir, vt, timeout, envJson, ...args] = process.argv.slice(2);
const env = { ...process.env, ...JSON.parse(envJson) };
for (const k of ['VITEST', 'VITEST_WORKER_ID', 'VITEST_POOL_ID']) delete env[k];
const r = spawnSync(vt, ['run', '--root', dir, '--globals', '--reporter=default', ...args], { env, cwd: dir, encoding: 'utf8', timeout: Number(timeout) });
writeFileSync(dir + '/stdout.txt', r.stdout ?? '');
writeFileSync(dir + '/stderr.txt', r.stderr ?? '');
writeFileSync(dir + '/meta.json', JSON.stringify({ status: r.status, signal: r.signal, error: r.error ? r.error.code : null }));
""")
src = subprocess.run(['git', '--git-dir', CL, 'show', '%s:%s' % (HEAD, F)], capture_output=True, text=True, check=True).stdout
a = src.index('interface SuiteCounts'); b = src.index('/**\n * Run the slot-sensitive files as a child vitest')
LIFT = os.path.join(L, 'lift.ts')
open(LIFT, 'w').write('// BYTE-LIFTED from %s:%s (interface SuiteCounts .. end of readSuiteCounts) — a PREDICTION instrument, never evidence\n' % (HEAD[:12], F)
    + src[a:b] + """
import { readFileSync } from 'node:fs';
const dir = process.argv[2];
const out = readFileSync(dir + '/stdout.txt', 'utf8'); const err = readFileSync(dir + '/stderr.txt', 'utf8');
const dm = /Tests\\s+(?:(\\d+) failed \\| )?(\\d+) passed \\((\\d+)\\)/.exec(`${out}\\n${err}`); // develop 6e2a00bfe :99/:103, byte-copied
console.log(JSON.stringify({ stdoutOnly: readChildOutput(out), joined: readChildOutput(`${out}\\n${err}`), round1Joined: readSuiteCounts(`${out}\\n${err}`), developJoined: dm === null ? null : { passed: Number(dm[2]), failed: Number(dm[1] ?? '0') } }));
""")
rows = []
for name, files, env, args, tmo, want, note in SH:
    d = os.path.join(L, name); os.makedirs(d, exist_ok=True)
    for fn, body in files.items(): open(os.path.join(d, fn), 'w').write(body + '\n')
    subprocess.run(['node', DRIVE, d, VT, str(tmo), json.dumps(env)] + args + sorted(files), stdin=subprocess.DEVNULL, capture_output=True, text=True)
    meta = json.load(open(os.path.join(d, 'meta.json')))
    so = open(os.path.join(d, 'stdout.txt')).read(); se = open(os.path.join(d, 'stderr.txt')).read()
    lr = subprocess.run(['node', '--experimental-strip-types', '--no-warnings', LIFT, d], capture_output=True, text=True)
    try: res = json.loads(lr.stdout.strip().splitlines()[-1])
    except Exception: res = {'LIFT_ERROR': (lr.stderr or lr.stdout)[-300:]}
    tl = lambda s: [l for l in s.replace('\x1b', '<ESC>').split('\n') if l.lstrip().startswith(('Tests', 'Test Files')) or ' Test Files ' in l]
    ok = lambda r: 'PASS' if r == want else 'FAIL'
    rows.append({'shape': name, 'meta': meta, 'stdout_lines': tl(so), 'stderr_lines': tl(se), 'want': want, 'lift': res, 'note': note,
                 'stdoutOnly': ok(res.get('stdoutOnly', 'ERR')), 'joined': ok(res.get('joined', 'ERR')), 'ansi_in_stdout': '\x1b' in so})
for r in rows:
    print('%-32s rc=%s sig=%s err=%s | want %s | stdout-only %s %s | JOINED %s %s | round-1 joined %s | develop %s' % (
        r['shape'], r['meta']['status'], r['meta']['signal'], r['meta']['error'], r['want'], r['lift'].get('stdoutOnly'), r['stdoutOnly'],
        r['lift'].get('joined'), r['joined'], r['lift'].get('round1Joined'), r['lift'].get('developJoined')))
    print('    stdout Tests/Test-Files lines: %s' % r['stdout_lines']); print('    stderr Tests/Test-Files lines: %s' % r['stderr_lines'])
    if r['note']: print('    note: ' + r['note'])
json.dump(rows, open(os.path.join(L, 'results.json'), 'w'), indent=1)
print('STDOUT-ONLY (the product path) WRONG on: %s' % [r['shape'] for r in rows if r['stdoutOnly'] != 'PASS'])
print('JOINED (the seat\'s "belt and braces" claim) WRONG on: %s' % [r['shape'] for r in rows if r['joined'] != 'PASS'])
