SUBJECT: [Secuura/Blockchain -> Wednesday] MERGED: #1023 KS-1207 @efaaa6034f036dd9538ee35b189217b1d08b90a9; follow-up KS-1215
TS: 2026-09-17T09:13:49.000Z
AUTH: {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'}
Seat A

## BLUF
MERGED: **#1023 KS-1207 → `efaaa6034f036dd9538ee35b189217b1d08b90a9`** on your 09:07:27Z GO (spf/dkim/dmarc pass), after #1024's receipt. Verified at origin: one parent `ee40d3099` (Seat B's #1022 hono merge, re-read first), tree `38ea11907` = my read-only prediction at that develop, two files, both blob targets equal. api-gateway 56 / 550 and shared 44 / 851 at the merge. KS-1207 stays In Progress; facts comment `39b00f27-70a0-4077-ae46-5d32036e7070`. **Follow-up filed: KS-1215** (N-1 + F-1). Your 09:11:25Z ANSWER is received: next I take KS-839 into the freed slot, and build KS-1213 locally.

## Recommendation
Please queue KS-1215. Open PRs of this lineage are now #1018 only, so KS-839 goes first (develop `efaaa6034` merged in, push, PR, READY), then KS-744 as the second slot. KS-1213 is built locally in between (write-side refuse, measure first).

## Detail
- **Pre-step** (09:11:12Z):
  - Develop had moved to `ee40d3099` (Seat B, KS-1211 hono: root lock, mcp-server + originate locks, audit baseline). `git diff --name-only 81ee4b729 ee40d3099` has 0 files under `services/api-gateway` or `packages/shared`, so no STOP. The root lock diff is version fields only; nothing in api-gateway or shared imports hono (0 files). The worktree install (hono 4.13.0) therefore does not affect the gateway or shared suites.
  - `git merge-tree --write-tree ee40d3099 2f74491eb` = `38ea1190744edd675c500032b67f851cb87e9094`. It differs from the gate's `985e615cc` exactly in #1024's two originate files plus #1022's four files. `auth.ts` `b8fce678a` and the ks1207 test `f56bd48b9` = targets (control: develop's `auth.ts` `7c985bdce`).
  - linkKinds [KS-1207 contributes]. Closing-phrase scan of the title, body, 3 commits, 1 + 0 comments and my squash body: 0.
  - **GitHub `mergeable` read null / `unknown`** (the base had just moved). I merged on the content predictions plus the `sha` pin, and verified by tree after (below).
- **Merge:** REST squash with the `sha` pin, 09:11:18Z → http 200 at 09:11:22Z. Title = PR title + ` (#1023)`. Body = the fix commit's message, with two prose ticket mentions (the old session-revocation ticket and the residual's ticket) reworded out so the develop commit names only KS-1207; `Refs KS-1207.`, Co-Authored-By.
- **Verified:** ls-remote develop = `efaaa6034`; parent `ee40d3099599…`; **tree `38ea11907` = prediction**. Files vs `ee40d3099`: ks1207 test +185, `auth.ts` +14 −10. Blobs `b8fce678a` / `f56bd48b9`. Message ids: KS-1207 only; closing hits 0. Worktree detached at the merge: api-gateway **56 files / 550, 0 failed, 0 pending**; shared **44 / 851**; tsc rc 0; porcelain 0.
- **KS-1207:** In Progress (last state change 08:01:36Z at PR open; the merge moved nothing).
- **KS-1207 comment `39b00f27`:** the squash sha; CLOSED on all 8 optional mounts (0 / 112 rows reach the upstream vs 79 at develop; 1,255 cells per tree unchanged outside the intended classes); R-1 (the 3 unnamed mounts' intended change); R-2 (could-not-validate → the Bearer principal, up to 30 s after recovery via the 5xx negative cache); R-4 (the required-mount "Invalid API key" mislabel during an outage, pre-existing); R-5 (a bad-signature Bearer forwarded anonymous on optional proxy mounts, pre-existing); the KS-736 residual not this PR's; "Schemathesis / Akto NOT REQUIRED for this merge, REQUIRED before this ticket can close"; KS-1215; §5f.
- **KS-1215** (Backlog, High, board account, related KS-1207): "api-gateway: a revoked-session JWT plus a VALID key whose connector-token exchange fails is forwarded with the revoked Bearer and no session check (plus the fall-through cells no suite has)".
  - N-1: the repro, 10 mounts incl. required, the principal split with a live JWT, the three failure paths read at `internal.ts:33-87`, inducement NOT established, blast radius, the unratified fix shape (delete the header or refuse) and the regression test.
  - F-1: the five 0-red properties and the cells.
  - `/api/batch/*` named as an UNMEASURED question; KS-736 and KS-1198 named as related, not widened. Not built.
  - **Searched first:** `getConnectorBearer` 1 (KS-739, unrelated); `connector-token` 6 (KS-1198, KS-1205, KS-695, KS-1197, KS-1195, KS-1196, none on exchange failure); `exchange failure` 1 (KS-739); `left unset` 3 (unrelated).
- §5f Sunday sweep adds KS-1207 and KS-1202.

