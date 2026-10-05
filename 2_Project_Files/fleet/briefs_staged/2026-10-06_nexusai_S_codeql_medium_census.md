# BLUF — NEW SEAT Datasec/NexusAI-S: a READ-ONLY CENSUS of the 103 MEDIUM CodeQL alerts open on NexusAI main, mapped to Jira, exactly as seat Q (S88Q) did the 143 critical+high last night. Map each alert to a ticket that already covers it, or file ONE grouped ticket per fix shape for the rest. NEVER dismiss. No code changes, no pushes, no jest. Deliverable: a census file and a REPORT mail to Tuesday. Tuesday tells Kam.

**Addressed to the cockpit seat `Datasec/NexusAI-S` ONLY.** `Datasec/NexusAI-M`, `-N`, `-O` and `-R` are live and share this inbox (datasec-nexusai@). The older `[... -> Datasec/NexusAI-Q]` census mails in this inbox were for a seat that has WRAPPED: they are your TEMPLATE, not your brief. Establish your seat from your own pane's cockpit name (`tmux display -p '#{@cockpit_name}'`), your launcher and your process tree. Number your session from the highest HANDOVER-S* on disk (S89R was the last), suffixed with s.

## AUTHORITY
- Kam, live board 2026-10-06 07:07:35 (view=tuesday), verbatim: *"Decision nexusai-codeql-medium-alerts-ticketing: a — Ticket the mediums the same way"*. The card's option (a) read: one read-only seat, grouped tickets per fix shape, never dismiss.
- Ticket creation and comments on RD are inside the v1.3 delegated scope.

## WHAT IS MEASURED (Tuesday, 2026-10-06 ~07:08 AEDT)
- main = 2f0ae4a (ls-remote). The open set is 246 (5 critical, 138 high, 103 medium), all CodeQL. Controls: fixed #248 absent, known-open #239 present.
- The 103 MEDIUM by rule: js/log-injection 72 (ALL rule severity ERROR), js/file-access-to-http 14, js/http-to-file-access 5, js/prototype-polluting-assignment 3, actions/missing-workflow-permissions 3, js/identity-replacement 2, actions/unpinned-tag 2, js/shell-command-injection-from-environment 1, js/xss-through-exception 1. By rule severity: 72 error, 31 warning.
- Main is MOVING tonight (RD-648, then RD-618 land), so re-fetch the set yourself at start, quote your count and the main sha, and pin the census to that sha.

## THE TEMPLATE (read whole first, all in the NexusAI folder)
- Seat Q's evidence: `evidence-s88q-codeql-census/` (summary.md, census.csv, medium-appendix.csv) and `HANDOVER-S88Q.md`. Reuse its METHOD exactly: the paginated fetch with its Link-header proof; the prior-work search by RULE ID, FULL PATH, BASENAME and ALERT NUMBER over ALL RD issues AND comments, with a positive and a negative control; the census columns; labels `codeql-baseline` + `security`; component `security-compliance`; our account as assignee; BLUF/Recommendation/Detail ticket bodies with the alert list (path:line + URL) and the grouping test used.
- The grouping rule Tuesday ratified for Q (the Q plan ANSWER 2026-10-05T11:28Z): test code = ONE ticket per rule across all test files; product code = ONE ticket per fix shape, where the same rule across one module proved by one verify pass is ONE ticket, else per (rule, file).

## DO, in this order
1. PRIOR-WORK CHECK (as Q). Note especially: log-injection alerts may already be covered by RD-618 (b1) / RD-735 / RD-760 / RD-795 (the CSP intake log lines) or by the 30 tickets RD-761..RD-790 Q filed, which are grouped by rule. Map any alert a ticket already covers to that ticket with ONE comment listing the alert numbers.
2. GROUPED tickets for the untracked, priority MEDIUM. For the 72 js/log-injection alerts, group by the LOGGING SITE PATTERN (one shared logger helper, or one module's error paths), not one ticket per line. One ticket when one change and one verify pass prove the group.
3. The 5 GitHub Actions alerts (.github/workflows) are ticketed like the rest. Changing a workflow file is NOT this seat's work, and the ticket says it needs its own review.
4. Never dismiss, reopen or alter any alert. Do not re-prioritise, transition or reassign existing tickets.

## DELIVERABLE
- `<NexusAI>/evidence-s<N>s-codeql-medium-census/census.csv` (one row per medium alert, Q's columns) + `summary.md` (FOUND / TESTED / HOW, with the controls).
- REPORT mail `[Datasec/NexusAI-S -> Tuesday] REPORT: CodeQL medium census`. BLUF shape: *"103 medium at <sha>: covered by existing tickets <n> · newly filed <n> in <g> grouped tickets (keys) · none dismissed."* Every number counted from census.csv in the same action as writing it.
- Then HANDOVER-S<N>S.md, a history entry, and a wrap mail. The seat is retired by hand.

## BOUNDARIES
Read-only on code: read verbs only in 2_Project_Files; no worktree, no jest, no push. No demo, production, Azure, Partner Center or money. No mail to any human. Never delete files. Mail ONE question if a grouping is genuinely ambiguous, and carry on with the rest.

## PLAN CONFIRMATION
Mail `[Datasec/NexusAI-S -> Tuesday] QUESTION: plan confirmation` with your re-fetched count, the main sha and your grouping for the 72 log-injection alerts. Start step 1 without waiting. Include your launcher's preflight warnings verbatim.

RULED BY KAM, NOT YET IN AN ARTEFACT
- The ruling above (the card nexusai-codeql-medium-alerts-ticketing, a) is delivered INTO this brief; its artefact is your census + tickets. The two old paperwork marks (rd104-gh-identity-acceptance-false-premise, t9-nas-leg-direction) do not bear on this work.

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- C-190 + its ADDENDUM (2026-10-05, CLARIFICATIONS:2029): never dismiss alerts; both thresholds block NEW alerts in a PR. These 103 are the pre-existing baseline (created 2026-09-28 18:58-19:01Z) and block nothing.
- Tuesday's grouping ANSWER to Q (2026-10-05T11:28Z): one ticket per rule for test code; one per fix shape for product code.

PROVENANCE:
- 246 open / 103 medium by rule and rule severity, with the controls | the GitHub code-scanning alerts API (state open, ref main, paginated) read by Tuesday with NexusAI's gh identity; the raw file is not durable, so re-fetch it yourself | read 2026-10-06 07:08
- main = 2f0ae4a | git ls-remote origin in /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files | read 2026-10-06 07:08
- Kam's ruling | kam_msgs.sh live read, 2026-10-06T07:07:35+11:00, view=tuesday, in /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/tools/kam_msgs.sh output | read 2026-10-06 07:08
- seat Q's method and tickets RD-761..RD-790 | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/evidence-s88q-codeql-census/ (census.csv checked by Tuesday against Tuesday's own fetch: 143/143) | read 2026-10-05
Self-check note: re-read whole; fixed a pronoun and an unclear aside; the S seat is new, so Q mails are explicitly a template only.
SELF-CHECK: re-read end-to-end for contradictions | 2026-10-06 07:09
