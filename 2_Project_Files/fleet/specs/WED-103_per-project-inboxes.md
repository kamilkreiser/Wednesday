# WED-103 — per-project inboxes with inbox-scoped keys

**Status:** inboxes CREATED + isolation PROVEN 2026-08-13. Migration pending
(each project's own agent executes; the shared-file edit is Kam's).
**Authorised by:** Kam, 2026-08-13 ("go ahead and set up the per-project
inboxes"), after upgrading Agent Mail to Developer the same evening.

## The problem this closes

`coagent@agentmail.to` is a SHARED bus carrying every client's traffic. On
2026-08-13 a Datasec/HPSM poller filtered it on message class (`'ANSWER' in
subject`) without the project tag, captured a **Secuura** message's headers
and ~400 characters into a Datasec scratchpad, and self-disclosed it. The
agent's own diagnosis was right: *"this is a fleet-protocol gap, not an HPSM
bug"* — every agent polling the shared bus has the same exposure, and a
tag-filter you must remember to write is not a mechanism
(`0_Brain/learnings/2026-08-13_shared-bus-tag-filter-or-leak.md`).

Hard rule 2 (no cross-client contamination) was being enforced by
instruction. This makes it structural.

## What now exists

| Inbox | For |
|---|---|
| `wednesday-agent@agentmail.to` | Wednesday (coordinator) — unchanged |
| `secuura-blockchain@agentmail.to` | Secuura / Blockchain (Platform K) |
| `datasec-nexusai@agentmail.to` | Datasec / NexusAI |
| `datasec-vision@agentmail.to` | Datasec / Vision Sales Portal |
| `datasec-hpsm@agentmail.to` | Datasec / HPSM |
| `coagent@agentmail.to` | LEGACY shared bus — retire after migration |
| `secure_abacus@agentmail.to` | legacy, 0 messages, unidentified — leave alone, ask Kam |

7 of 10 inboxes used. Dormant projects (Tokenomics, CypherKey, Lead_Bot,
myPKI) get an inbox **when first delegated to** — same discipline as
`launchers.conf`. That leaves 3 free; if the fleet needs more than 10 the
next tier is a Kam money decision, not a quiet upgrade.

## The isolation is PROVEN, not assumed (exercised 2026-08-13 before arming)

A key scoped to `secuura-blockchain@` was minted and tested against every
path that matters:

| Test | Result |
|---|---|
| Read its OWN inbox (quiet path) | **HTTP 200** |
| Read another CLIENT's inbox (`datasec-hpsm@`) | **HTTP 404** |
| Read the SHARED BUS `coagent@` — *the actual leak path* | **HTTP 404** |
| **Enumerate all inboxes** (`GET /v0/inboxes`) | **`count: 1`** — only its own |

The enumeration result is the strongest: a Secuura agent holding a scoped key
**cannot learn from the mail layer that any Datasec project exists.** That is
R0 (client contexts structurally unable to leak,
`learnings/2026-08-04_delegation-v2-observability`) satisfied by construction
rather than by policy. The 404 rather than 403 is a bonus — the boundary does
not even confirm the other inbox exists.

Test key deleted afterwards; see "Revocation" below for what that taught us.

## Migration — who does what, and why nobody carries a secret

**The rule that shapes this** (`learnings/2026-08-06`, the Vision SP secret):
*if a workflow requires a human to carry a secret between two places, the
workflow is the defect.* So no key is ever mailed, pasted, or relayed.

1. **Wednesday (done):** create the inboxes; prove isolation; write this spec.
2. **Each project's own agent, at its next session start**, under a brief:
   - mint its OWN inbox-scoped key with the account key it already holds:
     `POST /v0/inboxes/<its-inbox>/api-keys` with a name like
     `<client>-<project>-agent`;
   - write it to its OWN `4_Credentials/.env` as `AGENTMAIL_API_KEY`,
     **replacing** the account-wide key (gitignored, 0600, never echoed);
   - verify BOTH directions before reporting done — its own inbox returns
     200 AND `coagent@` returns 404 (a check that cannot fail is not a check);
   - switch its comms to: read its own inbox, send to `wednesday-agent@`.
   The secret is created and consumed inside one process in its own project.
   Wednesday never sees it. Hard rule 1 is untouched — I brief, they execute.
3. **Kam only:** the shared workspace `CLAUDE.md` fleet-comms section (it is
   cross-client, so it is his hand, not mine and not a project agent's).
   Draft text is in `WED-103_workspace-claude-md-draft.md` alongside this file.
4. **Retire `coagent@`** only when every active project reports migrated.
   Until then it stays readable — Wednesday keeps reading both, since the
   coordinator is the one role legitimately spanning clients.

## Revocation is EVENTUALLY CONSISTENT — measured, ~5–8 minutes

**Corrected 2026-08-13, same session, before this spec was relied on.**

Deleting an inbox-scoped key returns **HTTP 204** and the key vanishes from
the account listing (`count: 0`) **immediately** — but the key keeps
authenticating for several minutes afterwards. Measured with a polling probe:
repeated `200`s, then **`403` at t+299s on the probe's own clock**, with the
DELETE occurring shortly before the probe started. So the real
deletion-to-invalidation window is **roughly five to eight minutes** — bounded,
not pinned, because the timer started after the delete.

**My first reading of this was wrong and is recorded so nobody re-derives it:**
two spot checks inside that window showed 200 and I concluded revocation was
not enforced, which would have meant *"rotate the key" is not an available
incident response*. It is available. The observations were real; the
conclusion was premature. A report and then a correction both went to
AgentMail support the same evening.

**Operational rules — unchanged in substance, and they are what caught it:**
1. **Never report a credential retired on the strength of a 204.** Poll the
   old key until it actually fails. This is
   `learnings/2026-08-06_never-discard-stderr` corollary 3 (distinguish
   "failed" from "not ready yet") pointed at teardown instead of setup —
   cloud identity is eventually consistent in BOTH directions.
2. Treat an issued scoped key as **live until proven dead**, and keep issued
   keys minimal and named — one per project, no throwaways left behind.
3. **If a key is known-leaked, five minutes is the exposure.** Plan for it:
   revoke first, then treat the window as live-compromised rather than
   assuming instant containment. Asked support whether immediate forced
   invalidation exists; answer pending.

The account-side hygiene is clean — no orphan key records, no key material on
this drive.

## What this does NOT fix

- **Wednesday's own key stays account-wide** — the coordinator must read
  every project's mail. If my key leaks, the whole estate is exposed. That
  is a real residual and it is the correct one to keep: one broad key held
  by the one role that needs breadth, versus five broad keys held by roles
  that do not.
- Anything an agent has ALREADY read from the shared bus is not un-read.
- It does not stop an agent quoting client content into the wrong file; it
  stops it acquiring that content by accident in the first place.

### Two residuals found AFTER arming (2026-08-13 ~22:2x)

**1. A scoped key is also a key-MINTING authority for its own inbox.** Found by
the Secuura/Blockchain agent during its migration and disclosed unprompted:
`POST /v0/api-keys` with an inbox-scoped key returns **200** and creates a
further key — scoped to that same inbox (verified on the created key's
`inbox_id`). `POST /v0/inboxes` is refused **403**, and `GET /v0/api-keys` with
a scoped key returns **count 1** (its own only, no enumeration of other
clients'). **So containment holds and the blast radius is unchanged** — this is
key proliferation *inside* one boundary, not privilege escalation. But the
model stated above is corrected: a scoped key is not "read and send for one
inbox", it is **"read, send, and mint further keys for one inbox"**. Accepted as
a residual, not a design defect.

**3. Migrated agents can no longer re-verify Kam's v1.3 grant (found 2026-08-14,
Secuura/Blockchain s30 boot).** The signed delegation grant
(`<8DF1B897-3EC1-453C-8301-51F4090B3DA9@me.com>`, dkim=pass header.i=@me.com) lives
on `coagent@`. A project's inbox-scoped key returns **404** there by construction —
which is the isolation working — so **the artefact the protocol requires every
agent to re-check each session is now permanently unreachable from every migrated
project.** HPSM was already in this position and had not noticed; NexusAI and
Vision inherit it on migration.

**This is a defect in this design, not in any agent.** It was surfaced by an agent
doing its boot verification properly and flagging that it could not complete a
required check, rather than skipping it silently.

**The fix is Kam's hand and cannot be mine: he re-sends the signed grant to each
per-project inbox.** A forward from me carries the platform's signature and mine,
not his — the relay v1.3 exists to refuse. *A grant I could send myself would
authorise nothing* ([[2026-08-07_protocol-v1.3-signed-delegation]] point 3). **If I
ever offer an agent a forwarded copy, the correct response is to refuse it.**

**Interim (in force):** each agent's own recorded verification — Message-ID plus
full auth results in its `history.md` from its last bus-access session — is
provenance for **non-approval-class work only**. On the first approval-class
action, the agent HOLDS. Tracked as **WED-108** (P1). Add the re-send to the
create-an-inbox checklist so a new project never starts in this state.

**2. Five LEGACY ORG-WIDE keys predate this migration and each spans every
inbox** — `multi-agent`, `secure_cursor`, `secure_test_claude`, `coAgent`,
`Clara`, all created 2026-03-15 → 2026-04-19, i.e. months before the per-project
inboxes existed. **This is the real bound on the isolation proven above.** The
404s are genuine for the scoped keys; they say nothing about a process still
holding one of these five. Whoever holds `coAgent` or `Clara` today can read
every project's inbox, including all four new ones — which is exactly the
cross-client exposure WED-103 exists to remove, reachable by a different door.
**Not actionable by me:** deleting a key is irreversible and may break a running
side project, so it is Kam's signature class. Raised as an audit item
(**WED-107**): identify what holds each of the five, retire or re-scope what is
dead, and keep only what genuinely needs breadth. Discovered while independently
verifying the Secuura agent's incident disclosure — the audit was not the
purpose of the check, which is usually how these are found.

**Related:** `0_Brain/learnings/2026-08-13_shared-bus-tag-filter-or-leak.md` ·
`0_Brain/learnings/2026-08-04_delegation-v2-observability.md` (R0) ·
`0_Brain/learnings/2026-08-06_exercise-mechanisms-before-arming.md` ·
`0_Brain/learnings/2026-08-09_an-enforcement-you-must-arm-is-not-one.md`
