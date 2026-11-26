#!/usr/bin/env python3
"""QA-AUDIT-WIRE task 3: fail closed (R-6), every cause the checker can make, plus Open (a) and (b).
Head binaries; convener `a` with --audit, joiner `b` without. Loopback only; data under <work dir>.
Usage: python3 -B qa_causes.py <bin dir> <work dir (new)> [cause ...]   -> JSON lines on stdout"""
import json, os, shutil, stat, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qa_lib import Q

BIN, ROOT = sys.argv[1], sys.argv[2]
ONLY = sys.argv[3:]
os.makedirs(ROOT, exist_ok=False)
QUAR = os.path.join(ROOT, "_quarantine")  # never delete: move
os.makedirs(QUAR)
R6 = "not sent: the audit log could not record this message (see status.audit); nothing was queued"
OUT = []


def emit(d):
    OUT.append(d)
    print(json.dumps(d, sort_keys=True), flush=True)


class S:
    def __init__(self, name, a_extra=("--audit",), pre=None):
        self.q = Q(BIN, os.path.join(ROOT, name))
        self.n = 0
        if pre:
            pre(self)
        self.q.start("a", list(a_extra))
        self.q.start("b")
        self.q.pair("a", "b")

    def adir(self):
        st = self.q.status("a")
        sid = st["session"]["session_id"] if "session_id" in st.get("session", {}) else None
        base = os.path.join(self.q.dir("a"), "audit")
        if not os.path.isdir(base):
            return None
        subs = [d for d in os.listdir(base) if len(d) == 64]
        return os.path.join(base, subs[0]) if subs else None

    def send(self, who, text, kind="chat", re=None):
        a = {"kind": kind, "text": text}
        if re is not None:
            a["re"] = re
        return self.q.ctl(who, "send", a)

    def outbox(self, who="a"):
        try:
            v = json.load(open(os.path.join(self.q.dir(who), "outbox.json")))
        except Exception as e:
            return {"error": repr(e)}
        return v

    def got(self, who, text, t=6.0):
        t0 = time.time()
        while time.time() - t0 < t:
            r = self.q.ctl(who, "inbox_read")
            ms = r.get("result", {}).get("messages", [])
            if any(m.get("text") == text for m in ms):
                return True
            time.sleep(0.25)
        return False

    def ack_all(self, who):
        for _ in range(50):
            r = self.q.ctl(who, "inbox_read")
            res = r.get("result", {})
            ack = res.get("ack")
            if ack:
                self.q.ctl(who, "inbox_ack", {"upto": ack})
            if not res.get("more"):
                break

    def uniq(self, tag):
        self.n += 1
        return f"QAW-{tag}-{self.n}-{int(time.time()*1000) % 100000}"

    def audit(self):
        return self.q.status("a").get("audit")

    def probe(self, tag):
        """receiving, inbox, status and audit_seal while the cause holds"""
        t = self.uniq(tag + "-from-b")
        sb = self.send("b", t)
        recv = self.got("a", t)
        st = self.q.ctl("a", "status")
        seal = self.q.ctl("a", "audit_seal")
        return {
            "b_send_ok": sb.get("ok"),
            "a_received_and_inbox": recv,
            "a_status_ok": st.get("ok"),
            "a_status_audit": st.get("result", {}).get("audit"),
            "a_audit_seal": seal.get("result") or seal.get("error"),
            "a_alive": self.q.procs["a"].poll() is None,
        }

    def refused_check(self, tag):
        ob0 = self.outbox()
        t = self.uniq(tag)
        r = self.send("a", t)
        ob1 = self.outbox()
        txt = json.dumps(ob1)
        return t, {
            "send": r.get("error") or r.get("result"),
            "send_ok": r.get("ok"),
            "r6_text": (r.get("error") or {}).get("message") == R6,
            "code": (r.get("error") or {}).get("code"),
            "send_next_before": ob0.get("send_next"),
            "send_next_after": ob1.get("send_next"),
            "text_in_outbox_json": t in txt,
        }

    def close(self):
        return self.q.cleanup()


def chmod(p, mode):
    os.chmod(p, mode)


def run_cause(name, apply, undo, expect_refused=True):
    s = S("c_" + name)
    try:
        first = s.uniq("first")
        r0 = s.send("a", first)
        seq0 = s.audit()["own_seq"]
        apply(s)
        t, ref = s.refused_check(name)
        ref["peer_got_it"] = s.got("b", t, 4.0)
        pr = s.probe(name)
        undo(s)
        t2 = s.uniq(name + "-after")
        r2 = s.send("a", t2)
        a2 = s.audit()
        emit({
            "cause": name,
            "first_send_ok": r0.get("ok"),
            "own_seq_before": seq0,
            "during": ref,
            "probe": pr,
            "after_send": r2.get("error") or r2.get("result"),
            "after_send_ok": r2.get("ok"),
            "after_peer_got_it": s.got("b", t2),
            "after_own_seq": a2.get("own_seq"),
            "after_audit": a2,
            "stderr_audit_lines": [l for l in s.q.stderr("a").splitlines() if "audit" in l],
        })
    finally:
        emit({"cause": name, "left_processes": s.close()})


def sub(s, n):
    return os.path.join(s.adir(), n)


CAUSES = {}

CAUSES["store_unwritable"] = (lambda s: chmod(sub(s, "store"), 0o500), lambda s: chmod(sub(s, "store"), 0o700))
CAUSES["anchors_unwritable"] = (lambda s: chmod(sub(s, "anchors"), 0o500), lambda s: chmod(sub(s, "anchors"), 0o700))
CAUSES["archive_unwritable"] = (lambda s: chmod(sub(s, "archive"), 0o500), lambda s: chmod(sub(s, "archive"), 0o700))
CAUSES["auditdir_0755_midsession"] = (lambda s: chmod(os.path.dirname(s.adir()), 0o755),
                                      lambda s: chmod(os.path.dirname(s.adir()), 0o700))
CAUSES["sessiondir_0755"] = (lambda s: chmod(s.adir(), 0o755), lambda s: chmod(s.adir(), 0o700))


def main():
    for name, (ap, un) in CAUSES.items():
        if ONLY and name not in ONLY:
            continue
        run_cause(name, ap, un)
    # audit/ wrong at CREATE time: a 0755 directory, and a plain file
    for name, mk in [("auditdir_0755_at_create", lambda p: os.makedirs(p, mode=0o755) or os.chmod(p, 0o755)),
                     ("auditdir_is_file_at_create", lambda p: open(p, "w").close())]:
        if ONLY and name not in ONLY:
            continue

        def pre(s, mk=mk):
            os.makedirs(s.q.dir("a"), mode=0o700)
            mk(os.path.join(s.q.dir("a"), "audit"))
        s = S("c_" + name, pre=pre)
        try:
            t, ref = s.refused_check(name)
            ref["peer_got_it"] = s.got("b", t, 4.0)
            pr = s.probe(name)
            emit({"cause": name, "during": ref, "probe": pr,
                  "stderr_audit_lines": [l for l in s.q.stderr("a").splitlines() if "audit" in l]})
        finally:
            emit({"cause": name, "left_processes": s.close()})


if __name__ == "__main__":
    main()
