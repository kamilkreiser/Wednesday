From Friday (laptop seat), Datasec / MPS Commercial Calculator. Replies go to friday-laptop-agent@agentmail.to. This project has no mail key, so your STATUS file is your wrap.
# BRIEF B58 · SEAT-F: FIX ROUND for gate B57 (W-1 Blocker, W-2 Blocker, W-3 Major, plus the cheap Minor and test gaps) on B54's `e6c9ced`
**Written:** 2026-10-13 01:45 AEDT, as a draft by Friday's drafter. **Fired:** @NOW@. **Pane:** `Datasec/MPS-F`. Your commission is the newest file in `Briefs/` whose name contains `_SEAT-F_`.
(Launcher check. `Launch_Claude.command:107` takes the seat letter from a pane name that matches `*MPS*-?`. `:111` makes the commission "the NEWEST brief in 1_Project_Definition/Briefs/ whose file name contains _SEAT-${SEAT}_". The launcher states the rule in the prompt; it does not pick the file itself. At drafting (01:4x AEDT), `ls -t Briefs | grep _SEAT-F_` printed one line, `2026-10-12_B54_SEAT-F_overlay-store-residue.md`. This file replaces it.)
**Seat:** Seat F, a Claude build seat. One branch, red-first. **QA tier 1** throughout. W-2 and W-3 are holes in a path-safety refusal on a store that holds sell prices (the code half of lifting the hosted SITE HOLD). W-1 makes the overlay refuse every edit for good.
**Round:** FIX ROUND. This is **round 2 of 2** under Kam's two-NO-GO cap (lane A3: B57 was round 1, `B57_STATUS.md:1`, `:10`). The next gate is a **deltas gate**. **If it says NO GO, Friday ships what is closed and tickets the rest. There is no round 3.** So close each row completely, or list it as NOT DONE. Never leave a row half-done.
**Report:** `1_Project_Definition/Briefs/2026-10-13_B58_STATUS.md`. Its **last line** is exactly one of these:
- `READY FOR GATE: b58/gate-b57-overlay-fix-round <sha>`, where `<sha>` is the full 40-hex SHA read back by `git ls-remote origin refs/heads/b58/gate-b57-overlay-fix-round` in the same action as the push;
- `STOPPED: NEEDS FRIDAY`, followed by ONE question.

## AUTHORITY
- **Gate B57** (`Briefs/2026-10-12_B57_STATUS.md`, Seat E, round 1, 545 lines, last line `READY FOR REVIEW` `:545`) gave `B54 e6c9ced: NO GO (2 Blockers: W-1, W-2; 1 Major: W-3)` (`:10`) and `overall: NO GO` (`:16`, `:543`). In its words: *"B54: NO GO (round 2 owes W-1, W-2, W-3)"* (`:16`).
  - The closure table says `[B27-H1]` **NOT CLOSED** (`:35`) and `[B27-H3]` **NOT CLOSED** (`:37`). `[B27-H2]`, `[B27-H4]`, `[B37-G1-LOAD]` and `[B38-N6]` are CLOSED-WITH-NOTES (`:36`, `:38-40`). Do not rebuild those; keep them green.
  - `B53 3852d30: GO WITH NOTES` (`:8`). B53 is a different lane. Its Minors V-1 and V-2 are **not this round** (see the table under ROWS).
- **Kam, terminal to Friday, 2026-10-12 ~18:4x AEDT, verbatim** (carried from B54): *"keep going and keep rolling out agents to work through all tickets and items for MPS Calculator, Security Controls creation tool and HPSM POC"*. Only the MPS part is yours.
- **The fix shapes below are the gate's, not Friday's.** Each row marks them *"the gate proposes; verify before building"*. If you build something else, say why in STATUS.
- These stand unchanged: Q-09 (synthetic sets only), Q-16 (build nothing that deletes), C-19 (the restart proof waits on Kam's test), the **SITE HOLD** and the **P-1 / L-2 HOLD** (HOLDS).

## PRIOR-WORK CHECK (do this first; report it in STATUS `## PRIOR WORK`)
Re-read each item at `e6c9ced` and record whether it is **still open, already closed, or moved**, with `file:line`. If an item is already closed, do not rebuild it; say so.
- **`B57_STATUS.md`:** `wc -l` it (the drafter read **545** lines, last line `READY FOR REVIEW`). If the verdict, the findings list or any line quoted below changed, record each change. **If a new Blocker or Major for B54 appears, STOP: NEEDS FRIDAY.**
- `src/MpsCalc.Api/Inventory/CatalogueOverlayStore.cs` at `e6c9ced`, read by the drafter with `git show`:
  - `:323-363` `MutateAsync`. `:342` `await before.WaitAsync(Remaining(arrivedAt))`; `:347` `_ = before.ContinueWith(_ => mine.TrySetResult(), …)`; `:348` `mine = null;`; `:361` `mine?.TrySetResult();` in the `finally`.
  - `:366-370` the test-only sync `Mutate`; `:119` `LockTimeout`; `:122` `BeforeRename` and `:125` `AfterReload` (test seams; `AfterReload` runs at `:355`, inside the file lock).
  - `:154-163` `OpenHosted`: `RefuseOverlap` against the quote store (`:157`) and the reference directory (`:161`), then `RefuseLinkedOverlap` (`:162`). `:180-181` `Full` uses `Path.GetFullPath`, which is lexical.
  - `:188-215` `RefuseOverlap`: `StringComparison.OrdinalIgnoreCase` (`:190`) over `QuoteFileStore.RealPath` (`:196-197`).
  - `:222-243` `RefuseLinkedOverlap`: `FileInfo.LinkTarget` (`:224`), `QuoteFileStore.RealPath(reference)` (`:232`), `File.Exists(target)` (`:238`).
  - `:285-289` `WellFormed`.
- `src/MpsCalc.Api/Quotes/QuoteFileStore.cs:547-566` `RealPath` (at `e6c9ced`; `:548-566` at `1329f2e`). `:560` (`:561` at main) does `RealPath(Path.GetFullPath(… Path.Combine(cur, link)), depth + 1)`. **This is frozen** (row W-2).
- `tests/MpsCalc.Api.Tests/OverlayGateFindingsTests.cs:376-401` (`G1_a_burst_across_two_hosts_loses_and_duplicates_nothing`; `NotEmpty` `:394`).
- `tests/MpsCalc.Api.Tests/OverlayResidueTests.B54.cs`: `OverlayResidueTests` `:23`, `OverlayResidueTimingTests` `:344`.
- Read whole: `B57_STATUS.md`, in particular `## Findings` (`:371-411`), the H-1 layout table (`:224-247`), the H-3 timing table (`:261-279`), the red-proof tables (`:298-354`), `## Notes` (`:448-466`), needs-Friday (`:468-473`), the hosted notes (`:475-483`) and the pre-deploy items (`:504-509`). Also your own `B54_STATUS.md` (294 lines) and `B54…md`, and records `BACKLOG.md` rows `[B27-H1]`, `[B27-H3]` and `[B54-R1]`…`[B54-R3]` (on `records/b54`).
- The gate's instruments, **read-only. Copy them; never run them in place:** `.tools/qa-B57/tools/h1_57.py`, `h1all.sh`, `h3_57.py`, `h3_57b.py`, `h3matrix.sh`, `start57.py`, `qlib57.py`, `oidc_stub57.py`, `jwt57.py`, `stubctl.py`, `pkg.sh`, `tamper54_copy.py`, `mutrun57.py`, `muttable57.py`, `leak57.py`, `words57cs.py`. Their evidence is in `Briefs/2026-10-12_B57_evidence/` (`06_h1-*.json`, `06_h1_replicates_L09_L17.json`, `08_h3-*.json`, `08_twohost_no_holder.json`).
- Search for prior work: `git log --all --oneline -i --grep='W-1\|W-2\|W-3\|handoff\|B58'`. List the hits.

## Base and branch
- **Base: B54 head = `e6c9cedbf760e9ca2f5957703f420267c9189bf8`** (tree `32a6c317…`, parent `5f95cc8`, subject "B54 item 2 follow-up: one malformed form per required audit field"). This is `git log -1 --format='%H %T %P %s' e6c9ced`, read by the drafter. B54 is **not merged** and has no PR (`ls-remote` lists `refs/pull/29/head` = `3852d30`, B53, and no PR at `e6c9ced`).
- **What the drafter measured (read verbs only), 01:41 AEDT 2026-10-13:**
  - `ls-remote`: `main` = `1329f2e824e9237e44ebb01918993ec0111a6972`; `b54/overlay-store-residue` = `e6c9ced…`; `b53/source-store-hardening` = `3852d309…`; `refs/heads/b58*` printed **0 lines**.
  - `merge-base 1329f2e e6c9ced` = `b28c95eb`; `rev-list --left-right --count 1329f2e...e6c9ced` = `1 5`.
  - `git diff --stat b28c95eb 1329f2e -- src/MpsCalc.Api/Inventory 'tests/MpsCalc.Api.Tests/Overlay*' tests/MpsCalc.Api.Tests/InventoryApiTests.cs tests/MpsCalc.Api.Tests/CatalogueOverlayStoreTests.cs` printed nothing: main did not touch the overlay.
  - The gate measured `merge-tree --write-tree 1329f2e e6c9ced` → `d36f5bca…` rc 0 (`B57:66`).
  - **B53** (PR #29) touches exactly 5 paths, all `src/MpsCalc.Api/Sources/*` and two `SourceLifecycleTests.*` files (`diff --name-only b28c95eb 3852d30`). That is disjoint from your write set. **Friday may land PR #29 on main while you work.**
- **Friday's decision: cut from `e6c9ced`, and do NOT rebase or merge main into the branch.**
  - Why: B54's five commits stay as they are, so the deltas gate can diff `e6c9ced...<your head>` exactly. A rebase would rewrite them and need a force push, which is forbidden. Main moves only by squash PRs that cannot touch your paths. So a clean `merge-tree` is the proof that the PR will land; a rebase adds nothing.
  - Branch **`b58/gate-b57-overlay-fix-round`**, created with `worktree add -b b58/gate-b57-overlay-fix-round '/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator/.tools/wt-B58' e6c9ced` (`chmod 700`). Take base measurements in `.tools/wt-B58-base`, detached at `e6c9ced`. **Never add commits to `b54/…`**: gate B57 pinned it.
- **Step 0 (before any edit):** `git -C 2_Project_Files fetch origin`, then `git ls-remote origin refs/heads/main refs/heads/b54/overlay-store-residue refs/heads/b53/source-store-hardening 'refs/heads/b58*'`. Record `M0` = the main SHA it prints.
  - If `b54/…` is not `e6c9ced…`, or a `b58*` branch exists: **STOP: NEEDS FRIDAY**.
  - `M0` must be `1329f2e…` or a descendant (`merge-base --is-ancestor 1329f2e M0`). If it is a descendant, run `git diff --name-only 1329f2e M0 -- src/MpsCalc.Api/Inventory src/MpsCalc.Api/Quotes/QuoteFileStore.cs 'tests/MpsCalc.Api.Tests/Overlay*'`. If that prints anything: **STOP: NEEDS FRIDAY**. (PR #29 landing prints nothing here. That is expected; say so.) Anything else: **STOP: NEEDS FRIDAY**.
  - **Prove the start is clean:** `git merge-tree --write-tree M0 e6c9ced` gives rc 0. Record the tree. This writes objects only, no ref, so it is allowed here.
- **At the end (after the last commit, before the push):** fetch again and record `M1` = main.
  - `git merge-tree --write-tree M1 HEAD` must give rc 0, with no conflict lines. Record the tree.
  - If `M1 ≠ M0`: `git diff --name-only M0 M1` must not intersect your write set (`comm -12`, count 0). Then also build and run the API suite on that merge tree, in a `git clone --shared` under `.tools/qa-B58/clone` (detached, push URL set to `NO-PUSH`, never pushed). Report it as a row in Test Evidence.
  - Any conflict, or an intersection: **STOP: NEEDS FRIDAY**. Never resolve it by rebasing.
- **Push your branch only, and read it back.** Friday opens the PR (from `b58/…`; it carries B54's five commits plus yours) and lands it once CodeQL and the checks are green. **Never push an unscanned commit to main. No PR from you. No force push.**

## Ports
- **6680–6689.** This was B54's range, and B54's seat is closed (`B54_STATUS.md:294` `READY FOR GATE`). **Friday reassigns 6680–6689 to B58.** That overrides "never use a port named in an earlier brief" for this range only. Use API 6680–6686 and the OIDC stub 6689.
- The drafter's check at 01:39 AEDT: `lsof -nP -iTCP:6680-6689 -sTCP:LISTEN` printed nothing (rc 1), so **0 listeners**. **Run `lsof` again before every bind.** On any listener in your range, **STOP: NEEDS FRIDAY**; never move ranges.
- Gate B57 used 6650–6659 (`B57:512`). Never touch it, nor any other range named in an earlier brief or STATUS. Pass ports through env; never edit a shared config default.

## Hosted mode for every H-1 arm
**The H-1 guard runs only in hosted mode** (`OpenHosted`, `CatalogueOverlayStore.cs:147-178`; `Program.cs:60`). DevStub has no reference-overlap guard by design (`B57:247`: L01 opens on both trees in DevStub). So **every live H-1 arm (W-2, W-3 and the full layout re-run) runs an Entra-fake, Production process**, as the gate did (`B57:224`, `:296`):
- the real published package (copy `pkg.sh`), `ASPNETCORE_ENVIRONMENT=Production`;
- `AzureAd__MetadataAddress` pointed at your own copy of `oidc_stub57.py` on 6689;
- tokens minted with a copy of `jwt57.py` and a **signing key you generate** under `.tools/qa-B58/keys/` (0600, never printed). Never reuse the gate's key;
- gate-random GUIDs in `.tools/qa-B58/ids.json`;
- the quote store, overlay and reference paths under the hosted root, all **synthetic**, on both volumes: the project volume (case-**sensitive**) and `$(getconf DARWIN_USER_TEMP_DIR)qa-B58-ci/` (case-**insensitive**). Both are normalisation-**insensitive** (`B57:225`). Measure both properties again and print them.
- In-process suite tests call `OpenHosted` directly, as B54's `OverlayResidueTests` do. That needs no process.

## Write set (PATHS; nothing outside it)
- `src/MpsCalc.Api/Inventory/CatalogueOverlayStore.cs`
- `tests/MpsCalc.Api.Tests/OverlayResidueTests.B54.cs`, `tests/MpsCalc.Api.Tests/OverlayGateFindingsTests.cs`
- a new file `tests/MpsCalc.Api.Tests/OverlayGateB57Tests.B58.cs`
- **4 paths.** All are inside B54's own set (`B54…md` Write set; `B57:78`). Their intersection with B53 (5 paths), `main...b47/feedback-pill`, `main...b49/gate-b48-fix-round` and `main...b46/home-dashboard` was **0** each (`diff --name-only 1329f2e...origin/<b> | grep -i -c 'Inventory/\|Overlay\|InventoryApi'` printed 0 ×4).
- **FROZEN (the diff must be empty):**
  - **`src/MpsCalc.Api/Quotes/**`, including `QuoteFileStore.cs` and its `RealPath`** (see row W-2);
  - `src/MpsCalc.Api/Inventory/InventoryEndpoints.cs` (no row needs it; if one does, **STOP: NEEDS FRIDAY**);
  - `src/MpsCalc.Api/Program.cs`. `Open`, `OpenHosted`, `MutateAsync`, `PlatformModesWarning` and `StrayTempFiles` keep their signatures. **`PathKey`, `FileName` and `LockFileName` keep their names and values** (`SourceLifecycle.cs:148` reads `PathKey`, `B57:85`);
  - `src/MpsCalc.Api/Sources/**` (lane B53), `Contracts/**`, `Feedback/**`, `Infrastructure/**`, `src/MpsCalc.Engine/**`, `src/MpsCalc.Import/**`;
  - `docs/**`, `docs/api/openapi.json`, `web/**`, every other test file, `tests/…/Infrastructure/**`, **`*.csproj`** (so: no `AllowUnsafeBlocks`, no new package), `infra/**`, `scripts/**`, `.github/**`.
- **If a row needs a frozen file**, do not touch it. Mark the arm **NOT DONE: BLOCKED-BY-FILES (<file>, <owner>)** and go on, except where the row says STOP.

## Tier 1 (all rows)
- **The H-1 FAIL condition, verbatim (B57 `:388`):** *"a hosted start that succeeds when the reference file's final target sits in, contains or equals the overlay directory (any link form, any case form)"*. **For this round, "any case form" includes Unicode normalisation forms (NFC / NFD).**
- A Busy answer changes nothing, and **the next write after a Busy run is 200/201** (W-1).
- Controls still open: a regular-file reference path (L00), a link to a genuinely different directory (L03), the sibling `catalogue-overlay-books/` (L16). **A start refused with a regular-file reference path is a FAIL** (`B57:478`).
- No price, total or applied percent moves on any fixture (the full engine + API suites). The overlay file, version and audit are unchanged by every refusal.
- Value-free: no refusal or log line carries a price, a SKU from a price book, or a credential.

## ROWS (in this order; red test first for each; one commit per row)

### Row W-1 · Blocker · one timed-out wait leaves the overlay Busy for good
- **Finding, verbatim (B57 `:372-373`):** *"W-1 · Blocker · B54 · INTRODUCED · `src/MpsCalc.Api/Inventory/CatalogueOverlayStore.cs:342-348`"*. FOUND: *"a writer whose `before.WaitAsync(Remaining(arrivedAt))` times out runs `_ = before.ContinueWith(_ => mine.TrySetResult(), …); mine = null;`. The lambda captures the **variable** `mine`, not its value, so when `before` completes the continuation dereferences `null` (the fault is swallowed: an unobserved task) and this writer's `TaskCompletionSource` is **never completed**. … from then on **every** write in the process answers 503 Busy, though nothing holds the lock, until the process restarts. Nothing is logged (`fail:` 0)."*
- **FAIL condition, verbatim (B57 `:375`):** *"(tier 1, brief "A Busy answer that changed something"; and item 8's "the next write after release 200"): any next write after release that is not 200."*
- **Measured by the gate:** next write after release 503 in **23/23** runs with ≥ 2 waiters; base 200 in 18/18; the one-line capture gave 200 in 6/6 (`B57:44`, `:376-380`). Also with **no outside holder**: two hosts on one overlay, N = 250, both hosts stuck at 503 after any round that produced a 503 (`:381`).
- **Fix shape. The gate proposes; verify before building (`:383`):** *"capture the source in a local before the hand-off (`var handoff = mine; before.ContinueWith(_ => handoff.TrySetResult(), …)`), or restructure so the timed-out writer completes its own source from a `finally` after `before` completes."* Friday adds: the hand-off continuation must not be able to fault. Prove it with a test that counts `TaskScheduler.UnobservedTaskException` (or an equal check), or say why no check is possible.
- **Red-first cell. Use the gate's exact scenario: writers time out, then the holder releases, then the next write must be 200.**
  - **Trigger note:** **with 1 waiting writer it recovers (2/2)** (`:377`, `:271`). The trigger is **≥ 2 waiters**. A 1-waiter test is a guard, not a red test. Say which is which.
  - (1) **The live shape, in-process (`:383`):** hold `overlay.lock` from a second handle. Run **2** and then **16** concurrent writes until each answers Busy. Release. Then one PATCH and one POST must each be 200/201, and the overlay version advances by exactly one each. **RED at `e6c9ced`.**
  - (2) **The in-process turn only:** a slow first writer (the `AfterReload` seam, `:125`/`:355`, delaying past `LockTimeout`) with **two** waiters behind it. After it finishes, one write must be 200. **RED at `e6c9ced`.**
  - (3) **W-4 (taken here):** after the G1 burst (`OverlayGateFindingsTests.cs:376-401`), after every Busy test in that file, and at the end of each `OverlayResidueTimingTests` case, one more write must be 201/200 once nothing holds the lock.
  - **GREEN at head**, and the H-3 timing tests keep their bound (0 late; reads < 100 ms).
  - **Tampered back RED:** (a) the lambda captures `mine` again; (b) the gate's `O6-handoff-continuation-dropped` (`:339`, GREEN at `e6c9ced`, must be RED now); (c) the gate's `B1-only-first-write-per-host-succeeds` (`:341`, GREEN at `e6c9ced`, must be RED now through (3)).
- **Live (DevStub Release is fine for W-1; your ports):** a copy of `h3_57.py` / `h3matrix.sh`.
  - Run an outside `flock` holder, then `fcntl`, at N = 1, 2, 3, 16, 32, 64, 128 and 64 mixed POST+PATCH, 3 runs each (1 run each for `fcntl`).
  - Per run, report: late / N, max, median, the read time during the wait, and **the next write after release (3 single writes, 1 s apart): 200 ×3 in every run**.
  - Two hosts on one overlay with **no outside holder** (copy the `08_twohost_no_holder.json` shape): N = 250, 3 rounds. After any round that produced a 503, **both hosts answer 201 to every later write**.
  - Give the load average before every timing.

### Row W-2 · Blocker (by the tier-1 text) · `..` after a directory link defeats the link check
- **Finding, verbatim (B57 `:385-386`):** *"W-2 · Blocker (by the brief's tier-1 text; contested like B27 H-1) · B54 · residue of the H-1 fix · `CatalogueOverlayStore.cs:222-243` with `QuoteFileStore.RealPath` (`Quotes/QuoteFileStore.cs:548-563` at `1329f2e`)"*. FOUND: *"`RealPath` resolves a link at each segment by `RealPath(Path.GetFullPath(cur + link))`. `GetFullPath` collapses `..` **lexically** before the components before it are resolved; the kernel resolves `..` after following them. A reference path `pbf/reference.json → "d/../real.json"` with `pbf/d → <overlay>/sub` names `<overlay>/real.json` for the kernel, and `pbf/real.json` for the guard. With a file at `pbf/real.json` (a decoy), the guard checks `pbf/` and passes."*
- **FAIL condition:** the tier-1 text above (`:388`). Measured by the gate: L09 **opens 8/8** (4 per volume), loads the **real** file's ids, and one POST writes `overlay.json` + `overlay.lock` beside the real file 8/8 (`:389`).
- **Fix shape. The gate proposes; verify before building (`:391`):** *"resolve the reference file with the operating system, not by string: open it and compare the containing directory's `(st_dev, st_ino)` with the overlay directory and its ancestors and descendants (`stat` on Unix), or resolve link targets segment by segment, applying `..` to the **physical** parent of the resolved prefix (never `GetFullPath` on an unresolved prefix)."*
- **Friday's constraint: the fix stays local to the overlay store.** `QuoteFileStore.RealPath` is shared and frozen.
  - **Preferred:** a private resolver inside `CatalogueOverlayStore.cs` that walks the path segment by segment. It follows each link hop relative to that link's **physical** parent, applies `..` to the resolved prefix, and never calls `GetFullPath` on a prefix whose links are not yet resolved. It keeps the existing loop cap and the loop / dangling words. Use it for **every** path that `RefuseOverlap` and `RefuseLinkedOverlap` compare (the overlay, the quote store, the reference directory and the link target), not only the link target.
  - **Identity compare (`st_dev`/`st_ino`):** use it only if it needs no `*.csproj` change and gives the same answer on macOS and on Linux (CI is `ubuntu-latest`, `.github/workflows/ci.yml:32`). If it needs `AllowUnsafeBlocks` or a package, it is out of reach: say so and use the resolver.
  - **If the fix can only be made by changing `QuoteFileStore.RealPath`: STOP: NEEDS FRIDAY**, with the blast radius. The drafter's count (`git grep -n RealPath e6c9ced -- src`) gives these non-test callers, and every one would change:
    - `Quotes/QuoteFileStore.cs:481`, `:488` (`ResolvePrivate`, the DevStub quote store and every DevStub store opener);
    - `Infrastructure/HostedWeb.cs:45`;
    - `Sources/SourceLifecycle.cs:575-576` (`:934-935` at B53's `3852d30`; lane B53);
    - `Inventory/CatalogueOverlayStore.cs:196`, `:197`, `:232`.
    - Plus 6 test fixtures that use it to find the temp root (`HostedStoreTests.cs:21`, `OverlayGateFindingsTests.cs:35`, `OverlayHostedStoreTests.cs:29`, `OverlayResidueTests.B54.cs:37`/`:356`, `OverlayRestartTests.cs:27`, `ProposalSaveFailureTests.cs:24`).
    - Re-count them at your base and put the list in the STOP question.
- **Red-first cell:**
  - **Test (in-process `OpenHosted`, temp volume and project volume):** L09 (`ref.json → d/../real.json`, `d → <overlay>/sub`, decoy at `pbf/real.json`) → start **refused**, the words name the overlap, nothing written beside the real file. **RED at `e6c9ced`.**
  - **Control (`:391`):** the same link where the decoy *is* the real target (`d` a plain directory, so lexical = physical) → **opens**. Green at both.
  - **Extra arms, measured first at `e6c9ced`, with the result reported:**
    - **L09b:** the **configured** `ReferenceStorePath` itself is `<HR>/pbf/d/../real.json`, with `d → <overlay>/sub` and a decoy at `pbf/real.json`, and no file link. `Full` (`:180-181`) is lexical too. If it opens at `e6c9ced`, it is W-2's class and the same commit must refuse it.
    - **L09d:** `..` after a link inside the **quote store** path's overlap compare, if one can be built. If one cannot be built (`ResolveHosted` refuses links in the configured hosted path), say so.
  - **GREEN at head.**
  - **Tampered back RED:** (a) put `QuoteFileStore.RealPath` back for the target resolution; (b) apply `GetFullPath` to the unresolved prefix inside your resolver. Each one goes RED on its own.

### Row W-3 · Major · an NFD-spelled target passes the overlap compare
- **Finding, verbatim (B57 `:393-394`):** *"W-3 · Major · B54 · residue of the H-1 fix (same compare as B25 G-4) · `CatalogueOverlayStore.cs:188-213` (`RefuseOverlap`, `OrdinalIgnoreCase` string compare)"*. FOUND: *"a link target spelled in NFD (`catalogue-overlay-café` decomposed) reaches the NFC-named overlay directory on both macOS volumes (both are normalisation-insensitive), but the two strings differ, so `RefuseOverlap` passes."*
- **FAIL condition, verbatim (`:395`):** *"FAIL condition as W-2 (*"any case form"*; a normalisation form is not literally a case form, hence Major). L17: opens **8/8** (4 per volume); one POST writes `overlay.json` + `overlay.lock` beside the real file 8/8. The configured-path variant L18 opens at base and head alike (N-11, PRE-EXISTING)."*
- **Fix shape. The gate proposes; verify before building (`:396`):** *"compare directory identity, not spelling (`st_dev`/`st_ino`), as for W-2; at least normalise both strings to NFC before the compare."*
  - **Friday's default:** the same compare as row W-2. If W-2 uses the resolver (no identity), then `RefuseOverlap` normalises **both** sides to NFC (`string.Normalize(NormalizationForm.FormC)`) **before** the `OrdinalIgnoreCase` equal / prefix tests. Every path goes through it: the overlay, the quote store, the configured reference directory (that covers **L18 / N-11**) and the link target (that covers **L17**).
  - Refusing an NFD/NFC pair on a normalisation-sensitive disk is the **safe direction**, the same as case on a case-sensitive disk (`:184-186`). Say so in the code comment and in STATUS.
- **Red-first cell:**
  - **Tests: L17** (an NFD link target → the NFC overlay directory) and **L18** (an NFD configured `ReferenceStorePath`, no link) → refused, in the overlap words, with nothing written beside the real file. **RED at `e6c9ced`** on macOS.
  - **CI is `ubuntu-latest`** (ext4 is normalisation-sensitive). Measure the volume in the test (create the NFC directory, then test whether its NFD spelling exists), and assert the right outcome for that volume. The test must be **green on Linux** and must **never be skipped silently**: print which branch ran. If an arm cannot be built on Linux, assert that it cannot, and name it in STATUS.
  - **GREEN at head.**
  - **Tampered back RED:** remove the NFC step. RED on L17 and L18.
  - **Not this round:** the same compare in `Sources/SourceLifecycle.cs:926-945` (B53's `RefuseOverlap`, `3852d30`) is `Sources/**`, which is frozen. Record it (RECORDS).

### Row 4 · Gate Minors, Notes and test gaps for B54: TAKEN / NOT THIS ROUND (drafter's call; each quoted by line)
"One-line and inside the same files" means the fix fits in the 4 write-set paths, with no frozen file and no ruling. **TAKEN rows each get their own commit, red first** (or green-at-base guard + mutant RED, where the row says so). You may move a TAKEN row to NOT THIS ROUND only with a measured reason in STATUS. **Moving a NOT THIS ROUND row to TAKEN is STOP: NEEDS FRIDAY.**

| Item (B57 line) | Gate's words (verbatim, shortened with …) | Call | Reason / shape |
|---|---|---|---|
| **W-4** Minor (`:398-401`) | *"the rewritten G1 accepts any number of 503s as long as one write succeeds; no overlay test writes again after a Busy run"* | **TAKEN (inside row W-1, cell 3)** | Gate HOW `:401`: *"after the burst (and after every Busy test), one more write must be 201/200; and the H-3 timing tests must end with a successful write after release."* |
| mutant **O3** GREEN (`:351`, `:336`) | *"`WellFormed` checks audit entry 1 only … GREEN on the suite (every B54 form breaks entry 1), **RED on my probe**: a store whose 2nd audit entry has `by: null` boots"* | **TAKEN (test only)** | Add a form whose 2nd audit entry has `by: null` → start refused, file byte-unchanged. A guard: green at `e6c9ced`; the O3 mutant must be RED on the suite at head. |
| mutant **O6** GREEN (`:352`) | *"the suite cannot see the hand-off at all"* | **TAKEN (row W-1)** | Tamper (b) of row W-1. |
| mutant **B1** GREEN (`:353`) | *"by Friday's default the burst test accepts 2 × 201 + 46 clean 503s"* | **TAKEN (row W-1)** | Tamper (c) of row W-1, through cell 3. Keep Friday's "201 or a clean 503" default. Do not add a minimum success ratio (that is load-sensitive, `[B37-G1-LOAD]`). |
| **N-11** (`:459`) | *"an NFD-spelled configured `ReferenceStorePath` into the NFC overlay directory opens at base and head (L18)"* | **TAKEN (row W-3)** | Same compare. |
| **N-8** (`:456`) | *"`by: ""` (empty) is accepted … Not null-bearing, so outside B27's FAIL; the contract requires `by`"* | NOT THIS ROUND | One line, but it needs a **ruling**: is empty the same as missing? It also widens PRE-1's hosted outage class. A stricter boot check refuses a hosted start whose file carries it (`:479`, `:505`). Goes to needs-Friday + RECORDS. |
| **N-9** (`:457`) | *"a duplicated key in an audit entry with the **first** value null and the last non-null loads (last wins)"* | NOT THIS ROUND | Needs a raw-token pre-scan (B53's lives in frozen `Sources/**`). Not one line. RECORDS. |
| **N-10** (`:458`) | *"an 8 MiB padded `overlay.json` loads; no size cap (none required)"* | NOT THIS ROUND | None required. |
| **N-14** (`:462`) | *"a hard link of a file inside the overlay directory cannot be seen by any path check"* | NOT THIS ROUND | A directory-identity compare still cannot see a file hard link. RECORDS (with B41 N-7 / `[B42-L3]`). |
| **N-15** `[B54-R2]` (`:463`) · **N-7** `[B54-R3]` (`:455`) | *"time before the handler … is not counted"* · *"every start refusal prints the host's unhandled-exception trace"* | NOT THIS ROUND | Both need `Program.cs` / `Infrastructure` (frozen). Already recorded. |
| mutant **O4** GREEN, UNVERIFIED (`:354`) | *"POST arrival stamped after authorization … no timing probe can separate it"* | NOT THIS ROUND | No instrument can see it. |
| `[B54-R1]` (`:256`) | *"`itemClass` absent → `device` · `itemClass: 2` → `software` … declared"* | NOT THIS ROUND | Needs the hosted file measured first (UNMEASURED `:494`). |
| UNMEASURED (`:493`) | *"Whether `ResolveLinkTarget(returnFinalTarget: true)` (B53's version-store reference-link check, `SourceLifecycle.cs:160-181`) has W-2's `..` blind spot"* | NOT THIS ROUND | `Sources/**` (lane B53). RECORDS row, so the next Sources lane probes it. |
| **V-1**, **V-2**, N-1…N-6, N-12, N-13, N-16…N-18 | B53's, or not a lane's | NOT THIS ROUND | Not this lane. Do not record them; they are B53's records. |

## Test Evidence (run each command as `cmd > out 2>&1; rc=$?`, then read the file)
- **Base vs head** (`wt-B58-base` at `e6c9ced`, `wt-B58`):
  - .NET full suite, Release `--no-incremental`, **0 warnings**. The gate measured `e6c9ced` at **235 / 72 / 787 = 1,094/1,094** (`B57:360-361`). Re-measure; do not trust it;
  - `dotnet list package --vulnerable --include-transitive` 0;
  - reconcile every count change by test name (`--list-tests`, `comm`);
  - `git diff --numstat e6c9ced -- web docs` empty.
- **Red-first, per row:** each new test fails at `e6c9ced` (or at the row's parent commit) and passes at head. Report `RED n/m → GREEN`. Guards (O3, the 1-waiter case, controls) are green at both; say so.
- **Red-proof table, one line per conjunct** (tamper → RED on the whole API project → sha256 restore + `status --porcelain` empty). It covers every row's tampers above. Also **re-run the gate's B54 sample and own O-mutants** from copies of `tamper54_copy.py` / `muttable57.py`: `T1a`, `T1b`, `T2e`, `T3a`, `T3b`, `T4a`, `T4a-x`, `T4b`, `O2`, `O3`, `O5`, `O6`, `B1`, `B2`, `B3`. **Each must be RED at head**, with anchors re-derived 1/1. `O4` stays UNVERIFIED; say so.
- **The H-1 layout re-run** (copy `h1_57.py` / `h1all.sh`; Entra-fake Production; both volumes; fresh roots; head vs `e6c9ced`). Run L00–L20 as `B57:226-246`, plus your L09b, L09c (the decoy-is-real control) and L09d.
  - **Expect:** refuse layouts **17/17 refused per volume** (gate: 14/17 at `e6c9ced`); controls L00, L03, L16 and L09c open 4/4 per volume; L19 (hard link) opens (N-14, declared).
  - For every opened layout, list the files beside the real file after one POST. Replicates: L09 and L17, 6 fresh roots each, refused 6/6.
- **H-3 / W-1 table** (row W-1 live), with the load average on every row.
- **H-4 unchanged:** B54's and B27's 8 forms are still refused at boot, and the running 503s are unchanged (copy `h4_57.py`; 1 pass, Entra-fake).
- **Store off = base:** the overlay success path (POST, PATCH, GET inventory, GET audit) gives version and audit equal to `e6c9ced`'s, on one restart (B22's behaviour unchanged).
- **Merge proof:** the step-0 and end `merge-tree` rows (trees, rc), and the merged-tree suite if main moved.
- **Leak + secret scan** over `git diff e6c9ced...HEAD` and `git log --format=%B e6c9ced..HEAD`, using a copy of `leak57.py` plus `gitleaks git --redact`. Counts only, with a planted control per class that fires.
- **No frozen change:** `git diff --numstat e6c9ced -- src/MpsCalc.Api/Quotes src/MpsCalc.Api/Program.cs src/MpsCalc.Api/Sources src/MpsCalc.Api/Inventory/InventoryEndpoints.cs src/MpsCalc.Api/Contracts src/MpsCalc.Api/Feedback src/MpsCalc.Api/Infrastructure src/MpsCalc.Engine src/MpsCalc.Import docs web infra scripts .github '*.csproj' tests/MpsCalc.Api.Tests/Infrastructure` is empty (paste it). `git diff --name-only e6c9ced` lists only the 4 write-set paths.
- **Processes:** every process you started (pid, port, cwd) and its stop. **0 left at READY.**
- Evidence → `Briefs/2026-10-13_B58_evidence/` (0700 folder, 0600 files; mask the project path as `<P>`); tools and logs → `.tools/qa-B58/` (0700).

## NEW WORDS (Friday shows Kam before any deploy)
- Every new or changed visible string, old → new, verbatim, with `file:line`: start refusals, problem `detail`s, log templates. **Friday's aim is 0 new words:** W-2 and W-3 should reuse B54's existing refusal words (`CatalogueOverlayStore.cs:201`, `:205`, `:209`, `:213`, `:236`, `:240`), and W-1 changes no answer.
- Run copies of `words57cs.py` over `e6c9ced...<head>`: count = count, and a planted undeclared string (in an unpushed local commit) must be flagged.

## STATUS sections
- BLUF (one line per row)
- **PRIOR WORK** (every cite above re-read; what moved; the B57 line-count check)
- Base read: step 0 (`M0`, `merge-tree` tree and rc), end (`M1`, tree and rc), and whether PR #29 landed in between; Commits
- Test Evidence; Red-proof table; Tier-1 conditions
- FOUND / TESTED / HOW / NOT TESTED per row
- Fix shape chosen per row: the gate's or another, and why (W-2: resolver or identity, and why)
- The H-1 layout table (head vs `e6c9ced`, both volumes) and the H-3 / W-1 table (next write after release in every row)
- The TAKEN / NOT THIS ROUND table as built
- NEW WORDS; Modified pre-existing tests (before → after, why)
- UNMEASURED
- `## NOT DONE / NOT COVERED`, as prominent as the evidence
- RECORDS
- needs-Friday:
  - N-8 (empty `by`: a ruling, and its PRE-1 effect);
  - the W-2 fix shape as built;
  - every BLOCKED-BY-FILES arm;
  - one line for Friday: "H-1 fixed on branch; the SITE HOLD stays until a deploy brief";
  - one line: PRE-2 (`B57:506`) is what the deploy brief must run against the package;
  - Jira draft lines (Jira writes are Friday's).
- `## For the records seat` (instead of a history entry): the closes to fold once merged
- Leak + secret scan; processes; worktrees and files left

## RECORDS (local `records/b58` branch, commit only)
- The records repo is the project root. It has no remote (`git remote -v` printed 0 lines). Root `main` = `01ef803`; `records/b54` = `1129a25`, `0 1` ahead, **not folded**.
- `git -C '<project root>' worktree add .tools/wt-B58-records -b records/b58 records/b54` (`chmod 700`). That keeps `[B54-R1]`…`[B54-R3]`.
- `BACKLOG.md` `## Deferred problems`, new rows only, in the existing row shape:
  - N-8, N-9, N-14 (or a dated line on the existing hard-link row);
  - the B53 `RefuseOverlap` NFD class (`SourceLifecycle.cs:926-945`);
  - the B53 `ResolveLinkTarget` `..` question (`B57:493`);
  - one row per row or arm you leave NOT DONE.
  - **Edit no existing row**; Friday folds the closes.
- One commit, `Records: gate B57 rows not fixed in B58 (B58)`. **Never fold into `main`.** `CLAUDE.md`, `JIRA.md`, `history.md` and Jira are Friday's.

## Time-box
**About 2.5–3 h.** If you run short, finish in this order: **W-1** (with W-4), **W-2**, **W-3**, then O3. List what is left as **NOT DONE**, never half-built. Remember there is no round 3.

## UNMEASURED (by the drafter, each with its closing instrument)
- Whether L09b (a `..` after a directory link in the **configured** reference path) opens at `e6c9ced`. It closes with your base run of L09b.
- Whether a `st_dev`/`st_ino` compare is reachable without a `*.csproj` change on both macOS and Linux. It closes with your W-2 build note.
- Whether `merge-tree M0 e6c9ced` is still clean at firing (the gate's `d36f5bca` was against `1329f2e`). It closes with step 0.
- The hosted share's normalisation and case rules (`B57:492`). It stays UNMEASURED: no hosted request.
- CodeQL and CI for your head: Friday reads them on the PR.

## HOLDS
- Datasec only. No other client's names, tickets or paths.
- **CodeQL policy:** push your branch only; never push to main; never dismiss an alert; never ask for a bypass. **No PR.**
- **No deploy.** No Azure command, no app-setting change, no hosted request, nothing sent to any human, **no Jira write**.
- **SITE HOLD** (records `BACKLOG.md` `## Holds on the hosted site`): none of the four store path settings changes. `MpsCalc:ReferenceStorePath` stays a regular file on the hosted site. Fixing H-1 on a branch **does not lift it** (`B57:482`).
- **P-1 / L-2 HOLD:** this brief deploys nothing.
- **Q-09:** never open, activate or show a real price book. Every reference file, overlay and probe is **synthetic**. Never open `.local/pricebooks/` or anything under it.
- No pricing rule change: no price, total or applied percent moves on any fixture.
- **Never open `4_Credentials/.env`.** No secrets anywhere. The OIDC signing key is yours, under `.tools/qa-B58/keys/` (0600), and is never printed or committed.
- **Never delete; quarantine** to `.tools/_quarantine/2026-10-13_B58_<what>/` (0700). Never edit a running script; write a new file instead.
- **No `5_Project_History/history.md` entry** (Friday's). The launcher's grant to write history and Jira (`Launch_Claude.command:96`) is void by this brief.
- **Own worktree and own ports.**
  - Allowed: `fetch`, `worktree add`, `merge-tree --write-tree` (objects only), commits and pushes on `b58/gate-b57-overlay-fix-round`, the `clone --shared` under `.tools/qa-B58/clone` (never pushed), and records commits on `records/b58` only.
  - Never `checkout`/`switch` in `2_Project_Files` or the project root. **Never `rebase`, `merge` into your branch, `gc`, `prune`, `reset`, `worktree remove`, `branch -D` or force-push.** Never push to `b54/…`.
  - Other seats' worktrees and tools (`wt-B57*`, `qa-B57/`, `wt-B53*`, `qa-B53/`, `wt-B54*`, `qa-B54/`) are read-only. Copy from them.
- **Processes:** kill by port + cwd, never by name. Stop everything you started before READY. `caffeinate`, the shared `VBCSCompiler` and any listener outside 6680–6689 are not yours.
- **.NET:** `export DOTNET_ROOT='/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator/.tools/dotnet' PATH="$DOTNET_ROOT:$PATH"`; `UseSharedCompilation=false`; `-nodeReuse:false`. Fix warnings; never suppress them.
- **Instruments:** verdicts are ratios with denominators. Every scanner zero needs a positive control that fired. Timings run while other lanes may build: state the load average with every timing. zsh does not word-split `set -- $x` (`B57:487`). Never `cat` a file into itself (`B57:486`).

## End
The last line of `Briefs/2026-10-13_B58_STATUS.md` is exactly one of:
- `READY FOR GATE: b58/gate-b57-overlay-fix-round <sha>`
- `STOPPED: NEEDS FRIDAY`, followed by ONE question.
