PR 2163: GO WITH NOTES
PR 2164: GO WITH NOTES
PR 2165: GO WITH NOTES

Gate 305, tier 2 (Sonnet), 2026-11-10 16:2x to 16:4x AEDT. Findings only; nothing posted, mailed, pushed or fetched in !CODING. All tests and mutants ran in my own scratch clone (blobless, sparse, 2 scratch dirs under the session scratchpad: `g305` for the bash suites, `iss` for the issuer vitest copy).

## Pins (re-read at start 16:2x and end 16:38:52 by ls-remote; NONE moved)
- develop b602c418296a3191d9efba5511d6c0ffda4e3212 (unmoved). Its one-commit move from 0e6479d7b6c0 (b602c418, "Refs KS-2130", message says the preflight abort-text cell) changes ONE file: `Blockchain/Dev/scripts/__tests__/ks1547_preflight_step_header_denominator.test.sh`. It touches none of the six paths the three PRs write or read (checked by `git diff --name-status 0e6479d7b6c0 b602c418296a`).
- PR 2163 head 8f0048de07fa6ea20d9242a24b710b73dfe00b9b, PR 2164 head f03f4e72a8b7725f5dac5b7254e13b67cb2deb6b, PR 2165 head f11dc645401aca105aeb2fc1f7b94bbf9f48e4e5: all unmoved. All three: one commit, parent 0e6479d7b6c0, base branch develop, state open, not draft.
- Machine: load1 10.6 at start, 14 mid-way (a drive copy), waited with an until-loop to below 8. The bash suites, all red-proof legs and all mutants ran at load1 5.8 to 7.4. EXCEPTION, disclosed: the two whole-suite issuer runs (develop baseline and PR head) started at load1 9.12 and 8.96, over the 8 line; the suite is 3 files and passed both times, and the targeted runs after that were under 9. df DevMASTER 91 GiB available at start and end.

## Cross-cutting, FOUND
- File sets by the PR files API (GitHub REST, read, key from the Secuura .env sourced in-process, never printed) AND by `git diff --numstat 0e6479d7b6c0 pr<n>` of refs/pull/<n>/head: they agree.
  - 2163: `Blockchain/Dev/scripts/__tests__/ks949_main_seed_idempotence.test.sh` modified +12 -1. Nothing else.
  - 2164: `systemTest/__tests__/no_hardcoded_slot_literals.test.sh` modified +4 -0. Nothing else.
  - 2165: `Blockchain/Dev/frontend/issuer/src/components/blockchain/BlockchainCard.tsx` +3 -0 (the one product file) and `Blockchain/Dev/frontend/issuer/src/__tests__/blockchain-card.test.tsx` +32 -0. Nothing else.
- Held-Spark comparison, per file, changed lines (+ and -) extracted from the READY fence and from `git diff`: 2163 EQUAL (13 = 12+1); 2164 EQUAL (4); 2165 EQUAL on both files (32 test, 3 product). No difference. (Hunk headers and context lines differ in width, as expected; the changed lines are identical.) Tool: scratchpad `cmp.py`.
- Open-PR census by the API: 81 open PRs, 381 file rows (the seat's 79/378 plus these three). Planted control `.claude/hooks/block_secret_reads.py` returned PR 2156 (and only it), so the instrument works. Each PR's own paths returned only that PR: ks949 suite -> 2163; slot-literals suite -> 2164; BlockchainCard.tsx and its test -> 2165. The files the cells read or the callers (`startup-migrations.ts`, `support/slot-expect.sh`, `DocumentDetail.tsx`) have no open PR. No sharing, among the three or with any other open PR.
- Merge trees onto develop b602c418296a (`git merge-tree --write-tree`): 2163 alone rc 0 tree 816f7bc95cba, 2164 alone rc 0 tree d10c5acfc8ce, 2165 alone rc 0 tree 97e50ffac38e, all three together (two-parent commits chained) rc 0 tree e30ea82061b1; the tree-vs-develop numstat of the three-together tree is exactly the union of the four file rows above (32/3/12-1/4) and nothing else. No conflict.
- Closing words: searched title, body, PR comments (including the Linear bot linkbacks) and the three commit messages for close/closes/closed/closing/fix/fixes/fixed/resolve/resolves/complete. No closing word in closing form. The only hits: 2164 body says the PR "does not explain or fix the occurrence" (a negation), and 2165 commit says "its closing `)}`" (JSX). All three use "Refs KS-xxxx" and say the ticket stays open.

---
## PR 2163: GO WITH NOTES

FOUND
- Test-only, one bash file, zero product bytes. Cell ID4 plants `tenant_slug='slug-only-drift'` on id c1000000-...0001 (tenant_id untouched), runs the shipped statement, passes only on tag `UPDATE 1` and the slug back at `oxford-university`. TOTAL_CELLS 27 to 28 (the number the suite prints; it is used only in the summary and the abort line).
- It does what the ticket's item 2 asks: the gate's own proposal text (slug-only drift on a second id, `c1...0001` to `slug-only-drift`, assert UPDATE 1 and the slug restored, reds under Tg3) is implemented line for line. Item 1 (ID3 size assertion) is not in the diff and the body says so.
- Body claims match the change; nothing larger is claimed. The body says "a guard without the slug arm reads red", which is exactly what I measured, no more.

TESTED / HOW (scratch clone at develop b602c418296a; real throwaway PostgreSQL over a unix socket, Homebrew binaries, no container, no TCP)
- Suite on develop: 27 passed, 0 failed (9 s). On the PR head: 28 passed, 0 failed (7 s), ID4 `ok`. Counts before/after 27 to 28; no cell lost.
- Seat's plant (slug arm removed from the guard, anchor ` OR u.tenant_slug IS DISTINCT FROM v.tenant_slug)` found exactly once in `startup-migrations.ts:1111`): 27 passed, 1 failed; the single FAIL line is `FAIL — ID4: slug-only drift on a second id was not repaired, command tag 'UPDATE 0', slug 'slug-only-drift'`. Reproduced.
- My own mutant (slug arm changed to a self-compare `u.tenant_slug IS DISTINCT FROM u.tenant_slug`, a different edit from the seat's): 27 passed, 1 failed, again exactly ID4. Product restored byte-identical (`cmp` rc 0) after each run.
- Control in the other direction (my mutant: tenant_id arm removed, slug arm kept): 28 passed, 0 failed. See G305-2163-1.
- Pins/labelling: ID4 is green on develop and goes red only under a plant of the slug arm; its label states what it pins ("the slug arm of the IS DISTINCT FROM guard") and the comment says why AG4 cannot see it. Honest.

NOT TESTED
- Item 1 of the ticket (not in the PR). Other regressions than the slug arm. The suite on a machine without Homebrew PostgreSQL (the suite prints SKIP there; it was not exercised). Pre-push hook (not run by me; the body quotes it and states the 3 skipped legs honestly).

Findings
- G305-2163-1 (Note): ID4 catches the guard missing its slug arm only. A guard that has ONLY the slug arm (tenant_id arm removed) still reads 28/28 (measured, mutant above), because AG4 plants both columns and ID4 plants only the slug. The ticket's title says "a one-arm guard is invisible"; the PR covers one of the two one-arm shapes, which is what its title and body say, but the other arm remains uncovered and no ticket line names it. Suggest the board note it when KS-1145 item 1 is picked up.
- G305-2163-2 (Note, process): the READY's 'built on 0e6479d7b6c0' is one commit behind develop; the merge tree is clean and the one develop move touches an unrelated file, so no rebase is needed.

---
## PR 2164: GO WITH NOTES

FOUND
- Test-only, one bash file under repo-root `systemTest/` (not Blockchain/Dev), +4 -0: after each of the suite's two `git init -q` calls a SETUP cell asserts `git rev-parse --is-inside-work-tree` prints `true`, else a FAIL line saying git init did not make the tree a work tree. Suite 11 to 13 cells.
- Scope vs KS-2098: the ticket says "No fix here" and offers a possible shape ("check the exit status of the `git init` ... stop the suite with a setup message"). The PR is a variant of that shape (checks the outcome, not git's exit status, and prints a FAIL rather than stopping), and the body states plainly that it does not explain or fix the occurrence and the cause stays UNMEASURED. It claims no more than it does.

TESTED / HOW (scratch clone; the suite lists files through git so it needs a work tree; it ran in the clone's sparse checkout)
- Develop: `11 passed, 0 failed` (24 s). PR head: `13 passed, 0 failed`, both SETUP lines `ok`. Counts 11 to 13.
- Plant 1 (planted-control tree's `git init` replaced by `true`, anchor found once): 9 passed, 4 failed: the new SETUP FAIL plus `planted 54 literals, the guard reported 0`, `a bare 'slot-literal-ok:' exempted a literal`, `an untracked source file was skipped`. The provenance SETUP stayed `ok`.
- Plant 2 (provenance-control tree's `git init` replaced by `true`): 11 passed, 2 failed: the provenance SETUP FAIL plus `the membership check cannot catch a non-from_runs element`. The planted-control SETUP stayed `ok`.
- My own mutant (provenance tree initialised `--bare`, so git init succeeds but the tree is not a work tree): 11 passed, 2 failed, the same two lines. This shows the cell checks the property it names, not merely that init ran.
- The four control lines the ticket quotes are the four that go red across the two plants (3 under plant 1, 1 under plant 2), as the seat says. Product (helper `support/slot-expect.sh`) untouched. Each cell is attributable to its own tree.

NOT TESTED
- Whether a failed `git init` was ever the cause of the ticket's occurrence (unmeasured by the PR and by me). The hook leg-14 run under load. Any sibling suite.

Findings
- G305-2164-1 (Minor): the cells are green on develop in every normal run and cannot be red except when git init leaves a non-work-tree. They are not "pins" of any product behaviour; the labelling ("SETUP") is honest about that, and the PR body says if git init was not the cause they stay silent. Noted, not a defect.
- G305-2164-2 (Note): the check would read `true` falsely if `$TMP` (mktemp -d) were ever inside an enclosing git work tree (rev-parse looks upward). With the default mktemp location it is not; I did not test a TMPDIR inside a repo. A path-equality check (`--show-toplevel` equals the tree) would be sturdier. Not worth blocking.
- G305-2164-3 (Note): on failure the suite continues and prints the later control FAILs as well as the SETUP line (measured: 4 failed lines under plant 1). The SETUP line is the first FAIL of the group, so a reader sees the cause first; the body's wording ("names a failed git init") is accurate.

---
## PR 2165: GO WITH NOTES (tier 2 stands: no raise)

FOUND
- One product file, +3 -0, a frontend display condition inside `BlockchainCard.tsx`: a JSX comment, `{proof.blockNumber > 0 && (` before the Block row and its closing `)}`. One test file +32 with five cells (R1, R2, R3 red-first, C1, C2 controls). No auth, data, credential or deploy path. Tier 2 stands: not raised. A non-comment product byte does change, as the body says ("product bytes change; the gate may raise it").
- Scope vs KS-2095: the ticket's F5 (issuer) fix shape is "carry blockHeight through and hide the row when it is null". This PR does the hide half for the issuer only; F4 (verifier) and carrying the height are not in the diff, and the body says so and uses Refs. No overclaim.

TESTED / HOW
- Whole issuer suite (vitest, 3 files; my copy of frontend/issuer with `npm ci` from its own package-lock, since the monorepo node_modules was too slow to copy): develop 15 passed, 0 failed; PR head 20 passed, 0 failed (READY: 15 to 20). Same counts the seat reports. (Both ran at load1 about 9: see the load note.)
- Red proof reproduced: product file set back to develop's bytes, test file kept: `Tests 3 failed | 8 passed (11)`, the three red are exactly R1, R2, R3; C1 and C2 and the six older cells pass. With the PR product, 11 of 11.
- My own mutants against the PR product, the test file kept (each reddens a NAMED cell): `>= 0` instead of `> 0` reddens R1 and R2 (2 failed); `!= null` reddens R1 and R2 (2 failed); `false &&` (row always hidden) reddens the older `displays formatted block number` and C2 (2 failed). All restored by cmp.
- Pins/labelling: R1 to R3 are green only with the fix, C1 and C2 green both ways: they behave as pins. See G305-2165-2 on the names.
- RENDERED, component render (jsdom, `@testing-library/react`, `animate={false}`, my own probe file in scratch, not in the PR), the rows inside the tx-details block, one render per blockNumber value, develop product then PR product:
  - 1234567: both: `Tx Hash`, `Block 1,234,567`, `Slot 98,765,432`, `Confirmed ...`. Unchanged.
  - 1: both show `Block 1`.
  - 0 (what DocumentDetail passes for an anchor with a hash and no height): develop shows `Block 0`; PR shows no Block row and keeps Tx Hash, Slot and Confirmed.
  - undefined: develop THROWS `Cannot read properties of undefined (reading 'toLocaleString')` (the whole card fails to render); PR renders the card with no Block row.
  - null: develop THROWS the same; PR renders with no Block row.
  - NaN: develop shows `Block NaN`; PR no Block row. -5: develop shows `Block -5`; PR no Block row.
  So what a user sees: a confirmed anchor on the issuer's Document detail page no longer reads "Block 0"; it shows Tx Hash, Slot (if any) and Confirmed, and no block line at all (because the issuer never carries the height, every such anchor now lacks the line until the carry-through half lands). In the animated sequence the Block row was only ever shown in the final Confirmed stage, so the change affects that final state only.
- Type check, lint: not re-run by me (the seat reports tsc rc 0 and eslint 0 errors; its caveat that the package tsconfig excludes `src/__tests__` is true of the config). Not claimed by me.

NOT TESTED
- A real browser render (NOT TESTED; the component render above is a jsdom render, not a browser). The verifier portal. The credential modal in a browser. The animated (animate=true) timeline in a browser. `tsc` and eslint (carried from the seat, not re-run by me).

Findings
- G305-2165-1 (Minor): the change is wider than the body's one named caller. `BlockchainCard` has a second caller, `CredentialDetailModal.tsx` (Blockchain tab, `animate={false}`), which passes `credential.cardanoAnchor.blockHeight` straight through. A credential anchor with a height of 0 or an absent height used to print "Block 0" (or crash the card on undefined/null, measured above) and now leaves the row out, the same behaviour the PR intends. The body only discusses DocumentDetail and says the other callers were not searched. Not a defect (the effect is the intended one), but the body undersells the blast radius; a rendered user-visible change on the credential modal is not named.
- G305-2165-2 (Minor): the cell names carry the word `RED` ("RED ks2095 R1 ...") permanently; after merge those cells are green and still say RED and "control ks2095 C1". A future reader scanning vitest output for RED sees green cells so named. Cosmetic, from a held Spark patch the seat did not re-author.
- G305-2165-3 (Note): develop's behaviour for undefined/null was a thrown TypeError (whole card), not just "Block 0". The new R3 pins that it no longer throws; the PR body says "absent at run time" shows no row but does not say develop crashed. Improvement, understated.
- G305-2165-4 (Note): negative and NaN `blockNumber` also hide the row (measured above); the body discloses this ("read from the condition, not tested by any cell") and no cell pins it. Fine.
- G305-2165-5 (Note, Wednesday's PRETTIER FLAG, report not ruling): I ran prettier 3.8.3 (the monorepo copy) with `--no-config`. Default style (double quotes): it warns on both touched files AND on the untouched `blockchain/types.ts`, `DocumentDetail.tsx` and `provenance-timeline.test.tsx`; on develop's versions of the two touched files it warns too. So the default check does NOT distinguish this change (the seat is right). With `--single-quote` (the files' own quote style), the PR's product file shows 30 changed diff lines against develop's 19: the extra 11 are this PR's wrapped Block row, whose `<div>` body is not indented under `{proof.blockNumber > 0 && (` and the `)}` after a blank line. So a style-matched prettier does distinguish it. The repo has no prettier config and no format gate for the issuer; nothing here would fail a gate. Not ruled.
- G305-2165-6 (Note, environment, outside the diff): the seat's finding that `Blockchain/Dev/node_modules/node_modules` is a stray symlink: I read `worktrees/s-r94-b/Blockchain/Dev/node_modules/node_modules` (read only) at 16:2x and it is a symlink dated 10 Nov 16:09 whose target is that same tree's own `node_modules` (not the s-g30-identus path the READY names). I did not clone or copy it. The READY's account that it was moved aside in s-r94-b is therefore not what the tree shows now (it may have been recreated or re-pointed after the READY). I did not investigate further and made no change.

---
## Q8 summary (the PRETTIER FLAG): see G305-2165-5. It applies to PR 2165 only; the two bash PRs have no prettier surface.
## Declared limits of this gate
- No browser, no live stack, no container. I used a scratch `npm ci` for the issuer copy and for the Dev workspace (with `--ignore-scripts`), not the seat's node_modules. A dependency-version difference between the lockfiles is possible; the counts matched the seat's 15 and 20 exactly.
- The pre-push hook output in the bodies is the seat's quote, which I did not reproduce.

## SPARK SHADOW
Tunnel UP, spark_gate.sh and spark_review.py run on each PR after this verdict was written (blind). Full rows in `calibration.md` in this folder. Summary:
- PR 2163: Spark GO WITH NOTES (match). Recall 0/2, FP 2 of 5. TOOL GAP: the deterministic half reported head `0 passed, 1 failed` for the ks949 suite (`packages/shared is not built`, a fresh worktree has no gitignored dist) and the Spark did not mention it; my own run is 27 to 28 of 28.
- PR 2164: Spark GO WITH NOTES (match). Recall 2 partly of 3, FP 1 of 4 (it misread the tool's base==head run of a test-only PR as a contradiction).
- PR 2165: Spark GO WITH NOTES (match). Recall 1 of 6 (negative/NaN unpinned); it missed the second caller, the develop crash and the prettier point; FP 3 of 6. Its deterministic half matched mine exactly (head 11/11, base 8 pass 3 fail).
