VERDICT: GO WITH NOTE at head 4521a6f629b0c669ffbbe47798ebdcfb830d231b (tier 2, round 1 of 2; landing tree 46d3e6b7a9a089370db16fd9bad31720ade3e632 on develop 8323f2f70cd796219774f240184f777813c28aec; 0 blockers, 3 notes)

GATE AD1, PR #1618 (KS-1642), Sonnet, 2026-10-19. All runs in my own clone under scratchpad/ad1/repo (fetched develop + refs/pull/1618/head; nothing written under !CODING, no GitHub/Linear writes).

## Heads (re-read at start and again before this verdict)
- `git ls-remote origin`: develop 8323f2f70cd796219774f240184f777813c28aec both times (unchanged); refs/pull/1618/head 4521a6f629b0c669ffbbe47798ebdcfb830d231b both times. Merge-base 80868551e679.
- Three-dot list is exactly 3 files, +70/-0: idNamespaceCollision.ts (+3), ks1642-...-unreadable-error-shape.test.ts (+53, new), ks1612-409-mapping-...test.ts (+14). Matches the claim.

## Q4 Landing
- `git merge-tree --write-tree develop pr1618` = 46d3e6b7a9a089370db16fd9bad31720ade3e632; a real merge in my clone gives the same tree, no conflicts. Matches the prediction.
- Built packages/shared, `npm run generate --workspace=services/originate` (OK), after a clean `npm ci` from the landing lockfile.
- tsc --noEmit on the landing tree: rc 0, 0 bytes. Positive control: a planted `const x: number = "s"` file made the same command print TS2322 (control file is in my scratch only).
- Originate unit suite on the landing tree: 123 suites / 1488 tests passed, rc 0. Develop alone: 122 / 1481, rc 0. +1 suite, +7 cells (5 + 2). Claim confirmed.

## Q3 Red-first and mutant kill
- Piece 1: new test file at develop's idNamespaceCollision.ts (blob bb0cd29d): 3 failed (G1, G3, G4, each with the thrown "ks1642 unreadable" error, i.e. the right cause) and 2 passed (H10, C1 controls); the ks1612 suite alongside was 15/15. With the PR's file restored (blob d7d3670b) ks1642 + ks1612 = 20/20.
- Piece 2: `r.constraint === null &&` is on line 87 (confirmed with grep; line 84 is the pre-patch position). Deleting it (blob aa55d3f1, moved) turned ks1612 to 1 failed / 14 passed / 15, the one failure being "RED KS-1642 H9"; H9c stayed green. Restored byte-identical (cmp against the saved copy; blob d7d3670b again). Claim confirmed.

## Q1 Does the guard change any answer for a READABLE error?
- Differential run of develop's helper vs the PR's over 30,000 seeded random readable shapes (both predicates = 60,000 comparisons; mixed code/originalCode/constraint/message, nested cause incl. non-enumerable, meta.driverAdapterError, arrays, cycles, null-prototype, readable getters, primitives): 0 differences. Positive controls: 44,999 of the old answers were `true` (so the corpus does exercise the match path), and a Proxy with a throwing ownKeys gives old = THROW, new = false (the comparison can see a difference).
- Callers, by `git grep` at the PR head: one production caller, `services/originate/src/routes/documents.ts:743-744` (inside `catch (saveErr)` around saveDocument). The other users are tests: ks1612-409-mapping (unit; passes), ks1612-051 and ks1612-documents-id-namespaces-disjoint (both `.integration.test.ts`, not run, see NOT-RUN), and the new ks1642 file.

## Q2 Is "unreadable means not a collision" the right default
- Yes. At documents.ts:743-745 a false answer falls through to `throw saveErr`, so the original DB error surfaces on its existing path (the outer catch's 500). Before the PR, an unreadable node made the helper itself throw from inside the catch block, replacing saveErr with the helper's own error. No caller swallows an error it previously surfaced; the change only stops masking saveErr. A false "collision" (a spurious 409) is the unsafe direction and cannot arise from an unreadable node.

## Notes
1. The "old never-throws comment is replaced" statement (brief and the author's CLAIM) is not what the diff does: it is +3/-0 and line 56 still reads "Nothing here throws on an unexpected shape" (now true, but untouched); the new test header quotes it as the broken promise. Cosmetic.
2. An unreadable node is skipped whole, including its subtree: an outer error whose `code` getter throws but whose readable `cause` holds a real 050 refusal answers false (measured, control: the refusal alone answers true), so that rare wrapped shape maps to the 500 path instead of 409. It threw before (also a 500), so no regression and the safe direction; no cell pins it.
3. The up-front read is a probe, not a snapshot: fields are read again after the `try`, so a stateful getter that throws only on its second read would still throw. Not reachable from driver errors; no cell covers it.

## NOT-RUN
- DB-backed integration suites (jest.config.js ignores `.integration.test.ts`; no database/Docker): ks1612-051-...integration, ks1612-documents-id-namespaces-disjoint.integration, ks1402-...connector-actor.integration. The two ks1612 integration files import these helpers.
- Author's preflight hook (13/16 legs) and shell suites: not re-run. Docker legs not run (rules).
- Other workspaces' suites (api-gateway, anchoring, etc.) and lint: not run; the PR touches only services/originate.
- GitHub-side state (PR body, checks, KS-1642 comment): not read, no GitHub access used beyond ls-remote/fetch.
- Authenticity of the author's own logs: not consulted; every figure above is from my runs.
4e6a0a77ccab73306d38b17a02887d22a5425cd2335ec26effbc4de2f84f88f3
