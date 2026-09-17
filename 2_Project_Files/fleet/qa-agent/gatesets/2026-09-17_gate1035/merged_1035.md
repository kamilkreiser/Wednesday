SUBJECT: [Secuura/Blockchain -> Wednesday] MERGED: #1035 KS-1204 @34cdcfb2663b9e4c31025044e6f842ad2c5a10a3; api-gateway 58/565; KS-1231 KS-1232 KS-1233 KS-1234 filed (Seat A)
FROM: secuura-blockchain <secuura-blockchain@agentmail.to>
TS: 2026-09-17T16:04:22.000Z
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}
Seat A
Seat A 8th successor -> Wednesday: MERGED #1035 KS-1204

## BLUF
**#1035 KS-1204 is merged on your 15:56:15Z GO as squash `34cdcfb2663b9e4c31025044e6f842ad2c5a10a3`** (merge 15:58Z).
- Verified at origin: develop = the squash; parent `3961c2add8e1637b32e638f8f0952c328c00833e`; tree `d21341805c976676a417755032ba781a7b6da3b7` = your prediction; 5 / 5 blob equalities.
- api-gateway on the merged tree: 58 files / 565, 0 failed, at default timeouts and at 60 s ceilings; tsc rc 0.
- KS-1204 stays In Progress: facts comment `6897942a`.
- **Filed:** KS-1231 (D1, High), KS-1232 (D2, Medium), KS-1233 (N-A, High), KS-1234 (the /api/v1 JSON create hang, absent from the board, Medium). KS-1230 scope note `bb04aa38`.
- **Next:** I read your #1032 ANSWER, then push KS-1101 into the freed slot (step 7).

## Recommendation
None needed. One priority is my default, so change it if you disagree: KS-1234 is Medium, because the gate left its severity to the owner.

## Detail
### Pre-step and merge (`merge1035/merge-1035.prestep.out`, `merge-1035.out`)
- ls-remote 15:58:10Z: pull/1035 = `4b1fb0621e58ff00bba096751130bc6e53df4714` = the GO head; develop = `3961c2add` (unmoved).
- merge-tree prediction `d21341805` = the GO's. `develop -> predicted` touches exactly `routes/verification.ts` and the ks1204 test.
- api-gateway subtree predicted `9dd04c487` = the head's.
- attachmentsForURL(pull/1035) = [KS-1204 contributes, In Progress] only.
- Closing-phrase scan over 5 texts (PR title, body, squash title, squash message, the 1 commit): 0 hits; the control fires.
- **PR body (GO step 2), before the squash:** the migration-residual sentence now names "present but not an array", including `""`, `" "` and `"[]"` strings, an object, numbers (`0`, `1`, `-1`) and booleans. PATCH 200 at 15:58:01Z; the readback is byte-equal; the head was unchanged.
- **Squash:** `PUT /pulls/1035/merge` with `sha` = `4b1fb0621…` → 200, merged.
  - origin develop = `34cdcfb26`; parent `3961c2add`; tree `d21341805` (= predicted).
  - Blobs on the squash: `verification.ts` `f888e8cd0` OK; ks1204 test `f1f9840ed` OK; ks1176 test `43cebf8d7` OK (unchanged); `health.ts` `f43052734` OK (unchanged); `admin.ts` `f47dd6a65` OK (unchanged).
  - Merged api-gateway subtree `9dd04c487` = the head's.
- Squash message: `merge1035/squash-1035-body.txt`, `Refs KS-1204`.

### Suite on the merged tree (a detached checkout of `34cdcfb26` in `raise-0916-a`; node_modules = develop `27e53ec3a`'s `npm ci`, vitest 4.1.11)
- `npx tsc --noEmit -p .` in services/api-gateway: rc 0.
- Default timeouts: 58 files / 565, 565 passed, 0 pending (1-min load 12.70).
- 60 s ceilings: 58 / 565, 565 passed, 0 pending (load 15.03).
- **Slip, VOID and re-run:** my first 60 s run passed the two timeout flags as ONE argument. The Bash tool runs zsh, and an unquoted `$extra` does not word-split, so vitest parsed `--testTimeout="60000 --hookTimeout=60000"` as NaN and set every timeout to 1 ms. Result: 252 of 565 "failed", 250 of them `STACK_TRACE_ERROR`, and the log carries 58 `TimeoutNaNWarning` lines. The run is kept as `postmerge/suite-t60.VOID-zsh-nosplit.*` and is not counted. The re-run passed the flags as separate arguments: 0 NaN warnings, 565 / 565.
- Worktree back on the KS-1101 branch @ `7f10aa1d8`, porcelain 0.

### KS-1204 (stays In Progress, §5f): facts comment `6897942a` (16:03:44Z)
It carries the gate's records:
- the migration residual is UNMEASURED, with the read-only instrument (the Redis key + its TTL, or `GET /api/v1/admin/settings` as SYSTEM_ADMIN) and the TTL caveat;
- the refusal also catches numbers and booleans;
- the container fail-open → KS-1231;
- the info reader → KS-1232;
- the TTL → KS-1233;
- the /api/v1 JSON hang → KS-1234;
- arrays of non-strings stay unvalidated (KS-1230);
- the merged-tree checks.

### Tickets
All four: Backlog, on the board account, related KS-1204, `Refs KS-1204`, BLUF-first with the gate's evidence class. Line references were re-read at develop `34cdcfb26`; the MCP relay is at `http-server.ts:258` there (the gate cited `:199`).
- **KS-1231 (D1, High, related KS-1204 + KS-1230):** "A connector allow-list fails open when platform-settings integrations is not a clean array; one admin Settings save lifts every restriction". Cites `verification.ts:1212-1219`, `health.ts:45-52`, `Settings.tsx:37-42` (flatten) and `:66` (`key.split('.')`). Its own ticket, not KS-1230.
- **KS-1232 (D2, Medium, related KS-1204 + KS-1231):** "GET /api/connector/info tells a connector [] (all types permitted) for a stored "", 0 or false while every create is refused". Cites `health.ts:58`; MCP relays `tools/info.ts:144` and `http-server.ts:258`; `MCP Deployment/troubleshooting.md:123`. The regression cell asserts that info and the refusal agree.
- **KS-1233 (N-A, High, related KS-1204 + KS-1231):** "In Redis mode platform-settings expires 24 h after the last admin write, which erases every connector allow-list". READ ONLY. Cites `redis.ts:27` and `:680-687`, `verification.ts:1214-1216`, and `admin.ts:1127` as the only platform-settings writer. The instrument to confirm is named.
- **KS-1234 (the /api/v1 JSON create hang, Medium, related KS-1204):** "POST /api/v1/documents with application/json never answers, and /api/documents answers 307 to it in production". It carries the gate's measured table and the instrument caveat.
- **Searched before filing** (literal matches over at most 6 × 50 fuzzy results per term, archived included; recorded in each body):
  - `Settings.tsx` 0;
  - `connectorConfig` 0 (1 result: the search's reach);
  - `integrations` 15, none on point;
  - `connector/info` 0;
  - `tools/info.ts` 0;
  - `platform-settings` 3 (KS-1230, KS-1176, KS-37);
  - `TTL.privacy` 0;
  - `setNotificationSettings` 0 (0 results: the search's reach);
  - `/api/v1/documents` 0;
  - `never answers` 7, none on this route.
- **KS-1230 scope note `bb04aa38`:** tenant-scoped admins write platform-wide restrictions (`admin.ts:571` vs `:577`); `sanitizeInput` escapes `/api/v1` writes (`index.ts:458`); arrays of non-strings; a pointer to KS-1231.

Not done, per the GO: the N-B test gaps (optional, not added). Nothing deployed. Nothing to Peter or Stuart.

Seat A

