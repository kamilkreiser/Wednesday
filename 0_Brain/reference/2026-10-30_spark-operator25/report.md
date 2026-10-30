# Spark operator 25 — report (saved by Wednesday from the returned text; the agent's own write was refused by a tool)
Basis develop 85cd24d81cb9; drainer 97411; none started. 12 of 20 sibling check-*.sh guards screened with a planted real violation (excl. check-no-sql-injection.sh, E 22nd's).
- 4 real defects, 4 rounds, 4 PASS 7/7 (no rebrief), all held under local-model/night/READY_KS-0-KS-0-O25-P{1..4}_...:
  - P1 check-dockerfile-non-root.sh:27 — BSD sed -E has no \s, so USER root / USER 0 print OK rc 0 on macOS; no-USER Dockerfile dies silently rc 1. (checker reanchored the hunk: strict=False)
  - P2 check-no-strictness-patches.sh:46 — no --exclude-dir=node_modules: a vendored flip fails the gate; packages read 6x per run.
  - P3 check-connector-xss.sh:23 — walks node_modules then post-filters (cost only).
  - P4 check-no-pii-store.sh:56 + :64 — `git ls-files --exclude-standard=false` is invalid (rc 129 hidden by || true): untracked leg dead; once fixed, :64 exits 1 inside a warning-only block. Raise both hunks together.
- Clean with firing controls: no-default-passwords, no-math-random, no-trust-header-reads, test-wallet-testnet, no-latest-tags, env-consistency (rc 2 cosmetic), production-guard, script-portability.
- Not screened (8): need a stack/az or large: akto-container-names, app-db-password-default, container-isolation, environment, no-demo-mutation, shared-relink, slot-credentials, stack-safety.
- Note (not briefed): check-test-wallet-testnet.sh says "nothing to check" for an `export LACE_WALLET_ADDRESS=addr1...` line.
- Faults: generator wrote 4 brief dirs to 0_Brain/night/briefs (GEN_BRIEFS unset) -> quarantined to ./_quarantine_2026-10-30/misplaced_night. Lesson: set -euo pipefail + $(grep) finding nothing = silent kill; BSD vs GNU \s = silent wrong answer.
- Raise: no tickets exist (raise seat files them); before merging P1 run it over the real services/ tree (it will now name any root/no-USER Dockerfile). P4 may warn on other untracked *pii*.json (rc stays 0).
- Next: plant hits in the suite-less unscreened guards with PATH stubs for docker/az; prune run dirs (~335 MB each).
