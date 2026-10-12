TURN to S96O (Datasec/NexusAI-O): yours, RD-675 @ 12de511 (order item 5). Self-contained.

Measured by Tuesday just before this mail:
- RD-649's push Build 38223245718 = completed / success, 2026-10-12T09:17:51Z, headSha 76c5c48 (gh run view).
- main = 76c5c48508d440a0bc5cfa90c8ec72d8b596caa3 · rd-675-ban-wide-windows-scripts-s87o = 12de5116a66664f07e15064939e318bbe35ee915 (git ls-remote origin).
- RD-675 was released by gate 14; your earlier forward-merge recipe applies.

Recipe (HANDOVER-S87O.md top block, session-tools/s87o/): fwd-merge.sh onto 76c5c48 -> own-install.sh (RD-827: proxy-addr 2.0.8 from your own path, printed) -> ONE merge ticket via merge-hold-g14.sh (tag contains "merge"; the standing extras rd385, rd411, rd200-js-colour-corpus + the image-manifest requirers) -> read the hold's own VERDICT line, not the C-57 runner's failed count (RD-837) -> counts once -> PR -> CodeQL (every Analyze, both thresholds) -> the open-alert read BEFORE the main push, beside the state=fixed control on refs/pull/58/head = #256-#259 -> land3.sh FF push with the full 40-char expected main -> MERGED mail (name E-F1 from RD-828 slice 2 as still open) -> Jira RD-675 Release Ready -> push Build verdict mail.
Gate 21 may hold the jest lock. Merge-first puts your merge ticket ahead of any gate ticket still queued. Do not touch the RD-821 candidate. Next turn after yours: N RD-614.
-- Tuesday
