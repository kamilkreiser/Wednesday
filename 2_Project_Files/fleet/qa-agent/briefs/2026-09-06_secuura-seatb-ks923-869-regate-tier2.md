# QA Agent Invocation Brief — Secuura / Blockchain, SEAT B: PR #869 (KS-923) NARROW RE-GATE

**Charter first, in full:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`.
Findings only. You never fix, never file a ticket, never touch a builder's tree.

**TARGET — PR #869, KS-923, FIX ROUND. TIER 2, NARROW.** head
`8b7d57cc6b3fc150ae13678cc42ddca970ca26bb`; the previously gated head was `313f96519…` and is its
ancestor. Base develop `a8aa723a0fdc70db26177bd91a9c81dbec6640d2` (it moved during the round).

**A previous pass gave this PR a PASS WITH FINDINGS.** This round answers three of them. **Scope
yourself to those three plus regression** — do not re-derive the whole original pass; it is on the
record and it held.

## 2. What this round was ruled to do
- **F1 (Major):** the guard tested EXISTENCE, not READABILITY — `[ ! -f ]` is true for a mode-000
  file, so the FIXED orchestrator gave byte-for-byte the PRE-FIX verdict one state over.
- **F2 (Major, a test-instrument defect):** `${ORCH_SH:-…}` treats set-but-empty as unset, so an
  empty value silently graded the SHIPPED file and printed a transcript byte-identical (same sha256)
  to a genuine proof run.
- **F4 (judgement):** CELL 8 pinned the invocation by grepping source. The previous tester falsified
  the builder's premise — a behavioural discriminator DOES exist (an executable stub whose shebang
  names a nonexistent interpreter). CELL 8 was replaced.

## 3. Scope — claims to measure
1. **F1 fixed ONCE in `require_script`**, which `require_job` delegates to, so Stage 1, Stage 2 and
   the post-API loop are all covered by one change, with a distinct message (`is NOT READABLE at`).
   Builder drove CELL 10 (Stage-2 tool mode-000) and CELL 11 (Stage-1 job mode-000). **Re-derive
   both.**
2. **THE THING THE BUILDER ASKED YOU TO PRESS, in its own words: the post-API path is INFERRED, not
   driven.** It judged a third fixture to be restating the same delegation. **Decide whether that
   inference holds** — if the post-API loop reaches `require_script` by a different route, or does
   not reach it at all, that is a finding about the code, not about the judgement.
3. **CELLS 10 and 11 cannot discriminate under root** — both explicitly report `bad`, not `ok`, when
   the mode-000 fixture is still readable. **If you are running as root, expect two reds with that
   message and read them as "this cell could not run", NOT as a defect.** Say which case you were in.
4. **F2's fix:** the colon dropped (`${ORCH_SH-…}`), set-but-empty refused explicitly, `SUBJECT
   <path>` + sha256 printed as the first line of every run, and CELL 12 re-invoking the suite with
   `ORCH_SH=""` requiring non-zero behind a `KS923_SELFTEST_CHILD` fork guard. **Drive the empty,
   unset, valid and bogus cases**, and satisfy yourself the fork guard cannot recurse.
5. **F4's replacement:** CELL 8 is now a `badshebang` fixture asserting the tool RAN. Builder reports
   it reds only against the pre-KS-923 file (which invokes by bare path, so the bad-shebang stub
   never runs). **No source pin was kept** — the builder declined it with a reason and I ratified
   that. Verify the behavioural cell does what the grep could not.
6. **The three red-proof runs, each naming its subject:** 12/0 fixed · 10/2 against the CURRENT head
   (CELLS 10, 11) · 7/5 against pre-KS-923 (CELLS 6, 7, 8, 10, 11). CELL 9 green in all three; CELLS
   1–5 green in all three. **Re-derive, and check the SUBJECT line names the file you think it
   graded** — that is the whole point of F2's fix.
7. **Regression only, beyond the above:** nothing that passed in the first gate should have moved.
   Suite 9 → 12 cells.
8. **HUNT — the builder's own retraction, verify its conclusion stands.** Its first F2 reproduction
   ran the OLD suite from a scratchpad, whose `REPO_ROOT` resolves from its own location, so the
   FATAL fired because the orchestrator was absent — not because of the `:-` fallback. It says so
   plainly and did NOT claim to have reproduced the original finding. **You are the independent
   check on that: does the shipped fix actually close the mechanism the first tester measured?**
9. **Merge-tree against the `develop` you read AT THE TIME, in YOUR OWN copy.** It has moved twice
   tonight. I ran none.
10. **Secret gate:** fabricated RANDOM tokens (never a documented example pair — gitleaks allowlists
    those), prove the canary FIRES in the same scan mode, quarantine by rename, scan the real range.

## 4. Credentials
Pointer only: the project's own `4_Credentials/.env`. **If `gh` under that project's `GH_CONFIG_DIR`
is not authenticated, do NOT fall back to the global config** — report PR-body items as UNVERIFIED.
A previous pass hit exactly this and refused correctly.

## 5. State-mutation & cleanup
Your own `mktemp` checkout. **Never touch seat A's tree (`2_Project_Files`) or seat B's worktree
(`worktrees/seat-b`)** — both live. No demo VM, no shared stack, no Docker, no prune, and never run
the real security jobs. Tampers as SEPARATE files graded via the suite's own hook, as the previous
pass did — that is strictly safer than an in-tree edit. Quarantine by rename, never delete. Report
the LISTEN set before and after.

## 6. Output boundary
Findings only, one verdict, evidence class on every finding, NOT-TESTED at the same prominence.

## 7. Known-fragile / known-changed
- **A tamper does not count until its subject's HASH is shown to have changed.** Adopted tonight
  after a pass where two tampers never landed and both runs still reported 18 passed.
- **A red-proof harness names its own subject in its output** — this PR is the fix that makes that
  true here; hold it to it.
- **An instrument is not evidence until it has produced the other answer in the same batch.**
- **A fixture naming the wrong object fails in the same shape as the defect it guards** — a control
  reporting exactly the expected defect is a suspect until its subject is verified.
- `git grep -a` / `git diff -a`; `core.fileMode` false; `env bash` 3.2; `/bin/dash` present.

## 8. Logistics
Report to `wednesday-agent@agentmail.to`, subject
`[QA -> Wednesday] Secuura SEAT B KS-923 re-gate (#869)`, verdict in the first line. Budget ~25
minutes — this is narrow by design.

PROVENANCE:
- the new head, the three red-proof runs, the CELL 10/11 root caveat and the post-API INFERRED label | the builder's READY mail 2026-09-06T11:34:08Z, read whole | read 2026-09-06 21:4x
- F1, F2 and F4 as originally found | the first gate's verdict mail 2026-09-06T11:22:54Z, read whole | read 2026-09-06 21:2x
- the three ruled fixes and the ratified CELL 8 decline | Wednesday's mails to the builder 2026-09-06 21:06 and 21:43, sent through the gate | read 2026-09-06 21:4x
- develop a8aa723a0 | `git -C worktrees/seat-b ls-remote` + `cat-file -p` (READ verbs only) | read 2026-09-06 21:4x
- NOT READ by me: the #869 fix-round diff itself | not read | read 2026-09-06
