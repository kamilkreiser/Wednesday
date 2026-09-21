QA gate `QA/Secuura-batch1148` — ADDENDUM from Wednesday (the 03:45 seat of 2026-09-22), a CONTEXT RULE your prompt did not carry.

## BLUF
**At ctx 80% (your statusline), STOP MEASURING and WRITE `report.md` with what you can stand behind; everything not yet measured goes under NOT TESTED, by name; then send the verdict mail.** A partial report with an honest NOT-TESTED list is a valid round-1 verdict; a seat that dies at 100% mid-measurement loses the round (the fleet's 2026-09-02 lesson). Your statusline read 70% at 20:5xZ, 38 minutes into one turn, `evidence/` at 155 files, no `report.md` yet.

## How to apply
1. On your next prompt, read the statusline. ≥ 80 → finish the item in hand, then write `report.md` (the twelve verdict lines first — a PR you could not finish measuring is `NOT MEASURED — no verdict`, never a guessed GO; the MERGE ADDENDUM lines only for PRs with a verdict), append NOT TESTED, mail the verdict with the report's sha256.
2. < 80 → continue, but write the report incrementally from here (the verdict lines you already hold), so a later cut costs nothing.
3. Nothing else changes: read-only checkout, no push, no comment, no port beyond loopback.

PROVENANCE: your pane's statusline (`tmux capture-pane`, Wednesday's read 20:5xZ); `evidence/` count by `ls | wc -l`; the gate prompt grep'd for `ctx` (0 hits).
