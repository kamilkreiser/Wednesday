# [Secuura/Blockchain -> Wednesday] QUESTION: status item4 ticket text ready (Seat B 51st): the search NARROWED it - KS-1376 already covers the certifications half and its after-039 fix reaches already-migrated DBs too, so the text is charge_events only (8 rows, RLS never enabled); nothing filed

**ITEM 4's text is ready — and the board search NARROWED it from two tables to one. KS-1376's fix already covers the `certifications` half.** Nothing filed, nothing posted. Please read my ctx.

## 🔴 THE FINDING THAT CHANGES THE TICKET
The brief's draft filed **both** `charge_events` and `certifications` as one new finding. **Reading
KS-1376 in full — which the brief flagged as UNMEASURED and told me to do before filing — says the
`certifications` half should not be re-filed.**

KS-1376 (Backlog, created 2026-09-28T21:22:17Z, from the gate39 pass over #1332) is
*"Security: certifications ends RLS FORCE with no tenant_isolation policy on every fresh database,
permanently"*. **That is B 50th's `certifications` reading exactly** — forced, 0 policies.

Its stated fix shape is *"a migration numbered **after 039** that applies 039's `tenant_isolation`
block to `certifications`"*. **A migration numbered after 039 is unrecorded on EVERY database,
including one already past 039** — that is the whole mechanism B 50th's finding rests on, running in
our favour. **So KS-1376's fix, when it ships, also remediates kintsugi's `certifications`.** Its
title says "fresh database" and its cause differs, but its remedy reaches both.

**What no ticket covers is `charge_events`:** RLS **not enabled at all** (`relrowsecurity=false`,
`relforcerowsecurity=false`), 0 policies, and **8 rows already in it** — the only one of 038a's four
tables holding data. So the ticket I have drafted is scoped to **`charge_events` plus the
already-migrated mechanism**, and it states in the body why `certifications` is not re-filed.

**Your STOP condition, read strictly:** KS-1376 does not cover "an already-migrated database never
receives 039's policies" — it is scoped to fresh databases and to one table. So I did not stop on it.
But it covers half the symptom, which is enough that filing the brief's two-table draft would have
duplicated an open Backlog ticket. **If you would rather the new ticket carry both tables, or be a
comment on KS-1376 instead, say so — that is a scoping call, not a measurement.**

## THE SEARCH (STANDING_LINES :98-:100), re-run with a positive control
Team KS, `includeArchived: true`, on **title AND description**, paginated:
- `charge_events` **7** hits — none about RLS (metering auth, PII payload, billing wiring, a regclass
  migration abort, a metering write, a CORE_MIGRATIONS env).
- `039_rls_fail_closed` **6** — KS-1055, KS-1054, KS-1050, KS-943, KS-578, KS-467.
- `relforcerowsecurity` **1** — KS-959, which is KS-597's org-context fallback; it cites forced RLS
  only to explain why a zero row-count needs a control. **Not a cover** (I closed this earlier).
- `certifications` **50, hasNextPage true** → this is where KS-1376 surfaced.
- `tenant_isolation` **20** → KS-1376 and KS-1054 first.
- **Positive control** `migration` → **50**, so the query shape returns non-zero.

Closest three re-read live: **KS-1054** In Progress (board account), **KS-1376** Backlog unassigned,
**KS-1055** Backlog unassigned.

## FACTS RE-CHECKED AT SOURCE, not carried from the brief
From B 50th's own `boot/probe_rls.out` and handover `:104-:136`:
```
certifications relrowsecurity=true  relforcerowsecurity=true  policies=0   rows 0   cols 17
charge_events  relrowsecurity=false relforcerowsecurity=false policies=0   rows 8   cols 12
oauth_apps     relrowsecurity=true  relforcerowsecurity=true  policies=2   rows 0
svc_webhooks   relrowsecurity=true  relforcerowsecurity=true  policies=1   rows 0
CONTROL users  relrowsecurity=true  policies=2 | fake policy 0 | to_regclass(fake) false
```
**Re-check (b) closed with a citation, so the clause KEEPS:** api-gateway's startup stage skips a
recorded file at `services/api-gateway/src/startup-migrations.ts:137-141` —
`SELECT 1 FROM _secuura_migrations WHERE filename = $1 LIMIT 1` then
`if (existing.rows.length > 0) continue;`. Read at `91a8f6b721bc`. Paired with
`run-migrations.sh:118-122`, **both** runners skip, each now with its own line.

## THE TEXT — saved, NOT posted
`5_Project_History/2026-10-01_seatB-51st/item4/`
- **title** 121 B, sha256 `1facfe057646fd82`
- **description** 5364 B, sha256 `c99de066b941f0cb`
- Client-visible vocabulary swept: **0** hits for seat / pane / fleet / Wednesday / tmux / Claude /
  agent / Kam / Stuart / Peter / worktree.
- Hyphenated keys: KS-1054 (3), KS-1055 (2), KS-1376 (2), KS-597 (1), KS-959 (1) — all
  cross-references in a description, which attaches nothing. **None belongs to Stuart or Peter**, so
  no back-reference lands on a person's ticket, which was your concern on KS 1395. `KS 458`
  de-hyphenated. **Say if you want any of these de-hyphenated too.**

### TITLE, verbatim
```
charge_events has RLS off entirely on every database already past 039, and 8 rows are in it — a redeploy cannot fix it
```

### DESCRIPTION, verbatim
```
## BLUF

**On a database that recorded `039_rls_fail_closed.sql` before `charge_events` existed, that table ends with row-level security not enabled at all — no RLS, no FORCE, no policy — and a redeploy cannot change it.** Measured on the kintsugi database, which holds **8 rows** in that table. Both migration runners skip any file already recorded, so 039's edits are inert there, and `038a_ks1054_core_tables_before_039.sql` only helps a database whose 039 has not yet run. No fix is proposed in this ticket.

## Measured

Read on the kintsugi main database before and after the 2026-09-30 deploy, identical both times:

| table | exists | rows | RLS enabled | RLS forced | policies |
| -- | -- | -- | -- | -- | -- |
| charge_events | yes | **8** | **false** | **false** | **0** |
| certifications | yes | 0 | true | true | 0 |
| oauth_apps | yes | 0 | true | true | 2 |
| svc_webhooks | yes | 0 | true | true | 1 |

Controls read in the same session: `users` reads RLS enabled with 2 policies; a policy name that does not exist returns 0; `to_regclass` on a table that does not exist returns false. So the zeros above are readings, not a blind query.

**`charge_events` is the row of that table with no ticket.** It is also the only one of the four holding data.

## Why a deploy does not fix it

* Both runners skip a migration already recorded in `_secuura_migrations`: `scripts/run-migrations.sh:118-122`, and api-gateway's startup stage at `services/api-gateway/src/startup-migrations.ts:137-141`, which reads `SELECT 1 FROM _secuura_migrations WHERE filename = $1 LIMIT 1` and `continue`s when a row comes back. Both were read at `91a8f6b721bc`.
* `039_rls_fail_closed.sql` has listed `charge_events` since KS 458. It skips any listed table that does not exist yet, or that has no `tenant_id` column.
* `038a_ks1054_core_tables_before_039.sql` creates these tables **before** 039 runs, so a fresh database gets 039's policies on its first boot. On this database, 038a ran on 2026-09-30 **after** 039 was already recorded; its only effect there was one tracker row, the four tables already existing.
* So 038a cannot help a database where 039 has already run, and editing 039 itself reaches nothing — the edit to it inside the deployed range was inert on this box for exactly that reason.

**Unmeasured:** why `charge_events` was skipped when this database first ran 039. The consistent reading is that it did not exist yet, as 038a's own header describes for a bare database, but the original run's log was not read, and whether the table had a `tenant_id` column at that moment was not read.

## Relationship to the existing tickets — read before filing

* **KS-1376** covers `certifications` ending RLS FORCE with no `tenant_isolation` policy, and its fix shape is *"a migration numbered after 039 that applies 039's `tenant_isolation` block to `certifications`"*. A migration numbered after 039 is unrecorded on **every** database, including ones already past 039 — so **that fix also remediates the `certifications` row above.** The `certifications` half is therefore not re-filed here.
* **KS-1054** covers fresh databases being fail-open until the second boot, fixed by Secuura/Distributed_Secuura#1332.
* **KS-1055** covers per-tenant databases never receiving the file migrations.
* **What none of them states** is the case this ticket is for: **`charge_events` on an already-migrated database, with RLS never enabled and rows already present.** Searched team KS with `includeArchived`, on title and description, by `charge_events` (7 hits, none about RLS), `039_rls_fail_closed` (6), `relforcerowsecurity` (1, KS-959, which is KS-597's org-context fallback and cites forced RLS only to explain why a zero row-count needs a control), `certifications` (50, paginated) and `tenant_isolation` (20). Positive control `migration` returned 50, so the query shape works.

## Other environments

* A fresh database from `91a8f6b721bc`: covered by KS-1054's fix; not re-measured here.
* **demo: unmeasured.** The instrument that closes it is the same read-only catalog query — `pg_class.relrowsecurity` and `relforcerowsecurity`, the `pg_policies` count, the row count — against demo's main database.
* Any other database created before #1332 and already past 039: unmeasured.

## What done means

1. On every already-migrated database this applies to, `charge_events` has RLS enabled and forced with the `tenant_isolation` policy 039 defines, shown by the same catalog read before and after.
2. It is delivered by a path an existing database actually runs on deploy — a migration numbered after 039 — not by editing a recorded file.
3. A regression check that is red on a database where 039 was recorded before `charge_events` existed, and green after. Driven as the application role, not as a source-text assertion: the failure mode here is a runtime one, and only a driven probe separates "policy present" from "table reachable because the reader owns it".
4. The **8 existing rows stay readable to their own tenant** after the change, tested rather than assumed. This is the part that makes the change riskier than the `certifications` case, where the table is empty.

Related: KS-1054 (fresh databases, fixed by #1332). See also KS-1376 (the `certifications` row above, whose fix shape covers it) and KS-1055 (per-tenant databases).
```

Team KS, Backlog, board account, **one `related` relation to KS-1054** and nothing else. Posted only
on a GO naming Seat B 51st, with the gate's amendments, then read back by id and compared — and I will
report `cmp` honestly: Linear rewrote KS-1399's description on save (bold reflow around an inline-code
span plus a dropped trailing newline), so expect rc 1 with a token-stream proof rather than rc 0.

## STATE
**#1363 MERGED** (freeze lifted), **#1364 READY**, **KS-1399 filed**, ITEM 4 text ready. **ITEMs 2 and
3 go to my successor as UNRAISED**, as ruled. Writing the handover next while the gate runs.
**Fuse: 192.3 h, computed at 2026-09-30T23:44:11Z** — 3 rows at #1364's head, 4 at develop.

Watcher, `ps` in the same action as this sentence — and you were right that it was down: I had
re-armed it with `nohup … &` inside a shell that then exited, so it died with its parent. Re-armed
properly as a tracked background job:
```
90923       02:33 /bin/bash ./inbox_watch46.sh 2026-09-30T23:40:55.000Z 60
```
