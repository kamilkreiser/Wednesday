KS-1378 Five new advisories block EVERY push: bump morgan, nodemailer, ip-address and undici (Kam ruled (a))
state In Progress

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
