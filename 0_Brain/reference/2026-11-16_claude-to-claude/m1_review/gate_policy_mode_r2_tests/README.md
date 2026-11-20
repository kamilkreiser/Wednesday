# QA-POLICY-MODE-R2 tests and probes (copies; run from worktrees of the checker's own clone)
- zz_r2_modecmp.rs: lines 1-613 of the first check's zz_qa_mode.rs (scratch path prefix qpm/ -> qpm2/ only) + a writer of every decide_with_mode result. Compiled at fc7acfc and 443549c; compared by cmp_modes.py.
- zz_r2_inc/cases.rs: the shared probe list (included by the two files below; place it in tests/zz_r2_inc/).
- zz_r2_absent.rs: mode-absent `decide` for every probe (compiles at main, fc7acfc and head; outputs must be identical).
- zz_r2_probes.rs: every probe three ways (absent, live unverified, live verified); QA_ASSERT=1 asserts no M1/N3 probe is a mode allow.
- probe_output_*.txt: the outputs (columns: class | name | absent || live shell-unverified || live shell-verified, surface Console).
- mutant_*.diff: the five mutations (m5, m8 = the first check's; ma, mb, mc = mine), each in its own worktree and target dir.
- wait_and_check.sh: the heavy-slot waiter that ran scripts/check.sh at the head.
- zz_qa_diff.rs was reused UNCHANGED from ../gate_policy_mode_tests/ (not copied here).
