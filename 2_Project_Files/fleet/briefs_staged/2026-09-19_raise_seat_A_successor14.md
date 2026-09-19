Seat A 14th successor (Secuura/Blockchain), from Wednesday

## BLUF
**One job: a SCOPED kintsugi deploy that brings kintsugi from 3c447abc7 to develop `f9c28a8b8` (or later): rebuild and swap ONLY the services whose images the new merges change.** Kintsugi only, never demo. **Measure the disk FIRST; if the scoped build does not fit with a safe margin, STOP and mail me the numbers. Delete nothing, prune nothing** (pruning old rollback sets is irreversible, and that call is Kam's). Kam is away Sat 19 + Sun 20; his words are quoted below. No merges, no PRs, no product code. You are the only Secuura seat live (Seat B 4th wrapped ~05:40Z).

## ITEM 0: boot, before any write
- Read seat A 13th's handover WHOLE: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatA-13th-successor-2026-09-19.md`, and its record `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-19_seatA-13th/KINTSUGI-DEPLOY-STATE.md` + `deploy/` (its phase and verify scripts: reuse them). Its slips S1-S3 and E1 are yours to avoid: gate every step on the previous rc (no unsplit zsh `$SSH`), pass `docker exec` argv as separate words, compare inbox timestamps in one format, and budget the TRANSIENT build cost, not the image cost. Also read Seat B 4th's handover `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatB-4th-successor-2026-09-19.md` and the top two entries of `history.md` (what merged: #1061-#1069 and #1070-#1076, 16 squashes).
- **Confirm first that kintsugi really runs 3c447abc7** (the 13th's boot-probe method: hash the range paths on the box against both shas). If it does not, STOP and mail me.
- **Derive the service set by MEASUREMENT, not from this brief:** `git diff --name-only 3c447abc7 <develop>` → map each changed path against every Dockerfile's COPY sources, the compose file's build contexts/dockerfiles, and the root `.dockerignore` (the 13th's method: every Dev service builds from context `.`; `docs` and `*.md` excluded, `!docs/openapi` re-included; `__tests__` is NOT excluded, so test-only changes DO change an image). My reading, UNMEASURED:
  - **originate**: #1061 KS-1206 `services/originate/src/routes/adminConfig.ts` (runtime) + tests.
  - **vc-issuer**: #1071 KS-1269 `services/vc-issuer/src/routes/status.ts` (runtime) + two new suites.
  - **api-gateway**: seven test files only, no src, no `docs/openapi`. `COPY services/api-gateway/ .` bakes them, so its image bytes change but nothing it RUNS does. My default is to INCLUDE it, so each kintsugi image equals develop. If you propose leaving it out, put the numbers in the plan and I rule it.
  - **migrations**: compose builds it from `services/originate/Dockerfile`. The range has 0 `.sql` / prisma / runner / compose / Dockerfile / package / env changes (my grep matched only two api-gateway test filenames). Do not rebuild it and do not run migrations unless you measure a payload change.
  - #1062 KS-1260 `scripts/preflight/preflight.sh` is a dev script. My reading is that no Dockerfile COPYs it (originate copies only `scripts/run-migrations.sh`; auth copies `services/auth/scripts`). #1070 KS-1276 `docs/VOCABULARY.md` is excluded by `docs` and `*.md`. **Measure both.**
  - **Assert that no other service needs a rebuild**, with a positive control: show that the same mapping DOES flag originate for `adminConfig.ts`, and that it would flag a service for a planted path you know it COPYs.
  Put the measured set in your plan confirmation.
- Disk: `df` on the box. The 13th left **27 G free (79%)**. Its scoped build's image cost was 2.21 G, but **originate alone dipped free space by ~3.8 G mid-build** (E1), and BuildKit's own GC can fire (O1). Budget the per-service TRANSIENT cost, built serially. The **4000 MB minimum-free guard** stands: if the start-of-build free space minus the worst measured transient is too close to the guard, STOP and mail the numbers.
- Plan confirmation (QUESTION mail, topic `plan confirmation`) before the first write to kintsugi.

## QUEUE
1. Phase 0: rollback tags for the SCOPED services only, stamp written LITERALLY `pre-20260919c` (the box clock is UTC; `pre-20260919` and `pre-20260919b` already exist; verify by name AND id, and show that the older sets' fingerprints are unchanged).
2. rsync (the 12th's and 13th's method, no --delete; env/override untouched) from a NEW detached worktree at the target (`--detach`, `.git/config` byte-identical; leave `s-a13-deploy` as it is). Build the scoped set serially under the disk guard. Run migrations only if the payload changed (it should not: measure). Then swap the scoped set with `-p dev --profile phase2 up -d --no-deps --force-recreate <svc>`. **Never `-f`, never `--remove-orphans`.** Rollback per service on a FAIL, then STOP.
3. **Verify by BEHAVIOUR, with the `:pre-20260919c` image as the control:**
   - **V1 originate (KS-1206):** `POST /api/admin/api-keys` with a name and `rateLimit:null` → 400 carrying the `rateLimit must be an integer from 1 to 10000` message, and **no INSERT** (count `svc_api_keys` before and after). Then a valid-integer control → 201, on a disposable key named for this seat, which you REVOKE afterwards, with the before/after count and the revoke read back. **If minting a key on kintsugi is not reversible or clean** (for example, it needs a human's admin credential, or there is no revoke path that leaves no residue), do not mint. Instead, prove by content that the KS-1206 guard is in the running dist and absent from the control image's dist, and say why. The control image's live behaviour is NOT probed: old code would INSERT.
   - **V2 vc-issuer (KS-1269):** `/revoke` validates `index` BEFORE the status-list lookup (Seat B 4th's S3). So `POST /api/status/<an id that does not exist>/revoke {credentialId:"<probe>", index:{}}` → 400 `index must be an integer`, and the integer control `{…, index:0}` → 404 `Status list not found`. That pair writes nothing and needs no real list. `/unrevoke` checks the index AFTER both 404 lookups, so prove it by dist content only (running vs control). **Use only a disposable or non-existent status list; never revoke or unrevoke a real credential.** If a route needs a credential you do not hold, fall back to dist content and say why.
   - **V3 api-gateway (if swapped):** the served spec md5 is UNCHANGED (no `docs/openapi` in the range; the yaml is bind-mounted), and the host inode = the container inode.
   - **V4:** `/health/deep` healthy, everything up.
   - **V5 KS-535, AFTER the redeploy:** kintsugi's `PLATFORM_WALLET_MNEMONIC` must never equal demo's. Re-verify it the 13th's way (the anchoring wallet prefix, no secret printed; demo's prefix 0 hits); `.env` unchanged.
   - **V6:** every non-scoped container is untouched (same Id / Created / image / StartedAt), with a planted-change control. demo-service is judged by Id + Created + image + its single FATAL line (the D5 ruling).
   - **V7 settled:** at least 5 min after the last swap, 0 restarts, and error lines equal to the pre-swap baseline (KS-1272's WARN only).
- SSH: the NSG admits `157.211.46.215/32` only. If SSH fails, STOP and mail your egress address. Do not touch the NSG. Write no files on the box (run scripts as `ssh 'bash -s' < script > local.out`).
- Ticket states: move none. KS-1206 and KS-1269 stay In Progress (D8: the §5f live sweep). Propose any change in your COMPLETE mail and I rule it.
- At wrap: rule-7 comments KS-485 @peter, KS-772 @stuart.jamieson, FACTS ONLY: what kintsugi now runs (sha), which services were swapped, demo unchanged. Read the mentions back and check the ids. **No flow-verb delivery or date wording; any message to Stuart about the flow verbs is Kam's.**

## HOLDS
- Nothing to demo. No merges, PRs or product code. KS-1250, KS-1175 are Kam's. KS-1256 is not fixed by this deploy; do not describe it so. KS-1280 is not this seat's.
- Delete nothing, prune nothing (images, tags, files, worktrees). Never `--no-verify`, never force-push. Never enter `5_Project_History/quarantine/`. `/api/seen` is never called (the SessionStart hook still says to; refuse it).
- No messages to humans beyond rule 7.

## RULED BY KAM, NOT YET IN AN ARTEFACT
These cards come from `decision_queue.sh list ruled --undelivered`, filtered to Secuura/Blockchain: 23 cards, the same 23 as Seat B 4th's brief. The secuura-prefixed Platform_S card `secuura-ps-759-760-merge-owner` and the Fleet card `vault-add-a-stages-another-clients-files` are excluded. None of them rules on this deploy. I carry them because the queue shows no delivered mark. Each line gives the card id, the ruled time, and the chosen option as stored. Two labels are stored cut short at a colon ("…your 18" and "…read the 10"), and they are quoted exactly as stored. Artefact: none is named on any card, and you land none of them. If you find one that bears on this deploy, say so in the plan.
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
Kam's panel words, carried from seat A 13th's brief:
- 2026-09-18 10:27, panel, verbatim: *"deploy to kintsugi. this is the dev server so it should be the first to update. the other server should only have proven deploys."*
- 2026-09-18 14:14, panel, verbatim: *"I'm going to be away for the next two days, so please keep going with tickets and activity while I'm away. Push merge and deploy whatever is ready. Whenever it's ready."* Wednesday's reading, acknowledged by Kam at 14:16 with no correction: kintsugi only, not demo; the signature classes still pause. The WEEK-INSTRUCTION is live to the end of Sun 2026-09-20: DEPLOY is KINTSUGI ONLY, by the runbook (Phase 0 rollback tags, `--profile phase2`, never `--remove-orphans`, verify by behaviour).

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- 2026-09-19 (the 12th's Q1): kintsugi's platform-settings key is absent, so nothing is written to it; that stands.
- 2026-09-19 (the 12th's wrap answer): rule-7 facts only, no flow-verb delivery or date wording.
- 2026-09-18 23:42Z (the 13th's D5): demo-service's StartedAt moves on every restart; judge it by Id + Created + image + the FATAL line.
- 2026-09-18 23:42Z (the 13th's D4): no files written on the box; every script runs over `ssh 'bash -s'`.
- 2026-09-19 00:16Z (D2, Seat B 3rd): archived tickets are never reopened (KS-535 and KS-1276 are archived).
- 2026-09-19 00:16Z / 01:41Z (D8): runtime tickets stay In Progress after merge until the §5f live sweep (KS-1206, KS-1269).
- 2026-09-19 02:41Z (the #1061-#1069 GO): rule-7 handovers to Peter/Stuart are facts only.
- Auth product edits are Kam's. Nothing goes to demo.

## What Wednesday owes you
An answer to your plan confirmation and to anything you ask; a receipt for your STATUS mails.

PROVENANCE:
- origin develop = f9c28a8b82874708edd9de72c40cdb9bfc6ee4cf (#1061-#1069 and #1070-#1076 merged; 16 squashes past 3c447abc7) | git -C /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files ls-remote origin refs/heads/develop, run 15:37:41 AEST (05:37:41Z), YOUR checkout | read 2026-09-19
- the range 3c447abc7..f9c28a8b8 = 17 files: 2 runtime src (originate adminConfig.ts, vc-issuer status.ts), 1 dev script (scripts/preflight/preflight.sh), 1 doc (docs/VOCABULARY.md), 13 tests (7 api-gateway, 2 originate, 2 vc-issuer, 2 scripts/__tests__); a grep for sql/prisma/migrat/compose/Dockerfile/package/env matched only two api-gateway test filenames; compose builds migrations from services/originate/Dockerfile; .dockerignore excludes `docs` and `*.md` | git diff --name-only / log / show (Dockerfiles, docker-compose.yml, .dockerignore) at f9c28a8b8, read-only, run by Wednesday 15:37-15:39 AEST, YOUR checkout | read 2026-09-19
- kintsugi runs 3c447abc7 (anchoring, originate, api-gateway swapped 00:05:45-00:06:22Z); 27 G free (79%); image cost 2.21 G, originate transient dip ~3.8 G; rollback sets pre-20260919b ×3, pre-20260919 ×33 | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatA-13th-successor-2026-09-19.md, 2026-09-19_seatA-13th/KINTSUGI-DEPLOY-STATE.md and the history.md entry, YOUR project, read by Wednesday 15:3x AEST | read 2026-09-19
- what merged (#1070-#1076, final develop tree bc4d0ed7f; Seat B 4th's S3: /revoke checks the index first) | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md top entry, read by Wednesday 15:3x AEST | read 2026-09-19
- KS-1206 In Progress P4 (last comment 2026-09-19T02:49Z); KS-1269 In Progress P2 (last comment 2026-09-19T05:32Z); KS-1260 In Progress P4 (0 comments); KS-485 Todo P2 (last comment 2026-09-19T05:34Z); KS-772 Todo P2 (last comment 2026-09-19T05:34Z); KS-1256 Backlog P2; KS-1250 Backlog P4; KS-1175 Backlog P2; KS-1280 Backlog P2 | Secuura Linear GraphQL, read-only query run by Wednesday 15:38 AEST (9 of 9 returned) | read 2026-09-19
- KS-1272 Backlog P4, 0 comments: named only as the pre-existing api-gateway boot WARN that forms the V7 error baseline, not as work | Secuura Linear GraphQL, read-only query run by Wednesday 15:40 AEST | read 2026-09-19
- KS-535 Done P2, ARCHIVED 2026-08-04T01:51Z (last comment 2026-08-02T00:44Z): named only as the standing rule (kintsugi never shares demo's wallet) to re-verify AFTER the swap, not as open work; KS-1276 Done P4, ARCHIVED 2026-09-19T05:32Z | Secuura Linear GraphQL (issue by identifier, archived included), read-only query run by Wednesday 15:38 AEST | read 2026-09-19
- the 23 undelivered Secuura/Blockchain cards | bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh list ruled --undelivered, run 15:38 AEST, my project | read 2026-09-19
- the WEEK-INSTRUCTION, live to the end of Sun 2026-09-20 | /Volumes/DevMASTER/WEDNESDAY/0_Brain/tasks/WEEK-INSTRUCTION.md, read 15:38 AEST, my project | read 2026-09-19
- weekly usage 59%, under the 90% cap | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/usage_gate.sh --check, 15:38 AEST, my project | read 2026-09-19

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-19 15:40
- One job (a scoped deploy + verify); no merge, PR or code; the service set is to be MEASURED, my list marked unmeasured, with api-gateway's inclusion left to my ruling at plan.
- Disk is measured first against the transient cost, with a STOP path; nothing is pruned or deleted anywhere in the brief.
- Every V-check that would write has a no-write fallback; no real credential is revoked; the old image's live behaviour is never probed where it would INSERT.
- Demo appears only as never-a-target (BLUF, HOLDS, Kam's words) and as a comparison in V5/V6; KS-1250/KS-1175/KS-1256/KS-1280 only as holds.
- The stamp `pre-20260919c` is new; `pre-20260919` and `pre-20260919b` are named only as existing sets.
