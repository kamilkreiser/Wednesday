#!/usr/bin/env python3
"""QA-MEASURE-2 4.7: hand-made inputs for idmatch.py and hook_stub.py (no model). usage: python3 -I -B qm2_rehearse.py <spike dir> <work dir>"""
import hashlib, json, os, subprocess, sys
sys.dont_write_bytecode = True
S, W = sys.argv[1], sys.argv[2]
SID = "11111111-2222-4333-8444-555555555555"; T1, T2 = "toolu_01QAPLANTAAAAAAAAA1", "toolu_01QAPLANTBBBBBBBBB2"
def case(name, planted):
    d = os.path.join(W, "idm", name); os.makedirs(os.path.join(d, "hook"), exist_ok=True); os.makedirs(os.path.join(d, "mcp"), exist_ok=True)
    with open(os.path.join(d, "hook", "stdin.jsonl"), "w") as f:
        for n, t in ((1, T1), (2, T2)):
            f.write(json.dumps({"pid": 10, "ppid": 9, "proc_cwd": d, "chain": [[9, "claude"], [1, "launchd"]], "env_names": [],
                "event": {"hook_event_name": "PreToolUse", "tool_name": "mcp__m2__probe", "tool_input": {"n": n}, "tool_use_id": t,
                          "session_id": SID, "cwd": d, "mcp_server": {"name": "m2", "source": "dynamic"}}}) + "\n")
    with open(os.path.join(d, "mcp", "mcp.log"), "w") as f:
        for i, (n, t) in enumerate(((1, T1), (2, T2))):
            p = {"name": "probe", "arguments": {"n": n}}
            if planted: p["_meta"] = {"claudecode/toolUseId": t, "qa/session": SID}
            m = {"jsonrpc": "2.0", "id": i + 2, "method": "tools/call", "params": p}
            f.write(json.dumps({"ts": 1.0 + i, "dir": "in", "raw": json.dumps(m), "msg": m}) + "\n")
    env = {"QA_SESSION": hashlib.sha256(SID.encode()).hexdigest() if planted else hashlib.sha256(b"other").hexdigest()}
    json.dump(env, open(os.path.join(d, "mcp", "mcp.env.sha256"), "w"))
    json.dump({"pid": 11, "ppid": 9, "chain": [[9, "claude"]]}, open(os.path.join(d, "mcp", "mcp.ppid"), "w"))
    out = subprocess.run(["python3", "-I", "-B", os.path.join(S, "idmatch.py"), d], capture_output=True, text=True).stdout
    print("### idmatch.py, hand-made pair %s" % name)
    print("\n".join(l for l in out.splitlines() if l.startswith(("validity", "(a)", "(b)", "    nearest", "(e)"))).replace(SID, "<SID>").replace(T1, "<T1>").replace(T2, "<T2>"))
case("WITH-ids", True); case("WITHOUT-ids", False)
print("### hook_stub.py fed hand-made inputs (logged line read back)")
hd = os.path.join(W, "stubhd"); os.makedirs(hd, exist_ok=True)
open(os.path.join(hd, "out.PreToolUse.json"), "w").write('{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"allow","permissionDecisionReason":"allowed by the owner"}}\n')
open(os.path.join(hd, "out.ConfigChange.json"), "w").write('{"decision":"block","reason":"coagent blocks: settings change (MEASURE-2 stub)"}\n')
ins = [{"hook_event_name": "PreToolUse", "tool_name": "mcp__m2__probe", "mcp_server": {"name": "m2", "source": "dynamic"}},
       {"hook_event_name": "PreToolUse", "tool_name": "mcp__m2__n|pipe"}, {"hook_event_name": "PreToolUse", "tool_name": "mcp__m2__n_é"},
       {"hook_event_name": "PreToolUse", "tool_name": "Bash", "tool_input": {"command": "echo S1-MARK XYZ7"}},
       {"hook_event_name": "ConfigChange", "source": "local_settings", "file_path": "/x/.claude/settings.local.json"}]
for e in ins:
    raw = json.dumps(e, ensure_ascii=False).encode("utf-8")
    p = subprocess.run(["python3", "-B", os.path.join(S, "hook_stub.py"), hd], input=raw, capture_output=True)
    rec = json.loads(open(os.path.join(hd, "stdin.jsonl"), encoding="utf-8").read().splitlines()[-1])
    tn = e.get("tool_name")
    print("in %-16s rc=%d logged_event==input:%s mcp_server kept:%s S1-MARK kept:%s hex==bytes typed:%s printed:%s" % (
        tn or e["hook_event_name"], p.returncode, rec["event"] == e, "mcp_server" in rec["event"], "S1-MARK" in json.dumps(rec["event"]),
        (rec["tool_name_hex"] == tn.encode().hex()) if tn else "n/a", p.stdout.decode().strip()[:60]))
