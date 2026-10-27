STARTABLE: YES (after you stamp the seven slots; the heavy slots and load are a wait, not a blocker: load1 7.80 and two of three slots held at the read)

# B829 drafter report: gate kit for PR #129 (MPS walk-cap row g07), seat G176, tier 2

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-27_B829_SEAT-G176_mps-129-walk-cap-row-gate-tier2.md` (73 lines; `.pre-stamp` copy beside it, `cmp` equal; four-underscore line count 8, `@X@` count 0, non-ASCII 0). Drafted 14:25 to 14:32 AEDT (clock `date`).

## BLUF
- Gates PR #129 head `09cea7de42baa9d1fc6d42deafefd2147c220d95` on main `32b09108a5c476249498d22229debe3e73c8a5d6`, Sonnet, tier 2 (row G2 `model-routing.md:109`; G-cap `:111`), round 1 of 2, ports 9530-9539, pane `Datasec/MPS-G176`, `BRIEF_SEAT_LEVEL=sonnet`, `WED_USAGE_STOP=100`.
- **The discrepancy is settled by the drafter's reading, and the kit makes the gate prove it.** The diff has ONE `[Fact]`. `QuoteApiTestsUnderEntra.cs:10` is `public sealed class QuoteApiTestsUnderEntra : QuoteApiTests`, so each `[Fact]` of the partial class lists twice (QuoteApiTests and QuoteApiTestsUnderEntra). The builder's STATUS body says "1 [Fact] = 2 names"; only the READY line says "rows added 2". The kit grades it a Note if static count, `--list-tests` multiset diff and trx agree (1 source row, exactly 2 listed names, 3158 -> 3160), a Major only if the listed delta is not those two names.
- Heart (Check 2): the gate writes its own g07 mutants (Distinct before the Take, after the Take, DistinctBy on the name, tuple-level Distinct), plus reach mutants (control walk removed, repeat walk removed, cap 20 -> 2, one character of the sentence) so the row is shown to reach the check it is named for; Pass A (base test file GREEN under g07) and Pass B (head file RED, first failing assertion `Assert.Equal(expected, Errors(b))`).
- CodeQL is NOT done at the read: `CodeQL` completed `neutral` (a placeholder), `Analyze (python)` and `Analyze (actions)` success, `Analyze (csharp)` and `Analyze (javascript-typescript)` in progress, dotnet/web/python jobs in progress, `code-scanning/analyses` length 2. Check 8 WAITS (60 s polls, 40 min cap) and never dismisses or re-runs.

## Q-n questions (stamp decisions; defaults given)
- **Q-1 round count.** The walk-cap class reached its cap twice earlier (B678 first line "NO GO round 2 of 2" on PR #112; B763 "NO GO round 2 of 2" on b745, landed as #127). The kit counts this PR as round 1 of 2 only by the coordinator's 13:0x ruling recorded in the B821 builder kit. Default: accept, with the cap sentence in ROUND COUNT. Confirm at the stamp.
- **Q-2 grading of "rows added 2".** Default in the kit: Note if the measurement agrees (wording slip: names, not rows). Say so at the stamp if you want it a Minor.
- **Q-3 PR text.** The PR body names the ticket key MPSCALC-355 and ends with "CodeQL and the checks on this head are pending" (stale at landing); the title differs from the commit subject. The kit grades these Notes for your edit before landing (the squash uses the commit message under the repo flags per the #128 gate; the gate re-reads the flags). Default: accept.
- **Q-4 cw-weak wording.** The builder disclosed that its kit's cw-weak sentence cannot hold if an exact count is kept (count 4 vs 3 is red under g07). The kit asks the gate to run both scratch copies and state which assertion is decisive. Default: yes.
- **Q-5 retained-kill scope.** Tier 2 asks 3 of the six committed kills re-made (g01, g04, g06) against the head file and does NOT re-run the lineage's five equivalents. Default: accept; strike Check 5 if you want the cheaper gate.

## UNMEASURED (by me)
No build, test, mutant or C# compile ran. Not measured: the builder's 3158 and 3160 counts, the 92 `~WalkCap` names, the 1537-test family under g07, the row GREEN at main, the row RED under g07 (all RELAYED from the builder STATUS); whether my four mutants m1-m4 each compile at 0 warnings and each redden the row (m4's tuple equality is a prediction from the source: the two `fleet[1].site` tuples share name and control value); whether m5/m7 compile as written; the cross-control `sectionIdListed` edit; the hosted run beyond the 14:26 reads; the head's `mergeable_state` once checks finish (it read `blocked` at 14:26); the pull ref `refs/pull/129/merge` object (not in the shared repo at the read); load at launch.

## Facts relied on but not read at source
- The B821 builder kit's 13:0x ruling text on the round count is read from the builder kit, not from the wave-1 common file.
- Slots 1 and 2 are held by B819 and B820 (RELAYED from the builder STATUS); I listed the slot directory names only, not their holder files.
- M40's and M44's "Yours" paths and ports are read from their kits' lines (B819 line 26; B820 line 28 and the Ports line); I did not read their STATUS files or trees.
- Live-lane branch absence for b819/b820 is the builder's 14:21 read; my `ls-remote 'refs/heads/b82*'` at 14:2x printed only the b821 branch (so no b819 or b820 branch existed then).
- The 60-of-274 GATE VERDICT census and the hit list were read from first lines only (loop over `Briefs/*_STATUS.md`); the two B678/B763 quotes are first lines, not bodies.
- Model id `claude-sonnet-5-5` read from `models_latest.json` (`levels.sonnet.model_id`) at 14:2x; row text of G2 and G-cap read by `sed -n 109p`/`111p` (first characters only).
- The landing rule line numbers (744, 774, 809, 829, 854) are from a `grep -n -i -F 'landing rule'` before the final records append; they may drift.
- The hunk shape of the diff is read from the 20-line diff in full (one hunk `@@ -733,4 +733,17 @@`); the local numstat `13 0`, rev-list `0 1`, tree `a9e75936...`, and zero non-ASCII added bytes (no planted control run by me) are drafter reads.

## Read
B821 builder kit (102 lines) and STATUS whole; B794 MPS tier-2 gate kit whole (shape for C1-C9, heavy slot, load rule, stamp slots, verdict form) and B828 kit head, drafter report and stamp block (tier-2 weight); `QuoteWalkCaps.cs` at main (helper lines 127-182) and the head diff; `QuoteEndpoints.cs` lines 1425-1456 at main; the PR #129 object, body, diff, compare, commit, check-runs, runs and code-scanning analyses (GET); `git cat-file`, `rev-parse`, `rev-list`, `grep`, `ls-remote` in the shared repo (read verbs); project `CLAUDE.md` Rules and the landing-rule grep; M40 and M44 kit lines for Yours/Ports; `tmux list-panes`, `lsof`, `uptime`, a python word-boundary scan of 124 SEAT kits for 953x and for `G176`/`B829`; `ls -a .tools`.
First line of STATUS: `GATE VERDICT B829: PR #129 b821/mps-walk-cap-rows <GO|GO WITH FINDINGS|NO GO> @ 09cea7d (round 1 of 2 ...)` (the full form is in the kit).
