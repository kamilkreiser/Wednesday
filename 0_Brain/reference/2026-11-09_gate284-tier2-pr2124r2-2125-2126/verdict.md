PR 2124: GO WITH NOTES; PR 2125: GO; PR 2126: GO

Gate 284, tier 2 (Sonnet). Findings only; nothing posted, mailed or pushed.
Pins re-read at start (16:06) and end (16:09): develop 204e62acdc35, 2124 17f43f1be684, 2125 f9e9da889d42, 2126 f70c0833f660 (and 2127 190ffa868d7d, 2052 b61674e7b763 at start). NONE moved.
DevMASTER free 106 GiB at start and end (df). Load1 6.6 at start, 4.6 at end. Clone /tmp/g284 (boot volume) = 1.3 GB at the end (repo + 3 worktrees + scratch); no rm used by me.

## Files and stop line (Q1)
| PR | file | class | non-comment byte in a PRODUCT file? |
|---|---|---|---|
| 2124 | Blockchain/Dev/scripts/smoke-test.sh | dev/ops tooling script (tier 2) | n/a: changed code is tooling (the sed in the echo) |
| 2124 | Blockchain/Dev/scripts/__tests__/smoke_test_honours_smoke_base_url.test.sh | test | no |
| 2125 | api-gateway/src/index.ts | PRODUCT | 0 non-comment bytes (proved below) |
| 2125 | Projects Documents/fragments/{cheat,flow}/KS-2109-...html | docs | no |
| 2126 | systemTest/fixtures/provision.ts | test fixture, not a deployed service | 0 non-comment bytes (proved below) |
Stop line not tripped for any PR.

## FOUND / TESTED / HOW

### PR 2125 (GO)
- Claim comment-only: PROVEN. Instrument: typescript 5.9.3 (from the repo's own node_modules, read-only) transpileModule, removeComments true, develop's index.ts vs the head's blob. Result: stripped-equal true, with-comments-equal false. Controls: planted code edit (req.headers -> req.header) stripped-equal false; planted comment edit stripped-equal true, with-comments false. The diff hunk (read whole) is 12 lines, every one inside a `//` run, lines 324-333.
- Comment true at this develop: auth.ts:697 is `if (tenantOverride && isPlatformRole(decoded.role))`; verifyRs256(token) at auth.ts:651 precedes it in the same handler; isPlatformRole is imported from '@secuura/shared' (auth.ts:14), defined packages/shared/src/security/keyRevokePolicy.ts:140 over PLATFORM_ROLES = {SYSTEM_ADMIN, SUPER_ADMIN} (line 60). `SUPER_ADMIN_ROLES` count in auth.ts = 0 (positive control: isPlatformRole count 2), so "KS-1536 replaced that list" is consistent. No other tenantOverride site in auth.ts (only 696-697).
- Fragments claim "code changed 0 ... 39,572 bytes": I did not measure bytes; the zero is reproduced by the compare above. Suites 1880/99 not re-run (NOT TESTED).
- No findings.

### PR 2126 (GO)
- Claim comment-only: PROVEN, same instrument. provision.ts develop vs head: stripped-equal true, with-comments false. Control: planted `split(` -> `splitX(` gives stripped-equal false.
- Comment true: buildPassword = `Ks256-${key}-${seed}-Pw!` (actors.ts:99); buildEmail = `ks256-${key}-${seed}@secuura-test.invalid` lower-cased (actors.ts:43,122); the Error at provision.ts:343 interpolates spec.key and spec.email while redactSecrets (342) only scrubs spec.password; redactSecrets is a plain split/join (line ~277). Rebuild from the banner is therefore possible.
- G284-2126-1 (info, no action): "A server echo that JSON-, URL- or HTML-escaped the password is not matched" is true of the function, but for the generated passwords (`Ks256-<key>-<seed>-Pw!`) none of those escapings changes the string, so it is a theoretical caveat today. Harmless.

### PR 2124 round 2, delta only (GO WITH NOTES)
Delta b2853fcf9274 -> 17f43f1be684 = 2 files, +10/-2 (smoke-test.sh +3/-2, suite +7/-0), as the seat says. Scope: smoke-test.sh hunk touches only lines 17-19 (comment reword + the sed); the 15 full-run warnings are untouched (warn() call sites unchanged, only shifted +1 line). Three sibling smoke suites are not in the diff (byte-identical by omission); I ran smoke_test_degraded_warns at the head: 5 passed, 0 failed.
- G282-2124-1 CLOSED. Comment (lines 17-18) states the stripping rule (to the last @ before the first /) and names what is NOT covered (skip warnings, scheme-less URL, query string). True of the code.
- G282-2124-3 CLOSED. warn() call sites in direct_skip / local_skip are at 47 and 56 on the parent, 48 and 57 at the head (instrument: sed line-number grep on both worktrees, positive control: both worktrees return the two lines).
- G282-2124-4 CLOSED. Suite at head 9 passed, 0 failed. Parent's script + head's suite (assembled in a scratch tree so REPO_ROOT resolves to the parent script): 8 passed, 1 failed, the one FAIL is the new raw-@ cell. The cell greps -F "ssw0rd-tail" in the --quick output: it does not pass for the wrong reason (fails on `[^/@]*@`).
- Mutants (suite run against each mutated script, mutant file confirmed to differ): old `[^/@]*@` caught (1 FAIL, new cell only); `.*@` NOT CAUGHT, 9/9 pass, CONFIRMING the seat's statement; no scheme anchor caught (3 FAIL); my own, `[^/]*@[^/:]*` (eats the host), caught by the "scheme, host and port only" cell (1 FAIL). A first "no-greedy" mutant of mine was malformed (sed error) and is discarded, not counted.
- G282-2124-2 PARTLY CLOSED, and the comment is false in one shape: G284-2124-1 below.
- Not re-opened: round 1.

## Findings
- G284-2124-1 (LOW, residue to ticket; closes G282-2124-2 only partly). The comment, body and ticket comment say a secret in the query string "is printed unchanged". For a URL with no path and an `@` in the query, the sed strips from the host: measured with the head's exact expression (BSD sed -E), `https://h?token=a@b` prints `https://b` (host and the query up to the @ are dropped; nothing after the last @ is hidden). `https://h/p?e=a@b` and `https://h?x=1&e=a/b@c` are printed unchanged, as claimed. Effect: a mis-print of the target (a SMOKE_BASE_URL with a path-less query containing @), no new leak, but the "unchanged" sentence is not true for that shape. Control: the credentials case `https://u:p@h:1` prints `https://h:1`.
- G284-2124-2 (INFO). The '.*@' mutant surviving means no cell pins "the userinfo ends at the first / ": a slash-bearing path containing @ (`https://u:p@h/p@q` measured: prints `https://h/p@q`, correct) is protected only by the code, not by a cell. Seat already disclosed this; it is residue, not a ship-stopper.
- G284-2124-3 (INFO). I did not read the live PR body or ticket comment (no network but git); the seat's READY says they were edited to match. NOT TESTED.

## Merge trees (Q4)
git merge-tree --write-tree on develop 204e62acdc35: 2124 rc 0 (tree 3b257363), 2125 rc 0 (db4cca90), 2126 rc 0 (af43dc1a); all three merged in sequence rc 0 (tree 83edf3d1). Shared paths pairwise among 2124, 2125, 2126, 2127, 2052: all 0 except 2052/2127 = 1 file (check-slot-credentials.sh), which does not involve this batch. Control: 2125 against itself = 3 shared paths (the comm instrument works). Other open PRs beyond 2127 and 2052: NOT TESTED (no PR list without gh/network; the seats report 0 open PRs on their paths).

## NOT TESTED
Live PR bodies and Linear comments (network is git only). api-gateway/guard suites (1880, 99) and the packages/shared build. GNU sed (only BSD sed here). Scheme-less and uppercase-scheme edge shapes were probed by hand only (`HTTPS://u:p@h` -> `HTTPS://h`; `u:p@h.example` unchanged, as the comment says). The skip-warning leak itself (named residue). Other open PRs.

## Conduct
Wrote only under /private/tmp/g284 and this file. Nothing in !CODING was written or fetched into (only `git config` / `ls-remote`-style reads and the remote URL/ssh command read from the 2_Project_Files checkout config). No .env opened. The suite's own trap does `rm -rf` on its mktemp dir under /private/tmp/g284/tmp (the suite's code, not my command). No push, post or mail.
