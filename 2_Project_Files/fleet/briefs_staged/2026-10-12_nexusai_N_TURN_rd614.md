TURN to S94N (Datasec/NexusAI-N): yours, RD-614 @ a71d078 (order item 6). Self-contained, in case your context was compacted while you were idle.

Measured by Tuesday just before this mail:
- RD-675's push Build 38239053736 = completed / success, updatedAt 2026-10-12T11:48:40Z, headSha 9f2dbf8b2836 (gh run view).
- main = 9f2dbf8b2836521f4432915d3e28493e850f0b1b · rd-614-degraded-banner-title-s86n = a71d0786af2c68f0a44e226f7e3d99d4a428fa15 (git ls-remote origin).
- RD-614 was released by gate 13 (2026-10-05) with an F-C1 duty attached (your gate-13 notes carry it; read the F-C1 row before the forward merge and say in MERGED how it was met).

NEW SINCE YOUR LAST MERGE: the jest lock tool changed. O swapped in RD-821 round 3 at 2026-10-12T10:53:52Z (session-tools/nexusai-lock.sh sha256 3c33f5ae58e1be20…, verified by Tuesday; the old tool is kept as nexusai-lock.sh.pre-1012-o-r3). Gate 21 passed it, but YOUR merge ticket is its FIRST LIVE USE. If the ticket does anything unexpected (refuses, orders wrongly, never acquires), STOP and mail Tuesday with the lock's own output; do not work around it.

Recipe: HANDOVER-S87N.md (sections 13-15), exactly as for RD-649 this afternoon. Forward merge of 9f2dbf8 into a71d078 -> RD-827 own install (proxy-addr 2.0.8 from your own path, printed) -> ONE merge ticket (tag contains "merge") -> C-68 by grep + the standing extras (rd385, rd411, rd200-js-colour-corpus + the image-manifest requirers) -> read the hold's own VERDICT line, not the C-57 runner's failed count (RD-837) -> counts once -> PR -> CodeQL (every Analyze, both thresholds) -> the open-alert read BEFORE the main push, beside the state=fixed control on refs/pull/58/head = #256-#259 -> FF push with the full 40-char expected main from git rev-parse -> MERGED mail -> Jira Release Ready -> push Build verdict mail.
The lock queue was empty at O's swap. Next turns after yours: N RD-629 (F-D1 duty), then N RD-591.
-- Tuesday
