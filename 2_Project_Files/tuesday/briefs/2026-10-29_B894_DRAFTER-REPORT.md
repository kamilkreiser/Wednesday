STARTABLE: YES, after Tuesday stamps the 12 slot lines (11 slots plus the last line) and saves the unstamped kit as `.pre-stamp`; best launched AFTER records/b893 has landed on main (Job F STOPS otherwise, by design), and after the G198 waiter has launched.

# B894 drafter report (Datasec/NexusAI-R84: RD-868 writers, RD-869 family ruling)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-29_B894_SEAT-R84_nexusai-records-rd868-writers-rd869-ruling.md` (142 lines by `wc -l`, template B893 shape; ticket texts are templated for W3-W5 to stay short). Model Sonnet, rows C8 (`model-routing.md:98`) and C7 (`:97`), id `claude-sonnet-5-5` (`models_latest.json:22-23`). Launch line carries `WED_USAGE_STOP=100` before `bash .../launch_when_cool.sh` and inside the quotes, `BRIEF_SEAT_LEVEL=sonnet` inside.

## BLUF
Main is still `0df1e348` (`commits/main`, read 14:3x to 14:45 AEDT). RD-868 lists 6 numbered items; 4 are writers the ruling names (GET sync, kql cache, simpleDb, chat log). Default result: 6 new tickets (W1 GET sync, W2 kql cache, W3/W4/W5 one per dead simpleDb method, W6 chat log line 7007), 4 comments, RD-868 to Done (decision ticket per `CLAUDE.md:303`), 2 C-entries (C-227, C-228), 1 HISTORY entry. One writer DROPPED as already tracked (the 8914 log line = CodeQL alert 200, listed in RD-798).

## Writers table (re-derived at main 0df1e348; server.js blob 312c352e92479eff43e37bcff98bba3c8ee5f2f7, simpleDb.js blob 0d07e81a927b73d0fdd2e0c4a1db4cbf4efdccf6, both raw GET + git hash-object)
| id | writer (RD-868 item) | file:line at the sha | RD-868 said (ecb6b1e) | status |
|---|---|---|---|---|
| W1 | GET sync on a read (1) | server.js route 21029; sync call 21038 (guard 21037, settings read 21033); function 20699, writes 20760 / 20778 / 20795 | 21126 / 21135 | ticket |
| W2 | kql_query cache (2) | executeRiskConditionRows 4923 write 4935; GET /:level 21056 write 21090; POST /:id/execute 21130 write 21151 | 4923/4935, 21153/21187, 21227/21248 | ticket (1 ticket, 3 sites) |
| W3 | dead simpleDb addRiskCondition (5) | simpleDb.js 681 (INSERT 684) | 678 | ticket (slot SIMPLEDB THREE) |
| W4 | dead updateRiskCondition (5) | simpleDb.js 733 (UPDATE 767) | 730 | ticket |
| W5 | dead deleteRiskCondition (5) | simpleDb.js 779 (UPDATE 781) | 776 | ticket |
| W6 | raw chat log 'User confirmed suggestion' (6) | server.js 7007 in POST /api/chat 6971 | 7116 | ticket; value is a fixed literal (10 literals 8285-8330, assignment 8341), no CodeQL alert there |
| W7 | raw chat log 'Risk condition query detected' (6) | server.js 8914 in analyzeQuery 8483 | 9011 | DROPPED: CodeQL alert 200 open at 8914, RD-798 lists alert 200 (slot CHAT2 FILE overrides) |
| - | boot ensureLowTonerRiskCondition (3), erasure purge (4) | 5058, ~18958 stale | - | not tickets (RD-868 itself says nothing to decide) |

Controls: wrong-line grep fails (identifiers printed with their line); 11 `jsonStorage.(add|update|delete)RiskCondition(` call lines in server.js, 0 on `database|simpleDb|db`; alert 201 at 8924 read beside 200; the three simpleDb declarations fire in the census. Census frame: `git/trees/<sha>?recursive=1` truncated false, 1021 entries, 797 blobs by extension list (js mjs cjs ts html json md sh yml yaml py txt, package-lock.json excluded), 796 distinct shas, 795 fetched raw; 1 not fetched (`verify-setup.sh`, 404). The kit makes the seat re-run it and fill `{CAT-LISTED}`/`{CAT-FILES}` itself.

## Other facts re-measured
- RD-868: To Do, Medium, 1 comment (39717), link Relates RD-836. RD-869/870/872: To Do, 0 comments (b846lib GET). RD-868 transitions: 41 Done -> Done, one entry named Done.
- Searches (`project = RD AND ( ... )`, controls key = RD-868 -> 1, nonsense -> 0): no writer ticket exists. RD-798 (To Do, 44 log-injection alerts) is the only overlap.
- `CLARIFICATIONS.md` is NOT in the repo: it lives at `1_Project_Definition/CLARIFICATIONS.md` (2436 lines, highest C-226, last section `## 63.`), not git-tracked, and records seats append it in place (b813 precedent). So the lane's "docs-only branch with both files" cannot be literal: the branch carries `HISTORY.md` only; the C-entries are a local append (Job E). Say so if you disagree.
- `records/b893` not on origin at 14:4x (`git/matching-refs/heads/records/b89` returned 0 rows; control: `records/b875` returns 1); HISTORY.md at main 8841 lines, last heading B875 :8766, no B893 heading. Open PR: #139 only.
- Ports 9840-9849: `lsof` printed 0 lines. Word-boundary scan of 40 non-`.pre-` SEAT kits of 10-28 and 10-29: hits B862, B865, B877 (closed seats' 9840-9849 mentions), B895 (names R84/R83 as records seats). No live use. Panes: H51-H53, J31, J32, NexusAI-M54, fleet-monitor, tuesday.
- Jira text scans by program on the 40 Jira-bound part lines: non-ASCII 0, at-sign 0, percent 0, `C-<digit>` 0, person/seat/brief/lane/card words 0. Summary lengths 203 / 227 / 160 / 174 / 175 (limit 255). Slot census: `grep -c -E` of four underscores prints 12 on the kit (control: a planted `a ____ b` prints 1).

## D-decisions
- D-1 One ticket per METHOD for the simpleDb writers (3), because the source lists three and "writer" = a function that writes; the question text said two. One ticket for the kql cache (RD-868 item 2 treats it as one item, the question said "a kql cache"), though it has 3 write sites.
- D-2 RD-868 moves to Done (default), by the project rule for a decision ticket; slot MOVE868 `NONE` leaves it. The move needs every create read back.
- D-3 W6 is filed as the ruling requires but says honestly that the value is not request text; the recommendation is "leave or wrap". Priority Low for all (RD-868 shows no more).
- D-4 RD-872 comment says the ruling does not extend the closed list of 21 nouns (matches B895's reading, which pins RD-872 behaviour byte-identical); strike that clause if you read the ruling wider.
- D-5 No Jira link used (the template creates with no links); "Related: RD-868" in the text. Labels: operations / hygiene+tech-debt / security (copied from RD-868 and RD-862 shapes) plus `b894-2026-10-29`.

## Q-questions for Tuesday (default in brackets)
- Q-1 SIMPLEDB: THREE tickets or ONE? [THREE, source count; ONE if you read the card's "two" as the intended unit].
- Q-2 CHAT2: file the 8914 line anyway? [DROP: already RD-798 alert 200, "drop any already filed"].
- Q-3 MOVE868: DONE or NONE? [DONE per `CLAUDE.md:303`].
- Q-4 `scripts/fix_risk_conditions.js:45,97,164` (raw UPDATE risk_conditions on SQLite) and `server.js:6944` (chat validate path `jsonStorage.addRiskCondition`) are further writers RD-868 does not list; not ticketed [leave out of this lane, surface to the product owner in a later card if wanted].
- Q-5 Launch order: after records/b893 lands. If R84 starts first it files Jira and C-entries, then STOPs at Job F; re-stamp HISTORY and rerun Job F only [launch after].

## UNMEASURED
Whether the 796th sha (`verify-setup.sh`) holds a caller (it is a shell script, 404 on the blob endpoint); computed-name calls to the simpleDb methods; race behaviour of concurrent GETs (named in RD-868, not run); any deployed instance's open/closed mode; the live B895 builder's final scope (read only its first lines); decision cards (not read, rulings taken from the task text).

## Outside-the-fences disclosure
Wrote only the kit and this report, plus scratch in `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/67807bfb-43bf-444e-bc05-31759ccc4569/scratchpad/k/` (jr.py, jc.py, js.py, tree.json, blobs, alerts.json, copies of server.js / simpleDb.js / HISTORY.md / JIRA.md). Reads beyond the named inputs: NexusAI `CLAUDE.md` and local `JIRA.md` by line, `CLARIFICATIONS.md` tail and numbering, `session-tools/b813/append-c813.py` (head), `session-tools/b846/b846lib.py`, Jira GETs of RD-798, RD-859, RD-862, RD-869/870/872, the B895 kit's first lines and three grep matches, `model-routing.md` lines 96-99. `gh` was `-X GET` only under the project GH_CONFIG_DIR (code-scanning alerts paged, git blobs fetched). No decision_queue call, no fleet/briefs_staged, scoreboard, ledger, Wednesday/Friday tree; no git verb in a project repo; no HTTP to an app host; one `cd`-containing call was refused by the hook and re-issued without it.
