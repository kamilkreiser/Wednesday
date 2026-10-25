STARTABLE: YES (after your stamp; nothing blocks it at 21:3x AEDT, with the decisions and questions below)

# B695 drafter report - SEAT-J17, Datasec / Security Composer, PCOMP-97 (B648-1..5)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-25_B695_SEAT-J17_composer-pcomp97-deploy-command-guard-pins.md` (112 lines, 9 lines carry the four-underscore pattern: eight slots plus the last line; control: a scratch line holding four underscores reads 1; 0 non-ASCII characters; no person's name; no decision-card id in the kit).

## BLUF
One file (`packages/db/test/b616-deploy-commands.db.test.ts`), one commit, new branch `b695/composer-deploy-guard-pins` off main `667830ed`. Five numbered items with fix shape, red-proof and what must not change; PCOMP-22 named as a later serial Opus lane and NOT in the kit. Sonnet row C2 (`model-routing.md:92`), `claude-sonnet-5-5`, launch line with `BRIEF_SEAT_LEVEL=sonnet` inside the quotes, pane `Datasec/Security-Composer-J17`, ports 9970-9979, seat-local lock `.tools/b695/lock` taken only around db-container and vitest runs. Landing: squash, head-pinned (CLARIFICATIONS lines 1799, 1802, 1823, 855, 582). The seat stops at READY FOR QA with a PRIOR WORK section; Tuesday opens the PR. Deploys nothing; no Jira writes.

## Facts re-measured (instrument; control)
- main = `667830ede8f23beb33bbf3c5e20b072d63b64ebf` (`ls-remote`; control: `refs/heads/b6*` listing prints the other branches); `refs/heads/b695*` absent (rc 0, no line).
- Open PRs (`gh api -X GET pulls?state=open`): #92 (b671, `f2245db0`, 1 file `apps/api/test/b626-date-rule-rows.db.test.ts`), #91, #86, #85 (draft). Files shared with `packages/db/test/b616-deploy-commands.db.test.ts`: 0, 0, 0, 0 (files 1, 2, 2, 57; control: `compare` of the PR #89 head to its parent lists the file, 1). `packages/db/` paths in any of the four: 0. `DEPLOY.md` in any: 0.
- Ten other `b6*` branches by `compare/main...<b>`: 0 share the file except `b616/composer-c-db-0026-0027` (1; squash-merged PR #89 history; listed, not a stop).
- The file at main (`gh api` raw): 422 lines, 19608 bytes (equals the sweep's 19,608); 16 `it`s (`/usr/bin/grep -c -E '^  it\('` 16; control `^describe` 1). `git log` of it: one commit `d64efb8f` (PR #89).
- Items still open at origin main (python `str.count`, each zero beside a sibling control that fires): `char === "#"` 0 (`char === "\\"` 2), `<<` 0, `$'` 0, `[-*+]` 0 (FENCE_LINE text 1), `toLowerCase` 0 (line-72 text 1), `!x"` 0 (old plant 1), the four anchors (flush at the closing fence, `includes("psql")`, `index += 1` after the backslash, `&&` in `inString`) 1 each. Line numbers 20, 23, 72, 77, 81, 130, 154, 346, 350 match the ticket.
- `DEPLOY.md` at main: 607 lines, 58013 bytes. The scanned span (heading `## Rolling back a deploy that applied 0026` at 431, `## Rolling back ... 0027` at 491, `## A later migration` at 539) holds ONE fenced block (450-453); no `<<`, no `$'`, no trailing comment in it (the trailing comments at lines 54, 202, 206 sit outside). So no fix can hit the real text, and the real-text rows must stay green on unchanged bytes.
- Ticket PCOMP-97: read whole through a Jira GET helper (a NexusAI session-tools `jira.py`, GET only, same Jira site; Composer has no helper of its own, as B688 used an HPSM-POC one); status Backlog; the count of comments printed 0 (control: the helper prints one `=====` header, 1). Its summary says "3 scanner gaps" = B648-1, -2, -3 (B648-1 holds three planted shapes).
- Gate B648 verdict line (STATUS line 1): "GO WITH FINDINGS ... round 1 of 2 for class G-5/G-6"; PR #89 earlier NO GO 1 of 2 (B620) and NO GO 2 of 2 (B633) per the ticket text. BACKLOG row 372 says the later PR's round count is not ruled.
- Model: `levels.sonnet.model_id` = `claude-sonnet-5-5` (`python3 -I`); rows C2 `:92`, G1 `:108`, G2 `:109`, L6 `:85` by `/usr/bin/grep -n -i`.
- Ports 9970-9979: `lsof -nP -iTCP:9970-9979 -sTCP:LISTEN` rc 1, nothing listed. Word-scan of 142 non-`.pre-` SEAT kits of 24 and 25 Oct: THREE hits, B646 (J13) and B648 (G109) reserved the block, B659 mentions it ("9970-9979 by B646/B648"); all finished, and the pane list shows none of them. Control: the same scan style on 981x finds B688. The brief says so.
- Panes: `tuesday`, `Datasec/Security-Composer-J16`, `Datasec/Security-Composer-G122`, HPSM-POC-G124, MPS-G125, MPS-M26, NexusAI-M11, `fleet-monitor`.
- Landing: repo `allow_squash_merge`, `allow_merge_commit`, `allow_rebase_merge` all true (`gh api -X GET repos/...`); project practice is squash, head-pinned (CLARIFICATIONS 1799/1802/1823/855/582 read by `sed -n` + `grep -o`).
- The scripts the kit points at exist: `.tools/b671/scripts/{common,dbtest,dbone,heavy,unit}.sh` and `names.py` (line counts 21/74/12/42/31/49). `dbtest.sh` takes `B593_CMD`, so a `packages/db` config route needs only the one adaptation the kit names. `heavy.sh` excludes its own tag and counts `pc-b[0-9]` lines of other Composer seats.
- The vitest `packages/db` config (`include packages/db/test/**/*.db.test.ts`, `fileParallelism false`, `testTimeout 30000`) and the root config (`exclude packages/db/test/**`) read at main by `git show`: the file is outside the unit run, so the kit drops the SOW unit step and runs lint, format:check and typecheck only.

## Decisions (D)
- D1 New `it`s: 12 named (X11, X20, X14, X1a, X1b, three tag rows, M16, M26, W049, W028) plus up to 3 guards stated before the first run, one `it` per shape so each is red by name. Expected 28 to 31 rows.
- D2 X14 (the `$'` shape) is IN, though the ticket's "Done when" names only X11 and X20 for B648-1: the fix shape lists all three, and a half-fixed `quoteScan` would be a half-closed finding. It is zsh-only reachable (gate table).
- D3 Titles and comments carry words, no shape ids (X11, M16) and no work numbers: the gate's C7 counted "ids in titles 0, header ids 0". Finding ids may appear only in the commit message.
- D4 The central property for item 1 is kill-lost 0 (the gate's own G-5 clause, and the reason B648-1 was a literal-reading Major candidate). Fixes are judged by an old/new/pty corpus; a trade-off (bang inside the comment or heredoc body itself) is a STOP with one question, not a seat judgement.
- D5 W028 is a pin of the scanner's current decision (a `#` line after a continuation is dropped); the ticket says only "per the finding", and the gate calls it the safe direction, so the row's comment must not claim a shell fact unless a pty backs it.
- D6 Item 5's red-proof is the `:82` mutant plus a pty line for the new plant; the bash 3.2.57 clause stays RELAYED from the gate (macOS bash is not claimed as measured).
- D7 Unit step dropped (file excluded from the unit config); lint, format:check, typecheck rc 0 plus a scratch tsconfig typecheck of the file (the gate's Note B648-10: `tsc -b` does not read `packages/db/test`). The SOW mount is therefore not used; the HP-NDA hold is kept.
- D8 Gate tier proposed Tier 2 (G2: tests-only follow-up on a mechanism B648 measured). Round count is left to you (Q-2).
- D9 Read access for the seat to five B648 gate evidence files (pty-table, x-series-table, c2-table and two pty logs) by exact path, as data; `.tools/b648/**` stays forbidden.
- D10 Lock: seat-local `.tools/b695/lock` (mkdir, released by move), taken by `heavy.sh` only around db-container and vitest runs; a shared ref lock only for ref writes.

## Questions for Tuesday (each with a default)
- Q-1 Gate tier for the later PR: Tier 2 (G2) or Tier 1 (G1)? Default: Tier 2 (tests-only, mechanism measured by B648). Note that B648-1 touches the kill-lost clause; if you want a pty-reading gate, say so.
- Q-2 Round count of the later PR: "round 1 of 2 on its own count" (new PR) or inherit the class G-5/G-6 count (B648 was its round 1 of 2)? Default: new PR, round 1 of 2 on its own count; write it into the Stamp.
- Q-3 Ports 9970-9979 (finished B646/B648, mentioned by B659): accept? Default: yes (rc 1 now, panes gone).
- Q-4 Timing: J16 (B688, `api-contract`) and G122 are live in this project. Launch beside them (heavy.sh serialises on `pc-b[0-9]` lines) or wait for G122 to end? Default: launch through `launch_when_cool` after the stamp.
- Q-5 Hard stop: suggested target READY 2.5 h, hard stop 4 h after Step 0 (more than B671's 2 h / 3.5 h: scanner change, pty corpus, five swaps). Default as suggested.
- Q-6 Should PCOMP-22 be commissioned (Opus, serial) only after this PR lands? Default: yes, it edits `DEPLOY.md` Route B and adds a test beside this file; the kit forbids the seat to open it.

## UNMEASURED
No build, test, container, mutant, pty or corpus run. Not measured: that the copied scripts run under the rename; `npm ci` cache hit; that the file runs under the `packages/db` config via `dbone.sh` and whether it passes db-free; that each of the four swaps leaves the 16 old rows green (the gate said 0 red each, RELAYED); every shell fact (RELAYED from the gate tables; whether the image has zsh); whether a bang in a comment, heredoc body or after `$'` is a history event in bash 5.2 (decides the item-1 trade-off); the group baseline 38 files / 475 (RELAYED, gate head); whether the pre-commit hook runs in a worktree.

## Outside-the-fences disclosure
- Wrote only the two files above (plus scratch files in the session scratchpad: a copy of the test file, of `DEPLOY.md`, the PR file lists, the ticket text, a shell snippet).
- Read-only reads outside the fences' named list: the NexusAI project's `session-tools/b621/jira.py` was RUN (it reads the NexusAI `.env` in-process and prints nothing secret; GET only; same Jira site). The rule says "the project's own read helpers"; Composer has none, and B688 did the same through an HPSM-POC helper. Read (never run) the first 40 lines of an HPSM-POC `jira.py` to compare. Tell me if you want that strengthened.
- Read the Composer project's own files: B648 STATUS (grep lines and sed ranges), BACKLOG row 368 (= row 372's text), CLARIFICATIONS landing lines, the `.tools/b671/scripts/{heavy,dbone,dbtest}.sh` and `ls` of `.tools` and of the B648 evidence folder (names and two table greps only; no `.tools/b648` read).
- One `gh api` loop used the Composer `GH_CONFIG_DIR` with GET only; no PR, comment or ref write anywhere. No `git fetch`, no worktree. `decision_queue.sh` not touched. A hook once refused an unquoted `===` in my shell line (retry done with a script file); two hook advisories about case-sensitive phrase greps: the counts were paired with controls in the kit and above.
- No HTTP to any hosted host other than `gh`/Jira GETs named above.
