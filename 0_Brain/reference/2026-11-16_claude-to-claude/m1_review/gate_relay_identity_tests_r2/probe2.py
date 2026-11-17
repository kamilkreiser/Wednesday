#!/usr/bin/env python3
"""QA gate r2 driver for `coagent relay --identity-file / --identity-stdin` at the v3 blob.

Reuses round 1's `run()` and helpers (probe_base.py = the first 200 lines of round 1's probe.py,
unchanged) with the v3 layout. Every relay listens on 127.0.0.1 with an ephemeral port (or a
127.0.0.1 port this script took from the OS, to make a bind fail); the non-loopback probes are
refused before any bind. Every file lives under the scratch root.

usage: probe2.py <scratch-root> <head-binary> <main-binary> <pin-client-binary> [section ...]
"""
import hashlib, os, random, select, signal, socket, stat, struct, subprocess, sys, threading, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import probe_base as B  # noqa: E402

ROOT, HEAD, MAIN, CLIENT = B.ROOT, B.HEAD, B.MAIN, B.CLIENT
HDR = b"coagent-relay-identity v3\n"
B.HDR = HDR
log, fresh_dir, env_for, listing, run, short, fp_of, url_of, fstate, file_id_line, prefixes = (
    B.log, B.fresh_dir, B.env_for, B.listing, B.run, B.short, B.fp_of, B.url_of, B.fstate, B.file_id_line, B.prefixes)


def split_blob(b):
    h = len(HDR)
    cl = struct.unpack(">I", b[h:h + 4])[0]
    cert = b[h + 4:h + 4 + cl]
    k0 = h + 4 + cl
    kl = struct.unpack(">I", b[k0:k0 + 4])[0]
    return cert, b[k0 + 4:k0 + 4 + kl]


def join_blob(cert, key, hdr=HDR, hash_=None):
    if hash_ is None:
        hash_ = hashlib.sha256(cert).digest()
    return hdr + struct.pack(">I", len(cert)) + cert + struct.pack(">I", len(key)) + key + hash_


B.split_blob = split_blob
B.join_blob = join_blob


def valid_blob(b):
    try:
        c, k = split_blob(b)
        return join_blob(c, k) == b
    except Exception:
        return False


def make_identity(d, name="relay.identity"):
    p = os.path.join(d, name)
    r = run(HEAD, ["relay", "--identity-file", p], label="make")
    assert r["started"], r
    B.note_key_from_file(p)
    return p, fp_of(r["out"])


def sha(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def removed_line(r):
    return [l for l in r["err"].splitlines() if "leftover" in l]


SECTIONS = set(sys.argv[5:]) or {"default", "usage", "f5", "acltext", "cleanup", "race", "kill", "blob", "stdin", "pin", "scan"}


# ------------------------------------------------------------------ default (unchanged vs main)
def sec_default():
    log("== DEFAULT: neither option, main vs head; 3 starts each in empty cwd/TMPDIR/HOME")
    for name, b in (("main", MAIN), ("head", HEAD)):
        fps = []
        for i in range(3):
            base = fresh_dir(f"default-{name}")
            r = run(b, ["relay"], base=base, lsof=(i == 0), label=f"default-{name}")
            fps.append(fp_of(r["out"]))
            left = [x for x in listing(base) if x not in ("cwd", "tmp", "home")]
            log(f"DEFAULT {name} run{i}: rc={r['rc']} prefixes={prefixes(r['out'])} identity_line={file_id_line(r)} leftover={left} stderr_lines={len(r['err'].splitlines())}")
            if i == 0:
                regs = [l for l in r["lsof"].splitlines() if " REG " in l or " DIR " in l]
                kinds = sorted(set(l.split()[3] + ":" + l.split()[-1].rsplit('/', 1)[-1] for l in regs))
                log(f"DEFAULT {name} lsof REG/DIR entries: {len(regs)} -> {kinds}")
        log(f"DEFAULT {name} fingerprints distinct: {len(set(fps)) == 3}")


# ------------------------------------------------------------------ usage exit codes
def sec_usage():
    log("== USAGE: exit codes main vs head (identity file paths are NEW paths in a 0700 scratch dir)")
    for c in [["relay", "--listen"], ["relay", "--bogus"], ["relay", "--status-secs", "x"], ["relay", "--listen", "nope"],
              ["frobnicate"], ["--version", "extra"], ["relay", "--listen", "0.0.0.0:0"], ["relay", "--identity-file"],
              ["relay", "--identity-stdin", "--identity-stdin"], ["relay", "--identity-file", ""], ["relay", "--identity-file", "-x"],
              ["relay", "--identity-file=a"]]:
        base = fresh_dir("usage")
        rm = run(MAIN, c, base=fresh_dir("usage-main"), timeout=5, label="usage-main")
        rh = run(HEAD, c, base=base, timeout=5, label="usage-head")
        extra = [x for x in listing(base) if x not in ("cwd", "tmp", "home")]
        log(f"USAGE {c}: main rc={rm['rc']} | head rc={rh['rc']} listened={rh['listened']} files={extra}")


# ------------------------------------------------------------------ F5: early refusals leave no file
def sec_f5():
    log("== F5: every early refusal with a NEW identity path leaves no file")
    cases = [
        ("non-loopback 0.0.0.0", ["--listen", "0.0.0.0:0"]),
        ("non-loopback [::]", ["--listen", "[::]:0"]),
        ("non-loopback 10.255.255.1", ["--listen", "10.255.255.1:0"]),
        ("non-loopback 192.0.2.1", ["--listen", "192.0.2.1:0"]),
        ("bad listen address", ["--listen", "nope"]),
        ("listen port only", ["--listen", "8080"]),
        ("bad status-secs", ["--status-secs", "x"]),
        ("unknown flag", ["--bogus"]),
    ]
    for name, extra in cases:
        d = fresh_dir("f5"); p = os.path.join(d, "relay.identity")
        r = run(HEAD, ["relay"] + extra + ["--identity-file", p], timeout=10, label=f"f5-{name}")
        log(f"F5 {name:28}: {short(r)} file_exists={os.path.lexists(p)} dir={listing(d)}")
        # also with the option first
        d = fresh_dir("f5b"); p = os.path.join(d, "relay.identity")
        r = run(HEAD, ["relay", "--identity-file", p] + extra, timeout=10, label=f"f5b-{name}")
        log(f"F5 {name:28} (option first): rc={r['rc']} listened={r['listened']} file_exists={os.path.lexists(p)}")
    for name, args in [("both options", ["--identity-file", "P", "--identity-stdin"]),
                       ("both options reversed", ["--identity-stdin", "--identity-file", "P"]),
                       ("file twice", ["--identity-file", "P", "--identity-file", "P"])]:
        d = fresh_dir("f5c"); p = os.path.join(d, "relay.identity")
        a = [p if x == "P" else x for x in args]
        r = run(HEAD, ["relay"] + a, timeout=10, label=f"f5c-{name}")
        log(f"F5 {name:28}: rc={r['rc']} listened={r['listened']} file_exists={os.path.lexists(p)}")
    # non-loopback + stdin: refused without waiting for standard input
    r = run(HEAD, ["relay", "--listen", "0.0.0.0:0", "--identity-stdin"], stdin_bytes=b"", keep_open=True, timeout=10, label="f5-stdin")
    log(f"F5 non-loopback + stdin (pipe open, silent): {short(r)}")
    # leftovers must NOT be removed by a start refused for its address
    d = fresh_dir("f5-left"); p = os.path.join(d, "relay.identity")
    lp = os.path.join(d, ".relay.identity.tmp-1-2"); open(lp, "wb").write(b"x"); os.chmod(lp, 0o600)
    r = run(HEAD, ["relay", "--listen", "0.0.0.0:0", "--identity-file", p], timeout=10)
    log(f"F5 non-loopback refusal with a leftover present: rc={r['rc']} leftover still there={os.path.exists(lp)} dir={listing(d)}")
    # bind failure after creation (DQ3): port in use on 127.0.0.1
    d = fresh_dir("bindfail"); s = socket.socket(); s.bind(("127.0.0.1", 0)); s.listen(1); port = s.getsockname()[1]
    p = os.path.join(d, "relay.identity")
    r = run(HEAD, ["relay", "--listen", f"127.0.0.1:{port}", "--identity-file", p], timeout=10)
    s.close(); B.note_key_from_file(p)
    log(f"F5 bind fails after create (DQ3): {short(r)} err={r['err'].strip().splitlines()} dir={listing(d)} valid={valid_blob(open(p,'rb').read()) if os.path.exists(p) else None}")
    r2 = run(HEAD, ["relay", "--identity-file", p])
    log(f"F5 next start after the bind failure: {short(r2)} {file_id_line(r2)}")


# ------------------------------------------------------------------ F1: are the text's claims true?
def sec_acltext():
    log("== F1 text: what `ls -l`, `ls -le`, `ls -led` actually show for ACL entries")
    d = fresh_dir("acltext"); g, _ = make_identity(d)
    log("ACLTEXT before: ls -l:", subprocess.run(["/bin/ls", "-l", g], capture_output=True, text=True).stdout.strip())
    c = subprocess.run(["/bin/chmod", "+a", "everyone allow read", g], capture_output=True, text=True)
    log("ACLTEXT chmod +a rc:", c.returncode, c.stderr.strip())
    log("ACLTEXT file ls -l:", subprocess.run(["/bin/ls", "-l", g], capture_output=True, text=True).stdout.strip())
    le = subprocess.run(["/bin/ls", "-le", g], capture_output=True, text=True).stdout
    log("ACLTEXT file ls -le (repr):", repr(le))
    r = run(HEAD, ["relay", "--identity-file", g])
    log(f"ACLTEXT file with ACL -> {'LOADED' if r['listened'] else 'refused'} (owner ruling: accepted, documented) stderr={r['err'].strip().splitlines()[:2]}")
    c = subprocess.run(["/bin/chmod", "+a", "everyone allow read,file_inherit", d], capture_output=True, text=True)
    led = subprocess.run(["/bin/ls", "-led", d], capture_output=True, text=True).stdout
    log("ACLTEXT folder ls -led (repr):", repr(led))
    p = os.path.join(d, "new.identity")
    r = run(HEAD, ["relay", "--identity-file", p]); B.note_key_from_file(p)
    log(f"ACLTEXT create under inheriting folder -> {file_id_line(r)}; ls -le new file: {subprocess.run(['/bin/ls', '-le', p], capture_output=True, text=True).stdout!r}")


# ------------------------------------------------------------------ F3: attack the cleanup
def precious(dirpath, name="precious", mode=0o600, data=None):
    p = os.path.join(dirpath, name)
    open(p, "wb").write(data or os.urandom(64))
    os.chmod(p, mode)
    return p


def sec_cleanup():
    log("== CLEANUP attacks (identity path <d>/relay.identity; d is 0700)")
    other = fresh_dir("other-files")
    # A1 symlink with a matching name -> another file of the user
    d = fresh_dir("c-symlink"); tgt = precious(other, "tgt1"); h0 = sha(tgt)
    ln = os.path.join(d, ".relay.identity.tmp-11-22"); os.symlink(tgt, ln)
    r = run(HEAD, ["relay", "--identity-file", os.path.join(d, "relay.identity")])
    log(f"CLEAN A1 symlink->user file: {short(r)} target intact={os.path.exists(tgt) and sha(tgt) == h0} link still there={os.path.islink(ln)} dir={listing(d)}")
    # A1b dangling symlink with a matching name
    d = fresh_dir("c-dangle"); ln = os.path.join(d, ".relay.identity.tmp-1-2"); os.symlink(os.path.join(other, "nonexistent"), ln)
    r = run(HEAD, ["relay", "--identity-file", os.path.join(d, "relay.identity")])
    log(f"CLEAN A1b dangling symlink: {short(r)} target created={os.path.lexists(os.path.join(other, 'nonexistent'))} dir={listing(d)}")
    # A2 directory with a matching name (with a file inside)
    d = fresh_dir("c-dir"); sub = os.path.join(d, ".relay.identity.tmp-1-2"); os.mkdir(sub, 0o700); precious(sub, "inner")
    r = run(HEAD, ["relay", "--identity-file", os.path.join(d, "relay.identity")])
    log(f"CLEAN A2 directory: {short(r)} dir still there={os.path.isdir(sub)} inner={os.listdir(sub)}")
    # A3 FIFO with a matching name
    d = fresh_dir("c-fifo"); ff = os.path.join(d, ".relay.identity.tmp-1-2"); os.mkfifo(ff, 0o600)
    r = run(HEAD, ["relay", "--identity-file", os.path.join(d, "relay.identity")], timeout=10)
    log(f"CLEAN A3 FIFO: {short(r)} fifo still there={stat.S_ISFIFO(os.lstat(ff).st_mode)}")
    # A4 hard link with a matching name to an unrelated 0600 file of the user
    d = fresh_dir("c-hard"); tgt = precious(other, "tgt4"); h0 = sha(tgt)
    hl = os.path.join(d, ".relay.identity.tmp-3-4"); os.link(tgt, hl)
    r = run(HEAD, ["relay", "--identity-file", os.path.join(d, "relay.identity")])
    log(f"CLEAN A4 hard link to a 0600 user file: {short(r)} removed={removed_line(r)} link name gone={not os.path.lexists(hl)} target content intact={sha(tgt) == h0} target nlink={os.lstat(tgt).st_nlink}")
    # A4b hard link to an unrelated 0644 file of the user
    d = fresh_dir("c-hard644"); tgt = precious(other, "tgt4b", 0o644); h0 = sha(tgt)
    hl = os.path.join(d, ".relay.identity.tmp-3-4"); os.link(tgt, hl)
    r = run(HEAD, ["relay", "--identity-file", os.path.join(d, "relay.identity")])
    log(f"CLEAN A4b hard link to a 0644 user file: {short(r)} name kept={os.path.lexists(hl)} target intact={sha(tgt) == h0}")
    # A5 leftover that is a hard link to the identity file itself (kill between link and unlink)
    d = fresh_dir("c-self"); g, gfp = make_identity(d); h0 = sha(g)
    hl = os.path.join(d, ".relay.identity.tmp-5-6"); os.link(g, hl)
    r = run(HEAD, ["relay", "--identity-file", g])
    log(f"CLEAN A5 leftover = hard link to the identity itself: {short(r)} {file_id_line(r)} same fp={fp_of(r['out']) == gfp} identity intact={sha(g) == h0} nlink={os.lstat(g).st_nlink} dir={listing(d)}")
    # A6 how strict is the pattern: none of these may be removed
    d = fresh_dir("c-pattern"); g, gfp = make_identity(d)
    names = ["relay.identity.bak", "relay.identity~", ".relay.identity.swp", ".relay.identity", "relay.identity.tmp-1-2",
             ".relay.identity.tmp-1", ".relay.identity.tmp--1", ".relay.identity.tmp-1-", ".relay.identity.tmp-1-2-3",
             ".relay.identity.tmp-a-1", ".relay.identity.tmp-1-2.bak", ".relay.identity.tmp-1-2 ", " .relay.identity.tmp-1-2",
             ".relay.identity.TMP-1-2", ".RELAY.IDENTITY.tmp-1-2", ".relay.identity.tmp-١-2", ".relay.identity.tmp-+1-2",
             ".relay.identity.tmp-1-2\n", "..relay.identity.tmp-1-2", ".relay.identity..tmp-1-2", ".relayXidentity.tmp-1-2",
             ".relay.identit.tmp-1-2", ".relay.identity.tmp-1_2", ".other.identity.tmp-1-2", ".relay.tmp-1-2"]
    made = []
    for n in names:
        try:
            precious(d, n); made.append(n)
        except OSError as e:
            log(f"CLEAN A6 could not create {n!r}: {e}")
    hs = {n: sha(os.path.join(d, n)) for n in made}
    r = run(HEAD, ["relay", "--identity-file", g])
    gone = [n for n in made if not os.path.lexists(os.path.join(d, n)) or sha(os.path.join(d, n)) != hs[n]]
    log(f"CLEAN A6 {len(made)} near-miss names: {short(r)} {file_id_line(r)} removed_line={removed_line(r)} REMOVED/CHANGED={gone}")
    # A6b which shapes DO match (they are removed)
    d = fresh_dir("c-match"); g, _ = make_identity(d)
    yes = [".relay.identity.tmp-0-0", ".relay.identity.tmp-999999999999999999999999-1", ".relay.identity.tmp-007-08"]
    for n in yes:
        precious(d, n)
    r = run(HEAD, ["relay", "--identity-file", g])
    log(f"CLEAN A6b matching shapes: {removed_line(r)} left={[n for n in yes if os.path.lexists(os.path.join(d, n))]}")
    # A6c case-insensitive filesystem: path given in a different case than the file
    d = fresh_dir("c-case"); g, gfp = make_identity(d)
    precious(d, ".relay.identity.tmp-1-2")
    r = run(HEAD, ["relay", "--identity-file", os.path.join(d, "RELAY.IDENTITY")])
    log(f"CLEAN A6c path in other case: {short(r)} {file_id_line(r)} same fp={fp_of(r['out']) == gfp} lowercase leftover kept={os.path.lexists(os.path.join(d, '.relay.identity.tmp-1-2'))}")
    # A6d non-UTF-8 names (APFS refuses them?)
    try:
        fd = os.open(os.path.join(d.encode(), b".\xff.tmp-1-2"), os.O_CREAT | os.O_WRONLY, 0o600); os.close(fd)
        log("CLEAN A6d non-UTF-8 name: CREATED (filesystem accepts it)")
    except OSError as e:
        log(f"CLEAN A6d non-UTF-8 name: refused by the filesystem: {e}")
    # A7 another identity's leftover and other files in the same folder untouched
    d = fresh_dir("c-others"); g, _ = make_identity(d); g2, _ = make_identity(d, "other.identity")
    o_left = precious(d, ".other.identity.tmp-7-8"); hg2 = sha(g2); ho = sha(o_left)
    r = run(HEAD, ["relay", "--identity-file", g])
    log(f"CLEAN A7 other identity + its leftover: {short(r)} other identity intact={sha(g2) == hg2} other leftover intact={sha(o_left) == ho}")
    # A8 a refused parent removes nothing
    d = fresh_dir("c-openparent", 0o755); lp = precious(d, ".relay.identity.tmp-1-2")
    r = run(HEAD, ["relay", "--identity-file", os.path.join(d, "relay.identity")])
    log(f"CLEAN A8 parent 0755 with a leftover: {short(r)} leftover kept={os.path.exists(lp)}")
    # A9 mixed: valid leftovers + ONE suspicious -> nothing removed
    d = fresh_dir("c-mixed")
    for i in range(5):
        precious(d, f".relay.identity.tmp-{i}-1")
    precious(d, ".relay.identity.tmp-9-9", 0o640)
    r = run(HEAD, ["relay", "--identity-file", os.path.join(d, "relay.identity")])
    log(f"CLEAN A9 five good + one 0640: {short(r)} remaining={len([x for x in os.listdir(d) if 'tmp' in x])} created={os.path.exists(os.path.join(d,'relay.identity'))}")
    # A10 leftovers with setuid / 0400 / 0000 / 0200 modes
    for m in (0o4600, 0o400, 0o000, 0o200, 0o1600):
        d = fresh_dir("c-mode"); lp = precious(d, ".relay.identity.tmp-1-2", m)
        r = run(HEAD, ["relay", "--identity-file", os.path.join(d, "relay.identity")])
        log(f"CLEAN A10 leftover mode {oct(os.lstat(lp).st_mode & 0o7777) if os.path.lexists(lp) else oct(m)}: {short(r)} removed={removed_line(r)!r:.60} kept={os.path.lexists(lp)}")
    # A11 a refused load (file 0640) still removes leftovers? (order)
    d = fresh_dir("c-refusedload"); g, _ = make_identity(d); os.chmod(g, 0o640); lp = precious(d, ".relay.identity.tmp-1-2")
    r = run(HEAD, ["relay", "--identity-file", g])
    log(f"CLEAN A11 refused load (0640 identity) with a leftover: {short(r)} leftover kept={os.path.exists(lp)} removed_line={removed_line(r)}")
    # A12 thousands: 5000 matching good leftovers; 50,000 non-matching names; 5000 + one suspicious
    d = fresh_dir("c-many")
    for i in range(5000):
        fd = os.open(os.path.join(d, f".relay.identity.tmp-{i}-1"), os.O_CREAT | os.O_WRONLY, 0o600); os.close(fd)
    r = run(HEAD, ["relay", "--identity-file", os.path.join(d, "relay.identity")], timeout=120)
    log(f"CLEAN A12a 5000 leftovers: {short(r)} removed_line={removed_line(r)} remaining={len(os.listdir(d))} elapsed={r['elapsed']:.2f}s")
    d = fresh_dir("c-many-nonmatch")
    for i in range(50000):
        fd = os.open(os.path.join(d, f"f{i}"), os.O_CREAT | os.O_WRONLY, 0o600); os.close(fd)
    r = run(HEAD, ["relay", "--identity-file", os.path.join(d, "relay.identity")], timeout=120)
    log(f"CLEAN A12b 50,000 non-matching files: {short(r)} entries={len(os.listdir(d))} elapsed={r['elapsed']:.2f}s")
    d = fresh_dir("c-many-bad")
    for i in range(5000):
        fd = os.open(os.path.join(d, f".relay.identity.tmp-{i}-1"), os.O_CREAT | os.O_WRONLY, 0o600); os.close(fd)
    os.chmod(os.path.join(d, ".relay.identity.tmp-4999-1"), 0o604)
    r = run(HEAD, ["relay", "--identity-file", os.path.join(d, "relay.identity")], timeout=120)
    log(f"CLEAN A12c 5000 leftovers, one 0604: {short(r)} remaining={len(os.listdir(d))} elapsed={r['elapsed']:.2f}s")


# ------------------------------------------------------------------ F3: race the check against the removal
def sec_race(n=200):
    log(f"== RACE: a matching name flipped between a 0600 file and a symlink/hard link to a user file, {n} starts")
    d = fresh_dir("race"); other = fresh_dir("race-other")
    tgt = precious(other, "victim"); h0 = sha(tgt)
    name = os.path.join(d, ".relay.identity.tmp-1-2")
    stop = [False]

    def flipper():
        i = 0
        while not stop[0]:
            i += 1
            t = os.path.join(d, f"stage{i % 2}")
            try:
                if i % 3 == 0:
                    os.symlink(tgt, t)
                elif i % 3 == 1:
                    os.link(tgt, t)
                else:
                    fd = os.open(t, os.O_CREAT | os.O_WRONLY, 0o600); os.close(fd)
                os.rename(t, name)
            except OSError:
                try:
                    os.unlink(t)
                except OSError:
                    pass
    th = threading.Thread(target=flipper); th.start()
    outcomes = {}
    p = os.path.join(d, "relay.identity")
    try:
        for i in range(n):
            r = run(HEAD, ["relay", "--identity-file", p], timeout=15, label="race")
            k = "listened" if r["listened"] else ("refused:" + (r["err"].strip().splitlines() or ["?"])[0].split(": ")[-1][:60])
            outcomes[k] = outcomes.get(k, 0) + 1
            if os.path.exists(p):
                B.note_key_from_file(p)
    finally:
        stop[0] = True; th.join()
    log(f"RACE outcomes: {outcomes}")
    log(f"RACE victim intact={os.path.exists(tgt) and sha(tgt) == h0} nlink={os.lstat(tgt).st_nlink} mode={oct(os.lstat(tgt).st_mode & 0o777)}")
    # two relays creating the same NEW path at the same moment
    res = {"both listened same fp": 0, "one refused": 0, "other": 0}; bad = 0
    for i in range(30):
        d = fresh_dir("pair"); p = os.path.join(d, "relay.identity")
        out = [None, None]

        def go(j):
            out[j] = run(HEAD, ["relay", "--identity-file", p], timeout=15, label="pair")
        ts = [threading.Thread(target=go, args=(j,)) for j in (0, 1)]
        [t.start() for t in ts]; [t.join() for t in ts]
        a, b = out
        if a["listened"] and b["listened"] and fp_of(a["out"]) == fp_of(b["out"]):
            res["both listened same fp"] += 1
        elif a["listened"] != b["listened"]:
            res["one refused"] += 1
            loser = a if not a["listened"] else b
            msgs = res.setdefault("loser messages", {})
            m = (loser["err"].strip().splitlines() or ["?"])[0].split(": ", 2)[-1][:90]
            msgs[m] = msgs.get(m, 0) + 1
        else:
            res["other"] += 1
            log("PAIR other:", short(a), short(b), fp_of(a["out"]) == fp_of(b["out"]))
        names = os.listdir(d)
        if names != ["relay.identity"] or not valid_blob(open(p, "rb").read()):
            bad += 1; log("PAIR bad dir:", names)
        B.note_key_from_file(p)
    log(f"PAIR 30 simultaneous creates: {res}; dirs not exactly one valid file: {bad}")


# ------------------------------------------------------------------ F3: kill loop
def sec_kill(n=160):
    log(f"== KILL: SIGKILL a relay at a random 0-80 ms, {n} times, same folder; final file moved aside after each; then one clean start")
    d = fresh_dir("kill"); aside = fresh_dir("kill-aside")
    p = os.path.join(d, "relay.identity")
    st = {"kills": 0, "final_valid": 0, "final_partial": 0, "final_open_bits": 0, "temp_seen_after_kill": 0, "temp_open_bits": 0,
          "max_temps_at_once": 0, "removed_reported": 0}
    for i in range(n):
        cwd, env = env_for(fresh_dir("killenv"))
        pr = subprocess.Popen([HEAD, "relay", "--identity-file", p], cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                              stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        time.sleep(random.uniform(0.0, 0.08))
        pr.kill(); pr.wait()
        e = pr.stderr.read().decode(errors="replace"); pr.stderr.close()
        B.ALL_OUTPUT.append(("kill", e))
        if "removed" in e:
            st["removed_reported"] += int(e.split("removed ")[1].split()[0])
        st["kills"] += 1
        names = os.listdir(d)
        temps = [x for x in names if x != "relay.identity"]
        if temps:
            st["temp_seen_after_kill"] += 1
            st["max_temps_at_once"] = max(st["max_temps_at_once"], len(temps))
            for x in temps:
                B.note_key_from_file(os.path.join(d, x))
                if os.lstat(os.path.join(d, x)).st_mode & 0o077:
                    st["temp_open_bits"] += 1
        if "relay.identity" in names:
            b = open(p, "rb").read(); B.note_key_from_file(p)
            st["final_valid" if valid_blob(b) else "final_partial"] += 1
            if os.lstat(p).st_mode & 0o077:
                st["final_open_bits"] += 1
            os.rename(p, os.path.join(aside, f"final-{i}"))
    extra = 0
    while not [x for x in os.listdir(d) if x != "relay.identity"] and extra < 400:
        extra += 1
        cwd, env = env_for(fresh_dir("killenv"))
        pr = subprocess.Popen([HEAD, "relay", "--identity-file", p], cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(random.uniform(0.0, 0.08)); pr.kill(); pr.wait()
        if os.path.exists(p):
            B.note_key_from_file(p); os.rename(p, os.path.join(aside, f"final-x{extra}"))
    for x in os.listdir(d):
        B.note_key_from_file(os.path.join(d, x))
    st["extra_kills_to_get_a_leftover"] = extra
    before = sorted(os.listdir(d))
    r = run(HEAD, ["relay", "--identity-file", p], label="kill-clean")
    after = sorted(os.listdir(d))
    B.note_key_from_file(p)
    st["clean_start"] = short(r)
    log("KILL stats:", st)
    log(f"KILL folder before the clean start: {len(before)} temp files; clean start says {removed_line(r)}; after: {after}; final valid={valid_blob(open(p,'rb').read()) if os.path.exists(p) else None} nlink={os.lstat(p).st_nlink if os.path.exists(p) else None}")


# ------------------------------------------------------------------ blobs through both options
def sec_blob():
    log("== BLOB through both options (v3)")
    d = fresh_dir("blobsrc"); g, gfp = make_identity(d); blob = open(g, "rb").read()
    c, k = split_blob(blob)
    d2 = fresh_dir("blobsrc2"); g2, _ = make_identity(d2); c2, k2 = split_blob(open(g2, "rb").read())
    c_ser = bytearray(c); c_ser[15] ^= 1; c_ser = bytes(c_ser)
    v1 = b"coagent-relay-identity v1\n" + struct.pack(">I", len(c)) + c + struct.pack(">I", len(k)) + k
    variants = {
        "valid": blob, "v1 (round-1 layout)": v1, "v2 + v3 body": blob.replace(b" v3\n", b" v2\n", 1),
        "CRLF": blob.replace(b" v3\n", b" v3\r\n", 1), "hash flipped": blob[:-1] + bytes([blob[-1] ^ 1]),
        "cert serial flipped, old hash": join_blob(c_ser, k, hash_=hashlib.sha256(c).digest()),
        "cert serial flipped, REHASHED": join_blob(c_ser, k),
        "certA+keyB rehashed": join_blob(c, k2), "trailing byte": blob + b"\0", "no hash": blob[:-32],
    }
    for name, b in variants.items():
        rs = run(HEAD, ["relay", "--identity-stdin"], stdin_bytes=b, label=f"blob-stdin-{name}")
        dd = fresh_dir("blobfile"); p = os.path.join(dd, "id"); open(p, "wb").write(b); os.chmod(p, 0o600)
        rf = run(HEAD, ["relay", "--identity-file", p], label=f"blob-file-{name}")
        fps = fp_of(rs["out"]) if rs["listened"] else None
        log(f"BLOB {name:30}: stdin {short(rs)} fp={'same' if fps == gfp else ('NEW' if fps else '-')} | file {short(rf)}")


# ------------------------------------------------------------------ F4 + stdin sanity
def sec_stdin():
    log("== STDIN")
    d = fresh_dir("stdinsrc"); g, gfp = make_identity(d); blob = open(g, "rb").read()
    for size in (16384, 16385, 16386, 1 << 20, 64 << 20):
        for rep in range(2):
            p = os.path.join(fresh_dir("acct"), "in"); f = open(p, "wb"); f.write(b"A" * size); f.close()
            f = open(p, "rb")
            r = run(HEAD, ["relay", "--identity-stdin"], stdin=f)
            off = os.lseek(f.fileno(), 0, os.SEEK_CUR); f.close()
            log(f"STDIN accounting {size} bytes rep{rep}: {short(r)} consumed={off}")
    # a valid blob followed by junk, in one regular file: offset?
    p = os.path.join(fresh_dir("acct2"), "in"); open(p, "wb").write(blob + b"Z" * 100000)
    f = open(p, "rb"); r = run(HEAD, ["relay", "--identity-stdin"], stdin=f); off = os.lseek(f.fileno(), 0, os.SEEK_CUR); f.close()
    log(f"STDIN valid blob + 100,000 junk bytes: {short(r)} consumed={off} (blob is {len(blob)})")
    # valid from a regular file and from a pipe
    f = open(g, "rb"); r = run(HEAD, ["relay", "--identity-stdin"], stdin=f); off = os.lseek(f.fileno(), 0, os.SEEK_CUR); f.close()
    log(f"STDIN valid regular file: {short(r)} fp_same={fp_of(r['out']) == gfp} consumed={off}")
    base = fresh_dir("stdin-valid")
    r = run(HEAD, ["relay", "--identity-stdin"], base=base, stdin_bytes=blob)
    log(f"STDIN valid pipe: {short(r)} fp_same={fp_of(r['out']) == gfp} files={[x for x in listing(base) if x not in ('cwd','tmp','home')]}")
    f = open("/dev/null", "rb"); r = run(HEAD, ["relay", "--identity-stdin"], stdin=f); f.close()
    log(f"STDIN /dev/null: {short(r)}")
    cwd, env = env_for(fresh_dir("closed")); t0 = time.monotonic()
    pr = subprocess.run([HEAD, "relay", "--identity-stdin"], cwd=cwd, env=env, capture_output=True, text=True, timeout=20, preexec_fn=lambda: os.close(0))
    B.ALL_OUTPUT.append(("closed", pr.stdout + pr.stderr))
    log(f"STDIN fd 0 closed: rc={pr.returncode} t={time.monotonic()-t0:.2f}s err={pr.stderr.strip().splitlines()[:2]}")
    times = []
    for i in range(5):
        r = run(HEAD, ["relay", "--identity-stdin"], stdin_bytes=b"", keep_open=True, timeout=30)
        times.append(round(r["elapsed"], 2))
    log(f"STDIN silent open pipe x5: elapsed {times}; last: {short(r)}")
    r = run(HEAD, ["relay", "--identity-stdin"], stdin_bytes=blob, keep_open=True, timeout=30)
    log(f"STDIN valid blob, pipe kept open: {short(r)}")
    # endless pipe
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
    try:
        pr.stdin.close()
    except BrokenPipeError:
        pass
    pr.wait(10); o, e = pr.stdout.read(), pr.stderr.read()
    B.ALL_OUTPUT.append(("flood", o.decode() + e.decode()))
    log(f"STDIN endless pipe: rc={pr.returncode} writer pushed {wrote} bytes (pipe buffer included) t={time.monotonic()-t0:.2f}s err={e.decode().strip().splitlines()[:1]}")


# ------------------------------------------------------------------ pin end to end
def run_client(url, fp, expect):
    r = subprocess.run([CLIENT, "--exact", "gate::gate_pin_client", "--nocapture"], env={**os.environ, "GATE_URL": url, "GATE_FP": fp, "GATE_EXPECT": expect},
                       capture_output=True, text=True, timeout=60)
    lines = [l for l in r.stdout.splitlines() if "GATE_CLIENT" in l]
    tr = [l for l in r.stdout.splitlines() if l.startswith("test result")]
    return r.returncode, lines + tr


def sec_pin():
    log("== PIN across restarts, end to end (the relay crate's client, via the gate's gate_pin_client)")
    d = fresh_dir("pin"); p = os.path.join(d, "relay.identity")

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
        B.ALL_OUTPUT.append(("pin", o.decode() + e.decode()))
        return pr.returncode
    pr, o1 = start(["relay", "--identity-file", p]); fp1 = fp_of(o1); B.note_key_from_file(p)
    rc, l = run_client(url_of(o1), fp1, "ok"); log(f"PIN start1 {file_id_line({'out': o1})} client rc={rc} {l}"); stop(pr)
    s0 = fstate(p)
    pr, o2 = start(["relay", "--identity-file", p])
    rc, l = run_client(url_of(o2), fp1, "ok"); log(f"PIN start2 {file_id_line({'out': o2})} same fp={fp_of(o2) == fp1}; client pinned to start1 rc={rc} {l}"); stop(pr)
    log(f"PIN file unchanged by the load: {s0 == fstate(p)}")
    pr, o3 = start(["relay", "--identity-stdin"], stdin_bytes=open(p, "rb").read())
    rc, l = run_client(url_of(o3), fp1, "ok"); log(f"PIN stdin start same fp={fp_of(o3) == fp1}; client rc={rc} {l}"); stop(pr)
    pr, o4 = start(["relay"])
    rc, l = run_client(url_of(o4), fp1, "pin_mismatch"); log(f"PIN default start, client pinned to start1: rc={rc} {l}"); stop(pr)


import base64
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
    log(f"== SCAN: {len(B.ALL_OUTPUT)} captured outputs against {len(B.KEYS)} keys")
    # positive controls
    if B.KEYS:
        k = B.KEYS[0]
        ctl = {"hex": k.hex(), "HEX": k.hex().upper(), "b64": base64.b64encode(k).decode(), "b64url": base64.urlsafe_b64encode(k[1:]).decode(),
               "dec": "[" + ", ".join(str(x) for x in k) + "]"}
        log("SCAN positive controls:", {n: scan_text("prefix " + t + " suffix", k) for n, t in ctl.items()})
    hits = []
    for label, text in B.ALL_OUTPUT:
        for k in B.KEYS:
            kind = scan_text(text, k)
            if kind:
                hits.append((label, kind))
    log(f"SCAN hits: {len(hits)} {hits[:10]}")


def sec_scan2():
    sec_scan()
    # also the stderr of every pair/kill run and a deliberate-print control through the same path
    n_hex = sum(1 for _, t in B.ALL_OUTPUT for k in B.KEYS[:1] if k.hex() in t)
    log(f"SCAN texts={len(B.ALL_OUTPUT)} keys={len(B.KEYS)} total_chars={sum(len(t) for _, t in B.ALL_OUTPUT)}")

if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "p"), exist_ok=True)
    for s in ["default", "usage", "f5", "acltext", "cleanup", "race", "blob", "stdin", "pin", "kill", "scan"]:
        if s in SECTIONS:
            try:
                (sec_scan2 if s == "scan" else globals()["sec_" + s])()
            except Exception as e:
                import traceback
                log(f"SECTION {s} CRASHED: {e!r}")
                traceback.print_exc()
