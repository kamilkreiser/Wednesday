# READY — KS-1269-U (Ornith, briefed, code_patch) — PASS 7/7 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-19_ks1269-ornith35b-night2/out.md.checker/section_N.diff`, each applied with its `section_N.diff.opts`** (section_1 = `Blockchain/Dev/services/vc-issuer/src/routes/status.ts` above `:295 manager.unrevoke(credentialId);`; section_2 = NEW `src/__tests__/ks1269-status-unrevoke-refuses-a-non-integer-index.test.ts`).

**Held 11:29 2026-09-19 by the 10:2x Wednesday seat after a source read.** Tip `3c447abc7`. `POST /api/status/:id/unrevoke` answers 400 for a PRESENT non-integer `index`; absent stays admitted. The `/unrevoke` twin of READY_KS-1269 (/revoke, @@ -230): 62 lines apart; both orders apply strict to an identical status.ts, vc-issuer 119/119 + tsc 0 each order (the brief-writer's proof). **Raise it in the SAME PR as READY_KS-1269** (one ticket, one test pass) — **Refs KS-1269**. **Pins NOTHING about `-1`:** KS-662's -1 allowance is the /revoke row; its 2026-08-27 comment lists `/unrevoke {index:-1} → 200` as NON-RULED — a ruling for Kam (Monday list), unchanged by this fix. Anchor cost, stated: an unknown list/credential still 404s before a bad index 400s. Runtime change → stays In Progress on merge (§5f); tier 2.

## Source read (Wednesday)
- Model `+` lines 75/75 non-blank present in the KS-1269-U brief; 0 `-` lines. Crossed controls: KS-1276 brief 75/75 absent; the sibling KS-1269 brief 21/75 absent (shared test scaffolding — a weaker discriminator, stated).
- Checker A1-A7 PASS: strict apply; A3c 4/4 brief `+` lines in the product hunk; A4 red-first at the tip; A5 green after; A6 no new vc-issuer red; A7 tsc 0.

**HELD. Not raised.**

---
## Checker verdict (verbatim tail)
develop's own reds (attributed, not counted): []
NEW reds: []
reds fixed by the patch: []
tests added: 5
PASS A6 whole services/vc-issuer suite: no NEW red vs the untouched tip
PASS A7 tsc --noEmit for services/vc-issuer: rc 0 after the patch (baseline rc=0)
INFO tsc test-file types: could not tell services/vc-issuer's test runner (jest:[jest, ts-jest] vitest:[vitest.config.ts, scripts.test=vitest, vitest]) — kept the old default --types node,vitest/globals
INFO tsc on the test file alone (--types node,vitest/globals): rc=0 (0 lines; not gated — the runner does not type-check and the service tsconfig excludes __tests__)
SUMMARY files=2 +83/-0 test=src/__tests__/ks1269-status-unrevoke-refuses-a-non-integer-index.test.ts red_first=yes apply_mode=strict
RESULT: PASS (7/7)
