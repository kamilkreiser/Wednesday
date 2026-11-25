#!/usr/bin/env python3
"""QA-MEASURE-2: every run's command line against the committed rig (T-d, section 4.3, 4.4).
usage: python3 -I -B qm2_cmdcheck.py <spike dir at the head>
For each runs.log line: the raw folder exists with command.txt; the command's env -u list equals m2.sh's UNSET (parsed
from the committed m2.sh); the claude flags are exactly the committed template for its kind (hl / tui_start) plus the
case's extra args; model = claude-haiku-5-5; --permission-mode default once; no skip flag / allowedTools / allow rule.
Also: every settings.json, mcp.json, plugin file, SKILL.md: any permissions/allow/defaultMode key; S1 skill frontmatter."""
import json, os, re, shlex, sys
sys.dont_write_bytecode = True
S = sys.argv[1]; RAW = os.path.join(S, "raw")
m2 = open(os.path.join(S, "m2.sh"), encoding="utf-8").read()
unset = re.search(r"UNSET=\((.*?)\)", m2, re.S).group(1).split()
print("committed UNSET (%d): %s" % (len(unset), " ".join(unset)))
HL = ["timeout", "300", "claude", "-p", "<PROMPT>", "--model", "claude-haiku-5-5", "--output-format", "stream-json", "--verbose",
      "--strict-mcp-config", "--debug-file", "<D>/debug.log", "--settings", "<D>/settings.json", "--permission-mode", "default"]
TUI = ["claude", "--model", "claude-haiku-5-5", "--strict-mcp-config", "--no-chrome", "--debug-file", "<D>/debug.log",
       "--settings", "<D>/settings.json", "--permission-mode", "default"]
EXTRA = {"I1": ["--mcp-config", "<D>/mcp.json"], "T1": ["--mcp-config", "<D>/mcp.json"], "P1": ["--plugin-dir", "<D>/plug dir/m2plug"],
         "S1": [], "W1": []}
for c in ("E1", "E2-start", "E2-mid", "E2-mid-noCC", "E3-r1", "E3-r1-sandbox"): EXTRA[c] = ["--mcp-config", "<D>/mcp.json"]
PROMPTS = {"I1": "Call the tool mcp__m2__probe twice: first with n=1, then with n=2. Then reply DONE.",
           "T1": "Write the exact names of every tool you have whose name begins with mcp__, one per line. Then call each of them once.",
           "P1": "Run the shell command `env | grep -c '^CLAUDE_PLUGIN_'` and reply with its output.",
           "S1": "Use the skill m2probe with the argument XYZ7."}
BAD = re.compile(r"dangerously|skip-permissions|allowedTools|allowed-tools|--allow|bypassPermissions|acceptEdits|dontAsk|--restricted|\bauto\b")
lines = [l for l in open(os.path.join(S, "runs.log"), encoding="utf-8") if l.strip()]
print("runs.log lines: %d" % len(lines))
allok = True
for l in lines:
    f = dict(kv.split("=", 1) for kv in l.split())
    case, kind = f["case"], f["kind"]
    d = os.path.join(RAW, case); ct = os.path.join(d, "command.txt")
    ok = os.path.isdir(d) and os.path.exists(ct) and f["rec"] == "raw/%s/" % case
    txt = open(ct, encoding="utf-8").read().strip()
    toks = shlex.split(txt)
    if toks[:1] == ["cd"]: toks = toks[3:]          # cd <dir> && ...
    assert toks[0] == "env"
    i = 1; us = []
    while toks[i] == "-u": us.append(toks[i + 1]); i += 2
    rest = [t.replace("<SCR>/%s" % case, "<D>") for t in toks[i:]]
    want = (HL if kind == "headless" else TUI) + EXTRA[case]
    if kind == "headless":
        got_prompt = rest[4]; rest = rest[:4] + ["<PROMPT>"] + rest[5:]
        p_ok = got_prompt == PROMPTS[case]
    else:
        p_ok = True
    flags_ok = rest == want
    pm = rest.count("--permission-mode")
    bad = BAD.findall(txt)
    r = ok and us == unset and flags_ok and p_ok and pm == 1 and not bad and f["model"] == "claude-haiku-5-5"
    allok &= r
    print("run=%s %-14s %-11s folder+command.txt=%s env-u==UNSET=%s flags==template=%s prompt==cases=%s perm-mode-count=%d bad-flags=%s model=%s -> %s" % (
        f["run"], case, kind, ok, us == unset, flags_ok, p_ok, pm, bad or 0, f["model"], "OK" if r else "MISMATCH"))
    if not flags_ok: print("   got :", rest); print("   want:", want)
print("ALL RUNS MATCH THE COMMITTED RIG:", allok)
print("\n== settings / mcp / plugin / skill files (keys that could allow or change mode)")
KEYRX = re.compile(r'"(permissions|allow|defaultMode|allowedTools|enabledPlugins|sandbox|model|env)"')
for case in sorted(os.listdir(RAW)):
    for fn in sorted(os.listdir(os.path.join(RAW, case))):
        if fn in ("settings.json", "mcp.json", "cwd.claude.settings.local.json", "cwd.SKILL.md") or fn.startswith("plugin."):
            t = open(os.path.join(RAW, case, fn), encoding="utf-8").read()
            ks = KEYRX.findall(t); at = re.findall(r"allowed-tools:.*", t)
            print("%s/%s: keys %s %s" % (case, fn, sorted(set(ks)) or "-", at or ""))
