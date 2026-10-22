# B476 drafter report (read-only, 2026-10-22 19:41-19:55 AEDT)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-22_B476_SEAT-G42_hpsmpoc-b472-uatopen-gate-tier1.md` (49 lines, unstamped). Shape cloned from the B469 kit (every section: REFUSE, Stamp, Model/Step 0/Launch/Report, HOLD, CHECKS, SEVERITY/VERDICT, NOT TESTED, last line). Subject: B472 READY `e353322e`, tier 1, Opus, pane `Datasec/HPSM-POC-G42`, ports 8270-8279, round 1 of 2. Wrote only these two files. Ran no build, test, mutant, `az`, docker; no HTTP to a hosted site; no Jira write; git in the project: read verbs only (the legacy 3-arg `merge-tree` printed to stdout).

## Slot count with a control
- `/usr/bin/grep -c -E '_''_''_''_'` on the kit = **6 lines** (5 Stamp slots: Stamp time, Launch authority, Heads at stamp, Model receipt, Hard stop; plus the last line `READ-WHOLE-BY-TUESDAY: ____`). The REFUSE line in the kit says "the unstamped brief reads 6". Control: a scratch file `a____b` reads 1. The REFUSE text itself does not match (the pattern is split by quotes).
- `@[A-Z_]+@` count 0 (control: a scratch `x @AB_C@ y` reads 1). Person-name grep (`kamil|kreiser|Kam`) 0 after I replaced the GitHub login by "the project's GitHub account" (it read 1 before).
- Tuesday still owes: the stamp, the `.pre-stamp` copy beside the kit, the READ-WHOLE line.

## Measured (command -> outcome)
- `ls-remote origin` 19:41: main `d70f9dc13fdfbfb6e979b6d282737ccc58cd7600`; `b472/uatopen-refused-mint-at-run` `e353322e…` (= READY); b429 `4c02e8b9`, b460 `b9fd28ed`, b461 `52bd6e7c`, b462 `e8ecb8ae`, b465 `c65a5ab6`, b467 `3b2a8240`, b438 `c1a245f8`; no `b466*`, no `b476*` (control: the b472 line prints).
- The local clone holds both objects (`cat-file -t` commit for `d70f9dc1` and `e353322e`). `rev-list` main..head 1, head..main 0; `diff --stat`: 1 file, +19 -6 (`UatOpenTests.cs`, 615 -> 628 lines); `diff -- api/src` 0 bytes; commit trailer `Claude Sonnet 5.5` (builder Sonnet, gate Opus: they differ, unlike B469).
- `merge-tree` (legacy, base = main): 0 conflict markers; control: output holds `merged`/`result`. `compare` ahead 1 behind 0, 1 file; open PRs 0.
- Head line numbers: `Refused()` `:365`, rows `:377`/`:378`, `[MemberData]` `:393`, method `:394`, assert `:400`; main: `:355`, `:367`/`:368`, `:383`, `:384`, `:387`. Class `UatOpenAssertionTests` at main `:311`.
- **The assert line is not byte-equal.** At main it passes `assertion`; at head it passes `sent` (the run-time mint). The brief said "the assert as they are". The kit makes the gate state this exactly (status, method, call equal; the argument differs) and class it a Minor/Note. The `-` lines of the diff number exactly 6 (signature, `return new()`, two rows, method signature, assert): the kit asks for each to be accounted.
- Overlap of the one path with live branches by `gh api compare` GETs: b429 (43 files, control `web/src/instrumentation.ts` = 1), b460 (1), b461 (14), b462 (6), b465 (19), b467 (2), b438 (2): 0 each. **Two non-live branches list the path: `b409/uat-open-signin`, `b418/uat-template-drift`** (the builder's reading: squash-merged heads of #177/#178). I did not re-verify the PR merge dates; the kit makes the gate do so (check 9).
- B466 branch absent; its brief's Yours: `grep -c -i UatOpen` = 0.
- Jira GETs: `text ~ "UatOpenTests"` 0, `text ~ "UatOpen"` 0 (control `text ~ "assertion"` 10), `created >= "2026-10-22"` 0, `text ~ "JwtBearerRolePathTests"` 1 = HPSMPOC-122 (Done, the B68 forged-JWT matrix, not a defect ticket). So neither the defect nor the sibling has a ticket.
- Census sibling at main (read by `git show`): `JwtBearerHostFactory.cs:54` `var until = expires ?? DateTime.UtcNow.AddMinutes(30);`, `IssuedAt`/`NotBefore` = until - 31 min; `JwtBearerRolePathTests.cs:42` `SignedPartner`, `:45` `Rows` both `static readonly`, `Names()` `:84` reads `Rows.Keys` at discovery. `git grep -i ClockSkew` over `api` at main = 0 lines (control `TokenValidationParameters` hits in `Program.cs` and `EntraMetadataWarmup.cs`): so the default 5 min skew applies, **the drafter confirms the builder's reading of the code, not the library default**. Row expectations (200/403 become 401 at ~35 min) are from the builder's STATUS and my read of the `Rows` table.
- `UatOpenFixedClockFactory` (only a `TimeProvider` override in the Auth folder) is `UatOpenAssertionEdgeTests`'s, so `UatOpenAssertionTests` runs on the real clock: the run-time `UtcNow` mint is consistent with the host clock (the kit asks the gate to prove it by grep).
- Ports 8270-8279: 0 listeners (unfiltered `lsof` listed 25). The only `827x` text in the 2026-10-2x briefs is inside hex shas (control: `8260-8269`, `8240-8249` are named). `.tools/b476` absent (control `.tools/b198` exists). Load1 at 19:42-19:43: 31.4 and 25.0 (very busy; the kit tells the gate to wait and do light work). `.tools/.git-lock` exists as an entry at 19:4x (not opened).
- Model: `levels.opus.model_id` = `claude-opus-5-5`; G1 text at `model-routing.md:108`, G2 (`:109`) lists "tests-only" as tier 2, which the kit says honestly while following B472's own tier-1 ruling.

## What the kit adds beyond the prompt's list (all attack the builder's claims)
- **Check 3 (iii)** the status-only assert means "same reason" cannot be read from the test: the gate must isolate the refusing clause per row with a scratch probe. **(v)** a time-row boundary table (no wait) showing the discovery-shape decay at 9 min 31 s and that the run-time shape never decays.
- **Check 4** a DIFFERENT delay instrument from the builder's (fixture-constructor sleep, which xunit runs after discovery, with an ordering proof by stamps) plus R-short (40 s, +50 s offset), R-ctl (0 s) and R-full (575 s, the real row, nothing shrunk).
- **Check 5** M1/M2/M3 as asked, plus an M3 ladder with predicted floors (expired row only notices `SkewSeconds` < 120; the future row < 600; predictions, not measured) and M4/M5 controls (drop the lifetime clauses) to show the untouched rows still bite.
- **Check 10** test-side mutants T1-T4 and a null/null guard probe. My prediction, unmeasured: **T2 (offset sign swapped) survives**, because both swapped tokens are still refused with 401. That would be a Minor, by design.
- **Check 8** a second census method (starting from minting helpers, not from time APIs) and a runtime measurement of the JwtBearer skew and the sibling's red set (shift `Sign`'s default to -6 min in a scratch tree), instead of quoting the library default.
- Locks as instructed: shared `.tools/.git-lock` for git ref writes only (copied `lock.sh`), seat-local `.tools/b476/heavy.lock` (`mkdir`) for every heavy job including the 575 s sleep.

## Unmeasured (nothing was built or run)
- Every red/green prediction in the kit: R-short/R-full, M1-M5, the ladder floors, T1-T4, the null/null guard, the per-row clause table, the boundary table, the sibling's red set and the 35 minute horizon.
- Whether `UatOpenAuthentication.Verify` is `public` or reachable by `InternalsVisibleTo` for the gate's direct probe (the kit gives the host route as the fallback).
- Whether `b409`/`b418` are only merged leftovers (relayed from the builder); #177/#178 merge dates.
- The required status contexts on `main` today (B469's kit read five; I did not re-read).
- Whether b466 will be pushed by the gate's start; `dotnet` on the gate's PATH.
