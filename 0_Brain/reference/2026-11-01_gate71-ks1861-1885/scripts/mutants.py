#!/usr/bin/env python3
"""Gate 71 harness: base-product run and mutants for KS-1861 #1885.
usage: mutants.py base | mutants [ID ...]
 base    : run the PR's two files + the gate71 real-PG probe at the head; swap tenant-provisioning/src/index.ts to the
           develop blob the author built on (60e59bd2), run them again, restore, assert sha256.
 mutants : one unique-anchor replacement each (anchor count asserted == 1), run the PR's two files and then the gate
           probe, restore, assert sha256. Writes evidence/mutants.json.
Every run goes through scripts/probe_run.sh (nice -n 10, --maxWorkers=1, waits while load1 > 8, password scrubbed)."""
import subprocess, os, sys, json, hashlib, re
G = "/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate71-ks1861-1885"
R = f"{G}/repo"; D = f"{R}/Blockchain/Dev"; E = f"{G}/evidence"
TP = f"{D}/services/tenant-provisioning"; IDX = f"{TP}/src/index.ts"
PR_DEL = "src/__tests__/ks1861-tenant-delete-archives-and-keeps-every-row.test.ts"
PR_ST = "src/__tests__/ks1860-tenant-status-follows-the-documented-order.test.ts"
PROBE = "src/__tests__/gate71-realpg-probe.test.ts"
BASE = "60e59bd2270b5ec6e0e73e7823501188f8196403"
RUN = f"{G}/scripts/probe_run.sh"

def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()

def run(log, files, probe=False):
    args = ["bash", RUN, log] + (["--probe"] if probe else []) + files + ["--reporter=verbose"]
    p = subprocess.run(args, capture_output=True, text=True, timeout=1800,
                       env=dict(os.environ, GATE71_S1_OUT="/dev/null"))
    out = open(log).read()
    m = re.search(r"^\s+Tests\s+(?:(\d+) failed)?(?: \| )?(?:(\d+) passed)?", out, re.M)
    failed = int(m.group(1) or 0) if m else -1; passed = int(m.group(2) or 0) if m else -1
    reds = sorted(set(re.findall(r"×\s+src/__tests__/\S+ > (?:[^>\n]+ > )?([^\n]+?)\s+\d+ms", out)))
    return {"rc": p.returncode, "passed": passed, "failed": failed, "reds": reds, "log": os.path.relpath(log, G),
            "stderr_tail": p.stderr[-400:]}

def base_run():
    h0 = sha(IDX); saved = open(IDX, "rb").read(); res = {"head_index_sha256": h0}
    try:
        res["head_pr"] = run(f"{E}/base_head_pr.log", [PR_DEL, PR_ST])
        blob = subprocess.run(["git", "-C", R, "show", f"{BASE}:Blockchain/Dev/services/tenant-provisioning/src/index.ts"],
                              capture_output=True, check=True).stdout
        open(IDX, "wb").write(blob)
        res["base_index_sha256"] = sha(IDX)
        res["base_pr"] = run(f"{E}/base_product_pr.log", [PR_DEL, PR_ST])
        res["base_probe"] = run(f"{E}/base_product_probe.log", [PROBE], probe=True)
    finally:
        open(IDX, "wb").write(saved)
    res["restored_sha256_ok"] = sha(IDX) == h0
    json.dump(res, open(f"{E}/base_runs.json", "w"), indent=1); print(json.dumps(res, indent=1))

DROP_UNDER_FLAG = """    if (!archived) {
      res.status(409).json({ success: false, error: { code: 'CONFLICT', message: 'Tenant status changed while archiving; nothing was changed' } });
      return;
    }
    if (process.env.PROVISION_PER_TENANT_DB === 'true') {
      const adminPool = new pg.Pool({ user: PG_USER, password: PG_PASSWORD, host: PG_HOST, port: PG_PORT, database: 'postgres', max: 2 });
      await adminPool.query(`DROP DATABASE IF EXISTS "secuura_tenant_${slug.replace(/-/g, '_')}"`);
      await adminPool.end();
    }
"""
NOT_ARCHIVED = """    if (!archived) {
      res.status(409).json({ success: false, error: { code: 'CONFLICT', message: 'Tenant status changed while archiving; nothing was changed' } });
      return;
    }
"""
AUDIT_IN_TX = """        await client.query(
          `INSERT INTO platform_audit_log (action, target_type, target_id, details)
           VALUES ('tenant_archived', 'tenant', $1, $2)`,
          [req.params.id, JSON.stringify({ slug, previousStatus, erased: false })],
        );
        archived = true;"""

# (id, origin, description, anchor, replacement)
M = [
 # Re-runs of the author's mutants (re-written from their one-line descriptions; the author's patch text was not available)
 ("DM2", "author", "DROP DATABASE under PROVISION_PER_TENANT_DB=true after the archive", NOT_ARCHIVED, DROP_UNDER_FLAG),
 ("TB1", "author", "Kam's (b) removed: archived -> suspended refused", "  suspended: ['active', 'archived'],", "  suspended: ['active'],"),
 ("TB2", "author", "archived -> active admitted", "  active: ['provisioning', 'suspended'],", "  active: ['provisioning', 'suspended', 'archived'],"),
 ("SS1", "author", "provisioning dropped from the Delete start statuses", "const ARCHIVABLE_FROM = ['provisioning', 'active', 'suspended'];", "const ARCHIVABLE_FROM = ['active', 'suspended'];"),
 ("SS4", "author", "archived added to the Delete start statuses", "const ARCHIVABLE_FROM = ['provisioning', 'active', 'suspended'];", "const ARCHIVABLE_FROM = ['provisioning', 'active', 'suspended', 'archived'];"),
 # Gate 71's own mutants
 ("G71-M1", "gate", "race guard dropped: archive UPDATE without AND status = $2",
  "`UPDATE tenants SET status = 'archived', updated_at = now() WHERE id = $1 AND status = $2`,\n        [req.params.id, previousStatus],",
  "`UPDATE tenants SET status = 'archived', updated_at = now() WHERE id = $1`,\n        [req.params.id],"),
 ("G71-M2", "gate", "audit row written outside the transaction (on the pool, not the tx client)",
  AUDIT_IN_TX, AUDIT_IN_TX.replace("await client.query(\n          `INSERT", "await platformQuery(\n          `INSERT")),
 ("G71-M3", "gate", "no ROLLBACK in the catch (aborted connection returned to the pool)",
  "      await client.query('ROLLBACK').catch((rollbackErr: unknown) => {", "      await Promise.resolve().catch((rollbackErr: unknown) => {"),
 ("G71-M4", "gate", "client.release() dropped (pool connection leak)", "    } finally {\n      client.release();\n    }\n    if (!archived) {", "    } finally {\n    }\n    if (!archived) {"),
 ("G71-M5", "gate", "a vault erase slipped in: DELETE FROM vault_entries before the archive",
  "      await client.query('BEGIN');\n      const updated", "      await client.query('BEGIN');\n      await client.query('DELETE FROM vault_entries WHERE tenant_id = $1', [req.params.id]);\n      const updated"),
 ("G71-M6", "gate", "the failure audit in the outer catch removed",
  "VALUES ('tenant_archive_failed', 'tenant', $1, $2)`,\n      [req.params.id, JSON.stringify({ erased: false })],\n    ).catch(",
  "VALUES ('tenant_archive_failed', 'tenant', $1, $2) LIMIT 0`,\n      [req.params.id, JSON.stringify({ erased: false })],\n    ).catch("),
 ("G71-M7", "gate", "lost race answers 200 archived (silent)", "    if (!archived) {\n      res.status(409)", "    if (false) {\n      res.status(409)"),
 ("G71-M8", "gate", "COMMIT issued even when nothing matched, and archived forced true",
  "      if (updated.rowCount) {", "      if (true) {"),
 ("G71-M9", "gate", "status route: archived -> suspended also lets suspended -> suspended", "  suspended: ['active', 'archived'],", "  suspended: ['active', 'archived', 'suspended'],"),
]

def mutants(only):
    out = []
    try:
        for mid, origin, desc, a, rpl in M:
            if only and mid not in only: continue
            src = open(IDX).read(); h0 = sha(IDX)
            n = src.count(a)
            if n != 1:
                out.append({"id": mid, "error": f"anchor count {n}"}); print(mid, "ANCHOR", n, flush=True); continue
            open(IDX, "w").write(src.replace(a, rpl))
            try:
                pr = run(f"{E}/mut_{mid}_pr.log", [PR_DEL, PR_ST])
                pb = run(f"{E}/mut_{mid}_probe.log", [PROBE], probe=True)
            finally:
                open(IDX, "w").write(src)
            ok = sha(IDX) == h0
            kp, kb = pr["rc"] != 0, pb["rc"] != 0
            out.append({"id": mid, "origin": origin, "desc": desc, "pr": pr, "probe": pb, "killed_by_pr": kp,
                        "killed_by_probe": kb, "verdict": "killed" if (kp or kb) else "SURVIVED", "restored_sha256_ok": ok})
            print(mid, out[-1]["verdict"], "pr_failed", pr["failed"], "probe_failed", pb["failed"], "restored", ok, flush=True)
            if not ok: raise SystemExit("restore failed")
    finally:
        json.dump(out, open(f"{E}/mutants.json", "w"), indent=1)

if __name__ == "__main__":
    if sys.argv[1] == "base": base_run()
    elif sys.argv[1] == "mutants": mutants(set(sys.argv[2:]))
    else: raise SystemExit("usage")
