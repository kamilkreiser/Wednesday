# B474 drafter report (sub-agent for Tuesday, read-only, 2026-10-22 18:54-19:02 AEDT)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-22_B474_SEAT-G41_hpsmpoc-b465-words-gate-tier2.md` (44 lines, unstamped, no READ-WHOLE last line; Tuesday fills the Stamp and appends it). Shape cloned from the B468 kit (tier-2 gate): header, change/claims, fact marks, REFUSE, Stamp, Model/escalation/ports/Step 0/Launch/Report, HOLD + standing, CHECKS, SEVERITY/VERDICT with the two final-line formats, NOT TESTED BY DESIGN. Eight checks (B468 had seven): 1 delta, 2 the words byte for byte, 3 prior work/Jira, 4 red-first + 14 gate mutants, 5 suites incl. merge with current main, 6 real browser + 5 e2e specs, 7 B461 sequencing + the card facts, 8 merge/overlap/secrets/CI.

## Slot count of the kit (with control)
- `/usr/bin/grep -c -E '_''_''_''_' <kit>` = **5** (lines 15-19: Stamp time, Launch authority, Heads at stamp, Model receipt, Hard stop). Control: a scratch file `a____b` reads 1.
- `/usr/bin/grep -o -E '@[A-Z_]+@' <kit> | wc -l` = **0**. Control: scratch `a@BC@d` reads 1.
- No person's name in the kit (case-insensitive grep for the three name tokens = 0).

## Measured (how)
- `ls-remote origin` 18:54:58: main `d70f9dc1` (moved from `a93b926a` by #181 `4695d7f`, 3 paths, and #182 `d70f9dc`, `Hpsmpoc290Tests.cs`); `b465/hpsmpoc-148-310-words` = `c65a5ab6` (matches READY); `b461/…` `52bd6e7c`; `b429/telemetry-224` `4c02e8b9` (moved since B468); `b462/hpsmpoc-308-sqlserver-shard` `e8ecb8ae` (now exists; B468 saw it absent); `b467/…` `3b2a8240`; no `b466*`; no `b474*`.
- `gh api compare/main...b465/…`: diverged, ahead 6, behind 2, 19 files (18 modified, 1 added), merge base `a93b926a`. The head object is in the shared repo; `d70f9dc` is not (no fetch allowed for me), so ahead/behind against it is from GitHub, not local git.
- Diff of the 7 source files read whole (`git diff -U1`): each ruled string matches the pack text; `timeZoneName: "short"` is the one dates option; the 401 sentence is in `clientFailure` only; `followUpFailure` untouched.
- Pack strings: each of the 148 title, 6a, 7a, 8a and the two time examples appears exactly once in the pack file; head counts per source file are 1 for each anchor; old strings (`coming later`, old 8a body as on-screen text) 0. A non-ASCII check of the added lines was attempted and FAILED (BSD grep has no `-P`), so it is left to the gate (the kit says `LC_ALL=C grep -E`).
- Overlap (compare lists, 19 paths vs each): b429 (43 files, control `web/src/instrumentation.ts` present) 0, b459 (2) 0, b460 (1) 0, b461 (14) 0, b462 (6) 0, b467 (2) 0. check-runs total 0, open PRs 0, required contexts printed (5).
- B461 sequencing: `playbook-action-plan-live-api.spec.ts` :155 `h1(page, "Partner Dashboard")`, :173 and :251 `The plan was discarded` identical at main `a93b926` and b461 head `52bd6e7c`; b461's only change to the file is line 6 (a comment). Head still has `Partner Dashboard` in 3 lines (the spec :155 and two lines of the new `PartnerDashboard.test.tsx` row).
- Test rows per file base -> head: dates 2->7, ActionPlanScreen 14->15, api.failure 0->3, ClientFollowUpScreen 18->20, PartnerDashboard 7->8, PhaseFlow 8->9, CustomerShell.notfound 1->1; 13 added + 1 rename = builder's "lost 1, added 14".
- Time-formatting call sites: `dates.ts` is the only `toLocaleTimeString`; `SendFollowUp.tsx:88` is a date-only call (no zone).
- Ports: `lsof` for 8250-8259 rc 1 (0 listeners); no brief names 8250-8259 (8210-8219 B468, 8220-8229 B469, 8230-8239 B471, 8240-8249 B472). No brief uses pane `G41`.
- Environment: `.tools/ms-playwright` (project root) holds chromium-1243, headless shell and ffmpeg; `.tools/node24` is v24.21.0, machine node v26.8.1; `.tools/dotnet` exists but no API is needed (mock BFF). `playwright.config.ts` starts THREE servers per non-live run (web, entra stub, hosted `server.js`), honouring `WEB_PORT`, `E2E_STUB_PORT`, `E2E_HOSTED_PORT`: the kit assigns trios 8250-8252 (head) and 8253-8255 (base), 8256 for hand-driven screens. Load1 11.4 at 18:55.

## Corrections to the prompt / builder (the kit carries them)
1. Builder says Playwright Chromium "not installed": it exists project-locally in `.tools/ms-playwright` (only the home cache is empty). So the five edited e2e specs, which the builder never ran, are in scope for the gate (Check 6), not NOT RUN by default.
2. Builder's "Partner Dashboard prints ONE line" became three (two lines of its own required unit row); the gate's sequencing fact stays `:155` only.
3. Main moved twice since the builder's base (builder saw only #181): now `d70f9dc`; the kit has the gate build `-merged` on current main.
4. The B465 brief's pane is `W1`; the gate pane `G41` is free.
5. Word pack 5a premise "our own text is already -ise" is false for `phase-flow.ts` (builder found this; the kit makes the gate verify the Jira 310 comment does not repeat it).
6. The gate's anchor `e.status === 401) return "Open the link your partner sent you.` was chosen as a prefix so it stays count 1 despite the long string.

## Beyond the prompt (flag if unwanted)
- Check 7(2) goes further than "measure GMT offsets": it also asks WHERE the zone comes from (server render vs reader). The builder measured Chrome only with system zone = Sydney, which would hide a server-zone string or a hydration mismatch. I made that a Blocker-class fact to report, still ruling nothing.
- Check 7(3) asks for a scratch (never committed) vitest probe of whether the notice button can ever render.
- Check 2 compares the builder's BRIEF text against the pack too (the brief told the builder to copy from the brief, not the pack).
- Check 3 reads the builder's two Jira comments (ids 39890, 39891) for a false premise and for names/secrets.
- Check 5 has the gate run `signin-budget.test.ts` alone against base and head (builder's one timeout), as a Note unless reproduced.
- 14 gate mutants (W1-W4, D1-D3, H1, P1, C1-C4, K8), with W4 flagged a probable survivor (button condition).

## UNMEASURED
- Nothing was run: no test, build, browser, server, merge-tree (main's `d70f9dc` is not in the local repo and fetch is forbidden), gitleaks.
- The non-ASCII byte check of the added lines; whether the 12-red-of-100 count reproduces; whether the three Playwright-versus-chromium-1243 versions match.
- Whether a screen shows the time server-rendered (zone from the server) or client-only; whether the 148 scenario is reachable through the mock's UI.
- The Jira comments' text and the issues' Done-when (not read; the gate reads them).
- Which mutants are survivors (predictions only: W4 likely; the literal 6a row is believed present).
- The mapping of ports 8220-8249 to seats is from brief text, not from `lsof`.
