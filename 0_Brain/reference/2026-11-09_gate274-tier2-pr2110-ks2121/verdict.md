PR 2110: GO WITH NOTES

Gate 274, tier 2 (Sonnet), 2026-11-09 07:50-07:55 AEDT. Findings only; nothing posted, mailed or written outside this folder and /private/tmp/g274.

## Pins
- develop 93028c8151ec: read at start and at end, did NOT move.
- PR 2110 head 2cfbd109db5d6ccf5303e6362c5177b96e916254: read at start and at end, did NOT move. The head is one commit whose parent is 93028c8.
- DevMASTER free: 9.7 GiB at start and at end (floor 8). load1 3.0 at start, 4.5 at end.

## FOUND / TESTED / HOW
1. Test-only (Q1): TRUE. `git diff 93028c8 2cfbd10` is 1 file, +15 -0, the transfer test `ks2081-transfer-doors-refuse-non-user-principals.test.ts`. No product, config or docs byte. The test file sha goes ce2785b0e79243cb -> 05e9b42e82e39c93, as the seat said.
2. Does the cell compare the 403 refusals (Q2): YES. The cell, quoted:
   ```
   describe('KS-2121: the refusal is one answer across the six write doors', () => {
     it('RED KS-2121 F1: a key reads one and the same refusal, headers included, at all six write doors', async () => {
       const id = await open();
       const token = key(null, TENANT_A);
       const prints = new Set<string>();
       for (const d of DOORS) {
         const res = await call(token, 'POST', d.path(id), d.body());
         expect([d.name, res.status]).toEqual([d.name, 403]);
         prints.add(fingerprint(res));
       }
       expect(DOORS).toHaveLength(6);
       expect(prints.size).toBe(1);
     });
   });
   ```
   The cell does what the ticket asks. KS-2121's fix shape reads: "one cell that takes the refusal's `fingerprint` for one key at each of the six doors and expects a single value, shown red by a per-door header like own3." `fingerprint` is the file's own helper: status, raw body and every header except `date`. `DOORS` is 2 open doors plus 4 id doors, so 6, and the length is asserted. Each door's status 403 is asserted by name. A single id is used, so the cell pins across doors only. Across ids the existing R3 cells already pin it.
3. Red-first / cells (Q3), all run by me in /private/tmp/g274/h (Node v26.8.1; `@secuura/shared` built and linked, `jsonwebtoken` linked from auth, `npm ci --ignore-scripts`):
   - Whole transfer suite at head: 461 passed, 0 failed.
   - Test file swapped to the develop version (sha ce2785b0e79243cb): 460 passed, 0 failed. The head version was then restored, sha 05e9b42e82e39c93 confirmed, and `git status` was clean. So 460 -> 461, 0 failed both sides, and the cell passes on develop.
   - Mutants. The product `index.ts` sha 46ceb56cc1174bdf was restored after each run (confirmed after each). Each mutant adds `res.setHeader('X-Probe', ...)` before the 403 in `refuseNonUserPrincipal` (index.ts:522-526).
     - `req.route?.path` (per-door, id-free; this is the seat's mutant, re-made by me): exactly 1 cell red, F1, "expected 6 to be 1"; 460 green. Matches the seat.
     - `req.path` (the checker's, id-dependent): 5 red by assertion, F1 plus R3 approve, reject, execute and cancel. Matches the seat and the PR body.
     - `req.method` (control, all six doors are POST so it is constant): 0 red. The cell does not false-fail.
     - `req.originalUrl` with the first UUID stripped (my own): 5 red, the same 5. This is not purely id-free: the malformed id is not stripped, so the R3 cells see it.
     - `req.params?.id` (my own, id only): 5 red, with F1 "expected 2 to be 1". F1 reddens because the open doors carry no id, so it separates open from id doors. The cell therefore catches any header that differs between the open doors and the id doors, not only a per-door-name header. That is within the intent and is not a defect.
4. Merge tree (Q4): `git merge-tree --write-tree` of 2cfbd10 on 93028c8151ec returned rc 0. This is trivially clean because the head is a direct child of develop. Path-sharing scan: I fetched blobless all `refs/pull/19*`, `20*` and `21*` heads (236 refs) and diffed each against its merge-base with 93028c8. The planted control PR 2110 was found (positive). The only other hit on this test file is PR 2077, which is already merged (its own KS-2081 commit, the file's origin), so no open PR is shown sharing the path. PRs 1938, 1944, 1953, 1957, 1962, 1975 and 2048 touch other files under services/transfer, not this one. The seat's driver reads "47 open PRs, none on this path".
5. PR body and ticket comment (Q5): I could not read the live PR or the live comment (no GitHub token for the repo, the REST call returns 404 for the private repo, and Linear was not touched). I read the seat's recorded bodies instead (`evidence/d3/mail/pr_body_FINAL.md`, `ticket_comment_FINAL.md`, `pr_record.json` with head 2cfbd109db5d and title "Refs KS-2121: ..."). Every factual sentence I could re-measure holds at the head:
   - +15 -0, 1 file.
   - 460 -> 461, 0 failed.
   - A per-door id-free header reddens exactly this cell and the other 107 stay green (108 cells in the file).
   - The checker's header reddens 5 cells: F1 plus R3 approve, cancel, execute and reject.
   - Both are restored byte-equal.
   - "Refs" and not a closing form.
   - The cell is green on develop by design.

## Findings
- G274-1 (low, naming): the cell is named `RED KS-2121 F1 ...`, yet it passes on develop (I measured this). The file's own header (lines 6-7) defines "a name starting RED fails at the branch's base by assertion; a name starting control passes there too, so it proves only by the planted mutants named in the PR". By the file's own rule this cell should start with `control`. As named, it overstates: a reader or tooling that trusts the label will expect it to be red on base. The PR body itself says "green on develop by design". Suggest renaming it `control KS-2121 F1 ...` (a cosmetic round-2 change, and it would give a new head). The describe title is fine.
- G274-2 (note, no action): the cell uses one id for the id doors, so a header that varies only by id is not caught by F1 alone (R3 catches it). Not an error, but the cell's name "one and the same refusal" is across doors, for one id only. Measured by the `req.params.id` mutant: F1 turned red there only because of open vs id doors.
- G274-3 (note): the live PR body and comment were not read at origin (no token). They were checked against the seat's recorded final text only. If Wednesday has a gh token, a body sha1 compare against `4e9a311c852f8f6bd8e74aad5f8433f491b0f83a` closes it.
- G274-4 (note, from the READY): the seat's pre-push hook ran 13 of 16 legs and 3 were skipped (legs 3, 4, 8, stack down). This is NOT a pass. The seat says so and the PR body quotes it. It matters only if Wednesday counts the hook as evidence.

No finding stops a merge. None needs Kam's ruling.

## NOT TESTED
- Live PR 2110 body and the live KS-2121 comment at origin (see G274-3); KS-2121 live state.
- Open-PR set is not enumerated (no API token). Scan covered PR numbers 1900-2199 only, so an older open PR sharing the path is not excluded. The seat's driver read 47 open PRs and none on this path.
- `tsc` of the test file and lint (the seat ran tsc; I did not repeat it; transfer has no lint script).
- Node 24, the preflight hook legs, the boxed stack.
- Whether the mutant is the regression that matters (the PR says so itself).
- My setup differs from CI/seat: workspace packages hand-linked, `--ignore-scripts`. Results match the seat's counts exactly (460/461), so no sign of skew.

## Conduct
- Clones: /private/tmp/g274/r (develop, then blobless full history plus 236 PR refs), /private/tmp/g274/h (head; node_modules; shared build). Total 1.8 GB on the boot volume (disk3s5, 265 GiB free). No rm (QA no-rm), so the clone remains for removal by Wednesday.
- Nothing was written inside any /Volumes/DevMASTER/!CODING checkout. Only ls-remote and file reads were done there; the ssh key path was read from the config and never printed. No `cd` was used (one early call carried a `cd` and the hook refused it, with no effect).
- Product `index.ts` was mutated only in my own clone and restored by sha (46ceb56cc1174bdf) after every run.
