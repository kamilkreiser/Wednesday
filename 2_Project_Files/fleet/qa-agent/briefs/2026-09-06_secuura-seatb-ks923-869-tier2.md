# QA Agent Invocation Brief — Secuura / Blockchain (Platform K), SEAT B: PR #869 (KS-923)

**Charter first, in full:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`.
Findings only. You never fix, never file a ticket, never touch a builder's tree.

**TARGET — PR #869, KS-923. TIER 2, through-code.**
head `313f96519cbe75d9f2ff4708b4ce875213a030d1`, cut on `develop a821bd0aad137347954a287707e573e417e8ce9d`.

## 2. Spec / DoD
The security orchestrator's Stage 2 had **no `require_job` guard at all**. The builder measured the
real orchestrator with the Stage-2 tool **absent entirely** and got rc 0, seven jobs run, and
`Stage 2 JOIN complete` — a security-tool dispatch path that could not report its own absence, whose
only trace was the exact false sentence its parent ticket exists to delete. DoD, set by me when I
re-sequenced this ahead of two launcher residues:
1. a cell that REDS when the Stage-2 tool is absent;
2. each of the three states red-proofed SEPARATELY, no fixture tripping more than one condition;
3. the assertion on the ABSENCE of the false sentence, not on an exit code that is already non-zero
   for other reasons.

## 3. Scope — claims to measure. Each is a CLAIM UNDER TEST.
1. **The three states, separately.** The builder reports CELL 6 (absent), CELL 7 (present but 644)
   and CELL 8 (invocation shape) red against the pre-fix orchestrator and green on the fix, with
   CELLS 1–5 (the parent ticket's) green in BOTH runs. Re-derive it: 9/9 on the fix, 6/3 pre-fix,
   and confirm no fixture trips more than one condition (`build_fixture`'s third argument is said to
   be the only thing that varies: `exec | noexec | absent | failing`).
2. **CELL 9 is the control for an ABSENCE assertion — press on it.** A cell asserting a string is
   absent is worthless if the string is never emitted. CELL 9 is said to build a Stage-2 tool that
   RUNS and exits 3, assert the sentence IS printed, and assert the run does not fail — green in
   both runs by design. **Verify it can produce the other answer**, and verify CELL 6 is genuinely
   blind without it.
3. **HUNT — the `ORCH_SH=` hook is the instrument, so test the instrument.** The pre-fix run is done
   by pointing the suite at an `orchestrate.sh` extracted from `a821bd0aa`, with no file tampered
   and nothing checked out. **Can that hook silently fall back to the fixed file?** Name the
   assertion before you run: if `ORCH_SH` is unset, empty, or points at a non-existent path, does
   the suite fail loudly or quietly test the shipped file and report green? A red-proof that can
   silently grade the wrong subject is the failure mode this whole ticket is about.
4. **CELL 8 is the builder's own stated weak point and it asked for your judgement.** It pins the
   invocation by grepping the source for `bash "$SC_TOOL"` — a text assertion about code, not a
   behavioural one: it would survive a rename that broke nothing and red on a cosmetic reformat.
   The builder could find no behavioural way to distinguish `bash "$p"` from `"$p"` when the file is
   executable, and says CELL 7 covers the case that matters. **Say whether a behavioural
   discriminator exists, and whether CELL 8 earns its place or should be dropped.** Your call is
   input to mine, not the decision.
5. **The KS-922 overlap — verify the split is exactly as claimed.** The builder took the **stage-2
   half** of KS-922 (`"${stage2_pids[@]:-}"`) because CELL 6's absence assertion is unreachable
   without it: with the guard in place and the tool absent, bash 3.2 expands an empty array to one
   empty word, `wait ""` fails, and the false sentence prints anyway. **`stage1_pids` at :97 is said
   to be untouched.** Confirm that, and confirm the overlap is declared in the commit message, on
   the PR and on both tickets.
6. **Regression on the healthy path.** With the Stage-2 tool present and executable, does the run
   behave exactly as before the fix? CELLS 1–5 green in both runs is the claim; measure the
   orchestrator itself, not only the suite.
7. **HUNT — the guard's own edges.** Name the assertion first, then measure: a `SC_TOOL` path
   containing a space; a tool present but not readable; a tool whose shebang differs from the jobs
   already invoked via bash (the builder confirmed `#!/usr/bin/env bash` with a control read in the
   same batch — verify that control).
8. **Modes are index facts here** (`core.fileMode` is false): confirm `orchestrate.sh` is still
   100755 and the suite 100644 in the index at both SHAs.
9. **Merge-tree against the `develop` you read AT THE TIME, in YOUR OWN copy.** Develop is moving —
   seat A is live. I ran no merge-tree; nothing here is predicted.
10. **Secret gate:** no gitleaks canary exists in the repo. Build your own fabricated pair, prove it
    FIRES in the same scan mode, quarantine by rename, then scan the real range.

## 4. Credentials
Pointer only: the project's own `4_Credentials/.env`. You should need none.

## 5. State-mutation & cleanup
Your own `mktemp` checkout with its own index. **Never touch seat A's tree (`2_Project_Files`) or
seat B's worktree (`worktrees/seat-b`)** — both are live. Never the demo VM, the shared local stack,
or Docker on this box. **No prune of any kind, and never run the real security jobs.** Restore any
tamper by inverse edit and prove byte-identity by sha256. Quarantine by rename, never delete.
Report the LISTEN set before and after.

## 6. Output boundary
Findings only, one verdict, evidence class on every finding that recommends an action, and the
NOT-TESTED list at the same prominence as the findings.

## 7. Known-fragile / known-changed
- **Every tamper prediction NAMES THE ASSERTION it trips**, or is written as "measure what moves".
  Hold me to it: if a hunt above states a consequence without naming its assertion, say so.
- **An instrument is not evidence until it has produced the other answer in the same batch.**
- **A control that mutates its subject is not a control** — extract with `git show`, never
  `git checkout`, in a tree another seat is holding.
- `rm -f` exits 0 on a path that does not exist, and zsh does not word-split an unquoted variable:
  a deletion loop can print success for six deletions that never happened. The control is the
  listing afterwards.
- A `git show <sha>:<path>` for an absent path prints `fatal` and `grep -c` reads 0 — resolve by
  `ls-tree` first. `git grep -a` / `git diff -a` in this repository.
- `env bash` on this box is 3.2; `/bin/dash` is present; Docker here is linux/arm64.

## 8. Logistics
Report to `wednesday-agent@agentmail.to`, subject
`[QA -> Wednesday] Secuura SEAT B KS-923 (#869)`, verdict in the first line. Report path under the
QA project's own `projects/secuura/reports/`. Budget ~30 minutes.

PROVENANCE:
- the head, its base, and that both were re-read from origin rather than taken from push output | the builder's READY mail 2026-09-06T11:03:11Z, read whole | read 2026-09-06 21:0x
- the defect this fixes (rc 0, seven jobs run, "Stage 2 JOIN complete" with the tool absent; the suite green in all three states) | the builder's STATE mail 2026-09-06T10:53:33Z, read whole | read 2026-09-06 20:5x
- the three DoD conditions | Wednesday's ACK to the builder 2026-09-06 20:55, sent through the gate | read 2026-09-06 20:55
- develop a821bd0aa and its parentage | `git -C worktrees/seat-b ls-remote` + `cat-file -p` (READ verbs only; no fetch, no merge-tree, no worktree add in either seat's checkout) | read 2026-09-06 20:4x
- NOT READ by me: the #869 diff itself — I have read only the builder's description of it | not read | read 2026-09-06
