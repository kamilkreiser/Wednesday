#!/usr/bin/env python3
"""QA gate: the gate's own mutations on the RELAY-IDENTITY code. Each mutation is applied alone to
a scratch worktree, the new code's tests run (coagent-cli: all targets; coagent-relay: identity_blob
and the lib unit tests), and the result is RED (some test failed: names and first panic line kept),
SURVIVED, or NO-COMPILE. The source is restored after each row and checked by hash at the end.

usage: mutate.py <worktree> [ids...]
"""
import hashlib, os, re, subprocess, sys, time

WT = sys.argv[1]
ONLY = set(sys.argv[2:])
C = "crates/coagent-cli/src/"
R = "crates/coagent-relay/src/"

MUTS = [
 ("G01", "parent must be a directory: check removed", C+"identity_file.rs", "if !dmd.is_dir() {", "if false {"),
 ("G02", "parent mode: OTHER bits ignored (mask 0o070)", C+"identity_file.rs", "if dmode & 0o077 != 0 {", "if dmode & 0o070 != 0 {"),
 ("G03", "parent mode: GROUP bits ignored (mask 0o007)", C+"identity_file.rs", "if dmode & 0o077 != 0 {", "if dmode & 0o007 != 0 {"),
 ("G04", "file mode: OTHER bits ignored (mask 0o070)", C+"identity_file.rs", "if mode & 0o077 != 0 {", "if mode & 0o070 != 0 {"),
 ("G05", "file mode: GROUP bits ignored (mask 0o007)", C+"identity_file.rs", "if mode & 0o077 != 0 {", "if mode & 0o007 != 0 {"),
 ("G06", "file mode: only read bits checked (mask 0o044)", C+"identity_file.rs", "if mode & 0o077 != 0 {", "if mode & 0o044 != 0 {"),
 ("G07", "directory-at-path branch removed (falls to not-regular)", C+"identity_file.rs", "if ft.is_dir() {", "if false {"),
 ("G08", "regular-file check removed (a FIFO would be opened)", C+"identity_file.rs", "if !ft.is_file() {", "if false {"),
 ("G09", "size cap off by one (>= : a file of exactly the cap refused)", C+"identity_file.rs", "if md.len() > IDENTITY_FILE_MAX {", "if md.len() >= IDENTITY_FILE_MAX {"),
 ("G10", "size cap loosened to 1 MiB in the pre-read check", C+"identity_file.rs", "if md.len() > IDENTITY_FILE_MAX {", "if md.len() > 1 << 20 {"),
 ("G11", "file read bound loosened (take cap+1 -> 1 MiB)", C+"identity_file.rs", "(&f).take(IDENTITY_FILE_MAX + 1)", "(&f).take(1 << 20)"),
 ("G12", "post-read bound removed (builder: equivalent)", C+"identity_file.rs", "if buf.len() as u64 > IDENTITY_FILE_MAX {", "if false {"),
 ("G13", "fd re-check (fstat) removed", C+"identity_file.rs", "    check_file(path, &fmd, uid)?;\n", "\n"),
 ("G14", "temp file not exclusive (create+truncate)", C+"identity_file.rs", ".create_new(true)", ".create(true).truncate(true)"),
 ("G15", "temp file created 0660", C+"identity_file.rs", ".mode(0o600)", ".mode(0o660)"),
 ("G16", "temp name leaked on success (forget the guard)", C+"identity_file.rs", "    drop(tmp);\n    Ok(())", "    std::mem::forget(tmp);\n    Ok(())"),
 ("G17", "file fsync removed", C+"identity_file.rs", ".and_then(|()| f.sync_all())", ""),
 ("G18", "parent judged without following a link (stricter)", C+"identity_file.rs", "let dmd = match fs::metadata(dir) {", "let dmd = match fs::symlink_metadata(dir) {"),
 ("G19", "the GRANDPARENT is checked instead of the parent", C+"identity_file.rs", "Some(p) if !p.as_os_str().is_empty() => p,", "Some(p) if !p.as_os_str().is_empty() => p.parent().unwrap_or(p),"),
 ("G20", "current uid = the group id", C+"identity_file.rs", "Ok(a.peer_cred()?.uid())", "Ok(a.peer_cred()?.gid())"),
 ("G21", "AlreadyExists on link reported as a generic I/O error", C+"identity_file.rs", "Err(e) if e.kind() == io::ErrorKind::AlreadyExists => {", "Err(e) if false && e.kind() == io::ErrorKind::AlreadyExists => {"),
 ("G22", "a load that hits NotFound (race) ... create on any metadata error", C+"identity_file.rs", "Err(e) if e.kind() == io::ErrorKind::NotFound => {\n            let mut ips", "Err(_) => {\n            let mut ips"),
 ("G23", "stdin: empty input not reported as Nothing", C+"identity_stdin.rs", "Ok(Ok(_)) if buf.is_empty() => Err(StdinError::Nothing),", ""),
 ("G24", "stdin: TooLarge test off (left to from_blob)", C+"identity_stdin.rs", "Ok(Ok(_)) if buf.len() > IDENTITY_BLOB_MAX => Err(StdinError::TooLarge {", "Ok(Ok(_)) if false => Err(StdinError::TooLarge {"),
 ("G25", "stdin deadline constant 5 s -> 30 s", C+"identity_stdin.rs", "Duration::from_secs(5);", "Duration::from_secs(30);"),
 ("G26", "stdin cap loosened (cap+1 -> 1 MiB)", C+"identity_stdin.rs", "let mut limited = r.take(IDENTITY_BLOB_MAX as u64 + 1);", "let mut limited = r.take(1 << 20);"),
 ("G27", "caller passes a one-day deadline", C+"relay_cmd.rs", "crate::identity_stdin::IDENTITY_STDIN_DEADLINE,", "std::time::Duration::from_secs(86_400),"),
 ("G28", "any version line accepted", R+"tls.rs", "if line == IDENTITY_BLOB_HEADER {", "if line.starts_with(IDENTITY_BLOB_MAGIC) {"),
 ("G29", "unknown version reported as wrong header", R+"tls.rs", "} else if line.starts_with(IDENTITY_BLOB_MAGIC) {", "} else if false {"),
 ("G30", "no newline: always 'truncated header'", R+"tls.rs", "None if IDENTITY_BLOB_HEADER.starts_with(blob) =>", "None if true =>"),
 ("G31", "InconsistentKeys::Unknown passes (as rustls does)", R+"tls.rs", "Err(rustls::Error::InconsistentKeys(_)) => {", "Err(rustls::Error::InconsistentKeys(rustls::InconsistentKeys::Unknown)) => Ok(()),\n        Err(rustls::Error::InconsistentKeys(_)) => {"),
 ("G32", "unparseable certificate accepted", R+"tls.rs", "Err(_) => Err(IdentityBlobError::UnusableCertificate),", "Err(_) => Ok(()),"),
 ("G33", "fingerprint computed over the key, not the stored certificate", R+"tls.rs", "let fingerprint = Fingerprint(sha256(cert.as_ref()));\n        Ok(TlsIdentity {\n            cert,\n            key_pkcs8: key.to_vec(),", "let fingerprint = Fingerprint(sha256(key));\n        Ok(TlsIdentity {\n            cert,\n            key_pkcs8: key.to_vec(),"),
 ("G34", "export cap check removed", R+"tls.rs", "if len > IDENTITY_BLOB_MAX {\n            return Err(IdentityBlobError::TooLarge { len });", "if false {\n            return Err(IdentityBlobError::TooLarge { len });"),
 ("G35", "export writes the certificate length for both parts", R+"tls.rs", "v.extend_from_slice(&(part.len() as u32).to_be_bytes());", "v.extend_from_slice(&(cert.len() as u32).to_be_bytes());"),
 ("G36", "IdentityBlob Debug prints its bytes", R+"tls.rs", 'write!(f, "IdentityBlob({} bytes, redacted)", self.0.len())', 'write!(f, "IdentityBlob({:?})", self.0)'),
 ("G37", "import cap off by one (> -> >= : a blob of exactly the cap refused)", R+"tls.rs", "if blob.len() > IDENTITY_BLOB_MAX {", "if blob.len() >= IDENTITY_BLOB_MAX {"),
 ("G38", "a path starting with '-' accepted", C+"args.rs", "if v.is_empty() || v.starts_with('-') {", "if v.is_empty() {"),
 ("G39", "--identity-stdin overrides silently (no exclusivity on this side)", C+"args.rs", '"--identity-stdin" => set_identity(&mut o.identity, IdentitySource::Stdin)?,', '"--identity-stdin" => o.identity = IdentitySource::Stdin,'),
 ("G40", "resolved identity not handed to the relay", C+"relay_cmd.rs", "    cfg.identity = identity;\n", "    let _ = identity;\n"),
 ("G41", "identity refusal exits 0", C+"relay_cmd.rs", 'eprintln!("coagent relay: nothing was started");\n            return 1;', 'eprintln!("coagent relay: nothing was started");\n            return 0;'),
 ("G42", "identity line printed BEFORE the banner", C+"relay_cmd.rs", "    print_banner(&handle, &opts);\n    if let Some(line) = &identity_line {\n        println!(\"{line}\");\n    }", "    if let Some(line) = &identity_line {\n        println!(\"{line}\");\n    }\n    print_banner(&handle, &opts);"),
 ("G43", "Windows branch compiled on unix (cfgs swapped)", C+"relay_cmd.rs", "#[cfg(unix)]\nasync fn file_identity", "#[cfg(any())]\nasync fn file_identity"),
 ("G44", "the stdin error text carries the raw error kind of rustls (n/a) -> file error prints the blob length only", C+"identity_file.rs", 'Blob { path, err, .. } => write!(f, "{}: the identity file is not a usable relay identity: {err}", path.display()),', 'Blob { path, err, bytes_read } => write!(f, "{}: the identity file is not a usable relay identity: {err} ({bytes_read} bytes: {:?})", path.display(), std::fs::read(path).unwrap_or_default()),'),
]
# G43 also needs the not-unix branch switched on:
EXTRA = {"G43": (C+"relay_cmd.rs", "#[cfg(not(unix))]\nasync fn file_identity", "#[cfg(all())]\nasync fn file_identity")}

ENV = dict(os.environ)
CMDS = [["cargo", "test", "--locked", "--offline", "-p", "coagent-cli", "--no-fail-fast"],
        ["cargo", "test", "--locked", "--offline", "-p", "coagent-relay", "--no-fail-fast", "--test", "identity_blob", "--lib"]]


def h(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


files = sorted({os.path.join(WT, m[2]) for m in MUTS})
before = {f: h(f) for f in files}
for mid, prop, rel, old, new in MUTS:
    if ONLY and mid not in ONLY:
        continue
    edits = [(rel, old, new)] + ([EXTRA[mid]] if mid in EXTRA else [])
    origs = {}
    bad = None
    for r, o, n in edits:
        p = os.path.join(WT, r)
        src = origs.get(p) or open(p, encoding="utf-8").read()
        origs.setdefault(p, src)
        cur = open(p, encoding="utf-8").read()
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
                r = subprocess.run(c, cwd=WT, env=ENV, capture_output=True, text=True, timeout=1800)
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
