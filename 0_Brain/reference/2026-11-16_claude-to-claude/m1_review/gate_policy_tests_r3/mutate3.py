#!/usr/bin/env python3
# Round-3 mutation runner: apply ONE textual mutation, run the builder's full coagent-policy suite
# (lib + every tests/*.rs it ships; the gate's r3 file is NOT in tests/ during the run), record which tests
# fail, restore the file byte for byte. Baseline failures (environment) are subtracted.
import subprocess, sys, os, re, json
REPO = sys.argv[1]
OUT = sys.argv[2]
SRC = os.path.join(REPO, "crates/coagent-policy/src")
M = [
 ("M1 PowerShell Get-Content falls back to a Read target", "action.rs",
  "    let _ = host;\n    shell_execute(cmd, ShellKind::PowerShell, cwd, env, norm)",
  "    let _ = host;\n    if let Some(rest) = cmd.and_then(|c| c.strip_prefix(\"Get-Content \")) {\n        return (Kind::Read, vec![Target::Path { role: PathRole::Read, path: norm.normalise(rest, cwd, env) }]);\n    }\n    shell_execute(cmd, ShellKind::PowerShell, cwd, env, norm)"),
 ("M2 no Unicode fold in component_match (old per-char lower-case)", "glob.rs",
  "if ci && !(pat.is_ascii() && s.is_ascii()) {", "if false && ci && !(pat.is_ascii() && s.is_ascii()) {"),
 ("M3 fold only the candidate", "glob.rs",
  "let (fp, fs) = (fold_name(pat), fold_name(s));", "let (fp, fs) = (pat.to_string(), fold_name(s));"),
 ("M4 default-ignorables not removed", "glob.rs",
  "        if crate::text::invisible(c) {\n            continue;\n        }", "        if false && crate::text::invisible(c) {\n            continue;\n        }"),
 ("M4b default-ignorables not removed (both passes)", "glob.rs",
  "    out.nfkc().filter(|c| !crate::text::invisible(*c)).collect()", "    out.nfkc().collect()"),
 ("M4c default-ignorables removed in neither pass", "glob.rs",
  "        if crate::text::invisible(c) {\n            continue;\n        }\n        match c {", "        match c {"),
 ("M5 exact-command match case-insensitive", "engine.rs",
  "matches!(t, Target::Command { text: t2, .. } if t2 == text)", "matches!(t, Target::Command { text: t2, .. } if t2.eq_ignore_ascii_case(text))"),
 ("M6 exact-command ignores cwd", "engine.rs",
  "let same_cwd = action.cwd.canonical() == Some(cwd.as_path());", "let same_cwd = { let _ = cwd; true };"),
 ("M7 exact-command ignores the tool", "engine.rs",
  "            action.tool_name == \"Bash\"\n                && same_cwd", "            true\n                && same_cwd"),
 ("M8 hash omits the cwd", "hash.rs",
  "for part in [tool_name, cwd, body.as_str()] {", "for part in [tool_name, { let _ = cwd; \"\" }, body.as_str()] {"),
 ("M9 over MAX_MENTIONS passes as T2", "action.rs",
  "            || scan.pieces.len() > MAX_MENTIONS\n", "            || false\n"),
 ("M10 over 64 KiB passes as T2", "action.rs",
  "        } if why == OVERSIZE\n", "        } if false\n"),
 ("M11 no ancestor-of-credential T3", "engine.rs",
  "                let cred_mode = if *role == PathRole::Mentioned {\n                    Mode::Shell { ancestor: true }",
  "                let cred_mode = if *role == PathRole::Mentioned {\n                    mode"),
 ("M12 grant line '*' matches by prefix", "grant.rs",
  "    line == cmd\n", "    line == cmd || line.strip_suffix('*').is_some_and(|p| cmd.starts_with(p))\n"),
 ("M13 exclusions not matched by name in shell text", "engine.rs",
  "                if *role == PathRole::Mentioned\n                    && (first_hit_by_name(&state.exclusions, &sp).is_some()",
  "                if false && *role == PathRole::Mentioned\n                    && (first_hit_by_name(&state.exclusions, &sp).is_some()"),
 ("M14 hard deny not matched by name in shell text", "engine.rs",
  "first_hit(&state.hard_deny, &sp, mode).or_else(|| by_name(&state.hard_deny))", "first_hit(&state.hard_deny, &sp, mode)"),
 ("M15 privilege words not T3", "engine.rs",
  "    if has(T3_PRIVILEGE.words) {", "    if false && has(T3_PRIVILEGE.words) {"),
 ("M16 dangerouslyDisableSandbox ignored", "engine.rs",
  "    if action.sandbox_disabled {", "    if false && action.sandbox_disabled {"),
 ("M17 T3 execute reachable by approvals/grant", "engine.rs",
  "    if a.tier == Tier::T3 {\n        return ask(action, state, &a, surface, now, vec![]);",
  "    if a.tier == Tier::T3 && action.kind != Kind::Execute {\n        return ask(action, state, &a, surface, now, vec![]);"),
 ("M18 grant execute matches PowerShell too", "engine.rs",
  "                Target::Command {\n                    text,\n                    shell: ShellKind::Bash,\n                    ..\n                } => Some(text),",
  "                Target::Command {\n                    text,\n                    ..\n                } => Some(text),"),
 ("M19 quoted/escaped whole words not scanned", "shell/mod.rs",
  "    for w in lenient_words(text) {", "    for w in lenient_words(text).into_iter().take(0) {"),
 ("M20 MAX_MENTION_COMPONENTS bound dropped", "action.rs",
  "            || mention_components(scan) > MAX_MENTION_COMPONENTS =>", "            || false =>"),
 ("M21 ss for sharp s dropped", "glob.rs",
  "            '\\u{DF}' | '\\u{1E9E}' => out.push_str(\"ss\"),", "            '\\u{1E9E}' => out.push_str(\"ss\"),"),
 ("M22 grant scopes folded (allow side widened)", "engine.rs",
  "            covers_subtree(&p.comps, c, false)\n        } else {\n            match_components(&p.comps, c, false) || covers_subtree(&p.comps, c, false)",
  "            covers_subtree(&p.comps, c, true)\n        } else {\n            match_components(&p.comps, c, true) || covers_subtree(&p.comps, c, true)"),
 # round-2 survivors that still apply
 ("R11 mentions checked only up to 10 words", "action.rs",
  "const MENTION_CHECK_CAP: usize = MAX_MENTIONS + 1;", "const MENTION_CHECK_CAP: usize = 10;"),
 ("R17 component bound dropped on the realpath-success branch", "path/mod.rs",
  "            if too_deep(&c) {\n                return unc(TOO_LONG);", "            if false && too_deep(&c) {\n                return unc(TOO_LONG);"),
 ("R22 automount prefixes reach the OS", "path/mod.rs",
  "        if NO_OS_PREFIXES\n            .iter()", "        if false && NO_OS_PREFIXES\n            .iter()"),
 ("R24 free text checked for only 100 chars", "action.rs",
  "const FREE_TEXT_CHECK_CHARS: usize = MAX_FREE_TEXT_CHARS;", "const FREE_TEXT_CHECK_CHARS: usize = 100;"),
 ("M14' memory allows recursive reads", "engine.rs",
  "    !recursive\n        && !reads.is_empty()", "    true\n        && !reads.is_empty()"),
]

def run():
    env = dict(os.environ)
    r = subprocess.run(["cargo", "test", "--manifest-path", os.path.join(REPO, "Cargo.toml"), "-p", "coagent-policy",
                        "--offline", "--no-fail-fast"], capture_output=True, text=True, env=env)
    out = r.stdout + r.stderr
    failed = sorted(set(re.findall(r"^test (\S+) \.\.\. FAILED", out, re.M)))
    compile_err = "error[E" in out or "could not compile" in out
    return failed, compile_err, out

only = sys.argv[3:] if len(sys.argv) > 3 else None
base_failed, ce, _ = run()
log = open(OUT, "a")
log.write(f"BASELINE failed={base_failed} compile_error={ce}\n"); log.flush()
for name, f, old, new in M:
    if only and not any(name.startswith(o + " ") for o in only):
        continue
    p = os.path.join(SRC, f)
    orig = open(p, encoding="utf-8").read()
    n = orig.count(old)
    if n != 1:
        log.write(f"{name}: NOT APPLIED (pattern found {n} times)\n"); log.flush(); continue
    open(p, "w", encoding="utf-8").write(orig.replace(old, new))
    try:
        failed, ce, out = run()
    finally:
        open(p, "w", encoding="utf-8").write(orig)
    new_fail = [t for t in failed if t not in base_failed]
    if ce:
        log.write(f"{name}: COMPILE ERROR\n" + "\n".join(l for l in out.splitlines() if l.startswith("error"))[:600] + "\n")
    elif new_fail:
        log.write(f"{name}: CAUGHT by {len(new_fail)}: {', '.join(new_fail[:6])}\n")
    else:
        log.write(f"{name}: SURVIVED\n")
    log.flush()
st = subprocess.run(["git", "-C", REPO, "status", "--porcelain"], capture_output=True, text=True).stdout
log.write(f"git status after: {st!r}\n")
