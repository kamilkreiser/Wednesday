# Wednesday's rulings on the R 33rd draft's OPEN QUESTIONS (draft read lines 1-282, whole)
Source file: fleet/briefs_staged/2026-10-10_seatR33_merge_gate81_DRAFT.md (drafter: Sonnet; unread lines: none).
1. Successor ordinal: if R 33rd wraps with #1444 unlanded, the next merge seat is R 34th, which takes the remaining gate81 row FIRST and then the gate82 rows. R 34th is NOT launched until R 33rd has wrapped. WRAP names "Seat R 34th" as the next seat.
2. Ctx rule: finish to a safe boundary first (a row landed and verified, or M pushed and the STATUS mailed); wrap at ctx >= 56 at that boundary; a merge-in started and not pushed is never left for a successor. Release a row only at ctx <= 55 (Wednesday's pane read).
3. Matcher: add `r 34th` / `seat r 34th` as FOREIGN, plus whichever seats are live on the floor at send (measured by `tmux list-panes`).
4. The npm-ci line and the per-fragment-count line stay NOT required in the GO (as B32).
5. No gate82 landing happens between the two rows, because R 34th is not launched until R 33rd wraps. Develop moves only by R 33rd's own landings unless a human merges (STOP rule stands).
6. The merge-in tool's first run on a no-overlap row is R-4 (no dry arm in ITEM 0).
7. REC32 stays copy-only; its sweep is out of scope.
Open for send: every @FILL@ is read live by Wednesday at send; send_brief requires the RULED BY KAM, NOT YET IN AN ARTEFACT section (decision_queue.sh list ruled --undelivered secuura-).
