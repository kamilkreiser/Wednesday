PR 2260: GO WITH NOTES (at head a36828a28ce16d616358cabd4a589c7f2cfbcebe; tier 1 delta)

# Gate 383, tier 1 delta, PR 2260 round 2 (KS-1936), 2026-11-20 ~02:25 AEDT

I re-pinned the head with gh api twice: before the first measurement and again just before this verdict.
- Head: a36828a28ce1. Open, not merged, not draft. updated_at 2026-11-19T15:11:28Z.
- Develop: 6ebd769a0301 both times.
- The live title reads: "Refs KS-1936: only a platform admin can use PATCH /api/admin/identity/users/:id/level".

Everything ran in my own clone, scratch/g. It is a `--shared` clone of the builder's s-w42-base; that repo was only read.
- Worktrees: h = head, d = develop 6ebd769a0301, m = scratch merge dc83480a7b61. The merge tree is 036976c22254, rc 0, the same tree the builder reported.
- node_modules were APFS-cloned from s-w42-ks1936; that tree was only read. Lockfile and package.json blobs are equal at head and develop.
- In each of my three copies, the absolute link `node_modules/node_modules` (it points into s-w42-ks1936) was MOVED ASIDE to scratch/_quarantine/{h,d,m}. After that, 0 foreign absolute links remained.
- The shared package was built in each tree. TMPDIR was /private/tmp/g383t. Load1 was under 8 at the start of every run; the suite script waited through two spikes, up to 16.

## Verdict reasoning
The delta does exactly what it says.
- Only the test file and the two fragments changed. admin.ts is byte-identical.
- The title and both H2s now name the one route.
- Each new cell kills its target mutant by the stated assertion, and one mutant of my own as well.
- On the merged state with LIVE develop, the whole api-gateway suite and both ratchets are clean.

The notes are LOW or INFO; none blocks the merge. The malformed-body cell's precondition is weaker than its comment says (F1). One round-1 sentence about originate's sibling is stale against gate 382 F3 (F2).

## Q1: delta only. CONFIRMED
- `git rev-list --parents`: a36828a28ce1 has ONE parent, 55f448ff69a5.
- `git diff --stat 55f448ff69a5 a36828a28ce1`: 3 files, +43 -9, all modified:
  - `services/api-gateway/src/__tests__/ks1936-identity-level-route-is-platform-only.test.ts` +34;
  - the flow fragment 10 lines;
  - the cheat fragment 8 lines.
- The whole PR against merge-base fb975989cee1: 4 files, +220 -3.
- admin.ts blob is `c817ec2f9b3931e0a810423cf66ef298f5528e9d` at BOTH 55f448ff69a5 and a36828a28ce1. Develop's blob is c13a267002d2, the positive control that the lookup discriminates. The file's sha256 in my tree is 00814053d343eef8, matching the builder.
- Title, flow H2 and cheat H2 each name `PATCH /api/admin/identity/users/:id/level`.
- None of the three says anything about any other route as fixed or safe.
  - The fragments' only other-route mention is round 1's flow ".2 What it does not cover": the organisations PUT/DELETE and originate's handler as "Not probed ... routed to separate tickets". That is not a claim of safety.
  - The PR body names no `api/users/admin/:id` route. Count: 0 (only a `/api/users/admin/organizations/:id` hit, in "What is NOT done"). Positive control: `identity/users` gives 3.

## Q2: the two new cells are honest. CONFIRMED, with F1
Mutant matrix on my tree h, 14-cell file. Each mutant is a counted replacement on admin.ts, and admin.ts was sha256-restored after each run. Evidence: scratch/evidence/mutants_g383.out and .json.

| mutant | result | failing cells (assertion) |
|---|---|---|
| BASE head | 14/14 | none |
| M0 develop's admin.ts | 7 fail | 5 tenant cells, plus malformed `expected 400 to be 403`, plus header `expected 200 to be 403` |
| M1 drop the gate | 7 fail | same 7 |
| M2 isPlatformOrOrgBoundedRole | 7 fail | same 7 |
| M3 check after a query | 7 fail | 6 by `expected [SELECT 1] to have a length of +0`; the malformed cell by `expected 400 to be 403` |
| **M6 gate after the parser** | **1 fail** | malformed-body cell only: `expected 400 to be 403` (the stated reason) |
| **M8 gate reads x-user-role first** | **1 fail** | header cell only: `expected 200 to be 403` (the stated reason) |
| G9 (mine) parser moved to the FRONT, before requireAdmin | 1 fail | malformed-body cell only: `expected 400 to be 403` |
| G10 (mine) gate admits the token role OR the header role | 1 fail | header cell only: `expected 200 to be 403` |
| G11 (mine, probe) lenient parser (error becomes `{}`) | 14/14 | none (the gate still runs first, as expected) |
| **G12 (mine, probe) lenient parser + M6** | **14/14, SURVIVES** | see F1 |

- Both new cells pass at head: 14/14 in my h run, and 14/14 inside the merged-state suite.
- What the 400 is today: on a system-admin call with `{"verificationLevel":` the reply is 400 with an HTML `SyntaxError: Unexpected end of JSON input`. That is the real parser, so the precondition holds for the real reason today. Probe: scratch/evidence/probe_400.txt.
- **F1 LOW (test honesty, optional fix): the precondition can be met without the parser.**
  - The precondition asserts only `status === 400`. The handler's own level check also answers 400: a system-admin sending `{}` gets 400 `BAD_REQUEST`, measured.
  - So if the parser ever turned lenient, the precondition would still pass, and the cell would no longer pin "gate before parser". G12 shows this: M6 survives all 14 cells.
  - The comment "Precondition: the parser really rejects this body" is therefore stronger than the assertion.
  - Fix: assert the precondition reply is NOT the handler's `BAD_REQUEST` JSON (e.g. `expect(text).not.toContain('BAD_REQUEST')`), or that it carries the parser's error.
- re-run M0/M1/M2/M3 for 14 cells: done, 7 fail each, as the builder and the fragments state.
- The fragments' "5 of 5 killed" is true for the PR's five named mutants (M1 M2 M3 M6 M8).

## Q3: merged state (new head onto LIVE develop 6ebd769a0301). CLEAN
- Merge: `git merge-tree --write-tree 6ebd769a0301 a36828a28ce1` gives rc 0, tree 036976c22254. Scratch commit dc83480a7b61; never pushed.
- Develop over the PR's base touches 0 of the PR's 4 paths. It does include PR 2102's four api-gateway test edits, `baseline-api-gateway.txt` (7 lines), `baseline-originate.txt` (+5) and originate's `tsconfig.test.json`.
- **Whole api-gateway vitest suite, sequential.** Evidence: scratch/evidence/suite_{d,m}.json, failnames_{d,m}.txt.
  - develop alone: 2,057 of 2,057 in 180 files, rc 0, 35 s wall;
  - merged: 2,071 of 2,071 in 181 files, rc 0, 44 s wall;
  - failure-name sets are equal (both empty);
  - the only file difference is the PR's test file, 14 cells, all passed;
  - +14 tests and +1 file, exactly the PR.
- **Test-type ratchet** (`scripts/preflight/test-types-ratchet.sh services/api-gateway services/originate`):

  | arm | rc | api-gateway | originate |
  |---|---|---|---|
  | develop | 0 | 218 files, 180 under __tests__, 15 errors, 15 baselined, 0 new, 0 stale | 327 files, 266 under __tests__, 0 errors, 0 new, 0 stale |
  | merged | 0 | 219 files, 181 under __tests__, 15 baselined, **0 new**, 0 stale | identical to develop |

  - **No new ratchet error is introduced by the PR's test file on the merged state.**
  - Planted control: a type error appended to the PR's test file on m gives rc 1, "2 new", naming `ks1936-identity-level-route-is-platform-only.test.ts(159,7)`. The file was restored by sha256.
  - (The builder's "25 baselined" was at the older develop. Live develop's api-gateway baseline is now 15.)
- **tsc** for api-gateway on m: rc 0, 0 lines. Planted control (admin.ts on m) gives rc 2, naming `services/api-gateway/src/routes/admin.ts(1727,7)`. Restored by sha256.

## Q4: the PR body. CONFIRMED, with F2
- **Round 1 text is intact.** Against gate 382's saved body (10,472 chars), the new body (14,273 chars, 14,298 bytes) has a common prefix of 3,413 and a common suffix of 7,059, which together cover all of round 1.
  - The insertion is exactly the "## Round 2 (gate 382, F1 and F5)" block, placed before "## Test Evidence".
  - The builder said 14,274; I measure 14,273 characters. Trivial, INFO.
- **The Round 2 block reads true** against my measurements:
  - one commit, admin.ts not touched;
  - 14 cells, 7 of 14 red on develop's admin.ts;
  - M1/M2/M3 each killed by 7 cells; M6 and M8 each killed by one cell;
  - the title and H2 rescoped;
  - the NOT-run list is honest;
  - develop figures are named as 387579252c12. They are not the merged state; Q3 now supplies that.
- "Refs KS-1936" is in the title. The body links the ticket. **No closing keyword**: regex hits 0, and the control "Closes KS-1936" fires.
- **The hook line is quoted verbatim**: "PREFLIGHT INCOMPLETE — 13/16 legs ran, 3 SKIPPED. Nothing failed." / "legs 3 4 8 — local stack not up ..." / "This is NOT a pass. ..."
  - Legs 3, 4 and 8 are the OpenAPI-driven legs: spec-auth conformance, path resolvability and served-spec consistency. The route is not in the spec, and this delta changes no route or spec at all. **No skipped leg bears on this change**, which is gate 382's judgement and stands.
  - The cited pre-push lines exist at head: 57-82 is the non-ff loop and refusal; 135 is the `_jr_skip=onremote` skip; 333-337 is the formatting-gate-missing refusal.
- **F2 LOW (body wording, pre-existing round-1 text): a stale claim about a sibling route.**
  - Round 1's "What is NOT done" says originate's handler "looks shadowed by the gateway's route, by reading". Gate 382 F3 found it reachable through the gateway's unauthenticated `/originate/` passthrough (proxy.ts:1282).
  - Round 1's text must stay intact, and it is not a claim that the route is fixed. But it is a soft "safe" about another route that the gate contradicted.
  - The Round 2 line "No sentence here or in the fragments describes any other route" is also slightly overstated: round-1 text still names the siblings, as unchanged and unprobed.
  - Suggested fix: one line in the Round 2 block, "the originate note below is superseded by gate 382 F3 (reachable via /originate/)". Optional; does not block.
- INFO: Test Evidence's "Touched (4 files, 186 insertions, 3 deletions)" is round-1's figure. The PR is now +220 -3, and the Round 2 "replaces" list does not name this figure.

## INFO for Wednesday (not the PR)
- The builder's tree `worktrees/s-w42-ks1936/Blockchain/Dev/node_modules/node_modules` is AGAIN an absolute link into its own tree, mtime 02:01, during the push window.
- The READY says the link was moved aside. Something (the push's deps step?) recreates it.
- s-w42-dev has none.
- Any seat copying s-w42-ks1936's node_modules inherits a cross-seat link. I moved mine aside.

## Caveats (mine)
- Nothing was posted, mailed, pushed, merged or written to Linear or GitHub. GitHub was only read; Linear was not read this round.
- No database, container or box was used.
- My probe file was run in my tree h and then moved to scratch/_quarantine. h, d and m are clean apart from the moved links.

Evidence: scratch/evidence/
- mutants_g383.{out,json}, mut_*.json
- probe_400.txt
- suite_{d,m}.{json,out}, failnames_{d,m}.txt
- ratchet_{d,m}.out, tsc_m.out, controls_g383.out
- pr.json, pr_body.txt
- build_shared_*.out

Scripts: scratch/setup_g383.sh, mutants_g383.py, suites_g383.sh, suites_g383.log, controls_g383.py, g383-probe.test.ts.
