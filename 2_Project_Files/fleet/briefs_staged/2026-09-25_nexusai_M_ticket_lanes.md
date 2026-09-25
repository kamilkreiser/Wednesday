# BLUF — NEW SEAT Datasec/NexusAI-M: work through the NexusAI board. FIRST deliverable is a LANE PLAN (which open tickets agents can do now, split into lanes that never touch the same files); then YOU take lane 1 and build it to READY FOR QA. Tuesday launches the other lanes from your plan. Nothing merges without a QA gate verdict at its head and Tuesday's GO.

**Addressed to the cockpit seat `Datasec/NexusAI-M` only.** `Datasec/NexusAI-L` is ALSO live and shares this inbox: it is finishing the RD-665 fix-only port to main (C-162) and holds the customer-test environment in 73e9b141. A mail addressed to NexusAI-L is not yours. Establish which seat you are from your own pane/launcher, never from which thread looks familiar.

## AUTHORITY
- Kam, Tuesday's terminal, 2026-09-25 ~22:0x AEST, right after `/login` (new Claude account), verbatim: *"New account logged in, so you should have plenty of Azure credits. Please work your way through the tickets and merge once tested."*
- Recorded in Tuesday's EXPIRING-GRANTS: merges to main on Tuesday's GO after a QA gate at the head + full verify, one at a time. Tuesday relays the GO; you never self-merge without it.

## HARD BOUNDARIES
- **Main is moving tonight:** L is porting the RD-665 fix (webtest ping->standard) onto main. Read `git ls-remote origin refs/heads/main` before branching and again before any push; branch from the CURRENT main.
- **No demo redeploy, no production, no Partner Center, no money, no mail to any human.** A merge must not deploy: check the deploy-demo.yml guard each time.
- **The customer-test environment (73e9b141, tenant ec01829b, `4_Credentials/.azure-customer-test`) is L's. Do not touch it.** Friday's HPSM-POC (a6b8fe11) is never touched by anyone.
- **Tickets that need Kam or a client human** (RD-536 is Kam's own list; anything shaped "decide whether") are NOT lane work: list them separately with the one-line reason.
- Your repo rules stand: C-68 (never rebase a gated commit), C-57/C-89 (counts regenerated, never hand-edited), the jest lock for every run (`session-tools/nexusai-lock.sh`), SESSION_SECRET unset for verify.

## DELIVERABLE 1 — THE LANE PLAN (mail it within your first hour; ~1 page)
1. **Sweep the RD board** (To Do + In Progress + Testing; the whole set, paginated, with the count and its predicate stated). For each candidate: agent-actionable now? (no human input, no Kam ruling, not blocked).
2. **Priority:** Highest first, then High. Named by Tuesday as likely early items, VERIFY each at source before listing: RD-508 (an AI response that sends headers then stalls hangs every AI status check), RD-460 (package "not self-contained: customers need a Datasec-issued ACR token" — today's customer test in 73e9b141 pulled the release image ANONYMOUSLY, C-161/run 3; it may be closable with that evidence, but check what the ticket actually claims first), RD-664 (GPT-4.1 GlobalStandard quota 0 in the customer sub). The 117 Release Ready tickets: say whether any are fixed on a branch but NOT on main (merge candidates for Tuesday) vs already on main.
3. **Lanes:** 2-4 lanes, each = an ordered ticket list + the DIRECTORIES/FILES it touches. Two lanes may never share a file. Name the foreseeable collisions (the counts file is shared by every lane: say how you propose to handle it, e.g. regenerate at merge time).
4. **Per lane:** the QA tier each ticket needs (tier 1 security/auth/data/deploy; tier 2 tests/docs/config).
5. PRIOR-WORK CHECK standing line: before rebuilding, replacing or removing anything, look at what exists and why (git log -S/--follow, CLARIFICATIONS, history, tickets); write it down; keep what works.

## THEN — LANE 1 IS YOURS
Take lane 1's first ticket, branch from current main, build, red-proof (the new cell red before the fix, green after, a control), full verify, push the branch, READY FOR QA to tuesday-agent@ (branch + head sha, sets not counts, PRIOR WORK section, what was NOT tested). Continue down lane 1 while the gate runs; one branch per ticket.

## PLAN CONFIRMATION
Mail `[Datasec/NexusAI-M -> Tuesday] QUESTION: plan confirmation` and start the read-only sweep without waiting.

PROVENANCE:
- Kam's words | Tuesday's terminal after /login | read 2026-09-25 ~22:0x
- board shape (568 not Done: 288 To Do, 19 In Progress, 136 Testing, 117 Release Ready, 6 On Hold, 2 Declined) | Tuesday's paginated Jira read 21:2x AEST (statusCategory != Done) | read 2026-09-25
- RD-665 fix-only port to main by L | L's SCOPE+METHOD mail 11:57Z, C-162 | read 2026-09-25
- main 0677388 carries the ping webtest | Tuesday's git show 0677388:azure-marketplace/combined/mainTemplate.json in YOUR repo /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files | read 2026-09-25
Self-check note: re-read whole; merges only on a gate verdict at the head plus Tuesday's GO; lanes never share a file; L's environment and HPSM-POC are out of scope.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-25 22:03
