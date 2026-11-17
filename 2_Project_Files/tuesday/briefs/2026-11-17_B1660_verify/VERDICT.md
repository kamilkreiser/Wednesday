GATE B1660: GO WITH FINDINGS @ 96650be on main 5a79f8a

Tier G2, one round over the combined branch (two commits, 5f6b916b then 96650be6). Own clone in /private/tmp/b1660-gate/, local builds, ports 9870-9873 only (0 listeners before and after every run), nothing pushed, no PR, no merge, no Jira, no mail, no board, no az, no hosted HTTP. Evidence: `evidence/` in this folder.

## Refs, diff, merge
- `git ls-remote` branch = 96650be664c5f1528e09c158b76413e38b614f82; main = 5a79f8a47bac26d093fe2eb3bd55ae83817dd4ff (read at the start and again at the end). `gh api compare`: ahead 2, behind 0. Open PRs 0.
- Diff against main is exactly 3 files: `RevenueCalculator.tsx` +1 -1, `Revenue.restyle.test.tsx` +39, `web/e2e/html-layout.spec.ts` +73 (numstat by program). Only line 220 of the component changed (by program over every line; the rest of that line is equal once className is removed). Overlap with open PRs 0 (none open).
- `git merge-tree --write-tree origin/main HEAD` is clean and its tree (62b8f34d) equals the head's tree (main has not moved).
- No word, label, hint, unit or figure changed: the 65 label/hint/unit/title strings of `STEPS` are equal at main and head by program (control: a planted unit edit differs); the whole component file is equal apart from line 220; unit and label/hint text read from the rendered page are equal at 1280, 820 and 390 (96 rows).

## Red at main, green at head (right reason)
- A5 (vitest, restyle file): at main red by assertion `expected [ 'flex', 'max-w-32', ... ] to include 'w-[5.375rem]'` (1 failed, 7 passed); at head 8 passed.
- T20 (`html-layout.spec.ts -g T20`, desktop and tablet, workers 1): at main both red by soft assertions P1 (boxes differ in width), P3 (boxes differ in left edge), Q3 (long unit 3 lines, box taller than 44.5); 0 timeouts, 0 positive-control failures. Q1 and Q2 hold at main by construction (main's number box is wide and its hints are 203.2 px). At head 2 passed (desktop, tablet).

## Measured properties (own script measure.mjs, 1280 / 820 / 390, steps 1, 3, 4; head against main)
Controls that fired: fixture boxes of known width 100 and 140 read 100 and 140, a fixture hint set to 100 px reads 100; boxes per step 6, 4, 6 in every frame; a planted line-count difference is caught by the comparison.
| property | main | head |
|---|---|---|
| P1 all 16 boxes one width | 28.1 to 85.0 px | 86.0 px, spread 0.0 (all three viewports) |
| P3 left edges per step (1280) | boxes' left edges spread 48.2 px (step 1), 0.0 (step 3), 56.9 px (step 4); inputs 0.0 | inputs 0.0 and boxes 0.0, steps 1, 3, 4 |
| Q1 number box / grey box (1280) | n/a (139 to 195.9 px inputs) | smallest 1.605 (inputs 138.0 px, boxes 86.0 px) |
| hint widths (1280 / 820 / 390) | 203.2 / 498 / 316 | identical: 203.2 / 498 / 316 (0 of 96 rows differ) |
| label and hint line count, 96 rows | - | 0 differ from main (control fires on 1 planted row); wrapped-line totals 59 / 33 / 40 equal to main |
| Q3 lines | up to 3 | at most 2 (only USD / device / month); smallest room 2.75 px; scrollWidth over clientWidth 0 |
| heights | 44.0, and 50.0 on two rows | 44.0 for all 16 boxes, equal to their input |
Font stress on the head build (default plus Verdana, Tahoma, Trebuchet MS, Arial, Helvetica, Georgia, Geneva injected): Q3 holds in all; smallest room 0.13 px (Trebuchet MS), 0.50 px (Verdana).

## Look (screenshots head2-1280-step1.png and head2-1280-step4.png)
Matches the product owner's two words ("align these", "slim the grey box first"): step 1 shows six grey boxes of one width and one left edge, one line each (USD / hour on one line), the number box clearly wider than the grey box, labels and helper sentences wrapped as on main. Step 4 shows USD / device / month on two lines (USD / device over / month) in a box and input of the same height; no text outside a box. The grey text is small (11 px).

## Runs at head (own clone, load1 6 to 18, one heavy job at a time)
- `npm run lint` rc 0; `npm run typecheck` rc 0; `npm run build` rc 1 then rc 0 (Next's one-shot security notice; same-command retry; no `next upgrade` run, no package file touched); client-bundle line "none of 39 provenance markers".
- Whole vitest: main 4338 passed, head 4339 passed, 304 files each; by program (file, ancestors, title, outcome): lost 0, added 1 (the new A5), changed 0 (control: dropping one head row gives lost 1).
- `html-layout.spec.ts` (desktop, tablet, CI=1, retries 1): 42 passed. `playbook-partner.spec.ts` (playbook-desktop, playbook-mobile, `--no-deps`, CI=1): 14 passed. `node scripts/e2e.mjs --check-shards`: plan OK.
- Infra (python 3.14.10 on PATH, bicep 0.47.16): `test_hidden_characters` 14 OK (control: a tracked file with U+202E makes it fail); whole discover 325 OK; `validate.sh` rc 0.
- CodeQL 2.27.4, javascript-typescript, `javascript-code-scanning.qls` (87 rules) over `web/`: 0 results (no planted-flaw control was run; hosted code scanning stays the proof).

## CI and deploy
`ci.yml` triggers: push to main, pull_request, workflow_dispatch. It has no deploy job and no cloud login (0 hits for azure/login, publish-profile, id-token; control: upload-artifact 8 hits). On main it only keeps the build packages as artifacts. A merge deploys nothing.

## Scans over added lines (113) and both commit messages
Names (ban list plus the project's people line, underscore-aware, control `_by_Kam_` fires): 0. Work ids, seat ids, ticket keys: 0. Secrets, GUIDs, hosts, Cf characters, non-ASCII: 0 (the two "secrets" hits are the local helper `tokens(`, a false positive). CodeQL hand rows (`new RegExp(`, hand-escape `.replace(/[`, innerHTML, child_process): 0. Skip/only/fixme/waitForTimeout/overflow-hidden/truncate/text-ellipsis: 0. Controls fire for every row (`evidence/scan.txt`).

## Findings
| # | Severity | Finding | Recommendation |
|---|---|---|---|
| 1 | Minor | Q3 in T20 depends on the machine's system font: smallest room is 2.75 px here, 0.13 px in the tightest of 7 fonts tried. A hosted runner font wider than any of those would turn T20's Q3 red and block the PR. Not seen here. | Land as is. If hosted T20 goes red on Q3, take the 88 px step (`w-[5.5rem]`, ratio stays at least 1.5) as a new round. |
| 2 | Minor | T20's hint selector is scoped to the step section because the page has one more `-hint` paragraph outside it (not identified; the builder did not name its element either). The row works; the scope is an assumption. | None needed; note only. |
| 3 | Minor (cosmetic) | T20's Q1 message prints the literal "1.5 times", so a future threshold change would not update the text. | None. |
| 4 | Minor (not shown) | I did not re-run the builder's seven mutants or planted-wrong controls; I relied on red at main and green at head. Claim not re-measured. | Accept: the commission did not ask for them; hosted CI plus the measured rows above carry it. |
| 5 | Info | The builder's earlier landing files in the project evidence folder for the first commit describe `w-40` and 16rem and are false for the combined branch. | Use the files in this folder. |
| 6 | Info | `html-layout.spec.ts` has two rows titled T07 (pre-existing, not this change). | None. |

Builder claims graded against my own runs: P1 86.0, P3 0.0, Q1 1.60, Q2 203.2 and 0 of 96, Q3 (2 lines, 2.75 px, 44.0 px), vitest 4339, html-layout 42, playbook 14, infra 14 / 325 / rc 0: all true. Both commit messages are ASCII with one Claude trailer each and no names; they are replaced by the squash text.

## NOT RUN
- The seven mutants and the two planted-wrong controls (finding 4).
- `npm audit` and `node scripts/audit-dev.mjs` (registry HTTP; no `package*.json` change, by diff).
- The other e2e shards in full, the api jobs, the secrets scan, dependency review and hosted code scanning (hosted-only; hosted CI is the proof).
- A CodeQL planted-flaw control.
- Nothing else touched hosted systems.
