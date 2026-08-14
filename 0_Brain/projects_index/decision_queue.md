# Kam decision sitting — 2026-08-14

> **Status at ~12:5x (fresh session).** The Kintsugi deploy you authorised is
> **RUNNING** — Secuura session 34, launched as this session's first act, demo only.
> **Items A, B, 1, 2, 3, 4, 4b, 5b and 7 below are still open and still yours.**
> Nothing here has been actioned on your behalf; items 5 and 6 are struck through
> because you ruled them.
> **The two most time-bound: item 4 (a live defect in Will's tool, now in its seventh
> day) and HPSM-25 Amplify, which was due today.**

## ✅ RULED 2026-08-14 ~12:4x — all 18 backlog decisions CLOSED
Twelve accepted as recommended. The six that needed him:
- **KS-621 — `organization` IS A SECURITY BOUNDARY.** Net-new enforcement; neither
  layer scopes by org today, so this is a model to build and **it changes the schema**.
  Design comes to me before any code.
- **KS-239 — SIGNED OFF.** Erasure irreversible and complete; downstream GDPR tickets
  can stop citing it as open.
- **KS-386 — a DATA-MODEL ruling, not a retention answer.** *"we do not hold PII. you
  need to record what was done (typically with partners) to what level, etc. not the
  actual data"* — Platform K should not hold the KYC images at all; it keeps the
  **attestation**. Split: design + stop-storing is the agent's; **disposal of existing
  data is irreversible and stays Kam's explicit signature.**
- **KS-263 — deferred to next week.**
- **KS-339 — Kam discusses access with Phil and Steve himself**; Stuart worked on it
  last. Nobody contacted.
- **KS-101 — priority DOWN**: Platform K does not need the Stripe consolidation, no
  near-term commercialisation. Kam requests the info from Stuart; external contact is
  his and I have contacted nobody.

**Also ruled: the Kintsugi hold is LIFTED and the deploy is authorised** (demo only;
production untouched and still his signature).

> ✅ **DONE 2026-08-14 05:07Z — cutover complete, 33/33 healthy, `cardanoMode: REAL`,
> zero build failures across 30 images.**
> 🔴 **CORRECTION to what I told you: revocation was NOT off beforehand.** My brief and
> this queue both said KS-617 "restores gateway session revocation, currently off on
> demo". **It was on.** The agent measured it: revoked tokens returned 401 on covered
> endpoints both before and after. **What was missing is the guarantee that a Redis
> outage cannot silently switch it off** — now proven over a 45-second outage with both
> controls. A narrower and true claim. The wrong sentence came from my own project's
> notes and I relayed it without checking it against the system.
> **Also less precise than I reported: the "seven already live" split** rested on a
> marker sweep that grepped only `/app/dist` while three fixes live in a shared package.
> The old images are gone, so it cannot be re-run. **Five are proven by behavioural
> probes taken before cutover; the rest are inference and the board will say so.**

---

## STILL OPEN — needs Kam

### 🔴 A. Secuura / Blockchain — **five findings that are one defect: signals firing into channels nobody reads**
Filed by session 33. **Four of the five were found by reading a red that already
existed** — nothing was hidden. Three are time-sensitive.

- **KS-636 — a CRITICAL CVE in the base image of all ten services, unread for 13
  days.** The watchdog flagged `node:24-alpine` CVE-2026-59873 on **2026-08-01**. It
  worked. Its failure — which its own header calls the reminder — went unread.
- **KS-637 — the nightly Internal Audit has failed 40 runs straight** (2 successes in
  its last 100), dying at "Boot dev stack" before any job runs. **DAST,
  tenant-isolation, licence-compliance and the Aiken contract tests run NOWHERE
  else.** Tenant isolation matters especially now: **you have just ruled `organization`
  a security boundary**, and the tests that would prove it have not run in weeks.
- **KS-635 — a dated failure: an audit-baseline exception expires 2026-08-31**, and
  the gate then **blocks every push**. Its owning ticket is closed *and archived*, so
  **nothing on the board names the date.** Two and a half weeks away.
- **KS-638 — the team's own test board has never shown a green run**: 22 runs since
  2026-05-25, **0 passed**. The latest red is E2E passing 210/0 while the generator is
  *structurally incapable* of reporting passed. **The worst of the five, because it is
  read and disbelieved** rather than unread.
- **KS-634 — no CI gate runs the services' unit suites** since 2026-03-12.

**Recommendation:** these are not backlog items, they are the reason backlog items go
unnoticed. **KS-636 and KS-637 want action this week** (a critical CVE and the only
place four security suites run); **KS-635 wants a date in the diary before 08-31**;
KS-634 and KS-638 batch with the other CI work.

### ⚠ B. Scope guard on the hold lift — please confirm if I have it wrong
You authorised *"deploy the kintsugi queue"*, which I have scoped to **the demo VM
queue only**. **The extranet auto-deploys on push to main and remains held** — the
agent correctly declined to fix KS-638's one-line verdict bug for exactly that reason.
**I have not extended your lift to the extranet or anything else.** Say the word if you
want that surface unblocked too; otherwise it stays where it is.



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

### 4b. Datasec / HPSM — 🔴 **M0's acceptance evidence cannot be produced by either party**
**Problem (new, 2026-08-14):** **M0 — 25% / A$187,500, the FIRST and LARGEST payment**
— is accepted on SOW §7.1's *"SOW/funding authority, named owners, delivery plan and
backlog mobilisation confirmed."* **P01 is unsigned, P02 is past due and unfilled, and
no Datasec staff are named in any document either** (§11's nine roles; D-13, open five
sessions). So neither side can currently produce the evidence for the first invoice.
**Stated narrowly, and this is the agent's own framing:** it is **not** a drafting
defect — "named owners" is unqualified and a mobilisation list could satisfy it.
**The defect is our own tracking:** every register records P02 as an input reshaping
*later* gates, never as the acceptance evidence for the *first* one. The ask-list
front page named M1, M6 and M8 as the money behind P02. **M0 is larger than all three
and comes first.**
**It also re-prices D-13:** the two open pod-lead names are not a resourcing question,
they are **half of M0's acceptance evidence** — a commercial argument for Monday.
**Options:** (a) raise it in the Monday session as a commercial item and fold it into
the HP correction bundle · (b) treat it as internal tracking only and fix our own
registers · (c) both.
**Recommendation:** **(c)** — the register fix is ours and free; the naming question
is HP's and belongs in the bundle. **Not yet verified by me** — flagged for the next
session to check against the SOW extraction before it reaches HP.
**Related, same session:** all eight gates read against the §6 prerequisite table for
the first time — **7 of 8 depend on a prerequisite, and all 6 paying gates do**, split
honestly between *unanswered* and *our proposal awaiting HP approval*. And a
correction in our favour: the silence calendar dated the content freeze to **M2**, a
gate carrying **no payment and naming no content**; the content actually lands on
**M3, 20% / A$150,000**, so we had been claiming relief against nothing.

### ~~5. Secuura / Blockchain — the Kintsugi deploy~~ ✅ RULED: DEPLOY AUTHORISED 2026-08-14
**Problem:** thirteen merged-but-unshipped changes sit behind the hold, **four of them
security fixes** — including KS-617, which restores gateway **session revocation**
that is currently not running on demo. The backlog sweep cannot close any of them
without asserting a fix is live when it is not.
**Now countable:** the agent measured the In Review column and **19 of 23 tickets have
a merged PR** — it is a merge-residue pile, not a review queue. **Twelve are moving to
"Tested Not Deployed" and deliberately NOT being archived**, so the deploy debt stays
visible as a standing number rather than disappearing off the board. **Your one deploy
decision clears all twelve at once.**
**Options:** (a) lift the hold and deploy the queue · (b) keep the hold and accept
that the demo runs without those controls, with the tickets openly labelled
"awaiting deploy" · (c) deploy a security-only subset.
**Recommendation:** ruling needed rather than a specific option from me — this is a
product/environment call, not a technical one. What I would flag: **the longer the
queue, the riskier the eventual single deploy**, and KS-617 is a control people may
assume exists.

### 5b. Secuura / Blockchain — **KS-634: no CI gate has run the services' unit suites since March**
**Problem:** `ci.yml` is `workflow_dispatch`-only and **last ran 2026-03-12**; the `pr`
workflow's `test:unit` is Playwright's own suite, not the services'. **So for five
months a unit suite could die at module load and nothing would report it — and one
did** (a 73-test suite found dead on `develop` this morning and revived).
**This is not a backlog item; it is why several backlog items exist.**
**Options:** (a) fix it as a scoped CI session, alongside KS-628 and #687 which are
also `pr`-workflow work · (b) leave it and keep finding dead suites by hand.
**Recommendation:** **(a)**, batched with the other CI work — it is shared CI that
Peter and Stuart depend on, which is why nobody has changed it at short notice.

### ~~6. Secuura / Blockchain — the backlog residue~~ ✅ RULED: all 18 decided (see top)
**DELIVERED.** Full document in the Secuura vault folder:
`Notes (MASTER)/Secuura/platform-k-backlog-decisions-2026-08-14.md`.

**The agent went through all 87 Backlog items and pushed back on the premise, which I
think is right:** *"the backlog cannot be cleared to zero by triage, because it is not
full of stale tickets — it is full of real work."* **Exactly ONE** was genuinely
finished-and-unclosed (KS-400, closed and archived, with the superseding commit
`7cffe4341` and mechanism named).

| Why it is open | Count | Who moves it |
|---|---|---|
| Real engineering work, specified, nobody has done it | ~50 | any session |
| Blocked on a **decision** | ~20 | **you** |
| Blocked on the **Kintsugi deploy** | 12 | **one deploy** |
| Owned by Peter or Stuart | ~10 | them |
| Fixed today, in review | 3 | — |

**The highest-leverage item on the page is not a decision at all — it is the deploy**
(item 5 above). One action closes twelve.

**What the sweep actually found was not stale tickets: it was twelve tickets whose
DESCRIPTIONS were wrong**, corrected today with evidence — including four that each
said "the dependabot PR is left open so it stays fresh" when **every one of those PRs
was closed on 2026-07-14**. *"A backlog item that misdescribes its own state is worse
than a stale one: someone acts on it and wastes the afternoon."* It also declined to
close KS-341 despite its technical content being about deleted infrastructure, because
the underlying ask survives the platform it was written against — **the difference
between clearing a board and emptying one.**

### 7. Standing, unchanged
**Amplify HPSM-25 — overdue as of today.** · WED-107 (five legacy org-wide AgentMail
keys spanning every inbox) · KS-486/KS-621 org boundary-or-label · KS-624/625
by-design-or-remediate · F-1 WAF · F-5 CAPTCHA · KS-386 retention · KS-329 · KS-256 ·
verify-file 415 · KS-130/169/229 · the HP correction bundle (X1–X5 + X6 + CT §18
carriage) · four modelled revenue streams with one contract vehicle.

### 🔴 7b. Datasec / HPSM — **the Monday deck may not open, and this is now your 30 seconds well spent**
**Problem:** this was on your awareness list for two days as a formality. I tried to
close it and it did not close. **The system Quick Look renderer on this Mac produces
nothing for our Monday deck** — two runs, still going minutes later, empty logs — while
it renders **HP's own Playbook v3 (153 MB, 151 slides, 133 media) inside 25 seconds.**
Ours is 190 KB, 43 slides, no media at all. So it is not size and it is not complexity.
The file is structurally valid — I parsed the package independently, every CRC clean,
zero malformed XML.
**What it does not prove:** Quick Look is not PowerPoint, and python-pptx output usually
opens fine. **What changed is that the answer is no longer assumed** — one real renderer
refuses it while accepting a far heavier file.
**Options:** (a) you double-click the deck now — if PowerPoint opens it, this closes and
HPSM investigates at leisure · (b) treat it as broken and have HPSM regenerate before
Monday regardless · (c) leave it.
**Recommendation:** **(a), today.** It is thirty seconds and it is the difference
between finding this out now and finding it out in the room on Monday. HPSM already has
the finding with the controls attached and a bisect plan (the 28-slide client-safe build
is the first comparison). **Not (c)** — you present from this file in three days.

### 7c. Datasec / NexusAI — **RD-76 (Entra SSO) now blocks FIVE verifications, and that is a measured cost**
**Problem:** Entra SSO blocks agent browser-verification of the NexusAI demo. It has been
sitting as a standing inconvenience. **Today it stopped being one:** the project has five
items it can build and deploy but cannot prove — RD-85 (pill labels clip), RD-65 (dark
mode), RD-79 (session-expiry UX), RD-80 (SSE model label), and the new RD-89 health field,
which landed in an admin-gated endpoint the agent cannot curl.
**Why it matters more than it reads:** the agent is doing the right thing — refusing to
substitute *"the right code is deployed"* for *"the behaviour is verified"* — so the honest
consequence is a growing pile of shipped-but-unproven work rather than a false green.
**Options:** (a) give agent sessions a verification path to the demo (a service-principal
or a test identity that can sign in) · (b) accept it and let those five close on
code-deployed evidence with the gap stated · (c) leave them open indefinitely.
🔴 **Refinement from the agent, and it changes the ask:** the fifth item is an **admin-gated
JSON endpoint, not a page** — so the blocker is **any authenticated surface**, not "pages
behind SSO". **An acceptance criterion written around rendering pages would leave the API
case still blocked while looking closed.**
**Recommendation:** **(a)**, and it is a one-time setup rather than a per-ticket cost. If
you would rather not, **(b) with the gap written on each ticket** is honest and I can rule
that myself — **(c) is the one to avoid**, because five open tickets that are actually
finished make the board lie in the other direction.

### 🔴 9. WED — **AgentMail: deletion is NOT revocation, the vendor will not say when it will be, and WED-107's plan is now wrong**
**Problem:** the 08-13 session proved that deleting an inbox-scoped API key returns 204 and
removes it from the listing **while the key keeps authenticating** — reproduced twice, two
independent keys. **AgentMail replied 2026-08-14: *"We will consider fixing it in the
future."*** None of the four questions answered — no TTL, no propagation window, no forced
invalidation, no statement on other scoping gaps.
**Why it is yours and not mine:** it changes the security posture of the fleet's entire
comms layer. **Every key we have issued must now be treated as permanently valid.**
**What it breaks specifically:** the per-project migration's premise was *"a compromised key
can be revoked and replaced."* The isolation half works exactly as advertised; **the
revocation half does not exist.** And **WED-107's plan — delete the five legacy org-wide
keys — would make them vanish from the listing while leaving them live**, which is strictly
worse than leaving them visible.
**Options:** (a) press AgentMail for a supported forced-invalidation path or a date, naming
the impact — external comms, so yours · (b) treat keys as unrevocable and adapt: minimise
issuance, no test keys, and neutralise the legacy five some other way (rotate the account,
or migrate off the shared key entirely) · (c) accept and document the risk as it stands.
**Recommendation:** **(b) now, (a) alongside it.** (b) is entirely ours and does not wait on
a vendor who has just declined to commit. **Not (c) alone** — a documented risk that nobody
can act on is where WED-107 already sits.
**Note:** re-testing whether this is still broken **requires issuing a key that may never be
revocable**, so I have not re-tested and the 08-13 evidence stands. The cost of verifying
the defect is an instance of the defect.

### 8. Awareness only — no decision
- Secuura B-3 would have reset your real `kam@secuura.ai` SYSTEM_ADMIN account to a
  repo-published password. Fixed in #686, unshipped.
- ~~PowerPoint-opens check — 30 seconds, still unverified.~~ **Promoted to item 7b: it
  is no longer a formality.**
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
