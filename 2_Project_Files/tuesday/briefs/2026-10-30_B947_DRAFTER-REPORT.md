# B947 drafter report (gate kit for PR #252, partner home), 2026-10-30 ~15:45

Kit: 2026-10-30_B947_SEAT-G222_hpsmpoc-252-partner-home-gate-tier2.md (67 lines, 0 non-ASCII bytes, 8 lines with the four-underscore pattern: S1-S7 plus the last line, checked with python3 -I).

Measured by the drafter (gh api -X GET, tarball of main 571fc9d9 in scratch, lsof read-only, 15:33-15:40):
- PR #252 open, head a3e01c83, base.sha 7365165d (stale), 3 files +414 -39, 5 commits; main 571fc9d9; branch 2 behind, 12 files of #246/#247 disjoint from the 3.
- refs/pull/252/merge = 479a7a37 with parents b5b6aa34 + a3e01c83: stale (not recomputed against #247).
- Checks at 15:33: 18 runs, 14 complete/success incl. CodeQL and all four Analyze; in progress: journey-and-prototype e2e, api, two SQL Server.
- Ports 9780-9789 free (9700-9799 shows only 9734, 9735). Model id claude-sonnet-5-5 at models_latest.json line 23; routing row G2 at fleet/specs/model-routing.md:109 (0_Brain/skills/model-routing.md does not exist).
- Four next-action hrefs (/assessments, /playbook/phase-1, /services, /engagements) each have a page.tsx on main; moduleHref and MockTag exports unchanged on main vs head.

Wrong at source:
1. PR title, PR body and commit cffaf367 say "from 1050 px"; the head splits at xl (1280): PartnerDashboard.tsx:135. Builder STATUS says 1280 (Correction 1), so the STATUS is right and the PR text is wrong. Tile grid also moved xl -> 2xl (lines 100-103): not in the PR body.
2. Builder STATUS FOR TUESDAY 145 proposes a body saying 1280; the corrected PR body lost that and the "Known: a11y journey timeout" caveat.
3. Builder says plants 9 of 9 and e2e on pre-merge sources; unit 3261 is on 7365165d, not on 571fc9d9.
4. Words in none of the three sources (drafter grep of main): "Open your customers", "Customer pipeline table" (aria), the table caption. "the review guide" is kit-allowed but has 0 referent hits in the app.

Q-questions (defaults, for the S3 slot):
- Q-1 Landing tree = merge onto the main read at Step 0, one allowed re-fetch of main if it moves (the B940 C-1 fix). Default YES.
- Q-2 1280 vs ticket 1050: Minor/Note, not NO GO (Tuesday's own stamp allowed the D-4 fallback); PR title/body/squash must say 1280; product owner told. Default as written.
- Q-3 Pipeline table vs "Customers by stage" bars disagree on the mock (builder, not forced): Note if prototype override and same at main elsewhere; Major if both read the service. Default as written.
- Q-4 New accessible names and "review guide": Minor, listed for the product owner's veto; Major only if it reads as an HP document. Default as written.
- Q-5 NO GO parks the PR at round 1 of 2; Tuesday writes a round-2 fix kit.

Recommended stamp defaults: S1 STAMPED <time> AEDT 2026-10-30 by Tuesday, Q-1..Q-5 accepted as defaults; S2 until 19:00, launch_when_cool load1 below 7 on two reads, one waiter (load1 was 10.67 at 15:35, so expect a wait); S4 YES to every item named; S5 target 120, hard stop 180 minutes after Step 0; S6 read live at the stamp (main may have moved); S7 model: claude-sonnet-5-5 -- G2 -- gauge <n>% -- load1 <n>.

Reasons not to launch now: none blocking. Load is high (10-13), and 4 CI jobs are still running (the gate polls to the end). If main moves before launch, the kit's REFUSE list says what stops and what only re-pins.
