# QA GATE 52: Secuura/Distributed_Secuura PR #1860 (KS-1887, Seat D 46th), Tier 2, Round 1
**Head gated: 01f9cb0c57a2c1c9884b722f9dcb87677f504873** on develop dc8c210cb29d507014ce7f13034f841542b04a7b. Both re-read with `git ls-remote` at gate start (refs/pull/1860/head and refs/heads/develop): neither had moved. Clone at a fresh path, `rev-parse --show-toplevel` asserted equal before fetch. Findings only: nothing pushed, commented or changed in Linear.

## VERDICT: GO WITH NOTES. No finding needs fixing before merge.

Diff: 238 files, +13199/-4 = 9 tool/doc files + 229 frozen fragment files (117 flow legacy, 112 cheat legacy). The two shared pages themselves are NOT in the diff.

| Q | Result |
|---|---|
| 1 Byte identity | PASS (with the nuance in F1) |
| 2 Completeness | PASS |
| 3 Own tests + red-proof | PASS, 4 of 4 mutants killed |
| 4 `adopt` on a real PR (#1852) | PASS |
| 5 SKILL.md | PASS, two small notes |
| 6 Scope | PASS |

## Q1 Byte identity (instrument: `build --out` then sha256; control: planted character)
- Head tree rendered with the PR's own KS-1887 fragments set aside (so render = frozen legacy only):
  - Flow `62990735186b4659dccc5676e7b5261da43d45ba70adc2997e22accf87fdcd9c`, committed page at head, and develop's page: all three equal.
  - Cheat `c89d4c382a76678fa16697ce1c55c0ccbaccc4363da67b59858e466594c8ea19`, committed at head, and develop's: all three equal.
  - `check --committed` on that tree: "current (117 of 117)" / "(112 of 112)", OK, rc 0.
- Control: one `X` planted inside the `<h2>` of legacy flow fragment 0050. Render sha became `531e689c...`, differs from committed. `check --committed` rc 1 ("FAIL ... committed page" ); plain `check` rc 0 with an ADVISORY that the page differs. That is exactly the A1 ruling (advisory loose, strict is strict). Tree restored, `git status` clean.
- F1 (note, by design): at head with the KS-1887 fragments in place the render has one extra entry per page (flow `07a32b71...`, cheat `faf55704...`), so `check --committed` returns rc 1 "lagging 117 of 118" on the PR's own head. The PR's own new entry is the difference; the pages are refreshed after merge (author's mail and SKILL both say so). Anyone who wires `check --committed` into CI before the first refresh will see this red. Not a defect in the PR. Evidence: `evidence/q1_byte_identity_and_control.txt`.

## Q2 Completeness (instrument: python count of `<h2>` both ways; `evidence/q2_completeness.py`)
- Develop Flow page: 124 `<h2>`, all numbered, no duplicate numbers. Fragments: 117 legacy files with exactly one `<h2>` each + 7 `<h2>` in head.html = 124. Multiset of heading text equal. Develop Cheat: 112 `<h2>`; 112 fragments, one each, 0 in head/tail. Multiset equal.
- Byte check: head + legacy (name order) + tail equals develop's page byte for byte, both pages (902262 and 597411 bytes).
- F2 (INFO): the Flow page's first 7 sections live inside head.html, not in their own fragments. Each is in exactly one place, nothing lost or duplicated, but "one fragment per section" is 117 of 124 for Flow.

## Q3 Own tests and red-proof
- `docs_fragments.test.sh` at head: 81 passed, 0 failed, 0 skipped (the author's 81). `html_docs_matrix.test.sh`: 18 passed, 0 failed (the author's 18). Run one at a time. Logs in `evidence/`.
- Mutants, applied to a working-tree copy, file sha restored and checked each time:
  - M1 `check --committed` never strict (docs-fragments.mjs:358 -> false): 3 FAIL (C1b, C2b, C3b).
  - M2 ordering without `--reverse` (:222): 4 FAIL (B1, B4, B9, B10).
  - M3 html_docs_check placeholder test blinded (:93) in `html_docs_matrix.test.sh`: 1 FAIL ("a placeholder row was NOT reported").
  - M4 tag-balance lint disabled (:169): 1 FAIL (A5).
  - 4 of 4 killed; each sed verified to change the file.

## Q4 `adopt` on a real PR: #1852 (KS-1544 class; not 1837/1857/1383)
- Branch adds one section (+20 flow / +23 cheat lines) on merge-base a8c554659; its KS-1544 text is not in develop's page.
- Run in a throwaway clone at head: `adopt --from-ref refs/pr/1852 --against dc8c210c...`. Output: flow fragment "renders as section 130 (it was written as 134)"; cheat fragment "renders unnumbered". Fragment diff against the lines the PR added: only the `134.N` numbers turned into `<!--n-->`, nothing else. `check` OK (lint clean, html_docs_check passes); `build --out` shows `<h2>130.` for it. A second `adopt` skips both as "already a fragment". Fragment file names are truncated from the heading (`...-order-b.html`), and the flow and cheat slugs for the same entry differ: cosmetic.
- Full SKILL recipe also run (simulating post-merge develop with the 1860 head): `git merge` conflicted in exactly the two pages; `checkout $D -- pages`, `adopt`, `check` OK, commit; resulting tree differs from $D only by the PR's own code/tests and the 2 new fragments, pages untouched. Number there is 129 (no KS-1887 fragment in this sim to take 129 first... it is merge-order provisional, as documented).
- Whether #1852 is still open could not be confirmed (gh not logged in); its ref exists and its entry is not in develop.

## Q5 SKILL.md docs section
Reads plainly: create one fragment in each of `fragments/flow/` and `fragments/cheat/`, `<!--n-->` instead of a number, run `check`, commit the two files, never edit pages or run `build`. Worked example, naming rule, reviewer preview, who refreshes, hand-edit and PR-transition recipes all present. I ran the commands as written and they behave as stated. No contradiction with the tool.
- F3 (LOW): "Leg 14 of the pre-push gate runs it [check] for any push that changes Blockchain/Dev". Leg 14 runs the test suite, whose cell F4 lints the real tree; it does not run `check` itself. Effect is equivalent for lint, but wording over-states. The same paragraph correctly says a fragments-only push skips the gate, so nothing automated checks a PR author's fragment; they must run `check` by hand. Nothing in the repo wires `check` anywhere else (grep: only SKILL, tool, test mention it).
- F4 (LOW): rule line "Both fragments, every time" does not mention that other places in the skill (earlier/later sections about timings, "update the page") may still say "update the HTML docs"; I read only the changed hunk plus context and did not audit the whole skill for stale page-edit wording. See UNMEASURED.

## Q6 Scope
Diff is: SKILL.md (+65/-4), the tool, its test, 3 files x 2 pages of head/tail/KS-1887 fragment, 229 legacy fragments. No lockfile, manifest, baseline, hook, preflight leg or product code. Matches the author's claim.

## Other
- F5 (LOW): `check` and `build` need full first-parent history; a shallow clone exits 2 (documented, tested B-cells). Any CI job that checks out shallow would refuse. The repo has no required checks today.

## UNMEASURED
- Whole-SKILL.md audit for stale "edit the page" wording outside the changed hunk.
- `build --base` write path and refresh step (D cells passed in the author's suite; I did not run it on a real develop).
- Two stacked PRs converting the same base entry; behaviour on a long-lived develop beyond throwaway/real-history first-parent ordering.
- Pre-push hook with leg 14 (stack-dependent legs 3, 4, 8 skipped by the author); not run by me.
- `spark_gate.sh`: not run. It diffs test files on base vs head, and these tests and the tool they guard exist only at head, so a base run cannot be meaningful; red-proof was done with mutants instead.
- #1852 open/closed state (gh unauthenticated).
- Node 24 LTS (host has v26.8.1 only).

Evidence: `evidence/` (suite logs, mutant logs, byte-identity and completeness output, #1852 added-lines).
