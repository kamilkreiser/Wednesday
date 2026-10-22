# B481 drafter report (Sonnet, read-only), 2026-10-22 about 22:10-22:45 AEDT

Brief: `2026-10-22_B481_SEAT-R2_hpsmpoc-b467-testfix-round1.md` (108 lines) plus `.pre-stamp` (cmp equal). Fix round 1 of 2, TEST-ONLY, on `b467/hpsmpoc-187-204-words` @ `d6eba5f681372d409748e2e5023962b4157e0c81`; pane `Datasec/HPSM-POC-R2` (not in the live pane list: live are A1, G42, G44, G45, H5, W2); Sonnet C2; delta gate tier 2 after. Shape cloned from B480.

## Read
B477 STATUS (431 lines, whole), B480 `.pre-stamp` + drafter report, B467 ADDENDUM-1 (whole), B467 brief lines 1-40, gate evidence `api-head-seed-narratives.txt` and `probe-V3/V5/V6` files (read only). `git show d6eba5f6:` of `Providers.cs` :125-170, `NarrativeOutputValidator.cs` :170-190, `ShowcaseSeeder.cs` :225-255, `Hpsmpoc187GroupedSummaryTests.cs` :1-44 and :196-226 (+ test list), `ShowcaseSeedTests.cs` :165-200. Did not open `.tools/b477`.

## Item -> file:line map (head d6eba5f6)
| Finding | Item | Source | Test home |
|---|---|---|---|
| B477-1 MAJOR, V5 | 1 | `Providers.cs:163` kind guard | new rows in `Hpsmpoc187GroupedSummaryTests.cs` (weak row :218-225 stays unedited) |
| B477-2 MAJOR, seed | 2 | `ShowcaseSeeder.cs:240-246` (pipeline), :249-255 (row) | new `[Fact]` in `api/tests/HpsmPoc.Api.Tests/Assessment/ShowcaseSeedTests.cs` next to :172-194 |
| B477-3 MINOR, V3 | 3 | validator `:182` | new row beside `Row_c` (:206-216) |
| B477-4 MINOR, V6 | 4 | `Providers.cs:164` `g.Count > 1` (NOT the validator) | row or equivalence proof |
B477-5..8 are named in the brief as not in scope (Tuesday tickets them).

## Deviation to confirm (partition)
Item 2 cannot live in the Reporting project: the seeder and its factory are in `HpsmPoc.Api.Tests`, and `ShowcaseSeedTests.cs` is NOT one of b467's nine paths. The brief names it as the one file outside the nine, no new tracked file, at most 4 test paths. Overlap of the ShowcaseSeed trio (`ShowcaseSeedTests.cs`, `ShowcaseSeedDraftContentTests.cs`, `ShowcaseSeeder.cs`) with b461, b465, b466, b472, b429, b462: 0 each. It adds one Api-suite run to the builder (about 4 minutes, queue-serialised behind other seats' Api runs). Your call whether to accept it.

## Partition intersection (`git diff --name-only 1d1fa462...<sha>` vs b467's nine, 4695d7f2..d6eba5f6)
```
b461 53052201a968 n=14 shared=0
b465 c65a5ab667e7 n=19 shared=0
b466 3eded1128663 n=10 shared=0
b472 e353322e7094 n=1  shared=0
b429 4c02e8b94f19 n=43 shared=0
b462 e8ecb8ae5fca n=6  shared=0
planted control (one b467 path appended to the b466 list): 1
self control (b467 range vs its own nine): 9
ShowcaseSeed trio vs the same six lists: 0 each
```
b466 does touch `api/tests/HpsmPoc.Api.Tests/Assessment/Hpsmpoc178CustomerNameTests.cs` (same project, other file); b472 touches `Auth/UatOpenTests.cs`. Same-project, no shared file.

## Main vs branch
`merge-base d6eba5f6 1d1fa462` = `4695d7f2` (unchanged). `rev-list --left-right --count 1d1fa462...d6eba5f6` = `2 2` (main-only `d70f9dc1` #182, `1d1fa462` #183). Main-only paths since the fork: 7 (`ci.yml`, `RequestTimingLogTests.cs`, five Feedback.Tests files), none in Yours. I did not re-run the legacy `merge-tree` (the gate did: 0 markers at both mains, its marker control not built). Decision in the brief: NO main merge (default, as B480).

## Ports and locks
Block **8320-8329**. `grep -w '832[0-9]'` over all `tuesday/briefs/*.md` = no hit; controls: `831[0-9]` = 2 files (B480 itself); `825[0-9]` control = 7 files. 8290-8309 are taken (B478 and neighbours), 8280-8289 B477. `lsof -nP -iTCP:8320-8329 -sTCP:LISTEN` = empty (rc 1); positive bind control not run (builder does). Locks: copied `lock.sh` for ref writes; `.tools/b481/heavy.lock` for builds, tests, mutants; waitload from b267; the Api-suite rule (wait on other seats' live `HpsmPoc.Api.Tests` test processes, never break) is spelled out in line 9. The gate's own note that B478 waits on `api-run` holders: I did not find a file path for that queue in the briefs, so the brief says "by process", as the B477 brief did (ASSUMPTION).

## Other measurements
- Stamp slots `grep -c -E '_''_''_''_'` = 8; control `x____` = 1. Person-name grep (kam, kamil, kreiser) = 0. Card id = 0.
- `ls-remote`: main `1d1fa462`, b467 `d6eba5f6`, b465 `c65a5ab6`, b461 `53052201`, b466 `3eded112`, b472 `e353322e`; no `b481*`. `.tools/b481` absent; no `wt-b481-*`. `.tools/b198/lock.sh` and `.tools/b267/waitload.sh` exist.
- `records/b467` is on the analysis repo, not the code origin (ls-remote on the code origin shows none); I did not GET it. The brief makes the builder GET it and record it (expected `7d723d13…` from the gate).

## Assumptions (marked)
- The seeded sentence and titles in item 2 are copied from the gate's evidence (`api-head-seed-narratives.txt`), not re-measured. The narrative GET exposes `inputFindingIds` (F-001..F-007), not per-paragraph ids, so the pin is on text, with a fallback if titles are fragile.
- Constant name for the remediation kind and test-project visibility of `SharedActions` (internal) not checked; the brief tells the builder to read them.
- Item 4: V6 is at `Providers.cs:164`, not the validator (the gate's text blurs this). I gave a candidate killing-input recipe; I did not test it, and it may be impossible if the canonical JSON always carries a `1` (the brief allows a proof instead).
- Mutant list kept to V5, V3, V6, S (seed) plus V0 and V2 as regression kills; the other gate mutants need no re-run because nothing but added test rows moves (stated in the brief).
- PR-body paragraph is written by the builder (as asked), with a source check of `HostedDemoStartup.LookForCompleteSeedAsync`; I did not read that file.
- Flagged for you in the brief's FOR TUESDAY: the records entries C-144/C-145 cite code head `d6eba5f6`, which stops being the branch head after this push.
- Hard stop / target READY left to you at stamp.
