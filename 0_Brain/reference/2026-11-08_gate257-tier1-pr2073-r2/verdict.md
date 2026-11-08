# Gate 257, tier 1, round 2 of 2: verdict

| PR | Ticket | Head | Verdict |
|---|---|---|---|
| 2073 | KS-1152 R-880-1 | 2684a29d8f576ff74634f07ad6576af5bd00370b | GO WITH NOTES, one item for Kam (F1). No finding blocks. |

This verdict covers this SHA only. Readings at origin (ls-remote from my clone):
- start 2026-11-08T11:11:04Z: develop cfb6c1573ba9, 2073 2684a29d8f57, 2060 796ea55fb8eb, 2072 14f402572f1a, 2077 b387a6ef1c02
- end 2026-11-08T11:36:36Z: develop cfb6c1573ba9, 2073 2684a29d8f57, 2072 14f402572f1a, 2077 b387a6ef1c02. Nothing moved, so the verdict stands.

Severity is mine. Priority is not.

Environment: my clone /private/tmp/g257 (blobless, from the remote and deploy key the shared checkout names, read only there). Node is the host's v26.8.1 line. node_modules came from the seat's worktree s-y6-ks1152, whose root lock is byte-identical to this head's (295b276a). Real PostgreSQL 15 ran in my own private cluster on port 55757, now stopped. It was built the way the containers build it: docker/init/0[1-9]*.sql, then 59 main-DB migrations, then the app role's grants (NOSUPERUSER NOBYPASSRLS; svc_api_keys has RLS forced).

---

## For Kam, at the top: F1, the deciding question

**The seat's carried finding reproduces, and it is wider than the seat put it.** On a real gateway route over real security on real PostgreSQL:
- **G2.** A 0 answers `rotated: false`. A retry then answers `rotated: true`, count 1 and no warning, while the older key with no connector id still validates.
- **G3.** An organisation that holds both an older key with no connector id and a key with the connector id gets `rotated: true`, count 1 and no warning **on the first call**, and the older key still validates. No 0 is needed.

So `rotated: true` has never meant "no older key of this organisation still works", and this PR does not make it mean that.

**Inside the card's words?** Literally, yes. Card a speaks only of a count of 0, and every sentence the spec and contract say about `rotated` is true of the code: a count of 1 or more. In purpose, no. Card b's question was whether the operator should be told "rotated" while the old key works. G2 and G3 tell the operator exactly that, with no warning.

**Does it make "rotated" a false statement Stuart's team will act on?** Not Stuart's team directly. Rotation is platform-admin only (GUARDRAIL 1), so a K admin reads the reply, and whether Platform S reads `rotated` is unknown. The only code reader is systemTest, and it stops at `rotated: true`. The contract Stuart's team reads says "a retry does not help" but not that the retry answers `rotated: true`, and it does not mention G3 at all.

**Why it does not block:**
- This is old behaviour. Develop answers `rotated: true` on the 0 itself, on the retry and on G3.
- This PR strictly narrows it: the 0 is now honest.
- The cause is in security's retire, which matches only connector_id. The gateway cannot see it.

**Wednesday's ruling A2 versus Kam's card:** A2 is not wider in scope. The added warning and its "revoke it by its id" advice sit inside card b's "say why". The extra console.warn and the contract paragraph are additions Kam did not name, and they are harmless. But A2 has a cost Kam's card does not show. One code now carries two instructions, so a client that reads only the code will retry after a 0 and land in G2. The body calls that retry "futile, not harmful". I disagree with "not harmful": the retry ends in a false all-clear, `rotated: true` with no warning. That trade-off is Kam's to make.

---

## PR 2073, KS-1152: findings

**F1, MEDIUM, old behaviour, does not block, needs Kam.** `rotated: true` with no warning while an older key of the organisation with no connector id still validates. This happens on the retry after a 0 (G2) and on the first call when the organisation holds both kinds of key (G3).
- Where: `services/api-gateway/src/routes/platform.ts:979` (rotated is the count ≥ 1) and `services/security/src/index.ts:239,246` (`WHERE connector_id = $1 AND tenant_id = $2 ...`).
- MEASURED AT RUNTIME on real PostgreSQL, at this head and again on the develop merge:
  - G2a: 200, `rotated` false, `priorKeysRevoked` 0, PRIOR_KEY_STILL_ACTIVE. The older key and the new key both validate.
  - G2b (the retry): 200, `rotated` true, 1, no warning. The older key is still valid; the 0 call's key is no longer valid.
  - G3: 200, `rotated` true, 1, no warning. The older key is still valid; the connector key is retired.
- Oracle: the purpose of card b, and the flow fragment's "was told it rotated while the old key kept working".
- Fix shape, READ ONLY as to the fix, so do not build it here: security reports how many active keys of the organisation remain after the retire, or the retire also takes the organisation's keys that have no connector id. Either is a ruling. A regression test the owner should add: G3's shape, asserting that `rotated` is not true while the older key validates.
- Documentation the owner should add, one sentence each in the contract and the spec, if Kam keeps this behaviour: "`rotated: true` says nothing about an older key with no connector id; a retry after a 0 answers `rotated: true` with that key still active."
- Not measured: how many such keys exist on any box.

**F2, MINOR, test gap that round 2 created.** Nothing pins `rotated` to an existing organisation any more. I planted T5: drop `existing.rows.length > 0 &&` from `rotated` (`platform.ts:979`). **0 of 25 cells failed.**
- Why: in round 1, C3's count of 0 caught this plant (gate 245's plant "rotated on a new org", 1 red). Under `>= 1`, a count of 0 on a new organisation reads false either way.
- The real shape it leaves open, MEASURED as G6: a new organisation whose rotate retires a sibling key of this connector answers 201 with count 1. Today that is `rotated` false. Under T5 it would read true, and the spec says "true only when an existing Organisation was rotated".
- Fix shape: C3 should also run with a count of 1, for example `it.each([[0],[1]])`.

**F3, MINOR, spec and fragment text is untrue for a new organisation.** On a rotate of a NEW organisation with a count of 0 or more, the reply is 201, `rotated` false and **no** warning. MEASURED as G5 (count 0) and G6 (count 1); cell C3 pins it.
- Three sentences are untrue for that case:
  - The spec's `rotated` description, in `tenant-provisioning.openapi.ts` and the yaml: "A count of 0 answers false, with PRIOR_KEY_STILL_ACTIVE and a message..." The sentence is unqualified, but the 0 warning is for an existing organisation only.
  - The spec's `rotationWarning` description: "Present when a rotate did not retire a prior key". G5 retired nothing and has no warning.
  - The cheat fragment: "Otherwise, with status 200 or 201 ...: `rotated: false` and `rotationWarning.code` PRIOR_KEY_STILL_ACTIVE".
- The PR body's table is right ("new organisation, a count | 201 | false | the count | absent"), and the contract paragraph is right because it says "on an existing organisation".
- Fix: add "on an existing Organisation" to those three sentences. This is a published-spec edit, so it needs a regeneration.

**F4, NOTE, READ ONLY.** A count that is a number but not a non-negative integer (-1, 0.5) answers `rotated` false with **no** warning, and the number is passed up. The code comment at `platform.ts:944` says a malformed reply must not read as rotated: it does not, but nothing says why. Security returns `rowCount`, so this cannot happen today. No cell covers it.

**F5, NOTE, my own prediction was wrong (recorded, not a defect).** I planted T4 (`=== 0` → `< 1`) expecting it to be equivalent. It is not: `null < 1` is true in JS. C10 (no warn on null on an existing organisation) caught it, 1 red.

## The commission's six questions

1. **Gate 245's F1 and F2: closed.** F1: G1 and G2a give a 0 on an existing organisation as `rotated: false`, 0 and the no-prior-key message, measured on real PostgreSQL. F2: the new-organisation message has no "previous key" (cell R3 ran and passed). I also confirmed by code read that it is chosen only when the reply is not a number and the organisation is new (`platform.ts:962-966`). The seat's P4 held-lock run covers it end to end; I did not repeat that run.
2. **The 0 branch: yes.**
   - G1, existing organisation, no other key: 200, `rotated: false`, `priorKeysRevoked: 0`, PRIOR_KEY_STILL_ACTIVE, and the message "The new key works, but no previous key of this connector was switched off...". It matches the code's constant byte for byte through cell R6 (toEqual).
   - `rotated` is true only for a count of 1 or more: C1 at counts 1 and 3, and G3 and G4 live.
   - My plants, each restored with the sha256 checked (437e32a8...), run twice:

     | Plant | Cells red |
     |---|---|
     | T1 `>= 0` | R6 |
     | T2 0 branch on a new organisation | C3, C10 |
     | T3 the 0 carries the retry message | R6 |
     | T4 `< 1` | C10 |
     | T5 | **survived** (F2) |
     | T6 no warning on a 0 | R6 |
     | T7 the 0 reported as null | R4, R6 |

     Every red was by assertion.
3. **The carried finding:** reproduced, and extended by G3. See the top and F1.
4. **Spec and S-K-OWNERSHIP-CONTRACT.md, sentence by sentence:**
   - Contract: every round-2 sentence is true of this head, checked against G1, G2 and the code. It omits the retry's `rotated: true` and G3 (F1). That is an omission, not a false sentence.
   - The older steps 1 and 3 ("old key untouched", `DELETE /api/keys/:id`) predate this PR and are already corrected by the [RE-VERIFIED 2026-10-30] note above them.
   - Spec: the request description and the `priorKeysRevoked` description are true. The `rotated` and `rotationWarning` descriptions are untrue for a new organisation (F3).
   - The body's "list the organisation's keys (security GET /api/keys, key admin)" is true by read: `index.ts:1561`, requireKeyAdmin, organizationId required.
5. **systemTest `connector_keys.py:230` and its live caller: no real caller breaks.**
   - READ ONLY: the one live caller (`test_connector_key_lifecycle.py:82`, via `connector_key_fixtures.py:108`) registers a fresh organisation with a provisioning key. The gateway mints with `connectorId: platform-s:<externalRef>` (`platform.ts:906`) in the caller's tenant, and the organisation row has that tenant. The admin rotate then retires 1, so `rotated: true`.
   - PROBED: G4, a clean rotate of a connector key, gives true. It does not cover the provisioning-key door or a real box.
   - The other `rotate=True` user, `test_connector_identity.py:255`, expects a 403 and does not read `rotated`.
6. **Merge on develop cfb6c1573ba9 (PR 2060 merged): clean.**
   - merge-tree rc 0, tree fa487d06. Planted control: a conflicting edit to the same `rotated` line gives CONFLICT, rc 1.
   - On that merged tree (synthetic commit 73e5899c, local only):
     - KS-1152 gateway cells: 25 of 25.
     - Whole gateway: 1865 of 1865 (167 files, 3 workers).
     - Security KS-1152 real-PostgreSQL cells and my probe: 10 of 10.
     - `check:openapi`: PASS, 422 example blocks OK.
   - **2072 and 2077 share only the generated yaml.**
     - develop + 2073 + 2072 + 2077: clean at every step.
     - The order develop, 2077, 2072, 2073 gives the identical tree 7e94372c.
     - On the triple merge, `generate-openapi --check` PASSES: the text merge already equals the generated file.
     - Regenerating twice gives the same sha256 both times (170ddf7a...), equal to the merged file.
     - A planted source edit without regeneration fails the check (CHECK FAIL, rc 1).
     - **The regeneration is deterministic, and today it is a no-op.** Whichever PR merges second should still run it.

## What I did NOT test
- Platform S (another repository), whether it reads `rotated`, and the four platform suites.
- Any box, a local stack, or a real login or real token. The gateway's sign-in and its organisation lookup were stubs in my probe.
- A real `API_KEY_ROTATION_GRACE_SECONDS` window. Under grace, "retired" means expiring, not dead.
- A timeout between gateway and security, and the revoke-by-id route.
- I did not re-run the seat's P4 held-lock case end to end. The security file's held-row cell ran (null, both keys active).
- Not run on my side: tsc, eslint, the ratchet, the docs-fragments check, tenant-provisioning, and the whole security suites.
- The PR body and the ticket comment as published. I read the seat's `pr/body_r2.md`; network was git only.
- How many keys with no connector id exist on any box.
- Node LTS.

## My own conduct
- **Fixed nothing, posted nothing, no box, no docker.** Network was git ls-remote and fetch only. The shared checkout was read only: I read its remote URL and core.sshCommand, and fetched nothing there. The seat's worktree s-y6-ks1152 and record folder were read only: an rsync of node_modules out, and file reads.
- **Writes:** this verdict, and /private/tmp/g257. **One stray write:** a merge-tree output went to /private/tmp/null_g257, outside my folder. I moved it at once into /private/tmp/g257/_quarantine_2026-11-08/.
- **One bad dependency copy, quarantined, not removed:**
  - My first node_modules came from the shared checkout. Its zod is 3.25.76, but the lock says 4.6.7, and packages/shared failed tsc with 10 errors. I moved that copy to `_quarantine_2026-11-08/` and used the seat's worktree, whose zod is 4.6.7 (a clean build).
  - That copy carried an absolute self-link, `node_modules/node_modules`, which points at the seat's worktree. A stack trace showed a dependency loaded through it. I moved the link to quarantine and re-ran: 25 of 25, and the plants gave the same results on the second run.
  - Product code always came from my clone; every failure path names /private/tmp/g257.
- **Load:** mostly 5 to 7.5. **It went over 8 twice:** 9.02 just after the whole gateway run, and 9.20 at clone time. Both came back under 8 within about a minute. I waited for load under 7 before the next heavy step.
- **Disk:** DevMASTER stayed at 23 GiB free throughout; nothing of mine is on it.
- **Clone left in place, not removed** (the QA template's no-rm rule): /private/tmp/g257, **7.2 GiB by du** (5.5 GiB by `du -A`; three worktrees share APFS clones of node_modules). It holds:
  - the repo and three worktrees (head, merged, m3)
  - my private PostgreSQL data directory and its 0600 password file (never printed; stopped, pid 43170 gone)
  - my probe (`probe/g257-probe.integration.test.ts`, plus untracked copies in two worktrees)
  - the plant runner `tamper.py` and raw outputs in `out/`
  - local synthetic refs refs/g257/*, never pushed
  - the quarantine
