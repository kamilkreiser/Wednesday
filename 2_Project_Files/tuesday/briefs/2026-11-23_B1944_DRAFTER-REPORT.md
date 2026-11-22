STARTABLE: YES

# B1944 DRAFTER REPORT: lane A2-F (the card store's two owed Minors after gate B1941), seat Datasec/OXPd2-X40

Drafter: Opus, read-only toward OXPd, Jira and GitHub, 2026-11-23 02:58 to 03:27 AEDT (clock reads by `date`: 02:58:30,
03:15:04, 03:17:03, 03:26:51). Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B1944_SEAT-X40_oxpd2-a2-f.md`
(76697 bytes at the sidecar's write clock, 0 non-ASCII bytes, 8 unfilled slot lines S1 to S7 + READ-WHOLE). Sidecar
`... .md.measured`: `stamp_check.py <kit>` rc 0, `150 claims, 150 measured, 0 not measured`. Scratch:
`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s313/d1944/` (below `<d>`); the seat's tools: `<d>/seat-tools/`
(10 files, sha256 in the kit's THE TOOLS).

## BLUF
- FOUND 1 (a blob maker's own cancellation escaped untyped): both `catch (Exception failure) when (failure is not
  OperationCanceledException)` around the maker become `catch (Exception)`: `ICardBlobCodec` has no token parameter
  (read: `string SearchPrefix(string cardId)`, `string Blob(string cardId, string? mail)`), so nothing it throws can
  be the caller's cancellation. Cell F12, 6 rows (prefix/blob maker, OperationCanceledException/TaskCanceledException,
  find/enrol). I did NOT build the gate's sketch (token + `IsCancellationRequested` filter): Q1 alternative b.
- FOUND 2 (a name twice outside the set read last-wins): Tuesday's default REFUSE, built as ONE whole-answer check
  right after the store's only JSON parse (`CsaStore.cs:242`-`:243`, every answer the store reads passes there: 4
  callers of `GetJsonAsync`), walking every object and array, names ordinal after unescape. The set's own duplicate
  check is folded in and removed (D3). Cells F13 (9), R07 (4), K06 (3), E11 (2).
- README: two sentences rewritten from the code with `file:line` (`README.md:34-37`, `:41-46`).
- Red first at main `394fa997` MEASURED: whole solution `total: 1783`, `failed: 24`, all Identity, every message
  `Assert.IsType() Failure` (6 escaped cancellation types, 18 null). Green `1783 / 0 / 1779 / 4`. 44 mutants 44 MATCH,
  44 undone. Loop 50/50. Chain, guard, unittest, RULES 551, boundary, words, gitleaks, neutral scan: all clean with
  controls. Sized for one seat in well under 2 hours (READY at Step 0 + 110, push at + 80).

## FACTS RE-MEASURED (instrument, control)
- Origin (gh api -X GET under the project GH_CONFIG_DIR, 03:14): main `394fa997826e3d102fafa6a0c05a4847132cb01a`;
  private true, push true; matching-refs heads/b1944 0 (control heads/b1934 1 row at `75fb5fdf`); PRs 28..24 closed
  and merged, 0 open.
- Main's push run: `hosted2.py 394fa997... --total 1759 --rules 551 --skipped-linux 4 --skipped-windows 21 --unit 111
  --floor 111 --hardened-scan` -> `HOSTED 394fa997826e3d102fafa6a0c05a4847132cb01a: PASS` (03:10; linux 1755, windows
  1738 succeeded; CodeQL Analyze x3 success).
- The three Identity source files at main are byte-equal to kit B1934's THE CODE (sha256 3137741c..., 975b937a...,
  03d6b38c...): the lane landed as gated.
- CLARIFICATIONS.md (696 lines, sha256 3b0c0e8e...): `duplicate`, `last-wins`, `repeated`, `cancel`, `CodecFailed`,
  `MalformedAnswer`, `card store`, `blob maker`, `custom security`, `HPAuthenticationSuite`, `cardId`, `deviation` 0
  each; `strict` 6 and `twice` 1 read at source (C-61/C-63 are the PRINTER's answers, "Keep both strict for now";
  line 200 an attachment list); control `tolerant` 5. The wave-3 commission line 9 rulings: no card-store subject.
  So nothing in this lane is the product owner's; C-63 is NOT cited as covering it.
- BACKLOG.md: neither Minor filed yet (`last-wins` 0, `name twice` 0, `CsaStore` 0; control `tolerant` 8).
- No `B1944` file in `<project>/1_Project_Definition/Briefs/` (control B1934 2); `<project>/.tools/b1944` absent.
- Toolchain: `.tools/dotnet/dotnet --version` 10.0.404; gitleaks 8.30.1. df 975 GiB free; load1 6.66 at 03:15.
- Every heavy job via `heavy.py` and `.tools/wave1-heavy.lock.d`: lock waits 0 to 2, load1 1.68 to 6.83; I never
  touched another holder's lock.

## D-DECISIONS (all Tuesday's as coordinator; none the product owner's)
D1 catch-all for the maker; D2 one whole-answer repeated-name check (fail closed); D3 the set's own check removed;
D4 the named cost (a repeated name anywhere, also in parts never read, fails the call); D5 five new Theories, 24
rows, no existing cell/helper touched (+153 -0 in tests); D6 one commit on a NEW branch
`b1944/a2-f-card-store-follow-ups` from main, lane A2's rebase-before-first-push rule kept.

## Q-QUESTIONS FOR TUESDAY (each with its default; Q1, Q2 STOP-CLASS, answer in words at S4)
- Q1 default a: every maker exception, cancellation included, is CodecFailed. Alt b the gate's sketch (pass a
  cancellation when the caller's token is cancelled; mirrors `GraphClient.cs:518`); alt c token into the maker
  (public interface change: refused). Cost of a: caller cancelled + maker throws -> CodecFailed, not its cancellation.
- Q2 default a: refuse everywhere by one whole-answer check (MEASURED red 18 rows at main). Alt b per-object checks
  only at objects read; alt c a Limits line naming last-wins (fails open). Cost: D4.
- Q3 default: remove the set's own check (its old mutant `mDuplicateNameTaken` would otherwise survive).
- Q4 default: neither change is a deviation-register row (Workpath's behaviour on both shapes UNMEASURED; nothing
  stored changes); named in FOR RECORDS for the records seat R300.
- Q5 Opus (`<project>/CLAUDE.md:7`); Q6 READY Step 0 + 110, push + 80, pane Datasec/OXPd2-X40, G1 round 2 of 2.
- For your stamp S7: the grant ends 09:00 AEDT; the kit leaves the absolute hard stop to you.

## CHAIN INPUTS (each input produced by an earlier step or present at BASE)
| Step | Inputs | From |
|---|---|---|
| 0 | kit, stamp slots | Tuesday's stamp |
| 1 | `<d>/seat-tools` (10 files), `<repo>` local values, origin, BASE's push run | exists; exists; GitHub |
| 2 | three source files at BASE | Step 1 clone |
| 3 | `1-red.diff`, the clone at BASE | Step 1 |
| 4 | `2-fix.diff`, `mutants_a2f.py`, the red tree built, the seat's loop script | Step 1; Step 3; written in Step 4 |
| 5 | green tree, mutants undone and rebuilt | Step 4 |
| 6 | staged tree, `boundary.py`, `words.py`, `commit-message.txt` | Step 5; Step 1 |
| 7 | the commit, `origin/main`, `run_step.py`, `hosted2.py` | Step 7a; fetch in 7b; Step 1 |

## WHAT I RAN, WHERE, AT WHAT LOAD
In my own scratch clones only (`clone.py ... draft`: push URL `invalid://no-push`, no identity):
- `<d>/clone`: the prototype (edits, the two diffs taken from it), first red run of the Identity executable.
- `<d>/clone2`: the seat's chain: apply red, locked restore, build, whole-solution RED; apply fix, build, GREEN;
  `mutants_a2f.py run` twice (see DISCLOSURES); build after last undo (dll 03:11:16 > newest source 03:10:46); loop 50;
  restore --force (28 of 28 lock files equal); build; test; two publishes; release guard 10/11 files; unittest 111;
  repo_rules 551 (never --source-documents); boundary + control; words + control; gitleaks + control; neutral scan with
  the 7 blobs staged (25 of 25, 1350 objects, 0 not among them, no leaks found). Its index holds the 7 staged files.
- `<d>/clone3`: both patches applied fresh (7 of 7 cmp-equal to `<d>/clone`), `apply --check` of 2-fix refused, then
  `git apply -R 2-fix.diff` to get the red state for the Identity executable alone (`Total: 112, Errors: 0, Failed:
  24`, red cells E11 F12 F13 K06 R07). Left in the red state.
- Load 1.68 to 6.83 at the jobs; the lock held by others at times (waits up to 2).

## UNMEASURED
Whether Graph ever answers a repeated name; any hosted leg on this lane's head (PREDICTED linux 1779 / windows 1762
succeeded at total 1783); the parser's depth limit as such (DERIVED from the API, the walk is bounded by it); the
seat-mode clone, the commit, its identity read, the neutral scan on a commit, the push, the rebase (each NEVER RUN,
said in the kit).

## DISCLOSURES (outside the fences, and corrections made while drafting)
- Inside the fences: I wrote only the kit, its sidecar, this report and `<d>/**`. No write to OXPd (`<repo>`,
  `<project>/.tools/**` except taking/releasing the shared lock through `heavy.py`, which moves each lock folder into
  `<d>/_quarantine/locks/`), no Jira call, GitHub GETs only, no push, no PR, no `cd`, nothing deleted (old diffs and
  sidecar skeletons moved to `<d>/_quarantine/`). Read only: project CLAUDE.md, CLARIFICATIONS.md, BACKLOG.md (counts),
  03 plan lines 108 and 378, the Graph layer's cancellation lines (`GraphClient.cs` grep). Nothing under
  `Source_Documents/`, no key folder, no NAS, no sibling project.
- The first red run had F12's two find/blob rows reading null (no holder in the fake, so the blob maker was never
  called); I gave the fake user the card's blob, re-measured: all 6 F12 rows red on the escaped cancellation type.
- The first `mutants_a2f.py run` (`<d>/logs/mutants1.txt`) printed 39 of 44 MATCH: four new rows had placeholder
  expectations and `mNoSchemaCheck` now also reddens F12 row 6 (its request count includes the two schema reads). I
  set those five expectations to the measured cells and re-ran all 44: `44 of 44 MATCH, 44 of 44 undone equal`
  (`<d>/logs/mutants2.txt`). The kit names the changed expectation.
- The README paragraph was rewrapped after the first mutants run (README only, no compiled file); `2-fix.diff` was
  regenerated (old one in `<d>/_quarantine/2-fix.v1.diff`), copied into `<d>/clone2`, and the build, test, loop,
  chain, words (209 added lines), gitleaks and neutral scan all ran after it.
- The scans are the project's own tools (`words.py`, `boundary.py`, gitleaks, `run_step.py`'s neutral scan, the
  repo's `release_guard.py` and `repo_rules.py`) plus two small programs of mine marked as such in the kit (the public
  line count and the ASCII check).
