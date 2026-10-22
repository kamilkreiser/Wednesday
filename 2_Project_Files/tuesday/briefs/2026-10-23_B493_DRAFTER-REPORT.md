# B493 DRAFTER-REPORT (2026-10-23, drafted about 02:00-02:40 AEDT)

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-23_B493_SEAT-J2_hpsmpoc-test-teeth-jwt-uatopen.md` (129 lines; stamp-slot count 8 = seven slots + last line, measured).

## Chosen
- Seat `Datasec/HPSM-POC-J2` (live panes at drafting: tuesday, J1, K1, G49, fleet-monitor; J2 free; J3 if taken at stamp). Sonnet, model row C2. Gate after: tier-2 delta.
- Ports **8410-8419** (lsof 8400-8419 empty rc 1; B492 holds 8400-8409; the only brief hits for 841x are finished 2026-10-21 briefs B390/B395, where 8412 is a finished seat's port).
- Branch `b493/hpsmpoc-test-teeth-jwt-uatopen`, cut from main after #188 merges.

## Property
P1 (JWT matrix cannot pass for the wrong reason or run short): ADDED-18 reason pinned (MA6a red), ADDED-16/-17 reasons pinned (MR16/MR17), `Names()` == `Rows.Keys` (MA8, MA8b, MA8c), optional structural no-static-JWT-string test (MA1, "cheap" defined as about 30 lines, else deferred). P2 (UatOpen refusals keep teeth): the two lifetime rows minted at run time (L1/L0 red under a delay, old shape survives), iat sign/size pinned from the minted token (T2 red), future-side boundary pair 30 accepted / 31 refused (F-a..F-d red). Closing mutant battery table with controls c0/c1/c2.

## Edit sites read
At PR #188 head `fd54671a` (blob `ce5378eb`, 126 lines; main `42a1d92f` still has the old 124-line shape, blob `0e936f97`, 0 lines of `Func<string?>`), `JwtBearerRolePathTests.cs`:
- :43 `private static string SignedPartner() => JwtBearerHostFactory.Sign(Who("signed-partner", new[] { "Partner" }));`
- :46 `Rows` tuple `(Func<string?> Token, (string Name, string Value)[] Headers, string Expect, string[]? Roles)`
- :71-72 ADDED-16, :73-74 ADDED-17, :75-76 ADDED-18 (`expires: DateTime.UtcNow.AddHours(-1)`)
- :85 `public static TheoryData<string> Names() => [.. Rows.Keys];`
- :87-92 fact; :90 `Assert.Equal(13, Rows.Keys.Count(k => k.StartsWith("B68-", ...)))`, :91 `Assert.Equal(20, Rows.Count);`
- :98-101 `var (mint, ...) = Rows[row]; ... var token = mint();`; :114 `Assert.True(expect == got, ...)`; :115 `if (expect == "401") Assert.Contains(reply.Headers.WwwAuthenticate, h => h.Scheme == "Bearer");`

At main `42a1d92f`, `Auth/UatOpenTests.cs` (blob `2887e3ea`, 628 lines):
- :358-363 `RefusedRows : TheoryData<string, string?, int?>`; :365 `Refused()`
- :377 `{ "expired", -3 * 60 }`, :378 `{ "issued beyond the skew in the future", 10 * 60 }`
- :379 `{ "lifetime over 120 s", UatOpenFactory.Mint("consultant", lifetime: 121) },` :380 `{ "zero lifetime", UatOpenFactory.Mint("consultant", lifetime: 0) },`
- :394-401 theory; :398 `... issuedAt: DateTimeOffset.UtcNow.AddSeconds(offset))`; :400 `Assert.Equal(HttpStatusCode.Unauthorized, (await MeWith(sent)).Status);`
- `UatOpenAuthentication.cs:157` (blob `e51abdb1`): `if (exp <= iat || exp - iat > MaxLifetimeSeconds || iat > t + SkewSeconds || exp < t - SkewSeconds) return null;`, `:56` MaxLifetimeSeconds 60, `:59` SkewSeconds 30, `:136` `public static string? Verify(string?, byte[], DateTimeOffset)` (public, usable for a unit pin).
- `UatOpenAssertionEdgeTests.cs` read whole (141 lines): holds the -31 expiry pair, no future-side pair; not edited.

## Departures from the commission
1. **B476-1/-2 fix-shape** names `UatOpenAssertionEdgeTests.cs`, which the partition excludes: the future-side pair goes in `UatOpenTests.cs` (via public `Verify` with a fixed instant); B476-1 uses the gate's second option (iat sign/size pin in the theory body), which fits the partition.
2. **B491-1 extended** to ADDED-16/-17 (reason pins; the gate said "ideally each 401 row"); B68-04/-05/-06/ADDED-19 deliberately excluded (signature is checked before lifetime, so nothing can shadow them: B491 A3/B491-4).
3. #188 may be squash-merged, so the REFUSE uses a content check (`Func<string?>` count 1 with controls, plus `pulls/188` merged true), not `merge-base --is-ancestor`.
4. B491's gate corrected B489's zero-byte control (`4695d7f2..48521806 -- api/src` is 0 bytes); the brief uses `48521806..4e77cf1d` instead.
5. Adding a lifetime column to the theory changes display names (as B472 did, B476-4); key stays method + `why`, case count stays 16.

## UNMEASURED
Nothing run: no test, build, mutant, fetch, worktree. Specifically unmeasured: every mutant's survival at base (RELAYED from gates; MR16/MR17 are my additions; the substrings `audience`/`issuer`/`expired` are read from the gates' quoted challenge texts, not measured); that F-a..F-d are killed by the pair (reasoned); L1/L0 horizons (151 s / 30 s, the gate's source reading); the reflection test fitting in about 30 lines; whether #188 merges unchanged; Jira state (not queried); any open branch's overlap with `UatOpenTests.cs` beyond b490 (0) and PR #188.

## `____` slots (8 lines)
Stamp time; stamped by; launch authority; hard stop and target READY; main at launch (must contain #188's merge); Jira HPSMPOC-321 state; model receipt + load1; last line `READ-WHOLE-BY-TUESDAY: ____`.
