## BLUF: the #1015 (KS-1018) TIER 1 ROUND 1 gate set is written. Launcher `--check` rc 0 (06:47:28–43 AEST). The gate was NOT launched.
- Brief: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1015-ks1018-tier1.md` (239 lines, sha256 `d1e10ea8039d50e5`)
- Prompt: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1015-ks1018-tier1.prompt.txt` (170 lines, sha256 `34d3e09603911b94`)
- Launcher: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks1018_1015.sh`, mode 100755, 216 lines, sha256 `78376b1d0550436d`, `bash -n` rc 0.
  - GENERATED from `launch_qa_secuura_ks999_1013.sh` by `gen_launcher_1015.py` (asserted substitutions, a residual guard for #1013 identifiers, output controls, bash -n; `gen_launcher_1015.out` 06:47:00). Same guards and exit codes 2..23.
  - Re-pointed: head exit 6; compare `523f283c6 ahead=2 files=2` exit 10/13; 18 JUDGED blobs (users.ts + the ks1018 test ABSENT at base, LANDED on head blob `6723276d0` or commit-1 blob `0fb3e7197`); GUARDED `services/auth/src/`, the auth config files, `packages/shared/src/` (widened from #1013's `crypto/`), `docs/openapi/`, `eslint.config.mjs`, the Dev lockfile, and NEW `migrations/`, `docker/init/`, `deployment/azure/migrate/` (exit 18); LANDED exit 19. Overrides `QA1015_*`.
  - The #1015 set does not use the round-2 exits 24/25 (round 1).
- `--check` output: `check.out` (develop still `523f283c6`, all 18 blobs = base).
- **Negative controls, `--check` only, stdin /dev/null: 9 of 9 as expected** (`controls_check.out` 06:47:49–06:49:10):
  - N1 head override (#1013's `5fbfb66a9`) → 6
  - N2 `neg_prompt_nomail` → 12
  - N3 `neg_brief_nosha` → 20
  - N4 `neg_brief_notier` → 7
  - N5 `neg_prompt_nofarm` → 22
  - N6 `neg_prompt_nosubject` → 23
  - N7 develop = the #1015 head → 19 (users.ts `8ef9065e2` LANDED)
  - N8 develop = commit-1 `6e30fe9f5` → 19 — **its label overclaims**: it refused on users.ts first, so it does NOT prove the commit-1 test blob is judged LANDED. It adds nothing over N7.
  - N9 develop = `1125607e9` → 18 via GUARDED userRepo.ts blob `822b3fcd8` (the blob arm).

## Top predictions (labelled; all drafter-measured in a scratch clone — the gate re-measures)
1. **The base defect is WRITES, and wider than the PR says** (MEASURED, `drafter_probe.out` 06:38, fault confined to the verification SELECT, stateful table):
   - base saves a duplicate PENDING row (all three infra forms);
   - base auto-approves STANDARD while a request is pending;
   - base approves a REJECTED request from a stale in-memory copy, raising the user's level and overwriting the row REJECTED → APPROVED.
   - Head: 503 with 0 writes in every row. **Predicted: no Major against #1015.**
2. **Three tampers are invisible (0 of 751, tsc rc 0)** (MEASURED, `drafter_run.out` 06:36–06:37):
   - D-TW-GET: the review rethrow widened to every error. The review site has no non-infra control.
   - D-NARROW: rethrow only when `err.code` is set. The KS-217 message-form pool timeout falls through again.
   - D-CTL-NOMEM: a non-infra error no longer falls through to memory. The controls cannot tell it apart.
   - Predicted grade: Polish / TICKET.
   - By contrast, all three caller fail-open tampers red 1 each, and ServiceUnavailableError→500 reds 17. **The #1013 F1/F2 lessons are applied.**
3. **The seat's base 200s on the two `/me` routes need a PARTIAL fault** (MEASURED, `drafter_probe_realrepo.out` 06:39).
   - With the REAL userRepo under a total outage, GET and POST already answer 503 at base (getUserById runs first). Only review flips (404 → 503).
   - Also on the unchanged save side (MEASURED): an INSERT fault still acks 200, and the request then vanishes from a healthy list. Pre-existing; the gate rules it.

## Disagreements with the READY mail / PR body (each a prediction)
1. "A DB outage let a new upgrade request be accepted and saved": true only for a fault confined to `verification_upgrade_requests`. A total outage already 503s at base on GET/POST.
2. The PR understates the base defect: the auto-approve write (S2) and the stale-memory approval of a REJECTED request (S3) are not named and not pinned.
3. "Any other error falls through as before" diverges from the KS-253 contract text in `dbErrors.ts` ("let anything else propagate … as a 500 — in neither case is a DB error a 'user not found'") and from `getUserById`'s `throw err`. At head a 42P01 still creates a duplicate PENDING, and now logs ERROR. Deliberate per the brief; the gate grades it.
4. "Casts only; no runtime change": runtime-equivalent, but not literally casts only. Emitted-JS diff = 5 redundant parens + one hoisted `const calls` (planted control caught).
5. "The applied file is byte-equal to the 139 lines": the READY's 139 `+` lines are an in-order subsequence of commit-1 (214 lines). The rest are declared seat edits. The seat's `apply-*.out` are 0 bytes, so the `--recount` apply is uncaptured.
6. The seat's including-tsc config (`exclude: ["node_modules","dist"]`, no noEmit) differs from the drafter's. Both read 37. The seat's "8 errors before the typing commit" was not re-derived by the drafter.
7. The PR body calls the change "a DB outage" throughout. The honest scope is an infrastructure error on the verification SELECT. Records, not findings.
- **Held (seat claims the drafter reproduced):**
  - auth 62/751 at head, pending 0 (base 61/745);
  - red before green 6 run / 4 red with the exact messages;
  - T0/T1/T2/T3/TL/TW/TK/TI reds exactly as the seat's table, tsc rc 0 on every row;
  - log meta keys `[code, error]`;
  - project tsc rc 0;
  - linkKind KS-1018 `contributes`, 0 closing phrases, 0 shared files.

## Pre-measurements (drafter; scratch `gate1015_draft_3jd99tvx`; all PREDICTIONS for the gate)
- **Substrate** (`drafter_setup.out` 06:33:24–48):
  - `--shared` clone; worktrees base `523f283c6` (auth tree `b788fec96`) and head `77145ce84` (auth tree `b5296906a`).
  - Farm per ENTRY: Dev 987, auth 9, shared 8, `.vite` skipped. `@secuura/shared` IN TREE in both trees.
  - Shared dist rc 0.
- **Suites** (`drafter_suites.out` 06:34):
  - auth base 61/745, head 62/751;
  - project tsc rc 0 both;
  - red before green 6 run / 4 red / 2 green;
  - including tsc 37 → 37, NEW 0, users.ts 0, ks1018 0 (listed), plant +1.
  - shared suite NOT run (tree `89afd4b9d` identical).
- **READY compare** (`drafter_ready_compare.out` 06:35):
  - product `+14 −4` equal in order;
  - users.ts commit-1 = head;
  - test 139/139 in commit-1, 136/139 at head.
- **Tampers** (`drafter_run.out` 06:35:40–06:37:31, whole suite, tsc rc 0 on all 19 rows, pending 0, 751 run):

  | Row | Red |
  |---|---|
  | T0 | 0 |
  | T1 | 1 |
  | T2 | 1 |
  | T3 | 1 |
  | TL | 1 |
  | TW | 1 |
  | TK | 1 |
  | TI | 0 |
  | **D-TW-GET** | **0** |
  | D-TW-FIND | 1 |
  | D-TL-GET | 1 |
  | D-TK-FIND | 1 |
  | **D-NARROW** | **0** |
  | **D-CTL-NOMEM** | **0** |
  | D-CF-POST | 1 |
  | D-CF-LIST | 1 |
  | D-CF-REVIEW | 1 |
  | D-EH-503-AS-500 | 17 |
  | T0-after | 0 |

- **HTTP probes** (`drafter_probe.out`, `drafter_probe_realrepo.out`): S1–S6 as in the brief.
  - Every head 503 has body = the fixed classifier text, headers content-type + x-powered-by, no Retry-After.
  - Every infra row at head logs `DB <fn> failed` [code, error] + `Error occurred`.
- **Reads:**
  - three schema sources (no unique pending index; FK difference in `docker/init`);
  - caller census (3 routes, no in-repo client);
  - spec (none of the three routes documented);
  - Linear 06:31:50; GitHub 06:31:06 (20 other open PRs, #1014 = api-gateway `enforcement.ts` + a test).
- **Checkout** (read-only; `git_read.out` 06:28:52 → `close_read.out` 06:49:28):
  - unchanged: porcelain 0, config sha `d7e7298b02c45f52`, 110 `.git/worktrees`, auth `.vite` 6,697 b @ 09-09 08:58:04, api-gateway `.vite` 5,907 b @ 09-17 01:02:02.
  - **refs 904 → 905**: a ref appeared during drafting, not by the drafter (a seat push, likely A9 or #1014 activity; not identified).
  - develop `523f283c6` and `refs/pull/1015/head` `77145ce84` at both readings.

## Deviations / slips (stated)
- **`drafter_setup.py` ran `git -C <checkout> worktree list --porcelain` twice** (before and after the clone: 111 entries both times). It is a listing, but the WEDNESDAY no-cd hook classes `worktree` as a write verb pointed outside the project: a later Bash reading that included it was REFUSED by the hook before running (nothing executed). The Python call inherited the #1013 set's `drafter_setup.py` unchanged. The close reading was re-run without it.
- **The generator refused twice before writing anything:**
  - the `QA1013_` count was 10, not 11, after the header swap;
  - the residual guard caught the intended provenance line.
  - Both were fixed with asserted edits. The launcher file did not exist until the third run (`assert not os.path.exists(DST)`).
- **The generator's first run had a Python syntax error** (a `]` for `)`). It wrote nothing.
- **Derivation of `linear_read.py` refused once:** the anchor `pull/1013 ` count was 0. It was re-derived. `gh_read.py` had already been written by the same step, and it ran correctly.
- The brief's "Drafted 06:28–06:5x" end time is approximate in the header. Every measured clock in the brief is from `date` output in the named `.out` files.
- **Not measured by the drafter:**
  - `docker info`; NODE_ENV variants of the leak check; ORG_ADMIN under the stale-memory row;
  - L4–L7 legitimate shapes; the `git apply` / `patch` behaviour on the over-declared READY header; the seat's 8-error claim at commit-1;
  - eslint (with or without a control); the shared suite; the api-gateway proxy read; a merged tree (develop = base throughout).
- Never launched the gate, never ran the launcher without `--check`, no tmux, no mail, no docker, no `rm`, no `cd`. No write to the Secuura checkout: scratch clone only, git write verbs only from script files inside it. Seat A's worktree was never entered; `a15-ks1018/` was read only. No `*1014*` file was read or written (only the GitHub PR files API for #1014's file names).
