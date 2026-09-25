--- comment 5826361616 by linear[bot] at 2026-09-25T03:49:04Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1118/post-apiverificationverify-the-documenthash-over-hash-precedence-is">KS-1118 POST /api/verification/verify: the `documentHash`-over-`hash` precedence is unpinned, and the why-comment + test header overclaim "every body that worked before keeps its answer" (QA-965 F-2 + F-3)</a></summary>
<p>

## BLUF

Two test-side gaps left by PR #965 (KS-1103, merged 2026-09-13), from its tier-2 gate; neither is a product defect and neither held the merge. (1) The alias chain `providedHash || contentHash || documentHash || hash` is pinned by test only against `contentHash` and `providedHash`: moving `hash` to THIRD leaves all 575 originate cells green, so the "read LAST" claim is not fully pinned. (2) The why-comment at `routes/verification.ts:739-740` and the test header at `ks1103-verify-hash-field.test.ts:15-17` say "every body that worked before keeps its answer" — two body shapes that worked at base now answer from a different strategy (no caller in the repo sends either; the new behaviour is v2's and arguably better), so the sentence, not the code, is wrong.

## Recommendation

One test pass, one file each:

1. **F-2 — add one cell** in the precedence block of `ks1103-verify-hash-field.test.ts`: `{documentHash:A, hash:B}` with no rows → 200, exactly 1 lookup, the lookup saw A (documentHash) and never B. The gate's T5 tamper (`hash` moved to third) is the red-proof: today it reds nothing.
2. **F-3 — narrow the two sentences** to: "every body carrying a pre-existing alias keeps its lookup value; documentId-only, documentData-only and alias bodies are unchanged; a body pairing `hash` with `documentId` or `documentData` now takes the hash strategy, as v2 already does — no caller in the repo sends that pairing."

## Detail

* **Where:** `Blockchain/Dev/services/originate/src/routes/verification.ts` — the chain at `:742` at `d63b27ab3` (`providedHash || contentHash || documentHash || hash`), the why-comment `:739-740`; `src/__tests__/ks1103-verify-hash-field.test.ts` header `:15-17` and its P block (P1 `{contentHash:A, hash:B}`, P2 `{providedHash:A, hash:B}`).
* **F-2, measured by the gate (MEASURED):** row P3 `{documentHash:A, hash:B}` → head saw A, never B (correct today); tamper T5 (`hash` moved to third) → 575/575 green, and the gate's probe on the tampered code moves exactly that row. Evidence: `evidence/jest-tamper-T5.summary.txt`, `evidence/probe-head-T5.json` in the report directory.
* **F-3, measured (MEASURED):** `{documentId:X, hash:B}` — base: strategy 2 (by id, 2 lookups saw X); head: strategy 1 (by hash, 1 lookup saw B), rows DH1/DH2/DH3. `{documentData:{…}, hash:B}` — base: hashes the data; head: uses the sent `hash` (DD1). The repo-wide caller census (73 files) finds no caller sending either pairing; DH3 shows a matching `hash` now proves integrity where base answered `verified:false` with a false "no hash was provided" warning.
* **Source:** `Testing Agent MAIN/projects/secuura/reports/2026-09-13-ks1103-965-d63b27ab3-tier2-r1/report.md`, FINDINGS F-2 and F-3; §2b rows P3, DH1–DH3, DD1.
* **Not in this ticket:** F-1 (v1 reads `hash` LAST, v2 reads it FIRST — the same conflicting body looks up two different hashes on the two public routes) is a product-consistency ruling, on the CTO's panel, not ticketed by the merge round.
* **Related:** KS-1103 (PR #965), KS-1114 (the `title`-only contract), KS-735 (verify-result display).
* **Dedupe, before filing (s200, 2026-09-13):** literal census over 1,106 KS issues (685 archived; titles + descriptions) and 899 comments on non-archived issues — `documentHash` → KS-1103, KS-1114, KS-256, KS-480 and four archived; `originate/src/routes/verification.ts` → 11 issues, none about the alias precedence pin or the comment's claim. Controls: `LIKE` → KS-1020; a nonsense token → 0.
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1118-pin-documenthash-over-hash-and-narrow-the-product-comment-that-2828784a810d">Review in Linear</a></p>

