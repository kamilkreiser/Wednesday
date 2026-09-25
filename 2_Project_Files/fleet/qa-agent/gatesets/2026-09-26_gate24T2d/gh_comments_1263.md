--- comment 5837621582 by linear[bot] at 2026-09-25T18:37:43Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1140/ks879-guard-the-cell-walks-the-tree-on-its-own-offendersunderdev-root">KS-1140 ks879 guard: the 🔴 cell walks the tree on its own (`offendersUnder(DEV_ROOT)` :148) while the CONTROL and F1 vouch for `WALKED` (:136) — plus the docblock's four stale figures (GF-2/3/4, R1)</a></summary>
<p>

## BLUF

PR #978 (KS-885 + KS-886, merged 2026-09-13) widened `packages/shared/src/__tests__/ks879-no-raw-control-bytes-repo-wide.test.ts` to the whole Dev tree and asserted the escape itself. The tier-2 gate found one Minor against the PR — **GF-1: the array the 🔴 cell judges is not the array its controls vouch for** — and three Polish prose figures in the same file (GF-2, GF-3, GF-4) plus one Record (R1). One file, one test pass. The fix shape for GF-1 is the GATE'S PROPOSAL, carried here as a proposal — the builder's call.

Report: `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-13-ks885-886-978-13b767a7f-tier2-r1/report.md` — §6 GF-1..GF-4, Records R1. Line numbers at `13b767a7f` = develop after the squash (M14).

## Items (one test pass)

1. **GF-1 (Minor, MEASURED AT RUNTIME) — the 🔴 cell's walk is decoupled from the walk CONTROL and F1.** `:136` `const WALKED: readonly string[] = sourceFiles(DEV_ROOT);` is what the walk CONTROL (`:158-180`) and F1 (`:253-260`) pin; `:148` `const offenders = offendersUnder(DEV_ROOT);` calls `sourceFiles(root)` AGAIN at `:127` — a second walk, and that is the array the 🔴 cell actually judges. At base one array `files` (`:106`) served both. Repro from a pristine `13b767a7f` worktree: (1) `:148` → `offendersUnder(join(DEV_ROOT, 'packages'))`, nothing else; (2) `npx vitest run src/__tests__/ks879-…test.ts` → `8 passed (8)`; (3) plant `Blockchain/Dev/tests/__qa978_planted.spec.ts` = `const bad = 'doc` + byte 0x00 + `bad';` + LF; (4) run again → **still** `8 passed (8)` — the CONTROL counted 1,285 files and F1 found its three named files while the 🔴 cell judged `packages/` alone. Control: restore `:148` with the plant still on disk → `1 failed | 7 passed (8)`, the 🔴 cell names `tests/__qa978_planted.spec.ts: 0x00 at byte 16`. It is the KS-885 class exactly ("a control weakened while copying"). **Fix shape (PROPOSAL, verbatim from the gate):** *"let* `offendersUnder(root, files: readonly string[] = sourceFiles(root))` *take the list, and have the 🔴 cell call* `offendersUnder(DEV_ROOT, WALKED)` *— F2 keeps calling it with a scratch root only — so the CONTROL and F1 vouch for exactly the array the 🔴 cell judged, and the tree is walked once. Regression test (described): Tg2 above must red the walk CONTROL or the 🔴 cell; a control that pins* `offenders`*' input length equals* `WALKED.length` *would also do it."*
2. **GF-2 (Polish) —** `:161` **"(798 files)" is 791.** 791 tracked under the two roots at `0f69129b3` and at head (the builder's own red-first and the gate's T3 print `[ …(791) ]`); 798 = 791 + the seven scratch files the READY mail already corrected out of 1,291 → 1,284. No assertion uses it. (The PR body's two "798" were corrected to 791 before the squash; the file's `:161` was not — a comment edit.)
3. **GF-3 (Polish) —** `:43` **"1,284 files, 12,758,153 bytes read … at** `0f69129b3`**" is the head tree's figure**, not the base's: at `0f69129b3` proper the set is 12,751,993 bytes; 12,758,153 is with the modified ks879 (14,440 B) on disk. The floors do not depend on it. Say "at this commit" or restate.
4. **GF-4 (Polish) —** `:36-37` **cross-references the wrong sentence:** "749 of the 1,242 files the sentence above counts" — `:29` counts 1,240 (four EXTS, `14914258c`); 749 / 1,242 are `6fd033c36`'s five-EXTS figures. Say "749 of the 1,242 files tracked at `6fd033c36`".
5. **R1 (Record) — the docblock's 1,284 / 12,758,153 is stale on arrival:** the gate measured 1,288 / 12,823,398 on develop `e91eb5bda` + head; the tree it lands on (M14) carries #975/#976's edits too — restate on the next touch of the file or of `SKIP_DIRS`, or drop the exact figures (the floors are `> 1,000` / `> 5 MB`).

## Dedupe (searched before filing)

By symbol over 1,125 KS issues + 914 comments (includeArchived): `offendersUnder` → KS-886's READY comment only; `WALKED` → 0; `sourceFiles` → KS-924 only (`sourceFilesUnderRoots` in `entrypoint-corpus.test.ts`, another file — s206's PR-3); `ks879` → KS-885, KS-886; `12,758,153` → KS-886's comment. No home; filed new.
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1140-give-the-ks879-census-figures-their-commits-or-drop-them-gf-3-8517e8739555">Review in Linear</a></p>

