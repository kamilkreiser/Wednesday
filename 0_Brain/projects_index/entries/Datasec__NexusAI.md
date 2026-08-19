---
client: Datasec
project: NexusAI
path: /Volumes/DevMASTER/!CODING/Datasec/NexusAI
status: active
updated: 2026-08-20
---

# Datasec / NexusAI

**Last session (2026-08-17):** Booted clean and built nothing, deliberately. Board
reproduced Wednesday's figures exactly (53 open of 95; 21/14/11/5/2). The authorised
RD-95+RD-98 demo deploy was **held**: the deployed cutoff is `e384116` (RD-88), not
`b54ee24`, and RD-94 is a git ancestor of both authorised commits, so "nothing else
rides along" cannot be satisfied from `main`. Separately the local jest suite had been
silently dead — devDependencies pruned, and a piped `npm test` reports the pipe's exit
status, so it read exit 0 over zero tests. Repaired (`npm ci`, 183/183), filed as RD-100.

**Open / next:**
- [ ] **K2 — Kam's `gh auth login` (RD-74)** gates the resume; stood down since 08-18.
- [ ] RD-62's live half — the demo threshold mis-set is **HELD for Kam** (decision queue).
- [ ] On relaunch: re-derive the queue from the board (57 open verified 2026-08-20:
      22 To Do · 16 Release Ready · 12 Testing · 5 On Hold · 2 In Progress).
- [ ] Kam's desk, unchanged: RD-99 · `.gitleaks.toml` rescope of RD-55 · RD-93 · RD-76.

**Completed (moved off the dashboard 2026-08-20, verified in HISTORY.md sessions
29–30):** both asks ANSWERED (RD-94 rode along); the deploy SHIPPED — demo live on
rev `--0000084`, image `1.17.8-rd94-95-98-8f2ce5f`, RD-94/95/98 all Release Ready;
RD-100's durable half shipped (`39cb7bc`); RD-101 filed AND fixed (`c09f6f6` — the
CI gate can now fail, four controls run).

**Blockers:** two asks with Wednesday, both unanswered (sent 20:12Z) — (a) may RD-94 ride
along in the authorised deploy, or does it hold; (b) may the demo's active data source
carry a temporary, reversible threshold mis-set so RD-62's stale branch can be proven at
the unauthenticated `/api/health`. Nothing is being built pending both.

**Notes for Wednesday:** the deploy is genuinely both-or-hold — a cherry-pick excluding
RD-94 would ship a tree that has never existed on `main` and whose suite has never run as
that combination. The safe default on silence is HOLD, since proceeding would resolve a
scope question in the permissive direction. RD-62's dashboard-banner criterion stays behind
RD-76 regardless; the other two criteria do not need a browser. Unchanged on Kam's desk:
RD-99, the `.gitleaks.toml` copy that rescopes RD-55, RD-93, RD-74 (one `gh auth login`,
provably blocks RD-66), RD-76.
