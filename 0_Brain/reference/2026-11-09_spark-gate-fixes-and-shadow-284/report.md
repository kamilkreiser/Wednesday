Spark fixes A1-A4: 4/4 landed with red-proof; shadow 284: 2124 GO WITH NOTES 2125 GO WITH NOTES (salvaged) 2126 GO WITH NOTES; recall 1/3

(Saved by Wednesday from the operator subagent's final message, 2026-11-09 16:2x; the harness refused the subagent's own write. Content as the operator reported it, condensed; not re-measured by Wednesday.)

# Part A: tooling fixes (/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/gate/, .pre-1109-* backups, CHANGES.md; evidence /private/tmp/sparkfix284)
- A1 spark_gate.sh + shadow_facts.py: the base ref (develop, origin/develop or a 40-hex sha) is resolved to a sha in the clone; an empty merge-base or 0-file diff exits 6 and runs no base suite. Root cause: shadow_facts.py hard-coded origin/<ref> (origin/origin/develop -> empty merge-base). The OLD tool also failed with the develop SHA (empty merge-base, bogus 39/39 base). New: both forms -> merge-base 4d6b7bb17fd3, 5 files, base 36 pass / 3 fail, head 39/0; base = head refuses exit 6; unknown branch refuses exit 5. Two refusal arms added to tests/test_spark_gate_arms.sh.
- A2 spark_review.py: --ticket-file and --pr-body-file (old flags still work); --linear-env no longer defaults to the real .env; a missing input prints 'MISSING: ...' in prompt, facts.missing_inputs, stderr, meta and review.json; checklist tells the model to raise one Note rather than guess. Arm 5b updated.
- A3 evidence-quote check: strips whitespace, 'N: ' line numbers, '# ' markers, backticks and HTML tags; splits '...' elisions into segments. PR 2127 findings 2 and 5 flip to found; 1 and 4 stay not found correctly; two planted fabricated quotes stay not found.
- A4 checklist item 8b + template_siblings.py: up to 3 template siblings (400 lines each), nearest by path-component distance, as their own prompt section. PR 2127: old prompt 0 occurrences of ISSUER_NAME; new includes Blockchain/Dev/env.example line 236 (the G283-1 Blocker).
- A5 (added, same-session rule) salvage path: when both attempts loop, recover complete findings parsed before the loop, de-duplicate, derive the verdict, mark salvaged_partial=true. PR 2125: old rc 4 'SCHEMA FAILURE x2'; new rc 0, 7 findings.
- Existing gate tests pass (arms 1-5, 8 of 8).

# Part B: blind shadow on gate 284's batch (Claude verdict read only after all three Spark reviews)
- PR 2124: Spark GWN, Claude GWN (match). Head 9/9, base 6/3. 19,161 + 834 tokens, 42.9 s, 6 Notes all true at source (3 restate the PR's own disclosures). Missed G284-2124-1 (query-string '@' mis-print: needs executing the sed); found G284-2124-2 only as a copy of the PR's disclosure.
- PR 2125: Spark GWN (salvaged), Claude GO (mismatch, Notes only). No suite; facts via shadow_facts.py. 63,882 + 1,948 tokens incl. looped attempts. 5 of 7 Notes are 'not in the facts' padding.
- PR 2126: Spark GWN, Claude GO (mismatch, Notes only). 9,420 + 445 tokens, 22.8 s, 3 Notes true of inputs, nothing new. Missed G284-2126-1 (escaped echo of the password not matched).
- Recall 1/3; verdicts match 1/3; mismatches in the cautious direction; no false findings at source. The real misses need EXECUTING code (as on PR 2127).

# Owed
1. Realistic-input arm (run the touched script against the repo's template; probe shaped inputs like the 2124 URL case).
2. Drop padding Notes.
3. Comment-only 'stripped-equal' arm so the gate proves that claim itself.
4. --no-suite mode for spark_gate.sh.
5. Loop-prone large prompts: A5 salvages, does not prevent.
6. /private/tmp/sparkfix284 is 2.8 GB (8 gate worktrees), regenerable; not deleted.

# Conduct (operator's statement)
Nothing under !CODING; no push, post or mail; one in-process read of GH_TOKEN and LINEAR_API_KEY in /private/tmp/sparkfix284/fetch_inputs.py, nothing printed or in argv; nothing deleted; the Spark answered throughout.
