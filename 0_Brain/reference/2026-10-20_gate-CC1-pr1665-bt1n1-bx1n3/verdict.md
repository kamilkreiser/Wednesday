VERDICT: GO at head a404df30d1ce... (tier 2, round 1 of 2; landing tree 91a915deca6598f8456d544ce9c9a3950b1bae39 on develop 7e3b9362e08b1b5b2c418f43e05c9bd0616f896e; 0 blockers, 2 notes)

## BLUF
Tier 2 holds: three files, zero product files, test-only. The new auth file has six cells, all green. Four of the six arms I ran went red by assertion in exactly the cells the author named. The other two arms survived, and both survivals match the author's disclosed bound. Counts reproduce exactly. The landing tree reproduces on live develop. No blocker. Two notes are below, and neither needs a change to the PR.

## Heads (ls-remote against GitHub)
- Start (02:17Z) and end (02:22Z): develop 7e3b9362e08b1b5b2c418f43e05c9bd0616f896e, refs/pull/1665/head a404df30d1cdc82a236321930353e634213ffce4. Both equal the claim and neither moved.
- I fetched with the project deploy key, read-only, into the scratchpad clone. I pushed nothing.

## Findings

Q1 Scope (three-dot `gh/develop...pr1665`): 3 files, +384/-0, all 'A' or 'M'.
- BACKLOG.md (+26)
- services/auth/src/__tests__/ks1157-the-marker-at-the-route-and-across-a-rotation.test.ts (new, +333)
- services/originate/src/__tests__/ks1659-a-connector-certifying-with-no-holder.test.ts (+25)
- No product file is touched. Tier 2 is confirmed.

Q6 Landing: `git merge-tree --write-tree gh/develop pr1665` returned rc 0 and tree 91a915deca6598f8456d544ce9c9a3950b1bae39. That is identical to the claim, computed against live develop 7e3b9362e08b.

Q2 The new file's six cells by NAME (all pass, 13/2/2/2/11/1 ms):
1. GAP KS-1157 X1 (password login creates its session with NO marker argument)
2. GAP KS-1157 X1b (password login naming deviceId and clientType is STILL unmarked)
3. GAP KS-1157 X3 (the authorization_code grant IGNORES a caller-supplied mintedBy)
4. CONTROL KS-1157 XC1 (the harness reaches BOTH handlers and both mint)
5. GAP KS-1157 X2 (rotateSessionRefreshToken rewrites the session and the oauth marker SURVIVES)
6. CONTROL KS-1157 XC2 (an UNMARKED session stays unmarked across the same rotation)

Isolation first, then the whole suite, as briefed:
- Isolated run of the six guards plus the new file (ks949, ks1186, ks1188, ks999, s130-f6, ks488, ks1157-the-marker): 11 files, 84 tests, 0 failed, rc 0.
- Whole auth suite with the file: 105 files / 1132 passed / 0 failed, rc 0.
- Whole auth suite without it (`--exclude`): 104 files / 1126 passed / 0 failed, rc 0.
- Timeouts: I saw no failure in any run, so there is no elapsed time to read against 5000 ms. The author's non-determinism (2, 10, 0 failed) did not reproduce in my two whole-suite runs and one isolated run on this machine.
- The absence of a failure is not proof it cannot happen. See note N1.

Q4 Counts by cell NAME (the sorted verbose name lists were diffed):
- auth: 6 names only in the with-file run, 0 only in the without-file run, so 0 vanished.
- originate, whole jest suite on the PR tree: 135 suites, 1576 tests, 0 failed. With ks1659 reset to the develop version: 135 suites, 1575 tests, 0 failed.
- originate: the sole name added is "GAP KS-1659 N3: a HUMAN caller who named no holder keeps owner_user_id = its OWN uuid ...", with 0 vanished.
- The four platform suites were NOT run. They need the stack on :6882 and I ran no Docker. The PR changes no runtime surface.

Q3 Arms. Each was run in this order:
- tsc --noEmit -p <service>/tsconfig.json on its own, rc 0
- the cell run
- the product file restored from the PR tree, with sha256 equality asserted. It was equal in every arm, and `git status` of the clone was clean at the end.

| Arm | Mutation | tsc | Result |
|---|---|---|---|
| A1 (author's X1, reproduced) | password-login createSession gets 'oauth' | rc 0 | RED by assertion: X1 (`expected [undefined,'browser','oauth'] to deeply equal [undefined,'browser']`) and X1b; 2 failed / 4 passed |
| A2 (author's social-site survivor, reproduced) | social-login createSession gets 'oauth' | rc 0 | SURVIVES, 6/6 pass, which confirms the bound |
| G1 (author's, reproduced) | `holder.id === issuer.id ? null : ...` in certificationRepo | rc 0 | RED by assertion in N3 only (`Expected "a0000000-...0010", Received null`); 7 of 8 pass |
| A4 (mine) | rotation INVENTS the marker (`session.mintedBy='oauth'`) | rc 0 | RED: XC2 only |
| A6 (mine) | rotation DROPS the marker (`delete session.mintedBy`) | rc 0 | RED: X2 only |
| A5 (mine) | register-site createSession gets 'oauth' | rc 0 | SURVIVES, 6/6 pass |

- The disclosed bound holds, and the real gap is wider than the author wrote. The author named the social site. My A5 shows the register site passes every cell too, and the platform-admin site is also not driven. Only the password site is covered. The file header says "X1 covers the PASSWORD login site only ... four call sites", so the header is accurate and this only widens the examples.
- A5's "survives" has a limit. I confirmed the edit compiled (tsc rc 0), but I did not diff the mutated file. I located the edit by script as the first createSession call. I am recording this and not claiming more than that.

Q5 The author's finding is correct.
- `git ls-tree` on develop shows tsconfig.test.json only in api-gateway, auth, vc-issuer and systemTest/api-explorer. `services/originate` has none.
- `package.json` `check:test-types` runs `scripts/typecheck-tests/check.cjs` for services/auth, api-gateway and vc-issuer only. Baselines exist for those three alone.
- originate's own tsconfig.json excludes `src/__tests__` and `*.test.ts`, so `tsc -p` over it never sees a test file.
- Own-program check of the changed originate test file: temp tsconfig in the scratchpad extending originate's tsconfig, with `exclude: []`, includes only the ks1659 file, types jest and node. tsc rc 0. Positive control: appending `const __pc: number = "x"` gave rc 2 with TS2322 and TS6133. Restored, sha equal.
- Auth through the gate's own checker, `check.cjs services/auth`: "tsc examined 156 files, 105 of them under __tests__; 42 errors: 42 in the baseline, 0 new". Positive control: the same appended line gave rc 1 with "44 errors: 42 in the baseline, 2 new", both in the new file. Restored, sha equal.
- The 105 files under __tests__ equals the 105 test files in the suite, so the new file is inside leg 16's corpus. The author's 0-new figure reproduces.

## Notes
N1 (non-blocking). The auth suite's timeout non-determinism did not reproduce for me (2 green whole-suite runs, 1 green isolated run). The BACKLOG entry is honest that it is "not purely pre-existing". Its figures (2, 10, 0 failed; 5002-5766 ms) cannot be re-measured from a green run, so I take them as the author's observations, not mine. The entry files the follow-up correctly, and a red in a file this PR does not touch after merge is the thing to read first. I did not check that the cited KS-1155 and kyc db.retry entries exist; the only line I read in BACKLOG.md is the diff.
N2 (non-blocking). The social-site and register-site gap above. If the denylist target set matters for those sites, they want a cell later. The PR states the limit in the file header, so nothing is hidden.

## FOUND / TESTED / HOW
- FOUND: the PR is test-only, and the claimed landing tree reproduces. The six auth cells and the one originate cell are additive. Each is red by assertion on its named mutant, with no collateral on the arms I ran.
- TESTED: the isolated guards, both auth whole-suite runs, both originate whole-suite runs, six mutant arms, two type-check programs with positive controls, merge-tree, and ls-remote at both ends.
- HOW: scratchpad clone `gate_cc1/src`, shared from the cache and fetched from GitHub; `npm ci --ignore-scripts` with `--prefix`; packages/shared built first; vitest and jest run via `npm --prefix`.

## NOT RUN
- The four platform suites (stack on :6882, no Docker).
- The arm for the author's X3 (body-read of mintedBy) and for X2 through the refresh route. I ran my own rotation arms instead (A4, A6).
- Preflight legs 3, 4 and 8, which need the local stack. I have no view of the in-hook preflight.
- Any GitHub or Linear read of the two ticket comments.
- Anything under `!CODING`, which I did not touch.

## Wall-clock
About 5 min from clone to verdict (258 s from npm ci to the last check at 02:22Z).

## Hygiene
`git -C /Volumes/DevMASTER/WEDNESDAY status --short` shows no untracked path outside 0_Brain/, 5_Project_History/, 2_Project_Files/local-model/ and 2_Project_Files/fleet/briefs_staged/. The only file I wrote there is this verdict.md.
sha256 of `sed '1d;$d' verdict.md | shasum -a 256`: c664ef5672b91b1bfc0864ff26ee11ee69cb410993af27b717bfdca7cb506073
