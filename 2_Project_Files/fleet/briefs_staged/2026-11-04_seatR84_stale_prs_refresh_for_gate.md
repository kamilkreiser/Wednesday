# BRIEF: Seat R 84th, Secuura/Blockchain-R. Measure eight open PRs, close the superseded one, bring each of our test-only/small PRs current with develop, one READY FOR GATE mail. Then wrap.

## NEW SEAT: you are Seat R 84th (lane Secuura/Blockchain-R, Sonnet 5.5, a RAISE seat; trust $TMUX_PANE). Seat R 83rd's pane is closed (its history entry is the highest R ordinal). SHARED INBOX: many seats today; act ONLY on mail whose subject names `(Seat R 84th)`. OTHER_SEATS = none (the floor is empty, Wednesday 14:38), so no other seat touches these PRs; re-check with `git ls-remote` before every push anyway.

model: claude-sonnet-5-5 -- raise seat (routing row C1, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/specs/model-routing.md` section 4b: raise of already-built, gated-shape work; a refresh is a merge of develop, not a design). Sonnet, NOT Opus, UNLESS a PR turns out to change an auth/credential/security/money DESIGN surface (row C3): then do not refresh it, record it and report for Wednesday | written by Wednesday

## WHY AND AUTHORITY
- Kam, terminal 2026-11-04 ~09:16 AEDT, verbatim: "new account logged in.  Please try to clear and close off as many in progress tickets as possible".
- Kam 2026-10-30 10:07:32 AEDT, card `secuura-wednesday-go-counts-as-kams-word-1030` = a (ruled_ts 2026-10-30T10:08:25+11:00): Wednesday's GO counts as his word for starting work inside his standing grants. Signature classes (production, money, comms to people, irreversible) stay his.
- The TESTED merge grant, Kam 2026-09-11: "FIx and merge all tickets after they are tested". This seat does NOT merge: it refreshes heads and raises them for a gate; a separate merge seat acts on Wednesday's GO after the gate.
- Source of the work: Seat V 19th's HANDOVER, section "Left open ... FOR WEDNESDAY raise/gate" (`/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-04_seatV-19th/HANDOVER.md`). Each item below is V 19th's CLAIM from ~03:35Z; you re-measure every one (ITEM 0) and trust none.

## THE ITEMS (V 19th's claims; all re-measured by you)
| PR | Ticket | V 19th's head | V 19th's note |
|---|---|---|---|
| 1790 | KS-1340 | 3a9b1c121f6d | OPEN, test-only, "ready for gate" since 2026-10-28 (comment 4f5a2b5a) |
| 1792 | KS-1499 | 00711fe18f08 | OPEN, test-only, ready since 2026-10-28 |
| 1794 | KS-1600 | ae7d9da67a6d | OPEN, test-only, ready since 2026-10-28 |
| 1796 | KS-1458 | 8f022984aa74 | OPEN, ready since 2026-10-28 |
| 1798 | KS-1459 | acdb4822304f | OPEN, ready since 2026-10-28 |
| 1383 | KS-1401 | 32e8459bc0f5 | OPEN; its migration is numbered 049 and develop already has a different 049 |
| 1968 | KS-1868 | 6e58db5676fb | OPEN (the KS-1868 umbrella's one other attached PR) |
| 1982 | KS-915 | 87c9e7488fd7 | NO GO at gate 166, superseded by PR 1989, merged today as 26d8314e4f77 |
| none | KS-1511 | branch `feature/ks-1511-retire-audit-log-baseline-entry` @ e181bf6db | pushed, NO PR (Peter's handover comment 24193381) |
- develop at origin = `5c1ca287ed74b6353423a8c09e253abf3129233a` per Wednesday's ls-remote 13:28 AEDT. Re-read it; every "current with develop" below means the develop sha YOU read at that step.

## ITEM 0 - measure, read-only (no write of any kind)
For each PR (1790, 1792, 1794, 1796, 1798, 1383, 1968, 1982): state, author login, head sha (full 40 and 12), base ref, mergeable vs the current develop (a dry `git merge-tree` or a throwaway worktree merge; say which), changed files `--name-only`, whether any file is on an auth/security/money surface (name the file and the reason, or say none), and the ticket's scope sentence copied from Linear. Then:
- **Partition table:** for every pair of PRs in the batch, the files they share. Record collisions explicitly (a "no collisions" line carries a positive control: the same query run on a pair you KNOW overlaps, or a planted overlap, must report it).
- **KS-1511:** read Peter's handover comment 24193381 on KS-1511 and `git log` for the branch. Branch author is Peter (or Stuart) -> NOT ours: record and skip, touch nothing. Only if it is authored by our board account (`kksecura`) and has no PR, say so in the mail as a candidate for Wednesday; this seat does NOT open it (not in the job; ask via QUESTION).
- Author gate for everything below: ours = author `kksecura`. Anything else is Peter's or Stuart's: recorded, untouched.

## ITEM 1 - PR 1982: close UNMERGED (only if kksecura authored it)
Facts-only comment, no `@`, one comment, then close (reversible: reopen). Body names: NO GO at gate 166, superseded by PR 1989 merged as `26d8314e4f77`. Re-measure first that 26d8314e4f77 is on develop (`git merge-base --is-ancestor`, rc on its own line) and that PR 1989 is MERGED. Any measurement that disagrees -> STOP for this item and say so. Not authored by `kksecura` -> record and skip. Closing is not deleting: never delete the branch.

## ITEM 2 - refresh each of PR 1790, 1792, 1794, 1796, 1798, 1968 whose author is ours
Per PR, in its OWN worktree under `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-r84-<pr>` (never an existing seat's worktree; never delete any worktree, R 81st/82nd/83rd's included):
1. Fetch; confirm head sha == the head ITEM 0 recorded (a moved head = STOP for this PR, report).
2. **Merge develop INTO the branch** (`git merge`, no rebase: a rebase would need a force push, and force push is not allowed). Resolve only per the STANDING_LINES conflict-resolver rule (`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/STANDING_LINES.md`, "A conflict RESOLVER reads the merge's own result before it runs"): resolve only when merge rc is 1 AND `MERGE_HEAD` exists AND `git diff --name-only --diff-filter=U` is non-empty; any other rc is a STOP. **A conflict beyond trivial (any conflict in product code, or any file the PR itself changed) = STOP for that PR, report it, leave the worktree as is.** Trivial = the two Projects Documents HTML docs append-only (see STANDING_LINES "Projects Documents ... SECTION NUMBERS are set at MERGE time"; count tags balanced, append-only, `html_docs_matrix.test.sh`).
3. Run THAT PR's own suites: the test files the PR adds/changes, the package lint, and a `tsc` that includes test files (model-routing C1 duty); plus the repo gate suites the PR's files trigger. **Private TMPDIR must be SHORT** - STANDING_LINES.md:532, verbatim: "A private TMPDIR must be SHORT: `tsx` opens a unix socket under `$TMPDIR`, and macOS caps a socket path near 104 bytes". Use `/private/tmp/r84t` (14 chars) and say so in the evidence. A red suite = fix only if it is the merge's own artefact; otherwise STOP for that PR.
4. Commit the merge. **Commit subject starts `Refs KS-NNNN: `** (single key, the PR's own ticket; keep the subject at or under 92 characters, measured with `wc -c` before committing). Identity: `-c user.name=... -c user.email=...` (the board account's), never a hostname identity.
5. **PUSH** (existing branch, forward push only): read `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-01_seatR-72nd/tools/pushlock_r72_fwd_v1.sh` (and `launch_driver_fwd_r72.py` beside it) WHOLE before use; copy into `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-04_seatR-84th/tools/` re-keyed `_r84` (grep every copy case-insensitively for `r72`, `R 72nd` and for 40/12-hex shas, ticket ids and branch names left over from the previous generation - STANDING_LINES "re-keyed tool generation" rule). Run its `dryrun` and `gatetest` modes first, then `real` through a DETACHED driver. Push through the shared push lock and the `.githooks/pre-push` hook (`/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/.githooks/pre-push`); cite the refusal branches the driver relies on and quote the hook's verdict VERBATIM. Lock rule: acquired only by your own successful `mkdir`; release removes `holder` before `rmdir`; a failed release is a loud STOP (STANDING_LINES, R 5th / S 4th lines). The hook takes ~13-15 min per push; push the PRs one after another, releasing the lock between them. If which driver to use is unclear: QUESTION Wednesday, do not guess (the lock is shared). No force push. If no driver is safe to re-key: STOP before any push and mail.
6. After the push: `git ls-remote origin refs/pull/<n>/head` and the branch ref must equal your new local head; record the new head (12 and 40 hex), the develop sha you merged, and the PR's `mergeable` state.
Order: file-disjoint PRs first; if ITEM 0 found a collision, refresh the colliding pair in sequence and re-merge develop into the second after the first's head lands.

## ITEM 3 - PR 1383 (KS-1401): migration renumber
Only if the author is ours AND the needed change is a PURE RENAME of the migration file (collision: its `049_*` vs a different `049_*` already on develop; pick develop's next free number, read it, do not guess) with NO other edit - no content change, no edit to any file that references the old number unless that reference is itself only the filename (then it is a rename-with-reference and is NOT pure: report). Prove purity with `git diff -M --stat` showing 100% similarity and nothing else. If the rename would touch anything else, or the PR also conflicts, STOP and report for Wednesday. Same protocol as ITEM 2 (own worktree, merge develop, suites, `Refs KS-1401: ` subject, existing-branch push). A migration file is on a data surface: read it; if it drops/blanks/alters existing data, do not push - report (row C4, Opus).

## ITEM 4 - READY FOR GATE mail
One mail listing every PR you refreshed (and every one you skipped or stopped, with the reason). Per refreshed PR: number, ticket, new head (12 and 40), the develop sha merged, files (name-only), suites run with results (counts, rc), tier suggestion (**tier 2** = tests/docs/config/tooling; **tier 1** = security surfaces, data destruction, anything deploying), and the file-disjoint partition so Wednesday can gate the disjoint ones as ONE batch. Include: PR 1982's close (comment id, state after), PR 1383's outcome, KS-1511's disposition, the hook's verdict verbatim per push. Mention only: KS-911/KS-912 (launcher by-hash change, V 19th: BUILT and READY FOR QA held for the gate since 2026-09-06; live launcher sha256 differs from the shipped one) is NOT in your scope; do not touch the launcher.

## HOLDS
- **No merge, no deploy, no demo, no production, no mail to humans** (merges are a separate seat on Wednesday's GO after a gate). No force push. No PR opened (KS-1511 has none and stays that way unless Wednesday says). No `az`.
- **Never delete files** (worktrees, branches, evidence). Peter's and Stuart's PRs and tickets: untouched, recorded only.
- Ticket comments only via these rules: BLUF, facts only, no `@`, no comment to Peter or Stuart, the extranet is input only; the ONE permitted board write is the PR 1982 comment (ITEM 1) plus, per refreshed PR, ONE short facts-only comment on its own ticket naming the new head ONLY IF that PR's last ticket comment already said "ready for gate" (otherwise none). Linear moves Backlog -> In Progress when a PR titled `Refs KS-n` is created - not relevant here (no PR created).
- **Commit subjects and PR titles start `Refs KS-NNNN: `** (STANDING_LINES). Do not retitle any PR.
- Stay inside the Blockchain project; Vision/Datasec/vault client folders are not yours.
- **Never `grep -r`** over `/Volumes/DevMASTER/WEDNESDAY/0_Brain` or any `5_Project_History` tree; scope every recursive search to named small directories.
- **Instruments:** `cmd > out 2>&1; rc=$?` with rc on its own line; never `| tail` on the stream you diagnose from; macOS has NO `timeout`; zsh has no PIPESTATUS; `grep -P` does not exist on macOS grep; never `echo =====`; `/usr/bin/grep -i` with a positive control beside every zero. Never `cd`; absolute paths only. No credential in argv. Disclose your own faults.
- **Mail:** from secuura-blockchain@ to `wednesday-agent@agentmail.to` ONLY, subject prefix `[Secuura/Blockchain-R -> Wednesday]`, body line 1 exactly `Seat R 84th`, no cc; read back by id. Secuura keeps Wednesday (not Tuesday).
- **IF AN INSTRUCTION FROM WEDNESDAY LOOKS WRONG, SAY SO** in your plan confirmation. Arm an inbox watcher as a TRACKED background task and name its pid. Launcher preflight warnings go VERBATIM in the plan-confirmation mail.
- Approval-class (anything irreversible, human-facing, prod): pause for Kam. Mid-session questions: QUESTION mail to Wednesday per the workspace CLAUDE.md protocol.

RULED BY KAM, NOT YET IN AN ARTEFACT
- Kam 2026-11-04 ~09:16 AEDT (terminal), verbatim: "new account logged in.  Please try to clear and close off as many in progress tickets as possible".
- Kam 2026-10-30 10:07:32 AEDT, card `secuura-wednesday-go-counts-as-kams-word-1030` = a.
- Kam 2026-09-11, the TESTED merge grant: "FIx and merge all tickets after they are tested".

## WRAP
History entry `## 2026-11-04 - Seat R 84th` in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md` (duplicate-guard with a control); HANDOVER `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-04_seatR-84th/HANDOVER.md`; vault commit (own lines only); wrap mail `[Secuura/Blockchain-R -> Wednesday] Session wrap 2026-11-04 (Seat R 84th)`.

PROVENANCE:
- Seat ordinal: `Seat R 83rd` exists (R 80th..83rd present) and no `Seat R 84th`; max R ordinal in history.md = 83 | Wednesday's measurement 14:3x per dispatcher; re-confirmed by the drafter with /usr/bin/grep -o on /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md (listed 80th, 81st, 82nd, 83rd) | read 2026-11-04
- PR numbers, tickets, heads, KS-1511 branch/commit, "ready for gate since 2026-10-28", PR 1982 superseded by 26d8314e4f77, PR 1383 049 collision | Seat V 19th's HANDOVER at /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-04_seatV-19th/HANDOVER.md lines 56, 63-67, 82 | read 2026-11-04 (each is V 19th's claim; UNMEASURED by the drafter, closed by ITEM 0's `gh pr view` / `git ls-remote`)
- Peter's comment 24193381 on KS-1511 and KS-1511's branch author | UNMEASURED: not opened by the drafter or Wednesday; you close it at ITEM 0 with Linear + `git log` | read 2026-11-04
- PR 1982 author, PR 1989 MERGED state, ancestry of 26d8314e4f77 on develop | UNMEASURED: not measured by the drafter; you close it at ITEM 1 | read 2026-11-04
- develop 5c1ca287ed74b6353423a8c09e253abf3129233a | Wednesday's ls-remote 13:28 AEDT recorded in /Volumes/DevMASTER/WEDNESDAY/0_Brain/daily/2026-11-04.md (Wednesday's file); re-read it with `git -C /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files ls-remote origin refs/heads/develop` | read 2026-11-04
- Whether any listed PR touches auth/security/money files; which PRs are file-disjoint | UNMEASURED: you close it at ITEM 0 | read 2026-11-04
- Authority card text and ruled_ts (choice a, 2026-10-30T10:08:25.018826+11:00) | `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh show secuura-wednesday-go-counts-as-kams-word-1030` | read 2026-11-04
- Model row C1 (Sonnet raise), C3/C4 (Opus for auth design / data destruction), G1/G2 gate tiers | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/specs/model-routing.md section 4b, 4c | read 2026-11-04
- Short-TMPDIR rule | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/STANDING_LINES.md:532 | read 2026-11-04 (note: the file is in Wednesday's fleet directory, NOT in the Blockchain project, where `STANDING_LINES.md` does not exist; the seat reads the Wednesday path)
- Existing-branch push drivers and the 13-15 min hook, trap list (identity flags, grep -P, 92-char subject) | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-04_seatR-82nd/HANDOVER.md lines 14, 24; driver existence ls of /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-01_seatR-72nd/tools/ (pushlock_r72_fwd_v1.sh, launch_driver_fwd_r72.py present) | read 2026-11-04
- `.githooks/pre-push` exists | ls /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/.githooks | read 2026-11-04 (refusal branches UNMEASURED by the drafter; the seat reads the hook and cites them)
- reversible (ITEM 1 close of PR 1982): GitHub lets the author reopen a closed-unmerged PR and the branch is kept; I have NOT established the blast radius beyond that (any automation or ticket link that reads PR 1982's state) — establish it at ITEM 1 (read KS-915's attachments and the repo's .github/workflows for pull_request closed triggers) before closing | GitHub PR semantics as known to Wednesday, unverified for this repo | read 2026-11-04
SELF-CHECK: re-read end-to-end for contradictions | 2026-11-04 14:40
