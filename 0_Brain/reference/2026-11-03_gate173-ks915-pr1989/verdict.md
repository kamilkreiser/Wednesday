NO GO (G173-F1)

# QA Gate 173 (Tier 1, round 1): PR 1989 / KS-915 `restore-local-secrets.sh` rebuilt to ask the real readers

## Subject
- **Start, ls-remote at 08:14:44Z:** `refs/pull/1989/head` = `refs/heads/fix/ks-915-restore-local-secrets-readers` = `ea41c34668ddc93f02a4dd997c365b9975a8adb3`. develop = `de8d208a8426747b3a752309e08167fa0de4b2ff`. Both match the READY. PR 1982 head `87c9e748…` is still open and was not touched.
- **End, ls-remote at 09:14:30Z:** the head is unchanged at `ea41c346…`. **develop moved** to `1cbf260548e7fd534603725f9fc6b05c5cdd9907`. It gained two commits (KS-1967, KS-1968), and neither touches a file the script reads. I diffed docker-compose.yml, docker-compose.local.yml, env.example, .env.local.example, bootstrap-env.sh, docker/pgbouncer, both .gitignores and start-secuura.sh: 0 changes (results/00_subject_end.txt).
- **Merge check:** `git merge-tree --write-tree` gives rc 0 both times. Against de8d208a the tree is `c93315c1e719`. Against the end develop 1cbf2605 it is `1ae2502f9c50`.
- **Diff:** three-dot against develop is 4 added files: the script (482 lines), its suite (571 lines) and two docs fragments. The merge-base is develop itself. The script's sha256 is `fb26f4c09833…`.
- **Host:** macOS (Darwin 27), `/bin/bash` 3.2.57 (the only bash on this host), Node 26.8.1 (**not** the LTS 24 line), dotenv 16.6.1 and pg-connection-string 2.12.0 (loaded read-only from the checkout's node_modules through a symlink in my clone), Docker Compose 5.5.0 (`config` only; no container was started).
- **NOT run on:** Linux/GNU userland, bash 4 or 5, Node 24, libpq/psql, pgbouncer itself, or a booted stack.

**Method.**
- I made `git clone --shared` into `repo/`. The PR ref and develop were fetched from GitHub into that clone. Nothing was written to the client checkout.
- Every run used a throwaway clone under `scratch/`, with the same file set the PR suite's `new_clone` uses. Each ran under `env -i` with HOME=`home/` and TMPDIR=`tmp/<tag>`. `home/.docker/cli-plugins/docker-compose` links to Docker.app's plugin, because without it the script fails closed. That was my first suite run, 82 FAIL, kept as `runs/suite_head_try1_nodockerplugin.bin`.
- Harnesses are in `harness/` and raw results in `results/`. They show only rc, tree hashes, modes, counts and labels.
- **The consumer instrument:** `harness/classify.js` reads dotenv 16.6.1; a bash `set -a; .` shell, with an independent `/usr/bin/env` read where the reader could be spoofed; and the REAL `docker compose config` through both entries. It prints REMOTE/PRODUCTION labels per service and never a value.
- **Counting rule (gate 166's):** a slip counts only when the script exits 0 and writes ADMIN, AND a real reader resolves a non-local host or `production` from the same files.

## Findings

### G173-F1 — HIGH — FIX-BEFORE-MERGE: `POSTGRES_HOST` (the pgbouncer upstream) is read by none of the four checks, so the script writes while compose sends the pooler to a remote database
- **FOUND:** In `Blockchain/Dev/docker-compose.yml` the pgbouncer service takes `POSTGRES_HOST: ${POSTGRES_HOST:-postgres}`, along with POSTGRES_PORT and POSTGRES_DB, from `.env`, the repo-root `.env` or the shell.
  - `docker/pgbouncer/entrypoint.sh:44-46` writes that host into the pool's `[databases]` upstream. Its own comment reads "Azure passes POSTGRES_HOST=<pg-fqdn>".
  - Every service's `DATABASE_URL` points at `@pgbouncer:6432`, which the script counts as local by design.
  - `judge()` looks only at NODE_ENV, PG*, and keys ending in `DATABASE_URL`. The canonical-line check looks only at lines naming DATABASE_URL, NODE_ENV, PGHOST or PGSERVICE. `grep -c POSTGRES_HOST` gives 0 in the script and 0 in the suite; the control `PGHOST` gives 12 in the script.
- **TESTED (results/q6.txt n01–n05):** 3 of 3 forms were ACCEPTED. Each gave rc 0, a generated ADMIN, `ALLOW_DEFAULT_SEED_PASSWORDS=true`, and mode 600, and the marker was printed 0 times. After each run:
  - n01, `POSTGRES_HOST=gate173rmt.host` in Blockchain/Dev/.env: compose resolves `POSTGRES_HOST=REMOTE` for the **pgbouncer** service through BOTH entries (dev and root). dotenv and bash `set -a` read it too.
  - n02, the same line in the **repo-root .env**: the root entry (`docker-compose.local.yml`, the one start-secuura.sh uses) resolves pgbouncer REMOTE.
  - n03, the same value exported in the shell: both entries resolve pgbouncer REMOTE.
  - **Render, results/q1_pgbouncer_render.txt.** I ran the entrypoint's own sed expression on the committed `pgbouncer.ini`:
    - n01 gives `secuura = host=gate173rmt.host port=5432 dbname=secuura`. The control gives the stock `host=postgres` line.
  - **Sibling form, n04:** `POSTGRES_DB="secuura host=gate173rmt.host"` is also ACCEPTED (rc 0, ADMIN written).
    - It renders `… dbname=secuura host=gate173rmt.host`.
    - Whether pgbouncer lets the later `host=` win was **not measured**.
    - compose's DATABASE_URLs keep host `pgbouncer` (pg reads the space as part of the database name), so no reader flags it.
  - **Controls in the same run:** `NODE_ENV=production` was refused (k92) and `NODE_ENV=development` accepted (k01). The `?host=` / `?hostaddr=` / `?service=` and `@remote` forms that compose interpolates into DATABASE_URL through POSTGRES_DB or APP_DB_PASSWORD (r07, r08, r09) were refused by the compose reader. That shows the compose instrument fires for the keys it judges.
- **Reach:** I did not start pgbouncer or connect to anything. "Reaches a remote database" stops at what compose passes and what the entrypoint renders.
- **HOW to fix:**
  - In `judge()`, refuse a non-local `POSTGRES_HOST` for any service, and judge the composed upstream (POSTGRES_HOST/PORT/DB) the way a DATABASE_URL is judged. Or, more generally, judge every resolved env key that ends in `_HOST` or `HOSTADDR`.
  - Add `POSTGRES_HOST` and `POSTGRES_DB` to the canonical-line keys.
  - Add n01–n04 as suite cells: dev .env, root .env, shell, and the POSTGRES_DB form.

### G173-F2 — MEDIUM: the bash reader takes its verdict from the shell that just ran the file, so a crafted line can forge the verdict
- **FOUND:** The reader sources `.env` and then calls `printf` to print the result. A function the file defined replaces the `printf` builtin. Separately, a file can print its own `@@RLS-KS915@@` record and `exit`. A single line beginning `X=1; …` is accepted by both dotenv and compose (the value is the rest of the line), and it does not name a key literally, so the canonical check skips it.
- **TESTED (results/q2345.txt sp0–sp3, results/q2b_followup.txt):**
  - **Control sp0:** `X=1; declare -x NODE_""ENV=production` is refused by bash `set -a`.
  - **sp1:** the same line plus a `printf()` override gives **rc 0 with ADMIN written**. An independent bash `set -a` plus `/usr/bin/env` then reads `NODE_ENV=production` (1 line).
  - **sp3:** the same with `DATABASE_""URL=…gate173rmt…` gives rc 0 with ADMIN written. `/usr/bin/env` reads a DATABASE_URL naming the remote marker (1 line).
  - **sp2:** the fake record plus `exit` is also accepted (rc 0). It is not counted as a slip, because `exit` also ends the consumer shell before it can read anything.
  - Gates 165/166 and the suite have no such cell. Mutant m16 (`indexOf` instead of `lastIndexOf`) survives the suite and accepts a fake-record-first form that the head refuses (results/q7b_survivors.txt).
- **Weight:** this needs a deliberately hostile `.env` author. Such a person can already run any builtin in every `set -a` user's shell. I count it as **2 class-bar slips by an adversarial file, 0 by an accidental one**, so it is not blocking on its own. Wednesday rules.
- **HOW to fix:**
  - Print through something the file cannot redefine: `set -o posix` (special builtins win over functions) with `export -p`, or `\builtin` after `unset -f printf builtin`.
  - Use a per-run random marker the file cannot know, and refuse when a second marker appears.

### G173-F3 — LOW: the "sandbox" can still write a file anywhere, and it has no time limit
- **TESTED (results/q6b_sandbox.txt).** I ran the script's reader command line verbatim (lines 262–268) on one-line files.
  - **`history -w <abs path>` writes the file despite `set -r`** on bash 3.2. This was 3 of 3:
    - x1: `history -s …; history -w /abs`
    - x2: `HISTFILE=/abs; history -w`
    - xb: content I chose (`NODE_ENV=production`) landed in the file
  - The same thing happened through the whole script: b05 and b06 changed TMPDIR during the script's own run (outside_same=N, before my consumers ran). b06 then went on to rc 0.
  - **Blocked, 6 of 6:** `command -p`, `hash -p`, `>`, `builtin printf >`, `exec`, `/usr/bin/touch`, `enable -f`.
  - **Control:** the same `command -p touch` line without the sandbox creates its file.
  - **Reading outside works:** x7, `read -r NODE_ENV < /abs/file`, reads `production`, and the script refuses it (b04).
  - **Hang:** b13, a `.env` containing `while :; do :; done`, kept the script running until my 60 s alarm (rc 142). Nothing was written. The looping reader (pid 79836) survived its parent until I killed it, and one sandbox directory (holding only a symlink) was left in TMPDIR.
- **Context:** develop already runs `.env` unrestricted in `scripts/check-slot-credentials.sh:156` (`set -a; . "$ENV_FILE"`), so executing the file is not a new capability. The finding is that the "no output redirection" sandbox claim in the comment at line 251 is broader than what bash 3.2 delivers.
- **HOW to fix:** `enable -n history` (and `kill`) before `set -r`, or `set +o history; readonly HISTFILE=/dev/null`. Add a reader timeout that fails closed.

### G173-F4 — LOW: when the repo-root `.env` names ADMIN_USER_PASSWORD, the root entry's auth does not get the value the script wrote
- **TESTED (results/q2345.txt ra1/ra2, q2b_followup.txt ra0).** The script decides blank-or-set and verifies the copy through the **Blockchain/Dev** entry only.
  - **ra1**, root `.env` with `ADMIN_USER_PASSWORD=`: rc 0, "generated". `docker-compose.local.yml` then gives auth a **blank** admin.
  - **ra2**, root `.env` with another value: auth gets that value, not the one written.
  - **Control ra0**, no root `.env`: the root entry's auth ADMIN equals dev `.env`'s.
- This errs in the safe direction (no unsafe write), but the "generated … in Blockchain/Dev/.env" message is wrong for start-secuura.sh users. Fix: also read `ADMIN`/`ALLOW` facts through the root entry, or warn when they differ.

### G173-F5 — MEDIUM (test strength): 22 of my 50 mutants survive the PR's suite; 5 of them are in the permissive direction and not equivalent
- **Raw table (results/q7_raw.txt), counted by me:** 28 KILLED, 22 SURVIVED, 0 not applied (results/mutants_applied.txt: 50 of 50 applied). Every mutant run's output contains 0 48-hex strings.
- The builder's figure of 25 mutants, 21 killed and 4 surviving refers to the builder's own set.
- **Non-equivalent, driven head against mutant (results/q7b_survivors.txt):**
  - **m06**, shell verdict ignored: shell `TEST_DATABASE_URL=postgres://u:p@gate173rmt.host/x`. Head rc 3, mutant **rc 0** writes. canonical_shell checks only 5 key names.
  - **m11**, hostaddr param, with `POSTGRES_DB=secuura?hostaddr=10.9.9.9`: head 3, mutant **0**.
  - **m12**, service param, with `POSTGRES_DB=secuura?service=…`: head 3, mutant **0**.
  - **m13**, "localhost" as a substring, with `POSTGRES_DB=secuura?host=localhost.gate173rmt.host`: head 3, mutant **0**.
  - **m16**, first marker: the F2 fake-record-first form gives head 3, mutant **0**.
  - **m36**, ALLOW re-check removed, with shell `ALLOW_DEFAULT_SEED_PASSWORDS=`: head rc 1 (correct), mutant rc 0 and says "set" while compose still passes blank. Safe direction, wrong message.
  - The suite has no cell that interpolates through `POSTGRES_DB`/`APP_DB_*`, which is why m11–m13 live. My r07–r09 show the head refusing that class.
- **Equivalent at the script level ("killed only by the layered run"), driven:** each refuses at both head and mutant through another reader.
  - m07 (NODE_ENV trim/lower), m08, m09 and m10 (judge PGHOSTADDR/PGSERVICE/PGHOST, form placed in .env.local), m14 (dotenv first file only), m27 (`$` allowed in RE_LINE), m28 (canonical NODE_ENV any case), m29 (canonical query check), m47 (no `LC_ALL=C`, NBSP under UTF-8).
  - That is 9 mutants. These are the "inside one reader" survivors the builder described.
- **Equivalent or unreachable by reading, not driven:**
  - m22 (compose rc ignored: an empty or garbage output still gives "no verdict"), m23 (no-services → OK: then no AUTH facts → die 1 before any seed write), m25 (MISSING unreachable after `check_tools`).
  - m30 (no CR split: a joined line naming a key is never canonical), m31 (NUL check: no reader reads production from a NUL form I could build; not driven).
  - m33 (no canonical re-check of the copy: the rewrite emits only canonical ADMIN/ALLOW lines), m35 (dotenv ADMIN re-check: correctness of systemTest's read only).
  - That is 7. Total: 6 + 9 + 7 = 22.

### HOLD-FOR-KAM condition (stated; Wednesday rules)
This script writes credentials and turns on the published demo accounts. Its whole safety claim is "never against production or a remote database".
- F1 is 3 accepted writes while compose sends the stack's pooler to a remote host, from forms that look like an ordinary Azure environment.
- F2 is 2 accepted writes against a deliberately hostile file.
- No value is printed or committed by any path I measured (Q3, below).

## What passed (measured)

**Q1, gate 166's 28 forms: 0 slips.** All 28 were refused at the head:
- 23 .env bodies × 2 placements × 2 locales (C and en_US.UTF-8) = 92 cells.
- Plus s01, s02, e01, e02 and e03 × 2 locales = 10.
- Each of the 102 cells gave rc 3, a byte-identical tree, mode 644 and the marker 0 times (results/q1_C.txt, q1_UTF8.txt).
- Gate 166's 9 non-slip bodies (c16, c17, c20–c23, c26–c28) were also refused: 36 cells.
- **Controls:**
  - k91 (canonical remote) and k92 (production) were refused, and the consumers read them REMOTE/PRODUCTION: 4 cells.
  - k01, k02, k03 and k05 (development, localhost:6432, socket, `@pgbouncer … # comment`) were accepted: 8 cells.
- **Which reader refused (C locale, 71 refusals):** dotenv 46, bash `set -a` 16, canonical-line 6, shell judge 3.
- **New forms beyond F1/F2 (results/q6.txt):**
  - PGHOST/PGHOSTADDR/PGSERVICE in .env, .env.local, root .env, shell, `export`, a multi-host value, `?service=` and `?options=`: 12 of 12 refused (p01–p10, p12, p13). `PGHOST=localhost` was accepted (p11).
  - Root `.env` and `.env.local` NODE_ENV/DB forms, plus POSTGRES_DB/APP_DB_PASSWORD interpolations into DATABASE_URL: 9 of 9 refused (r01–r09). r10 was accepted.
- **Temp-copy re-read:** a shell `ADMIN_USER_PASSWORD=` or `ALLOW…=` overriding the copy gives rc 1 with ".env was left as it was". The tree is unchanged and 0 temp copies remain (t01, t02).
- **`--rotate` with a multi-line quoted ADMIN** fails closed: compose refuses the file (t03, t04).

**Q2, a reader that cannot run: 16 of 16 fail closed with nothing written.**
- **rc 3 (14):**
  - no node; no node_modules; no docker
  - docker without the compose plugin
  - compose output that is garbage, `{}`, `[]`, an environment list, empty, or rc 2
  - a broken dev compose file; a broken root compose file
  - an unparseable `.env` (b09); a `.env` that exits (b10)
- **rc 1 (1):** an auth service without an environment. Bootstrap ran, but there was no seed write.
- **rc 3 (1):** a symlinked or hard-linked `.env`.
- Every message names the action. The `cannot` messages name `npm ci` or docker.
- **By design, accepted:** with the root `docker-compose.local.yml` absent, the script proceeds and says "repo-root entry (absent …)" (f07).

**Q3, no value printed: 0 hits.**
- 77 generated values were collected from 755 env files under `scratch/` and `runs/`. 3 crafted strings were set aside, by checking which values appear verbatim in the harness or the suite.
- I searched 342 files: every script and suite log, every mutant-suite output, `results/`, `harness/`, `tmp/` (bash-reader sandboxes and leftovers) and `home/`. **0 hits.** The planted control was found: 1.
- Every suite run (head, absent, PR 1982, and the 50 mutants, including m49, which prints the value) contains 0 48-hex strings. So gate 166 F7 is closed.
- Compose's resolved output only ever goes through a pipe into node and is never stored.

**Q4, idempotence (results/q2345.txt):**
- The second run is byte-identical for `.env` and `.env.local`, and the output says "kept".
- `--rotate` changes exactly 2 diff lines, both `ADMIN_USER_PASSWORD`. The file has 526 lines before and after. `.env.local` is unchanged and the mode is 600.
- The old value appears in **0** files across the clone (including `.git`), TMPDIR and HOME. Control: the saved pre-rotate copy contains it (1).
- The next run keeps the rotated value.

**Q5, ignore status:**
- `.env`, `.env.local` and `.env-ks915.*` are ignored. Controls: `.env.ks915.*` and `env.example` are NOT-IGNORED.
- After 4 runs, `git status -uall` lists 0 env files. Control: `env.example` is listed.
- **SIGKILL during the re-read** (a docker shim holds the `--env-file` call):
  - 1 copy is left behind. It is mode 600, ignored, listed 0 times in `git status`, and holds the new ADMIN.
  - `.env` is unchanged.
  - 0 sandbox directories are left. Every descendant pid was killed.

**The PR's suite:**
- **267 of 267** at head (147 s).
- **Red-first:** with the script absent, **238 of 267 FAIL**; with PR 1982's script (sha `8dff35f7f199`), **110 of 267 FAIL**. Both match the builder's figures.
- At PR 1982's script, all 28 of gate 166's forms appear among the failing G166 cells.

## NOT tested
- **pgbouncer itself:** whether it connects to the rendered upstream, and whether the later `host=` wins in the n04 form. No container was started, so "reaches a remote database" is not measured past compose and the entrypoint's sed.
- **libpq:** `PGSERVICEFILE` alone (p14 is accepted; libpq consults it only when a service is named, which was not measured) and libpq URL parsing.
- **Platforms:** bash 4/5 (where `history` with a slash and `HISTFILE` are restricted, so F3's write may not reproduce), Linux/GNU, Node 24, and a booted stack or a real seeded login.
- **Other compose invocations:** `--env-file`, `COMPOSE_FILE`/`COMPOSE_ENV_FILES` overrides, `docker-compose.dev-debug.override.yml` / `e2e.override.yml` / `production.yml` entries, and compose profiles.
- **Host-side readers** of POSTGRES_HOST, PGHOST or `.env.local` beyond what compose resolves.
- shellcheck, `run-shell-suites.sh`, the docs-fragments check, and the PR body. The builder's claims were taken from the commission's summary; the PR API was not read.
- SIGINT and SIGHUP on a foreground run.

## Plain answer for Kam
The rebuilt script is much stronger than PR 1982:
- Every one of the 28 tricks that got past the last version is now caught, in both locales.
- It never shows a password.
- A second run changes nothing, and `--rotate` changes only the one password.
- When a tool it needs is missing, it stops safely and says what to do.

But it still misses one setting that matters. The database pooler (pgbouncer) gets the address of the real database from a setting called `POSTGRES_HOST`, and that is exactly how the Azure setup points it at the cloud database. If a developer's settings file, or the one at the top of the repo, carries a cloud address there, the script goes ahead and switches on the local test accounts while the stack would send its database traffic to that remote server. That needs one more check, and a test, before it can merge.

Two smaller points can be fixed at the same time:
1. A deliberately hostile settings file can fool one of the checks.
2. The check's "sandbox" can still write a file on older macOS bash.
