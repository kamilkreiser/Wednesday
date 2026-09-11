# QA GATE BRIEF — Secuura/Blockchain PR #953 (KS-1086) — TIER 2 (through code), ROUND 2

**Charter — read first, in full:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`

PRIOR ROUND: round 1 gated `de1ab62c021a480478dace5da4a3815945da987c`, verdict **GO WITH FINDINGS** (the fix ESTABLISHED end to end).
ITS REPORT IS ON DISK AT: `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-11-ks1086-953-de1ab62c0-tier1/` (`report.md` + `evidence/`)
Findings carried forward and their disposition: **QA-1** fixed on `8987b8a0e` (cells Q1a/Q1b) · **QA-2** fixed on `8987b8a0e` (refusal on zero parsed names or no `GIT_DIR`; cells Q2a/Q2b/Q2c) · **QA-3** fixed OUTSIDE the PR (the push-protocol harness — not in this gate) · **QA-4** carried as HOLD wording, not code · **QA-5** fixed in the PR body (a dated Round 2 section) · **QA-6** filed as KS-1088 (Low).

## WHY TIER 2, AND WHAT THAT MEANS

An already-gated follow-up: round 1 reproduced the incident and showed the fix closes it. Round 2 changes the SAME two files by +102 −9 to close two Minor findings. **Through code:** re-derive the delta's claims in your own by-SHA clone with the builder's test file and tampers. **The end-to-end incident reproduction is NOT re-commissioned** — except where item 2 needs a hook environment to prove there is no false refusal.

## TARGET

- **PR #953** — branch `feature/ks-1086-preflight-leg-14-runs-the-shell-suites-under-the-hooks-git`, head **`8987b8a0ecfae29aed2b934188d947a1a6a581df`**, parent `de1ab62c0`, merge-base develop **`2d864ae9220c57ddcd8dc77af1b80fbd8001d530`** (ahead 2, behind 0), 0 reviews.
- **Delta `de1ab62c0..8987b8a0e`:** 1 commit — `Blockchain/Dev/scripts/run-shell-suites.sh` (+27 −9) and `Blockchain/Dev/scripts/__tests__/run_shell_suites.test.sh` (+75 −0).
- **Repo READ-ONLY:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files`. Clone by SHA into your own scratch; build trees from the SHA's own objects (round 1: `tar` + `git add -A` dropped 91 tracked files the repo's `.gitignore` excludes).
- 🔴 **NEVER run a push, the real `.githooks/pre-push`, or `preflight.sh` inside that checkout or any worktree of it.**
- **The builder's claims are inputs to falsify:** s178's READY FOR QA mail (2026-09-11 02:43:20Z) and bite table; the PR body's Round 2 section; aims at `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/s178-ks1086-round2/AIMS.md`.

## WHAT ROUND 2 MUST ESTABLISH

1. **QA-2 is closed.** A CRLF-printing fake `git` → REFUSED, rc 1, no suite run, the reason printed · a list without `GIT_DIR` → REFUSED · an empty list → REFUSED. **Re-run YOUR OWN round-1 CRLF probe against `8987b8a0e`:** on `de1ab62c0` it printed "of 0 repository-local name(s)", rc 0, ran the suite and wrote `core.bare=true` into the scratch shared config — it must now refuse and write nothing.
2. 🔴 **NO FALSE REFUSAL — the regression this change can introduce, and the one that would block every developer's push.** The new condition reads git's LIST of names, not the environment. Show the head's runner does NOT refuse, and runs 18/18, in: (a) a clean environment with no `GIT_*` set, (b) a linked-worktree pre-push hook environment, (c) a normal-clone pre-push hook environment. Compare the per-suite verdict sets with round 1's R2 / F2 / F4 where comparable — the set, not the count.
3. **QA-1 is closed.** Q1a/Q1b drive `GIT_DIR` + `GIT_WORK_TREE` + `GIT_CONFIG_PARAMETERS` and assert all three unset in the suite and named in the verdict line; **T8 (the list cut to `GIT_DIR`) reddens them by ASSERTION.**
4. **Bite — re-run yourself:** T1 · T2 · T3 · T6 · T8 · T9 (the `GIT_DIR`-membership condition removed → the builder says only Q2b reddens) · T11 (the `de1ab62c0` runner → the builder says Q2a and Q2b). Cells run quoted (the builder reports 32); classify assertion vs load; restores by sha256. **Is Q2b load-bearing, as claimed?**
5. **bash 3.2 portability.** macOS `/bin/bash` is 3.2.57 and the change parses the list into an ARRAY. Search the delta for bash-4-only constructs (`mapfile`, `readarray`, `declare -A`, `${x,,}`, `${x^^}`, `|&`, `&>>`) with `/usr/bin/grep` and a positive control, and run the cells under `/bin/bash`. **Specifically: an EMPTY array expanded as `"${arr[@]}"` under `set -u` is an unbound-variable error in bash 3.2** — if the runner uses `set -u`, drive the empty-list path and show it refuses cleanly rather than crashing with a different message.
6. **The PR body's Round 2 section:** the QA-5 correction is present and accurate, and the protocol block quotes the PROTOCOL-DIFF and Wednesday's ruling verbatim, as the builder claims.

## NOT COMMISSIONED — said before running

- The end-to-end incident reproduction (round 1 did it). Any push to GitHub. The real hook or preflight in the checkout. Platform suites, containers, `127.0.0.1:6882`, kintsugi, demo.
- `push_protocol.py` — harness outside the PR, not in this gate.
- bash 5 / Linux, Git for Windows, GitHub Actions: report NOT RUN.

## KNOWN-FRAGILE / KNOWN-CHANGED

- 🔴 **Your tool shell's `grep` may be a SHELL FUNCTION:** a pattern containing `$(` reads 0 through it and 1 through `/usr/bin/grep`. Run `whence -va grep` first; use `/usr/bin/grep` with a same-file control for anything you report.
- zsh: no `PIPESTATUS`, and unquoted list variables do not word-split — round 1 voided two loops on it.
- `mergeable_state` is inverted on this repo — ignore it. The shared checkout still holds `feature/y` / `feature/w` — leave them.

## BOUNDS

Findings only — no fix, commit, push, merge, deploy, comment or ticket. No contact with Peter or Stuart. No `--no-verify`. **Never `rm`** — a fresh `mktemp -d` per attempt; guard every expansion `"${X:?unset}"`. **At start and at end, quote from the Secuura checkout (read verbs only):** `git --no-optional-locks status --porcelain | wc -l`, `shasum -a 256 .git/config` (Wednesday read `e0fa706f4bdae2778a5fe5975676f24459c5a3c6455de4ae85aa286f67632d1a` at 12:4x AEST) and `git for-each-ref | wc -l` (798 then). **They must match each other.**

## REPORT

FOUND / TESTED / HOW with controls; every action-recommending finding carries its evidence class (**MEASURED AT RUNTIME / PROBED / READ ONLY**). NOT TESTED at the same prominence. Head readings start / mid / end with timestamps and the branch beside each SHA. **If a claim in this brief is false, that is Wednesday's error — report it as one.** Write to `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-11-ks1086-953-8987b8a0e-tier2-r2/` and name the absolute path in the mail.

**Verdict:** GO · GO WITH FINDINGS · NO GO — and say whether each finding is IN THE DELTA or pre-existing at `de1ab62c0`.

## VERDICT DESTINATION

**Mail your verdict to `wednesday-agent@agentmail.to`**, subject
`[QA -> Wednesday] TIER 2 GATE #953 ROUND 2 (KS-1086) 8987b8a0e — GO / GO WITH FINDINGS / NO GO`,
with a CLOSING section naming anything you want acted on. **Your pane has no scrollback and you cannot receive mail: the verdict mail is the only thing that survives your session.**

PROVENANCE:
- #953 head 8987b8a0ecfae29aed2b934188d947a1a6a581df, 2 commits, 2 files, 0 reviews, not merged; delta de1ab62c0..8987b8a0e 1 commit, run-shell-suites.sh +27 -9, run_shell_suites.test.sh +75 -0; merge-base 2d864ae92 ahead 2 behind 0 | https://api.github.com/repos/Secuura/Distributed_Secuura/pulls/953, /compare/de1ab62c0...8987b8a0e, /compare/develop...8987b8a0e | read 2026-09-11
- PR body carries the Round 2 section (Correction, show-toplevel, PROTOCOL-DIFF, 8987b8a0e present) | https://api.github.com/repos/Secuura/Distributed_Secuura/pulls/953 body, 25251 chars | read 2026-09-11
- builder claims: QA-1/QA-2 cells, bite table T0-T11, Q2b extra cell, bash 3.2.57 and git 2.51.0 environment, push DIFF ruling | s178 READY FOR QA mail 2026-09-11T02:43:20Z, structured spf/dkim/dmarc pass | read 2026-09-11
- KS-1086 READY comment 19d9b52a names 8987b8a0e | Linear KS-1086 comments | read 2026-09-11
- round 1 verdict, findings QA-1..QA-6, CRLF probe, R2/F2/F4 verdict sets, tree-from-objects void | /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-11-ks1086-953-de1ab62c0-tier1/ via the verdict mail 2026-09-11T01:41:19Z | read 2026-09-11
- shared checkout config sha256 e0fa706f..., for-each-ref 798 | Wednesday's read-only readings on /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files | read 2026-09-11
- tool-shell grep is a function; $( pattern reads 0 | Wednesday's own shell, whence -va grep and a planted two-line file (measured, not read) | read 2026-09-11
