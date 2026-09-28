# KS-1371: Ornith brief + golden (POST /api/status/:id/unrevoke refuses index -1 with 400)

Written 06:26 AEST 2026-09-29 (shell `date`) by a screening drafter for Wednesday. It ran no model, raised no PR, changed no GitHub or Linear state (Linear was only READ: by the screen and by `build_input.sh`), mailed nobody, and wrote nothing under `!CODING/`. Every git write verb ran in its own `--shared` clones under `scratchpad/screen0929/`. The Blockchain checkout was only read (`ls-remote`, `cat-file`, `clone --shared` from it); `prepare_clone.sh` reported its tracked-modified count as 0 after each farm.

- **Tier: ORNITH** (Spark is the fallback). It is one product hunk (two lines replaced by three, every byte in the brief) plus one test hunk that appends four cells to an existing file whose harness is reused unchanged. The same file and test already passed Ornith 7/7 for the sibling change (KS-1269-U, 2026-09-19).
- **Base:** develop `215cc6875e2bac0b6d6b38918572384fbfcbdb77`, read by `git ls-remote` at 06:08 AEST. The object is local in the Blockchain checkout. Measured in `screen0929/base` (`clone --shared` + detached checkout; node_modules farmed by `tasks/code_patch/prepare_clone.sh`; `packages/shared` built in the clone).
- **Shape:** `status.ts:328`-`:329`, in the `/unrevoke` KS-1269 check, becomes `(!Number.isInteger(req.body.index) || req.body.index < 0)` with the message `'index must be a non-negative integer'`, plus one comment line. `/revoke` is untouched and still admits `-1`, which is the KS-662 ruling.
- **Why the test is appended, not a new file:** the append reuses `dispatch`/`unrevokeWith` verbatim. A new file would be an 86-line transcription. That variant was measured first: a new 6-cell file went 2 failed / 4 passed at the tip, and it passed with the fix (21/21 together with both KS-1269 files; suite 17 files / 152 / 0). It was moved to `scratchpad/screen0929/_moved/`. For Ornith, the smaller output is the safer one.

## Files
- `KS-1371.md` is the brief: 14,351 chars, sha256 `42644e2a51d3b9c7…`.
- `KS-1371.golden.diff` is the golden: sha256 `0238cdd9b9d224c9…`. It touches 2 files, with 21 `+` lines (17 non-blank) and 2 `-` lines.
- **Fence rebuild:** the brief's two ```diff fences are IDENTICAL to the golden's two hunks (`fencecheck.py`). Control: mutating one token in a brief copy (`-7` → `-8`) printed DIFFER.
- **Char lint:** 0 `+` lines contain a backslash, backtick, double quote or non-ASCII character. There are 0 blank context lines and 0 non-ASCII context lines. The leading context `:327` is unique (count 1). The two `-` lines also occur at `:259`-`:260` (`/revoke`), and the header places the hunk; the checker's A2a anchor check passed.

## Measured (scratch clones at 215cc687; vitest from the farmed tree; node 24.7.0)

| step | result |
|---|---|
| `git apply --check` / `patch -p1 -F0 --dry-run` in a fresh clone at the tip | rc 0 / rc 0; the applied files are `cmp`-identical to the measured files |
| test hunk ALONE at the tip (RED) | **2 failed / 7 passed / 9**: exactly `RED KS-1371 U1` and `U2`, by ASSERTION (`expected [ 200, null, false ] to deeply equal [ 400, 'BAD_REQUEST', true ]`) |
| golden applied (GREEN) | **9 / 9** |
| vc-issuer suite | tip **16 files / 146 passed / 0 failed**; golden **16 files / 150 passed / 0 failed** |
| `tsc --noEmit -p services/vc-issuer` | rc 0 at the tip and with the golden (the config excludes tests) |
| eslint (run from `Blockchain/Dev`) on both files with the golden | rc 0. Control: `var` + `debugger` planted in the test file gave rc 1 |
| **real Ornith checker** (`tasks/code_patch/checker.sh`, golden as model output, fresh clone + `prepare_clone.sh`) | **RESULT: PASS (7/7)**: A2 strict, A3 the 2 files, A3c 17/17, A4 2 failed / 9 with assertion reds and controls green, A5 9/9, A6 no new red, A7 tsc rc 0 |
| **real Spark checker** (`spark_checker.sh`, same way) | **SPARK RESULT: PASS**: 7/7 + A2a anchor 2/2 hunks ok |

**Arms** (the golden test against a variant `status.ts`; the fixed file was restored and `cmp`-checked after):

| arm | result |
|---|---|
| `:329` back to the tip's `!Number.isInteger(...)` only | 2 failed / 9: U1 and U2 |
| `< 0` → `<= 0` | 1 failed / 9: the control `index 0 still unrevokes` |
| the `|| req.body.index < 0` clause also pasted into `/revoke` (`:259`) | 1 failed / 9: the control `revoke still admits index -1` |

## build_input: rc 0
```
NIGHT_BRIEFS_DIR=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1371 bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/build_input.sh KS-1371 <out>/input.json product=Blockchain/Dev/services/vc-issuer/src/routes/status.ts ref=Blockchain/Dev/services/vc-issuer/src/__tests__/ks1269-status-revoke-refuses-a-non-integer-index.test.ts test_file=Blockchain/Dev/services/vc-issuer/src/__tests__/ks1269-status-unrevoke-refuses-a-non-integer-index.test.ts line=328 ctx=49152
```
The output, verbatim except the last line's scratch path:
```
ticket KS-1371 · Todo (unstarted) · High · assignee=kamil.kreiser@secuura.ai · updated 2026-09-28T16:23:07.876Z
product file PINNED: services/vc-issuer/src/routes/status.ts (ticket names 0: [])
fix shape: WEDNESDAY BRIEF (KS-1371.md) — the ticket's fix-shape/decision gates are bypassed; the brief states the change and any decision → 'The exact change'
product services/vc-issuer/src/routes/status.ts (14470 B, 415 lines) defect line 328 [pinned (line=)]: 'if (req.body.index !== undefined && !Number.isInteger(req.body.index)) {'
reference test PINNED: Blockchain/Dev/services/vc-issuer/src/__tests__/ks1269-status-revoke-refuses-a-non-integer-index.test.ts
test_file PINNED (modify in place): Blockchain/Dev/services/vc-issuer/src/__tests__/ks1269-status-unrevoke-refuses-a-non-integer-index.test.ts (3409 B) — suggested_test_file = it
  named sites: no '## Where' section — checklist empty (A3b passes vacuously)
  expected '+' lines from the brief's edit blocks: 17 (A3c)
  red cells declared by the brief: 2 ['RED KS-1371 U1', 'RED KS-1371 U2']
  prompt source: WEDNESDAY BRIEF /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1371/KS-1371.md (14351 chars) — the ticket description is NOT the prompt
  suggested_test_file = the brief's `## The test` File: line Blockchain/Dev/services/vc-issuer/src/__tests__/ks1269-status-unrevoke-refuses-a-non-integer-index.test.ts (== the title slug)
contract: key set == KS-871 input (top-level, ticket, repo)
wrote <scratch>/bi1371/input.json (43807 B; ~10939 prompt tokens at 4 B/token — num_ctx 49152 leaves ~38213 for the answer)
```
The ref pin is the `/revoke` KS-1269 test (read-only), so the reference is never the file being modified.

## The round command (NOT run)
Build the input where night inputs live, then queue one line (Ornith, `night_run.sh`):
```
NIGHT_BRIEFS_DIR=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1371 bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/build_input.sh KS-1371 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/inputs/code_1371_brief.json product=Blockchain/Dev/services/vc-issuer/src/routes/status.ts ref=Blockchain/Dev/services/vc-issuer/src/__tests__/ks1269-status-revoke-refuses-a-non-integer-index.test.ts test_file=Blockchain/Dev/services/vc-issuer/src/__tests__/ks1269-status-unrevoke-refuses-a-non-integer-index.test.ts line=328 ctx=49152
```
queue.md line:
```
KS-1371 input=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/inputs/code_1371_brief.json task=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/tasks/code_patch/task.md ctx=49152
```
A copy of the input this drafter built (rc 0) is at `scratchpad/screen0929/bi1371/input.json` in session `407373b1…`, until that scratchpad is cleaned.
**Round counter:** 0 rows in `night/done.md`, no `READY_KS-1371*`, no earlier brief. This is round 1, with one rebrief allowed; after that it goes to the cloud.

## UNMEASURED / doubts for Wednesday
1. **The ticket offers two options, and this brief takes one.** KS-1371 says: "validate `index` against its declared bounds before the write ..., or widen the ruling deliberately". The brief takes the first, which is what the standing KS-662 ruling (unrevoke tolerates only a non-string `reason`; `unrevoke {index:-1}` is listed as NON-RULED) and the schema (`nonnegative()`) already say. Peter's 09-28 KS-1269 comment says "your view decides it" to Kam. **If Kam wants the ruling widened instead, do not run this round.**
2. **The KS-1269 test file is edited.** KS-1269 is In Progress (#1071 merged, not deployed). The append changes no KS-1269 cell. Whether a reviewer prefers a separate `ks1371-*.test.ts` is a raise-time taste call; the same cells in a new file were measured green too.
3. **No live stack.** The sweep's 200 on a placeholder `credentialId` is the reporter's observation, not reproduced here.
4. **No Ornith or Spark model round** was run. Both checkers were run on the golden only.
5. **The open-PR list comes from `ls-remote` merge refs** plus the fetched heads of all 22 (06:13 AEST), not the GitHub files API. A PR with no merge ref would be missed.
6. **`PAUSE_QUEUE`** (paused until 06:00 2026-09-29) and the G2 foreign-pane gate (refusing all night per `night/log/night_2026-09-29.log`) are Wednesday's to clear. Neither was touched.
