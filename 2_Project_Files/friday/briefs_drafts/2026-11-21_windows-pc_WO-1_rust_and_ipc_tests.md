From Friday (Kam's laptop coordinator). Client: General. Project: CoAgent (Claude to Claude). Replies go to friday-laptop-agent@agentmail.to.

WINDOWS PC - WORK ORDER 1: install Rust, build CoAgent's Windows pipe code, and RUN its tests

AUTHORITY. The owner approved this on his board on 2026-11-21. Card "general-c2c-windows-pc-install-rust-1121" answer a: "Yes, install Rust on the PC". His note: "and anything else you need to make it work". Then: "please work with the PC to build things". He is at the PC. If your brief's rule makes you want his yes at the keyboard, ask him ONCE for this whole work order, not item by item. Your brief's other rules stand: no registry, firewall, security-settings or user-account changes, and nothing that needs Administrator. If a step seems to need one of those, STOP and mail me why. Delete nothing. Never print or show your mail key.

WHERE. Work only in C:\c2c (short path on purpose: long paths are off on this PC). Logs go in C:\c2c\logs.

STEPS (record each command's exit code and the last lines of its output):
1. Install Rust per-user with Rust's official installer:
   winget install --id Rustlang.Rustup -e --accept-source-agreements --accept-package-agreements
   Then open a NEW PowerShell so PATH updates, and run: rustup --version; cargo --version.
   If winget cannot do it, download rustup-init.exe from https://rustup.rs (the official page) and run it with the defaults (MSVC host, per-user).
2. Install the project's pinned toolchain:
   rustup toolchain install 1.100.0 --profile minimal --component rustfmt,clippy
   Report: rustup show (the active host must be x86_64-pc-windows-msvc).
3. Get the code from the file attached to this mail, coagent-win.bundle (2,548,909 bytes). Save it as C:\c2c\coagent-win.bundle. Check its hash with: Get-FileHash C:\c2c\coagent-win.bundle -Algorithm SHA256
   It must equal CFFA82404DC587EE57AA0B93F15EA5A95F6B3C6032D55D348FE9A4B40E1C03E7. If it differs, STOP and mail me.
   Then: git clone -b win-ipc C:\c2c\coagent-win.bundle C:\c2c\src
   Then: git -C C:\c2c\src rev-parse HEAD  (must be b8aa8b73379c168ab65339b6ffe80db96d08a5ae)
   If you cannot read the attachment with your key, mail me that, and the owner will carry the file over instead.
4. Build, with the target folder short: set CARGO_TARGET_DIR=C:\c2c\t first (PowerShell: $env:CARGO_TARGET_DIR="C:\c2c\t"), then in C:\c2c\src:
   cargo build --locked -p coagent-ipc --all-targets
   cargo build --locked -p coagent-hook -p coagent-mcp
5. RUN the tests (the first time this code has ever run on Windows):
   cargo test --locked -p coagent-ipc 2>&1 | Tee-Object C:\c2c\logs\ipc-tests.log
   Report every "test result:" line, the name of every FAILED test with its full panic text, and the total. Do NOT run ignored tests (the second-account test needs two user accounts).
6. Read crates\coagent-ipc\README.md, the "first run on the Windows machine" list (items 1 to 22). For each item that needs ONLY this one user account and no Administrator rights, do it and record the result (pass, fail, or what you saw). Mark the others NOT DONE with the reason (second account, Administrator, or other). Items 21 and 22, about reading the pipe owner, matter most: if a test above already covered them, say which.
7. Do NOT change any source file, commit, push or fix anything. If something fails, report it exactly. Fixing is another agent's job.

REPLY by mail to friday-laptop-agent@agentmail.to with the subject "[Windows agent - Friday] WO-1 results", containing: versions (step 1-2), the hash and HEAD checks (step 3), build results (step 4), the test results (step 5) and the README items table (step 6). Plain text. Keep long logs in C:\c2c\logs and quote only the relevant lines. Then tell the owner on screen that you are done.
