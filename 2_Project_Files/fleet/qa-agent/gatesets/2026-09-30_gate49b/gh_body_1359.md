gate47 N-1350-7. The startup-migration predicate exits 1 for two different reasons — the migrations
genuinely failed, or the check could not be verified (python3 absent, and after the present-but-broken
fix, a python3 that cannot run). Both callers printed a line claiming the migrations FAILED, which is a
stronger claim than rc 1 supports.

Message text only. No exit code, no counter, no branch change: rc 1 still counts an ERROR and rc 2
still counts a SKIP, each pinned by a control cell in the new suites.

    deploy.sh:857      "startup migrations FAILED - see above"
                    -> "... FAILED or could not be verified - see above"
    deploy-all.sh:312  smoke value "one or more failed"
                    -> "failed or could not be verified - see above"

The `deploy-all.sh` twin was not named by the gate; a local-model screen found it. Both are fixed here
so the two callers cannot drift apart again.

## Test Evidence

**Touched:** `Blockchain/Dev/deployment/azure/deploy.sh` (100755, +2/−2),
`Blockchain/Dev/deployment/azure/deploy-all.sh` (100755, +2/−2), and two new shell suites (100644):
`ks1054_deploy_sh_rc1_message.test.sh`, `ks1054_deploy_all_rc1_message.test.sh`.
No service code, no migration, no config, no lock, no gate file.

**Provenance, checked before applying anything:** each patch's diff block was extracted from its held
pass and compared against the golden in its brief directory — **byte-equal, `cmp` rc 0** (4783 B and
4617 B). `git apply --check` rc 0 for each at the base.

🔴 **The exec bit, because it actually bit here:** `git apply` dropped the executable bit on **both**
100755 files. Caught by `[ -x ]` on disk **before the first test run**, restored with `chmod 755`, and
the bytes verified unchanged (`cmp` rc 0). Committed modes read from the tree, not from `stat`:
**100755 ×2** for the deploy scripts, **100644 ×2** for the new suites — the 100644 pair is the control
in the same commit. After the later rebase onto the merged develop the bits were intact (a cherry-pick
preserves them where `git apply` does not), re-checked the same way.

**Ran — red-first on TWO runners, rc captured on its own line:**
- macOS: each new suite **4 passed / 0 failed** with the change. With **both** product files reverted to
  develop and the new suites kept: **3 passed / 1 failed each**, and the reds are **exactly M1** and
  **exactly N1**. Restored by byte copy (`cmp` rc 0 ×2, both `[ -x ]` YES) and re-green rc 0 ×2.
- `python:3.12-slim` (**bash 5.2.37, coreutils 9.7, Python 3.12.14**, `--network none`, source mounted
  read-only and copied to a writable layer): **4/0** and **4/0**; base **3/1** and **3/1**, reds
  **exactly M1** and **exactly N1**; restored and re-green rc 0 ×2.
- **The M2/M3 and N2/N3 control cells stayed green in every arm.** That is what pins the claim that this
  is message text only: rc 1 still counts an ERROR and rc 2 still counts a SKIP either side of the change.
- The reverted-product arms ARE the tamper arms — reverting the wording reddens exactly M1 / N1.

**Rebase:** cherry-picked onto the merged develop; the stored pre-rebase diff and the post-rebase diff
are **`cmp`-equal, rc 0**, with identical patch-ids (`116095428c4b1c7b59c8a4de8310aae2189fcf4b`). Both
new suites re-run green at the rebased head.

**NOT run / NOT covered:**
- `deploy.sh` and `deploy-all.sh` were **not driven end to end**; the cells exercise the predicate and
  the callers' message and counting paths, not a full deploy.
- The scripts were **not run against any real environment**. No deploy. **Merged is not deployed.**
- At a base without the present-but-broken fix the rc-1 "could not be verified" case already exists via
  python3 being absent, so these cells do not depend on that change landing first.
- No Schemathesis, Akto, k6 or Playwright run. Round 1 of 2 on this class.

**Migrations + config:** none.

Refs KS-1054
