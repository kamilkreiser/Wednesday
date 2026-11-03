NO GO — HOLD-FOR-KAM (not mergeable at 411f8e1e; back to Seat E for round 2: F1, F2, F4 FIX-BEFORE-MERGE)

# QA Gate 165 (Tier 1, round 1): PR 1982 / KS-915 `restore-local-secrets.sh`

- Subject: head `411f8e1ea760dfc01048cd0d11519b8271b2a2aa`. ls-remote at gate start gave refs/pull/1982/head = refs/heads/fix/ks-915-restore-local-secrets = 411f8e1e. That matches the READY mail and the brief.
- develop by ls-remote: `32921f7921c2cdeb87e4361a2976a9e8cfd6beac`, 5 commits past the PR's base 2a827aac.
- `git merge-tree --write-tree develop pr` gives rc 0 and tree `8a689938c476`, with no conflicts.
- Script sha256 at head: `25de2fd6ebe7…`, which matches the author's figure.
- Method: I ran everything in throwaway trees under `scratch/` and `mut/`, with `env -i`, HOME=`home/` and TMPDIR=`tmp/`. Nothing ran in the shared checkout. The harness is in `harness/` and raw results are in `results/`.
- No secret value is printed anywhere. Comparisons are done in-process, and the results show only counts, truncated hashes, modes and key names.

## Findings

### G165-F1 — HIGH — FIX-BEFORE-MERGE: the refusal reads a different .env line than the real consumers read
- **FOUND:** `read_key` matches only the line `^KEY=` and keeps the FIRST match. dotenv, docker compose and `set -a; .` accept other line shapes, and they keep the LAST occurrence. So a hosted `DATABASE_URL`, or `NODE_ENV=production`, can be written in a shape the script does not see. In that case the script exits 0 and writes `ADMIN_USER_PASSWORD` and `ALLOW_DEFAULT_SEED_PASSWORDS=true`.
- **TESTED:** I started from a completed .env with `ADMIN_USER_PASSWORD` blank and mode 0644. The script ACCEPTED all of these (rc 0, admin written, mode changed to 600):
  - DATABASE_URL: `export DATABASE_URL=…remote`, `  DATABASE_URL=…remote` (leading whitespace), `DATABASE_URL = …remote`, `DATABASE_URL: …remote`, and a local line followed by a remote line (results/q1.txt 206–210).
  - NODE_ENV: `NODE_ENV=production # live`, `export NODE_ENV=production`, `NODE_ENV= production`, `development` followed by `production`, and `  NODE_ENV=production` (results/q1b.txt 308–312).
  - The same ten shapes went through the real parsers (results/q1c.txt). **dotenv 16.6.1** (the version host scripts import) resolves 10/10 to the remote host or to production. **docker compose v5.5.0 `config`** also resolves 10/10. **bash `set -a; .`** resolves 7/10.
- **HOW to fix:** refuse fail-closed when the key appears more than once, or in any non-canonical shape. The shapes to catch are `^\s*(export\s+)?KEY\s*[=:]` other than exactly `^KEY=`. Also strip a ` #` inline comment and leading whitespace before comparing. Add one cell per shape above.

### G165-F2 — HIGH — FIX-BEFORE-MERGE: a percent-encoded `host` query key gets past the check
- **FOUND:** the loop over query parameters compares the RAW key against `host` and `hostaddr`.
- **TESTED:** `postgres://u:p@localhost/x?h%6Fst=<remote>` is accepted, both in the shell and in .env (rc 0; q1 #37, #212). **pg-connection-string 2.12.0** (pg 8.20.0) parses it to `host="<remote>"` (q1c).
- **HOW to fix:** percent-decode the key before comparing it, or refuse any `%` in a query key. Add a cell for it.

### G165-F3 — MEDIUM: multi-host and junk-after-bracket authorities are accepted
- **TESTED:** these are accepted (rc 0; q1 #34–36, #211):
  - `postgres://u:p@localhost:5432,<remote>:5432/x`
  - `postgres://u:p@[::1],<remote>/x`
  - `postgres://u:p@[::1]<remote>.com/x`
- The host is cut at the first `:` or at `]`. Node's pg throws `ERR_INVALID_URL` on all three, so Node consumers are safe. libpq takes a comma-separated host list and would fall back to the remote host. libpq was **not measured**, because psql is not installed.
- **HOW to fix:** refuse an authority that contains `,`, and refuse anything after `]` other than `:port`.

### G165-F4 — MEDIUM — FIX-BEFORE-MERGE: the temp file holding a full copy of .env is not gitignored
- **FOUND:** `mktemp "$ENV_FILE.ks915.XXXXXX"` creates `Blockchain/Dev/.env.ks915.*`. `git check-ignore -v --no-index` reports it **NOT-IGNORED** at PR head. The controls behave as expected: `.env` is ignored by `Blockchain/Dev/.gitignore:23` and `.env.local` by `:19`.
- **TESTED** with a slow-awk shim that holds `set_key` open (q4b):
  - SIGTERM and SIGHUP: the EXIT trap removes the temp file. Nothing is left.
  - **SIGKILL: the temp file is left behind.** It is 29,960 bytes, mode 0600, and holds the same POSTGRES_PASSWORD as .env. `git status --porcelain` lists it, so a later `git add -A` would commit every local secret.
  - A crash, power loss or OOM kill has the same effect as SIGKILL.
- **HOW to fix:** create the temp file under an ignored name, for example `"$DEV_DIR/.env-ks915.XXXXXX"` (root `.gitignore` ignores `.env-*`). Confirm with check-ignore, and add a cell for it.

### G165-F5 — LOW: an existing ADMIN value in a non-canonical shape is replaced without --rotate
- **TESTED:** `export ADMIN_USER_PASSWORD=x` and `ADMIN_USER_PASSWORD = x` are read as blank. The script then appends a new generated line (q234 x5 and x6: 2 lines, "generated"). Last-wins parsers then use the new value, so the existing value is effectively replaced without `--rotate`.
- Same root cause as F1. The canonical shapes all behave correctly: plain, quoted, single-quoted, CRLF, and duplicates, which are kept.

### G165-F6 — LOW: `ALLOW_DEFAULT_SEED_PASSWORDS=TRUE` is reported as "kept (already true)", but the seeder skips it
- The script lower-cases the value before comparing. `userRepo.ts:1332` compares `!== 'true'` exactly. So a developer is told "already true" and the seeder still skips (q234 x7).
- **HOW to fix:** compare exactly, or warn when the value differs only in case.

### G165-F7 — LOW / NOTE (Q6): the generated value works with the seeder, but fails the platform's own strength rule
- **What works:**
  - The value is 48 lowercase-hex characters (`openssl rand -hex 24`, CSPRNG), which is under bcrypt's 72-byte limit.
  - The seeder applies no policy: `requiredSeedPw` only needs a non-empty value, and `hashPassword` checks nothing.
  - Login is `z.string().min(1)`.
  - The seeder rewrites an existing row's hash at boot (`updateUser`), so `--rotate` followed by recreating auth also works.
  - **So the script is useful today.**
- **The caveat:** I ran the real `checkPasswordStrength` and `minLengthForRole`, extracted from `services/auth/src/services/password.ts` at develop, over 26 generated values. All 26 come out `isStrong=false`, both at the default length and at SYSTEM_ADMIN's 14. They have only 2 character classes, and the rule needs 3.
  - Controls: `Str0ngP@ssw0rd!` gives true; `a1`×24 gives false.
  - If anyone later applies the platform's own policy to seeded admins, every generated value would be rejected.
  - Suggest generating mixed-class output, for example base64url with a guaranteed upper-case letter, digit and symbol.

### G165-F8 — LOW: the allow-list misses compose's `pgbouncer` service
- The legacy `.env.example` ships `DATABASE_URL=…@pgbouncer:6432/…`. A .env made from that template is refused as "not a local host" (q1 #39). This errs in the safe direction, but it blocks older clones.

### G165-F9 — LOW: a symlinked .env makes `chmod 600` change a file outside Blockchain/Dev
- `chmod` follows the symlink, so the target outside Blockchain/Dev changed mode 644 → 600 (q234 m4). Only the mode changes, not the content.

### G165-F10 — LOW / NOTE: a hostile `BASH_ENV` makes the child bootstrap-env.sh trace its own generated values
- `BASH_ENV=<file with set -x>` on a fresh clone: 6 of 6 bootstrap keys appear in the output. The script's own ADMIN value does not appear.
- `bash -x` and `SHELLOPTS=xtrace`: 0 leaks.
- The cause is behaviour bootstrap-env.sh already has. The script passes the environment through unchanged.
- **HOW to fix:** invoke bootstrap with `env -u BASH_ENV -u SHELLOPTS bash …`.

### G165-F11 — MEDIUM (test strength): 14 of 26 gate mutants survive the PR's suite
- **Survivors that make the guard MORE permissive (the dangerous direction):**
  - mA: `*localhost*` treated as local
  - mC: `hostaddr` check dropped
  - mE: a schemeless value treated as local
  - mF and mG: NODE_ENV compared without lower-casing, which lets `PRODUCTION` through
  - mH: quote stripping dropped, which lets `"production"` through
  - mJ: the unclosed-`[` check dropped
  - mU: first match changed to last match (this direction is the F1 fix)
- **Survivors that only refuse more:** mD, mP, mQ, mS, mT and mV.
- **Killed:** mB, mI, mK, mL, mM, mN, mO (refusal moved after bootstrap), mR, mW, mX, mY (`set -x`) and mZ (echo of the value).
- The suite pins only one remote host shape and one `?host=` shape. The author's figure of "10 of 10 killed" is true of the author's own set.
- **HOW to fix:** add cells for uppercase and quoted NODE_ENV, hostaddr, a host that contains "localhost", a schemeless value, an unclosed bracket, and the F1, F2 and F4 shapes.

### G165-F12 — NOTE: writes outside Blockchain/Dev, and a design residual
- In a repo that has `.githooks/`, bootstrap-env.sh writes `core.hooksPath` into `.git/config` (q234 m5). This is existing behaviour, and bootstrap-env.sh is unchanged by design.
- No other path outside Blockchain/Dev changed. I hashed HOME, TMPDIR and the repo-root files: all unchanged.
- **Design residual (approved design, not tested):** a compose-hosted shared box, such as the VM demo, has local-looking hosts. The DATABASE_URL predicate cannot tell it apart from a laptop; only `NODE_ENV=production` there would cause a refusal.

## What passed (measured)

### Q1 refusals
- **Shell forms:** I constructed 39. The 33 that should be refused were refused with rc 3, both on a fresh clone and with a .env already present at 0644. Each time the tree hash was unchanged, HOME/TMPDIR were unchanged, no .env was created, the mode was not changed, `DATABASE_URL` was named, and the host marker appeared 0 times in the output. The shapes covered:
  - other hostnames, IPv4, `127.0.0.2`, `0.0.0.0`
  - host:port, user@host, `?sslmode&connect_timeout`
  - IPv6 and IPv4-mapped IPv6
  - `postgres.<x>.com`, `localhost.<x>.com`, `postgres-<x>`
  - uppercase hosts, an uppercase whole URL
  - schemeless and libpq keyword strings
  - double- and single-quoted values, leading and trailing spaces, embedded spaces
  - `p@ss@host`, `localhost@remote`
  - `?host=`, `?HOST=`, `?hostaddr=`, `&host=`, `postgres:///x?host=`, duplicate `host=`
  - `localhost%2E…`, `localhost.`, unclosed `[`
- **The slips:** 4 of the 6 accepted forms are real slips (F2, F3). The other 2 are `pgbouncer`, which was refused (F8), and `host%3D`, which pg resolves to localhost, so it is benign.
- **Local controls:** 7 of 7 accepted: localhost, LOCALHOST, 127.0.0.1, [::1], postgres, a socket directory, and empty.
- **.env, canonical shapes:** 5 of 5 refused, each with the file byte-identical and mode still 644. The shapes: plain, double-quoted, single-quoted, inline comment, CRLF.
- **Shell and .env disagreeing:** refused in both directions. A shell value of `""` does not hide a remote value in .env.
- **NODE_ENV=production:** refused when set in the shell, both with no .env and with one present, and for `PRODUCTION`. Also refused in .env as plain, quoted and `Production`. `development` and `demo` were accepted.

### Q2 no value printed
- I searched for 22 strings (every non-template value of 8+ characters in .env, .env.local and the pre-rotate .env, plus each one's 16-character prefix).
- They covered nine runs: fresh, second idempotent, `--rotate`, after rotate, `--help`, unknown flag, DATABASE_URL refusal, NODE_ENV refusal, and `--rotate --help`.
- **Hits: 0.** Control: one value planted into a copy of the output was found (1).
- xtrace lines: 0. `bash -x` and `SHELLOPTS=xtrace` runs: 0 leaks.
- Static reading: `set +x` comes at line 41, before any value exists. The value reaches awk through `ENVIRON`, not argv. No message, including error messages, interpolates a value. Output is limited to names, paths, lengths and generated/kept.

### Q3 idempotence and --rotate
- Second run: .env and .env.local sha256 identical, ADMIN hash the same.
- `--rotate`: the ADMIN hash changed, and the diff is exactly 2 lines, both ADMIN_USER_PASSWORD. The file has 526 lines before and after, .env.local is unchanged, and the next run keeps the rotated value.
- An existing plain, quoted, single-quoted or CRLF value, and an explicit `false`, are all kept byte-identical.
- With no trailing newline, the other lines stay identical.

### Q4 modes and gitignore
- Fresh run: 600/600.
- A complete .env and .env.local, both at 0644: both end at 600, and the content is unchanged.
- An incomplete .env at 0644: ends at 600.
- A refused run leaves a 0644 file alone, which is correct.
- `.env` and `.env.local` are gitignored. The temp file is not (F4).

### Q5 untouched files, the PR's own suite, docs check
- The PR touches 4 added files only. `bootstrap-env.sh`, `env.example`, `.env.example`, `docker-compose.yml` and `userRepo.ts` are byte-identical between develop tip and the PR.
- The PR's suite at head: **70/70**. Red-first with the script absent: **49 of 70 FAIL, 0 FATAL**. Both match the author's figures.
- `docs-fragments.mjs check` ends with `OK`.

## NOT tested
- shellcheck (not installed on this host; the repo has no shellcheck leg).
- `run-shell-suites.sh` (the author's 114/0/1 figure, not re-measured).
- libpq/psql handling of multi-host URLs (F3).
- A booted stack: no compose up, no seeded row, no real login with a generated value. Q6 is based on reading the code plus running the real policy function, not on a live login.
- The GNU `stat` branch and Linux.
- SIGINT on a foreground run.
- The VM demo's real `.env` (it was out of bounds, so I did not read it).
- Node 24 (this host has Node 26.8.1).
- Prisma's URL parser.

## Plain answer for Kam
The script does its main job well:
- It makes a strong new local admin password on the developer's own machine.
- It never shows that password on screen. I checked every run and planted a copy as a control.
- A second run doesn't change anything, and `--rotate` changes only the one password.
- It locks the files down so only the owner can read them.

It also refuses to run when the database address is obviously somewhere else, and there are dozens of ways of writing that address that it correctly catches.

But I found a few ways to slip past that check, so it should go back for one more round before it merges:
1. **Rewording the settings file.** The tools that actually read the file also accept the same setting with "export" in front, with extra spaces, or written twice. The script only looks at one plain spelling. So a file pointing at a remote database, or marked as production, can get past the check while the real tools still read the remote or production value.
2. **A disguised address.** One partly scrambled way of writing the database address also gets through.
3. **A leftover copy if it crashes.** If the script is killed hard at exactly the wrong moment, it leaves a full copy of the secrets file that git would happily commit.

All three are small, well-understood fixes, plus a few more tests to lock them in.
