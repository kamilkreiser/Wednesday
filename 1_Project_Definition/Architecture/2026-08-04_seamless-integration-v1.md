# Seamless Integration v1 — one surface for Kam, questions flow to Wednesday

Date: 2026-08-04 · Status: v1 built, for Kam's review · Ticket: WED-42 (Urgent)
Root cause being fixed: first-pilot friction (ledger 2026-08-03, w=1) — Kam had
to answer agent questions, step through approvals, and context-switch between
sessions. Design goals from the ticket: **one interaction surface for Kam;
Wednesday fields agent questions; only approval/ambiguity/decision-class items
escalate; no session-switching.** Hard constraint: structurally incapable of
cross-client leakage ("very important" #1).

Blueprint inputs: orchestrator-adws review adoptions #1 (two-tier summarization
context firewall) and #8 (async monitoring patterns — completion oracle,
sleep+check loop, anti-eager-polling), at
`0_Brain/reference/tac-course/orchestrator-adws-code-review.md`.

---

## Approaches considered (reject nine, keep one)

| # | Approach | Verdict | Why |
|---|---|---|---|
| a | **Mail Q&A + Wednesday monitors the inbox while a delegation runs** | **ADOPT (v1)** | Rides the proven fleet channel (2 pilot wraps + 1 instruction email already worked); mount-independent; zero new infrastructure; async-with-receipts matches fleet culture. |
| b | Wednesday spawns project sessions herself (Agent tool / `claude -p` in their folder) | REJECT for execution | Breaks identity isolation structurally: a subagent runs under *Wednesday's* session (her `gh`/`az`/permission state), not the project launcher's `GH_CONFIG_DIR`/`AZURE_CONFIG_DIR` scoping. Exactly the leak class "very important" #1 forbids. Launch via the project's own launcher (`open`) stays the pattern. Read-only scouts remain fine. |
| c | CoAgent bridge (real-time relay) | REJECT (decided 2026-08-03, WED-27) | Poll-both-channels protocol is an attention tax; same-machine fleet doesn't need websocket relay; real-time peer-to-peer is a gap we don't have yet. |
| d | Orchestrator UI (lesson-12 style) | DEFER → WED-46 | Right long-term surface; v1 must not block on a UI build. The mail loop becomes the data feed the dashboard later renders. |
| e | Vault instruction-files as the question channel (Kam's Obsidian idea) | REJECT for Q&A | Wednesday is vault-READ-ONLY — her half of a Q&A can't live there. Mail already covers async and works with the T9 unmounted. Idea stays good for *Kam→fleet* notes (his vault, his write access). |
| f | Linear comments as the Q&A channel | REJECT | Wednesday's tracker access is read-only ever (standing grant, 2026-08-03) — structurally cannot write answers there. Right place for *receipts*, wrong place for dialogue. |
| g | Shared file-drop on T9 as the question channel | REJECT | Requires the drive mounted in every project session; mail's whole advantage (proven 08-03) is mount-independence. |
| h | Agents ask Kam, Wednesday summarises after | REJECT | This is the anti-pattern being fixed. |
| i | Wednesday pre-answers everything in mega-briefs, no question path | REJECT alone | Over-briefing can't anticipate everything (pilot proved it). But the *instinct* survives as the brief-template tightening below. |
| j | Real-time polling loop at high frequency (< 1 min) | REJECT | Anti-eager-polling (blueprint #8): burns attention and tokens for no latency win on tasks that run tens of minutes. |

## The v1 loop

```
Kam approves brief → Wednesday emails instructions + launches project launcher
     │
     ├── project agent works; hits a question
     │     ├─ answerable from brief? → continues (brief tightening below)
     │     └─ else → EMAILS wednesday-agent@ (QUESTION convention)
     │                  ├─ can continue other work → says so, keeps going
     │                  └─ blocked → polls its inbox ~3 min for the ANSWER
     │
     ├── Wednesday (monitoring loop, sleep+check ≈ every 3–5 min):
     │     inbox digest (summaries firewall — subjects + previews only)
     │     ├─ QUESTION → triage:
     │     │    ANSWER    — from mental model, VALIDATED against the target
     │     │                project's own files (read-only) before sending
     │     │    ESCALATE  — approval/ambiguity/decision-class → Kam (one
     │     │                question per turn, spoken tap + text)
     │     │    REDIRECT  — belongs elsewhere; route it, cc the asker
     │     └─ wrap email → completion oracle: delegation over → score + close
     │
     └── Kam sees: ONE Wednesday session + occasional escalations. Nothing else.
```

## Conventions (the protocol on the wire)

**Question (agent → Wednesday):**
- To: `wednesday-agent@agentmail.to`
- Subject: `[<Client>/<Project> -> Wednesday] QUESTION: <topic>`
- Body sections: **Context** (1–3 lines + file paths) · **Question** (one
  question per mail — the fleet inherits one-question-at-a-time) · **Meanwhile**
  (`continuing with <x>` or `BLOCKED`) · **Needed by** (if time-bound).

**Answer (Wednesday → agent):**
- Subject: `[Wednesday -> <Client>/<Project>] ANSWER: <topic>` (mirror the topic
  string — it is the correlation key).
- Body: the answer + the validation evidence (what was checked, where), or the
  escalation receipt ("with Kam, expect answer by ~X — continue with Y").

**Escalation classes (pause-for-Kam list, from his standing brief):**
1. Approval-class: prod/demo-affecting actions, money, external comms to humans,
   anything irreversible.
2. Genuine ambiguity in *Kam's intent* that the brief + Wednesday can't resolve.
3. Decisions he has reserved (per-project decision queues, legal, pricing).
Everything else Wednesday answers — that is the job.

**Completion oracle:** the existing Step-2d wrap email. No new signal needed —
"Stop event after response events" from the blueprint maps to wrap-after-work.

## Structural anti-leak measures (not vibes)

1. **Identity isolation preserved:** execution stays in project-launcher
   sessions (approach-b rejection above) — per-project `gh`/`az` state intact.
2. **Single-client working set:** when composing an ANSWER, Wednesday's sources
   are the target project's own tree + that client's entry card + the brief.
   Other clients' material is out of bounds for that compose — checklist line in
   the skill, checked per answer.
3. **Subject-line client tag is the routing key** — every mail names exactly one
   client/project; the digest tool groups by it; a mail whose body references a
   *different* client than its subject is flagged, never actioned.
4. **Read-only enforcement by construction** where possible: scouts get
   read-only toolsets (blueprint #4); tracker writes are impossible (read-only
   grant); vault writes are impossible (read-only mount rule).

## Built in this session (v1 deliverables)

1. This design note.
2. `2_Project_Files/fleet/inbox_digest.sh` — summaries-firewall poller: digest
   mode (subjects + client tags + short previews, newest first, state-aware so
   only NEW mail surfaces), `full <message_id>` mode for raw body on demand.
3. `0_Brain/skills/delegation-monitoring.md` — the operational ritual
   (launch → monitor → triage → answer/escalate → oracle → score).
4. Brief-template tightening in `0_Brain/skills/delegation-protocol.md`:
   a **Pre-answered questions** section (kills predictable questions before they
   fly) + the standing question-routing paragraph every brief now carries.
5. Draft fleet-side edit (below) for Kam's named go-ahead.

## Fleet-side edit — DRAFT, needs Kam's named go-ahead (not applied)

Addition to the workspace CLAUDE.md "Fleet comms via email" section (DevMASTER,
outside Wednesday's write scope until Kam says the word):

> **Mid-session questions (added 2026-08-04):** when a session working a
> Wednesday-briefed task hits a question the brief doesn't answer, do NOT ask
> Kam by default. Email `wednesday-agent@agentmail.to`, subject
> `[<Client>/<Project> -> Wednesday] QUESTION: <topic>`, body: Context / one
> Question / Meanwhile (what you'll keep doing, or BLOCKED) / Needed-by.
> If blocked, re-check your inbox every ~3 minutes for
> `[Wednesday -> <Client>/<Project>] ANSWER: <topic>`; after ~15 minutes with
> no answer, proceed on the safest interpretation and say so in your wrap —
> or pause ONLY if the item is approval-class (prod/demo-affecting, money,
> external comms, irreversible). Approval-class items always pause for Kam.

## Verification (R1 — this session's verifier)

Round-trip self-test: QUESTION mail sent from coagent@ → digest tool surfaces
and classifies it → ANSWER sent → lands in coagent@ with mirrored topic.
Plus: digest state-tracking shows each mail once; no key material in any file.
Results recorded in the daily note + WED-42 receipt.

## v2 candidates (parked)

Push-not-poll (Agent Mail webhooks → local listener) · dashboard rendering of
the Q&A stream (WED-46) · per-question latency + escalation-rate metrics on the
scoreboard (pairs WED-30) · Haiku pre-triage of question mail (full blueprint
#1, second tier).
