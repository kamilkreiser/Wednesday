GATE B1494: NO GO @ b225dbc on main 54ed762

Tier G1 (Opus), per S8 of the kit. Subject: branch b1494/mps-api-stores, READY sha b225dbcf99f2fe841399c2651d7351d0db11b02f, 4 commits (MPSCALC-122, -123, -99, -217). Gate run 2026-11-11 15:33-16:0x AEDT, own clone and worktrees under fleet/state/s267/gate1494/ (push URL INVALID-NO-PUSH; nothing pushed).

## Why NO GO (one line)
MPSCALC-123 moves the first disk write of an upload into the body read, outside the store's write-failure handling: when the store directory cannot be written, an upload with a file now gets an unhandled 500 (exception text and server path in the DevStub body) where main answers 503 FEEDBACK_STORE_UNAVAILABLE with its own words. Proved at base and at head by the same probe. 122, 99, 217 and the 98 run pass on their own; the 123 commit needs a small fix plus a row.

## Findings

| # | Sev | Ticket | Finding | Evidence |
|---|---|---|---|---|
| 1 | Major | MPSCALC-123 | **Failure path changed: a store write failure during the upload now answers an unhandled 500, not 503.** At head `UploadSpool.Create` (`src/MpsCalc.Api/Feedback/FeedbackAttachments.cs:37`, called at `:344`) and `file.WriteAsync` (`:350`) run inside `ReadMultipart` (`FeedbackEndpoints.cs:152`), before `SubmitWith`'s `catch (IOException or UnauthorizedAccessException) -> WriteFailed` (`FeedbackStore.cs:638`). Nothing catches them there, so a store directory with no write permission, a full disk, or a removed directory gives a raw 500. Probe `GateProbe123_a_store_directory_that_cannot_be_written_answers_503_store_unavailable` (store opened, then root set to 0500, one 4 KiB PNG sent), same file at both trees: **main: 503 FEEDBACK_STORE_UNAVAILABLE (pass); head: `500 (not json); System.UnauthorizedAccessException: Access to the path '<store>/.upload-<id>.tmp' is denied`**. That also skips the `FEEDBACK_STORE_UNAVAILABLE ... the write failed` log line. It goes against the kit ("Keep: ... every refusal's status, code and words") and against STATUS ("every path out ... a failed write (503)"). Fix shape (builder's call): map an IOException or UnauthorizedAccessException from the spool, meaning create, write or flush on the store's volume, to the existing WriteFailed answer (503 FEEDBACK_STORE_UNAVAILABLE, existing words). Keep a client abort (`RequestAborted`, or a read on the request body) out of that mapping. Add a red-first row like the probe. | `logs/probes-head.log`, `logs/probes-base.log` |
| 2 | Minor | MPSCALC-217 | Deploy note, not a code defect: a reference store that an Administrator staged and activated through the admin route before this change and that holds a repeated (sheet, SKU) pair would answer 503 SOURCES_UNAVAILABLE at first need after the deploy. Main validated such a document; the existing decoy row validated one until its data edit. The importer never writes one (P217 re-proved below). The hosted store was not read (fence). Worth one look at the active stored version before the deploy card. | P217 below; `logs/plants217.txt` |
| 3 | Minor | MPSCALC-123 | STATUS claims "every refusal ... status, code and words unchanged". That holds for every refusal probed (14 edge arms identical at main and head), but not for the failure path in row 1. Graded false for that one clause. | below |
| 4 | Info | MPSCALC-123 | My client-abort probe (head only) passed: the temp file existed mid-part, was gone afterwards, no item was stored. But it took 3 m 20 s in TestServer before the aborted request finished. That is harness behaviour; the Kestrel suite is the real-socket proof. Not a product finding. | `logs/probes-head.log` |

No Blocker: every path is inside the lane (with ANSWER-1's one file), no secret, no name, no red at head or merge that is green at main, no hosted touch, nothing deployed.

## Press-hardest: MPSCALC-217 (all MEASURED here)
**(a) The decoy builder edit.** The diff of `SourceLifecycleTests.GovernedNullClassEdges.cs` is +1/-0 (numstat). The one added line is at `:761`, `more[1]["supplySku"] = "1" + ...`. `Assert.` count in the file: 116 at main, 116 at head. No test name changed (name lists below). The group key (`ReferenceDocumentValidator.SupplyGroups`) is built from the `rows` cells, not the SKU, so the edit leaves the decoy's key, size and price untouched. In-builder asserts (sizes fewer < real < more, each decoy collides with the real key) are unchanged and still run.
The edited test still catches its own property. Plants in the throw-away mut-tree (product at head), one at a time, then reverted (`git diff --quiet` after each):
| Plant in `SupplyGroups` | Decoy test |
|---|---|
| none | GREEN |
| last group wins (`groups[key] = rows`, the builder's plant) | RED (`Expected "Validating" / Actual "Failed Validation"`) |
| **larger group wins** (exercises the edited "more" decoy) | **RED** |
| smaller group wins ("fewer" decoy) | RED |
| first-SKU-sorts-first wins ("same" decoy) | RED |
| max-SKU wins (no decoy is built for this) | GREEN (not a weakening: no decoy carries a higher max SKU, at main or head) |
| data edit removed, product at head | RED (`Failed Validation`: the repeat is now refused at validate, so the edit is needed) |
| whole 217 product change reverted to main, edit kept | GREEN (the edit does not depend on the fix) |
**(b) Removed or weakened tests.** Removed lines under `tests/` over main..head: 14 (`git diff --numstat` summed). Control: one assertion line planted out of a test file in mut-tree made it 15, then was restored. All 14 lines are the one allowed method `StoreLoadRowsTests.Control_a_repeated_supply_row_is_still_served_as_before` (`Assert.` 13 -> 11 in that file = its two asserts; `[Fact|Theory]` 6 -> 5). Every other test file has 0 removed lines. Name lists (`dotnet test --list-tests`, sorted): main 4405, head 4411. `comm -23` = exactly that one name; `comm -13` = exactly the 7 rows the builder lists. No Skip, no pragma, no Thread.Sleep added. The two `Task.Delay` added are the 20 ms poll and the slow-body pacing, both allowed.
**(c) The refusal, at the edges** (probe theory over the store-load routes catalogue / inventory / calculate; same file at main and head):
| Shape | main | head |
|---|---|---|
| exact repeat adjacent / first-and-last / last row / triple | 200,200,200 (served, collapsed) | 503 SOURCES_UNAVAILABLE x3 |
| repeat with a different price | 200 x3 (first price served silently) | 503 x3 |
| same SKU, other sheet / same sheet, other SKU | 200 | 200 |
| case-variant SKU / trailing-space SKU | 200 | 200 (ordinal, the same key rule as the importer's `Duplicates`) |
| null sheet vs "" sheet, same SKU | 503 | 503 (refused downstream of `From`, by an existing guard) |
The fault is reported, not served. The validate path refuses a staged document holding a repeat (the decoy row without its edit, above).
P217 re-proved in my clone at main: (i) `PriceBookImporter.cs:195` `Duplicates(map.Supplies, ...)` -> `:61` `Block` -> Blocking -> `:16` `Succeeded` false; (ii) `log -S` and `--diff-filter=A` both print `774b82d` (control: a nonexistent string prints 0); (iii) one writer, `PriceBookImporter.cs:165` (control `DeviceRows =` hits `:163`). Callers of `ActiveSourceSet.From`: `SourceDocumentChecks.cs:325` plus two test fixtures.

## Other tickets
- **122** (tests only): plant, hosted pipeline only, that strips the three headers on the act-as 400, the 503 and the 500 answers: the 3 new hosted rows RED; DevStub 7 rows and old hosted 401/403/404/200 GREEN. Reverted. The new rows bite exactly the gap the ticket names.
- **123**: red-first with main product and head tests: both LaneL2_123 rows RED (`largest file 0 bytes`; `allocated 61.02 MiB`). Cleanup plant (spool `File.Delete` removed): 13 of the existing `Each_refusal_answers_its_code_and_stores_nothing` rows go RED, so cleanup is guarded by existing rows. Edge probes, identical at main and head: exactly 5 MiB 201; 3 x 5 MiB 201; 5 MiB+1 chunked 413; JPEG 3-byte magic only 201; PNG magic minus 1 byte 415; exactly 8-byte PNG magic 201; PDF 201; second file over 413; second file bad type 415; unclosed after a 4 MiB file 400; truncated inside the file 400; garbage body 400; replay 200 + key reuse 422 with one attachment folder and 0 temp files; 3 files stored byte-equal with the recorded sha256. Head only: a body trickled 1 byte per read is stored whole; a leftover `.upload-<id>.tmp` is named at start by the existing rule and left in place. The whole-request 16 MiB bound cannot be reached with valid parts (3 x 5 MiB + 16 KB + 8 KB preamble < 16 MiB): not probed further.
- **99**: red-first: Busy after 2684 ms at main code (body 1500 ms, bound 1000 ms). Edge probes at head, all pass: slow body (1500 ms > bound) with the store FREE -> 201, not Busy; store held, 600 ms body, 2000 ms bound -> Busy between 1.9 and 2.45 s, so counted from arrival; held then released at 1200 ms, inside the bound -> 201; released at 1500 ms, after a 1000 ms bound -> Busy before 1.45 s. Validate, activate and rollback keep their own clock (`SourceLifecycle.cs:624-626`, `arrival` defaults null).
- **98** (closed-with-evidence, no commit): c1 re-planted at main (`CatalogueOverlayStore.cs:607`), 3 runs per condition: clean 4/4 green x3; c1 4/4 red x3. Undone, `git diff --quiet`. The builder's evidence file sha256 `77eca997...` matches STATUS.

## Steps
1. Refs: `ls-remote` branch = b225dbcf99f2fe841399c2651d7351d0db11b02f; main = 54ed76273cf5e7eb804315635c413034f28b3372 at the start (15:33) and the end (15:56): unmoved. Ahead 4, behind 0. 12 changed paths: 11 of 12 in the kit's OWNS; the 12th, `tests/MpsCalc.Api.Tests/SourceLifecycleTests.GovernedNullClassEdges.cs`, was added by ANSWER-1 for one edit, giving 12 of 12 (control: a planted `web/x.ts` printed 1). None under Inventory, Quotes, Contracts, Import, .github, docs, web, scripts, infra or csproj. Open-PR overlap: NOT RUN (needs the GitHub API, which the fence bars).
2. Merge: `git merge-tree --write-tree main head` rc 0, clean; tree `92b8c746...` = head tree (main is an ancestor), diff 0 lines.
3. CI: job dotnet: build `0 Warning(s)` `0 Error(s)` at main and head; tests from trx: main 743+196+3466 = 4405 passed, 0 failed; head 743+196+3472 = 4411 passed, 0 failed; both rc 0. Merge = head tree, so the head run is the merge run. Job package at head, Node v24.22.2, npm offline from the machine cache: `package rc=0`, `markers found 0/57`, B2 scan 0 hits. Job python: no python test reads a changed path (grep of each changed file name: 0 hits; control CatalogueOverlayStore: 1). The whole loop was still run at both trees (`python3 -I`, BICEP unset): 10 files, rc 0 each, identical per file at main and head (`out/py-main-tree.txt`, `out/py-head-tree.txt`). `test_infra.py` printed "no Bicep compiler" in its log at both trees (see NOT RUN). Job web: no web path changed; not run.
4. Red without the fix: every new or changed row is red with the fix removed (above). 122 is tests-only and red under the planted fault.
5. Closed lines: 98 above. No ALREADY-ON-MAIN lines in STATUS.
6. Probes: above.
7. Scans over 524 added lines and 4 commit messages: ban-list names (Kam, Kamil, Kreiser, Steve, Peter, Paul, Blanchard, Inch, Waite, plus the seat names), underscore-aware, 0 hits (control `x_by_kam_y` fired). B-numbers, seat ids, finding ids, decision cards: 0 (control fired). Non-ASCII 0 (control U+200B fired). Cf characters 0. GUIDs, tenants, hosts 0. Emails: only `*@example.test` and the attribution address. gitleaks 8.30.1: canary rc 1, then range rc 0. CodeQL pre-scan: new RegExp / Regex, hand-escape, innerHTML, child_process: 0 (control fired). Commit author/committer metadata is the repo's own configured identity (not scanned as content).
8. Claims (STATUS): base 4405/0 TRUE; head 4411 passed 0 failed TRUE; build 0 warnings TRUE; names lost 1 / gained 7 TRUE; removed test lines 14 TRUE; 12 files, ahead 4 / behind 0 TRUE; main unmoved TRUE; 98 red 10/10 under c1 TRUE as far as re-run (3/3), evidence sha256 TRUE; 217 decoy proof (red under displacement, green restored) TRUE; P217 (i)-(iii) TRUE; 122 planted faults turn the new rows red TRUE; 123 rows red at base TRUE (61.02 vs the claimed 61.07 MiB, within noise); 99 red at base TRUE (2684 vs 2555 ms); package rc 0 TRUE; gitleaks TRUE; "every refusal's status/code/words unchanged" TRUE for refusals, **FALSE for the store-write-failure path (finding 1)**; "a failed write (503)" on every path out **FALSE** (finding 1); RSS figures NOT SHOWN (not re-measured here).
9. Tier: G1, this gate. No security-shaped issue beyond finding 1 (an error-path status, plus an exception message with a server path in the Development-mode body; hosted runs Production, where ASP.NET sends an empty 500).

## NOT RUN
- Hosted CI and CodeQL: the proof for landing, after the fix.
- Open-PR overlap and sibling-lane branches: needs the GitHub API (fence).
- The infra half of the python job, which needs `az bicep` (fence): the loop was run without BICEP at both trees and compared per file.
- The web and e2e jobs: no web path changed.
- RSS re-measurement for 123.
- The MPS heavy-lock directories were not taken: they live inside the MPS project folder, which this gate may not write. Heavy jobs ran with load printed (4.4-17.6).
- Anything needing docker or a database: none needed.

## Trees (gitignored, under fleet/state/s267/gate1494/)
`clone` (push URL INVALID-NO-PUSH, deploy key as repo-local core.sshCommand), `main-tree` (main, tracked diff 0; untracked probe copies), `head-tree` (head, porcelain 0), `mut-tree` (head, tracked diff 0 after every plant; untracked probe files), `pkg-tree`, `pkgout`, `logs/`, `out/`, `scripts/`.

## Landing files
Not written. The standard asks for them only on GO or GO WITH FINDINGS. After the 123 fix lands on the branch, re-gate the new head (head-pinned squash; `--match-head-commit` on the new sha, not b225dbc).
