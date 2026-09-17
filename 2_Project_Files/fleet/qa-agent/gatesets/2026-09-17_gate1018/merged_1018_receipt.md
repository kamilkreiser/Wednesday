SUBJECT: [Secuura/Blockchain -> Wednesday] MERGED: #1018 KS-1050 @e02515f8f4635822120e1cd90380b015ab5ddf00
TS: 2026-09-17T10:38:14.000Z
AUTH: {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'}
Seat A

## BLUF
MERGED: #1018 KS-1050 → develop `e02515f8f4635822120e1cd90380b015ab5ddf00`, on your 10:35:25Z GO. Verified at origin: parent = the gated develop `19f1e5475`, tree = the read-only prediction, both blob targets equal, and the auth subtree equals the gated head's (so 63 / 755 by construction). KS-1050 stays In Progress. ONE facts comment posted: `d856751d-e63c-4b84-b132-6edd3edba608`. It carries the gate's records and the round-1 correction.

## Recommendation
No action needed. F-1 is untouched, as ruled (yours to route). Next: the cap now has a free slot (#1026 and #1028 open). I finish the KS-1213 local build to a red-proofed head, then take KS-1180-P1 into the free slot (develop merged in first) and STATUS both. KS-1194 still waits for Kam's tap; its merge-tree re-runs against `e02515f8f` now that #1018's final `users.ts` is on develop.

## Detail
- **Pre-step** (`5_Project_History/2026-09-17_seatA-6th/merges/merge-1018.out`, ~10:36Z):
  - ls-remote: develop `19f1e5475` (unmoved since the gate), pull/1018/head `efd677e98c917a52f8af442c9fcfde756166070e` (= GO).
  - PR open, mergeable true / `unstable`.
  - `merge-tree --write-tree 19f1e5475 efd677e98` rc 0 → `ce49c7bfd`; predicted blobs `users.ts` `c723a68af` OK, ks1050 test `ffb3e801a` OK; develop → predicted = exactly the 2 PR files.
  - `attachmentsForURL(pull/1018)` = [KS-1050 `contributes` In Progress].
  - Closing-phrase scan over 8 texts (PR title, body, squash title, squash message, 4 commit messages): 0 hits; control `Closes KS-1` fires.
- **Squash:** REST `PUT /pulls/1018/merge`, `merge_method squash`, `sha` pin `efd677e98…` → 200 `merged: true`, sha `e02515f8f4635822120e1cd90380b015ab5ddf00`.
  - Title `KS-1050: a profile update that matched no row answers 503 "Profile update could not be confirmed", not success (#1018)`; body `merges/squash-1018-body.txt`, `Refs KS-1050`.
- **At origin:** develop = `e02515f8f` (== the squash); parent `19f1e5475` (== pre-merge develop); tree `ce49c7bfd` (== predicted); merged blobs `users.ts` `c723a68af` OK, test `ffb3e801a` OK; merged auth subtree `89aad911c` == head's `89aad911c`.
- **Suite on the merged tree:** not re-run. Develop did not move, and the auth subtree is byte-identical to the gated head's, where the gate and I measured 63 files / 755 tests.
- **KS-1050:** In Progress after the merge (no state change, completedAt null).
- **Comment `d856751d`** (10:37:52Z, read back, 5 / 5 anchors), BLUF / Recommendation / Detail, no at-signs:
  - the merge and the 503 contract;
  - the explicit correction of `413d3b05` (round 1's 500 "matched no row" shape was Wednesday's reading, withdrawn before the merge; only round 2 merged);
  - the gate's records (develop 200 `{success:true,data:{}}` vs head 503 through the real helper; 16 / 16 tamper rows on 63 / 755);
  - no live-RLS reproduction;
  - the unswept callers (`users.ts:1266`; `auth.ts:255, :539, :587, :1239, :1243, :1313, :1317`, as the gate read them).
- **F-2 noted:** my "68" with-tests count does not reproduce under the gate's instrument (37 = 37). The scratch tsconfigs differ (mine extends auth's `tsconfig.json` with absolute `include` paths). I will not quote that count again without naming the instrument.

