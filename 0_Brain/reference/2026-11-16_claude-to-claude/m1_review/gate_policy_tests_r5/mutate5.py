"""Round-5 mutation runner. One mutant at a time on a mutation clone; the WHOLE coagent-policy suite of the branch
(builder tests + gate files q01/r2/r3/r4) minus `p_identity_60k` (it runs 480 000 real-shell print runs; its one
assertion, deny-or-strict-T3, is also asserted by t17 and r5), PLUS this gate's r5 tests minus the 100k central test.
Source restored byte for byte after each mutant (verified with git status at the end).
Usage: MUT_TAG=mutA python3 -I mutate5.py [ids...]"""
import os, subprocess, sys, time, re

S = "/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/0bad48b2-2056-45a8-9019-8cc0029c12d3/scratchpad/gate_m2_policy_r5"
TAG = os.environ.get("MUT_TAG", "mutA")
REPO = f"{S}/{TAG}"
P = "crates/coagent-policy/src/"
EN, SH, AC, ST, GL = P + "engine.rs", P + "shell/mod.rs", P + "action.rs", P + "state.rs", P + "glob.rs"

M = [
    ("BASE no-op (baseline: must be green)", EN, "        batchable: !t3,", "        batchable: !t3,"),
    # ---- earlier rounds' mutants that still apply (round 3: M*, round 4: B*/C*/E*)
    ("M4 (r3) default-ignorables not removed", GL, "        if crate::text::invisible(c) {\n            continue;\n        }", "        if false && crate::text::invisible(c) {\n            continue;\n        }"),
    ("M4b (r3) default-ignorables not removed in the 2nd pass", GL, "    out.nfkc().filter(|c| !crate::text::invisible(*c)).collect()", "    out.nfkc().collect()"),
    ("M9 (r3) over MAX_MENTIONS not oversize", AC, "            || scan.pieces.len() > MAX_MENTIONS\n", "            || false\n"),
    ("M10 (r3) over 64 KiB not oversize", AC, "        } if why == OVERSIZE\n", "        } if false\n"),
    ("M11 (r3) no ancestor-of-credential T3", EN, "                    Mode::Shell { ancestor: true }", "                    mode"),
    ("M13 (r3) exclusions not matched by name in shell text", EN, "                if *role == PathRole::Mentioned\n", "                if false && *role == PathRole::Mentioned\n"),
    ("M14 (r3) hard deny not matched by name in shell text", EN, "first_hit(&state.hard_deny, &sp, mode).or_else(|| by_name(&state.hard_deny))", "first_hit(&state.hard_deny, &sp, mode)"),
    ("M15 (r3) privilege words not T3", EN, "    if has(T3_PRIVILEGE.words) {", "    if false && has(T3_PRIVILEGE.words) {"),
    ("M16 (r3) dangerouslyDisableSandbox ignored", EN, "    if action.sandbox_disabled {", "    if false && action.sandbox_disabled {"),
    ("M17 (r3) T3 execute reachable by approvals/grant", EN, "    if a.tier == Tier::T3 {\n", "    if a.tier == Tier::T3 && action.kind != Kind::Execute {\n"),
    ("M14' (r3) memory allows recursive reads", EN, "    !recursive\n", "    true\n"),
    ("B1 (r4) attached option arguments not scanned", SH, "        if !w.starts_with('-') {\n            return;\n        }", "        if true {\n            return;\n        }"),
    ("B4 (r4) '=' not a split character", SH, 'const SPLIT: &str = ";&|<>()`$={},:";', 'const SPLIT: &str = ";&|<>()`${},:";'),
    ("B8 (r4) basename of a word not checked", SH, "        if base != lower && !base.is_empty() {", "        if false {"),
    ("B9 (r4) no fold of command words", SH, "    let f = crate::glob::fold_name(&lower);\n    if f != lower {", "    let f = lower.clone();\n    if f != lower {"),
    ("C6 (r4) T3 batchable", EN, "        batchable: !t3,", "        batchable: true,"),
    ("C7 (r4) session scope offered for T3", EN, "    if a.tier == Tier::T3 || a.may_read_excluded {\n        return None;", "    if a.may_read_excluded {\n        return None;"),
    ("E1 (r4) owner list case-insensitive", EN, "        a == b\n", "        a.eq_ignore_ascii_case(b)\n"),
    ("E3 (r4) grant scopes folded", EN, "    let ci = false;", "    let ci = true;"),
    ("E4 (r4) owner list through a symlinked cwd", EN, "action.cwd.canonical() == Some(oc.cwd.as_path()) && cwd_is_physical(&action.cwd);", "action.cwd.canonical() == Some(oc.cwd.as_path());"),
    ("E5 (r4) CredentialFolder reported as CredentialPath", EN, "a.raise(Tier::T3, Some(Reason::CredentialFolder(p.reason)));", "a.raise(Tier::T3, Some(Reason::CredentialPath(p.reason)));"),
    # ---- new: the T3 rule
    ("N1 shell commands T2", EN, "                a.raise(Tier::T3, Some(Reason::ShellExpansion));\n                #[cfg(feature = \"red_shell_not_t3\")]", "                a.raise(Tier::T2, Some(Reason::ShellExpansion));\n                #[cfg(feature = \"red_shell_not_t3\")]"),
    ("N2 shell T3 without the fixed sentence", EN, "                a.raise(Tier::T3, Some(Reason::ShellExpansion));\n                #[cfg(feature = \"red_shell_not_t3\")]", "                a.raise(Tier::T3, None);\n                #[cfg(feature = \"red_shell_not_t3\")]"),
    ("N3 T3 read delay 0 for execute", EN, "        read_delay_secs: if t3 { 5 } else { 0 },", "        read_delay_secs: if t3 && action.kind != Kind::Execute { 5 } else { 0 },"),
    ("N4 T3 execute batchable", EN, "        batchable: !t3,", "        batchable: !t3 || action.kind == Kind::Execute,"),
    ("N5 session scope offered for a T3 execute", EN, "    if a.tier == Tier::T3 || a.may_read_excluded {\n        return None;", "    if (a.tier == Tier::T3 && action.kind != Kind::Execute) || a.may_read_excluded {\n        return None;"),
    ("N6 ExactCommand approval honoured again", EN, "        Scope::ExactCommand { .. } => false,", "        Scope::ExactCommand { text, .. } => action.targets.iter().any(|t| matches!(t, Target::Command { text: t2, .. } if t2 == text)),"),
    ("N7 grant covers execute", EN, "        Kind::Execute => Err(Some(\"a grant never covers a shell command\".into())),", "        Kind::Execute => ok(\"execute\".into(), vec![]),"),
    ("N8 no session scope suppression for execute (equivalent unless T3 broken)", EN, "        Kind::Execute => None,", "        Kind::Execute => Some(Scope::ExactInput { hash: action.raw_input_hash.clone() }),"),
    ("N9 RunsGivenCode line dropped", EN, "    if has(crate::patterns::RUNS_GIVEN_CODE.words) {", "    if false {"),
    # ---- new: the owner list and its order
    ("O1 owner list before the taint rule", EN, "    if state.link == LinkPhase::ClosedTainted {", "    if state.link == LinkPhase::ClosedTainted && owner_list_allows(action, state).is_none() {"),
    ("O2 owner list beats pause", EN, "    if state.paused {", "    if state.paused && owner_list_allows(action, state).is_none() {"),
    ("O3 owner list beats the bounds", EN, "if let Some(why) = action.oversize {", "if let Some(why) = action.oversize.filter(|_| owner_list_allows(action, state).is_none()) {"),
    ("O4 owner list beats exclusions", EN, "    if a.excluded {", "    if a.excluded && owner_list_allows(action, state).is_none() {"),
    ("O5 owner list beats hard deny", EN, "if let Some(reason) = a.hard_deny {", "if let Some(reason) = a.hard_deny.filter(|_| owner_list_allows(action, state).is_none()) {"),
    ("O6 owner list ignores the shell kind", EN, "tool_ok && oc.shell == shell && same_cwd && exact_text(text, &oc.text)", "tool_ok && same_cwd && exact_text(text, &oc.text)"),
    ("O7 owner list ignores tool_ok (equivalent: shell is derived from the tool)", EN, "tool_ok && oc.shell == shell && same_cwd && exact_text(text, &oc.text)", "oc.shell == shell && same_cwd && exact_text(text, &oc.text)"),
    ("O8 owner list ignores the cwd", EN, "action.cwd.canonical() == Some(oc.cwd.as_path()) && cwd_is_physical(&action.cwd);", "cwd_is_physical(&action.cwd);"),
    ("O9 owner list text trimmed", EN, "        a == b\n", "        a.trim() == b.trim()\n"),
    ("O10 owner list text prefix", EN, "        a == b\n", "        a.starts_with(b)\n"),
    ("O11 owner list Unicode-normalised (NFKC fold)", EN, "        a == b\n", "        crate::glob::fold_name(a) == crate::glob::fold_name(b)\n"),
    ("O12 add_owner_command keeps the raw cwd", ST, "                    cwd: canonical,", "                    cwd: cwd.to_path_buf(),"),
    ("O13 sandbox bypass ignored only for listed (control for the r5 finding)", EN, "    if action.sandbox_disabled {", "    if action.sandbox_disabled && owner_list_allows(action, state).is_none() {"),
    # ---- new: scan bounds
    ("S1 PIECE_CAP = MAX_MENTIONS (word bound never exceeded)", SH, "const PIECE_CAP: usize = crate::action::MAX_MENTIONS + 1;", "const PIECE_CAP: usize = crate::action::MAX_MENTIONS;"),
    ("S2 PIECE_CAP = 10", SH, "const PIECE_CAP: usize = crate::action::MAX_MENTIONS + 1;", "const PIECE_CAP: usize = 10;"),
    ("S3 64 KiB bound x4", AC, "    if text.len() > MAX_EXEC_BYTES {", "    if text.len() > MAX_EXEC_BYTES * 4 {"),
    ("S4 mention component bound dropped", AC, "            || mention_components(scan) > MAX_MENTION_COMPONENTS =>", "            || false =>"),
    ("S5 suffix scan only at '/'", SH, "            if i > 0 && (c == '/' || c == '~') {", "            if i > 0 && c == '/' {"),
    ("S6 attached argument needs 100 bytes", SH, "        if !w.starts_with(\"--\") && body.len() > 1 && body.is_char_boundary(1) {", "        if !w.starts_with(\"--\") && body.len() > 100 && body.is_char_boundary(1) {"),
    ("S7 quotes kept in the word scan", SH, "        .filter(|c| !matches!(c, '\\'' | '\"' | '\\\\'))", "        .filter(|c| !matches!(c, '\\\\'))"),
    ("S8 words not lower-cased", SH, "    let lower = w.to_ascii_lowercase();", "    let lower = w.to_string();"),
    ("S9 PowerShell backtick kept", SH, "        .filter(|c| *c != '`')", "        .filter(|_| true)"),
    ("S10 PowerShell dialect = Bash dialect", AC, "shell_execute(cmd, ShellKind::PowerShell, cwd, env, norm)", "shell_execute(cmd, ShellKind::Bash, cwd, env, norm)"),
    ("S11 nested-quote spans not added", SH, "        out.extend(text.split(q).skip(1).step_by(2).map(String::from));", "        let _ = q;"),
    ("S12 options kept as pieces", SH, "        && !p.starts_with('-')\n", "\n"),
    # ---- new: brace / ANSI-C helpers
    ("Z1 one brace variant only", SH, "const ZIP_VARIANTS: usize = 8;", "const ZIP_VARIANTS: usize = 1;"),
    ("Z2 no brace variants", SH, "const ZIP_VARIANTS: usize = 8;", "const ZIP_VARIANTS: usize = 0;"),
    ("Z3 brace word length bound removed (perf only)", SH, "        || w.len() > crate::path::MAX_PATH_BYTES\n", "\n"),
    ("Z4 always the first alternative", SH, "                    Seg::Group(g) => g[i.min(g.len() - 1)],", "                    Seg::Group(g) => g[0],"),
    ("Z5 groups need two commas", SH, "            Some(k) if after.as_bytes()[k] == b'}' && after[..k].contains(',') => {", "            Some(k) if after.as_bytes()[k] == b'}' && after[..k].matches(',').count() > 1 => {"),
    ("Z6 variants not added as words", SH, "        for z in zip_braces(&w) {\n            add_word(&z, scan);", "        for z in zip_braces(&w) {\n            let _ = add_word;"),
    ("D1 ANSI-C decode trigger never fires", SH, "text.contains(\"$'\")", "text.contains(\"$'\\u{0}\")"),
    ("D2 \\x escape not decoded", SH, "                                .take(2)\n", "                                .take(0)\n"),
    ("D3 octal escape not decoded", SH, "                        d if d.is_digit(8) => {", "                        d if false && d.is_digit(8) => {"),
    ("D4 \\u escape not decoded", SH, "                        'u' | 'U' => {", "                        '\\u{1}' => {"),
]

SKIPS = ["--skip", "p_identity_60k", "--skip", "p_central_shell_property_100k", "--skip", "survey_scan_growth",
         "--skip", "a_monitor_tool_is_a_shell_call", "--skip", "a_owner_list_does_not_cover_sandbox_bypass",
         "--skip", "a_scan_blow_up_inputs_round5"]
FAST = ["--lib"] + sum([["--test", t] for t in ["q01_gate_attacks", "r2_gate_attacks", "t01_table", "t02_property",
        "t03_b16", "t04_paths", "t05_hard_deny", "t06_t3", "t07_exclusions", "t08_binding", "t09_grants", "t10_surface",
        "t11_determinism", "t12_docs", "t13_option_spellings", "t14_gate_return", "t15_addendum3", "t17_addendum5",
        "r5_gate_attacks"]], [])
CARGO = os.path.join(os.environ["CARGO_HOME"], "bin", "cargo")

def cargo_test(env, targets):
    try:
        p = subprocess.run([CARGO, "test", "--manifest-path", f"{REPO}/Cargo.toml", "-p", "coagent-policy", "--offline",
                            "--no-fail-fast"] + targets + ["--"] + SKIPS, capture_output=True, text=True, env=env, timeout=3000)
        return p.stdout + p.stderr, p.returncode
    except subprocess.TimeoutExpired as e:
        out = e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
        return out, "TIMEOUT"

def verdict_of(out, rc):
    failed = sorted(set(re.findall(r"^test (\S+) \.\.\. FAILED", out, re.M)))
    if "error[E" in out or "error: could not compile" in out:
        return "COMPILE-ERROR", failed
    if failed:
        return "caught", failed
    if rc == "TIMEOUT":
        return "TIMEOUT", failed
    if rc != 0:
        return f"rc={rc} no FAILED line", failed
    return "SURVIVED", failed

def run(ids):
    env = dict(os.environ)
    env["CARGO_TARGET_DIR"] = f"{S}/target_{TAG}"
    env["COAGENT_TEST_TMP"] = f"{S}/ci_{TAG}"
    env["CARGO_PROFILE_TEST_OPT_LEVEL"] = "1"
    env["CARGO_PROFILE_DEV_OPT_LEVEL"] = "1"
    os.makedirs(f"{S}/ci_{TAG}", exist_ok=True)
    log = open(f"{S}/logs/mut5_{TAG}.log", "a")
    for (name, f, old, new) in M:
        mid = name.split()[0]
        if ids and mid not in ids:
            continue
        path = f"{REPO}/{f}"
        src = open(path).read()
        n = src.count(old)
        if n != 1:
            line = f"{time.strftime('%H:%M:%S')} {mid} | {name} | ANCHOR COUNT {n} (not applied)"
            print(line, flush=True); log.write(line + "\n"); log.flush(); continue
        open(path, "w").write(src.replace(old, new))
        t = time.time()
        phase = "fast"
        try:
            out, rc = cargo_test(env, FAST)
            v, failed = verdict_of(out, rc)
            if v != "caught" and v != "COMPILE-ERROR":
                phase = "full"
                out, rc = cargo_test(env, [])
                v, failed = verdict_of(out, rc)
        finally:
            open(path, "w").write(src)
        if v == "caught":
            r5only = all(re.match(r"^(a_owner_list_|a_scan_|a_no_panic_fuzz_20k|a_non_shell_spot_checks)", x) for x in failed)
            v = ("caught ONLY by r5: " if r5only else "caught by ") + ", ".join(failed[:6]) + (f" (+{len(failed)-6})" if len(failed) > 6 else "")
        line = f"{time.strftime('%H:%M:%S')} {mid} | {name} | {v} | phase={phase} rc={rc} | {int(time.time()-t)}s"
        print(line, flush=True); log.write(line + "\n"); log.flush()
        if v == "COMPILE-ERROR":
            log.write("\n".join(l for l in out.splitlines() if "error" in l)[:1500] + "\n")
    st = subprocess.run(["git", "-C", REPO, "status", "--porcelain"], capture_output=True, text=True).stdout
    print("git status porcelain:", repr(st)); log.write(f"porcelain: {st!r}\n")

run(sys.argv[1:])
