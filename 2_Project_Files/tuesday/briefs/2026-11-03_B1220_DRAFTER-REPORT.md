STARTABLE: YES

BLUF: kit B1220 for seat C85 (Sonnet, `BRIEF_SEAT_LEVEL=sonnet` inside the quotes) drafted at 71 lines (target 60 missed: the commit-message and moved-main rules are kept whole). One more commit on b1214/composer-deploy-md-255-sentence @ c00b3d49, plain fast-forward push, no PR, replaces only the 250-byte round-1 sentence on line 255 with the product owner's 16:56 option (a) sentence verbatim.

Facts re-measured (16:56-17:05 AEDT, `date` printed 16:56:56):
- origin: main 2f63b2f677b030799cf7f507016fd0d0df59dbaf; branch c00b3d491410586bf10a2e80e3f8b4798b3b583c; `refs/heads/b1220*` none (control: b1170 prints 1). Instrument: git ls-remote.
- Open PRs 91 86 85; `DEPLOY.md` count in each file list 0 0 0 (gh -X GET --paginate). No Composer pane (`%0 tuesday` only). `.tools/b1220`, `wt-b1220-fix`, `composer-heavy.lock` absent (ls rc 1); `.tools/b1214`, `wt-b1214-fix`, `.tools/b1217` exist (read-only to the seat).
- At c00b3d49 (git show | awk): `DEPLOY.md` 652 lines, sha256 begins 6b7d1a9a; line 255 = 291 bytes, round-1 sentence 250 bytes, unique with ` Measured with a throwaway` (count 1). New sentence: 355 bytes, ASCII, `!` 0, backslash 0 (control `a!b\c` 1); new line 255 = 396 bytes (python, computed).
- `b778:1395-1409` expectEditAccepts printed; the accept assertion is :1405. `CHECK_EDITS` :1292-1347, `now:` entries at :1295 1300 1305 1310 1315 1321 1337 1344 (listed by grep), rows call it at :1735-1778. Commit message copy and gate facts are RELAYED from B1217 STATUS/residue.
- Model: models_latest.json:23 claude-sonnet-5-5; model-routing.md:92 (C2) and :109 (G2); brief_seat.sh:24 defaults opus.

D-decisions: D1 plumbing copied from `.tools/b1214/scripts` (that dir has prettier.sh and counts.py; kit copies seven files, not five). D2 push described as a fast-forward of c00b3d49 with no lease flag. D3 gate B1217-2/-3/-5 listed in HOLDS, not built. D4 commit subject adds ", third property" so it is not identical to the first commit.

Q for Tuesday:
- Q1: the third clause says "taking any one of those pieces out", but several `CHECK_EDITS` entries replace a piece with other text (`now:` not empty: :1300, :1310, :1315, :1344), so the clause is narrower than the test's edit. Default: build the ruled sentence verbatim and have the round-2 gate judge it; the kit has the seat report the nine values.
- Q2: commit author will again be `.localdomain` (B1217-6); default: squash writes the account identity, no action.

UNMEASURED: no test/prettier/container run; the new sentence against prettier and b778; whether rows 48-50/52/53 reach :1405 (read, not planted); hosted CI and CodeQL; model-routing row text beyond the cited lines.

Outside the fences: none. Read B1217 STATUS and `B1217_evidence/residue.md` (project files, read-only). Ran `git ls-remote`, `git show`, `gh api -X GET`, `tmux list-panes`, `ls`; no ref write, no card read, no forbidden tree. Stamp slots left as four underscores.
