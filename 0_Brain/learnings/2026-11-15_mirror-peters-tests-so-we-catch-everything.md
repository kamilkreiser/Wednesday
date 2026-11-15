---
date: 2026-11-15
type: principle
source: "Kam, live board 2026-11-15 16:11:32 view=wednesday, verbatim: 'thanks.  mirror our tests to his so we catch everythign' — in answer to Wednesday's 16:0x measurement that the one missing test tool is a running Docker daemon + a stack slot (every push reads PREFLIGHT INCOMPLETE 13/16; Schemathesis and Akto pre-merge never run)"
status: live
tier: W
---

# Mirror Peter's tests: our PRs run the same suites his process runs — the full preflight, Schemathesis pre-merge, Akto, Playwright and k6 — so nothing he would catch reaches him first

**The lesson:** "Tested" for a Secuura PR means tested the way Peter's process tests it, not the subset an agent can run without a stack. The suites defined in `systemTest/` (Schemathesis `run.py pre-merge`, Playwright API journeys, Akto OWASP scan, k6 performance) and all 16 pre-push preflight legs run against a local stack slot of the PR's tree. A run that skips legs is reported as skipped, and the gap is closed by bringing the stack up, not by accepting "PREFLIGHT INCOMPLETE" as normal.

**How to apply:**
1. The stack is a prerequisite, so keep it available: Docker Desktop running, one named slot (`SECUURA_STACK_SLOT`, `systemTest/run-in-slot.sh`), seeded admin credentials for that slot (`TEST_ADMIN_EMAIL` / `TEST_ADMIN_PASSWORD`, never printed). This Mac has 24 GB: a full slot (~36 containers) is brought up only when the floor leaves room (load1 < 7, memory checked), and never on Kintsugi or demo.
2. Gates and merge seats add a "Peter suites" leg once a slot exists: the PR's tree on the slot, the suites' own pass lines quoted verbatim, and a baseline run on develop beside it, so a red is attributable.
3. Card secuura-premerge-block-nine-prs-1113 = c still means our PR text carries no self-hold sentence; this lesson changes what is RUN, not what is written. Until the slot is live, merges continue on gate verdicts (Kam 15:40 "the recent merge rules override everything historic") and say the suites were not run.
4. Peter remains the reviewer of his own process; this is us running it first, not replacing him.

**Family:** [[2026-11-15_recent-merge-rules-override-historic-holds]] · [[2026-09-11_secuura-we-approve-and-merge-our-own-tested-work]]
