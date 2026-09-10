---
date: 2026-09-10
type: preference
source: Kam, email 2026-09-10 13:22 AEST, replying to Wednesday's UAT question
status: live
tier: W
---

# Secuura deploys go to KINTSUGI FIRST — demo is promoted to behind gates, and the board's "Deployed to UAT" label describes the OLD arrangement

**His words, verbatim (email, 2026-09-10 13:22):**
> *"The demo box is labeled badly (a legacy thing)*
> *Kintsugi is our dev box so things should always be deployed there first.*
> *This is approval to bring kintsugi up to date and deploy everything so its current. In the
> future deploy to kintsugi first*
> *And we will set up gates once everything is tested and working to deploy to demo."*

**This reverses what every session in this project had been doing**, which is why it is a rule
file and not a note. Until this email, `develop` merges landed and **the demo VM** was redeployed
to match; `secuura02-kintsugi-vm` was treated as out of scope and session after session recorded
*"Kintsugi untouched"* in its scope line.

## The two environments, so nobody re-derives them

| | box | host | role |
|---|---|---|---|
| **dev — deploy here FIRST** | `secuura02-kintsugi-vm` | `kintsugi.secuura.net` | Platform K's dev server (KS-601) |
| **demo — promoted to, behind gates** | `secuura02-demo-vm` | `demo-pk.secuura.net` | what prospects and the team are shown |

## Why this surfaced, and the part worth keeping

Stuart asked Kam whether *"Deployed to UAT"* on a Linear ticket meant it was on kintsugi too.
**The measured answer was no** — the deployment runbook targets demo, kintsugi appears in exactly
one file (its own build plan) and in no deploy script, and "Deployed to UAT" is assigned from
ancestry into what is deployed, which was demo.

**But the useful answer was underneath the yes/no:** the board label was describing an arrangement
Kam had already decided to change, and **Stuart may have been verifying fixes on a box that never
received them.** Answering only the question asked would have confirmed a stale shape and left the
real problem in place. [[2026-08-06_bluf-write-for-the-reader]] is about what to put first;
this is about noticing that the question is not the thing that matters.

## How to apply

1. **Kintsugi first, always, for anything with a deployable surface.** Demo is a promote, not a
   default, and it waits for the gates Kam is going to define.
2. **Do not trust the board's environment labels.** `Deployed to UAT` predates this ruling and
   describes demo. Until the board is re-labelled, read the state as "on demo" and say so.
3. ⚠ **KS-535 IS ABSOLUTE AND IT HAS ALREADY COST A SESSION: kintsugi must never share demo's
   `PLATFORM_WALLET_MNEMONIC`.** Two deployments on one wallet select the same UTxOs and race;
   the loser fails with `All inputs are spent`. It has happened at scale — 295 local and 2 demo
   anchors. **Any kintsugi deploy brief carries this by name.**
4. **Measure the box before deploying to it.** Kintsugi was down 53 hours (2026-09-07 → 09-09) and
   nobody should assume its state from memory.
5. **The project's own rule is that any deploy notifies Stuart and Peter** (extranet to-do +
   Linear comment). That still stands — but on 2026-09-10 Wednesday held the notice for Kam's word
   rather than sending it on the agent's initiative, because the day had already turned on who was
   told what.

**Family:** [[2026-09-10_steps-to-kam-are-a-claim-about-his-screen]] (a label is a claim about a
system, and this one had gone stale) · [[2026-08-03_mental-model-not-source-of-truth]] ·
[[2026-09-05_never-update-prod-and-demo-is-kams-class]].
