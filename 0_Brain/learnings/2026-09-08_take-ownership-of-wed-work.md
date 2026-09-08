---
date: 2026-09-08
type: preference
source: Kam, panel, verbatim
status: live
tier: W
---

# Any WED work is CLAIMED before it is started — client work is split by machine, and Wednesday's own project is the half with no owner

**His words, verbatim (2026-09-08, panel):**
> *"from now on, any work on wednesday, take ownership so both agents dont work on the same things"*

**The operative case, so the headline matches it:** a seat is about to start work on the WEDNESDAY
project itself — a tool, a dashboard change, a doctor check, a lesson consolidation, a launcher.
**Claim it first, in a place the other seat can see, and release it when done.** Client work needs
none of this: his 2026-09-07 11:01 ruling already splits Secuura to the Studio and Datasec to the
laptop. **WED work is the only category with no owner, and it is exactly where two coordinators
collide.**

## Why he asked, and the instance that earned it

Hours before he said this, s150 read *"item (b) is STILL NOT STARTED"* out of a handover it had
inherited from the other seat, **repeated it to Kam on the panel**, and began sizing a build of a
chat-panel filter **that had existed since 2026-09-07**. Only opening the file stopped it. Nothing
about that failure was exotic: an unowned WED item, two seats, and a claim that lived in a handover
the other seat does not read.

**The general shape: a claim that lives in a handover is invisible to the seat most likely to
duplicate it.** Handovers are written for a SUCCESSOR on the same machine; the other coordinator
never reads them.

## How to apply

1. **Claim before starting, not after deciding.** `2_Project_Files/tools/wed_claim.sh claim "<item>"`.
   It pulls first, refuses (rc 3) when an OPEN claim already matches, and **pushes immediately** — the
   push is the publication, and it is what makes the claim visible rather than discoverable-in-a-conflict.
2. **`check` before proposing WED work to Kam**, not just before building it. Proposing a thing the
   other seat is already doing costs his attention, which is the scarce resource this exists to protect.
3. **Release when done**, with a note. An OPEN claim on finished work is an overstated record and will
   get the whole ledger discounted ([[2026-08-16_an-overstated-record-gets-discounted-wholesale]]).
4. **`--force` exists and its use is stated in the item text.** Two genuinely distinct pieces of work
   can touch one file; a gate that cannot be overridden gets routed around instead of used
   ([[2026-09-07_a-prior-ruling-gate-refusal-is-a-research-prompt]] — a refusal is a question, answer it).
5. **"Not started" inherited from the other seat is a CLAIM WITH A DATE, not a fact** — check the
   ledger AND open the artefact before acting on it. That is the failure above, and the claim ledger
   does not replace the check; it only makes the duplication visible earlier.
6. **Scope: WED work.** Client work stays split by his 11:01 ruling. If that split changes, this file
   does not — the ledger covers whatever has no owner.

## Honest limits, stated rather than discovered later

- **It is advisory, not enforcing.** Nothing prevents a seat from working without claiming; the tool
  only makes a collision visible. Promoting it to enforcement (a pre-write hook) is a candidate if a
  duplication happens anyway, not before ([[2026-08-03_go-slow-earn-autonomy]] rule 4).
- **The match is a case-insensitive substring**, deliberately loose. It will warn on near-misses. That
  is the correct direction for a warning whose false positive costs one `--force` and whose false
  negative costs duplicated work.
- **It cannot help if a seat does not pull.** Every subcommand pulls first for exactly this reason, and
  a failed pull prints a warning rather than proceeding silently.
- **His scope word is "from now on"** — a standing rule, not a windowed one, so no expiry is owed
  (contrast [[2026-09-06_a-scoped-override-carries-its-own-expiry]], which applies to his week-scoped grants).

**Family:** [[2026-07-31_manage-dont-do]] (who does the work) · [[2026-08-09_an-enforcement-you-must-arm-is-not-one]]
(why this is a tool and not a habit — and the honest note that it is still only advisory) ·
[[2026-09-07_a-rule-for-creation-is-not-a-mandate-to-retrofit]] (rule 2: before reshaping anything,
find what already occupies the slot — the exact miss that earned this) ·
[[2026-08-14_i-read-representations-they-read-sources]] (an inherited "not started" is a representation) ·
[[2026-09-05_a-relayed-ruling-is-delivered-only-when-it-is-in-the-artefact]] (a claim in a handover is
not delivered to the other seat).
