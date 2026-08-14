# Kam decision sitting — 2026-08-14 (live queue at the top; 08-04 archive below)

Format per Kam's 2026-08-06 rule: **Client/Project · problem · options · my
recommendation.** He is unwell today, so this is built to be ruled in one pass.

---

## OPEN — needs Kam, ranked

### 1. Datasec / HPSM — **E14: does an executed CSPA exist, and can we read it?**
**Problem:** the CSPA sits at **rank 1 in SOW §3, above the SOW itself**, and it is
not in our corpus. It now gates four separate threads: the money half of the
reconciliation, X5's precedence question, X6's payment-terms deferral, and whether
the reconciliation day is worth commissioning at all.
**Options:** (a) it exists and Kam can share it → we read it and four threads unblock ·
(b) it exists and cannot be shared → we mark those four as permanently
assumption-based and say so in the Monday pack · (c) none was ever executed → that is
itself a finding and changes the precedence argument.
**Recommendation:** answer (a)/(b)/(c) — five minutes, highest-value open item across
the programme for five sessions running.

### 2. WED — **WED-108 (P1): re-send your signed v1.3 grant to each per-project inbox**
**Problem:** the per-project migration cut every migrated agent off from `coagent@`,
where your grant lives. **Two projects have now independently confirmed it** (Secuura
s30, HPSM s21) — both are running on provenance-by-history rather than a check they
ran today.
**Options:** (a) re-send the signed grant to `secuura-blockchain@`, `datasec-hpsm@`,
`datasec-nexusai@`, `datasec-vision@` · (b) leave it and accept that agents hold work
whenever an approval-class item appears.
**Recommendation:** (a). **Your hand only — a forward from me authorises nothing**,
and the agents have been told to refuse one if I ever offer it.

### 3. Datasec / Vision — **Will's PoC threshold: >5 or ≥5, and does 10 get encoded?**
**Problem:** Will writes both *">5 devices"* and *"less than 5 devices"* in one
paragraph, and *"really should be 10+ in a perfect world"*. The readings differ only
at exactly 5 devices.
**Options:** (a) **≥5** — a deal of 5 is acceptable, 1–4 raises the advisory ·
(b) **>5** — 5 itself raises the advisory · (c) also encode 10 as a second threshold.
**Recommendation:** **(a) ≥5**, because *"less than 5"* is his operative exclusion,
which puts 5 on the acceptable side. **Reject (c)** — he calls 10 a perfect world and
in the same breath says PoCs get insisted on with a couple; a live 10-gate rebuilds
the over-strict behaviour we are removing. The agent is proceeding on ≥5 with the
value in **one named constant**, so your ruling is a one-line change either way.

### 4. Datasec / Vision — 🔴 **the LIVE tool is still dropping PoC lines right now**
**Problem:** on a deal of 1–4 devices, ticking the PoC box **silently drops the PoC
line** — no charge, no flag, nothing on screen or in the PDF. **Live since 2026-08-07
19:16 (`49b3dfc`, v2.08) and STILL LIVE** — the fix is on main as v2.20 but **not
deployed**; `hpas-quickquote.azurewebsites.net` is running v0.3.2-tool2.19. Window so
far: **6 days 16 hours and open.**
**Two things that make it worse than it first looked:** the field seeded to
`min(dealDevices, 5)`, so **ticking the box was enough** — no unusual input needed —
and that is **exactly Will's population**, the small deals he wrote in about. Before
v2.08 the control was *disabled*, so an AM could see the rule refusing them; now they
tick it and get nothing back with no signal at all.
**Not a reversal by anyone:** collateral from the pricing-engine extraction — the
floor went into the engine against the wrong number and the UI's correct deal-size
gate was deleted as redundant in the same commit. **Nobody decided this.**
**Options:** (a) deploy v2.20 now, then tell Will with the dates · (b) tell Will now,
deploy when convenient · (c) deploy quietly and say nothing.
**Recommendation:** **(a).** The deploy is the part that stops the bleeding and it is
one action; the telling is yours and reads far better alongside "and it is already
fixed in the field". **Not (c)** — he found the rule himself and will connect the two.
**Whether any real quote was affected is unknown** — that needs production data and I
have not gone near it. **External comms and the deploy are both your class; I have
done neither.**

### 5. Secuura / Blockchain — **the Kintsugi deploy, now ONE decision covering thirteen changes**
**Problem:** thirteen merged-but-unshipped changes sit behind the hold, **four of them
security fixes** — including KS-617, which restores gateway **session revocation**
that is currently not running on demo. The backlog sweep cannot close any of them
without asserting a fix is live when it is not.
**Options:** (a) lift the hold and deploy the queue · (b) keep the hold and accept
that the demo runs without those controls, with the tickets openly labelled
"awaiting deploy" · (c) deploy a security-only subset.
**Recommendation:** ruling needed rather than a specific option from me — this is a
product/environment call, not a technical one. What I would flag: **the longer the
queue, the riskier the eventual single deploy**, and KS-617 is a control people may
assume exists.

### 6. Secuura / Blockchain — **the consolidated backlog residue** (arriving today)
The agent is sweeping 87 backlog items plus 16 In Review stalls, closing and
archiving what is genuinely done. **Everything that cannot close because it needs your
decision arrives as ONE list**, each with the question in a line and its
recommendation. Not ready yet; it will land in its wrap.

### 7. Standing, unchanged
**Amplify HPSM-25 — overdue as of today.** · WED-107 (five legacy org-wide AgentMail
keys spanning every inbox) · KS-486/KS-621 org boundary-or-label · KS-624/625
by-design-or-remediate · F-1 WAF · F-5 CAPTCHA · KS-386 retention · KS-329 · KS-256 ·
verify-file 415 · KS-130/169/229 · the HP correction bundle (X1–X5 + X6 + CT §18
carriage) · four modelled revenue streams with one contract vehicle.

### 8. Awareness only — no decision
- Secuura B-3 would have reset your real `kam@secuura.ai` SYSTEM_ADMIN account to a
  repo-published password. Fixed in #686, unshipped.
- **PowerPoint-opens check** on the Monday deck — 30 seconds, still unverified.
- **Local Docker cannot pull base images on this Mac** (KS-631) — bounds what any
  local agent session can verify. CI unaffected.
- The 06:00 wake will keep dying until Fable-5 credits renew (~2 days), per your
  ruling to leave the pin.

---

## ARCHIVE — 2026-08-04 sitting

## RULINGS (live, batch of 5 format per Kam)

**Batch 1 (ruled ~15:10):**
1. RD-64 — fix confirmed by Kam → CLOSE.
2. Release-Ready batch (RD-59/60/63/45/23) → BATCH-ACCEPT (Kam: "go with
   your call").
3. RD-41 → PARK until the commercial track moves (option c).
4. RD-55/54 security pair → SEVERITY DOWNGRADED by Kam's context: NexusAI is
   a DEMO system; commercial model = clients deploy via Azure Marketplace
   with their own keys. So git-history keys are demo-scoped. Fold into next
   routine NexusAI session as hygiene — no dedicated scrub session. (My
   "real exposure" ranking corrected — update boards-digest framing.)
5. KS-518 → accept by-design, CLOSE.

**Batch 2 (ruled ~15:15):**
6. KS-539 → (c)+(a): Wednesday distils Stuart's doc to a half-page
   (read-only), Kam rules on the summary. → Wednesday task after sitting.
7. #633 repoint → NOD. → consolidated Secuura brief.
8. Stale-tenant-refs → NAMED GO-AHEAD for a Tokenomics micro-session.
9. RD-61 → work closely with Kam; SCHEDULED follow-up TOMORROW 08-05
   (→ WED ticket + morning-briefing slot).
10. CypherKey keyed digests on demo → YES, enable. → consolidated CypherKey
    brief (one-way door acknowledged).

**Batch 3 (ruled ~15:25; Kam re-confirmed 10=a in between):**
11. Android app-lock → (c) FAIL-CLOSED with a documented recovery path
    (re-auth, not bypass). → consolidated CypherKey brief (CPKEY-163).
12. Twilio rotation → (b) DEFERRED ONE MONTH → due 2026-09-04 (goes in the
    CypherKey brief as a dated item + Wednesday follow-up tickler).
13. CPKEY-93 store publishing → (a) AFTER 161/162 land.
14. Vision dependabot ×3 → (a) NAMED GO-AHEAD for a short VSP session
    (+ LEAD_BOT_API_KEY handoff confirm).
15. RD-18 → (a) stays PARKED until commercial track (RD-13) moves.

**Batch 4 (ruled ~15:30 — Kam said "start actioning" after seeing recs;
recorded as recs-accepted, flagged as Wednesday's reading):**
16. T9-root CLAUDE.md → (a) SYNC from DevMASTER (backup kept — reversible).
17. Agent Mail upgrade → (b) DEFER until a 4th inbox is needed; WED-8 closes
    with the deferral noted.

**SITTING COMPLETE — 17/17 ruled. Execution log below.**

Execution: rulings collected through the sitting; ONE consolidated brief per
project dispatched at the end (avoids a session-launch per batch).

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
