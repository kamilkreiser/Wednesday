From Tuesday, 2026-10-16 14:44 AEDT, to EVERY MPS lane seat (B100-B109). Copy into your Briefs folder. SUPERSEDES rule 1 of ADDENDUM-5 (the load check alone let every lane start at once: load went 8 -> 143 in minutes).
# MPS LANES ADDENDUM-6: at most THREE heavy runs at a time, by slot

1. A heavy run (`dotnet build`/`test`, `npm ci`/`test`/`run build`, Playwright/e2e, a full CI line) needs a SLOT. Take one atomically from the PROJECT ROOT's git-ignored `.tools/`:
   `mkdir "<project root>/.tools/heavy-slot-1" 2>/dev/null || mkdir "<project root>/.tools/heavy-slot-2" 2>/dev/null || mkdir "<project root>/.tools/heavy-slot-3"`
   If all three exist, wait 3 minutes and try again. Write your brief id and the start time into a `holder` file inside the slot you took.
2. When your run ends (pass, fail or abort), remove ONLY your own slot: delete its `holder` file and `rmdir` it, in the same command block as the run's end (this is the one removal allowed, your own lock). Never touch another lane's slot. A slot older than 45 minutes whose holder's run has clearly ended: report it in STATUS, do not remove it.
3. One heavy run per lane at a time (unchanged). Targeted single test files that finish in under a minute need no slot.
4. Record the slot number and the load at start beside each result.
