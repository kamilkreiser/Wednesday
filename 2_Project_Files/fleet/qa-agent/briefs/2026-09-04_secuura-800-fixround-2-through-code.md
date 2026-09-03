# QA Agent Invocation Brief — Secuura/Blockchain, #800's SECOND FIX ROUND, STATIC THROUGH-CODE

## Charter (read first, in full)
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`

**Then read your own prior pass on this PR, in full — it defines every FR id below:**
`/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura-blockchain/reports/2026-09-04-800-fixround-through-code/SUMMARY.md`
(4 Major: FR-1 sourcing-safety justification false on the second caller · FR-2 nineteen cases assert
printed text and never the exit code · FR-3 nothing runs the shell suites on any live path · FR-4 the
148-line runner has no test of its own. 5 Minor: FR-5 new line numbers in the commit banning them ·
FR-6 the mid-sentence splice · FR-7 `.env` can assign the script's own control variables · FR-8 "the
shell refused to parse it" fires on files that parse · FR-9 the remedy is per-RUN not per-FINDING.)

## 1. Target
- **Client / Project:** `Secuura / Blockchain (Platform K)`
- **Running target:** **NONE — STATIC pass, read by SHA.** Do not start, stop or rebuild the stack;
  do not run compose; **do not execute `check-slot-credentials.sh` or `run-shell-suites.sh` against
  any real `.env` or the real repo.** Exercise scripts on **fixtures in YOUR OWN scratchpad only.**
- **Environment:** none contacted. **Zero writes to the Secuura tree.** Expect `git status` to show
  two untracked `(conflict_on_2026-07-03)` snapshots on arrival — they pre-date this session by two
  months; report the tree as **UNCHANGED BY YOU**, never as clean.
- **Production?:** nothing is deployed and no finding of yours triggers a deploy.

## 2. Subject and the claims to falsify

**PR #800, head `7e6621bb1`** against develop `492152a81` (both read from the GitHub API and
`git log` at 06:07 on 2026-09-04). The pass above judged `e26cfce2b`; **three commits landed after
it and they are this pass's subject:**

- `0332df892` — **FR-2**: assert the exit code. Suite 19 → 23 → 27 cases.
- `7673682a9` — **FR-1 / FR-6 / FR-8**: the comment-block rewrite.
- `7e6621bb1` — **FR-4**: a test of its own for the 148-line runner (16 cases, real `git init` fixture).
- **FR-3 was answered in a SEPARATE PR: #806, head `5718213c4`**, based on #800's branch
  (`feature/ks-762-app_db_password-is-a-committed-literal-default-in-docker`), deliberately with no
  reviewer requested. **It is in scope for this pass** — FR-3 was a Major and its remedy lives there.
- **FR-5 / FR-7 / FR-9 are CONFIRMED DEFERRED** by ruling, named on the PR rather than fixed.
  **Do not re-report them as open findings; DO report if a deferral is now wrong.**

**All claims below are the builder's. Falsify them.**

1. **FR-2 — the exit code is now asserted.** Its `--quiet` case asserts `SILENT/0` at **measured zero
   bytes of output**, and it added the complement `LOUD/1` *"because without it a script printing
   nothing at all would satisfy the silent case."* **Verify that complement exists and would fail if
   the script were gutted.** Re-run attack 6 from your own prior pass (flip every `exit 1` → `exit 0`)
   and state the failing set BEFORE you run it.
2. **FR-1 / FR-6 / FR-8 — the false sentence was DELETED, not softened.** The builder reports it
   settled ask 2 **positively** rather than by an absent grep: `DEPLOYMENT-ARCHITECTURE.md` confirms
   the demo VM builds and `up -d`s over rsynced source, so `start-environment.sh` is developer-facing,
   and *"FR-1's justification could be made TRUE rather than hedged, with the invariant named so a
   third caller cannot be wired in blind."* **Test the invariant, not the prose:** is there anything
   that would actually catch a third caller wired in without sourcing?
3. **FR-4 — the runner now has 16 cases on a real `git init` fixture, runner self-hosting.** The
   builder disclosed its own regression inside this fix: *a flat fixture put `REPO_ROOT` outside
   `$tmp`*, fixed by nesting **plus a real suite under the globbed root so leg 13 reaches a GENUINE
   verdict there rather than being stubbed.* **Your prior FR-4 was exactly "the one fixture it appears
   in is arranged so it cannot bite" — check the new one bites.**
4. **FR-3 / #806 — the preflight leg.** Preflight 9/9, PUSH_RC=0. The builder reports the leg
   **validated itself on its first run by catching two real defects**: (i) the suites were **never
   hermetic** — `.githooks/pre-push:45` sources `slot-target.sh` (39 exported variables) before
   preflight, and two suites unit-test how those values are derived while the subject reads them as
   `${AKTO_PREFIX:-akto-s$SLOT}`, so an ambient value wins and the assertion compares the shell's
   answer with itself (reproduced four times: **25/0 and 66/0 clean; 24/1 and 61/5 after sourcing**
   → **KS-786**); (ii) its own fixture regression above. It also **REFUSED** an offered
   skip-on-absent-runner leg, calling it the check-that-cannot-fail class. **Verify the refusal held
   in the shipped code** — there must be no path where an absent runner yields a green leg.
5. **Wall-clock:** the full nine-suite set is claimed as a **range, 31–44 s over six runs, 34 s
   typical**, with the leg printing its own wall-clock every run. Suite set 9 → 10.

- **Source tree (read-only):** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files`

## 3. Scope — and the standing hypothesis

**Charter:** judge whether the four Majors are genuinely closed, and **hunt the class rather than the
instances.** The standing hypothesis has paid every time it was used on this project: **assume one
more instance exists**, and **look for it in the fix round itself** — the last two rounds both
introduced a new instance of the very class they closed (F-7 was introduced by the commit written to
close F-800-01; FR-4 was introduced by the commit written to close F-800-07).

**THE LOAD-BEARING QUESTION FOR THIS PASS — this is why it exists.** Every Major you found last time
was a **control or an assertion that could not bite**, not a bug in the subject. The builder itself
found, in this very session, **five instruments that lied and two of them were controls it wrote** —
including one that asserted zero occurrences on a path that never prints one, because
`SECUURA_ENV_FILE=<(printf ...)` is a process substitution and `[ -f "$ENV_FILE" ]` routed it to the
"no `.env` at all" branch. It was caught **only because a prediction was written down before the
tamper ran.** So:

> **Judge the CONTROLS of this fix round at least as hard as the fixes.** For every new assertion,
> ask what tamper it exists to catch, predict the failing SET before running it, and compare. A
> control that has never been made to fail is a claim. A control that isolates nothing measures
> nothing. Two of this fleet's independent testers converged on that in one night — it is the method
> now, not a suggestion.

- **Out of scope:** the running stack, any container, the demo/UAT VM, **any PR state change or
  comment**, and any file in the Secuura tree.
- **THE HOLD YOU MUST NOT BREAK:** **#799 is FROZEN at `b36757f7a`** with Peter requested at that
  exact head; a push voids his review. **Nothing you do touches #799**, and you make no push
  anywhere. You are findings-only regardless.

## 4. Credentials (POINTER ONLY — never values)
- **Path:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/` — **you should not need
  any.** This is a static read. If you believe you need a credential, that is a QUESTION to Wednesday,
  not a step.
- **Personas:** none — no running system is contacted.

## 5. State-mutation & cleanup
- **Sanctioned pattern:** **exclude-and-report-only.** Nothing outside your own scratchpad changes.
- **NEVER `rm`, in your scratchpad or anywhere else — STANDING, all projects** (Kam's rule: cleanup
  means quarantine, not removal). Three passes have blocked on Claude Code's own *"Dangerous rm
  operation on possibly-empty variable path"* guard while tidying a scratch fixture, and each time
  the answer was no. **Build each attempt in its own `mktemp -d` and abandon the old one.** If a path
  genuinely must be cleared, **move it into a dated `_quarantine_YYYY-MM-DD/` beside it and say so.**
  Guard every expansion — `"${DIR:?unset}/${SUB:?unset}/…"`. **If cleanup is costing real budget,
  stop building the fixture and report the affected checks as NOT RUN with the blocker named.**

## 6. Output boundary (fixed — not a choice)
- **Findings, reports and recommendations ONLY.** No code, no tests, no fixtures, no tickets, no
  config, no PR comments. Describe the fix-shape and the regression test the owner should add, in
  prose. The Secuura agent authors and commits everything. (Kam ruling 2026-08-11, absolute.)

## 7. Known-fragile / known-changed areas
- **Known-fragile:** shell-suite hermeticity (KS-786, filed last night) · anything asserting on
  printed TEXT rather than exit status · fixtures that stub the thing under test · line-number
  citations · `get_value`'s sourcing blast radius.
- **Recent changes — do NOT flag as new:** the three commits and #806 named in §2; KS-785 and KS-786
  filed on 2026-09-03; the suite-set count moving 9 → 10.
- **Known open gaps carried, not re-discovered:** FR-5 / FR-7 / FR-9 deferred by ruling; #806 has no
  reviewer by design and cannot merge before #800.

## 8. Logistics
- **Time-box:** one bounded session; wrap at your own context boundary with a SUMMARY.
- **Findings sink:** your own report tree, `projects/secuura-blockchain/reports/2026-09-04-800-fixround-2-through-code/`.
  **File no tickets.** Priority on any finding is the humans' call, never yours.
- **Escalation:** back through Wednesday (`wednesday-agent@agentmail.to`, subject
  `[Testing Agent MAIN -> Wednesday] QUESTION: <topic>`). Approval-class items (prod/demo-affecting,
  money, external comms, anything irreversible) ALWAYS pause for Kam.

---

PROVENANCE:
- #800 head `7e6621bb1`, base develop, Peter requested, 0 reviews | GitHub API `/repos/Secuura/Distributed_Secuura/pulls/800` | read 2026-09-04 06:07
- #799 frozen at `b36757f7a`, Peter requested, one COMMENTED review | same API, pulls/799 | read 2026-09-04 06:07
- #806 head `5718213c4`, base = #800's branch, no reviewer requested | same API, pulls/806 | read 2026-09-04 06:07
- develop at `492152a81`; the three post-pass commits and their subjects | `git log --oneline 492152a81..7e6621bb1` in the Secuura checkout | read 2026-09-04 06:07
- FR-1..FR-9 definitions and the attack table | your own SUMMARY.md at the report path named above | read 2026-09-04 06:08
- The builder's claims in §2 (hermeticity numbers, the deleted sentence, the refused skip-leg, the 31–44 s range) | the Secuura agent's own STATUS and wrap mails to wednesday-agent@, 2026-09-03 18:23:57Z and 18:38:38Z | read 2026-09-04 06:05 — **these are its claims, not Wednesday's measurements**
