---
date: 2026-09-20
type: correction
source: Tuesday (Datasec seat) — nearly removed RD-518, a live security blocker, from Kam's critical path after refuting its stated cause
status: live
tier: W
---

# Refuting a defect's stated MECHANISM does not refute the DEFECT — the sentence can be right and its explanation wrong, and removing the line is the expensive half

**The lesson:** a ticket carries two things — a CONCLUSION ("X is broken") and a MECHANISM ("because
Y"). They fail independently. Disproving Y disproves Y. **The conclusion has to be killed on its
own terms, and it usually has more than one route to being true.** When the conclusion is a
security property, assume it survives until measured otherwise.

## The case — I was one instrument away from shipping it

RD-518 read: *"`KEYVAULT_NAME` vs `KEY_VAULT_NAME` — Key Vault silently does nothing in every
deployment."*

I measured the names. **They match.** The only tracked `mainTemplate.json` sets `KEYVAULT_NAME`,
`encryptionService.js` reads `KEYVAULT_NAME`, both build scripts consume that template, and every
`KEY_VAULT_NAME` in the tree is untracked build output. I wrote that the premise was "refuted in
the direction that would shrink the minimum set", told Kam on the panel it would likely come off
the list, and asked only whether the path "works".

**The conclusion was right the whole time, by a route nobody had written down.** The Key Vault
Crypto User role is granted to the **user-assigned** identity only. The code calls
`new DefaultAzureCredential()` with **no options**, no managed-identity client id is passed into
the container, and `AZURE_CLIENT_ID` is bound to the **printer-data service principal**. So:

- `hasPrinterData` TRUE → EnvironmentCredential runs first and authenticates as the printer-data
  SP, which holds no Key Vault role.
- `hasPrinterData` FALSE → ManagedIdentityCredential with no client id, and with both a
  system-assigned and a user-assigned identity present it resolves to the **system-assigned** one,
  which has no role assignment.

**In both shapes the credential used lacks the grant.** "Key Vault silently does nothing" was the
right sentence attached to the wrong cause.

## Why it was nearly fatal rather than merely wrong

**The failure is silent.** The KV path fails, encryption falls back to machine-id-derived keys, and
it logs a WARN. No error, no failed boot, nothing red. A broken deployment looks fine — so nothing
downstream would have contradicted my removal.

**And the reporting bug hid the functional bug.** The one surface that would say "Key Vault is not
configured" is `server.js`, which reads the *unset* `KEY_VAULT_NAME` and therefore says
`not_configured` **unconditionally** — so it carries no signal at all. The smaller defect I had
correctly identified was the thing suppressing the larger one I had dismissed.

## THE MIRROR, same day, same pair of tickets — a CORRECT conclusion resting on a reason that answered a NEIGHBOURING question

RD-518 was this lesson's forward case: **I refuted the mechanism and nearly killed a true
conclusion.** RD-550 is its mirror, and it landed on a ruling I had already made.

I ruled RD-550 out of the minimum set citing the agent's argument that the ticket "conflates two
stores" — AI config on the persistent volume, the SQLite store ephemeral. **Both halves were true.
Neither was operative.** Persistence on disk would not help if the boot hydration never ran: the
data would survive and still be unusable after a restart. **The evidence answered "is the data
DESTROYED" while the ticket asked "is the data APPLIED at boot."** Two adjacent questions, one
answer, and it fitted well enough that neither of us noticed.

The agent caught it **by re-reading the ticket's own words in order to rewrite it** — the ticket
said the *hydration* sits in the wrong branch, not that the store is lost. The real reason turned
out to be narrower and the ruling survived on better grounds.

**The rule: a ruling inherits the quality of the reasoning under it. Before accepting a reason,
check it answers THE QUESTION THE TICKET ASKED, not a neighbouring one that happens to be true.**
A true statement about an adjacent property is the most convincing wrong answer available, because
nothing about it is false.

**And the tell to watch for:** I accepted it because it was *well-measured*. It was — file paths,
volume mounts, all correct. **Rigour in the evidence is not relevance of the evidence**, and I have
no habit that checks the second once the first is satisfied. That habit is: restate the ticket's
question in one sentence, then ask whether the evidence is about THAT.

Same session, same pair: [[2026-09-20_a-control-in-the-wrong-scan-mode-buys-confidence]]'s w=3 root
is *I specify using a property I measured, and the property that governs is one I did not.* This is
its judgement-side twin: **I ACCEPT a property someone else measured, and the property that governs
is one neither of us checked.**

## The rule

1. **A ticket's conclusion and its mechanism are two claims. Kill them separately.** "The stated
   cause is wrong" is a finding about the ticket's TEXT, never about the world.
2. **Before removing a line from a critical path, ask: could this conclusion be true by another
   route?** Name the routes you checked. "I refuted the only route I thought of" is not a refutation.
3. **Asymmetry governs the effort.** Being slow costs an hour. Being wrong here ships silent
   fallback encryption to every customer. **When a measurement would let you REMOVE a blocker, take
   one more measurement** — the direction of the error is not symmetric and neither is its cost.
4. **Suspect a "the ticket is wrong" finding most when it is convenient.** Mine arrived exactly when
   I wanted the minimum set smaller and Kam's package sooner. That is when to slow down, not speed
   up ([[2026-08-14_i-read-representations-they-read-sources]]'s third switch: EXPECTATION).
5. **A feature that cannot announce its own absence is a defect in itself** — cousin of
   [[2026-08-07_a-check-that-cannot-fail]]. Where a control silently falls back, the fix includes
   making the fallback loud, not only wiring the path.

## What saved it, so the practice is kept

The agent **refused to say WORKS** when it had strong evidence and an obvious incentive to close —
it had proved every component provisioned and correctly scoped, and it still said that proves the
deployment *grants* what the code needs, not that the runtime *executes*. Then it named a cheap
next instrument. **I asked for the instrument instead of ruling on the inference.**

Two habits, and both are cheap: **never convert "strongly implied" into "measured" on a line that
gates someone else's decision**, and **when an agent offers a cheaper next measurement, take it
before you rule.**

Related: [[2026-09-20_a-control-in-the-wrong-scan-mode-buys-confidence]] (same session — a sound
control pointed at the wrong instrument) and its w=3 root, *I specify using a property I measured,
and the property that governs is one I did not*. This is that root wearing its diagnostic costume:
I **judged** using a property I measured, and the property that governed was one I had not.
