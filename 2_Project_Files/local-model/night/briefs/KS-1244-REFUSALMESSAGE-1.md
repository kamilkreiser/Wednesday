# KS-1244 REFUSALMESSAGE-1 PIN THE EXACT 401 BODY THE GATEWAY ANSWERS WHEN AN sk_ KEY FAILS VALIDATION ON A REQUIRED MOUNT — `{ success: false, error: { code: 'UNAUTHORIZED', message: 'Invalid API key' } }`, for a Node-joined key pair AND a single unknown key — Wednesday's task for Ornith, TEST_ONLY, **ONE existing test file, one hunk, one cell added, no product file** (written 2026-09-21 after the #1112-#1118 batch gate; its NOT-PINNED row REFUSALMESSAGEUNPINNED, KS-1244, measured 0 red of 685 at the #1114 head)

File: `Blockchain/Dev/services/api-gateway/src/__tests__/auth.test.ts`
Tip: `7be81d5c9b109959b559e03652fb092c12de58e8`
Runner: `vitest`

Written from develop `7be81d5c9b109959b559e03652fb092c12de58e8` (`git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" ls-remote origin refs/heads/develop` on 2026-09-21, read verbs only; the tree that carries the seven #1112-#1118 squashes, #1114 = KS-1244 JOINEDKEY-1 + KS-1198 SKMETA-1 included). The test file at that tip is **309 lines** (blob `6d837e0aeeb8`), read whole; its full content is in `files[...]` of your input. The product the cell pins is `Blockchain/Dev/services/api-gateway/src/middleware/auth.ts` (blob `bf09d315a644`, **432 lines**): `export function authenticateToken(required: boolean = true)` at `:273`; the API-key path `:275-:282` — `apiKey` (`:276`), `presentedKey = Boolean(apiKey && apiKey.startsWith('sk_'))` (`:277`), `meta = … await validateApiKey(apiKey) : null` (`:278`), `if (presentedKey && !meta && required) {` (`:279`), and on **`:280`** the refusal `      res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Invalid API key' } });` (whole-line ×1 in the file; `Invalid API key` occurs on no other line). This service runs **VITEST** (`package.json` `"test": "vitest"`, `vitest.setup.ts` generates an RS256 pair and provisions `JWT_PUBLIC_KEY` + `__TEST_JWT_PRIVATE_PEM`; no jest).

## THE MODE — read this twice

**TEST_ONLY.** Your diff touches EXACTLY ONE file: the test file above, MODIFIED IN PLACE (`--- a/<path>` / `+++ b/<path>`, the path exactly as written above). You never touch `middleware/auth.ts` or any other product file: the behaviour is already what it is at the tip, and this cell PINS it.

## What the cell pins (one paragraph)

#1114 (KS-1244 JOINEDKEY-1) added the cell at `:220-:234` of this file: a repeated `x-api-key` (two individually valid keys that Node joins into `'sk_first, sk_second'`) on a REQUIRED mount is refused 401 with no principal and no Bearer fall-through, in either order. That cell asserts `res._json?.success` and `res._json?.error?.code` — never the MESSAGE. The #1112-#1118 gate planted `message: 'Invalid API key'` → `message: 'nope'` on `auth.ts:280` and measured **0 red of 685**: the refusal's message, which integrators read and which the gateway's own `:165` (`Authentication required`) and `:201` (`Invalid or expired token`) neighbours already pin for THEIR branches, is unpinned for the API-key branch. This change adds ONE cell, directly under the KS-1244 cell and inside the same `describe('authenticateToken')`, that drives `authenticateToken(true)` twice through the file's own `makeReq`/`makeRes` fakes with `fetchMock` answering `{ data: { valid: false } }` — once with the Node-joined pair `'sk_first, sk_second'` (the ticket's own drive; `apiKeyCache` is cleared by the file's `beforeEach`, so the joined string goes to `validateApiKey` and comes back null) and once with a single unknown key `'sk_ks1244-unknown'` — each with a Bearer beside it, and asserts for both `[presented, next calls, status, body] = [presented, 0, 401, { success: false, error: { code: 'UNAUTHORIZED', message: 'Invalid API key' } }]` — the WHOLE body by `toEqual`, so the message is pinned and so is the absence of any extra field. **It pins TODAY's wording**: if the owners ever change the message on purpose, the cell goes red on purpose and is rewritten with the new text.

## The exact change — ONE hunk in the test file

The cell goes at the END of `describe('authenticateToken', …)` (`:135-:235`): after `:234` (`    });`, the close of the KS-1244 cell) and before `:235` (`  });`, the close of the describe). `    });` and `  });` each occur many times in the file, so the hunk carries THREE leading context lines — `:232` (`      }`), `:233` (`      expect(outcomes).toEqual([['sk_first, sk_second', 0, 401, false, 'UNAUTHORIZED', undefined], ['sk_second, sk_first', 0, 401, false, 'UNAUTHORIZED', undefined]]);`, **unique in the file**) and `:234` (`    });`) — and ONE trailing context line (`:235`). Copy every line byte for byte. Every `+` line is ASCII only (the title uses `-`, never an em dash). There is no blank line anywhere in the fence. Keep the header exactly as shown. **Your diff MUST begin with the two file-header lines, above the `@@` line: `--- a/Blockchain/Dev/services/api-gateway/src/__tests__/auth.test.ts` then `+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/auth.test.ts`.**

```
@@ -232,4 +232,17 @@
       }
       expect(outcomes).toEqual([['sk_first, sk_second', 0, 401, false, 'UNAUTHORIZED', undefined], ['sk_second, sk_first', 0, 401, false, 'UNAUTHORIZED', undefined]]);
     });
+    it('RED KS-1244: an sk_ key that fails validation on a required mount is refused with the exact body 401 UNAUTHORIZED Invalid API key - a Node-joined pair and a single unknown key alike', async () => {
+      fetchMock.mockResolvedValue({ ok: true, json: async () => ({ data: { valid: false } }) });
+      const outcomes: unknown[] = [];
+      for (const presented of ['sk_first, sk_second', 'sk_ks1244-unknown']) {
+        const req = makeReq({ headers: { 'x-api-key': presented, authorization: 'Bearer ' + buildTestToken({ sub: 'u-ks1244', role: 'user' }) } });
+        const res = makeRes();
+        const next = vi.fn();
+        await authenticateToken(true)(req, res as any, next);
+        outcomes.push([presented, next.mock.calls.length, res._status, res._json]);
+      }
+      const refused = { success: false, error: { code: 'UNAUTHORIZED', message: 'Invalid API key' } };
+      expect(outcomes).toEqual([['sk_first, sk_second', 0, 401, refused], ['sk_ks1244-unknown', 0, 401, refused]]);
+    });
   });
```

`describe`, `it`, `expect`, `vi` are imported at `:6`; `authenticateToken` at `:12`; `makeReq` (`:24-:32`), `makeRes` (`:34-:48`, records `_status` and `_json`), `buildTestToken` (`:50-:53`) and `fetchMock` (`:67`, stubbed as the global `fetch`) are the file's own — you add NO import and NO file-scope constant. The cell's shape copies the KS-1244 cell above it (`:220-:234`): a loop, `outcomes.push`, one `toEqual` on the table. `fetchMock.mockResolvedValue` (not `Once`) because `validateApiKey` is called once per presented key; `apiKeyCache.clear()` and `fetchMock.mockReset()` run in the file's `beforeEach` (`:75-:84`), so neither key is cached when the cell starts. Nothing listens, nothing is fetched for real (the global `fetch` is the mock), no port, no database.

## Cells

- `refusalbody` = `RED KS-1244: an sk_ key that fails validation on a required mount is refused with the exact body 401 UNAUTHORIZED Invalid API key - a Node-joined pair and a single unknown key alike`

## Red cells

The cell below is a GENUINE assertion-red: it fails under the tamper declared for it and passes at the tip. It is declared here rather than with a red glyph in its title because every `+` line in this diff must be ASCII only.

- RED KS-1244: an sk_ key that fails validation on a required mount is refused with the exact body 401 UNAUTHORIZED Invalid API key - a Node-joined pair and a single unknown key alike

## Tampers

One single-line tamper on `middleware/auth.ts`, the gate's own row byte for byte (From = the tip's `:280`, To = the gate's `'nope'`). The `From` occurs EXACTLY ONCE in the file as a whole line (python whole-line scan: hits `[280]`; `Invalid API key` substring: `:280` only; positive control `res.status(401)`: 4 lines). The `To` is valid TypeScript (measured: the file loads and the whole suite runs under it). The checker plants it and restores the file by bytes.

### REFUSALMESSAGECHANGED — the API-key refusal's message becomes 'nope'
File: `Blockchain/Dev/services/api-gateway/src/middleware/auth.ts`
Line: 280
From:
```
      res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Invalid API key' } });
```
To:
```
      res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'nope' } });
```
Reds: `refusalbody`

## Controls

- `RED KS-1244: a repeated x-api-key (two individually valid keys joined by Node) on a required mount is refused 401 with no principal and no Bearer fall-through, in either order`
- `rejects with 401 when required=true and no token is present`
- `RED KS-1198: an sk_ key validated on the API-key path attaches the validated key metadata as req.connectorMeta, scopes intact, for the connector gates to read`

*(All three are FULL `it(...)` titles copied from the file at the tip — `:220`, `:156`, `:136` — unchanged by this hunk (the insertion is below all of them). For a VITEST suite the checker matches a declared cell by its FULL title, never by a prefix; no title is a prefix of another. Under REFUSALMESSAGECHANGED the KS-1244 cell stays green because it asserts `success` and `error.code` only — that is exactly the gap this brief closes, and it doubles as the proof that the tampered line still runs the refusal; the no-token control's `Authentication required` body comes from the Bearer path (`auth.ts`, a different line) and is untouched; the KS-1198 control never reaches `:280` (its key validates). The file's other cells are also green under the tamper but are left undeclared.)*

## THE CELL — state it to yourself before you write a line

At the untouched tip the cell passes: for each presented value, `authenticateToken(true)` reads `x-api-key`, sees the `sk_` prefix (`presentedKey` true), asks `validateApiKey`, which asks the mocked `fetch` and gets `{ data: { valid: false } }` → null; `presentedKey && !meta && required` is true, so `:280` answers `res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Invalid API key' } })` and returns before `next` and before the Bearer path — `[presented, 0, 401, refused]` twice (measured). Under **REFUSALMESSAGECHANGED** the same branch answers `message: 'nope'`: `toEqual` on the whole body fails for both rows — an assertion red on `refusalbody` alone (measured, file and whole suite). The KS-1244 cell above it stays green (it reads no message), as do the other two controls.

## Premises (measured — by reading the tip, NOT by running anything, except where the MEASURED section below says so)

- **Premise: the From line.** `auth.ts` at `7be81d5c9`, line 280 is `      res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Invalid API key' } });` (6-space indent), byte for byte; it occurs **once** as a whole line. The checker plants and restores it (T8 by sha256 after).
- **Premise: the gate's claim, re-derived.** `git grep -i -n 'invalid api key' <tip> -- services/api-gateway/src/__tests__` = ONE hit, `ks1207-a-failed-optional-api-key-falls-through-to-the-bearer-check.test.ts:181` — the phrase is in that control's TITLE only; its assertion is `[r.status, r.code, r.forwarded]` = `[401, 'UNAUTHORIZED', []]` (`:183`), no message. The KS-1244 cell at `:233` asserts `'UNAUTHORIZED'` and `false`, not the message. Positive control: `unauthorized` (case-insensitive) is in 6 test files. Agreed: the message is unpinned.
- **Premise: the anchor.** The test file is **309** lines; `:232`-`:235` are non-blank, `:233` is unique, `:235` is the `describe('authenticateToken')` close. The hunk is a pure insertion with three leading and one trailing context line — no blank line is asked of you anywhere.
- **Premise: `+` lines that also occur at the tip.** Three, unavoidable and added by this brief (so T4 accepts them): `      }`, `    });`, and `        const res = makeRes();` / `        const next = vi.fn();` (the KS-1244 cell has the same two lines). No `-` line anywhere, so nothing of the tip is removed.
- **No backslash** in any `+` line (0, counted). **No non-ASCII** in any `+` line (0, counted). **No template literal** in any `+` line (no backtick — `'Bearer ' + buildTestToken(...)` is string concatenation, as `:227` does). The title uses `-`, `:` and `_`.
- **Premise: the runner.** `services/api-gateway/package.json` at the tip has `"test": "vitest"`, no jest — the builder auto-detects vitest and the `Runner:` line agrees.
- **Premise: the surface.** Pure unit drive of the exported middleware with the file's fakes; the global `fetch` is `vi.fn()`; no server, no port, no database, no real key (the JWT beside the key is the file's `test_token_` shape and is never reached). GATEWAY authentication surface, test-only pin (allowed under Kam's scope rule; no product edit).

## Collision

`/usr/bin/grep -il '+++ b/.*api-gateway/src/__tests__/auth.test.ts' night/READY_*.md` = **2** of 253 READYs (KS-1244-JOINEDKEY-1, KS-1198-SKMETA-1) — and EVERY `+` line of both is already in the file at `7be81d5c9` (python: 15/15 and 9/9 present): they are MERGED (#1114), not banked. Positive control: the ks1234 file's `+++ b/` is in 4 READYs. No other brief of this round touches this file (row 1 is the ks1215 file; row 3 is originate). `middleware/auth.ts` is a tamper file in 6 READYs, all merged or on other lines. Sequencing needed: none.

## MEASURED by the writing seat (2026-09-21, `--shared` scratch clone at `7be81d5c9`, node_modules farmed from the source checkout via the harness's `prepare_clone.sh`, source tracked-modified count 0 before and after; artefacts under `2_Project_Files/local-model/runs/2026-09-21_gate1112rows-drafter-precheck/REFUSALMESSAGE/`)

- **Tip:** `ls-remote` at 08:51 = `7be81d5c9b109959b559e03652fb092c12de58e8`; measurement clone `m_gw2` HEAD = the tip; `prepare_clone.sh` rc 0 (`measure.log`).
- **From line:** `      res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Invalid API key' } });` whole-line hits `[280]`; `Invalid API key` substring lines `[280]`; positive control `res.status(401)` 4 lines.
- **File at the bare tip:** **18 passed / 0 failed of 18** (`file_tip_bare.json`). Golden hunk `git apply` rc 0 → file sha256 `7b7ff0bd76f6807d`; **file with hunk: 19 / 0 of 19** (`file_tip_applied.json`).
- **Whole api-gateway suite:** bare tip **688 / 0 of 688 in 70 files** (row 1's `whole_bare_tip.json`); with THIS hunk alone **689 / 0 of 689** (`whole_applied.json`); with this hunk AND row 1's ks1215 hunk **691 / 0 of 691** (`whole_both_gateway_hunks.json`).
- **Under REFUSALMESSAGECHANGED:** file **18 passed / 1 failed of 19** — the ONE red is `refusalbody` (`AssertionError: expected [ …(2) ] to deeply equal [ …(2) ]`; default reporter: both rows `"message": "nope"` received vs `"Invalid API key"` expected — `probe_auth_received.log`). Whole suite **688 / 1 of 689** — the same one cell, no other file red (the ks1207 control that NAMES the message in its title stays green: it asserts status/code/forwarded only). Restored by checkout: `auth.ts` sha256 `9abef1c21164bbbc` == tip blob, porcelain 0.
- **Controls under the tamper:** all three green (in the 18/19 above).
- **Golden and variants:** see the drafter report (`runs/2026-09-21_gate1112rows-drafter-precheck/REPORT.md`, Row 2) — `golden_runs.log`.

## Output

Exactly ONE ```diff block, nothing outside it: `--- a/Blockchain/Dev/services/api-gateway/src/__tests__/auth.test.ts` / `+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/auth.test.ts`, then the hunk above exactly as shown (`@@ -232,4 +232,17 @@`).

## Notes for the raise (not for the model)

- Test-only, zero product bytes. **Raise tier: TIER 1 at the gate (gateway authentication surface — allowed). Refs KS-1244** (and KS-1207 for the neighbouring comment). **NEVER Closes** — KS-1244's defect (the OPTIONAL-mount fall-through, row OPTIONALMOUNTJOINEDKEY) is BY DESIGN unpinned and stays open; this cell pins the REQUIRED-mount refusal's message.
- **From the #1112-#1118 batch gate's NOT-PINNED table** (report `2026-09-21_seatB-12th/gate/report.md:168`, row REFUSALMESSAGEUNPINNED). The gate proposed the joined-key drive alone asserting `error.message`; this brief drives the joined pair AND a single unknown key and asserts the WHOLE body (`toEqual`), which also pins `success: false` and that no extra field is added — a superset of the gate's cell.
- **Said plainly:** the cell asserts wording. That is the point (integrators read it; the neighbours `:165`/`:201` pin theirs), and the cost is one deliberate rewrite if the wording is ever changed on purpose.

## Build line (not for the model)

```
bash tasks/test_only/build_test_only_input.sh KS-1244 night/inputs/test_only_1244REFUSALMESSAGE-1.json night/briefs/KS-1244-REFUSALMESSAGE-1.md tip=7be81d5c9b109959b559e03652fb092c12de58e8 ctx=65536
```
