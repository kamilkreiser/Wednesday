---
date: 2026-09-07
type: pickup
scope: SECUURA + Wednesday's own work. Datasec belongs to the LAPTOP seat — see NEXT-PICKUP-DATASEC-LAPTOP.md and do not touch it.
source: replaced wholesale at the 50% checkpoint by the 10:07 successor seat
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — ~11:0x AEST Monday. THREE MERGES DONE. One seat live on #885 round 2.

**Mail timestamps are UTC ≈ AEST−10.** Voice allowed (06:00–23:00). Kam is awake and ruling fast —
he has ruled **six cards** since 10:22. **Run `kam_rulings_today.sh` before writing anything — AND
SEE THE BLIND SPOT BELOW, because it only reads one of his two panels now.**

## 🔴 THE THING THAT CHANGED TODAY: THERE ARE TWO WEDNESDAYS, BY KAM'S DESIGN
**Kam, 11:01 verbatim:** *"The agent on the laptop is working on data sec items. I will re-sync the
two projects once we've finished, but for now I will separate the running of Secuura on this machine
and Datasec on the other machine, as this machine is running a little bit slow, and also I have an
additional Claude Max account for Datasec that I will use to split the credits across the two
projects."*

- **THIS seat = Secuura + Wednesday's own work. The laptop seat = Datasec** (it owns NexusAI, which
  Kam unpaused at 10:46; Vision is PARKED and is **PRE-PRODUCTION, not live** — his 10:44 correction).
- **The partition is clean and the other seat is disciplined about it:** it writes only
  `NEXT-PICKUP-DATASEC-LAPTOP.md` and states in its own handover that the shared files
  (`NEXT-PICKUP.md`, the daily note, `_ledger.md`) are this seat's. **Zero collisions so far.**
- **PULL BEFORE EVERY WRITE.** `origin/main` moved under this seat once today without warning.
- You will see `[Wednesday -> Datasec/…]` mail in the shared inbox **that this seat did not send.**
  That is the laptop. It is not yours.

### ⚠ THE BLIND SPOT — raise it again if Kam has not ruled
`kam_rulings_today.sh` reads **ONE panel**. Kam ruled **five times on the other one** today (10:15
review scope · 10:44 Vision parked + pre-production · 10:46 NexusAI unpaused · 10:48 the Marketplace
objective · **10:49 the rotation band → 80–90%**) and **none reached this seat's instrument.** They
arrived only because the laptop seat pushed a file and this seat read the commit. **The boot rule
"read his rulings before writing anything" now silently covers half his words.** Put to him as: one
panel, or the tool reads both and says which it read. **Not yet ruled.**

## ✅ ROTATION BAND IS 80–90% (Kam 10:49). 70% is a CHECKPOINT ONLY.
The launcher said **70%** until this seat fixed it — it was **two rulings stale** and is why seats
kept rotating early. Fixed in `Launch_Wednesday.command`, verified by extracting `INITIAL_PROMPT` and
asserting its length (11,150) and tail. Backup `.pre-0907-band8090`.

## 🔴 FIRST ACTION FOR YOU — #885 round 2 is IN FLIGHT with s145. Do not re-brief it; check it landed.
**Kam ruled `round2-plus-probe` at 11:01:35.** The brief went out 01:02:58Z (subject starts
`KAM RULED round2-plus-probe`) and the tap was **queued behind a running turn** — s145 was mid-KS-597
at the checkpoint. **VERIFY IT ACTUALLY STARTED #885 rather than trusting the queue** (this morning a
"next" item sat unstarted for ~75 minutes while both parties believed otherwise).

**F1 is a BLOCKER:** `startup-migrations.ts:958-982` says `ON CONFLICT (email)` while the real
collision on a seeded box is the **PRIMARY KEY `id`** — Postgres aborts **all twelve rows** and the
error is swallowed as a **debug-level "User seed skipped"**. Kam's real address stays live.
**AUTH DB is genuinely fixed** (proved against real Postgres under fail-closed RLS). Also in scope:
F2 (three files still publish a password beside the identity), F4 (the drift guard covers 2 of 4
executable seed sites — a planted tamper passed 7/7), F5 (revert `ALLOW_DEFAULT_SEED_PASSWORDS`
default-ALLOW back to DENY). **F3 is FILE-ONLY, not fix** — see below.
**This is round 2 of 2 under Kam's cap. A third needs his word.**

### THE PROBE — one, read-only, hard bounds
Kam authorised **ONE read-only probe** of the demo to establish whether it is actually in the
already-seeded state. **Bounds given: state the success/failure condition IN WRITING BEFORE running
it; if no read-only probe can discriminate, SAY SO AND STOP rather than reaching for something that
changes state; never use or transmit the real address or any credential.** **His exposure is
UNMEASURED and has been told to him as unmeasured — do not let that harden into a fact either way.**

## 🔴 F3 — THE BIGGER FIND, and Kam chose NOT to prioritise it (round2 over escalate). File it as a P1.
A **second** published-default super-admin: a `platform_admins` row whose **bcrypt hash is committed
with its PLAINTEXT in a comment on the line above** (verified by `bcrypt.compare` **with a negative
control**). Worse than the row KS-949 fixes because: `routes/auth.ts:344-346` checks that table
**FIRST**; `:381-383` hardcodes `role: SYSTEM_ADMIN` / `status: ACTIVE` so **row status is never
consulted**; and `deployment/azure/migrate/run-platform.sh:124` **re-asserts the published password
on EVERY run**, including on an already-seeded box. **Do not reproduce the plaintext or the hash in
any artefact.**

## PR / MERGE STATE — verified at origin
```
develop 61df129e9c580e3b4622d9b5de11f2abd765b8f6   THREE MERGES TODAY; it had not moved before today
  306d0db92 -> db94e9fc8 (#884 KS-858/F5) -> 603b0a017 (#882 KS-698) -> 8aefd2b06 (#876 r3) -> 61df129e9 (#886)
#885  a98df6b11  KS-949  NO GO -> round 2 IN FLIGHT (Kam authorised) + the probe
#874 #879 #880 #881 #883 — untouched today
```
**#880/KS-577 STAYS KAM'S** — merging it silently picks Option 1 for Platform S, a client-facing
commitment. A merge is Wednesday's; a merge that decides something with a client is his.

## s145's QUEUE after #885 round 2 (it was DISPLACED and returns)
1. **KS-645 correction + fold into KS-952.** KS-645's headline is **false and was false at base** —
   the role guard is an ancestor of base and `ISSUER_ADMIN` → 403 at the wire at both SHAs; `git grep
   "KS-645"` → zero hits. The **real** residue is cross-tenant (a `SYSTEM_ADMIN` in tenant A clears
   tenant B's bucket). **One mechanism, TWO ASYMMETRIC RULES** — `/check` wants strict
   derive-from-principal; `/reset` wants platform-may-name-any / tenant-may-name-own, because strict
   binding there **breaks** a real capability.
2. **KS-597** — forward fix committed at the checkpoint; the fallback is deliberately NOT written
   (`organization_members` = 0 rows, so it cannot be exercised — it is a ticket carrying that
   measurement as its blocker). **Kam ruled `afterfix` on the 95k backfill: it is its own round AFTER
   the fix merges, never before.**
3. **CI wiring, NON-BLOCKING** (Kam 10:41 `wire-nonblocking`). Report the first run's numbers:
   workspaces run, `--if-present` skips, failures, wall-clock.

## KAM'S DESK — 1 open
`workspace-dead-secuura-tenant-cleanup` — **actually already ruled `grant` at 10:50 and EXECUTED**;
the card just needs marking. The three carriers were fixed: the runnable `az account set` in
`CLAUDE-reference.md:83` commented out with the live Founders Hub values added, the **new-project
launcher template** repointed with a warning, and the dead `azureProfile.json` **quarantined by
rename**. The warning at `/Volumes/DevMASTER/CLAUDE.md:29` was deliberately KEPT — it is the guard.

## MECHANISMS BUILT THIS SEAT
- **`pretooluse_no_cd.sh` now refuses `git -C <path outside WEDNESDAY>` + a WRITE verb.** 15 fixtures,
  5 refuse / 10 pass. **It bricked itself once** (a literal quote inside the single-quoted embedded
  python) — **a gate in the path of every call is in the path of its own repair; only a non-Bash tool
  got it back.** It **fail-closes on `$VAR` paths by design** — write the literal path for your own
  repo. Backup `.pre-0907-gitwrite`.

## STANDING NOTES
No `cd`. Tap ≤200 chars, and **every tap has a mail behind it, verified by `preview` being non-null**.
`<<'EOF'` for every brief. **What merges must be what was gated** — do not amend a branch after its
gate. **A merge GO authorises the base-ref check and any retarget needed to make its destination
true** (GitHub does not retarget a stacked PR when its parent merges; the API reports `merged: true`
either way). **Name the field that decides WHOSE a thing is** — a commit names remote+branch, a ticket
names board AND assignee, a selection rule names its ownership predicate. Never delete — quarantine.
**The base-column criterion (`base rc1 → head rc0`) is RETIRED as an authorising test** — it does not
discriminate.
