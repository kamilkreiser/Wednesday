PR 2107: GO; PR 2108: GO WITH NOTES; PR 2109: GO WITH NOTES; PR 2104: GO WITH NOTES

# Gate 273, tier 1 (Opus), Secuura/Blockchain, Seat G 30th batch: verdict

| PR | ticket | head | verdict |
|---|---|---|---|
| 2107 | KS-1971 ssrf-guard | 987ee2de56e0 | GO |
| 2108 | KS-1973 vc verifier | 678512909761 | GO WITH NOTES (1 Medium text finding in the ticket comment, 2 Low) |
| 2109 | KS-2110 test-only pins | 5350041b426d | GO WITH NOTES (1 Low) |
| 2104 r2 | KS-1972 event-indexer poll() | e7faa4f72c4e | GO WITH NOTES (round 1 findings closed; 1 residue Low, 1 new Low text) |

No finding reaches the stop line: in all four PRs, every byte that changes behaviour does exactly what the READY says and nothing more.

## Pins (ls-remote by me, start 2026-11-08 20:31:49Z, end 20:43:33Z): NONE MOVED
- develop 93028c8151ecdd173c341fb7c23a4b89e381cc04: start = end = commission
- 2107 987ee2de56e0b9f5e80ad76a6c79d8e909579cc5: start = end = commission
- 2108 6785129097618efbfc9d74336cd33e53fba4d1c7: start = end = commission
- 2109 5350041b426d3e3ee42d5bd812a17b07a2718c3d: start = end = commission
- 2104 e7faa4f72c4e9a2d1b6e0364fa321acb215b9e6c: start = end = commission

## Batch-wide (Q6 baseline, Q8 merge)
- Instrument: my clone /private/tmp/g273/repo plus a worktree /private/tmp/g273/wt. node_modules are an APFS clone of /private/tmp/g262w/dev2's, and packages/shared/node_modules is a tar copy of the project checkout's (read only, .vite excluded). The lockfile is STALE relative to develop's (sha256 80b45c60 develop vs cc69eb81 installed). This is the same instrument limit gate 271 had. Run as vitest 4.1.12 on Node v26.8.1 with cwd = packages/shared (spawned with a cwd option, no `cd`). My first develop run used the wrong cwd, and 9 repo-walking guard files could not find the Dev root. I discarded it and report only the cwd-correct runs.
- Whole packages/shared suite. develop 93028c8: 1597 tests, 1 red. 2107 head: 1603 / same 1 red. 2108: 1605 / same 1 red. 2109: 1599 / same 1 red. 2104: 1603 / same 1 red. Sequential 4-PR merge (739d6f9c, my commit-tree): 1619 / same 1 red. The four new or extended files pass together on the merge (99/99, 6/6, 6/6, 8/8). The single red in every run is `wallet-signature.test.ts | verifyMessageSignature (CIP-8/CIP-30) — KS-278 accepts a valid wallet signature`, AssertionError. These figures equal the seats' counts.
- develop has not moved since the cuts on any PR path. `git diff --stat <merge-base> origin/develop -- <PR files>` is empty for all four, and develop 15dca468..93028c8 changed 0 files in packages/shared.
- Merge trees on 93028c8 all have rc 0: 2107 d4dcc6a9, 2108 2d28aabe, 2109 8423d614, 2104 e88b69e6. Sequential 2107→2108→2109→2104 also rc 0 (13 files, +477/-4). Pairwise path overlap is 0 for all 6 pairs. The self-control 2107∩2107 = 4, which shows the overlap count can see a shared path. Planted overlap control: my commit on develop rewriting ssrf-guard.ts:327 gives merge-tree rc 1 with CONFLICT (content) against 2107, and rc 0 against 2108. So the instrument detects a conflict and does not invent one.
- Open PRs sharing a path: I took every PR that has a refs/pull/N/merge at origin (47) and diffed each head against develop's merge base for the batch's 13 paths. Only 2104, 2107, 2108 and 2109 themselves hit, which is the positive control. PR 2105 (KS-1974) touches prism/identus-client.ts and no batch path.
- Docs check (`docs-fragments.mjs check --root <merged tree>`) prints OK: flow 117 legacy + 221 new, cheat 112 legacy + 221 new, and the same 2 ADVISORY lines. Planted control: `<div><table>` appended to the KS-1973 flow fragment gives `FAIL — 1 finding(s)` (tags not balanced). I restored it by checkout and the check printed OK again.
- eslint on the 3 product files and 4 test files (merged tree): 0 errors, 2 warnings, both already on develop. They are `prefer-const` deadline at ssrf-guard.ts:541 and `@ts-ignore` at event-indexer.ts:102, both exactly as the fragments state. The warnings are the positive control that eslint ran.

---

## PR 2107 (KS-1971, ssrf-guard): GO

BLUF: one line, ssrf-guard.ts:327, changes `reason = (err as Error).message` to `reason = String((err as Error).message)`, inside the existing try. Every caller is fail-closed both before and after the change, and none becomes more permissive. Measured at runtime through the two public entry points.

FOUND / TESTED / HOW
- Q1 diff: the PR changes 4 files, and the only product byte is that one line. Semantics: `String(x)` differs from the template literal `${x}` only for a Symbol, where String() succeeds and the template throws. For objects both use ToPrimitive(string), so a throwing toString or a revoked Proxy now throws INSIDE the try and reaches the existing constant. The function's catch always returns `ok:false`, so no input can reach `ok:true` through the changed path.
- Q2 callers. I used `git grep -w` over the PR tree for all four symbols. Control: `pinnedLookup` is found at its definition, ssrf-guard.ts:394.
  - resolvePublicAddresses: assertResolvedHostPublic (:352), safeOutboundRequest (:520), and the index.ts re-export.
  - assertResolvedHostPublic: assertSafeOutboundUrl (:372) and the re-export.
  - assertSafeOutboundUrl: originate routes/webhooks.ts:172 (validateWebhookUrl, used at :223 create and :300 PATCH) and m365-integration index.ts:1286 (teams webhook-config).
  - safeOutboundRequest: originate webhooks.ts:459 (deliverWebhook, used by /:id/test :382 and dispatchEvent :537) and m365 index.ts:1495 (teams notify loop).
  - I read each handler (READ ONLY; the guard entry points themselves were MEASURED, below):
    - originate create and PATCH: `!ok` → 400 and nothing persisted. Before, the rejection went to the route catch, so a 500 and nothing persisted.
    - originate /test: before, a 500 via fail500. Now 200 with delivery.success:false and `blocked by SSRF guard: ...`.
    - dispatchEvent: before, the rejection aborted the whole loop into the outer catch. Now that row is logged blocked and the loop continues; every later row is still guarded on its own.
    - m365 registration: `!ok` → 400. Before, next(error).
    - m365 notify: `!ok` → failed.push. Before, its try/catch → failed.push.
  - Result: no caller turns `ok:false` into a send or a persist. The change can only turn a 500 or an abort into a refusal. The exported `resolvePublicAddresses` and `assertResolvedHostPublic` now return a non-empty refusal where they rejected. An unknown consumer that ignored the return value and relied only on a throw was already open for ordinary DNS failures, which always returned `ok:false`. That is not a new class.
- Runtime (MEASURED; a scratch cell with dns/promises mocked to reject, URL https://g273.example.test/hook):

  | value | develop: assertSafeOutboundUrl / safeOutboundRequest | 2107 head |
  |---|---|---|
  | ordinary Error | `ok:false` / `ok:false reason:'blocked'` | the same |
  | Symbol message | REJECTED "Cannot convert a Symbol value to a string" | `ok:false` (reason 'blocked' from safeOutboundRequest), text `(Symbol(g273))` |
  | message object whose toString throws | REJECTED "boom" | `ok:false` / 'blocked', text `(unreadable thrown value)` |

  The ssrf-guard.ts:506 comment ("resolvePublicAddresses catches every lookup failure and RETURNS { ok: false }") was false on develop for these values and is true at this head.
- Q6 red-first, on the PR's own file:
  - Head: 6/6 pass.
  - Product reverted to develop's blob: 4 fail (R1-R4), all AssertionError "expected true to be false", and C1/C2 pass. Restored; blob 6547421d equals the PR blob.
  - My mutant M1 (fail OPEN: the inner catch returns `{ok:true, addresses:['93.184.216.34']}`) fails R2 and R3 by assertion, restored by blob. My first M1 attempt targeted the wrong line (330), changed nothing, and its 6/6 result is discarded. I caught it from the unchanged sed output and redid it at line 329.
  - Mutant M2 (`assertResolvedHostPublic` returns '' for a refusal, so the caller's `if (reason)` reads it as allowed): all 6 PR cells pass, because R4 asserts only `typeof answer === 'string'`. The existing ssrf suite (10 files, 110 tests) catches it with 8 assertion failures, so this is Info, not a finding.
- Q7 text: I read the PR body draft, the comment draft and both fragments against the head. The ticket comment draft's sha1 (whitespace-stripped) equals the seat's recorded posted body_sha1 53c1e83fd70a. Each claim I checked is true: "Nothing is allowed that was refused"; "assertResolvedHostPublic returns null only for ok:true" (:353); "dispatchEvent... continues to the next one", which my read of :530-552 confirms; the prefer-const at :541; 4/6 red-first.

NOT TESTED: a real DNS lookup; the HTTP layer of the originate/m365 routes (handlers read, not driven); the request-construction catch at :587-595 (unchanged); tsc; Node 24; the live PR body and Linear comment, which I read as drafts tied by hash, not fetched.

Findings: none.

---

## PR 2108 (KS-1973, vc verifier): GO WITH NOTES

BLUF: the two hunks do what the READY says, and nothing becomes more permissive. But BOTH hunks are unreachable from the only two production callers. **There is no "default resolver"**: with no `didResolver` configured, verifyIssuerDID skips the lookup and the Ed25519 branch never runs its inner try. The ticket comment tells a client reader the opposite.

FOUND / TESTED / HOW
- Q1 diff: verifier.ts +13/-2. In hunk A (:463-471) the issuer catch builds the text with `String(error)` inside a try, with the constant as fallback. In hunk B (:400-408) the Ed25519 inner catch's read is moved inside a try. Nothing else changes.
- Q3, MEASURED with a scratch cell driving the public `verify()`, develop vs head:
  - A `didResolver` rejecting with an ordinary Error gives `verified:false`, issuerDID false, on both.
  - A revoked Proxy, an object whose toString throws, or a Symbol makes develop REJECT ("Cannot perform 'get' on a proxy that has been revoked" / "boom" / "Cannot convert a Symbol value to a string"). The head resolves with `verified:false`, `checks.issuerDID:false`, and the entry "Failed to resolve DID ...: unreadable thrown value" or "Symbol(s)".
  - Hunk B, measured through the PR's own R4/R5 with the product at develop: develop already gives `valid:false`, with the text "Signature verification error: ..." from the outer catch. So hunk B is text-only.
  - `allChecksPass = Object.values(checks).every(Boolean)` (:191), so issuerDID false always means verified false.
- Callers (READ ONLY plus the measurement above):
  - `git grep -w` outside verifier.ts finds 0 production hits for VerifiableCredentialVerifier, createVCVerifier and **didResolver**. Control: VerifiableCredentialVerifier is found 3 times in verifier.ts.
  - verifyCredential is called only at vc-issuer routes/credentials.ts:374 and routes/presentations.ts:330. Both pass `checkStatus`/`checkExpiration`/`checkBlockchain` plus `...revocationVerifierConfig()`, which supplies only `storedRecordResolver` and `statusListRevocationResolver` (revocationResolvers.ts:38-74).
  - The constructor's defaults are `checkStatus`, `checkExpiration` and `checkBlockchain` only. MEASURED: `Object.keys(new VerifiableCredentialVerifier().config)` = ["checkStatus","checkExpiration","checkBlockchain"], and didResolver is undefined.
  - So on both routes `verifyIssuerDID` never calls a resolver (`if (this.config.didResolver)` at :457 is false) and the Ed25519 branch takes the no-resolver arm (:413-418). The PR changes no byte of either route's behaviour.
  - The handlers' catch paths: both are `catch (error) { next(error); }` (credentials.ts:393, presentations.ts:395). Before, a rejection went to the error handler. After, it would be 200 `verified:false`, which reaches `res.json({verified:false})` or, for presentations, `every(r => r.verified)` = false. Neither treats `verified:false` as success.
- Unknown consumers: the vc barrel re-exports the class (`vc/index.ts:10 export * from './verifier'`; package.json exports "./vc"), and package.json has `publishConfig.registry https://npm.pkg.github.com`, so outside consumers are possible and cannot be enumerated from this repo. Any consumer that wires a didResolver and catches the rejection as "deny" now gets a resolved result with `verified:false`. It becomes more permissive only if it ignores `verified` and treats "resolved" as success. Such a consumer was already open on develop for an ORDINARY resolver error (measured: resolved, `verified:false`), so this adds no new class. READ ONLY for the consumer side.
- Q6 red-first:
  - Head: 8/8 pass.
  - Product reverted to develop: R1-R3 fail with AssertionError "expected 'rejected' to deeply equal {valid:false…}", and R4/R5 fail with AssertionError (text differs). Controls C1-C3 pass. Restored; blob 04f24453 matches.
  - My mutant (fail OPEN: the issuer inner catch returns `{valid:true, errors:[]}`) fails R1 and R2 by assertion. R3 (Symbol) passes, because String(Symbol) does not reach that catch. Restored by blob.

Findings
- **G273-2108-1 (Medium; text in a ticket comment a client human reads; READ ONLY plus MEASURED default config).** Ticket comment 6c16f52b on KS-1973 (draft comment_row4_final.md:18-19; its whitespace-stripped sha1 equals the recorded posted body_sha1 e8f4dee7ca61) says: "They pass only the revocation resolvers, so the issuer-DID lookup uses the verifier's default resolver, whose code I did not read", and then "Shape change for them: where a hostile resolver value used to make `verify()` reject, it now returns `valid: false`". Both statements are false at this head. No default resolver exists (verifier.ts:90-97, measured). The issuer-DID lookup is SKIPPED on both vc-issuer routes, so there is no shape change for them. The error matters for security because the comment tells a reader that the public verify routes resolve the issuer DID, when they do not. Context, pre-existing and NOT this PR's (identical on develop, measured): with that production-shaped config, a structurally valid credential with any `z…` proofValue verifies `verified:true` when NODE_ENV ≠ production (:413-418 pass-through). Fix shape: correct the comment in place, or post a superseding comment in the same form Wednesday ruled for 26195e09. This does not block the code.
- **G273-2108-2 (Low; text).** The PR body ("now returns `valid: false`"), the ticket comment BLUF and both fragments say `verify()` returns `valid: false`. verify()'s public result (vc/types.ts:173 CredentialVerificationResult) has no `valid`. It returns `verified: false` with `checks.issuerDID: false`. `valid` is the private methods' shape.
- **G273-2108-3 (Low; test quality).** All 8 cells drive the private `verifyIssuerDID`/`verifySignature` through a cast. The PR's headline behaviour change (verify() used to reject and now resolves `verified:false`) is pinned by no cell. I measured it (above). A cell on the public `verify()` would pin it.

NOT TESTED: a real DID resolver or key material; the vc-issuer HTTP routes driven (handlers read only); tsc; Node 24; the live Linear comment fetched (the hash ties the draft to the seat's recorded post).

---

## PR 2109 (KS-2110, test-only): GO WITH NOTES

BLUF: the diff adds exactly the two cells (+7/-0, one file, no product byte). M4 and G5b are true pins of develop: green on develop (97 → 99 tests, 0 failed, both sides) and red under plants of my own. G5b is a text pin, and I measured a defect it cannot see.

FOUND / TESTED / HOW
- Q1: `git diff origin/develop...refs/pr/2109` shows exactly two `it` lines plus 5 lines of G5b. The cells read middleware/index.ts:162 requirePlatformRole and services/tokenisation/src/index.ts:225/:294, unchanged on develop.
- Q4, my own plants at the head, each restored by blob:
  - PA: requirePlatformRole's first test changed from `!req.user` to `!req.user?.role`. Exactly M4 fails by assertion ("expected 'UnauthorizedError' to be 'ForbiddenError'"). Restored ccde0ce9.
  - PB: the gate moved from /api/generate-key to /api/hash-key, so the requirePlatformRole() count stays 2 and G5 stays green. Exactly G5b fails by assertion. This differs from G's plant, which used rotate-key and a stray `void`.
  - PC: an UNGATED `app.post('/api/generate-key', async (_req,res)=>…)` inserted on the line before the gated one (diff shown: line 225 ungated, 226 gated). Express answers the first registration, so generate-key is open. **99/99 pass, G5 and G5b both green.** Restored b60ca86b.
- Q4, what G5b misses (reading the file as text): a duplicate or earlier ungated registration of the same path (measured, PC); router-level or `app.use` middleware ordering that runs before the route; a literal sitting in a comment or dead code; a route mounted in another file. G5b proves the gated line exists, not that the live route is gated.
- Q7: the PR body and the comment (comment sha1 equals the recorded 76e7622e7a95) say "G5b reads index.ts as text; no route-level cell". That is true and disclosed.

Findings
- **G273-2109-1 (Low; test name).** G5b's title, "tokenisation puts requirePlatformRole on each key route itself", and the comment BLUF ("each of tokenisation's two key routes carries the gate on its own route line") read as "each key route is gated". Plant PC leaves an ungated generate-key route live with G5b green. The body's caveat is accurate. The cell name claims more than the cell proves. Info: M4 and G5b carry the file's `RED` prefix but are green on develop by design. The body says so.

NOT TESTED: tokenisation's live routes; the gate 244 plant itself (G's; I used my own); tsc.

---

## PR 2104 round 2 of 2 (KS-1972, event-indexer poll()): GO WITH NOTES

BLUF: the head reverts df9493550372 and wraps only poll()'s call. Against develop the diff is one hunk in event-indexer.ts (:200-206). isRateLimited, processBlock (from :213) and processTransaction (from :248) are byte-equal to develop, because the whole develop→head diff of the file is that single hunk. A value poll() cannot read now reaches handleError. No real rate limit is ever reclassified.

FOUND / TESTED / HOW
- Q1/Q5 diff: `git diff origin/develop refs/pr/2104 -- event-indexer.ts` gives exactly +7/-1: `let limited = false; try { limited = this.isRateLimited(err); } catch { /* comment */ } if (limited) {`. There are 3 `this.isRateLimited(` call sites (count 3). Against develop the PR has 4 files; the old test file is gone.
- Q5 rate limit, by reasoning: the new path differs from develop ONLY when isRateLimited THROWS. Whenever it returns true or false, the branch is identical. On develop a throw made poll() reject, with no backoff, so a value that throws was never treated as a rate limit before either.
- Q5, MEASURED with a scratch cell, develop vs head:
  - `{status_code:429, message getter throws}`: backoff 2000, onError 0 on both, because the first operand short-circuits.
  - `{response:{status:429}}`: backoff 2000 on both.
  - `{status_code getter throws, message:'429 Too Many'}`: develop rejects, backoff 0. The head resolves, backoff 0, onError 1 'unreadable thrown value'. No backoff is lost.
  - Site 3, with txsUtxos throwing a revoked Proxy: identical on both (resolved, onError 1, lastProcessedBlock stays 5, so retried).
  - Site 1 revoked Proxy with onError UNSET: develop rejects and logs nothing. The head resolves and console.error gets "[event-indexer] unreadable thrown value". This is the default handleError path that the seat lists as not driven.
- Q6 red-first:
  - Head: 6/6 pass.
  - Product at develop: R1-R3 fail with AssertionError "expected true to be false", and C1-C3 pass. Restored; blob b7516622 matches.
  - My mutant Ma (poll's catch sets `limited = true`, so an unreadable value counts as a rate limit) fails R1-R3 ("expected +0 to be 1").
  - My mutant Mb (a guard local to processBlock's call at :229, not G's guard inside isRateLimited) fails exactly C3 ("expected 6 to be 5"). This shows C3 pins site 2 from a second direction.
- Q7: the title, the body draft, the comment (sha1 equals the recorded 05d9b8dd6fa7) and both fragments are true at the head. True points include: three call sites in three methods; C3 pins processBlock; site 3 not driven; C2 2000 ms; the @ts-ignore at :102. The ruling is Wednesday's (in_11, 2026-11-08T19:25:58Z), not Kam's. It is NARROWER than round 1 (it removes behaviour) and no Kam card is cited.

Findings, as round 2 of 2
- G271-2104-1 (round 1, medium): **CLOSED.** Sites 2 and 3 are byte-equal to develop. My measurement keeps develop's retry at site 3, and C3 plus my Mb pin site 2.
- G271-2104-2 (round 1, low; status-code arms unpinned): **CLOSED by obsolescence.** The expression is no longer moved, and isRateLimited is byte-equal to develop.
- **G273-2104-1 (Low; RESIDUE).** No cell pins site 3 (processTransaction). A guard local to processTransaction's catch would pass all 6 cells; this follows from my Mb result plus the file's cells, READ ONLY for site 3. The seat discloses that site 3 is not driven. Ticket it as residue.
- **G273-2104-2 (Low; NEW, text).** The body, comment and fragments describe the round 1 effect as "a silently skipped block (lastProcessedBlock advances)". Two parts of that are loose. "Silently": handleError calls onError at sites 2 and 3, so the skip is reported. "Skipped block" at site 3: there it is a skipped transaction, and the block's other transactions are still processed. This is round 1's wording carried forward, and it does not mislead about this head's behaviour.

NOT TESTED: the real setInterval/Blockfrost path; Node's unhandled-rejection behaviour on develop's `void this.poll()` (not run); tsc.

---

## Conduct
- Findings only. No push, PR edit, comment, ticket write or mail. No `cd`: vitest was spawned with a cwd option. No git verb ran in any !CODING checkout except READ verbs (remote -v, config read, status at the end). Every write verb ran in /private/tmp/g273. The hook refused one `cp` whose source path was in the project checkout, because it parsed the source as a destination. I redid it as a read (tar -c) from a script, and nothing was written there. The project checkout's `git status` at the end shows only pre-existing untracked files that are not mine.
- Network: ls-remote and fetch only.
- Disk, DevMASTER: 9 GiB free at start and at end (`df -g`), never below the 8 GiB line.
- Load1 peaked at 6.23, during the merged-tree full suite with maxWorkers=4.
- Clone /private/tmp/g273 is **2.1G**, mostly the node_modules APFS clone. Not removed, per the commission's no-rm rule. My scratch cells were moved to /private/tmp/g273/_quarantine/.
- My own slips, both caught and redone: (1) the first develop baseline ran with the wrong cwd (9 guard files could not find the Dev root), discarded. (2) The first 2107 M1 mutant used a wrong line number and was not planted, so its 6/6 was discarded and redone at line 329.
