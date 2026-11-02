# QA Gate 140 verdict: Secuura/Distributed_Secuura PR 1953 (Refs KS-1725: zod 3 -> zod 4.6.7 behind a zod 3 issue layer), DELTA of gate 135, round 2 of 2, TIER 1

## BLUF
**GO WITH NOTES. Nothing is FIX-BEFORE-MERGE.** Gate 135's four FIX-BEFORE-MERGE classes (F1-F4) are **CLOSED** at head `928ee20c`. I re-measured that with my own runs, not the author's cells:
- The corpus over the whole product: F1 0, F2 0, F3 0, F4 0. F4 was made evaluable this round, and a control fires 112 cells.
- The real shared middleware (`validateBody` -> `errorHandler`, 422) and `validation.validateBody` (400): 46 cases on both envelopes, every F1-F4 row EQUAL to real zod 3.25.76.
- I regenerated **all 45** golden cases myself from real zod 3.25.76: 45/45 byte-equal. Control: on zod 4 they give 0/45.
- F6 is closed too: gate 135's surviving mutant (users.ts `.guid` -> `.uuid`) is now killed by the new auth route test.

Other results:
- **Merges:** both merges of develop are clean auto-merges (merge-tree = committed tree).
- **Rule 4:** `check:openapi` rc 0. The yaml is byte-identical to a fresh regeneration, and a planted one-word drift gives rc 1.
- **merge-tree onto current develop:** clean, exactly the PR's 150 paths.
- **Logging:** no new log line.

Two survivors carry real meaning, but neither can be reached in product code today, so both are notes (G140-F2, G140-F5).

## Heads
- START (logs/head_start.log, 2026-11-02T17:36:49Z): PR `928ee20c84dce74930422176e17c962b1ed85bde` (matches the author's), develop `2d3b3bb3d3865689e3cad843f9ebb90a2f606960` (matches).
- END (logs/head_end.log, 18:03:59Z): both **unchanged**.
- Gate 135's head `ea6d924e` is an ancestor (rc 0). First-parent commits since then: `a6e0fb3c` (the fix), `25523f25` (merge of develop `8151e756`), `473ef1e0` (comment date only: one test-comment line, 2026-11-03 -> 2026-11-02), `928ee20c` (merge of develop `2d3b3bb3`, PR 1955).
- PR body not read live (no PAT). The author's READY mail is in evidence/s14_ready.txt.
- Node v26.8.1. **Nothing was measured on Node 24.**

## FINDINGS
- **G140-F1 (info; measured) G135-F1..F4 CLOSED; F5 disclosed; F6 CLOSED.**
  - F1 (`zod3Datetime` :400): the error function returns the message only on `invalid_format`.
  - F2 (:310) and F3 (:322) run in `zod3Issues` (:344), F2 first, and again in every union branch (MF3d kills that).
  - F4 (`zod3NativeEnum` :237, mark :241, rule :175) is used at all 9 request sites. NaN stays invalid_type (equal to zod 3, driver `F4_raw_NaN`), and a non-NaN number becomes invalid_enum_value.
  - No raw `z.nativeEnum(` remains in product code, except the spec-only `vc-issuer.openapi.ts` (2) and the helper itself.
- **G140-F2 (recommended; measured) Survivor MF2b: the F2 `.int()` exclusion is not pinned by any cell.**
  - Removing `&& i.expected !== 'integer'` leaves 268/268 green.
  - It is load-bearing: `z.number().min(5).int()` given 1.5 is EQUAL to zod 3 at the head (too_small + invalid_type integer), and without the exclusion the too_small would be dropped (logs/probe_int_order.log).
  - Product reach today: **0**. Census: 0 number checks declared BEFORE `.int()` in product code; control: 136 `.int().<check>` sites.
  - Fix (non-blocking): add one golden case, `z.number().min(5).int()` given 1.5, frozen from zod 3.25.76.
- **G140-F3 (info; reasoned) Equivalent survivors.**
  - MF3c (pass order swapped): commutative. A type-failed path has no element issues, so F3 never moves an issue that F2 drops.
  - MF3b (F3 also moves non-array length issues): a string or number has no child paths.
  - MF4c (the helper's error function returns undefined): the mark stays on the raw issue and the installed global map applies the same rule.
  - MF3e (strictlyUnder admits the same path) differs only for an array with two failing length checks on the same side; see F4.
- **G140-F4 (info; measured) A class gate 135 did not list, product reach 0.**
  - zod 3 kept only the LAST `.min`/`.nonempty` (or `.max`) on an array, because it stores one value. zod 4 reports both.
  - Example: `z.array(z.string()).min(1).min(3)` given `[]`: zod 3 gives 1 issue, head gives 2 (probe_int_order.log `two_len_checks`).
  - Census: 0 product arrays with two same-side length checks. The corpus shows 0 such cells.
  - This was already in the PR at gate 135; it is not a delta regression. List it in the PR body for completeness.
- **G140-F5 (recommended; measured) The F4 sites are pinned by source TEXT only.**
  - MF4e (`nft.routes.ts:34` back to raw `z.nativeEnum`) leaves nft-certificate 200/200 green. MF4f (`credentials.ts:39`) leaves vc-issuer 714/714 green.
  - Both are killed only by block K's AST census cell (helper count 9): a real CI kill, but not a behaviour kill.
  - My corpus does run the real site schemas: 0 F4 cells with the helper, 112 with raw `z.nativeEnum`.
  - Fix (non-blocking): one route-level cell, e.g. POST /mint with `storageTier: 1`, asserting zod 3's invalid_enum_value body.
- **G140-F6 (info; measured) Gate 135 was wrong that "a `.trim()` chain is immune". The author is right that it was an input artefact.**
  - Gate 135's case `['a','b','c','d']` sat inside `.min(3).max(200)`.
  - `string.trim().min(8)` given `[]` is RED at the unfixed product (red-first list) and EQUAL to zod 3 at the head (driver `F2_trim_min_given_empty_array`, `F2_trim_min_given_long_array`).
- **G140-F7 (info; measured) The author's F2-limit disclosure is accurate, and the limit cannot be reached today.**
  - Census (logs/census_f2_limit.log), case-insensitive, product code:
    - 0 `z.intersection(`. The one `.and(` hit is the compat file's own comment.
    - 0 `too_small`/`too_big` and 0 `invalid_type` issue-code literals.
    - 8 `addIssue`: 3 are `ZodIssueCode.custom` in anchorSchema.ts, and 5 are a non-zod `SecurityIssue` class in services/shared audit.ts.
    - 0 `.merge(`, 0 `z.preprocess(`. The one zod `.pipe(` is after string transforms in oauth.ts:1225.
  - Controls: `z.union(` 9, `.superRefine(` 2.
  - Keep the disclosure in the PR body.
- **G140-F8 (info; measured) Reds that are not this PR's.**
  - anchoring threadTokenMint (KS-562): 776/777 at the head AND on develop alone (same cell).
  - packages/shared wallet-signature (KS-1727): 1446/1447 at the head; red on develop alone (4/5). The intermittent threadToken "different policy IDs" cell the author saw was green in this run.
  - auth ks949: 3 cells time out at 5 s when run alone, identically at the head and on develop (1 of them in the whole-suite run, 1550/1551). That is environment, as at gate 135.
- **G140-F9 (info; measured) Lint.**
  - Changed files: 0 errors. One warning, `cases-g135.ts:37` unused eslint-disable, the same as the existing `cases.ts:27`.
  - nft-certificate, vc-issuer and auth lint: rc 0.
  - packages/shared lint has 1 error at `middleware/index.ts:543` (no-control-regex). It is pre-existing on develop (:541), and the PR's hunk in that file is only the zod3Issues wrap.

## Q1. Heads + diffstat (logs/merge_tree.log, fix_diffstat.log, paths.txt)
- Three-dot vs develop `2d3b3bb3`: **150 files, +4661/-524**, as claimed.
- Against gate 135's 146: +4 new paths (cases-g135.ts, golden-g135.json, the auth route test, vc-issuer credentials.ts), 0 dropped.
- Paths whose PR diff changed since gate 135: zod3-compat.ts, the compat test, nft.routes.ts and the two KS-1725 fragments.
- The fix commit `a6e0fb3c` is 9 files, +606/-16, as claimed.

## Q2. The fix hunks (logs/fix_product.diff)
- `zod3-compat.ts`: `zod3NativeEnum`, the `nativeNumber` rule in `zod3Annotate`'s enum branch, `dropLengthAfterTypeFailure`, `arrayLengthFirst`, `zod3Issues` composing them, and the `zod3Datetime` error function.
- nft.routes.ts: 7 sites. credentials.ts: 2 sites plus the import.
- Acceptance and the OpenAPI output do not change: same ZodEnum def and entries (the K cell), and the yaml regenerates byte-identical.
- No envelope, status code or message construction changed.

## Q3. Behaviour (run, not read)
- **Corpus** (gate 135's corpus_side.cjs, re-pointed; changes marked G140; logs/corpus_*):
  - Base is MY develop worktree `2d3b3bb3` (zod 3.25.76, raw issues). Head is the real dist compat module plus the real `zod3Issues`.
  - The pairmap is **equal to gate 135's** (951/951 keys).
  - Plain run (gate 135's method), 294,503 cells, product classes:

    | class | cells |
    |---|---|
    | safe-int bound (F7a) | 132 |
    | int stops the chain (T3) | 54 |
    | not_finite (F7b) | 39 |
    | safe-int refused (T1) | 22 |
    | coerce Infinity refused (T2) | 9 |
    | F5 | 6 |
    | REJ->ACC | **0** |
    | **F1 / F2 / F3** | **0** |
    | other | 0 |

    That equals the author's before/after table and gate 135's in-process projection.
  - `G140_ENUMS=1` (enums imported by the request files resolved, so the 9 F4 sites are evaluated): 299,401 cells, 8 more expressions. Product classes are the same accepted set, and **F4 = 0**.
  - Control `G140_RAWNE=1` (helper replaced by raw `z.nativeEnum`): **F4 = 112 cells** at nft.routes.ts :30/:40/:47/:652 and credentials.ts :35. So the corpus sees F4, and the helper closes it.
- **Real middleware** (scripts/driver140.cjs; logs/driver140_cmp.txt): 46 cases x 2 envelopes plus 3 raw.
  - EQUAL: F1 on missing/null/number/bool/array/object/bad format/empty/ok, and the message-less form.
  - EQUAL: F2 (string with min, length or trim given arrays; arrays with min/length given strings).
  - EQUAL: F3 (simple, nested, siblings) and F2xF3 in a union.
  - EQUAL: F4 on number, 0, float, optional, numeric and mixed enums, keys vs values, bool, null, missing, array, and NaN/Infinity raw.
  - The only DIFFs are accepted ones: int stops the chain (T3), F5, and the safe-int tightening (T1).
  - Control with raw `z.nativeEnum`: 20 DIFF rows (all number inputs, plus Infinity).
- **Golden provenance (B)** (scripts/golden_regen.cjs): I transpiled the head's `cases-g135.ts` and built every case with zod 3.25.76 from my develop worktree.
  - **45/45 byte-equal** to golden-g135.json; the earlier golden.json is 66/66.
  - Control with zod 4.6.7: 0/45 and 1/66.
  - The author's generator script is not in the repo (only its output). I verified the output, not the script.

## Q4. Re-measure
- New cells at the head:
  - compat test 268/268 (logs/t_head_compat.log; run with `npm --prefix`, because the test locates the Dev root from cwd);
  - auth ks1725-guid-acceptance-patch-route 15/15.
- **Red-first** (product files zod3-compat.ts, nft.routes.ts, credentials.ts at `ea6d924e`, tests at the head; logs/redfirst.log): **33/268 red, every one an AssertionError**. 30 are golden cells (F1 8, F2 9, F3 6, F2xF3 2, F4 5; every control case stayed green), plus the errorHandler cell, the helper cell and the site census.
  - The auth route test is 15/15 at both, a pin (users.ts unchanged).
- **Merges (D)** (logs/merges.log): `25523f25` = merge-tree(a6e0fb3c, 8151e756), tree 29a451dc, EQUAL. `928ee20c` = merge-tree(473ef1e0, 2d3b3bb3), tree 3e09008f, EQUAL.
  - No path in either merge comes from outside develop's side.
  - anchoring `index.ts` (logs/hunks_anchoring.log), the only file both sides changed. Branch hunks at old lines 13, 69, 302, 604, 908, 943, 1108, 1363; PR 1955's at 699, 1315, 1824. Closest: 1363 vs 1315, **48 lines**, none inside another. Same as the author's.
- Whole suites + tsc (logs/suites/summary.txt; tsc 0 errors in all 10 runs):

  | unit | passed / total | note |
  |---|---|---|
  | anchoring | 776/777 | threadTokenMint, also red on develop alone |
  | packages/shared | 1446/1447 | wallet-signature KS-1727, also red on develop alone |
  | nft-certificate | 200/200 | |
  | vc-issuer | 714/714 | |
  | auth | 1550/1551 | ks949 timeout; also red on develop |
  | originate | 2334/2334 | |
  | governance | 288/288 | |
  | staking | 84/84 | |
  | api-gateway | 1462/1462 | |

- **Rule 4 (E)** (logs/openapi.log):
  - `check:openapi` rc 0 (CHECK PASS, spec-examples pass).
  - `generate-openapi` (real write): sha256 unchanged b76638b1..., 314 paths.
  - Planted " Drift" in info.title: `--check` rc 1 and `check:openapi` rc 1. Restored by bytes, sha256 equal, tree clean, rc 0.
- Docs fragments: `check` OK. A planted unbalanced `</table>` in the flow fragment this round edited gives rc 1 naming it. Restored, sha256 equal, rc 0.

## Q5. Mutants on the fix lines (scripts/mutants.py; logs/mutants.log, mutants.json)
Product only, tests untouched. Each mutant is a one-occurrence (or one-line) replacement. Original bytes are written back, sha256 is asserted, and the tree is clean after each; shared is rebuilt around compat mutants. **All RESTORE_OK.**

| mutant | result |
|---|---|
| MF1a F1 reverted to `{ error: message }` | KILLED 9 |
| MF1b F1 condition inverted | KILLED 12 |
| MF2a F2 pass disabled | KILLED 12 |
| MF2b F2 `.int()` exclusion removed | **SURVIVED** -> G140-F2 |
| MF2c F2 drops too_small only | KILLED 2 |
| MF3a F3 pass disabled | KILLED 9 |
| MF3b F3 moves non-array length issues | survived, equivalent (F3) |
| MF3c pass order swapped | survived, equivalent (F3) |
| MF3d post-passes not in union branches | KILLED 4 |
| MF3e strictlyUnder admits same path | survived, unreachable (F3/F4) |
| MF3f F3 inserts one place late | KILLED 9 |
| MF4a helper does not mark | KILLED 6 |
| MF4b NaN guard removed | KILLED 1 |
| MF4c helper error returns undefined | survived, equivalent (F3) |
| MF4d rule covers every non-string | KILLED 5 |
| MF4e nft.routes.ts:34 raw nativeEnum | killed by the source census only (nft 200/200) -> G140-F5 |
| MF4f credentials.ts:39 raw nativeEnum | killed by the source census only (vc 714/714) -> G140-F5 |
| MF6 users.ts:778 `.guid` -> `.uuid` (gate 135's M3b survivor) | **KILLED 9/15** by the new route test |

## Q6. merge-tree (logs/merge_tree.log)
Onto develop `2d3b3bb3`, which is already in the head: rc 0. The tree `3e09008f` equals the head tree and changes exactly the PR's 150 paths.

## Q7. Logging (ks1346) (logs/logging.log)
- 0 logger/console lines added by the fix commit, and 0 in the whole three-dot PR.
- The 4 log lines in `ea6d924..473ef1e0` arrived from develop (governanceService.ts, PR 1952) and are not this PR's.
- Control: the same grep finds 16 logger lines in nft.routes.ts.

## Notes for the PR body
1. G140-F2, recommended: a golden case `z.number().min(5).int()` given 1.5 (it pins the F2 `.int()` exclusion).
2. G140-F5, recommended: one route-level F4 cell (number into an nft `storageTier`).
3. G140-F4, info: list "an array with two same-side length checks reports both on zod 4 (zod 3 kept the last); 0 product sites".
4. G140-F6/F7, info: gate 135's trim-immunity remark is withdrawn; the F2-limit census is reproduced.
5. G140-F8/F9, info.

**Under the cap: there is no residue to ticket as FIX-BEFORE-MERGE.** F2 and F5 can be follow-up cells after the merge; neither blocks. The fuse: merging retires the 2026-11-09 GHSA-mrhx-c7xc-m3w5 expiry, per gate 135 Q7 (not re-run this round).

## NOT TESTED
- Node 24. A booted service or a real HTTP hop: the shared middleware was run directly, and the auth route test runs a real express route with mocks.
- The four platform suites, image builds, the pre-push hook, the PR body as live on GitHub.
- Audit and lockfile checks were not re-run; the fix commit touches no manifest or lock (9 files listed in Q1).
- Whole suites of the units not listed in Q4.
- The author's golden generator script itself (only its output, regenerated 45/45). The author's planted-conflict control for the 1955 merge (I proved the merge trees equal instead).
- The intermittent threadToken cell (green this run).

Artefacts:
- scripts/, logs/ (suites/ inside), evidence/s14_ready.txt.
- Clone repo/ at `928ee20c`, clean, push URL `no_push_qa_gate`. Worktree repo_base/ at develop `2d3b3bb3`, clean.
- Every runner was anchored with `npm --prefix` / `--root` / absolute driver paths to my trees. Nothing was written outside this workdir, except one yaml backup in the session scratchpad.
- Background runs (install, mutants, suites, two monitors) all exited; `ps` shows no vitest/jest of mine.
