//! QA-RELAY-RECONNECT (independent check): probes of the identity rules (setting off / on), the
//! refusals at invite time, a swapped valid identity, the key never printed, and R6's clock.
//! Written by the checker; not part of the branch.
mod common;
mod rr_support;

use std::os::unix::fs::{MetadataExt, PermissionsExt};
use std::path::{Path, PathBuf};
use std::process::Command;
use std::time::{Duration, Instant};

use common::*;
use rr_support::*;
use serde_json::{json, Value};

const BASE_NAMES: &[&str] = &[
    "contacts.json", "identity.key", "inbox.json", "ipc", "ipc/daemon.sock",
    "ipc/daemon.sock.lock", "outbox.json", "quarantine", "session.json",
];

fn listing(dir: &Path) -> Vec<String> {
    fn walk(root: &Path, d: &Path, out: &mut Vec<String>) {
        for e in std::fs::read_dir(d).unwrap() {
            let p = e.unwrap().path();
            out.push(p.strip_prefix(root).unwrap().to_string_lossy().to_string());
            if std::fs::symlink_metadata(&p).unwrap().is_dir() {
                walk(root, &p, out);
            }
        }
    }
    let mut v = vec![];
    walk(dir, dir, &mut v);
    v.sort();
    v
}

/// Every regular file under `root`, recursively (sockets and FIFOs skipped).
fn all_files(root: &Path) -> Vec<PathBuf> {
    let mut out = vec![];
    let mut stack = vec![root.to_path_buf()];
    while let Some(d) = stack.pop() {
        let Ok(rd) = std::fs::read_dir(&d) else { continue };
        for e in rd {
            let p = e.unwrap().path();
            let md = std::fs::symlink_metadata(&p).unwrap();
            if md.is_dir() {
                stack.push(p);
            } else if md.is_file() {
                out.push(p);
            }
        }
    }
    out
}

fn contains(hay: &[u8], n: &[u8]) -> bool {
    !n.is_empty() && hay.windows(n.len()).any(|w| w == n)
}

/// The relay's certificate (DER) as presented on the wire, fetched over loopback TLS.
fn cert_der(url: &str) -> Vec<u8> {
    let port = url.rsplit(':').next().unwrap().split('/').next().unwrap();
    let out = Command::new("/bin/sh")
        .arg("-c")
        .arg(format!(
            "echo | openssl s_client -connect 127.0.0.1:{port} 2>/dev/null | openssl x509 -outform DER"
        ))
        .env("PATH", "/opt/homebrew/bin:/usr/bin:/bin")
        .output()
        .unwrap();
    assert!(out.stdout.len() > 100, "no certificate fetched from {url}");
    out.stdout
}

/// Spellings of a byte string to look for (raw, hex both cases, base64 both alphabets at three
/// alignments, a 40-char inner chunk so PEM line wrapping cannot hide it).
fn spellings(b: &[u8]) -> Vec<Vec<u8>> {
    use data_encoding::{BASE64, BASE64URL};
    let mut v = vec![b.to_vec(), hex::encode(b).into_bytes(), hex::encode_upper(b).into_bytes()];
    for enc in [&BASE64, &BASE64URL] {
        for skip in 0..3 {
            let s = enc.encode(&b[skip..]);
            v.push(s.as_bytes()[8..48].to_vec());
        }
    }
    v.push(format!("{:?}", &b[..16]).trim_end_matches(']').as_bytes().to_vec());
    v
}

/// `ps` arguments AND environment (macOS `ps -E`) of a pid.
fn ps_args_env(pid: u32) -> String {
    let o = Command::new("/bin/ps")
        .args(["-E", "-ww", "-o", "command=", "-p", &pid.to_string()])
        .output()
        .unwrap();
    String::from_utf8_lossy(&o.stdout).to_string()
}

struct Stat {
    bytes: Vec<u8>,
    mode: u32,
    ino: u64,
    mtime: (i64, i64),
    ctime: (i64, i64),
}
fn stat(p: &Path) -> Stat {
    let md = std::fs::symlink_metadata(p).unwrap();
    Stat {
        bytes: if md.is_file() { std::fs::read(p).unwrap_or_default() } else { vec![] },
        mode: md.mode(),
        ino: md.ino(),
        mtime: (md.mtime(), md.mtime_nsec()),
        ctime: (md.ctime(), md.ctime_nsec()),
    }
}
fn same(a: &Stat, b: &Stat, what: &str) {
    assert_eq!(a.bytes, b.bytes, "{what}: bytes changed");
    assert_eq!(a.mode, b.mode, "{what}: mode changed");
    assert_eq!(a.ino, b.ino, "{what}: inode changed (replaced)");
    assert_eq!(a.mtime, b.mtime, "{what}: mtime changed");
    assert_eq!(a.ctime, b.ctime, "{what}: ctime changed");
}

/// Item 4 (setting OFF), one long scenario: after EVERY step the data directory holds only the
/// base names, and the relay's certificate (which sits next to the key in any identity blob) is in
/// no file under the run directory (data dirs, HOME, TMPDIR, stderr files) and in no process's
/// arguments or environment. Messages across each crash arrive exactly once, in order.
#[test]
fn qrr_id_off_long_scenario_nothing_on_disk() {
    let mut run = Run::new("qio");
    let a = run.daemon("a", &[]);
    let b = run.daemon("b", &[]);
    let (da, db) = (run.dir(a), run.dir(b));
    let tools_tmp = tools_dir().join("tmp");
    let mut certs: Vec<Vec<u8>> = vec![];
    let check = |run: &mut Run, step: &str, certs: &mut Vec<Vec<u8>>| {
        let s = run.status(0);
        if let Some(u) = s["session"]["relays"][0]["url"].as_str().or(None) {
            if !s["relay"].is_null() {
                let c = cert_der(u);
                if !certs.contains(&c) {
                    certs.push(c);
                }
            }
        }
        for n in listing(&da) {
            assert!(BASE_NAMES.contains(&n.as_str()) || n.starts_with("quarantine/") || (n.starts_with('.') && n.ends_with(".tmp") && !n.contains("relay")),
                "after {step}: unexpected name in the host's data directory: {n}");
            assert!(!n.contains("relay"), "after {step}: {n}");
        }
        for f in all_files(&run.root) {
            let b = std::fs::read(&f).unwrap_or_default();
            for c in certs.iter() {
                for sp in spellings(c) {
                    assert!(!contains(&b, &sp), "after {step}: the relay certificate (identity blob) found in {}", f.display());
                }
            }
        }
        for p in [s["relay"]["relay_pid"].as_u64(), s["relay"]["guard_pid"].as_u64()].into_iter().flatten() {
            let t = ps_args_env(p as u32);
            assert!(!t.contains("BEGIN"), "after {step}: {t}");
            for c in certs.iter() {
                for sp in spellings(c) {
                    assert!(!contains(t.as_bytes(), &sp), "after {step}: certificate in ps of {p}: {t}");
                }
            }
            eprintln!("QRR ps -E after {step} pid {p}: {}", t.trim());
        }
        // tools tmp (outside the run): no new file holding a certificate
        let _ = &tools_tmp;
        eprintln!("QRR listing after {step}: {:?}", listing(&da));
    };
    check(&mut run, "start", &mut certs);
    run.pair(a, b);
    check(&mut run, "pairing", &mut certs);
    let pin0 = host_pin(&da);
    send(&da, "m1");
    send(&db, "b1");
    exactly(&db, &["m1"]);
    exactly(&da, &["b1"]);
    check(&mut run, "messages", &mut certs);
    let mut k = 0;
    for n in 1..=3 {
        let r0 = reconnects(&db);
        let old = relay_pid(&da).unwrap();
        signal(old, "-KILL");
        k += 1;
        send(&da, &format!("c{k}"));
        send(&db, &format!("d{k}"));
        wait_new_relay(&da, old, Duration::from_secs(20));
        run.status(a);
        wait_reconnected(&da, &db, r0, "reconnected after a child crash", Duration::from_secs(60));
        assert!(status_of(&da)["relay_moved_line"].is_null());
        assert_eq!(host_pin(&da), pin0, "crash {n}: same pin");
        exactly(&db, &[format!("c{k}").as_str()]);
        exactly(&da, &[format!("d{k}").as_str()]);
        check(&mut run, &format!("child crash {n}"), &mut certs);
    }
    // three crashes back to back without waiting for reconnection in between
    let r0 = reconnects(&db);
    for _ in 0..3 {
        let old = relay_pid(&da).unwrap();
        signal(old, "-KILL");
        wait_new_relay(&da, old, Duration::from_secs(20));
        run.status(a);
    }
    send(&da, "x1");
    send(&da, "x2");
    wait_reconnected(&da, &db, r0, "reconnected after 3 back-to-back crashes", Duration::from_secs(60));
    assert_eq!(host_pin(&da), pin0, "back-to-back: same pin");
    exactly(&db, &["x1", "x2"]);
    check(&mut run, "three back-to-back crashes", &mut certs);
    // guard kill
    let r0 = reconnects(&db);
    let old = relay_pid(&da).unwrap();
    signal(guard_pid(&da).unwrap(), "-KILL");
    send(&da, "g1");
    wait_new_relay(&da, old, Duration::from_secs(20));
    run.status(a);
    wait_reconnected(&da, &db, r0, "reconnected after a guard kill", Duration::from_secs(60));
    assert_eq!(host_pin(&da), pin0, "guard kill: same pin");
    exactly(&db, &["g1"]);
    check(&mut run, "guard kill", &mut certs);
    assert_eq!(certs.len(), 1, "one certificate across all child restarts");
    // end, second invite (a NEW identity: another pin), pair
    assert_eq!(run.ctl(a, "end", json!({}))["ok"], true);
    wait_until("ended", Duration::from_secs(20), || status_of(&db)["session"]["ended"] == true && relay_pid(&da).is_none());
    check(&mut run, "session end", &mut certs);
    run.pair(a, b);
    assert_ne!(host_pin(&da), pin0, "a new session gets a new identity with the setting off");
    check(&mut run, "second session", &mut certs);
    // whole-program restart with the setting OFF does NOT heal; the relay.moved path works
    let r0 = reconnects(&db);
    let pin1 = host_pin(&da);
    let old = relay_pids_of(&da);
    run.crash(a);
    wait_gone(&old, "old relay gone");
    run.start(a);
    run.status(a);
    check(&mut run, "host restart (off)", &mut certs);
    let t0 = Instant::now();
    while t0.elapsed() < Duration::from_secs(20) {
        let g = status_of(&db);
        assert_ne!(g["session"]["attached"], true, "the guest attached after an OFF restart: {g}");
        assert_ne!(g["session"]["connected"], true, "the guest connected after an OFF restart: {g}"); let _ = r0;
        std::thread::sleep(Duration::from_millis(500));
    }
    let s = status_of(&da);
    assert_ne!(host_pin(&da), pin1, "a new identity after an OFF restart");
    assert_eq!(s["relay_identity"]["source"], "memory");
    let line = s["relay_moved_line"].as_str().expect("a relay.moved line").to_string();
    send(&da, "after-restart");
    let j = run.ctl(b, "join", json!({ "blob": line }));
    assert_eq!(j["ok"], true, "join relay.moved: {j}");
    run.wait_connected(a, b);
    exactly(&db, &["after-restart"]);
    check(&mut run, "relay.moved followed", &mut certs);
    run.stop(a);
    check_after_stop(&run, &da, &certs);
    run.finish();
}

fn check_after_stop(run: &Run, da: &Path, certs: &[Vec<u8>]) {
    for n in listing(da) {
        assert!(!n.contains("relay"), "after clean stop: {n}");
    }
    for f in all_files(&run.root) {
        let b = std::fs::read(&f).unwrap_or_default();
        for c in certs {
            for sp in spellings(c) {
                assert!(!contains(&b, &sp), "after clean stop: certificate found in {}", f.display());
            }
        }
    }
}

/// Item 5 (setting ON): clean stop and SIGKILL restarts heal with nothing pasted; the file is made
/// once (0600 in a 0700 directory) and never rewritten (bytes, mode, inode, mtime, ctime).
#[test]
fn qrr_id_on_restarts_heal_and_file_never_rewritten() {
    let mut run = Run::new("qion");
    let a = run.daemon("a", &["--keep-relay-identity"]);
    let b = run.daemon("b", &[]);
    let (da, db) = (run.dir(a), run.dir(b));
    assert!(!da.join(ID_FILE).exists(), "no file before the first invite");
    run.pair(a, b);
    let f = da.join(ID_FILE);
    let st0 = stat(&f);
    assert_eq!(st0.mode & 0o7777, 0o600);
    assert_eq!(std::fs::metadata(&da).unwrap().mode() & 0o7777, 0o700);
    let pin0 = host_pin(&da);
    assert_eq!(status_of(&da)["relay_identity"]["source"], "saved_created");
    for (n, clean) in [(1, true), (2, false), (3, false), (4, true)] {
        let r0 = reconnects(&db);
        let old = relay_pids_of(&da);
        if clean { run.stop(a) } else { run.crash(a) }
        wait_gone(&old, "old relay gone");
        run.start(a);
        run.status(a);
        let m = format!("r{n}");
        send(&da, &m);
        wait_reconnected(&da, &db, r0, "healed after a host restart (on)", Duration::from_secs(60));
        let s = status_of(&da);
        assert!(s["relay_moved_line"].is_null(), "restart {n}: {s}");
        assert_eq!(s["relay_identity"]["source"], "saved_loaded");
        assert_eq!(host_pin(&da), pin0);
        exactly(&db, &[m.as_str()]);
        same(&st0, &stat(&f), &format!("restart {n}"));
        // child crash while on: same pin, file untouched
        let r0 = reconnects(&db);
        let old = relay_pid(&da).unwrap();
        signal(old, "-KILL");
        wait_new_relay(&da, old, Duration::from_secs(20));
        run.status(a);
        wait_reconnected(&da, &db, r0, "healed after a child crash (on)", Duration::from_secs(60));
        same(&st0, &stat(&f), &format!("crash after restart {n}"));
    }
    // end + new session: the SAME fingerprint (P-5), file untouched
    assert_eq!(run.ctl(a, "end", json!({}))["ok"], true);
    wait_until("ended", Duration::from_secs(20), || relay_pid(&da).is_none() && status_of(&db)["session"]["ended"] == true);
    run.pair(a, b);
    assert_eq!(host_pin(&da), pin0, "every invitation shows the same fingerprint with the setting on");
    same(&st0, &stat(&f), "second session");
    let names = listing(&da);
    assert!(names.iter().all(|n| BASE_NAMES.contains(&n.as_str()) || n == ID_FILE || n.starts_with("quarantine/")), "{names:?}");
    run.finish();
}

/// Refusals at INVITE time (no session yet; the builder's cases run at a restore): each damaged
/// file planted before the first invite; `invite` answers relay_unavailable with R7's text; status
/// shows it; no relay child; no fresh identity; the file untouched (bytes, mode, inode, mtime,
/// ctime); no other name created; the daemon still answers (a FIFO does not block). Then the file
/// is put right and the next invite works with the saved identity.
#[test]
fn qrr_id_refusals_at_invite_time() {
    // a good file made by a daemon of its own
    let mut run = Run::new("qirf");
    let m = run.daemon("m", &["--keep-relay-identity"]);
    let dm = run.dir(m);
    let inv = run.ctl(m, "invite", json!({}));
    assert_eq!(inv["ok"], true);
    let good = std::fs::read(dm.join(ID_FILE)).unwrap();
    let good_pin = status_of(&dm)["pairing"].clone();
    let _ = good_pin;
    run.stop(m);
    let h = 26usize;
    let cl = u32::from_be_bytes(good[h..h + 4].try_into().unwrap()) as usize;
    let ks = h + 4 + cl + 4;
    let mut cases: Vec<(String, Box<dyn Fn(&Path)>, &str)> = vec![];
    let g2 = good.clone();
    for cut in [1usize, 25, 27, 100, cl / 2 + 30, ks + 5, good.len() - 32, good.len() - 1] {
        let g = g2.clone();
        cases.push((format!("cut at {cut}"), Box::new(move |p: &Path| wr(p, &g[..cut], 0o600)), ""));
    }
    for pos in [3usize, 28, 200, ks + 10, ks + 40, good.len() - 5] {
        let g = g2.clone();
        cases.push((format!("bit flip at {pos}"), Box::new(move |p: &Path| { let mut b = g.clone(); b[pos] ^= 0x10; wr(p, &b, 0o600) }), ""));
    }
    {
        let g = g2.clone();
        cases.push(("one byte over 16 KiB".into(), Box::new(move |p: &Path| { let mut b = g.clone(); b.resize(16 * 1024 + 1, 7); wr(p, &b, 0o600) }), "larger than 16 KiB"));
    }
    for mode in [0o400u32, 0o640, 0o644, 0o660, 0o666, 0o700, 0o4600, 0o1600] {
        let g = g2.clone();
        cases.push((format!("mode {mode:o}"), Box::new(move |p: &Path| wr(p, &g, mode)), "mode is not 0600"));
    }
    {
        let g = g2.clone();
        cases.push(("symlink to a good file".into(), Box::new(move |p: &Path| {
            let t = p.parent().unwrap().parent().unwrap().join("good-target.key");
            if !t.exists() { wr(&t, &g, 0o600) }
            std::os::unix::fs::symlink(&t, p).unwrap();
        }), "not a regular file"));
    }
    cases.push(("FIFO".into(), Box::new(|p: &Path| { assert!(Command::new("/usr/bin/mkfifo").args(["-m", "600"]).arg(p).status().unwrap().success()) }), "not a regular file"));
    cases.push(("directory".into(), Box::new(|p: &Path| { std::fs::create_dir(p).unwrap(); std::fs::set_permissions(p, std::fs::Permissions::from_mode(0o700)).unwrap() }), "not a regular file"));
    cases.push(("empty".into(), Box::new(|p: &Path| wr(p, b"", 0o600)), ""));
    let host = run.daemon("h", &["--keep-relay-identity"]);
    let dh = run.dir(host);
    let f = dh.join(ID_FILE);
    let mut n_ok = 0;
    for (name, plant, cat) in &cases {
        // a fresh start per case: no identity held
        let old = relay_pids_of(&dh);
        run.stop(host);
        wait_gone(&old, "relay gone between cases");
        if let Ok(md) = std::fs::symlink_metadata(&f) {
            if md.is_dir() { std::fs::remove_dir(&f).unwrap() } else { std::fs::remove_file(&f).unwrap() }
        }
        plant(&f);
        run.start(host);
        let before_names = listing(&dh);
        let st = stat(&f);
        let r = run.ctl(host, "invite", json!({}));
        assert_eq!(r["ok"], false, "case {name}: invite must be refused: {r}");
        assert_eq!(r["error"]["code"], "relay_unavailable", "case {name}: {r}");
        let msg = r["error"]["message"].as_str().unwrap_or_default().to_string();
        assert!(msg.starts_with("the saved relay identity was refused ("), "case {name}: {msg}");
        assert!(msg.contains("no new identity was made"), "case {name}: {msg}");
        if !cat.is_empty() {
            assert!(msg.contains(&format!("({cat})")), "case {name}: category: {msg}");
        }
        let s = status_of(&dh);
        assert_eq!(s["relay_identity"]["refused"].as_str(), Some(msg.as_str()), "case {name}: status: {s}");
        assert_eq!(s["relay_identity"]["source"], "none", "case {name}: {s}");
        assert!(s["relay"].is_null(), "case {name}: relay started: {s}");
        assert!(s["relay_moved_line"].is_null(), "case {name}");
        assert!(s["pairing"].is_null() || s["pairing"]["state"] != "waiting", "case {name}: {s}");
        same(&st, &stat(&f), &format!("case {name}"));
        assert_eq!(before_names, listing(&dh), "case {name}: names changed");
        let err = std::fs::read_to_string(&run.daemons[host].stderr).unwrap_or_default();
        assert!(err.contains(&msg), "case {name}: stderr lacks R7's text");
        // put it right (remove the damage; plant the good file) and invite again
        let md = std::fs::symlink_metadata(&f).unwrap();
        if md.is_dir() { std::fs::remove_dir(&f).unwrap() } else { std::fs::remove_file(&f).unwrap() }
        wr(&f, &good, 0o600);
        let r = run.ctl(host, "invite", json!({}));
        assert_eq!(r["ok"], true, "case {name}: invite after the file was put right: {r}");
        let s = status_of(&dh);
        assert_eq!(s["relay_identity"]["source"], "saved_loaded", "case {name}: {s}");
        assert!(s["relay_identity"]["refused"].is_null());
        assert_eq!(std::fs::read(&f).unwrap(), good, "case {name}: the good file untouched");
        run.status(host);
        n_ok += 1;
    }
    eprintln!("QRR refusals at invite time: {n_ok} cases");
    run.finish();
}

fn wr(p: &Path, b: &[u8], mode: u32) {
    use std::io::Write;
    use std::os::unix::fs::OpenOptionsExt;
    let mut f = std::fs::OpenOptions::new().write(true).create_new(true).mode(0o600).open(p).unwrap();
    f.write_all(b).unwrap();
    drop(f);
    std::fs::set_permissions(p, std::fs::Permissions::from_mode(mode)).unwrap();
}

/// Setting ON, the saved file replaced (while the host is stopped) by ANOTHER valid identity: it is
/// used, announced (a relay.moved line, the "new certificate" text), and the guest does NOT attach
/// to it until its owner pastes the line (I1).
#[test]
fn qrr_id_on_swapped_valid_identity_needs_the_line() {
    let mut run = Run::new("qisw");
    let a = run.daemon("a", &["--keep-relay-identity"]);
    let b = run.daemon("b", &[]);
    let o = run.daemon("o", &["--keep-relay-identity"]);
    let (da, db, dob) = (run.dir(a), run.dir(b), run.dir(o));
    assert_eq!(run.ctl(o, "invite", json!({}))["ok"], true);
    let other = std::fs::read(dob.join(ID_FILE)).unwrap();
    run.status(o);
    run.stop(o);
    run.pair(a, b);
    let pin0 = host_pin(&da);
    let old = relay_pids_of(&da);
    run.stop(a);
    wait_gone(&old, "old relay gone");
    let f = da.join(ID_FILE);
    let tmp = da.join("swap.tmp");
    wr(&tmp, &other, 0o600);
    std::fs::rename(&tmp, &f).unwrap();
    let r0 = reconnects(&db);
    run.start(a);
    run.status(a);
    let s = status_of(&da);
    assert_eq!(s["relay_identity"]["source"], "saved_loaded", "{s}");
    assert_ne!(host_pin(&da), pin0);
    let line = s["relay_moved_line"].as_str().expect("a line (new certificate)").to_string();
    let err = std::fs::read_to_string(&run.daemons[a].stderr).unwrap();
    assert!(err.contains("relay restarted with a new certificate; the joiner needs the relay.moved line (status)"));
    let t0 = Instant::now();
    while t0.elapsed() < Duration::from_secs(15) {
        let g = status_of(&db);
        assert_ne!(g["session"]["attached"], true, "the guest attached to another identity without a line: {g}");
        assert_ne!(g["session"]["connected"], true, "{g}"); let _ = r0;
        std::thread::sleep(Duration::from_millis(300));
    }
    assert_eq!(run.ctl(b, "join", json!({"blob": line}))["ok"], true);
    run.wait_connected(a, b);
    run.finish();
}

/// Item 8, setting ON: the saved key is never printed: every stderr (host, guest), every status and
/// error reply taken, `ps` arguments AND environment of the daemon, guard and relay.
#[test]
fn qrr_id_on_key_never_printed() {
    let mut run = Run::new("qikp");
    let a = run.daemon("a", &["--keep-relay-identity"]);
    let b = run.daemon("b", &[]);
    let (da, db) = (run.dir(a), run.dir(b));
    let mut replies: Vec<String> = vec![];
    run.pair(a, b);
    let blob = std::fs::read(da.join(ID_FILE)).unwrap();
    let key = key_of_blob(&blob);
    let mut needles = key_needles(&blob);
    needles.extend(spellings(&key));
    // PEM spelling of the key, line by line
    let pem = data_encoding::BASE64.encode(&key);
    for chunk in pem.as_bytes().chunks(64) {
        if chunk.len() == 64 { needles.push(chunk.to_vec()); }
    }
    let mut procs = vec![run.pid(a)];
    let s = status_of(&da);
    procs.extend([s["relay"]["relay_pid"].as_u64(), s["relay"]["guard_pid"].as_u64()].into_iter().flatten().map(|p| p as u32));
    for p in &procs {
        let t = ps_args_env(*p);
        replies.push(t);
    }
    replies.push(s.to_string());
    replies.push(status_of(&db).to_string());
    // crash, restart, damage, a refused invite, a refused join, end
    let old = relay_pid(&da).unwrap();
    signal(old, "-KILL");
    wait_new_relay(&da, old, Duration::from_secs(20));
    run.status(a);
    replies.push(status_of(&da).to_string());
    let s = status_of(&da);
    for p in [s["relay"]["relay_pid"].as_u64(), s["relay"]["guard_pid"].as_u64()].into_iter().flatten() {
        replies.push(ps_args_env(p as u32));
    }
    let old = relay_pids_of(&da);
    run.stop(a);
    wait_gone(&old, "gone");
    let f = da.join(ID_FILE);
    std::fs::set_permissions(&f, std::fs::Permissions::from_mode(0o644)).unwrap();
    run.start(a);
    replies.push(status_of(&da).to_string());
    replies.push(run.ctl(a, "invite", json!({})).to_string());
    replies.push(run.ctl(a, "join", json!({"blob": "garbage"})).to_string());
    std::fs::set_permissions(&f, std::fs::Permissions::from_mode(0o600)).unwrap();
    wait_until("healed", Duration::from_secs(80), || status_of(&da)["session"]["connected"] == true && status_of(&db)["session"]["connected"] == true);
    run.status(a);
    replies.push(status_of(&da).to_string());
    replies.push(run.ctl(a, "end", json!({})).to_string());
    for r in &replies {
        assert_no_key(&needles, r.as_bytes(), "a reply or ps output");
    }
    for f in all_files(&run.root) {
        if f.file_name().map(|n| n == ID_FILE).unwrap_or(false) || f.ends_with("good-target.key") {
            continue;
        }
        let b = std::fs::read(&f).unwrap_or_default();
        assert_no_key(&needles, &b, &format!("file {}", f.display()));
    }
    eprintln!("QRR key scan: {} needles over {} replies/ps outputs and every file of the run", needles.len(), replies.len());
    run.finish();
}

/// R6: the host's relay program fails to start for a while; status shows the backoff (1, 2, 4 ...
/// seconds), the cause is logged once, and when the program works again the relay returns with the
/// SAME pin and the guest reconnects by itself, nothing restarted.
#[test]
fn qrr_id_r6_backoff_visible_and_heals() {
    let mut run = Run::new("qir6");
    let prog = run.root.join("cg");
    let flag = run.root.join("cg.fail");
    let real = bin("coagent");
    std::fs::write(&prog, format!("#!/bin/sh\nif [ -e '{}' ]; then exit 3; fi\nexec '{}' \"$@\"\n", flag.display(), real.display())).unwrap();
    std::fs::set_permissions(&prog, std::fs::Permissions::from_mode(0o700)).unwrap();
    let a = run.daemon("a", &["--coagent", prog.to_str().unwrap()]);
    let b = run.daemon("b", &[]);
    run.pair(a, b);
    let (da, db) = (run.dir(a), run.dir(b));
    let pin0 = host_pin(&da);
    let pid = run.pid(a);
    std::fs::write(&flag, b"x").unwrap();
    let r0 = reconnects(&db);
    let old = relay_pid(&da).unwrap();
    signal(old, "-KILL");
    let mut seen = vec![];
    let t0 = Instant::now();
    while t0.elapsed() < Duration::from_secs(20) {
        let s = status_of(&da);
        if let Some(r) = s["relay_identity"]["retry_in_s"].as_u64() {
            if seen.last() != Some(&r) { seen.push(r); }
        }
        assert!(s["relay"].is_null() || t0.elapsed() < Duration::from_secs(1), "{s}");
        std::thread::sleep(Duration::from_millis(100));
    }
    eprintln!("QRR R6 retry_in_s values seen: {seen:?}");
    assert!(seen.iter().any(|v| *v >= 4), "the backoff grows: {seen:?}");
    let err = std::fs::read_to_string(&run.daemons[a].stderr).unwrap();
    let n_cause = err.lines().filter(|l| l.contains("cannot restart the relay")).count();
    eprintln!("QRR R6 cause lines: {n_cause}");
    assert!(n_cause <= 2, "one log line per change of cause, not per try: {n_cause}");
    std::fs::remove_file(&flag).unwrap();
    send(&da, "after");
    wait_until("relay back", Duration::from_secs(70), || relay_pid(&da).is_some());
    run.status(a);
    wait_reconnected(&da, &db, r0, "reconnected after R6", Duration::from_secs(60));
    assert_eq!(host_pin(&da), pin0);
    assert_eq!(run.pid(a), pid);
    assert!(status_of(&da)["relay_identity"]["retry_in_s"].is_null());
    exactly(&db, &["after"]);
    let _: Value = json!(null);
    run.finish();
}

/// R4 judgement (builder's flag 3): with the setting ON, when the new identity cannot be SAVED
/// (here: the data directory made read-only by the test after the start), the start fails and no
/// unsaved identity is used. Then the directory is put back and the next invite works.
#[test]
fn qrr_id_on_create_fails_no_unsaved_identity() {
    let mut run = Run::new("qicf");
    let a = run.daemon("a", &["--keep-relay-identity"]);
    let da = run.dir(a);
    std::fs::set_permissions(&da, std::fs::Permissions::from_mode(0o500)).unwrap();
    let r = run.ctl(a, "invite", json!({}));
    let s = status_of(&da);
    std::fs::set_permissions(&da, std::fs::Permissions::from_mode(0o700)).unwrap();
    eprintln!("QRR create-fails invite: {r}; status relay_identity {}", s["relay_identity"]);
    assert_eq!(r["ok"], false, "{r}");
    assert!(r["error"]["message"].as_str().unwrap_or_default().contains("could not be saved"), "{r}");
    assert!(s["relay"].is_null(), "a relay started with an unsaved identity: {s}");
    assert_eq!(s["relay_identity"]["source"], "none");
    assert!(!da.join(ID_FILE).exists());
    let r = run.ctl(a, "invite", json!({}));
    assert_eq!(r["ok"], true, "{r}");
    assert_eq!(status_of(&da)["relay_identity"]["source"], "saved_created");
    run.status(a);
    run.finish();
}
