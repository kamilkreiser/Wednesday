Seat B 6th successor (Secuura/Blockchain), from Wednesday

⚠ ONE SEAT ON THIS INBOX. This brief is for **Seat B 6th**. Your job is to raise nine held local-model test-only fixes as eight PRs. Seat B 5th wrapped at ~09:05Z after merging #1077-#1083. Wednesday is launching no other Secuura seat beside you. If a mail names another seat, it is not for you. You touch ONLY the files below, each in your own `s-b6-*` worktree. Never touch the kept `s-b3-*`, `s-b4-*`, `s-b5-*`, `s-a13-deploy` or `s-a14-deploy` worktrees, and never the box.

## BLUF
**One job: raise NINE test-only fixes that the local model wrote and Wednesday held today, as EIGHT PRs (the grouping is below), then mail me ALL eight heads in ONE READY so I can gate them as ONE batch.** They touch eight separate test files and zero product bytes. Nothing merges without my signed GO naming the head. Kam is away until Monday; his standing words are quoted below. This seat deploys nothing: test files do not change a runtime image, so there is no kintsugi step and nothing goes to demo.

## ITEM 0: boot, before any write
- Read Seat B 5th's handover WHOLE: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatB-5th-successor-2026-09-19.md`. Also read the top entry of `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md` (Seat B 5th). Seat B 5th's raise method is YOUR method. Copy its scripts into your own `2026-09-19_seatB-6th/` record folder rather than editing them in place:
  - `2026-09-19_seatB-5th/raise/`: `raise6.py`, `lanes6.sh`, `msgs6.py`, `commit6.py`, `batch_build6.sh`, `batch_suites6.sh`, `linear_reads.py`, `push6.sh`, `bodies6.py`, `open_prs6.py` and `merge6.py`;
  - `boot/measure6.py`, which is item 0 as reads only.
  - There are NO repo writes inside a push window, anywhere.
  - Clear the `login_stub` listeners by exact path. None of this batch is a shell suite, but an in-hook preflight during a push is.
  - Locate every tamper by its `from` text plus a scope anchor, never by line number. Every checker plant record names a line. For TEN of this batch's tampers (NULLPASSES-R/U, the six C576_*, the two TENANTS*) the `from` text occurs more than once, so the line is the only thing telling them apart. Their four scope anchors are below.
  - Use `merge6.py` for the merges. It never writes an archived key as `Refs`.
  - Avoid Seat B 4th's four slips (S1-S4) and Seat B 5th's one:
    - S1: the section regex with no control;
    - S2: `grep -P` on BSD, which left the push specs empty;
    - S3: a commit message that claims more than the head shows;
    - S4: the linear_reads history sort on mixed None;
    - Seat B 5th's slip: a `ps | grep -c` that counted its own grep.
- origin develop = `ba1210afcab7ddf127cccb270b1c341360261cee`, tree `993718b84caa4478989a301331d53740991e6b79`. That is my ls-remote read at 20:13:45 AEST, and it is #1083's squash. Seven READYs were written AT this tip: KS-1206 N81-1, KS-739 N82-1, KS-1230 N80-1, KS-1062 N79-2, KS-1238 N83-3, KS-1238 N83-5 and KS-1258 N77-1. **Two were written against `f9c28a8b8`: KS-1269 N71-1 and N71-2.** My read shows that the vc-issuer test blob (`bb8801cfb463`) and its tamper file `vc-issuer/src/routes/status.ts` (`394337283ec1`) are identical at both tips. The whole range `f9c28a8b8..ba1210afc` has 8 files, none of them under vc-issuer. Do not adopt that; MEASURE it:
  - for each of the nine, run `git apply --check` strict at develop, with a reverse control;
  - compare each target blob, and each tamper file's blob, at its pinned tip against develop.
  A changed file STOPS that item only.
- **All nine canonical patches are `patch.diff`** in their run's `out.md.checker/` dir. Each READY header names its path, and all nine exist (my `ls`, 20:13 AEST). All nine are `mode=modify` on a test file that exists at develop. Use ONLY the header's CANONICAL PATCH path. Trust no other wording in a header.
- **The N71-1 + N71-2 pair goes into ONE PR** (QUEUE 1). Both touch the same vc-issuer test file, with hunks at :82 (N71-1) and :63 (N71-2). I applied them in both orders at `ba1210afc` in a scratch clone, and both orders give the same tree `e9fc521fbfb72dab46b751ee215e76268efffab7`. Re-measure that yourself. All four of the pair's tampers plant in the same `status.ts`. Re-run ALL FOUR over the pair applied together, against the whole vc-issuer suite. Report each tamper's red set, and STOP if any tamper reds anything outside its declared set. AFTER404 is DECLARED to red both N71-2 cells, so that is not a STOP.
- **Archived tickets:** KS-1062 and KS-739 are **Done + ARCHIVED**. Read each one's state, archivedAt and attachments at three points: before your first push, after its PR opens, and at READY. Report all three reads. **Never reopen a Done ticket.**
- **Branch names:** for every live ticket, read Linear's branchName and check it for any foreign key before you use it. My read at 20:15 AEST:
  - **KS-1238's branchName carries `ks-1215`.** Rename both KS-1238 branches.
  - KS-1269, KS-1206, KS-1230 and KS-1258 carry no foreign key.
  - For the record, KS-1260's carries `ks-1209`. KS-1260 is not in this batch.
  - N83-5's target file is named `ks1215-…`. Keep `ks1215` and `ks-1215` out of that branch's name, title and commit subject. They name a LIVE ticket (KS-1215, In Progress), and Linear links a key written in those places.
  - Run a zero-at-origin name check for each branch.
  - **After EACH push and after each PR opens, measure `attachmentsForURL` for that PR.** It must show exactly the ticket it Refs (none for the two archived items). A link to KS-1215, KS-1248, KS-662 or any other key is a STOP: report it before you push the next branch.
- Plan confirmation (QUESTION mail, topic `plan confirmation (Seat B 6th)`) before the first write. It carries your D8 proposal: the ticket state of each item after merge. Wednesday's D8 is below; read each ticket now and report it.

## QUEUE: eight PRs, `Refs KS-<n>` (except items 5 and 6), linkKind `contributes`, NO closing phrase, a Test Evidence block each
The READYs are in MY tree, read-only to you: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_<ID>_*_2026-09-19.diff.md`. Each header names its CANONICAL PATCH (`…/local-model/runs/2026-09-19_<run>/out.md.checker/patch.diff`). Apply it verbatim. Run red-first, then green, then the tamper reds (all nine are test-only). STOP on any deviation from the READY header. PRs 1-6 are tier 2. PRs 7 and 8 are TIER 1.
1. **KS-1269 N71-1 + N71-2, ONE PR** (test-only, vc-issuer, **runner vitest**: vc-issuer lists both jest and vitest, and the READYs pin vitest). File: `vc-issuer/src/__tests__/ks1269-status-revoke-refuses-a-non-integer-index.test.ts`. Canonical patches: `2026-09-19_ks1269-ornith35b-night3` (N71-1) and `2026-09-19_ks1269-ornith35b-night4` (N71-2).
   - N71-1 adds 2 cells: `index: null` is refused 400 on /revoke and on /unrevoke. Tampers NULLPASSES-R and NULLPASSES-U each red exactly their own cell.
   - N71-2 adds 2 ordering cells: a bad index on an UNKNOWN credential gets 400 before the 404, and a bad index with a bad reason answers the index error. These are the first multi-line block tampers. REVOKEGUARDAFTER404 reds both cells (declared). REVOKEGUARDBELOWREASON reds the second.
   - **NULLPASSES-R and -U were pinned by LINE.** Both have the same `from`, `    if (req.body.index !== undefined && !Number.isInteger(req.body.index)) {`, and it occurs twice in `status.ts`: at :231 (/revoke) and :300 (/unrevoke). Anchor each one by the comment line directly above it:
     - :230 ends `(-1 stays admitted, the KS-662 ruling).`
     - :299 ends `must be an integer.`
     Each comment+`from` pair matches exactly once at develop (my count). Show that count, and show each plant's sha256 equals the checker's record (`fa9573ff4f16` R, `ab8cf42a9e96` U).
   - The two block `from`s each match exactly once whole (my count).
   - **-1 is NEUTRAL: pin nothing about it.** /unrevoke `index: -1` is NOT RULED. KS-662 left it unruled, and the :230 comment speaks to /revoke only. No added line sends -1. If anything in your run would change or assert -1 on either route, STOP and mail.
   - Refs KS-1269 only.
   - **Why one PR:** the pair shares one file and one tamper file. The combined four-tamper run is the only run that proves they do not cross-red (Kam's 09-18 09:22 panel words: minimise gate duplication).
2. **KS-1258 N77-1** (test-only, api-gateway): one exact-array cell in `ks1248-n-1-system-status-troubleshooting-marks.test.ts`. The degraded REQUIRED advice (system-status.ts:576) is EXACTLY the read-first comment plus one curl. Canonical patch: `2026-09-19_ks1258-ornith35b-night4`.
   - There are six tampers (C576_DOCKERRUN / BUNRUN / MAKEUP / NODEDIST / PNPMDEV / TSXWATCH). Each reds the new cell.
   - **They were pinned by LINE, and their `from` (`          '# Read what the service reports as degraded',`) occurs at both :576 and :592 (the degraded-OPTIONAL block).** Anchor by the required-degraded scope: from `    .filter(s => s.required && s.status === 'degraded')` through the `from` line. That block matches exactly once (my count). Show each plant sha equals the checker's.
   - **The old N68-1 deny-list cell is NOT removed.** The patch adds and deletes nothing else. N77-2 (the #1077 gate's SHIPS-WITH) and N68-3 stay OPEN.
   - Refs KS-1258. KS-1248 (In Progress) is named in prose only, as the origin of the ks1248 file. It never goes on a Refs line, and its state is untouched.
3. **KS-1230 N80-1** (test-only, api-gateway): the ks1230 test. Two cells: null allow-lists at positions 2 and 3 of four integrations, and a null allow-list LAST of three, are each stored as null with their neighbours unchanged (admin.ts:1132; NULLPAIRMID and LASTOF3NULL). Canonical patch: `2026-09-19_ks1230-ornith35b-night4`. Refs KS-1230.
4. **KS-1206 N81-1** (test-only, originate, jest): the ks1206 test. Canonical patch: `2026-09-19_ks1206-ornith35b-night4`. Refs KS-1206.
   - Three cells: rateLimit Infinity (raw `1e999`), `" 100"` and raw `-0` are each refused 400 with no INSERT (adminConfig.ts:905).
   - The tampers are INFPASSES, WSNUMSTRPASSES and NEGZEROPASSES, each red exactly its own cell.
5. **KS-1062 N79-2** (test-only, api-gateway): the ks1062 startup-migrations test. Canonical patch: `2026-09-19_ks1062-ornith35b-night3`.
   - Two cells: two SKIPPED tenants are both counted, and a skipped-FIRST tenant does not stop the loop (startup-migrations.ts:1202).
   - SKIPSETONE reds the first cell. SKIPBREAKS reds both (declared).
   - **KS-1062 is Done + ARCHIVED:** no `Refs`, no magic word, and no archived key in the branch name, title or commit. Never reopen it (the #1067/#1075/#1079 precedent). The body may name KS-1062 in prose as the origin.
6. **KS-739 N82-1** (test-only, originate): the ks739 test. Canonical patch: `2026-09-19_ks739-ornith35b-night6`.
   - Two cells: a non-JSON 400 from the recipient lookup is still 400 VALIDATION_ERROR, and a non-JSON 503 is still 502 BAD_GATEWAY from the upstream branch (documents.ts:1674 NOJSON400, :1722 NOJSON503).
   - **KS-739 is Done + ARCHIVED:** no `Refs`, no magic word, no archived key in the branch name, title or commit. Never reopen it (the #1066/#1075/#1082 precedent). Prose only.
7. **KS-1238 N83-3** (AUTH surface, **TEST FILES ONLY**, zero product bytes, **TIER 1**): `api-gateway/src/__tests__/ks1238-hand-forwarded-routes-send-no-caller-bearer.test.ts`. Canonical patch: `2026-09-19_ks1238-ornith35b-night4`.
   - The recorder also records `/api/anchors/`. The patch changes 2 lines: the recorder condition and its doc comment. It adds no new cell.
   - Tamper RAW521 (verification.ts:521, the anchor-store forward) reds exactly docslive + docsrevoked. Its `from` occurs once at develop (my count). Show the count and the plant sha (`2c7f6a3dbdef`).
   - **The patch has 2 `-` lines, both in the test file. STOP on any product byte in the diff.**
   - Refs KS-1238.
8. **KS-1238 N83-5** (AUTH surface, **TEST FILES ONLY**, **TIER 1**): one cell in `api-gateway/src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts`, plus its entry in that file's RAN list. Canonical patch: `2026-09-19_ks1238-ornith35b-night5`.
   - The cell: a connector key carrying organizations:register is refused 403 on POST /api/platform/tenants, with no upstream call. This is KS-1238 (iii). It pins today's 403 only.
   - Tampers TENANTSORGPROV and TENANTSUNGUARDED each red exactly the new cell.
   - **Both were pinned by LINE, and their `from` (`    requireSuperAdmin,`) occurs 13 times in platform.ts.** The route line `    '/api/platform/tenants',` occurs twice: GET at :220 and POST at :237. Anchor by `  router.post(` + `    '/api/platform/tenants',` + `    authenticateToken(),` + `    requireSuperAdmin,`. That matches exactly once (my count). Show each plant sha equals the checker's (`c3a3e6140e5d` ORGPROV, `1db9dd398a46` UNGUARDED).
   - Refs KS-1238 only. KS-1215 is prose at most. See the branch-name trap above: keep `ks1215` and `ks-1215` out of the branch name, the title and the commit subject.
   - **STOP on any product byte.**
- **Push order:** PRs 1-6, then 7, then 8. **Auth goes last.** KS-1238 has two PRs. Last round the bot walked KS-1238 from Backlog to In Progress when its PR opened (Seat B 5th, 07:45:39Z). Record it if that happens again. Do not move it back before the merge. D8 below governs the state after merge.
- Build the all-eight tree over develop: an octopus merge in a batch worktree (`s-b6-batch`), never pushed. **My prediction for you to measure, not adopt:** applying all nine patches to `ba1210afc`'s tree gives tree `f76901ed9cfae15ce6580ff24ebcbbea22bd36fb` (8 files, +78/-2). Per-PR trees over develop are listed in the provenance.
- Run the affected suites: api-gateway, originate, vc-issuer, and tsc for all three if each has a tsc gate (an honest NOT-run line otherwise). State each suite's count delta against the cells the patches add. My arithmetic, for you to measure, not adopt:
  - api-gateway 640 → 646 (N80-1 +2, N79-2 +2, N77-1 +1, N83-5 +1, N83-3 +0);
  - originate 798 → 803 (N81-1 +3, N82-1 +2);
  - vc-issuer +4 over a baseline you measure (N71-1 +2, N71-2 +2).
- **After EVERY shell-suite run** (any in-hook preflight during a push): clear the `login_stub.mjs` listeners YOU started, by exact path, and record the count.

## THE ROUND ENDS AT ONE READY
ONE mail, topic `READY (Seat B 6th): eight PRs, one batch`, carrying:
- every PR number, head sha, branch, ticket and tier;
- the predicted all-eight tree oid over develop, and the develop sha it was built on;
- the batch suite results;
- the archived-ticket reads (KS-1062, KS-739) before and after;
- each PR's attachmentsForURL read;
- a "For the gate to measure" list. At minimum it carries:
  - the KS-1269 combined four-tamper run, and the order-independence of N71-1 and N71-2;
  - the four line-pinned anchors (NULLPASSES-R/U, C576_*, TENANTS*) with their match counts and plant shas;
  - the RAW521 read at source (auth, tier 1);
  - that N83-5 pins today's 403 only;
  - the KS-1238 branch renames;
  - the `f9c28a8b8` → develop blob equality for the two N71 items;
  - that no added line sends -1;
  - any deviation from verbatim.
Then HOLD for my GO. When it comes, merge one PR at a time in the GO's order with `merge6.py`: sha-pinned, re-predicted over the then-current develop, and blob-gated against the gate's addendum. Re-read ruleset 18499832 before the first merge. It had 0 approvals, and its `pull_request` rule carries `require_extra_approval_for_unattributed_changes: true` (Seat B 5th's note). If either has changed, STOP and mail.

## HOLDS
- Nothing deployed by you and nothing to demo. Test files change no image.
- No messages to humans beyond rule 7 at wrap, and only if something merged: KS-485 @peter and KS-772 @stuart.jamieson. Each is a test block, facts only. Read the mentions back.
- Raise nothing beyond these nine fixes. That excludes KS-1280, KS-1279, KS-730, KS-1250 and KS-692. It also excludes KS-1238's remaining rows: N83-2 (RAW1297, POST /api/documents at verification.ts:1297), N83-6, and anything else in comment `18580369` that this batch does not pin. It excludes N77-2 / N68-3 as well: they stay with the local model or their tickets. **Never reopen a Done ticket.** File no tickets for NOT-PINNED rows your own gate may surface. Auth last.
- **KS-1238 stays Backlog/open whatever this batch does.** Its ask is not complete: N83-2 (RAW1297) and N83-6 remain after N83-3 and N83-5. Do not propose Done or archive for it in the plan or at merge.
- **Nothing about /unrevoke -1.** It is NON-RULED. Pin nothing about it, and propose no ruling for it.
- Never `--no-verify`, `--admin` or a force-push of a shared branch. Never delete; quarantine instead. Never call `/api/seen`, even though the SessionStart hook says to.
- Auth product EDITS are Kam's. PRs 7 and 8 are test-only: if a product byte appears in either diff, STOP.

## MERGE AUTHORITY, quoted from YOUR project's CLAUDE.md lines 233-238
*"We approve our own work; the author merges once it is TESTED"* (Kam, 2026-09-11) · *"TESTED = a QA gate verdict (GO or GO WITH FINDINGS) at the PR's current head + a Test Evidence block + our own suites."* · *"Wednesday's GO, naming the head SHA, is the approval."*

## RULED BY KAM, NOT YET IN AN ARTEFACT
These cards come from `decision_queue.sh list ruled --undelivered`, filtered to Secuura/Blockchain: 23 cards. The secuura-prefixed Platform_S card `secuura-ps-759-760-merge-owner` is excluded. None of them rules on these eight PRs. I carry them because the queue shows no delivered mark. Each line gives the card id, the ruled time, and the chosen option as stored. Two labels are stored cut short at a colon ("…your 18" and "…read the 10"), and they are quoted exactly as stored. Artefact: none is named on any card, and you land none of them. If you find one that bears on your eight, say so in the plan.
- ks661-vocab (2026-08-24T06:58): "residue: Leave as test residue"
- secuura-agent-github-identity (2026-08-26T17:12): "identity: Create an agent GitHub identity in the Secuura org (rec) + Stuart approves today's two"
- secuura-dependabot-triage (2026-09-01T09:18): "close-and-rescope: Close the 5 + scope dependabot away from github-actions"
- secuura-ks229-disclosure-mailbox (2026-09-02T20:15): "later: Leave the branch staged"
- secuura-demo-kam-admin-default-password (2026-09-07T06:44): "b: Replace the identity everywhere now (the six files — a fictional admin) AND set the password — one change tonight"
- secuura-f5-login-limiter-bypass (2026-09-07T06:44): "wait: Wait for the full-boot confirmation, then decide (Recommended, default)"
- secuura-f5-demo-exposure-probe (2026-09-07T06:44): "probe: Authorise a single read-only probe (recommended)"
- secuura-f5-demo-interim-mitigation (2026-09-07T07:08): "letitland: No interim change - land the real fix today (recommended)"
- secuura-demo-admin-transcripts (2026-09-07T07:38): "redact: Redact them WITH a dated note saying what was removed and why (recommended)"
- secuura-demo-admin-mfa (2026-09-07T07:38): "later: Leave MFA off for now, revisit after the suites run (recommended)"
- secuura-891-workflow-scope-merge (2026-09-07T18:56): "kam-merges: You merge #891 yourself - one click (Recommended)"
- secuura-force-push-own-branch-standing (2026-09-07T18:56): "narrow-allow: Allow it on an agent's OWN unshared branch, under exactly those checks (your 18"
- secuura-org-trust-boundary-within-tenant (2026-09-07T19:01): "bind: Bind the issuer to the actor - 403 on a mismatch, exactly as onBehalfOf already does (Recommended)"
- secuura-archive-fifteen-platform-s-tickets (2026-09-08T10:35): "archive: Archive them too — read the 10"
- secuura-advisory-gate-moving-set (2026-09-09T08:12): "both: Both — delegate now, build the grace window next"
- secuura-advisories-high-and-prod-reaching (2026-09-09T10:30): "measure-first: Measure the nodemailer exposure first, then decide the two together"
- secuura-four-advisories-ruled-after-measurement (2026-09-09T10:30): "bump: Bump the pins instead of accepting them - removes the vulnerable code rather than recording a decision to live with it (Recommended)"
- secuura-required-approvals-zero-after-the-untick (2026-09-10T10:38): "raise-to-1: Raise required approving reviews from 0 to 1 on the require-pr-gates ruleset"
- secuura-ks998-format-gate-fails-open-on-missing-deps (2026-09-16T09:54): "a: Hard fail ONLY when a tracked file under that package is in the push (the ticket's middle option)"
- secuura-ks1011-stack-marker-unknown-on-restore (2026-09-16T09:54): "b: start-secuura.sh only WARNS (loud, named) when it finds unknown markers and prints the recreate command for the operator"
- secuura-ks1081-two-env-templates-which-is-canonical (2026-09-16T09:54): "a: env.example (the larger, the one CLAUDE.md documents) is canonical"
- secuura-ks1168-ilike-search-on-encrypted-pii (2026-09-16T09:54): "a: EXACT-only search"
- secuura-ks1194-1032-round2-merge-tap (2026-09-18T09:31): "merge: Merge now"
Kam's panel words, carried from Seat B 5th's brief:
- 2026-09-18 10:27, panel, verbatim: *"deploy to kintsugi. this is the dev server so it should be the first to update. the other server should only have proven deploys."*
- 2026-09-18 14:14, panel, verbatim: *"I'm going to be away for the next two days, so please keep going with tickets and activity while I'm away. Push merge and deploy whatever is ready. Whenever it's ready."* Wednesday read this back to Kam as kintsugi only, not demo, with the signature classes still pausing. Kam acknowledged at 14:16 with no correction. The WEEK-INSTRUCTION is live to the end of Sun 2026-09-20. Under it, merge only on Wednesday's signed GO naming the head, after the gate.
- 2026-09-18 09:22, panel: minimise gate duplication; batch file-disjoint changes into one gate.

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- 2026-09-19: Refs + contributes, never Closes, no closing phrase. One batch gate. Merges go one at a time, sha-pinned, each re-predicted over the then-current develop.
- 2026-09-19 (Seat B 2nd): no repo writes anywhere inside a push window. Any diff line you cannot attribute to your own action is a STOP.
- 2026-09-19 (the #1050-#1060 gate): locate tampers by a scope anchor + `from` text, never by line number.
- 2026-09-19 00:16Z (D2, Seat B 3rd): archived tickets are never reopened. No archived key goes in a branch, title or commit magic word. **Archived tickets get no `Refs`:** for this seat that means KS-1062 and KS-739 (Wednesday's rule for this round, and merge6's).
- 2026-09-19 (D8, for this round): KS-1269, KS-1258, KS-1230 and KS-1206 keep their current state after merge. All four read In Progress at 20:15 AEST; read and report each again in your plan. **KS-1238 stays Backlog** (not Done, not archived). If the bot walks it on PR-open, return it to Backlog after the last merge and verify the state. KS-1062 and KS-739 are untouched. KS-1215 and KS-1248 are prose only and untouched.
- 2026-09-19 08:52Z (the #1077-#1083 GO, dispositions): NOT-PINNED rows go to the local model and NO tickets are filed for them. This batch carries five of those rows (N77-1, N79-2, N80-1, N81-1, N82-1) plus two of KS-1238's own scope (N83-3, N83-5), all come back through the local model. N83-2..N83-6 stay KS-1238's scope, in its comment `18580369`.
- 2026-09-19 02:41Z / 05:28Z / 08:52Z: rule-7 handovers to Peter/Stuart are test blocks, **facts only**.
- 2026-09-19 (today's leak): **clear any `login_stub.mjs` listeners you start, by exact path, after EVERY shell-suite run**, and record the count cleared. Never kill a listener you did not start.
- Auth product edits are Kam's; KS-1238 here is test-only. Nothing goes to demo. This seat deploys nothing.

PROVENANCE:
- origin develop = ba1210afcab7ddf127cccb270b1c341360261cee, tree 993718b84caa4478989a301331d53740991e6b79 (= #1083's squash, and the tree Seat B 5th predicted) | git -C /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files ls-remote origin refs/heads/develop + rev-parse ba1210afc^{tree}, run 20:13:45 AEST (10:13:45Z), YOUR checkout, read-only | read 2026-09-19
- the nine canonical patches exist, each at `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-19_<run>/out.md.checker/patch.diff`. Runs and sha256: ks1269-ornith35b-night3 c7f34ae103a8, ks1269-ornith35b-night4 885987c3b5cd, ks1206-ornith35b-night4 81095581702a, ks739-ornith35b-night6 44253ae07f7e, ks1230-ornith35b-night4 eb5f367f1cbb, ks1062-ornith35b-night3 ad178aa105ea, ks1238-ornith35b-night4 cb5a055a9c29, ks1238-ornith35b-night5 d90130d83c38, ks1258-ornith35b-night4 9e85922f4810. Each touches exactly one file under `__tests__/`, and 8 distinct files in total. Only N83-3 has `-` lines (2) | ls + shasum + grep on each, run 20:13 AEST, my project | read 2026-09-19
- apply-check at ba1210afc: all nine pass `git apply --cached --check` strict, and each reverse control (`-R --check`) is refused. N71-1+N71-2 give the same tree in both orders (e9fc521fbfb72dab46b751ee215e76268efffab7). All nine together give tree f76901ed9cfae15ce6580ff24ebcbbea22bd36fb (8 files, +78/-2). Single-PR trees over develop: N71 pair e9fc521fb, N77-1 b904e7243, N80-1 8f3df5a64, N81-1 6c3dfead8, N79-2 56a40abab, N82-1 bab87a37e, N83-3 95ecc81a8, N83-5 4a4802bb7 | a `git clone --shared` of YOUR checkout into Wednesday's session scratchpad, write verbs there only, with a temporary GIT_INDEX_FILE, run 20:14 AEST | read 2026-09-19
- the vc-issuer ks1269 test blob bb8801cfb463 and status.ts 394337283ec1 are equal at f9c28a8b8 and ba1210afc. `git diff --stat f9c28a8b8 ba1210afc` has 8 files, 0 under vc-issuer | git -C YOUR checkout rev-parse / diff --stat, read-only, run 20:14 AEST | read 2026-09-19
- tamper `from` counts at develop: NULLPASSES-R/U's `from` sits at status.ts :231 and :300, and each comment+`from` anchor matches once; the N71-2 block `from`s match once each; C576_*'s `from` sits at system-status.ts :576 and :592, and the `.filter(s => s.required && …)` block anchor matches once; TENANTS*'s `from` occurs 13 times in platform.ts, the route line twice (GET :220, POST :237), and the router.post 4-line anchor once; RAW521, INF/WSNUMSTR/NEGZERO, NOJSON400/503, NULLPAIRMID/LASTOF3NULL and SKIPSETONE/SKIPBREAKS each occur once. Plant shas come from each run's `tamper_*.plant.out` | input.json tampers + git show ba1210afc:<file>, read-only, run 20:14-20:16 AEST | read 2026-09-19
- the nine READY files, their canonical-patch headers, tips (N71-1/N71-2 at f9c28a8b8, the other seven at ba1210afc), declared red sets, and raise notes (Refs / NO Refs / tier) | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_{KS-1269-N71-1,KS-1269-N71-2,KS-1206-N81-1,KS-739-N82-1,KS-1230-N80-1,KS-1062-N79-2,KS-1238-N83-3,KS-1238-N83-5,KS-1258-N77-1}_*_2026-09-19.diff.md, held by Wednesday 16:54-20:12 AEST, and each run's input.json, my project | read 2026-09-19
- Linear reads, 10:15:49Z: KS-1269 In Progress High on kamil.kreiser@secuura.ai, 1 attachment, last comment 2026-09-19T05:32Z, branchName has no foreign key; KS-1206 In Progress Low, same assignee, last comment 2026-09-19T02:49Z, branchName clean; KS-1230 In Progress Medium, same assignee, last comment 2026-09-18T07:00Z, branchName clean; KS-1258 In Progress Low, same assignee, last comment 2026-09-18T06:59Z, branchName clean; KS-1238 Backlog Medium, unassigned, last comment 2026-09-19T08:57Z, branchName carries `ks-1215`; KS-1215 In Progress High, live; KS-1248 In Progress Medium, unassigned; KS-1279 and KS-1280 Backlog, 0 comments | Secuura Linear GraphQL, a read-only query run by Wednesday's drafter with the key from /Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env (your tree), sourced transiently and never copied | read 2026-09-19
- KS-1062 Done ARCHIVED 2026-09-13T05:35:48Z (1 attachment, last comment 2026-09-13T05:35Z); KS-739 Done ARCHIVED 2026-09-14T08:33:49Z (1 attachment, last comment 2026-09-14T08:33Z); KS-662 Done ARCHIVED 2026-08-29T00:21Z | same query, issue by identifier, archived included, 10:15:49Z | read 2026-09-19
- KS-485 Todo High, KS-772 Todo High, last comments 2026-09-19T08:57Z (Seat B 5th's rule-7). KS-485's comment read hit the 50-row page cap, so that "last" is not proven to be the newest | same query, 10:15:49Z | read 2026-09-19
- Seat B 5th's final state, its method scripts (`raise/*6.*`, `boot/measure6.py`), its slip, and the ruleset note | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatB-5th-successor-2026-09-19.md, the history.md top entry, and `2026-09-19_seatB-5th/mail/06-wrap.txt` + `raise/` listing, read 20:1x AEST | read 2026-09-19
- the #1077-#1083 GO: the dispositions (N77-1/N79-2/N80-1/N81-1/N82-1 to the local model, no tickets; N83-2..N83-6 are KS-1238's scope), KS-1238 NOT-COMPLETE → Backlog, and the facts comment's list of open items | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-19_seatB-5th/mail/in-GO-085228.json, read 20:1x AEST | read 2026-09-19
- the 23 undelivered Secuura/Blockchain cards (22 with the secuura- prefix, excluding the Platform_S one, plus ks661-vocab) | bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh list ruled --undelivered [secuura-], run 20:15:24 AEST, my project | read 2026-09-19
- the WEEK-INSTRUCTION, status live, valid_until 2026-09-20 | /Volumes/DevMASTER/WEDNESDAY/0_Brain/tasks/WEEK-INSTRUCTION.md, read 20:1x AEST, my project | read 2026-09-19
- the TESTED grant and the merge-authority sentence | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/CLAUDE.md lines 233-238, sed run 20:1x AEST | read 2026-09-19

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-19 20:20
- Nine fixes, eight PRs, eight distinct test files, zero product bytes. The KS-1269 N71 pair is the only grouped item. KS-1238 has two PRs because its patches touch two files. The count appears as eight PRs in the BLUF, the QUEUE and the READY section.
- KS-1062 and KS-739 have no Refs wherever they appear (QUEUE items 5 and 6, the Wednesday rulings). Every other item carries Refs and never Closes.
- The tips are stated once: two items at f9c28a8b8 and seven at ba1210afc, each measured by the seat.
- PRs 7 and 8 (KS-1238) are tier 1, test-only and pushed last, and KS-1238 stays Backlog. The others are tier 2.
- -1 appears only as NON-RULED / pin nothing. KS-1258's old deny-list cell is kept (N77-2/N68-3 open).
- KS-1280, KS-1279, KS-730, KS-1250, KS-692, N83-2 and N83-6 appear only as not-in-this-batch. Demo and kintsugi appear only as not-yours.
- KS-1215, KS-1248 and KS-662 are prose-only and untouched. The KS-1215 trap is named for both the branchName and the ks1215 file name.
