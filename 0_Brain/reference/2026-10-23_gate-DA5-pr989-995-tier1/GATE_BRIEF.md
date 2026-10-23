# Gate brief: GATE DA5 = PR #989 (KS-973) + PR #995 (KS-741), one batched session, OPUS, TIER 1, round 1 of 2 each

Written by Wednesday at 13:26 AEDT on 2026-10-23 (shell date). **Why tier 1:** #995 changes runtime behaviour on a trust boundary (originate strips an `x-emitter-internal` header at its own inbound); #989 changes password redaction in the systemTest pre-suite/provisioning path and its follow-up commit names `BOOTSTRAP_ADMIN_PASSWORD`. Security surfaces get the full gate (2026-09-05 tiers). Verdict each PR separately; they are file-disjoint (confirm).

Both were brought up to develop today by a MERGE of develop into the PR branch (Kam 10:53: "merge and archive everything that is ready or close to being merged"), and each carries ONE follow-up commit nobody specified, made by the author seat, which you must judge on its own: #995's pins a hermetic-manifest guard for the PR's new test; #989's replaces a bare `...process.env` spread in its new test with `envWithoutSlot()`. The authors' claims: `READY_CLAIM_995.txt` (Seat G 17th) and `READY_CLAIM_989.txt` (Seat G 18th) beside this brief. Read both WHOLE; their measurements are the authors': re-measure the load-bearing ones.

**Heads (Wednesday's `git ls-remote origin` at 13:2x AEDT):** develop `39016e29898a64c56209d7ef01e4b6bc1b51f5c0`.
- #995 head `d89eab06b150ce9eb3e8b0b6d73e1fb186b803f0`; the author's re-prediction on this develop: clean, landing tree `2aca8639872d37eee190d53fdd8bf04514d846dc`, six files.
- #989 head `eb0f470b685100af865e6c0cb0474a4400c44161`; it already contains develop; tree `bbe3fc31718824e1c45b0df93103b40ff67cde1c`, five files (`systemTest/fixtures/pre-suite.ts`, `provision.ts`, three new test files).
ls-remote both heads and develop at start and end; derive both landing trees yourself on LIVE develop.

**Project:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` is READ ONLY. Clone INSIDE `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/f30afbb4-9b45-43f4-9b2a-53bb682e8a53/scratchpad/gate_da5/` via `git clone --shared /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src <that dir>/src`; fetch develop and `refs/pull/989/head`, `refs/pull/995/head` from the Secuura origin (read-only use of the project's deploy key via GIT_SSH_COMMAND is what the DA3 gate did; do not copy the key). npm ONLY with an explicit `--prefix` inside your clone. **Time-box about 45 minutes; the weekly allowance is at 99%: be lean, and say what you did not run.**

**Verdict file:** `verdict.md` in this folder. First TWO lines: `VERDICT #995: <GO|GO WITH NOTE|NO GO> at head d89eab06b150... (tier 1, round 1 of 2; landing tree <sha> on develop <sha>; N blockers, M notes)` and the same for `#989` at `eb0f470b6851...`. Then BLUF, findings per PR, FOUND / TESTED / HOW, NOT RUN, wall-clock. **Last line, written LAST:** the sha256 of `sed '1,2d;$d' verdict.md | shasum -a 256`, labelled with exactly that command; recompute from stdout after writing.

**Rules:** findings only; no GitHub or Linear writes; nothing written under `!CODING`; no push; no `cd`; no `rm` outside your clone; no stderr to /dev/null; no Docker; no installs outside your clone; every zero with a positive control from a DIFFERENT family; red by ASSERTION; mutants run before they count; restore asserted by sha256. Write NOTHING in `/Volumes/DevMASTER/WEDNESDAY` except `verdict.md`; report untracked paths outside 0_Brain/, 5_Project_History/, 2_Project_Files/local-model/, 2_Project_Files/fleet/briefs_staged/.

## Questions — #995 (KS-741), the security one
1. **What the strip does, from the code:** where in originate's middleware order the strip runs relative to every reader of `x-emitter-internal` (and of the gateway-provenance headers) — read every reader, including ones added on develop since the PR's base. Could a request reach a reader BEFORE the strip? Could the strip remove a header a legitimate internal caller (the gateway, the emitter) relies on, breaking a real path? Name the internal callers that set it and show whether they reach originate through the stripped inbound.
2. **The conflict resolution** (import block union in `originate/src/index.ts`): correct, and does the merged file wire the strip exactly once?
3. **Red-first:** the PR's seven new tests fail by ASSERTION with the strip removed (a mutant), pass with it restored. Whole originate suite develop vs head BY CELL NAME: 0 vanished, 0 pass-to-fail (the author: 1,643 -> 1,650).
4. **The unasked follow-up commit** (hermetic-manifest pin + SUBJECTS line): correct for the guard's two checks (MANIFEST-DRIFT and CONFIGPINNED)? Show the guard red without it.
5. Anything a security reviewer (Peter) would flag: header-name case handling, arrays/duplicates of the header, a prefix variant, logging the stripped value.

## Questions — #989 (KS-973)
6. **Redaction:** does the PR redact the generated password everywhere the pre-suite/provision path can echo it (server error bodies, transport errors, logs), including develop's new code in `provision.ts` (transport errors name their port; bootstrap login returns its status)? Find a path that still prints it, or show none exists by reading every output site.
7. **The new tests can fail:** a mutant that stops redacting reddens them by assertion.
8. **The unasked follow-up** (`envWithoutSlot()` with `SECUURA_STACK_SLOT` and `BOOTSTRAP_ADMIN_PASSWORD` named): correct for develop's slot-independence guard, and does naming `BOOTSTRAP_ADMIN_PASSWORD` in a child env expose the password anywhere it was not exposed before (logs, argv, a fixture file)?
9. Suites develop vs head BY CELL NAME (author: 1,422 -> 1,431; typecheck and lint rc 0).

## Not covered
Say what you did not run: the hook's skipped legs 3, 4, 8 (no stack), any live endpoint, integration.
