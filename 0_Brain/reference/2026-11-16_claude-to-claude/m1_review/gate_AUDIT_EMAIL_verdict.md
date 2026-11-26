VERDICT: GO WITH NOTES — head e31b29ac78fc19c6fc3c8fb206d44e2e91d7877c

# QA-AUDIT-EMAIL: independent check of branch `audit-email`

Head `e31b29ac78fc19c6fc3c8fb206d44e2e91d7877c` (one commit, parent `5e11609cee1cb483bd006547e9092d49522691cc`). Every comparison is against `5e11609`. Main (`5cab5e42df6cb3db05f3d38c7ba973beafd044b2`) was not merged or judged.
Brief: the coordinator's `briefs_drafts/2026-11-26_coagent_QA-AUDIT-EMAIL_check_brief.md`. Checked 2026-11-26 on this laptop, project toolchain linked into `/private/tmp/claude-501/qae/tools`; every build in its own empty target dir under `/private/tmp/claude-501/qae/`.
Tags: TESTED = I ran it; READ = I read it. Every script, harness, plant diff and log is in `m1_review/gate_audit_email_tests/` (index at the end).

## BLUF

1. **Is every address the owner would expect blanked now blanked?** Mostly. In my own corpus (8,172 planted addresses in 70 real-looking placements plus every older rule's input as a neighbour) the base leaves 6,978 visible in a preview and the head leaves 1,294. Every one of those 1,294 falls in a class the lane's documents list. But three of those classes come from **the coordinator's rule as ruled (R-1)**, and the owner would meet two of them in ordinary text: **an address inside a URL** (`https://x.example.com/c?to=<address>`: the whole URL is skipped, and the URL rule does not mask a query address) and **an address followed by `:` and a non-space** (`git log --format=%ae:%s` lines, colon-keyed keys `user:<address>:profile`). The third class is an address with more domain characters glued on (`<address>9f86…`, `<address>-1`, `<address>-----BEGIN…`).
2. **Does every other rule answer as before?** Yes. My own differential over 28,962 inputs (seed `0x0ae5eed`) has 0 unattributed differences. Every other function and constant of `redact.rs` is byte-identical, and `find` only gains lines. Every planted regression I tried is reported, except one that equals the base by construction (see (e)).
3. **What is still not blanked, and how often?** The URL-token and colon classes, the glued-after class, non-ASCII addresses, encoded or spelled-out forms, and the 64 KiB window end. Each is listed below with its count in my corpus. A scratch "longest valid prefix" variant removes 799 of the 1,679 glued and colon survivors in my glued corpus. It changes no listed not-an-address answer and stays linear.
4. **Do the records tell the truth?** Nearly. Old logs are kept byte for byte (shown with a real base daemon), and the format is unchanged. Four wording faults, all Minor: one false example (`alice@bücher.example` "keeps `alice@b`": the whole address is kept); the colon exclusion described only as "an scp or ssh target"; "left to the URL rule" for URL tokens; and summaries attached to the owner's ruling. Two code branches have no test that goes red when they are reverted (case-insensitive `xn--`, trailing `-` trim).

**Verdict for the lane's work: GO WITH NOTES.** No Blocker or Major lies against what the lane built. The URL-token and colon classes are findings against the coordinator's rule, as section 8 ruling 11 asks. The lane documents both (the doc comment states the rule exactly), so section 3 and ruling 5 do not make them a NO GO. The coordinator decides the rule on the figures in (b) and (c).

## Proofs (section 0)
- TESTED `git ls-remote` (GitHub remote, deploy key): `e31b29ac78fc19c6fc3c8fb206d44e2e91d7877c refs/heads/audit-email`, `5cab5e42df6cb3db05f3d38c7ba973beafd044b2 refs/heads/main`.
- TESTED `git log --format='%H %P' 5e11609..e31b29a` → one line `e31b29ac78fc19c6fc3c8fb206d44e2e91d7877c 5e11609cee1cb483bd006547e9092d49522691cc`. `git merge-base e31b29a 5cab5e4` = `5e11609…`.
- TESTED builder's STATUS `wc -lc` = 1059 lines, 101,212 bytes. It ends with `Head: e31b29ac78fc19c6fc3c8fb206d44e2e91d7877c (branch audit-email, pushed)` and then `READY FOR QA AUDIT-EMAIL`.
- TESTED `git show --stat`: 8 files, 976 insertions, 3 deletions; numstat as the coordinator's (`docs/AUDIT.md` 13/3).

## Section 1a: my judgement of each S-point
| S | Drafter's reading | My result | Where |
|---|---|---|---|
| S-1 | the scp test keeps ANY address before `:` + a non-whitespace byte | **Confirmed.** Kept whole at the head: `alice@example.com:fix the build`, `user:alice@example.com:profile`, `mail alice@example.com:thanks`, and `:` followed by `)`, `,`, `"`, U+000B, U+00A0 or a CJK character. **Wrong on one case:** `curl -u alice@example.com:secret` → `curl -u [REDACTED]` at base AND head. The older `flags` rule masks a `-u`/`--user` value that holds `:` (`redact.rs:505`), so the password half is masked too. | (b), (c), (d) |
| S-2 | the URL exclusion skips the whole token | **Confirmed.** Query, path, and glued after a URL by `,`, `)` or `;`: kept whole. With a port: `https://x.example:8443/c?to=alice@example.org` → `https://[REDACTED]@example.org` (domain kept). Without a port: kept whole. | (b), (d) |
| S-3 | the non-ASCII sentence is wrong both ways | **Confirmed, each case.** `alice@bücher.example` is kept WHOLE (not `alice@b`). `jörg@example.com` → `jö[REDACTED]`. `alice@mail.exämple.com` → `[REDACTED]ämple.com`. U+2066–U+2069, U+FE0F, U+034F before the `@` or in the domain keep the address whole; inside the local part they mask the part after them. | (d) |
| S-4 | older rules partly mask glued forms | **Confirmed.** `alice@example.com9f86d081884c7d659a2feaa0c55ad015` → `alice@example.[REDACTED]` (at base too). `alice@example.com-----BEGIN PRIVATE KEY-----` → `alice@example.com[REDACTED]`. My survivor count uses the three-part leak check, not "was an `emails` span found". | (c) |
| S-5 | summaries masked but untested; the daemon sends none | **Confirmed.** I tested it through the chain: stored masked at the head, kept at the base. A near-limit summary is refused at the head; the host returns the refusal unchanged. Older rules already grow summaries (`K=v` ×400, 1,599 bytes → refused at both). The daemon sends `summary: None` (`crates/coagent-daemon/src/audit.rs:698`, at the head and at `gh/main`). | (h) |
| S-6 | `xn--` case-insensitive and untested | **Confirmed.** A case-sensitive plant passes every builder test (revert p4, all green). My differential reports it: 988 every-input oracle mismatches, 119 unattributed. `a@b.xn--` → `[REDACTED]--`: the trim makes `b.xn` pass as letters, as the drafter read. | (e), (f) |
| S-7 | branches with no committed test | **Confirmed.** Trailing `-` trim removed → every builder test green (p6). The all-dots local part (`s == at` removed, p5) IS caught, by `ae_what_is_not_an_address_is_kept_exactly` ("dotted decorator"). No "Not caught" form is pinned by a committed test (READ `ae_email.rs`). | (f) |
| S-8 | two rows cannot show their own reason | **Partly confirmed.** AE-1c's evidence comes from the scp sample. But reverting the URL exclusion alone also turns that test red, on its own URL sample (p2), so the URL branch is guarded by the test, not by its own row. AE-3/AE-3b evidence `leaked` matches every leak kind, as the drafter read. The observed failure texts do name their own kind (`address: leaked`, `domain: leaked`). | (f) |
| S-9 | the builder's oracle shares its author's readings | **Confirmed by READ** (STATUS 759-809). My independent oracle, using the brief's literal words, differs from `emails` on exactly three named decisions (see (e)). | (e) |
| S-10 | summaries attached to the owner's ruling | **Confirmed**, in four places (commit subject, `docs/AUDIT.md:37`, `redact.rs:250` comment "(and summaries)", BACKLOG:369). Minor, words only. | (i) |
| S-11 | prescribed `build.rs` comment names the seat | **Confirmed**: lane brief line 35 prescribed it word for word. Not a finding (ruling 7); Note. | (k) |
| S-12 | `xn--zckzah` outside the reserved names | **Confirmed**: Python's codec decodes it to `テスト` (KATAKANA TE SU TO). Its top label is not `.example`/`.test`/`.invalid`, so it is outside lane brief line 133 as written. No mailbox. A made-up label (e.g. `xn--qae0`) would serve the test equally: the code reads only the first four bytes (`:823`). Note. | (k) |
| S-13 | N-6's own run not re-made | **Re-made**: base 1 hit, head 0. | (b) |
| S-14 | two doc lines call every pattern a credential | **Confirmed** (`redact.rs:7`, `:139`, untouched). Note. | (j) |

Drafter's readings that were wrong: only S-1's `curl -u` case (masked by an older rule at both SHAs). S-8 is narrower than read, because the URL branch is guarded by the test.

## (a) Scope (TESTED): PASS
- Diff outside the eight paths: `0`; control (red script exclusion dropped): `1`.
- numstat: BACKLOG 18/0, Cargo.toml 3/0, build.rs 4/0, redact.rs 135/0, ae_email.rs 786/0, AUDIT.md 13/3, M0-OUTCOMES 11/0, red script 6/0. A line-level diff (`qa_scope.py`) finds only insert runs in the six zero-removal files. redact.rs inserts at 249 (5) and 695 (130). `git diff -U0` hunks: `@@ -249,0 +250,5 @@` and `@@ -689,0 +695,130 @@`; `emails` at head :742, `email_domain_ok` at :811; 690 → 825 lines.
- Each path maps to an "Owned" line of lane brief section 3: redact.rs (item 1; no other fn changed: below); build.rs (3 names + 1 comment appended before `];`); Cargo.toml (`# comment`, `[[test]]`, `name = "ae_email"` after `qa_seal`, before `[lints]`); new `tests/ae_email.rs`; red script (1 comment + 5 rows before `)`); AUDIT.md (the item-6 places only: 37-40, 679-686, 882); BACKLOG and M0-OUTCOMES appended.
- `docs/AUDIT.md`: the 3 removed lines are the old "Pattern redaction misses things" bullet (base 675-677). The 8 new lines keep every old word in order except three: `and` moved from before `long mixed runs` to before `email addresses`, `runs).` became `runs,`, and `` `PATH=`). `` became `` `PATH=`, ``. These are a word move plus two punctuation changes, all inside the bullet; the drafter expected only the `and` move. The other two hunks only add lines (37-40, 882). The new bullet also adds `` file-like `name@file.rs` `` to the over-masking list (the builder disclosed it, STATUS 225).
- `docs/M0-OUTCOMES.md`: base (251 lines, 24,410 bytes) is a byte prefix of the head file (equal bytes and sha256). `BACKLOG.md` is not a byte prefix: every base line is kept in order, and the 18 added lines sit in four runs at head lines 369 (1), 400 (1), 1684 (1), 1687-1701 (15).
- Bodies, by my own extractor (`qa_bodies.py`; it blanks strings, chars and comments before brace matching): 24 fns + the trait declaration and 15 `pub const` are byte-identical at both SHAs. `find` differs, and `emails`, `email_domain_ok` are new. Controls: `find` is reported different; a one-byte change planted in `hex_runs` of a scratch copy is reported (`DIFF fn hex_runs`). My sha256 prefixes equal the builder's table.
- Protected files: 23 files × 2 SHAs = 46/46 equal to the lane brief's values (`qa_protected.sh`). Control: `tests/ae_email.rs` at the base is reported `NOT-FOUND`, never hashed as empty.
- `Cargo.lock`, root `Cargo.toml`: `git diff` 0 bytes. No new dependency. `unsafe` in added lines: 0; control line planted in a copy of the added lines: 1. Host tree `7808b4ddc5414b6a3f592a7d647ee54a9de130e7` at both SHAs. `git diff … -- crates/coagent-audit/src` 7,393 bytes, 0 with redact.rs excluded.

## (b) The defect is closed, by my own attack (TESTED)
**Generator and corpus** (`h/qa_corpus.py`, seed `0x0ae5eed`; mine, not `gen_corpus.py`). Addresses follow the lane grammar:
- local parts 1–300 bytes over `[A-Za-z0-9._%+-]`, with plus-tags and dotted names;
- 2–6 labels, the suffix one of `example.com/org/net`, `test`, `invalid`, `example` in mixed letter case;
- 12% `xn--` last labels in all four cases (`xn--`, `XN--`, `Xn--`, `xN--`). These are made up and cannot be under a reserved name (S-12); they are never written outside the corpus file.

**Placements:** 70 templates.
- prose (start, middle, end);
- JSON (value, nested value, key, array);
- YAML, TOML, CSV, TSV;
- shell (`git config user.email`, `--author="A <…>"`, `curl -u …:x`, `curl -u …:pw`, `ssh`, `mail`, `--email=`);
- headers (`From:`, `To:`, `Reply-To:`, `Cc:` list, `From: "Name" <…>`, `To:` list), trailers;
- log lines (`user=… action=login`, ISO-time line, `[…]`, `user:…:profile`, pipe, quoted);
- `git log --format=%ae:%s` and `%h %ae:%s`;
- URL query, query with port, path, glued after a URL by `,` and `)`;
- `mailto:`, HTML `href="mailto:"`, markdown link, JS and Python stack frames, SQL, brackets and quotes;
- every terminal punctuation; `: `, `:` at the end, newline, tab, CRLF, `/`, `#`, `&`, `_` after;
- `EMAIL=`, `contact=`.

On top of the templates:
- each of 9 older-rule neighbours (Bearer, `Authorization:`, `API_KEY=`, `--password`, `ghp_` token, hex run, URL with password, PEM block, `TOKEN=`), × 4 joins (space, nothing, `:`, `=`) × 2 sides × (inside a line, whole text), 25 each;
- the 64 KiB window end (5 offsets, plus after a collapsing masked run);
- 12 templates with addresses under 8 bytes.

Every input also goes through the chain's summary: `AuthorChain::prepare` with `summary: Some(text)`, the stored opening read back. Probe: `h/qae_probe.rs` in scratch copies `qae/pb` (base) and `qae/ph` (head), one dump per input. A Python model of strip, `apply_mask` and `truncate` reproduces every probe answer at both heads: 0 mismatches over 28,962 inputs. That is the control on all my computed answers.

**Counts** (planted addresses, three-part leak check of lane brief line 70; a "part" leak counts only if the 8-byte window is not also text of the template outside the address, because reserved domains repeat in the context, e.g. `api.example.com`):

| | planted | base: visible in preview | head: visible in preview | head: visible in summary |
|---|---|---|---|---|
| (b) placements | 8,172 | 6,978 | **1,294** | 1,254 (240 window inputs refused as summaries at both, raw > 16 KiB) |

Control: the base count is the whole set minus the accidental masks of lane finding 3 (1,194 at the base: `EMAIL=`, `--author`, long-token local parts, `session:`, `curl -u`). Positive control: the same leak check flags 6,978 base previews in which the address is visibly left in; it flags 0 head previews in the 189 templates the rule covers.
Reach: 230 template ids, all generated. 189 have 0 head survivors in preview and in summary.

**Every head survivor of (b), by class:**
| class | templates (n each) | head survivors | form of the preview | documenting line |
|---|---|---|---|---|
| `:` + non-space after the address (the RULE, R-1 scp text) | `gitlog-ae-s` 60/60, `gitlog-h-ae-s` 60/60, `log-colon-key` 60/60; each neighbour joined AFTER by `:` (9 × 2 × 25 = 450/450) | 630 | `<address>:fix the build` whole | doc comment `redact.rs:718-720` (rule text exact); AUDIT.md:685, BACKLOG:1699, M0:257 say only "scp or ssh target" |
| inside a `scheme://` token (the RULE, R-1 item 1) | `url-query` 60, `url-path` 60, `url-glued-comma` 60, `url-glued-paren` 60 (whole address); `url-query-port` 60 and URL-with-password neighbour joined BEFORE by nothing/`:`/`=` (150) (`https://[REDACTED]@<domain>`: domain only) | 450 | whole, or domain only | doc comment :714-717; AUDIT.md:683-684 ("left to the URL rule"); BACKLOG:1699 |
| more domain characters glued after (the RULE as written) | hex neighbour joined after by nothing 36/50, PEM 42/50, `--password` 46/50, URL-with-password 50/50 | 174 | whole, or `<address>[REDACTED]` | doc comment :730-732; AUDIT.md:683; BACKLOG:1699 |
| 64 KiB window end (R-2) | `window-after-mask` 40/40 | 40 | `[REDACTED] <part of the address>` | BACKLOG new entry; doc comment :729 |
| total | | **1,294** | | |

No head survivor lies outside these classes: no undocumented class. JSON, YAML, TOML, CSV, headers, trailers, prose, shell flags, stack frames, SQL, markdown/HTML, `mailto:`, every punctuation, and every older-rule neighbour joined by space or `=` or placed before: 0 survivors.

**S-13, N-6's own run** (TESTED). The AUDIT-WIRE check's `qa_content.py`, `qa_causes.py`, `qa_lib.py`, `qa_inspect.rs` were copied unchanged, paths given as arguments only; the inspector was placed in the scratch copies' `crates/coagent-daemon/tests/`. Base binaries (`qae/tb/debug`) then head (`qae/t/debug`):
- base: audit folder holds `qaw.fake.person@example.invalid` in 1 file (`…/store/….00000000000000000010`); short preview `QAW short email: qaw.fake.person@example.invalid end`.
- head: **0 hits**; preview `QAW short email: [REDACTED] end`; the 8 other values 0 hits at both; daemon log 0 at both.
- verify Ok at both; control file hits every needle; no process left.

**PASS.**

## (c) The builder's "Points" item 1: glued-after forms (TESTED)
**1. How they arise** (`qa_corpus.py` section `c`, 25 templates × 80 addresses). Shape sources are my own knowledge of the tools, named per row: git's `--format` placeholders (`%ae`, `%h`, `%s`); redis-style colon-namespaced keys; `curl -u user:password` (curl's man page); a cache key built as address + hex digest; log rotation suffixes; the ssh/scp `host:port` shape.

| template | source of the shape | head survivors /80 | variant /80 |
|---|---|---|---|
| `<a>9f86…` (hash) | address + md5/sha key | 80 (as `<local>@<domain prefix>.[REDACTED]`) | 0 |
| `<a>2026`, `<a>-1`, `<a>-backup2`, `<a>.1`, `<a>-old` | rotation and year suffixes | 80 each | 0 each |
| `<a>--password` | two arguments run together | 80 | 0 |
| `<a>-----BEGIN PRIVATE KEY-----…` | PEM after an address, newline lost | 80 (`<a>[REDACTED]`) | 0 |
| `<a>550e8400-…` (uuid), `<a>dXNl…` (base64) | concatenated ids | 79, 80 | 0, 0 |
| `<a>https://…` | address glued to a URL (an scp-form `:/`) | 80 | 80 |
| `cache:<a>:v2` | redis-style key | 80 | 80 |
| `<a>:Fix flaky test`, `e31b29a <a>:Mask emails` | `git log --format=%ae:%s`, `%h %ae:%s` | 80, 80 | 80, 80 |
| `<a>:` + U+00A0 / `)` / `,` / `"` / U+000B / CJK | punctuation after a colon | 80 each | 80 each |
| `<a>:8080` | host:port | 80 | 80 |
| `user=<a>action=login`, `user=<a>id=42` | key=value joined by nothing (letters glued: masked, with more) | 0, 0 | 0, 0 |
| `session:<a>:1732600000` | `session` is a sensitive name: older rule masks | 0 | 0 |
| `curl -u <a>:hunter2pw …` | curl man page | 0 (older `flags` rule) | 0 |
| **total /2,000** | | **1,679** | **880** |

**2. The variant** (scratch copy `qae/pv`, diff `variant.diff`). When the whole run fails `email_domain_ok`, take the longest prefix of the run that, trimmed of trailing `.`/`-`, passes it, and apply the scp test at that prefix's end. I built it **linear**: one pass per domain run (`email_longest_ok`), tracking the current label's start, an "all letters" flag, completed labels and whether an empty label was seen. The Python reference in my oracle is the naive form and is used only for attribution.
The label-boundary-only variant answers differently on 1,170 inputs. It cannot end inside a label, so it leaves the last label(s) visible: `…example.com--password` → `[REDACTED].com--password`.

**3. The measured trade:**
- Survivors (preview): (b) 1,294 → 1,170 (−124: the hex, PEM and `--password` glued-after neighbours); (c) 1,679 → 880 (−799); (d) 40 → 37. The variant does nothing for the colon forms or for URL tokens: they are separate exclusions.
- The lane's "not an address" answers: every builder test is green on the variant, including `ae_what_is_not_an_address_is_kept_exactly` with its literal strings. None of my 15 not-an-address texts changes. Head → variant differs on 1,297 inputs (b 124, c 800, d 3, e 370), every one a glued form.
- Other rules: base → variant differential, attributed with a variant oracle: 0 unattributed (10,615 attributed, 18,347 identical); every-input oracle mismatches 0.
- Cost: linear (g): every family exponent 0.98–1.01 for `emails`, 0.99–1.01 for `redact`.
- Its spans are a superset of the head's by construction: it only acts where the head skips.

**PASS for the lane as built.** The glued forms are documented (doc comment :730-732, AUDIT.md:683, BACKLOG:1699). Severity: **Minor, against the rule**. Masking more would close 799/800 of the non-colon glued forms in my corpus, and these shapes are machine-made (keys, suffixes, run-together arguments) more than human prose. The coordinator holds the choice; I make none.

## (d) NOT-caught forms and over-masking, re-measured (TESTED)
| form | base preview | head preview | documented as | behaves as documented? |
|---|---|---|---|---|
| `"john doe"@example.com` | kept | kept | not caught | yes |
| `alice@bücher.example` | kept | **kept whole** | "keeps `alice@b`" | **no: the whole address is kept** |
| `jörg@example.com` | kept | `jö[REDACTED]` | not caught (any non-ASCII byte) | **no: mostly masked** |
| `alice@mail.exämple.com` | kept | `[REDACTED]ämple.com` | not caught | **no: partly masked, partly shown** |
| `alice%40example.com`, `alice&#64;example.com`, `alice at example dot com` | kept | kept | not caught | yes |
| `alice@\nexample.com`, `alice @ example.com` | kept | kept | not caught | yes |
| `a@localhost`, `a@[192.0.2.1]` | kept | kept | not caught | yes |
| `https://user@host.example/` | kept | kept | masked by neither rule | yes |
| `user@host.example.com:/path` | kept | kept | scp target keeps its user name | yes |
| `name@file.rs`, `y = x@self.weight` | kept | `[REDACTED]`, `y = [REDACTED]` | over-masking accepted | yes |
| `...@example.com` | kept | kept | (grammar: empty local part after trim) | yes (not listed) |
| `..a@example.com` | kept | `..[REDACTED]` | leading `.` trimmed | yes |
| `a@b.example-` | kept | `[REDACTED]-` | trailing `-` trimmed | yes |
| `a@b.xn--` | kept | `[REDACTED]--` | (trim makes `b.xn` pass as letters) | S-6 overlap, harmless |
| `a@b.XN--ZCKZAH` | kept | `[REDACTED]` | case-insensitive (doc comment) | yes |
| `alice@example.com9f86d081884c7d659a2feaa0c55ad015` | `alice@example.[REDACTED]` | same | glued, not caught | yes (older rule masks part) |
| `alice@example.com--flag` | kept | kept | glued, not caught | yes |
| `alice@example.com-----BEGIN PRIVATE KEY-----` | `alice@example.com[REDACTED]` | same | glued | yes |
| `alice@example.comhttps://x.example/p` | kept | kept | glued | yes |
| `alice@example.com:` + U+00A0 / `)` / `,` / `"` / U+000B / CJK | kept | kept | rule text (doc comment) | yes, by the doc comment's rule; NOT by "scp or ssh target" |
| `user:alice@example.com:profile`, `alice@example.com:fix the build`, `mail alice@example.com:thanks` | kept | kept | same | same |
| `curl -u alice@example.com:secret` | `curl -u [REDACTED]` | same | — | older `flags` rule (`redact.rs:505`) |
| `https://x.example/c?to=alice@example.org` | kept | kept | "left to the URL rule" | kept whole: the URL rule does nothing here |
| `https://x.example:8443/c?to=alice@example.org` | `https://[REDACTED]@example.org` | same | same | URL rule masks up to the `@`; domain shown |
| `see https://x.example/a,alice@example.org` (also `)` and `;`) | kept | kept | inside a token | yes |
| U+2066/2067/2068/2069/FE0F/034F before `@` or inside the domain | kept | kept | any non-ASCII byte | yes (invisible to a reader) |
| same, inside the local part | kept | `al<char>[REDACTED]` | any non-ASCII byte | **no: mostly masked** |
| U+200B / U+00AD anywhere | the address, char stripped | `[REDACTED]` | stripped first | yes |

**R-1 control:** `https://bob:pw1234@host.example/r` → `https://[REDACTED]@host.example/r` at base and head; `git clone https://bob:hunter2pw@example.com/r` → `git clone https://[REDACTED]@example.com/r` at both; scp target kept whole at both. PASS: the harness is right.

**Result:** every documented form behaves as documented, except the non-ASCII sentence and its example (S-3): **Minor L-1** below.

## (e) Every existing rule's answers unchanged: my own differential (TESTED): PASS
- Corpus: 28,962 inputs, seed `0x0ae5eed`:
  - (b) 7,992 and (c) 2,000 placements, (d) 65 literal forms;
  - 4,000 generated credentials alone;
  - 3,000 mixes of addresses, credentials, not-an-address shapes and words, joined by space, nothing, `:`, `=`, newline, tab or `,`;
  - 4,000 strings over an edge alphabet (`aZ9._%+-@:/ "'<>\`\n\txé` U+200B U+00A0 U+2066 `-`);
  - 2,000 S-1..S-4 edges (an address with a prefix in {none, `x`, URL, `mailto:`, `user:`, `<`, `"`, `TOKEN=`, `é`} and a tail in {`:`, `:x`, `: `, `:`U+00A0, `:)`, `-`, `--`, `.`, `..`, `9`, `-9`, `.9`, `x`, `é`, `-----BEGIN`, `https://a`, `:/`, `@`, `@b.example`});
  - 3,000 Unicode strings over 8 ranges (30% with an address);
  - 40 inputs of 65,000–70,000 bytes with an address at bytes 65,300–65,600;
  - 2,865 test literals: 573 distinct string literals of `tests/ae_email.rs`, `gate_attacks.rs`, `gate_r2.rs`, `redaction.rs` (the files whose code calls `preview(`, `.redact(` or `patterns::find/emails`), each in the 5 placements of `redaction.rs:73-79`.
- Compared per input: `find` on the clean text and on the clean window (sorted, merged), `redact`, `preview`, the chain's stored summary (or its refusal) and stored full tier.
- **My oracle** (`h/qa_analyze.py` `oracle`) is written from lane brief lines 42-51, not from `emails` or the builder's helper. Literal readings: `xn--` lower-case as written; "a byte that is not whitespace" as a byte outside C `isspace` (so U+000B counts as whitespace); the scp `:` read after the trimmed domain ("a domain", which the brief defines as trimmed); the URL token delimited exactly as `url_userinfo` delimits it (the brief says so).
- **Result:** inputs 28,962 · identical 19,615 · attributed 9,347 · **unattributed 0** · differing: find 9,347, redact 9,347, preview 9,039, summary 9,067.
- **Oracle differences (grammar decisions of the code, each named):**
  1. `xn--` compared case-insensitively: 988 inputs (STATUS point 4).
  2. U+000B after `:` is not whitespace for the code (Rust `is_ascii_whitespace`): 81 inputs. Such an address is kept.
  3. Under a Unicode-whitespace reading, U+00A0 after `:` would also be whitespace: 181 more inputs (262 in all). The code keeps those addresses.
  With the code's own three readings the oracle agrees on **every** input, identical ones included: 0 mismatches. The scp test after the trimmed end (STATUS point 5) is also my literal reading: no difference.
- **Attribution:** an input is attributed only if the new spans = old ∪ new `emails` spans, the new redact, preview and summary = `apply_mask` (and `truncate`, and the 4,096 limit) of that union, and the `emails` spans = my oracle's (with readings 1 and 2 named). I also added an every-input check: `emails` spans against the oracle on identical inputs as well, so a plant that leaves outputs equal to the base is still seen.

**Planted regressions through my comparison** (`logs/analyze_<plant>.txt`):
| plant | unattributed | every-input oracle mismatches | first report |
|---|---|---|---|
| head built `COAGENT_AUDIT_RED=redact_no_url` (log: `RED CONTROL BUILD`) | 1,186 | 0 | `#38 url-query-port`: base `https://[REDACTED]@…example.org`, plant keeps it whole |
| `redact_no_long` (`RED CONTROL BUILD`) | 3,196 | 0 | `#19 sh-email-eq`: base `tool [REDACTED]@…`, plant `tool --email=[REDACTED]` |
| p7: `emails` takes the byte after the domain (the builder's third plant) | 7,901 | 8,212 | `#0 prose`: `…[REDACTED]about the build.` spans `[(15, 61)]` vs oracle `[(15, 60)]` |
| p4: `xn--` case-sensitive (S-6) | 119 | 988 | `#7 json-array` (an `xN--` address left whole) |
| p2: only the URL exclusion removed | 1,637 | 1,687 | `#37 url-query` |
| p3: only the scp test removed | 2,372 | 2,750 | `#31 log-colon-key` |
| p5: `s == at` removed | 119 | 128 | `"john doe"@example.com` → `"john doe"[REDACTED]` |
| p6: trailing `-` trim removed | 24 | 165 | `a@b.xn--` |
| p1: the `emails` call removed from `find` | 0 (identical everywhere) | 0 | **not seen**: a head without the call equals the base, and my probe calls `emails` directly. That plant is the defect itself, not a change to another rule; my survivor count in (b) catches it (the builder's leak tests also go red, (f)). |

**The builder's "Points" item 2, judged:**
- Under the lane brief's attribution rule ALONE, the builder's third plant (p7) is attributed on every differing input (1,728 + 7,901 = 9,629). It is caught only by the oracle condition. This confirms the builder's point.
- The builder's oracle as code (READ, STATUS 759-809) implements the grammar with the code's own readings: case-insensitive `xn--`, ASCII whitespace, the trimmed scp end, `url_userinfo`'s delimiters. So it can detect drift between `emails` and its author's reading. It cannot detect a reading of the brief that both share (S-9); for example it would accept case-insensitive `xn--` or U+000B as non-whitespace as correct. Its attribution compares merged spans, so "0 unattributed" is a statement about outputs.
- Same seat, independent code: that is not enough on its own for a rule the coordinator relies on. With my independent oracle the residue is exactly the three decisions above, and none hides a defect. All three keep the code at least as strict as a literal reading would, except U+000B and U+00A0 after `:`: those make the code keep an address that a whitespace reading would mask.

## (f) The product fix reverted, and the red rows (TESTED)
**Reverts with the builder's tests** (`git archive e31b29a` + ONE edit to `src/redact.rs`; tests untouched; own empty target dir; every `.rs` touched; each log shows `Compiling coagent-audit`; diffs kept as `plant_p<N>.diff`):
| edit | builder test(s) red | first panic line | red on its own assertion? |
|---|---|---|---|
| (1) p1 `emails(b, &mut r);` removed | listed, prop, not-addresses, old-previews (4 of 4 run) | listed: `followed by a colon and a space: address: leaked in preview "mail bob@example.com: thanks"`; prop: `AE-3: address: leaked "_@A.aA" in "Bearer [REDACTED] _@A.aA tail words" …`; not-addresses (its positive control, `:308`): `left: "git@git.example.com:org/repo.git by bob@example.com via …"`; old-previews (its control, `:781`): `… new event is masked …` | **yes** for `ae_listed_addresses_never_appear_in_a_preview` and `ae_prop_generated_addresses_never_survive` (their leak assertions) |
| (2) p2 URL exclusion alone | `ae_what_is_not_an_address_is_kept_exactly` | `url user, no password: not an address: changed: "git clone https://bob@example.com/r" -> "git clone https://[REDACTED]/r"` | yes |
| (3) p3 scp test alone | same | `scp target: not an address: changed: "scp build.tar user@host.example.com:/tmp/x" -> "scp build.tar [REDACTED]:/tmp/x"` | yes |
| (4) p4 `xn--` case-sensitive | **none** (4 passed, 1 ignored) | — | **unguarded branch (L-3)** |
| (5) p5 `s == at` removed | not-addresses | `dotted decorator: not an address: changed: "@app.route(\"/\")" -> "[REDACTED](\"/\")"` | yes (the branch is guarded) |
| (6) p6 trailing `-` trim removed | **none** | — | **unguarded branch (L-3)** |
| (7) p7 byte after the domain | listed (`:190` exact string), not-addresses (`:308`), old-previews | `left: "mail [REDACTED] thanks"` / `right: "mail [REDACTED]: thanks"` | yes |

**The three red names, by hand** (row form, `COAGENT_AUDIT_RED=<name> cargo test --locked -p coagent-audit --test ae_email -- --exact <test>`, own target per name, `RED CONTROL BUILD` in each log, exit 101):
- `redact_no_email` / listed (AE-1): `followed by a colon and a space: address: leaked in preview "mail bob@example.com: thanks"`.
- `email_keeps_domain` / listed (AE-1b): `followed by a colon and a space: domain: leaked in preview "mail [REDACTED]@example.com: thanks"`.
- `email_eats_scp_and_urls` / not-addresses (AE-1c): `assertion `left == right` failed: scp target: not an address: changed: "scp build.tar user@host.example.com:/tmp/x" -> "scp build.tar [REDACTED]:/tmp/x"`.
- AE-3, whole failure text: `AE-3: address: leaked "_@A.aA" in "Bearer [REDACTED] _@A.aA tail words" (raw "Bearer Zm9vYmFyYmF6cXV4MTIz _@A.aA tail words") (minimal case Case { local: "_", labels: ["A"], tld: "aA", position: 0, filler: 200, neighbour: 0, join: 0, after: false, decor: 0, cut: 0 })`. It names its own kind (`address`).
- AE-3b, whole failure text: `AE-3: domain: leaked "_@A.aA" in "Bearer [REDACTED] [REDACTED]@A.aA tail words" (raw …) (minimal case Case { local: "_", labels: ["A"], tld: "aA", … })`. It names its own kind (`domain`).
- The row evidence `leaked` would also accept the other kind (S-8): Note N-3.

**The whole audit red runner at head** (TESTED, heavy; the counter read 1 before the start; run as `bash scripts/red-controls-audit.sh` from my clone's root through `r.sh`, with `COAGENT_AUDIT_RED_TARGET=/private/tmp/claude-501/qae/red-t` and `COAGENT_AUDIT_RED_LOGS=/private/tmp/claude-501/qae/red-logs`; 2,077 s):
- Rows counted by program inside `ROWS=(`: **173 at the base, 178 at the head**. The 173 base rows are byte-identical and in order as the head's first 173. The five new rows are the lane brief's rows in the five-field form; AE-1c's evidence is `not an address: changed`. `MUTANTS` has 2 rows at both, identical. `RED` names in `build.rs`: 144 → 147, the base list a prefix.
- Run: `rows: 178 cfg rows + 2 source-mutant rows`; **180 `RED`, 0 `NOT-RED`**; `GREEN: 316 tests ok`; `RED CONTROLS OK: every guard went red under its control, on its property, and green without`; `exit=0`. All 178 cfg logs show `RED CONTROL BUILD`; both mutant logs show `MUTANT APPLIED`. Every path in my logs is under `/private/tmp/claude-501/qae` (the other `/private/…` strings are BACKLOG text inside the runner's mutant copy).
- The five lane rows' first evidence lines:
  - `redact_no_email AE-1`: `followed by a colon and a space: address: leaked in preview "mail bob@example.com: thanks"`
  - `email_keeps_domain AE-1b`: `followed by a colon and a space: domain: leaked in preview "mail [REDACTED]@example.com: thanks"`
  - `email_eats_scp_and_urls AE-1c`: `assertion `left == right` failed: scp target: not an address: changed: "scp build.tar user@host.example.com:/tmp/x" -> "scp build.tar [REDACTED]:/tmp/x"`
  - `redact_no_email AE-3`: `AE-3: address: leaked "_@A.aA" in "Bearer [REDACTED] _@A.aA tail words" …`
  - `email_keeps_domain AE-3b`: `AE-3: domain: leaked "_@A.aA" in "Bearer [REDACTED] [REDACTED]@A.aA tail words" …`
- No line was removed or moved in `build.rs` or the red script ((a)). **PASS.**

## (g) Linear time (TESTED, release)
- The builder's test re-run (`cargo test --release -p coagent-audit --test ae_email -- --ignored --exact ae_email_time_scales_linearly --nocapture`, own target `qae/trel`): exit 0, `test result: ok. 1 passed`. Lines (µs):
  `a@ repeated: emails [(64, 507), (128, 1019), (256, 1290)]; redact [(64, 3833), (128, 8463), (256, 14980)]` · `a. repeated then @b.example: emails [(64,138),(128,288),(256,582)]` · `@ repeated: emails [(64,276),(128,371),(256,1109)]` · `local run, no @: emails [(64,49),(128,209),(256,192)]` · `a@b. repeated: emails [(64,296),(128,619),(256,1180)]` · `x://a@ repeated: emails [(64,84),(128,202),(256,388)]` · `every rule's trigger: emails [(64,77),(128,134),(256,279)]`.
  The 4x/8x assertion admits exponents up to 1.5. Single runs are noisy (the 64→128 KiB steps vary). No family comes near 1.5 in my fitted runs below.
- My own families (`h/qae_time.rs`, best of 3, 64/128/256/1024 KiB, exponent = least-squares slope of log time on log size):

| family | `emails` µs 64/128/256/1024 KiB | exp | `redact` exp | variant `emails` exp |
|---|---|---|---|---|
| `@`×n | 186/372/715/2972 | 1.00 | 1.00 | 1.00 |
| `a@`×n | 322/618/1274/6604 | 1.10 | 1.05 | 1.00 |
| `a.`×n (no `@`) | 50/96/201/796 | 1.00 | 1.04 | 1.00 |
| `a`×n (local run) | 48/100/201/763 | 1.00 | 0.99 | 0.99 |
| `a.`×n then `@` | 138/288/558/2381 | 1.02 | 1.02 | 1.01 |
| `a@` + `a.`×n + `9` (fails at the end: the variant's worst case) | 172/362/698/2866 | 1.01 | 1.01 | 1.00 |
| `@a.`×n (64 KiB–1 MiB) | 315/617/1343/5150 | 1.01 | 1.03 | 0.99 |
| `x://`×n then addresses | 247/266/506/2110 | 0.82 | 1.04 | 0.98 |
| `a@b.c:`×n | 179/351/717/2878 | 1.00 | 1.02 | 1.01 |
| `a@b.example:`×n (scp test each time) | 193/370/774/2986 | 0.99 | 1.01 | 1.00 |
| `a@b.example9`×n (glued) | 298/575/1200/4604 | 0.99 | 1.03 | 1.00 |
| `a@b.ex` + `-`×n | 321/345/698/2874 | 0.84 | 1.03 | 1.00 |
| every rule's trigger | 97/171/631/1373 | 0.99 | 1.02 | 0.99 |

**PASS:** every exponent is between 0.82 and 1.10, at the head and for the variant. Other seats' jobs were running (heavy counter 1), so absolute times carry load noise.

## (h) Old records, the record format, and summaries (READ + TESTED)
- **Old records kept as written, by a REAL old build** (TESTED, `n6/qae_oldnew.py`, log `oldnew.jsonl`):
  1. Base binaries: convener `a` with `--audit`, joiner `b`; a sends `QAE old build: mail qae.old.person@example.invalid about the release` (stored: own seq 1, preview with the address, verify Ok); a stops.
  2. Head binaries on the SAME data folder (b restarted too): a sends `QAE new build: mail qae.new.person@example.invalid …`, then `audit_seal` → `sealed: the log was filed away and continues`; a stops.
  3. Copy, opened with the head inspector (`opened: Current`): event 1 = `QAE old build: mail qae.old.person@example.invalid about the release`, **byte-identical to what the base wrote**; event 2 = `QAE new build: mail [REDACTED] about the release`. `verify_segments` over the segment file plus the export: `Ok(SegmentsReport { from_genesis: true, segments: [(0, 1, 2), (1, 3, 2)], … })`. The old address is now only in the sealed archive bundle; the new one has 0 hits.
  4. The head redactor run on the old text would give `… mail [REDACTED] …`, so it is the store, not a re-mask, that kept event 1.
  Side observation: after the restart the joiner did not reconnect within 180 s. The send was recorded anyway (it is the convener's own event). Daemon behaviour, not this lane's; listed under Open.
- **The format:** `git diff … -- crates/coagent-audit/src` holds only redact.rs (7,393 bytes; 0 with it excluded). `git grep -n -E '\.redact\(|preview\('` over both crates' `src` at base and head: `chain.rs:236`, `chain.rs:245`, `redact.rs:93` (definition), `redact.rs:98`, identical at both. Positive control: `chain.rs:245` found. `received.rs`/`bundle.rs` mention only the size constants (`received.rs:31`). **R-4's proviso holds.**
- **S-5, summaries** (TESTED, `h/qae_sum.rs` and `h/qae_host.rs` in the scratch copies; every address reserved):
  1. Through `SessionAudit::record` and export: `notify alice@example.com about the deploy` (41 bytes) → base stored as written, head stored `notify [REDACTED] about the deploy` (34 bytes).
  2. **The builder's figure (585 six-byte addresses, 4,094 → 6,434 bytes) cannot be re-made with a reserved name.** No six-byte address exists under `example.com/org/net`, `.test`, `.invalid` or `.example`; the shortest is `a@b.test`, 8 bytes. (I wrote this STOP-and-say into STATUS before writing it here.) Mine, through the chain: 455 × `a@b.test` joined by spaces = **4,094 bytes → base stored 4,094 bytes; head refused `FieldLimit("summary")`** (redacted: 5,004 bytes). Also `"x"×4087 + " a@b.test"` (4,096 bytes) → base stored; head refused (4,098 after redaction). The builder's figure is arithmetic on the same mask (6 → 10 bytes each: 585 × 4 = 2,340 more, 4,094 + 2,340 = 6,434). It is consistent with mine but was measured by the builder through `redact` alone with a non-reserved two-letter top label. Both stand.
  3. What the caller sees: the daemon sends `summary: None` (`crates/coagent-daemon/src/audit.rs:698`, at the head and at `gh/main`), so **no daemon send can meet this; a user of the daemon sees nothing**. A library caller using the host: `AuditHost::apply(Record{ summary: 4,094 bytes })` → base `Ok(Recorded(1))`; head `Err(Audit(FieldLimit("summary")))`, own seq unchanged (0), the next record without a summary `Ok(Recorded(1))` (READ `host.rs:532-546`: P-6, the refusal is returned as it is, never retried).
  4. Older rules already grow summaries past the limit: 1,024 × `K=v` (4,095 bytes) and even 400 × `K=v` (1,599 bytes) are refused at the base and at the head (`K=v` → `K=[REDACTED]`, 3 → 12 bytes). The class is not new; the lane's documents do not say so (Note N-9).

## (i) The owner's answer (TESTED, by program)
- CLARIFICATIONS C-17 (line 168) against lane brief section 9 (line 166): **equal**, 80 characters, 82 UTF-8 bytes. Its Context line says lane AUDIT-EMAIL recorded it; the builder says written (STATUS 240). PASS.
- Every lane line naming the owner (case-insensitive `owner`, added lines and commit message, `qa_owner.py`): 17 lines. Those that say "the owner's ruling: email addresses blanked/are blanked in previews" (Cargo.toml comment, build.rs comment, red-script comment, `redact.rs:696`, BACKLOG Resolved line, `ae_email.rs:1`, M0-OUTCOMES:254 "blanked in the audit log's short previews") say no more than his words plus the card. "The owner will be told" (BACKLOG) is the coordinator's R-7, not a ruling claim.
- **S-10:** four lines attach summaries to his ruling:
  - the commit subject `Mask email addresses in audit previews and summaries (the owner's ruling)`;
  - `docs/AUDIT.md:37` `Email addresses are masked whole … (the owner's ruling), in summaries too`;
  - `redact.rs:250` `// The owner's ruling: email addresses are blanked in previews (and summaries) as well.`;
  - BACKLOG:369 `a new rule masks email addresses whole (…, the owner's ruling), in previews and summaries`.
  His words are "Yes, blank email addresses" on a card about "the audit log's short previews"; summaries are the coordinator's R-3. Effect: a reader of the history credits the owner with a ruling on summaries he did not make. No product effect: the daemon writes no summary. **Minor L-4**, words only.

## (j) Every claim the lane wrote, matched to a run (TESTED)
My list (`qa_sentences.py`, keywords `keeps, is masked, masked, is kept, kept, not caught, never, every, only, whole, unchanged, as before, neither`, case-insensitive) finds 33 sentences in the added lines of AUDIT.md, M0-OUTCOMES, BACKLOG, the doc comment (head 696-741) and the commit message (`logs/sentences.txt`). The ones that state a fact:

| file:line | claim | my run | verdict |
|---|---|---|---|
| M0-OUTCOMES:255, commit body l.3 | "an ASCII address with a dotted domain is replaced whole" | (b) and (c): replaced whole when matched; glued, colon and URL-token forms are ASCII and dotted and are not replaced. The same paragraph, and the next commit sentence, point to the exclusions and misses | true as qualified; wider in isolation (Note N-5) |
| AUDIT.md:685, BACKLOG:1699 (twice), M0-OUTCOMES:257, commit l.4, doc comment :719-720 | "an scp or ssh target keeps its user name" | (b) 630, (c) 800 kept: every address before `:` + a non-whitespace byte, scp or not. The doc comment's rule text (:718-719) is exact; the other five lines are narrower than the effect | **narrower than the effect: Minor L-2** |
| AUDIT.md:683-684, commit l.4 | "one inside a `scheme://` token is left to the URL rule (so `https://user@host.example/` is masked by neither rule)" | (d): a query or path address is masked by neither rule unless a `:` precedes it in the token, and then the domain is shown | **true for the example, misleading for the class: Minor L-2** |
| doc comment :725-727, BACKLOG:1699 | "any address with a non-ASCII byte … so `alice@bücher.example` keeps `alice@b`" | (d): whole address kept; non-ASCII in the local part → mostly masked; in a later label → prefix masked, rest shown | **false: Minor L-1** |
| M0-OUTCOMES:259 | "Every other rule answers as before: over 38,225 inputs … differ only where an address was masked (0 unattributed)" | my 28,962 inputs: 0 unattributed. Byte-identical bodies plus `find` appending spans prove it for every input: the other rules' spans cannot change, and `apply_mask` of a union differs only inside `emails` spans | true (the "every" is covered by the structural proof, not only the sample) |
| M0-OUTCOMES:260, BACKLOG:1684 | "Logs already written are kept as written" | (h): a real base daemon's preview kept byte for byte; the grep proves no reader re-runs the redactor, so summaries too | true |
| AUDIT.md:37-39, BACKLOG:369 | "one 6-byte address adds 4 bytes; 585 of them in a 4,094-byte summary make 6,434 bytes, now refused" | (h)(2): same class through the chain with 8-byte reserved addresses (4,094 → refused); arithmetic of the 10-byte mask confirms 6,434 | true (builder's figure; mine differs in shape, both given) |
| AUDIT.md:37-39 | "a preview received from a peer is stored as the peer wrote it" | READ `received.rs:31` (size constants only) and the grep | true (not run) |
| AUDIT.md:882 | "`emails` alone 0.30/0.61/1.20 ms for 64/128/256 KiB of `a@`" | (g): my rerun 0.51/1.02/1.29 ms; my 4-size run 0.32/0.62/1.27/6.60 ms | a single machine-dependent measurement (Note N-7) |
| BACKLOG:1694 | window end: "the same holds for every rule (a token cut by the window can fall below its minimum length)" | TESTED: a cut hex run and a cut `ghp_` token reach the preview at both SHAs; `Bearer <token>` stays masked (`[REDACTED] Bearer [REDACTED]`) | wider than measured (Note N-8) |
| BACKLOG:1689 | peer previews "are stored, exported and verified unchanged" | READ only | not run (NOT checked) |
| doc comment :696 | "The whole address … is one span" | READ `:801-805` (`r.push((s, e))` at :804) | true |
| doc comment :702 | "The run stops at … every non-ASCII byte" | READ `local`/`domain` closures; (d) | true |
| doc comment :709 | "`mailto:` is kept" | (b) `mailto` template; ae test `see mailto:[REDACTED] for help` | true |
| doc comment :711 | "other rules may still mask part of it" | (d) `alice@example.[REDACTED]` | true |
| doc comment :738-741 | linear: "a byte is visited at most twice" | READ; (g) exponents ≈1 | true |
| commit l.6-7 | "Every other rule, apply_mask, truncate and preview are unchanged byte for byte; find gains added lines only." | (a) | true |
| `redact.rs:7`, `:139` (older lines, not the lane's) | "masks text that LOOKS like a credential", "The credential-shaped patterns" | an email address is not a credential | wide older text: Note N-6 (S-14) |

## (k) Names, ids, fixtures (TESTED)
- Byte scan (`qa_scan.py`, outside the repository). The words were given on the command line at run time:
  - the identity (`whoami`), the full and short host names, the home path;
  - the owner's name parts and account name, the personal mail domain and a public mail domain;
  - the three coordinator seat names, the drive name, `Development`, `!CODING`, the vault folder name, the drive tag;
  - 57 folder names taken at run time from levels 1-2 under `/Volumes/Laptop-DEV/!CODING/` (generic file names, numbered folders and this project's own names left out).
  Each was scanned plain, slugged (`-`, `_`, joined), URL-encoded (`quote`, `quote_plus`, lower hex), backslash-escaped, as UTF-16LE, in any letter case. Files: the 976 added lines, the commit message, and the eight files whole at the head.
  - Controls: a scratch copy of `ae_email.rs` with a planted `// planted control: <host>` line → found (3 words); a 600-byte random binary with the login name as UTF-16LE → found (4 words).
  - **Added lines and commit message: 0 hits for any person, account, machine, seat, client or project name.** The only hits there are generic folder words that are also ordinary English (`tests`, `docs`, `doc`, `report`, e.g. "tests in tests/ae_email.rs").
  - Older lines: a coordinator seat name appears 45/2/1 times in BACKLOG/AUDIT.md/M0-OUTCOMES at both SHAs (pre-existing, listed, not graded).
- Addresses (every `@` + dotted domain in the added lines and commit message, other than reserved names), each with why it is not a mailbox:
  - `app.route` (a decorator); `1.2.3`, `18.0.0` (version pins);
  - `file.rs`, `self.weight` (over-masking examples);
  - `example.com9f86`, `example.com--flag` (glued forms written to say they are not caught);
  - `example..com`, `example.c` (malformed on purpose);
  - `shop.example.xn--zckzah` ×2 (S-12);
  - `Pa55w0rd@db.example.com`, `hunter2pw@example.com`, `p@h.example`: these sit inside URLs and are reserved;
  - **`noreply@anthropic.com` in the commit message's `Co-Authored-By:` trailer**: the tool vendor's no-reply address. 398 of the base's 419 commits carry the same trailer, so it is this repository's convention, not this lane's choice (Note N-10).
- S-11: `// AUDIT-EMAIL (the owner's ruling: email addresses blanked in previews)` (`build.rs:162`) was prescribed word for word by lane brief line 35, against its own line 134 ("carries no seat name"). Earlier blocks carry lane names (`// M3 AUDIT-SEAL addendum 4`). Within the rules as prescribed; Note N-11 for the next audit-crate brief.
- S-12: `xn--zckzah` decodes to `テスト` (Python `punycode`/`idna` codecs). Whether IANA still lists it as a test label I cannot establish offline (UNVERIFIED). It is outside lane brief line 133 as written. No address whose last label starts `xn--` can be under a reserved name, so the rule and a test of that branch cannot both be met. A made-up label (`xn--qae0`) would serve the test equally (`:823` reads four bytes). Note N-12.
- Card ids in added lines: none; control: 6 in base BACKLOG; a planted made-up id in a copy of the added lines: found. Absolute paths: 2 hits, both `https://example.com/users/@alice:profile` (a URL path); control: the lane brief, 2 hits. Fixtures: `World::new`, `MemStore::new` at run time (READ). Commit author: the repository's configured owner identity (a GitHub noreply address), the same as the base's commits. A fact.

## (l) Suite, clippy, fmt (TESTED)
- Head: `cargo fmt --all --check` exit 0. `cargo clippy -p coagent-audit --all-targets --locked -- -D warnings` exit 0 (log shows `Compiling coagent-audit`; the only warning is the workspace manifest's unused `rand_core`, pre-existing).
- `cargo test -p coagent-audit -p coagent-audit-host --locked --no-fail-fast` (own empty target dirs): **base 384 passed / 0 failed / 14 ignored in 50 targets; head 388 / 0 / 15 in 51**. Per-target diff: only `tests/ae_email.rs` (4 passed, 1 ignored). The builder's STATUS says 379 / 383 (host 67). Its own logs (`tools/tmp/ae/b49b11/logs/{base,head}_tests.log`) sum to 384 / 388 with host 72, as mine do. A STATUS arithmetic slip, not a code fault (Note N-13).
- `aw_*` (listed by `git ls-tree` at both: answers, disk, lifecycle, off, peer, record, round2, seal, util), after `cargo build --workspace --bins --locked`: **14 passed / 0 / 0 in 9 targets at base and head** (1,1,3,1,2,1,4,1,0).
- `gate_r2` report tests (`--nocapture --test-threads=1`): 41 output lines each, one difference: `kept    email: "mail bob@example.com: thanks" -> "mail bob@example.com: thanks"` → `CHANGED email: "mail bob@example.com: thanks" -> "mail [REDACTED]: thanks"`. `scp` and `url with @path` print `kept` at both. Both tests green.

## For the owner, in plain words
**What changed:** an email address in the audit log's short previews (and in its summaries) is now replaced by `[REDACTED]`, as passwords and keys already were. The message you checked in the first audit-wiring test, which kept a made-up address in the log, now keeps none. Logs written before this change are not rewritten.
**Still not blanked** (facts about the product; "my corpus" means my own test texts):
- An address inside a web link, such as `…/unsubscribe?email=<address>`. Every such case in my corpus kept it (450 of 450: 240 whole, and 210 where the name before the `@` was hidden but the domain still shows).
- An address followed directly by a colon and more text: a `git log` line formatted as `<address>:<message>`, or a key like `user:<address>:profile`. Kept every time (630 in my placements). An `ssh`/`scp` target like `git@host:repo` is kept on purpose.
- An address with characters glued on with no space (`<address>-1`, `<address>2026`, `<address><hash>`). Kept every time but once (799 of 800 in that part of my corpus).
- An address with an accented letter (`alice@bücher.example` is kept whole), or written in a disguised form (`alice at example dot com`, `alice%40example.com`).
- An address in a link's user name with no password (`https://user@host/`).
- Previews another member's older build sent you: stored as they wrote them.
None of these is reachable as a crash or a corruption: the log stays valid and verifiable.

## Findings
**Against the lane's work** (no Blocker, no Major):
- **L-1 Minor: the non-ASCII sentence and its example are false.** `crates/coagent-audit/src/redact.rs:725-727` and `BACKLOG.md:1699` say "any address with a non-ASCII byte … so `alice@bücher.example` keeps `alice@b`". Measured: the whole address is kept; a non-ASCII byte in the local part masks most of it (`jörg@example.com` → `jö[REDACTED]`); one in a later label masks a prefix and shows the rest (`alice@mail.exämple.com` → `[REDACTED]ämple.com`).
  - Repro: `printf 'alice@b\xc3\xbccher.example\n' | xxd -p > in.hex` then the probe (`gate_audit_email_tests/probe.sh ph tph in.hex out`) at the head.
  - Fix in words: "a non-ASCII byte in the domain keeps the address whole (`alice@bücher.example` is kept); in the local part or a later label the address is masked only in part".
- **L-2 Minor: two exclusions described narrower than their effect.**
  - (a) `docs/AUDIT.md:685`, `BACKLOG.md:1699` (twice), `docs/M0-OUTCOMES.md:257`, the commit body: "an scp or ssh target keeps its user name". Every address followed by `:` and a non-whitespace byte is kept whole: `git log --format=%ae:%s` lines, colon-keyed keys, `:)`, `:,`, `:"`, `:` + U+000B or U+00A0. The doc comment's rule text (`redact.rs:718-719`) is exact.
  - (b) `docs/AUDIT.md:683-684`: "one inside a `scheme://` token is left to the URL rule". The URL rule masks a query or path address only when a `:` precedes it in the token, and then shows its domain; otherwise nothing masks it.
  - Repro: the (d) table rows.
  - Fix in words: say "any address directly followed by `:` and a non-space (scp targets, `git log` `%ae:%s` lines, `key:<address>:…`) is kept" and "an address anywhere in a `scheme://` token (query, path) is kept; the URL rule masks only user-info before a `:`-holding `@`".
- **L-3 Minor: two branches no test guards.**
  - `email_domain_ok`'s case-insensitive `xn--` (`redact.rs:823`): a case-sensitive revert passes every builder test (plant p4).
  - The trailing `-` trim (`redact.rs:791`): removing `b'-'` from it passes every builder test (plant p6).
  - Repro: `gate_audit_email_tests/plant_p4.diff`, `plant_p6.diff`, then `cargo test -p coagent-audit --test ae_email` → green.
  - Fix in words: add `user@shop.example.XN--ZCKZAH` and `a@b.example-` (expected `[REDACTED]-`) to `listed()`.
- **L-4 Minor: summaries attributed to the owner's ruling** (S-10): commit subject; `docs/AUDIT.md:37`; `redact.rs:250`; `BACKLOG.md:369`. Repro: `git log -1 --format=%s e31b29a`. Fix in words: "(the owner's ruling, previews; the coordinator's ruling, summaries)". The commit subject cannot change without a rewrite; a BACKLOG line can say it.

**Against the coordinator's rule** (section 8 ruling 11; the lane built it as ruled and documented it; the coordinator decides on these figures):
- **RF-1 (Major by effect, not a NO GO for this merge): an address anywhere in a `scheme://` token is kept.** Lane brief line 46 / R-1 rule the whole token out, not only its user-info. My corpus: 450 of 450 URL-token placements kept the address or its domain. The shapes are common in ordinary command and log text: `?email=`, `?to=`, unsubscribe and `login_hint=` links, `mailto` inside URLs, paths like `/users/<address>/`.
  - Repro: `https://x.example/c?to=alice@example.org` → kept.
  - Suggested fix in words: exclude only the user-info part (from `://` to the first `/`, `?` or `#` of the token), and let `emails` match in the path, query and fragment.
- **RF-2 (Minor): an address followed by `:` and any non-whitespace byte is kept** (lane brief line 47). Measured: 630 of 630 such placements in (b), 800 of 800 colon forms in (c). Includes `git log --format=%ae:%s` (a custom format; default `git log` writes `Author: Name <address>`, which is masked) and colon-keyed keys. `curl -u <address>:<password>` is masked by the older `flags` rule.
  - Suggested fix in words: treat `:` as an scp target only when the text after it (to the next whitespace) starts with `/` or `~`, or holds a `/`, or ends `.git`. That choice is the coordinator's.
- **RF-3 (Minor): glued-after forms are kept** (STATUS point 1). (c): 1,679 of 2,000, of which 799 non-colon cases are closed by the linear longest-valid-prefix variant, with no listed not-an-address answer changed and no other rule changed.

**Notes:**
- N-1 (S-3): invisible characters not stripped (U+2066–U+2069, U+FE0F, U+034F) before the `@` or inside the domain keep an address whole while it looks whole to a reader. They are covered by "any non-ASCII byte". `is_format_char` could take them (an older rule's list).
- N-2: the all-dots local part (`...@example.com`) is kept, by the grammar; not listed.
- N-3 (S-8): rows AE-3/AE-3b accept any `leaked` text; `address: leaked` / `domain: leaked` would pin each row's own kind. AE-1c's evidence comes from the scp sample; the URL branch is guarded by the same test (p2), not by a row of its own.
- N-4 (S-9): the builder's oracle shares its author's readings; mine finds exactly three code decisions (`xn--` case, U+000B and U+00A0 after `:`). The two whitespace ones keep an address that a whitespace reading would mask.
- N-5: "an ASCII address with a dotted domain is replaced whole" (M0-OUTCOMES:255, commit body) is true only as qualified by the next sentences.
- N-6 (S-14): `redact.rs:7` and `:139` still say every pattern is credential-shaped (older text).
- N-7: the AUDIT.md:882 time figures are one machine-dependent run (my rerun: 0.51/1.02/1.29 ms).
- N-8: BACKLOG:1694 "the same holds for every rule": a scheme-word rule (`Bearer <token>`) still masks after the window cut. Hex and prefix tokens do leak as described.
- N-9 (S-5): summaries could already be refused because of older rules (400 × `K=v`, 1,599 bytes, refused at both); the lane's documents present the refusal as new to email addresses.
- N-10: the commit message's `Co-Authored-By:` trailer holds the tool vendor's no-reply address, as 398 of the base's 419 commits do.
- N-11 (S-11): the lane brief prescribed a seat name in `build.rs:162`; next audit-crate brief: say "the owner's ruling (email addresses)" without the lane name.
- N-12 (S-12): `xn--zckzah` is outside lane brief line 133; a made-up `xn--` label serves the test as well; the brief's rule cannot be met by any `xn--` test.
- N-13: the builder's STATUS test counts (379/383, host 67) differ from its own logs (384/388, host 72); the per-target difference is right.

**Open** (seen, not this lane's, not investigated): after both daemons of a pair are restarted, the joiner did not reconnect to the convener within 180 s (my (h) run; the convener's own send was still recorded). `crates/coagent-daemon` reconnect behaviour; worth a look in a daemon lane.

## What was NOT checked
| item | why |
|---|---|
| `scripts/check.sh` | brief: not run (the coordinator's merge check runs it) |
| The red runner at the base | ruling 2: head only; base rows counted by program (173, prefix of the head's) |
| Real-world frequency of each surviving class | my corpus is templates; frequencies are per template, not per real log |
| Peer previews "stored, exported and verified unchanged" (BACKLOG:1689) | READ only (`received.rs:31`); no two-build peer run |
| IANA status of `xn--zckzah` | no network by rule; UNVERIFIED |
| The builder's six-byte summary figure through the chain | no six-byte reserved address exists; re-measured with 8-byte reserved addresses |
| Main `5cab5e4` and the merge | brief: not merged, not judged |
| Windows builds | not in scope |

## Files (`m1_review/gate_audit_email_tests/`)
- `r.sh` (cd inside a wrapper), `probe.sh`, `plants.sh`.
- `harness/`: `qa_corpus.py` (generator, seed `0x0ae5eed`), `qae_probe.rs` (dump per input), `qa_analyze.py` (Python model with self-check, survivors, differential, attribution, my oracle, variant oracles), `qa_compare_var.py`, `qa_hv.py`, `qae_sum.rs` and `qae_host.rs` ((h) summaries), `qae_time.rs` ((g)), `dbg*.py` (attribution debugging, kept as run).
- `qa/`: `qa_scope.py`, `qa_bodies.py` (my extractor), `qa_protected.sh`, `qa_owner.py`, `qa_sentences.py`, `qa_scan.py` + `run_scan.sh` (the words are not in the files), `sum_results.py`, `added.txt` and `commit_msg.txt` (the lane's added lines and message).
- `n6/`: the AUDIT-WIRE harness copied (`qa_content.py`, `qa_causes.py`, `qa_lib.py`, `qa_inspect.rs`), and `qae_oldnew.py` ((h) real old build).
- `plants/`: `plant_p1.diff` … `plant_p7.diff`, `variant.diff`, `lane.diff`.
- `logs/`: every build, test, probe, plant, analysis, N-6, old/new, timing, scan-summary (counts only) and red-runner log; `corpus_c1.meta.jsonl` (the corpus metadata). The corpus itself and the per-input dumps (1.5 GB) are not copied; they are re-made from the seed by `qa_corpus.py` and `probe.sh`.
- `red-logs/`: the runner's 181 log files (its mutant copy of the repository is left out).
- Work dir `/private/tmp/claude-501/qae` holds the clone, worktree, scratch copies, target dirs and data folders. No process of mine is left (no daemon, relay or test binary: `ps` checked). I wrote nothing outside the work dir, this folder, the verdict, and the project's STATUS file.
