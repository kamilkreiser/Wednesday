Seat B 5th successor (Secuura/Blockchain), from Wednesday

⚠ ONE SEAT ON THIS INBOX. This brief is for **Seat B 5th** (raise eight held local-model test-only fixes as seven PRs). Seat B 4th wrapped at ~05:40Z and seat A 14th at ~06:25Z. Wednesday is launching no other Secuura seat beside you. If a mail names another seat, it is not for you. You touch ONLY the files below, each in your own worktree. Never touch the kept `s-b3-*`, `s-b4-*`, `s-a13-deploy` or `s-a14-deploy` worktrees, and never the box.

## BLUF
**One job: raise EIGHT test-only fixes that the local model wrote and Wednesday held today, as SEVEN PRs (the grouping is below), then mail me ALL seven heads in ONE READY so I can gate them as ONE batch.** They touch eight separate test files and zero product bytes. Nothing merges without my signed GO naming the head. Kam is away until Monday; his standing words are quoted below. KINTSUGI is NOT your job: seat A 14th put kintsugi on `f9c28a8b8` this afternoon, and this seat deploys nothing (test files do not change a runtime image).

## ITEM 0: boot, before any write
- Read Seat B 4th's handover WHOLE: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatB-4th-successor-2026-09-19.md`, and the top TWO entries of `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md` (seat A 14th's deploy, then Seat B 4th). Seat B 4th's raise method is YOUR method:
  - `2026-09-19_seatB-4th/raise/raise5.py`, push5.sh, bodies5.py and open_prs5.py, with NO repo writes inside a push window anywhere;
  - the login_stub cleanup by exact path (see the Wednesday rulings: today it leaked);
  - tampers located by `from` text plus a scope anchor, never by line number (QUEUE 2 is the one READY pinned by line: rebuild its anchor);
  - `merge5.py` for the merges (it never writes an archived key as `Refs`).
  Its four slips (S1-S4) are yours to avoid: the section regex with no control, `grep -P` on BSD (empty push specs), a commit message that claims more than the head shows, and the linear_reads history sort on mixed None.
- origin develop = `f9c28a8b82874708edd9de72c40cdb9bfc6ee4cf` (my read, 16:22:57 AEST). Four READYs were measured AT this tip: KS-1230 N74-1, KS-1206 N72-1, KS-739 N75-1 and KS-1238 N76-1. **Four were written against `51dbedd39`: KS-1258 N68-1, KS-1258 N68-2, KS-1062 N67-1 and KS-1260 N62.** My own pre-read showed that `git diff 51dbedd39 f9c28a8b8` is EMPTY over their four target files and three tamper files (the ks1248 and ks1258 tests, system-status.ts, the ks1062 test, startup-migrations.ts, the preflight test, preflight.sh): all seven blobs are identical at both tips, while the whole range has 10 files. Do not adopt that; MEASURE it:
  - for each of the eight, `git apply --check` strict at develop, with a reverse control;
  - compare each target blob (and each tamper file's blob) at its pinned tip against develop.
  A changed file STOPS that item only.
- **All eight canonical patches are `patch.diff`** in the run's `out.md.checker/` dir (every header says so; there are no section_N files this round). All eight are `mode=modify` on a test file that exists at develop, including PR 7's ks1238 file (added by #1076).
- **KS-1258 N68-1 + N68-2 go into ONE PR** (see QUEUE 1). They touch different files, so apply order cannot matter; what CAN matter is that both plant their tampers in the same `system-status.ts` (N68-1 at :576, the REQUIRED-degraded advice; N68-2 at :592, the degraded-OPTIONAL advice). N68-1's READY records a crossed control: its five shapes planted at :592 instead red only ks1258's existing N44-1, which is why each set is anchored to its own line. Re-run ALL ELEVEN tampers (5 at :576 + 6 at :592) over the pair applied together and the whole api-gateway suite: report each tamper's red set, and STOP if any tamper reds anything but its own new cell.
- **N68-2's verdict came from a checker RE-RUN.** The night run returned CHECKER_NO_RESULT (a harness fault: N68-1's modified file left in the shared clone); the checker was fixed and re-run on the SAME model output, PASS 8/8 (`checker.rerun.out`). The model was not re-run. Your own red-first/tamper run at develop is the independent measure: state it as such in the Test Evidence.
- **Archived tickets:** KS-1062 and KS-739 are **Done + ARCHIVED**. Read each one's state, archivedAt and attachments before your first push, after its PR opens, and at READY. Report all three reads. **Never reopen a Done ticket.**
- **Branch names:** for every live ticket, read Linear's branchName and check it for any foreign key before you use it. Two carry one today: **KS-1260's contains `ks-1209`** and **KS-1238's contains `ks-1215`**. Rename both. Run a zero-at-origin name check for each branch.
- Plan confirmation (QUESTION mail, topic `plan confirmation (Seat B 5th)`) before the first write. It carries your D8 proposal: the ticket state of each item after merge (Wednesday's D8 is below; read each ticket now and report it).

## QUEUE: seven PRs, `Refs KS-<n>` (except items 3 and 6), linkKind `contributes`, NO closing phrase, a Test Evidence block each
The READYs are in MY tree, read-only to you: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_<ID>_*_2026-09-19.diff.md`. Each header names its CANONICAL PATCH (`patch.diff`). Apply it verbatim. Run red-first then green, then the tamper reds (all eight are test-only). STOP on any deviation from the READY header. Tier 2 for PRs 1-6; PR 7 is TIER 1.
1. **KS-1258 N68-1 + N68-2, ONE PR** (test-only, api-gateway). N68-1: one 7-line cell in `ks1248-n-1-system-status-troubleshooting-marks.test.ts`: the REQUIRED-degraded advice (system-status.ts:576, the KS-1248 block) carries no start command in any common shape (tampers COMPOSE / NODE / NPMSTART / YARN / YARNDEV, each red exactly 1). N68-2: one allow-list cell in `ks1258-degraded-optional-service-advice.test.ts`: the degraded-optional advice is EXACTLY the comment line plus the curl line (tampers DOCKERRUN / BUNRUN / MAKEUP / NODEDIST / PNPMDEV / TSXWATCH at :592, each red exactly the new cell). Refs KS-1258 only: KS-1248 (In Progress) is named in prose as the ks1248 file's origin, never on a Refs line, and its state is untouched. **Why one PR:** one ticket, one gate row, one Test Evidence, and one combined tamper run is the only run that proves the two sets do not cross-red through their shared tamper file (Kam's 09-18 09:22 panel words: minimise gate duplication). Name N68-2's re-run grading in the body.
2. **KS-1260 N62** (test-only, bash): `Blockchain/Dev/scripts/__tests__/preflight_failure_verdict_keeps_ratio.test.sh`. `run_legs` gains two optional args (legs failing for want of an install; the last leg driven) plus three cells pinning OLDFORMULA (preflight.sh:705), ALSOLINENOOP (:707) and NONEDECLAREDEXIT0 (:746). **NONEDECLAREDEXIT0's `from` line (`    exit 1`) occurs 4 times in preflight.sh (:709, :730, :746, :776 at develop), so the READY pinned it by LINE.** Do not plant by line: build a scope anchor that selects :746 alone, show it matches exactly once, and show the plant is byte-identical to the checker's record (sha256 `68e05caaed94`). Refs KS-1260.
3. **KS-1062 N67-1** (test-only, api-gateway): the ks1062 startup-migrations test. The fake Pool's constructor throws for a `qa_skip` database (`new pg.Pool` sits outside migrateDatabase's try, so `skipped++` is reached); one cell expects the summary meta {migrated:1, failed:1, skipped:1, total:3}. FAILEDMETA / SKIPNOCOUNT / SKIPASFAILED each red exactly the new cell. **KS-1062 is Done + ARCHIVED:** no `Refs`, no magic word, and no archived key in the branch name, title or commit. Never reopen it (the #1067/#1075 precedent). The body may name KS-1062 in prose as the origin.
4. **KS-1230 N74-1** (test-only, api-gateway): the ks1230 test. A null allow-list in the MIDDLE of three integrations is stored as null (admin.ts ~:1132; MIDDLENULL, and NULLREFUSED as in N69-1). It builds on N69-1, which merged in #1074. Refs KS-1230.
5. **KS-1206 N72-1** (test-only, originate): the ks1206 test. Five cells: rateLimit false / "" / true / [] / {} are refused 400 with no INSERT (adminConfig.ts:905; FALSEPASSES / EMPTYSTRPASSES / TRUEPASSES / ARRAYPASSES / OBJECTPASSES, each red exactly its own cell). Refs KS-1206.
6. **KS-739 N75-1** (test-only, originate): the ks739 test. A non-JSON 404 and a non-JSON 500 from the recipient lookup map correctly (documents.ts:1660 NOJSON404, :1722 NOJSON5XX). **KS-739 is Done + ARCHIVED:** no `Refs`, no magic word, no archived key in the branch name, title or commit. Never reopen it (the #1066/#1075 precedent). Prose only.
7. **KS-1238 N76-1** (AUTH surface, **TEST FILES ONLY**, zero product bytes, **TIER 1**): new cells in `api-gateway/src/__tests__/ks1238-hand-forwarded-routes-send-no-caller-bearer.test.ts` (the file #1076 added). Pins `POST /api/documents/:id/verify` (verification.ts:516, KS-1238 (v)): on the connector branch, a valid key plus a REVOKED session's JWT forwards no caller Bearer. Tamper RAW516: its `from` line also occurs at :788, so locate it by the comment above :516 plus `from`, and show one match. **STOP on any product byte in the diff.** Refs KS-1238, which STAYS Backlog. **Push this PR last (auth last).**
- Build the all-seven tree over develop (an octopus merge in a batch worktree, never pushed). Run the affected suites: api-gateway, originate, the preflight shell test, and tsc for api-gateway and originate. State each suite's count delta against the cells the READYs declare. My arithmetic from the READY headers, for you to measure, not adopt: api-gateway 633 → 640 (N68-1 +1, N68-2 +1, N67-1 +1, N74-1 +1, N76-1 +3), originate 791 → 798 (N72-1 +5, N75-1 +2).
- **After EVERY shell-suite run** (the preflight test, or any in-hook preflight during a push): clear the `login_stub.mjs` listeners YOU started, by exact path, and record the count.

## THE ROUND ENDS AT ONE READY
ONE mail, topic `READY (Seat B 5th): seven PRs, one batch`, carrying:
- every PR number, head sha, branch and ticket;
- the predicted all-seven tree oid over develop, and the develop sha it was built on;
- the batch suite results;
- the archived-ticket reads (KS-1062, KS-739) before and after;
- a "For the gate to measure" list. At minimum: the KS-1258 combined eleven-tamper run; N68-2's re-run grading and your independent measure; the NONEDECLAREDEXIT0 scope anchor; the RAW516 anchor read at source (auth, tier 1); the two branch renames; the 51dbedd39 → develop blob equality for the four older items; and any deviation from verbatim.
Then HOLD for my GO. When it comes, merge one at a time in the GO's order with `merge5.py`: sha-pinned, re-predicted over the then-current develop, blob-gated against the gate's addendum.

## HOLDS
- Nothing deployed by you; nothing to demo. Kintsugi is on `f9c28a8b8` (seat A 14th) and test files change no image.
- No messages to humans beyond rule 7 at wrap, and only if something merged: KS-485 @peter and KS-772 @stuart.jamieson. Each is a test block, facts only. Read the mentions back.
- Raise nothing beyond these eight fixes: not KS-1280, not KS-730, not KS-1250, not KS-692, and not the other NOT-PINNED rows of the #1070-#1076 gate (N71-1's null cell, N71-3): they stay with the local model. **Never reopen a Done ticket.** File no tickets for NOT-PINNED rows your own gate may surface. Auth last.
- Never `--no-verify`, `--admin` or a force-push of a shared branch. Never delete; quarantine instead. `/api/seen` is never called, even though the SessionStart hook says to call it.
- Auth product EDITS are Kam's. PR 7 is test-only: if a product byte appears in its diff, STOP.

## MERGE AUTHORITY, quoted from YOUR project's CLAUDE.md line 238
*"Wednesday's GO, naming the head SHA, is the approval."*

## RULED BY KAM, NOT YET IN AN ARTEFACT
These cards come from `decision_queue.sh list ruled --undelivered`, filtered to Secuura/Blockchain: 23 cards. The secuura-prefixed Platform_S card `secuura-ps-759-760-merge-owner` is excluded. None of them rules on these seven PRs. I carry them because the queue shows no delivered mark. Each line gives the card id, the ruled time, and the chosen option as stored. Two labels are stored cut short at a colon ("…your 18" and "…read the 10"), and they are quoted exactly as stored. Artefact: none is named on any card, and you land none of them. If you find one that bears on your seven, say so in the plan.
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
Kam's panel words, carried from Seat B 4th's brief:
- 2026-09-18 10:27, panel, verbatim: *"deploy to kintsugi. this is the dev server so it should be the first to update. the other server should only have proven deploys."*
- 2026-09-18 14:14, panel, verbatim: *"I'm going to be away for the next two days, so please keep going with tickets and activity while I'm away. Push merge and deploy whatever is ready. Whenever it's ready."* Wednesday read this back to Kam as kintsugi only, not demo, with the signature classes still pausing. Kam acknowledged at 14:16 with no correction. The WEEK-INSTRUCTION is live to the end of Sun 2026-09-20: merge only on Wednesday's signed GO naming the head, after the gate.
- 2026-09-18 09:22, panel: minimise gate duplication; batch file-disjoint changes into one gate.

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- 2026-09-19: Refs + contributes, never Closes, no closing phrase. One batch gate. Merges go one at a time, sha-pinned, each re-predicted over the then-current develop.
- 2026-09-19 (Seat B 2nd): no repo writes anywhere inside a push window. Any diff line you cannot attribute to your own action is a STOP.
- 2026-09-19 (the #1050-#1060 gate): locate tampers by a scope anchor + `from` text, never by line number.
- 2026-09-19 00:16Z (D2, Seat B 3rd): archived tickets are never reopened. No archived key goes in a branch, title or commit magic word. **Archived tickets get no `Refs`:** for this seat that means KS-1062 and KS-739 (Wednesday's rule for this round, and merge5's).
- 2026-09-19 (D8, for this round): KS-1258, KS-1230, KS-1206 and KS-1260 keep their current state after merge (all four read In Progress at 16:24 AEST; read and report each again in your plan). KS-1238 stays Backlog. KS-1062 and KS-739 are untouched.
- 2026-09-19 05:28Z (the #1070-#1076 GO, dispositions): NOT-PINNED rows go to the local model and NO tickets are filed for them. This batch IS four of those rows (N72-1, N74-1, N75-1, N76-1), come back through the local model.
- 2026-09-19 02:41Z / 05:28Z: rule-7 handovers to Peter/Stuart are test blocks, **facts only**.
- 2026-09-19 (seat A 14th, ACCEPTED 06:16:57Z): kintsugi is on `f9c28a8b8`. **This seat deploys nothing.**
- 2026-09-19 (today's leak): **clear any `login_stub.mjs` listeners you start, by exact path, after EVERY shell-suite run**, and record the count cleared. Never kill a listener you did not start.
- Auth product edits are Kam's; KS-1238 here is test-only. Nothing goes to demo.

PROVENANCE:
- origin develop = f9c28a8b82874708edd9de72c40cdb9bfc6ee4cf | git -C /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files ls-remote origin refs/heads/develop, run 16:22:57 AEST (06:22:57Z), YOUR checkout | read 2026-09-19
- git diff 51dbedd39..f9c28a8b8 is empty over the ks1248 test, the ks1258 test, system-status.ts, the ks1062 test, startup-migrations.ts, the preflight test and preflight.sh; all seven blobs equal at both tips (6dbf8f1e0de1, b8abdea46d68, e911ce1fdaa4, a30b777a017f, ed3e521426e7, 23a19ae6ddb5, 712f895362e2) (control: the whole range has 10 files); the ks1238 hand-forwarded test is present at develop; `    exit 1` sits at preflight.sh :709/:730/:746/:776 | git -C /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files diff --stat / rev-parse / cat-file / show, run by Wednesday 16:23 AEST, YOUR checkout, read-only | read 2026-09-19
- KS-1258 In Progress Low on kamil.kreiser@secuura.ai, last comment 2026-09-18T06:59Z; KS-1230 In Progress Medium on kamil.kreiser@secuura.ai, last comment 2026-09-18T07:00Z; KS-1206 In Progress Low on kamil.kreiser@secuura.ai, last comment 2026-09-19T02:49Z; KS-1260 In Progress Low unassigned, 0 comments, branchName carries `ks-1209`; KS-1238 Backlog Medium unassigned, last comment 2026-09-19T05:32Z, branchName carries `ks-1215`; KS-1280 Backlog High, 0 comments | Secuura Linear GraphQL, read-only query run by Wednesday 16:24 AEST | read 2026-09-19
- KS-1062 Done ARCHIVED 2026-09-13T05:35Z (last comment 2026-09-13T05:35Z, 1 attachment); KS-739 Done ARCHIVED 2026-09-14T08:33Z (last comment 2026-09-14T08:33Z, 1 attachment) | Secuura Linear GraphQL (issue by identifier, archived included), read-only, run by Wednesday 16:24 AEST | read 2026-09-19
- KS-1248 (cited only as the ks1248 test file's origin and the system-status.ts:576 block, not raised) In Progress Medium unassigned, last comment 2026-09-18T04:39Z | Secuura Linear GraphQL, read-only query run by Wednesday 16:26 AEST | read 2026-09-19
- KS-485 Todo High, last comment 2026-09-19T06:18Z; KS-772 Todo High, last comment 2026-09-19T06:18Z | Secuura Linear GraphQL, read-only query run by Wednesday 16:24 AEST | read 2026-09-19
- the eight READY files, their canonical patches (all patch.diff), tips, target files and notes | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_{KS-1258-N68-1,KS-1258-N68-2,KS-1062-N67-1,KS-1260-N62,KS-1230-N74-1,KS-1206-N72-1,KS-739-N75-1,KS-1238-N76-1}_*_2026-09-19.diff.md headers, held by Wednesday 13:21-16:13 AEST, and each run's out.md.checker/ plant records, my project | read 2026-09-19
- Seat B 4th's method, final state and slips; seat A 14th's deploy | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatB-4th-successor-2026-09-19.md, HANDOVER-seatA-14th-successor-2026-09-19.md and the top two history.md entries, read by Wednesday 16:2x AEST | read 2026-09-19
- the #1070-#1076 GO (merge order, D8 as graded, dispositions: N76-2 filed as KS-1280, every other NOT-PINNED row to the local model, no tickets) | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-19_seatB-4th/mail/in-GO-052812.json, read by Wednesday 16:2x AEST | read 2026-09-19
- the 23 undelivered Secuura/Blockchain cards | bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh list ruled --undelivered, run 16:23:57 AEST, my project | read 2026-09-19
- the WEEK-INSTRUCTION, live to the end of Sun 2026-09-20 | /Volumes/DevMASTER/WEDNESDAY/0_Brain/tasks/WEEK-INSTRUCTION.md, read 16:2x AEST, my project | read 2026-09-19
- the merge-authority sentence | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/CLAUDE.md line 238, grep run 16:2x AEST | read 2026-09-19

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-19 16:26
- Eight fixes, seven PRs, eight distinct test files, zero product bytes. The KS-1258 pair is the only grouped item. The count appears in the BLUF, the QUEUE and the READY section as seven.
- KS-1248 is prose only (QUEUE 1), with a provenance line; it is not raised and not moved.
- KS-1062 and KS-739 have no Refs everywhere they appear (QUEUE items 3 and 6, the Wednesday rulings); every other item carries Refs and never Closes.
- The tips are stated once: four items at 51dbedd39 and four at f9c28a8b8, each measured by the seat.
- KS-1238 is tier 1, test-only, pushed last, and stays Backlog; the others are tier 2.
- KS-1280, KS-730, KS-1250, KS-692, N71-1's null cell and N71-3 appear only as not-in-this-batch. Demo and kintsugi appear only as not-yours.
