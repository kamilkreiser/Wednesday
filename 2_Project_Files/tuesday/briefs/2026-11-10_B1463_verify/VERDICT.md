GATE B1463: GO WITH FINDINGS @ aa9bac7 on main 2211608

Tier 2 (one product string on a sidebar link, tests). No security-shaped issue found. Own clone in the session scratchpad (push URL invalid, never pushed); production builds served on ports 9990-9997 only; 0 listeners left on 9990-9999 after every run.

## Refs and merge
- `git ls-remote` of the branch = aa9bac758b074e959c4e24cf17430076a0b8fd1d = READY sha. Main read now = 2211608276f4cada15b3192c9b8753a5d722a4ef (did not move; #306 not landed at the read). Main is an ancestor of the head (rc 0); one commit.
- Changed paths 7 of 7 inside OWNS (GlobalNav.tsx, GlobalNav.test.ts, AppShell.sidebar.test.tsx, AssessmentsHub.myreadiness.test.tsx, shell-sidebar.spec.ts, playbook.ts, assessments/page.tsx). All under web/; no api, infra, package or lock file.
- Overlap with open PRs: #306 (steps.test.ts only) and #307 (api/**, infra/sql/**) = 0, from the commission's scopes (I did not call the hosted API: fence).
- `git merge-tree --write-tree main head`: clean, rc 0, tree 7bc36502a4ac6981137b18e6698bedcb0b60da48 = the head's tree exactly (main is its parent, so merge = main plus the head blobs). Against a later main the merge is unchanged unless #306/#307 touch these 7 files (they do not by scope).
- A merge triggers CI only (ci.yml: "No deploy job, no cloud credentials"; it only keeps deploy packages). No deploy.

## Findings
| # | Sev | Finding | Evidence |
|---|---|---|---|
| 1 | Minor | The sweeps in shell-sidebar.spec.ts that were tuned to this row's position (window heights 676-684, 648-656, 640, 470, 380, 354) still pass, but the row and everything below it moved down 12 px; I did not re-derive whether those height cells still straddle the boundary they were chosen for. Green is shown, boundary coverage is not. The builder's STATUS says the same pins were kept (no re-measure needed because nothing went red). | 16 whole shards green; wrap table below |
| 2 | Minor | Product-visible: the new label (26 characters) wraps to two lines in the 228 px and 245 px columns; link 44 -> 56 px; rows below +12 px; collapsed rail unchanged. Built as ruled (no class, size or style change). Flag to the product owner; not a defect of the change. | wrap table |
| 3 | Minor | Overlap with open PRs taken from the commission, not re-read live. | step 1 |
| 4 | Minor (pre-existing, same at main) | 46 e2e tests are skipped across the 8 shards (4+1+4+4+13+5+15+0), identical at main and head. | shard table |
| 5 | Info | Git author/committer handle is the repo's existing identity (same on the last 5 main commits); it is commit metadata, not message or added text. | git log |

No Blocker. No Major.

## Claims graded (builder STATUS)
| Claim | Grade |
|---|---|
| One commit aa9bac75 on main 22116082; 7 files, 53 in, 53 out | true |
| Only the link label changed in source; id, href, icon, group, also untouched | true (diff of GlobalNav.tsx: line 44 label, plus two comments naming the link) |
| 49 of 53 added lines are the removed line with the string swapped; 4 differ (3 comments + 1 test title) | true (my program: 4 differ, same 4) |
| Exactly one new product string | true (44 new string tokens, all contain the new string; 0 others; plant of an extra word fires) |
| Hub eyebrow, breadcrumb, runner link unchanged | true (eyebrow AssessmentsHub.tsx:131, ReadinessResult.tsx:44, ReadinessRunner.tsx:236 and their tests absent from the diff; the eyebrow assertion at myreadiness.test.tsx:53 keeps "My readiness"; only its comment changed) |
| Red first (unit): 13 failed / 61 passed of 74 | true (my red copy: 13 failed, 61 passed) |
| Red first (e2e): 42 failed (desktop + tablet) | true for desktop: 21 failed, 86 passed; tablet not re-run (symmetric 107 rows) |
| Whole vitest 289 files / 4216 passed at main and head | true |
| 8 shards whole, identical at main and head, no failure | true |
| Sidebar spec 107 rows in desktop and 107 in tablet; held by prototype-desktop-2 and prototype-tablet-2 | true (log rows 107/107 in exactly those two shards) |
| Wrap table | true (every cell reproduced, plus 820 px) |
| No strict-mode locator went red, none changed | true (no locator line in the diff; 0 failures at head) |
| lint, typecheck, build, audits rc 0 | true |
| infra hidden-character test passes; added lines clean | true |
| Name scan clean | true |

## Wrap measurement (re-measured by me: Chromium, production build, mock API, getBoundingClientRect; link /assessments)
Link height / row-below top, main -> head, px (full output: wrap-table.txt in this folder):

| Role | Cell | Column | Link h main/head | Wrapped (lines) | Row below top main/head | Delta |
|---|---|---|---|---|---|---|
| Partner | 1280x800 | 228 | 44/56 | main 1, head 2 | 219/231 | +12 |
| Partner | 1024x768 | 228 | 44/56 | 1 -> 2 | 260/272 | +12 |
| Partner | 820x1180 drawer | 245 | 44/56 | 1 -> 2 | 249/261 | +12 |
| Partner | 390x844 drawer | 245 | 44/56 | 1 -> 2 | 249/261 | +12 |
| Partner | 1280x800 collapsed | 64 | 44/44 | no / no | 207/207 | 0 |
| Admin | 1280x800 | 228 | 44/56 | 1 -> 2 | 219/231 | +12 |
| Admin | 1024x768 | 228 | 44/56 | 1 -> 2 | 260/272 | +12 |
| Admin | 820x1180 drawer | 245 | 44/56 | 1 -> 2 | 249/261 | +12 |
| Admin | 390x844 drawer | 245 | 44/56 | 1 -> 2 | 249/261 | +12 |
| Admin | 1280x800 collapsed | 64 | 44/44 | no / no | 207/207 | 0 |

The row below is "Training & playbooks". Every row beneath the link moves by the same 12 px (all tops are in wrap-table.txt source JSON; Admin tops at head 1280x800: Home 153, link 201/56, Training 261, ..., Admin 801).

## Checks (main vs head, by program)
| Check | Main | Head |
|---|---|---|
| lint (eslint --max-warnings=0) | rc 0 | rc 0 |
| typecheck | rc 0 | rc 0 |
| build (production) | rc 0 | rc 0 |
| `e2e.mjs --check-shards` | OK | OK |
| npm audit prod / audit-dev | not run (no package change) | rc 0 / rc 0 |
| vitest whole | 289 files, 4216 passed, 0 failed, 0 skipped | same |
| vitest rows | 4 rows renamed only: 1 in AssessmentsHub.myreadiness.test.tsx, 3 in GlobalNav.test.ts (4 only-at-main, 4 only-at-head, all 4216 passed) | |
| e2e journey-and-prototype | 2+182+14 passed | same |
| e2e prototype-desktop-2 (holds shell-sidebar.spec.ts, 107 rows) | 177 passed, 4 skipped | same |
| e2e prototype-tablet-1 | 181 passed, 1 skipped | same |
| e2e prototype-tablet-2 (holds shell-sidebar.spec.ts, 107 rows) | 177 passed, 4 skipped | same |
| e2e playbook-desktop-1 | 64 passed, 4 skipped | same |
| e2e playbook-desktop-2 | 54 passed, 13 skipped | same |
| e2e playbook-mobile-1 | 63 passed, 5 skipped | same |
| e2e playbook-mobile-2 | 52 passed, 15 skipped | same |
| infra/tests/test_hidden_characters.py | OK, 14 tests, 1515 tracked | OK; planted U+200B in a tracked file: FAILED rc 1 (fires); removed: OK |

All 8 shards were run whole (every spec that renders the shell), main and head in parallel on this machine; no red appeared, so no serial re-run was needed. Located the sidebar spec by the per-test rows in the shard logs.

## Red without the fix (copies in the scratchpad)
- Unit: head tests with main's GlobalNav.tsx: 13 failed / 61 passed of 74 (3 files). Every changed row is among the red ones (GlobalNav.test.ts lines 11, 14, 20, 23, 39, 44, 57, 88, 141, 160; AppShell.sidebar.test.tsx lines 63, 81; AssessmentsHub.myreadiness.test.tsx (d)).
- E2E: head's shell-sidebar.spec.ts against main's production build, desktop project: 21 failed / 86 passed. Every changed row is red: spec lines 183, 199, 309, 488, 558, 642, 727, 735, 813, 835, 843, 861.

## Closed lines re-verified at main
- steps.ts already labels the same route "Playbook Partner Readiness" (positive control: the string is in 32 files under web/ at head; a never-string reads 0). Census of "My readiness" under web/: 14 files at main; at head the remaining hits are only the hub eyebrow/header comments, the breadcrumb, the runner link, `content.test.ts:22` and their tests (the classes the kit named OTHER). No case-insensitive variant pins the sidebar link; the `my-readiness` id is untouched.

## Scans
- New-words: exactly one new product string. Added literals/JSX text: 44 string tokens new, 0 without the string.
- className/style/href/style changed lines: 0.
- Name scan, underscore-aware `(?<![A-Za-z])<name>(?![a-z])`, for Kam, Kamil, Kreiser, Steve, Peter, Paul, Blanchard, Inch, Waite over 53 added lines and the commit message: 0 each; planted `_by_<name>_` control fires for all nine.
- Secrets, GUIDs, hosts, key/token words: 0 (controls fire). Cf/Cc/non-ASCII over added lines: 0 (U+200B control fires). The only long-token matches are two test paths containing ASM-1.
- CodeQL pre-scan over added lines, tests included: `new RegExp(` 0; hand-escape `.replace(/[...]/g, "\\$&")` 0; innerHTML / dangerouslySetInnerHTML 0; child_process or exec with a template 0 (all four controls fire).

## NOT RUN
- api jobs (dotnet, SQL Server): no api/** or infra path changed; hosted CI is the proof.
- Hosted CodeQL, the required-check set and the hosted web job: the landing path.
- The tablet project's sidebar spec as a red-without-fix run (desktop shown; 107 rows each, same code).
- npm audit at main (no package change).
- Live-API e2e (needs the api).
- Re-derivation of the sweep-height boundary coverage after the 12 px move (finding 1).
