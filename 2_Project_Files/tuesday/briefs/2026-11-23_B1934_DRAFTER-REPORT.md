STARTABLE: YES

# B1934 DRAFTER REPORT | lane A2 (WP1.4, C7 first slice: the card store against a fake Graph) | seat Datasec/OXPd2-X36

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B1934_SEAT-X36_oxpd2-a2.md` (269 lines, 88499 bytes, sha256 `1792d370c1df0ac62f7be36e942cf591fecb92e1a49346af9e4b70b1b10877da`), sidecar `....md.measured` (132 claim lines; `stamp_check.py <kit>` exits 0, MEASURED 01:00). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s312/d1934/` (below `<d>`). Drafted 00:31 to 01:01 AEDT 2026-11-23 by the second drafter of this lane (Opus), read-only toward the project, Jira and GitHub.

## BLUF
- The kit hands the seat the prototype as TWO FROZEN PATCHES (`<d>/gate/1-red.diff` red state with a throwing `CsaStore`, `<d>/gate/2-fix.diff` the library), so the seat applies, proves and lands; it writes no code (Q13, the alternative is the B1914 form). Expected seat time well inside the commission's 3 hours: the drafter's whole chain on the fresh clone `<d>/clone3` ran from about 00:46 to 00:51 (restore to the last check), lock waits included.
- The slice: the CSA card store only (find by card blob, read and count a user's values, enrol under 15 cards and 50 values with one PATCH, schema CHECK cached). OUT and owed: schema creation, the store's second slice (other values, removal, refresh-token chunks), the blob maker with the card key, the adapter to lane A1's `ICardIdentityService`, the Entra flows, the QR gateway, a tenant run. Why: the flows and the gateway each need a package (C-61 STOP); creation would invent a definition body the reports do not give.
- Two STOP-class questions for S4: **Q4** (the search departs from the Workpath app on purpose: a failed search is a typed failure, not "no user"; a next page is `Ambiguous`) and **Q8** (the schema is checked, never created).
- MEASURED on a fresh clone `<d>/clone3` at BASE `c480a0c8`: red `total: 1750, failed: 87` (L02 green against the stubs by design), green `total: 1750, failed: 0, succeeded: 1746, skipped: 4`; 39 mutants `MUTANTS: 39 of 39 MATCH, 39 of 39 undone equal`; loop 50 of 50; chain, guard (10 and 11 files), unittest 111, `RULES: clean (551 files)`, staged/boundary/lock/words/gitleaks checks each with its control FIRED.

## WHAT I REUSED FROM THE FIRST DRAFTER, AND WHAT I RE-DERIVED
- **Reused after review (every file re-hashed and rebuilt, nothing taken as measured):** the product code (`src/Datasec.Suite.Identity/*`, 11 files; README edited, see below), the fakes and five cell files, the stub `CsaStore` (`<d>/scratch/stub-CsaStore.cs`), `place.py` (diffed against kit B1914's: 2 hunks, the two project lines and the first docstring line only), its 37-mutant list (each old text re-checked by my `mutants_a2.py`, which refuses one that does not occur once), the tool copies `clone.py`, `heavy.py`, `hosted2.py`, `words.py`, `run_step.py` (sha256 equal to kit B1914's THE TOOLS, 5 of 5).
- **Found in its scratch and corrected:** (1) its last whole-solution run `test-final.log` was RED (`failed: 1`, L02, `CsaLimits.Probe`): its mutant undo used `shutil.copy2`, which restores the file's OLD time, so the incremental build after the last undo did not recompile and ran the `mWritableStatic` mutant. My `mutants_a2.py` undoes with `shutil.copyfile` (new time); MEASURED: after 39 mutants the build compiled the restored source and the whole solution read `failed: 0` (twice, on clone2 and clone3). (2) A literal e-acute in `FindTests.cs` (F09 row) is now the C# escape (the B1914 rule). (3) Its mutant runner's red-cell regex matched nothing (`mutants.out` read `red NONE` on every row); mine matches the `[FAIL]` lines (every row names its cells).
- **Added by me:** cells E10 (a collection holding one entry twice: both count toward the 15), F11 (a holder with no mail), L04 (a cancelled call: its cancellation, nothing written); mutants `mMailForced` (F11) and `mDistinctCards` (E10); README sentences for those and the named limit "Graph's per-value length UNMEASURED"; the seat's programs `mutants_a2.py`, `lockrule.py`, `boundary.py`, `staged.py`; the two patches (`<d>/tools/make_patches.py`); the commit message (the first drafter's moved to `<d>/_quarantine/commit-message-first-drafter.txt`).
- **Re-derived (not reused):** every measurement in the kit, from two fresh clones made by `clone.py ... draft` (`<d>/clone2`, then `<d>/clone3` after L04 was added); the first drafter's logs are kept in `<d>/_quarantine/logs-first-drafter/`, unused.

## FACTS RE-MEASURED (instrument, then result)
- `gh api -X GET .../git/ref/heads/main` -> `c480a0c81466f88102cb9d15a506b738615ebcbb` (00:31 and 01:00); `pulls?state=all` newest 25, all closed; `matching-refs/heads/b1934` -> 0.
- `hosted2.py c480a0c8 ... --total 1662 --rules 530 --skipped-linux 4 --skipped-windows 21 --unit 111 --floor 111 --hardened-scan` -> `HOSTED c480a0c81466f88102cb9d15a506b738615ebcbb: PASS` (`<d>/logs/hosted-main.txt`).
- `clar_grep.py` over CLARIFICATIONS (now C-1 to C-69; C-69 is the 20:03 grant, written since the commission): subject words of this lane 0 lines each; control `tolerant` 5. No ruled or open item of the product owner's inside this cut.
- `pointers.py`: 20 of 20 design and report fragments on their lines; control FIRED.
- Toolchain: dotnet `10.0.404`, gitleaks `8.30.1`; `.private` true, `.permissions.push` true; 980 GiB free.
- Panes at 00:52: `Datasec/OXPd2-X37`, `Datasec/OXPd2-X38`, `Datasec/NexusAI-N163` (no X36).
- Where I ran tests and at what load: only in my own clones `<d>/clone2` and `<d>/clone3`, every job through `heavy.py` and the shared wave lock (load1 3.71 to 6.68, lock waits up to 13; the F1/F2 drafters and seats held it at times). No project path was written.

## STOP-SEVERITY CHECKS RUN ON MY OWN PROTOTYPE OUTPUT (each PASS with its control FIRED)
`lockrule.py` PASS / CONTROL FIRED 2 of 2; `staged.py` PASS (22 rows) / 3 of 3; `boundary.py` clean (9 files) / 33 of 33; `words.py` clean (2 files) / 13 of 13; gitleaks rc 0 on clone and 23 neutral files / control rc 1; `diff --cached --quiet` over the shared paths rc 0 / control over slnx rc 1; `mutants_a2.py run` 39 of 39 MATCH; red-first 87 of 88 by `NotImplementedException`; `run_step.py` neutral scan at BASE with the lane's blobs staged: `25 of 25`, `not among them 0`, `no leaks found`. **NEVER RUN (kit says so):** the commit identity check, the neutral scan on a COMMIT of this lane, the push, `hosted2.py` on a head of this lane, the Step 7 (d) compare.

## CHAIN INPUTS (DRAFTER_RULES measured-literals rule 4)
| Step | Inputs | Produced by or present at |
|---|---|---|
| 0 | the kit, the Stamp slots | Tuesday's stamp |
| 1 | `<src>` 13 files; `<repo>` local values; origin; BASE's push run | `<d>/gate/` (exists); `<repo>`; GitHub |
| 2 | `place.py`, `1-red.diff`; BASE's slnx | Step 1 copy; the clone of Step 1 |
| 3 | the red tree; `lockrule.py`; Graph's two lock files at BASE | Step 2; Step 1; BASE |
| 4 | `2-fix.diff`, `mutants_a2.py`; the red tree built | Step 1; Step 3 |
| 5 | the green tree, mutants undone; owned paths staged | Step 4 |
| 6 | staged tree; `staged.py`, `boundary.py`, `words.py`, message | Step 5; Step 1 |
| 7 | the commit; `origin/main`; `run_step.py`, `hosted2.py` | 7 (a); the fetch of 7 (b); Step 1 |

## D-DECISIONS (the coordinator's defaults in the kit)
D1 Graph only, no SignIn reference; D2 Workpath names and limits fixed; D3 the blob maker handed in, forms checked; D4 the search (Q4); D5 four outcomes; D6 count rule, strict reader; D7 one PATCH, entries counted as held, prefix held by another user refuses; D8 check never create, cached 1 h (Q8); D9 card rule and lower-case id; D10 to D12 typed results, masks, no logging, cancellation untyped; D13 patches handed over; D14 names.

## Q-QUESTIONS FOR TUESDAY (each with its default; Q4 and Q8 STOP-class)
- **Q4** default: Workpath search except failed-search typed and next page `Ambiguous`. Alternatives: copy the app's two rules; or page through.
- **Q8** default: check, never create; creation owed. Alternative: create on demand (needs a definition body from a source and a broader app permission).
- **Q13** default: patches handed over (fits 3 hours). Alternative: B1914 form, the seat writes its own (two implementations for the gate; about 240 minutes).
- Q1 to Q3, Q5 to Q7, Q9 to Q12, Q14 as in the kit, each with a default.
- For the gate (not the seat): whether one malformed user in a search answer should fail the whole search (it does); whether the enrol-time other-user check on the PREFIX alone (E06 row 2) is the rule wanted for a mixed fleet.

## UNMEASURED
Everything about real Graph: the filter, the eventual-consistency delay, the PATCH semantics on a collection, annotation counting against the 50, attribute-name case, a value's length limit, the definition address form `<set>_<name>`, the app permission needed. Windows and Linux legs (PREDICTED windows `succeeded: 1729` with skipped 21). How long the seat's lock waits will be tonight.

## OUTSIDE THE FENCES (disclosure)
- I wrote only: the kit, its sidecar, this report, and files under `<d>/` (scratch: `clone2/`, `clone3/`, `tools/`, `gate/` additions, `logs/`, `scratch/`, `out/`, `out3/`, `_quarantine/`). I edited the first drafter's working tree `<d>/clone/` (three test files and the README) — it is this lane's scratch.
- Network: `git clone` from the origin twice (by `clone.py draft`, fetch only, push URL `invalid://no-push`); `gh api -X GET` only, under the project `GH_CONFIG_DIR`. No Jira call, no az, no HTTP to any other host.
- Temp folders under `/var/folders/.../T/` from the `--control` runs of `lockrule.py` and `boundary.py` (copies of my scratch files only; left in place, not deleted).
- Moves (no deletes): the first drafter's `logs/` to `<d>/_quarantine/logs-first-drafter/`; its commit message to `<d>/_quarantine/`; my clone2 mutant logs to `<d>/logs/clone2-mutants/`; gitleaks control folders to `<d>/_quarantine/glc-*`.
- No card id or person's name in the kit (MEASURED: 0 hits for `datasec-oxpd-` and for each ban-list name, underscore-aware, control `_by_Kam_` fired).
