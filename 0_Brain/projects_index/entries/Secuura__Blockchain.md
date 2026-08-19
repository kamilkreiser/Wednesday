---
client: Secuura
project: Blockchain
path: /Volumes/DevMASTER/!CODING/Secuura/Blockchain
status: active
updated: 2026-08-20
---

# Secuura / Blockchain (Platform K)

**Last sessions (2026-08-19, s47 + s48, both 1.0):**
- **s48: 🎉 KINTSUGI IS UP** — `secuura02-kintsugi.southeastasia.cloudapp.azure.com`
  (20.198.226.148), D2ps_v6 **zone 1** (zone 3 sub-restricted), 128 GiB, USD
  **77.05/mo list** (Kam-authorised). NSG pre-built at create: 22 from
  157.211.46.94/32 only · 80/443 open · deny-all. **Stage C NOT started** (own
  wallet on-box is absolute per KS-535; Blockfrost own-key rec pending; stack +
  Caddy + KS-584 P3 deploy queued). Plan defect on record: §3's `--image
  Ubuntu2404` is x64 — ARM64 image string required (KS-601 comment). KS-601 → In
  Progress. 🔴 Demo NSG has SSH open to 0.0.0.0/0 → Kam's queue. Wiring settled:
  **dev-ps consumes Kintsugi's API (Stuart wires it), uat-ps stays on demo's** —
  next brief carries dev-ps into Kintsugi's allowed origins + tell Stuart when up.
- **s47: KS-256/PR #568 review done** (comment d94fc204): merge NOT YET — pushed
  head fails originate tsc (Peter's fix uncommitted) + PII checkbox unticked;
  ack rec = per-PR yes, standing rule needs a schemathesis-baseline.json; "Demo
  Issuer" in all 16 `address` fields (E5 certifies it). Kam messaged Peter.
- **CI still dead** (org Actions money; discussion date ambiguous "Wed 08-20").
  Merge order on return: #721 → #720 → #718, then #568 on Kam sign-off.
- **Instrument rule, confirmed ×2 on 08-19: Linear `comments(last:N)` returns the
  OLDEST comments — always `first:50` + client-side sort.**

**Open / next:**
- **KS-256 re-review — Peter's explicit ask ("the only thing genuinely blocking").**
  Both s47 blockers CLEARED 08-19 (documentUuid fix pushed, all services tsc clean;
  PII checkbox with evidence); 8/10 review points closed; our ack condition built
  (schemathesis-baseline.json, 97 pairs, gate enforced). Head `867b25728`. Merge
  still gated: CI dead (PR reads CLEAN over 3 startup_failure runs), order on CI's
  return #721 → #720 → #718, then #568 on Kam's sign-off after the re-review.
- **KS-665 (High, assigned kksecura):** 5 example-fixable 400s · 132/2
  parameter-example gap · §10 · new `userAgent: Demo Issuer` instance.
- **Kintsugi Stage C (standing default, Kam's veto stands):** stack + OWN wallet
  on-box (KS-535 absolute) + Caddy — **kintsugi.secuura.net is live in DNS
  (Stuart, 08-19; CNAME verified resolving 2026-08-20)** so the cert goes on the
  real name · dev-ps into allowed origins + tell Stuart when up · KS-584 P3
  deploy into Kintsugi · Blockfrost own-key rec · ARM64 image string (plan §3
  wrong as written). Peter's KS-666 (stack isolation for concurrent agents)
  strengthens the case.
- **KS-490 + KS-491 still open** (both Todo, verified on the board 2026-08-20).
- **Kam:** KS-486 tenancy ruling (In Review) · demo NSG SSH open-to-world
  (queue item) · CI cost-discussion date.
- **Stuart:** KS-539 sign-off, open since 2026-08-04 (still In Review).

**Completed (moved off the dashboard 2026-08-20, verified Done on the board):**
KS-488 (Review C) · KS-647 (clean-room resolvability).

**Last session (2026-08-17, s39):** Boot + triage only — Kam launched the session himself and
wrapped it before confirming the queue, so **nothing on your s39 brief was executed**. `develop`
unchanged at `2129cdc8b`, 0/0, tree clean, zero code. Board verified independently at **136**
(95 backlog + 41 unstarted/started) — your figures reproduce exactly. **Where the brief does not
survive contact:** (1) C-5's SMTP defaults are in **two** services — `services/auth/…/email.ts:46,51`
**and** `services/originate/…/email.ts:47,52` — the ticket names one, so fixing the named one
leaves the defect live; (2) F-9's CSP at `nginx-demo.conf:595` sits in a **wholly commented-out
block** while the **live** header block at `:246-258` has no CSP — "uncomment :595" would read as a
fix and change nothing; (3) the owed `CLAUDE.md` correction **was already made by s38**, which
logged it as outstanding anyway. Also archived **14 Done tickets** (14/14, verified 0 remaining
against a control).

**Open / next (s39-era, SUPERSEDED by the 2026-08-20 block above — kept for the record):**
- ~~The s39 queue: KS-490 E-2/E-3 · KS-488 C-5 · KS-491 F-9 · KS-647~~ — KS-488 and
  KS-647 verified Done 2026-08-20; KS-490/491 carried into the current block.
- **Stuart:** KS-539 sign-off, open since 2026-08-04; Kam and Peter have both signed.

**Blockers:** none on me — the queue is available the moment a session runs it.

**Notes for Wednesday:** All holds observed and none tested — KS-486/642-645 no-code,
`pre-merge-platform-suites.yml` not dispatched, #686 left red, extranet not marked seen
(`EXTRANET_ME=kam`; clearing it resets Kam's own new-flags), demo untouched entirely. Worth
relaying: **two of the four rows in a brief were wrong in the same direction** — both would have
produced a change that looked like a fix and wasn't. That is the third consecutive session where
checking the row beat taking it.
