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
SEE THE BLIND SPOT BELOW: it reads the shared panel correctly, but five of his rulings today never
reached that panel at all, by a channel that is still UNMEASURED.**

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

### ⚠ THE BLIND SPOT — the OBSERVATION stands; the MECHANISM in the 12:30 wording was REFUTED
**Corrected by the 12:4x seat, measured not argued.** The 12:30 wording said `kam_rulings_today.sh`
"reads ONE panel" and Kam "ruled five times on the other one". **There is no other panel.** There is
ONE shared `chat_log.json` (1,589 messages at 12:4x, monotonic, both seats append, nothing
overwritten) — and the phrases from all five rulings appear in it **zero times in Kam's voice**
(`"between 80 and 90"`, `"rotation window"`, `"unpause"`, `"Marketplace"`: one hit each, every one
authored by Wednesday, not by Kam).

**What IS true, and it is the part to act on:** Kam ruled five times today (10:15 review scope ·
10:44 Vision parked + pre-production · 10:46 NexusAI unpaused · 10:48 the Marketplace objective ·
**10:49 the rotation band → 80–90%**) and **none of those words reached the shared record at all.**
They arrived only because the laptop seat pushed a file and the Studio seat read the commit.
**So the boot rule "read his rulings before writing anything" silently covers only the words he
types into the panel.** The channel the other five travelled on is **UNMEASURED** — pane-typing is
the known habit ([[2026-08-05_kam-types-into-panes]]) and has NOT been established. **Do not hand
Kam a remedy built on the two-panel story: the two explanations imply different fixes.** Raise it as
the observation plus the unmeasured channel. **Not yet ruled.**

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

## 🔴 FIRST ACTION FOR YOU — read s145's merge receipt + rotation measurement, then decide if it hands over
**#885 IS MERGED.** develop `61df129e9` → **`632f16dfe62f4c498a73ca09a39cadaf6eeab764`** (12:24).
**FOUR MERGES TODAY**; develop had not moved at all before this morning.
**Wednesday verified all FIVE of today's merges are ancestors of `632f16dfe`** — #885's branch was cut
before today's merges, so it was a genuine three-way and nothing was silently reverted.

**s145 is at ~70% and was sending its merge receipt AND the rotation measurement together when this
seat rotated. READ THAT MAIL FIRST.** Early figures visible on its pane (its measurement, not
Wednesday's): **93 executable / 87 documentary** occurrences of the retired credential, and
**104 flat spec files in `Blockchain/Dev/tests/` that are in NO playwright config's `testDir` and
referenced by no runner** (it ran a control). **That reshapes the rotation job and it is the seat's
finding — do not restate it as Wednesday's.**

### 🔴 THE DEPLOY — do NOT let it look like Kam's problem is solved
**After the revert, NOTHING IN #885 REMEDIATES KAM'S ROW.** The fix that would have is the one that was
taken out. **A deploy today ships four real improvements and does nothing about his address.**
Kam has been told exactly that. **He has an active deploy grant and a production grant (Secuura only,
this week) — so a deploy of F2–F5 is available and is Wednesday's to make — but it must be flagged as
what it is.** Do not deploy silently and do not let a receipt imply remediation.

### WHAT KS-962 AND KS-963 CARRY (filed, do not re-derive)
- **KS-962** — F1's own round. **The ratified shape: the migration REMOVES its INSERT** and keeps the
  PK conflict target only to re-sync `tenant_id`/`tenant_slug` on existing rows. It also carries
  **what NOT to do** — why repointing the conflict target is worse than the bug. **The new cell must
  drive BOTH seeders against ONE database in BOTH orders, on the `docker/init` shape, and must NOT
  stub `isEncryptedPii`.**
- **KS-963 (P1)** — the PII cutoff, **with BOTH readings**: the gate's mechanism proof (4 cells, 2
  controls) AND the two conditions that bound it. **`NODE_ENV=development` on the demo VM was
  measured** (pre-registered, hashed before the read) — **so condition B fails and the cutoff cannot
  fire there.** The sharp edge that survives regardless: **`getUserById` collapses "the encryption
  migration is incomplete" and "no such user" into one answer**, which is what makes the failure silent.

### ⚠ THE RECONCILIATION — carry it, do not re-open it
The gate's `services.bicep:564` (staging) and `env.demo.json:8` (production) are **real** — they belong
to the **RETIRED Container Apps estate**, not the running VM. **The gate and the seat were measuring
different environments. Neither was wrong.** Anyone re-reading those two mails will think they conflict.

## 🔴 s145 IS EXECUTING THE ROTATION — shape RATIFIED, order 1,2,4,3, then tickets
Kam ruled `rotate-properly` (11:43:32). **s145's measurement made the job much smaller than the card
he ruled on, and he has been told: of 183 occurrences the real surface is ~32**, because
**43 sit in `Blockchain/Dev/tests/` spec files that NOTHING RUNS** (in no playwright config's
`testDir`, referenced by no runner, with a working control). Split: **93 executable / 87 documentary**;
the 93 splits again into **8 env-var-with-published-fallback · 12 comments · 73 hardcoded**.

**AND THERE IS NO NEW SHARED SECRET TO DISTRIBUTE.** The machinery exists
(`systemTest/playwright/config/environment.ts:185` reads `getGeneratedActor(ADMIN_ACTOR_KEY)?.password`;
`provision-actors.ts` provisions per run). **The published default is the fallback that makes it moot.**
So the rotation collapses into a deletion — no second rotation waiting later.

**Ruled order:** (1) the 8 fallbacks — delete the default, keep the var, fail closed **[FIRST: it holds
the live defect `userRepo.ts:1071`]** · (2) the 5 CI sites — remove the literal (Actions is retired,
they cannot break a run that does not happen) · (3) the 4 startup/scripts + 3 harnesses — env var, no
fallback · (4) the 12 systemTest sites — route through the generated-actor path **[LAST of the code:
it is a routing change, the only real regression risk; prove the actor path resolves BEFORE removing
the fallback]** · (5) the 43 dead specs → **own ticket, quarantine not delete** · (6) the 87
documentary → own pass, after.

**⚠ FLAG TO KAM WHEN IT LANDS:** after step 1, **an unset var seeds NO admin rather than a known one**
— a behaviour change on anything relying on the default, and it goes to him under the production grant.

**s145 was at ~70% and told to do 1 and 2, push, then judge honestly whether 3 and 4 fit — and to wrap
with a handover rather than push anything half-done.** Check which it chose before assuming.

## PR / MERGE STATE — verified at origin 12:2x
```
develop 632f16dfe62f4c498a73ca09a39cadaf6eeab764   FOUR MERGES TODAY, all five verified as ancestors
  306d0db92 -> db94e9fc8 (#884 F5) -> 603b0a017 (#882) -> 8aefd2b06 (#876 r3) -> 61df129e9 (#886)
            -> 632f16dfe (#885, the split: F2-F5 shipped, F1 reverted to round-1 state)
#887  bb0502c80  KS-961 workspace-suites advisory lane — OPEN, needs a gate when Kam wants it
KS-597 af640e809 pushed, NO PR yet — ask s145 if one is wanted
#874 #879 #880 #881 #883 — untouched today
```
**#880/KS-577 STAYS KAM'S** — merging it silently picks Option 1 for Platform S.

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
