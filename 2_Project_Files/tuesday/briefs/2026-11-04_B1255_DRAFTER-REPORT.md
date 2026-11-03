STARTABLE: YES (once Tuesday fills the 9 stamp slots; no live Datasec/MPS pane, no heavy.lock or light.lock under .tools/*, load1 3.09, 188 GiB free, .tools/b1255 absent, origin b1255 ref absent)

# B1255 drafter report: SEAT-M92, MPSCALC-382 per-site purchase rule rows, tests only

Kit: /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-04_B1255_SEAT-M92_mpscalc-382-persite-rows.md (91 lines, 9 slots by `grep -c -E '_''_''_''_'`, 0 non-ASCII; `.pre-stamp` identical by `cmp`). Slots: 2026-11-04_B1255_slots.json (9 keys). Clocks (date, AEDT): 07:31:28 start, 07:32:17 Jira reads, 07:32:24 to 07:36:15 gh/raw reads, 07:38:33 last. Nothing in the kit is later than these.

## BLUF
- One file (tests/MpsCalc.Engine.Tests/ComponentQuantityRuleTests.cs), one commit, new branch b1255/mpscalc-382-persite-rows off main 511e6c03. Four new results: two [Fact] for item (1) (missing site entry beside a site with devices; missing entry alone) and one [Theory] of 2 cases for item (2) (repeated section id, both orders, as today's reading). Inserted between :992 and :994. No product byte, no ENGINE.md edit, no Jira write.
- Item (2) is built as a characterisation driven by ONE named `private const bool` (the open question's name); the seat proves the one-line flip by program in -mut (flag false: both cases red at the head, both green with the last-copy plant). If the flip or a warning-free build fails, the seat drops item (2) and ships item (1) alone (the kit carries both READY forms).
- The row-1 trap is in the kit: the rows call Calc directly; red-first reads the trx for `NullReferenceException` and a SitesWithDevices frame, so a plant-red by assertion mismatch (masking) is a STOP.

## Contradictions and mismatches FIRST
1. The sweep (SWEEP-0725, M-A) says a "null-site-list row in the file at :870 (`Group(null)`) and :882". Measured: :870 is the row where the section is not a group (`Group(null)` is a null fleet quantity), :882 is an optional per-site line. Neither holds a null site ENTRY; `null!` occurs 0 times in the target file. The only null-entry row is in another file, PurchaseSiteAllocationTests.cs:350 (call at :352), with no per-site line, which is why the plant survives. Kit follows the measured file.
2. Compare main...b1194/mps-359-persite-no-sites-refusal lists ComponentQuantityRuleTests.cs (1 hit), against the partition expectation of none. Cause: that branch is the already-landed -359 branch (3 commits not on main as such because main took a squash). Control that settles it: the file's blob on the branch head e296f5b7 and on main 511e6c03 are the same (dbf741f3...), so the branch adds nothing. Kit says so and tells the seat to prove it by blob.
3. The sweep and the ticket both list `PurchaseRecomputation.cs:54` among the product pointers. The independent review proved the plants on it equivalent (B1213 STATUS, "GY3, GY4 EQUIVALENT": a refused quote returns before the reconciler counts). The kit therefore gives NO reconciler row and says why; the pointer is cited only as context.
4. The ticket's text pins "main 0d656f90"; main is now 511e6c03. `compare 0d656f90...511e6c03` lists one file (Api TemplateIsolationTests.cs): the engine files and the target test file are unchanged, so the ticket's claims hold at the new main (blob dbf741f3 equals the branch head's). The kit pins 511e6c03.
5. The ticket body reads "which listed copy decides the note ... is an open question" and its checklist says the note is added "only when the first listed copy has no device site": measured and consistent (:398 reads `input.Sections.First`). No contradiction; recorded because Tuesday's call rests on it.
6. The older kits cite `CLARIFICATIONS.md:774` and `:2218` without the folder; the file is `1_Project_Definition/CLARIFICATIONS.md`. :774 reads "squash with the head pinned ..." (an entry about another round, same rule), :2218 reads "for this project a row counts as a red-first test when removing the behaviour turns it red; a planted fault counts." Kit gives the full path.

## Facts re-measured (instrument; control)
- Jira (copy of the b1212 reader, outputs to scratchpad, GET only): MPSCALC-382 Backlog, comments 0, updated 2026-11-03T19:40:54; MPSCALC-359 Backlog, comments 2 (the records comment is done: the seat must not comment); control MPSCALC-361 Done, comments 1. Ticket text quoted in the kit (BLUF, checklist, Acceptance check, Open question).
- Main: `gh api -X GET git/ref/heads/main` = 511e6c037ce029835c94b2400930bb6755009a30; open PRs 121 and 120; matching-refs b1255 = 0, control b1093 = 1.
- Raw files at 511e6c03 (line counts by wc -l): ComponentQuantityRuleTests.cs 1016, PurchaseCalculator.cs 1060, PurchaseRecomputation.cs 266, ENGINE.md 213, ci.yml 123.
- Pointers by awk NR / grep -n: PurchaseCalculator.cs :583 (guard `x is not null && x.Devices >= 1`, 1 occurrence in this file, 1 more in PurchaseRecomputation.cs :54), :398 (`input.Sections.First(s => s.Id == l.SectionId)`, 1 occurrence), :321 DUPLICATE SECTION, :319 `sectionIds.Add`, :339/:341 X-43, :168/:169/:175 structure check and the early return, :184, :187, :376-:378 UNKNOWN SECTION. Test file: Group :56, Input :59, Calc :62, L :72, Book :75, SiteRefusal :741, PerSiteNote :743, Sited :746, AssertRefusedAt :750, AssertPerSiteLine :763, AssertReconcilesUpfrontAt :906, last row declared :981 ending :992, blank :993, guards comment :994. DUPLICATE SECTION occurs 0 times in the test file (control: 1 in PurchaseCalculator.cs). PurchaseSiteAllocationTests.cs :350/:352.
- Partition: 7 branches match `^b11[7-9]|^b12`; compare main...<branch> with the ComponentQuantityRuleTests filter: 6 zero, 1 hit (the landed -359 branch, see Contradiction 2). Control: `commits/e296f5b7` prints 1 for the filter.
- Hand derivation (issue lists only, no money): row 1a ONE issue (Blocking, INVALID SITE ALLOCATION, sections[g].sites); row 1b TWO (that, then the note at bomLines[2].quantityRule); row 2, no-device copy first: duplicate + note; device copy first: duplicate only; the last-copy plant swaps both. Derived from PurchaseCalculator.cs :316-:341 (sections loop first), :373-:401 (lines loop), :169 (refused quote returns before Review issues), and the ticket's checklist agrees. The seat re-derives and runs it; UNMEASURED by execution at drafting.
- CI: ci.yml :42 `dotnet build MpsCalc.slnx -c Release`, :43 `dotnet test MpsCalc.slnx -c Release --no-build`; Directory.Build.props :6 TreatWarningsAsErrors true, :4 Nullable enable (hence `null!`).
- Model: model-routing.md :92 row C2 (Sonnet builder), :109 row G2 (tier-2 gate, tests-only); models_latest.json :23 claude-sonnet-5-5. Launch line carries BRIEF_SEAT_LEVEL=sonnet inside the quotes.
- Panes: tuesday, Datasec/NexusAI-N97, fleet-monitor; no Datasec/MPS pane. Ports: none needed (lsof listing in the kit is context). No heavy.lock/light.lock (glob matched nothing). .tools/b1255 absent (ls error).
- The eight .tools/b1212 sources exist: heavy.sh, hb.sh, env.sh, ci-dotnet.sh, jira_read.py, scratch/plant.py, scratch/run_plants.sh, scratch/trx_count.py (listings printed).

## D-decisions
- D-1 Rows 1a and 1b assert issue identity (severity, code, target) and the note through PerSiteNote only; the X-43 message is not copied into a literal (its words are the product owner's, and AssertRefusedAt cannot be reused because it requires every issue to be the note). Helpers are not edited.
- D-2 Item (2) is one Theory over the order, with the expectation tied to a single named const (the open question). Chosen over two fixed Facts because the one-line flip is Tuesday's condition for building it at all. The flip is proved in -mut with the opposite plant, so the claim "a later answer flips it with one line" is measured, not asserted.
- D-3 Plants: two only (GY1 on the calculator, GY7 on the calculator), plus P0 and the two flip runs; no round-1/2 plant sweep (those rows are unchanged and the file only gains lines in a gap). The seat runs both plants on the UNCHANGED file first to confirm the ticket's claim (0 red).
- D-4 Reconciler line :54 gets no row (equivalent per the review).
- D-5 Insertion between :992 and :994 so no existing line moves or changes; added constant lives in that gap too (a mid-class const is legal).
- D-6 Gate and round: tier 2, G2 (tests-only, mechanism measured by the independent review).

## Q-questions for Tuesday (default)
- Q-1 Sonnet C2 and gate G2? Default: yes.
- Q-2 Assert identity only (not the X-43 message text) in rows 1a, 1b and 2? Default: yes. Override if you want the full message pinned (adds a user-facing-word copy into a test).
- Q-3 Item (2) as a Theory with a const flag, STOP-to-item-(1)-alone if the flip proof or a warning-free build fails? Default: yes (this is your call, quoted verbatim).
- Q-4 Gate round: kit default ROUND 1 OF 2, NO GO 0 before, class 'MPS Engine test: per-site purchase rule rows'. I did not read earlier gate verdict lines for this class; confirm from them. Default: as printed.
- Q-5 Hard stop 60/120 minutes after Step 0 (like B1232), not after a clock you stamp. Default: yes.
- Q-6 The one-sentence ticket comment (item 2 is today's reading, question open) is drafted by the seat in FOR TUESDAY for the records seat to paste after landing. Default: yes; the seat writes no Jira.
- Q-7 Branch name: the instruction said b1255/mpscalc-382-persite-rows; used as given.

## UNMEASURED
- Engine baseline count at 511e6c03 (relayed 739 from the last gate's merge run; Import 196, Api 3359). The seat measures it.
- Whether the rows go red/green as hand-derived (needs dotnet; no build run by a drafter). Whether `private const bool` compiled and used in an == expression builds with 0 warnings under TreatWarningsAsErrors and latest-recommended analysis (the kit has the fallback, a static bool property, then the STOP).
- That a null entry reaches InputHash.Compute without throwing for the item-(1) shapes: the existing row at PurchaseSiteAllocationTests.cs:350 builds the same shape and passes today, and the review's probe ran both cases; not re-run by me.
- Whether any decision card cites MPSCALC-382 (no decision_queue read, per the rules).
- Hosted CI, CodeQL, web and python jobs.

## Outside the fences
Read-only only: Jira GET (three keys, scratchpad copy of the b1212 reader, outputs under the session scratchpad), `gh api -X GET` (ref, pulls, matching-refs, compare, branches, contents raw, trees, commits, under the MPS project's GH_CONFIG_DIR), local reads of the B1212/B1232 kits, STATUS files and drafter reports, the B1213 STATUS and residue.md, CLARIFICATIONS.md, model-routing.md, models_latest.json, .tools listings, plant.py and run_plants.sh heads; tmux list-panes, lsof, df, uptime. One `sed -i` on my own just-written kit file to reword one phrase. No fetch, no ref write, no card read, no mail, no Artifact/Docs tool. One stray `cd` in a command was refused by the hook before it ran (re-issued without it).
