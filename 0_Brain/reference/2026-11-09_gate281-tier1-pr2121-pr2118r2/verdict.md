PR 2121: GO WITH NOTES; PR 2118: GO WITH NOTES

# Gate 281 (RELAUNCH), tier 1 batch (Opus): PR 2121 (KS-2131, round 1) and PR 2118 (KS-2127, round 2 of 2, delta only)

| PR | head | verdict |
|---|---|---|
| 2121 (KS-2131) | 5ea632ca569c40af9685b85845273b3a13b470a9 | **GO WITH NOTES** |
| 2118 (KS-2127 r2) | cd8b80e38a4bfedbfb04cd3bdcddf93b10ffa074 | **GO WITH NOTES** |

Nothing here needs a ruling from Kam. One note on PR 2118 (G281-2118-1) traces to Wednesday's own ruling wording, not to the seat. That is said in the finding.

**Relaunch.** The first run of gate 281 died at the 13:5x seat rotation and wrote no verdict. This run started at 13:55 AEDT.

**Pins.** I read them with `git ls-remote` through the project deploy key, at the start (13:55:24 AEDT) and at the end (14:14:54 AEDT). **None of them moved**, so I gated the commissioned heads.
- develop: `4d6b7bb17fd3be7b3fde8a3babc5d59c91c959b8` at both reads.
- PR 2121 head: `5ea632ca569c40af9685b85845273b3a13b470a9` at both reads. One commit on 2a031f51403f.
- PR 2118 head: `cd8b80e38a4bfedbfb04cd3bdcddf93b10ffa074` at both reads. Round 1's 08cf86d0ec5f plus one commit, on 273de443c30c.

---

## PR 2121 (KS-2131): GO WITH NOTES

### BLUF

The PR is test-only: 3 paths, with no product byte. Its 4 cells boot the real app in-process and do what they claim:
- With no credential, billing, nft and certifications each answer 401 `UNAUTHORIZED` "Authentication required".
- The `sk_` control is admitted and forwarded, with 1 hit each.

I reproduced every mutant the seat declared, and the whole-suite census reproduces exactly at develop 4d6b7bb17fd3. The deviation is real, and the certifications cell's title is true.

There is one test-quality note. The "0 upstream hits" half of each cell is read at the moment the gateway's response ends. A gate that answers 401 and **still forwards** the request passes all 18 cells (G281-2121-1).

### Findings

**G281-2121-1 · Minor (test quality, plus one client-readable sentence) · `Blockchain/Dev/services/api-gateway/src/__tests__/ks570-proxy-mount-auth.test.ts` head line 677 (`hits: seen.filter(...)` evaluated in `res.on('end')`). MEASURED AT RUNTIME.**
- **FOUND.** I mutated the real gate to send its 401 and then call `next()` instead of `return` (index.ts line 1132, `return;` → `return next();`).
  - The PR's file stays **18 of 18 green**.
  - In a copy of the same cells, I changed only one thing: the hit count is read 500 ms after the response ends. That copy turns the billing and nft cells red with `[401, 'UNAUTHORIZED', 'Authentication required', 1]`. The service DID receive the request.
  - Without the mutant, the delayed copy is 4 of 4 green. That is the control.
- **Why it happens.** The cells snapshot `seen` when the gateway's response finishes. A forward that happens after the 401 is sent reaches the recorder too late to be counted.
- **What the control does and does not show.** The `sk_` control proves the recorder can count a forward whose response *waits on* the upstream. It cannot show the race above.
- **What it costs.** The cells' stated purpose ("nothing may reach the service") is pinned only for a defect that forwards *instead of* refusing, not for one that forwards *as well as* refusing. The flow and cheat fragments, the PR body and comment 758b93c9 all say "so '0 hits' is a figure that can fail". That is true, but only for the first kind of defect.
- **Fix shape (owner's call).** Count hits only after the recorder has settled. For example:
  - send an admitted `sk_` sentinel through the same mount after each refusal, and read the count once its hit lands; or
  - poll `seen` briefly before asserting 0.

  Red-proof the fix with this `return next()` mutant.
- **Severity reasoning.** Minor, not Major. Every refusal-without-forward defect is caught, and status, code and message are asserted exactly. A refuse-then-forward gate is an unusual shape.

### Answers to the commission's questions

1. **Test-only?** Yes. The diff from develop to the merge tree is exactly 3 paths: the test file (+96/-1) and the two new KS-2131 fragments. No `src/` file outside `__tests__` changed.
   - **Real app?** Yes. `vi.resetModules()` then `import('../index')`, with every `*_SERVICE_URL` stubbed to a local recorder and `NODE_ENV=test`. The PR head file runs 18 of 18.
   - **The `sk_` control.** It is admitted and forwarded, 1 hit each on billing and nft. This is inside the green run, and my gate-off and leak mutants left it green.
2. **The deviation, by my own mutants.** I applied each one in my clone, ran the file, then restored it. sha256 equality was checked after every run.

   | mutant | the 4 KS-2131 cells | the rest of the file |
   |---|---|---|
   | gate `if (false)` alone | billing and nft red, certifications **green** | 14 green |
   | gate off **and** `requireScope(...)` line removed from the certifications mount (proxy.ts 666) | billing, nft and certifications red | 1 pre-existing static cell also red |
   | `requireScope` removed alone | 0 red | 1 pre-existing static cell red |

   - The pre-existing static cell is "every mount allowed because a gateway guard refuses still carries both layers". It reads the mount source, so it sees my deletion. The seat's mutant evidently disabled `requireScope` in a form that cell does not read. That does not change the result on the KS-2131 cells.
   - **The certifications title** ("refused 401 by the gateway (its spec gate, and the mount's requireScope behind it)") **is true.** Each layer alone holds the cell green, and only both off turn it red.
3. **The whole-suite census at develop 4d6b7bb17fd3. Reproduced exactly.**
   - **Control:** 1880 of 1880 green.
   - **Gate `if (false)`:** 1871 passed and 9 red. These are the same 9 the seat names: ks1461 ×4 (credentials, referrals, governance, and the v1 alias), ks1469 ×3, ks1244 P2 (its probe is `GET /api/v1/credentials`, line 559), and the ks1090 type-check cell. **None is on billing, nft or certifications.**
   - **With PR 2121 merged on develop** (probe commit `287f142d83e5`, local only): control 1884 of 1884, and gate off gives 11 red, which is the same 9 plus exactly the billing and nft cells. That confirms "1880 -> 1884".
   - The seat's evidence file says "files 502". That figure is vitest's `numTotalTestSuites` (describe blocks), not files: there are 168 files. It is internal only; the PR body says "503 describe blocks", which is right.
4. **The fragments are true**, except for the "0 hits can fail" scope in G281-2121-1.
   - "14 of 14 green with the gate off", "Four new cells", "1880 -> 1884" and the mutant table all match my measurements.
   - **eslint** on the file is clean. As a control, a planted file in the same folder fails (rc 1).
   - **The type ratchet** (the ks1090 REAL cell) is green in the 1884 run.
   - **`docs-fragments.mjs check` ends OK** on the head (224 new) and on the merge of both PRs (227 new = develop's 225 + 2). The ADVISORY line-6235 lines are also present on develop.

---

## PR 2118 round 2 (KS-2127): GO WITH NOTES

### BLUF

All three round-1 notes are closed, each measured:
- **G278-1:** every not-HEAD shape under the fault now shows the KS-2127 cause, and it is still refused rc 1.
- **G278-2:** the tag sentence is now true in both fragments and in the seat's recorded PR body and comment.
- **G278-3:** the new `--all` cell goes red under M3.

There is no regression in a healthy repo.
- **Push shapes:** the head's hook matches round 1 and develop on all 21 shapes.
- **Existing suites:** the 9 suites are 264 of 264 on both hooks.
- **New suite:** 12 of 12 on the head, exactly the not-HEAD cell red on round 1's hook, and 7 fault cells red with 5 controls green on develop's hook.

One new Note (G281-2118-1). The banner now printed inside the refusal says "running the preflight UNCONDITIONALLY" right before "REFUSED". That reintroduces, for KS-2127 only, the contradictory text that the hook's own contract comment (head lines 95-96, gate 1540 Minor 1) and a ks998 cell forbid for KS-882.

**Under the two-NO-GO cap this should ship.** The residue is one line of text to ticket.

### Findings

**G281-2118-1 · Note (operator-facing text, closes nothing, new in round 2) · `.githooks/pre-push` head line 375 together with lines 117-119 (banner text) and 95-96 (contract comment). MEASURED AT RUNTIME.**
- **FOUND.** Under the fault, I pushed a branch the remote already has, with the tip not HEAD. The hook printed, verbatim:

  ```
  [pre-push] KS-2127: 'git diff …' FAILED, so what this push changes
  [pre-push]   cannot be computed. A change set that cannot be computed is not an empty one:
  [pre-push]   running the preflight UNCONDITIONALLY. (Run that git diff by hand to see why.)
  [pre-push] REFUSED — this push sends refs/heads/f (…), which changes Blockchain/Dev
  ```

  No preflight runs; the push is refused.
- **What the hook's own documentation says.** The contract comment (lines 95-96) says `_jr_banner` is "printed by the caller ONLY if the run really follows (it used to be printed here, so a refusal followed it: contradictory text, gate 1540 Minor 1)". That comment is now stale.
- **The repo's own suite guards the same contract for KS-882.** My mutant M5 makes the line-375 print unconditional. Under it, ks998 fails exactly "...and the 'Running the preflight UNCONDITIONALLY' banner is NOT printed before the refusal" (79/1). Under the PR head, that cell passes because the guard is KS-2127-only.
- **The cause itself is now shown, and that was G278-1's point.** Only the banner's last sentence is wrong in this context.
- **Whose slip.** Wednesday's ruling offered "print the banner there" as an option without checking the banner's text, and the seat took that option. The slip is the ruling's, not the seat's.
- **Fix shape (owner's call, ticket it).** Print a cause line without the "running … UNCONDITIONALLY" sentence inside the refusal. For example, "KS-2127: 'git diff …' FAILED, so this push cannot be shown not to change Blockchain/Dev". Update the line 95 comment. Mirror the ks998 cell for KS-2127: assert that "UNCONDITIONALLY" is absent from a not-HEAD refusal.

There are no other findings on the delta.

### Answers to the commission's questions (the delta only)

5. **G278-1: CLOSED.**
   - **Probe:** gate 278's `shapes.sh`, which I read whole and copied unchanged (sha1 b4415731 both); the 21 shapes, with the fault.
   - **Result:** all 4 not-HEAD shapes now carry the `KS-2127:` banner, still rc 1 and REFUSED:
     - a tag on a new commit;
     - a docs-only branch;
     - a fast-forward of an existing branch;
     - a branch that tracks develop.
   - **Round 1's hook:** the same 4 are refused rc 1 with no banner. Every other faulted shape is identical between round 1 and round 2.
   - **The new cell** (CELL 6) asserts rc != 0 (and != 99, its set-up guard), "but HEAD is" AND `KS-2127`. Its no-fault control asserts the refusal carries no KS-2127.
   - **Mutant M6** (exit 0 in place of refusing when the marker is KS-2127's) turns exactly that cell red. **Fail-closed holds:** rc and refusal are unchanged from round 1 on every shape.
6. **G278-2: CLOSED.**
   - **Both fragments** now say "a tag on a new commit whose diff fails used to pass silently; it now runs the preflight if it is HEAD and is refused otherwise". My probe measures exactly that:
     - develop's hook: both tag shapes rc 0 with no preflight;
     - head's hook: HEAD-tag runs the preflight with `--all`, and not-HEAD is refused.
   - **The PR body and comment 8d3c3eff:** I read them from the seat's own records, not the live APIs (see NOT TESTED). The r2 PR body (line 42) and the edited comment both carry the corrected sentence. The old comment's "(it now runs the preflight; no cell pins it)" is gone, and the edit read-back is recorded as equal, still one comment.
   - **The commit message** quotes the old sentence only as what was wrong.
7. **G278-3: CLOSED.** M3 (`st_all=0` in `_jr_diff_failed`) turns exactly "a new branch: with git diff failing, the format gate is asked to check every package (--all)" red, 11/1. Its control ("fed the changed paths, not --all") passes under the head.
8. **No regression.**
   - **Healthy repo:** all 21 push shapes are IDENTICAL across head, round 1 and develop (`diff` of the three probe outputs is empty).
   - **The 9 existing hook suites:** 264 of 264 on both the head's tree and develop's tree, with per-suite tallies equal: 36, 12, 4, 80, 21, 10, 4, 82, 15.
   - **The new suite:**
     - head: 12/0;
     - round 1's hook (HOOK_SH): 11/1, the not-HEAD cell;
     - develop's hook: 5/7, all 7 fault cells red and 5 controls green.

     This matches the READY.
   - **Fragment figures** ("12 of 12", "5 controls pass and all 7 fault cells fail"): true. Of the seat's "6 of 6 tampers", I reproduced M3 and added my own M5 and M6. I did not re-run the other four.

---

## Both: question 9, merge trees and overlap

- **PR 2121 on develop:** `git merge-tree --write-tree` gives rc 0 and tree `0eab2c78817fd660673a1b1d803545b87ffe5533`. The diff from develop is exactly its 3 paths.
- **PR 2118 on develop:** rc 0, tree `56ffc9fbc7824ffea8e86bf06b502502af9e53ce`. The diff from develop is exactly its 4 paths, and the hook blob is `5f10bdcc8d7b`, the same as the head's.
- **The two together** (2118 merged onto a local probe commit of 2121 on develop): rc 0, tree `5bdbcf625baf219bc92aabf127c7b7f9f7283c85`, 7 paths. The ks570 blob is the 2121 head's `3ce900f66bde` and the hook blob is the 2118 head's `5f10bdcc8d7b`.
- **Shared paths between the two PRs: none.** Either merge order is clean.
- **Open-PR overlap.** I used the 50 `refs/pull/*/merge` refs at the remote as the proxy for open PRs; there is no gh login, so no API. Against the 7 paths, the only hits are 2118 and 2121 themselves, which are the self-controls.
- **Planted control:** `Blockchain/Dev/.env.example` from PR 2052 was added to the needle list, and it was detected on PR 2052.

## NOT TESTED

- **Live GitHub and Linear content:** the PR 2118 body, comment 8d3c3eff, the PR 2121 body and comment 758b93c9. There is no gh login (the project's gh config says "not logged in") and no Linear read. I read only the seat's recorded files under `5_Project_History/2026-11-09_seatR-90th/push/` (READ ONLY evidence class).
- **PR 2121:**
  - other methods and operations under the three mounts;
  - a live stack;
  - Node 24 (I ran Node v26.8.1).
- **PR 2118:**
  - the seat's other four tampers (only M3, plus my own M5 and M6);
  - dash runs of the round-2 hook (gate 278 ran round 1 under dash; the delta is one `case … esac` line);
  - the leg-14 replica.
- **The decision-queue cards.** Neither READY cites a card. I read the card KS-2131's ticket cites (`secuura-ks736-made-up-token-result-1106`, ruled b by Kam, "record the guards and fix the check, no behaviour change"). PR 2121 is within it.

## Conduct

- **Findings only.** I posted, mailed and pushed nothing. The clone's push URL was set to an invalid value as a guard. Every push went to local bare fixtures only, and I never ran the hook against the real remote.
- **The `!CODING` tree.** I used only read verbs on `!CODING` git checkouts (`config --get`) and read files there. I did not fetch there.
  - **node_modules was copied out with rsync, a read of `!CODING`** (first from `2_Project_Files`, which was stale zod 3; then from the seat's worktree `worktrees/s-r90-ks2131`, zod 4.6.7). The source was read only, and every write was in my clone.
- **Run 1's leftovers.** I inspected `/private/tmp/g281` before reusing it. The clone was clean at `pr/2121`, but its `Blockchain/Dev/node_modules` was a partial copy (vitest empty). **I did not rm it.** I moved it, and my own stale copy, into `/private/tmp/g281/_quarantine_2026-11-09/`.
- **Writes in my clone.** Write verbs (fetch, worktree add, checkout, commit-tree, merge-tree, product-file mutants) ran only in `/private/tmp/g281`. Each mutant was restored and its sha256 checked.
  - My two probe test files were moved out of the tree into `/private/tmp/g281/mut/` afterwards, not deleted.
  - I built `packages/shared/dist` in my clone with tsc.
- **`cd`.** One Bash call contained a no-op `(cd $G 2>/dev/null; true)` subshell, despite "never cd". It did nothing else, and I note it.
- **Load.** load1 ran 4.3 to 7.4 (peak 7.38 during the probe and suite runs). It never reached 8. Full vitest runs used `--maxWorkers=3`.
- **Disk.** df DevMASTER showed 106 GiB free at both start and end.
- **The clone is left in place, no rm: `/private/tmp/g281` = 5.3 GB** on the boot volume (247 GiB free). That is the clone with node_modules (about 1.4 GB), two quarantined node_modules copies (about 2.3 GB), 4 worktrees and fixtures.
- The common rules file says to remove the clone. The commission says not to (no rm), and I followed the commission.
