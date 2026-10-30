STARTABLE: YES after your stamp. It is light (Python only, no port, no npm), so it can go before B942 when load1 first reads below 7; CI and CodeQL on the head were still running at 13:44 (CodeQL neutral; the gate reads them last, after a wait)

# B943 drafter report (2026-10-30, about 13:42 to 14:10 AEDT)
Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-30_B943_SEAT-G220_hpsmpoc-251-infra-binding-gate-tier2.md` (67 lines; 8 four-underscore lines = 7 slots + the last line, lines 59-65 and 67; at-sign slot pattern 0, control 1; non-ASCII bytes 0 by `LC_ALL=C grep -c '[^ -~]'`, after one correction: the Write tool decoded three backslash-u escapes in the kit's mutant and tuple text, and I re-wrote them as ASCII text by a `python3 -I` byte fix and re-counted 0). Shape: B938 for structure and conventions; the infra checks follow B922 (stamped cap gate) and B919 (its plant, corpus and mutant sections). I read everything read-only: gh `-X GET` under the project `.gh-config`, `git --no-optional-locks ls-remote`, raw `contents?ref=` reads into my scratchpad, one Python probe that imported scratch COPIES of the base and head files by path (functions only, `sys.dont_write_bytecode`, 0 `__pycache__` after), no Jira call, no `cd`, no hosted HTTP, no ref written, no message, nothing in the project folder.

## BLUF
Seat `Datasec/HPSM-POC-G220` (Sonnet, `BRIEF_SEAT_LEVEL=sonnet` inside the quotes), ports none, gates PR #251 @ `a8b9e81a` (2 commits on main `e21d8044`, 0 behind, 1 path `infra/tests/test_security_baseline.py` +143 -14: commit 1 129/5, commit 2 14/9). Round 1 of 2 on class "infra binding rule extensions". The heart is the gate's own plant table on the compiled landed template (24 other rules / base / after) for E2, E3, E4 and E6, with real `main.bicep` edits recompiled, a stub control, item 1's lint decline re-measured, an independent E4 corpus, about 25 of its own mutants (mW1 and mW2 alive at base and red at the head only through the integer row; m39 at base and head), commit 2's token and AST proof plus a truth check of each new comment, the CI predicate under 3.14, 3.9 and `-X dev`, then CI and CodeQL last.

## Facts re-measured (instrument; control)
- **PR and refs (13:43-13:44):** #251 open, draft false, mergeable true, `blocked`; head `a8b9e81a`, base `e21d8044`; commits `3126e8ee` (subject 173 chars) and `a8b9e81a` (87); 1 file +143 -14; title 165 chars with both keys. `refs/pull/251/merge` `695b6000`, parents `e21d8044` and `a8b9e81a`, tree `9c577233` = head tree.
- **The file, three versions:** base 2614 lines, blob `79e6b3bd`, 123 tests; commit 1 2738 lines, `daf921b1`, 130; head 2743, `000e676a`, 130. Non-ASCII lines 8 in all three. `uFF13` 0/1/1, `u0663` 2/2/2. Head anchors are in the kit (`except (ValueError, IndexError)` of `key_vault_name_problem` moved 1131 -> 1140).
- **Patch read whole:** the code delta is exactly the commission's E2-E6 and H. Commit 2 touches only the three comment places; the remaining two stale comments are untouched, as stamped.
- **Probes (scratch copies):** the landed suffix reads `''` at base and head. The ticket plant reads `''` at base and RED at head. `evaluated` gives `'ab'` for concat and toLower, and `None` with an integer, so commit 2's ARM_TOKEN comment holds. U+FF13 and U+00B2 raise `ValueError`.
- **VALUE-POSITION RESIDUE (new):** with S = uniqueString(resourceGroup().id, parameters('environmentName')), these four read GREEN at base AND head, though none gives a unique name:
  - `[take('zzzzzz', length(S))]`
  - `[take(S, 0)]`
  - `[concat('zzzzzz', string(equals(S, 'q')))]`
  - `[coalesce('zzzzzz', S)]`
  An S only in an `if` condition reads RED at head. The walk accepts the scoped call in any argument, not only where it reaches the value.
- **Base line 1660** (inside the existing RED row at 1653) types one of the new IndexError inputs and expects "which cannot be read". So the builder's Correction 1 (m39 is already killed at base) is plausible by reading; the gate measures it.
- **Checks at 13:44:** 13 runs; CodeQL `neutral`; `Analyze (python)` success (it reads this PR's bytes); `infra (Bicep validate)` success; vitest, web build, api still running; `web (Next.js)` not yet listed.
- **Overlap:** #244-#250 hold no `infra/` byte (file lists by GET); `b97/internal-notes` (old family, no PR) lists the path, as the B933 kit said.
- **Round count:** 102 first lines; the loose scan hit B867, B919 (NO GO round 1 on class B, PR #243) and B922 (GO WITH FINDINGS at class B's cap). There is no NO GO on this class or PR.
- **Ports and dirs:** no port needed; `.tools/b943` absent (control `.tools/b198`). Panes as in the kit, no G220.

## Builder claims found wrong or loose at drafting
1. **The ticket and the B933 kit's fact 4 said the IndexError half was pinned by no row.** The builder's Correction 1 says an existing row (base 1660) already kills m39. My read of 1660 supports the builder. The gate measures it, and -403 item 6's premise becomes a Note.
2. **Commit 1's message, "The suffix is green only when the scoped call is reached in every environment", is loose.** "Reached" includes non-value arguments (`length`, `equals`, `coalesce`'s second argument), and those shapes read green. The commission's wording ("any argument position") allowed it, and the message itself declares the wrapper and length unpinned. A non-`if` picker (`coalesce`) is the same shape as item 4 and is declared nowhere. Default grade: Note with ticket text (D-1, Q-1).
3. **The builder's "existing test methods other than the two named equal 138 of 138" names no frame.** The file has 123 `def test_` at base, so 138 must count methods of every class. The gate states its own frame.
4. **The builder's Correction 3: a bare `git fetch -q origin` ran in the shared clone,** against its kit. Its refs check says nothing was removed and the one new ref is its own. This is a process Note for Tuesday, not a code finding.
5. Commit 1's subject is 173 characters (Note; the squash text replaces it).
No code claim found wrong.

## D-decisions (mine, in the kit)
- D-1: **The VP residue is a Note with ticket text by default**, cells attached (Q-1 lets Tuesday make it Major).
- D-2: **Real `main.bicep` edits in the scratch mut tree** (at least four, recompiled by the pinned Bicep, restored byte-equal). One of them is a Bicep ternary, so the `if` shape the rule reads is the one Bicep emits.
- D-3: **The stub control** (the new checks returned empty, the new constant not looped) shows which new rows can fail.
- D-4: **The gate builds its own E4 corpus** with a different generator and seed, at least 5,000 + 5,000, plus every typed constant of the base file. Its control must FAIL.
- D-5: Hard stop: target 120 and HARD STOP 180 minutes after Step 0.
- D-6: **The kit names class B's history on PR #243** (NO GO round 1, then GO WITH FINDINGS at its cap) but counts this round as round 1 of 2 on the new class, as the B933 stamp ruled (Q-3).

## Q-questions for Tuesday (each with a default)
- Q-1: How is the VP value-position residue graded? Default: Note with ticket text, not Major.
- Q-2: May the gate make real `main.bicep` edits in `wt-b943-mut`, never committed? Default YES.
- Q-3: Does class B's capped history bear on this round? Default NO (new class, new PR, per the B933 stamp).
- Q-4: What does a NO GO mean? Default: the PR is parked open and Tuesday writes a round-2 fix kit.
- Q-5: Is the PR body corrected before or after the gate? Default: after, from the gate's numbers.

## Stamp slot defaults (suggested)
S1 STAMPED <time> by Tuesday s206, D-1 to D-6 accepted; S2 from the stamp until 17:30, launch_when_cool at load1 below 7; S3 Q-1 to Q-5 as the defaults; S4 Tuesday under the 2026-10-16 merge-once-tested grant, the 2026-09-13 as-many-agents rule, the 2026-10-24 standing order, the Datasec CodeQL policy and the 2026-10-22 Sonnet-first grant; YES to the two-refspec fetch, wt-b943-mut (test-file mutants and real main.bicep edits), the pinned Bicep compile, own gitleaks; S5 target 120 / HARD STOP 180 after Step 0; S6 Tuesday's own read at the stamp; S7 `model: claude-sonnet-5-5 -- G2 -- gauge <n>%` with load1.

## UNMEASURED
All runtime numbers in the kit are the builder's, written as predictions. Also unmeasured: any suite run, any real-file mutant run, m39 at base as a real run, the CodeQL `neutral` reason, the hosted `infra` and `vitest` conclusions, and the two-commit squash title.

## Outside-the-fences disclosure
None breached. I opened nothing under `.tools/b933/`, `b916/`, `b919/`, `b920/`, `b922/` or their trees. My probe imported scratch copies of the test file from my session scratchpad, ran functions only (no suite, no Bicep) and wrote no `__pycache__`.
