# B479 drafter report (2026-10-22 21:0x AEDT, read-only)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-22_B479_SEAT-G45_hpsmpoc-b461-delta-regate-round2.md` (24995 bytes, shaped from the B468 round-1 gate and the B478 HOLD wording; it defers the E1-E22/S1-S2 anchors and the Standing paragraph to the B468 kit by path).

## Measured (GET and read verbs only)
- ls-remote: main `1d1fa462`, b461 `53052201` (= READY, commit object present), b465 `c65a5ab6`, b429 `4c02e8b9`, b459 `26460869`, b460 `b9fd28ed`, b462 `e8ecb8ae`, b466 `3eded112`, b467 `d6eba5f6`, b472 `e353322e`; no `b479*` ref.
- `rev-list --count 52bd6e7c..53052201` = 2, reverse 0. `rev-list --left-right --count 1d1fa462...53052201` = 3 / 3: b461 is 3 commits behind main (`4695d7f2` #181, `d70f9dc1` #182, `1d1fa462` #183). Main-only paths: 9 (including `ci.yml`), 0 among the 14. Legacy 3-arg `merge-tree a93b926 1d1fa462 53052201` = 0 conflict lines (control: a line with `<<<<<<<` read 1).
- Delta numstat = the 6 files in the brief, exact. 31 minus lines (1+1+1+26+2). Added skip-family lines 0. Added `it(` rows 24 (35 -> 59). Both commits carry the Sonnet 5.5 trailer.
- Overlap of the 14 by `gh api compare` + `grep -c -x -F -f`: b429 (43 files) / b465 (19) / b466 (10) / b467 (9) / b472 (1) / b462 (6) / b460 (1) / b459 (2): all 0; control: the b429 list holds `web/src/instrumentation.ts` (1).
- Open PRs: 1 (#184, a dependabot vitest bump, `web/package.json` + lock, outside the 14). Check-runs on the head 0. Required contexts unchanged (five).
- `:155` of the action-plan spec reads `"Home"` with a trailing comment naming the merge order; `Partner Dashboard` in the ten live specs: 0. B465 is diverged from main (not landed).
- Ports 8300-8309: 0 listeners (rc 1). `.tools/b479` absent. `levels.sonnet.model_id` reads `claude-sonnet-5-5`. load1 7.12 at 21:02. An Api-suite `dotnet test` of another seat (`wt-b471-mut`) was in `ps` at 21:05.
- Anchor counts at the head (`git show | grep -c -F`): E1, E2, E4, E6-E8, E10-E21, S1 and the 20 new-mutant anchors N1-N20 count 1. See corrections for the three that do not.

## Corrections to the request and to the round-1 kit
1. E3 anchor moved: `if (read.mode === "unreadable")` is 0 at the head; it reads `if (read.mode === "unreadable" && read.probed !== false)`.
2. E5 (`if (extra.length) out.push`) and E9 (`if (!hasBuild) out.push`) now occur twice (`liveApiRefusals` plus the new `orderCheckRefusals`), so the round-1 anchors would hit the wrong copy; the kit tells the gate to disambiguate and adds E5b/E9b.
3. S2 must remove the whole `test.skip(...)` statement (the builder's first S2 only commented it out and was weak).
4. The unit file and `--check-shards` read `.github/workflows/ci.yml`, which main changed in #183: the kit adds a `-merge` worktree (main + head) for the suites, which the request did not name explicitly.
5. B465 is not on main, so the live action-plan spec would fail at `:155` on a plain head build; the kit has the live runs apply B465's `web/src` inside `-merge` only (uncommitted), mirroring what the builder did, and says so.
6. Open PR #184 (not in the request) is recorded as a Note.
7. I could not verify the "20:24" time of #183 (no timestamp read); the kit names the three behind-commits by sha only.

## Slot count (kit)
`grep -c -E '_''_''_''_'` on the kit = 6 (the five Stamp slots and the last line `READ-WHOLE-BY-TUESDAY: ____`). Control: a scratch file holding four underscores reads 1. `grep -o -E '@[A-Z_]+@' | wc -l` = 0; control: a scratch file `@AB_C@` reads 1. Zero occurrences of a person's name.

## Unmeasured
Nothing was run: no test, build, API, browser or HTTP beyond `gh api` GETs and `ls-remote`. `dotnet --version`, Playwright version, node on the gate seat, the live behaviour of the new `checkDefaultCaller` against shapes A-F, and the 24 new rows' mutant coverage are the gate's to measure. Jira was not read (the kit needs no ticket text; the Done-when (a) clause is judged from the round-1 STATUS). Load at the gate's start is unknown.
