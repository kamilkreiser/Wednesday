---
date: 2026-09-08
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's (Kam ruled the name 11:56). Read Datasec mail by SUBJECT only.
source: replaced WHOLESALE at 22:4x by s154 at its 50% checkpoint (band is 80-90, Kam 2026-09-07 — this is NOT a rotation)
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — s154 (Studio) LIVE at 50%. Secuura s153 REBUILDING. Nothing blocked, nothing waiting on Kam.

## 🟢 s153 IS MID-BUILD — do not re-brief it, do not tap it, wait for its delta mail
Booted 22:31, **verified at RUNG 6** (boot mail; brief DKIM-verified with all eight failing-value
controls absent AND a positive discrimination control 8/8 over a synthetic blob; commission quoted
back; floor re-read in its own action). Confirmed to start at 22:33. **At ~21% and building.**

**Its next mail is the DELTA, both directions, or a STOP if the build fails.** Answer it promptly —
this seat has twice ended a seat's turn by staying silent, and the rule adopted is **the reply goes
BEFORE the capture.**

    BUILT_SHA   5ffaaf396c6957c2498447fd80c039ef92831206   (develop; head re-verified from origin
                immediately before the build launched, and it had not moved since its boot)
    building    32 services serially; postgres/redis/stack-marker are image-only and not rebuilt
    monitored   by PID 22245 AND by log growth — never by the wrapper's exit (trap 3)

## 🔴 THE TWELVE ENDPOINTS ARE A BASELINE, NOT FINDINGS — nothing from them is filed before the delta
Every suite s152 ran tested **today's spec against images built 2026-09-02..05**. s153 sharpened this
and its framing is the one that carries: **the gap is the SIX DAYS of image age, not the nine commits**
between `811a82253` and head — only ONE file under `Blockchain/Dev/services` changed across those nine,
so nearly the whole delta lives in the older half. **Say that in the delta write-up**, or a reader will
assume the nine commits explain whatever moves.

The set, quoted as s152 wrote it (Wednesday has expanded no shorthand):

    GET /api/gdpr/erasures/{externalRef} · POST /api/gdpr/erasures
    POST /api/m365/connections/complete · /init · /{id}/refresh
    POST /api/m365/documents/sync · POST /api/m365/outlook/exchange-token · POST /api/m365/sites
    POST /api/oauth/apps/{id}/rotate-secret · POST /api/onedrive/files/{id}/sync
    POST /api/teams/webhook-config · POST /api/wallets/verify

> 🔴 **CORRECTED 22:5x by s153's delta — this framing was WRONG AT EVERY HOP and the correction
> lands here because this file is the only one of the three that can still be edited.** s152's mail and
> Wednesday's brief both say *"eleven attributable, one unattributed"*. **The true shape is ELEVEN OWNED
> PLUS A STOCHASTIC SLOT — there is no twelfth defect to attribute.**
>
> **Settled on the OLD code, without the rebuild**, which is the stronger claim: three runs of identical
> code (s152's 12:12Z artefact + s153's two before-runs) returned **12 → 11 → 12 failing**, with
> `rotate-secret` PRESENT / ABSENT / PRESENT. Nothing changed and the answer moved twice.
> **Independent confirmation:** the second stochastic member, `POST /api/gdpr/consent`, is one KS-784
> had already named as a past occupant of that same slot — so the slot is the mechanism, not a story
> fitted to two runs. **NOTHING about `rotate-secret` is to be filed.**

**THE DELTA, both directions (s153, BUILT_SHA `5ffaaf396…`, 32/32 built, 0 failures):**
- **FIXED (2)** — failed in every before-run, none after: `GET /api/gdpr/erasures/{externalRef}` and
  `POST /api/gdpr/erasures`. **Their fix was already in the code; only the stale image hid it** — the
  eleventh instance of work-done-and-the-board-not-saying-so, caught in-session for once.
- **INTRODUCED (1)** — `PATCH /api/users/admin/{id}` returns **500**. Isolated to two necessary
  conditions with clean controls (valid UUID → 404; empty body → 400) and the trace names `22P02` at
  `tenant-guc.js:178`. **Attributed to `561de81ca` — KAM'S OWN KS-963 `rethrow` ruling — and the
  framing is load-bearing: KS-963 did NOT create a defect, it removed the swallow that was hiding one.
  The route never validated the id format, so the old 404 was itself a wrong answer. THE RULING IS NOT
  TO BE REVERTED.** Filed as its own P2 on the missing validation, related to KS-963 as context.
- **UNCHANGED (9)** — 7 m365/onedrive (KS-693), `teams/webhook-config` (KS-784), `wallets/verify` (KS-686).
- **Legs identical both sides** (3: 321/321 · 4: 341/341 · 8: 307/341), and run-validity 0 of 316
  operations errored on all four runs — which is what makes every "unchanged" mean anything.
- ⚠ **EVERY SUITE RUN TONIGHT RAN IN THE DEGRADED STATE**, schemathesis included — the actor
  manifest was REJECTED in all four runs. **This does not weaken the delta** (both sides identical in
  that respect, run-validity clean) **but it is a SHARED CONDITION, and a shared condition is what a
  one-sided reading misses.** Disclosed by s153 unprompted, against its own results.

## 🔴 RULED BY WEDNESDAY, STILL OPERATIVE — do NOT set `BOOTSTRAP_ADMIN_PASSWORD`
The likely one-line unblock for KS-969 is supplying it. **It is not to be supplied.** Setting a
credential in order to make a suite pass is the anti-pattern, and this one sits on the **KS-949 /
KS-964 / KS-966 rotation surface — the rotation whose entire purpose was retiring a published default.
A value that unblocks a test is exactly how a retired default comes back.** s153 declined to try it on
its own judgement and Wednesday ruled it explicitly so no successor reads the restraint as an oversight.
**The open question — what SHOULD supply it in a local test stack now the default is retired — is a
design answer, not a value, and it belongs on KS-969.**

## 🔴 KS-969 REPRODUCES, AND ITS TITLE IS FALSE
Re-run against the rebuilt images: **identical to s152 in every number** (static 4 errors, unit 48/48,
e2e 1 failed + 11 DID NOT RUN). It has NOT quietly fixed itself. **But its premise has moved:** the
title says *"provisioning is never invoked"* and **provisioning IS invoked — six times tonight — and
correctly REFUSES** to publish a manifest whose actors drifted from their requested roles.
**Steps 1-3 are the guard WORKING.** The defect is step 5: the refusal promises *"suites keep their
seeded accounts"*, every other consumer honours that, and **Playwright's admin path falls back to `''`
instead**, so a DEGRADED run becomes a FAILED one. The `?? ''` is deliberate and its intent is right
(KS-966 site 8) — **do not let the correction read as someone's mistake.**
**State the blast radius in this order: coverage 0 of 12, of which 1 failed and 11 did not run** —
*"1 failed"* out of twelve reads as 92% green and the true figure is nothing at all.

## 🟢 THE STACK IS UP AND STAYS UP — tear-down is nobody's tonight
33/33 services, migrations `applied=45 failed=0`, gateway `localhost:6882` → 200. Exactly ONE consumer
(the stack itself), enumerated with independent controls. Tear-down, recorded for whoever finally does
it and **not for the next seat**:

    docker compose -f <Secuura Blockchain>/2_Project_Files/docker-compose.local.yml stop
    docker desktop stop

**`stop`, NEVER `down`, never `-v`.** The `guardian` and `queue` orphan containers stay exactly where
they are. The 32 `secuura_slot3-*` images are the **Testing-Agent** project's, from `akto_s3` on
2026-09-07, zero containers — **not ours, not touched, not mentioned again.**

## 🔴 WEDNESDAY'S OWN ERRORS THIS SEAT — three, all in `_ledger.md`, and two are about my own instruments
1. **A brief CONDITION written to protect Kam's dashboard did not require its own control.** The seat's
   port enumerator returned a false zero on `${VAR:-default}` syntax; only a control IT added caught it.
   **The class: an artefact Wednesday writes to DIRECT a check is itself an instrument.**
2. **`boot_digest.py --check` validated only `_boot_digest.md`** while the boot prompt tells every seat
   to read `_boot_digest_by_tier.md`. Doctor could print "boot digest current" with the read-at-boot
   file stale. **Fixed and red-proofed 4 cells** (fresh 0 / missing 1 / stale 1 / regenerated 0);
   `CLAUDE.md` rule 3b corrected to require BOTH commands.
3. **I told Kam I had launched "s155". It is s153** — their `history.md` runs s148..s152. The number was
   a SCRATCH FILENAME that leaked into a sentence. **w=2 today.** Corrected to him and to the seat.

## 🟢 THREE THINGS FILED THIS SEAT that a successor should not re-derive
- **`brief-standing-lines.md` gained three entries**, all credited to the seats that found them:
  *a reviewer's instruction has a DATE* (with its exception: a PREFERENCE does not expire when state
  moves) · *a piped long build buffers to EOF, and a wedged daemon then looks exactly like a quiet one*
  · *a derived identifier nobody wrote down cannot be found by searching for what you think it is
  called.*
- **The false-absence lesson gained rule 11/12: a control must be able to fail INDEPENDENTLY.** A
  control drawn from the same family as the thing you are missing returns zero too and agrees with the
  wrong answer.
- **s152 scored 1.00** on the scoreboard.

## 🔴 WITH KAM — nothing blocks, everything has a safe default
`secuura-ks963-widen-to-preauth` (this seat's). Three are **TUESDAY's** and she has not booted:
`hpsm-credential-bearing-prd-outside-every-snapshot` · `secrev-live-pass-blocked-on-tenant` ·
`nexusai-rd369-round3-or-ship-at-the-cap`.

**Two things wait on Kam to decide whether to SAY** — that Peter's *"let it ride the next release"* on
#768 predates #908, and that his registry blocker was lifted by #760 on 2026-09-01. Both are recorded
on tickets; **neither is sent and sending is not ours.**

**WED-48 is 4 days overdue** (CypherKey Twilio token rotation, due 09-04) — the only overdue item on
the WED board (24 open, `hasNextPage: false`, 0 labelled `lesson`).

## 🔴 DO NOT RE-RAISE — settled, with the reading that settled them
- **The Studio's Docker disk.** 212 GB reclaimable against **135 GiB free** — nothing at risk. **Kam
  RULED this on 2026-09-03:** offered an agent-prune, he **declined it** and chose to handle the Studio
  himself at the desk. Card DROPPED, not overridden. Told to him once, as information, no ask.
- **F-02 SSH preflight is a FALSE ALARM.** Push proven twice; repo-local `core.sshCommand` is what git
  uses. **It does not go to Kam** — the same instruction was once given to him wrongly and is a ledger row.
- **KS-1005** — a High with a one-line fix, blocked on #872, which has no approval at head. Listed by
  s153 deliberately so it is not silently dropped. Not actionable.
- **The archive-cascade card** — closed, no card filed, all 7 inside the 61 Kam ruled `three` on.

## STANDING (unchanged)
Nothing deployed; demo `400517aaf` is INHERITED and is not asserted by anyone. **#880 is KAM'S** and
carries the KS-843 cutover precondition. 18,609-line hold on #896/#899/#900, #899 before #900. Actions
dead 19 days — every check UNAVAILABLE, never failing; **billing is Kam's access alone**, and that is an
inherited claim, not re-measured tonight. Nobody messages Peter or Stuart outside a reply to a review
they opened. No merge that makes an external commitment. **Never delete — quarantine.**
**Kam's writing rules:** the panel speaks the WHOLE message; the **ASK goes FIRST as literal steps**, or
*"no action needed"* in the first line.
