# QA-POLICY-B item 7: build and run the builder's tests against one mutant tree (own target dir), each run with a
# timeout. usage: python3 -B mut_run.py <tree> <out.txt>
import os, subprocess, sys, time, re
W = "/private/tmp/claude-501/qpb"; T = sys.argv[1]; OUT = sys.argv[2]
env = dict(os.environ, RUSTUP_HOME=f"{W}/tools/rustup", CARGO_HOME=f"{W}/tools/cargo",
           PATH=f"{W}/tools/cargo/bin:" + os.environ["PATH"], CARGO_TARGET_DIR=f"{W}/tt_{T}/debug",
           COAGENT_TEST_TMP=f"{W}/tt_{T}/testtmp", RED_CONTROLS_LOG=f"{W}/tt_{T}/red-normal.log")
os.makedirs(env["COAGENT_TEST_TMP"], exist_ok=True)
heavy = subprocess.run(["bash", "/Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/heavy_runs.sh"], capture_output=True, text=True).stdout.strip()
base = ["cargo", "test", "-p", "coagent-policy", "--locked", "--offline"]
with open(OUT, "w") as f:
    f.write(f"tree {T} head {subprocess.run(['git','-C',f'{W}/{T}','rev-parse','HEAD'],capture_output=True,text=True).stdout.strip()} heavy {heavy} start {time.strftime('%T')} CARGO_TARGET_DIR={env['CARGO_TARGET_DIR']} COAGENT_TEST_TMP={env['COAGENT_TEST_TMP']}\n")
    f.write(subprocess.run(["git", "-C", f"{W}/{T}", "diff"], capture_output=True, text=True).stdout)
    for name, sel in [("unit free_text_scan_b", ["--lib", "--", "free_text_scan_b"]), ("t29_free_text", ["--test", "t29_free_text"]),
                      ("t28_at_names", ["--test", "t28_at_names"])]:
        t0 = time.time()
        try:
            p = subprocess.run(base + sel, cwd=f"{W}/{T}", env=env, capture_output=True, text=True, timeout=900)
            out = p.stdout + p.stderr; rc = p.returncode
        except subprocess.TimeoutExpired as e:
            out = (e.stdout or b"").decode() if isinstance(e.stdout, bytes) else (e.stdout or ""); rc = "TIMEOUT(900s)"
        compiled = "Compiling coagent-policy" in out
        res = [l for l in out.splitlines() if l.startswith("test result")]
        panics = []
        lines = out.splitlines()
        for i, l in enumerate(lines):
            if "panicked at" in l:
                panics.append(l.strip()[:200] + " | " + (lines[i + 1].strip()[:260] if i + 1 < len(lines) else ""))
        failed = [l for l in lines if l.startswith("test ") and l.endswith("FAILED")]
        f.write(f"== {name}: rc {rc} compiled-in-this-run {compiled} {time.time() - t0:.0f}s {res}\n   failed: {failed}\n")
        for pn in panics[:4]:
            f.write(f"   PANIC {pn}\n")
        if "error[" in out:
            f.write("   COMPILE ERROR: " + " | ".join(l for l in lines if "error" in l)[:600] + "\n")
        f.flush()
print("done", T)
