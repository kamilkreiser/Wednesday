GATE B1497: GO WITH FINDINGS @ 4f084fb on main 009421a

Gate: independent QA, tier 2 (Sonnet), commissioned by Tuesday 2026-11-11 ~15:4x AEDT. Project HPSM-POC (folder `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC`, repo `datasecau/HPSM-POC`). Subject: branch `b1497/hpsmpoc-customer-look-a11y`, READY head `4f084fb302a44b004e7efee8b666952120889011`, 5 commits on main `009421a28616c8b31dde86b59d4c4ca674c288fa`. Nothing pushed, no PR, no Jira, no mail, no az, no hosted HTTP (localhost ports 9661-9666 only; GitHub read calls: `ls-remote` and `gh api -X GET` for pulls and main). `lsof` 9660-9669: 0 rows at the end.

Nothing found above Minor. No security-shaped issue. The four product changes and the three test lines do what the kit and ANSWER-1 say, and every new or edited test fails when its fix is removed.

## Findings

| # | Sev | Where | Finding | Instrument / evidence |
|---|---|---|---|---|
| F1 | Minor | P3 `PlaybookShell.tsx` (every `/playbook` page) | Keyboard order changed. The skip link still works (`#main` hash set, `:target` is the single `<main>`, exactly one `main` and one `#main` on 34 of 34 page cells), but `<main>` now starts with the top line, so the first Tab after "Skip to main content" lands on the product-name link "HP Security Services Playbook" (`/playbook`) instead of the first content link (`/playbook/introduction`). One extra tab stop; a screen reader reads the product name and "N of 11 modules viewed" first inside main. Not a WCAG 2.4.1 failure (the skip target is the start of main). It is the direct, intended consequence of the ruling "put the top line in main"; recorded so HP's reviewer is not surprised. | `probes/p3.spec.ts` skip-link section at 390 and 1280: main-tree `afterTab` = link `/playbook/introduction` ("HP Print Security Services Playbook"), head `afterTab` = link `/playbook` ("HP Security Services Playbook"), both inside main. Control: the same section run twice at main (`main`, `main2`) returns the identical `/playbook/introduction`, so the difference is the change, not noise. |
| F2 | Minor | ANSWER-1 item 1, `FindingDetail.test.tsx:56` | Condition (a) of ANSWER-1 words the control as "RED when the card's count is wrong (or the card is removed)". The edited line `card(/^Evidence \(\d+\)$/)` goes RED when the card is removed, renamed or its count is not a number, but a wrong NUMERIC count (title "Evidence (99)") stays GREEN. The unedited line `/^Evidence/` behaved the same (measured: main test + main source + "Evidence (99)" = 7 of 7 green). So no assertion was loosened; the "wrong count" half of the wording was never a property of this test. | `probes/mut_unit.sh` F1 (card renamed: RED, 2 tests incl. the new region row), F2 (count "(many)": RED), F3 (count 99: GREEN), F4 (evidence id cell blanked: RED). Main-blob control run separately: 7 of 7 green with count 99. |
| F3 | Minor | STATUS, P0 closure lines | The builder's control figures "379 in 8 of 8" (C2) and "401 in 8 of 8" (C3 the earlier ticket note) do not reproduce as 8 of 8. Mine: 379 / 401 in 4 of 8 cells (sample-b under all 4 roles), sample-c reads 360 / 390 even with the mutation (its stage pill is short). The control still fires and the pass predicate (360 / 390 at main in 8 of 8) reproduces. Also: the "2 rows each (1 linked, 1 plain)" Recent-activity claim: on a fresh mock sample-c shows 1 plain row; sample-b shows 1 linked + 1 plain, gap 3 px both, as claimed. These closures are on main and not in this diff. | `probes/p5.spec.ts` at main (port 9661) and at a mutated copy (9663: `parts.tsx:69` `md:whitespace-nowrap` -> `whitespace-nowrap`; menu list `fixed` -> `absolute right-0 mt-1` with the two style writes dropped). the earlier ticket note: main 5 of 5 items inside the viewport and hit by `elementFromPoint` for each of Admin, Consultant, Partner, Demo (20 of 20); mutant 5 of 5 inside, 0 of 5 hit (0 of 20). C1 control (old row markup) NOT RUN by me. |
| F4 | Note | STATUS, "vitest at main goes red (10 timeouts) at load 25 to 32" | Not reproduced. Main vitest whole was green (0 failed) at load1 7.53 at start and again at load1 34.1 at start. The builder's own explanation (machine load) stands only for the timed e2e specs: at main the shard `journey-and-prototype` had 1 red, `a11y.spec.ts:39` (30 s test limit) at load1 37.4; the same shard at head was green at load1 22.6. That spec walks the whole journey and does not open a page this branch changes beyond what the other shards cover. Grade: the vitest claim is "not shown"; the e2e load claim is true. | `vitest_*.log`, `shards*.log` (table below). |
| F5 | Note | P1 look | The run list is now the full page column; the profile card (`ApiSteps.tsx:97`) and the follow-up panel (`FollowUpPanel.tsx:99`) keep `max-w-3xl`, so at 1440 px they stop at 768 px while the list runs to the full column. That is what the feedback asked for (tile only) and what the builder HELD as a question. I did not measure those two blocks' edges. | Builder's HELD note; `ApiSteps.tsx` diff is the one class string. |
| F6 | Note | Landing rule | The project's own `CLAUDE.md` is silent on how a PR lands. The head-pinned squash is stated in the project's records (a builder status file of 2026-10-27 under `1_Project_Definition/Briefs/`, line 133, citing CLARIFICATIONS line 138; the kit and an earlier gate kit cite `CLARIFICATIONS.md:3617` in the analysis repository: "The landing form is a head-pinned squash"). I did not open the analysis repository. Squash form used in `landing.txt`. | `grep` of the project folder. |
| F7 | Note | Gate process | Two commands of mine contained a `cd` inside a subshell (one `cd $G/head/web && npm ci ...`, one `cd /tmp ...; true`). They changed no file and no state outside my own clone; disclosed because the fence says no `cd`. The first run of `npm ci` in `head` was done that way; its result was re-checked (`node_modules` 368 entries, rc 0). | transcript |

## What I checked (all against the clone `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s267/gate1497/`, push URL `invalid://no-push`)

### 1. Refs, partition, merge
- `git ls-remote` branch = `4f084fb302a44b004e7efee8b666952120889011` (READY sha); main = `009421a2...` at start and at the end (read twice). `merge-base` = main.
- 5 commits, author = committer on every row (the project's configured identity). Messages carry the Sonnet trailer; the squash replaces them.
- 11 changed paths, all inside the OWNS: 8 owned (`ApiSteps.tsx` + new `ApiSteps.snapshotTile.test.tsx`; `FindingDetail.tsx` + new `FindingDetail.region.test.tsx`; `PlaybookShell.tsx` + `PlaybookShell.test.tsx`; `steps.ts` + `steps.test.ts`) and the 3 ANSWER-1 lines (`FindingDetail.test.tsx`, `playbook-customer-screens.spec.ts`, `layout.test.ts`): 11 of 11. No package, API, migration, `.github`, `infra`, `web/scripts` or other e2e path.
- Open PRs: 0 (`gh api -X GET pulls?state=open` length 0; control `pulls/99999` = 404). Sibling kits of 2026-11-11: the lane H-B/H-D kit lists exactly these 11 files as NOT its own and the lane H-C kit names none of them; overlap 0 (basename search of the kits, not a full OWNS parse). Branch-name overlap with other open branches: none checked beyond the builder's list.
- `git merge-tree --write-tree origin/main origin/b1497/...`: rc 0, tree `706b79f59dc89da0b3f0c43c197e7b9956ddb13c` = the head's own tree (main is the merge base, so the merged tree is the head tree: main plus the 11 head blobs). Controls: a planted conflicting title edit on main printed `CONFLICT (content)` in `steps.ts`; a planted disjoint README line returned rc 0.
- Merge would not deploy: `ci.yml` runs on push to main, pull_request and dispatch; header says "No deploy job"; it keeps deploy packages only. No deploy workflow exists.

### 2. CI jobs that read the changed files (counts by program; load1 beside each; this machine is shared and sat at 5 to 37)
`web-build` steps: `npm run lint` rc 0, `npm run typecheck` rc 0, `npm run build` rc 0 at head; build rc 0 at main; `node scripts/e2e.mjs --check-shards` rc 0 ("every test in exactly one shard") at head.

`web-unit` (vitest whole, `npm test`):

| run | tree | load1 at start (end) | files | passed | failed | skipped |
|---|---|---|---|---|---|---|
| 1 | head | 8.80 (17.20) | 291 | 4219 | 0 | 0 |
| 1 | main | 7.53 (23.03) | 289 | 4216 | 0 | 0 |
| 2 | head | 21.94 (34.12) | 291 | 4219 | 0 | 0 |
| 2 | main | 34.12 (31.78) | 289 | 4216 | 0 | 0 |

Head minus main = +2 files, +3 tests (the three new rows), 0 failed either side, in both runs. The merged tree equals the head tree, so the merge run is the head run. Run 1 head started at load1 8.8, a little above the ~7 target; I could not get the machine under 7 again (others' load).

`web-e2e`: all 8 shards run whole at head and at main (the `git grep` list of specs that open a changed page is every shard; `playbook-walkthrough.spec.ts` and `walkthrough-uat.spec.ts` are in the playbook shards). Ports 9662 (web), 9664-9666 (hosted, stub, chooser).

| shard | head: passed / skipped / failed (load1 at start) | main: passed / skipped / failed (load1 at start) |
|---|---|---|
| playbook-desktop-1 | 64 / 4 / 0 (5.90) | 64 / 4 / 0 (21.09) |
| playbook-mobile-1 | 63 / 5 / 0 (9.50) | 63 / 5 / 0 (24.34) |
| playbook-desktop-2 | 54 / 13 / 0 (10.96) | 54 / 13 / 0 (19.99) |
| playbook-mobile-2 | 52 / 15 / 0 (10.56) | 52 / 15 / 0 (17.53) |
| prototype-desktop-2 | 177 / 4 / 0 (13.45) | 177 / 4 / 0 (15.33) |
| prototype-tablet-1 | 181 / 1 / 0 (17.36) | 181 / 1 / 0 (24.43) |
| prototype-tablet-2 | 177 / 4 / 0 (18.88) | 177 / 4 / 0 (29.09) |
| journey-and-prototype | 2 + 182 + 14 / - / 0 (22.55) | 2 + 181 + 14 / - / 1 (24.67; red: `a11y.spec.ts:39` 30 s timeout, load1 37.4 at the end) |

Skips are the live-API, on-demand-screenshot and touch-keyboard ones, equal at both. The one red is at main, load-driven, and is not a head failure.

`infra`: `infra/tests/test_hidden_characters.py` 14 tests OK at head and at main (it walks every tracked file). Control: a planted U+200B appended to a tracked file in my copy makes it `FAILED (failures=1)`; restored, OK. `bash -n` over the 6 tracked `*.sh`: 6 of 6 ok. shellcheck and bicep are not installed here: NOT RUN.

### 3. (a) The three ANSWER-1 test lines: each proven, nothing else changed
- Exactly one line each: `git diff` shows `FindingDetail.test.tsx` +1/-1, `playbook-customer-screens.spec.ts` +1/-1, `layout.test.ts` +1/-1; the other files in the diff are the new tests, one new row in `PlaybookShell.test.tsx` (+8/-0), and `steps.test.ts` (+1/-1, the title). No other test line changed.
- Item 3 `layout.test.ts:31` (`... || line.includes("${PAGE_X}")`), run in my own mutation copy: baseline at head 6 test files / 32 tests green. Pre-edit line against head sources: RED (1 failed, names the PlaybookShell main line), so the edit is needed. Plant `<main className="px-2">` in `CustomerShell.tsx`: RED. Plant `<main className={`max-w-5xl ${PAGE_X}`}>`: RED (2 failed: the row and the cap rule). Plant `<main className="PAGE_X-ish px-2">` (PAGE_X only as text, not a template part): RED, so the new clause does not accept just the word. Restored by copy, sha equal each time. The edited test also passes against MAIN's `PlaybookShell.tsx` and `FindingDetail.tsx` (10 of 10 green), so the edits are not fitted to the head only.
- Item 1 `FindingDetail.test.tsx:56`: see F2 (renamed card RED, non-numeric RED, evidence row blanked RED; wrong numeric count green as before).
- Item 2 `playbook-customer-screens.spec.ts:169` (`name: /^Evidence \(/`), built and served, `--project=playbook-desktop --no-deps -g "the demo path"`: the unedited spec (main's file) against the head build = RED, `strict mode violation: getByRole('region', { name: /^Evidence/ }) resolved to 2 elements`; the edited spec against the head build = GREEN (6.5 s); the edited spec against a rebuilt copy with the card renamed to "Proof (" = RED (`element(s) not found`). The two shards that hold the spec are green at head in the shard table above (playbook-desktop-1, playbook-mobile-1).
- Each new unit row, with its source reverted to main's blob in my copy: `ApiSteps.snapshotTile.test.tsx` RED / GREEN at head; `FindingDetail.region.test.tsx` RED / GREEN; the `PlaybookShell.test.tsx` row RED (1 failed, 6 passed) / GREEN (7); `steps.test.ts` RED (1 failed, 12 passed) / GREEN (13).

### 4. (b) P3 landmark and accessibility (`probes/p3.spec.ts`, production build, mock API, Consultant)
17 page states x 2 widths (390, 1280) = 34 cells: Playbook home, all 11 module pages, the home again, the snapshot runner, its review state, the page after "Complete snapshot", and `.../result`.
- Exactly one `<main>` and one `#main` and no `[role=main]`: 34 of 34 at main, 34 of 34 at head. Header, footer and navigation counts equal.
- axe (project tags): `region` (moderate) 1 node in 34 of 34 at main, 0 nodes in 34 of 34 at head; head lists no other rule at all; no rule id at head that main lacks.
- Page text equal in 32 of 34 (the 2 that differ, the snapshot module page at both widths, differ only in a run-list timestamp "Started 3:42 pm" vs "3:44 pm"; control: a second run at main differs from the first run in the same cells for the same reason). Full-page screenshots are pixel-identical (sha256) in the same 32 of 34. Boxes of `[data-testid="modules-viewed"]` and the first `h1`, document `scrollWidth` and `scrollHeight` equal in 34 of 34. `<main>`'s own box now includes the top line and the full padded width (intended).
- Accessibility tree diff (home, runner): the top-line link and "N of 11 modules viewed" moved from before `main` to the first two items inside it; nothing else.
- Skip link: Tab 1 = "Skip to main content", Enter sets `#main`, `:target` = MAIN, at both widths, main and head. See F1 for the one behavior change.
- Print rules in `globals.css:167-169` (`main button`, `main [role=tablist]`, ...) cannot reach the top line (it has `no-print` and holds a link and a paragraph); the print spec runs in the playbook shards, green.

### 5. (c) P4 words, byte for byte
- The menu entry (`GlobalNav.tsx:50`) label bytes `44656c697665727920706861736573` ("Delivery phases"); the new title is exactly that byte string followed by `: Assess / Implement / Optimize`, all ASCII. The old title had the same tail (compared by program). Page title (`services/page.tsx:4`), crumbs and `ServicesHub` header carry the same label.
- Diff of all string literals, template parts and JSX text, head minus main, per changed product file (`probes/lits.py`; control: a planted JSX word and a planted class literal are both found): `steps.ts` +"Delivery phases: Assess / Implement / Optimize" -"Service offers: Assess / Implement / Optimize"; `FindingDetail.tsx` +`@/components/ui/Table` (an import path) and the caption string now a constant (the same bytes: "Evidence behind this finding" removed as JSX text, added as a literal); `ApiSteps.tsx` the class string without `max-w-3xl`; `PlaybookShell.tsx` none. No other user-facing string changed. The step's `key`, `purpose`, `cue`, `say` and `caveat` are untouched (diff has only the title line and one comment line).
- `git grep -i -F "Service offers: Assess"` at head: 0 (main 2). Remaining "service offers" hits: step 11 spoken notes (`steps.ts:138`), a code comment (`ServicesHub.tsx:1`), and tests that assert the old name is absent (`PartnerDashboard.tiles.test.tsx`, `PartnerDashboard.words.test.tsx`) and one e2e spec comment: none is a heading.
- The code comment on the step cites the 2026-11-11 ruling; no person's name, no card id.

### 6. P1 and P2 re-measured (`probes/p12.spec.ts`)
- P1 (Consultant, `/customers/sample-c/assessment`, one run): list right edge vs engagement section vs Next row: 1024: 996.14 / 996.14 / 996.14 main and head; 1280: 1243.19 x3 main and head; **1440: main 1280.41 / 1397.59 / 1397.59 (red), head 1397.59 x3 (equal)**. Page text equal main vs head at all three widths; no sideways scroll.
- P2 (Consultant, quollridge scored, F-001 and F-002 at 360, 390, 412, 1280): `scrollable-region-focusable` (serious) on F-001 at 360: 1 at main, 0 at head; 0 everywhere else; no new rule id at head; text equal 8 of 8; unfocused pixels identical 8 of 8. At head the scroll box is `role=region`, `aria-label` = the caption "Evidence behind this finding", `tabindex=0`; Tab reaches it with a 3 px `:focus-visible` outline at 360 and 390.

### 7. Scans (added lines and commit messages)
- Names (the 9-name ban list plus the project's people lines; underscore-aware `(?<![A-Za-z])<name>(?![a-z])`): 0 in 98 added lines and 0 in the 5 messages; control `_by_<name>_` planted for the first name fires (1).
- Secrets, tenant/subscription ids (GUID pattern), hosts: 0 real; the only URL-like text is the test stub `http://mock.test`. gitleaks over `009421a2..4f084fb3`: rc 0 "no leaks found"; canary (random ghp-shaped value in a scratch repo): rc 1.
- Cf/Cc characters: 0 in added lines and messages (control U+200B detected); non-ASCII in added lines: 1, the existing en dash in the time field `t` of the step on the changed title line (unchanged text).
- CodeQL pre-scan over every added line, tests included: `new RegExp(` 0, hand-escape `.replace(/[...]/g` 0, `innerHTML` / `dangerouslySetInnerHTML` 0, `child_process` 0. Regex literals added in tests are constants. No Major.
- Ticket keys, B-numbers and seat ids in added lines and messages: 0.

### 8. Builder's claims graded

| Claim | Grade |
|---|---|
| Head vitest 4219 passed, 0 failed, 291 files | true (twice) |
| Main vitest 10 failed / 4206 passed under load | not shown (main green twice, load1 7.5 and 34) |
| All 8 e2e shards green at head, equal skips | true |
| Main e2e shard counts equal | true (journey shard has one load-driven red at main) |
| P1 edges 1440: 1280.41 -> 1397.59, equal within 1 px | true |
| P2 axe 1 -> 0 at 360, no new rule, text equal | true |
| P3 `region` 1 node in 30 of 30 at main, 0 at head, boxes equal | true (mine: 34 cells) |
| New words: only the P4 title | true |
| 357 / 399 pass predicates at main | true (360 in 8 of 8; 390 with letter spacing in 8 of 8; menu 20 of 20) |
| 357 / 399 control "8 of 8" | partly true: control fires in 4 of 8 (F3) |
| 439 gap equal for linked and plain rows | true on the cells with both kinds (3 px, 3 px); control not re-run by me |
| Three ANSWER-1 controls | true; item-1 wording gap in F2 |
| Hidden characters 14 OK; `bash -n` 6 of 6 | true |
| shellcheck, bicep, npm audit: not run | true (not run by me either) |

## NOT RUN
Hosted CI and hosted CodeQL on this head (no PR exists; hosted CI is the proof for `api`, `api-sqlserver`, CodeQL and the audit jobs). shellcheck v0.11.0, bicep and `bash infra/scripts/validate.sh` (tools not installed). `npm audit` steps (registry; no package change). Live-API e2e specs (no API). The closed-line control for C1 (old Recent activity markup). A screen-reader pass (VoiceOver / NVDA) over the Playbook landmark order; Safari, Firefox, real phones; print rendering of the Playbook pages. The UAT half of 357 and anything hosted. The profile-card and follow-up-panel edges at 1440 (F5). The vitest-under-load behavior the builder described (not reproduced, F4).

## Landing (Tuesday)
Head-pinned squash, files in this folder: `landing.txt`, `squash-subject.txt`, `squash-body.txt`, `pr-title.txt`, `pr-body.txt`. The squash replaces the five commit messages. The figures in the bodies are mine.

## Files
`VERDICT.md`, `pr-title.txt`, `pr-body.txt`, `squash-subject.txt`, `squash-body.txt`, `landing.txt` in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-11_B1497_verify/`. Evidence (logs, probe scripts, JSON outputs) stays in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s267/gate1497/out/` and `.../probes/`.
