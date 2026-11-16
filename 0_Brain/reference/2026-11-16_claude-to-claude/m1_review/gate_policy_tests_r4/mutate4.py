"""Round-4 mutation runner: one mutant at a time on the mutation clone, FULL coagent-policy suite (the builder's
tests only), source restored byte for byte after each. Usage: python3 -I mutate4.py [ids...]"""
import os, subprocess, sys, time, re

S = "/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/1d34e9cf-ed94-49aa-ba4c-99451dcbbc42/scratchpad/gate_m2_policy_r4"
TAG = os.environ.get("MUT_TAG", "mut")
REPO = f"{S}/{TAG}"
SH = "crates/coagent-policy/src/shell/mod.rs"
EN = "crates/coagent-policy/src/engine.rs"
AC = "crates/coagent-policy/src/action.rs"

M = [
    ("A1 add '*' to the PLAIN set", SH, 'const PLAIN_CHARS: &str = "/._-:,+@%=";', 'const PLAIN_CHARS: &str = "/._-:,+@%=*";'),
    ("A2 add '$' to the PLAIN set", SH, 'const PLAIN_CHARS: &str = "/._-:,+@%=";', 'const PLAIN_CHARS: &str = "/._-:,+@%=$";'),
    ("A3 add '~' to the PLAIN set (tilde anywhere)", SH, 'const PLAIN_CHARS: &str = "/._-:,+@%=";', 'const PLAIN_CHARS: &str = "/._-:,+@%=~";'),
    ("A4 add '{' '}' (brace) to the PLAIN set", SH, 'const PLAIN_CHARS: &str = "/._-:,+@%=";', 'const PLAIN_CHARS: &str = "/._-:,+@%={}";'),
    ("A5 non-ASCII letters plain", SH, "    c.is_ascii_alphanumeric() || PLAIN_CHARS.contains(c)\n}", "    c.is_alphanumeric() || PLAIN_CHARS.contains(c)\n}"),
    ("A6 tabs/newlines as separators (split_whitespace, no control check)", SH,
     "    if body.chars().any(|c| c.is_control()) {\n        return Err(\"control character (newline, tab, ...)\");\n    }\n    let toks: Vec<&str> = body.split(' ').filter(|t| !t.is_empty()).collect();",
     "    let toks: Vec<&str> = body.split_whitespace().collect();"),
    ("A7 operator glued to a word ('>' '<' in words)", SH, 'const PLAIN_CHARS: &str = "/._-:,+@%=";', 'const PLAIN_CHARS: &str = "/._-:,+@%=<>&";'),
    ("A8 drop 'eval' from the refused builtins", SH, '    "eval",\n', ''),
    ("A9 drop '.' from the refused builtins", SH, '    ".",\n', ''),
    ("A10 drop 'export' from the refused builtins", SH, '    "export",\n', ''),
    ("A11 no assignment check in command position", SH, "            if t.contains('=') {\n                return Err(\"assignment in command position\");\n            }", ""),
    ("A12 '=' first allowed", SH, "    if w.starts_with('=') {\n        return Err(\"'=' at the start of a word (zsh =cmd)\");\n    }", ""),
    ("A13 quoted word: any content", SH, "        if inner.chars().all(plain_word_char) {", "        if true {"),
    ("A14 leading operator allowed", SH, "                return Err(\"operator without a command before it\");", "                expect_word = true;"),
    ("A15 trailing operator allowed", SH, "    if expect_word && !toks.is_empty() {\n        return Err(\"command ends with an operator\");\n    }", ""),
    ("B1 attached option arguments not scanned (whole-word again)", SH, "        if !w.starts_with('-') {\n            return;\n        }", "        if true {\n            return;\n        }"),
    ("B2 attached short-option argument (body[1..]) dropped", SH, "            add_piece(&body[1..], scan, seen);", "            let _ = body;"),
    ("B3 suffix at '/' or '~' dropped", SH, "            if i > 0 && (c == '/' || c == '~') {", "            if i > 0 && false {"),
    ("B4 '=' not a split character (of=/path)", SH, '";&|<>()`$={},:"', '";&|<>()`${},:"'),
    ("B5 ',' and ':' not split characters", SH, '";&|<>()`$={},:"', '";&|<>()`$={}"'),
    ("B6 scan stops at the first ';' (skip after one operator)", SH, "    let cleaned: String = text\n        .chars()", "    let cleaned: String = text\n        .split(';').next().unwrap_or(\"\")\n        .chars()"),
    ("B7 redirection targets not write targets", AC, "        for w in &scan.writes {", "        for w in scan.writes.iter().take(0) {"),
    ("B8 basename of a word not checked", SH, "        if base != lower && !base.is_empty() {", "        if false {"),
    ("B9 no fold of command words", SH, "    let f = crate::glob::fold_name(&lower);\n    if f != lower {", "    let f = lower.clone();\n    if f != lower {"),
    ("C1 OPAQUE raised to T2 only (batchable)", EN, "                    a.raise(Tier::T3, Some(Reason::ShellExpansion));\n                    #[cfg(feature = \"red_opaque_batchable\")]",
     "                    a.raise(Tier::T2, Some(Reason::ShellExpansion));\n                    #[cfg(feature = \"red_opaque_batchable\")]"),
    ("C2 OPAQUE fixed reason dropped", EN, "                    a.raise(Tier::T3, Some(Reason::ShellExpansion));\n                    #[cfg(feature = \"red_opaque_batchable\")]",
     "                    a.raise(Tier::T3, None);\n                    #[cfg(feature = \"red_opaque_batchable\")]"),
    ("C3 bash_plain result ignored (everything PLAIN)", AC, "            Err(why) => scan.opaque = Some(why),", "            Err(_why) => {}"),
    ("C4 PowerShell always PLAIN", SH, "        Err(\"PowerShell text outside the plain set\")", "        Ok(())"),
    ("C5 PowerShell '$' plain", SH, '.all(|c| c.is_ascii_alphanumeric() || " -._/\\\\:".contains(c))', '.all(|c| c.is_ascii_alphanumeric() || " -._/\\\\:$".contains(c))'),
    ("C6 T3 batchable", EN, "        batchable: !t3,", "        batchable: true,"),
    ("C7 session scope offered for T3", EN, "    if a.tier == Tier::T3 || a.may_read_excluded {\n        return None;", "    if a.may_read_excluded {\n        return None;"),
    ("D1 brace expansion cap 64 -> 1", SH, "    if out.len() >= 64 || depth > 16 {", "    if out.len() >= 1 || depth > 16 {"),
    ("D2 brace expansion not done", SH, "        if w.contains('{') {\n            for e in brace_expand(&w) {", "        if false {\n            for e in brace_expand(&w) {"),
    ("D3 $HOME not decoded", SH, '    let t = text.replace("${HOME}", "~").replace("$HOME", "~");', '    let t = text.to_string();'),
    ("D4 ANSI-C not decoded", SH, "        if b[i] == '$' && b.get(i + 1) == Some(&'\\'') {", "        if false {"),
    ("E1 (round-3 M5) exact command case-insensitive", EN, "    {\n        a == b\n    }", "    {\n        a.eq_ignore_ascii_case(b)\n    }"),
    ("E2 (round-3 M18) grant line matches PowerShell", EN, "                Target::Command {\n                    text,\n                    shell: ShellKind::Bash,\n                    ..\n                } => Some(text),", "                Target::Command { text, .. } => Some(text),"),
    ("E3 (round-3 M22) grant scopes folded", EN, "    #[cfg(not(feature = \"red_grant_scope_folds\"))]\n    let ci = false;", "    #[cfg(not(feature = \"red_grant_scope_folds\"))]\n    let ci = true;"),
    ("E4 (m1) exact command through a symlinked cwd", EN, "            let same_cwd =\n                action.cwd.canonical() == Some(cwd.as_path()) && cwd_is_physical(&action.cwd);", "            let same_cwd = action.cwd.canonical() == Some(cwd.as_path());"),
    ("E5 CredentialFolder reported as CredentialPath", EN, "                    a.raise(Tier::T3, Some(Reason::CredentialFolder(p.reason)));", "                    a.raise(Tier::T3, Some(Reason::CredentialPath(p.reason)));"),
]

def run(ids):
    env = dict(os.environ)
    env["CARGO_TARGET_DIR"] = f"{S}/target_{TAG}"
    env["COAGENT_TEST_TMP"] = f"{S}/ci_{TAG}"
    env["CARGO_PROFILE_TEST_OPT_LEVEL"] = "2"
    env["CARGO_PROFILE_DEV_OPT_LEVEL"] = "2"
    os.makedirs(f"{S}/ci_{TAG}", exist_ok=True)
    log = open(f"{S}/logs/mut4.log", "a")
    for (name, f, old, new) in M:
        mid = name.split()[0]
        if ids and mid not in ids:
            continue
        path = f"{REPO}/{f}"
        src = open(path).read()
        n = src.count(old)
        if n != 1:
            print(f"{mid} ANCHOR COUNT {n}: {name}", flush=True); log.write(f"{mid} ANCHOR {n}\n"); continue
        open(path, "w").write(src.replace(old, new))
        t = time.time()
        try:
            p = subprocess.run(["cargo", "test", "--manifest-path", f"{REPO}/Cargo.toml", "-p", "coagent-policy", "--offline", "--no-fail-fast"],
                               capture_output=True, text=True, env=env, timeout=1500)
            out = p.stdout + p.stderr
            rc = p.returncode
        except subprocess.TimeoutExpired as e:
            out = (e.stdout or b"").decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
            rc = "TIMEOUT"
        finally:
            open(path, "w").write(src)
        failed = sorted(set(re.findall(r"^test (\S+) \.\.\. FAILED", out, re.M)))
        if "error[E" in out or "error: could not compile" in out:
            verdict = "COMPILE-ERROR"
        elif failed:
            verdict = "caught by " + ", ".join(failed[:6]) + (f" (+{len(failed)-6})" if len(failed) > 6 else "")
        elif rc == "TIMEOUT":
            verdict = "TIMEOUT"
        else:
            verdict = "SURVIVED"
        line = f"{mid} | {name} | {verdict} | rc={rc} | {int(time.time()-t)}s"
        print(line, flush=True); log.write(line + "\n"); log.flush()
        if verdict == "COMPILE-ERROR":
            log.write("\n".join(l for l in out.splitlines() if "error" in l)[:2000] + "\n")
    st = subprocess.run(["git", "-C", REPO, "status", "--porcelain"], capture_output=True, text=True).stdout
    print("git status porcelain:", repr(st)); log.write(f"porcelain: {st!r}\n")

run(sys.argv[1:])
