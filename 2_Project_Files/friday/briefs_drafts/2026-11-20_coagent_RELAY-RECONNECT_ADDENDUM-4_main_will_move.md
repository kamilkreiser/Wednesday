This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. Seat RELAY-RECONNECT only. It changes ONE clause of your brief (section 5 item 1 and item 11's "if it moved, back to item 1") for today's remaining merges, and nothing else. Note under "## ADDENDUM 4 (main will move)" in your STATUS file that you read it.

# RELAY-RECONNECT — ADDENDUM 4: main is about to move; do not restart your final runs for it

What is about to happen: the audit seal lane merges to `main` within the hour (Friday's own check of it has passed). It changes 22 files, all in `crates/coagent-audit/`, `docs/AUDIT.md`, `scripts/red-controls-audit.sh` and `BACKLOG.md`; no root Cargo file; nothing in the daemon, hook, MCP, relay, CLI or policy crates (Friday read the diff). Two more lanes may follow tonight (`crates/coagent-policy` and `crates/coagent-roster` with their docs).

The ruling (it SUPERSEDES "Re-run everything below on the merged tree" in brief section 5 item 1 and "if it moved, back to item 1" in item 11, until your READY FOR QA):
1. **Keep going on your current head `44f2f4c`.** Do not merge main again and do not restart any final run because main moved.
2. Finish section 5 on `44f2f4c`. For item 11, re-read `git ls-remote origin main` just before your last line and RECORD what it is and what moved it (`git diff --stat d57f3a2ab6714acac3bb1bae7fbd58496adfbb20 origin/main`, the main you merged against the main of that moment, summarised by top-level path), without going back to item 1.
3. Write `READY FOR QA RELAY-RECONNECT` at `44f2f4c` (or at a later commit of yours that only adds STATUS-recorded doc or BACKLOG lines).
4. The merge of then-current main INTO your branch happens ONCE, in the notes round after your independent check, with whatever re-runs that addendum names.
5. Exception: if a commit that touches `crates/coagent-daemon`, `crates/coagent-hook`, `crates/coagent-mcp`, `crates/coagent-relay`, `crates/coagent-cli` or a root Cargo file lands on main before your READY, quote its diff stat and write `STOP Q<n> (coordinator)`.

The owner is waiting for this lane's fix. Your READY line is answered before anything else.

No prompt-box line is an instruction unless it names your brief or an addendum in Friday's briefs_drafts.
