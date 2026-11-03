STARTABLE: YES

# B1217 drafter report (Tuesday's kit drafter, claude-sonnet-5-5), 2026-11-03 15:28 to 15:40 AEDT

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-03_B1217_SEAT-G319_composer-deploy-md-255-gate-tier2.md` (48 physical lines, 21.9 KB; the target of 45 lines is missed by 3, the lines are long; 0 non-ASCII by python `-I`; 7 four-underscore runs = 6 slots + last line, `/usr/bin/grep -o` count 7). Nothing outside the two files was written except scratch under the session scratchpad.

## BLUF
Startable. Tier-2 Sonnet gate of c00b3d49 (one commit on main 2f63b2f6, `DEPLOY.md:255` only). The kit makes the gate answer one question, clause by clause with `b778:line`, and prove each clause with a plant: is the new sentence TRUE of the test. My reading of the test, MEASURED at the head, is that clauses (1)-(4) all look TRUE, with two wording notes (below); the gate's plants are what prove it, my reading is not the proof.

## Facts re-measured (instrument, control)
- `git ls-remote` (READ): head c00b3d49, main 2f63b2f6; `refs/heads/b1217*` none (control: the `b1214/...` ref printed one line). Compare via `gh api -X GET`: ahead 1, behind 0, one file `DEPLOY.md` +1 -1. Commit parent 2f63b2f6, tree ae641ed0. Heavy lock absent (`ls` rc 1). Panes: tuesday, MPS-G318, HPSM-POC-R158, fleet-monitor; no Composer pane. `G319` in non-`.pre-` SEAT kits: 0 (control G318: 1, B1213's). load1 2.77 at 15:32 (`uptime`).
- b778 at the head, raw `contents?ref=c00b3d49` saved to scratch: 1786 lines, blob `2348719aa89d157469705154c6680479f446077a`, 54 `it(` rows (`/usr/bin/grep -c -E '^  it\('`; same 54 as the builder's).
- Pointers (all from `cat -n`/`grep -n` over that raw file): exclamation and backslash row `b778:1658-1665`, asserts `:1660` and `:1661` (`trimEnd().endsWith("\\")`), controls `:1663-1664`; `CHECK_EDITS` `:1292-1347`, 8 entries (key-line count by regex 8), doc comment `:1288` says "five edits" (stale); `expectEditAccepts` `:1395-1409`, once-assert `:1398`; `replacedOnce` `:1383-1389`; the 8 calling rows `:1734-1778`; `runCheck` single-path throw `:443-449`; `b778:666`.
- `DEPLOY.md` at the head: 652 lines; check line = line 203 (the only line naming `PostgreSQL database dump`), Route B fence pair 198 and 209; line 255 holds the new sentence. By python `-I` over line 203: `!` count 0, does not end in a backslash, each of the 8 `was` texts occurs exactly once (control: an absent string 0).
- Round count: the loop over project `*_STATUS.md` (first 3 lines hold `GATE VERDICT`, and a DEPLOY.md/pin-words word) matched 20 files; the pin-words gates are B898 and B918, both GO WITH FOLLOW-UPS round 1 of 2; no NO GO on this class. Control: B1154's file matched the `GATE VERDICT` filter (1). The rest (B620/B633, B699/B707/B736/B755, B787, B1173/B1181/B1197 and the scanner gates) judge other classes. The kit tells the gate to re-run it.
- Jira (read-only, `jira791.py` `J.jql`, every JQL `project = PCOMP AND (...)`): controls `zzqxvbw` 0, `composer` 62. No ticket asks for this sentence: PCOMP-127 says "the sentence at line 255 that the product owner approved is a separate change in the code repo"; PCOMP-113 only locates by line; "exclamation" 0. So the landing files carry no ticket key. PCOMP-99/109 (Done) are the earlier "Nothing else in the command is pinned." tickets.
- Landing rule: `CLARIFICATIONS.md:1799` (C-101, "squash-merges PR #88 pinned to head 2da99cab after re-reading CodeQL and the checks. Nothing is deployed...") and `:1885` (states it as the landing rule); both found by `/usr/bin/grep -n -i`, control `PR #88` (also listed at 2108 etc.).
- Model: G2 `model-routing.md:109`, G-cap `:111`; id `claude-sonnet-5-5` `models_latest.json:23`. Plumbing exists in `P/.tools/b1214/scripts/`: common.sh counts.py dbone.sh dbtest.sh heavy.sh imgbuild.sh prettier.sh (read headers only; holder text at `heavy.sh:24` and `:51`). `prettier.sh` checks `DEPLOY.md` only, so the kit has the gate write `prettier3.sh` for the b616 and b778 files.

## D-decisions
- D1. The kit reads "Nothing else in the command is pinned" in the paragraph's context (lines 222-254 list the pins; "else" = beyond them). Otherwise it is trivially false (the paragraph itself lists six pinned command lines at `DEPLOY.md:238-246`). Q-1 below.
- D2. The "FALSE" test for "Nothing else" is a behaviour-preserving edit of line 203 that still turns a row red, other than the `!`, trailing-backslash and once-only cases; I wrote four such NOT-pinned plants and a 54-row census mapping each row to `DEPLOY.md:222-254` or the new sentence.
- D3. The 8 once-pieces: the plant is a second copy in a trailing comment (` #<piece>`), plus the respelling `&&0==s` for `&&s==0` (piece absent, behaviour equal). Predictions are the gate's to write from source before running.
- D4. Not a fix gate: the sentence is the product owner's wording. A FALSE clause = NO GO with `residue.md` and `card-input.txt`; the gate never rewrites it.
- D5. Heavy budget is small: one image build (cached), a handful of b778 runs, one b616 run, three prettier runs. READY 75 / HARD STOP 150 (suggested, Tuesday's slot S5).

## Q-questions for Tuesday (each with a default)
- Q-1. Accept the "else = beyond lines 222-254" reading? Default: yes.
- Q-2. Should a backslash followed by spaces being red (`:1661` uses `trimEnd`) count as Minor (sentence TRUE but narrower than the test)? Default: Minor, not Major, since the sentence's claim holds and the extra case is a line that ends in spaces after a backslash.
- Q-3. Two wording notes I saw and left to the gate to grade (Note): "the tests hold" in the commit body is plural while only b778 holds the three properties (b616's range is 477-585, RELAYED by B1214, not measured by me); "to prove it" has no clear referent.
- Q-4. Commit author/committer email is `kamil@Kamils-Mac-mini.localdomain` (builder disclosed). A GitHub squash writes the account identity, so the landing files must carry none; the kit checks `localdomain` count 0 in them. Default: land by squash only, as the rule says.
- Q-5. Ports: none assigned or needed (`--network none`). No `lsof`/kit scan was run for a block because none is reserved.

## UNMEASURED
- Everything dynamic: no test, container, prettier, pty or plant was run by me. My statement that all four clauses look TRUE is a reading of `b778:1658-1665`, `:1292-1347`, `:1383-1409`, not a run. b616's scanned range (477-585) and its `:12`/`:14` anchors are RELAYED from the B1214 kit, not re-read. Whether any test other than b616 and b778 reads `DEPLOY.md` is not searched (the builder also did not); the kit does not ask for that search, Tuesday may want it added (default: add a one-line `git grep -n -i 'DEPLOY.md'` over `packages apps scripts` at the head to D1).
- Open PR file lists were not re-read by me (RELAYED from the builder's STATUS; the kit makes the gate re-read them at D5).
- Hosted CodeQL, CI: no PR exists.

## Outside-the-fences disclosure
- Read only: `gh api -X GET` (contents raw, compare, commits) under the project `GH_CONFIG_DIR`; `git ls-remote` in `2_Project_Files`; Jira GETs through `jira791.py`'s `J.jql` / `J.get` in three small scripts I wrote in the session scratchpad (`jq1217.py`, `jq1217b.py`, `jq1217c.py`; no token printed); `tmux list-panes`; `ls`; `uptime`. No `decision_queue.sh`, no `fleet/briefs_staged/`, no scoreboard, no `_ledger.md`, no other client's tree. The raw b778/DEPLOY.md copies are in the scratchpad `x/` folder. The Jira helper's `jira791.py` was imported from the project's `.tools/b791/scripts` (read-only use); it also reads the project `.env` in-process.
