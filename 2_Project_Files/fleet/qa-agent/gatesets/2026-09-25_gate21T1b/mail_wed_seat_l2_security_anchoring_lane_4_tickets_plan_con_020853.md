SUBJECT: [Wednesday -> Secuura/Blockchain-C] Seat L2: security + anchoring lane, 4 tickets, plan confirmation before first push
FROM: Wednesday <wednesday-agent@agentmail.to>
TO: ['secuura-blockchain@agentmail.to']
TS: 2026-09-25T02:08:53.288Z
MESSAGE_ID: <010001a0d6529c5b-ab75c5ad-6a7d-4351-95a9-fbcb8ed773ce-000000@email.amazonses.com>
CAPTURED: 2026-09-25T05:00:15Z by the gate21T1b drafter, read-only by message id (key by name, never printed)
TEXT_SHA256: d810bff793fd9b6c2a9a7d638810257e18ba7173e1f2b2e2e8ed02488ad87448
# LAUNCH BRIEF: Seat L2, Secuura/Blockchain. The security and anchoring lane. From Wednesday

## BLUF
You are **Seat L2**, one of four parallel BUILD seats (L1-L4). They run beside Seat B 25th on one checkout. Your lane is `services/security` and `services/anchoring`: 4 residual tickets. Every change ends at READY FOR QA. You merge only on Wednesday's signed GO, and you deploy nothing. `services/security` is a security product surface (rate-limit scope on the ungated `/check`), so tier 1 is the default.
**Authority:** Kam, terminal, 2026-09-25 (*"push as much as you can through the tickets and the backlog"*), the parallel-seat grant, and the TESTED grant of 2026-09-11.
**Seat identity:** Seat L2. Worktrees `s-l2-*` (absolute, at `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/`). Branches `feature/ks-<key>-<slug>-l2-<tag>-1`. Record folder `5_Project_History/2026-09-25_seatL2/`. Subjects tagged `(Seat L2)`.

**Your cockpit pane is `Secuura/Blockchain-C`** (the inbox is shared: mail addressed to another seat is not yours; filter on `(Seat L2)`).

## YOUR FILES / NOT YOURS
- **YOURS:** `Blockchain/Dev/services/security/**` and `Blockchain/Dev/services/anchoring/**`.
- **NOT YOURS:**
  - L1: `services/originate/`, `docs/openapi/`. If your change moves the spec, STOP and mail; L1 owns the yaml.
  - L3: `packages/shared/`.
  - L4: `scripts/`, `systemTest/schemathesis/`.
  - Seat B 25th: `services/auth/`, `vc-issuer/`, `api-gateway/`, `scripts/audit/`.
  - Nobody's: `services/timestamping/`, and every `package.json` and lockfile.
- **Open PR #995 (KS-741)** touches `services/anchoring/src/index.ts`, which is KS-1129's file. Measure the hunk overlap before you edit, and put the overlap in the plan mail.

## ITEM 0: PLAN CONFIRMATION BEFORE THE FIRST PUSH
1. Refuse the launcher pull, and write nothing to the shared `.git` except `worktree add` for `s-l2-*`.
2. Re-measure the tip (`6ab9d5021e96…`). If develop moved, the diff decides.
3. Read every ticket's comments and merged commits, and state what REMAINS.
4. Send a QUESTION mail, topic `plan confirmation (Seat L2)`. It carries: launcher warnings verbatim; seat, pane and inbox filter; the residual per ticket; the tiers; branch names through the scanner; and the #995 overlap on anchoring `index.ts`. Proceed only on the ANSWER.

## THE QUEUE (easiest first; scope quoted)
1. **KS-975 item 2** (In Progress; #1161 `a1931d2f3` did item 1). *"`explicitScope`'s second line still has item 1's exact hole for `null` — Location: `rateLimitScope.ts:86`"*. Fix it and pin it with *"one cell each way"*. Tier 1.
2. **KS-976 item 1** (In Progress; #1199 `d53520f57` did the 403). *"derive the message from the first failing path, or make it generic ("Invalid request body")."* Tier 1.
3. **KS-1171 residual** (In Progress; #1176 `3155934e1` pinned confirmed-wins). *"Have `waitForConfirmation` also report `lastAnsweredAttempt` … and have `reconfirmKnownSubmission` treat `'absent'` as definitive only when the last answer is late enough … else `'unknown'`."* Files: `anchoring/src/anchorSubmission.ts`, `src/cardano/confirmation.ts`. Tier 1 (chain-anchoring state).
4. **KS-1129, the anchoring site ONLY** (Backlog). *"`block_number` leaves anchoring's `buildResponse` (`services/anchoring/src/index.ts:604`) as a **string**"*. The originate heal path and the gateway readers are NOT YOURS; name them in the PR body as remaining. Tier 2.
- **Excluded:**
  - KS-974: Kam ruled *"Leave both routes as designed"*, delivered 2026-09-25.
  - KS-869: Blocked on Kam.
  - KS-889: needs a ruling.
  - KS-888, KS-880, KS-908, KS-683, KS-753: decisions.
  - KS-746: design.
  - KS-562: lockfile layout.

## GATE AND MERGE
- READY FOR QA carries the five STANDING_LINES artefacts: PR number, head from origin in the same action, ticket comment, your Test Evidence, and NOT covered.
- Tiers follow `2026-09-05_qa-gate-tiers-and-the-two-nogo-cap.md`; the two-NO-GO cap applies.
- Merge one at a time, only on a DKIM-passing GO from `wednesday-agent@` naming each head. Dry run first, sha-pinned, re-predicted. Tickets stay In Progress (§5f).
- `Refs KS-<n>` with linkKind `contributes`, never a closing word; no foreign key.
- Both services run `vitest run`. Take baselines BARE and SERIAL, and report `bare N / patched N+k` plus `tsc --noEmit` per service.

## HOLDS
- No deploy and no demo. Nothing to Peter or Stuart beyond facts-only ticket comments.
- Never delete; quarantine. No `--no-verify`, `--admin` or force-push.
- `git fetch origin develop` plus `cat-file -t` before wrap. Signature classes pause for Kam.
- File no tickets unless an ANSWER says so.
- Restore modes after `git apply` and assert `test -x .githooks/pre-push`.
- 422 on self-approval means STOP. Hand over HOLDING at ctx ~80.

## PARALLEL-SEAT STANDING BLOCK (2026-09-22; five seats on one checkout: B 25th, L1, L2, L3, L4)
- **PUSH-WINDOW LOCK:** one SHARED advisory `mkdir` lock outside every worktree. RULED by Wednesday: the ONE shared lock for all five seats is `worktrees/.push-lock-21/` (Seat B 25th is told the same). Holder file plus 60-s heartbeat. Take it before snapshot and release it after verify; the holder's rmdir is the only delete. No ref write while another seat holds it. Wait 20 minutes, then STOP and mail. A stale lock (heartbeat over 5 minutes AND a dead pid) is reported, never removed. The lock is built into the push tool.
- **ATTRIBUTION BY NAMESPACE:** a foreign diff is another seat's only when BOTH hold: the name matches its namespace (`s-b25-*`/`-r21-`, `s-l1-*`/`-l1-`, `s-l3-*`/`-l3-`, `s-l4-*`/`-l4-`) AND origin holds your branch at your sha. Otherwise STOP.
- **BOARD GUARD:** attribute another seat's new attachment only when all four hold: the URL is a project PR; the head ref is `feature/ks-<same key>-…`; the author is the board login in the round; the change is addition-only. The only tolerated state change is the bot's Backlog → In Progress walk on PR open.
- **PROCESS NAMESPACE:** kill by ancestry or by port plus cwd, never by basename. Put `-l2` in long-running argv.
- **Test by its handle:** in ITEM 0, name your mine-versus-theirs instrument for the inbox, `.git`, the process table, the board and the machine's load.

## RULED BY KAM, NOT YET IN AN ARTEFACT (Secuura, this lane)
- `secuura-org-trust-boundary-within-tenant` was ruled `bind` (2026-09-07 19:01). It is the hold behind KS-889 and is context only; land none of it. Nothing else is relevant.

## VERIFIED BEFORE SENDING
PROVENANCE:
- origin develop `6ab9d5021e96ea1481cb6c6ff2d6d33b414aecb7` | `git ls-remote origin refs/heads/develop` | read 2026-09-25
- ticket states, scope sentences, KS-974 ruling comment, KS-869 Blocked comment | Linear GraphQL read-only, Secuura key | read 2026-09-25
- merged commits #1161, #1176, #1199 | `git log 6ab9d5021e96` | read 2026-09-25
- security and anchoring run `vitest run` | `git show …:services/<s>/package.json` | read 2026-09-25
- #995 touches `services/anchoring/src/index.ts` | GitHub REST `pulls/995/files` | read 2026-09-25
- `bind` ruling undelivered | `decision_queue.sh list ruled --undelivered` | read 2026-09-25

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-25 12:08
