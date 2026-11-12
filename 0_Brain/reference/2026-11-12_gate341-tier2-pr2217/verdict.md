PR 2217: GO (at head 7b77e16a6e34; tier 2; round 1)

Gate 341, tier 2 (Sonnet), 2026-11-12 about 22:2x AEDT. Findings only: nothing pushed, commented, ticket-written, merged or mailed. All write verbs ran in `scratch/` of this folder (`scratch/repo`, push URL DISABLED, fetched over https with the Blockchain project's own gh credential, a READ use). The project checkout was touched only by `ls-remote`, `config --get`, and read-only use of an existing worktree's `tsc` binary. Never `cd`.

**Pins.** Start and end (ls-remote): develop bba80c3c8e241570ba21c0cbe47dc75ad4b5fd2c, refs/pull/2217/head 7b77e16a6e34eb0f41594fc16215167f0fabc950. NEITHER MOVED. PR: open, not draft, MERGEABLE, base develop, 1 commit (parent 13e62febfba8), `closingIssuesReferences` empty, 3 files +25 -0.

## Answers

**Q1 Scope: YES.** `git diff --numstat 13e62febfba8 pr2217`: test-helpers.ts 4/0, cheat fragment 4/0, flow fragment 17/0 (3 files, +25 -0, all `M`/`A`, no delete or rename). The only code hunk (`@@ -72,6 +72,10 @@`) adds two `//` comment lines plus `created_at?: string;` and `timestamp?: string;` inside `interface AgentMailMessage`, after `received_at`. No added line contains `export`, `function` or `=>` (count 0); the date line (117 at head) is untouched. No runtime line, export or product byte.

**Q2 tsc leg reproduced: YES.** TypeScript 5.9.3 (`Dev/node_modules/.bin/tsc` of an existing worktree), flags `--noEmit --target es2022 --module esnext --moduleResolution bundler --skipLibCheck --strict --types node --typeRoots <Dev>/node_modules/@types`, run on scratch copies outside every worktree with a node_modules symlink beside them:
- parent (13e62febfba8): rc 2, exactly two errors, (113,59) TS2339 `created_at` and (113,77) TS2339 `timestamp`.
- head: no output, rc 0.
- control (head with `msg.created_at` on the date line changed to `msg.zzz_planted`): rc 2, exactly one error, (117,59) TS2339 `zzz_planted`. So the check reads the file and a undeclared member is caught.

**Q3 Honest about runtime: YES.** Code comment says "Optional and type-only: whether the mail API really sends these two fields is not measured." Body and both fragments say the same ("without claiming the API returns them"; "Not measured here. Which date fields the mail API really returns"). Nothing claims the API sends the fields. The body also correctly says the proof is a hand-run check, not a repo gate. Reader check: `git grep AgentMailMessage` under tests/e2e at head finds exactly test-helpers.ts and email-notifications.prelaunch.spec.ts (matches the body); 20 files contain the import path `fixtures/test-helpers` (matches). The comment line is long but a type-only comment.

**Q4 Merge: YES.** `git merge-tree --write-tree origin/develop pr2217` rc 0, tree 657d6995830b; in that tree test-helpers.ts blob = the PR's (6ae52a56f96e) and packages/shared audit-logger.ts blob = develop's (29569eea3a92), i.e. both sides survive; merged vs develop = 3 files, +25 -0. Develop move 13e62febfba8..bba80c3c8e24 = 2 files (packages/shared audit-logger.ts and its ks1923 test), nothing in tests/e2e or the fragments. Census: GraphQL over all pages, 102 open PRs, none truncated at 100 files; paths of this PR touched by 2217 only (fixture, anything under `Dev/tests/e2e/`, the KS-2029 fragments). Positive controls: the detector finds 2217 itself on the fixture and finds `services/api-gateway/src/index.ts` -> 2125, and "any file named test-helpers.ts" -> 2217. No other open PR touches the fixture.

**Q5 Body: YES.** Title `Refs KS-2029: ...`; first body paragraph begins "TIER 2: test-only and type-only ..."; only reference is KS-2029 (`Refs`; my regex for close/fix/resolve forms finds none); `closingIssuesReferences` empty. It states no repo-defined leg type-checks tests/e2e (and that eslint does not cover it). Fragment pair present (flow +17, cheat +4) and their text agrees with the body.

## Findings

**G341-2217-1 (Note): no repo gate type-checks tests/e2e.** The two TS2339 sat unseen for that reason and nothing in the repo prevents a recurrence; the PR discloses it (body, fragments) and files nothing. Board-seat follow-up, not a blocker.

**G341-2217-2 (Note): proof is ad hoc and head-only on a moved base.** The seat's legs ran on 13e62febfba8, not bba80c3c8e24; I re-ran the tsc leg on the file extracted from the PR head, and the merged tree's fixture blob is identical to the head's, so the result carries to the merge. The Playwright types came from the root install (1.61.1), not the e2e package's own `^1.40` resolution; stated in the body.

**G341-2217-3 (Info): no spec type-checked.** email-notifications.prelaunch.spec.ts (the one other reader) was not checked by the seat or by me; adding optional members only widens the type, so a new error there is not expected, but unmeasured.

No Major or Minor finding.

## NOT TESTED

- Type-checking any spec file under tests/e2e (including email-notifications.prelaunch.spec.ts) or the e2e package with its own Playwright version.
- Running any e2e spec, the Docker stack, Node 24, the platform suites, any service suite.
- What fields the mail API really returns (unmeasured by the PR and by me).
- docs-fragments check, audit:gate, check:test-types, eslint, the pre-push hook legs: seat's claims read, not re-run.
- Linear (KS-2029 comment and attachment not read).
- Whether the fixture is used outside tests/e2e (the seat's systemTest grep not reproduced).
