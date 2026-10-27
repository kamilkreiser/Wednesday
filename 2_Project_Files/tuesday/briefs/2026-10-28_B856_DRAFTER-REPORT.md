STARTABLE: YES (main f4ea31c9 re-read, open PRs 0, no b856 ref or tree, pane M50 and ports 9870-9879 free; one flag: B855 shares the jest lock and the repository but no path)

# B856 drafter report (kit for Datasec/NexusAI-M50, NexusAI RD-898: exact bad-row label and padded and accented valid-level rows, test only)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-28_B856_SEAT-M50_nexusai-rd898-exact-label-pins.md` (119 lines; 9 four-underscore lines, the eight Stamp slots plus the last line). Shape copied from the B849 kit (same section order, same STATUS-NOW, same launch-line form through `launch_when_cool.sh`, no nested `cockpit.sh add`).

## BLUF
- The lane is ONE file: `__tests__/rd892-testing-dropdown-null-level.test.js` (234 lines, blob `e266ef36`, read whole). F1's line 191 `toMatch(/^[\s[\]]*$/)` becomes an exact `toBe('[] ' + condition_text)` for all five rows; D1 and D2 gain a padded and an accented valid-level row through their own extra-row constant. No product byte, no new cell, `Tests: 21` unchanged, counts file untouched (`5220 / 310`, blob `d3c0021b`), `--update-counts` never run.
- Red-proof is by mutants, not against the product: the gate's GM10 (`|| ' '`) must turn F1 red for all five rows (MS1), plus two-space, no-break-space, trim, NFD-normalise, ASCII-only-upper-case, the old base line, the bracket change, and a tamper control (old loose assertion under MS1 stays green).
- Main is `f4ea31c99931b7e8708fa0c88f9a9d9fb287c991` (ls-remote), only `HISTORY.md` moved since the #132 merge. Open PRs 0. Quoted from Jira (GET, whole, no comments): summary, the Recommendation (scope) and the Done-when sentence, verbatim in the kit.
- Partition from both sides: yours = the one test file; B855 (M49) = `__tests__/rd891-probe-name-race.test.js` and `scripts/verify-expected-counts.json`. The kit treats a later move of B855's two paths on main as expected, not a stop, and keeps this branch on its Stamp base.

## Facts re-measured (instrument and control)
- Main and branches: `git --no-optional-locks ls-remote origin refs/heads/main` = `f4ea31c9...`; `refs/heads/b856*` printed nothing (control: `refs/heads/b849*` prints `81c73e48...`); `compare/7d21711d...f4ea31c9` ahead 2, files `HISTORY.md` only; the commits API shows `f4ea31c9` has 2 parents and a `users.noreply.github.com` author address (not quoted). `pulls?state=open` printed no row; `compare/main...records/b854` ahead 0.
- Blobs at main (raw API copy, `git hash-object` equal to the API sha): test file `e266ef36eded...` (234 lines), `static/js/testing.js` `7fa16e85...` (line 41 reads `[${(condition.risk_level || '').toUpperCase()}] ${condition.condition_text}`), counts file `d3c0021bb5f5...` (`tests` 5220, `suites` 310). Trees API depth-1 `__tests__/*.test.js` census = 310.
- The test file read whole (every line number in the kit is from this copy): `SLOTS` lines 45-49, `FORBIDDEN_FRAGMENTS` line 51 (substring test: `nan` would trip on "finance"), F1 lines 178-194, F2 builds from `SLOTS.map` so SLOTS must not grow. Cell inventory: P1, P2, D1, D2, F1 x5, F2 x2, F3 x5, F4 x5 = 21.
- Jira: RD-898 read through `b774lib.py` loaded in-process (`get`, `adf_texts`, `search`), status To Do, Low, created 2026-10-28, comments empty. The JQL `project = RD AND ( key in (...) OR text ~ ... )` listed RD-898 and RD-897 among others (read by key; no other ticket seen covering the exact-label pin in the first result page, which the seat repeats).
- Gate evidence read: `Briefs/2026-10-27_B853_STATUS.md` findings B853-1 (line 133) and B853-4 (line 136), the C6 matrix (GM1 14 red, GM8/GM9 9 red, GM10 and GM11 0 red of 21).
- CLARIFICATIONS.md: line 2067 (merge path), 2068 (never dismiss an alert), 2412 (the demo hold). Quoted as lines at the drafter's read; the seat re-reads.
- Ports: `lsof -nP -iTCP:9870-9879 -sTCP:LISTEN` empty (rc 1). Word-boundary scan (python3 -I) over 626 `*SEAT-*.md` kits: 9870 and 9879 hit only closed 2026-10-25/26 kits (B637 B642 B691 B693 B720 B728 B750 B752 B753 B754), 9875 hits B750, others none; no 2026-10-27 or 2026-10-28 kit hits. Live panes: `tuesday`, `fleet-monitor`. Control: the same scan found the closed-kit hits, i.e. it can fire.
- Pane `Datasec/NexusAI-M50`: 0 kit hits (control: `NexusAI-M25` hits the B849 kit); `worktrees/` and `session-tools/` hold no `b856`.
- Lock tool sha256 `cf01bafb...971f` (unchanged), `queue-jest/` empty, load1 3.34.
- Model: `models_latest.json` level sonnet = `claude-sonnet-5-5`; `model-routing.md` row C2 line 92, L6 line 85 (the class), G2 line 109 (tier 2 gate, round 1 of 2).
- Hygiene scan (python3 -I) over the kit: non-ASCII 0, clock times 0, person names 0, at-sign tokens 0, TAB 0, four-underscore lines 9.

## D-decisions (mine)
- D-1 Extra rows live inside D1 and D2 (the ticket's own words: rows inside an existing cell move no count), so the counts file stays out and B855's lane is not touched.
- D-2 Expected labels must be typed literals with `\u` escapes, never computed with the implementation's own method; a rule in the PROPERTY and a Step-6 scan (planted control) enforce it.
- D-3 The extra-row constant is separate from `SLOTS` because F2 maps the whole `SLOTS` array against a three-element levels list.
- D-4 Mutants beyond GM10 are chosen so each new row has one that reddens only it: trim (padded), NFD (accented), ASCII-only upper-case (accented, sharp-s), and a no-break space (which the old `\s` class accepted). MS9 is a tamper control: the old loose assertion stays green under MS1, proving the exact line is what bites.
- D-5 No clock time in the kit; the hard stop is stated as durations relative to the seat's own Step-0 date (target 2 hours, hard stop 3.5 hours, shorter than B849's because there is no counts regeneration).
- D-6 Not widened: non-string levels (B853-2), the second reader, the #132 commit wording (B853-5/-6), any product byte.

## Deviations from the B849 shape (D-n)
- D-7 No red-at-base step: the assertions are stricter tests of a correct product, so the order is baseline green, edit, green, mutants, one plain verify, one commit of one path. The Done-when has no `--update-counts`.
- D-8 REFUSE "main moved" treats a move of B855's two paths (`rd891` test, counts file) as expected; the B849 kit stopped on any counts move. Reason: B855 runs beside this lane by design and this lane changes no count.
- D-9 The mutants edit `static/js/testing.js` (not this lane's file) only inside the clone during a ticketed run, restored by saved copy and hash, as the B849 kit allowed; the diff must still be one path.
- D-10 The model row: the sweep names L6 as the class and C2 as the routing row; the kit follows the order (Sonnet) and cites both.

## Q-questions for the coordinator (each with a default)
- Q-1 Does the lane need the `Tests:` figure to stay exactly 21? Default yes; a need for a new cell is a STOP to Tuesday (it would put the counts file in a collision with B855).
- Q-2 Ordering against B855: both can run at once (distinct paths, one jest lock, FIFO). Default: run beside, no sequencing; whichever lands second needs no counts work from B856. Confirm you do not want B856 to wait for B855.
- Q-3 Gate tier. Default tier 2, round 1 of 2 (G2 line 109), as the sweep says.
- Q-4 Ports 9870-9879 (hits only closed seats). Default accepted.
- Q-5 Is a second sweep for a ticket other than RD-898 covering the same pin needed? Default no; the seat repeats the search at PRIOR WORK and stops if one appears.
- Q-6 The kit asks for padded and accented rows, and allows CJK, sharp-s and a long level as extras; the set is the builder's choice per the ticket. Default: at least the two, more only if each passes the stated PROPERTY.

## UNMEASURED
- No cell, mutant, jest, build or clone was run. Every red/green figure in the kit (MS1-MS9) is a prediction from the template and the gate's matrix. jsdom's `textContent` keeping a padded label's spaces is expected and proved by Step 4.2. CodeQL on the new head, the Linux runner and node 24, and whether any other test pins the bytes of this test file (Step 3.2 searches).

## Outside-the-fences disclosure
- Read-only: `gh api -X GET` under the NexusAI `GH_CONFIG_DIR` (contents raw, commits, compare, pulls, branches, trees), `git --no-optional-locks ls-remote` and one `git grep` on the stale shared checkout, `lsof`, `tmux list-panes`, `shasum`, `uptime`, `ls` of briefs, worktrees and session-tools, a Jira GET through `b774lib.py` loaded in-process, python3 -I scratch scripts and saved raw copies in the session scratchpad. Two of my Bash calls were refused by hooks (a `cd`, an unquoted `=====`) and re-issued without them. I wrote the kit, this report, and scratch files only in the scratchpad; no project, Jira, GitHub or git write.
