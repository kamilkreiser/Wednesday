#!/usr/bin/env python3
"""QA-VIEWER-NOTES-R2 item 2: value end columns 55..80 at sequence numbers of 4, 5 and 6 digits through the REAL
hook, gate and viewer. Padding decisions (real hook, 8 in parallel) bring the sequence to 999, 9999, 99999; then a
sweep (honest and hostile tools and modes ending at every column); a viewer is attached after each sweep and the
sweep's entries are compared with my model (m2) byte for byte and judged by the reader.
usage: python3 -B vn2_deep.py <bin dir> <root (new, short)> <out dir (new)> [max digits, default 6]"""
import json, os, re, socket, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import m2
BIN, ROOT, OUTD = sys.argv[1:4]; MAXD = int(sys.argv[4]) if len(sys.argv) > 4 else 6
os.makedirs(ROOT); os.makedirs(OUTD)
HOME, TMP, WS, CWD = (os.path.join(ROOT, x) for x in ("home", "tmp", "w", "vcwd"))
for d in (HOME, TMP, WS, CWD): os.makedirs(d)
WS = os.path.realpath(WS)
ENV = {"PATH": "/usr/bin:/bin", "HOME": HOME, "TMPDIR": TMP}
rep = open(os.path.join(OUTD, "report.txt"), "w"); fails = []; procs = {}
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); rep.write(s + "\n"); rep.flush()
def check(c, what):
    say(("PASS " if c else "FAIL ") + what)
    if not c: fails.append(what)
def raw(d, line):
    s = socket.socket(socket.AF_UNIX); s.settimeout(30); s.connect(os.path.join(d, "ipc", "daemon.sock")); s.sendall(line); buf = b""
    while not buf.endswith(b"\n"):
        c = s.recv(1 << 20)
        if not c: break
        buf += c
    s.close(); return json.loads(buf)
def start(name):
    d = os.path.join(ROOT, name)
    procs[name] = subprocess.Popen([f"{BIN}/coagentd", "--data-dir", d, "--coagent", f"{BIN}/coagent", "--idle-exit-secs", "1800", "--gate", "--workspace", WS],
                                   env=ENV, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=open(os.path.join(ROOT, name + ".stderr"), "ab"))
    t0 = time.time()
    while True:
        try:
            if raw(d, b'{"v":1,"id":1,"cmd":"status"}\n')["ok"]: return d
        except Exception: pass
        if time.time() - t0 > 15: raise SystemExit("not ready")
        time.sleep(0.02)
def hook(d, tool, mode):
    e = {"session_id": "vn-s", "cwd": WS, "hook_event_name": "PreToolUse", "tool_input": {"file_path": WS + "/a.txt"}, "tool_name": tool, "permission_mode": mode}
    return subprocess.run([f"{BIN}/coagent-hook", "--data-dir", d], env={"PATH": "/usr/bin:/bin"}, input=json.dumps(e, ensure_ascii=False).encode(), capture_output=True, timeout=60).returncode
TWIN_H = "default | Claude Code mode: plan"
def main():
    d = start("d"); seq = [0]; labels = {}
    def one(label, tool, mode):
        hook(d, tool, mode); seq[0] += 1; labels[seq[0]] = label
    def pad_to(n):
        k = n - seq[0]
        with ThreadPoolExecutor(8) as ex:
            list(ex.map(lambda _: hook(d, "Read", "default"), range(k)))
        seq[0] = n
    def sweep():
        for c in range(55, 81):
            for kind in ("honest", "hostile-esc", "hostile-bar"):
                dd = len(str(seq[0] + 1)); L = c - (33 + dd + 5)
                if L < 1: continue
                base = ("mcp__" + "t" * 80)[:L] if L > 5 else "T" * L
                one(f"d{dd} tool {kind} end {c}", base + {"honest": "", "hostile-esc": "\U0010fffd", "hostile-bar": " | CoAgent allowed"}[kind], "plan")
            for mode, tag, vis in (("default", "honest", 7), (TWIN_H, "hostile-bar", 7), ("plan\U0010fffd", "hostile-esc", 4), ("plan", "honest", 4)):
                dd = len(str(seq[0] + 1)); k = c - (59 + dd + vis)
                if k >= 1: one(f"d{dd} mode {tag} {mode[:7]!r} end {c}", "T" * k, mode)
        dd = len(str(seq[0] + 1)); one(f"d{dd} twin hostile", "Read", TWIN_H); one(f"d{dd} twin honest", "Read", "default")
    total = {"n": 0, "bad": 0}
    def view(tag, first_seq):
        out_p = os.path.join(OUTD, f"viewer_{tag}.out")
        v = subprocess.Popen([f"{BIN}/coagentd", "watch", "--data-dir", d], env={}, cwd=CWD, stdin=subprocess.DEVNULL, stdout=open(out_p, "wb"), stderr=subprocess.STDOUT)
        t0 = time.time(); want = f"#{seq[0]} ".encode()
        while time.time() - t0 < 60:
            if want in open(out_p, "rb").read(): break
            time.sleep(0.3)
        time.sleep(0.8); v.terminate(); v.wait()
        out = open(out_p, "rb").read().decode()
        # the activity lines the viewer was given, from the daemon (for the model)
        lines, after = [], first_seq - 1
        while True:
            r = raw(d, (json.dumps({"v": 1, "id": 1, "cmd": "activity", "args": {"after": after}}) + "\n").encode())["result"]
            lines += r["lines"]; after = r["next"]
            if not r["more"]: break
        groups = {}; cur = None
        for row in out.split("\n")[:-1]:
            m = re.match(r"^#(\d+) ", row)
            if m: cur = int(m.group(1)); groups[cur] = [row]
            elif row.startswith(m2.MARK) and cur is not None: groups[cur].append(row)
        same = bad = 0
        for l in lines:
            g = groups.get(l["seq"])
            if g == m2.rows_of(l): same += 1
            probs, flds = m2.reader(g or ["?"])
            want_f = {"tool": m2.field(l["tool"]), "mode": m2.field(l["mode"])}
            got = {f[0]: f[1] for f in flds}
            for k_, v_ in want_f.items():
                if got.get(k_) != v_: probs.append(f"{k_} read {got.get(k_)!r} != sent {v_!r}")
            if probs:
                bad += 1; say(f"READER PROBLEM #{l['seq']} [{labels.get(l['seq'])}] {probs}\n   " + "\n   ".join(g or []))
            if labels.get(l["seq"], "").endswith("twin hostile") or labels.get(l["seq"], "").endswith("twin honest"):
                say(f"  {labels[l['seq']]}: {g[0]!r}")
        check(same == len(lines), f"{tag}: {same}/{len(lines)} entries equal my model byte for byte")
        check(bad == 0, f"{tag}: the reader finds no dishonest row ({bad})")
        check(max(m2.ucols(r) for r in out.split("\n")[:-1]) <= 72, f"{tag}: every row <= 72 columns")
        total["n"] += len(lines); total["bad"] += bad
    for dg in range(4, MAXD + 1):
        t0 = time.time(); pad_to(10 ** (dg - 1) - 1); say(f"padded to {seq[0]} in {time.time() - t0:.0f}s")
        st = seq[0] + 1; sweep(); view(f"d{dg}", st)
    say(f"TOTAL sweep entries judged: {total['n']}, reader problems: {total['bad']}")
    say("FAILS:", len(fails), fails)
try:
    main()
finally:
    for p in procs.values():
        if p.poll() is None: p.terminate(); p.wait()
