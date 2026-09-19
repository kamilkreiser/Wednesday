# READY — KS-1269 (Ornith, briefed, code_patch) — PASS 7/7 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-19_ks1269-ornith35b-night/out.md.checker/section_N.diff`, each applied with its `section_N.diff.opts`** (section_1 = `Blockchain/Dev/services/vc-issuer/src/routes/status.ts`; section_2 = the NEW suite `src/__tests__/ks1269-status-revoke-refuses-a-non-integer-index.test.ts`).

**Held 10:42 2026-09-19 by the 10:2x Wednesday seat after a source read.** Tip `3c447abc7`. `POST /api/status/:id/revoke` now answers 400 for a PRESENT `index` that is not an integer (`index: {}` used to answer 200 and revoke); absent `index` and `-1` stay admitted. **Refs KS-1269, never Closes:** `/revoke` only — `/unrevoke` shares the request schema and still ignores `index` (the residual, say so in the PR body). **Premise carried, not re-read by anyone:** the `-1` exception is the KS-1269 ticket's quote of the KS-662 ruling — the raising seat reads KS-662 before the PR body cites it. Same file as held READY_KS-692 (its hunk :31-43), no overlap. Runtime change → stays In Progress on merge (§5f). Tier 2 at the gate (input validation, not an auth surface).

## Source read (Wednesday)
- section_1 (product): the brief's 4 `+` lines in the product hunk (checker A3c/A3i byte-exact).
- section_2 (new suite): 77/77 non-blank line bodies present in the brief; crossed controls KS-1276 77/77 absent, KS-1260 75/77 absent — discriminating.
- Checker A4 red-first 3 failed / 6 at the tip (the 3 🔴 by assertion); A5 6/6 after; A6 whole vc-issuer suite no new red; A7 tsc rc 0.

**HELD. Not raised.**

---
## Checker verdict (verbatim tail)
after suite rc=0 total=114 passed=114 failed=0 suites_failed=0 loaded=1 failed_names=[]
baseline: total=108 failed=0 | after: total=114 failed=0
develop's own reds (attributed, not counted): []
NEW reds: []
reds fixed by the patch: []
tests added: 6
PASS A6 whole services/vc-issuer suite: no NEW red vs the untouched tip
PASS A7 tsc --noEmit for services/vc-issuer: rc 0 after the patch (baseline rc=0)
INFO tsc test-file types: could not tell services/vc-issuer's test runner (jest:[jest, ts-jest] vitest:[vitest.config.ts, scripts.test=vitest, vitest]) — kept the old default --types node,vitest/globals
INFO tsc on the test file alone (--types node,vitest/globals): rc=0 (0 lines; not gated — the runner does not type-check and the service tsconfig excludes __tests__)
SUMMARY files=2 +86/-0 test=src/__tests__/ks1269-status-revoke-refuses-a-non-integer-index.test.ts red_first=yes apply_mode=strict
RESULT: PASS (7/7)
