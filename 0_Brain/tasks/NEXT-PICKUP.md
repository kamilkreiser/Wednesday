---
date: 2026-09-09
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's — read her mail by SUBJECT only, never brief or answer for a Datasec project.
source: replaced WHOLESALE at 12:5x by the seat that booted 12:37, because the previous version said the repo was BLOCKED and it has been clear since 12:01
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — 2026-09-09 12:5x. SECUURA IS CLEAR. THE BLOCKER NOW IS APPROVAL, NOT PUSH.

> 🔴 **THE VERSION THIS REPLACES WAS DANGEROUSLY STALE.** It was written at 08:3x and its
> first heading read *"the repo is BLOCKED and ONE Kam ruling clears everything"*. That was
> true when written and became false at 12:01. It was still the file a successor is told to
> read FIRST. Replaced wholesale rather than appended, per this file's own rule.
> **The full, current state is the 12:17 handover block in `0_Brain/daily/2026-09-09.md`** —
> this file carries only what is still OPEN and whose it is.

## 🔴 THE ONE ASK ON KAM, AND IT IS TWO WEEKS OLD

**Invite an agent account to the Secuura GitHub org with write on `Distributed_Secuura`.**

He **already ruled this** — card `secuura-agent-github-identity`, choice `identity`,
ruled **2026-08-26T17:12**. It was never executed, and it cost real time today: at 11:45
the seat attempted the approvals Kam authorised at 11:39 and GitHub returned **HTTP 422,
"Review Can not approve your own pull request", on BOTH PRs** — `kksecura` opened them and
`kksecura` is our PAT. Kam hand-merged #914 and #915 instead.

**Four PRs are ready and every one of them meets the same wall.** Raised to him at 12:5x.
**Do not work around it** — no `--admin`, no force. It is his one action.

## 🟢 STATE — verify before acting on any of it

**Secuura `develop b6884888d`, CLEAR.** Every author can push, measured 12:01 on three
agreeing instruments (ancestry with a discriminating control · both audit legs
EXIT=1 → EXIT=0 with 0 unbaselined and the count falling 41 → 36, exactly the five the
bump removes · the pins read out of develop's own lockfiles). Residual, stated so it does
not return as a false re-block: a fresh worktree still meets leg 1 `DEPS MISSING` — that
is an environment condition, not the repo.

**READY, NONE MERGED:** **#916** (KS-993 + KS-1026, head `584b12ba1eed`, retargeted to
develop today) · **`ed954f09e`** (KS-926 — ⚠ **NO PR EXISTS FOR IT AT ALL**; real work,
14/14 preflight, and nothing tracking it for review) · **#887** (KS-961, Peter holding on
one named line; unblocked for free now that develop's advisories are gone) · **#879**
(KS-945, retargeted today). **#912 STAYS HELD** — NO GO; its api-gateway `confidence` fix
must land with or before it.

**FLOOR:** empty of agents at 12:5x. Wednesday `%0` · `%1` monitor.

## 🔴 THE ONE THAT OUTLIVES TODAY

**NO DEPLOY without migration 048 applied FIRST.** On KS-1031 and in #914's PR body.
`run-migrations.sh` **exits 0 when migrations fail**, so compose's own
`service_completed_successfully` gate does not catch it. If it is missed, every connector
erasure anonymises, shreds the DEK and then aborts deterministically, and the connector's
unbounded retry never succeeds. **Kam's production ban is lifted this week, which is
exactly why this must not go quiet.**

## 🟡 WITH KAM, HIS HANDS

- The **GitHub identity invite** above — the priority.
- The **Peter/Stuart unblock message**, drafted 11:47 and paste-ready, nothing in it that
  is not already on a ticket. **Default if he is silent: nobody is messaged.** They have
  been blocked, so silence is probably not what he wants — say so rather than let it lapse.
- Whether an agent opens the **missing KS-926 PR**.
- The **eight advisory acceptances as ONE review**, well before the 2026-09-24 re-triage.
- The workspace `CLAUDE.md` tenant section is **behind what he said at 12:15** (two dev
  tenants — his kreiser.org one, and the developers' one). Shared file, his call.

## 🟠 OWED BY WEDNESDAY — and they are ONE FAMILY, which is the new part

Three fleet tools hardcode **Wednesday's identity** and misbehave at Tuesday's seat. They
were all written when there was one coordinator, and the 09-08 split made every one of
them wrong. Kam has an open card on the first instance only (`wed-wakewatch-...`,
rec `parameterise`); it was raised to him at 12:5x that it is a family of three.

1. **`wake_watch`** polls WEDNESDAY's inbox on whichever seat runs it — it fired at
   Tuesday this morning. **This is the open card.**
2. **`send_brief.sh:24`** hardcodes both the sending inbox AND the sender prefix, so
   **every mail Tuesday sends through it goes out as Wednesday.** Tuesday measured this.
   Shared file; sequence it when no seat is live on it. **This is the worst of the three.**
3. **`statusline`** — ✅ **FIXED 12:5x** (`2_Project_Files/tools/statusline_publish.sh`,
   seat name passed as an argument, no hostname fallback). Kept here as the worked example
   of the fix shape, not as outstanding work.

Also still owed, unstarted: the **pre-push marker hook** (claimed via `wed_claim.sh` 11:08,
Tuesday's design adopted whole — she declined the window, it stays Wednesday's) · the
**"READY FOR QA" artefact rule**: no brief has ever said what READY means as an artefact,
which is how a whole seat's work ended up with no PR.

## WITH TUESDAY, HERS NOT MINE

Four Datasec cards ruled 12:09 and transcribed by Wednesday (`all-three` · `round3` ·
`name-tenant` · `structural-look`). ⚠ **`name-tenant` is ruled WITHOUT its answer** — the
option text is *"Tell Wednesday which tenant"* and Kam has still not named the ID. The card
reads `ruled`, which is exactly what stops anyone asking. The target is **the developers'
dev tenant, NOT kreiser.org** — his own words, relayed verbatim. **Wednesday deliberately
did not guess the ID** despite an obvious candidate, because the workspace file says the
mapping is unresolved and must not be asserted until checked.

Briefed to her 12:51: pull, point her statusline at the wrapper, and **commit
`usage_tuesday.json`** — her seat is on another machine and the repo is the only thing that
carries that file to Kam's dashboard.
