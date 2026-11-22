GATE B1894: NO GO @ a9dc8cd on main e1e8043 (second reader)

Reader B1894 (successor of round-2 reader B1891), lane I round 3 (the refuse round), delta review, Opus.
Commission: `2026-11-22_B1893-B1894_GATE_COMMISSION.md`. Kit: B1892 as stamped (S1 to S7). Ruling printed by
`decision_queue.sh show datasec-oxpd-ci-guards-round2-nogo-1122`: choice a, ruled 2026-11-22T13:53:27. Written
2026-11-22 AEDT, 14:35 to 14:46. Evidence: `probes/` (each program, and each new workflow shape as a diff against the
head's ci.yml) and `logs/` (every output). Scratch: my session scratchpad only (a `draft` clone by the kit's
`clone.py`, push URL `invalid://no-push`, worktrees of it). The planted value is in no file of this folder (by program:
36 files, 0 holding its tail half or the whole value; control: the head's ci.yml holds the tail half 2 times).

## Why NO GO

Refusal 1 (bytes) and refusal 3 (a quote in an attribute line) refuse every shape I could make of their class, through
the whole program. **Refusal 2 does not refuse its own shape.** The ruling's words are "no quoted value spread over
lines". The refusal is built on `yaml_scan`, and `yaml_scan` opens a quote at ANY token start, also inside a plain
scalar. YAML opens a quote only where a node starts. So a quote inside a plain KEY makes `yaml_scan` pair it with the
real opener of the value. `yaml_scan` then reports the line closed, while YAML holds the value open over the next
lines. The N2 trick then works unchanged: the continuation line `  b: |` opens a phantom block, and the rest of the job
is hidden from R3, R4 and R6. The commission grades "a refusal that does not refuse its shape, a hole of the SAME three
classes still open through the whole program" as NO GO.

| # | Sev | Refusal | Shape that gets through (appended to the head's ci.yml as job `extra`) | Measured |
|---|---|---|---|---|
| P1 | MAJOR (parser-dependent, the same standard as N2) | 2 (D32), inside the closed list | `    k "x: "a` then `  b: |` then `    "`, then the hidden lines `"runs-on": ubuntu-latest`, `env: {A: b}`, `steps:` with `- "uses": actions/checkout@main` and a backslash. YAML: the key is the plain scalar `k "x`, and its value `"a` is a double-quoted scalar left open. `yaml_scan`: the quote at `"x` opens, the quote at `"a` closes, so it reports closed. Variants that also pass: `k 'x: 'a` (single), `k 'x: "a'` and `k "x: 'a"` (the other quote spans the opener), the continuation at column 0, the same in a sequence entry (`- k "x: "a`), and two through expression removal (`${{ x: "a }}`: the opener sits inside the removed `${{ }}`; `k ${{ y }}#: "a`: the removal puts a blank before `#`, so `yaml_scan` reads a comment that YAML does not see). | `repo_rules.py` of the head on a fresh git tree (export, `git init`, `add -A`): **`RULES: clean (412 files)`, rc 0, for all 8 shapes** (`logs/d32-new-shapes-whole.txt`, `logs/d32-new-shapes2-whole.txt`). Controls on the same tree: `k x: "a` (no quote in the key) gives `R6 ci.yml:220`, rc 1; the hidden lines alone fire R6 at 221, 222, 224 and 225. Ruby Psych 2.6.10 / libyaml 0.2.1 reads each job with the hidden keys (`["k \"x", "runs-on", "env", "steps"]`; in full: `"k 'x"=>"a' b: | ", "runs-on"=>"ubuntu-latest", "env"=>{"A"=>"b"}, "steps"=>[{"uses"=>"actions/checkout@main"}, ...]`). One more shape, `name: x 'y: "a'`, is INVALID to Psych (not counted). At HEAD2 every one of these is also rc 0, so the hole is old: this round's refusal does not close it. **Limit:** like N2, each shape needs a continuation line indented less than its mapping; YAML 1.2 forbids that and libyaml accepts it. Whether GitHub's parser accepts it is UNMEASURED. |

A small fix for P1 (for Tuesday's card; not mine to build): (i) take the open-quote reading on the line as written, as
well as with its expressions removed; and (ii) a quote outside a block that is not the first character of a value (at
the line's first non-blank, after `- `, or after `: `) is an R6 finding. Cost today: of the 114 lines of ci.yml outside
a block, 4 hold a quote, and 0 hold one that is not at a value start (`probes/quote_census.py`; control: the P1 file
gives 1, at line 220). Mitigation, as in rounds 1 and 2: every such edit moves `REVIEWED_WORKFLOW`, so a reader is made
to look, but the rule that reader relies on still reads clean.

## Minor and records findings

| # | Sev | Inside the three? | Finding |
|---|---|---|---|
| m11 | Minor (cells) | no (old code) | Of my 21 round-2 mutants, 3 now survive on the head (were 4): `n-yaml-hash-anywhere`, `n-r8-comment-any-word`, `n-g3-cpio-binary-one-order`. `n-yaml-quote-anywhere` is now killed (by the D32 cell). These are records under the ruling (B1891 m9). |
| r3 | Records | refusal 1 | `x85_probe.py` still prints `R6 []` for the N1 shapes on the head. That is expected: it calls `check_spellings()` directly, and refusal 1 lives in `judge()`. The whole-program run is the test, and it fires (below). |
| r4 | Records (reader incident) | n/a | My session scratchpad is shared with reader B1893's session. B1893 wrote an untracked `repo_rules.py` at the root of my `head2` worktree, and two programs into my `probes/` folder (14:41). It is byte-equal to HEAD2's `build/repo_rules.py`. No run of mine reads either file: `whole.py` exports from git, and the other probes run `build/repo_rules.py`. From 14:43 I worked in a separate subfolder. Nothing was deleted. |

## What I re-ran (at head a9dc8cd9 unless said)

- **Origin and scope:** the clone reads branch = a9dc8cd9, main = e1e8043d. a9dc8cd9 has ONE parent, ff1defac, and tree
  `c7dad617257d1813da56599ee0a78177f1b1c2dd` (= FACT 5). `diff --name-status ff1defac a9dc8cd9`: exactly four `M`.
  Numstat 1/1, 2/2, 31/5, 64/0. `diff --quiet` over `test_pipeline_controls.py`, `release_guard.py`, `squash_scan.py`,
  their tests, `src tests packaging contracts build/denylist`: rc 0 (control README.md: rc 1). I read the product diff
  whole. Outside D31 to D33 it changes only docstrings: `yaml_structure` now returns `yaml_scan(line)[0]` with the loop
  unchanged; `check_spellings` gains one finding; R8 gains one finding; `judge` gains `check_plain`. README and the
  docstrings match the code, except the claim of R6 that P1 breaks.
- **Fingerprints and floor:** `scan True rules True whole True floors [111]` (control: a one-letter edit gives
  `whole False`). Constants unchanged (the diff of `test_pipeline_controls.py` is 0 lines). Indented `def test_` 111,
  column-1 0, `FLOOR=111` (`ci.yml:211`).
- **Suite:** `Ran 111 tests`, OK. **`repo_rules.py` WITHOUT `--source-documents`** (no `1_Project_Definition` in the
  worktree, rc 0): `R5 hash half NOT RUN`, `RULES: clean (412 files)`, rc 0.
- **N1, N2 through the whole program** (B1891's exact shapes, regenerated byte-equal to its `*.ci-yml.diff`;
  `logs/n-probes-whole.txt`). At HEAD2 all five shapes (two N1, three N2) are rc 0, clean (as round 2). On the
  head: `a-ring-in-trailing-comment` R6 :219, `a-ogonek-in-full-line-comment` R6 :220, the three N2 shapes R6 :220
  each, rc 1. Both controls are rc 1 on both trees. Psych reads the hidden keys in every shape.
- **Refusal 1, every byte:** all 159 bytes outside 0x20 to 0x7E and LF (NUL left to R7), placed in the N1 comment,
  plus C2 85, U+2028, U+2029, a BOM mid-line and at file start, C4 85, and a lone CR at the end with no final LF:
  **167 of 167 rc 1**, R6 at the planted line (`logs/n1-bytes-head.txt`). Refusal 1 holds.
- **N3:** `r8_probe.py` (`logs/r8_probe.txt`). At HEAD2 the three quoted shapes are rc 0 while git sets `filter: lfs`. On
  the head each is `RULES: R8 .gitattributes:1`, rc 1. `macro-use-only-control` is rc 0 on both, and the two controls
  are rc 1 on both. **12 more shapes** (`probes/r8_more.py`, `logs/r8_more.txt`): an indented quote, a tab before it, a
  CR before it, a BOM before it, `"#a.bin"`, an escaped quote, the quote then a tab, a CRLF file, a nested
  `sub/.gitattributes`, the second line after a plain one, and no final LF. Each is rc 0 at HEAD2 and rc 1 on the head,
  with git setting `filter: lfs` in each. A comment line holding quotes is quiet on both. Refusal 3 holds.
- **Mutants on the head** (`logs/mutants-round1-on-head.log`, `logs/mutants2-on-head.log`). Round-1's 16: 11 KILLED and
  5 NOT APPLIED (old text moved), as in round 2. My 21 `r-*`/`n-*`: 18 KILLED and 3 SURVIVED (m11). Every kill is
  FAIL-only (0 ERROR), with porcelain empty after each. After all of them: `Ran 111`, OK.
- **Release guard on lane D's publish folders** (`.tools/b1831/out/linux` and `windows`, read only, the head's
  unchanged code). Default: `GUARD-WARN`, then `GUARD: clean (10 files)` / `(11 files)`, rc 0. `--release`: `the
  development CA deny-list holds 0 fingerprints`, rc 2. A copy of `build/` with a synthetic one-fingerprint list,
  `--release`: clean 10 / clean 11, rc 0. All as in round 2.
- **CodeQL CLI** (`codeql_py.py`): head `CODEQL a9dc8cd93969: 0 results (code-scanning 0, security-extended 0)`, rc 0.
  Control 28d2852d: `6 results (code-scanning 3, security-extended 3)`, rc 1.
- **Hosted, by GET** (`hosted2.py a9dc8cd9... --total 1335 --rules 412 --skipped-linux 4 --skipped-windows 19 --unit 111
  --floor 111 --hardened-scan`): `HOSTED a9dc8cd93969dfd5f623c10345257b6e6a723104: PASS`, run 44980825061, every job on
  attempt 1. linux 1335/1331/4, `GUARD: clean (10 files)`. windows 1335/1316/19, `(11 files)`. rules: `Ran 111`,
  `UNIT-TEST FLOOR: ran 111, floor 111`, `RULES: clean (412 files)`. secret-scan: planted control 25 of 25,
  `NEUTRAL-EXPORT: listed 18 ... wrong 0` and `listed 1072 ... wrong 0`, `NEUTRAL-SCAN-REACH: ... 1072, not among the
  stored objects 0`, 52 commits scanned, no leaks.
- **Words and scanner:** 98 added lines, and the commit message (278 bytes, byte-equal to the kit's
  `commit-message.txt`). `words2.py --control`: `CONTROL FIRED: 13 of 13`. Over both: `WORDS: clean (2 files)`.
  gitleaks 8.30.1: the control (the value cut by `squash_scan.cut(...)[1]`, length 41, never printed) rc 1; the added
  lines and the message under neutral names rc 0, `no leaks found`.

## What I did NOT test

GitHub's own workflow parser (P1, like N2, rests on libyaml and Psych; a spec-strict parser refuses these shapes). The
merge with main e1e8043d, the landing texts, `p2full.py`, `r6probe2.py`, B1890's mutants, the drafter's `prove3.py`,
`mutants3.py`, `mutants.py` and `frame3.py`: these are B1893's, or the seat's, and I did not run them. Anything on
Windows. I did not build a fix for P1. No dotnet, no lock, no `--source-documents`, nothing under `Source_Documents/`.
No push, no pull request, no Jira, no message. Nothing written in the OXPd_2 project folder.
