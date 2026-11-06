STARTABLE: YES, after Tuesday fills the slots (S2 = `2e69315d24293ea1896393990497610e85bd7210`). Re-read the tip, code main, open PRs and the pane list at the stamp (a moved tip refuses the seat).

# Drafter report: B1339 SEAT-H133, two test rows and a correction on b1320/hpsmpoc-retire-demo-repo-paths (drafted 15:47 to 15:57 AEDT 2026-11-06)

## BLUF
1. Kit `2026-11-06_B1339_SEAT-H133_hpsmpoc-retire-demo-round2-rows.md` (96 lines, ASCII, 12 four-underscore runs: eleven slots and the last line) and `2026-11-06_B1339_slots.json` (a trial through `stamp_brief.py` on a scratch copy: 12 slots stamped, 0 left). Sonnet, C2 (`model-routing.md:92`), `BRIEF_SEAT_LEVEL=sonnet` inside the launch quotes. Tier 2, two added test rows, no product byte.
2. **The correction does not need a commit.** B1320_STATUS lives in the project root's working copy of the analysis repo (`datasecau/HPSM-POC-analysis`), untracked (`ls-files` 0; 56 STATUS files in the folder are tracked, the rest not). It never touches the code branch.
3. **R182 has landed already:** records PR 183 merged at 15:49:40 (records main `b4432413`, was `f529d3b4`); its pane was still listed at 15:53. Its kit cites B1320_STATUS by `192 lines, a944c1bad5bb7b26` and by `:170 :172 :175`; an append moves no pointer but changes the sha and line count. Rule in the kit (Step 8): append to B1320_STATUS only when R182's pane is gone AND its STATUS last line is a closing marker; otherwise the text goes in H133's own STATUS and a line for the next records seat. Records main holds no line quoting `:97` (`named UAT twin` 0; control `twin` 10).
4. Partition measured both sides: H131 (B1326) is not pushed (no `b1326` ref), its kit's only path is `Hosting/ApiFactoryHostStartRetryTests.cs`, and its one mention of `UatOpenTests` (line 57) is a note about H130. Overlap 0 on my two files. The REFUSE on other panes says "GRANTS a write" and tests the other kit's lane row, with H130's kit as the control that fires.

## Facts re-measured (instrument; control)
1. `gh api -X GET`: branch `2e69315d`, main `f4220286`, compare ahead 2 behind 1 files 30, `2e69315d` has 1 parent `ecb097a3`; open PRs 0 (control: `pulls/291` closed and merged; the first query of the drafter also showed #291 on a closed listing, not open).
2. Raw files at `2e69315d`: `UatOpenTests.cs` 704 lines (`:189`-`:192` the row and its neighbours; `With` `:323`, `MeWithAssertion` `:108`, uses of `With` with `WEBSITE_INSTANCE_ID` at `:171`, `:186`); `uatOpen.test.ts` 297 lines (`:193`-`:195`); `routes.ts` 38 lines (`:17`-`:23`); `UatOpenAuthentication.cs` 215 lines (`:105`, `:108`). The gate's fix-shape for web (`res.headers...`) does not compile at `:194`: there is no `res`; the kit adds a second call inside the same `it` (count stays 4072).
3. CI: `ci.yml` 682 lines. Web `npm test` `:478` (no count floor; the only `floor` in the file is `:314`, 100 / 110 databases). The new row's namespace `HpsmPoc.Api.Tests.Auth` falls in shard `api-other-and-feedback` (`:254`-`:255` filter), whose pass predicate is every trx outcome Passed, at least one Passed, the four named tests present, then databases at least the floor. A new host adds a database; a +1 row cannot lower it. SQL Server leg NOT RUN by the seat (no docker grant); a landing condition.
4. Expected counts (DERIVED from the gate's RELAYED numbers): web 4072, `.Auth.` 287, Api project 2162/0/13.
5. Landing form quoted from records main `b4432413`, `CLARIFICATIONS.md:3617` (printed by `awk NR==3617`): head-pinned squash. Main's one path (`web/e2e/mock-rows.spec.ts`) is not in the branch's 30 paths.
6. Model: `model-routing.md:92` C2, `:108` G1, `:109` G2; id `models_latest.json:23`. Ports: `lsof -nP -iTCP:9370-9379 -sTCP:LISTEN` 0 (control 11 overall).
7. `status_watch.sh:56` knows both `READY FOR QA:` and `READY:`. The kit's last line uses the template's `READY FOR QA: B1339 ...` form.

## D-decisions
- D-1 Row 1 is a new `[Fact]` after `:190`, the gate's assertion verbatim; Row 2 is one added line inside the existing `it`, `:194` untouched (property: zero removed lines).
- D-2 Plants Y4 and Y1 are run on copy trees; their exact edit is the seat's to print (the gate's evidence holds only its one-line descriptions). Y4 base: the row is also run on a tree at `6d592ede`.
- D-3 Time: READY Step 0 + 90, HARD STOP + 120 (two dotnet trees, whole web suite and load around 7).
- D-4 Ports: block given, none typed.

## Q-questions for Tuesday (each with a default)
- **Q-1** Correction route: append to B1320_STATUS when R182 is gone (Step 8's rule), else own STATUS plus a line for the next records seat. Default: as the kit.
- **Q-2** The kit's last line is `READY FOR QA:` (the template form) not bare `READY:`; both are in the watcher. Default: keep.
- **Q-3** Gate row for round 2: see below. Default: G2 row with Opus 5.5 first, delta scope, resume G354.
- **Q-4** Tier 2 for this seat, not the template's tier 3 (it adds test rows, not comments). Default: tier 2 as written; the branch's gate stays the judge.
- **Q-5** Port block 9370-9379 is also reserved (none typed) in kit B1335 (NexusAI N102). Default: harmless because neither seat types a port; if you want it clean, give this seat another block.
- **Q-6** Default I think may be wrong: the kit lets the seat append to another seat's STATUS file at all. If you want B1320_STATUS left strictly alone, switch Step 8 to the second route always.

## Round 2 gate proposal
- Row: your G1 reading is defensible because the mechanism sits on a sign-in lock, but the table's G2 row (`model-routing.md:109`) says tests-only follow-ups go to Sonnet unless the mechanism sits on a G1 surface, in which case Opus 5.5 first. So: Opus 5.5, gate class G2/G1 hybrid, named as "tests-only follow-up on a G1 surface". Round count: "NO GO 1 of 2 on class 'retire the demo site's repository paths'" (cap row `:111`); this would be round 2.
- Scope: delta only. G354's own FOR TUESDAY 2 says Steps 1-7 stand on an unchanged head; the head now changes by two test lines. Gate re-measures: the commit's two added rows and nothing else removed, Y4 and Y1 red, restored, web and `.Auth.` runs, the correction line, and re-reads the base lock matrix only by citing G354's cells (not re-run).
- Resume vs fresh: resume G354 (pane idle). It has the worktrees, the plants, the matrices and the clock history; a fresh seat re-pays about 100 minutes. Risk: a resumed gate may anchor on its own verdict; mitigate by making the gate recompute the two plants from the kit's own text, and by a fresh Opus read only if the delta touches anything outside the two files.

## UNMEASURED
Whether R182's pane has closed and its STATUS last line (read at 15:53: it still said records pending in the lines I saw). Whether `problem()` returns a mutable Response for plant Y1. H131's pushed diff (nothing pushed). Whether the new Fact passes under the test host with a platform marker set (the gate measured the behaviour; the seat re-proves it).

## Outside the fences
Read-only everywhere except my three files. One stray `.md.bak` made by my own `sed -i` was moved to my scratchpad (`rm` is blocked, and it was my artefact). Raw file fetches by `gh api -X GET` into the scratchpad `b1339/`. I read the analysis repo's records main by `gh api -X GET` (CLARIFICATIONS.md) and `git` read verbs on the project root. No card read, no `_ledger.md` read (one grep of `_ledger_laptop_datasec.md`, which the rules name, found nothing), no Jira, no hosted host, no mail.
