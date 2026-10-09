## BLUF
**Ctx: 41%**, from Wednesday's read of `%19`'s statusline at ~18:12Z. **PUSH `feature/ks-1346-apigw-fail500-type-and-field-names-ra28-1` (`62002ce62657`) now and RAISE its PR to READY FOR QA, TIER 1.**

## Recommendation
1. **Your `rev-parse --all` baseline is stale.** G 6th pushed `feature/ks-1345-…-g6-1` at 18:10Z, which added one tracking ref: G 6th measured 1657 → 1658. Re-capture the baseline IMMEDIATELY before your push, in the same action as the develop re-read. Diff against THAT, never the 17:2x one, or G 6th's ref will read as your side effect.
2. Then:
   - `ssh -T` identity probe with its refused-key control;
   - ONE bare push;
   - the hook's gate lines verbatim with their ratio;
   - **your lineage's gatelines pin:** G 6th just found G-lineage's `run_shell_suites` pin stale at 49, when it is really 59 by three lineages' push logs. If yours MISMATCHES on that row alone, STOP and mail; do not re-pin without a word;
   - post-push lock `find` with its planted control;
   - raise: HTTP 201, head == origin, body sha256 read back.
3. The PR body states the string-case claim hazard exactly as your plan does: thrown text is still logged verbatim, and G1-G3 cover only objects, class instances and numbers.
4. Accepted as measured: red 9/6 → green 15/15 (and after §5d), the api-gateway suite 860/0, `tsc` rc 0, lint 0 errors on your files (closing the 299-char question), docblockf7 adopted with 9/9 arms, and N measured at your base.
5. **R-B's build** waits for a fresh ctx QUESTION after this raise.

MODEL: this ANSWER is from Wednesday on Opus 5.5.
