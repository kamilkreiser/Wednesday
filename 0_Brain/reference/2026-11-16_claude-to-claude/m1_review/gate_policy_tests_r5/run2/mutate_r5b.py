#!/usr/bin/env python3
"""Mutation driver, gate r5 run 2. Applies ONE textual mutant at a time to the scratch tree <mut> (an archive of
0ea9b95 plus my r5b_* test files), runs the coagent-policy suite, records which tests fail, restores the file
(verified byte-identical by sha256 before the next mutant).

usage: python3 -I mutate_r5b.py <mut-tree> <out.tsv> [mutant-id ...]
Environment: the toolchain from env_r5.sh (cargo on PATH, CARGO_TARGET_DIR, COAGENT_TEST_TMP).
The 60 000-line shell-identity test (r4 p_identity_60k) is skipped: it runs shells, takes many minutes, and
asserts nothing a mutant below can change except "every line is T3", which other tests cover.
"""
import hashlib, os, re, subprocess, sys, time

E = "crates/coagent-policy/src/engine.rs"
A = "crates/coagent-policy/src/action.rs"
SH = "crates/coagent-policy/src/shell/mod.rs"

MUTANTS = [
    # id, file, old, new, what it breaks
    ("E1", E, "                #[cfg(not(feature = \"red_shell_not_t3\"))]\n                a.raise(Tier::T3, Some(Reason::ShellExpansion));",
     "                #[cfg(not(feature = \"red_shell_not_t3\"))]\n                a.raise(Tier::T0, Some(Reason::ShellExpansion));",
     "shell command no longer raised to T3 (falls to T2 by kind)"),
    ("E2", E, "    if a.tier == Tier::T3 {\n        return ask(action, state, &a, surface, now, vec![]);",
     "    if a.tier == Tier::T3 && false {\n        return ask(action, state, &a, surface, now, vec![]);",
     "[8] T3 no longer asks before approvals / memory / grant"),
    ("E3", E, "        batchable: !t3,", "        batchable: true,", "T3 card batchable"),
    ("E4", E, "        read_delay_secs: if t3 { 5 } else { 0 },", "        read_delay_secs: 0,", "no read delay on T3"),
    ("E5", E, "    if a.tier == Tier::T3 || a.may_read_excluded {\n        return None;",
     "    if a.may_read_excluded {\n        return None;", "session_scope: T3 guard removed (Execute arm still None)"),
    ("E6", E, "        Kind::Execute => None,",
     "        Kind::Execute => Some(Scope::ExactInput {\n            hash: action.raw_input_hash.clone(),\n        }),",
     "session_scope: shell gets an ExactInput scope (T3 guard still there)"),
    ("E56", E, "    if a.tier == Tier::T3 || a.may_read_excluded {\n        return None;",
     "    if a.may_read_excluded {\n        return None;", "E5 and E6 together (applied as two edits)"),
    ("E7", E, "        Scope::ExactCommand { .. } => false,",
     "        Scope::ExactCommand { text, .. } => action.targets.iter().any(|t| matches!(t, Target::Command { text: x, .. } if x == text)),",
     "a stored ExactCommand approval allows again (old behaviour)"),
    ("E8", E, "        Kind::Execute => Err(Some(\"a grant never covers a shell command\".into())),",
     "        Kind::Execute => ok(\"execute\".into(), vec![]),", "a grant covers every shell command"),
    ("O1", E, "        a == b\n", "        a.trim() == b.trim()\n", "owner list: whitespace-trimmed match"),
    ("O2", E, "        a == b\n", "        a.starts_with(b)\n", "owner list: prefix match"),
    ("O3", E, "            let same_cwd =\n                action.cwd.canonical() == Some(oc.cwd.as_path()) && cwd_is_physical(&action.cwd);",
     "            let same_cwd = action.cwd.canonical() == Some(oc.cwd.as_path());", "owner list: symlinked cwd accepted"),
    ("O4", E, "            tool_ok && oc.shell == shell && same_cwd", "            same_cwd", "owner list: tool/shell not compared"),
    ("O5", E, "            let same_cwd =\n                action.cwd.canonical() == Some(oc.cwd.as_path()) && cwd_is_physical(&action.cwd);",
     "            let same_cwd = action.cwd.canonical().is_some_and(|c| c.starts_with(&oc.cwd)) && cwd_is_physical(&action.cwd);",
     "owner list: any sub-directory of the entry's cwd"),
    ("O6", E, "    if let Some(why) = owner_list_allows(action, state) {\n        return Decision::Allow { why };\n    }\n    // [8]",
     "    // [8]", "owner list removed entirely (positive controls must go red)"),
    ("A1", A, "        \"Bash\" => classify_bash(", "        \"BashX\" => classify_bash(", "Bash no longer classified as a shell (unknown tool, T2)"),
    ("A2", A, "        \"PowerShell\" => classify_powershell(", "        \"PowerShellX\" => classify_powershell(",
     "PowerShell no longer classified as a shell"),
    ("A3", A, "    if text.len() > MAX_EXEC_BYTES {", "    if text.len() > MAX_EXEC_BYTES * 4 {", "64 KiB bound raised 4x"),
    ("S1", SH, ".map(|c| if c == '\\\\' { '/' } else { c })", ".map(|c| c)", "PowerShell '\\' not read as a separator"),
    ("S2", E, "    if has(crate::patterns::RUNS_GIVEN_CODE.words) {", "    if false {", "RunsGivenCode reason line never added"),
    ("S3", E, "first_hit(&state.hard_deny, &sp, mode).or_else(|| by_name(&state.hard_deny))",
     "first_hit(&state.hard_deny, &sp, mode)", "hard deny by-name match removed"),
]
SECOND = {"E56": ("        Kind::Execute => None,",
                  "        Kind::Execute => Some(Scope::ExactInput {\n            hash: action.raw_input_hash.clone(),\n        }),")}


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def run(tree):
    cmd = ["cargo", "test", "--manifest-path", os.path.join(tree, "Cargo.toml"), "-p", "coagent-policy",
           "--offline", "--no-fail-fast", "--", "--skip", "p_identity_60k", "--skip", "g5_central"]
    t = time.time()
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    out = p.stdout
    failed, binary = [], "?"
    for line in out.splitlines():
        m = re.search(r"Running (?:unittests )?(\S+)", line)
        if m:
            binary = os.path.basename(m.group(1)).replace(".rs", "")
        m = re.match(r"test (\S+) \.\.\. FAILED", line)
        if m:
            failed.append(f"{binary}::{m.group(1)}")
    compile_err = "error[E" in out or "could not compile" in out
    return p.returncode, failed, compile_err, time.time() - t, out


def main():
    import signal
    signal.signal(signal.SIGTERM, lambda *a: (_ for _ in ()).throw(KeyboardInterrupt()))  # run finally on TERM
    tree, out_tsv = sys.argv[1], sys.argv[2]
    only = set(sys.argv[3:])
    with open(out_tsv, "a") as f:
        # baseline: the unmutated tree; its failures (my two finding tests) are subtracted from every mutant
        rc, base_failed, cerr, secs, log = run(tree)
        open(os.path.join(os.path.dirname(out_tsv), "mut_BASE.log"), "w").write(log)
        f.write(f"BASE\trc={rc} {secs:.0f}s\tfailing at baseline: {','.join(base_failed) or '-'}\n"); f.flush()
        base = set(base_failed)
        for mid, rel, old, new, what in MUTANTS:
            if only and mid not in only:
                continue
            path = os.path.join(tree, rel)
            before = sha(path)
            src = open(path).read()
            n = src.count(old)
            if n != 1:
                f.write(f"{mid}\tNOT APPLIED (old text found {n} times)\t\t\t{what}\n"); f.flush()
                continue
            mutated = src.replace(old, new)
            if mid in SECOND:
                o2, n2 = SECOND[mid]
                assert mutated.count(o2) == 1, mid
                mutated = mutated.replace(o2, n2)
            try:
                open(path, "w").write(mutated)
                rc, failed, cerr, secs, log = run(tree)
                open(os.path.join(os.path.dirname(out_tsv), f"mut_{mid}.log"), "w").write(log)
                failed = [x for x in failed if x not in base]
                mine = [x for x in failed if x.startswith("r5b_")]
                seat = [x for x in failed if not x.startswith("r5b_")]
                status = "COMPILE ERROR" if cerr else ("KILLED" if seat else ("SURVIVED (seat) / killed by mine" if mine else "SURVIVED"))
                f.write(f"{mid}\t{status}\trc={rc} {secs:.0f}s\tseat: {','.join(seat) or '-'}\tmine: {','.join(mine) or '-'}\t{what}\n")
                f.flush()
            finally:
                open(path, "w").write(src)
                assert sha(path) == before, f"{mid}: restore failed"


if __name__ == "__main__":
    main()
