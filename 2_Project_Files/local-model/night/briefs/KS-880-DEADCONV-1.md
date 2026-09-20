# KS-880 DEADCONV-1 PIN THAT THE DEAD converters.ts rowToApiKey MAPS NEITHER tenantId NOR connectorId (a row carrying both columns comes back without either key) — Wednesday's task for Ornith, TEST_ONLY, **ONE existing test file, one hunk, one cell added, no product file** (written 23:35 on 2026-09-20, widened sweep round 25)

File: `Blockchain/Dev/services/security/src/__tests__/row-converters.test.ts`
Tip: `dc061f2bb6dff9180a0724b1d1d5c50b9a0173fa`
Runner: `vitest`

Written from develop `dc061f2bb6dff9180a0724b1d1d5c50b9a0173fa` (`git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" ls-remote origin refs/heads/develop` at 23:32 on 2026-09-20, read verbs only; the #1101 merge, 2026-09-20 17:53:42 +1000). The test file at that tip is **154 lines**, read whole; its full content is in `files[...]` of your input. The product the cell pins is `Blockchain/Dev/services/security/src/converters.ts` (**138 lines**, read whole): the `ApiKey` interface at `:43-58` (`connectorId?: string` at `:57`, NO `tenantId` member), `rowToApiKey` at `:122-138`. This service runs **VITEST**.

## THE MODE — read this twice

**TEST_ONLY.** Your diff touches EXACTLY ONE file: the test file above, MODIFIED IN PLACE (`--- a/<path>` / `+++ b/<path>`, the path exactly as written above). You never touch `converters.ts`, `index.ts` or any other product file: the behaviour is already what it is at the tip, and this cell PINS it.

## What the cell pins (one paragraph)

KS-880 reports that `services/security/src/converters.ts:122` holds a SECOND `rowToApiKey` — imported by nothing in production (its only importer at the tip is this test file, `:13`; production uses the copy at `index.ts:418`, called from `index.ts:347`, `:473`, `:1306`) — and that the dead copy has diverged from the live one: the live copy maps `tenantId` (the RLS tenancy field) and `connectorId` (KS-869); the dead copy maps NEITHER. The ticket's own two dispositions are "quarantine by rename" or "reconcile `index.ts` onto `converters.ts`", and it names the trap precisely: the dead copy "carries a passing test, which is exactly what would make a future reader trust it". Today that passing test (`:137`) asserts scopes, rate limits, usage count, `isActive` and `lastUsedAt` — the words `tenant`, `connector` and `KS-880` occur **0** times in the file. This change adds ONE cell that feeds the dead converter a row carrying BOTH `tenant_id` and `connector_id` and asserts that the returned object has NEITHER key (`'tenantId' in k` and `'connectorId' in k` both `false`), with `organizationId` beside them as the liveness element (`'org_1'`, the one field the dead copy does map). Every existing cell is unchanged. **It pins TODAY's behaviour and decides nothing about KS-880** — whichever disposition the owners take, the reconcile route (adding the two fields to `converters.ts`) now arrives as a deliberate red in this suite instead of a silent green, and the quarantine route removes the file and this cell together. The cell's title says "dead copy" so no future reader mistakes it for an endorsement.

## The exact change — ONE hunk in the test file

The new cell goes at the end of the `describe('rowToApiKey()', ...)` block opened at `:136`, directly above that block's closing line `});` (`:154`, the file's LAST line and the ONE trailing context line). There is NO leading context: the line above (`:153`, `  });`) stays and is not written. Copy every line byte for byte. Every `+` line is ASCII only. There is no blank line anywhere in the fence. Keep the header exactly as shown. **Your diff MUST begin with the two file-header lines, above the `@@` line: `--- a/Blockchain/Dev/services/security/src/__tests__/row-converters.test.ts` then `+++ b/Blockchain/Dev/services/security/src/__tests__/row-converters.test.ts`.**

```
@@ -154,1 +154,11 @@
+  it('RED KS-880: the dead converters.ts rowToApiKey maps NEITHER tenantId NOR connectorId - a row carrying both columns comes back without either key', () => {
+    const row = {
+      id: 'key_2', organization_id: 'org_1', tenant_id: 'a0000000-0000-4000-8000-000000000002', connector_id: 'conn_1',
+      name: 'connector-2', key_hash: 'h', key_prefix: 'sk_t_', scopes: '["read:docs"]',
+      rate_limit: '100', rate_limit_window: '60', last_used_at: null, usage_count: '0', is_active: true,
+      expires_at: null, created_at: '2026-04-01T00:00:00Z',
+    };
+    const k = rowToApiKey(row);
+    expect([k.organizationId, 'tenantId' in k, 'connectorId' in k]).toEqual(['org_1', false, false]);
+  });
 });
```

`rowToApiKey` is already imported by the file at `:12` (the `import { ... } from '../converters';` at `:7-13`) — you add NO import. The cell needs no mock, no app boot, no port and no database: `rowToApiKey` is a pure function over a plain object, and the file has no `vi.mock`, no `beforeEach` and no setup of its own beyond the `stubDecrypt` at `:17` (not used by this cell).

## Cells

- `deadmapsneither` = `RED KS-880: the dead converters.ts rowToApiKey maps NEITHER tenantId NOR connectorId - a row carrying both columns comes back without either key`

## Red cells

The cell below is a GENUINE assertion-red: it fails under each tamper and passes at the tip. It is declared here rather than with a red glyph in its title because every `+` line in this diff must be ASCII only.

- RED KS-880: the dead converters.ts rowToApiKey maps NEITHER tenantId NOR connectorId - a row carrying both columns comes back without either key

## Tampers

Two single-line tampers on two DIFFERENT lines of `converters.ts`. They are the two halves of the ticket's "reconcile" shape landing in the dead copy: the tenancy field, and the connector field. Each `From` is the tip's line at that number, byte for byte, and each `To` is valid JavaScript that loads under vitest (esbuild strips types; `service/tsconfig.json` excludes `src/__tests__` and no gate runs tsc on a tampered tree), so nothing fails to load and no cell reds for the wrong reason. Each `From` line occurs EXACTLY ONCE in the file (counted with `grep -c -F -x`; the `createdAt:` line at `:136` was NOT chosen because it occurs 3 times, at `:102`, `:118`, `:136`).

### TENANTMAPPED — the dead copy starts mapping tenant_id to tenantId
File: `Blockchain/Dev/services/security/src/converters.ts`
Line: 125
From:
```
    organizationId: r.organization_id as string,
```
To:
```
    organizationId: r.organization_id as string, tenantId: r.tenant_id as string,
```
Reds: `deadmapsneither`

### CONNECTORMAPPED — the dead copy starts mapping connector_id to connectorId (the live copy's KS-869 line)
File: `Blockchain/Dev/services/security/src/converters.ts`
Line: 135
From:
```
    expiresAt: r.expires_at ? new Date(r.expires_at as string) : undefined,
```
To:
```
    expiresAt: r.expires_at ? new Date(r.expires_at as string) : undefined, connectorId: (r.connector_id as string | null) ?? undefined,
```
Reds: `deadmapsneither`

## Controls

- `maps key fields and parses scopes array`
- `maps event fields and parses details JSON`

*(Both are FULL `it(...)` titles, copied byte for byte from the file at the tip — `:137` and `:119` — each occurs exactly once in the file and neither is a prefix of any other title. For a VITEST suite the checker matches a declared cell by its FULL title, never by a prefix; the prefix rule in `build_test_only_input.sh`'s header is for BASH suites only (the KS-1275 round-1 FAIL, 2026-09-20). The file's other eleven cells are also green under both tampers but are left undeclared. The `:137` control is the strongest liveness proof in the file: it drives the SAME `rowToApiKey` object literal that both tampers mutate, and stays green under both because it asserts only `scopes`, `rateLimit`, `rateLimitWindow`, `usageCount`, `isActive` and `lastUsedAt` — an extra key on the returned object changes none of them.)*

## THE CELLS — state it to yourself before you write a line

At the untouched tip the new cell passes: the object literal at `:123-137` has thirteen properties and none of them is `tenantId` or `connectorId` (the words `tenantId`/`tenant_id` and `connectorId`/`connector_id` occur in `converters.ts` only at `:13`, `:57`, `:89` — the AuditLog interface, the ApiKey interface's optional member, and `rowToAuditLog`), so `'tenantId' in k` and `'connectorId' in k` are both `false`, and `organizationId` is `r.organization_id as string` = `'org_1'`, which is exactly the triple the cell asserts.

Under **TENANTMAPPED** the returned object gains a `tenantId` key (`'a0000000-0000-4000-8000-000000000002'`), so `'tenantId' in k` is `true` and the triple is `['org_1', true, false]` — assertion red. Under **CONNECTORMAPPED** the returned object gains a `connectorId` key (`'conn_1'`), so the triple is `['org_1', false, true]` — assertion red. Under BOTH, every existing cell stays green: `:26-65` never touch `rowToApiKey`; `:71` and `:102` drive `rowToAuditLog`; `:119` drives `rowToSecurityEvent`; `:137` drives `rowToApiKey` but asserts six fields the tampers do not touch.

## Premises (measured — by reading the tip, NOT by running anything)

- **Premise: the two `From` lines.** `converters.ts` at `dc061f2bb`, line 125 is `    organizationId: r.organization_id as string,` and line 135 is `    expiresAt: r.expires_at ? new Date(r.expires_at as string) : undefined,`, byte for byte; each occurs **exactly once** in the file (`grep -c -F -x`, 1 each).
- **Premise: the anchor.** The test file is **154** lines; `:154` is `});` (column 0, the file's last line, one of five column-0 `});` at `:45`, `:68`, `:116`, `:134`, `:154` — the hunk header's `-154` is what locates it) and `:153` is `  });`. The trailing context line is non-blank and the insertion is pure, so no blank line is asked of you anywhere.
- **Premise: nothing pins this today.** `KS-880`, `tenant`, `connector_id` and `connectorId` occur **0** times in the test file at the tip (`grep -c -i`; control: `rowToApiKey` occurs 3 times).
- **Premise: the ticket's claims hold at the tip, with moved line numbers.** The live copy is at `index.ts:418` (the ticket said `:309`), maps `tenantId` at `index.ts:424` and `connectorId` at `index.ts:439`; production calls it at `index.ts:347`, `:473`, `:1306` (the ticket said `:253`, `:379`, `:1162`). `git grep` for `from '../converters'` / `from './converters'` at the tip over `services/security/` returns exactly ONE file: this test file.
- **Premise: no `+` line re-adds a tip line.** The only `+` line that also occurs at the tip is the closing `  });` (unavoidable for a new cell). `    };` also occurs at the tip (`:103`, `:119`, `:137` and inside `:87`/`:109`/`:126`/`:145` of the test) but is not a `-` line of this fence, so the builder's context-marked-as-addition check does not fire.
- **No backslash** in any `+` line (0, counted). **No non-ASCII** in any `+` line (0, counted). The title uses `-`, not an em dash. (The file's own non-ASCII is at `:2`, `:15`, `:94` — comments, untouched.)
- **Premise: the runner.** `security/package.json` at the tip has `"test": "vitest run"` and `vitest ^4.1.11` in devDependencies, with no `jest` / `ts-jest` — the builder auto-detects vitest and the `Runner:` line above agrees with it. `vitest.config.ts` sets `globals: true`, `environment: 'node'`, no `setupFiles`, no `include` narrowing.
- **Premise: no live-lane collision.** `converters.ts` is not `enforcement.ts`, `startup-migrations.ts`, `index.ts` or `trustHeaders.ts`, and is not under `services/anchoring/**`. `grep -l -i 'converters\.ts|row-converters|KS-880'` over the 225 held `READY_*` files returns **0** (control: `trustHeaders` returns 1). `git log` on `converters.ts` + the test file at the tip shows two commits (T2-D, KS-28); no remote branch names 880 or converters (`refs/pull/880/head` is PR #880, unrelated).
- **Premise: the surface.** `converters.ts` is a dead pure-mapper module. The cell constructs no user, no token, no session and no MFA state; it calls one pure function with a plain object. Zero product bytes. `candidates.md:231` parked KS-880 as "two-file refactor (Claude seat)" — that is the code_patch tier's verdict on the ticket's FIX and stands; this brief is the test-only PIN beside it, not the fix.
- **Premise: the ticket's third divergence is NOT pinned.** `organizationId` nullability (`as string` vs `?? null`) is out of this cell's scope on purpose: `'org_1'` is the liveness element, and the tampers never touch `:125`'s left-hand semantics beyond appending a property.

## MEASURED by the writing seat (see the run directory named below; filled after the checker runs)

- See `2_Project_Files/local-model/runs/2026-09-20_ks880DEADCONV-1-drafter-precheck/` (checker.log, patch.diff, var1/, var2/, full_suite.log, tip_suite.log, tsc.log) — the report accompanying this brief carries the numbers.

## Output

Exactly ONE ```diff block, nothing outside it: `--- a/Blockchain/Dev/services/security/src/__tests__/row-converters.test.ts` / `+++ b/Blockchain/Dev/services/security/src/__tests__/row-converters.test.ts`, then the hunk above exactly as shown (`@@ -154,1 +154,11 @@`).

## Notes for the raise (not for the model)

- Test-only, zero product bytes. **Raise tier: TIER 2. Refs KS-880** (and KS-869, whose finding the missing `connectorId` is; KS-28/KS-33 for `tenantId`). **NEVER Closes** — KS-880's acceptance is "exactly one `rowToApiKey` reachable from production"; this brief takes no part of that decision and leaves the dead copy where it is.
- **Not from a gate cell.** Found by the 2026-09-20 widened test-only sweep of the KS Backlog/Todo; the ticket's load-bearing premise (the dead copy maps neither field, with a green test on it) is provably invisible to the suite today.
- **Collision: none.** No held `READY_*` carries a hunk in the test file or in `converters.ts`.
- **Ticket tension, said plainly:** KS-880 does not ask for more tests on the dead copy — it asks for the copy to be quarantined or reconciled. This cell is a characterisation pin whose title names the copy as dead; the reviewer should read it as "the divergence is now visible to the suite", not as "the dead copy is endorsed". If the owners prefer NOT to touch the test file until the disposition is chosen, hold this READY rather than raise it.

## Build line (not for the model)

```
bash tasks/test_only/build_test_only_input.sh KS-880 night/inputs/test_only_880DEADCONV-1.json night/briefs/KS-880-DEADCONV-1.md ctx=65536
```
