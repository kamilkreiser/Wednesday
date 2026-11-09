# Gate 292, TIER 1 (Opus): PR 2138 (Refs KS-590, all four anonymous-verify disclosure gaps + the v2 chain-only twin + a docs correction), Seat G 32nd. Commissioned 2026-11-09 20:0x by the 18:46 Wednesday seat. Security surface (tenant disclosure on anonymous verify): FULL tier-1 depth.

Common rules: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-07_gate_tier1_common.md, read whole and applied at full tier-1 depth.

Pins (Wednesday's ls-remote at 20:08:53 AEDT; RE-READ them at start and end, and say whether each moved):
- develop 1b3a3ec34a5bb4df13a4cea9ae7b03b7a87a172a (the PR was built on f98afb113c2d; the move between them is PR 2115, one api-gateway test file: confirm it shares no path)
- PR 2138 head d769c05d0a9b4e47413ed7ec9d02024b3180edc0
- READY (read whole): /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-09_seatG-32nd/mail/out_02_ready_full.md. Evidence: the same seat folder's evidence/ and drafts/predictions.md. Reproduce; do not trust.

The ruling and the scope (read whole):
- Kam's card secuura-backlog-31-decisions-1109 = a (13:44), pack row 16 option 1, 'withhold all four': /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_secuura-backlog-decisions/decisions.md lines 161-172.
- The seat's brief: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-09_seatG32_build.md. Wednesday's plan answer: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-09_G32_answer_plan.md. That answer brought verificationV2.ts chainOnlyMatch and docs/VERIFICATION.md:50-70 into scope, and accepted the seat's rulings on the ks563 and ks1939 C2 cells.

Questions:
1. EACH GAP CLOSED, on every route: for gaps 1 to 4 and the v2 chain-only twin, show the code at the head that withholds the field, and an anonymous or cross-tenant request (in-process) that got the field on develop and does not get it at the head. Are there OTHER routes or response builders that still return title, issuer, certifiedBy, certifierOrganizationId, organization_name or onChainMetadata tenant fields to an anonymous or cross-tenant caller? Enumerate the response builders in originate's verify paths (v1 and v2) and say for each whether it is scrubbed. A positive control must sit beside every zero.
2. OVER-WITHHOLDING (the seat asks you to look here first): gap 2 is scoped UNCONDITIONALLY, with onChainMetadata withheld whole. Does a SAME-tenant, authenticated caller still get everything it got before, on every route? Name every field that a legitimate same-tenant caller loses, if any; that would be a finding. Also check that verified, integrity, anchor facts, isCertified and existence answers are unchanged for every caller.
3. Gap 3 relies on the 039 RLS migration (the seat's words): what exactly does the change assume RLS does? Is it true at develop (read the migration)? Does the code withhold the fields even where RLS would not apply, or does it trust RLS to do so?
4. Gap 4 is a SELECT fix: is tenant_id now selected on EVERY by-id path, and does isCrossTenantResponse then scope it? Show it with a cell.
5. Red-first and mutants: reproduce 16 of 23 red on develop and 23 of 23 at the head; the seat's 10 mutants; ONE mutant of your own per gap that reddens a named cell. Are any cells PINS (green on develop by design)? Are they labelled honestly?
6. The three CHANGED existing cells (ks584 legacy, ks563, ks1939 C2): does each change only the assertion the ruling withdraws, and keep the rest? Read each diff hunk.
7. The whole originate suite (the seat: 2,592 -> 2,615, 0 common changes), tsc (4 = 4) and eslint, compared with develop.
8. The DB-gated integration suites were NOT run by the seat. The seat names the KS 1114 T9 golden (R 84th's PG recipe) as the one to measure. Find the recipe in the R 84th record. If it runs WITHOUT docker or any box (a local postgres process in your own clone is fine), run that golden at develop and at the head and report it. If it needs docker or a box, say UNMEASURED and name what would measure it.
9. docs/VERIFICATION.md:50-70: does it now say what the code does? Is that the only doc change?
10. Merge tree onto develop 1b3a3ec34a5b. Name any open PR that shares a path, with a planted control (the seat reports 0 of 60). Does PR 2131 (row 7o, vc-issuer and secuura-api.yaml) or any queued PR touch the same files?
11. The PR body and KS-590 comment 845cb0df claim no more than the change. Does the body state the behaviour change plainly? (Titles and fields of untenanted rows disappear for anonymous and cross-tenant callers; whether kintsugi or demo holds such rows is UNMEASURED.)

Constraints: clone under /private/tmp/g292 (no rm; state its size at the end). Never cd. In any /Volumes/DevMASTER/!CODING checkout use only ls-remote, show, log, diff, ls-tree, cat-file and grep: never fetch or any git write verb there. Never push. Never run the hook against the real remote. No real .env or credential file (fixtures only). No docker, no box, no kintsugi, no demo. Keep load1 under 8. Read df for DevMASTER at start and end.

Output: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_gate292-tier1-pr2138-ks590/verdict.md (if your Write is refused, put the whole verdict in your final message). Line 1 exactly: 'PR 2138: <V>', with V one of GO | GO WITH NOTES | NO GO. Then FOUND / TESTED / HOW (instrument, controls), NOT TESTED, and findings with ids G292-<n>, each with a severity. Findings only; post nothing; mail nothing.
