VERDICT: GO WITH NOTES — head dd70630dd74cd1dac9261f1ac83542514562c767

# QA-SCANNER-NEXT: independent check of branch `scanner-next`

Seat QA-SCANNER-NEXT, 2026-11-25. Brief: Friday's `briefs_drafts/2026-11-25_coagent_QA-SCANNER-NEXT_check_brief.md`, read whole. I did not make the lane. Read whole before anything else: the SCANNER-NOTES check's verdict (N-1 to N-4), the lane's brief (constraints, items 1-5, R-1 to R-8, R-12, R-13), the builder's STATUS (136 lines), and the diff `debbb44..dd70630` every line. Work dir `/private/tmp/claude-501/qsx` (own clone of the project repository, GitHub remote added and fetched with the deploy key; own cargo home whose `bin` and `rustup` are links to the project's toolchain, as `coagent_merge_check.sh` does; cargo 1.100.0, rustc 1.100.0; own empty target dirs). Every comparison by SHA. TESTED = I ran it; READ = I read it. Every secret-shaped string below is made up.

## BLUF
- **Does the scanner answer exactly as before?** Yes. No code byte under `src/` changed (two comment lines only, proved by program), and my old-against-new comparison of 1 257 714 texts (900 000 generated on the earlier checks' seeds and mine, 357 210 targeted flag forms of my own, every pin, every docs example) finds 0 differing in verdict, kind or count; a one-character planted change shows thousands.
- **Are the recorded misses and over-flags true?** Yes: the 7 new misses are Clean and the 3 over-flags flagged, at both commits. For the strictness decision: `--user=:` and the Windows-path form flag only as a password flag; the upper-case `-U=`/`--USER=` forms also flag as an upper-case name, so loosening the flag rule alone would not clear them. Do not make flags case-sensitive to fix them: `curl -U user:password` (a real proxy password) is caught only because flags are lower-cased.
- **Can the purity test still fail?** Yes. It finds everything it found before, plus the three new spellings, and each turns it red when planted in a real source file. It still misses a comment-split alias placed after a `/*` or `//` inside a string, and blanks rustc counts but the test does not (U+2028, U+200E, VT…), as before; and its new path rule is very slow on a hostile run of `std ::` (30 s for 115 KB). Notes only.
- **Not covered:** `check.sh` whole, fmt and clippy (Friday's merge check), Linux and Windows. Verdict GO WITH NOTES: six Notes, no Blocker, no Major.

## Proofs (section 0) — TESTED
- `git ls-remote gh scanner-next main` (GitHub remote, deploy key) → `dd70630dd74cd1dac9261f1ac83542514562c767 refs/heads/scanner-next` · `debbb4442fc90b1d5c1f04f123a665dcd8cf381f refs/heads/main`. Both equal the brief.
- `git rev-list --parents -n1 dd70630…` → `dd70630… debbb44…`: ONE parent, main. `git log --oneline debbb44..dd70630` → one commit (`dd70630 SCANNER-NEXT: record N-1 misses and N-2 over-flags, t07 sees two more spellings, Finding doc words`).
- Builder STATUS `coagent/5_Project_History/STATUS_SCANNER_NEXT.md`: 136 lines; last line `READY FOR QA SCANNER-NEXT`, the line above it `dd70630dd74cd1dac9261f1ac83542514562c767`. Matches. Nothing differs: no stop.

## 1. Head, base, scope — TESTED
- `git diff --name-status debbb44 dd70630` → 5 paths, all `M`: `BACKLOG.md`, `crates/coagent-scanner/src/lib.rs`, `crates/coagent-scanner/tests/t03_known_overflag.rs`, `crates/coagent-scanner/tests/t07_pure.rs`, `docs/SCANNER.md`. `--summary`: no create, delete or mode change. `--shortstat`: 124 insertions, 3 deletions.
- `git diff --numstat` → `6 0 BACKLOG.md` · `2 2 …/src/lib.rs` · `36 0 …/tests/t03_known_overflag.rs` · `66 0 …/tests/t07_pure.rs` · **`14 1 docs/SCANNER.md`**.
- **The docs figure: Friday's numstat is right, the builder's STATUS §2 "+15 −2" is wrong.** The four docs hunks: §2 view (3) −1 +2 (one line rewrapped into two), §3 t07 bullet +3, §4 bullet +8, §5 row +1 = +14 −1. Nothing follows from it: the builder's §8 quotes of every docs change equal the diff word for word; only the count in its table is off (a STATUS miscount, no file affected). Note N-5 below records it.
- **Only `///` lines change under `src/`** (program `qa/doc_only.py`: every `+`/`-` line of `git diff debbb44 dd70630 -- crates/coagent-scanner/src`, trimmed, must start `///`) → `4 changed lines; 0 not ///`. Control: the same program fed `+    let x = 1;`, `-/// ok`, `+    ///indented doc`, `-//! inner` → `4 changed lines; 2 not ///: ['+    let x = 1;', '-//! inner']`. Second proof: `lib.rs` at both SHAs with every `///` line dropped → `cmp` identical (control: whole files differ).
- `git diff debbb44 dd70630 -- crates/coagent-scanner/src/families.rs | wc -c` → **0**; control: the same for `lib.rs` → 759.
- `build.rs`, the crate's `Cargo.toml`, `scripts/red-controls-scanner.sh`, root `Cargo.toml`, `Cargo.lock`, `docs/M0-OUTCOMES.md`: diff **0 bytes**; blob ids equal at both SHAs (`build.rs` `7e7c8132…`, crate `Cargo.toml` `2e5542eb…`, root `Cargo.toml` `5c0f3bc3…`, `Cargo.lock` `0094acf1…`, `families.rs` `61396848…`). Every path outside the five: `git diff … -- . ':!<the five>'` → **0 bytes**; control, the same with `BACKLOG.md` not excluded → 3 120.
- **Tree ids of every other crate equal** (12 crates: audit-host, audit, cli, crypto, daemon, hook, ipc, mcp, policy, proto, relay, roster: SAME at both SHAs); `scripts/`, `preview/`, `spikes/`, `tests/common` SAME; the scanner crate's tree differs (control). The other test files t01, t02, t04, t05, t06, t08, t09, t10: blobs SAME.
- `cargo tree --locked -p coagent-scanner -e all` (head) → `coagent-scanner v0.0.1 (…)` alone; `-i coagent-scanner -e all` → only `coagent-scanner feature "default" (command-line)`: nothing in the workspace depends on it. Control: `cargo tree -p coagent-daemon --depth 1` lists its path dependencies. **No new dependency.**
- `unsafe` in added lines: 0. `cfg!` in added lines: 0. Removed lines in `t03`, `t07`, `BACKLOG.md`: 0, 0, 0 (numstat above).
- Judgement: **scope clean.** The three removed lines are the two `///` lines of `Finding` and one docs line (§2 view (3), rewrapped; see item 5).

## 2. The scanner answers exactly as before (the heart) — TESTED
**Own harness** (`gate_scanner_next_tests/tests/qa_sx_diff.rs`, modules built by `qa/mkqa.sh`, release, 50.5 s, own empty target dir `target_diff`, log shows `Compiling coagent-scanner`): the base's `lib.rs` → `tests/qa_base/mod.rs` (`diff` against `git show debbb44:` empty) and `families.rs` with `use crate::` → `use super::` (1 line changed, counted by `diff`), beside the head, which is the library itself. Two controls built the same way from `dd70630`: **headcopy** (unchanged: must equal the library) and **headmut** (ONE character changed in a rule, `HEX_MIN` 16 → 15: must differ). Generators copied unchanged from the earlier checks' folders (`gen.rs` sha256 `dd585acc00f0c38f…`, `qa_r2_gen.rs` `6fbcf6574a4af199…`; first-generator texts as the earlier check, `gen::text(r, if i % 10 == 0 { 40 } else { 8 })`). Each text compared by verdict (`share_flagged`) AND kinds AND counts (`(format!("{:?}", kind), count)` per finding, in order).

| Texts | Source / seed | Flagged base → head | Differing in verdict, kinds or counts | headcopy ≠ head | headmut ≠ head |
|---|---|---|---|---|---|
| 200 000 | first generator, `0x0a5c0ffee5eed001` (earlier checks') | 130 997 → 130 997 | **0** | 0 | 4 493 |
| 200 000 | first generator, `0x95ca17e70a11d001` (mine) | 131 363 → 131 363 | **0** | 0 | 4 453 |
| 250 000 | rich generator, `0x0e2c0ffee5eed003` (earlier checks') | 159 410 → 159 410 | **0** | 0 | 4 813 |
| 250 000 | rich generator, `0x95ca17e70a11d003` (mine) | 158 872 → 158 872 | **0** | 0 | 4 872 |
| 357 210 | **my own targeted texts**: 15 flag spellings (`--password`, `-p`, `-P`, `--Password`, `--token`, `--api-key`, `--secret`, `--pass`, `-u`, `--user`, `-U`, `--USER`, `--User`, `-pw`, `--release`) × 14 joiners (blank, `=`, `= `, `", "`, `",` LF, `",` CRLF, `' '`, tab, `","`, `" , "`, escaped-quote comma, `',` LF `'`, `",` LF LF `"`, double comma) × 9 made-up values (`qa:qapw0001`, `qapw0001`, `:`, `x`, `1000:1000`, `-x`, empty, `qa:`, `:qapw0001`) × 21 prefixes (`[`, `["`, `mysql `, `["mysql", "`, JSON `\n` and `\u000a` before, `C:\tools\n`, `C:\run\t`, `C:\x\r`, `curl `, `psql `, an escaped backslash, backtick, paren, an argv inside a JSON string, a glued `x`, …) × 9 suffixes | 96 150 → 96 150 | **0** | — | — |
| 144 | every `t03` pin, base lists (53 + 14) and head lists (56 + 21) | 109 → 109 | **0** | 0 | 0 |
| 313 | **every backtick span of `docs/SCANNER.md`** at base and head (deduplicated; each also with `<ESC>` replaced by the ESC byte): includes the new §4 and §5 examples | 72 → 72 | **0** | 0 | 0 |
| 47 | the SCANNER-NOTES check's `s5_forms_rows` | 30 → 30 | **0** | 0 | 0 |
| **1 257 714** | | | **0** | **0** | |

Result lines (verbatim, log `logs/sx_diff.log`): `SXDIFF gen 0x0a5c0ffee5eed001 (earlier checks' seed): 200000 texts; flagged base 130997 -> head 130997; differing in verdict, kinds or counts: 0; controls: headcopy != head 0, headmut (HEX_MIN 16->15) != head 4493` · `SXDIFF targeted N-1/N-2 forms (mine): 357210 texts; flagged base 96150 -> head 96150; differing in verdict, kinds or counts: 0` · `PINS base overflags 53 misses 14; head overflags 56 misses 21` · `CONTROL headmut != head on 4453 of 200000 (mine seed)` · `test result: ok. 8 passed` (the 8 include the base `t03`'s and head `t03`'s two tests each, compiled into the harness against the head library: both green).
- **The planted control works:** the one-character rule change shows 4 453 to 4 872 differing texts per 200 000-250 000; the unchanged copy shows 0. So the harness can see a difference, and the head copy is the library.
- The builder's figures for the shared seeds (130 997, 159 410; 144 pins, 109 flagged; 47 rows, 30 flagged; pin list sizes 67 → 77) are reproduced exactly.
- Judgement: **the scanner answers exactly as at `debbb44`** — as it must, since no code byte under `src/` changed (§1); the differential confirms it on 1.26 M texts, 0 different.

## 3. The pins — TESTED
Own probe `gate_scanner_next_tests/tests/qa_sx_pins.rs` (debug, own target dir `target_pins`, `Compiling coagent-scanner` in the log): the base library (scratch module from `debbb44`) and the head library, each new pin taken from the two `t03` files themselves (the head list minus the base list), plus two copies of the head with the FLAG rule loosened, one line each (`qa/mkloose.sh`): **loose_case** (`-u`/`--user` tested on the bytes as written, so `-U`/`--USER` are not `user`) and **loose_b** (form (b), `--user=a:b`/`-u=a:b`, switched off).
- **Existing pins unchanged:** the base `KNOWN_OVERFLAGS` (53) and `KNOWN_MISSES` (14) are exact prefixes of the head lists (`assert_eq!` on the slices, green). New: **7 misses, 3 over-flags**, as the builder says.
- **Each of the 7 new misses is Clean at the base AND the head** (`base [] | head []` for every one): (i) `["--password",` LF `  "qapw0001"]`; (ii) the same with CRLF; (iii) `'--password' 'qapw0001'`; (iv) `["mysql", "-p", "qapw0001"]`; (v) `{"args": "[\"--password\", \"qapw0001\"]"}` (escaped quotes); (vi) `--user= qa:qapw0001`; (vii) `{"cmd": "a\u000a--password qapw0001"}`.
- **Each of the 3 new over-flags is flagged at the base AND the head, and by these families:**

| Pin | Base | Head | Flag rule case-sensitive | Form (b) off |
|---|---|---|---|---|
| `--user=:` | PasswordArgument 1 | PasswordArgument 1 | PasswordArgument 1 | **Clean** |
| `-U=qa:qapw0001` | SecretAssignment 1, PasswordArgument 1 | the same | **SecretAssignment 1** | **SecretAssignment 1** |
| `C:\tools\n-u qa:qapw0001` | PasswordArgument 1 | PasswordArgument 1 | PasswordArgument 1 | PasswordArgument 1 |

- **The builder's claim for the owner's card is CONFIRMED:** the upper-case forms also flag through SecretAssignment (`U`, `USER` are env-style upper-case names before `=`: `families.rs` `assignments` strips the leading dashes and `env_style` accepts an all-upper name), and with the flag rule loosened either way `-U=qa:qapw0001` stays flagged by SecretAssignment alone. `--USER=qa:x` at base and head: SecretAssignment 1, PasswordArgument 1 (variant table). **Refinement for the card:** a MIXED-case flag (`--User=1000:1000`) is flagged by PasswordArgument ONLY (not env-style), so a case-sensitive flag rule would clear it; the claim holds for all-upper names only, which is what the docs row says ("an upper-case `-U=` or `--USER=`"). `--user=:` is caused by form (b) alone; the Windows-path pin by form (c) (the `\n` read as an escape) with the old `-u user:pass` rule, so switching (b) off does not clear it.
- **Two variants of mine per form** (recorded, not graded; every one equal at base and head):

| Form | Variant | Base = head | Note |
|---|---|---|---|
| miss (i) | `["--token",` LF `  "qatk0002"]` · `["-u",` LF TAB `"qa:zz0002"]` | Clean · Clean | the miss is any flag, not only `--password` |
| miss (ii) | `["--secret",` CRLF `"qase0003"]` · `["--password",` CR `"qapw0002"]` (CR alone) | Clean · Clean | |
| miss (iii) | `"--token" "qatk0002"` · `'--password' qapw0002` (quoted flag, bare value) | Clean · Clean | control: `--password 'qapw0002'` (bare flag, quoted value) → PasswordArgument 2 |
| miss (iv) | `["mariadb", "-p", "qapw0002"]` · `["sshpass", "-p", "qapw0003", "ssh"]` | Clean · Clean | control: `["mysql", "-pqapw0002"]` (glued) → PasswordArgument 1 |
| miss (v) | escaped-quote argv with `--token` · with `-u` and `qa:zz0002` | Clean · Clean | |
| miss (vi) | `-u= qa:zz0002` · `--user=` TAB `qa:qapw0002` | Clean · Clean | |
| miss (vii) | `\u0009` before `--token qatk0002` · `\u000d` before `-u qa:zz0002` | **AuthScheme 1** · Clean | the first is flagged, but by AuthScheme (the word `token` then a value), not as a password flag: my variant's choice of flag, not a docs error |
| over (i) | `-u=:` · `--user=":"` | PasswordArgument 1 · PasswordArgument 1 | |
| over (ii) | `-U=root:wheel` · `psql -U=qa:zz0002 -h db` | SecretAssignment 1 + PasswordArgument 1 (both) | `--User=1000:1000` → PasswordArgument 1 only (above) |
| over (iii) | `C:\t-u root:wheel` · `D:\work\r--password qapw0002` | PasswordArgument 1 · PasswordArgument 1 | any sensitive flag, not only `-u a:b`; control: `C:\tools\nightly-u qa:x` → Clean (the letter must be followed directly by `-`) |

- The docs' own examples (the §4 bullet's seven with `x`, the §5 row's four) give exactly what the docs say: the seven Clean, `--user=:` PasswordArgument, `-U=qa:x` and `--USER=qa:x` SecretAssignment + PasswordArgument, `C:\tools\n-u qa:x` PasswordArgument (log `logs/sx_pins.log`).
- Judgement: **every pin is true.** No new miss is flagged and no new over-flag is Clean, at either SHA.

## 4. The purity test — READ + TESTED
**READ (head `t07_pure.rs`).** `hits` (`:61-101`): the per-line rules and the first `token_hits(text)` (`:94`) are byte for byte the base's (0 removed lines; base lines kept in order, checked by program); then a SECOND `token_hits` on `comments_blanked(text)`, each hit tagged ` (comments blanked)` (`:97-99`). **New third token rule** (`:190-201`): a root token (`std`/`core`/`alloc`) whose NEXT token is `::` → the path is joined from the following run of identifier and `::` tokens and `ALLOWED_PATHS` (empty) is applied with `starts_with`, as the line rule does; the hit is `"<l>: <root> :: path"`. It fires whatever precedes the root (so `x::std::y` is refused too: stricter, never weaker). **`comments_blanked`** (`:108-146`): byte walk; `//` → blanks to (not including) the next `\n`; `/*` → depth-counted walk, `/*` +1, `*/` −1, stop at depth 0, unclosed → to the end; every byte inside except `\n` → blank. It does not parse string, raw-string, byte-string or char literals (its doc comment says so for `//`). Panic and loop review: `out[i + 1]` is written only after `b.get(i + 1)` matched; `depth -= 1` happens only inside a comment entered with depth ≥ 1 and the walk breaks at 0, so no underflow; every branch advances `i`; the opener and closer bytes are ASCII and every byte between is blanked, so a multi-byte character is either kept whole or blanked whole, and the final `from_utf8(...).expect` cannot fail. Tokens: only `is_ascii_whitespace` separates (blank, tab, LF, FF, CR), and `::` is one token.

**TESTED, base `hits` against head `hits`** (`gate_scanner_next_tests/tests/qa_sx_t07.rs`, debug, own target dir `target_t07probe`; the two `t07_pure.rs` files copied from git with only `fn hits` made `pub` and the test renamed). 122 texts: the SCANNER-NOTES check's 17 probe spellings (wrapped as its probe did, `//! x\n<spelling>\n`) and **35 spellings of mine × 3 placements** (wrapped; at the very start of the file; at the very end, no trailing LF). Result line: `T07SUM 122 texts; base hits the head lacks: 0`.
- **Every hit of the base is a hit of the head** (compared as multisets of hit strings): 0 lacking.
- The check's 17: base finds 12, head finds **15**; the three new are exactly item 3's spellings (`use std /* c */ as s;`, `use std // c` + LF + `as s;`, `std :: env :: var`); still found by neither: `use crate::x as std;` and `macro_rules! m { () => { std } }` (no root before `as` or `::`; not a use of std).
- Mine: base finds 9 of 105, head 66. The per-spelling table is below ("Every probe spelling").
- **The real `src/`** (`t07_real_src`): `lib.rs` and `families.rs` at the head → base hits `[]`, head hits `[]` (both runs, all rules). The one place in `src/` where blanking reaches code is `families.rs:386` (`b"://"`: the rest of that line is blanked in the copy only).
- **Hostile texts for `comments_blanked`** (`t07_hostile`, debug): unclosed `/*` at the end, a lone `/` at the end, a lone `*`, `//` at the very end, `/` alone, empty, `/*` × 64 Ki, `*/` × 64 Ki, `/*/` × 64 Ki, `//` × 64 Ki, `/é` × 64 Ki, an unclosed `/*` before 64 Ki of `東🙂`, `//` before 64 Ki emoji, 64 Ki nested openers then one closer: **no panic, no loop, each under 33 ms** (128-458 KB). **But the new path rule is quadratic** on a run of root paths: `std :: ` × 1 Ki 122 ms, × 2 Ki 480 ms, × 4 Ki 1.90 s, × 8 Ki 7.59 s, × 16 Ki (115 KB) **30.4 s**; `std::` glued × 8 Ki 7.64 s; control `a :: ` × 64 Ki (no root) 37 ms. Cause (READ): for every root token the `take_while` walks the whole following identifier/`::` run and collects it into a `String`, so a run of n roots costs n². Test-only; on the real `src/` it costs nothing (0 roots). → Note N-3.
- **What the head still misses** (each a real, compiling use: `rustc --edition 2021 --crate-type lib --emit=metadata` on a file holding it → exit 0; control: NBSP between `std` and `::` → exit 1 `unknown start of token`):
  - (a) **a comment marker inside a literal before a comment-hidden alias**: `let u = "a//b"; use std /* c */ as s;`, `let u = "/*"; use std /* c */ as s;`, `let u = "/*";` then on a LATER line `use std /* c */ as s;`, `r#"/*"#` then a later line, `b"/*"` then `use core // c` + LF + `as c;`. A `/*` in any literal blanks the REST OF THE FILE in the copy (it is read as an unclosed comment), a `//` in a literal blanks the rest of its line; the run on the text as given never sees through a comment. Base misses them too (not a weakening). → Note N-1.
  - (b) **Rust whitespace that is not ASCII whitespace** around `::` or `as`: VT (U+000B), U+0085, U+200E, U+200F, U+2028, U+2029 are whitespace to rustc but separate tokens to `token_hits`: `std\u{2028}::env::var("X")`, `std\u{200e}::\u{200e}env`, `std\u{0b}::\u{0b}env`, `std\u{85}::env`, `use std\u{2029}as\u{2029}s;`, `use std\u{200f}as s;` → no hit at base or head. → Note N-2 (pre-existing class, newly reachable now that blanks around `::` are claimed).
  - A doc comment that itself holds a commented alias (`//! use std /* c */ as s;`) → no hit at either (the copy blanks the whole comment; the text-as-given run sees `/ *` between `std` and `as`). It names no item in code; recorded only.

## 5. The words — READ (each against the code at the head and my probes of item 3)
- **`Finding`'s doc comment** (`lib.rs:100-101`): "how many matches of it were found (in whichever of the scanned views, docs/SCANNER.md section 2, found the most)". Code: `scan` (`lib.rs:243-275`) keeps, per family, the finding with the largest count over the views (`keep_largest`, `b.count > a.count`). **True.** ASCII only; no `t07` forbidden name and no `rand` word in it (t07 green at the head, §4 and the red script's green run).
- **§2 view (3) clause** (`SCANNER.md:55-56`): "(when the text holds no format character, view 2 is the text as given)". Code: `let mut view = text; if has_format { view2 = …; view = &view2; } if view.contains("\u{1b}[") { … }` (`lib.rs:258-267`). **True.** The one removed docs line is this sentence's line, rewrapped into two with the clause inserted; every other base line of `docs/SCANNER.md` is kept in order (checked by program: 1 base line not kept, this one).
- **§3 t07 sentence** (`SCANNER.md:169-171`): "also refuses `std`, `core` or `alloc` directly before `::` with blanks around it (`std :: env`), and runs a second time on a copy of the file with every `//` and `/* */` comment blanked (`use std /* c */ as s;`), beside the run on the file as given". **True** for the code (§4 READ) and shown by my probes and plants. Loose but not false: "blanks" means ASCII whitespace only (N-2), and "every comment blanked" also blanks after a `//` or `/*` inside a literal (N-1); the code comment says the latter, the docs do not. Notes, not graded higher: nobody acts on this sentence about the scanner's behaviour.
- **§4 bullet** (`SCANNER.md:198-205`): the seven forms, each with its docs example, are Clean at base and head (§3; the docs' own `x` examples TESTED); the closing sentence, "The argv look-ahead crosses only blanks and tabs around one comma, and only `\n`, `\t` and `\r` written as a backslash and a letter count as a JSON escape", matches `argv_value_quote` (`families.rs:615-631`) and `after_json_escape` (`:608-610`) exactly, and it is what makes my variants Clean too (any flag after a line break; `\u0009`, `\u000d`). "A flag and its value as shell words with no comma (`'--password' 'x'`)": precisely, the miss is a QUOTED flag followed by anything but a comma (`'--password' qapw0002` is Clean too); `--password 'qapw0002'` (bare flag) is flagged (spaced rule). The example shows the quoted flag, so the bullet does not mislead. **True.**
- **§5 row** (`SCANNER.md:253`): the four examples flag at base and head, by exactly the families the last column names (PasswordArgument; the two upper-case forms also SecretAssignment, whose `text()` is "a value given to a secret-looking or upper-case name", `lib.rs:83`). "(flags are lower-cased before the name test)" matches `families.rs:651-653`. **True, with two refinements for the owner's card (Notes, wording; nothing the owner would decide wrongly from the row as written):** (1) the Windows clause is wider than `-u a:b`: a backslash, `n`/`t`/`r`, then ANY flag the flag rule takes (`C:\tools\n--key-file id_rsa` → PasswordArgument; `D:\work\r--password …` too), and narrower than "a folder whose name starts with" suggests: the letter must be followed directly by `-` (`C:\tools\nightly-u qa:x` → Clean); (2) **if the owner considers loosening the upper-case forms**: a case-sensitive flag rule would clear `-U=qa:x` from PasswordArgument only (SecretAssignment keeps it flagged, as the row says) but would also make `curl -U qa:qapw0001 …` Clean — curl's `-U` is `--proxy-user user:password`, a real credential, caught today only because flags are lower-cased (TESTED with `loose_case`: head PasswordArgument 1 → loosened `[]`). Switching off only form (b) for upper case would not have that cost (`loose_b` keeps it). REASONED for curl's option meaning; TESTED for the scanner's answers.
- **BACKLOG** (`BACKLOG.md:1522-1527`, appended after the base's last line 1521): entry 1 (Where: `argv_value_quote`, `after_json_escape`; Symptom: the seven forms, pinned in t03 and docs §4; Why deferred: R-2, R-3, a later lane with its own two-head differential; Discovered) and entry 2 (one line naming the three forms, the docs §5 row and the `KNOWN_OVERFLAGS` pins). Both match what was done. **Nothing existing edited:** sha256 of lines 1-1521 at the head = the base file whole = `af53c40464258394…` (control: lines 1-1522 at the head → `467030e41310a7eb…`); the base file ends with a line feed, so the append touches no base byte.
- `t03` and `t07`: every base line kept in order at the head (program, 0 not kept); `docs/M0-OUTCOMES.md` untouched (optional, the builder says so; true).
- Judgement: **no word says anything false about what the scanner does.** The section 5 row and the section 4 bullet are true as written.

## 6. Not wired — TESTED
- `git grep -n -I -E 'coagent[-_]scanner' <sha> -- . ':!crates/coagent-scanner'`: base 19 lines, head 20; `diff` of the two lists: ONE added line, `BACKLOG.md:1523` (this lane's "Where:" naming `crates/coagent-scanner/src/families.rs`), and one docs line number moved (267 → 280). Files: `BACKLOG.md` 5, `Cargo.lock` 1 (its own package entry), root `Cargo.toml` 1 (`members`, `:18`), `docs/SCANNER.md` 2, `scripts/red-controls-scanner.sh` 11. **No other crate, script or manifest names it** beyond what main has; manifests outside the crate naming it: 1 (the root `members` line, as main). `cargo tree -i coagent-scanner -e all` → only its own `default` feature (§1).
- Positive control: the same search for `coagent[-_]policy` outside its crate → 130 lines, 4 manifests.
- Judgement: **not wired; nothing calls, imports or depends on the scanner.**

## 7. Names and ids — TESTED
Own tool outside the repository (`/private/tmp/claude-501/qsx/namescan/scan.py`, `python3 -B -I`; reads bytes; prints `file:line` and the word's NUMBER, never the word), **29 words passed on the command line only** (owner name parts and handle, the login name, short and full host name and computer name read at run time, the home path, mail domains, coordinator names, client names, workspace drive and folder names, `/Users/`, `/Volumes/`, `/private/tmp`, the temp user folder, the mail service, the deploy-key file name, the credentials, keys and brain folder names, `noreply`), **94 spellings** (plain, lower, upper, URL-encoded, backslash-escaped blanks, slugs, backslash paths; words under 5 letters as whole words only), plus id shapes (UUID, `toolu_`/`msg_`/`req_`/`session_` ids, `sk-ant-`).
- **The 124 added lines** (`git diff -U0 debbb44 dd70630`, `+` lines) and **the 5 changed files whole at the head**: `scanned 6 files, 94 spellings of 29 words: 44 word hits, 4 id shapes`. **0 word hits in the added lines**; all 44 are in `BACKLOG.md` lines 241-1420, main's own text (the lane's entries are 1522-1527). The 4 id shapes are the made-up `deadbeef-0001-…`/`deadbeef-0002-…` UUIDs in unchanged lines (`t03:19`, `:93`; docs `:228`, `:244`).
- **Controls:** a scratch copy of `t07_pure.rs` with one planted line (login name, short host name and home path, generated at run time) and a planted binary (NUL, `BIN`, the home path, NUL, 0xFF, a made-up `toolu_` id, NUL): `scanned 2 files … 13 word hits, 1 id shapes` (7 on the copy's line 285, 6 in the binary, plus the `toolu_` id). Both found.
- **Every secret-shaped value in the added lines is made up:** `qapw0001` (×9), `qa:qapw0001`, `qa:x`, `a:b`, `x` — the `t03` style; no other value of 6+ characters with a digit except dates, paths and identifiers (`2026-11-25`, `u000a--password`, `from_utf8`, `0usize`).
- The commit's author identity is the repository's configured one (a GitHub noreply address), not in any file; the commit message holds no name.
- Judgement: **nothing of the owner's in what the lane adds; no real secret.**

**TESTED, planted copies of `src/`** (each its own scratch copy and its own EMPTY target dir; each log shows `Compiling coagent-scanner`; `COAGENT_SCANNER_SRC_DIR` pointed at the copy, as the red script's planted row does; the head's `t07_pure` and the base's `t07` copied as a test target, `qa_t07_base`):

| Copy | Planted (where) | Head `t07_pure` | Base `t07` |
|---|---|---|---|
| plant_0 (control) | nothing | exit 0, green | exit 0, green |
| plant_1 | `    use std /* c */ as s;` in `families.rs` after `:386` (right below the `b"://"` line) | **exit 101**: `t07: the scanner source names a forbidden item: ["families.rs:387: std alias (comments blanked)"]` | exit 0 (misses it) |
| plant_2 | `    use std // c` + LF + `        as s;` in `lib.rs` after `:232` | **exit 101**: `["lib.rs:234: std alias (comments blanked)"]` | exit 0 |
| plant_3 | `fn planted() -> bool { std :: env :: var("X").is_ok() }` in `families.rs` after `:13` | **exit 101**: `["families.rs:14: std :: path", "families.rs:14: std :: path (comments blanked)"]` | exit 0 |

Each of the three new spellings planted in a real source file turns the head test red; the base test stays green on the same copies (so the plants exercise exactly the new rules); the unplanted copy is green at both.

**TESTED, the red script once** (per ADDENDUM 1, run without waiting for a slot: the counter read 3 all along, Friday's merge checks and another seat's run): `bash scripts/red-controls-scanner.sh` from the root of a pristine second clone at `dd70630` (no QA file in it), `COAGENT_TOOLS`, `COAGENT_SCANNER_RED_TARGET`, `_LOGS`, `_SCRATCH` all in my work dir (new empty dirs), 16:48:25-16:50:00, **exit 0**:
```
names: 21 red controls, each in build.rs, used under src/ and a row
no_pem … no_base64_lines  P1  RED  (each "t01: exactly '<its test>' failed")
flag_everything P2 · reason_echoes_text P3 · prefix_window P4 · quadratic_line_end P5 · slice_mid_char P6   RED
flag_after_space_only M1 RED (130 of 240) · line_end_lf_only m1 RED · ansi_kept m2 RED
cr_run_split N-R1 RED · one_stripped_view N-R2 RED · argv_space_only N-R5 RED (96 of 96)
rows: 21 cfg rows
planted std::env     P7   RED     t07_pure::the_scanner_reads_nothing (scratch copy e244c7)
      evidence: t07: the scanner source names a forbidden item: ["lib.rs:307: std::env", "lib.rs:307: std:: path", "lib.rs:307: std :: path", "lib.rs:307: std :: path (comments blanked)"]
==> green run (no red control): coagent-scanner, every test
GREEN: 28 tests ok
RED CONTROLS OK: every guard went red under its control, on its property, and green without
```
(rows condensed from two lines each; 21 rows counted RED in the log; whole log `gate_scanner_next_tests/logs/red_script.log`). **21 rows red, the planted row red (now with item 3's two extra hits beside the base's two), the green run green with 28 tests** — the builder's figures exactly.
- Judgement: **the purity test got stronger and can still fail.** Every base hit is a head hit; the three new spellings turn it red in a real source file; `src/` gives 0 hits. What it still misses (N-1, N-2) the base missed too; the new path rule is quadratic on a hostile run of root paths (N-3).

## Every probe spelling (item 4)
Input as written in the probe (escapes as Rust writes them); "mine" rows were run wrapped, at the start of a file and at its end, with the same answer in all three placements. Base / head = whether `hits` returns anything.
| # | Spelling (source) | Base | Head | Judgement |
|---|---|---|---|---|
| 1 | `use std /* c */ as s;` (check's 17) | not found | found | newly found (item 3) |
| 2 | `use std // c\n    as s;` (check's 17) | not found | found | newly found (item 3) |
| 3 | `fn f() -> bool { std :: env :: var(\"X\").is_ok() }` (check's 17) | not found | found | newly found (item 3) |
| 4 | `fn f() -> bool { std::env ::var(\"X\").is_ok() }` (check's 17) | found | found | found at both |
| 5 | `use std::{self as s};` (check's 17) | found | found | found at both |
| 6 | `use r#std as s;` (check's 17) | found | found | found at both |
| 7 | `extern crate std as s;` (check's 17) | found | found | found at both |
| 8 | `use ::{std as s};` (check's 17) | found | found | found at both |
| 9 | `pub use std as s;` (check's 17) | found | found | found at both |
| 10 | `use core::{self};` (check's 17) | found | found | found at both |
| 11 | `fn f() -> bool { ::core::mem::size_of::<u8>() == 1 }` (check's 17) | found | found | found at both |
| 12 | `type S = ::alloc::string::String;` (check's 17) | found | found | found at both |
| 13 | `use std::{env};` (check's 17) | found | found | found at both |
| 14 | `use self::std as s;` (check's 17) | found | found | found at both |
| 15 | `use crate::x as std;` (check's 17) | not found | not found | not a use of std/core/alloc (recorded) |
| 16 | `macro_rules! m { () => { std } }` (check's 17) | not found | not found | not a use of std/core/alloc (recorded) |
| 17 | `use\tstd\tas\ts;` (check's 17) | found | found | found at both |
| 18 | `use std /* a /* b */ c */ as s;` (mine, 3 placements) | not found | found | newly found (item 3) |
| 19 | `use std\n/* c */\nas s;` (mine, 3 placements) | not found | found | newly found (item 3) |
| 20 | `use core /* c */ as c;` (mine, 3 placements) | not found | found | newly found (item 3) |
| 21 | `use alloc // c\n as a;` (mine, 3 placements) | not found | found | newly found (item 3) |
| 22 | `use ::std /* c */ as s;` (mine, 3 placements) | not found | found | newly found (item 3) |
| 23 | `use { std /* c */ as s };` (mine, 3 placements) | not found | found | newly found (item 3) |
| 24 | `use r#std /* c */ as s;` (mine, 3 placements) | not found | found | newly found (item 3) |
| 25 | `use std/**/as s;` (mine, 3 placements) | not found | found | newly found (item 3) |
| 26 | `fn f() -> bool { std/* c */::env::var(\"X\").is_ok() }` (mine, 3 placements) | not found | found | newly found (item 3) |
| 27 | `fn f() -> bool { std::/* c */env::var(\"X\").is_ok() }` (mine, 3 placements) | found | found | found at both |
| 28 | `fn f() { core :: mem :: drop(1) }` (mine, 3 placements) | not found | found | newly found (item 3) |
| 29 | `type V = alloc :: vec :: Vec<u8>;` (mine, 3 placements) | not found | found | newly found (item 3) |
| 30 | `fn f() -> bool { std\n::\nenv::var(\"X\").is_ok() }` (mine, 3 placements) | not found | found | newly found (item 3) |
| 31 | `fn f() -> bool { std\t::\tenv::var(\"X\").is_ok() }` (mine, 3 placements) | not found | found | newly found (item 3) |
| 32 | `fn f() -> bool { r#std :: env :: var(\"X\").is_ok() }` (mine, 3 placements) | not found | found | newly found (item 3) |
| 33 | `/// see std :: env :: var for the variable` (mine, 3 placements) | not found | found | newly found (item 3) |
| 34 | `//! use std /* c */ as s;` (mine, 3 placements) | not found | not found | a comment holding a commented alias: names no item in code (recorded) |
| 35 | `*/ use std /* c */ as s;` (mine, 3 placements) | not found | found | newly found (item 3) |
| 36 | `/*/ use std as s; */` (mine, 3 placements) | found | found | found at both |
| 37 | `let u = \"http://x\";\nuse std /* c */ as s;` (mine, 3 placements) | not found | found | newly found (item 3) |
| 38 | `let u = \"a//b\"; use std /* c */ as s;` (mine, 3 placements) | not found | not found | **head misses a real use** (Note N-1: comment marker inside a literal; rustc compiles it) |
| 39 | `let u = \"/*\"; use std /* c */ as s;` (mine, 3 placements) | not found | not found | **head misses a real use** (Note N-1: comment marker inside a literal; rustc compiles it) |
| 40 | `let u = \"/*\";\nfn g() {}\nuse std /* c */ as s;` (mine, 3 placements) | not found | not found | **head misses a real use** (Note N-1: comment marker inside a literal; rustc compiles it) |
| 41 | `let r = r#\"/*\"#;\nuse std /* c */ as s;` (mine, 3 placements) | not found | not found | **head misses a real use** (Note N-1: comment marker inside a literal; rustc compiles it) |
| 42 | `let c = b\"/*\";\nuse core // c\n as c;` (mine, 3 placements) | not found | not found | **head misses a real use** (Note N-1: comment marker inside a literal; rustc compiles it) |
| 43 | `let r = r#\"use std /* c */ as s;\"#;` (mine, 3 placements) | not found | found | literal only: head's extra hit is harmless (stricter) |
| 44 | `let s = \"std :: env\";` (mine, 3 placements) | not found | found | literal only: head's extra hit is harmless (stricter) |
| 45 | `fn f() -> bool { std\u{b}::\u{b}env::var(\"X\").is_ok() }` (mine, 3 placements) | not found | not found | **head misses a real use** (Note N-2: whitespace to rustc that `is_ascii_whitespace` does not count; rustc compiles it) |
| 46 | `fn f() -> bool { std\u{85}::env::var(\"X\").is_ok() }` (mine, 3 placements) | not found | not found | **head misses a real use** (Note N-2: whitespace to rustc that `is_ascii_whitespace` does not count; rustc compiles it) |
| 47 | `fn f() -> bool { std\u{200e}::\u{200e}env::var(\"X\").is_ok() }` (mine, 3 placements) | not found | not found | **head misses a real use** (Note N-2: whitespace to rustc that `is_ascii_whitespace` does not count; rustc compiles it) |
| 48 | `fn f() -> bool { std\u{2028}::env::var(\"X\").is_ok() }` (mine, 3 placements) | not found | not found | **head misses a real use** (Note N-2: whitespace to rustc that `is_ascii_whitespace` does not count; rustc compiles it) |
| 49 | `use std\u{200f}as s;` (mine, 3 placements) | not found | not found | **head misses a real use** (Note N-2: U+200F is Rust whitespace; rustc compiles it) |
| 50 | `use std\u{2029}as\u{2029}s;` (mine, 3 placements) | not found | not found | **head misses a real use** (Note N-2: whitespace to rustc that `is_ascii_whitespace` does not count; rustc compiles it) |
| 51 | `use std\u{c}as s;` (mine, 3 placements) | found | found | found at both |
| 52 | `fn f() { mystd :: x() }` (mine, 3 placements) | not found | not found | not a use of std/core/alloc (recorded) |

## Findings
**No Blocker. No Major.** Every scanner answer is unchanged, every pin is true, the docs and BACKLOG say nothing false, the purity test lost nothing and fails on each new spelling, scope is clean, nothing is wired, nothing of the owner's is added. Repro files: `gate_scanner_next_tests/` (see its README; in a clone at `dd70630` with the QA files in `crates/coagent-scanner/tests/`).

**N-1 (Note, test strength): `comments_blanked` does not skip literals, so a comment marker inside a string hides a comment-split alias from both runs.**
- File: `crates/coagent-scanner/tests/t07_pure.rs:108-146` (`comments_blanked`).
- What happens: a `/*` inside a string, raw string or byte string is read as an unclosed comment and blanks the REST OF THE FILE in the copy; a `//` inside a string blanks the rest of its line. After such a literal, `use std /* c */ as s;` (or `use core // c` + LF + `as c;`) is found by neither run (e.g. `let u = "/*";` then, lines later, `use std /* c */ as s;`). Each compiles (rustc exit 0). Not a weakening (the base misses them too); not in `src/` today (its only marker in a literal is `b"://"`, `families.rs:386`, which blanks only the rest of that line).
- Repro: `cargo test --locked -p coagent-scanner --test qa_sx_t07 -- --nocapture t07_spellings 2>&1 | grep "HEAD MISSES"`.
- Suggested fix: when blanking, step over `"…"` (with `\` escapes), `r#"…"#` (any number of `#`), `b"…"`/`br"…"` and char literals unchanged, so only real comments are blanked; then fix the doc comment's "can only add a hit, never hide one" to say "relative to the run on the text as given".

**N-2 (Note, test strength, pre-existing class): `token_hits` separates tokens only on ASCII whitespace; rustc also takes VT, U+0085, U+200E, U+200F, U+2028, U+2029 as whitespace.**
- File: `crates/coagent-scanner/tests/t07_pure.rs:162` (`c.is_ascii_whitespace()`), and so the item-3 rule `:190-201` and the alias rule `:183`.
- What happens: `std\u{2028}::env::var("X")`, `std\u{200e}::\u{200e}env…`, `std\u{0b}::\u{0b}env…`, `std\u{85}::env…`, `use std\u{2029}as\u{2029}s;`, `use std\u{200f}as s;` compile (rustc exit 0; NBSP control exit 1) and give no hit at base or head. Now that the docs claim "blanks around `::`" are covered, these are the remaining blanks.
- Repro: as N-1 (`HEAD MISSES … \u{2028}` etc.); `gate_scanner_next_tests/rustc_ws/*.log` for the compiles.
- Suggested fix: treat every Rust whitespace character (Pattern_White_Space: the ASCII five, VT, U+0085, U+200E, U+200F, U+2028, U+2029) as a blank in `token_hits` (step by `char`, not byte, there).

**N-3 (Note, test robustness): the new path rule is quadratic on a run of root paths.**
- File: `crates/coagent-scanner/tests/t07_pure.rs:193-197` (`toks[k..].iter().take_while(…).collect()` for every root token).
- What happens (debug): `std :: ` × 4 Ki 1.90 s, × 8 Ki 7.59 s, × 16 Ki (115 KB) 30.4 s; `std::` × 8 Ki 7.64 s; without a root, `a :: ` × 64 Ki 37 ms. No panic, no loop; on the real `src/` it costs nothing (0 roots). A hostile or generated source file could make `t07` (and the red script's green run) very slow.
- Repro: `cargo test --locked -p coagent-scanner --test qa_sx_t07 -- --nocapture t07_hostile 2>&1 | grep quadratic`.
- Suggested fix: stop the walk after as many tokens as the longest `ALLOWED_PATHS` entry needs (with the list empty, push without walking), or join the path once per run of tokens instead of once per root.

**N-4 (Note, words, the builder's STATUS): the docs figure.** `STATUS_SCANNER_NEXT.md:21` says `docs/SCANNER.md` "+15 −2"; numstat is **+14 −1** (Friday's read is right). Nothing follows: the STATUS §8 quotes equal the diff. Repro: `git diff --numstat debbb44 dd70630 -- docs/SCANNER.md`. Fix: none needed beyond the record.

**N-5 (Note, words for the owner's card): the §5 row's Windows clause, and what loosening the upper-case forms would cost.**
- File: `docs/SCANNER.md:253`.
- (a) The Windows over-flag is any flag the flag rule takes right after `\n`/`\t`/`\r` (`C:\tools\n--key-file id_rsa` → PasswordArgument), not only `-u a:b`; and the folder must be exactly the letter followed by `-` (`C:\tools\nightly-u qa:x` → Clean), narrower than "a folder whose name starts with". (b) A case-sensitive flag rule would clear `-U=`'s PasswordArgument (SecretAssignment keeps it flagged, as the row says) but would also make `curl -U qa:qapw0001 …` Clean — curl's `-U` is `--proxy-user user:password`, a real credential, flagged today only because flags are lower-cased. Switching off form (b) for upper case would not cost that.
- Repro: `cargo test --locked -p coagent-scanner --test qa_sx_pins -- --nocapture p_owner_card`.
- Suggested fix: one clause in the row, or on the owner's card at wiring time: "(any sensitive flag, right after a backslash and n/t/r)"; and "loosen the upper-case `=` form only, not the lower-casing: `curl -U user:password` depends on it".

**N-6 (Note, pre-existing, outside this lane): `curl --proxy-user qa:qapw0001 https://h` is Clean at base and head and is not in docs §4.** A real credential form (`--proxy-user` is neither `-u`/`--user` nor a sensitive name). Repro: `p_owner_card` above (`head []`). Suggested fix: a later scanner lane records it in §4 with a pin, or adds `--proxy-user` to the user-flag names (a rule change, with its own two-head differential).

**Open (no category):** none.

## What was NOT checked
| Not checked | Why / what would check it |
|---|---|
| `scripts/check.sh` whole (workspace fmt, clippy, tests, deny) | the brief says not to (Friday's merge check runs it). The red script's green run passed the crate's 28 tests |
| `cargo fmt --check` and the crate's `clippy -D warnings` | not run by me (the builder reports both exit 0); the merge check's `check.sh` runs them |
| Linux and Windows | macOS only; the lane adds no OS code |
| The builder's harness, logs, worktree and scratch (`coagent/tools/tmp/scx`) | not touched by the brief's rule; every harness re-made by me |
| Compiling the planted spellings INTO the crate | the plants were read by `t07` through `COAGENT_SCANNER_SRC_DIR` (as the red script's planted row does); the gap spellings were compiled separately with rustc |
| Literals and whitespace beyond my probe list (e.g. `'/'` char tricks, macros building paths, `concat!`) | not enumerated; N-1 and N-2 name the classes |
| Timing on an idle machine | 3 other heavy jobs ran during every run of mine; times are upper bounds |
| `qa_props` | not asked; no scanner code changed (§1, §2) |
| How a later wiring lane uses the over-flag record | later lane |

## Process notes (QA seat)
- Work dir `/private/tmp/claude-501/qsx`: `clone/` (my QA files under `crates/coagent-scanner/tests/`, never committed), `clone_red/` (pristine at `dd70630`, for the red script), `plant_0..3/` (scratch `src/` copies), `rustc_ws/`, `namescan/`, own target dirs (`target_main`, `target_diff`, `target_pins`, `target_t07probe`, `target_plant_0..3`, `red_target`) and cargo home (`tools/cargo` whose `bin` and `rustup` are links to the project's toolchain). Network: `git fetch`/`ls-remote` from GitHub with the deploy key and `cargo fetch --locked` only. No model run. No `cd` in my commands except inside the one subshell that starts the red script from its clone's root, as the brief's form requires.
- In the project repository I used only `git --no-optional-locks` read verbs (and `git clone` from it). The only file written in the project folder is my STATUS file.
- One slip, no effect: one command line held a stray `rm -rf /dev/null`, which the system refused; nothing was deleted anywhere. One status update was staged through a file in `/tmp` and moved at once into my work dir.
- Copies of every script and test I wrote, and my logs, are in `gate_scanner_next_tests/` (the name scan's planted controls and their log are not copied).
