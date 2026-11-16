#!/usr/bin/env python3
"""Mutation run for coagent-policy: apply ONE textual mutation, run the builder's full crate suite
(unit + t01..t12, NOT the QA q01 file), record caught/SURVIVED, restore the file byte-for-byte."""
import os, subprocess, sys, pathlib

S = "/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/1d34e9cf-ed94-49aa-ba4c-99451dcbbc42/scratchpad/gate_m2_policy"
CR = pathlib.Path(S) / "repo/crates/coagent-policy"
T = "/Volumes/Laptop-DEV/!CODING/Claude to Claude/coagent/tools"
env = dict(os.environ, RUSTUP_HOME=T + "/rustup", CARGO_HOME=T + "/cargo",
           PATH=T + "/cargo/bin:" + os.environ["PATH"], CARGO_TARGET_DIR=S + "/target-mut")

M = [
 ("M1 closed-link allows T3 reads", "src/engine.rs", "if a.tier < Tier::T3\n            && matches!(action.kind, Kind::Read | Kind::Search)", "if a.tier <= Tier::T3\n            && matches!(action.kind, Kind::Read | Kind::Search)"),
 ("M2 drop ~/.zshrc hard deny", "src/patterns.rs", 'p(Home, ".zshrc", "shell rc file"),', ""),
 ("M3 free text skips exclusion check", "src/engine.rs", "                if first_hit(&excl, path, excl_mode).is_some() {\n                    a.excluded = true;\n                }\n                if *role == PathRole::InText {\n                    continue; // free text: exclusions only\n                }", "                if *role == PathRole::InText {\n                    continue;\n                }\n                if first_hit(&excl, path, excl_mode).is_some() {\n                    a.excluded = true;\n                }"),
 ("M4 Uncertain treated as inside", "src/engine.rs", "p.canonical().is_some_and(|c| state.within_workspace(c))", "match p { NormPath::Uncertain { .. } => true, _ => p.canonical().is_some_and(|c| state.within_workspace(c)) }"),
 ("M5 lexer accepts unquoted '!'", "src/shell/lexer.rs", "'!' => return Err(\"unquoted '!'\"),", "'!' => { w.value.push('!'); i += 1; }"),
 ("M6 grant expiry off-by-one", "src/engine.rs", "if now < g.issued_at || now >= g.expires_at {", "if now < g.issued_at || now > g.expires_at {"),
 ("M7 ExactCommand ignores tool name", "src/engine.rs", "            action.tool_name == \"Bash\"\n                && same_cwd", "            same_cwd"),
 ("M8 T3 gets a session scope", "src/engine.rs", "if a.tier == Tier::T3 || a.may_read_excluded {\n        return None;", "if a.may_read_excluded {\n        return None;"),
 ("M9 max_actions > instead of >=", "src/engine.rs", ".is_some_and(|m| gs.actions_used >= m)", ".is_some_and(|m| gs.actions_used > m)"),
 ("M10 find -execdir accepted", "src/shell/mod.rs", '    "-execdir",\n', ""),
 ("M11 grep -f accepted", "src/shell/mod.rs", 'refuse_if(cl.contains(\'f\'), "grep -f reads patterns from a file")?;', ""),
 ("M12 git --ext-diff accepted", "src/shell/mod.rs", '                    "--ext-diff",\n', ""),
 ("M13 resolve ignores card expiry", "src/engine.rs", "    if now >= card.expires_at {\n        return deny(DenyReason::Expired);\n    }", ""),
 ("M14 memory allows recursive reads", "src/engine.rs", "    !recursive\n        && !reads.is_empty()", "    !reads.is_empty()"),
 ("M15 wildcard domain without dot boundary", "src/grant.rs", 'host.ends_with(&format!(".{suffix}"))', "host.ends_with(suffix)"),
 ("M16 url_host accepts userinfo", "src/action.rs", "if authority.contains('@') || authority.starts_with('[') {", "if authority.starts_with('[') {"),
 ("M17 ReadsUnder honours execute", "src/engine.rs", "            matches!(action.kind, Kind::Read | Kind::Search)\n                && not_execute(action)\n                && !ps.is_empty()", "            !ps.is_empty()"),
 ("M18 drop .gitattributes T3", "src/patterns.rs", '    p(\n        Anywhere,\n        ".gitattributes",\n        "textconv/filter drivers run programs on git diff/show",\n    ),\n', ""),
 ("M19 deny-side matching case-sensitive", "src/rules.rs", "            Spelling::Abs(c) => abs_hit(pat, c, mode),", "            Spelling::Abs(c) => abs_hit(pat, c, mode) && c.iter().all(|x| x.chars().all(|ch| !ch.is_ascii_uppercase())),"),
 ("M20 sandbox Unknown accepted for execute grant", "src/engine.rs", "&& (state.sandbox != Sandbox::On || action.sandbox_disabled)", "&& (state.sandbox == Sandbox::Off || action.sandbox_disabled)"),
]

tests = ["--lib"] + sum([["--test", t] for t in ["t01_table","t02_property","t03_b16","t04_paths","t05_hard_deny","t06_t3","t07_exclusions","t08_binding","t09_grants","t10_surface","t11_determinism","t12_docs"]], [])
only = sys.argv[1:]
for name, f, old, new in M:
    if only and name.split()[0] not in only:
        continue
    p = CR / f
    orig = p.read_bytes()
    src = orig.decode()
    if src.count(old) != 1:
        print(f"{name}: PATTERN NOT FOUND ({src.count(old)})", flush=True); continue
    p.write_text(src.replace(old, new))
    try:
        r = subprocess.run(["cargo", "+1.100.0", "test", "--manifest-path", S + "/repo/Cargo.toml", "-p", "coagent-policy", "--offline"] + tests,
                           env=env, capture_output=True, text=True, timeout=1500)
        out = r.stdout + r.stderr
        if "error[" in out or "could not compile" in out:
            verdict = "DID NOT COMPILE"
        elif r.returncode != 0:
            failed = [l.split()[1] for l in out.splitlines() if l.startswith("test ") and l.endswith("FAILED")]
            verdict = "caught by " + ", ".join(failed[:4])
        else:
            verdict = "SURVIVED"
    finally:
        p.write_bytes(orig)
    print(f"{name}: {verdict}", flush=True)
