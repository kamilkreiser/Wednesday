# KS-1350: Spark brief (RUNG 3, comment_patch), originate routes/webhooks.ts fail500 docblock

Written 2026-09-27 02:1x AEST by a Spark brief-writer/runner sub-agent for Wednesday. Git write verbs ran only in scratch clones (develop 94c9c7aa). Nothing written in any Secuura folder; nothing queued, pushed or held.

- Tier: **comment_patch**, not doc_patch. doc_patch grades markdown `## ` sections (D4-D6) and a .ts docblock has none, so it cannot grade this honestly. comment_patch was built for exactly this (C4 token equivalence proves no code token changed).
- `KS-1350.md` is the brief: one hunk `@@ -549,13 +549,16 @@`, 8 '-' / 11 '+', comment lines only.
- `golden/`: `KS-1350.golden.diff` (extracted from the fence), `webhooks.fixed.ts` (the golden result), `ks1350_verify.sh` + `verify.out` (strict apply; tsc --noEmit originate rc 0 and eslint webhooks.ts rc 0 at the tip AND on the result), `build_input.out`, `ks1350_round.sh` (the round script).

## Build (rc 0)
```
NIGHT_SOURCE_CHECKOUT=<scratch clone at develop 94c9c7aa> \
bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/build_comment_input.sh KS-1350 <run>/input.json \
  /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1350/KS-1350.md \
  product=Blockchain/Dev/services/originate/src/routes/webhooks.ts
```
Then `tasks/comment_patch/prepare_clone.sh`, `LM_BACKEND=spark SPARK_THINK=0 local_model_task.sh tasks/comment_patch/task.md …`, `tasks/comment_patch/checker.sh …` + A2a (`a2a_anchor.py` over the checker's patch.diff, the way KS-789 ran it).
