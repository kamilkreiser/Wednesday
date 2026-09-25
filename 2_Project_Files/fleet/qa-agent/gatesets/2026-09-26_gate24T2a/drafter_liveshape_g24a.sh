#!/bin/bash
# drafter_liveshape_g24a.sh — the DRAFTER's own capture of real vitest 4.1.11 piped `--reporter=default` summaries (a PREDICTION instrument
# for the kit; the gate re-captures and grades through the REAL code path). Fixtures under <work>/_sp/live/, OUTSIDE any package; vitest from
# <work>/_sp/pkg (npm ci of the #1245 head's own systemTest/performance lockfile). stdin /dev/null, stdout+stderr piped to files.
set -u
W="$(dirname "$(/bin/realpath "$0")")"; L="$W/_sp/live"; VT="$W/_sp/pkg/node_modules/.bin/vitest"
mk() { mkdir -p "$L/$1"; printf '%s\n' "$3" > "$L/$1/$2"; }
mk S01_failonly a.test.ts "it('f', () => { expect(1).toBe(2); });"
mk S02_skiponly a.test.ts "it.skip('s', () => {});"
mk S03_todoonly a.test.ts "it.todo('t');"
mk S04_xfailonly a.test.ts "it.fails('x', () => { throw new Error('boom'); });"
mk S05_xfail_pass a.test.ts "it.fails('x', () => { throw new Error('boom'); }); it('p', () => {});"
mk S06_fail_pass_skip a.test.ts "it.skip('s', () => {}); it('f', () => { expect(1).toBe(2); }); it('p', () => {});"
mk S07_passonly a.test.ts "it('p', () => {});"
mk S08_multifile a.test.ts "it('f', () => { expect(1).toBe(2); }); it.skip('s', () => {});"
mk S08_multifile b.test.ts "it('p', () => {});"
mk S09_allfailed a.test.ts "it('f1', () => { expect(1).toBe(2); }); it('f2', () => { expect(1).toBe(2); }); it('f3', () => { expect(1).toBe(2); });"
mk S10_everylabel a.test.ts "it('f1', () => { expect(1).toBe(2); }); it('f2', () => { expect(1).toBe(2); }); it('p1', () => {}); it('p2', () => {}); it.fails('x', () => { throw new Error('b'); }); it.skip('s1', () => {}); it.skip('s2', () => {}); it.todo('t');"
mk S11_orient a.test.ts "it('f1', () => { expect(1).toBe(2); }); it('f2', () => { expect(1).toBe(2); }); it('p1', () => {}); it('p2', () => {}); it('p3', () => {});"
mk S12_beforeall a.test.ts "describe('d', () => { beforeAll(() => { throw new Error('hook'); }); it('a', () => {}); it('b', () => {}); });"
mk S13_lookalike_stdout a.test.ts "it('logs', () => { console.log('      Tests  5 passed (5)'); }); it('f', () => { expect(1).toBe(2); });"
mk S14_lookalike_stderr a.test.ts "it('logs', () => { console.error('      Tests  5 passed (5)'); }); it('f', () => { expect(1).toBe(2); });"
mk S15_notests a.test.ts "const x = 1;"
mk S16_ctxskip a.test.ts "it('rs', (ctx) => { ctx.skip(); }); it('p', () => {});"
mk S17_xfail_unexpectedpass a.test.ts "it.fails('x', () => {}); it('p', () => {});"
mk S18_importerror a.test.ts "throw new Error('collect'); it('p', () => {});"
mk S19_diffcontext a.test.ts "it('d', () => { expect('a\\n      Tests  9 passed (9)\\nb').toBe('a\\n      Tests  9 passed (9)\\nc'); }); it('p', () => {});"
for d in "$L"/S*; do
  n="$(basename "$d")"; files="$(cd "$d" && ls *.test.ts)"
  ( cd "$d" && "$VT" run --root "$d" --globals --reporter=default $files < /dev/null > "$d/stdout.txt" 2> "$d/stderr.txt"; echo $? > "$d/rc.txt" )
  printf '%-26s rc=%s | %s\n' "$n" "$(cat "$d/rc.txt")" "$(grep -h -E '^[[:space:]]*(Test Files|Tests)[[:space:]]' "$d/stdout.txt" "$d/stderr.txt" | tr '\n' '#')"
done
