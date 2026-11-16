# Friday's independent re-run of G1 and G2 (2026-11-17 00:2x, laptop)

Method: copied `spikes/lib`, `spikes/G1-deny-blocks-write`, `spikes/G2-dead-daemon-blocks` (scripts only; no `work/`, `raw/`, `output.txt`) from the project repo at commit 46b982d into Friday's session scratchpad under `verify_m0/spikes/`, and ran each `run.sh` there. Claude Code 2.1.325, model claude-haiku-5-5 (read by the script from models_latest.json).

## G1 — REPRODUCED
`SUMMARY G1-deny-blocks-write: pass=22 fail=0`, rc=0. CANARY.txt exists in the four control case directories (no hook, hook allow; default and bypassPermissions) and in neither deny case directory (checked with `find`).

## G2 — the BLOCK is reproduced; two assertions about the MESSAGE TEXT failed, and the fault is in the test instrument
`SUMMARY G2-dead-daemon-blocks: pass=24 fail=2`, rc=1 (the seat's own run: pass=26 fail=0).
- All five "expect absent" cases have no CANARY.txt (killed-before, killed-midcall, crash-onfailure-block, missing-binary, timeout-onfailure-block). All five controls created the file. So the liveness invariant held in Friday's run.
- The two FAILs: `crash-onfailure-block` and `timeout-onfailure-block`: "tool_result does not contain 'onFailure is "block"'".
- Cause, measured: the phrase IS in the raw stream (`grep -o -i -c 'blocking because onFailure is'` = 1 in each raw `.stream.jsonl`). `lib/stream_summary.py` line 25 keeps only the first 400 characters of a tool_result (`str(c)[:400]`), and the hook error text begins with the full hook command line, which contains the install path twice. Friday's scratchpad path is longer than the project path, so the phrase fell past character 400.
- Consequence: the assertion's result depends on the length of the directory the repo is checked out in. On a deeper path it reports a false FAIL; the same shape could hide a real change in the message.

## Return to the seat (one item)
Make text assertions read the untruncated tool_result (truncate only for display), then re-run G2 from a path at least as long as Friday's scratchpad path to show it no longer depends on path length. Sweep the other spikes' `run.sh` for assertions made through `summ … --json` on `text`.
