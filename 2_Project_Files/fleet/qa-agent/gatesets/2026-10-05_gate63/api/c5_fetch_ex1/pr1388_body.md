## What this changes

#1376 closed the forgeable paths in the RFC 3161 verifier and committed the trust anchors. It never
**delivered** one to a running service, so `readTrustAnchorsPem()` returned `undefined`, zero anchors
parsed, and `rfc3161-verify.ts:289` refused **every real DER token** with `no trust anchor
configured` — whatever the TSA did.

Measured read-only on both live boxes, 2026-10-05:

| | kintsugi | demo |
|---|---|---|
| `TSA_URL` | PRESENT but **EMPTY** | PRESENT but **EMPTY** |
| `TSA_TRUST_ANCHORS_PEM` | **ABSENT** | **ABSENT** |
| `/app/config` in the running image | **absent** | **absent** |
| `/health` → `tsa.provider` (from inside the container) | **D-Trust GmbH** | **D-Trust GmbH** |
| `ts_timestamps` | **0 rows** (lifetime inserts 0) | **1 row, and it is a mock** |

An empty `TSA_URL` is **not** "no provider" — it falls through to the code default. `/health`, read
from inside each container, reports `https://timestamp.d-trust.net/tsa`, `eidasQualified: true`.
Control on every env reading: `PORT` reads `4004`; a name that cannot exist reads ABSENT.

Two changes close the gap:

1. **`docker-compose.yml`** passes `TSA_TRUST_ANCHORS_PEM` to the timestamping service, defaulting to
   `/app/config/tsa-trust-anchors-dtrust.crt`. The default is what makes the anchor effective **with
   no `.env` edit on any box**; a box `.env` can still override it. Measured: neither box has a TSA
   override to fight it (kintsugi's compose override mentions `TSA` 0 times; control, it matches
   `services` twice).
2. **The timestamping Dockerfile's runtime stage** copies `config/` to `/app/config`, **before** the
   `chmod -R a+rX`. Order is load-bearing: the service runs as the unprivileged `nodejs` user, so a
   file copied after the chmod ships unreadable. Asserted from the written file, not from intent.

## Scope: ONE provider's root

Kam's card `secuura-ks1404-tsa-trust-and-library-1004` = **a** pins "*that provider's* published
root". Both boxes resolve to D-Trust, so `config/tsa-trust-anchors-dtrust.crt` holds **D-TRUST Root
CA 1 2017 alone** and the bundle's DigiCert root is needed by neither. The new file is **block 1 of
the already-committed bundle, extracted verbatim**:

- byte-identical to that block: **true** (2,354 bytes both sides)
- DER SHA-256 `4d24807b9cad5110f40ed79d934346d7c9b0290431dc9b11a40bbb86fcf2aef6`, matching
  `config/README.md`
- exactly **1** certificate in the file; control, the bundle holds 2
- control: the bundle's DigiCert root differs (`3e9099b5…`, 955 DER bytes)

**Nothing was fetched. No network call was made. No new root is introduced.** The two-root bundle
stays in the tree and cells 17/17b still assert it.

## Test evidence

**Touched:** `docker-compose.yml`, `services/timestamping/Dockerfile`, a new per-provider `.crt`, a
new unit file, three comment-only edits, both platform-k docs.

**Ran, locally:**

- `src/__tests__/ks1404-wiring.test.ts` — **3 failed / 3 passed at base `f01c1da5717f`; 6 passed at
  head.** Cells **A, B, C1** are the red arms. **C2, D and E are CONTROLS that pass at base AND
  head** and are labelled as such, not counted as red.
- Whole timestamping service suite at head: **7 files, 86 passed, 0 failed**, re-run on a real
  `npm ci` tree (1937 packages), not the borrowed one used earlier.
- `ks1404-verify-rfc3161.test.ts`: **0 changed lines**, byte-identical, still green.
- `tsc` for the service: the **same single** pre-existing error at base and head
  (`rfc3161-verify.ts` TS2345), its line moving 344→349. **Zero new.**

**Why cell C2 is here.** The pre-existing KS-1404 suite passes the anchor as **inline PEM text**
everywhere. The `readFileSync` branch of `readTrustAnchorsPem()` — the one the compose default makes
every box use — had **no coverage at all**. This change depends entirely on it.

**The comment-only claim, and a correction to how it is proved.** `tsc` **copies JSDoc into the
emitted JavaScript**, so a `cmp` of `dist/` is not the right instrument and does not come out equal
(31 dist lines changed). The proof is that **all 9 emitted `.js` files are identical once comments
are stripped — 0 differing** — with controls both ways (the stripper distinguishes `const a=1` from
`const a=2`, and treats two different comments as the same code). The only other `dist` change is
`.js.map` mappings shifting because the comment block's line count moved.

**NOT run:** the local image build proof (`docker build` at base and head, then
`test -r /app/config/tsa-trust-anchors-dtrust.crt` as `nodejs` → base 1 / head 0, control
`/app/package.json` → 0 both sides). Left for the gate, deliberately, on the coordinator's ruling —
it is the one remaining check and it is named here rather than quietly omitted.

**Migrations + config:** no migration. No lockfile and no manifest touched — `pkijs` and `asn1js`
arrived with #1376 and are already dependencies, so this adds none. No `.env` edit on any box; the
anchor arrives by the compose default.

## Docs

Flow-diagram block **11** gains **11.4 in place** — no new top-level number and nothing renumbered,
because KS-1404 already owns 11. Two now-false sentences in 11.2 and 11.3 are corrected and say what
they previously claimed. The cheat sheet's KS-1404 table gains the matching row and its two stale
sentences are corrected the same way. Both files' closing tags are untouched.

## What this does NOT prove

- **That D-Trust's TSA signs under this root today.** `config/README.md` already records the
  root-to-TSA binding as UNVERIFIED, and there is no real DER token on either box to check it
  against: `ts_timestamps` is empty on kintsugi and holds exactly one **mock** row on demo
  (`D-Trust GmbH (mock)`, `eidas_qualified` false, proof starting `ey`, 2026-07-30).
- **Revocation.** No CRL and no OCSP check is wired, and pinning a root adds neither.
- **Policy OIDs.** Nothing asserts a token was issued under a qualified policy.

## Deploying this changes kintsugi's answer for a real token from `false` to `true`

…but **only if the box reaches D-Trust**, which is an open measurement. Kintsugi has minted no
timestamp at all — 0 rows, 0 lifetime inserts, 0 `[TSA]` log lines, 0 mock fallbacks — so it is
neither "pinnable" nor "mock-only" on the existing vocabulary; the coordinator adopted
**PINNABLE-BY-CONFIG / UNEXERCISED** for it. If the first real mint after deployment falls back to a
mock, that is the evidence that the authority question needs reopening, and it stops there.

**Demo's status:** MOCK-ONLY on the one data point that exists, which is 67 days old. Stated as a
reading, not as a property of the box.

## Order

Kam's card `secuura-ks1404-anchors-before-049-merge-order-1005` = **a**: *"Hold #1383's merge until
the anchor wiring has merged."* So this PR is on #1383's critical path, and a develop SHA carrying
this fix **without** migration 049 will exist for kintsugi and, after a clean kintsugi sweep, for
demo.

Refs KS-1404
https://linear.app/secuura/issue/KS-1404
