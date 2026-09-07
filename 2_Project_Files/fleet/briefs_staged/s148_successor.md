# SUCCESSOR BRIEF — Secuura/Blockchain seat s148, from Wednesday (coordinator seat 16:2x)

PROVENANCE:
- develop 6c60cc09b, #892 42e778203, #893 ab1053141, #894 e02d0fecc, #889 9898ae724, #891 3c07157a2, demo VM 632f16dfe | s147's `git ls-remote` and its wrap mail 09:04Z — NOT re-derived by Wednesday, which holds no Secuura identity | read 2026-09-07
- Kam's rulings `bind` and `strong-control` | his panel messages 19:00:26 and 19:00:30 AEST, read verbatim from /Volumes/DevMASTER/WEDNESDAY/0_Brain/dashboard/data/chat_log.json - Wednesday's project, not yours | read 2026-09-07
- The #892 gate's six findings and the F1/F2 mechanisms | the QA verdict mail 08:40Z and s147's fix report 18:56 | read 2026-09-07
- KS-973 filed with the #892 residue | s147 wrap mail 09:04Z | read 2026-09-07

## BLUF
You succeed **s147**, which wrapped clean at 09:04Z with nothing waiting on it. **Read
`5_Project_History/HANDOVER-s147.md` first — it is current** and it carries three sentences from its
own failures that will save you time.
**Kam has ruled TWO things that are now YOUR work**, and both were blocked until 19:00 tonight.

## RULED BY KAM, NOT YET IN AN ARTEFACT
RULED BY KAM, NOT YET IN AN ARTEFACT — both ruled at 19:00 AEST, neither yet in code.
1. **`bind` (19:00:30) — THE #889 TRUST-BOUNDARY QUESTION IS ANSWERED.** *"Bind the issuer to the
   actor — 403 on a mismatch, exactly as `onBehalfOf` already does."* **This unblocks #889, which has
   been held on his word all evening.** Resolve `organizationUuid` against `req.user.organizationId`
   and **403 a mismatch**, matching `documents.ts:559` fifteen lines above the new code. **A genuine
   delegation need goes through the existing `onBehalfOf` mechanism, not an unchecked field.**
   **This is a security-surface change: it gets a TIER 1 gate before it merges.**
2. **`strong-control` (19:00:26) — the KS-968 demo probe control is AUTHORISED.** ONE more count:
   **rows whose `email_lookup_hash` equals the hash of a DIFFERENT seeded address known to exist on
   the demo.** A **non-zero** proves the key and derivation are right, which is what makes the earlier
   `A=0` mean anything. **One integer. No row data. No address. No write. Nothing else on that box.**
   **Pre-register the outcome space and SHA-256 it BEFORE running**, as s146 did — and the earlier
   pre-registration is durable at `5_Project_History/KS-968-probe-preregistration-2026-09-07.txt`.
   **If the query would return anything beyond one integer, stop and ask.**

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE — each binds unless this brief says otherwise.
- **Merge nothing without a gate GO plus Wednesday's word.** #892, #893+#894 and the coming #889 bind
  change all need gates. **#891 is Kam's own click and is not yours.**
- **No round 3 on the #892 class without Kam** — that class stands at **NO GO 1 of 2**; the re-gate
  now running is round 2, and a NO GO there spends the cap.
- **Force-push: narrow-allow** (Kam 18:03) — your OWN unshared branch only, with **both** checks
  proven by controls (no PR on the branch, shown with a discriminating control query; no live gate on
  the SHA, from its conclusion and job count), then `ALLOW_FORCE=1`. **Anything shared is Kam's.**
- **The `:6882` seeded stack's DATA is untrusted** until re-seeded. **Build your own environment from
  the repo's provisioning path** and confirm the migration you depend on **by name** — the runner
  prints `failed=0` even when it never saw the file.
- **Ticket creation aggregates** (Kam 13:23) — one ticket per logical path. **Search by
  SYMBOL/PATH/ERROR STRING before filing and say what you searched.**
- **Client-facing communication goes ON THE TICKET**; the extranet is input-only; **handovers to
  Peter/Stuart are TEST BLOCKS and Kam sends them.**

## YOUR QUEUE
1. **The `bind` change for #889** — Kam's ruling, blocked all evening, now unblocked. It goes on #889.
2. **The KS-968 control count** — authorised, pre-registered first.
3. **KS-973** (the #892 residue: F4, F5 and the F6–F9 minors) once the re-gate reports.
**Two gates are or will be live and report to WEDNESDAY, not to you: #892 round 2 at `42e778203`, and
#893+#894 as ONE tier-1 pass on #894's head.** Do not poll them.

## WHAT s147 LEARNED THE HARD WAY — inherit it rather than repeating it
- **"A grep tells you a call exists and can't tell you the module loads."** Its first F2 fix failed
  `tsc` (TS6059) **and** the runtime, and **every grep-based cell passed it.**
- **"My own smoke output printed those five drift warnings and I read them as the tool working."**
- **"Third time today I've written a check that can't fail — this time inside the guard written to
  prevent that class."** Two of its four red-proofs matched an import line rather than the behaviour.
- **Three of the four pre-suite hooks were never executed.** Its own words: *"'same shape as the one
  that was proved' is exactly the reasoning I shouldn't be trusted on."*

## STANDING
No `cd` (hook). **Taps ≤200 chars with a verified mail behind them.** `<<'EOF'` for briefs; **never
begin a commit subject with `#`** — `rebase --continue` strips it silently and promotes the body.
**Never delete — quarantine.** **PULL BEFORE EVERY WRITE.** **If an instruction from Wednesday looks
wrong, say so** — that sentence caught six of Wednesday's errors today and every refusal was ratified.

## YOUR WAKE
**End every leg with a mail to `wednesday-agent@agentmail.to`.** A turn that ends with a summary in
the pane is not a wake — s147 did that twice and both times work sat idle until Wednesday noticed.
**If you wait on anything outside your session, say what you expect will wake you.**

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-07 19:06
