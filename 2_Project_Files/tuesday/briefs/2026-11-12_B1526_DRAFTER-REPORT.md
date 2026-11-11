STARTABLE: YES (after the Stamp; six slots and the last line are four underscores, 7 matches by `grep -c`, control: kit has no `@X@` tokens, 0)

# B1526 drafter report (2026-11-12, about 06:00-06:06 AEDT by `date`)

## BLUF
Kit for SEAT-M125, MPSCALC-388: measure each row's failure rate on main under load first, find the cause, then fix test-side (G2) or product-side (G1, new red-before-green row). Acceptance is the ticket's: 20 whole-suite runs at load above 7, load printed, no assertion weakened. Model: C2 Sonnet (`model-routing.md:92`), id `claude-sonnet-5-5` (`models_latest.json` lines 23, 38). Not C3: a feedback limiter's counting is not an auth, credential, security or money design surface.

## Facts re-measured
- Main `baf0aabec3c02457072ee848b166b17d3d7b0e80` (`gh api -X GET .../branches/main`); the red hosted run was main `37656d8a`, so main has moved.
- Ticket MPSCALC-388 read whole by GET (copy `fleet/state/s270/draft1526/MPSCALC-388.txt`). It states the cause of neither row is measured.
- Row 1 log (`main37656d8a_dotnet.log` lines 228-238): Expected 20, Actual 18, `FeedbackRateLimitTests.cs:73`, 213 ms. Only the assertion is logged; the other answers' status codes are not.
- Source at `baf0aabe` (saved in the scratch folder): limiter check and slot reservation are inside one `lock (_lock)` (`FeedbackStore.cs:603`, count at `:616`); item write is under the same lock with a unique temp name (`QuoteFileStore.cs:309`); an IOException or UnauthorizedAccessException on write returns `WriteFailed` and releases the reservation (`FeedbackStore.cs:646-658`), mapped to 503 at `FeedbackEndpoints.cs:226-228`. Row 2: test line 250 is the final `CalculateSources` on the host, `:251` closes `using var host`.
- Side SDK dir `.tools/dotnet-10.0.404` exists (`ls -d`). `lsof` 9810-9819: 0 rows (control: 11 listeners machine-wide). Non-`.pre-` SEAT kits of 11 and 12 Nov: 0 files name 9810-9819 (control finds 9730 in B1521). No `heavy` lock directory under `.tools` at drafting.

## D-decisions
- D1: model row C2 Sonnet; gate tier is a Stamp slot (G2 test-side, G1 if any product byte changes), set by Tuesday from the seat's `## CHANGE`.
- D2: kit puts measurement (30 runs per class, 100 for row 1 if unreproduced, under busy-loop load) BEFORE any cause claim; an unreproduced row is stated as such.
- D3: READY target 150 minutes (20 whole suites at about 6.5 min each dominate); a partial count is `PARTIAL n of 20`, never READY.
- D4: the commit subject may end `(MPSCALC-388)` (house style, as B1521); added code lines carry no key.
- D5: CodeQL pre-scan lists a C# row set with planted controls, stated as a property first.

## Q-questions for Tuesday
- Q1: Is 20 sequential whole-suite runs (about 2.5 hours of heavy slots) acceptable, or should the seat run them two at a time in both slots? Default: one at a time, one slot, as written.
- Q2: Should the seat be allowed a docs line if a product fix truly needs one? Default: no, STOP and ask.

## DERIVED cause lean (not run)
Row 1 looks test-side or environment-side from the source read: the limiter's counting is serialized under one lock, so a plain over-refusal is unlikely; the live hypothesis is two posts answered 503 by a transient write failure under hosted load (would read as 18 Created, 10 429, 2 other). That needs the status codes of the non-201 answers, which no log has. Row 2 looks test-side (host disposed while a worker or hosted service is still running), also DERIVED, stack not seen.

## UNMEASURED
- Whether either row reproduces locally at any load (nobody has run them; the drafter ran no dotnet).
- The statuses of the two missing row-1 answers; the NRE stack of row 2 (not in any file I read).
- Live MPS panes: `tmux list-panes -a` printed no MPS or NexusAI name and I had no control, so the kit says UNMEASURED and Tuesday states live seats in the Stamp.
- `FeedbackRig` source: my fetch of `Infrastructure/FeedbackRig.cs` returned 404 at that path; the kit tells the seat to read the whole `Infrastructure/` folder.
- Heavy-lock holders and the `.git-lock` state beyond the `heavy` filter listing.

## Outside the fences
None known. Reads: the DRAFTER_RULES, the two template kits, the gate standard and B1520 verdict, model-routing and models_latest, the saved log, MPS source via `gh api -X GET` raw, the MPS `.env` read in-process for one Jira GET (nothing printed). Wrote only the two files plus scratch under `fleet/state/s270/draft1526/`. No `decision_queue.sh`, no briefs_staged, no ledger, no git in the project repo, no HTTP to any host except GitHub API GET and Jira GET.
