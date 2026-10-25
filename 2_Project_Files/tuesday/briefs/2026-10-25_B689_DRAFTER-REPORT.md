STARTABLE: YES (after your stamp; one dated premise to re-check at the stamp: main must still be `dbbf5881` and the pair 5102/306, see UNMEASURED and Q-3)

# B689 drafter report (NexusAI lane N-GUARD, RD-844), drafted 2026-10-25 19:2x-19:5x AEDT

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-25_B689_SEAT-M11_nexusai-844-banner-guard.md` (131 lines). Seat `Datasec/NexusAI-M11`, ports 9820-9829, model C2 Sonnet `claude-sonnet-5-5`, launch carries `BRIEF_SEAT_LEVEL=sonnet` and `WED_USAGE_STOP=100`.

## BLUF
- The ticket is startable and the ruling (C-221, `CLARIFICATIONS.md:2386-2390`) already exists in the project record with its scope and three conditions; the kit copies them verbatim. The ruled fix is a page-level route in the guard that answers exactly the Font Awesome 6.0.0 URL with an empty stylesheet, plus a count assertion inside the EXISTING `test.each(PAGES)` cell.
- **Count-neutral is proved by arithmetic on the sources and made a hard STOP by run:** 12 pages + 46 red cells + 2 identity pages = 60 measurements; 6 + 60 = 66 tests in the rd490 file. The gate that judges the counts (`verify-suite.sh:87-92`) fails in EITHER direction against the counts file (now 5102 / 306, not the 5005 / 305 of the older kits). So the kit forbids any new `test(`, `it(`, `describe(`, `.each` row or file, requires the 66 titles identical before and after, and requires one full verify at the head reading the pinned pair; any difference is a STOP, never an edit of the counts file.
- The one trap that the earlier attempt fell into is written into the kit: `waitUntil: 'domcontentloaded'` was INERT on the real setup and status pages (B621-1); `waitUntil` stays `'load'`.

## Facts re-measured (instrument, control)
| Fact | Reading | Instrument | Control |
|---|---|---|---|
| main | `dbbf5881f1594916d4abb90df884ea4ad42ef80c` | `git ls-remote origin refs/heads/main`, 19:27 | the same call lists the b-branches I compared |
| open PRs | only #115 (`records/b681`, `813a94f1`), files `HISTORY.md` | `pulls?state=open`, `pulls/115/files` | `pulls/112/files` lists the 3 files incl. the counts file; `pulls/99999` 404 |
| branches vs main | b617, b632, b642, b658, records/b362, b605, b656: ahead 0, 0 files; records/b681: ahead 1, `HISTORY.md` | `compare/main...<branch>` | `19b7106b...6e076b29` lists 6 files |
| guard file | blob `0d74337f`, 17810 B, 339 lines, `:294` `waitUntil: 'load', timeout: 20000` | contents GET (raw + blob sha) | blob equals the unmodified base gates B621 and B637 recorded; a nonexistent path 404s |
| rd490 test | blob `75ed1aa5`, 17442 B, 347 lines | same | same |
| counts file | blob `a8085c1d`, tests 5102, suites 306 | contents GET | the B667 gate STATUS reads the same pair from a local verify |
| pages | 14 html, 2 EXEMPT, 12 measured | contents listing of `static/` | 12 equals the "12 pages" the guard comment and the 60-measurement arithmetic need |
| red / identity cells | 30 concealments, 46 (concealment, page) pairs, 2 identity pages | small python over the concealments file | planted 3-page entry counts 3 |
| tests / measurements | 66 / 60 | 6+12+46+2 and 12+46+2 | equals the 66 gate B625 expected and the "60 measurements" in B621/C-221 |
| cdnjs requests in pages | exact FA 6.0.0 link in setup:8, status:9, marketplace-landing:9 (exempt); prose mention in first-run-setup:2258 | read all 14 pages, grep | jsdelivr counts per page printed (the grep fires); naive `cdnjs` search gives 4 files, requests are in 3 |
| Deploy demo | variables 0, environments `["dev"]`, last 5 runs push/skipped | `actions/variables`, `environments`, `workflows/deploy-demo.yml/runs` | `build.yml` runs listing shows real conclusions (success) so the field fires |
| Deploy-demo trigger | `on: push branches [main], paths-ignore '**.md','docs/**','tests/**'`, plus dispatch | file at the sha, lines 26-33 | n/a |
| RD-844 | To Do, 1 comment | Jira GET via the HPSM-POC read helper (read whole first) | `project = RD AND ( text ~ "zzz-no-such-string-7f3a" )` = 0 |
| next builder name | highest used NexusAI-M is M10 (B658) so M11 | word-boundary scan `NexusAI-M[0-9]+\b` over 135 non-`.pre-` SEAT kits of 10-24 and 10-25 | scratch `x NexusAI-M99 y` matches once |
| ports 9820-9829 | free; kit hits: B632 (M7, finished, previous owner), B658 and B662 only in their own control sentence `x 9820 y` | `lsof -nP -iTCP:9820-9829 -sTCP:LISTEN` rc 1; word-boundary scan | scratch `x 9820 y` matches once; live panes list has no NexusAI pane |
| 38900-38939 (the rd490 test's own band) | 0 listeners | `lsof` | the test itself proves each port by refusal |
| lock tool | sha256 `3c33f5ae...` unchanged; `queue-jest` empty | `shasum`, `ls` | equals the value B658 stamped |
| load | 8.93 / 8.88 / 8.33 at 19:30 | `uptime` | n/a (wait rule) |
| sweep rows | RD-844 lane N-GUARD, count-neutral, M, Sonnet; YOURS are exactly the two paths | sweep lines 133 and 192 | the counts file and `HISTORY.md` are in NOT YOURS as the commission says |

## Landing rule (quoted in the kit with source)
`CLARIFICATIONS.md:2067` "Merge path: open a PR from the gated branch, wait for CodeQL (a background wait that EXITS), then land the SAME commit. Never squash, never rebase ([[C-68]])." `:2068` no dismissal, `:2073` wait for every `Analyze (<language>)`; C-68 `:665`, C-209 `:2270`. Deploy trigger: `deploy-demo.yml` lines 26-33 (push to main only, `tests/**` ignored). Observation worth your eye: `tests/**` does not ignore `__tests__/`, so the eventual merge DOES start a `Deploy demo` run (expected `skipped`: variable unset, last 5 runs skipped). A branch push starts none. The kit states both.

## D-decisions (mine; each recorded in the kit)
- D1 Seat name M11 (highest M seen is M10; the pane is not live).
- D2 Exact-URL predicate for the stand-in (the ruling names one stylesheet); any other cdnjs request is left real and is not hidden. A page-level `page.route` inside `guardPage` (so the guard owns its independence), not a context route in the test.
- D3 The count assertion lives INSIDE the existing `test.each(PAGES)` cell, with the expected number derived from the page's own file (no typed page list); the "regression cell" B621 suggested becomes a measured harness in `session-tools/b689/` (a jest cell would move the counts).
- D4 `waitUntil: 'load'` kept (B621-1).
- D5 One full verify at the head is REQUIRED (the pinned counts are the CI predicate), with the escape "jest UNMEASURED" if the machine stays above load 7 for 60 minutes.
- D6 Target READY 3 h, HARD STOP 5 h after Step 0 (the template used 2 h / 4 h; the last full verify ran about 28 minutes and the lock may be held).
- D7 Gate after: G2 tier 2 (Sonnet, tests-only) as the default; see Q-1.
- D8 The PRIOR-WORK CHECK standing line is verbatim in its first and last sentences ("before the first git write in your clone" ... "returned unread") and lane-specific in the middle: it names B617, B621, B625, B637, B656 and the C-entries, and adds a PRESERVES clause (waitUntil load, the 60 measurements and 66 cells, the exact URL) as the learnings on prior-work sections require.
- D9 The harness boots ONE product server on 9820 with a contained HOME of its own; it is heavy and outside the jest lock, so the kit gates it on load below 7 and one run at a time and has STATUS say it ran outside the lock.

## Q-questions for Tuesday (each with a default)
- Q-1 Gate tier: the guard is the only automated check that the open-site banner is visible, so a weakened guard is a security-adjacent test. Default: tier 2 (Sonnet, G2 tests-only) because the change is test-only and the kit makes the gate re-run the stall harness, the census and the full verify; stamp tier 1 instead if you read "security surface" broadly.
- Q-2 Outbound exception: the shipped rd490 test makes the headless browser ask cdnjs and jsdelivr (public CDNs, not a Datasec host), so the baseline jest run and the "with the stylesheet" comparison (a ruling condition) cannot avoid it. Default: allow, disclosed in STANDING LINE 2 as the only exception; remove it and the ruling's third condition cannot be met by run.
- Q-3 Main drift at the stamp: PR #115 (HISTORY.md) is the only open PR and shares no path. Default: stamp PRE-CLEARED with the sha you read; the REFUSE check stops the seat if main moved into the guard, the rd490 test, the concealments file, setup/status pages, `build.yml` or `verify-suite.sh`, and does NOT stop on a counts-file move alone (the seat uses what main pins).
- Q-4 A page that asks a second cdnjs URL: default is "not answered, visible"; the census (Step 5.3) reads live requests and would show it. If you want the cell to FAIL on any unanswered cdnjs request, say so; I left it out because the ruling covers one stylesheet and a new failure mode on a dependency nobody ruled on is a product-owner question.
- Q-5 The kit tells the seat to leave `cdn.jsdelivr.net` real (not in the ruling). Default: leave it; RD-721 (vendoring) is the proper cure and is `Testing`, not on main.

## UNMEASURED
No browser, jest, npm, clone, worktree, fetch, CodeQL or workflow run. In particular: whether Playwright's page route precedes the harness's context stall route (kit Step 5.2 proves it); whether an empty stylesheet leaves banner box/contrast/ink unchanged on setup and status (Step 5.4); whether any page requests a second cdnjs URL dynamically (I read page text, not live requests); the code-search index completeness (the kit re-counts by `git grep`); the `tests/**` glob behaviour in `paths-ignore` (read, not run); whether `marketplace-landing.html` is served; the full-verify wall time at this load; PR #115's build status (not read); the older B658 kit's claim that the whole verify was skipped does not apply here and was not measured.

## Outside-the-fences disclosure
- Loaded the HPSM-POC read helper (`HPSM-POC/.tools/b653/jira.py`) as a module with `python3 -I` and called its `api("GET", ...)` for RD-844 and three JQL searches (all `project = RD AND ( ... )`); that helper reads the HPSM-POC project's `.env` in-process (the commission authorised it). I also ran its `show` path once (`jira.py RD-844`), which only GETs.
- `gh api -X GET` only, under the NexusAI `GH_CONFIG_DIR`, including `search/code` (a GET against GitHub's index). One `gh auth status` call was made (counts "Logged in"; the login was not printed).
- `git --no-optional-locks ls-remote` in the shared NexusAI repo (a read verb); no other git in a project repo.
- Read-only reads of NexusAI's `1_Project_Definition/CLARIFICATIONS.md` (by line), `1_Project_Definition/Briefs/` STATUS files B617/B621/B625 (grep)/B637/B656/B667 (grep) and the B621 evidence folder listing; listed `NexusAI/session-tools` and `HPSM-POC/.tools/b653` directory contents; read `model-routing.md` and `models_latest.json`.
- No `decision_queue.sh` call of any kind (the ruling was read from the project's own `CLARIFICATIONS.md`, not from a card), no `fleet/briefs_staged/`, no scoreboard, no `_ledger.md`, no WEDNESDAY/FRIDAY tree, no other client's project.
- Scratch files only in the session scratchpad (page copies, a Jira query script, the guard and test copies, `jq.py`); no hosted/demo/production host was contacted. One shell command of mine was refused by the pretooluse hook (a bare `=====` word); nothing ran.
- Wrote only the two output files named in the commission.
