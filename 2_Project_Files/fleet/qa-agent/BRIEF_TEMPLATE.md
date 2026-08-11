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

`/Volumes/KK_T9_External_HDD/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`

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

## 6. Output boundary (fixed — not a choice)
- **Findings, reports and recommendations ONLY.** The QA agent makes NO changes
  of any kind — no code, no tests, no fixtures, no tickets, no config. It
  describes the fix-shape and the regression test the owner should add, in
  prose in its report; the project's own agent authors and commits everything.
  (Kam ruling 2026-08-11, absolute — supersedes the earlier opt-in.)

## 7. Known-fragile / known-changed areas
- **Known-fragile:** `<areas historically brittle — hunt the class here first>`
- **Recent changes — do NOT flag as new:** `<list, so a known change is not reported as a regression>`
- **Known open gaps / missing tools:** `<so they are carried as gaps, not re-discovered>`

## 8. Logistics
- **Session time-box:** `<bounded work unit>`
- **Findings sink + conventions:** `<tracker, naming/label conventions>`
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
