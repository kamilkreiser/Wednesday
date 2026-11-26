#!/usr/bin/env python3
"""QA-AUDIT-EMAIL (h): a log written by a REAL base build, opened by the head build.
Usage: python3 -B qae_oldnew.py <base bin dir> <head bin dir> <work dir (new)> <base inspect runner> <head inspect runner>
Convener `a` with --audit, joiner `b`. Loopback only. Every address is made up."""
import json, os, shutil, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qa_lib import Q

BB, HB, ROOT, RUNB, RUNH = sys.argv[1:6]
os.makedirs(ROOT)
ADDR1 = "qae.old.person@example.invalid"; ADDR2 = "qae.new.person@example.invalid"
T1 = f"QAE old build: mail {ADDR1} about the release"; T2 = f"QAE new build: mail {ADDR2} about the release"
def emit(d): print(json.dumps(d, sort_keys=True), flush=True)
def copy_inspect(q, name, runner, texts):
    cp = os.path.join(ROOT, name); shutil.copytree(q.dir("a"), cp, symlinks=True, ignore=shutil.ignore_patterns("*.sock", "*.lock", "ipc")); os.chmod(cp, 0o700)
    sid = [d for d in os.listdir(os.path.join(cp, "audit")) if len(d) == 64][0]
    tf = os.path.join(ROOT, name + ".texts.json"); json.dump(texts, open(tf, "w")); out = os.path.join(ROOT, name + ".inspect.json")
    rr = subprocess.run(runner, shell=True, env=dict(os.environ, QA_DATA=cp, QA_SID=sid, QA_OUT=out, QA_TEXTS=tf), capture_output=True, text=True)
    ins = json.load(open(out)); return ins, rr.returncode, cp
def grep(root, needle):
    hits = []
    for r, ds, fs in os.walk(root):
        for f in fs:
            if needle.encode() in open(os.path.join(r, f), "rb").read(): hits.append(os.path.relpath(os.path.join(r, f), root))
    return hits
q = Q(BB, os.path.join(ROOT, "run"))
try:
    q.start("a", ["--audit"]); q.start("b"); q.pair("a", "b")
    r1 = q.ctl("a", "send", {"kind": "chat", "text": T1})
    st1 = q.status("a").get("audit")
    q.stop("a")
    ins1, rc1, cp1 = copy_inspect(q, "copy_base", RUNB, [T1])
    emit({"part": "base wrote", "send_ok": r1.get("ok"), "audit_status": st1, "inspect_rc": rc1, "events": [(e["seq"], e["kind"], e["full"]) for e in ins1["events"]], "verify": ins1["verify"][:200], "addr1_in_audit": grep(os.path.join(cp1, "audit"), ADDR1)})
    q.bin = HB  # the head binaries on the same data folder
    q.stop("b"); q.start("a", ["--audit"]); q.start("b")
    try:
        conn = q.wait_connected("a", "b", t=180)
    except AssertionError as e:
        conn = repr(e)
    emit({"part": "reconnect", "connected_after_s": conn})
    r2 = q.ctl("a", "send", {"kind": "chat", "text": T2})
    seal = q.ctl("a", "audit_seal")
    st2 = q.status("a").get("audit")
    q.stop("a")
    ins2, rc2, cp2 = copy_inspect(q, "copy_head", RUNH, [T1, T2])
    ev = [(e["bundle"], e["is_export"], e["seq"], e["full"]) for e in ins2["events"]]
    first_base = [e["full"] for e in ins1["events"] if e["seq"] == 1]
    first_head = sorted({e["full"] for e in ins2["events"] if e["seq"] == 1})
    emit({"part": "head opened", "send_ok": r2.get("ok"), "seal": seal.get("result") or seal.get("error"), "audit_status": st2, "inspect_rc": rc2,
          "opened": ins2["opened"], "segment_files": ins2["segment_files"], "verify": ins2["verify"][:300], "events": ev,
          "first_preview_byte_identical_to_base": first_head == first_base, "first_base": first_base, "first_head": first_head,
          "head_redactor_on_T1_would_give": ins2["previews"][0], "addr1_in_audit": grep(os.path.join(cp2, "audit"), ADDR1), "addr2_in_audit": grep(os.path.join(cp2, "audit"), ADDR2)})
finally:
    emit({"part": "left", "left": q.cleanup()})
