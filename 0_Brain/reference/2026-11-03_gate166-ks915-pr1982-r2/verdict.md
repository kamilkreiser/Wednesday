NO GO (G166-F1, G166-F2, G166-F3, G166-F4, G166-F5)

# QA Gate 166 (Tier 1, round 2): PR 1982 / KS-915 `restore-local-secrets.sh`

This is round 2 of 2, so the cap applies. A NO GO means nothing merges and Wednesday cards it to Kam. Each blocking form below is exact, and the cells that reproduce it are named.

## Subject
- **Start, ls-remote at 03:08:37Z:** `refs/pull/1982/head` = `refs/heads/fix/ks-915-restore-local-secrets` = `87c9e7488fd7ef407bd80b06dba2374d969ee019`. develop = `27fe5476526c4200b752449e04be689724289e6d`. Both match the brief.
- **End, ls-remote at 03:36:37Z:** identical. The head did not move.
- **PR API (read-only GET):** head `87c9e748…`, open, not merged, base develop.
- **Body:** the body sha256 (no trailing newline) is `7c6677c7345d…`, which equals the author's patch receipt.
- **Merge check:** `git merge-tree --write-tree develop pr` (in my clone) gives rc 0 and tree `5bf7752fdf95`.
- **Diff:** three-dot vs develop is 4 files, all added. Between 411f8e1e and the head, only the script and its test changed.
- **Script sha256 at head:** `8dff35f7f199…`.
- **Host:**
  - macOS (Darwin 27), `/bin/bash` 3.2.57 (the only bash on this host)
  - Node 26.8.1. This is **not** the LTS line 24.
  - dotenv 16.6.1 and pg-connection-string 2.12.0, loaded read-only from the checkout's node_modules
  - Docker Compose v5.5.0 (`config` only)
- **NOT run on:** Linux/GNU, bash 5, Node 24, libpq/psql, Prisma.

**Method.**
- **Where and how:** I made a `git clone --shared` into `repo/` and fetched the PR ref from GitHub there. Every run happened in a throwaway clone under `scratch/` or `mut/`, with `env -i`, HOME and TMPDIR inside the workdir. Nothing was written to the client checkout.
- **Round-1 harness:** copied into `harness/` with its paths changed and re-run unchanged against the head (results/q1, q1b, q234, q4b). There are three edits:
  - I added `postgres:///x` to the controls.
  - The temp-file glob is now `.env-ks915.*`.
  - The check-ignore list includes both names.
- **New harnesses:**
  - D3 spellings: `d3_cases.sh`, `d3_script.sh` (each case appended to and prepended to a completed .env with a blank ADMIN, in the C locale and in en_US.UTF-8), and `d3e.sh`.
  - What the real consumers read: `d3_consumers.sh` and `d3_full.sh`. These cover dotenv 16.6.1, bash `set -a; .`, a compose probe file, and the REAL `Blockchain/Dev/docker-compose.yml` resolved by `docker compose config`, with pg-connection-string resolving the host.
  - Mutants: `mutants_r2.py`, run by `q5r2_suite_mutants.sh`.
  - `leak_sweep.py`.
- **Counting rule:** a slip is counted only when the script exits 0 and writes ADMIN AND at least one real consumer resolves a non-local host or `production` from the same file.

## Findings

### G166-F1 — HIGH — FIX-BEFORE-MERGE: a value that refers to another variable, or has a `${…:-default}`, is read literally by the script but interpolated by compose and bash
- **FOUND:** the script compares the raw text. `docker compose` and bash `set -a; .` expand `$VAR`, `${VAR}`, `${VAR:-x}` and `${VAR-x}`, taking values from earlier .env lines or from the shell.
- **Slips:** 9 forms. In each the script exits 0, writes ADMIN and `ALLOW_DEFAULT_SEED_PASSWORDS=true`, and sets the mode to 600. This holds in both locales and in both placements.
  - **NODE_ENV:** the REAL docker-compose.yml gives **api-gateway `NODE_ENV=production`** (its line `NODE_ENV=${NODE_ENV:-development}`), and bash `set -a` reads production too.
    - `NODE_ENV=${GATE_UNSET:-production}` (one line, c03)
    - `NODE_ENV="${GATE_UNSET:-production}"` (c18)
    - `NODE_ENV=${GATE_UNSET-production}` (c19)
    - `GATE_ENVX=production` followed by `NODE_ENV=${GATE_ENVX}` (c04), and the `$GATE_ENVX` form (c05)
    - shell `GATE_SHELLX=production` with .env `NODE_ENV=${GATE_SHELLX}` (s01)
  - **DATABASE_URL:** bash `set -a` and the compose probe resolve a pg host of `gate166rmt.host`.
    - `GATE_Q=?host=gate166rmt.host` followed by `DATABASE_URL=postgres://u:p@localhost/x${GATE_Q}` (c06), and the `$GATE_Q` form (c07)
    - the same with the variable set in the shell (s02)
- **TESTED:** results/d3_script_C.txt, d3_script_UTF8.txt and d3_full.txt.
  - Controls in the same run: a canonical `NODE_ENV=production` and a remote URL are read as production/REMOTE by every consumer (k91, k92). `NODE_ENV=development` is read as development (k93).
  - Reach: for DATABASE_URL, the real compose file never passes .env's value into any container, because each service hard-codes `@postgres` or `@pgbouncer`. So the DB form reaches host-side `set -a` users only. I did not measure which scripts those are.
- **HOW to fix:** fail closed on any `$` in a DATABASE_URL or NODE_ENV value, read from the shell or from .env. Add one cell per form above.

### G166-F2 — HIGH — FIX-BEFORE-MERGE: a `host` query key with a TAB, CR or LF inside it (or the escape that becomes one) gets past the F2 rule
- **FOUND:** the query loop compares the raw key. pg-connection-string parses with the WHATWG URL parser, which deletes ASCII TAB, LF and CR, so `ho<TAB>st` becomes `host`. dotenv turns `\n` and `\r` inside double quotes into real control characters. compose also turns `\t` into one.
- **Slips:** 7 of 7 forms accepted (rc 0, ADMIN written). For each, pg resolves `host="gate166rmt.host"`.
  - **Shell:** `DATABASE_URL=$'postgres://u:p@localhost/x?ho\tst=gate166rmt.host'` (e01). Also `?host\t=` (e02) and `?ho\rst=` (e03).
  - **.env:**
    - `DATABASE_URL="postgres://u:p@localhost/x?ho\nst=gate166rmt.host"` (a literal backslash-n; dotenv and compose read REMOTE; e11)
    - `"…?ho\tst=…"` (compose reads REMOTE; e12)
    - an unquoted literal TAB (dotenv and compose read REMOTE; e13)
    - `"…?ho\rst=…"` (dotenv and compose read REMOTE; e14)
- **TESTED:** results/d3e.txt. Control in the same run: `?host=` in .env is refused (rc 3), and all three consumers read it as REMOTE (e19).
- **HOW to fix:** refuse any whitespace or control character, and any backslash, anywhere in the URL. Or decode the URL the way WHATWG does before comparing.

### G166-F3 — MEDIUM — FIX-BEFORE-MERGE: a bare CR inside a line (a classic-Mac line break) hides a second key line from the script
- **FOUND:** dotenv turns every `\r\n?` into `\n`. The script's `read` splits on LF only and strips just a trailing CR. A key that comes after an embedded CR is therefore invisible to the script.
- **Slips:** 4 forms accepted, rc 0 with ADMIN written, in both locales and both placements:
  - `DATABASE_URL=postgres://u:p@localhost/x\rDATABASE_URL=postgres://u:p@gate166rmt.host/x` (c08: dotenv reads REMOTE)
  - `A=1\rDATABASE_URL=postgres://u:p@gate166rmt.host/x\r` (c10: dotenv reads REMOTE)
  - `NODE_ENV=development\rNODE_ENV=production` (c09: dotenv reads production)
  - `NODE_ENV="development"\rNODE_ENV=production` (c25: dotenv AND the REAL compose api-gateway read production)
- **TESTED:** results/d3_full.txt.
  - Ordinary CRLF is handled: c22 and c23 are refused.
  - `\v` and `\f` are not slips, because no consumer reads production or remote from them (c27, c28).
- **HOW to fix:** split on CR as well as LF, or refuse any CR that is not at the end of a line.

### G166-F4 — MEDIUM — FIX-BEFORE-MERGE: a UTF-8 BOM before the first key hides that line from the script
- **FOUND:** JavaScript `\s` includes U+FEFF, so dotenv reads `<BOM>DATABASE_URL=` as DATABASE_URL. compose strips a leading BOM. The script's grep needs `^[[:space:]]*`, and a BOM is not `[[:space:]]` in either locale.
- **Slips:**
  - BOM as the first line of .env (c01, c02):
    - `<BOM>DATABASE_URL=postgres://u:p@gate166rmt.host/x`: dotenv and compose read REMOTE.
    - `<BOM>NODE_ENV=production`: dotenv and the REAL compose api-gateway read production.
  - A BOM in the middle of the file, after a local line (c24): dotenv reads REMOTE. compose refuses that file outright.
- **TESTED:** results/d3_script_*.txt and d3_full.txt. Windows editors save a BOM by default.
- **HOW to fix:** strip a leading U+FEFF before matching, and refuse a U+FEFF anywhere else.

### G166-F5 — MEDIUM — FIX-BEFORE-MERGE (C/POSIX locale only): a no-break space (U+00A0) used as whitespace hides the key or the value
- **FOUND:** dotenv (JavaScript `\s`, `.trim()`) and compose treat U+00A0 as whitespace. The script's `[[:space:]]` matches it under en_US.UTF-8 but not under C/POSIX.
- **Slips:** under `env -i` (no LANG), all 5 forms are accepted with rc 0 and ADMIN written. Under `LANG=LC_ALL=en_US.UTF-8` all 5 are refused.
  - `<NBSP>NODE_ENV=production`, `NODE_ENV<NBSP>=production`, `NODE_ENV=<NBSP>production` and `NODE_ENV=production<NBSP>` (c11–c14): dotenv and the REAL compose api-gateway read production.
  - `<NBSP>DATABASE_URL=…gate166rmt…` (c15): dotenv and compose read REMOTE.
- **TESTED:** results/d3_script_C.txt against d3_script_UTF8.txt. Peter's locale is unknown. A text copied from a web page commonly carries NBSP.
- **HOW to fix:** pin a UTF-8 match, or refuse any non-ASCII byte on a line that names the key.

**One fix for F3, F4 and F5:** refuse fail-closed when any line *contains* the text `DATABASE_URL` or `NODE_ENV` and is not exactly canonical and local. That is a substring test, not an anchored grep.

### G166-F6 — MEDIUM (test strength): 11 of 38 mutants survive the PR's suite, and one of them is in the dangerous direction
- **Raw table** (results/q5r2.txt), counted by me: 27 killed, 11 SURVIVED, 0 did not apply.
- **The author's figure** of 22/22 refers to the author's own set.
- **Dangerous direction, non-equivalent:**
  - `r2_cand_no_anyhash` (the "cut at any `#`" reading is dropped).
  - Driven (results/d4_survivor.txt): the mutant ACCEPTS `NODE_ENV=production#x` (rc 0, ADMIN written), and dotenv reads `production`. The head refuses it (rc 3). The suite has no cell for this form.
- **Non-equivalent, not dangerous to the refusal:**
  - `g165_mH2_no_dquote_effective`: `ADMIN_USER_PASSWORD=""` would be "kept" while blank, and `ALLOW="true"` would be misreported.
  - `r2_admin_set_first_only`
  - `r2_seed_first_wins`
  - `r2_trap_removed`: the SIGTERM cleanup is unpinned; only SIGKILL has a cell.
  - `r2_setkey_canonical_only`: `--rotate` would leave the old non-canonical line in the file.
  - `r2_eff_no_inline_comment`: changes the ALLOW/ADMIN reading.
  - `r2_empty_url_refused`: refuses more; there is no empty-URL control in the suite.
- **Equivalent or probably equivalent (by reading, not proven):**
  - `r2_no_comma_check`: RE_PLAIN and RE_BRACKET already reject every comma shape I could build.
  - `r2_no_cr_strip`: the later trims include `\r`.
  - `g165_mH_no_quote_strip_candidates`
- **Gate 165's surviving classes, re-expressed on the new code:** mA, mC, mE, mF, mJ and both mU are now killed (7). mH survives (probably equivalent) and mH2 survives (non-equivalent, above).

### G166-F7 — LOW, PRE-EXISTING (same line at 411f8e1e): the PR's own suite prints a generated value when a refusal cell fails
- **FOUND:** `restore_local_secrets.test.sh:191` passes `"$(val_of "$CE" ADMIN_USER_PASSWORD)"` as `got` to `expect`. On failure, `expect` prints `got "<value>"` (line 47). This contradicts the header's "no value is ever printed here".
- **TESTED:** under mutant `r2_no_file_db`, the suite output carried one 48-character hex ADMIN value. The value was generated inside the suite's own scratch, which is removed at exit, so it is a throwaway and not a credential of any system. I moved that log to an ignored `.bin` name.
- **HOW to fix:** compare inside the process with `yn [[ -z … ]]`, as the other cells do.

### G166-F8 — LOW: a hard-linked .env makes `chmod 600` change a file outside Blockchain/Dev
- This is the sibling of round-1 F9, which is now closed for symlinks.
- A complete .env hard-linked to `outside_hard.env` gives rc 0, and the outside link's mode goes 644 → 600 (d3e). Only the mode changes, not the content.

### G166-F9 — LOW: ADMIN set and then blank is reported as "kept", while every consumer reads blank
- The form is `ADMIN_USER_PASSWORD=x` followed by `ADMIN_USER_PASSWORD=`. The result is rc 0, the file unchanged, and "kept ADMIN_USER_PASSWORD". dotenv reads it blank, so the seeder creates no admin (d3e).
- The error is in the safe direction: nothing is written. But the message is wrong. The cause is that `admin_set` is any-line while the consumers are last-wins.

### HOLD-FOR-KAM condition (stated; Wednesday rules)
This is a credential-handling script for a client developer.
- **Blocking findings:** F1–F5 are writes that happen while a consumer reads production or remote. None prints or commits a value. Generated-value searches give 0 of 22 with a planted control of 1, and the trackable-file sweep gives 0 real hits (below).
- **The one printed-value finding:** F7. It is the test suite printing a throwaway value it generated itself, and only on a failing cell.

## What passed (measured)

**Expected by ruling:**
- Round-1 control 7, `postgres:///x?host=/tmp`, is now REFUSED: rc 3, tree unchanged, no .env (q1 #106; d3 k04 in .env).
- `postgres:///x` is ACCEPTED: rc 0 (q1 #108; d3 k03).

**D1, the gate-165 items at head:**
- **F1:** 10 of 10 round-1 forms refused, each with rc 3, the tree byte-identical, mode 644 and the marker never printed: q1 206–210 (.env DB shapes) and q1b 308–312 (NODE_ENV shapes). Related forms also refused in both locales (7): `export<TAB>`, quoted `#`, CRLF and a tab-value (c16, c17, c20–c23, c26).
- **F2:** 3 of 3 refused: `h%6Fst` fresh and present (q1 #37), and in .env (#212). `host%3D` is also refused (#38).
- **F3:** 7 of 7 refused (q1 #34–36 ×2, #211).
- **F4:** closed.
  - The temp file is `.env-ks915.*`, ignored by `.gitignore:16:.env-*`.
  - SIGKILL leftover: 29,964 bytes, mode 600, ignored. `git status` lists 0. Its name is printed 0 times; my first counter's 1 was the workdir path, which contains "ks915".
  - Control: the round-1 name `.env.ks915.Ab12Cd` is NOT-IGNORED.
  - SIGTERM leaves nothing behind.
- **F5:** 2 of 2. `export ADMIN…` and `ADMIN = …` are both kept, file unchanged, 1 line (q234 x5, x6).
- **F6:** 1 of 1. `TRUE` is rewritten and the output says "rewrote … compares exactly 'true'" (q234 x7).
- **F9:** 2 of 2. A symlinked .env (q234 m4) and a symlinked .env.local (d3e f9l) are each refused with rc 3, the .env unchanged at 644, and the target's content and mode unchanged.
- **F11:** see G166-F6. 7 of the 9 re-expressed gate-165 mutants are now killed.

**D2, held, none regressed:**
- Shell refusals: 39 of 39 forms ×2 variants (fresh and present) refused, 78 cells. Each had rc 3, the tree the same, HOME/TMPDIR the same, the variable named, and the marker 0 times.
- Local controls: 7 accepted (101–105, 107, 108).
- .env: canonical 5 of 5 refused. Shell and .env disagreeing: 3 of 3 refused.
- NODE_ENV: 12 of 12 refused; development and demo accepted.
- **Q2, no value printed:**
  - 0 of 22 values found, with the planted control found (1).
  - xtrace lines: 0. Under `bash -x` and `SHELLOPTS=xtrace`: 0 leaks.
- **Q3:** the second run is byte-identical. `--rotate` changes exactly 2 diff lines (ADMIN only), 526 lines before and after. The next run keeps the rotated value. The canonical value shapes (plain, quoted, single-quoted, CRLF, duplicates) are kept. With no trailing newline, the other lines are identical.
- **Q4:**
  - Modes come out 600/600. A refused run leaves a 0644 file alone.
  - Nothing outside Blockchain/Dev changes except bootstrap's existing `core.hooksPath` write (F12).
- **The PR's suite:** 137 of 137 at head.
  - With the script absent: 97 of 137 FAIL, 0 FATAL.
  - With the 411f8e1e script: 41 FAIL. The author reports 40 of 67 new cells; I counted whole-suite FAIL lines and did not map them to the new cells.

**.env.local vs .env:** in the real compose file, 4 of 34 services load `.env.local`: api-gateway, auth, kyc and m365-integration. A `.env.local` carrying `DATABASE_URL=…remote` and `NODE_ENV=production` reaches **0 of those 4**, because their `environment:` entries override it. Control: a planted key reached 4 of 4 (results/d3_envlocal.txt).

**D6:** the PR body states F7, F8, F10 and F12 as known limits. F10 is unchanged: under `BASH_ENV`, 6 of 6 bootstrap keys are traced, the same as round 1, and the script's own ADMIN value is not traced. The `core.hooksPath` half of F12 is not mentioned in the body. That is minor, and not worse.

**Leak sweep of every file git would track in this workdir:**
- 284 distinct generated values were read from 367 env files.
- After my two moves to `.bin`, there are 0 real hits. The 10 remaining hits are my own crafted test strings (`production` and similar).
- Planted control: 1.

## NOT tested
- Which host scripts actually consume `.env`'s DATABASE_URL through dotenv or `set -a`. This is "host scripts" as round 1 described them; I did not re-measure it.
- libpq/psql and Prisma URL parsing. The tab and LF stripping in F2 was shown for pg-connection-string only.
- bash 5, Linux/GNU userland, Node 24, and a booted stack or a real seeded login.
- SIGHUP. The cell ran under `nohup`, which ignores SIGHUP, so its rc 0 is not a measurement. SIGTERM proves the trap.
- `run-shell-suites.sh` and shellcheck.
- `docker-compose.local.yml` at the repo root, and `--env-file` or `COMPOSE_ENV_FILES` overrides.
- Host-side readers of `.env.local`. Only compose containers were measured.

## Plain answer for Kam
All the specific holes found last round are closed:
- reworded settings lines
- the disguised database address
- the crash leftover that git could commit
- the symlink trick
- the upper-case "TRUE"

Everything that worked before still works. It never shows a password, a second run changes nothing, and the files are locked to the owner.

But there are still other ways to write the settings file that the real tools read as "production" or "a remote database" while the script reads them as safe:
- a setting that points at another setting (for example "use production if nothing else is set")
- a hidden tab or line break inside the address
- old-Mac line endings
- the invisible marker that Windows editors put at the start of a file
- a no-break space on some machines

In each of those cases the script would still go ahead and switch on the local test accounts. These are all one family of problem, with one straightforward fix: refuse anything that is not written in the plain, simple form. Because this is the second and final round, it should not merge as it stands, and the decision on next steps is yours.
