# Delegation brief — Peter consent window + pre-approved merges/deploy

From: Wednesday (coordination) · To: the Secuura/Blockchain Claude session
Date: 2026-08-04 · Status: APPROVED by Kam 2026-08-04 (in-session, after review)
· Re-dispatched ~14:00 with v1.1 plan-confirmation routing after the first
session was closed early (see "Re-dispatch note" + amended Questions section)

## Re-dispatch note (14:00)

The earlier session (launched ~13:40) was closed shortly after its plan was
confirmed. **Before executing, verify what (if anything) it completed** — check
git (were #641/#642 merged? anything deployed?) and Linear states, then resume
from wherever reality actually is. All items below are idempotent: skip
what's already verifiably done, do the rest.
Protocol: Wednesday's delegation standard (verifier, round cap, wider/deeper)
+ **first live outing of the question-routing rule** (see "Questions" below —
also now in the workspace CLAUDE.md fleet-comms section, Kam-approved today).
Wednesday never edits Secuura files; this session executes.

---

## Priority 1 — Peter's consent window (time-critical: closes EOD today)

**Background (verify before acting — my summary is a mental model, not truth):**
The S↔K ownership contract (`Blockchain/Dev/docs/S-K-OWNERSHIP-CONTRACT.md`,
PR #601, merged `82b5e0df5`) carries sign-off asks to Stuart and Peter
(KS-480 comment 2026-07-29: Stuart §4/§6/§8, Peter §5/§6), with the project's
silence-consent rule attached. Your own 08-04 wrap tracks the outstanding set
as "Peter §4/§5, window closes EOD 2026-08-04". **First step: re-derive the
exact outstanding sections + deadline from KS-480 and any replies received
(board comments, mail) — your record is authoritative, not my paraphrase.**

**Task:**
1. Check for any response from Peter (KS-480 thread, PR #601, mail).
2. **If he responded:** triage per the pre-answers below.
3. **If silent:** send one final same-day nudge (comment on KS-480 @peter +
   your usual channel) stating the window closes EOD today and silence = consent
   on the outstanding sections per the standing rule — then, after EOD, record
   consent-by-silence on KS-480 with the evidence trail (ask date, nudge date,
   rule citation). The §10 ② build itself is NEXT-session work; today is about
   closing the window cleanly.

## Priority 2 — Pre-approved mechanical work (from your own wrap)

**Task:** merge PR #641 + PR #642 (both one green check from merge at your last
wrap; **Kam pre-approved the merges + combined deploy** — recorded in your
08-04 wrap) → ONE combined VM deploy → demo verify → close KS-555/556/557 with
receipts.

**Context (paths, not pasted content):**
- KS-555/556/557 in Linear; PRs #641/#642 in your repo.
- KS-560 tracks the 11 known browser-tier e2e residuals — they are NOT
  blockers for this deploy.

## Priority 3 — only if time allows

- Stuart nudge: PS-498 post-deploy results + KS-539 sign-off — **nudge only**,
  no building on his behalf.

## Out of scope today

KS-560 residuals, KS-559 dep sweep, and all open Kam decisions (KS-518 by-design,
#633 repoint, KS-539 sign-off, stale-tenant refs) — Wednesday is packaging those
for a separate Kam sitting.

## Constraints

- Secuura tenant/identity only, per your launcher. No prod beyond the
  pre-approved combined VM deploy to demo.
- Re-verify PR state before merging (green checks may have gone stale since
  your wrap — validate, don't trust the record).
- No-skip applies: a failed deploy-verify is rolled back per your runbook and
  reported, never pushed through.

## Pre-answered questions (so you don't need to ask)

- **Which env?** The ONE combined VM deploy to demo — pre-approved. Nothing
  else deploys today.
- **Merge order?** #641 then #642 (or your repo's convention); single deploy
  after both are in.
- **New e2e failures post-merge?** The 11 KS-560 residuals are known — not
  blockers. Anything NEW introduced by these merges is a regression: fix
  before deploying (no-skip).
- **Peter replied with minor/clarifying §5–§6 comments?** Fold them, note on
  KS-480, proceed.
- **Peter replied with a MATERIAL contract change** (e.g. rejects the
  cross-org 403 semantics or the rotation posture)? That is approval-class —
  pause that thread for Kam, continue Priority 2 meanwhile.
- **Codex cross-model review on these merges?** Not today — the pilot is done
  and the protocol is being revised (prompt-fidelity finding, thank you for
  honest logging).

## Questions the brief doesn't answer — NEW ROUTING (first live outing)

Do NOT ask Kam by default. Email `wednesday-agent@agentmail.to`, subject
`[Secuura/Blockchain -> Wednesday] QUESTION: <topic>`, body: Context (1–3
lines + file paths) / one Question per mail / Meanwhile (`continuing with <x>`
or `BLOCKED`) / Needed-by. If blocked, re-check your inbox every ~3 minutes
for `[Wednesday -> Secuura/Blockchain] ANSWER: <topic>` (topic mirrored
exactly). After ~15 minutes with no answer, proceed on the safest
interpretation and record that in your wrap — UNLESS the item is
approval-class (prod/demo-affecting beyond the pre-approved deploy, money,
external comms beyond the Peter/Stuart nudges above, anything irreversible),
which ALWAYS pauses for Kam. **I am monitoring the inbox every 3–5 minutes
while your session runs.**

**Plan-confirmation (v1.1 — NEW since the first dispatch):** this brief is
Kam-approved, so send your boot plan-confirmation to ME as a QUESTION mail
(topic: `plan confirmation`) instead of pausing your session for Kam. I
confirm against the approved brief within a poll cycle. Pause for Kam ONLY
if your plan deviates from this brief (new scope, approval-class actions).
Your previous session's plan was already confirmed (proceed 1+2 in parallel;
KS-560 = triage notes only; KS-549 nudge-only; no-skip on new e2e
regressions) — if your plan matches it, treat that confirmation as standing
and just say so in your plan-confirmation mail.

## Definition of done (the verifier — checklist, score = fraction met)

1. Consent window closed cleanly: Peter's reply triaged OR nudge sent +
   consent-by-silence recorded on KS-480 with the evidence trail.
2. #641 + #642 merged, checks green at merge time.
3. Combined VM deploy executed + demo verified (your standard verification,
   evidence in the wrap).
4. KS-555/556/557 closed with receipts.
5. Wrap email per Step 2d (to wednesday-agent@), including: consent outcome,
   deploy evidence, and — new — a line for any QUESTION mails you sent and
   whether the answers unblocked you (this scores the new routing mechanism).

**Round cap: 3.** Verifier not green after 3 refinement rounds → stop, report.
