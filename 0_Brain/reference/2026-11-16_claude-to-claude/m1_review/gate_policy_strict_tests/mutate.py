#!/usr/bin/env python3
"""QA gate mutation driver (POLICY-STRICT). Usage: mutate.py <tree> <logdir> [ids...]
For each mutant: apply ONE textual edit to <tree>/crates/coagent-policy/src/<file> (asserting the old text occurs
exactly once), run the branch's OWN crate tests (cargo stops at the first failing test binary), then the QA tests
(qa_strict, r6_gate), restore the file, and print one line per mutant. The toolchain env must already be exported."""
import subprocess, sys, os, time

tree, logdir = sys.argv[1], sys.argv[2]
only = set(sys.argv[3:])
SRC = os.path.join(tree, "crates/coagent-policy/src")

M = [
 ("M01", "engine.rs", "strict raise T3 lowered to T2",
  "            a.raise(Tier::T3, s.reason());", "            a.raise(Tier::T2, s.reason());"),
 ("M02", "action.rs", "mcp__ (service) arm excused from the not-taught check",
  "} else if known_tool(&input.tool_name).is_none() && !red_default_allow {",
  "} else if known_tool(&input.tool_name).is_none() && !red_default_allow && kind != Kind::Service {"),
 ("M03", "known.rs", "list entry matched by prefix",
  "KNOWN_TOOLS.iter().find(|t| t.name == name)", "KNOWN_TOOLS.iter().find(|t| name.starts_with(t.name))"),
 ("M04", "known.rs", "list entry matched case-insensitively",
  "KNOWN_TOOLS.iter().find(|t| t.name == name)", "KNOWN_TOOLS.iter().find(|t| t.name.eq_ignore_ascii_case(name))"),
 ("M05", "known.rs", "list entry matched after trimming whitespace",
  "KNOWN_TOOLS.iter().find(|t| t.name == name)", "KNOWN_TOOLS.iter().find(|t| t.name == name.trim())"),
 ("M06", "known.rs", "isolation 'worktree' matched case-insensitively / trimmed",
  'Some(Value::String(s)) if s == "worktree" => SubagentPlace::Local,',
  'Some(Value::String(s)) if s.trim().eq_ignore_ascii_case("worktree") => SubagentPlace::Local,'),
 ("M07", "known.rs", "name check after isolation (worktree + name read local)",
  '    if obj.contains_key("name") {\n        return SubagentPlace::PossibleTeammate;\n    }\n    match obj.get("isolation") {\n        None => ABSENT_ISOLATION,\n        Some(Value::String(s)) if s == "worktree" => SubagentPlace::Local,',
  '    match obj.get("isolation") {\n        Some(Value::String(s)) if s == "worktree" => SubagentPlace::Local,\n        _ if obj.contains_key("name") => SubagentPlace::PossibleTeammate,\n        None => ABSENT_ISOLATION,'),
 ("M08", "known.rs", "isolation null read as absent (local)",
  "        None => ABSENT_ISOLATION,", "        None | Some(Value::Null) => ABSENT_ISOLATION,"),
 ("M09", "action.rs", "ExitWorktree demoted to the ordinary T2 card",
  '        "ExitWorktree" => {\n            arm_strict = Some(Strict::WorktreeRemoval);',
  '        "ExitWorktree" => {\n            red_default_allow = true;'),
 ("M10", "action.rs", "remote subagent demoted (Remote => not strict)",
  "                SubagentPlace::Remote => Some(Strict::RemoteSubagent),", "                SubagentPlace::Remote => None,"),
 ("M11", "action.rs", "choke: the Execute branch removed (a taught tool with a command gets strict None)",
  "    let strict = if kind == Kind::Execute {\n        Some(arm_strict.unwrap_or(Strict::Shell))\n    } else if arm_strict.is_some() {",
  "    let strict = if arm_strict.is_some() {"),
 ("M12", "engine.rs", "UnknownTool back to the END of the reason order (not first on the card)",
  "    ShellExpansion,\n    /// A tool the gate has not been taught (no entry in [`crate::known::KNOWN_TOOLS`]): strict (POLICY-STRICT).\n    /// Placed here so that it is the first reason on such a card.\n    UnknownTool,\n",
  "    ShellExpansion,\n", [("    CredentialFolder(&'static str),\n}", "    CredentialFolder(&'static str),\n    UnknownTool,\n}")]),
 ("M13", "known.rs", "absent isolation ruled remote (stricter; tests the ruling's own tests)",
  "pub const ABSENT_ISOLATION: SubagentPlace = SubagentPlace::Local;", "pub const ABSENT_ISOLATION: SubagentPlace = SubagentPlace::Remote;"),
 ("M14", "known.rs", "every own-prefix name taught (prefix of our MCP tools)",
  "    KNOWN_TOOLS.iter().find(|t| t.name == name)\n}",
  "    if name.starts_with(\"mcp__plugin_coagent_link__\") { return KNOWN_TOOLS.iter().find(|t| t.name == \"mcp__plugin_coagent_link__share\"); }\n    KNOWN_TOOLS.iter().find(|t| t.name == name)\n}"),
 ("M15", "known.rs", "a non-object subagent input read as local",
  "    let Some(obj) = input.as_object() else {\n        return SubagentPlace::Remote;\n    };",
  "    let Some(obj) = input.as_object() else {\n        return SubagentPlace::Local;\n    };"),
 ("M16", "engine.rs", "strict ignored for kind other (catch-all back to T2 in the engine)",
  "    if let Some(s) = action.strict {", "    if let Some(s) = action.strict.filter(|_| action.kind != Kind::Other) {"),
 ("M17", "known.rs", "a wrong list entry: SendMessage taught at T2",
  '    KnownTool { name: "CronList",',
  '    KnownTool { name: "SendMessage", kind: Kind::Other, lowest: Tier::T2, reason: "x", read_on: ON, host: DOCS },\n    KnownTool { name: "CronList",'),
 ("M18", "known.rs", "isolation 'remote' only is remote; any other string local",
  "        Some(_) => SubagentPlace::Remote,",
  "        Some(Value::String(s)) if s != \"remote\" => SubagentPlace::Local,\n        Some(_) => SubagentPlace::Remote,"),
]

T_FILES = ["t19_strict","t18_addendum7","t01_table","t12_docs","t02_property","t03_b16","t04_paths","t05_hard_deny","t06_t3","t07_exclusions","t08_binding","t09_grants","t10_surface","t11_determinism","t13_option_spellings","t14_gate_return","t15_addendum3","t17_addendum5"]
G_FILES = ["q01_gate_attacks","r2_gate_attacks","r3_gate_attacks","r4_gate_attacks","r5b_bound_probe","r5b_r4_regressions","r5b_shell_t3"]
OWN = ["cargo", "test", "-p", "coagent-policy", "--offline", "--lib"] + sum([["--test", t] for t in T_FILES], [])
OWN_G = ["cargo", "test", "-p", "coagent-policy", "--offline"] + sum([["--test", t] for t in G_FILES], [])
QA = ["cargo", "test", "-p", "coagent-policy", "--offline", "--test", "qa_strict", "--", "--skip", "qa_untaught"]
QA2 = ["cargo", "test", "-p", "coagent-policy", "--offline", "--test", "qa_strict", "--test", "r6_gate", "--no-fail-fast"]

def run(cmd, log):
    t = time.time()
    with open(log, "w") as f:
        p = subprocess.run(cmd, cwd=tree, stdout=f, stderr=subprocess.STDOUT)
    out = open(log).read()
    failed = p.returncode != 0 and "test result: FAILED" in out
    compile_err = p.returncode != 0 and not failed
    first = ""
    for line in out.splitlines():
        if line.startswith("---- "):
            first = line[5:].split(" stdout")[0]; break
    return failed, compile_err, first, int(time.time() - t)

for m in M:
    mid, fn, what, old, new = m[:5]
    extra = m[5] if len(m) > 5 else []
    if only and mid not in only:
        continue
    path = os.path.join(SRC, fn)
    orig = open(path).read()
    if orig.count(old) != 1:
        print(f"{mid} SKIP old text occurs {orig.count(old)} times", flush=True); continue
    mutated = orig.replace(old, new)
    for o2, n2 in extra:
        assert mutated.count(o2) == 1, (mid, o2)
        mutated = mutated.replace(o2, n2)
    open(path, "w").write(mutated)
    try:
        o = run(OWN, os.path.join(logdir, f"{mid}_own.log"))
        if not o[0] and not o[1]:
            o = run(OWN_G, os.path.join(logdir, f"{mid}_own_gate.log"))
        q = run(QA, os.path.join(logdir, f"{mid}_qa.log"))
        if not q[0] and not q[1]:
            q = run(QA2, os.path.join(logdir, f"{mid}_qa2.log"))
    finally:
        open(path, "w").write(orig)
    def s(r): return "COMPILE-ERROR" if r[1] else ("KILLED by " + r[2] if r[0] else "survived")
    print(f"{mid}\t{what}\tOWN: {s(o)} ({o[3]}s)\tQA: {s(q)} ({q[3]}s)", flush=True)
