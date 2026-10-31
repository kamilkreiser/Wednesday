#!/usr/bin/env python3
"""Gate 64 harness: base-product runs and own mutants for KS-1860 #1876.
usage: mutants.py base | mutants [Mx ...] | control
 base     : swap tenant-pool-manager.ts and tenant-provisioning index.ts to the merge-base blobs (c63d3dc6), run the PR
            files + the gate probe, restore, assert sha256.
 mutants  : one unique-anchor replacement each (anchor must occur exactly once), run the relevant test files, restore,
            assert sha256. Writes evidence/own_mutants.json.
Every run: nice -n 10, --maxWorkers=2, TMPDIR = gate tmp/. Waits while load1 > 16."""
import subprocess, os, sys, json, hashlib, shutil, time, re
G = "/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate64-ks1860-1876"
R = f"{G}/repo"; D = f"{R}/Blockchain/Dev"; E = f"{G}/evidence"
VITEST = f"{D}/node_modules/.bin/vitest"
SH = f"{D}/packages/shared"; TP = f"{D}/services/tenant-provisioning"
PM = f"{SH}/src/db/tenant-pool-manager.ts"; TC = f"{SH}/src/db/tenant-context.ts"; IDX = f"{TP}/src/index.ts"
PR_SH = "src/__tests__/ks1860-suspended-or-archived-tenant-is-refused.test.ts"
PR_TP = "src/__tests__/ks1860-tenant-status-follows-the-documented-order.test.ts"
PROBE_SRC = f"{G}/scripts/gate64-probe.test.ts"; PROBE = "src/__tests__/gate64-probe.test.ts"
TPPROBE_SRC = f"{G}/scripts/gate64-tp-probe.test.ts"; TPPROBE = "src/__tests__/gate64-tp-probe.test.ts"
BASE = "c63d3dc6c83931a96d52e0c261b44b3b6e1bc318"
ENV = dict(os.environ, TMPDIR=f"{G}/tmp", NODE_ENV="test")

def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def load1():
    o = subprocess.run(["sysctl", "-n", "vm.loadavg"], capture_output=True, text=True).stdout
    return float(o.strip("{} \n").split()[0])
def wait_load():
    while load1() > 16: time.sleep(20)
def place_probes():
    shutil.copy(PROBE_SRC, f"{SH}/{PROBE}")
    if os.path.exists(TPPROBE_SRC): shutil.copy(TPPROBE_SRC, f"{TP}/{TPPROBE}")
def park_probes():
    for p in (f"{SH}/{PROBE}", f"{TP}/{TPPROBE}"):
        if os.path.exists(p): os.remove(p)   # inside the gate clone; originals live in scripts/
def vit(root, files, log, extra_env=None):
    wait_load()
    env = dict(ENV, **(extra_env or {}))
    p = subprocess.run(["nice", "-n", "10", VITEST, "run", "--root", root, *files, "--maxWorkers=2"],
                       capture_output=True, text=True, env=env, timeout=900)
    out = p.stdout + p.stderr
    open(log, "w").write(out)
    m = re.search(r"Tests\s+(?:(\d+) failed \| )?(?:(\d+) passed)?(?: \| (\d+) skipped)?", out)
    failed = int(m.group(1) or 0) if m else -1; passed = int(m.group(2) or 0) if m else -1
    reds = sorted(set(re.findall(r"(?:FAIL|×)\s+[^\n]*?((?:RED|CONTROL) KS-1860 [A-Z]\d+|gate64[^\n]*?[A-Z]\d+[^:\n]*)", out)))
    return {"rc": p.returncode, "passed": passed, "failed": failed, "reds": reds, "log": os.path.relpath(log, G)}

def base_run():
    place_probes()
    orig = {p: sha(p) for p in (PM, IDX)}; saved = {p: open(p, "rb").read() for p in orig}
    res = {}
    try:
        res["head_shared"] = vit(SH, [PR_SH, PROBE], f"{E}/head_shared_pr_probe.log", {"GATE64_SNAPSHOT": f"{E}/getpool_snapshot_head.json"})
        res["head_tp"] = vit(TP, [PR_TP] + ([TPPROBE] if os.path.exists(TPPROBE_SRC) else []), f"{E}/head_tp_pr_probe.log")
        for p in orig:
            rel = os.path.relpath(p, R)
            blob = subprocess.run(["git", "-C", R, "show", f"{BASE}:{rel}"], capture_output=True, check=True).stdout
            open(p, "wb").write(blob)
        res["base_shared"] = vit(SH, [PR_SH, PROBE], f"{E}/base_product_shared.log", {"GATE64_SNAPSHOT": f"{E}/getpool_snapshot_base.json"})
        res["base_tp"] = vit(TP, [PR_TP] + ([TPPROBE] if os.path.exists(TPPROBE_SRC) else []), f"{E}/base_product_tp.log")
    finally:
        for p, b in saved.items(): open(p, "wb").write(b)
        park_probes()
    res["restored_sha256_ok"] = all(sha(p) == orig[p] for p in orig)
    json.dump(res, open(f"{E}/base_runs.json", "w"), indent=1); print(json.dumps(res, indent=1))

# (id, description, file, anchor, replacement, suite) ; suite: "sh" or "tp"
M = [
 ("G64-M1", "status map not consulted: getTenantStatus reads the pool-config map again", PM,
  "    return this.tenantStatuses.get(tenantId);", "    return this.tenantConfigs.get(tenantId)?.status;", "sh"),
 ("G64-M2", "archived dropped from the refused set in extractTenantContext", TC,
  "if (status === 'suspended' || status === 'archived') {", "if (status === 'suspended') {", "sh"),
 ("G64-M3", "status recorded only after the active/provisioning filter", PM,
  "        this.tenantStatuses.set(row.tenant_id, row.status);\n        if (row.status !== 'active' && row.status !== 'provisioning') continue;",
  "        if (row.status !== 'active' && row.status !== 'provisioning') continue;\n        this.tenantStatuses.set(row.tenant_id, row.status);", "sh"),
 ("G64-M4", "rows into the pool map (SM4: the continue removed)", PM,
  "        if (row.status !== 'active' && row.status !== 'provisioning') continue;\n", "", "sh"),
 ("G64-M5", "rows into the pool map AS ACTIVE (SM4 variant: getPool would hand a suspended tenant its own DB)", PM,
  "        if (row.status !== 'active' && row.status !== 'provisioning') continue;\n",
  "        const _s = row.status; if (_s !== 'active' && _s !== 'provisioning') row.status = 'active';\n", "sh"),
 ("G64-M6", "refresh failure clears the status map (fail-open on every DB blip)", PM,
  "      console.error('[TenantPoolManager] Failed to load tenant configs:', err.message);",
  "      this.tenantStatuses.clear();\n      console.error('[TenantPoolManager] Failed to load tenant configs:', err.message);", "sh"),
 ("G64-M7", "refresh failure treats every known tenant as active", PM,
  "      console.error('[TenantPoolManager] Failed to load tenant configs:', err.message);",
  "      for (const k of this.tenantStatuses.keys()) this.tenantStatuses.set(k, 'active');\n      console.error('[TenantPoolManager] Failed to load tenant configs:', err.message);", "sh"),
 ("G64-M8", "status map never cleared on refresh (removed tenants linger)", PM,
  "      this.tenantStatuses.clear();\n      for (const row", "      for (const row", "sh"),
 ("G64-M9", "refresh interval 10x longer (600 s)", PM,
  "const DEFAULT_REFRESH_INTERVAL = 60_000;", "const DEFAULT_REFRESH_INTERVAL = 600_000;", "sh"),
 ("G64-M10", "isEnabled() guard dropped (refuses with multi-tenancy off)", TC,
  "if (manager.isEnabled() && tenantId !== DEFAULT_TENANT_ID) {", "if (tenantId !== DEFAULT_TENANT_ID) {", "sh"),
 ("G64-M11", "disallowed transition admitted: active -> archived", IDX,
  "  archived: ['suspended'],\n};", "  archived: ['suspended', 'active'],\n};", "tp"),
 ("G64-M12", "disallowed transition admitted: archived -> active", IDX,
  "  active: ['provisioning', 'suspended'],", "  active: ['provisioning', 'suspended', 'archived'],", "tp"),
 ("G64-M13", "same-status admitted: suspended -> suspended", IDX,
  "  suspended: ['active'],", "  suspended: ['active', 'suspended'],", "tp"),
 ("G64-M14", "allowed transition refused: suspended -> active (no reactivation)", IDX,
  "  active: ['provisioning', 'suspended'],", "  active: ['provisioning'],", "tp"),
 ("G64-M15", "conditional WHERE dropped (unconditional UPDATE)", IDX,
  "`UPDATE tenants SET status = $1, updated_at = now() WHERE id = $2 AND status = ANY($3::text[])`,\n      [status, req.params.id, STATUS_REACHABLE_FROM[status]],",
  "`UPDATE tenants SET status = $1, updated_at = now() WHERE id = $2`,\n      [status, req.params.id],", "tp"),
 ("G64-M16", "audit row written on refusal (before the rowCount check)", IDX,
  "    if (!updated.rowCount) {\n      const current",
  "    await platformQuery(`INSERT INTO platform_audit_log (action, target_type, target_id, details) VALUES ('tenant_status_changed', 'tenant', $1, $2)`, [req.params.id, JSON.stringify({ status })]);\n    if (!updated.rowCount) {\n      const current", "tp"),
 ("G64-M17", "404 and 409 swapped", IDX,
  "      if (current.rowCount === 0) {", "      if (current.rowCount !== 0) {", "tp"),
 ("G64-M18", "unknown id answers 409 (follow-up SELECT ignored)", IDX,
  "      if (current.rowCount === 0) {", "      if (false) {", "tp"),
 ("G64-M19", "409 message names the requested status twice (current status not read back)", IDX,
  "Cannot change tenant status from ${current.rows[0].status} to ${status}", "Cannot change tenant status from ${status} to ${status}", "tp"),
 ("G64-M20", "refusal answers 200 with no change (silent no-op)", IDX,
  "      res.status(409).json({\n        success: false,", "      res.status(200).json({\n        success: true,", "tp"),
 ("G64-M21", "allowed lists passed in the wrong param slot (from-list = target)", IDX,
  "[status, req.params.id, STATUS_REACHABLE_FROM[status]],", "[status, req.params.id, [status]],", "tp"),
]

def mutants(only):
    place_probes()
    out = []
    try:
        ctl_sh = vit(SH, [PR_SH, PROBE], f"{E}/mut_control_sh.log", {"GATE64_EXPECT": f"{E}/getpool_snapshot_base.json"}); ctl_tp = vit(TP, [PR_TP] + ([TPPROBE] if os.path.exists(TPPROBE_SRC) else []), f"{E}/mut_control_tp.log")
        out.append({"id": "CONTROL", "sh": ctl_sh, "tp": ctl_tp})
        for mid, desc, f, a, rpl, suite in M:
            if only and mid not in only: continue
            src = open(f).read(); h0 = sha(f)
            n = src.count(a)
            if n != 1: out.append({"id": mid, "desc": desc, "error": f"anchor count {n}"}); continue
            open(f, "w").write(src.replace(a, rpl))
            try:
                if suite == "sh":
                    pr = vit(SH, [PR_SH], f"{E}/mut_{mid}_pr.log"); pb = vit(SH, [PROBE], f"{E}/mut_{mid}_probe.log", {"GATE64_EXPECT": f"{E}/getpool_snapshot_base.json"})
                else:
                    pr = vit(TP, [PR_TP], f"{E}/mut_{mid}_pr.log")
                    pb = vit(TP, [TPPROBE], f"{E}/mut_{mid}_probe.log") if os.path.exists(TPPROBE_SRC) else None
            finally:
                open(f, "w").write(src)
            ok = sha(f) == h0
            killed_pr = pr["rc"] != 0; killed_pb = bool(pb and pb["rc"] != 0)
            out.append({"id": mid, "desc": desc, "file": os.path.relpath(f, D), "pr_tests": pr, "probe": pb,
                        "killed_by_pr_tests": killed_pr, "killed_by_gate_probe": killed_pb,
                        "verdict": "killed" if (killed_pr or killed_pb) else "SURVIVED", "restored_sha256_ok": ok})
            print(mid, out[-1]["verdict"], "pr", pr["failed"], "probe", pb and pb["failed"], "restored", ok, flush=True)
            if not ok: raise SystemExit(f"restore failed for {f}")
    finally:
        park_probes()
        json.dump(out, open(f"{E}/own_mutants.json", "w"), indent=1)

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "base": base_run()
    elif mode == "mutants": mutants(set(sys.argv[2:]))
    else: raise SystemExit("usage")
