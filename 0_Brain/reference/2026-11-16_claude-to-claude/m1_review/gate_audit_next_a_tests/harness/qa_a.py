# property (a): hashes, prefix/run checks, bodies, dark names. usage: python3 -B qa_a.py <clone>
import hashlib, re, subprocess, sys
C = sys.argv[1]; B = "5e11609cee1cb483bd006547e9092d49522691cc"; H = "d79ae1ca194fbe354ca8be594b9c76325f1b6eb0"
def show(sha, p):
    r = subprocess.run(["git", "-C", C, "show", f"{sha}:{p}"], capture_output=True)
    return r.stdout if r.returncode == 0 else None
D = "crates/coagent-daemon/tests/"
want = {"gate/gate_attacks.rs":"b0f8d6b2bc2869a4","gate/gr2.rs":"caee212babc8072b","gate/gr3.rs":"eddd91ae98da52dc","gate/gr4.rs":"bf8f2999dc657817","gate/gate_hostile/mod.rs":"fa18b0bd9501b4e9","gate_r2.rs":"a1944e0c65afb1c3","gate_r3.rs":"17cfcca984130c79","gate_r4.rs":"a2ca92a68cc5e433","gate_r5_model.rs":"022f47049bce6688","gate_r6_model.rs":"755820e391466664","gate_r6_model_wrapper.rs":"2fb203a07390d43c","gate_return.rs":"d2ca677d7409133b","common/mod.rs":"08ed3f585cf09a22",
 "release_audit.rs":"1ee5785a1412318d","ipc.rs":"7ae8babc5d652f68","dn_help.rs":"2cd8ee5f41e8c1b3","aw_answers.rs":"9146d9280a08694e","aw_lifecycle.rs":"08ceedaa2dad16d4","aw_off.rs":"0e22f50b73bb3120","aw_peer.rs":"f5a4a3635845e6d4","aw_record.rs":"92ff8c92428441e7","aw_seal.rs":"4c8791c73a788f1f","aw_util.rs":"0f797bdc91d2d53b"}
EMPTY = hashlib.sha256(b"").hexdigest()[:16]
bad = 0
print("== protected/kept sha256[:16] base | head | brief")
for p, w in want.items():
    hb = show(B, D+p); hh = show(H, D+p)
    if hb is None or hh is None: print("MISSING", p); bad += 1; continue
    sb = hashlib.sha256(hb).hexdigest()[:16]; sh = hashlib.sha256(hh).hexdigest()[:16]
    ok = sb == sh == w and sb != EMPTY
    bad += not ok
    print(f"{'OK ' if ok else 'BAD'} {p} {sb} {sh} {w}")
print("rows", len(want), "bad", bad, "empty-hash", EMPTY)
print("control missing path:", show(B, D+"an_after.rs") is None and "an_after.rs at base: git show fails (reported, not hashed)")
# M0 prefix, BACKLOG runs
for p in ["docs/M0-OUTCOMES.md", "BACKLOG.md", "crates/coagent-daemon/build.rs", "scripts/red-controls-daemon.sh", D+"aw_disk.rs"]:
    b, h = show(B, p), show(H, p)
    print(f"prefix {p}: {h.startswith(b)}")
def runs(p):
    b = show(B, p).decode().split("\n"); h = show(H, p).decode().split("\n")
    i = 0; added = []; 
    for j, line in enumerate(h):
        if i < len(b) and line == b[i]: i += 1
        else: added.append(j+1)
    rr = []
    for n in added:
        if rr and rr[-1][1] == n-1: rr[-1][1] = n
        else: rr.append([n, n])
    return i == len(b), len(added), rr, h
for p in ["BACKLOG.md", D+"aw_disk.rs", "crates/coagent-daemon/build.rs", "scripts/red-controls-daemon.sh"]:
    kept, n, rr, h = runs(p)
    print(f"runs {p}: every base line kept in order={kept}; added {n}; runs {rr}")
    for a, z in rr: print(f"   before run {a}: {h[a-2][:90]!r}  after: {(h[z] if z < len(h) else "<EOF>")[:90]!r}")
