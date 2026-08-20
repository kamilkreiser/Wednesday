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

**Open / next (refreshed 2026-08-20 midday — K2 CLEARED, session scored 1.0):**
- **Next session's pre-approved lead:** disposition the seven remaining Release
  Ready (RD-94 · RD-91 · RD-82 · RD-77 · RD-71 · RD-61 · RD-58) — no deploy needed.
- **Kam's desk:** RD-104 gh-storage policy (neither option closes the no-hosts
  fallback while a keychain entry survives; clearing the keychain = irreversible,
  signature-class) · **RD-76 now priced: FOUR finished tickets parked behind the
  SSO block (RD-56/67/68/89)** · RD-62 threshold · RD-99 · RD-55 rescope ·
  RD-93 · RD-103.
- Board 52 open (21 To Do · 14 Release Ready · 9 Testing · 6 On Hold · 2 In
  Progress); five closed today with controls; RD-105 new (orphan scripts).
- RD-101/RD-100/RD-102 Release Ready (gate proven red on run 32323894047 —
  labelled probe).

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
