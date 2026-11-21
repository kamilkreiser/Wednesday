#!/usr/bin/env python3
"""QA-WIN-IPC-R2 mutants of the fix round (crates/coagent-ipc/src/windows.rs and src/sid.rs).
Each mutant gets its OWN git worktree (inside the checker's clone, detached at the head) and its OWN
build folder. Per mutant, in that worktree:
  (1) cargo check  --locked --target x86_64-pc-windows-msvc -p coagent-ipc --all-targets
  (2) cargo clippy --locked --target x86_64-pc-windows-msvc -p coagent-ipc --all-targets -- -D warnings
  (3) cargo test   --locked -p coagent-ipc            (the crate's tests that run on macOS)
The anchor must occur exactly once. Worktrees are left in place (never deleted) for inspection;
the mutated file is never committed.
Usage: python3 -I qa_r2_mutate.py <clone> <head sha> <work dir> [ids...]
Env: the toolchain (cargo on PATH, RUSTUP_HOME/CARGO_HOME set, RUSTUP_TOOLCHAIN=1.100.0)."""
import os, subprocess, sys

CLONE, HEAD, WORK = sys.argv[1], sys.argv[2], sys.argv[3]
ONLY = set(sys.argv[4:])
WIN = "crates/coagent-ipc/src/windows.rs"
SID = "crates/coagent-ipc/src/sid.rs"
MUT = [
    ("R1", "skip the owner check (result discarded)", WIN,
     "                check_peer_sid(&owner_sid, expected_owner_sid)?;\n",
     "                let _ = check_peer_sid(&owner_sid, expected_owner_sid);\n"),
    ("R2", "skip the process check (result discarded)", WIN,
     "                check_peer_sid(&server_sid, expected_process_sid)?;\n",
     "                let _ = check_peer_sid(&server_sid, expected_process_sid);\n"),
    ("R3", "Q15 again: identifier compare as a prefix match (sid.rs, used by the owner check too)", SID,
     "peer.eq_ignore_ascii_case(expected)",
     "expected.to_ascii_uppercase().starts_with(&peer.to_ascii_uppercase())"),
    ("R3b", "owner-only prefix compare written inline in connect_expecting_each", WIN,
     "                check_peer_sid(&owner_sid, expected_owner_sid)?;\n",
     "                if !expected_owner_sid.to_ascii_uppercase().starts_with(&owner_sid.to_ascii_uppercase()) {\n"
     "                    return Err(IpcError::PeerSidRejected.into());\n"
     "                }\n"),
    ("R4", "GetSecurityInfo read as a BOOL: non-zero code = success, zero = failure", WIN,
     "    if rc != ERROR_SUCCESS {\n",
     "    if rc == ERROR_SUCCESS {\n"),
    ("R4b", "GetSecurityInfo code ignored (the error branch can never fire)", WIN,
     "    if rc != ERROR_SUCCESS {\n",
     "    if rc != ERROR_SUCCESS && rc == ERROR_SUCCESS {\n"),
    ("R5", "drop the yield_now after a rejection (m-3)", WIN,
     "            tokio::task::yield_now().await;\n",
     ""),
]


def sh(args, cwd=None):
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def cargo(tree, target, args):
    env = dict(os.environ, CARGO_TARGET_DIR=target)
    # --manifest-path goes right after the subcommand (never after clippy's `--`; the first run of
    # this script put it last, which handed it to clippy-driver: that run's clippy column is void).
    r = subprocess.run(["cargo", args[0], "--manifest-path", os.path.join(tree, "Cargo.toml")] + args[1:],
                       capture_output=True, text=True, env=env)
    return r.returncode, r.stdout + r.stderr


def summarize_test(rc, out):
    if rc == 0:
        tot = sum(int(l.split()[3]) for l in out.splitlines() if l.startswith("test result: ok."))
        return f"green ({tot} passed)"
    if "error[" in out or "could not compile" in out:
        return "NO-COMPILE"
    failed = [l.split()[1] for l in out.splitlines() if l.startswith("test ") and l.endswith("FAILED")]
    return "KILLED(" + ",".join(failed) + ")"


for mid, what, rel, old, new in MUT:
    if ONLY and mid not in ONLY:
        continue
    tree = os.path.join(WORK, "wt", mid)
    target = os.path.join(WORK, "target", "mut_" + mid)
    if not os.path.exists(tree):
        rc, out = sh(["git", "-C", CLONE, "worktree", "add", "--detach", tree, HEAD])
        if rc != 0:
            print(f"{mid}: worktree add failed: {out}")
            continue
    p = os.path.join(tree, rel)
    orig = open(p, encoding="utf-8").read()
    n = orig.count(old)
    if n != 1:
        print(f"{mid:4} {what}: ANCHOR FOUND {n} TIMES", flush=True)
        continue
    open(p, "w", encoding="utf-8").write(orig.replace(old, new, 1))
    rc, d = sh(["git", "-C", tree, "diff", "--stat"])
    log = open(os.path.join(WORK, f"mut_{mid}.log"), "w")
    log.write(f"== {mid} {what}\n{d}\n")
    rc1, o1 = cargo(tree, target, ["check", "--locked", "--target", "x86_64-pc-windows-msvc",
                                   "-p", "coagent-ipc", "--all-targets"])
    rc2, o2 = cargo(tree, target, ["clippy", "--locked", "--target", "x86_64-pc-windows-msvc",
                                   "-p", "coagent-ipc", "--all-targets", "--", "-D", "warnings"])
    rc3, o3 = cargo(tree, target, ["test", "--locked", "-p", "coagent-ipc"])
    log.write(f"--- win check rc={rc1}\n{o1}\n--- win clippy rc={rc2}\n{o2}\n--- mac test rc={rc3}\n{o3}\n")
    log.close()
    warn1 = sum(1 for l in o1.splitlines() if l.startswith("warning:") and "rand_core" not in l
                and "generated" not in l)
    print(f"{mid:4} {what}\n     win check rc={rc1} (warnings other than rand_core: {warn1}) | "
          f"win clippy -D warnings rc={rc2} | mac tests: {summarize_test(rc3, o3)}", flush=True)
