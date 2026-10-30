STARTABLE: YES after your stamp; load1 read 6.74 at 12:33 but the 5-minute figure was 11.33, so launch_when_cool may still hold it. CI and CodeQL on the head were still running at 12:35 (the gate reads them last, after a wait)

# B940 drafter report (2026-10-30, about 12:33 to 12:55 AEDT)
Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-30_B940_SEAT-G217_hpsmpoc-247-playbook-rail-gate-tier2.md` (67 lines; 8 four-underscore lines = 7 slots + the last line, lines 59-65 and 67, counted by `grep -c -E '_''_''_''_'`; at-sign slot pattern 0; non-ASCII bytes 0 by `LC_ALL=C grep -c '[^ -~]'`). Shape: B938 (stamped this session) copied section by section: preamble, SUBJECT, WHAT THE GATE JUDGES, Step 1 + C1-C9, SEVERITY/VERDICT, first line, FOR TUESDAY, LANDING HOLD, STATUS-NOW, ports, model, Step 0, Launch, Report, PARTITION, Load, STANDING LINES, REFUSE, Stamp. Read-only throughout: gh `-X GET` under the project `.gh-config`, `git --no-optional-locks` on the shared repo, no Jira call, no `cd`, no hosted HTTP, no ref written, no message, nothing in the project folder.

## BLUF
Seat `Datasec/HPSM-POC-G217` (Sonnet, `BRIEF_SEAT_LEVEL=sonnet` inside the quotes), ports 9720-9729, gates PR #247 @ `f14281a8` (3 commits on main `e21d8044`, 0 behind, 5 paths +209 -47). Round 1 of 2 on class "playbook rail removal". The gate re-measures: a page census on the home + 11 module pages, 4 roles, at 1280 and 390 (96 cells per tree, never cut) with base as the control; the viewed count by a visit walk; "All modules", Previous/Next and deep links against base; the current main-nav entry; widths, axe and print; exports and test rows; 13 plants plus one equivalent, two rebuilt for the browser; suites in CI order; CI and CodeQL last; overlap.

## Facts re-measured (instrument; control)
- **PR and refs (12:33-12:35):** #247 open, draft false, mergeable true, `blocked`; head `f14281a8`, base `e21d8044`; 3 commits, all unsigned; 5 files +209 -47. `refs/pull/247/merge` `928e25db` has parents `e21d8044` and `f14281a8`, and its tree `150fe541` = the head tree. Open PRs: 244, 245, 246, 247. Patch 318 lines, 0 non-ASCII. Instrument: gh GET, `ls-remote`.
- **Frozen files equal at base and head** (sha256 by `git show | shasum`): SnapshotLauncher, BlockRenderer, playbook `layout.tsx`, `PlaybookHome.tsx`, `productName.test.tsx`, `GlobalNav.tsx`, `globals.css`. `name-status`: A on the 3 tests, M on the 2 product files.
- **Test rows:** 6 + 3 + 8 = 17 (`ModuleScreen.nav.test.tsx` holds 5 `it(` plus one `it.each` of 3). This matches the builder's +17 (3242 -> 3259).
- **Two traps written into the kit:** (a) `AppShell.tsx:90` renders its own `main#main` while the session is loading, so the gate counts `main` only after the `h1` shows. (b) At the head a module page carries 3 `nav` landmarks by design (Main, Account, Previous and next module). So "no navigation landmark" is defined as no `nav` other than those.
- **Role/auth:** the 20 added lines that match `session|cookie|auth|role` are `getByRole` queries and `useSession` test mocks. The shell's `useSession()` read is an unchanged context line. The product files add 0 such lines. Not an escalation, but the gate re-reads it.
- **Checks at 12:35:** 18 runs. `CodeQL` completed **neutral** (same pattern as #244 at its draft). Analyze actions, js-ts and python success; csharp, vitest, api, SQL Server and five e2e shards in progress; `web (Next.js)` not listed. Code-scanning: head-ref analyses 3, merge-ref 0, open alerts 0.
- **Overlap:** b928 (2 files), b929 (4), b930 (23), b932 (3), b934 (7), b936 (1): each shares 0 of the 5 paths (control: the 5 against themselves = 5). **b930 (H61) edits `GlobalNav.tsx`:** Assessments retires and `my-readiness` takes `also: ["/playbook/snapshot-assessment"]`. It also edits `e2e/playbook.ts` and `e2e/shell-sidebar.spec.ts`. No shared path, but the two are coupled in meaning (AC 2's current entry, and the helpers the gate imports).
- **Ports:** `lsof -iTCP:9720-9729 LISTEN` = 0 lines (the unrestricted listing printed 15). In 9600-9799 only 9670-9673 listen (H66). The 972x scan hit only B916, inside a historical list of finished seats (B886). G215 holds 9700-9709 and G216 holds 9710-9719. `.tools/b940` and `.tools/wt-b940-head` are absent.
- **Panes 12:3x:** tuesday, G215, H68, H66, H65, H67, H64, H61, H62 (the builder, parked), H63, H59, fleet-monitor. No G217.
- **Round count:** 99 `GATE VERDICT` first lines. The loose scan got 9 hits, all other PRs and classes. Result: "NO GO 0 of 2 ... round 1 of 2".
- **Model:** `model-routing.md` G2 `:109`, G-cap `:111`; `models_latest.json:23` `claude-sonnet-5-5`; `brief_seat.sh:24` defaults to opus.

## Builder claims found wrong or loose at drafting
1. **Commit `0c01b69e` says "ModuleScreen.nav.test.tsx adds 7 tests".** It holds 8. The builder caught this itself in `f14281a8` and in FOR TUESDAY item 4. This is a Minor (text): the squash must carry 8.
2. **The PR body (Tuesday's text) ends with a generated-by line holding 1 non-ASCII character.** It must stay out of the squash text. The body's "e2e 416 passed" folds the 2 timed-journey passes into the 414.
3. Nothing else contradicted at source. The runtime numbers (3259, 414/46/0, the 8 plants, the 24 px offset, the card widths) are unmeasured by me and written into the kit as predictions.

## D-decisions (mine, in the kit)
- D-1: **Base is the control for every browser census.** The rail exists at base, so a zero at head counts only if base reads 1 on the same cell. In addition, p1 (rail back) and p10 (`no-print` dropped) are rebuilt as head-side controls for the census and print probes.
- D-2: **The never-cut census frame is 12 pages x 4 roles x {1280, 390} = 96 cells per tree.** 1024 and 1440 are added only if load allows.
- D-3: **13 plants + pE.** The gate re-makes the builder's p1-p8 and adds p9 (`lg:flex-row`), p10 (`no-print`), p11 (literal 11), p12 (All modules after the foot nav) and p13 (Previous/Next swapped). p4 needs a scratch copy of the frozen `PlaybookHome.tsx` in the mut tree only (Q-2).
- D-4: **The `snapshot-assessment` current entry (Assessments) is a Note, not a finding.** It matches base, and the file belongs to H7/H61.
- D-5: Hard stop: target verdict at 120 minutes and HARD STOP at 180 minutes after Step 0. This is lighter than B938: there is no ref tree and only 2 plant builds.
- D-6: Cut order under load is written into the kit's Load line (base whole e2e first; C3, C6 and C8 are never cut).

## Q-questions for Tuesday (each with a default)
- Q-1: Is the snapshot-assessment current entry (Assessments, `GlobalNav.tsx:42`) a Note and not a finding? Default YES.
- Q-2: May p4 plant a scratch copy of the frozen `PlaybookHome.tsx` in `wt-b940-mut` only? Default YES.
- Q-3: Rebuild p1 and p10 for the browser? Default YES (two builds on 9726).
- Q-4: Landing order against b930 (GlobalNav): if b930 lands first, does the gate re-measure on the merge tree, or do you? Default: the kit's main-moved rule STOPs on `GlobalNav.tsx` / `e2e/playbook.ts`, and you re-launch on the new merge.
- Q-5: What does a NO GO mean? Default: the PR is parked and you write a round-2 fix kit.

## UNMEASURED
All runtime numbers; the CodeQL `neutral` reason; whether `web (Next.js)` and the shards pass; whether `parseStored` keeps a well-formed unknown visited id (the kit makes the gate read it first); the three-commit squash title; the runner's fonts.

## Outside-the-fences disclosure
None breached. I computed sha256 prefixes of two helpers and four instruments under `.tools/` (read only) and ran one `ls` of `.tools/` names, which printed every seat's folder name (names only, nothing opened). I listed `.tools/b940` and `.tools/wt-b940-head` (both absent). I did not open `.tools/b931/` or any `wt-b931-*`. Scratch files (PR body, patch, messages, path lists) are in the session scratchpad only.
