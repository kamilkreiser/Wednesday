#!/usr/bin/env python3
"""Gate r6 mutation driver. usage: python3 -I mutate_r6.py <pristine tree> <scratch tree> <out dir> [ids...]
Each mutant: copy the pristine file, apply ONE text replacement (must match exactly once), run the listed test
targets, record pass/fail per test, restore the file from the pristine tree, and verify the restore with a byte compare.
Toolchain env comes from the caller (env.sh)."""
import os, re, shutil, subprocess, sys, filecmp, signal

A = "crates/coagent-policy/src/action.rs"
E = "crates/coagent-policy/src/engine.rs"

MONITOR_ARM_OLD = '''        #[cfg(not(feature = "red_monitor_unknown"))]
        "Monitor" => {'''

MUTANTS = {
    # Monitor arm deleted outright (Monitor then reaches the catch-all, which sees its `command` field)
    "MA": (A, MONITOR_ARM_OLD, '''        #[cfg(any())]
        "Monitor" => {'''),
    # Monitor arm returns the unknown kind (as before addendum 7), catch-all untouched
    "MA2": (A, MONITOR_ARM_OLD + '''
            let (kind, mut t) = shell_execute(''', '''        #[cfg(not(feature = "red_monitor_unknown"))]
        "Monitor" => {
            #[allow(unreachable_code)]
            return_other_kind_marker();
            let (kind, mut t) = shell_execute('''),
    # Monitor scanned with PowerShell rules instead of Bash
    "MF": (A, '''            let (kind, mut t) = shell_execute(
                str_field(ti, "command"),
                ShellKind::Bash,''', '''            let (kind, mut t) = shell_execute(
                str_field(ti, "command"),
                ShellKind::PowerShell,'''),
    # Monitor ws URL target dropped
    "ME": (A, '''                t.push(Target::Url {
                    url: url.to_string(),
                    host: url_host(url),
                });''', '''                let _ = url;'''),
    # command-field rule off everywhere
    "MB": (A, "    COMMAND_FIELDS.iter().find_map(|k| str_field(ti, k))", "    { let _ = ti; None }"),
    # unknown_shell: Bash scan only (PowerShell scan dropped)
    "MB2": (A, "    targets.extend(ps.into_iter().filter(|t| {", "    targets.extend(ps.into_iter().take(0).filter(|t| {"),
    # command-field rule off for mcp__ only
    "MB3": (A, '''            match command_field(ti) {
                // addendum 7 item 4''', '''            match None::<&str> {
                // addendum 7 item 4'''),
    # command-field rule off for the catch-all only
    "MB4": (A, "        _ => match command_field(ti) {", "        _ => match None::<&str> {"),
    # owner list: tool not bound (any tool name with a matching shell)
    "MC": (E, '''        (ShellKind::Bash, "Bash") | (ShellKind::PowerShell, "PowerShell")
    );''', '''        (ShellKind::Bash, _) | (ShellKind::PowerShell, _)
    );'''),
    # owner list: sandbox-off exclusion removed
    "MD": (E, '''    if action.sandbox_disabled {
        return None;
    }''', '''    if action.sandbox_disabled && false {
        return None;
    }'''),
    # a real slowdown: 60 ms of extra work in decide for any action with a command over 1 000 bytes
    "MG": (E, '''    let surface = effective_surface(surface, action);
    // [1] a decision belongs to one session''', '''    let surface = effective_surface(surface, action);
    if action.targets.iter().any(|t| matches!(t, Target::Command { text, .. } if text.len() > 1000)) {
        std::thread::sleep(std::time::Duration::from_millis(60));
    }
    // [1] a decision belongs to one session'''),
}
# MA2 needs a helper that makes the arm return the Other kind; simpler: replace the whole arm head with an early value
MUTANTS["MA2"] = (A, MONITOR_ARM_OLD + '''
            let (kind, mut t) = shell_execute(''', '''        #[cfg(not(feature = "red_monitor_unknown"))]
        "Monitor" => {
            #[allow(unreachable_code)]
            if true { (Kind::Other, vec![raw_target.clone()]) } else {
            let (kind, mut t) = shell_execute(''')

TESTS = {
    "default": ["t18_addendum7", "r5b_shell_t3::g5_monitor", "r5b_shell_t3::g5_owner", "r6_gate::g6_", "t17_addendum5"],
    "MG": ["q01_gate_attacks::z_timing", "t17_addendum5::m1_blow_up"],
}

def run(cmd, log):
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    with open(log, "a") as f:
        f.write("$ " + " ".join(cmd) + "\n" + p.stdout + f"\nrc={p.returncode}\n")
    return p.returncode, p.stdout

def main():
    pristine, tree, out = sys.argv[1:4]
    ids = sys.argv[4:] or list(MUTANTS)
    os.makedirs(out, exist_ok=True)
    tsv = open(os.path.join(out, "mutation_results.tsv"), "a")
    for mid in ids:
        rel, old, new = MUTANTS[mid]
        src = os.path.join(pristine, rel); dst = os.path.join(tree, rel)
        text = open(src).read()
        n = text.count(old)
        if n != 1:
            tsv.write(f"{mid}\tNOT APPLIED (matches={n})\n"); tsv.flush(); continue
        if mid == "MA2":
            # close the extra `else {` opened by the replacement: the arm ends with `(kind, t)\n        }`
            mutated = text.replace(old, new)
            mutated = mutated.replace("            (kind, t)\n        }\n        // RED CONTROL ONLY: `Monitor` back",
                                      "            (kind, t)\n        }}\n        // RED CONTROL ONLY: `Monitor` back", 1)
        else:
            mutated = text.replace(old, new)
        log = os.path.join(out, f"mut_{mid}.log")
        open(log, "w").close()
        def restore(*_):
            shutil.copyfile(src, dst)
            sys.exit(1)
        signal.signal(signal.SIGTERM, restore)
        try:
            open(dst, "w").write(mutated)
            red, green, other = [], [], []
            for t in TESTS.get(mid, TESTS["default"]):
                target, _, filt = t.partition("::")
                cmd = ["cargo", "test", "--manifest-path", os.path.join(tree, "Cargo.toml"), "-p", "coagent-policy",
                       "--offline", "--test", target, "--", "--test-threads", "2"] + ([filt] if filt else [])
                rc, o = run(cmd, log)
                f = re.findall(r"^test (\S+) \.\.\. FAILED", o, re.M)
                ok = re.findall(r"^test (\S+) \.\.\. ok", o, re.M)
                if "could not compile" in o or "error[" in o:
                    other.append(f"{target}:COMPILE_ERROR")
                red += [f"{target}::{x}" for x in f]
                green += [f"{target}::{x}" for x in ok]
            verdict = "KILLED" if red else ("COMPILE_ERROR" if other else "SURVIVED")
            tsv.write(f"{mid}\t{verdict}\tred={','.join(red)}\t{';'.join(other)}\tgreen_count={len(green)}\n"); tsv.flush()
            print(mid, verdict, red, other, flush=True)
        finally:
            shutil.copyfile(src, dst)
            assert filecmp.cmp(src, dst, shallow=False), f"restore failed for {rel}"
    tsv.close()

if __name__ == "__main__":
    main()
