#!/usr/bin/env python3
"""QA-AUDIT-WIRE task 4: a gate decision is not recorded. a: --audit --gate --workspace <ws>.
Usage: python3 -B qa_gate.py <bin dir> <work dir (new)>"""
import hashlib, json, os, sys, time, uuid
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import qa_causes as C  # noqa: E402

BIN, ROOT = sys.argv[1], sys.argv[2]
os.makedirs(ROOT, exist_ok=True)
ws = os.path.join(ROOT, "ws")
os.makedirs(ws)
open(os.path.join(ws, "a.rs"), "w").write("fn main() {}\n")


def snap(d):
    out = {}
    for r, ds, fs in os.walk(d):
        for f in fs:
            p = os.path.join(r, f)
            out[os.path.relpath(p, d)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return out


def ev(tool, inp):
    s = str(uuid.uuid4())
    return {"session_id": s, "transcript_path": os.path.join(ws, s + ".jsonl"), "cwd": ws, "prompt_id": str(uuid.uuid4()),
            "permission_mode": "default", "effort": {"level": "medium"}, "hook_event_name": "PreToolUse",
            "tool_name": tool, "tool_input": inp, "tool_use_id": "toolu_" + "ab" * 12}


s = C.S("gate", a_extra=("--audit", "--gate", "--workspace", ws))
try:
    s.send("a", "QAW gate scenario first send")
    d = s.adir()
    before = snap(d)
    a0 = s.audit()
    r1 = s.q.ctl("a", "gate", {"event": ev("Glob", {"pattern": "*.rs", "path": ws})})
    r2 = s.q.ctl("a", "gate", {"event": ev("Read", {"file_path": os.path.join(ws, "a.rs")})})
    time.sleep(0.5)
    after = snap(d)
    act = s.q.ctl("a", "activity", {"after": 0})
    print(json.dumps({"gate1": r1, "gate2": r2, "audit_before": a0, "audit_after": s.audit(),
                      "folder_unchanged": before == after, "files": sorted(after),
                      "activity_lines": len((act.get("result") or {}).get("lines", act.get("result", {}).get("items", []))),
                      "activity": act}, sort_keys=True))
finally:
    print("left", s.close())
