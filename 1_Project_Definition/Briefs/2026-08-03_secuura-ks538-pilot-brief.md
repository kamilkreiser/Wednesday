# Delegation brief — KS-538 extranet comments box + cross-model validation pilot

From: Wednesday (coordination) · To: the Secuura/Blockchain Claude session
Date: 2026-08-03 · Status: APPROVED by Kam 2026-08-03 (verbally to Wednesday,
after review of both briefs; the earlier DRAFT marker was Wednesday's stale
status line — good catch by the Platform K session)
Protocol: this brief follows Wednesday's delegation standard (verifier, round
cap, wider/deeper). Wednesday never edits Secuura files; this session executes.

---

## Part 1 — The feature: KS-538

**Task:** Implement the extranet comment/request button (KS-538, P3): a button
on extranet pages letting users (e.g. Phil) ask questions, request documents,
or query versioning — turning the extranet from a one-way feed into two-way
communication. Related: KS-339 (Phil + Steve access; extranet as company source
of truth).

**Context (paths, not pasted content):**
- Ticket: KS-538 in Linear (full text + source: 2026-07-31 Kam/Stuart catch-up).
- Repo: `Secuura/secuura-extranet` — the coupled sibling project (declared in
  `!CODING/Secuura/CLAUDE.md`); shared working scope with Blockchain.
- Your own CLAUDE.md conventions govern: extranet skill ("keep the board
  short"), to-do/document notification patterns.

**Constraints:**
- ⚠ **The extranet auto-deploys on push to `main`. Work on a branch + PR; no
  merge to main until the review gate below passes AND Kam approves.** (Kam's
  standing go-slow directive, 2026-08-03.)
- Scope: comments/requests must respect existing extranet auth (Phil/Steve are
  external partners — no new anonymous surface).
- Design choice (thread model, storage, notification wiring) is yours — note
  the decision + rationale on KS-538 as you go.

**Definition of done (the verifier):**
1. Feature works per ticket intent: a signed-in extranet user can submit a
   comment/request from a page; it is stored, visible to the team, and
   notified per your existing patterns (to-do and/or document conventions).
2. Tests: unit tests for the new API surface + at least one end-to-end path
   (submit → visible). All green, run output shown.
3. KS-538 updated with commit/PR links + a one-line extranet document post per
   your conventions.
4. **Round cap: 3.** If the verifier isn't green after 3 refinement rounds,
   stop and report back rather than looping.

## Part 2 — The pilot: cross-model validation (first live outing)

This task doubles as the pilot for Kam-approved cross-model validation
(Wednesday's WED-20). Two mechanisms, both advisory — findings are triaged by
you; tests and Kam decide, never the second model.

**Setup (once):**
- Install the OpenAI Codex CLI project-local (suggest `2_Project_Files/ci/tools/
  codex-cli`: `npm install @openai/codex` in that folder), with
  `CODEX_HOME=<project>/4_Credentials/.codex` (verify gitignored). Kam performs
  `codex login` once (ChatGPT-subscription auth — no API key).
  - Fallback if Kam prefers zero setup: Wednesday's install at
    `/Volumes/KK_T9_External_HDD/WEDNESDAY/2_Project_Files/tools/codex-cli`
    (+ CODEX_HOME `…/WEDNESDAY/4_Credentials/.codex`) — works only while the
    T9 drive is mounted; degrade gracefully (skip with a note) if absent.

**(a) Second-model diff review — before the PR merges:**
- Pipe `git diff main...<branch>` + a one-paragraph intent summary to
  `codex exec` with an adversarial-reviewer prompt: return findings as a list
  (severity, file:line, claim, why it's wrong). Cap the diff at what fits
  sensibly; exclude lockfiles.
- Triage each finding on the PR: **confirmed → fix; rejected → one-line reason.**
  Log all of it (see metrics).

**(b) Spec-only adversarial tests:**
- BEFORE showing Codex any implementation, prompt it with ONLY the KS-538
  ticket text + your API surface signatures: "write tests for this spec."
- Run its tests against your implementation. Failures are triaged: real gap →
  fix; test wrong → note why. This breaks the tests-that-pass-their-own-bugs
  correlation.

**Privacy note (Kam has approved for this pilot):** diffs and specs go to
OpenAI under Kam's personal ChatGPT account. Never include anything from
`4_Credentials/`/`3_Access_Keys/` in a prompt (they're gitignored — diffs are
inherently safe; keep it that way).

**Pilot metrics — log to a markdown file in the repo (your choice of spot,
suggest `ci/crossmodel/pilot-log.md`):** per review: findings raised /
confirmed real / false positives / anything the second model caught that your
tests missed / wall-clock cost. Same for the spec-tests: how many of its tests
failed your implementation, and how many of those were real. This data decides
whether the mechanism earns standing status — honest logging matters more than
a flattering score.

## Reporting back

On completion (or at the round cap): comment on KS-538 as usual, and summarize
the pilot metrics in your wrap-up so they land in Wednesday's index card via
the end-of-session feed. Wednesday reads results read-only and scores the
delegation on her board.
