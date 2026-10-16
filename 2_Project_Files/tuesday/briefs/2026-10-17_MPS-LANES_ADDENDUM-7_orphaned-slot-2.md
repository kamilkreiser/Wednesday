From Tuesday, 2026-10-17 07:1x AEDT, to lane D (B103), as this project's live builder seat. One housekeeping task, then back to waiting for gate B163.
# MPS-LANES ADDENDUM-7: quarantine the ORPHANED heavy-slot-2 (gate B161's), after you verify it is orphaned

**Fact (Tuesday, 07:14):** `<project root>/.tools/heavy-slot-2/holder` reads `B161 2026-10-17 06:58:00 AEDT CI line m-all147 (stand-in new main)`. Gate B161 wrote its VERDICT and Tuesday closed its pane (%30) at ~07:05 while that run was still going. `pgrep -f qa-B161` = 0 processes. Its runner releases a slot only from its own live process, so nothing will ever release this one. It cuts the machine to two heavy slots for every MPS seat. Tuesday's error: the pane was closed before the run ended.

**Do, in this order, in ONE command block, and STOP if any check fails:**
1. Verify it is still orphaned: `pgrep -f qa-B161` prints nothing; the holder's first word is `B161`; `lsof +D '<project root>/.tools/heavy-slot-2'` shows no process.
2. Quarantine it, never delete: `mkdir -p '<project root>/.tools/_quarantine/2026-10-17_B161_orphaned-heavy-slot-2'`, then `mv '<project root>/.tools/heavy-slot-2' '<that dir>/'`. The slot is free again once the directory is gone from `.tools/`.
3. Read back: `ls -d '<project root>/.tools/heavy-slot-2'` is absent, and the quarantine holds `holder`.

Append one line to your STATUS: `HOUSEKEEPING: heavy-slot-2 (B161 orphan) quarantined <time>`. Do not touch slot 1 (B163's, live) or any other seat's files.
