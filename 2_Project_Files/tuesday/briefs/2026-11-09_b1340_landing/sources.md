# Sources for the b1340 landing text

Abbreviations (all under `/Volumes/Laptop-DEV/!CODING/Datasec/NexusAI/1_Project_Definition/Briefs/`):
- ST = `2026-11-07_B1365_STATUS.md` (the gate's verdict, 384 lines)
- CI = `2026-11-07_B1365_evidence/card-input.txt` (20 lines)
- RS = `2026-11-07_B1365_evidence/residue.md` (108 lines)
- BL = `2026-11-06_B1340_STATUS.md` (the builder's record, 80 lines)
- MG = `git log --merges -5 main` in the NexusAI checkout (house shape)

Line numbers were read from `cat -n` output of the files in this drafting session.
The drafter did not run any program to generate pointers beyond `cat -n`; each was read off the numbered print.

## pr-title.txt
| sentence | rests on |
|---|---|
| names RD-798, RD-799, RD-800 | ST:242 (the three keys exist, To Do), CI:1 |
| "44 flagged log lines", "logSafe" | ST:96, BL:7, BL:21 |

## pr-body.txt
| sentence (opening words) | rests on |
|---|---|
| Wraps all 44 flagged log lines ... in logSafe | ST:9, ST:96, CI:4 |
| ... a CR/LF value ... can no longer forge a log line | CI:4 ("a CR/LF value forges no log line at the head"), ST:121 |
| Nothing deploys ... deploy switch repository variables are 0 | ST:176, ST:269 (read 22:13 AEDT 7 Nov, see UNMEASURED) |
| The new tests have four known weaknesses | ST:11-19 (B1365-1 to -4), CI:8-12, RS:9-69 |
| server.js differs from main in exactly 44 lines, 38 plain, 6 design | ST:96, ST:250 |
| the 44 lines are RD-800 11, RD-799 8, RD-798 25 | DERIVED by the drafter from BL:7 (RD-800: 208 209 211-219 = 11; RD-799: 164-171 = 8; RD-798: 162 163 187-207 222 223 = 25; sum 44). Not stated as a count anywhere in the records. See QUESTION 1 |
| line 3169 logs the first 8 characters of state and cookie, as its neighbour | CI:5, ST:130, ST:320, ST:147 |
| Lines 215 and 216 change log form (array now JSON) | BL:17 |
| 119 tests in 3 suites | ST:167, ST:238 |
| shared test helper (log-wrap-shape.js) | BL:7, ST:107 |
| one added line in the rd477 sandbox so the wrapped function can call logSafe | BL:10, ST:208 |
| committed counts 5369/322 to 5488/325 | ST:166, ST:162-165 |
| The branch changes 7 paths | ST:94 |
| All 44 lines wrapped; CR/LF forges no log line at head | ST:9, ST:121, ST:251 |
| Characters 9 to 40 appear in none of the captured output or log files | ST:134 (stdout, stderr, combined.log, error.log, audit-buffer.json) |
| callback answers 11 of 11, chat answers 24 of 24 equal, audit records equal | ST:138 (11 of 11 and audit), ST:58 (24 of 24 paired answers), CI:6 |
| All eight findings from the first round closed | ST:99-107, ST:262 |
| 40 of 40 shifted clock states and 10 future dates green | ST:53, ST:112, CI:7 |
| Full verify passes at 5488/325 on the head and on the merge result with current main | ST:201-202, CI:19 |
| The second gate round said NO GO ... the cap | ST:1, ST:3, ST:9 |
| Those findings are in the test files, not the product code | CI:8, ST:9 |
| Major: mask too wide, rd798 test line 436 | ST:14, ST:9, RS:11-17 |
| swallows text right before or right after a job's time | ST:14, ST:26, RS:15-17 |
| Three planted test edits (marker before, marker after, "Invalid Date") passed | ST:14, RS:19-22, CI:9-10 |
| A narrower date-time-shaped mask, checked offline, catches all three | ST:14, ST:336, RS:28-32, CI:10 |
| Minor: 190 comparisons pin nothing of the off-hours paragraph within a pinned state | ST:15, ST:90, RS:37-43 |
| Minor: rd798 C-BODY, 12 keys red on a German-locale machine | ST:16, ST:212, RS:53-58 |
| green under the CI shape and on the gate's Mac | ST:212 ("hosted shape C.UTF-8 + TZ=UTC 119/119 ... en_AU (this Mac) 119/119"). The hosted runner's real locale is NOT measured (RS:56-57); wording "CI shape" means that run shape. See UNMEASURED |
| Minor: rd799 test line 272 title says "the full state", asserts eight characters | ST:17, RS:63-67 |
| These four findings are being ticketed with the reviewer's cells attached | RELAYED: the 09:00 default of option (a) as given in the drafting task; CI:20 offers option (b) "ship ... and ticket the four test findings"; RS:34-35, RS:50-51 are the cells. Not yet done: see UNMEASURED |
| Hosted CI and CodeQL have not run on this head | ST:314, ST:339, CI:18 |
| Whether the 44 alerts close is read on main's analysis after the merge | CI:18, ST:263 |
| Left as they are: learningManager.js alerts 152, 153 | CI:13, RS:88-89, ST:184 |
| ... cache line 204 not driven by two seats | CI:13, RS:88, ST:349 |
| ... route that answers 500 (POST /api/learning/confirm-clarification) | CI:14, RS:90-91, BL:15 |
| ... a session revocation that never runs | CI:14, RS:91-92, BL:15 |
| A merge to main starts a Deploy demo run, its build and deploy jobs skip while CI_DEPLOY_ENABLED is unset | ST:176, CI:16 |
| repository and organization variables both 0 at the gate's final read | ST:269, ST:176 |
| A standing product-owner ruling holds every demo deploy until a separate notice-and-button change lands | ST:180 (C-224, "THE PRODUCT OWNER'S RULING ... no NexusAI demo deploy goes out until RD-876 part 2 (the notice and the show-all button) lands"), CI:17 |
| last line (robot) | the line given in the drafting task, verbatim |

## merge-subject.txt / merge-body.txt
| item | rests on |
|---|---|
| Subject shape `Merge <branch> (<ticket>) into main` | MG, subjects of `edf1ab7` and `632a377` ("Merge rd-369-round2-s47 (RD-369 round 2) into main", "Merge rd-369-recut-s47 (RD-369) into main") |
| Body: short gate line, then what is ticketed not fixed, as MG bodies do | MG bodies of `edf1ab7`, `632a377` ("The residue is TICKETED, not fixed, and there is no round 3 ...") |
| Wraps all 44 lines; 119 tests in 3 suites; verify 5488/325 at head and merge result | ST:96, ST:167, ST:201-202 |
| Gate: round 2 of 2, NO GO by the cap | ST:1, ST:3 |
| no round 3 without the product owner | ST:306 ("A third round needs his word on a card"), ST:336 |
| Nothing deploys ... variables are 0 | ST:176, ST:269 |
| Hosted CodeQL is read on main after this merge | CI:18, ST:263 |

Landing rule (merge commit, never squash): ST:330 (quoting CLARIFICATIONS.md:2067 "Never squash, never rebase ([[C-68]])").

## UNMEASURED (the drafter could not verify)
- The branch itself: `git diff --stat fe75d7b2 2b60ff66` and `git log fe75d7b2..2b60ff66` both failed in the NexusAI checkout (`fatal: ambiguous argument 'fe75d7b2': unknown revision`). The objects are absent locally; I did NOT fetch. Every statement about the diff (7 paths, 5 commits, 44 lines, 119 tests) rests on ST, not on a git read by me. The commit subjects of the five branch commits are therefore not read; I did not copy any.
- The deploy switch values (repo variables 0, org variables 0, environment `dev` only) are the gate's read at 22:13:29 AEDT Sun 8 Nov (ST:266-269). I did not re-read them (no gh, per rules). Tuesday re-reads before landing (BL:4 says the same).
- Whether the second statement "green under the CI shape" holds on the hosted runner: only the shape was run (ST:340, RS:56-57).
- Whether the ticket for the four findings exists yet: nothing in the sources shows one filed.
- The house merge shape on NexusAI's current main: the local checkout's `main` is stale (the latest merges it shows are September, authored with a different trailer); origin's recent merges were not read (no fetch, no gh used).
- Hosted CodeQL, hosted Build: ST:339-340.
- The Jira ticket texts (title, alert counts per ticket): not read; the drafter used no Jira.

## QUESTIONS
1. Which RD keys does this branch close? The records never say a ticket is closed. ST:242: RD-798, RD-799, RD-800 are all To Do. Alert lane per BL:7 is RD-800 11, RD-799 8, RD-798 25 (my derivation). ST:184: 46 open `js/log-injection` alerts on main: 44 in server.js plus learningManager.js 152 and 153, which BL:16 says were held out for a later lane. The user-brief mention of "44/27 alerts" for RD-798 is not in any source I read. The body therefore says "(RD-798, RD-799, RD-800)" as references and never "closes". Also 171 (revocation never runs), 222 and 223 (route throws first) are wrapped but unreachable (BL:15), so they cannot be shown closed by behaviour; CodeQL on main is the only read (CI:18). Tuesday decides whether any ticket moves, on main's analysis after the merge (DRAFTER_RULES.md:42).
2. The "25" for RD-798 and "11" and "8" in the body are my sums from BL:7, not a printed count. If Tuesday would rather not carry a derived number, delete the bullet "Per the build record the 44 lines are ...".
3. Merge-commit trailer: MG bodies end with a `Co-Authored-By:` line and a `Claude-Session:` URL; I wrote neither (the rules forbid "Claude" in the title and I have no session URL). Tuesday adds the trailer the lander's rules require.
4. Hosted CodeQL shape at line 3169 is UNMEASURED (ST:323); if CodeQL flags it on the PR head, the PR body's "Summary" claim is unaffected, but the landing waits on CodeQL green per the task.
5. Source tension (minor): ST:212 gives the German-locale red as 12 keys, and RS:55 names the keys 162, 191, 195, 196, 197, 203 (p and h, 12 keys); consistent. ST:26 states two readings of "declared mask" (Major vs Note); the gate took Major, and the body follows the gate.
