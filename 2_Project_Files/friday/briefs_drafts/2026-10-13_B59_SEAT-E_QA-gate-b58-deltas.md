From Friday (laptop seat), Datasec / MPS Commercial Calculator. No mail key in this project: the STATUS file is the wrap.
# BRIEF B59 · SEAT-E: DELTAS QA GATE (TIER 1 throughout), ROUND 2 OF 2 for lane A3 (the catalogue overlay): `b58/gate-b57-overlay-fix-round` `727c7c8`, deltas `e6c9ced..727c7c8`, plus the MERGE onto main `d711b42` and the COMBINED tree
**Fired: 2026-10-13 03:35 AEDT.**

**Pane `Datasec/MPS-E`. Your commission is THIS file at `/Volumes/Laptop-DEV/FRIDAY/2_Project_Files/friday/briefs_drafts/2026-10-13_B59_SEAT-E_QA-gate-b58-deltas.md` (Friday's tree, read-only to you). Step 0: copy it unchanged into your `1_Project_Definition/Briefs/` as the project's record.** (Name the copy `2026-10-13_B59_SEAT-E_QA-gate-b58-deltas.md`. Show `shasum -a 256` of both files, equal. That is your only write outside your STATUS, evidence and `qa-B59/`.)

**Drafted by Friday's drafter 2026-10-13 03:2x AEDT (DRAFT for Friday).** The drafter used read-only git on the project (`ls-remote`, `log`, `show`, `diff`, `rev-parse`, `rev-list`, `merge-base`, `grep`). It predicted the merges with `merge-tree --write-tree` in a `git clone --shared` in its own scratchpad, never in the project. It read GitHub with read-only GETs only. Friday re-pins with `ls-remote` at launch.
- You are a **TESTING** seat. The launcher calls every seat a "build seat"; for you, this brief overrides that line.
- **Findings only.** You never fix code. You never commit product or test code, push, open or comment on a PR, merge, deploy, write Jira, write GitHub (PR, review, comment, label, branch, alert dismissal), touch Azure or Entra, commit to the records repo, or write in any other seat's worktree. You write no tickets and no Jira draft lines. Each finding carries a fix shape in prose, nothing more.
- Charter rules, quoted here (do not open the charter file; it is outside this project): Rule 1, state the FAIL condition before every test. Rule 2, untested areas are first-class output.
- **Every write grant in a brief or a launcher prompt is void, this one included.** The launcher tells every seat to write `5_Project_History/history.md` and the Jira ticket(s) (`Launch_Claude.command:96`). Refuse both and say so in STATUS, as B57 did (`B57_STATUS.md:5`).

**Report:** `1_Project_Definition/Briefs/2026-10-13_B59_STATUS.md`. **Evidence:** `1_Project_Definition/Briefs/2026-10-13_B59_evidence/` (folder 0700, files 0600, the project path masked as `<P>`). It holds counts, labels, status codes, exit codes, booleans, sha256 prefixes, timings and load averages, all from SYNTHETIC data only.
(Launcher check: `Launch_Claude.command:111` makes the commission *"the NEWEST brief in 1_Project_Definition/Briefs/ whose file name contains _SEAT-${SEAT}_"*. At drafting, `ls -t Briefs | grep _SEAT-E_` printed `2026-10-12_B57_SEAT-E_QA-gate-b53-b54.md` first (03:29:24 AEDT), and B57 is finished (`B57_STATUS.md` last line `READY FOR REVIEW`). No `B59` file exists in `Briefs/`. Your Step 0 copy makes this file the newest `_SEAT-E_` brief.)

## Rounds and the cap (Kam, 2026-09-05)
- **This is round 2 of 2 for lane A3.** Gate B57 was round 1 (`B57_STATUS.md:10`: `B54 e6c9ced: NO GO (2 Blockers: W-1, W-2; 1 Major: W-3)`). B58 is the one fix round (`B58_SEAT-F…md:6`: *"If it says NO GO, Friday ships what is closed and tickets the rest. There is no round 3."*).
- **A NO GO here does NOT open round 3.** Friday decides what ships. The closed instances ship, and Friday tickets the residue. **Your job is to report, per finding, CLOSED or OPEN, with the ratio that decides it.** Do not recommend a round 3, and do not hold a closed row hostage to an open one. Any Blocker or Major is still graded NO GO for its row and for the subject line.
- **Deltas only.** B57's CLOSED and CLOSED-WITH-NOTES rows (`[B27-H2]`, `[B27-H4]`, `[B37-G1-LOAD]`, `[B38-N6]`, `B57_STATUS.md:36-40`) are **not re-gated**. You check only that they stay green on the new trees (item 7). B53 (now on main) is not in scope beyond the combined suites.

## Verdict lines (each GO / GO WITH NOTES / NO GO), FIRST in STATUS, in this order
- `B58 727c7c8 (deltas e6c9ced..727c7c8): …`
- Per row: `(W-1) hand-off, next write after a Busy run: …` · `(W-2) .. after a directory link: …` · `(W-3/N-11) NFD vs NFC: …` · `(W-4) every Busy test ends with a write: …` · `(O3/O5) guard tests: …` · `(F) late-writer flake, 20/20 alone + 20/20 under load: …`
- Cross-cutting: `(R) red-proof by revert: …` · `(S) full suites base vs head vs combined: …` · `(M) mutants: …` · `(W) NEW WORDS: …` · `(L) leak + secret scan: …` · `(D) B58 STATUS deviations and UNMEASURED: …`
- `MERGE d711b42+727c7c8: …`
- `COMBINED d711b42+727c7c8 (tree 2f0e21eb): …` (prove the write sets are disjoint, the tree matches, and every lane blob is carried over unchanged; then the combined suites and probes)
- `overall: …`

Then one closure row per finding: **CLOSED / CLOSED-WITH-NOTES / NOT CLOSED / UNMEASURED / NOT IN SCOPE**, each with the ratio that decides it. Rows: `[B57-W1]`, `[B57-W2]`, `[B57-W3]`, `[B57-W4]`, `[B57-N11]`, `[B57-O3]`, `[B57-O5]`, `[B57-O6]`, `[B57-B1]`, `[B53-R8]`/CI run 38264207131 (the late-writer flake), `[B27-H1]` (code only; **the SITE HOLD stays**), `[B27-H3]`. Keep-green rows (item 7): `[B27-H2]`, `[B27-H4]`, `[B37-G1-LOAD]`, `[B38-N6]`. NOT IN SCOPE (B58 left them NOT THIS ROUND by brief, `B58_STATUS.md:238`): N-8, N-9, N-10, N-14, N-15/N-7, O4, `[B54-R1]`, `[B58-R1]`…`[B58-R6]`, V-1, V-2.

**Last line, exactly:** `READY FOR REVIEW: b58/gate-b57-overlay-fix-round 727c7c89b3c5c9ff0e28bcc14432e80624908165`. If you are stopped, the last line is **`STOPPED: NEEDS FRIDAY`** plus ONE blocking question.

## Authority
- **The pass conditions are B58's brief, read whole:** `Briefs/2026-10-13_B58_SEAT-F_gate-b57-overlay-fix-round.md` (268 lines): Tier 1 (`:84-89`), Row W-1 (`:93-110`), Row W-2 (`:111-132`), Row W-3 (`:134-145`), Row 4 table (`:147-165`), Test Evidence (`:167-185`), Write set and FROZEN (`:71-82`), HOLDS (`:235-252`), FRIDAY'S NOTE (`:260-268`, including the flake order at `:268`).
- **The ORIGINAL FAIL conditions are your oracle, not B58's restatement:** `B57_STATUS.md` W-1 `:372-383` (FAIL `:375`), W-2 `:385-391` (FAIL `:388`), W-3 `:393-396` (FAIL `:395`), W-4 `:398-401`, N-11 `:459`. The H-1 tier-1 text, verbatim (`:388`): *"a hosted start that succeeds when the reference file's final target sits in, contains or equals the overlay directory (any link form, any case form)"*. B58's brief adds: **"any case form" includes NFC/NFD for this round** (`B58…md:85`).
- **The builder's claims (claims, not facts):** `Briefs/2026-10-13_B58_STATUS.md` (290 lines, `wc -l`), whole. Its evidence folder (`2026-10-13_B58_evidence/`, 48 files), `.tools/qa-B58/` and `.tools/wt-B58*` may be **read**, and their tools **copied**. Nothing in them is proof for you. **Test every headline claim yourself.**
- **Headline claims under test** (B58 STATUS BLUF `:9-15`):
  - W-1 CLOSED: `var handoff = mine;` (`CatalogueOverlayStore.cs:497-498` at `727c7c8`). 5 new W-1 tests red at `e6c9ced`, green at head; the 1-writer case is a guard. Live: next write 200 ×3 in every run (H-3 / W-1 table `:168-181`; 32/32 head runs). Two hosts with no holder: both hosts 201 after every round that had 503s (3/3 rounds) (`:183-191`).
  - W-2 CLOSED: a private resolver `Physical` (`:324-357`) plus `Spellings` (`:238-239`); `QuoteFileStore.RealPath` untouched. L09 refused, L09b refused (it opened at `e6c9ced`), L09c control opens, L09d "cannot be built through configuration".
  - W-3 + N-11 CLOSED **by directory identity, not NFC** (`RefuseSameDirectory` `:248-264`, `Identity` via `DllImport` of `stat` `:279-316`). The reason given: `Directory.Build.props:9` `<InvariantGlobalization>true</InvariantGlobalization>` makes `string.Normalize(FormC)` a no-op (`:135`). **Declared consequence:** on a normalisation-sensitive disk (Linux) an NFD/NFC pair now **opens** (two real directories), where B58's brief expected "refuse, the safe direction" (`B58…md:139`; STATUS `:274`, needs-Friday 2 `:278`).
  - O3 guard test taken; O5 guard test added at `727c7c8`.
  - The flake (`OverlayGateFindingsTests.G1_a_writer_that_reaches_the_front_of_the_queue_late_still_answers_within_the_bound_from_arrival`, `OverlayGateFindingsTests.cs:328` at `727c7c8`): "not W-1"; the cause was the test's `Task.Run` on a starved pool; fixed in the test only; **20/20 alone (load 10.6–12.7) and 20/20 under load (20.3–112.2)** (`:13`, `:72`, `:125`).
  - Suites: base `e6c9ced` 1,094; head **"810 = 1,117 (+23)"** in the BLUF (`:14`) but **"811 = 1,118"** in Test Evidence (`:57`, `:59`). Red-first: **"22 red / 810"** (`:65`) then **"RED 23/23"** (`:70`). Reconcile both (item 5).
  - Red-proof: 22 tamper rows (+2 in run 2), every one RED; **run 1 was at `3ec9b5f`, not at the head** (`:75`).
  - NEW WORDS: 0 visible (11 literals: 3 reused templates, 8 internal) (`:240-247`).
- **These stand unchanged; you rule on none of them:** the **SITE HOLD**, the **P-1 / L-2 HOLD**, Q-09 (synthetic sets only), Q-16 (nothing is pruned or deleted), C-19.

## Tier-1 Blocker classes (whatever the path)
- **Overlay H-1:** a hosted start that succeeds when the reference file's **final target** sits in, contains or equals the overlay directory: any link form, any case form, **any normalisation form on a normalisation-insensitive disk**. Also, the other way: **a start refused with a regular-file reference path** (`B57:478`), and the shipped hosted layout refused (item 3, arm H0).
- **Overlay W-1:** a Busy answer that changed something; **a next write after a Busy run that is not 200/201** once nothing holds the lock.
- **Leak:** a price, SKU, cell value, planted marker, exception text (`Exception`, `--->`, `   at `, `.cs:line`), or an absolute build or worktree path in any HTTP response, problem `detail`, start-refusal **message**, or log line you can provoke. The one allowed path is the operator's own configured value for the setting being refused (your scratch path). Start refusals still print a host trace after the words (`[B54-R3]`, parity). Judge the message, and count the trace separately.
- **Any frozen path in the delta** (`B58…md:76-81`). `web/**` changed. A real price book opened by anything you start. A real-client datum in anything you write. Anything deployed.

## Targets (re-pin at start and again before the verdict)
| What | Ref | Pin (instrument, time) |
|---|---|---|
| Main (base) | `refs/heads/main` | **`d711b42cfcb53da3a2043a2d672511f8ea6ea296`** (`git ls-remote origin`, 03:27:48–03:27:51 AEDT, rc 0); tree **`ef5cd1566b0804614418bcb533a0057126d87fd3`** (`git log -1 --format=%T`). One parent, `1329f2e`. Subject: *"Source version store hardening (B53; gate B57 GO WITH NOTES) (#29)"*. PR #29: `closed`, `merged` true, `merge_commit_sha` = `d711b42…` (`gh api …/pulls/29`, read-only GET, 03:29:04 AEDT). Its tree equals B57's predicted `merge-tree 1329f2e 3852d30` = `ef5cd156…` (`B57_SEAT-E…md:80`). |
| Subject | `refs/heads/b58/gate-b57-overlay-fix-round` | **`727c7c89b3c5c9ff0e28bcc14432e80624908165`** (same `ls-remote`; = B58 STATUS last line `:290`); tree **`b9987176be2c90919fed638ab2de8cc0f21426ea`** |
| Round-1 subject (lane base) | `refs/heads/b54/overlay-store-residue` | **`e6c9cedbf760e9ca2f5957703f420267c9189bf8`** (same `ls-remote`; unchanged since B57); tree **`32a6c31719182e528c4cd944dcf568c27aa9a0e8`** |
| B53 branch (already landed) | `refs/heads/b53/source-store-hardening` | `3852d309…` (same call; = `refs/pull/29/head`) |

**First action:**
1. `git -C 2_Project_Files fetch origin`.
2. `git ls-remote origin refs/heads/main refs/heads/b58/gate-b57-overlay-fix-round refs/heads/b54/overlay-store-residue`. All three must equal the pins. **If any differs, STOP: NEEDS FRIDAY.**
3. Run the same `ls-remote` again before the verdict. A moved head voids the verdict. A moved main voids the MERGE and COMBINED lines.

**Measured by Friday's drafter (re-measure; do not trust):**
- **Chain:** `e6c9ced..727c7c8` = 7 commits, 0 merges (`rev-list --count`, `--merges`); `306a2c0^` = `e6c9ced…` (`rev-parse`); `merge-base --is-ancestor e6c9ced 727c7c8` rc 0. So no rebase.
  | Commit | Subject (short) | numstat (`diff --numstat <c>^ <c>`) |
  |---|---|---|
  | `306a2c0` | W-1: a writer that gives up its turn hands it on | store +5/−2; `OverlayGateB57Tests.B58.cs` +242; `OverlayGateFindingsTests.cs` +25/−6; `OverlayResidueTests.B54.cs` +8 |
  | `a2eb9d2` | W-1 follow-up: the hand-off's own unobserved faults | test file +19/−7 |
  | `899202e` | W-2: resolve overlap paths as the kernel does | store +97/−34; test file +157 |
  | `8cf2890` | W-3: refuse an overlap by directory identity | store +86/−1; test file +109/−1 |
  | `b560b14` | row 4 (O3) guard | test file +37 |
  | `3ec9b5f` | W-3 follow-up: accented control on a normalisation-sensitive disk | test file +11/−4 |
  | `727c7c8` | row 4 (O5) guard | test file +34 |
- **The product file changes in 3 commits only** (`306a2c0`, `899202e`, `8cf2890`). `git diff --stat 8cf2890 727c7c8 -- src` is **empty**, so the product at `8cf2890` = the head's product.
- **Delta write set** (`diff --numstat e6c9ced 727c7c8`): 4 paths, **+810 / −35**: `src/MpsCalc.Api/Inventory/CatalogueOverlayStore.cs` +180/−29, `tests/MpsCalc.Api.Tests/OverlayGateB57Tests.B58.cs` +597 (new), `OverlayGateFindingsTests.cs` +25/−6, `OverlayResidueTests.B54.cs` +8. = the 4 paths allowed (`B58…md:71-75`).
- **Frozen numstat** (`diff --numstat e6c9ced 727c7c8 -- src/MpsCalc.Api/Quotes src/MpsCalc.Api/Program.cs src/MpsCalc.Api/Sources src/MpsCalc.Api/Inventory/InventoryEndpoints.cs src/MpsCalc.Api/Contracts src/MpsCalc.Api/Feedback src/MpsCalc.Api/Infrastructure src/MpsCalc.Engine src/MpsCalc.Import docs web infra scripts .github '*.csproj' Directory.Build.props tests/MpsCalc.Api.Tests/Infrastructure`): **empty**, rc 0.
- **Public surface:** `PathKey`, `FileName`, `LockFileName` byte-equal in value (`CatalogueOverlayStore.cs:81-83` at `e6c9ced`, `:82-84` at `727c7c8`: one line moved). `SourceLifecycle.cs:148` (main `d711b42`) still reads `CatalogueOverlayStore.PathKey`. `Program.cs:60`/`:62` (main) call `OpenHosted` / `Open`.
- **Merge prediction** (scratch `git clone --shared`, git 2.54.0 (Apple Git-157), 03:28:17 AEDT):
  - `merge-tree --write-tree d711b42 727c7c8` → **rc 0, tree `2f0e21eb4c77184d557a033151448ecc2a8e6c2d`**, no conflict lines. (= B58 STATUS `:41`, `:204`.)
  - Control: `merge-tree --write-tree d711b42 e6c9ced` → rc 0, `23bacbada3562876e7c235c8984d332eabcb2fbd` (= gate B57's combined tree, `B57_STATUS.md:48` and `B58_STATUS.md:39`).
  - `diff --name-only d711b42 2f0e21eb` = 5 paths (B54's 4 + B58's new test file; +1,439 / −56). `diff --name-only 23bacbad 2f0e21eb` = exactly B58's 4 paths.
  - **Blob equality:** those 5 paths in `2f0e21eb` = `727c7c8`'s blobs **5/5**; PR #29's 5 paths (`diff --name-only 1329f2e d711b42`: `Sources/{SourceAdminEndpoints,SourceDocumentChecks,SourceLifecycle}.cs`, `SourceLifecycleTests.{B53,GateB41}.cs`) in `2f0e21eb` = `d711b42`'s blobs **5/5**. Intersection 0.
  - `rev-list --left-right --count d711b42...727c7c8` = **`2 12`**; `merge-base` = `b28c95eb`. **B58 was never built or tested on `d711b42`.** B58 skipped the merged-tree suite because main did not move during its run (`M1 = M0`, STATUS `:41`, `:205`). **Your combined run is the first measurement on the merged code.**
- **Text-disjoint is not semantics-disjoint.** Re-measure:
  - The overlay no longer calls `QuoteFileStore.RealPath` (`git grep -n RealPath 727c7c8 -- src/MpsCalc.Api/Inventory` → 0 lines; at `e6c9ced`, `:196`, `:197`, `:232`). B53's `SourceLifecycle.cs:934-935` (main) still calls it, and `:165` uses `ResolveLinkTarget(returnFinalTarget: true)`. Those are B53's W-2/W-3 class (`[B58-R4]`, `[B58-R5]`): NOT IN SCOPE. Say so; do not probe them as findings.
  - `Identity` (`:279-301`) branches on `OperatingSystem.IsMacOS()` and on `RuntimeInformation.ProcessArchitecture == X64` (`stat$INODE64`, `:309`), and uses `libc.so.6` on Linux (`:313`). Only macOS arm64 and Linux arm64/amd64 containers were measured by B58 (`:136`).
- **CI / CodeQL:** `gh api …/commits/727c7c8…/check-runs` → `total_count` **0**; `gh api …/pulls?state=open` → **0 open PRs** (both read-only GETs, 03:29:04 AEDT). `ci.yml` runs on `pull_request` and on pushes to `main` only (`on:` block), and CodeQL is the org's default setup (`ci.yml` header). So nothing has scanned `727c7c8` yet.
- **Shipped hosted layout** (`infra/modules/showcase.bicep:81-83` at `d711b42`): `MpsCalc__ReferenceStorePath` `/home/data/pricebooks/reference.json`, `MpsCalc__QuoteStore__Path` `/home/data/quotes/`, `MpsCalc__CatalogueOverlay__Path` `/home/data/catalogue-overlay/`. Item 3 rebuilds this **shape** under your synthetic hosted root. You never touch hosted.
- **Ports:** `lsof -nP -iTCP:6650-6659 -sTCP:LISTEN` at 03:29:24 AEDT → 0 lines (rc 1). B57 used this range and has finished (`B57_STATUS.md:516`). `6680-6689` (B58's) → 0 lines at the same time.
- `.tools/wt-B59*` and `.tools/qa-B59` do not exist (zsh glob: no matches, 03:29:24).

## Your setup (own worktrees, own ports, own state)
- **Clones** (git verbs that write are allowed **only** here): `git clone --shared '<project>/2_Project_Files' '<project>/.tools/qa-B59/clone'` (0700). Then `remote set-url --push origin NO-PUSH`, and show that a dry push fails. In the clone: `checkout --detach d711b42…`, then `merge --no-ff --no-edit 727c7c8…` (local identity `qa-b59@invalid`, never pushed). Assert `rev-parse HEAD^{tree}` = **`2f0e21eb…`**. **If it differs, STOP: NEEDS FRIDAY.**
- **Worktrees** (0700, never removed). From `2_Project_Files` (`worktree add --detach` only): `wt-B59-main` @ `d711b42`; `wt-B59-head` @ `727c7c8`; `wt-B59-e6` @ `e6c9ced`. From **your clone**: `wt-B59-comb` @ the combined commit (tree `2f0e21eb`); `wt-B59-red` @ `727c7c8` (the revert staircase, item 1); `wt-B59-mut` @ `727c7c8` (mutants, restored by sha256); `wt-B59-clean` @ combined and `wt-B59-e6-clean` @ `e6c9ced`, for `scripts/package.sh` and nothing else. **Run every `worktree add` from `bash -c '…'` with each path quoted** (B57's incident 2: zsh does not word-split `set -- $x`, and five worktrees got the sha in their names, `B57_STATUS.md:487`).
- **Tool output:** `…/.tools/qa-B59/` (0700). Point every cache, log and TRX there.
- **Copied instruments** (copy into `qa-B59/tools/`; never edit or run them in place): from `qa-B57/tools/`: `h1_57.py`, `h1all.sh`, `h3_57.py`, `h3_57b.py`, `h3matrix.sh`, `h4_57.py`, `qlib57.py`, `oidc_stub57.py`, `jwt57.py`, `stubctl.py`, `pkg.sh`, `mutrun57.py`, `muttable57.py`, `tamper54_copy.py`, `leak57.py`, `leakscan.py`, `qalib.py`, `words57cs.py`, `parity57.py`, `load57.sh`, `suite.sh`. From `qa-B58/tools/`: `h1_58.py`, `h1all58.sh`, `h3_58.py`, `h3matrix58.sh`, `twohost58.py`, `mutrun58.py`, `tamper54_b58copy.py`, `words58cs.py`, `leak58.py`, `boost58.sh`, `loop58.sh`. Re-derive every anchor at the commit you mutate (count 1/1). Name every copied script in STATUS. Show that each control fired **in this run**. Make new keys in `qa-B59/keys/` (0600); never reuse another gate's or seat's key.
- **Synthetic data, your own:** reference files, overlays and layouts under `qa-B59/roots/` and `$(getconf DARWIN_USER_TEMP_DIR)qa-B59-ci/` (0700), `SYN-B59-*` codes. Every process you start sets `MpsCalc__ReferenceStorePath` to **your synthetic** reference file. **Never `.local/pricebooks/`.** Never start a process on the shipped Development reference path (`appsettings.Development.json:4`).
- **Volumes:** measure and print both volumes' case **and** normalisation rules (B58 measured: project volume case-sensitive, normalisation-insensitive; temp volume case-insensitive, normalisation-insensitive, `B58_STATUS.md:147`).
- **Allowed git verbs.** In `2_Project_Files`: `fetch`, `ls-remote`, `worktree add --detach` only. In your own `wt-B59*`: `checkout --detach`, `checkout <sha> -- <path>` (staircase only, in `wt-B59-red`), `restore`, `status`, `diff`, `show`, `log`, `rev-parse`, `archive`. In `qa-B59/clone`: anything local, never `push`. Records repo (project root): read-only. **Forbidden everywhere else:** any branch or tag on a shared repo, `push`, `merge` into a shared ref, `rebase`, `gc`, `prune`, `worktree remove/prune`, `reset` on a shared ref, deleting any lock, and any force.
- **Ports (yours only): 6650–6659. Run `lsof -nP -iTCP:<port> -sTCP:LISTEN` before every bind.** On any listener that is not yours, **STOP: NEEDS FRIDAY**; do not move ranges.

  | Port | Process |
  |---|---|
  | 6650 | combined, DevStub Release (W-1 live; two-host host A) |
  | 6651 | combined, DevStub Release (two-host host B) |
  | 6652 | `e6c9ced`, DevStub Release (red-first live) |
  | 6653 | combined, Entra-fake Production, real package from `wt-B59-clean` (H-1 layouts, H-4 spot) |
  | 6654 | `e6c9ced`, Entra-fake Production, real package from `wt-B59-e6-clean` (H-1 base) |
  | 6655 | main `d711b42`, DevStub Release (overlay success-path parity) |
  | 6656 | `727c7c8` alone (only when a claim must be shown on the published SHA) |
  | 6657–6658 | spare |
  | 6659 | OIDC/JWKS stub (your copy) |

  **Never bind** the ranges B57 listed (`B57_SEAT-E…md:130`), and 6680–6689 (B58's, finished). That list was not re-measured for current use: `lsof` first, every time.
- **.NET:** `export DOTNET_ROOT='/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator/.tools/dotnet' PATH="$DOTNET_ROOT:$PATH"`. Build with `-nodeReuse:false -p:UseSharedCompilation=false`. **After every staircase step or tamper restore, `touch` the file and build `--no-incremental`.**
- **Processes:** stop them by port + cwd, or by a pid you recorded; never by name. Everything you started is stopped before READY. `caffeinate`, the shared `VBCSCompiler`, `@playwright/mcp` and other seats' containers are not yours.
- **Instruments:** run `cmd > out 2>&1; rc=$?`; never take an exit status through a pipe. **Never `cat` a file into itself** (B57's 43 GB incident, `B57_STATUS.md:486`). Every verdict is a ratio with its denominator. Every scanner zero and every tamper needs a control that fired. The shell is zsh: run loops and multi-word variables via `bash -c '…'`. **State the load average (`uptime`) with every timing.**

## Items (round 2, deltas). State each FAIL condition before you run it.
0. **Pins, trees, partition, merge, frozen.**
   - Re-pin, and confirm the three trees above.
   - Run `git diff --name-status` per commit for the 7 commits. Map each to its row (W-1, W-2, W-3, O3, O5). **A path outside the 4-path write set is a finding.**
   - Frozen numstat = 0 lines over the list in Targets. `git diff --numstat e6c9ced 727c7c8 -- web docs` empty.
   - **MERGE / COMBINED:** reproduce `2f0e21eb` in your clone. Show blob equality 5/5 (lane) and 5/5 (PR #29), and the intersection 0 (`comm -12`). Re-measure each coupling in Targets, quoting the line. FAIL: the tree differs, an intersection > 0, or a coupling changed.
   - **Through the code:** walk B58 rows W-1, W-2, W-3 and row 4, bullet by bullet, against the diff. Record per bullet MET / NOT MET / NARROWED-AND-DECLARED, with the `file:line` at `727c7c8`. A bullet that is neither met nor declared is a finding.
1. **(R) Red-proof by REVERT, not by reading (TIER 1; decides W-1, W-2, W-3).** In `wt-B59-red` (detached `727c7c8`: the head's tests throughout), replace **only** `src/MpsCalc.Api/Inventory/CatalogueOverlayStore.cs` with each commit's version (`git checkout <sha> -- <that path>`), rebuild `--no-incremental`, and run the whole `MpsCalc.Api.Tests` project. A staircase:
   | Step | Product file from | Expected (from B58's claims) |
   |---|---|---|
   | R0 | `e6c9ced` | every new W-1, W-2 and W-3 test RED; the W-4 steps on the 5 pre-existing tests RED (`B58_STATUS.md:67`); guards green (`after_writers(1)`, L09c ×2, the accented control ×2, O3) |
   | R1 | `306a2c0` (W-1 only) | W-1 tests and the W-4 steps GREEN; W-2 and W-3 tests still RED |
   | R2 | `899202e` (W-1 + W-2) | W-2 tests GREEN (L09, L09b, L09d); W-3 tests still RED (L17, L18, containment) |
   | R3 | `8cf2890` (= head product) | all GREEN |
   - Report a RED/GREEN matrix **by test name × step**, with counts (n red / N run). Each finding is CLOSED only if its own tests flip at its own step and at no other step. A test that is RED at R3, or that never goes RED, is a finding (a test that cannot see its fix).
   - **One-line causal check for W-1** (independent of B58's `W1a`): at `727c7c8`, make the continuation read `mine` again (anchor `handoff.TrySetResult()`, 1/1). W-1 tests must go RED. Restore by sha256.
   - Restore `wt-B59-red` to `727c7c8` at the end: `status --porcelain` empty, sha256 equal.
   - FAIL: any of W-1, W-2 or W-3 without at least one test that is RED at the step before its fix and GREEN at its fix.
2. **W-1 live (TIER 1), on the COMBINED tree** (DevStub Release 6650; red-first on `e6c9ced` 6652). Copy `h3_57.py` / `h3matrix.sh` (or B58's `h3_58.py`).
   - **Original FAIL** (`B57:375`): *"any next write after release that is not 200."*
   - Hold `overlay.lock` from another process (`flock`, then `fcntl`, each with a control that blocks). Run N = 2, 3, 16, 64 and 64 mixed POST+PATCH, ≥ 3 runs each for `flock`, 1 run each for `fcntl`. Per run report: late / N (> 5.5 s from **client send**), max, median, the read time during the wait, **the next write after release (3 single writes, 1 s apart)**, and the load average.
   - Red-first: N = 2 and 16 on `e6c9ced` → 503 ×3 (B57: 23/23; B58: 2/2).
   - **Two hosts, no outside holder** (copy `twohost58.py`): 6650 + 6651 on one overlay, N = 250 POSTs per host, 3 rounds. After every round that produced any 503, **both hosts answer 201 to every later write**. Then read the disk: version = rows = number of 201s, audit 1..n, none lost, none duplicated. If no round produces a 503, say so and raise N until one does (state N and load).
   - FAIL: any next write not 200/201; a Busy that changed anything; a read ≥ 1 s. (A late answer > 5.5 s under a load you state is a Minor, not a Blocker.)
3. **W-2 / W-3 live: the H-1 layout re-run (TIER 1), on the COMBINED package** (Entra-fake Production on 6653, real package from `wt-B59-clean`, gate-random GUIDs, `AzureAd__MetadataAddress` → your stub on 6659, tokens minted locally and never printed; base `e6c9ced` package on 6654; **both volumes**; fresh roots per layout).
   - **Original FAIL:** the H-1 text above (`B57:388`), "any case form" incl. NFC/NFD.
   - Layouts: B57's L00–L20 plus B58's L09b, L09c and L09d (copy `h1_58.py` / `h1all58.sh`, layout definitions read as data). Expected per B58 (`B58_STATUS.md:144-166`): refuse layouts **18/18 per volume** at combined, base 14/18; controls L00, L03, L16, L09c open 4/4; L19 (hard link) opens (N-14, declared).
   - **The gate's own arms (not in B58's set):**
     - **H0, the shipped hosted shape** (`showcase.bicep:81-83`) under your synthetic root: `<HR>/data/pricebooks/reference.json` (a regular file), `<HR>/data/quotes/`, `<HR>/data/catalogue-overlay/`, trailing separators as shipped. **Must open at combined, on both volumes.** A refusal here is a tier-1 FAIL (a hosted outage after deploy).
     - **H0-id, identity false positives:** the overlay and the reference directory are siblings on the same device (one parent), and the reference directory's parent is reached through a directory link. Must open. *(Every overlap test so far ran on one device; a compare that read the device only, or a wrong offset, would refuse every hosted start. Item 6, mutant G3, checks the suite sees it.)*
     - **NFD quote store:** `MpsCalc__QuoteStore__Path` spelled in NFD for an NFC overlay directory (or the reverse), where the hosted rule lets you build it. State what `ResolveHosted` does with it. Expected: refused, or "cannot be built" with the reason measured.
     - **NFD + case together:** an NFD link target with a case change into the overlay (on the case-insensitive volume). Expected: refused.
     - **The overlay directory absent at start**, with an NFD link to a reference file inside the (NFC) path it will occupy. State whether the start opens and what it then writes, and why `Identity` (null for a missing path, `:275`) leaves this to the name compare.
   - For each layout record: exit code, listener (`lsof`), the message (verbatim, scratch paths only), the trace class, and the files beside the real file before and after. **If any layout opens and should not, send one POST to `manual-items` and count the files written beside the real file** (B27's measurement).
   - Replicates on fresh roots: L09, L09b, L17, L18, H0, 3 per volume each.
   - **The changed situation for existing words** (B58 `:245`): `{other}` now quotes the configured spelling made absolute (`Rooted`), not the collapsed one. Confirm that each refusal quotes only your configured scratch value, never another path.
   - **W-3's declared Linux behaviour:** B58 says that on a normalisation-sensitive disk an NFD/NFC pair opens. You have no Linux host: list it UNMEASURED by you, cite B58's container evidence (`15_linux-*`) as a claim, and put the policy question in `## needs-Friday` (see Notes).
   - FAIL: any Blocker class.
4. **(F) The late-writer flake (Friday's order, `B58…md:268`).**
   - Test: `OverlayGateFindingsTests.G1_a_writer_that_reaches_the_front_of_the_queue_late_still_answers_within_the_bound_from_arrival` (`OverlayGateFindingsTests.cs:328` at `727c7c8`).
   - **FAIL condition:** any red in 20 runs alone, or in 20 runs under load.
   - Run it **×20 alone** and **×20 under load** (a second suite looping from `wt-B59-main`, plus boosters; reach **load ≥ 80** in at least 5 of the 20), on **`727c7c8` AND on the combined tree**. Report n/20, load before / after / peak per batch.
   - Do the same ×20 + ×20 for the new timing class `OverlayGateB57TimingTests` (it joins the same xUnit collection, `OverlayGateB57Tests.B58.cs:20`): new timing tests are new flake risk.
   - **Causal check of B58's diagnosis** (`B58_STATUS.md:13`, `:125`): in `wt-B59-mut`, put back only that test's `e6c9ced` body (the two `Task.Run(() => Assert.Throws(() => AddRow(…)))` writers and the 10 s holder), keep the product at head, and run it ×20 under the same load. If the old body fails and the new body does not, the diagnosis is supported. If neither fails, the cause is **UNMEASURED**: say so; do not claim it.
   - **Weakened guard?** B58 says *"Assertions unchanged in strength"* (`:257`). Compare old vs new (`git diff e6c9ced 727c7c8 -- tests/MpsCalc.Api.Tests/OverlayGateFindingsTests.cs`). In particular, both writers now join through `MutateAsync` on the test thread, so the test no longer exercises the sync `Mutate` wrapper on a pool thread. Say whether anything that test used to prove is no longer proved elsewhere.
5. **(S) Suites: main `d711b42` vs combined; `727c7c8` alone vs `e6c9ced`.**
   - .NET Release `--no-incremental`, 0 warnings, all four trees. `dotnet list package --vulnerable --include-transitive` 0 (7/7).
   - Counts: **UNMEASURED by the drafter.** By arithmetic only (not a measurement): `d711b42` = B57's base 1,153 + B53's 63 = 1,216 (`B57_STATUS.md:360-361`); combined = 1,216 + B54's 45 + B58's 24 cases = 1,285 (B58 `:59`: +14 methods, +24 cases). Reproduce `e6c9ced` = 1,094 and `727c7c8` alone. **Reconcile B58's two head counts** (810 / 1,117 at `:14` vs 811 / 1,118 at `:57`) by name (`--list-tests`, `comm`): 0 names lost, every added name belongs to B58.
   - **Repeat the full combined API suite ≥ 5 times and the main suite ≥ 5 times**, with `uptime` each time. Count failures by name. FAIL: any red that main does not show at the same rate, any warning, a count that does not reconcile.
   - Modified pre-existing tests: B58's table (`:249-263`, 11 rows). Check each before → after by diff. Each must only gain a step; say whether any assertion was removed or loosened.
6. **(M) Mutants, at `727c7c8` and on the combined tree.**
   - **B58's own run 1 was at `3ec9b5f`, not at the head** (`:75`). Re-run at least 8 of B58's rows **at `727c7c8`**: `W1a`, `O6`, `B1` (burst only), `W2a`, `W2b`, `W2c`, `W3a`, `W3b`, `O5`. Confirm each RED count and list the red test names.
   - **At least 5 of your own**, independent of B58's:
     - (G1) `Spellings` keeps only `Physical(path)` (drops the collapsed spelling): L09b should go RED;
     - (G2) `Physical` applies `..` with `Path.GetDirectoryName` on the **unresolved** string prefix for the reference only (not the overlay);
     - (G3) `Identity` returns `(device, 0)` (device only): every same-device compare matches. **Something must go RED** (the controls L00, L03, L16, L09c, or your H0). If nothing does, that is a finding: the suite cannot see a false refusal of every hosted start;
     - (G4) `RefuseSameDirectory` checks equality only, both ancestor walks removed (B58's `W3b` removes "inside/contains" only on one side: say how yours differs);
     - (G5) the hand-off continuation uses `TaskContinuationOptions.OnlyOnRanToCompletion`;
     - (G6) `mine = null;` removed (the `finally` then completes the timed-out writer's turn at once: the turn is handed on early). Must go RED on the suite or on your probe (two writers inside the file lock at once, or a version written twice).
   - Each tamper must go RED on the full suite **or** on your probe; say which. A tamper green on both is **UNVERIFIED**, with the term named. Prove each restore by sha256 and an empty `status --porcelain`.
7. **Keep-green (regression only; one pass each; combined tree).**
   - H-4: B27's 4 + B54's 4 malformed forms refused at boot (Entra-fake 6653), file byte-unchanged; the running 503 detail unchanged on POST and PATCH (copy `h4_57.py`). FAIL: any form that starts, or a changed detail.
   - Overlay success path, main `d711b42` (6655) vs combined (6650), no contention: `GET /inventory`, `GET /inventory/audit`, `POST /inventory/manual-items`, `PATCH /inventory/{key}`, then a restart and the same reads. Overlay version and audit sequence equal; bodies equal after normalising the ids and times you name. FAIL: any difference you cannot name.
   - The G1 burst group ×20 alone and ×20 under load (load ≥ 80 at least 5 times), per run "a × 201, b × 503", and the W-4 write after the burst. FAIL: any red run.
8. **(W) NEW WORDS.**
   - Re-extract with a copy of `words57cs.py` / `words58cs.py` over `e6c9ced...727c7c8`, non-test C# under `src/`, with your own planted control in an unpushed commit in your clone (it must be flagged 1/1).
   - Claim (`B58_STATUS.md:240-247`): **0 visible strings added or changed**; 11 literals = 3 reused templates (`:254`, `:258`, `:262`, byte-equal to `:212`, `:216`, `:220`) + 8 internal (`"libc"` ×2, `"stat"` ×2, `"stat$INODE64"`, `"libc.so.6"`, `"."`, `".."`). Also the W-1 Busy text at `:500-501` is unchanged from `e6c9ced`.
   - List each verbatim under `## NEW WORDS (for Kam)`, **declared** or **undeclared**, with `file:line` at `727c7c8`. Any undeclared API- or operator-visible string is a **Minor**. Also list the changed situations for existing words (refusals that now fire for L09, L09b, L17, L18; `{other}` quoted as configured).
9. **(L) Leak and secret scan.** A copy of `leak57.py` (or `leak58.py`) over the added lines of `e6c9ced...727c7c8` and `git log --format=%B e6c9ced..727c7c8`, counts only, with a planted control per class. `gitleaks git --redact` over the range, with a fresh control repo. Re-adjudicate B58's hits (`:208`: e-mail 3 = `admin@example.test`; 1 timing constant). **The price-book, store-SKU and credential-fragment classes are NOT TESTED** (their lists need `.local/pricebooks/` and `4_Credentials/.env`, both forbidden). Self-scan your STATUS and evidence before READY: 0.
10. **(D) B58's deviations and UNMEASURED items: rule on each one.** For each, give MEASURED-BY-GATE (with your ratio), ACCEPTED-AS-DECLARED, or UNMEASURED:
    - (a) the two head counts (810/1,117 vs 811/1,118) and the red counts (22/810 at `:65` vs "RED 23/23" at `:70`): item 5;
    - (b) the tamper table's run 1 at `3ec9b5f`, not at the head: item 6;
    - (c) the H-1 packages built from `b560b14` (`:145`; `b560b14..727c7c8` is test-only, `git diff --numstat b560b14 727c7c8 -- src` empty at drafting): your item 3 packages come from the combined tree;
    - (d) Linux runs at `3ec9b5f` (`:62`) and the Linux "opens" branch for W-3 (`:137`): UNMEASURED by you (no Linux host); cite them as claims;
    - (e) W-3 built by identity, not NFC (`:135-136`, `:274`): graded as built in item 1/3; the Linux "opens" policy goes to needs-Friday;
    - (f) the `727c7c8` commit message says the O5 guard is *"Green at e6c9ced"*, and STATUS `:69`/`:122` corrects it to RED through W-1. Your R0 step decides it;
    - (g) O4 UNVERIFIED (`:100`, `:268`): NOT IN SCOPE, as at B57;
    - (h) B58's CodeQL note: the new `DllImport`s may draw a CodeQL note (`:267`). NOT TESTED by you unless item 11 can read it;
    - (i) the macOS x64 branch (`stat$INODE64`, `:309`) and the hosted App Service C library (`[B58-R6]`, `:266`): UNMEASURED; say what a wrong answer would do (`Identity` null → the name compare only; a wrong offset → see G3).
11. **CodeQL / CI.** At drafting, 0 check runs on `727c7c8` and no open PR (Targets). If a PR exists when you run **and** this seat has a **read-only** GitHub identity for `datasecau`, read the check runs and code-scanning alerts (counts, rule ids, `file:line`; never dismiss, comment or re-run). Otherwise list each as **NOT TESTED** with the reason (B57 `:498`: `gh auth status` rc 1). Never borrow another project's identity. **CodeQL is required by Datasec org policy before merge**: say so in NOTES FOR FRIDAY.

## NOTES FOR FRIDAY (hosted): counts only. You have NO hosted access and make no hosted request.
Hosted runs `1329f2e` (B55). The overlay is on hosted (`Program.cs:60` `OpenHosted`). Write one `NOTE FOR FRIDAY (hosted)` per change, each with its FAIL condition for a later deploy brief. Every number comes from your local measurement or a cited STATUS:
- **W-1:** what the fix changes on hosted (an instance no longer stays Busy after a timed-out wait with ≥ 2 waiters). **PRE-2** (`B57_STATUS.md:506`) is still owed against the package: hold `overlay.lock`, 2 waiting writes, release, one write → 200.
- **W-2/W-3:** the overlap guard now calls `stat(2)` through `DllImport` at **every hosted start**. Give your H0 ratio (the shipped shape opens). State what remains UNMEASURED on hosted: the `/home` share's case and normalisation rules (`B57:492`), whether `stat` returns stable device/inode numbers on that share, and the image's C library (`[B58-R6]`).
- **The SITE HOLD:** H-1 is code on a branch. Say what fixing W-2/W-3 changes and what remains (B54 STATUS `:242-247` (a)–(e): merged with CodeQL green; Kam sees the NEW WORDS; the P-1 / L-2 hold; the deploy plus post-deploy P-7 and a start check; a brief that lifts it). **You do not lift it.**
- PRE-1 (`[B54-R1]`, hosted `overlay.json` fields) is unchanged by B58. If Friday rules N-8 (`[B58-R1]`) as "empty = missing", PRE-1 must count empty `by` too.

## needs-Friday (the gate's view; Friday rules)
- **W-3's Linux behaviour** (B58 needs-Friday 2, `:278`): on a normalisation-sensitive disk an NFD/NFC pair now opens, where B58's brief asked for "refuse, the safe direction". Give your view: is "opens when they are truly two directories" acceptable for the tier-1 text, given the hosted share's rule is UNMEASURED?
- N-8 (`[B58-R1]`): carried from B58; no gate test owed this round.

## NOT TESTED here (list each in STATUS with its reason; none is a gate pass)
- **Hosted:** nothing deploys; no hosted read. Real Entra. The SMB share. Linux / CI file semantics (macOS APFS only; B58's container runs are claims). Windows (`Identity` returns null there, `:281-284`). macOS x64.
- CodeQL / CI, unless item 11 could read them. The price-book, store-SKU and credential-fragment leak classes (holds). Real price books (Q-09).
- B53's own overlap and link checks (`[B58-R4]`, `[B58-R5]`), V-1, V-2: lane B53, NOT IN SCOPE. N-8, N-9, N-10, N-14, N-15/N-7, O4, `[B54-R1]`: B58's NOT THIS ROUND, by brief.

## Severity, findings, STATUS shape
- Severities: **Blocker / Major / Minor / Note.** Tag each finding **B58** (in the delta), **COMBINED** (appears only on the merged tree) or **PRE-EXISTING** (`e6c9ced` parity, measured), and **INTRODUCED** where the delta caused it.
- **Each finding:** an ID (`Y-1…` for B58, `Z-1…` for combined), severity, `file:line` at `727c7c8` (or at the combined tree for Z), then **FOUND** / **TESTED** (FAIL condition, steps, expected vs actual, counts) / **HOW** (fix shape plus regression test, in prose). Write no code.
- **STATUS skeleton.** Fill every `{{PLACEHOLDER}}`, in this order. Leave none unfilled: write UNMEASURED or NOT TESTED with a reason instead.
```
# B59 STATUS · SEAT-E · deltas QA gate (tier 1), round 2 of 2 (lane A3): `b58/gate-b57-overlay-fix-round` `727c7c8` on main `d711b42`
Seat E (pane `Datasec/MPS-E`), a Claude testing seat. Client: Datasec only. Commission: {{COMMISSION_PATH_AND_STEP0_SHA256_PAIR}}
Launcher preflight, verbatim: {{PREFLIGHT_LINES}}
Grants refused: {{HISTORY_AND_JIRA_REFUSAL_LINE}}

## Verdict lines
- `B58 727c7c8 (deltas e6c9ced..727c7c8): {{VERDICT}}` ({{BLOCKER_MAJOR_COUNTS}})
- Per row: `(W-1) …: {{V}}` · `(W-2) …: {{V}}` · `(W-3/N-11) …: {{V}}` · `(W-4) …: {{V}}` · `(O3/O5) …: {{V}}` · `(F) …: {{V}}`
- Cross-cutting: `(R) {{V}}` · `(S) {{V}}` · `(M) {{V}}` · `(W) {{V}}` · `(L) {{V}}` · `(D) {{V}}`
- `MERGE d711b42+727c7c8: {{V}}`
- `COMBINED d711b42+727c7c8 (tree 2f0e21eb): {{V}}`
- `overall: {{V}}`
- Cap: round 2 of 2. {{CLOSED_LIST}} closed; {{OPEN_LIST}} open. Friday decides what ships; no round 3.

## Closure table
| Row | State | Deciding ratio |
{{ONE_ROW_PER_FINDING_AS_LISTED_IN_THE_BRIEF}}

## BLUF
{{3_TO_8_BULLETS}}

## Step 0 and pins
{{COPY_SHA256_BOTH_FILES}} · {{PIN_TABLE_START_AND_BEFORE_VERDICT_WITH_TIMES_AND_RC}}

## Trees, merge, partition, frozen
{{TREE_2F0E21EB_REPRODUCED}} · {{BLOBS_5_OF_5_AND_5_OF_5}} · {{COMM_INTERSECTION}} · {{COMMIT_MAP_7_ROWS}} · {{FROZEN_NUMSTAT_PASTED}} · {{COUPLINGS_TABLE}} · {{THROUGH_THE_CODE_BULLETS}}

## (R) Red-proof by revert
{{STAIRCASE_MATRIX_TEST_NAME_BY_STEP_R0_R1_R2_R3}} · {{W1_ONE_LINE_CAUSAL}} · {{RESTORE_PROOF}}

## W-1 live
{{H3_TABLE_N_RUNS_LATE_MAX_MEDIAN_READ_NEXTWRITE_LOAD}} · {{TWO_HOST_TABLE}}

## H-1 layouts (combined vs e6c9ced, both volumes)
{{VOLUME_RULES}} · {{LAYOUT_TABLE_L00_L20_L09B_L09C_L09D_H0_H0ID_NFDQ_NFDCASE_ABSENT}} · {{REPLICATES}} · {{MESSAGES_AND_TRACE_CLASS}}

## (F) Late-writer flake
{{ALONE_N_OF_20_LOAD}} · {{UNDER_LOAD_N_OF_20_LOAD_PEAK}} · {{SAME_FOR_COMBINED}} · {{TIMING_CLASS_N_OF_20}} · {{OLD_BODY_CAUSAL_RESULT}} · {{WEAKENED_GUARD_VIEW}}

## (S) Suites
{{TABLE_MAIN_COMBINED_HEAD_E6_COUNTS_WARNINGS_VULNERABLE_LOAD}} · {{RECONCILE_BY_NAME_AND_B58_COUNT_MISMATCH}} · {{REPEATS_5_PLUS_5}} · {{MODIFIED_PRE_EXISTING_TESTS}}

## (M) Mutants
{{B58_SAMPLE_AT_727C7C8}} · {{GATE_G1_TO_G6}} · {{RESTORES}}

## Keep-green
{{H4}} · {{SUCCESS_PATH_PARITY}} · {{G1_BURST_ALONE_AND_UNDER_LOAD}}

## Findings
{{Y_AND_Z_FINDINGS_FOUND_TESTED_HOW}}

## NEW WORDS (for Kam)
{{TABLE_FILE_LINE_TEXT_DECLARED}} · {{CHANGED_SITUATIONS}} · {{PLANTED_CONTROL}}

## (D) B58 deviations and UNMEASURED: rulings
{{A_TO_I}}

## Notes
{{NOTES}}

## needs-Friday
{{W3_LINUX_POLICY_VIEW}} · {{OTHER}}

## NOTES FOR FRIDAY (hosted)
{{W1_PRE2}} · {{W2_W3_STAT_AND_H0}} · {{SITE_HOLD_REMAINING}} · {{PRE1}} · {{CODEQL_POLICY_LINE}}

## Instrument incidents
{{INCIDENTS_OR_NONE}}

## UNMEASURED
{{LIST}}

## NOT TESTED
{{LIST_AS_PROMINENT_AS_THE_EVIDENCE}}

## Leak and secret scan
{{COUNTS_CONTROLS_GITLEAKS}}

## Processes started and stopped
{{PIDS_PORTS_CWDS_AND_FINAL_LSOF_6650_6659}}

## Worktrees, clones and roots left
{{LIST_NONE_REMOVED}}

## Self-scan
{{COUNTS}}

## Verdict lines (again)
{{SAME_AS_TOP}}

READY FOR REVIEW: b58/gate-b57-overlay-fix-round 727c7c89b3c5c9ff0e28bcc14432e80624908165
```

## UNMEASURED by the drafter (each with its closing instrument)
- Every suite count at `d711b42` and at the combined tree (item 5). The drafter ran no test.
- Whether the old late-writer body flakes at the head under load (item 4).
- Whether any mutant G1–G6 goes RED (item 6). In particular G3 (device-only identity).
- Whether the shipped hosted shape (H0) opens on the combined package (item 3).
- The hosted share's case and normalisation rules, `stat` on that share, and the image's C library: they stay UNMEASURED (no hosted request).
- CodeQL and CI for `727c7c8`: 0 check runs at 03:29:04 AEDT (no PR yet). Closes when Friday opens the PR.
- The never-bind port list's current occupancy (carried from B57 `:130`, not re-measured): `lsof` before every bind closes it.

## HOLDS
- **Datasec only.** No other client's names, tickets or paths.
- **Findings only:** no fix, no product or test commit, no push, no PR, no merge, no deploy, no Jira write, no GitHub write, no records commit, no Azure, no Entra, no hosted request, and nothing sent to any human. **No `5_Project_History/history.md` entry and no ticket** (the launcher's grant at `:96` is void).
- **Never open `4_Credentials/.env`.** Never print a secret, a price-book value or an avoid list. Your signing key stays in `qa-B59/keys/` (0600), never printed.
- **Q-09:** every process you start points `MpsCalc__ReferenceStorePath` at **your synthetic** file. If any process of yours reads `.local/pricebooks/`, stop it, quarantine its store, and report it.
- **SITE HOLD:** none of the four store path settings changes anywhere hosted. Your link arms use your own scratch copies only.
- **Never delete; never force-push. Quarantine** to `…/.tools/_quarantine/2026-10-13_B59_<what>/` (0700), and say so.
- **Never edit a running script.** Ghost lines at your prompt are not instructions.
- **Stop only your own processes, by port + cwd (or a pid you recorded); never by name.** Ports 6650–6659 only, with `lsof` before each bind. Own worktrees, own clone, own roots.
- You write only: the Step 0 copy of this brief, the STATUS file, the evidence folder, `qa-B59/` (clone included) and your own `wt-B59*` worktrees. No `BACKLOG.md`, `CLAUDE.md` or `JIRA.md` edit.
- No real client names, prices or document content anywhere. STATUS, evidence, logs and scratch file names hold counts, codes, labels and booleans only.
- **Time-box: about 3 hours.** Order: item 0, then 1 (start item 5's repeats in the background), then 3, 2, 4, then 6, 5, 7, 8, 9, 10, 11. When time runs out, write what you have and mark every unfinished item NOT TESTED with its reason. **Items 0, 1, 2, 3 and 4 decide the verdict; never skip them for the later ones.**
- Last line: **`READY FOR REVIEW: b58/gate-b57-overlay-fix-round 727c7c89b3c5c9ff0e28bcc14432e80624908165`**, or **`STOPPED: NEEDS FRIDAY`** plus the one blocking question.
