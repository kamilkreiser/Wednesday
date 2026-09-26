# KS-1341: Spark brief set (routes/webhooks.ts, 7 unconditional err.message 500s)

Written 2026-09-26 15:03:39 AEST (shell `date`) by a brief-writer sub-agent for Wednesday. It ran no model, queued nothing, and wrote nothing in any project folder. Every repo read used a read-only git verb at origin develop `e080174c86c671349c508560744644fc0ef33388` (re-read 15:03:13 AEST).

## BLUF

The ticket has **8 edit points** in total: 7 one-line site replacements plus 1 helper insertion. That is over the 3-per-brief limit, so the work is **SPLIT INTO THREE briefs, run strictly A → B → C**. Each brief changes ONE product file (`webhooks.ts`) and adds ONE new test file.

| file | brief | sites (develop line) | edit points | new test file (lines) | closes |
|---|---|---|---|---|---|
| `brief.md` | **A** (queue first) | helper insertion after `:548`, plus `:200` GET / and `:267` POST / | 3 | `ks1341a-…test.ts` (173) | 2 of 7 |
| `brief-B.md` | **B** (after A merged) | `:325` PATCH /:id, `:337` DELETE /:id, `:352` rotate-secret | 3 | `ks1341b-…test.ts` (197) | 3 of 7 |
| `brief-C.md` | **C** (after A and B merged) | `:391` POST /:id/test, `:416` GET /:id/deliveries, plus a whole-file SOURCE cell | 2 | `ks1341c-…test.ts` (166) | KS-1341 |

**Why the helper goes at the END of the file.** `fail500` is a hoisted function declaration, and the file already calls `deliverWebhook` at `:378`, above its declaration at `:427`. Putting the helper at the end means no line before `:549` moves. B and C therefore quote the same develop line numbers, and those numbers still hold after A merges. B and C each carry a two-command "Before queueing" re-check against the new develop sha.

## Spark predicate: PASS for all three (reasoning)

- **One product file.** Only `webhooks.ts`, plus one new test file per brief.
- **Fix spelled out.** Every `+` line is given byte for byte, with the hunk headers. The helper is copied from `gdpr.ts:210-213` (KS-730, merged today as #1283).
- **Test to copy.** The harness comes from `ks1160-webhooks-post-persists-normalised-url.test.ts:7-60` and the cell shape from `ks730c…:58-127`. The red cells use a LEAK string that does NOT contain `does not exist` and carries no SQLSTATE. Each red cell asserts that the body never contains LEAK, that the logger received it under the route's context, and that the catch was REACHED. A positive control is included.
- **This file's own traps.** GET / and GET /:id/deliveries use `.catch()` to turn a rejected query into a 200, so those cells throw synchronously, and controls A0/C0 pin the benign branch. PATCH turns a SQLSTATE into a 400, and control B0 pins that.
- **Not an auth/credential change.** rotate-secret handles a secret, but brief B changes only the catch's response line (`:352`). The secret path is not touched: generation, encryption, storage, the one-time return and HMAC signing (`:345-:350`, `:42-:62`, `:433`) stay byte-identical, and a green control pins it end to end. The thrown text now goes to the log instead of the client. It cannot contain the plaintext secret: `encryptField`'s throws (`encryptedField.ts:286/293/301/318`) never include `plaintext`, and the UPDATE binds only ciphertext. **So this does NOT change secret handling, and I do not recommend routing it to a Claude seat.** If Wednesday reads "security surface" literally (the whole ticket is an info-leak fix), B is the one to move to a cloud seat. A and C do not touch rotate-secret.
- **Round counter.** 0. This is the first brief. Linear shows Backlog, no attachments.

## What was measured (scratchpad `golden/`, not shown to the model)

- `build_golden.py` builds `webhooks.A.ts`, `.AB.ts` and `.ABC.ts` from the develop blob. `assemble_and_check.sh` assembles `A/B/C.golden.diff`, and `git apply` (strict, no `--recount`) applies them as a chain on a scratch copy. The result equals the goldens byte for byte.
- The diff reconstructed from each brief's fenced blocks equals that brief's verified golden diff.
- `typescript@5.9.3 transpileModule` found 0 syntax errors in all 3 test files and in `webhooks.ABC.ts`.
- Source counts: at A+B+C, 0 `message: err.message` response lines, 7 `fail500(res,` calls, 7 distinct contexts and 1 definition. At A+B the counts are 2 leaks and 5 calls, so C3 is RED there.
- Each tamper line appears exactly once in its tree.

## UNMEASURED (also in each brief)

- **No test was run.** That means no jest, no ts-jest type-check and no eslint. RED at the tip and GREEN after the fix are reasoned, not observed. The checker's first run is the first execution.
- It is untested whether the `it.each` row type (non-`as const`, union `body`) type-checks under ts-jest. It is also untested whether setting `NODE_ENV=production` inside the jest worker has side effects.
- The rest of the originate suite was not run.
- Open PRs were not listed via the GitHub API. Only `git ls-remote` branch names were checked: the ks-1160 branch is the pre-squash head of merged #1186, and the ks-927 branch has no commits touching this file.
- The eslint verdict on a helper declared after its callers comes from reading the config (it has no `no-use-before-define`), not from a lint run.

## REV 2, SUPERSEDED BY REV 3 BELOW (Wednesday, 2026-09-26 15:1x) — brief A's Edit 3 re-anchored
The builder's blank-context rule (IMPROVEMENTS.md, 2026-09-18) refused rev 1: Edit 3 anchored on the blank `:548`. Rev 2 inserts the helper AFTER `:549` `export default webhooksRouter;` (single non-blank context line; hunk `@@ -549,1 +549,19 @@`). Lines above do not move, so B and C are unchanged. Verified by Wednesday with `patch -p1 -F0` on develop e080174c's webhooks.ts: A, then B, then C all apply strictly; final file 7 `fail500(` calls + 1 declaration, 0 `message: err.message`. `golden/webhooks.{A,AB,ABC}.ts` regenerated from that chain (backups `.pre-*-blankctx`). **`golden/assemble_and_check.sh` is STALE** (it hard-codes the rev-1 insertion at 549-566 / `@@ -545`); do not re-run it to regenerate the diffs. `KS-1341.md` is a copy of `brief.md` (the name the builder looks for).

## REV 3 (Wednesday, 2026-09-26 15:1x) — Edit 3 = the helper FIRST, then `:549` as the only (trailing, non-blank) context
Rev 2 was refused by the builder's leading-only-context rule. Rev 3 puts the 18 inserted lines (docblock, helper, one empty `+` line) BEFORE `export default webhooksRouter;`, which is the single trailing context line (`@@ -549,1 +549,19 @@`). Verified: A, then B, then C apply strictly (`patch -p1 -F0`) on develop e080174c's file; final 7 `fail500(` calls + 1 declaration, 0 leaks; goldens regenerated (backups `.pre-*-rev3`); `KS-1341.md` re-copied. `assemble_and_check.sh` stays STALE.
