GO WITH NOTES — MERGE (no HOLD-FOR-KAM)
Merge tree on c7abf98e51030f908050fede10a3546871d4f2c1: PR 1798 alone rc 0, tree cd68df214e09d00fd5fed398bb98102e9b5bf066; PR 1796 + PR 1798 together rc 0, tree b97218c515e0efa25f82733177e43cc04e7e89f7 (same tree in either order).

# QA Gate 186 (Tier 1, round 1): PR 1798 / KS-1459 users.ts uses the canonical verification-level order

## Subject
- Pin at START (08:00Z / 19:00 AEDT) and END (08:09Z), `git ls-remote origin` from the read-only checkout:
  - refs/pull/1798/head = 3db8f8c07e7d7693778bc90c155d16cd6a273405 (start = end, = commission)
  - refs/pull/1796/head = 759fd6fb19aaa22df4bd86dd61dcb6d4a9832fa8 (start = end)
  - refs/heads/develop = c7abf98e51030f908050fede10a3546871d4f2c1 (start = end, = commission)
- Base = merge-base(head, develop) = 5c1ca287ed74b6353423a8c09e253abf3129233a. develop c7abf98 changes 10 files since that base, none under services/auth or packages/shared; develop's users.ts is byte-identical to base's (diff empty). So the merged auth tree equals the head's auth tree, and head measurements apply to the merge.
- Diff vs base: 1 file, `Blockchain/Dev/services/auth/src/routes/users.ts`, +14 -8: import of `VERIFICATION_LEVEL_ORDER` (line 13), `const LEVEL_ORDER: readonly string[] = VERIFICATION_LEVEL_ORDER;` (1382) replacing the 5-level literal, and two comments (1375-1381, 1490-1494). Scope matches question 1 exactly.
- Host: macOS, Node v26.8.1 (NOT LTS; Node 24 not run), TypeScript 5.9.3, vitest 4.1.12, express 4.22.3, zod 4.6.7. node_modules APFS-cloned (`cp -c`) from worktree s-r84-1798 (HEAD = 3db8f8c, package-lock sha equal to head's).
- Method: `git clone --shared` into `repo/` (ignored), PR/develop refs fetched there; every runner anchored (`vitest --root`, `tsc -p <abs>`) under `env -i` with HOME/TMPDIR in the workdir; cwd = `cwd/` for the matrix and repo-file runs, cwd = the clone's `services/auth` (inside the workdir) for the whole suite (see G186-F4). The REAL `userRoutes` + `errorHandler` were driven over HTTP on 127.0.0.1 (express app, ephemeral port) with the db/userRepo/authenticate mocks copied verbatim from the repo's own ks1236 test; users.ts swapped per variant (base / head / 9 mutants / 1 tsc control) and restored to head after each run (cmp-verified).

## Findings

### G186-F1 — INFO: head is strictly MORE RESTRICTIVE than base; 0 cells more permissive
- **FOUND**: Of 270 driven cells, 48 differ base->head; all 48 are review-approve cells that base APPROVED (200, level written) and head REFUSES (400 BAD_REQUEST, nothing saved, request stays PENDING). 0 cells where head allows what base refused. 0 differences on the submit route. 0 differing cells have a target the submit zod schema admits (STANDARD/ENHANCED/HIGH/GOVERNMENT). Per caller, the 11 upper-case newly-refused pairs (current > target) are: target NONE with current BASIC, SOCIAL, STANDARD, ENHANCED, HIGH, GOVERNMENT (6); target SOCIAL with current STANDARD, ENHANCED, HIGH, GOVERNMENT (4); target BASIC with current SOCIAL (1). The other 13 per caller are the same pairs with a lower-case stored `none`/`social` (the review route upper-cases). At base each of those 48 cells would have LOWERED the subject's level (e.g. GOVERNMENT -> NONE) on approve: the PR closes that for stored NONE/SOCIAL targets.
- **TESTED**: review approve, SYSTEM_ADMIN and ORG_ADMIN callers, current x target over {NONE, BASIC, SOCIAL, STANDARD, ENHANCED, HIGH, GOVERNMENT, WEIRD, social, none} (200 cells); submit, USER caller, current over the same 10 x target over {STANDARD, ENHANCED, HIGH, GOVERNMENT, NONE, BASIC, SOCIAL} (70 cells). Mocked db/userRepo (not a real database).
- **HOW**: `harness/gate186-matrix.test.ts` via `harness/run_variant.sh`, outputs `runs/{base,head}.json`, compared by `harness/analyze.py` -> `runs/base_vs_head.txt`. Controls in the same action: head->base reports base more permissive in 48 cells (the instrument can fire in that direction); head->head reports 0 differing.

### G186-F2 — LOW: no committed test pins KS-1459; reverting the PR passes the repo's suite
- **FOUND**: The PR adds no test (its ticket comment invokes the escape clause). The repo's ten verification-route test files pass 107/107 at base AND at head, and 7 of 9 ordering mutants survive them, including `drop NONE` and `drop SOCIAL` (each equivalent to partially reverting this PR) and `swap SOCIAL<->STANDARD` (which changes zod-admitted, API-reachable cells: submit SOCIAL->STANDARD refused; review STANDARD over a stored SOCIAL approved). Only the two GOVERNMENT mutants (swap HIGH<->GOVERNMENT, drop GOVERNMENT) go red, on ks1236's "GOVERNMENT over a PENDING HIGH" cell.
- **TESTED**: the ten files named in `harness/run_repo_files.sh` (ks1018 x2, ks1193 x2, ks1194 x3, ks1236, ks1477, ks467), per mutant.
- **HOW**: `runs/repofiles_table.txt`, `runs/repofiles_<variant>.out`. Not merge-blocking: the head is safe per F1 and the gate's own matrix kills 9/9.

### G186-F3 — LOW: the ks1236 test's header and a CONTROL cell name now state a false reason
- **FOUND**: `services/auth/src/__tests__/ks1236-approve-never-lowers-a-subjects-verification-level.test.ts` lines 10-11 still say "a level outside the known order (e.g. SOCIAL, NONE) cannot be compared and approves as before", and its last cell is named "CONTROL KS-1236: a level outside the known order (SOCIAL) cannot be compared and approves as it did before". At head SOCIAL is ranked; the cell (subject SOCIAL, target ENHANCED) still passes only because SOCIAL (2) < ENHANCED (4). The PR corrected the same claim in users.ts but not here; ticket item 2 asks to "fix the comment".
- **TESTED**: read at head; cell passes at head (part of the 107/107).
- **HOW**: file read; matrix row review/SOCIAL/ENHANCED = 200 at head and base.

### G186-F4 — INFO (PRE-EXISTING, harness): whole-suite results and the ks949 flake
- **FOUND**: Run 1 (cwd = `cwd/`, default timeouts): 138/141 files, 1670/1674 tests; ks1009 (file-level: "could not locate the Dev root from <cwd>") and ks1467 (2 cells, ENOENT on `<cwd>/src/services/passwordLoginGate.ts`) read paths relative to `process.cwd()` and cannot pass from any cwd but the package dir; ks949 2 cells "Test timed out in 5000ms". Run 2 (cwd = clone's services/auth, inside the workdir): 140/141 files, 1685/1687, the only failures the same 2 ks949 timeouts. ks949 ALONE at head: 31/31 in 1.36 s. Run 3 head `--testTimeout=60000`: 141/141 files, 1687/1687. Base users.ts `--testTimeout=60000`: 141/141, 1687/1687. The ks949 cells walk the repository tree; the timeouts are load timing, not this PR (the PR changes no file ks949 reads beyond the tree it walks, and it passes alone and under a longer budget).
- **TESTED**: whole `services/auth` unit suite (vitest.config.ts), not the integration config.
- **HOW**: `harness/run_suite.sh`, `runs/suite_{head_run1,head_run2,head_ks949_alone,head_run3_t60k,base_t60k}.out`. Wednesday's `logs/combined.log` mtime 17:46 before and after (not written); `cwd/` empty after.

### G186-F5 — INFO: the "canonical" order used is the auth service's copy, not the shared package's
- **FOUND**: KS-1459 item 2 names `packages/shared/src/verification/policy-engine.ts` VERIFICATION_LEVEL_ORDER as canonical; the PR imports `services/auth/src/types/index.ts` VERIFICATION_LEVEL_ORDER (narrowed by the coordinator's ruling, recorded in the PR's ticket comment 6f661672, with the shared-unification half left open). Both arrays are value-identical at head: NONE, BASIC, SOCIAL, STANDARD, ENHANCED, HIGH, GOVERNMENT. `LEVEL_ORDER` is now an alias of that same array object, typed `readonly string[]`; users.ts only calls `.indexOf` on it (no mutation path; tsc would refuse one).
- **TESTED**: `git show` of both files at head; `git grep LEVEL_ORDER` at head.
- **HOW**: read.

## What passed (measured)
- Q1 scope: 1 file, 2 code hunks (import line 13; LEVEL_ORDER line 1382) + 2 comment hunks. Matches.
- Q2 ticket intent + ranking table (ticket read via Linear API, key sourced in-process, never printed; KS-1459 In Progress, 2 comments read in full). Index per level, base -> head: NONE -1 -> 0; BASIC 0 -> 1; SOCIAL -1 -> 2; STANDARD 1 -> 3; ENHANCED 2 -> 4; HIGH 3 -> 5; GOVERNMENT 4 -> 6; unknown -1 -> -1. Pair table (21 unordered pairs of the 7 levels): base orders only the 10 pairs among BASIC/STANDARD/ENHANCED/HIGH/GOVERNMENT, head orders all 21; the 10 base-ordered pairs keep the same relative order at head (0 flips); the 11 pairs involving NONE or SOCIAL go from "incomparable" (-1, both routes treat as allowed) to ranked exactly as the canonical order NONE < BASIC < SOCIAL < STANDARD < ... which is what the ticket asks. No level is ranked higher relative to any other than at base in a way that grants more: driven count of head-more-permissive cells = 0 (F1). HOLD-FOR-KAM condition NOT met.
- Q3 callers at head (`git grep LEVEL_ORDER` over services/auth/src and packages): users.ts 1382 (constant), 1391-1392 (submit, refuse if targetIndex <= currentIndex), 1496-1497 (review, refuse if targetIndex !== -1 && currentIndex > targetIndex). Untouched readers of the canonical constant: middleware/authenticate.ts 206-207; services/account-recovery.ts 63 holds its own identical array. Only writer of `verification_upgrade_requests` is `saveVerificationRequest` (users.ts 1261), called from submit (1428, zod-limited target) and from review (1510/1551/1576, copies of the stored row) — R84's reachability claim holds in code. Matrix: 270 cells, 48 differ, all more restrictive, 0 more permissive, 0 reachable through the submit schema.
- Q4 mutants (gate matrix vs head, raw table `runs/mutants_table.txt`): 9 run, 9 killed, 0 survivors.
  | mutant | differing | more permissive | more restrictive | zod-admitted-target cells |
  |---|---|---|---|---|
  | m1 swap SOCIAL<->STANDARD | 9 | 4 | 5 | 5 |
  | m2 swap NONE<->BASIC | 8 | 4 | 4 | 0 |
  | m3 swap BASIC<->SOCIAL | 8 | 4 | 4 | 0 |
  | m4 swap HIGH<->GOVERNMENT | 6 | 3 | 3 | 6 |
  | m5 drop NONE | 28 | 28 | 0 | 0 |
  | m6 drop SOCIAL | 28 | 28 | 0 | 0 |
  | m7 drop GOVERNMENT | 28 | 19 | 9 | 18 |
  | m8 drop BASIC | 16 | 16 | 0 | 0 |
  | m9 swap STANDARD<->ENHANCED | 6 | 3 | 3 | 6 |
  Counted from the table: 9 rows, every "differing" > 0. Against the repo's own ten files: 2 killed (m4, m7), 7 survive (F2) — none equivalent (each changes driven cells).
- Q5 suites: see F4. Final: head 141/141 files, 1687/1687 at --testTimeout=60000; at default timeouts only the 2 pre-existing ks949 timeout cells fail, and ks949 alone passes 31/31. `tsc -p services/auth/tsconfig.json --noEmit`: head rc 0 / 0 errors, base rc 0 / 0; control (the plain `const LEVEL_ORDER = VERIFICATION_LEVEL_ORDER;`) rc 2 with exactly the two TS2345 at users.ts 1496/1497 the author reported, so tsc does examine users.ts.
- Q6 merge (in the gate clone, `harness/merge_tree.sh`, `runs/merge_tree.txt`): 1798 onto c7abf98 rc 0, tree cd68df214e09 (its users.ts == head's users.ts byte-for-byte; only users.ts differs from develop); 1796 onto c7abf98 rc 0, tree c316ecfd5296; 1798 onto (develop+1796) rc 0 and 1796 onto (develop+1798) rc 0, both tree b97218c515e0efa25f82733177e43cc04e7e89f7 (order-independent); in that combined tree the 1798 LEVEL_ORDER line is present (1) and 1796's 3 added users.ts lines are present (3/3). 1796's only users.ts hunk is @@ -1174,8 +1174,9 @@ (comments in /me/mfa/disable), disjoint from 1798's — R84's claim verified. Control: a planted develop-child editing the same LEVEL_ORDER line -> merge-tree rc 1, 1 CONFLICT line.
- R84 READY section verified: head SHA, base, 1-file scope, the two index moves (NONE -1->0, SOCIAL -1->2), the call-site lines, the zod limit at users.ts 160, the merge-tree claim, and "suite 141/1687 passes with ks949 timeouts as a load flake" all reproduced. Not reproduced: R84's claim that ks949 FAILS on a base tree (my base run used --testTimeout=60000 and passed).

## NOT tested
- No real PostgreSQL: db and userRepo were mocked (the repo's own harness). Whether any stored verification_upgrade_requests row in any environment has target_level NONE, BASIC or SOCIAL was NOT queried; such a row is the only way the 48 changed cells can be reached.
- The 10 other services and frontends; middleware/authenticate.ts `requireVerificationLevel` and account-recovery were read, not driven (the PR does not touch them).
- Node 24 (LTS), Docker, the pre-push preflight, the four platform suites (Schemathesis, Akto, Playwright, k6), lint, the test-types ratchet, the integration vitest config, deploys, real clients.
- Ticket items 1 (non-atomic approve) and 3 (stale PENDING auto-close) — out of this PR's scope by its own statement.

## Plain answer for Kam
This change makes the account-verification approval check use the full official list of verification levels instead of a shorter local copy that left out "none" and "social". Nothing a user can do through the app changes: users can still only request the four higher levels, and every such request behaves exactly as before. The only difference is for a pending request asking for "none", "basic" or "social" against a user already above that level — the app could never create one, but if one existed, approving it used to silently lower that person's level, and now it is refused. In every case I tested, the new version is equally or more strict; nowhere does it allow more. The notes are housekeeping: no new automated test locks this behaviour in, and one old test still describes the old behaviour in its wording.
