STARTABLE: YES (after your stamp; -377 is NOT STOP-shaped: it needs no API field or persistence beyond the browser; one ticket premise is corrected below and does not block)

# B955 drafter report (Sonnet 5.5, 2026-10-30 about 17:05 to 17:45 AEDT)
Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-30_B955_SEAT-H75_hpsmpoc-376-377-steps-3-5.md` (150 lines; 9 four-underscore lines = 8 slot lines + the last line, counted by a python line scan; at-sign slot pattern 0; non-ASCII lines 0). Read-only everywhere else: `gh api -X GET` under the project `.gh-config`, Jira GET through `.tools/b649/jira.py`, a tarball of main extracted in scratch, no `cd`, no ref written, no message. Nothing written in the project's Briefs folder.

## BLUF
Seat `Datasec/HPSM-POC-H75`, ports 9840-9849, branch `b955/hpsmpoc-376-377-steps-3-5` off main `332dcc6f`, Sonnet (row C2 line 92), `BRIEF_SEAT_LEVEL=sonnet`. ONE branch, two parts in order: part 1 (-376) restyles the Findings, Recommendation and Roadmap steps and pins the by-section caption; part 2 (-377) adds a browser-held action register (`customer/remediation-store.ts` plus an exported `RoadmapRegister` inside `RoadmapScreen.tsx`, rendered after the buckets, never inside `RoadmapBoard`). Four new files, six edited. Gate G2 tier 2 by default (Q-6).

## Your questions, answered
- **Does -377 need an API field or persistence that does not exist? No.** `schema.gen.ts` holds no owner, target date, state or evidence reference per roadmap action. It has `ActionPlan` (partner readiness plan: ownerRole, dueDate, status; no evidence field), `ResponseWrite.evidenceRefs` (answers) and `addEvidenceReference` (EV-nnn for answers). The ticket itself says to hold it in the browser in that case and to record the API ask in the PR, so the kit builds it client-side and carries ready-to-paste API-ask text. The default "build -376 only" does not apply. Useful extra: `ScoredResult.actions[].owner` already exists (D-5 / Q-4).
- **Customer-facing or status words in -377:** yes, all new. "Evidence submitted" and "Verified complete" occur nowhere in `web/src` or `web/e2e` (grep, controls fired); "Not started" and "In progress" exist elsewhere. Full list in Q-2.
- **Model row:** builder C2 (line 92), not C3 (no auth, credential or money design). Gate G2 (line 109) by the routing table; G1 (line 108) lists security surfaces, destruction, deploys and "handed to a client tester". -377 is none of those on its face, but see Q-6.

## Sweep pointers found WRONG or incomplete (what is true)
1. **The caption premise.** The ticket says the design draws only the current figure and the caption must say what is drawn. That is the design's HTML (`stepScore`). The APP's `ScoreBar` already prints "current -> target" and draws a target tick whenever `target` is non-null, so "By section: current vs target" is TRUE in the app. -376 AC 2 is a prove-and-pin job unless a section can have a null target (Q-1).
2. **H16's YOURS list misses couplings.** `DesignSystemScreen.tsx` imports `RoadmapBoard` and `FindingCard`; `snapshot/SnapshotResult.tsx` (H15) imports `ResultsView`; `FirmwareTask.tsx` (H18) imports `findingHref`. Export names and props are frozen in the kit. Read-only tests that exercise the screens and were not listed: `FindingOverride.test.tsx`, `LoadFailed.states.test.tsx`, `CustomerHeading.alias.test.tsx`, `industries.test.tsx` (requires `useCustomerEyebrow(` in four of the files), `gate-b99-labels.test.ts`, `draft-density.test.tsx`.
3. **HPSMPOC-402 "page score bars":** `ScoreBar` already uses `progressTrackClass` and `progressFillClass`; likely met in code, a records matter, not this lane.
4. **Layout fact the sweep could not have:** after #245 the content column is 762 px at 1280, so `RoadmapBoard`'s `xl:grid-cols-4` gives about 170 px per bucket. The kit tells the builder to re-tune and measure.

## Measured (instrument; control)
- main `332dcc6f` (`commits/main`); open PRs #253, #252, #251, #250, #248, each `pulls/<n>/files` intersected with the 12 lane path lines by `grep -x -F -f`: shared 0 each; planted `RoadmapScreen.tsx` line reads 1. All 15 live `b9*` branches (`compare/main...<b>`): shared 0 each. `matching-refs/heads/b955` = 0 (control `heads/b9` = 22 refs). `lsof` on 9840-9849 = 0. `.tools/b955` absent (controls `.tools/b198`, `b267`, `b649/jira.py` list). Load1 7.40 at 17:20, 8.7 at 17:15.
- Line counts and sha256 prefixes of the six edit files are in the kit (RoadmapScreen 76, ResultsScreen 54, FindingCard 171, RecommendationScreen 144, ResultsView 74, FindingDetail 225); non-ASCII characters counted per character per file.
- `browserStore` (partner/browser-store.ts): sessionStorage, parse-gated, try/catch around every storage call, memory fallback; `isDay` exported from `partner/action-plan.ts` (count 1).
- Jira: both tickets read whole, 0 comments each; scope sentences and Done-when quoted verbatim in the kit.
- Design file sha256 equal to the pin; `stepScore` line 181, `stepRoadmap` 185, `partnerRemediation` 283, save handler 305.
- Not run: any suite, build, browser, worktree.

## D-decisions (mine, in the kit)
D-1 caption proved and pinned, not rewritten; D-2 one branch, part 1 pushed green before part 2; D-3 base 332dcc6f; D-4 store export names fixed (HPSMPOC-388 will read them); D-5 owner starts from the action's existing `owner`, written only on Save; D-6 `browserStore` / sessionStorage; D-7 keyed by customer route id + action id; D-8 the only added strings; D-9 target READY 200, hard stop 300.

## Q-questions for Tuesday (words first; each with a default)
- **Q-1 (word) The by-section caption.** Default: keep "By section: current vs target" byte-equal and pin it with a test; the builder STOPs if any section can show a null target. Answer needed only if you want different words.
- **Q-2 (words) The register's added strings (D-8), approve or change:** heading "Action register"; label "Sample data, kept in this browser only"; labels "Owner", "Target date", "State", "Evidence reference"; states "Not started", "In progress", "Evidence submitted", "Verified complete" (the ticket's words); button "Save action update"; refusal "Add an evidence reference before marking an action Verified complete."; "Enter a real date."; "Saved in this browser." Default: as listed (prototype wording where the ticket is silent).
- **Q-3 (word) The sentence "Verified complete needs an evidence reference. The reference is not checked independently."** Default YES, include: the status word reads as assurance and the later security workspace may show it to customers; the design's own text says the local demo does not verify.
- **Q-4 Owner start value.** Default: prefill from the existing `actions[].owner` when present (no invented values). Alternative: always empty.
- **Q-5 Storage.** Default sessionStorage via `browserStore` ("like the action plan"; survives reload, dies with the tab). Alternative localStorage would survive a new tab but is a new pattern.
- **Q-6 Gate tier.** Default G2 tier 2 for the branch. Consider G1 only if you want the refusal rule and the "Verified complete" word treated as an assurance claim before wave 3 shows it to customers.
- **Q-7 One PR or two.** Default one PR, one gate. Risk: a NO GO on -377 holds -376. Alternative: land -376 from the part-1 commit as its own branch (needs a second ref).

## Stamp slots, recommended
STAMP: read whole with this report, D-1..D-9 accepted, Q answers above. KEYS: HPSMPOC-376, HPSMPOC-377 (402 and 388 context). LAUNCH WINDOW: until the 18:30-style evening window you set; load1 below 7; name H59, H63, H66, H68, H69, H70, H71, H73 and the gates beside it. Launch authority: the 10:07:23 commission, 10-29 design instruction, 10-16 merge-once-tested grant, as-many-agents rule, 10-24 standing order, Sonnet-first grant. Target READY 200 min, hard stop 300. Head/main at launch: 332dcc6f unless moved (re-check, base stays 332dcc6f if no listed path moved). Model line: `model: claude-sonnet-5-5 -- Sonnet first: three-screen restyle plus a browser-held register (model-routing.md row C2 line 92, gate row G2 line 109)`. Pane `Datasec/HPSM-POC-H75` (no such pane at 17:1x).

## Reasons not to launch now
None blocking. Load is 7 to 9 with ten HPSM-POC panes; launch via `launch_when_cool`. Keep the launch after H74 (B954, steps 1-2) is not required: files are disjoint, the only shared render is `ResultsView`, which the kit freezes in shape.

## Outside-the-fences disclosure
One `gh search/code` burst (about 12 calls) hit the search rate limit; I switched to a tarball of main and local grep. No other effect. Scratch is under `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/8a8e5624-4358-43cb-ab64-af03ddbc5b41/scratchpad/drafters/b955/`. No file written in the project's Briefs folder.
