#!/usr/bin/env python3
"""QA-AUDIT-WIRE task 3 (part 2) and task 1 (iii): anchors two sends, the session folder moved away
(running, and across a restart), Open (a) (record lands, daemon state save fails), the host closed
(LandedUnknown via an unreadable store), and a seal whose `status()` fails just before it.
Usage: python3 -B qa_causes2.py <bin dir> <work dir (new)> [scenario ...]"""
import json, os, shutil, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import qa_causes as C  # noqa: E402  (re-uses S, emit; its main() runs only when argv names its causes)

S, emit = C.S, C.emit
ONLY = sys.argv[3:]


def want(n):
    return not ONLY or n in ONLY


def files_with(root, needle):
    hits = []
    for r, ds, fs in os.walk(root):
        for f in fs:
            p = os.path.join(r, f)
            try:
                if needle.encode() in open(p, "rb").read():
                    hits.append(os.path.relpath(p, root))
            except PermissionError:
                hits.append("UNREADABLE " + os.path.relpath(p, root))
    return hits


def audit_lines(s):
    return [l for l in s.q.stderr("a").splitlines() if "audit" in l]


def sc_anchors_two():
    s = S("d_anchors_two")
    try:
        s.send("a", s.uniq("first"))
        anc = os.path.join(s.adir(), "anchors")
        os.chmod(anc, 0o500)
        t1, r1 = s.refused_check("anch1")
        r1["peer_got_it"] = s.got("b", t1, 4)
        a1 = s.audit()
        t2, r2 = s.refused_check("anch2")
        r2["peer_got_it"] = s.got("b", t2, 4)
        pr = s.probe("anch")
        os.chmod(anc, 0o700)
        t3 = s.uniq("anch-after")
        r3 = s.send("a", t3)
        emit({"scenario": "anchors_two", "send1": r1, "audit_after_send1": a1, "send2": r2, "probe": pr,
              "after": r3.get("result") or r3.get("error"), "after_peer": s.got("b", t3), "after_audit": s.audit(),
              "log": audit_lines(s)})
    finally:
        emit({"scenario": "anchors_two", "left": s.close()})


def sc_moved_running():
    s = S("d_moved_run", a_extra=("--audit", "--keep-relay-identity"))
    try:
        s.send("a", s.uniq("first"))
        d = s.adir()
        sid = os.path.basename(d)
        dest = os.path.join(C.QUAR, "moved_run_" + sid)
        shutil.move(d, dest)
        t1, r1 = s.refused_check("moved1")
        r1["peer_got_it"] = s.got("b", t1, 4)
        pr = s.probe("moved")
        present = os.path.exists(d)
        emit({"scenario": "moved_running", "send": r1, "probe": pr, "folder_present_after": present,
              "audit_dir_listing": sorted(os.listdir(os.path.dirname(d))), "log": audit_lines(s)})
        # restart with the folder still away
        s.q.stop("a")
        s.q.start("a", ["--audit", "--keep-relay-identity"])
        s.q.wait_connected("a", "b", 120)
        t2, r2 = s.refused_check("moved2")
        r2["peer_got_it"] = s.got("b", t2, 4)
        pr2 = s.probe("moved-restart")
        emit({"scenario": "moved_running+restart", "send": r2, "probe": pr2,
              "folder_present_after": os.path.exists(d),
              "audit_dir_listing": sorted(os.listdir(os.path.dirname(d))),
              "created_lines": [l for l in audit_lines(s) if "created" in l], "log": audit_lines(s)})
    finally:
        emit({"scenario": "moved_running", "left": s.close()})


def sc_moved_restart():
    s = S("d_moved_rst", a_extra=("--audit", "--keep-relay-identity"))
    try:
        s.send("a", s.uniq("first"))
        d = s.adir()
        sid = os.path.basename(d)
        s.q.stop("a")
        shutil.move(d, os.path.join(C.QUAR, "moved_rst_" + sid))
        s.q.start("a", ["--audit", "--keep-relay-identity"])
        s.q.wait_connected("a", "b", 120)
        t, r = s.refused_check("mvr")
        r["peer_got_it"] = s.got("b", t, 4)
        pr = s.probe("mvr")
        emit({"scenario": "moved_restart", "send": r, "probe": pr, "folder_present_after": os.path.exists(d),
              "audit_dir_listing": sorted(os.listdir(os.path.dirname(d))),
              "created_lines": [l for l in audit_lines(s) if "created" in l], "log": audit_lines(s)})
    finally:
        emit({"scenario": "moved_restart", "left": s.close()})


def sc_open_a():
    s = S("d_open_a")
    try:
        s.send("a", s.uniq("first"))
        seq0 = s.audit()["own_seq"]
        dd = s.q.dir("a")
        text = "QAW-OPEN-A unique text " + str(int(time.time()))
        os.chmod(dd, 0o500)
        try:
            r1 = s.send("a", text)
            a1 = s.q.ctl("a", "status").get("result", {}).get("audit")
        finally:
            os.chmod(dd, 0o700)
        ob = s.outbox()
        peer1 = s.got("b", text, 4)
        r2 = s.send("a", text)  # the same text, given again
        peer2 = s.got("b", text, 6)
        a2 = s.audit()
        emit({"scenario": "open_a", "own_seq_before": seq0, "send_during": r1.get("error") or r1.get("result"),
              "audit_after_refusal": a1, "text_in_outbox_after_refusal": text in json.dumps(ob),
              "peer_got_after_refusal": peer1, "resend": r2.get("error") or r2.get("result"),
              "peer_got_after_resend": peer2, "own_seq_end": a2["own_seq"], "log": audit_lines(s),
              "stderr_tail": s.q.stderr("a").splitlines()[-6:]})
    finally:
        emit({"scenario": "open_a", "left": s.close()})


def sc_landed_unknown_record():
    s = S("d_lu_rec")
    try:
        s.send("a", s.uniq("first"))
        st = os.path.join(s.adir(), "store")
        os.chmod(st, 0o300)  # write+search, no read: a put lands, its directory sync cannot open the dir
        try:
            t1, r1 = s.refused_check("lu1")
            a1 = s.q.ctl("a", "status").get("result", {}).get("audit")
            t2, r2 = s.refused_check("lu2")
            pr = s.probe("lu")
        finally:
            os.chmod(st, 0o700)
        r1["peer_got_it"] = s.got("b", t1, 3)
        t3 = s.uniq("lu-after")
        r3 = s.send("a", t3)
        emit({"scenario": "landed_unknown_record", "send1": r1, "audit_after_send1": a1, "send2": r2, "probe": pr,
              "after": r3.get("result") or r3.get("error"), "after_peer": s.got("b", t3), "after_audit": s.audit(),
              "store_files_with_send1_text": len(files_with(st, t1)), "log": audit_lines(s)})
    finally:
        emit({"scenario": "landed_unknown_record", "left": s.close()})


def sc_landed_unknown_seal():
    s = S("d_lu_seal")
    try:
        s.send("a", s.uniq("first"))
        st = os.path.join(s.adir(), "store")
        os.chmod(st, 0o300)
        try:
            seal = s.q.ctl("a", "audit_seal")
            a1 = s.q.ctl("a", "status").get("result", {}).get("audit")
        finally:
            os.chmod(st, 0o700)
        a2 = s.audit()
        seal2 = s.q.ctl("a", "audit_seal")
        emit({"scenario": "landed_unknown_seal", "seal": seal.get("result") or seal.get("error"), "audit_during": a1,
              "audit_after_restore": a2, "seal_again": seal2.get("result") or seal2.get("error"), "log": audit_lines(s)})
    finally:
        emit({"scenario": "landed_unknown_seal", "left": s.close()})


def sc_seg_before_fallback(root_mode=0o300, store_mode=0o500, tag="iii"):
    """task 1 (iii): a seal after one landed seal (segment 1), with status() failing (root unreadable)
    and the commit failing (store unwritable)."""
    s = S("d_" + tag)
    try:
        s.send("a", s.uniq("first"))
        s1 = s.q.ctl("a", "audit_seal")["result"]
        for i in range(55):
            s.send("a", s.uniq("fill"))
            if i % 20 == 19:
                s.ack_all("b")
        d = s.adir()
        st = os.path.join(d, "store")
        before = s.audit()
        arch_before = sorted(os.listdir(os.path.join(d, "archive")))
        os.chmod(st, store_mode)
        os.chmod(d, root_mode)
        try:
            seal = s.q.ctl("a", "audit_seal")
            a1 = s.q.ctl("a", "status").get("result", {}).get("audit")
        finally:
            os.chmod(d, 0o700)
            os.chmod(st, 0o700)
        a2 = s.audit()
        arch_after = sorted(os.listdir(os.path.join(d, "archive")))
        seal_again = s.q.ctl("a", "audit_seal")
        emit({"scenario": "seg_before_fallback_" + tag, "first_seal": s1, "audit_before": before,
              "seal": seal.get("result") or seal.get("error"), "audit_during": a1, "audit_after_restore": a2,
              "archive_before": arch_before, "archive_after": arch_after,
              "seal_again": seal_again.get("result") or seal_again.get("error"),
              "audit_after_again": s.audit(), "log": audit_lines(s)})
    finally:
        emit({"scenario": "seg_before_fallback_" + tag, "left": s.close()})


SC = {
    "anchors_two": sc_anchors_two,
    "moved_running": sc_moved_running,
    "moved_restart": sc_moved_restart,
    "open_a": sc_open_a,
    "lu_record": sc_landed_unknown_record,
    "lu_seal": sc_landed_unknown_seal,
    "iii": sc_seg_before_fallback,
}
for n, f in SC.items():
    if want(n):
        try:
            f()
        except Exception as e:
            emit({"scenario": n, "harness_error": repr(e)})


def sc_iii2():
    """task 1 (iii), second form: a stored own checkpoint newer than the last seal is left by a seal
    refused after its step 0 (archive/ unwritable); then root unreadable (status() fails, segment_before
    falls back to 0) and store/ unwritable (the commit fails, the store re-opens at the same segment)."""
    s = S("d_iii2")
    try:
        s.send("a", s.uniq("first"))
        s1 = s.q.ctl("a", "audit_seal")["result"]
        s.send("a", s.uniq("second"))
        s.send("a", s.uniq("third"))
        d = s.adir()
        st, ar = os.path.join(d, "store"), os.path.join(d, "archive")
        os.chmod(ar, 0o500)
        try:
            s2 = s.q.ctl("a", "audit_seal")
        finally:
            os.chmod(ar, 0o700)
        before = s.audit()
        arch_before = sorted(os.listdir(ar))
        os.chmod(st, 0o500)
        os.chmod(d, 0o300)
        try:
            seal = s.q.ctl("a", "audit_seal")
            during = s.q.ctl("a", "status").get("result", {}).get("audit")
        finally:
            os.chmod(d, 0o700)
            os.chmod(st, 0o700)
        after = s.audit()
        arch_after = sorted(os.listdir(ar))
        again = s.q.ctl("a", "audit_seal")
        emit({"scenario": "iii2", "first_seal": s1, "seal_archive_unwritable": s2.get("result") or s2.get("error"),
              "audit_before": before, "archive_before": arch_before,
              "SEAL_UNDER_TEST": seal.get("result") or seal.get("error"), "audit_during": during,
              "audit_after_restore": after, "archive_after": arch_after,
              "seal_again": again.get("result") or again.get("error"), "audit_end": s.audit(), "log": audit_lines(s)})
    finally:
        emit({"scenario": "iii2", "left": s.close()})


if "iii2" in ONLY:
    try:
        sc_iii2()
    except Exception as e:
        emit({"scenario": "iii2", "harness_error": repr(e)})
