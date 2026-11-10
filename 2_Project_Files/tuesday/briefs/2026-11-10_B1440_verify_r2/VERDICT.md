GATE B1440-2: GO WITH FINDINGS @ fc90f07 on main 6b0c5f2

Round 2 of 2. Branch b1440/hpsmpoc-web-ui-rulings, READY fc90f0729aa491b568800ef703e2b81643309f66 (git ls-remote equal), 7 commits on
main 6b0c5f2caefedf47c940c9c5287dd9e358ae7cbb (re-read 12:3x and 13:06 AEDT: unchanged; merge-base = main). This round adds db1dbf2 (the logo
link) and fc90f07 (the mock) on top of round-1 head 1cbd4cd. Tier 1 (HPSMPOC-410 privacy surface re-crawled). The gate clone is in the
session scratchpad, with the push URL set to INVALID_NO_PUSH. It was never pushed. Ports used: 9920-9924 only. lsof showed 0 listeners in
9920-9929 before every run and after the last.

The round-1 Blocker is fixed and nothing regressed. All eight web e2e shards are green at head, with counts equal to main. Three findings
remain, none blocking: a landing-order note and two pre-existing or pointer items.

## Round-1 findings, re-verified at fc90f07

| R1 | Sev | Status at fc90f07 | Instrument and control |
|---|---|---|---|
| F1 T07 red (417) | Blocker | FIXED | journey-and-prototype rc 0 (2 + 182 + 14 passed) and prototype-tablet-1 rc 0 (181 passed, 1 skipped) at head. Both are equal to main. T07's own selector `header button.min-h-11, header a.min-h-11` at 768 px: main 4 matches, head 4 matches, all weight 600. The logo link is no longer matched (`measure417_*.tsv`, T07 rows; at round 1 head had a 5th match with weight 700). Control: in the red copy `mut2` (head tests plus 1cbd4cd's AppShell.tsx), the 3 `AppShell.logoLink` rows fail. |
| F2 hosted-entra flake | Minor | NOT RECURRED | The hosted project ran inside journey-and-prototype at main and at head, with 14 passed each. The diff touches no auth or cookie file. |
| F3 Home pipeline table shows name to Demo | Finding (out of scope) | UNCHANGED, as the addendum rules | The crawl shows the same counts at main and head. It is listed in the builder's STATUS, `## FOR THE RECORDS SEAT`. |
| F4 other Demo name surfaces | Finding (out of scope) | UNCHANGED, as the addendum rules | `cmp410_Demo.txt` has every row except the two 410 surfaces "same". Its body is byte-identical to round 1's after the header lines. The builder lists every file:line (pointers re-printed by this gate: true). |
| F5 mock 422 carries no "name is blank." | Minor | FIXED | `NAME_BLANK = { code: "customer.name-blank", field: "name", message: "name is blank." }` is used by create (`api.ts`) and rename (`customer-detail.ts`). The cross-check over the API lane's 39 rows (`cross324_head.tsv`) reads 39 SAME, and all 20 blank rows carry `name is blank.`. The API's words were re-read at the API branch 792c78f2, `CustomerEndpoints.cs:81` and `:202` (`"customer.name-blank", "name", "name is blank."`). Control: in `mut2` (1cbd4cd's mock), the 12 create and rename rows fail. |
| F6 39 Unicode-17 marks mock-blank / API-visible | Minor | FIXED | The gate's own full-scalar sweep: `VisibleText.cs` taken by `git show 792c78f2:...` into a scratch console project, on .NET 10.0.13, gives 5989 blank. It is byte-identical to round 1's .NET output. The head's `invisible-text.ts` was run over all 1,112,064 scalar values: **0 differ** on Node 24.21.0 (Unicode 17.0, CI's node) and on Node 26.13.0 (Unicode 18.0). Control: a planted flip of U+0041 reads **1** on both. Through `nameIsBlank` itself (round 1's vitest sweep at head): the output file is byte-equal to the .NET list. The two entry points (`isInvisibleCodePoint`, `hasNoVisibleCharacter`) agree on every scalar value. A lone surrogate is visible, the empty string is blank, and a visible letter between U+200B pairs is not blank (`sweep_mod.txt`). |

## Findings this round

| # | Sev | Item | Finding | Instrument and control |
|---|---|---|---|---|
| G1 | Finding | 324 order | **The API lane's hidden-character branch (B1441 @ 792c78f2) should land first.** The order does not break CI either way: no test reads across the two. But on main 6b0c5f2 the API's customer create and rename still refuse only `string.IsNullOrWhiteSpace` (`CustomerEndpoints.cs:79,198` at 6b0c5f2), so a name of U+200B alone is accepted by the API and refused by the mock. If this branch lands first, main holds a mock that is stricter than its API until B1441 lands. The mock's header also names `VisibleText.cs`, which main does not yet hold. If B1441 changes its rule in its own gate, the table here goes stale. The classifier body at main (`FeedbackEndpoints.IsInvisible`, lines 276-286) is the same as 792c78f2's `VisibleText.IsInvisible`, so the table itself is right for main's classifier either way. Only the customer-name wiring differs. | `git show` at both refs; `grep -n -i blank`. |
| G2 | Minor | 324 | The mock's 422 title "The name must not be blank" differs from the API's "The request breaks a domain rule" (`Problems.cs:38` at 792c78f2). This was already so at main and is not in the addendum's scope (it asked for the message field only). It is recorded for a ticket, not a fix. | Read at both sources. |
| G3 | Minor | 324 | The header comment of `invisible-text.ts` says "39 marks new in Unicode 17 differ". The test and the commit say 70. Both are true on their own runtime: Node 24 gives 39 and Node 26 gives 70, measured here with main's old regex against the .NET list (`sweep_oldregex.txt`). The STATUS line "UNMEASURED which Unicode version each ships" is now measured: Node 24.21.0 ships Unicode 17.0 and Node 26.13.0 ships Unicode 18.0. The code does not depend on either number. | `process.versions.unicode`; sweep. |

No secret, name, tenant/subscription id, host or Cf/Cc/Z character appears in the 367 added lines, the 7 commit messages or the new table
file. Ban-list scan: an underscore-aware regex, with a planted ban word between underscores and a planted U+200B. The scanner caught both, so it can fail. The one host-shaped hit,
`http://mock.test`, is a test fixture origin already used in 3+ test files at main. The commit messages carry no B-number or seat id, and
0 non-ASCII characters.

## Required checks

- **Refs and partition.** ls-remote of the branch equals READY. 13 of 13 changed paths (main..head) are inside OWNS (`web/src/components/**`,
  `web/src/server/mock/**`). `customer-name.test.ts`, `.github`, `web/e2e`, package, api, lib and non-mock server paths are untouched. Open PRs: 0
  (`pulls?state=open` length 0; control `state=closed` lists 303, 302, 301). Sibling branches: the API branch @792c78f2 has 8 paths, all `api/**`.
  The retention branch @5dfd22e has 14 paths, all `api/**` and `infra/sql/**`. Overlap 0.
- **Merge.** `git merge-tree --write-tree main head` rc 0, tree 5b33ecc3 = head's tree. Head descends from main, so merge = head.
- **Deploy.** ci.yml (only workflow; `security/` holds only gitleaks.ignore) runs on push to main. Its main-only steps upload and verify
  deploy-package artifacts. No job deploys, so the merge triggers no deploy.
- **HPSMPOC-417 width table** (Chromium, production build, mock API, Partner, /workspace and /home identical):

  | width | header main | header head | link main | link head | img h main/head | img w main/head |
  |---|---|---|---|---|---|---|
  | 360 | 128 | 128 | 28 | 44 | 28/28 | 120.36/120.36 |
  | 390 | 128 | 128 | 28 | 44 | 28/28 | 120.36/120.36 |
  | 640 | 128 | 128 | 40 | 44 | 40/40 | 171.94/171.94 |
  | 768 | 128 | 128 | 40 | 44 | 40/40 | 171.94/171.94 |
  | 1024 | 72 | 72 | 40 | 44 | 40/40 | 171.94/171.94 |
  | 1280 | 72 | 72 | 40 | 44 | 40/40 | 171.94/171.94 |
  | 1536 | 72 | 72 | 40 | 44 | 40/40 | 171.94/171.94 |

  The link is 44 at every width, the image is unchanged and the header did not grow. The built CSS gains exactly one rule
  (`.min-h-\[2\.75rem\]{min-height:2.75rem}`, +39 bytes). Selector collision: `min-h-[2.75rem]` appears only in AppShell.tsx:172 and its test. The only
  `.min-h-11` header selectors are `html-layout.spec.ts:157,164`. Other logo selectors go by href. The builder's 10 file:line pointers were re-printed: all true.
- **HPSMPOC-410 crawl** (round 1's instrument, 236 Demo and 234 Partner pages per tree, 0 errors). Demo, main to head: Upcoming activity 6 to 0,
  Customer details dd 8 to 0, every other surface the same. The body is byte-identical to round 1. Partner: 790 and 790 full-name hits. The only
  non-same rows are keyed by the probe customer's random id (14 and 14). After normalising the id, they are identical to round 1.
- **HPSMPOC-438 / 392 closed lines.** Old sentence over `web/`: main 2, head 0. Ruled sentence in components: main 0, head 2.
  "Revenue and proposals" 0/0. "Customer engagements" (exact case) 2/2 (`EngagementsList.tsx:35`, `steps.ts:209`, as recorded). Revenue control 1,
  package routes 0 (control: revenue routes 2).
- **New table file: bundle and characters.** `web/src/server/mock/invisible-text.ts` is 5472 bytes, with the RANGES literal 3463 bytes, plain
  ASCII, and 0 Cf/Cc/bidi characters. It is **not shipped to the client**: the table's last range `917504-921599` appears in 0 of 79 `.next/static`
  files. Control: "Upcoming activity" is found in 1 static file, so the search can hit. Static JS is 2,838,867 bytes at 1cbd4cd and 2,838,874 at head:
  +7 bytes, the class name only. Static JS at main is 2,835,464. The table is in server-side chunks only: 12 server files including source maps,
  one edge chunk and one SSR chunk. These are the same chunks that already carry the mock at main (`customer.name-blank` is in 12 server files at
  both). Server JS grows +24,187 bytes and edge JS +3,787 bytes.
- **Red without the fix** (copies). `mut` (head tests plus main's 6 product sources, new module removed): 5 files failed, 1 passed; 8 failed, 23 passed
  (the invisible file fails at import). `mut2` (head tests plus 1cbd4cd's AppShell.tsx, api.ts and customer-detail.ts, new module kept): 2 files
  failed; 16 failed, 35 passed. These are the 3 logo-link rows, 12 message rows and the 70-code-point row. The 3 module-only rows (table totals,
  range edges, lone surrogate) pass there by design, since they test the new module directly, and fail when it is absent (`mut`). Head: 6 files,
  51 passed.

## CI, by program (gate runs; main | head; merge = head)

| job / step | main | head |
|---|---|---|
| web-build npm audit --omit=dev | rc 0 | rc 0 |
| web-build audit-dev.mjs | rc 0 | rc 0 |
| web-build lint | rc 0 | rc 0 |
| web-build typecheck | rc 0 | rc 0 |
| web-build build | rc 0 | rc 0 |
| web-build e2e.mjs --check-shards | rc 0 | rc 0 |
| web-unit vitest | 285 files, 4187 passed, 0 failed | 289 files, 4216 passed, 0 failed (+29 by name vs main, 0 removed, 0 status changes; vs 1cbd4cd +7 -3 renamed rows) |
| web-e2e journey-and-prototype | rc 0: 2 + 182 + 14 passed | rc 0: 2 + 182 + 14 passed |
| web-e2e prototype-desktop-2 | rc 0: 177 passed, 4 skipped | rc 0: 177 passed, 4 skipped |
| web-e2e prototype-tablet-1 | rc 0: 181 passed, 1 skipped | rc 0: 181 passed, 1 skipped |
| web-e2e prototype-tablet-2 | rc 0: 177 passed, 4 skipped | rc 0: 177 passed, 4 skipped |
| web-e2e playbook-desktop-1 | rc 0: 64 passed, 4 skipped | rc 0: 64 passed, 4 skipped |
| web-e2e playbook-desktop-2 | rc 0: 54 passed, 13 skipped | rc 0: 54 passed, 13 skipped |
| web-e2e playbook-mobile-1 | rc 0: 63 passed, 5 skipped | rc 0: 63 passed, 5 skipped |
| web-e2e playbook-mobile-2 | rc 0: 52 passed, 15 skipped | rc 0: 52 passed, 15 skipped |
| infra hidden-character scan (test_hidden_characters.py) | 14 OK | 14 OK |
| infra/tests whole | 181 ran: 4 errors + 1 failure | the same 5 (identical set, and identical to round 1; no bicep binary locally) |

## Builder STATUS claims (## ADDENDUM-1)

- True: ls-remote = fc90f07; AppShell.tsx:172 text; `min-h-11` gone from the logo; image classes untouched; the width table (every figure
  re-measured equal); both shards whole rc 0 with equal counts at main and head; the selector-collision pointers; NAME_BLANK and its two
  uses; the mock problem shape carries `message`; table 378 ranges / 5989 code points; sweep 0 differ, planted 1; old regex vs table 70 on Node 26;
  the gate's 39 are a subset; lint/typecheck/build rc 0; vitest 289/4216, +4 new.
- Now measured (was UNMEASURED): Node 24.21.0 = Unicode 17.0, Node 26.13.0 = Unicode 18.0 (G3).
- True by this gate's whole-shard runs: "98 passed" for the five specs plus html-layout. They ran inside the shards, all green. Not re-run separately.
- Not shown: the builder's own port use and the red runs (the gate's own red copies agree).

## NOT RUN

- api, api on SQL Server, the Bicep part of infra validate, secrets (gitleaks), dependency review, CodeQL: hosted CI is the proof. The diff
  touches no api, infra or package file.
- The Entra and UAT shells' logo link was not browser-measured. Only the mock sign-in shell was. The class-token test covers all three.
- The Demo crawl ran on the offline mock with no scored run, so the ORG-nnnnn alias path was not crawled. vitest covers it.
- Hover-only tooltips and unopened dialogs were not opened. Hidden DOM text was read.
- The API branch's own suites were not run here (gated separately). Its rule was used only as the sweep reference.
