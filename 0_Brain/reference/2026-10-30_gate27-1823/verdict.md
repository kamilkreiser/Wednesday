## QA GATE - TIER 1, round 1: GO WITH NOTES

**PR:** Secuura/Distributed_Secuura #1823, "Refs KS-1798, KS-1799: a GDPR write route answers 500 when a thrown value cannot be read" (Seat S 8th)
**Head:** `3952a58525392271ea0b539c102394709d8c15d5`. ls-remote of refs/pull/1823/head showed this SHA at the start (2026-10-30T00:03:12Z) and again at the end (2026-10-30T00:14:42Z). It matches the author's claim.
**Develop:** `530f091120d5da749edf972e8e0089e44cfc5589` at both reads. The merge-base with the head is `a786e06e6f6e` (as the author said). There is 1 commit, with no merge-in.
**Gate:** QA gate 27, tier 1 (Wednesday raised it from tier 2 because this is a GDPR write route). I report findings only. I fixed nothing, commented nowhere, pushed nothing, merged nothing and deployed nothing.

### The GDPR question, answered

**No.** The new try/catch cannot turn a failed write into a reported success, or a successful write into a reported failure. For every ordinary pg error (unique, FK, not-null, CHECK, too-long, in bare-pg, tagged and Prisma shapes) the status code and the body are byte-for-byte the same as develop. The service is called exactly once on every path. The only behaviour that changes is for a thrown value whose `pgCode` read throws: it used to get **no response at all** (the request hung), and it now gets a non-2xx answer (500, or the 404/400 its readable `code` maps to).

Why:
- `mapGdprWriteDbError` has exactly two callers, POST `/consent` (gdpr.ts:271) and POST `/dsr` (gdpr.ts:353). Each calls it only inside the `catch` of a `try` whose success path (`res.status(201).json({success:true,…})`) is earlier in the try. So the function can only run after `gdpr.recordConsent` or `gdpr.createDSR` has rejected, or after the 201 write itself threw. That ordering did not change.
- After mapping, the route does no further writes. It either returns a 404/400 that the mapper sent itself, or falls into `fail500`.
- The function can still emit only 404 NOT_FOUND, 400 VALIDATION_ERROR, or `false` (meaning 500). The PR adds no new status and no `success:true`.
- When the `pgCode` read does not throw, `ownPgCode` is the same value the old expression read, and `?? extractPgCode(err)` is unchanged. `extractPgCode` is itself total (pgErrors.ts:55-59, KS-1780), so the new code path cannot throw.
- The `pgCode` getter is read **exactly once** at head, as it was at base (cell "counting getter"), so a getter's side effects are unchanged.
- No erasure route calls the mapper. POST `/erasures` uses `sendConnectorRefusal`, and POST `/erasure/:userId` uses `fail500`. Neither is touched by the diff, which is one hunk in gdpr.ts at lines 138-146.
- A half-applied write inside the service (for example a recordConsent that wrote and then threw) is service-internal. It is unchanged by this PR and not covered by these mocks; see NOT TESTED.

**COUNTS**
- **Diff:** 5 files, +111 / -1. Exactly the declared 5. I checked with `git diff --numstat` against the merge-base a786e06e and three-dot against develop 530f0911, and both gave the same set.
  - `gdpr.ts`: +8 / -1, ONE hunk. It is one try/catch around the `pgCode` read, plus the KS-1798 comment line.
  - `pgErrors.ts`: **0 changed bytes**. The diff is 0 bytes, the blob is `31ec74b4…` at the merge-base and at head, and the sha256 is `71b4fb0aebe04658…` (equal to the Spark note).
  - Test files: ks445 +50 / -0 and ks1780 +11 / -0.
  - Docs: the flow doc +22 and the cheat sheet +20.
- **Canonical Spark bytes:** I compared the PR's `+`/`-` lines with the canonical `patch.diff` of each Spark run (`cmp`). The result is **EQUAL** for gdpr.ts (9 lines), ks445 (50) and ks1780 (11). The Spark tip `7152ac669d2d` and the PR's merge-base `a786e06e6f6e` have identical blobs for gdpr.ts, ks445, ks1780 and pgErrors.ts, so the patch landed on the same pre-image.
- **spark_gate.sh** (run FIRST), run 2:
  - The diff was 5 / +111 / -1, and the head was asserted as the tip.
  - Targeted HEAD: **29 passed / 0 failed** (ks445 20/20, ks1780 9/9).
  - BASE product code: **26 passed / 3 failed**. The reds are exactly KS-1798 D1, D2 and D3, each `Expected: 500, Received: "NO ANSWER"`, after `TypeError: Cannot perform 'get' on a proxy that has been revoked` at gdpr.ts:139. ks1780 is 9/9 on base product code, as expected for a test-only pin.
  - Run 1 was an instrument error; see I1.
- **Red-first, KS-1799 B5:**
  - Untouched helper at head: 9/9. The ks1780 file at the merge-base (without B5): 8/8.
  - I applied the tamper at pgErrors.ts:57 in my head worktree, checking first that line 57 was exactly `  } catch {`. The result was **1 failed / 8 passed**, and the only red is `RED KS-1799 B5 …`.
  - I restored by content (a byte copy). The sha256 is `71b4fb0aebe04658b24482bd94b71116d59989b83eaa6ac964dc976e04d65f39` before and after, which is **equal**. A re-run gave 9/9.
  - B5 is a pin, as the author declared.
- **Whole originate jest** (node v26.8.1, jest 29, packages/shared built with `npx tsc` in each of my worktrees):
  - HEAD: **151 suites, 1855/1855, 0 failed**.
  - develop 530f0911: **152 suites, 1854/1854, 0 failed**.
  - The difference is consistent: head = a786e06e's 1849 + 6 cells; develop = 1849 + #1822's 1 suite / 5 cells. This matches the author's 1849 to 1855.
  - No red on either side.
- **Attack cells** (`g27-attack.test.ts`, 46 cells, both routes; table in `attack_table.txt`):
  - HEAD: **46/46**.
  - BASE a786e06e: 34/46.
  - DEVELOP 530f0911: 34/46, and develop's table is identical to base's on all 46 rows.
  - Exactly **12 rows change** from base to head (6 per route), and every one of them changes from `NO ANSWER` to a non-2xx with `success:false`:

  | Planted thrown value | BASE / develop | HEAD |
  |---|---|---|
  | Proxy whose get/getPrototypeOf/ownKeys traps all throw | NO ANSWER | 500 INTERNAL_ERROR |
  | revoked Proxy | NO ANSWER | 500 INTERNAL_ERROR |
  | Error with a throwing `pgCode` getter | NO ANSWER | 500 INTERNAL_ERROR |
  | throwing `pgCode` getter + `code: '23503'` | NO ANSWER | 404 NOT_FOUND |
  | throwing `pgCode` getter + `code: '23505'` | NO ANSWER | 500 INTERNAL_ERROR |
  | Proxy that throws only on `pgCode`, `code: '22001'` | NO ANSWER | 400 VALIDATION_ERROR |

  - **Unchanged rows** (both routes, the same status / code / success / call count at base, head and develop):
    - success resolve: 201, `success:true`;
    - plain Error: 500;
    - thrown null, thrown undefined and thrown string: 500;
    - bare pg 23505 unique: 500; bare pg 23503 FK: 404; bare pg 23502 not-null: 500;
    - tagged 23505: 500; 23503: 404; 23502: 500; 22001: 400; 23514: 400;
    - Prisma 23503: 404; Prisma 23505: 500;
    - a tagged pgCode outranks `code`: 500;
    - counting getter: 404, read once.
  - The service mock was called exactly once in every row: no retry and no skip.
- **My mutants of the new catch** (`mutants.py`, head worktree, restored by content, sha256 `032103df…` equal):

  | Mutant | PR ks445 (20) | g27 attack (46) |
  |---|---|---|
  | M1 catch rethrows (= the old behaviour) | **killed** (3 red: D1-D3) | killed (12) |
  | M2 catch answers 200 `success:true` | **killed** (3) | killed (12) |
  | M3 catch maps to 23503, giving 404 | **killed** (3) | killed (10) |
  | M5 catch maps to 22001, giving 400 | **killed** (3) | killed (10) |
  | M4 catch `return false` (skips the extractPgCode fallback) | **SURVIVES** (20/20) | killed (4: "getter throws + code 23503", "Proxy throws only on pgCode, code 22001", both routes) |
  | M6 drop `?? extractPgCode(err)` | killed by compile only (TS6133, unused import) | killed by compile only |

- **Merge-tree of the head onto develop 530f0911:** CONFLICT, tree `95823e7e68e380113eaaf8c761f63b785af025e6`, in **only** the two Projects Documents files.
  - Flow doc: markers at lines 5854-5889.
  - Cheat sheet: markers at lines 5937-5969.
  - **`Blockchain/` merges clean.** Under Blockchain/, the merged tree differs from the head only by develop's 2 files (certifications.ts and the #1822 test), and differs from develop only by this PR's 3 files.
  - Section `122.` is still valid: develop's highest is `121.`.

---

### Findings, ranked (none blocks the merge)

**F1 (Low, test strength). The PR's cells do not pin the `?? extractPgCode(err)` fallback after a throwing read.**
- Mutant M4 replaces the catch with `return false`, which skips `extractPgCode` and answers 500. It passes all 20 ks445 cells.
- In behaviour, M4 differs from the head only for a value whose `pgCode` read throws but whose `code` / `meta.code` / message is readable. That value gets 500 under M4, against the head's honest 404/400.
- Two of my cells kill M4 ("getter throws + code 23503", giving 404; "Proxy throws only on pgCode, code 22001", giving 400).
- This is not a safety gap: M4 is still a non-2xx and fails closed. If wanted, a D6-style cell would pin it.

**F2 (Info). A hostile value carrying a readable FK `code` now answers 404 "User not found".**
- At head, a thrown value with a throwing `pgCode` getter and a readable `code: '23503'` is answered 404 NOT_FOUND. At base it got no answer.
- This is the same answer an ordinary bare-pg 23503 gets on develop, so it is consistent with the existing mapping, not a new semantic. It is still a failure status with `success:false`, never a reported success.

**F3 (Info, out of scope, author-disclosed, confirmed). A sibling direct read remains.**
- `routes/certifications.ts:1073` (on develop) reads `(error as {code?})?.code ?? …meta?.code` directly in the catch of GET `/certifications/:id`.
- A hostile value would escape that catch the same way. It is a read route, not a GDPR write.
- The author disclosed it and asked before filing. I did not measure it.

**F4 (Info, merge-prep). Both docs conflict, and both conflicts are append-at-the-same-point.**
- Flow doc: develop's section 121 against this PR's section 122.
- Cheat sheet: develop's KS-1666 entry against this PR's KS-1798/1799 entries.
- Resolution: keep both in each file. No code path conflicts.

---

### FIX-BEFORE-MERGE
(none)

Optional follow-ups:
- F1: a cell that plants a throwing `pgCode` getter plus a readable `code: '23503'` and expects 404.
- F3: file the certifications.ts direct read, at Wednesday's call.
- F4: resolve both doc conflicts at merge-prep.

---

### TESTED / NOT TESTED / HOW

**TESTED**
- Diff scope, and byte-equality with both canonical Spark patches.
- spark_gate (red-first at BASE product code, green at HEAD).
- The B5 tamper with a sha256-equal restore.
- The whole originate jest suite at head and at develop.
- 46 attack cells at base, head and develop.
- 6 mutants of the new code, run against the PR's file and my file.
- A read of every route in gdpr.ts that reaches `mapGdprWriteDbError`, and of both erasure routes.
- The merge-tree onto develop.

**NOT TESTED**
- **A real Postgres.** Every error was a planted mock rejection of `gdprService`. I did not run integration suites (`jest.integration.config.js`) or a live stack.
- **Service-internal partial writes** (gdprService.recordConsent / createDSR writing and then throwing). That code is outside the diff and unchanged.
- **The certifications.ts sibling** (F3).
- **Other checks:** tsc and eslint beyond what ts-jest compiled, the 4 platform suites, Node 24, html_docs_check and a render of the docs, audit:gate / audit:locks, and the author's hook legs 3, 4 and 8.

**HOW**
- **The clone:** `git clone --shared` of the Secuura checkout into the then-non-existent path `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/e5f54089-c0c9-4cb7-8aa3-cf2e956a3e73/scratchpad/gate27/clone`.
  - Its `rev-parse --show-toplevel` was asserted equal to that path before any fetch or write.
  - Its origin was set to `git@github.com:Secuura/Distributed_Secuura.git`.
  - `core.sshCommand` was read from the checkout with `git config --get` and set in the clone's own config.
  - No git verb wrote to the checkout.
- **Worktrees:** three, in my clone (`wt_head`, `wt_base`, `wt_dev`), made by `mkwt.sh`.
  - `Blockchain/Dev/node_modules` is a real directory of symlinks to the checkout's entries. `@secuura/*` is a real directory with the workspace's relative links, so it resolves to **my worktree's** packages.
  - originate and shared `node_modules` are symlinks to the checkout's.
  - `packages/shared` was built with `npx tsc` in each worktree (rc 0, 29 dist entries).
  - TMPDIR was `/tmp/g27`.
- **Cleanup:** my attack file was copied in for its runs and removed before the whole-suite runs. Final `git status` in each worktree shows only the 2 node_modules symlinks.
- **Processes:** none left running. Each jest ran in the foreground or as my own background job and exited. I killed nothing.
- **Artefacts in this folder:**
  - `g27-attack.test.ts`, `attack_table.txt` and `attack_{base,head,dev}.json`;
  - `mutants.py` and `mutants_result.json`;
  - `mkwt.sh`;
  - `spark_facts.json` (run 2) and `spark_facts_run1_jest_not_found.json` (run 1).

### Instrument errors / caveats of my own
- **I1. spark_gate.sh run 1 measured nothing.**
  - I passed `--node-modules <checkout>/Blockchain/Dev/services/originate/node_modules`, which holds only 9 packages and no jest.
  - Every targeted run gave `rc 127, sh: jest: command not found`, and the harness still exited **rc 0**, reporting `files_failed: 2, passed: 0, failed: 0`.
  - The harness reports an unrunnable runner as a 0/0 with rc 0, not as a refusal. That is a harness weakness; I did not edit the tool.
  - Run 2, with `--node-modules <checkout>/Blockchain/Dev/node_modules` (the hoisted root), measured correctly (29 / 26+3).
  - The deploy-key fetch worked on both runs, because `core.sshCommand` was set in the clone's config. There was no gate-26-style fetch error.
- **I2. Several calls were refused by hooks and re-issued.** A `======` separator, a `cd`, and an unquoted `set -- $p` were refused. A zsh `$T:P` modifier also mangled one `git show` path; it was re-issued as a literal SHA. None of these ran against the checkout.
- **I3. My base and head jest runs used the checkout's hoisted node_modules** (via symlinks), not a fresh `npm ci`. The versions are whatever the checkout has installed. The author used a fresh npm ci at the vite 6.4.5 locks.
