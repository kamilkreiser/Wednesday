PR 2245: GO WITH NOTES (at head 616c57ba4e5136c98947b277aaed6e40429b8c1b; tier 1)

# Gate 370, tier 1 (Opus), PR 2245: KS-2189 + KS-2188, the kyc erasure. Findings only.

Pins: head re-pinned with gh api at 03:25 AEDT and again at 16:34:21Z (03:34 AEDT): 616c57ba4e51, open, 1 commit, 8 files. Develop c7b3c2abf08c983bed5129a3f2a81b1c3a1be4a9 at both reads. PR built on d041f1a54f8f, which is an ancestor of c7b3c2ab.
Scratch: my own `git clone --shared` of `worktrees/s-c40-base` (read only there), origin removed. `npm ci` at Blockchain/Dev (1794 packages, rc 0), then `npm run build -w @secuura/shared`. Node v26.8.1 (not LTS), vitest 4.1.12, tsc 5.9.3. I read load1 before every leg (2.81 to 7.42). One mutant leg waited 60 s at the load gate. No database, no ssh, nothing posted.

## Verdict basis, by commission question

**Merge-tree.** `git merge-tree --write-tree` gives tree 3243262ccfd4, clean (rc 0), in both orders on develop c7b3c2ab. The patch-id of the merged tree against develop equals the PR's own diff. Planted control: a commit on develop that edits the initiate schema line conflicts (rc 1, 1 CONFLICT).

**Suites, interleaved:**

| Tree | Result | Runs |
|---|---|---|
| develop c7b3c2ab | 218/218 in 20 files | twice |
| merged tree | 258/258 in 22 files | twice |
| head 616c57ba alone | 258/258 | once |

There is no pre-existing red.

**Red-first.** I ran the merged tree with develop's index.ts. 18 cells fail and 240 pass, and all 18 fail by AssertionError: KS-2189 S1, S2, S3, S4 and I1; KS-2188 P1, P5, P6 and B1 for each of the 3 causes; and ks2166 cell I. This matches the READY. On develop, P6's thrown message is the caught JSON.parse text quoting the stored value (`Unexpected token 'Z', "ZQX-poison"`). That is the leak KS-2188 closes.

**(1) KS-2189.**
- `USER_ID_MATCHES_ASCII_FOLDED` is `translate(user_id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz') = translate($1, <same 26 / 26>)`. Both sides use the exact 26 ASCII capitals to the 26 ASCII smalls, with nothing non-ASCII in either string.
- The constant is used in all four statements: the erasure read, and the DELETEs on images, consents and verifications. The image-by-id DELETE (`id = ANY($1)`) is unchanged, fed from the decodable rows of the folded read.
- Schema: user_id and id are TEXT on all three tables (migrations 002 and 035). So `translate(text)` and `id <> ALL($2::text[])` type-check by reading. They were NOT run on PostgreSQL.
- O2's K_SIGN really holds U+212A. I checked the bytes: `ks2189-Kelvin-subject`.
- Initiate uses `z.string().guid().transform(asciiFoldedUserId)`, a hoisted function declaration. I2 (lower-case stored unchanged), I3 (400) and I4 (403) are green.
- The O1 control (a different id) is green under every mutant except the ones that delete everything.

**(2) KS-2188.**
- `dbReadVerificationsForErasure` decodes with Promise.allSettled. A rejected row is recorded by `String(rows[i].id)` only.
- A failed SELECT logs and throws. P9 is green, and my mutant g18 (the SELECT failure swallowed) turns ks1931 R1/R2, ks2185 R1a/R3a-c and P9 red.
- The DELETEs run in today's order, with `AND id <> ALL($2::text[])` on the verifications DELETE.
- Then evict. Then one `logger.error` with `{ keptVerificationIds, kept }`, and a throw whose message holds the ids and the count, with no content.
- The route answers the KS-2185 generic 500 (P3). The bus handler logs `err.message`, which now holds ids only, and rethrows (B1).
- A retry converges (P7). An all-decodable erasure answers 200 with count 2 (P8).

**(3) Nothing widened.**
- The 8 files are index.ts, 2 new cells, 3 existing cells and 2 fragments. None of them is in packages/shared, routes/, userErasedSubscriber.ts, db.ts, subjectDeks.ts or migrations.
- In dbGetVerificationsByUser only the comment line at 240 changed. The GET route is unchanged.
- `subjectDeks.evict(userId)` still runs on the given spelling.
- Only kyc's own index.ts touches the three tables (git grep over services/ and packages/; the 2 shared hits are crypto/image helpers).

**(4) Existing cells changed by design.**
- With the change in place and develop's ks1931 and ks2185 files (the OLD regexes), 7 of 14 cells fail: ks1931 R1 and R2; ks2185 R1a, R1b, R3a, R3b and R3c. The injection no longer fires.
- With the widened regexes, 14 of 14 pass. So each widened failOn FIRES on the folded SQL.
- ks2166 cell I now uses an upper-case caller and expects the lower-case fold to be stored. My g09 (transform removed) turns it red. The stored value is the body's fold, never the caller's raw spelling.

**(5) My own mutants.** Each mutant runs the whole kyc suite on the merged tree. The tool is `scratch/tools/mutants_g370.py`; per-mutant JSON is in `scratch/out/`, and the summary is `scratch/out/mutants_summary.txt`. I proved the sha256 restore after every mutant.

Control: g00, with every fold removed, fails S1-S4.

Killed (red set):
- g01 read unfolded: S3
- g02 images DELETE unfolded: S1, S2, S4
- g03 consents DELETE unfolded: S1, S2, S4
- g04 verifications DELETE unfolded: S1-S4
- g05 lower() everywhere: O2a, O2b, plus the 7 W3 regex cells
- g05b lower() on the read only: O2a, O2b, plus 6 W3 cells
- g05c lower() on the verifications DELETE only: O2a, O2b
- g06b translate on the param side only: S1-S4
- g09 transform removed: I1, ks2166 I
- g10 per-row catch removed: P1, P5, P6 and B1, times 3 causes
- g11 kept row deleted too (`OR 1=1`): 21 red
- g11b empty exclusion parameter: P1, P2, P4, P5, P7 and B1, times 3
- g12 exclusion inverted (`id = ANY`): 25 red
- g13 success instead of the throw: P3-P7 and B1, times 3
- g13b throw only when 2 or more rows are kept: same set as g13
- g14 throw before the deletes: P1, P6 and B1, times 3
- g15 row content logged: P5, times 3
- g15b caught message logged: P5, times 3
- g16 caught message in the throw: P5 and P6, times 3
- g16b ids dropped from the throw: P6, times 3
- g18 SELECT failure swallowed: 7 red

Survivors:
- **g06**: the fold on the column side only, `translate(user_id, ...) = $1`. 0 red. See finding G370-1.
- **g19**: the erasure's own kept-ids `logger.error` line removed. 0 red. See G370-2.
- **g07**: the fold over A-F only. 0 red. Equivalent for GUID ids; see G370-3.
- **g08**: `toLowerCase()` at initiate. 0 red. EQUIVALENT, as the seat declared (zod `guid()` admits ASCII hex only).
- **g17**: evict removed. 0 red. evict is pre-existing and not a changed branch.

**(6) PR body.**
- It states the scan cost (btree defeated, read and DELETE on verifications plus one scan each on consents and images, row counts UNMEASURED).
- It states the ASCII-only fold by Wednesday's W4, with the PostgreSQL locale "no longer relied on" and "not measured".
- It states the partial-erasure semantics, the two-key title as a known merge-tool case, the existing cells changed by design (W3, and ks2166 I), and what was NOT run. No self-hold sentence.
- A grep for closing words with `/usr/bin/grep -i` gives 1 hit: "a subject-DEK resolve that rejects", in prose with no issue key. It is not a closing keyword.

**Other checks.**
- tsc on the service: rc 0. tsc over src plus all 22 test files (my config; `--listFilesOnly` shows both new files): rc 0. A planted TS2322 gives rc 2.
- eslint (root flat config, the subprocess cwd set to Blockchain/Dev, absolute paths) on the 6 changed TS files: rc 0. A planted `debugger;` gives rc 1 in a test file and rc 1 in index.ts.
- check:test-types: rc 0, 0 new errors in all 5 services.
- `docs-fragments.mjs check`: OK. A planted unclosed div in the flow fragment gives FAIL rc 1 ("tags are not balanced"). Restored sha-equal.

## Findings

- **G370-1 (LOW, test gap; product correct):** no cell erases with a NON-lower-case id.
  - Both the owner's DELETE path id and the bus payload are untested with an upper-case id. The owner check admits the caller's own upper spelling, and the bus payload is unvalidated.
  - So mutant g06 (`translate(user_id, A..Z, a..z) = $1`) survives the whole suite. With g06, an erasure called with an upper-case id would miss every lower-case-stored row, and that includes every row initiated after this PR.
  - Suggested follow-up cell: lower-case-stored rows, erased via the route with UPPER as the path id and the caller id, and via the bus with UPPER. Not a blocker: the shipped SQL folds both sides; I read this and S1-S4 exercise it with the other spelling direction.
- **G370-2 (LOW, test gap):** removing the new kept-ids `logger.error` line (g19) leaves the suite green.
  - P5's "names the kept row id" positive is satisfied by the cascade handler's own failure line, which carries `err.message`.
  - On the route path, the ids would then be logged only by the shared errorHandler (winston; the cell does not record it).
  - The spec says "log the ids once at error level". The line exists at the head; nothing pins it.
- **G370-3 (INFO):**
  - g07 (fold over A-F only) survives. It is equivalent for GUID ids: auth issues `uuidv4()` ids (userRepo.ts:774). It is not equivalent for a non-GUID bus id with letters G-Z in upper case. No such id is known.
  - g17 (evict removed) survives. It is pre-existing, outside the change.
- **G370-4 (INFO, UNMEASURED, as the PR says):**
  - No PostgreSQL ran. translate() semantics, `$1` type inference inside translate(), `id <> ALL($2::text[])` with an empty array, and the scans are read and modelled only. By reading, the column types support them (TEXT).
  - The new read's SELECT-failure log keeps KS-1931's `error: <caught message>` (a pg error text, not row content). That behaviour is unchanged and copied.
- **G370-5 (INFO, a behaviour note on GET):**
  - Initiate now stores the lower-case fold. A caller whose token id is upper-case and who GETs `/api/kyc/user/<UPPER>` will no longer see rows initiated after this PR: the GET read stays exact-text by ruling W1.
  - Near-theoretical, because auth issues lower-case uuidv4 ids. It is named because GET's observed result changes for that caller. Not built or measured.

## For Kam (personal-data erasure path: what is and is not erased)

All as ruled in the ANSWER of 2026-11-15 04:41:40Z (3 ii) and W4. Nothing here is new scope.
1. **NEWLY erased:**
   - Verifications, consents and images stored under any ASCII-case spelling of the subject's id.
   - Legacy images named by those rows.
   - Every decodable row, all consents and all images by user_id of a user who also has an undecodable row. Before, NOTHING was deleted for that user.
   - This is an irreversible deletion that previously did not happen. It is the ruled semantics.
2. **Still NOT erased:**
   - The undecodable verification row(s) and any legacy image named only by them. They are kept, and the call throws: route 500, then bus retry and dead-letter. No success and no count is returned.
   - The upper-case spelling's `pii_subject_keys` DEK row (a privacy residue; the candidate filing, unmeasured).
3. **Never reached:** an id equal only under Unicode case rules (U+212A). Proven against the stand-in only. The PostgreSQL locale is not relied on.

The test gaps G370-1 and G370-2 do not change what the shipped code erases.
