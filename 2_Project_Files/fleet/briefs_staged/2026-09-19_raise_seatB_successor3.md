Seat B 3rd successor (Secuura/Blockchain), from Wednesday

⚠ TWO SEATS SHARE THIS INBOX. This brief is for **Seat B 3rd** (raise nine held local-model fixes). **Seat A 13th** is live beside you, running a scoped kintsugi deploy; its mails name "seat A 13th", and they are not yours. Seat A writes NO code and merges nothing. You touch ONLY the files below, each in your own worktree, and never seat A's worktree `worktrees/s-a13-deploy` or anything on the box.

## BLUF
**One job: raise NINE fixes the local model wrote and Wednesday held today, one PR per item, then mail me ALL heads in ONE READY so I gate them as ONE batch.** They are file-disjoint. Nothing merges without my signed GO naming the head. Kam is away until Monday; his standing words are quoted below.

## ITEM 0: boot, before any write
- Read Seat B 2nd's handover WHOLE: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatB-2nd-successor-2026-09-19.md`. Its raise method (raise3.py; push_protocol with NO repo writes inside a push window, anywhere; the login_stub cleanup) is YOUR method. Its memory lines apply (the `$?`-after-substitution trap).
- develop at origin = `3c447abc7714e98fbba596aa1045b7bb47a6d215` (my read). The READYs were measured at three tips (`59412d057` for six, `3c447abc7` for KS-1258 N53-1, KS-1230 N54-1 and KS-1260). **For each item, confirm its target file is unchanged between its pinned tip and develop, and that its patch applies at develop.** A changed file STOPS that item only. KS-739 F1's TAMPER is in `routes/documents.ts`, which #1060 changed (its line moved by −12). Re-measure the tamper by its `from` text + a scope anchor at develop, not by the line number (the #1050-#1060 gate's rule).
- **The ARCHIVED-TICKET question (decide by measurement, then say which in your plan):** KS-991, KS-739 and KS-1062 are **Done and ARCHIVED** (13-14 Sep); these three PRs only PIN already-fixed behaviour. Seat B 2nd saw the branch-name automation move Backlog tickets to In Progress on the first push. **A Done ticket must NOT be reopened by a pin.** Default: name each of those three branches WITHOUT the archived ticket's key, and Refs the archived ticket in the body only. Or, if you measure that a body Refs also re-derives a state change, file ONE follow-up ticket "test pins for already-fixed behaviour (KS-991/KS-739/KS-1062)" after a board search and Refs that. Read each archived ticket's state before and after your first push, and report both.
- Plan confirmation (QUESTION mail, topic `plan confirmation (Seat B 3rd)`) before the first write.

## QUEUE: nine PRs, `Refs KS-<n>`, linkKind `contributes`, NO closing phrase, a Test Evidence block each
READYs are in MY tree, read-only to you: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_<ID>_*_2026-09-19.diff.md`. Each header names its CANONICAL PATCH (patch.diff, or section_N.diff + opts). Apply verbatim; red-first then green (or tamper-reds for test-only); STOP on a deviation from the READY header.
1. KS-1206 (code_patch, runtime): `services/originate/src/routes/adminConfig.ts` (+4) + a new test. **The gate must measure one question, so put it in the PR body:** null/0 `rateLimit` (formerly defaulted to 1000) now answers 400. Is any caller sending those? The held KS-730-B (09-17) edits the same file; it is NOT in this batch.
2. KS-1260 (bash_patch, runtime, **the pre-push gate every author runs**): `scripts/preflight/preflight.sh` (~:702-704) + a new suite. Scope is the RATIO ONLY (Wednesday's ruling), and Refs, never Closes.
3. KS-1101 N-3 (test-only): the ks1101 health test file.
4. KS-864 R-1 (test-only): NEW file ks864d.
5. KS-991 R-1 (test-only, bash suite): NEW file `scripts/__tests__/pre_push_hook_current_develop.test.sh` (it pins the pre-push hook).
6. KS-739 F1 (test-only): the ks739 test file.
7. KS-1062 F-1 (test-only): NEW file ks1062 startup-migrations.
8. KS-1258 N53-1 (test-only): the ks1258 test file (widens N44-1's regex).
9. KS-1230 N54-1 (test-only): the ks1230 test file (asserts a stored null).
- Build the all-nine tree over develop, run the affected suites (api-gateway, originate, the bash suites incl. the preflight siblings), and mail its oid with the nine heads.

## HOLDS
- Nothing deployed by you; nothing to demo. No messages to humans beyond rule 7 at wrap (only if something merged): KS-485 @peter, KS-772 @stuart.jamieson, facts only.
- Do NOT raise KS-730 (A or B), KS-1250, or anything beyond these nine. **Never reopen a Done ticket.** Auth last. Never `--no-verify`, never force-push a shared branch. Never delete; quarantine. `/api/seen` is never called.

## MERGE AUTHORITY, quoted from YOUR project's CLAUDE.md line 238
*"Wednesday's GO, naming the head SHA, is the approval."*

## RULED BY KAM, NOT YET IN AN ARTEFACT
- 2026-09-18 10:27, panel, verbatim: *"deploy to kintsugi. this is the dev server so it should be the first to update. the other server should only have proven deploys."*
- 2026-09-18 14:14, panel, verbatim: *"I'm going to be away for the next two days, so please keep going with tickets and activity while I'm away. Push merge and deploy whatever is ready. Whenever it's ready."* Wednesday's reading, acknowledged by Kam at 14:16 with no correction: kintsugi only, not demo; the signature classes still pause.
- 2026-09-18 09:22, panel: minimise gate duplication; batch file-disjoint changes into one gate.

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- 2026-09-19: Refs + contributes, no closing phrase; one batch gate; merges one at a time, sha-pinned, re-predicting over the then-current develop.
- 2026-09-19 (Seat B 2nd): no repo writes anywhere inside a push window; any diff line not attributable to your own action is a STOP.
- 2026-09-19 (the #1050-#1060 gate): locate tampers by a scope anchor + `from` text, not by line.

PROVENANCE:
- origin develop = 3c447abc7714e98fbba596aa1045b7bb47a6d215 | git -C /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files ls-remote origin refs/heads/develop, run 09:28 AEST, YOUR checkout | read 2026-09-19
- KS-1206 Backlog P4 on kamil.kreiser@secuura.ai, 0 comments; KS-1101 In Progress P3, last comment 2026-09-18T01:04Z; KS-1230 In Progress P3, last comment 2026-09-18T07:00Z; KS-1258 In Progress P4, last comment 2026-09-18T06:59Z; KS-1260 Backlog P4 unassigned, 0 comments; KS-864 Backlog P3, last comment 2026-09-16T17:35Z; KS-730 Backlog P2, 0 comments | Secuura Linear GraphQL, read-only query run by Wednesday 10:02 AEST | read 2026-09-19
- KS-991 Done ARCHIVED 2026-09-13T23:19Z (last comment 2026-09-13T23:19Z); KS-739 Done ARCHIVED 2026-09-14T08:33Z (last comment 2026-09-14T08:33Z); KS-1062 Done ARCHIVED 2026-09-13T05:35Z (last comment 2026-09-13T05:35Z) | Secuura Linear GraphQL with includeArchived, read-only, run by Wednesday 10:0x AEST | read 2026-09-19
- KS-485 Todo P2, last comment 2026-09-18T23:26Z; KS-772 Todo P2, last comment 2026-09-18T23:26Z | Secuura Linear GraphQL, read-only query run by Wednesday 09:30 AEST | read 2026-09-19
- KS-1250 Backlog P4 | Secuura Linear GraphQL, read-only query run by Wednesday 09:30 AEST | read 2026-09-19
- the nine READY files, their tips and target files | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_*_2026-09-19.diff.md headers, written and source-read by Wednesday 06:4x-10:0x AEST, my project | read 2026-09-19
- the merge-authority sentence | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/CLAUDE.md line 238, grep run 06:04 AEST | read 2026-09-19

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-19 10:03
- Nine items, nine distinct target areas; none is seat A's (no code there).
- The archived-ticket rule is stated once as a measurement plus a default, and "never reopen a Done ticket" is under HOLDS.
- KS-730, KS-1250 appear only under HOLDS; demo only under HOLDS.
