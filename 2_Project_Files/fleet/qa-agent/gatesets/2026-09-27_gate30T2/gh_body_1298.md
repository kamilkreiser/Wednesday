#1298 KS-1347: take the ks732 spec and handler paths with fileURLToPath, not pathname
head aefa0ef5c46e0d5519c454d5e5506ad54fcda894

## BLUF
The ks732 MFA-disable proof read three files through `new URL(..., import.meta.url).pathname`, which **percent-encodes**. On a checkout whose path contains a space those reads resolved to names that do not exist and the proof failed for a reason nothing in the output explained. All three now use `fileURLToPath`. **Test files only — no auth product code changes.**

Refs KS-1347

## What changed
Two files, +88/−3, both under `services/auth/src/__tests__/`.
- `ks732-mfa-disable-proof.test.ts` (+4/−3) — the `fileURLToPath` import and the three path expressions.
- `ks1347-ks732-spec-paths-survive-a-spaced-checkout.test.ts` (+84, new) — plants files under a **spaced** checkout root and asserts every path resolves to the real file, with a no-spaces control and a shape control over ks732's own source.

**Site 1 of 2.** The proxy `server.ts` site is untouched, so the ticket stays open.

## Provenance — and the ONE token that is not the model's
The diff block is **`cmp` rc 0 against BOTH the brief's golden and the run's canonical patch** — 5,407 B, sha256 `ce9ab6c59386b515…` (control: `cmp` against an unrelated golden → rc 1). Strict `git apply --check -p1` per section at `3f70224a069b`, no `--recount`, no fuzz; **both tamper controls fire** (`pathname`→`pathnameZZ` rc 1; new-file hunk count `+1,84`→`+1,999` rc 128).

**One token was changed on review, and here is the whole delta:**
```diff
-const PATH_LINES = KS732_LINES.filter((line, i) => i > 0 && ...).map((line) => line.trim());
+const PATH_LINES = KS732_LINES.filter((_line, i) => i > 0 && ...).map((line) => line.trim());
```
The `.filter` callback declares `line` and uses only `i`. As written, the golden **adds a `TS6133: 'line' is declared but its value is never read`** under a test-inclusive compile. The rename to `_line` satisfies `noUnusedParameters`. **The product lines in ks732 are byte-identical to the model's output**; this single token is the only departure, and it is in the new test file.

## Test Evidence
Author-run, locally, at head `aefa0ef5c46e0d5519c454d5e5506ad54fcda894` (base `3f70224a069b`). **`services/auth` runs vitest, not jest.**

- **RED (new cell alone, the ks732 edit reverted — revert confirmed by blob id):** `Tests: 1 failed | 2 passed (3)` — `RED KS-1347 A2: from a checkout path WITH spaces every path is the real planted file, not a percent-encoded one`. The **no-spaces control (A1) stayed green**, so the cell discriminates the defect rather than failing everywhere; A0 pins the shape of ks732's own source. No startup error, 3 ran.
- **GREEN (both files):** `Tests: 16 passed (16)` after a sha256-verified restore.
- **auth suite (`vitest run`):** **bare 832 passed**, **patched 835 passed**, 0 new reds; the +3 is this cell.
- **`tsc --noEmit` over a program PROVEN to contain both touched files** (`exclude: []`, **719 files**, each once by `--listFilesOnly`): **37 errors at my head and 37 at the tip.** All 8 differing rows are `ks732-mfa-disable-proof.test.ts` errors whose **line numbers MOVED** because this patch adds one import (`(293,37)→(294,51)`, `(296,35)→(297,49)`, `(316,37)→(317,51)`, `(318,11)→(319,11)`); **0 differing rows are anything else, and 0 errors name the new cell.** Those 37 are pre-existing (`TS1343` `import.meta` under this module setting, plus unused-symbol rows in other test files) and are not touched here.
- **`npx tsc --noEmit` with the package's real config** (which **excludes `src/__tests__`**): **rc 0, 0 errors.**
- **`npm run lint` (`eslint src`):** **rc 0, 15 problems (0 errors, 15 warnings) at BOTH trees**, identical. Control: a planted `debugger` in the new cell gives `no-debugger` and rc 1.
- **Push gate — only what THIS push printed:** `pre_push_hook_base.test.sh` **28/0** · `pre_push_hook_base_fixture_guard.test.sh` **6/0** · `run_shell_suites.test.sh` **49/0** · shell suites **60 of 60** · `OK — 13 code guards passed` · zero `FIXTURE BUILD FAILED`.
- **Preflight:** `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.`

**NOT run / NOT covered:**
- **The 37 pre-existing test-file type errors are not fixed here** — including `TS1343` on `import.meta` in ks732 itself. This PR neither adds to them nor reduces them.
- The proxy `server.ts` site is untouched.
- No local stack (legs 3, 4, 8), no live sweep, no deploy, no integration/e2e.
- The fix is proven by a cell that plants files under a spaced root; it is **not** proven by running the real ks732 proof from a genuinely spaced checkout.

## Review notes
- Base `develop` `3f70224a069b`, fast-forward. No merge-in.
- Foreign keys un-hyphenated in title, body and commit message (`ks732`). The `ks732` strings in the touched files are file content and path names.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

