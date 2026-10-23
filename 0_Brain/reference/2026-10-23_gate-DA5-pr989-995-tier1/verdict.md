VERDICT #995: GO WITH NOTE at head d89eab06b150... (tier 1, round 1 of 2; landing tree 2aca8639872d37eee190d53fdd8bf04514d846dc on develop 39016e29898a64c56209d7ef01e4b6bc1b51f5c0; 0 blockers, 4 notes)
VERDICT #989: GO WITH NOTE at head eb0f470b6851... (tier 1, round 1 of 2; landing tree bbe3fc31718824e1c45b0df93103b40ff67cde1c on develop 39016e29898a64c56209d7ef01e4b6bc1b51f5c0; 0 blockers, 3 notes)

# Gate DA5, tier 1, round 1: PR #995 (KS-741) and PR #989 (KS-973)

Gate seat: Opus subagent. Shell clock 13:27:09 to about 13:37 AEDT, 2026-10-23.

## BLUF

- **#995 does what it says.** Originate now deletes `x-emitter-internal` on every request, mounted once, after the vouch middleware and ahead of every router that could build an anchoring hop. No reader of the marker exists in originate. The only setters are originate's own outbound hops to anchoring, so the strip breaks no legitimate path, and C4 shows the genuine `originate-create` marker still arrives. The full originate suite went from 138/1,643 to 139/1,650 passed, with 0 vanished and 0 pass-to-fail by cell name. The follow-up commit is correct for both guard checks: each check goes red by assertion when its half of the commit is removed.
- **#989 does what it says at the one site that interpolates a server message.** I read every output site in the pre-suite/provision path, including develop's transport-error and bootstrap-status code, and found none that prints the generated password in cleartext. The new tests go red by assertion under two different mutants. The follow-up `envWithoutSlot()` commit is correct and exposes nothing new. The suites went from 81/1,422 to 84/1,431 (0 vanished, 0 pass-to-fail). Lint (tsc both configs plus oxlint) returned rc 0.
- **The notes, by weight:**
  1. #989: the redaction is cosmetic against a careful reader. The generated password is `Ks256-<key>-<seed>-Pw!`, and the redacted message itself prints the key and the email `ks256-<key>-<seed>@…`.
  2. #995: anchoring's edited comment over-claims ("the only value that can arrive here is one originate itself set"). Anchoring has no inbound strip, and it sits on the same flat compose network the PR cites for originate.
- Heads were unmoved from start to end (ls-remote at start and at 13:35). The two PRs are file-disjoint: #995 touches six files under `Blockchain/Dev/services/`, and #989 touches five files under `systemTest/`.

## Findings — #995 (KS-741)

**Q1: strip placement and readers.** I read `originate/src/index.ts` on the landing tree. The order is: helmet, cors, overloadProtection, json, urlencoded, rejectNulBytes, `/health`, `GET /api` (static JSON), then `createGatewayProvenanceMiddleware` at :219, then `createEmitterMarkerStrip()` at :223, then every `/api/*` router from :266 on.
- Only `/health` and `GET /api` run before the strip. Neither reads or forwards trust headers: `git grep header` over `routes/health.ts` returned 0.
- Readers of `x-emitter-internal` across the whole landing tree: only `anchoring/src/index.ts:531`, a different service. Nothing in originate reads it.
- Setters: only `originate/routes/documents.ts:878` (`originate-create`) and `:1375` (`originate-lifecycle`), both outbound to anchoring. No service, nginx config or script sends the marker *to* originate (I grepped `.conf`, `.py`, `.sh`, `.yml` and `.yaml`). The gateway strips `x-emitter-*` on `/api/*` anyway.
- So the strip cannot break a real path. C4 is the runtime positive: the genuine outbound marker reaches the recorder.

**Q2: conflict resolution.** Against develop, the merged `index.ts` changes only the import block (+5/-1, the union of the PR's name and develop's `resolveRequestTenantId` line) and the 4-line mount block. `createEmitterMarkerStrip()` appears once (count 1, against `createGatewayProvenanceMiddleware(` count 1 as a control). The resolution is correct, and the strip is wired exactly once.

**Q3: red-first.** The brief's premise does not hold: not all seven tests can redden when the strip is removed. Five of the seven go red by assertion across two mutants; the other two are green by design.
- Mutant M1, strip body made a no-op (`void req;`): C1, C2 and C5 go red with `Received: "forged-by-client"`; the other four stay green. My first attempt, which deleted the line outright, failed to compile (TS6133), not by assertion, so I did not count it.
- Mutant M2, the `app.use(createEmitterMarkerStrip())` mount removed from `index.ts`: C6a and C6-CONTROL go red (`Expected > 0, Received -1`).
- Restore was asserted by sha256 (`shasum -c` OK) for `gatewayProvenance.ts` and `index.ts`.
- **C3 and C4 never redden under strip removal.** C4 is a positive control by design. C3 passes with the strip disabled because `routes/anchors.ts` builds explicit headers, so C3 guards anchors.ts and does not discriminate for the strip.
- Full suite on develop vs landing, by cell name: 138 suites / 1,643 passed → 139 / 1,650 passed, rc 0 both sides. 0 vanished, 0 pass-to-fail, 7 new cells (exactly the ks741 cells).

**Q4: the unasked follow-up `d89eab06b150`.** It is correct for both guard checks.
- Removing the import-scope pin line from the ks741 test turns CONFIGPINNED red by assertion, naming `ks741-emitter-marker-strip.test.ts` ("sets no IMPORT-SCOPE ANCHORING_SERVICE_URL base"). MANIFEST-DRIFT stays green.
- Removing the SUBJECTS line turns MANIFEST-DRIFT red, naming the file. CONFIGPINNED stays green.
- Restored, both files' sha256 checked OK, and the guard passed 10/10.
- The value `http://127.0.0.1:2` is the ECONNREFUSED shape the guard requires, not the bad port `:1`. Accept the commit.

**Q5: what a security reviewer would check.** I measured each item over a raw TCP socket against the real `createEmitterMarkerStrip` through tsx, with a no-strip app as the positive control.
- Case: `X-EMITTER-INTERNAL` and `X-Emitter-Internal` are both stripped. The no-strip control kept both as `"forged"`.
- Duplicates: two headers arrive joined as `"a, b"` and are stripped together.
- Prefix: `x-emitter-internal-x` is not stripped by originate. This is harmless, because anchoring reads only the exact key and the gateway strips the `x-emitter-*` prefix.
- `req.rawHeaders` still holds the marker after the strip. `git grep rawHeaders` over `Blockchain/Dev/services` found 0 readers today. This is a theoretical bypass for a future rawHeaders forwarder only.
- Logging: the strip logs nothing, so the value is never echoed.

**Notes on #995**
- **N1, comment over-claim (the most important).** The edited comment at `anchoring/src/index.ts:525-530` says the marker cannot be spoofed and that "the only value that can arrive here is one originate itself set on its outbound hop". That holds only for paths through the gateway or originate.
  - Anchoring has no inbound strip; its middleware is helmet, cors, json, rejectNulBytes, requestLogger, then jwtAuthenticate.
  - `docker-compose.yml` treats anchoring exactly as it treats originate: both are on the flat network with host ports unpublished (`:1286` vs `:557`). That is the same exposure the PR uses to justify the originate strip.
  - So a direct compose-network caller holding a connector JWT can set the marker and suppress its own flat-anchor provenance row.
  - This is pre-existing and not introduced by this PR. Reword the comment, or open a ticket for an anchoring-side guard.
- **N2.** C3 does not test the strip (see Q3). The PR body should not count it as a red-first cell for KS-741.
- **N3.** C6 checks the mount's order only against `/api/anchors`. A move to between `/api/documents` (:275-276, which also builds a marked hop) and `/api/anchors` would pass C6. This is minor; today the order is correct.
- **N4.** rawHeaders retention and the prefix variant, as described under Q5. No action needed now.

## Findings — #989 (KS-973)

**Q6: every output site.** I read `provision.ts`, `pre-suite.ts`, `provision-actors.ts`, `describe-error.ts` and `login-outcome.ts` at the head.
- Only one site interpolates a server-supplied message: `provision.ts:342-343`. It is now `redactSecrets(…, [spec.password])`.
- Develop's new code is clean:
  - The transport rethrow at `provision.ts:129` interpolates the URL and `describeError(err)`. `describeError` walks only `message`, `errors` and `code` down the cause chain, never the request body.
  - `bootstrapToken` returns only `{status, transport}`.
  - `login-outcome.ts` builds its text from status and where. The bootstrap password is never interpolated.
  - `createAsAdmin` and `login` return null without printing anything.
- The remaining console sites (`provision-actors.ts` :80, 186, 244, 274, 291, 343, 354, 380, 388 and `pre-suite.ts` :66, 115-125, 139, 187) print the seed, emails, roles, URLs and statuses, never a password.
- Child-process check: I ran the real `pre-suite.ts` with `BOOTSTRAP_ADMIN_PASSWORD=unused-port-1-refuses-first` against `127.0.0.1:1`. Python counted 0 occurrences of the value in stdout+stderr. The different-family control, `admin@secuura.com`, counted 1, and the banner was present.
- One pre-existing exposure by design: the manifest `generated/actors.json` stores passwords in cleartext (gitignored).

**Q7: the tests can fail.**
- Mutant R1, `redactSecrets` made a no-op: 3 of 5 go red by assertion. The unit test fails with `expected 'pw=hunter2…' to be 'pw=[REDACTED]…'`, and both the provisionActor cell and the runPreSuite banner cell fail with `not to contain 'Ks256-owner-s227-redaction-Pw!'`.
- Mutant R2, the call site un-redacted with the function intact: those last two cells go red.
- The two CONTROL / empty-secret cells stay green as designed.
- Restore asserted by sha256 OK.

**Q8: the unasked follow-up `eb0f470b6851`.** It is correct. With the pre-follow-up version of `preSuiteStreams.test.ts` restored (from `eb0f470b6^`), `unitSuiteSlotIndependence` goes red by assertion: "no test file spawns a child on a bare process.env spread", naming `tests/unit/fixtures/preSuiteStreams.test.ts`. Restored, sha256 OK, 12/12 pass.
- `BOOTSTRAP_ADMIN_PASSWORD` was already named in the child env before the follow-up, as an unchanged context line. It is a dummy literal, passed in env and not in argv. `envWithoutSlot` spreads `process.env` minus the slot keys and then applies the override, so the dummy replaces any real shell value.
- The child printed the value 0 times (see Q6). No fixture file is written with it. The follow-up exposes nothing new. Accept it.

**Q9: suites.** `systemTest/performance` unit run, develop vs head: 81 files / 1,422 passed → 84 / 1,431 passed, rc 0 both sides. 0 vanished, 0 pass-to-fail, 9 new cells (exactly the three new files' cells). `npm run lint` on the head (check-installed, then tsc on both tsconfigs, then oxlint `--type-aware --deny-warnings`) returned rc 0.
- My own faults, both re-run clean:
  - My first suite run lacked the `systemTest/oxlint` install. `lintConfigContract.test.ts` failed to load on both sides with the same 18 cells. I installed it in the clone and re-ran.
  - My first lint run was concurrent with the unit run in the same tree. tsgolint panicked on a ks1300 canary temp file. Run alone, lint returned rc 0.

**Notes on #989**
- **N1 (the most important): the redaction can be undone by derivation.**
  - `actors.ts:98`: `buildPassword = \`Ks256-${key}-${seed}-Pw!\``.
  - The redacted message names `"${spec.key}"` and `spec.email` = `ks256-<key>-<seed>@secuura-test.invalid`, and the new test *asserts* both are present. `provision-actors.ts:246` prints the seed outright.
  - Anyone reading the DEGRADED banner can therefore reconstruct the password.
  - Impact is low: these are test accounts on undeliverable addresses, provisioning against a remote host is refused without `ALLOW_REMOTE_PROVISION`, and the manifest holds the passwords anyway.
  - This is outside item 6's literal scope ("cleartext in the banner"). It is worth a ticket, either a non-derivable password (seed plus a random component) or an honest comment saying the redaction is cosmetic.
- **N2.** Matching is exact-substring. An echo that JSON-escapes, URL-encodes or HTML-escapes the password would not match. The fixed parts of the password (`Ks256-`, `-Pw!`) need no escaping, but `--seed` is caller-supplied, so a seed containing `"` or `\` would escape in a JSON echo. This is an edge case.
- **N3.** The conflict at `pre-suite.ts` is correct: against develop, the head adds only the 4-line comment above `invokedDirectly`. Develop's `manifestReport` block is intact.

## FOUND / TESTED / HOW

- **Heads:** I ran `git ls-remote` against the Secuura origin (deploy key used read-only through `GIT_SSH_COMMAND`, not copied) at the start and at about 13:35. develop was `39016e29898a`, #989 `eb0f470b6851` and #995 `d89eab06b150` both times.
- **Landing trees:** derived with `git merge-tree --write-tree` on live develop: #995 `2aca8639872d…` (matches the author's re-prediction), #989 `bbe3fc31718824…` (its own tree; develop is an ancestor). #995's landing tree differs from develop in exactly its six files.
- **Clone:** `git clone --shared` of the spark cache into `scratchpad/gate_da5/src`, with three detached worktrees: develop, #995 landing (a local commit-tree of `2aca86`, never pushed), and the #989 head.
- **npm:** `npm ci --prefix` only, inside the clone: Blockchain/Dev `--workspace services/originate --workspace packages/shared --ignore-scripts`, a manual `tsc` build of shared, then systemTest/performance and systemTest/oxlint.
- **Tools:** jest `--json` for originate, vitest `--reporter=json` for performance, cell-name diffs by python `-I`, mutants by `sed` with a sha256 restore after each, and a raw-socket header probe through tsx (the probe file was removed and the worktree is clean).
- **originate on the landing tree:** `tsc --noEmit` rc 0.

## NOT RUN

- The hook's skipped legs 3, 4 and 8 (no stack). No live endpoint, no Docker.
- Originate integration (`jest.integration.config.js`, DB-backed), the anchoring vitest suite, and the api-gateway tests. The `trustHeaders.ts` and anchoring changes in #995 are comment-only (I read the diffs).
- Originate `npm run lint`: eslint could not load `@eslint/js`, because my workspace-scoped install skipped the root devDeps. Environment only; not a finding.
- Schemathesis, k6, Playwright, Akto, the format gate, prettier. I did not check the author's format-gate EPIPE defect claim.
- No full repo install. No re-check of either PR body.
- The Secuura project checkout already shows 3 untracked files under `systemTest/akto/` that I did not create; I read it only.
- WEDNESDAY tree: no untracked paths outside the allowed folders (`git status` filter rc 1 = none); the only file I wrote is this one.

## Wall-clock

From 13:27:09 AEDT (brief read) to about 13:37 AEDT by the shell clock, inside the 45-minute box.

sed '1,2d;$d' verdict.md | shasum -a 256: be2f26d014ae8997aad68ae349cebeae16f3f936957c3df1a6390516b5a25af9
