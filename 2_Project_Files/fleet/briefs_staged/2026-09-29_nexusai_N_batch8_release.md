# BLUF — Datasec/NexusAI-N (lane 2): BATCH 8 PASSED and you are its MERGE AUTHOR. RELEASE all three, one at a time, in this order: RD-700 -> RD-609 -> RD-648. Each goes through a PULL REQUEST under C-190, and the FIRST one lands only after Tuesday's fleet mail confirms M's landing step for PR #32. B-O1 is RULED below: ACCOUNTED for this transition merge. Then file three follow-up tickets.

Verdict: QA/NexusAI-batch8, mailed 2026-09-29 00:44Z. Report `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-29-gate-batch8/report.md` (read whole by Tuesday 10:4x AEST). Read §0, §9, §10 and §18 before the first merge.

## THE RELEASE (the gate's order, measured order-independent: both orders give tree 02f87dd)
1. RD-700 `rd-700-rd411-control-comment-s86n` @ `006b056` — GO (tier 2). Comments only, by two instruments.
2. RD-609 `rd-609-gate-table-archive-name-s86n` @ `8f9d921` — GO WITH FINDINGS (tier 2).
3. RD-648 `rd-648-harness-boot-residuals-s86n` @ `e1c7b21` — GO WITH FINDINGS (tier 2). Last, so its C-68 union runs on the tree that holds everything.
Heads and main read by Tuesday with `git ls-remote origin` at 10:49 AEST: main `dd15ce1`, the three heads as above. Re-read ls-remote before each merge.

## PER MERGE (unchanged pattern + C-190)
- Forward merge onto current main (never rebase, C-68). The gate measured every conflict as the counts file only; regenerate counts ONCE per merge.
- C-57 id-superset in a CHECKOUT (K1). The gate measured K1/K1 missing 0.
- Full verify through the lock, SESSION_SECRET unset.
- Open a PR from the merged branch, wait for CodeQL (a background wait that EXITS), no NEW high+ alert in changed code (test code too), never dismiss an alert. A CodeQL-pattern fix commit on top of a gated head does not need a re-gate, but mail its diff (sha + files) to Tuesday before landing so Tuesday reads it at source first. Your queued `s86n-rd648-codeql` ticket counts: if it moves RD-648's head, say so and name the new sha.
- Land with the step Tuesday mails the fleet once M's PR #32 lands. Until that mail, open PRs and wait for CodeQL only; do NOT land anything.
- Turns: C-186 order (O, P, M, N) and the merge-turn rule are unchanged.
- MERGED mail per ticket: main sha (ls-remote), parents, counts, C-57 result, PR number, CodeQL result, Build run id + failing set (must sit inside the known set; M0's Build was fully green), demo run id (must be SKIPPED).
- **C-68 for the merge author (gate §0, §18.2):** RD-681 (M, in flight), RD-652 and RD-618 (batch 7) each add a harness consumer, and RD-681 changes `backend/server.js`. Whichever of RD-648 and each of those merges SECOND re-runs the harness union BY NAME on the real merged tree (23 requirers + rd648 + the added consumer).

## RULED BY TUESDAY — B-O1 (gate §9.8, for C-183)
The gate measured a K2/K2 C-57 on this transition merge missing exactly RD-609's OLD title, because the parents' file registers the OLD title in every tree kind and only RD-609 makes it tree-dependent. **RULING: ACCOUNTED under C-133's ADDENDUM for this transition merge only**, on three conditions the gate measured: (1) C-133 on blobs holds (merged blob `58d3994` = RD-609's; since `3d05567` only RD-609 changed the file); (2) the NEW title is present and PASSED in the K2 merged run; (3) the only missing id is that OLD title. Any other missing id = STOP. Once RD-609 is on main both sides are tree-aware and the pair no longer appears. It blocks no merge anyway: your C-57 runs in K1. Record it as an addendum to C-183 in CLARIFICATIONS with this provenance, and mail Tuesday the C-number.

## TICKETS (one per logical path; search the board by symbol and path first, and say what you searched)
1. RD-648 follow-up, "harness boot deadline": A-F1 (the deadline term guarded by no cell; fix-shape: H1 bound `r.ms < bootTimeoutMs + 1500`), A-F2 (a live server whose EVERY /api/health answer takes > 5 s now fails its boot; the READY :28 sentence is untrue for that shape; fix-shape: let an attempt after a timed-out one run to the time remaining, plus an "always 6 s" cell), A-F3 and A-F4 as Polish items inside it. Also note the consumer count is 22 requirers at M0, not 25.
2. RD-609 follow-up, "gate-table format check": B-F1 (a malformed row after a blank line inside the section is reported by nothing; `shaFormatProblems` should read to the same boundary as `gateRows()`, plus a cell), B-F3 (no git on PATH reads as "NOT A GIT CHECKOUT"), B-F2 and B-N1 as notes inside it.
3. Suite archive half (gate §9.7, §18.5b; pre-existing, not a batch 8 defect): 14 suites (171 cells) call `git ls-files` and fail identically from a `git archive` (K2) tree at `dd15ce1`, so C-183's premise that gates run from archive trees holds only for K3. Backlog, tier to be set when it is worked.

## RULED BY KAM, NOT YET IN AN ARTEFACT
- rd104-gh-identity-acceptance-false-premise: Kam's own action (two settings pages); nothing for N to land.
- t9-nas-leg-direction: not N's work.

## HOLDS
No deploy, no demo, no Partner Center, no `.github` or ruleset change, never dismiss a code-scanning alert. Ticket comments only for anything client-facing. PRIOR-WORK CHECK; never delete (quarantine).

PROVENANCE:
- verdicts, order, tree 02f87dd, C-57 K1/K2 results, findings, C-68 note | /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-29-gate-batch8/report.md | read 2026-09-29 10:4x
- main and the three heads | git ls-remote origin, run in your own 2_Project_Files (read verb) | read 2026-09-29 10:49
- C-183 text (the id-set condition) | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/1_Project_Definition/CLARIFICATIONS.md:1886 | read 2026-09-29 10:5x
- C-190 PR route and the landing-step hold | Tuesday's ANSWER to all NexusAI seats 2026-09-28T22:07Z (datasec-nexusai@ inbox) | read 2026-09-29 10:5x
Self-check note: previous mails to N naming these ids (the 09-27 19:33Z RD-609 ruling) are consistent; B-O1 extends C-183, it supersedes nothing.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-29 10:50
