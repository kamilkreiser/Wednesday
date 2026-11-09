PR 2116: GO; PR 2117: GO WITH NOTES; PR 2119: GO
# Gate 279, tier 2 batch: PR 2116, PR 2117, PR 2119 (findings only, run 2026-11-09 12:48 to 13:05 AEDT)

| PR | head (re-read at start and end: NOT moved) | verdict |
|---|---|---|
| 2116 (KS-2133) | 84401f920af8 | GO |
| 2117 (KS-2134) | 0efffbb15fe6 | GO WITH NOTES |
| 2119 (KS-2138 item 1) | 6facf676e10b | GO |

develop e028786a0921 at start and at end: NOT moved. The pins held.
STOP LINE (any product byte means NEEDS TIER 1): not tripped. PR 2116 touches one api-gateway test file (+13/-0); PR 2117 one auth test file (+29/-0); PR 2119 one cheat HTML fragment (+1/-1). I read all three diffs whole (git diff origin/develop...prN in my clone). No product byte in any.

## Q5, merge trees
- `git merge-tree --write-tree` of each head on develop e028786a0921: rc 0, 0 conflicts, for 2116, 2117, 2119. All three together, real `git merge` of the three heads on develop: rc 0, 3 files changed (+43 -1).
- The three PRs share NO path with each other (uniq -d over the three name lists: 0).
- Open PRs: I could not call the GitHub API (the project's gh config is not logged in; I did not go looking for a token). Substitute: I took the seat's census list of 48 open PR numbers (evidence/e4/openprs_pre_push.json), fetched each head from origin myself, plus PR 2118 (opened after that census), and diffed each against its merge-base. Path overlap with the three PRs' 3 paths: NONE in 48 lists. Control: one of my paths planted into PR 2102's list was found (1 hit, expected 1). PR 2118 touches `.githooks/pre-push`, the ks2127 test, and the two KS-2127 fragments: disjoint. Caveat: the open set is the seat's list, so a PR opened or listed outside it is unseen (PRs numbered above 2119: none exist on origin).
- Merge order: any order.

## PR 2116 (KS-2133), GO
BLUF: test-only, the claims reproduce, cell names are true.
FOUND / TESTED / HOW
- Code under test, index.ts:683 `const sameBytes = nextRaw === openApiSpecRaw;`, the warn branch at 688 and the success branch below it. Quoted by me from the merged tree.
- Env: api-gateway on a merged tree needed zod 4 and a built packages/shared; I used the seat's worktree s-t20-d2 node_modules (zod 4.6.7) and rebuilt shared/dist in my clone. A first attempt with the main checkout's stale node_modules (zod 3.25.76) failed all 7 cells at import, before any assertion, including the unmutated baseline; I discarded that run and the finding is only about my environment.
- Unmutated merged tree: 7 of 7 green. Base (develop) version of the test file, copied: 5 of 5 green.
- My mutants of the `sameBytes` line, each applied then restored by sha (index.ts f3403c1d01216da7 before and after every one, git diff of it empty):
  - length-only: exactly 1 red, the "SAME LENGTH" cell.
  - trim-only: exactly 1 red, the "whitespace-only change" cell.
  - MY OWN `slice(0,-3)` compare (tail ignored): exactly 1 red, the same-length cell.
  - always-true: 4 red (the control, the second-send-of-same-changed-text, and both new cells).
  - lower-case compare: 7 of 7 green, a SURVIVOR (not claimed by the seat; see G279-2116-1).
  - The base file under length-only, trim-only, tail3, lower-case: 5 of 5 green each (the gap the PR says it closes). Under always-true the base file is red 2 of 5, so the base cells do bite for that.
- Cell names true: "SAME LENGTH ... the comparison is of the text, not its length" goes red only under a length-style compare; "whitespace-only ... not made after trim" only under a trim compare. The seat's "|| mutant reddens both new cells" I did not run separately; it follows from the two single reds above (a `||` is red whenever either is). Marked as inferred, not run.
- Whole api-gateway suite on the merged tree: 1887 tests / 169 files, 0 failed. That is the seat's 1882 / 168 plus my 5-cell base copy in 1 file, so 1882 / 168 is consistent. Not run on bare develop.
Findings
- G279-2116-1 (info): a case-folding compare (`toLowerCase` on both sides) survives both the old and the new cells. Not a claim of the PR; noted as the remaining gap in the same family.
- G279-2116-2 (info): PR body names "Gate 249" results and the checker's `||` mutant; I could not re-run the checker, only my own equivalent mutants.

## PR 2117 (KS-2134), GO WITH NOTES
BLUF: test-only, both new cells bite as claimed. The flake explanation is true for the two tree-walk cells; the body goes a step further than the evidence for the cell behind the original "red 1 -> 0".
FOUND / TESTED / HOW
- Product code quoted: github.ts:95 `const access_token = tokenBody.access_token;` used raw in Authorization at 97 and 112 (the second send, `/user/emails`); google.ts:96 ``Authorization: `Bearer ${tokens.access_token}` ``.
- Unmutated merged tree: touched file 8 of 8 green; base copy 6 of 6 green.
- My mutants, each restored by sha (google.ts 9df70e329cc5c78f and github.ts 730690a5fd88bb9b match the seat's sha prefixes; linkedin 13733a82a70397a0, microsoft-personal 7c85ce8a1321404e, facebook c1619b2b19cb70d1 restored too):
  - google `.toLowerCase()` on the sent token: exactly 1 red, the mixed-case cell.
  - github second-send `.trim()`: exactly 1 red, the second-send cell.
  - github `.toLowerCase()` at the source (both sends): exactly 1 red, the mixed-case cell.
  - MY OWN linkedin, microsoft-personal and facebook `.toLowerCase()` at the source: each exactly 1 red, the mixed-case cell ("on all five" is true: it covers every adapter, not only Google).
  - Every one of those 6 mutants against the BASE file copy: 6 of 6 green (the gap is real).
- Cell names true. The second-send cell asserts the `/user/emails` Authorization equals `Bearer ' tok-ks1858-f1 '` and it sees the second call because the stub profile has no email; at the old fixture (email present) that branch never ran. I read the stub: sound.
- Suite: merged tree auth 1845 tests / 150 files (the seat's 1839 / 149 plus my 6-cell base copy) with 1 failure, the ks949 timeout below; develop alone 1837 / 149 clean twice (matches the seat's "before 1837").
- ks949 flake: ks949 file alone on develop 31 of 31 (and 31 of 31 with DEMO_SECUURA_PASSWORD=x). Whole auth suite on UNTOUCHED develop e028786a0921: 2 clean runs at load about 10 to 12; then 3 concurrent runs at load up to 22 gave, in all three, exactly the same 2 failures: "the enumeration actually finds seed sites, including the one the gate planted in" (5005 to 5007 ms) and "no executable seed site anywhere in the tree names the real address" (5000 to 5001 ms). Also seen once on the merged tree at load about 8.5 (5003 ms). So the explanation "5 s timeout in two tree-walk cells of ks949, reproduced on untouched develop" is TRUE.
Findings
- G279-2117-1 (low): the PR body and ticket comment say the held pass's "red 1 -> 0" was "the same kind of timing flake in another cell of that file". The cell is "NOT seeded when DEMO_SECUURA_PASSWORD is unset", which the seat says ran 2756 ms, i.e. under the 5 s timeout. A cell that fails at 2.7 s did not time out. The seat's own evidence logs list only the two tree-walk cells as failing; the 2756 ms failure is not in the files I read. I could not reproduce that cell failing in 8 whole-suite runs and one run with the env var set. So "same kind" is plausible but unproven. Wording fix only; no code consequence for this PR.
- G279-2117-2 (info, process): the seat reports that Blockchain/Dev/node_modules/node_modules in their worktrees is a symlink into another worktree (s-t16-email-catches). I saw the same symlink and it is what vitest's stack traces resolved through. Not this PR's issue; a handover item as the seat already says.

## PR 2119 (KS-2138 item 1), GO
BLUF: docs-only, the reworded row is true of the code.
FOUND / TESTED / HOW
- Diff: one `<td>` in `Projects Documents/fragments/cheat/KS-528-react-router-v7-portals.html` line 12; "G1 to G6" becomes "G1 to G5; G6 was red on develop b7d433fda83c by design and is green since PR 2091 merged (01b26bc772a7)". Other G6 mention in the file (line 4, "pin G6", issuer sets useTransitions on purpose) is consistent.
- Code the row describes, quoted from react_router_v7_portals.test.sh lines 100-101:
  `if (count(/<BrowserRouter useTransitions=\{false\}>/g, all('issuer')) !== 1) out.push('G6 issuer: ...not present exactly once');`
  `for (const a of ['admin', 'verifier']) if (/useTransitions/.test(all(a))) out.push('G6 ...must stay unset...');`
- Issuer main.tsx, read by me from git objects: at b7d433fda83c `<BrowserRouter>` bare (lines 40, 46), zero `useTransitions` (G6 red there: TRUE). At 01b26bc772a7 `<BrowserRouter useTransitions={false}>` (line 44) once, and `from 'react-router'`. At develop e028786a0921 line 44 the same, count 1. 01b26bc772a7 is an ancestor of develop (merge-base --is-ancestor yes) and is titled "Refs KS-528: the three portals import their router from react-router 7, and a suite pins it". The 0-at-old-base, 1-at-merge, 1-at-cut counts are TRUE (I measured old base, merge, and current develop; the cut 2a031f51 is between them, not separately read).
- G1 to G5 "nothing" at b7d433fda83c: consistent with the pre-migration source (bare BrowserRouter passes G3's one-element/no-basename rule; admin/verifier unchanged); I did not run the checker against that old tree. Inferred.
- Portals suite on the PR 2119 tree: passed=25 failed=0, the three G6 mutants each reported red, as the suite expects.
- docs-fragments check (needed the systemTest support helper; my first runs were REFUSED rc 2 for the missing helper, which was my sparse checkout; added it): develop e028786a0921 rc 0; PR 2119 head rc 0 ("lint clean, render passes html_docs_check"); planted unclosed `<div><p>` in that fragment rc 1, "tags are not balanced", file restored by sha. Counts: develop "225 new", PR head "223 new": the PR is cut on 2a031f51, two fragment files are newer on develop; harmless.
- Narrowing: the PR body says "Items 2 to 4 of the ticket (the router suite's source-text pins and the checker's two missed plants) are not in this PR", "Item 1 of 4", "Refs KS-2138 ... leaves the ticket open", and under "What this did NOT do". The ticket comment says the same. STATED. (Read from the seat's saved final bodies, see NOT TESTED.)
Findings
- G279-2119-1 (info): the portals suite's real-tree cell label says "R0-R4 and G1-G5" while its condition also covers G6. The seat already flags this stale label and leaves it; I agree it is stale and not in this PR.
- G279-2119-2 (info): "by design" in the row is the old gate's phrase for G6 being a red-first cell; on today's develop it is green, and the row says so. Reads correctly.

## Words (Q6)
I read the PR bodies and ticket comments from the seat's saved copies (evidence/e2|e3|e4/mail/pr_body_FINAL.md, ticket_comment_FINAL.md), not live from GitHub or Linear (no gh login, no Linear access). Checked as true against my runs: file lists and line counts (+13/-0, +29/-0, +1/-1), "no product byte", the 1880/1882 and 1837/1839 style counts (consistent with my runs), mutant outcomes, "the only changed-spec control appends a comment line" (read in the base test), "fixture GitHub user has an email so the second send never fires" (read in the base test), PR 2083 / KS-1505 and PR 2084 / KS-1858 as merged ancestors (a KS-1505 commit "the spec hot-reload warns..." exists on develop; I did not map PR numbers 2083 and 2084 to commits). Heads quoted in the comments match the pins. One wording issue: G279-2117-1.

## NOT TESTED
- Live PR bodies and Linear comments (NOT TESTED; only the saved copies).
- Gate 249's own results and the checker's `||` mutant as run by the checker; the claim that the checker's mutant reddens both cells is inferred from my single-compare mutants.
- G1 to G5 empty at b7d433fda83c by running the checker on that tree.
- Whole api-gateway suite on bare develop (only merged tree); auth whole suite on the merged tree gave 1844/1845 with the known flake.
- Node 24 (my runs used the machine's default Node), tsc/eslint on the new test files, any browser render of the fragment, hooks' 13 legs.
- The origin of the seat's 2756 ms "NOT seeded" failure.

## Conduct
- Clone: /private/tmp/g279 (blobless, sparse: Blockchain/Dev, Projects Documents/fragments, systemTest/__tests__/support), final size 3.3G (1.8G node_modules and a shared dist build, the rest old/ copies). Not removed (the commission says no rm). Scratch in it: old/ (moved-aside stale node_modules), g279-base-copy test files, run scripts, .orig copies. Nothing was written inside /Volumes/DevMASTER/!CODING: only read verbs and ls-remote there; I copied node_modules and dist OUT of the seat's worktree s-t20-d2 and the main checkout. The `git -C` fetch/checkout/merge write verbs ran only in the clone.
- Disk: DevMASTER 107 GiB free at start and at end (1.7Ti used, 95%). load1: 5.35 at start, 4.04 at end.
- DEVIATION, mine: load1 was above 8 for a few minutes. To reproduce the ks949 flake on untouched develop I ran three whole auth suites concurrently, and load1 peaked at 22. This was deliberate and short; I am declaring it, not excusing it.
- Two mistakes of mine, both caught: (1) first api-gateway runs used a stale node_modules (zod 3) and failed at import, all 7 red including baseline; I did not read those as findings, replaced the dependencies and reran. (2) My first overlap loop printed false OVERLAP lines from a whitespace compare in `wc -l`; I fixed the compare and reran with a planted control.
- Pushed, posted, commented, mailed: nothing.
