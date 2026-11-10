GATE B1392-2: GO WITH FINDINGS @ 9302bc0 on main 0820efe

Tier 2 (UI copy + one hub component). Nothing security-shaped found. No Blocker, no Major.

## Refs and merge (MEASURED)
- `git ls-remote origin`: `b1392/hpsmpoc-caveat-reword` = 9302bc0dd94b8cec4c0dec1270abee28c969eae6 (= READY sha); `main` = 0820efe9ff08d32bc0d4710643081abb268f4725.
- Two commits: 33550c0 (parent 0820efe9) and 9302bc0 (parent 33550c0). merge-base = main.
- Scratch clone (push URL set invalid, never pushed): `git merge-tree --write-tree origin/main 9302bc0` rc 0, tree a1eeaabb... = head tree a1eeaabb... (clean; merge = head bytes).
- Changed paths 7. In L1 OWNS: 5 of 7 (web/src/components/**, web/src/app/**, web/src/content/**). Outside: web/e2e/playbook.ts, web/e2e/playbook-event-states.spec.ts (L4's), authorised by ruling (1); see F1.
- Open PRs: 0 (`pulls?state=open` length 0; control `state=closed` lists 302, 301, 300). Sibling branches: b1393/b1394/b1395 and b1392/hpsmpoc-web-ui overlap 0; b1392/hpsmpoc-web-ui-d touches steps.ts/steps.test.ts but its content is already on main (squash 90d30d5; `git diff aca2290c 0820efe9 -- web/src/content/walkthrough/` empty), so effective overlap 0.
- No data write, API, contract or migration change, by program: changed paths matching `^api/|web/src/api/|web/src/server/|migration|openapi|contract` = 0; added non-test lines calling `api.`/fetch/method = 0 (control: the test file adds 4 `api.` lines); probe P6 and the existing "reads only" row: 0 non-GET requests while the hub renders.
- Deploy: ci.yml line 1 "No deploy job, no cloud credentials"; only workflow is ci.yml. A merge triggers CI only (it keeps deploy packages on main); no deploy.

## CI jobs, main vs head (merge = head tree), counts by program
| Job / step | main 0820efe | head 9302bc0 |
|---|---|---|
| infra hidden-character scan (infra/tests/test_hidden_characters.py, walks git ls-files) | 14 tests OK | 14 tests OK; control: planted raw U+202E in steps.ts -> FAIL naming steps.ts:250:4 |
| web lint | rc 0 | rc 0; control: planted `any`/`var` file -> rc 1 |
| web typecheck | rc 0 | rc 0 |
| web unit (vitest, 285 files) | 4183 passed, 0 failed, 0 skipped | 4187 passed, 0 failed, 0 skipped (+4: 1 steps row, rows b, c, d; a replaces) |
| web build | rc 0 | rc 0 |
| e2e --check-shards | - | "shard plan OK" |
| e2e playbook-desktop-1 | 64 passed, 4 skipped | 64 passed, 4 skipped |
| e2e playbook-desktop-2 | 54 passed, 13 skipped | 54 passed, 13 skipped |
| e2e playbook-mobile-1 | 63 passed, 5 skipped | 63 passed, 5 skipped |
| e2e playbook-mobile-2 | 52 passed, 15 skipped | 52 passed, 15 skipped |
| e2e prototype-desktop-2 (walkthrough-uat, shell-sidebar, responsive) | 177 passed, 4 skipped | 177 passed, 4 skipped |
| e2e prototype-tablet-2 (same specs, tablet) | 177 passed, 4 skipped | 177 passed, 4 skipped |
| e2e prototype-tablet-1 (a11y, keyboard, html-layout) | 181 passed, 1 skipped | 181 passed, 1 skipped |
| e2e journey-and-prototype | 2 + 182 + 14 passed | 2 + 182 + 14 passed |
All 8 e2e shards run serially, ports 9750-9753 (lsof 0 before each). One earlier attempt of mine failed on a runner fault (`npm exec -- node` pulled an npm "node" package); fixed to /opt/homebrew/bin/node and rerun; that log is kept as `.badrun`.

## Red without the fix (MEASURED, in copies)
- Head's steps.test.ts + AssessmentsHub.myreadiness.test.tsx on main's code: 5 failed - new save/score/approve row (hits report.caveat score the + approve the), step 10 caveat pin, row (a), row (c), updated first row. (b) and (d) green by design.
- Mutation controls at head: ungating leadWithCurrent -> (b) + 7 rows red; renaming the sidebar label -> (d) red. Both can fail.
- Head's two e2e pins on main's build (playbook-desktop, event-states + readiness specs): 6 failed, 25 passed (the H1 heading "Playbook Partner Readiness" not found). Green at head.

## ADDENDUM-3 probes (scratch test at head, quarantined after; same probe at main for contrast)
| Probe | Head result |
|---|---|
| P1 newest completed run on unknown content (deck id/version, wrong hash) | notice "Your latest results cannot be shown here", no current panel, 1 Start |
| P1b run stamped with a version the API does not hold (9.9.9) | hub shows its error state (mock 500), 0 Start - identical at main; pre-existing, not this change |
| P2 no run at all | no current panel, no overview, 1 Start |
| P2b only an in-progress deck run | no current panel, 1 Start, Resume listed |
| P3 in-progress current run newer than completed deck run | current panel leads, 1 Start (inside the panel), Resume + View results listed, no deck statement drawn |
| P4 completed current run older than a newer completed deck run | current panel leads, current run's overview not drawn, both runs listed with View results, 1 Start (see F4) |
| P5 current completed run newest | overview drawn, 1 Start |
| P6 deck lead | 0 non-GET requests; 16 list items, 4 areas; panel text equals the third NEW WORDS line |
| P7 run on 0.4.0 (held, carries the deck set) | current panel leads |
| Start-count control | re-enabling the card's Start under the panel -> P3, P4 red (2 Starts) |
| Sidebar | GlobalNav.tsx:44 label "My readiness" unchanged at head (row d, and not in the diff) |

## Coordinator ruling (2): the `save` exemption, graded
- What it does: strips `\bdo not save\b` (case-insensitive, global) before the three patterns run on every caveat and cue. It removes three words only, so any other "save" in the same text is still caught ("Do not save. Save the answer." -> caught; "Do not save yet; save after you score it." -> caught; "don't save an answer" -> caught, a safe false positive).
- Narrowest? Not strictly: the narrowest is step 6's exact phrase "View only: do not save an answer". The only slip I found through the exemption itself is a hyphen compound ("Do not save-and-submit"). Acceptable.
- Slips that come from the addendum's own patterns, not the exemption: "approve it", "approve your narrative", "score it", "score this assessment", "saving", "submit" are not caught.
- Today's shipped text: a broad verb scan of every field of all 14 steps finds no instruction to score, approve or save in any caveat or cue (hits are descriptive: "the latest score", "its human-approval label", "approved narrative").
- Grade: fit for purpose; F2.

## Copy that goes to the product owner (MEASURED, by program, against the head)
- NEW CAVEAT line = the step 10 `caveat` string in steps.ts, exact match (control: +1 char does not match).
- NEW WORDS 2 "Playbook Partner Readiness: current statements" = `${READINESS_TITLE}: current statements` rendered, exact.
- NEW WORDS 3 = the panel paragraph rendered with 16 and 4, exact (also seen in the DOM by P6).
- NEW WORDS 1 is "Playbook Partner Readiness" followed by a builder annotation in parentheses (F3).

## Scans
- Ban-list names, underscore-aware `(?<![A-Za-z])name(?![a-z])`, over added lines and both commit messages: 0 (control a planted `_by_<name>_` line = 1). B-numbers 0, seat ids 0, GUIDs/tenant/subscription ids 0, hosts 0, secret words 0, Cf characters 0. Non-ASCII in added lines: one U+2026, the app's loading text already on main. Commit messages: plain ASCII, end with the attribution line.

## Findings
| # | Severity | Finding |
|---|---|---|
| F1 | Minor | Ruling (1): each out-of-OWNS e2e file changes one line. With the old pin string replaced, the code is identical to main's (by program). Each line also adds a trailing comment ("the hub's H1 since 2026-11-10 ..."). A comment changes no behaviour, so I grade it Minor, not Blocker. The coordinator may rule otherwise. |
| F2 | Minor | The `save` exemption is not the narrowest form (step 6's exact phrase would be). The patterns the addendum dictated miss "approve it/your", "score it/this", "saving", "submit". No shipped caveat or cue is affected today. |
| F3 | Minor | STATUS NEW WORDS line 1 carries a parenthetical annotation; send only "Playbook Partner Readiness". The tab renders as "Playbook Partner Readiness [middle dot] HP Security Services Playbook" (root layout title template). |
| F4 | Note | P4: if a deck-version run is completed after a current-version run, the hub leads with the current statements and does not draw the current run's overview (still listed). This follows the spec's literal rule. The UI cannot create it (Start always uses the current package). |
| F5 | Note | P1b: the hub's error state for a run on a package the API does not hold is the same at main; not this change. |

## Builder STATUS claims (ADDENDUM-2 and ADDENDUM-3)
| Claim | Grade |
|---|---|
| Base 0820efe9; commit 33550c0 parent 0820efe9 | true |
| A2 diff 2 files, 17+/1- | true |
| Caveat loses only the score-and-approve clause | true (diff) |
| Red-first on 0820efe9's caveat, hits score the + approve the | true (my run: same two hits) |
| steps.test 13 passed at head | true (13 rows, all green in the full run) |
| Full npm test 4184 at 33550c0 | not shown (not re-run at 33550c0; consistent with main 4183 + 1) |
| Lint/typecheck rc 0 | true |
| Walkthrough e2e green | true (inside the shards above) |
| NEW CAVEAT text | true, exact |
| A3 commit 9302bc0 parent 33550c0; 5 files 101+/20-; branch 7 files 118+/21- | true |
| 0 Cf; one non-ASCII = existing U+2026 ellipsis | true |
| Re-printed 0820efe9 lines (Hub 61-69, 83, 95, 96; page.tsx 4) | true |
| 3 failed / 11 passed at 0820efe9; 14 passed at head | true |
| (b) mutation red (8 failed) / (d) mutation red | true in kind (my combined mutation: 9 failed = 8 + d) |
| Full suite 4187; lint, typecheck, build rc 0 | true |
| e2e counts for desktop-1/2, mobile-1/2, prototype-desktop-2, prototype-tablet-2 | true, every count equal |
| Old-H1 pins updated: myreadiness row, playbook.ts:150, event-states:56 | true (both e2e lines are h1() pins) |
| No data write, API, contract or migration change | true |
| NEW WORDS 2 and 3 | true, exact; NEW WORDS 1: see F3 |
| Ports 9700-9709 0 listeners | true (0 at my check) |
| Head = 9302bc0 by ls-remote | true |

## NOT RUN (hosted CI is the proof)
- api, api on SQL Server (needs .NET + SQL Server/Azurite containers; no api path changed).
- infra Bicep validate and shellcheck (no infra or *.sh change). Only the hidden-character scan ran from this job.
- secrets (gitleaks full history): not run. I ran a regex secret scan over the diff and messages instead.
- npm audit / audit-dev, dependency review: no dependency change (package.json/lock diff empty). Not run.
- CodeQL, deploy-package steps.
