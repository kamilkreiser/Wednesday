# B22-08 doc-header-sample-tag — the Document generation header shows "Sample data" only for seeded sample customers

File: `web/src/components/customer/DocumentGeneration.tsx`
File: `web/src/components/customer/DocumentGeneration.test.tsx`
Tip: `99483e47cf050c1de125c9805df7e46e878b4702`
Runner: `vitest`

Written 2026-09-26 09:59 AEST from the SHA above, both files read whole (`web/src/components/customer/DocumentGeneration.tsx` 225 lines, `web/src/components/customer/DocumentGeneration.test.tsx` 125 lines).

## The mode — read this twice

CODE+TEST. Your diff touches EXACTLY 2 files, both on the File: lines, modified in place: `web/src/components/customer/DocumentGeneration.tsx` (one inserted import, one changed line) and `web/src/components/customer/DocumentGeneration.test.tsx` (one inserted test). You never touch `web/src/components/customer/content.ts`, `web/src/components/ui/Tag.tsx`, or any other file.

## What is wrong (one paragraph)

`DocumentGeneration.tsx` line 92 renders `<SyntheticTag />` (literal text "Sample data", `Tag.tsx:32-34`) in the page header for EVERY customer, including one the user added live. The signal that separates seeded samples from user-added customers is `extrasFor(customer.apiId, customer.name)` from `./content` (`content.ts:72-74`): seeded samples have extras, user-added customers get `null`. PR #28 used exactly this signal on the engagement overview (`EngagementOverview.tsx:91` and `:113`). This file does not import `extrasFor` yet (imports at lines 6-28 read whole). The fix imports it and renders the tag only when extras exist. The rest of the header (the `deterministic` tag, the lead) is unchanged.

## The exact change

3 edit points. Line numbers are the line numbers AT THE TIP, before any edit. Your hunk headers must use them.

Edit 1 — `web/src/components/customer/DocumentGeneration.tsx`, pure insertion of 1 line AFTER line 20 (nothing is removed).
Context: line 20 is `import { customerApi } from "./api";`, line 21 is `import { isApproved, latestExecutiveSummary } from "./ApiNarrative";` — the new lines go between them. Copy context byte-exact from the file.

```
+import { extrasFor } from "./content";
```

Edit 2 — `web/src/components/customer/DocumentGeneration.tsx` line 92, replacement.
Context: line 91 is `      <div className="no-print">`, line 93 is `          lead="Create documents from this customer's engagement data: the executive report, or a focused part of it." />` — copy both as context, byte-exact from the file.

```
-        <PageHeader title="Document generation" eyebrow={customer.name} tags={<><SyntheticTag /><Tag kind="deterministic">From the scored result: rules, not AI</Tag></>}
+        <PageHeader title="Document generation" eyebrow={customer.name} tags={<>{extrasFor(customer.apiId, customer.name) && <SyntheticTag />}<Tag kind="deterministic">From the scored result: rules, not AI</Tag></>}
```

Edit 3 — `web/src/components/customer/DocumentGeneration.test.tsx`, pure insertion of 15 lines AFTER line 112 (nothing is removed).
Context: line 112 is `  });`, line 113 is an EMPTY line — the new lines go between them. Copy context byte-exact from the file. The first `+` line is an EMPTY line (a `+` with nothing after it).

```
+
+  it("B22-08: the seeded sample keeps its 'Sample data' tag; a customer the user added has none", async () => {
+    session([]);
+    const seeded = show();
+    const h1 = await screen.findByRole("heading", { level: 1, name: "Document generation" });
+    expect(within(h1.parentElement!).getByText("Sample data", { exact: true })).toBeInTheDocument();
+    seeded.unmount();
+    const { mockState } = await import("@/server/mock/store");
+    const id = "CUST-SYN-ADDED-DOC";
+    mockState().customers.push({ id, name: "Harbourside Accounting", synthetic: true, latestAssessmentStatus: null, createdAt: "2026-09-25T02:00:00Z", industry: "Professional services" });
+    pathname = `/customers/${id}/documents`;
+    render(<CustomerShell customer={customerForRoute(id)!}><DocumentGeneration /></CustomerShell>);
+    const added = await screen.findByRole("heading", { level: 1, name: "Document generation" });
+    expect(within(added.parentElement!).queryByText("Sample data", { exact: true })).toBeNull();
+  });
```

**What must NOT change.** Line 166 (`<p className="mt-2 font-semibold">Sample data · neutral template</p>`) — it is a known second site and is deliberately OUT of this brief. Do NOT touch any other import line, the `Stepper` component, or anything below line 93. In the test file, do NOT touch the imports (lines 1-13), the mocks (lines 15-29), the helpers (lines 31-45) or any existing `it(...)` block; do NOT add a top-level import — the new test loads `mockState` with a dynamic `await import("@/server/mock/store")` inside the test, as written.

## The test

File: `web/src/components/customer/DocumentGeneration.test.tsx`
The shape to copy is the test at lines 105-112 (`the template choice offers the neutral template...`): `session(...)`, `show()`, await the h1 `Document generation`; the render-with-an-API-id shape is the one `EngagementOverview.test.tsx` lines 91-96 use. The new test is given in full above; write it exactly. There is no database / app boot / network here: the mock API runs in-process (`handleMock`, test file lines 15-19) — copy that shape and nothing else.
Run from the repo root: `cd web && npx vitest run src/components/customer/DocumentGeneration.test.tsx`.

## Cells and controls

How the checker proves red (read by the coordinator, not the model): `red_test_cmd` runs ONLY the new test (`-t "B22-08: the seeded sample keeps"`) and passes only when the output says `Tests  1 passed`. With the whole diff reverted the test does not exist, so the command fails (measured rc 1 for the DocumentGeneration brief; same mechanism, not re-run for the other two). That proves the test is present and green with the fix; the stronger property, that the test is RED against the unfixed product line, was measured by the brief-writer (Premises) and is the tamper below.

- `added-header` = `B22-08: the seeded sample keeps its 'Sample data' tag; a customer the user added has none`   <- RED before Edits 1-2, GREEN after (its first half, the seeded customer, is green both before and after; the second half is the red one)
- every other `it` in `DocumentGeneration.test.tsx` (6 tests)   <- must stay GREEN

## The failing case (the "tamper")

Revert Edit 2: line 92 back to its tip text (given in Edit 2's `-` line; literal count 1 at the tip). The new line-92 text containing `extrasFor(customer.apiId, customer.name) && <SyntheticTag />` is byte-unique in the patched file (literal count 1). With the revert, the new test fails at its last assertion (`expected <span …> to be null`).

## Premises (each one measured, with where)

- `extrasFor` is exported by `web/src/components/customer/content.ts:72` and returns `null` for an id/name not in `CUSTOMER_EXTRAS` (`content.ts:31-70`).
- `customer.apiId` and `customer.name` exist on the `Customer` type (`web/src/lib/customers.ts:12-25`); `customer` is `useCustomer()` at line 63.
- `PageHeader` renders the tags in a div beside the h1 inside the same parent div (`web/src/components/ui/PageHeader.tsx:19-25`), so `h1.parentElement` scopes the assertion to the header.
- Line 92 old text: literal count 1 at the tip.
- RED/GREEN measured 2026-09-26 in a scratch copy of the tip (vitest 5.0.1): only the new test = 1 failed | 6 passed (fails at the last `toBeNull`); with Edits 1-2 = 7 passed.

## UNMEASURED — stated rather than glossed

Same as the sibling briefs: the exact `cd web && ...` commands and the `npm ci` guard were not run inside the checker's clone; `tsc` shows 13 pre-existing `PageProps`/`LayoutProps` errors before and after (none in touched files); ESLint not run successfully (import order is not known to be linted; the import is placed after `./api`, unsorted like the neighbouring lines 20-28). The live-API path was not exercised.

## Collision

Line 166 of this same file is a second "Sample data" site; it needs the same `extrasFor` import, so it is a FOLLOW-UP brief to write only after this one lands (writing it now would add a duplicate import). No other brief in this folder touches this file. First round for this brief.

## Scope

Closes the Document generation HEADER site of B22-08. refs B22-08, does NOT close it: line 166 of this file (cover preview text) remains; see `CENSUS.md`.

## Output

Exactly ONE fenced diff block, nothing outside it. Paths exactly as the File: lines give them (`a/<path>` and `b/<path>`). Every `+` line on its own physical line. Every context line keeps its leading space. One `--- a/` / `+++ b/` pair per file, product file first.

## FORMAT TRAPS measured on this model today (read before writing the diff)
- An EMPTY **context** line is written as ONE SPACE character, never as nothing, and it is never dropped — including the last context line of a hunk.
- The hunk header counts must equal the lines you actually write: old count = context + `-` lines; new count = context + `+` lines. Count them before you write the header.


## REBRIEF (round 2 of 2) — Edit 3 is RE-SHAPED; this section REPLACES Edit 3 above
Your round-1 answer had the right product edits and the right test, but put the empty line after the test instead of before it, and miscounted the header. So Edit 3 now inserts AFTER line 113 (the existing EMPTY line), BEFORE line 114, and the empty `+` line comes LAST. Write this hunk EXACTLY (the lines starting with a space are context; line 113 is ONE SPACE):

```
@@ -112,3 +112,18 @@
   });
 
+  it("B22-08: the seeded sample keeps its 'Sample data' tag; a customer the user added has none", async () => {
+    session([]);
+    const seeded = show();
+    const h1 = await screen.findByRole("heading", { level: 1, name: "Document generation" });
+    expect(within(h1.parentElement!).getByText("Sample data", { exact: true })).toBeInTheDocument();
+    seeded.unmount();
+    const { mockState } = await import("@/server/mock/store");
+    const id = "CUST-SYN-ADDED-DOC";
+    mockState().customers.push({ id, name: "Harbourside Accounting", synthetic: true, latestAssessmentStatus: null, createdAt: "2026-09-25T02:00:00Z", industry: "Professional services" });
+    pathname = `/customers/${id}/documents`;
+    render(<CustomerShell customer={customerForRoute(id)!}><DocumentGeneration /></CustomerShell>);
+    const added = await screen.findByRole("heading", { level: 1, name: "Document generation" });
+    expect(within(added.parentElement!).queryByText("Sample data", { exact: true })).toBeNull();
+  });
+
   it("/documents: pick a customer to open its documents", async () => {
```
Edits 1 and 2 (the product file) are unchanged from above. Exactly ONE fenced diff block, product file first.
