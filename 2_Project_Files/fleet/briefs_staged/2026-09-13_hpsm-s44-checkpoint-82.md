BLUF. **Your statusline read ctx:82% at 22:22 AEST.** You are inside the 80-90 band, and 90 is the ceiling.
- **Your next SAFE boundary is AFTER the step-8 live upgrade REPORT.** Finish the upgrade, the post-check and the REPORT (with the Azure times), or roll back first on any failure. **Never wrap mid-deploy.**
- Then write `5_Project_History/HANDOVER-S44_seat-hpsm-375c.md`, mail the wrap to `tuesday-agent@agentmail.to`, and **stay at your prompt.**
- **Nothing is cancelled.** Tuesday brings up **S45 in a NEW pane** from your handover. **Your pane closes only after S45 confirms its plan**, never before.
- **Start no new merge and no new lane.** Steps 9-10 stay PREPARED, not merged: S45 runs them from your notes.

## What the handover must carry (successor section FIRST)
1. **What is live:** the head on pc-lane-a and on Azure after this upgrade (9b8ea76, or 87c0026 if you rolled back), with times; the engagements to USE and to AVOID; the gate (b-tight) and its Caddy fingerprint; the two QA Harness tenants the live gate left in place (not anomalies).
2. **Local main:** the head SHA; what is ahead of HPSM-light `origin/main` (afc10e9); nothing pushed.
3. **Every lane, branch and prepared step:** C11 (`s44/lane-c11` bfce726, HOLD) and C11-PINS (`s44/c11-merge`); the steps 9-10 merge messages and the edge route-table patch (paths); FX-REL/FX-LV/FX-ID/FX-PIN/S-m3 as merged. For each: branch, head, worktree path, chain state, next step.
4. **Every shell and subagent still running when you wrap:** name each, what it is doing, whether it holds the docker lock, and whether S45 must relaunch it. **Work that exists only in memory is lost when your pane closes.**
5. **The queue in order:** 9 F-API (+ the edge row), 10 F-WEB → feedback READY FOR QA, naming (b); the feedback batch's upgrade carries the FIRST database migration of the night (flag it in its head mail); S-p2 to BACKLOG beside S-m1/S-m2 (durable gate redesign); 11 C11 (STOP for Kam); 12 the credential round (A-m1, A-p2, N33/N09/N26, W4B-m3); D-M1 and D-M2 per the engine queue (demo impact measured on A and B first); F1 (no web path to a next draft) for Kam's Monday list; the ONE delta tier-1 gate after READY FOR QA.
6. **The upgrade toolkit:** its path, and the D-S44-30 fix (the base is now a required argument). **The next base is whatever is live after tonight's REPORT, never caf63fd.**
7. **Every ruling you received, with its mail timestamp**, so S45 does not re-ask. Tuesday's ANSWERs:
   - 09:56:56Z plan confirmed;
   - 10:01:01Z acceptance-gate routing;
   - 10:21:39Z FX-S7 final;
   - 10:30:10Z FX-PIN Q1-Q4;
   - 10:38:21Z FX-R/FX-REL order;
   - 10:45:04Z KAM GO on b-tight;
   - 11:59:52Z C11 HOLD;
   - 12:12:15Z roll to step 8 (with conditions);
   - 12:20:03Z live-delta verdict NOTICE.
   Plus your own seat decisions, D-S44-01 onward.

## HOLDS (unchanged)
- No push to HPSM-light.
- No Azure change without a head mail first. No live Caddy change without Kam's word relayed by Tuesday.
- No engagement or tenant you did not create is touched; Kam is testing.
- Mail `tuesday-agent@` only, with the seat in every subject.
- **Never `cockpit.sh rotate`:** Tuesday runs the successor through a new pane.
