# Internal tooling screen — 160 Secuura tickets (Linear project 'Internal tooling', team KS)

Written 2026-10-05 18:34 AEDT (`date`) by a screener / Spark brief-writer sub-agent for Wednesday, after Kam's 18:14 ruling
on the live board: "run cloud and local agents as hard as possible to action these".
Base: develop `46c3e20cfbd21acee0c67d544180c33deaa4c8ef`, read with `git ls-remote origin refs/heads/develop` using the Secuura
checkout's own `core.sshCommand` at 18:16 AEDT. Code was read in a `--shared` scratch clone at that SHA. Nothing was written to
`!CODING`, Linear or GitHub.
Row data: `screen.tsv` beside this file (header + 160 rows; columns: id, title, state, family, files, class, reason).

## BLUF

**Ticket set.** 160 tickets, measured: a Linear GraphQL read-only pagination of `project(1dab6a9f-…){issues(first:50)}` ran
4 pages until `hasNextPage=false`, returning 160 nodes and 160 unique identifiers. States: In Progress 101, Backlog 58, Todo 1.

**Class counts.** Computed by `awk -F'\t' 'NR>1{print $6}' screen.tsv | sed 's/:.*//' | sort | uniq -c` after the last edit:

| class | n |
|---|---|
| ALREADY-DONE? | 60 |
| CLAUDE-LANE (31 directory families) | 50 |
| NEEDS-KAM | 32 |
| BLOCKED-BY-LIVE-SEAT | 11 |
| NEEDS-HUMAN | 4 |
| SPARK | 2 |
| ORNITH | 1 |
| **total** | **160** |

**Headline.** The most work sits in **ALREADY-DONE? (60)**. A board seat can clear these by reading the cited file:line and
merge, then sweeping and closing; none of it is a build. Claude-sized work is 50 tickets. Local-model-sized work is small: 3
tickets plus 1 carve. Most of this estate consists of residues of gated PRs whose fixes already landed.

### Proposed Claude lanes (4)

The lanes below are pairwise file-disjoint, disjoint from the live seats, and disjoint from the queued Spark files. Measured:
the `files` sets of every lane ticket and the three queued Spark briefs were intersected pairwise by a python check over
`screen.tsv` (0 overlaps; 0 hits against the live-seat path list; positive control `{'x'}&{'x'}` was truthy).

| lane | directory family (files) | tickets |
|---|---|---|
| L1 | `Blockchain/Dev/scripts/run-shell-suites.sh` + `scripts/__tests__/run_shell_suites.test.sh` (+ a NEW PTY harness) | KS-1330 → KS-1331 → KS-1325, in that order. Develop's runner has no trap at all, so 1330's signal handling lands first. |
| L2 | `Blockchain/Dev/scripts/preflight/preflight.sh` + `scripts/run-code-guards.sh` (verdict/tally work; NOT `.githooks/pre-push`) | KS-1127 (leg 14 skip tally in the closing verdict), KS-1153 (R-925-A TAB tail `:173`, F-925-4 double-count) |
| L3 | `Blockchain/Dev/services/auth/src/__tests__/` named files only: `ks431-oauth-app-update.test.ts`, `ks949-platform-admin-seed-identity.test.ts`, `ks963-preauth-rethrow.test.ts` | KS-825 (non-deterministic auth green), KS-1053 (ks949 seed flake), KS-1131 (ks963 regex/positional items 3-4; test-only, but on the reset-token surface, so not Spark) |
| L4 | `Blockchain/Dev/scripts/audit/*.mjs` + `scripts/preflight/lockfile-cleanroom.sh` (CORRECTED 2026-10-05 20:5x: `scripts/lockfile-cleanroom.sh` does not exist at develop f01c1da5717f, per Seat G 1st's `git cat-file` 09:36Z) | KS-829 (baseline `scope` validation), KS-1209 (lock-discovery "missing expires" polish), KS-1394 (audit-locks regen pointer) |

Lane caveats:
- **L3:** Seat E 3rd owns auth `routes/oauth.ts` / `mfa.ts` / `users.ts`. L3 touches only the three named test files. Whether
  Seat E's own PR edits any of those three is **UNMEASURED** (Seat E's diff was not read). Check it before launch. KS-1017
  (an auth test-estate class sweep, `*.test.ts`) is kept OUT of L3 for that reason. Run it after Seat E lands.
- **L2 vs pre-push:** KS-1292 / KS-1300 / KS-1332 (family `.githooks+scripts/preflight`) also need `.githooks/pre-push`. KS-884
  (pre-push qualified refs) is a held Ornith READY waiting on a Kam card. Those three go in wave 2, after the KS-884 decision,
  so two writers never meet in the hook.

Wave 2 lanes, file-disjoint from L1-L4 but not proposed now:
- `scripts/credential-guards`: KS-951, KS-967. Credential surface.
- `scripts/preflight(root-derivation)`: KS-902, KS-903. KS-902 touches `no-tracked-credentials.sh`, which KS-967 also touches, so run it after that lane.
- `tests/e2e`: KS-1038, KS-1039, KS-1113. Needs a live stack.
- `services/originate/tests(integration)`: KS-1311, KS-1340. Needs a disposable Postgres. Originate is Seat B's service, but these are different files.
- `systemTest(url-pathname)`: KS-1337, KS-1347.
- `services/api-gateway/tests`: KS-1237, KS-1259. KS-1237 X-MSG-MEMBER has a golden-passing brief parked at `night/briefs/split_1237msg`, with both local rounds spent.
- `docs(md)`: KS-965, KS-1320, KS-1343.
- Singletons: KS-784, KS-851, KS-957, KS-987, KS-998 items 1-3, KS-1014, KS-1076, KS-1090, KS-1137, KS-1145, KS-1154, KS-1156, KS-1158, KS-1159, KS-1274, KS-1316, KS-1319, KS-1328, KS-1405.
  - KS-1274 is not Spark-able: all three sibling trivy suites use bare `{}` as their clean-image stub, so the one-line fix reds them too.
  - KS-1316 needs a round-2 QA gate on the open PR #1268, not a build.

### Local-model candidates, easy → hard

ORNITH count = **1**, from `screen.tsv` class `ORNITH`: KS-865. Nothing was queued for Ornith (server down, queue paused until
06:00 by design). KS-998 item 4 is also Ornith-shaped (one token, one edit point), but its ticket row stays CLAUDE-LANE
because items 1-3 remain.

| # | ticket | class | shape | Spark brief | queued? |
|---|---|---|---|---|---|
| 1 | **KS-865** | ORNITH | `scripts/check-no-latest-tags.sh:17` header still advertises the removed `deploy-staging.yml`. One hunk, one line replaced, plus a NEW bash suite. | `KS-865-header-lists-checked-files` | **yes** |
| 2 | **KS-998 item 4** (carve) | CLAUDE-LANE row; carve is Ornith-shaped | `systemTest/scripts/check-package-format.sh:180` `grep -qx` → `grep -qxF`, one hunk, plus a NEW bash suite | `KS-998-format-gate-grep-fixed` | **yes** |
| 3 | **KS-1164** follow-up | SPARK | test-only: a NEW vitest cell pinning `gate/report.ts:104` `toLocaleString()` grouping; tamper `→ String(...)` | `KS-1164-locale-count-cell` | **NO, harness gap** (below) |
| 4 | **KS-1136 item 2** | SPARK | `Blockchain/Testing/jobs/09-aggregate-report.sh`: ONE inserted 13-line loop, so every non-04 artefact that does not parse emits `<job>/unreadable-artefact` high; plus a NEW bash suite | `KS-1136-aggregate-unreadable-artefacts` | **yes** |

Measured red/green, from each brief-writer's scratch clone at 46c3e20cfbd2, bash 3.2.57 / node v24.7.0:
- **KS-865:** new suite at tip 3 pass / 2 FAIL (rc 1); with golden 5/0. Sibling `check_no_latest_tags.test.sh` 7/0 on both sides.
- **KS-998:** new suite at tip 5 pass / 3 FAIL (rc 1); with golden 8/0. On both sides: `package_format_gate.test.sh` 33/0, `pre_push_hook_base.test.sh` 28/0, `pre_push_hook_current_develop.test.sh` 4/0.
- **KS-1136:** new suite at tip 3 pass / 3 FAIL (rc 1); with golden 6/0. On both sides: `aggregate_report_trivy_artefact.test.sh` 5/0, `orchestrate_jobs.test.sh` 18/0.
- **KS-1164:** tip 3/3 green. Under the tamper, 1 FAIL / 2 pass, by assertion. The shipped KS-704 suite stays 4/4 under the tamper, which reproduces the gap. With `LC_ALL=C` the new file is still 3/3.

Verified by this writer, not only by the forks:
- `git apply --check` of each `golden.diff` in a scratch clone at 46c3e20cfbd2: rc 0 ×4.
- `round.sh <dir> --dry-run` re-run on all four: rc 0 ×4, each `DRY-RUN OK — … input built at 46c3e20cfbd2`.

**KS-1164 harness gap, the reason it is not queued.** In `tool=systemTest/performance` mode, `prepare_clone.sh` farms node_modules
from `<source>/systemTest/performance/node_modules`. The round's source is `spark/cache/src`, and `round.sh` links node_modules
for `Blockchain/Dev` only. Measured at 18:3x: `ls spark/cache/src/systemTest/performance/node_modules` → "No such file or
directory", while the `!CODING` checkout has one. A real round would therefore end HARNESS rc 5 at prepare. The dry-run cannot
see this, because it never reaches prepare. Fix, which is Wednesday's call and harness-owned:
`ln -s "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/systemTest/performance/node_modules"
spark/cache/src/systemTest/performance/node_modules`, or teach round.sh to link it when `tool=` is pinned. After that, append
`KS-1164-locale-count-cell` to `spark/queue.md`.

### Reclassified at brief time (counts above already include these)

- **KS-884** SPARK → NEEDS-KAM. Wednesday holds it out of Spark (`0_Brain/tasks/NEXT-PICKUP.md:751`: ".githooks/pre-push = gate
  wiring: card it to Kam"). A held Ornith READY exists (`night/READY_KS-884_…_2026-09-16.diff.md`). The defect is still live at
  `.githooks/pre-push:165`.
- **KS-1250** ORNITH → NEEDS-KAM. The ticket offers two fixes (honour `SMOKE_BASE_URL`, or fix the runbook). Wednesday records it
  as irreversible-class (`0_Brain/tasks/EXPIRING-GRANTS.md:54`, `:68`), because a full run against a named gateway POSTs a
  document (`smoke-test.sh:186`) and anchors it (`:208`). A held Ornith READY exists (2026-09-18, made at `207716440`), and it
  needs a re-apply check at develop.

## The other classes (ids; reasons with file:line in `screen.tsv`)

- **ALREADY-DONE? (60).** A board seat verifies the cited line/merge and closes or sweeps:
  - KS-789 811 872 887 890 896 897 910 911 912 928 944 947 958 980
  - KS-1011 1034 1037 1040 1045 1047 1049 1073 1089 1097 1110 1111 1117 1118 1133 1135 1139 1140 1142 1143 1144 1147
  - KS-1155 1179 1181 1192 1199 1217 1229 1260 1261 1266 1273 1277 1279 1288 1291
  - KS-1293 1294 1296 1298 1299 1301 1306 1312

  Several still owe a LIVE sweep rather than code: KS-1139 (bash ≥ 4.1 plus a real Key Vault), KS-1296 (a rebuilt stack), and
  KS-1306 (the INSERT path on a database).
  Points a closing seat should check:
  - KS-811: its folded POST /api/documents half reads Seat B's `documents.ts`.
  - KS-911: the launcher has changed since the gate; the F2 redirect was not re-located.
  - KS-1181: the ks727 header `:20` still says "if a count below is wrong, a test is red".
- **NEEDS-KAM (32).** KS-785 837 846 884 925 939 940 955 956 964 1000 1010 1033 1036 1051 1081 1085 1088 1138 1141 1146 1148 1188
  1250 1290 1305 1313 1314 1317 1324 1326 1351. The usual reasons:
  - the ticket says "decide whether" or "fix shapes not chosen";
  - a `.github/workflows` edit, which is Kam-class, on retired Actions;
  - an open NO-GO-at-cap PR waiting on Kam's disposal (KS-1313/1326 on #1245, KS-1314 on #1278);
  - launcher edits "not while two seats are live" (KS-939/940).
- **NEEDS-HUMAN (4).**
  - KS-1035: a maintainer dismisses stale GitHub approvals.
  - KS-1082 and KS-1098: Peter's decisions.
  - KS-1378: code merged `2cb858335472`; only a live mail sweep is left, and deploys are on hold under KS-1379.
- **BLOCKED-BY-LIVE-SEAT (11).**
  - Seat B: KS-836, KS-930, KS-937, KS-1152, KS-1267.
  - Seat E: KS-838, KS-1180, KS-1185, KS-1193.
  - Seat F (`migrations/__tests__`): KS-1030.
  - KS-808: its only open defect is the already-held Spark pass `KS-808-applied-counts-skips` (PASS 16:34).

## UNMEASURED — stated rather than glossed

- **Open-PR state from GitHub was not read.** "No lane" judgements rest on ticket comments, `git ls-remote` branch heads
  (737 heads), and git ancestry of merges, not on the GitHub PR list.
- **ALREADY-DONE? rows rest on reading code and git ancestry/logs at 46c3e20cfbd2.** No suite was run for them.
- **Spark candidates:** no `--control` round was run (the golden has not been through the Spark checker), and no model round.
  The goldens were measured by hand (red at tip, green with golden) in scratch clones.
- **Classification depth.** Each of the 160 tickets was read in full (description plus all comments, oldest first) by one of
  five screening sub-agents, 32 tickets each. This writer spot-checked their rows, not every row.
- **Seat E's diff was not read** (affects L3).

## What was written

- this file, plus `screen.tsv`;
- `local-model/night/briefs/{KS-865-header-lists-checked-files, KS-998-format-gate-grep-fixed, KS-1136-aggregate-unreadable-artefacts, KS-1164-locale-count-cell}/`, each holding `KS-<n>.md`, `golden.diff` and `spark.pins`;
- three lines appended to `local-model/spark/queue.md`: `KS-865-header-lists-checked-files`, `KS-998-format-gate-grep-fixed`, `KS-1136-aggregate-unreadable-artefacts`.

`queue.sh` was NOT started; `pgrep -fl spark/queue.sh` → rc 1, none running. Spark's `round.sh --dry-run` wrote only
`spark/state/dry/*` and refreshed the cache. Scratch work, the clones and per-batch notes, is in the session scratchpad
`its/`.
