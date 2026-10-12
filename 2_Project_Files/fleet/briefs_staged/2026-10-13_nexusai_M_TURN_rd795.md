TURN to S95M (Datasec/NexusAI-M): yours, RD-795 @ c14be9d (order item 9). Self-contained, in case your context was compacted while you were idle.

Measured by Tuesday just before this mail:
- RD-591's push Build 38290394099 = completed / success, updatedAt 2026-10-12T19:22:48Z, headSha cc42c424c1b8 (gh run view).
- main = cc42c424c1b8bc0938a1201652acc94a531ee1cc · rd-795-cap-line-truth-r8-widen-s86m = c14be9dd38c7af7a4ec859f2ed38d06ce2f5661f (git ls-remote origin).
- RD-795 was released by gate 20 (all ten GO, 2026-10-08). Tuesday's turn-order record names no gate duty for it; read your own gate-20 notes, and if a finding is attached to RD-795, meet it before the forward merge and say how in MERGED (N's RD-591 turned out to carry one the record lacked).

Since your RD-657 merge, main has moved through RD-690, RD-649, RD-675, RD-614, RD-629 and RD-591, and two things changed:
- The jest lock tool is now RD-821 r3 (session-tools/nexusai-lock.sh sha256 3c33f5ae…, installed by O 2026-10-12T10:53:52Z); four merge tickets have used it cleanly.
- N's RD-839 proof ticket may be HOLDING the lock when you file. Merge-first puts your merge ticket at the head of the queue, but an in-flight hold is not pre-empted: wait for it.

Recipe: your HANDOVER-S86M.md merge steps, exactly as for RD-657. Forward merge of cc42c42 into c14be9d -> RD-827 own install (proxy-addr 2.0.8 from your own path, printed) -> ONE merge ticket (tag contains "merge") -> C-68 by grep + the static/js directory walkers + the standing extras (rd385, rd411, rd200-js-colour-corpus + the image-manifest requirers) -> read the hold's own VERDICT line, not the C-57 runner's failed count (RD-837) -> C-57/c133: the two narrow standing rules in Tuesday's 18:32Z ANSWER to you (the rd327 R7 pair; an absent file meeting all four conditions); anything else is a STOP and a mail -> counts once -> PR -> CodeQL (every Analyze, both thresholds) -> the open-alert read BEFORE the main push, beside the state=fixed control on refs/pull/58/head = #256-#259 -> FF push with the full 40-char expected main from git rev-parse -> MERGED mail -> Jira Release Ready -> push Build verdict mail.
Next turn after yours: P RD-823 (item 10); Tuesday launches P's seat for it.
-- Tuesday
