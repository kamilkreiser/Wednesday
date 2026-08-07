---
date: 2026-08-07
type: decision-pack
for: Kam
status: awaiting-answers
---

# Decision pack — held for Kam's check-in, 2026-08-07 afternoon

Four items. **One is a correction to something I already told him and he already
ruled on** — it goes first. Nothing is blocked on work; all four are his.

---

## 1. CORRECTION — Secuura/Blockchain: the key-listing defect does not exist

**What I told him this morning:** their evening session found "two verified live
defects", one of which was that *an admin cannot list an org's keys on demo at
all* — 25 rows in `svc_api_keys` against a boot log reading `apiKeys: 0`. He
ruled **2a: GO on the standalone ~0.5-day fix, do it first**.

**It is not real, and their retraction is better evidenced than the original
claim.** Checked read-only on demo 2026-08-07:

- the boot warm **has been correctly platform-scoped since 2026-07-14**
  (`runWithPlatformScope` at `services/security/src/index.ts:344`, commit
  `46fb9f88d`, KS-458/PR #534 — with a comment describing this exact failure
  mode). Their original citation of lines `:346-365` was the query lines
  **inside** the wrapper they missed two lines above;
- **`apiKeys: 0` was accurate** — the boot line is timestamped
  `2026-07-30 03:23:44` and the oldest row in the table was created at
  `03:24:06`, 22 seconds later. Nothing was missed because nothing was there;
- **listing works now:** demo `/health` reports `activeApiKeys: 22`,
  `auditLogs: 205`.

**Their stated error:** *"Confirming a mechanism is not confirming a cause."*
The RLS behaviour they demonstrated is real; it just was not what happened.

**My error, which Kam should hear from me:** I forwarded their finding to him
using the word **"verified"**. The verification was theirs, not mine, and I
flattened that out while relaying. He spent a ruling on it. Nothing was built —
the ruling was to do it first, and the retraction arrived before work started —
so the cost is one wasted decision and no execution.

**Consequences:** ruling 2a is withdrawn as moot. **Finding A stands** —
`rotate: true` still mints a new key and never revokes the old one — so the
KS-480 sizing argument survives on one leg rather than two, and the honest
framing to Peter changes accordingly. **Recommend: no action beyond
acknowledging it; the split (ruling 3a) already covers the real work.**

---

## 2. Secuura/Blockchain — KS-570 triage

Revoked-session JWTs accepted on `/api/status` and `/api/leaderboard/*`.
Assessed as Kam instructed (4c: assess before triaging), nothing created.

**Their recommendation: High, moved to Todo.** Plus a second call they flagged
rather than decided: **whether the authorization gap gets its own ticket.**

**My recommendation: take their triage (High → Todo), and yes to a separate
ticket** — an auth-bypass shape and a session-revocation shape are different
work with different reviewers, and bundling them tends to get the smaller one
quietly dropped.

---

## 3. Secuura/Blockchain — KS-564 ship ruling

All three legs built and proven, preflight green, sitting at the merge boundary.
Deploy boundary held all session: nothing merged, nothing on demo beyond
read-only.

**Their recommendation: ship all three legs as one piece.**
**My recommendation: agree.** It has been held twice now for the right reasons;
the only thing between it and demo is Kam's own word.

**This is approval-class — it needs Kam's authored confirmation, not my relay.**
One line from `kreiser.org@me.com` to `coagent@agentmail.to` does it, and agents
now verify authorship by DKIM rather than the From line.

---

## 4. Secuura's Linear is at the free-plan cap — 250 active issues

**This blocks Peter as well as us: the next ticket anyone files may fail.**
Archiving closed issues does not help — the cap counts **active** ones.

Options: (a) upgrade the plan — costs money, which is why it is Kam's;
(b) bulk-close or archive genuinely dead active issues to make headroom;
(c) leave it and accept that ticket creation is now unreliable on a client
board.

**My recommendation: (b) first as immediate relief, then (a) if the board is
genuinely carrying 250 live items** — but I would not spend money before someone
has looked at whether 250 issues are really active, and I have not looked
because it is a client board and read-only to me.

---

## Not in this pack, but pending elsewhere

- **RD-76 (NexusAI):** the demo sits behind Entra SSO, so no session can visually
  verify a deploy. Needs Kam's eyes once, and will recur every deploy.
- **Vision Stage 1** is running well and needs nothing.

---

# ADDED AFTER v1.3 LANDED — two items, both surfaced by the agents

## 5. CONFIRM OR CORRECT — does v1.3 stop the routine Peter/Stuart notifications?

Secuura caught a collision the moment they read the grant. It names Peter and
Stuart as external humans requiring Kam's signature, **but Platform K's standing
rule 7 requires notifying them on every environment push** — a routine action
they performed 40 minutes before the grant landed.

**My ruling, pending Kam's confirmation: rule 7 notifications continue.** Their
authority originates with Kam, who approved rule 7 before v1.3 existed, so
sending them is executing a decision he already made — not authority originating
with me, which is the grant's actual test. The alternative reading is worse on
its own terms: a partner who reads every ticket would silently stop hearing
about pushes, and a protocol written to protect the relationship would be the
thing damaging it.

**Still requiring his signature, and I have told them so:** a NEW topic with
Peter or Stuart · anything committing us (dates, scope, prices, undertakings) ·
a change to rule 7 itself · any message whose substance is mine rather than a
relay.

**Kam: confirm or narrow.** If he narrows it, rule 7 pauses the same day.

## 6. NEEDS KAM'S HANDS — v1.3 is not in the file every session reads first

NexusAI flagged it: the grant is recorded in each project's own `CLAUDE.md` and
in the vault, **but the workspace-level `/Volumes/DevMASTER/CLAUDE.md` is outside
every agent's write scope — and mine.** That is the first file every project
session reads.

**So a cold session in any project will not know v1.3 exists** until someone with
write access to that file adds it. Until then, adoption depends on each agent
having retained the mail, which a fresh session will not have.

**Recommend:** Kam adds a short pointer to the workspace CLAUDE.md — the grant's
date, subject, Message-ID, and that it is verifiable on the bus by DKIM. I have
drafted nothing into that file because it is outside my scope and I am not going
to make an exception for a document that expands my own authority.

## 7. PRODUCT DECISION (Stuart's, via Kam) — what does a duplicate upload MEAN?

Stuart's finding, forwarded 2026-08-07: **S and K disagree on what a document
is.** K's registry is claimed to be `UNIQUE (content_hash, tenant_id)` with
`ON CONFLICT … DO UPDATE`, so re-uploading identical bytes silently overwrites
the prior registry pointer; S inserts a new row every time with no duplicate
check. **S says two documents, K says one and the newer wins.** He believes it
sits upstream of a class of symptoms they have both been chasing. Kam's read:
*"a start but a good one."*

**The decision he is actually asking for — and it is Kam's, because Stuart says
so himself: "It's a product call, not a technical one."**

Same org, same bytes:
- **(a) Dedupe** — reuse the row. One document, shared twice. Matches K's model;
  means a user who uploads the same file twice cannot have two separate
  registrations even if they meant to.
- **(b) Warn the uploader** — surface it at upload time and let them choose.
  Honest, but puts a question in front of a user who may not understand it.
- **(c) Keep both deliberately** — two documents, by design. Matches S's current
  behaviour; requires K to stop treating hash as identity, which is the larger
  change.

**No recommendation from me yet, deliberately.** I have asked Secuura to verify
the K half against the real schema and code first, because **Stuart's analysis is
itself AI-generated** — his own attribution is *"(so from Claude …)"* — and I
made exactly this mistake today by relaying an agent's finding to Kam as
"verified". A product decision built on an unverified premise is the expensive
version of that error, not the cheap one.

**One thing worth Kam seeing now, because it is the trap in Stuart's option 4:**
stamping identity into the file (watermark, XMP, embedded id) does make documents
genuinely distinct — but it **changes the artefact the user handed us, and
therefore changes the hash they would compute independently.** On a product whose
proposition is "this is provably the document you gave us", that is substantive.
Stuart has noticed it; it should not pass as a footnote.

**Nothing has gone to Stuart or Peter.** Under v1.3 a new topic with them needs
Kam's signature.

---

# THE ARCHITECTURE DECISION SET — added after the commission delivered (2026-08-07 evening)

The Secuura agent's response is in and verified. Headline: **K already has the
identity model in its schema — UUID primary key, UNIQUE external_id, org/user
columns, GitHub-shaped org tables. The model is built and unused (0 org members,
0 documents with an org set). This is a wiring-and-contract job, not a schema
job.** Three findings Kam should read in their words (in
`1_Project_Definition/architecture/2026-08-07_K-S-architecture-response.md`):
K never sees document bytes (the hash is S's assertion, not K's observation);
no smart contract has ever executed (all 234 anchors are metadata, the compiled
validators have never run); the hash is not even stored canonically (two
spellings, two shapes, tie-break arbitrary in 8 of 9 real duplicate groups).

## 8. APPROVE THE PLAN — P1 → P5 → P2 → P3 → P4

P1 accept the three UUIDs (optional) + populate org column + neutralise the
dormant multi-tenancy upsert, 3–5 days · P5 hash canonicalisation, 2–3 days ·
P2 org membership + upload-time org selection, 1–1.5 wks · P3 UUID as primary
identity, verify-by-hash returns a list with a count (breaking, versioned),
1 wk · P4 rules as a versioned hashed anchored document, 2–3 wks. P6 (on-chain
thread identity) and P7 (enforcement contracts) explicitly gated on the
self-sovereign trigger, not a date. **Recommend: approve.**

## 9–12. The four remaining questions, each with a recommendation

**9. Duplicate uploads = two registrations?** Recommend **yes** — it follows
from Kam's own "generated for every single document", and the idempotent
registration endpoint (re-POST of a known UUID returns the existing row) makes
accidental duplicates structurally impossible while keeping deliberate ones.
This also closes decision-pack item 7.

**10. Rules precedence (user vs org).** Recommend **fixed precedence, org wins,
for the first release** — the agent notes variable precedence is materially more
expensive, and no customer has asked for it yet. Revisit when one does.

**11. Governance of governance.** Recommend **offering "no one, ever" as a
per-contract option** — the agent's point: cheapest to implement and the
strongest claim the product could make. Alongside it, a named-role variation
path for contracts that need one.

**12. The bridge state.** Recommend **adopting the agent's reading**: from P1,
K is authoritative for identity, hash and anchor; S stays authoritative for
workflow state and presentation indefinitely; rules move to K at P4.

## The question the smart-contract stage turns on (no action now — P4+ framing)

Their words, worth reading before any P6/P7 decision: *"do we need the chain to
PROVE the rules, or to ENFORCE them? For authenticity and dispute resolution,
proving is usually what customers actually ask for. Enforcement earns its cost
when a party we do not control could act against the rules — which, while both
platforms are ours, is not yet true. Self-sovereign documents outside the
platform is exactly that trigger."*

## Awaiting from the agent (in flight): the finalised S-pack v1.0 + a cover note
for Kam to send Stuart under his own name + the one-page plan sheet.
