PR 2150: GO WITH NOTES; PR 2152: NO GO

# Gate 298, tier 1 (Opus): PR 2150 (KS-1970) and PR 2152 (KS-1516). Seat U 21st round 1.

| PR | head | verdict |
|---|---|---|
| 2150 | ef2e7e75b26d677b3c999850f2688fda170b16d9 | GO WITH NOTES |
| 2152 | 990efc316091978cdac4e3e37a571efc9bc779d8 | NO GO (needs Kam's call: see G298-2152-1) |

**Pins.** Start (21:27:16Z, ls-remote): develop 0d286210f98b, PR 2150 ef2e7e75b26d, PR 2152 990efc316091. These match the commission. End (21:42:31Z): both PR heads are UNCHANGED. **Develop MOVED** to 07d4218e9776 (PR KS-2138, one file `Projects Documents/fragments/cheat/KS-528-react-router-v7-portals.html`, +1 -1). I recomputed both merges onto 07d4218e: rc 0 each, and that file is not in either PR. Neither verdict is voided.

**Method.** I made a blobless clone in this session's scratchpad (`.../scratchpad/r`), with PR heads at `refs/p/<n>`. I added three sparse worktrees (`w/base` = d0b4825c, `w/a` = PR 2150, `w/b` = PR 2152) holding services/auth, services/timestamping and packages/shared. `node_modules` and `packages/shared/dist` are symlinked read-only from the seat's `worktrees/s-u21-b` install. The project checkout's install is stale (zod 3.25.76, no `zod3-compat` in dist), and every cell failed to load under it. In !CODING I used only read verbs, cp-free reads and symlink targets: no fetch, no write, no cd, no rm. I posted nothing and mailed nothing. Load1 was gated under 8 before every vitest run by a wait loop. Other seats pushed it to 18.6 while I was idle, and it was 6.1 to 7.9 at each of my starts. DevMASTER free space: 94 GiB at start and at end. Scratch size: 234 MB clone + 21 MB trees. The tree is left in place: no rm.

---

## PR 2150 (KS-1970, auth `issuerCertSweep.ts`): GO WITH NOTES

**BLUF.** The change does what it says, at exactly the three named catch sites and nowhere else. Each site's guard is caught by its own cells under my own mutants, and readable Errors and strings still log their text. The body's sentence "for every readable value the logged text is what it was" is slightly too broad (G298-2150-1). Nothing blocks.

FOUND / TESTED / HOW
1. **Touched set.** The diff d0b4825c..ef2e7e75 is exactly 2 files: `services/auth/src/services/issuerCertSweep.ts` (+31 -13 by the seat's count; git stat 44 lines changed) and the NEW `.../__tests__/ks1970-issuer-cert-sweep-fire-and-forget-catches-read-a-hostile-thrown-value.test.ts` (+330).
   - **Held patch.** I extracted the fence (lines 29 to 427) of `READY_KS-1970-KS-1970-O122-P1_*.diff.md` myself: 20,793 B, byte-equal (`cmp`) to the seat's `evidence/row1/held.patch` (sha256 f5f3687c...155130).
   - I applied it with `git apply --cached` to d0b4825c in a temporary index. The resulting tree dace2dda3f63 **equals the PR head tree**, which is stronger than hunk-for-hunk.
   - Control: a one-word change planted in the patch gives a different tree (a52c204f), and the diff names both files.
2. **The three sites.** At base they are 127-133, 171-175 and 179-183 (equal to the ticket); at head they are 127-139, 177-187 and 191-201. Each now does `try { reason = String(err instanceof Error ? err.message : err) } catch { reason = 'unreadable thrown value' }` before the logger call. This is the same pattern the file already used at its three guarded sites (64-76, 86-97, 105-116 at head).
   - Red at base: the test file copied onto d0b4825c gives 12 failed of 18 (R1 to R12), with 6 controls green.
   - Green at head: 18 of 18.
   - **My own mutants**, each re-adding the unguarded `err instanceof Error ? err.message : String(err)` inside the logger arguments at ONE site:

     | Mutant | Site | Cells that went red |
     |---|---|---|
     | X1 | EXPIRING_SOON publish | exactly R1 to R4 |
     | X2 | startup | R5 to R8, **plus R9 and R10** (see G298-2150-2) |
     | X3 | scheduled | exactly R9 to R12 |
     | X5 | scheduled catch made silent (`void reason`) | C5, C6 and R9 to R12 |

     Every mutant restored clean (`git diff --quiet`).
3. **Nothing else changed.** A readable Error still logs its message: the controls C1 to C6 (ordinary Error and plain string, at each site) are green at head. Mutant X4 (always log the constant, all 6 guard sites) reddens all six controls, plus the three Symbol cells R4, R8 and R12, so the controls do bind.
   - Other bytes changed: one blank line removed before `if (effectiveInterval > 0)`, and one comment line added (`// KS-1970: the scheduled tick below ...`). The body says both.
   - Log messages and the other fields (certId, daysRemaining) are unchanged.
4. **ks728 cold-start class.** `ks728-social-link-responds.test.ts` at head: 2 of 2 green. I did not see the timeout class bite in auth.
5. **Merge.** `merge-tree` onto develop 0d286210: rc 0, and again onto 07d4218e: rc 0.
   - PR 2117 (the 0d286210 move) touched only `auth/src/__tests__/ks1858-a-usable-token-is-sent-exactly-as-the-provider-answered-it.test.ts`. That is the same directory as this PR's new test, but **0 shared paths** (control: 2150 against itself = 2). The file contains no `issuerCert` text (0 hits; control `import` = 6).
   - 2150 and 2152 share 0 paths. Merged one after the other (2150, then 2152 onto that): rc 0.
6. **Words.** Commit message, the posted body (the API record's body_sha1 425e42acbbcd = sha1 of the stripped `pr_body_ks1970.final.md`) and ticket comment 51d69e68 (`linear_comment_ks1970.md`):
   - 0 closing keyword + key (control: `Refs KS-` = 1 in commit and body), and no bare closing words.
   - The "Not measured in production" caveat is carried.
   - The body names the pre-existing ks949 timeouts and does not claim a pass from the hook.

Findings
- **G298-2150-1 LOW (wording).** Body line 5 and ticket comment 51d69e68 say "for every readable value the logged text is what it was" ("readable values log as before"). That is not quite true:
  - An Error whose `message` is a readable non-string now logs differently. A Symbol now logs the string `Symbol(…)` where it used to hand the logger a Symbol. A null-prototype object now logs the constant where it used to hand the logger the object. A number now logs as a string.
  - The PR's own cells R3/R4, R7/R8 and R11/R12 assert exactly this change and are red at base.
  - The behaviour is better than before; only the sentence is too broad. Suggested truth: "for every readable value whose message is a string the logged text is what it was."
  - File: issuerCertSweep.ts at 130, 180 and 194 (`String(...)` wraps `err.message`).
- **G298-2150-2 LOW (test isolation).** The scheduled-sweep cells (R9 to R12, C5 and C6) call `startIssuerCertSweep(100)`, which also runs the startup sweep against the same hostile value. So a regression at site 2 (startup) also reddens R9 and R10 (my mutant X2). Each site still has its own red set (X3 gives exactly R9 to R12), so no regression can hide. The site-to-cell mapping in the body is just not one-to-one.
- **G298-2150-3 INFO.** R1 to R8 and C1 to C4 are titled `ks1868` and the describe block says "KS-1868", inside a file named ks1970. The body raises this itself ("raised as held"). Cosmetic.

NOT TESTED (2150)
- The whole auth suite: I did not run it. My sparse tree cannot run the whole-tree walkers: `ks949-platform-admin-seed-identity.test.ts` at base failed 3 of 31 in my tree ("the walk finds .env.example files at all", and so on) because the tree is sparse, not because of timeouts. That is not comparable with the seat's numbers. So the seat's "ks949 reds are pre-existing" rests on its own evidence. I read its 4 JSON files: baseline run 1 had 3 ks949 cells + the auth.integration beforeAll timeout; baseline run 2 had 1 ks949 cell; after run 1 had 2 ks949 cells; after run 2 had 0. Every after-red is in the before-set. That is consistent, but it is carried, not reproduced.
- tsc and eslint (carried from the seat). Any real logger behaviour with a Symbol field.

---

## PR 2152 (KS-1516, timestamping `/verify` and create): NO GO, needs Kam's call

**BLUF.** The diff implements option a on the paths it names, and nothing beyond it: no data write, no backfill, no migration. **But the PR's headline LIVE-behaviour sentence is false at this head.** A stored `opentimestamps` or `blockchain` row with `verified = true` (exactly the residue rows) still answers **`verified: true`** on `/api/timestamps/verify` when the caller sends `timestampType: "rfc3161"` with that row's hash and proof. The early return keys on the caller-supplied type. The DB lookup (`WHERE hash = $1 AND proof = $2`) does not filter on `timestamp_type`, and it honours the row's `verified` column.
- This is not a regression: develop answers true there too.
- It is a hole in "report verified:false for both types", and the body, commit message and ticket comment 5debce26 all state "a stored row marked verified = true … read[s] false … for every caller".
- **Kam's call:** either (i) close it in this PR (e.g. the stored-row branch answers false when `ts.timestampType !== 'rfc3161'`; that is within option a, not a data write), or (ii) accept it as residue and correct the body and comment to say the stored rows still verify true under a mislabelled type until the backfill. Under (ii) this becomes GO WITH NOTES.

FOUND / TESTED / HOW
1. **Touched set.** Exactly 2 files: `services/timestamping/src/index.ts` (+9 -2, four hunks; one is the reworded KS-753 comment) and the NEW `.../__tests__/ks1516-opentimestamps-and-blockchain-are-never-reported-verified.test.ts` (+124).
   - Held patch: I extracted the fence (lines 29 to 183) of `READY_KS-1516-KS-1516-O123-P1_*.diff.md`: 10,741 B, byte-equal to `evidence/row2/held.patch` (sha256 8c314751...ed4e3c).
   - Applied to d0b4825c, it gives tree 4cf3aafaca2c = **the PR head tree**.
2. **What a stored row loses, and the control cells.**
   - My probe P4 at head: the R5 answer is exactly `{verified:false, reason}`. Keys `['reason','verified']`; `timestamp` and `tsaUrl` are gone (P5). Base: P4 and P5 red (the row's timestamp was returned).
   - Creation stores `verified = false` with no `verified_at` for both types (R1 and R2 green at head, red at base; INSERT params are read by the cells).
   - Controls C1 to C4 (rfc3161 create, ots with no attestations, rfc3161 stored row, rfc3161 forged token) are green at both base and head.
   - Red proof: the test file on d0b4825c gives 6 failed of 10 (R1 to R6, assertion failures, 0 timeouts); head gives 10 of 10.
   - **My own mutants** on index.ts:

     | Mutant | Change | Cells that went red |
     |---|---|---|
     | M1 | drop the early return | R3 to R6 (clean re-run; the first run also timed out R1/R2 cold, see G298-2152-3) |
     | M2 | drop `blockchain` from the early return | exactly R4 and R6 |
     | M3 | drop the opentimestamps `verified = false` | exactly R1 |
     | M4 | early return answers true | R3 to R6 and C2 |

     All restored clean.
3. **Option a and nothing beyond.** Card `secuura-ks1516-unverified-timestamp-claims-1102`: ruled `a` on 2026-11-02 12:44 (decision_queue show, read only).
   - The diff writes no data, adds no migration, does no backfill, and does not touch `supportedTypes`, OpenAPI or CONNECTORS.
   - It falls SHORT of option a for the residue rows (G298-2152-1).
4. **The dead decode switch** (index.ts head 624-655, the opentimestamps and blockchain cases plus `default`). It is unreachable for both types because of the early return at 577. rfc3161 returns at 614. `verifyTimestampSchema` (schemas.ts:38) admits only the three enum values, so the `default` arm is also unreachable. It is harmless today: if a fourth type were ever added, the reachable arm answers `verified:false`.
5. **The PR body.** It does state the live change first and names the residue (stored rows, backfill Kam's, supportedTypes and OpenAPI, CONNECTORS.md sentence, options b and c).
   - Posted body = `pr_body_ks1516.final.md` stripped (body_sha1 d8279d279f1c matches).
   - Closing words: 0 closing keyword + key in commit, body or comment. The only bare "close" is "what would close it". Control: `Refs KS-` = 1.
   - The false sentence is G298-2152-1.
6. **Suites.** Whole timestamping suite in my sparse tree, my two probe files excluded:
   - head: 112 tests, 0 failed.
   - base (with the copied ks1516 file): 112, with only R1 to R6 failing.
   - `ks1725-hash-pattern…` (3 cells) failed to LOAD in both of my trees with ENOENT, a sparse-checkout artefact, so it is unmeasured by me. The seat counted it, which gives 115.
   - The seat's pre-existing red (`ks1868-timestamping-db-pool-error-listener…` C1, its baseline run 1 only) was 5 of 5 green in my base run. It is a flake on the seat's loaded box; it is not caused by this PR.
7. **Merge.** onto 0d286210: rc 0; onto 07d4218e: rc 0; with 2150: rc 0, 0 shared paths.

Findings
- **G298-2152-1 MEDIUM (an evidentiary claim is false; needs Kam).** index.ts:577 (early return keyed on `data.timestampType`) and index.ts:584-606 (stored-row lookup by hash+proof only, honouring `ts.verified`).
  - Measured with the PR's own harness: probe P1 is a stored `opentimestamps` row with `verified=true`, verified with `timestampType:'rfc3161'`, and it answers **`verified: true`** at head. P2 is the same for `blockchain`: **true** at head.
  - Both are also true at base (pre-existing).
  - This contradicts the body's first bullet, its "Before this deploys" line ("answers false for these two types for every caller, including rows stored as true"), the commit message ("a stored row marked verified = true … read false") and ticket comment 5debce26.
  - Reachable only for rows created before this deploys (new rows store false). Anyone holding such a proof, or a relying party who mislabels the type, gets `true`.
- **G298-2152-2 LOW (wording).** The body's "rfc3161 is unchanged on every path" is very slightly untrue. Probe P3: a stored rfc3161 row with `verified=true`, verified with `timestampType:'opentimestamps'`, now answers false where develop answered true. It only affects a caller who mislabels the type, and false is the safe direction.
- **G298-2152-3 LOW (test flake class).** R1 and R2 (the first two cells, cold app import + RSA keygen) timed out at the 5,000 ms default in 2 of my 9 runs of this file (5,118 ms / 5,509 ms on the first head run; 5,943 ms / 6,349 ms in mutant run M1, where the product change does not affect them). Warm, they take 31 to 720 ms. This is the same cold-start class as ks728 and can false-fail a gate or CI leg under load.
- **G298-2152-4 INFO.** `ks753-mock-tsa-fallback-is-not-verified.test.ts:17-18` (header comment: "the mock-ONLY types (opentimestamps, blockchain) are placeholders by design and keep their behaviour") goes stale with this PR. It is not in the body's residue list.
- **G298-2152-5 INFO.** The GET read paths (`/api/timestamps/:id`, `/hash/:hash`, `/document/:documentId`, via `formatTimestampResponse`) still return the stored `verified: true` and `verifiedAt` for residue rows. The body covers this by naming the stored rows as residue, but it only names `/verify` as the live surface. A reader may think the stored rows no longer read true anywhere.

NOT TESTED (2152)
- Any database (the cells use the PR's DB stand-in; my probes use the same harness). Any stack, real TSA or chain. The gateway proxy path.
- tsc (carried from the seat).
- Callers outside the repo, and what any environment's data holds: UNMEASURED, as the seat says.

---

## Both
- The seat's named pre-existing reds: I did not reproduce ks949 (my tree is sparse, so the instrument does not apply). ks1868-timestamping was green at base in my run. Neither file is touched by either PR.
- No ticket state or GitHub write, mail or post by me. Clone and worktrees are left in the scratchpad (no rm), and the probe/test copies are untracked there only.
