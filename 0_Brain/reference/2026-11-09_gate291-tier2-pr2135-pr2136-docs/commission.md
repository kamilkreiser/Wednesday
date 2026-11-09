# Gate 291, TIER 2 (Sonnet): PR 2135 (KS-1807) + PR 2136 (KS-2151), both Seat Y 11th, DOCS ONLY. ONE session, two verdicts. Commissioned 2026-11-09 19:3x by the 18:46 Wednesday seat (batched under Kam's 2026-09-18 minimise-gate-duplication rule; tier 2: docs, no code byte, by the seat's READYs: prove it).

Common rules: follow the tier-2 shape of /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_gate284-tier2-pr2124r2-2125-2126/commission.md (read it whole; its common-rules pointer applies) at tier-2 depth.

Pins (Wednesday's ls-remote at 19:31:14 AEDT; RE-READ them at start and end, and say whether each moved):
- develop 1b3a3ec34a5bb4df13a4cea9ae7b03b7a87a172a (the PR 2115 squash). Both PRs were built on older develops; read what moved since and whether it touches either PR's paths.
- PR 2135 head e2ada9bf1ea9db6c901a3a33723241e9d38be031 (KS-1807: 3 files, +8/-6, docs)
- PR 2136 head b907ba03bea2e2fdcd6c1fe7aa0dc73f4c7f1edd (KS-2151: S-K-OWNERSHIP-CONTRACT.md, VOCABULARY.md, openapi/WORKFLOWS.md; +39/-2)
- PR 2073 head 2684a29d8f576ff74634f07ad6576af5bd00370b (open, by another author; it shares S-K-OWNERSHIP-CONTRACT.md with both)

READYs: the seat's two READY mails, saved in /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-09_seatY-11th/mail/ (find the newest READY files; say which you read). Evidence is in the same seat folder's evidence/. Reproduce; do not trust.

What the docs must say: the RULINGS, read whole:
- KS-1807 (Kam's card secuura-ks1807-undecided-k-side-1109 = a, 'Docs record today's behaviour now', 17:20): the docs record what the code does TODAY, not what is planned. Stuart's answers (Kam's panel relay 16:17: no on connector revoke with onBehalfOf; his answers on documents:revoke, anchors:read and the provisioning-key mint go on KS-1807) must be reflected where the PR claims them. Read KS-1807 at Linear read-only if you can; otherwise say UNREAD.
- KS-2151 (Kam's 6 Nov answer, as Stuart restated it in the 16:17 relay): 'one anchor row per document, and a new paid transaction for every share and lifecycle event until stage 2'.
- Wednesday's rulings to the seat: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-09_seatY11_docs.md, 2026-11-09_Y11_answer_plan.md, 2026-11-09_Y11_grant_pushA.md, 2026-11-09_Y11_grant_pushB.md (read whole). Note SCOPES.md line 138 stays byte-identical (the brief's own error, superseded by the plan answer).

Questions (each PR):
1. Docs only, no code byte: prove it through the PR files API and a diff read.
2. TRUTH OF EVERY CHANGED SENTENCE against the code at develop: for each added or changed sentence that states behaviour, quote the code line that makes it true, or name it as unbacked (a finding). The seat says it re-read anchorSubmission.ts and attemptFamily.ts for KS-2151; re-derive that. For KS-1807, each 'today's behaviour' line is checked against the route or scope code it describes.
3. Untouched lines: the seat claims 3 marker lines byte-identical, and that SCOPES.md:138 is untouched. Verify it.
4. Merge trees onto today's develop: each PR alone, both together, and each with PR 2073's head (the seat says rc 0 in either order). Name any open PR that shares a path, with a planted control. G 32nd (KS-590) will edit docs/VERIFICATION.md soon: that is NOT in either PR (the seat lists it as not covered); confirm.
5. The docs checker and docs-fragments: re-run the seat's docs checker (10 of 10 tokens) and docs-fragments (OK, fragment word NONE), with a planted defect proving each check can fail.
6. The body and ticket comments claim no more than the change (PR 2136 comment cf010d51 on KS-2151).

SPARK SHADOW (rule 2026-10-26: every tier-2 Claude gate gets one): after your own verdict is written, run /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/gate/spark_gate.sh on each PR, as /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_gate289-tier2-pr2133-pr2134/calibration.md describes (read it whole, including its tooling fault: if the runner finds no test runner and reports '0 passed, 0 failed', that run is INVALID; for docs-only PRs, say what the Spark gate actually checked). Append a calibration row to this folder's calibration.md. If the Spark does not answer, say so in one line; your verdict stands alone.

Constraints: your own clones under /private/tmp/g291 ONLY. Never cd. In any /Volumes/DevMASTER/!CODING/ checkout use only ls-remote, show, log, diff, ls-tree, cat-file and grep: never fetch or any git write verb there. Never push. Never run the hook against the real remote. No real .env. No containers. Keep load1 under 8 (wait if it is higher). Read df for DevMASTER at start and end. No rm.

Output: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_gate291-tier2-pr2135-pr2136-docs/verdict.md (if your Write is refused, put the whole verdict in your final message). Line 1 exactly: 'PR 2135: <V>; PR 2136: <V>', each V one of GO | GO WITH NOTES | NO GO. Then, per PR: FOUND / TESTED / HOW (instrument, controls), NOT TESTED, and findings G291-2135-<n> / G291-2136-<n> with severities. Findings only; post nothing; mail nothing.
