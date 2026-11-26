#!/usr/bin/env python3
"""QA-AUDIT-NEXT-A (b1) F-6 + S-7 + S-8 + restart, (b3) R2-N3 store reads, (b5) S-2, (b4) N-5.
Usage: python3 -B qa_an.py <bin dir> <work dir (new)> <store reader binary> <out.jsonl> case...
Cases: create_0755 create_file create_uchg n_i n_ii n_iii n_iv n_v n_vi n_vii
Every daemon: loopback, data folder under the work dir. The store is read from a COPY (qa_store)."""
import glob, json, os, re, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qa_lib import Q

BIN, ROOT, READER, OUT = sys.argv[1:5]
CASES = sys.argv[5:]
os.makedirs(ROOT, exist_ok=False)
outf = open(OUT, "a")
flags_set = []


def emit(case, step, v):
    outf.write(json.dumps({"case": case, "step": step, "v": v}) + "\n")
    outf.flush()
    print(f"[{case}] {step}: {json.dumps(v)[:400]}")


def audit(q, w="a"):
    return q.status(w).get("audit")


def sid(q):
    return q.status("a")["session"]["session_id"]


def folder(q):
    return os.path.join(q.dir("a"), "audit", sid(q))


n_read = [0]


def store(q, case, step):
    n_read[0] += 1
    scratch = os.path.join(ROOT, f"sc{n_read[0]}")
    env = dict(os.environ, QA_DATA=q.dir("a"), QA_SID=sid(q), QA_SCRATCH=scratch)
    r = subprocess.run([READER, "--exact", "qa_read_store", "--nocapture", "--test-threads=1"], env=env, capture_output=True, timeout=120)
    m = re.search(r"QASTORE (\{.*\})", r.stdout.decode())
    v = json.loads(m.group(1)) if m else {"error": r.stdout.decode()[-800:] + r.stderr.decode()[-800:]}
    emit(case, f"STORE {step}", v)
    return v


def seal(q, case, step):
    r = q.ctl("a", "audit_seal", {})
    emit(case, step, r)
    emit(case, step + " -> status.audit", audit(q))
    return r


def send(q, case, step, text):
    r = q.ctl("a", "send", {"kind": "chat", "text": text})
    emit(case, step, r)
    return r


def new_q(name, pre=None):
    q = Q(BIN, os.path.join(ROOT, name))
    q.start("a", ["--audit"])
    q.start("b")
    if pre:
        pre(q)
    return q


def audit_log_lines(q):
    out = []
    for l in q.stderr("a").splitlines():
        if "audit" in l:
            out.append(re.sub(r"\d+", "<n>", l.split("coagentd: ", 1)[-1]))
    return out


def end_both(q, case, step):
    ra = q.ctl("a", "end")
    time.sleep(1.0)
    rb = q.ctl("b", "end")
    emit(case, step + " end replies (a, b)", [ra.get("ok"), rb.get("ok"), (rb.get("error") or {}).get("code")])
    time.sleep(1.0)


def creation_case(case, prepare, fix, unfix):
    q = new_q(case)
    try:
        entry = os.path.join(q.dir("a"), "audit")
        prepare(entry)
        q.pair("a", "b")
        emit(case, "after pairing status.audit", audit(q))
        send(q, case, "send 1", "QAN one")
        emit(case, "after send status.audit", audit(q))
        seal(q, case, "audit_seal")
        emit(case, "status again 1", audit(q))
        emit(case, "status again 2", audit(q))
        send(q, case, "send 2", "QAN two")
        emit(case, "after send 2 status.audit", audit(q))
        emit(case, "outbox", json.load(open(os.path.join(q.dir("a"), "outbox.json"))) if os.path.exists(os.path.join(q.dir("a"), "outbox.json")) else None)
        emit(case, "stderr audit lines (before restart)", audit_log_lines(q))
        # restart after the creation failure
        q.stop("a")
        q.start("a", ["--audit"])
        time.sleep(1.0)
        emit(case, "restarted status.audit", audit(q))
        send(q, case, "send after restart", "QAN three")
        seal(q, case, "audit_seal after restart")
        emit(case, "restarted status.audit again", audit(q))
        lines = audit_log_lines(q)
        emit(case, "stderr audit lines (all)", lines)
        emit(case, "log created line count", sum("audit log created" in l for l in lines))
        emit(case, "missing-or-empty line count", sum("missing or empty" in l for l in lines))
        emit(case, "audit dir listing", sorted(os.listdir(entry)) if os.path.isdir(entry) else "not a dir")
        # S-8 (1): end and pair again with the cause still there
        end_both(q, case, "S-8(1)")
        emit(case, "S-8(1) after end status.audit", audit(q))
        q.pair("a", "b")
        emit(case, "S-8(1) paired again, cause kept: status.audit", audit(q))
        send(q, case, "S-8(1) send", "QAN four")
        # S-8 (2): end, remove the cause, pair again
        end_both(q, case, "S-8(2)")
        fix(entry)
        q.pair("a", "b")
        emit(case, "S-8(2) paired again, cause removed: status.audit", audit(q))
        send(q, case, "S-8(2) send", "QAN five")
        seal(q, case, "S-8(2) audit_seal")
        lines = audit_log_lines(q)
        emit(case, "S-8 log created line count", sum("audit log created" in l for l in lines))
        emit(case, "S-8 stderr audit lines (last 6)", lines[-6:])
    finally:
        try:
            unfix(os.path.join(q.dir("a"), "audit"))
        except Exception as e:
            emit(case, "unfix error", repr(e))
        emit(case, "left processes", q.cleanup())


def mk_0755(e):
    os.mkdir(e); os.chmod(e, 0o755)


def mk_file(e):
    open(e, "wb").write(b"not a directory"); os.chmod(e, 0o600)


def fix_0755(e):
    os.chmod(e, 0o700)


def fix_file(e):
    os.rename(e, e + ".moved")  # never delete: move aside


def mk_uchg(e):
    os.mkdir(e); os.chmod(e, 0o700)
    subprocess.run(["chflags", "uchg", e], check=True)
    flags_set.append(e)
    emit("create_uchg", "flag set (ls -lOd)", subprocess.run(["ls", "-lOd", e], capture_output=True).stdout.decode().strip())


def fix_uchg(e):
    if os.path.isdir(e):
        subprocess.run(["chflags", "nouchg", e], check=True)
        emit("create_uchg", "flag cleared (ls -lOd)", subprocess.run(["ls", "-lOd", e], capture_output=True).stdout.decode().strip())


def paired(case):
    q = new_q(case)
    q.pair("a", "b")
    return q


def chmod_rel(q, rel, m):
    os.chmod(os.path.join(folder(q), rel), m)


def nothing_case(case):
    q = paired(case)
    try:
        if case == "n_i":          # send, seal, second seal
            send(q, case, "send", "QAN i")
            seal(q, case, "seal 1"); store(q, case, "after seal 1")
            seal(q, case, "seal 2 (nothing new)"); store(q, case, "after seal 2")
        elif case == "n_ii":       # send, store/ 0500, refused send, seal
            send(q, case, "send", "QAN ii")
            store(q, case, "before")
            chmod_rel(q, "store", 0o500)
            try:
                send(q, case, "send (store 0500)", "QAN ii refused")
                seal(q, case, "seal (store 0500)")
            finally:
                chmod_rel(q, "store", 0o700)
            store(q, case, "after, rights back")
            send(q, case, "send after rights back", "QAN ii after")
            seal(q, case, "seal after rights back"); store(q, case, "after the next seal")
        elif case == "n_iii":      # seal right after pairing, no send
            store(q, case, "fresh")
            seal(q, case, "seal with nothing ever sent"); store(q, case, "after")
            seal(q, case, "seal again"); store(q, case, "after 2")
        elif case == "n_iv":       # send, seal, restart, seal with nothing new
            send(q, case, "send", "QAN iv")
            seal(q, case, "seal 1")
            q.stop("a"); q.start("a", ["--audit"]); time.sleep(1.0)
            emit(case, "restarted status.audit", audit(q))
            seal(q, case, "seal after restart (nothing new)"); store(q, case, "after")
        elif case == "n_v":        # store/ 0500 with NO send since the last seal
            send(q, case, "send", "QAN v")
            seal(q, case, "seal 1"); store(q, case, "after seal 1")
            chmod_rel(q, "store", 0o500)
            try:
                seal(q, case, "seal (store 0500, nothing new)")
            finally:
                chmod_rel(q, "store", 0o700)
            store(q, case, "after, rights back")
        elif case in ("n_vi", "n_vii"):  # anchors/ or archive/ 0500 before a seal that follows a send
            rel = "anchors" if case == "n_vi" else "archive"
            send(q, case, "send", "QAN " + case)
            store(q, case, "before")
            chmod_rel(q, rel, 0o500)
            try:
                seal(q, case, f"seal ({rel} 0500)")
            finally:
                chmod_rel(q, rel, 0o700)
            store(q, case, "after, rights back")
            seal(q, case, "seal after rights back"); store(q, case, "after the next seal")
        emit(case, "stderr audit lines", audit_log_lines(q))
    finally:
        emit(case, "left processes", q.cleanup())


for c in CASES:
    if c == "create_0755":
        creation_case(c, mk_0755, fix_0755, lambda e: None)
    elif c == "create_file":
        creation_case(c, mk_file, fix_file, lambda e: None)
    elif c == "create_uchg":
        creation_case(c, mk_uchg, fix_uchg, fix_uchg)
    else:
        nothing_case(c)
emit("all", "flags set", flags_set)
