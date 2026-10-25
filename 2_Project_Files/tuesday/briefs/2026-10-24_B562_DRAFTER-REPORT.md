# B562 drafter report (gate kit for PR #104, SEAT-G72, tier 1, Opus, round 1 of 2)

Drafted 2026-10-24 07:49-08:05 AEDT, read-only. Files written: the brief, its `.pre-stamp` copy (cmp equal), this report. Nothing fetched, built, run or published; no Jira, mail, chat, decision-queue, Artifact or Docs call; no `cd`; gh GET only; git read verbs only.

Brief (100 lines): `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-24_B562_SEAT-G72_mps-104-gate-tier1.md`
Pre-stamp: same path + `.pre-stamp`. Slot grep: 9 lines (8 slots, lines 26-33, and the last line 100); `@X@` pattern 0; non-ASCII 0; no person's name.

## Facts MEASURED (07:49-07:53, by `date`)
- Head `655606a9b7a77bc92b7ef35e3302c4369c7d4029` = `refs/pull/104/head`; main `a5b4bbb5...` (the PR base, unmoved); `refs/pull/104/merge` `51ed297f`, parents `a5b4bbb5` + `655606a9`; **merge tree sha = head tree sha (`99ea66a7...`)**, so wt-merge and wt-head are the same tree today.
- PR #104 open, not draft, mergeable true, state `blocked` (checks running), 7 commits, 7 files, +512 -7. Numstat per file as in the brief; per-commit path counts 1,1,1,4,1,1,1; both fenced production files diff-stat empty; 7/7 Co-Authored-By trailers; 0 percent figures; 0 non-ASCII added bytes; 0 Skip/Trait/TODO.
- Commit messages: the only two ticket/brief-id hits are the NEW TEST FILE NAME `SourceLifecycleTests.B560WhitespaceId.cs` (in two messages). Graded Minor in the brief (the commission suggested the name; messages cannot be amended; squash message is Tuesday's).
- Check-runs of the head: 7 listed, all `in_progress` (dotnet, python, web, Analyze x4); alerts on `refs/pull/104/head` open = 0 (no positive control exists); `required_status_checks` list length 0; rules types deletion, non_fast_forward, code_scanning, required_status_checks.
- Overlap of the 7 paths with PR #102's 21 files: 0 (`comm -12`). Open PRs: #104, #102 only. No `b562*` or `b561*` head on origin; `.tools/b562`, `.tools/qa-b562` absent.
- Heavy slots: slot 1 held by the builder's STALE holder `B560 06:57` (the harness refused its removal; Tuesday's ADDENDUM-1 of 07:50 orders a move: whether done is UNMEASURED), slot 2 `B561 07:48` live, slot 3 free. load1 7.56 at 07:49. Live panes: %0 tuesday, %360 MPS-M7 (B561), %359 MPS-M6 (builder, idle), %358 HPSM-POC-G71, %1 fleet-monitor. No MPS-G72.
- Ports: block **9110-9119**; no 2026-10-23/24 brief names a 911x token; lsof empty (rc 1), bind control listed then freed. The gate needs no port.
- SDK 10.0.401, node v26.8.1, npm 11.19.0 (this box); model id `claude-opus-5-5`; gh auth shows a logged-in account (handle not quoted).
- Source reads: the whole production change is one optional parameter on `PanelRows` and one changed return expression (`!HeadingShaped(sku) || (mapOptionSkus?.Contains(sku) ?? false)`), plus a per-sheet ordinal set built in `ImportPanelOptions`; the new membership test sits inside `!SkuShaped(sku)`. `DEVICE SKU MISSING` exists at `PriceBookImporter.cs:423`; the doc says 30 devices at `IMPORTER.md:22` and `:106` (builder cites 105). The real catalogue map is not in the tracked tree (only `CatalogueMap.cs` and a synthetic fixture).

## Shape decisions
Cloned B552 (tier-1 gate, findings-only, REFUSE block, stamp slots with four underscores, own instruments, heavy-slot atomic mkdir, load rule, RESUME, final VERDICT lines). Changes: round 1 of 2 (cap statement kept: round 2 would be the cap); 8 questions rebuilt for this PR; GRADING rewritten for an importer Warning-only change (G-1 differential: stored row/panelBlocks/count/end-place change = Blocker; G-2 surviving mutants; G-3 test validity; G-4 docs/words; G-5 confidentiality Blocker; G-6 CI; G-7 hygiene; G-8 delta/claims; G-9 coupling with #102); checks C1-C11; C5 is the gate's own differential with a generator-power control; C6 re-generates the 428-triple literal (python3 -I, unidata must be 16.0.0); C10 builds a scratch combination with #102.

## Judgement calls for Tuesday at the stamp
1. **Hard stop**: I suggest target 2.5 h / hard stop 3.5 h (about 35 mutants, each a Release build + filtered run; Api whole run 4-12 min; CodeQL poll up to 30 min). B552 used 3/4 h with more mutants; change if you want slack.
2. **Load threshold**: set to load1 < 7 (B560's rule, task text), not B552's 8. Load was 7.56 at 07:49 with B561 live.
3. **Heavy slot 1 is a stale holder** (B560). If your ADDENDUM-1 move has not happened by launch, the gate takes slot 3 (slot 2 is B561's); it never touches holders. Confirm at the stamp.
4. **Q-1** (scratch rows, scratch map/book, scratch source edits in its own `.tools/b562/` worktrees): needed for C3-C6 and C10; the brief asks you to answer YES/NO in the "Stamped by" slot.
5. **Brief-number hygiene**: `B560` sits in the new test file name and two commit messages. I graded it Minor and told the gate the squash message must omit it; if you prefer Major (template: a ticket key/finding id in a commit is Major), edit G-7.
6. **Docs words are IN the branch** (4 docs lines) although the commission said docs ship only after the product owner's words. The gate lists which lines carry new words and does not judge them; the merge-sequencing against his words is yours. My lead L5 flags the care-row sentence "a SKU listed on several sheets is a row on each, so they are not distinct SKUs" as an unprovable claim about the real book (359 BID + sheets = 371 bounds new SKUs at 12, says nothing about repeats): graded Minor (G-4).
7. **Partial -200** is accepted by your stamp ruling 5; the gate grades it PARTLY and "owed", not NOT MET-as-failure.
8. **Multi-device reachability** (leads L2/P8/P9): the new rows hold the plain code on one-device sheets only; whether a real colour-panel sheet maps several devices is UNMEASURED (real map not readable). The gate builds a scratch two-device map; survivors are Minor if unreachable-by-census, Major otherwise; a seat allowed to open the store owes the count.
9. **#102 coupling**: I added a scratch merge of #102's head + the 7 paths (wt-102) with the 18 new names as filters, graded as merge-order info (G-9), NOT NOT-TESTED-by-default. Heavy; the gate may skip it at the hard stop (stated NOT TESTED). Drop it if you prefer the lighter gate.
10. **Mail line**: the first line is cloned from B552 (question mail only if the key NAME is set); the B560 build brief said no mail. Keep or delete.
11. **Tier**: kept tier 1 per the B560 stamp ruling (1).

## UNMEASURED
Builder's runtime claims (counts, mutants, differential, red-first), the test files other than `PanelSectionMapCodeTests.cs` (names/sizes only), the real map and any real-book count, whether the stale slot was moved, CI outcome (all 7 checks still running), whether `d355620` exists in the clone, Jira state after the builder's read (not called), the builder's commission sha256 (RELAYED, gate re-measures).
