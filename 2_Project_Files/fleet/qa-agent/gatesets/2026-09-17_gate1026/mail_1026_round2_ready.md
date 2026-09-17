SUBJECT: [Secuura/Blockchain -> Wednesday] READY FOR QA (round 2 delta): #1026 KS-839 @df97c0def4b3f1be3db0172e3f0e464b53fc1d42 (TIER 1)
TS: 2026-09-17T10:14:16.000Z
AUTH: {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'}
Seat A

## BLUF
READY FOR QA (round 2 delta): #1026 KS-839 at `df97c0def4b3f1be3db0172e3f0e464b53fc1d42` (tier 1).
- **The fix:** `oauth.ts:353` → `if (allowed.some(entry => parseScopeString(entry).includes('*'))) return [];`. `parseScopeString` is the SAME function the token route re-splits with, defined in the same file at `:357`: a plain `scope.split(/[\s,]+/).filter(s => s.length > 0)`, with no second regex and no import. `:354` is byte-unchanged.
- **Cells added:**
  - 🔴 R3: the 8 padded carriers grant `[]` with `scope` omitted, and mint no `'*'` through the join/re-split.
  - 🔴 R4: the 8 carriers grant `[]` for a named request.
  - CONTROL 2: the zero-width-space `*` and fullwidth `*` stay literal; explicit, empty and `documents:*` lists are unchanged.
- **Red-proof:** R3 and R4 are red at BOTH develop's bytes and round 1's bytes (`8ab493354`). **Tampers: 10 / 10 as predicted, 0 VOID**, whole auth suite 63 files / 758 tests on every row, restored by sha. That includes the six round-1 rows, G-TRIMSTAR reversed (R3 + R4), and G-TRIM-ONLY, `entry.trim() === '*'` (R3 only).
- develop `19f1e5475` merged in (tree = prediction `2455003d0`, which is also your drafter's predicted tree over #1025). Push PROTOCOL-CLEAN. Preflight ran 12/15 legs, 3 SKIPPED (no stack), nothing failed. 4 stubs of mine ended by pid, 0 remain.
- **KS-1085 facts comment posted: `063d309f-6c94-4060-80c0-912e7240e3bf`** (10:05:31Z, read back, 5 / 5 anchors), per your 10:04:46Z RECEIVED. No new launcher ticket.

## Recommendation
1. **Gate the head `df97c0def`** (tier 1). The round-2 change is that one commit; `0c0a38753` only brings develop in.
2. **No KS-839 comment names #1026.** Its one comment, `15b8fe60` (06:47Z), relays Kam's two lines and predates the PR. The PR ↔ ticket link is the attachment (`contributes`). **Default:** one BLUF facts comment on KS-839 naming #1026 and both rounds, posted after the verdict (with the merge facts if it merges), the same timing you ruled for KS-1050. Say if you want it sooner.
3. **Next:** KS-744 (your hold lifts now that this READY is out). I merge develop in again (the real merge on `middleware/auth.ts` against #1023), re-run api-gateway + tsc, push as the third open PR, and send READY. The #1018 and #1026 GOs come to me when they arrive.

## Detail

### Head and push
- Branch `feature/ks-839-security-an-allowedscopes-of-bypasses-the-invalid_scope`, fast-forward `8ab493354` → `df97c0def4b3f1be3db0172e3f0e464b53fc1d42`:
  - `0c0a38753`: merge of develop `19f1e5475` (parents `8ab493354`, `19f1e5475`). #1025 changed only `scripts/audit/audit-baseline.json`. The tree `2455003d0` equals the read-only `merge-tree` prediction.
  - `df97c0def`: round 2 (parent `0c0a38753`): `oauth.ts` +1 −1, ks839 test +51 −2.
- Reviews endpoint on #1026 immediately before the push: 0 reviews. Origin develop at push time: `19f1e5475`.
- Push 10:06:43Z → 10:12:41Z, rc 0. push_protocol verify: PROTOCOL-CLEAN, fast-forward, config identical, worktrees identical, 113 heads identical, other refs changed 0.
- **Origin now:** `refs/heads/<branch>` = `refs/pull/1026/head` = `df97c0def4b3f1be3db0172e3f0e464b53fc1d42` (ls-remote read again in the send action below).
- PR REST after the body PATCH: open, 5 commits, changed_files 2, mergeable true / `unstable`.
- In-hook preflight: `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` Legs 3, 4 and 8 skipped (no local stack): not a pass of those. Leg 1 `spec is in sync`; leg 5 59 / 59; audit-gate 33 advisories / 34 baselined; audit-locks 43 locks; shell suites 35 / 35.

### The change, read at the head
```
352 export function validateScopes(requested: string[], allowed: string[]): string[] {
353   if (allowed.some(entry => parseScopeString(entry).includes('*'))) return []; // KS-839: a wildcard grants nothing, padded or not (' *', 'openid,*' split to '*' on the way to the token)
354   return requested.filter(s => allowed.includes(s));
355 }
357 export function parseScopeString(scope?: string): string[] {   (unchanged; a function declaration, so it is hoisted)
```
**The path the cells mirror** (`routes/oauth.ts` at the head, unchanged by this PR):
- `:389` `const requestedScopes = parseScopeString(scope);`
- `:390-392` `validateScopes(requestedScopes.length > 0 ? requestedScopes : app.allowedScopes, app.allowedScopes)`
- `:776` `scope: client.grantedScopes.join(' ')`
- `:972` `parseScopeString(result.scope || '')` at the token route.

### Cells (the REAL `validateScopes` + `parseScopeString`; the file mocks only `../db` and `../utils/logger`, as round 1 did: 2 stubs)
- `mintedWithScopeOmitted(a)` = `parseScopeString(validateScopes(a, a).join(' '))`.
- 🔴 R3 asserts `[name, validateScopes(a, a), mintedWithScopeOmitted(a)]` = `[name, [], []]` for all 8 carriers.
- 🔴 R4 asserts `validateScopes(parseScopeString('openid documents:read admin:everything *'), a)` = `[]` for all 8. Reading the code, only `['openid', ' *']` leaks at the two older trees (it grants `['openid']`), so R4 is red there on that one carrier. vitest truncates the diff, so this is READ, not printed.
- CONTROL 2: `validateScopes(['*​'], ['*​'])` = `['*​']`, minted `['*​']`; the same for `'＊'`; `['documents:read']` vs `['documents:read', 'openid']` → `['documents:read']`; `['openid']` vs `[]` → `[]`; `[]` vs `[]` → `[]`; `['documents:*']` vs `['documents:*']` → `['documents:*']`. U+200B is not in JavaScript's `\s`, so `parseScopeString` leaves it; that is the measured behaviour and why it is a control.
- `EXPECTED_CELLS` 3 → 6; COMPLETENESS unchanged.

### Red-proof and tamper table
Runner `5_Project_History/2026-09-17_seatA-6th/ks839-r2/tamper.py`, output `tamper/tamper.json`, 20:05:22 → 20:06:09 AEST. Each row:
- one anchored edit (count 1) or a blob swap;
- `tsc --noEmit -p .` (non-zero = VOID);
- the WHOLE auth suite, denominator asserted = T0's (63 / 758 / pending 0);
- restore by bytes against the HEAD blob plus `git diff --quiet HEAD`.

Every red is an `AssertionError`; 0 load failures; 0 reds outside the ks839 file on every row.

| Row | Form | ks839 reds (pred = measured) |
|---|---|---|
| T0 | none | 0 |
| RP-DEV | `oauth.ts` = `19f1e5475` bytes | R1 `expected [ 'admin:everything' ] to deeply equal []`, R2, R3, R4 |
| RP-R1 | `oauth.ts` = `8ab493354` bytes | R3 `expected [ …(8) ] to deeply equal [ [ 'space-star', [], [] ], …(7) ]`, R4 |
| DEL353 | line 353 deleted | R2, R3, R4 |
| REVERT | `if (allowed.includes('*')) return requested; // Wildcard — all scopes` | R1, R2, R3, R4 |
| NEVERFIRES | `includes('**')` inside the new line | R2, R3, R4 |
| NOCOUNT | R1's `CELLS_RUN += 1;` removed | COMPLETENESS `expected 5 to be 6` |
| TI | inert comment after line 354 | 0 |
| G-TRIMSTAR reversed | line 353 back to round 1's `if (allowed.includes('*')) return [];` | R3, R4 |
| G-TRIM-ONLY | `if (allowed.some(entry => entry.trim() === '*')) return [];` | R3 |

How the round-1 rows moved: DEL353 and NEVERFIRES now also red R3 and R4, and REVERT reds all four, because the padded cells exist. TI's anchor is still `:354`. G-TRIM-ONLY is new. It shows that a different tokenizer is caught: trimming catches the padded carriers but not `',*'`, `'openid *'` or `'openid,*'`, so R3 reds. R4 stays green on that row, because the one carrier that leaks there (`['openid', ' *']`) is caught by the trim.

### Suites, tsc, eslint (ratios)
- ks839 alone 7 / 7.
- Whole auth suite 63 / 758, 0 failed, 0 pending (round 1: 63 / 755; develop 62 / 751 per your drafter).
- `packages/shared` not re-run: its subtree at the head is byte-identical to develop `19f1e5475`'s (`dbd72dea0`), which I ran at 44 / 851 on #1018's branch today.
- `tsc --noEmit -p services/auth` rc 0.
- **Test-including program** (scratch tsconfig extending auth's, all of `src`, `exclude: []`, ks839 test in the program by `--listFilesOnly`): rc 2, 68 error lines, all in pre-existing test files, **0 in the ks839 test, 0 in `oauth.ts`**.
  - Caveat: your #1026 drafter read 37 lines on both of its trees. My instrument reads 68 on this tree and on #1018's. The tsconfigs differ in something I have not isolated, so the two counts are not comparable. Only the "0 in the touched files" reading is mine to claim.
- **eslint:** `oauth.ts` 0, ks839 test 0. Control: `oauth.ts` on stdin with an unused const appended → `no-unused-vars` fires.

### PR body (PATCHed and read back byte-equal)
- **Title:** `KS-839: an OAuth app allow-list holding the wildcard, exact or padded, grants nothing`.
- **Body:** the `Linear:` URL line, then a new BLUF / Recommendation / Round 2 section, then `## Round 1 record (kept as written; its "the wildcard grants nothing" held for the exact '*' only, and round 2 extends it to padded entries)` holding round 1's body verbatim with headings demoted.
  - The Round 2 section covers: what round 1 missed, with the drafter's measured route behaviour; the fix; new cells; red-proof; tamper table; Test Evidence; platform suites; PII.
  - Its Recommendation records three items NOT widened into: KS-1210 (registration accepts any scope string), the `documents:*` literal with `requireScope` vs `hasScope` disagreeing, and the route default pinned by no ROUTE cell (G-ROUTE-DEFAULT-BYPASS 0).
- Closing phrases 0 (control fires), at-signs 0, `Refs KS-839`, Claude Code footer.

### Links, stubs
- `attachmentsForURL(pull/1026)` after the push = KS-839 `contributes` (In Progress). Controls: pull/1018 → KS-1050 `contributes`; pull/99999 → [].
- **Stubs:** `stop_push_stubs.py` (ps rows parsed 1094). 4 targets, pids 40777 / 40850 / 40926 / 40995, started 20:09:47-50 AEST, cwd this worktree, ppid 1, all SIGTERM'd; 0 alive after 2 s. LISTEN node rows 4 → 0.
  - One more process matched my census pattern and is not a stub: pid 55043, a `/bin/zsh -c` tool shell with cwd `/Volumes/DevMASTER/WEDNESDAY` (ppid 43676), whose command line names `login_stub.mjs`. That is presumably Wednesday's own census. It listens on nothing and was left alone.
  - Seat B's 4 stubs from 19:58 are gone; that seat wrapped.

### NOT done / NOT covered
- the authorize and token ROUTES end to end with a padded allow-list at this head (the drafter measured the round-1 head there);
- the gateway `requireScope` against a round-2 token;
- a live `oauth_apps` census;
- Schemathesis / Akto / Playwright / k6 (no stack);
- the KS-839 contract sentence (`auth.openapi.ts:2553` / `:2672`) and KS-805, which still wait for #922.

