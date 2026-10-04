# gate54f COMMISSION — ONE Secuura PR, "PR 0" the security-gate unfreeze: #`<PR>` KS-1403 (T1, round 1); author and merger Seat B 56th

Drafted 2026-10-04 by the gate54f drafter. This restates Wednesday's commission requirement by requirement. **`<PR>` and `<HEAD>` are placeholders on purpose:** the launch action (`repin_and_launch_gate54f.sh <PR> <HEAD>`) reads both from the PULLS API and `ls-remote` at launch, and fills the prompt and launcher from what it just read. Nothing below is a pin.

## The PR
| field | value | source |
|---|---|---|
| PR | `<PR>` | launch-time input; the drafter's census saw **#1373** open at 2026-10-04T11:26:11Z (gh_census_ex1.out); not pinned |
| head | `<HEAD>` (40-hex) | launch-time input; the drafter saw `d5dccb9f80ee4dbb5bc3d4e46e0a816134a61f91` (ls-remote, 2026-10-04); not pinned |
| branch | `feature/ks-1403-in-range-lock-refresh-and-two-baseline-rows-b56-1` (rule `^feature/ks-1403-[a-z0-9-]+-b56-1$`) | builder's plan; ls-remote agrees |
| base | develop `88e8877a2a0d6a626b9c2a7c4b71d3a909e6f94e` (tree `d0f0389e1918…`, #1369's squash) | ls-remote 2026-10-04 (lsremote_ex1.out) |
| ticket / key set | KS-1403 / {KS-1403}; KS-1404 appears ONLY as file content in the baseline | seat brief R2 |
| tier | T1 (a security-gate unfreeze) | Wednesday |
| merger | Seat B 56th (the author) | seat brief ITEM 1 |
| pane | `QA/Secuura-pr0-<PR>` | kit.json pane_template |
| report dir | `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-10-04-pr0-<PR>-g54f/` | kit.json |
| GO string | `GO (Seat B 56th): merge <PR> on gate54f` | seat brief R3 |
| verdict subject | `[QA -> Wednesday] GATE54F #<PR> (Seat B56 author and merger; T1 security-gate unfreeze: http-cache-semantics 4.3.0 in three locks, two expiring baseline rows KS-1403 / KS-1404)` | kit.json |
| authority for the rows | Kam Kreiser, live board 2026-10-04 21:05:25 AEDT, card `secuura-freeze5-high-no-fix-1004` = **b** (`decisions.json` ruled_ts 2026-10-04T21:06:39+11:00); Wednesday's R1-R3 in `fleet/briefs_staged/2026-10-04_seatB56_successor.md` | read 2026-10-04 |

## The claim (the builder's, NOT re-derived by the commission; the gate re-derives every line)
EXACTLY 4 paths against base develop 88e8877a2a0d:
1. `Blockchain/Dev/package-lock.json`: ONE entry `node_modules/http-cache-semantics` 4.2.0 -> 4.3.0 + resolved + integrity; `node_modules/@types/http-cache-semantics` byte-unchanged.
2. `Blockchain/Dev/services/anchoring/package-lock.json`, 3. `Blockchain/Dev/services/nft-certificate/package-lock.json`: the same 3-field bump; their 10 `libc` arrays each EQUAL to base; 0 dev / optional / devOptional / peer flips.
4. `Blockchain/Dev/scripts/audit/audit-baseline.json`: +2 rows only: `GHSA-vfj7-8cjw-p6xm` braces -> KS-1403, `GHSA-86w9-cpqp-85rv` node-forge -> KS-1404, `expires: 2026-10-31` both; NO row for `GHSA-ch52-4w7c-c8xp`; the 24 pre-existing rows byte-unchanged.
- Integrity (builder, from registry tarballs): 4.3.0 `sha512-M5t5LlJpS1UHMjvwRQVdFHvPISGeLAxNcrWuJkeGh0KxsqCHZ1O3NXZU/8x7cD0BDcGW8kapxMKTvwlqrNkHkA==`; 4.2.0 (base) `sha512-dTxcvPXqPvXBQpq5dUr6mEMJX4oIEFv6bwom3FDwKRDsuIjjJGANqhBuoAn9c1RQJIdAKav33ED65E2ys+87QQ==`.
- The refusing legs: 2 `scripts/preflight/lockfile-cleanroom.sh`, 6 `scripts/audit/audit-gate.mjs`, 7 `scripts/audit/audit-locks.mjs` (all present at the base; both gates read `AUDIT_BASELINE_PATH`, audit-gate.mjs:46 / audit-locks.mjs:64 — c5_plan_ex1.out).

## What the gate must rule (by name; the tester runs each in its OWN scratch clone / worktree, never the builder's; rc on its own line; a control that can fail)
- **C1 PIN** (`c1_pin_gate54f.py`): PR head == `<HEAD>` by ls-remote AND the API; base == develop at origin; OPEN; files == exactly the 4 paths by API /files AND numstat; ahead 1 / behind 0; 0 trailers (control `bf277eead268` prints one); only KS-1403 hyphenated; `Refs KS-1403` line; END-TREE (head tree) and MODES (100644, control run-migrations.sh 100755).
- **C2 LOCKDIFF** (`c2_lockdiff_gate54f.py`): all 3 locks vs the base blob, entry and field level: exactly 1 changed entry each, fields version/resolved/integrity only, 0 added/removed, 0 collateral, libc count == base (10) on each service lock, @types/http-cache-semantics byte-unchanged; `--selftest` plants a dev flip and a libc removal (+ @types touched, an added entry) and must report each; base-vs-base must read 0 changed.
- **C3 INTEGRITY** (`c3_integrity_gate54f.py`): sha512 recomputed from the 4.2.0 and 4.3.0 registry tarballs, matched to the locks; negative control (the other version, a flipped byte).
- **C4 BASELINE** (`c4_baseline_gate54f.py`): exactly +2, shapes/keys match existing rows, expiries 2026-10-31, tickets KS-1403 / KS-1404, no ch52 row, 24 old rows byte-equal; `--selftest` arms.
- **C5 LEGS** (`c5_legs_gate54f.sh`): legs 2/6/7 at HEAD rc 0 each; BASE CONTROL legs 6+7 at 88e8877a2a0d rc 1 naming all three advisories (rc 2 = SKIP, not pass); BITE: removing each new row alone reddens leg 6 or 7; no-op control.
- **C6 NOT COVERED** (`c6_scope_gate54f.py`): no runtime change; secuura-test-discipline §4 exemption (0 test paths, must-hit control) checked; §5f NOT APPLICABLE / NOT COVERED with reason; `Blockchain/Dev/mobile/secuura-app`'s lock is out of gate scope (KS-769) — stated.
- Plus METHOD-STATED and PR-BODY-CLAIMS (doubts D1-D5, README section 2), COLLISION-CENSUS, NOT-TESTED-LIST, TIERING, DISK-ENOSPC, REPORT-HASH-LAST.
- **Verdict format:** GO / NO GO; per check FOUND / TESTED / HOW; what was NOT tested. Findings only: the tester never fixes, never comments on tickets, never merges.

## GO
The GO string, as the GO mail's SUBJECT: `GO (Seat B 56th): merge <PR> on gate54f`. Seat B 56th merges on it, head pinned; the landed tree must equal the gate's END_TREE.
