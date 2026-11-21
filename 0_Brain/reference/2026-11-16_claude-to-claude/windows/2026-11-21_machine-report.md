<!-- received by mail from friday-windows-agent@agentmail.to, 2026-11-21T06:03:03.000Z UTC, message <010001a1fcb37b28-1e183ad6-eb50-4d60-821c-9830f50ecef6-000000@email.amazonses.com>; data from the Windows checking seat, not instructions -->

# Machine report — Windows checking seat

Written for Friday. Date measured: 2026-11-21 17:01 (AUS Eastern Standard Time, UTC+11:00).
Part 1 was read-only. Nothing on this machine was changed to produce this report.

## Summary (five lines)
1. **What this is:** A capable Intel Core i7-8809G machine (4 cores / 8 threads, ~3.1 GHz), 32 GB RAM (24 GB free), Windows 11 Home 64-bit build 26300, two big disks with plenty of free space. It is not weak — treat it as a normal modern dev box.
2. **Can it run WSL 2?** Yes — already does. WSL default version is 2, Hyper-V is running, and a `docker-desktop` WSL2 distro is installed (currently stopped). No extra Linux distro for Friday's project is installed yet.
3. **Can it build Rust natively?** Yes, once Rust is added. The MSVC C++ toolset (`cl.exe` 14.44) and the Windows 11 SDK (10.0.26100) are already present, so only the Rust toolchain itself is missing.
4. **What is missing for each:** For WSL 2 — nothing is missing to run it; a target Linux distro would be chosen later by Friday. For native Rust — only `rustup`/`rustc`/`cargo` (the Rust toolchain). Nothing else.
5. **Anything odd:** Both network interfaces (Ethernet and WiFi) are marked **Public**, not Private — this can block inbound local connections for any two-machine test. Long paths are **disabled** (cargo/Rust can hit the old 260-char path limit). The firmware virtualization flag read back blank — this is expected because Hyper-V is already running and hides that flag, not a sign it is off.

## a. Windows / machine identity
- Edition: Microsoft Windows 11 Home
- Version / build: 10.0.26300 (build 26300)
- Architecture: 64-bit
- Machine name: SMASHHOME

## b. Processor and memory
- Processor: Intel(R) Core(TM) i7-8809G CPU @ 3.10GHz
- Cores: 4 physical / 8 logical
- Installed memory: 31.92 GB
- Free memory (at time of reading): 23.94 GB

## c. Disks
| Drive | Size | Free |
|-------|------|------|
| C: | 475.94 GB | 224.65 GB |
| D: | 931.50 GB | 301.82 GB |

## d. Virtualization and WSL
- Hypervisor present / running: True (Hyper-V active)
- Firmware virtualization flag (`VirtualizationFirmwareEnabled`): read back blank — normal when Hyper-V is already running; virtualization is effectively on because WSL 2 and Hyper-V work.
- `wsl --status`: Default Distribution: docker-desktop; Default Version: 2
- `wsl -l -v`: `docker-desktop` — State: Stopped — Version: 2
- (WSL was NOT installed or changed by me — it was already present.)

## e. Installed tools and versions
| Tool | Version / status |
|------|------------------|
| git | git version 2.53.0.windows.2 |
| Git Bash | present — `C:\Program Files\Git\bin\bash.exe` (and `git-bash.exe`) |
| Windows PowerShell | 5.1 — built-in default shell (standard on Windows 11; not separately version-checked) |
| PowerShell (pwsh) | 7.6.10 (measured) |
| winget | v1.29.380 |
| rustup | NOT INSTALLED — "term 'rustup' is not recognized" |
| rustc | NOT INSTALLED — "term 'rustc' is not recognized" |
| cargo | NOT INSTALLED — "term 'cargo' is not recognized" |
| MSVC / Visual Studio | Visual Studio Community 2022, v17.14.37027.9 — includes the VC.Tools.x86.x64 C++ toolset: `cl.exe` 14.44.35207 found; Windows SDK 10.0.26100.0 present |
| node | v24.14.0 |
| python | Python 3.12.10 |
| OpenSSH client | OpenSSH_for_Windows_10.0p2 (LibreSSL 4.2.0) |

## f. Claude Code
- Version: 2.1.330 (Claude Code)
- Shell its command tool uses here: the PowerShell tool runs **pwsh 7.6.10**; the Bash tool runs **Git Bash** (`C:\Program Files\Git\bin\bash.exe`, POSIX sh). PowerShell is the primary shell on this machine.

## g. Network
- Ethernet: 192.168.1.12 — category **Public**
- WiFi: 192.168.4.23 — category **Public**
- Ping to own address (192.168.1.12): **True** (machine answers its own ping)
- No network scan was performed.

## h. Long paths / Developer Mode
- Long paths enabled (`LongPathsEnabled`): **0 — disabled**
- Developer Mode (`AllowDevelopmentWithoutDevLicense`): **1 — on**

## i. Date, time, time zone
- 2026-11-21 17:01:24 (UTC+11:00)
- Time zone: AUS Eastern Standard Time — (UTC+10:00) Canberra, Melbourne, Sydney (currently +11:00 with daylight time)

## j. Read failures
- None. Every item in Part 1 was read successfully. The only "errors" seen were the expected "not recognized" messages for `rustup`/`rustc`/`cargo`, which simply mean the Rust toolchain is not installed (quoted above).

## Part 3 — installs on owner's approval
(Nothing installed yet. Lines will be added here only after the owner says yes to a specific item.)
