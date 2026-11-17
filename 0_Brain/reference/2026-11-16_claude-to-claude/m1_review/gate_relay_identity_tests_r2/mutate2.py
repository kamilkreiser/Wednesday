#!/usr/bin/env python3
"""QA gate r2: round 1's 44 mutants (G01-G44, three stdin anchors moved to the new code with the
SAME mutation) plus new mutants N01.. on code changed since e143847. Each is applied alone to a
scratch worktree; tests: coagent-cli (all targets) and coagent-relay (identity_blob, gate_identity_fuzz,
lib). RED = some test failed (names + first panic lines kept), SURVIVED, NO-COMPILE, ANCHOR.
Sources restored after each row and checked by hash at the end.

usage: mutate2.py <worktree> <shard k/n | ids...>
"""
import hashlib, os, re, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
WT = sys.argv[1]
SEL = sys.argv[2:]
C = "crates/coagent-cli/src/"
R = "crates/coagent-relay/src/"

# round 1's rows, verbatim except the three stdin anchors (see mutate_r1_rows.py)
_r1 = open(os.path.join(HERE, "mutate_r1_rows.py")).read()
_ns = {"C": C, "R": R}
exec(_r1[_r1.index("MUTS = ["):_r1.index("ENV = dict")], _ns)
MUTS = list(_ns["MUTS"])
EXTRA = dict(_ns["EXTRA"])

F = C + "identity_file.rs"
STD = C + "identity_stdin.rs"
RC = C + "relay_cmd.rs"
T = R + "tls.rs"
MUTS += [
 # --- hash / version line / blob (tls.rs)
 ("N01", "hash check weakened to the first byte only", T, "if sha256(cert) != *stored_hash {", "if sha256(cert)[0] != stored_hash[0] {"),
 ("N02", "export stores a zero hash", T, "v.extend_from_slice(&self.fingerprint.0);", "v.extend_from_slice(&[0u8; 32]);"),
 ("N03", "export stores no hash", T, "v.extend_from_slice(&self.fingerprint.0);", ""),
 ("N04", "one trailing byte after the hash accepted", T, "if !rest.is_empty() {\n            return Err(IdentityBlobError::TrailingBytes", "if rest.len() > 1 {\n            return Err(IdentityBlobError::TrailingBytes"),
 ("N05", "a v1 line accepted as current", T, "if line == IDENTITY_BLOB_HEADER {", "if line == IDENTITY_BLOB_HEADER || line == b\"coagent-relay-identity v1\\n\" {"),
 ("N06", "a v2 line accepted as current", T, "if line == IDENTITY_BLOB_HEADER {", "if line == IDENTITY_BLOB_HEADER || line == b\"coagent-relay-identity v2\\n\" {"),
 ("N07", "a CRLF v3 line accepted", T, "if line == IDENTITY_BLOB_HEADER {", "if line == IDENTITY_BLOB_HEADER || line == b\"coagent-relay-identity v3\\r\\n\" {"),
 ("N08", "hash mismatch reported as TrailingBytes (own error lost)", T, "return Err(IdentityBlobError::CertificateHashMismatch);", "return Err(IdentityBlobError::TrailingBytes { extra: 0 });"),
 ("N09", "missing hash reported as a truncated key", T, "return Err(IdentityBlobError::Truncated {\n                part: IdentityPart::CertificateHash,", "return Err(IdentityBlobError::Truncated {\n                part: IdentityPart::Key,"),
 ("N10", "key-belongs check result ignored", T, "key_belongs_to_certificate(cert, key)?;", "let _ = key_belongs_to_certificate(cert, key);"),
 ("N11", "Fingerprint::of_certificate hashes the wrong bytes", T, "Fingerprint(sha256(der))", "Fingerprint(sha256(&der[1..]))"),
 ("N12", "fingerprint taken from the stored hash, hash check removed", T, "if sha256(cert) != *stored_hash {", "if false && sha256(cert) != *stored_hash {"),
 # --- cleanup (identity_file.rs)
 ("N13", "pattern: leading dot not required", F, ".strip_prefix('.')\n        .and_then", ".strip_prefix(\"\")\n        .and_then"),
 ("N14", "pattern: digits not required", F, "let digits = |s: &str| !s.is_empty() && s.bytes().all(|b| b.is_ascii_digit());", "let digits = |s: &str| !s.is_empty();"),
 ("N15", "pattern: second number not checked", F, "Some((a, b)) if digits(a) && digits(b))", "Some((a, _b)) if digits(a))"),
 ("N16", "pattern: empty numbers allowed", F, "let digits = |s: &str| !s.is_empty() && s.bytes().all(|b| b.is_ascii_digit());", "let digits = |s: &str| s.bytes().all(|b| b.is_ascii_digit());"),
 ("N17", "pattern: any identity name's leftovers match", F, ".and_then(|r| r.strip_prefix(name))\n        .and_then(|r| r.strip_prefix(\".tmp-\"))", ".and_then(|r| r.split_once(\".tmp-\").map(|(_, t)| t))"),
 ("N18", "cleanup: only directories refused (symlink/FIFO removed)", F, "let why = if !left.file_type().is_file() {", "let why = if left.file_type().is_dir() {"),
 ("N19", "cleanup: metadata follows links", F, "let left = fs::symlink_metadata(&p).map_err(io_err(\"examine\", &p))?;", "let left = fs::metadata(&p).map_err(io_err(\"examine\", &p))?;"),
 ("N20", "cleanup: owner check removed", F, "} else if left.uid() != uid {", "} else if false {"),
 ("N21", "cleanup: other bits ignored (mask 0o070)", F, "} else if left.mode() & 0o077 != 0 {", "} else if left.mode() & 0o070 != 0 {"),
 ("N22", "cleanup: group bits ignored (mask 0o007)", F, "} else if left.mode() & 0o077 != 0 {", "} else if left.mode() & 0o007 != 0 {"),
 ("N23", "cleanup: suspicious match skipped, others removed, start proceeds", F, "return Err(FileError::SuspiciousLeftover { path: p, why });", "let _ = why; continue;"),
 ("N24", "cleanup runs BEFORE the parent check", F, "    check_parent(dir, &dmd, uid)?;\n    let removed = remove_leftovers(path, uid)?;", "    let removed = remove_leftovers(path, uid)?;\n    check_parent(dir, &dmd, uid)?;"),
 ("N25", "cleanup count reported as 0", F, "    Ok(found.len())\n", "    Ok(0)\n"),
 ("N26", "cleanup removal error ignored", F, "fs::remove_file(p).map_err(io_err(\"remove the leftover temporary file\", p))?;", "let _ = fs::remove_file(p);"),
 ("N27", "create's temp name no longer matches the cleanup pattern", F, "format!(\".{name}.tmp-{pid}-{nanos}\")", "format!(\".{name}.tmp-{pid}_{nanos}\")"),
 ("N28", "a planted file at the temp name is removed on EEXIST", F, ".map_err(io_err(\"create a temporary file next to\", path))?;", ".map_err(|e| { let _ = fs::remove_file(&tmp_path); io_err(\"create a temporary file next to\", path)(e) })?;"),
 ("N29", "cleanup message not printed", RC, "    if removed > 0 {", "    if false && removed > 0 {"),
 ("N30", "cleanup line printed on stdout", RC, "        eprintln!(\n            \"coagent relay: removed {removed}", "        println!(\n            \"coagent relay: removed {removed}"),
 # --- stdin descriptor cap (identity_stdin.rs / relay_cmd.rs)
 ("N31", "stdin limit cap+2", STD, "let mut limited = counted.take(IDENTITY_BLOB_MAX as u64 + 1);", "let mut limited = counted.take(IDENTITY_BLOB_MAX as u64 + 2);"),
 ("N32", "stdin read through a BufReader again", STD, "let counted = Counting { inner: r, n };", "let counted = Counting { inner: std::io::BufReader::new(r), n };"),
 ("N33", "deadline message reports 0 bytes", STD, "bytes_read: counter.load(Ordering::SeqCst),", "bytes_read: 0,"),
 ("N34", "stdin TooLarge threshold off by one (>=)", STD, "Ok(Ok(Ok(buf))) if buf.len() > IDENTITY_BLOB_MAX => Err(StdinError::TooLarge {", "Ok(Ok(Ok(buf))) if buf.len() >= IDENTITY_BLOB_MAX => Err(StdinError::TooLarge {"),
 # --- order of refusals (relay_cmd.rs)
 ("N35", "early non-loopback refusal exits 0", RC, "RelayError::NonLoopbackNotAllowed(opts.listen)\n        );\n        return 1;", "RelayError::NonLoopbackNotAllowed(opts.listen)\n        );\n        return 0;"),
 ("N36", "early refusal ignores --allow-non-loopback (always refuses non-loopback)", RC, "if !bind_allowed(opts.listen, opts.allow_non_loopback) {", "if !bind_allowed(opts.listen, false) {"),
]

ENV = dict(os.environ)
CMDS = [["cargo", "test", "--locked", "--offline", "-p", "coagent-cli", "--no-fail-fast"],
        ["cargo", "test", "--locked", "--offline", "-p", "coagent-relay", "--no-fail-fast", "--test", "identity_blob",
         "--test", "gate_identity_fuzz", "--lib"]]


def h(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


rows = MUTS
if SEL and "/" in SEL[0]:
    k, n = map(int, SEL[0].split("/"))
    rows = [m for i, m in enumerate(MUTS) if i % n == k]
elif SEL:
    rows = [m for m in MUTS if m[0] in SEL]

files = sorted({os.path.join(WT, m[2]) for m in MUTS} | {os.path.join(WT, e[0]) for e in EXTRA.values()})
before = {f: h(f) for f in files}
for mid, prop, rel, old, new in rows:
    edits = [(rel, old, new)] + ([EXTRA[mid]] if mid in EXTRA else [])
    origs = {}
    bad = None
    for r, o, n in edits:
        p = os.path.join(WT, r)
        cur = open(p, encoding="utf-8").read()
        origs.setdefault(p, cur)
        if cur.count(o) != 1:
            bad = f"anchor found {cur.count(o)} times"
            break
        open(p, "w", encoding="utf-8").write(cur.replace(o, n, 1))
    t0 = time.time()
    status, failed, panics = "?", [], []
    try:
        if bad:
            status = "ANCHOR " + bad
        else:
            outs = ""
            nocompile = False
            for c in CMDS:
                r = subprocess.run(c, cwd=WT, env=ENV, capture_output=True, text=True, timeout=2400)
                o = r.stdout + r.stderr
                outs += o
                if r.returncode != 0 and ("error[" in o or "could not compile" in o):
                    nocompile = True
            failed = re.findall(r"^test (\S+) \.\.\. FAILED", outs, re.M)
            panics = re.findall(r"panicked at [^\n]*\n([^\n]*)", outs)
            status = "NO-COMPILE" if nocompile and not failed else ("RED" if failed else "SURVIVED")
            if nocompile:
                errs = re.findall(r"^error(?:\[\w+\])?: [^\n]*", outs, re.M)
                panics = errs[:2] + panics
    finally:
        for p, src in origs.items():
            open(p, "w", encoding="utf-8").write(src)
    print(f"[{status:10}] {mid} {prop}  ({time.time()-t0:.0f}s)")
    if failed:
        print("     failed: " + "; ".join(failed[:6]) + (f" (+{len(failed)-6})" if len(failed) > 6 else ""))
    for pm in panics[:2]:
        print("     says: " + pm.strip()[:220])
    sys.stdout.flush()
after = {f: h(f) for f in files}
print("sources restored byte-for-byte" if before == after else "PROBLEM: a source differs after the run")
