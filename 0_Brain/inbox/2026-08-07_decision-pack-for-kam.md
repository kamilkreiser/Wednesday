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
