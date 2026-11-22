GATE B1891: NO GO @ ff1defa on main ca94ed9 (second reader)

Reader B1891 (successor of round-1 reader B1880, the adversarial reader of the guards), G1 round 2 of 2, Opus.
Commission: `2026-11-22_B1890-B1891_GATE_COMMISSION.md`. Kit: B1882 as stamped (S1 to S7 read). Written 2026-11-22 AEDT
(clock at start 10:28:11, origin read 10:39:48). Evidence: `probes/` (every probe program, and each workflow probe as a
diff against the head's ci.yml) and `logs/` (every output). Scratch: my session scratchpad only (a `draft` clone by the
kit's `clone.py`, push URL `invalid://no-push`, and three worktrees of it). The workflow's planted value appears in no file
of this folder (by program: 54 files, 0 holding its tail half or the whole value; control: the head's ci.yml holds the
tail half 2 times).

## Why NO GO

Every round-1 F1 to F4 probe of mine is now caught, and every item the kit assigned to me holds (below). But three new
shapes get past R6 and R8, the same class as round-1 F1 and F3, which the kit's own property covers ("R6 starts a block
only where YAML does; R8 splits as git splits"). The commission grades "an R6/R8/G2/G3 hole of the same class" as NO GO.
Each one comes with a control that fires. All three were holes at HEAD1 too: this round did not add them. It claims a
property that they break.

| # | Sev | Guard | Shape that gets through | Measured |
|---|---|---|---|---|
| N1 | MAJOR | R6 (and R3, R4 with it) | **A UTF-8 letter whose last byte is 0x85, in a comment, opens a phantom block.** `judge()` reads a workflow as `data.decode("latin-1").splitlines()` (`build/repo_rules.py:323`). `str.splitlines()` breaks at U+0085, so `Å` (C3 85) or `ą` (C4 85) splits the line in two. Then `  extra: # Åb: |` becomes the line `  extra: # Ã` and the line `b: |`, which is a block start at column 0. Every deeper line after it is read as text. In the probe a whole job hides this way: `"runs-on"`, `"permissions": write-all`, `env: {A: b}`, `- "uses": actions/checkout@main`, a backslash. This does not depend on any parser's leniency: every UTF-8 YAML reader sees `Å` as a letter inside the comment. | `repo_rules.py` on a worktree of the head with the shape appended: `RULES: clean (412 files)`, rc 0, for both a trailing comment and a full-line comment (`a-ring-in-trailing-comment`, `a-ogonek-in-full-line-comment`). Control (the same with a plain `A`): rc 1, R6 at lines 220, 221, 222, 224, 225. Ruby Psych (libyaml 0.2.1) parses all three to the same job mapping, with `permissions: write-all`. HEAD1: clean, rc 0 (old). Logs `x85_probe.txt`, `*.rules.txt`. |
| N2 | MAJOR (parser-dependent) | R6 | **A multi-line quoted scalar whose continuation line ends `: |`.** `    name: "a` then `  b: |` then `    "`. `yaml_structure` treats an unclosed quote as running to the end of ITS line only, so the next line is read as YAML afresh, and `  b: |` opens a block. Lines indented 4 after that are text to R6, but they are keys of the job to YAML. Single quotes and a continuation at column 0 work the same way. | `RULES: clean (412 files)`, rc 0, for all three shapes. Control (the quote closed on one line): rc 1, 4 R6 findings. Psych parses the job mapping with every hidden key. **Limit:** YAML 1.2 wants a continuation line indented more than the mapping, so a strict parser refuses these files. libyaml accepts them. Whether GitHub's parser accepts them is UNMEASURED (the same reference standard round 1's F1 was graded on). If GitHub refuses them, N2 becomes records only. |
| N3 | MAJOR | R8 | **A quoted pattern with the attribute right after its closing quote:** `"a.bin"filter=lfs`. Git (`attr.c`) unquotes the pattern and then reads attributes from just after the quote, with no blank needed. R8 splits on blanks only, so the whole line is one word and `words[1:]` is empty. This contradicts D17 and the new README sentence ("split into lines and words where git splits it"). The kit's `r8_vs_git.py` tested a quoted pattern only with a space after it. | `git check-attr filter` (git 2.54.0): `a.bin: filter: lfs` for `"a.bin"filter=lfs`, `"*"filter=lfs` and `"x y"filter=lfs`. `repo_rules.py`: `RULES: clean (4 files)`, rc 0, for all three. Controls: `* filter=lfs` and round 1's `* -text\rfilter=lfs` give `RULES: R8 .gitattributes:1`, rc 1. No fingerprint covers `.gitattributes`. Log `r8_probe.txt`. |

Small fixes for each Major (for Tuesday's card; not mine to build):
- N1: split workflow lines on `\n` only, with any `\r` taken as a line end the way YAML takes it, as R8 now does. Or refuse every byte outside printable ASCII under `.github/workflows/`, since today's ci.yml is ASCII only, as the seat measured.
- N2: carry an unclosed quote over to the next lines, with no block start until it closes. Or make an unclosed quote an R6 finding: there is no multi-line quoted scalar in ci.yml today.
- N3: for a line that starts with `"`, end the pattern at its unescaped closing quote and read the attributes from there, as git does.

Mitigation, the same as round 1: every one of these edits moves `REVIEWED_WORKFLOW` (N1, N2), and the suite fails `test_the_whole_workflow_is_the_reviewed_text` (measured for N2: `FAILED (failures=1)`). So a reader is forced to look, but the rule that reader relies on still reads clean. Nothing mitigates N3.

## Minor and records findings

| # | Sev | Finding |
|---|---|---|
| m9 | Minor (cells) | **4 of my 21 mutants of the fixed code survive** (`logs/mutants2.log`). In each case the product code is right and a cell is missing: `n-yaml-hash-anywhere` (a `#` with no blank before it starts a comment); `n-yaml-quote-anywhere` (a quote opens anywhere, not only where a token starts); `n-r8-comment-any-word` (a line is skipped when any word starts `#`); `n-g3-cpio-binary-one-order` (`71 C7` dropped). |
| m10 | Minor (text) | **G3: formats that have magic bytes but are not on the list are clean:** lzip (`LZIP`), a zlib stream, OLE compound file / MSI (`D0 CF 11 E0`), xar, squashfs, WIM (`logs/g3_more.txt`; control xz: G3). The README and the docstring now say "Formats with no magic bytes are not seen: brotli, lzma-alone, an old tar". That reads as if every format with magic bytes is seen. Name these limits, or add their magic. |
| r1 | Records | Unchanged and still records (D25 and round-1 m2, m6, m8): a PKCS7 PEM and `x5c` JSON are clean in default and release mode; a planted value split by a lone CR scans clean in the squash scan; UTF-16BE at the end of a file, UTF-32 and a name in a text file with no NUL are clean; lzma-alone is clean; `'X''Y':` is not seen as a quoted key; NEL inside a comment (H20). The NEL shape is a near relative of N1: a NEL byte pair C2 85 is a line break to YAML 1.1 and libyaml, but not to YAML 1.2. N1 is the shape where no YAML reads a break at all. |
| r2 | Records (reader incident) | I typed a four-character literal as a `grep -c` pattern over my own hosted log (`logs/hosted.txt`; count 0). It may be longer than the planted value's two-character head that the commission allows. Nothing was printed and no file holds it. Every other check of the value was made by program from the workflow's two halves. |

## What I re-ran (all at head ff1defac unless said)

- **Origin by `gh api -X GET`** (10:39:48): `matching-refs/heads/b1861` one row = ff1defac...; main = ca94ed96...;
  `compare/782b3795...ff1defac`: ahead 1, behind 0, 8 files; pull requests of any state with a head starting `b1861`: 0;
  open: 0. Local: ff1defac has ONE parent 782b3795, tree `79a6ca2d746c8aa18591dea012ebc8c7c4e13b51` (FACT 5).
- **Scope (both):** `diff --name-status 782b3795 ff1defac` gives exactly the eight `M`. The numstat equals FACT 5 (1/1, 5/5, 29/14, 63/16,
  18/9, 75/0, 98/0, 89/0). The eight sha256 equal `FIXED.sha256` (8 of 8). `diff --quiet` over `test_pipeline_controls.py`
  `src tests packaging contracts build/denylist Datasec.Suite.slnx Directory.Packages.props` rc 0 (control README.md rc 1);
  `ls-files` 412; no `A`/`D`/`R`; no removed test method. `ci.yml` changes only `FLOOR=84` -> `FLOOR=108`. The three
  fingerprint constants each equal the program's value on the head's ci.yml (`scan True rules True whole True`; control:
  a one-letter edit moves the whole-file value). Indented `def test_` 108, column-1 0, = `FLOOR`.
- **Suite:** `Ran 108 tests`, `OK`. **`repo_rules.py` WITHOUT `--source-documents`** (scratch with no supplied-source
  folder): `R5 hash half NOT RUN`, `RULES: clean (412 files)`, rc 0.
- **Read whole:** the product diffs of the three programs and README, and the three test diffs. README and docstrings
  against the code: accurate, but for the N3 (R8 split), N1/N2 (R6 "starts a block only where YAML does") and m10 (G3) points above.
- **Every probe of round-1 F1 to F4 and m1 to m8, re-run:** F1 `comment-opens-block` R6 [200, 201, 202]; `full-line-comment`
  R6 [221, 222, 224, 225]; `trailing-comment` R6 [220, 221, 223, 224] (control the same); `trailing-comment-block` quiet
  (no phantom any more, nothing hidden). F2 `flow-seq-quoted-key` and `flow-seq-bare-key` R6 [221]. F3 (`* -text\rfilter=lfs`)
  R8, rc 1. F4 `ca-name-with-bang-after` G2, `ca-name-bang-in-zip-member` G2 (`a.zip!ExtSDKRootCA!x.cer`). m1: every shape
  G3 but lzma-alone (a named limit). m3: `BZh`/`MSCF` text clean. m4: `BASH_FUNC_test%%` R6 [19]. `bash-env-split-in-shell`
  is clean (H19, a named limit). m5: NUL in the body gives exit 2 `the subject or the body holds a NUL byte`. m2, m6 and m8
  are unchanged (records). The ZIP depth 2 and 3 cases give G2, depth 4 gives G3, a ZIP in a tar gives G3. The fingerprint
  probe: a BOM, a dropped final newline and an NBSP each move it; a changed digit after `FLOOR=` does not, and `floors()`
  pins it.
- **My 16 round-1 mutants:** 11 KILLED, 5 NOT APPLIED (old text moved), the same as the drafter measured. I re-made those 5 on
  the fixed lines (`r-*`): all 5 KILLED. **New mutants of the fixed code: 16** (`n-*`), 12 KILLED by assertion, 4 SURVIVED (m9).
  Every row is FAIL-only (0 ERROR), with porcelain empty after each. After all of them: `Ran 108`, OK.
- **Release guard on lane D's real publish folders** (`.tools/b1831/out/linux` and `windows`, read only): default
  `GUARD-WARN` + `GUARD: clean (10 files)` / `(11 files)`, rc 0, the same as HEAD1. `--release` with the tracked list:
  `the development CA deny-list holds 0 fingerprints`, rc 2. A copy with a synthetic 1-fingerprint list in `--release`:
  clean 10 / clean 11, rc 0.
- **Q14 as built: HOLDS, and it opens no hole** (`logs/q14_probe.txt`, with Psych). A deeper `# x: |` line inside a block is text to
  both R6 and YAML. A less-indented comment line ends the block for both (Psych: a less-indented comment and then keys parse
  as keys; R6 judges them and fires). Deeper text after such a comment is a YAML error, and R6 judges it as YAML, so R6 is
  stricter. A comment never opens a block (F1 shapes above). **Q26 as built: HOLDS.** C1 was pushed alone (one parent, no merge commit).
  `diff --name-only 5bb1418c ca94ed96`: 50 rows, 0 under `build/`, `.github/` or `README.md` (control with a planted
  `build/x.py`: 1). `merge-tree --write-tree ca94ed96 ff1defac`: rc 0, tree `9a1e42a2...`, 446 files (equal to S3). The
  merged tree's rules and suite are B1890's to measure, not mine.
- **CodeQL CLI 2.27.4** (`codeql_py.py`): head ff1defac `0 results (code-scanning 0, security-extended 0)`, rc 0; control
  28d2852d `6 results (code-scanning 3, security-extended 3)`, rc 1.
- **Hosted, by GET** (`hosted2.py ff1defac... --total 1335 --rules 412 --skipped-linux 4 --skipped-windows 19 --unit 108
  --floor 108 --hardened-scan`): `HOSTED ff1defac24c24a0331af201db6a7d0cc6de40d3d: PASS`, run 44961377381, every job
  attempt 1. secret-scan: `listed 18 ... wrong 0`, `listed 1061, copies of the right length 2122, wrong 0`,
  `NEUTRAL-SCAN-REACH: ... reaches 1061, not among the stored objects 0`. rules: `Ran 108`, `UNIT-TEST FLOOR: ran 108,
  floor 108`, `RULES: clean (412 files)`. linux `GUARD: clean (10 files)`, windows `(11 files)`.
- **Words and scanner:** 378 added lines and the commit message (386 bytes, byte-equal to the kit's `commit-message.txt`):
  `words2.py --control` `CONTROL FIRED: 13 of 13`; `WORDS: clean (2 files)`. gitleaks 8.30.1 control (the value built from
  the two halves, never printed) rc 1; the added lines and the message under neutral names: rc 0, `no leaks found`.

## What I did NOT test

GitHub's own workflow parser (N2 rests on libyaml and Psych; N1 does not need it). Anything on Windows. The merge of the head
with ca94ed96 measured by rules and suite, the merge with lane G's head edaa1b70, the landing texts, `prove.py`,
`scan_faults.py`, the drafter's `prove2.py` and `mutants.py`, and the seat's one deviation: these are reader B1890's, and I
did not run them. I did not build a fix for N1 to N3. No dotnet, no lock, no `--source-documents`, nothing under
`Source_Documents/`. No push, no pull request, no Jira, no message. Nothing written in the OXPd_2 project folder.
