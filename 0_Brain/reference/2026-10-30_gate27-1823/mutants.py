"""Gate 27 mutants of the KS-1798 catch in routes/gdpr.ts (head worktree only). Restores by content, asserts sha256.
usage: python3 -I mutants.py <originate-dir> <out-dir>"""
import hashlib, json, os, re, subprocess, sys

O, OUT = sys.argv[1], sys.argv[2]
F = f"{O}/src/routes/gdpr.ts"
JEST = f"{O}/../../node_modules/jest/bin/jest.js"
orig = open(F, 'rb').read()
sha0 = hashlib.sha256(orig).hexdigest()
CATCH = "  } catch {\n    ownPgCode = undefined;\n  }\n"
assert orig.decode().count(CATCH) == 1, "catch anchor not unique"
LOOKUP = "  const pgCode = ownPgCode ?? extractPgCode(err);\n"
assert orig.decode().count(LOOKUP) == 1
MUT = {
    "M1 catch rethrows": (CATCH, "  } catch (e) {\n    throw e;\n  }\n"),
    "M2 catch answers 200 success": (CATCH, "  } catch {\n    res.status(200).json({ success: true });\n    return true;\n  }\n"),
    "M3 catch maps to 23503 (404)": (CATCH, "  } catch {\n    ownPgCode = '23503';\n  }\n"),
    "M4 catch returns false (skips extractPgCode)": (CATCH, "  } catch {\n    return false;\n  }\n"),
    "M5 catch maps to 22001 (400)": (CATCH, "  } catch {\n    ownPgCode = '22001';\n  }\n"),
    "M6 drop the extractPgCode fallback": (LOOKUP, "  const pgCode = ownPgCode;\n"),
}
TESTS = {"pr_ks445": "src/__tests__/ks445-gdpr-write-guards.test.ts", "g27_attack": "src/__tests__/g27-attack.test.ts"}
res = {}
try:
    for name, (a, b) in MUT.items():
        open(F, 'wb').write(orig.decode().replace(a, b).encode())
        res[name] = {}
        for tk, t in TESTS.items():
            p = subprocess.run(["node", JEST, "--config", f"{O}/jest.config.js", t], cwd=O, capture_output=True, text=True,
                               env={**os.environ, "TMPDIR": "/tmp/g27"})
            m = re.search(r"Tests:\s+(.*)", p.stderr + p.stdout)
            reds = re.findall(r"✕ (.*?) \(\d+ ms\)", p.stderr + p.stdout)
            res[name][tk] = {"rc": p.returncode, "tests": m.group(1) if m else None, "reds": reds}
            print(name, tk, p.returncode, m.group(1) if m else None, flush=True)
finally:
    open(F, 'wb').write(orig)
    sha1 = hashlib.sha256(open(F, 'rb').read()).hexdigest()
    print("restored sha256", sha1, "equal" if sha1 == sha0 else "MISMATCH")
    res["_restore"] = {"sha256_before": sha0, "sha256_after": sha1}
    json.dump(res, open(f"{OUT}/mutants_result.json", "w"), indent=1)
