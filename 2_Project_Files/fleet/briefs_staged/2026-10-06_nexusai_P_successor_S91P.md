# BLUF — SUCCESSOR SEAT Datasec/NexusAI-P (lane 4): LAND RD-719 @ 7861a06 in P's next merge turn (gate 15 = GO WITH FINDINGS, no Blocker), file ONE findings ticket for it, then start RD-721 under its recorded rulings. RD-430 and RD-694 item 4 are in gate 14 (live): wait for Tuesday's RELEASE on those. Send a PLAN CONFIRMATION to Tuesday before filing any merge ticket.

**Addressed to the cockpit seat `Datasec/NexusAI-P` ONLY.** `Datasec/NexusAI-M`, `-N`, `-O` and `-R` are live and share this inbox (datasec-nexusai@), and gates 14, 17 and 18 are live too. A mail addressed to another seat is not yours. Establish your seat from your own pane's cockpit name (`tmux display -p '#{@cockpit_name}'`), your launcher and your process tree, never from which thread looks familiar. Number your session from the highest HANDOVER-S* on disk (S90S was the last at 21:2x AEDT): you are **S91P** unless a newer one appears.

## READ FIRST, in this order (all in the NexusAI folder)
1. `HANDOVER-S86P.md` WHOLE — your lane's state. Its sections 7-9 are current; its RESUME card (top) is SUPERSEDED by this brief (the pause it names ended 2026-10-04; batch 6 is closed, section 9).
2. `1_Project_Definition/CLARIFICATIONS.md`: C-182 and its ADDENDUM (around :1902, RD-719/RD-721 rulings), C-185 and its addenda (around :1973-1979, the known-failing set and the local re-run rule), C-186 + its 2026-09-29 ADDENDUM (merge turns), C-190 + its addendum (around :2029: pre-scan BOTH CodeQL thresholds), C-141 addenda 1-6 (around :1500-1530; addendum 6 is today's lock change). Line numbers are Tuesday's earlier reads, not re-derived now: find each by its C-number.
3. The gate 15 report, WHOLE: `Testing Agent MAIN/projects/nexusai/reports/2026-10-05-gate-batch15/report.md` (RD-719 is member A).

## AUTHORITY
- Merges: the open-ended NexusAI grant "work through the tickets and merge once tested" (Kam, 2026-09-25, re-affirmed 2026-09-27; Tuesday's EXPIRING-GRANTS row), on Tuesday's GO after a QA gate verdict at the head. This mail IS that GO for RD-719 @ 7861a06 (the AUTHORITY to merge; the TIMING is set separately by the TURN mail below), carried through a forward merge of the then-main (the gate's "onto END main 9938876: counts only" no longer describes main, see below).
- Tuesday's ruling on A-F1 (MAJOR, coverage): **land RD-719 now; A-F1 is fixed in the follow-up ticket's FIRST round (tier 2, through code).** Why: the shipped bytes are proven identical to upstream (gate R-NET, cmp rc 0); A-F1 is a gap in what the cells guard (a consistent file + record + attribute swap stays green), not a product defect; RD-721 is blocked behind RD-719.

## MEASURED BY TUESDAY (2026-10-06 21:1x-21:2x AEDT)
- NexusAI main = **d97039f** (head SHA of the push runs, `gh run list --branch main`, read 21:13 AEDT with NexusAI's own gh config). Push runs on d97039f: Gitleaks success, Deploy demo SKIPPED, npm-audit failure (RD-816's advisory, expected), **Build 37447602745 IN PROGRESS** at 21:13. Main moved 9938876 -> d97039f by RD-424 r2 (PR #54).
- Jest lock (read 21:14 AEDT, `session-tools/locks/`): holder `s89r-rd794-hold08-proof`; waiting `qa-b14-H11`, `qa-b17-HF2`.
- `session-tools/nexusai-lock.sh` was REPLACED 10:13:02Z by seat O (RD-821): `--replace <own-ticket>` and merge-first placement (merge-tagged tickets go ahead of waiting builder tickets; gates keep their places). Read O's shared-bus mail of 10:13Z ("nexusai-lock.sh replaced") before your first lock call.

## MERGE TURN — where you stand
- Next turn: **N (RD-653)** when Build 37447602745 is green, unless gate 18 GOs RD-816 first (then RD-816 lands first, M's merge). Then M's RD-735 after RD-816. **Your RD-719 takes the turn after those, Tuesday will name it in a TURN mail.** (N taking RD-653 straight after RD-424 does not break C-186's "never two in a row while another author is ready": lane 4 had no live seat, so P was not a ready author when the turn was given.) Only file the merge ticket when that TURN mail names you (C-186 rule: only the author whose turn it is files one).
- Until then, prepare locally (no lock time needed for this): forward-merge the then-main into `rd-719` in your worktree `worktrees/s86p-rd719`, run the merge-tree dry run, and have `session-tools/s86p/merge-hold.sh` ready with the gate's C-68 set for RD-719 (rd490's browser guard is on it, per your S86P table).
- Landing step, unchanged (C-190 + addendum): hold passes → counts commit → C-89 → push the branch → PR to main (no reviewers or labels) → a background wait that EXITS until every CodeQL Analyze completes with no NEW alert at either threshold (security high+ AND rule severity `error`) → `git push origin "${SHA}:refs/heads/main"` as a fast-forward of the SAME sha (braced: zsh modifiers) → read main back by ls-remote (publickey denial = transport, retry up to 5x, RD-738) → Deploy demo must be SKIPPED → Build failing set inside C-185's known set {rd549 O4 envReached-only, rd549 C2/C10 envReached-only}; anything else is a STOP → Jira comment + Release Ready → MERGED mail to Tuesday.
- MERGED mail also carries A-F3 (the READY said 10 `new Chart(` sites; the gate counted 16) and A-P1 (15:55:13Z vs 15:55:14Z), as the gate asked.

## FINDINGS → ONE TICKET (Kam's one-ticket rule), filed by you, linked to RD-719, BEFORE the merge
- A-F1 MAJOR (C-40): a cell pinning the sha384 (or upstream sha256 fbc4…e710) to a CONSTANT independent of the provenance record; the gate's M-swap must turn it red.
- A-F2 Minor: the V3 no-CDN matcher misses protocol-relative `//cdn` tags, CDN URLs inside shipped `.js`, and pages under a `static/` subdirectory. Scheme-optional matcher over the shipped set (.html + .js).
- A-F4 Minor: the MIT notice TEXT ships for neither Chart.js nor @kurkle/color; a shipped third-party notices file (RD-721 can carry it — say which in the ticket).
- A-N1 (deployment note, goes on RD-721 as a comment): `/vendor/` is outside STATIC_ASSET_PREFIXES, so signed-in requests for it stamp session activity.
- Before filing: search the board by symbol/path (STATIC_ASSET_PREFIXES, chart-3.9.1, V3) and say in the ticket what you searched and found.

## THEN: RD-721
Starts only after RD-719 has LANDED. Its rulings are recorded: the C-182 ADDENDUM and Tuesday's 2026-10-05 ANSWER (Bootstrap 5.3.0 everywhere; item 4 first as a REPORT, never a removal; one tier-1 round per library with both-theme before/after screenshots; Icons measured first with a control; Font Awesome 6.0.0 + PapaParse 5.5.3 vendored as they are, each with an RD-719-shape provenance record). If that ANSWER is not yet a C-number addendum, record it first and mail the C-number back.

## RD-430 + RD-694 item 4
Both are MEMBERS of gate 14 (`fleet/qa-agent/briefs/2026-10-05_nexusai-gate-batch14.md`, Tuesday's tree), which is live. Do nothing on them until Tuesday's RELEASE.

## RULED BY KAM, NOT YET IN AN ARTEFACT (Tuesday's card store, `decision_queue.sh list ruled --undelivered`, read 21:2x AEDT)
- `rd104-gh-identity-acceptance-false-premise` (ruled `youcheck`, 2026-09-07) — not lane 4's; no action for you.
- `t9-nas-leg-direction` (ruled `a`, 2026-09-21; a drive backup leg) — not lane 4's; no action for you.
Unverified by Tuesday whether either already sits in an artefact; neither touches RD-719 or RD-721.

## RULED BY TUESDAY FOR THIS PROJECT, STILL OPERATIVE
- The A-F1 ruling above (this mail).
- C-186 + addendum: merge order O, P, M, N; the turn passes to the next READY author after each push Build is green; never two turns in a row while another author is ready.
- C-185 local rule (2026-10-06, CLARIFICATIONS around :1978): a LOCAL merge-hold verify failing ONLY on a known-set cell is re-run ONCE as a fresh hold; any other failure, or a second consecutive known-set red, is a STOP with both logs to Tuesday.
- C-141 addendum 5: yield once per gate TAG.
- Seats on one launcher launch one at a time (2026-10-04): you are the only launch this hour.

## STANDING LINES
- PRIOR-WORK CHECK: before rebuilding, replacing, removing or redesigning anything, look first (git log -S/--follow/blame, CLARIFICATIONS, history, handovers, tickets), write down what existed and why with its source; every READY FOR QA carries a PRIOR WORK section (or "nothing replaced").
- CodeQL: never push an unscanned commit to main; never bypass; never dismiss an alert (fix it in code).
- Never delete: quarantine/move. Never edit a script while a copy of it runs. Never kill by pattern (C-174).
- Every factual sentence in a mail names its instrument, or says "unmeasured". Mail a partial result BEFORE any wait.

PROVENANCE:
- main = d97039f; push runs Gitleaks success, Deploy demo skipped, npm-audit failure, Build 37447602745 in_progress | gh run list -R datasecau/Reporting_Dashboard_Au --branch main (your own 4_Credentials/.gh-config, account kamilDatasec) | read 2026-10-06
- jest lock holder s89r-rd794-hold08-proof; waiters qa-b14-H11, qa-b17-HF2 | your own session-tools/locks/nexusai-jest.lock + queue-jest/ | read 2026-10-06
- nexusai-lock.sh replaced 10:13:02Z, sha256 051f18d6...0244 | shasum of the file + seat O's READY mail 10:13:50Z | read 2026-10-06
- RD-719 @ 7861a06 GO WITH FINDINGS (A-F1 Major, A-F2/A-F4 Minor, A-F3, A-P1, A-N1) | your own Testing Agent MAIN/projects/nexusai/reports/2026-10-05-gate-batch15/report.md, via /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/briefs_staged/2026-10-06_nexusai_P_rd719_gate15_RELEASE.md (Tuesday's tree, not yours) | read 2026-10-06
- lane 4 state (RD-430, RD-694, RD-719 worktree, RD-721 queued, batch 6 closed) | NexusAI/HANDOVER-S86P.md sections 7-9 | read 2026-10-06
- RD-430 + RD-694 item 4 are gate-14 members | /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-05_nexusai-gate-batch14.md header (Tuesday's tree) | read 2026-10-06
- RD-721 round-1 rulings | /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/briefs_staged/2026-10-05_nexusai_P_rd721_versions_ANSWER.md (Tuesday's tree; the same text was mailed to you 2026-10-05) | read 2026-10-06
- undelivered NexusAI cards rd104-gh-identity-acceptance-false-premise, t9-nas-leg-direction | /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/tools/decision_queue.sh list ruled --undelivered (Tuesday's tree) | read 2026-10-06
- highest HANDOVER is S90S | ls NexusAI/HANDOVER-S* | read 2026-10-06

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-06 21:17 (fixed: GO vs TURN timing; N's consecutive turn explained)

## PLAN CONFIRMATION
Mail `[Datasec/NexusAI-P -> Tuesday] QUESTION: plan confirmation` with: your seat identity facts (pane id, cockpit name, claude pid), what you read, your forward-merge plan for RD-719 onto the then-main (with the merge-tree result), the findings ticket draft, and any launcher preflight warnings verbatim. Then prepare locally and wait for the TURN mail (your wake: Tuesday's mail plus a tap).
-- Tuesday
