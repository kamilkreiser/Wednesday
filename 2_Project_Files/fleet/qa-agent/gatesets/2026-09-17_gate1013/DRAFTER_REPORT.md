## BLUF: the #1013 (KS-999) TIER 1 gate set is written. Launcher `--check` rc 0 on the final bytes (04:56:42–56). The gate was NOT launched.
- Brief: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1013-ks999-tier1.md` (sha256 `2e071467baa41e3b`)
- Prompt: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1013-ks999-tier1.prompt.txt` (sha256 `75156817352a49d0`)
- Launcher: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks999_1013.sh`, mode 100755, 217 lines, sha256 `203ba6447bf03c7d`, `bash -n` rc 0, heredoc apostrophes 0 / parens even (81/81, 8/8).
  - Derived BY HAND from the #1010 launcher (not by a generator — stated). Same guards and exit codes 2..23.
  - Re-pointed: head exit 6; compare `1125607e9 ahead=1 files=3` exit 10/13; 21 JUDGED blobs; GUARDED `services/auth/src/`, the auth config files, `packages/shared/src/crypto/`, `docs/openapi/`, `eslint.config.mjs` and the Dev lockfile (exit 18); LANDED exit 19.
  - New: an ABSENT state (contents API 404) for the file the PR adds, and the override `QA1013_CUR_DEV`.
  - Exit 20 (SHA in both files), 22 (per-ENTRY farm), 23 (exact subject + coagent@ + wednesday-agent@), 12 (mail step), 21 (TTY on launch) and 16 (overrides on launch) are kept.
- `--check` output: `check.out` (04:56:42, rc 0, develop still `1125607e9`).
- **Negative controls, `--check` only, stdin /dev/null: 9 of 9 as expected** (`controls_check.out` 04:56:59–04:58:36; `controls_check_n9.out` 04:58:45).
  - N1 head override (#1010's c3213b04e) → 6
  - N2 `neg_prompt_nomail` → 12
  - N3 `neg_brief_nosha` → 20
  - N4 `neg_brief_notier` → 7
  - N5 `neg_prompt_nofarm` → 22
  - N6 `neg_prompt_nosubject` → 23
  - N7 develop = the #1013 head → 19 (userRepo.ts `9060b308e` LANDED)
  - N8 develop = d067725ff → 18 via **UNJUDGEABLE** (status=behind). Every JUDGED blob matched there, so this proves the compare arm, not the blob arm.
  - N9 develop = fa55e58c9 → 18 via **GUARDED** userRepo.ts blob `e6093b9f4` (the blob arm).

## Top predicted findings (for the gate to measure)
1. **The ticket's and READY's route-family premise is wrong in both directions.**
   - `/api/oauth/token` never calls `getUserById`. Both grants read `getUserByIdPreAuth` (oauth.ts:952/:1066, a KS-1186 sibling), and its catch hard-codes 500 (:1091-1093). So it stays 500 under a DEK infra failure at head.
   - Meanwhile `updateUser` ends `return getUserById(...)` (:926). That puts the 500→503 flip on login (:587), register, reset-password, verify-email, social link, wallet link, PATCH /users/me, the mfa setup/disable routes, admin PATCH (via PlatformScope), and more. It is far wider than four families.
   - Grade: a RECORD against the ticket text and KS-1186's scope, and a census the gate must measure. Not a code defect in #1013.
2. **The change's HTTP effect is unpinned, and so is the new log line's shape.**
   - `Q-EH-503-AS-500` (ServiceUnavailableError answers 500) reds 14/745, none in ks999/ks949.
   - `Q-LOG-LEAK` (the getUserById catch also logs `stack` + `userId`) reds 0/745.
   - Polish / TICKET candidates.

## Pre-measurements (drafter, read-only toward the checkout; `--shared` clone in scratch `gate1013_draft_hah47ehc`). ALL ARE PREDICTIONS for the gate.
- **Substrate** (`drafter_setup.out` 04:45:47–59):
  - Trees: base `1125607e9` and head `5fbfb66a9`. No merged worktree: develop = base (ls-remote 04:44:09, branches API 04:48:55, close read 04:59:02).
  - Farm per entry: Dev 987 entries, auth 9, shared 8, `.vite` skipped. `@secuura/shared` resolves IN TREE in both trees.
  - Source checkout worktree entries: 111 before and after.
- **Suites:**
  - auth base 60/740 (`drafter_suites.out` 04:47:27); head 61/745 (`t_T0`, `t_T0after`). Pending 0, success true.
  - ks949 base 30/30. Red before green: ks999 on base 5 run / 2 red / 3 green.
  - Project tsc auth rc 0 on both trees and on every tamper row.
  - shared: NOT re-measured (tree hash `89afd4b9d` identical base/head).
- **HTTP probe** (`qa1013-drafter-probe.test.ts`, `drafter_probe.out` 04:50:25–27, `probe_rows_{base,head}.json`). Real userRoutes/mfaRoutes/walletRoutes, real userRepo, real errorHandler, loopback. Stubs: db, getDek, shared crypto, authenticate, logger. Conditions a–e × 4 routes:
  - **(b) DEK infra → base 500 INTERNAL_ERROR, head 503 SERVICE_UNAVAILABLE on all four.**
  - (a)/(c)/(d)/(e): identical status and body on both trees.
  - (c) head adds the error log `DB getUserById failed`; base logged only `Error occurred`.
  - No user id in any body except the healthy /me data. No user id in any error-log meta for (b)/(c). `Retry-After` absent in every row.
  - Direct calls under (b): `getUserByIdWithPasswordHash` and `getUserByIdPreAuth` are raw `Error` at base AND head (KS-1186 real at unit level). `getUserById`: raw at base → AppError 503 + log at head.
  - Harness artefact: wallet/unlink (a) = 500 `WALLET_UNLINK_NOT_PERSISTED` on both trees (the stub answers the UPDATE with 0 rows).
- **Tampers** (head, whole auth suite of 745, tsc rc 0 and pending 0 on every row; `drafter_run.out` 04:48:29–04:49:46):

  | Row | Red |
  |---|---|
  | T0 | 0 |
  | TA | 2 |
  | TL | 2 |
  | TC | 3 |
  | TI | 0 |
  | Q-SWALLOW | 4 |
  | Q-500 | 4 |
  | Q-CTL-NODEK (control-aimed) | 7 (incl. 3 auth.integration) |
  | Q-DECRYPT-503 | 1 (the ks949 CHARACTERISATION) |
  | **Q-LOG-LEAK** | **0** |
  | **Q-EH-503-AS-500** | **14, 0 in ks999/ks949** |
  | T0-after | 0 |

  The seat's six rows match its `tamper999.out` exactly.
- **Including tsc** (in-tree `extends ./tsconfig.json`, `include src/**/*.ts`, `exclude []`, noEmit; `drafter_suites.out`, `tsc_including_*.out`):
  - base 37 → head 37. NEW 0 (line-number-free multiset compare).
  - userRepo.ts 0, ks999 0. ks949: 7 TS1343 at :226… → :228… (+2). 0 TS2741.
  - `--listFilesOnly`: 60/61 `__tests__` files; ks999 listed at head, ks949 listed in both.
  - Plant +3 TS6133.
- **eslint** (`drafter_eslint.out` 04:50:54): the 3 files 0 errors / 0 warnings on base and head. **No positive control was run** — the brief makes the gate owe one.
- **READY comparison** (`ready_patch_compare.out` 04:48:08): the product `+` line is present ×1 at head. The ks999 test = the patch's 97 `+` lines (0 diff lines). The patch hunk header says `+1,75`.
- **Linear** (04:49:10): attachmentsForURL(pull/1013) = 1 (KS-999 `contributes`, In Progress). KS-1186 Backlog, 0 attachments. KS-1168 Backlog, 0. KS-963 and KS-253 Done/archived with their own old `closes` links.
- **GitHub** (04:48:55): 1 commit, 3 files +126 −10. 0 closing phrases in title, body, commit and 1 comment (positive control 2 hits). **21 other open PRs, 0 exact shared files** (#1011 and #1012 included). Dependabot #948/#649/#575 touch auth package.json + the lockfile; #922 touches secuura-api.yaml (all GUARDED).
- **Spec** (`spec_read.out` 04:49:26): 16 calling routes are documented in `secuura-api.yaml`, and **every one already declares 503**. `/api/users/me/verification` and `/api/auth/verify-email` are absent. Controls: `^paths:` 1, `/api/documents` 28. The 503 response schema was not read (the gate owes it).
- **Source census:** a read-only sub-agent sweep (git show at the SHA). No caller outside `errorHandler` branches on 503 vs 500. No middleware reads users. No fail-open or lockout on an error in scope. No `Retry-After` in auth src. The errorHandler 500 body is generic in every env.

## Disagreements with the READY mail (each a prediction)
1. **/oauth/token is not a `getUserById` route.** It uses `getUserByIdPreAuth` and hard-codes 500.
2. **The reach is wider than four families** (via `updateUser` :926 and `getUserByIdPlatformScope`).
3. **Line numbers are base numbering.** `:406` is head `:410`; siblings `:442/:508/:581/:590/:623` are head `:446/:512/:585/:594/:627`; `:1036` is head `:1040`. Count five: held.
4. **`:1036` reasoning holds, but more strongly than stated.** `listUsersInner` has no try at all, so its `query()` infra failure is unclassified too. RECORD.
5. **Test patch hunk header `+1,75` vs 97 lines.** "Both sections clean" needs its tool named.
6. **`logCalls.length = 0` in the ks949 KS-963 `beforeEach` is an edit the READY's declared list does not name.** Harmless-looking; the gate judges it.
7. **The seat's including-tsc program was out-of-tree, inside the LIVE worktree** (67 lines incl. a TS2741 in ks1013's test). In-tree: 37 → 37, 0 TS2741. The #1010 gate's R4 class.
- **Held:** 60/740 → 61/745; the T0/TA/TL/TC/TI/T0-after reds; red before green 5/2; eslint 0; including-tsc NEW 0 with ks949 +2; the decrypt failure still propagates (as a 500) and is now logged; KS-999 `contributes`; disjoint from #1011/#1012.

## Outside the rules / slips (stated)
- **An early read-only Bash call had `echo ====` and zsh aborted it** ("==== not found", exit 1). The READY mail was re-read in the next call with `'-----'`. This is the same class the #1010 drafter hit. The brief and prompt now say "never begin a line or an echo argument with `=====`".
- **One Bash call was refused by the no-cd hook** before running (a stray `cd /dev/null` in the command line). Nothing executed; re-issued without it.
- **`drafter_run.py`'s first run died on its own marker assertion AFTER landing the TL tamper outside the try.** The scratch clone's head `userRepo.ts` was left tampered from ~04:48:0x. The next run restored it first (`git checkout --` inside the scratch worktree, from the script), and every later row asserted a sha-identical restore. The first run is kept as `drafter_run.first-run-marker-assert.out`.
  - Concurrency check: `drafter_suites.py`'s head including-tsc ran 04:47:3x–42, BEFORE the first tamper run started (04:47:48). So the head tsc numbers were not read on a tampered file. The Secuura checkout was never touched.
- **A GitHub-read derivation refused on its own asserted anchor count** (`/pulls/1010` ×5, not 3) and wrote nothing. It was re-derived with per-anchor asserts. Kept: `gen_reads.out`.
- **The checkout's `.git/config` sha differs from the #1010 gate's close reading:** `bb55e140…` (04:19) → `d7e7298b…`, config mtime 04:32:28; refs 897 → 899. That is before this drafter's first reading (04:44:23) and matches Seat A's #1013 push window (~04:35–04:40). Porcelain, config sha, refs 899, worktrees 110 and both `.vite` results.json were unchanged across my readings at 04:44:23 / 04:50:58 / 04:59:02.
- **The #907 gate's report was not found on disk** (grep 0 by SHA/date). The brief says so and names the #970 KS-963 report as the nearest.
- The launcher was never run without `--check`. No tmux, no merge, no comment, no mail, no docker, no `rm`. #1011/#1012 gate dirs were never listed or read. Seat A's worktree was never entered; its records dir `a14-ks999/` was read only. The route census sub-agent used `git show`/`git grep` by SHA only.

## Not measured by the drafter
- `docker info`; `/api/oauth/token` and `POST /api/auth/login` over HTTP; any route reached via `updateUser` / PlatformScope; one sibling route over HTTP; pg-coded (53300 / ECONNREFUSED) variants of (b).
- L3 (a non-infra DEK failure over HTTP) and L5 (destroyed DEK); the api-gateway proxy's handling of an upstream 503; the 503 response schema in the spec; `auth.openapi.ts`.
- The per-cell AST diff of ks949; eslint positive control; the shared suite; a merged tree (develop = base throughout drafting).
