STARTABLE: YES

# B835 drafter report (kit for Datasec/NexusAI-M24, NexusAI RD-893 part 1, ruled "Store it lower-case")

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-27_B835_SEAT-M24_nexusai-893-risk-level-lowercase.md`

## BLUF
- The ruling (card `nexusai-risk-level-case-rule-1027`, `choice='b'`, ruled 2026-10-27T13:35:52+11:00) is option b, "Store it lower-case": "HIGH and High are saved as high, so the condition shows in the High list." It is silent on create, on the readers and on rows already stored in mixed case, so those are Q-questions with defaults.
- The fix is one statement in `backend/server.js`, `app.put('/api/risk-conditions/:id')`, after the existing level check and before `updateRiskCondition`. Only the PUT can store a mixed-case level (all other write paths measured below).
- A new test file (`__tests__/rd893-risk-level-stored-lowercase.test.js`), HTTP against the real server in rd878's shape, with red-first edit cells, controls, a driven create-refusal cell and eight mutants. Because it adds a suite, the counts file changes by the project's rule: 5178 + N tests / 309 suites, regenerated once by `--update-counts`.
- Startable: the kit's three paths (`backend/server.js`, one new test file, the counts file) do not intersect PR #130's four test files (the live seat M23). Main is `c8e1a9a11e8035037cff6285f4be7e7d30f1c459`.
- Two findings the ticket did not state: (1) the alert mailer (`riskAlertScheduler.js:114`) reads the three levels through the same strict `===` reader, so a condition edited to "HIGH" also stops being mailed; (2) the Settings page rule editor always sends lower-case, so the Settings UI cannot create the bad state. Only a direct API client can.

## Facts re-measured (instrument and control)
All at main `c8e1a9a1`, raw files by `gh api -X GET .../contents/<path> -f ref=<sha> -H 'Accept: application/vnd.github.raw'` under the NexusAI `GH_CONFIG_DIR`.
- Main: `git --no-optional-locks ls-remote origin refs/heads/main` = `c8e1a9a11e8035037cff6285f4be7e7d30f1c459`; the shared checkout HEAD is `cd2b5439` (stale, control that it is not main). Control for the saved copy: `git hash-object` of the saved server.js = `8c9306522a15...`, equal to the API's blob sha for `backend/server.js`.
- Open PRs: 1 (#130). `pulls/130/files` lists four test paths. `compare/main...b823/...`: ahead 4, behind 3. `b816/...`, `b798/...`, `b777/...`: ahead 0 (landed).
- Counts: file blob `7f92fb6a0911`, tests 5178, suites 308 (PR #129 moved it from 5170/307). Census of `__tests__/*.test.js` in the trees API = 308 (equals suites, control for the frame). Test name `rd893` in tree: 0 hits (control `rd878`: 1).
- Defect, read from code (not driven): PUT validates `updates.risk_level.toLowerCase()` against low/medium/high (`server.js:21233`) and stores `updates` as sent via a spread (`jsonStorage.js:3754-3765`); `getRiskConditionsByLevel` is strict `===` (`jsonStorage.js:3743`); the by-level route lower-cases only the URL level (`:21056-21069`). The earlier builder drove this on a stand (B807 status, "RD-893: the stand"): PUT "HIGH" and "High" leave the row in neither the High nor the Low list; PUT "high" lists it. RELAYED, not re-driven by me.
- Create: Joi `riskLevel: Joi.string().valid('low','medium','high')` (`validators.js:55`); `grep` for `insensitive` and `convert` in validators.js: 0 hits (control: `riskConditionInputSchema` hits). So create refuses "HIGH" with a 400 (code reading; the kit has a cell that drives it). It also lower-cases again at store (`server.js:20990`).
- Write paths (frame: server.js, jsonStorage.js, simpleDb.js, riskAlertScheduler.js, scripts/fix_risk_conditions.js, grep on `risk_level|riskLevel|addRiskCondition|updateRiskCondition`): create (lower-cases), PUT (the defect), validate-condition save (`level.toLowerCase()`, `:6944`), settings sync (literals `'low'/'medium'/'high'`), `ensureRiskCondition` (three callers, all literal `'high'`), `simpleDb` (SQLite, in-repo callers UNMEASURED). No import or restore route found by grep (a grep, not a proof; the kit tells the builder to re-grep). The fix script writes none.
- Readers: `getRiskConditionsByLevel` (by-level route, `generateRiskConditionReport`, alert scheduler for low/medium/high), validate-condition duplicate check (`:6934`, strict), `static/js/index.js:4726` (strict). Settings page lower-cases for display (`settings.js:1131,1151`) and sends `low/medium/high` (`:1217-1219`; sent at `:1356`).
- Trap found: `static/settings.html:616-618` offers `High/Medium/Low` capitalised for the red-flag risk level, a different setting (`red_flag_risk_level`). A grep for `risk_level` finds it; the kit forbids touching it and adds a "no added line mentions red_flag" property.
- Mixed-case rows in stored data: UNMEASURED (no access to any deployed instance by rule). What is measured: only a direct API PUT could create one; Settings cannot; and a Settings save of the rule sends lower-case, so a mixed-case row repairs itself on its next save (kit cell E6 documents it).
- Jira (b774lib loaded in-process, `get` and `search`, JQL `project = RD AND ( ... )`): RD-893 status To Do; its first part is this defect; its other parts (other PUT fields' types, the Log Analytics path) are not this lane. Search for risk-level/lower-case text: 33 keys, RD-893 first. Control: the credentials were not printed; a scan of my output for `token|Basic ` matched three ticket summaries that contain the word, no credential.
- Ports: `lsof -nP -iTCP:9630-9639 -sTCP:LISTEN` empty (rc 1). **Your handover said 0 hits in today's kits; I measured otherwise.** Word-boundary scan over the 130 non-`.pre-` SEAT kits of 10-26 and 10-27: 9630 and 9639 each hit 5 kits (B778, B779, B781, B784, B787; all closed Composer/HPSM seats that reserved or named the block for themselves); 9631 and 9635 hit 0. Live panes at ~16:2x: `%0 tuesday`, `%80 Datasec/NexusAI-M23`, `%79 Datasec/HPSM-POC-G180`, `%78 Datasec/HPSM-POC-G178`, `%77 Datasec/MPS-G177`, `%75 Datasec/HPSM-POC-H46`, `%1 fleet-monitor`. None holds 9630-9639. Control: `9620` hits B765, B766, B834. `NexusAI-M24` hits 0 kits (control `NexusAI-M23` hits). 9640-9649 are not cleaner (5 other kits hit).
- Lock tool sha256 `cf01bafbc51f555ca0f14d1711f01885bcec5bc6293b177fe24702226bb4971f` (matches the B823 kit); `queue-jest/` listing printed nothing. Load1 6.52 (5 min 7.38).
- Model: `model-routing.md` line 92, row C2 (multi-file build, not decision-shaped, not auth-design, not a data-destroying path), Sonnet 5.5 first, ruled 2026-10-10. Not C3 (no auth or credential surface: the route's admin gate is untouched), not C4. Id `claude-sonnet-5-5` from `models_latest.json` (line 23). Launch line has `BRIEF_SEAT_LEVEL=sonnet` inside the quotes.

## D-decisions (mine)
- D1. Normalise in the PUT handler, not in `jsonStorage.updateRiskCondition`. Every other writer passes a literal or already lower-cases (measured), so the handler is the only door; one product file, 4 added lines at most, 0 removed. Cost: a future writer that bypasses the handler is not covered.
- D2. New test file with a copied harness, not new cells in rd878. rd878 says falsy levels are pinned neither way and the project convention is a small copy; a new file is additive and moves the counts by one suite. Cost: counts become 5178 + N / 309 and the counts file is in the diff (kit has the project's `--update-counts` rule, assert-by-program, once).
- D3. Cells are HTTP against the real server (the defect is route plus store plus list), with a create-refusal cell that falls back to an in-process Joi check if the POST cannot be driven deterministically.
- D4. Invalid words and stray spaces stay refused (cell E4), pinning that the ruling is about letter case only.
- D5. A mixed-case-row repair cell (E6) is a control, deliberately not a pin of the reader's strictness.
- D6. Eight mutants, including one in `validators.js` (create) and one in the wrong handler, with a rule that every cell is red under some mutant or is a named control.

## Q-questions for Tuesday (each with the default the kit uses)
- Q-1. Should create also normalise "HIGH" to lower-case? The ruling text speaks only of edit. Default: no; create keeps refusing, and a cell drives that refusal. (If yes, it is a Joi `.insensitive()` or pre-lowercase change in `validators.js`/`server.js`: a second product file and a changed 400 behaviour, which wants its own ruling.)
- Q-2. What happens to rows already stored in mixed case, and the readers? Default: no data migration, no reader change; the write is closed, the Settings UI cannot produce the state, and a re-save from Settings heals a row. The alternative (case-insensitive reader in `getRiskConditionsByLevel`, the duplicate check and `index.js`) widens the diff over four files and hides the data problem. Tuesday may open a ticket to census the stored rows on the instances that matter (I cannot: no deployed access).
- Q-3. New test file (default) or extend rd878.
- Q-4. The falsy levels (`""`, `0`, `false`, `null`) still skip the check and are stored as sent (an empty string would vanish from all lists). Default: not touched, not pinned (rd878 says the same); worth a separate ticket.
- Q-5. Gate tier. Default: tier 2 (the change is a validated admin route, not auth, not data-destroying, not deploying; the gate's own rule row is G2 "tests-only..." which strictly covers tests, so this is a judgement call: product code, one line). Tier 1 is defensible because it changes behaviour that feeds the alert mailer. Your call.
- Q-6. Ports: keep 9630-9639 (default), since every hitter is a closed seat and nothing listens.

## UNMEASURED
- Any server being run: I ran nothing (no clone, npm, jest, server). The red/green table, the mutants and the counts N are the builder's.
- Create's refusal of "HIGH" on a running server (code reading only).
- The Log Analytics path with a mixed-case level (RD-893 part, not this lane).
- Stored mixed-case rows on any deployed instance.
- The landing-rule line numbers in `CLARIFICATIONS.md` (relayed from the B823 kit; the kit says re-find by text) and `verify-suite.sh:85-96`/`build.yml:83-84` (relayed from the B816 kit).
- CodeQL on the new head; the Linux runner and node 24.
- Whether `simpleDb.addRiskCondition` has any caller.

## Outside-the-fences disclosure
- Wrote only the two files. Read the card only via `decision_queue.sh show <exact id>` into a scratch file and through filtered `sed`/`grep` of its option lines (I printed lines 5-10 with `cut`, which showed the options and the default text; that output included the card's BLUF line, since the ruling lines sit beside it; no `list`). Did not read `briefs_staged`, `scoreboard`, `_ledger.md`, or any WEDNESDAY/FRIDAY/non-Datasec tree.
- Git in the project repo: only `ls-remote`, `rev-parse HEAD`, `grep` and `ls-tree`-style reads (`git grep` on the stale shared checkout to locate code; then switched to origin via the API). No fetch, worktree, checkout, ref write.
- `gh` only `-X GET` under the NexusAI `GH_CONFIG_DIR` (contents, trees, pulls, compare, branches list). No HTTP to any hosted host.
- Jira: GET and search through `b774lib.py` loaded in-process with `python3 -I`; a scratch script in the session scratchpad (not the project). No token printed.
- Used `lsof`, `tmux list-panes`, `shasum`, `uptime` read-only. Two small slips: one early Bash call ran an `ls` in the working directory (TUESDAY root), harmless; and two grep calls without `-i` drew the case advisory (each had controls from the same file in my reading, the hits were located by line).
- Scratch files (saved raw copies, tree list, the Jira script) live in the session scratchpad `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/59f24562-ea21-4839-8efe-6c4a3767c6d2/scratchpad/`.
- Kit self-checks: slot-line count with the split-quote pattern = 9 (eight slots plus the last line); the `@[A-Z_]+@` count = 0; a scan for person names and the card id = 0 hits; non-ASCII bytes = 0.
