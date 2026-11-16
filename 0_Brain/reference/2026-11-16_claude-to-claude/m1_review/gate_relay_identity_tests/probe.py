#!/usr/bin/env python3
"""QA gate driver for `coagent relay --identity-file / --identity-stdin` (M1 RELAY-IDENTITY).

Every relay listens on 127.0.0.1 with an ephemeral port (or a port this script itself just took
from the OS on 127.0.0.1). Every file it makes lives under the scratch root given on the command
line. Prints one line per probe; the caller saves the output.

usage: probe.py <scratch-root> <head-binary> <main-binary> <pin-client-binary> [section ...]
"""
import base64, hashlib, os, pty, random, select, signal, socket, stat, struct, subprocess, sys, time

ROOT, HEAD, MAIN, CLIENT = sys.argv[1:5]
SECTIONS = set(sys.argv[5:]) or {"default", "usage", "file", "modes", "acl", "kill", "blob", "stdin", "pin", "scan"}
HDR = b"coagent-relay-identity v1\n"
ALL_OUTPUT = []   # (label, text) for the key scan
KEYS = []         # every key seen in a blob this run
results = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    results.append(s)


_n = [0]


def fresh_dir(tag, mode=0o700):
    _n[0] += 1
    d = os.path.join(ROOT, "p", f"{os.getpid()}-{_n[0]:04d}-{tag}")
    os.makedirs(d)
    os.chmod(d, mode)
    return d


def env_for(base):
    """cwd, TMPDIR and HOME all inside the scratch root, empty."""
    cwd = os.path.join(base, "cwd"); tmp = os.path.join(base, "tmp"); home = os.path.join(base, "home")
    for d in (cwd, tmp, home):
        os.makedirs(d, exist_ok=True); os.chmod(d, 0o700)
    env = {"PATH": "/usr/bin:/bin", "TMPDIR": tmp + "/", "HOME": home, "LANG": "C"}
    return cwd, env


def listing(d):
    out = []
    for dp, dn, fn in os.walk(d):
        for x in dn + fn:
            out.append(os.path.relpath(os.path.join(dp, x), d))
    return sorted(out)


def split_blob(b):
    h = len(HDR)
    cl = struct.unpack(">I", b[h:h + 4])[0]
    cert = b[h + 4:h + 4 + cl]
    k0 = h + 4 + cl
    kl = struct.unpack(">I", b[k0:k0 + 4])[0]
    return cert, b[k0 + 4:k0 + 4 + kl]


def join_blob(cert, key):
    return HDR + struct.pack(">I", len(cert)) + cert + struct.pack(">I", len(key)) + key


def note_key_from_file(p):
    try:
        with open(p, "rb") as f:
            b = f.read()
        if b.startswith(HDR):
            KEYS.append(split_blob(b)[1])
    except Exception:
        pass


def run(binary, args, base=None, stdin=None, stdin_bytes=None, timeout=15, keep_open=False,
        umask=None, label="", lsof=False, hold=0.0):
    """Start the binary; if it prints the stop hint, optionally lsof it, then SIGINT it.
    Returns dict(rc, out, err, started, elapsed, lsof)."""
    if base is None:
        base = fresh_dir("run")
    cwd, env = env_for(base) if not isinstance(base, tuple) else base
    pre = None
    if umask is not None:
        def pre():
            os.umask(umask)
    stdin_arg = subprocess.DEVNULL if stdin is None and stdin_bytes is None else (subprocess.PIPE if stdin_bytes is not None else stdin)
    t0 = time.monotonic()
    p = subprocess.Popen([binary] + args, cwd=cwd, env=env, stdin=stdin_arg, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, preexec_fn=pre)
    if stdin_bytes is not None:
        try:
            p.stdin.write(stdin_bytes)
            p.stdin.flush()
            if not keep_open:
                p.stdin.close()
        except BrokenPipeError:
            pass
    out = b""; err = b""; started = False; lsof_txt = ""
    fds = {p.stdout.fileno(): "o", p.stderr.fileno(): "e"}
    deadline = t0 + timeout
    while fds and time.monotonic() < deadline:
        r, _, _ = select.select(list(fds), [], [], 0.05)
        for fd in r:
            chunk = os.read(fd, 65536)
            if not chunk:
                del fds[fd]; continue
            if fds[fd] == "o":
                out += chunk
            else:
                err += chunk
        if not started and b"Press Ctrl-C" in out:
            started = True
            if hold:
                time.sleep(hold)
            if lsof:
                lsof_txt = subprocess.run(["/usr/sbin/lsof", "-n", "-P", "-p", str(p.pid)], capture_output=True, text=True).stdout
            if not keep_open:
                p.send_signal(signal.SIGINT)
        if p.poll() is not None and not fds:
            break
    if p.poll() is None:
        p.send_signal(signal.SIGINT)
        try:
            p.wait(5)
        except subprocess.TimeoutExpired:
            p.kill(); p.wait()
    # drain
    for fd, k in list(fds.items()):
        try:
            while True:
                c = os.read(fd, 65536)
                if not c:
                    break
                if k == "o":
                    out += c
                else:
                    err += c
        except OSError:
            pass
    if stdin_bytes is not None and keep_open:
        try:
            p.stdin.close()
        except Exception:
            pass
    el = time.monotonic() - t0
    o = out.decode(errors="replace"); e = err.decode(errors="replace")
    ALL_OUTPUT.append((label or " ".join(args), o + "\n" + e))
    return {"rc": p.returncode, "out": o, "err": e, "started": started, "elapsed": el, "lsof": lsof_txt,
            "listened": ("url: " in o) or ("relay listening" in e)}


def fp_of(out):
    for l in out.splitlines():
        if l.startswith("fingerprint: "):
            return l.split()[1]
    return None


def url_of(out):
    for l in out.splitlines():
        if l.startswith("url: "):
            return l.split()[1]
    return None


def prefixes(out):
    ps = []
    for l in out.splitlines():
        if l.startswith(" ") or not l.strip():
            continue
        ps.append(l.split(":")[0] if ":" in l[:30] else l[:20])
    return ps


def fstate(p):
    st = os.lstat(p)
    with open(p, "rb") as f:
        h = hashlib.sha256(f.read()).hexdigest()
    return (h, oct(st.st_mode), st.st_mtime_ns, st.st_ino, st.st_uid, st.st_nlink)


def short(r):
    msg = [l for l in r["err"].splitlines() if l.startswith("coagent relay:")]
    return f"rc={r['rc']} listened={r['listened']} t={r['elapsed']:.2f}s msg={msg[:1]}"


def file_id_line(r):
    return [l for l in r["out"].splitlines() if l.startswith("identity:")]


def make_identity(d, name="relay.identity"):
    """Use the head binary itself to create a valid identity file at d/name; return (path, fp)."""
    p = os.path.join(d, name)
    r = run(HEAD, ["--listen", "127.0.0.1:0", "relay", "--identity-file", p][2:] if False else ["relay", "--identity-file", p], label="make")
    assert r["started"], r
    note_key_from_file(p)
    return p, fp_of(r["out"])


# ---------------------------------------------------------------- sections

def sec_default():
    log("== DEFAULT: neither option, main vs head; 3 starts each in empty cwd/TMPDIR/HOME")
    for name, b in (("main", MAIN), ("head", HEAD)):
        fps = []
        for i in range(3):
            base = fresh_dir(f"default-{name}")
            r = run(b, ["relay"], base=base, lsof=(i == 0), label=f"default-{name}")
            fps.append(fp_of(r["out"]))
            left = listing(base)
            log(f"DEFAULT {name} run{i}: rc={r['rc']} prefixes={prefixes(r['out'])} identity_line={file_id_line(r)} leftover={[x for x in left if x not in ('cwd','tmp','home')]}")
            if i == 0:
                regs = [l for l in r["lsof"].splitlines() if " REG " in l or " DIR " in l]
                kinds = sorted(set(l.split()[3] + ":" + l.split()[-1].rsplit('/', 1)[-1] for l in regs))
                log(f"DEFAULT {name} lsof REG/DIR entries: {len(regs)} -> {kinds}")
                log(f"DEFAULT {name} stdout lines (verbatim shape):")
                for l in r["out"].splitlines():
                    log("   | " + (l if not l.startswith(("fingerprint:", "url:", "address:", "coagent relay:", "invite candidate:")) else l.split(':')[0] + ": <...>"))
        log(f"DEFAULT {name} fingerprints distinct: {len(set(fps)) == 3} {fps}")


def sec_usage():
    log("== USAGE: exit codes main vs head")
    cases = [["relay", "--listen"], ["relay", "--bogus"], ["relay", "--status-secs", "x"], ["relay", "--listen", "nope"],
             ["frobnicate"], ["--version", "extra"], ["relay", "--listen", "0.0.0.0:0"], ["relay", "--identity-file"],
             ["relay", "--identity-file", "a", "--identity-stdin"], ["relay", "--identity-stdin", "--identity-file", "a"],
             ["relay", "--identity-stdin", "--identity-stdin"], ["relay", "--identity-file", "a", "--identity-file", "b"],
             ["relay", "--identity-file", "--identity-stdin"], ["relay", "--identity-file", ""], ["relay", "--identity-file", "-x"],
             ["relay", "--identity-file=a"]]
    for c in cases:
        base = fresh_dir("usage")
        rm = run(MAIN, c, base=fresh_dir("usage-main"), timeout=5, label="usage-main")
        rh = run(HEAD, c, base=base, timeout=5, label="usage-head")
        log(f"USAGE {c}: main rc={rm['rc']} listened={rm['listened']} | head rc={rh['rc']} listened={rh['listened']} files={listing(base)[3:] if len(listing(base))>3 else []} err={rh['err'].strip().splitlines()[:1]}")


def sec_file():
    log("== FILE: creation, reload, refusals")
    # umask variants
    for um in (0o000, 0o077, 0o022, 0o277):
        d = fresh_dir(f"umask{um:o}")
        p = os.path.join(d, "relay.identity")
        r1 = run(HEAD, ["relay", "--identity-file", p], umask=um, label="create")
        note_key_from_file(p)
        st = os.lstat(p) if os.path.lexists(p) else None
        log(f"FILE create umask {um:03o}: {short(r1)} line={file_id_line(r1)} mode={oct(st.st_mode) if st else None} uid_ok={st and st.st_uid == os.getuid()} dir={listing(d)}")
        if st:
            s0 = fstate(p)
            time.sleep(1.1)
            r2 = run(HEAD, ["relay", "--identity-file", p], label="load")
            s1 = fstate(p)
            log(f"FILE reload umask {um:03o}: {short(r2)} line={file_id_line(r2)} same_fp={fp_of(r1['out']) == fp_of(r2['out'])} file_unchanged={s0 == s1}")
    d = fresh_dir("refusals")
    good, gfp = make_identity(d)
    # symlink at path -> valid
    p = os.path.join(d, "link"); os.symlink(good, p)
    log("FILE symlink->valid:", short(run(HEAD, ["relay", "--identity-file", p])))
    # dangling symlink -> target must not be created
    p = os.path.join(d, "dangle"); tgt = os.path.join(d, "dangle-target"); os.symlink(tgt, p)
    r = run(HEAD, ["relay", "--identity-file", p])
    log("FILE dangling symlink:", short(r), "target created:", os.path.lexists(tgt))
    # symlink parent (DQ2)
    d2 = fresh_dir("realparent"); g2, fp2 = make_identity(d2)
    lp = os.path.join(fresh_dir("linkparent"), "via"); os.symlink(d2, lp)
    r = run(HEAD, ["relay", "--identity-file", os.path.join(lp, "relay.identity")])
    log("FILE parent is a symlink to a 0700 dir (DQ2):", short(r), file_id_line(r), "same fp:", fp_of(r["out"]) == fp2)
    # parent symlink to an open dir
    d3 = fresh_dir("openparent", 0o755)
    lp2 = os.path.join(fresh_dir("linkparent2"), "via"); os.symlink(d3, lp2)
    log("FILE parent symlink to 0755 dir:", short(run(HEAD, ["relay", "--identity-file", os.path.join(lp2, "x")])), "created:", listing(d3))
    # FIFO at path
    p = os.path.join(d, "fifo"); os.mkfifo(p, 0o600)
    log("FIFO at path:", short(run(HEAD, ["relay", "--identity-file", p], timeout=10)))
    # directory at path
    p = os.path.join(d, "adir"); os.mkdir(p, 0o700)
    log("FILE directory at path:", short(run(HEAD, ["relay", "--identity-file", p])))
    # trailing slash / dot forms
    for suffix in ("/", "/."):
        log(f"FILE path {good!r}+{suffix!r}:", short(run(HEAD, ["relay", "--identity-file", good + suffix])))
    # device / root-owned parent
    log("FILE /dev/null:", short(run(HEAD, ["relay", "--identity-file", "/dev/null"])))
    # (a Unix socket at the path takes the same NotRegular branch as the FIFO; the scratch path is
    # longer than the AF_UNIX limit, so it is not run.)


def sec_file2():
    d = fresh_dir("refusals2")
    good, gfp = make_identity(d)
    # hard link to the valid file
    p = os.path.join(d, "hardlink"); os.link(good, p)
    r = run(HEAD, ["relay", "--identity-file", p])
    log("FILE hard link (nlink=2):", short(r), file_id_line(r), "same fp:", fp_of(r["out"]) == gfp)
    # over cap
    p = os.path.join(d, "big"); open(p, "wb").write(b"\0" * 16385); os.chmod(p, 0o600)
    log("FILE size cap+1:", short(run(HEAD, ["relay", "--identity-file", p])))
    p = os.path.join(d, "atcap"); open(p, "wb").write(b"\0" * 16384); os.chmod(p, 0o600)
    log("FILE size exactly cap (garbage):", short(run(HEAD, ["relay", "--identity-file", p])))
    p = os.path.join(d, "huge"); f = open(p, "wb"); f.truncate(1 << 30); f.close(); os.chmod(p, 0o600)
    log("FILE sparse 1 GiB:", short(run(HEAD, ["relay", "--identity-file", p])))
    # existing invalid file never overwritten
    p = os.path.join(d, "invalid"); open(p, "wb").write(b"-----BEGIN PRIVATE KEY-----\nnot\n"); os.chmod(p, 0o600)
    s0 = fstate(p); time.sleep(1.1)
    r = run(HEAD, ["relay", "--identity-file", p]); s1 = fstate(p)
    log("FILE existing invalid:", short(r), "unchanged:", s0 == s1)
    # empty file
    p = os.path.join(d, "empty"); open(p, "wb").close(); os.chmod(p, 0o600)
    log("FILE empty file:", short(run(HEAD, ["relay", "--identity-file", p])), "size after:", os.path.getsize(p))
    # group-readable valid identity: refused, not repaired
    d4 = fresh_dir("grp"); g4, _ = make_identity(d4); os.chmod(g4, 0o640)
    s0 = fstate(g4); time.sleep(1.1)
    r = run(HEAD, ["relay", "--identity-file", g4]); s1 = fstate(g4)
    log("FILE group-readable valid:", short(r), "unchanged incl mode:", s0 == s1, s1[1])
    # mismatched pair in a file
    d5 = fresh_dir("mismatch"); a, _ = make_identity(d5, "a"); b, _ = make_identity(d5, "b")
    ca, _ = split_blob(open(a, "rb").read()); _, kb = split_blob(open(b, "rb").read())
    p = os.path.join(d5, "mixed"); open(p, "wb").write(join_blob(ca, kb)); os.chmod(p, 0o600)
    log("FILE cert A + key B:", short(run(HEAD, ["relay", "--identity-file", p])))
    # 0400 and 0000 files
    for m in (0o400, 0o200, 0o000):
        d6 = fresh_dir(f"m{m:o}"); g6, _ = make_identity(d6); os.chmod(g6, m)
        r = run(HEAD, ["relay", "--identity-file", g6]); os.chmod(g6, 0o600)
        log(f"FILE mode {m:04o}:", short(r), file_id_line(r))
    # parent 0500 (no write) and creation into it
    d7 = fresh_dir("ro-parent", 0o500)
    log("FILE create in 0500 parent:", short(run(HEAD, ["relay", "--identity-file", os.path.join(d7, "x")])), listing(d7))
    os.chmod(d7, 0o700)
    # relative path in an open cwd and in a 0700 cwd
    base = fresh_dir("relcwd"); cwd, env = env_for(base); os.chmod(cwd, 0o755)
    log("FILE relative path, cwd 0755:", short(run(HEAD, ["relay", "--identity-file", "relay.identity"], base=(cwd, env))), listing(cwd))
    os.chmod(cwd, 0o700)
    r = run(HEAD, ["relay", "--identity-file", "relay.identity"], base=(cwd, env))
    log("FILE relative path, cwd 0700:", short(r), file_id_line(r), listing(cwd)); note_key_from_file(os.path.join(cwd, "relay.identity"))
    # long name: final name fits NAME_MAX but temp name does not
    d8 = fresh_dir("longname"); nm = "x" * 240
    log("FILE 240-char name:", short(run(HEAD, ["relay", "--identity-file", os.path.join(d8, nm)])), [len(x) for x in listing(d8)])
    # bind fails after create (DQ3)
    d9 = fresh_dir("bindfail"); s = socket.socket(); s.bind(("127.0.0.1", 0)); s.listen(1); port = s.getsockname()[1]
    p = os.path.join(d9, "relay.identity")
    r = run(HEAD, ["relay", "--listen", f"127.0.0.1:{port}", "--identity-file", p])
    s.close(); note_key_from_file(p)
    log("FILE bind fails after create (DQ3):", short(r), "err:", r["err"].strip().splitlines(), "dir:", listing(d9))
    # bind refused (non-loopback without allow) after create
    d10 = fresh_dir("nonloop"); p = os.path.join(d10, "relay.identity")
    r = run(HEAD, ["relay", "--listen", "0.0.0.0:0", "--identity-file", p])
    log("FILE --listen 0.0.0.0 without allow, new file (nothing bound):", short(r), "dir:", listing(d10)); note_key_from_file(p)


def sec_modes():
    log("== MODES: every permission bit on the file (base 0600) and on the parent (base 0700)")
    bits = [0o4000, 0o2000, 0o1000, 0o040, 0o020, 0o010, 0o004, 0o002, 0o001]
    for bit in bits:
        d = fresh_dir("fbit"); g, _ = make_identity(d); os.chmod(g, 0o600 | bit)
        actual = oct(os.lstat(g).st_mode & 0o7777)
        r = run(HEAD, ["relay", "--identity-file", g])
        log(f"MODE file 0600|{bit:04o} (actual {actual}): {'LOADED' if r['listened'] else 'refused'} {short(r)}")
        os.chmod(g, 0o600)
    for bit in bits:
        d = fresh_dir("dbit"); g, _ = make_identity(d); os.chmod(d, 0o700 | bit)
        actual = oct(os.lstat(d).st_mode & 0o7777)
        r = run(HEAD, ["relay", "--identity-file", g])
        d2 = fresh_dir("dbitc", 0o700 | bit); r2 = run(HEAD, ["relay", "--identity-file", os.path.join(d2, "n")])
        log(f"MODE dir 0700|{bit:04o} (actual {actual}): load {'LOADED' if r['listened'] else 'refused'}; create {'CREATED' if r2['listened'] else 'refused'} {listing(d2)}")
        os.chmod(d, 0o700); os.chmod(d2, 0o700)


def sec_acl():
    log("== ACL (macOS): an ACL entry is not a mode bit")
    d = fresh_dir("acl-file"); g, _ = make_identity(d)
    c = subprocess.run(["/bin/chmod", "+a", "everyone allow read", g], capture_output=True, text=True)
    ls = subprocess.run(["/bin/ls", "-le", g], capture_output=True, text=True).stdout.strip().splitlines()
    r = run(HEAD, ["relay", "--identity-file", g])
    log(f"ACL file 'everyone allow read' (chmod rc={c.returncode} {c.stderr.strip()}): ls -le={ls} -> {'LOADED' if r['listened'] else 'refused'} {short(r)}")
    d = fresh_dir("acl-dir"); g, _ = make_identity(d)
    c = subprocess.run(["/bin/chmod", "+a", "everyone allow list,search,add_file,delete_child", d], capture_output=True, text=True)
    ls = subprocess.run(["/bin/ls", "-led", d], capture_output=True, text=True).stdout.strip().splitlines()
    r = run(HEAD, ["relay", "--identity-file", g])
    log(f"ACL dir 'everyone allow add_file,delete_child' (rc={c.returncode}): ls -led={ls} -> {'LOADED' if r['listened'] else 'refused'} {short(r)}")
    d = fresh_dir("acl-dir-create")
    subprocess.run(["/bin/chmod", "+a", "everyone allow list,search,add_file,delete_child", d], capture_output=True, text=True)
    r = run(HEAD, ["relay", "--identity-file", os.path.join(d, "n")])
    note_key_from_file(os.path.join(d, "n"))
    log(f"ACL dir create -> {'CREATED' if r['listened'] else 'refused'} {short(r)}")
    # inheritable ACL on the parent: does the relay's OWN new file come out readable by others?
    d = fresh_dir("acl-inherit")
    c = subprocess.run(["/bin/chmod", "+a", "everyone allow read,file_inherit", d], capture_output=True, text=True)
    p = os.path.join(d, "n")
    r = run(HEAD, ["relay", "--identity-file", p])
    note_key_from_file(p)
    ls = subprocess.run(["/bin/ls", "-le", p], capture_output=True, text=True).stdout.strip().splitlines() if os.path.exists(p) else []
    log(f"ACL inheritable 'everyone allow read,file_inherit' on parent (rc={c.returncode} {c.stderr.strip()}): create -> {'CREATED' if r['listened'] else 'refused'}; new file ls -le={ls}")
    r2 = run(HEAD, ["relay", "--identity-file", p])
    log(f"ACL inherited file reload -> {'LOADED' if r2['listened'] else 'refused'}")
    # xattr does not matter for access; record that one is tolerated
    d = fresh_dir("xattr"); g, _ = make_identity(d)
    subprocess.run(["/usr/bin/xattr", "-w", "com.example.gate", "1", g], capture_output=True)
    r = run(HEAD, ["relay", "--identity-file", g])
    log(f"XATTR file with a user xattr -> {'LOADED' if r['listened'] else 'refused'}")


def sec_kill(n=150):
    log(f"== KILL: SIGKILL a creating relay at a random moment, {n} times")
    stats = {"no_file": 0, "final_valid": 0, "final_partial": 0, "temp_left": 0, "final_nlink2": 0, "world_readable": 0}
    leftovers = []
    for i in range(n):
        d = fresh_dir("kill")
        p = os.path.join(d, "relay.identity")
        cwd, env = env_for(fresh_dir("killenv"))
        pr = subprocess.Popen([HEAD, "relay", "--identity-file", p], cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                              stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        time.sleep(random.uniform(0.0, 0.06))
        pr.kill(); pr.wait(); pr.stderr.close()
        names = os.listdir(d)
        for nm in names:
            st = os.lstat(os.path.join(d, nm))
            if st.st_mode & 0o077:
                stats["world_readable"] += 1
        tmps = [x for x in names if x != "relay.identity"]
        if tmps:
            stats["temp_left"] += 1; leftovers.append((i, tmps, [os.lstat(os.path.join(d, x)).st_size for x in tmps]))
            for x in tmps:
                note_key_from_file(os.path.join(d, x))
        if "relay.identity" in names:
            b = open(p, "rb").read(); note_key_from_file(p)
            try:
                c, k = split_blob(b); ok = join_blob(c, k) == b
            except Exception:
                ok = False
            stats["final_valid" if ok else "final_partial"] += 1
            if os.lstat(p).st_nlink > 1:
                stats["final_nlink2"] += 1
        else:
            stats["no_file"] += 1
    log("KILL stats:", stats)
    log("KILL leftovers (iter, names, sizes) first 10:", [(i, [t.split('-')[0] for t in ts], sz) for i, ts, sz in leftovers[:10]])


def sec_blob():
    log("== BLOB through both options")
    d = fresh_dir("blobsrc"); g, gfp = make_identity(d)
    blob = open(g, "rb").read()
    c, k = split_blob(blob)
    d2 = fresh_dir("blobsrc2"); g2, _ = make_identity(d2)
    c2, k2 = split_blob(open(g2, "rb").read())
    variants = {
        "valid": blob, "wrong header": b"hello" + blob[5:], "v2": blob.replace(b" v1\n", b" v2\n", 1),
        "CRLF": blob.replace(b" v1\n", b" v1\r\n", 1), "trailing byte": blob + b"\0", "empty cert": join_blob(b"", k),
        "empty key": join_blob(c, b""), "certA+keyB": join_blob(c, k2), "cap+1": blob + b"\0" * (16385 - len(blob)),
        "certlen ffffffff": blob[:len(HDR)] + b"\xff\xff\xff\xff" + blob[len(HDR) + 4:],
    }
    for name, b in variants.items():
        rs = run(HEAD, ["relay", "--identity-stdin"], stdin_bytes=b, label=f"blob-stdin-{name}")
        dd = fresh_dir("blobfile"); p = os.path.join(dd, "id"); open(p, "wb").write(b); os.chmod(p, 0o600)
        rf = run(HEAD, ["relay", "--identity-file", p], label=f"blob-file-{name}")
        log(f"BLOB {name:18}: stdin {short(rs)} fp_same={fp_of(rs['out']) == gfp if rs['listened'] else '-'} | file {short(rf)}")
    # truncation at every position through stdin (sampled every 7 bytes + boundaries)
    bad = 0; listened = 0; positions = sorted(set(list(range(0, len(blob), 7)) + [len(HDR) - 1, len(HDR), len(HDR) + 4, len(blob) - 1]))
    for n in positions:
        r = run(HEAD, ["relay", "--identity-stdin"], stdin_bytes=blob[:n], timeout=8, label="trunc")
        bad += r["rc"] == 0; listened += r["listened"]
    log(f"BLOB truncation via stdin at {len(positions)} positions: rc0={bad} listened={listened}")
    # RSA blob made with openssl, if present
    rsa = os.path.join(ROOT, "probe", "blobs", "rsa.blob")
    if os.path.exists(rsa):
        rb = open(rsa, "rb").read(); KEYS.append(split_blob(rb)[1])
        r = run(HEAD, ["relay", "--identity-stdin"], stdin_bytes=rb, label="rsa")
        log(f"BLOB RSA (openssl) via stdin: {short(r)} fp={fp_of(r['out'])} expected sha256:{hashlib.sha256(split_blob(rb)[0]).hexdigest()}")


def sec_stdin():
    log("== STDIN")
    d = fresh_dir("stdinsrc"); g, gfp = make_identity(d); blob = open(g, "rb").read()
    # valid via pipe, no files created anywhere
    base = fresh_dir("stdin-valid")
    r = run(HEAD, ["relay", "--identity-stdin"], base=base, stdin_bytes=blob)
    log(f"STDIN valid pipe: {short(r)} line={file_id_line(r)} fp_same={fp_of(r['out']) == gfp} files={listing(base)}")
    # valid from a regular file
    f = open(g, "rb"); r = run(HEAD, ["relay", "--identity-stdin"], stdin=f); f.close()
    log(f"STDIN regular file: {short(r)} fp_same={fp_of(r['out']) == gfp}")
    # /dev/null
    f = open("/dev/null", "rb"); r = run(HEAD, ["relay", "--identity-stdin"], stdin=f); f.close()
    log(f"STDIN /dev/null: {short(r)}")
    # fd 0 closed in the child
    cwd, env = env_for(fresh_dir("closed"))
    t0 = time.monotonic()
    pr = subprocess.run([HEAD, "relay", "--identity-stdin"], cwd=cwd, env=env, capture_output=True, text=True, timeout=20,
                        preexec_fn=lambda: os.close(0))
    ALL_OUTPUT.append(("closed", pr.stdout + pr.stderr))
    log(f"STDIN fd 0 closed: rc={pr.returncode} t={time.monotonic()-t0:.2f}s err={pr.stderr.strip().splitlines()[:1]}")
    # TTY
    for i in range(2):
        m, s = pty.openpty()
        r = run(HEAD, ["relay", "--identity-stdin"], stdin=s, timeout=20)
        os.close(m); os.close(s)
        log(f"STDIN tty run{i}: {short(r)}")
    # silent open pipe: deadline, 5 repeats
    times = []
    for i in range(5):
        r = run(HEAD, ["relay", "--identity-stdin"], stdin_bytes=b"", keep_open=True, timeout=30)
        times.append(round(r["elapsed"], 2))
        log(f"STDIN silent open pipe run{i}: {short(r)}")
    log(f"STDIN deadline elapsed seconds: {times} spread {min(times)}..{max(times)}")
    # valid blob but no EOF
    r = run(HEAD, ["relay", "--identity-stdin"], stdin_bytes=blob, keep_open=True, timeout=30)
    log(f"STDIN valid blob, pipe kept open: {short(r)}")
    # dribble: one byte per second (deadline is for the whole read)
    cwd, env = env_for(fresh_dir("dribble"))
    pr = subprocess.Popen([HEAD, "relay", "--identity-stdin"], cwd=cwd, env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    t0 = time.monotonic(); sent = 0
    try:
        while pr.poll() is None and time.monotonic() - t0 < 20:
            pr.stdin.write(blob[sent:sent + 1]); pr.stdin.flush(); sent += 1; time.sleep(0.5)
    except BrokenPipeError:
        pass
    pr.wait(10); o, e = pr.communicate()
    ALL_OUTPUT.append(("dribble", o.decode() + e.decode()))
    log(f"STDIN dribble 2 B/s: rc={pr.returncode} t={time.monotonic()-t0:.2f}s sent={sent} err={e.decode().strip().splitlines()[:1]}")
    # read accounting: stdin is a regular file shared with this process; its offset after exit = bytes read
    for size in (16384, 16385, 16386, 1 << 20, 64 << 20):
        p = os.path.join(fresh_dir("acct"), "in"); f = open(p, "wb"); f.write(b"A" * size); f.close()
        f = open(p, "rb")
        r = run(HEAD, ["relay", "--identity-stdin"], stdin=f)
        off = os.lseek(f.fileno(), 0, os.SEEK_CUR); f.close()
        log(f"STDIN accounting file of {size} bytes: {short(r)} bytes consumed by the relay = {off}")
    # endless pipe: count bytes the writer got into the pipe
    cwd, env = env_for(fresh_dir("flood"))
    pr = subprocess.Popen([HEAD, "relay", "--identity-stdin"], cwd=cwd, env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    os.set_blocking(pr.stdin.fileno(), False); wrote = 0; t0 = time.monotonic(); chunk = b"B" * 4096
    while time.monotonic() - t0 < 10:
        try:
            wrote += os.write(pr.stdin.fileno(), chunk)
        except BlockingIOError:
            if pr.poll() is not None:
                break
            time.sleep(0.01)
        except BrokenPipeError:
            break
    pr.wait(10); o, e = pr.communicate() if pr.stdout else (b"", b"")
    log(f"STDIN endless pipe: rc={pr.returncode} writer pushed {wrote} bytes before EPIPE/exit (pipe buffer included) err={e.decode().strip().splitlines()[:1]}")


def run_client(url, fp, expect):
    r = subprocess.run([CLIENT, "--exact", "gate_pin_client", "--nocapture"], env={**os.environ, "GATE_URL": url, "GATE_FP": fp, "GATE_EXPECT": expect},
                       capture_output=True, text=True, timeout=60)
    lines = [l for l in r.stdout.splitlines() if "GATE_CLIENT" in l]
    return r.returncode, lines


def sec_pin():
    log("== PIN across restarts, end to end with the relay crate's client")
    d = fresh_dir("pin"); p = os.path.join(d, "relay.identity")
    for i in range(2):
        r1 = run(HEAD, ["relay", "--identity-file", p], keep_open=True, timeout=8) if False else None
    # start 1 (keep running while the client connects)
    def start(args, stdin_bytes=None):
        cwd, env = env_for(fresh_dir("pinenv"))
        pr = subprocess.Popen([HEAD] + args, cwd=cwd, env=env, stdin=subprocess.PIPE if stdin_bytes else subprocess.DEVNULL,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if stdin_bytes:
            pr.stdin.write(stdin_bytes); pr.stdin.close()
        out = b""; t0 = time.monotonic()
        while b"Press Ctrl-C" not in out and time.monotonic() - t0 < 15:
            r, _, _ = select.select([pr.stdout], [], [], 0.1)
            if r:
                c = os.read(pr.stdout.fileno(), 65536)
                if not c:
                    break
                out += c
        return pr, out.decode()

    def stop(pr):
        pr.send_signal(signal.SIGINT); o, e = pr.communicate(timeout=10)
        ALL_OUTPUT.append(("pin", o.decode() + e.decode()))
        return pr.returncode

    pr, o1 = start(["relay", "--identity-file", p]); fp1 = fp_of(o1); url1 = url_of(o1); note_key_from_file(p)
    rc, l = run_client(url1, fp1, "ok"); log(f"PIN start1 {file_id_line({'out': o1})} client rc={rc} {l}")
    log(f"PIN start1 stop rc={stop(pr)}")
    s0 = fstate(p)
    pr, o2 = start(["relay", "--identity-file", p]); url2 = url_of(o2)
    rc, l = run_client(url2, fp1, "ok"); log(f"PIN start2 {file_id_line({'out': o2})} fp same={fp_of(o2) == fp1}; client pinned to start1 rc={rc} {l}")
    log(f"PIN start2 stop rc={stop(pr)} file unchanged={s0 == fstate(p)}")
    pr, o3 = start(["relay", "--identity-stdin"], stdin_bytes=open(p, "rb").read())
    rc, l = run_client(url_of(o3), fp1, "ok"); log(f"PIN stdin start with the same blob: fp same={fp_of(o3) == fp1}; client rc={rc} {l}"); stop(pr)
    pr, o4 = start(["relay"])
    rc, l = run_client(url_of(o4), fp1, "pin_mismatch"); log(f"PIN default start, client pinned to start1: rc={rc} {l}"); stop(pr)


def b64_windows(key, win=18):
    out = set()
    for i in range(0, len(key) - win):
        w = key[i:i + win]
        for enc in (base64.b64encode, base64.urlsafe_b64encode):
            s = enc(w).decode().rstrip("=")
            out.add(s[4:-4])  # inner part is alignment-independent
    return out


def needles(key):
    n = []
    for i in range(0, len(key) - 16, 4):
        w = key[i:i + 16]
        n.append(("hex", w.hex())); n.append(("HEX", w.hex().upper()))
        n.append(("dec", ", ".join(str(x) for x in w)))
        n.append(("dec-nospace", ",".join(str(x) for x in w)))
    for s in b64_windows(key):
        n.append(("b64", s))
    return n


def scan_text(text, key):
    for kind, s in needles(key):
        if s and s in text:
            return kind
    # base64 of the whole key at any of 3 offsets (control for long runs)
    return None


def sec_scan():
    log(f"== SCAN: {len(ALL_OUTPUT)} captured outputs against {len(KEYS)} keys")
    # positive controls
    if KEYS:
        k = KEYS[0]
        ctl = {"hex": k.hex(), "HEX": k.hex().upper(), "b64": base64.b64encode(k).decode(), "b64url": base64.urlsafe_b64encode(k[1:]).decode(),
               "dec": "[" + ", ".join(str(x) for x in k) + "]"}
        log("SCAN positive controls:", {n: scan_text("prefix " + t + " suffix", k) for n, t in ctl.items()})
    hits = []
    for label, text in ALL_OUTPUT:
        for k in KEYS:
            kind = scan_text(text, k)
            if kind:
                hits.append((label, kind))
    log(f"SCAN hits: {len(hits)} {hits[:10]}")


if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "p"), exist_ok=True)
    order = ["default", "usage", "file", "file2", "modes", "acl", "blob", "stdin", "pin", "kill", "scan"]
    for s in order:
        if s in SECTIONS:
            try:
                globals()["sec_" + s]()
            except Exception as e:
                import traceback
                log(f"SECTION {s} CRASHED: {e!r}")
                traceback.print_exc()
