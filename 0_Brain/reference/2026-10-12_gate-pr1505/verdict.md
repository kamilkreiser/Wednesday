# QA gate: Secuura Platform K PR #1505 (KS-1185 F1)

- Head: `c4d43567df35c06eaf8f550d8e246b0774fbbb33` (bundle ref confirmed exact; one commit, 2 files, +155/-2)
- PR merge-base: `6b978ca38442be9b8e54f176da9738cef430ee99`
- Gated against real current `origin/develop` = `cc2939bbf3521c5f6d8789befc04deda83f44cdf` (fetched read-only; head merged onto it with no conflicts; merged diff vs develop is the same 2 files, +155/-2)
- Gate clone: scratchpad `gate1505/clone`, branch `merged`. Nothing written to `!CODING`.

## VERDICT: GO WITH NOTE

The change does what it says: the only shipped caller passes no override, so nothing changes at runtime, and every invalid bound I tried throws at construction. The note is one small hole in the cells (BigInt is not covered) and the stated departures are sound.

## By my runs

Node v24.7.0, merged tree (develop cc2939bb + c4d43567).

- Callers (whole repo, `git grep`): exactly ONE non-test caller of `createVerificationRoutes`, `services/api-gateway/src/index.ts:898`. It passes no `originateForwardTimeoutMs`, and nothing env-derived, config-file-derived, script, doc, or other-service code sets it (grep over non-.ts files: zero hits; positive control: the .ts grep returned the ks1087 test and verification.ts). The only test that passes an override is ks1087 with `1_000` (valid). So throwing at construction cannot break startup in any shipped configuration. No Major.
- New file, on the head: 14/14 pass. On the base `verification.ts` (develop's) with the new test file: 9 failed, 5 passed (0, -1, NaN, Infinity, null, '800', 1.5, 2147483648, true all red; the 5 controls undefined/1/800/2147483647/closed-port-502 green). Author's "9 cells red on the base" confirmed.
- Gateway suite: 114 files, 1100 tests, all pass.
- `tsc --noEmit` (api-gateway): rc 0.
- eslint on the two touched files: 0 errors, 5 warnings, all on lines the PR does not touch (651, 1058, 1177, 1493, 1569; the diff is at 112-155 and 463-468), so pre-existing.
- `npm run check:test-types` on the merged tree: rc 0. auth 42 errors, 42 in baseline, 0 new; api-gateway 35 errors in baseline, 0 new, 0 stale, 114 test files examined (new file included). Positive control: the baseline is non-empty and matched, so the checker was really counting.
- `npm run check:openapi`: rc 0 ("CHECK PASS", 413 example blocks resolve).
- Harness note: to run vitest I symlinked the project's node_modules into the scratch clone (re-pointing `@secuura/*` at the clone) and built `packages/shared` there; no project files touched.
- Tampers (restored after, file byte-identical confirmed). Running ks1185 + ks1087 cells:
  - Author's four re-run: A1 ceiling check removed -> the 2147483648 cell red (1). A2 `> 0` removed -> 0 and -1 red (2). A3 isInteger->isFinite -> 1.5 red (1). A4 undefined no longer the default -> the GREEN undefined control plus the sibling F4 default-bound cell red (2).
  - Mine: M1 guard accepts 0.5 -> caught only through the 1.5 cell (no 0.5 cell of its own; any non-integer is caught by 1.5). M2 numeric-string coercion `Number(value)` -> '800' and true red (2). M3 ceiling `<` (off by one low) -> the 2147483647 edge control red. M4 ceiling `<= MAX+1` -> the 2147483648 cell red. M5 lower edge `> 1` -> the 1 ms control red. M7 boolean via unary plus -> '800' and true red. M8 validated but the raw override used at runtime (default lost) -> the sibling F4 cell red (not the new file; the new file builds with undefined but never fires). M9 resolver returns the default instead of throwing -> all 9 refusal cells red.
  - M6 BigInt accepted (extra clause `typeof value === 'bigint' && value > 0n`): NOT CAUGHT, 27/27 green. See Finding 1.
  - 12 of 13 caught; the one escape is the BigInt tamper.

## Findings

No Major.

**Minor 1: no BigInt cell.** `Number.isInteger(1n)` is false, so the shipped code refuses a BigInt, but no cell pins it, and tamper M6 (accepting a positive BigInt) passes the whole suite. A BigInt reaching `setTimeout` throws ERR_INVALID_ARG_TYPE, i.e. the same class as '800'/null that the cells do cover. Reachable only by a future caller passing a BigInt. Suggest adding one row to `REFUSED` (`['1n', 1n, '1']`). Not a merge blocker.

**Note 1: refusal message is ambiguous for two values.** `String(1n)` prints `1` and `String(-0)` prints `0`, so "(got 1)" can describe a BigInt and "(got 0)" can describe -0. Cosmetic.

**Note 2: the test file builds with `undefined` but never fires the default.** The "no override means 15 s" runtime behaviour is pinned by the sibling F4 default-bound test (it caught tamper M8), not by this PR's cells. Fine, but this PR's claim "default 15 s unchanged" rests on that sibling file.

**Note 3: author claims I did not re-check.** First push under the 16-leg hook ("13/16 legs ran, 3 SKIPPED") is a process claim I cannot see; I did not run the hook.

## The two departures

1. **Ceiling 2147483647 (the ticket says "finite integer > 0").** Right call. Measured on v24.7.0 with `http.ClientRequest#setTimeout` (the call the route makes): 2147483647 and 1 are accepted silently; 2147483648 prints `TimeoutOverflowWarning` ("Timer duration was truncated to 2147483647"), i.e. about 24.8 days, effectively "never", which is exactly the failure the ticket is trying to remove. Control: the global `setTimeout` behaves differently (an overflowing value there becomes 1 ms), so the claim holds specifically for the request timer, which is the one used. A ceiling is strictly within the ticket's intent and cannot reject any useful value. It is the author's own addition and is stated as such.
2. **Not reordering the 'error' listener before `setTimeout`.** Right call. With the bound an integer in [1, 2147483647], `ClientRequest#setTimeout` cannot throw (confirmed 1 and 2147483647 on a live request; the throwing values are all refused earlier at construction). The listener at line ~1076 is attached synchronously right after, so there is no window left that the reorder would close, and no test could demonstrate it. Skipping it is justified and stated openly. The only residue is that the guard now carries the whole protection; the 9 refusal cells hold it.

## NOT tested

- No real approve-forward against a server that never answers (the author's "800 fires at 804 ms" run): I did not repeat it. I ran the PR's own closed-port cell (502, pending doc kept) and the Node timer behaviours directly, but not a hanging-server timing.
- The 16-leg pre-push hook, CI, and any Docker/e2e legs (not allowed here).
- `check:test-types` was run only on the merged tree here, not on the bare PR base.
- No deploy or live gateway boot: the "fails when the gateway boots" benefit is argued from `index.ts:898` calling the factory at startup, not observed.
- Other Node versions (only v24.7.0).
