#!/usr/bin/env python3
"""QA-AUDIT-WIRE task 6: SIGKILL of the --audit daemon at moments of the checker's choosing (inside a
seal, between a record and its reply, idle), restart, and the invariants; then the inspector over a copy.
Usage: python3 -B qa_kill.py <bin dir> <work dir (new)> <inspect runner> [kills]"""
import json, os, random, shutil, subprocess, sys, threading, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import qa_causes as C  # noqa: E402

BIN, ROOT, RUNNER = sys.argv[1], sys.argv[2], sys.argv[3]
KILLS = int(sys.argv[4]) if len(sys.argv) > 4 else 14
os.makedirs(ROOT, exist_ok=True)
S, emit = C.S, C.emit
random.seed(0xA0D1)
AEX = ("--audit", "--keep-relay-identity")


def snap(d):
    out = set()
    for sub in ("archive", "anchors"):
        p = os.path.join(d, sub)
        if os.path.isdir(p):
            out |= {sub + "/" + f for f in os.listdir(p)}
    return out


s = S("kill", a_extra=AEX)
events = []
last_acked = 0
reach = {"in a seal": 0, "between a record and its reply": 0, "idle": 0, "seal answered before the kill": 0}
try:
    d = s.adir()
    sid = os.path.basename(d)
    for i in range(5):
        r = s.send("a", f"QAK warm {i}")
        if r.get("ok"):
            last_acked = s.audit()["own_seq"]
    k = 0
    attempts = 0
    while k < KILLS and attempts < KILLS * 4:
        attempts += 1
        mode = os.environ.get("QA_MODE") or ["seal", "record", "idle"][attempts % 3]
        for j in range(random.randint(1, 4)):
            r = s.send("a", f"QAK {attempts}-{j} " + "y" * random.randint(1, 200))
            if r.get("ok"):
                last_acked = max(last_acked, s.audit()["own_seq"])
        before = snap(d)
        _a = s.audit()
        seg_before = _a["segment"]
        seq_pre = _a["own_seq"]
        res = {}

        def call(cmd, args=None):
            try:
                res["r"] = s.q.ctl_raw("a", {"v": 1, "id": 1, "cmd": cmd, **({"args": args} if args else {})})
            except Exception as e:
                res["r"] = repr(e)
        if mode == "seal":
            th = threading.Thread(target=call, args=("audit_seal",))
        elif mode == "record":
            th = threading.Thread(target=call, args=("send", {"kind": "chat", "text": f"QAK in flight {attempts}"}))
        else:
            th = None
        if th:
            th.start()
            time.sleep(random.uniform(float(os.environ.get("QA_DMIN", "0")), float(os.environ.get("QA_DMAX", "0.012"))))
        pid = s.q.procs["a"].pid
        s.q.crash("a")
        at_kill = snap(d)
        if th:
            th.join(30)
        ans = res.get("r")
        answered_ok = isinstance(ans, dict) and ans.get("ok") is True
        new_files = sorted(at_kill - before)
        pending = "anchors/pending" in at_kill
        if mode == "seal":
            where = "in a seal" if (pending or new_files or (s.audit()["segment"] if False else False)) and not answered_ok else (
                "seal answered before the kill" if answered_ok else "idle")
        elif mode == "record":
            where = "between a record and its reply" if not answered_ok else "idle"
        else:
            where = "idle"
        if mode == "record" and answered_ok:
            last_acked = max(last_acked, seq_pre + 1)
        s.q.start("a", list(AEX))
        a = s.audit()
        created = [l for l in s.q.stderr("a").splitlines() if "audit log created" in l]
        opened = [l for l in s.q.stderr("a").splitlines() if "audit log opened" in l]
        ev = {"kill": k + 1, "mode": mode, "where": where, "answer_before_kill": ans if not isinstance(ans, dict) else
              {"ok": ans.get("ok"), "res": ans.get("result") or ans.get("error")},
              "new_files_at_kill": new_files, "pending_at_kill": pending, "segment_before": seg_before,
              "after": {"state": a["state"], "own_seq": a["own_seq"], "segment": a["segment"], "reason": a["reason"]},
              "last_acked": last_acked, "own_seq_not_lower": (a["own_seq"] or 0) >= last_acked,
              "created_lines_total": len(created), "opened_lines_total": len(opened), "last_opened": opened[-1:] }
        events.append(ev)
        reach[where] = reach.get(where, 0) + 1
        k += 1
        last_acked = max(last_acked, a["own_seq"] or 0) if a["state"] == "on" else last_acked
        try:
            s.q.wait_connected("a", "b", 120)
        except AssertionError:
            pass
        s.ack_all("b")
    # final: one seal, then stop and inspect a copy
    fin = s.q.ctl("a", "audit_seal")
    s.q.stop("a")
    cp = os.path.join(ROOT, "copyA")
    shutil.copytree(s.q.dir("a"), cp, ignore=shutil.ignore_patterns("ipc"))
    outp = os.path.join(ROOT, "inspect.json")
    rr = subprocess.run(RUNNER, shell=True, env=dict(os.environ, QA_DATA=cp, QA_SID=sid, QA_OUT=outp),
                        capture_output=True, text=True)
    ins = json.load(open(outp))
    nums = ins["own_numbers"]
    emit({"events": events})
    emit({"reach": reach, "kills": len(events), "final_seal": fin.get("result") or fin.get("error"),
          "inspect_rc": rr.returncode, "opened": ins["opened"], "verify": ins["verify"], "segment_files": ins["segment_files"],
          "own_numbers_min_max_count": [min(nums), max(nums), len(nums)], "gaps": [x for x in range(1, max(nums) + 1) if x not in nums],
          "signed_twice": ins["signed_twice"], "every_restart_state_on": all(e["after"]["state"] == "on" for e in events),
          "never_lower": all(e["own_seq_not_lower"] for e in events),
          "created_lines_final": max(e["created_lines_total"] for e in events)})
finally:
    emit({"left": s.close()})
