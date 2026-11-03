STARTABLE: YES

BLUF: kit B1224 for seat C86 (Sonnet, `BRIEF_SEAT_LEVEL=sonnet` inside the quotes, C2 `model-routing.md:92`), 70 lines (target 60; copied the B1220 template whole, the lines are dense; the template was 71). One more commit on `b1214/composer-deploy-md-255-sentence` @ 3c62b959, replacing the 355-byte first sentence of DEPLOY.md line 255 with the ruled 399-byte one.

Facts re-measured (17:30-17:40 AEDT; `date` printed 17:30:17):
- origin (`git ls-remote`): branch 3c62b959ba869de24e23b916f57c75b200d77e3b, main 2f63b2f677b030799cf7f507016fd0d0df59dbaf, `refs/heads/b1224*` none (control `b1170*` printed 1). Commit object exists locally (`cat-file -t` commit).
- DEPLOY.md at 3c62b959 (`git show` to scratch, python `-I`): 652 lines; line 255 = 396 bytes; old sentence 355 bytes, begins/ends as the kit says, old+` Measured with a throwaway` count 1 (unique); rest of line = ` Measured with a throwaway \`postgres:16\``; sha256 begins `ee9cf0eb`.
- New sentence (typed verbatim from the brief): 399 bytes, ASCII, `!` 0, backslash 0, count in the file 0, appears once in the kit (program check); new line 255 = 440 bytes with newline (program: 399 + the 40-byte rest + newline). Six pinned strings: 0 in the new sentence; in the file 1, 8, 1, 5, 2, 1. Control `a!b\c` prints 1 for `grep -c -F '!'`.
- b778 at 3c62b959 (1786 lines): `:666` = `expect(block.checkLine.split(SCRIPT)).toHaveLength(2);`; `:443-449` runCheck, `parts.length !== 2` throws; `:1405` unchanged.
- `.tools/b1224`, `wt-b1224-fix`, `composer-heavy.lock` absent (`ls` rc 2). Plumbing `.tools/b1220/scripts` holds all 7 files. Panes matching `Composer|tuesday`: `%0 tuesday` only. Four-underscore runs in the kit: 8 lines (7 stamp slots + the last line; grep -c counts lines, kit slots are by design). `models_latest.json:23` claude-sonnet-5-5; `brief_seat.sh:24` default opus; CLARIFICATIONS `:1799`, `:1885` both contain `PR #88`. No B1224 file existed before.

D-decisions: D1 commit subject `Deploy guide: say the Route B check line names the script path exactly once` (no key/card/person). D2 expected counts b778 54/54, b616 109/109 and the control plant 44 of 54 are RELAYED from B1220's STATUS. D3 rev-list counts: 3c62b959 is 2 over main, so the new head is 3. D4 plumbing is renamed from b1220 (occurrence counts, not lines, because B1220 hit that fault in `prettier.sh`).

Q-questions for Tuesday: Q1 B1217 `residue.md` was not found at `Briefs/B1217_evidence/residue.md` (my path guess); the kit therefore cites only the B1220 STATUS and does not claim the residue's text. Default: leave as is (the HOLDS list is taken from the B1220 STATUS). Q2 The kit has no gate round count (this is a builder before round 2 of 2). Default: B1222 carries it.

UNMEASURED: open PRs' `DEPLOY.md` file lists (gh not run by me; the seat re-counts at REFUSE 6; B1220 measured 91/86/85 at 17:00); the stamp slots; whether the pane name Datasec/Security-Composer-C86 is free in the live pane list beyond the one `tmux list-panes` read.

Outside-the-fences: none beyond the listed read verbs; no card read, no decision_queue, no fleet/briefs_staged, no ledger. I read B1222's report/kit via `ls`/sed head only to compare ids (briefs dir listing, 12 lines of its report).
