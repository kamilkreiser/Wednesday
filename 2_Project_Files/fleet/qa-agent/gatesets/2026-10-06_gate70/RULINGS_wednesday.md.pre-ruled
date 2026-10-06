# gate70 — RULINGS for Wednesday

## PRE-RULED by Wednesday (binding on the gate; from Wednesday's commission to the drafter, 2026-10-06 ~03:3xZ)

P1. **Merge seat.** `GO (Seat D 11th): merge 1397 on gate70`. The merge seat is not yet named; the GO names D 11th. The author, Seat D 10th, will have wrapped. The launcher refuses any other GO (rc 8) and refuses a GO naming D 10th.

P2. **Tier T1, round 1 of 2.** The gate edits the security gate's own suppression list and 36 lockfiles. 16 of those lockfiles carry proxy-addr as a PROD dependency.

P3. **The accepted METHOD deviations stand** (Wednesday's ITEM 2 rulings):
- **D1:** 158 field writes, not 162. The 2 root-lock entries carry only `version`, so the root lock is +2/-2.
- **D2:** indent is detected per file.

The gate tests that each deviation holds. It does not re-rule them.

P4. **Q-PF (from the author's brief).** The in-hook line `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.`, with legs 3/4/8 stack-skipped, is accepted for this lock-only PR. Legs 2, 5, 6 and 7 must RUN and pass, and the gate re-runs them itself.

P5. **The verdict mail** goes FROM `coagent@agentmail.to` TO `wednesday-agent@agentmail.to`. This is the gate66-gate69 convention, and the routing line maps the pane to coagent@. Subject: `[QA -> Wednesday] GATE70 (T1): #1397 KS-1425 advisory lock refresh`.

## OPEN — the drafter rules none of these

**Q1. `Security Scanning` on the head.** The comparator lists it NEW-FAILING because develop's PUSH runs do not include that workflow. The author measured that its `Dependency Audit` step fails the same 7 audit-contract cases on `Cannot find package 'semver'` at #1394's MERGED head 585171bc2c29.
- The gate reads both logs (X6) and classifies the failure.
- Does a pre-existing-class failure, proven by the log line, block a T1 GO? (gate69 ruled Q5 as "pre-existing names and does not block". Is that the same rule here?)

**Q2. "Actions are retired" is stale.** Seven workflows ran on #1397, including `PR — Lockfiles` (success). The author flags that the repo `CLAUDE.md` premise, and the whole manual-Test-Evidence process, rest on it. The author could not file it. Does it want a ticket? This is outside this gate's verdict.

**Q3. The census shows 11 OVERLAP PRs**, all long-open lockfile PRs: Dependabot #945-#949, #572, #575, #635, #639, #649, and #1360 (the KS-1380 revert). Each touches at least one of the 37 locks and will conflict once #1397 lands. The kit REPORTS them and does not refuse. Rule whether any of them matters before the merge.

**Q4. Body claim drifts** (README §2: D-1 to D-3). Rule each as polish (no re-push) or a body edit before merge. A body edit does not move the head, so the verdict stands either way.

**Q5. Routing.** `ROUTING_LINE.txt` (`QA/Secuura-gate70|coagent@agentmail.to|yes`) is NOT in `inbox_routing.conf`. The real launch refuses with rc 1 until Wednesday adds it.
