STARTABLE: YES (after Tuesday stamps the 7 slots + last line; head and main re-read at the stamp)

# B738 drafter report (G147, round 2 of 2 gate of PR #224, Sonnet G2, browser leg)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-26_B738_SEAT-G147_hpsmpoc-224-round2-gate-tier2.md`. Drafted 13:10 to ~13:40 AEDT 2026-10-26.

## BLUF
Shape copied from the round-1 gate kit (B730), narrowed to: close B730-1 by the gate's own browser measurement at the same cells (plus 1920x1080 and 1366x768, 18 cells), prove the instrument can see the defect by running the same script on the BASE build (a660c5cd), regression-check headers/words/asset bytes, red-at-base/green-at-head for the new rows with five gate-own mutants (g1-g5, g5 tests the helper bound), and a lighter whole-PR pass (Check 7). CI-paused grading is written as a CONDITION (best verdict GO WITH FINDINGS conditional). Round count: NO GO 1 of 2, this is the cap.

## Facts re-measured (instruments)
- `gh api -X GET pulls/224` 13:15: open, head 0413f25c66ea2b61b2fec57672fdc19c04f2c544, base b069274c, commits 2, changed_files 17, mergeable_state blocked; `git/ref/pull/224/head` agrees; main `matching-refs` = b069274c (unmoved). Control for the "17": `compare b069274c...head` files length 17.
- `compare a660c5cd...0413f25c`: ahead 1 behind 0, 6 files, numbers exactly as relayed (+9, +12, +48, +47, +2-2, +1-1 = +119 -3). Matches the relay.
- Check-runs at the head: total 15, completed 15, failure 14, skipped 1 (same pattern as the builder's); analyses for refs/pull/224/head: 4 rows, all commit a660c5c, none at 0413f25 (so "not scanned at head").
- PR #225 open, head 056073b. Open PRs: 221, 222, 223, 224, 225.
- B730 STATUS line 1 read: NO GO, one Blocker B730-1 (logon logo 205-373 px down at 4 of 12 cells). That is the round-count instrument; it reads first lines only.
- Panes (tmux list-panes 13:10): tuesday, HPSM-POC-G145, MPS-M31, MPS-G143, HPSM-POC-G144, HPSM-POC-G141, MPS-G138, fleet-monitor. No G147, no H35. No `.tools/b738` or `wt-b738-*` (ls of `.tools`: b730 b733 b734 b735 and trees).
- Ports: assigned 9560-9569. `lsof -nP -iTCP:9560-9569 -sTCP:LISTEN` rc 1 (nothing). Word-boundary scan `956[0-9]` over non-.pre- SEAT kits of 10-25 and 10-26: 0 hits; control `996[0-9]` hit B722, B733, B734 (scan fires). Did NOT run a bound-and-listen control myself this time (the kit makes the seat run it at Step 0). Rejected 9910-9919 (round 1's block: free but inside the avoid list), 9950-9959 (B736's mention of the J20 block), 9960-9969 (B733/B734 mention it).
- Model: `models_latest.json` line 23 `claude-sonnet-5-5`; routing rows G2 line 109, G-cap line 111 read.
- Stamp-slot count: `grep -c '_''_''_''_'` = 8 lines (7 slots + last); `@[A-Z_]+@` = 0; non-ASCII = 0.
- Landing precedent: CLARIFICATIONS.md:138 (PR #27 squash head-pinned) re-grepped, one hit.

## D-decisions
- D1: Ports 9560-9569 (zero hits; the avoid list given by Tuesday respected).
- D2: Instrument control = run the SAME browser script on the base build; if no cell reads over 200 at base, the round-2 PASS is declared NOT EVIDENCE. This is the single most important guard against a blind instrument.
- D3: 18 logon cells = round-1's 12 + 1920x1080 and 1366x768 on three renders (the builder's table has them; round 1 also failed at 1920).
- D4: Under the pause, no polling for CI completion; best verdict GO WITH FINDINGS conditional. The best-case sentence says the required contexts are not green so branch protection blocks the merge by rule; no bypass language beyond "Tuesday and the product owner decide".
- D5: Mutants g1-g5: g5 loosens the helper's 200 bound to prove the e2e helper measures; g3 (`pt-64`) shows browser rows can fail where the unit row cannot; built mutants limited to two builds if load tight.
- D6: Base tree = a660c5cd (round-1 head), so "red at base" is exactly the round-2 delta.
- D7: Header guard repeated on base AND head (8 rows, identical expected); wide sweep at 4 extra widths, light.
- D8: The Entra demo banner above the logo is a Note (N-F) not a defect: the 200 px line is the earlier kit's number measured with the banner included; product owner decides how he reads "top".
- D9: Time: target 2 h, hard stop 3 h, cap 18:30 (as relayed).

## Q-questions for Tuesday (each with a default)
- Q1: Hash-only read of the logo path again? Default YES (same as round 1).
- Q2: Should the gate run the base-build browser R2/R3 reds (needs a second `next build`)? Default YES; cut order in PRIORITY puts it after 2a/2b/2c and lint/typecheck/build.
- Q3: Is a NO GO on a Note-only reading (N-A, N-F) ruled out? Default YES: written as Notes, never Major.
- Q4: Does Tuesday want the gate to wait for CI if the product owner lifts the pause mid-run? Default NO (kit: no polling; at verdict re-read once; if checks have really run, judge on content).
- Q5: Squash message: two commits fold into one; default Tuesday words it.
- Q6: User-guide refresh list is in FOR TUESDAY (changed pages + screenshot folder). Default: Tuesday re-shoots after deploy, using the gate's screenshots only as reference.

## Things I want Tuesday to see
- The builder deviated from its brief (`pt-6 pb-8`, not `py-8`) on all three renders: the kit tells the gate to judge it as measured (24 px block, 27 px slack worst cell), not as a defect.
- The builder's R2/R3 browser rows are red at base only in 5 of 12 cells (the rest equivalent, builder says); the gate's M1 rule accepts equivalence only if reproduced.
- Round-1 kit wrongly said `smoke.spec.ts` does not exist; the builder corrected it; the new kit lists it (4 tests).
- The PR total numstat is NOT additive (round 2 rewrote lines round 1 added); the kit tells the gate to derive it, no pre-stated number (an early draft said +410 -13; removed).
- Kit text avoids person names and decision-card ids (B### tokens appear as brief ids only).

## UNMEASURED
No npm, build, test, browser, clone, fetch. Not measured: the builder's 27-cell table, the red-at-base counts, the 198/2982 suite, mutant results, lock/heavy helper presence (copied from `.tools/b198` and `.tools/b267` by path as in round 1; I did not re-`ls` those two files), whether Entra renders by hand, the real content of the check-run `output` (I read only counts and names), whether any other open PR's `web/` paths are still 0 (relayed from the builder's 13:0x read), the 10-25 kits' own port blocks beyond the word scan.

## Outside-the-fences disclosure
Read only: DRAFTER_RULES.md, the B730 kit (two pages) and STATUS first lines and grep hits, B735 STATUS, model-routing lines 109-111, models_latest.json line 23, CLARIFICATIONS/CLAUDE grep, `gh api -X GET` (pulls, compare, check-runs, analyses, git/ref, matching-refs) under the project GH_CONFIG_DIR, `tmux list-panes`, `lsof` (no bind control), `ls` of the briefs folder and of the project's `.tools` (names only), grep scans of other kits for port numbers. I did NOT read `fleet/briefs_staged/`, the scoreboard, `_ledger.md`, any card, any WEDNESDAY/FRIDAY tree, any project `.tools/b73x` contents, `HP Reporting and Docs/`, inbound folders. One early shell loop word-split `ls` output when grepping kits for ports (read-only; no effect). No cd, no write other than these two files. One remark on the Bash hook advisory about a case-sensitive grep: used once on my own kit to print a sentence (positive hit shown).
