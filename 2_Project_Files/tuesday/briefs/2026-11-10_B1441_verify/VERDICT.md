GATE B1441: GO WITH FINDINGS @ 792c78f on main 6b0c5f2

Branch b1441/hpsmpoc-api-hidden-characters, READY 792c78f292bdd6f1feba07575830cb9032973d98. `git ls-remote` gave the same sha at
14:4x and again at 15:01 AEDT. The branch has two commits on main 6b0c5f2caefedf47c940c9c5287dd9e358ae7cbb, and main is an
ancestor of the head (rc 0). Tier 1. The gate worked in its own clone in the session scratchpad. Its push URL was set to
`invalid://no-push` and it never pushed. Ports: 9930 only (one SQL Server container at a time). 0 listeners in 9930-9939
before and after; both containers are stopped. The pr-title.txt and squash-subject.txt files that an earlier gate left here
were overwritten. Every file in this folder is this gate's own.

No Blocker. No Major. The findings are Minor or informational.

## Findings

| # | Sev | Item | Finding | Instrument and control |
|---|---|---|---|---|
| F1 | Minor | 257 | Only the unit rows pin the white-space half of `FoldWidthAndSpace`. No upload row does: `DeviceStems` already ends the folded stem with `TrimEnd()`, so a fold that drops `char.IsWhiteSpace` still passes all 21 `Hpsmpoc257FileNameTests` rows. The builder disclosed this (STATUS, FOR THE RECORDS SEAT). The unit rows and the all-scalar sweep do catch it, so the new tests are not vacuous. | Gate mutant in a copy (`IsWhiteSpace` branch removed; forwarder made to differ at U+2800): 7 failed. 5 fold rows, the scalar sweep and the shared-classifier sweep failed, and 0 `Hpsmpoc257FileNameTests` rows failed. |
| F2 | Minor (product) | 324 | A customer whose name was stored invisible-only before this ruling now gets 422 `customer.name-blank` on any profile save that sends the name back unchanged. The B482 `heldName` allowance in `Shape.Customer` (`Requests.cs:137-147`) covers the shape check only, not the blank rule (`CustomerEndpoints.cs:202`). The builder disclosed it (open item 1). DERIVED from source. Whether any such record exists on a hosted database is UNMEASURED; the gate touched no hosted host. It is for the records seat or product owner, not a defect against the ruled words. | Source read at 792c78f2 (`git show`, lines cited). |
| F3 | Minor | 257 | Two stale comments in a file no lane owns: `api/tests/HpsmPoc.Modules.Feedback.Tests/FeedbackAttachmentTests.cs:173-175` ("compared in its compatibility form") and `:183` ("White space that NFKC keeps"). The comments still describe the NFKC fold. The rows under them pass. The builder disclosed this. | `git show 792c78f2:<file>` lines 172-186. |
| F4 | Info | #304 | The web mock in PR #304 (`web/src/server/mock/invisible-text.ts`) cites this branch's `VisibleText.cs @ 792c78f2` as its source. The B1440 gate's F6 found the mock stricter than this classifier on 39 code points (marks new in Unicode 17, which .NET 10.0.13 does not classify as Mn) and lenient on 0. This is RELAYED, not re-measured here. This branch is unaffected. | `git show pr304:web/src/server/mock/invisible-text.ts` (header cites 792c78f2); B1440_verify/VERDICT.md F6. |
| F5 | Info | env | `infra/tests/test_resource_hygiene.py`: 1 of 18 fails locally, the same at main and at head. It expects a unittest report format that this Mac's python3 does not print (`test_keeps (test_own.Own.test_keeps)`). The cause is the environment, not this diff. Hosted `infra` is the proof. | Run at main and at head: `FAILED (failures=1)` at both, same test. |

Scans: name, secret, tenant or subscription id, host, Cf/Cc, non-ASCII and seat-id scans each found 0. They ran over the 569
added lines and the 46 commit-message lines. The CodeQL pre-scan also found 0 (`new RegExp(` from a variable, a `.replace(/[...]/g,
"\\$&")` hand-escape, `innerHTML`/`dangerouslySetInnerHTML`, `child_process`). Positive control: a planted scratch commit (never
pushed) made every scanner fire: name 1 (the planted `_by_<name>_` form), secret 1, guid 1, host 1, Cf 2, non-ASCII 1, seat 1,
CodeQL 3 of 3. The diff adds no web or JS file, so hosted CodeQL `js/*` has nothing new to read here.

## Required checks

- **Refs and partition.** Branch at origin = READY (2 reads). 8 of 8 changed paths are inside OWNS or the authorised
  NEEDS-SHARED file: `CustomerEndpoints.cs`, `FeedbackFiles.cs`, `FeedbackEndpoints.cs` (the classifier is shared, as the kit allows), the new
  `api/src/HpsmPoc.Modules.Assessment/Endpoints/VisibleText.cs` (NEEDS-SHARED, authorised by Tuesday), and 4 new files under
  `api/tests/**`. `Hpsmpoc178CustomerNameTests.cs` is untouched. Open PRs: 1 (#304 @ d49be881, base main). Overlap with #304's 13
  paths (all `web/**`) is 0. Overlap with sibling branch b1442 @ c16f422e (17 paths) is 0. Pairwise `merge-tree` of this head with
  #304 and with b1442: rc 0 both.
- **Merge against current main.** `git merge-tree --write-tree main head` rc 0, tree d52786aa = the head's tree. Head descends
  from main 6b0c5f2c (main has not moved since the branch point), so the merge equals main plus the 8 head blobs. **This branch
  merges clean against current main.**
- **#304.** It touches no path of this branch, and merging it with this head is clean (rc 0). Its dependency is in meaning only:
  its mock mirrors this classifier's refusal set (F4). Hold #304 until this branch lands, as planned.
- **CI, `api` job (SQLite, as the test step runs; Release, TreatWarningsAsErrors).** Restore rc 0 and build rc 0 with 0 warnings
  at main and at head. Test rc 0 at both.

  | Program | main 6b0c5f2c passed / failed / not run | head 792c78f2 (= merge) |
  |---|---|---|
  | HpsmPoc.Api.Tests | 2195 / 0 / 13 | 2273 / 0 / 13 (+78) |
  | HpsmPoc.Modules.Assessment.Tests | 291 / 0 / 9 | 291 / 0 / 9 |
  | HpsmPoc.Modules.Feedback.Tests | 414 / 0 / 0 | 477 / 0 / 0 (+63) |
  | HpsmPoc.Modules.Reporting.Tests | 850 / 0 / 0 | 850 / 0 / 0 |
  | HpsmPoc.Modules.Rules.Tests | 164 / 0 / 0 | 164 / 0 / 0 |
  | TOTAL | 3914 / 0 / 22 | 4055 / 0 / 22 |
- **CI, `api on SQL Server` (subset).** Image `mcr.microsoft.com/mssql/server:2025-CU9-ubuntu-24.04@sha256:2b5b5816...` (CI's
  pin), `--platform linux/amd64`, `@@VERSION` 17.0.5005.3. A random sa password was passed to docker by name only; the logs hold 0
  copies of its prefix. Connection in CI's form on 127.0.0.1:9930. Filter: Hpsmpoc324, Hpsmpoc257, FeedbackAttachment,
  CustomerApiTests, Hpsmpoc178CustomerName, Hpsmpoc99, Hpsmpoc177, Hpsmpoc226, Hpsmpoc290. Api.Tests: main 156/0, head 234/0.
  Feedback.Tests: main 246/0, head 309/0. Test databases: 27 at main, 29 at head.
- **Repo-wide scans (DRAFTER_RULES rule 8).** `infra/tests/test_hidden_characters.py` ran 14 tests, OK at main and at head.
  Control: a staged scratch file holding U+202E fails it (`api/plant.txt:1:2 U+202E`). Also OK at main and at head:
  test_ci_workflow 36, test_deploy_package 44, test_env_value 7, test_deploy_hpsmpoc208 35, test_web_env_scan 11,
  test_outbound_address_spelling 4, test_hosted_demo_pin 10. test_resource_hygiene: see F5.
- **Red without the fix (in a copy).** Head with the two call sites reverted to `string.IsNullOrWhiteSpace` and the stem reverted
  to NFKC, keeping VisibleText and FoldWidthAndSpace so every test compiles. 35 failed of 141: Api.Tests 28 (exactly the 14
  NothingVisible rows, each run on create and on rename), Feedback.Tests 7 (the 6 Accepted upload rows, plus the DeviceStems unit
  row). Green at head: 141 of 141. The fold unit rows and the shared-classifier rows test new or moved code, so they cannot
  fail with the call sites reverted; the gate's own mutant shows they are live (F1).
- **Closed lines.** None. The STATUS closes nothing with evidence, and both tickets were STILL OPEN at main: at 6b0c5f2c,
  `CustomerEndpoints.cs:79,198` read `IsNullOrWhiteSpace` and `FeedbackFiles.cs:139` reads `FormKC` (`git show`).
- **Probes (the gate's own rows in a copy, at main and at head).** Customer create. These 5 rows give 201 at main and 422
  `customer.name-blank` at head: U+034F alone, U+FE0F alone, U+E0100 alone, 120 x U+3164, and U+3000 U+200B. These 4 rows give
  exactly one code each and never 500: U+180E, U+1D173, NEL U+0085, a lone surrogate. 121 x U+200B gives 400
  `customer.name-length` alone, and W + U+0301 gives 201. Head 11 of 11.
  File names. Two rows are refused at main and accepted at head: CON + U+FE52 + `txt.txt`, and fullwidth LPT + U+2074 `.txt`.
  These stay refused at head: fullwidth COM + U+00B9, NUL + U+2000, fullwidth CONIN + U+FF04, lower `con` + U+FF0E + `txt`, and
  AUX + U+202F. PRN + U+FF5F (just outside the fullwidth range) is accepted at main and at head. Head 9 of 9.
  The gate's first CON + U+FE52 row (`CON` + U+FE52 + `txt`, no extension) gave 422 `feedback.attachment-type`. That was a
  fault in the probe, not the code: the name has no allowed extension. The probe was corrected and re-run.
- **Tier 1.** This is API input validation. No security-shaped issue was found beyond F2, a product question disclosed by the
  builder.

## Builder STATUS claims

| Claim | Grade |
|---|---|
| Branch head 792c78f2 = ls-remote; 2 commits on 6b0c5f2c; main unchanged | true |
| Commits since fa401da9 touch none of the 3 owned files | not shown here (not re-run; main = branch point, so it does not affect landing) |
| Assessment cannot reference Feedback (Feedback.csproj:18 references Assessment; Assessment refs Rules :14, Reporting :16); InternalsVisibleTo lists only Assessment.Tests and Api.Tests | true (csproj grep at 792c78f2) |
| The blank checks sit at CustomerEndpoints.cs:81 and :202, same code, field and words | true |
| SQLite counts by program, main 3914/0/22 and head 4055/0/22, 0 warnings | true (identical per program) |
| Red at main: Api.Tests 28 failed, Feedback.Tests 6 failed | true in substance: the gate's fix-removed copy gives 28 and 6 + 1 (the extra one is the DeviceStems unit row, which does not compile at main) |
| 12 of 12 mutants killed | not shown (2 gate mutants agree, F1) |
| SQL Server subset main 156/246, head 234/309; databases 27/29 | true (identical) |
| 0 non-ASCII and 0 hidden characters in added lines; commit messages ASCII without seat ids | true |
| CON + U+FF0E stays refused under the width fold | true (row green at head; the gate's lower-case probe agrees) |
| Open PRs 0 at each push | not shown (#304 is open now and opened after; 0 overlap) |
| Containers stopped, 0 listeners in 9950-9959 | not shown (outside the gate's port block; not read) |

## NOT RUN

- The two whole `api on SQL Server` shards, their named-test and database-floor checks, and the roll-up. Only the subset
  above ran. Hosted CI is the proof.
- The Azurite (Blob) step of the `api` job: 22 not-executed rows at both main and head. The vulnerable-package step, the deploy
  package step, gitleaks, dependency review, and CodeQL itself are hosted. The CodeQL pre-scan above ran locally.
- `infra` Bicep validation (`validate.sh`, `test_security_baseline.py` with Bicep), and the web jobs. No path of theirs changed.
  The repo-wide infra scans did run (above).
- No Jira read. No hosted host touched. No PR opened, nothing pushed.
