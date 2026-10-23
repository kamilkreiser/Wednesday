# Drafter report: B535 (SEAT-G61), MPS Calculator tier-2 QA gate on PR #101 (B522 deal-usage colour rate row)

Drafted 2026-10-23 about 14:30-14:50 AEDT (clock `date`) by Tuesday's read-only gate-kit drafter (Sonnet 5.5, row C8). Wrote only: the kit, its `.pre-stamp` (made with `cp`, `cmp` identical) and this report. Nothing stamped, launched, sent, published, fetched, built or run in the project; no decision-queue tool, no scoreboard, nothing under `fleet/briefs_staged/`, no Artifact/Docs/mail/chat, no HTTP to any app or hosted host, no `az`, no docker, no Jira. The real price books were not opened.

## Number
**B535 was free** (highest existing was B534; `ls briefs | grep B535` empty before writing). The number stands.

## Files
- Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-23_B535_SEAT-G61_mps-b522-deal-usage-colour-row-gate-tier2.md` (101 lines, 54,875 bytes; seat `Datasec/MPS-G61`, model `claude-sonnet-5-5` (read from `models_latest.json`), tier 2, round 1 of 2, ports **8770-8779** reserved, none needed).
- `.pre-stamp`: same path plus `.pre-stamp`, byte-identical.

## Slot count and scans of the kit
Four-underscore line count (`/usr/bin/grep -c -E '_''_''_''_'`): **9** = 8 slot lines + the last line `READ-WHOLE-BY-TUESDAY: ____`; the kit's Stamp says "reads 9". Control: `printf 'x____\n'` through the same pattern reads 1. Other scans: at-sign-capitals-at-sign 0; non-ASCII bytes 0 (`LC_ALL=C`); person-name list (Kam, Kreiser, Paul, Friday, Wednesday) 0; the decision-card id 0; `mps-...-10nn` shape 0.

## What I read
Templates: the B524 tier-2 kit `.pre-stamp` (whole) and its drafter report (whole); the B533 tier-1 kit `.pre-stamp` (whole) for the red-first, mutant, CI-predicate and CodeQL discipline (scaled down). Subject: builder brief B522 (123 lines), ADDENDUM-1, ADDENDUM-2, builder STATUS (whole). Raw by `gh api -X GET`: the compare diff `e027ebd...af210955` (447 lines), `Proposal.cs` at base and head, the new test file (names, fixture helpers, property constants), `B103DealUsageProposalTests.cs`, `ci.yml`, the commit message, `pulls/101` and its files and commits, `check-runs`, `code-scanning` alerts and analyses, `rules/branches/main`, `compare main...<branch>` file lists for every `b5*` branch. Also `ls-remote`, `lsof`, `tmux list-panes`, `uptime`, `ls` of `.tools`, a briefs-folder scan for port tokens. Not opened: the builder's `.tools` trees, `.env`, the real books, the web files.

## Facts re-derived (all MEASURED 14:32-14:36 AEDT)
- Head `af210955...` = branch = `refs/pull/101/head`; merge ref `046863b6` has parents `e027ebd0` and `af210955`; main `e027ebd0`; PR #101 open, not draft, 4 files, +338 -10, 1 commit, mergeable true, state blocked; open PRs #98, #99, #100, #101.
- Check-runs at 14:32: 8 listed; CodeQL neutral; Analyze actions and python success; dotnet, web, python, Analyze csharp and javascript-typescript in progress; no `package` yet; alerts on the PR ref 0; 2 of 4 analyses so far. Rules on main: CodeQL required, `required_status_checks` empty.
- Diff: `Proposal.cs` three hunks as in the kit; ten removed lines in all (3 + 2 + 5); 24 new names (11 methods, one theory of 2 cases, x 2 hosts). Literal census by my regex: 769 -> 771, added occurrences are the two binding keys only.
- Intersection of the four paths with every `b5*` branch: 0 shared; self-compare 4 of 4 (control).
- Heavy slots at 14:33: 1 and 2 absent, 3 held by B518. Panes: MPS-G57 (a live gate), MPS-M16 (the live builder), M2, M3, M4; no MPS-G61. Load 6.34 / 8.23 / 10.01. Ports 8770-8779: no listener, no brief names it (hits are an old 10-21 brief and the 8700-8799 scan range).
- Commit message carries the Sonnet 5.5 attribution trailer; holds no ticket key or name (by reading; gate re-checks).

## Where I departed from the template, and why
- No docs/openapi/generator checks; instead C2 (existing-line table, red-first, ten mutants named in the task's four classes plus the sum's inputs), C3 (literal census with a planted control), C4 (a base-versus-head differential of whole proposals through a scratch recorder, with a DEAD-frame rule so a fixture set that never reaches the rule cannot pass it), C8 (web consumers read-only plus an Escalation rule on any customer string that was never produced before).
- Kept the B524 slot format, pins, load rule, Stamp (8 slots), verdict shape and severity shape; took red-first, mutation, CI pass predicate, names multiset and instance-state CodeQL from B533, scaled down (10 mutants, no attack-row or property-oracle battery; the builder's own property row is read and mutated instead).
- Escalation encodes the task's rule: any figure other than the colour row's presence, or any customer-read string beyond it, is a STOP for Tuesday.

## Leads recorded in the kit for the gate (drafter reading, not findings)
1. `classOf[l.SectionId]` is a new unguarded dictionary lookup in `CopyPurchase`; it throws if a counted line names a section the result does not hold. The pre-existing `labels` dictionary already throws on a duplicate section id, so only the unknown-section case is new. Reachability from a validated draft is not known to me; the kit makes it a probe with a Blocker/Major rule (a head 500 where base answered 200).
2. Arithmetic: the builder's red run counts 4 edited existing rows red per host (26 = 2 x (9 + 4)); the diff edits 4 methods in `B103DealUsageProposalTests.cs` and 2 in `B103DealUsageCountedLineTests.cs`, which would be 6 per host if the CountedLine edit was in place for that run. The kit asks the gate to predict first and explain any difference.
3. The binding equality edit (`:139`) is a consequence of the allow-list decision, not of the ruling's clause; the kit makes the gate show what it pins and run the two registry guards (the builder cites `QuoteApiTests.ExportRegistry.cs`) with a control.
4. With no class estimating colour pages, the builder says the web already has a mono-only rate-method sentence (`sections.ts`, about `:204`) that would now appear for deal-usage quotes. Whether that existing sentence was ever produced before is the gate's read (C8); it is a FACT for Tuesday, a STOP only if the string was never produced by any earlier path.
5. The existing comment block in `CopyPurchase` holds a person's name and a card id at base (unchanged context in this diff); the kit says never quote it and rates it a Note.
6. Routing row G2's own text lists tests, docs, config and tooling, and this diff has one `src` file on a customer document; the kit follows your instruction (G2) and the builder brief, and says the tier is Tuesday's stamped call. Tier-1 would be the B533 shape.
7. The stale per-class sentence in `docs/API.md` (near `:563-570`) is a follow-up (B517 owns the file), noted as a Note, not a defect.
8. B518 adds blocking issues in `DealUsageOf` (the engine side of the same counted-line arithmetic): a semantic neighbour; C6 asks the gate to read its diff.

## Stamp-time reminders for Tuesday
- Re-read head, main and PR #101's check-runs at launch (five legs were in progress at 14:33).
- The B535 launch needs the Q-1 answer YES (scratch rows, a recorder and mutants in scratch worktrees) or C2 and C4 become NOT TESTED as behaviour.
- Pane `Datasec/MPS-G57` is live and the builder pane `Datasec/MPS-M16` is live; heavy-slot-3 was held by B518; load was 6-10.

## UNMEASURED
Nothing was built, run or fetched. Not measured by me: any CI leg result beyond the 14:33 in-progress snapshot; whether the new rows are red at base for the reasons the builder states; the mutant results; whether `classOf` can throw on a validated draft; the web files (OnePager.tsx, ProposalDocument.tsx, sections.ts); the model-routing row's fit; the contents of the B518 branch diff; the full literal census beyond my regex (the tokenizer may differ); load at launch; the `.pre-stamp` of the builder brief's sha256 against the STATUS's own value; the property row's generator reach.
