matches 1
=====MSG 2026-09-16T23:07:35.000Z {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'} chars 5701
Seat A

## BLUF
- READY FOR QA: #1019 KS-1187 @ 8b8996f8b290ef55c35721c30f8671f982fa5a91 (https://github.com/Secuura/Distributed_Secuura/pull/1019). TIER 1, per your ANSWER 22:51:36Z.
- Built to (1) + (2) with Tightenings A and B, in `routes/proxy.ts` only, plus one cell of `ks843-erasure-scope-gate.test.ts`. That existing source pin required the literal whole-string collapse, which IS this bug; the first tamper run's T0 red exposed it.
- Red before green: at base the 13 real-app refusal cells are 200 with an upstream hit (the bypass reproduced), all AssertionError. The 19 verdict-table cells are TypeError (the function does not exist at base; stated as such).
- Tamper: 5 rows, all as predicted in the final run, tsc rc 0 each, 481 gateway + 851 shared cells per row.
- Open PRs of mine: #1017, #1018, #1019. That is 3 of 3.

## Recommendation
Commission the tier-1 gate at 8b8996f8b. Merge authority is your GO per the card default; KS-1187 stays In Progress on merge (§5f, the edge unmeasured).
**Question:** the brief caps KS-1187 at the two comments already posted (8a59cf75 is the second). So I have NOT posted the usual "PR raised" facts comment on the ticket. Say if you want one.
**Usage:** at your 36% reading, this seat is close to Kam's 40% cut. I will hold 3 of 3 and start nothing new unless you say so. The N-1 (KS-1202) measurement is next only on your word.

## Detail
**Links:** attachmentsForURL(pull/1019) = [('KS-843', 'closes', 'In Progress'), ('KS-1187', 'contributes', 'In Progress')]. KS-1187 state now In Progress (moved by the branch name / PR link, not by me). KS-1187 carries 2 comments from me (the ruling and the severity reads); none added for the PR.

**Commits** (branch = Linear's branchName, cut `--no-track` at develop fa887f382; shared .git/config sha unchanged):
- 50a4b749a: proxy.ts + the new test file.
- 8b8996f8b: the ks843 source pin.

**The wrapper** (`proxy.ts`):
- `erasureDoorVerdict(collapseRepeatedSlashes(original), erasureDoorCaseSensitive)`;
- not-door → next() (as before);
- undetermined → 400 NON_CANONICAL_PATH;
- door → req.url = the canonical path, erasureDoor(...), restore req.url = original, next().
- `erasureDoorCaseSensitive` is read from the door Router's own `caseSensitive` (undefined → false; Tightening B), and pinned by the upper-case real-app cell plus a verdict cell with caseSensitive true.
- `erasureDoorVerdict` is exported and is the only implementation; the test imports it.

**Tightening A, which refusal is which:**
- 403 = the canonical sub-path names the door;
- 400 = the first effective segment is undecodable, or `..` climbs out of the mount;
- forwarded = plainly not the door, including a malformed escape in a later segment.
- Controls: a plain non-erasure read, an odd but decodable spelling and a malformed-later-segment path, all 200 with 1 hit, identical at base.

**Cells:** 39.
- The verdict table: 19.
- Real app, test mode: 10 request shapes → 403, 0 hits; 2 shapes → 400, 0 hits; origin-form without the scope → 403; WITH the scope: origin-form, the other target form and a spelled path are admitted and forwarded as sent (req.url restored); the 3 Tightening A controls.
- Production mode: the 2 v1 shapes the gate measured passing → 403, 0 hits; WITH the scope → admitted.

**Harness note:** the connector tokens carry `email: 'connector@secuura.io'` (as generateConnectorToken mints it). The first head run had every forwarded cell at 500 `Invalid value "undefined" for header "x-user-email"`: the KS-744 class, and my side-item-8 finding reproduced in a harness.

**Red before green** (proxy.ts at base bytes, restored by sha): 39 run, 7 green, 13 AssertionError, 19 TypeError. With the fix: 39/39.

**Tamper** (final run at 8b8996f8b; each row = whole api-gateway suite 54 files / 481 run + packages/shared 44 / 851 + tsc; restored by sha + `git diff --quiet HEAD`; porcelain clean):

| Row | Tamper | Reds (all AssertionError) |
|---|---|---|
| T0 | none | 0 |
| T739 | the whole-string collapse restored | 7: 4 test-mode target-form cells, 2 production v1, the ks843 source cell |
| TC | the canonical check removed | 8: the 5 spellings, 2 × 400, the ks843 source cell |
| TW | the 400 widened to all non-door gdpr | 4: 3 Tightening A controls + ks843-erasure-path-bypass "a non-erasure /api/gdpr path is untouched by the gate" |
| TI | inert | 0 |

- shared had 0 reds on every row.
- **SLIPS, stated:**
  - the first run (at 50a4b749a) had T0 = 1 red: the ks843 pin, fixed in the second commit;
  - its TW row had that same ks843 control red, which I had not predicted.
  - Predictions for the final run were written before it.
  - Records: `2026-09-17_seatA-3rd/ks1187/build/tamper.run1-at-50a4b749a/` and `…/tamper/`.

**eslint:** proxy.ts has 4 warnings at base and head, the same messages with line numbers removed; the ks843 test 0/0; the new test 0.

**Push:** rc 0, 23:01:07Z → 23:06:45Z; `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` (legs 3/4/8, no stack; not a pass of those); PROTOCOL-CLEAN (first push, tracking ref at origin's head).
**Stubs:** this push left 4 login_stub.mjs listeners (23:04:00-03Z); each re-identified (command, cwd, ppid 1, started after the push) and SIGTERM'd; 0 remain; controls 47787/11434/5432 present before and after.

**PR body:** "Refs KS-1187" with the ticket URL. A guard refused any spelling, target literal or at-mention in the body; closing phrases 0 (control 2 of 2). The Linear branch name itself contains the words "absolute-form request target" (Linear's suggestion, unchanged).

**NOT run:** the edge (a real nginx/Caddy); a real originate; Schemathesis/Akto/Playwright/k6 (no stack; Schemathesis per your (a)).

