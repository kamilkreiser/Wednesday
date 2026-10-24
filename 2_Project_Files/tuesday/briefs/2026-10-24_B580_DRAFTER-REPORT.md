# B580 DRAFTER REPORT (Sonnet drafter for Tuesday)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-24_B580_SEAT-G79_mps-104-delta-gate-round2-tier2.md` (81 lines, tier-2 delta gate, round 2 of 2 = the cap, MPS PR #104). Unstamped copy: the same path plus `.pre-stamp`, `cmp` rc 0. Template: the B576 kit (read whole); round-1 report B562 (read whole, lines 1-509); fix-round brief B574 and its STATUS (read whole). I launched nothing, committed nothing, posted nothing, wrote only the kit, its `.pre-stamp` copy and this report.

## Measured by me (read-only, 24 Oct 12:01-12:06 AEDT by `date`)
- `ls-remote origin`: `b560/mps-importer-source-version-pins` = `refs/pull/104/head` = `006677b1c64e1800a087d41627ee3b9312e7e839`; main `a5b4bbb5d377f29dd63bf0c64d54b44c122a6055`; `refs/pull/104/merge` = `7419dec27df76a4f9543a1e71bb04ce0841549f2`, parents (GET `git/commits/<sha>`) main and the head.
- `pulls/104`: open, draft false, mergeable true, `clean`, 10 commits, 7 changed files. Open PRs: #106, #105, #104, #102. `pulls/104/files`: the 7 paths named in the kit (docs, `SynnexBook.cs`, `PriceBookImporter.cs`, 4 test files).
- `compare/655606a9...006677b1`: ahead 3, behind 0; docs 1/1, Api tab file 14/0, panel file 84/0, supply file 16/0; commits `84987ea`, `7c97587`, `006677b` chained by parent; trailer present on all three (`git log --format` trailers). `git diff 655606a 006677b --stat -- src` output 0 bytes. Docs hunk header `@@ -127 +127 @@`. `git show 006677b:docs/IMPORTER.md`: the phrase `a SKU listed on several sheets` 0, at `655606a` 1.
- Anchors at the head (`grep -n -F` of `git show`): `PriceBookImporter.cs:660` (join), `SourceDocumentChecks.cs:132`, `ReferenceDocumentValidator.cs:211`, one hit each. New row lines: panel 211, 222, 236; Api tab 79; supply row in the `+65,16` hunk (its method name `An_included_supply_priced_one_decimal_step_below_zero_...` from the diff). Added-line names from `git diff -U0`: 5 `[Fact]` rows. The panel file also holds `SecondDevice = "SYN-A3B"`, `CaseTwin = "syn-a3"` and a Price List row at `B24` (read from the head).
- Check-runs on the head: 9 listed, all `completed` `success`; `code-scanning/alerts?...state=open` length 0; `analyses?ref=refs/pull/104/head` has csharp, javascript-typescript, python, actions at `006677b` with `results_count` 0 and empty error.
- Panes (`tmux`): `tuesday`, `Datasec/MPS-M13`, `Datasec/MPS-G77`, `Datasec/MPS-G76`, `fleet-monitor`. No pane named for G79.
- Ports: `lsof -nP -iTCP:9300-9399 -sTCP:LISTEN` empty (rc 1). Word-boundary scan `(^|[^0-9])930[0-9]([^0-9]|$)` over `briefs/2026-10-23_*` and `2026-10-24_*`: 0 files; the same scan for `931`, `934`, `936`, `937` and `939` hits other files (hash-like text, not ports of mine); control the scan for `926[0-9]` lists the B576 files. **Port block chosen: 9300-9309** (first free 10-block from 9300; the blocks 9230-9239 and 9260-9299 are allotted per the commission).
- `refs/heads/b580*` on origin: 0 (control `refs/heads/b56*` lists b560, b561, b565). `.tools/b580` absent (control `.tools/b576` lists).
- Heavy slots at 12:01-12:02: slot-1 `B575 12:01:52 forced`, slot-2 `B576 12:02:00 job3-Rc-posinf2`, slot-3 directory present with no holder file (the kit says report, never take over).

## Kit facts
- Slot lines: 9 (8 labelled slot lines plus the last line `READ-WHOLE-BY-TUESDAY: ____`), every one ending with the four underscores (a line-end pattern counted 9; the other pattern counted 9; control scratch line `x____y` reads 1). Hint text sits before each slot, none after. The REFUSE and Stamp prose contain no four-underscore run elsewhere.
- At-sign pattern count 0; non-ASCII lines 0; person-name scan (4 name words) 0; no card id; ticket keys appear only as the pattern `MPSCALC-n` and the Jira JQL prefix, as in the template; sha256 of the kit `84dd843fe3ebc3ce58640753a0ec68f56ad2ce8c86f38767afa41cbb08f802e4`.
- Launch line as B576 with `Datasec/MPS-G79`, `BRIEF_SEAT_LEVEL=sonnet` and the new brief path. IDs: B580, SEAT-G79, `.tools/b580`, `.tools/wt-b580-*`. Hard stop line: target verdict 2 h, hard stop 3 h after launch, relative to the seat's Step-0 `date`.

## Shape choices worth Tuesday's eye
- Nine checks like B576: delta and hygiene (3 commits, 4 paths, +115 -1, test files additions only, docs fence differs from B576 because the docs line is allowed), docs deletion by a word-level subsequence program, rows green at head and red-or-green-by-design at main's source (with predictions written first), the mutant re-run with a closure test per finding (B562-1 needs P8 and P9 dead on NEW rows only, B562-2 P16, B562-3 V1e-V1g plus the finer V1h, V1i, B562-4 W5, B562-5 clause gone and nothing added), a differential with seed 580101 and a Python oracle with P8, P9, P16 power controls, the CI line on `refs/pull/104/merge`, check-runs and CodeQL, path intersection, scope and process.
- The kit adds neighbours (P1, P2, P3, P7, P12, P15, W2, W6, W7, W3, P11 equivalents, V1b, V1c) so the gate sees the new rows weakened no old killer; a tier-2 seat may sample them if load is high, the must-check set is the 7 survivors plus W1.
- The landing rule is stated in Check 7 (g): squash with `--match-head-commit 006677b1...`, no brief number or finding id in the squash message; the gate does not merge.
- Seat-set statement of severity keeps round 1's grading (Majors B562-1 and -2, Minors B562-3..-5) and the cap statement.
- Escalation to tier 1 includes: a docs hunk beyond line 127 or any added word, a changed test line, a new row whose book does not import or whose Warning count differs from the builder's.

## Not measured (no build, test, mutant or probe was run by me)
Every .NET count, the five rows' behaviour, mutant outcomes, the differential, the docs word counts (17 removed, 0 added are the builder's, marked RELAYED), the red-at-main predictions (taken from the builder's differential, RELAYED), load1. The fix-round brief B574 file was listed (`ls`) and read whole.

## Things I noticed
- The panel-file additions hold device and price literals the builder declares invented; the kit makes the gate list every decimal literal by program.
- The B574 STATUS says "18" new rows in round 1 and "5" in round 2; the kit relies on the 5 (measured: 5 `[Fact]` lines added by the diff).
- Slot-3 has no readable holder at this moment; Tuesday may want to check it is not a leftover.

## Fences kept
Wrote only the kit, its `.pre-stamp` copy and this report. No Artifact/Docs/mail/chat tool, no decision-queue tool, no Jira call, no HTTP to a hosted site; `gh` GETs only under the project's `GH_CONFIG_DIR`; git in the MPS repo: `ls-remote`, `show`, `diff`, `log`, `ls-tree`, `cat-file` only. No `cd`. No background job running.
