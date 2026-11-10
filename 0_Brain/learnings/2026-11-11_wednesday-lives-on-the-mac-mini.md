---
date: 2026-11-11
type: preference
source: "Kam, terminal, 2026-11-11 ~09:4x: 'by the way. you are now on the mac mini as its always on and I will need to take the laptop with me from time to time' and 'spark also set up and connected from this machine'"
status: live
supersedes: ""
tier: W
---

# Wednesday's seat is the always-on Mac mini — the laptop travels

**The lesson:** From 2026-11-11, Wednesday (Secuura + general) runs on Kam's always-on Mac mini, not the laptop, so she never goes dark when he takes the laptop away. Treat the mini as the home machine: its machine-local dependencies are what PORTABILITY.md and doctor.sh must cover, and its local aliases are what my tools must resolve.

**Context:** Kam moved the seat after the DevMASTER -> Secuura_DEV drive copy (the copy ran on the laptop and was interrupted). The first boot on the mini found two missing machine-local pieces at once: no Homebrew rsync (macOS openrsync has no -X / --itemize-changes parity, so every copy and dry run failed rc 1), and the Spark's ssh alias is `hp-loan-spark` (NVIDIA Sync on the mini; zgx-15d5.local), not `Spark` (Studio) or `ZGX-Nano-G1n` (laptop). Both fixed at boot: `brew install rsync` (3.5.2) and a third fallback in local-model/spark/tunnel.sh (backup .pre-1111-mini).

**How to apply:**
1. At boot, `hostname` tells me which machine I am on; on the mini, Tuesday's seat is elsewhere (her chat lines carry seat KamilsMacStudio). Both coordinators still share this repo through git.
2. A tool that names a host alias, a binary path or a volume is checked on the mini before it is trusted. A `rc 1` from a copy tool is first read as "wrong binary", not "nothing to copy".
3. In zsh, `log` is a builtin: system logs are read with `/usr/bin/log`. Same family as the wrong-binary trap above.
