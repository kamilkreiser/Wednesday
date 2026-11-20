#!/usr/bin/env python3
"""QA-WIN-IPC mutations of crates/coagent-ipc/src/endpoint.rs and src/sid.rs.
Each mutant: exact text replacement (anchor must occur exactly once), then
  (a) the builder's tests: cargo test -p coagent-ipc --test win_name
  (b) my tests:            cargo test -p coagent-ipc --test qa_win_name --release
The source is restored after every mutant and checked against git at the end.
Usage: python3 -I qa_mutate.py <worktree root>   (toolchain env set; CARGO_TARGET_DIR private to that worktree)"""
import subprocess, sys, os
ROOT = sys.argv[1]
E = "crates/coagent-ipc/src/endpoint.rs"
S = "crates/coagent-ipc/src/sid.rs"
MUT = [
 ("Q1", "fold non-ASCII letters too", E,
  "let mut text: Vec<u8> = absolute_path\n        .bytes()",
  "let lowered = absolute_path.to_lowercase();\n    let mut text: Vec<u8> = lowered\n        .bytes()"),
 ("Q2", "drop every trailing separator (two or more)", E,
  "if text.last() == Some(&b'\\\\') {\n        text.pop();\n    }",
  "while text.last() == Some(&b'\\\\') {\n        text.pop();\n    }"),
 ("Q3", "escape with upper-case hex", E, "{b:02x}", "{b:02X}"),
 ("Q4", "accept a drive-relative path (C:, C:x) as absolute", E,
  "[d, b':', s, ..] if d.is_ascii_alphabetic() && is_sep(*s) => true,",
  "[d, b':', ..] if d.is_ascii_alphabetic() => true,"),
 ("Q5", "compare identifiers without ASCII folding", S,
  "peer.eq_ignore_ascii_case(expected)", "peer == expected"),
 ("Q6", "an empty expected identifier equals an empty peer", S,
  "!peer.is_empty() && !expected.is_empty() && peer.eq_ignore_ascii_case(expected)",
  "peer.eq_ignore_ascii_case(expected)"),
 ("Q7", "never drop the trailing separator", E,
  "if text.last() == Some(&b'\\\\') {\n        text.pop();\n    }", ""),
 ("Q8", "length limit off by one (refuse at the limit)", E,
  "if name.len() > MAX_PIPE_NAME {", "if name.len() >= MAX_PIPE_NAME {"),
 ("Q9", "keep '/' (no slash folding)", E,
  "if b == b'/' {\n                b'\\\\'", "if false && b == b'/' {\n                b'\\\\'"),
 ("Q10", "'~' kept literally (escape no longer self-delimiting)", E,
  "matches!(b, b'.' | b'_' | b'-')", "matches!(b, b'.' | b'_' | b'-' | b'~')"),
 ("Q11", "UNC arm accepts three separators", E,
  "[s1, s2, c, ..] if is_sep(*s1) && is_sep(*s2) && !is_sep(*c) => true,",
  "[s1, s2, _c, ..] if is_sep(*s1) && is_sep(*s2) => true,"),
 ("Q12", "Unix endpoint drops the ipc folder", E,
  'Ok(data_dir.join("ipc").join("daemon.sock"))', 'Ok(data_dir.join("daemon.sock"))'),
 ("Q13", "length counted before the prefix (limit 8 bytes too generous)", E,
  "if name.len() > MAX_PIPE_NAME {", "if name.len() - NAME_PREFIX.len() > MAX_PIPE_NAME {"),
 ("Q14", "':' kept literally", E,
  "matches!(b, b'.' | b'_' | b'-')", "matches!(b, b'.' | b'_' | b'-' | b':')"),
 ("Q15", "sid compare: prefix match", S,
  "peer.eq_ignore_ascii_case(expected)", "expected.to_ascii_uppercase().starts_with(&peer.to_ascii_uppercase())"),
]
def run(args, env=None):
    return subprocess.run(args, cwd=ROOT, capture_output=True, text=True, env=env)
def test(name, release):
    a = ["cargo", "test", "--locked", "-p", "coagent-ipc", "--test", name] + (["--release"] if release else [])
    r = run(a)
    out = r.stdout + r.stderr
    if r.returncode == 0:
        return "survives"
    if "error[" in out or "could not compile" in out:
        return "NO-COMPILE"
    failed = [l.split()[1] for l in out.splitlines() if l.startswith("test ") and l.endswith("FAILED")]
    return "KILLED(" + ",".join(f.split("::")[-1] for f in failed[:4]) + ")"
only = set(sys.argv[2:])
print(f"{'id':4} {'mutation':55} {'builder win_name':40} {'my qa_win_name'}")
for mid, what, rel, old, new in MUT:
    if only and mid not in only:
        continue
    p = os.path.join(ROOT, rel)
    orig = open(p, encoding="utf-8").read()
    n = orig.count(old)
    if n != 1:
        print(f"{mid:4} {what:55} ANCHOR FOUND {n} TIMES")
        continue
    try:
        open(p, "w", encoding="utf-8").write(orig.replace(old, new, 1))
        b = test("win_name", False)
        q = test("qa_win_name", True)
        print(f"{mid:4} {what:55} {b:40} {q}", flush=True)
    finally:
        open(p, "w", encoding="utf-8").write(orig)
d = run(["git", "diff", "--stat", "--", "crates/coagent-ipc/src"])
print("restored:", "yes (git diff of src empty)" if not d.stdout.strip() else d.stdout)
