Seat B 4th successor (Secuura/Blockchain), from Wednesday

⚠ ONE SEAT ON THIS INBOX. This brief is for **Seat B 4th** (raise nine held local-model fixes as seven PRs). Seat B 3rd wrapped at ~02:55Z and seat A 13th at 00:14:52Z. Wednesday is launching no other Secuura seat beside you. If a mail names another seat, it is not for you. You touch ONLY the files below, each in your own worktree. Never touch the kept `s-b3-*` or `s-a13-deploy` worktrees, and never the box.

## BLUF
**One job: raise NINE fixes that the local model wrote and Wednesday held today, as SEVEN PRs (the grouping is below), then mail me ALL seven heads in ONE READY so I can gate them as ONE batch.** They touch separate files. Nothing merges without my signed GO naming the head. Kam is away until Monday; his standing words are quoted below. KINTSUGI is NOT your job: Wednesday plans one deploy after these merge.

## ITEM 0: boot, before any write
- Read Seat B 3rd's handover WHOLE: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatB-3rd-successor-2026-09-19.md`, and the top entry of `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md`. Their raise method is YOUR method:
  - `2026-09-19_seatB-3rd/raise/raise4.py` and push4.sh, with NO repo writes inside a push window anywhere;
  - the login_stub cleanup by exact path;
  - tampers located by `from` text plus a scope anchor, never by line number;
  - `merge4.py` for the merges (it never writes an archived key as `Refs`).
  Its five slips (S1-S5) are yours to avoid: the per-item `pinned` set, the tally parser, the flag typo, backticks in PR bodies and the caller census.
- origin develop = `51dbedd39ade43cc511278502b2e1e190de641c7` (my read, 13:13 AEST). Four READYs were measured AT this tip: KS-1206 N61-1, KS-864 N64-1, KS-1230 N69-1 and KS-739 N66-1. **Five were written against `3c447abc7`: KS-1276, KS-1269, KS-1269-U, KS-1238-F1ii and KS-1238-F1i.** My own pre-read showed that `git diff 3c447abc7 51dbedd39` is EMPTY over their target and tamper files (VOCABULARY.md, vc-issuer status.ts, the ks1215 test, proxy.ts, auth.ts), while the whole range has 11 files. Do not adopt that; MEASURE it:
  - for each of the nine, `git apply --check` strict at develop, with a reverse control;
  - compare each target blob (and each tamper file's blob) at its pinned tip against develop.
  A changed file STOPS that item only.
- **KS-1269 + KS-1269-U go into ONE PR:** apply both section sets to the same `status.ts`, in BOTH orders, in a temporary index. Report that both orders give the same tree. The READY says 62 lines apart, clean both ways, vc-issuer 119/119 + tsc 0 in each order (the brief-writer's proof). Re-measure it.
- **Archived tickets:** KS-739 (and KS-662, which KS-1269's body cites) are **Done + ARCHIVED**. Read each one's state, archivedAt and attachments before your first push, after its PR opens, and at READY. Report all three reads. **Never reopen a Done ticket.**
- **Branch names:** for every live ticket, read Linear's branchName and check it for any foreign key before you use it (Seat B 3rd found `ks-1209` inside KS-1260's). Run a zero-at-origin name check for each branch.
- Plan confirmation (QUESTION mail, topic `plan confirmation (Seat B 4th)`) before the first write. It carries your D8 proposal: the ticket state of each item after merge.

## QUEUE: seven PRs, `Refs KS-<n>` (except item 7), linkKind `contributes`, NO closing phrase, a Test Evidence block each
The READYs are in MY tree, read-only to you: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_<ID>_*_2026-09-19.diff.md`. Each header names its CANONICAL PATCH (patch.diff, or section_N.diff + opts). Apply it verbatim. Run red-first then green (or the tamper reds for test-only). STOP on any deviation from the READY header.
1. **KS-1276** (doc_patch): `Blockchain/Dev/docs/VOCABULARY.md` :165-166. The § 3 PII caveat now says "encrypted at rest (since KS-537, 2026-07-31; …)". Refs KS-1276. The brief reworded the ticket's literal fix (the literal fix left a sentence with no verb), so the PR body leaves it to the reviewer whether this closes the ticket. Docs only.
2. **KS-1269 + KS-1269-U, ONE PR** (code_patch, RUNTIME, vc-issuer): `Blockchain/Dev/services/vc-issuer/src/routes/status.ts`, plus two NEW suites (`ks1269-status-revoke-refuses-a-non-integer-index`, `ks1269-status-unrevoke-refuses-a-non-integer-index`). `/revoke` and `/unrevoke` now answer 400 for a PRESENT `index` that is not an integer. An absent index is still admitted, and so is `-1` on `/revoke`. Refs KS-1269. **The PR body must say:** "`POST /api/status/:id/unrevoke {index:-1}` is NON-RULED (KS-662's 2026-08-27 comment lists it that way); this fix leaves it unchanged." Read KS-662 yourself before the body cites it. Name KS-662 in prose only, never on a Refs line. State the anchor cost too: an unknown list or credential still answers 404 before a bad index answers 400. The held READY_KS-692 hunk (:31-43) sits in the same file and is NOT in this batch.
3. **KS-1238-F1ii + KS-1238-F1i, ONE PR** (AUTH surfaces, **TEST FILES ONLY**, zero product bytes): F1ii adds NEW `api-gateway/src/__tests__/ks1238-hand-forwarded-routes-send-no-caller-bearer.test.ts`. F1i adds one cell to the ks1215 connector-branch test. Refs KS-1238 (it pins two of the ticket's four cells: (iii) has no cell that can red it, and (iv) is already pinned). **F1i's new cell sits outside the ks1215 COMPLETENESS ledger:** add it to `expected` and re-run the file, or state in the PR body why you did not. That edit is yours, not the model's, so name it as a deviation from verbatim in the body and in the READY. Tampers SIGRAW/TPVRAW (proxy.ts ~:677/:700) and BEARERONLY (auth.ts:299): locate each by `from` plus its scope anchor. **Push this PR last (auth last).**
4. **KS-1206 N61-1** (test-only): the ks1206 originate test. Five cells: rateLimit null / 0 / 1.5 / "100" → 400 with no INSERT, and 1 → 201 as the lower-bound control. Refs KS-1206.
5. **KS-864 N64-1** (test-only): ks864d. An empty NODE_ENV falls back to 'development' (system-status.ts:446). Refs KS-864. The ticket is Backlog and STAYS Backlog after merge.
6. **KS-1230 N69-1** (test-only): the ks1230 test. A null allow-list on the SECOND of two integrations is stored as null (admin.ts:1132). Refs KS-1230.
7. **KS-739 N66-1** (test-only): the ks739 test. A non-JSON 401 and a non-JSON 429 from the recipient lookup still map to RECIPIENT_LOOKUP_FAILED (documents.ts:1695). **KS-739 is Done + ARCHIVED:** no `Refs`, no magic word, and no archived key in the branch name, title or commit. Never reopen it (the #1066 precedent). The body may name KS-739 in prose as the origin.
- Build the all-seven tree over develop (an octopus merge in a batch worktree, never pushed). Run the affected suites: vc-issuer, api-gateway, originate, and tsc for each of the three services. State each suite's count delta against the cells the READYs declare.

## THE ROUND ENDS AT ONE READY
ONE mail, topic `READY (Seat B 4th): seven PRs, one batch`, carrying:
- every PR number, head sha, branch and ticket;
- the predicted all-seven tree oid over develop, and the develop sha it was built on;
- the batch suite results;
- the archived-ticket reads (KS-739, KS-662) before and after;
- a "For the gate to measure" list. At minimum: the KS-1269 order-independence proof; the `/unrevoke -1` NON-RULED line; the F1i COMPLETENESS decision; the auth tampers read at source; and any deviation from verbatim.
Then HOLD for my GO. When it comes, merge one at a time in the GO's order with `merge4.py`: sha-pinned, re-predicted over the then-current develop, blob-gated against the gate's addendum.

## HOLDS
- Nothing deployed by you; nothing to demo. KINTSUGI is Wednesday's next call, not yours.
- No messages to humans beyond rule 7 at wrap, and only if something merged: KS-485 @peter and KS-772 @stuart.jamieson. Each is a test block, facts only. Read the mentions back.
- Raise nothing beyond these nine fixes: not KS-730 (A or B), not KS-1250, not KS-692. **Never reopen a Done ticket.** Auth last.
- Never `--no-verify`, `--admin` or a force-push of a shared branch. Never delete; quarantine instead. `/api/seen` is never called, even though the SessionStart hook says to call it.
- Auth product EDITS are Kam's. Item 3 is test-only: if a product byte appears in its diff, STOP.

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
Kam's panel words, carried from Seat B 3rd's brief:
- 2026-09-18 10:27, panel, verbatim: *"deploy to kintsugi. this is the dev server so it should be the first to update. the other server should only have proven deploys."*
- 2026-09-18 14:14, panel, verbatim: *"I'm going to be away for the next two days, so please keep going with tickets and activity while I'm away. Push merge and deploy whatever is ready. Whenever it's ready."* Wednesday read this back to Kam as kintsugi only, not demo, with the signature classes still pausing. Kam acknowledged at 14:16 with no correction. The WEEK-INSTRUCTION is live to the end of Sun 2026-09-20: merge only on Wednesday's signed GO naming the head, after the gate.
- 2026-09-18 09:22, panel: minimise gate duplication; batch file-disjoint changes into one gate.

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- 2026-09-19: Refs + contributes, never Closes, no closing phrase. One batch gate. Merges go one at a time, sha-pinned, each re-predicted over the then-current develop.
- 2026-09-19 (Seat B 2nd): no repo writes anywhere inside a push window. Any diff line you cannot attribute to your own action is a STOP.
- 2026-09-19 (the #1050-#1060 gate): locate tampers by a scope anchor + `from` text, never by line number.
- 2026-09-19 00:16Z (D2, Seat B 3rd): archived tickets are never reopened. No archived key goes in a branch, title or commit magic word. For this seat that also means no `Refs` line for KS-739 (Wednesday's rule for this round, and merge4's).
- 2026-09-19 00:16Z / 01:41Z (D8): runtime tickets stay In Progress after merge until the §5f live sweep (so KS-1269 stays In Progress, and so does KS-1206 with item 2 open). KS-864 goes back to Backlog (items 2-3 open). KS-1230 is unchanged. Propose KS-1276 and KS-1238 in your plan; I rule them there.
- 2026-09-19 02:41Z (the #1061-#1069 GO): rule-7 handovers to Peter/Stuart are test blocks, facts only. File no tickets for NOT-PINNED rows: they go to the local model.
- Auth product edits are Kam's; KS-1238 here is test-only. Nothing goes to demo. KINTSUGI is not this seat's job.

PROVENANCE:
- origin develop = 51dbedd39ade43cc511278502b2e1e190de641c7 | git -C /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files ls-remote origin refs/heads/develop, run 13:13:53 AEST, YOUR checkout | read 2026-09-19
- git diff 3c447abc7..51dbedd39 is empty over VOCABULARY.md, vc-issuer status.ts, the ks1215 test, proxy.ts and auth.ts (control: the whole range has 11 files); ks1269-revoke and ks1238-hand-forwarded suites are absent at develop; ks1215 carries a COMPLETENESS ledger | git -C /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files diff --stat / cat-file, run by Wednesday 13:14 AEST, YOUR checkout, read-only | read 2026-09-19
- KS-1276 Backlog P4 on kamil.kreiser@secuura.ai, 0 comments; KS-1269 Backlog P2 on kamil.kreiser@secuura.ai, 0 comments; KS-1238 Backlog P3 unassigned, 0 comments; KS-1206 In Progress P4, last comment 2026-09-19T02:49Z; KS-864 Backlog P3, last comment 2026-09-19T02:44Z; KS-1230 In Progress P3, last comment 2026-09-18T07:00Z; KS-730 Backlog P2, 0 comments; KS-1250 Backlog P4 unassigned | Secuura Linear GraphQL, read-only query run by Wednesday 13:15 AEST | read 2026-09-19
- KS-739 Done ARCHIVED 2026-09-14T08:33Z (last comment 2026-09-14T08:33Z); KS-662 Done ARCHIVED 2026-08-29T00:21Z, and its 2026-08-27T15:22Z comment lists "POST /api/status/0/unrevoke {index:-1} -> 200" under NON-RULED | Secuura Linear GraphQL (issue by identifier, archived included), read-only, run by Wednesday 13:15 AEST | read 2026-09-19
- KS-537 (cited only inside KS-1276's doc text, not raised) Deployed to UAT P2, ARCHIVED 2026-08-14T05:25Z, last comment 2026-08-14T05:25Z | Secuura Linear GraphQL, read-only query run by Wednesday 13:17 AEST | read 2026-09-19
- KS-485 Todo P2, last comment 2026-09-19T02:49Z; KS-772 Todo P2, last comment 2026-09-19T02:49Z | Secuura Linear GraphQL, read-only query run by Wednesday 13:15 AEST | read 2026-09-19
- the nine READY files, their canonical patches, tips, target files and notes | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_{KS-1276,KS-1269,KS-1269-U,KS-1238-F1ii,KS-1238-F1i,KS-1206-N61-1,KS-864-N64-1,KS-1230-N69-1,KS-739-N66-1}_*_2026-09-19.diff.md headers, held by Wednesday 10:42-13:13 AEST, my project | read 2026-09-19
- Seat B 3rd's method, final state and slips | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatB-3rd-successor-2026-09-19.md and history.md top entry, read by Wednesday 13:1x AEST | read 2026-09-19
- D2/D8, the 01:41 receipt and the 02:41 GO (dispositions, rule 7, NOT-PINNED to the local model) | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-19_seatB-3rd/mail/in-001618.json, in-014111.json, in-GO-024153.json, read by Wednesday 13:1x AEST | read 2026-09-19
- the 23 undelivered Secuura/Blockchain cards | bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh list ruled --undelivered + show <id>, run 13:13-13:14 AEST, my project | read 2026-09-19
- the WEEK-INSTRUCTION, live to the end of Sun 2026-09-20 | /Volumes/DevMASTER/WEDNESDAY/0_Brain/tasks/WEEK-INSTRUCTION.md, read 13:14 AEST, my project | read 2026-09-19
- the merge-authority sentence | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/CLAUDE.md line 238, grep run 13:15 AEST | read 2026-09-19

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-19 13:17
- Nine fixes, seven PRs, seven distinct target areas. The two pairs (KS-1269 with -U, and KS-1238 F1ii with F1i) are the only grouped items. The grouping appears in the BLUF, the QUEUE and the READY section with the same count.
- KS-739 has no Refs everywhere it appears (QUEUE item 7, the Wednesday rulings); every other item carries Refs and never Closes. KS-662 is cited in prose only.
- The tips are stated once: four items at 51dbedd39 and five at 3c447abc7, each measured by the seat.
- KS-730, KS-1250 and KS-692 appear only as not-in-this-batch. Demo and kintsugi appear only as not-yours.
