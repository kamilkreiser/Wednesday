# SEAT A successor brief — Secuura / Blockchain (Platform K), 2026-09-07 morning

You are a fresh seat. Your predecessor **s141b wrapped 2026-09-07 ~01:21 and closed its pane**; its
handover is in your OWN tree at `5_Project_History/HANDOVER-s141b.md` — read it. Seat B (s142) also
wrapped (~01:41) after completing the OAuth cluster and KS-729 leg 1.

## BLUF
**Item 1 is a P1 security fix Wednesday has RULED and is commissioning now: the F5 `//` bypass, fixed
as the KS-858 class — one edge normalisation, `//`-only, path-only, above every predicate.** It is
your first priority. The ONE thing that may interrupt it is a verdict from the two QA gates running
against `#876` and `#882` right now — a NO GO there is inserted ahead of item 1; anything else waits. Nothing merges, nothing deploys,
nobody outside the team is told anything.

## 1. QUEUE

### ITEM 1 (P1, start here) — F5 / KS-858: normalise `//` once at the gateway edge
**Wednesday RULES option A** from seat B's own four options (its mail
`[Secuura/Blockchain -> Wednesday] F5 items 1+2 DONE`, 2026-09-06T14:43:04Z — read it in full before
you start; it is the source, this brief is a pointer at it).

`scope:` KS-858 is the CLASS ticket ("a predicate mounted above a catch-all proxy, walked around by
`//`, proxy normalises on the way out"). F5 is its **second confirmed instance**; KS-843's gdpr
`//erasures` hole was the first. This item closes the class at one choke point — it is NOT scoped to
the eight limiter mounts, and you should expect it to close scope gates and the gdpr shape too.

**Why A and not B/C/D — Wednesday's reasoning, so you can argue with it:** B (fail-closed 400) is
smaller and cannot create a bypass, and it is the fallback if A proves unsafe. C is refused outright —
per-predicate matching is the trap KS-843 F-9 and KS-858 already record. D alone ships no code. A is
chosen because the class has two confirmed instances already and closing instances one at a time is
exactly what KS-858 exists to stop, and because **there is a proven in-repo template**: `proxy.ts:682`
already collapses repeated slashes scoped to `/api/gdpr` and restores `req.url`. **If you find A is
not safely implementable, say so and take B — that is a technical judgement and it is yours; mail
Wednesday with the measurement, do not silently switch.**

**Constraints on the implementation, and these are the finding, not decoration:**
1. **`//` and repeated separators ONLY. PATH ONLY, never the query string.** Do not fold in `%2F` or
   `%XX` decoding and do not fold in case (case is KS-801). Seat B measured that the other three
   spellings (`%XX`, `;x=1` matrix, `%2F`) **skip the limiter but are 404'd by real express 4.22.2**
   at the backend — they are curios, not reachable exploits, and touching them in this change would
   widen the blast radius past what has been measured.
2. **Above every predicate**, so one middleware covers limiters, scope gates and the gdpr class.
3. **Do not double-apply** with the existing `/api/gdpr`-scoped normalisation at `proxy.ts:682` —
   establish what happens when both run, and say so.

**Red-proofs required (each must red ONLY its own clause):**
- (i) all 8 limiter mounts: `//` now HITS the limiter. Positive control first — each mount exhausted
  with its OWN distinct 429 message, the way seat B did it. The 8 are login, register,
  forgot-password, refresh, password-reset, verify-email, `/api/auth/mfa`, `/api/users/me/mfa`.
  Six of them are UNAUTHENTICATED under the public `/api/auth` proxy.
- (ii) the three curio spellings are **UNCHANGED** — still not reaching a guarded op, no new
  reachability created by your change.
- (iii) **query strings are untouched** — a `//` inside a query value survives byte-identical.
- (iv) the gdpr `//erasures` shape (KS-843) is closed by the same middleware.
- A green baseline before every tamper and again after every byte-identical restore. A hash proves
  the bytes; only a run proves the file still works.

**A NEW BRANCH, off `develop` @ `306d0db923183f3b62b053f0242549e37bdf362c`** (read by Wednesday with
`ls-remote` at 06:1x in the same action as writing this line). **Do NOT push to `#876` or `#882` —
both are under an ACTIVE QA gate right now** (see §3). End at READY FOR QA; do not merge.

### ITEM 2 (same visit as item 1) — the ticket dispositions the measurement implies
Wednesday's triage ruling (v1.3 scope: ticket triage, priority, status are Wednesday's):
- **KS-946 → Blocker**, re-priced on the `//` vector confirmed across all 8 mounts; the other three
  spellings recorded as curios with seat B's express-4.22.2 measurement.
- **KS-858 → P1**, and it carries F5.
- **KS-733 must NOT close as "MFA is now throttled."** Its own remedy (mounting the limiter on
  `/api/users/me/mfa`) is real for the canonical path and `//`-bypassable like the other seven. Keep
  it open with the bound stated, or gate its close behind item 1 landing.
- **HELD, do not post:** seat B's ready-to-post KS-946 *result comment* stays held. Disclosure to
  Peter and Stuart is Kam's card and it is open. Nothing about F5 goes on a ticket a client human
  reads until Wednesday relays his word.

### ITEM 3 (inserted at priority when it lands) — the two live gate verdicts
Wednesday will mail you each verdict. Fix rounds go **on the PR's own branch**, and only once the
gate against it has REPORTED. Round counting under Kam's two-NO-GO cap applies per class.

**SUPERSEDES the ordering in Wednesday's 2026-09-06T15:11Z GO and its 15:01Z ACK to s141b** ("next =
KS-577 then KS-762", and "KS-729/KS-664 for the successor"). KS-577 (#880) and KS-762 are now on
Kam's desk, not in this seat's queue; F5 takes item 1.

### ITEM 4 (only when 1–3 are dry) — the standing P2 table
Your predecessor's standing queue in `HANDOVER-s141b.md`. **Do NOT start KS-739** (it opens
"Awaiting Kam's decision"). **KS-729 leg 2 and KS-664 are on Kam's desk, not yours** — leg 2 is a
@meshsdk MAJOR bump needing its own window; KS-664's fix is an unpushed branch living only on the
Ubuntu dev VM.

RULED BY KAM, NOT YET IN AN ARTEFACT
Five rulings are ruled-but-undelivered for this project. **None of them is an action for you** — each
is a Kam-side or a deliberate-wait item, listed so the record is complete and so you do not re-raise
them. If any becomes actionable inside your work, mail Wednesday; do not act on it.
- secuura-ci-billing: "wait" (2026-08-26) -> must land in the KS billing ticket's comment, once Kam's org billing access resolves. Kam-side; nothing for you.
- secuura-agent-github-identity: "identity" (2026-08-26) -> must land in the agent-identity ticket's comment, once Kam creates the GitHub identity. Kam-side org action; nothing for you.
- secuura-dependabot-triage: "close-and-rescope" (2026-09-01) -> must land in the Dependabot config PR / the triage ticket. It is Peter's repo; nothing for you.
- secuura-ks229-disclosure-mailbox: "later" (2026-09-02) -> must land in KS-229's comment as a dated deferral. Deliberately deferred; nothing for you.
- secuura-ps-759-760-merge-owner: "kam-merges" (2026-09-05) -> must land on PS #759 and PS #760. Platform S is OUTSIDE this seat's scope; nothing for you.

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- **2026-09-07 06:3x (this brief): F5 is fixed as option A — `//`-only, path-only, above every
  predicate, implemented as the KS-858 class fix.** B is the named fallback on a measurement.
- **2026-09-07 06:3x: TWO QA GATES ARE LIVE — `#876` @ `a0ad0a084` and `#882` @ `bd2b761a0`.
  Push nothing to either branch.** On 2026-09-06 a push to a branch under gate made a tier-1 verdict
  describe a SHA the head had moved past; that cost a whole pass. **New work goes on a NEW branch;
  if you believe a fix belongs on a gated branch, mail Wednesday and wait.**
- **2026-09-05 23:24 (to s133, still binding): do NOT narrate KS-823 in a published contract — a
  defect is not a guarantee.** Same rule generalises: no open-defect narration in any published
  artefact.
- **2026-09-06 (Kam, panel 09:42 + corrected 10:24): every NEW or UNASSIGNED Platform K ticket is
  assigned to OUR account. A ticket ALREADY assigned to Peter or Stuart stays theirs** — moved only
  on Kam's word, per ticket, never by a predicate.
- **2026-09-06 (Kam, panel 09:42): ticket CREATION aggregates** — one larger ticket per logical path
  with its items as a checklist or sub-issues, never three or five separate tickets for one line of
  work. "Within a logical path" is the limit.

## 4. HOLDS — none of these moves without Kam
- **No merge. No deploy. The demo box is never touched.** Local only.
- **No external communication to any human outside the team** (Peter, Stuart, anyone). Client-facing
  communication goes ON THE TICKET, posted by you under your board authority — and **F5 specifically
  is held**: nothing about it reaches a ticket a client human reads until Wednesday relays Kam's word.
  **The extranet is INPUT ONLY** — never post there.
- **Handovers to Peter or Stuart are TEST BLOCKS** (review-stream parent · the PRs in the block · the
  ONE pass that proves it · the one thing the human does), never a list of PRs. A PR that fits no
  block is stated as the exception with its reason.
- **Never delete — quarantine by rename.** No `rm`, no `--delete`, no discarding uncommitted work.
- **Restore every tamper by INVERSE EDIT verified with sha256, then RE-RUN the suite.**
- **A control must be able to fail.** A red-proof must break ONLY the guard it is for; a green
  baseline proves it can pass for the right reason. Count first (`grep -c`) — never call a truncated
  list complete.
- **A measurement travels; an explanation of it does not.** When you relay someone's claim, carry
  their sentence verbatim including its hedges, and label anything you add as yours.
- **zsh word-splits.** Your predecessor hit this FIVE times in one session (branch names, `Refs`
  trailers, first review requests, submitted reviews, restore loops). Quote every expansion; prefer
  python over shell loops for anything that walks a list of ids.

PROVENANCE:
- develop @ 306d0db923183f3b62b053f0242549e37bdf362c, #876 @ a0ad0a084e7ecdd772d106740a283f738ccdadf7, #882 @ bd2b761a0fc9deaf1b8cbd8a5bd16db492a180f4 | `git ls-remote origin` run from Wednesday's own seat at 06:1x | read 2026-09-07
- The F5 measurement (8 mounts, // reaches the handler), the four fix options, the real-express-4.22.2 backend 404 result, and the two instrument corrections | seat B's (s142) mail `[Secuura/Blockchain -> Wednesday] F5 items 1+2 DONE`, 2026-09-06T14:43:04Z, quoted not paraphrased | read 2026-09-07
- The proxy.ts:682 gdpr-scoped normalisation template — NOT re-read by Wednesday, verify it yourself before building on it | seat B's mail of 2026-09-06T14:43:04Z | read 2026-09-07
- KS-946, KS-858 and KS-733 current states — NOT read by Wednesday in this action, read them from the board before changing any of them | unmeasured | read 2026-09-07
- The five undelivered ruled cards in section 2 | `decision_queue.sh list ruled --undelivered secuura-` run from Wednesday's seat | read 2026-09-07
- The seat A standing P2 table, KS-739's hold, KS-729 leg 2 and KS-664 | s141b's wrap mail 2026-09-06T15:21:24Z and its HANDOVER-s141b.md in the project's own tree | read 2026-09-07

## 6. PROTOCOL
Plan confirmation to `wednesday-agent@agentmail.to` before you build, subject
`[Secuura/Blockchain -> Wednesday] QUESTION: plan confirmation`. Mid-round questions go to Wednesday,
not Kam. Wrap at your rhythm-§2 band with a resumable handover in your own tree. **If an instruction
from Wednesday looks wrong, say so** — two seats corrected Wednesday last night and both were right.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-07 06:15
