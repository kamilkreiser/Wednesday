#1302 KS-1348: give originate's production File transports a JSON format so the logs hold text
head 99374a3dbef16de9ae4a3a1759cf64e81a8b136f

## What this changes

Under `NODE_ENV=production`, `utils/logger.ts` adds two File transports — `logs/error.log` and
`logs/combined.log` — and gave them **no format**. The logger-level format carries no `json()` and no
`printf()`, so nothing rendered the entry and **every line written to either file was the literal text
`undefined`**. Both transports now carry their own `combine(json())`, as the Console transport already did.

Only production builds these transports, which is why no existing cell could see it. `Refs KS-1348`.

Two files, **+96 / -2**: the product change is **+4 / -2** in `services/originate/src/utils/logger.ts`
(`:47`, `:48`); the rest is a new cell.

## ⚠ BEHAVIOUR CHANGE, stated rather than buried

**The production log files will now really hold logged error text.** The `fail500` family logs
`err.message` server-side, so that text now reaches `logs/error.log` and `logs/combined.log` **on disk**
instead of being discarded as `undefined`. That is the point of the fix — a log line reading `undefined`
has no diagnostic value — but it does change what those files contain in production, and it is worth a
reviewer's attention rather than a footnote.

## How the cell proves it

It loads the **real** module under production through `jest.isolateModules` (the module reads `NODE_ENV`
once, at import), with the working directory moved to a fresh temp dir so the relative `logs/` paths land
there, logs one error, and **reads back what winston actually wrote**. Three controls ship with it:
exactly one line was written to each file — so the red assertion reads a real write, not an empty file —
and the module loaded its production shape (one `Console` plus the two `File` transports).

## Provenance — the GOLDEN is canonical here, not the model's own block

The two differ by **one trailing context line**, and that line is exactly what made the model's hunk
header miscount: it declared `old=6 new=8` against an actual 7 and 9 (the checker recorded the same, and
its own apply needed `--recount --ignore-whitespace`). Their added/removed line sequences are
**identical, 98 each** — measured. The **golden applies strictly with no accommodation** (`git apply
--check -p1`, rc 0), paired with a hunk-count tamper (`+N,999`) git refused (rc 128), so that rc 0 is not
a check that could not fail. A path tamper would have been inert here, because a new file applies at any
path — that is why the count is tampered instead.

**Independent identity check:** after applying the golden, `services/originate/src/utils/logger.ts` and
the new test file are **byte-identical (`cmp` rc 0) to the golden's own expected copies**
(`logger.fixed.ts`, `ks1348-…test.ts`), with a control proving `cmp` discriminates. The READY made no
identity claim; this is one.

Produced by the local model (Spark) under a Wednesday brief, **re-verified by this seat**. Wednesday's
harness figures are hers; every number below is from my own runs.

## Test Evidence

**Touched:** `services/originate/src/utils/logger.ts`, `services/originate/src/__tests__/ks1348-production-file-log-lines-are-json.test.ts` (new)

**Ran** — worktree detached at develop `94c9c7aa9be7`; `npm ci` 1936 packages; `packages/shared` BUILT.

| check | result |
|---|---|
| **RED** — new test present, **product hunk reverted** (confirmed by numstat, and `format: combine(json())` occurrences back to **0**) | **2 failed / 3 passed / 5 total**, rc 1, **0 loadfail markers**; both failures on assertions |
| **GREEN** — product hunk applied | **5 passed / 5**, rc 0 |
| originate suite **BARE** (untouched tip: product reverted **and** the new untracked test moved aside, porcelain 0) | 84 suites, **979 passed / 979** |
| originate suite **PATCHED** | 85 suites, **984 passed / 984** |
| **NEW reds** | **none** — both failing sets empty |
| `tsc` — widened program **proven to contain** the new test (1 hit) and `logger.ts` (1 hit); control **0** hits in the package program | **0 errors** |
| `tsc` **positive control** — unused const appended | **1 error, 1 × TS6133** → that program really type-checks the new file |
| `eslint src` at **HEAD** / at **TIP** | rc 0 both, **0 errors** both |
| lint **control** — planted `debugger;` | rc **1**, `no-debugger` → lint runs and can fail |
| every restore after a control | **sha256 identical** |

**Gate lines THIS push printed** (`s-b33-ks1348-99374a3dbef1-push.out`, per suite block by exact
basename): `pre_push_hook_base.test.sh` **28/0** · `..._fixture_guard.test.sh` **6/0** ·
`run_shell_suites.test.sh` **49/0** · shell suites **60 passed, 0 failed, 0 skipped (of 60)** ·
`^FIXTURE BUILD FAILED` **0** · `OK — 13 code guards passed.` ·
`PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` Push rc 0; 0 orphaned `login_stub` pids.

**Migrations + config:** none. No migration, no `package.json`, no lockfile; the widened tsconfig was
temporary and removed before staging. Exactly **2 files staged**, checked against a forbidden-path guard.

**NOT run / NOT covered:**
- **Nothing deployed.** The cell exercises winston's real file writing in a temp dir; it does **not**
  exercise a deployed production container, log rotation, `maxsize`/`maxFiles` behaviour, or disk
  permissions in any real environment.
- No assertion about log VOLUME or retention: if error text is now persisted where `undefined` used to be,
  the files will grow differently. Not measured, and worth a reviewer's judgement.
- The integration suite was not run (needs a live stack); preflight legs 3, 4 and 8 do not run without one.
- Only the two File transports are covered. The Console transport and the non-production paths are unchanged
  and untested here.

Refs KS-1348

