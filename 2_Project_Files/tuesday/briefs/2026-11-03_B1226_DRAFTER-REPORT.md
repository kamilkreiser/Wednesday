STARTABLE: YES

# B1226 drafter report (SEAT-G323, NexusAI RD-922 tier-1 gate, round 2 of 2, the cap)

## BLUF
Kit written in the shape of B1219 (same 85-line size as the template, not 75: the round-2 mutant list and the round-1 findings table would not fit in less; Q-4). Stamp: 9 four-underscore lines (8 slots + last line), 0 non-ASCII, 0 at-sign tokens. Every pin below re-read at drafting, 2026-11-03 18:39-18:41 AEDT.

## Facts re-measured (instrument; control)
- `ls-remote`: branch 5429e6dd1ca53ad0d1d740b0d4df9514b5f7f2fa, main 0835221808f9007e5b17ec492765af067515edb9, `b1226*` and `b1223*` none (Tuesday's frame: origin refs).
- `gh api compare` main...5429e6dd: ahead 2, behind 0; test +206 -0 (blob cbfe1d0c), clear_db.js +3 -0 (18a96745), counts +3 -3 (649eb44a). `compare` 98b00901...5429e6dd: ahead 1; test +33 -3, counts +2 -2; clear_db.js absent. Confirms Tuesday's claim.
- Raw blob at 5429e6dd: test 206 lines, script 55 lines (`wc -l`), counts file prints tests 5301 suites 316. `git hash-object` matches the three compare blobs.
- Non-ASCII in the test file at the blob: 0 (`LC_ALL=C grep -c` of `[\200-\377]`). The round-1 control (2 hits at 98b00901) comes from the round-1 STATUS, not re-run by me; the kit tells the seat to run the control itself.
- Pointers printed by `grep -n` over the raw blobs: script `:36` await, `:40` VACUUM, `:42 :43`, `:45`, `:47`, `:48`; test `:34 :35 :36`, `:57 :58 :61 :62`, `:80`, `:95-:98`, `:104`, `:117 :119`, `:135 :138`, `:145`, R1 `:146-:181`, R2 `:183-:205`, asserts `:196 :197 :198 :199 :202 :204`.
- Open PRs 0; actions/variables 0; repo-scoped org variables 0; environments ["dev"].
- Lock tool sha256 cf01bafb...971f and fence c16b65f9...0f86 = the round-1 values (shasum). Queue-jest 0 entries. load1 4.22, 209 GiB free (`df -g`).
- Ports 8590-8599: `lsof` rc 1 (nothing listening). Seat scan of non-.pre SEAT kits of 2-3 Nov for G323/B1226/NexusAI-G323: 0 (control G318: 9 files). Panes (`tmux list-panes -a`): tuesday, fleet-monitor, Datasec/HPSM-POC-H112, H111, MPS-G318; no NexusAI pane. `session-tools/b1226` and `worktrees/b1226-*` absent (control: b1219 paths exist).
- model-routing.md `:94` C4, `:108` G1, `:111` cap ("A third round needs Kam's word on a card"); models_latest.json `:17` claude-opus-5-5.
- CLARIFICATIONS.md (2496 lines): `:665` C-68, `:2062` C-190, `:2067` item 2 (never squash), `:2068`, `:2412` C-224, `:2467`, `:2492`. EXPIRING-GRANTS.md line 32 still holds the NOT covered row (grep -n).

## D-decisions
- D1 The round-2 seat gets its own clone/head tree (`b1226-*`); b1219, b1215, b1223 trees are read-only for facts, never run or edited.
- D2 Per-test grading: jest JSON is read per test name so R1 and R2 are graded separately.
- D3 Mutant plan: all round-1 mutants (MA MB MC MD ME MF-plant MG) plus MH now aimed at R2; new R2 mutants MK (exit(1) removed), ML (console.error removed), MJ (success lines before :36, a PLANT if it takes more than one edit), MN (catch prints success); T-series on the test file (T1 trigger never fires, T2 stderr asserts removed, T3 success-line assert removed) to prove each R2 assertion is load-bearing. Predictions are the drafter's reasoning, UNMEASURED; the seat hashes its own before running.
- D4 MB and MC are PREDICTED GREEN on R2 (the BEFORE DELETE trigger fires on the matching row, so the catch still runs); this is the builder's D8.1, not a defect, and R1 catches both. Without this line a gate would wrongly call it a survivor.
- D5 NO GO is FINAL: residue.md + card-input.txt with the question "ship closed instances and ticket the residue, or authorise a third round?" (cap `:111`); no fix commission.
- D6 Round-1 finding table B1219-1..-9 (CLOSED / OPEN / UNCHANGED-NOTE) required in STATUS.
- D7 Landing text on GO: both PR openers, tests paragraph names R2; Build expectation 5301/316; merge-body says nothing deploys; one Opus 5.5 trailer.

## Q-questions for Tuesday (each with a default)
- Q-1 Round-count census must read exactly 1 NO GO on the class (B1219); I read it from B1219's first line only and did not re-run the census (kit orders the seat to). Default: keep the STOP at 0 or 2.
- Q-2 Hard stop 150/240 minutes and absolute latest are left to your stamp (S5); the round-1 absolute latest was 21:30. Default: same 150/240.
- Q-3 T-series edit the test file in the seat's own head tree only (quarantined originals); the round-1 rule "mutants only in clear_db.js" is widened for this. Default: allowed.
- Q-4 Length 85 vs target 75. Default: accept; cutting would drop MK/ML/MJ/MN or the findings table.

## UNMEASURED
Predictions for MK/ML/MJ/MN/T1-T3 and the R2-at-main (N) outcome; hosted Build/CodeQL; node 24; the merge-tree result (fence 3: forbidden for me); round-1 non-ASCII control; the weekday behaviour of launch_when_cool at the stamp.

## Outside-the-fences disclosure
Read: DRAFTER_RULES, the B1219 and B1223 kits, B1219 and B1223 STATUS (grep and slices), CLARIFICATIONS lines by `sed -n`, EXPIRING-GRANTS, model-routing lines, brief_seat.sh header lines 17-24. Wrote scratch blobs t.js, c.js, n.json to the session scratchpad only. Ran `gh api -X GET` under the NexusAI GH_CONFIG_DIR (compare, pulls, variables, environments, contents). One `ls-remote` read. `lsof`, `tmux list-panes`, `uptime`, `df`, `shasum`. No decision_queue, no fetch/clone, no ledger/scoreboard/briefs_staged read, no mail/Artifact/Docs tool. Two files written: the kit and this report.
