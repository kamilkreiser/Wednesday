# QA gate PR #1461 (KS-1405) - verdict: GO WITH NOTE

Head: fa84d8bc3b5738383cdb1314c8b201acbe936c1d (parent a31b77577). Own clone, read-only on shared repo.

1. Diff: 2 files +91/-1. Wrapper = Spark product hunk (mktemp default; blank line moved only) + one guard line (run-schemathesis.sh:27). Test = Spark's 75 lines + CASE_TMPDIR export, RC_NOTMP run, cell 4, PASS==4 (diff-verified, nothing else).
2. Cells (own runs): original 2 pass/2 fail (cells 1,4 red); Spark-fixed 3/1 (cell 4 red); hardened 4/0, also under /bin/bash 3.2.57. Mutants each turn a cell red: default "." -> c1+c4; ignore env -> c3+c4; guard exit 0 -> c4; guard without exit -> c4; message changed -> c4; TMPDIR ignored -> c4. Controls: full-suite 4/0 on hardened.
3. Runner --list 79 (ks1405 listed once), --check-unreached OK; orchestrate_jobs.test.sh byte-unchanged, 18/0/0 pass.
4. Semantics: no -e, so guard is required and reachable (TMPDIR=/nonexistent -> rc 1; explicit empty FINDINGS_DIR falls to mktemp, fine). Only caller orchestrate.sh:159 always passes a non-empty FINDINGS_DIR. Quoting fine; template XXXXXX trailing is portable (macOS, GNU, busybox); trailing-slash TMPDIR benign.
5. Docs: ci/README.md and systemTest/README.md do not state the default; no change needed.

Defects
- Minor 1: test leaks one run-schemathesis.XXXXXX dir per run in the real TMPDIR (default run's mktemp is not redirected into $WORK; trap removes only $WORK). Test file lines ~38-50 (run_case / dflt). Fix: export TMPDIR="$WORK/tmp" for the default case.
- Minor 2 (note): wrapper header Env block (run-schemathesis.sh:14-16) does not state the new default or that the temp dir is not cleaned; path is printed on the final "wrote" line, so acceptable.

Could not check: real GitHub Actions run, Linux bash/mktemp (reasoned only), pushed-PR head (used the worktree branch head).
