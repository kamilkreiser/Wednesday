# B22-08 sites-panel-sample-tag — the Sites & devices panel stops calling a user-added customer's empty figures "Sample data"

File: `web/src/components/customer/EngagementOverview.tsx`
File: `web/src/components/customer/EngagementOverview.test.tsx`
Tip: `99483e47cf050c1de125c9805df7e46e878b4702`
Runner: `vitest`

Written 2026-09-26 09:59 AEST from the SHA above, both files read whole (`web/src/components/customer/EngagementOverview.tsx` 247 lines, `web/src/components/customer/EngagementOverview.test.tsx` 154 lines).

## The mode — read this twice

CODE+TEST. Your diff touches EXACTLY 2 files, both on the File: lines, modified in place: `web/src/components/customer/EngagementOverview.tsx` (one line) and `web/src/components/customer/EngagementOverview.test.tsx` (one inserted test). You never touch `web/src/components/customer/parts.tsx`, `web/src/components/customer/content.ts`, `web/src/components/ui/Tag.tsx`, or any other file.

## What is wrong (one paragraph)

In `EngagementOverview.tsx` line 91 the component already computes `const x = extrasFor(customer.apiId, customer.name);` — the "sample extras" that only the seeded sample customers have (a customer the user adds live gets `null`). PR #28 used `x` to fix the page header (line 113: `{x && <SyntheticTag />}`). The Sites & devices panel at line 144 was missed: `tags={factsRecorded ? undefined : <SampleTag />}` shows the `SampleTag` (literal text "Sample data", `parts.tsx:13-15`) whenever the user has not recorded sites or printers, even for a user-added customer whose panel then reads only "Not recorded" (lines 148, 152, 160) and whose footnote already says no sample applies (line 168). A panel with no sample values must not carry a "Sample data" tag. The fix adds `|| !x` so the tag shows only when the figures really are sample extras. Seeded samples (x present, no facts recorded) keep the tag — the existing test at line 50 asserts that and must stay green.

## The exact change

2 edit points. Line numbers are the line numbers AT THE TIP, before any edit. Your hunk headers must use them.

Edit 1 — `web/src/components/customer/EngagementOverview.tsx` line 144, replacement.
Context: line 143 is an EMPTY line, line 145 is `          <ul className="flex flex-col gap-3">` — copy both as context, byte-exact from the file.

```
-        <Panel title="Sites & devices" id="sites-title" tags={factsRecorded ? undefined : <SampleTag />}>
+        <Panel title="Sites & devices" id="sites-title" tags={factsRecorded || !x ? undefined : <SampleTag />}>
```

Edit 2 — `web/src/components/customer/EngagementOverview.test.tsx`, pure insertion of 11 lines AFTER line 124 (nothing is removed).
Context: line 124 is `  });`, line 125 is an EMPTY line — the new lines go between them. Copy context byte-exact from the file. The first `+` line is an EMPTY line (a `+` with nothing after it).

```
+
+  it("B22-08 follow-up: a customer the user added, with no sites or printers recorded, has no 'Sample data' tag on Sites & devices", async () => {
+    session([]);
+    const id = "CUST-SYN-ADDED-4";
+    mockState().customers.push({ id, name: "Harbourside Legal", synthetic: true, latestAssessmentStatus: null, createdAt: "2026-09-25T02:00:00Z", industry: "Professional services" });
+    show(id);
+    expect(await screen.findByRole("heading", { level: 1, name: "Harbourside Legal" })).toBeInTheDocument();
+    const sites = card("Sites & devices");
+    expect(within(sites).getAllByText("Not recorded").length).toBeGreaterThan(0);
+    expect(within(sites).queryByText("Sample data", { exact: true })).toBeNull();
+  });
```

**What must NOT change.** Any other line of `EngagementOverview.tsx` (in particular line 113, the header tags, and lines 165-168, the footnote). In the test file, do NOT touch the imports (lines 1-13), the mocks (lines 14-27), the helpers `session`, `show`, `card` (lines 29-38), or any existing `it(...)` block. Do not add imports: `mockState`, `show`, `card`, `screen`, `within` already exist in the test file (lines 2, 12, 34-38).

## The test

File: `web/src/components/customer/EngagementOverview.test.tsx`
The shape to copy is the test at lines 91-109 (`an API-only customer: ...`): it pushes a customer into `mockState().customers`, calls `show(id)`, awaits the h1, then asserts inside `card("Sites & devices")`. The new test is given in full above; write it exactly. There is no database / app boot / network here: the mock API runs in-process (`handleMock`, test file lines 14-18) — copy that shape and nothing else.
Run from the repo root: `cd web && npx vitest run src/components/customer/EngagementOverview.test.tsx`.

## Cells and controls

How the checker proves red (read by the coordinator, not the model): `red_test_cmd` runs ONLY the new test (`-t "B22-08 follow-up: a customer the user added"`) and passes only when the output says `Tests  1 passed`. With the whole diff reverted the test does not exist, so the command fails (measured rc 1 for the DocumentGeneration brief; same mechanism, not re-run for the other two). That proves the test is present and green with the fix; the stronger property, that the test is RED against the unfixed product line, was measured by the brief-writer (Premises) and is the tamper below.

- `added-no-facts` = `B22-08 follow-up: a customer the user added, with no sites or printers recorded, has no 'Sample data' tag on Sites & devices`   <- RED before Edit 1, GREEN after
- `seeded-sites` = `the demo customer, assessment in progress: details, sample sites, progress, summary and the next step` (line 43; asserts the seeded sample's Sites panel still shows "Sample data" at line 50)   <- must stay GREEN
- `typed-figures` = `B24 B22-08/B22-22: a customer the user added carries no 'Sample data' label on the figures they typed` (line 111)   <- must stay GREEN

## The failing case (the "tamper")

Revert Edit 1: line 144 of `EngagementOverview.tsx` back to `        <Panel title="Sites & devices" id="sites-title" tags={factsRecorded ? undefined : <SampleTag />}>`. The new text `factsRecorded || !x ? undefined : <SampleTag />` is byte-unique in the patched file (literal count 1), and the old line is byte-unique at the tip (literal count 1). With the revert, the new test fails at its last assertion (`expected <span …> to be null`).

## Premises (each one measured, with where)

- `x` is computed at `EngagementOverview.tsx:91` as `extrasFor(customer.apiId, customer.name)`; `extrasFor` returns `null` for any id/name not in `CUSTOMER_EXTRAS` (`content.ts:72-74`).
- `SampleTag` renders the text "Sample data" (`parts.tsx:13-15` with `content.ts:78`).
- Line 144 old text: literal count 1 in the file at the tip (counted with Python `list.count`).
- RED/GREEN measured 2026-09-26 in a scratch copy of the tip (tarball at the Tip, `npm ci`, vitest 5.0.1): test file with only the new test = 1 failed | 8 passed; with Edit 1 too = 9 passed. The failure is at the new test's last line (`toBeNull`).
- Suite `src/components/customer src/components/screens`: 91 passed at the tip; 94 passed with all three sibling briefs applied together (this one adds 1).

## UNMEASURED — stated rather than glossed

The `red_test_cmd`/`suite_cmd` were run with `vitest --root web` from outside `web/`, not as `cd web && npx vitest ...` inside the checker's clone; the `npm ci` guard inside them was not run in a clone. `tsc`: 13 errors at the tip and 13 after, all `PageProps`/`LayoutProps` (Next.js generated types absent in a bare tarball) — none in the touched files, but a clean `tsc` was not achieved. ESLint was not run successfully (invoked outside the project; config not picked up). The live-API path (real service, not the mock) was not exercised. Playwright e2e not run.

## Collision

Sibling brief `ProfileScreen.brief.md` (same folder) also inserts a test into `EngagementOverview.test.tsx`, at a different place (after line 153, before the final `});`). The hunks do not overlap; both were applied together in the scratch copy and 94/94 passed. First round for this brief.

## Scope

Closes the Sites & devices panel residue of B22-08 / B24 FOUND-1 on the engagement overview. refs B22-08, does NOT close it: `DocumentGeneration.tsx` (two sites) and `ProfileScreen.tsx` are separate briefs; see `CENSUS.md`.

## Output

Exactly ONE fenced diff block, nothing outside it. Paths exactly as the File: lines give them (`a/<path>` and `b/<path>`). Every `+` line on its own physical line. Every context line keeps its leading space. One `--- a/` / `+++ b/` pair per file, product file first.

## REBRIEF (round 2 of 2) — what your first answer got wrong, exactly
Your round-1 diff had the RIGHT product line and the RIGHT test lines. Two format faults made it fail:
1. **The empty line is in the wrong place.** The FIRST `+` line of the test-file hunk must be an EMPTY `+` line, BEFORE the `it(` line. You put the empty line AFTER the closing `});` instead. Keep line 125 (the existing empty line) as a CONTEXT line after your 11 added lines.
2. **Hunk headers must count lines exactly.** Use these headers, verbatim:
   - product file: `@@ -143,3 +143,3 @@` (context line 143 empty, the -/+ pair for line 144, context line 145).
   - test file: `@@ -124,2 +124,13 @@` = context line 124 `  });`, then your 11 `+` lines (the first one empty), then context line 125 (empty).
Nothing else changes. Exactly ONE fenced diff block.
