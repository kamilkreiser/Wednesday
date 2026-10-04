Refs KS-1403

## What this does

An **in-range lock refresh** of `http-cache-semantics` 4.2.0 → 4.3.0 in the workspace-root lock and
the two standalone service locks that pinned it, plus **two triaged baseline rows** for the two
advisories that have no published fix in existence.

It exists to **unfreeze the push path**: preflight legs 6 and 7 currently fail on every push from
every branch, so nothing can reach `develop` until this lands.

**Ruled by Kam Kreiser, live board 2026-10-04 21:05:25 AEDT, card
`secuura-freeze5-high-no-fix-1004` = b: _"Fix what can be fixed, remove node-forge, accept only
braces"_.** The option text continues: _"node-forge gets removed from timestamping in the same rework
the separate unsigned-token card needs; until that lands it carries a baseline row with the same
expiry."_ So the node-forge row is inside the ruling, and the removal itself belongs to KS 1404's
seat, not to this PR.

## Why the repo froze without anyone touching it

**The mechanism is a RANGE WIDENING, not a new publication**, which is what makes two of the three
unfixable. The three advisories were published 03 and 18 Sep and then **updated** 2026-10-01T21:09
and 2026-10-02T22:36 — *after* the last green push on 2026-10-01 16:0xZ, whose preflight ran these
same two legs and reported nothing failed. **The packages never moved. The advisories' affected
ranges moved onto versions we already pin.** That is why a repo nobody touched for 2 d 19 h froze
itself.

| advisory | package | our pin | registry latest | fixable? |
|---|---|---|---|---|
| `GHSA-ch52-4w7c-c8xp` | http-cache-semantics | 4.2.0 | **4.3.0** | **yes — this PR** |
| `GHSA-vfj7-8cjw-p6xm` | braces | 3.0.3 | **3.0.3** | no — baseline row |
| `GHSA-86w9-cpqp-85rv` | node-forge | 1.4.0 | **1.4.0** | no — baseline row |

The "registry latest" column is read from `registry.npmjs.org` directly in this round, not from
`npm view`: braces' latest **is** 3.0.3 and node-forge's latest **is** 1.4.0, both equal to our pin,
each advisory range being `<= our pin` with `first_patched_version: none`. **No refresh, caret or
major bump clears either.** Only `http-cache-semantics` has somewhere to go.

## The three lock changes

The only dependant of `http-cache-semantics` anywhere is `node_modules/cacheable-request` at
`^4.0.0`, which **already admits 4.3.0**, so there are **no manifest changes** — this is a pure
in-range lock refresh.

Measured per lock by an entry-and-field differ against the **base blob read from the SHA**, never
from a working file:

| lock | changed | added | removed | field classes | collateral |
|---|---|---|---|---|---|
| `Blockchain/Dev/package-lock.json` | 1 | 0 | 0 | version, resolved, integrity | **0** |
| `services/anchoring/package-lock.json` | 1 | 0 | 0 | version, resolved, integrity | **0** |
| `services/nft-certificate/package-lock.json` | 1 | 0 | 0 | version, resolved, integrity | **0** |

`dev` / `optional` / `devOptional` / `peer` changes on any other entry: **0 on all three.**

**`node_modules/@types/http-cache-semantics` is byte-unchanged from base, asserted in the same run.**
It is a *different package* that also happens to sit at 4.2.0, so a version-string edit would have
hit both.

### Two things that would have shipped quietly, and did not

**1. `npm update http-cache-semantics --package-lock-only` was tried first and REJECTED.** In a
scratch copy of the base manifests plus the base root lock, it produced the intended bump **plus 13
collateral changes**: `dev: <absent> → true` on eleven `lightningcss-*` platform binaries and on
`magicast`, and `devOptional: true → <absent>` on `magicast`. This PR instead sets exactly the three
fields on exactly the one entry. That surgical result is **field-for-field identical to npm's own
output on the allowed entry** — the only entries where the two differ are npm's 13 collateral ones.

**2. The two service locks had silently lost 20 `libc` arrays** (10 each) when they were refreshed:
`"libc"` count 10 → 0 on every `@rolldown/binding-linux-*` and `lightningcss-linux-*` entry, all of
them `dev: true, optional: true`. The diff was true at *package* level and wrong at *field* level.
**All 20 are restored here**, each byte-equal to base, and both locks are back to their exact base
byte size (212,896 and 132,553). The committed diff on each service lock is now **3 lines out, 3
lines in** — the version, the resolved URL and the integrity, and nothing else.

### The integrity values are verified at source, because the clean-room leg cannot do it

`npm ci --dry-run --ignore-scripts` returns **rc 0 on a lockfile carrying a deliberately bogus
integrity hash** — measured in this round with a planted `sha512-AAAA…`. So leg 2 passing is *not*
evidence that a lock's hashes are right, and it is not offered as such here.

Instead the 4.3.0 tarball was downloaded (14,074 B) and its sha512 computed directly:
`sha512-M5t5LlJpS1UHMjvwRQVdFHvPISGeLAxNcrWuJkeGh0Kxs…`, which matches all three locks. Negative
control: the 4.2.0 tarball hashes to `sha512-dTxcvPXqPvXBQpq5dUr6mEMJX4oIEFv6bwom3FDwKRDs…`, which
is exactly what the two service locks carried **before**, and is not equal to the 4.3.0 value.

## The two baseline rows

Added to `scripts/audit/audit-baseline.json` under `accepted`, keyed by GHSA id, matching the
existing row shape (`package`, `reason`, `ticket`, `decidedAt`, `expires`). 24 → 26 rows. **Every
pre-existing row is asserted byte-equal afterwards** and `$comment` is unchanged; the rows were
appended textually because the file does not survive a JSON round-trip (16,994 B vs 17,051 at
indent 2) and a rewrite would have reformatted all 24.

| GHSA | package | ticket | expires |
|---|---|---|---|
| `GHSA-vfj7-8cjw-p6xm` | braces | KS 1403 | **2026-10-31** |
| `GHSA-86w9-cpqp-85rv` | node-forge | KS 1404 | **2026-10-31** |

**`GHSA-ch52-4w7c-c8xp` gets no row** — the refresh above fixes it.

The expiry is 31 Oct on both, per the ruling's "same expiry" and because 15 Oct would re-freeze the
push path before the KS 1404 rework can remove node-forge. Both rows sit in the existing 31-Oct
cohort. **The 2026-10-09 fuse is untouched: it is still 2 rows, both KS 528's, and nothing here
re-dates anything.**

### The reasons were re-measured, and the figures I was handed were wrong both times

- **braces** — I was told "PROD only in `services/api-gateway`, DEV in 10 locks". Measured across
  all 40 tracked lockfiles at the base SHA: braces 3.0.3 is in **11** of them, **PROD in three**
  (`services/api-gateway`, the workspace-root lock, and `mobile/secuura-app`) and **DEV in eight**
  (`frontend/admin`, `frontend/issuer`, `frontend/verifier`, `services/governance`,
  `services/originate`, `services/referral`, `services/staking`, `services/vc-issuer`).
  **Zero direct callers** in our own source — `require('braces')` and `from 'braces'` return 0 hits,
  with a must-hit control on the same grep shape finding `express` imported in 330 files, so the zero
  is a measurement and not a dead grep. It reaches us only transitively.
- **node-forge** — I was told "PROD in timestamping". Measured: **PROD in three** lockfiles (root
  1.4.0, `services/timestamping` 1.4.0, `mobile/secuura-app` 1.3.3), and it is a **direct dependency
  of two manifests** (root `^1.4.0`, timestamping `^1.3.3`).
- **One caveat on those counts, stated rather than buried:** leg 7 reports
  `Blockchain/Dev/mobile/secuura-app` as **declared out of scope** (KS 769, expires 2026-10-19), so
  "PROD in three locks" includes one lockfile the gate does not scan.
- **The "verify path is never called" half I confirmed by reading the code, not the claim.** The only
  two importers under `services/timestamping` are `src/tsa/qualified-tsa.ts` and
  `src/tsa/rfc3161-client.ts`, and every `forge.*` call site in them is ASN.1 construction or
  parsing, a buffer utility, or the single `forge.pkcs7.messageFromAsn1` used for optional
  certificate metadata inside a `try/catch`. `forge.pki.*verify`, `.verify(` and `verifySignature`
  return **zero** hits across `services/timestamping/src`, with a must-hit control finding `.verify(`
  in `services/auth` (`jwt.ts`, `issuerCert.ts`).
  ⚠ **That absence is itself the KS 1404 defect**: `verifyRealToken` only walks the ASN.1 for an
  OCTET STRING equal to the expected message imprint and reads `genTime`, so an **unsigned** token
  carrying a matching imprint reads as valid. Fixing that is KS 1404's seat, not this PR.

## The leg proof

Legs 2, 6 and 7 on this tree, from `Blockchain/Dev`:

- **leg 2** `scripts/preflight/lockfile-cleanroom.sh` — **rc 0**, all 35 standalone locks pass
  clean-room `npm ci`.
- **leg 6** `scripts/audit/audit-gate.mjs` — **rc 0**, _"OK — no advisories outside the triaged
  baseline"_. Names 0 of the three.
- **leg 7** `scripts/audit/audit-locks.mjs` — **rc 0**, 43 standalone lockfiles, 1,611 distinct
  packages, 8 advisories matched / 8 already baselined. Names 0 of the three.

**The base control, which is what makes those greens mean something.** In a scratch worktree created
at the base SHA and removed again:

- legs 6 and 7 at base: **rc 1 each** — not rc 2, so these are genuine failures and not skips — and
  the base tree **names all three advisories** (leg 6 twice each, leg 7 once each).
- the *same* scratch tree with this PR's four files copied in: exactly 4 files differ, **leg 6 rc 0,
  leg 7 rc 0**, and all three advisories named **zero** times. So the fix travels with the four
  files, not with my working tree.
- **both rows bite**: removing `GHSA-vfj7-8cjw-p6xm` alone → legs 6 and 7 rc 1; removing
  `GHSA-86w9-cpqp-85rv` alone → legs 6 and 7 rc 1; both restored → rc 0 again. Neither row is inert.

`npm ci` at `Blockchain/Dev` from the refreshed root lock installs **1,934 packages, exit 0**, and
leaves the lock blob unchanged — so the lock is installable as committed.

The 15-row CLEANUP advisory that leg 6 prints is informational, rc 0, and deliberately **not** in
this PR.

## Documentation — section 4 exemption

**No test file changes in this PR (measured: 0 test paths in the diff, against a must-hit control
where the same grep shape matches 1,806 files in the base tree), so the two platform-k HTML docs are
not updated.** The diff is exactly 4 paths: three lockfiles and the audit baseline. 0 `package.json`
manifests.

## NOT COVERED

- **The clean-room ran on its node-24 host path, not in Docker.** Docker is down on this host
  (`docker info` rc 1, socket absent), so the dockerised clean-room was not exercised. Host toolchain
  was node v24.7.0 / npm 11.5.1.
- **Skill section 5f: no live sweep.** Nothing here is a runtime-behaviour change, and no ticket is
  moved to Done on this PR's account.
- **No deploy.** No `az`, no VM, no migration, no Schemathesis, no Akto.
- **KS 1404's removal of node-forge from timestamping is a later seat's work**, red-first. This PR
  only accepts the advisory until then.
- **The 15-row leg-6 CLEANUP is not here.**
- `npm ci --dry-run` cannot validate an integrity value, as shown above; the integrity evidence here
  is the tarball hash, not the clean-room leg.

## Test Evidence

**Touched:** `Blockchain/Dev/package-lock.json`, `Blockchain/Dev/scripts/audit/audit-baseline.json`,
`Blockchain/Dev/services/anchoring/package-lock.json`,
`Blockchain/Dev/services/nft-certificate/package-lock.json`. 4 files, 24 insertions, 8 deletions.

**Ran:**
- preflight leg 2 (`lockfile-cleanroom.sh`) — rc 0, 35/35 locks
- preflight leg 6 (`audit-gate.mjs`) — rc 0 on this tree, **rc 1 at base naming all three**
- preflight leg 7 (`audit-locks.mjs`) — rc 0 on this tree, **rc 1 at base naming all three**
- baseline-row bite test, both rows, each reddening a leg when removed
- `npm ci` at `Blockchain/Dev` from the refreshed root lock — 1,934 packages, exit 0
- `npm ci --dry-run --ignore-scripts` at the workspace root on the refreshed lock — rc 0
- `deps-present.sh --self-test` — detector fires on empty and partial trees, silent on a complete one
- entry-and-field lock differ with its own self-test (plants a `dev` flip and a `libc` array, asserts
  both are reported, and asserts an identical pair reports nothing)
- integrity verified against the 4.3.0 registry tarball, with the 4.2.0 tarball as a negative control
- `node -e` parse of the baseline: 26 rows, both tickets and expiries read back, `GHSA-ch52` absent
- the full in-hook push preflight — ratio and skipped legs quoted in the READY

**NOT run:**
- the dockerised clean-room (Docker down on this host — see NOT COVERED)
- any service unit suite, Playwright, Schemathesis, Akto, k6 — this PR changes no source and no test
- any live sweep (skill section 5f)
- the 15-row baseline CLEANUP leg-6 advisory suggests — out of scope by ruling

**Migrations + config:** none. No migration, no manifest, no environment variable, no compose file.
The only config-shaped file is the audit baseline, and the two rows added to it are temporary
exceptions with a 2026-10-31 expiry and a named ticket each.
