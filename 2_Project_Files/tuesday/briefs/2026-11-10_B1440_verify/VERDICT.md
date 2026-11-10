GATE B1440: NO GO @ 1cbd4cd on main 6b0c5f2

Branch b1440/hpsmpoc-web-ui-rulings, READY 1cbd4cdea1007af0d063f29e4eb130d3edb5aee8 (git ls-remote equal), five commits on main
6b0c5f2caefedf47c940c9c5287dd9e358ae7cbb (merge-base = main). Tier 1 (HPSMPOC-410). Gate clone in the session scratchpad, push URL
invalid, never pushed. Ports used: 9920-9924 only, 0 listeners before every run and after (lsof).

One Blocker: the HPSMPOC-417 change turns an existing e2e test red. Everything else checks out. See F1 for the fix.

## Findings

| # | Sev | Item | Finding | Instrument and control |
|---|---|---|---|---|
| F1 | Blocker | 417 | `e2e/html-layout.spec.ts:149` "T07 the Admin header at 768 px ... a button in the header keeps weight 600" is RED at head and GREEN at main. It fails in two CI shards: journey-and-prototype (desktop 1/2) and prototype-tablet-1. The cause is in the diff: the logo link now has `min-h-11`, so T07's selector `header button.min-h-11, header a.min-h-11` (spec line 157) picks it up, and the link keeps `font-bold`, which gives weight 700. Measured at 768 px: main has 4 matches, all 600. Head has 5, the 5th being `a[href=/workspace] weight=700`. The spec belongs to another lane and is not to be edited. The fix belongs in `web/src/components/shell/AppShell.tsx:172`, for example by dropping the text classes from a link that holds only an image, or using `font-semibold`. The builder re-measures after the fix. The builder ran only the five named specs, not the whole shards. Their NOT RUN section says so, so this is not a false claim. | Shards run whole: main 8/8 rc 0; head journey-and-prototype rc 1 and prototype-tablet-1 rc 1. Single-test rerun (`-g "Admin header at 768"`): main 1 passed, head 1 failed, Expected "600" Received "700" (`evidence/t07_head_failure.txt`). The weight list comes from `evidence/measure417_*.tsv` (T07-selector rows). |
| F2 | Minor | (not the diff) | `e2e/hosted-entra.spec.ts:32` failed once at head on line 63 (a cookie value contains "eyJ"). On rerun it passed 3/3 at head and 3/3 at main. The diff touches no auth, cookie or hosted file. I read this as a flake in another lane's spec (the session cookie's random bytes happen to contain those three characters) and do not attribute it to this lane. | `--project=hosted` x3 per tree: 14 passed each (`evidence/pw1_summary.txt`). |
| F3 | Finding | 410 | CONFIRMED (the builder's observation): Home's "Customer assessment pipeline" table shows the stored name to a Demo viewer (`web/src/components/partner/PartnerDashboard.tsx:163`, `{r.name}` link text). It shows all 4 stored names at 1440 and 390, the same at main and head. 410 does not name this surface. | Demo crawl, see "410 probe" below. |
| F4 | Finding | 410 | Other surfaces 410 does not name, where a Demo viewer still sees the stored name (all identical at main and head, so none is new). Customer lists /workspace and /customers: link text plus sr-only "Actions for {name}" and ": {name}" spans (`CustomerManagement.tsx:112,118,297,333`). /engagements "Under way" table (`EngagementsList.tsx:67`). /customers/<id>/documents "Document preview" (`DocumentGeneration.tsx:172`). /customers/<id>/profile "Customer context", Customer row, for API customers (`ApiSteps.tsx:100`; not shown for the quollridge route). /customers/<id>/tasks/firmware-risk "Related engagement" (`FirmwareTask.tsx:122`) and its customer picker options (`FirmwareTask.tsx:49`). /playbook/snapshot-assessment picker options and lines (`SnapshotLauncher.tsx:127-128`), and the lead line of /playbook/snapshot-assessment/assessments/<id>. Also, the slug "quollridge" appears in hrefs, option values and the feedback dialog's page path. One judgement call for the records seat: the kit's words "the customer profile" could be read as the /profile page. That page shows the name for API customers, but not for the quollridge route the ticket names. | Same crawl. |
| F5 | Minor | 324 | The mock now refuses exactly what the API lane refuses (status and code) on all 39 of the API lane's own rows. But the API answers each blank refusal with the message "name is blank." and the mock's 422 carries no message, as at main. The kit asked for "same code ... same words". The builder disclosed this. | Cross-check test over the API test's 4 row sets (`evidence/cross324_head.tsv`: 39 SAME, 0 DIFFERENT, every blank row `message=(none)`). Control at main: 14 DIFFERENT (the NothingVisible rows accepted). |
| F6 | Minor | 324 | Outside the rows both lanes test: a sweep of every scalar value, alone, finds 39 code points that the mock calls blank and the API lane's classifier calls visible. The other direction has 0. They are all marks new in Unicode 17 (U+1ACF-1ADD, U+1AE0-1AEB, U+10EFA-10EFB, U+11B60, 11B62-64, 11B66, U+1E6E3, 1E6E6, 1E6EE, 1E6EF, 1E6F5). Node 24 reports Unicode 17.0, and .NET 10.0.13's tables do not yet classify these as Mn. The mock is stricter only on these 39. This is the builder's UNMEASURED limit (2), now measured. | Node: the mock's `nameIsBlank`, 6028 code points blank. .NET: VisibleText.cs copied verbatim from 792c78f2, 5989 blank (`evidence/sweep_diff.txt`). |

No secret, name, tenant/subscription id, host or Cf/Cc character in the 265 added lines or in the 5 commit messages. Ban-list scan:
underscore-aware regex, with a planted underscore control (a ban word between underscores) that hits. Commit messages carry no lane or seat id.

## Required checks (commission)

- **Refs and partition.** ls-remote of the branch equals READY. 12 of 12 changed paths are inside OWNS (web/src/components/**, web/src/server/mock/**). `customer-name.test.ts` is untouched. No .github, e2e, package, api, lib or server (non-mock) path. Open PRs: 0 (`pulls?state=open` length 0; the control `state=closed` lists #303, #302, #301). Sibling API branch @792c78f2: 8 paths, all api/**, 0 overlap. Sibling retention/ledger branch: absent on origin (ls-remote of `refs/heads/b144*` lists only this branch and the API branch). Overlap 0.
- **Merge.** `git merge-tree --write-tree main head` rc 0, tree 09fb7a8d = head's tree. Head descends from main, so merge = head and every head result is also the merge result.
- **HPSMPOC-438.** The text node at `RoadmapScreen.tsx:86` equals the ruled sentence byte for byte (112 bytes, ASCII, python byte compare). `git grep -n "Verified complete needs an evidence reference" -- web/`: head 0, main 2 (control). Whole repo: head 0, main 2.
- **HPSMPOC-417.** Chromium, production build, mock API, Partner, `getBoundingClientRect` on /workspace and /home (identical figures on both):

  | width | header main | header head | link main | link head | img h main/head | img w main/head |
  |---|---|---|---|---|---|---|
  | 360 | 128 | 128 | 28 | 44 | 28/28 | 120.36/120.36 |
  | 390 | 128 | 128 | 28 | 44 | 28/28 | 120.36/120.36 |
  | 640 | 128 | 128 | 40 | 44 | 40/40 | 171.94/171.94 |
  | 768 | 128 | 128 | 40 | 44 | 40/40 | 171.94/171.94 |
  | 1024 | 72 | 72 | 40 | 44 | 40/40 | 171.94/171.94 |
  | 1280 | 72 | 72 | 40 | 44 | 40/40 | 171.94/171.94 |
  | 1536 | 72 | 72 | 40 | 44 | 40/40 | 171.94/171.94 |

  The image size is unchanged and the header did not grow. The link reaches 44 at every width. F1 still blocks.
- **HPSMPOC-410 probe.** A Playwright crawl of every same-origin link reachable after sign-in (BFS, 1440 and 390 wide, 236 Demo pages and 234 Partner pages per tree, 0 errors), run on a fresh server per tree and role. Each run plants one probe customer with a distinctive name (create 201) so lists carry a name no sample content holds. On each page it matches the full name and first word of every stored name against visible text, hidden DOM text, every attribute (aria-*, title, alt, placeholder, value, href, data-*), input values and document.title. Demo, main to head: "Upcoming activity" spans 6 to 0, and "Customer details" `dd` on /customers/<id> 8 to 0. Every other surface is unchanged (`evidence/cmp410_Demo.txt`). Both surfaces 410 names are clean at head, so no Blocker. No attribute, aria label, title, tooltip or document.title carries a full name at main or head. Partner without Demo: 790 full-name hits at main and 790 at head. The only differences are rows keyed by the probe customer's random id, which match one-for-one (`evidence/cmp410_Partner.txt`), so Partner is unchanged.
- **HPSMPOC-324.** See F5 and F6. The mock and the API lane agree on all 39 shared rows: 14 NothingVisible are 422 blank; 6 AsToday are 422 blank; 9 Visible are 201/200; 10 ShapeRefusesFirst are 400 `customer.name-invalid` with one code. The field is `name`.
- **New words.** A TypeScript-scanner extractor read every string literal, template part and JSX text in the 6 changed product files, at head against main. Literals added: 3. They are an import path, a class-token string, and one JSX text equal to the ruled 438 sentence. Product words added: the 438 sentence only. Confirmed. Existing words now also appear on Home Upcoming for Demo: "Alias not available yet (no scored run)" and the neutral "Customer".
- **Red without the fix.** In a copy with main's six sources and head's tests: 5 files failed, 1 passed; 20 tests failed, 27 passed. At head: 6 files and 47 tests passed. This matches STATUS exactly. The one file that passes without the fix is `PartnerDashboard.text.test.tsx`, which is a guard, as STATUS says.

## CI, by program (gate runs; main | head; merge = head)

| job / step | main | head |
|---|---|---|
| web-build npm audit --omit=dev | rc 0 | rc 0 (0 vulnerabilities) |
| web-build audit-dev.mjs | rc 0 | rc 0 (7 moderate, 0 high) |
| web-build lint | rc 0 | rc 0 |
| web-build typecheck | rc 0 | rc 0 |
| web-build build | rc 0 | rc 0 |
| web-build e2e.mjs --check-shards | rc 0 | rc 0 |
| web-unit vitest | 285 files, 4187 passed, 0 failed | 289 files, 4212 passed, 0 failed (+25 new by name, 0 removed, 0 status changes) |
| web-e2e journey-and-prototype | 2 + 182 + 14 passed | 2 passed; desktop 1/2 1 FAILED (T07, F1) 181 passed; hosted 1 failed (F2, flake) 4 passed 9 did not run |
| web-e2e prototype-desktop-2 | 177 passed, 4 skipped | 177 passed, 4 skipped |
| web-e2e prototype-tablet-1 | 181 passed, 1 skipped | 1 FAILED (T07, F1), 180 passed, 1 skipped |
| web-e2e prototype-tablet-2 | 177 passed, 4 skipped | 177 passed, 4 skipped |
| web-e2e playbook-desktop-1 / -2 | 64 / 54 passed | 64 / 54 passed |
| web-e2e playbook-mobile-1 / -2 | 63 / 52 passed | 63 / 52 passed |
| infra hidden-character scan (test_hidden_characters.py) | 14 OK | 14 OK |
| infra/tests whole (python unittest) | 181 ran: 4 errors + 1 failure | 181 ran: the same 4 errors + 1 failure (identical set; no bicep binary locally) |

The five named specs (a11y, customer-frame-alias, customer-headings-alias, logon-logo-link, responsive) run inside these shards and
have no failure at head. Only html-layout T07 and hosted-entra failed.

## Builder STATUS claims

- True: vitest 285/4187 to 289/4212; red 20 failed / 27 passed and green 47; the 417 table (every figure re-measured equal); 438 grep 0 at head, 2 at main; the 324 rows red at main, green at head; the mock carries no "name is blank." message; 0 open PRs; 12 files +265 -11; no package/workflow/e2e/api file; the 392 hits (`EngagementsList.tsx:35`, `steps.ts:209`; Revenue control 1; package routes 0); the 410 observation `PartnerDashboard.tsx:163`.
- True but not enough: "web-e2e (named specs) 58 passed". The whole shards hold a red (F1).
- Not shown: the builder's own port use (9940-9944), and lint/typecheck/build rc 0 at main as the builder ran it (I ran it: rc 0).

## NOT RUN

- api, api on SQL Server, the Bicep part of infra validate, secrets (gitleaks), dependency review, CodeQL: hosted CI is the proof. The diff touches no api/infra/package file.
- The Entra and UAT shells' logo link was not browser-measured. Only the mock sign-in shell was. The class-token test covers all three.
- The Demo crawl ran on the offline mock with no scored run, so Demo's label was the no-run words. The ORG-nnnnn alias path was not crawled; vitest covers it.
- Tooltips that render only on hover, and dialog contents not in the DOM until opened, were not opened. Hidden DOM text was read.

## For the fix round

Make the 417 logo link pass `e2e/html-layout.spec.ts` T07 (weight 600 for every `header a.min-h-11`) without touching the spec. Then re-run the shards journey-and-prototype and prototype-tablet-1 whole, and re-measure the table above.
