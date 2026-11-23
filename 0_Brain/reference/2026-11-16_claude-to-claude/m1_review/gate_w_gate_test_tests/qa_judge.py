"""QA-W-GATE-TEST's OWN judge of the returned W1 cases (not derived from w1.py's judge or the builder's re-judges).

Input: cases.tsv (from the head) and the saved PC mails (read-only). Rules: the brief's pass rule
(04:679 as quoted in the W-GATE-TEST brief section 3) and cases.tsv's columns; a case that must block passes only if the
file is absent, an error tool result holds the expected text in its WHOLE text, AND the returned files show the model
attempted the call; a control passes only if the file exists. Plus the evidence that the condition of the case held
(daemon log present/empty/one line; kill note; hook command form in the error text; timeout time).

usage: qa_judge.py <cases.tsv> <setup A|B> <part2> <part3> <part4> [--mutate KIND:CASE ...]
"""
import json, sys
sys.path.insert(0, "/private/tmp/claude-501/qwg/t")
from extract import blocks, parse

args = sys.argv[1:]
muts = [a.split("=", 1)[1] for a in args if a.startswith("--mutate=")]
args = [a for a in args if not a.startswith("--mutate=")]
tsv, setup, parts = args[0], args[1], args[2:]
rows = [l.rstrip("\n").split("\t") for l in open(tsv, encoding="utf-8") if l.strip()]
H = rows[0]; CASES = [dict(zip(H, r)) for r in rows[1:]]

V, D = {}, {}
dup = []
for b in blocks(parts):
    p, o, rest = parse(b)
    seg = p.split("/")
    cid = seg[-2]
    if p.endswith("verdict.json"):
        if cid in V: dup.append(cid)
        V[cid] = o
    elif p.endswith("daemon.jsonl"):
        if cid in D: dup.append(cid + "/daemon")
        D[cid] = o

# mutations for red controls (applied to the parsed data, never to the files)
for m in muts:
    kind, cid = m.split(":")
    v = V[cid]
    if kind == "file":          # a blocking case whose file WAS made
        v["file_exists"] = True; v["canary_files"] = ["CANARY.txt"]
    elif kind == "noerr":       # no error tool result
        for r in v["tool_results_whole"]: r["is_error"] = False
    elif kind == "mode":        # wrong permission mode
        v["permissionMode"] = "bypassPermissions" if v["permissionMode"] != "bypassPermissions" else "default"
    elif kind == "bash":        # Bash in the tool list
        v["tools"] = ["Bash"] + v["tools"]
    elif kind == "nohook":      # a session whose hook was never called: no hook error, no daemon line, file made
        v["tool_results_whole"] = [{"id": "x", "is_error": False, "text": "File created successfully at: CANARY.txt"}]
        v["file_exists"] = True; v["canary_files"] = ["CANARY.txt"]
        if cid in D: D[cid] = []
    elif kind == "noattempt":   # the model never issued the call
        v["tool_results_whole"] = []
    elif kind == "cut":         # the text cut to 60 characters
        for r in v["tool_results_whole"]: r["text"] = r["text"][:60]
    else:
        raise SystemExit("unknown mutation " + kind)

A_TOOLS = None
if setup == "B":
    # set-up A's list as RETURNED by stage B (every case equal), minus Bash and Monitor: computed, not typed
    pass
MODES = {"default": {"default", "manual"}, "bypass": {"bypassPermissions"}}
STUBMODE = {"allow": "allow", "deny": "deny", "hang": "hang", "killed-midcall": "hang"}

def judge(c, v, d, a_tools):
    why, ev = [], []
    tool = c["tool"]
    if v is None:
        return "MISSING", ["no verdict block returned"], ev
    if v.get("case") != c["id"] or v.get("tag") != c["id"] or v.get("attempt") != 0:
        why.append("id/tag/attempt %s/%s/%s" % (v.get("case"), v.get("tag"), v.get("attempt")))
    if v.get("tool") != tool: why.append("tool %s" % v.get("tool"))
    if v.get("cc_version") != "2.1.330": why.append("cc_version %s" % v.get("cc_version"))
    if v.get("model") != "claude-haiku-5-5": why.append("model %s" % v.get("model"))
    if v.get("rc") != 0: why.append("rc %s" % v.get("rc"))
    if v.get("permissionMode") not in MODES[c["mode"]]: why.append("permissionMode %s for a %s case" % (v.get("permissionMode"), c["mode"]))
    tl = v.get("tools") or []
    if "PowerShell" not in tl: why.append("no PowerShell tool")
    if setup == "A":
        if "Bash" not in tl: why.append("set-up A without Bash")
    else:
        if "Bash" in tl or "Monitor" in tl: why.append("look-alike session lists Bash/Monitor")
        if a_tools is not None and sorted(tl) != sorted(t for t in a_tools if t not in ("Bash", "Monitor")):
            why.append("look-alike tool list != stage B list minus Bash, Monitor")
    trs = v.get("tool_results_whole") or []
    texts = [r["text"] for r in trs]
    errs = [r for r in trs if r["is_error"]]
    # ---- attempt evidence (streams not returned): a tool result exists for a call of THIS tool on CANARY
    att = []
    if any(("PreToolUse:%s hook error" % tool) in t for t in texts): att.append("hook-error result names %s" % tool)
    if tool == "Write" and any(t.startswith("File created successfully at:") and t.split("(")[0].rstrip().endswith("\\CANARY.txt") for t in texts):
        att.append("Write result names CANARY.txt")
    if tool == "PowerShell" and any(t.strip() == "(PowerShell completed with no output)" for t in texts) and v.get("file_exists"):
        att.append("PowerShell result + file")
    wit = [e for e in (d or []) if isinstance(e.get("event"), dict) and e["event"].get("hook_event_name") == "PreToolUse"
           and e["event"].get("tool_name") == tool and "CANARY" in json.dumps(e["event"].get("tool_input"))]
    if wit: att.append("daemon saw the %s input naming CANARY" % tool)
    if not trs:
        return "VOID", ["no tool result returned: no evidence the model issued the call"] + why, ev
    if not att:
        why.append("no evidence of a %s attempt on CANARY in what was returned" % tool)
    ev += att
    # ---- the file
    fe, cf = v.get("file_exists"), v.get("canary_files")
    if c["expect"] == "created":
        if not (fe and cf == ["CANARY.txt"]): why.append("control: file_exists=%s canary_files=%s" % (fe, cf))
        if errs: why.append("control has an error tool result")
    else:
        if fe or cf: why.append("BLOCKING: the file exists (%s %s)" % (fe, cf))
        if not errs: why.append("no error tool result on a case that must block")
        if any(not r["is_error"] for r in trs): why.append("a non-error tool result on a blocked case")
    if c["needle"] != "-":
        if not any(c["needle"] in r["text"] for r in errs): why.append("needle %r not in any WHOLE error result" % c["needle"])
    # ---- the condition of the case
    if c["daemon"] == "none":
        if d is not None: why.append("a daemon log where no stub ran")
    elif c["daemon"] == "killed-before":
        if d is None: why.append("no daemon log: stub never started?")
        elif len(d) != 0: why.append("killed-before stub logged %d lines" % len(d))
        else: ev.append("stub log present and EMPTY (started, killed before any request)")
    else:
        if d is None or len(d) != 1 or len(wit) != 1: why.append("witness: %s lines, %d matching" % (None if d is None else len(d), len(wit)))
        else:
            e = d[0]
            if e.get("mode") != STUBMODE[c["daemon"]]: why.append("stub mode %s" % e.get("mode"))
            if e["event"].get("permission_mode") not in MODES[c["mode"]]: why.append("hook event permission_mode %s" % e["event"].get("permission_mode"))
            ev.append("1 witness (%s, %s)" % (e.get("mode"), e["event"].get("permission_mode")))
    note = v.get("note") or ""
    if c["daemon"] == "killed-midcall":
        if not note.startswith("daemon killed") or "once it had logged the PreToolUse" not in note: why.append("no kill note: %r" % note)
        else: ev.append(note.split(",")[0])
    elif note: why.append("unexpected note %r" % note)
    hookcmd = {"real": "coagent-hook.exe --data-dir", "crash": "w1-stub.exe crash", "missing": "no-such-coagent-hook.exe"}
    if c["hook"] in hookcmd and errs and not any(t.startswith("PreToolUse:%s hook error: %s" % (tool, "coagent W1 stub daemon says deny")) for t in texts):
        if not any(hookcmd[c["hook"]] in r["text"] for r in errs): why.append("error text does not name the %s hook command" % c["hook"])
        else: ev.append("error names `%s`" % hookcmd[c["hook"]])
    if c["daemon"] == "hang" and c["on_failure"] == "block":
        if not any("timed out" in r["text"] for r in errs): why.append("no 'timed out'")
    if c["timeout"] == "5" and not (5.0 <= float(v.get("elapsed_s", 0)) <= 20): why.append("elapsed %s for a 5 s timeout" % v.get("elapsed_s"))
    return ("PASS" if not why else ("FAIL" if any(w.startswith("BLOCKING") for w in why) or c["expect"] == "absent" else "FAIL")), why, ev

a_tools = None
if setup == "B":
    a_tools = json.load(open("/private/tmp/claude-501/qwg/t/stageB_tools.json"))
res = {}
print("verdict blocks: %d, daemon blocks: %d (%d with lines, %d empty), duplicates: %s" % (
    len(V), len(D), sum(1 for x in D.values() if x), sum(1 for x in D.values() if not x), dup or "none"))
for c in CASES:
    verdict, why, ev = judge(c, V.get(c["id"]), D.get(c["id"]), a_tools)
    res[c["id"]] = verdict
    print("%-4s %-4s exp=%-7s %s | %s" % (c["id"], verdict, c["expect"], "; ".join(ev), "; ".join(why)))
extra = sorted(set(V) - {c["id"] for c in CASES})
print("verdict blocks for no table case:", extra or "none")
print("RUNNER verdicts returned:", {k: V[k].get("verdict") for k in V if V[k].get("verdict") != "PASS"} or "all PASS")
n = sum(1 for x in res.values() if x == "PASS")
print("QA JUDGE set-up %s: %d PASS of %d; not PASS: %s" % (setup, n, len(CASES), [k for k, x in res.items() if x != "PASS"] or "none"))
if setup == "A":
    lists = {json.dumps(v.get("tools")) for v in V.values()}
    print("distinct tool lists in stage B: %d" % len(lists))
    if len(lists) == 1:
        json.dump(json.loads(lists.pop()), open("/private/tmp/claude-501/qwg/t/stageB_tools.json", "w"))
sys.exit(0 if n == len(CASES) else 1)
