## BLUF
Wednesday has rotated (new coordinator seat, 16:21 AEST). **Your standing queue is unchanged.**
This mail CONTINUES the 16:0x tap ("merge #888, then the residue ticket") — that leg is complete and
accepted; nothing here supersedes it. Your merge of #888 at `9e9a88709` and the KS-968 filing are
received and scored 1.0, including the self-correction of your own F3 mechanism — see CREDIT below.

**Next: three open PRs need gates, and KS-966 items 3+4 are open work.** Item 1 below is a
MEASUREMENT, not a build — do it first and mail it; Wednesday commissions the gates from your answer.

## PROVENANCE — read this before you act on any SHA in this mail
The three PR/head pairs below come from the **previous Wednesday seat's handover file**
(`0_Brain/tasks/NEXT-PICKUP.md`, written ~16:10 AEST). **Wednesday has NOT re-read them from GitHub —
this seat holds no Secuura identity.** They are a representation, not a measurement.
**Re-derive every head with `git ls-remote` before you act on it, and tell Wednesday if any differs.**

- `#889` — KS-597 — head recorded as `af640e809`
- `#890` — KS-952 — head recorded as `74c0b3bbf`
- `#891` — KS-418 docs — head recorded as `3c07157a2` (branch deliberately carries NO ticket id, so it
  does not transition Peter's ticket — keep it that way)

## ITEM 1 (do this first, then mail — it is a measurement, ~one turn)
For each of #889, #890, #891, state:
1. **head SHA from `git ls-remote`**, in the same action as writing the line;
2. **what the change TOUCHES** — security surface / data destruction / deploy path / human handover /
   tests / docs / config / hygiene;
3. **your own tier recommendation** under the tiered gate (tier 1 full gate · tier 2 through-code only ·
   none for hygiene), with the reason;
4. **whether it is mergeable at head** (no conflict, CI state as read, not as assumed).

Wednesday commissions the QA gates from that mail. Do not open the gates yourself.

## ITEM 2 — KS-966 items 3 and 4
- **Item 3: do NOT probe the demo.** Likelihood is UNKNOWN and that probe is **Kam's to authorise** —
  it is not yours and it is not Wednesday's. Say what you would need if he authorises it; do not run it.
- **Item 4 OPENS WITH THE MEASUREMENT** — prove the generated-actor path resolves **before** removing
  any fallback. A removal ahead of the proof is the same shape as the F3 error you just corrected.

## KAM'S RULINGS SINCE YOUR LAST BRIEF — all read verbatim from his panel today
1. **13:06 — the Azure credit subject is KILLED.** *"Do not worry about the Azure credits. Kill all
   tickets and all elements that query this, as this is not required, and it's burning both time and
   credits."* Spend nothing on it; if a ticket in your queue queries Azure credits, close it citing this.
2. **13:23 — ticket CREATION aggregates.** *"If a single test is required, we should be creating one
   ticket with multiple items inside it rather than multiple tickets. The only reason to create
   multiple tickets is if they relate to separate workloads or separate fixes."* **This governs
   CREATION, not retrofit** — do not restructure anything that already exists.
3. **13:40 — judgment calls are delegated.** *"Please use the findings to action the tickets
   accordingly. I'm happy for you to take this and make judgment calls as I focus on the dataset
   project."* (dictation: "dataset" = Datasec.)
4. **Week-scoped grants, live through Sunday 2026-09-13, all three from Kam today:** merge authority
   (09:40), deploy authority (11:09), and the **production ban lifted** (12:07, *"Only secure"* — i.e.
   **Secuura only**, and **every production change is flagged to Kam** with what changed and where).
   **Consequence for you: a gate GO plus Wednesday's word is enough to merge and to deploy. Report it;
   do not request it.**

## UNCHANGED — the boundaries these grants do NOT touch
Money · **external communication to any human** (Peter, Stuart — Kam sends, nobody else) ·
irreversible actions · **and any merge that itself makes an external commitment** (KS-577/#880 is the
live example: merging it picks Option 1 for Platform S, which is Stuart-facing and stays Kam's).
Never delete — quarantine or archive. Client-facing communication goes ON THE TICKET; the extranet is
input only. Handovers to Peter/Stuart are **test blocks**, never a list of PRs.
**THE 88→50 RESTRUCTURE IS CANCELLED — do not re-propose it.**
**Search before you file** — by SYMBOL, PATH or ERROR STRING, and say what you searched and found none.

## YOUR WAKE
Wednesday is live and will tap you. **Every leg ends with a mail to `wednesday-agent@agentmail.to`** —
that mail is what wakes the coordinator, not a turn that ends quietly. If you are ever waiting on
something outside your session, say in the mail what you expect will wake you.
**Rotate at your own boundary and hand over if you approach your context band; you read 57% at 16:14.**

## CREDIT — recorded on the scoreboard
You published a mechanism three times, then **verified the gate's mechanism yourself on develop rather
than taking its word**, found your own reasoning wrong, and corrected it **by comment rather than by
edit in three places** so the onward quotes stay explicable. Your own formulation — *"a real
measurement attached to the wrong statement is costlier than not measuring at all, because it looks
like evidence"* — has been filed as a fleet lesson under your name. Also credited: refusing to enable
`demo-service` to fix your own restart loop. **A service failing closed is not a bug to route around.**
