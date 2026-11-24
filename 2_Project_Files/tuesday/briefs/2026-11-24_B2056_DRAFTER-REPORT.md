STARTABLE: YES

# B2056 DRAFTER REPORT: OXPd L3, WP1.8 OneDrive module, first slice (browse My Drive), kit for seat X66

Read-only drafter (Opus) for Tuesday s324. Window 2026-11-24 20:01:11 to 20:47 AEDT (by `date`). Scratch:
`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s324/d2056/` (below `<d>`). Kit:
`tuesday/briefs/2026-11-24_B2056_SEAT-X66_oxpd2-l3-onedrive-browse.md` (255 lines, ASCII only, 8 Stamp slots left as
four underscores) and its sidecar `.measured` (148 claims, 148 measured: 140 by `measure.py` over the evidence files, 8 by
hand; `stamp_check.py` rc 0 at 20:46).

## BLUF
1. The kit is startable after the stamp: frozen `1-red.diff` and `2-fix.diff`, tools copied and hashed, red first, green,
   15 mutants, the chain and the checks all MEASURED by the drafter in a fresh clone at BASE `89a10a1b`.
2. The slice: new `src/Datasec.Suite.OneDrive/` (`MyDriveBrowser`: `ListRootAsync`, `ListFolderAsync(itemId)`), new
   `tests/Datasec.Suite.OneDrive.Tests/` (11 cells, 49 cases), two lines in `Datasec.Suite.slnx`, the two new lock files.
   No package (both lock files' ids are a subset of the landed Graph pair's), no existing file but the slnx.
3. **One Graph call, list children (v1.0), not deprecated:** `GET me/drive/root/children` and
   `GET me/drive/items/{id}/children`, each with `$select`, plus next links only of four children forms. Microsoft's source
   file for that page (read by `gh api -X GET` of `microsoftgraph/microsoft-graph-docs-contrib`, commit `8207700c`, the one
   the rendered page names) has 0 lines holding `deprecat`; controls: drive-recent 3, drive-sharedWithMe 3. No Recent, no
   Shared with me, no search (C-82, C-83, C-84), enforced by cells O08/O11 and `checks_l3.py` check 9.
4. Design choice worth Tuesday's eye (Q2): the module walks pages itself over `GraphClient.SendAsync` instead of
   `GetPagesAsync`, because the landed walk follows any on-origin next link before the caller sees it, so a server could
   lead it to a deprecated call. Each link is checked before it is requested.
5. Gate: G2 recommended (Q3). The slice hands an `IGraphTokenSource` to the layer per call and cannot read a token
   (`GraphToken.Value` is internal to the Graph assembly).

## FACTS RE-MEASURED (instrument; control)
| Fact | Value | Instrument | Control |
|---|---|---|---|
| origin `main` | `89a10a1ba26a16aae7996e059d548bf53531fd44` | `gh api -X GET .../commits/main` at 20:01:21 and 20:38 | the two clones' `origin/main` the same |
| open PRs | 0 | `pulls?state=open` | 5 newest of `state=all` read (47 to 43, closed) |
| branch `b2056*` on origin | 0 rows | `matching-refs/heads/b2056` | `heads/b2048` 1 row |
| seat id X66 free | 0 kit names, 0 content hits in 77 non-`.pre-` SEAT kits of 2026-11-17 to 11-24; no pane | word scan of names and contents; `tmux list-panes` | X65: 1 name, 3 files, pane `%425 Datasec/OXPd2-X65` |
| `.tools/b2056` | absent | `ls .tools` | `b2053` present |
| BASE hosted run | `HOSTED 89a10a1b...: PASS` at `--total 2153 --rules 659 --unit 111` | `hosted3.py` (B2053's, unchanged) | its own `NOT-A-LINE-OF-ANY-LOG count 0` |
| red | OneDrive exe `Total: 49, Errors: 0, Failed: 41`, 41 of 41 `[FAIL]` followed by `Assert.*() Failure` | `heavy.py`, `<d>/logs/r-exe.log` | O03 empty row, O06, O10, O11 green on the first shape |
| green | `total: 2202`, `failed: 0`, `succeeded: 2198`, `skipped: 4` (2153 + 49) | `f-test`, `f-test-after-mutants`, `c-test` | the red total 41 |
| mutants | `MUTANTS: 15 of 15 MATCH, 15 of 15 undone equal` | `mutants_l3.py run` (frozen) in clone2 | a TBD run first in clone (0 of 15 MATCH: every row DIFFER against `TBD`, as it must) |
| chain | locks equal 36 of 36; `GUARD: clean (14 files)`/`(15 files)`; `Ran 111 tests`, `OK`; `RULES: clean (671 files)` | `frozen_run.py chain` | guard folders hold 0 files naming Lab, Tests or OneDrive |
| checks | `CHECKS: 10 of 10 PASS` | `checks_l3.py` | each check's planted control fired |
| words | `WORDS: clean (2 files)`; lock files 2 + 2 hits, all class `seat ids`, = `x64` count 2 + 2 | `words.py` | `--control` `CONTROL FIRED: 13 of 13`; landed Graph.Tests lock file also 2 hits |
| gitleaks 8.30.1 | clone2 and 18 neutral files `no leaks found` rc 0 | `gitleaks dir` | planted two-half random token rc 1, moved to `<d>/_quarantine/gl-control` |
| toolchain | `10.0.404`, `8.30.1` | `--version` / `version` | n/a |
| model | `claude-opus-5-5` (models_latest.json line 17); OXPd CLAUDE.md:7 "newest Opus" | `awk NR==` | `fleet/specs/model-routing.md` has 0 OXPd lines (grep), so the project rule governs |

## CHAIN INPUTS (each input exists at BASE or is made by an earlier step)
| Step | Inputs | From |
|---|---|---|
| 0 | kit, Stamp S4 | Tuesday |
| 1 | `<src>` ten files; `<repo>` local config; origin | `<d>/seat-tools` (exists); `<repo>`; GitHub |
| 2 | Graph layer at BASE | Step 1 clone |
| 3 | `1-red.diff` (holds both lock files); package cache `.tools/nuget-packages` | Step 1; exists (heavy.py names it; restore offline rc 0 MEASURED) |
| 4 | `2-fix.diff`, `mutants_l3.py`; red tree built | Step 1; Step 3 |
| 5 | green tree, mutants undone | Step 4 |
| 6 | staged tree; `checks_l3.py`, `words.py`, message | Step 5; Step 1 |
| 7 | commit; `origin/main`; `run_step.py`, `hosted3.py` | 7(a); fetch; Step 1 |

## D-DECISIONS (Tuesday's defaults as coordinator; the kit says none is the product owner's)
D1 browse only, My Drive only. D2 own page walk over `SendAsync`. D3 next links only of four children forms. D4 an item
outside the rules ends the listing (no silent skip). D5 a `remoteItem` item is listed, never followed (owed 115 untouched).
D6 one class `BrowseTests`, own fakes, the real `GraphClient`. D7 one commit, push by sha, rebase before first push only.

## Q-QUESTIONS FOR TUESDAY (each with its default; Q1 and Q2 STOP-CLASS, answered in words at S4)
- **Q1** list-children is the only call and is not deprecated. Default a: yes (source file 0 `deprecat` lines; controls 3, 3);
  re-count at the stamp. Alt b: also read a Microsoft deprecation list beyond the per-call page (UNMEASURED).
- **Q2** next-link rule. Default a: the four children forms. Alt b: the first request's path only. Alt c: the layer's
  `GetPagesAsync` (cannot promise no other call). Graph's real next-link form is UNMEASURED (tenant test).
- **Q3** gate tier. Default G2; alt G1.
- **Q4** `remoteItem` items. Default: listed, not followed; alt: left out (a silent drop).
- **Q5** Select and thumbnails. Default: narrow Select, no thumbnails; alt: the app's Select with `$expand=thumbnails`.
- **Q6** page bound. Default 100 (`GraphOptions.DefaultMaxPages`); alt: none or caller-only.
- **Q7** commit subject (285 chars, words clean). **Q8** no local CodeQL (no Rosetta). **Q9** Opus, READY Step 0 + 150 min,
  push by + 110, pane `Datasec/OXPd2-X66`, landing order with B2053 and B2057 free (disjoint paths).
- Also for Tuesday (not in the kit's Q list): tonight's kick-off may change WP1.8's scope; the commission already holds
  stamp and launch on that answer or its default.

## UNMEASURED
- Every hosted leg on this lane's head (PREDICTED `--total 2202 --rules 671`, linux succeeded 2198, windows 2181).
- How a real tenant answers: next-link form, item shapes, ids (the module's rules are its own).
- Whether lane L4 (B2057) moves `Ran 111` or the guard lines before this lane lands (the kit's rebase rule takes the new
  main's numbers).
- CodeQL on this code (the PR's own run).
- `clone.py seat`, the commit, `run_step.py`'s neutral scan on a commit, the push, the read-back, the rebase: NEVER RUN
  by the drafter (named in the kit's FACTS 7).

## OUTSIDE-THE-FENCES DISCLOSURE
1. **Web reads of Microsoft's public documentation** (the commission asked for "Microsoft's page read in this drafting"):
   WebFetch of `learn.microsoft.com` for driveitem-list-children and drive-recent; and `gh api -X GET` (under the OXPd
   project `GH_CONFIG_DIR`, the Datasec login) of three raw files of the public repository
   `microsoftgraph/microsoft-graph-docs-contrib` plus one `commits?path=` read. GET only; no Datasec data sent; saved under
   `<d>/evidence/ms-*.md`. A read of a non-Datasec GitHub repository through the Datasec login is beyond the rules' usual
   `gh` use (which names the project's own repository); Tuesday may prefer a different route next time.
2. Builds and tests ran only in my scratch clones under `<d>`, every heavy job through the project's `heavy.py` and the
   shared lock (waits 0 to 5 per job, load waits up to load1 13.5); seat X65's lock was never touched. My scratch writes
   (my own clones' index and worktree, a temporary index file) are inside `<d>`; nothing in any project folder, Jira, GitHub
   or card store was written.
3. One command in my scratch sent stderr to `/dev/null` (an accidental re-run of my own `scans.py`, which stopped at an
   existing-folder check; its results had already been printed and are reproduced by `evidence/checks.out`). Nothing was
   lost or hidden by it, but it breaks the stated shell form.
4. One `rm -f` of a non-existent scratch file was refused by the no-rm hook before running; nothing was deleted. Two
   `README.md` copies of the red-shape step went to `<d>/_quarantine/` (moved, not deleted).
5. No person, nothing of another client, no Fable, no Azure, no tenant, no printer.
