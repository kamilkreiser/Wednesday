# KS screen for the Spark: 2026-10-07, 23:00 delta (1 brief delivered, KS-1139 smoke-test counters)

Written 2026-10-07 23:05 AEDT (shell `date`; the brief is stamped 23:03:06) by a Spark brief-writer sub-agent for Wednesday. Secuura only. Method: SCREEN_1520's instruments and rules, the kit predicate (`spark-kit_2026-09-23/02_FOR_THE_COORDINATOR.md` §2), the kit-03 brief shape, `spark/README.md` (`--dry-run` / `--control`).

**Read-only on client systems:**
- Linear: GraphQL reads only. `LINEAR_API_KEY` came from the Blockchain `4_Credentials/.env` in a `set -a` subshell and was never printed.
- GitHub: REST GET only (open PRs and their files).
- Git under `!CODING/`: read verbs only (`ls-remote`, `status`). `git status --porcelain --untracked-files=no` on the Blockchain checkout reads 0 lines after the work.
- Every git write verb (clone, fetch, checkout, worktree, apply) ran in `git clone --shared --no-checkout` copies under this session's scratchpad. The tip was fetched by full sha from the GitHub URL with the deploy key and `env -u GIT_SSH_COMMAND`.
- `round.sh --dry-run` and `--control` used round.sh's own cache and run dirs.

**Not touched:** `spark/queue.md`, `night/queue.md`, `PAUSE_QUEUE`, tmux, mail, Linear writes, GitHub writes. No model round was run. Nothing was deleted.

## BLUF

1. **Tip:** develop `2c27ddfeef519599407682c89a28c275d7bc3559`. `ls-remote` read it at 22:54:16, 23:01:47 and 23:05:08 AEDT, unchanged. It is the sha Wednesday read at ~22:5x.
2. **Delta: 20 distinct tickets**, matching Wednesday's counts (18 + 6, with 4 in both). See "How the delta was derived".
3. **Delivered: 1 brief.**

   | Brief dir (`2_Project_Files/local-model/night/briefs/`) | Ticket | Tier | Dry-run | Control |
   |---|---|---|---|---|
   | `KS-1139-smoke-test-counters-errexit` | KS-1139 (In Progress, Kamil); refs KS-1148 | bash_patch | **rc 0**, "DRY-RUN OK"; prompt source is the brief (`input.json` `ticket.description` opens with the brief's heading; builder: "sites 5 (3 must_change); expected '+' 3") | **rc 0, CONTROL-PASS: PASS 7/7 + A2a 1/1, golden BYTE-IDENTICAL**, 33 s |

   - **Files:** `Blockchain/Dev/scripts/smoke-test.sh`: 1 hunk, `:27`/`:28`/`:29`, changing `((X++))` to `X=$((X + 1))`. Plus a new test, `__tests__/smoke_test_counters_survive_errexit.test.sh` (102 lines).
   - **Control run dir:** `runs/spark_secuura_2026-10-07_KS-1139-smoke-test-counters-errexit-control`.
   - **sha256/16:** brief `40150a91737d5676`, golden `48b01b8cb87e16d7`.
   - **Pins:** `tier=bash_patch`, `ref=…/smoke_test_degraded_warns.test.sh`, `test_file=…/smoke_test_counters_survive_errexit.test.sh`.
4. **What it fixes.** `smoke-test.sh`'s three counter helpers return status 1 when counting from 0. On bash ≥ 4.1 (the Linux CI runner, the Ubuntu demo VM), errexit kills the deploy smoke test at its first check. This is the "A bug in the script" finding in Peter's 09:59Z comment on KS-1148, and the three sites his 10:05Z comment added to KS-1139's census. The fix shape is KS-1139's own: `COUNT=$((COUNT + 1))`.
5. **Not queued.** Wednesday appends the dir name to `spark/queue.md`. Counter: round 0 of 2.

## How the delta was derived

Two separate GraphQL `issues(first:100)` queries, each paginated until `hasNextPage` was false, then unioned. There is no top-level `or:`.
- **Updated set:** filter `team.key eq KS`, `state.type in [backlog, unstarted]`, `updatedAt gt 2026-10-07T04:20:00Z`. Result: 1 page, **18 nodes, 18 distinct**.
- **Created set:** filter `team.key eq KS`, `createdAt gt 2026-10-07T04:20:00Z`. Result: 1 page, **6 nodes, 6 distinct**.
- **Positive control:** KS-1441, KS-1443 and KS-1444 are all in the created set (they are also in the updated set).
- **Union:** 20 distinct. KS-1441, 1442, 1443 and 1444 are in both sets. KS-1439 and KS-1440 are created-only, both Done.
- **Excluded before screening (6):**
  - Peter: KS-492, 1396, 1439, 1440, 1442.
  - Stuart: KS-188.
  - KS-1439 and KS-1440 are also Done.
  - None of the R lane's In Progress tickets appear in the delta.
- **Screened: 14.** All were read in full at source, including every comment created after 04:20Z (instrument: the `comments` field, filtered by `createdAt`).

## Verdict per ticket

| Ticket | Verdict · the clause that fails |
|---|---|
| **KS-1139** (reached through the KS-1148 comment) | **BRIEFED.** `smoke-test.sh:27-29` only. KS-1139 is not in the delta: it is In Progress, so the state filter excludes it, and it was created 2026-09-13. It was read because Peter's 10:05Z comment on it is the home for the sites. The ticket's other residue is owed live sweeps, not code. |
| KS-1148 CI-runner gaps (3 new comments) | **NOT** for its own items: CI job setup (missing `npm ci` or build), with no in-process runner. The 09:59Z comment changes the verdict for one carve only, `smoke-test.sh`, which is briefed under KS-1139 where Peter filed the sites. The other two suites it names are KS-1443's (below). |
| KS-1443 two shell tests assume macOS | **NOT.** Both items are **test-only** (the fixes "stay inside the tests"), and no wired Spark tier takes test-only (`round.sh` refuses `test_only`; bash_patch/bash_patch2 need ≥ 1 product script). The red is also **Linux-only**: lsof's `MainThrea` and `/usr/bin/pg_isready` cannot red on this Mac's checker. Item 2 is KS-1296's cell (In Progress). Item 1 is systemTest ("Peter can take it if preferred"). |
| KS-1444 `--rebuild` leaves untagged images | **NOT: decision** ("Suggested fix (for Kamil's judgement)"). Docker/ops work with no runner. |
| KS-1441 Akto LOW HEADER_ALL_KEYS_INVALID_VALUES | **NOT: decision** ("Classify each: by design, or a finding. Kamil's call"). It is also a **security surface** (Akto, CWE-20, wallet-status) and **measure-first** (a targeted Akto re-run comes first). |
| KS-1009 wallet/status anonymous enumeration (2 Peter comments) | **NOT: security/auth surface**, unchanged. The comments add Akto evidence and a correction; neither spells a fix. |
| KS-724 scan revokes its own bearer (1 Peter comment) | **NOT: auth/token surface**, unchanged. The comment reports item 1 fixed in PR #1411; items 2 and 3 are still open and still about tokens and sessions. |
| KS-709 Akto PASS on nothing executed (1 Peter comment) | **NOT**, unchanged: decision, Peter's systemTest/akto split, and the security tier. The comment is one more data point. |
| KS-752 Schemathesis baseline gate unreachable (1 Peter comment) | **NOT**, unchanged: no runner, live stack or ops. The comment is evidence only ("Nothing needed from you"). |
| KS-565 sweeps register (1 Peter comment) | **NOT**, unchanged. The comment is a register addendum: "Nothing here needs anything from you". The earlier carve (KS-591 carve 1) stands. |
| KS-593 not_a_server_error register (1 Peter comment) | **NOT**, unchanged. The comment is count-only, with "none is new". Existing KS-593 briefs and READYs cover the briefable rows. |
| KS-716 super-admin surface unscanned (no new comment) | **NOT**, unchanged: Peter's split, and a credential-adjacent `secrets.example.yml`. Its updatedAt matches the KS-724 comment that names it (09:28Z). |
| KS-1138 manifest_readers_agree in CI (no comment) | **NOT**, unchanged: no runner, live stack or ops (10-05 widened screen). Updated 10:05Z, when KS-1443 linked it. |
| KS-1324 run_shell_suites wall-clock margin (no comment) | **NOT**, unchanged: a timing flake that cannot red-prove deterministically. Updated 09:54Z, matching the KS-1148 comment that lists it. |
| KS-1331 run-shell-suites grandchild signal (no comment) | **NOT**, unchanged: process-group signals have no deterministic in-process red, and there is a capped-round residue with an open PR. Updated at the same time as KS-1324. |

**Not separately verified:** for the four tickets with no new comment, which field changed. The updatedAt times match the comments and new tickets that link them; the issue history was not read.

## The delivered brief: how it was measured

All measurement ran in a `--shared` scratch clone detached at `2c27ddfeef51`, under `/bin/bash` 3.2.57.

- **Red-first.** At the tip the new suite reads `3 passed, 3 failed`, rc 1. The 3 FAILs are exactly the RED cells: `want 0 1, got 1 1 (statement: ((PASS++)))` and its FAIL/WARN twins.
- **Green after.** With the hunk: `6 passed, 0 failed`, rc 0.
- **Sibling suite.** `smoke_test_degraded_warns.test.sh` reads 5/5 both before and after.
- **`bash -n`** returns rc 0.
- **Why the red works on bash 3.2.** The RED cells read each helper's own counter statement out of `smoke-test.sh` and run it from 0. They grade the STATUS (measured on 3.2: `((P++))` from 0 returns 1), which is exactly what errexit acts on in bash ≥ 4.1.
  - The death itself cannot be reproduced on 3.2 (measured: `set -euo pipefail; P=0; ((P++))` survives).
  - This is the same proof shape #1260 used on `sync-secrets.sh` (merged).
- **Strict apply.** The golden passes `git apply --check` and `git apply` on a pristine worktree at the tip. Both resulting files are `cmp`-identical to the hand edit.
- **Fences match the golden.** Both fences in the brief were cut from the golden by script and re-compared equal.
- **Blank context.** There are no blank context lines: `:26` is re-emitted as a `-`/`+` pair.
- **ASCII.** The test is all ASCII. The product lines carry `✓` and `✗` on `:27`/`:28`, and the `:30` context carries `━`. These are unavoidable, and the brief tells the model to copy them byte for byte.
- **Checker legs (control).** B0–B6 all PASS. B4 is red-first with 3 FAIL lines. B6 confirms the sibling suite has no new failure. B7 is informational: shellcheck is not installed. A2a: hunk 1 is at `:25` (OK) and the new file is skipped.
- **Edit points: 3 sites, 1 hunk.** This is within the kit's limit.

**Collision census:**
- **Open PRs:** GitHub GET, ~23:00 AEDT: 24 open PRs, 137 file entries, 0 paths containing `smoke`. Positive control: 4 `Blockchain/Dev/scripts/` paths are in that list.
- **Branches:** no branch names `smoke-test`.
- **READYs:** `READY_KS-1250` (HELD, "DO NOT RAISE WITHOUT KAM") touches `smoke-test.sh`, but at `@@ -15,2`, which is disjoint from `:25`-`:30`.
- **Earlier KS-1139 carves:** night lane A/B (09-16), R16B (09-22) and R17 (09-23). All were on `sync-secrets.sh` or `validate-lint.sh`, and all passed first round. `grep -lF smoke-test.sh` over every KS-1139 READY and brief finds 0 files. Control: 5 READYs name `validate-lint.sh`.
- **Spark ledgers:** KS-1139 has 0 rows in `spark/done.md` and `spark/queue.md`.

**Scope written in the brief:** "NARROWING: `smoke-test.sh:27`-`:29` only. Refs KS-1139 and KS-1148; closes NEITHER."

**Surface call (Wednesday's to confirm).** `smoke-test.sh`'s full mode logs in with demo credentials. The brief touches only the counter helpers, and the test runs `--quick` against a stub `curl`. This screen judged it not an auth surface, and the brief states that judgement in a Surface note.

## Findings for Wednesday (none acted on)

1. **KS-1139's census regex is `^`-anchored, so it misses one-line function bodies.** Peter says so in his 10:05Z comment. His unanchored search also lists `validate-env.sh:62/:81/:99`, which the ticket rules NOT defects (errexit is suppressed inside `if` bodies). That ruling was not re-measured.
2. **Docker was not running** (the socket at `~/.docker/run/docker.sock` is absent). A first `docker images | grep` read empty only because grep hid the connect error; the unfiltered control exposed it. So no bash ≥ 4.1 measurement was possible on this host.
3. **Disk.** One more per-round clone was added under `spark/cache/work/` (the control run). Two scratch clones sit in this session's scratchpad. Nothing was removed.

## UNMEASURED

- **No model round.** Whether the Spark reproduces the golden, including the non-ASCII bytes, was not measured.
- **No bash ≥ 4.1 run.** The death, and whether `smoke_test_degraded_warns` goes green on the Linux runner after the fix, rest on Peter's bash 5.2 measurement. Peter: it "could still have a second failure behind the first".
- **No full (non-`--quick`) run and no real stack.**
- **Field-level history** of the four tickets updated without a comment was not read.
- **Whether any live seat is working KS-1139 right now** was not checked beyond the commission's R-lane list (KS-1139 is not on it). Its last Secuura-agent comment is 2026-09-25 (Seat L5, round 24).
