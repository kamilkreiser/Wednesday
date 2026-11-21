STARTABLE: YES

# B1882 DRAFTER REPORT: lane I (WP0.3 CI guards) fix round, round 2 of 2

Drafter: Opus 5.5, read-only, for Tuesday s307. Clock reads by `date`: 23:40:37 (start), 23:52:34, 00:00:32, 00:01:42, 00:10:16; the write clock is the sidecar's `WRITE` line. Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s307/d1882/` (`<d1882>`): `clone/` (push URL `invalid://no-push`), `gate/` (the seat's 14 tools), `logs/`, `scratch/`, `tools/`.

## BLUF
- The kit `2026-11-21_B1882_SEAT-X26_oxpd2-wp03-ci-guards-fix-round.md` commissions ONE fix commit on `b1861/wp03-ci-guard-follow-ups` (HEAD1 `782b3795`), fast-forward, no rebase. It answers all four Majors and every Minor the commission named, with the drafter's prototype built, red-first, mutated and scanned.
- **MEASURED on the prototype (`470f2fd3`, tree `79a6ca2d`):** cells against HEAD1's code `Ran 108`, `FAILED (failures=18)`, 9 distinct FAIL names, 0 ERROR; with the code `Ran 108`, `OK`; `PROVE2: PASS (7 rows)` (control FAIL); 38 mutants on the fixed code `37 killed, 1 survived` (the survivor named equivalent); `RULES: clean (412 files)` without `--source-documents`; CodeQL head 0+0, control 3+3; gitleaks clean, control fired; `words2.py` clean; both workflow steps by `run_step.py` green (`Ran 108`, `UNIT-TEST FLOOR: ran 108, floor 108`; neutral scan 25 of 25, wrong 0, reach 0).
- **No fingerprint constant moves**: the only `ci.yml` change is `FLOOR=84` -> `FLOOR=108`, which every fingerprint reads as `N` (MEASURED: the three constants equal the program's values on the fixed file; control: a one-byte edit elsewhere moves `REVIEWED_WORKFLOW`). `test_pipeline_controls.py` unchanged. No new file. Rules count unchanged by this round (412 on the branch).
- **Main moved to `f01b907e` (PR 13, lane E)**: 35 files since `5bb1418c`, 0 under `build/`, `.github/`, `README.md` (MEASURED); `merge-tree` of the fix with `f01b907e` rc 0, tree `25c5399a`, `RULES: clean (445 files)`, `Ran 108` OK on it.

## FACTS RE-MEASURED (instrument; control)
- Origin by `gh api -X GET` (project `GH_CONFIG_DIR`, 00:00:32): `refs/heads/b1861/...` = `782b3795...` (one row); `main` = `f01b907e...`; open PRs 0; PRs with head `b1861*` 0; `compare/5bb1418c...f01b907e` ahead 1, behind 0, 35 files.
- HEAD1 hosted (`hosted2.py`): `--total 1335 --rules 412 --skipped-linux 4 --skipped-windows 19 --unit 84 --floor 84 --hardened-scan` PASS; control `--unit 108 --floor 108` FAIL 2 on exactly the two `rules` rows. Main `f01b907e`: `--total 1392 --rules 443 ... --unit 60 --floor 60` PASS (a first run without `--total` printed `every total line: ['total: 1392', ...]`, FAIL 4 on the total rows: the control).
- Red (`logs/red.log`): the export of HEAD1 + `1-cells.diff`: 9 names (5+4+1+2+1+1+1+2+1 = 18 FAIL lines), `ERROR:` 0.
- R8 vs git 2.54.0 `check-attr` (`r8_vs_git.py`, 13 shapes): fixed `12 of 13 agree, holes 0, stricter 1`; HEAD1's code `holes 1` (the lone CR). Git splits lines at LF only and words at space, tab, CR (VT, FF, NEL are not separators: MEASURED).
- Readers' probes against the fixed code: B1880's six workflow diffs (F1, F2) now fire R6 (and R4 where a `uses` is unpinned); B1880's `g_probe.py` and `g_probe3.py`: F4 shapes G2, every m1 shape G3 but lzma-alone, BZh/MSCF text clean; B1879's `p1full` shapes are the cell's first two rows.
- Readers' own mutant programs on the fix: B1880's 16: 11 killed, 5 NOT APPLIED (old text moved); B1879's 22 (HEAD constant set to `470f2fd3`): 17 killed, 4 NOT APPLIED (m1, m5, m9, m16), m12 survived (named equivalent).
- Lane D's real publish folders (read-only): fixed guard and HEAD1's guard `GUARD: clean (10 files)` / `(11 files)`; release mode with a synthetic 1-fingerprint list clean 10 / 11; with the tracked list exit 2.
- Lane G (`8efae983`) merged with main + fix: clean, `RULES: clean (477 files)`, `Ran 108` OK.
- Toolchain: git 2.54.0 (Apple Git-157), gitleaks 8.30.1, Python 3.14.10, CodeQL 2.27.4. Load 2.79 at 00:01:42. `<project>/.tools/b1882` absent. Panes: `Datasec/OXPd2-X27` live, no X26.

## D-DECISIONS (all Tuesday's defaults; Questions Q14 to Q28 in the kit)
D15 `yaml_structure` (quotes followed, comment removed) and the block start read on it; D16 a `[` outside expression/quotes/comment is R6 (keeps `ci.yml:7` clean); D17 R8 = git's split; D18 the CA name anywhere in the whole joined path; D19 15 pinning cells, one per surviving non-equivalent reader mutant (B1879 m12 named equivalent, reasoned); D20 `BASH_FUNC_`; D21 NUL check plus a wrapped run (a failed git/export step, OSError or UnicodeError is exit 2: one step past the ruling's words, flagged as Q20); D22 full bzip2/cab magic; D23 lz4 (2), compress, ar, cpio (5 headers), ZIP-not-at-start via `zipfile.is_zipfile`, lzma-alone a named limit; D24 README/docstring limits; D25 records only; D26 diffs applied cells-first; D27 no fingerprint moves; D28 moved main (STOP-class Q26); D29 hosted numbers; D30 windows 120/90, X26, 38 mutants.

## Q-QUESTIONS FOR TUESDAY (each with a default; the two STOP-class ones need words in S4)
- **Q14 (STOP-class in part):** what "a comment never ... closes a block" means. Default: a comment line ends a block only by its indentation, like any line (YAML ends a block scalar at a less-indented line, comment or not), which is stricter. Alternative: a comment line never ends a block (risks a hole).
- **Q26 (STOP-class):** the moved main. Default per the commission: no rebase; STOP on any main change under `build/`, `.github/`, `README.md`; else `merge-tree` clean -> push `C1` alone; any conflict STOP.
- Q20: accept the wrapped run beyond the NUL check (default yes).
- Q18: accept B1879 m12 as equivalent (default yes).
- The rest as listed in the kit.

## CHAIN (each step's inputs exist at HEAD1 or come from an earlier step)
Step 1 needs `<src>` (exists, 14 files, sha256 in the sidecar `TOOLS` line) and the origin. Step 2 needs HEAD1 (Step 1's clone) and `1-cells.diff`. Step 3 needs Step 2's tree and the tools. Step 4 the green tree. Step 6 the staged tree and `commit-message.txt`. Step 7 `C1` and the fetch of 7(b). Table in the kit.

## STOP-SEVERITY CHECKS RUN ON THE DRAFTER'S OWN OUTPUT (PASS with a control) or NEVER RUN
- The 14 tool hashes: printed at the write clock (sidecar `TOOLS`); the seat compares.
- RED exactly 9 names, 0 ERROR: PASS (`prove2.py` STAGE cells; control `prove2.py` with BASE = the fix: FAIL).
- 8 sha256 equal `FIXED.sha256`: PASS (control in the same run would fail on any fuzzy apply; the BASE=fix control fails at apply).
- Fingerprints equal the constants: PASS (control: a one-byte edit gives False).
- `RULES: clean (412 files)` with the NOT RUN note: PASS.
- `C1`'s tree `79a6ca2d`: PASS on the drafter's commit (a tree sha does not depend on identity or time).
- mutants `37 killed, 1 survived ... True`: PASS.
- `R8-VS-GIT: 12 of 13 agree, holes 0, stricter 1`: PASS (control: HEAD1's code holes 1).
- CodeQL: PASS (0+0; control 3+3).
- Step 6(a)'s planted-list control, the identity comparison of 7(a), the push, the read-back and the hosted run of `C1`: NEVER RUN (marked so in the kit).

## UNMEASURED
- The hosted run of any new head (no push). The runner's Python 3.12 on the new cells (`mock.patch.object` on `tempfile.TemporaryDirectory`, `zipfile.is_zipfile` on short files): UNMEASURED, named in Step 7(g).
- GitHub's YAML parser's view of the R6 shapes (B1880 used Ruby Psych; the drafter used no parser).
- Real lz4 / compress / ar / cpio files: the cells use each format's magic plus filler (B1880's probe used real-shaped files: G3 on the fixed guard).
- The OSError branch of D21 (no cell; a named limit H29).

## OUTSIDE-THE-FENCES DISCLOSURE
- **Planted value, partial print (my incident):** at about 23:50 a `grep -n ... | cut -c1-30` over `ci.yml` printed the two half-lines: the head half whole (two characters) and the first ten characters of the tail half. The whole value was never typed or printed. It is in this session's transcript only, in no file I wrote (my program scans of `<d1882>` logs are for my literals; I did not write that output to a file). Tuesday may wish to note it. The kit now tells the seat never to cut a line holding a planted half.
- **Scratch identity:** my prototype commit and two scratch merge commits in `<d1882>/clone` (push URL `invalid://no-push`, never pushed) used `-c user.name=drafter -c user.email=drafter@invalid`, and the B1880 mutant program's scratch export repo `-c user.name=d`. No project repo was written; the kit forbids identity overrides for the seat.
- **Scratch worktrees** `scratch/merged` and `scratch/merged-g` were added to my own scratch clone (refs inside `<d1882>/clone/.git` only).
- **Reads in the OXPd_2 project folder:** read-only `ls` and the release guard over `<project>/.tools/b1831/out/{linux,windows}` (lane D's publish folders, as B1880 did); `<project>/CLAUDE.md`, `CLARIFICATIONS.md` size, the round-1 STATUS. Nothing written there. No `--source-documents`, nothing under `Source_Documents/`.
- **The readers' probe programs** (B1880 `g_probe.py`, `g_probe3.py`, `mutants.py`; B1879 `mutants.py`) were copied into `<d1882>/scratch` and run there against my scratch tree; their workflow diffs were applied with `patch` to copies in `<d1882>/scratch`. One B1880 diff (`bash-env-split-in-shell`) did not apply (hunk context); its `.rej` sits in my scratch.
- gh: `-X GET` only, under the project `GH_CONFIG_DIR`. No push, PR, Jira or mail. No dotnet, no lock. Nothing deleted.
- Model row: G1, `model-routing.md:108`; model id `models_latest.json:16-17` (`claude-opus-5-5`).
- Reading load for the seat: items 2 to 8 = 162131 bytes plus the kit (sidecar `LOAD`), about 250 kB for an Opus seat.
