From Friday (laptop seat), Datasec / Security Composer.

# BRIEF B125 (SEAT A): Lane T1-API, the contract and `apps/api/src/routes`. Contract and API correctness: #146 (If-Match on withdrawException), #150 (refuse submit on critical issues), #303 (setPolicyTarget's ETag described), #179 (GenerateRecord wording), #177 (generator's user id to Datasec roles only), #294 (where the HPSM name is read back), #116 (an exception read for the approver summary, API half). Tier 1.
**From:** Friday (laptop seat), 16:51 AEDT 2026-10-11. Replies go to Friday. **Seat:** Datasec/Security-Composer-A. Datasec / Datasec Security Composer only (the product is "Policy Designer" on screen, C-62). Report `1_Project_Definition/Briefs/2026-10-11_B125_STATUS.md` (BLUF · FOUND · TESTED · HOW · **PRIOR WORK (required)** · **TEST EVIDENCE (required)** · NOT TESTED · **CONTRACT DIFF (required: 0.31.0 → 0.32.0, one bump)** · **NEW WORDS (required)** · QUESTIONS FOR FRIDAY · UNMEASURED). The last line is `READY FOR QA: <branch> @ <sha>` (branch pushed, head SHA read by `ls-remote` in the same action, `ci.sh` green, the READY items in §7 present) or `STOPPED: NEEDS FRIDAY` followed by one question.

**Launch (how Friday starts this seat, as B120/B121 were started):** `cockpit.sh launch Datasec/Security-Composer-A` (`FRIDAY/2_Project_Files/fleet/cockpit/launchers.conf:34` → the project's own `Launch_Claude.command`). That launcher reads the pane name, sets `YOUR SEAT: A`, and commissions **the newest brief whose file name contains `_SEAT-A_`** (`Launch_Claude.command:92-105`): this file. Two things in the launcher's FIRST ACTIONS do not fit this round, and this brief overrides them for this seat only:
- It says to read `./BACKLOG.md`. **The working copy is records `main` (`441fa893`, 293 lines), which does not hold #303** (or #298–#308): `grep -c` of those six row numbers there = 0, control #146/#150/#155 = 3. Read the rows from `git --no-optional-locks show records/b124:BACKLOG.md` (records/b124 = `ce70da67db8cee3785409960fae1852dc2b113b4`, 307 lines; `git merge-base --is-ancestor records/b124 main` = false). C-67 and C-68 are likewise only on `records/b124`.
- It says to record progress in "the Jira ticket(s) the brief names". **This brief names none** (the Composer has no Jira; `BACKLOG.md:4` @records/b124). Its scope rule 1 (this folder only) stands: the FRIDAY paths cited here are provenance, not reading.

**Authority (Kam, Friday's terminal, 2026-10-11 ~11:58, verbatim, recorded at `FRIDAY/0_Brain/daily_friday/2026-10-11.md:64`):** *"I have logged you in using a freash account. please continue on the work with HPSM poc, security composer and the MPS calculator"*. Friday's reading: keep building the Composer's agent-doable rows. The rows are commissioned from Friday's read-only sort of every open BACKLOG row (`FRIDAY/2_Project_Files/friday/briefs_drafts/2026-10-11_composer_open_backlog_sort.md` §6 "T1-API"). **Nothing here is a Kam decision.** Three rows (#177, #294, and the If-Match shape of #146) carry **Friday's reading, to be confirmed at the gate**, stated at each row. #150's refusal is new words a salesperson can see: NEW WORDS, and Kam sees them before any demo deploy (#251 precedent). This brief deploys nothing.

**Base.** Composer origin main = **`4e00d573cc4c1ae215e2aad70e92a08e3218281b`**: the build LIVE on the demo since B124 (C-68, `Briefs/2026-10-11_B124_STATUS.md`, records/b124 `ce70da67`). The drafter read it at 2026-10-11 16:37 AEDT two ways: `friday_as.sh datasec gh api repos/datasecau/Datasec-Security-Composer/commits/main --jq .sha` and `git ls-remote origin refs/heads/main`. Both gave `4e00d573…`. **The local clone does not hold that commit** (`git cat-file -t 4e00d573…` in `2_Project_Files` = "could not get object info"). Every code cite below is **(read at `4e00d573`)**, read with `git show 4e00d573:<path>` / `git grep … 4e00d573` in a `git clone --shared` of `2_Project_Files` after a fetch.
- **First action:** in your own worktree, `git fetch origin`, then `git -C 2_Project_Files ls-remote origin refs/heads/main`. **If it is not `4e00d573…`: STOP** (`STOPPED: NEEDS FRIDAY`, with the new SHA and the time read). Do not rebase onto a moved main on your own.

**Branch** `b125/api-contract-correctness` from `4e00d573`, own worktree **`/Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/_wt_b125`** (absolute, outside `2_Project_Files`). At drafting neither exists: `ls -d _wt_b12*` gives `_wt_b120`, `_wt_b121`, `_wt_b124rec` only; `git branch -a --list '*b125*' '*b126*'` is empty (0 lines); `ls-remote origin 'refs/heads/b12*'` lists only `b120/…` and `b121/…`.
**Tier 1:** contract (one bump, 0.31.0 → 0.32.0), API behaviour, and one authz row (#116's new read). No migration, no content, no dependency change; if one turns out to be needed, STOP.

**Running in parallel: SEAT B** (`Datasec/Security-Composer-B`, brief `Briefs/2026-10-11_B126_SEAT-B_details-screens-polish.md`, Lane T2-DETAILS, tier 2) may be LIVE at the same time. It owns **`apps/web/src/screens/**`** and **`apps/web/src/styles/**`**. **Those paths are NOT yours**, including `apps/web/src/screens/Approval.tsx` (withdrawException's caller) and `apps/web/src/screens/w3/approverSummary.tsx` (#116's web half). Its stacks are `pc-b126*` on 10.126.x.0/24 and ports **6760–6769**: never start, stop, reuse or remove them. Other Datasec seats may share the machine (Docker, CPU) but no files.

---

## 1. Why: the rows (quoted verbatim from `git show records/b124:BACKLOG.md`, records/b124 `ce70da67`; do not re-rule)
- **#146** (`BACKLOG.md:140` @records/b124): *"**B54-N4 (Low, design):** `withdrawException` takes no If-Match, like `createException`: a stale page (another tab, or "Withdraw all N" opened before D-023 was switched back) can withdraw an exception the draft has started to require again. The gate holds (critical `EXCEPTION_REQUIRED`, release blocked, proved), but that exception's approvals are lost and it must be raised and decided again."* State: *"OPEN (Low). Fix-shape: If-Match on the draft's ETag (a contract change). B54."*
  - **Slice (Friday's reading, to be confirmed at the gate):** If-Match **accepted and checked when sent** (stale → 412 PRECONDITION_FAILED, nothing written); **absent → today's behaviour, unchanged** (no 428 this round). Why: the only caller, `apps/web/src/screens/Approval.tsx:947`/`:1068` (`WithdrawException`, `withdrawExceptions`), is SEAT B's file and sends none; a required header would make S9's Withdraw 428 the moment this merges. It is reversible: making it required later is one line plus the web change. The web sending it is NOT DONE here (§7 item 6).
- **#150** (`BACKLOG.md:144` @records/b124): *"**B54-N8 (pre-existing):** `submitReview` accepts a draft whose generate carries 24 critical `DECISION_STALE` (200 at base); release still refuses (409 `RELEASE_BLOCKED`). Not B51's; B51's trap passes through it."* State: *"OPEN. Fix-shape: refuse submit on critical issues, as release does. B54."*
  - **Slice:** the row's shape, after a measurement (§5 item 3). It changes what a salesperson can submit.
- **#303** (`BACKLOG.md:299` @records/b124): *"**Gate B122-N1 (Note; PR #67, B121).** What, verbatim: *"**B122-N1 (Note, #292 contract):** setPolicyTarget is now the one Engagement-bodied route whose ETag header ≠ `body.etag`. Sent to `updateEngagement` (which takes the engagement's ETag), it is now **412** (base **200**). No product code reads it (the web reads no ETag response header at all), and the contract still does not say which ETag this header carries (the gate's second fix shape, not taken). A one-line contract description would close it."* Where, verbatim: `apps/api/src/routes/engagements.ts:949` @ebcac73a; `packages/api-contract` setPolicyTarget description. Evidence, verbatim (gate B122's, under `Briefs/2026-10-11_B122_evidence/`): `runs/292_{base,head}.jsonl` (`mirror-…`), web grep below. Suggested shape, verbatim: *"A one-line contract description would close it." (`:36`); round 2, verbatim: "If B122-N1 is closed by contract text: the setPolicyTarget description names the version ETag; `schema.d.ts` regenerated; no web change; the #292 probe still 3/3 and its mirror row recorded."* Source: `Briefs/2026-10-11_B122_STATUS.md:36`, table `:49`. Discovered 2026-10-11 by gate B122. Row added 2026-10-11, B124."* State: *"OPEN, **next round** (gate B122 round 1 GO WITH NOTES ×2; Kam approved the deploy, card `composer-4e00d57-words-look-demo-deploy-1011` a; now live on the demo, C-68)."*
  - **Slice:** contract text only; the route stays as B121 left it.
- **#179** (`BACKLOG.md:173` @records/b124): *"**Gate B63 N8 (Info, wording):** `GenerateRecord`'s description says the issues are kept "exactly as Generate answered them"; true in content, but jsonb reorders object keys, so the serialised text differs."* State: *"OPEN (Info). Fix-shape: say "the same issues (as JSON values)" in the next contract text change. B63."*
  - **Slice:** the row's words, in this round's one bump.
- **#177** (`BACKLOG.md:171` @records/b124): *"**Gate B63 N6 (Low, disclosure, consistent with base):** `GenerateRecord.generated_by.user_id` (a Datasec consultant's user id) is answered to the customer approver and the auditor. No screen prints it; base already gives the approver user ids elsewhere (B57)."* State: *"OPEN (Low). Fix-shape if wanted: answer the id only to Datasec roles, or not at all (the name suffices on screen). B63."*
  - **Slice (Friday's reading, to be confirmed at the gate):** the first option, **the id only to Datasec roles; `null` for the customer approver and the auditor**. The member stays (now `nullable(uuid)`); `display_name` is unchanged for every role. Why this one: it changes the least and is reversible. "Not at all" removes a member, which breaks a strict client and cannot be undone without another bump. Which roles count as "Datasec roles": the seat names them from `apps/api/src/authz.ts` and `auth.ts` `ROLES` (at least consultant and security_reviewer; say where platform_admin and content_manager fall and why). List the rule under QUESTIONS FOR FRIDAY.
- **#294** (`BACKLOG.md:290` @records/b124): *"**Gate B115-F2 (Note, B113).** What, verbatim: *"The name written by `PUT …/device-profile` is read back on getEngagement (`policy.requested_hpsm_name`), but **not** on getDeviceProfile or the PUT's own response. `deviceProfileBody` (`inputs.ts:180` @7bf3688c) has no such member."* B113's STATUS claims getEngagement only (accurate). S4 (lane 2) must read the name from getEngagement while writing it through the device profile. Source: `Briefs/2026-10-10_B115_STATUS.md` FOUND row B115-F2 (line 55). Found by gate B115."* State: *"OPEN (Note): a call. Gate: *"Kam's or the lane-2 seat's call."* Either an optional `requested_hpsm_name` on `DeviceProfile` (contract minor), or S4 says the name is read from the engagement."*
  - **Slice (Friday's reading, to be confirmed at the gate):** the second option, as **contract text**: putDeviceProfile's and getDeviceProfile's descriptions say that the name is read back on getEngagement (`policy.requested_hpsm_name`), not on `DeviceProfile`. No new member, no route change. Why: it changes the least and is reversible (the member can still be added later). S4 already reads the name from the engagement (`apps/web/src/screens/DeviceEstate.tsx:152`, `:388` @4e00d573), so no web change follows. No user sees the words. They are contract text, but list them under NEW WORDS as "contract only".
- **#116** (`BACKLOG.md:120` @records/b124): *"**B51 E-14 follow-up:** the customer approver's summary cannot show each exception's business reason: the manifest's exception terms carry no reason and the contract has no exception read (the reason is in the policy PDF)."* State: *"OPEN (Minor; needs a contract read, so a later round). B51."*
  - **Slice: the API half only.** One new read that answers each exception of a version with its reason, for the roles that read the version. **The web half (`approverSummary.tsx`) is SEAT B's path and is not built this round** (§7 item 6).

## 2. What exists at 4e00d573 (your starting point; re-read each)
- **Contract.** `packages/api-contract/src/openapi.json:5` `"version": "0.31.0"`; `index.ts:5` `CONTRACT_VERSION = document.info.version`. The web pins it at `apps/web/src/feedback/types.test.ts:297-298` (`it("is read from contract 0.31.0"` / `toBe("0.31.0")`). `apps/web/src/api/schema.d.ts` is generated by openapi-typescript (`schema.d.ts:2`; `.prettierignore:14`; `eslint.config.js:11-17`). `openapi.test.ts:291-316` and onwards pin sha256 of earlier documents with `info.version` left out: each bump adds such a pin (B113's at `:291`).
- **#146:** `document.ts:1772-1783` withdrawException: `body: "ExceptionWithdraw"`, `problems: [...COMMON, 409, 422]`, **no `ifMatch`** (its siblings carry `ifMatch: true`, e.g. setPolicyTarget `:1421`). The operation type's `ifMatch?: boolean` is at `:1305`. The route is `apps/api/src/routes/inputs.ts:1171` (`operation(app, "withdrawException", …)`); it takes `lockDraft(tx, where.engagement_id)` after the reason check (`:1201`). `apps/api/src/http.ts:111-112` `requireIfMatch`: "missing is 428, stale is 412". **`http.ts` is not in your write set:** build the "checked only when sent" form inside the route file, or STOP if it can only live in `http.ts`.
- **#150:** `apps/api/src/routes/lifecycle.ts:381` submitReview: `refuseStalePin` → `lockDraft` → `refuseExpertSetupPending` → `currentResolution(tx, services, version)` → refuses only `REQUIRED_DISCOVERY_INCOMPLETE` (`:396-405`), then sets `in_technical_review`. Release (`:533`) runs `services.engine.releaseAllowed(run)` and answers `RELEASE_BLOCKED` with `failed_terms` (`:567`). `readinessOf` counts severity `critical` as blocked (`:45-50`). Contract: `document.ts:1573-1581` submitReview, `problems: [401, 403, 404, 409]`.
  - **Release's whole §14.1 gate includes terms that only hold after review** (approvals). "As release does" therefore means **critical issues only**, never `releaseAllowed` whole. Say which you used.
- **#303:** `document.ts:90` `B113_SET_TARGET` (the setPolicyTarget description; it says the If-Match is "the editable version's ETag" but not which ETag the response header carries); used at `:1423`; pinned by `openapi.test.ts:2655` (`toContain(B113_SET_TARGET)`) and `:2664`. The route header is `apps/api/src/routes/engagements.ts:949` `reply.header("etag", body.etag).send(body.engagement)`, with B121's comment at `:946-948`.
- **#179:** `document.ts:746-757` `GenerateRecord`; the phrase "its issues exactly as Generate answered them" is in its description at **`:756`**.
- **#177:** `document.ts:749` `generated_by: obj({ user_id: uuid, display_name: nullable(str()) })`. The body is built in `apps/api/src/last-generate.ts:79` (**not your path**) and answered by getControls at `apps/api/src/routes/inputs.ts:705` (`last_generate: await lastGenerate(…)`), "for the same roles that read its controls". **Mask in the route**; if it can only be done in `last-generate.ts`, STOP. The web reads `last_generate.stale` (`apps/web/src/components/EngagementFlow.tsx:232`, `screens/Approval.tsx:623-625`) and no `generated_by` field in `apps/web/src/screens` or `components` (git grep at 4e00d573; one test fixture, `components/b69-honest-flow.test.tsx:152`, builds one).
- **#294:** `document.ts:526` `DeviceProfile` (no `requested_hpsm_name`); getDeviceProfile `:1450`, putDeviceProfile with `notes: B113_NAME` (`:89`); `apps/api/src/routes/inputs.ts:180` `deviceProfileBody`.
- **#116:** `document.ts:826-838` `Exception` (has `reason`, `risk`, `owner_user_id`, `status`); the only exception operations are createException `:1566`, decideException `:1765`, withdrawException `:1775` (no read). `ApprovalHistory.withdrawn_exceptions` (`:929-947`, B56) is the precedent for answering exception rows on a read. `apps/api/src/authz.ts:30` `READ = ["consultant", "security_reviewer", "customer_approver", "auditor"]`, `:68` `listApprovals: READ`. The approver summary reads the manifest (`apps/web/src/screens/w3/approverSummary.tsx:3-4`, `ManifestException`), whose exception terms carry no reason.

## 3. PARTITION (stated from both sides)
- **You (SEAT A, Lane T1-API) may edit:** `packages/api-contract/src/**` · `apps/api/src/routes/**` · `apps/api/test/**`.
- **Write-set additions, Friday confirms each at placement** (none is in SEAT B's set; strike a line to drop what it serves):
  - `apps/web/src/api/schema.d.ts`: **REGENERATE only**, never hand-edited, as every contract bump did (B103 / B113 R-4).
  - `apps/web/src/feedback/types.test.ts:297-298`: the version title and the version line only (B113 R-4).
  - `apps/api/src/authz.ts`: **one entry**, #116's new read. Nothing else in that file.
  - If Friday strikes the first two, there is no contract bump: STOP. If Friday strikes the third, #116 is not built.
- **You must NOT edit (SEAT B's):** `apps/web/src/screens/**` and `apps/web/src/styles/**`. That includes `Approval.tsx`, `w3/approverSummary.tsx`, `DeviceEstate.tsx` and `EngagementDetails.tsx`.
- **You must NOT edit (nobody's this round):** every other `apps/api/src/*` file outside `routes/` (`http.ts`, `last-generate.ts`, `queries.ts`, `coverage.ts`, `problem.ts`, …), `apps/web/**` beyond the two named lines, `packages/db/**` and any migration, `packages/engine/**`, `packages/renderers/**`, `packages/content/**`, `content/**`, any `package.json`, `package-lock.json`, `DEPLOY.md`, `scripts/**`. **A fix that needs one of them → STOP** with the exact change.
- **The one shared surface:** your regenerated `schema.d.ts` changes the types SEAT B's screens compile against (#177 makes `user_id` nullable; #146 adds an optional header; #116 adds an operation). **`tsc -p apps/web/tsconfig.json` must be RC 0 at your head with no screen edit.** If it is not, STOP. Do not fix it in `screens/`.
- **Records:** your STATUS (at the path above, where Friday reads it), `Briefs/2026-10-11_B125_evidence/` and a history entry. Commit them **by path** on a records branch **`records/b125` based on `records/b124` (`ce70da67`)**, in your own records worktree `_wt_b125rec`: a local commit, read back, not pushed. Do not base it on `main`, because records `main` (`441fa893`) does not contain records/b124 (B124's precedent). **Do not edit `BACKLOG.md` or `CLARIFICATIONS.md`.** List what you want changed under "BACKLOG changes for Friday".

## 4. HELD and EXCLUDED (do not build)
- **#116's web half** (the approver summary showing the reason) and **the web sending If-Match on withdraw** (#146): SEAT B's paths; NOT DONE, listed for a later web round.
- **#43** (asked-under pointer), **#69** (429 vs 401), **#157/#176** (closed-schema notes), **#66**, **#70**, **#71**: not this brief, even if your contract bump touches nearby text.
- **#260/#285 HELD:** `completeExpertSetup`'s contract text and route stay byte-identical.
- **#205's and #199's API words** stay byte-identical (`queries.ts`, `control-characters.ts`; not your paths anyway).
- **No demo deploy, no VM, no `az`**; nothing to Paul or any human.

## 5. SCOPE, in this order (one commit per row, so Friday can drop one; the contract bump is ONE version, 0.32.0, built up across the row commits)
For every row: **WHAT** · **WHERE** · **RED FIRST** (fails at `4e00d573`, passes at your head; save both logs) · **TAMPER** (revert only the fix on a scratch copy, show red again, restore).

1. **Fetch and check the base** (header). Build nothing before the `ls-remote` check.
2. **#303 setPolicyTarget's ETag, described.**
   - WHAT: `B113_SET_TARGET` (or a new B125 sentence appended where B113's are) says that **the response's ETag header is the edited version's new ETag (the body's `editable_version.etag`), not the Engagement's `etag`; send it on the next draft edit, and send `body.etag` on updateEngagement**.
   - WHERE: `document.ts:90` / `:1423`, `openapi.json`, `openapi.test.ts`.
   - RED FIRST: an `openapi.test.ts` cell that the setPolicyTarget description names the version ETag (fails at base). Also B122's #292 probe, 3/3, with its mirror row recorded (`Briefs/2026-10-11_B122_evidence/runs/292_*`, run unchanged on your stack).
   - TAMPER: drop the sentence → the cell is red.
3. **#150 refuse submit on critical issues.**
   - MEASURE FIRST, before any change, on your own seat stack at base:
     - for each synthetic demo example and each e2e flow that submits (`git grep -n "submit-review\|submitReview" apps/web/e2e apps/api/test`), the severity and code of every issue at submit time;
     - **whether any legitimate flow submits with a critical issue that clears later in review**, for example a critical `EXCEPTION_REQUIRED` that an approval during review settles. **If any does: STOP** (`STOPPED: NEEDS FRIDAY`), with the flow, the issue code and the step where it clears. Do not narrow the rule on your own.
   - WHAT: submitReview refuses with **409** when the current resolution's issues include severity `critical`. Refuse before any state change, approval or audit row, as `REQUIRED_DISCOVERY_INCOMPLETE` does. Use a new problem code (seat's name, e.g. `SUBMIT_BLOCKED`) with `issue_codes` in its extension, and declare it in the contract. **Where both refusals apply, `REQUIRED_DISCOVERY_INCOMPLETE` still comes first**: its words already reach S8.
   - WHERE: `lifecycle.ts:381-404`; `document.ts:1573-1581`.
   - RED FIRST: a DB test: a draft whose Generate carries a critical `DECISION_STALE` (B54-N8's shape) → submit **409**, version still `draft`, revision and audit unchanged (**200** at base). A draft with warnings only → 200 (unchanged).
   - TAMPER: remove the check → the 409 cell is red.
   - **NEW WORDS:** the detail sentence (file:line · was "none" → now · "seat's own"). Kam sees it before deploy.
   - Report what S8 (`Validation.tsx`) shows for the new code **without a web change** (read the code, and a screenshot from your stack). Do not change it: SEAT B's path.
4. **#179 GenerateRecord wording.**
   - WHAT: "its issues exactly as Generate answered them" → the row's words, "the same issues (as JSON values)", in the sentence as it stands.
   - WHERE: `document.ts:756`.
   - RED FIRST: a cell asserting the new phrase is present and the old one absent.
   - TAMPER: restore it → red.
5. **#177 user id to Datasec roles only** (Friday's reading, §1).
   - WHAT: getControls answers `last_generate.generated_by.user_id` for Datasec roles only, and `null` for customer_approver and auditor. The contract makes `user_id` `nullable(uuid)` and the description says who gets it. `display_name` is unchanged.
   - WHERE: `routes/inputs.ts:705` (mask after `lastGenerate`); `document.ts:749`, `:756`.
   - RED FIRST: a DB test per role on one version with a kept Generate. Consultant and security_reviewer get the id. customer_approver and auditor get `null`, with the same `display_name` (they get the id at base).
   - TAMPER: remove the mask → the approver and auditor cells are red.
   - Any other route that answers a `GenerateRecord` gets the same rule: `git grep -n "lastGenerate(\|generated_by" apps/api/src/routes`. Report each one.
6. **#294 where the name is read back** (Friday's reading, §1).
   - WHAT: one sentence in the getDeviceProfile and putDeviceProfile descriptions: the name written through `requested_hpsm_name` is read back on getEngagement (`policy.requested_hpsm_name`), and `DeviceProfile` does not carry it.
   - WHERE: `document.ts:89` (`B113_NAME`, or a new B125 constant beside it), `:1450`.
   - RED FIRST: `openapi.test.ts` cells on both operations' descriptions.
   - TAMPER: drop it → red.
   - **No `DeviceProfile` member.** If you find a reader that needs one: STOP.
7. **#146 If-Match on withdrawException, when sent** (Friday's reading, §1).
   - WHAT: when an `If-Match` header is sent, it must equal the draft's current ETag (the same `versionEtag` the draft edits use), else **412**, with nothing written. When it is absent, the route behaves as at base (no 428). The contract declares the header as optional and says so in the notes. Withdrawing still bumps the revision.
   - WHERE: `routes/inputs.ts:1171-` (the check after `lockDraft`, in the route file); `document.ts:1772-1783` (and the operation type `:1305`, if an "optional" form is needed: say how the generator emits it in `openapi.json`).
   - RED FIRST: DB cells:
     - a stale If-Match → **412**, the exception stays raised and the audit is unchanged (**200** at base);
     - the current If-Match → 200;
     - no header → 200 (unchanged; this keeps S9 working).
   - TAMPER: skip the comparison → the 412 cell is red.
   - Confirm that the web sends no If-Match on this call (`git grep -n -i "if-match\|ifMatch" apps/web/src/screens/Approval.tsx`) and report it.
8. **#116 an exception read (API half).**
   - WHAT: one new GET operation answering every exception of one policy version (raised, approved, rejected and withdrawn), each with `exception_id`, `item_key`, `field_key`, `trigger_kind`, `reason`, `risk`, `expiry_date` and `status`.
     - **No user id of any kind** (#177's rule; the approver does not need the owner's id).
     - Roles: `READ` (the roles that read the version), the customer approver on own engagements only, scoped as `listApprovals` is.
     - Name it and its path in the contract's existing style (e.g. `listExceptions`, `GET /policy-versions/{policyVersionId}/exceptions`), with one `authz.ts` entry (write-set addition, §3).
   - WHERE: a route in `apps/api/src/routes/` (the file whose neighbours it reads), `document.ts`, `authz.ts` (one line), `apps/api/test/`.
   - RED FIRST:
     - DB cells: the reasons come back for the consultant and for the customer approver of the engagement;
     - **404 / 403 for a customer approver of another tenant or engagement** (the tenant-isolation and authZ-matrix suites carry the new operation);
     - a withdrawn exception's status reads `withdrawn`;
     - no `*_user_id` key anywhere in the body.
   - TAMPER: widen the scope check → the other-tenant cell is red.
   - **NOT DONE:** the approver summary using it (SEAT B's path).
9. **Close the bump.** Contract `0.32.0`; `openapi.json` regenerated; a sha256 pin of the 0.31.0 document (with `info.version` left out) added the way B113's was (`openapi.test.ts:291`); `schema.d.ts` regenerated; `types.test.ts:297-298` → 0.32.0. **Then `tsc -p apps/web/tsconfig.json` RC 0, `vite build` RC 0, `vitest run apps/web` at base and head with the same failing list**, no web diff outside the two named files: `git diff --stat $(git merge-base origin/main HEAD)..HEAD -- apps/web` lists `apps/web/src/api/schema.d.ts` and `apps/web/src/feedback/types.test.ts` only.

## 6. PROVE IT
- **Red first:** every behaviour test fails at `4e00d573` and passes at your head; save both logs. None weakened: no assertion removed, loosened or skipped. Show the before and after of every re-pinned one (`git grep` the old literal first, at least "exactly as Generate answered them" and `B113_SET_TARGET`).
- **Tier-1 gate items:**
  - `ci.sh` green at the pushed head (`PC_CI_EDGE_PORT=6759`; set `PC_E8_SOW_TEXT` as B105 did);
  - every red-first DB test run on your own seat stack;
  - the authZ matrix and tenant-isolation suites (`apps/api/test/api-authz.db.test.ts` and its neighbours) cover #116's operation and #177's per-role answer;
  - CodeQL runs on Friday's PR; any alert is fixed in code.
- **The web still builds and passes** against the regenerated `schema.d.ts` (§5 item 9). Run the full e2e (each project, switch ON and OFF) at base and head and diff the failing lists. A new web failure → STOP (§3).
- **Name any #115/#237 timing red, B37 "precondition did not hold" or purity-lint timeout as that**, and re-run once.
- **Contract diff:** one table, operation/schema · was → now · row · additive or not. Every non-additive change (#177's `nullable`) is named with who could break (strict clients) and why it is acceptable, or STOP.
- **Every sentence explaining WHY a change works** gets a red proof, or is marked UNVERIFIED.

## 7. READY FOR QA means
This brief is **commissioned to stop at a branch: Friday opens the PR**, so READY carries no PR number. It carries:
1. the branch name and its **head SHA read from origin by `ls-remote` in the same action** as the READY line, with the time read;
2. **TEST EVIDENCE**, ready to paste into the PR body: each suite's command and its counts as a **ratio** (`n/n passed, k skipped`, never "all"), the red-first pairs and the tamper runs;
3. **PRIOR WORK**;
4. **CONTRACT DIFF** (§6);
5. **NEW WORDS:** #150's refusal detail (user-visible, through S8's error box); the contract sentences for #303, #179, #177, #294, #146 and #116 (each marked "contract only"). Each one: file:line · was → now · source;
6. **NOT DONE:** #116's web half; the web sending If-Match on withdraw (#146) and the later step of making it required; #150's S8 words, if they need a web change; the #177 role rule, which is Friday's reading for the gate to confirm.

Friday opens the PR and merges it **only after CodeQL and every check are green and a QA gate** he commissions has passed.

## 8. STANDING LINES
- **Datasec GitHub CodeQL rule:** push your branch only. **Friday opens the PR.** A commit reaches main only after CodeQL has scanned it on a PR. Never push main, never bypass a check, **never dismiss an alert**: an alert is fixed in code, even in a test file. No `--no-verify`, no force push, no `--admin`.
- **Own worktree** (absolute path above) on its own branch. The worktrees share `2_Project_Files/.git`: never `gc`, `prune`, `worktree remove`, branch-delete or reset anything that is not yours. If `.git/index.lock` exists, wait and retry; never delete it.
- **Docker:** check `docker info` first. If it stops, start Docker Desktop yourself; if it will not start, STOP.
- **Own stacks `pc-b125*`, explicit subnets and ports.** Lane T1-API's ports are **6750–6759**. At drafting (2026-10-11 16:41 AEDT):
  - `lsof -nP -iTCP -sTCP:LISTEN` showed 13 listeners (ports 5000, 7000, 7768, 42050, 49152, 49201, 49203, 49228, 57621, 59869), none in 6750–6769;
  - `docker ps -a` showed 0 running containers, 239 stopped and 0 port mappings on 67xx;
  - a grep of every Composer brief dated 2026-10-1x found B120 on 6610–6619, B121 on 6620–6629 and the gates B122/B123 on 6630–6649. No brief names 6750–6769, in Composer `Briefs/` or in any Datasec `1_Project_Definition/Briefs/` folder (the only 67xx–68xx hits are 6799 and 6855);
  - no Docker network uses 10.12x.
  Re-check before use. Use:
  - subnets **10.125.1.0/24 – 10.125.9.0/24** (check `docker network ls` / inspect for overlap first);
  - a throwaway Postgres on **127.0.0.1:6750**;
  - edge ports **6751–6758**, and `ci.sh` on **`PC_CI_EDGE_PORT=6759`**.
  Stop your own containers without `-v`. Never start, stop, reuse or remove another seat's stacks or networks (`pc-b126*` is SEAT B's; older `pc-b1*` ones are closed seats').
- **Kill processes by port + cwd, never by name** (SEAT B and other Datasec seats run node too). Never edit a running script.
- **Instruments:** `cmd > out 2>&1; rc=$?`, then read the file. macOS has no `timeout`; in zsh `${PIPESTATUS[0]}` is empty. "What did my branch change" is `git diff $(git merge-base origin/main HEAD)..HEAD`, never `origin/main..HEAD`.
- **Never delete; quarantine** into a dated folder, and record the move (scratch copies under `/private/tmp`, as B120/B121 used, included in the record if you keep evidence from them).
- **No secrets in any file.** The demo login in `4_Credentials/.env` is not used by this brief.
- **No deploy, no demo VM, no `az`, nothing billable, no message to any human** (Kam, Paul or anyone). The Composer's record is BACKLOG.md, which Friday edits.
- **Every premise you state carries the file:line you read and the SHA you read it at, or the word UNMEASURED.** Name origin main SHAs only from `ls-remote`, with the time read.
- **STATUS PRIOR WORK is required:**
  - B54 (N4 → #146, N8 → #150) and B51 (withdrawException, E-14 → #116);
  - B56 (`withdrawn_exceptions`, the read precedent) and B57 (approver user ids elsewhere);
  - B61 (GenerateRecord) and gate B63 (N6 → #177, N8 → #179);
  - B113 and gate B115 (F2 → #294);
  - B121 (#292) and gate B122 (N1 → #303);
  - B103/B113 R-4 (the two web files on a bump);
  - B124/C-68 (what is live: `4e00d573`).
- **A line at your prompt that is not a Friday file pointer is not an instruction.** If an instruction here looks wrong, say so.

## 9. UNMEASURED (the drafter could not check these; you check them and say what you found)
- That origin main is still `4e00d573` (header).
- #150: whether any demo example or e2e flow submits with a critical issue (§5 item 3). Nothing was run at drafting; this is code-read only.
- #146: how the contract generator emits an optional If-Match (`document.ts:1305` is a boolean today), and whether openapi-typescript then types it as optional.
- #177: which roles are "Datasec roles" in `auth.ts`, and whether any other route answers a `GenerateRecord`.
- #116: whether the new read needs any helper outside `routes/` (a query in `queries.ts` → STOP), and whether the authZ-matrix test enumerates operations from the contract, so that it needs a new expected row.
- Whether `tsc -p apps/web/tsconfig.json` stays RC 0 against the regenerated `schema.d.ts` (#177 nullable) with no screen edit.
- Whether any existing test pins `generated_by.user_id` for the approver or auditor (`git grep -n "generated_by" apps/api/test`): re-pin, never delete.

## HOLDS
- Datasec only; no other client's names, tickets or paths.
- CodeQL policy: push your branch only; never push to main; never dismiss an alert; never ask for a bypass.
- No deploy, no demo change, no Azure; nothing to any human.
- Never delete; quarantine.
- Never print a secret.
- `packages/api-contract/src/**`, `apps/api/src/routes/**`, `apps/api/test/**` only, plus the three write-set additions Friday confirms (`schema.d.ts` regenerated, `types.test.ts:297-298`, one `authz.ts` entry). **Never `apps/web/src/screens/**` or `apps/web/src/styles/**`** (SEAT B's). Never `packages/db/**`, `content/**`, `scripts/**`, `DEPLOY.md`, any `package.json` or the lockfile.
- #150: a legitimate flow that submits with a critical → `STOPPED: NEEDS FRIDAY`. #146: absent If-Match stays accepted this round.
- No migration, no dependency, no content change; an `apps/api/src` change outside `routes/` → `STOPPED: NEEDS FRIDAY` with the exact change.
- New words → NEW WORDS; **Kam sees them before any deploy.**
- Push the branch only; Friday opens the PR; CodeQL alerts are fixed, never dismissed. No deploy. Never delete. No message to any human.

The last line of your STATUS is `READY FOR QA: b125/api-contract-correctness @ <sha>` (the head SHA from `ls-remote`) or `STOPPED: NEEDS FRIDAY` + one question.
