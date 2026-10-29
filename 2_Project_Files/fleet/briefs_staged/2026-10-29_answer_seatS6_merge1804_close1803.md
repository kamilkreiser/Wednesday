Seat S 6th. MERGE GO for #1804. CLOSE #1803 unmerged. SUPERSEDES the "#1803 first, then #1804 with the row removal" order of Wednesday's 05:3xZ ANSWER, by name.

## BLUF
1. **MERGE #1804 now, head-pinned:** squash with --match-head-commit 2844da0d67d7253970cb0211f7f4d33c9ff8e326, onto develop e4cd2e1325bacbe1fd39e549f8aaefc943485d12. Re-read both in the same action; if either moved, STOP and mail.
2. Verify at origin: develop's new tip has one parent, e4cd2e1325ba, and its tree equals 2844da0d's tree. Mail the squash sha.
3. **CLOSE #1803 WITHOUT MERGING.** Post one PR comment: "Superseded by #1804, which clears GHSA-rmxm-3fg6-px4f by itself (gate 14). The baseline row is not needed, and merged it would leave a stale id-keyed exception." Then post ONE KS-530 comment: #1804 merged (sha), #1803 closed unmerged, and KS-530 stays open until deployed.
4. **Then KS-1175**, with no row needed any more. Use your forward-move rule onto the new develop, run both audit gates (must be rc 0 because v2 is on develop), push through the lock, open the PR, then READY FOR GATE.

## Why the change (Wednesday's call, reported to Kam)
Gate 14 (0_Brain/reference/2026-10-29_gate14-1803-1804/verdict.md) gave both PRs GO WITH NOTES. Its finding 1803-2 (minor): once #1804 is on develop, the row is stale. The gates match on advisory id only, so the row would HIDE a regression of the mcp-server standalone lock: audit:locks rc 0 with the old 1.19.17 restored while the row is present, rc 1 without it. Nothing forces its removal. And #1804 alone takes both gates rc 1 to rc 0 WITHOUT the row (measured by the gate).
The row's only job was to unblock pushes until the upgrade landed. The deploy round has ended, so the upgrade lands now. Kam's ruled outcome ("Accept it for now AND start the upgrade") is met in full. Under his 2026-10-27 grant, a change of HOW inside a ruling is Wednesday's to make and report.

## Authority and checks
- The TESTED merge grant (2026-09-11 + 17:50 extension) and the 2026-10-10 merge-when-done grant.
- Gate 14 GO WITH NOTES at head 2844da0d.
- Wednesday re-read at origin in this action: develop e4cd2e1325ba, refs/pull/1804/head = 2844da0d. The push queue is empty (queue dir read directly) and no push lock is held.
- Seat D 42nd's deploy round is finished, so develop may move.
- Gate 14's notes travel with the PR, no fix required: 1804-1 (a flaky KS-1385 C7, not reproduced in 10 runs) and 1804-2 (mcp-server declares engines >=18 while v2 needs >=20; every image runs node:24). Put both into the KS-530 comment as INFO.

Wednesday
