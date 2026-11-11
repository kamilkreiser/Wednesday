# notes.md: drafter notes for brief_R100.md (2026-11-12 ~01:4x AEDT)

## Could not measure (the brief's UNMEASURED paragraph carries them)
- Strict apply of rows 38, 40, 41, 42 at develop 4f85ca04c622, and the open-PR / held-READY census for their files: no GitHub call, no patch apply, no suite made by the drafter. Instrument that closes it: the kit's `ready_patch_c2_r100.py`, `census_r100.py`, `census_paths_r100.py`.
- State of PR 2005 (head a968818a0038, the existing ks-1959 branch): ls-remote shows the pull ref exists, which does not say open or closed. Closes it: GitHub pulls API read by the seat.
- vc-issuer test runner, and `measure_testonly` on `.sh` suites beyond row 37: not read.
- GNU vs BSD `grep -x -F`: operator left it unmeasured.
- Gauge, other panes: only tmux pane titles listed.
- The vault: `daily/2026-11-11.md` modified-ness read as one status line; whose lines are in it is not read (the seat reads `git diff`).

## Departures from R 99th's brief, and why
1. Header, GO and stamp block: R 99th's stamp block was Wednesday's; mine is a GO section drawn from the commission (round rule, PACE), saying her stamp wins if added. No SELF-CHECK stamp, per the common rules.
2. Two-round split removed: Wednesday released rows 37, 38, 40 and the addendum rows in one round, so one READY (rows 38, 40, 41, 42 plus 2183 as batch member).
3. Rows 18 to 37 moved to "context only, not yours"; rows 38, 40 kept; rows 41 and 42 added from the addendum mail with sizes read by `ls -l`.
4. Existing-branch warning for row 38 is NEW and not in R 99th's brief or the HANDOVER: origin holds `feature/ks-1959-vc-issuer-revoke-swallows-a-failed-db-update-the-route` at a968818a0038, equal to refs/pull/2005/head. Row 37's old warning is spent (R 99th pushed 2183).
5. Row 36's and 20's items dropped (pushed). TOOL TRAP 1 now mentions bash suites because rows 41 and 42 are bash.
6. Seats updated: B 140th %59, S 57th %56 (commission; panes confirmed in tmux). R 99th's "no board seat live" line replaced.
7. Kam's card for row 42 quoted from `decision_queue.sh show` (read-only after reading its usage text); the go-counts card is carried from R 99th's brief, not re-printed.
8. Kam-rulings key-filter line added (commission), and quoted-heredoc line added to CARRIED.
9. Gate 312: the commission says no verdict yet, but `verdict.md` exists in the gate folder (written 01:36, 37,745 B) with GO / GO WITH NOTES. Reported in UNMEASURED as hers to relay, not folded into any instruction. Wednesday should decide whether to keep or remove that line.
10. Linear keys: 15 keys named in the body each have a provenance line (read-only `ticket_state_r99.py`, run with the project's own key in-process; output not saved). KS-2130 appears only as the cell label's key. Keys in R 99th's brief that this brief does not name (KS-2132, KS-1534, KS-2149, etc.) were dropped, not carried.
11. The drafter's "Wednesday's" attribution for the card ruling: the card text is Kam's; only the reads are mine.

## Checks
- No cd, no write outside this folder (the ticket tool printed to stdout only), no git write verb, no GitHub/mail/Linear write, no .env value printed.
- A grep ending in `cut` appeared once (advisory hook); the lines it showed were presence reads, no absence was asserted from them.
