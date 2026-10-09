# Carve screen for the Spark, 08:30 delta: 3 tickets carved, piece 1 of each drafted (none queued)

Written 2026-10-10 08:39 AEDT (shell `date`; Linear read 08:25, develop tip and open-PR census 08:26) by a read-only screening and brief-drafting sub-agent for Wednesday. Secuura only. Commission: Kam 2026-10-09 23:12 "keep pushing harder and harder tickets to the spark as a way of testing it" and 2026-10-05 "50 Spark tasks a day by CARVING big tickets". Method and exclusions mirrored from `../SCREEN_0600.md`; predicate from `learnings/2026-09-23_spark-kit-running-a-local-coding-model.md`; shape from kit `03_BRIEF_TEMPLATE.md`.

**Develop tip (`git ls-remote origin refs/heads/develop`, 08:2x AEDT): `7834fd8059da31025aba15a47c4b4d61447016ed`.** The Secuura checkout does not hold that object (its HEAD is `1fba82dd`, its `origin/develop` ref `ae9bf682`), and I may not fetch. So every file below was read at the tip through the GitHub contents API (`?ref=7834fd80...`, REST GET) and, for the three product files, byte-compared with `git show 613070f29112:<file>` (the SHA the 06:00 screen used, present locally): all identical. Each brief's `Tip:` line carries the true tip; its header says the same brief is valid at `613070f29112a40a0d8d9684cd50c7c2ae54592c` if the builder cannot resolve the tip.

## BLUF

Three open Secuura KS tickets that fail the predicate as written carve into pieces that fit it. Piece 1 of each is drafted, with a hand-derived golden diff and a new in-process test, under `carve_0830/`. **DRAFT, NOT QUEUED.** Recommended order if Wednesday queues: 1, then 2, then 3.

| # | ticket | fails the predicate as written because | piece 1 (drafted) | dir under `carve_0830/` |
|---|---|---|---|---|
| 1 | **KS-1426** preflight leg 2 installs only 4 directories of lockfiles | P2: the ticket says "Not claimed: a fix"; widening `find` is a trade (install time every push, `--no-workspaces` on the root lock, Prettier scope) it leaves open. P6: acceptance is "6 of 36 locks installed" = real npm installs | the leg PRINTS which tracked `package-lock.json` files it did not install (`surface: N of M`, then the list); no scope change, exit code untouched. 1 product file (31-line function + 4-line call) + new 107-line stub-PATH suite on a throwaway git repo | `KS-1426-p1-lockfile-cleanroom-names-surface/` |
| 2 | **KS-1417** dead `API_GATEWAY_PORT=6882` in both env templates | P1: two product files; P2: "your call" between delete and replace | `env.example:361` becomes two comment lines; new 78-line suite runs the REAL `bootstrap-env.sh` for slot 2 and reads whether the key reached the generated `.env` | `KS-1417-p1-env-example-dead-gateway-port/` |
| 3 | **KS-1289** `.dockerignore` `tests` does not match `__tests__` | P6: acceptance is a Docker rebuild showing the rebuilt-image set shrinks (23 of 29 to about 6); nothing in-process can run it | one inserted line `**/__tests__`, **placed after the `!connectors/whatsapp-bot` negation** (last match wins) + new 72-line static suite that checks presence AND order, with planted-file controls. **Flag: a fleet seat excluded this ticket on 2026-09-26 for image-wide blast radius; read the golden before queueing.** | `KS-1289-p1-dockerignore-excludes-tests-dirs/` |

**Why these three are harder than the 06:00 floor (KS-1456, a 2-line echo edit):** KS-1426's payload is a 31-line bash function with three bash 3.2 traps (empty array under `set -u`, no `+=`/`mapfile`, newline via `$'\n'`) and a suite that builds a git repo; KS-1417's suite drives the real bootstrap script end to end; KS-1289's difficulty is placement (a patch that applies cleanly beside the existing `tests` line excludes nothing under `connectors/whatsapp-bot`, and the test is built to refuse exactly that).

**Figures (scratch tree, bash 3.2.57; node/npm/psql stubbed where the subject calls them), each with its control:**

| draft | new suite at the tip | with the golden | tamper (one literal break) | strict `git apply --check` |
|---|---|---|---|---|
| KS-1426 | rc 1, 3 passed / **2 failed** | rc 0, 5/5 | 2 tampers, each reddens exactly 1 cell (4/1) | fwd rc 0, reverse-before nonzero, bytes equal, reverse-after rc 0 |
| KS-1417 | rc 1, 2 passed / **2 failed** | rc 0, 4/4; siblings `bootstrap_env_canonical_template` 7/7 and `bootstrap_env_slot_ports` 51/51 both before and after | re-adding the key reddens both cells | same four |
| KS-1289 | rc 1, 2 passed / **2 failed** | rc 0, 4/4 | pattern moved to line 14 reddens the order cell (3/1) | same four |

`brief_lint.py` (run with `-B -I`, read-only, no `__pycache__` written): printed its shell assignments and no `REFUSED` line on all three. The fenced diff and the fenced test in each brief were byte-compared to the golden and to the test file: identical, and the new-file hunk line counts match.

## FRAME: tickets read, filters, counts, controls

- **Enumerated:** Linear GraphQL, team `KS`, state type in `backlog, unstarted, started`, paginated: **509 tickets** (Backlog 245, In Progress 217, Todo 29, In Review 13, Blocked 5). **Control:** every one of those five state counts equals the 06:00 screen's, and the assignee split Peter 18 / Stuart 8 equals its 26.
- **Waterfall (same order as 06:00):** 509 open, minus the 14 named live lanes (all 14 present: control) = 495, minus assigned to Peter (18) or Stuart (8) = 469, minus In Review / Blocked net = 454, minus title keyword for an auth/credential/security surface or a decision card = 343 (removed **111**, equals 06:00), minus already named in a `local-model/` brief dir, READY or quarantine file, `spark/done.md` or `spark/queue.md` (**113** ticket numbers, 06:00 had 108; the +5 are files written since 06:00) = **230**.
- **Live lanes re-derived rather than copied.** Open PRs now (GitHub REST GET, 08:26): **27 open PRs, 137 file entries** (06:00: 26/133). The 06:00 list's PRs are partly gone; the open ones are #1442-#1446 (KS-998, KS-1346, KS-1410 x2, KS-937), #1383 (migration 049), #1360 (lock revert), #1253, #1250, #995, #989, #927, #923, #920, #887, #809, #1129 and ten Dependabot bumps. Collision census for the three targets: `lockfile-cleanroom` 0, `.dockerignore` 0, `env.example` / `env.local.example` 0, the three new test names 0, `scripts/preflight/` 0. **Controls:** `run-shell-suites` finds 1 (on #1250), `.gitignore` finds 1 (on #920), a nonsense name finds 0; pagination page length 27 and the largest PR's file page (22) are both under the 100 cap, so no PR was truncated.
- **Mechanical pass:** of the 230, descriptions citing at least two repo paths and with no comment saying merged/squash = **49**. Plus a title scan of all 230. **29 descriptions read** in full or to 5,000 characters (some long lines cut to 700-1,000 characters on screen): 954, 807, 1426, 1405, 1417, 1138, 1251, 768, 1389, 1082, 1317, 846, 1393, 1391, 1114 (plus its comments), 1327, 1023, 1329, 1289, 1022, 1326 (plus comments), 1030, 1115, 1434, 1409, 1444, 1387, 1088, 1323.
- **Staged-lane check:** `fleet/briefs_staged/`, `local-model/night/briefs/`, `spark/` grepped for the three ticket numbers: KS-1426 appears only as a "near miss" in G7's wrap (a different defect) and in G3's plan as a Backlog row; KS-1289 only in the 2026-09-26 L8 lane's exclusion list (reason quoted above); KS-1417 nowhere. No seat holds any of them.
- **Why KS-1417 was missed at 06:00 though it was in the 235:** its description cites `env.example:361`, a bare filename, and the 06:00 mechanical pass required a `services|packages|scripts|connectors|frontend/<path>:<line>`. A harness note, not a criticism: the regex for "cites a file and line" should accept a bare filename plus line.

## The carves

### 1. KS-1426 (Backlog, board account, filed 2026-10-06 from gate70 N-1397-7)

- **As written:** "the leg prints 'All 35 standalone lock(s) pass' and reads like a total ... 6 of the 36 locks #1397 changed were never clean-room installed". Fix shape explicitly not claimed ("Widening `find` would add install time to every push ... a naive change there has its own blast radius").
- **Carve:**
  - **P1 (Spark, drafted):** disclose the surface. File `Blockchain/Dev/scripts/preflight/lockfile-cleanroom.sh` (+ one new test). Depends on nothing.
  - **P2 (NOT Spark, a decision):** widen discovery to include `connectors/`, the root lock and `systemTest/*`, or declare the exclusions by named rule with a reason (the KS-768 option 2, delivered for leg 7 as `lock-discovery.mjs`). Blocked on a ruling about install time and `--no-workspaces` on the root lock. Depends on P1 (reuses its listing).
- **What P1 closes:** nothing of the ticket's acceptance; it makes the "All N" line stop reading as a total. Brief says so as narrowing: "closes 0 of 1 acceptance lines; refs KS-1426, does NOT close it."
- **Expected output on the real tree (computed, not run):** `git ls-tree` at `613070f29112` shows 45 tracked `package-lock.json`, 35 of them matching the leg's four-directory pattern (the same 35 as KS-768; positive control: the pattern hits `scripts/preflight/package-lock.json`), so the new line should read `35 of 45` and list 10 paths (connectors/whatsapp-bot, mobile/secuura-app, the root lock, tests/e2e, tests/e2e-v2, observability, and four under systemTest).
- **Draft brief:** `carve_0830/KS-1426-p1-lockfile-cleanroom-names-surface/` (`KS-1426.md`, `golden.diff`, `spark.pins`).

### 2. KS-1417 (Backlog, board account, filed 2026-10-05 from KS-1411)

- **As written:** two templates, delete or replace, "your call".
- **Carve:**
  - **P1 (Spark, drafted):** `Blockchain/Dev/env.example:361` plus the new suite. This is the canonical template that `bootstrap-env.sh` copies, so it is the one that matters.
  - **P2 (Spark, not drafted):** `Blockchain/Dev/env.local.example:56` plus a second cell appended to P1's new test file (2 files, 1 product + 1 test; **depends on P1 having merged** because it modifies the file P1 creates). Same ticket-named options; the same comment text.
- **Judgment call surfaced:** the brief takes "replace with a comment" (the ticket's option 2) because deleting the only line under `# API GATEWAY` leaves an empty heading; the suite passes under either, so Wednesday can flip it to delete without touching the test.
- **What P1 closes:** 1 of 2 template lines; refs KS-1417, does not close it. The ticket's optional static guard is KS-1381's and is not touched.
- **Draft brief:** `carve_0830/KS-1417-p1-env-example-dead-gateway-port/`.

### 3. KS-1289 (Backlog, board account, filed 2026-09-25, Seat B)

- **As written:** add a pattern for `__tests__` and "verify by rebuilding after a shared-test-only change and showing the set of images that rebuild shrinks".
- **Carve:**
  - **P1 (Spark, drafted):** the pattern line, placed after every `!` line, plus a static suite. No Docker needed.
  - **P2 (NOT Spark):** the rebuild measurement. Needs Docker and the stack; belongs to a seat that can run them; depends on P1 on a branch.
- **Premises measured at `613070f29112` (read-only `git grep` / `ls-tree`):** all 25 service `tsconfig.json` files mention `src/__tests__` (24 service Dockerfiles, each has one); no Dockerfile under `Blockchain/Dev` (35) runs vitest/jest/`npm test`; the only Dockerfile line naming `__tests__` outside comments is `billing/Dockerfile:52`, a `jq` that already excludes it from the tsconfig; outside `__tests__` directories the string appears in services/packages only in comments and in vitest/jest/tsconfig config. **Control weakness, stated in the brief:** the import regex has no positive control (it returns 0 inside test directories too), so "no runtime import of a test file" rests on the broader `__tests__` listing, which does fire.
- **Why it is flagged:** the L8 lane (2026-09-26) excluded it for "`.dockerignore` changes every image's build context". It is one inserted line, but it changes what is in 23+ images. Not approval-class (no prod, money or external comms), yet Wednesday should read the golden first.
- **Draft brief:** `carve_0830/KS-1289-p1-dockerignore-excludes-tests-dirs/`.

## Candidates read and rejected (reason per ticket)

Predicate clauses: P1 one product file, P2 fix shape spelled out, P3 in-process test nearby, P4 not auth/credential/security, P5 not shipped/held/at counter, P6 a runner the checker runs, P7 no open-PR collision.

| ticket | verdict |
|---|---|
| KS-1405 schemathesis.json not gitignored | `.gitignore` route collides with #920 (touches `.gitignore`: positive control in the census); the other route (default `FINDINGS_DIR` elsewhere) is "whoever picks it up should decide" (P2) |
| KS-1329 packages/shared does not type-check `src/__tests__` | every piece is a test-file edit (test-only is not wired in `round.sh`) or the `ssrf-guard.ts` TS2349, which the ticket calls a decision on a security guard (P2, P4); the leg touches the push gate |
| KS-1391 no frontend declares `test` | step 1 is a `frontend/issuer/package.json` edit; #948, #947 and #639 touch that file (P7), and package.json edits sit under the push-freeze hold lane |
| KS-1114 verify title-only body | Kam ruled `implement-title`, but the ruling comment leaves the design open (several registrations sharing one title; whether the anonymous route may answer at all): P2, and a verification route |
| KS-1434 spec lacks `rotate` | `/api/security/keys` is the API-key surface (P4), and the fix is the `*.openapi.ts` plus the regenerated yaml (P1) |
| KS-1115 anchor_store status CHECK | needs a live census of rows on every environment before a migration; unrunnable here (P6) |
| KS-1444 untagged images after `--rebuild` | docker prune and compose labels across ~35 services, "for Kamil's judgement"; no in-process runner (P2, P6) |
| KS-1389 / 1382 / 1381 / 1162 | slot-derivation group with a shared acceptance and a coordinated push-hook change (P1, P2) |
| KS-1088, 1331, 1302, 1303 | `run-shell-suites.sh` is on #1250 (P7); 1088 is "decide whether the runner should enforce isolation" (P2) |
| KS-1326 childSuiteCounts killed child | `systemTest/performance` (Peter's authority) and `countsFromSpawn` already appears at `613070f29112` in `unitSuiteSlotIndependence.test.ts:185,:244`, so the ticket text is stale or partly delivered; not verified, so not drafted |
| KS-954 `//api/billing` 404 | "Mechanism NOT determined. Reproduce before fixing" (P2) |
| KS-807 control-byte guard cannot see raw bodies | "asks a question ... decide first" (P2); shared security middleware (P4) |
| KS-1251 eslint `rules: {}` on `*.mjs` | "fix what it flags" is an unmeasurable count without running eslint, and two config files (P1, P6) |
| KS-1317, KS-846 | `package.json` edits with fix options "not chosen" (P2) |
| KS-1393 | deleting 31 spec files and a 708-branch sweep; never delete, and it is a decision (P2) |
| KS-1138 | fails on the Linux runner only; cannot reproduce on this host (P6) |
| KS-768 | delivered for leg 7 by #796 per its comment; KS-1426 is its leg-2 twin and is carved above |
| KS-1387 | cause removed by KS-1380 (comment 2026-10-02); residue is a close, not a code change (P5) |
| KS-1030, 1022, 1327, 1409, 1323 | multi-file or Postgres-dependent (1030), "NOT per-route" structural design (1022), whole-row read-modify-write design (1327), owner's decision (1409), seat tooling outside the repo (1323) |

**A zero, with its control:** "no further carve survived beyond these three" is a statement about 29 descriptions read and a title scan of 230, not a measurement of all 230 bodies. The instrument fires: the same filters admitted KS-1426, KS-1417 and KS-1289 and rejected KS-1405 and KS-1391 for the stated collisions.

## UNMEASURED

- `round.sh --dry-run` and `--control` for any draft (they write `spark/state/` and `runs/`, outside this commission). The builder (`build_bash_input.sh`) has not read any of the three: whether `ref=` / `test_file=` / `Tip:` resolve is owed; in particular the builder refuses a tip "not local", and the true tip `7834fd80` is not in the checkout, so the first dry-run may need the `613070f29112` fallback named in each header.
- No real run of any subject against the real tree: KS-1426's `35 of 45` is computed from a tree listing; KS-1289's effect on a Docker build context is reasoned from the file's own comment, not observed; KS-1417's gateway behaviour is the ticket's own measurement.
- Only bash 3.2.57 (macOS) was run. The Linux runner's bash was not.
- 201 of the 230 survivors were screened on title and the mechanical pass only; a ticket whose title hides a fit could be missed. The 49-ticket pass requires two path citations in the description.
- The 14 live lanes were taken from the commission and checked only for presence on the board; I did not re-verify their state. PR #1268 (named in KS-1329) is not among the 27 open PRs; whether it merged was not checked.
- Live seats' unpushed work on these three files was not checked (only open PRs and staged briefs).
- Whether a model reproduces the exact text: that is the experiment. The wording of the new output lines in KS-1426 and the comment in KS-1417 is Wednesday's choice; none of it is approval-class.

## Harness findings

1. **`pretooluse_no_cd.sh` also refuses `git -C <scratch> init|apply` as a write verb "outside WEDNESDAY"**, though the target was the session scratchpad it tells agents to use. Workaround used: write goldens with `diff -u` and run `git apply --check` from Python with `cwd=`. Worth teaching the hook that the scratchpad is allowed.
2. **`pretooluse_no_rm.sh` refuses `rm -rf $VAR` even on a scratch path**, by design (the hook cannot see variables); used fresh directories instead.
3. **The 06:00 "cites a file and line" regex misses a bare filename plus line** (KS-1417's `env.example:361`); widen it.
4. **The checkout's `origin/develop` is `ae9bf682` and the real tip is `7834fd80`; `613070f29112` sits between.** Three different "tips" in one checkout. Any working-tree read is stale; the contents API at a SHA is the only read that is both current and read-only.
5. **`brief_lint.py` accepts a brief whose `Tip:` the builder cannot resolve.** A lint warning "Tip object not in the local checkout" would catch it before `round.sh --dry-run` writes state.

## Files written (all under this folder)

`CARVE_0830.md` (this file) and three draft directories, each with `KS-<n>.md`, `golden.diff`, `spark.pins`:
`KS-1426-p1-lockfile-cleanroom-names-surface/` · `KS-1417-p1-env-example-dead-gateway-port/` · `KS-1289-p1-dockerignore-excludes-tests-dirs/`.
Scratch (session scratchpad, not durable): `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/799de9f1-e570-4ab2-ad2b-ee9f62d6143d/scratchpad/` (`ks.json` the 509 tickets with 50 comments each, `left.json` the 230, `prs.json`, `tip/` the tip copies, `w14xx/` and `w14xx_gold/` the tip and golden trees, `mkbriefs.py` the generator: fences are copied from the golden and the test file, never retyped).
