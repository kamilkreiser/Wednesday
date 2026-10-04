# Gateset 2026-10-04_gate54f — README for Wednesday

Drafted 2026-10-04 (work ran ~11:15Z – 11:45Z UTC, times from `date -u`). Every figure below names the kit file it came from.

## 0. What this gate is, and its status

**gate54f is a FAST, T1 gate over ONE Secuura/Blockchain PR: "PR 0", KS-1403, the security-gate unfreeze** (Seat B 56th, author and merger). It changes exactly 4 paths against develop `88e8877a2a0d6a626b9c2a7c4b71d3a909e6f94e`: http-cache-semantics 4.2.0 -> 4.3.0 in the root lock and two service locks, plus two expiring rows in `scripts/audit/audit-baseline.json` (braces -> KS-1403, node-forge -> KS-1404). Pre-push legs 2 / 6 / 7 were refusing every Secuura push. Authority: Kam's card `secuura-freeze5-high-no-fix-1004` = **b** (live board 2026-10-04 21:05:25 AEDT) plus Wednesday's R1-R3 in the B 56th brief.

**Status: KIT COMPLETE, NOT LAUNCHED. Two things are Wednesday's: the routing line (section 4) and the launch (section 5).**

**The PR appeared while the kit was being drafted.** The census (gh_census_ex1.out) found **#1373** open (created 2026-10-04T11:26:11Z, kksecura), head **`d5dccb9f80ee4dbb5bc3d4e46e0a816134a61f91`** on `feature/ks-1403-in-range-lock-refresh-and-two-baseline-rows-b56-1`, base develop 88e8877a2a0d. **The kit still takes PR and HEAD as INPUTS and pins them at launch.** It does NOT pin #1373. Because the head object was already in the shared object store (`git cat-file -t` -> commit), the drafter ran C1-C4 and C6 on it read-only as **PREDICTIONS** (`pred1373_*`). Section 1 has the results.

**What the drafter did and did not do.** It wrote only into this directory. In `/Volumes/DevMASTER/!CODING/` it ran only read verbs: `ls-remote`, `show`, `ls-tree`, `cat-file`, `rev-parse`, `log`, `diff`, `rev-list`, `merge-base`. Every script refuses any other git verb (`lib_gate54f.git`). External reads: GitHub REST GETs (the PR, its files, the open-PR census, one compare inside `--check`); the npm registry (the packument, the two tarballs hashed in memory, and ONE bulk-advisory query POST, which writes nothing). GH_TOKEN was read by name and never printed. Nothing else happened: no launch, no routing line, no mail, no comment, no ticket change, no fetch, no clone, no worktree, no install, no leg run, no delete.

## 1. Drafter predictions on #1373 at d5dccb9f80ee (the gate re-derives each one, at the head it pins)

| check | file | result |
|---|---|---|
| C1 pin | pred1373_c1.out | **PIN PASS 10/10**: both instruments == d5dccb9f80ee; open, not merged, base develop, mergeable True / unstable; ahead 1 behind 0; API files == numstat == the 4 paths (`package-lock.json +4/-2`, `audit-baseline.json +14/-0`, each service lock `+3/-3`); 0 trailers (control bf277eead268 prints 1); only KS-1403 hyphenated on title/body/commit; `Refs KS-1403` present; END_TREE (head tree) `3a55f42e9f84bd7e9d5d28480bb7e68c0321bf4e`, develop tree `d0f0389e1918` (= gate53's END_TREE) |
| C2 lockdiff | pred1373_c2.out | **LOCKDIFF PASS 15/15**: 1 changed entry per lock, 0 added/removed, 0 flag flips, libc 10 -> 10 on both service locks, @types byte-identical, every hunk inside the entry. Root: `version` changed, `resolved` + `integrity` ADDED (allowed only for the root) |
| C3 integrity | pred1373_c3.out | **INTEGRITY PASS 7/7**: the recomputed 4.3.0 sha512 == the builder's == the registry's == all 3 locks; 4.2.0 == the builder's base value; flipped-byte control fires. Advisory query: ch52 `<=4.2.0` (4.3.0 clear), vfj7 braces `<=3.0.3`, 86w9 node-forge `<=1.4.0`, all three MATCHED |
| C4 baseline | pred1373_c4.out | **BASELINE PASS 6/6**: 24 -> 26, added exactly {vfj7, 86w9}, no ch52, 24 old rows equal by value AND raw bytes, +14 lines insert-only, 2026-10-31 cohort 1 -> 3 |
| C6 scope | pred1373_c6.out | **SCOPE PASS 6/6**: 4 paths, 0 test paths (regex control hits 1947 base paths), 0 runtime/manifest paths, 11 instrument files blob-equal, the mobile lock unchanged and still out of scope (KS-769, expires 2026-10-19), modes 100644 (control 100755) |
| C5 legs | — | **NOT RUN BY THE DRAFTER** (it needs a worktree and an install; section 6) |

## 2. Doubts for the GATE to rule (the drafter rules none; all are in the prompt)
- **D1 — the root lock was hand-edited, and the edit is visible in its field order.** The base root lock is STRIPPED: 1617 of 1967 entries have no `resolved`, and the http-cache-semantics entry had only `version` + `license`. At d5dccb9f80ee the entry reads `version, license, resolved, integrity`. Every other entry in that lock with both fields has `resolved` BEFORE `license` (316 of 316, pred1373_c2.out `INFO L6`). The PR body says it "sets exactly the three fields on exactly the one entry", after `npm update` gave 13 collateral changes. The B 56th brief's Q3 said: "never hand-edit the root lock without a ruling". The gate rules METHOD-STATED: was there a ruling, and will the next npm write re-order or re-strip it (cosmetic churn rather than a defect, probably)? The service locks keep npm's order.
- **D2 — the rows carry a fifth key, `decidedAt`.** R2 named `package, reason, ticket, expires`. The 5-key shape already exists on 5 base rows, so C4 passes it and reports `INFO R2-SHAPE DEVIATES`. Polish at most.
- **D3 — PR-BODY-CLAIMS in the reasons.** The braces reason counts "all 40 tracked lockfiles". The repo tracks 45; 40 sit under `Blockchain/Dev`, so the scope is unstated. It says braces is "PROD in 3 (api-gateway, root, mobile/secuura-app)", while Kam's card said "ships in ONE image". These may agree: lock-level PROD is not the same as shipped-in-an-image. The gate says so.
- **D4 — the mobile tree.** `Blockchain/Dev/mobile/secuura-app` still pins http-cache-semantics 4.2.0, braces 3.0.3 and node-forge 1.3.3. Its OUT_OF_SCOPE_LOCKS fuse is `2026-10-19`. After that date it re-enters leg 7's corpus with its own advisories. This is a re-freeze risk outside this PR.
- **D5 — the new fuse.** Both rows expire 2026-10-31, joining GHSA-ggr8. Unless KS-1403 / KS-1404 land first, every push re-freezes that day. Information.
- **D6 — not the gate's:** KS-1403 may have moved itself to In Progress when the PR was created; the usage quota.

## 3. The kit's instruments (each exercised, outputs beside it)
| script | what it does | exercised runs (rc) |
|---|---|---|
| `lib_gate54f.py` | shared helpers; `git()` refuses any non-read verb | imported by all |
| `c1_pin_gate54f.py` | C1 (P1-P6), END_TREE, trailer control | `c1_help_ex1` (0); `c1_shortsha_ex1` (2, refuses a short sha); **`c1_control1369_ex2` (1: merged #1369 fails P2/P3/P4/P6 while the trailer control passes)**; pred1373_c1 (0) |
| `c2_lockdiff_gate54f.py` | C2 L1-L6 + `--selftest` T0-T5 | `c2_help_ex1` (0); **`c2_selftest_ex2` (0, `SELFTEST OK 6 of 6`: base-vs-base 0 changed FAILs; legitimate bump PASSes; dev flip, libc removal 10->9, @types touched, added entry each FAIL and are named)**; `c2_basevsbase_ex2` (1, `CHANGED-ENTRIES … 0`); pred1373_c2 (0) |
| `c3_integrity_gate54f.py` | C3 I1-I4 + `--advisories` | `c3_help_ex1` (0); **`c3_atbase_ex1` (1: I1-I3 pass, I4 FIRES on all 3 locks reading 4.2.0 / ABSENT at the base; all 3 advisories matched)**; pred1373_c3 (0) |
| `c4_baseline_gate54f.py` | C4 B1-B5 + `--selftest` T0-T6 | `c4_help_ex1` (0); **`c4_selftest_ex1` (0, `7 of 7`: +0 rows FAILs; both legitimate insert shapes PASS; ch52 row, a re-escaped `→` (value-equal, byte-different), a wrong expiry, swapped tickets each FAIL on the named check)**; `c4_basevsbase_ex1` (1); pred1373_c4 (0) |
| `c5_legs_gate54f.sh` | C5 `plan` / `parse-selftest` / `run head|base` / `bite` | `c5_help_ex1` (0); `c5_plan_ex1` (0: 3 leg files present at the base, control path rc 128, both gates read AUDIT_BASELINE_PATH); `c5_parse_ex1` (0: a FAIL row counts, a CLEANUP row does not); `c5_refusal_ex1` / `c5_biterefusal_ex1` (2: refuse the shared checkout path before writing). **`run` and `bite` were NOT executed** (section 6) |
| `c6_scope_gate54f.py` | C6 S1-S6 + the NC statements | `c6_help_ex1` (0); `c6_basevsbase_ex2` (1: S1 0 paths); **`c6_control1369_ex2` (1: #1369 fires S1 and S3 on its `package.json`)**; pred1373_c6 (0) |
| `gh_census_gate54f.py` | the API read + open-PR census (gate52's step-2 heredoc, as a file) | `gh_census_ex1` (0; 22 others, 12 overlaps incl. #1373 itself) |
| `fill_gate54f.py` | fills prompt + launcher + `pins_gate54f.json` from launch-time reads | `fill_help_ex1` (0); `fill_stalebase_ex1` (1, STALE BASE); `fill_badargs_ex1` (1, short sha + `-b55-` branch); `fill_sim1373_ex2` (0, SIM files only) |
| `launcher_gate54f.TEMPLATE.sh.txt` | the launcher (gate52's guards, one row, plus exit 9 STALE PIN) | SIM launcher: `launcher_check_sim_ex2` (0, all guards pass); `launcher_stale_ex2` (9); `launcher_wronghead_ex2` (6); `launcher_movedev_ex2` (17); `launcher_notty_ex2` (21: the one run WITHOUT `--check`, stdin /dev/null; it refused at the TTY guard and never reached `exec claude`) |
| `repin_and_launch_gate54f.sh` | the launch action | `repin_help_ex1` (0); `repin_badargs_ex1` (9); **`repin_dryrun_ex1` (0, full dry run on #1373 / d5dccb9f80ee, routing reported missing)**; **`repin_dryrun_wronghead_ex1` (11, a stale head refused)**; `repin_dryrun_census15_ex1` (15: `reported_overlaps` emptied via G54F_REPORTED=control_reported_empty.json -> the 11 overlaps refuse) |
| `prompt_gate54f.TEMPLATE.txt` | the tester's prompt (19 by-name keywords) | filled as `pr1373.SIM.prompt.txt` / `dry*.SIM.prompt.txt` |

All the `*.SIM.*` and `pins_gate54f.SIM-*.json` files are exercise output. They are never launched, and the real `pins_gate54f.json` does not exist until the real launch writes it.

## 4. Routing line — NOT added
Back up the file first. Then add ONE line to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf`, with the PR number Wednesday launches (for #1373):
```
QA/Secuura-pr0-1373|coagent@agentmail.to|yes
```
Until that line is present, step 0 of the launch action refuses with rc 1. The dry run reports it instead (repin_dryrun_ex1.out).

## 5. How Wednesday launches it
```
/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-04_gate54f/repin_and_launch_gate54f.sh <PR> <HEAD-40-hex> [--dry-run]
```
Run it with the PR and head named in the seat's READY (for #1373 as seen in drafting: `1373 d5dccb9f80ee4dbb5bc3d4e46e0a816134a61f91`). Add `WED_USAGE_STOP=…` only with Kam's recorded authority. In one action it does the following:
- (1) reads the PULLS API and runs the census;
- (2) runs ONE `ls-remote`;
- (3) refuses rc 11 unless your HEAD == API == pull/head == branch, the PR is open and unmerged, it is on develop, and the branch is `-b56-1`;
- (3b) refuses rc 10 if develop moved;
- (3c) fills the prompt, the launcher and `pins_gate54f.json` from those reads;
- (3d) re-reads develop and the head;
- then runs the override check, `usage_gate.sh --check`, the launcher's `--check` (which also refuses a pin older than 30 min, exit 9), and `cockpit.sh add`.

**Run it with `--dry-run` first.**

## 6. What I could not adapt, or did not measure
- **gate52's automatic RE-PIN over a moved develop (its step 3b) is not adapted.** gate52 re-ran pin/specdiff/handlers/endtree/fill when develop moved. This kit's expectations are base-blob-specific: 24 rows, libc 10, the exact bump entry, the 11 census overlaps. So a develop move REFUSES rc 10 and is a RE-DRAFT. I did not write a substitute re-measure.
- **gate52's scratch-clone pin (`pin_gate52.py`: fetch into a `--shared` clone, merge-tree/commit-tree END_TREE simulation) is not adapted.** I was barred from fetch/clone/merge-tree, and with one PR whose parent == develop, END_TREE == the head's tree. C1 reads that tree, and the gate re-derives it in its own clone.
- **gate52's 135-control `controls_gate52.sh` suite is not reproduced.** Instead, each instrument carries built-in self-test arms (C2, C4, C5 parse), and the guards were exercised on a SIM fill (section 3). Not controlled: the real-launch usage gate (12), `cockpit.sh add` (14) and the override refusal (16). The census rc 15 path IS controlled (repin_dryrun_census15_ex1).
- **C5 `run` / `bite` were never executed.** They need a worktree plus `npm ci` of `scripts/audit`, and I could neither create a worktree nor write outside this folder. So the drafter has NO leg-6/7 rc at head or base. The base-control prediction rests only on C3's advisory query (all three advisories match pinned versions at the base). Whether leg 6 needs a ROOT install in the tester's worktree to report a non-vacuous tree is unmeasured; the prompt makes the tester say so.
- The advisory database is live. The C3 query reflects 2026-10-04 ~11:25Z.
- No Linear read.

## 7. Re-draft recipe (develop moved, or the change is not this one)
1. Set kit.json `base`, `base_blobs`, `baseline_rows_base`, `locks.*.libc_base` from the new develop (C2/C4 `--selftest` print the base figures), and re-run `gh_census_gate54f.py --json` to refresh `reported_overlaps`.
2. Re-run both self-tests, `c6` base-vs-base, and a `--dry-run`.
