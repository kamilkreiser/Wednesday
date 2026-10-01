# [Secuura/Blockchain -> Wednesday] READY FOR QA (Seat B 52nd): #1365 (KS-1364) head bf277eead26897bb648c801f92308681dbdaffdc - push rc 0, preflight 12/15 ran 3 SKIPPED nothing failed, suites 38->48 28->32 93->98 47->57 all 0 failed, red-first 11 RED 0 controls, SCREEN :276 YAML equality MEASURED and HOLDS; KS-1364 moved ITSELF to In Progress

## BLUF
**READY FOR QA: PR #1365, head `bf277eead26897bb648c801f92308681dbdaffdc`** (GitHub API and
`ls-remote` read in the SAME action, both that SHA). Base `develop`, 11 files, **+316/-6**,
title 81 chars. `Refs KS-1364` — it **narrows** the ticket, 11 of 17 operations, and does
not close it. Push **rc 0** under `.push-lock-47`. Nothing merged; I hold for your GO.

## Preflight, quoted as the hook printed it
```
PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.
```
All three skips are **one** named reason, `SKIP — local stack not up on
http://localhost:6882 (start it to run this leg)`, and the legs are:
- `3/15  Spec-auth conformance (unauth requests to bearer-authed ops must 401/403)`
- `4/15  Path resolvability (every spec'd path must route — KS-473 class)`
- `8/15  Served-spec consistency (/api/docs/openapi.json vs .yaml — KS-656)`

**Leg 8 is the same gap my PR body declares as NOT COVERED** (the served
`/api/docs/openapi.json` was not read) — the hook and my own NOT-COVERED line agree, which
is the honest reading rather than two different stories. Your brief allowed no deploy and
no stack bring-up, so I did not start the stack to convert them.
Also green and worth naming: `1/15 OpenAPI spec drift` ran and said **"OK — spec is in
sync"** — an independent corroboration of my `check:openapi`. `shell suites: 67 passed,
0 failed, 0 skipped (of 67)`; `OK — 13 code guards passed`.
`gatelines47.py` -> `VERDICT: MATCHES the declared fleet STOP condition`, which per B 51st's
handover is the **GOOD** state, not a failure.
Lock: TAKEN 02:09:18Z poll 1 waited 1s, **RELEASED 02:15:34Z by `Secuura/Blockchain b52`
pid 9002**, cool-off stamp written. `origin heads for this branch: 0` before the push.
My own orphaned `login_stub` pids under my worktree: **0**.

## Evidence
| service | before | after | failed |
| -- | -- | -- | -- |
| nft-certificate | 38 | **48** | 0 |
| analytics | 28 | **32** | 0 |
| billing | 93 | **98** | 0 |
| m365-integration | 47 | **57** | 0 |

Every AFTER equals your table; every BEFORE equals your 38/28/93/47. All re-measured from a
fresh install — no Spark figure carried.
- **Red-first by assertion: 11 failing cells, exactly the 11 `RED KS-1364` cells, 0 controls
  failing** (4/1/2/4 by vitest's own totals = your 2+2+1+2+3+1). Names NR1 NR2 NV1 NV2 AR1
  BL1 BL2 MS1 MS2 MS3 OD1. 44/31/96/53 passed beside them, so not a LOADFAIL.
- **Twelve applies:** six goldens `--check` rc 0 + apply rc 0 with **ZERO offsets** (so the
  second carve on each shared file applied strict on top of the first); six companions
  rc 0 with **8 hunks needing offsets** (carve 2: +2,+2; 4: +1,+1; 5: +3,+3,+3; 6: +5),
  expected because every companion header reads `index 9c5c51cd4..<x>`.
- `tsc --noEmit` rc 0, **0 errors**, four services. Base rc not captured; 0 errors cannot be
  worse than base, and I claim no more.
- All five base blobs identical between c56dd7c32edf and 723dc0722b68 and equal to yours.

## The YAML route, and SCREEN :276 is now MEASURED
**Both routes, and they agree.** The six companions applied give
sha256 `7089242840e35885887a698ca70d5c89e5aa8cfb779aee17b048fdabbda5e2d3` (your drafter's
prefix exactly), +11/-0, all eleven added lines the identical string `        required: true`.
Then `npm run generate-openapi -- --check` on that tree -> **rc 0,
`CHECK PASS: on-disk YAML matches generated`**. So the companion union IS what the generator
produces from the patched TS — the equality SCREEN :276 recorded as "Not run".
**Control: with the YAML reverted to base the same check goes rc 1**
(`CHECK FAIL: generated YAML differs from on-disk version`), so the rc 0 is a reading.
`check:openapi` rc 0 overall; `check-spec-examples`: 405 example blocks, all resolving.
`--check` did not write (YAML sha256 identical before and after).

## NOT COVERED
No Schemathesis and no live run — that the no-body cases stop firing is a **prediction** from
the rendered spec. The served `/api/docs/openapi.json` was not read (preflight leg 8, skipped).
The 15 pairs baselined in `systemTest/schemathesis` against KS 255 are untouched; un-baselining
them is not ours. No migration, no config, no lockfile, no `package.json`.

## 🔴 TWO THINGS FOR YOU TO RULE
1. **KS-1364 MOVED ITSELF to In Progress, and your HOLDS says it stays Backlog.**
   I issued **no** state mutation on it — my only Linear writes this round were KS-1401's
   create + 2 relations, KS-1397's comment, and KS-1397 -> Done. The evidence it was the
   GitHub integration: PR #1365 created **02:16:27Z**, KS-1364 `updatedAt` **02:16:36.950Z**
   — 10 seconds later — and **KS-1015, also Backlog and never branched by me, is still
   Backlog**, updatedAt 2026-09-29. This is the known "a branch name moves the ticket"
   behaviour. **I have NOT moved it back**, because that is an unruled state change and only
   KS-1397 -> Done was ruled. Say the word and I will, or leave it.
2. **`mergeable_state: unstable`, and I CANNOT tell you why.** The `kksecura` PAT **403s** on
   both `/commits/<sha>/status` and `/commits/<sha>/check-runs`
   ("Resource not accessible by personal access token"), so the cause is unreadable from
   here — I am not guessing at it. Per KS-660 `mergeable_state` carries no testing claim
   anyway; the Test Evidence block carries it.

## The fuse
**(unread)**, against 2026-10-09T00:00:00Z. **3 rows** at develop c56dd7c32edf (B 51st §A;
I did not re-measure the baseline and do not claim it as my own reading). **I re-dated nothing.**

## State
Nothing merged, nothing deployed, no `az` call, no SSH to any VM. No comment on KS-1364 (it is
Peter-created with 0 comments). Nothing on KS-492, #1360, #1362. Develop still c56dd7c32edf.
Watcher, ps read in this action:
94265 78700       24:44 /bin/bash ./inbox_watch47.sh 2026-10-01T01:52:55.000Z 60

**Please read my ctx.**
