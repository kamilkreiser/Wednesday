auth: {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'}
Seat A

## BLUF
**MERGED #1029 (KS-1180 part 1, test-only) on your GO (12:44:07Z): squash `27e53ec3aa010b50cd9b2e4a1d15cbb34605ba7d`, merged_at 12:45:58Z.**
- Verified at origin: develop = the squash; parent `bb848b828` = pre-merge develop (unmoved since your read); tree `38dd44d8c7a4db0a60980e1a120233a12704ac5e` = your prediction.
- The ks1072 test blob `d9c98320e` is equal. The squash touches exactly that one file.
- **The api-gateway suite on the merged develop with the real 4.1.11 install:** 57 files / 556 tests, 0 failed, 0 pending, at default timeouts AND at 60 s ceilings; ks1072 6 / 6.
- KS-1180 stays In Progress. Facts comment `17822539-0c66-4213-a8af-1fbdd55af19b`. R-1029-2/3/4 filed as **KS-1227** (test-only, local-model candidate).
**A slot is free (open: #1031, #1032). Next: KS-1215 into it.** I will merge develop `27e53ec3a` into the KS-1215 branch, re-read the content, and re-run the cells and the tamper table on 4.1.11 before the push and the READY.

## Recommendation
Route **KS-1227** to the local model if you agree. No other action needed on this receipt.

## Detail
- **Pre-step** (`merges/merge-1029.prestep.out`), then the same script with `--do-merge` (`merges/merge-1029.out`):
  - ls-remote: develop bb848b828, pull/1029 cd3580e1f (= GO); develop unmoved since your 22:43:43 AEST read, so the ks1072 STOP condition was not met.
  - PR open at the GO head, mergeable true (state unstable).
  - merge-tree rc 0, predicted 38dd44d8c = GO. Predicted blob d9c98320e OK.
  - develop→predicted files: exactly `services/api-gateway/src/__tests__/ks1072-the-latest-anchor-selector-documents-a.test.ts` (the script stops on any other set).
  - attachmentsForURL(pull/1029) = [KS-1180 contributes In Progress]; KS-1073 not linked. Closing-phrase scan: 0 hits over 7 texts; the control fires.
  - The merge PUT with sha pin cd3580e1f: http 200 merged true. At origin: develop == squash, parent == pre-merge develop, tree == predicted, blob OK.
  - The merged api-gateway subtree differs from the head's (dea998d3f vs e7c377ff4), as expected: develop gained #1028 and #1030 after the head's base.
- **The 4.1.11 run** (records `merges/1029-postmerge/`):
  - My own worktree `raise-0916-a` was detached at `27e53ec3a` (porcelain 0) and `npm ci` run in `Blockchain/Dev` against develop's root lock (rc 0, 1937 packages, 30 s).
  - `require.resolve` from `services/api-gateway` gives vitest 4.1.11 and its mocker 4.1.11 (it was 4.1.10 before the install).
  - Default run rc 0: 57 / 556 / 0 / 0 (1-min load 5.6). `--testTimeout=60000 --hookTimeout=60000` rc 0: 57 / 556 / 0 / 0 (load 6.5). Porcelain 0 after; the worktree is back on the KS-1215 branch.
- **KS-1180 facts comment** carries the addendum's records:
  - P-1016-1 fixed by the anchor-store witness (discrimination measured: 5 witness reds at head, 0 on the pre-PR blob, on head and merged);
  - P-1016-2 closed (TS18046 1 → 0);
  - **P-1029-1: the witness proves tier 2 was ASKED once, not that it ANSWERED; the open tier-1 half closes that**;
  - R-1029-1: the PR table's "GT2" is not the #1016 GT2;
  - R-1029-2/3/4 → KS-1227.
  - Readback 4/4 anchors. The first post attempt was refused by the helper's at-sign guard (the vitest mocker's scoped package name); I reworded it, and nothing was posted twice.
- **KS-1227** (Low, Backlog, our account, related KS-1180, `Refs KS-1180` in the body): try/finally around `postTier2`'s listener; decide and pin the counting rule; an optional note on P-1029-1's message. Regression proof: the gate's Q-D4-LEAK probe reads a listener count of 1.
  - Board search first (`tickets/search-1029-findings.txt`, literal, archived included): `ks1072-the-latest-anchor-selector` 3 (KS-1072, KS-1199 on a tie-verdict cell, KS-1180); `postTier2` 0, `anchorServer` 0, `listenerCount` 0. The same search found the file name, so the instrument can match.
- **Squash message:** `merges/squash-1029-body.txt` (Refs KS-1180; states "asked once, not answered"; no closing verb).
- **Not mine, noted:** your R-1029-8 (the shared checkout's `.git/config` changed 22:32:42 AEST). This seat made no git write between 12:16Z and 12:44Z (idle on the watcher); my KS-1194 push ended 12:08:19Z, PROTOCOL-CLEAN with config IDENTICAL.

