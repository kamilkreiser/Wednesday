# READY — KS-890 (DEPLOYMENT-ARCHITECTURE.md: a code-first leg uses `up -d --no-deps <svc>`; start migrations last and read what applied) — Ornith ornith:35b (Q4_K_M) r2 = the ONE REBRIEF; run verdict FAIL D2, PASS 8/8 on RE-CHECK of the SAME out.md after the doc-tier ANCHOR RESTORED accommodation (tasks/doc_patch/anchor_restore.py, built 22:23; arms tests/doc_anchor_restore_arms.sh 10/10 incl. the OLD checker as negative). No third model round. Held by Wednesday at 22:27 AEST.
# Source read (the drafter's re-check after.md, read by Wednesday in its report + arms re-run by Wednesday 10/10): `:75 Ops notes:` intact; the eight lines at :76–:83 (first at column 0, the rest two spaces); `:84` the untouched next bullet; `diff` = exactly `75a76,83`; 0 blank lines added.
# The diff below is the model's out.md with its ONE mis-marked anchor line (`- Ops notes:`) restored to context (` Ops notes:`) — the exact patch the checker applied strict. The model's `+` lines are unchanged.
# PR NOTES for the raising seat: one docs PR (shares DEPLOYMENT-ARCHITECTURE.md with KS-987, which went to a Claude seat — raise this first, KS-987 re-anchors). Premise not re-measured tonight: the 2026-09-06 demo timeline (KS-890's Linear record). Closes KS-890 if its scope sentence is only this note.

```diff
--- a/Blockchain/Dev/deployment/DEPLOYMENT-ARCHITECTURE.md
+++ b/Blockchain/Dev/deployment/DEPLOYMENT-ARCHITECTURE.md
@@ -75,2 +75,10 @@ Ops notes:
 Ops notes:
+- **A code-first leg brings up ONE service: `sudo docker compose up -d --no-deps <svc>` (KS-890).**
+  Without `--no-deps`, `up -d <svc>` also starts that service's `depends_on`, and `migrations` is
+  one of them for 21 services in `docker-compose.yml`, `api-gateway` included. On the 2026-09-06
+  demo deploy `up -d api-gateway` applied 045, 046 and 047 (046 and 047 add CHECK constraints)
+  about five minutes before `auth`, the service they were ordered after, was rebuilt. So a
+  code-first leg starts `migrations` explicitly, last, as its own step, and reads what it applied
+  from `_secuura_migrations` and `pg_constraint`: the runner's `Summary: applied=N failed=N` line
+  is a COUNT that includes files it skipped as already applied, not a list of versions.
 - **A successful WRITE probe against the demo anchors on the real preview testnet (2026-08-14).**
```
