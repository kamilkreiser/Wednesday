#1230 KS-1131 CALLSHAPED: ks963 helper counts consume CALLS, not mentions (items 1, 2)
head 1116dab0466da48ce96c4811f8086b061a49aa70

## BLUF

`assertConsumeIsGuarded` is the structural check behind the two ks963 cells, and it read RAW TEXT, so it could be fooled in both directions. Two of the ticket's four items are addressed here, as two commits on one file.

**F-A, property 2:** the count between the expiry guard and the user lookup counted the raw NAME, so a comment or log string merely MENTIONING `consumeResetToken` in that gap counted as a call and reddened a correct file. It now counts call-shaped occurrences.

**F-B, property 1:** the `!user` guard body only had to CONTAIN the name, so a comment naming it satisfied the guard while no consume ran - a false green on the branch that stops a single-use reset token being burned on a missing user. The body must now contain the call-shaped name too.

This file is both the product (its helper) and the suite that grades it, so the change and the cells that pin it land together.

## This PR NARROWS the ticket, it does not complete it

Items 3 (F-C, the `:256` non-await write) and 4 (P2, the positional wallet slice) remain open. `:218`, the expiry-body count, is untouched. `:206` is kept, so the guard body now asserts both the raw and the call-shaped name; the raw one is implied by the new one and a later tidy may drop it.

## Test Evidence

**Touched** - `Blockchain/Dev/services/auth/src/__tests__/ks963-preauth-rethrow.test.ts` only. No product source outside this file; `auth.ts` and `wallet.ts` are read by the suite and unedited.

**Ran, by me, at this head**
- auth lane **bare 828/828** over 76 files at develop, **patched 832/832** over 76 files. `tsc --noEmit` rc 0 both sides.
- **RED-FIRST, one arm per conjunct**, from the checker's own split halves:

| arm | tree | F-A cell | F-B cell | controls |
|---|---|---|---|---|
| A | both test hunks, neither edit | RED in 1ms | RED in 3ms | both green |
| B | plus F-A's edit only | green | RED in 3ms | both green |
| C | plus F-B's edit | green | green | both green |

Arm B is the one that earns F-B its place: with F-A applied, exactly the F-B conjunct survives. Arm C's file is byte-identical (`cmp` rc 0) to what is committed here. My cells fail in 1ms and 3ms, i.e. assertion reds; every other red in arm A was 3000ms or slower.
- Per-stage blobs asserted: F-A alone `560bb49c242f` / 354 lines, stacked `041396c7fce5` / 381 lines, tip `9427c652ac2d` / 327.

**NOT run**
- Push preflight verdict, verbatim: `PREFLIGHT INCOMPLETE - 12/15 legs ran, 3 SKIPPED. Nothing failed.` Legs 3, 4 and 8 NOT run (local stack not up on :6882); this PR has no route, spec, served-spec or runtime-config surface.
- The helper is still text-based, so the residual is real and MEASURED rather than assumed, in both directions: a comment that writes the name WITH a paren (`// consumeResetToken(x) was here`) inside the `!user` block still satisfies property 1 - a false green that survives this PR - and the same shape in the gap gives a false red, the safe direction. A call written `consumeResetToken (x)` would not be counted; prettier never emits it. The comment-and-string stripper the ticket also offers is the stronger remedy and is not this change.
- No HTTP request was made; the five pre-auth callers are exercised only through the helper's synthetic handlers.
- One auth run reddened 3 cells and another 1, all `Test timed out` in `ks949-platform-admin-seed-identity.test.ts`, a repo-walk guard this PR does not touch. Each was re-run once and came back 828/828 and 832/832. The identical file passed in a sibling worktree at the same blob, and failure count tracked the import phase (152.50s / 62.59s / 39.70s).

**Migrations + config** - none.

Refs KS-1131


🤖 Generated with [Claude Code](https://claude.com/claude-code)

