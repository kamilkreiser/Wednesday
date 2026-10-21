# B429 ADDENDUM-CKPT — from Tuesday, Datasec / HPSM-POC, written 02:44:56 AEDT. Your context reads 50% and nothing durable exists yet (no STATUS file; `git ls-remote origin 'refs/heads/b429*'` prints nothing, read by Tuesday just before this file).

**BLUF: keep going on Phase A; nothing in the brief changes. Make your progress durable now, and plan your context.** This is not ADDENDUM-1 (that stays reserved for the Phase B GO).

## RULED BY TUESDAY
1. **Now, before the next heavy step:** create `1_Project_Definition/Briefs/2026-10-22_B429_STATUS.md` with Step 0 and a PROGRESS block: commit 1's sha and what it holds, the trees, the baseline counts you have, what remains (commits 2-3, the checks). Update PROGRESS after each commit.
2. **Push `b429/telemetry-224` after each commit whose own suites are green** (branch only, never main, never force; the brief's identity and `GIT_SSH_COMMAND` rules apply; `ls-remote` after each push, quoted in PROGRESS). An early push is allowed by this addendum; the PR is still Tuesday's.
3. **Context:** if your statusline passes 75% before READY FOR QA, finish the step you are in, write a RESUME block in STATUS (branch sha on origin, the next command to run, anything not yet written down), release your processes, and end with `STOPPED: NEEDS TUESDAY context at <n>% — resume from <sha7>`. Tuesday then starts a successor on the same brief.

## Mechanics
Copy this file unchanged into `1_Project_Definition/Briefs/`, `cmp` rc 0, quote its sha256 in STATUS. Fences unchanged.
