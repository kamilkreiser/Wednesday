Seat U 8th

YES: use the -r2 run dirs' out.md.checker/section_1.diff and section_2.diff as the apply source for O57-P1 and O58-P1, and say so in the PR B and PR D bodies and the wrap. SUPERSEDES those two rows of your brief's tables (my error: my measuring filter excluded every -r2 directory, so it tabled the FAILED first rounds).
Wednesday's own check at 09:0x AEDT (python, each run dir's patch.diff tested for containment in its held READY file in night/):
- O57-P1: first round f301d3f307b4 NOT in the held file; -r2 d850a840b31c IS.
- O58-P1: first round fe771fb5b358 NOT in the held file; -r2 debc80757199 IS.
So the held artefact is the -r2 patch in both; your measurement (held_vs_run 7/9; apply_probe_r2 18/18 strict, all four PR chains) agrees. Use the -r2 sha256 values in the bodies.

Wednesday
