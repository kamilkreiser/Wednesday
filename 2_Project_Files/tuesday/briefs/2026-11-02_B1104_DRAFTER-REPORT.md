STARTABLE: YES (whole ruling in one lane: API commit first, web commit second; 39,991 bytes)

# B1104 drafter report (reworked on the coordinator's message), Mon 2 Nov 2026, `date` reads 07:06:29 to 07:25 AEDT

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-02_B1104_SEAT-H99_hpsmpoc-header-scored-count.md`. The kit says in its own text that the Q-1/Q-3/Q-5 decisions are Tuesday's, not the product owner's.

## BLUF
- Held customers: display problem. Saved customers: the "0 of 0" is the API's, computed at read time, not stored: `CustomerEndpoints.cs:307` `Views.Summary(latest, result, null)` and `Views.cs:107-109`. The list route passes a real evaluation (`AssessmentEndpoints.cs:42`), hence "16 of 16". No API response holds a scored count (`QuestionState`, `Questionnaire.cs:23`, has no scored flag; it lives on the ruleset question). Runtime is UNMEASURED; the kit makes the seat prove it with an API row red at main (A1).
- Design in the kit: add optional `scoredAnswered` / `scoredRequired` inside `completion` (omitted when the ruleset is null), pass the evaluation at the four customer-read routes, send the same fields from the list route, print them in the header and in the other answered-count screens (moved when they show the same customer's count, named and reasoned when left).

## The five requirements
1. **Cost**: Step 4. In-process host, EF command counter plus stopwatch, N=300 warm reads, three interleaved base/head runs, SQLite. STOP if more than one extra SQL command, or median slower than max(5 ms, 25 percent), or p95 slower than max(15 ms, 50 percent). Justification: the added work is in-memory over at most 16 questions plus one profile read (`ProfileValuesAsync`, `AssessmentEndpoints.cs:664`); a round trip is what matters on hosted SQL Server after a wake. Control: the list route counter must read one command more than a no-profile read. Row A6 commits the head's command count.
2. **Additive contract**: enumerated by me by program (`grep -rl -F AssessmentSummary`): API-side `Contract/openapi.yaml` (byte copy, sha in PROVENANCE.md, NOT edited) and `Contract/openapi.delta.json`; web-side `contract/design-pack/api/openapi.yaml` (not edited), `contract/seat-a/openapi.delta.json` (a DIFFERENT file; `cmp` differs at char 18; both `schemaPatches` empty), `openapi.merged.json` (regenerate, `--check`), `src/api/schema.gen.ts` (`gen:api`), `types.ts`, mock `api.ts` and `customer-detail.ts`. The patch goes in both delta files; the seat re-enumerates and proves zero removed lines. `AssessmentSummary` has `additionalProperties: false` but `completion` does not.
3. **Both DB modes**: no provider-specific code on the customer read (only a comment, `CustomerEndpoints.cs:124`); CI runs the API tests on SQLite (`ci.yml:87`) and on SQL Server (`:165`, part `api-assessment` = namespaces `.Assessment.` and `.Hosting.`). The new test class must sit in `HpsmPoc.Api.Tests.Assessment`. The seat has no docker, so the SQL Server leg is hosted CI only; the kit says so.
4. **API test red on the null**: row A1 (customer read equals list route's completion; red at main with 0 and 0), plus A2-A7 and plants PA1-PA5. A5 guards a hazard I found: `SetOf` throws when a content package is no longer loaded (`AssessmentEndpoints.cs:635-650`), so an unwrapped evaluation could turn working customer reads into 500s.
5. **Ruleset census (python over the shipped JSON)**: unscored questions DO exist: `snapshot-placeholder` 16 questions, 11 scored (api seed and web copy); `snapshot-policy-aligned` 0.1.0/0.1.1/0.1.2 all 16 of 16 scored; `synthetic-structural` 4 questions, 3 scored. So the counts differ only on placeholder and synthetic-structural; the "16 of 16" sample customer's ruleset is UNMEASURED.

## Partition (re-measured 07:18; both sides in the kit)
Panes: R128 (live since 07:14), G276, H98, H97; H99 absent. H97's kit: four api paths, 0 hits for `Views.cs`, `CustomerEndpoints`, `AssessmentEndpoints`, `openapi`, `schema.gen` (grep -c -i). H98: seven paths (partner/, globals.css, AppShell.sidebar.test.tsx, shell-sidebar.spec.ts); its only `CustomerShell.tsx` mention is a hold. G276's eight files (`compare c1457349...b1073`) share nothing with mine; it only reads `CustomerShell.tsx`. R128's kit: 0 mentions of HPSMPOC-420/421. b1095, b1097, b1098, b1104 refs all absent on origin, so partition rests on kit lists, with a compare-based recheck at the PIN. Shared surface only: H97 and I both run `HpsmPoc.Api.Tests`; `SqlServerWakeRetry.cs` wraps the DB opens my extra read uses.

## Other facts (instrument)
Main `c14573495e51c4ee6d656460f6940927a97e0007` by `git ls-remote` and `gh api` at 07:18:35 and 07:20:56; open PRs 0. Ports 9010-9019: `lsof` 0, positive control (python listener on 9019) read 2 then 0; word-bounded kit scan has no hit. Model: C2 re-tested for additive API plus web (C3 no auth/security/money design: `Gate.CustomerAsync` untouched; C4 no write, migration or delete), Sonnet, `BRIEF_SEAT_LEVEL=sonnet` in the launch; gate G1 tier 1 Opus. READY target 240 min, hard stop 330. Slot lines 11, ASCII, no card id or person's name in the kit.

## Q-questions for Tuesday (each with a default)
- Q-A The delta files: PROVENANCE.md says each delta entry is tied to an ADR. Default: the `$comment` cites the product owner's 2026-11-02 ruling; confirm that suffices.
- Q-B Names `scoredAnswered` / `scoredRequired` inside `completion`. Default: as written.
- Q-C Saved chip when the API lacks scored fields (older API, null ruleset): default hide the chip (never the old words), so no screen says two things.
- Q-D Cost thresholds (+1 command; max(5 ms, 25 percent) median; max(15 ms, 50 percent) p95). Default as written.
- Q-E Time: READY 240 / hard stop 330 minutes (two suites plus cost runs). Default as written.

## Contradictions with the commission
1. The kit is 39,991 bytes, under 40 KB, but only by cutting prose and compressing; no check was dropped. Several steps are long single paragraphs.
2. The kit's `PartnerDashboard`-style row names are not used; Step 7 names screens without pre-measured line pointers for `SecurityDashboard.tsx`, `SecurityReports.tsx`, `SnapshotResult.tsx` beyond `:134` (the seat prints what each counts, as asked).
3. "Passing a real evaluation changes `answered` and `required` from 0 and 0": this does change what an existing field carries; I read your fence as allowing it (a correction, not a change of meaning) and the kit says so; if you read it otherwise, say so before the stamp.
4. A dangling reference to "D-3" remains in Step 7 (the D-list was cut for size).

## UNMEASURED
Real API at runtime; whether every saved customer shows "0 of 0"; the read's actual cost; whether the `Scored` property is reachable from `RulesetOf`; the first sample customer's ruleset; line pointers into the security screens; hosted CI.

## Outside the fences (disclosure)
Read-only: `gh api -X GET` (tree, contents, tarball of main into the session scratchpad, matching-refs, compare, pulls), `git ls-remote` in the project repo, Jira GET through `.tools/b1007/` (two issue reads, one JQL with `project = HPSMPOC AND ( ... )`), `decision_queue.sh show` of the one exact card (earlier turn), kits B1095/B1097/B1098/B1102 by grep, `tmux list-panes`, `lsof`, one 6-second loopback listener on 9019 as positive control (earlier turn), python censuses over the unpacked tarball. Only the two named files were written, plus scratch scripts in the session scratchpad (trim scripts that rewrote the kit).
