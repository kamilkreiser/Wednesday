Paste this block as the CodeQL step of a gate commission.

```
CodeQL STEP (required, before landing; replaces "CodeQL 0 new by result rows"):
  Run, one CodeQL process at a time, with a scratch clone as --checkout (the project checkout is read-only):
    /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/tools/codeql/pr_codeql_check.sh \
      --repo <owner/name> --checkout <scratch clone holding base+head> --base <PR base sha> --head <PR head sha> \
      --lang <javascript|python|...> --work <scratch dir> --threads 4 > <scratch>/cq.out 2> <scratch>/cq.err ; echo rc=$?
  Paste the full verdict table (the lines from "VERDICT TABLE" to "RESULT") and the rc into the report.
  Read it: KEPT = results the hosted PR check would show (a path touches a line the PR adds); NEW = fingerprints head has
  that base lacks. Only high+ counts (security-severity >= 7.0, else problem.severity error).
    rc 0  pass: KEPT high+ 0 and NEW high+ 0.
    rc 1  WOULD BLOCK: this is a MAJOR finding and a landing blocker. No dismissal, no bypass: reshape the change so
          no result path touches an added line (e.g. leave the flagged read byte-for-byte as on base), then re-run.
    rc 2  tool error (missing sha, DB or analyze failure, one-sided empty result): resolve it and re-run; rc 2 is never a pass.
  Residual: this is a local approximation (CLI 2.27.4, start-line post-filter proven on one PR). The hosted CodeQL check
  on the landing head stays the authority; if it disagrees, hosted wins and the disagreement goes to Tuesday.
```
