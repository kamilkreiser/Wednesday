From Tuesday (Kam's Datasec coordinator seat). Datasec / MPS Commercial Calculator. Questions to tuesday-agent@agentmail.to; your STATUS file is the wrap.
# BRIEF B108 · LANE C1: Access & roles — build the tickets from Paul's 16 Oct review

**BLUF.** Kam's instruction (live board, ~12:0x AEDT 2026-10-16): tickets for everything from his MPS review with Paul, and agents to action them. Seat B99 filed the tickets and proposed file-disjoint lanes; you are lane **C1**. Work your tickets in order, ONE BRANCH AND ONE READY LINE PER TICKET. Report in `1_Project_Definition/Briefs/2026-10-16_B108_STATUS.md`.
**Step 0:** copy this file unchanged into your `1_Project_Definition/Briefs/` (sha256 both equal; this copy is in Tuesday's tree, read-only to you).

## YOUR LANE (source: `1_Project_Definition/Briefs/2026-10-16_B99_STATUS.md`, section "DO 5 · LANES", and the register `1_Project_Definition/Registers/2026-10-16_paul-review-items.md`; read both before you start)
- **Tickets, in order:** T01 (-136) → T02 (-137) → BL-27 (-188)
- **Files you own (touch nothing else):** `src/MpsCalc.Api/Infrastructure/{CallerResolver,AuthStartup,DevStubAuth}.cs`, `web/src/auth/**`, `web/src/api/personas.ts`, `web/src/app/session.ts`, `web/src/components/Shell.tsx`, `scripts/entra_apps.py`
- **Tier:** 1. Tier 1 = anything that changes a calculated figure or a price (B99 marks T07/T12/T15/T16/T20/T23/T24/T25 tier 1): a calculation-register row (find the register the project's CLAUDE.md / CLARIFICATIONS name; UNMEASURED by Tuesday; if you cannot find one, STOPPED) and a test that is RED at base before the change. Tier 1 work goes to the QA gate before merge; Tuesday commissions it.
- **Kam's cards** (posted 12:5x, open): roles (K-01/K-18), words (K-02/K-03/K-14/K-20), catalogue (K-05/K-06/K-07/K-10/K-13/K-16), pricing (K-09/K-11/K-12), data asks (K-04/K-08/K-21), scope (K-15/K-17/K-19). Build on the card's stated DEFAULT unless a ticket says WAITS/SKIP. Tuesday mails you if Kam rules differently. New screen words are shown to Kam at the gate before any deploy: list every new or changed user-facing sentence in your STATUS.
- **Other lanes run at the same time** on the same repo (A, B, C1, C2, D, E, F, G, H, J). Never edit a file outside your list. If you need a change in another lane's file (especially lane D's contract files: `Dtos.cs`, `openapi.json`, `docs/API.md`, `web/src/api/generated/**`), write `NEEDS LANE <x>: <what>` in your STATUS and move to your next ticket.

## KAM'S RULING FOR THIS LANE
Kam, live board 13:05:46 AEDT 2026-10-16, card mps-paul-review-roles-k01-k18-1016 = a: "All roles + owner self-approval, audited; accept cost-plus visibility". So: every user gets all four roles through an Entra group assignment (NO code bypass); a quote's owner may approve their own quote, and the approval writes an audit line naming that it was a self-approval; BL-27 (K-18) is accepted for release 1 (record it, no code). **Any actual Entra change (group, app role assignment, `scripts/entra_apps.py` run against the tenant) is Kam's to approve: build and test the script and code, write the exact change in STATUS under FOR KAM, run nothing against Entra.** C-12 (a second account approves) is superseded for owner self-approval by this ruling: add a CLARIFICATIONS-ready paragraph in your STATUS quoting the ruling; Tuesday records it.

## DO (per ticket)
1. Read `CLAUDE.md`, `CLARIFICATIONS.md` (C-01…C-32), the ticket in Jira (MPSCALC, read-only except a comment) and its register row. Worktree under `2_Project_Files/.tools/wt-b108-<ticket>` from origin main (re-read main by `git --no-optional-locks ls-remote`; the root checkout is read-only verbs only).
2. Branch `b108/mpscalc-<n>-<short>` from main (stack on your own previous branch only when the ticket needs it, and say so). Red first where behaviour changes. Smallest change that meets the ticket's acceptance.
3. Checks: the CI's own lines from `.github/workflows/` (dotnet build -c Release 0 warnings + tests; web lint, test, build; python), no lost test names vs base, diff inside your file list (prove with a planted path your check catches, once per session), gitleaks over the range.
4. Push the branch only. Append to STATUS: `READY FOR REVIEW: <branch> @ <sha from ls-remote> (MPSCALC-<n>, tier <t>)` with a 3-line BLUF above it. One Jira comment on the ticket naming the branch and sha (read it back). No transitions.
5. Next ticket. A ticket that WAITS on a card or another lane: one STATUS line saying what it waits on, then skip it.
6. At ~70% of your context, or when your list is done or all waiting: finish the ticket in hand, write a HANDOVER section (what is done, what waits, where), last line `DONE: B108 lane C1 (<n> ready, <m> waiting)`.

## HOLDS
Tuesday opens every PR and merges after CodeQL (all three languages, C-08/C-11) and checks are green, and after the QA gate for tier 1. Never push main; never force-push; never dismiss an alert or bypass a check; no deploy (MPS hosted is card-per-deploy); no Entra or Azure change; nothing to Paul or any human; never delete (quarantine); secrets by name only from `4_Credentials/.env`. If anything here disagrees with what you measure, act on the measurement only inside these holds and say so; otherwise `STOPPED: NEEDS TUESDAY` + ONE question as the last line.

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-16 12:54
