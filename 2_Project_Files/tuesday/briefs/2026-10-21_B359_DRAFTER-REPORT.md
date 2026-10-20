# B359 drafter report (Sonnet 5.5, read-only), 2026-10-21 02:44-02:50 AEDT

Kit: `2026-10-21_B359_SEAT-G24_nexusai-gate-pr101-tier2.md` (PR #101 @ 6e947f4d, tier 2, routing row G2, Sonnet; tier-1 escalation if an auth/SCIM test guarantee is weakened). Unstamped: 3 slots (MAIN_SHA x2, STAMP_TIME x1) on 2 lines; last line `READ-WHOLE-BY-TUESDAY: PENDING`. Save a `.pre-stamp` copy before stamping.

## Facts the drafter MEASURED that change Tuesday's picture
1. **Alert #151 (RD-810, `js/file-access-to-http`) is already OPEN on `refs/pull/101/head` at `tests/uat-run.js:43`** (rule severity warning, security severity medium, instance commit 6e947f4d). Same alert NUMBER as main's (`:30`, instance d463f881), so not a new number, but an open instance on the PR ref. The builder left this as "may or may not". All three `Analyze` runs and the `CodeQL` check are completed/success at 02:47 (the `CodeQL` check read `neutral` at 02:45, mid-run); `build` still in progress. The kit makes this a reported finding (Minor by the drafter's reading), never a dismissal; the policy reading is Tuesday's/Kam's.
2. PR #101 is **non-draft** (Tuesday opened it so CodeQL runs); `mergeable` true, state unstable then.
3. **Main = the PR's base** (d463f881), so mode 0; r5 merged-tree is conditional on main moving.
4. **#97 and #67 overlap #101 in exactly `scripts/verify-expected-counts.json`** (comm -12 on file lists). `backend/validators.js` is not in #101.
5. **Jest lock is HELD at 02:44 by gate 29** (`nexusai-jest.lock` present, queue empty); load1 10-17. The gate will wait.
6. `deploy-demo.yml` `on:` = push + workflow_dispatch; a PR triggers no deploy; the head's runs are Gitleaks Scan, Build, npm-audit and dynamic CodeQL.
7. The three test-file diffs are +2/-0 each (nothing removed). The new test has a module-scope refusal to require the script unless `https.request` is mocked.

## Decisions I made (flagged)
- **PANE**: shape source convention is `QA/NexusAI-gate<sequence>` (inbox_routing.conf:231-238), so the kit uses **`QA/NexusAI-gate33`**, not `gate101`. Routing line needed: `QA/NexusAI-gate33|tuesday-agent@agentmail.to|no`, after line 238.
- The NexusAI shape is **kit + launcher**; the launcher for this gate does NOT exist (MEASURED); the kit's FILL AT STAMP says to derive `launch_qa_nexusai_gate33.sh` from gate 32's (738 lines) in a separate job.
- The new test is NOT run against main's old `uat-run.js` (it would execute the old replay on require, albeit mocked): the red-at-main arm is RELAYED/NOT RUN; M-default is the in-gate equivalent. The no-socket proof is the gate's own spy with a positive control that never forwards.
- Beyond your list I added: guard-deleted copies (gate 32's m-g1 shape), a NOOP mutant, optional M-guard/M-agent mutants, the c57 id-superset run, an H1a (`--update-counts`, scratch clone) plus H1b (plain verify) pair, a sibling census of the three files, and a #97/#67 merge-tree reading if their objects are in the mirror.
- Opus id not typed (read from models_latest.json).

## Not done / UNMEASURED
No jest, mutant, node, npm or lock ticket. Did not read the builder's evidence folder, Charter/BRIEF_TEMPLATE, gate 29's files, or CLARIFICATIONS above line 2362 (the gate re-scans). Did not verify the builder's per-mutant isolation (RELAYED). Did not check whether #97/#67 head objects exist in the local repo.

## Open questions with recommended answers
1. Pane `gate33` vs `gate101`? Recommend gate33 (convention).
2. Launch now or after gate 29 releases the lock? Recommend launch now (lock-free rows first); expect a long queue wait.
3. Run both H1a and H1b full verifies (~25 min each)? Recommend yes, H1b first priority; allow H1a NOT RUN if starved.
4. Severity of #151 on the PR ref? Recommend Minor, reported; Kam decides if a moved pre-existing alert counts as "new" under C-190.
5. Who writes the gate-33 launcher? Recommend a separate launcher-drafting job from the gate 32 launcher.
