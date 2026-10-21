---
date: 2026-10-21
type: decision-detail
client_project: Datasec/HPSM-POC
card: hpsmpoc-b377-word-pack-thursday-1021
source: B386 brief "WORD PACK FOR TUESDAY" (tuesday/briefs/2026-10-21_B386_SEAT-D17_hpsmpoc-lane6-reviewer-path-fixes.md:105-117), strings MEASURED by the B386 drafter at HPSM-POC main 54fbceac unless marked RELAYED; findings from the B377 hosted reviewer walk (2026-10-21 08:00)
status: open
---

# HPSM-POC — the eight wording findings from the HP-reviewer walk (Thursday build)

**BLUF.** The hosted-site walkthrough (B377, as an HP reviewer would see it) found eight places where the
WORDS are inconsistent or misleading. They are Kam's words, so no agent changed any of them: PR #173
(B386) fixed only the word-free issues. The card asks which, if any, go into the build HP reviews on
Thursday. Default if unanswered: none; the eight go on one ticket for after the review.

**Timing.** If Kam picks (b) or (c) by about 18:00 AEDT, a small lane builds it, a tier-2 gate checks it,
it lands and is deployed before the 23:59 freeze. Later than that, it waits for the next deploy.

## The eight (file:line at main 54fbceac; "RELAYED" = from B377's walk, not re-read)

| # | Finding | Where | Today's words |
|---|---|---|---|
| 1 | B377-4: five names for the product | `components/screens/SignInScreen.tsx:53`, `:121`; `components/shell/AppShell.tsx:148`; `app/layout.tsx:8`; `components/home/phase-flow.ts:65`, `:66`; content package `playbook-placeholder.v0.5.0.json:11` (RELAYED) | "HP Security Services Playbook" · "Playbook" / "Security Services Playbook" · "HPSM-POC — Security Services Playbook" and "%s · Security Services Playbook (POC)" · "DataSec-HP Playbook Platform Enabler" · "DataSec Security Services Playbook Web Platform" · "HP Print Security Services Playbook" |
| 2 | B377-12: "DataSec" vs "Datasec" | `phase-flow.ts:22`, `:23`, `:65`, `:66`; the page also shows "DATASEC IMPLEMENTATION PATH" (source line not located) | "DataSec Consulting Services touchpoints" and the two names above |
| 3 | B377-13: times shown without a time zone | the date formatter in `web/src/lib` (file not read) | "Report issued 10 Oct 2026, 9:51 pm" (RELAYED) |
| 4 | B377-15: "Home" vs "Partner Dashboard" | `components/partner/PartnerDashboard.tsx:50`; Menu "Customers" goes to `/workspace` while `/customers` shows the same list (`GlobalNav.tsx:27`) | title "Partner Dashboard" |
| 5 | B377-16: US and UK spelling mixed | counts only (RELAYED): "optimization" 5, "Prioritized", "Centralized", "unauthorized" 2, against 51 "-ise" words; site language en-AU; likely HP-supplied text | — |
| 6 | B377-17: "Your tools (coming later)" | `components/home/phase-flow.ts:28` (its own comment says these are new words for Kam to rule) | "Your tools (coming later)" |
| 7 | B377-18: wrong message for a visitor with no link | `components/followup/api.ts:120` (every 401 maps to it), under the heading "These questions cannot be shown" | "Your session has ended. Open the link again." |
| 8 | B377-19: "Customer not found" text | `CustomerShell.tsx:123-124` | "The customers service does not know this customer (it may have been removed, or the demo was reset)." |

## The options on the card, with the exact words proposed (Tuesday's proposals; Kam's to change)

- **(a) No word changes for Thursday.** HP sees today's wording. The eight go on one HPSMPOC ticket for after the review. *(default)*
- **(b) Fix the two consistency items only (1 and 2).** One product name everywhere a person reads it: **"HP Security Services Playbook"** (the name the sign-in page already shows first); the browser-tab template becomes "%s · HP Security Services Playbook". One spelling: **"Datasec"** (as in the company email domain). The HP-supplied content package name (item 1, last) is left alone. Items 3-8 go on the ticket.
- **(c) (b) plus the two messages (7 and 8).** Item 7 becomes **"This link is not valid or has expired. Please open the latest link your partner sent you."** Item 8 becomes **"This customer could not be found. It may have been removed, or the demo may have been reset."** Items 3-6 go on the ticket.
- **(d) Your own words** for any item: reply with the item number and the words.

**Not covered by any option, and unchanged:** nothing goes to HP or any person from an agent; handing the site to HP is Kam's. Items 3 (time zone), 4 (one canonical address) and 5 (spelling in HP-supplied text) are product or content decisions, not quick word swaps, which is why no option fixes them before Thursday.

**UNMEASURED:** whether the brand is written "Datasec" or "DataSec" in Datasec's own style guide (Tuesday read the email domain and the workspace's usage only); the exact count of places each string appears in the content packages.
