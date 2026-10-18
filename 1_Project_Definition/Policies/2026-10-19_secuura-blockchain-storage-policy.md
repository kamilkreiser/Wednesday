---
date: 2026-10-19
type: policy
source: Kam, terminal 2026-10-15 ~15:4x (WED-154), verbatim: "on monday, please create an efficient policy to create more efficient storage of old blockchain files and old tests.  If we do not need them going forward, they can be removed and this can / should be done regularly"
status: APPROVED — Kam ruled card wed-secuura-storage-policy-1019 = a "Approve the policy and the first removal" (live board 2026-10-19 07:24:57). Round 1 commissioned to Seat D (brief 2_Project_Files/fleet/briefs_staged/2026-10-19_seatD_storage_removal_round1.md).
---

# Storage policy: old Secuura/Blockchain (Platform K) files and old tests

**BLUF.** The space is not in old tests (2.7 MB of test output). It is in **git worktrees and the
`node_modules` inside them**: 608 GiB of worktrees under `Blockchain/worktrees/`, 416 GiB of which is
`node_modules`. About **371 GiB** is "not needed going forward" by the predicates below, measured
today on a drive at **91% (178 GiB free)**. Removing it would take DevMASTER to roughly 70%. The
measurement and the tool are Wednesday's, in Wednesday's tree. Every removal inside the Secuura
project is done by the project's own seat (hard rule 1), with counts before and after.

**Evidence:** `0_Brain/reference/2026-10-19_storage-policy/MEASUREMENT.md` (FOUND / TESTED / HOW, per
class) and `dryrun_2026-10-19.md` (every candidate path with size, age and verdict). Tool:
`2_Project_Files/tools/storage_dryrun_secuura.sh`. Its arms are `2_Project_Files/tests/storage_dryrun_arms.sh`:
17/17 on the drafter's full run, and 16/16 fixture-only when Wednesday re-ran them. The tool contains no
removal, move or rename verb and refuses to run if one is planted in it; six planted verbs were refused.

## Classes, predicates, actions

| class | measured 2026-10-19 | "not needed" predicate (all must hold) | action |
|---|---|---|---|
| **W** worktrees + deploy clones | 578 items, 608 GiB | HEAD is in `origin/develop` (ancestor, or every changed file byte-identical in develop = squash-merged) · tree clean · idle ≥ 7 d · not held by a live seat (cwd/lsof) · not touched in 48 h | **remove** (`git worktree remove` by the Secuura seat): the content is in git. **181 items, 200 GiB.** |
| **N** `node_modules` in kept working copies | 107 working copies | not live · idle ≥ 14 d | **remove** (regenerable by `npm ci`, the 2026-09-29 rule). **166 GiB.** |
| **E** regenerable parts of `5_Project_History` | 6 items, 3.9 GiB | `node_modules` or a clean merged scratch clone, idle ≥ 14 d | **remove**. **1.4 GiB.** Records (reports, evidence, mail, HANDOVER, history.md) are **never** candidates. |
| **P** seat scratch (`Blockchain/scratchpad`) | 43 items, 23 GiB | as W/N, idle ≥ 14 d; anything unclassified (pg data, logs) | regenerable parts **remove**; unclassified → **archive to G-DRIVE**, cleared after ~30 d. **0 today** (nothing 14 d old). |
| **R** local-model run clones/caches (Wednesday's tree) | 12 dirs, 18 GiB | `clone/ cache/ work/` inside a run, idle ≥ 14 d, no live process; the run's record files stay | **remove** by Wednesday. **2.9 GiB** today; the 15 GiB A/B run qualifies ~22 Oct. |
| **S** Spark per-round work dirs (Wednesday's tree) | 127 dirs, 42 GiB | today: the runner's own 4 guards (only 1 dir, 0.3 GiB, passes) | **PROPOSED change:** relax guard 3 to "run dir exists AND pid dead AND idle ≥ 7 d" → 42 dirs, 13.9 GiB. Wednesday's tool, Wednesday's change, arms first. |
| **T** test output | 4 dirs, 2.7 MB | untracked · idle ≥ 14 d | remove (trivial). |
| **Unmerged worktrees** | 368 items, 387 GiB | fail the "in develop" test | **KEEP.** A second pass reads each branch's PR state (closed unmerged ≥ 30 d → archive to G-DRIVE, then remove) — needs a Secuura seat's GitHub identity; not measured today. |

**Never in scope, whatever the predicate says:** the main checkout `2_Project_Files`, anything a live
seat holds, anything touched in 48 h, anything unmerged or dirty, `1_Project_Definition`, credentials
(`3_Access_Keys`, `4_Credentials`), records in `5_Project_History`, the brain. The remote boxes
(kintsugi, demo) are **outside this policy**: their images and rollback sets go through the deploy
seat and the 2026-10-07 G-DRIVE archive rule.

## Order of preference (Kam's 2026-09-29 and 2026-10-07 rules)
1. Regenerable (W merged-clean, N, E, R): removed.
2. Possibly useful (P unclassified, unmerged-but-abandoned W): archived to `/Volumes/G-DRIVE/Secuura/Blockchain/archive/<date>_<what>/` with a manifest, cleared there after ~30 d at the monthly review. G-DRIVE: 11 TiB, 67% used.
3. Outright removal of anything else: only on Kam's word, per set.

## Cadence (a mechanism, not an intention)
- **Weekly dry-run** at each weekly consolidation (which `doctor.sh` now checks for lapses). The dry-run writes a dated report, and Wednesday reads it.
- **The removal run** is a Secuura seat's job on a brief that names the report and its candidate list, with `df` and counts before and after, and a 48 h re-check of liveness at the moment of removal. **Once Kam approves the policy, the weekly removal of class W-merged-clean, N, E and T needs no card.** Archive classes and anything new still go to a card.
- A launchd job for the weekly dry-run is OWED (WED tooling). Until it exists, the consolidation ritual is the trigger.

## The sync rule (2026-10-15) still binds
Any archive leg counts every folder on both sides before saying done, and nothing is removed on the
strength of a copy existing.
