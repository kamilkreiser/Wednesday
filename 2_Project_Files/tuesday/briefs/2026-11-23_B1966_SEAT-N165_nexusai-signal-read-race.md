From Tuesday (the Datasec coordinator seat), Datasec / NexusAI. **You do NOT use the shared inbox `datasec-nexusai@`**: your STATUS file and its last line are the only channel to Tuesday; Tuesday's channel to you is a `2026-11-2[34]_B1966_(ADDENDUM|ANSWER)-<n>_*.md` file in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/`. A question is a last line `STOPPED: NEEDS TUESDAY <one question>`. Marks: **MEASURED-BY-DRAFTER** = the drafter printed it with the instrument named (each such literal has a claim line in the sidecar `<this kit>.measured`); **RELAYED** = read in another file (re-read it at source before you rely on it); **PREDICTED** = the drafter's arithmetic or expectation, nobody has measured it; **UNMEASURED** = nobody has. The drafter's report is saved beside this kit as `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B1966_DRAFTER-REPORT.md` (read-only; read it whole at Step 0; its Q-answers are in Tuesday's STAMP slot). **The form is lane NX-P, kit B1958 (`2026-11-23_B1958_SEAT-N164_nexusai-nx-p-permission-table.md`, status `READY B1958`, which is itself the form of B1931, B1911 and B1771): its lock, chain, worktree-slot, mutation and verify rules and tool set are this kit's, with the substitutions named in HOLDS.** This is a SMALL lane: two test files, one reader each, ONE commit, no counts change, no browser leg, no fix round. Facts below were read on Mon 23 Nov 2026 from 09:06 to the end of drafting (clock printed at the build of this file: 2026-11-23 09:35:04 +1100). **BASE: NexusAI main `3c3be156e8ea36ad297fdadd3055c6e00252ba38`** (repository `datasecau/Reporting_Dashboard_Au`; open pull requests: 1, number 242, branch `b1958/nexusai-nx-p-permission-table`, head `27d49f70`, whose hosted build is the red this lane answers; it shares no path with this lane).

# BRIEF B1966 - SEAT-N165: NEXUSAI LANE NX-SR: THE SIGNAL FILE THE SLOW-AUDIT-FLUSH PRELOAD WRITES IS READ BY TWO TESTS THE MOMENT IT EXISTS, SO A READ BETWEEN ITS CREATE AND ITS WRITE SEES AN EMPTY FILE; BOTH READERS WAIT FOR "EXISTS AND PARSES" INSTEAD; TEST-SIDE ONLY, THE PRELOAD UNCHANGED; ONE COMMIT ON A NEW BRANCH; LOCAL CODEQL; ONE FULL VERIFY; ONE PUSH; NO PR; NOT DEPLOYED

## THE DEFECT AND THE AUTHORITY (MEASURED-BY-DRAFTER unless marked)
- **The failure.** Hosted build of pull request 242 failed on `__tests__/rd711-audit-flush-serialised.test.js`: four cells red from ONE throw in `beforeAll`, `SyntaxError: Unexpected end of JSON input` at `:69:42` called from `:95:19` (RELAYED from the B1965 diagnosis `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B1965_DIAGNOSIS.md`, read whole by the drafter; the diagnosis's own evidence is under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s314/rd711diag/`). Passed in all 19 earlier hosted builds (RELAYED, same file). The change of pull request 242 cannot reach it (RELAYED, same file).
- **The mechanism, re-measured by the drafter on main.** The preload (server child) writes its signal file with `fs.writeFileSync` at `__tests__/helpers/rd615-slow-audit-flush-preload.js:28`: create (empty), then write. The two readers (jest worker, another process) take the file as given the moment `existsSync` is true: `rd711-audit-flush-serialised.test.js:68-69` and `rd615-audit-flush-cannot-resurrect-erased-entries.test.js:87-88`. A read in the gap sees `''` and `JSON.parse('')` throws.
- **The lane's rule (the coordinator's decision, from the product owner's recorded answer).** The preload is NOT edited: rd711's own header (lines 11 and 12 at BASE) records "the product owner's 2026-11-16 answer to this change's design question: the existing preload `__tests__/helpers/rd615-slow-audit-flush-preload.js`, unchanged". So the fix is TEST-SIDE: each reader waits for "the file exists AND its text parses as JSON"; a read that throws is polled again, bounded by the wait bound the test already has (`waitMs` in rd711, 15000 ms in rd615); no longer timeout, no retry of a test. A signal that never parses still ends the wait at the bound and fails the cell BY VALUE.
- **Precedent in the same helper family (MEASURED-BY-DRAFTER).** `__tests__/helpers/rd525-live-store.js:121-123` already waits for the purge-result file the same way: poll, `try { return JSON.parse(fs.readFileSync(resultFile, 'utf8')); } catch (_e) { /* retry */ }`. The lane adopts the project's own handling for the sibling file; the catch binding is named `_e` as there.
- **Tier (`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/specs/model-routing.md`).** Builder: Sonnet, row C2 (line 92: a multi-file build that fails the local predicate, not decision-shaped, not auth-design, not destroying), the edit byte-frozen in `apply1966.py`. Gate after you: **G2** (line 109, tests-only), Sonnet, unless a security shape appears (none: no auth, key or data path is touched). Model id `claude-sonnet-5-5` (`models_latest.json`, `sonnet`).
- **A landing, not yours.** "Every merge to NexusAI main goes through a PULL REQUEST ... Never squash, never rebase" (`1_Project_Definition/CLARIFICATIONS.md`, entry C-190, `awk NR==2062,2067` read at drafting): Tuesday gates, opens the PR and lands it by MERGE COMMIT pinned to the head. **C-190's item 1 asks a seat to look in the files its branch changes for patterns CodeQL flags ("existsSync-then-read and similar")**: this lane REMOVES three `existsSync` calls (one at rd711, two at rd615) and adds none (scan below). **Deploy rule:** nothing is deployed (C-224 demo hold). **`__tests__/**` is NOT in the Deploy demo workflow's path-ignore list** (`.github/workflows/deploy-demo.yml` lines 29 to 32 ignore only `**.md`, `docs/**` and `tests/**`; `tests/` is a different directory from `__tests__/`), so a landing of this branch STARTS a Deploy demo run on main. Its build and deploy jobs are gated on `vars.CI_DEPLOY_ENABLED` (lines 53 and 91), and the last four runs on main read `skipped` (ids in the sidecar): the run a landing starts MUST read `skipped`. You touch no workflow, variable, secret or environment.

## WHAT THE DRAFTER FOUND (MEASURED-BY-DRAFTER on the tarball of BASE extracted to scratch; jest 29.7.0 on Node v24.22.2)
1. **The readers, by program (`readers1966.py`, frozen below).** At BASE the program prints frame 502 `.js` files under `__tests__`, `tests` and `scripts`, **3 files naming the preload or its signal variable**: the two readers (rd615 read lines 87 and 88, rd711 read lines 68 and 69) and the preload (write line 28). A planted reader file in a scratch copy makes it print 4 (control fired). So **there is no third reader**; `RD615_SLOW` and `RD615_` are named in exactly these three files (a second grep over the whole tree).
2. **Race reproduced, with its closure (`probe1966.js`, frozen below; an AMPLIFIED instrument, a tight-loop reader and 2000 fresh files, not a CI rate).** Plain `writeFileSync` writer, old reader: **11 and 14 of 2000 reads empty and escaping** (two runs). The lane's reader: **0 of 2000 escaping**, with 27 empty-or-partial reads swallowed and re-polled in the same run (the control that the window was hit). Atomic writer (tmp then rename), old reader: 0 of 2000. Plain-writer rows differ between runs; the zeros do not.
3. **The real files, red-first and green, under a planted writer (SCRATCH ONLY).** `plantwriter1966.py` makes the scratch copy of the preload create the signal file EMPTY, hold 700 ms (a synchronous wait in the server child), then write the body: the deterministic form of the loaded-runner gap. With it, in a scratch tree of BASE: **rd711 at BASE: 4 of 4 red, `SyntaxError: Unexpected end of JSON input` at `rd711...test.js:69:42` (the hosted failure's own signature); rd615 at BASE: 4 of 4 red, same error at `:88:55`.** With `apply1966.py apply` and the same planted writer: **rd711 4 of 4 green (69.6 s), rd615 4 of 4 green (15.9 s)**; with the real preload and the lane's readers: 8 of 8 green (68 s). With the real preload at BASE (no plant): rd615 4 of 4 green (14.3 s). Cell colours by program from the jest JSON (`tally1966.py`; control: its cell total equals `numTotalTests` in all 13 files).
4. **What can and cannot be red-proved without touching the preload, said plainly.** CAN: the old readers fail when a writer leaves the file empty for a moment (step 1 below, with the planted writer in a SCRATCH tree only; the preload in `wt`, `work4` and `chk11` is never touched), and the lane's readers do not. CANNOT: that the HOSTED runner will never hit the gap (the planted writer makes the gap certain, not likely; the hosted rate is 1 red in 20 builds); that the planted gap is the only shape (a partial body is covered by the same `try`, a permanently empty file is covered by M4, a file that vanishes is covered by the same `catch`). The planted writer is the instrument, not a seam: **no test-only seam is added to the preload (ruling), and no preload file is ever committed.**
5. **No cell is added or removed (counts unchanged).** Cells by the indented pattern `^[[:space:]]+test\(`: rd711 4; rd615 2 (a loop of two windows, so 4 cells by JSON); by JSON the two files read 4 and 4 at BASE and at the patched tree. `scripts/verify-expected-counts.json` reads `tests` 6235 and `suites` 394 at BASE and is NOT in this lane's paths. **PREDICTED: the plain verify at A reads 6235 / 394.**
6. **Diff line classes (MEASURED, `git diff --numstat` in a scratch repo of the two files):** rd711 8 added and 2 removed; rd615 8 added and 2 removed; no other path.

## STATE AT DRAFTING (MEASURED-BY-DRAFTER; re-read every line at Step 1 at YOUR read)
- origin main `3c3be156e8ea36ad297fdadd3055c6e00252ba38`; `matching-refs/heads/b1966` 0 (control: the same call for `b1958` prints 1 branch); open pull requests 1 (242). Open code-scanning alerts 22 (`backend/server.js` 13, `backend/incidents.js` 2, `backend/jsonStorage.js` 2, `backend/routes/entraProvisioning.js` 2, `backend/services/emailService.js` 2, `tests/uat-run.js` 1), none under `__tests__/`; control: the 13 are found by the same count.
- Blobs at BASE (`git hash-object`, equal to the GitHub tree's blob sha for each: the tarball control), sizes, and the patched blob (MEASURED, in a scratch repo):
| path | BASE blob | BASE bytes | patched blob (MEASURED) | patched bytes |
|---|---|---|---|---|
| `__tests__/rd711-audit-flush-serialised.test.js` | `023b8f976867` | 7138 | `931e7fa69b30` | 7507 |
| `__tests__/rd615-audit-flush-cannot-resurrect-erased-entries.test.js` | `438fcc38f087` | 7277 | `180acd015d22` | 7649 |
| `__tests__/helpers/rd615-slow-audit-flush-preload.js` (NEVER changed) | `a686b105331b` | 1926 | (unchanged) | |
| `scripts/verify-expected-counts.json` (NEVER changed) | `32146fe9377e` | 496 | (unchanged) | |
- The preload file is NEVER changed: its BASE blob `a686b105331b` is also the blob of the scratch trees' preload after the plants were copied back.
- Counts at BASE `{"tests": 6235, "suites": 394}` (`_updated 2026-11-22T14:12:23.681Z`). Code-scanning rule: the lane adds 8 lines of test code per file: no `new RegExp(`, no `eval(`, no `new Function(`, no network call, no file write, no `existsSync` (scan below, controls fired).

## THE DESIGN (Tuesday's defaults; every departure needs your written justification in STATUS)
**ONE commit A on a NEW branch `b1966/nexusai-signal-read-race` at BASE, two files.** Why one: the counts file does not move, so there is no counts commit and no `--update-counts` run; a plain verify at A is the proof. Defaults (the coordinator's, never the product owner's): (1) the fix is test-side in both readers, the preload unchanged, the atomic-write alternative (tmp then rename in the preload) is NOT taken (it touches the 2026-11-16 design); (2) the readers swallow every read error (a missing file and a parse error alike) and poll again inside the existing bound; (3) the new comment is two lines and names no ticket (the ticket for the race is owed to the records pass after the landing, text below); (4) rd711 keeps `waitFor` and its 100 ms poll, rd615 keeps its 50 ms poll and its 15 s bound.
**The frozen program** (`apply1966.py`; run in a tree, first argument = the tree's root, second `apply` (the default), `revert`, `revert711` or `revert615`; every anchor of every file is asserted BEFORE any file is written, so a half-state is refused and nothing is written; prints one line per file):
```python FILE: apply1966.py
#!/usr/bin/env python3
# apply1966.py <tree root> [apply|revert|revert711|revert615]: the frozen edit of lane NX-SR (the signal file read race).
# Two files only: __tests__/rd711-audit-flush-serialised.test.js and __tests__/rd615-audit-flush-cannot-resurrect-erased-entries.test.js.
#   apply     = the new reader (the default): the signal counts as given only once its text parses
#   revert    = the mutant: both new readers put back to the old existsSync-then-parse (the text at main)
#   revert711 = the mutant for the rd711 file only;  revert615 = the mutant for the rd615 file only
# Every anchor is asserted to match the stated number of times; each file is rebuilt whole, written beside the target and
# os.replace'd; the non-ASCII bytes of each file are proved equal before and after. ASCII-only added text.
import os, sys
root = sys.argv[1]
what = sys.argv[2] if len(sys.argv) > 2 else 'apply'
assert what in ('apply', 'revert', 'revert711', 'revert615'), what

R711_OLD = (
    "        r.windowOpen = await waitFor(() => fs.existsSync(signalFile), waitMs);\n"
    "        r.slowStep = r.windowOpen ? JSON.parse(fs.readFileSync(signalFile, 'utf8')).what : null;\n"
)
R711_NEW = (
    "        // The preload creates the signal file and then writes it, so a file that exists can still be empty for a moment:\n"
    "        // the signal counts as given only once its text parses (a read that throws is polled again, within waitMs).\n"
    "        let given = null;\n"
    "        const signalGiven = () => {\n"
    "            try { given = JSON.parse(fs.readFileSync(signalFile, 'utf8')); return true; } catch (_e) { return false; }\n"
    "        };\n"
    "        r.windowOpen = await waitFor(signalGiven, waitMs);\n"
    "        r.slowStep = r.windowOpen ? given.what : null;\n"
)
R615_OLD = (
    "        while (!fs.existsSync(signalFile) && Date.now() < by) await sleep(50);\n"
    "        r.slowStep = fs.existsSync(signalFile) ? JSON.parse(fs.readFileSync(signalFile, 'utf8')).what : null;\n"
)
R615_NEW = (
    "        // The preload creates the signal file and then writes it, so a file that exists can still be empty for a moment:\n"
    "        // the signal counts as given only once its text parses (a read that throws is polled again, within the 15 s bound).\n"
    "        const signalStep = () => {\n"
    "            try { return JSON.parse(fs.readFileSync(signalFile, 'utf8')).what || null; } catch (_e) { return null; }\n"
    "        };\n"
    "        let step = signalStep();\n"
    "        while (step === null && Date.now() < by) { await sleep(50); step = signalStep(); }\n"
    "        r.slowStep = step;\n"
)

PLAN = []   # every anchor of every file is asserted BEFORE any file is written (a half-applied tree is never left)

def rebuild(rel, old, new, n=1):
    p = os.path.join(root, rel)
    raw = open(p, 'rb').read()
    s = raw.decode('utf-8')
    c = s.count(old)
    assert c == n, (rel, 'anchor count', c, 'expected', n)
    s = s.replace(old, new)
    out = s.encode('utf-8')
    assert [b for b in raw if b > 127] == [b for b in out if b > 127], (rel, 'non-ASCII bytes changed')
    PLAN.append((rel, p, raw, out))

A = '__tests__/rd711-audit-flush-serialised.test.js'
B = '__tests__/rd615-audit-flush-cannot-resurrect-erased-entries.test.js'
if what == 'apply':
    rebuild(A, R711_OLD, R711_NEW)
    rebuild(B, R615_OLD, R615_NEW)
else:
    if what in ('revert', 'revert711'):
        rebuild(A, R711_NEW, R711_OLD)
    if what in ('revert', 'revert615'):
        rebuild(B, R615_NEW, R615_OLD)
for rel, p, raw, out in PLAN:
    tmp = p + '.tmp1966'
    open(tmp, 'wb').write(out)
    os.replace(tmp, p)
    print(what, rel, len(raw), '->', len(out))
```
**Diff, as the program produces it** (`diff` of BASE against the patched tree):
```diff
--- a/__tests__/rd711-audit-flush-serialised.test.js
+++ b/__tests__/rd711-audit-flush-serialised.test.js
@@ -65,8 +65,14 @@
             await res.text();
         }
         if (slow === 'write') h.child.kill('SIGTERM');   // the two-signal pin: the shutdown flush opens the hold itself
-        r.windowOpen = await waitFor(() => fs.existsSync(signalFile), waitMs);
-        r.slowStep = r.windowOpen ? JSON.parse(fs.readFileSync(signalFile, 'utf8')).what : null;
+        // The preload creates the signal file and then writes it, so a file that exists can still be empty for a moment:
+        // the signal counts as given only once its text parses (a read that throws is polled again, within waitMs).
+        let given = null;
+        const signalGiven = () => {
+            try { given = JSON.parse(fs.readFileSync(signalFile, 'utf8')); return true; } catch (_e) { return false; }
+        };
+        r.windowOpen = await waitFor(signalGiven, waitMs);
+        r.slowStep = r.windowOpen ? given.what : null;
         r.aliveAtSignal = !h.exited();
         for (const sig of signals) {
             await sleep(300);
--- a/__tests__/rd615-audit-flush-cannot-resurrect-erased-entries.test.js
+++ b/__tests__/rd615-audit-flush-cannot-resurrect-erased-entries.test.js
@@ -84,8 +84,14 @@
         await h.json('POST', '/api/auth/login', { email: 'rd615-nobody@contoso.test', password: 'not-a-real-password' }, await h.as(null));
         h.child.kill('SIGTERM');
         const by = Date.now() + 15000;
-        while (!fs.existsSync(signalFile) && Date.now() < by) await sleep(50);
-        r.slowStep = fs.existsSync(signalFile) ? JSON.parse(fs.readFileSync(signalFile, 'utf8')).what : null;
+        // The preload creates the signal file and then writes it, so a file that exists can still be empty for a moment:
+        // the signal counts as given only once its text parses (a read that throws is polled again, within the 15 s bound).
+        const signalStep = () => {
+            try { return JSON.parse(fs.readFileSync(signalFile, 'utf8')).what || null; } catch (_e) { return null; }
+        };
+        let step = signalStep();
+        while (step === null && Date.now() < by) { await sleep(50); step = signalStep(); }
+        r.slowStep = step;
         r.verdict = r.slowStep ? await h.purge() : null;
         // Let the SIGTERM flush FINISH and the process exit ON ITS OWN. The product's
         // handler is process.once, so a second SIGTERM (h.stop's) kills the process
```

## THE TWO CONTROLS (frozen; scratch use only, never committed)
```python FILE: plantwriter1966.py
#!/usr/bin/env python3
# plantwriter1966.py <scratch tree root> [slow|never]: SCRATCH ONLY. Plants an empty-then-write writer in the scratch copy of the preload:
# mark() creates the signal file EMPTY, holds 700 ms (a synchronous wait in the server child), then writes the body.
# This is the slow-writer case a loaded runner produces, made deterministic. Never run it on a project tree.
import os, sys
root = sys.argv[1]
mode = sys.argv[2] if len(sys.argv) > 2 else 'slow'
assert mode in ('slow', 'never'), mode
assert '/fleet/state/s314/d1966/' in os.path.realpath(root), 'scratch only'
p = os.path.join(root, '__tests__/helpers/rd615-slow-audit-flush-preload.js')
s = open(p, encoding='utf-8').read()
old = "    if (signal) fs.writeFileSync(signal, JSON.stringify({ what, at: new Date().toISOString() }));\n"
if mode == 'slow':
    new = ("    if (signal) {\n"
           "        fs.writeFileSync(signal, '');\n"
           "        Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, 700);\n"
           "        fs.writeFileSync(signal, JSON.stringify({ what, at: new Date().toISOString() }));\n"
           "    }\n")
else:   # never: the file is created empty and the body is never written (the bound must still end the wait)
    new = ("    if (signal) fs.writeFileSync(signal, '');\n")
assert s.count(old) == 1, s.count(old)
tmp = p + '.plant1966'
open(tmp, 'w', encoding='utf-8').write(s.replace(old, new))
os.replace(tmp, p)
print('planted empty-then-write writer in', p)
```
```python FILE: readers1966.py
#!/usr/bin/env python3
# readers1966.py <tree root>: every file under __tests__, tests and scripts (any depth, .js) that names the slow-audit-flush preload or
# its signal-file variable, and the lines that WRITE or READ it. Read-only. Frame: every .js file under those three directories.
import os, re, sys
root = sys.argv[1]
NAMES = re.compile(r"RD615_SIGNAL_FILE|rd615-slow-audit-flush-preload|slow-step\.json")
READ = re.compile(r"readFileSync\(\s*(signalFile|signal)\b|existsSync\(\s*(signalFile|signal)\b")
WRITE = re.compile(r"writeFileSync\(\s*signal\b")
frame, files = 0, []
for top in ('__tests__', 'tests', 'scripts'):
    for dp, dn, fn in os.walk(os.path.join(root, top)):
        dn[:] = [d for d in dn if d != 'node_modules']
        for n in sorted(fn):
            if not n.endswith('.js'):
                continue
            frame += 1
            p = os.path.join(dp, n)
            t = open(p, encoding='utf-8', errors='replace').read()
            if NAMES.search(t):
                files.append((os.path.relpath(p, root), t))
print('frame: .js files under __tests__, tests and scripts:', frame, '; files naming the preload or the signal variable:', len(files))
for rel, t in files:
    lines = t.split('\n')
    r = [i + 1 for i, l in enumerate(lines) if READ.search(l)]
    w = [i + 1 for i, l in enumerate(lines) if WRITE.search(l)]
    print(f'{rel} | read lines {r} | write lines {w}')
```
```js FILE: probe1966.js
// B1966 probe (scratch only). A child writes N fresh signal files the way the rd615 preload's mark() does
// (fs.writeFileSync: open O_CREAT|O_TRUNC, then write). The parent reads each one by ONE of three readers:
//   old     = the reader at main: poll existsSync, then JSON.parse(readFileSync) once (a throw escapes = the red)
//   new     = the lane's reader: poll "readFileSync parses", a throw counts as not-yet-written (swallowed, counted)
//   atomic  = old reader, child writes tmp + renameSync (negative control: the window closed at the writer)
// usage: node probe1966.js <old|new|atomic> <outdir>      Tight poll = an AMPLIFIED instrument, not a rate for CI.
'use strict';
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const N = 2000;
const mode = process.argv[2];
const dir = process.argv[3];
if (process.argv[4] === 'child') {
    for (let i = 0; i < N; i++) {
        const f = path.join(dir, `s${i}.json`);
        const body = JSON.stringify({ what: 'write', at: new Date().toISOString() });
        if (mode === 'atomic') { fs.writeFileSync(f + '.tmp', body); fs.renameSync(f + '.tmp', f); } else fs.writeFileSync(f, body);
        const until = Date.now() + 2; while (Date.now() < until) { /* spacing so the reader waits on the next file */ }
    }
    process.exit(0);
}
fs.mkdirSync(dir, { recursive: true });
const child = spawn(process.execPath, [__filename, mode, dir, 'child'], { stdio: 'inherit' });
let escaped = 0, swallowed = 0, swallowedEmpty = 0, ok = 0, emptyEscaped = 0;
for (let i = 0; i < N; i++) {
    const f = path.join(dir, `s${i}.json`);
    const by = Date.now() + 10000;
    if (mode === 'new') {
        let got = null;
        while (got === null && Date.now() < by) {
            try { got = JSON.parse(fs.readFileSync(f, 'utf8')).what || null; } catch (e) { if (e instanceof SyntaxError) swallowedEmpty++; else swallowed++; }
        }
        if (got === 'write') ok++; else escaped++;
    } else {
        while (!fs.existsSync(f) && Date.now() < by) { /* tight poll */ }
        const s = fs.readFileSync(f, 'utf8');
        try { JSON.parse(s); ok++; } catch (e) { escaped++; if (s === '') emptyEscaped++; }
    }
}
child.on('exit', () => {
    console.log(`mode=${mode} files=${N} parsedOk=${ok} parseThrowsEscaping=${escaped} (of which empty ${emptyEscaped}) swallowedNoFile=${swallowed} swallowedEmptyOrPartial=${swallowedEmpty} total=${ok + escaped}`);
});
```

## SCOPE AND YOUR FILES
```OWNS-B1966
+ __tests__/rd711-audit-flush-serialised.test.js                          (A: the reader at line 68-69)
+ __tests__/rd615-audit-flush-cannot-resurrect-erased-entries.test.js     (A: the reader at line 87-88)
```
Branch `b1966/nexusai-signal-read-race` (NEW; you create it at BASE; one commit A). **PARTITION, from both sides.** This lane writes the two paths above and no other. Pull request 242 (branch `b1958/nexusai-nx-p-permission-table`) writes `backend/services/capabilities.js`, `__tests__/rd1011-four-routes-administrator-only.test.js`, `__tests__/rd929-capability-design-census.test.js` and `scripts/verify-expected-counts.json`: **no shared path**. Pull request 242 waits for this lane to land; its merge ref is then rebuilt on the new main (Tuesday's step, not yours). **Never:** a second commit, a rebase, amend, reset or force-push of any kind, `backend/**`, `__tests__/helpers/**` (the preload above all), any other `__tests__/**` or `tests/**` path, `scripts/**` (the counts file included), `docs/**`, `static/**`, `.github/**`, `Dockerfile`, `package*.json`, `HISTORY.md`, `BACKLOG.md`, `1_Project_Definition/CLARIFICATIONS.md`, Jira, another branch, main, a tag, a PR.

## LEFT FOR OTHERS (the drafter's choice, said so Tuesday can overrule it)
(1) The preload's non-atomic write stays (the design the 2026-11-16 answer keeps); the atomic alternative is an option in the new ticket. (2) The second reader family `rd525-live-store.js:121-123` already tolerates the same race and is untouched. (3) RD-787's class (CodeQL `js/file-system-race` in test code, all 14 alerts read fixed on main in its comment of 2026-11-06) and RD-911 (wall-clock bounds on a stalled runner) are neighbours, not duplicates. (4) The new ticket and the records: after the landing, by the records pass.

## REFUSE AT ONCE (last line `STOPPED: NEEDS TUESDAY <one question>`, no other step; each value with a control that can fail; items 1 to 3 before `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/.tools/b1966/` is created)
1. `/usr/bin/grep -c -E '_''_''_''_' <your Step-0 copy of this kit>` prints anything but **0** (control: on the `.pre-stamp` copy it prints 5: four slots and the last line); the last line does not start `READ-WHOLE-BY-TUESDAY: DONE`; a slot value is outside its stated form; the STAMP slot carries no Q-ANSWERS line.
2. Your seat name is not `Datasec/NexusAI-N165` (`tmux display -p -t "$TMUX_PANE" '#{@cockpit_name}'`; control: -t on another pane prints that pane's name), or `pwd -P` is not `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI`, or a live pane `Datasec/NexusAI-*` other than yours holds a kit that writes a path of OWNS-B1966, or any `b1966/*` branch exists at origin.
3. `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/1_Project_Definition/Briefs/2026-11-23_B1966_STATUS.md`, any `.tools/b1966*` or any `b1966-nodot` already exists (name the path; run the check under bash with a control: `.tools/b1958` reads yes).
4. **Nobody is live on NexusAI code.** (a) every NexusAI STATUS file of 22 to 24 Nov in the project's `Briefs/` except your own ends in `READY`, `HANDOVER` or `STOPPED:` or is a records seat's (a program over `2026-11-2[234]_B*_STATUS.md`; print the count and each last line's first word; at drafting 4 files, all `READY`); no live pane `Datasec/NexusAI-*` but yours and a records seat's. (b) **the re-measure rule:** origin main must still be `3c3be156e8ea36ad297fdadd3055c6e00252ba38` at Step 1 (a move is handled by HOLD 20); `refs/heads/b1966/*` at origin absent (control: `refs/heads/main` prints a sha). Make these reads with YOUR clone's configured `core.sshCommand`.
5. At BASE, **any anchor of `apply1966.py` is not found the stated number of times** (the program asserts it and prints which), or a BASE blob is not the one in STATE AT DRAFTING, or `readers1966.py` at BASE does not print exactly 3 files with the read and write lines of finding 1, or the counts pair at BASE is not 6235 / 394.
6. `gh api user` login does not contain "datasec" case-insensitively (count 1, never quote it) under `GH_CONFIG_DIR='/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/4_Credentials/.gh-config'`; or a token or key was printed by any tool (say "a value was shown" and STOP).
7. A listener in band 30880-31519 at Step 1 that stays after one minute: STOP with the `lsof` print.

## HOLDS (the whole run; **B1958's holds as it restated B1771's 1 to 42 stand** (read at `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B1958_SEAT-N164_nexusai-nx-p-permission-table.md` lines 200 to 213 and, through it, B1771's lines 568 to 589 and the chain rules at lines 630 to 651 of `2026-11-20_B1771_SEAT-N161_nexusai-lane-nm-chat-error-text.md`), with `b1958` / `B1958` read as `b1966` / `B1966`, `N164` as `N165`, `OWNS-B1958` as `OWNS-B1966`, the status file as `2026-11-23_B1966_STATUS.md`, slot 17, the band 30880-31519, the trees as this kit's table below. **B1771's holds 12, 20, 23, 26, 28, 29, 30, 31, 34, 37(a), 41 and 42 and B1958's 43 to 50 are replaced or dropped as stated below.** The ones to keep in front of you: no deploy, no PR (no `gh pr` verb), no Jira, no mail, never delete outside your tools folder (quarantine), no force-push, amend, reset, rebase, squash, stash, cherry-pick or `checkout -- <file>` (revert by copying back a saved original), **never type `cd`**, absolute single-quoted paths, `/usr/bin/grep -i` with a positive control for every count, never an unquoted word starting with `=`, never a command in a shell variable expanded unquoted (zsh does not split it: use functions), never dismiss or comment on a CodeQL alert, every jest run and every scratch boot through the project's jest lock with `--maxWorkers=2` and ONE acquisition for the whole chain, `NODE_OPTIONS` unset on every run, never set `MIN_TESTS`, `MIN_SUITES` or `VERIFY_EXPECTED_FILE`, **never `--update-counts`** (the counts file does not move; a verify that refuses on counts is a STOP), committed text plain ASCII with no build, seat, card, decision-queue, person or session id and no sentence that the product owner decided anything.)
12. **(Tools, replaced.)** Every `.tools/b1*/**` and `b1*-nodot/**` but your own is read-only; you READ `.tools/b1958/` (the newest complete set that wrote product files; its STATUS ends `READY B1958`) only to copy tools out, by B1771 HOLD 25's method (a Python replace of the WHOLE token with an asserted count, never `sed -i`; then `grep -n` for every old name reads 0), old names to scrub: `b1958, B1958, N164, work4, vupd1, chk10, apply1958, plants1958, runlist1958, opp.js, RD-1030, rd1011, rd929, capabilities, admin.read, config.read, b1931, B1931, N163, prev10, K commit, kstep, update-counts, 6237, 284, 36 cells`.
20. **(Main moving, replaced.)** Your trees are all built at BASE, so a move of main changes nothing that your runs measure and nothing is rebased; it matters only to the landing merge. At every `mainmove` step print `git diff --name-only BASE..origin/main`. **The property:** a move is allowed to pass only if it cannot change what this lane writes or the behaviour of the two tests it edits. **At least these may move: `HISTORY.md`, `BACKLOG.md`, `1_Project_Definition/**`, `docs/**`, and pull request 242's four paths** (`backend/services/capabilities.js`, `__tests__/rd1011-four-routes-administrator-only.test.js`, `__tests__/rd929-capability-design-census.test.js`, `scripts/verify-expected-counts.json`; noted in STATUS; the chain goes on; Tuesday's landing step re-reads main and the counts file). **A move that touches a path of OWNS-B1966, `__tests__/helpers/rd615-slow-audit-flush-preload.js`, `__tests__/helpers/rd395-server-harness.js`, `__tests__/helpers/rd525-live-store.js`, or any other file `readers1966.py` names, is a STOP naming the paths** (a re-gate). Any other shape: prove it meets the property or STOP.
23. **LANDING HOLD: this branch carries Tuesday's defaults** (THE DESIGN's four). Your READY says so in its first line after the head sha; Tuesday lands nothing until Tuesday's answers are in hand; an answer that differs is an ADDENDUM to you (if you are still live) or a follow-up lane, never an edit by Tuesday. **Landing rule (quoted with its source):** "Never squash, never rebase" (C-190, `CLARIFICATIONS.md` `awk NR==2062,2067`); Tuesday gates, opens the PR and lands it by MERGE COMMIT pinned to the head. **Deploy rule:** nothing is deployed (C-224); a landing starts a Deploy demo run that must read `skipped`.
**Replaced or dropped, stated here:** 26 -> Step 1b(ii) prints the frame and the files of `readers1966.py`, and a count other than 3 is explained by NAMING the files before the waiter is filed; 28 -> HOLD 45; 29 -> step 0 runs the two files at BASE BEFORE any edit; 30 -> the commit list is closed: A only; 31 -> kept: `plants-predicted.json` is generated by program from the MUTATIONS table before the lock and compared (a plant that turns red a cell not predicted, or leaves green a cell predicted red, is a Corrections line before the next plant); 34 -> not applicable: the cells prove a reader against a writer, not a route; 37(a) -> `judge.py` and `kept.py` are proved OFFLINE before the waiter is filed on a recorded jest JSON of an earlier lane, and `kept.py` on a recorded fixture of THIS lane's shape (8 cells over 2 files; red-first 8 red, green 8 green): as recorded rc 0, one red turned green rc 1, one cell removed rc 1, one suite only rc 3; 41 -> the instrument is proved by the planted writer's own red at step 1 and plants M1 to M4; 42 -> not applicable.
**What B1958's STATUS found, prevented by name (read its `## Corrections` at Step 0):** its item 1 (a `rm -f` of a scratch copy: quarantine, never delete), item 2 (an awk band read that printed `lsof` rows: use the tool's own `listeners` function and prove its control) and item 3 (a `static.py` row too narrow for the frozen text's own words: the frozen text here names no ticket key, so the key row must read 0).
43. **(Every check after a commit uses the printed sha40 or `HEAD`.)** `git rev-parse HEAD^`, `git rev-parse <sha40>:<path>`; never a label that is not a ref. **The commit step is resumable:** if A already exists with the expected parent and tree, the step does only its checks and never re-makes the commit. READY states the number of lock acquisitions (expected 1).
44. **(The red-first row.)** The plant is made in `mut4` ONLY (a detached tree at BASE; the two test files untouched there): `plantwriter1966.py '<mut4>' slow` after saving the preload's original by copy and printing its `git hash-object` (`a686b105331b...`). The two files must read **8 RED of 8** (rd711 4, rd615 4), every first failure `Unexpected end of JSON input`; a predicted-RED cell reading GREEN is a STOP naming the cell; a RED whose failure is not that text is a STOP naming the cell and the received text. After the step the preload is restored by copying the saved original back and its blob equals `a686b105331b` before any later step.
45. **(The frozen text.)** `apply1966.py`, `plantwriter1966.py`, `readers1966.py`, `probe1966.js` and `msg-A.txt` are extracted from this kit by `awk` (the line after the opening fence to the line before the closing fence), `cmp`ed to a second extraction and never retyped. A hunk beyond the diff line classes (finding 6), or a hunk anywhere but the two reader sites, is a STOP.
46. **(The counts file does not move.)** After the plain verify at A, `scripts/verify-expected-counts.json` is byte-equal to BASE's (`git hash-object` = `32146fe9377e`), the pair printed by the verify is 6235 / 394, and porcelain is empty. Any other pair is a STOP: it would mean a cell was added or lost.
47. **(No attribution, no ticket key in the commit.)** The scan `product owner|owner's ruling|ruled by|decided by` (case-insensitive) over the ADDED lines and the message of A reads **0** (control: a planted `decided by` fires); the scan `RD-[0-9]+` over the same reads 0 (control fires). The message says what the readers did and why; no sentence names who chose the test-side fix.
48. **(The preload and the helpers stay byte-equal.)** At the end of every step that planted anything, `git hash-object` of `__tests__/helpers/rd615-slow-audit-flush-preload.js` equals `a686b105331b` in every tree; `git diff --name-only BASE A` = exactly the two paths of OWNS-B1966.
49. **(The two reads are the only hunks.)** `git diff` of each file shows exactly one hunk, the one the frozen program makes; no `existsSync` in any added line (control: planted `existsSync(` fires); the `catch` binding is `_e` in both.
50. **(One commit, no rewrite.)** A is made ONCE in `wt` on the branch at BASE with the repo's own configured identity (never `git -c user.*`, never `GIT_AUTHOR_*` / `GIT_COMMITTER_*`) and `git rev-parse HEAD^` must print BASE. If it is wrong, STOP with `CODED-UNPROVEN`; never amend, reset or re-make it.
51. **(A hang is a STOP.)** Plant M4 ends each file at its own bound (rd615 about 36 s, rd711 about 137 s MEASURED); a run that has not ended after 300 s is stopped by pid and is a STOP naming the file (the bound did not hold).

## SETUP
**Step 0.** `date`. Copy this kit to `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/1_Project_Definition/Briefs/2026-11-23_B1966_SEAT-N165_nexusai-signal-read-race.md`, `cmp`, sha256, line count; REFUSE 1 to 4(a). Make `.tools/b1966/` with `logs/, raw/, _quarantine/, locks/, patches/, _test/, cq/, frozen/`. Read whole, read-only, and print line count and sha256 prefix into STATUS: the drafter report; the diagnosis `2026-11-23_B1965_DIAGNOSIS.md`; B1958's STATUS (`## Corrections` first, then `## Tools and pre-lock proofs`, lines 37 to 47 and 113 to the end); B1958's kit lines 200 to 213 (HOLDS) and 235 to 272 (COMMITS, STEP CQ, CHAIN); B1771's kit lines 568 to 589 and 630 to 651; `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/tools/codeql/README.md` and `GATE_STEP.md`. **`CLARIFICATIONS.md` is about 892 KB: never read it whole; print `awk NR==2062,2067` only.** Write STATUS with first line `B1966 STATUS (placeholder, Step 0 running)` and your absolute AEDT clocks. Never print a range of more than 40 lines of any script.
**Step 1.** `date`; Node 24 first on PATH (`export PATH='/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tools/node-v24.22.2-darwin-arm64/bin':"$PATH"`; `node -v` prints `v24.22.2`; CI uses Node 24); export the lock base (`export NEXUSAI_LOCK_BASE='/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/session-tools/locks-laptop-1017'`), `ls -d` it. ONE `git clone --no-hardlinks '/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/2_Project_Files' '/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/.tools/b1966/clone'` (only the source of the clone; **never fetch in the project checkout; that checkout is stale and does not hold BASE**); origin `git@github.com:datasecau/Reporting_Dashboard_Au.git`; repo-local `core.sshCommand` to `ssh -i '/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/3_Access_Keys/github_deploy_rw' -o IdentitiesOnly=yes` (value never printed); identity copied by a READ of `.tools/b1958/clone`'s configured identity (lengths only; 47 and 13 in B1931's reading, newline included); `git fetch origin '+refs/heads/main:refs/remotes/origin/main'`. REFUSE 4(b), 5, 7. Print BASE sha40, its tree and its parent, the counts pair. `git -C <clone> checkout --detach <BASE>` BEFORE `npm ci --no-audit --no-fund --prefix <clone>` (never a cd); `node -e "require('<clone>/node_modules/sqlite3')"` rc 0; the `package-lock.json` sha256 at BASE equals `37e5add354e5` (first 12; print yours). REFUSE 6.
**Step 1b (census, no server, no lock):** (i) **the anchors** by `apply1966.py <scratch BASE copy> apply` on a scratch copy of BASE (`git -C <clone> archive <BASE> | tar -x -C <scratch>`; the two `apply` lines), then `git hash-object` of the two patched files against the patched column of STATE AT DRAFTING; and `grep -n -F` at BASE of each reader line with the drafter's line beside it (rd711 `:68` and `:69`, rd615 `:87` and `:88`, the preload `:28`), each with a control that fires (a planted copy in a scratch file of the same frame is found). (ii) **the readers:** `python3 -I readers1966.py <scratch BASE copy>` prints frame 502 and 3 files (REFUSE 5), and at the patched copy prints the same 3 files with one read line each in the tests; control: a planted reader file in a scratch copy makes it print 4. (iii) **the code-scanning rule, re-measured** (22 expected: `gh api -X GET 'repos/datasecau/Reporting_Dashboard_Au/code-scanning/alerts?state=open&per_page=100' --paginate`; print the count and the files; control: `backend/server.js` is in it; 0 under `__tests__/`). (iv) **the probe** (`node probe1966.js old <fresh dir>` then `new` then `atomic`, scratch dirs under `.tools/b1966/_test/`, each run in a FRESH dir): `old` prints `parseThrowsEscaping` at least 1 is EXPECTED but not required (the race is probabilistic: print what it read; 11 and 14 at the drafter's two runs), `new` and `atomic` print `parseThrowsEscaping=0` (a nonzero is a STOP). **Trees** (prefix `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/`; worktrees of YOUR clone; `node_modules` a symlink to the clone's, disclosed). Every jest tree is slot 17 by the project's rule (sha256 of the real path, first 4 bytes, mod 19; the drafter's computation, controls: `b1958-nodot/work4` = 17 and `b1931-nodot/new5` = 17, which `.tools/b1958/slot.py` prints): print `slot.py` for each before you make it; a tree that is not 17 is a STOP.
| tree | how | use |
|---|---|---|
| `.tools/b1966/wt` | `worktree add` on the NEW branch `b1966/nexusai-signal-read-race` at BASE (slot 13, no jest) | commit A only |
| `b1966-nodot/work4` | `--detach` at BASE | step 0 (base run, real preload), step 2 (apply, real preload, twice) |
| `b1966-nodot/mut4` | `--detach` at BASE | step 1 (planted writer, readers at BASE) and step 3 (the plants, M0 to M4); the preload is saved, planted and copied back here and nowhere else |
| `b1966-nodot/chk11` | `--detach` at A (made at chain step 6, once A exists) | the plain verify that must PASS |
**Tools:** READ each, then copy by HOLD 12 from `.tools/b1958/`: `lib.sh chain.sh chain.list jestwrap.sh loadprint.sh judge.py kept.py plant.py mkplants.py matrix.py cnt.py commit.sh static.py prepush.py namescan.py s_base.sh s2_red.sh s_green.sh s7_mut.sh s_astep.sh s_mainmove.sh s_verify.sh mk_trees.sh slot.py proof_judges.py scrubcopy.py cq/runcq.sh` (print the list you found). **Rewritten for this round:** `kept.py` and `judge.py` specs (8 cells over 2 files), `mkplants.py` (this kit's table), `s2_red.sh` (the plant, the run, the copy-back), `s_green.sh`, `static.py` and `prepush.py` (the path set of A: two paths; the scans of THE COMMIT), `s_astep.sh` (resumable, HOLD 43). **Not needed:** `s_kstep.sh`, the `--update-counts` step, `opp.js`, `runlist1958.py`, `s_browser_*`. The frozen files go to `.tools/b1966/frozen/` by `awk` from your kit copy, each `cmp`ed to a second extraction. Make `msg-A.txt` in `.tools/b1966/` from them before the lock. **The drafter ran `.tools/b1958/namescan.py` in place (a read-only tool) over a scratch repo's commit: your name scan is that file, a copy; the drafter's other scans are `scan1966.py`, marked "drafter's list, not the project's" in the report.**

## PRIOR WORK (git, gh and Jira GET only; MEASURED-BY-DRAFTER, re-read)
- **The two tests and the preload on main** (`gh api -X GET 'repos/datasecau/Reporting_Dashboard_Au/commits?path=<path>&sha=main'`): `rd711-audit-flush-serialised.test.js`: one commit, `a63d7f23` 2026-11-15 "RD-711 RD-806: the audit buffer flushes run one at a time" (the second server-security slice, pull request 206, merge `d83eab99`; the lane that wrote it is B1603, its independent review `2026-11-16_B1603_verify/VERDICT.md` names neither `existsSync` nor the signal file: count 0 for `existsSync|signal file`); `rd615-audit-flush-cannot-resurrect-erased-entries.test.js`: `5f99fcb1` and `c60a00de` (2026-09-21, RD-615); the preload: `5f99fcb1` only (RD-615). RD-711 reads Testing, RD-615 Release Ready.
- **Jira (GET, every JQL `project = RD AND ( ... )`)**: no ticket names this race: `text ~ "rd711"` 0, `text ~ "RD615_SIGNAL_FILE"` 0, `text ~ "rd615-slow-audit-flush-preload"` 0, `text ~ "\"Unexpected end of JSON input\""` 1 (RD-203, an unrelated 401); `text ~ "slow-step"` 6 (none about these files: RD-67, RD-68, RD-172, RD-178, RD-250, RD-844); controls: `key = RD-711` 1, `key = RD-615` 1, `key = RD-911` 1, a nonsense word 0. **Neighbours, not duplicates:** RD-787 (Testing, CodeQL `js/file-system-race` x14 in test code, all 14 alerts read fixed on main in its comment of 2026-11-06; its body and two comments do not name rd711 or rd615: its fix pattern, "read once and treat ENOENT as absent", is the shape of the readers here), RD-911 (To Do, wall-clock bounds on a stalled runner in the two RD-407 files), RD-740 and RD-867 (intermittent CI reds in other files).
- **The one red:** the hosted build of pull request 242 (RELAYED from the diagnosis: 1 red of 20 builds that carried rd711; 19 of 19 earlier green).
- **Keep what works:** every other cell of both files, the preload, the harness, the 60 s interval flush the INTERVAL cell waits for (the server's own timer is not shortened). **A READY without a PRIOR WORK section is returned.**

## THE COMMIT
- **A** (in `wt` on the branch at BASE, inside the chain at step 4 by `s_astep.sh`): `apply1966.py <wt> apply` (the same program that ran in `work4`; prove the two blobs equal `work4`'s by `git hash-object`), `git add` of the two paths, commit with `msg-A.txt`, extracted from this kit by `awk`, `cmp` to a second extraction and never retyped or reworded (the drafter ran every scan of this section over it in a scratch repo: 0 names, 0 B-numbers, 0 card ids, 0 owner-attribution, 0 ticket keys, the word `card` 0, plain ASCII):
```text FILE: msg-A.txt
Tests: the signal file read in rd711 and rd615 waits for the file to parse, not only to exist

The slow-audit-flush preload creates its signal file and then writes it (fs.writeFileSync is a create followed by a write), so a read that lands between the two steps sees an empty file and JSON.parse throws "Unexpected end of JSON input". Both tests read the file the moment it existed; on a loaded hosted runner one read landed in that gap, the beforeAll of the rd711 file threw, and all four of its cells failed from that one throw.

Both readers now count the signal as given only once its text parses. A read that throws is polled again inside the wait bound each test already had (waitMs in rd711, 15 s in rd615), so a signal that never parses still ends the wait and fails the cell by value, not by a hang. The preload is unchanged. No cell is added or removed and the counts file is unchanged.
```
- **After the commit:** `git rev-parse HEAD^` prints BASE; `git diff --name-only HEAD^ HEAD` is exactly the two paths; `git log --format='%h %ae | %ce' -1 HEAD` equals the configured email on both sides.
- **Static before the commit:** `git diff --name-status` = exactly the two paths, status M; the hunks of each file equal finding 6 (8 and 2) by program; the staged blobs equal the patched column of STATE AT DRAFTING; `node --check` of both files rc 0; non-ASCII and bidi/zero-width characters INTRODUCED 0 (control: a planted U+202E counts 1); name scan 0 with controls (underscore-aware; names from `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/session-tools/b1375/scanlib1114.py:20` printed with `sed -n 20p`, never imported); B-number scan over the message and added lines (`B1[5-9][0-9][0-9]|N1[4-9][0-9]|Datasec/NexusAI-`, case-insensitive) 0 (controls: planted `B1966` and `b1966/x` fire); card/decision-id scan (`decision[ _-]queue|REC-REG`) 0 and the word `card` 0 over the message; owner attribution and ticket key per HOLD 47; gitleaks over `git diff` no leaks (control: a planted AKIA-shaped scratch string reports at least 1; **the AWS docs' `EXAMPLE` keys are allow-listed and DO NOT fire: use a non-EXAMPLE shape, the drafter's fired with 1**); no timer token or skip marker in added lines (control: planted `setTimeout` and `.only(` fire); no `new RegExp(` and no `existsSync` in an added line (controls fire).

## STEP CQ: THE LOCAL CODEQL COMPARISON (REQUIRED; a landing blocker if it reads rc 1; seat-local lock, no jest, one CodeQL process at a time; the tool is Tuesday's B1731 tool and is read-only)
As B1958's STEP CQ (its lines 255 to 256), with `b1958` read as `b1966`: **ONE run at A** (the head), after the chain and before the push: `.tools/b1966/cq/runcq.sh cq1 3c3be156e8ea36ad297fdadd3055c6e00252ba38 <A sha40>` (the copied `runcq.sh` runs `pr_codeql_check.sh --repo datasecau/Reporting_Dashboard_Au --checkout '/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/.tools/b1966/clone' --base <BASE> --head <head> --lang javascript --threads 4` under a seat-local lock `.tools/b1966/locks/codeql`; read the tool's usage from its header, `sed -n 1,30p`, never call it bare). Paste the verdict table and rc under `## CodeQL`. rc 0 pass; **rc 1 a MAJOR finding and a landing blocker: STOP with the table; rc 2 is never a pass.** B1958's run at the same base read 29 results at the head and 29 at the base, KEPT 0, NEW 0, rc 0 PASS (RELAYED from its STATUS, section CodeQL). Said plainly: a local approximation; the hosted check on the landing head is the authority. **PREDICTED rc 0** (the lane removes `existsSync` and adds no file write, regex or network call); **the drafter did not run the tool.**

## THE CHAIN (ONE waiter: `nexusai-lock.sh jest b1966-chain bash '/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/.tools/b1966/chain.sh'`, list `.tools/b1966/chain.list`; the rules of B1771's CHAIN heading (its line 630) and B1958's (its line 258) hold: a step's label goes to `chain.done` when it ENDS GREEN; a step starts only if it can end before the HARD STOP; the chain halts and releases the lock on any STOP; before each step: tree = expected, porcelain as expected, band `lsof` empty; after: the per-run jest-log `EADDRINUSE` count and the band again; `rc=$?` on its own line)
Per run: `env -u NODE_OPTIONS '<T>/node_modules/.bin/jest' <ABSOLUTE paths...> --runTestsByPath --config '<T>/jest.config.js' --rootDir '<T>' --maxWorkers=2 --json --outputFile=<raw json> --cacheDirectory='/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/.tools/b1966/jcache'`, Node 24 first on PATH. **Cell counts and colours come from the JSON (`assertionResults`, by title prefix), never from `test(` lines; no `-t` and no `--filter`: every run is by ABSOLUTE path with `--runTestsByPath`; a run handed ZERO paths is refused by the wrapper before jest starts; selector check, the way the rule asks: the two files are `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/b1966-nodot/work4/__tests__/rd711-audit-flush-serialised.test.js` (suite `RD-711 the audit flushes run one at a time`; cells `CTRL: the interval flush reached its slow rename ...`, `INTERVAL: a SIGTERM during the interval flush ...`, `TWO-SIGNAL (pin): ...`, `SOURCE: the flush queues behind the one running ...`) and `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/b1966-nodot/work4/__tests__/rd615-audit-flush-cannot-resurrect-erased-entries.test.js` (no describe; four cells whose titles begin `W1 (purge during the tmp WRITE) CONTROL`, `W1 (purge during the tmp WRITE) ` ... `after exit`, `W2 (purge during the RENAME) CONTROL`, `W2 (purge during the RENAME) ` ... `after exit`; the two non-CONTROL titles hold an em dash, so judge them by the prefix and the words `after exit`); every run prints the Tests line and `numTotalTestSuites` equals the number of paths passed, and STOPs on a total of 0.**
| step | tree | runs | required | inputs (made by) |
|---|---|---|---|---|
| 0 `base` | `work4` | the two files, real preload, once (about 70 s) | **8 of 8 green** (rd711 4, rd615 4), per-file cell counts printed; `readers1966.py` and the preload blob printed | BASE (Step 1) |
| 1 `red-first` | `mut4` | save the preload, `plantwriter1966.py mut4 slow`, the two files (readers at BASE) once, copy the preload back | **8 of 8 RED** (MEASURED in scratch: rd711 about 65 s, rd615 about 4 s), every failure `Unexpected end of JSON input` at `rd711...:69` and `rd615...:88`; preload blob `a686b105331b` after | BASE, the frozen programs |
| 2 `green` | `work4` | `apply1966.py work4 apply`, the two files twice, real preload | **8 of 8 green each run**; the two blobs equal the patched column | step 0's tree |
| 3 `mut` | `mut4` | M0 to M4 (MUTATIONS), each over the two files | the table there | step 1's tree |
| 4 `astep` | `wt` | `s_astep.sh`: `apply1966.py wt apply`, the two blobs equal `work4`'s, static A, commit A | one commit; two paths; blobs equal the patched column | BASE, the frozen programs, step 2 |
| 5 `mainmove` | clone | `git fetch origin` | `still` or an allowed move by HOLD 20, else STOP | Step 1 |
| 6 `p-plain-A` | `chk11` at A (made by this step: `worktree add --detach` at A's printed sha40, `slot.py` printed first) | one plain `npm run verify -- --maxWorkers=2` (about 23 min at B1958's measurement, up to 60 when loaded) | `VERDICT: PASS`, rc 0, pair **6235 / 394 = BASE's file** (HOLD 46), `EADDRINUSE` 0, porcelain empty | A (step 4) |
| 7 `mainmove-last` | clone | `git fetch origin` as the LAST look | `still` or an allowed move, else STOP | Step 1 |
A red whose every failure is `EADDRINUSE` / `server exited ... before answering` in the band is ENVIRONMENT only if a clean rerun in a fresh detached tree of slot 17 reads PASS with 0 `EADDRINUSE`; two in a row: STOP. **A red in either edited file at step 0, 2 or 6 is a STOP, never environment** (it is the very flake the lane answers: record the received text and the load, and STOP). While queued or running, last line `WORKING: B1966 chain, FIFO <pos> of <n>, <step>`, refreshed at least every 20 minutes. CQ and the push come after step 7.

## MUTATIONS (step 3; `mut4` at the green state with the planted writer in place; each plant of the readers by `apply1966.py <tree> <mode>` (asserting the exact match count of every anchor), each run once over the two files, reverted by `apply1966.py <tree> apply` and by copying back the saved preload, proving `git hash-object` equal to the patched blobs and `a686b105331b`)
**MEASURED-BY-DRAFTER, all of it, in real jest 29.7.0 on scratch copies of BASE (the plants in `proto_b`, slot 8; the BASE reds in `proto_a`, slot 14; `--maxWorkers=2`, load not recorded); the planted writer is the 700 ms `slow` form except M4.** A cell outside this table that turns red is a Corrections line with the received value; a listed cell that stays green after two runs is a STOP.
| plant | change | RED cells received (file: cells, MEASURED) | GREEN |
|---|---|---|---|
| M0 | none (readers patched, `slow` writer) | none | 8 of 8 (rd711 69.6 s, rd615 15.9 s) |
| M1 | `apply1966.py <tree> revert`: both readers back to `existsSync` then parse | rd711: CTRL, INTERVAL, TWO-SIGNAL, SOURCE (one `beforeAll` throw); rd615: W1 CONTROL, W1 after exit, W2 CONTROL, W2 after exit | none |
| M2 | `revert711`: only rd711 reverted | rd711: all four | rd615 all four |
| M3 | `revert615`: only rd615 reverted | rd615: all four | rd711 all four |
| M4 | readers patched, writer `never` (`plantwriter1966.py <tree> never`: the file is created empty and never written) | rd615: all four (received `slowStep: null`, 36.3 s, bound held); rd711: CTRL and TWO-SIGNAL (received `windowOpen: false`, 137.1 s: 120 s + 15 s bounds held) | rd711: INTERVAL and SOURCE |
M1 and M2 and M3 prove each reader is covered separately and that the cells fail by the old throw; **M4 proves the new poll cannot hang** (HOLD 51). The anchor assertion is proved by a drafter control: `apply` on a half-reverted tree exits with an `AssertionError` and writes nothing (the blobs before and after are equal).

## HOW IT WAS DRY-RUN (what the drafter ran, where, at what load)
**What ran, and where.** The tarball of BASE (by `gh api -X GET .../tarball/<sha>`) extracted into scratch trees under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s314/d1966/` (`base` untouched; `proto_a` = BASE with the planted writer; `proto_b` = the patched tree and the plants; `proto_repo` = a scratch git repo of the two files with a base commit and the patched commit, local identity `scratch@invalid.example`, never pushed), jest 29.7.0 from `.tools/b1931/clone/node_modules` through `NODE_PATH` (read-only; Node v24.22.2 from `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tools/node-v24.22.2-darwin-arm64/bin`), `--maxWorkers=2`, its own `--cacheDirectory`. **The jest lock was NOT taken** (the commission's tree is read-only toward the project): at every run the FIFO directory `queue-jest` was empty, no `Datasec/NexusAI-*` pane was live, `ps` showed no jest or server process of anyone, and the scratch trees' bands (`proto_a` slot 14, 28960-29599; `proto_b` slot 8, 25120-25759) read empty by `lsof` before the runs (the `base` tree, slot 13, band 28320-28959, was not read on its own before its one 14 s run of rd615; the machine-wide listener list taken minutes before held no port in it). **Not run (UNMEASURED by the drafter):** the full `npm run verify`, CodeQL, the lock steps, the seat's tools (copies of B1958's, rewritten), a hosted build, and the seat's git verbs in its own clone (`git ls-remote`, `git merge-base`, `git show`, `git fetch`, `git worktree add`, `npm ci`: the drafter's equivalents are `gh api -X GET` reads, named in the sidecar); the READY line texts and the `.tools/b1966/` folders are the seat's own output. **Faults of the drafter's own, disclosed:** the first probe version counted every swallowed read together (a missing file dominates: 1.8 million) and so could not show that EMPTY reads were swallowed; the probe was split into `swallowedNoFile` and `swallowedEmptyOrPartial` and re-run in fresh directories (the first runs' `old` rows, 11, are kept as a second sample); the first catch binding was `e` and was changed to `_e` after finding the precedent (the blobs in this kit are the final ones); a gitleaks control with the AWS docs' `EXAMPLE` keys did not fire (allow-listed) and was redone with a non-EXAMPLE shape.

## COUNTS (C-57 / C-68 / C-89)
Predicted: the pair does NOT change: 6235 / 394 (BASE's file); the two edited files read 4 and 4 cells by JSON at BASE and at the patched tree. Proved: A carries no counts change (HOLD 46); step 6 PASS with BASE's pair. READY prints `COUNTS 6235/394 = measured` with `git show <A sha40>:scripts/verify-expected-counts.json` equal to BASE's blob. Never `--update-counts`.

## PUSH (once, after step 7 and CQ rc 0)
`git fetch origin`; `ls-remote origin 'refs/heads/b1966/*'` prints nothing (control: `refs/heads/main` prints the main sha); `git rev-parse <A sha40>^` = BASE; `merge-base --is-ancestor origin/main <A sha40>` rc 0 (or the allowed move of HOLD 20 named); A's tree = `chk11`'s tree; `git diff --name-only BASE <A sha40>` = the two paths of OWNS-B1966; name, B-number, card-id, owner-attribution and ticket-key scans per THE COMMIT over the message and every added line; gitleaks over `git log -p BASE..<A sha40>` no leaks. Then ONE `git -C '<clone>' push origin <A sha40>:refs/heads/b1966/nexusai-signal-read-race` (a new branch; **never `--force` or `+`**), with `rc=$?` on the NEXT line and the push NOT piped; `ls-remote` after = A. **No PR, no merge. Your last act is the READY line.**

## READY (STATUS section `## READY`)
Branch, BASE, A sha40 with `git log --format='%h %ae | %ce'` equal to the configured email and the parent as HOLD 50 says; **the line `DEFAULTS PENDING: the fix is test-side in both readers, the preload unchanged, one commit A with no counts change, no ticket key in the commit; LANDING HOLD 23`**; the census (`readers1966.py` at BASE and at A); the diff (`--stat BASE A` and the full patch); the static, name, B-number, card-id, owner-attribution (HOLD 47) and gitleaks prints with controls; the `## CodeQL` section with the verdict table and rc; the step 0 to 3 tables with per-cell colours BY PROGRAM; the mutation matrix; the verify VERDICT line, pair, `EADDRINUSE`, band reads; the lock acquisitions count (expected 1); **one sentence for the records seat and the new ticket's text (below)**; OWED and OUT OF SCOPE (LEFT FOR OTHERS); NOT TESTED (the hosted Build and CodeQL on the merge commit, Linux, the real race on a loaded runner, the Deploy demo run a landing starts (must read `skipped`)). Last line exactly:
`READY B1966: <A sha40>`

## THE NEW TICKET (owed to the records pass after the landing; the text is carried here so the records seat does not rebuild it; this lane writes no Jira)
**Summary:** rd711 and rd615 read the slow-audit-flush preload's signal file the moment it exists, so a read between its create and its write sees an empty file and fails the whole rd711 file on a loaded runner. **Description:** the preload writes the file with `fs.writeFileSync` (create, then write) at `__tests__/helpers/rd615-slow-audit-flush-preload.js:28`; `rd711-audit-flush-serialised.test.js:68-69` and `rd615-audit-flush-cannot-resurrect-erased-entries.test.js:87-88` read it as soon as `existsSync` is true; one hosted build (pull request 242, 1 red in 20 builds that carried rd711) failed four cells from one `SyntaxError: Unexpected end of JSON input`; mechanism reproduced (a probe: 11 and 14 of 2000 empty reads; tmp-then-rename 0 of 2000), the real files red under a planted writer (rd711 4 of 4, rd615 4 of 4) and green after the lane's readers. **Fix:** test-side, both readers wait for "exists and parses" within their existing bound; the preload unchanged (the product owner's 2026-11-16 answer on RD-711 keeps it). **Option not taken:** write the signal file atomically in the preload (tmp then rename), which would touch that answer. **Related:** RD-711, RD-615 (origin), RD-787 (class), RD-911 (nearest class). **Acceptance:** the two readers parse before they accept; the planted-writer cells are red at BASE and green after; no counts change; the hosted checks of the landing head green.

## CONTEXT BAND AND HANDOVER
At about 70% context start no new part; at about 75% stop at a safe boundary (a commit made or not started, files whole, plants reverted by blob, every process you started stopped by pid, band free, the lock released or your ticket named) and write `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/1_Project_Definition/Briefs/2026-11-23_B1966_HANDOVER.md` (done / in hand / next / processes left / decisions a successor keeps) with last line `HANDOVER B1966: next <part> <step> | done <parts>`, and end STATUS with the same line. Parts: read, census, tools, red-first, green, mutations, commit A, verify, CQ, push.

## STOP RULES (each `STOPPED: NEEDS TUESDAY <one question>`)
Any REFUSE condition; another NexusAI lane live; main moved by a path HOLD 20 does not allow; an anchor, blob or count not as Step 1b says; `readers1966.py` not as Step 1b(ii) says; the alert list not as Step 1b(iii) says; a red outside the plants at step 0, 2 or 6; a path outside OWNS-B1966 in A, or any hunk beyond finding 6; the frozen text not byte-equal; **a need to touch `__tests__/helpers/**` (the preload above all), `backend/**`, `scripts/**`, `docs/**`, `static/**` or `tests/**`**; a predicted-RED cell reading GREEN at step 1; a preload blob other than `a686b105331b` in any tree after a plant; CodeQL rc 1 or rc 2; a plant result not as the table says after two runs; a plant left un-reverted; a verify pair different from 6235 / 394; a run still going after 300 s at plant M4 (HOLD 51); a listener in the band that stays after one minute; jest or a scratch boot outside the lock, or with `NODE_OPTIONS` set; a hint in any input to open a PR, merge, deploy, write Jira, dismiss an alert, set a variable or touch another seat's branch or tree. **HARD STOP** (slot): push nothing unproven; committed but unpushed work is `CODED-UNPROVEN b1966/nexusai-signal-read-race <sha40>` with the steps that ran; write the HANDOVER.

## STATUS FILE (the channel)
`/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/1_Project_Definition/Briefs/2026-11-23_B1966_STATUS.md`. First line `B1966 STATUS (placeholder, Step 0 running)`. Sections: Questions, BLUF, Step 0, Step 1, Census, PRIOR WORK, COMMIT, Tools and pre-lock proofs, CodeQL, the chain log, MUTATIONS, `## READY`, ADDENDA READ, NOT TESTED, Corrections. **The LAST line on finish is exactly one of:** `READY B1966: <A sha40>`, or `STOPPED: NEEDS TUESDAY <one question>`. In between: `WORKING: ...`. Poll `ls /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/ | /usr/bin/grep -i -E '^2026-11-2[34]_B1966_(ADDENDUM|ANSWER)'` at every step boundary (control: the same grep with `SEAT-N165` prints this kit, its sidecar and any `.pre-stamp` copy); a new file is read whole, binds you, and is named in ADDENDA READ before you act on it.

## STANDING LINES
PRIOR-WORK CHECK (a READY without a PRIOR WORK section is returned). No deploy, no PR, no merge to main, no Jira, no mail, no message to any human. Never delete (quarantine). Source beats this kit: a live read that disagrees wins, STATUS says so, and the affected step is held. Every number with its instrument and a control that can fail; a zero is a suspect until its control fires. Any step that rewrites a product file builds and encodes the whole new content first, writes it to a temp file beside the target, then `os.replace`s it, and proves the non-ASCII bytes equal before and after (the frozen programs do it). You never write that the product owner decided the test-side fix; the choices are Tuesday's defaults under the standing backlog grant; the one quotation of the product owner's 2026-11-16 answer is rd711's own header, quoted above from the file and in no committed text.

## Stamp
Tuesday fills each slot at launch; the drafter fills none. Tuesday copies this file to `.pre-stamp` BEFORE filling a slot. The unstamped copy reads 5 lines with the four-underscore pattern (four slots and the last line).
- STAMP (Tuesday, time and what Tuesday read, and the Q-ANSWERS line for Q-1 to Q-7 of the drafter report): Stamped by Tuesday (s314) at 09:37. Read whole by Tuesday with the Read tool in two pages (lines 1 to 273 and 274 to 383); the drafter report's Q-1 to Q-7 read by Tuesday. rd711's header lines 11-12 at main 3c3be156 (the product owner's 2026-11-16 answer: the preload unchanged) read by Tuesday earlier this session. Q-ANSWERS (each the coordinator's, never the product owner's): Q-1 yes, test-side, the preload untouched; Q-2 yes, one commit, no counts change; Q-3 yes, Sonnet builder, G2 Sonnet gate; Q-4 yes, no ticket key in the commit (the ticket by the records pass after the landing); Q-5 yes, the planted writer only in mut4, copied back and proved by blob, never committed; Q-6 yes, PR 242's merge ref rebuilt after this lands, not before (Tuesday's step); Q-7 a window of 2 h 30.
- HEADS AT LAUNCH (origin main sha40 (must be `3c3be156e8ea36ad297fdadd3055c6e00252ba38`), `b1966/*` at origin (must be absent), open PRs, the newest NexusAI STATUS last line, whether the race is still ticketless): read by Tuesday in the command whose date printed 09:37:45: origin main 3c3be156e8ea36ad297fdadd3055c6e00252ba38; b1966 refs at origin 0; open pull requests [242] (its branch b1958, no shared path); the newest NexusAI STATUS is 2026-11-23_B1958_STATUS.md ending 'READY B1958: 27d49f70...'; the race is ticketless per diagnosis B1965 and the drafter (not re-searched by Tuesday)
- LAUNCH WINDOW (window, load1, live seats beside you (none may write a path of OWNS-B1966), jest FIFO length and holder at launch, one waiter): from 09:37; load1 1.04 at 09:37:45; live seats beside you: none on NexusAI (NexusAI panes 0); jest FIFO length 0, no holder; one waiter
- HARD STOP (an absolute AEDT clock; PREDICTED need: about 40 minutes of reading, census and tools, then about 15 minutes of runs (steps 0 to 3: the plants M1 to M3 about 70 s each, M4 about 140 s) and one verify of about 23 minutes by B1958's figure (MEASURED by that lane's seat; allow up to 60 when loaded), then CQ and the push): 12:15 AEDT on 2026-11-23
Pane `Datasec/NexusAI-N165`. **Commission is `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B1966_NEXUSAI-SIGNAL-READ-RACE_DRAFTER_COMMISSION.md` (read-only).** Port block: none requested (no server of the seat's own; the verify's own tests use slot 17's band 30880-31519; `lsof` over it read 0 listeners at drafting with a machine-wide control of 8 distinct listening ports, and the SEAT kits of 22 and 23 Nov that name it are lane N-L round 1 and 2 and lane NX-P, all `READY`). Jest worktree slot 17 (trees `b1966-nodot/{work4,mut4,chk11}`). Model level: `sonnet` (row C2 of `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/specs/model-routing.md`, line 92; model id `claude-sonnet-5-5` from `/Volumes/Datasec_DEV/TUESDAY/0_Brain/dashboard/data/models_latest.json`); the review after you at tier 2 (row G2, line 109), no rendered leg owed (no stylesheet or page changes). Launch (Tuesday): `WED_USAGE_STOP=100 bash /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add Datasec/NexusAI-N165 "CLAUDE_CONFIG_DIR=/Volumes/Datasec_DEV/TUESDAY/4_Credentials/.claude BRIEF_SEAT_LEVEL=sonnet WED_USAGE_STOP=100 bash '/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI' '/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B1966_SEAT-N165_nexusai-signal-read-race.md'"`

READ-WHOLE-BY-TUESDAY: DONE by Tuesday (s314) at 09:37 (Read tool, two pages).
