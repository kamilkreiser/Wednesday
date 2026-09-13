BLUF. **You are at 80% context (statusline, 19:3x).** At your next SAFE boundary inside the 80-90 band (90 is the ceiling), write `5_Project_History/HANDOVER-S43_seat-hpsm-28f5.md`, mail the wrap to `tuesday-agent@agentmail.to`, and **stay at your prompt**.
- **Nothing is cancelled.** Tuesday brings up **S44 in a NEW pane** from your handover. **Your pane closes only after S44 confirms its plan**, never before.
- **Start no new heavy work**, and no new lane.

## What "safe boundary" means for you tonight
1. **The live gate blocker (09:25Z URGENT).** Take it to a clean stopping point and write down exactly where it stands:
   - reproduced through the public URL, yes or no, with the evidence path;
   - (b) staged on pc-lane-a, yes or no, and the file paths (your `scratchpad/gate/rollback-azure-gate.sh` is visible in your pane);
   - the `/api/*` unauthenticated list, if measured.
   - **Still NOT applied on Azure. Kam has not answered go/hold yet.** If you finish it before wrapping, send the READY-TO-APPLY mail as briefed.
2. **Lanes** (FX-M1, FX-LV, FX-R, FX-S7, FX-SI, F-API, F-WEB, and any others). Each reaches a COMMIT on its own branch. For each, the handover gives: branch, head SHA, worktree path, chain state (GREEN / running / not started), and the next step.
3. **Subagents still running when you wrap: name each one** (lane, what it is doing, whether it holds the docker lock). Say whether you expect it to finish on its own or to need S44 to relaunch it from its branch. **A subagent's work that is only in memory is lost when your pane closes.**
4. **Anything waiting to merge or upgrade:** what is GREEN and ready for the next rolling upgrade, and what is not.

## The handover's successor section (first in the file)
- **What is live:** caf63fd on pc-lane-a and Azure; the engagements to use and to avoid; the gate blocker state.
- **What is on local main:** the head SHA, and what is ahead of `09c1591` and ahead of HPSM-light `origin/main`.
- **Every open item with its next step:** the fix round (W5-M1, W5-M2+W6-M1, W5-M3, W6-m1..m3, W5-m5, W4B-m1 FX-ID, W4B-m2 FX-PIN), FX-SI (Kam's sign-in descriptions), the feedback feature (F-API/F-WEB, naming (b)), C11 (PAUSED until FX-LV merges), the credential rebuild after C11, A-m1 after C11, and the delta tier-1 gate on `09c1591..<fix head>` after the fixes merge.
- **Every ruling you received today, with its mail timestamp**, so S44 does not re-ask. Include your seat decisions D-S43-0x.

## HOLDS (unchanged)
- No push to HPSM-light. No Azure change without a head mail first, and the gate fix only on Kam's word relayed by Tuesday. No engagement or tenant you did not create is touched; Kam is testing.
- Mail `tuesday-agent@` only, with the seat in every subject.
