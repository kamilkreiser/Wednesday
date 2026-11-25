#!/usr/bin/env python3
"""QA-MEASURE-2 section 4.4: the fixed files and typed prompts of every run against the text run.sh writes AT THE HEAD.
usage: python3 -I -B qm2_rigdiff.py <spike dir at the head>
Rebuilds answer.py, writer.py, inject.sh (r1), SKILL.md, the E2 local settings, I1's CLAUDE.md and the P1 plugin layout
from run.sh's own heredocs/strings (bash substitutions done by hand, as bash would), then byte-compares them with each
committed raw/<case>/cwd.* copy. Then every SAY line in keys.log against run.sh's prompt strings, and the E3 SAY line
against rehearsal.txt's (socket name masked)."""
import json, os, re, sys
sys.dont_write_bytecode = True
S = sys.argv[1]; RAW = os.path.join(S, "raw")
run = open(os.path.join(S, "run.sh"), encoding="utf-8").read()
def heredoc(after, tag):
    i = run.index(after); j = run.index("\n", run.index("<<", i)) + 1; k = run.index("\n" + tag + "\n", j)
    return run[j:k + 1]
LOCAL = re.search(r"^LOCAL_SETTINGS='(.*)'$", run, re.M).group(1)
answer = heredoc("put_answer() {", "PY")
writer = heredoc("put_writer() {", "PY").replace("$LOCAL_SETTINGS", LOCAL).replace("\\\\n", "\\n")
hdr = heredoc("put_inject() {", "SH2").replace("\\$", "\x00").replace("$1", "r1").replace("\x00", "$")
r1 = heredoc("    r1) cat >> \"$D/cwd/inject.sh\" <<'SH2'", "SH2")
inject = hdr + r1 + 'echo "$(ts) INJECT_DONE" >> $L\n'
skill = heredoc("put_skill() {", "MD")
claude_md = "# Scratch project\n\nMarker for the memory check: M2MEMO. Nothing else here.\n"
want = {"cwd.answer.py": answer, "cwd.writer.py": writer, "cwd.inject.sh": inject, "cwd.SKILL.md": skill,
        "cwd.claude.settings.local.json": LOCAL + "\n", "cwd.CLAUDE.md": claude_md}
n = bad = 0
for case in sorted(os.listdir(RAW)):
    for fn, w in want.items():
        p = os.path.join(RAW, case, fn)
        if os.path.exists(p):
            got = open(p, encoding="utf-8").read(); n += 1
            ok = got == w; bad += not ok
            print("%-14s %-32s %s" % (case, fn, "IDENTICAL to run.sh's text" if ok else "DIFFERS"))
            if not ok:
                import difflib; print("".join(difflib.unified_diff(w.splitlines(True), got.splitlines(True), "run.sh", fn))[:1500])
# P1 plugin files: rebuild the JSON as p1_plugin() does, with <SCR> paths, compare parsed
P = "<SCR>/P1/plug dir/m2plug"; hd = "<SCR>/P1/hook"; md = "<SCR>/P1/mcp"; stub = P + "/hook_stub.py"
hooks = {"description": "MEASURE-2 P1: PreToolUse registered twice, exec form and shell form; both stubs answer allow.",
         "hooks": {"PreToolUse": [{"matcher": "*", "hooks": [{"type": "command", "command": "python3", "args": ["-B", stub, hd, "exec"], "timeout": 30, "onFailure": "block"}]},
                                  {"matcher": "*", "hooks": [{"type": "command", "command": "python3 -B '%s' '%s' shell" % (stub, hd), "timeout": 30, "onFailure": "block"}]}]}}
mcp = {"mcpServers": {"m2": {"command": P + "/stub_mcp_m2.py", "args": [], "env": {"M2_LOG": md + "/mcp.log", "M2_DIR": md, "M2_TOOLS": "probe"}}}}
for fn, w in (("plugin.hooks_hooks.json", hooks), ("plugin..mcp.json", mcp)):
    got = json.load(open(os.path.join(RAW, "P1", fn))); n += 1; ok = got == w; bad += not ok
    print("%-14s %-32s %s" % ("P1", fn, "IDENTICAL (parsed) to p1_plugin()'s object" if ok else "DIFFERS: %s" % json.dumps(got)[:300]))
print("fixed files compared: %d ; differing: %d" % (n, bad))
# typed prompts
P_ = {k: re.search(r"^%s='(.*)'$" % k, run, re.M).group(1) for k in ("CONFIRM_P", "MID_P", "W1W_P", "W1B_P")}
E3T = re.search(r'say "(First start the shell command .*?)"\n', run).group(1).replace("\\`", "`")
exp = {"E1": [P_["CONFIRM_P"]], "E2-start": [P_["CONFIRM_P"]], "E2-mid": [P_["MID_P"]], "E2-mid-noCC": [P_["MID_P"]],
       "E3-r1": [E3T], "E3-r1-sandbox": [E3T], "W1": [P_["W1W_P"], P_["W1B_P"]]}
reh = open(os.path.join(S, "rehearsal.txt"), encoding="utf-8").read()
reh_e3 = re.search(r"\d+\.\d+ SAY (First start.*)", reh).group(1)
for case, ps in exp.items():
    says = [l.split(" SAY ", 1)[1].rstrip("\n") for l in open(os.path.join(RAW, case, "keys.log"), encoding="utf-8") if " SAY " in l]
    tgt = open(os.path.join(RAW, case, "inject.target.txt")).read().strip() if case.startswith("E3") else None
    want_says = [p.replace("$target", tgt) if tgt else p for p in ps]
    ok = says == want_says; bad += not ok
    extra = ""
    if case.startswith("E3"):
        mask = lambda s: re.sub(r"tmux-\d+/m2-[a-z0-9]+", "tmux-N/m2-X", s)
        extra = " ; equals rehearsal.txt's E3 SAY line (socket name masked): %s" % (mask(says[0]) == mask(reh_e3))
    print("%-14s SAY lines %d, equal to run.sh's prompt text: %s%s" % (case, len(says), ok, extra))
print("TOTAL differing items:", bad)
