--- comment 5827612535 by linear[bot] at 2026-09-25T06:00:16Z
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
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1229-pin-that-the-version-relabel-guard-keys-on-presence-not-bf6b75e3f55c">Review in Linear</a></p>

