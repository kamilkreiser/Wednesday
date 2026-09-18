Seat B 2nd successor (Secuura/Blockchain), from Wednesday

⚠ TWO SEATS SHARE THIS INBOX TODAY. This brief is for **Seat B 2nd** (raise nine held local-model fixes). **Seat A 12th** is live beside you, doing the kintsugi rebuild; its brief's subject names "seat A 12th". A mail naming seat A is not yours; do not act on it. Seat A writes NO code and merges nothing; you touch ONLY the nine files below, each in your own worktree. Never touch seat A's worktree or its phase-state file.

## BLUF
**One job: raise NINE fixes the local model (Ornith) wrote and Wednesday held yesterday, one PR per item, then mail me ALL nine heads in ONE mail so I gate them as ONE batch.** Nine different files, so they are file-disjoint. Nothing merges without my signed GO naming the head. Kam is away Sat 19 + Sun 20; his standing words are quoted below.

## ITEM 0: boot, before any write
- Read the 11th's handover WHOLE: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatA-11th-successor-2026-09-18.md` ("Held for the NEXT seat to RAISE" names the method).
- **develop has MOVED since the fixes were written and I do not know what landed.** My `ls-remote` at 06:04 AEST reads `59412d0575dff3243f5f0ccd1e50608ddb920d6c`; the fixes were measured at `8b9c3f022` (KS-1261, KS-1136 item 1) and `52df64f84` (the other seven). UNMEASURED by me: before raising any item, confirm its patch still applies to develop AS IT STANDS and its target file is unchanged since the pinned tip (`git diff <pinned>..origin/develop -- <file>` empty). A changed file is a STOP for that item: tell me, raise the rest.
- Re-read each ticket before acting (state, assignee, latest comment).
- Send me your plan confirmation (QUESTION mail, topic `plan confirmation`) before the first write.

## QUEUE: the nine, each a PR (`Refs KS-<n>`, linkKind `contributes`, no closing phrase, a Test Evidence block)
The READY files are in MY tree, read-only to you: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_<ID>_*_2026-09-18.diff.md`. **CANONICAL PATCH = the run's `out.md.checker/section_N.diff`, each applied with its `section_N.opts`** (every READY header names its run dir under `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/`). Use the 11th's method, `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-18_seatA-11th/raise/raise2.py`: verbatim, red-first at develop then green at head. **STOP on any deviation** from what the READY header predicts.
1. KS-1261 → `Blockchain/Dev/scripts/preflight/preflight.sh` (initialise FAILED_LEGS / fail_total). **The pre-push gate every author runs: say so in the PR body.**
2. KS-1136 item 1 → `Blockchain/Testing/jobs/04-container-trivy.sh` (a failed per-image scan exits 1, not clean).
3. KS-1267 Q1 (test-only) → `.../services/originate/src/__tests__/ks1228-a-refused-request-writes-no-provenance-row.test.ts`. Its header mentions `--recount`: read it.
4. KS-1258 N44-1 (test-only) → `.../services/api-gateway/src/__tests__/ks1258-degraded-optional-service-advice.test.ts`
5. KS-1230 N45-5 (test-only) → `.../services/api-gateway/src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts`
6. KS-1202 N-B (test-only) → `.../services/originate/src/__tests__/ks1202-a-mismatched-data-documenttype-is-refused.test.ts`
7. KS-1153 R-918-A (test-only, bash suite) → `Blockchain/Dev/scripts/__tests__/run_code_guards.test.sh`. **Strict apply MISPLACES this hunk; apply with the NAMED `--recount` its header states.**
8. KS-1209 N41-3 (test-only, bash suite) → `Blockchain/Dev/scripts/__tests__/preflight_verdict_names_real_failures.test.sh`
9. KS-1134 (test-only, bash suite) → `Blockchain/Dev/scripts/__tests__/orchestrate_jobs.test.sh`
- **Note for your evidence:** items 1 and 8 both bear on preflight's verdict (a product change and a suite that drives it). Run item 8's suite on the tree WITH item 1 applied too, and report both results.
- Runtime behaviour changes (1, 2) stay In Progress on merge per your project's `secuura-test-discipline` §5f; test-only items may go Done after merge.
- Build the predicted all-nine tree over develop and run the affected suites on it; mail me that tree's oid with the nine heads.

## HOLDS: do not do these
- **Nothing deployed by you; nothing to demo.** Seat A owns kintsugi today.
- **Do NOT raise KS-1250** (a READY for it exists in my tree: it is Kam's, leave it) or anything beyond these nine. **Do NOT brief or touch KS-1260** (same file as item 1; it waits for item 1 to merge).
- **No messages to humans** beyond the rule-7 ticket comments at wrap (KS-485 @peter, KS-772 @stuart.jamieson), and only if something merged.
- Auth/MFA/OAuth last. Never `--no-verify`, never a force-push to a shared branch. **Never delete. Quarantine.** Never enter `5_Project_History/quarantine/`. `/api/seen` is never called.

## MERGE AUTHORITY, quoted from YOUR project's CLAUDE.md line 238, not paraphrased
*"Wednesday's GO, naming the head SHA, is the approval."* So: one batch QA gate at the nine heads, then my signed GO naming each head, then you merge one at a time, sha-pinned, re-predicting the tree over the develop current at each merge.

## RULED BY KAM, NOT YET IN AN ARTEFACT
- 2026-09-18 10:27, panel, verbatim: *"deploy to kintsugi. this is the dev server so it should be the first to update. the other server should only have proven deploys."*
- 2026-09-18 14:14, panel, verbatim: *"I'm going to be away for the next two days, so please keep going with tickets and activity while I'm away. Push merge and deploy whatever is ready. Whenever it's ready."* Wednesday's reading, acknowledged by Kam at 14:16 with no correction: kintsugi only, not demo; the signature classes still pause.
- 2026-09-18 09:22, panel: minimise gate duplication; batch file-disjoint changes into one gate.

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- 2026-09-18: every PR `Refs` + linkKind `contributes`, no closing phrase; file-disjoint PRs are mailed together and gated as ONE batch.
- 2026-09-18 (the 11th's handover): these nine are raised only by a seat told to; you are told.

## What Wednesday owes you
- An answer to your plan confirmation; one batch gate on the nine heads; a signed GO per head before any merge.

PROVENANCE:
- origin develop = 59412d0575dff3243f5f0ccd1e50608ddb920d6c | git -C /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files ls-remote origin refs/heads/develop, run 06:04:40 AEST, YOUR checkout | read 2026-09-19
- KS-1261 Backlog P4 unassigned, 0 comments; KS-1136 Backlog P3 on kamil.kreiser@secuura.ai, 0 comments; KS-1267 Backlog P4 kamil.kreiser, 0 comments; KS-1258 In Progress P4 kamil.kreiser, last comment 2026-09-18T06:59Z; KS-1230 In Progress P3 kamil.kreiser, last comment 2026-09-18T07:00Z; KS-1202 In Progress P2 kamil.kreiser, last comment 2026-09-17T09:09Z; KS-1153 Backlog P4 kamil.kreiser, 0 comments; KS-1209 In Progress P4 kamil.kreiser, last comment 2026-09-18T04:39Z; KS-1134 Backlog P4 kamil.kreiser, 0 comments | Secuura Linear GraphQL, read-only query run by Wednesday 06:05 AEST (17 of 17 returned) | read 2026-09-19
- KS-1250 Backlog P4; KS-1260 Backlog P4 unassigned | same query, 06:05 AEST | read 2026-09-19
- KS-485 Todo P2 last comment 2026-09-18T07:01Z; KS-772 Todo P2 last comment 2026-09-18T07:01Z | Secuura Linear GraphQL, read-only query run by Wednesday 06:06 AEST | read 2026-09-19
- the nine READY files, their pinned tips, run dirs and target files | /usr/bin/grep of each /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_* header, 06:0x AEST, my project | read 2026-09-19
- raise2.py exists | ls of /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-18_seatA-11th/raise/, 06:09 AEST, YOUR project | read 2026-09-19
- the merge-authority sentence | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/CLAUDE.md line 238, grep run 06:04 AEST | read 2026-09-19
- weekly usage 44%, under the 90% cap | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/usage_gate.sh --check, 06:03 AEST, my project | read 2026-09-19

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-19 06:09
- Nine items, nine distinct files, none of them touched by seat A (which writes no code).
- develop's move is stated UNMEASURED with the check that closes it per item; a changed file stops only that item.
- KS-1250 and KS-1260 appear only under HOLDS; demo appears only under HOLDS.
- Merge authority is quoted once from the project CLAUDE.md line 238.
