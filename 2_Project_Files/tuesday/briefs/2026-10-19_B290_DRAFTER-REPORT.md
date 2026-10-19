# B290 DRAFTER REPORT (2026-10-19, clock from `date`: 19:02-19:03 AEDT)

Brief: `2026-10-19_B290_SEAT-G9_composer-gate-pr81-tier2.md` (same folder). Written with the Write tool only. Ran only reads: `ls-remote`, `gh api` GETs (pulls/81 and its diff), `ls`, `grep`, `lsof`, `date`, `uptime`. No git write verb, no Artifact/Docs/mail/chat, no HTTP to any hosted site.

## What I read
- Template `2026-10-19_B281_SEAT-G8_composer-gate-pr80-tier2.md` whole; `B281_STATUS.md` whole (instruments that worked: FAIL ledger, own `--shared` clone with `DISABLED-no-push`, own mkdir lock, planted byte / U+202E / merge-tree plants, 12-cell compose identity, watcher `docker inspect`, gitleaks canary, secret-scan canary, swap of run order after the load confound).
- `B285_STATUS.md` whole, the B285 brief whole (FORBIDDEN list in THE WORK step 3), `B285_DRAFTER-REPORT.md`.
- The full PR #81 diff (gh GET, 4 files) to ground the claims. Listing of the B92 `addendum6/` kit (existence only; the gate reads `mutants.py` itself).

## Premises and sources
1. Pins MEASURED by `ls-remote` at drafting: main `50d97508105af917ece8307063635f8475773f68`; branch and `refs/pull/81/head` both `33bb703ee8178ec3f48d14993a29daff36eca3e3`. `gh api pulls/81`: open, draft, base `50d97508`, 4 files, +116/-57 (sum of builder's per-file counts: 4+2+3+2+23+6+86+47 added/deleted lines match: +116/-57).
2. `B290` has 0 hits in `briefs/` and the project's `Briefs/` (grep). Port block 7260-7269: `lsof` rc 1 at drafting; I did not check it against other seats' blocks or the pane name (a grep of `briefs/` for `7260|G9` matched older, unrelated briefs; not read).
3. Load at drafting: 9.93 then 5.55 within a minute (swings with HPSM-POC / NexusAI). Brief uses the "below 8" start rule you gave; B281 used 6.
4. Builder facts (RELAYED, from B285 STATUS): the numbers in C-b..C-g (hog 16/20 to 20/20, thresholds, F1-F7, ci.sh 20/20 x2).

## What I put in the gate beyond your rows (flag if you want any dropped)
- **Clock audit (C-d).** In the diff `overGrowth` still times with `cpuMs()` (process CPU, GC helpers included); only `fastest()` (s47) and b20 use thread time. The gate states where each clock sits and whether the split ratio is helper-robust.
- **Blind-spot mutant M-G2.** The new split check compares one 1 MB document with 64 documents of the same entries, so a plant super-linear in the length of a single entry leaves the ratio near 1; only the absolute 250 ms bound can catch it. The gate plants that class and runs the OLD 16 KB / 1 MB test as the control. This is the one place I think the protective intent could actually have slipped.
- **M-G1** is your "milder plant" (about 1.5x, window K swept for a detection edge); **M-G3** is the builder's own admitted b20 miss (about +120 ms).
- Comment-stripped compare as a second instrument beside `docker compose config`, plus the `compose.yaml:121` "no longer pulls anonymously" inconsistency the builder reported (FOR TUESDAY 6) graded as a candidate Minor.
- r7 also compares test case lists from a reporter, and asserts the `build(MB)` attack text bytes are unchanged base vs head ("changing an input" is on the brief's FORBIDDEN list).
- Severity floor stated in the brief (planted mutant green = Blocker; two files not 20/20 under hog = Major; margin under 5% = Minor) so the verdict is not argued afterwards.

## Decisions I made that you may want to change
- **PC_E8_SOW_TEXT:** I wrote it as a PROPOSED ruling carried from B281's, to be confirmed by you at stamp; I did not assert it as yours. Without confirmation the node-step rows are NOT TESTED.
- The hog restart rule (kill by PID at <= 290 s, restart for longer loops) is mine, to close the builder's "hog covered 40% of M3" gap.
- Ci.sh runs once (as you said); the hog is not run over ci.sh in this gate (r5 owns the hog).
- The gate may read the committed B92 kit (`addendum6/`) but not the builder's `.tools/wt-b285*`/`b285/**` (other seat's scratch).
- Heavy rows depend on load; the brief's priority order is r2, r6, r5, r3, r4, r1, r7, r0, r8, r9 and a 20-minute load wait cap.

## Could not measure
Whether the 20x loops plus five mutants plus the ci.sh run fit one session at this machine's load (builder's mutant runs alone took 61-719 s each). Whether CodeQL has run on #81 yet (not queried; the brief tells the gate to say "pending" if so). Pane name / port block collisions beyond `lsof`.

## Slots left (4 tokens on 3 lines, all in the file)
`@SLOT:B_NUMBER_CONFIRM@` (heading; default `B290`), `@SLOT:PORT_BLOCK@` (default `7260-7269`), `@SLOT:STAMP_TIME@` (twice; default your launch time, format `2026-10-19 HH:MM AEDT`). Control: `grep -c` of the pattern on the stamped file must be 0; on the file as written it prints 3 (lines), the `.pre-stamp` copy will print 3 (REFUSE control fires with >= 1).
