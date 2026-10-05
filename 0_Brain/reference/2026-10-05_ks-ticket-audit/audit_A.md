# KS audit — partition A (auditor A, 2026-10-05)

**Partition:** not-archived KS tickets in In Progress / In Review / Blocked = **253** (234 + 14 + 5, matches expected) + not-archived Done/Canceled = **43** (all Done, 0 Canceled). **296 rows** in `audit_A.tsv`. Snapshot `ks_all_2026-10-05T0205Z.json`; code read at develop `3ce8cd4026a6` (fetched into scratch; the local checkout's origin/develop was older, `060bd30`).

## BLUF

- **Hypothesis "most In Progress tickets have a merged fixing PR" — TRUE for the PR, HALF-TRUE for "open only for the sweep".** 222 of 234 In Progress have an attached PR with GitHub `merged_at` set. Control: all 398 merged PRs in the partition have a merge commit that is an ancestor of develop `3ce8cd` (0 exceptions). But only **66** are sweep-only runtime fixes, plus **26** tooling tickets with a merged PR and no recorded residue (§5f does not apply to them, so they could close). About **106** of the 222 have a merged *partial* PR: a named residue is still open, or the merged PR is a tagged sub-scope.
- **The 31 Oct path is a deploy plus a sweep, not more code.** Of the 56 open rows on the critical path, 32 are MERGED-AWAITING-SWEEP. The last kintsugi record is develop `6ab9d50` on 09-23 (KS-601), so later merges are probably not deployed anywhere.
- **The board is mostly test-of-test work.** In the open partition, 124 of 253 rows are TEST-OR-TOOLING (harness, guards, gate records, docs, preflight). 104 of those are P3 or P4.
- **Archive: 30 yes** (29 Done tickets that are kamil-only, plus KS-763 already fixed), **14 ASK** (Done tickets that Peter or Stuart created or are assigned to), 0 cascades (no archive candidate has children).

## Counts per class

| class | In Progress | In Review | Blocked | open total | Done (43) |
|---|---|---|---|---|---|
| TEST-OR-TOOLING | 117 | 7 | 0 | 124 | – |
| MERGED-AWAITING-SWEEP | 66 | 0 | 0 | 66 | – |
| GENUINE-DEFECT | 22 | 0 | 0 | 22 | – |
| GENUINE-HARDENING | 20 | 0 | 1 | 21 | 1 (KS-1397, closed by ruling) |
| NEEDS-HUMAN | 5 | 6 | 4 | 15 | – |
| UNVERIFIED | 3 | 1 | 0 | 4 | 1 (KS-1362) |
| ALREADY-FIXED | 1 | 0 | 0 | 1 | 41 |
| DUPLICATE / NOT-GENUINE | 0 | 0 | 0 | 0 | – |

(A row-level count is in the TSV. DUPLICATE and NOT-GENUINE are 0 because the discipline forbids assigning them from a title, and no deep read proved one. Candidates are listed under "Could not verify".)

**PR split, measured with the GitHub REST `merged_at` field on attachment URLs:** In Progress has 222 merged, 5 open, 5 closed-unmerged and 2 with no PR. In Review has 9 merged and 5 open. Blocked has 4 merged and 1 with no PR (one more PR is cited only in a comment, and it is merged).
**Staleness:** 62 of 234 In Progress tickets have had no comment or state change for more than 14 days (8 for more than 21 days). 46 In Progress tickets have zero comments. 54 were moved to In Progress on one day (09-25) and 36 on 09-21: these are bulk moves, not work starting.

## Top 10 genuine defects by risk to "stable by 31 Oct"
1. **KS-801**: the gateway path predicates are case-sensitive, so `/API/…` skips them. The line is still present at `services/api-gateway/src/middleware/contentType.ts:119` (develop 3ce8cd).
2. **KS-806**: the wallet synthetic email is built from `walletAddress.slice(0,8)`, so wallet identities collide. The line is still present at `services/auth/src/routes/wallet.ts:200`.
3. **KS-695**: the K-side connector-scoped org erasure route is missing. `erase-connector` gets 0 hits under `Blockchain/` (the control `subjects:erase` is found at `platform.ts:488`), and Platform-S already calls the route.
4. **KS-1233**: in Redis mode, platform-settings expires, which erases connector allow-lists. The fail-open class remains on other triggers, and a deploy action is owed (from the agent comment).
5. **KS-1213**: derived-document writers relabel the served type. The L03 legacy residual is still open (agent comment).
6. **KS-1194**: the MFA auto-approve returns 200 when the level was never persisted (part 2 is open).
7. **KS-968** (MAJOR): the platform-admin seed throws 23505 and the error is swallowed. The merged PR #905 "closes nothing" on this ticket.
8. **KS-1334**: `err.message` leaks into 500 bodies. The fifth site is still open.
9. **KS-745**: the audit export calls a route the security service does not have, so it returns 404.
10. **KS-1018**: verification-store reads swallow DB errors. Item 3 (the in-memory fallback) is open and needs a decision.

**Also on the path, fixed on develop but not deployed or swept (MERGED-AWAITING-SWEEP):**
- KS-1404: an unsigned timestamp token verified as valid.
- KS-1402: every Platform-S transfer-custody call got a 401.
- KS-1054: a fresh database fails open on RLS until its second boot.
- KS-1231: a routine admin Settings save flipped a restricted connector to unrestricted. #1171 has since merged, but the Settings page still produces the bad data.
- KS-1028: erasure fan-out was skipped after the crypto-shred.
- KS-1187: an absolute-form request target bypassed the erasure door.
- KS-1370, KS-1352, KS-1375: revoked keys and credentials still verified.

**Fuses (push gate):** `scripts/audit/audit-baseline.json` has 3 rows expiring 2026-10-15 and 4 rows expiring 2026-10-31: react-router (KS-528), deepmerge-ts (KS-664) and braces, which has no upstream fix (KS-1403). The mobile tree exclusion lapses on 2026-10-19 (KS-769, 81 advisories, 2 critical). **KS-1380:** revert PR #1360 is still OPEN. Merging it would make develop fail a clean build again (Peter and Kam need to decide).

## Could not verify
- **Scope closure for the 26 "close candidate" tooling rows.** I only know that the merged PR names the ticket and that no residue was recorded. A control sample of 7 showed that merged PR titles often carry sub-scope tags (`KS-910 LEGCOMMENT`, `KS-1036 item3`, `KS-1156 R-C2`), and KS-910's real ask was a decision. So I did not mark these ALREADY-FIXED.
- **Residue claims for about 106 merged-partial rows.** These come from the agents' own comments (the last 3 comments, matched by regex and then reviewed by hand for false positives). I did not re-read them at develop. Only 7 rows were read at file:line (KS-801, KS-806, KS-695, KS-763, KS-729, KS-530, KS-1404), plus baseline expiries and KS-755.
- **Nothing was checked live.** Every MERGED-AWAITING-SWEEP row depends on a deployed stack.
- **5 `Secuura/platform-s` PR links return 404** with this GH_TOKEN (no access).
- **DUPLICATE and NOT-GENUINE candidates, not settled:**
  - KS-1172/KS-1173 overlap (the same PR #1059; 1173 adds `certified`).
  - The gate-record tickets KS-1152, KS-1153, KS-1156, KS-1158 and KS-1159 are agent QA records filed as tickets.
  - KS-1036 and KS-1035 are about the board and merge process.
- **The four UNVERIFIED rows:**
  - KS-946: the re-price to P3 needs Kam's confirmation before it can close.
  - KS-869: its stated blocker, #880, has since merged.
  - KS-966: comments say items 3 and 4 are closed.
  - KS-1084: unmeasured cross-tenant effect, labelled P0.

## Method and controls
- **Linear data:** for each ticket I fetched the description, `comments(first:50)` sorted client-side, attachments, relations, children and `history(first:50)`, one ticket per query, read-only.
- **GitHub data:** GET `/repos/{repo}/pulls/{n}` for every Secuura PR in the attachments, descriptions or comments (427 PRs).
- **Controls:**
  - Every merged PR's merge commit was checked as an ancestor of 3ce8cd with `git merge-base --is-ancestor`: 398 of 398.
  - I searched for revert PRs and found one open (#1360).
  - Every grep zero was paired with a found control: `subjects:erase`; `GHSA-vfj7` found while `4mjr`/`x5fp`/`mwp4`/`frvp` returned 0.
- **Definitions:**
  - "Idle" is the time since the latest comment or state change, against the snapshot time 02:05Z.
  - ARCHIVE is `yes` only for Done tickets, or ALREADY-FIXED rows with a proving cite. Any ticket created by or assigned to Peter or Stuart gets ASK.
  - "Critical path" is a heuristic: P1–P2 product or security, push-gate fuses, and named Platform-S blockers. Tooling rows are `no`.
- Scratch (scripts and raw JSON): `scratchpad/ksaudit/A/`.
