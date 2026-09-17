SUBJECT: [Secuura/Blockchain -> Wednesday] MERGED: #1026 KS-839 @75ad0e55c6335a5f34f6d0b74dfe00b334b2eb2e; F-10 KS-1219, F-4 KS-1220
TS: 2026-09-17T10:59:20.000Z
AUTH: {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'}
Seat A

## BLUF
MERGED: #1026 KS-839 → develop `75ad0e55c6335a5f34f6d0b74dfe00b334b2eb2e` (10:58:03Z), on your 10:51:35Z GO. Verified at origin: parent = the gated develop `20ab16f9a`; tree `bad1cbf5f` = your prediction; blobs `oauth.ts` `8995edec6` and ks839 test `7853f210e` equal; **auth on the merged tree 64 files / 762 tests, all pass**, tsc rc 0. KS-839 stays In Progress. Facts comment `ac3cf66c-3396-4ff3-ab6d-194997fa7020`. **Tickets: F-10 → KS-1219, F-4 → KS-1220** (both Backlog, Low, related KS-839, not built).

## Recommendation
No action needed. Next: the KS-1180-P1 PR at `cd3580e1f` and READY (tier 2), per your 10:57:09Z ruling. After it, the open PRs are #1028 and KS-1180-P1, so one slot is free: KS-1213 is next to push, with develop `75ad0e55c` merged in first.

## Detail
- **Pre-step** (`5_Project_History/2026-09-17_seatA-6th/merges/merge-1026.out`):
  - ls-remote develop `20ab16f9a` (= gated), pull/1026/head `df97c0def` (= GO); PR open, mergeable true / `unstable`;
  - `merge-tree` rc 0 → `bad1cbf5f` (== the GO's prediction); predicted blobs OK; develop → predicted = exactly the 2 PR files;
  - `attachmentsForURL(pull/1026)` = [KS-839 `contributes` In Progress];
  - closing-phrase scan over 9 texts (PR title, body, squash title and message, 5 commit messages) = 0; control fires.
- **Squash:** `PUT /pulls/1026/merge`, squash, `sha` pin `df97c0def…` → 200, `75ad0e55c`. Title `KS-839: an OAuth app allow-list holding the wildcard, exact or padded, grants nothing (#1026)`, body `merges/squash-1026-body.txt`, `Refs KS-839`.
- **At origin:** develop == squash; parent `20ab16f9a`; tree `bad1cbf5f`; both merged blobs OK. The merged auth subtree `8bbbe53e1` ≠ the head's `55006066c`, as expected (develop carries #1018), so the suite was re-measured.
  - Instrument: a detached checkout of `75ad0e55c` in my own worktree `raise-0916-a` (porcelain 0 before and after), `npx vitest run` in `services/auth` → 64 / 762, 0 failed, 0 pending; `tsc --noEmit -p .` rc 0; switched back to the KS-1180-P1 branch at `cd3580e1f`.
- **KS-839:** In Progress (completedAt null) before and after.
- **Comment `ac3cf66c`** (10:58:51Z; read back 5 / 5 anchors; body corrected at 10:59:01Z by `commentUpdate`, because I first wrote the merge time as "~11:00Z" and the squash commit reads 20:58:03 AEST):
  - the merge and the property (named → 400 `invalid_scope`, omitted → empty grant, token `[]`, gateway 403), both rounds;
  - the gate's records: 0 / 432 minted tokens with `*` (develop 172); 0 leaks in 18,437,344 checks over every code point (develop 27,157); look-alikes literal; 26 separators refused; consent round trip and refresh re-mint `[]`; `['openid','*']` refused per option E;
  - open items one line each: F-4 → KS-1220; F-5 relayed, not ticketed; F-7 the contract text at `auth.openapi.ts:2553` / `:2672`, owed after #922; F-8 `documents:*` 403 vs `hasScope` true, pre-existing; F-9 → KS-1210; F-10 → KS-1219.
- **KS-1219 (F-10)**, Minor, pre-existing: `/api/oauth/authorize` 500 `server_error` on an array-valued `scope`. Cause re-read at develop `20ab16f9a`: GET `routes/oauth.ts:473-478` casts `req.query as Record<string, string>`, and `parseScopeString` (`services/oauth.ts:357-360`) calls `.split` on the array. POST (`:619`) was not re-read beyond the gate's measurement. Searched: `server_error` 47 (the Schemathesis family; the one authorize hit, KS-283, is malformed Unicode, Done), `array-valued` 2 unrelated, `as Record<string, string>` 0, `invalid_scope` 3, `parseScopeString` 0.
- **KS-1220 (F-4)**, test-only: non-ASCII `\s` carriers (` *`, `\v*`, `　*`) each `[]`, with the G-SECOND-REGEX tamper as the regression proof. Searched: `parseScopeString` 0, `ks839` 1 (KS-839), `invalid_scope` 3.

