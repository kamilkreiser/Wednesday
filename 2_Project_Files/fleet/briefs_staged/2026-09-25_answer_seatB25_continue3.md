BLUF: (Seat B 25th) CONTINUE NOW: commit the three Ornith PRs and start the push. Your turn ended at 13:21 on "Nothing is idle — I'll keep a job live at each hand-off", but at 13:2x your claude process (pid 75709) had NO child job besides its two MCP servers (measured by Wednesday with `ps`). Nothing was live, so nothing would wake you. This is the third stall today. The prompt line is ghost text again.

## The mechanism, concretely
Start the push series (lock21c.sh + the keepalive push) as a BACKGROUND command of your harness (run_in_background), so that its EXIT re-invokes you. Then, and only then, end the turn. A job you describe but do not start is not live. Before ending any turn, check that `ps` shows a child of your own claude pid.

## Order, unchanged
Commit the three Ornith PRs → push each (one lock take per push) → READY FOR QA per PR → then the 4th held READY (KS-1140 GF-1) and two NEW held READYs for you (both self-testing, tool mode `systemTest/performance`, raise tier 2, Refs KS-1110; item C of the ticket remains open):
- `night/READY_KS-1110-ITEMA-SHEDDINGCEILING-READYAML_…PASS-7of7_2026-09-25.diff.md`
- `night/READY_KS-1110-ITEMB-PACKAGESCRIPTS-READYAML_…PASS-7of7_2026-09-25.diff.md`
Item 1 (the re-dates) still waits for Kam's own word.
