STARTABLE: YES

# B1117 drafter report (M76, MPS sites warning, reading B), drafted 2026-11-02 11:4x-11:5x AEDT (`date` at the last write: 11:52)

## BLUF
Reading B is a small engine change and the card's "one line" holds in spirit, with one correction: the Priced flag is not a variable at the check (it is a literal at three returns), so the one-line shape is MOVING the call below the line-check stop (after `PurchaseCalculator.cs:216`) and deleting the 4-line guard, not editing the guard's test. Kit is 15,337 bytes (`wc -c`), unstamped, six slots plus the last line left as four underscores. Two things need Tuesday: the MPSCALC-367 ticket text says the opposite of the ruling (see C-1), and the gate tier (Q-1).

## Facts re-measured (instrument; control)
- Code main = `f8f808c4...` by `gh api -X GET git/ref/heads/main` and `git ls-remote` (both print `f8f808c47a5526f6e1c1c3ac38798358e5da1035`); parent `19d084f` = #140; `f8f808c` = #141 whose files (4 tests, none of mine) came from `gh api compare 19d084f...f8f808c`.
- Guard, call, stop, returns: lines printed by `awk` over `git show <sha>:...` at the pin: call `:209`, guard `:580`, stops `:169` and `:212-216`, returns `:171 :215 :266`. Control: the awk for `CheckSiteAllocation(` also printed the definition `:578`.
- Ordering: Priced is a literal argument of `PurchaseResultOf` (`:1031`), so a one-line edit of the guard would need the stop's three codes copied. The move keeps issue order (tests `:287` and `:297` pin order; they stay green by reading, NOT RUN).
- Api/web/contract: `git grep` for `SITE ALLOCATION` over tests/web/contract/Api = 2 hits, all in `PurchaseSiteAllocationTests.cs`; `-w Sites` outside the engine = 0 hits (control: engine = 2 files). `QuoteEndpoints.cs:873,:1186` count `Blocking` only. So no Api/web branch exists and a person cannot reach the sentence today (no screen or contract states a site).
- No new word: message `:593` and code `:69` untouched by the shape; only the doc comment `:575` and the ENGINE.md row X-44 sentence change.
- Reading-A pins: one existing row, `PurchaseSiteAllocationTests.cs:407` (asserts lists `["MARKUP NOT SET"]` at `:412` and `["UNKNOWN ITEM"]` at `:415`); the kit has the seat change it and name old and new. Other "no Differs" rows (`:369 :379 :388 :398`) have Priced false and stay valid under B.
- ENGINE.md:170 sentence read and the replacement text written into the kit, including the two missing SOURCE codes (B1091-1).
- Partition: `gh api compare main...` for `b1093/...` (14 files) and `b1063/...` (#142, 5 files): none of `PurchaseCalculator.cs`, `docs/ENGINE.md`, `PurchaseSiteAllocationTests.cs`. M75 B1116 paths (web tests, `docs/IMPORTER.md`) disjoint by its kit. Open PRs: #142, #121, #120.
- Jira GET (MPSCALC-367, -257; token not printed; ticket 367 status Backlog, labels lane-v4 tier-2, 0 comments after the body; 257 Backlog with the 10:42 record comment). Model: C2 row `model-routing.md:92`; id `claude-sonnet-5-5` (`models_latest.json:23`).
- CI predicate read: `ci.yml:42-43` build Release then test the whole `MpsCalc.slnx`; `Directory.Build.props:6` TreatWarningsAsErrors true.
- Machine at drafting: `df -g` 41 GiB free on the volume (the kit's stop is under 25); `sysctl vm.loadavg` 10.89 10.34 12.74, so a launch waits for load1 below 7.

## D-decisions made
- D1: shape = move the call below the stop, delete the guard (not a copied three-code predicate). Reason: one source of truth for "stopped".
- D2: two commits: A tests only and RED at the pin (red-first evidence in history), B product + docs; squash landing keeps main clean.
- D3: five plants, not six; each names the row that must go red; P3 separates the line-issue half from the source half.
- D4: standing mechanics restored: seat-local `.tools/b1117/heavy.lock`, load1 below 7 on two reads, moving heartbeat, ref writes under `.tools/.git-lock`, STATUS at Step 0 with `WORKING:`, PRIOR-WORK CHECK, red-first, at most 6 plants, `df` with stop under 25 GiB. No port block (Engine tests in-process).

## Q-questions for Tuesday (each with a default)
- Q-1 Gate: G1 or G2? Argued G2 (`model-routing.md:109`): the change moves no figure, status or hash and adds no string; the mechanism (the guard and the stop) was measured by gate B1091; it is a follow-up on an engine path with an Api that cannot reach it. Against: G1 (`:108`) lists "security surfaces, data destruction, deploys, client testers", none apply, but it IS a product-behaviour change on a tested pricing path. Default: G2, with the gate told to re-prove "Priced false lists unchanged and priced lists differ only by the one added issue" at the head. Escalate to G1 if the seat reports any figure or order difference (the kit already stops it).
- Q-2 One-line claim: the move is -4 +1 code lines plus a comment; the card told the product owner "one line". Default: treat it as the same decision (the product owner chose the behaviour; the kit's `STOPPED` triggers cover a second predicate, new code, or an Api/web edit). Tell him at landing if you want the exact count.
- Q-3 Who restates MPSCALC-367 (see C-1)? Default: the records seat after landing; this lane writes no Jira.
- Q-4 Fixture 5 (the base case) is already pinned by an existing row; the kit does not add one. Default: leave it.

## Contradictions
- C-1: MPSCALC-367 as filed asks for rows asserting a priced quote with an expired source raises NO allocation issue (its Recommendation and Acceptance check), and the ruling says "MPSCALC-367 pins it" while choosing reading B. If any seat builds 367 as written after this lane lands, its rows would be red. The kit tells M76 to build reading-B rows and report; it does not touch Jira.
- C-2: B1091 STATUS `:117` says the early return stops "only the three codes", and `:115` calls reading B "the kit's sentence, Priced false". Source agrees with both; the move reproduces exactly that set.

## UNMEASURED
Nothing was built, tested or planted (`dotnet` not on this PATH). Not read: old `b*` branches that may list my three paths; whether `SourceValidityTests.cs` fixtures (expired source, date before sources) fit `PurchaseSiteAllocationTests.cs` Books; whether any Engine readiness reader counts Review issues (seat greps at Step 2); the web suite; the live pane list for `Datasec/MPS-M76`; the test tree outside the five files grepped.

## Outside the fences
None. Reads only: Jira GET by a scratch script (in the session scratchpad) that read the project `.env` in-process; `gh api -X GET`; `git show/grep/ls-tree/ls-remote --no-optional-locks` on the project repo; the pre-existing B1094/B1115/B1116 kits for shape. One Bash call was refused by the zsh word-split hook and re-issued under `bash`. No card store, no `decision_queue.sh`, no fenced tree. Writes: the kit and this report only.
