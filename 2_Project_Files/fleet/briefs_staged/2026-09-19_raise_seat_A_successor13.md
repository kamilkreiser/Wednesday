Seat A 13th successor (Secuura/Blockchain), from Wednesday

## BLUF
**One job: a SCOPED kintsugi deploy that brings kintsugi from 59412d057 to develop as it stands (3c447abc7 or later): rebuild and swap ONLY the services whose images the new merges change.** Kintsugi only, never demo. **Measure the disk FIRST; if the scoped build does not fit with a safe margin, STOP and mail me the numbers. Delete nothing, prune nothing** (pruning old rollback sets is irreversible, and that call is Kam's). Kam is away Sat 19 + Sun 20; his words are quoted below. No merges, no PRs, no product code. You are the only Secuura seat live.

## ITEM 0: boot, before any write
- Read seat A 12th's handover WHOLE: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatA-12th-successor-2026-09-19.md`, and its runbook `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-19_seatA-12th/KINTSUGI-REBUILD-STATE.md` + `deploy/` (its phase scripts). Also read Seat B 2nd's handover `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatB-2nd-successor-2026-09-19.md` (what merged).
- **Derive the service set by MEASUREMENT, not from this brief:** `git diff --name-only 59412d057 <develop>` → map each changed path to the compose services whose build context contains it. My reading, UNMEASURED: originate (#1059 lifecycleActions.ts, #1060 documents.ts), anchoring (#1059 anchorSchema.ts), api-gateway (the regenerated OpenAPI yaml is bind-mounted or baked; the 12th found the yaml's host inode = container inode, so check whether a yaml change needs an image at all); #1050/#1051 are scripts (preflight, Testing job 04), which likely touch no running image. Put the measured set in your plan confirmation.
- Disk: `df` on the box. The 12th left 24 G free (81%); a FULL warm rebuild used ~19 G. Estimate the scoped build from the 12th's per-service image sizes. The 4000 MB guard stands.
- Plan confirmation (QUESTION mail, topic `plan confirmation`) before the first write to kintsugi.

## QUEUE
1. Phase 0: rollback tags for the SCOPED services only, stamp written LITERALLY `pre-20260919b` (the box clock is UTC; `pre-20260919` already exists; verify by name).
2. rsync (the 12th's method, no --delete; env/override untouched), build the scoped set serially under the disk guard, migrations only if the range adds any (it should add none: measure), then swap the scoped set with `-p dev --profile phase2 up -d --no-deps --force-recreate <svc>`. **Never `--remove-orphans`.** Rollback per service on a FAIL, then STOP.
3. **Verify by BEHAVIOUR:** in the running originate, the three new verbs (`note`, `certified`, `verified`) are accepted by the lifecycle-event path (a read-only probe or the in-container dist grep with a :pre-20260919b control) and `certify` is untouched; in the running anchoring, LIFECYCLE_VERBS carries them; /revoke's order (the dist carries the post-update record) vs the control image; /health/deep healthy; KS-535 wallet unchanged; demo-service's failure mode unchanged; every non-scoped container untouched (same image id, same StartedAt).
- SSH: the NSG admits `157.211.46.215/32` only. If SSH fails, STOP and mail your egress address. Do not touch the NSG.
- At wrap: rule-7 comments KS-485 @peter, KS-772 @stuart.jamieson, FACTS ONLY: what kintsugi now runs (sha), which services were swapped, demo unchanged. **No delivery or date wording about the flow verbs; any message to Stuart about them is Kam's.**

## HOLDS
- Nothing to demo. No merges, PRs or product code. KS-1250, KS-1175 are Kam's. KS-1256 is not fixed by this deploy; do not describe it so.
- Delete nothing, prune nothing (images, tags, files, worktrees). Never `--no-verify`, never force-push. Never enter `5_Project_History/quarantine/`. `/api/seen` is never called.
- No messages to humans beyond rule 7.

## RULED BY KAM, NOT YET IN AN ARTEFACT
- 2026-09-18 10:27, panel, verbatim: *"deploy to kintsugi. this is the dev server so it should be the first to update. the other server should only have proven deploys."*
- 2026-09-18 14:14, panel, verbatim: *"I'm going to be away for the next two days, so please keep going with tickets and activity while I'm away. Push merge and deploy whatever is ready. Whenever it's ready."* Wednesday's reading, acknowledged by Kam at 14:16 with no correction: kintsugi only, not demo; the signature classes still pause.

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- 2026-09-19 (the 12th's Q1): kintsugi's platform-settings key is absent, so nothing is written to it; that stands.
- 2026-09-19 (the 12th's wrap answer): rule-7 facts only, no flow-verb delivery or date wording.

## What Wednesday owes you
An answer to your plan confirmation and to anything you ask; a receipt for your STATUS mails.

PROVENANCE:
- origin develop = 3c447abc7714e98fbba596aa1045b7bb47a6d215 (all eleven merged) | git -C /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files ls-remote origin refs/heads/develop, run 09:28 AEST, YOUR checkout | read 2026-09-19
- kintsugi runs 59412d057; 24 G free (81%); a warm full rebuild ~19 G; rollback set pre-20260919 ×33 | seat A 12th's wrap mail (22:32:36Z, spf/dkim/dmarc pass) and /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatA-12th-successor-2026-09-19.md, YOUR project | read 2026-09-19
- KS-1172 In Progress P2 (last comment 2026-09-15T10:36Z); KS-1173 In Progress P2 (last comment 2026-09-15T10:36Z); KS-1264 In Progress P3 (0 comments); KS-485 Todo P2 (last comment 2026-09-18T23:26Z); KS-772 Todo P2 (last comment 2026-09-18T23:26Z); KS-1256 Backlog P2; KS-1250 Backlog P4; KS-1175 Backlog P2 | Secuura Linear GraphQL, read-only query run by Wednesday 09:30 AEST (8 of 8 returned) | read 2026-09-19
- KS-535 Done P2, ARCHIVED 2026-08-04T01:51Z (last comment 2026-08-02T00:44Z): named only as the standing rule (kintsugi never shares demo's wallet) to re-verify AFTER the swap, not as open work | Secuura Linear GraphQL (includeArchived), read-only query run by Wednesday 09:3x AEST | read 2026-09-19
- weekly usage 47%, under the 90% cap | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/usage_gate.sh --check, 08:1x AEST, my project | read 2026-09-19

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-19 09:30
- One job (a scoped deploy + verify); no merge, PR or code; the service set is to be MEASURED, my list marked unmeasured.
- Disk is measured first with a STOP path; nothing is pruned or deleted anywhere in the brief.
- Demo appears only under HOLDS; KS-1250/KS-1175/KS-1256 only as holds/awareness.
- Rule-7 wording forbids flow-verb delivery/date language, consistent with the 12th's ruling.
