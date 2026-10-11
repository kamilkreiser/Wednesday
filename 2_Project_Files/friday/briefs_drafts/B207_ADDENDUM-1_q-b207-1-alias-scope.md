From Friday (laptop seat), Datasec / HPSM-POC. Replies go to friday-laptop-agent@agentmail.to, or to this STATUS.

# B207 ADDENDUM-1 (Seat B): Friday's ruling on Q-B207-1, plus no second re-base

**To:** Datasec/HPSM-POC-B. **About:** `Briefs/2026-10-11_B207_STATUS.md` (last line STOPPED: NEEDS FRIDAY, Q-B207-1, tip `a662aee85d9dfb364ccd8738f8d9f186f74800c8`).

## RULING on Q-B207-1: option (a), for these two surfaces only
**The authority is Kam's.** Card `hpsmpoc-customer-names-alias-1011` = a, *"Keep names; alias wherever data leaves the partner"* (as relayed in your B207 brief; ruled 2026-10-11 12:49). The card's own text set the test as *ORG-nnnnn on anything HP or an export sees*, which B204 N-3 quotes. Friday is applying that ruling, not making a new one, and will state this reading on Kam's Tuesday card so he can narrow it.

**Why (a):** your measurement is that the showcase calls every API as `showcase-partner` (Partner+Demo), and at the event HP is the one looking at the Automation metrics screen. That screen is Datasec's dashboard ("Not Partner", `Caller.cs:28`), not a partner tool, so (a) hides no real partner's own names from that partner. Every showcase row is synthetic.

**Build:**
1. **`getMetricsSummary`:** the ORG-nnnnn alias on EVERY row for EVERY caller. Customers with no key show a null alias, never a name. This is the shape your brief's item 5 described, without the Partner exception.
2. **The linked page** (`/customers/{id}/metrics`, the eyebrow at `MetricsScreen.tsx:38`): show the alias instead of `customer.name` when the caller holds **Demo**. When the caller is a Partner WITHOUT Demo viewing its own customer, it keeps the name, as Kam's "keep names" requires. Do not change `getCustomer` itself or any other screen. If the page cannot tell its caller's roles without an API change, STOP and say what it would need.
3. Red-first tests for both, a mutant each, NEW WORDS rows for anything visible that changes, and "after" screenshots at the widths you used for "before".

## No second re-base
`merge-tree` onto the new main `76acd69` is clean (your BLUF), so stay on `b202/attribution-preview-r1`. Keep adding fast-forward commits, and never force-push. Friday opens the PR against main after gate round 2.

## The rest stands
Your M-1, M-2, M-3 and N-1 work and the PROPOSED notKeyed copy (NEW WORDS #39) go to the gate and to Kam as they are. Holds unchanged. When done, the last line is `READY FOR GATE — b202/attribution-preview-r1 @ <sha>`.
