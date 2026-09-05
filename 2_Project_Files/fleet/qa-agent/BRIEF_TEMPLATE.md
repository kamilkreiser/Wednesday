# QA Agent Invocation Brief — TEMPLATE

Wednesday fills this in to invoke the cross-project QA/testing agent for ONE
specific project's task. It carries only the calling client's context; the
methodology lives in the charter, referenced by path (never pasted — paths stay
current, copies go stale).

**R0 (client isolation):** this brief carries exactly one client's content.
Never name or reference any other client. Send it only into the target
project's own session.

**Send via** `fleet/send_brief.sh --to '<Client>/<Project>' --subject '[Wednesday -> <Client>/<Project>] QA session: <topic>' --body-file <this-filled-file>`.
The PROVENANCE block below satisfies the send-brief gate — every load-bearing
fact names where it was read and when.

---

## Charter (read first, in full)

`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`

Read it end-to-end before running anything. It defines mission, the two
hard-coded rules (state the FAIL condition before each test; untested areas are
first-class output), the method catalog, the user-perspective pass, the
anti-LLM-failure rules, the hard boundaries, and the reporting standard. This
brief supplies only WHAT and WHERE.

---

## 1. Target
- **Client / Project:** `<Client> / <Project>`
- **Running target + how to reach it:** `<base URL / how to launch>`
- **Environment identity (confirmed with a human):** `<which env; mode / NODE_ENV>`
- **Production? :** MUST be non-prod. `<confirm non-prod, name the env>`

## 2. Spec / DoD being tested against
- **Spec source:** `<path to OpenAPI / acceptance criteria / DoD>`
- **The claims to challenge:** `<key claims from the spec/PR, as inputs to falsify — NOT as evidence>`
- **Source tree (read-only, for root-causing):** `<path or "not provided">`

## 3. Scope
- **Charter (one or two sentences):** `<explore X with Y looking for Z>`
- **In scope:** `<areas / endpoints / journeys>`
- **Out of scope / do NOT touch:** `<areas, destructive ops, prod-adjacent resources>`

## 4. Credentials (POINTER ONLY — never values)
- **Path to test credentials:** `<path in 4_Credentials or project store>`
- **Roles/personas to exercise:** `<attacker-role, normal-role, others>`
- **Disposable account for state-mutating fuzz:** `<path / how to provision, or "none — exclude-and-report-only">`

## 5. State-mutation & cleanup
- **Sanctioned pattern for this project:** `<disposable identity you may provision | scoped teardown | exclude-and-report-only>`
- **Reachable-on-demand product states:** `<list; anything not here is a documented coverage gap, not a silent omission>`
- **NEVER `rm`, in your scratchpad or anywhere else — STANDING, all projects (Kam's rule: cleanup
  means quarantine, not removal).** Three passes have now blocked on Claude Code's own
  *"Dangerous rm operation on possibly-empty variable path"* guard while tidying a scratch fixture,
  and each time the answer was no. **Build each attempt in its own `mktemp -d` and abandon the old
  one** — a scratchpad is disposable, so nothing needs deleting. If a path genuinely must be cleared,
  **move it into a dated `_quarantine_YYYY-MM-DD/` beside it and say so in the report.** And guard
  every expansion — `"${DIR:?unset}/${SUB:?unset}/…"` — so an empty variable ABORTS the command
  rather than widening it. **If a cleanup is costing you real budget, that is the signal to stop
  building the fixture**: report the affected checks as **NOT RUN with the blocker named**, which is
  worth more than a result measured against a workspace you had to invent.

## 6. Output boundary (fixed — not a choice)
- **Findings, reports and recommendations ONLY.** The QA agent makes NO changes
  of any kind — no code, no tests, no fixtures, no tickets, no config. It
  describes the fix-shape and the regression test the owner should add, in
  prose in its report; the project's own agent authors and commits everything.
  (Kam ruling 2026-08-11, absolute — supersedes the earlier opt-in.)

## 6a. EVIDENCE CLASS ON EVERY FINDING THAT RECOMMENDS AN ACTION (mandatory)

**Added 2026-09-04 after a QA recommendation of this fleet's own was overturned by a live
probe, on a client platform, one commit before it shipped.**

**The case, so this rule is not abstract.** A QA pass read an unpublished API operation
STATICALLY and reported it *"the one most worth publishing."* The builder authored it,
regenerated the spec, and the repo's own contract check went GREEN with every example
resolving. It then probed the live endpoint before finalising: **the gateway 415s every
content-type the operation accepts — octet-stream, pdf, text/plain, multipart, none —
and only an empty body reaches the handler at all.** Publishing it would have replaced
*"absent from the spec"* with *"the spec says POST octet-stream and the gateway refuses
it"* — **a divergence CREATED by the ticket that exists to close divergences.** The QA
report was right that the operation was the most valuable one, and **it could not have
known it 415s, because a static read cannot.** Nothing in the report said which it was.

**THE RULE: any finding that recommends an ACTION — publish this, wire this, delete this,
prioritise this — carries its EVIDENCE CLASS inline, in these words:**

- **`MEASURED AT RUNTIME`** — the behaviour was driven and observed. Name the probe.
- **`PROBED`** — an adjacent call was made; say which, and what it does NOT cover.
- **`READ ONLY`** — established from source, spec, config or docs, **not executed.**

**A recommendation with no evidence class is incomplete and the receiving agent should ask
for one rather than act on it.** *"Most worth publishing"* is an action recommendation; it
rested on a read; the report presented it with the same confidence as its measurements.

**Why this is a template rule and not advice:** the reader of a QA report is usually an
agent under time pressure with the report's own confidence as its only calibration.
**A finding that is right about VALUE and silent about FEASIBILITY reads as both.**

**The corollary for green gates, from the same session:** a repo's own contract check
passing is not evidence that a consumer can call the thing. **Green `check:openapi` was
not enough; the live probe was the thing.** Where a recommendation depends on a runtime
behaviour, say so even when — especially when — a static gate agrees with you.

- **Every suite named in §3 carries WHERE it runs** — the tester's own by-SHA copy, or a stack the tester MAY drive at a named port. A suite with no runnable environment named is **NOT COMMISSIONED — say so, with the reason** (2026-09-05: two Secuura briefs assigned "the four platform suites" while §1 forbade the only stack that could run them; the tester had to resolve the contradiction). Name suites by PATH and command, never by a phrase.

## 7. Known-fragile / known-changed areas
- **Known-fragile:** `<areas historically brittle — hunt the class here first>`
- **Recent changes — do NOT flag as new:** `<list, so a known change is not reported as a regression>`
- **Known open gaps / missing tools:** `<so they are carried as gaps, not re-discovered>`

## 8. Logistics
- **Session time-box:** `<bounded work unit>`
- **Findings sink + conventions:** `<tracker, naming/label conventions>`
- **The head observed at the end is a MOVING reading while a builder is live in the tree** (2026-09-05: a tester read `05b36a826` → `a6bd20521` → `05b36a826` in one pass as the builder switched branches). Report it as THREE TIMESTAMPED readings (start / mid / end) WITH the branch name beside each SHA — never one bare SHA.
- **Escalation path:** back through Wednesday (`wednesday-agent@agentmail.to`,
  QUESTION subject) for anything the brief does not answer; approval-class items
  (prod/demo-affecting, money, external comms, anything irreversible) ALWAYS
  pause for Kam. Priority on any finding is the humans' call, never yours.

---

PROVENANCE:
- <fact used to scope this session> | <source path / URL / ticket / command> | read YYYY-MM-DD
- <target env + mode> | <where confirmed with a human> | read YYYY-MM-DD
- <spec / DoD location> | <path> | read YYYY-MM-DD
- <known-fragile / recent-changes list> | <source> | read YYYY-MM-DD
