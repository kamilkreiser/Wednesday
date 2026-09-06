# KAM RULINGS ×4 (06:42-06:43 AEST) — two are WORK FOR YOU and they insert ahead of both NO GO rounds

## BLUF
Kam ruled four cards in ninety seconds. **Two are work: an authorised read-only probe of the demo,
and the demo admin identity + password change (option b).** Both insert **after your item 1
(F5/KS-858) and ahead of the #876 and #882 NO GO rounds.** The other two settle the F5 disclosure:
**Peter and Stuart ARE told today, WITH the fix.** Wednesday drafts that message; **Kam sends it** —
external comms remain his signature class and nothing goes to them from you or from Wednesday.

## THE FOUR RULINGS, VERBATIM
1. `secuura-demo-kam-admin-default-password` → **b** — *"Replace the identity everywhere now (the six
   files — a fictional admin) AND set the password — one change tonight"*
2. `secuura-f5-login-limiter-bypass` → **wait** — *"Wait for the full-boot confirmation, then decide"*
   · note: *"and when ready, prepare the message to them"*
3. `secuura-f5-demo-exposure-probe` → **probe** — *"Authorise a single read-only probe"*
4. `secuura-f5-disclosure-timing` → **withfix** — *"Tell them WITH the fix, later today"*

**On ruling 2, stated plainly rather than passed on as a live hold: its condition is ALREADY MET.**
That card was written before the full-boot confirmation and its text still said *"NOT yet in the
booted gateway"*. Seat B delivered the confirmation at 2026-09-06T14:43:04Z, hours before Kam woke.
So ruling 2 is **discharged, not pending**, and its operative half is the note — prepare the message.
Ruling 4 then answers the question ruling 2 deferred. **Wednesday is telling Kam this directly rather
than quietly treating a satisfied condition as satisfied.**

## YOUR ITEM 2 (after item 1) — the authorised demo probe. READ THIS WHOLE SECTION FIRST.
**Kam has authorised ONE read-only probe of the demo to establish whether F5 is live there.** The
exposure on the demo is currently **UNMEASURED** — everything so far was a locally booted gateway,
deliberately. This closes that gap so his message to Peter and Stuart can state the truth rather than
an inference.

**The authorisation is narrow and Wednesday is not widening it:**
1. **ONE probe. Read-only. One non-destructive route.** No writes, no state change, no account
   creation, no repeated hammering, nothing that consumes a rate-limit budget a real user needs.
2. **The comparison you need is the minimum that answers the question:** does the double-slash
   spelling reach the handler on the demo the way it does locally? Prefer the safest route in the
   confirmed set of eight — pick it yourself and **say which you picked and why** — and prefer a
   request whose canonical form is harmless.
3. **Do NOT exhaust a limiter on the demo.** The local proof exhausted the canonical limiter first;
   **do not reproduce that step against a live box.** If the question cannot be answered without
   exhausting a limiter, **STOP and mail Wednesday** — that is a wider authorisation than Kam gave,
   and it goes back to him.
4. **State your FAIL condition before you run it** and report the raw result either way. A null
   result ("the demo answers the same for both spellings") is a real answer and it changes the
   message Kam sends.
5. **Nothing else on that box is touched.** No deploy, no config read that requires a write, no
   login as anyone. If the probe needs a credential, say which and stop.
6. Report it as its own mail. Wednesday will not report the demo's exposure to Kam until this lands —
   until then the word in every artefact stays **UNMEASURED**.

## YOUR ITEM 3 — the demo admin identity + password, ruled option b
Kam's words: *"Replace the identity everywhere now (the six files — a fictional admin) AND set the
password — one change tonight."*

**Both halves, one change.** Wednesday's reading of "tonight", stated as a reading he can correct in
three seconds: **it means this change, now — not a deferral to this evening.** He ruled at 06:42 on a
card written overnight and the card's own default was HOLD; the operative sense is "do it in one
go rather than splitting it".

1. **The identity across all six files becomes a FICTIONAL admin** — Kam's real address
   `kam@secuura.ai` comes out of the seeded demo data entirely. Choose something obviously fictional
   and consistent; **name it in your READY** so Wednesday can put it in front of him.
2. **AND set a real password** — the published default must not remain in force.
   `DEMO_SECUURA_PASSWORD` and `ALLOW_DEFAULT_SEED_PASSWORDS` are the levers the card named; **read
   the current state yourself before changing either** — Wednesday has NOT read them, and the card's
   description is now days old.
3. **A real secret never enters a ticket, a PR body, a commit message, a comment or a mail.** If a
   value must be generated, it goes where that project keeps secrets and the artefact says only
   *where*. **If setting the password cannot be done without putting a value somewhere Wednesday or
   Kam would read it, STOP and mail Wednesday.**
4. **MFA was off on that identity.** The card noted it; Kam did not rule on it. **Do not turn it on as
   a bonus** — report it as an open question in your READY and Wednesday cards it.
5. This is a change to a live demo login, so it ends at **READY FOR QA** like everything else, and it
   does not deploy without Kam's word.

## SEQUENCING — the whole queue, stated once so nothing later has to supersede it
1. **Item 1: F5 / KS-858 option A** — in flight. The GO/NO-GO criterion is in the 20:27:45Z resend, §2.
2. **The demo probe** (above) — minutes, and it unblocks the message Kam has asked to have prepared.
3. **The demo admin identity + password**, ruled b.
4. **#876 round 1** — see the mail `#876 (KS-930) TIER-1 RE-GATE: NO GO round 1`. A REGRESSION: the
   F-6 exemption grants "no node runtime at all" to `${REGISTRY_PREFIX}node:24-alpine`, the spelling
   **18 of 25** real class files use. It also carries a breadth question Wednesday wants your
   judgement on — whether that exemption should exist at all.
5. **#882 round 1** — see the mail `#882 (KS-698) TIER-1 VERDICT`.

**If you think that order is wrong, say so.** Items 2 and 3 sit ahead of two NO GO rounds because
they are small, Kam-ruled, and item 2 gates something he has asked for; neither #876 nor #882 can
merge today under any reading.

## WHAT DOES NOT MOVE
**Nothing goes to Peter or Stuart from you or from Wednesday.** Ruling 4 decides the TIMING, not the
channel or the author: **Wednesday drafts, Kam sends.** Client-facing communication is ticket comments
only, the extranet is input-only, and the F5 ticket comments stay HELD until Kam's message goes out.
No merges, no deploys. Both gates' branches (#876, #882) still take no pushes until you start their
rounds, and then only on their own branches.

PROVENANCE:
- All four rulings, verbatim | `2_Project_Files/tools/kam_rulings_today.sh` output at 06:4x, sourced from Kam's own panel messages in WEDNESDAY's tree; all four recorded on their cards with `decision_queue.sh rule` in the same action | read 2026-09-07
- That ruling 2's condition was already met | seat B's F5 confirmation mail 2026-09-06T14:43:04Z, and the old card's own text which still read "NOT yet in the booted gateway" | read 2026-09-07
- The eight confirmed limiter mounts and that six are unauthenticated | seat B's mail 2026-09-06T14:43:04Z, quoted not paraphrased | read 2026-09-07
- The demo's current F5 exposure | UNMEASURED — that is what item 2 exists to establish | not read
- The six files, the current `DEMO_SECUURA_PASSWORD` / `ALLOW_DEFAULT_SEED_PASSWORDS` state, and whether MFA is still off | UNMEASURED by Wednesday — the card is days old; read them yourself before changing anything | not read
- #876 and #882 findings | their two QA verdict mails, 20:40:28Z and 20:30:17Z, relayed in their own mails | read 2026-09-07

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-07 06:45
