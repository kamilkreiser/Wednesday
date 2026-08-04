# Kam decision sitting — 2026-08-04

One sitting, ~30–40 min, clears 20+ items. Ranked: quick wins → time-pressured
→ posture calls → odds and ends. Freshness: NexusAI validated live today (Jira
read-only); Secuura validated live today (Linear read-only); CypherKey as of
its 08-02 card (no session since); Vision as of its 08-02 card.
Each item: the decision + my recommendation. You decide; I record + route.

## 1 · Quick wins (~5 min, clears 8 tickets)

- **RD-64 confirm + close** — your Settings-page 403 bug, fixed + deployed
  rev 69, now Release Ready (moved after my card was written). *Rec: hard-refresh
  the Settings page, fire one quick-question, close it.*
- **NexusAI Release-Ready batch (6): RD-59, RD-60, RD-63, RD-45, RD-23, RD-41**
  — all verified Release Ready just now; most are done work aging since June.
  *Rec: batch-accept 5 of them. The one to pause on is RD-41 (deploys Monday
  lead-sync creds toward a PROD go-live) — confirm Monday go-live is still
  wanted before that one ships.*

## 2 · Time-pressured (~10 min)

- **NexusAI security pair — RD-55 (RSA key + SP secrets in git history,
  In Progress since mid-June) + RD-54 (leaked LAW key, To Do).** 6+ weeks of
  real exposure. *Rec: authorize a dedicated NexusAI scrub session this week —
  I'll brief it under the new protocol; the decision needed today is only
  "yes, schedule it".*
- **Secuura trio (all In Review, blocking their board):**
  - **KS-518** — rule on the by-design question (their analysis is on the
    ticket).
  - **KS-539** — read Stuart's governing-rules doc + sign off (Peter/Stuart
    also pending; your sign-off unblocks the nudge chain).
  - **#633 repoint** (KS-551 rider) — mechanical once you nod.
- **Secuura stale-tenant-refs to-do** — sits outside Blockchain's write scope
  (Tokenomics launcher + client CLAUDE.md). *Rec: named go-ahead for me to
  brief a short Tokenomics session; it's a 15-minute fix rotting on the board.*
- **RD-61 dead ABTDEMO feed (demo dashboard empty since 1 June)** — needs the
  external fleet owner, not code. External comms = your class. *Rec: tell me
  who owns the ABTDEMO/HPAM fleet relationship and I'll draft the chase email
  for your send.*

## 3 · Posture calls (~10 min, CypherKey — as of 08-02 card)

- **Keyed digests on demo** (`OTP_ERD_ROOT_KEY`) — permanent once set (one-way
  door, flagging per go-slow). *Rec: yes — it closes the DB-breach enumeration
  finding on the env customers actually see.*
- **Android app-lock fail-open vs fail-closed** (CPKEY-163). *Rec: fail-closed
  — it's a security product; availability losing to integrity here is the
  brand promise.*
- **Twilio token rotation** — *Rec: yes, schedule with the next CypherKey
  session.*
- **CPKEY-93 store publishing** — start now or after 161/162 land? *Rec: after
  — publishing pipelines bite when the app is still moving.*
- (2-min machine task whenever at that keyboard: `gh auth login` for CypherKey.)

## 4 · Odds and ends (~5 min)

- **Vision: 3 dependabot branches** — *Rec: named go-ahead for a short VSP
  session to review/merge (mechanical, prod untouched); it also confirms the
  LEAD_BOT_API_KEY handoff while in there.*
- **RD-18 privacy package** — Put on Hold since June. *Rec: stays parked until
  the commercial track (RD-13 gating GA) moves; no action today, just confirm.*
- **Wednesday's own:** Agent Mail plan upgrade (browser; WED-8's last item —
  lower urgency now wednesday-agent@ exists, your call whether today) ·
  **T9-root CLAUDE.md sync** (found today: it's an older variant missing the
  fleet-comms section my own sessions load — one `cp` from DevMASTER's copy,
  needs your OK since it's workspace-level) · WED-10 ALDI SIM errand (whenever
  passing a store).

## Not flagged (deliberate)

myPKI — parked by your explicit call 2026-08-03, not resurfaced.
