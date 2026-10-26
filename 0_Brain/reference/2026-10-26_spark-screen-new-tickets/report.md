# Spark screen of new KS tickets - 2026-10-26 12:33 AEDT

Result: 8 tickets read whole (description, comments, attachments) from Linear; 0 BRIEFED, 8 REJECTED. No brief folder was written (nothing fits; a valid result).

Develop sha read: 28dac5c12ba5c00d9fc3ad04daee5230eff71619 (git ls-remote origin refs/heads/develop; the shared checkout's own HEAD is the older 1ae6f17d19a8, so I read the tip from my own clone at .../scratchpad/screen_clone via git show, objects present locally). Census: KS Backlog/Todo with updatedAt >= 2026-10-25 = exactly these 8 (KS-1079 is the only one created earlier).

## Partition measured
- Seat R READY files (night/READY_*_2026-10-26*): .dockerignore + packages/shared ks1289 test; frontend/issuer package.json + ks1391 test; api-gateway ks1510 / ks1512 / ks1649 tests + docs/developer-portal.html; scripts/__tests__ ratchet_leg, tenant_isolation_stderr_own_file, ks1513/1527/1560 .test.sh; systemTest/scripts/check-package-format.sh + ks1716 test (branch feature/ks-1716 b3a063dd33b9: those 2 files).
- Seat J branch feature/ks-1717-signed-emitter-hop dfc89078979b vs develop: .env.example, env.example, deployment/azure/services.bicep, docker-compose.yml, docs/ENVIRONMENT-VARIABLES.md, packages/shared/src/index.ts, packages/shared/src/security/emitterSignature.ts (+test), services/anchoring/src/emitterGuard.ts, anchoring/src/index.ts, originate/src/routes/documents.ts, ks1293 manifest test, 2 new originate tests.
- Seat K KS-1683: PR ref 1683/head exists (75078aef7904); vc-issuer list and by-hash routes, not diffed further because no screened ticket touches vc-issuer.

## Per ticket
| id | title (short) | verdict | failed clause | files | verified by |
|---|---|---|---|---|---|
| KS-1727 | shared wallet-signature.test.ts positive cell red | REJECTED | security surface (CIP-8 signature verification, used by /sign-wallet); fix shape not derivable (cause unmeasured, ticket says so) | packages/shared/src/cardano/wallet.ts:352-420, __tests__/wallet-signature.test.ts:47-49 | read both at tip; verifier is Ed25519/COSE logic; no hypothesis in ticket |
| KS-1726 | five stale fail-open comments (GATEWAY_VOUCH_SECRET) | REJECTED | no runnable test (comment/doc only, no red-first); 5 sites in 3 files (>3 edit points); and COLLIDES with Seat J (bicep, docker-compose, ENVIRONMENT-VARIABLES.md are in the 1717 branch diff) | services.bicep, docker-compose.yml, ENVIRONMENT-VARIABLES.md | ticket read; diff --stat of 1717 branch |
| KS-1725 | plan zod 4 / msal-node 7 | REJECTED | planning/dependency upgrade across 25+ locks; security advisory; not a file edit | many lockfiles | ticket read |
| KS-1724 | uncapped request-body arrays | REJECTED | decision-shaped (what cap, which of 232 sites, express limits); 118 parse sites; security/DoS design | many | ticket read |
| KS-1722 | governance proposerId blank lists all | REJECTED | fix shape not chosen (400 at route vs !== undefined in service vs adopt unused ProposalQuerySchema; ticket lists none); data-exposure/authorization-adjacent, tenant scoping "not examined" | services/governance routes/governance.ts:142-154, services/governanceService.ts:245-249 | read both at tip; jest suite exists but no chosen shape |
| KS-1721 | schemathesis symlinked-venv test fails on Linux | REJECTED | fix shape not spelled out (change the test? skip on Linux? change guard in scripts/venv_reexec.py?) = decision; Python/pytest 3.14 env the kit checker does not run; inference only partly measured | systemTest/schemathesis/scripts/venv_reexec.py, tests/unit/runner/test_prevenv_bootstrap.py:317 | read venv_reexec.py docstring and test list at tip; QA comment confirms macOS pass, so platform-dependent |
| KS-1720 | plain mypy tests/ aborts | REJECTED | no in-process test to copy; config-only edit that would not make validate-lint pass (317 errors remain with the flag); not red-first | systemTest/schemathesis/pyproject.toml, validate-lint.sh | ticket read |
| KS-1079 | kintsugi demo-service gate | REJECTED | decision-shaped ("a decision with a stated reason"), ops/config on two boxes, security gate flag | none in repo | ticket + 3 comments read |

## UNMEASURED
Nothing was run (no jest, vitest, pytest). KS-1727's root cause was not reproduced. Seat K's file list was not diffed.
