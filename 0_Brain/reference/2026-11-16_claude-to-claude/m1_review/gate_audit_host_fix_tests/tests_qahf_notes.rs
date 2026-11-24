//! QA-AUDIT-HOST-FIX (the independent check of branch `audit-host-fix`, head 5b3a395): N-2 (the
//! lock) and N-4 (unreadable anchors and limits) through the public API. Written by the checker;
//! lives only in the checker's clone.
#![cfg(unix)]

mod common;

use std::os::unix::fs::{DirBuilderExt, MetadataExt, PermissionsExt};
use std::path::{Path, PathBuf};
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;
use std::time::{Duration, Instant};

use coagent_audit_host::{DirError, HostError};
use common::*;
use sha2::{Digest, Sha256};

fn put(p: &Path, bytes: &[u8]) {
    std::fs::write(p, bytes).unwrap();
    std::fs::set_permissions(p, std::fs::Permissions::from_mode(0o600)).unwrap();
}

fn made(w: &World, name: &str) -> (PathBuf, PathBuf) {
    let base = scratch(name);
    let root = base.join("host");
    let mut h = create_host(w, 1, &root, cfg(w));
    for n in 0..3 {
        host_record(&mut h, &w.ids[1], coagent_audit_host::Causer::LocalHuman, n + 1);
    }
    drop(h);
    (base, root)
}

/// `open` on a thread, with a watchdog: a hang is a failure, never a stuck test.
fn open_watched(w: &World, root: &Path) -> Result<(), String> {
    let (tx, rx) = std::sync::mpsc::channel();
    // the World is rebuilt on the thread from its base (fixed identities: the same keys)
    let b = W_BASE.with(|c| c.get());
    let _ = w;
    let root = root.to_path_buf();
    std::thread::spawn(move || {
        let w = World::new(b, 3, 3);
        let r = open_host(&w, 1, &root, cfg(&w), 10).map(|_| ());
        let _ = tx.send(r);
    });
    match rx.recv_timeout(Duration::from_secs(10)) {
        Ok(Ok(())) => Ok(()),
        Ok(Err(e)) => Err(format!("{e:?}")),
        Err(_) => Err("HANG (10 s)".into()),
    }
}

thread_local! { static W_BASE: std::cell::Cell<u8> = const { std::cell::Cell::new(0) }; }

fn mtime(p: &Path) -> (i64, i64, u64) {
    let m = std::fs::metadata(p).unwrap();
    (m.mtime(), m.mtime_nsec(), m.len())
}

/// N-2: every shape of `lock` I could plant. Nothing outside the folder is created or changed, and
/// no shape opens the folder.
#[test]
fn qahf_n2_lock_shapes() {
    let w = World::new(200, 3, 3);
    W_BASE.with(|c| c.set(200));
    let (base, root) = made(&w, "qahf-n2");
    let lock = root.join("lock");
    std::fs::rename(&lock, base.join("real-lock-aside")).unwrap();
    let mut lines = Vec::new();
    let mut bad = Vec::new();

    // (1) dangling link
    let nowhere = base.join("outside-nowhere");
    std::os::unix::fs::symlink(&nowhere, &lock).unwrap();
    let r = open_watched(&w, &root);
    lines.push(format!("dangling link: {r:?}; target created {}", nowhere.exists()));
    if nowhere.exists() || r.is_ok() {
        bad.push("dangling link");
    }
    std::fs::rename(&lock, base.join("aside-1")).unwrap();

    // (2) link to an existing outside file: content and mtime unchanged
    let outside = base.join("outside-file");
    put(&outside, b"outside, untouched");
    std::thread::sleep(Duration::from_millis(20));
    let m0 = mtime(&outside);
    std::os::unix::fs::symlink(&outside, &lock).unwrap();
    let r = open_watched(&w, &root);
    let m1 = mtime(&outside);
    let content = std::fs::read(&outside).unwrap();
    lines.push(format!(
        "link to an existing file: {r:?}; content same {}; mtime/len same {}",
        content == b"outside, untouched",
        m0 == m1
    ));
    if r.is_ok() || content != b"outside, untouched" || m0 != m1 {
        bad.push("link to file");
    }
    std::fs::rename(&lock, base.join("aside-2")).unwrap();

    // (3) link to an outside directory: nothing created inside it
    let odir = base.join("outside-dir");
    std::fs::DirBuilder::new().mode(0o700).create(&odir).unwrap();
    std::os::unix::fs::symlink(&odir, &lock).unwrap();
    let r = open_watched(&w, &root);
    let n_in = std::fs::read_dir(&odir).unwrap().count();
    lines.push(format!("link to a directory: {r:?}; entries in it {n_in}"));
    if r.is_ok() || n_in != 0 {
        bad.push("link to dir");
    }
    std::fs::rename(&lock, base.join("aside-3")).unwrap();

    // (4) a chain: lock -> link1 -> link2 -> nowhere2 (dangling at the end)
    let nowhere2 = base.join("outside-nowhere-2");
    let l2 = base.join("chain-2");
    let l1 = base.join("chain-1");
    std::os::unix::fs::symlink(&nowhere2, &l2).unwrap();
    std::os::unix::fs::symlink(&l2, &l1).unwrap();
    std::os::unix::fs::symlink(&l1, &lock).unwrap();
    let r = open_watched(&w, &root);
    lines.push(format!("chain to nowhere: {r:?}; target created {}", nowhere2.exists()));
    if r.is_ok() || nowhere2.exists() {
        bad.push("chain dangling");
    }
    std::fs::rename(&lock, base.join("aside-4")).unwrap();
    // (4b) a chain ending at an existing file
    let l3 = base.join("chain-3");
    std::os::unix::fs::symlink(&outside, &l3).unwrap();
    std::os::unix::fs::symlink(&l3, &lock).unwrap();
    let m0 = mtime(&outside);
    let r = open_watched(&w, &root);
    lines.push(format!("chain to a file: {r:?}; mtime/len same {}", m0 == mtime(&outside)));
    if r.is_ok() || m0 != mtime(&outside) {
        bad.push("chain file");
    }
    std::fs::rename(&lock, base.join("aside-5")).unwrap();

    // (5) lock is a directory
    std::fs::DirBuilder::new().mode(0o700).create(&lock).unwrap();
    let r = open_watched(&w, &root);
    lines.push(format!("lock is a directory: {r:?}"));
    if r.is_ok() {
        bad.push("dir");
    }
    std::fs::rename(&lock, base.join("aside-6")).unwrap();

    // (6) lock is a FIFO (mkfifo by the system tool; the open must not hang)
    let st = std::process::Command::new("/usr/bin/mkfifo")
        .arg("-m")
        .arg("600")
        .arg(&lock)
        .status()
        .unwrap();
    assert!(st.success());
    let r = open_watched(&w, &root);
    lines.push(format!("lock is a FIFO: {r:?}"));
    if r.is_ok() || r.as_ref().err().is_some_and(|e| e.contains("HANG")) {
        bad.push("fifo");
    }
    std::fs::rename(&lock, base.join("aside-7")).unwrap();

    // (7) lock is a HARD link to an outside file of the owner, 0600 (not a symbolic link)
    let hard_t = base.join("outside-hard");
    put(&hard_t, b"hard target");
    std::thread::sleep(Duration::from_millis(20));
    let m0 = mtime(&hard_t);
    std::fs::hard_link(&hard_t, &lock).unwrap();
    let r = open_watched(&w, &root);
    lines.push(format!(
        "lock is a hard link to an outside file: {r:?}; content same {}; mtime/len same {}",
        std::fs::read(&hard_t).unwrap() == b"hard target",
        m0 == mtime(&hard_t)
    ));
    if std::fs::read(&hard_t).unwrap() != b"hard target" || m0 != mtime(&hard_t) {
        bad.push("hard link changed the outside file");
    }
    std::fs::rename(&lock, base.join("aside-8")).unwrap();

    // (8) lock absent: open creates it, 0600, a regular file
    let r = open_watched(&w, &root);
    let md = std::fs::symlink_metadata(&lock).map(|m| (m.file_type().is_file(), m.mode() & 0o777));
    lines.push(format!("lock absent: {r:?}; created {md:?}"));
    if r.is_err() || md.ok() != Some((true, 0o600)) {
        bad.push("absent");
    }
    // (9) with the real (existing, unheld) lock back: opens
    std::fs::rename(&lock, base.join("aside-9")).unwrap();
    std::fs::rename(base.join("real-lock-aside"), &lock).unwrap();
    let r = open_watched(&w, &root);
    lines.push(format!("real lock back: {r:?}"));
    if r.is_err() {
        bad.push("real");
    }
    println!("QAHF N-2:\n  {}", lines.join("\n  "));
    scratch_done(&base);
    assert!(bad.is_empty(), "N-2 shapes failed: {bad:?}");
}

/// N-2, the race the builder names: a thread flips `lock` between a regular file and a dangling
/// symbolic link as fast as it can while the main thread opens the folder again and again. The
/// link's target must never be created.
#[test]
fn qahf_n2_lock_race() {
    let w = World::new(205, 3, 3);
    let (base, root) = made(&w, "qahf-n2race");
    let lock = root.join("lock");
    let target = base.join("race-target-never");
    let stop = Arc::new(AtomicBool::new(false));
    let (s2, l2, t2, b2) = (stop.clone(), lock.clone(), target.clone(), base.clone());
    let flipper = std::thread::spawn(move || {
        let mut flips = 0u64;
        let link_tmp = b2.join("link-tmp");
        let file_tmp = b2.join("file-tmp");
        while !s2.load(Ordering::Relaxed) {
            // a dangling link put in place atomically, then a regular file put back atomically
            let _ = std::fs::remove_file(&link_tmp);
            std::os::unix::fs::symlink(&t2, &link_tmp).unwrap();
            let _ = std::fs::rename(&link_tmp, &l2);
            std::fs::write(&file_tmp, b"").unwrap();
            std::fs::set_permissions(&file_tmp, std::fs::Permissions::from_mode(0o600)).unwrap();
            let _ = std::fs::rename(&file_tmp, &l2);
            flips += 1;
        }
        flips
    });
    let start = Instant::now();
    let (mut ok, mut symlink, mut other) = (0, 0, std::collections::BTreeMap::<String, usize>::new());
    let mut n = 0;
    while start.elapsed() < Duration::from_secs(20) && n < 3_000 {
        n += 1;
        match open_host(&w, 1, &root, cfg(&w), 10) {
            Ok(_) => ok += 1,
            Err(HostError::Dir(DirError::Symlink(_))) => symlink += 1,
            Err(e) => {
                let s = format!("{e:?}");
                *other.entry(s.chars().take(90).collect()).or_default() += 1;
            }
        }
        assert!(!target.exists(), "N-2 race: the link's target was created after {n} opens");
    }
    stop.store(true, Ordering::Relaxed);
    let flips = flipper.join().unwrap();
    println!(
        "QAHF N-2 race: {n} opens in {:?}, {flips} flips; opened {ok}, refused Symlink {symlink}, other {other:?}; target exists {}",
        start.elapsed(),
        target.exists()
    );
    assert!(!target.exists());
    scratch_done(&base);
}

/// Wrap `payload` the way the crate does (magic, version 1, length, SHA-256, payload): computed
/// here from the format (`src/fsio.rs:34-42`), so a VALID wrapper around a payload that is not an
/// anchor can be planted.
fn wrap_like(magic: &[u8], payload: &[u8]) -> Vec<u8> {
    let mut out = magic.to_vec();
    out.push(1);
    out.extend_from_slice(&(payload.len() as u32).to_be_bytes());
    out.extend_from_slice(&Sha256::digest(payload));
    out.extend_from_slice(payload);
    out
}

fn damages(good: &[u8], other_magic: &[u8]) -> Vec<(&'static str, Vec<u8>)> {
    let mut v = Vec::new();
    v.push(("empty", Vec::new()));
    v.push(("truncated to 40", good[..40].to_vec()));
    v.push(("truncated by one", good[..good.len() - 1].to_vec()));
    let mut x = good.to_vec();
    x.push(0);
    v.push(("one byte appended", x));
    let mut x = good.to_vec();
    x[4] = 2;
    v.push(("unknown version", x));
    let mut x = good.to_vec();
    x[8] ^= 1;
    v.push(("length field wrong", x));
    let mut x = good.to_vec();
    x[20] ^= 1;
    v.push(("digest field wrong", x));
    let mut x = good.to_vec();
    let l = x.len() - 1;
    x[l] ^= 0x80;
    v.push(("payload bit flipped", x));
    let mut x = good.to_vec();
    x[..4].copy_from_slice(&other_magic[..4]);
    v.push(("the other file's magic", x));
    v.push((
        "valid wrapper, payload not an anchor",
        wrap_like(&good[..4], b"definitely not an anchor payload"),
    ));
    v.push(("valid wrapper, empty payload", wrap_like(&good[..4], b"")));
    v.push(("zeros", vec![0u8; good.len()]));
    v
}

fn refused_as(r: &Result<(), HostError>, file: &str) -> bool {
    matches!(r, Err(HostError::Dir(DirError::Unreadable { name, .. })) if name == file)
}

/// N-4: each kind of damage to `anchors/current`, `anchors/pending` and `anchors/limits` refuses
/// the open naming that file; never taken as absent (also with the owner's unanchored setting on).
#[test]
fn qahf_n4_each_damage() {
    let w = World::new(210, 3, 3);
    let (base, root) = made(&w, "qahf-n4");
    let a = root.join("anchors");
    let (cur, pen, lim) = (a.join("current"), a.join("pending"), a.join("limits"));
    let good_cur = std::fs::read(&cur).unwrap();
    let good_lim = std::fs::read(&lim).unwrap();
    assert!(!pen.exists());
    let mut lines = Vec::new();
    let mut bad = Vec::new();
    let try_open = |unanch: bool| {
        let mut c = cfg(&w);
        c.allow_unanchored = unanch;
        open_host(&w, 1, &root, c, 10).map(|_| ())
    };
    for (file, path, good, other) in [
        ("anchors/current", &cur, &good_cur, &good_lim),
        ("anchors/pending", &pen, &good_cur, &good_lim),
        ("anchors/limits", &lim, &good_lim, &good_cur),
    ] {
        for (how, bytes) in damages(good, other) {
            for unanch in [false, true] {
                put(path, &bytes);
                let r = try_open(unanch);
                let ok = refused_as(&r, file);
                lines.push(format!(
                    "{file} {how} (unanchored {unanch}): {} {}",
                    if ok { "REFUSED Unreadable" } else { "!!" },
                    if ok { String::new() } else { format!("{r:?}") }
                ));
                if !ok {
                    bad.push(format!("{file} {how} {unanch}: {r:?}"));
                }
                // restore
                if file == "anchors/pending" {
                    std::fs::rename(path, base.join(format!("pen-aside-{}", lines.len()))).unwrap();
                } else {
                    put(path, good);
                }
            }
        }
        // a symbolic link and a directory at the file
        let aside = base.join(format!("{}-aside", file.replace('/', "-")));
        if path.exists() {
            std::fs::rename(path, &aside).unwrap();
        }
        std::os::unix::fs::symlink(&aside, path).unwrap();
        let r = try_open(true);
        lines.push(format!("{file} is a symbolic link: {r:?}"));
        if !matches!(&r, Err(HostError::Dir(DirError::Symlink(_)))) {
            bad.push(format!("{file} symlink: {r:?}"));
        }
        std::fs::remove_file(path).unwrap();
        std::fs::DirBuilder::new().mode(0o700).create(path).unwrap();
        let r = try_open(true);
        lines.push(format!("{file} is a directory: {r:?}"));
        if r.is_ok() {
            bad.push(format!("{file} dir: {r:?}"));
        }
        std::fs::rename(path, base.join(format!("{}-dir", file.replace('/', "-")))).unwrap();
        if aside.exists() {
            std::fs::rename(&aside, path).unwrap();
        }
    }
    // an anchor of ANOTHER session at current: refused (WrongSession), not absent
    let w2 = World::new(215, 3, 3);
    let (base2, root2) = made(&w2, "qahf-n4-other");
    let other_cur = std::fs::read(root2.join("anchors").join("current")).unwrap();
    put(&cur, &other_cur);
    let r = try_open(false);
    lines.push(format!("current from another session: {r:?}"));
    if r.is_ok() {
        bad.push(format!("other session: {r:?}"));
    }
    put(&cur, &good_cur);
    assert!(try_open(false).is_ok(), "restored folder does not open");
    println!("QAHF N-4:\n  {}", lines.join("\n  "));
    scratch_done(&base);
    scratch_done(&base2);
    assert!(bad.is_empty(), "N-4: {bad:#?}");
}
