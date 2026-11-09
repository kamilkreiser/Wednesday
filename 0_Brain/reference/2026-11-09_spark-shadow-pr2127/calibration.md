Spark shadow PR 2127: verdict GO WITH NOTES (Claude gate 283: NO GO, mismatch); recall 0/7 of G283 findings (1 partly: G283-1 mechanism only); FP 0 false at source (2 empty/garbled Notes)

# Calibration 6, 2026-11-09 ~16:2x: PR 2127 (KS-785, tier 1) round 1, head 190ffa868d7d9abac61401d84d654944c042cfc7, develop 204e62acdc35 (merge-base 4d6b7bb17fd3)
Method: blind run (verdict.md read only after review.json existed). Clone /private/tmp/spark2127/clone (blobless, repo deploy key as core.sshCommand). Suite Blockchain/Dev/scripts/__tests__/check_slot_credentials.test.sh. Evidence: /private/tmp/spark2127/{out2,review}/ (facts.json, diff.patch, review.json, prompt_user.txt).

## Deterministic half
Head 39/39; base (merge-base product code) 36 pass / 3 fail. Matches gate 283 exactly (39/39; develop 36/39, the 3 predicted cells). Gate ~59 s with no model. First run used base-ref `origin/develop` and silently produced merge_base "", diff 0 files, and a BASE run of 39/39 (bogus, base == head). Rerun with `develop` is the one scored.

## Spark review half
Prompt 30,259 tokens, completion 1,039, 66.1 s, one attempt, valid JSON, no repetition. Verdict GO WITH NOTES, 6 findings, all Note, 0 overstated sentences. Inputs missing: ticket text (no Linear key: the tool's default reads a real .env, which the commission forbids) and the PR body (no gh identity; the PR's commit message was supplied as a labelled stand-in).

## Scoring against gate 283
| id | sev | Spark | note |
|---|---|---|---|
| G283-1 fresh-clone start dies at `source` (env.example:236 `ISSUER_NAME=Secuura Platform`, rc 127) | Blocker | PARTLY (Note 1 only) | Spark noted `source` executes the .env as shell and nobody ran a real .env. It never saw env.example (0 hits for ISSUER_NAME in the prompt: the file is untouched and uncited) and never named set -e abort. Severity Note, verdict wrong. |
| G283-2 malformed .env prints secret tail and stops start | Major | MISSED | |
| G283-3 `bash -x` prints .env values | Minor | MISSED | |
| G283-4 ports/NODE_ENV reach beyond the passwords, undisclosed | Minor | MISSED | |
| G283-5 mutants `set -a` and `|| true` stay green | Minor | MISSED | Spark Note 5 (shape (b) untested) is a different point. |
| G283-6 comment overstates "value compose gets on either path" | Note | MISSED | |
| G283-7 OVL_IGNORE_PRS conduct | Note | MISSED | needs the READY/brief, outside the tool's inputs |
Verdict: Spark GO WITH NOTES vs NO GO. Wrong direction (missed a Blocker). Facts: match (39/39, 36+3).

## Spark's own findings, checked at source (head 190ffa86)
1. Note: source runs the .env as arbitrary shell, no real-stack run. TRUE (start-environment.sh:142-145 sources it; flow fragment "never run against a real stack"). Real but understated; overlaps G283-1/2.
2. Note: agreement shown only against a stub docker. TRUE (test file:409-413 quoted exactly). Matches gate 283's own "fixtures only" limit; no new information.
3. Note: "154 non-comment lines identical" not in facts. TRUE and fair as UNMEASURED (gate 283 measured 135 non-comment non-blank and did not reconcile 154).
4. Note: "three red cells" count supported but cells unnamed. EMPTY (count 36/3 matches; asks for a name).
5. Note: shape (b) is reasoned, not tested. TRUE, low value.
6. Note: fragments "included" claim. EMPTY and garbled ("included)Skip;"); it asserts nothing wrong.
Evidence quotes are accurate; `evidence_quote_found_in_input:false` on 1, 2, 4, 5 is a whitespace/line-wrap artefact in the checker (the flow fragment and test comment quotes exist verbatim across line breaks).
Pattern: after the 2026-10-30 checklist amendment the false NO GO shape is gone (no Major, "not in facts" reported as Note), but the opposite failure appeared: the Spark cannot run code, so it cannot find a defect that only execution reveals. Tier 1 stays Opus. Running tier 1 record: 0 usable of 3.

## What the tooling or checklist should change
1. spark_gate.sh: normalise a `origin/` prefix on <base-ref> (or REFUSE), and make shadow_facts.py exit non-zero when merge_base is empty or diff files == 0. Today it writes a green facts.json with a bogus base run.
2. spark_review.py: add `--ticket-file` / `--pr-body-file` fed from a pre-fetched path, and stop defaulting --linear-env to a real .env; the ticket (acceptance lines) was absent so checklist D never ran.
3. Context builder: for every file the new code `source`s, includes or reads, add the committed template/default sibling (`env.example`, `*.example`, defaults) to the prompt. The decisive file here was in the repo but not in the diff.
4. REVIEW_CHECKLIST.md: new item under A or C: "If new code sources/parses/executes a file, name the shipped template of that file and say whether the new code can process it; if the template was not provided, say so as a Note." Also: "tests that stub a collaborator and feed minimal fixtures cannot see realistic input: name the stub and the missing realistic case."
5. Deterministic half: add an optional "realistic-input" arm (run the touched script against the repo's own template under a stub PATH, as gate 283 did) so the Blocker is measured by a script, not left to the model.
6. spark_review.py evidence check: compare after collapsing whitespace and comment markers.
7. Post-process: drop findings whose claim says only "unmeasured/count matches" (Notes 4 and 6 are padding).

Conduct: nothing written under /Volumes/DevMASTER/!CODING; no push/post/mail; no .env opened; no rm. Workspace /private/tmp/spark2127 = 893M (clone + two worktrees). Spark answered throughout.
