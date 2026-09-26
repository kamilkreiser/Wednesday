# HPSM-POC "Sample data" tag census (B22-08 / B24 FOUND-1)

Written 2026-09-26 09:59 AEST. Repo `datasecau/HPSM-POC`, `main` = `99483e47cf050c1de125c9805df7e46e878b4702` (checked with `gh api repos/datasecau/HPSM-POC/commits/main --jq .sha`; it had not moved). All of `web/src` was read from a tarball of that SHA.

**How the census was built.** (1) `grep -rn SyntheticTag web/src`, excluding tests. The 10 files claimed were confirmed; there are no others. (2) A case-insensitive `grep -i -e "sample data" -e synthetic` over `web/src/**/*.ts(x)`, excluding tests. It turned up the second label component, `SampleTag` (`customer/parts.tsx:13-15`, which renders `SAMPLE.tag` = "Sample data" from `content.ts:78`), plus some literal "Sample data" text. (3) Every hit was read in context. Control: the same grep finds the known `EngagementOverview.tsx:113` usage.

**The signal.** A seeded sample customer has "sample extras": `extrasFor(customer.apiId, customer.name)` (`customer/content.ts:72-74`, keyed at `:31-70`). A customer the user adds gets `null`. You can't use the API's `synthetic` flag to tell them apart, because every customer is `synthetic: true`: the mock refuses anything else (`server/mock/api.ts:178`), and so does the API (AD-19).

| # | File:line (at the tip) | Label | Verdict | Why | Route |
|---|---|---|---|---|---|
| 1 | `components/customer/EngagementOverview.tsx:144` | `SampleTag` on the "Sites & devices" panel | **defect** | The condition is `factsRecorded ? undefined : <SampleTag />`, so it doesn't check `x` (line 91). If the user adds a customer and records no sites or printers, the panel reads "Not recorded" (lines 148/152/160) and still carries "Sample data". This is residue left over after PR #28. | **Spark**: `EngagementOverview.brief.md` (2 edits) |
| 2 | `components/screens/ProfileScreen.tsx:19` | `SyntheticTag` in the header | **defect** | This is the `!customer.hasAssessment` branch (line 18), so every API customer lands here, including ones the user adds, and the tag is unconditional. | **Spark**: `ProfileScreen.brief.md` (3 edits) |
| 3 | `components/customer/DocumentGeneration.tsx:92` | `SyntheticTag` in the header | **defect** | It's unconditional and `eyebrow={customer.name}` sits beside it, so any customer, including a user-added one, gets the tag. | **Spark**: `DocumentGeneration.brief.md` (3 edits) |
| 4 | `components/customer/DocumentGeneration.tsx:166` | literal `Sample data · neutral template` on the cover preview | **defect** | The cover preview always renders (lines 152-167) under `{customer.name}` (line 161), so it says "Sample data" for a user-added customer too. | **Spark, follow-up**: not written yet. It needs the same `extrasFor` import as #3, so writing it now would clash with #3 (a duplicate import). Write it against the tip after #3 lands (1 product line + 1 test = 2 edits), or fold it into the same PR by hand. |
| 5 | `components/screens/ProfileScreen.tsx:23` | `SyntheticTag` in the header | correct | Only the `hasAssessment` branch reaches this line. `hasAssessment: true` exists only for the seeded Quollridge fixture (`lib/customers.ts:34`). | none |
| 6 | `components/customer/EngagementOverview.tsx:113` | `SyntheticTag` in the header | correct | It is gated on `x`. This is the PR #28 fix. | none |
| 7 | `components/customer/EngagementOverview.tsx:141, 167, 216` | `SampleNote` | correct | All three are gated on `x`. | none |
| 8 | `components/customer/CustomerManagement.tsx:161` | `SyntheticTag` in the page header of the customer list | unclear (page-level) | It isn't about one customer; it labels a list that mixes seeded and user-added rows. The same page already gates its list-level `SampleTag` on `rows.some(r => r.illustrative)` (line 213), which is a cheap model to copy if Kam wants the header to follow it. That's a product decision, not a defect. | decision; no brief |
| 9 | `components/customer/EngagementsList.tsx:24` | `SyntheticTag` in the page header of the engagements list | unclear (page-level) | Same as #8. If every started engagement belongs to a user-added customer, the header still says "Sample data". `useDirectory()` rows (line 19) carry `illustrative`, so the same gate as #8 is cheap. It's still a decision. | decision; no brief |
| 10 | `components/snapshot/SnapshotRunner.tsx:139` | `SyntheticTag` gated on `activePackage.package.synthetic` | unclear | The tag marks the **content package** (placeholder Playbook content), not the customer. But the eyebrow is the customer's name (line 138), and the tag's tooltip says "not a real customer" (`Tag.tsx:33`), so a user-added customer's snapshot looks tagged. The right fix is a wording/tag decision (a content tag, not the customer one), not a gate. | Claude + decision |
| 11 | `components/snapshot/SnapshotResult.tsx:50` | `SyntheticTag` gated on `activePackage.package.synthetic` | unclear | Same as #10. The eyebrow is the customer name once loaded (lines 43-49). | Claude + decision |
| 12 | `components/playbook/PlaybookHome.tsx:25` | `SyntheticTag` gated on `pkg.synthetic` | correct | The Playbook home has no customer; the tag labels placeholder content. | none |
| 13 | `components/screens/DesignSystemScreen.tsx:110` | `SyntheticTag` | correct | This is the design-system swatch row. | none |
| 14 | `components/ui/Tag.tsx:32-34` | `SyntheticTag` definition | n/a | This is the definition itself. | none |
| 15 | `components/customer/CustomerManagement.tsx:213` | `SampleTag` | correct | It is gated on `rows.some(r => r.illustrative)`. | none |
| 16 | `components/customer/ConversationCoach.tsx:113` | `SampleTag` on a talk track | correct | It labels the talk-track wording (sample script content, `content.ts:112-116`). Tracks built from the customer's findings get a different tag. | none |
| 17 | `components/customer/FirmwareTask.tsx:113` | `SampleNote` | correct | It is gated on `x?.engagementStart`. | none |
| 18 | `components/customer/ApiSteps.tsx:84` | text "Sample data only: fictional organisations, never a real customer." | unclear (policy text) | This is shown on every API customer's profile. It states the POC-wide rule that every customer is fictional (AD-19) rather than calling this customer seeded, so it is probably correct. Flagged for Kam's eye only. | none |
| 19 | `components/screens/ReportScreen.tsx:57` | text "Draft: sample data, and the scoring rules are not yet approved" | unclear | It is gated on a draft ruleset. `ReportPreview` is also used by Document generation for any customer, so a user-added customer's generated document says "sample data". This is wording, not a tag. | decision; no brief |
| 20 | `components/screens/ReportScreen.tsx:141` | text "All customer data in this proof of concept is sample data." | correct (policy text) | This is a methodology statement about the POC, not about one customer. | none |
| 21 | `app/layout.tsx:24`, `components/shell/AppShell.tsx:83`, `components/partner/*` | app banner / "Prototype" tag / partner showcase figures | correct | These are app-wide or partner showcase labels; none of them is about a customer. | none |

## Claude-needed

- **#10, #11 (Snapshot runner/result).** This isn't a gate problem: the tag is truthfully about the content package. Fixing it means choosing a different tag or wording, which is a product decision and not something to brief exactly. If the decision is instead to gate on the customer, the runner needs the customer id → `extrasFor` path worked out, and nothing measured here says `useSnapshot` exposes the API customer id (unmeasured).

## Decisions for Kam (not defects as specified)

- #8, #9: should page-level list headers carry "Sample data" when the list can contain user-added customers?
- #18, #19: POC-wide "sample data" wording on the screens of user-added customers.

## Measured

- The RED/GREEN for all three written briefs was run in a scratch copy of the tip (tarball, `npm ci`, vitest 5.0.1). Each new test fails without the product edit, at its final `toBeNull`, and passes with it. The customer+screens suite goes 91 → 94 passed with all three applied together, 0 failed.
- `tsc --noEmit`: 13 errors before and 13 after, all `PageProps`/`LayoutProps`. Those are Next.js generated types, which are missing from a bare tarball. None is in a touched file.

## UNMEASURED

- ESLint: it did not run, because the config wasn't picked up when invoked from outside `web/`.
- The briefs were not run through `spark_run.py --dry-run` and the answers were not put through `spark_check.py`. A hook refuses write git verbs outside FRIDAY, so no checked-out clone could be made. Instead, the briefs were parsed with the runner's own `parse_brief`: File:/Tip: are OK, `expect.files` equals the brief's File: lines, and every `expected_added` line appears as a `+` line in its brief.
- The `npm ci` guard inside `red_test_cmd`/`suite_cmd` was not run inside the checker's clone (it needs network there).
- The live API path and the Playwright e2e were not run.
- Harness note for the coordinator: `spark_check` C4 reverts the WHOLE diff, including the added test. So `red_test_cmd` is written to pass only when the new test exists and passes (`-t <name>` plus `grep "Tests +1 passed"`). The stronger property, that the test is red against the unfixed product line, was measured here but is not re-proved by the checker.
