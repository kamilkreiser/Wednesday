VERDICT: GO WITH NOTES — head 430dde30be41e026b909e271f698f8013325e892

# QA-SCANNER-NOTES: independent check of branch `scanner-notes`

Seat QA-SCANNER-NOTES, 2026-11-25. Brief: Friday's `briefs_drafts/2026-11-25_coagent_QA-SCANNER-NOTES_check_brief.md`, read whole. I did not make the lane. Work dir `/private/tmp/claude-501/qsn` (own clone, own empty target dir and cargo home whose `bin` and `rustup` are links to the project's toolchain, as `coagent_merge_check.sh` does; `RUSTUP_TOOLCHAIN=1.100.0`: cargo 1.100.0 (3acc79c0c 2026-11-05), rustc 1.100.0 (0ef1bc386 2026-11-09)). Every cargo run used `--manifest-path` (no `cd`). Every comparison by SHA. TESTED = I ran it; READ = I read it. Every secret-shaped string below is made up; no byte of a generated or corpus text is quoted (cases by number and family only).

## BLUF
- **Does the scanner still flag everything it flagged?** Yes. Over 900 000 generated texts (the two earlier checks' generators and seeds, plus seeds of mine), nothing flagged at main is Clean at the head and no family is lost; with the lane's three items reverted the head answers exactly as main on every text. My own 170 733 targeted texts (every flag start with the new forms around it, base64 and `.netrc` behind every line-end combination, colour codes with invisibles at every position) lose nothing either, and an exhaustive comparison of 137 256 line-end patterns finds only the ruled change.
- **Are the two regressions closed?** Yes. Short base64 lines behind `\r\r\n` (and `\r \r\n`, `\r\t\n`, `\r\r\r\n`) flag again, and so do the shapes with an invisible next to or inside a colour code: both classes are 0 against the pre-fix scanner, and what remains is only the three ruled classes.
- **Did the over-flag rates move?** No. Chat 2.6 %, report lines 28.3 %, flag sentences 33 %, before and after; not one of 388 sentences changes. The new forms flag argv lists, `--user=a:b` and a flag right after a written `\n` in JSON, when the option name looks secret.
- **Not covered:** a pretty-printed argv list with a line break after the comma and a few other forms still pass and are not yet in the docs' list of misses (N-1, Minor); `check.sh` whole and Linux/Windows were not run by me.

## Proofs (section 0) — TESTED
- `git ls-remote gh scanner-notes main` (GitHub remote, deploy key) → `430dde30be41e026b909e271f698f8013325e892 refs/heads/scanner-notes` · `9145840f24f23aff5b589044ce8aa8776283bdac refs/heads/main`. Both match the brief. The local project repo's `origin/scanner-notes` is the same `430dde3…`.
- `git merge-base --is-ancestor f193620… 430dde3…` → exit 0; `git merge-base f193620 430dde3` = `f193620c…`. `9145840` is NOT an ancestor (main's later merge not taken in, by the brief's rule; it changed the audit-host crate, not the scanner).
- `git log --oneline f193620..430dde3` → 2 commits: `a721330` (the lane), `430dde3` (leaves `Finding`'s doc comment as at main).
- Builder STATUS `coagent/5_Project_History/STATUS_SCANNER_NOTES.md`: 195 lines; last line `READY FOR QA SCANNER-NOTES`, line above it `430dde30be41e026b909e271f698f8013325e892`. Matches.
- `git diff --stat f193620...430dde3` → 11 paths, 490+ / 33−, as the drafter counted.

## 1. Head, base, scope — TESTED
- `git diff --name-only f193620...430dde3` → 11 paths: `BACKLOG.md`, `crates/coagent-scanner/{build.rs, src/families.rs, src/lib.rs, tests/t03_known_overflag.rs, tests/t05_bounds.rs, tests/t07_pure.rs, tests/t08_docs.rs, tests/t10_notes.rs}`, `docs/SCANNER.md`, `scripts/red-controls-scanner.sh`. Filter against the brief's owned set → **none outside it**; control: the same filter fed `crates/coagent-audit/src/x.rs` prints it. `--summary`: one create (`t10_notes.rs`, 100644), no mode change.
- Forbidden paths: `git diff f193620 430dde3 -- Cargo.toml Cargo.lock crates/coagent-scanner/Cargo.toml <crate>/tests/{t01_flagged,t02_clean,t04_display,t06_property,t09_fix_round}.rs <crate>/tests/common preview spikes | wc -c` → **0**; every other crate (`crates ':!crates/coagent-scanner'`) → **0**; every other script → **0**. Control: the same over `crates/coagent-scanner` → **28 356** bytes.
- Blob for blob, `f193620` = `430dde3`: t01 `6f62ca7c…`, t02 `7fd6c58e…`, t04 `9c8459ff…`, t06 `e1de2466…`, t09 `c914b585…`, `tests/common` tree `f32df043…`, crate `Cargo.toml` `2e5542eb…`, root `Cargo.toml` `5c0f3bc3…`, `Cargo.lock` `0094acf1…`. **All identical.**
- `lib.rs` lines 1-179 (`Kind`, `text()`, `Finding`, `Verdict`, `is_format_char`): `diff` of `sed -n 1,179p` at both SHAs → **identical**; the first difference is line 180 (`stripped`'s doc comment).
- `git diff --numstat f193620 430dde3` on every existing test file, the script, `build.rs`, `BACKLOG.md`: removed lines **0** in each (t03 +48, t05 +21, t07 +54, t08 +1, script +4, build.rs +4, BACKLOG +5); `docs/SCANNER.md` +46 −10 (rewritten paragraphs, §2 row, §5 row). No `unsafe` in any added line.
- Judgement: **scope clean; no existing assertion changed or removed.**

## 2. The code, line by line — READ
Read: the whole diff `f193620...430dde3` (11 files), every line; `families.rs` and `lib.rs` at the head whole around every change. Line numbers at `430dde3`.
- **`cr_lf` (`families.rs:159-166`)**: ONE backward pass, `cr_lf[i] = true` for `\n`, `= cr_lf[i+1]` for `\r`, blank (0x20) and tab, `false` for every other byte (VT, FF, U+0085, U+2028 included). **`line_term(b, cr_lf, i)` (`:124-140`)**: `\n` → 1; `\r` → 1 only when `cr_lf[i+1]` is false, i.e. when the bytes after it, past `\r`/blank/tab, do not reach a `\n`; U+0085, U+2028 unchanged. So exactly the brief's rule with R-1's run (CR, blank, tab). `gle`, `gls` and `gline_next` all call the same `line_term` (`:168-189`, `:213-215`): one definition of a line end. A `\r` that is no longer a line end leaves the trailing `\r`/blanks/tabs inside the line before the `\n`; the two line shapes trim them: `Base64Lines` trims blank, tab and `\r` from the line end (`:934`), the `.netrc` "alone on its line" test skips blank, tab and `\r` after the value (`:792`), and the `machine` line test (`LineHas::general`) only sees a line longer by bytes that hold no word. PEM keeps its `\n` window (untouched).
- **Views (`lib.rs:241-275`)**: view 1 raw; `has_format` → view 2 = `stripped(text, true, false)`; if the current view (view 2, or the raw text when there is no format character) holds `ESC [` → view 3 = codes removed from it; if `has_format` and the RAW text holds `ESC [` → view 4 = `stripped(text, true, true)`, byte for byte main's one-pass `stripped_view`. Largest count per family over the views (`keep_largest`, the same `b.count > a.count` as main). **Main's view is always among the head's views**: format and `ESC [` → view 4; format only → main's view removes no code (no `ESC [` in the raw bytes) = view 2; `ESC [` only → main's view removes no format character = view 3. So the head can never name fewer families, or a lower count, than main because of the views (REASONED from the code; TESTED in §4: 0 losses).
- **`stripped(text, drop_format, drop_codes)` (`:184-216`)**: main's loop with two switches; `ansi_kept` sits in the code test (`:190-193`), so it now switches off code removal in views 3 and 4 (and in the red branch).
- **Item 3 (`families.rs:606-722`)**: the start test is main's `i == 0 || flag_may_start_after(b[i-1])` with `|| (forms && after_json_escape(b, i))` added (`:645`): a superset. The name walk, `spaced`, both spaced pushes and the htpasswd / `-p` branches are main's code (the only edit is `name == b"-u" || name == b"--user"` named `user`). The argv form (`:661-680`) and `--user=` form (`:683-692`) only push; they never change `e` or `i`. The one new skip: a start after a JSON escape is followed by `i = e.max(i + 1)` (`:720`), and on a `-p` glued value on a `mysql` line `e = e.max(ve)` (`:711`) can jump over bytes where main would have started a flag; but that branch has just pushed a `PasswordArgument` match itself, and main's own pushes inside a glued value (no blank in it) are impossible except another glued `-p`, so the family can never be lost by it (TESTED §5: 0 lower counts). **No start or spaced value main accepts is changed.** `argv_value_quote` (`:615-634`) walks blanks/tabs, one comma, blanks/tabs, a quote: each walk stops at the next non-blank, so the walks of different flags do not overlap (linear; TESTED §6).
- **Red branches**: three new `cfg!(coagent_scanner_red = …)` sites (`families.rs:131`, `:641`, `lib.rs:251`), names appended in `build.rs`. `cfg!` is the constant `false` unless rustc gets `--cfg coagent_scanner_red=…`, which only `build.rs` emits after its release refusal (TESTED §9). `cr_run_split` restores main's `\r` arm exactly; `one_stripped_view` restores main's condition and main's one view exactly; `argv_space_only` sets `forms = false`, which removes exactly (a) to (c).
- **`t07_pure` item 4**: `token_hits` tokenises the whole file (identifiers, `::`, any other non-blank character alone), reports `as` after `std`/`core`/`alloc`, and `::` + root when the token before `::` is not an identifier; called after main's per-line rules (`hits` unchanged above it). Gaps I found by reading and then TESTED (§8): a comment between the root and `as` (`use std /* c */ as s;`) and a path written with blanks around `::` (`std :: env :: var`) are found by neither rule (Note N-3).

## 3. The builder's own statements, judged — READ + TESTED
| # | Builder's statement (STATUS) | Friday's answer | My check | Judgement |
|---|---|---|---|---|
| 1 | FR-2: 93 family losses (27 whole texts), all item 2 (dropping main's one-pass view); main's view kept as a FOURTH view | accept, if the check reproduces the losses on a three-view copy and shows each recovered at the head by view 4 alone | TESTED (§4): r2_3v against main, seed `…d003`: **93 family losses, 27 whole texts**, same per-family split; **all 93 named at the head**, which differs from r2_3v only by view 4. First generator: 0 | **Condition met. Accept.** |
| 2 | t05: `\r` × 64 KiB is the existing row; `\r` × 64 Ki then `\n` would be 65 537 bytes, built as `\r` × (64 Ki − 1) then `\n` | accept, if the existing row is confirmed and the built row is scanned | TESTED (§6): `"lone CR only"` = `"\r".repeat(m)` (`t05_bounds.rs:174`); the built row is 65 536 bytes and `scan` → `Clean` (not TooLarge); the 65 537-byte form → TooLarge | **Condition met. Accept.** |
| 3 | item 4: the sixth planted line (`::std::env::var`) is already caught by main's rule; a control, not a red | accept | TESTED (§8): main's `hits` misses the first five and panics on `use ::std as s;`; the sixth is caught by main's word and path rules | **Accept.** |
| 4 | Open (1): `Finding`'s doc comment (`lib.rs:100-101`) is inexact; left as at main | accept as left; BACKLOG later | TESTED (§1): lines 1-179 identical to main | **Accept** (Note N-4 only records it). |
| 5 | FR-6: `a\\n--password x` → head PasswordArgument, main Clean: an over-flag, not a miss | accept, if the check reports how often the generators and corpora hit it | TESTED (§4, §5, §7): by hand PasswordArgument at head, Clean at main; **0 of 900 000 generated texts and 0 of 388 corpus sentences** hold the shape | **Condition met. Accept.** |
| 6 | the FR-2 class and the 1 939 rich-generator gains are generated constructions, not ordinary text | accept, if the check reads a sample of each gain class and says in plain words whether any looks like ordinary agent text | READ (§4 (c)): 6 samples of each of the 14 gain classes on each generator, plus the 27 FR-2 texts: hostile constructions with codes and invisibles inside tokens, N-R1 base64 lines, and `--user=` + colon | **Condition met: none looks like ordinary agent text. Accept.** |
| 7 | b0835a9 remainder: lf PasswordArgument = 263, all N-R3 (260 by a probe, 3 by hand) | accept, if the check attributes the 263 by its own method | TESTED (§4 (b)): own method (`b0835a9` with its netrc rule removed): **261 + 2 by hand = 263**, all N-R3 (the 2 also hold `htpasswd -B`) | **Condition met. Accept** (split differs by method, total equal). |
| 8 | `docs/M0-OUTCOMES.md` not touched; the `rand_core` warning pre-existing | accept both | TESTED: not in the name list (§1); root `Cargo.toml` blob-identical to main (§1, §8) | **Accept.** |
| 9 | a scratch file written to `/tmp`, moved | accept, no check | not checked (process only) | — |
Other figures of the STATUS re-made by me and equal: 28 tests (t10 3); 21 red rows; 0 losses over 450 000 texts and the gain tables; b0835a9 lines; qa_props reach line; qa_diff 3 / 8 / 0 and PasswordArgument scan-only 41 612; 0 rate change on 388 sentences; scope byte counts (0 / 28 356). One cosmetic difference: the builder counts 482 added lines for the name scan; `git diff -U0 f193620...430dde3 | grep '^+' | grep -v '^+++'` gives 490 here (0 word hits either way).

## 4. The two-head differentials (the heart) — TESTED
**Own harness** (`gate_scanner_notes_tests/qa_n_diff.rs`, built by `qa_tools/mkvars.sh`, release, 32.8 s): main `f193620` and `b0835a9` copied from git as scratch test modules (`lib.rs` → `mod.rs`, `use crate::` → `use super::` in `families.rs`, nothing else); the head is the library itself; one-item-reverted copies of the head, each differing from the head by exactly ONE line (counted by `diff`): **r1** (`cr_run_split` arm → `true`), **r2** (`one_stripped_view` → `true`), **r2_3v** (view 4's condition → `false`: the three views of FR-2's first state), **r3** (`forms = false`), **all3** (r1+r2+r3), **none** (the head copied unchanged: a control that the copy equals the library); for b0835a9 → head: **ansi** (`ansi_kept` test → `false`), **lf** (`line_end_lf_only` arm → `true`), **htp** (htpasswd letters lower-cased), **m3** (the r2 round's list additions removed), as the r2 check's `qa_r2_attr.rs`. A loss is attributed to the item whose revert brings the family back; a gain to the item whose revert removes it. Each text is compared by family AND count.

**(a) `f193620` against the head**
| Texts | Seed | Flagged main → head | Flagged at main, Clean at head | Families lost | Unattributed | all3 ≠ main (kinds+counts) | head copy ≠ library |
|---|---|---|---|---|---|---|---|
| 200 000, first check's generator | `0x0a5c0ffee5eed001` | 130 984 → 130 997 | **0** | **0** | **0** | **0** | 0 |
| 200 000, first check's generator, my seed | `0x5eed0a11c0de0b07` | 130 938 → 130 962 | **0** | **0** | **0** | **0** | 0 |
| 250 000, r2 check's rich generator | `0x0e2c0ffee5eed003` | 157 471 → 159 410 | **0** | **0** | **0** | **0** | 0 |
| 250 000, rich generator, my seed | `0x5eed0a11c0de0b08` | 157 251 → 159 159 | **0** | **0** | **0** | **0** | 0 |
| **900 000** | | | **0** | **0** | **0** | **0** | |
Result lines (verbatim): `DIFF gen: … WHOLE losses 0; WHOLE gains 13` · `DIFF gen: family losses by item {}; unattributed 0` · `DIFF rich: … WHOLE losses 0; WHOLE gains 1939` · `DIFF rich: family losses by item {}; unattributed 0` (and the same two lines, 0 and 0, for both of my seeds). **The head with all three items reverted gives exactly main's verdict, kinds and counts, on all 900 000 texts**, so nothing else about the scanner changed. The builder's figures (13 and 1 939 whole-text gains, 86 PasswordArgument family gains on the first generator, the 13-class gain table on the rich one) are reproduced exactly on the two seeds they used.

**(b) `b0835a9` against the head, rich generator** (`n_b_regressions`)
| Seed | `lf` Base64Lines class | `ansi` real-shape class (r2 check's `space_csi` method) | ansi artefacts | Remaining family losses by cause | Attributed to r1/r2/r3 or unattributed |
|---|---|---|---|---|---|
| `0x0e2c0ffee5eed003` (the r2 check's: 74 and 173 at `1096a77`) | **0** | **0** | 0 | htp 797, htp+m3 1, lf 261 (PasswordArgument), lf+htp 2, m3 128 (AuthHeader 27, AuthScheme 12, HexRun 40, KnownToken 19, PasswordArgument 8, SecretAssignment 22) | **0** |
| `0x5eed0a11c0de0b08` (mine) | **0** | **0** | 0 | htp 753, lf 235, lf+htp 3, m3 125 | **0** |
Whole texts lost (seed `…d003`): htp 308, lf 101 (PasswordArgument), m3 45: identical to the builder's line. **Both regressions are closed** and nothing remains outside `htp`, `m3` and the lf PasswordArgument class.

**The lf PasswordArgument class is N-R3, by my own method** (Friday's condition (7)): a copy of `b0835a9` with its `.netrc` rule removed (one line, `qa_old_nonetrc`). Seed `…d003`: of the 263 lf PasswordArgument family losses, **261: `b0835a9` without its netrc rule no longer names PasswordArgument**, so the old flag came from the netrc rule alone; **2 others** are the two `lf+htp` texts: each also holds an `htpasswd -B` line (which `b0835a9` flagged through its lower-cased letters, so removing the netrc rule leaves the family), and READ by hand each has a `machine … login …` line split from `password <value>` by U+2028 = the N-R3 shape. My seed: 235 + 3, the same two kinds. **263 = N-R3 (261 by probe + 2 by hand)**; the builder's split was 260 + 3 by a different probe; the total agrees.

**(c) Gains, per item and family** (seed `…d001` / `…d003`; my seeds alike)
- First generator: 13 whole texts, 86 PasswordArgument family gains, **all r3**, all form (b): `--user=` + a value holding a colon (my seed: 24 texts, 100 family gains, same class).
- Rich generator: 1 939 whole texts (r2 1 717, r1 210, r1+r2 10, mixed 2); family gains: r2 AuthHeader 595, AuthScheme 525, HexRun 630, KnownToken 478, LongToken 1 701, PasswordArgument 598, PrivateKey 215, SecretAssignment 607, UrlCredentials 72, Base64Lines 177; r1 Base64Lines 534; r1+r2 Base64Lines 25; combined Base64Lines 1.

**Friday's condition (1), FR-2 (`n_fr2_three_views`)**: the three-view copy (r2_3v) against main, seed `…d003`: **93 family losses in 27 whole texts** (AuthHeader 5, AuthScheme 5, HexRun 32, KnownToken 9, LongToken 25, PasswordArgument 3, PrivateKey 1, SecretAssignment 13): the builder's figures exactly. **All 93 are named by the head**, and the head differs from r2_3v only by view 4, so each is recovered by view 4 alone. First generator: 0 losses for the three-view copy. Accepted, condition met.

**Friday's condition (6), the gains read by me** (6 samples of each of the 14 gain classes per generator, 84 + 6 texts, read in my work-dir log): the r2 gains are shapes rejoined across an `ESC [` code that holds or touches an invisible character, many with several codes and invisibles in one token; the r1 gains are short base64 lines joined by `\r\r\n`, `\r\r\r\n`, `\r\t\n`, `\r \r\n`, i.e. the N-R1 shape coming back; the first generator's r3 gains are `--user=` followed by a value with a colon (some with an empty part, such as a bare colon). **In plain words: none of them looks like ordinary agent text; each is a generated construction or a credential shape.** The r3 class is the ruled form (b), whose everyday form (`--user=root:wheel`) is pinned in t03.

**FR-6 frequency** (Friday's condition (5)): an escaped backslash before `n`/`t`/`r` and a `-` occurs in **0** of the 900 000 generated texts and in **0** of the 388 corpus sentences (§7); so it caused 0 of the gains here. By hand it does flag (a JSON string holding `a`, an escaped backslash, `n`, then `--password hunter22` → PasswordArgument, main Clean), as the builder reports; an over-flag, not a miss.

## 5. No new miss from the new forms and views — TESTED
`gate_scanner_notes_tests/qa_n_cases.rs` (release). Every text compared main → head: every family main names must be named by the head, and the head's PasswordArgument count must not be lower.
| Cases | Texts | Family named at main and not at head | PasswordArgument count lower at head |
|---|---|---|---|
| **Every start main's rule accepts** (all 66 ASCII bytes that are not a letter, digit, `-`, `_`, `.`, `/`, plus é, 東, 🙂, NBSP, U+0085, U+2028, U+2029, ideographic space, ZWSP, U+180B, U+2065, fullwidth paren, two colour codes, CRLF, `ESC [` ZWSP `0m`) × the 10 shapes of `t09::m1_password_flags_wrapped` × 2 values × 10 new-form prefixes × 8 new-form suffixes (argv elements, `--user=a:b`, written `\n`/`\t`/`\\n` escapes, `", "`, `-u=a:b,`), plus the start alone; and 5 flags × 10 spaced values (quoted, with commas, tabs, two blanks, `-x`, `;`) × 5 wrappings | 126 610 | **0** | **0** |
| 47 rows of argv arrays (odd quoting, commas, tabs, newline after the comma, tuples, empty, `-x`, unclosed, mismatched quotes, double comma, `-u` with and without colon, JSON-escaped quotes), `--user=`/`-u=` (colon or not, quoted, upper case, blank after `=`, empty, bare colon, URL, glued after a word, curl), JSON escapes before and after a flag (`\n`, `\t`, `\r`, `\\n`, `\u000a`, `\b`, before `-p` on a mysql line, a glued `-p` swallowing a flag), a Windows path `\n-` | 47 | **0** | **0** |
| **Line ends, exhaustive**: `x<sep>y` for every separator of 1-6 units over {`\r`, `\n`, blank, tab, U+0085, U+2028, `a`} (137 256 texts), line-end sets of main and head compared through a probe appended to scratch copies | 137 256 | — | — |
| Three base64 lines and four `.netrc` forms joined by every such separator of up to 4 units (no `a`), plain and behind `> `, with and without a final separator | 31 080 | **0** | **0** |
| 10 made-up shapes (one per family) × every character boundary × 12 code/invisible inserts (`ESC[0m`; ZWSP inside, before, after the code; between ESC and `[`; inside the parameters; U+180B and BOM in the parameters; an unfinished `ESC [`; LRI/PDI around a code) × 3 leads | 12 996 | **0** | **0** |
- **Line ends** (`LINEENDS` line): main's line ends not at the head: **6 546, every one a `\r` whose run of `\r`/blank/tab ends in `\n`; 0 other**; line ends at the head not at main: **0**. So the only change is the ruled one, and no new line end exists.
- **Codes and invisibles**: own family not named: main 4 096, head 2 168 of 12 996. With an invisible inside or next to the code, the head now misses exactly as often as with the plain code and no invisible (e.g. hex: 21 of 63 with `ESC[0m`, with `ESC[3`ZWSP`2m`, with ESC ZWSP `[0m`; main 21 / 53 / 53): what remains is the plain-code class (a code glued inside a short shape behind a letter, an unfinished `ESC [`), the same at both heads.
- **What the forms do and do not catch** (the 47 rows): flagged now, Clean at main: argv with `"` or `'` or mixed quotes, with or without blanks/tabs around the comma, tuples, a value with a blank, an unclosed value, `-u`/`--user` with a colon; `--user=`/`-u=`/`-U=`/`--USER=` with a colon, quoted or not, in backticks, after `curl`; a flag after a written `\n`, `\t`, `\r`, `\\n`; a Windows path `C:\tools\n-u qa:x`. **Still Clean at both heads** (not new misses; the ruled wording does not reach them): an argv array pretty-printed with a NEWLINE after the comma (`["--password",` newline `"x"]`), shell words without a comma (`'--password' 'x'`), `["mysql", "-p", "x"]`, argv inside a JSON string with escaped quotes (`\"--password\", \"x\"`), a double comma, an empty or `-x` value, `--user= a:b` (blank after `=`), `x--user=a:b` glued to a word, a `\u000a` or `\b` escape before a flag. See Note N-1.

## 6. Linear time — TESTED
- **t05 in my debug build** (`cargo test --locked -p coagent-scanner --test t05_bounds -- --nocapture --test-threads 1`, smallest of five): 38 rows, **all under 150 ms; worst 67.91 ms** (`ESC [` ZWSP, a code in a name, repeated); the 7 new rows 18.99 / 19.08 / 41.35 / 66.42 / 67.91 / 23.31 / 26.74 ms (builder 19.08 / 19.13 / 41.73 / 67.37 / 69.00 / 23.67 / 26.83). `2 passed`.
- **Friday's condition (2)**: the existing row `"lone CR only"` is `"\r".repeat(m)` (`t05_bounds.rs:174`); the built row `\r` × (64 Ki − 1) then `\n` is exactly 65 536 bytes and `scan` answers **`Clean`** (scanned, not TooLarge); `\r` × 64 Ki then `\n` is 65 537 bytes → `TooLarge`. Accepted, condition met.
- **My own shapes** (`qa_n_time.rs`, 25 shapes, smallest of five, 8 KiB and 64 KiB; each 64 KiB text checked not TooLarge):

| Shape (new rule it hits) | debug 64K ms | ratio debug | release 64K ms | ratio release |
|---|---|---|---|---|
| CR × (n−1) then LF (one CR run) | 18.65 | 7.85 | 2.46 | 7.94 |
| CR × n, no LF | 20.42 | 8.08 | 2.52 | 7.98 |
| CR/blank/tab run, LF at the very end | 18.40 | 7.92 | 2.46 | 7.96 |
| CR/blank/tab run, a letter at the very end | 19.16 | 8.01 | 2.45 | 7.95 |
| `\r \r\n` repeated | 18.76 | 7.85 | 2.35 | 8.05 |
| base64 line + `\r\r\n` repeated | 20.55 | 7.88 | 2.87 | 8.09 |
| netrc `password x` + `\r \r\n` repeated | 21.21 | 7.88 | 3.14 | 7.84 |
| `machine` + `\r\t\r\n` + password repeated | 22.56 | 7.84 | 3.20 | 7.70 |
| argv flag then one 64 KiB blank run | 18.15 | 8.13 | 2.48 | 7.91 |
| argv flag, blanks, comma, repeated | 22.61 | 7.86 | 3.26 | 7.79 |
| argv value quote left open, repeated | 23.54 | 7.87 | 3.45 | 8.02 |
| argv pairs, mixed quotes | 23.43 | 8.02 | 3.40 | 8.11 |
| argv `-u` pairs | 24.86 | 7.89 | 3.20 | 7.84 |
| JSON escape then flag | 26.95 | 7.95 | 4.10 | 7.96 |
| JSON escape then a dash | 27.02 | 7.91 | 3.33 | 8.16 |
| escaped backslash, `n`, `-u=a:b` | 26.91 | 7.76 | 3.54 | 7.95 |
| mysql, then JSON escape + glued `-p` repeated | 23.87 | 8.26 | 3.51 | 7.93 |
| `--user=a:b` repeated | 29.91 | 8.18 | 4.37 | 7.80 |
| `-u=` then one 64 KiB value of colons | 32.00 | 8.00 | 3.80 | 7.64 |
| ZWSP `ESC [` repeated (views 2-4) | 40.85 | 7.90 | 5.26 | 8.13 |
| ESC ZWSP `[0m` repeated | 33.08 | 7.90 | 4.45 | 7.94 |
| `ESC [` ZWSP `0m` + 4 letters repeated | 59.09 | 8.18 | 8.59 | 7.82 |
| LRI, colour, hex, reset repeated | 55.74 | 8.02 | 7.64 | 8.16 |
| `ESC [` ZWSP then one long parameter run | **78.96** | 8.03 | **10.43** | 7.84 |
| `ESC [` with ZWSP after every parameter byte | 36.09 | 7.73 | 4.99 | 7.85 |
**Worst 78.96 ms debug, 10.43 ms release; every ratio 7.6-8.3.** Linear. (The counter read 1 other seat's heavy job during these runs; numbers are upper bounds.)

## 7. Over-flags, main against the head — TESTED (for the owner's card)
`qa_n_cases.rs::s7_overflag_corpora`, every sentence, verdict compared by kinds AND counts:
| Corpus | Sentences | Flagged at main | Flagged at head | Newly flagged | No longer flagged | Verdict changed at all |
|---|---|---|---|---|---|---|
| first check's plain agent chat (`qa_docs.rs` EVERYDAY) | 228 | 6 (2.6 %) | 6 (2.6 %) | **none** | none | none |
| first check's technical report lines (TECHNICAL) | 60 | 17 (28.3 %) | 17 (28.3 %) | **none** | none | none |
| r2 check's 100 flag sentences (`qa_r2_flags_corpus.rs`) | 100 | 33 (33.0 %) | 33 (33.0 %) | **none** | none | none |
**In plain words: this lane moves no rate.** Not one of the 388 sentences changes its verdict, family or count. The builder's statement is confirmed.

The new over-flag classes the lane pinned in `t03`, one sentence each (TESTED by the t03 pins passing in §9 and by my rows in §5):
- **Argv arrays:** a command written as a list of quoted words now flags when a word is an option whose name holds key, token, auth, session, secret, pass or similar and the next word follows after a comma (`["--key-file", "id_rsa"]`, `"--auth-mode", "login"`), and `["-u", "1000:1000"]`.
- **`-u`/`--user` with a colon after `=`:** a user and group written with an equals sign now flags (`docker run -u=1000:1000 alpine`, `--user=root:wheel`), even a bare colon (`--user=:`).
- **A JSON escape before a sensitive flag:** a command inside a JSON string, where a written `\n`, `\t` or `\r` sits right before such an option, now flags (`{"cmd": "make\n--token-file t.txt"}`), also after an escaped backslash (FR-6).

## 8. Unchanged invariants — TESTED
- **Alone:** `cargo tree --locked -p coagent-scanner -e all` (pristine second clone at `430dde3`) → `coagent-scanner v0.0.1 (…)` alone; `-i coagent-scanner -e all` → only `coagent-scanner feature "default" (command-line)`. Crate `Cargo.toml`, root `Cargo.toml`, `Cargo.lock` blob-identical to main (§1). **No new dependency of any kind.**
- **Pure:** my grep of `src/` for `std::`, `core::`, `alloc::`, `unsafe`, `static mut`, `include!`, `#[path`, print macros, `use ` → only `use crate::{Kind, VERDICT_FAMILIES};` (`families.rs:13`) and `#![forbid(unsafe_code)]`. `t07_pure` green (§9).
- **`t07`'s new token rule is red on main's `hits` (by hand):** scratch test `qa_t07_main.rs` = main's `t07_pure.rs` (`git show f193620:`) with ONLY the head's six new planted lines added after main's `:142` (diff kept as `qa_t07_main.diff`, 7 added lines), run against the head's `src/` → exit 101, first panic: `panicked at crates/coagent-scanner/tests/qa_t07_main.rs:151:9: control: the planted line "use ::std as s;" was not found`. The head's own `t07` passes on the same six lines (§9). The sixth (`::std::env::var`) is caught by main's word and path rules, as the builder says: Friday's answer (3) accepted.
- **My probe of the head's `hits`** (`qa_t07_head_probe.rs`, 17 spellings, each as line 2 of a two-line file): found: `use r#std as s;`, `extern crate std as s;`, `use ::{std as s};`, `pub use std as s;`, `use self::std as s;`, `use\tstd\tas\ts;`, `use std::{self as s};`, `use core::{self};`, `::core::mem::…`, `::alloc::string::String`, `std::env ::var`. **Not found:** `use std /* c */ as s;`, `use std // c` + newline + `as s;`, and `std :: env :: var("X")` (blanks around `::`). None of these is in `src/` today (grep above). → Note N-3.
- **No byte of the input in a verdict:** `lib.rs` lines 1-179 identical to main (§1), so `Finding` (fields `kind`, `count` only outside a red build), `Verdict`, `Kind`, `text()` are untouched; `t04_display` green (§9); `qa_props` rebuilds `Debug` from (kind, count) and compares it exactly for all 300 000 cases (below).
- **Size bound first:** `lib.rs:229-232`, `if text.len() > MAX_SCAN_BYTES { return Verdict::Flagged(vec![finding(Kind::TooLarge, 1, None)]); }` is the first statement of `scan` (READ); `t05_bounds::size_bound_is_checked_first` green.
- **No panic, deterministic** (first check's `qa_props.rs`, unchanged, release, at `430dde3`): `qa_props: seed 0x51c0de0000000002, 300000 cases, no panic, deterministic, Debug == kinds+counts for all` · `reach [89622, 83314, 80047, 78791, 137703, 87488, 75315, 110721, 45941, 4407, 484, 97118]` (the builder's line exactly) · largest count 10 878 · its 36 hostile shapes worst 8.42 ms release · `4 passed`, 114.3 s.
- **Base differential** (first check's `qa_diff.rs` + `qa/`, unchanged, release): `qa_diff: seed 0xa5c0ffee5eed001, 400000 texts; base redactor masks something in 249573; scan Clean in 138208` · **`texts the base masks and scan calls Clean: 3`** · per family as the r2 check except PasswordArgument scan-only 41 439 → **41 612** (the added forms) and Clean 138 241 → 138 208 · **`family misses explained only by the strip-list difference: 8; misses where the base rule matches a scanner view: 0`**. **3 / 8 / 0 as required.**
- **fmt and clippy** (pristine clone): `cargo fmt --all --check` → exit 0, no output; `cargo clippy -p coagent-scanner --all-targets --locked -- -D warnings` → exit 0; its one warning, `unused workspace dependency rand_core`, comes from root `Cargo.toml`, blob-identical to main: pre-existing (Friday's answer (8) accepted).

## 9. The reds and the tests — TESTED
- **`cargo test -p coagent-scanner --locked`** (debug, pristine second clone, own target dir): t01 10, t02 1, t03 2, t04 1, t05 2, t06 1, t07 1, t08 1, t09 6, **t10 3** → **28 passed, 0 failed** (25 at main + the 3 of t10).
- **`bash scripts/red-controls-scanner.sh`, once**, started exactly so (Python `subprocess`, `cwd` = the pristine clone's root, own `COAGENT_TOOLS`, target, log and scratch dirs), 10:01:03-10:02:37, other seats' heavy jobs before it: 2. Exit 0:
  ```
  names: 21 red controls, each in build.rs, used under src/ and a row
  no_pem … no_base64_lines   P1  RED  (each: t01 exactly its own test failed; evidence as at main)
  flag_everything P2 · reason_echoes_text P3 · prefix_window P4 · quadratic_line_end P5 (345 ms - 1.13 s) · slice_mid_char P6   RED
  flag_after_space_only M1 · line_end_lf_only m1 · ansi_kept m2   RED (evidence as at main)
  cr_run_split      N-R1 RED  t10_notes::r1_cr_runs     evidence: N-R1: base64 lines split by a CR run were missed: [16 made-up cases …]
  one_stripped_view N-R2 RED  t10_notes::r2_three_views evidence: … missed: ["RE-1 …", "RE-3 …", "PEM …", "an invisible inside the code", "an invisible between ESC and ["]
  argv_space_only   N-R5 RED  t10_notes::r5_flag_forms  evidence: N-R5: a password flag form was not seen (96 of 96): …
  rows: 21 cfg rows
  planted std::env  P7   RED  t07_pure::the_scanner_reads_nothing (scratch copy 10bfc5)  evidence: ["lib.rs:307: std::env", "lib.rs:307: std:: path"]
  GREEN: 28 tests ok
  RED CONTROLS OK: every guard went red under its control, on its property, and green without
  ```
- **Each new control against the WHOLE `t10_notes`** (debug, red-control marker present in each build): `cr_run_split` → only `r1_cr_runs` fails (`t10_notes.rs:38`, the N-R1 assertion); `one_stripped_view` → only `r2_three_views` (`:106`; the 5 non-FR-2 cases; the two FR-2 cases pass, since main's view finds them); `argv_space_only` → only `r5_flag_forms` (`:159`, 96 of 96). Also: `ansi_kept` → only `r2_three_views` (4 cases: the two invisible-in-code and the two FR-2 cases), and it still turns `t09::m2_ansi_codes` red (script row); `line_end_lf_only` → only `r1_cr_runs` (its lone-CR control at `:50`). **Each row is red for its own reason.**
- **Release refuses** (own target dir): `COAGENT_SCANNER_RED=<cr_run_split | one_stripped_view | argv_space_only> cargo build --release -p coagent-scanner` → exit 101 each, "COAGENT_SCANNER_RED is for test builds only"; release without the variable → exit 0, no marker. With §2 (READ: `cfg!` constant false without `--cfg`), **no red branch is reachable in a normal build.**
- **No existing assertion changed** (§1: 0 removed lines in every existing test file and the script; t01, t02, t04, t06, t09, `tests/common` blob-identical).

## 10. Docs — READ
`docs/SCANNER.md` at `430dde3`, every changed paragraph and row against the code:
- **§2 PasswordArgument row**: forms (a), (b), (c) as built. (a) says "then `,`"; the code also allows blanks and tabs around the comma (shown by its own example `"-u", "user:pass"`), and needs a sensitive name with a value not starting `-`, or `-u`/`--user` with a colon, as the spaced rule. Accurate.
- **§2 format paragraph**: the four views, when each runs, "a family flags if any view matched, and its count is the largest": matches `lib.rs:241-275`. "(3) view 2 without terminal control sequences, when view 2 holds `ESC [`" reads correctly once view 2 of a text without format characters is the text itself (the code uses the raw text there).
- **§2 lines paragraph**: "A run of carriage returns, blanks and tabs that ends in `\n` is ONE line end … A `\r` before anything else still ends a line": matches `cr_lf`/`line_term` and my exhaustive line-end test (§5).
- **§3**: the 7 timing rows (mine within 1.1 ms of each, §6); the t07 bullet: true for the forms it names; it does not claim comments or spaced `::` (N-3).
- **§4**: the FR-3 bullet (N-R3) and the FR-4 (c) bullet (U+2029, VT, FF, U+009B), each pinned in `t03::KNOWN_MISSES` (green, §9) and FR-4 (c) in the appended BACKLOG entry; the "SCANNER-NOTES covers" sentence is true (§5). **Not listed:** the argv and escape forms the ruled wording does not reach (§5 last bullet) → Note N-1.
- **§5**: the FR-5 widened M1 row, the N-R5 row, the FR-4 (a) and (b) rows: each example is a `KNOWN_OVERFLAGS` pin (green). **§7**: three rows, one per new red name, each naming its own test: matches `build.rs` and the script's rows.
- `Finding`'s doc comment (`lib.rs:100-101`, "in the raw text or in the text with invisible format characters removed") is inexact since codes and four views; left as at main because Finding is untouched (lines 1-179 identical, §1). Friday's answer (4) accepted; a doc line for a later lane.

## 11. Names and ids — TESTED
Tool outside the repo (`/private/tmp/claude-501/qsn/qa_tools/namescan.py`, the first check's tool unchanged), `python3 -B -I`, 24 words on the command line only (owner name parts and handle, the login name, short and full host name and home path read at run time, mail domains, workspace drive and folder names, coordinator and client names, `/Users/`, `/Volumes/`, `/private/tmp`, the temp user folder, the mail service, the deploy-key file name), 42 spellings.
- **The 490 lines the lane adds** (`git diff -U0 f193620...430dde3`, `+` lines) and `t10_notes.rs` whole: `scanned 2 files, 42 spellings of 24 words: 0 word hits`; 0 `ID`, 0 `KEY?`.
- **The 11 changed files whole:** 51 word hits, **all in `BACKLOG.md` lines 241-1402, main's own text** (the lane's entry is lines 1454-1458, after main's 1 453); `ID` ×4 = the two made-up UUIDs (`deadbeef-0001-…`, `deadbeef-0002-…`) in pre-existing lines of t03 and the docs.
- **Positive controls:** a scratch copy of `t10_notes.rs` with one planted line (login name + host name) and a planted binary (NUL, `BIN`, the home path, NUL, 0xFF, a `toolu_` id): `scanned 2 files … 13 word hits` (7 in the copy, 6 in the binary) + the `toolu_` id. Both found.
- **Nothing of the owner's** in what the lane adds.

## Every loss and gain class of item 4
| Class | Count (seed `…d001` gen / `…d003` rich; my seeds alike) | Item | My judgement |
|---|---|---|---|
| **Loss**, main → head, any family | **0** / **0** (my seeds 0 / 0) | — | nothing flagged at main is lost; the all-reverted copy equals main on kinds and counts for every text |
| Loss, three-view copy → main (FR-2's first state) | 0 / 93 families, 27 texts | item 2 without view 4 | closed by view 4 (ruling R-2); each of the 93 recovered by view 4 alone |
| Gain PasswordArgument | 86 / — (whole 13) | r3, form (b) | `--user=` + a value with a colon: the ruled form; everyday form pinned |
| Gain Base64Lines | — / 534 (+25 r1+r2, +1 combined) | r1 | N-R1 shape coming back (short base64 lines joined by a CR run ending in LF): right |
| Gain Base64Lines | — / 177 | r2 | base64 lines rejoined across a code that holds or touches an invisible: right or a joining artefact (N-R4 (b) class) |
| Gain AuthHeader, AuthScheme, HexRun, KnownToken, LongToken, PasswordArgument, PrivateKey, SecretAssignment, UrlCredentials | — / 595, 525, 630, 478, 1 701, 598, 215, 607, 72 | r2 | shapes seen again once the invisible inside or next to a code goes first (the N-R2 class) plus joins across removed codes (N-R4 (b), recorded by FR-4); generated constructions, none ordinary text |
| Loss, b0835a9 → head: lf Base64Lines | — / **0** (was 74) | — | N-R1 closed |
| Loss, b0835a9 → head: ansi real shape | — / **0** (was 173); artefacts 0 | — | N-R2 closed |
| Loss, b0835a9 → head: htp | — / 797 (+1 htp+m3) | r2 round item 5 | ruled (`htpasswd -B` takes no password) |
| Loss, b0835a9 → head: m3 | — / 128 | r2 round item 4 | artefacts (the r2 check's class) |
| Loss, b0835a9 → head: lf PasswordArgument | — / 263 (+2 lf+htp) | r2 round item 2 | N-R3 (FR-3, record only): 261 by my netrc probe, 2 read by hand |

## Findings
**No Blocker. No Major.** Repro files are in `gate_scanner_notes_tests/`. To run one: in a clone at `430dde3`, run `qa_tools/mkvars.sh <clone>` (it builds the scratch modules from git), copy the first check's `qa/` folder and the named files into `crates/coagent-scanner/tests/`, then run the command.

**N-1 (Minor): argv and escape forms the ruled wording does not reach are Clean, and docs §4 does not list them.** Not a new miss (Clean at main too); a realistic one left undocumented.
- File: `crates/coagent-scanner/src/families.rs:615-634` (`argv_value_quote`: only blanks and tabs around the comma), `:608-610` (`after_json_escape`: `\n`, `\t`, `\r` only); `docs/SCANNER.md` §4.
- What happens (made up): a pretty-printed argv array `["--password",` NEWLINE `"hunter22"]` (and with CRLF), shell words without a comma `'--password' 'hunter22'`, `["mysql", "-p", "hunter22"]`, an argv inside a JSON string with escaped quotes, `--user= qa:hunter22` (blank after `=`), a `\u000a` escape before a flag → Clean at both heads.
- Repro: `cargo test --locked -p coagent-scanner --release --test qa_n_cases -- --nocapture s5_forms_rows 2>&1 | grep "head \[\]"` → the rows named above (plus the ruled controls).
- Suggested fix: list them in docs §4 with `KNOWN_MISSES` pins now; a later lane (with its own two-head differential, as R-4 (c)) may let the argv look-ahead cross one line end.

**N-2 (Note, for the owner's card): the new forms' over-flags reach a little further than the pins show.** `--user=:` (a bare colon), `-U=qa:x` / `--USER=…` (upper-case flags are lower-cased, so `psql`-style `-U=` counts as `-u=`), and a Windows path whose folder starts with `n`, `t` or `r` before `-u a:b` (`C:\tools\n-u qa:x`) flag. All follow from the ruled rules; none occurs in the 388 corpus sentences. Suggest one docs §5 line.

**N-3 (Note, test strength, item 4): `t07`'s token rule misses a comment between the root and `as`, and a path with blanks around `::`.** `use std /* c */ as s;`, `use std // c` + newline + `as s;`, `std :: env :: var("X")` → no hit (`qa_t07_head_probe.rs`). Main's path rule misses the last one too; none is in `src/` today. Repro: `cargo test --locked -p coagent-scanner --test qa_t07_head_probe -- --nocapture 2>&1 | grep -- "-> \[\]"`. Suggested fix: drop `//` and `/* */` comments before tokenising, and treat `root` `::` (blanks allowed) as a path start.

**N-4 (Note):** `Finding`'s doc comment (`lib.rs:100-101`) still describes two views; left as at main by the brief (Friday records it for a later lane). The docs' view 3 wording assumes view 2 is the text itself when it holds no format character; true, but one clause would say it.

## What was NOT checked
| Not checked | Why / what would check it |
|---|---|
| `scripts/check.sh` whole (workspace fmt/clippy/test/deny) | the brief says not to (Friday's merge check runs it). I ran `cargo fmt --all --check`, the crate's clippy with `-D warnings`, the crate's 28 tests and the red script (all exit 0) |
| `qa_props` in debug | the brief asks for release; release 300 000 done. Debug timing covered by t05 and my 25 shapes |
| The builder's harness, logs and worktree (`tools/tmp/scn/5e2a7e`, `44ba1d`) | not touched by the brief's rule; I re-made every harness myself |
| Linux and Windows builds | macOS only; the lane adds no OS code. `\r\r\n` (N-R1) is the Windows-relevant case and is covered by tests |
| Real agent traffic | every corpus is made up (the first check's, the r2 check's, mine) |
| Mutation testing beyond the 21 rows and my one-item reverts | not asked |
| The red script's names check fed a deliberately mismatched name | read only; it passed with 21 names |
| Timing on an idle machine | 1-2 other heavy jobs during my runs; numbers are upper bounds |
| `9145840` merged into the lane | by the brief's rule Friday sends one merge-in addendum after this check; `9145840` changed the audit-host crate only (brief, not re-checked by me) |
| How SCANNER-WIRE will use the verdict | later lane |

## Process notes (QA seat)
- Work dir `/private/tmp/claude-501/qsn`: `clone/` (my QA files under `crates/coagent-scanner/tests/`, never committed), `clone_red/` (pristine at `430dde3`, for the red script, crate tests, fmt, clippy, tree), own target dirs (`target`, `target_red`, `target_ctl`) and cargo home (`tools/cargo` with `bin`, `rustup` linked to the project's toolchain). Network: `git fetch`/`ls-remote` from GitHub (deploy key) and `cargo fetch --locked` only. No model run.
- In the project repo I used only `git --no-optional-locks` read verbs (and `git clone` from it as a read). The only file written in the project folder is my STATUS file.
- Before each run over a minute I counted other seats' heavy jobs in `ps`: 1 (the differentials, timing), 2 (crate tests, red script). One heavy run of mine at a time.
- Copies of every script and test file I wrote, and my logs, are in `gate_scanner_notes_tests/` (the logs hold random made-up token-shaped strings from the generators; the name-scan planted controls and their log are NOT copied, because they hold the planted words).
