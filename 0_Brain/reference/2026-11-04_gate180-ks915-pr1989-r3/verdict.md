GO WITH NOTES — HOLD-FOR-KAM (signature class: a secrets-writing script that switches on the published demo accounts, as gate 174 stated; plus G180-F1: one crafted two-line .env that round 2 refused is accepted at head)

# QA Gate 180 (Tier 1, round 3 of 3 by Kam's 09:33:42 ruling): PR 1989 / KS-915 `restore-local-secrets.sh`, G174-F1 + G174-F2 only

**Merge tree for the merge seat:** `git merge-tree --write-tree a01e579ca47be1ca60828537316823051730edf6 df71e6b7c6258c6b01202d8fabedcdeafc445c95` → rc 0, tree **`26e4302bf61e4aae27df6d1380542b8af0df8e4c`**.

## Subject
- **Start, ls-remote 2026-11-04T01:32:20Z** (checkout's `ls-remote origin`): `refs/pull/1989/head` = `df71e6b7c6258c6b01202d8fabedcdeafc445c95`; develop = `a01e579ca47be1ca60828537316823051730edf6`. Both equal the commission.
- **End, ls-remote 2026-11-04T01:45:16Z:** head **unchanged** `df71e6b7c625…`, develop **unchanged** `a01e579ca47b…`.
- History (my clone): `c71a6d106` (round 2) → `84e706ae8` (merge of develop ee1e1b832) → `df71e6b7c` (fix). Three-dot vs develop = the same 4 files (+1464). Round-3 delta `84e706ae8..df71e6b7c`: script +69/-27 (judge(), bash record 8→13 values with guard i+16, `readonly PATH` + stderr `grep -c ': PATH: '` refusal, canonical-line list, canonical_value, canonical_shell), suite +158, two fragments. Script sha256 `2f1c8b3f3343…` (round 2 `f4a44ee7faa8…` = gate 174's).
- **Host:** macOS Darwin 27 arm64, `/bin/bash` 3.2.57 (the only bash on the harness PATH, checked), Node v26.8.1 (not LTS), dotenv 16.6.1 / pg-connection-string via the gate-173 WEDNESDAY-side node_modules link (read-only), Docker Compose v5.5.0 (`config` only), throwaway `redis:7-alpine` containers `--rm --network none` for busybox sed (render only). **NOT run on:** bash 4/5, Linux/GNU, Node 24, the edoburu/pgbouncer image or pgbouncer itself, a booted stack.

**Method.** `git clone --shared` into `repo/` (GitHub added as a second remote IN MY CLONE only, PR ref + develop fetched there); the checkout got read verbs only. Gate 174's harness copied and re-keyed (marker `gate180rmt`): each cell is a throwaway clone under `scratch/` with the PR suite's file set, run under `env -i`, HOME=`home/`, TMPDIR=`tmp/<tag>`, recording rc, tree hash before/after, mode, temp copies, marker count in the log, then the same files read by independent consumers (dotenv, plain unsandboxed `bash set -a`, real `docker compose config` through both entries) printing labels only. Every form was run at head and (for F1, F2-residual) with the round-2 script (`SCRIPT_SRC=round2`) as the red control. The render oracle cuts `entrypoint.sh` lines 42-56 from the head blob and runs them under busybox sed on a copy of the committed `pgbouncer.ini`, with exactly the values compose passes. No value was printed; 0 of 137 tracked workdir files contain a 48-hex string (control: the ignored golden `.env` has 8).

## Findings

### G180-F1 — LOW: the stderr-closing residual the seat disclosed is real and measured — one crafted two-line `.env` refused at round 2 is accepted at head while a plain `set -a` reads a remote POSTGRES_HOST (no command executes)
- **FOUND:** ruling (B) depends on the reader's stderr reaching `grep -c ': PATH: '`. `exec 2<&-` (an input-dup close, which `set -r` does not stop on bash 3.2) on an earlier line shuts stderr, so the readonly-PATH error is never counted, and bash still skips the rest of the PATH line. Written so dotenv and compose parse every line: `GATE_A=1; exec 2<&-` / `GATE_B=1; PATH=/usr/bin:/bin; declare -x POSTGRES_""HOST=<remote>`.
- **TESTED (results/q2b_f2_residual.txt, q2b_f2_residual_round2.txt, q2c_f2_r3_nocons.txt):**
  - r1 at **head: rc 0, ADMIN written, mode 600**; independent reads: dotenv local, compose dev/root all-local, **plain `set -a`: POSTGRES_HOST=REMOTE**. At **round 2: rc 3**, refused by bash set -a naming POSTGRES_HOST (there the PATH assignment succeeded and the line ran in full). So head is more permissive than round 2 on this one cell.
  - r2 (`exec 2<&1`, stderr into stdout): head rc 3, "bash set -a gave no reading" (fails closed).
  - r3 (same residual, with `touch <abs>` after the PATH assignment): head rc 0, **artifact absent after the script**; control, a plain `set -a` on the same file afterwards, CREATED. The PATH lock holds; only the read diverges.
  - r0 (the same-line form without the `exec` line): head rc 3, PATH named (control for r1).
- **Weight:** needs a hand-crafted hostile `.env` (two shell-syntax lines, a quote-split key name); the remote host reaches only a plain `set -a` shell, not compose, so pgbouncer's rendered upstream stays local (compose all-local in r1). Same class as G173-F2 (a hostile `.env` steering the bash reader, named out of scope), and the seat disclosed it in its READY's RESIDUAL paragraph. Round 2 let the same author run any external command from inside the reader (G174-F2); head trades that for this under-read. Not FIX-BEFORE-MERGE in my judgement; a ticket next to G173-F2. Fix direction only: a sentinel the reader must print to stderr after `. e` (its absence = refusal), or check `[[ -w /dev/fd/2 ]]`-style liveness in the -c string after the source.
- **Instrument error, mine, corrected:** my first r3 run said CREATED; that file came from my own unsandboxed consumer (`consumers_full`), not the script. Re-run with consumers off: absent (q2c).

### G180-F2 — INFO (test strength): the surviving mutant `e33_canon_value_pool_any` is NOT equivalent — two forms kill it — but neither is a safety gap
- **FOUND:** the mutant (pool arm of `canonical_value` → `return 0`, E 33rd's `mutants_e33.py:53`, applied by me, 1 replacement) survives the suite: **421 passed, 0 failed** (runs/suite/mutant_pool_any.out; = the seat's 0/421). Driven (results/q3_mutant_head.txt vs q3_mutant_mut.txt, 6 forms):
  - u2 `PGBOUNCER_MAX_CLIENT_CONN=abc` then `=10`: **head rc 3 (canonical-line check, sole refuser) / mutant rc 0**. Every reader takes the LAST line: dotenv, bash, compose dev, compose root all read digits.
  - u4 the `=abc` line hidden inside a double-quoted multi-line value of another key: **head rc 3 / mutant rc 0**. dotenv and bash read the key unset; compose reads its default (digits).
  - u1 `=1x`, u3 `=10` then `=abc`, u5 shell `=abc`: head 3 / mutant 3 (dotenv or the shell judge refuses first); u6 `=10`: 0 / 0 (control).
- **Classification:** killable, so not equivalent; the READY's "by reading, every value the canonical line admits that is not digits is refused earlier by dotenv, bash or compose" is wrong for u2/u4. But the mutant's extra acceptances are only lines no reader the script consults (and no compose service) actually uses, so no non-numeric value reaches pgbouncer: **reachable, not permissive in effect**. Severity INFO; one suite cell (u2) would kill it. A tool that takes the FIRST occurrence of a key (e.g. `grep -m1`) was not looked for (NOT tested).

## What passed (measured)

**Q1, G174-F1: closed.** results/q1_f1_head.txt vs q1_f1_round2.txt, 25 cells each.
- Gate 174's g01-g04 verbatim (+ g05, the fifth key `_MAX_USER_CONNECTIONS`): **5/5 refused at head** (rc 3, tree identical, mode 644, marker 0, the key named; g04 names the shell environment); **5/5 accepted at round 2** (rc 0).
- New forms, 11: v01 double-quoted `\n` (dotenv makes a real LF), v02 shell value with real LFs, v03 CR-joined (sole refuser: compose), v04 `+100`, v05 `-1`, v06 full-width digits, v07 `0x10`, v08 `${GATE_X}` with a LF-bearing shell GATE_X, v09 `export … '10|marker'`, v10 a slip in the repo-root `.env` over a plain dev value, v11 duplicate key: **11/11 refused at head, 11/11 accepted at round 2.** (16 F1 forms, 16 red at round 2, 16 green at head.)
- Line-break rule: l01 shell NODE_ENV with LF, l02 shell DATABASE_URL with trailing LF, l03 `.env` NODE_ENV="development\nstaging": **3/3 refused at head, each named "carries a line break" (l01/l02) or by dotenv (l03)**. NOT red-first: round 2 refuses all 3 too (canonical-line check). l04 a LF in an unjudged shell key: accepted at both (control; matches Wednesday's scope ruling).
- Benign: b01 five plain integers in `.env`, b02 the same in the shell, b03 two blanks (compose's `:-` defaults apply), b04 a value with a trailing `# comment` plus a repo-root integer, b05 NODE_ENV=development: **5/5 accepted at head** (rc 0, mode 600, ADMIN set).
- **Render oracle (results/q1_render_oracle.txt): confirmed.** g01, g02, g04, g05 (dev entry) and g03 (root entry) each render **2 `[databases]` headers**, the second followed by `secuura = host=gate180rmt.host …`; g03 through the dev entry, b01 (five integers) and the stock golden clone render **1** header and only `host=postgres`. v03's CR form renders one line containing raw CRs (whether pgbouncer splits on CR: not measured; refused at head anyway).

**Q2, G174-F2: holds for every form the commission names.** results/q2_f2_head.txt.
- 16 PATH escape forms through the whole script (e01 = gate 174's e1; export, declare, prefix assignment, `read <<<`, `printf -v`, eval, a function `local`, `declare +r`, subshell, EXIT trap, `for PATH in`, `+=`, `unset PATH`, `{ …; } 2<&-`, `exec 2<&-; PATH=…` on one line): **16/16 rc 3, artifact absent 16/16, `.env` byte-identical**; unsandboxed control CREATED **15/16** (e14 `unset PATH` cannot run touch unsandboxed either: no control, as expected). e16 is refused by compose (unparsable line), not by the PATH count.
- Same-line forms: s1 `PATH=/usr/bin:/bin; POSTGRES_HOST=<remote>`, s2 `PATH=…; declare -x POSTGRES_""HOST=<remote>`, s3 the `PATH+=:/x` variant: **3/3 REFUSED by the PATH count** ("a line … changes or names PATH"), not under-read; independent plain `set -a` reads POSTGRES_HOST=REMOTE on each (control). z1, z2, z4 (stderr redirected on the same line): 3/3 refused (count or no-reading); z3 refused by compose.
- Benign: b1 `ENV=`, `SHELL=`, `NODE_ENV=development`, `MY_PATH=`; b2 `PYTHONPATH`, `MANPATH`, `PATH_PREFIX`, `NPM_PATH`; b3 a `# PATH=…` comment: **3/3 accepted**.
- Exception: G180-F1 (an EARLIER line closes stderr).

**Q3, the survivor:** G180-F2 — killable (2 forms), not a safety gap.

**Q4, no regression.**
- PR suite at head: **Results: 421 passed, 0 failed**; with the round-2 script under the head suite: **368 passed, 53 failed** (= the READY). The 53 are all round-3 cells (G174 F1 7, F1-nl 4, F2 21, compose 4, layer 2, pin 5, the G166-harness q01-q07/f17/pt forms 9, one `(v)` shell cell). 0 48-hex strings in either output.
- G173-F1 (results/q4_regression_head.txt): n01-n04 **4/4 refused**, h10 and p02 refused, n05 `POSTGRES_PORT=5432` accepted (control).
- Credential-through-DATABASE_URL condition: w01-w05 (APP_DB_PASSWORD hostaddr and host, POSTGRES_PASSWORD via repo-root `.env`, shell APP_DB_USER, POSTGRES_USER `?host=`) **5/5 refused, each by `docker compose config`** naming the composed URL and service; c01 plain password accepted (control).

## NOT tested
- pgbouncer itself (whether it obeys a re-opened `[databases]` section or a CR in the ini); the edoburu image; a booted stack; a real seeded login.
- bash 4/5 (whether `exec 2<&-` / the readonly abort behave the same), Linux/GNU, Node 24, shellcheck.
- `run-shell-suites.sh`, the format-gate candidate cell, docs-fragments check, the pre-push hook, the PR body: taken from the READY, not re-run.
- The seat's other 97 mutants (only the named survivor was re-run); gate 174's G166 69+69 locale forms and Q5/Q7 surfaces were not re-run beyond the PR suite's own cells.
- Tools outside the script's reader set that take the FIRST occurrence of a key (G180-F2's harmlessness assumes none consume the pool keys).
- Out of scope by ruling, not graded: G174-F3/F4/F5, G173-F2, the looping `.env`, entrypoint.sh:26-30 userlist echo.
- Environment: Docker Desktop's socket was gone at my end check (`docker ps` could not connect at 01:45Z); every render ran before that and used `--rm`. I did not stop Docker.

## Plain answer for Kam
The last gate found that five connection-limit settings could smuggle a second, remote database line into the pooler's configuration; the script now refuses any of them that is not a plain number, and it refused all 16 ways I tried, while ordinary numbers still work. It also refuses any checked setting that hides a line break. The script's sandbox can no longer run outside programs through a changed PATH; all 16 ways I tried were blocked. One leftover, which the developer had already disclosed: a deliberately hostile settings file can blind the new PATH check so the script reads one value differently from a plain shell. That only affects people who load the file by hand, not the database pooler, and it needs a hand-written attack. One of the developer's test mutations was described as harmless for the wrong reason; it is harmless, but only one extra test would prove it. I see nothing that blocks the merge, but this script still writes passwords and switches on the demo accounts, so Wednesday should rule on the hold.
