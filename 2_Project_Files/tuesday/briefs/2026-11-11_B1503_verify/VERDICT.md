GATE B1503: GO WITH FINDINGS @ a2461ce on main 009421a

Tier 2 (UI classes, one global CSS focus rule, CI-reader tests; no auth, data or deploy surface). Nothing security-shaped found. Own clone (no-hardlinks, push URL invalid) at /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s268/gate1503/; head and main built separately; ports 9670-9676 used, `lsof` 0 listeners in 9670-9679 at the end.

## Checks (all MEASURED by this gate)
- Refs: ls-remote branch = a2461ce7153e8548c21951462fb3581ae38fec13; main = 009421a28616c8b31dde86b59d4c4ca674c288fa (both re-read at 17:28). 7 files changed (6 M, 1 A), all inside the kit's OWNS; none under .github, package*, web/e2e, web/scripts, api. Open PRs: 1 (309, lane H-A, 11 files); `comm -12` with this branch = 0. Identity: 5 commits, author = committer = the project's noreply address.
- Merge: `git merge-tree --write-tree` clean (tree ccf0172); `git diff` merge tree vs head = empty (main plus head blobs).
- vitest whole: main 289 files / 4216 passed; head 290 files / 4222 passed (+6); 0 failed at both. Matches the builder.
- lint rc 0, typecheck rc 0, build rc 0 at head (and main builds). 
- Red without the fix: head's 3 test files copied onto main's tree: 6 failed (moreLink 2, TrainingScreen 3, Button focus-radius 1), 15 passed; all 6 are the new rows. Green at head.
- (a) Focus-rule probe (builder's p3_diag, copied, retargeted to my clones; /customers/sample-b/assessment; consultant and partner at 1280 and 390; 111 focused elements, main vs head): unfocused radius differs for 0 elements; Feedback pill 4/4 equal 9999px -> 9999px, cornerDiff 0 at both trees, focused radius identical main vs head; sidebar rows (.sidebar-ring) focused radius identical main vs head (4px at both: the spec decision left open); Button/ButtonLink 14/14 changed at main, 0/14 at head; rounded-full chips 8/12 changed at main, 0/12 at head; 44 own-radius non-sidebar elements changed focus radius main vs head, all of them violators fixed; 0 unexpected changes. Elements with no own radius still 0px -> 4px at both (unchanged). Control: the sidebar current item "Customers" reads 8px -> 8px at both.
- (b) every new unit row is red against main (6 of 6 above).
- (c) P5 plants (builder's p5_plants.py re-run by me): P-a to P-h: main's reader green (Ran 36 rc 0), head's rows red (Ran 40 rc 1) each naming the matching pin row plus the plants row; controls C-1 SHA bump, C-2 tag bump, C-3 digest bump, C-4 unplanted: green in both. Real file: test_ci_workflow.py head Ran 40 OK, main Ran 36 OK. test_hidden_characters.py Ran 14 OK at both. Whole infra/tests discover (no bicep here): main Ran 181 failures 1 errors 4; head Ran 185 same failures 1 errors 4 (4 setUpClass = bicep absent; 1 = Python 3.9 test-name format row); same set at both, so not this lane's.
- (d) New words: head minus main literals: parts.tsx 1 (class string), TrainingScreen.tsx 3 (class strings), non-class words EMPTY, planted control found. Diff read by eye: only classes and comments change; no aria-label, title, tooltip.
- Scans over 239 added lines + 5 commit messages: ban list (Kam, Kamil, Kreiser, Steve, Peter, Paul, Blanchard, Inch, Waite) 0 hits, every `_by_<name>_` control fires; non-ASCII/Cf 0; secrets/ids/hosts 0 (one `https://example.invalid/...` plant string inside a test, not a host); CodeQL pre-scan: no `new RegExp(`, no hand-escape replace, no innerHTML, no child_process.
- e2e at head, all 8 shards on the mock build, whole shards: journey-and-prototype 182 passed; prototype-desktop-2 177 passed 4 skipped; prototype-tablet-1 181 passed 1 skipped; prototype-tablet-2 177 passed 4 skipped; playbook-desktop-1 64 passed 4 skipped; playbook-desktop-2 54 passed 13 skipped; playbook-mobile-1 63 passed 5 skipped; playbook-mobile-2 52 passed 15 skipped. 0 failed. Counts equal the builder's.
- Deploy trigger: .github untouched; nothing deploys on merge.

## Findings
| # | Sev | Finding |
|---|---|---|
| 1 | Minor | The landing form (head-pinned squash) is not in the project's CLAUDE.md (grep -n -i for squash, head-pinned, match-head-commit: 0 hits); it is in the analysis repo CLARIFICATIONS line 3617 as the kit quotes, and in earlier HPSM briefs. Used as the kit says. |
| 2 | Minor | The global rule `[class^="rounded-"]` / `[class*=" rounded-"]` matches plain `rounded-*` only. A responsive or variant radius (e.g. `md:rounded-lg`, `focus:rounded-md`, the skip link) is not matched and still squares to 4 px on focus. Intended and stated by the builder; not a regression. |
| 3 | Minor | The sidebar rows (.sidebar-ring) still square to 4 px on keyboard focus; pinned as "the ring it always had" by shell-sidebar.spec.ts:290-296. A spec decision left open, as stated. |
| 4 | Minor | Builder note, confirmed as environment: a11y.spec.ts:39 is near its 30 s timeout under load at main too; it passed here (journey shard green at load 7). |
| 5 | Minor | The Button focus-radius unit row and the MoreLink/TrainingScreen rows are class and source pins (jsdom paints no corners); the layout proof is the probe, which I re-ran for the focus rule only. |

Not a finding: hosted api CI jobs on main are red for the .NET SDK runner drift (separate fix seat).

## NOT RUN
- `npm audit` and `scripts/audit-dev.mjs` (network registry; package files untouched).
- shellcheck (not installed) and the infra job's `validate.sh` / baseline runner (bicep absent here); the Python 3.11+ row. Hosted CI is the proof for those.
- Probes P1 (MoreLink heights at 4 roles x 4 widths), P2 (Training look at 5 widths, screenshots) and the P3 80-route census: not re-run; class-level reading plus unit rows and the 8 green shards stand in; builder's numbers for them are not shown by this gate.
- Merge-tree CI: tests run on head and main trees; the merge tree is byte-equal to head so a separate merge run adds nothing.
- Any hosted, demo, UAT or production host; az; docker; Jira, mail, PR.
