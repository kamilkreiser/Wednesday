STARTABLE: YES (with one premise correction, Q-1, that changes what the kit builds)

# B710 drafter report (SEAT-H30, HPSM-POC, HPSMPOC-349 open clause)
Drafter: Sonnet 5.5, read-only. Clock from `date`: Mon 26 Oct 2026 07:52:20 AEDT at start. Kit: `2026-10-26_B710_SEAT-H30_hpsmpoc-349-marker-reflow.md`.

## BLUF
1. **The task premise is stale.** The `markerStep` pattern already accepts a trailing comma and a line break at main `b069274c`: `web/src/e2e-runner.test.ts:88` `MARKER_STEP_CALL = /markerStep\(\s*process\.env\s*,?\s*\)/`, with its own row at `:862` (PR #212). Ticket comment 1 already says that half is met. The open clause is the OTHER rows' reflow tolerance (comment 2: "not built; no formatter configured").
2. So the kit builds that clause narrowly: 8 named call-shaped pins hardened as constants (by eye, at least), ONE table-driven reflow row (accepts a wrapped call with trailing comma, refuses a real defect), and a one-line reason for each pin that needs none. One path, no `e2e.mjs` edit.
3. No formatter exists in `web/` (tree 1586 paths, lock file, package.json, eslint config all count 0), so "reflow" is a hypothetical. The B693 gate called it a candidate decision. Default D-1 builds it; Q-1 offers record-only.
4. Origin main `b069274c` re-read (one parent, 0 open PRs, 0 ahead); not yet in the shared clone (seat fetches). Ports 9770-9779 free; no pane or kit names H30 or `b710`.

## Facts re-measured (instrument, control)
- main: `ls-remote` and `gh api -X GET commits/main` both `b069274cfc201bc451ab2c22dc6adc2a6e231bef`; `compare/b069274c...main` ahead_by 0; open PRs length 0. `cat-file -t b069274c` in the clone FAILS (positive control `4e63fc41` prints `commit`). `ls-remote refs/heads/b710*` empty (control `b652*` prints 1). Live `b7*` refs: 7 old names (listed in the kit; the seat classifies them by program).
- The file: raw blob via `gh api -X GET` (Accept raw) saved to the scratchpad; `git hash-object` = `76bc48afcad2f1dc4c07fa25f6a49d136ba5f7c9` = the API's `.sha`; 1070 lines; `readFileSync(path.join(WEB` 8; `toMatch(` lines 69; test openers 99. Control: `NOSUCH-zz7f3a` counts 0.
- Pins not reflow-tolerant (read from the saved blob, line numbers at the base): `:544`, `:546`, `:549`, `:551`, `:436`, `:438`, `:449`, `:458`, `:1002`, `:1006`. Already tolerant: `:88`, `:852`, `:984-985`. I corrected my own first numbers after a count: `webEnvProblems(process.env)` literal appears 5 times (2 `indexOf` reads, 3 inside the `withoutComments` row's fixtures), not 2; the readApi lines are 549 and 551 (I first typed 550 and 552). The kit carries the corrected values.
- Formatter absence: tree `git/trees/main?recursive=1` 1586 paths; pattern `.prettierrc*|prettier.config.*|biome.json*|dprint.json|.editorconfig`: 2 hits, both `api/src/**/Migrations/.editorconfig` (not `web/`); `web/package.json` `prettier|biome|dprint` 0 (control `vitest` 2); lock file `node_modules/(prettier|@biomejs/biome|dprint)` 0; `web/eslint.config.mjs` 20 lines, `prettier|stylistic|comma-dangle|max-len` 0.
- CI predicates read from `ci.yml` at main: `web unit tests (vitest)` `:451` runs `npm test` `:478`; `web build` `:372` runs `npm run lint` `:396`, `npm run typecheck` `:409`, `--check-shards` `:426`. No SQL Server job reads this file.
- Jira (GET, JQL with parentheses): HPSMPOC-349 Backlog, both comments read whole; `text ~ "markerStep"` 349/345/328; `text ~ "reflow" AND statusCategory != Done` 352/349; zero control `zzqxnonexistentphrase` 0.
- Ports: `lsof -nP -iTCP:9770-9779 -sTCP:LISTEN` empty (rc 1); positive control: a python listener on 9771 listed, then freed. Word scan of non-`.pre-` SEAT kits of 25 and 26 Oct for `977[0-9]`: hits in B626, B627, B631, B633, B640, B641, B684, B685. Reading them: the block 9770-9779 was assigned to B627 (Composer, finished) and B684 (H26, HPSM-POC Hosting lane, landed as #219); B684 and B685 name it as "reserved, none needed". Nothing listens now. Panes: `tuesday`, `Datasec/NexusAI-M13`, `Datasec/Security-Composer-G133`, `fleet-monitor`; no H30 and no kit names `H30`/`b710/` (control `H26` hits 1 kit).
- Model: `model-routing.md` line 92 (C2, Sonnet first), gate G2 line 109 (tier 2), G-cap line 111; id `claude-sonnet-5-5` from `models_latest.json` line 23.
- Stamp-slot lines in the kit: 8 (7 slots + last line), `@FOO@` lines 0, as the template reads.

## D-decisions
- D-1: build the reflow clause for call-shaped pins only (constants plus one table row) rather than "record as not wanted". Reason: the task brief asked for a pattern change plus one reflow row, and the ticket's own Done-when offers both exits per row. The kit lets the seat drop a pin it proves already tolerant.
- D-2: the property, not the list, binds ("no code-text pin fails on a meaning-preserving wrap"); the 8 pins are "at least", and a program table classifies every `toMatch/indexOf` site.
- D-3: quote style is NOT widened (no formatter, so quote choice is not a reflow).
- D-4: no `e2e.mjs`/`web/e2e` edit; script and spec reflow mutants live in the `-mut` tree to measure the OLD rows red ("before").
- D-5: gate class round count "NO GO 0 of 2" from B693 line 1 (`#220 GO`) and the B609/B622 GO WITH FINDINGS relayed in the B683 kit.

## Q-questions for Tuesday
- Q-1: build the tolerance (default, D-1) or record "reflow not wanted, no formatter configured" through the records seat and close the clause with no code? Default: build, narrowly as drafted; if the answer is record-only, this kit is not launched and no seat is needed.
- Q-2: should the markerStep half be recorded as already met in the PR body and ticket words? Default: yes (the kit's FOR TUESDAY asks for it).
- Q-3: target READY / hard stop for the stamp. Default suggestion: 2 h / 4 h (one `npm ci`, one full web suite, about 12 single-site mutants, 20 repeats per pool of one file).

## UNMEASURED
No vitest, npm, worktree or mutant run. Not measured: which of the 8 old pins actually fail under a real reflow (the seat's step 4 measures it; a pin that stays green is dropped); whether the `b069274c` web suite count is the gate's 195 files / 2955 tests (RELAYED at the PR head); whether CodeQL flags the new regexes; the 7 old live `b7*` branches were not compared (the seat does it by program); `B708`/`B709` kits did not exist at the read, so PARTITION names those lanes from the task text only.

## Outside-the-fences disclosure
Read: DRAFTER_RULES.md whole, the template kit B683 whole, the sweep file whole, `model-routing.md` lines 92 and 108-111 only (sed), `models_latest.json` lines 20-26, `B693_STATUS.md` lines 1, 45, 101, 159 and 12 (sed/grep), `CLARIFICATIONS.md` line 138 (grep), `ci.yml`, `web/package.json`, `web/eslint.config.mjs`, the file tree and the runner test as raw blobs via `gh api -X GET`. Jira via `.tools/b649/jira.py` loaded with `importlib` from a `python3 -I` script in the scratchpad (`.../scratchpad/b710/py/j.py`); the helper reads the project `.env` in-process, nothing printed. Briefs folder listed by name and word-scanned (read-only). No git ref write, no fetch, no worktree, no HTTP to any hosted site, no mail, chat, Artifact, Docs, `decision_queue.sh`, az, ssh or docker. Two hooks advised case-sensitive greps (zero-risk: all my counts were paired with controls or were positive hits) and one refused an unquoted `=====` (fixed, re-run). I wrote only the kit and this report (plus scratch files in the scratchpad).
