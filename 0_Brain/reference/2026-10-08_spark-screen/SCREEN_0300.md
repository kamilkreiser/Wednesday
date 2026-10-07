# KS screen for the Spark: 2026-10-08, 03:00 delta (0 briefs delivered; the one candidate, KS-1449, is already a held Spark PASS)

Written 2026-10-08 02:56:30 AEDT (shell `date`) by a Spark brief-writer sub-agent for Wednesday. Secuura only. Method: SCREEN_2300's (itself SCREEN_1520's instruments), the kit predicate (`spark-kit_2026-09-23/02_FOR_THE_COORDINATOR.md` §2), `spark/README.md`.

**Read-only on client systems:**
- Linear: GraphQL reads only. `LINEAR_API_KEY` came from the Blockchain `4_Credentials/.env` in a `set -a` subshell and was never printed.
- GitHub: REST GET only (open PRs and their files).
- Git under `!CODING/`: read verbs only (`ls-remote`, `status`). `git status --porcelain --untracked-files=no` on the Blockchain checkout reads 0 lines after the work (02:55:21).
- Every write verb ran in a `git clone --shared --no-checkout` copy under this session's scratchpad (`.../scratchpad/clone`). The tip object was already present in the shared store, so no fetch was needed. Strict-apply checks used `git apply --cached` against throwaway index files (`GIT_INDEX_FILE` under the scratchpad), with no working tree.
- No `round.sh` run: nothing was briefed (see BLUF 3).

**Not touched:** `spark/queue.md`, `night/queue.md`, `PAUSE_QUEUE`, tmux, mail, Linear writes, GitHub writes. No model round was run. Nothing was deleted. Nothing was created under `!CODING/`.

## BLUF

1. **Tip:** develop `eae08a3f441c9d9570061df560eefe146ad50d2d`. `ls-remote` read it at 02:51:43 and 02:55:21 AEDT, unchanged. It is the sha Wednesday read.
2. **Delta: 13 distinct tickets.** Created 5 + updated 12, with 4 in both, which matches Wednesday's counts. Positive control: KS-1449 is in both sets.
3. **Delivered: 0 briefs.** This is a valid result. Of the 7 tickets screened, 6 fail the predicate on an explicit clause. The seventh, **KS-1449**, passes it on its face, but its fix is **already a reviewed, held Spark PASS**:
   - The pass is `night/briefs/KS-591-nft-mint-upload-fee`. Its 10-05 round passed 7/7, and its `REVIEW.md` says "VERDICT: HOLD (ready to raise)". Golden hunk 2, `@@ -1119,6 +1119,7 @@`, inserts `      required: true,` after the upload body's `content:` line, which is `nft-certificate.openapi.ts:1121` at `eae08a3f`.
   - Briefing it again would duplicate held work on the same file and lines.
4. **The held work still applies at today's tip.** Two held passes are measured: `KS-591-nft-mint-upload-fee` and `KS-1364-nft-ipfs-pin-unpin-size` (10-05 PASS 7/7).
   - Each `golden.diff` and `openapi-yaml.companion.diff` passes `git apply --cached --check` at `eae08a3f` with rc 0, alone and stacked (all 4 rc 0). Control: a reversed apply of the KS-591 golden refuses, rc 1.
   - Stacked, they mark **10 of 10** nft-certificate request bodies `required: true`. At the tip it is 4 of 10.
   - So KS-1449's "Done when" box 1, and its "check whether sibling `nft` operations have the same omission" clause, are closed by raising these two passes. **Neither is in an open PR.**
5. **For Wednesday (owner calls, not acted on):**
   - (a) Raise the two held nft passes together. That closes KS-1449's spec half.
   - (b) **KS-1447** is unassigned (see the exclusions below).
   - (c) **KS-1448** is routed "Claude: security surface".

## How the delta was derived

Two separate GraphQL `issues(first:100)` queries, each paginated until `hasNextPage` was false, then unioned in Python. There is no top-level `or:`. Script: `scratchpad/q/lin.py`; output: `scratchpad/q/delta.json`.
- **Created set:** filter `team.key eq KS`, `createdAt gt 2026-10-07T12:00:00Z`. Result: 1 page, **5 nodes, 5 distinct**. They are KS-1445 to KS-1449.
- **Updated set:** filter `team.key eq KS`, `state.type in [backlog, unstarted]`, `updatedAt gt 2026-10-07T12:00:00Z`. Result: 1 page, **12 nodes, 12 distinct**.
- **In both sets:** KS-1446, 1447, 1448 and 1449. KS-1445 is created-only (Done).
- **Positive control:** KS-1449 is in the created set and in the updated set.
- **Union: 13.** KS-485, 492, 565, 593, 627, 752, 984, 1396, 1445, 1446, 1447, 1448, 1449.
- **Excluded before screening (6):**
  - Peter-assigned: KS-492, 984, 1396, 1445 (also Done) and 1446.
  - KS-1447 is unassigned and Peter-created, so it is held as an owner question.
- **Screened: 7.** KS-485, 565, 593, 627, 752, 1448 and 1449. Each was read at source, with its description where new and every comment created after 12:00Z (the `comments` field, filtered by `createdAt`).

## Verdict per ticket

| Ticket | Verdict · predicate clause |
|---|---|
| **KS-1449** POST /api/nft/ipfs/upload body not `required` | Passes on its face: one product file, fix shape spelled ("declare `requestBody.required: true` in the route's OpenAPI source"), in-process spec-render test pattern beside it, not auth, round 0. **NOT BRIEFED: duplicate of held work.** The exact hunk is in `KS-591-nft-mint-upload-fee` (HOLD, ready to raise). Its sibling clause is covered by `KS-1364-nft-ipfs-pin-unpin-size`. **Overlap with KS-1364:** yes, the same class. KS-1364 is the umbrella, In Progress (Kamil), and its table does not name this operation. KS-1449 is also KS-591's class (positive_data_acceptance), and the held pass "Refs KS-591". A raise of the held pass should add "Refs KS-1449". |
| **KS-1448** POST /api/notifications BOLA | **NOT: security/auth surface** (BOLA, cross-user write, in-app phishing). Also **decision**: "unless the caller is an admin or internal service (decide which)". **Routing: Claude, security surface.** Sites confirmed at the tip: `api-gateway/src/routes/notifications.ts:242` (`router.post('/', …)`) and `:244` (`const { userId, … } = req.body`). This file is also KS-1410's (live lane, R 14th). |
| KS-485 Security review plan/handover | **NOT: security surface**, unchanged. It has no new comment. Its updatedAt (14:53:46.654Z) matches KS-1448's creation (14:53:46.409Z), and KS-1448 is in its inverse relations. |
| KS-565 sweeps register (2 Peter comments) | **NOT: decision.** The 14:53Z append on `GET /api/kyc/microsoft/result/{sessionId}` says: "Either return `sessionId` … and add `completed` to the enum, or reshape the declared schema". Runtime and spec drift across 2 branches, and it is a KYC (identity) surface. The 12:04Z comment is recurrence only ("Nothing new needed"). |
| KS-593 not_a_server_error register (2 Peter comments) | **NOT: auth surface** (`services/auth/src/routes/wallet.ts`, `POST /api/auth/wallet/verify`, CIP-8). It is also **mechanism not established** ("I did not identify the exact throw site … Replay with `st replay xPmeIe`"), so it is measure-first. |
| KS-627 real wallet signature verification (1 Peter comment) | **NOT: auth/crypto surface** (CIP-8/COSE), unchanged. The comment is a baseline re-pointing with "nothing is asked of you". |
| KS-752 baseline gate unreachable (1 Peter comment) | **NOT: no runner / live stack**, unchanged. The comment is a data point with "nothing is asked of you". |

## Exclusions by reason

- **Peter's (assigned):** KS-492, KS-984, KS-1396, KS-1446.
- **Done:** KS-1445 (also Peter's).
- **Owner question for Wednesday:** KS-1447 is Peter-created and UNASSIGNED ("left unassigned as asked").
  - It asks for a systemTest-only Schemathesis guard, scoped to the `negative_data_rejection` check on `GET /api/users/admin/list` only (Kam's KS-592 2026-08-26 ruling, quoted verbatim in the source).
  - It also asks for:
    - a red-to-green test;
    - a test that the `offset=-1` 500s still fail `not_a_server_error`;
    - an update to `test_by_design_permissive.py`'s scope note;
    - retiring the `schemathesis-baseline.json` entry after a live sweep.
  - Not briefed per the commission. Note also that it is an admin-list surface, and box 5 needs a live sweep.
- **Security surface:** KS-1448, KS-485, KS-593, KS-627.
- **Decision:** KS-565 (and KS-1448).
- **No runner / live stack:** KS-752.
- **Duplicate of held Spark work:** KS-1449.
- **Live lane:** none of the 7 screened tickets' files fall in R 14th's set or PRs #1422/#1423. The exception is `notifications.ts` (KS-1448, already excluded as security). `nft-certificate.openapi.ts` is in no live lane.

## Collision census (for KS-1449)

- **Open PRs:** GitHub REST GET at ~02:53 AEDT: 24 open PRs, 121 file entries. **0 touch `nft-certificate.openapi.ts` or `docs/openapi/secuura-api.yaml`.** Positive control: the same census lists 2 nft-certificate paths, #1360 (`services/nft-certificate/package-lock.json`) and #649 (`services/nft-certificate/package.json`).
- **At the tip:** the body-flag parser (`scratchpad/q/bodies.py`) reads `nft-certificate.openapi.ts` at `eae08a3f`. There are 10 `registerPath` blocks with a body: 4 have `required: true` and 6 do not. The 6 are `/nft/mint` (block at `:844`), `/nft/ipfs/upload` (`:1113`), `/nft/ipfs/pin` (`:1140`), `/nft/ipfs/unpin` (`:1165`), `/nft/metadata/estimate-size` (`:1250`) and `PUT /nft/admin/platform-fee` (`:1279`).
  - Positive control: the 4 marked ones are the landed KS-1364 lines `:879`, `:904`, `:1067` and `:1095`.
  - On the index with both held passes stacked: 10 of 10 marked, 0 unmarked.
- **Upload body at the tip:** `:1120` is `    body: {` and `:1121` is `      content: { 'application/json': { schema: NftIpfsUploadRequestSchema } },`. The held golden's insertion point is unchanged.
- **Ledgers:**
  - `spark/done.md:12` is `KS-591-nft-mint-upload-fee` PASS (7/7), 2026-10-05 13:21:51.
  - `spark/done.md:22` is `KS-1364-nft-ipfs-pin-unpin-size` PASS (7/7), 2026-10-05 16:26:39.
  - No `READY_*` exists for either pass. The `READY_KS-591-*` files present are CUSTODY-1 and TENANT-1 only.
  - The 10-06 screen (`2026-10-06_spark-screen/SCREEN.md:103`) already caught a duplicate against this same held pass, for platform-fee.
  - KS-1449 has 0 rows in `spark/done.md` and `spark/queue.md`.
- **Held pass hashes (sha256/16, read only):** `KS-591-nft-mint-upload-fee/KS-591.md` is `97c965aed88e9bfe`, and its `golden.diff` is `0d4db30c1b350d1e`.

## Findings for Wednesday (none acted on)

1. **Two held nft passes have sat unraised since 10-05**, and they now have a third ticket waiting on them (KS-1449, alongside KS-591 and KS-1364). Both still strict-apply at `eae08a3f` and stack cleanly. The 10-05 review measured `npm run check:openapi` rc 0 with the companions, at its own tip `3ce8cd4026a6`; it was not re-run at `eae08a3f` (see UNMEASURED).
2. **KS-1449's runtime half** ("the pair stops firing, or is baselined") needs a live Schemathesis sweep after the raise. That is Peter's or systemTest's side, not Spark work.
3. **KS-1448 shares `notifications.ts` with the live KS-1410 payload (R 14th).** Whoever takes the BOLA fix should base it after R 14th's raise lands, to avoid a conflict.

## UNMEASURED

- **No `round.sh --dry-run` / `--control`** was run on the held passes at `eae08a3f`. Only `git apply --cached --check` was run, so neither the checker legs nor `check:openapi` were re-run at this tip.
- **Drift, measured (blob compare in the scratch clone):**
  - `nft-certificate.openapi.ts` is the **same blob** at `eae08a3f` as at each held brief's `Tip:` (`3ce8cd4026a6` for KS-591, `fe6daca343c1` for KS-1364).
  - `docs/openapi/secuura-api.yaml` **changed** since both tips: 87 insertions. Both companion diffs still apply (measured above).
  - Whether round.sh's STALE gate counts the YAML, which both briefs name only as do-not-touch, was not measured. Control: the instrument reads 42 files changed between `2c27ddfee` and `eae08a3f`, so it does detect change.
- **Whether a live seat is working KS-1364** right now was not checked beyond the commission's R 14th list and the open-PR census (neither names it).
- **Field-level history** of KS-485 (updated with no comment) was not read. Attributing that update to the KS-1448 link is by timestamp and relation only.
- **KS-1449's runtime claim** (a bodyless POST answers 400 `data Required`) was not reproduced. No live stack was used.
