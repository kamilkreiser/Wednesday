# B590 DRAFTER REPORT (SEAT-G81, HPSM-POC tier-2 gate kit for `b586/hpsmpoc-test-followups-p1-p4`)

Drafted 2026-10-24 16:19-16:30 AEDT, read-only.

## BLUF
The kit is written: `2026-10-24_B590_SEAT-G81_hpsmpoc-b586-gate-tier2.md` (98 lines) with a byte-identical `.pre-stamp` (`cmp` clean). It has 8 lines with the four-underscore pattern (7 slots + the last line), 0 `@[A-Z_]+@` matches, 0 non-ASCII bytes, no person name, no sample client name, no decision-card id. Port block **9420-9429**. Model row **G2**. Two things Tuesday should know before stamping: (1) with no PR the gate cannot see CI or SQL Server, so the kit caps the verdict at GO WITH FINDINGS; (2) the builder's per-file numstat figures are wrong (its total is right).

## What I read
- Whole: the B578 gate kit (both pages, lines 1-116), its ADDENDUM-1, the builder brief B586 (138 lines), the builder STATUS B586 (170 lines).
- `fleet/specs/model-routing.md` row G2 (line 109), the project `CLAUDE.md` (lines 34-51) and a grep of `CLARIFICATIONS.md` for gate/merge/test rules (no rule found that changes this gate; the kit tells the gate to read it and say so).
- Measured: `gh api compare` (ahead 2, behind 0, 4 files), `ls-remote` (head `4839fb4f...`, main `0e631d75...`, no `b590*`), open PRs 0, check-runs on the head 0, local `git diff --numstat` and `-U0` hunk headers, the added hunks of 3 of the 4 files in full, the 3d and scanner rows of the runner test by line, `HasMaxLength(120)` at `AssessmentDbContext.cs:137`, `lsof` on 9300-9479, tmux panes, load.

## Decisions Tuesday must confirm at the stamp
1. **Verdict cap with no PR.** The kit says: at most GO WITH FINDINGS while there is no PR (no CI, no CodeQL, no SQL Server shard), GO only if a PR with green shards exists at verdict time. Confirm, or say the gate should wait for the PR.
2. **Hard stop.** Suggested target verdict 2 h, hard stop 3.5 h after Step 0 (about 45 web mutants plus about 15 Api builds). Your call; I wrote it as a suggestion in the slot label.
3. **Load rule.** Written as load1 below 8 (your instruction), not 7. Load was 7.13 at 16:20, so a waiter is likely.
4. **Port block.** See below; confirm 9420-9429 is still free at the stamp.
5. **Optional Jira GET** (project = HPSMPOC AND ..., zero control) is allowed to the gate as in B578; strike it if you want the gate Jira-free.
6. **Whole Api project run** and `npm run build` are marked OPTIONAL; the affected Api classes and the whole web suite are mandatory. Repeats: 10 per pool (builder claims 50).
7. **Gauge** in the receipt line is left as `<n>%` for you.
8. If a PR for this head is opened before the gate finishes, the kit makes the gate read it (GET only) and judge shards and CodeQL; it never waits more than 30 minutes while idle.

## Port block and how chosen
`lsof -nP -iTCP:9300-9419 -sTCP:LISTEN`, `9420-9429`, `9430-9479` all printed nothing (rc 1). Word-boundary scan `(^|[^0-9])942[0-9]([^0-9]|$)` over the 327 `2026-10-23_*` and `2026-10-24_*` files in `tuesday/briefs/` matched only the NexusAI test-cells brief B588 (seat brief, `.pre-` copies, drafter report), whose text says "9400 to 9429 ... 0 lines" as a scan range; B588's own block is 9410-9419. So 942x is not allotted; control `ports 9420-9429` counts 1. Blocks 9300-9419 are allotted today (as you stated). Other hits in the 94xx range (9431, 9446, 9459, 9466) are hex/uuid fragments (B582 lines 75-76, 111 seen), not ports; I did not exhaustively classify 9459/9466.

## Findings the drafter made (relayed into the kit as facts or checks)
- Builder STATUS per-file stats (14/2, 22/0, 15/0, 84/6) do not match the measured 15/2, 24/0, 16/0, 87/6; total +142 -8 matches.
- The 8 removed lines are mapped to hunks: 2 comment lines, 4 regex lines (3a, 3c), 2 `bodyOf` lines (3b).
- The builder writes the held-name constant as "33 characters plus 4 edge spaces"; my count of the literal is 27 UTF-16 units. Either way far below 120. The gate recounts.
- The raw-text source-text rows (:754, :757, :842 at head) still read the unstripped function text, so a comment holding the call may satisfy them; the kit asks the gate to measure that (Minor/pre-existing unless this branch worsened it).
- The mapping of the new runner rows: 3d at head :829, scanner at :857, its self-test row at :912, order row at :922.

## UNMEASURED
Everything that needs a run: suite and class counts, red-first claims, mutants, lint, typecheck, the Api build, SQL Server behaviour of the 2 new Api cases, CI and CodeQL on this head (none exists), the scanner's equality with a real parser, whether the 3a/3c patterns accept anything beyond whitespace and one trailing comma (reasoned only), the main-branch SQL Server shard log content. I read the Api `Plant` helper's body and `Requests.cs:140-150` not at all; the kit makes the gate read them. Hunks of `e2e-runner.test.ts` were read by header and by grep, not whole. I did not read the older gate STATUS files (B476...B572); the kit names them for the gate.
