VERDICT: GO WITH NOTE at head 902b1ee093f9... (tier 2, round 1 of 2; landing tree 3f5b74d20fad5ec79e4055332b33646f3bb8938d on develop 89956fe92956a810f6821fdee09915f087feea7b; 0 blockers, 4 notes)

## BLUF

The PR is what it says: test-only plus one comment line. I measured every claim and found none false.

- **Heads:** #1650 = `902b1ee093f921bc4395b40dedb45a9ab6667eb4` and develop = `89956fe92956a810f6821fdee09915f087feea7b`, by `ls-remote` at the start (09:55 AEDT) and again at the end (10:00 AEDT). Neither moved. Because develop is the merge-base, the head is a fast-forward and the landing tree equals the head's own tree.
- **Q1:** the only non-test change is one comment line, and no product code changed.
- **Q2:** BI-M1 and BI-M5 each red the new cells by assertion. My own mutants confirm the cells read the verifier through the service's own decrypt path, and the one vacuity case I built reds them.
- **Q3:** BI-M4 reds H3 only. BI-M6 still reds H1. H3 fails closed on every reformat I tried.
- **Q4:** m365 suite 20 files / 201 cells at develop, 21 / 206 at the head, 0 vanished, 0 status changes.
- **Q5:** m365 `tsc --noEmit` rc 0, and the test files type-check in their own program rc 0.
- **Q6:** both residue points confirmed.

The four notes are below. None blocks the merge.

## Findings: blockers

None.

## Findings: notes

**NK1. "CSPRNG" is claimed in the V2 title and the file header, but the cells pin only the SHAPE.**
- My mutant **BK-X1** replaced `randomUrlToken()` with 32 bytes from `Math.random()`, base64url-encoded. That has the right length and alphabet and still differs per sign-in.
- It survives all 206 cells (206 passed, 0 failed, tsc rc 0).
- That is not a regression against the claim: the author's own table says V3 kills BI-M5 and the fixed-verifier case, and neither is this.
- A property that would kill it: spy on `crypto.randomBytes` and assert the stored verifier equals the bytes it returned.
- Impact is the same low rating BI1 gave PKCE here (confidential client). Suggest a one-line wording fix or a KS-ticketed follow-up. Not for this PR.

**NK2. Under a zero-rows mutation, V1 and V2 go red through a `TypeError`, not an assertion.**
- BK-X4 (`saveOAuthState` returns before the INSERT) leaves no row to read. V0 and V3 red by assertion (`'undefined' to be 'string'`).
- V1 reds on `s256(undefined)` (a Node `TypeError`) and V2 on `undefined.length`.
- The cells do not pass vacuously, which is the question that matters. The failing line is just a throw.
- Cosmetic.

**NK3. Residue (a) confirmed: m365-integration is outside preflight leg 16's corpus.**
- `scripts/preflight/preflight.sh:767` is `step "16/16 Test files are type-checked against the shrinking baseline (KS-1000 / KS-1487)"`.
- `:775` delegates to `bash scripts/preflight/test-types-ratchet.sh`.
- `test-types-ratchet.sh:47` is the default corpus: `set -- services/auth services/api-gateway services/vc-issuer`. Line 38's usage text repeats it.
- **Control:** `grep -c m365` returns 0 for both `test-types-ratchet.sh` and `typecheck-tests/check.cjs`, and `grep -c auth` returns 5 on the same script, so the grep can see the file.
- I also measured the type-check of m365's test files myself: 21 test files listed (including both PR files), 0 diagnostics. That agrees with the author's "0 errors, so an empty baseline would do".
- Routing this to KS-1554 is Wednesday's call, not the gate's.

**NK4. A leftover file in my scratch clone only.**
- I created `Blockchain/Dev/services/m365-integration/tsconfig.bk1.json` (extends the service config with an empty `exclude` for tests) in my own clone. It is not in the PR and is not under `!CODING`. The brief bars `rm`, so I left it.

## Findings: confirmations (what each question showed)

**Q1: test-only, measured**
- The three-dot diff (`develop...pr1650`) has exactly 3 files, 274 insertions / 1 deletion:
  - `packages/shared/src/crypto/encryptedField.ts` (M, 1/1)
  - `m365-integration/src/__tests__/ks1677-the-pkce-verifier-is-secret-and-random.test.ts` (A, 207/0)
  - `m365-integration/src/__tests__/ks1677-the-sign-in-returns-to-the-host-that-set-its-cookie.test.ts` (M, 66/0)
- The comment at `encryptedField.ts:61`: before `tokenCrypto.ts:24` `tokenAad`, after `tokenCrypto.ts:28` `tokenAad`.
- **Byte check:** develop's file with `tokenCrypto.ts:24` replaced by `tokenCrypto.ts:28` by `sed` is sha256 `3c8a39393357…53fc`. The head's file is the same hash. So that line is the entire change to the file, and it sits inside a `/** */` comment.
- **`tokenAad` at `:28`:** at develop, `m365-integration/src/security/tokenCrypto.ts` has `export const tokenAad = …` on line 28 (lines 20-34 printed). **Control:** `export type TokenColumn` is on line 24, so the old cite pointed at the type, not `tokenAad`.
- The second test file has 0 deleted lines, so H1 and H2 are unchanged. The new cell H3 and a header comment are the only additions.
- No product file changed, so no test helper can be imported by product code. Tier 2 stands; no escalation.

**Q2: NB1 cells bite.** Run at the head against the full m365 suite, tsc rc 0 before each mutant, byte-identical restore asserted by sha256 after each. No file failed to load.

| mutant | tsc | result | red cells |
|---|---|---|---|
| none (head) | 0 | 206 / 206 | none |
| BI-M1 `codeVerifier = state` | 0 | 204 / 2 failed | V1 (`['authUrl.param.state']` to equal `[]`), V2 (`not.toBe`) |
| BI-M5 `sha256Hex(connectionId)` | 0 | 204 / 2 failed | V2 (`[64,false]` to equal `[43,true]`), V3 (equal verifiers) |
| BK-X2 (mine) `codeVerifier = binding` | 0 | 203 / 3 failed | V1 (`['cookie.value']`), V2, and the existing R18 |
| BK-X3 (mine) verifier stored in plaintext | 0 | 204 / 2 failed | V0 (`storedVerifier not.toBe verifier`), and the existing R14 |
| BK-X4 (mine) no INSERT, zero rows | 0 | 194 / 12 failed | V0, V3 by assertion; V1, V2 by TypeError (NK2); plus R4, R11, R14, R19, C1-C3, R15 |
| BK-X1 (mine) `Math.random` bytes | 0 | 206 / 0 failed | none (survives, NK1) |

- BI-M1 and BI-M5 match the author's table exactly (V1+V2 and V2+V3).
- The `tsc` for BK-X3 first returned rc 2 (an unused import under `noUnusedLocals`). I corrected the mutant with `(void encryptToken, rec.codeVerifier)`, re-ran, and reported only the rc 0 run.
- **Read path:** `signIn()` takes the stored value from the INSERT's parameter and decrypts it with the service's own `decryptToken(…, 'code_verifier', connectionId)` from `../security/tokenCrypto`. The keyring is the real `PII_ENCRYPTION_KEY`. This is the product storage path, not a test accessor.
- **Vacuity:** zero rows is BK-X4 above. V0 and V3 fail by assertion, V1 and V2 by throw, so nothing passes vacuously. V3's own control (both connection ids equal to `conn_<fixed>`) took, since it passes at the head.
- BK-X2, BK-X3 and BK-X4 are mutants the author did not run. BK-X1 is the only one that survives.

**Q3: NB2 polarity.** Same restore discipline, run on the `ks1677-the-sign-in-returns…` file only.

| mutant | H1 | H2 | H3 |
|---|---|---|---|
| BI-M4 `!empty(apiPublicUrl)` | pass | pass | RED `expected [ 'empty(apiPublicUrl)', true ] to deeply equal […, false ]` |
| BI-M6 redirect and FRONTEND_URL to `-api.` (control) | RED (`to contain '-admin.'`) | not run | RED |
| BK-B1 (mine) arms swapped | pass | pass | RED |
| BK-B2 (mine) ternary split across lines | RED | pass | RED (`expected null not to be null`) |
| BK-B3 (mine) predicate `empty(containerAppsEnvDomain)` | pass | pass | RED |
| BK-B4 (mine) closing `}` on the next line | pass | pass | RED (`expected null not to be null`) |

- **Real line:** `deployment/azure/services.bicep:1625` is `{ name: 'ENTRA_REDIRECT_URI', value: empty(apiPublicUrl) ? '' : 'https://${resourcePrefix}-admin.${containerAppsEnvDomain}/api/m365/callback' }`. It is a single line, and H3's regex (`value: (!?) pred ? '…' : '…' }`) matches it.
- **Uniqueness:** `ENTRA_REDIRECT_URI` appears once in the file, and `value: empty(apiPublicUrl) ?` appears once (grep returned line 1625 only). So the first-occurrence `indexOf` and the mutation `.replace` in H3's control cannot land on another line.
- **Fails closed:** a reformatted line makes the parser return `null`, and `expect(t).not.toBeNull()` reds (B2, B4).
- **H1 and H2 untouched:** zero deleted lines in the diff of that file, so they are byte-identical to develop. BI-M6 still reds H1.
- BI-M6 also reds H3. The brief's "still reds H1" holds, and the author's table already lists H1 and H3.

**Q4: no weakening.**
- A vitest JSON report of the full suite at develop and at the head. Cells compared by file plus full name.
- Develop: 20 files / 201 passed / 0 failed. Head: 21 files / 206 passed / 0 failed / 0 pending.
- Vanished: none (empty set). New: 5 (V0-V3 and H3). Status changes among develop's cells: none.

**Q5: landing.**
- `git merge-tree --write-tree develop pr1650` = `3f5b74d20fad5ec79e4055332b33646f3bb8938d`, rc 0. That equals `pr1650^{tree}`, since develop is the merge-base. I did the merge-tree after refetching develop; it was still `89956fe92956`.
- m365 `tsc --noEmit -p services/m365-integration` at the head: rc 0.
- Test files in their own program: `tsconfig.bk1.json` (extends the service config, `exclude` without `src/__tests__`). `--listFilesOnly` lists 21 m365 test files (control that the override took; 2 of them are the PR's). `tsc --noEmit` rc 0, 0 `error TS` lines.
- **Control:** I appended `const __plant: number = 'x';` to the new test file. The same program gave rc 2 (TS2322 and TS6133). The file was restored byte-identical (sha matched the saved copy).

**Q6: the author's two residue points.**
- (a) Confirmed. See NK3.
- (b) `packages/shared`: `vitest run` at the head, cwd `packages/shared`: 52 files / 994 tests / 994 passed / 0 failed / 0 pending, rc 0. The head differs from develop only in one comment in that package, so this stands for develop. I did NOT open `BACKLOG.md:1236` (see NOT RUN).

## FOUND / TESTED / HOW

- **Clone:** `git clone --shared` of the spark cache into `scratchpad/gate_bk1/src`. The cache did not hold the PR head, so I added GitHub as a remote `gh` and fetched `refs/pull/1650/head` and `develop` into my clone. I reused the checkout's own `core.sshCommand` (the deploy key) for the read-only fetch, the way `spark/round.sh` does. That is a fetch, not a write to GitHub. Heads checked by `ls-remote` at 09:55 and 10:00 AEDT.
- **Install and build:** `npm ci --ignore-scripts` in `Blockchain/Dev` (1937 packages, rc 0). `packages/shared` built, rc 0. Every npm, tsc and vitest call ran through `scripts/inrepo.py`, which asserts the subprocess cwd is inside my clone. No `npx`, no `cd`, no Docker.
- **Suites:** the full m365 suite at develop (clone checked out at develop) and at the head (checked out at the PR), each with `--reporter=json`. Cells compared programmatically.
- **Mutants:** `scripts/mutants.py` (source mutants, one at a time, exact-count replacement asserted, tsc first, sha256 restore asserted) and `scripts/bicep_mut.py` (the same for `services.bicep`). Outputs are in `out/` beside them in the scratch folder.
- **Scratch folder:** `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/2a56ac36-e9ca-49f4-8d2d-f02d4a53f9ed/scratchpad/gate_bk1/`.

## NOT RUN

- **Docker and the four platform suites (Schemathesis, Akto, Playwright, k6):** barred by the brief and, for the platform suites, they need a stack.
- **Bicep compile:** no Bicep CLI. H3 reads source, as the author says. I did not compile either the template or any mutation of it.
- **Preflight as a whole:** I read leg 16 and ran nothing from it.
- **Real OAuth, Microsoft or Graph:** nothing.
- **`BACKLOG.md:1236` staleness:** my attempt to read it was interrupted by a hook, and I did not retry. I confirmed only that the `packages/shared` suite is green. Whether that BACKLOG line is stale is not measured here.
- **Other services' suites** (auth, api-gateway and the rest): not run. Not needed for a diff that touches only m365 tests and one shared comment.
- **Landing-tree run:** the head IS the landing tree (fast-forward onto an unmoved develop), so I did not run a second copy of the same tree.
- **The CI result of #1650:** I did not read GitHub checks.

## Wall-clock

09:54 AEDT start to 10:01 AEDT verdict, about 7 minutes.

sha256 of the file without its first and last line (method: sed '1d;$d' verdict.md | shasum -a 256): 45b3cd2ba6cc9ec9be86fc465d919d64656472439a25ccbd9457b39ea32c6484
