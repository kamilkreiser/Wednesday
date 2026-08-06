---
date: 2026-08-06
type: correction
source: "Consolidation w=2 promotion of two retro lines that never became files: (1) wake_watch.sh armed with 3 defects found in its first hour (bash 3.2 assoc arrays, own outbound copies false-firing, bg-shell panes tripping the idle rule); (2) cockpit Fresh flow shipped with an untested interactive path — Kam: 'clicked fresh but it resumed'"
status: live
supersedes: ""
---

# Exercise a new mechanism in its real environment BEFORE arming it

**The lesson:** a script, watcher, hook or interactive flow is not shipped when
it is written and syntax-checked — it is shipped when it has been RUN in the
environment it will live in, on every branch a human or machine will actually
take. Arming first and debugging after means the first failure lands on Kam.

**The two occurrences (same week, same root cause, different costumes):**
1. **wake_watch.sh (08-05):** armed immediately, then three defects surfaced in
   the first hour — macOS bash 3.2 has no associative arrays; my own outbound
   mail copies fired the tripwire; panes running background shells tripped the
   idle rule. Each was findable in one dry run against the live cockpit.
2. **Cockpit Fresh flow (08-05, caught by Kam 08-06):** the branch was never
   driven with realistic keystrokes, so a buffered Enter auto-aborted the
   confirm and Fresh silently resumed. "It reads correct" is not a test.

**Why the existing rules didn't prevent it:** `always-verify-and-check` fires
strongly on *outcomes I report* ("is it done?") but weakly on *mechanisms I
arm* — a watcher that starts without erroring feels verified. It isn't: starting
is not behaving.

**How to apply:**
1. Before arming: run it once against the live environment and prove BOTH
   paths — the fire path (force the condition) and the quiet path (prove it
   does NOT fire on normal state). Both were what finally validated wake_watch.
2. Interactive prompts: walk every branch with the input a human really types,
   Enter included (piped-input tests count).
3. Portability check in the same breath: macOS ships bash 3.2 — no `declare -A`,
   no `timeout`. Assume the oldest shell on the drive's target machines.
4. Check the exec bit after any drive sync — 2026-08-06 the wake_watch exec bit
   was lost in transfer and `nohup` failed with "Permission denied". Syncs
   move content, not always modes.

**Related:** [[_ledger]], [[2026-08-06_artifact-presence-is-not-execution]],
[[2026-08-04_gitignore-artifacts-at-creation]] (same meta-failure: a retro line
is not a lesson until it is a file)
