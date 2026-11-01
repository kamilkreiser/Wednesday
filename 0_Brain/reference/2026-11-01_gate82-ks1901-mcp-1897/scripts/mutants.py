#!/usr/bin/env python3
"""Mutate product files in wt_head in place, run the 5 PR test files, restore by sha256. Log per mutant to logs/mut_<id>.log."""
import hashlib, subprocess, sys, re
W = "/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate82-ks1901-mcp-1897"
M = W + "/wt_head/Blockchain/Dev/services/mcp-server/src"
HTTP, HASH = M + "/http-server.ts", M + "/tools/hash.ts"
TESTS = ["src/__tests__/" + t for t in [
 "ks1901-mcp-http-batch-items-never-echo-the-thrown-text.test.ts", "ks1893-hash-tool-never-returns-the-fs-error-text.test.ts",
 "ks1410-mcp-http-500-part-a-never-echoes-the-thrown-text.test.ts", "ks1410-mcp-http-500-part-b-never-echoes-the-thrown-text.test.ts",
 "ks1868-hash-tool-unreadable-throw.test.ts"]]
ERR = "error: 'An unexpected error occurred' });"
REG_CATCH = "console.error('[mcp-http] POST /register-batch item failed:', describeThrown(err));\n        results.push({ success: false, title: doc.title, error: 'An unexpected error occurred' });"
VER_CATCH = "console.error('[mcp-http] POST /verify-batch item failed:', describeThrown(err));\n        results.push({ verified: false, error: 'An unexpected error occurred' });"
MUT = [
 ("M1_describeThrown_object_String(err)", HTTP, "return `non-Error object thrown (fields: ${Object.keys(err).join(', ') || 'none'})`;", "return String(err);"),
 ("M2_describeThrown_object_values", HTTP, "Object.keys(err).join(', ')", "Object.values(err).join(', ')"),
 ("M3_describeThrown_string_branch_dropped_to_kind", HTTP, "if (typeof err === 'string') return err;", "if (typeof err === 'string') return 'non-Error string thrown';"),
 ("M4_describeThrown_try_removed(rethrow)", HTTP, "  } catch {\n    return 'unreadable thrown value';\n  }", "  } catch (e) {\n    throw e;\n  }"),
 ("M5_describeThrown_unreadable_text_changed", HTTP, "return 'unreadable thrown value';", "return 'x';"),
 ("M6_register_item_catch_rethrows", HTTP, REG_CATCH, REG_CATCH + "\n        throw err;"),
 ("M7_verify_item_catch_rethrows", HTTP, VER_CATCH, VER_CATCH + "\n        throw err;"),
 ("M8_register_constant_replaced_by_err.message", HTTP, REG_CATCH, REG_CATCH.replace("error: 'An unexpected error occurred'", "error: (err as Error).message")),
 ("M9_verify_constant_replaced_by_String(err)", HTTP, VER_CATCH, VER_CATCH.replace("error: 'An unexpected error occurred'", "error: String(err)")),
 ("M10_register_log_removed", HTTP, "console.error('[mcp-http] POST /register-batch item failed:', describeThrown(err));", ""),
 ("M11_verify_log_console.log", HTTP, "console.error('[mcp-http] POST /verify-batch item failed:', describeThrown(err));", "console.log('[mcp-http] POST /verify-batch item failed:', describeThrown(err));"),
 ("M12_register_log_raw_err", HTTP, "console.error('[mcp-http] POST /register-batch item failed:', describeThrown(err));", "console.error('[mcp-http] POST /register-batch item failed:', err);"),
 ("M13_hash_console.error_to_log", HASH, "console.error('[mcp-server] secuura_hash_document failed:', logged);", "console.log('[mcp-server] secuura_hash_document failed:', logged);"),
 ("M14_hash_constant_replaced_by_logged", HASH, "JSON.stringify({ success: false, error })", "JSON.stringify({ success: false, error: logged })"),
 ("M15_hash_object_branch_String(err)", HASH, "logged = `non-Error object thrown (fields: ${Object.keys(err).join(', ') || 'none'})`;", "logged = String(err);"),
 ("M16_hash_unreadable_keeps_constant_dropped", HASH, "          error = 'unreadable thrown value';\n", ""),
 ("M17_hash_inner_try_removed(rethrow)", HASH, "        } catch {\n          logged = 'unreadable thrown value';", "        } catch (e) {\n          throw e;\n          logged = 'unreadable thrown value';"),
 ("M18_hash_string_branch_dropped_to_kind", HASH, "else if (typeof err === 'string') logged = err;", "else if (typeof err === 'string') logged = 'non-Error string thrown';"),
 ("M19_hash_catch_returns_err.message", HASH, "let error = 'An unexpected error occurred';", "let error = (err as Error)?.message ?? 'An unexpected error occurred';"),
 ("M20_hash_isError_dropped", HASH, "          isError: true,\n        };\n      }\n    },", "        };\n      }\n    },"),
]
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
orig = {p: open(p).read() for p in (HTTP, HASH)}
osha = {p: sha(p) for p in orig}
only = sys.argv[1:]
out = []
for mid, path, a, b in MUT:
    if only and not any(mid.startswith(o) for o in only): continue
    n = orig[path].count(a)
    if n != 1:
        out.append(f"{mid} | PATTERN COUNT {n} (not applied)"); continue
    open(path, "w").write(orig[path].replace(a, b))
    log = f"{W}/logs/mut_{re.sub(r'[^A-Za-z0-9_.]', '_', mid)}.log"
    r = subprocess.run(["bash", W + "/scripts/vt.sh", "head", log] + TESTS, capture_output=True, text=True)
    txt = open(log).read()
    m = re.search(r"Tests\s+(.*)", txt)
    failed = sorted(set(re.findall(r"(?:FAIL|×)\s+src/__tests__/(\S+)", txt)))
    open(path, "w").write(orig[path])
    ok = sha(path) == osha[path]
    verdict = "KILLED" if r.returncode != 0 and "failed" in (m.group(1) if m else "") else ("SURVIVED" if r.returncode == 0 else "ERROR-NOT-ASSERTION")
    out.append(f"{mid} | {verdict} | {m.group(1) if m else '?'} | restored_sha_equal={ok}")
    print(out[-1], flush=True)
print("\n".join(out))
