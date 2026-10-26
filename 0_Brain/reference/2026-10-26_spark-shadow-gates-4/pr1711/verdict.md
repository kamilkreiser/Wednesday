# Spark shadow verdict PR #1711 (findings only, no scoring)
Verdict: **NO GO**
HEAD {'files': 1, 'files_ok': 1, 'files_failed': 0, 'passed': 15, 'failed': 0, 'count_unparsed_files': []}  BASE {'files': 1, 'files_ok': 1, 'files_failed': 0, 'passed': 15, 'failed': 0, 'count_unparsed_files': []}
tokens: 11208 prompt / 972 completion, 38.5s, 1 attempt

1. [Major] The new test suite passes on the base product code, so it does not actually verify the fix; it is red only by absence of the new symbol, not by behavioral failure.
   evidence: facts.json targeted_on_base_product_code: "rc": 0, "ok": true, "passed": 15, "failed": 0 for systemTest/__tests__/generated_guard_restore.test.sh
   The test suite is designed to fail on the unfixed guard (e.g., line 130-133 expects 'restoring .* FAILED' which the old code never prints), but it passes on base, meaning the test is not actually exercising the old behavior—likely because the test file itself is new and the base run uses the new test file against the old guard, yet the test still passes, indicating the test is not sensitive to the change.
2. [Major] The test suite's fake cp instrument is not faithful to the real cp: it fails only on a destination suffix, but the real cp can fail for many other reasons (permissions, disk full, etc.), so the test only covers a narrow failure mode and does not prove the guard handles all restore failures.
   evidence: systemTest/__tests__/generated_guard_restore.test.sh:59 `*$1) echo "fake cp: refusing a copy into \$last" >&2; exit 1 ;;`
   The fake cp only fails when the destination ends in a chosen suffix; real cp failures are not limited to that, so the test does not validate the guard's behavior under other failure causes.
3. [Minor] The test suite does not verify that the guard's stderr messages are actually written to stderr; it only checks the combined output file, so a message written to stdout would also pass.
   evidence: systemTest/__tests__/generated_guard_restore.test.sh:90 `PATH="$WORK/fakebin:$PATH" /usr/bin/env bash "$WORK/$DRV_LABEL/driver.sh" > "$DRV_OUT" 2>&1`
   The test redirects both stdout and stderr to the same file, so the assertions on 'restoring .* FAILED' and 'KEPT at' do not distinguish between stdout and stderr, even though the guard's contract is to write to stderr.
4. [Minor] The test suite's 'clean run' control does not verify that the guard's snapshot copy is actually performed; it only checks the restore, so a guard that never snapshots would still pass the clean-run control.
   evidence: systemTest/__tests__/generated_guard_restore.test.sh:116-120 (control block) and the guard's snapshot at support/generated_guard.sh:33 `cp -R "$GENERATED_GUARD_GEN/." "$GENERATED_GUARD_STASH/" 2>/dev/null || generated_guard_snapshot_ok=0`
   The clean-run control only checks that the sentinel is restored and the stash is removed; it does not assert that the snapshot copy was attempted, so a guard that skips snapshotting would still pass.
5. [Note] The test suite's use of `mktemp -d "/tmp/ks1735.XXXXXX"` is not portable across all Unix-like systems (e.g., macOS requires a template with at least three X's and the directory must exist), which could cause the test to fail on non-Linux environments.
   evidence: systemTest/__tests__/generated_guard_restore.test.sh:45 `WORK="$(mktemp -d "/tmp/ks1735.XXXXXX")" || exit 2`
   The template is Linux-specific; on macOS, `mktemp -d` requires a template with at least three X's and the directory must exist, so this may fail on macOS.
