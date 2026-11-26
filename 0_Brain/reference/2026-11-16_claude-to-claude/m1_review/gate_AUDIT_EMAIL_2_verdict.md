VERDICT: GO WITH NOTES — head 5aa56e1217947471bbb358c6a5a5214f31ee65a8

# QA-AUDIT-EMAIL-2: independent check of branch `audit-email-2`

Head `5aa56e1217947471bbb358c6a5a5214f31ee65a8` (one commit, parent `d4979dfe554c26019ed23139852813f95d5a4b25`). Every comparison is against `d4979df`. Main was read as `d4979dfe554c26019ed23139852813f95d5a4b25` (equal to the base); nothing was merged or judged.
Brief: the coordinator's `briefs_drafts/2026-11-27_coagent_QA-AUDIT-EMAIL-2_check_brief.md`. Checked 2026-11-27 on this laptop; project toolchain linked into `/private/tmp/claude-501/qae2/tools` (`COAGENT_TOOLS` set for every run); every build in its own empty target dir under `/private/tmp/claude-501/qae2/`.
Tags: TESTED = I ran it; READ = I read it. Scripts, harness, plant diffs and logs: `m1_review/gate_audit_email_2_tests/` (index at the end).

## BLUF
1. **Does the new version ever show something the old one hid?** No. Over 53,607 test texts (the first check's, my own with 7,500 hostile ones, and every test string of five files) no byte the old version masked is shown by the new one, and the code guarantees it for every text: the new rule only skips less. A planted copy that breaks this is caught on its first input. No finding against the coordinator's rulings is Major, so nothing needs deciding before a merge.
2. **Is every address now hidden or in a named gap?** Yes. Every address still shown falls in a class the code's own description names. Two of them are named by the rule's wording only: an address joined to a web link that has no path (`https://x.example.com,alice@example.org`), and an address before a colon when a `/` comes later in the same word (`alice@example.org:net/ipv4: fix`). The other three documents describe the first one too narrowly (Minor L2-1).
3. **What is still shown, and how often did it come up?** In my texts (80 per kind): 798 link-joined and 1,312 colon-then-later-`/` addresses, 269 before `:~`, 80 before `:…git`, 80 glued onto a link; on the first check's texts 140 (it measured 1,294 before) and 80 (1,679 before), the builder's figures, re-measured on the real final commit. Two branches that keep addresses have no test that fails when they are removed (Minor L2-2).
4. **Do the records tell the truth?** Yes, with Notes. Old logs are not rewritten, the record format is unchanged, every documented example gives its stated answer, the red controls all go red (185 of 185) and the suites are green. Notes: a summary the old version stored can now be refused (library callers only; the daemon sends none), and a few sentences are wider than their measurement.

**Verdict for the lane's work: GO WITH NOTES.** No Blocker or Major lies against what the lane built. Two Minors (L2-1 words, L2-2 tests) and Notes; the ruling findings RM-1 and RM-2 are Minor, apart in (m).

## Proofs (section 0)
- TESTED `git ls-remote` (GitHub remote, deploy key): `5aa56e1217947471bbb358c6a5a5214f31ee65a8 refs/heads/audit-email-2`, `d4979dfe554c26019ed23139852813f95d5a4b25 refs/heads/main`.
- TESTED `git log --format='%H %P' d4979df..5aa56e1` → one line `5aa56e1217947471bbb358c6a5a5214f31ee65a8 d4979dfe554c26019ed23139852813f95d5a4b25`.
- TESTED builder's STATUS `wc -lc` = 279 lines, 43,712 bytes; it ends `Head: 5aa56e1217947471bbb358c6a5a5214f31ee65a8` then `READY FOR QA AUDIT-EMAIL-2`.
- TESTED numstat equals the drafter's (nine paths): BACKLOG 7/0, Cargo.toml 3/0, build.rs 6/0, redact.rs 143/37, ae2_email.rs 665/0, ae_email.rs 0/5, AUDIT.md 16/12, M0-OUTCOMES 18/0, red script 8/2.
- Disclosure (rule slip of mine): two of my early shell commands contained a `cd` into my own work dir, against section 2 "never `cd`". Nothing outside the work dir was touched; every later command used absolute paths or the wrapper `qae2/r.sh`. Two times I first wrote into my STATUS were estimates, not read from the clock; I corrected them to the `date` output.

## Section 1a: my judgement of each W-point
| W | drafter's reading | my result | run |
|---|---|---|---|
| W-1 | the differential, item 0, survivors and bodies ran on `0c1ef5f` | **Confirmed**: `0c1ef5f` differs from the head in `redact.rs` only at the doc lines :740-741 (plus three documents). The figures hold at the head: my run at `5aa56e1` gives 25,130 / 3,832 / 0 on the first check's corpus and 1,294 → 140, 1,679 → 80; bodies: the head equals `0c1ef5f` item for item | (a0), (b), (e) |
| W-2 | `.git` case-sensitive, `xn--` not; `Repo.GIT` masked | **Confirmed**: `git@host.example:Repo.GIT` → `[REDACTED]:Repo.GIT`; `repo.GIT` 80/80 masked in my corpus. My oracle reads "ends `.git`" literally and agrees | (c), (d), (m) |
| W-3 | after any `://`, user-info runs to the token end when no `/?#`; path-less forms keep both addresses | **Confirmed**: both addresses kept; also `://` with no scheme and U+000B joins; 798 survivors in my corpus; with a port the domain shows | (b), (c)1, (d) |
| W-4 | the colon test reads the whole token; `src/lib.rs`, `profile/v2`, `fix,see/notes`, a date path kept | **Confirmed**, all four, plus `net/ipv4:` subjects and later links in key=value lines; 1,312 survivors; the documents' "what remains" sentences are scoped to the first check's corpus | (b), (c)2, (d), (j) |
| W-5 | the `~` clause, the stop bytes, the `email_longest_ok` conditions untested | **Narrower and wider**: the `~` clause, the stop bytes other than whitespace and `c >= 0x80`, and `c != b'-'` are unguarded; `closed >= 1`, `!empty`, `len >= 2` ARE guarded (by the not-an-address lists) | (f) |
| W-6 | the L-3 rows guard only a tail | **Confirmed**; AE2-4 guards 6 bytes; AE2-5 guards one byte and in the over-mask direction | (f) |
| W-7 | evidence names the sample, not the kind | **Confirmed** with an over-mask plant (p7) whose failure contains AE2-1's evidence | (f) |
| W-8 | 372 × `a@b.test:x`: stored at base, refused at head | **Confirmed**: 4,091 bytes stored at base; head refused (4,835) | (h) |
| W-9 | squashed commits exist locally, no ref | **Confirmed**; a fetch-only repository of every GitHub branch lacks all three | (k) |
| W-10 | BACKLOG :1855 contradicts :1853 | **Confirmed** (older text) | (j) |
| W-11 | "near the limit" wider than 1,599 bytes | **Confirmed** (39% of the limit) | (h), (j) |
| W-12 | host masking in the doc comment only | **Confirmed** (AUDIT.md, M0, BACKLOG silent) | (j) |
| W-13 | the TLD file is unnamed | **Confirmed, and resolved**: found and hashed (path with the home part elided) | (k) |
| W-14 | figures without a count | (d) literal forms counted (11 by my leak check, 23 by the first check's analyzer, all named forms); ratios: one more run, 3.94-4.10, my four-size fits 0.99-1.00 | (b), (g) |
Drafter's readings that were wrong: none outright; W-5 is narrower on the `email_longest_ok` conditions (three of four are guarded) and wider on `c >= 0x80`.

## (a0) The head under test is the final head (TESTED): PASS
- `git rev-parse 5aa56e1^{tree}` in my clone (refs fetched from GitHub) = `e2a6436127f0610c3d866348cbed6c3913514b91`; `0c1ef5f^{tree}` = `6717d494875f6e381171ef64cd048e1e46712f4e`.
- Every head copy I built records, in its log before the build, `redact.rs` sha256 `2ba4ac7812f7ae78c0575e7e21f7dee599334fa03a856968998991874b4ef93f` = `git show 5aa56e1:crates/coagent-audit/src/redact.rs | shasum -a 256`. Opposite case shown once: `git show 0c1ef5f:…/redact.rs` hashes to `764e5953…f5367`; `git diff 0c1ef5f 5aa56e1` touches four files and, in `redact.rs`, only the two doc-comment lines `:740-741` (`mail.exämple.com` → `mail.exämple.test`). The base copies hash to `a40ced9f…ade5f`, the build brief's value.
- Rule on W-1: the builder's figures hold at the head. On the first check's corpus my run at `5aa56e1` gives the builder's exact numbers (identical 25,130, attributed 3,832, unattributed 0), and the first check's own analyzer, run on my probe outputs at `5aa56e1`, gives 1,294 → 140 and 1,679 → 80. The builder's own corpus and its 54,017 total I did not re-make; my own corpora give 0 unattributed over 53,607 inputs (property (e)).

## (a) Scope (TESTED): PASS
- `git diff --name-only d4979df 5aa56e1 -- . ` with the nine paths excluded: 0 lines; control (last exclusion dropped): 1 (`scripts/red-controls-audit.sh`).
- `redact.rs` (my `h/scope.py`, difflib on the base and head files): 37 removed lines, all inside `:7`, `:139`, `:250`, the base doc comment of `emails` (`:696-741`), its body (`:742-807`) or `email_domain_ok` (`:811-824`). Hunks: `:7`, `:139`, `:250`, then only inside 696-824.
- `find`'s diff is the one comment line (`// The owner's ruling: … (and summaries) as well.` → `// Email addresses (the owner's ruling, previews; the coordinator's ruling, summaries).`).
- `tests/ae_email.rs`: one delete of base lines 245-249, the five lines of the tuple `"address in a url query"` (as text the run removes `),` / `(` / name / text / text, the same five lines shifted by one, byte-equal result); head sha256 `044f280668218228ddfb15784990275b3f6aba07caa37e15f8242be6a8db5942` (the builder's value).
- `docs/AUDIT.md`: hunks at base `:37-40`, `:680-686`, `:882` only; base line 679 equals head line 680.
- `BACKLOG.md`: no removed or changed base line; inserts after base lines 369 (2), 1695 (1), 1844 (1), 1847 (3). `docs/M0-OUTCOMES.md`: one insert of 18 lines after base line 331; the base file (33,191 bytes) is a byte prefix of the head file (34,939 bytes).
- Red script: base rows 178, head rows 183 (counted inside `ROWS=(` by program); the 178 base rows equal the head's first 178 except rows 177-178, the AE-3/AE-3b evidence fields (`leaked` → `address: leaked`, `domain: leaked`); six lines appended before `)` (one comment, five rows); `MUTANTS` 2 rows at both, equal.
- `build.rs`: one insert before `];`: the comment line worded exactly as build brief line 49 prescribes, and the five names. Lines starting four spaces and `"`: 147 → 152. `Cargo.toml`: one comment line, `[[test]]`, `name = "ae2_email"`, after `name = "ae_email"`, before the blank line and `[lints]`.
- Bodies, by the first check's extractor `qa_bodies.py` (QA's, not the builder's): 40 items same (25 fns incl. the trait declaration, 15 `pub const`); not same: `find`, `emails`, `email_domain_ok`; new `email_longest_ok`, `email_xn`. Controls: `find` reported different (its comment line); a one-byte change planted in `hex_runs` of a scratch copy reported `DIFF fn hex_runs`. The head's items equal `0c1ef5f`'s item for item.
- Protected files: 23 × 2 SHAs = 46/46 equal to the build brief's values (`h/protected.sh`). Control: `tests/ae2_email.rs` at the base is reported `NOT-FOUND`, never hashed as empty. Host tree `7808b4ddc5414b6a3f592a7d647ee54a9de130e7` at both.
- `git diff d4979df 5aa56e1 -- Cargo.lock Cargo.toml`: 0 bytes. No new dependency. `unsafe` in the 866 added lines: 0; with one planted control line: 1. `git diff --name-only … -- crates/coagent-audit/src`: `redact.rs` only.

## (b0) The headline promise, attacked directly (TESTED): PASS, none in 53,607 inputs
- Search (my `h/qa2_diff.py`, section b0): for every input, the byte ranges of `patterns::find` at the base (on the clean text and on the clean window, moved to character boundaries as `apply_mask` moves them) must lie inside the head's; then, at output level, no base-masked stretch of 4+ bytes may appear in the head preview when the base preview did not show it. It stops at the first failing input and reports it.
- Result: 0 inputs on the first check's corpus (28,962), on my corpus (20,980; it includes 7,500 hostile inputs written for this: addresses masked by the old colon test (`: `, `:` at the end, `:` + newline) next to later `a@b.example:/x`, `<a>:x<b>:y/z`, long tokens before, colon chains, quotes, `://`, `?`, `#`, `~`, `.git`, non-ASCII, U+000B, between 2 and 14 fragments each) and on the literal corpus (3,665). Summaries: the model check below shows every stored summary equals the mask of the head spans, so the span search covers them.
- Why it holds (READ, structural): the other rules' bodies are byte-identical and `find` only unions spans; in `emails` the head skips an `@` only inside `[start, info)` with `info ≤ end` (the base skipped all of `[start, end)`); where the whole run passes the span is the base's; the head's colon test keeps an address only when the text after `:` is non-empty and starts with a non-stop byte, which is never ASCII whitespace, so the base kept it too. So the head's spans contain the base's for every input, not only the sampled ones.
- Control (opposite case): plant `pb0` (the colon test also keeps `<address>: `, after empty → `continue`) is reported on its first such input, `#55 colon-space`: `mail …@j3.auiv9i.exaMpLe.cOm: thanks` base `mail [REDACTED]: thanks`, plant shows the address. Counts: 386 (first check's corpus), 860 (mine), 23 (literals). The stale-index plant is also reported by this search (3 / 52 / 1), and `redact_no_url`, `redact_no_long`, `email_xn_case_sensitive` too.

## (b) Every address a person would read: my own attack (TESTED): PASS (every head survivor is in a class the doc comment names)
**My generator** (`h/qa2_corpus.py`, seed `0x2ae5eed2`, 20,980 inputs, 40 over 65,536 bytes): local parts 1-300 bytes over `[A-Za-z0-9._%+-]`; 2-6 labels under `example.com/org/net`, `.test`, `.invalid`, `.example` in every letter case; 8% the lane's own `shop.example.xn--qae0` in its four letter cases (the coordinator's ruling 8 label, quoted from `ae2_email.rs`; no other `xn--` label is used). Placements: the first check's 70 (rebuilt from its verdict :60-76) and 60 for this lane: links with no `/`, `?`, `#` after the host followed by `,` `;` `)` `|` `]`, a CSV row with a bare link column, `://` with no scheme, a port then `,`; query and fragment with no path; port + path; user-info + query; `mailto:` inside a link; `?next=https://<a>`; two links on a line; passwords holding `/`, `?`, `#`; `<a>:` followed by a path-first `%ae:%s` subject, `key:<a>:x/y`, a date path, `fix,see/notes`, `profile/v2`, `~`, `~user`, `repo.git`, `repo.GIT`, `repo.git,`, `(…repo.git)`, a port, a bare file, `:secret`, a later link in the same token, U+000B, U+00A0, a quote, `<`, a backtick before the `/`, a space before the `/`; and 14 glued forms. 80 of each, plus 7,500 hostile inputs (section b0) and 3,040 edge and long inputs.
**Leak check** (mine): a planted address counts as shown when the preview holds it whole, or (8 bytes or more) the `@` with a byte on each side, or any 8-byte window of it, each only when that text is not also in the rest of the input or in another planted address. Control: unmasked previews (strip + truncate only) flag 13,464 of 13,749 planted addresses; the other 285 lie past 240 characters and are still counted (a mask before them can pull them into view, as the window-end class shows).

| corpus | planted | shown at base | shown at head (preview) | head summary |
|---|---|---|---|---|
| mine (seed `0x2ae5eed2`) | 13,749 | 7,609 | **3,105** | 3,125 (40 refused) |
| the first check's (seed `0x0ae5eed`), my leak check | 10,232 | 3,001 | **231** (b 140, c 80, d 11) | 191 (240 refused at both) |
| the first check's, its own analyzer (copied, `python3 -I -B`) on my probe outputs at `5aa56e1` | (b) 8,172; (c) 2,000 | 1,294; 1,679 | **140; 80** | |

**Every head survivor, by why it is shown** (`h/qa2_why.py`, which re-derives the reason from the head grammar for each one; 0 "other"):
| class | my corpus | first check's | templates (n=80 each unless said) | preview | documenting line |
|---|---|---|---|---|---|
| U1 user-info to the token's end: no `/`, `?`, `#` between the `://` and the `@` (W-3) | 798 | 0 | `w3-comma`, `w3-semi`, `w3-paren`, `w3-pipe`, `w3-bracket`, `w3-csv`, `w3-csv2` (151), `w3-noscheme`; `w3-port-comma` shows the domain only (`https://[REDACTED]@<domain>`) | whole | doc comment `redact.rs:721-723` ("or the token's end") ONLY; `docs/AUDIT.md:686`, `docs/M0-OUTCOMES.md:336-337`, `BACKLOG.md:1853` say "to the first `/`, `?` or `#`" without it (finding L2-1) |
| U2 user-info, `@` before the first `/` (no password) | 0 | 1 | `https://user@host.example/` | whole | doc comment :724-725, AUDIT.md:686-687 |
| C1 `:` then `/` | 566 | 1 | hostile `idx`; `user@host.example.com:/path` | whole | doc comment :727-730; AUDIT.md:687-688; M0:338-340; BACKLOG:1853 |
| C1' glued to a following link (the run passes, then `:` + `//`) | 80 | 131 | `g-url`; `glued-url`, URL-with-password neighbour joined by nothing (50) | whole | doc comment :747-749; AUDIT.md:685; M0:343 |
| C2 `:` then `~` | 269 | 0 | `c-tilde`, `c-tilde-user`, hostile | whole | as C1 |
| C3 `:` then a token holding a later `/` (W-4) | 1,312 | 50 | `c-gitlog-path`, `c-date-path`, `c-comma-path`, `c-profile-v2`, `c-url-later`, `c-json-later`, `c-vt`; `<a>:https://…` neighbour (50) | whole | as C1 (by the rule "holds a `/`"); examples named nowhere |
| C4 `:` then a token ending `.git` | 80 | 0 | `c-git` | whole | as C1 |
| window end (64 KiB) | 0 | 40 | `window-after-mask` | `[REDACTED] <part>` | doc comment :746-747; AUDIT.md:685 |
| old not-caught forms (quoted, split, all-dots, non-ASCII, single-label, numeric) | 0 | 8 | (d) literals | whole or part | doc comment :737-746 |
Not shown at the head in my corpus (0 survivors): every link with a path, query or fragment, `<a>:` + a port, a bare file name, `:secret`, `:` + U+00A0, quote, `<`, backtick or space before the `/`, `repo.GIT`, `repo.git,`, `(…repo.git)`, and every glued form except a following link. The base count equals the planted set minus the base's accidental masks (`EMAIL=`, `--email=`, `curl -u`, long-token local parts, `session:`).
**Result:** no head survivor lies outside a class the doc comment of `emails` names, by rule or example. U1 is named by the doc comment's rule only; the three other documents leave out its "or the token's end" (L2-1, Minor). U1 and C3 are survivors made by the coordinator's rulings 1 and 2 (property (m)).

## (c) Each narrowed rule as new parsing code under a hostile author (TESTED; inputs in `h/qa2_dtab.py`, base and head probe outputs; every head answer equals my oracle)
**1. The user-info boundary (ruling 1)**
| input | base preview | head preview |
|---|---|---|
| `https://alice@example.org/x` (`@` before the first `/`) | kept | kept (user-info, no password) |
| `https://x.example/alice@example.org` | kept | `https://x.example/[REDACTED]` |
| `https://x.example?alice@example.org/p`, `…#alice@…/p` (`?`/`#` before any `/`) | kept | `https://x.example?[REDACTED]/p`, `…#[REDACTED]/p` |
| `https://bob:p?w@host.example.com/r`, `…p#w@…` | `https://[REDACTED]@host.example.com/r` | `https://[REDACTED]/r` (host masked too) |
| `see ://alice@example.org`, `x://alice@example.org` (`://` with no scheme letters) | kept | **kept** (any `://` opens a token) |
| `https://x.example/r?next=https://alice@example.org` (`://` inside a query) | `https://[REDACTED]@example.org` | `https://[REDACTED]` (the inner `://` is inside the first token; the `@` is after `?`) |
| `https://x.example.com/a alice@example.org https://y.example.com,bob@example.org` (two tokens) | first masked, second kept | same (the second is U1) |
| token cut by `"`, `'`, `<`, `>`, backtick, space, tab, `é` before the address | masked | masked (identical) |
| token NOT cut by U+000B: `https://x.example.com` U+000B `alice@example.org` | kept | **kept** (U+000B is not Rust ASCII whitespace) |
| `https://x.example.com:8443,alice@example.org` | `https://[REDACTED]@example.org` | same (domain shown) |
| `https://u:p@x.example.com?to=alice@example.org` | `https://[REDACTED]@example.org` | `https://[REDACTED]` |
**2. The colon test (ruling 2), clause by clause, and the stop bytes**
| input | head | clause |
|---|---|---|
| `a@b.example:~` / `a@b.example:x~` | kept / `[REDACTED]:x~` | `~` first only |
| `a@b.example:x/y` / `a@b.example:xy` | kept / masked | holds `/` |
| `a@b.example:x.git` / `a@b.example:x.gi` | kept / masked | ends `.git` |
| `a@b.example:`, `a@b.example: /x` | masked (as at base) | empty after |
| `a@b.example:x` + each stop byte (`"`, `'`, `<`, `>`, backtick, space, `é`, tab, LF, CR, FF) + `/y` | masked, all 11 | the `/` is past the token end |
| `a@b.example:x` U+000B `/y` | **kept** | U+000B is inside the token |
| `a@b.example:x` + `,` `;` `)` `]` `}` `|` + `/y` | **kept**, all 6 | not stop bytes |
| `a@b.example:c@d.example:e@f.example:/x` | all three kept | one token with a `/` |
| `a@b.example:x c@d.example:/y` / `a@b.example:/x c@d.example:y` / `c@d.example:z a@b.example:x/y` | first masked / second masked / first masked | the indexes move forward per token |
The two forward-only indexes (`redact.rs:852-859`): my oracle recomputes every answer from scratch; it agrees with `emails` on every input of all four corpora (55,000+ answers, including the 7,500 hostile inputs with chains of addresses and colons in one token). The stale-index plant is caught (property (e)).
**3. The longest valid prefix (`email_longest_ok`)**
| input | base | head |
|---|---|---|
| `a@b.example..x` / `a@.b.example` | kept / kept | `[REDACTED]..x` / kept |
| `a@b.c9`, `a@b.e9` | kept | kept (no letters label of 2+) |
| `a@b.xn---`, `a@b.xn--9` | `[REDACTED]---`, `[REDACTED]` | same (whole run passes) |
| `a@b.example-.9`, `a@b.xn--.9`, `a@b.xn--qae0-.9` | kept | `[REDACTED]-.9`, `[REDACTED]--.9`, `[REDACTED]-.9` |
| `a@1.example9`, `a@b-.example9`, `a@-b.example9`, `a@b.example.9`, `a@b.Example9-` | kept | `[REDACTED]9`, `…9`, `…9`, `[REDACTED].9`, `[REDACTED]9-` |
| **new over-masking:** `pkg@2.0.0.beta1`, `pip install torch@2.1.0.dev20231001`, `v@1.2.post1`, `x@self.weight2` | kept | `[REDACTED]1`, `pip install [REDACTED]20231001`, `[REDACTED]1`, `[REDACTED]2` |
| `pkg@1.2.3`, `pkg@1.0.0-beta.2`, `pkg@1.2.3-rc1`, `img@sha256:9f86d081`, `A@B.T` | kept | kept |
Item 4's "not an address" list: `ae2_not_an_address_is_still_kept` and `ae_what_is_not_an_address_is_kept_exactly` pass at the head (literal expected strings).
**4. A real address still shown and in NO documented class:** none found. The nearest are U1 (named by the doc comment's rule only; the shape a person meets: `url=https://api.example.com,user=alice@example.org,status=200`, a comma-joined key=value log line, or a CSV export with a bare link column) and C3 (`git log --format=%ae:%s` on a project whose subjects start with a path, kernel style: `alice@example.org:net/ipv4: fix the checksum`).

## (d) The documented answers, re-measured (TESTED at base and head; full table `logs/dtab.txt`)
Every example of the doc comment (`:696-760`), `docs/AUDIT.md:680-690`, `BACKLOG.md:1848`, `:1852-1854` and the M0 paragraph gives the documented answer at the head, among them: `...@example.com` kept; `alice@example.com-1`/`2026`/`--flag` → `[REDACTED]-1`/`2026`/`--flag`; `<a@b.example>`, JSON, `mailto:`, trailer, query, `.` `,` `)` `: ` → masked; `a@b.example:8080` → `[REDACTED]:8080`; `key:a@b.example:profile` → `key:[REDACTED]` (an older rule masks `key:` values at base and head, so this example does not isolate the new rule); `a@b.example:fix the build` masked; `https://user:pw@host.example/` → `https://[REDACTED]@host.example/`; `https://user@host.example/` kept; `git clone https://bob:pa/ss@host.example.com/r` → `git clone https://[REDACTED]/r`; `user@host.example.com:/tmp/x`, `git@host.example:org/repo`, `git@host.example:repo.git` kept; `user@host.example.com:file.txt` → `[REDACTED]:file.txt`; mentions, decorators, `pkg@1.2.3`, `a@b`, `user@localhost` kept; `"john doe"@example.com` and `alice@bücher.example` kept whole; `jörg@example.com` → `jö[REDACTED]`; `alice@mail.exämple.test` → `[REDACTED]ämple.test`; `aliceé@example.com` and `alice@exämple.test` (the "not at all" cases) kept; U+2066 before the `@` or in the domain kept; `%40`, `&#64;`, spelled, split, `a@localhost`, `a@[192.0.2.1]`, `a@b.examplehttps://x.example/p` kept; `name@file.rs`, `x@self.weight` masked. BACKLOG:1848's three window figures re-made exactly (`[REDACTED] Bearer [REDACTED]`, `[REDACTED] 9f86d081884c7`, `[REDACTED] ghp_16C7e42F2`, same at base). 
- W-2: `git@host.example:Repo.GIT`, `…repo.GIT`, `…repo.Git` → `[REDACTED]:…` (masked; the drafter's reading confirmed).
- W-3: `https://x.example.com,alice@example.org,bob@example.org` and `see https://x.example.com;alice@example.org` kept whole at the head (the URL rule masks nothing: no `:` before the `@`); with a `/` after the host (`https://x.example.com/,alice@example.org`) → masked.
- W-4: `alice@example.com:src/lib.rs`, `user:alice@example.com:profile/v2`, `alice@example.com:fix,see/notes`, `alice@example.com:2026-11-27/notes` kept whole; `alice@example.com:fix the build/tests` masked (the space ends the token).
- The first check's (d) rows at the head: glued hash and PEM → `[REDACTED]` (one mask; base showed part); colon + U+00A0, `)`, `,`, `"`, U+000B, CJK → masked; `user:…:profile`, `mail …:thanks` masked; `curl -u …:secret` → `curl -u [REDACTED]` at both; port query → `https://[REDACTED]`; link glued by `,` `)` `;` after a path → masked; `a@b.example-` → `[REDACTED]-`; `a@b.xn--` → `[REDACTED]--` at both.
- **R-1 control:** `https://bob:pw1234@host.example/r` → `https://[REDACTED]@host.example/r` at base and head; `git clone https://bob:hunter2pw@example.com/r` → `git clone https://[REDACTED]@example.com/r` at both. The harness is right.
Every documented answer behaves as documented.

## (e) My own differential of the old head against the new head, with my own oracle (TESTED): PASS
- Builds: base copy `xb` (`git archive d4979df` + my probe) and head copy `xh` (`git archive 5aa56e1` + my probe), each in its own empty target dir. Probe: the first check's `qae_probe.rs` copied with its `emails` columns on at both heads (the base has `patterns::emails` from the first lane); per input it dumps `find` on the clean text and the clean window, `emails` on both, `redact`, `preview`, the chain's stored summary or its refusal, and the full tier.
- **My oracle** (`h/qa2_diff.py`, `oracle`), written from build brief items 1-3 (lines 56, 62, 69) and rulings 1-2 on top of the first lane's grammar text, not from `emails`, `ae2_diff.py` or `qa_analyze.py`. Readings: user-info to the first `/`, `?`, `#` after the `://` or the token's end (ruling 1's words); the colon-test token end exactly as item 2 defines it (Rust `is_ascii_whitespace`, `"'<>` backtick, byte ≥ 0x80), so U+000B is inside the token; "ends `.git`" literally, lower case (the coordinator's ruling 4); `xn--` literally, lower case; the longest prefix found naively (every prefix tried from the longest), the span being that prefix trimmed of `.`/`-`, and the colon test applied at its end. A model of strip, `apply_mask`, `truncate` and the summary limits reproduces every probe answer at both heads: 0 mismatches over 53,607 inputs.
- **Attribution rule**, written into my STATUS before the first run: (i)-(iii) and (v) as the build brief words them; (iv) a new span gets the SET of old exclusions that, each tested alone on the base grammar, drop its `@` (1 link token, 3 strict prefix of the trimmed run, 2 the old colon test); attributed when the set is non-empty, multi-member sets reported apart; (vi) the head's `emails` spans equal my oracle with the code's `xn--` reading switched on (named decision D1). I also check (vi) on EVERY input, identical ones included, so a plant whose output equals the base is still seen.

| corpus | inputs | identical | attributed (link / link+colon / link+glued / colon / colon+glued / glued / other sets) | unattributed | oracle differences (every input) | more than one class |
|---|---|---|---|---|---|---|
| the first check's, seed `0x0ae5eed` (meta sha256 `3a12d6c6…a39605`, equal to its file) | 28,962 | 25,130 | 3,832 (638 / 36 / 50 / 1,801 / 0 / 1,307 / 0) | **0** | D1 1,202, other 0 | 86 |
| mine, seed `0x2ae5eed2` (40 inputs over 65,536 bytes) | 20,980 | 16,382 | 4,598 (1,691 / 106 / 6 / 1,666 / 30 / 1,098 / 1 link+colon+glued) | **0** | D1 834, other 0 | 143 |
| literals: `ae_email.rs` 238, `ae2_email.rs` 164, `gate_attacks.rs` 99, `gate_r2.rs` 142, `redaction.rs` 90 distinct (733) × the 5 placements of `redaction.rs:73-79` | 3,665 | 3,487 | 178 (45 / 5 / 0 / 68 / 0 / 60 / 0) | **0** | D1 10, other 0 | 5 |
| total | 53,607 | 44,999 | 8,608 | **0** | | 234 |

**Oracle differences, each a grammar decision of the code:**
- D1 `xn--` compared case-insensitively (the first lane's documented reading): 2,046 inputs in all. With it switched on my oracle agrees with `emails` on every input.
- `.git` letter case: the code reads it literally (lower case), as my oracle does: 0 differences. `.GIT` is masked (W-2).
- "starts with `/`" is never needed apart from "holds a `/`" (the second contains the first): 0 differences.
- The token end of the colon test: the code's equals item 2's definition: 0 differences (U+000B stays inside; reported under (c) and (m)).
- User-info delimiters `/`, `?`, `#` only: 0 differences (W-3 is the rule as worded).
- Item 3's colon test at a strict prefix's end: my oracle applies it and agrees on every input; it can never fire, because the byte after a strict prefix of the run is a domain byte, never `:` (STATUS Point 3 confirmed, by reasoning and by 0 differences).

**Planted loosenings** (each built in its own empty target dir; the cfg ones from the head copy with `COAGENT_AUDIT_RED`, every log showing `RED CONTROL BUILD`; the source ones as one edit, diffs `logs/plant_<name>.diff`):
| plant | unattributed: first check's / mine / literals | every-input oracle (other than D1) | (b0) promise search | first report |
|---|---|---|---|---|
| `redact_no_url` | 1,186 / 953 / 45 | 0 | 1,186 / 953 / 45 | first check's #38 `url-query-port`: base `https://[REDACTED]@…example.org`, plant `https://x.example.com:8443/c?to=[REDACTED]`: (i), (ii) |
| `redact_no_long` | 2,609 / 650 / 106 | 0 | 2,609 / 650 / 106 | #19 `sh-email-eq`: base `tool [REDACTED] --verbose`, plant `tool --email=[REDACTED] --verbose` |
| `email_xn_case_sensitive` | 1,028 / 790 / 10 | 0 (it equals my literal oracle; caught by (iii) and (vi) with the code's reading) | 834 / 385 / 10 | #1 `prose-end`: `…XN--za6ce5bpz` base `[REDACTED]`, plant `[REDACTED]--za6ce5bpz` |
| `email_no_dash_trim` | 24 / 2 / 5 | 28 / 2 / 5 | 0 (masks more) | #10010 `a@b.xn--`: base `[REDACTED]--`, plant `[REDACTED]`: (iii), (vi) |
| p7, `emails` takes the byte after the domain | 10,946 / 9,424 / 360 | 12,055 / 9,685 / 370 | 0 | mine #0: `Please ask [REDACTED] about…` → `…[REDACTED]about…`; spans `[(11, 65)]` vs oracle `[(11, 64)]` |
| pq, user-info ends at the first `/` only | **0 / 0 / 0** | 0 / **349** / **10** | 0 | mine #78 `l-query-nopath`: `https://x.example.com?to=<a>`: plant spans `[]`, oracle `[(25, 73)]` (output equal to the base, so only the every-input check sees it) |
| pg, colon test without `.git` | 0 / 81 / 4 | 0 / 81 / 4 | 0 | mine #100 `c-git`: `<a>:repo.git` base kept, plant `[REDACTED]:repo.git` |
| pt, colon test without `~` | 0 / 270 / 0 | 0 / 270 / 0 | 0 | mine #98 `c-tilde`: `<a>:~` base kept, plant `[REDACTED]:~` |
| pstale, `slash` not moved to `q` | 6 / 257 / 6 | 73 / 269 / 6 | 3 / 52 / 1 | mine #10757 `` `:/x@a@b.example: " ``: base `` `:/x@[REDACTED]: " ``, plant shows the address (a stale `/` keeps it) |
| pb0 (section b0's control) | 387 / 946 / 23 | 780 / 1,275 / 33 | 386 / 860 / 23 | mine #55 `colon-space` |
| `email_url_whole_token` | 0 / 107 / 5 | 741 / 1,808 / 50 | 0 | first check's #37 `url-query`: plant spans `[]`, oracle `[(27, 312)]` |
| `email_colon_any` | 2 / 137 / 5 | 2,173 / 1,963 / 78 | 0 | #15 `sh-curl-u`: plant `[]`, oracle `[(8, 30)]` |
| `email_whole_run_only` | 0 / 34 / 0 | 1,422 / 1,135 / 60 | 0 | #4194 `neigh-pwflag-after-''`: plant `[]`, oracle `[(2, 71)]` |
Every plant is reported on at least one of my corpora. On the first check's corpus pq, pg and pt are not reported (it has no `?`/`#` before a first `/` with an address, no `.git` without `/`, no `~` alone), as the builder found for pq and pg. pq is reported by no unattributed difference on any corpus: wherever it changes `emails`, the output equals the base's; only the every-input oracle check sees it. The three plants equal to the base on their own class are seen by the every-input oracle check and by (b)'s survivor count (they restore the base's survivors), and appear unattributed only where an input mixes classes.

**STATUS Point 8, judged:** the builder's oracle reads `xn--` case-insensitively and the token end as the code does (STATUS :52). Mine reads `xn--` and `.git` literally and takes the token end from item 2's words. They differ in reading only on `xn--` (D1, 2,046 inputs here), the first lane's documented decision, not a new one. "0 unattributed" does not rest on a reading only the builder's seat made: with my independent oracle and my class rule it holds on all three of my corpora.

## (f) Reverts and red rows (TESTED)
**Reverts with the builder's tests** (a tree `git archive 5aa56e1` + ONE edit to `src/redact.rs`, tests untouched, every `.rs` touched, own empty target dir; each log shows `Compiling coagent-audit`; run: `ae2_email`, `ae_email`, `redaction`, `gate` (it compiles `gate_attacks.rs`), `gate_r2`; diffs `logs/revert_<name>.diff`):
| # | edit | test red | first panic line | red on its own assertion? |
|---|---|---|---|---|
| 1 | `~` clause removed | **none** (all 5 targets pass) | — | **unguarded**; not equivalent: `a@b.example:~` head kept, mutant `[REDACTED]:~` (masks more) |
| 2 | `.git` clause removed | `ae2_addresses_before_a_colon_are_masked` | `AE2-2: ends .git: scp target with a path changed: "git remote add o git@host.example:repo.git" -> "git remote add o [REDACTED]:repo.git"` | yes |
| 3 | `?` removed from the delimiters | `ae2_addresses_in_links_are_masked` | `AE2-1: query with no path: link address: "https://x.example.com?to=alice@example.org" -> "https://x.example.com?to=alice@example.org"` | yes |
| 4 | `#` removed | same | `AE2-1: fragment with no path: link address: "https://x.example.com#alice@example.org" -> …` | yes |
| 5 | `stop` reduced to ASCII whitespace | **none** | — | **unguarded**; not equivalent: `a@b.example:x"/y` head `[REDACTED]:x"/y`, mutant keeps the address (6 of my literal inputs differ) |
| 6 | `c >= 0x80` removed from `stop` | **none** | — | **unguarded**; not equivalent: `a@b.example:xé/y` head masked, mutant keeps it |
| 7 | `closed >= 1` → `>= 0` | `ae2_not_an_address_is_still_kept`, `ae_what_is_not_an_address_is_kept_exactly` | `AE2-6: single-label domain: not an address: changed: "ssh user@localhost" -> "ssh [REDACTED]"` | yes |
| 8 | `!empty` removed | same two | `AE2-6: empty label: not an address: changed: "bob@example..com" -> "[REDACTED]"` | yes |
| 9 | `c != b'-'` removed | **none** | — | **unguarded**; not equivalent: `a@b.xn--.9` head `[REDACTED]--.9`, mutant `[REDACTED].9` (masks more) |
| 10 | `label.len() >= 2` → `>= 1` | same two as 7 | `AE2-6: one-letter last label: not an address: changed: "bob@example.c" -> "[REDACTED]"` | yes |
| 11 | stale `slash` | `ae2_old_previews_are_kept_as_written` | `control: a new event is masked by the new rule: [(4, "event 4: open https://example.com/c?to=alice@example.org then alice@example.com:fix"), (5, "event 5: open https://example.com/c?to=[REDACTED] then alice@example.c…` | yes, on the new-event assertion, by chance of its sample (the link's `/` is the stale one) |
No mutant is equivalent: each has a distinguishing input (above or in (e)). W-5 is confirmed and wider than the drafter read: besides the `~` clause and the stop bytes, `c >= 0x80` and `c != b'-'` also have no test; the other conditions of `email_longest_ok` (`closed`, `empty`, `len`) are guarded by the not-an-address lists. Mutants 5 and 6 are loosenings (an address is kept); 1 and 9 mask more.

**The five red names by hand** (`COAGENT_AUDIT_RED=<name> cargo test --locked -p coagent-audit --test ae2_email -- --exact <test>`, one target dir, each log `RED CONTROL BUILD` and `Compiling coagent-audit`, exit 101). Whole failure texts:
- `email_url_whole_token`: `assertion `left == right` failed: AE2-1: query: link address: "open https://example.com/c?to=alice@example.org now" -> "open https://example.com/c?to=alice@example.org now"` / `left: "open https://example.com/c?to=alice@example.org now"` / `right: "open https://example.com/c?to=[REDACTED] now"`.
- `email_colon_any`: `… AE2-2: git log %ae:%s: colon address: "alice@example.com:fix the build" -> "alice@example.com:fix the build"` / left the same / right `"[REDACTED]:fix the build"`.
- `email_whole_run_only`: `… AE2-3: dash digit: glued address: "alice@example.com-1" -> "alice@example.com-1"` / right `"[REDACTED]-1"`.
- `email_xn_case_sensitive`: `… AE2-4: upper case: xn-- label: "user@shop.example.XN--QAE0" -> "[REDACTED]--QAE0"` / right `"[REDACTED]"`.
- `email_no_dash_trim`: `… AE2-5: xn-- label then a dash: trailing dash: "user@shop.example.xn--qae0-" -> "[REDACTED]"` / right `"[REDACTED]-"`.
Each failed on the preview assertion of `check_masked` (`ae2_email.rs:44`, the `-> "…"` form), none on the `no span` assertion.
- **W-7, ruled: confirmed.** Both assertions print `"{tag}: {name}: {what}…"`, so the row evidence (`AE2-1: query: link address`) matches a kept address, an over-mask and a missing span alike. Shown: the p7 tree (an over-mask: the byte after the domain eaten) fails `ae2_addresses_in_links_are_masked` with `AE2-1: query: link address: "open https://example.com/c?to=alice@example.org now" -> "open https://example.com/c?to=[REDACTED]now"`, which contains the row's evidence. Note.
- **W-6, ruled: confirmed, narrower for AE2-5.** Under `email_xn_case_sensitive` AE2-4's sample shows `--QAE0` (6 bytes, the tail of a made-up top label; the local part and the rest of the domain stay masked). Under `email_no_dash_trim` AE2-5's sample shows nothing: the red variant masks one byte MORE (`[REDACTED]` instead of `[REDACTED]-`), so that row guards an exact output, not a leak.
- AE-3 / AE-3b: the evidence fields are `address: leaked` and `domain: leaked`; by program (`grep -A12 'panicked at' | grep -cF`): AE-3b's evidence against AE-3's failure text 0, AE-3's against AE-3b's 0; each against its own 1.

**The whole audit red runner at the head** (heavy counter 0 before; `bash scripts/red-controls-audit.sh` from the head copy's root through `qae2/rr.sh`, `COAGENT_AUDIT_RED_TARGET=/private/tmp/claude-501/qae2/red-t`, `COAGENT_AUDIT_RED_LOGS=/private/tmp/claude-501/qae2/red-logs`; 02:59:02 to 03:32:44): `rows: 183 cfg rows + 2 source-mutant rows`; **185 `RED`, 0 `NOT-RED`**; `GREEN: 323 tests ok`; `RED CONTROLS OK: every guard went red under its control, on its property, and green without`; `exit=0`. Every cfg log shows `RED CONTROL BUILD`; both mutant logs show `MUTANT APPLIED`; every path in the logs is under `/private/tmp/claude-501/qae2`. Rows counted by program: 178 at the base, 183 at the head (see (a)). The five lane rows' first evidence lines are the ones quoted above (identical to the hand runs). **PASS.**

## (g) Linear time (TESTED, release)
- The builder's test (`cargo test --release --locked -p coagent-audit --test ae2_email -- --ignored --exact ae2_email_time_scales_linearly --nocapture`, own target `qae2/trel`): exit 0, `1 passed`. µs at 64/128/256 KiB, `emails` | `redact`: `a@` 339/678/1357 | 3585/7169/14385; `a.`…`@b.example` 140/280/563 | 5274/10555/21118; `@` 173/346/695 | 2114/4217/8438; local run 52/104/209 | 2318/4671/9362; `a@b.` 345/690/1414 | 3526/7060/14150; `x://a@` 165/331/664 | 2947/5885/11890; every rule 69/138/273 | 3204/6452/12791; `a@b.example:`…`/` 266/536/1075 | 3806/7628/15262; link + `a@b.example/`… 200/396/788 | 3554/7094/14207; `a@`+`a.`…+`9` 260/524/1056 | 5443/10856/21727; `a@b.example9` 377/752/1502 | 3537/7101/14206. The first lane's `ae_email_time_scales_linearly`: `a@` `emails` 339/678/1357 µs (= AUDIT.md's 0.34/0.68/1.36 ms).
- My families (`h/qae2_time.rs`, best of 3, 64/128/256/1024 KiB, least-squares exponent; heavy counter 1 during):
| family | `emails` µs 64/128/256/1024 | exp | `redact` exp |
|---|---|---|---|
| B1-B11 (the builder's eleven) | e.g. `a@` 339/678/1358/5435; `a@b.example9` 376/750/1490/5943 | 0.99-1.00 | 1.00 |
| I1 `a@b.example:` ×n, no stop, no `/` (token end runs to the text end once) | 273/544/1085/4334 | 1.00 | 1.00 |
| I2 `a@b.example:x ` ×n (a stop each time) | 175/348/691/2754 | 0.99 | 1.00 |
| I3 one `://` token, `@` every 3 bytes, no `/?#` | 104/208/417/1665 | 1.00 | 1.00 |
| I4 many `://` tokens, `/` late in each | 93/185/372/1462 | 0.99 | 1.00 |
| I5 `a@b.example:c` ×n then a stop | 271/538/1073/4284 | 1.00 | 1.00 |
| P1 `a@` + `ab.`×n + `9` (best prefix moves every label) | 274/544/1091/4348 | 1.00 | 1.00 |
| P2 `a@b.` + `xn--`×n | 162/340/668/2641 | 1.00 | 1.00 |
| P3 `a@` + `-`×n | 173/349/701/2767 | 1.00 | 1.00 |
| P4 `a@b.example-1` ×n (a prefix each time) | 375/747/1493/5966 | 1.00 | 1.00 |
- **Control:** the builder's by-hand plant (`tok_end = q; slash = q;`) built into my harness (copy `gq`): I1 207,051/827,755/3,323,778 µs → exponent **2.00**; B8 2.00; I5 2.00 (64-256 KiB). My harness sees a quadratic index.
- **PASS:** every exponent 0.99-1.00; no family near 1.5. W-14's "3.9 to 4.1": in my one run of the builder's test the 22 ratios 256/64 lie between 3.94 and 4.10 (one more run, not a repeat series) (and my four-size fits are 0.99-1.00).

## (h) The format, old records, and summaries (READ + TESTED)
- `git diff d4979df 5aa56e1 -- crates/coagent-audit/src` touches `redact.rs` only. `git grep -n -E '\.redact\(|preview\('` over `crates/coagent-audit/src` and `crates/coagent-audit-host/src` (READ, the scope run): `chain.rs:236`, `chain.rs:245`, `redact.rs:93`, `redact.rs:98` at both SHAs (the files outside `redact.rs` are byte-identical, the protected and host-tree checks of (a)); positive control: `chain.rs:245` is found. **R-4's proviso holds**: the redactor runs only when an author prepares its own event; no stored field, encoding or verify step changes.
- `ae2_old_previews_are_kept_as_written`, READ whole and run (green in the head suite; also the revert that catches the stale index, (f) #11). What it does NOT show: the "old build" is an identity redactor in the same binary, not a build of `d4979df`; no real old-build daemon was run (the coordinator's ruling 3: not required); summaries are not checked by it.
- **Summaries, W-8** (TESTED through `AuthorChain::prepare`, my probe; every address reserved):
| text | raw bytes | base | head |
|---|---|---|---|
| 372 × `a@b.test:x` joined by spaces | 4,091 | stored, 4,091 bytes | **refused `FieldLimit("summary")`** (redacted 4,835) |
| 371 × `a@b.test:x` | 4,080 | stored, 4,080 | refused (4,822) |
| 455 × `a@b.test` | 4,094 | refused (5,004) | refused (5,004) |
| 400 × `K=v` | 1,599 | refused (5,199) | refused (5,199) |
| 1,024 × `K=v` | 4,095 | refused (13,311) | refused (13,311) |
The builder's figure (372 × `a@b.test:x`, 4,091 → 4,835, stored at base, refused at head) is re-measured exactly. What the caller gets (READ at the head): the daemon sends `summary: None` (`crates/coagent-daemon/src/audit.rs:831`), so no daemon send carries a summary. A program using the library through the host: `host.rs:529-546` builds the `EventInput` with the caller's summary and returns `m.record(…)?` / `m.record_for(…)?` as it is ("P-6: a refusal is returned as it is; never retried"), so the caller gets `Err(Audit(FieldLimit("summary")))`, nothing is recorded for that event, and it must send it again (for example without the summary). **For the owner:** through the daemon a user sees nothing different; a program using the library directly can now get an error for a summary near the limit that holds addresses in links, before a colon or glued, and that one event is not recorded until it is sent again. The documents say only that summaries near the limit can be refused (AUDIT.md:38-40), not that a summary the old version stored can now be refused: Note N2-3.

## (i) The owner's ruling, in words (TESTED, by program: case-insensitive `owner` over the added lines and the commit message, `h/qa2_sent.py`)
| file:line | words | verdict |
|---|---|---|
| docs/AUDIT.md:37 | "(the owner's ruling, previews; the coordinator's ruling, summaries)" | PASS |
| docs/AUDIT.md:886 | "the owner's ruling (previews); the coordinator's ruling (summaries, the grammar)" | PASS |
| BACKLOG.md:370 | "the owner's ruling covers previews, and masking summaries is the coordinator's ruling" | PASS |
| redact.rs:250 | "(the owner's ruling, previews; the coordinator's ruling, summaries)" | PASS |
| redact.rs:696 | "(the owner's ruling, previews; the coordinator's ruling, summaries and the grammar below)" | PASS |
| build.rs:166 | "(the owner's ruling: email addresses blanked)" (prescribed word for word by build brief line 49) | PASS |
| ae2_email.rs:2 | "(the owner's ruling: email addresses blanked in previews)" | PASS |
| commit l.3 | "The owner's ruling blanks email addresses in previews; summaries and the grammar are the coordinator's ruling." | PASS |
None says more than "Yes, blank email addresses" for previews.

## (j) Every claim the lane wrote, matched to a run (TESTED; keywords: is masked, masked, is kept, kept, not caught, never, every, only, whole, unchanged, as before, neither, near, refused; 45 lines in `logs/sentences.txt`)
| file:line | claim | my run | verdict |
|---|---|---|---|
| AUDIT.md:686, M0:336-337, BACKLOG:1853, commit l.5-6 | "an `@` in a link's user-info part (from the `://` to the first `/`, `?` or `#`) is left to the URL rule" | (b) U1: with no `/?#` after the host the user-info part runs to the token's end (798 survivors in my corpus); the doc comment (:721-723) says "or the token's end", these four do not | **narrower than the effect: Minor L2-1** |
| M0:334-336 | "an address in a link, one followed by a colon and more text, and one with more domain characters glued after it were kept. Under the coordinator's ruling each is now masked" | U1, C3 and glued-to-a-link remain kept; the following sentences qualify it | true as qualified, wider in isolation: Note |
| M0:341-343, BACKLOG:1853 | "On the independent check's corpus … fall from 1,294 to 140 … and from 1,679 to 80; what remains is … glued to a following link, … followed by `:` and a link, and … cut by the 64 KiB window end" | re-measured at the head on that corpus: 140 = 50 + 50 + 40, 80 glued-url (and 11 literal forms in its (d) section, named elsewhere) | true as scoped to that corpus; my corpus adds U1 and C3: Note (W-4) |
| M0:343-345 | "Every other rule answers as before: over 54,017 inputs the old and new redactor differ on 15,483, … (0 unattributed)" | the builder's figure, measured on `0c1ef5f` (equal bodies); not re-made. Mine: 53,607 inputs, 8,608 differ, 0 unattributed. "Every other rule" is covered by the structural proof (byte-identical bodies, `find` unions) | true; figure the builder's |
| M0:345 | "Logs already written are kept as written" | (h): grep four lines at both; the test passes | true (identity-redactor stand-in, as the first check) |
| AUDIT.md:38-40, BACKLOG:371 | "a summary near the limit can be refused; older rules already do this (400 `K=v`, 1,599 → 5,199), and so do addresses (455 × `a@b.test`, 4,094 → 5,004)" | re-measured exactly; 1,599 bytes is 39% of the limit | figures true; "near the limit" wider than its example: Note (W-11); silent on summaries stored before and refused now: Note (W-8) |
| AUDIT.md:687-689 | "an scp target with a path is not masked (…); an address in a link's path, query or fragment, `<address>:<port>`, an scp target with a bare file name, and an address with domain characters glued after it are masked" | (c), (d) | true (glued to a link is named two lines above) |
| AUDIT.md:886 | "0.34/0.68/1.36 ms for 64/128/256 KiB of `a@`, one release run on one machine, 2026-11-26" | my run 339/678/1357 µs | true |
| doc comment :709-712 | longest valid prefix | (c)3, (e) | true |
| doc comment :721-726 | user-info part; "a password holding a `/` ends the user-info part early, so its host is masked as an address too" | (c)1 | true; the documents other than the doc comment do not say it (W-12): Note |
| doc comment :727-732 | scp target with a path; `user@host.example.com:file.txt` is masked | (c)2, (d) | true |
| doc comment :733 | "version pins (`pkg@1.2.3`): no prefix of the domain run has a last label of letters" | (c)3: true by rule; pins with a letters label (`pkg@2.0.0.beta1`) are now masked | true |
| doc comment :737-749 | the not-caught list | (d) | true |
| doc comment :755-760 | linear time, two forward-only indexes | (g), control 2.00 | true (REASONED in the code, measured here) |
| redact.rs:7, :139 | "credential or an email address", "credential shapes and email addresses" | | true |
| BACKLOG:1848, :1852, :1854 | window figures; non-ASCII correction; invisible characters | (d) | true |
| "an scp target with a path is not masked" (AUDIT.md:687, M0:339, BACKLOG:1853, doc comment) | | true by the stated test; `.GIT` and `repo.git,` are masked (W-2) | true |
| commit l.7-10, l.19-20 | the colon and glued rules; doc comments no longer call every pattern credential-shaped | (c), (a) | true |
| BACKLOG:1855 (older text, not the lane's) | "Why deferred: … URL tokens left to the URL rule, scp targets not masked" | contradicted by :1853 | Note for a later lane (W-10) |

## (k) Names, ids, fixtures, history (TESTED)
- Byte scan (`h/qa2_scan.py` + `h/run_scan.sh`, outside the repository; words given on the command line at run time, never written to a file): the login name, the host names (three forms), the home path; the owner's name parts and account name; the personal and three public mail domains plus the client's domain and the agent mail domain; seven seat-day names (the coordinator seats among them); the drive name, `Development`, `!CODING`, the vault folder, the workspace folder, the coordinator's folder names; two client names; 54 folder names taken at run time from levels 1-2 under the workspace's `!CODING` (86 words). Each plain, slugged, URL-encoded (three ways), backslash-escaped, as UTF-16LE, any case. Files: the 866 added lines, the commit message, the nine files whole at the head.
  - Controls: a scratch copy of `ae2_email.rs` with a planted `// planted control: <short host name>` line → found (3 words); a 624-byte random binary holding the login name as UTF-16LE → found (5 words).
  - **Added lines and commit message: 0 hits** for any person, account, machine, seat, client or project name. The only hits there are generic folder words: `encoding` (from the slug of `!CODING`) in an added line of `docs/AUDIT.md` ("an unusual encoding"), and `doc` in the commit message.
  - Older lines (counts equal at both SHAs, not graded): a coordinator seat name 45/2/1 times in BACKLOG/AUDIT.md/M0.
- Addresses: every `@` + dotted domain in the added lines and the commit message outside the reserved names: version pins `1.2.3` (5), `18.0.0` (2); decorator `app.route`; over-masking examples `file.rs`, `self.weight`; malformed on purpose `example.c`; glued forms on a reserved name (`example.com-1`, `…2026`, `….1`, `…-backup2`, `…-old`, `…--password`, `…--flag`, `…9f86…`, `…550e8400-…`, `…-----BEGIN`, `example.comhttps`, `b.examplehttps`, `b.example9`); `mail.ex…` (the regex stops at `ä` of `alice@mail.exämple.test`, reserved); the coordinator's ruling 8 label `shop.example.XN--QAE0` / `Xn--qae0` / `xn--qae0` (and `xn--qae0-`); `anthropic.com` in the `Co-Authored-By:` trailer (the repository's convention, the first check's N-10). None is a mailbox. The builder's list (STATUS :253) is confirmed.
- **The coordinator's ruling 8:** `xn--qae0` in any case appears only in `tests/ae2_email.rs` (`git grep -i` at the head: lines 11, 314, 317, 320, 335; none at the base). Python's `idna` and `punycode` codecs refuse it ("incomplete punycode string"). **W-13:** the list the builder used exists on this machine: `<home>/.cache/uv/archive-v0/<id>/hypothesis/vendor/tlds-alpha-by-domain.txt` (the `hypothesis` package's vendored IANA file), header `# Version 2026100300, Last Updated Sat Oct  3 07:07:01 2026 UTC`, 1,437 names, 151 starting `XN--`, sha256 `f9816a9e5f92191d4a3d73045a579f57eda381dd1ad7b4c535505c7ec610218c`; `grep -i -x xn--qae0` exit 1: not in it. Not checked against the live registry (no network by rule).
- **History, W-9:** a new empty repository (`qae2/gho`) fetched every branch from GitHub (deploy key): `git cat-file -t 0c1ef5f`, `52879c7`, `afb1600` → "Not a valid object name" each (missing); opposite case `5aa56e1` → `commit`. In the project's own object store all three are `commit` and `git for-each-ref --contains` prints 0 refs for each; `git grep -c 'mail.exämple.com'` finds the non-reserved name in `0c1ef5f` (`redact.rs` 1) and `52879c7` (`BACKLOG.md` 1, `redact.rs` 1), not in `afb1600` or `5aa56e1`. GitHub does not serve them: Note (the coordinator's ruling 7). Whether GitHub ever received them as unreachable objects cannot be seen from a fetch.
- Card ids in added lines and the commit message: 0; control: 8 in `git show d4979df:BACKLOG.md`; a planted made-up id: found. Absolute paths (`/users/|/volumes/|/private/|~/`, any case): 8 hits, all test strings (`https://example.com/users/@alice:profile`, `user@host.example.com:~/x`), none a drive path; control (a planted `/Volumes/x`): found. Commit author: the repository's configured owner identity (a GitHub no-reply address), the same on all 431 commits of the base (a fact).

## (l) Suite, clippy, fmt (TESTED)
- Head: `cargo fmt --all --check` exit 0; `cargo clippy -p coagent-audit --all-targets --locked -- -D warnings` exit 0 (the only warning: the workspace manifest's unused `rand_core`, pre-existing).
- `cargo test -p coagent-audit -p coagent-audit-host --locked --no-fail-fast`, own empty target dirs, every `test result` line summed by program: **base 388 passed / 0 failed / 15 ignored in 51 targets** (+2 doc-test runs of 0), exit 0; **head 395 / 0 / 16 in 52**, exit 0. The only per-target difference: `ae2_email` (7 passed, 1 ignored); `ae_email` 4 passed, 1 ignored at both (its not-address test still one test).
- `gate_r2` report tests (`-- r2_report_redaction --nocapture --test-threads=1`) at base and head: output identical line for line; `kept    scp: "scp build.tar user@host:/tmp/x" …` and `kept    url with @path: "https://example.com/users/@alice:profile" …` at both; both green.
- Daemon (the coordinator's ruling 2, head only): `cargo build --workspace --bins --locked` exit 0, then the 13 `an_*`/`aw_*` targets (`git ls-tree` at the head): **20 passed / 0 / 0**, per target 1,2,1,2,1,1,3,1,2,1,4,1,0, exit 0 (the builder's figure). Disclosure: my first attempt passed the 13 `--test` flags as one word (a shell quoting slip) and ran 78 targets with 0 tests matched; I re-ran with a proper argument list; the figure above is the second run.

## (m) Findings against the coordinator's rulings themselves (TESTED where a run exists; apart from the lane's findings)
Frequencies are per template of my corpus (80 inputs each), not real-world rates (unmeasured).
- **Ruling 1 (user-info to the first `/`, `?`, `#` or the token's end): RM-1, Minor.** A link with no path, query or fragment followed in the same whitespace-free token by an address keeps the address whole, and the URL rule masks nothing (no `:` before the `@`): `url=https://api.example.com,user=alice@example.org,status=200` (a comma-joined key=value log line), `https://x.example.com,alice@example.org` (a CSV row with a bare link column), `see https://x.example.com;alice@example.org`, `…)`, `…|`, `[…]`. Also any `://` with no scheme letters (`see ://alice@example.org`) and a token joined by U+000B. 80/80 kept in each of 9 templates (798 in all); with a port the domain shows (`https://[REDACTED]@example.org`, 80/80). Masks more, also from this ruling: a password holding `/`, `?` or `#` now hides the host name (`git clone https://[REDACTED]/r`): a Note (a reader loses the host; nothing leaks).
- **Ruling 2 (the colon test): RM-2, Minor.** An address followed by `:` is kept when anything later in the same whitespace-free token holds a `/` (the token does not stop at `,` `;` `)` `]` `}` `|` or U+000B): a `git log --format=%ae:%s` line whose subject starts with a path (kernel style `alice@example.org:net/ipv4: fix the checksum`, or `alice@example.com:src/lib.rs: …`), `user=alice@example.org:ok,url=http://x.example.com/`, `key:<a>:x/y`, `<a>:2026-11-27/notes`, `<a>:fix,see/notes`: 80/80 in each of 7 templates, 1,312 C3 survivors in my corpus (+566 C1 in the hostile inputs). `~` alone keeps it too (`<a>:~`, `<a>:~user`: 269). Over-masking from the same ruling (Notes): `user@host.example.com:22` and `user@host.example.com:file.txt` now hide the user and host of an ssh/scp target a reader may need; `git@host.example:Repo.GIT` (W-2, upper case) and `(git@host.example:repo.git)` / `…repo.git,` (the `)` or `,` ends the token text, so it no longer "ends `.git`") are masked.
- **The longest-valid-prefix rule (item 3, the coordinator's lane ruling): RM-3, Note.** It newly masks version pins and expressions with a letters label: `pkg@2.0.0.beta1` → `[REDACTED]1`, `torch@2.1.0.dev20231001` → `[REDACTED]20231001`, `v@1.2.post1` → `[REDACTED]1`, `x@self.weight2` → `[REDACTED]2`. Usual npm and Go pins (`pkg@1.2.3`, `pkg@1.0.0-beta.2`, `pkg@1.2.3-rc1`) stay kept.
- **Ruling 3 (the first lane's test file): Note.** The doc comment of `effective_join` (`tests/ae_email.rs`, head :412-419) still says its generator avoids shapes "the rule does not catch by design" (colon, glued), which are now caught (the builder's "Doc lines owed", STATUS :267). No effect on results.
- **Ruling 8 (the `xn--` label): none found.** `xn--qae0` is used in `ae2_email.rs` only, is not in the 2026-10-03 top-level list on this machine, and is not valid punycode for Python's codecs.
- Rulings 4, 5, 6, 7, 9, 10, 11: none found (I checked the AE-3/AE-3b fields, the `:7`/`:139` words, the N-1 BACKLOG line with `is_format_char` unchanged, the appended records lines, the one `find` line, the names, and the base recount, which I re-made: 1,294 and 1,679 at `d4979df`).
No ruling finding is Major by effect: the two kept classes need a path-less link or a `/` later in the same token, both narrower than the first check's RF-1 (every link) and RF-2 (every colon).

## Every figure of the builder's STATUS
| figure | STATUS line | re-measured? |
|---|---|---|
| base 388 / 0 / 15 in 51 targets | :22 | re-measured: 388 / 0 / 15 in 51 |
| head 395 / 0 / 16 in 52; difference `ae2_email` 7 + 1; `ae_email` 4 + 1 | :163 | re-measured: equal |
| daemon 20 passed in 13 targets (1,2,1,2,1,1,3,1,2,1,4,1,0) | :23, :164 | re-measured at the head only: equal; base not run |
| base red run 178 + 2 rows, 180 RED, GREEN 316 | :24 | rows counted by program (178, 2); the base run itself the builder's, not re-run |
| head 183 + 2 rows, 185 RED, 0 NOT-RED, GREEN 323 | :166 | re-measured: equal |
| item 0 answers (eight texts, three L-1 examples) | :28-34 | re-measured at base (dtab): equal |
| 630 / 450 / 174 / 40 = 1,294 of 8,172; 1,679 of 2,000 (base) | :37 | 1,294 and 1,679 re-measured (class split not re-made) |
| 28,962 / 25,130 identical / 3,832 attributed / 0; classes 724 / 1,801 / 1,307 | :93 | re-measured at the HEAD: 25,130 / 3,832 / 0; inputs with link 724, colon only 1,801, glued (incl. window-only) 1,307 |
| own 21,400 / 9,922 / 11,478; lit 3,655 / 3,482 / 173; total 54,017 / 38,534 / 15,483 | :94-96 | the builder's, not re-run (its corpus not re-made); mine: 20,980 / 16,382 / 4,598; 3,665 / 3,487 / 178 (733 literals vs 731); 53,607 / 44,999 / 8,608; 0 unattributed |
| plant table (c1 / own / lit unattributed and oracle counts) | :102-108 | first-check-corpus column re-measured for `redact_no_url` 1,186, `email_xn_case_sensitive` 1,028, `email_no_dash_trim` 24, p7 10,946, pq 0, pg 0 (equal); `redact_no_long` 2,609 (equal); oracle columns differ by construction (my oracle); own/lit columns the builder's |
| survivors 1,294 → 140 (114 + 20 + 6), 1,679 → 80 | :111 | re-measured at the head: 114 + 6 + 20 = 140; 72 + 6 + 2 = 80 |
| "(d) literal forms: the remaining survivors are the documented not-caught forms" (no count) | :111 | counted (W-14): 11 shown by my leak check, 23 by the first check's analyzer (16 whole, 1 part, 6 domain; it also counts non-`@` planted strings), every one a named not-caught form |
| the 40 bodies same | :113 | re-measured with the first check's extractor: 40 same |
| eleven timing families, ratios 3.9-4.1 | :156-158 | re-measured: close (within about 8% per point); 22 ratios 3.94-4.10; my fits 0.99-1.00 |
| by-hand prescan 206,943 / 833,361 / 3,323,655 µs | :159 | re-measured in my harness: 207,051 / 827,755 / 3,323,778 (exp 2.00) |
| 400 × `K=v` 1,599 → 5,199; 455 × `a@b.test` 4,094 → 5,004; 372 × `a@b.test:x` 4,091 → 4,835 | :149 | re-measured: equal |
| N-8 window figures | :148 | re-measured: equal |
| 550 / 9,934 / 36 changed-answer entries (122 port, 4,414 password) | :62 | the builder's, not re-run |
| 1,437 and 151 names in the TLD list | :46 | re-measured on the file named in (k): 1,437 and 151 |
| `ae_email.rs` head sha256 `044f2806…` | :78 | re-measured: equal |
| bodies sha256 prefixes (`b15ec77e…` etc.) | :113 | not comparable (a different extractor); same/different verdicts equal |

## The builder's disclosures, ruled
- **Point 11 (`rm -f /tmp/x`):** the rule that applies is the seat's launch prompt ("Never delete (quarantine)"), which the removal broke. The builder says the file was its own, seconds old, written by a stray `printf`. `/tmp` is shared by every seat on this laptop; whether another process had a file of that name, and what was removed, cannot be verified now (no `/tmp/x` exists). Note N2-8.
- **Point 12 (edits before item 0):** the builder's log times (READ, `tools/tmp/ae2/f12673/logs`): `base_check.log` 20:57:13, item 0 (`pb_item0.log`) 20:57:45, the recount 20:58:42, the base crate tests 21:22:49, the base red run 21:57:30; the first head build log (`head_ae_first.log`) ends 21:58:49, after every base gate. So nothing of the head was BUILT before the gates, as it says; the drafts were EDITED before item 0, against build brief line 53 ("before any edit") taken literally. Note N2-8.
- **The squash** (`git reset --soft d4979df` + one commit before the push): trees equal (`afb1600^{tree}` = `5aa56e1^{tree}`); the three squashed commits are not served by GitHub ((k)); the measured figures hold at the head ((a0)). Note N2-7.

## For the owner, in plain words
**What changed:** in the audit log's short previews (and summaries), an email address inside a web link's path or query (`…/unsubscribe?email=<address>`), one followed by a colon and text (`<address>:fix the build`, `user:<address>:profile`, `<address>:8080`), and one with characters glued on (`<address>-1`, `<address>2026`) is now replaced by `[REDACTED]`. Nothing the old version hid is shown now (checked on 53,607 test texts and by reading the code). Logs written before are not rewritten.
**Still not blanked** (facts about the product; counts are from my test texts, 80 per kind):
- An address right after a web link that has no path, joined without a space: `https://x.example.com,alice@example.org` (every case kept; 798 in my texts).
- An address followed by a colon when a `/` comes later before any space: `alice@example.org:net/ipv4: fix …`, `<address>:2026-11-27/notes` (every case kept; 1,312), or by `:~`.
- An address glued straight onto a following link (`<address>https://…`), one cut by the 64 KiB reading window, one with an accented letter, a quoted name, or written in a disguised form (`alice at example dot com`), and the user name of a link with no password (`https://user@host/`).
**Summaries that become too long:** no user of the daemon can meet this (it sends no summary). A program that uses the audit library directly and sends a summary near the 4,096-byte limit that holds such addresses can now get an error for that one event, where the old version stored it; the event is not recorded until it is sent again. Nothing already stored is lost.
None of this can corrupt or break a log: it stays valid and verifiable.

## Findings
**Against the lane's work** (no Blocker, no Major):
- **L2-1 Minor: the user-info boundary is described narrower than it is in three documents and the commit message.** `docs/AUDIT.md:686`, `docs/M0-OUTCOMES.md:336-337`, `BACKLOG.md:1853` and the commit body l.5-6 say the user-info part runs "from the `://` to the first `/`, `?` or `#`"; the code (and the doc comment `redact.rs:721-723`) end it at the token's end when there is none, so `https://x.example.com,alice@example.org` keeps the address (798 of 798 such placements in my corpus).
  - Repro: probe `https://x.example.com,alice@example.org` at the head (`h/probe.sh xh txh dtab head`, row W-3) → kept whole.
  - Fix in words: add "or the token's end, so an address joined to a link with no path, as in `https://x.example.com,alice@example.org`, is kept" to each of those places.
- **L2-2 Minor: two branches that keep addresses have no test that goes red when they are reverted.** The `stop` closure's bytes other than whitespace (`redact.rs:798`: `"`, `'`, `<`, `>`, backtick) and its `c >= 0x80`: reduced to whitespace, every builder test still passes and `a@b.example:x"/y`, `a@b.example:xé/y` are kept. Two more branches that mask (the `~` clause `:861`, `c != b'-'` `:894`) are also unguarded (they mask more when removed).
  - Repro: `logs/revert_pstop.diff`, `revert_p80.diff`, `revert_pt.diff`, `revert_pdash.diff`; `cargo test -p coagent-audit --test ae2_email --test ae_email --test redaction --test gate --test gate_r2` → green.
  - Fix in words: add `a@b.example:x"/y` → `[REDACTED]:x"/y` and `a@b.example:xé/y` → `[REDACTED]:xé/y` to `ae2_addresses_before_a_colon_are_masked`, `a@b.example:~` to the kept list, and `a@b.xn--qae0-.9` → `[REDACTED]-.9` to the glued samples.
**Notes:**
- N2-1 (W-7): the five new rows' evidence names the sample, not the kind of failure; an over-mask of the same sample matches it (shown with p7).
- N2-2 (W-6): AE2-4 guards 6 visible bytes (`--QAE0`); AE2-5 guards one byte in the over-mask direction (the red variant masks the `-` too).
- N2-3 (W-8): a summary the base stored can be refused at the head (372 × `a@b.test:x`); the documents say only "near the limit".
- N2-4 (W-11): "a summary near the limit can be refused" is illustrated by 1,599 bytes, 39% of the limit (`docs/AUDIT.md:38-39`, `BACKLOG.md:371`).
- N2-5 (W-12): only the doc comment says a password holding `/`, `?` or `#` now hides the link's host.
- N2-6: `docs/M0-OUTCOMES.md:334-336` "each is now masked" and M0:341-343 / BACKLOG:1853 "what remains is …" are wider in isolation: true as qualified and as scoped to the first check's corpus; U1 and C3 also remain.
- N2-7 (W-9): squashed commits holding a non-reserved example name remain in the project's local object store (no ref); GitHub does not serve them.
- N2-8: the builder's Points 11 (a delete outside the project, unverifiable) and 12 (drafts edited before item 0; nothing built before the gates).
- N2-9 (W-10, older text, for a later lane): `BACKLOG.md:1855` "Why deferred" still names the old exclusions that :1853 narrows.
- N2-10 (W-13): the TLD list behind the `xn--qae0` check was unnamed; it is named in (k).
**Against the coordinator's rulings** (section (m); the lane built them as ruled and the doc comment states them): RM-1 Minor (ruling 1: path-less links), RM-2 Minor (ruling 2: a later `/` in the token, `~`), RM-3 Note (item 3: letter-label version pins over-masked), Notes on the over-masking of `host:port`, bare-file scp targets, `.GIT` and `repo.git)`, the hidden host of a password with `/`, and the stale `effective_join` comment.
**Open:** none outside this lane.

## What was NOT checked
| item | why |
|---|---|
| `scripts/check.sh` | brief: not run (the coordinator's merge check runs it) |
| the red runner at the base | not asked; base rows counted by program (178) |
| daemon `an_*`/`aw_*` at the base | the coordinator's ruling 2: head only |
| a real old-build daemon run | the coordinator's ruling 3: not required |
| the builder's own corpus (21,400) and its 54,017 / 15,483 total | not re-made; replaced by my three corpora |
| real-world frequency of each surviving class | my corpora are templates |
| reverts against every test target of the crate | run against the five redactor-asserting targets (`ae2_email`, `ae_email`, `redaction`, `gate`, `gate_r2`); other targets use `PatternRedactor` only as a default |
| IANA's live registry for `xn--qae0` | no network by rule; the local 2026-10-03 list only |
| Windows builds; main and the merge | not in scope |

## Files (`m1_review/gate_audit_email_2_tests/`)
- `r.sh`, `rr.sh` (wrappers doing the `cd`), `h/`: `mkcopy.sh`, `probe.sh`, `plants_e.sh`, `plant.py` (every source plant as one exact edit), `reverts.sh`, `mktime.sh`, `daemon.sh`, `qae2_probe.rs` (the first check's probe, emails columns on), `qae2_time.rs` ((g)), `qa2_corpus.py` (my generator, seed `0x2ae5eed2`), `qa2_lits.py` (literal corpus), `qa2_dtab.py` ((c)/(d) inputs), `qa2_diff.py` (model, oracle, b0, differential, survivors), `qa2_why.py` (survivor classes), `scope.py`, `protected.sh`, `qa2_sent.py`, `qa2_scan.py` + `run_scan.sh` + `scan_go.sh` (the words are not in the files), and the first check's `qa_corpus.py`, `qa_analyze.py`, `qa_bodies.py` as copied.
- `logs/`: builds, suites, probes, every differential and plant analysis, plant and revert diffs and logs, timing, scans (full output), `dtab.txt`, `sentences.txt`, `red_run.log`, `lane.diff`, `commit_msg.txt`; `red-logs/` (the runner's 185 row logs and the green log). The corpora and per-input dumps are not copied (they are re-made from the seeds).
- Work dir `/private/tmp/claude-501/qae2`. No process of mine is left (checked with `ps`). Nothing was written outside the work dir, this folder, the verdict and my STATUS file in the project.
