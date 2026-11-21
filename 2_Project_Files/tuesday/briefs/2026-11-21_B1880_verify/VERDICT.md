GATE B1880: NO GO @ 782b379 on main 5bb1418 (second reader)

Reader B1880 (the adversarial reader of the guards), G1 round 1 of 2, Opus. Commission:
`2026-11-21_B1879-B1880_GATE_COMMISSION.md`. Kit: B1861 as stamped. Written 2026-11-21 AEDT.
Evidence: `probes/` (every probe program, plus each workflow probe as a diff against the head's ci.yml) and
`logs/` (every output). The workflow's planted value appears nowhere in this folder (grep for its tail half:
0 files; control: the head's ci.yml holds it 2 times, as its two halves).

## Why NO GO

Four guards let a shape through that their own stated property covers. The commission grades that as a
Major, and a Major is a NO GO in round 1. Each one is reproduced below with a control that fires.

| # | Sev | Guard | Shape that gets through | Measured |
|---|---|---|---|---|
| F1 | MAJOR | R6 | **A comment that ends `: |` or `: >` opens a block that is not there.** `R6_BLOCK_START` is searched over the raw line, so a full-line comment (`    # note: |`) or a trailing comment after a key with no value (`  extra: # note: |`) starts a "block". Every deeper line after it is then read as text: quoted keys, `{...}` flow mappings and backslashes all pass. In the probe a whole job hides this way, and R4 also misses its unpinned `- "uses": actions/checkout@main` (the quote sits between `uses` and `:`). | `repo_rules.py` on a clone of the head with that job appended: `RULES: clean (412 files)`, rc 0, for both comment forms. Control (the same job with no comment): rc 1, 4 R6 findings (lines 220, 221, 223, 224). Ruby Psych 3.1 (libyaml) parses all three files to the same job mapping. |
| F2 | MAJOR | R6 (and R4) | **A quoted key inside a flow sequence.** `steps: [ "uses": "actions/checkout@main" ]` is a single-pair flow mapping, so it has both a quoted mapping key and a flow mapping, the two shapes the ticket names. R6 looks for a quoted key only at the start of a line and for `{` only, so it misses this. R4 misses the unpinned `uses` too. | `RULES: clean (412 files)`, rc 0. Psych reads `steps` as `[{"uses": "actions/checkout@main"}]`. |
| F3 | MAJOR | R8 | **A lone CR used as the separator.** `.gitattributes` holding `* -text\rfilter=lfs\n`: git counts `\r` as a blank between attributes, but `splitlines()` turns `filter=lfs` into the first word of a "new line", and `split()[1:]` drops it. No fingerprint covers `.gitattributes`, so nothing else catches this. | `git check-attr filter text -- a.bin` (git 2.54.0) prints `filter: lfs`, `text: unset`. `repo_rules.py`: `RULES: clean (2 files)`, rc 0. Control (`* -text filter=lfs`): `RULES: R8 .gitattributes:1`, rc 1. |
| F4 | MAJOR (old behaviour, newly claimed) | G2 name rule | **A `!` after the CA name.** `base_name()` splits on the last `!` (the ZIP member separator) for files on disk and for member names too. So `ExtSDKRootCA!.cer` on disk, or a ZIP member `ExtSDKRootCA!x.cer`, has the base name `.cer` / `x.cer`. The new docstring defines a base name as "split on / and on \\" and says the rule fires on "a base name that holds ExtSDKRootCA anywhere". While the deny-list holds 0 fingerprints (today), the name rule is G2's only control. Main's prefix rule split on `!` the same way: the code is old, but the property is new in C5. | `GUARD: clean (1 files)`, rc 0, both shapes. Controls: `ExtSDKRootCA.cer` gives G2, rc 1; the ZIP member `ExtSDKRootCA.cer` gives `G2 a.zip!ExtSDKRootCA.cer`, rc 1. |

Every Major has a small fix (for Tuesday to put in the fix kit, not mine to build):
- F1: find a block start only outside a comment (strip a `#` that follows a space before the search; a whole-line comment never starts a block).
- F2: refuse a quoted key after `[` or `,` as well, or refuse `[` outside `${{ }}` the way `{` is refused.
- F3: split lines on `\n` only, then split attributes on `[ \t\r]`. That is git's own `blank` set.
- F4: take the base name from the member name or the on-disk name itself, not from the joined `path!member` text.
Mitigation that holds today for F1 and F2 only: any edit of `ci.yml` moves `REVIEWED_WORKFLOW` (measured: with the F1 probe the suite gives `FAILED (failures=1)` on `test_the_whole_workflow_is_the_reviewed_text`), and a second workflow file fails `test_the_workflow_folder_holds_the_one_workflow`. So a reader is forced to look, but the rule that reader relies on comes back green. Nothing mitigates F3 or F4.

## Minor and records findings

| # | Sev | Finding |
|---|---|---|
| m1 | Minor | **G3 archive formats outside the list are clean in every mode:** lz4 frame, Unix compress `.Z`, lzma-alone, `ar`, cpio newc, a ZIP with one byte in front of it (Python's zipfile opens it; the guard never tries, so its member `ExtSDKRootCA.cer` goes unjudged), and a file that starts `PK\x05\x06`. The docstring's opening sentence ("an archive it cannot open, is a finding") claims more than the closed list in brackets delivers. Name these as limits or add the magic bytes. Only brotli is named today. |
| m2 | Minor | **Release mode, certificate containers outside D12's list:** a PEM `-----BEGIN PKCS7-----` holding a listed certificate gives `clean`, rc 0, in default AND release mode with a 1-fingerprint deny-list. A base64 certificate in JSON (`"x5c": [...]`) is clean too. (A DER `.p7b` IS caught: G2.) The ticket asks for "a key store or certificate container it cannot read into"; D12 closed the list without these. Name them as limits, or add `*.p7b`/`*.p7c` and the PKCS7 label. |
| m3 | Minor | **False G3 on clean text:** a text file that starts `BZh` or `MSCF` gives G3, rc 1. It fails loud, never silent. bzip2's magic is really `BZh` plus `1`-`9`; cab's is `MSCF\0\0\0\0`. |
| m4 | Minor | **R6 does not refuse an exported bash function, which has the same power as `BASH_ENV`.** `env: BASH_FUNC_test%%: |` with `() { return 0; }` in a block: R6 gives no finding. bash (3.2 here, measured) imports it and every `test` in a later step then passes: `test 1 -eq 2` succeeds. The fingerprint is the only control. Suggest folding `BASH_FUNC_` into the BASH_ENV check in the fix round. Shell text that builds the name (`echo "BASH""_ENV=..." >> "$GITHUB_ENV"`) is also unseen: a named limit of any line rule. |
| m5 | Minor | **squash_scan, a NUL byte in the body:** git refuses the commit, and `subprocess.CalledProcessError` comes out as a traceback with rc 1. This is not one of the docstring's stated exits (the docstring promises 2 for an input it cannot use). It fails closed and prints no value. |
| m6 | Records (S3 iii) | **squash_scan, CR and non-UTF-8:** a subject or body with CRLF is stored verbatim. A planted value split by one lone CR scans `clean`, so the result is equal to main's scan only if GitHub does not normalise CRs when it squashes. That is UNMEASURED (no push). Non-UTF-8 input gives rc 2 (`cannot read an input`). |
| m7 | Minor (cells) | **10 of my 16 mutants survive the suite.** In each case the product code is right and only a cell is missing: R6 quoted key after `- `; R6 `{` not after `: ` (`- {a: b}`); R6 `- |` block start; R7 NUL only past byte 8000 (git's own binary heuristic window: the `late.txt` cell does not reach it); R8 tab separator; squash control rc not asserted; squash message copy counts not asserted; squash scratch-inside-checkout (H11, named); squash duplicate planted half; G3 `.jceks` name. |
| m8 | Records | **G1 searches ASCII and UTF-16LE only (as its docstring says).** UTF-16BE at the end of a file and UTF-32 are clean (UTF-16BE followed by an ASCII character is caught by the LE needle). A name in a text file with no NUL byte (`deps.json`) is clean by design. Name these as limits. |

## What I re-ran (all at head 782b3795 unless said)

- Origin by `gh api -X GET`: `refs/heads/b1861/wp03-ci-guard-follow-ups` = 782b3795..., the only b1861 ref; main = 5bb1418c...; compare: ahead 5, behind 0, 9 files. The local numstat equals the commission's (23/4, 17/10, 78/29, 68/3, 198/0, 56/4, 119/1, 78/1, 135/0). `ls-files` 412.
- Suite: `Ran 84 tests`, `OK`. `repo_rules.py` WITHOUT `--source-documents` on my scratch clone (whose parent holds no supplied-source folder): `R5 hash half NOT RUN`, `RULES: clean (412 files)`, rc 0.
- Hosted, by GET (`hosted2.py ... --total 1335 --rules 412 --skipped-linux 4 --skipped-windows 19 --unit 84 --floor 84 --hardened-scan`): `HOSTED 782b3795737cd34e527eee1a07b90d12f2cbb801: PASS`, run 44902762994, every job attempt 1. secret-scan: `NEUTRAL-EXPORT: listed 18 ... wrong 0` and `listed 996, copies of the right length 1992, wrong 0`; `NEUTRAL-SCAN-REACH: ... reaches 996, not among the stored objects 0`. rules: `Ran 84`, `UNIT-TEST FLOOR: ran 84, floor 84`, `RULES: clean (412 files)`. The hosted awk ran the new programs green (H14, as far as a green run can show).
- CodeQL CLI 2.27.4 (`codeql_py.py`): control 28d2852d (archived read-only from the seat's clone) `6 results (code-scanning 3, security-extended 3)`, rc 1. Head `0 results (code-scanning 0, security-extended 0)`, rc 0.
- Release guard on lane D's real publish folders (`.tools/b1831/out`, read-only): head and main each print `GUARD-WARN` + `GUARD: clean (10 files)` / `(11 files)`, rc 0. Head `--release` gives exit 2 (0 fingerprints), as designed. A copy of the head's guard with a synthetic 1-fingerprint deny-list: `--release` gives clean 10 / clean 11, rc 0 (no clean publish is refused in release mode). Another spelling of the same deny-list path is accepted (realpath).
- Whole-file fingerprint: no edit found that leaves it unmoved except the digits after `FLOOR=`, and `floors()` pins those. `FLOOR=084` passes both checks but means the same number to bash's `test`, so it is harmless. A BOM, a dropped final newline and an NBSP each move it.
- C4 export: read whole. Each copy is checked against its object's size (55 / 43008), the listing is counted by NR, and the reach check uses `rev-list --objects --all`. I found no listing or copy fault that stays green beyond what D6 states (a tree's first copy is judged only as longer than 55 bytes or not).
- S3 outside the frame: (i) a tracked symlink is judged by its TARGET's bytes (to a binary: R7; dangling: R0). A gitlink gives R0, absent or as an empty folder. Both are loud. (ii) a ZIP inside a ZIP: found at depth 2 and 3, G3 at depth 4. A ZIP inside a tar: G3 for the tar. (iii) see m6.

## Mutants of my own (product code; each applied once, suite run, file written back, `git status --porcelain` empty after each)

Killed by assertion (FAIL, 0 ERROR), 6, beyond the kit's 34: `b-r6-bash-env-case-sensitive`, `b-r8-tracked-root-file-only`, `b-g-name-case-sensitive` (3 FAIL), `b-g-cab-unseen`, `b-g-utf16-pem-text-only`, `b-ci-tree-length-check-dropped` (the scan job's and the whole file's fingerprints plus the outside-edit cell). Survived: 10 (m7). After all of them: `Ran 84`, OK. Log: `logs/mutants.log`.

## Deviation ruled (B1880: deviation 1)

**Deviation 1: CONFIRMED, the seat's reading is right.** I re-ran the red stage of C2 myself: a worktree at C2 (a1c77fa) with C1's `build/repo_rules.py` put back. Result: rc 1, `Ran 71 tests`, `FAILED (failures=16)`; 16 `FAIL:` lines that reduce to exactly 8 distinct cell names, the kit's eight; `ERROR:` 0. Three cells fail in 3 subTests each (quoted-key, backslash, block) and R8 in 3, which accounts for the 16. The kit's `failures=8` counted names, not the unittest summary line. Log: `logs/c2-red-rerun.log`.

## What I did NOT test

Anything on Windows. Ubuntu's mawk run locally (only the hosted green run covers it). GitHub's own workflow YAML parser (I used Ruby Psych/libyaml as the reference: a parser that refused F1 or F2 would make them harmless, but that is UNMEASURED). NEL (U+0085) as a line break (Psych 1.1 breaks on it, which agrees with the reader). A `working-tree-encoding` that drops a NUL (macOS iconv refuses UTF-7 with U+0000; glibc NOT RUN). GitHub's normalisation of a squash message. prove.py and scan_faults.py re-runs, deviations 2 to 4, the scope census, C1 to C5 against their scope sentences, the merge and the later-lanes table, and the landing texts: all of these are reader B1879's and I did not run them. No push, no pull request, no Jira, no mail. Nothing written in the OXPd_2 project folder.
