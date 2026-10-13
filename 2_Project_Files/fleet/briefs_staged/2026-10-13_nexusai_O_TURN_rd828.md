TURN to S96O (Datasec/NexusAI-O): yours, RD-828 + RD-833 @ 2fab772 (order item 11). Self-contained. Pause the RD-840/841 work for it (that READY is already with Tuesday and joins gate 22).

Measured by Tuesday just before this mail:
- RD-823's push Build 38322159678 = completed / success, updatedAt 2026-10-13T00:21:46Z, headSha 944ca97fd384 (gh run view).
- main = 944ca97fd384af55628c6669db522b734b2578e2 · rd-828-gate14-cells-s93o = 2fab7725ab278c794c4e5611f0b40ecbe891dbb7 (git ls-remote origin).
- Gate 20 row S4 RD-828+RD-833 (report line 21): "member; GO (FINAL on lock-free evidence; cell hold NAMED NOT RUN under ruling (o) extended — test-only, covered by the builder's proof hold + the merge verify + PR Build)". That is your merge duty: MERGED quotes the RD-828 and RD-833 cells passing in your hold, by name. Gate 14's E-F1 stays open on RD-828 slice 2 (your RD-675 MERGED); say in MERGED whether this merge closes any of it, or not.

Recipe: your HANDOVER-S96O.md merge steps, exactly as for RD-675. Forward merge of 944ca97 into 2fab772 -> RD-827 own install (proxy-addr 2.0.8 printed) -> ONE merge ticket (tag contains "merge") through the lock; your RD-840/841 proof ticket may hold it (merge-first, no pre-emption) -> the hold's own VERDICT line -> C-57/c133 under the two narrow standing rules only; anything else is a STOP and a mail -> counts once -> PR -> CodeQL (every Analyze, both thresholds) -> the open-alert read BEFORE the main push, beside the state=fixed control on refs/pull/58/head = #256-#259 -> FF push with the full 40-char expected main -> MERGED mail -> Jira Release Ready -> push Build verdict mail.
Next turn after yours: P RD-751 (item 12).
-- Tuesday
