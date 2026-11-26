#!/usr/bin/env python3
"""QA-AUDIT-NEXT-A (h): SIGKILL the daemon inside a seal and between a record and its reply, at a sweep of
delays; restart; seal (may file), seal again (nothing new): each NothingToSeal text against the store copy.
Usage: qa_kill.py <bin> <work dir new> <reader> <out.jsonl>"""
import json, os, re, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qa_lib import Q
BIN, ROOT, READER, OUT = sys.argv[1:5]
os.makedirs(ROOT)
out = open(OUT, "w")
T_UNW = "not sealed: the log could not write its checkpoint; fix the cause (see status.audit), then give the command again"
T_NEW = "not sealed: nothing new since the last filed point"
bad = []


def store(q, sidh, tag):
    r = subprocess.run([READER, "--exact", "qa_read_store", "--nocapture"], capture_output=True, timeout=120,
                       env=dict(os.environ, QA_DATA=q.dir("a"), QA_SID=sidh, QA_SCRATCH=os.path.join(ROOT, "sc_" + tag)))
    m = re.search(r"QASTORE (\{.*\})", r.stdout.decode())
    return json.loads(m.group(1)) if m else {"error": r.stdout.decode()[-400:]}


def listing(d):
    out = []
    for r, ds, fs in os.walk(d):
        for f in fs:
            out.append(os.path.relpath(os.path.join(r, f), d))
    return sorted(out)


n = 0
for what in ("seal", "send"):
    for delay_ms in (0, 1, 2, 3, 5, 8, 12, 20, 40):
        n += 1
        tag = f"{what}{delay_ms}"
        q = Q(BIN, os.path.join(ROOT, tag))
        rec = {"what": what, "delay_ms": delay_ms}
        try:
            q.start("a", ["--audit"]); q.start("b"); q.pair("a", "b")
            sidh = q.status("a")["session"]["session_id"]
            fold = os.path.join(q.dir("a"), "audit", sidh)
            for i in range(3):
                q.ctl("a", "send", {"kind": "chat", "text": f"QAK {i}"})
            req = {"v": 1, "id": 5, "cmd": "audit_seal"} if what == "seal" else {"v": 1, "id": 5, "cmd": "send", "args": {"kind": "chat", "text": "QAK killed"}}
            c = subprocess.Popen([os.path.join(BIN, "coagentd"), "ctl", "--data-dir", q.dir("a"), json.dumps(req)], env=q.env(), stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            time.sleep(delay_ms / 1000)
            q.crash("a")
            rep = c.communicate(timeout=30)[0].decode().strip()
            rec["reply_before_kill"] = rep[:200] or None
            rec["files_after_kill"] = [f for f in listing(fold) if not f.startswith("store/")] + [f"store: {len([f for f in listing(fold) if f.startswith('store/')])} files"]
            q.start("a", ["--audit"]); time.sleep(0.8)
            st = q.status("a").get("audit")
            rec["after_restart"] = {k: st.get(k) for k in ("state", "reason", "segment", "own_seq", "seals")}
            seals = []
            for j in range(2):
                r = q.ctl("a", "audit_seal", {})["result"]
                s = store(q, sidh, f"{tag}_{j}")
                last = s["own_checkpoints"][-1] if s.get("own_checkpoints") else 0
                seals.append({"row": r["row"], "sealed": r["sealed"], "text": r["action"], "store_seq": s.get("own_seq"), "store_cps": s.get("own_checkpoints"), "store_segment": s.get("segment"), "twice": s.get("signed_twice")})
                if r["row"] == "10/14 (NothingToSeal)":
                    want = T_UNW if s["own_seq"] > last else T_NEW
                    if r["action"] != want:
                        bad.append(f"{tag} seal {j}: {r['action']!r} but store seq {s['own_seq']} cps {s['own_checkpoints']}")
                if s.get("signed_twice"):
                    bad.append(f"{tag}: a number signed twice")
            rec["seals"] = seals
        except Exception as e:
            rec["error"] = repr(e); bad.append(f"{tag}: harness error {e!r}")
        finally:
            rec["left"] = q.cleanup()
            out.write(json.dumps(rec) + "\n"); out.flush()
            print(tag, json.dumps(rec)[:700], flush=True)
print(f"QA kill: {n} cases; failures {len(bad)}")
for b in bad:
    print("QA FAIL", b)
