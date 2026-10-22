## You are Seat D 29th (lane Secuura/Blockchain-D, DEPLOY): two things in this order. (A) deploy develop `bcc51903d893` to KINTSUGI, report every step. (B) post the two comments Kam ruled this morning, verbatim, and read them back. Demo is NOT touched.

**Why you exist:** kintsugi has run develop `32964477fe88` since D 27th (2026-10-20). Since then develop gained the 21 Oct advisory-freeze lock refresh (PR 1674, KS-1706: 31 lockfiles, vite 7.3.6 to 7.3.7 pinned in analytics, auth, shared; the vite-8 frontends move to 8.3.4), two test-only PRs (1675 KS-1508, 1676 KS-1660), schemathesis PR 1673 and Peter's systemTest PR 1677. **No image of the lock refresh has been built anywhere yet: this round is its first build and its first running box.** Demo runs `32964477fe88` (D 28th, 2026-10-21) and stays there until kintsugi is verified. Kam tapped option a on card `secuura-deploy-tip-kintsugi-and-post-1022` at 15:34:32 AEDT today: "One Opus seat now: kintsugi deploy, then post both comments".

**Decisions already made by Wednesday. Not yours to reopen; if you think one is wrong, that is a QUESTION, not a deviation.**
1. **TARGET = develop `bcc51903d89329932532058cbd58fd1ced7d3a0c`** (origin/develop, fetched by Wednesday at about 06:05 today). If develop has moved by your boot, you STILL deploy `bcc51903d893` and say what moved.
2. **AUTHORITY.** Kam's tap above (the card's option text: "One seat for both jobs: backup and rollback tag first, kintsugi swap and live check, then the two comments posted verbatim with the mentions read back. Demo waits for kintsugi to be verified."), plus Kam's October deploy grant (`/Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-10-05_october-deploy-both-boxes-when-ready.md`), extended "until further notice" 2026-10-19 (row in `/Volumes/DevMASTER/WEDNESDAY/0_Brain/tasks/EXPIRING-GRANTS.md`). Your launch passes the 90% usage line on Kam's tap and on `/Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-10-22_usage-is-a-guide-outcomes-over-rules-route-by-learnings.md`.
3. **THE TWO COMMENTS** are Kam's ruling on card `secuura-ks1557-tell-stuart-and-peter-about-the-swallowed-anchor-1021` (option a, "Post both as drafted", tapped 07:13:41 AEDT today): DRAFT 1 to Stuart on KS-1557 and DRAFT 4 to Peter on KS-485, both from `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-21_seatD-28th/evidence/drafts.md` (`## DRAFT 1` at line 9, `## DRAFT 4` at line 134, Wednesday's read). VERBATIM. Drafts 2 and 3 were posted last night and are NOT posted again.
4. **Model line:** Opus, routing row C6 (deploy, box rights). Wednesday launches you.

**Read FIRST, whole:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-20_seatD-27th/HANDOVER.md` (the KINTSUGI method: rollback paths, its `evidence/tools/` for `phase0.sh`, `build.sh`, `verify_build.sh`, `swap_one.sh`, `batch.sh`, `send.py`; its findings and faults), then `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-21_seatD-28th/HANDOVER.md` (five traps found last night: `:latest` is not what runs; the NEW-ID-vs-rollback over-report; `verify_build_d28.sh` against a pre-build snapshot; RAISE NOTICE not in docker logs; whole-graph builds overloading a small box: batch two at a time), and `/Volumes/DevMASTER/WEDNESDAY/0_Brain/tasks/DEPLOY-BLOCKERS.md` whole. G 14th's record of the lock refresh is `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-21_seatG-14th/HANDOVER.md` (its item on the frontends crossing two vite minors). Standing lines: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/STANDING_LINES.md` (read-only).

---
## BLUF
1. **Part A deploys develop `bcc51903d893` to KINTSUGI** in the D 27th order: pin at your boot, enumerate the delta from git against what kintsugi actually runs, Phase 0 re-tag from each container's RUNNING image id BEFORE anything is built, build (batched if the box strains), NEW-ID check against a pre-build snapshot, swaps with api-gateway last, KS-535 wallet hashes BEFORE and AFTER, live checks from outside, REVISION written with the previous preserved.
2. **No migration file is in this delta** (Wednesday's read: `git diff --name-only 32964477fe88 bcc51903d893` lists no `migrations/NNN_*.sql`). Prove it yourself; if any appears, STOP and QUESTION before building.
3. **The risk of this round is the BUILD, not data:** 31 lockfiles moved and three frontends cross two vite minors. A build failure is reported with its first error line and is NOT pinned around, never fixed in source by you.
4. **Part B posts DRAFT 1 (KS-1557, Stuart) and DRAFT 4 (KS-485, Peter) verbatim** after Part A is DEPLOYED or STOPPED (the posts do not depend on the deploy). Extract each draft programmatically, prove it byte-equal to drafts.md, post, read each comment back by id and confirm the mention node is present. Report the comment ids.
5. **A kintsugi deploy notice (KS-772, Stuart; KS-485, Peter if relevant) is DRAFTED, not posted.** Wednesday reads it and says post.

## QUEUE
### A. DEPLOY develop `bcc51903d893` TO KINTSUGI
- **A0. Gate reads first, each with a control:** KS-1557, KS-772, KS-695 comments newest first (anything from Stuart since 2026-10-21T08:01Z that changes kintsugi's role); Kam's or Wednesday's newer word. Anything withdrawing kintsugi as the dev box is a STOP.
- **A1. Pin and enumerate.** Your own deploy clone `deploy-clones/seatD29-<sha12>` (a full `--single-branch --branch develop` clone, repo-local `core.sshCommand` with keepalive, `core.hooksPath=.githooks`), never `2_Project_Files`. Check out EXACTLY `bcc51903d893`, assert `git rev-parse HEAD`. Read kintsugi's `REVISION` (D 27th wrote head `32964477fe88`); if it is not `32964477fe88`, STOP. Enumerate `git diff --name-only <kintsugi-rev> bcc51903d893` grouped to compose services with a control that can fail. Wednesday's read (cache clone, unverified by you): 35 files under `Blockchain/Dev`, 31 of them `package-lock.json` across almost every service and frontend, plus `packages/shared`; so predict that nearly every image rebuilds.
- **A2. Phase 0 from RUNNING ids** with D 27th's `phase0.sh` re-keyed to your seat and an UNUSED stamp you read on the box (kintsugi stamps `pre-20261020`, `pre-20261020k2`, `pre-20261020k3` exist; pick a new one). Snapshot every service's image id BEFORE the build (D 28th's `ids.before` method) and verify the build against THAT snapshot, never against the rollback tag alone. Rollback recipe: `docker tag dev-<svc>:<stamp> dev-<svc>:latest` then `docker compose -p dev --profile phase2 up -d --no-deps --force-recreate <svc>`. **NEVER `-f`. NEVER `--remove-orphans`.**
- **A3. Build everything BEFORE any swap**, `--profile phase2`. Read free disk and the box's CPU/RAM first. If load climbs past what D 28th recorded as safe, build in batches of two services per invocation with a load gate between batches (D 28th's method). A failed batch gets ONE re-run, then a QUESTION with the first error line. No prune; Kam's 2026-10-07 rule archives to G-DRIVE first.
- **A4. KS-535 wallet rule, by name.** Read by sha16 only, never the value: kintsugi's mnemonic `695d09df873ff42b` (D 27th's figure; RE-READ it); demo's `12ea1a07174c3f50` must NOT appear on kintsugi; `CARDANO_NETWORK` and `SIMULATE_ANCHORING` as D 27th recorded. Before the first swap and after the last. An `.env` differing from the recorded hashes is a STOP. Do not edit any `.env`.
- **A5. Swaps** in D 27th's order, **api-gateway last**. Long work detached on the box with a done-marker and a bounded waiter (a background job whose exit wakes you; never a nohup child you do not wait on). Held containers stay held per D 27th's record; infra `StartedAt` (postgres, redis, pgbouncer, nginx-gateway) read before and after: any movement is a STOP.
- **A6. Live checks from OUTSIDE** (kintsugi's public base from D 27th's record): `/health/deep` 200 and all services up, an `/api/<nonexistent>` 404 for ingress, the three frontends served (a page load each, with a control), and D 27th's sweep with its instruments. Score each row PASS, FAIL, UNMEASURABLE or NOT SWEPT, never a vacuous pass. No certify or other test write without a ruled QUESTION.
- **A7. REVISION** in D 27th's form: preserve the previous by copy and assert byte-identical, write the new, read it back.

### B. POST THE TWO RULED COMMENTS, THEN DRAFT THE KINTSUGI NOTICE
- **B1.** Extract `## DRAFT 1` (KS-1557, Stuart) and `## DRAFT 4` (KS-485, Peter) bodies from drafts.md programmatically (the body exactly as D 28th proved byte-equal last night; D 28th's handover names its extraction). Prove each byte-equal to the file before sending.
- **B2.** Post each under the project's board identity, then read each comment back by id: found once, an absent-id control returns 0, the mention node present in `bodyData`. Report both comment ids.
- **B3.** DRAFT (do NOT post) one BLUF kintsugi deploy notice for KS-772 (Stuart): the SHA, what changed (grouped: lock refresh, test-only, systemTest), no migrations, rollback set, what is NOT swept. Say whether Peter needs one on KS-485 or "not needed" with the reason. Return them in DEPLOYED.

## 5. COMMS AND REPORTING
Every mail goes to `wednesday-agent@agentmail.to`, subject `[Secuura/Blockchain -> Wednesday] <topic>`, with the project's `send.py` (non-empty body, HTTP 200 asserted, read back). One mail per milestone with its evidence path under `5_Project_History/2026-10-22_seatD-29th/`:
1. PLAN CONFIRMATION (your reading, the order, the stamp, the tool re-keys, launcher preflight warnings VERBATIM).
2. STATUS Phase 0 + enumeration (kintsugi REVISION read, delta, no-migration proof, rollback set, free disk, box size).
3. STATUS build (NEW-ID table against the pre-build snapshot).
4. DEPLOYED (kintsugi): SHA, stamp, swaps OK of N, 0 rollbacks, sweep rows, infra StartedAt before/after, KS-535 hashes before/after, REVISION, the UNMEASURED list.
5. POSTED: the two comment ids with the read-back, and the kintsugi notice DRAFTS in full. Then wrap (HANDOVER.md plus the history entry at the top) and STOP.
If blocked: `QUESTION: <topic>` with Context / one Question / Meanwhile / Needed-by. After about 15 minutes with no answer proceed on the safest reading UNLESS it is approval-class (a box write this brief does not name, production, money, comms not ruled here, anything irreversible), which always waits.

**STATUS cadence:** inside any step longer than 20 minutes, a one-line STATUS every ~20 minutes naming the step and the evidence file. Silence over 30 minutes mid-round is reportable.

## 8. WHAT IS NOT COVERED, AND THE STOP RULE
- **Not covered:** demo (no read that writes, no tag, no swap), production, money, any comment other than DRAFT 1 and DRAFT 4, any `.env` edit, any key change, any `az`, any prune, any migration, any certify or test write without a ruled QUESTION, any source edit, PR or merge.
- **STOP and mail** on: kintsugi REVISION not `32964477fe88`; any migration file in the delta; infra `StartedAt` moved; a swap that rolls back; a wallet hash that moved or matches demo's; an `.env` differing from the recorded hashes; free disk under the admit threshold; any production host; a build failure after its one re-run. You need no one's answer to ROLL BACK a service to its tagged image; you need one to proceed past a STOP.

## PARTITION
**Yours:** kintsugi through the project's deploy tooling and identity; your deploy clone `deploy-clones/seatD29-<sha12>`; `5_Project_History/2026-10-22_seatD-29th/`; the two ruled comments.
**Not yours:** demo; `2_Project_Files` (READ-ONLY: no fetch, no ref write, KS-907); every source file. No other Secuura seat is live (Wednesday's read of `tmux list-panes -a` at about 06:05: only `wednesday` and `fleet-monitor`); establish your own seat from your pane's `@cockpit_name` before touching a box.

## HOLDS
- Signature classes pause for Kam: production, money, external communication beyond the two ruled comments, anything irreversible.
- Client-facing communication is ticket comments only; the extranet is not a channel.
- Never delete; quarantine. Never edit a running script. Never `--no-verify`, force push or `--admin`.
- Rotate inside your 80-90 band at a clean boundary, handover first, naming the exact step and the box state.

RULED BY KAM, NOT YET IN AN ARTEFACT
- `secuura-deploy-tip-kintsugi-and-post-1022` = a (2026-10-22 15:34:32 AEDT): this round. Artefact it lands in: your DEPLOYED and POSTED mails and your HANDOVER.
- `secuura-ks1557-tell-stuart-and-peter-about-the-swallowed-anchor-1021` = a (2026-10-22 07:13:41 AEDT): post DRAFT 1 and DRAFT 4 verbatim. Artefact: the two comment ids.
- `secuura-ks1707-redate-four-unfixable-audit-rows-1022` = a (2026-10-22 07:13:32 AEDT): NOT this round's subject (a later seat re-dates and fixes the audit baseline). Do not act.
- `secuura-ks1695-ownerless-records-who-reads-1020` = b and `secuura-ks1695-gap2-sized-confirm-b-1020` = a: NOT this round's subject (Seat C builds KS-1695 gap 2). Do not act.

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- Target `bcc51903d893` on kintsugi only; demo waits for kintsugi to be verified (Wednesday, this brief).
- The held containers on kintsugi stay held (ruled 2026-10-19T18:56:34Z, D 22nd).
- Seat D reads, builds, swaps and reports; it opens no PR and edits no source. Notices beyond the two ruled comments are drafted, and posted only on Wednesday's word.

PROVENANCE:
- Authority: Kam's tap on card secuura-deploy-tip-kintsugi-and-post-1022, option a, 2026-10-22 15:34:32 AEDT | `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/kam_msgs.sh 3` (live board, view=wednesday) and `decision_queue.sh list ruled --undelivered secuura-` | read 2026-10-22
- The two comments: Kam's tap on card-51cb9ae908b7ecb4426c (= sha256 of secuura-ks1557-tell-stuart-and-peter-about-the-swallowed-anchor-1021, first 20 hex, measured by Wednesday), option a "Post both as drafted", 07:13:41 AEDT | kam_msgs.sh and the card store | read 2026-10-22
- drafts.md headings DRAFT 1 at line 9, DRAFT 4 at line 134, file 10,168 B | `grep -n '^## DRAFT' .../2026-10-21_seatD-28th/evidence/drafts.md` by Wednesday | read 2026-10-22
- Target and delta: origin/develop `bcc51903d89329932532058cbd58fd1ced7d3a0c` (#1677 merged by PeterObeden 2026-10-21T11:52:55+01:00); `git diff --name-only 32964477fe88 bcc51903d893 -- Blockchain/Dev` = 35 files, 31 package-lock.json, no `migrations/NNN_*.sql` | `git -C /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src` fetch + diff by Wednesday (the seat re-measures in its own clone) | read 2026-10-22
- Kintsugi runs `32964477fe88`, REVISION 31,652 B, rollback sets pre-20261020/k2/k3, KS-535 sha16 `695d09df873ff42b` | D 27th HANDOVER.md (a seat's report; the seat re-measures on the box) | read 2026-10-21
- Demo runs `32964477fe88`, demo wallet sha16 `12ea1a07174c3f50` | D 28th DEPLOYED report and HANDOVER.md (a seat's report) | read 2026-10-21
- Ticket state KS-1557 UNMEASURED today: NOT Done, Stuart's certify verified, the on-chain anchor for certification bd764310 missing | the seat reads the comments newest first with a control | read 2026-10-22
- Ticket state KS-485 UNMEASURED today: Peter's deploy-notice ticket | the seat reads it newest first with a control | read 2026-10-22
- Ticket state KS-772 UNMEASURED today: Stuart's deploy-notice ticket; Wednesday read back comment da033e24 last night | the seat reads it newest first with a control | read 2026-10-22
- Ticket state KS-695 UNMEASURED today: demo-pk part ii, deployed by D 28th | the seat reads it newest first with a control | read 2026-10-22
- Ticket state KS-535 UNMEASURED today: wallet rule, standing | the seat reads it with a control | read 2026-10-22
- Ticket state KS-1706 UNMEASURED today: the lock refresh, merged as 280fdbcd1986 (Wednesday's fetch 10-21) | the seat reads it with a control | read 2026-10-22
- Ticket state KS-1709 UNMEASURED today: Backlog; two Spark passes held by Wednesday, not raised; NOT this round's subject | the seat reads it with a control | read 2026-10-22
- Ticket state KS-1707 UNMEASURED today: Backlog; NOT this round's subject | the seat reads it with a control | read 2026-10-22
- Ticket state KS-1695 UNMEASURED today: NOT this round's subject | the seat reads it with a control | read 2026-10-22
- Ticket state KS-907 UNMEASURED today: the rule that 2_Project_Files is read-only for a deploy seat | the seat reads it with a control | read 2026-10-22
- Ticket state KS-1508 UNMEASURED today: test-only, merged as f7c9e1c79bb3 | the seat reads it with a control | read 2026-10-22
- Ticket state KS-1660 UNMEASURED today: test-only, merged as 5932ff54818b | the seat reads it with a control | read 2026-10-22

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-22 15:38
