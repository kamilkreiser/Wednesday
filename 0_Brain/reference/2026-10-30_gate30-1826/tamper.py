#!/usr/bin/env python3
"""Gate 30 tamper harness. Each mutant: exact-once anchor replace, parse check (TS transpile diagnostics),
vitest json run of the PR's file, restore by byte copy, sha256 assert. Mutant copies live in this dir (outside src)."""
import hashlib, json, os, shutil, subprocess, sys

AUTH = "/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/3595961a-a258-453d-996e-1aad78887d58/scratchpad/gate30/clone/Blockchain/Dev/services/auth"
HERE = os.path.dirname(os.path.abspath(__file__))
GATE = f"{AUTH}/src/services/passwordLoginGate.ts"
REPO = f"{AUTH}/src/repositories/userRepo.ts"
TESTS = os.environ.get("G30_TESTS", "src/__tests__/ks1188-f3-a-spent-backup-code-503-says-so.test.ts").split()
TAG = os.environ.get("G30_TAG", "")
VITEST = f"{AUTH}/../../node_modules/.bin/vitest"

BURN = """          await userRepo.updateUserOrThrow(
            user.id,
            { mfaBackupCodes: user.mfaBackupCodes },
            'Backup-code sign-in',
          );"""
SPLICE = "        user.mfaBackupCodes.splice(backupResult.index, 1);"
MUTANTS = {
    # (a) burn removed entirely: the code stays valid
    "a_no_burn": (GATE, BURN, "          void 0; // G30 tamper a: burn removed"),
    # (b1) wrong code burned: splice the wrong index (nothing removed for a 1-code user; the used code survives)
    "b1_wrong_index": (GATE, SPLICE, "        user.mfaBackupCodes.splice(backupResult.index + 1, 1); // G30 b1"),
    # (b2) no splice at all: the UPDATE writes the array unchanged (the used code survives)
    "b2_no_splice": (GATE, SPLICE, "        // G30 b2: splice removed"),
    # (b3) burn ALL codes (splice(0)): one UPDATE, every other backup code destroyed
    "b3_burn_all": (GATE, SPLICE, "        user.mfaBackupCodes.splice(0); // G30 b3"),
    # (b4) the UPDATE loses its WHERE: every user's row gets this user's codes
    "b4_no_where": (REPO, "      `UPDATE users SET ${setClauses.join(', ')} WHERE id = $${idx}`,",
                    "      `UPDATE users SET ${setClauses.join(', ')}` + (values.pop(), ''), // G30 b4"),
    # (c) the author's: an extra UPDATE users before the real burn
    "c_extra_before": (GATE, BURN, "          await userRepo.updateUserOrThrow(user.id, { mfaBackupCodes: user.mfaBackupCodes }, 'G30 c');\n" + BURN),
    # (c2) the author's shape as a NON-throwing extra UPDATE users before the burn (updateUser, failure swallowed)
    "c2_extra_before_nothrow": (GATE, BURN, "          await userRepo.updateUser(user.id, { mfaBackupCodes: user.mfaBackupCodes }).catch(() => null); // G30 c2\n" + BURN),
    # (e) mine: a retry of the burn inside the catch (double burn ONLY on the faulted path)
    "e_retry_in_catch": (GATE, "        } catch (err) {\n", "        } catch (err) {\n          await userRepo.updateUser(user.id, { mfaBackupCodes: user.mfaBackupCodes }).catch(() => null); // G30 e\n"),
    # (e2) mine: retry the burn in the catch only when the read-back (not the 0-row check) failed
    "e2_retry_on_readback_fault": (GATE, "        } catch (err) {\n", "        } catch (err) {\n          if (!String((err as Error)?.message).includes('could not be confirmed')) await userRepo.updateUser(user.id, { mfaBackupCodes: user.mfaBackupCodes }).catch(() => null); // G30 e2\n"),
    # (d) mine: a double burn AFTER the real burn (a retry loop shape)
    "d_double_after": (GATE, BURN, BURN + "\n          await userRepo.updateUserOrThrow(user.id, { mfaBackupCodes: user.mfaBackupCodes }, 'G30 d');"),
}

def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()

def parse_ok(path):
    js = ("const ts=require('typescript');const s=require('fs').readFileSync(process.argv[1],'utf8');"
          "const r=ts.transpileModule(s,{reportDiagnostics:true,compilerOptions:{module:1,target:99}});"
          "const d=(r.diagnostics||[]).filter(x=>x.category===1);console.log(d.length);process.exit(d.length?1:0)")
    r = subprocess.run(["node", "-e", js, path], cwd=AUTH, capture_output=True, text=True)
    return r.returncode == 0, r.stdout.strip() + r.stderr.strip()[:300]

def run(label):
    out = f"{HERE}/t{TAG}_{label}.json"
    r = subprocess.run([VITEST, "run", *TESTS, "--maxWorkers=3", "--reporter=json", f"--outputFile={out}"], cwd=AUTH, capture_output=True, text=True)
    d = json.load(open(out))
    reds = [f["name"].split("/")[-1][:40] + " :: " + a["title"][:60] for f in d["testResults"] for a in f["assertionResults"] if a["status"] == "failed"]
    return d["numPassedTests"], d["numFailedTests"], d["numTotalTests"], reds, r.returncode

def main(names):
    res = {}
    base = {GATE: sha(GATE), REPO: sha(REPO)}
    p, f, t, reds, rc = run("baseline"); print(f"baseline: {p} pass / {f} fail / {t} total rc={rc}")
    for name in names:
        target, anchor, repl = MUTANTS[name]
        src = open(target).read()
        n = src.count(anchor)
        if n != 1: print(f"{name}: ANCHOR COUNT {n} != 1, skipped"); continue
        mut = src.replace(anchor, repl)
        mpath = f"{HERE}/mutant_{name}.ts"; open(mpath, "w").write(mut)
        ok, diag = parse_ok(mpath)
        if not ok: print(f"{name}: MUTANT DOES NOT PARSE ({diag}), skipped"); continue
        orig = f"{HERE}/orig_{os.path.basename(target)}"; shutil.copyfile(target, orig)
        try:
            shutil.copyfile(mpath, target)
            assert sha(target) != base[target]
            p, f, t, reds, rc = run(name)
        finally:
            shutil.copyfile(orig, target)
        restored = sha(target) == base[target]
        print(f"{name}: {p} pass / {f} fail / {t} total rc={rc} | restored sha256 equal={restored} ({base[target][:16]})")
        for r_ in reds: print("    RED", r_)
        res[name] = dict(passed=p, failed=f, total=t, reds=reds, restored=restored)
    p, f, t, reds, rc = run("final"); print(f"final: {p} pass / {f} fail / {t} total rc={rc}")
    json.dump(res, open(f"{HERE}/tamper_results{TAG}.json", "w"), indent=1)

if __name__ == "__main__":
    main(sys.argv[1:] or list(MUTANTS))
