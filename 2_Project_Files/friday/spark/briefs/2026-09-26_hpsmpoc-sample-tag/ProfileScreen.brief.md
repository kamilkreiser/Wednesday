# B22-08 profile-header-sample-tag — the Customer profile header of a user-added customer stops showing "Sample data"

File: `web/src/components/screens/ProfileScreen.tsx`
File: `web/src/components/customer/EngagementOverview.test.tsx`
Tip: `99483e47cf050c1de125c9805df7e46e878b4702`
Runner: `vitest`

Written 2026-09-26 09:59 AEST from the SHA above, both files read whole (`web/src/components/screens/ProfileScreen.tsx` 70 lines, `web/src/components/customer/EngagementOverview.test.tsx` 154 lines).

## The mode — read this twice

CODE+TEST. Your diff touches EXACTLY 2 files, both on the File: lines, modified in place: `web/src/components/screens/ProfileScreen.tsx` (one inserted import, one changed line) and `web/src/components/customer/EngagementOverview.test.tsx` (one inserted test — this is the nearest test file that already renders a customer screen inside the real `CustomerShell` against the mock API; there is no `ProfileScreen.test.tsx`). You never touch `web/src/components/customer/content.ts`, `web/src/components/ui/Tag.tsx`, `web/src/components/customer/EngagementOverview.tsx`, or any other file.

## What is wrong (one paragraph)

`ProfileScreen.tsx` has two headers. Line 19 is the branch for every customer WITHOUT a prototype assessment (`if (!customer.hasAssessment)`, line 18) — that is every API customer, including one the user added live — and it renders `tags={<SyntheticTag />}` unconditionally, so a user-added customer's profile shows "Sample data". Line 23 is reached only by the one prototype demo customer (`hasAssessment: true` exists only at `web/src/lib/customers.ts:34`), a seeded sample, so line 23 is correct and stays as it is. The seeded-vs-user-added signal is `extrasFor(customer.apiId, customer.name)` from `@/components/customer/content` (`content.ts:72-74`), the one PR #28 used on the engagement overview. The fix imports it and makes line 19's tag conditional on it.

## The exact change

3 edit points. Line numbers are the line numbers AT THE TIP, before any edit. Your hunk headers must use them.

Edit 1 — `web/src/components/screens/ProfileScreen.tsx`, pure insertion of 1 line AFTER line 8 (nothing is removed).
Context: line 8 is `import { ApiProfile } from "@/components/customer/ApiSteps";`, line 9 is `import { PlaceholderTag, SyntheticTag } from "@/components/ui/Tag";` — the new lines go between them. Copy context byte-exact from the file.

```
+import { extrasFor } from "@/components/customer/content";
```

Edit 2 — `web/src/components/screens/ProfileScreen.tsx` line 19, replacement.
Context: line 18 is `  if (!customer.hasAssessment) {`, line 20 is `  }` — copy both as context, byte-exact from the file.

```
-    return (<><PageHeader title="Customer profile" eyebrow={customer.name} tags={<SyntheticTag />} lead="The profile sets the context for the assessment." /><ApiProfile /></>);
+    return (<><PageHeader title="Customer profile" eyebrow={customer.name} tags={extrasFor(customer.apiId, customer.name) && <SyntheticTag />} lead="The profile sets the context for the assessment." /><ApiProfile /></>);
```

Edit 3 — `web/src/components/customer/EngagementOverview.test.tsx`, pure insertion of 16 lines AFTER line 153 (nothing is removed).
Context: line 153 is `  });`, line 154 is `});` — the new lines go between them. Copy context byte-exact from the file. The first `+` line is an EMPTY line (a `+` with nothing after it).

```
+
+  it("B22-08: the profile of a seeded sample keeps its 'Sample data' tag; a customer the user added has none", async () => {
+    session([]);
+    const { ProfileScreen } = await import("@/components/screens/ProfileScreen");
+    pathname = "/customers/sample-b/profile";
+    const seeded = render(<CustomerShell customer={customerForRoute("sample-b")!}><ProfileScreen /></CustomerShell>);
+    const h1 = await screen.findByRole("heading", { level: 1, name: "Customer profile" });
+    expect(within(h1.parentElement!).getByText("Sample data", { exact: true })).toBeInTheDocument();
+    seeded.unmount();
+    const id = "CUST-SYN-ADDED-5";
+    mockState().customers.push({ id, name: "Harbourside Legal", synthetic: true, latestAssessmentStatus: null, createdAt: "2026-09-25T02:00:00Z", industry: "Professional services" });
+    pathname = `/customers/${id}/profile`;
+    render(<CustomerShell customer={customerForRoute(id)!}><ProfileScreen /></CustomerShell>);
+    const added = await screen.findByRole("heading", { level: 1, name: "Customer profile" });
+    expect(within(added.parentElement!).queryByText("Sample data", { exact: true })).toBeNull();
+  });
```

**What must NOT change.** Lines 23 and 24 (the prototype customer's header), and nothing from line 20 down. Do NOT touch line 9 (the `Tag` import). In the test file, do NOT touch the imports (lines 1-13), the mocks (lines 14-27), the helpers (lines 29-38) or any existing `it(...)` block; do NOT add a top-level import — the new test loads `ProfileScreen` with a dynamic `await import(...)` inside the test, as written.

## The test

File: `web/src/components/customer/EngagementOverview.test.tsx`
The shape to copy is the test at lines 91-96: push a customer into `mockState().customers`, render inside `CustomerShell` with `customerForRoute(id)!`, await the h1. The new test sets `pathname` itself (the module-level `let` at line 19) and calls `render(...)` directly because `show()` renders `EngagementOverview`, not `ProfileScreen`. The new test is given in full above; write it exactly. There is no database / app boot / network here: the mock API runs in-process (`handleMock`, test file lines 14-18) — copy that shape and nothing else.
Run from the repo root: `cd web && npx vitest run src/components/customer/EngagementOverview.test.tsx`.

## Cells and controls

How the checker proves red (read by the coordinator, not the model): `red_test_cmd` runs ONLY the new test (`-t "B22-08: the profile of a seeded sample"`) and passes only when the output says `Tests  1 passed`. With the whole diff reverted the test does not exist, so the command fails (measured rc 1 for the DocumentGeneration brief; same mechanism, not re-run for the other two). That proves the test is present and green with the fix; the stronger property, that the test is RED against the unfixed product line, was measured by the brief-writer (Premises) and is the tamper below.

- `profile-added` = `B22-08: the profile of a seeded sample keeps its 'Sample data' tag; a customer the user added has none`   <- RED before Edits 1-2, GREEN after (its first half, seeded `sample-b`, is green both before and after)
- every other `it` in `EngagementOverview.test.tsx` (8 tests)   <- must stay GREEN

## The failing case (the "tamper")

Revert Edit 2: line 19 back to its tip text (Edit 2's `-` line; literal count 1 at the tip). The new line 19 text containing `tags={extrasFor(customer.apiId, customer.name) && <SyntheticTag />}` is byte-unique in the patched file (literal count 1). With the revert, the new test fails at its last assertion (`expected <span …> to be null`).

## Premises (each one measured, with where)

- Line 18 `if (!customer.hasAssessment) {` guards line 19; `hasAssessment: true` appears only at `web/src/lib/customers.ts:34` (Quollridge, seeded); an API-only customer gets `hasAssessment: false` (`customers.ts:87`).
- `sample-b` is a seeded route (`customers.ts:46-47`, apiId `CUST-SYN-SAMPLE-B`) and `CUSTOMER_EXTRAS["CUST-SYN-SAMPLE-B"]` exists (`content.ts:37`), so the control half keeps its tag after the fix.
- `PageHeader` puts the tags beside the h1 in the same parent div (`web/src/components/ui/PageHeader.tsx:19-25`).
- Line 19 old text: literal count 1 at the tip.
- RED/GREEN measured 2026-09-26 in a scratch copy of the tip (vitest 5.0.1): only the new test = 1 failed | 8 passed (fails at the last `toBeNull`); with Edits 1-2 = 9 passed.

## UNMEASURED — stated rather than glossed

Same as the sibling briefs: the exact `cd web && ...` commands and the `npm ci` guard were not run in the checker's clone; `tsc` shows 13 pre-existing `PageProps`/`LayoutProps` errors before and after (none in touched files); ESLint not run successfully. Placing a ProfileScreen test in `EngagementOverview.test.tsx` is a convenience of this runner (it refuses a File: that does not exist at the tip, so a new `ProfileScreen.test.tsx` cannot be named); a reviewer may prefer to move it.

## Collision

Sibling brief `EngagementOverview.brief.md` also inserts into `EngagementOverview.test.tsx`, after line 124. This brief inserts after line 153. The hunks do not overlap; both applied together passed 94/94 in the customer+screens suite. First round for this brief.

## Scope

Closes the Customer profile header site of B22-08. refs B22-08, does NOT close it; see `CENSUS.md`.

## Output

Exactly ONE fenced diff block, nothing outside it. Paths exactly as the File: lines give them (`a/<path>` and `b/<path>`). Every `+` line on its own physical line. Every context line keeps its leading space. One `--- a/` / `+++ b/` pair per file, product file first.

## FORMAT TRAPS measured on this model today (read before writing the diff)
- An EMPTY **context** line is written as ONE SPACE character, never as nothing, and it is never dropped — including the last context line of a hunk.
- The hunk header counts must equal the lines you actually write: old count = context + `-` lines; new count = context + `+` lines. Count them before you write the header.
