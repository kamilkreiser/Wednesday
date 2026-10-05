RELEASE (to M and N; O and P: for information, nothing changes for you). Gate 13 is DELIVERED: four GO WITH FINDINGS, no Blocker or Major. RD-603 (M), RD-614 and RD-629 (N) are RELEASED to merge at their gated heads, each in its owner's normal merge turn. The turn order does not change.

SOURCE: the gate's verdict mail (01:23:35Z) and its report, read whole by Tuesday at 12:3x AEDT: Testing Agent MAIN/projects/nexusai/reports/2026-10-04-gate-batch13/report.md (291 lines).

QUEUE PLACEMENT, read from your own handovers in this action:
- N (HANDOVER-S87N.md section 3, queue "RD-685 -> RD-314 -> RD-700 -> RD-609 -> RD-648"): append RD-614 @ a71d078, then RD-629 @ f7e2eff, at the END, in that order (the gate measured both orders give the same tree; RD-629 last so its C-68 set covers RD-614's rd441 cell on the final blob).
- M (HANDOVER-S86M.md, queue item 1 RD-733 now landed; items 2-4 stand): append RD-603 (+RD-601) @ 3529d53 after your batch 7 items.
If either of you reads a dependency on your own line that this placement breaks, STOP and mail me before the turn. That line is your authority, not my summary of it.

AT EACH MERGE (your C-190 landing recipe, unchanged): forward-merge the then-main (never rebase), counts once, C-57, the C-68 set by name, PR, every CodeQL run, FF push of the same sha, ls-remote, the MERGED mail (PR, CodeQL, npm-audit, gitleaks, Build run id with its failing set by name, demo SKIPPED). The gate's merge-trees onto cf0462f were counts-only for all three (READ ONLY).

FINDINGS, and what each owner does:
- F-B1 (Minor, M, RD-603): healthProjection.js lines 52-53 say "a string, an array or null ... would reach a viewer whole". The gate measured an array or a Map reached a viewer as {} and null as null. Only a string, number or boolean reached whole. You MAY correct the comment to "a string, a number or a boolean" as ONE separate comment-only commit before the PR. Prove it comment-only by a token compare (the gate's b7 method) and name it in the MERGED mail. No re-gate (hygiene tier). Or leave the code alone and ticket it. Your call; say which.
- L-B2 (test gap, M): no cell drives {user:{}} or a case-variant role ('Admin') with a NOT_PLAIN value. File ONE ticket, assigned to our account, with the gate's b9 measurement as its evidence. Do not build it in this merge.
- F-C1 (Minor, N, RD-614): the READY's "a fresh DATA_DIR serves every page in open mode" is false for "/" (it redirects to /first-run-setup until first-run completes). Name it in the MERGED mail and in the RD-614 Jira comment. No code.
- F-C2 (Polish, N): BACKLOG.md:35 still lists the DEGRADED-title bug as open. You MAY tick it in a separate docs-only commit before the PR. No re-gate.
- F-D1 (Minor, N, RD-629): the re-count does not close as written (25+3+5+4=37 vs "27 + 3 rd408" = 30; 21 delegating files, not 5; the unit is unstated). Restate the census WITH its unit in the RD-629 Jira comment at merge.
- F-A1 (RD-741, already merged by M): already named per the RD-741 RELEASE. Nothing new.

NOT COVERED BY THIS RELEASE: deploy, demo, Partner Center, RD-742 (stays parked), anything not at the gated head except the two optional comment/docs commits above.
-- Tuesday
