# B347 drafter report (Tuesday, Datasec / MPS Commercial Calculator), 2026-10-20 21:41-21:55 AEDT

## BLUF
Wrote the tier-2 gate brief for PR #89 (b311/v2-home @ 0d7250e on main 67bf200): `2026-10-20_B347_SEAT-G25_mps-gate-pr89-tier2.md` (105 lines, B325's shape). Its centre is an independent staff-figure leak test (list JSON on both hosts, CSV bytes from a real browser download, DOM) with a positive control, plus figures byte-equality, the membership matrix, CSV neutralisation, the V0Home pin flip, 9 mutants, counts, NEW WORDS, CI/CodeQL and the merge prediction. Model: Sonnet 5.5, row G2, `claude-sonnet-5-5`, launch `BRIEF_SEAT_LEVEL=sonnet`. Port block 7510-7519 (web 7511, API 7512). Stamp slots: only `@@MAIN_SHA@@` and `@@STAMP_TIME@@`, once each. Not launchable as a GO yet: **CodeQL has not started on the draft head**, and the brief says wait or ask.

## MEASURED (21:41 AEDT, read verbs / gh GET)
- `ls-remote`: `b311/v2-home` = 0d7250e2...; main = 67bf2004...; `b311*` 1, `b345*` 0 (B345 has not pushed); `refs/pull/89/head` did NOT appear in my ls-remote output although I asked for it (PR GET gives the same head); the brief tells the gate to say which source it used.
- PR #89: open, draft true, 3 commits, 13 files, +1011/-28, mergeable true, state blocked, base = main 67bf200. File list and per-file +/- recorded in the brief.
- Check-runs on head: only `web`, `dotnet`, `python`, all `in_progress` since 10:40:16Z; no CodeQL/Analyze run; analyses 0; open alerts 0; ruleset 24139430 active.
- uptime load 5.74 6.22 6.69; `heavy-slot-1` exists (holder not read); `.tools/b345`, `wt-b345-*`, `b340` exist.
- Ports: 7510-7519 and 7520-7529 lsof-free; no 2026-10-2x brief names 7510 (7520-7579 are named, so I avoided 7520). Avoided 7400-7449, 7640-7649, 7700-7709.
- Model: `models_latest.json` sonnet = `claude-sonnet-5-5`, checked 2026-10-20 20:55 +1100, warnings and stale_pins empty. `brief_seat.sh:24` defaults to opus.
- Head code (saved in the scratchpad, read): `QuoteEndpoints.cs:671-676` is the only `ToSummary` call and applies `Mapping.Restrict` for non-internal callers; `Mapping.cs:258-262` Restrict nulls the four fields; `QuoteFigures.cs` Draft branch now calls `ToDto(c, internalMetrics: caller.SeesInternalMetrics)`; `feedback/csv.ts` `csvCell` neutralises `= + - @ TAB CR`; `stubApi.ts:209` matches `r.group === p.group`; `b46-home.spec.ts:254` still asserts four tabs.

## RELAYED (from builder STATUS/brief, B325 brief, routing file)
Builder numbers (dotnet 1,769 to 1,797; web 94/900 to 98/936; names lost 2 / added 30 dotnet, lost 0 / added 26 vitest; 15 mutants red; gitleaks), the per-mode GP table (most staff cells empty), the 12 NEW WORDS, Jira comments 39795-39797, the disclosed `rm -f` and `git checkout --` and load breach, the scope exception on `QuoteApiTests.V0Home.cs`, FOR TUESDAY items 1-7. Routing row G2 and its security-shaped escalation to G1 (`model-routing.md:109`). B345's brief `:92` (it will not touch `b46-home.spec.ts:254`).

## UNMEASURED
Not read: `docs/API.md`, `ApiJson.cs` (null omission), `QuoteEvents.cs` (type of `IsDraft`), `web/README.md` personas, `isDecimalString`/`roundHalfAwayFromZero`, the new test files, all Jira tickets and comments, node/dotnet versions. Nothing was run, built, fetched or pushed. Whether B345 will push before the gate ends. CI web totals.

## Hazards I put in as named traps (new vs B325)
T-a the Draft branch now builds the DTO with internal metrics for staff callers and `Facts.Of` also feeds `/figures` (differential probe: plain vs staff caller, base vs head). T-b only one `ToSummary` caller (re-measure). T-c key presence, both hosts. T-d browser persona gate vs server grant. T-e Home queue never shows staff columns. T-f stub cannot answer the tab, so Path A proves nothing about it. T-g published contract text still says 400. T-h negative money in the CSV is a bare number by design; judge it. The double gate (fill then strip) means one layer is untestable over HTTP; the gate removes each layer separately and grades an untested layer Minor.

## Questions for Tuesday (each with a recommendation)
1. **Who carries `b46-home.spec.ts:254` (the stale four-tab assertion)?** B311 may not edit e2e, B345 is forbidden to touch it, so nobody owns it. Recommend: add it to B345's phase-2 e2e list only if B345 has not yet passed that file (one-line edit), otherwise a small follow-up card after #89 lands; the gate lists it as a Minor either way.
2. **CodeQL has not started on the draft head.** Recommend: mark #89 ready (Tuesday) before launching the gate, or launch now and accept the brief's wait-up-to-45-minutes then `STOPPED: NEEDS TUESDAY`. I put the wait in.
3. **Tier 2 vs tier 1 for a leak-centred gate.** Routing G2 says a Sonnet gate that finds a security-shaped issue hands the PR to G1. Recommend: keep Sonnet (your commission, mechanism already measured in B325 r5 and B318-class gates), but if r2 finds any Blocker the re-gate after the fix runs on Opus; the brief says so.
4. **Scope exception on `QuoteApiTests.V0Home.cs`.** The brief makes the gate judge it rather than accept it. Recommend: accept in advance if the gate calls it honest (CI would be red otherwise), and say so in the launch tap to save a round.
5. **MPSCALC-28 Duplicate row action and MPSCALC-245 wording** (Home figures + My/All vs list rows). Recommend: do not make them gate failures (already told so); records seat B308 files a split ticket for Duplicate and corrects 245's text.

## Fence
No fence broken. Wrote only the two files above (Write). No Artifact, Docs, mail, chat, publish. Git: `ls-remote`, `cat-file` only, in the project; GitHub via `gh api` GET under the project's GH_CONFIG_DIR. Scratch copies of head files under `/private/tmp/claude-501/s347/` (scratchpad area, not the project). No pricebook folders, `.tools` trees or `.env` opened; no HTTP to any hosted site; no `cd`; no secret printed. One hook refusal (an unquoted `======` separator) cost one retry, nothing ran.
