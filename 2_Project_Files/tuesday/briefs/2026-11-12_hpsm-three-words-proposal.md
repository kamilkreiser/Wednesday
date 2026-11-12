# HPSM-POC Playbook site: three wording changes before the UAT deploy

Prepared 2026-11-12 (at drafting) for the product owner, following his ruling of 2026-11-12 14:38: "Fix all three before deploying".
Nothing here has been built, committed or sent. "MA:n" is line n of the messaging document of 12 November (`messaging_alignment.txt`).
Line numbers are at the reviewed branch head `9308afa0`, read from GitHub and printed by `grep -n`.

## BLUF

Three wording changes before the UAT deploy; approve as proposed, or pick the alternative per point.

1. Walkthrough cover: "HP-aligned recommendations" becomes "recommendations mapped to applicable HP capabilities" (your document's own form until HP approves the stronger one).
2. Next engagement page: the lead stops naming three engagement types the page never picks, and says what it does pick.
3. Home page: the "planned" note says the *integration* is planned, not the HP products.

Each change is words only: no layout, route or behaviour changes, and nothing claims HP approval or shows an integration as done.

## 1. Walkthrough cover lead

**WHERE.** `web/src/content/walkthrough/steps.ts:42` (`COVER.lead`), drawn by `web/src/components/walkthrough/WalkthroughPanel.tsx:141`. Seen on the demo walkthrough panel, step 1, in the blue title card under "The trust you've earned. The opportunity ahead."

**TODAY.**
> "From trusted print partner to security-led business growth. The Playbook connects guided assessments, reviewed findings, HP-aligned recommendations, customer reporting and commercial next steps. Partners can deepen existing relationships, deliver relevant technology and services, and build recurring engagement without having to become cybersecurity consultancies."

**PROPOSED.** The same paragraph with one phrase swapped:
> "From trusted print partner to security-led business growth. The Playbook connects guided assessments, reviewed findings, recommendations mapped to applicable HP capabilities, customer reporting and commercial next steps. Partners can deepen existing relationships, deliver relevant technology and services, and build recurring engagement without having to become cybersecurity consultancies."

Source: MA:96 (the paragraph, verbatim) with MA:46's second form ("recommendations mapped to applicable HP capabilities").

**WHY.** MA:46 says to prefer "HP-aligned, product-validated recommendations" only after approval; until then use "recommendations mapped to applicable HP capabilities". Every other walkthrough line already uses that form (steps 2, 8 and 14), so the cover was the one place still using the wording that waits on HP.

## 2. Next engagement page lead

**WHERE.** `web/src/components/screens/NextEngagementScreen.tsx:23` (the `lead` under the page title "Next engagement"). Seen on a customer's Next engagement page (`/customers/<customer>/next-engagement`).

**TODAY.**
> "The logical next engagement (a paid assessment, a no-fee review or a managed review), chosen by rule, with the reason shown."

**What the page actually picks.** One follow-on engagement for the subject area with the biggest gap between today's score and the target (rule `largest-weighted-gap`; the page already says so at `NextEngagementScreen.tsx:51`). In the current ruleset (`snapshot-policy-aligned` 0.1.2) the five are, as the page shows them:
- A follow-on engagement for printer & fleet administration (its scope is being finalised)
- A follow-on engagement for network (its scope is being finalised)
- A follow-on engagement for identity & access (its scope is being finalised)
- A follow-on engagement for security governance & risk (its scope is being finalised)
- A follow-on engagement for security operations & monitoring (its scope is being finalised)

None of them is a paid assessment, a no-fee review or a managed review, and the page shows no price ("Not shown: service pricing is not confirmed yet.").

**PROPOSED.**
> "The logical next engagement for the area with the biggest gap, chosen by rule, with the reason shown."

Source: MA:233 (describe the demonstrator accurately); "the area with the biggest gap" repeats the page's own "How it is chosen" line. No "paid", per MA:65-66 (paid assessments are optional, not every partner charges).

**ALTERNATIVE.**
> "The logical next engagement, chosen by rule, with the reason shown."

The original lead minus the word "paid" (MA:65-66). Shorter still; leaves the area to the "How it is chosen" and "Area" lines below it.

**WHY.** Your document's three types (MA:65) were pasted into this lead in today's change, but the rule never chooses by type: it chooses a subject area. A reader from HP would look for a "managed review" on the page and find a "follow-on engagement for network" instead.

## 3. The "planned" note on the Home page tool lists

**WHERE.** One string, `web/src/components/home/phase-flow.ts:24` (`toolsNote`), drawn by `web/src/components/home/PhaseFlow.tsx:53`. It shows **three times**, once under each "Tools / assets" heading of the panel "Assess. Implement. Optimize." on the Home page (`/home`, `PartnerDashboard.tsx:103`). A search of every web source and test file at the head finds no other place it renders.

The lists it sits above (`phase-flow.ts:40`, `:51`, `:62`):
- Assess: HP Firmware Security Tool, HP Security Manager / EWS, Manual assessment template, Findings report template
- Implement: HP Security Manager, HP Web Jetadmin, HP Authentication Suite / Protected Access, HP Threat Assessment
- Optimize: HP Threat Assessment Reporting, HP Security Manager, Quarterly review template, SIEM integration if available

**TODAY.**
> "Tools named here are planned or subject to implementation until release validation is complete."

**PROPOSED.**
> "Integration with the tools named here is planned or subject to implementation until release validation is complete."

Source: MA:260 ("integrations with live HP systems ... not yet connected in the standalone prototype ... describe these capabilities as planned or subject to implementation until release validation is complete"), with its own subject, "integrations", put back.

**ALTERNATIVE.**
> "The Playbook is not yet connected to the tools named here. It guides the workflow; delivery may require them."

Source: MA:260 ("not yet connected") and MA:139 ("It guides the workflow; delivery may require HP management products"). Plainer, one sentence longer.

**WHY.** What MA:260 calls planned is the prototype's connection to HP systems, not the HP products themselves. HP Security Manager and HP Web Jetadmin ship today; the current note reads as if they do not. Both forms keep the point the approved line makes (no integration is shown as done) and still cover the "SIEM integration if available" item.

## Tests that pin each string (what changes with them)

- **1. Cover lead:** no test holds the sentence word for word; `web/src/content/walkthrough/steps.test.ts:65-66` scans the cover for banned words (the proposed text passes it). No test change needed.
- **2. Next engagement lead:** no test holds it (searched `web/src` and `web/e2e` for "logical next engagement" and "paid assessment, a no-fee": only the screen itself; control: the page title "Next engagement" is found in `web/e2e/keyboard.spec.ts:88`). No test change needed.
- **3. Tools note:** `web/src/components/home/PhaseFlow.test.tsx:46-47` (the exact sentence) and `:53` (it sits directly above each list); and the whole-page Home text in `web/src/components/partner/PartnerDashboard.text.test.tsx`, which carries the sentence three times in each of its two page states (around lines 32, 39, 45 and 81, 88, 94, split across fixed-width chunks). All three places change with the string.
