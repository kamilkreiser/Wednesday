--- comment 5827253041 by linear[bot] at 2026-09-25T05:21:53Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1229/ks1213-cells-ten-tampers-stay-green-a-refused-issue-can-mint-a-holder">KS-1229 ks1213 cells: ten tampers stay green - a refused issue can mint a holder stub or an anchor, and non-string / padded types are unpinned (test-only)</a></summary>
<p>

## BLUF

**Test-only.** PR #1031 (KS-1213, merged as `732c13459`) makes the four derived-document writers refuse a caller type that differs from the stored type, and the runtime at head is correct. But the tier-1 gate found ten ways to break it that the 85 ks1213 cells do not catch. In each, the tamper stays green on the whole originate suite (64 / 741) while the consequence was measured.

* Two are load-bearing: a refused issue that still mints a holder user in auth, or still submits an anchoring job.
* **A local-model candidate:** the cells go in `services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts`. No product change.

## Recommendation

Add one cell per row below; each must red under its tamper. Priority order: the two external side effects on issue first (X-ISSUE-AFTER-HOLDER, X-ISSUE-AFTER-ANCHOR), then X-ISSUE-LOOSE, then the rest. R-a is a one-line spec wording fix in the sign-wallet operation's 400 description (plus regenerating the yaml).

## Detail

Each row gives the tamper (the gate's name), the consequence measured on the tampered tree, and the cell that pins it:

* **X-ISSUE-AFTER-HOLDER** (the issue guard moved before `const id = uuidv4()`): a refused issue → 400 with `POST /api/users/stub` **called once**, which mints or resolves an INVITED user in auth. Cell: refused issue → users/stub 0.
* **X-ISSUE-AFTER-ANCHOR** (the guard moved before `const certification`): a refused issue → 400 with `/api/anchors` **1** (an anchoring job). Cell: refused issue → anchors 0.
* **X-ISSUE-LOOSE** (`typeof x === 'string' &&` in place of `!== undefined`): a non-string `data.documentType` (7, an array, an object, true) → **201, served the non-string**, with saveCertification 1 and anchors 1. Cell: a non-string type on issue → 400.
* **X-SIGNCERT-AFTER-UPSTREAM** (the guard moved after the issuer-certs sign call): a refused `/sign-cert` → 400 with **the sign upstream called once**. Cell: refused sign-cert → sign upstream 0.
* **X-VERSION-TRIM** (`x.trim() !== source.type`): `'DOCUMENT '` / `' DOCUMENT'` → **201, served with the whitespace**. Cell: padded type on `/version` → 400.
* **X-SIGNWALLET-SERVED** (compare with `source.data?.documentType ?? source.type`): a legacy source + DEGREE → **201 served DEGREE**. Cell: sign-wallet compares with the STORED type.
* **Q-SIGNCERT-UNTYPED-SOURCE-SKIP** (skip the guard for an untyped source): untyped source + DEGREE → **201, served DEGREE**, sign upstream 1. In-memory only: Postgres reads `type` as `document_type || 'document'`. Cell: untyped in-memory source + differing type → 400.
* **Q-VERSION-TRUTHY** (`if (metadata.documentType && …)`): null / '' / false → 201, stored = served DOCUMENT (benign: no relabel). Cell: a presence-not-truthiness refusal, or a comment that the benign shape is accepted.
* **Q-SIGNWALLET-AFTER-VERIFY** (the guard moved after `verifyMessageSignature`): a refused sign-wallet runs the signature check first (CPU only; an invalid signature would answer INVALID_WALLET_SIGNATURE before BAD_REQUEST). Cell: refused sign-wallet → verify not called.
* **R-a** (Polish): the sign-wallet OpenAPI 400 description names only `VALIDATION_ERROR` / `INVALID_WALLET_SIGNATURE`, not `BAD_REQUEST`.
* **Not in this ticket:** the provenance ordering on `/version` and issue (filed separately, same session); KS-1203 (untyped connector create); the legacy-inheritance residual L03 (KS-1213 itself).
* **Source:** the tier-1 gate report on #1031 at `be8596a29` (GO WITH FINDINGS, verdict 2026-09-17 13:11Z), §4 tampers and §9. Wednesday ruled these SHIP WITH a ticket, not as cells in #1031.
* **Searched before filing** (Linear, literal, archived included): `ks1213-a-derived-writer`: 0 (the same search matched other terms, so the instrument can match). No ticket covers these cells.
* Refs KS-1213 (stays In Progress).
</p>
</details>
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1133/verify-hash-precedence-v1-hash-last-v2-hash-first-document-the-split">KS-1133 verify-hash precedence: v1 hash-LAST, v2 hash-FIRST — document the split on both routes' descriptions (Kam 2026-09-13)</a></summary>
<p>

## BLUF

**Ruled by Kam 2026-09-13 16:55 AEST on the decision panel:** `accept-split`**.** His option text, verbatim: *"Accept the split in writing: v1 hash-LAST (legacy bodies unchanged), v2 hash-FIRST; document it on both routes' descriptions"*. The two public verify routes read the same conflicting body to different hashes, by design after this ruling — so the work is documentation on both routes' OpenAPI descriptions, plus a cell on each route asserting its own order, not a code change to either chain.

## The finding this rules (the #965 tier-2 gate's F-1, Minor, MEASURED AT RUNTIME)

Report: `Testing Agent MAIN/projects/secuura/reports/2026-09-13-ks1103-965-d63b27ab3-tier2-r1/report.md`, FINDINGS F-1; rows P1/W1 in `evidence/shapes-table.md`.

* `{contentHash:A, hash:B}` → **v1** `POST /api/verification/verify` looks up **A** (`providedHash || contentHash || documentHash || hash`, originate `routes/verification.ts:742` at `d63b27ab3`); **v2** `POST /api/v2/verification/verify` looks up **B** (`hash || providedHash || contentHash || documentHash`, `verificationV2.ts:446`).
* The divergence pre-dates #965 (at its base v1 ignored `hash` entirely); #965's T2 tamper pins v1's order by test, so the routes disagree by design rather than by omission. No caller sends two different hashes (the gate's §3 class (c) was empty), so the blast radius today is nil; the inconsistency is a contract fact a future connector author can trip on.
* The gate did not judge which order is right; Kam has: keep both, write it down.

## Checklist (one test pass)

- ☐ v1 route description in the served spec (`services/originate/src/openapi/*.openapi.ts` → regenerated `secuura-api.yaml`; the spec is bind-mounted, not baked): state the alias order `providedHash → contentHash → documentHash → hash` and that `hash` is read LAST so legacy bodies keep their answer.
- ☐ v2 route description likewise: `hash → providedHash → contentHash → documentHash`, `hash` read FIRST.
- ☐ One cell per route asserting the winner for `{contentHash:A, hash:B}` (v1 → A, v2 → B) — the gate's P1/W1 rows as tests, so a future "one shared chooser" cannot silently flip either route.
- ☐ Note the split in the spec's `VerifyRequest` description if it names the aliases (it currently describes a pre-KS-252 order — the gate's O-6, pre-existing prose; fix in the same pass if the sentence is touched).

## Neighbours

* **KS-1118** (Low, related): the `documentHash`-over-`hash` precedence within v1 is unpinned (F-2) + the overclaiming why-comment (F-3) — the same alias chain, one position over; a builder taking both in one pass loses nothing.
* KS-1103 (archived, #965 merged 2026-09-13) — where `hash` was first read at all on v1.

## Dedupe, before filing (s205, 2026-09-13)

Literal census over 1,120 KS issues (692 archived) and 911 comments — `hash-FIRST` 0 · `hash-LAST` 0 · `documentHash` → KS-1103 (archived), KS-1114, KS-1118, KS-1119, KS-256, KS-474, KS-480, KS-499, KS-501, KS-514 (KS-1118 is the neighbour; none carries the v1/v2 split as a ruled item). No home; filed new.

## Provenance

* The #965 tier-2 gate (report path above), F-1. Wednesday's plan ANSWER to s200 (2026-09-13 14:50 AEST): F-1 is Kam's call, carded, not ticketed.
* Kam's ruling `accept-split`, 2026-09-13 16:55 AEST, decision panel; relayed in Wednesday's ADDENDUM to s205 (16:57 AEST) with the option text verbatim. Filed by s205 as the ticket that carries it.
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1133-document-the-v1v2-hash-alias-split-on-both-verify-routes-and-c373164a7ae4">Review in Linear</a></p>

