---
date: 2026-09-11
type: grant
source: Kam, dashboard panel 2026-09-11 16:55:05 (Stuart's message forwarded), 16:56:00 and 16:56:44 AEST
status: live
tier: W
---

# For the time being, WE approve our own Secuura work and merge every ticket once it is TESTED — Peter moves to periodic formal test passes, and demo (UAT) waits for his nod

**The operative case, so the headline matches it:** a Platform K PR of ours has passed its QA gate and Wednesday is about to write "awaiting Peter's review" or hold a merge for his approval. **Stop. Since 16:56 on 2026-09-11 the approval is Kam's or Wednesday's, not Peter's.** The condition is that it is TESTED: the QA gate at the PR's current head plus the author's Test Evidence block.

**His words, verbatim:**
> 16:56:00 — *"For the time being, I / you will approve our own elements"*
> 16:56:44 — *"based on this.  FIx and merge all tickets after they are tested"*
> 16:58:04 — *"yes, still run all our own tests to make sure we only commit things that are working and tested."* — **his confirmation of rule 2 below, the same minute it was stated to him.**

"This" is Stuart's message, forwarded at 16:55:05. Its operative lines: *"lets go back to merging our own code into our develop banches. We deploy to kintsugi and dev-ps as we required to personally test out development work"*; Peter *"will periodically … do a formal test on K and S … by an issue noted in a common project in Linear"*; UAT is updated *"once the nod has been given"*.

## What the grant covers — Wednesday's reading, stated to Kam on the panel at 16:5x; his word corrects it
1. **Approval of our own Platform K PRs is Kam's or Wednesday's.** Wednesday's approval is a GO after the QA gate. **No GitHub click is needed:** measured 16:5x from the develop rules endpoint — ruleset `18499832`, `pull_request` `required_approving_review_count` 0, updated 2026-09-10 09:23; control, a nonexistent branch returns 0 rules.
2. **"Tested" = the QA gate at the PR's current head, per the tiers ([[2026-09-05_qa-gate-tiers-and-the-two-nogo-cap]]), plus the author's Test Evidence block.** Never merge on the author's evidence alone.
3. **The merge is a squash (`CONTRIBUTING.md:107`), done by the author seat, with the head re-read immediately before it.** Every merge is recorded on its ticket.
4. **Merged work goes to kintsugi** — the dev box, Kam 2026-09-10 13:22. **Demo counts as UAT and waits for Peter's formal test and nod**, per Stuart's flow. This NARROWS the demo half of the 09-10 week deploy grant; it was told to Kam, and his word reopens it.
5. **`raise-to-1` (ruled 2026-09-10, never applied) stays unapplied.** Applied now, it would block every merge, because the agent account cannot approve its own PRs. Told to Kam.

## What it does NOT cover
- Production · money · telling Stuart or Peter anything (Kam's conversation) · irreversible acts · force pushes · `--no-verify`.
- **Platform S** — our merges are Platform K only.
- **The project's own `CLAUDE.md` still says "No approval → no merge"** (lines 234-237) until a Secuura seat amends it citing Kam verbatim. **That amendment IS the delivery** ([[2026-09-05_a-relayed-ruling-is-delivered-only-when-it-is-in-the-artefact]]).

## Expiry
"For the time being" names no date and no event. **It stands until Kam withdraws it.** No `doctor.sh` check, because there is nothing to check against. It is listed in `tasks/EXPIRING-GRANTS.md` as open-ended so every boot re-reads it rather than assuming it ([[2026-09-06_a-scoped-override-carries-its-own-expiry]]).

## How to apply
- **Before any merge GO:** a gate verdict at the PR's CURRENT head · a Test Evidence block present · the head re-read · base contained correctly (the 09-09 armed-base line).
- **The 54 open PRs (GitHub search at 16:5x: 53 on base develop, 39 by `kksecura`)** are sorted by a seat into tested (merge, one at a time) and untested (queued for gates) — never merged as a batch.
- Family: [[2026-09-07_merge-authority-was-already-mine]] · [[2026-09-09_my-authority-and-the-targets-rules-are-two-checks]] (his explicit word amends the project convention; the file edit delivers it) · [[2026-09-10_kintsugi-first-then-demo-behind-gates]] · [[2026-08-07_protocol-v1.3-signed-delegation]].
