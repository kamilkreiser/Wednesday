# FIRMWARE-STAGE firmware-task-engagement-status — the firmware task's "Related engagement" status shows the customer's real stage, not always "New lead"

File: `web/src/components/customer/FirmwareTask.tsx`
File: `web/src/components/customer/FirmwareTask.test.tsx`
Tip: `291a4eb29b650afdb60ffa16bcc6ff4bbcc0d1a7`
Runner: `vitest`

Written 2026-09-26 10:46 AEST from the SHA above. Both files were read in full: `web/src/components/customer/FirmwareTask.tsx` (203 lines) and `web/src/components/customer/FirmwareTask.test.tsx` (105 lines).

## The mode — read this twice

CODE+TEST. Your diff touches EXACTLY 2 files, both named on the File: lines, and both are modified in place:
- `web/src/components/customer/FirmwareTask.tsx`: one line is replaced by two lines.
- `web/src/components/customer/FirmwareTask.test.tsx`: one test is inserted.

You never touch `web/src/components/customer/directory.ts`, `web/src/components/customer/useDirectory.ts`, `web/src/components/customer/EngagementOverview.tsx`, or any other file.

## What is wrong (one paragraph)

`FirmwareTask.tsx` line 65 computes the status that the "Related engagement" panel shows (line 109, `<StagePill stage={stage} />`). It reads `customer.hasAssessment ? stageFromPrototype(state.assessment) : stageFromApi(null)`. Every API customer has `hasAssessment: false`, so its stage is always `stageFromApi(null)`, which is `"new"` (`directory.ts:48`, `default: return "new"`). That renders "New lead" (`directory.ts:15`). A customer whose snapshot is in progress, scored or has its report issued (the seeded Kookaburra, for example) still reads "New lead" on its firmware task, while the Customers list shows its real stage. The Customers list gets that stage from `useDirectory()` rows: `DirectoryRow.stage` is computed in `directory.ts:89` from the API's `latestAssessmentStatus`, or from the prototype session for the one prototype customer. `FirmwareTask.tsx` already imports `useDirectory` (line 25) and already matches rows by `r.routeId === customer.id` (line 44, in `CustomerSwitch`). The fix reads this customer's row stage and falls back to today's expression while the directory is still loading.

## The exact change

There are 2 edit points. Line numbers are the line numbers AT THE TIP, before any edit, and your hunk headers must use them.

Edit 1 — `web/src/components/customer/FirmwareTask.tsx` line 65. Replace 1 line with 2 lines.
Context: line 64 is ``  const base = `/customers/${encodeURIComponent(customer.id)}`;``, and line 66 is `  const findings = res.status === "ready" ? res.result.findings : [];`. Copy both as context, byte-exact from the file. Neither is empty.

```
-  const stage = customer.hasAssessment ? stageFromPrototype(state.assessment) : stageFromApi(null);
+  const { rows } = useDirectory(); // the same stage the Customers list shows for this customer
+  const stage = rows.find((r) => r.routeId === customer.id)?.stage ?? (customer.hasAssessment ? stageFromPrototype(state.assessment) : stageFromApi(null));
```

Edit 2 — `web/src/components/customer/FirmwareTask.test.tsx`. Insert 11 lines AFTER line 104; nothing is removed.
Context: line 104 is `  });` and line 105 is `});`. The new lines go between them. Neither context line is empty. Copy both byte-exact from the file. The first `+` line is an EMPTY line: a `+` with nothing after it. It sits right after the non-empty context line `  });`.

```
+
+  it("the related engagement shows the customer's own stage, as the Customers list does: a snapshot in progress is not a new lead", async () => {
+    session([]);
+    const none = show("sample-c");
+    await screen.findByRole("heading", { level: 1, name: "Firmware risk assessment" });
+    expect(await within(card(/^Related engagement/)).findByText("New lead")).toBeInTheDocument();
+    none.unmount();
+    show("sample-b");
+    await screen.findByRole("heading", { level: 1, name: "Firmware risk assessment" });
+    expect(await within(card(/^Related engagement/)).findByText("Assessment in progress")).toBeInTheDocument();
+  });
```

**What must NOT change:**
- Line 25 (`import { useDirectory } from "./useDirectory";`) is already there. Do NOT add or change any import. `stageFromApi` and `stageFromPrototype` are still used, so their import at line 20 stays exactly as it is.
- Do NOT touch `CustomerSwitch` (lines 36-50), line 63 (`const x = ...`), or anything from line 66 down.
- In the test file, do NOT touch the imports (lines 1-15), the mocks (lines 17-27), the helpers (lines 29-42), or any existing `it(...)` block.

## The test

File: `web/src/components/customer/FirmwareTask.test.tsx`
The shape to copy is the test at lines 87-96 ("switching customer goes to that customer's task"): `session([])`, then `show(...)`, then await something that the async directory load renders. The new test uses the file's own helpers: `show(routeId)` (lines 36-39), which renders inside the real `CustomerShell` against the in-process mock API, and `card(name)` (line 40). It needs no new import: `within` and `screen` are imported at line 4.
- `sample-c` has no assessment in the mock seed, so it stays "New lead". This half is the control.
- `sample-b` has the seeded in-progress snapshot (`server/mock/store.ts:98`, customer `CUST-SYN-SAMPLE-B`, status `in-progress`), so its stage is "Assessment in progress" (`directory.ts:16`).

There is no database, no app boot and no network here: copy that shape and nothing else.
Run from the repo root: `cd web && npx vitest run src/components/customer/FirmwareTask.test.tsx`.

## Cells and controls

How the checker proves red (the coordinator reads this, not the model):
- `red_test_cmd` runs ONLY the new test (`-t "the related engagement shows the customer's own stage"`). It passes only when the output says `Tests  1 passed`.
- With the whole diff reverted, the test does not exist. Measured: rc 0, `Tests  5 skipped (5)`, so the grep fails and the command fails.
- The stronger property, that the test is RED against the unfixed product line, was measured by the brief-writer (see Premises). The tamper below repeats it.

The cells:
- `fw-stage` = `the related engagement shows the customer's own stage, as the Customers list does: a snapshot in progress is not a new lead`. It is RED before Edit 1 and GREEN after. Its first half (`sample-c`, "New lead") is green both before and after.
- Every other `it` in `FirmwareTask.test.tsx` (5 tests) must stay GREEN.

## The failing case (the "tamper")

Revert Edit 1: replace the two new lines with line 65's text at the tip (Edit 1's `-` line).
- Before the edit, that line has a literal count of 1 at the tip.
- After the edit, the new line containing `rows.find((r) => r.routeId === customer.id)?.stage` has a literal count of 1 in the patched file.

With the revert, the new test fails at its last assertion: `Unable to find an element with the text: Assessment in progress`.

## Premises (each one measured, with where)

- Line 65 is the only place `stage` is set, and line 109 renders it (`<StagePill stage={stage} />`). Read at the tip.
- `stageFromApi(null)` returns `"new"`, whose label is "New lead" (`directory.ts:42-49`, `:15`). `DirectoryRow.stage` comes from `latestAssessmentStatus`, or from the prototype for the one prototype customer (`directory.ts:89`).
- The rows use the same route id as `customer.id`: `CustomerSwitch` matches them with `r.routeId === current` (line 44), and the new test's GREEN proves the match for `sample-b`.
- For the prototype customer (Quollridge), the row's stage is `stageFromPrototype(session.assessment)` (`directory.ts:89`), so its displayed stage is unchanged.
- Measured 2026-09-26 in a scratch copy of the tip (a tarball of 291a4eb, `npm ci`, vitest 5.0.1, Node 26.8.1):

| Run | Result |
|---|---|
| Full vitest at the tip | 616/616 |
| New test, product at tip (RED) | 1 failed, 5 passed; fails at `Unable to find … Assessment in progress` |
| New test, with Edit 1 (GREEN) | 6/6 |
| `-t` filter, only the new test | `Tests  1 passed \| 5 skipped (6)` |
| customer+screens suite | 95 at base → 96 with the diff, 0 failed |

- `tsc --noEmit`: 13 errors, all in the pre-existing Next.js `PageProps`/`LayoutProps` group, and none in a touched file. ESLint (`--max-warnings=0`, run in `web/`) on both touched files: rc 0.

## UNMEASURED — stated rather than glossed

- The exact `cd web && ...` commands and the `npm ci` guard were not run in the checker's clone. The checker was not run on this brief.
- The page now makes a second `loadDirectory()` call, because `CustomerSwitch` already calls `useDirectory()`. That is a customers list plus up to 25 details, against the BFF. It was not measured live. It is a small cost in the showcase (5 customers), not a correctness issue.
- Not clicked live: the seeded Kookaburra (report issued) should now read "Report issued" on its firmware task.
- Node 26 was used, not the repo's `.nvmrc` 24.

## Collision

- No open branch or PR touches either file. The only open PR is #27, and its files do not include either one (checked by name via `gh pr view 27`).
- This is the first round for this brief.

## Scope

This is a new finding from this screen. It is not a B22 row. It is the same class as B22-07 (a customer page disagreeing with the Customers list). It closes this one site.

## Output

Exactly ONE fenced diff block, with nothing outside it.
- Paths exactly as the File: lines give them (`a/<path>` and `b/<path>`).
- Every `+` line on its own physical line.
- Every context line keeps its leading space.
- One `--- a/` / `+++ b/` pair per file, product file first.

## FORMAT TRAPS measured on this model today (read before writing the diff)
- An EMPTY **context** line is written as ONE SPACE character, never as nothing, and it is never dropped. That includes the last context line of a hunk. (In this brief no context line is empty. Keep it that way: use exactly the context lines named above.)
- The hunk header counts must equal the lines you actually write: old count = context + `-` lines; new count = context + `+` lines. Count them before you write the header.
- The insertion's EMPTY `+` line goes FIRST in Edit 2, directly after the context line `  });`. It never goes after the new test's closing `  });`, and never after the final `});`.
