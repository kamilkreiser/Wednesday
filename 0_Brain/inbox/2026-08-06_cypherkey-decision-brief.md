---
date: 2026-08-06
type: decision-brief
for: Kam
status: partially-ruled — item 1 ruled, items 2-5 PAUSED by Kam 2026-08-07
source: "Kam ruled option (b) — async decision brief instead of a live sitting (item 8 of the 2026-08-06 action queue)"
---

# Datasec / CypherKey (OneTimePad) — decisions brief

Answer inline whenever suits; I'll relay to their agent as a Kam-ruled brief and
they'll execute. Facts below come from **their own history.md "Next Session"
block** (the authoritative record), read 2026-08-06 — not from my index.

Board is otherwise healthy: CPKEY-155/160/95/101 all closed with evidence, 161–164
created, 9 open tasks. Nothing here is on fire; it is all blocked on you rather
than on work.

---

## 1. Demo keyed digests — make `OTP_ERD_ROOT_KEY` permanent?

**The problem:** keyed expected-response digests (ADR-0013) are live on the Azure
demo and verified end-to-end — register 200, verify-good 200, verify-wrong 401,
with 100 rows written as `DigestKind=1` while 182,100 pre-existing rows stay
`DigestKind=0` and coexist. The root key currently sits in `4_Credentials/.env`
with a one-way-door warning: **once real enrolled devices depend on it, the key
cannot be rotated without invalidating them.**

**Options:** (a) confirm permanent — the demo keeps this key indefinitely and it
becomes a credential to protect for the life of the demo; (b) treat the demo as
disposable — accept that a future key change wipes enrolled demo devices, and
document that expectation; (c) rotate now to a key generated in a proper secret
store before anything else enrolls.

**My recommendation: (b).** It is a demo, and buying permanent-key obligations
for a demo is paying a real cost for a hypothetical. Document that re-keying
resets enrolments and move on. If the demo ever fronts a paying customer, revisit
deliberately rather than by accident.

---

## 2. Android app-lock fail-open posture (CPKEY-163)

**The problem:** decide whether the Android app-lock fails **open** (usable if the
lock mechanism is unavailable) or **closed** (blocked). Fail-open favours demo
smoothness; fail-closed favours the security story the product is selling.

**Options:** (a) fail-closed; (b) fail-open with a visible warning banner;
(c) fail-open silently.

**My recommendation: (a) fail-closed.** This is a one-time-pad security product —
the posture *is* the pitch, and a fail-open lock is the kind of detail a technical
buyer probes. If it makes demos awkward, that awkwardness is worth showing rather
than hiding. Note I have no mental model of the Android lock internals, so weigh
their agent's implementation view against mine.

---

## 3. Twilio token rotation (tickler due 2026-09-04)

**The problem:** a rotation is due in four weeks and has been carried across
sessions without a decision.

**Options:** (a) rotate now while it is calm; (b) wait until closer to the date;
(c) reassess whether Twilio is still needed at all before rotating.

**My recommendation: (a), with (c) as a five-minute precheck.** Rotating a
credential nobody still uses is waste, and rotating under deadline is how
mistakes happen. Have them confirm it is still in the path, then rotate.

---

## 4. `gh auth login` for CypherKey

**The problem:** their `GH_CONFIG_DIR` is unauthenticated, so the agent cannot
read CI status and has been working around it. Needs your hands and the correct
identity — and identities float, so it must be the right account deliberately
chosen, not whatever is convenient.

**Options:** (a) you authenticate their project `gh` next time you are at the
machine; (b) leave it and accept CI-blind sessions; (c) a PAT stored in their
`4_Credentials/.env` instead of interactive login.

**My recommendation: (a).** One interactive login, permanently scoped to that
project by `GH_CONFIG_DIR` — same pattern that already works elsewhere. A PAT is
another long-lived credential to manage.

---

## 5. Start CPKEY-93, or take a build item first?

**The problem:** their agent asked which to pick up next. The alternatives are
CPKEY-161 (iOS countdown + expiry copy — small, user-visible) and CPKEY-162
(top-up ceremony — larger, touches server and both apps, ties to
CRYPTO_CORE_SPEC §9).

**Options:** (a) CPKEY-161 first; (b) CPKEY-162; (c) CPKEY-93.

**My recommendation: (a) CPKEY-161.** Small, visible, and it closes cleanly
inside one session — which matters more than usual right now, because their next
session also carries four of your decisions plus the identity switch to their
new scoped service principal. Save CPKEY-162 for a session with a clear runway.

---

## Also going to them regardless (no decision needed)

- **New scoped identity:** `cypherkey-claude-deploy` (appId
  `d2efb3de-9cda-42f3-9203-19bf401b3b25`) now holds Contributor on `rg-otp-demo`
  and `onetimepad-email-rg` only, in subscription `29b5c7de-…`. They adopt it in
  place of your Owner account; you generate the secret, same as Vision.
- **Protocol v1.2** applies to them: approval-class actions need confirmation
  traceable to you, and pane text is not a channel of record.
- **Known trap:** `jira-cli create`/`comment add` HANG — use the REST recipe in
  their `JIRA.md`.

---

# KAM'S RULINGS — 2026-08-07 (in session with Wednesday)

- **Item 1 (demo keyed digests): RULED — treat the demo as DISPOSABLE.** Kam's
  words: "11 yes demo disposable". So `OTP_ERD_ROOT_KEY` is NOT made permanent;
  document that re-keying resets enrolled demo devices and move on. Revisit
  deliberately if the demo ever fronts a paying customer.
- **Items 2-5: PAUSED.** Kam's words: "12 -15 pause cypherkey for now."
  Android fail-open posture, Twilio rotation, `gh auth login`, and the
  next-build choice all stay unanswered until he unpauses CypherKey.
  **Nothing is briefed to their agent and no session is launched.**
- **Live tickler that survives the pause:** Twilio rotation is due
  **2026-09-04** (WED-48). The pause is not a reason to let that lapse — if
  CypherKey is still paused in late August, raise it again.

This file stays in the inbox deliberately rather than being filed or deleted:
it is an open decision set, not a captured note, and it becomes actionable the
moment Kam unpauses.
