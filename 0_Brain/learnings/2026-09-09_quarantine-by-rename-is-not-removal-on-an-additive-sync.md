---
date: 2026-09-09
type: correction
source: Tuesday's first boot on Kamils-Mac-mini — a dead tenant re-installed onto a fresh machine
status: live
tier: M
---

# Quarantine by RENAME is not a removal on any additively-synced tree — the replica keeps both names, and the next restore ships the thing you quarantined

**The operative case, so the headline matches it:** you are about to neutralise a
dangerous file — a stale credential profile, a dead tenant, a superseded config, a
conflict copy — and the move is **quarantine, never delete**
([[2026-08-26_never-delete-cleanup-means-quarantine]]). **You are about to do it by
renaming the file in place.** Stop and ask one question: **does this tree get synced to
any replica by an engine that does not propagate deletions?** If yes, the rename does not
remove anything anywhere else. It **adds a second file**, and the original survives on
every replica.

## The case, measured

Kam quarantined the decommissioned Secuura tenant on 2026-09-07 by renaming
`Machine_Credentials/azure/azureProfile.json` to
`azureProfile.json.QUARANTINED-2026-09-07-dead-tenant-4012a4e8`, on DevMASTER. Correct
policy, correctly executed, and he ruled it himself.

On 2026-09-09 he ran `install_credentials.command` on a brand-new Datasec Mac mini. The
result, measured immediately after and not assumed: `~/.azure/azureProfile.json` named
exactly one subscription — **`Secuura Subscription`, tenant
`4012a4e8-26db-400b-b933-75f9931ed6e2`, `isDefault: true`** — the tenant the workspace
`CLAUDE.md` records as decommissioned 2026-06-25 with *never log into it*.

The T9 bundle held **both** files, `azureProfile.json` and the `.QUARANTINED-…` copy,
**both 426 bytes, both dated 27 Apr**. The installer copies the whole `azure/` directory,
so it restored the live one.

## The mechanism, and it is the part worth carrying

**A rename is a delete plus a create.** An additive / no-delete sync replicates the create
and refuses the delete. So the replica ends up holding *both* names — and the original,
which the quarantine was supposed to retire, is still the one every tool reaches for by
its ordinary name.

**Two safety policies we hold deliberately combine into a mechanism that resurrects
quarantined content:**

1. *Quarantine, never delete* — because deletion is the one operation that cannot be
   undone from inside the system ([[2026-08-26_never-delete-cleanup-means-quarantine]]).
2. *Sync additively, never propagate deletions* — because a sync that can delete is a
   delete command with a delay ([[2026-08-26_a-sync-that-cannot-refuse-a-deletion]]).

**Neither is wrong. Their interaction is, and nobody owned the interaction** — which is
why this survived three months and reached a machine built long after the decision.

## How to apply

1. **Quarantine by MOVING the file into a directory the sync engine already ignores**
   (`Archive/`, `_quarantine_YYYY-MM-DD/`), not by renaming it in place. A move out of the
   synced set is a removal everywhere; a rename inside it is an addition everywhere.
2. **Verify a quarantine AT EVERY REPLICA, not at the one you performed it on.** The
   check is one `ls` per replica for the ORIGINAL name — its absence is the property that
   matters, and its presence is invisible from the machine where you did the work. This is
   [[2026-08-05_verify-the-chain-not-the-legs]] pointed at a removal instead of a copy.
3. **Fix the SOURCE, not the machine in front of you.** A bundle, template or image that
   still ships the bad artefact will reproduce it on the next restore. Repairing only the
   current machine converts a systemic fault into a recurring one.
4. **State severity by what is REACHABLE, not by what is named.** Here the profile was
   inert — no token, `az account show` refused — so the exposure was directional (the next
   `az login` in a non-launcher shell defaults to a dead tenant; the next restore repeats
   it), not active. Saying that precisely is what lets the owner size it
   ([[2026-09-04_decisions-held-narration-drifted]]).
5. **The generalisation past syncs:** the same shape appears wherever a "removal" is
   implemented as a rename or a status flag inside a set that gets copied wholesale —
   archived tickets copied by an export, disabled accounts in a replicated directory,
   `.disabled` config files in a container image. **Ask what COPIES this set, and whether
   it copies intentions or only bytes.**

**What held, and it is why this cost nothing today:** the per-project
`AZURE_CONFIG_DIR` / `GH_CONFIG_DIR` isolation meant the coordinator seat read a
project-local profile with zero subscriptions and was structurally unable to touch the
restored one ([[2026-08-05_identities-float-verify-always]] rule 3 — prefer
structurally-isolated state over global state). The global fallback was wrong; the seat
never read it.

**Family:** [[2026-08-26_never-delete-cleanup-means-quarantine]] ·
[[2026-08-26_a-sync-that-cannot-refuse-a-deletion]] (its sibling — there the sync deleted
too much, here it deletes too little) · [[2026-08-25_travel-drive-stale-pointers]] (a sync
copies files, not intentions) · [[2026-08-05_identities-float-verify-always]] ·
[[2026-09-08_a-ruling-can-be-voided-by-removing-its-precondition]] (a ruling executed and
then undone by a mechanism nobody connected to it).
