VERDICT: GO WITH NOTES — head 1096a77b88330029ecac3df3bc2cef8c6c18d400

# QA-SCANNER-CORE-R2: second check of branch `scanner-core` (the fix round only)

Seat QA-SCANNER-CORE-R2, 2026-11-24. Brief: Friday's `briefs_drafts/2026-11-24_coagent_QA-SCANNER-CORE-R2_check_brief.md`. I did not make the round. Work dir `/private/tmp/claude-501/qsc2` (own clone, own empty target dirs and cargo home; toolchain linked as `coagent_merge_check.sh` does, `RUSTUP_TOOLCHAIN=1.100.0`: cargo 1.100.0, rustc 1.100.0 (0ef1bc386 2026-11-09)). Every comparison by SHA. TESTED = I ran it; READ = I read it. Every secret-shaped string below is made up.

## BLUF
- **Is the quoted-password miss closed?** Yes. All 240 of the first check's wrapped cases now flag (126 were Clean). So do 2 212 of my 2 380 wrappings: every punctuation byte, control byte, tab, line start after CR, non-ASCII and invisible character before the flag. The ones left Clean are the four bytes the fix list exempts on purpose (`.` `/` `_` `-`), plus two documented cases where a letter touches the flag (`ESC ( B` and a JSON `\n` escape).
- **Did the fix open a new miss?** Yes, three narrow ones, and each follows from the fix list's own wording. (1) Short base64 lines separated by a doubled carriage return (`\r\r\n`, a common Windows artefact). (2) A token that holds an invisible character AND touches a terminal colour code. (3) A `.netrc` `machine` behind a carriage return, which is the ruled meaning. None of them shows up in the first check's 300 000 generated texts or in ordinary text. I raise them as Notes, each with a one-line fix. Read strictly, brief §3 would make (1) and (2) Majors and the answer NO GO.
- **Can the new code crash, stall or leak?** No. 600 000 property cases (release and debug) gave no panic and identical answers each run. On 27 hostile shapes aimed at the new code, the worst time is 50 ms in debug and 7 ms in release, and doubling the input doubles the time. A verdict still holds only family names and counts.
- **How much more ordinary text flags?** Plain chat and report lines: no change, 0 new flags in 288 sentences (still 2.6 % and 28.3 %). A message that names an option whose name contains key, token, auth, session, secret, pass (or similar) inside backticks or brackets, followed by a word, now flags. 29 of my 100 such sentences newly flag (4 % → 33 %). Ordinary option names add nothing.

## Proofs (section 0) — TESTED
- `git ls-remote gh scanner-core main` (GitHub remote, deploy key) → `039b9875b69918c2a83e95d84f7f8169358b59d5 refs/heads/main` · `1096a77b88330029ecac3df3bc2cef8c6c18d400 refs/heads/scanner-core`. Both match the brief.
- `git merge-base --is-ancestor 039b987… 1096a77…` → exit 0; `git merge-base --is-ancestor b0835a9… 1096a77…` → exit 0; `git merge-base 039b987 1096a77` = `039b9875…` (main not merged in: origin/main did not move).
- `git log b0835a9..1096a77` → 2 commits: `8fe7faf` (parent `b0835a9`, "fix round … M1, m1, m2, m3, item 5, notes"), `1096a77` (parent `8fe7faf`, "PEM keeps the redactor's newline header window").
- Builder STATUS `coagent/5_Project_History/STATUS_SCANNER_CORE.md`: 241 lines; last line `READY FOR QA SCANNER-CORE r2`, line above it `1096a77b88330029ecac3df3bc2cef8c6c18d400`. Matches.

## 1. Head, base, scope of the round — TESTED
- `git diff --stat b0835a9 1096a77` → 12 paths, 667+ / 73−: `BACKLOG.md`, `crates/coagent-scanner/{build.rs, src/families.rs, src/lib.rs, tests/common/mod.rs, tests/t03_known_overflag.rs, tests/t05_bounds.rs, tests/t07_pure.rs, tests/t08_docs.rs, tests/t09_fix_round.rs (new, 100644)}`, `docs/SCANNER.md`, `scripts/red-controls-scanner.sh`. No mode change (`--summary`: only the one create).
- `git diff --name-only 039b987 1096a77` → 19 paths: the 18 of round 1 + `t09_fix_round.rs`. Every one is in the lane brief's owned set (§7).
- Every existing crate (12, from `git ls-tree -d 039b987 crates/`), `git diff <A> <B> -- <crate> | wc -c` for `039b987..1096a77` and for `b0835a9..1096a77` → **0 / 0** for each of coagent-audit-host, -audit, -cli, -crypto, -daemon, -hook, -ipc, -mcp, -policy, -proto, -relay, -roster. Control: `crates/coagent-scanner` over `b0835a9..1096a77` → 32 927 bytes.
- Root files: `git diff b0835a9 1096a77 -- Cargo.toml Cargo.lock crates/coagent-scanner/Cargo.toml | wc -c` → **0** (the round did not touch them). Against main, whole diff, unchanged from round 1:
  ```
  Cargo.toml  @@ -15,6 +15,7 @@ members = [ … "crates/coagent-hook",
              +    "crates/coagent-scanner",
  Cargo.lock  @@ -352,6 +352,10 @@
              +[[package]]
              +name = "coagent-scanner"
              +version = "0.0.1"
              +
  ```
- `BACKLOG.md` over the round: 10 added lines after base line 1378, 0 removed (two entries: N2 for the wiring lane; the redactor's copy of M1 for the lane owning coagent-audit). Against main: 20 added, 0 removed (append only).
- Judgement: **scope clean.**

## 2. Every changed line of the round, item by item against ADDENDUM 2 — READ
Read: the whole diff `b0835a9..1096a77` (12 files), every line. Line numbers are at `1096a77`. Removed lines in test files and the script over the round: exactly two, `common/mod.rs` `let v: Vec<(&str, &str)> = vec![` (re-wrapped by rustfmt onto two lines, same code) and the script's comment header (`property` → `property or finding`). **No round-1 test, assertion or case was removed or weakened**; every other test change is an addition (t03 +21 pins, t05 +9 shapes, t07 +11 forbidden words, a path rule and 8 planted controls, t08 +1 name, `common` +1 clean case, t09 new).

| Item | What was ruled | What the round did (file:line) | Exactly that, nothing more? |
|---|---|---|---|
| 1 M1 | a flag may start after any byte that is not an ASCII letter/digit, `-`, `_`, `.`, `/`; the 240 cases as a test; a red control restoring the old rule; new over-flags pinned and in the docs; clean-corpus changes listed | `flag_may_start_after` `families.rs:575-581`, used at `:590`; `t09::m1_password_flags_wrapped` (240 + 4); red `flag_after_space_only` (`:577`); 10 pins in t03 and a docs §5 row; STATUS lists them | **Yes.** The old start set (start or ASCII whitespace) is a subset of the new one, and the loop's jumps (`i = e.max(i+1)`, the glued `-p` value `e = e.max(ve)`) only skip bytes that are not whitespace, so no start the old rule saw is skipped now (READ; confirmed by the two-head differential, §4: 0 PasswordArgument losses outside item 5 and the line-end rule). |
| 2 m1 | lone CR, U+0085, U+2028 end a line as LF does for base64 lines, PEM, netrc; a leading `>`/`> ` (repeated) skipped in the line test; JSON `\n` NOT decoded and listed; tests; one red control | `line_term` `:120-130` (`\r` is a line end unless the next byte is `\n`, `:125`), `skip_quote_markers` `:134-139` (skips blanks and `>`), `gle`/`gls` built once per text `:150-169` (linear); base64 `:850-864`; netrc `:677-721` (`machine` via `LineHas::general`, `>` or a line start before `password` `:683`, value cut at the line end); PEM keeps `t.line_end` `:341` (see below); docs §4 lists JSON `\n`; red `line_end_lf_only` `:124` | **Yes, with one decision of the builder's (PEM) and two side effects of the rule as written** (Notes N-R1, N-R3 below): a CR that is followed by another CR or a blank counts as "lone", so `\r\r\n` is now a line end plus an empty line. |
| 3 m2 | in the stripped view remove `ESC [` … final 0x40-0x7E; the check's two cases; a red control; an ESC-heavy timing shape | `stripped_view` `lib.rs:184-213` (params 0x30-0x3F, intermediates 0x20-0x2F, final 0x40-0x7E; no final → kept); the second scan also runs on `ESC [` (`:235`); red `ansi_kept` (`:190`); t05 +4 ESC shapes | **Yes.** The stripped view of `b0835a9` (format characters removed, nothing else) no longer exists on its own: the one stripped view now removes both. That is what "in the stripped view" says; its side effect is Note N-R2. |
| 4 m3 | the named characters + the rest of the assigned Default_Ignorable_Code_Point set, written out, source named, no table read; unassigned NOT added and listed | `lib.rs:170-177`: 17B4-17B5, 180B-180D, 180F, 206A-206F, 1BCA0-1BCA3, 0600-0605, FFF9-FFFB; comment names `DerivedCoreProperties-18.0.0.txt`; docs §4 lists unassigned points | **Yes.** TESTED (`qa_r2.rs::r2_m3_every_position`): all 405 assigned Default_Ignorable code points (the published set as I know it from Unicode 15/16: 00AD, 034F, 061C, 115F-1160, 17B4-17B5, 180B-180F, 200B-200F, 202A-202E, 2060-2064, 2066-206F, 3164, FE00-FE0F, FEFF, FFA0, 1BCA0-1BCA3, 1D173-1D17A, E0001, E0020-E007F, E0100-E01EF) are on the list; beyond that set the list holds only 0600-0605 and FFF9-FFFB (ruled) and the unassigned E0000, E0002-E001F that round 1 already had (the round added no unassigned point). I did not re-read the 18.0.0 file (no network beyond `cargo fetch`). |
| 5 htpasswd | letters case-sensitive: `-B` alone not, `-b`/`-bc`/`-Bb` yes; a test; docs | `letters = &b[i + 1..e]` `:614`; `t09::item5_htpasswd_flag_case`; docs §2 | **Yes.** |
| 6 notes | N3 path rule + `include!`, `#[path`, `static mut`, `use std as`, print macros, planted control stays; N4 sentence; N5 nine rows pinned + docs + STATUS; N2 BACKLOG | t07 `:31-47`, `:69-80`, `:133-148`; docs §2 `:32-35`; t03 `:71-91`, docs §5; BACKLOG +5 lines | **Yes.** Small gaps in N3's word list (Note N-R6). |
| 7 docs | §4 lists what is still missed; BACKLOG entry for the redactor's copy of M1 | docs §4 `:149-175`; BACKLOG +5 lines; `coagent-audit` diff 0 bytes | **Yes.** |

**The builder's one decision: PEM keeps its `\n` header window (`1096a77`).** Judged sound. The window is `min(next \n, 120 bytes)`; any wider line end can only make it shorter, so keeping `\n` keeps every header `b0835a9` found. TESTED: my PEM-window differential (60 000 texts with CR, CRLF, U+0085, U+2028, `> `, colour codes, ZWSP, U+180B, `\r\r\n` and tab between `-----BEGIN`, padding of 0-124 blanks and `PRIVATE`, §4) → **0 texts and 0 families lost** old → new. A PEM block whose lines end in a lone CR, U+0085 or U+2028 is flagged (t09 and my rows). The 8fe7faf variant itself I did not rebuild; the builder's figure of 6 lost headers there is UNVERIFIED by me and does not matter at the head.

## 3. M1 — TESTED
`qa_r2.rs` (release), old = the scanner at `b0835a9` built beside the head in the same test binary.
- **The first check's 240 wrapped cases:** `r2_m1_round1_240` → old Clean **126**; head without `PasswordArgument` **0 of 240**. The first check's own `qa_probe.rs` re-run on the head: its CLEAN rows fell from 141 to 11, none of them a flag row (the 11 are the bound/empty/format-only controls, JSON-escaped base64, and the documented clean cases incl. `htpasswd -B`).
- **My wrappings** (`r2_m1_own_wrappings`): 85 bytes or sequences directly before the flag (all 32 ASCII punctuation bytes, all 33 control bytes 0x00-0x1F and 0x7F, é, 東, 🙂, NBSP, U+0085, U+2028, U+2029, ideographic space, ZWSP, U+180B, U+2065, fullwidth paren, tab, CR, LF, CRLF, `ESC[0m`, `ESC(B`, an OSC title, and a literal backslash-n), each at the text start and after `see `, × the 7 non-`-p` shapes × 2 values = **2 380 cases; old Clean 2 108; head Clean 168**, every one of them in a ruled or documented class:

| Byte before the flag | Head Clean (of 28) | Judgement |
|---|---|---|
| `.` `/` `_` | 28 each | ruled exclusion (ADDENDUM 2 item 1), e.g. `x/--password hunter22` |
| `-` | 8 | ruled exclusion; only `---user`/`---u` lose (`---password` still flags) |
| `ESC ( B` | 28 | the `B` is a letter glued to the flag; docs §4 "a shape glued to a terminal sequence other than `ESC [ … final`" |
| literal `\n` (backslash, `n`) | 28 | the `n` is a letter: a flag right after a JSON `\n` escape, e.g. `"cmd": "a\n--password x"`; same root as the documented "JSON `\n` escapes are not decoded" (listed for base64 only) → Note N-R5 |
| everything else (77 prefixes incl. every other punctuation byte, every control byte, tab, CR, line start after CR, NEL, LS, multi-byte, listed and unlisted invisibles) | **0** | closed |

- **Value forms** (`r2_m1_value_forms`): `` `--password\thunter22` ``, `` `--password  hunter22` ``, `(--password hunter22),`, `` `-u qauser:hunter22` ``, `<…>`, `{…}`, `|…|`, `*…*`, `~--password …` → flagged now (Clean before). `` `--password=hunter22` `` → SecretAssignment (both heads). Clean on both heads and not in the round's list: an argv array `["--password", "hunter22"]` / `"--password", "hunter22"` (the value follows `", "`, not a blank) and `` `--user=qauser:hunter22` `` → Note N-R5 (pre-existing, not listed in §4).
- **M1 is closed.**

**The other side: over-flags of the new start rule** (`r2_overflag_corpora`, every sentence old vs head):
| Corpus | Sentences | Flagged at `b0835a9` | Flagged at head | Newly flagged | No longer flagged |
|---|---|---|---|---|---|
| first check's plain agent chat (`qa_docs.rs` EVERYDAY) | 228 | 6 (2.6 %) | 6 (2.6 %) | **0** | 0 |
| first check's technical report lines (TECHNICAL) | 60 | 17 (28.3 %) | 17 (28.3 %) | **0** | 0 |
| **mine: 100 sentences with command flags in backticks or brackets** | 100 | 4 (4.0 %) | **33 (33.0 %)** | **29** | 0 |

**Read the 33 % with care: it depends on which flags a message names.** My 100 are about half ordinary flags (`--release`, `--locked`, `-p crate`, `--no-run`, `-la`, `--rm`, `-n ns`, `--force` …) and half flags whose NAME holds one of the scanner's name parts (key, secret, token, pass, pw, auth, private, cookie, session, signature, credential). **Ordinary flags: 0 new flags.** Every one of the 29 new flags is a flag with such a name (or `-u`/`--user` with a colon) that sits directly after a backtick, bracket or paren and is followed by a space and a word: `` `--key-file id_qa` ``, `` `--auth-mode login` ``, `[--session-name demo]`, `` `--secret-name qa-config` ``, `` `--token-ttl 1h` ``, `` `--private-key-path keys/qa.pem` ``, `` `--cookie-jar jar.txt` ``, `` `--signature-file sig.bin` ``, `` `--author qa` ``, `` `--keychain login` ``, `` `--passphrase-file pf.txt` ``, `` `--credential-helper store` ``, `` `--auth-type oauth` ``, `` `--pw-file pw.txt` ``, `` `--ssh-key ~/.ssh/qa_ed25519.pub` ``, `` `--api-key-env QA_KEY` ``, `` `--auth-header-name X-Qa` ``, `(--session-timeout 30m)`, `[--key-size 4096]`, `` `--secret-store vault` ``, `` `--passes 3` ``, `` `--bypass-cache yes` ``, `` `--cookie-domain .example.com` ``, `` `--private-registry reg.qa.example` ``, `` `--auth none` ``, `` `--compass-heading 90` ``, `` `--passthrough on` ``, `` `--user root:wheel` ``, `(-u 1000:1000)`. The same flag after a SPACE flagged before the round too (e.g. `az storage blob list --auth-mode login`): the round extends an existing over-flag to the backtick form agents use. **For the owner:** plain chat and report lines flag exactly as often as before; a message that names a key/token/auth/session/secret/pass-type option in backticks now flags where it did not. The docs §5 row ("a user and group, or a flag naming auth, key, session, secret, token or pass, inside backticks, brackets or parens") is confirmed; it also covers names holding private, cookie, signature, credential and pw, and words that merely contain "pass"/"auth" (`--passes`, `--bypass-cache`, `--compass-heading`, `--author`).

## 4. The two-head differential and the base differential — TESTED
**Two heads** (`qa_r2.rs::r2_two_head_differential`, release, 14 s): for every text, old = `b0835a9`'s scanner, new = the head; listed: every text flagged before and Clean now (WHOLE), and every family named before and not now. Then **every loss attributed** (`qa_r2_attr.rs`): four copies of the head, each with ONE change of the round reverted (ansi = colour codes kept; lf = only `\n` ends a line; htp = htpasswd letters lower-cased again; m3 = this round's list additions removed), and a fifth with all four reverted; a loss belongs to the change whose revert brings the family back.
| Texts | Seed | Flagged old → new | WHOLE (flagged → Clean) | Cause of each WHOLE |
|---|---|---|---|---|
| 200 000, the first check's generator | `0x0a5c0ffee5eed001` | 130 513 → 130 984 | 258 | htp 258 |
| 100 000, the first check's generator | `0x0e2c0ffee5eed002` | 65 392 → 65 605 | 144 | htp 144 |
| 250 000, my generator rich in CR, `\r\r\n`, U+0085, U+2028, U+2029, `>`/`> `/`>>`, `ESC [` codes (complete, unterminated, nested, with a listed character inside), `ESC ( B`, OSC, lone ESC, and the newly listed invisibles, inserted INSIDE family pieces and glued before them | `0x0e2c0ffee5eed003` | 136 900 → 157 471 | 1 005 | htp 314 (+3 mixed) · ansi 465 · lf 178 (Base64Lines 74, PasswordArgument 104) · m3 45 · combined 3 |
| 60 000, PEM header windows (the area of the builder's own regression): every separator above between `-----BEGIN`, 0-124 blanks and `PRIVATE`, leads `key:`/`> `/colour/backtick | `0x0e2c0ffee5eed004` | 51 317 → 52 183 | **0** | — (0 families lost either) |
| **610 000** | | | **1 407** | |
Family-level losses on the first check's generator: only PasswordArgument by htp (1 249) and one Base64Lines by lf. **On the first check's generator, nothing outside item 5 turned Clean.** Every loss is attributed (0 unattributed).

**Each class judged:**
| Class | Example (made up) | b0835a9 → head | Judgement |
|---|---|---|---|
| **htp** (item 5) | `htpasswd -B f u QCH3N9` (the first check's generator writes `-B` without `-b`) | PasswordArgument → Clean | **Ruled and right**: without `-b` htpasswd takes no password argument. |
| **lf, base64** (item 2) | `UUFGQUtFMDAwMXF1\r\r\nUUFGQUtFMDAwMnF2\r\r\nUUFGQUtFMDAwM3F3`; also `\r \r\n`, `\r\t\n`, `\r\r\r\n` | Base64Lines → Clean | **A real shape lost, as a side effect of the rule as written** → Note **N-R1**. The first CR of `\r\r\n` counts as "lone" (`families.rs:125`), so the text is three lines with EMPTY lines between: not adjacent. `\r\r\n` is the usual result of converting CRLF text a second time (Windows). Only short-wrapped base64 (12-23 per line, or lines without the letter/digit mix) is lost: 64-column lines are still LongToken (TESTED: `64-wide x2 with CR CR LF` → LongToken). |
| **lf, netrc** (item 2) | `machine h\u{2028}login u password qapw0001`, `machine h\rlogin u password …\n` | PasswordArgument → Clean | Consistent with the ruled line ends: `machine` is now on another line and `password` is not alone on its line; with LF in those places `b0835a9` is Clean too. A multi-line `.netrc` (`password x` alone on its line) is flagged with every line end. → Note **N-R3**. |
| **ansi** (item 3) | RE-1 `\u{1b}[0123456789ab\u{200b}cdef0123` (the code eats `0123456789a`); RE-3 `0a1b2c3d\u{200b}4e5f60718293\u{1b}[0mzz` (removing the reset glues the run to `zz`); `\u{1b}\u{1b}[-----BE\u{2066}GIN private key-----…` (the code `ESC [ ----- B` eats the start of the header) | HexRun / PrivateKey → Clean | Family-level 1 487 losses: **173 real shapes** (b0835a9 still finds the shape when each code is replaced by a space; 120 HexRun, 21 AuthHeader, 20 SecretAssignment, 5 AuthScheme, 5 PasswordArgument, 2 KnownToken) and 1 314 artefacts (the old match took the code's own bytes as the value, e.g. `--api-key \u{1b}[31m`). **Every real one needs BOTH a listed invisible character inside the shape (so the raw view misses) AND a colour code glued to it** (the raw view is unchanged by the round, so a loss can only come from the stripped view). A deliberate construction; ordinary coloured output has no invisible characters inside tokens. Side effect of "in the stripped view remove …": the format-only view of `b0835a9` is gone → Note **N-R2**. |
| **m3** (item 4) | `g\u{fffb}E5aA84EbD\u{2066}F7f4639`, `Q\u{180d}xo\u{2066}xa-vmts7znfZkY` | HexRun / KnownToken → Clean | **Artefacts**: the newly listed character was the only "boundary" in `b0835a9`'s stripped view; a reader sees `gE5aA84EbDF7f4639` / `Qxoxa-…`, a run glued to a letter (a documented known miss). Same class as round 1's N1. |
| combined | htpasswd `-B` + codes + invisibles | | the above together |

**PEM (the builder's own regression area):** 0 losses in 60 000 targeted texts and 0 PrivateKey losses in 550 000 others outside the ansi class (97 PrivateKey family losses are all ansi: a code eating the `-----BEGIN` bytes in a header that also holds a listed invisible). The fix in `1096a77` holds.

**Base differential** (the first check's `qa_diff.rs` + `qa/`, unchanged, release, on the head):
```
qa_diff: seed 0xa5c0ffee5eed001, 400000 texts; base redactor masks something in 249573; scan Clean in 138241
qa_diff: texts the base masks and scan calls Clean: 3
PrivateKey 55773/0/0 · UrlCredentials 50247/0/4 · AuthScheme 55522/0/223 · AuthHeader 52301/0/36 · SecretAssignment 120549/8/777
PasswordArgument 14993/0/41439 · KnownToken 42678/0/1 · LongToken 74355/0/74 · HexRun 25626/0/3 · Base64Lines 6767/0/390   (base matched / scan missed / scan-only)
qa_diff: family misses explained only by the strip-list difference: 8; misses where the base rule matches a scanner view: 0
```
**0 real misses.** The 8 (3 whole) are the same texts as round 1's N1: the 11 example lines printed are byte-identical to the round-1 log (`diff` empty). The builder's STATUS figures match mine exactly.

## 5. m1, m2, m3 and item 5 — TESTED
The first check's cases, re-run on the head (`qa_hide.rs`, `qa_probe.rs`): `qa_hide` Clean cases **165 → 43**. The 43 left: U+2065 (unassigned, docs §4) ×24, "split across two lines" ×3, "base64 of it" ×1 (both docs §4), and 15 rows where round 1's 2-line base64 fixture shares its lines with prose (not a base64-lines shape; round 1 judged the same). Every lone-CR, `> `, NEL/LS, after-ANSI and named-invisible row of round 1 now flags. `qa_probe`: the four m1 rows (16-wide base64 with lone CR, `> `; `.netrc` lone CR) flag; JSON-escaped base64 stays Clean (ruled, docs §4); `\u{1b}[32mBearer qaB0001` and the 20-digit hex after a colour code flag.

**m1, line shapes** (`qa_r2.rs::r2_m1_line_shapes_hostile`, old → head):
| Input (made up) | b0835a9 | head | Judgement |
|---|---|---|---|
| base64 ×4, LF + CR + NEL mixed in one text | Clean | Base64Lines | fixed |
| base64 ×4, CR + LS + CRLF mixed | Clean | Base64Lines | fixed |
| base64 ×3 joined by `\r\r\n` | Base64Lines | **Clean** | **N-R1** (round opened it) |
| base64 ×3 joined by `\r \r\n` / `\r\t\n` | Base64Lines | **Clean** | N-R1 |
| base64 ×3, CRLF, with and without a final CRLF | Base64Lines | Base64Lines | holds |
| two 64-column base64 lines joined by `\r\r\n` | LongToken+Base64Lines | LongToken | still flagged (real key widths) |
| base64 ×3 joined by U+2029 / VT+FF | Clean | Clean | not in the ruled list (Note N-R4) |
| `>` glued, `> ` with CR ends, `>\t>\t` nested | Clean | Base64Lines | fixed |
| `>` inside a base64 line (`UUFGQUtF>MDAw…`) / at line ends | Clean | Clean | a marker only counts at the line start: right |
| markdown list `- ` first line + indented lines | Base64Lines | Base64Lines | holds |
| JSON `\n` escapes | Clean | Clean | ruled, docs §4 |
| a colour code at each line start | Clean | Base64Lines | fixed (stripped view) |
| `.netrc` CR, NEL, LS mixed in one text | Clean | PasswordArgument | fixed |
| `.netrc` `machine h\rlogin u password x\n` (one LF line) | PasswordArgument | **Clean** | N-R3 (ruled line ends; with LF there b0835a9 is Clean too) |
| `.netrc` `machine h\u{2028}login u password x\n` | PasswordArgument | **Clean** | N-R3 |
| `.netrc` `\r\r\n` line ends, password alone on its line | PasswordArgument | PasswordArgument | holds |
| `>password x`, `\rpassword x`, `password x\rmore` | Clean | PasswordArgument | fixed |
| `password >qapw0001` (a `>` that is part of the value) | PasswordArgument | PasswordArgument | the value keeps its `>`: right |
| `a>password x` mid-line | Clean | Clean | right (not a line start) |
| prose `> password policy` alone on a quoted line | Clean | **PasswordArgument** | new over-flag of the quote-marker rule; the same line WITHOUT `> ` flagged before too (the "alone on its line" rule) → Note N-R4 |

**m2, colour codes** (`r2_m2_ansi_hostile`):
| Input (made up) | b0835a9 | head | Judgement |
|---|---|---|---|
| round 1's `\u{1b}[32mBearer qaB0001\u{1b}[0m`, 20-hex after `\u{1b}[33m` | Clean | AuthScheme / HexRun | fixed |
| `\u{1b}[\u{1b}[31mBearer …` (nested), `\u{1b}[1m\u{1b}[31m…` (two glued), `\u{1b}[38:5:208m…`, `\u{1b}[?25l…`, `\u{1b}[2A…`, `\u{1b}[1 q…` | Clean | AuthScheme | fixed |
| an ESC sequence with no end: `\u{1b}[1;` alone, `\u{1b}[` alone, `Bearer qaB0001 \u{1b}[1;2;` | — | kept, no panic | ruled ("no final byte → kept") |
| `\u{1b}[3\u{1b}[1mBearer …` (overlapping: the first has no final) | Clean | Clean | the unfinished `\u{1b}[3` stays and glues `3` to `Bearer`; ruled form → Note N-R2 |
| `\u{1b}[1;2;3Bearer …` / `\u{1b}[1Bearer …` | Clean | Clean | the `B` IS the final byte (a cursor move), so the code eats it, as a terminal would; not a documented shape |
| ESC inside a secret: `0a1b2c3d4e\u{1b}[0m5f60718293` | Clean | HexRun | joins a split true one (fine) |
| ESC inside a flag name `--pass\u{1b}[0mword hunter22` | Clean | PasswordArgument | joined |
| false joins: `deadbeef01\u{1b}[0m23456789 ok`, `build2024\u{1b}[1mStatusOKfinal99` | Clean | HexRun / LongToken | **new over-flags** of joining (coloured output whose halves happen to form a run) → Note N-R4 |
| RE-1 `\u{1b}[0123456789ab\u{200b}cdef0123` | HexRun | **Clean** | **N-R2** (round opened it) |
| RE-1 without the ZWSP (control) | HexRun | HexRun | raw view catches it |
| RE-3 `0a1b2c3d\u{200b}4e5f60718293\u{1b}[0mzz` | HexRun | **Clean** | **N-R2** |
| a listed character inside the code: `\u{1b}[3\u{200b}2mBearer …`, `\u{1b}\u{200b}[32mBearer …` | Clean | Clean | m2 reopened by one inserted invisible: the code is recognised before the ZWSP is removed → Note N-R2 |
| `\u{1b}(BBearer …` | Clean | Clean | ruled, docs §4 |
| 8-bit CSI U+009B | Clean | Clean | not in the ruled form (Note N-R4) |
| PEM / netrc / htpasswd behind a colour code; colour inside a PEM header | flagged | flagged | holds |

**m3, every newly listed invisible at every position** (`r2_m3_every_position`): 26 characters (all 22 the round added, 0601-0604 and FFFA/1BCA1-2 included, plus E0001) × every character boundary of 12 short secrets (one per family + netrc + htpasswd) = **10 946 cases, 0 missed** (each still named by its own family). The first check's 780 insertions (t09) green.

**Item 5, htpasswd letters** (`r2_item5_htpasswd_letters`): 12 letters (`b B c C n m d s p D v i`) alone, every ordered pair, and every ordered triple of `b B c n`, each with and without a password after = **336 cases; flagged exactly when the letters hold a lower-case `b`; 0 wrong.** Also `HTPASSWD -B f u`, `` `htpasswd -B f u` ``, `htpasswd -C 10 -B f u` → Clean (were flagged); `htpasswd -B -b f u x`, `(htpasswd -Bb f u x)`, `htpasswd -nbB u x` → flagged.

## 6. Bounds, panics, time; nothing of the input in a verdict; pure and alone — TESTED
- **Builder's own tests in my clone** (debug, own empty target dir, `cargo test --locked -p coagent-scanner --test t01_flagged … --test t09_fix_round`): t01 10, t02 1, t03 2, t04 1, t05 2 (incl. the 31 timed shapes under 150 ms), t06 1, t07 1, t08 1, t09 6 → **25 passed, 0 failed**. `cargo fmt --all --check` on the pristine head → exit 0, no output. `cargo clippy --locked -p coagent-scanner --all-targets -- -D warnings` (pinned 1.100.0, own target dir) → exit 0.
- **The first check's property file** (`qa_props.rs`, seed `0x51c0de0000000002`, every case scanned twice under `catch_unwind`, `Debug` rebuilt from (kind, count) and compared exactly, every `text()` one of the fixed sentences): **release 300 000 cases, no panic, deterministic, Debug == kinds+counts for all** (104.9 s); **debug, the same 300 000, no panic, identical reach** (695.9 s, 21:09:45-21:21:22). Reach vs round 1: PasswordArgument 77 516 → 87 369, Base64Lines 3 958 → 4 407, Clean 97 501 → 97 133; the other nine numbers identical (PrivateKey 89 622 … TooLarge 484). Largest count 10 878 (unchanged). Slowest single scan 9.95 ms release / 42.2 ms debug. `qa_digits_and_counts`: no input digit run of 3+ in any Debug. Its 36 hostile shapes: worst 41.84 ms debug, 7.99 ms release. `qa_scale` (8 shapes, release): 64K/8K = 7.3-8.1. `qa_probe_bound_edges`: all bound rows as in round 1 (65 536 scanned, 65 537 TooLarge, multi-byte characters across the bound TooLarge).
- **My shapes for the new code** (`qa_r2.rs::r2_hostile_timed` and `r2_hostile_doubling`, 64 KiB each, smallest of five, each under `catch_unwind`: no panic):

| Shape (new code it hits) | debug ms | release ms | 64K/8K debug · release |
|---|---|---|---|
| `ESC [` + one 64 KiB digit run, no final (stripper) | 38.79 | 5.23 | 8.0 · 8.0 |
| `ESC [` + one 64 KiB intermediate run `!!!…`, no final | 35.20 | 4.61 | 8.2 · 7.9 |
| `ESC [` repeated | 36.13 | 4.61 | 8.0 · 8.1 |
| ESC repeated | 17.08 | 2.26 | 8.0 · 8.0 |
| `ESC [0` repeated (each ends at the next ESC) | 45.77 | 6.41 | 8.1 · 7.8 |
| `ESC [` + `0 0 0 …` (parameter after intermediate: no final) | **50.32** | **7.25** | 8.0 · 7.9 |
| `ESC [12` + ZWSP repeated (sequence kept) | 31.99 | 4.34 | 7.8 · 7.4 |
| colour code + 16 hex repeated | 35.83 | 4.96 | 8.1 · 7.8 |
| `\r\r\n` repeated (line ends) | 18.80 | 2.35 | 8.1 · 8.1 |
| U+0085 repeated / U+2028 repeated | 17.68 / 17.60 | 2.29 / 2.16 | 8.2 · 7.9 / 8.1 · 7.6 |
| `>` × 64 Ki on one line (quote markers) | 17.18 | 2.33 | 8.1 · 7.8 |
| `> ` + base64 line, alternating | 20.13 | 2.72 | 8.1 · 7.7 |
| 500 × `>` then `password x`, repeated lines | 17.53 | 2.36 | 8.0 · 7.6 |
| `>password x ` repeated on one line | 22.24 | 3.21 | 8.5 · 7.6 |
| `password x\r` repeated | 21.43 | 3.14 | 8.2 · 7.7 |
| `machine h\rpassword x ` repeated (general lines + `machine` cache) | 22.39 | 3.37 | 7.9 · 7.7 |
| `(--key "` repeated (new flag starts, quoted values) | 24.42 | 3.81 | 8.0 · 7.6 |
| `(--key '(--key "` alternating | 24.76 | 3.76 | 8.0 · 7.7 |
| `(-u a:b)` repeated | 28.10 | 3.50 | 8.0 · 7.9 |
| `mysql ` + `(-p` repeated (glued `-p`) | 26.66 | 3.73 | 8.0 · 7.8 |
| `x(-` repeated (a flag start every 3 bytes) | 26.63 | 3.61 | 8.1 · 7.8 |
| `htpasswd ` + `` `-Bb `` repeated | 26.84 | 3.32 | 7.7 · 7.7 |
| U+1BCA0 repeated (4-byte listed) | 16.47 | 2.15 | 7.9 · 7.9 |
| `a` + U+17B4 repeated | 24.80 | 3.53 | 8.1 · 8.2 |
| `0`+U+0600+`a`+U+0600 repeated | 28.36 | 4.02 | 7.9 · 7.9 |
| colour + U+180B + CR + `>` mixed | 23.42 | 3.01 | 8.1 · 7.8 |
Worst 50.32 ms debug (the builder's limit is 150 ms), 7.25 ms release; doubling the input doubles the time everywhere (7.4-8.5 per 8×). READ agrees: line terminators and line starts are computed once per text (`families.rs:150-169`); `stripped_view` advances past every byte it looks at, and an unfinished sequence is re-read at most once (`lib.rs:184-213`); `machine` is cached per general line. **No panic, no hang, no super-linear work.**
- **Nothing of the input in a verdict.** READ: the round did not touch `Finding`, `Verdict`, `Kind`, `text()` or `Debug` (the `lib.rs` diff is `is_format_char`, `stripped_view` and the second-scan condition). TESTED: the rebuild comparison above, 300 000 × 2 builds.
- **Pure and alone.** `crates/coagent-scanner/Cargo.toml` unchanged by the round (0 bytes); `cargo tree --locked -p coagent-scanner -e all` → the crate alone; `-i` → no dependant. My grep of `src/` for `std::`, `core::`, `alloc::`, `static mut`, `include!`, `#[path`, `unsafe`, print macros, `use ` → only `#![forbid(unsafe_code)]` and `use crate::{Kind, VERDICT_FAMILIES};`. **No `std::`, `core::` or `alloc::` path in `src/`; no dependency.**

## 7. The red controls — TESTED
`bash scripts/red-controls-scanner.sh` once, from my SECOND clone at `1096a77` (`git status` empty, so my QA files stayed out of its green run), started by Python `subprocess` with `cwd` = that clone's root so the command line is exactly `bash scripts/red-controls-scanner.sh` (`heavy_runs.sh --list` showed it as 1 job; 0 jobs before it), own `COAGENT_TOOLS`, target, log and scratch dirs under my work dir. Exit 0:
```
names: 18 red controls, each in build.rs, used under src/ and a row
no_pem … no_base64_lines   P1  RED  (each: t01 exactly its own test failed; evidence as in round 1, e.g. "AuthHeader did not flag its positive "authorization": Flagged([SecretAssignment])")
flag_everything            P2  RED  t02: ordinary text "prose" was flagged: Flagged([LongToken])
reason_echoes_text         P3  RED  t04: a reason quotes the input (short body lines): window "----" of "…echo: \"-----BEGIN PRIVATE KEY-----…"
prefix_window              P4  RED  missed at: ["ends exactly at the bound", "begins just after the half", "straddles the half"]
quadratic_line_end         P5  RED  over the 150ms limit: -----BEGIN 339 ms, Cookie: 489 ms, key=" 416 ms, -p on a mysql line 1.12 s, …
slice_mid_char             P6  RED  scan panicked on generated case 2 (seed 0x5ca90c0a6e700001): start byte index 42 is not a char boundary
flag_after_space_only      M1  RED  M1: a wrapped password flag was not seen (130 of 240): ["backticks: "`--password hunter22`"", …]
line_end_lf_only           m1  RED  m1: a line shape was missed with a non-LF line end: ["base64 lines, lone CR", "netrc, lone CR", "base64 lines, NEL", "netrc, NEL", "base64 lines, LS", "netrc, LS"]
ansi_kept                  m2  RED  m2: a shape glued to a colour code was missed: ["bearer short after ANSI", "hex 20 after ANSI", "flag after bold", "256-colour code"]
rows: 18 cfg rows
planted std::env           P7  RED  t07: the scanner source names a forbidden item: ["lib.rs:273: std::env", "lib.rs:273: std:: path"]
GREEN: 25 tests ok · RED CONTROLS OK
```
- **Each new row red for its own reason (READ of the three new `cfg` branches):** `flag_after_space_only` (`families.rs:577-579`) returns "ASCII whitespace only", exactly the copied rule → the 126 round-1 cases + the 4 extras are missed ("130 of 240" counts the extras against the 240: cosmetic). `line_end_lf_only` (`:124`) makes every byte but `\n` a non-terminator → exactly the six base64/netrc cases with CR, NEL, LS fail; the PEM cases in the same test pass (PEM never used the new line ends), which shows the row is about the line rule only. `ansi_kept` (`lib.rs:190`) skips the code removal → exactly the four colour-code cases fail. All 15 round-1 rows and the planted row are still red with the same evidence.
- **Release refuses** (own target dir): `COAGENT_SCANNER_RED=<each of the 3 new names> cargo build --release -p coagent-scanner` → exit 101, `build.rs:51` "COAGENT_SCANNER_RED is for test builds only"; `bogus` in a debug build → exit 101 "is not a known red control"; release without the variable → exit 0, no marker.
- **No red branch reachable in a normal or release build (READ):** 21 sites under `src/` (18 `cfg!(coagent_scanner_red = "…")`, one per name, + the 3 `#[cfg]` attributes of round 1's `echo` field). `cfg!` is the constant `false` unless rustc gets `--cfg coagent_scanner_red=…`, which only `build.rs` emits, only after the release refusal.

## 8. The docs and the owner's table — READ + TESTED
`qa_r2_docs.rs` (release): one row per sentence or table row of `docs/SCANNER.md` the round changed or added: §2 PasswordArgument cell (htpasswd letters; the M1 start rule incl. "not after a letter / `/`"), the format + terminal-code paragraph (a DI character, U+0600, U+FFF9, colour code, cursor move, intermediate-byte form, "no final byte → kept"), the lines paragraph (lone CR, NEL, LS, CRLF once, `>>` markers, netrc with lone CR and behind `> `, PEM with LS line ends, the PEM `\n` window), the three new §4 misses, and every added §5 row incl. `htpasswd -B` now clean: **55 rows, 0 mismatches** (two first-run mismatches were my own fixtures: `Authorization: Negotiate x` is AuthHeader AND SecretAssignment, and `` `--token-file t.txt` `` alone is PasswordArgument only, exactly as the docs row says; corrected). The first check's `qa_docs.rs` (80 rows of round-1 docs) → **80 rows, 0 mismatches** on the head; its `qa_builder_overflag_table` green.
- **The "still missed" list (§4) is true** (each pinned Clean in `t03::known_misses_pass_as_clean`, green; and re-tested above). **It is not complete** for what this check found: `\r\r\n`-separated short base64 (N-R1), a shape that holds a listed invisible AND touches a colour code (N-R2), a flag after a JSON `\n` escape or as an argv array element (N-R5), U+2029/VT/FF line ends and the 8-bit CSI U+009B (N-R4). The docs' catch-all "Anything in a format not listed above passes too" covers them only loosely.
- **The added over-flag rows are confirmed** (55 rows above, each by the family the table names). My corpus adds 20 more names of the same row's kind (§3).
- Docs §2 "the differential lost 6 headers when it was tried" is about `8fe7faf`: UNVERIFIED by me (not rebuilt). Docs §3 timing table, the 9 new rows: re-measured in my debug build (`t05_bounds::hostile_shapes_are_fast --nocapture`): 22.01 / 32.48 / 47.65 / 50.86 / 20.04 / 20.41 / 21.31 / 17.51 / 24.41 ms, 16 KiB message 5.55 ms: each within 0.4 ms of the docs.

## 9. Names and ids — TESTED
Tool outside the repo (`/private/tmp/claude-501/qsc2/qa_tools/namescan.py`, the first check's tool unchanged; copy in `gate_scanner_core_r2_tests/`), `python3 -B -I`, the words passed on the command line only (25: owner name parts, account handle and the login name read at run time, mail domains, the machine name and host name read at run time, the home path read at run time, workspace drive and folder names, coordinator and client names, `/Users/`, `/Volumes/`, `/private/tmp`, the temp user folder, the mail service), each in up to 10 spellings, plus id shapes and real-looking keys.
- Over the round's **new file** (`t09_fix_round.rs`, whole) and **all 420 lines the round adds** to the other 11 files: `scanned 2 files, 48 spellings of 25 words: 0 word hits`; `ID` ×2: `deadbeef-0002-4000-8000-00000000f00d` (the builder's made-up UUID, in t03 and docs §5); `KEY?` ×0.
- Positive controls: a scratch copy of `t09_fix_round.rs` with one planted line (login name + machine name) and a planted binary (`\x00\x01BIN<home path>\x00\xff toolu_…`): `13 word hits` + the `toolu_` id. Both found.
- **Nothing of the owner's** in what the round adds.

## Findings
**No Blocker. No Major.** Repro files are in `gate_scanner_core_r2_tests/`. To run one: in a clone at `1096a77`, copy `qa_r2*.rs`, `qa_old/`, `qa_var_*/` and the first check's `qa/` folder into `crates/coagent-scanner/tests/`, then run the command.

**How I graded the regressions (read this first).** Brief §3 puts "a new miss the round opened" in the NO GO class. The round did open three narrow ones (N-R1, N-R2, N-R3). Each one follows from the WORDS of a ruled item in Friday's closed list: item 2 says "a lone carriage return … ends a line", and item 3 says "in the stripped view remove …". The list did not let the builder go beyond those words (anything else was to be a `STOP`), and the builder implemented them exactly. Brief §1 says a closed-list item that looks wrong is a Note with evidence. So I raise them as Notes with their evidence and a one-line fix each. On the first check's generator (300 000 texts) none of them occurs. They need short-wrapped base64 with doubled CRs (N-R1), or a deliberately built text with an invisible character inside a token next to a colour code (N-R2). **If Friday reads §3 strictly, N-R1 and N-R2 are Majors and the verdict is NO GO.** I do not, for the reasons above.

**N-R1 (Note, regression that follows from item 2's words): short base64 lines separated by `\r\r\n` (or `\r` + blank + `\n`) are no longer flagged.**
- File: `crates/coagent-scanner/src/families.rs:125` (`b'\r' if b.get(i + 1) != Some(&b'\n') => 1`). The first CR of `\r\r\n` counts as lone, so the text gets an empty line between every two lines, and `base64_line_blocks` (`:850-860`) then sees them as not adjacent.
- What happens: `UUFGQUtFMDAwMXF1\r\r\nUUFGQUtFMDAwMnF2\r\r\nUUFGQUtFMDAwM3F3` → `b0835a9` Base64Lines, head **Clean**. The same with `\r \r\n` and `\r\t\n`. There are 74 such whole texts in my rich generator. `\r\r\n` is what CRLF text becomes when it is converted a second time (a common Windows artefact). Lines of 64/76 columns are still caught as LongToken. Only short-wrapped base64 is lost.
- Repro: `cargo test --locked -p coagent-scanner --release --test qa_r2 -- --nocapture r2_m1_line_shapes_hostile 2>&1 | grep -E "CR CR LF|CR space|CR tab"` → three rows `old Base64Lines | new CLEAN`.
- Suggested fix: count a run of CRs (and blanks) that ends in `\n` as ONE line end. Or let a line holding only CR/blanks not break a base64 block. Add the three texts to `t09::m1_line_ends` as positives.

**N-R2 (Note, regression that follows from item 3's words): one stripped view now removes invisibles and colour codes together, so `b0835a9`'s invisibles-only view is gone. A code can eat bytes of a shape, or glue the shape to a word, that the old view still saw.**
- File: `crates/coagent-scanner/src/lib.rs:184-213` (`stripped_view`) and `:235`.
- What happens: `\u{1b}[0123456789ab\u{200b}cdef0123` → `b0835a9` HexRun, head **Clean**: the code `ESC [ 0123456789 a` eats the start of the run, and the ZWSP splits the raw view. `0a1b2c3d\u{200b}4e5f60718293\u{1b}[0mzz` → HexRun → **Clean** (removing the reset glues the run to `zz`). `\u{1b}\u{1b}[-----BE\u{2066}GIN private key-----…` → PrivateKey lost. Across 250 000 hostile texts: 173 real-shape family losses, and every one of those texts also holds a listed invisible INSIDE the shape. Related, not a regression: one invisible character inside or right after the ESC (`\u{1b}[3\u{200b}2mBearer …`, `\u{1b}\u{200b}[32m…`) brings m2 back, because codes are recognised before invisibles are removed.
- Repro: `cargo test --locked -p coagent-scanner --release --test qa_r2 -- --nocapture r2_m2_ansi_hostile 2>&1 | grep -E "RE-1|RE-3|listed char"`.
- Suggested fix: run the families on three views: raw; invisibles removed (as at `b0835a9`); invisibles removed FIRST and THEN codes removed. The work stays linear (one more pass). Add RE-1, RE-3 and the ZWSP-inside-the-code cases to `t09::m2_ansi_codes`.

**N-R3 (Note, ruled line ends): a `.netrc` `machine` that shares a `\n` line with `password` but sits behind a lone CR, U+0085 or U+2028 no longer counts.** `machine h\u{2028}login u password x` → was PasswordArgument, now Clean. 104 whole texts in my rich generator. This is what the ruled line ends mean: with LF in those places, `b0835a9` is Clean too. A real multi-line `.netrc` (`password x` alone on its line) is flagged with every line end. No change needed. The docs could add one line.

**N-R4 (Note, for the docs and the owner's table): new over-flags and edges.** (a) A quoted prose line `> password policy` now flags. The same line without `> ` flagged before, because of the "alone on its line" rule. (b) Joining across a removed code can make a false run: `deadbeef01\u{1b}[0m23456789 ok` → HexRun, `build2024\u{1b}[1mStatusOKfinal99` → LongToken. (c) Not in the ruled form, so still Clean: U+2029, VT and FF as line ends, and the 8-bit CSI U+009B.

**N-R5 (Note, existed before the round, not in docs §4): password-flag forms that are Clean on both heads.** An argv array `["--password", "hunter22"]` / `"--password", "hunter22"` (the value follows `", "`, not a blank). `` `--user=qauser:hunter22` ``. A flag right after a JSON `\n` escape (`"…a\n--password hunter22"` as written in JSON: the `n` is a letter, which the ruled start rule excludes). Suggest listing them under §4, or a later lane.

**N-R6 (Note, N3 word list):** `t07_pure` matches the literal text `use std as`. It does not catch `use ::std as s;`, `use  std as s;` (two spaces), `use {std as s};`, or an alias split across lines, and after such an alias the path rule does not see `s::env::var`. None of these is used today (my grep). Suggest a token-level rule: any rename whose source is `std`, `core` or `alloc`, and any path that starts with `::std`.

**N-R7 (Note, for the owner): over-flag rates** (§3). Plain chat and report lines are unchanged: 0 new flags in 288 sentences (2.6 % / 28.3 %). A message that names a key/token/auth/session/secret/pass/private/cookie/signature/credential/pw-type option in backticks or brackets, followed by a word, now flags: 29 of my 100 such sentences newly flag (4 % → 33 %). Ordinary option names add 0.

**Cosmetic:** the M1 red row's evidence says "130 of 240", which counts the 4 extra wrappings against 240.

## What was NOT checked
| Not checked | Why / what would check it |
|---|---|
| `scripts/check.sh` whole (workspace fmt/clippy/test/deny) | the brief says not to run it whole (Friday's merge check runs it). I ran `cargo fmt --all --check`, the crate's clippy with `-D warnings`, and the crate's tests (all exit 0) |
| `8fe7faf` itself (the builder's 6 lost PEM headers) | not rebuilt. At the head, my PEM-window differential shows 0 losses, so the figure does not affect the verdict |
| `DerivedCoreProperties-18.0.0.txt` re-read | no network beyond `cargo fetch --locked`. I checked the list against the Default_Ignorable set as published in Unicode 15/16 from my own knowledge (405 code points, all present) |
| Real agent traffic | every corpus here is mine or the first check's; real rates may differ either way |
| Linux and Windows builds | macOS only; the round adds no OS code. `\r\r\n` (N-R1) is the Windows-relevant case |
| Mutation testing beyond the 18 red rows | not asked |
| The red script's names check fed a deliberately mismatched name | read only; it passed on the real tree with 18 names |
| How SCANNER-WIRE will show a flag or count | later lane |
| Timing on an idle machine | the counter read 0-2 other heavy jobs during my timed runs; numbers are upper bounds |

## Process notes (QA seat)
- Work dir `/private/tmp/claude-501/qsc2`: `clone/` (my QA files added under `crates/coagent-scanner/tests/`, never committed), `clone_red/` (pristine, for the red script, fmt and clippy), own target dirs (`target`, `target_rel`, `target_red`, `target_relchk`, `target_clippy`) and cargo home (`tools/cargo` with `bin` and `rustup` linked to the project's toolchain, as `coagent_merge_check.sh` does). All cargo runs used `--manifest-path` (no `cd`), with `RUSTUP_TOOLCHAIN=1.100.0`.
- The old scanner (`b0835a9`) ran beside the head in the same test binary: its `lib.rs`/`families.rs` were copied from git into `tests/qa_old/`, changing only `use crate::` → `use super::`. The four "one change reverted" copies of the head (`tests/qa_var_*`) each differ from the head by the one line or list named in `qa_r2_attr.rs`.
- In the project repo I used only `git --no-optional-locks` read verbs. I touched no worktree, target dir or scratch folder of the builder, nor the first check's work dir. Network: `git ls-remote`/`fetch` from GitHub (deploy key) and `cargo fetch --locked` only. No model run.
- **A slip:** early on, one status-helper command of mine wrote a one-line scratch file into `/tmp` (outside my work dir). I moved it into my work dir (`stray_tmp_file_moved_from_tmp.txt`); nothing was deleted.
- Copies of every file I wrote and every log are in `gate_scanner_core_r2_tests/` (the planted name-scan controls and their log are NOT copied, because the tool prints the matched spelling and they hold the planted names; the log was moved back to my work dir and a README with its summary line left in its place). The logs hold random token-shaped strings from the generators, all made up.
