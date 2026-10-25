# B592 DRAFTER REPORT: NexusAI PR #106 tier-2 gate kit (SEAT-G83)

Drafted 2026-10-24 17:51-18:05 AEDT, read-only. Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-24_B592_SEAT-G83_nexusai-106-gate-tier2.md` (102 lines; byte-identical `.pre-stamp` copy, `cmp` equal). Stamp slots: 8 (7 slot lines plus the last line), all unfilled; control: `grep -c` of four underscores reads 8, a planted `a____b` line reads 1; `@X@` pattern 0; non-ASCII 0; no person's name.

## BLUF
1. **The kit is ready, but PR #106 is NOT green and GO is impossible at the moment of drafting.** `audit-production-deps` FAILED twice on the head (check-runs 120806042904 and 120806632481). The job log shows `body-parser` 2.3.0, advisory GHSA-27r3-jxmh-p828 (high, range `>=2.0.0 <2.4.0`). `package.json` and `package-lock.json` blobs are equal to main's (`384805d9`, `6949fffe`), and main's own last npm-audit run was green on 2026-10-22, so this looks like a NEW advisory against an unchanged lock, not the cell lane. The kit makes the gate prove that on main's own tree (Check 5) and caps the verdict at GO WITH FINDINGS with a named suffix. Clearing it (a dependency-only change) is Tuesday's call and is a precondition for landing under the C-190 required checks.
2. `build` and `Analyze (javascript-typescript)` were still in_progress at 17:52, so there is no JavaScript CodeQL analysis yet (python and actions: 0 results). The gate must not treat the 0 open alerts as clean.
3. The builder's account has a hole the kit sends the gate after: it says the `customer` singular cell stays green under M863-k and M871a because `customer` "is also a commonWords entry". The drafter finds `'customer'` once between server.js lines 8060-8200 (the `GROUP_NOUNS` line) and not in the `commonWords` array. The `customer` cell may be killed by no mutant. The kit asks for the real reason and an own-mutant probe.
4. The counts-file "+2 -2" is `_updated` (timestamp) and `tests` (4971 -> 5005); `suites` stays 305. The brief says so.

## What I read (whole unless noted)
B412 gate kit, B590 gate kit, B588 builder brief, B588 STATUS (last line READY FOR QA), model-routing.md lines 100-125 (row G2 at line 109), `brief_seat.sh` (head), CLARIFICATIONS C-190 (lines 2058-2075) and the C-68 grep hits, NexusAI CLAUDE.md by grep (verify rule, no gate rule that changes this), the `git diff` of rd476, rd863, rd857, rd774, rd603, rd778, the rd424 added-lines grep, the counts diff, `.github/workflows/npm-audit.yml` at head, the audit job log (GET), `pulls/106`, `pulls/67` and its files, check-runs for head and main, code-scanning analyses, `ls-remote`, the lock-tool sha256, `server.js` 8040-8200 at main, anchors by `git show 6a69fdf4:<path>` greps.

## Decisions Tuesday must confirm at the stamp
1. **Audit red.** Confirm the rule I drafted: with Check 5b proving main's own tree fails the same advisory, the verdict is at most GO WITH FINDINGS ending `(CI red: audit-production-deps; base fact of main's own tree, not this lane)`; if main's tree passes and the head's does not, NO GO. Decide separately how the red clears before landing (a dependency-only lane or a ruling); the kit says it is not the gate's.
2. **Clones, not worktrees.** The request said "its own worktrees"; the NexusAI gate method (B412) forbids `git worktree add` in the shared repo (a ref write), so the kit uses `git clone --no-local` trees named `worktrees/b592-{base,head,mut}`. Confirm.
3. **Whole-suite names.** To save a 27-minute run, names are compared multiset-wise on the SEVEN touched files at base and head only (all other suite bytes and the product are identical by the tree diff), and the whole-suite total comes from the head's verify. A base verify is optional. Confirm.
4. **Hard stop.** Suggested target 2.5 h, hard stop 4.5 h from the gate's Step-0 `date` (about 17 named mutants on two files each, 4 own probes, one 27-minute verify). Edit if load (8.70 at 17:51) argues otherwise.
5. **Launch timing / pending checks.** The gate can start now, but `build` and the JavaScript analysis may still be pending; the kit waits up to about 40 minutes beyond its last hold and then writes the `(CI pending: ...)` suffix. Alternatively hold the launch until they finish.
6. **PR #67.** Kept as a NOTE (PRE-CLEARED at the builder stamp), as instructed.
7. **Receipt gauge.** Left in the slot for you to fill at launch; row id read as G2.

## Port block
**9440-9449.** `lsof -nP -iTCP:9300-9449 -sTCP:LISTEN` empty (rc 1). Word-boundary scan `(^|[^0-9])944[0-9]([^0-9]|$)` over 334 files `2026-10-23_*`/`2026-10-24_*`: 5 hits, 4 in B582 (hex id `a9446afd-...`, false positive) and 1 in the B590 drafter report (a scan-range sentence, not an allotment). Controls: `ports 9440-9449` matches, `x94400y` does not; the 93xx variant matches 60 files. The test harness reserves its own ports outside any block (RELAYED from the builder); the kit says to note it.

## Other facts worth knowing
- Head `303fb292` (ls-remote, refs/pull/106/head equal), main `6a69fdf4`, 0 behind / 9 ahead, +254 -4, 8 files, all `M`. Trailer on 9 of 9 commits. `mergeable_state` blocked (checks pending/red).
- Open PRs: #106 and #67 (#67 dirty, stale since 2026-10-07).
- `d5c516f`'s message overstates M871a by one cell (builder's own correction in STATUS); the kit makes it a Minor to measure.
- Existing cells whose environment changes without a removed line (rd863 `AI_RATE_LIMIT_MAX`, extra asks in three `beforeAll` blocks) are a named loosening check, plus a kill-set monotonicity program (old-name red sets old vs new under every mutant).

## UNMEASURED
No npm, jest, clone, worktree or mutant was run. Not measured by the drafter: that any cell is red under any mutant; that the head's full verify reads 5005/305 (the builder claims it); the real reason `customer` stays green; whether the audit advisory also fails on main's tree today (inferred from equal lock blobs and the advisory range, not run); the advisory's published date; the CodeQL result on the JavaScript analysis; the ordering of the rd424 file-write lines under CodeQL; the exact lines in `server.js` near `:1898` and `model-config.js:9` (RELAYED from the builder brief); the `.gitleaks.toml` invocation (RELAYED); node version on the gate seat versus CI node 24; the gauge value for the receipt line.
