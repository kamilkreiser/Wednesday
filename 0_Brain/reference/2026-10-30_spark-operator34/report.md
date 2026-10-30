# Spark operator 34, 2026-10-30 (Secuura only). Filed by the Wednesday seat from the agent's returned text.
- One task run, PASS 7/7 on the original brief, no rebrief, byte-identical to golden. Rung 3, 59 s round, 27 s model, 12458+872 tokens. Second task not run, to save allowance.
- Ticket: KS-1868, one site: demo-service src/index.ts:40 boot gate. Brief: 2_Project_Files/local-model/night/briefs/ks_1868_p1_demo_boot_gate_unreadable_throw/. Run dir: 2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1868_p1_demo_boot_gate_unreadable_throw.
- Held: local-model/night/READY_KS-1868-KS-1868-O34-P1_*. Inline inner try, fallback 'unreadable thrown value'; suite 86 -> 88.
- Overlap: all 30 open PRs' file sets via the GitHub API; control: services/auth found in 10 PRs. No PR touches demo-service src/index.ts or its __tests__; demo-service/package.json is in 2 PRs.
- Control run failed 4 times before the model call, all brief or test-authoring faults (vi.fn gate vs a revoked Proxy; red cell failing on a throw, not an assertion; cell title format; ## Red cells entry format).
- Next candidates, open-PR free per the scan: vc-issuer presentations.ts:182, credentialRepo.ts:432 (one-site briefs); kyc and security index.ts; tokenisation index.ts.
- NOT checked: tsc/eslint/whole-package outside the checker; a real boot of index.ts; the other 252 sites; other live seats' local demo-service work beyond the PR scan; the cache clone's develop not re-fetched.
- Wednesday's read: the diff's context line equals index.ts at 3974f364cbc8; product change is 6+/1- as stated; FATAL and exit(1) unchanged. Read at source AFTER hold_ready.py stamped "by Wednesday": that stamp was the operator's run.
