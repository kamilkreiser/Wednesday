import hashlib, subprocess, sys, re
G = "/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate102-ks1868-pr1920"
S = G + "/repo/Blockchain/Dev/services/analytics"
P = S + "/src/services/scheduledJobs.ts"
NEW = "src/__tests__/ks1868-scheduled-jobs-save-alert-unreadable-throw.test.ts"
orig = open(G + "/logs/head_product.ts").read()
sha = hashlib.sha256(orig.encode()).hexdigest()
guard = """    let reason: string;
    try {
      reason = err instanceof Error ? err.message : String(err);
    } catch {
      reason = 'unreadable thrown value';
    }
    logger.info('DB save alert failed', { error: reason });
  }
}

// =============================================================================
// DATABASE PERSISTENCE LOADING"""
assert orig.count(guard) == 1
base_line = "    logger.info('DB save alert failed', { error: err instanceof Error ? err.message : String(err) });\n  }\n}\n\n// =============================================================================\n// DATABASE PERSISTENCE LOADING"
M = {
 "M0_revert_to_base": base_line,
 "M1_drop_inner_try": guard.replace("    try {\n      reason = err instanceof Error ? err.message : String(err);\n    } catch {\n      reason = 'unreadable thrown value';\n    }\n", "    reason = err instanceof Error ? err.message : String(err);\n"),
 "M2_constant_to_String_err": guard.replace("reason = 'unreadable thrown value';", "reason = String(err);"),
 "M3_rethrow_only_unreadable": guard.replace("reason = 'unreadable thrown value';", "throw err;"),
 "M4_constant_for_all": guard.replace("reason = err instanceof Error ? err.message : String(err);", "reason = 'unreadable thrown value';"),
 "M5_rethrow_every_value_after_log": guard.replace("{ error: reason });\n", "{ error: reason });\n    throw err;\n"),
 "M6_readable_nonError_to_x": guard.replace("err.message : String(err)", "err.message : 'x'"),
 "M7_log_removed": guard.replace("    logger.info('DB save alert failed', { error: reason });\n", ""),
 "M8_constant_text_changed": guard.replace("'unreadable thrown value'", "'unreadable'"),
 "M9_log_the_value_itself": guard.replace("{ error: reason }", "{ error: reason, value: err }"),
}
def run(tag):
    out = G + "/logs/mut_%s.log" % tag
    subprocess.run(["bash", G + "/scripts/vt.sh", out, NEW], capture_output=True)
    t = open(out).read()
    failed = re.findall(r"×\s+(\w+ ks1868 \w+)", t)
    summ = re.findall(r"Tests\s+(.*)", t)
    asserts = t.count("AssertionError")
    return failed, summ[0] if summ else "?", asserts
rows = []
try:
    for name, repl in M.items():
        assert orig.count(guard) == 1
        open(P, "w").write(orig.replace(guard, repl))
        failed, summ, a = run(name)
        open(P, "w").write(orig)
        ok = hashlib.sha256(open(P).read().encode()).hexdigest() == sha
        verdict = "KILLED" if failed else "SURVIVED"
        rows.append("%-34s %-9s cells=%s | %s | assertionErrors=%d | restore %s" % (name, verdict, failed, summ, a, ok))
finally:
    open(P, "w").write(orig)
open(G + "/logs/mutants_table.log", "w").write("\n".join(rows) + "\n")
print("\n".join(rows))
print("final restore", hashlib.sha256(open(P).read().encode()).hexdigest() == sha)
