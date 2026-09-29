--- comment 5882277093 by linear[bot] at 2026-09-29T02:07:08Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-729/upgrade-ip-address-off-ghsa-mwp4-54f8-5fhr-high-ssrf-express-rate">KS-729 Upgrade ip-address off GHSA-mwp4-54f8-5fhr (high, SSRF) — express-rate-limit 8.4.1→8.5.1+ in mcp-server, @meshsdk/@cardano-sdk 9.0.5 line in root + frontend/issuer</a></summary>
<p>

## BLUF

`ip-address` **is on GHSA-mwp4-54f8-5fhr (high, SSRF / trust-boundary bypass; patched in 10.3.1) in three lockfiles.** Two of the three are the *same* root cause and are a **patch-level bump of a different package**; the third is a `@meshsdk` major-version question. This ticket is the live owner of the audit-baseline exception for that advisory (`scripts/audit/audit-baseline.json`, `GHSA-mwp4-54f8-5fhr`), which now expires **2026-09-30**.

Filed at Peter's request on PR #738 (2026-08-31): the exception previously pointed at KS-559, which is **Done AND archived**, so on expiry the row would be orphaned again — the exact state KS-635 was filed about. KS-635 remains in `reason` as the deciding ref; this ticket is what `ticket` points at, and its due date is set to the row's expiry so the two cannot drift.

## The advisory

```
GHSA-mwp4-54f8-5fhr  —  high
ip-address: Address4 decodes leading-zero octets as decimal while resolvers
decode them as octal, allowing SSRF and trust-boundary bypass
vulnerable: <= 10.3.0        first patched: 10.3.1        published 2026-08-03
```

## Where it actually is — measured, not inferred

Every `package-lock.json` outside `node_modules` was parsed for an `ip-address` entry:

| lockfile | resolved | vulnerable? |
| -- | -- | -- |
| `services/mcp-server` | **10.1.0** | ✅ yes |
| root `Blockchain/Dev` | **9.0.5** + 10.4.0 (nested) | ✅ the 9.0.5 |
| `frontend/issuer` | **9.0.5** + 10.4.0 (nested) | ✅ the 9.0.5 |
| `packages/shared` | 10.4.0 | ❌ already patched |
| `services/anchoring` | 10.4.0 | ❌ already patched |

⚠ This corrects the review table on #738 in one place: root and `frontend/issuer` carry **both** 9.0.5 and 10.4.0 — the 10.4.0 copies are nested under `@cardano-sdk/dapp-connector` and `@cardano-sdk/key-management`, which already declare `^10.2.0`. Only the hoisted 9.0.5 is exposed.

## Leg 1 — `services/mcp-server`: a patch bump of `express-rate-limit`, not an `ip-address` override

```
services/mcp-server: express-rate-limit@8.4.1  declares  ip-address: "10.1.0"   <- EXACT pin
```

An `ip-address` override would violate that exact pin. But the pin moved upstream:

| express-rate-limit | declares |
| -- | -- |
| 8.0.2 – 8.5.0 | `ip-address: "10.1.0"` (exact — vulnerable) |
| **8.5.1 – 8.7.0** | `ip-address: "^10.2.0"` → resolves 10.4.0 ≥ 10.3.1 ✅ |

**So the fix is** `express-rate-limit` **8.4.1 → ≥ 8.5.1 (latest 8.7.0) — a patch/minor bump, no override, no major.** The path is already proven inside this repo: the root lock carries `@modelcontextprotocol/sdk/node_modules/express-rate-limit@8.5.2`, which declares `^10.2.0` and resolves **10.4.0** today.

*(Instrument note: a first probe read* `express-rate-limit@10.1.0` *as having zero dependencies. It has none because **it does not exist** — the registry 404s it, against a 200 on 8.7.0. The "10.1.0" was the pinned* ip-address *version, not an express-rate-limit version. Corrected before it reached this ticket.)*

## Leg 2 — root + `frontend/issuer`: a `@meshsdk` / `@cardano-sdk` major question

```
node_modules/ip-address = 9.0.5
  declared by @cardano-sdk/core : ip-address ^9.0.5
  reached via @meshsdk/core-cst, @meshsdk/provider, @meshsdk/transaction
```

`^9.0.5` **cannot** reach the 10.x line, so no override satisfies the declared range. Newer `@cardano-sdk/core` — the copies vendored under `@cardano-sdk/dapp-connector` and `@cardano-sdk/key-management` in this same tree — already declare `^10.2.0`. **The fix is bumping** `@meshsdk/*` **so it pulls a** `@cardano-sdk/core` **on the 10.x line.**

This is the same `@meshsdk` family that owns the three **permanent** `undici` acceptances in the baseline (`GHSA-8xcm-r25x-g524`, `GHSA-m8rv-5g2x-5cg5`, `GHSA-v3r7-h72x-cjcm`, all `frontend/issuer -> @meshsdk -> @utxorpc/sdk -> @connectrpc/connect-node`), and the family behind the multi-pinned `@lucid-evolution` packages on #720. Worth doing as one sweep rather than three.

## Exposure — stated honestly, not minimised

Not assessed in this ticket. The advisory is an SSRF / trust-boundary bypass in `Address4` parsing, and whether any first-party request path reaches it through `@cardano-sdk` has **not** been swept. The baseline row is a time-boxed exception precisely because that sweep was never done — do not read it as a bounded-exposure acceptance the way the `qs` row (KS-531) is.

## Scope

- ☐ **Leg 1:** `services/mcp-server` — `express-rate-limit` 8.4.1 → ≥ 8.5.1; regenerate the standalone lock **in** `node:24-alpine` (host regen drops optional binaries); confirm `ip-address` resolves ≥ 10.3.1.
- ☐ **Leg 2:** root + `frontend/issuer` — `@meshsdk/*` bump onto a `@cardano-sdk/core` 10.x; assess against the undici acceptances and #720's `@lucid-evolution` pins in the same pass.
- ☐ Re-run `node scripts/audit/audit-locks.mjs` and `node scripts/audit/audit-gate.mjs` — both must exit 0 **with the** `GHSA-mwp4-54f8-5fhr` **baseline row removed**, which is the real done-state.
- ☐ Remove the row from `scripts/audit/audit-baseline.json`. Its expiry (2026-09-30) is this ticket's due date; if the work slips, the date moves **here** and on the row together, with a reason — never silently.
- ☐ Second instance of the same pattern, out of scope but named: `GHSA-q8mj-m7cp-5q26` (`qs`) is owned by **KS-531, also Done and archived**, expiring 2026-11-11. Flagged on 2026-08-21 and again by Peter on #738. It needs a live owner before that date.

## Refs

* KS-635 — the deciding ref for the date move (`reason` field on the row)
* KS-559 — original owner, **Done AND archived**; lineage only
* PR #738 — the date alignment 2026-08-31 → 2026-09-30 that this ticket unblocks
* KS-531 — the `qs` twin of this pattern
* Advisory: [https://github.com/advisories/GHSA-mwp4-54f8-5fhr](<https://github.com/advisories/GHSA-mwp4-54f8-5fhr>)

*Filed 2026-09-01 (session 94). Every version figure above was read out of the lockfiles and the npm registry in-session, with a firing control on each instrument.*
</p>
</details>
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1378/five-new-advisories-block-every-push-bump-morgan-nodemailer-ip-address">KS-1378 Five new advisories block EVERY push: bump morgan, nodemailer, ip-address and undici (Kam ruled (a))</a></summary>
<p>

**BLUF — the push preflight FAILS legs 6 and 7 on develop's own dependencies, so NO push on this repo succeeds until this lands.** Five newly published advisories are absent from `scripts/audit/audit-baseline.json`. Verified ABSENT from the baseline at develop `8af6ab8216007462e596daed6b0adcd1e87e34ee` itself, so this is not caused by any open branch.

Kam ruled card `secuura-five-new-advisories-block-every-push-0929` = **(a)** on the live board 2026-09-29 11:43:09 AEST: *"Bump all four packages, with a quick reachability check in the same round."* **No baseline entry for any of the five.**

## The five, verbatim from preflight leg 6

| advisory | package | where |
| -- | -- | -- |
| `GHSA-6vj9-mwq6-2f5v` | **nodemailer** | process-global DNS cache reuses the TLS `servername` across transports -> **cross-tenant SMTP credential disclosure**. 2 locks: services/auth, services/originate |
| `GHSA-9f6g-j8ch-79g4` | **morgan** | log injection via an unescaped double quote in quoted log fields. **10 service locks** |
| `GHSA-rpw4-54j3-4h4q` | **ip-address** | `Address6.isLinkLocal()` reads `fe80::/64` not `fe80::/10` -> SSRF / trust-boundary bypass. 3 locks incl. packages/shared |
| `GHSA-2vr4-cq9g-pvrc` | **ip-address** | no classifier for the NAT64 local-use range `64:ff9b:1::/48` -> SSRF / trust-boundary bypass |
| `GHSA-3wwx-pv8p-q78v` | **undici** | DoS via an unhandled error in WebSocket permessage-deflate decompression. frontend/issuer |

Leg 6 reads `30 distinct advisories reported, 25 baselined`; leg 7 reads `26 match, 21 already baselined` across 43 standalone locks / 1591 pinned packages. Both name the same five.

## The routes are NOT uniform — measured, not assumed

* **morgan** — declared `^1.10.0` in 10 services, pinned 1.12.0, **1.12.1 published and inside the caret**: a lock refresh reaches it.
* **ip-address** — `packages/shared` declares `^10.2.0`, pinned 10.4.0, **10.7.2 inside the caret**: a lock refresh reaches it there. The `@cardano-sdk/dapp-connector` and `@cardano-sdk/key-management` nested 10.4.0 copies and a 9.0.5 are TRANSITIVE: `overrides` or a parent bump.
* 🔴 **nodemailer — a lock refresh CANNOT fix it.** The highest published 9.x **IS** `9.1.1`, exactly what is pinned; `^9.0.3` is at its ceiling and latest is `10.0.12`. It needs a **MAJOR** bump in `services/auth` and `services/originate`. This is the most expensive of the four *and* it is the credential-disclosure one.
* **undici** — TRANSITIVE only, under `jsdom` (a test dependency) plus a 5.29.0. `overrides` or a jsdom bump.

## Not to be confused with

`KS 729` is a **different** ip-address advisory (GHSA-mwp4-54f8-5fhr). A bump here may also satisfy it; that is a bonus, not this ticket's claim.

## Scope

Bump, plus a per-advisory **reachability read** recorded in the PR body (FOUND / TESTED / HOW). **The proof is preflight legs 6 and 7 passing on the PR.** No baseline entry, no `--no-verify`. Filed by the Platform K build seat on Wednesday's instruction after Kam's ruling.
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1378-bump-morgan-nodemailer-ip-address-and-undici-off-five-815a0a16d4c7">Review in Linear</a></p>

