SUBJECT: [Secuura/Blockchain -> Wednesday] QUESTION: audit row GHSA-mwp4-54f8-5fhr ip-address (Seat B)
TS: 2026-09-17T07:27:06.000Z
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}

Seat B

CONTEXT
Row 15 of 15: GHSA-mwp4-54f8-5fhr, ip-address (KS-729, In Progress on its @meshsdk leg). expires 2026-09-30, which lapses Wed 30 Sep 10:00 AEST.
- [G] HIGH: Address4 decodes leading-zero octets as decimal where resolvers decode octal (SSRF / trust-boundary bypass). <=10.3.0; fixed 10.3.1.
- Carried: 9.0.5 in frontend/issuer (the client bundle) and in the root lock.
- The declarer is @cardano-sdk/core 0.46.12 (ip-address ^9.0.5), pinned EXACT by @meshsdk/core-cst 1.9.1 and @meshsdk/transaction 1.9.1.
- [V] @meshsdk/core 1.9.1 and @meshsdk/core-cst 1.9.1 are the LATEST stable releases (prereleases not checked). No @meshsdk release fixes this, major or not; the row's "that leg is a @meshsdk major bump" has nothing to bump to today.
- The root's hoisted @cardano-sdk/core 0.46.14 could move to 0.46.15 in range (ip-address ^10.2.0), but the nested exact 0.46.12 copies keep 9.0.5, so the row would stay.
- Lead: @cardano-sdk/core itself moved ip-address ^9.0.5 -> ^10.2.0 in a PATCH release (0.46.14 -> 0.46.15). That suggests its own usage survives the 9 -> 10 change. UNVERIFIED: reading that source diff needs a tarball fetch, which is not in the reads you authorised.
- Reach: the issuer runs in the browser. Whether the SSRF shape matters there is UNMEASURED.

QUESTION
Which does Kam choose for row 15?
(a) OVERRIDE (recommended, HIGH). Add `ip-address: ^10.3.1` to the overrides of frontend/issuer/package.json AND Blockchain/Dev/package.json (issuer is a workspace member; npm reads overrides only from the root manifest). That contradicts @cardano-sdk/core 0.46.12's ^9.0.5. Then the issuer build + unit suites. A wallet-flow check needs a stack, which is outside Seat B's holds, so it would be NOT run.
(b) Wait for a @meshsdk release, with a dated decision. Not mine.
(c) Something else Kam names.

MEANWHILE
Continuing with PR-1 (hono) and PR-2 (colord).

NEEDED-BY
Fri 25 Sep to you. The row lapses Wed 30 Sep 10:00 AEST; (a) needs one gate before then.

Seat B
