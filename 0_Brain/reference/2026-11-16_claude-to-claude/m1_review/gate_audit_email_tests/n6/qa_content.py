#!/usr/bin/env python3
"""QA-AUDIT-WIRE task 4: what is recorded. Head; convener `a` --audit, joiner `b`. Every planted value
below is MADE UP. Usage: python3 -B qa_content.py <bin dir> <work dir (new)> <inspect runner>
The inspect runner is a shell command prefix that runs the qa_inspect test with QA_* env set."""
import json, os, shutil, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import qa_causes as C  # noqa: E402

BIN, ROOT, RUNNER = sys.argv[1], sys.argv[2], sys.argv[3]
S, emit = C.S, C.emit

# made-up secret-shaped values (none is real)
PLANT = {
    "api_key": "sk-ant-api03-QAWfakeFAKEfake0123456789abcdefQAWfakeFAKEfake",
    "bearer": "Bearer qawFAKEtoken0123456789abcdefABCDEF.qaw",
    "password": "password=QawFakePassw0rd!77",
    "pem": "-----BEGIN OPENSSH PRIVATE KEY-----",
    "hex": "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
    "jwt": "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJxYXctZmFrZSJ9.qawFAKEsigFAKEsig0123456789",
    "urlpw": "https://qawuser:QawUrlPassFake9@example.invalid/path",
    "cloudkey": "AKIAQAWFAKE0123QAWX",
    "email": "qaw.fake.person@example.invalid",
}
DROPPED = "QAW-DROPPED-LINE-7c1e unique raw line the preview must not keep"
LINES = [
    f"line one: key {PLANT['api_key']} auth {PLANT['bearer']}",
    f"line two: {PLANT['password']} {PLANT['pem']} {PLANT['hex']}",
    f"line three: {PLANT['jwt']} {PLANT['urlpw']} {PLANT['cloudkey']} {PLANT['email']}",
    DROPPED,
    "line five: more text " + "x" * 80,
    "line six: the end",
]
LONG = "\n".join(LINES)
assert len(LONG) > 240 and LONG.count("\n") >= 3
SHORT_EACH = {k: f"QAW short {k}: {v} end" for k, v in PLANT.items()}  # each value alone, one line


def grep_tree(root, needles):
    hits = {n: [] for n in needles}
    for r, ds, fs in os.walk(root):
        for f in fs:
            p = os.path.join(r, f)
            try:
                b = open(p, "rb").read()
            except Exception:
                continue
            for n in needles:
                if n.encode() in b:
                    hits[n].append(os.path.relpath(p, root))
    return hits


def main():
    os.makedirs(ROOT, exist_ok=True)
    s = S("content")
    statuses = []
    try:
        q = s.q
        r_long = s.send("a", LONG)
        statuses.append(q.ctl("a", "status"))
        r_shorts = {k: s.send("a", t).get("ok") for k, t in SHORT_EACH.items()}
        r_req = s.send("a", "QAW a request from a", kind="request")
        # b sends a request and a chat with a peer marker
        PEERMARK = "QAW-PEER-MARK-5d2b only the peer wrote this"
        rb_req = s.send("b", "QAW-PEER-REQ-91aa please answer", kind="request")
        rb_chat = s.send("b", PEERMARK)
        time.sleep(1.5)
        inbox = q.ctl("a", "inbox_read")["result"]["messages"]
        peer_req = [m for m in inbox if m.get("type") == "request.new"][0]
        req_id = (peer_req.get("request_id") or peer_req.get("id"))
        statuses.append(q.ctl("a", "status"))
        a_before = s.audit()
        r_reply_peer = s.send("a", "QAW reply to the peer's request", kind="reply", re=req_id)
        a1 = s.audit()
        r_reply_none = s.send("a", "QAW reply naming nothing", kind="reply", re="zzzzQAWnothing0000")
        a2 = s.audit()
        own_id = r_req.get("result", {}).get("id")
        r_reply_own = s.send("a", "QAW reply naming my own request", kind="reply", re=own_id)
        a3 = s.audit()
        statuses.append(q.ctl("a", "status"))
        sid = os.path.basename(s.adir())
        q.stop("a")
        # copy (never touch the live folder) and inspect
        cp = os.path.join(ROOT, "copyA")
        shutil.copytree(q.dir("a"), cp, symlinks=True, ignore=shutil.ignore_patterns("*.sock", "*.lock", "ipc"))
        os.chmod(cp, 0o700)
        texts = os.path.join(ROOT, "texts.json")
        tl = [LONG] + list(SHORT_EACH.values())
        json.dump(tl, open(texts, "w"))
        outp = os.path.join(ROOT, "inspect.json")
        env = dict(os.environ, QA_DATA=cp, QA_SID=sid, QA_OUT=outp, QA_TEXTS=texts)
        rr = subprocess.run(RUNNER, shell=True, env=env, capture_output=True, text=True)
        ins = json.load(open(outp))
        fulls = [e["full"] for e in ins["events"]]
        long_prev = ins["previews"][0]
        emit({"part": "sends", "long_ok": r_long.get("ok"), "shorts_ok": r_shorts, "req_ok": r_req.get("ok"),
              "peer_req_ok": rb_req.get("ok"), "peer_chat_ok": rb_chat.get("ok"), "peer_req_id": req_id,
              "reply_peer": r_reply_peer.get("ok"), "reply_none": r_reply_none.get("ok"), "reply_own": r_reply_own.get("ok"),
              "audit_before_replies": a_before, "after_reply_peer": a1, "after_reply_none": a2, "after_reply_own": a3})
        emit({"part": "inspect", "runner_rc": rr.returncode, "opened": ins["opened"], "verify": ins["verify"],
              "own_numbers": ins["own_numbers"], "signed_twice": ins["signed_twice"],
              "kinds": [e["kind"] for e in ins["events"]], "summaries": [e["summary"] for e in ins["events"]],
              "long_preview_expected": long_prev, "long_preview_stored_equal": long_prev in fulls,
              "long_preview_len_chars": len(long_prev), "long_preview_lines": long_prev.count("\n") + 1,
              "short_previews": {k: ins["previews"][i + 1] for i, k in enumerate(SHORT_EACH)},
              "short_stored_equal": {k: ins["previews"][i + 1] in fulls for i, k in enumerate(SHORT_EACH)},
              "fulls": fulls, "member_status": ins["member_status"],
              "header_debug_example": ins["events"][0]["header_debug"] if ins["events"] else None})
        # byte greps: audit folder, daemon log, status answers, whole data folder
        needles = list(PLANT.values()) + [DROPPED, PEERMARK]
        logf = q.errf("a")
        stf = os.path.join(ROOT, "statuses.json")
        json.dump(statuses, open(stf, "w"))
        emit({"part": "grep",
              "audit_folder": grep_tree(os.path.join(cp, "audit"), needles),
              "daemon_log": {n: (n.encode() in open(logf, "rb").read()) for n in needles},
              "status_answers": {n: (n in open(stf).read()) for n in needles},
              "data_folder_live": grep_tree(q.dir("a"), needles)})
        ctl = os.path.join(ROOT, "control.txt")
        open(ctl, "w").write(LONG + "\n" + PEERMARK + "\n")
        emit({"part": "grep_control", "control_file": grep_tree(ROOT + "/control_only", needles) if False else
              {n: (n.encode() in open(ctl, "rb").read()) for n in needles}})
    finally:
        emit({"part": "left", "left": s.close()})


main()
