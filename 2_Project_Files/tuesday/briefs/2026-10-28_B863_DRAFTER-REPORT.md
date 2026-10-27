STARTABLE: YES (head `0c85ed9b` and main `df1dc0fe` verified on the PR, pane `Datasec/HPSM-POC-G186` and `.tools/b863` free, 9830-9839 no listener; seven check-runs still in progress is expected, the kit makes the gate wait; four stamp-time answers wanted, Q1-Q4, each with a default the kit carries)

# B863 drafter report (SEAT-G186, tier-1 QA gate, round 1 of 2, PR #236)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-28_B863_SEAT-G186_hpsmpoc-236-open-signin-wording-gate-tier1.md` (103 lines, shape of B831; 8 stamp slot lines, 0 at-tokens, 0 non-ASCII, no clock time typed).

## BLUF
- The gate establishes the five things asked: (1) no code token moved, by the gate's OWN stripper with planted-edit controls plus a word-diff second route; (2) every new sentence true, as a clause table against `config.ts`, `UatOpenAuthentication.cs`, `appservice.bicep`; (3) the leading words byte-equal and the pinning rows shown able to fail; (4) api / web / infra counts re-measured at base and head, the 3.9 failure run at base FIRST; (5) no secret or customer string; plus CodeQL (waits), merge tree, overlap with B858/B860, landing.
- Measured at the draft (read-only): PR #236 open, not draft, head `0c85ed9b`, base `df1dc0fe`, 4 files, +6 -5, 1 commit; main `df1dc0fe`; open PRs #236 only; no `b858*` or `b860*` ref yet; repo squash settings `COMMIT_OR_PR_TITLE` / `COMMIT_MESSAGES` (a plain squash lands the commit message); 13 check-runs, 7 in progress, `Analyze (python)` and `(actions)` rows at `0c85ed9` with 0 results; 0 open alerts; required contexts 5; `ci.yml` has no deploy job (header lines 1-25, `WHATIF` at 583).
- Real ambiguity worth the gate's time, found in the diff: the new README sentence "Each of the two has its own key" follows a sentence naming two locks, two apps and two environments (H-1). Also README line 233 "answer 403 `uat.action-off` there" is now next to a paragraph that includes the demo (H-2). Both are hypotheses with a default grade (Note), not facts.
- Model/routing: Opus `claude-opus-5-5` (`models_latest.json` line 17), row G1 `model-routing.md` line 108, G2 line 109 (does not apply), G-cap line 111. Charter Rule 1 line 86, Rule 2 line 92, verdict shape line 316, boundaries line 335.
- Launch line (form as B831, `BRIEF_SEAT_LEVEL=opus`) is at the end of the kit. Landing line: `gh pr merge 236 -R datasecau/HPSM-POC --squash --match-head-commit 0c85ed9bcacd734430f5b7bfec2138a1198a71b8 --subject "<subject>" --body-file <file>`, explicit text because of the squash setting; check localdomain 0 after; not a deploy.

## D-decisions (drafter's choices; Tuesday accepts or changes at stamp)
- D-1: Class text "the open sign-in wording" with six instances (a)-(f); round count 0 of 2 before, this is round 1 of 2. B831 is the nearest gate (GO WITH FINDINGS), and its findings are what this PR closes. Loose scan of the 87 GATE VERDICT first lines: 15 hits, none a NO GO on this class (B415, B436, B447, B471 are NO GO on other classes).
- D-2: Instrument for "no code token changed" is the gate's own comments-and-literals stripper (C# and TS), with the changed-literal list diffed whole (exactly one literal per file) and planted-edit controls that fire in both halves; the builder's `strip.py` is READ-FORBIDDEN. Second route is `git diff --word-diff=porcelain`. A compile-and-compare of the Api is NOT required (stated in C2, "one or two instruments" in the verdict line).
- D-3: Suites are re-run at base AND head by the gate (api SQLite, web vitest under Node 24, infra whole under 3.14 and 3.9, 3.9 failure base-first). This is heavy; the kit uses the B831 load rule (load1 below 8, two reads) and cuts it last in PRIORITY (api/web before the repeats).
- D-4: The gate has two control mutants of its own: API line 134 leading words changed and the branch removed (the row at `UatOpenTests.cs` 184-186 must go red), web line 91 check removed (the row at `uatOpen.test.ts` 70-76 must go red; its key sample is longer than 32 bytes). It records that the web row never asserts the text, as a fact about the row, a Note.
- D-5: Jira is GET-only for the two tickets through the project helper (2 GETs), unlike B831 (0 Jira). Reason: the done-when ("any test that pinned an old text moves with it") is part of what the gate grades.
- D-6: Ports: none expected; 9830-9839 reserved as the builder kit did, with the lsof positive control.
- D-7: Clones/worktrees mirror B831 (own clone, base and head worktrees only; no mutant worktree: mutants are scratch copies).
- D-8: Severity: a moved code token or changed leading part is a Blocker; a new sentence false in a way that misdescribes a lock is a Blocker; ambiguity with a true reading is a Note.
- D-9: Pane/kit names `Datasec/HPSM-POC-G186`, `.tools/b863`, `.tools/wt-b863-{base,head}`, STATUS `2026-10-28_B863_STATUS.md`.

## Q-questions (each with a default the kit already carries)
- Q-1: Should the gate also run a third route for C2 (build the Api at base and head and compare compiled string tables)? Default: no; two routes (stripper plus word-diff) and say "one or two instruments" in the verdict.
- Q-2: Does the product owner want README H-2 (demo's refusal behaviour next to the "there" sentence) ticketed if the sentence is true as written? Default: Note with ticket text, no finding.
- Q-3: Round count: confirm 0 of 2 before (B831 GO WITH FINDINGS is not a NO GO on this class). Default: round 1 of 2.
- Q-4: Squash text: Tuesday words subject and body from the gate's measured counts (the builder's message carries 2156/0/13, 3036/0/0, 277, names lost 0 added 0). Default: reuse the builder's message body if the gate confirms its counts, with a Tuesday-chosen subject; no ticket key, no `B###`.

## Not measured by the drafter
No suite, clone, fetch, stripper, mutant or plant was run; the 7 in-progress check-runs; whether B858/B860 push before the gate starts; toolchain versions on the gate's machine state; H-1/H-2 are readings, not tests.
