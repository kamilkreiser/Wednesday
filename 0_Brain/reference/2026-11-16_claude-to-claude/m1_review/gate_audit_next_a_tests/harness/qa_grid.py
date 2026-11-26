#!/usr/bin/env python3
"""QA-AUDIT-NEXT-A (h): ENUMERATED run property. (cause) x (sends before the seal 0/1/3) x (seals 1/2)
x (restart before the seal no/yes). Cause applied right after pairing, kept through the seals, then
rights back and the store read from a COPY (qa_store). Usage: qa_grid.py <bin> <work dir new> <reader> <out.jsonl> [causes]"""
import itertools, json, os, re, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qa_lib import Q

BIN, ROOT, READER, OUT = sys.argv[1:5]
CAUSES = sys.argv[5].split(",") if len(sys.argv) > 5 else ["none", "store", "anchors", "archive", "audit0755", "auditimm"]
SENDS = [int(x) for x in (sys.argv[6].split(",") if len(sys.argv) > 6 else ["0", "1", "3"])]
SEALS = [int(x) for x in (sys.argv[7].split(",") if len(sys.argv) > 7 else ["1", "2"])]
RESTART = [x == "1" for x in (sys.argv[8].split(",") if len(sys.argv) > 8 else ["0", "1"])]
os.makedirs(ROOT, exist_ok=False)
out = open(OUT, "w")
T_UNW = "not sealed: the log could not write its checkpoint; fix the cause (see status.audit), then give the command again"
T_NEW = "not sealed: nothing new since the last filed point"
T_OLD = "not sealed: nothing could be filed (nothing new since the last filed point, or the log could not write)"
pairs, fails, flags, n = {}, [], [], 0


def read_store(q, sidh, tag):
    sc = os.path.join(ROOT, f"sc_{tag}")
    r = subprocess.run([READER, "--exact", "qa_read_store", "--nocapture"], capture_output=True, timeout=120,
                       env=dict(os.environ, QA_DATA=q.dir("a"), QA_SID=sidh, QA_SCRATCH=sc))
    m = re.search(r"QASTORE (\{.*\})", r.stdout.decode())
    return json.loads(m.group(1)) if m else None


for cause, ns, nseal, rs in itertools.product(CAUSES, SENDS, SEALS, RESTART):
    n += 1
    tag = f"{n:02d}"
    rec = {"case": [cause, ns, nseal, rs]}
    q = Q(BIN, os.path.join(ROOT, tag))
    entry = os.path.join(q.dir("a"), "audit")
    try:
        q.start("a", ["--audit"]); q.start("b")
        if cause == "audit0755":
            os.mkdir(entry); os.chmod(entry, 0o755)
        if cause == "auditimm":
            os.mkdir(entry); os.chmod(entry, 0o700); subprocess.run(["chflags", "uchg", entry], check=True); flags.append(entry)
        q.pair("a", "b")
        st0 = q.status("a")
        sidh = st0["session"]["session_id"]
        fold = os.path.join(entry, sidh)
        if cause in ("store", "anchors", "archive"):
            os.chmod(os.path.join(fold, cause), 0o500)
        sends = []
        for i in range(ns):
            before = q.status("a")["session"]["send_next"]
            r = q.ctl("a", "send", {"kind": "chat", "text": f"QAG {tag} {i}"})
            after = q.status("a")["session"]["send_next"]
            sends.append({"ok": r.get("ok"), "code": (r.get("error") or {}).get("code"), "send_next": [before, after]})
            if r.get("ok") is not True and after != before:
                fails.append(f"{tag} {rec['case']}: a refused send was queued")
        rec["sends"] = sends
        if rs:
            q.stop("a"); q.start("a", ["--audit"]); time.sleep(0.8)
            rec["after_restart"] = q.status("a").get("audit")
        seals = []
        for j in range(nseal):
            seg_b = (q.status("a").get("audit") or {}).get("segment")
            r = q.ctl("a", "audit_seal", {})
            res = r.get("result") or {}
            seg_a = (q.status("a").get("audit") or {}).get("segment")
            stx = q.status("a").get("audit")
            seals.append({"row": res.get("row"), "text": res.get("action"), "sealed": res.get("sealed"), "calls": res.get("calls"),
                          "segment_before": seg_b, "segment_after": seg_a, "status_state": stx.get("state"), "status_reason": stx.get("reason")})
            k = f"{res.get('row')} | {res.get('action')}"
            pairs[k] = pairs.get(k, 0) + 1
            if res.get("sealed") is True and not (seg_b is not None and seg_a is not None and seg_a != seg_b):
                fails.append(f"{tag} {rec['case']}: sealed true without a moved segment: {res}")
            if (res.get("calls") or 0) > 1:
                fails.append(f"{tag} {rec['case']}: more than one seal call")
        rec["seals"] = seals
        # rights back, read the store
        if cause in ("store", "anchors", "archive"):
            os.chmod(os.path.join(fold, cause), 0o700)
        if cause == "auditimm":
            subprocess.run(["chflags", "nouchg", entry], check=True)
        stor = read_store(q, sidh, tag) if os.path.isdir(os.path.join(fold, "store")) else None
        rec["store"] = stor and {k: stor[k] for k in ("segment", "own_seq", "own_checkpoints", "archive_files", "signed_twice", "verifies")}
        for s in seals:
            if s["row"] == "10/14 (NothingToSeal)":
                if stor is None:
                    fails.append(f"{tag}: NothingToSeal with no store to read")
                    continue
                last = stor["own_checkpoints"][-1] if stor["own_checkpoints"] else 0
                truth = T_UNW if stor["own_seq"] > last else T_NEW
                # the store is read AFTER every seal of the case; a later seal may have filed: judge only the LAST NothingToSeal
        nts = [s for s in seals if s["row"] == "10/14 (NothingToSeal)"]
        if nts and stor is not None:
            s = nts[-1]
            last = stor["own_checkpoints"][-1] if stor["own_checkpoints"] else 0
            if seals[-1] is s:
                want = T_UNW if stor["own_seq"] > last else T_NEW
                if s["text"] != want:
                    fails.append(f"{tag} {rec['case']}: NothingToSeal text {s['text']!r} but the store shows own seq {stor['own_seq']} checkpoints {stor['own_checkpoints']}")
                rec["nothing_judged"] = {"text": s["text"], "store_seq": stor["own_seq"], "store_cps": stor["own_checkpoints"]}
        err = q.stderr("a")
        rec["created_lines"] = err.count("audit log created")
        if rs and err.count("audit log created") > (0 if cause in ("audit0755", "auditimm") else 1):
            fails.append(f"{tag} {rec['case']}: a log created after a restart")
        if stor and stor["signed_twice"]:
            fails.append(f"{tag} {rec['case']}: a number signed twice")
        rec["answers"] = q.ctl_raw("a", {"v": 1, "id": 1, "cmd": "status"}) is not None
        if not rec["answers"]:
            fails.append(f"{tag} {rec['case']}: the daemon stopped answering")
    except Exception as e:
        rec["error"] = repr(e)
        fails.append(f"{tag} {rec['case']}: harness error {e!r}")
    finally:
        try:
            if cause == "auditimm" and os.path.isdir(entry):
                subprocess.run(["chflags", "nouchg", entry])
        except Exception:
            pass
        rec["left"] = q.cleanup()
        out.write(json.dumps(rec) + "\n"); out.flush()
        print(tag, rec["case"], [ (s["row"], s["sealed"]) for s in rec.get("seals", [])], rec.get("error", ""), flush=True)
print(f"QA grid: {n} cases")
for k, v in sorted(pairs.items(), key=lambda x: -x[1]):
    print(f"QA pair\t{v}\t{k}")
print(f"QA flags set: {flags}")
print(f"QA failures: {len(fails)}")
for f in fails:
    print("QA FAIL", f)
