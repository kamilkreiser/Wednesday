---
date: 2026-08-06
type: reference
source: "Kam, 2026-08-06 (verbatim in 1_Project_Definition/Discovery/00_prompt-log.md), plus live az verification the same hour"
status: live
---

# Datasec — the five environments

Kam's own high-level structure, given 2026-08-06 while resolving whether a
Lead_Bot host still exists. This supersedes my previous mental model, which
knew only "two Datasec tenants" (workspace CLAUDE.md rule 4) and had been
patched twice with surprises — the third tenant found on 08-05, and the
"tenant TBD" that has been blocking Lead_Bot, Task_Dispatcher, myPKI and
others since the workspace rules were written.

## The five, as Kam stated them

| # | Environment | What lives there |
|---|---|---|
| 1 | **Corporate** | Email, SharePoint, the company's own IT |
| 2 | **Production** | Live customer-facing systems |
| 3 | **Dev** | Development |
| 4 | **Sales demo** (global variables) | What **NexusAI** uses |
| 5 | **"Our Datasec environment"** — linked to `kreiser.org@me.com` | **Vision Sales Portal, NexusAI and other things.** Separate *because it can be controlled by agents*; **not linked to anything production**. Wednesday is to have CLI access here. |

Kam's framing of #5 is the important part: the separation is deliberate and
its PURPOSE is agent control. It is the environment where an agent may act
without production risk. Treat that as a design intent to protect, not just a
convenience — the moment #5 gains a production linkage, the reason it can be
agent-controlled disappears.

## Tenant IDs — what is VERIFIED vs what is INFERRED

**Verified live on the Studio, 2026-08-06 ~10:5x** (read-only `az` calls):

- **`ae7a1e46-02d7-4035-9a3f-dc6d9e172217`** — user `kamil.kreiser@datasec.com.au`,
  a *tenant-level account with ZERO subscriptions visible*. This is the
  **corporate** tenant (#1). It is also the mailbox tenant found on 2026-08-05
  during the calendar work. **This is what Wednesday's global `az` is logged
  into right now** — i.e. her default identity has no compute access at all.
- **`d500ebad-cf53-4f2a-a501-f831289e67fc`** — user `kreiser.org@me.com`,
  subscription **"Azure subscription 1" `0c57ab37-349c-47ae-a10f-e284a380bbb9`**.
  Read from Vision Sales Portal's isolated `4_Credentials/.azure`. Matches
  Kam's description of **#5** exactly (his personal-linked, agent-controllable
  environment) and matches Vision's own 08-04 history ("tenant was verified
  d500ebad… / kreiser.org@me.com" before its prod deploy).

**Known but not re-verified today:**

- `fc05dcdd-2c88-4b0c-9e47-8cafdaba815b` — the "Datasec dev tenant" in the
  workspace CLAUDE.md, described there as the NexusAI demo environment. Kam's
  map puts NexusAI's demo in **#4 (sales demo)** and also says NexusAI lives in
  #5. Those are not necessarily contradictory (demo environment vs where the
  project's own resources live) but the mapping is **UNRESOLVED** — do not
  assert which of #3/#4 this ID is until checked.

**Inference, explicitly NOT fact:** Lead_Bot most likely belongs to **#5** — it
integrates with Vision (which is verified #5), writes to Vision's database as a
fallback, and is agent-touched work rather than production. Kam has not
confirmed this. Do not run `az` against Lead_Bot on that basis.

## Consequences for how I work

1. **Wednesday currently has NO CLI access to environment #5.** Her global `az`
   is the corporate tenant with no subscriptions. Kam believes she has access;
   she does not, today. Fix per the isolation pattern: a Wednesday-scoped
   `AZURE_CONFIG_DIR` at `4_Credentials/.azure` plus a one-time
   `az login --tenant d500ebad-…`, so the access is hers and structurally
   isolated — never borrowed from a project's config dir.
2. **Never borrow another project's `AZURE_CONFIG_DIR`.** Vision's authenticated
   state would answer Lead_Bot questions today; using it would be exactly the
   cross-project credential stretch the Lead_Bot agent flagged about itself.
   Read-only or not, the identity must be mine.
3. **The workspace CLAUDE.md rule 4 is incomplete**, not wrong: it names two
   Datasec tenants where there are at least three, and describes none of the
   five-environment structure. Correcting that file needs Kam's named
   go-ahead (it is his, and outside this project) — carried as an open item.

## The unaudited tenant cleanup — an open risk

Kam: *"there was a tenant cleanup. I could not remember what was removed."*
Nobody knows what was deleted. That means any project's notes, briefs, scripts
or launchers may still reference resources that no longer exist, and the
failure mode is a session burning time on a resource that was removed months
ago. This is the same class as the dead Secuura tenant that sat in a launcher
until June. Worth a scoped read-only sweep of environment #5's actual resources
against what the fleet's docs claim — cheap once CLI access exists.

**Related:** [[../learnings/2026-08-05_identities-float-verify-always]],
[[../learnings/2026-08-03_mental-model-not-source-of-truth]],
[[../projects_index/INDEX]]
