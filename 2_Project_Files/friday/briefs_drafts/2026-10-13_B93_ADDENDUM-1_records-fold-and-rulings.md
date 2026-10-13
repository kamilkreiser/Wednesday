From Friday (laptop seat), Datasec / MPS Commercial Calculator. ADDENDUM-1 to B93 SEAT-R. Same HOLDS as the brief, unchanged.

Friday read your STATUS (RECORDS DONE: records/b93 41359c6…; 25 tickets, 4 commented) and re-read `rev-parse records/b93` = 41359c6bc51a3cbeb88841d3c2bafc783ab63a98, `main` = e9c506392d92d8097e3d58d4d6fd2a841f765358. Accepted. Thank you for the clean "For Friday" list.

SUPERSEDES the brief's "Do NOT fast-forward main / Friday folds later" for this one step only: Friday has no write path into your repo, so the fold is yours.

1. FOLD (your For-Friday item 1, your own steps): stage the root `BACKLOG.md` only after `cmp` shows it equal to `2d4616a:BACKLOG.md`; `git merge --ff-only 2d4616a`; then, from a clean tree, `git merge --ff-only records/b93`. Prove: `rev-parse main` = 41359c6bc51a3cbeb88841d3c2bafc783ab63a98, root `git status --porcelain --untracked-files=no` empty. If any ff refuses or a blob differs: STOP, change nothing, `STOPPED: NEEDS FRIDAY` with the output. Never force, never reset.

2. Friday's rulings on your items 2-4 (record each on `records/b93`'s successor commits on main, as new lines only, never editing existing text):
   - Item 2 (D-5 / E87-4): yes, correct the record. Add a dated sub-bullet under the row carrying ADDENDUM-1 :11's sentence: "Correction 2026-10-13 (B93, Friday): as built and as ruled, a 2-cent move is RED, and a 1-cent move can be RED where references already drift; the 'within tolerance' wording in B85 ADDENDUM-1 :11 is wrong." Cite the three lines you cited.
   - Item 3 (B59 "P-7"): Friday rules it SATISFIED by B73's measurement (`B73_STATUS.md:184`: `reference.json` a regular file, application/json, 725,199 B, outside `/home/data/catalogue-overlay/`), which is exactly the property P-7 asks for. Record that as a BACKLOG sub-bullet on the P-7 / B59 row (or a new `[B93-P7]` row if none), naming B73 as the instrument. Nothing hosted is run.
   - Item 4: ONE new ticket for the user-visible look item "Software / month shows twice" (B84 O-3 / E-5, `B84_STATUS.md:34`, `:130`), read-first as in the brief, label `mpscalc-records-b93` + `needs-ruling` (the fix may change words). Everything else on your item 4 list becomes BACKLOG rows only (one row each, sourced), no tickets.

3. Commit message: `Records: fold B93 to main; D-5 correction, P-7 satisfied by B73, O-3 ticket (B93 ADD-1)`. Re-run your scan on the new range. Read the new ticket back by key.

Last line exactly: `RECORDS DONE: main <sha>; 1 ticket filed` (or `STOPPED: NEEDS FRIDAY` and ONE question).
