Seat A 11th successor (Secuura/Blockchain), from Wednesday

## BLUF
**Three jobs, in order: (1) KS-1254 (two test-only cells), (2) KS-1228 (the whole four-handler fix), then (3) the kintsugi rebuild on SATURDAY 19 Sep (AEST), which must end with #1038's Redis deploy action run VERBATIM.** Items 1 and 2 are file-disjoint, so mail me both heads in ONE mail and I gate them as one batch. Nothing merges without my signed GO naming the head. **Kam is away Sat 19 + Sun 20; his standing words are quoted below. Kintsugi only, never demo.**

## ITEM 0: boot, before any write
- Read your predecessor's handover WHOLE: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatA-10th-successor-2026-09-18.md` (FINAL STATE at the top). It names the worktrees, the filed tickets and the #1038 deploy action.
- Re-read `origin/develop` yourself. The value below is MY read; **if it has moved, say so before acting.**
- Re-read each ticket before acting on it (state, assignee, latest comment). A queue position is not a work state.
- Send me your plan confirmation (QUESTION mail, topic `plan confirmation`) before the first write.

## QUEUE, in order, every write gated on the previous step's rc
**1. KS-1254 (test-only, P4).** Two `it()` cells, in place, in `packages/shared/src/__tests__/ks256-spec-example-contract.test.ts`, pinning `PREFIXED_UUID_RE` (`scripts/spec-examples/check/contract.mjs`):
- an UPPER-case RFC variant nibble is REFUSED (must red ONLY under the gate's tamper M2, `[89ab]` to `[89abAB]`);
- `credit_<v4>` is ADMITTED (must red ONLY under tamper M6, `cred` made a substring);
- controls green under both: lower-case `a` variant admitted, `cred_<v4>` refused.
These were pre-measured in node by my brief-writer (my file `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/candidates.md` line 462, read-only to you). **Pre-measured is a claim, not a result: red-prove each cell yourself** against the M2 and M6 lines in the #922 round-2 gate's `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-18-ks679-922-30c773ee8-tier2-r2/evidence/tamper.out`. It pins EXISTING behaviour, so no product file changes. If either cell does not red under its tamper, STOP on it and tell me.
**2. KS-1228 (P3, on Kam's board account, so ours): the WHOLE fix, all four handlers** (`/version`, `/:id/share`, `/:id/transfer-custody`, and the certifications pin) in `services/originate/src/routes/documents.ts`: a refused request must not write an `action_provenance` row. The local model's product hunk for `/version` was CORRECT and is a starting point, not a spec: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-18_ks1228-ornith35b-night/out.md.checker/section_1.diff` (my project, read-only to you). **Its test file failed ts-jest's type check:** `TS6133` (originate's tsconfig has `noUnusedLocals` + `noUnusedParameters` ON) and **`TS2708 Cannot use namespace 'jest' as a value`, cause UNDIAGNOSED**, even though the test uses `jest.mock`/`jest.fn` the same way as the reference test. Diagnose TS2708 by measurement; do not guess. **Test cells: red-first at develop, green at head, and one control that stays green at both.** Runtime behaviour change, so per the project's `secuura-test-discipline` §5f it does NOT move to Done on merge.
- Both PRs: `Refs KS-<n>`, linkKind `contributes`, no closing phrase, a Test Evidence block. **Mail me both heads in ONE mail.**
**3. THE KINTSUGI REBUILD, on SATURDAY 19 Sep AEST, not before** (Stuart's dev box, ~2 h; my read-back to Kam named the weekend). Build to develop AS IT STANDS when you start (it will include items 1 and 2 if they have merged by then). Run the 9th's runbook exactly: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-18_seatA-9th/KINTSUGI-REBUILD-STATE.md`. Phase 0: NEW rollback tags (the `pre-20260918` set already exists, so name them for the day; verify BY NAME, 33 build services, 36 compose). `-p dev --profile phase2`. **Never `--remove-orphans`.** `--no-deps` on named services (postgres stays up). A phase-state file on disk; rotate only at a phase boundary. **Baseline `secuura-demo-service` BEFORE** (it crash-loops pre-existing without `DEMO_SERVICE_ENABLED`; a CHANGED failure mode is a stop). Verify by BEHAVIOUR, not by steps. Expect the KS-1245 smoke red (#1037's `/health/deep` shows degraded) and record it as the test lagging.
**THEN #1038's DEPLOY ACTION, VERBATIM, and it is the most important line in this brief:** *after the new api-gateway image is live on EVERY replica, per Redis: `redis-cli -u "$REDIS_URL" TTL secuura:gateway:notif:platform-settings`. If > 0: `PERSIST secuura:gateway:notif:platform-settings` and re-read -1. If -2: the allow-list has ALREADY failed open, so re-enter the connector integrations in admin settings and confirm TTL = -1. If -1: nothing to do.* Run it AFTER every replica is on the new image, never before (an old replica's next admin write re-arms the TTL). Mail me the TTL you read BEFORE and AFTER.
- **SSH:** the NSG admits `157.211.46.215/32` only and the address is dynamic. If SSH fails, STOP and mail me the address you egress from. **Do not touch the NSG yourself.**
- **KS-1256 (High) is NOT fixed by this rebuild or by #1038.** The allow-list still fails open on a Redis close/error/eviction. Do not describe the rebuild as closing it. It is not in your queue.

## HOLDS: do not do these
- **Nothing to demo.** Kam 10:27: demo takes only kintsugi-proven work, and only after Peter's nod.
- **KS-1250: do NOT raise it** (after it, a full smoke run anchors a real document on a named server). **KS-1175** (new fields on the immutable Cardano record): not yours. Both are Kam's.
- **No messages to humans.** The rule-7 ticket comments at wrap (KS-485 @peter, KS-772 @stuart.jamieson) are the only channel, and only if something merged or deployed.
- **Auth/MFA/OAuth work stays last.** Never `--no-verify`, never a force-push to a shared branch.
- **Never delete. Quarantine.** Never enter the quarantined worktree under `5_Project_History/quarantine/`.

## MERGE AUTHORITY, quoted from YOUR project's CLAUDE.md line 238, not paraphrased
*"Wednesday's GO, naming the head SHA, is the approval."* So each PR: QA gate at its head, then my signed GO naming that head, then you merge, sha-pinned, and re-predict the tree over the develop current at the time.

## RULED BY KAM, NOT YET IN AN ARTEFACT
- 2026-09-18 10:27, panel, verbatim: *"deploy to kintsugi. this is the dev server so it should be the first to update. the other server should only have proven deploys."*
- 2026-09-18 14:14, panel, verbatim: *"I'm going to be away for the next two days, so please keep going with tickets and activity while I'm away. Push merge and deploy whatever is ready. Whenever it's ready."* Wednesday's reading, said back to him and acknowledged at 14:16 with no correction: kintsugi only, not demo; the signature classes still pause.

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- 2026-09-18 (the 10th's brief): every PR `Refs` + linkKind `contributes`, no closing phrase; file-disjoint PRs are mailed together and gated as ONE batch (Kam 09:22, minimise gate duplication).
- 2026-09-18 (the #922 correction, recorded on KS-679 `cdf27b63`): my GO is the approval under the 09-11 merge flow; Peter's open comment is told in the rule-7 comment, not waited on.

## What Wednesday owes you
- A batched gate on items 1 and 2 when you mail their heads; a signed GO naming each head before any merge; an answer to anything you ask.

PROVENANCE:
- origin develop = 8b9c3f022bee76b79a47f1b8c5de8ad3ddb4a0ae (#1041 merged) | git -C /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files ls-remote origin refs/heads/develop, run 14:49 AEST, YOUR checkout | read 2026-09-18
- KS-1254 Backlog P4 unassigned; KS-1228 Backlog P3 on kamil.kreiser@secuura.ai; KS-1256 Backlog P2; KS-1250 Backlog; KS-1175 Backlog | Secuura Linear GraphQL, read-only query run by Wednesday 14:49 AEST (5 of 5 returned) | read 2026-09-18
- kintsugi runs a105cd32b; develop 8b9c3f022; the #1038 deploy action text | the 10th's handover FINAL STATE, /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatA-10th-successor-2026-09-18.md, YOUR project | read 2026-09-18
- KS-1245 Backlog P3, 0 comments ("F-1: scripts/smoke-test.sh:107 fails any /health/deep check that is not 'up'"): named only as the expected smoke red, NOT queued | Secuura Linear GraphQL, read-only query run by Wednesday 14:51 AEST | read 2026-09-18
- the merge-authority sentence | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/CLAUDE.md line 238, grep run 14:5x AEST | read 2026-09-18
- KS-1254 pre-measured cells; KS-1228 TS6133/TS2708 | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/candidates.md lines 458 and 462, my project | read 2026-09-18
- the KS-1228 starting hunk exists (1014 bytes) | ls of /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-18_ks1228-ornith35b-night/out.md.checker/section_1.diff, 14:49 AEST, my project | read 2026-09-18
- the rebuild runbook and the M2/M6 tamper file exist | ls of both paths, 14:49 AEST | read 2026-09-18
- weekly usage 32%, under the 90% cap | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/usage_gate.sh --check, 14:48 AEST, my project | read 2026-09-18

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-18 14:50
- Merge authority is stated once, quoted from the project CLAUDE.md line 238; nothing merges without a signed GO.
- KS-1250, KS-1175 and KS-1256 appear only as holds/awareness, never in the queue.
- Items 1 and 2 touch packages/shared tests and services/originate respectively: file-disjoint, so one batch gate is consistent.
- The rebuild date (Saturday 19 Sep AEST) matches the read-back to Kam; demo appears only under HOLDS.
