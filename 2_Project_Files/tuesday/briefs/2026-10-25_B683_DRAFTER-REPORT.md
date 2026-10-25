STARTABLE: YES

# B683 drafter report (SEAT-H25, lane H-E2E), drafted 2026-10-25 18:56 to 19:10 AEDT

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-25_B683_SEAT-H25_hpsmpoc-352-349-e2e-runner-rows.md` (123 lines, shape of B664; web route from B652).

## BLUF
- The lane is startable: main `4e63fc41` is the base, no open PR, no `b683*` ref, no live branch touches the four paths, ports 9760-9769 are free, pane name H25 is free. Four paths: `web/src/e2e-runner.test.ts`, `web/scripts/e2e.mjs` (ciMatrix only), `Hpsmpoc178CustomerNameTests.cs`, `customer-name.test.ts`.
- **Two things differ from the commission and are in the kit.** (1) The 349 "eight rows" are not eight open rows: the gate's AST census reads 3 slice-then-strip sites (these ARE 352 item 3) plus 5 raw-by-design sites; what 349 really has left open is the reflow-tolerance clause, a candidate decision for the product owner, so the kit records the 5 with a reason line and keeps reflow OUT (D-2). (2) `--check-shards` runs `ciMatrix` in CI's `web-build` job, so item 4 is a CI-judged tooling edit, not only a test edit.
- `4e63fc41` is not in the shared clone yet (seat fetches under the lock). The Api cells run on SQLite locally; SQL Server is CI's only (no docker), stated as NOT TESTED.

## Facts re-measured (instrument, control)
| Fact | Value | Instrument | Control |
|---|---|---|---|
| main | `4e63fc4142e213897a2a025013351ded3a17c826` (06:32:45Z, subject "CI reader polices the SQL Server shard job; two comments lose names (#217)") | `gh api -X GET commits/main`, `ls-remote origin refs/heads/main` | both agree; last 6 commits each 1 parent |
| open PRs | none | `pulls?state=open --jq` printed nothing | no direct control run (an empty list is a suspect zero); indirect: main's last commit subject carries `(#217)`, and `ls-remote 'refs/heads/b6*'` listed 12 refs, so the endpoints answer |
| `b683*` refs | 0 | `ls-remote 'refs/heads/b683*'` | `b652*` prints 1 |
| blobs | e2e-runner.test.ts `830d6cac` (1010 lines), e2e.mjs `68364efb` (557), Cust.cs `c177ed1f` (651), customer-name.test.ts `1746ce06` (368) | `gh api git/blobs` raw saved, `git hash-object` = tree entry for all four | `printf x | git hash-object --stdin` = `c1b0730e` (differs) |
| commit in shared clone | NOT present | `git cat-file -t 4e63fc41` fails | `754bf1e7` prints `commit` |
| raw read sites in e2e-runner.test.ts | `:99` WC, `:103` RAW, `:149` RAW, `:381-386` RAW helper and 3 uses, `:382` WC, `:495` WC, `:543/:911/:933` RAW slice, `:825` WC, `:952` WC | python3 line scan of the saved blob | matches the gate's AST census (B622 STATUS line 56): 32 sites, same raw set |
| ciMatrix | `e2e.mjs:90-93`, regex `/^ +shard: \[.*\]$/`; used by `--check-shards` (`:541`); CI runs it at `ci.yml:426`; real shard line `ci.yml:491` | saved blobs, `grep -n` | `grep -c '^ +shard: \['` on ci.yml = 1; the `ci.yml:173` comment naming `shard: [...]` starts with `#`, no match |
| plain-name rows | send exactly 1 more space (`HeldNameWithAnEdgeSpace` `:364`; `(f)` `:241`); edge-spaced name has 1, 2, 3-5 | read | fact-check counts in the kit all re-run on the saved blobs (3, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1); a nonsense string = 0 |
| CI predicates | web-unit `npm test` = `vitest run` whole suite; web-build lint (`eslint --max-warnings=0`), typecheck, `--check-shards`; SQL shard `api-assessment`: every outcome Passed (skip counts as failure), `floor=100` lower bound | `ci.yml` blob `135260d6` read | line numbers quoted from `grep -n` on the saved file |
| formatter in web/ | none | `grep -c -i -E 'prettier|biome|dprint'` on `web/package.json` = 0 | `vitest` = 2 |
| tools | node `v24.21.0`, dotnet `10.0.402` at `.tools/dotnet/dotnet` (bare PATH: not found) | ran `--version` on the full paths | file exists |
| Jira | 352: Backlog, 0 comments; 349: Backlog, 1 comment (markerStep met; 10 of 12 comment-proof, 2 recorded; reflow open); prior work: `ciMatrix` returns 352 only | `.tools/b649/jira.py` GETs, every JQL `project = HPSMPOC AND ( ... )` | `zzqxnonexistentphrase` 0; `UatOpenTests` 20 |
| panes | `Datasec/HPSM-POC-R43`, `Datasec/Security-Composer-G122`, `fleet-monitor`, `tuesday` | `tmux list-panes -a -F '#{@cockpit_name}'` | no H25; word scan of 131 non-`.pre-` SEAT kits (10-24, 10-25) for `H25` = 0, `HPSM-POC-H24` = 3 |

### Ports (block proposed: 9760-9769, none needed)
- `lsof -nP -iTCP:9760-9769 -sTCP:LISTEN` printed nothing (rc 1); whole listening set at 19:0x was only 5000, 7000, 49152, 49181, 49183, 49185, 59869. `lsof` 8560-8563 also empty (the existing `cli` rows use 8560/8561/8563 as closed ports). Positive control for lsof not re-run by me (the instrument was shown to list in earlier kits); the word-boundary scan positive control: block 960x hits 5 files, as the B664 kit reported.
- Word-boundary scan `(^|[^0-9a-f])976[0-9]([^0-9a-f]|$)` over 131 SEAT kits: **8 hits, all in finished lanes**: B626 (G98's reserved 9760-9769, pane gone), and mentions in B630 and B631 (history of that reservation). No live pane holds it. Hits for neighbours: 977x B627/B631/B633/B640/B641 (J10 block), 978x B628/B629, 979x B629/B592 (9795 is a source line number). **I did not take 9770, 9780 or 9790.** Tuesday should re-run the scan at stamp time, since B684 to B686 kits are being drafted beside this one and none existed on disk at 19:0x (`ls | grep B68[3-9]` printed nothing before my write).

## D-decisions (drafter's, each with the default taken)
- **D-1 (item 1 scope):** property-first: every extra-space count n in 1..5 and each distribution is refused for a plain held name; at least n = 3, 4, 5 (the ticket's shape, 9 cells per side). n = 2 on a plain name is also unpinned (no plain-name two-more row exists) but is NOT assumed: the seat adds it only if its X-plain-2 mutant survives.
- **D-2 (the 349 remainder):** the "eight rows" resolve to 3 + 5 (table above). The 3 close under item 3; the 5 raw-by-design sites get a one-line reason in the test file (no Jira write; the records seat writes the ticket words). Reflow tolerance of the ten comment-proof rows is OUT (the gate called it a candidate decision; no formatter exists in `web/`, count 0). The commission as worded ("each made comment-proof or recorded as needing neither") is already met for 10 of 12 by PR #212 per the ticket's own comment.
- **D-3 (helper shape):** one module-level helper, strip first, used at `:543`, `:911`, `:933`; the already-correct `fn` at `:495` stays byte-equal (smaller blast, one fewer thing to review); the playUnit end pattern is passed as its own argument, not widened. The cut takes text as an argument so the slice-shift row feeds it a fixture instead of reading a mutated file.
- **D-4 (ciMatrix):** loosen to an optional trailing blank-then-`#` comment and trailing blanks; refuse `[a]#x` (not a YAML comment), refuse two lines or none. It is a loosening of tooling CI runs, so `--check-shards` must still print `shard plan OK` on the real `ci.yml` (kit step 5/8).
- **D-5 (mutants):** product mutants (`Requests.cs` allowance, `customer-detail.ts` `nameRefusal`) live only in a third scratch worktree `wt-b683-mut`, never committed; the kit forbids editing product files in `-fix`. Budget one `dotnet build` per Api variant.
- **D-6 (pane, ports, model, gate):** pane `Datasec/HPSM-POC-H25`; ports 9760-9769 reserved; model row C2 (line 92), `claude-sonnet-5-5` from `models_latest.json` line 23; launch line carries `BRIEF_SEAT_LEVEL=sonnet` inside the quotes and `WED_USAGE_STOP=100`; gate tier 2 (G2 line 109), **NO GO 0 of 2 on this class** (B609 and B622 both GO WITH FINDINGS).
- **D-7 (hours):** suggested target READY 3 h, hard stop 5 h after launch (heavier than B664: npm ci, Api build, about 14 mutant builds).
- **D-8 (no worktree for the drafter, no run):** nothing was executed; every mutant count in the kit is the gate's (RELAYED) or marked UNMEASURED.

## Q-questions for Tuesday (each with a default)
- **Q-1:** Item 2 (six or more extra spaces, the mirrored split) stays OUT as commissioned. Default: OUT, left for the product owner.
- **Q-2:** Add a self-reading census row that fails when a new raw read of `scripts/e2e.mjs` appears? Default: NO (the kit counts by program in STATUS instead; a source-text row reading its own file adds a CodeQL file-access surface).
- **Q-3:** Should the seat also fold the `fn` helper at `:495` into the new helper? Default: NO (D-3).
- **Q-4:** Both B683 and B684 build `HpsmPoc.Api.Tests` at the same time; seat-local heavy locks do not coordinate across seats. Default: launch both under the existing launch_when_cool waiter (load1 < 7 twice) and rely on the load rule written in the kit.
- **Q-5:** Reflow tolerance (D-2): record "not wanted, no formatter configured" through the records seat, or open a follow-up? Default: record, because the gate itself offered that option.

## UNMEASURED
Everything that needs a run: base web suite counts at `4e63fc41` (the B652 kit's 195 files, 2937 passed predates #215 and #216), whether `--check-shards` runs here without a build, whether X-plain-2 survives, whether the playUnit cut survives the shared helper, Api build time, whether CodeQL flags the new regex, the SQL Server run of the new cells (CI only). The Positive control for the `lsof` instrument was not re-run in this draft. I did not read the stamp text of any sibling kit beyond B664's.

## Outside-the-fences disclosure
- Wrote only the two output files. No Artifact, Docs, mail, chat, publish tool; no `decision_queue.sh`; no card read. Did not read `fleet/briefs_staged/`, `scoreboard.md`, the main ledger, or any WEDNESDAY/FRIDAY tree.
- Read in the HPSM-POC project (read-only): `.tools/b649/jira.py` and `read.py` (whole headers/helper), B664/B673/B652/B622/B613 STATUS lines, B652 and B664 kits, `SETUP_RUNBOOK.md` and `CLAUDE.md` greps (dotnet), the shared clone via `git cat-file`, `git grep` on `754bf1e7` (read verbs, `--no-optional-locks`). No fetch, no checkout, no worktree.
- `gh api -X GET` only (commits, pulls, trees, blobs, contents of `web/package.json`) under the project's `GH_CONFIG_DIR`. One Jira helper import in a scratch script (`q.py`, in the session scratchpad) running GET searches; the Jira comment on 349 carries an author display name that I did not copy into the kit.
- Scratch files (blobs, tree listing, `q.py`) are in the session scratchpad `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/16269e6c-6a5b-4095-925b-ab14a2b17432/scratchpad/`. One `mkdir -p` of that directory; one `lsof`, `tmux list-panes`, `date`. No HTTP to hosted/demo/production hosts. No `cd`.
- The kit text names no person and no decision-card id (grep for the owner's names = 0); it does carry `B###` build ids and ticket keys (the template does), and forbids them in commits and test text.
- Stamp slots: 8 lines match the four-underscore pattern (7 slot lines at kit lines 113-119 and the last line 123); control: the REFUSE grep splits the pattern so the instruction line itself does not match; the at-sign check prints 0.
