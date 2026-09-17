# NEXT SEARCH 2026-09-17i (13:33–13:46 AEST): 17g's wording refusals, measured

**BLUF: ONE FIT, KS-944. It is test-only: one new services/auth vitest file pins the `security:` value of all six wallet operations in `auth.openapi.ts`. The api-gateway reads those values to decide which routes need a bearer.** Today, flipping `/api/auth/wallet/authenticate` to bearerAuth leaves the whole auth suite green (751/751, measured). **The real `checker.sh` (sha256 `f3ce186c…`) gave RESULT: PASS (7/7), mode test_only, strict,** on both the draft input (fin0) and the placed input (fin1), at develop `d7e95cd9f`. Two wrong variants failed at named gates: `FAIL A4 RED-FIRST` and `FAIL A3 (test-only)`. Nothing was queued.
- **Why 17g's refusal doesn't hold:** 17g's refusal ("partition + decisions") came from the ticket's *mechanism* prose, which names the gateway's index.ts, proxy.ts and specRouteMap.ts. The ticket's actual fix shape is one cell over the spec source. That source is `services/auth/src/auth.openapi.ts`: not partitioned, 0 open PRs, 0 READYs. The ticket has 0 comments and nothing to decide.
- **Two board closes found:** KS-810 and KS-793 are already done at the tip.
- **No second fit:** every other wording refusal still stands after measurement. Tip read and comments read; table below.

## Wednesday must read before queuing
1. **Prompt size.** The builder includes the whole product file, and `auth.openapi.ts` is 139 KB. The input comes to about 43K prompt tokens at ctx 65536, leaving about 22K for the answer (the builder did not warn). By bytes it is the largest of the 64 inputs (172.8 KB). The nearest precedent, `code_730B.json` at 154 KB, got PASS 7/7 at ctx 65536 (done.md, 05:55). The answer itself is 57 lines.
2. **Closes vs Refs.** The brief reads it as Closes: the cell and the red-proof are exactly what the ticket asks for. Put the contrast in the PR body: the A4 line, plus 751/751 green under the tamper without the file.
3. **Not measured:**
   - **`ks570`:** it is a gateway test, so the checker doesn't run it. No gateway src file imports `auth.openapi`.
   - **The yaml:** the cell pins the Zod source, while the gateway enforces the generated yaml. A hand edit to the yaml alone is caught only by preflight step 1, `check:openapi` (I read that step but did not run it). The yaml matches the source today (yaml parse).

## FOUND
- **Scope:** the 41 text-screened rows in 17g, re-pulled from Linear with comments (13:35:23). Every cited site was read at the tip.
- **KS-944 FITS.**
  - Record: Backlog, Medium (P3), assignee and creator Kam, 0 attachments, 0 comments, 0 relations.
  - Fix shape (from the ticket): "A cell over the spec source asserting the four operations declare `security: []` and the two authenticated ones declare `bearerAuth` — a table … Pair it with the reverse assertion".
  - Red-proof (from the ticket): flip authenticate.

## TESTED (KS-944)
- **Clone:** `/private/tmp/claude-501/night/s17i/clone`: clone.sh at 13:33:41, checkout.sh at 13:33:42, prepare_clone.sh rc 0 at 13:34:29. Every run was under `sandbox-exec nonet.sb`.
- **The gap:** the whole suite without the new file, under the tamper, gave 62 files and 751/751 green, tsc rc 0 (13:39:11–20).
  - Positive control: a module-scope throw on `:1829` turns s130-f6 red, 749/751 (13:39:27–33).
- **New test at the tip:** 3/3 passed (13:38:35).
  - **Under the checker's tamper:** R1 fails by assertion, and CONTROL and COMPLETENESS stay green (13:38:38).
  - **Other variants:**
    - link opened: R1 and CONTROL red;
    - status `security:` line deleted: R1 red;
    - challenge closed: R1 red;
    - INERT comment: 3/3 green;
    - completeness arm: `expected +0 to be 2`.
- **Test file:** 57 lines. 0 non-ASCII characters, 0 backslashes, 0 `$`, 0 backticks, 0 double quotes, 0 quote characters in comments. The fence equals the golden file. The path equals `suggested_test_file`. The brief states every line's indentation in prose.
- **Real checker** (sha256 `f3ce186cf515626f07d324a7df2218304f058a2b03fb26b9f68ec2c40813b53d`, identical before and after every run). fin1 ran on the placed input, 13:44:37–52, rc 0, verbatim:
```
mode: test_only (tamper at Blockchain/Dev/services/auth/src/auth.openapi.ts:1829)
PASS A1 output is exactly one fenced ```diff block, nothing outside it
baseline suite rc=0 total=751 passed=751 failed=0 suites_failed=0 loaded=1 failed_names=[]
baseline tsc rc=0 (0 lines)
PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)
PASS A3 (test-only) touched-file set == { Blockchain/Dev/services/auth/src/__tests__/ks944-the-gateway-s-auth-gate-reads.test.ts } — the product file is untouched, as the ticket requires
A3b: no must_change sites in the input — skipped
INFO A3i skipped — the input carries no expected '+' lines (a legacy or brief-less input); indentation not measured
PASS A4 RED-FIRST: src/__tests__/ks944-the-gateway-s-auth-gate-reads.test.ts fails at the untouched tip (1 failed / 3 run; controls green; assertion reds)
PASS A5 GREEN-AFTER: src/__tests__/ks944-the-gateway-s-auth-gate-reads.test.ts passes with the product hunk (3 passed / 3 run)
after suite rc=0 total=754 passed=754 failed=0 suites_failed=0 loaded=1 failed_names=[]
NEW reds: []
PASS A6 whole services/auth suite: no NEW red vs the untouched tip
PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)
SUMMARY files=1 +57/-0 test=src/__tests__/ks944-the-gateway-s-auth-gate-reads.test.ts red_first=yes apply_mode=strict
RESULT: PASS (7/7)
```
  fin0 (draft input, 13:41:29–46) printed the same lines.
  - **wrong_blind** (R1 swapped for a link/unlink count): placed input 13:44:52–13:45:08, draft input 13:41:51–13:42:10:
```
FAIL A4 RED-FIRST: the test file is NOT red at the untouched tip (rc=0, 0 failed / 3 run) — it does not prove the defect
RESULT: FAIL (1 failed)
```
  - **wrong_product** (the golden file plus a hunk on auth.openapi.ts): placed input 13:45:08–15, draft input 13:42:10–17:
```
FAIL A3 (test-only) touched-file set must be exactly ONE new test under Blockchain/Dev/services/auth/src/__tests__ and NOTHING else: n=2 product=1 tests=1 other=0
RESULT: FAIL (1 failed) — stopped at A3 (test-only mode: the product file must not change)
```
- **NOT tested:**
  - the model run and the raise;
  - the gateway suite (`ks570`) and a live gateway;
  - the preflight drift step;
  - the rows marked "read" in the table.

## HOW (partition)
- **Linear:** GraphQL reads only, key sourced inside Python and never printed, no Bearer prefix, `first:` only. Pool at 13:33:48: 328 tickets, 7 pages, hasNextPage false. 41 full records at 13:35:23.
- **Open PRs:** GitHub REST GET at 13:34:12, 20 PRs / 102 paths. 0 name `auth.openapi.ts`, `specRouteMap` or a ks944 path; control: 2 name `services/auth/src`.
- **Seat A heads:** `diff --name-only` only, 13:33:43. 15 paths, none `auth.openapi.ts`.
- **Held partitions:** none touched.
- **READYs:** 114. 0 have a `+++ b/` on `auth.openapi.ts`; control: 14 under `services/auth/`.
- **queue.md:** 0 lines mention KS-944 (control: 77 lines carry `KS-`). **done.md:** 0.
- **Source porcelain** (`--untracked-files=no`): 0 at 13:42:29 and 13:46:42. Control: the clone with a file edited gave 1, then 0 after restore. No git write verb was run against `!CODING`.

## Tip
`d7e95cd9f153e9036ed77935a73c93504fa6e3dc`, read with `git ls-remote <source origin URL> refs/heads/develop` from the scratch clone (using the source's `core.sshCommand`) at 13:33:41, 13:42:29 and 13:45:55. It did not move, and the input records the same tip.

## Files
| file | sha256 | note |
|---|---|---|
| `night/briefs/KS-944.md` | `c5a8f161904aaca9181dc745bfcac5e8a4230f82d81dffc43b42c0921e73b8d5` | 220 lines, 0 non-ASCII, 0 backslashes. Contains `## Red cells`, `## Tamper` (line 1829, statement_ok), `## Premises (measured)` P1–P11 and `## Notes for the raise`. |
| `night/inputs/code_944.json` | `fb92a4686c402e6a09b369f9b7ceef5fb9092926038a3f8facf6831565232616` | `build_input.sh` rc 0 at 13:44:29. Test-only tamper at `:1829`, 6 Where sites (0 must_change), 1 red cell, about 43.3K tokens at ctx 65536. |
| golden test / out.md | `3059d279…` / `bc36dbd1…` | `s17i/golden.test.ts`, `s17i/golden.out.md` |
| `night/candidates.md` | `8161b3115a104c5e…` | SEARCH 17i block appended inside an HTML comment by `.new` + `mv` at 13:46:36, after a re-read showed the base sha unchanged (`1050a963…`). Backup: `candidates.md.pre-1346-search17i`. Backticks: 278 before and after. |

**Queue line (NOT added):**
```
KS-944 input=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/inputs/code_944.json task=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/tasks/code_patch/task.md ctx=65536
```
**Rebuild pins:** `product=Blockchain/Dev/services/auth/src/auth.openapi.ts ref=services/auth/src/__tests__/s130-f6-openapi-module-in-the-import-graph.test.ts line=1829 ctx=65536`

## Rejections (the rows are in candidates.md SEARCH 17i)
| ticket | verdict | measured reason |
|---|---|---|
| **KS-944** | **FITS (briefed)** | See above. |
| KS-810 | BOARD CLOSE | Already fixed at the tip: `passwordLoginGate.ts` imports `z` from `@secuura/shared` (#822), and the s130-f6 test is the regression import. Stale comments remain at `auth.openapi.ts:1-21` and `ks796-f6…test.ts:118`. |
| KS-793 | BOARD CLOSE | Root `BACKLOG.md:122` already records the old headline as wrong. |
| KS-839 | STANDS | `oauth.ts:353` wildcard is present. Needs a ruling plus a spec statement (the yaml mentions wildcard 0 times; control: allowedScopes 19). |
| KS-855 | STANDS | The divergence is live (`oauth.ts:57-66` vs `scopes.ts:135`). Derive-vs-pin is unpicked. |
| KS-824 | STANDS | The fold-case fix touches 5 sites in 2 files, or it is a migration. The ticket says to measure before choosing. |
| KS-1107 | STANDS | Dropping the field changes the published register schema (`auth.openapi.ts:879`): multi-file. The other option is a feature, and the ticket asks for a consumer trace first. |
| KS-1152 | STANDS | R1 alone spans 5 files in 3 packages; the ticket holds 10 records plus a Kam line. |
| KS-1157 | STANDS | Kam ruled marker-only, but it is a multi-file feature. |
| 32 others | STAND (17g) | Comments read (KS-756, KS-1032, KS-1003, KS-977, KS-1053, KS-1017, KS-955, KS-724, KS-1091, KS-925, KS-1149, KS-836, KS-986, KS-668); none rules a single-file vitest shape. Decision, non-vitest or partitioned: KS-782, KS-834, KS-1177, KS-915, KS-840, KS-1168, KS-1124, KS-787, KS-619, KS-1038, KS-618, KS-918, KS-1105, KS-951, KS-1146. Excluded by owner: KS-329, KS-1015, KS-759. |

## Deviations
- **Hand-assembled brief:** built with `s17i/assemble.py`, not `new_brief.sh` (same as KS-623, KS-1009 and KS-1156).
- **The brief was placed three times.**
  - v1 and v2 were moved to `s17i/quarantine/placed_v1` and `placed_v2` after note edits.
  - The v2 note was about prompt size and precedent, and it is the text now in the brief.
  - The brief quotes the v2 input's byte count (172.6 KB); the final input is 172.8 KB.
  - fin1 and both wrong runs used the final input.
- **No `cd`, no `rm`.** Premeasure copies went to `s17i/quarantine/`, and `auth.openapi.ts` was restored after each run (`cmp` rc 0). At the end: clone porcelain 0, no processes left. Load 3.97 at 13:46.
