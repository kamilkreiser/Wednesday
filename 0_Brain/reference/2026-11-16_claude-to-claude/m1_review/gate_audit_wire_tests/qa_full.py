#!/usr/bin/env python3
"""QA-AUDIT-WIRE task 3 (LogFull with default limits) and section 1a (5) (the peer's requested allowance
filled by replies whose `re` names nothing); plus the base pre-check of `audit_seal` with dirty unsaved state.
Usage: python3 -B qa_full.py <bin dir> <work dir (new)> local|peer|precheck"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import qa_causes as C  # noqa: E402

BIN, ROOT, MODE = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(ROOT, exist_ok=True)
S, emit = C.S, C.emit
BIG = ("QAW fill " + "abcdefghij" * 23)[:239]  # one line, 239 chars: a preview of 239 chars


def fill(s, kind, re=None, cap=4000):
    n = 0
    t0 = time.time()
    last = None
    while n < cap:
        r = s.send("a", f"{n:05d}{BIG}"[:240], kind=kind, re=re)
        if not r.get("ok"):
            last = r
            break
        n += 1
        if n % 50 == 0:
            s.ack_all("b")
        if not r.get("result", {}).get("sent_now", True):
            time.sleep(0.05)
    return n, last, round(time.time() - t0, 1)


s = S("full_" + MODE)
try:
    if MODE == "local":
        n, last, secs = fill(s, "chat")
        a = s.audit()
        pr = s.probe("full")
        # a reply charged to the peer still lands? (its allowance is separate)
        rr = s.send("a", "QAW reply after full", kind="reply", re="zzzz0000")
        emit({"mode": MODE, "accepted": n, "refusal": last, "secs": secs, "audit": a, "probe": pr,
              "reply_after_full": rr.get("result") or rr.get("error"),
              "log_refusals": [l for l in s.q.stderr("a").splitlines() if "refused" in l][-3:]})
    elif MODE == "peer":
        n, last, secs = fill(s, "reply", re="zzzzQAWnothing0000")
        a = s.audit()
        rc = s.send("a", "QAW chat after the peer's allowance is full")
        # a reply to a REAL request of the peer, now
        s.send("b", "QAW-REAL-REQ", kind="request")
        time.sleep(1.5)
        ms = s.q.ctl("a", "inbox_read")["result"]["messages"]
        req = [m for m in ms if m.get("type") == "request.new"][-1]
        rid = req.get("request_id") or req.get("id")
        rreal = s.send("a", "QAW reply to a real request", kind="reply", re=rid)
        emit({"mode": MODE, "accepted_replies_naming_nothing": n, "refusal": last, "secs": secs, "audit": a,
              "chat_after": rc.get("result") or rc.get("error"),
              "reply_to_real_request_after": rreal.get("result") or rreal.get("error"),
              "log_refusals": [l for l in s.q.stderr("a").splitlines() if "refused" in l][-3:]})
    elif MODE == "precheck":
        s.send("a", "QAW first")
        os.chmod(s.q.dir("a"), 0o500)
        try:
            s.send("b", "QAW peer message while a cannot save")
            time.sleep(2.0)
            st = s.q.ctl("a", "status")
            seal = s.q.ctl("a", "audit_seal")
            snd = s.send("a", "QAW send while unsaved")
        finally:
            os.chmod(s.q.dir("a"), 0o700)
        seal2 = s.q.ctl("a", "audit_seal")
        emit({"mode": MODE, "status_ok": st.get("ok"), "seal_while_unsaved": seal, "send_while_unsaved": snd,
              "seal_after_restore": seal2.get("result") or seal2.get("error"),
              "log": [l for l in s.q.stderr("a").splitlines() if "save" in l][-3:]})
finally:
    emit({"mode": MODE, "left": s.close()})
