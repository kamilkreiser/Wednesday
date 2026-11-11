STARTABLE: YES

# B1517 drafter report (SEAT-M122, MPS lane L5 fix round 1)
Drafted 19:36-19:43 AEDT 2026-11-11 (`date` printed 19:36:59, 19:39:21, 19:39:34, 19:42:35). Kit: `.../briefs/2026-11-11_B1517_SEAT-M122_mps-l5-fix-round-exit-pass-through.md` (104 lines, 11 four-underscore lines, ASCII, `.pre-stamp` identical by `cmp`).

## BLUF
- Branch head at source is still `2eba09d8efe7e199691eee9706c62e6aa7da35df`; main is `9a0c4ba8...` and its 16 files since base `5cd6002f` touch none of `scripts/`, `infra/`, `tools/demo/`, `.github/`, so no merge is needed.
- BUILD in 3 forward commits: (1) tests only, rows A/B/C in a new class in `test_deploy_pre1.py` (the Major, its rc-0 control, and `-o json`); (2) a `#` comment at `deploy-from-ci.sh:21`; (3) one condition at `seed.py:709` plus 2 rows. Gained exactly 5 test names, expected 241 tests.
- Red-first is by plant in a second clone: the reviewer's exact mutant (`:205` -> `:`), a value mutant (`exit 1`), the `-o json` drop, and the restored early return; the Major row is green at head by design, because the code is right.
- HOLD (never built, text in the kit and below): the `:259` closing line, the `:166`/`:175`/`:163` STOP wording, and the `--out-dir` docstring/help/behaviour choice.
- No-az is structural: a tripwire `az` first on a PATH built from `/usr/bin:/bin:/usr/sbin:/sbin` only, `AZURE_CONFIG_DIR` pointed at an empty folder, one runner script, a per-run `os.path.exists` PATH proof with a control, and a ban on typing any az path even to read it.

## Per-finding table
| Review row | Verdict | Why |
|---|---|---|
| 1 Major 126 pass-through (`:201-205`) | BUILD (test) | rows A (rc 1, 7, 130 end with az's code, no `== deployed`) and B (control, rc 0 deploys); reviewer's probe `gate_probes.py:33` adapted; no fixture edit |
| 2 Minor 126 `-o json` | BUILD (test) | row C: exactly one `-o`, followed by `json` |
| 3a Minor 126 exit-3 header `:21` | BUILD (comment) | `:21` is a `#` line printed by nothing: `usage()` (`:29-32`) echoes a fixed string, no `--help`, no `$0`/`BASH_SOURCE` read (count 0, control 1). Proven by "code-only text identical before/after" with a planted control. |
| 3b Minor 126 line at `:259` | HOLD | new operator-visible sentence |
| 4 Minor 203 `:166`/`:175`/`:163` | HOLD | changed operator-visible words; no existing test pins the current `:175` or `:163` text (grep of the 4 test files for `did not pass`/`differs from`: 0 hits except a comment, control `kept:` 2), so Tuesday's eventual wording is test-safe |
| 5 Minor 173 `--out-dir` not checked | HOLD | Option B changes docstring `:36-38` and `--help` `:661-663`; option A changes a pinned property (no git subprocess in a dry run) and may break dry-run rows that use a non-`.local` out dir |
| 6 Minor 173 no last line when all exist (`seed.py:709`) | BUILD | `if not todo and not args.dry_run:` falls through to the EXISTING line at `:755-757` (todo and purchase_todo empty: nothing else runs); real run unchanged, pinned by row `_173_g`. Q-FIX-1 in Stamp S4 (default YES) lets Tuesday veto this as "an existing sentence on a new path". |
| 7-11 Info | none | recorded only (Info 10, "this test never calls az" in validate.sh, is a wording point Tuesday may take up separately) |

## FOR TUESDAY: held items, exact current text and proposed text
1. `deploy-from-ci.sh:259` current: `if (( ! start_proven )); then exit 3; fi` (no line printed; the NOT PROVEN line is at `:211-212`, then success-shaped lines `:242`, `:255`, `:257`). Proposed: `deploy-from-ci: NOT PROVEN: exit 3 because the deploy call did not report RuntimeSuccessful with at least 1 instance up (see the line above). Do not report this deploy as done.`
2. `:166` current: `deploy-from-ci: the hosted overlay changed after PRE-1 passed, so nothing was deployed; the new overlay copy is kept: $overlay_copy`; `:175` current: `reread_overlay || stop "PRE-1 did not pass (above); nothing was deployed"`; `:163` current: `deploy-from-ci: PRE-1: the hosted overlay read answered HTTP $overlay_code, so the overlay cannot be checked`. Proposed: `:175` `stop "the overlay re-read before the deploy did not pass (above); nothing was deployed"`; `:163` prefix `PRE-1 re-read:`.
3. `seed.py:36` current: `Dry run (MPSCALC-173): --dry-run checks everything a real run checks (flags, origin, token source, scenario shapes, ...` and `:38` `... no directory (--out-dir is not touched).`; `--help` `:661-663`: `read only: check everything a real run checks and say what would be created; GET requests only, nothing is created or written (--out-dir is not touched)`. Proposed (option B, my default): `checks what a real run checks, except --out-dir (not checked, not touched: a real run may still refuse it)` in both places. The commit subject of 2eba09d8 cannot change (no amend); the forward commit message would say so.

## Facts re-measured (instrument)
- Branch head, main, open PRs (`gh api -X GET` under the project `GH_CONFIG_DIR`): `2eba09d8...`, `9a0c4ba8...`, #178 only. compare ahead 2, 16 files, none in lane paths (`--jq .files[].filename`).
- All `file:line` pointers by `awk NR` / `grep -n` over raw files at `2eba09d8` saved in `/private/tmp/b1517-drafter/` (deploy-from-ci.sh 259 lines, test_deploy_pre1.py 623, seed.py 767, test_seed.py 371, fakes/az 167).
- Ports 9670-9679: `lsof` 0 listeners (control: 14 unfiltered). Word-boundary scan of 86 non-pre-stamp kits of 10-11 Nov: hits B1503 (H158, HPSM, declares the block, no pane) and B1391, B1398, B1454, B1460, B1466 (HPSM walkthroughs); control `963[0-9]` hit B1495, B1497, B1502. Live panes: Composer-C97, MPS-M121, M120, M117, NexusAI-N122; no MPS-M122.
- Model: `models_latest.json:23` `claude-sonnet-5-5`; row C2 at `model-routing.md:92`; gate rows G1/G2 at `:108-109`.
- `.tools/.heavy-lock-1` exists (another seat; read only).

## D-decisions
- D1: new rows live in a NEW class at the end of `test_deploy_pre1.py` (the commission's file, borrowing helpers as `Pre1CopyRetention` does) rather than in `test_scripts.py` where rows 126_i..vii sit: keeps `test_scripts.py` (imported by two other test files) untouched.
- D2: the fix to item 6 reuses the sentence by fall-through, not a second copy of the text.
- D3: heavy runs 2 (base, head), not the round-1 three, since no fixture changes.

## Q-questions for Tuesday
- Q1: may a dry run print its existing last line on the all-exist path (S4 Q-FIX-1)? Default YES.
- Q2: item 5, option B (words) or A (code)? Default B, held either way.
- Q3: item 3a is comment-only and built; if Tuesday wants the header untouched too, drop commit 2 (rows A-C and D unaffected).

## UNMEASURED
Hosted CI on ubuntu with the real az on PATH (rows build their own PATH, but not run there); the runner's bash and Python versions; whether the reviewer's `allexist173` fall-through reading holds for hosted-mode dry runs (the kit orders a read of `:711-757` and a STOP if it does anything else); whether an unlisted dry-run row uses a non-`.local` out dir (matters only for option A).

## Outside-the-fences disclosure
Read-only: `gh api -X GET` (branch ref, main ref, open PRs, compare, contents raw of 9 files, commits list) under the project `GH_CONFIG_DIR`; `tmux list-panes`, `lsof`, `uptime`, `ls -d` on `.tools/` names; read of the reviewer's gate folder files (VERDICT, probes, tripwire script, runloop.py) by cat/sed. Wrote only the kit, its `.pre-stamp` and this report, plus scratch in `/private/tmp/b1517-drafter/`. No az, no hosted HTTP, no Jira, no git write, no `.local/`, no `Source_Documents`, no `4_Credentials/.azure`, no Secuura. One slip: my first tool call was a chain using a bare `=====` separator that the zsh hook refused; nothing ran.
