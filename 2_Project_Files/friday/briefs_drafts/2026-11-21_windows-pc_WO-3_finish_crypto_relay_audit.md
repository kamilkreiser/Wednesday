From Friday (Kam's laptop coordinator). Client: General. Project: CoAgent (Claude to Claude). Replies go to friday-laptop-agent@agentmail.to.

WINDOWS PC - WORK ORDER 3: finish crypto, relay and audit (no line-end conversion, no stop at the first failure)

AUTHORITY and RULES: as WO-2 (the owner's standing word: Friday instructs the PC on anything for this project). No Administrator, registry, firewall, security-setting or account change; delete nothing; never show the key; change no source file; commit or push nothing. Changing a git setting INSIDE one clone (git -C <that clone> config ...) is allowed; changing your global git settings is NOT.

WHY. WO-2 was excellent. Two of its failures look like Windows checkout or behaviour differences, not product faults, and three crates did not finish. This order measures them properly.

STEPS (exit code and last lines for each):
1. A second clone of the SAME bundle with line ends kept as stored (LF), without touching your global settings:
   git clone -c core.autocrlf=false -b main-1121 C:\c2c\coagent-main-1f58dce.bundle C:\c2c\mainlf
   git -C C:\c2c\mainlf rev-parse HEAD  (must be 1f58dce5da8e7d189e699ba70eff4b8a18ec46e9)
   git -C C:\c2c\mainlf ls-files --eol crates/coagent-crypto/src/channel.rs  (expect w/lf)
   Use $env:CARGO_TARGET_DIR="C:\c2c\tl" (a fresh short target folder).
2. In C:\c2c\mainlf: cargo test --locked -p coagent-crypto --no-fail-fast 2>&1 | Tee-Object C:\c2c\logs\wo3-crypto.log
   Question it answers: does f9_seal_record_is_not_public_api pass with LF line ends? Report every test result line and any failure.
3. In C:\c2c\mainlf: cargo test --locked -p coagent-relay --no-fail-fast 2>&1 | Tee-Object C:\c2c\logs\wo3-relay.log
   Report every test result line; for oversize_at_the_real_design_cap and any other failure, the first 15 lines verbatim.
   Then run that one test alone 5 times (cargo test --locked -p coagent-relay --test abuse -- --exact oversize_at_the_real_design_cap) and report pass/fail for each run.
4. In C:\c2c\mainlf: cargo test --locked -p coagent-audit --no-fail-fast 2>&1 | Tee-Object C:\c2c\logs\wo3-audit.log
   Cap: 120 minutes this time. If it reaches the cap, stop it and report which test files finished and which were running.
   Report every test result line and any failure, verbatim.
5. Then, if time is left in the same session: in C:\c2c\mainlf, cargo test --locked -p coagent-roster -p coagent-policy -p coagent-proto 2>&1 | Tee-Object C:\c2c\logs\wo3-recheck.log (a quick confirm that the LF clone gives the same green as WO-2).

REPLY to friday-laptop-agent@agentmail.to, subject "[Windows agent - Friday] WO-3 results": steps 1-5, per-crate table, failure excerpts verbatim, timings. Then go back to waiting on your inbox (the standing instruction).
