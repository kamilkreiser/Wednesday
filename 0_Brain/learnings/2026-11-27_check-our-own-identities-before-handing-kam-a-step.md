---
date: 2026-11-27
type: correction
source: Kam, Tuesday terminal, 2026-11-27 (after the K2 click-step email)
status: live
tier: W
---

# Before handing Kam a step, check whether we can do it ourselves with an identity we already hold

**Rule.** Before any card, set of steps or email asks Kam to *do* something (create a user, an app registration, a role, consent, a resource, a setting), read whether a seat can do it with an identity or grant we already hold: the project's own `AZURE_CONFIG_DIR` (`az account show`, then a read-only `az ad` call), `gh auth status`, the project's `CLAUDE.md`, and `EXPIRING-GRANTS.md`. If a seat can, a seat does it and Kam gets a receipt. Only money, the signature classes (production, external comms, irreversible) and identities we genuinely do not hold go to his hands, and then the ask says why we could not do it.

**Kam's words (verbatim):** "you sent me an email to create a test user.  why?  you create john and william nichols yesterday.  so you or agent can do this.  I started the process but want to double check.  Dont forget the rule.  dont ask Kam if you can do it.  Also, thinking ahead what 2fa will you use?  Do you need a phone number?"

**What happened.** s333 wrote card K2 with the option "Tuesday sends the click steps; you create them". Kam tapped a. s334 commissioned a 9-page click-step PDF and sent it to him, without asking whether a seat could do the work. A read after his message showed the OXPd project's own `AZURE_CONFIG_DIR` signed in as kamil@datasec-rd.com in tenant ec01829b, and on 2026-11-25 a seat had already created two Security Manager logins and guest invites in that same tenant.

**Why it matters.** Every step handed to Kam costs his time and blocks the critical path on his calendar (K2 was dated 2 to 7 Dec). The standing rule already exists (2026-09-02 COO actionable tickets never wait for Kam; 2026-09-23 fix it yourself). The failure was inheriting a card's framing ("you create them") as if it decided who acts.

**How to apply.**
- A card option that says "you do X" is a premise to verify, not a decision about who acts.
- The identity read is cheap and safe (read-only); run it before writing the ask.
- When Kam has already started, tell him to stop where he is, read what he made, and only add.
- Second factor for a test user: no phone number needed. A seat-held software OATH (TOTP) token covers automated runs, if the tenant's authentication methods policy allows it (check first). A customer-mirror test of Authenticator number matching needs the Authenticator app on one device (no SIM).

Links: [[2026-09-02_coo-actionable-tickets-never-wait-for-kam]], [[2026-09-23_fix-it-yourself-talk-to-sister-seats-directly]], [[2026-09-18_a-premise-under-a-question-to-kam-is-load-bearing-verify-it]].
