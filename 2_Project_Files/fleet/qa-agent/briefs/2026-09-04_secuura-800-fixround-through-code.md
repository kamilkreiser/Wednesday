# QA Agent Invocation Brief — Secuura/Blockchain, #800's FIX ROUND, STATIC THROUGH-CODE

## Charter (read first, in full)
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`

## 1. Target
- **Client / Project:** `Secuura / Blockchain (Platform K)`
- **Running target:** **NONE — STATIC pass, read by SHA.** Do not start, stop or rebuild the stack;
  do not run compose; **do not execute `check-slot-credentials.sh` against any real `.env`.**
  If you exercise the script, do it on **fixtures in YOUR OWN scratchpad only.**
- **Environment:** none contacted. **Zero writes to the Secuura tree.** Expect `git status` to show
  two untracked `(conflict_on_2026-07-03)` snapshots on arrival — **they pre-date this session by
  two months; report the tree as UNCHANGED BY YOU rather than as clean.**
- **Production?:** nothing is deployed and no finding of yours triggers a deploy.

## 2. Subject and the claims to falsify
**PR #800, fix round at `e26cfce2b`** (earlier head `8cb16f79b`), against develop `492152a81`.
**This PR fixes a credential checker that had shipped a false clean.** A previous pass found three
Majors in it; this pass judges the fixes. **All claims below are the builder's — falsify them.**

- **F-5/F-6 fixed together by SOURCING rather than parsing** — `get_value` now sources the file in a
  subshell with `set -a`, *"so it cannot drift from the consumer because it is the consumer."* The
  builder's justification for it being safe here specifically: **`start-local.sh` runs `source .env`
  moments later on the same path, so the checker executes nothing the start path was not about to
  execute anyway.** **Test that justification, not just the code** — is the checker's sourcing
  genuinely equivalent in effect and blast radius to the start path's?
- **The remedy is now PER-FINDING, three states not two:** only a **positively-identified SHARED**
  value prints `docker compose down --volumes`; **BLANK** gets `bootstrap-env.sh` plus an explicit
  statement that whether a teardown is *also* needed depends on something **the script has not
  measured**; **UNREADABLE is new** — previously it resolved to "blank", *"asserting a finding the
  check had never reached."*
- **19 fixtures, up from 8 — and THE REMEDY IS ASSERTED, not just the detection**, with a control
  that **SHARED must STILL print `--volumes`.** The builder's reason: *"without that control,
  deleting the command from the script entirely would pass all three negatives."* **Verify that
  control exists and would actually fail if the command were removed.**
- **F-7: one runner, not a glob in three places**, with **preflight leg 12 asking the runner rather
  than re-globbing**; `verify-slot-credential-isolation.sh` reachable as
  `npm run verify:slot-isolation` and **deliberately NOT in a gate** because it stands up real
  compose projects and its teardown destroys volumes.
- **F-8: citations now name the SYMBOL, not the line** (`source .env` in `start-local.sh`) in both
  the commit message and `check-slot-credentials.sh` — the line number was wrong in every commit it
  ever appeared in.
- **Source tree (read-only):** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files`

## 3. Scope — and the standing hypothesis
**Charter:** judge whether the three Majors are genuinely closed, and hunt the class rather than the
instances. **The standing hypothesis, which has paid every time it was used on this project: assume
one more instance exists.** The three classes already found here:
1. **A check that returns a confident GREEN over a wrong state** (the original F-5/F-6).
2. **A guard shipped but invoked by NOTHING** (F-7 — third occurrence of that shape in this repo,
   and its first wired run immediately surfaced a suite red on develop that three tickets had broken
   without anyone seeing).
3. **A claim in shipped source that points somewhere it does not resolve** (F-8).

**Ask specifically: does the fix round itself contain any of the three?** The last one did — F-7 was
introduced by the commit written to close F-800-01.
- **Out of scope:** the running stack, any container, the demo/UAT VM, any PR state change or comment,
  and any file in the Secuura tree.

## 4. Credentials
**None, and none needed.** **Never read a real `.env`.** Everything about credential handling is
judged from the code and from fixtures you author in your own scratchpad.

## 5. State-mutation & cleanup
**Exclude-and-report-only.** Scratch in YOUR scratchpad; nothing copied back.

## 6. Output boundary (fixed)
**Findings, reports and recommendations ONLY.** No code, tests, fixtures, tickets, config or PR
comments. Fix-shapes and regression tests in prose.

## 7. Known-fragile / known-changed — do NOT re-report as new
- **The two `(conflict_on_2026-07-03)` snapshots** — two months old, not this session's.
- **`preflight_deps.test.sh` was red on develop** (22/11) because legs 10/11 and leg 5 landed without
  being added to its fixture — **found and fixed in this very PR**, by the wiring that F-7 added.
  Do not re-file; **do check the fix.**
- **2 of 27 auth test files fail at import** (`Missing "./utils/logger" specifier`) — proven
  pre-existing, filed in BACKLOG.md deliberately so an unrelated shared-package fix would not widen
  an auth-bypass PR's review.
- KS-784 records an orphan Schemathesis failure on `POST /api/teams/webhook-config`, unrelated.

## 8. Logistics
- **Time-box:** one bounded pass. Depth over breadth — the remedy's three states first if you cut.
- **Report to:** `projects/secuura-blockchain/reports/2026-09-04-800-fixround-through-code/SUMMARY.md`
  under your own tree, then mail Wednesday a summary. **Wednesday reads the FULL report, not the
  mail.**
- **Escalation:** `wednesday-agent@agentmail.to`, QUESTION subject. Approval-class pauses for Kam.
- **Your NOT-TESTED list is first-class output. State the counting UNIT and SETTLE POINT for any
  population figure.**
- **CONTEXT FOR YOUR SEVERITY CALLS, not a reason to soften them: #800 is first in a merge queue and
  the `APP_DB_PASSWORD` rotation is 2026-09-05 09:00.** Until #800 merges, the rotation remedy this
  checker prints is a **silent no-op**, and the team has been told not to follow it. **Report what you
  find at the severity you find it** — the clock is Wednesday's problem, not yours.

PROVENANCE:
- #800's fix round, the three-state remedy, the 19 fixtures, the F-7 runner and F-8's symbol citations | s120's STATUS mail 2026-09-03T15:44:06Z in wednesday-agent@agentmail.to | read 2026-09-04
- The three original Majors (F-5, F-6, F-7) and F-8 | /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura-blockchain/reports/2026-09-03-s119-batch-through-code/SUMMARY.md | read 2026-09-04
- Head e26cfce2b, develop 492152a81, and #800's zero-review state | s121's Session wrap 2026-09-03T16:57:55Z | read 2026-09-04
- The preflight_deps pre-existing red and the 2-of-27 import failures | s120's STATUS mail, same read | read 2026-09-04
- The APP_DB_PASSWORD rotation date and the standing extranet notice | /Volumes/DevMASTER/WEDNESDAY/0_Brain/daily/2026-09-04.md | read 2026-09-04

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-04 02:59
