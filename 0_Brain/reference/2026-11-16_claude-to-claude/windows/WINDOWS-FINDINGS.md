# CoAgent on Windows: findings from the owner's PC (running list)

Source of truth for the next Windows test-hygiene lane and for BACKLOG entries. Each line cites its work order's results file in this folder.

| # | Where | Finding | Kind | Source |
|---|---|---|---|---|
| 1 | coagent-ipc | Pipe owner check works; pid calls report the dead creator (the first check's M-1 confirmed on real Windows) | confirms a fix | WO-1 items 16, 21, 22 |
| 2 | coagent-ipc | A same-user process can create a further pipe instance (logon-SID DACL grants FILE_CREATE_PIPE_INSTANCE) | known limit | WO-1 item 3 |
| 3 | coagent-ipc | accept can hand over an already-closed connection first (immediate EOF) | caller must handle | WO-1 item 18 |
| 4 | repo | Git for Windows' installer default (system config) sets core.autocrlf=true; include_str!-based source tests then fail (crypto f9). LF clone: crypto 75/0 | needs root .gitattributes (eol=lf) | WO-2 failure 1, WO-3 step 2 |
| 5 | coagent-relay tests/abuse.rs:62 | oversize_at_the_real_design_cap: the client's write gets WSAECONNRESET 10054 after the relay's cut; DETERMINISTIC (6/6) | test must accept an Err there and assert the relay's Oversize counter | WO-2, WO-3 |
| 6 | coagent-relay tests/candidates.rs:64 | a_closed_first_candidate...: Windows reports a refused loopback connect only after ~2.0 s (SYN retries), so the 500 ms budget reports timed_out | test assumption (platform timing) | WO-3 failure 2 |
| 7 | coagent-relay tests/hygiene.rs:130 | cargo tree --offline --target all needs every target's deps cached (libc 0.2.191 missing on Windows) | environment: run cargo fetch --locked once | WO-3 failure 3 |
| 8 | coagent-cli tests | tests/support, identity_cli, identity_file, cli.rs use std::os::unix: test targets do not build on Windows | needs cfg gating or Windows support | WO-2 step 3 |
| 9 | coagent-audit | All finished binaries green (259 passed) but debug property tests are very slow (qa_fix 1,970 s, gate_r4 1,281 s); a full run exceeds 2 h | timing: run in release or raise the cap | WO-3 |
| 10 | green on Windows | proto 7, crypto 75 (LF), roster 252, policy 24, ipc 26/0/1 (win-ipc head), hook 1, mcp 4, cli lib+bins 6, relay 122 of 125 | — | WO-1..WO-3 |
