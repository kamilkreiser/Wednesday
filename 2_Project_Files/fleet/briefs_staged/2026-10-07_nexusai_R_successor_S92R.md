# BLUF — SUCCESSOR SEAT Datasec/NexusAI-R (lane R): (1) RD-761 FIX ROUND per Tuesday's 23:03Z ANSWER (GUID check at the sink, re-PR; CodeQL is the verdict); (2) RD-794 @ cd171f9 and RD-819 @ fdd07af: re-file hold 13, then send the two updated READY FOR QA mails (they are GATE BATCH 19 members); (3) RD-807 is already in gate 19, nothing owed. Send a PLAN CONFIRMATION to Tuesday before any product edit or lock ticket.

**Addressed to the cockpit seat `Datasec/NexusAI-R` ONLY.** `Datasec/NexusAI-M`, `-N`, `-O` and `-P` are live and share this inbox (datasec-nexusai@). A mail addressed to another seat is not yours, and that includes "M and R" style joint mails only where R is named. Establish your seat from your own pane's cockpit name (`tmux display -p '#{@cockpit_name}'`), your launcher and your process tree, never from which thread looks familiar. Number your session from the highest HANDOVER-S* on disk (S91P was the highest at 10:0x AEDT): you are **S92R** unless a newer one appears.

## READ FIRST, in this order (all in the NexusAI folder)
1. `HANDOVER-S89R.md` WHOLE — your predecessor wrote it for you (updated ~10:02 AEDT). Its section 1 "remaining steps" apply only AFTER the fix round below.
2. Tuesday's two mails of 2026-10-06T23:03Z and 22:52Z on this inbox: "ANSWER: RD-761 CodeQL — (a) GUID check at the sink, fix round, tier 2 into gate 19; turn passes to O" (read it WHOLE: it is the ruling for item 1) and the 22:52Z "RD-761 merge check received" ANSWER.
3. `1_Project_Definition/CLARIFICATIONS.md` by C-number (line numbers are Tuesday's grep at 10:0x, find each by its number): C-203 + addenda (:2191, RD-761's design and RD-794/RD-819 rulings), C-199 (:2152, stacking rules, applied to RD-819 on RD-794), C-190 (:2056, CodeQL ruleset, BOTH thresholds), C-185 (:1969, the CI known-failing set and the local re-run rule), C-186 (:2003, merge turns), C-141 + addenda (:1505, the jest queue; ADDENDUM 7: only a merge ticket's tag contains the word "merge").

## MEASURED BY TUESDAY (2026-10-07 ~10:0x AEDT)
- main = 8853e36 (ls-remote). O holds the merge turn now (RD-736, ticket s87o-merge-rd736 first in the jest queue).
- Branch heads at origin (ls-remote): rd-761-law-endpoint-policy-s89r = 72ca5d3 (= refs/pull/58/head); rd-794-ollama-runtime-slice-s89r = cd171f9; rd-819-ai-config-empty-body-s89r = fdd07af; rd-807-incidents-prototype-key-s89r = 9b15a99.
- PR #58 code-scanning on refs/pull/58/head (gh api, NexusAI's gh config): #256 + #257 js/request-forgery CRITICAL and #258 + #259 js/file-access-to-http MEDIUM at backend/azureLogAnalytics.js:335 and :360. git show 72ca5d3: line 334 builds `${apiBase}/workspaces/${this.workspaceId}/metadata`, so the host is constant and the path carries workspaceId.
- Hold 13 (s89r-rd819-hold13-proof) DID NOT RUN. Its waiter died when Tuesday closed S89R's pane at ~10:0x (it had been a child of that session), and its ticket left the queue cleanly (Tuesday read queue-jest/). session-tools/s89r/hold-13.log holds only waiting lines. **Re-file it under your own seat tag**, with run_in_background (never &). Its expected result is in HANDOVER-S89R.md section 2.

## AUTHORITY
- The open-ended NexusAI grant "work through the tickets and merge once tested" (Kam, 2026-09-25, re-affirmed 2026-09-27), on Tuesday's GO after a QA gate verdict at the head. RD-761 does NOT merge until its fix round has passed gate batch 19 AND Tuesday sends a TURN mail naming it.
- No CodeQL alert is ever dismissed (dismissal is Kam's alone; the Datasec rule is fix in code).

## WORK, in order
1. **RD-761 fix round**, exactly as the 23:03Z ANSWER rules: an anchored GUID test on workspaceId at the sink (every URL builder in that file that interpolates it, and the query POST if it shares the shape), refused BEFORE any URL is built or any token is fetched, with the named refusal RD-761 already uses, then encodeURIComponent. Cells red first at 72ca5d3 (0 token requests, 0 HTTP requests for a non-GUID; a valid GUID still reaches the constant host as the control). Proof: the cells, RD-761's suites by name, full verify, C-57. Push and let PR #58 re-run: #256-#259 gone, nothing new at either C-190 threshold. If they are not cleared, STOP and mail Tuesday with the run id. Then READY FOR QA, tier 2 through code, naming the new head and the CodeQL run id.
2. **Hold 13**, re-filed (see MEASURED). Then the two updated READY FOR QA mails: RD-794 @ cd171f9; RD-819 @ fdd07af, stacked, gate range cd171f9..fdd07af. Each carries PRIOR WORK, NOT TESTED, the drafter findings F1-F4 and how each was measured, the W5d note, and C-133's 9-id accounting.
3. RD-794/RD-819/RD-761 are partitioned from O (feedback.js, provisioning), N (dataErasure.js), M (CSP/health/server.js budget-log region) and P (static/vendor, login, server.js:2601). Your server.js edits must stay in RD-794's named regions (:19117, :19161 and the ai-config branch); anything else in server.js goes to Tuesday first.

## RULED BY KAM, NOT YET IN AN ARTEFACT (decision_queue.sh list ruled --undelivered, filtered to NexusAI, read 10:0x AEDT)
- `rd104-gh-identity-acceptance-false-premise` (ruled `youcheck`, 2026-09-07) and `t9-nas-leg-direction` (ruled `a`, 2026-09-21): neither is lane R's; no action. Unverified by Tuesday whether either already sits in an artefact.

## RULED BY TUESDAY FOR THIS PROJECT, STILL OPERATIVE
- RD-761 (a) fix round, tier 2 into gate 19 (2026-10-06T23:03Z ANSWER).
- RD-827: any tree at or after 90b2556 gets its OWN install before any hold (print the resolved proxy-addr path + version). The shared C-57 tool's "failed 3" is that tool's 2.0.7 install (RD-827 c39165); its id-superset verdict is the property.
- C-186: merge turns are given by Tuesday's TURN mail only.

## STANDING LINES
- PRIOR-WORK CHECK: before rebuilding, replacing, removing or redesigning anything, look first (git log -S/--follow/blame, CLARIFICATIONS, history, handovers, tickets), write down what existed and why with its source; every READY FOR QA carries a PRIOR WORK section (or "nothing replaced").
- CodeQL: never push an unscanned commit to main; never bypass; never dismiss an alert.
- Never delete: quarantine/move. Never edit a script while a copy of it runs. Never kill by pattern (C-174).
- Every factual sentence in a mail names its instrument, or says "unmeasured". Read the inbox by ADDRESSEE, never by sender prefix (S89R's own lesson).
- Context: write the handover when your pane first shows less than 10% before auto-compact, not at 1%.

PROVENANCE:
- main 8853e36; rd-761 72ca5d3 = refs/pull/58/head; rd-794 cd171f9; rd-819 fdd07af; rd-807 9b15a99 | git ls-remote origin on your own 2_Project_Files | read 2026-10-07
- CodeQL #256-#259 at azureLogAnalytics.js:335/:360 | gh api repos/datasecau/Reporting_Dashboard_Au/code-scanning/alerts?ref=refs/pull/58/head (your own 4_Credentials/.gh-config) | read 2026-10-07
- workspaceId in the metadata URL path | git show 72ca5d3:backend/azureLogAnalytics.js lines 330-336 in your own 2_Project_Files | read 2026-10-07
- hold 13 waiter gone, ticket gone | ps for pids 21892/21894 (absent) + ls of your own session-tools/locks/queue-jest/ (4 tickets, none s89r) | read 2026-10-07
- lane R state | NexusAI/HANDOVER-S89R.md sections 1-3 | read 2026-10-07
- C-numbers and line positions | grep of 1_Project_Definition/CLARIFICATIONS.md for C-141/185/186/190/199/203 | read 2026-10-07
- undelivered NexusAI cards | /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/tools/decision_queue.sh list ruled --undelivered (Tuesday's tree) | read 2026-10-07
- highest HANDOVER is S91P | ls NexusAI/HANDOVER-S* | read 2026-10-07

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-07 10:07 (fixed: the ANSWER times read 23:03Z and 22:52Z consistently)

## PLAN CONFIRMATION
Mail `[Datasec/NexusAI-R -> Tuesday] QUESTION: plan confirmation` with your seat identity facts (pane id, cockpit name, claude pid), what you read, your GUID-check plan for RD-761 (which functions, which helper if any), your hold-13 re-file plan, and any launcher preflight warnings VERBATIM. Then work; your wake is Tuesday's mail plus a tap.
-- Tuesday
