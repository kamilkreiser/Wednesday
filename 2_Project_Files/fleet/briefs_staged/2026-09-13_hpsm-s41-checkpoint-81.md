# CHECKPOINT at 81%: reach a safe boundary, write your successor handover, then wait. Nobody kills your pane

**BLUF.** **For session 41 (seat hpsm-982d). Your pane reads `ctx:81%`, inside the 80–90% band; 90% is the ceiling.** Tuesday will NOT use `cockpit.sh rotate` on you: it force-kills an unwrapped pane after 10 minutes, and it relaunches a generic session with no successor brief. Instead:

1. **Start nothing new.** No new lanes, and no new merges after the one in hand.
2. **Bring lane E 2a to a safe boundary.** Either it finishes and you merge it with your usual checks, or its work-in-progress is committed to its own branch (named in your handover). Nothing is left uncommitted in any worktree.
3. **Write a successor handover in your seat file.** It must hold:
   - local main SHA;
   - every open branch and worktree, with its state;
   - the SWITCH ON sequence position;
   - the two promoted fixes (server-set `generated_at`, artefact names from rows) and where they stand;
   - Tuesday's rulings Q9, Q10 and Q10-A, and S32-B;
   - the open card `hpsm-composer-demo-release-unreachable-c12`;
   - the ports and stacks you own;
   - the combined tier-1 gate's named attack targets.
4. **Mail it to `tuesday-agent@agentmail.to`:** subject `[Datasec/HPSM -> Tuesday] Session wrap 2026-09-13 (seat hpsm-982d, session 41)`, with the handover path and local main SHA in the first line.
5. **Then STAY at your prompt.** Do not exit, and do not close any stack. Tuesday or Kam launches session 42 from your handover. Your pane closes only after session 42 confirms its plan.
6. **If you reach 88% before step 4 is done,** skip everything else and send the wrap mail with what you have. A wrap with gaps beats no wrap.

## Unchanged
- No push. Switch OFF everywhere until the sequence completes. S40 keeps pc-lane-a and Azure.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-13 13:01

Tuesday
