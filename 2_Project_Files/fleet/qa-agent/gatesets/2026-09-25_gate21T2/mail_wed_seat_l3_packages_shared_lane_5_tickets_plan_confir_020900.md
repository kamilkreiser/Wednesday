SUBJECT: [Wednesday -> Secuura/Blockchain-D] Seat L3: packages/shared lane, 5 tickets, plan confirmation before first push
FROM: Wednesday <wednesday-agent@agentmail.to>
TO: ['secuura-blockchain@agentmail.to']
TS: 2026-09-25T02:09:00.678Z
MESSAGE_ID: <010001a0d652b94a-756771cd-716b-4aa4-999a-8d012b423730-000000@email.amazonses.com>
CAPTURED: 2026-09-25T03:45:34Z by the gate21T2 drafter, read-only by message id (key by name, never printed)
TEXT_SHA256: 6da286a1a2b9fb4191ac0c413d350f5288701e93412fbf9207ca5f9ebfb60923
# LAUNCH BRIEF: Seat L3, Secuura/Blockchain. The packages/shared lane. From Wednesday

## BLUF
You are **Seat L3**, one of four parallel BUILD seats (L1-L4). They run beside Seat B 25th on one checkout. Your lane is `packages/shared`: 5 tickets. Every change ends at READY FOR QA. You merge only on Wednesday's signed GO, and you deploy nothing. `packages/shared` is imported by every service, so run the dependent service suites your change can reach, not only this package's.
**Authority:** Kam, terminal, 2026-09-25, the parallel-seat grant, and the TESTED grant of 2026-09-11.
**Seat identity:** Seat L3. Worktrees `s-l3-*` (absolute). Branches `feature/ks-<key>-<slug>-l3-<tag>-1`. Record folder `5_Project_History/2026-09-25_seatL3/`. Subjects tagged `(Seat L3)`.

**Your cockpit pane is `Secuura/Blockchain-D`** (the inbox is shared: mail addressed to another seat is not yours; filter on `(Seat L3)`).

## YOUR FILES / NOT YOURS
- **YOURS:** `Blockchain/Dev/packages/shared/**`, EXCEPT the three files below.
- **NOT YOURS inside your family:**
  - `src/__tests__/ks860-test-listeners-bind-loopback.test.ts` (KS-1147, local-model candidate).
  - `src/__tests__/ks879-no-raw-control-bytes-repo-wide.test.ts` (KS-1140 GF-1, local-model candidate).
  - `src/__tests__/ks764-key-revoke-call-site-guard.test.ts` (Seat B 25th runs it against `startup-migrations.ts`).
  - `package.json`.
- **NOT YOURS elsewhere:**
  - L1: `services/originate/`, `docs/openapi/`.
  - L2: `services/security/`, `services/anchoring/`.
  - L4: `scripts/`, `systemTest/schemathesis/`.
  - Seat B 25th: `services/auth/`, `vc-issuer/`, `api-gateway/`, `scripts/audit/`.
  - Nobody's: every lockfile.
- No open PR touches `packages/shared` (measured).

## ITEM 0: PLAN CONFIRMATION BEFORE THE FIRST PUSH
1. Refuse the launcher pull. The only writes to the shared `.git` are `worktree add` for `s-l3-*`.
2. Re-measure the tip (`6ab9d5021e96…`). If develop moved, the diff decides.
3. Read every ticket's comments and merged commits, and state what REMAINS.
4. Send a QUESTION mail, topic `plan confirmation (Seat L3)`. It carries: launcher warnings verbatim; seat, pane and inbox filter; the residuals; tiers; scanner result; and whether KS-872 needs a dependency change. If it does, that is a STOP: `package.json` is off-limits. Proceed only on the ANSWER.

## THE QUEUE (easiest first; scope quoted)
1. **KS-1288** (Backlog, P3). *"Pin by **text** (the line's content, or a stable anchor) rather than by ordinal position, so an unrelated edit above the sites cannot red the suite. Where: `…/ks781-p3-3-body-parser-order.test.ts`, LEG D."* Tier 2.
2. **KS-1143 GF-2 only** (In Progress; #1212 `dd8f99cc7` closed GF-1). The ticket comment says: *"GF-1 is closed; GF-2 and the indirect-invocation false negative are not."* This is the same file as item 1, so land the two sequentially. The indirect-invocation false negative stays open on KS-1143 by Wednesday's ruling and is not in scope. Tier 2.
3. **KS-1181 residual** (#1179 `670f3f507` and `f93db9558` merged). *"Assert a hit or answered count (or `forwarded === false`) in the canary cells for non-forwarding handlers, with a 0-hit control."* Measure what remains. Tier 2.
4. **KS-1179 residual** (#1201 `b70512ca8` and `4d85ad928` merged). *"clear the DNS timer when the race rejects (F-6); bring the `blocked` and `timeoutMs` docblocks up to date (F-4, F-5)."* File `src/security/ssrf-guard.ts`. Tier 1 (SSRF guard).
5. **KS-872** (Backlog, P3). *"Either import `JsonWebKey` from where `@types/node` 26.x now exposes it, or declare the shape locally"*. Acceptance: *"`npx tsc -p packages/shared --noEmit` exits 0 with a planted-error control"*. The live site is `src/crypto/jwks.ts:129`. Measure first whether the tsc run is still red. Tier 1 (crypto).
- **Excluded:**
  - KS-1216: runtime images and audit gates.
  - KS-846: `package.json main`.
  - KS-1141: decision.
  - KS-1226: under `systemTest/performance`.

## GATE AND MERGE
- READY FOR QA carries the five STANDING_LINES artefacts.
- Tiers follow the 2026-09-05 tier rule; the two-NO-GO cap applies.
- Merge one at a time, only on a DKIM-passing GO naming each head. Dry run first, sha-pinned, re-predicted. Tickets stay In Progress (§5f).
- `Refs` with linkKind `contributes`, never a closing word.
- `packages/shared` runs `vitest run`. Take baselines BARE and SERIAL, and report `bare N / patched N+k` plus tsc.

## HOLDS
- No deploy and no demo. Nothing to Peter or Stuart beyond facts-only ticket comments.
- Never delete; quarantine. No `--no-verify`, `--admin` or force-push.
- Fetch develop plus `cat-file -t` before wrap. Signature classes pause for Kam. File no tickets unless an ANSWER says so.
- Restore modes after `git apply` and assert `test -x .githooks/pre-push`.
- 422 on self-approval means STOP. Hand over HOLDING at ctx ~80.

## PARALLEL-SEAT STANDING BLOCK (2026-09-22; five seats on one checkout: B 25th, L1, L2, L3, L4)
- **PUSH-WINDOW LOCK:** one SHARED `mkdir` lock outside every worktree. RULED by Wednesday: the ONE shared lock for all five seats is `worktrees/.push-lock-21/` (Seat B 25th is told the same). Holder file plus 60-s heartbeat. Take it before snapshot and release it after verify; the holder's rmdir is the only delete. No ref write while another seat holds it. Wait 20 minutes, then STOP and mail. A stale lock is reported, never removed. Built into the push tool.
- **ATTRIBUTION BY NAMESPACE:** a foreign diff is another seat's only when both hold: the name matches its namespace (`s-b25-*`/`-r21-`, `s-l1-*`/`-l1-`, `s-l2-*`/`-l2-`, `s-l4-*`/`-l4-`) AND origin holds your branch at your sha. Otherwise STOP.
- **BOARD GUARD:** attribute only when all four hold: a project PR; head ref `feature/ks-<same key>-…`; the board login in the round; addition-only. The only tolerated state change is the bot's Backlog → In Progress walk on PR open.
- **PROCESS NAMESPACE:** kill by ancestry or by port plus cwd, never by basename. Put `-l3` in argv.
- **Test by its handle:** name your mine-versus-theirs instrument for the inbox, `.git`, the process table, the board and the machine's load.

## RULED BY KAM, NOT YET IN AN ARTEFACT (Secuura, this lane)
- None relevant.

## VERIFIED BEFORE SENDING
PROVENANCE:
- origin develop `6ab9d5021e96ea1481cb6c6ff2d6d33b414aecb7` | `git ls-remote origin refs/heads/develop` | read 2026-09-25
- KS-1143 and KS-1288 share `ks781-p3-3-body-parser-order.test.ts` (the only `routerParserAnalysis` file) | `git grep -l` at the tip | read 2026-09-25
- `JsonWebKey` still at `src/crypto/jwks.ts:129`; ks860 `:440` and ks879 `:123` unchanged | `git grep -n` at the tip | read 2026-09-25
- merged commits #1179, #1201, #1212 | `git log 6ab9d5021e96` | read 2026-09-25
- ticket states, scope sentences, KS-1143 comment | Linear GraphQL read-only, Secuura key | read 2026-09-25
- 0 open PRs touch `packages/shared` | GitHub REST `pulls` + `pulls/<n>/files` (18 PRs) | read 2026-09-25

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-25 12:08
