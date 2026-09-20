# KS-1223 WALLET-1 PIN THAT x-wallet-address IS OUTSIDE THE EDGE STRIP (a client-sent value survives stripTrustHeaders while the trust family is removed) — Wednesday's task for Ornith, TEST_ONLY, **ONE existing test file, one hunk, one cell added, no product file** (written 23:24 on 2026-09-20, widened sweep round 24)

File: `Blockchain/Dev/services/api-gateway/src/__tests__/ks1041-vouch-header-strip.test.ts`
Tip: `dc061f2bb6dff9180a0724b1d1d5c50b9a0173fa`
Runner: `vitest`

Written from develop `dc061f2bb6dff9180a0724b1d1d5c50b9a0173fa` (`git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" ls-remote origin refs/heads/develop` at 23:19 on 2026-09-20, read verbs only; the #1101 merge, 2026-09-20 17:53:42 +1000). The test file at that tip is **113 lines**, read whole; its full content is in `files[...]` of your input. The product the cell pins is `Blockchain/Dev/services/api-gateway/src/utils/trustHeaders.ts` (**56 lines**, read whole): `TRUST_HEADER_PATTERN` at `:39-40`, `isStrippedTrustHeader` at `:43-47`, `stripTrustHeaders` at `:50-56`. This service runs **VITEST**.

## THE MODE — read this twice

**TEST_ONLY.** Your diff touches EXACTLY ONE file: the test file above, MODIFIED IN PLACE (`--- a/<path>` / `+++ b/<path>`, the path exactly as written above). You never touch `trustHeaders.ts` or any other product file: the behaviour is already what it is at the tip, and this cell PINS it.

## What the cell pins (one paragraph)

KS-1223 reports that a client-sent `x-wallet-address` reaches the upstreams because the header is OUTSIDE the gateway's edge strip pattern, and that `services/referral/src/routes/referrals.ts:55` then falls back to it when the principal has no `walletAddress`. Its load-bearing READ premise is the first half: `TRUST_HEADER_PATTERN` at `trustHeaders.ts:40` matches `x-(user|tenant|organization|org|role|roles?|auth-user|policy|emitter|gateway-vouch)` followed by `-` or end, so `x-wallet-address` is not matched, `isStrippedTrustHeader('x-wallet-address')` is `false`, and `stripTrustHeaders` leaves the header in the bag while deleting its trust-family neighbours. The suite pins none of it: the file's six cells name `x-gateway-vouch`, the trust family, `x-tenant-override` and six unrelated `x-` headers, and the word `wallet` occurs 0 times in the file. This change adds ONE cell that asserts the predicate answer AND the bag outcome for `x-wallet-address` in one call, with `x-user-id` (removed) and `authorization` (kept) beside it as the liveness pair. Every existing cell is unchanged. **It pins TODAY's behaviour and decides nothing about KS-1223** — the ticket's recommendation is "owners measure it, then decide" between dropping the referral fallback and/or adding `x-wallet-address` to the edge strip; this cell is the second of those two shapes made visible to the suite, so a strip widening arrives as a deliberate red rather than a silent change.

## The exact change — ONE hunk in the test file

The new cell goes at the end of the `describe('KS-1041 Step 2 — x-gateway-vouch is stripped at the edge', ...)` block opened at `:30`, directly above that block's closing line `});` (`:113`, the file's LAST line and the ONE trailing context line). There is NO leading context: the line above (`:112`, `  });`) stays and is not written. Copy every line byte for byte. Every `+` line is ASCII only. There is no blank line anywhere in the fence. Keep the header exactly as shown. **Your diff MUST begin with the two file-header lines, above the `@@` line: `--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1041-vouch-header-strip.test.ts` then `+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1041-vouch-header-strip.test.ts`.**

```
@@ -113,1 +113,7 @@
+  it('RED KS-1223: x-wallet-address is OUTSIDE the edge strip - a client-sent value survives stripTrustHeaders while the trust family is removed', () => {
+    expect(isStrippedTrustHeader('x-wallet-address')).toBe(false);
+    const headers: Record<string, unknown> = { 'x-wallet-address': 'addr_client_supplied', 'x-user-id': 'user-1', authorization: 'Bearer real-token' };
+    stripTrustHeaders(headers);
+    expect([headers['x-wallet-address'], headers['x-user-id'], headers.authorization]).toEqual(['addr_client_supplied', undefined, 'Bearer real-token']);
+  });
 });
```

`isStrippedTrustHeader` and `stripTrustHeaders` are already imported by the file at `:26-27` (the `import { ... } from '../utils/trustHeaders';` at `:23-28`) — you add NO import. The cell needs no mock, no app boot, no port and no database: both are pure functions over a string / a plain object, and the file has no `vi.mock`, no `beforeEach` and no setup of its own.

## Cells

- `walletoutside` = `RED KS-1223: x-wallet-address is OUTSIDE the edge strip - a client-sent value survives stripTrustHeaders while the trust family is removed`

## Red cells

The cell below is a GENUINE assertion-red: it fails under each tamper and passes at the tip. It is declared here rather than with a red glyph in its title because every `+` line in this diff must be ASCII only.

- RED KS-1223: x-wallet-address is OUTSIDE the edge strip - a client-sent value survives stripTrustHeaders while the trust family is removed

## Tampers

Two single-line tampers on two DIFFERENT lines of `trustHeaders.ts`. They are the two places a "strip it" fix could land: the pattern, or the bag walker. Each `From` is the tip's line at that number, byte for byte, and each `To` is valid TypeScript, so nothing fails to load and no cell reds for the wrong reason. Each `From` line occurs EXACTLY ONCE in the file (counted).

### WALLETINPATTERN — the strip pattern gains a wallet alternative
File: `Blockchain/Dev/services/api-gateway/src/utils/trustHeaders.ts`
Line: 40
From:
```
  /^x-(user|tenant|organization|org|role|roles?|auth-user|policy|emitter|gateway-vouch)(-|$)/i;
```
To:
```
  /^x-(user|tenant|organization|org|role|roles?|auth-user|policy|emitter|gateway-vouch|wallet)(-|$)/i;
```
Reds: `walletoutside`

### BAGDELETESWALLET — the bag walker deletes x-wallet-address by name, outside the pattern
File: `Blockchain/Dev/services/api-gateway/src/utils/trustHeaders.ts`
Line: 52
From:
```
    if (isStrippedTrustHeader(header)) {
```
To:
```
    if (isStrippedTrustHeader(header) || header.toLowerCase() === 'x-wallet-address') {
```
Reds: `walletoutside`

## Controls

- `strips a client-supplied x-gateway-vouch`
- `removes it from a header bag alongside the rest of the trust family`

*(Both are FULL `it(...)` titles, copied byte for byte from the file at the tip — `:31` and `:45` — each occurs exactly once in the file and neither is a prefix of any other title. For a VITEST suite the checker matches a declared cell by its FULL title, never by a prefix; the prefix rule in `build_test_only_input.sh`'s header is for BASH suites only (the KS-1275 round-1 FAIL, 2026-09-20). The file's other four cells are also green under both tampers but are left undeclared: `:36` is an `it.each` whose titles are `%s`-substituted at run time, and `:71`, `:79`, `:95` carry an em dash (non-ASCII) in their titles. The `:45` control is the strongest liveness proof in the file: it drives the SAME `stripTrustHeaders` loop that BAGDELETESWALLET mutates and the SAME pattern that WALLETINPATTERN widens, and stays green under both because its bag carries no `x-wallet-address`.)*

## THE CELLS — state it to yourself before you write a line

At the untouched tip the new cell passes: `x-wallet-address` matches none of the ten alternatives at `:40` (the token after `x-` is `wallet`), so `isStrippedTrustHeader` returns `false`; `stripTrustHeaders` then deletes `x-user-id` (matched by `user`) and leaves `x-wallet-address` and `authorization`, which is exactly the triple the cell asserts.

Under **WALLETINPATTERN** the first `expect` fails by assertion: `isStrippedTrustHeader('x-wallet-address')` is now `true`. Under **BAGDELETESWALLET** the first `expect` still passes (the predicate is untouched) and the second fails by assertion: the bag no longer holds `x-wallet-address`, so the triple is `[undefined, undefined, 'Bearer real-token']`. Under BOTH, every existing cell stays green: `:31`, `:36` and `:71` ask the predicate about `x-gateway-vouch` / `x-tenant-override`, which neither tamper changes; `:45`'s bag has no `x-wallet-address`, so the extra alternative and the extra `||` arm both match nothing in it; `:79`'s six unrelated headers contain no `wallet` token; `:95` tests the pattern against ten headers that still match.

## Premises (measured — by reading the tip, NOT by running anything)

- **Premise: the two `From` lines.** `trustHeaders.ts` at `dc061f2bb`, line 40 is `  /^x-(user|tenant|organization|org|role|roles?|auth-user|policy|emitter|gateway-vouch)(-|$)/i;` and line 52 is `    if (isStrippedTrustHeader(header)) {`, byte for byte; each occurs **exactly once** in the file (`grep -n -F`, one hit each). The word `wallet` occurs **0** times in `trustHeaders.ts`.
- **Premise: the anchor.** The test file is **113** lines; `:113` is `});` (column 0, the file's last line, the ONLY column-0 `});` in the file, closing the `describe` opened at `:30`) and `:112` is `  });`. The trailing context line is non-blank and the insertion is pure, so no blank line is asked of you anywhere.
- **Premise: nothing pins this today.** `KS-1223`, `wallet` and `addr_client` occur **0** times in the test file at the tip, and `git grep -il x-wallet-address` over `services/api-gateway/src/__tests__/` at the tip returns **0** files.
- **Premise: no `+` line re-adds a tip line.** The only `+` line that also occurs at the tip is the closing `  });` (unavoidable for a new cell).
- **No backslash** in any `+` line (0, counted). **No non-ASCII** in any `+` line (0, counted). The title uses `-`, not an em dash.
- **Premise: the runner.** `api-gateway/package.json` at the tip has `"test": "vitest"` and `vitest ^4.1.9` in devDependencies, with no `jest` / `ts-jest` — the builder auto-detects vitest and the `Runner:` line above agrees with it. `vitest.config.ts` sets `setupFiles: ['./vitest.setup.ts']` and no `include` narrowing.
- **Premise: no live-lane collision.** `trustHeaders.ts` is not `enforcement.ts`, `startup-migrations.ts` or `index.ts`, and is not under `services/anchoring/**`; the test file is not `documents.ts`. `grep -il 'trustHeaders|ks1041-vouch-header-strip'` over the 215 held `READY_*` files returns **0**. `git log` on `trustHeaders.ts` at the tip shows one commit (#951, KS-1041 Step 2); no remote branch names 1223 or wallet-address.
- **Premise: the surface.** `trustHeaders.ts` is the gateway's inbound header strip. The cell constructs no user, no token, no session and no MFA state; it calls two pure functions. Zero product bytes. Flagged so the "auth product EDITS stay out" rule is applied with the facts: this is a pin, not an edit, and the file is request hygiene rather than an auth handler.

## MEASURED by the writing seat (2026-09-20 23:25-23:27, `--shared` scratch clone at `dc061f2bb`, node_modules farmed from the source checkout, source tracked-modified count 0 after)

- REAL `tasks/test_only/checker.sh` on this brief's own diff: **RESULT: PASS (8/8)**, `apply=strict` (header counts right: 6 `+` and 1 context = 7). T5 green at the tip 9/9 cells in the file; T6 WALLETINPATTERN reds exactly `walletoutside`, T6 BAGDELETESWALLET reds exactly `walletoutside`, every red an assertion failure; T7 both controls green under both; T8 `trustHeaders.ts` restored by bytes (sha256 c6cd7b504ea1 == tip blob) after each.
- Two WRONG variants refused at the named gates: a control declared as the PREFIX `strips a client-supplied` -> **FAIL T5** `DECLARED CELL NOT IN THE RUN`; a predicate-only cell (no bag walk) -> **FAIL T6[BAGDELETESWALLET]** `reds NOTHING (0 of 9 cells failed)`.
- Whole api-gateway vitest suite at the bare tip: **68 files, 674/674 green**; with the cell applied: **68 files, 675/675 green** (+1 = this cell). `tsc --noEmit -p services/api-gateway/tsconfig.json` with the cell applied: **rc 0, 0 errors**.
- Artefacts: `2_Project_Files/local-model/runs/2026-09-20_ks1223WALLET-1-drafter-precheck/` (checker.log, patch.diff, var1/, var2/, full_suite.log, tip_suite.log, tsc.log).
- NOT measured: the referral-service half of KS-1223 (`referrals.ts:55`) is NOT pinned here and NOT measured; no live stack was booted and no port was touched.

## Output

Exactly ONE ```diff block, nothing outside it: `--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1041-vouch-header-strip.test.ts` / `+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1041-vouch-header-strip.test.ts`, then the hunk above exactly as shown (`@@ -113,1 +113,7 @@`).

## Notes for the raise (not for the model)

- Test-only, zero product bytes. **Raise tier: TIER 2. Refs KS-1223** (and KS-1041, whose file this is; KS-744 is the gate that found it). **NEVER Closes** — KS-1223's recommendation is "owners measure it, then decide"; this brief takes no part of that decision.
- **Not from a gate cell.** Found by the 2026-09-20 widened sweep of the whole KS Backlog/Todo (360 tickets) for test-only pins; the ticket's load-bearing premise (the header is outside the strip) is provably invisible to the suite today.
- **Collision: none.** No held `READY_*` carries a hunk in the test file or in `trustHeaders.ts`.

## Build line (not for the model)

```
bash tasks/test_only/build_test_only_input.sh KS-1223 night/inputs/test_only_1223WALLET-1.json night/briefs/KS-1223-WALLET-1.md ctx=65536
```
