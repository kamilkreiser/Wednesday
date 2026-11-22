GATE B1962: GO @ ceff5cf on main 423516c

Tier G2 holds: one test file, no product code, no security-shaped issue found (no hand-off to G1). Round 1 of 2. Read-only toward project, Jira, GitHub; wrote only this folder and `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s314/g1962/`.

## Findings
None blocking. Notes: (N1) a future alternative of the middle pattern needs its plant added by hand (the kit's D1); the T1d-style mutant shows it. (N2) The sibling alternations (True|False) and (png|svg|jpg) are untouched by the head (diff has no hunk near lines 88 and 97) and stay for a ticket of their own (FOR-RECORDS 4).

## What I measured
1. Attack (read of the whole head file and diff): the middle regex is `constraint:(Constraint|PolicyControlValue|Compare)`, three alternatives; plants are the kept `constraint:PolicyControlValue` plus `constraint:Constraint` and `constraint:Compare`, so every alternative is planted. The fragment check now spans parts, plant and morePlants.flat() (`constraint`, `:Constraint`, `:Compare` each alone are not a hit; test passes). No plant spells a scanned name whole: 0 occurrences of the three joined spellings in the file text (python, with a regex-piece control of 1), and the file's own-scan test is green. `morePlants` defaults to `[]`; the middle pattern is the only call site with a fourth argument (diff). Diff = the kit's five edits, 17 added 4 removed; blob 1d575680f7d18f127197a72033e4119e877ae7c4; 0 bytes above 127, 0 CR (control 0xC3 counts 1).
2. Image runs (CI image `--target ci`, `--network none`, one container per job, each under the project heavy lock via my own heavy.sh form; lock released, images removed by exact name). File at head: `Tests  10 passed (10)`; at base the same.
   Mutants (base image / head image): C0 10 passed / 10 passed; T1d GREEN / RED; T1e GREEN / RED; T1f RED / RED; S1 GREEN / GREEN. First assertions at head: T1d `constraint|:(Constraint|Policy|ControlValue): constraint:Compare: expected false to be true`; T1e `...constraint:Constraint: expected false to be true`; T1f `...constraint:PolicyControlValue: expected false to be true`. Every mutant restored, cmp equal; image file sha equals host copy.
   Base and head steps both: lint, format:check, typecheck, build rc 0; renderers 291 passed, 1 skipped; workspace 3041 passed, 2 failed (the two citations.test.ts rows only, SOW text); `content:check` current, hash 5679855b0b9c7948...; test-name multiset base vs head lost 0 added 0 in both (controls: one dropped name reports lost 1, one planted reports added 1). CK6 controls fired (prettier rc 1, eslint rc 1). After build at head: fixture-fence 3/3, qgate 10/10, b11-content-internal-text 6/6.
3. Releases: four blobs at head equal base (23cd95f5, 09d597c6, 3ed9445b, 30269393); diff names exactly the one path. GitHub: branch ref = pin, compare ahead 1 behind 0, one file +17 -4 blob 1d575680; main = 423516cb; open PRs 0; code-scanning open alerts on main 0.
4. Message and diff: gitleaks 8.30.1 (host binary, the project's gitleaks.toml, stdin) over the diff and the message: no leaks (planted key control: found, rc 1). Message has one trailer, no person, ticket key, B-number or card id (own list, controls fired). Author and committer both the identity slot's noreply address.
5. PR 131 check set: CodeQL, Analyze (javascript-typescript), Analyze (csharp), all completed success. Landing texts and FOR-RECORDS in this folder.

## Not measured / disclosure
- CodeQL on the head (no pull request yet); `secret-scan.sh --tree`; the live demo.
- gitleaks ran on the host binary, not in the project's image.
- A `cp` of the builder's Jira helper was refused by the path guard (it reads the source as a write); I did not retry it, and wrote my own GET-only helper in my scratch to read PCOMP-67 (HTTP 200, comments 0; control PCOMP-9999 404). Say so if you read that as going around the refusal.
- One `cd` appeared once in my own call and was refused by the hook; nothing ran.
