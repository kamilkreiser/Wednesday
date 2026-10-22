# B489 drafter report (Sonnet, read-only), 2026-10-23 about 00:20-00:50 AEDT

## BLUF
- **Brief:** `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-23_B489_SEAT-J1_hpsmpoc-321-jwt-sign-per-case.md`. Seat `Datasec/HPSM-POC-J1` (free: live panes were `Datasec/HPSM-POC-R2`, `-G47`, `-A2`, `fleet-monitor`). Sonnet C2, tier-2 delta gate later. Branch `b489/hpsmpoc-321-jwt-sign-per-case` from main `48521806ea98d30b3b7b0b57b3df51904523995f`.
- **Port block 8370-8379.** I read the live B488 brief (it holds 8360-8369 and says 8370-8399 appears in no brief), grep'd all `tuesday/briefs/*.md` with `-w '837[0-9]'` (only the B488 brief, which names the range as unclaimed; control `836[0-9]` hits B488 brief and report), and `lsof -nP -iTCP:8370-8379 -sTCP:LISTEN` was empty (rc 1). B481 8320-8329, B482 8330-8339, B487 8340-8349, B480 8310-8319 are taken. The Api test host is in-process, so the block is a reserve.
- **Fix property P:** no token used by a row is minted before that row's case body runs, OR every token's lifetime covers any realistic run. Shape A (Rows become recipes, `Func<string?>`, mint inside the case) is recommended with its reason; Shape B (long explicit `expires`) is allowed with a stated reason and a stated horizon; the `Sign` default of 30 min is not to change.
- **Mandatory proof:** red on the old shape under a simulated horizon, green on the new, the 11 at-risk rows by name, plus a horizon probe (-4 min accepted, -6 min refused), mutants M489-A (class-init mint reintroduced, must go red under the instrument) and M489-B (swapped expectation, must go red), a property check by program with a positive control on the old file, and a read-only census of other class-init mints.

## Edit sites read (all `git show 48521806:`; local clone's `main` is STALE at `8869b1a9`, dated 2026-09-23, which has neither file, but object `48521806` is present locally and was read directly)
`api/tests/HpsmPoc.Api.Tests/Assessment/JwtBearerRolePathTests.cs` (124 lines):
- `:20` `public class JwtBearerRolePathTests(JwtBearerHostFactory factory) : IClassFixture<JwtBearerHostFactory>`
- `:42` `private static readonly string SignedPartner = JwtBearerHostFactory.Sign(Who("signed-partner", new[] { "Partner" }));`
- `:45` `private static readonly Dictionary<string, (string? Token, (string Name, string Value)[] Headers, string Expect, string[]? Roles)> Rows = new()`; rows `:48-:81` (signing rows B68-01..13 and ADDED-16..20; ADDED-14/-15 carry no token; B68-04 `:52` and -05 `:54` derive from `SignedPartner`; ADDED-18 `:75` signs with `expires: DateTime.UtcNow.AddHours(-1)`).
- `:84` `public static TheoryData<string> Names() => [.. Rows.Keys];` (keys only, so recipes do not disturb discovery)
- `:97` `var (token, headers, expect, roles) = Rows[row];` and `:99` `if (token is not null) client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);`
- `:86-:91` key-count fact; `:112-:122` assertions (must not change).

`api/tests/HpsmPoc.Api.Tests/Support/JwtBearerHostFactory.cs` (75 lines):
- `:54` `var until = expires ?? DateTime.UtcNow.AddMinutes(30);`
- `:60-:62` `IssuedAt = until.AddMinutes(-31)`, `NotBefore = until.AddMinutes(-31)`, `Expires = until`.
- `:35-:48` `Configure`: no `ClockSkew` set. `git grep -n ClockSkew 48521806 -- api` = 0 hits (control: `JwtBearerHostFactory` = 29 lines in 4 files), so the library default skew applies (RELAYED 5 min by gate B476, bracket -4.9 / -5.1).
- Other `Sign` callers: `Auth/UatOpenAssertionEdgeTests.cs:127`, `Auth/UatOpenTests.cs:414`, `:536`, `:563`, each read: inside a `[Fact]` body, so not this defect (brief says report, do not edit).

## Verified facts vs the ticket
- The file exists on main (read through `git show`); the gate's line numbers `:42`, `:45-:82` and factory `:54` match exactly.
- Origin main = `48521806` (ls-remote 00:2x). Open branches seen: b46 (stale card), b460, b461, b462, b465, b466, b467; no `b489*`. `.tools/b489` and `.tools/wt-b489-*` absent. `records/b489` absent in the project-root repo (control `records/b467` = `7d723d13...`).
- The "no open branch touches JwtBearer" fact is the ticket-time measurement by Tuesday; I did not re-run the GitHub compare API (not needed for the draft; the brief makes the builder re-run it with controls).

## UNMEASURED (and why)
- Test count of the class (21 expected) and whether any run is green: no build/test allowed.
- The 5-minute skew value at this host (only RELAYED); the brief makes it step 2.
- Whether multi-line initialisers elsewhere mint at class init: only a single-line grep was run (hit: `:42`); the builder reads the rest (census).
- The faithful instrument (constructor delay + zero skew + 10 s lifetime): proposed, not tried.
- Jira ticket state: not queried (no need to draft; the builder records it).
- The Api-queue wait and launch load1.

## Departures from the B481 / B472 shapes
- Fresh branch, new-ref plain push (B472 shape) rather than fast-forwarding an existing branch (B481 shape); both ends at READY FOR QA.
- No records branch handling beyond "records/b489 does not exist and is not yours" (B481 had a records pointer to read; B472 said no records branch). Stated explicitly with a control.
- Added a stale-local-clone warning (local main is two months behind); B472 had a similar warning.
- Property-first fix section with two shapes and a property check by program, as asked; "false green" note for the 401 rows (they stay green after the horizon for the wrong reason).
- STATUS final-line format adapted: shape A/B and the k at-risk rows replace B481's per-item list.
- Every other standing section carried over: Step 0 copy, REFUSE list, PRIOR-WORK CHECK and PRIOR WORK, CodeQL line, no-human-message and client-comms line, never-delete, shell rules, locks by path (shared `.tools/.git-lock` for ref writes; seat-local `.tools/b489/heavy.lock`), Api-suite rule, load rule, ports, partition from both sides, intersection program, refs before/after, Stamp, launch line, report sections.

## `____` slots left for Tuesday (8 lines; REFUSE count control reads 8)
1. Stamp time
2. Stamped by
3. Launch authority
4. Hard stop and target READY
5. Main at launch (expected `48521806`)
6. Jira HPSMPOC-321 state at launch
7. Model receipt line and load1 at launch
8. Last line `READ-WHOLE-BY-TUESDAY: ____`
