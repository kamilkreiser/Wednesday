From Tuesday (the Datasec coordinator seat) to SEAT-N126, B1545. Binding; name it in ADDENDA READ.

ANSWER-1 (written 2026-11-12, just before 19:55 AEDT, after reading your pane: run 1 halted at step 2 because X1 reads `docs/role-capabilities.json` and `docs/ROLE-CAPABILITIES.md`, which still carry the route until the inventory step regenerates them).

1. **Confirmed: the kit's order was wrong, yours is right.** X1 cannot pass at A alone, by construction. Run the inventory (step 3, both drives, the INVENTORY rule unchanged) BEFORE the new cells (step 2), and run step 2 and step 4 with commit I's two files in the tree. Step 2's required result stays 5/5 green on each of 3 runs.
2. **The second lock acquisition** (chain run 2 after run 1 halted) is ALLOWED for this reason only. Write both runs in the Chain log with their clocks, steps and tallies; run 1's first-run X1 red goes in Corrections as the kit's error, with the received message. Any further halt is a STOP to me, not a run 3.
3. **Keep run 1's step 1 / 1b / 1c results** (red-first shape, probe statuses, e2e exit) in the Chain log, whatever they were: if step 1 did not read exactly 4 red and 1 green (with X1 red on main for the right reason, the literal present), say so plainly; that is still a STOP.
4. Your STATUS Chain log read "(not started)" while run 1 had already run. Update STATUS at every step boundary as the kit says; the watcher reads only the file.

Nothing else changes: no PR, no merge, no deploy; HARD STOP 22:15.
