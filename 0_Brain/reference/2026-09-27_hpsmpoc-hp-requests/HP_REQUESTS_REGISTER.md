---
date: 2026-09-27
type: register
project: Datasec/HPSM-POC
rule: learnings/2026-09-27_hpsmpoc-every-hp-ask-is-its-own-email-plus-a-register.md (Kam, live board 2026-09-27 16:34)
status: live
---

# HPSM-POC: everything we need from HP

**Why this exists:** Kam alone talks to HP. Each ask below was sent to Kam as its own email, with a copy-ready message. This register holds every ask in one place, with what it is for and where it stands. It is updated in the same action as each new email.

## Summary
| # | What we need from HP | What it is for | Status |
|---|---|---|---|
| HP-1 | Corrected deck v3 slides (duplicates, wrong labels, wrong cross-references, HP's own open placeholders) | The digital Playbook's partner section (HPSMPOC-65, C-12 minimum), which loads the deck verbatim | Emailed to Kam 2026-09-27 16:37 (AgentMail sent copy); not yet sent to HP |
| HP-2 | Permission to use IDC's quote and logo (deck slide 91) | Slide 91, the only partner-section slide withheld from the digital Playbook | Emailed to Kam 2026-09-27 16:37 (AgentMail sent copy); not yet sent to HP |
| HP-3 | The Customer Security Maturity questions | The customer snapshot's real questions (C-19: today the ruleset is DRAFT with placeholder questions; HPSMPOC-31) | **Already asked by Kam** on 2026-09-25 (~16:03, per his instruction that day). No answer recorded. No new email: say if you want a chaser drafted |
| HP-4 | Security Manager: live access and integration overview | Integrating the Playbook with HP Security Manager (live data, integration path); Kam's 29 Sep meeting notes (C-30) | Emailed to Kam 2026-09-29 08:58 (AgentMail sent copy); not yet sent to HP |
| HP-5 | Overview of Quick Assess | Understanding how Quick Assess relates to the Playbook's assessment (C-30) | Emailed to Kam 2026-09-29 08:58 (AgentMail sent copy); not yet sent to HP |
| HP-6 | Control Hub: is it part of Security Hub? | Clarification: where Control Hub sits, and whether the Playbook should reference it (C-30) | Emailed to Kam 2026-09-29 08:58 (AgentMail sent copy); not yet sent to HP |
| HP-7 | Firmware vulnerability tool: access, and how to integrate or upload results | Bringing firmware-vulnerability results into the Playbook, possibly via Security Manager (C-30) | Emailed to Kam 2026-09-29 08:58 (AgentMail sent copy); not yet sent to HP |
| HP-8 | Fleet Assessment tool: access and info (paid Security Manager module) | Fleet Assessment tool access; a paid Security Manager module, so any licence is Kam's call (C-30) | Emailed to Kam 2026-09-29 08:58 (AgentMail sent copy); not yet sent to HP |

## Candidates, not yet asked (each needs your decision first)
| # | Possible ask | What it is for | Why it is not asked yet |
|---|---|---|---|
| C-1 | HP/HPSM approved policy or configuration examples | HPSMPOC-46/-47/-48: the recommendation view and report section use a synthetic file today | Unconfirmed whether HP or the Datasec SME supplies them |
| C-2 | HP logo use and its approval route | HPSMPOC-21: branding of the app and PDF (HP, Datasec or co-brand) | The branding choice itself is your decision first |

## HP-1: corrected deck v3 slides (formatted request)
Subject: Playbook deck v3: corrections needed on a few partner-section slides

Hi [name],

While turning the Playbook deck (v3) into the digital Playbook, we found some copy-paste and labelling errors in the partner section (slides 87 to 146). Could you send corrected versions of these slides, or confirm the right text, when you have a moment?

Duplicated content
1. Slide 98 (Foundations cover): the text repeats the Phase 3 cover (slide 123) word for word. What should the Foundations cover say?
2. Slide 113 (Success story): the page opens with the pricing paragraph from slide 108. What is the intended opening paragraph?

Wrong labels
3. Slide 117: "Phase 1 deliverables" appears on a Phase 2 slide.
4. Slide 126: "Phase 1 Deliverables" appears on a Phase 3 slide.
5. Slide 119: the hours table heads its column "Phase 1 activity".
6. Slide 102 (Model 2): the table's first column is headed "Year" above licensing rows.

Wrong cross-references
7. Slides 104 and 126: "See Section 3: Beyond Year 1" points to what is section 4 in the deck.
8. Slides 106, 115 and 124: the SOW guidance "will be finalized in Section 4: Making it work". Making it work is section 5, and the SOW templates already exist (slide 138).

Open items the deck itself marks for HP
9. Slide 97: five "[PLACEHOLDER — HP to confirm …]" notes.
10. Slide 113: a "[Note for HP: …]".
11. Slides 109, 119 and 128: "HP price $ to be confirmed"; slide 102: "[HP to confirm per-printer price]".
12. Slide 140: links marked "[… to be inserted by HP]".

Template filler (just confirming these are meant to be empty)
13. Slide 142 has placeholder (lorem ipsum) text, slide 145 ("Disclaimers") is empty, and slide 146 has an unfilled contact block.

Thanks,
Kam

## HP-2: IDC quote and logo on slide 91 (formatted request)
Subject: Playbook deck v3: may we use the IDC quote and logo (slide 91)?

Hi [name],

Slide 91 of the Playbook deck (v3) shows IDC's logo with a quote attributed to a named IDC analyst. We have left that slide out of the digital Playbook for now.

Can you confirm whether HP's licence to that quote and logo covers their use in the digital Playbook (an internal proof of concept shown to partners)? If it does, we will add the slide as it is. If it does not, or if there is a newer approved version of the quote, please let us know what to use instead.

Thanks,
Kam

## Update 2026-09-29 (Kam's HP meeting): HP-3
Kam's meeting notes, verbatim: *"HP has asked us to suggest what questions to use.  We will use the 16 questions as a base but will align the questions to Policy Principles (Datasec Security Composer)"*. So HP-3 turns around: HP is not supplying the customer questions; Datasec proposes them. The HPSM-POC seat (B48) drafts the aligned set for Kam's approval. HP-3 status: **reversed, awaiting our proposal**.

## HP-4: Security Manager: live access and integration overview (formatted request)
Subject: HP Security Manager: access to a live system and an integration overview

Hi [name],

Thanks for Tuesday's session. To build the Playbook properly we'd like to work against HP Security Manager itself. Could you help with:

1. Access to a live (or demo / sandbox) Security Manager system we can use during the build.
2. An overview of how to integrate with it: the APIs or export formats available, how authentication works, and any integration guide.
3. Any product information or documentation you'd recommend we start with.

Who would be the best person to arrange this?

Thanks,
Kamil

## HP-5: Overview of Quick Assess (formatted request)
Subject: Quick Assess: overview

Hi [name],

Could you give us an overview of Quick Assess: what it assesses, who runs it, what it produces, and how its results might feed into or complement the Playbook's assessment? Documentation or a short walkthrough would be ideal.

Thanks,
Kamil

## HP-6: Control Hub: is it part of Security Hub? (formatted request)
Subject: Quick question: Control Hub

Hi [name],

A quick clarification: is Control Hub part of Security Hub, or a separate product? What does it cover, and is it relevant to the Playbook's assessment or recommendations? A pointer to documentation would be great.

Thanks,
Kamil

## HP-7: Firmware vulnerability tool: access, and how to integrate or upload results (formatted request)
Subject: Firmware vulnerability tool: access and integration

Hi [name],

Could we get access to the firmware vulnerability tool, along with some information on it? In particular we'd like to understand how we would integrate with it or upload its results, and whether that is done through Security Manager.

Thanks,
Kamil

## HP-8: Fleet Assessment tool: access and info (paid Security Manager module) (formatted request)
Subject: Fleet Assessment tool: access and information

Hi [name],

Could we get access to, and information on, the Fleet Assessment tool? We understand it is an additional paid module in Security Manager. Could you confirm that, and let us know whether access could be arranged for the POC (for example a trial or demo licence)?

Thanks,
Kamil

## Update 2026-09-29 (after the full transcript): one consolidated follow-up to Steve
Steve asked for one bullet list (34:31 "Could you just put a bullet list?"). HP-4 to HP-8, plus the expert remediation guidance, the weighting-matrix owner and the question-vetting offer, were consolidated into ONE copy-ready email to Kam (sent 11:0x from friday-laptop-agent@). Source: HPSM-POC `Registers/2026-09-29_HP-follow-up-bullet-list_DRAFT-FOR-KAM.md` (B53). Status for HP-4 to HP-8: **in the consolidated follow-up; not yet sent to HP**. Partial answers from the meeting: HP-4, access is via Kumar (Bangalore) and HP asks us to say how; HP-5, Quick Assess = full Security Manager capped at 100 devices.

## Sources
- The slide register built while loading the deck: `HPSM-POC/1_Project_Definition/Architecture/content/2026-09-27_B41_deck-v3-partner-section/README.md` (lines 18, 84-89 and the per-slide table).
- HP-3: Friday's pickup and the 2026-09-25 notes (the questions were not found in any file we hold; measured across HPSM-POC Source_Documents and the HP Playbook Project folder).
