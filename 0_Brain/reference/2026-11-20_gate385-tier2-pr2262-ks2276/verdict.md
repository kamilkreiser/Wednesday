PR 2262: GO WITH NOTES (at head b79fc89dd880ca9243c6076f261aaef23ab7a11f; tier 2)

# Gate 385, tier 2 (Opus), PR 2262 (KS-2276), 2026-11-20 ~06:16 AEDT

## Pins
I pinned with gh api twice: at 06:08, before the first measurement, and at 06:15:52, just before writing this verdict.
- Head: b79fc89dd880. The PR is open, not merged and not draft. updated_at is 2026-11-19T19:00:26Z. 1 commit, 3 files, +55 -0, mergeable true.
- The head's only parent is 2ad55ceceb7c.
- Develop was edfb8b230e4f both times. The API's base.sha is also edfb8b230e4f.
- `git diff --stat 2ad55ceceb7c b79fc89dd880` shows exactly the three paths: +22, +19 and +14.
- `routes/presentations.ts` has the same blob, 36167e74631d, at 2ad55ceceb7c, the head and develop. Its sha256 is 8fe8b6500b61 in all three of my trees.
- Develop moved 2ad55ceceb7c..edfb8b230e4f: 3 commits (9641bf571, e92365022, edfb8b230), 5 files, +133 -6.
  - A diff limited to `services/vc-issuer`, `packages`, `Projects Documents`, `package.json` and `package-lock.json` gives empty output.
  - Control: the same diff limited to `Blockchain/Dev/services` shows 3 files.
- Closing keywords on KS-2276: 0 in the PR body and 0 in the commit message. Control: the string "Closes KS-2276" gives 1.

## How I measured
- I made my own `git clone --shared --no-checkout` at `_work/g`, from s-w43-base's .git.
  - s-w44-base's .git failed: "alternate object stores, nesting too deep". Nothing was created by that attempt.
- edfb8b230e4f was in no local repo, so I fetched develop and refs/pull/2262/head INTO MY CLONE ONLY, over https, with the gh credential helper. That is read-only on GitHub.
- Three worktrees, all in my clone:
  - `_work/h`: the PR head.
  - `_work/d`: develop edfb8b230e4f.
  - `_work/m`: MERGED state, a no-ff merge of the PR onto edfb8b230e4f. It merged cleanly. `diff --stat develop..m` shows exactly the PR's 3 files, +55.
- node_modules were APFS-cloned (`cp -c`) from s-w44-ks2276, which I only read. I copied the root tree, packages/shared, services/vc-issuer and services/shared.
  - The absolute self-link `node_modules/node_modules` pointed into s-w44-ks2276. I moved it to `_work/_quarantine/{h,d,m}/nm_selflink`.
  - Absolute links left under node_modules: 0 in each tree. Control: 112 relative links remain in h.
- I quarantined the copied packages/shared/dist and rebuilt it myself (`tsc`, rc 0) in every tree.
- Run conditions: Node v26.8.1, vitest 4.1.12, TMPDIR /private/tmp/g385t. load1 was between 2.4 and 6.1 throughout.
- Scripts: `_work/mutants_g385.py` and `_work/eslint_g385.mjs`.
- Evidence: `_work/evidence/` (`mut_{d,h,m}.json`, `vt_*`, `suite_*`, `diff_m_M{1,2}.out`, `probe_domain.json`, `ks444_m_*`, `linear_ks2276.json`, `pr_body.md`).
- After every mutant I restored the route file from saved bytes and re-checked its sha256: 8fe8b6500b61 after every run.
- All three worktrees show 0 porcelain lines at the end. All planted files are in `_work/_quarantine/m/`.

## Q1. The gap and its closure: CONFIRMED, reproduced myself on develop, the head and the merged state
I mutated one line, `domainValid: ...`, in routes/presentations.ts. I ran the ks625 file alone and recorded the cells that failed.

| mutant | d: old file, 7 cells | h: PR head, 9 cells | m: merged, 9 cells |
|---|---|---|---|
| BASE | 7/7 | 9/9 | 9/9 |
| M1 `domainValid: true` | 7/7, survives | P8 fails | P8 fails |
| M2 `proof?.domain === domain` (the `!domain \|\|` half dropped) | 7/7, survives | P9 fails | P9 fails |
| M6 `!domain \|\| !!proof?.domain` | 7/7, survives | P8 fails | P8 fails |
| M7 `!domain \|\| proof?.challenge === challenge` | 7/7, survives | P8 fails | P8 fails |
| M8 `!==` | P1 fails | P1 and P8 fail | P1 and P8 fail |

- Each cell fails for the stated reason. Verbose diffs on m:
  - M1: `- "domainValid": false / + "domainValid": true` in P8.
  - M2: `- "domainValid": true / + "domainValid": false` in P9.
- The WHOLE vc-issuer suite on develop edfb8b230e4f reads 891/891 in 31 files under M1, and 891/891 under M2. This is the G287-1 gap, as the ticket states.

## Q2. Are the cells honest, and which mutants do they still miss? HONEST, with one LOW (F1)
- The diff is pure addition after line 149: +22 -0. All seven older cells are byte-identical, and none is weakened.
- P8 pins status, verified and the whole `checks` object. Only domainValid differs from P1's object.
- P9 sends no domain to a presentation that carries `proof.domain`. It pins `!domain` short-circuiting to true.
- Both cell names match what the cells assert.
- Q9 (`challengeValid: true`) is still killed by P6. P8 does not add to that, as expected.

Mutants of my own. All of them survive on 9/9 at h and on 9/9 at m:
- Q1 casefold
- Q2 trim
- Q3 prefix either way
- Q4 suffix/subdomain (`domain.endsWith(proof.domain)`)
- Q5 a proof that names NO domain passes (`proof?.domain === undefined ||`)
- Q6 no proof passes (`!proof ||`)
- Q7 an empty string compared instead of treated as unsent

Q8 (`domainValid: !domain`) is killed by P1.

A runtime probe on m (`probe_domain.json`, not a cell) shows the code is correct today:

| input | domainValid |
|---|---|
| CAPS | false |
| trailing space | false |
| `evil.ks625.example` | false |
| `ks625.example.evil` | false |
| `''` | true (read as unsent) |
| proof without a domain, verifier sends DOMAIN | false |
| no proof, verifier sends DOMAIN | false |
| `domain: null` | 400 |

So every survivor is a TEST gap, not a defect.

## Q3. Merged state: CLEAN
- **Whole vc-issuer suite:**
  - develop edfb8b230e4f: 891/891 in 31 files.
  - merged: 893/893 in 31 files.
  - Failure-name sets are equal, both empty.
  - Positive control: the same JSON-reporter pipeline counted the mutant failures above.
- **tsc** (`tsconfig.json`, noEmit), merged: rc 0, 0 errors. Planted `src/g385-planted.ts`: rc 2, TS2322 naming the file.
- **Test-types ratchet** (`check.cjs services/vc-issuer`), merged: rc 0. "examined 45 files, 31 of them under __tests__; 0 errors: 0 in the baseline, 0 new; 0 stale". Planted test: rc 1, 46/32 examined, 1 new error naming the file.
- **eslint** on the test file, through the ESLint API with cwd Blockchain/Dev: 0 errors, 0 warnings. Planted file: rc 1, with no-debugger (error) and @typescript-eslint/no-unused-vars (warn).
  - My first CLI call with `-c` and cwd outside Dev gave "Parsing error: Unexpected token Reply". That was MY invocation: the config's file globs are cwd-relative. It is not a finding.
- **docs-fragments check** (`--root m`): OK. "flow 117 legacy + 300 new, cheat 112 legacy + 300 new; lint clean, render passes html_docs_check". The two ADVISORY page-lag lines are pre-existing. A planted two-heading cheat fragment fails: rc 1, "must hold exactly one entry (one <h2>)".
- **The two new fragments:** each holds a single `<h2>`. The flow fragment uses the `<!--n-->` token. Both pass the checker, and I read them.

## Q4. PR body, Test Evidence and the KS-2276 facts comment 35744c27: TRUE (one cosmetic INFO)
- I read the PR body (gh api, 7,970 bytes) and the comment (Linear GraphQL, read-only, 2,907 chars).
- KS-2276 is In Progress. Its only attachment is PR 2262, and it has exactly one comment.
- Every figure I could re-measure holds:
  - 7 cells, then 9.
  - The mutant table, cell by cell.
  - 891 and 893 in 31 files.
  - tsc, eslint and the ratchet at 0, with planted controls that fired.
  - docs-fragments 299 then 300.
  - route sha256 8fe8b6500b6192bc.
  - Three paths, +55 -0.
  - "presentations.ts not touched".
  - The develop-movement paragraph: 3 commits, 5 files, none under vc-issuer.
  - The probe line on caps, trailing space and the empty string.
  - "no closing keyword".
- The suite figures were measured on 2ad55ceceb7c and I measured them on edfb8b230e4f. They are the same.
- Not re-measured by me (builder-only, and honestly labelled as such): the push-hook timings, the 13/16 legs and the refused first attempt.
- **Node v26.8.1 against LTS 24:** it does not materially matter here.
  - The cells use only Express routers dispatched in-process, zod and `crypto.generateKeyPairSync('ed25519')`, all stable long before Node 24.
  - Blockchain/Dev `engines` is `node >=18.0.0`.
  - Node 24 is not installed on this machine (homebrew lists node and node@26 only), so it is UNMEASURED on 24 by me too. The PR body discloses this correctly.
- INFO: the PR body's "NOT run" list has a doubled bullet, `- - Pre-push legs 3, 4 and 8`. Cosmetic.

## Q5. Report-only: the ks444 OBJECT-proof cell guards only its 200-not-400 boundary. CONFIRMED
- `ks444.requestSchema.test.ts` lines 180-193 assert status 200, `verified` false and `presentationProofValid` false.
  - Since KS-625, `presentationProofValid` is the constant `false`, and `verified = allCredentialsValid && false`. So two of those three assertions hold for any input.
  - The cell sends challenge `expected` against proof challenge `other`, but never asserts `challengeValid`.
- Measured on m:
  - Under `challengeValid: true`, the ks444 file stays 24/24.
  - Under a schema mutant that refuses an object proof (`proof: z.undefined()`), the cell fails, with 2 others: 21/24.
- So only the status boundary is guarded. This is not a finding against this PR.

## Findings
- **G385-2262-1 (LOW, test coverage; not merge-blocking).** Several weakenings of the domain comparison are neither pinned nor named by the PR, and they are the ones that matter for replay protection.
  - The unpinned weakenings:
    - a prefix match;
    - a suffix or subdomain match;
    - a proof that names NO domain being accepted (Q5);
    - an absent proof being accepted (Q6).
  - All of them leave the 9 cells green at the head and on the merged state.
  - The flow fragment and the PR body say "Matching is exact (measured, not pinned by a cell)" only for capitals, a trailing space and the empty string.
  - P8 uses a domain that shares no prefix or suffix with DOMAIN, and every P-cell presentation carries `proof.domain`. So "a mismatched domain is pinned" holds for a fully different domain only.
  - No runtime exposure today: domainValid is report-only, because `verified` is constant false under KS-625. It becomes load-bearing when KS-625 option 1 (the real holder-signature check) lands.
  - Suggested follow-up, Wednesday's call: two cells.
    - P10: a presentation created without a domain, verified with DOMAIN, gives domainValid false.
    - P11: `'evil.' + DOMAIN` gives false.
- **G385-2262-2 (INFO, security-shaped design note; NOT introduced by this PR).**
  - P9 pins the existing fail-open REPORTING semantic: "verifier sent no domain" reads `domainValid: true`, although nothing was compared. The empty string `''` reads the same way.
  - This is the current behaviour, documented in the KS-625 header, and this PR changes no product code. So I do not route the PR to a tier-1 gate on it.
  - When KS-625 option 1 makes `verified` depend on the checks, its gate must decide whether an omitted domain may pass. Then P9 is the cell that would have to change.
- **G385-2262-3 (INFO, cosmetic).** The doubled bullet `- - Pre-push legs 3, 4 and 8` in the PR body's NOT-run list.

## Not run / not measured
- Node 24 (not installed).
- The pre-push hook and its 16 legs; the four platform suites; any booted stack, container, database or box.
- Other services' suites and ratchets (develop's movement touches no vc-issuer path, and the PR touches nothing outside it).
- I did not re-measure the builder's push-attempt claims, and I did not read the builder's evidence files as results.

Nothing was written to GitHub, Linear or any !CODING path. No mail was sent, nothing was launched, and no sub-agents were used.
