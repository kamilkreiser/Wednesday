#!/usr/bin/env python3
"""Round-2 mutation run for coagent-policy @ 379332d: apply ONE textual mutation, run the builder's FULL crate
suite (lib + every tests/*.rs the builder ships, including q01; NOT my r2_gate_attacks.rs), record
caught/SURVIVED, restore the file byte-for-byte."""
import os, subprocess, sys, pathlib

S = "/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/1d34e9cf-ed94-49aa-ba4c-99451dcbbc42/scratchpad/gate_m2_policy_r2"
CR = pathlib.Path(S) / "repo/crates/coagent-policy"
T = "/Volumes/Laptop-DEV/!CODING/Claude to Claude/coagent/tools"
env = dict(os.environ, RUSTUP_HOME=T + "/rustup", CARGO_HOME=T + "/cargo",
           PATH=T + "/cargo/bin:" + os.environ["PATH"], CARGO_TARGET_DIR=S + "/target-mut")

M = [
 ("R1 sort allows -o", "src/shell/allow.rs", '(Flag(\'b\'), "ignore leading blanks"),', '(Flag(\'b\'), "ignore leading blanks"),\n            (Flag(\'o\'), "MUTANT"),'),
 ("R2 grep allows -R", "src/shell/allow.rs", '    (Flag(\'E\'), "extended regular expressions"),', '    (Flag(\'E\'), "extended regular expressions"),\n    (Flag(\'R\'), "MUTANT"),'),
 ("R3 long options prefix-tolerant", "src/shell/allow.rs",
  "LongEq(name, kind) => v\n                    .strip_prefix(name)\n                    .and_then(|r| r.strip_prefix('='))\n                    .map(|val| (*kind, val)),",
  "LongEq(name, kind) => v\n                    .split_once('=')\n                    .filter(|(k, _)| name.starts_with(*k))\n                    .map(|(_, val)| (*kind, val)),"),
 ("R4 find -newer operand not tiered", "src/shell/allow.rs",
  "                if kind == ReadPath {\n                    paths.push((super::path_raw(val), false));\n                }", ""),
 ("R5 find accepts unknown -primary", "src/shell/allow.rs",
  "            None if v.starts_with('-') => {\n                return Err(\"find option or primary not on the allow-list\")\n            }",
  "            None if v == \"-exec\" => {\n                return Err(\"find option or primary not on the allow-list\")\n            }"),
 ("R6 ';' allowed in a line with cd (line check only)", "src/shell/mod.rs",
  "has_cd && line.seps.iter().any(|s| *s != Sep::AndAnd)", "false && line.seps.iter().any(|s| *s != Sep::AndAnd)"),
 ("R7 cd target need not exist", "src/action.rs",
  "Some(d) if std::fs::metadata(d).is_ok_and(|m| m.is_dir()) => dirs.push(next),", "Some(_d) => dirs.push(next),"),
 ("R8 second pipeline stage operands not tiered", "src/shell/mod.rs",
  "commands.push((cds.len(), allow::check(spec, &words[1..], pos > 0)?));",
  "let c = allow::check(spec, &words[1..], pos > 0)?; if pos == 0 { commands.push((cds.len(), c)); }"),
 ("R9 '*' treated as plain", "src/shell/lexer.rs", 'const PLAIN: &str = "-_./:,+@%=";', 'const PLAIN: &str = "-_./:,+@%=*";'),
 ("R10 MAX_MENTIONS bound dropped", "src/action.rs", "if why == OVERSIZE || scan.pieces.len() > MAX_MENTIONS =>", "if why == OVERSIZE =>"),
 ("R11 mentions checked only up to 10", "src/action.rs", "for piece in scan.pieces.iter().take(MAX_MENTIONS + 1) {", "for piece in scan.pieces.iter().take(10) {"),
 ("R12 card cwd not escaped", "src/engine.rs", "cwd: Some(visible(&action.cwd.display())),", "cwd: Some(action.cwd.display()),"),
 ("R13 card tool_name not escaped", "src/engine.rs", "tool_name: visible(&action.tool_name),", "tool_name: action.tool_name.clone(),"),
 ("R14 package.json T3 dropped", "src/patterns.rs", '    p(\n        Anywhere,\n        "package.json",\n        "npm scripts run by npm test / npm run",\n    ),\n', ""),
 ("R15 closed link allows T1", "src/engine.rs", "        let pass = a.tier == Tier::T0;", "        let pass = a.tier <= Tier::T1;"),
 ("R16 filter grep -r treated as stdin-only", "src/shell/allow.rs",
  "let stdin_only = filter_position && operands.is_empty() && !recursive_flag;", "let stdin_only = filter_position && operands.is_empty();"),
 ("R17 path component bound dropped in resolve", "src/path/mod.rs",
  "        if absolute.as_os_str().len() > MAX_PATH_BYTES\n            || absolute.components().count() > MAX_PATH_COMPONENTS\n        {\n            return unc(TOO_LONG);\n        }", ""),
 ("R18 PowerShell parameter prefixes accepted", "src/shell/powershell.rs",
  "allowed.iter().find(|(n, _)| *n == lv)", "allowed.iter().find(|(n, _)| n.starts_with(lv.as_str()))"),
 ("R19 PowerShell colon form accepted", "src/shell/powershell.rs",
  "            if v.contains(':') {\n                return Err(\"parameter with an attached value\");\n            }", ""),
 ("R20 lexer '=' at word start accepted", "src/shell/lexer.rs",
  "                '=' if i == start => {\n                    return Err(\"unquoted '=' at the start of a word (zsh =cmd expansion)\");\n                }", ""),
 ("R21 cd operand any form", "src/shell/mod.rs",
  "v.starts_with('/') || v.starts_with(\"./\")", "true || v.starts_with('/') || v.starts_with(\"./\")"),
 ("R22 automount prefixes reach the OS", "src/path/mod.rs",
  "if NO_OS_PREFIXES.iter().any(|p| absolute.starts_with(p)) {", "if false && NO_OS_PREFIXES.iter().any(|p| absolute.starts_with(p)) {"),
 ("R23 deny-side fold ASCII only", "src/rules.rs", ".map(|c| c.to_lowercase().next().unwrap_or(c))", ".map(|c| c.to_ascii_lowercase())"),
 ("R24 free text checked only 100 chars", "src/action.rs", "let bounded: String = text.chars().take(MAX_FREE_TEXT_CHARS).collect();", "let bounded: String = text.chars().take(100).collect();"),
 ("R25 lexer '~' mid-word accepted", "src/shell/lexer.rs",
  "                        let _ = last_plain;\n                        return Err(\"unquoted '~' inside a word (tilde expansion or zsh glob)\");",
  "                        let _ = last_plain;"),
 ("M4' uncertain path inside", "src/engine.rs", "    p.canonical().is_some_and(|c| state.within_workspace(c))\n}",
  "    match p { NormPath::Uncertain { .. } => true, _ => p.canonical().is_some_and(|c| state.within_workspace(c)) }\n}"),
 ("M7' ExactCommand ignores tool name", "src/engine.rs", "            action.tool_name == \"Bash\"\n                && same_cwd", "            same_cwd"),
 ("M12' git recognised as read", "src/shell/mod.rs", "            #[cfg(feature = \"red_git_is_read\")]\n            if name == \"git\"", "            #[cfg(not(feature = \"red_git_is_read\"))]\n            if name == \"git\""),
 ("M14' memory allows recursive reads", "src/engine.rs", "    !recursive\n        && !reads.is_empty()", "    !reads.is_empty()"),
 ("M17' ReadsUnder drops kind/execute checks", "src/engine.rs", "            matches!(action.kind, Kind::Read | Kind::Search)\n                && not_execute(action)\n                && !ps.is_empty()", "            !ps.is_empty()"),
 ("M18' drop .gitattributes T3", "src/patterns.rs", '    p(\n        Anywhere,\n        ".gitattributes",\n        "textconv/filter drivers run programs on git diff/show",\n    ),\n', ""),
]

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
        r = subprocess.run(["cargo", "+1.100.0", "test", "--manifest-path", S + "/repo/Cargo.toml", "-p", "coagent-policy", "--offline",
                            "--tests", "--no-fail-fast"],
                           env=env, capture_output=True, text=True, timeout=1500)
        out = r.stdout + r.stderr
        if "error[" in out or "could not compile" in out:
            verdict = "DID NOT COMPILE"
        else:
            failed = [l.split()[1] for l in out.splitlines() if l.startswith("test ") and l.endswith("FAILED")]
            failed = [x for x in failed if not x.startswith(("n1", "n2", "n3", "n4", "n5", "n6", "n7"))]
            r2only = [l.split()[1] for l in out.splitlines() if l.startswith("test ") and l.endswith("FAILED")]
            verdict = ("caught by " + ", ".join(failed[:4])) if failed else "SURVIVED"
    finally:
        p.write_bytes(orig)
    print(f"{name}: {verdict}", flush=True)
