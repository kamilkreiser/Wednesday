PR 2111: GO WITH NOTES; PR 2112: GO

# Gate 275, tier 1 batch (Opus): PR 2111 (KS-2109, D5) and PR 2112 (KS-2120, D6)

| PR | Head | Verdict |
|---|---|---|
| 2111, KS-2109 (D5) | 4fff98cb12f2ae5e11619ef5d38176d7c16a45a5 | GO WITH NOTES (no defect in the diff; one pre-merge board item carried, G275-2111-3) |
| 2112, KS-2120 (D6) | ba5cb57dcecaeeff6e0bbc226597c40d19141afc | GO |

## Pins (ls-remote at origin)

| Ref | Start 22:38:23Z | End 22:57:27Z | Moved? |
|---|---|---|---|
| develop | a1bfe7a7df25 | **4e529633d0a1** | **YES**: one commit, `Refs KS-1971` (ssrf-guard.ts, its test, two KS-1971 fragments). It shares no path with either PR, or with any file their claims or cells read (15-path watch list, positive control 1 of 1). Both PRs merge-tree clean on 4e529633 too (rc 0). Neither verdict is voided: they rest on PR heads, which did not move. |
| PR 2111 head | 4fff98cb12f2 | 4fff98cb12f2 | no |
| PR 2112 head | ba5cb57dceca | ba5cb57dceca | no |
| PR 2109 head | 5350041b426d | 5350041b426d | no |
| PR 2110 head | 2cfbd109db5d | 2cfbd109db5d | no |

All tests ran on develop a1bfe7a7df25 with each PR's files laid over it. For every changed path, develop's blob equals the PR's cut base, and the merge-tree diff equals the PR's own diff byte for byte, so the overlay is the merge.

---

## PR 2111 (KS-2109, D5): GO WITH NOTES

**BLUF.** The PR changes only what the READY says: one comment line in trustHeaders.ts, one line in AGENT-DOCUMENT-OPERATION-RULES.md, and two new fragments. Both new sentences are true at develop. No code byte moves (two independent methods, three controls). The ks1536 guard reads the same at develop, at the head and on the union with PR 2109: 0 failed on every side. I planted a defect in the trustHeaders comment and the guard caught it, which proves the guard reads this file. The notes are wording, plus one item that should go to the board before merge.

### Q1. Does the diff do only what the READY says, and is each new sentence true?
FOUND: 4 files, +32 -2. They are trustHeaders.ts:37, AGENT-DOCUMENT-OPERATION-RULES.md:55, and the cheat and flow fragments `KS-2109-trustheaders-and-the-agent-rules-name-removed-role-lists.html`. That matches the READY. trustHeaders.ts went from blob 1de21fc3 to f4965f03, sha256 91d5844ff3fd, which matches the READY's 91d5844ff3fd427a.
- **trustHeaders.ts:37** now reads "gating on `isPlatformRole` (from @secuura/shared) before doing so". TRUE. `services/api-gateway/src/middleware/auth.ts:14` has `import { isPlatformRole, isSessionActive, runWithTenantId } from '@secuura/shared';`, and `:696-698` reads `const tenantOverride = req.headers['x-tenant-override'] ...; if (tenantOverride && isPlatformRole(decoded.role)) { req.headers['x-tenant-id'] = tenantOverride;`. `isPlatformRole` is `packages/shared/src/security/keyRevokePolicy.ts:140`, which applies an ASCII fold and then checks membership of `PLATFORM_ROLES = new Set(['SYSTEM_ADMIN', 'SUPER_ADMIN'])` (:60).
- **AGENT-DOCUMENT-OPERATION-RULES.md:55** now reads "`enforceAdminProxy` ... asks `isPlatformOrOrgAdminRole` and so admits `SYSTEM_ADMIN`, `SUPER_ADMIN` and `ORG_ADMIN` only: human roles". TRUE. At `routes/proxy.ts:1256-1258`, `if (!user || !isPlatformOrOrgAdminRole(user.role))` refuses with 403. It is mounted only on `/api/admin/` (:1265-1267). `keyRevokePolicy.ts:163-166` returns `PLATFORM_ROLES.has(folded) || folded === 'ORG_ADMIN'`. The connector mint stamps `role: 'connector'` (`services/auth/src/services/jwt.ts:291`), so a key is refused there. The phrase "only" leaves out the ASCII case fold (`super_admin` is admitted too). The flow fragment states the fold, so I count it as no finding.
- Fragments: "gate 244 found that every gate it drove behaved as PR 2060 says" is TRUE. Gate 244's verdict reads "every gate I drove behaved as the PR says", and its F5 lists exactly these three stale pointers. The fragments' description of the "not done" items (index.ts:327-329 stays out) matches the code: `index.ts:327-329` still names `SUPER_ADMIN_ROLES.includes(decoded.role)`.

### Q2. Comment-only proof
HOW: `ts.transpileModule` with `removeComments: true` (TypeScript from the clone), plus a separate method: the full `ts.createScanner` token stream with trivia skipped, hashed. The script is `scratchpad/emit/cmp.cjs`.
TESTED: develop against head gives emit 567ffef7ebc4396c, 790 B, IDENTICAL, and tokens 12ac8f7240a3ae0f, IDENTICAL. The raw bytes DIFFER. The seat's 567ffef7ebc4396c / 790 B is reproduced. Controls: a code change (the allow-list gains `'x-user-id'`) makes both DIFFER. A planted comment line leaves both IDENTICAL. A comment break-out (`*/ export const PWN = 1; /*` inside the edited comment) makes both DIFFER.

### Q3. ks1536 guard: head and union with PR 2109
HOW: vitest json reporter in packages/shared, with files laid over develop a1bfe7a7df25 and restored after each run. Runner: `scratchpad/emit/state_run.py`.
| State | Tests | Failed |
|---|---|---|
| develop | 97 | 0 |
| + PR 2111 | 97 | 0 |
| + PR 2109 only (control) | 99 | 0 |
| **UNION 2111 + 2109's test file** | **99** | **0** |
The red set is the same as develop's (empty). Plants on the union, with my own defect in trustHeaders.ts's edited comment line: `['super_admin', 'platform_admin']` reds G1 and G2. `new Set(['SUPER_ADMIN', 'SYSTEM_ADMIN'])` reds G2 only. Both are as expected, and they prove the guard sweeps this file.
Also run: the 4 api-gateway test files that name trustHeaders read 22 of 22 at develop and 22 of 22 at the head. The whole api-gateway suite read 168 files, 1872 tests, 1 failed at develop, and exactly the same at the head. The red is the same test on both sides (`ks1090` type-check baseline: `TS2307 Cannot find module '@electric-sql/pglite'`), and `ks1256-settings-store-statements-on-a-real-engine.test.ts` fails to import in my clone. Both come from my partial workspace install (three workspaces only). The 8 tests in that file account for the gap from the seat's 1880 exactly (file-by-file diff against the seat's after_suite.json). No test file reads AGENT-DOCUMENT-OPERATION-RULES.md (grep, with a positive control of 4 hits for trustHeaders).

### Q5. Fragments, and the hyphenated 'KS-1536'
`node Blockchain/Dev/scripts/docs-fragments.mjs check --root <clone>` returned rc 0 at develop (221 new entries), at the head (220, because it was cut on an older develop), and on my local union develop+2111+2112 (223 = 221 + 2). It prints "lint clean, render passes html_docs_check". The two ADVISORY lines (a committed page differs from the render at flow:6249 and cheat:6235) are present already at develop, so they are not this PR's. Planted control: an unclosed-tag fragment gives rc 1 with a tag-balance finding. I moved it to `scratchpad/_quarantine_2026-11-09/`, and the check then returned rc 0.
'KS-1536' hyphenated once in each fragment: **no effect that I can find.** The checker reads ticket keys only from the file NAME and from `<!--ref:KS-...-->` tokens, and lints only names, tags and tokens. Its rc is 0 with the key present. Whether Linear reads file content at all I did NOT test (no Linear read; network only for git). Linear links from branch, title, body and commits. I agree with Wednesday's default: leave it.

### Q6. Merge tree and overlap
`git merge-tree --write-tree develop pr/2111` returned rc 0, 4 files, and its diff equals the PR's own diff byte for byte. Pairwise with 2112, 2109 and 2110: rc 0 each. Planted control: a commit on develop that rewrites trustHeaders.ts:37 differently against pr/2111 gives rc 1, `CONFLICT (content)` in trustHeaders.ts. The same plant against pr/2112 gives rc 0. Open PRs: 46 `refs/pull/*/merge` at origin (the seat's census read 47 before 2105 merged). Paths were taken from each merge ref's first-parent diff. No open PR WRITES any of 2111's 4 paths. A planted path is found, naming PR 2110. PR 2109 shares a READ file (the ks1536 test), which the union in Q3 covers. PR 2066 shares the directory `docs/security` (it edits ROLES-AND-AUTHORIZATION-INVENTORY.md, not this file), and it also edits `keyRevokePolicy.ts`. I read that diff: it changes `decideTenantAccess`/`decideKeyRevoke` (adminIsLive) only and does not touch `isPlatformRole` or `isPlatformOrOrgAdminRole`, so the new doc line stays true after 2066. Merge order: any.

### Q7. Ticket comment e4a94ed6
NOT read live (no Linear access under the network-git-only rule). I checked the seat's posted source `evidence/d5/mail/ticket_comment_FINAL.md`, which the seat read back as "body equal modulo normalisation: True", against the code: every factual sentence holds at this head. They are the 4 files, +32 -2; the two replacements as worded; the index.ts pointer ruled out; and the PR 2109 line. "15 of 15 code claims" is the seat's count, which I did not recount, though I verified each claim the new wording makes (above).

### Findings
- **G275-2111-1, Low (wording, fragment).** The cheat fragment's Figures row reads "files, lines: **2** files against develop, **+2 -2**", and the flow fragment reads "Two lines of prose, in two files". The PR is 4 files, +32 -2. Read as "the code and doc files", it is true, but the cheat page states it as the PR's figure. D6's cheat words the same row correctly ("... plus these two fragments"). Not blocking.
- **G275-2111-2, Info, PRE-EXISTING and OUTSIDE the diff, READ ONLY and not measured at runtime. Candidate for the board.** The unchanged premise around the edited clause, "auth middleware decides whether to honour it", is not the whole story. The gateway never deletes `x-tenant-override` for a non-platform caller: auth.ts:696-704 only decides `x-tenant-id`. originate's `GET /api/admin/dashboard` (`routes/adminConfig.ts:603`, `:621-623`) reads the raw `x-tenant-override` header to filter counts by another tenant. Its gate is `requireRole('SYSTEM_ADMIN', 'ORG_ADMIN')` (:45), and the gateway's `enforceAdminProxy` admits ORG_ADMIN. So an ORG_ADMIN token appears able to read another tenant's document, user and verification counts, or the platform totals without the header. The edited clause itself is true, and this PR neither causes nor worsens it. Severity if confirmed: Moderate, as its own ticket.
- **G275-2111-3, Low, pre-merge board item (carried from the seat's census; UNMEASURED by me).** PR 2111 is attached to KS-1536 as well as KS-2109, through the branch name `feature/ks-2109-ks-1536-follow-up-the-one-role-vocabulary`. The seat measured 0 hits for ks-1536 in the title, body, commit and comment. What Linear's merge automation does to a ticket linked only by branch name is unmeasured. KS-1536 is an open umbrella. Recommend the board seat (S 41st, per the seat's note) detach KS-1536 before merge, or Wednesday confirm the automation leaves branch-only links alone.

NOT TESTED (PR 2111): the live ticket comment and PR body on Linear and GitHub (read from the seat's local copies only). eslint and tsc (not needed for a comment-proven change, and not rerun). Markdown link check of the doc page. Node 24 (all runs on v26.8.1). Any runtime probe of the tenant-override path (G275-2111-2 is read only).

---

## PR 2112 (KS-2120, D6): GO

**BLUF.** The PR is one comment edit in transferAccess.ts (1 line replaced, 3 added) and two fragments. Every claim in the new comment is true at develop, and it corrects a claim gate 240 had found wrong. No code byte moves. The transfer suite and the ks2081 doors test read the same at develop, at the head and on the union with PR 2110: 0 failed on every side. A planted defect in `isNonUserPrincipal` reds 12 doors cells, which proves the cells exercise this file. No findings.

### Q1. Diff and truth
FOUND: 3 files, +32 -1. They are transferAccess.ts:112 (replaced) plus :113-114 (added), and the cheat and flow fragments `KS-2120-transferaccess-comment-names-the-platform-admin-login.html`. transferAccess.ts went from 3d216a2b to d7e1184b, sha256 e3392639bf77, which matches the READY.
New claims, checked against develop a1bfe7a7df25:
- "The platform-admin login does not read those tables: it mints platform_admins.role as stored". TRUE. `services/auth/src/routes/auth.ts:367` has `userRepo.getPlatformAdmin(data.email)`. At `:470-471` the token is minted by `generateTokenPair({ ...syntheticUser, role: platformAdmin.role as any }, session.id)`. `repositories/userRepo.ts:1929-1941` has `SELECT id, email, password_hash, name, role, ... FROM platform_admins` with `role: row.role` unmodified. (The seat's "two sites, 471 and 495": :495 is the response body, not a mint. The comment says "mints", which is right either way.)
- "could carry a connector role only if someone wrote one into that row". TRUE for the role signal. The same login stamps `verificationLevel: 'ENHANCED'` as a constant (auth.ts:404). `id` is UUID in both schemas, so the GUID signal does not fire either. No other mint call site (auth.ts:305/634/754/1413, oauth.ts:1012/1144, wallet.ts:384) reads platform_admins.
- "The docker schema (docker/init-platform/01-platform-schema.sql) CHECKs that column to three values". TRUE. Lines 79-80 read `role VARCHAR(30) NOT NULL DEFAULT 'super_admin' CHECK (role IN ('super_admin','platform_admin','platform_viewer'))`.
- "the Azure migrate script (deployment/azure/migrate/run-platform.sh) declares it with no CHECK". TRUE. Line 69 reads `role VARCHAR(50) DEFAULT 'admin',`. No ALTER adds one: the only ALTERs (:77-78) add mfa columns, and an ALTER/CHECK grep across *.sql and *.sh finds nothing else.
- Fragments: "the gate that read PR 2077 said no behaviour change is needed for it" is TRUE. Gate 240's verdict, line 38, says "No behaviour change is needed for this PR. The comment is wrong in one case." "auth.ts builds that token with role: platformAdmin.role", "userRepo.ts returns the column straight from the row" and "four comment lines" are all TRUE. Other keys are spaced (KS 1536, KS 2081). The fragments cite KS 1536 comment `0f41081f`, which I did NOT verify (Linear).

### Q2. Comment-only proof
The same two methods. develop against head gives emit 915649e292b579eb, 2440 B, IDENTICAL, and tokens 327e151b580075c9, IDENTICAL. The raw bytes DIFFER, and the seat's figure is reproduced. Control: a comment break-out (`*/ const PWN = 1; /*` placed after "as stored") makes both DIFFER. The code and plain-comment controls ran on the trustHeaders pair with the same instrument.

### Q4. Transfer suite and the ks2081 doors test, head and union with PR 2110
| State | ks2081 doors test | whole services/transfer suite |
|---|---|---|
| develop | 107 / 0 failed | 16 files, 460 / 0 failed |
| + PR 2112 | 107 / 0 | 460 / 0 |
| + PR 2110 only (control) | 108 / 0 | (not run alone) |
| **UNION 2112 + 2110's test file** | **108 / 0** | **461 / 0** |
The red set is the same as develop's (empty). My plant, on the union: remove the `type` and `role` connector signals from `isNonUserPrincipal` and neuter `verificationLevel`. Result: 12 of 108 failed (the C1, C2 and R6 cells). The suite sees this file. (An aside that is not this gate's to rule: PR 2110's new F1 cell stayed green under that plant, because its `key(null, …)` token is still refused by another signal.)

### Q6. Merge tree and overlap
`merge-tree develop pr/2112` returned rc 0, 3 files, and its diff equals the PR's own diff byte for byte. Clean with 2111, 2109 and 2110. No open PR WRITES any of its 3 paths. PR 2110 shares the READ file (ks2081 test), which the union above covers. 2111 and 2112 share no path (an empty intersection, beside the planted control that does find one). Merge order: any.

### Q7. Ticket comment 16d3f464
NOT read live. The seat's posted source `evidence/d6/mail/ticket_comment_FINAL.md` is true at this head on every factual sentence (3 files, +32 -1; the new wording as described; the PR 2110 line). The `0f41081f` reference on KS 1536 is not verified.

### Findings
None.

NOT TESTED (PR 2112): the live Linear and GitHub text. KS 1536 comment 0f41081f. Any real platform_admins row, decoded token or run of the login (read from code only, like the seat). tsc (comment-proven, not rerun). Node 24.

---

## Own conduct
- Commission path deviation: the clone the commission named, `/private/tmp/g275`, was made (blobless, 11M). The fleet hook `pretooluse_no_cd.sh` then refused write verbs (checkout, merge-tree) outside WEDNESDAY other than the session scratchpad. All work moved to a fresh clone at `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/121f796c-56a6-4f7c-83fc-ac8bf3fbcbfe/scratchpad/g275`, 884M, on the boot volume, including 421M of node_modules and the shared dist. **Neither was removed (QA no-rm).** `/private/tmp/g275` (11M) is abandoned and can be quarantined. I also wrote two stray logs outside my gate folder and clone, `/private/tmp/g275.clone.log` and `/private/tmp/g275.fetch.log`, before moving into the scratchpad. They hold no secrets.
- In both clones I set `core.sshCommand` to the project's deploy key, as the checkout does. I never printed the key. I ran no git write verb in any `!CODING` checkout and did not fetch there. I made two local commits (a plant and a two-step union) in the scratchpad clone only, and never pushed.
- Load: two background greps over large folders ran too long and were stopped. A full api-gateway suite run pushed load1 to **13.0** (limit 8) for about a minute. That breaches the commission's constraint. I ran nothing heavy after it, and load returned to 4.8.
- Nothing was posted, commented or mailed. DevMASTER free space: 107 GiB at start, 108 GiB at end.
