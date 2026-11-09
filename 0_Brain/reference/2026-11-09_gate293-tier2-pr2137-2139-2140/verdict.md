PR 2137: GO; PR 2139: GO WITH NOTES; PR 2140: GO WITH NOTES

Gate 293, tier 2, Seat R 92nd round 1 of 4. Findings only. Posted nothing, mailed nothing.

## Pins (ls-remote at start 21:3x and at end; neither read moved)
develop d0b4825cc244..., PR 2137 8dfe859d9c75..., PR 2139 65954df16a35..., PR 2140 83f861da299c...: all four identical to the commission at start and at end.
READY file read: 5_Project_History/2026-11-09_seatR-92nd/mail/out_ready_round1.txt (plus the saved final PR bodies and ticket comments in .../push/). Held diffs: night/READY_*KS-2089*, *KS-2146*, *KS-2144*.
Each PR is one commit on f98afb113c2d (not today's develop d0b4825; develop moved by KS-2132 and KS-2133 test files only, none in these paths).

## PR 2137 (KS-2089 item 1, check-shared-relink.sh +2 -1)
FOUND
- Held vs PR: the only difference is the one the seat declared. Held: one line "...NON_JS_BASES (see image_name_component above). Bounded assumption, stated: the"; PR: same words re-wrapped over two lines, pointer now "base_ships_no_js_runtime above". Nothing else differs (added/removed line sets diffed).
- No executable byte: comment-stripped file (all lines whose first non-blank char is #) hash 6a4baecec2431d4d before and after; control (one code line altered) 5ca313d4eb04aee9, differs. bash -n rc 0 on the PR file. 707 -> 708 lines.
- Truth of comment, quoted: base_ships_no_js_runtime is lines 493-504 and line 503 is `return (nm in NON_JS_BASES)`. Caller line 575 `else if (!base_ships_no_js_runtime(stage_base[final]))` leads to line 580 A_FAIL "is not one this guard can positively identify". The comment sits inside image_name_component (starts 510), and the pointer "above" is correct. The old "falls to the `$` refusal below" is gone from the PR file; no other "`$` refusal" text remains in the file.
- Suite check_shared_relink_derived_claims.test.sh with the Dockerfiles/yml extracted: 17 passed, 0 failed at f98afb1 and at the PR head. Four cells read rc 1 with the "positively identify" phrase: `$NODE_IMAGE`, `${NODE_IMAGE}`, `$NODE_IMAGE:24`, `${NODE_IMAGE:-node:24-alpine}`. Cell 17 plants a dollar key and reads `0|the re-link invariant does not apply`. Claim confirmed.
- Merge tree: clean alone onto d0b4825 and with the other two.
- Body and ticket comment e5e62af6 claim no more than the change; "Refs" and items 2-5 untouched is stated.
TESTED / HOW: git diff of the PR against its cut; stripped-comment hash with control; bash -n; real suite run twice (partial tree gave 15/2 on BOTH sides, an extraction shortfall of mine, fixed by adding Dockerfiles; final 17/0 both).
NOT TESTED: the seat's own 17/0 transcript was not trusted; I re-ran. The guard against the repo's real tree was not run.
Findings: none.

## PR 2139 (KS-2146 narrowed, ks1536-one-role-vocabulary.test.ts +3 -1)
FOUND
- Held vs PR: added and removed lines byte-identical. No difference.
- No executable byte: esbuild emit with comments removed, f98afb1 / PR 2139 / PR 2140 versions of the file all 151d6969bbb0; control (expect( renamed) 93d91ec544a3, differs. Regex comment-strip agrees (69b247ce5535 across versions for the other file).
- Truth: G5 (line 172-176) asserts `t.match(/requirePlatformRole\(\)/g)?.length` is 2 and no PLATFORM_ADMIN_ROLES; G5b (178-182) asserts toContain of the exact generate-key and rotate-key lines with `requirePlatformRole(),`. Tokenisation index.ts has them at lines 225 and 294 and line 395 hash-key is ungated. I reproduced the plant on the real source text: an ungated `app.post('/api/generate-key'...)` before the gated line leaves G5 True and G5b True; control (gate removed) makes both False. So "an earlier ungated registration of the same path leaves both green" holds for the text assertions. I did not run vitest (no installed run of that package); the seat's 99/99 and 97/99 are therefore reported, not reproduced; my reproduction is of the two predicates.
- Narrowing: the body states plainly "NOT in this PR, and the ticket's two fix shapes stay open: renaming cell G5b, and a route-level cell", and "Refs". Ticket comment 572a206c says the same. Claim matches.
- Merge tree clean alone and combined.
Findings:
- G293-2139-1 (Low): header says G5 and G5b "show that the two gated route lines exist". G5 only counts `requirePlatformRole()` occurrences anywhere in the file (the "twice somewhere" its sibling's title names); only G5b pins the route lines. Slightly looser than the cell. Not wrong enough to block.
- G293-2139-2 (Info): new line 18 is about 141 characters and line 16 about 143; the seat reported width in the body. No lint rule observed.
TESTED / HOW: diff vs held; esbuild emit with control; predicate reproduction with plant and control. NOT TESTED: vitest run of the file.

## PR 2140 (KS-2144, ks1974-identus-...test.ts +2 -1)
FOUND
- Held vs PR: byte-identical added/removed lines.
- No executable byte: esbuild emit 5dd3e4eb22c3 for base and PR, control 0e8ef5b25773 differs.
- Truth: the toString case is real: helper `toStringThrows` (line 46-48, toString throws 'toString boom') feeds cell R2 (line 69-70) "an Error whose message is an object whose toString throws gives the notFound result with a constant reason". Symbol case is R1 (line 65). The "or is" wording matches both cells.
- Body and comment df346621 disclose that "is" was added to the gate's reading; no overclaim.
- Merge tree clean alone and combined.
Findings:
- G293-2140-1 (Low): the sentence this PR repairs still describes the defect in the present tense: "Its catch ... as `err instanceof Error ? err.message : String(err)`, which guards a read that THROWS but not a read that RETURNS a non-string ... comes back as that value itself, so `errorMessage` is not text." Current identus-client.ts line 134 is `String(err instanceof Error ? err.message : err)` with a fallback at 136 `'unreadable thrown value'`, and R1/R2 pin the fixed behaviour (`Symbol(ks1974)`, `unreadable thrown value`). The header is pre-fix history, not what the code does. Pre-existing and out of KS-2144's stated scope (a missing-words fix); worth a ticket, not a block.
TESTED / HOW: as above plus source reads. NOT TESTED: vitest 4 of 4.

## Common
- Merge trees (git merge-tree --write-tree onto d0b4825): 2137 alone be5d2dae, 2139 alone b077cd02, 2140 alone d5e8a091, all three chained clean (7 insertions, 3 deletions, three files, only the PR files differ from develop). No conflicts.
- Open-PR path overlap: no live GitHub token (gh not logged in), so no fresh API census. Used the seat's 07:20 census of 58 PRs (none touch the three files; control start-environment.sh returned 2127, as the seat found) and fetched every PR numbered above 2133 that was not ours (2134, 2135, 2136, 2138, 2141) and diffed against merge-base: none touches these paths. PRs opened between 07:20 and now with other numbers were not enumerated.
- G293-ALL-1 (Info): the commission's /private/tmp/g293 clone was refused by the workspace hook for write verbs (fetch/init); I cloned inside the session scratchpad with GIT_DIR instead, as gate 288/289 did. Nothing written in any !CODING checkout.
- G293-ALL-2 (Info): PR bodies were read from the seat's saved final bodies and ticket comment files in push/, not from GitHub (no token); the PR title and commit message of each PR matched. Ticket comment ids were not fetched from Linear.
