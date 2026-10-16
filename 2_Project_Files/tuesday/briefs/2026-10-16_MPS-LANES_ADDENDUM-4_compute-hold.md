From Tuesday, 2026-10-16 14:07 AEDT, to EVERY MPS lane seat (B100-B109). Copy into your Briefs folder. SUPERSEDES item 4 of ADDENDUM-3 until Tuesday lifts it.
# MPS LANES ADDENDUM-4: COMPUTE HOLD — no heavy runs until Tuesday lifts it

**Why:** the machine's load is ~250 on 8 cores. A tier-1 QA gate for another project (a build fix Kam ruled "fix now") cannot finish its test run at this load, and it has priority.

**Until Tuesday sends ADDENDUM-5 lifting this (expected within ~60 minutes):**
1. Do NOT start: `dotnet build`, `dotnet test`, `npm ci`, `npm install`, `npm test`, `npm run build`, lint over the whole tree, Playwright/e2e, docker, or any full CI line.
2. If one of those is running NOW and has more than a few minutes left, stop YOUR OWN run (your own process ancestry only; never by name) and note it in STATUS.
3. Keep working: reading, writing code and tests, register rows, STATUS, Jira comments, and at most ONE single targeted test file at a time if it finishes in under a minute.
4. A READY line waits for the hold to lift (its full CI line is required). Write "READY PENDING CI (compute hold)" instead, with the branch and sha.
