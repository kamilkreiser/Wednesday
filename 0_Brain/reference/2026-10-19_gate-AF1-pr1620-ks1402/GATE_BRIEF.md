# Gate brief: GATE AF1 = PR #1620 (KS-1402 invited-stub holder), Opus, tier 1, round 1 of 2

Commissioned by Wednesday after Seat C 26th's READY FOR GATE of 08:52Z. The author's CLAIM is beside this brief: `C26_READY_0852Z.txt`. Secuura only.

**Project:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` is READ ONLY (ls-remote, show, diff, cat-file, log). Every write verb runs in your own clone in your scratch: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/dd32393e-b87e-4d51-ac65-b22e5897a2c1/scratchpad/af1/`.

**What it is:**
- **The rulings:** Kam ruled (card `secuura-ks1402-who-creates-the-holder-1019` = a): *"K creates an invited stub user on transfer"*. The card adds: as certifications/issue does for holderEmail; a tier-1 gate (a user row from a connector call: the tenant boundary and PII proved); S changes nothing. Wednesday approved C's design A at 19:1x.
- **The transfer path:** on the transfer-custody EMAIL path's previous 404 branch only, originate calls auth `POST /api/users/stub` with the caller's Authorization forwarded. The S key is admitted by `certifications:write` (`hasUsersStubScope`, auth `routes/users.ts:250-259`). Originate then RE-READS the returned userId through its own bound tenant predicate and refuses a foreign-tenant answer (no-disclosure 404). The custody event and owner flip follow.
- **Failure arms:** timeout gives 503, any other failure 502, both before the transaction. A cross-tenant email stays 404. An unknown `newHolderId` stays 404.
- **No auth change, no migration.**
- **Re-pinned cells:** 19 existing cells (ks739 ×13, ks1402 ×5, ks697 ×1), with the status moved 404 -> 502 in their no-auth-upstream harnesses, and titles stating what each now proves. Every `lookupCalls`, writes-nothing and anchorCalls assertion is meant to be byte-unchanged. The KINTSUGI parity cell is re-pinned and renamed.
- **Heads:** #1620 head `dbb00e65dfb04abf6886237a76aaf3b2860ac3cb`; develop `66faac9aebc3aaa6e2ee453b004295345ff88cb8` (#1617 landed; #1618 may land during your run, so re-read). The author predicts landing tree `30f298e098bd` on 66faac9aebc3.

## Questions (each with its instrument; name what you did NOT run)
1. **Tenant boundary:**
   - Is the re-read through originate's bound predicate the authority, and can any path use the returned id without it (logs, events, the custody row)?
   - Run the TENANT PROOF cell, then plant a mutant of your own that skips the re-read on one branch only.
   - Is auth's `/stub` itself tenant-pinned from the forwarded JWT, with `EMAIL_RESERVED_ELSEWHERE` giving 404 (`userRepo.ts:753-793`)? Read it; you cannot run auth here unless you can build it, so say which.
2. **PII:** what exactly does the stub row hold? Read `createInvitedStub`. Does originate log or echo the email anywhere new (logger lines, the event payload, error bodies)?
3. **The 19 re-pinned cells + KINTSUGI:** read EVERY old and new assertion. The only permitted change is the status expectation (and titles/comments). Diff each test file against develop and list any changed line that is not a status, title or comment. **Any changed `lookupCalls` / `custodyInsertCount` / `anchorCalls` / writes-nothing line is a blocker.**
4. **Admission by `certifications:write`:**
   - confirm S's minted scope set carries it (`api-gateway routes/platform.ts:513-523`);
   - confirm there is a cell pinning that S's key reaches `/stub` via this path, the condition Wednesday set;
   - KS-1653 (the scope-gate tidy-up) is filed: check it exists by the PR body's claim only, not on Linear.
5. **Race and failure arms:**
   - the concurrent first-transfer race retry;
   - timeout 503 and other 502, with no custody row and no owner flip;
   - repeat transfer to the same email: no second user row (via the local resolve).
6. **Red-first, mutants, landing:**
   - the new suite is 12/12 in both tenancy modes (claim), red-first 9/3;
   - the author's 4 mutants, plus one of yours;
   - merge-tree on the LIVE develop (re-read at start and before the verdict);
   - originate unit suite 1481/1481 on the landing tree;
   - the new integration suite in both modes on scratch PostgreSQL (port 55410-55419, `docker/init/*` + migrations incl. 052);
   - tsc including tests;
   - the three-dot list is exactly the PR's 6 files.
   Build `packages/shared` first; Prisma via `npm run generate --workspace=services/originate`.

**Verdict file:** `verdict.md` in this folder.
- First line: `VERDICT: <GO|GO WITH NOTE|NO GO> at head dbb00e65dfb0... (tier 1, round 1 of 2; landing tree <sha> on develop <sha>; N blockers, M notes)`.
- Last line: the sha256 of `sed '1d;$d' verdict.md | shasum -a 256`.

**Rules:**
- Findings only: no fixes, no GitHub or Linear writes, nothing under `!CODING`.
- No `cd`, no `rm`, no stderr to /dev/null, no Docker.
- Every zero gets a positive control.
- The shell is zsh: no PIPESTATUS.
