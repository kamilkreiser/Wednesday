STARTABLE: YES

# B1219 drafter report (SEAT-G320, NexusAI RD-922 tier-1 gate, round 1 of 2)

## BLUF
Kit written in the B1201 shape: REFUSE 1-8, C1-C8, MAIN-MOVED RULE, GRADING, RULE L, VERDICT, LANDING, 8 stamp slots + last line (9 four-underscore lines, control reads 9; at-sign tokens 0; non-ASCII 0). It is 85 lines, not 70: lines are long; the cut would have been the tier-1 rigour you asked to keep. Drafted about 16:35-16:45 AEDT 3 Nov 2026 (`date` at 16:33:57 for the first read).

## Facts re-measured (instrument; control)
- Refs: `ls-remote` branch `98b00901...`, main `08352218...`, `b1219*` none; `compare` ahead 1 behind 0, files exactly the 3 paths, +176 / +3 -0 / +3 -3 (`gh api -X GET compare`; the same command's file list is the control that it prints 3 rows).
- Head blobs by `git hash-object` over raw reads: test `624022d1` (176 lines), script `18a96745` (55 lines; new DELETE `:36`, VACUUM `:40`, success `:43`, close `:45`; test `:140` one `test(`, `execFile` `:113`, `readdirSync` `:132`). Test file has 2 non-ASCII lines (`grep '[^ -~]'` count 2).
- Commit message read whole via `git/commits` GET; kit asks TRUE/SHORT/FALSE per sentence.
- Round census (`python3 -I`): 129 STATUS, 44 verdict lines, 8 NO GO, class hits 0 (control scratch line counts 1). Round 1 of 2.
- Deploy: `deploy-demo.yml` blob `597b3487` at main, lines `:26 :27 :28 :29 :33 :53 :91 :95` printed by `awk NR`; variables 0, org variables 0 (repo endpoint), environments ["dev"], open PRs [].
- `CLARIFICATIONS.md` 2496 lines; `:665 :2062 :2067 :2068 :2076 :2412 :2467 :2492 :2494` printed by `awk NR`. `model-routing.md :94 :108 :109 :111` printed; models_latest line 17 = `claude-opus-5-5`; grant line 32 text printed.
- Seat: `G320`, `B1219`, `NexusAI-G320` whole-word in non-`.pre-` 2/3 Nov SEAT kits: 0 (control `G318`: 4). `session-tools/b1219`, `worktrees/b1219-clone` absent; project uses `session-tools/` (`.tools` absent). Ports 8590-8599 free (rc 1, control `:7000` rc 0); no port needed. Lock and fence sha256 equal to B1201's. Disk 213 GiB; load1 6.51.

## D-decisions
- D1 Scope TABLE ONLY; the absent JSON wipe is a Note, never a defect; C7 grades the builder's D8 pointers TRUE/SHORT/FALSE (a FALSE claim about the JSON stores = Major).
- D2 Mutant MD (statement after VACUUM) and MG (duplicate) predicted GREEN on R1 (row counts identical); kit has the gate prove it with `freelist_count` and grade Note, because the cell cannot see file size. I judged this the honest shape; flag if you want it Major.
- D3 MF (swallowed misspelled table) is written as a PLANT (two edits), not a one-input mutant, to keep the C4 property.
- D4 Probes run the script only on trees built by the gate; REFUSE 8 added (hash of repo `data/` before and after).
- D5 No listener, no port block (cell is in-process).

## Q-questions (each with a default)
- Q-1 Builder trees `worktrees/b1215-n95`, `session-tools/b1215` read-FORBIDDEN, as B1201 did for its builder. Default: forbidden (the gate builds its own).
- Q-2 Target 150 / hard stop 240 minutes as B1201. Default: yes; pick the absolute latest time at stamp (load1 was 6.51, verify takes 24-26 min per the builder).
- Q-3 Landing text mentions the product owner's 3 November 2026 ruling by date (no card id, no name). Default: keep.
- Q-4 Trailer `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` copied from B1201 (matches the builder commit's trailer). Default: keep.

## UNMEASURED
Organisation-wide variables beyond the repo-scoped endpoint; Jira content (the kit's PRIOR WORK is the gate's; I used the builder's quote of the Done-when, not my own GET); whether `gh pr` merge flags still behave as in B1201; hosted Build/CodeQL; load at launch; whether R1 is red at main for the stated reason (the builder's claim, the gate re-runs it).

## Outside the fences
None. Read-only: gh GET (compare, git/commits, contents x3, variables, org-variables, environments, pulls), `ls-remote`, `lsof`, `tmux list-panes`, Python filesystem census of STATUS files, reads of listed docs. Scratch files in the session scratchpad only (raw copies of two head blobs and `deploy-demo.yml`). No decision card read. A mid-draft edit of the brief (removal of a literal at-sign token that tripped its own REFUSE 1 check) is the only change after first write.
