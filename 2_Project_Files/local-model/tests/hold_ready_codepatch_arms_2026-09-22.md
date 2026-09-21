# hold_ready.py code_patch arms — Tue 22 Sep 2026 03:45:18 AEST

backup: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/hold_ready.py.pre-0922-0345-codepatch
backup cmp rc=0
## Arm 1 BEFORE (old code, --dry-run on ks947 night2 test_only)
rc=0
DRY-RUN OK → READY_KS-947-F3F4b-R16_ornith35b-q4_BRIEFED-TESTONLY-MFA-LIMITER-OPTION-PARITY-AND-SPEC-MAX-PASS-8of8_2026-09-22.diff.md
  golden: golden not located — no byte-identity claim is made
  plus=66 minus=0 cells=10 tampers=3 nonascii=0
  header: > ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks947-ornith35b-night2/out.md.checker/patch.diff`** (from `ls` at 03:45 2026-09-22). Checker T3 (verbatim from checker.out): `PASS T3 diff applies at the tip (strict git apply --check)`; golden not located — no byte-identity claim is made.
  prnote: **PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it)
## Arm 2 BEFORE (old code, FAIL run ks947 night)
rc=1
Traceback (most recent call last):
  File "/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/hold_ready.py", line 37, in <module>
    co = open(os.path.join(run, 'checker.out')).read()
  File "<frozen codecs>", line 325, in decode
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xc2 in position 1214: invalid continuation byte
## Defect reproduction (old code on KS-1265 code_patch run)
    tip = inp['tip']; test_file = inp['test_file']; mode = inp.get('test_mode'); runner = inp.get('runner')
                                  ~~~^^^^^^^^^^^^^
KeyError: 'test_file'
## Arm 1 AFTER (new code, same --dry-run on ks947 night2) — Tue 22 Sep 2026 03:48:48 AEST
rc=0
cmp whole rc=1
ARM1 VERDICT: cmp clock-normalised rc=0 (       5 lines each; diff follows if any)
4c4
<   header: > ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks947-ornith35b-night2/out.md.checker/patch.diff`** (from `ls` at 03:45 2026-09-22). Checker T3 (verbatim from checker.out): `PASS T3 diff applies at the tip (strict git apply --check)`; golden not located — no byte-identity claim is made.
---
>   header: > ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks947-ornith35b-night2/out.md.checker/patch.diff`** (from `ls` at 03:48 2026-09-22). Checker T3 (verbatim from checker.out): `PASS T3 diff applies at the tip (strict git apply --check)`; golden not located — no byte-identity claim is made.
## Arm 2 AFTER (new code, FAIL run ks947 night, test_only T4 FAIL)
ARM2 VERDICT: rc=2
hold_ready: REFUSE — checker.out RESULT is not PASS: absent
## Arm 3 (new code, code_patch FAIL runs)
### 2026-09-20_ks1275-ornith35b-night :: RESULT: FAIL (1 failed) — stopped at A3 (cannot sequence red-first without exactly one test file)
ARM3 VERDICT (2026-09-20_ks1275-ornith35b-night): rc=2
hold_ready: REFUSE — checker.out RESULT is not PASS: RESULT: FAIL (1 failed) — stopped at A3 (cannot sequence red-first without exactly one test file); FAIL lines: ['FAIL A3 touched-file set is not {product, one test under Blockchain/Dev/services/originate/src/__tests__}: n=1 product=0 tests=1 other=0 ref_test_touched=yes']
### 2026-09-18_ks1233-ornith35b-night :: RESULT: FAIL (1 failed) — stopped at A4 (a test-side defect, not a product red)
ARM3 VERDICT (2026-09-18_ks1233-ornith35b-night): rc=2
hold_ready: REFUSE — checker.out RESULT is not PASS: RESULT: FAIL (1 failed) — stopped at A4 (a test-side defect, not a product red); FAIL lines: ['FAIL A4 RED-FIRST: the test is red at the tip but NOT for the right reason — CONTROL cell(s) red at the tip: control: in-memory path round-trips settings without expiry | control: other keys still use a TTL via setex (harness reach (2 failed / 3 run); the harness does not reach the code, so the red proves nothing']
### 2026-09-18_ks1190-ornith35b-night :: RESULT: FAIL (3 failed)
ARM3 VERDICT (2026-09-18_ks1190-ornith35b-night): rc=2
hold_ready: REFUSE — checker.out RESULT is not PASS: RESULT: FAIL (3 failed); FAIL lines: ['FAIL A4 RED-FIRST: the test file is NOT red at the untouched tip (rc=0, 0 failed / 8 run) — it does not prove the defect', "FAIL A5 GREEN-AFTER: src/__tests__/ks1190-api-gateway-meetsverificationlevel-fails-open-on.test.ts still red (or empty) after the product hunk (rc=1, 4 failed / 8 run): ['KS-1190", 'FAIL A6 whole services/api-gateway suite: NEW red(s) vs the untouched tip (see suite_delta.out)']
## Arm 3b (old code on the same code_patch FAIL run — for the record)
KeyError: 'test_file'
## Arm 2 AFTER, re-run after the refusal-message fix — Tue 22 Sep 2026 03:49:04 AEST
ARM2 VERDICT: rc=2
hold_ready: REFUSE — checker.out RESULT is not PASS: RESULT: FAIL (1 failed) — stopped at T4 (the diff is not the brief's lines; no test is run); FAIL lines: ['FAIL T4 BRIEF LINES — MISSING \'+\' \'const blanked = call.replace(/\\\'[^\\\']*\\\'/g, "\\\'\\\'").split(LF).map((line) => line.split(\\\'//\\\')[0]\'�']
## Arm 1 AFTER, re-run after the refusal-message fix
rc=0
ARM1 VERDICT (re-run): cmp clock-normalised rc=0
## Arm 4 (new code, --dry-run KS-1265 code_patch PASS 7/7 with golden) — Tue 22 Sep 2026 03:49:12 AEST
ARM4 VERDICT: rc=0
DRY-RUN OK → READY_KS-1265-EARLYGUARD-R16_ornith35b-q4_BRIEFED-CODEPATCH-ISSUERNAME-AT-GUARD-BEFORE-SAVE-PASS-7of7_2026-09-22.diff.md
  golden: CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed3-drafter-precheck/1265EARLYGUARD-R16/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) IDENTICAL in every file; body lines (context included) DIFFER in documents.ts (identical in ks549-documents-create-issuer-name-persist.test.ts); hunk headers differ (documents.ts: golden `@@ -614,3 +614,11 @@` vs run `@@ -611,6 +611,14 @@ documentsRouter.post(`; ks549-documents-create-issuer-name-persist.test.ts: golden `@@ -141,11 +141,8 @@` vs run `@@ -141,11 +141,8 @@ describe('KS-549 POST /api/documents — top-level issuerName persists into data', () => {`); APPLIED RESULT IDENTICAL: both patches applied strictly (`git apply -p1`, scratch tempdir) to the tip content carried in input.json['files'] yield byte-identical files (ks549-documents-create-issuer-name-persist.test.ts/documents.ts, sha256 equal)
  touched=['Blockchain/Dev/services/originate/src/__tests__/ks549-documents-create-issuer-name-persist.test.ts', 'Blockchain/Dev/services/originate/src/routes/documents.ts'] product_plus=8 product_minus=0 red=1/4 green=4/4 suite=809->809 strict=True nonascii=0
  header: > ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1265-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 03:49 2026-09-22; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1265-ornith35b-night/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1265-ornith35b-night/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed3-drafter-precheck/1265EARLYGUARD-R16/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) IDENTICAL in every file; body lines (context included) DIFFER in documents.ts (identical in ks549-documents-create-issuer-name-persist.test.ts); hunk headers differ (documents.ts: golden `@@ -614,3 +614,11 @@` vs run `@@ -611,6 +611,14 @@ documentsRouter.post(`; ks549-documents-create-issuer-name-persist.test.ts: golden `@@ -141,11 +141,8 @@` vs run `@@ -141,11 +141,8 @@ describe('KS-549 POST /api/documents — top-level issuerName persists into data', () => {`); APPLIED RESULT IDENTICAL: both patches applied strictly (`git apply -p1`, scratch tempdir) to the tip content carried in input.json['files'] yield byte-identical files (ks549-documents-create-issuer-name-persist.test.ts/documents.ts, sha256 equal).
  prnote: **PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/documents.ts` (+8/-0 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks549-documents-create-issuer-name-persist.test.ts` (+4/-7); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); secti
## Arm 4 re-run (body-lines clause now carries counts) — Tue 22 Sep 2026 03:50:02 AEST
ARM4 VERDICT (re-run): rc=0
  golden: CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed3-drafter-precheck/1265EARLYGUARD-R16/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) IDENTICAL in every file; body lines (context included) DIFFER in documents.ts (run 14 vs golden 11 body lines — context, since the change lines are equal) (identical in ks549-documents-create-issuer-name-persist.test.ts); hunk headers differ (documents.ts: golden `@@ -614,3 +614,11 @@` vs run `@@ -611,6 +611,14 @@ documentsRouter.post(`; ks549-documents-create-issuer-name-persist.test.ts: golden `@@ -141,11 +141,8 @@` vs run `@@ -141,11 +141,8 @@ describe('KS-549 POST /api/documents — top-level issuerName persists into data', () => {`); APPLIED RESULT IDENTICAL: both patches applied strictly (`git apply -p1`, scratch tempdir) to the tip content carried in input.json['files'] yield byte-identical files (ks549-documents-create-issuer-name-persist.test.ts/documents.ts, sha256 equal)
## Arm 5 (extra) code_patch refusal discipline on scratch copies of the KS-1265 run (the run dir is never modified)
ARM5a (copy without red_first.json) VERDICT: rc=2 :: hold_ready: REFUSE — red_first.json is missing: /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/bb573f73-d12e-46c4-921d-63e47258b61b/scratchpad/ks1265_copy_a/out.md.checker/red_first.json
ARM5b (declared test file differs from touched) VERDICT: rc=2 :: hold_ready: REFUSE — touched ['Blockchain/Dev/services/originate/src/__tests__/ks549-documents-create-issuer-name-persist.test.ts', 'Blockchain/Dev/services/originate/src/routes/documents.ts'] != declared ['Blockchain/Dev/services/originate/src/__tests__/other.test.ts', 'Blockchain/Dev/services/originate/src/routes/documents.ts'] (input.json product_file + suggested_test_file)
ARM5c (apply_check_strict_1.out non-empty while A2 claims strict) VERDICT: rc=2 :: hold_ready: REFUSE — apply_check_strict_*.out non-empty / opts carry an accommodation ([(1, 'Blockchain/Dev/services/originate/src/routes/documents.ts', 'error: patch failed: x:1')], recount=False) but the A2 line claims strict: PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)
ARM5d (copy's RESULT rewritten to FAIL) VERDICT: rc=2 :: hold_ready: REFUSE — checker.out RESULT is not PASS: RESULT: FAIL (1/7); FAIL lines: ['FAIL A6 whole services/originate suite: no NEW red vs the untouched tip']
## REAL HOLD (KS-1265) — Tue 22 Sep 2026 03:50:10 AEST
HELD → /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1265-EARLYGUARD-R16_ornith35b-q4_BRIEFED-CODEPATCH-ISSUERNAME-AT-GUARD-BEFORE-SAVE-PASS-7of7_2026-09-22.diff.md
  golden: bytes differ; applied result IDENTICAL; touched=2 product_plus=8 product_minus=0 red=1/4 green=4/4 suite=809->809 strict=True
rc=0
## ornith_status.py first line — Tue 22 Sep 2026 03:50:10 AEST
ORNITH: queue 0 · runner not running · newest KS-947 RESULT: PASS (8/8) done 02:54
## diff stat
 2_Project_Files/local-model/night/hold_ready.py | 248 +++++++++++++++++++++++-
 1 file changed, 245 insertions(+), 3 deletions(-)
## Brief-path fix: first READY cited night/briefs/KS-1265-EARLYGUARD-R16.md (ROWID-built); real file is briefs/KS-1265-R16-EARLYGUARD.md. First READY QUARANTINED, not deleted — Tue 22 Sep 2026 03:50:57 AEST
quarantined to: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/_quarantine_2026-09-22/
READY_KS-1265-EARLYGUARD-R16_ornith35b-q4_BRIEFED-CODEPATCH-ISSUERNAME-AT-GUARD-BEFORE-SAVE-PASS-7of7_2026-09-22.diff.md
## Arm 1 AFTER (re-run after brief-path fix)
ARM1 VERDICT (final): cmp clock-normalised rc=0
## Arm 4 (re-run after brief-path fix)
ARM4 VERDICT (final): rc=0
## REAL HOLD (KS-1265), second — Tue 22 Sep 2026 03:50:57 AEST
HELD → /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1265-EARLYGUARD-R16_ornith35b-q4_BRIEFED-CODEPATCH-ISSUERNAME-AT-GUARD-BEFORE-SAVE-PASS-7of7_2026-09-22.diff.md
  golden: bytes differ; applied result IDENTICAL; touched=2 product_plus=8 product_minus=0 red=1/4 green=4/4 suite=809->809 strict=True
rc=0
Brief (located by ticket + ROWID tokens under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1265-R16-EARLYGUARD.md`
## ornith_status.py first line — Tue 22 Sep 2026 03:50:57 AEST
ORNITH: queue 0 · runner not running · newest KS-947 RESULT: PASS (8/8) done 02:54
## diff stat (final)
 2_Project_Files/local-model/night/hold_ready.py | 256 +++++++++++++++++++++++-
 1 file changed, 253 insertions(+), 3 deletions(-)
