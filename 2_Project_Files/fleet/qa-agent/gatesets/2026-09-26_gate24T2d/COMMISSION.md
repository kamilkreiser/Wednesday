# COMMISSION — DRAFT the round-24 CAP batch gate kit "gate24T2d" over SEVEN PRs (Seats L5, B 28th, L7, L8), FROZEN at seven. Do NOT launch.

Relayed by Wednesday to the drafter on 2026-09-26 (~04:1x AEST) as three PRs + a round-25 widen slot (cap 8), then WIDENED four times mid-draft by
Wednesday's messages ("WIDEN gate24T2d with #1263 KS-1140 … Cap stays 8"; gate24T2c RUNNING since 18:24:04Z over 4db87c3e; then "WIDEN gate24T2d with
#1264 KS-1281 … 5 of the cap of 8"; "#1265 KS-1315 … 6 of the cap"; "#1266 KS-1120 … 7 of the cap of 8 — FREEZE at the next READY or at your pin"), and a CARRY for #1250's N-1250-b timing cell (re-run once under load; never decides the cap). Recorded here as
the gate's commission; the QA agent reads it. Shape copied from `gatesets/2026-09-26_gate24T2b/`: JSON pins, routing-file override, controls both ways
with `--invert`; re-keyed to SEVEN rows, no stack base, plus a Postgres port step for #1262.

## The batch — every head re-read by the drafter from origin (ls-remote + a fetch into a `--no-local` scratch clone + the PULLS API)
- **#1250** KS-1302 + KS-1303 ROUND 2 OF 2 — THE CAP (Seat L5, wrapped), head `2b8dcb824dd2c5cd4b92757934d7de9d28813a22`: THREE commits on BASE
  `6e2a00bfed57` (round 1 `c78f4093fb53`, R2 `86ba93d25211`, R2b `2b8dcb824dd2`), fast-forward. Graded against **Wednesday's RULING (a)**, which
  SUPERSEDES the round-1 signal-cell clause, AND against the round-1 blocking property itself (SIGTERM: non-zero, no further suite, no verdict, dir removed).
- **#1253** KS-1297 ROUND 2 OF 2 — THE CAP (Seat L5, wrapped), head `91e066264004fdb22c67efb0c25fc44375ec6eac`: TWO commits on BASE (round 1
  `6b88e4f03e82`, R2), fast-forward. THE READER RULE: the five swallowing shapes flagged, `false || bf` and `|| true` NOT flagged, through the REAL guard
  with `SUBJ_SH=<copy>`. **No READY message id reached the drafter** — its claims are captured from the PR body.
- **#1262** KS-1310 + KS-1311 (Seat B 28th, wrapped), head `3b319485d1e3a58f30e4190a7898d7562cb80c3b`: ONE commit on develop `fa25c9b10fb4`. A DB
  integration cell (a test-scoped BEFORE UPDATE trigger on `documents`) that REFUSES unless its connection is 127.0.0.1 on 55410-55419. The gate's own
  disposable Postgres on **127.0.0.1:55419 ONLY**; Docker for this PR only; red at `33ccff807eb2` (#1239's parent) must read `Expected: 0, Received: 1`
  with the owner unflipped; the trigger proven to FIRE; dropped + `pg_trigger`/`pg_proc` 0/0; torn down and proven gone.
- **#1263** KS-1140 (Seat L7, LIVE; the round-25 WIDEN, tier 3), head `3c33f936fe3985ab40b72b78bda15a6959448e18`: ONE commit on develop `4db87c3e4b98`,
  comment-only. Tier 3 = through-code only + a PROOF that no code byte changed (the TypeScript emit with removeComments, parent == head, with a
  DIFFERENT control). L7 merges its own PR on a GO.
- **#1264** KS-1281 (Seat L8, LIVE; the second round-25 WIDEN, tier 3), head `2e95121dfc475a09c81d61d61f9a81148b6bb0b9`: ONE commit on develop
  `4db87c3e4b98`, comments only in a PRODUCT file (services/vc-issuer/src/repositories/credentialRepo.ts). The same TIER-3 PROOF. L8 merges its own PR.
- **#1265** KS-1315 (Seat L7, LIVE, tier 2), head `87ef6a1b088754ab773f541ddb273acce8dfab4f`: test-only, four rows in systemTest/performance
  k6DockerRedaction (gate24T2a's N-1244-a fix-shape); red under T-1 (k6_docker.ts's QA-961-1 fallthrough -> `return masked;`). A systemTest/ push: no
  preflight, STOP count NOT APPLICABLE. READY not captured (no id): PR body.
- **#1266** KS-1120 (Seat L8, LIVE, tier 2), head `952f4329de97cd7f94ab6363e670248c456d0a54`: TEST-ONLY (relayed as "a PRODUCT change"; the diff is
  one vc-issuer test file) — X1 (F-1 prefix) and X2 (F-2 DB-miss -> memory get); red under T4 / T5 (tamper_ks1120.py). READY not captured: PR body.
- **FREEZE at seven** (Wednesday: at the next READY or at the pin). At the re-pin exactly four OPEN PRs sat on round-25 branches (#1263-#1266,
  gh_read_5.out) — all in; none excluded.

## The gate MUST (Wednesday's list + the drafter's reads, carried into the prompt)
1. Base-invariant + PAIRWISE checks per PR over develop; there is NO declared overlap. gate24T2c's seven are path-disjoint from all four.
2. #1250 under RULING (a): the four conditions MET / NOT MET, the SIGTERM property, and **no vacuously green signal arm**.
3. #1253 under THE READER RULE through the real guard, each shape's behaviour measured too.
4. #1262's Postgres: port proof with a control, anonymous volume, the red at `33ccff807eb2`, the owner measured (not inferred), 0/0 catalogue, teardown.
5. #1263's and #1264's TIER-3 PROOF (T3-a..T3-e); #1265's K-1..K-4 and #1266's P-1..P-3 red proofs.
6. THE CAP: a NO GO at round 2 ships nothing; the residue is ticketed (named by the gate, filed by Wednesday or a successor).
7. Fleet STOP: claimable for the six Blockchain/Dev PRs BY READ (#1265 NOT APPLICABLE); after merge fixture_guard 12/0 (#1253), run_shell_suites 58/0 (#1250), 60 of 60.
8. MG-3 (KS1127/KS1135 for #1250; KS1293/KS1305 for #1262; #1263's magic word; KS1090 for #1264; KS1111/KS1098 for #1265; KS1020 for #1266), MG-11 (all seven titles <= 83 chars).
9. GO string `GO: merge #1250, #1253, #1262, #1263, #1264, #1265, #1266 batch` (or the subset). Routing `QA/Secuura-batch1250r2`, PROPOSED line
   `QA/Secuura-batch1250r2|coagent@agentmail.to|yes`, NOT written by the drafter.

## LEGITIMATE SHAPES (BRIEF_TEMPLATE §2a) — the PRs that change a CHECKER
"port" = a Python copy of the reader (a READ instrument, never evidence); "live" = the drafter's own run of the REAL code (a PREDICTION). The gate
MEASURES every row.

### #1250 the runner under a signal (live, drafter_trapprobe_g24d.sh -> trapprobe_1.out; 1.5 s after start; suite a sleeps 4 s with a `sleep 30 &` grandchild)
| arm | develop (85920863d704) | round 1 (a01c9943c7a2) | **round 2 (8eef1c4877b3)** |
|---|---|---|---|
| TERM -> pid | rc 143, b not run, no verdict, dir LEFT, suite a ALIVE | **rc 0, b ran, verdict**, dir removed, 2 `No such file` | **rc 143, b not run, no verdict, dir removed** |
| INT -> pid, driver under `set -m` (the suite's own shape) | rc 0, b ran, verdict | rc 0, b ran, verdict | **rc 130, b not run, no verdict, dir removed** |
| INT -> pid, plain `&` | rc 0, b ran, verdict | rc 0, b ran, verdict | rc 0, b ran, verdict (INT ignored on entry) |
| INT -> group, `set -m` (^C) | rc 130, no verdict, dir LEFT | rc 1, b ran, verdict | **rc 130, no verdict, dir removed** |
| TERM -> pid, parent ignores INT | rc 143, dir LEFT | rc 0, b ran, verdict | rc 143, clean |
| INT -> group, parent ignores INT | rc 0, b ran, verdict | rc 0, b ran, verdict | rc 0, b ran, verdict |
| suite a's `sleep 30 &` grandchild after the signal | alive (every arm, every runner) | alive | alive (ORPHAN-ON-SIGNAL, pre-existing class) |

RULE 2 as stated ("bash ignores SIGINT in any background job whatever the parent"), measured: plain `&` — `trap -p INT` EMPTY inside; **`set -m`
then `&` — `trap -- 'echo x' SIGINT` INSTALLED**; INT-ignoring parent + `set -m` — EMPTY. So the suite's INT-to-pid arm (UNREACHABLE by a constant
branch) is PREDICTED reachable and discriminating in its own harness (round 2 OK, round 1 and develop RED).
What a suite sees (live, maskprobe_1.out): under develop's runner `INT installable=yes`, stdin = the caller's pipe; under round 2's `INT installable=no`,
stdin = /dev/null (RUNNER-MASKS-INT, BG-STDIN).

### #1253 cell 9 `c9_scan` (live: the REAL guard 5189cf31a098 with SUBJ_SH at the c2 call site -> readerprobe_1.out; port: predict (f))
| call-site shape | swallows the abort? | named? | cell 9 flags? | reading |
|---|---|---|---|---|
| bare | no | — | no | correct |
| `bf \| cat` / `{ bf; } \| cat` / `` x=`bf` `` / `(` line / `bf &` | YES | round-1 commit + HOLD line | yes | correct |
| **`bf \|\| true`** | no (rc 2) | PR body table, cell 10 text, HOLD line "not flagged" | **yes** | **WRONG** |
| **`false \|\| bf`** | no (rc 2) | cell 12, HOLD line "not flagged" | **yes** (and cell 10 reds, stale ERE) | **WRONG** |
| **`if bf; then :; fi`** / **`bf && :`** | no (rc 2) | PR body table (safe) | **yes** | **WRONG** |
| **`x=$(` / bf / `)`** | YES | class named (`x=$(bf)`) | **no** | **WRONG** |
| **`( : noop` on the line above** | YES | the code comment: the line above "must not OPEN a group" | **no** | **WRONG** (named?) |
| `(` two lines above | YES | DECLARED boundary | no | declared scope |
Every probe run also read 1 FAIL "CONTROL: untampered, from inside a git r…" — the drafter's archive tree is not a git repo (an instrument artefact,
not the guard's).

### #1262 the DB cell (READ)
| property | head | the seat's red at 33ccff807eb2 (b28-1310-BASE.out) |
|---|---|---|
| refusal | DEFAULT_DB must be 127.0.0.1 / **localhost** on 55410-55419; the PLATFORM URL and the earlier describes are not gated | — |
| the red | — | `Expected: 0, Received: 1` at `:658`; the owner assertion `:659` NEVER RAN |
| withTenant( in documents.ts | develop 5 | 0 |

### #1263 (port) — 31 changed lines, all comment lines; comment-stripped text equal; floors `> 1_000` / `> 5_000_000` untouched; Linear link `closes` (MAGIC-WORD-CLOSES).
### #1264 (port) — 13 changed lines, all comment lines; comment-stripped text equal; the files the comment names both create vc_credentials_store (READ); the deployed-grant claim UNMEASURED.
