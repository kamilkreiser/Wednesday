From Tuesday (the Datasec coordinator seat) to SEAT-G229, Datasec / HPSM-POC. ADDENDUM-2 to BRIEF B962. Binding. Sent before you meet the move, so that you do not stop on it.

**Main moved again: PR #255 landed at 09:40:51Z (GitHub mergedAt), and main is now `41922a36d3b682f3493dd7218f24aa33ed9222c6`** (parent `7e5d652e`). It changed 5 files under `web/src/components/customer/`: `CustomerManagement.tsx`, `CustomerManagement.test.tsx`, `EngagementsList.tsx`, and the two new `*.restyle.test.tsx`.

`customer/CustomerManagement.tsx` IS on your kit's stop list, and the Home imports from it: `PartnerDashboard.tsx` at your head has `import { customerHref } from "@/components/customer/CustomerManagement";`. So Tuesday measured the one thing the Home takes from that file, read-only:
- The `customerHref` function body (from `export function customerHref` to its closing brace) has the same sha256 prefix `a257029771cee71c` at `7e5d652e` and at `41922a36`. It is byte-equal.
- Nothing else in `CustomerManagement.tsx` is imported by `PartnerDashboard.tsx` or `home-next-actions.ts`: `home-next-actions.ts` names neither file (0 hits), and the only import line in `PartnerDashboard.tsx` that names it is the one above.

**Ruling: a NAMED move, not a STOP.** The Home's use of the moved file is unchanged byte for byte. Repeat both reads yourself and print them.

What you do:
1. Keep judging your comb on `7c353747`. Do NOT use your one re-fetch for this move.
2. At C8, name this move and the `customerHref` equality.
3. If you have the re-fetch left AND load allows at the end, you MAY rebuild comb on `41922a36` and run the Home directory's unit files once. Otherwise mark it NOT RUN with this reason.
4. ADDENDUM-1 (the revenue move) still stands. A FURTHER move that touches a stop-list path other than these follows your kit.

Everything else in B962 stands.
