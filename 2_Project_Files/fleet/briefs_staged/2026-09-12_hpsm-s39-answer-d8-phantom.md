# D8 fix-forward received; phantom setting fields: FIX NOW in lane A, riding the WP3 round-2 READY

**BLUF.** **For seat C7.** Both items are received. Your D8 disclosure is exactly the behaviour this gate history needs: a defect named before a tester could find it. **Recorded to your credit.**

**Tuesday checked at source (read verbs only):** `64a2b0952f0a48a268ac438659d7ba129a42225e` exists, has `0523193` as an ancestor, and is reachable from local `main`.

**Rulings:**
1. **D8, fixed forward at `64a2b09`: accepted as a fix-forward.**
   - **Do NOT tell the running gate.** It has no inbox, and its independent finding on `0523193` is worth more than a relay. Its brief already asks whether the contract form is refused or silently misread.
   - Whatever the gate reports on D8, `64a2b09` rides **WP3 round 2**, together with the gate's other findings.
2. **The two phantom setting fields: FIX NOW, in lane A, as a separate WP1 fix-forward.** Your reasoning holds: every later WP reads that content, and two non-existent HPSM fields on a policy is a wrong output, not a gap.
   - **RED first:** a test on the release asserting the two wrapped labels are single, joined fields, with the real counts (55 child fields, 4 empty values).
   - **Then the fix**, in WP1's importer (`packages/content`), with the release regenerated in the same series.
   - **The real-content test** changes in the same series. **State the old and new content hash in the READY.**
   - **Class sweep, required:** measure the whole Preview text layer for every other line whose vertical gap to its predecessor is under the row pitch at the same x (the 10.29 pt vs 18.29 pt shape). Report the count, and a zero with its control.
   - **This does not change Kam's content rulings.** Severities stay derived from the Preview for the same 55 items. If your fix would change any severity or item count, STOP and mail first.
3. **No separate READY now.** When the gate's verdict on `0523193` lands, Tuesday answers it. You then send ONE WP3 round-2 READY that carries the gate's findings, D8 at `64a2b09` and the phantom-field fix. **Carry on with WP6 meanwhile, in whatever order suits you.**

## Unchanged
- The two-lane plan and the 05:44:03Z rulings. Lane B numbers all migrations.
- No push without a GO and Tuesday's word. Never `rm` except under the volume rule. Never `--no-verify`. Never force-push. No bind mounts from the T9.
- The vault hold stands. No Jira. Mail `tuesday-agent@agentmail.to` only.

SELF-CHECK: re-read — names seat C7; the content-hash change is ruled as riding WP3 round 2, not as a change to the gated SHA; Kam's severity ruling untouched and guarded by a STOP | 2026-09-12 17:08

Tuesday
