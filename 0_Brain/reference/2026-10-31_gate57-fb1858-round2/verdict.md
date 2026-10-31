## QA GATE 57, TIER 1, ROUND 2 (delta): KS-1384 F-b #1858
(Opus, Sat 31 Oct 2026. Findings only: nothing was fixed, pushed, commented, merged or touched in Linear. Evidence is in `evidence/`.)

**Head.** #1858 = **c39f61fe2def334e8a8fcdc9639342c0aa0fe49b**, read with ls-remote at the start and at the end; unchanged (`evidence/lsremote_{start,end}.txt`).
- Round 1 gated head: 9e7dfdcf6627 (gate 48, GO WITH NOTES). Round 2 is a fast-forward: 0d35405a7637 (D1) → e166c54eb80b (merge of F0c's develop merge ab59f2903405) → c39f61fe2def (L2 + N2).
- develop now = 644452e4af6d. `git merge-tree` of the head with it is clean, and develop has no anchoring commits after dc8c210.

## VERDICT: **GO WITH NOTES**
L2 is CLOSED. Nothing must be fixed before merge. One new note (G57-N1, liveness) and one test-coverage note (G57-N2).

## Q1: is L2 closed? YES
Probe `evidence/probe/gate57-probe.test.ts`: the real reconciler and the real `createWalletLabelScan` over a scripted wallet (newest first, 100 per page, 5 pages, so it truncates past 500 transactions). The row is (pending, NULL) with one wait marker at t0, which is its last write. The sweep runs at t0 + 2 h + 15 min, after the boot grace.

| Cell | c39f61fe (head) | e166c54e (reconciler.ts swapped in, positive control) |
|---|---|---|
| Q1a member 1 landed 61 min before the marker | **adopted**, confirmed with member 1 | **FAILED "nothing was submitted"** |
| Q1b landed 3 h before the marker, quiet wallet | **adopted** | FAILED |
| Q1c landed 3 h before the marker, busy wallet (600 txs since) | search **truncated** on 3 passes, **row LEFT, 0 writes** | FAILED (the window from t0 is complete and misses member 1) |
| Q1d R4: payload landed under another hash 2 h before the row's last write | **adopted**, guarded on its own hash | FAILED (gave up) |
| W's (l2) 61 min and (r4) | pass | RED (both), as W claimed |

**On real Postgres** (`evidence/probe/gate57-l2-pg.integration.test.ts.ran`: the real SELECT feeds `created_at`, and the writes go through `runAnchorStatusUpdate`):
- Head: 2/2. The 61 min and 3 h rows read back `confirmed` with member 1's hash, and the search started at exactly created_at - 10 min.
- e166: 2/2 RED. The rows read back `status: failed` (`evidence/pg_l2_{head,e166}.log`).

An older landing is found when the wallet is quiet. On a busy wallet the search ends `truncated` and the row is LEFT. It is never failed.

## Q2: no regression for a member that never landed: none found
- **Q2a, R6.** A rested row with nothing on chain: the search is complete and the row is FAILED with SWEEP_FAILED_MESSAGE at t0 + horizon + 15 min.
- **Q2b.** At 1 ms before that instant: no scan, no write.
- **Q2c, R4.** Created 40 h ago, last write 24 h + 1 min ago: two answered misses, then FAILED, guarded on its own hash.
- **Q2d, R4.** Created 40 h ago, last write 23 h 59 min ago: no search and no write over 3 passes. The give-up window still counts from the last write (KS-1808).

All pass at the head.

## Q3: boot grace = the boot arm's window: TRUE
- Q3a: `SWEEP_BOOT_GRACE_MS` = (ANCHOR_TTL_SLOTS + BOOT_ARM_MARGIN_SLOTS) × 1000 = 130 min. It is read from the arm's own constants (reconciler.ts:143).
- Q3b: the real `BootArm` is not armed at S_boot + grace/1 s - 1 and is armed at S_boot + grace/1 s.
- Q3c: no scan at boot + grace - 1 ms; one scan at boot + grace.
- Mutants M5 (TTL only) and M6 (`>` for `>=`) are killed (below).

## Q4: delta discipline: nothing beyond gate 48's D1, L2/N2 and their tests
Instrument: a synthetic `git merge-tree --write-tree 9e7dfdcf6627 ab59f2903405` (= 48cd8180) diffed against the head (`evidence/q4_synth_vs_head.txt`).
- **Product:** `reconciler.ts` only (+38/-13 incl. comments). The changes are:
  - the grace constant;
  - `CARDANO_SLOT_MS`;
  - two imports;
  - `fromMs` from `created_at` instead of `updated_at`;
  - comments.

  The patch is in `evidence/delta_reconciler.patch`.
- **Tests:**
  - `ks1384-fb-sweep.test.ts` (+81/-16)
  - `ks1384-fb-sweep.integration.test.ts` (+8/-4: fixtures moved after the new grace, no assertion weakened)
  - the new `ks1384-fb-g49-f1-shapes.test.ts` (+196)
- **Docs:** the 2 Projects Documents pages differ from the synthetic merge only by its conflict markers. At the head they are byte-equal to dc8c210's (DOCS HOLD, not in scope).
- **N2 shapes reproduced:**
  - Ma (`!== 'dead'` → `=== 'live'`) is killed by (n2a) only;
  - Md (first member only) is killed by (n2b) only (`evidence/mut/M[ad].g49shapes.log`).

## Q5: mutants on the window and grace changes
Each mutant was applied by unique anchor and restored by sha256 `7e3af315…` (verified after each run): `evidence/mut/`.

| Mutant | My cells (Na/Nb/Nc excluded: they are red at head by design) | W's F-b and reconciler cells |
|---|---|---|
| M1 search from updated_at | **KILLED** by Q1a, Q1b, Q1c, Q1d | killed by (r4) and (l2) 61 min |
| M2 created_at **+** 10 min | **KILLED** by Q1a, Q1b | killed by (r4) |
| M3 R4 reverted to updated_at, R6 kept on created_at | **KILLED** by Q1d | **SURVIVES** all 6 files |
| M4 R6 reverted, R4 kept | **KILLED** by Q1a, Q1b, Q1c | killed |
| M5 grace = TTL only | **KILLED** by Q3a, Q3b | killed by (m3b) |
| M6 grace `>` instead of `>=` | **KILLED** by Q3c | killed (10 cells) |
| M7 lookback 0 | survives mine | killed by (r4) |

## FINDINGS
**G57-N1 (MINOR, liveness and readback, not money; reconciler.ts:204 with index.ts:1510-1580). The search from creation never ends for a re-armed row of an old document.**

Cause:
- The upsert `ON CONFLICT (document_id, network) DO UPDATE` never sets `created_at`. One row per document lives for ever, so a re-POST (a share, or the "latest event wins" verb) re-arms a row whose `created_at` can be weeks old.
- The adopt search now runs from that creation. Production's scan is capped at 20 pages × 100 and 30 s (index.ts:2272), so on a wallet with that much history since the creation it ends `truncated` on every pass.
- `adoptScan` returns `undecided` on anything but `complete`, **even when the match was found on page 1**.

Measured at the head (5-page harness):
- **Na:** created 30 days ago, re-armed 20 min ago, 600 transactions over the 30 days, nothing landed. R6 never decides: 0 writes. At e166 it is failed.
- **Nb:** the same row with its payload landed 5 min ago, on page 1. It is **not adopted** at the head (0 writes); at e166 it is adopted.
- **Nc, R4:** created 30 days ago, last write 25 h ago. The give-up is deferred on all 6 passes, and the row keeps a dead hash for ever. At e166 it is failed.

Assessment:
- This is the safe direction: never a wrong 'failed', and no fee.
- But W's "already true for any row whose last write is old" understates it. For R6 the old row is now the common re-POST case, and the row is never decided, not just sometimes deferred.
- The (r4) cell's own fixture is this shape (created 30 days ago, re-armed 11 minutes ago); it pins the window but does not exercise truncation.
- Possible shapes, for W to choose:
  - bound the start, e.g. `max(created_at, min(updated_at, markerT0) - (TTL + margin) - 10 min)`. The member must have been signed after the attempt began, and the wait marker bounds it.
  - or let a truncated scan that already holds a confirmed match adopt it.

It needs Wednesday's acceptance or a follow-up ticket. It does not block.

**G57-N2 (NOTE, test coverage).** W says "the adopt search (R6 and R4)" moved and that "(r4) now pins the creation start", but (r4) drives an R6 row only. Mutant M3 (R4 alone back on updated_at) survives every W cell in the F-b and reconciler files. Q1d is the shape that pins it.

**Carried, unchanged:** gate 48's N1 to N7 and D1.2 (batch rows adopt only the first constituent) are not touched by this delta.

## COUNTS (instrument named; Node v26.8.1, NOT LTS)
- **Install:** `npm ci --ignore-scripts` at Blockchain/Dev (1795 packages), then a build of @secuura/shared.
- **Unit, anchoring (vitest, --maxWorkers=2):** 722/723. The only red is threadTokenMint (host-dependent, as in gates 48 and 49). This matches W.
- **tsc, service tsconfig:** 0 errors. Positive control: a planted TS2322 gives rc 2 with one TS2322.
- **Real Postgres lane:** 10 files, 122/122.
  - Container `gate57-pg`, postgres:15-alpine, with repo `docker/init` and `init-platform` (copied into the scratchpad) and throwaway passwords.
  - `run-migrations.sh` gave applied=57, failed=0.
  - pg_stat_database showed 454 tuple writes during the run.
  - Bad-credentials control: 9 failed files, 1 passed, 118 skipped.
- **Probe at head:** 11/14. The 3 reds are Na, Nb, Nc: they are the G57-N1 finding, asserting e166's behaviour.
- **Probe at e166:** 6 red. Q1a to Q1d are the positive control; W's (r4) and (l2) 61 min are also red.

## SPARK SHADOW AND CALIBRATION
- **spark_gate.sh** (`… 1858 c39f61fe… e166c54eb80b ks1384-fb-sweep.test.ts`):
  - It resolved the merge-base, then shadow_facts printed **"merge-base (empty) · diff 0 files"**.
  - This is the base-side instrument fault recorded by gates 48 and 49, and it recurs.
  - BASE reported 24/24; the truth is 22/24 ((r4) and (l2) red, measured by swapping the product file).
  - HEAD 24/24 agrees.
- **spark_review.py:** run on the clean e166..c39f diff, with `--linear-env /dev/null`. It returned GO WITH NOTES.

| Spark finding | Gate 57 | Calibration |
|---|---|---|
| Note: no PR body or ticket | It was not supplied, by my choice | Noise |
| Note: facts.json shows 0 product files, which contradicts the diff | True: this is the instrument fault | **True** |
| Note: the shapes file was not run by the runner (×2) | True of the facts I gave it; I ran it (5/5 with nf, killing Ma and Md) | True of the instrument, not the PR |
| Note: (l2) asserts the outcome, not the window; the change is tested only indirectly | (r4) pins the R6 window. The real gap is R4's start (G57-N2), which it did not name | **Partial** |
| Verdict GO WITH NOTES | GO WITH NOTES | **Agrees** |

Score: 1 true, 1 partial, 2 instrument-true, 1 noise. **Missed G57-N1** (the re-armed and truncation liveness) and G57-N2's R4 specifics.

## UNMEASURED
- Any chain, Blockfrost, wallet or box.
- The real production scan sizes against a real wallet's history, so how often G57-N1 truncates in practice: my harness used a 5-page cap; production uses 20 pages and 30 s.
- The product upsert in a live re-POST race: the Postgres probe inserts rows directly.
- The four platform suites, eslint, hook legs and preflight.
- Node 24 LTS.
- Two processes.
- R1 and R2.

## HOW
- **Clone:** `git clone --shared --no-checkout` from gate 48's clone into the non-existent `repo/`, with toplevel asserted before any fetch. Push URL is `no_push_qa_gate`; fetch uses the Blockchain deploy key. Fetched refs/pull/1858/head and develop.
- **Product swaps:** done only in my clone, restored by sha. Probes were copied into src only for their runs, then kept as `*.ran`. `git status` was clean before teardown.
- **Hygiene:**
  - No git write verb was run in !CODING.
  - W's `s-w13-pg` was not touched.
  - `gate57-pg` was stopped and removed by name.
  - The clone and the scratchpad spark worktree and init copies were moved to the scratchpad and deleted.
  - Every PID I started has exited.
- **Folder:** 348 KB.
