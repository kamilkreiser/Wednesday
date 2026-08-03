# Fleet boards digest — first sweep

Swept: 2026-08-03 (WED-28 first run) · Read-only, per the recorded grant
([[../learnings/2026-08-03_grant-readonly-tracker-access]]).
Trackers: Datasec → Jira (CPKEY, MYP, RD; VSP has creds but no project key —
work rides on handoff docs) · Secuura → Linear (KS/PS) · Wednesday → Linear (WED).

---

## ⚡ KAM DECISION QUEUE (aggregated — the point of this digest)

**In flight right now:** Secuura sitting (A1 KS-547 role gate · A2 Stuart's
KS-480 trio · A3 KS-551 GH_REF · A4 pricing/KS-244) — being cleared live 08-03.

**Next queue, ranked by Wednesday:**
1. **NexusAI security pair (aging):** RD-55 (High, In Progress since mid-June —
   RSA private key + old SP secrets in git history, rotate + scrub) and RD-54
   (rotate/confirm-dead leaked Log Analytics key). Security debt with real
   exposure, 6+ weeks old. Decide: schedule the scrub session.
2. **NexusAI "Release Ready" stack (6 tickets):** RD-60, RD-63 (maintenance-tab
   false-healthy), RD-59 (security dep batch), RD-23, RD-45, RD-56, RD-41 —
   work done, awaiting ship/merge call. One sitting clears them.
3. **NexusAI RD-61 (High, updated today):** Global Variables LAW ingest dead
   since 06-01 — demo dashboard empty. Demo-facing; decide priority.
4. **CypherKey decisions (from 08-02 card):** enable keyed digests on demo
   (OTP_ERD_ROOT_KEY — permanent once set) · Android app-lock fail-open posture
   (feeds CPKEY-163) · Twilio token rotation · `gh auth login` · green-light
   CPKEY-93 (store publishing)?
5. **NexusAI RD-13 (High):** DEV offer in Partner Center + $0 test purchase —
   gates the whole commercial-GA horizon (H1, RD-6).
6. ~~Portfolio question — myPKI~~ **ANSWERED (Kam, 2026-08-03): parked
   deliberately.** Do not flag; drop from future decision queues until Kam
   reactivates.
7. **Wednesday board:** WED-8 (inbox limit: delete `secure_test` or upgrade
   plan) · WED-10 (ALDI SIM errand, whenever passing a store).

## Per-board state

### Datasec / CypherKey (Jira CPKEY) — active, healthy
27 open. Fresh build queue from 08-02: CPKEY-161 (iOS activation countdown),
162 (top-up ceremony dead-end), 163/164 (platform parity passes). Then 157/156
(attestation, PQC). Long-tail: 15 "In Progress" epic-style tickets untouched
since June — board hygiene candidate (their agent's call, not mine). Late-stage
security/compliance parked: pen test (44), red-team (45), IRAP (46).

### Datasec / NexusAI (Jira RD) — active TODAY, decision-heavy
30 open; 6 tickets touched 08-03 (a session ran today). Shape: a large
Release-Ready stack awaiting Kam, the security pair (RD-55/54), demo-data
outage (RD-61), and the long-range commercial/compliance track (SOC2 RD-20/28,
pen test RD-21, hires RD-22/31, marketplace RD-13/30/34).

### Datasec / myPKI (Jira MYP) — PARKED (deliberate, Kam 2026-08-03)
30 open. Priority core: accuracy/liveness research cluster (MYP-1/5/13 Highest,
MYP-20 macOS app Highest In Progress). Parked by Kam's explicit call — no
flagging in sweeps until reactivated.

### Datasec / Vision Sales Portal — no board
Jira creds but no project key. Open items live on the 08-02 index card:
3 dependabot branches, LEAD_BOT_API_KEY handoff confirmation.

### Secuura / Blockchain (Linear KS/PS) — most active; sitting in progress
28 active Kam-assigned (18 In Review pre-sitting), backlog 52 (12 High).
Detail in today's sitting brief. Watches: Peter's §4/§5 silence-consent window
closes EOD 08-04; Stuart+Peter KS-539 sign-offs outstanding.

### Wednesday (Linear WED) — own board
Open: WED-6 (discovery queue), 7 (full sweep — partially served by this
digest), 8 (inbox limit), 10/11 (WhatsApp path), 13, 16 (6am scheduler), 18
(industry scan), 20 (pilot — LIVE today), 22 (council), 26, 27 (comms fabric),
28 (this mechanism). Done today: 17, 19, 21, 24, 25.

## Sweep notes (for WED-28 refinement)

- Jira REST v3 `/search/jql` works clean with per-project creds; ~1 s/board.
- Decision detection is heuristic (state="Release Ready", DECISION in title,
  index-card notes) — a shared label convention (`kam-decision`) across boards
  would make the queue mechanical; needs per-project agents to adopt (proposal
  for the fleet, via Kam).
- Next sweep: fold in VSP handoff items; check Tokenomics (no tracker found);
  add "changed since last sweep" diffing once there are two sweeps to diff.
