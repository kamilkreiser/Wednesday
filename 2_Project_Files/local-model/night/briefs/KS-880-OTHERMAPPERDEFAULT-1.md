# KS-880 OTHERMAPPERDEFAULT-1 PIN THAT THE LIVE index.ts rowToAuditLog — THE OTHER MAPPER THAT CARRIES THE SAME DEFAULT-TENANT LINE — ANSWERS THE DEFAULT TENANT FOR A ROW WHOSE tenant_id IS MISSING, NULL OR EMPTY, AND PASSES A STORED tenant_id THROUGH — the twin of the merged rowToApiKey cell, driven in process with the file's own opt-in boot guard — Wednesday's task for Ornith, TEST_ONLY, **ONE existing test file, one hunk, one cell added, no product file** (written 2026-09-21 15:4x after the #1119-#1128 batch gate; its NOT-PINNED row OTHERMAPPERDEFAULT, #1124 / KS-880, measured 0 red of 215 at the head)

File: `Blockchain/Dev/services/security/src/__tests__/ks869-connector-id-persisted.test.ts`
Tip: `9f0265eb06ecf24d4de18149ce862ad2330a61ee`
Runner: `vitest`

Written from develop `9f0265eb06ecf24d4de18149ce862ad2330a61ee` (`git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" ls-remote origin refs/heads/develop` at 15:30 on 2026-09-21, read verbs only; the tree `23d60cace7c3` that carries the ten #1119-#1128 squashes, #1124 = KS-880 LIVETENANTDEFAULT-1 included). The test file at that tip is **113 lines** (blob `f452db039b9d`), read whole; its full content is in `files[...]` of your input. The product the cell pins is `Blockchain/Dev/services/security/src/index.ts` (blob `0903ce4380f2`, **1597 lines**, read whole around the converters): `export function rowToAuditLog(` at `:374-:400` — the KS-28 comment `:378-:382`, then **`:383`** `    tenantId: (r.tenant_id as string) || 'a0000000-0000-4000-8000-000000000001',` and **`:384`** `    userId: (r.user_id as string) || undefined,`; `rowToApiKey` at `:418-:436` carries the SAME `tenantId:` line at `:424` (followed by `name: r.name as string,`), which #1124 pinned. `decryptDetails` (`:55-:73`) answers `null` for a missing or empty `details`, and `:393` turns that into `{}`. The boot guard `if (process.env.SECURITY_DISABLE_BOOT !== '1')` is at `:1566`. This service runs **VITEST** (`package.json` `"test": "vitest run"`, vitest `^4.1.11`; no jest).

## THE MODE — read this twice

**TEST_ONLY.** Your diff touches EXACTLY ONE file: the test file above, MODIFIED IN PLACE (`--- a/<path>` / `+++ b/<path>`, the path exactly as written above). You never touch `index.ts` or any other product file: the behaviour is already what it is at the tip, and this cell PINS it.

## What the cell pins (one paragraph)

#1124 (KS-880 LIVETENANTDEFAULT-1) added the cell at `:104-:112` of this file: `rowToApiKey` answers the default tenant `a0000000-0000-4000-8000-000000000001` for a key row whose `tenant_id` is missing, `null` or `''`, and passes a stored `'t9'` through. The gate that merged it planted the SAME default dropped from the OTHER mapper — `rowToAuditLog`, `:383` — located by its function anchor as a two-line block with the `userId` line, and measured **0 red of 215**: the audit-log mapper's belt-and-braces default (the KS-28 comment: "a hand-edited row that somehow lost the column") has no pin, while its twin now does. This change adds ONE cell, directly under the KS-880 cell and inside the same `describe`, that imports `rowToAuditLog` from the already-loaded module (the file's `beforeAll` set `SECURITY_DISABLE_BOOT = '1'` and imported `../index` once; a second `await import('../index')` returns that cached module — nothing boots, nothing listens), builds a minimal audit row (`id`, `action`, `resource_type`, `success`, `created_at`; no `details`, which `decryptDetails` turns into `null` → `{}`) and asserts in ONE `toEqual` the same four-way table as the rowToApiKey cell: `[DEFAULT_TENANT, DEFAULT_TENANT, DEFAULT_TENANT, 't9']` for `tenant_id` missing, `null`, `''`, `'t9'`. **It pins TODAY's default** — whether a row with NO tenant should answer the default tenant at all is the ticket's BY-DESIGN question (the gate's DEFAULTTENANTBYDESIGN row) and is NOT decided here; if the owners ever remove the fallback on purpose, the cell goes red on purpose and is rewritten.

**Why THIS file and not a new `ks880-audit-log-default-tenant.test.ts`** (the gate offered either): the merged rowToApiKey cell lives here (`:104-:112`), the file already carries the opt-in boot guard and the dynamic import that make the live `index.ts` importable in process (`:42-:47`), and the new cell is the twin of `:104-:112` line for line — one file, two mappers, the same table. A new file would duplicate the guard and the import for one cell.

## The exact change — ONE hunk in the test file

The cell goes at the END of `describe('KS-869 — connector_id is persisted and read back', …)`: after `:112` (`  });`, the close of the KS-880 rowToApiKey cell) and before `:113` (`});`, the close of the describe — the file's last line). `  });` occurs SEVEN times and `});` twice (`:47`, `:113`), so the hunk carries THREE leading context lines — `:110` (`    const DEFAULT_TENANT = 'a0000000-0000-4000-8000-000000000001';`, **unique in the file**), `:111` (the KS-880 `expect([rowToApiKey(…` line, **unique**) and `:112` (`  });`) — and ONE trailing context line (`:113`). Copy every line byte for byte. Every `+` line is ASCII only (the title uses `RED KS-880:` and plain hyphens, never a glyph or an em dash — the file's own KS-880 cell at `:104` has the same shape). There is no blank line anywhere in the fence. Keep the header exactly as shown. **Your diff MUST begin with the two file-header lines, above the `@@` line: `--- a/Blockchain/Dev/services/security/src/__tests__/ks869-connector-id-persisted.test.ts` then `+++ b/Blockchain/Dev/services/security/src/__tests__/ks869-connector-id-persisted.test.ts`.**

```
@@ -110,4 +110,12 @@
     const DEFAULT_TENANT = 'a0000000-0000-4000-8000-000000000001';
     expect([rowToApiKey({ ...base }).tenantId, rowToApiKey({ ...base, tenant_id: null }).tenantId, rowToApiKey({ ...base, tenant_id: '' }).tenantId, rowToApiKey({ ...base, tenant_id: 't9' }).tenantId]).toEqual([DEFAULT_TENANT, DEFAULT_TENANT, DEFAULT_TENANT, 't9']);
   });
+  it('RED KS-880: rowToAuditLog answers the default tenant for a row whose tenant_id is missing, null or empty, and passes a stored tenant_id through', async () => {
+    const { rowToAuditLog } = await import('../index');
+    const base = {
+      id: 'a1', action: 'login', resource_type: 'user', success: true, created_at: new Date().toISOString(),
+    };
+    const DEFAULT_TENANT = 'a0000000-0000-4000-8000-000000000001';
+    expect([rowToAuditLog({ ...base }).tenantId, rowToAuditLog({ ...base, tenant_id: null }).tenantId, rowToAuditLog({ ...base, tenant_id: '' }).tenantId, rowToAuditLog({ ...base, tenant_id: 't9' }).tenantId]).toEqual([DEFAULT_TENANT, DEFAULT_TENANT, DEFAULT_TENANT, 't9']);
+  });
 });
```

`describe`, `it`, `expect`, `beforeAll` are imported at `:26`; `rowToApiKey` is the file-scope binding filled by `beforeAll` (`:40`, `:46`) — you add NO import line, NO file-scope binding, and you do NOT touch `:40` or `:46`: the cell takes `rowToAuditLog` from `await import('../index')` inside its own body (an `async` arrow, as `beforeAll`'s is), which is the SAME cached module. The cell's shape copies the KS-880 cell above it (`:104-:112`): a `base`, a `DEFAULT_TENANT`, one `toEqual` on the four-entry table. `base` carries only what `rowToAuditLog` reads without a fallback (`id`, `action`, `resource_type`, `success`, `created_at`); every other column has an `|| undefined` / `? … :` guard and `details` goes through `decryptDetails(undefined, id)` → `null` → `{}`. Nothing listens, nothing is fetched, no port, no database.

## Cells

- `auditdefault` = `RED KS-880: rowToAuditLog answers the default tenant for a row whose tenant_id is missing, null or empty, and passes a stored tenant_id through`

## Red cells

The cell below is a GENUINE assertion-red: it fails under the tamper declared for it and passes at the tip. It is declared here rather than with a red glyph in its title because every `+` line in this diff must be ASCII only.

- RED KS-880: rowToAuditLog answers the default tenant for a row whose tenant_id is missing, null or empty, and passes a stored tenant_id through

## Tampers

ONE tamper, a BLOCK tamper (the harness's 2026-09-19 shape) on `index.ts:383-:384`, because the `:383` line ALONE is NOT unique in the file: as a whole line it occurs at `:383` (inside `rowToAuditLog`) and `:424` (inside `rowToApiKey`) — python whole-line scan hits `[383, 424]`. The two-line From block — `:383` followed by `:384` `    userId: (r.user_id as string) || undefined,` (itself at `[384, 408]`, the second inside `rowToSecurityEvent` after a different line) — occurs **exactly once** as consecutive whole lines (hits `[383]`; the gate's row says the same: "the two-line block … is ×1 in the file — the first line alone is ×2"). Positive control: `tenantid` (case-insensitive) is on 55 lines of the file. It is the gate's OTHERMAPPERDEFAULT: the fallback removed from `rowToAuditLog`, the raw column handed through. `From` is the tip's two lines at those numbers, byte for byte; `To` is the same two lines with the `|| '...'` gone from the first (valid TypeScript — `r.tenant_id as string` is a `string`-typed expression, so `AuditLog.tenantId: string` still type-checks and vitest's esbuild transform loads the file; measured: the whole suite runs under it). The checker plants it as whole lines and restores the file by bytes. The merged rowToApiKey cell (`:104`) stays GREEN under it — its mapper's `:424` is untouched — which is exactly the gap this brief closes.

### AUDITTENANTRAW — the live rowToAuditLog's default-tenant fallback removed, the raw tenant_id column handed through
File: `Blockchain/Dev/services/security/src/index.ts`
Line: 383
From:
```
    tenantId: (r.tenant_id as string) || 'a0000000-0000-4000-8000-000000000001',
    userId: (r.user_id as string) || undefined,
```
To:
```
    tenantId: (r.tenant_id as string),
    userId: (r.user_id as string) || undefined,
```
Reds: `auditdefault`

## Controls

- `RED KS-880: rowToApiKey answers the default tenant for a row whose tenant_id is missing, null or empty, and passes a stored tenant_id through`
- `CONTROL — the mapper is importable and maps a row at all, or every cell below is vacuous`
- `🔴 READ half — a row with no connector_id yields undefined, not the string "null"`

*(All three are FULL `it(...)` titles copied from the file at the tip — `:104`, `:50`, `:70` — unchanged by this hunk (the insertion is below all of them). For a VITEST suite the checker matches a declared cell by its FULL title, never by a prefix; no title is a prefix of another, and the new title differs from the KS-880 control's in its mapper name (`rowToAuditLog` vs `rowToApiKey`). Under AUDITTENANTRAW the KS-880 rowToApiKey cell stays green because `:424` is not the tampered line — that is the gap this brief closes, and it doubles as the proof that the tampered module still loads and maps; the two KS-869 controls read `rowToApiKey` only. The file's other cells are also green under the tamper but are left undeclared.)*

## THE CELL — state it to yourself before you write a line

At the untouched tip the cell passes: `rowToAuditLog({ ...base })` finds `r.tenant_id` undefined, `:383`'s `||` answers the default; `null` and `''` are falsy and answer the default the same way; `'t9'` is truthy and is handed through — `[DEFAULT_TENANT, DEFAULT_TENANT, DEFAULT_TENANT, 't9']` (measured). Under **AUDITTENANTRAW** the same calls answer `[undefined, null, '', 't9']`: `toEqual` fails — an assertion red on `auditdefault` alone (measured, file and whole suite). The KS-880 rowToApiKey control above it stays green (`:424` untouched), as do the two KS-869 controls.

## Premises (measured — by reading the tip, NOT by running anything, except where the MEASURED section below says so)

- **Premise: the From block.** `index.ts` at `9f0265eb0`, `:383` + `:384` as consecutive whole lines occur **once** (hits `[383]`); `:383` alone `[383, 424]`; `:384` alone `[384, 408]`. The checker plants and restores it (T8 by sha256 after).
- **Premise: the gate's claim, re-derived.** `git grep -n 'rowToAuditLog' <tip> -- Blockchain/Dev/services/security/src/__tests__` = **4** lines, ALL in `row-converters.test.ts` (`:10`, `:70`, `:88`, `:110`), which imports from `../converters` — the DEAD `converters.ts` copy of the mappers (its `rowToAuditLog(row, decrypt)` takes a decryptor argument and carries NO default-tenant line; the merged KS-880 brief drew the same distinction). No test line names `rowToAuditLog` together with `'../index'` (0 hits; positive control: `rowToApiKey` is on 14 lines in 2 files, and `'../index'` is imported in 11 test files). Agreed: the LIVE mapper's default is undriven.
- **Premise: the anchor.** The test file is **113** lines; `:110`-`:113` are non-blank; `:110` and `:111` are unique; `:113` is the describe's close and the file's last line (the other `});` is `:47`, the `beforeAll` close). The hunk is a pure insertion with three leading and one trailing context line — no blank line is asked of you anywhere.
- **Premise: `+` lines that also occur at the tip.** Four, unavoidable and added by this brief (so T4 accepts them): `    const base = {`, `    };`, `    const DEFAULT_TENANT = 'a0000000-0000-4000-8000-000000000001';` (the KS-880 cell declares its own, block-scoped, at `:110`) and `  });`. No `-` line anywhere, so nothing of the tip is removed.
- **No backslash** in any `+` line (0, counted). **No non-ASCII** in any `+` line (0, counted). **No template literal** in any `+` line (no backtick). Longest `+` line 274 bytes (the `expect` table; the file's own `:111` is the same shape and length).
- **Premise: the runner.** `services/security/package.json` at the tip has `"test": "vitest run"` and `vitest ^4.1.11`, no jest — the builder auto-detects vitest and the `Runner:` line agrees.
- **Premise: the surface.** Pure unit drive of an exported row mapper with the file's opt-in boot guard; no server, no port, no database (`SECURITY_DISABLE_BOOT=1` is set by the file's `beforeAll` before the first import). SECURITY service, test-only pin (allowed under Kam's scope rule; no product edit).

## Collision

`/usr/bin/grep -il 'ks869-connector-id-persisted' night/READY_*.md` = **2** of 259. (1) KS-880-LIVETENANTDEFAULT-1 — MERGED as #1124 (its 9 `+` lines are all in the tip file, python-checked). (2) **`READY_KS-887_…_2026-09-16` — HELD, NOT merged** (0 of its 5 `+` lines at the tip): it tightens the WRITE-half cell at `:84-:90` (`@@ -84,7 +84,11 @@`, four lines added ABOVE this hunk's anchor). Measured on fresh clones (`OTHERMAPPERDEFAULT/collision.log`): both apply orders rc 0, ONE sha256 `7a1e03c90c603eed` over the file (125 lines), and the file with BOTH hunks **8 passed / 0 failed**. No textual overlap. **Sequencing note for Wednesday:** if KS-887 merges BEFORE this brief is queued, the tip's `:110-:113` become `:114-:117` and the builder will refuse this fence's header (`@@ -110,4`) — a one-number re-anchor, nothing else changes. Security `index.ts` is a tamper file in the KS-880-LIVETENANTDEFAULT-1 READY (merged as #1124; `:424`, a different line). No other brief of this round touches the security service (row 2 is the trivy suite; row 3 is `systemTest/`). Sequencing needed: none.

## MEASURED by the writing seat (2026-09-21, `--shared` scratch clone at `9f0265eb0`, node_modules farmed from the source checkout via the harness's `prepare_clone.sh`, source tracked-modified count 0 before and after; artefacts under `2_Project_Files/local-model/runs/2026-09-21_gate1119rows-drafter-precheck/OTHERMAPPERDEFAULT/`)

- **Tip:** `ls-remote` at 15:30 = `9f0265eb06ecf24d4de18149ce862ad2330a61ee`; measurement clone `m_sec` HEAD = the tip; `prepare_clone.sh` rc 0 (`measure.log`, `prepare.measure.log`).
- **From block:** `:383`+`:384` as consecutive whole lines: hits `[383]` (the input's block tamper planted by the same scan); `:383` alone `[383, 424]`; `:384` alone `[384, 408]`; `tenantid` (ci) 55 lines.
- **File at the bare tip:** **7 passed / 0 failed of 7** (`file_tip_bare.json`). Golden hunk `git apply` rc 0 → 113 → 121 lines, sha256 `1d152fe592c8f5d5`; **file with hunk: 8 / 0 of 8** (`file_tip_applied.json`).
- **Whole security suite:** bare tip **215 / 0 of 215 in 17 files** (`whole_bare_tip.json` — the gate's 215); with THIS hunk **216 / 0 of 216** (`whole_applied.json`).
- **Under AUDITTENANTRAW:** file **7 passed / 1 failed of 8** — the ONE red is `auditdefault` (`AssertionError: expected [ undefined, null, '', 't9' ] to deeply equal [ …(4) ]` — the raw column handed through, as predicted). Whole suite **215 / 1 of 216** — the same one cell, no other file red (the KS-880 rowToApiKey cell stays green: `:424` untouched). Restored by checkout: `index.ts` sha256 `ef4d361fa7042928` == tip blob, porcelain 0.
- **Controls under the tamper:** all three green (in the 7/8 above).
- **Golden and variants:** see the drafter report (`runs/2026-09-21_gate1119rows-drafter-precheck/REPORT.md`, Row 1) — `golden_runs.log`.

## Output

Exactly ONE ```diff block, nothing outside it: `--- a/Blockchain/Dev/services/security/src/__tests__/ks869-connector-id-persisted.test.ts` / `+++ b/Blockchain/Dev/services/security/src/__tests__/ks869-connector-id-persisted.test.ts`, then the hunk above exactly as shown (`@@ -110,4 +110,12 @@`).

## Notes for the raise (not for the model)

- Test-only, zero product bytes. **Raise tier: TIER 1 at the gate (security service — allowed as a test-only pin). Refs KS-880** (and KS-28 for the comment the default sits under). **NEVER Closes** — KS-880's question (whether a row with NO tenant should answer the default tenant at all, DEFAULTTENANTBYDESIGN) is BY DESIGN unpinned and stays open; KS-887's WRITE-half fix is a separate, later PR.
- **From the #1119-#1128 batch gate's NOT-PINNED table** (`Testing Agent MAIN/projects/secuura/reports/2026-09-21-batch1119-1128-tier1-r1/report.md`, row OTHERMAPPERDEFAULT). The gate's proposed cell title and table are used verbatim with a `RED KS-880:` prefix; the gate's `details` suggestion (an empty string or `{}`) is met by omitting `details` (same `decryptDetails` path: `null` → `{}`).
- **Said plainly:** the cell asserts a fallback the ticket questions. That is the point of a pin: the fallback is live today in BOTH mappers, and now both are red-proofed; the ticket's decision, when made, rewrites two cells instead of silently changing one mapper.

## Build line (not for the model)

```
bash tasks/test_only/build_test_only_input.sh KS-880 night/inputs/test_only_880OTHERMAPPERDEFAULT-1.json night/briefs/KS-880-OTHERMAPPERDEFAULT-1.md tip=9f0265eb06ecf24d4de18149ce862ad2330a61ee ctx=65536
```
