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
**⚠ TWO mechanisms carried the old number and only one of them is RUNNING the fix.**
- `Launch_Wednesday.command` — **FIXED** (it had said 70% through TWO band rulings). Backup
  `.pre-0907-band8090`; verified by extracting `INITIAL_PROMPT` and asserting its length + tail.
- `fleet/cockpit/wake_watch.sh` — **FIXED ON DISK, NOT RUNNING.** A new **90% CEILING** leg was added
  (there was none: the old top leg was 80, fired once, so a seat running to 95% got no further wake),
  80/70 re-worded to the 80–90 band, and the 65 leg demoted from *"mechanical tails only, then
  handover"* — which at 65 with a 90 ceiling would idle a seat for 25 points — to *"keep the handover
  current, do NOT wind down."* Exercised on nine values (95/90→CEILING, 85/80→BAND, 75/70→CHECKPOINT,
  66→light, 55→checkpoint, 40→none). Backup `.pre-0907-band8090`.
  **IT IS LIVE.** Wednesday first wrote that the running watcher held the old code and **that was
  wrong** — the next 70% wake arrived quoting the new wording (the phrase occurs 2x in the live file
  and 0x in the backup). Pid 2403 is the RUNNER; it invokes `wake_watch.sh` fresh each tick. **Trust
  the wake wording: if it cites 'Kam 09-07 10:49' it is the corrected file.**

The launcher said **70%** until this seat fixed it — it was **two rulings stale** and is why seats
kept rotating early. Fixed in `Launch_Wednesday.command`, verified by extracting `INITIAL_PROMPT` and
asserting its length (11,150) and tail. Backup `.pre-0907-band8090`.

## 🔴 FIRST ACTION FOR YOU — read Kam's ruling on `secuura-ks949-round3-cap-and-the-cutoff`. Nothing moves until he rules.
**#885 round 2 came back NO GO on `6dbe63cae` at 12:02. That SPENDS Kam's two-round cap.** The card
is on his desk with four options; **recommendation = `split`** (revert F1 only, ship F2–F5, F1 gets
its own round) because that is his own cap applied as written and the four are genuinely closed.
**Default if he is silent: nothing merges, nothing deploys, #885 stays at `6dbe63cae`.**

### 🔴 THE FACT THAT CHANGES EVERYTHING — nothing currently removes Kam's address
**The auth remediation — established as the ONLY path that would rewrite his row — is DISABLED on
prod-like environments.** `decryptEmail` throws on a non-ciphertext value once
`plaintextStillAcceptable()` is false, which it is whenever `NODE_ENV` is production/staging/demo
**and** the date is past `PII_PLAINTEXT_CUTOFF` (**2026-06-01, set NOWHERE in the repo — the source
default applies**). `getUserById` catches and returns **null**, so the remediation reads it as *"no
pre-existing row to remediate"* and skips. **All three deployment values are prod-like**
(`services.bicep:564` defaults to `staging`; `env.demo.json:8` says `production`).
**Four cells, two of them controls isolating the cutoff rather than the row shape.** The builder's own
suite **cannot see it**: its mock forces `isEncryptedPii: () => false` (test line 40) and runs
`NODE_ENV=development` (line 88). **So round 3 alone may not remediate anything either.**

### Why shipping this head was NOT offered to Kam as an option
It would write **twelve plaintext addresses into an encrypted column** on the first boot after a
deploy — and **eleven of the twelve are the documented public demo personas** the credential sheet
publishes and `scripts/auth-matrix-smoke.sh` drives. **Not a back-office table.**
**Also measured: Kam's old address remains the LIVE LOGIN KEY for a SYSTEM_ADMIN row** —
`auth_find_user_by_email_hash(<old hash>)` still returns it. The accurate description of the fix's
damage is **FINDABLE, THEN UNREADABLE**, not "unfindable" — the gate corrected Wednesday and the
builder on that, in both directions.

### A THIRD schema source, for KS-960
**The Azure deploy applies `deployment/azure/migrate/init.sql`** (`run.sh:26`, `run-platform.sh:25`) —
not `docker/init`, not `migrations/001`. It declares `email VARCHAR(255) UNIQUE` with **no
`email_lookup_hash`**; `migrations/030_auth_user_columns.sql:36-44` then converges it onto the
docker/init shape. **F1's 42P10 diagnosis survives that**, measured by the gate in its own container.

### The shape already ratified, for whenever Kam authorises the fix
**Option (b): the migration REMOVES its INSERT** and keeps the PK conflict target used **only** to
re-sync `tenant_id`/`tenant_slug` on rows that already exist. Rationale that decided it: **auth
already creates all twelve identically**, and on a stack where the migration has thrown every boot
since encryption landed **all twelve exist, ciphertext, hashes set** — *"we are not proposing to
remove a load-bearing statement, we are proposing to delete one that has never borne load."*
**The new regression cell must drive BOTH seeders against ONE real database in BOTH orders, on the
docker/init shape, and must NOT stub `isEncryptedPii`** — that stub is what blinded the builder's suite.

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
