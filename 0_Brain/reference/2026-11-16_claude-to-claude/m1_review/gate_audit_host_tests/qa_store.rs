//! QA-AUDIT-HOST (independent check): the store and the host folder against the REAL filesystem.
//! Every probe prints `QA <name>: <result>` so the run log carries the evidence.
//! Written by the checker; not part of the build under review.
#![cfg(unix)]

mod common;

use std::os::unix::fs::{symlink, PermissionsExt};
use std::path::Path;
use std::sync::mpsc;
use std::time::Duration;

use coagent_audit::budget::Table;
use coagent_audit::store::{Part, Store, StoreKey};
use coagent_audit_host::{
    AuditDir, AuditHost, DirError, HostError, MAX_LEFTOVER_TEMPS, MAX_RECORD_BYTES_PER_SESSION,
};
use coagent_proto::bytes::{KeyId, SessionId};
use common::*;

fn key(part: Part, n: u64) -> StoreKey {
    StoreKey {
        part,
        author: KeyId([0x11; 32]),
        n,
    }
}

fn chmod(p: &Path, m: u32) {
    std::fs::set_permissions(p, std::fs::Permissions::from_mode(m)).unwrap();
}

fn mkfifo(p: &Path) {
    let st = std::process::Command::new("mkfifo").arg(p).status().unwrap();
    assert!(st.success(), "mkfifo");
    chmod(p, 0o600);
}

/// Run `f` on another thread; a hang past 10 s is a FAILURE of the probe (an open that blocks).
fn no_hang<T: Send + 'static>(what: &str, f: impl FnOnce() -> T + Send + 'static) -> T {
    let (tx, rx) = mpsc::channel();
    std::thread::spawn(move || {
        let _ = tx.send(f());
    });
    match rx.recv_timeout(Duration::from_secs(10)) {
        Ok(v) => v,
        Err(_) => panic!("QA {what}: HANG (the open blocked for 10 s)"),
    }
}

/// A store with one record, re-opened by a fresh `AuditDir`.
fn store_with_one(name: &str) -> (std::path::PathBuf, std::path::PathBuf, String) {
    let base = scratch(name);
    let p = base.join("store");
    let mut d = AuditDir::open(&p).unwrap();
    let s = SessionId([3; 32]);
    d.put(&s, &key(Part::OwnEvent(None), 1), b"hello").unwrap();
    let rec = std::fs::read_dir(&p)
        .unwrap()
        .map(|e| e.unwrap().file_name().into_string().unwrap())
        .find(|n| !n.starts_with('.'))
        .unwrap();
    (base, p, rec)
}

#[test]
fn qa_s1_round_trip_put_remove_fresh_open() {
    let base = scratch("qa-s1");
    let p = base.join("store");
    let s = SessionId([3; 32]);
    let mut d = AuditDir::open(&p).unwrap();
    for n in 1..=5u64 {
        d.put(&s, &key(Part::OwnEvent(None), n), format!("r{n}").as_bytes())
            .unwrap();
    }
    d.put(&s, &key(Part::Fixed(Table::Roster), 1), b"ro").unwrap();
    d.put(&s, &key(Part::Fixed(Table::Roster), 1), b"ro2").unwrap(); // replace
    d.remove(&s, &key(Part::OwnEvent(None), 3)).unwrap();
    d.remove(&s, &key(Part::OwnEvent(None), 99)).unwrap(); // absent: nothing
    let before = d.list(&s).unwrap();
    drop(d);
    let d2 = AuditDir::open(&p).unwrap();
    let after = d2.list(&s).unwrap();
    assert_eq!(before, after);
    assert_eq!(after.len(), 5);
    // modes on disk: directory 0700, every file 0600
    let dm = std::fs::metadata(&p).unwrap().permissions().mode() & 0o777;
    let mut fm = Vec::new();
    for e in std::fs::read_dir(&p).unwrap() {
        fm.push(e.unwrap().metadata().unwrap().permissions().mode() & 0o777);
    }
    assert_eq!(dm, 0o700);
    assert!(fm.iter().all(|m| *m == 0o600), "{fm:?}");
    println!(
        "QA s1 round trip: 5 records equal after a fresh open; dir {dm:o}, files {:?}",
        fm.iter().map(|m| format!("{m:o}")).collect::<Vec<_>>()
    );
    scratch_done(&base);
}

#[test]
fn qa_s2_rights_refused() {
    let mut lines = Vec::new();
    for m in [0o710, 0o750, 0o701, 0o705, 0o770, 0o777] {
        let (base, p, _) = store_with_one("qa-s2d");
        chmod(&p, m);
        let r = AuditDir::open(&p);
        assert!(
            matches!(r, Err(DirError::Rights { .. })),
            "dir {m:o}: {r:?}"
        );
        lines.push(format!("dir {m:o} -> {:?}", r.err().unwrap()));
        chmod(&p, 0o700);
        scratch_done(&base);
    }
    for m in [0o640, 0o604, 0o660, 0o644, 0o606, 0o610, 0o601] {
        let (base, p, rec) = store_with_one("qa-s2f");
        chmod(&p.join(&rec), m);
        let r = AuditDir::open(&p);
        assert!(
            matches!(r, Err(DirError::Rights { .. })),
            "file {m:o}: {r:?}"
        );
        lines.push(format!("file {m:o} -> refused Rights"));
        scratch_done(&base);
    }
    // a leftover temporary file with group rights is ALSO refused (every entry is checked)
    let (base, p, _) = store_with_one("qa-s2t");
    let tmp = p.join(format!(".tmp.{}", "a".repeat(32)));
    std::fs::write(&tmp, b"x").unwrap();
    chmod(&tmp, 0o640);
    let r = AuditDir::open(&p);
    assert!(matches!(r, Err(DirError::Rights { .. })), "{r:?}");
    lines.push("temp 640 -> refused Rights".into());
    scratch_done(&base);
    println!("QA s2 rights: {}", lines.join("; "));
}

#[test]
fn qa_s3_symlinks_refused() {
    // symlinked store directory
    let (base, p, _) = store_with_one("qa-s3d");
    let link = base.join("store-link");
    symlink(&p, &link).unwrap();
    let r = AuditDir::open(&link);
    assert!(matches!(r, Err(DirError::Symlink(_))), "{r:?}");
    let a = format!("{:?}", r.err().unwrap());
    // symlinked record file (to a valid record elsewhere)
    let (base2, p2, rec2) = store_with_one("qa-s3f");
    let real = base2.join("elsewhere");
    std::fs::rename(p2.join(&rec2), &real).unwrap();
    symlink(&real, p2.join(&rec2)).unwrap();
    let r2 = AuditDir::open(&p2);
    assert!(matches!(r2, Err(DirError::Symlink(_))), "{r2:?}");
    // symlinked temp-named entry
    let (base3, p3, _) = store_with_one("qa-s3t");
    symlink("/dev/null", p3.join(format!(".tmp.{}", "b".repeat(32)))).unwrap();
    let r3 = AuditDir::open(&p3);
    assert!(matches!(r3, Err(DirError::Symlink(_))), "{r3:?}");
    println!(
        "QA s3 symlinks: dir -> {a}; record file -> {:?}; temp-named link -> {:?}",
        r2.err().unwrap(),
        r3.err().unwrap()
    );
    for b in [base, base2, base3] {
        scratch_done(&b);
    }
}

#[test]
fn qa_s4_fifo_where_a_record_should_be_refused_without_hanging() {
    let (base, p, rec) = store_with_one("qa-s4");
    std::fs::remove_file(p.join(&rec)).unwrap();
    mkfifo(&p.join(&rec));
    let p2 = p.clone();
    let r = no_hang("s4 fifo record", move || AuditDir::open(&p2).map(|_| ()));
    assert!(matches!(r, Err(DirError::UnknownFile(_))), "{r:?}");
    // a FIFO with a temporary file's name
    let (base2, p3, _) = store_with_one("qa-s4t");
    mkfifo(&p3.join(format!(".tmp.{}", "c".repeat(32))));
    let p4 = p3.clone();
    let r2 = no_hang("s4 fifo temp", move || AuditDir::open(&p4).map(|_| ()));
    assert!(r2.is_err(), "a FIFO with a temp name was accepted: {r2:?}");
    println!("QA s4 fifo: record name -> {r:?}; temp name -> {r2:?}; no hang");
    scratch_done(&base);
    scratch_done(&base2);
}

#[test]
fn qa_s5_unknown_names_refused() {
    let mut out = Vec::new();
    for bad in [
        "README",
        ".DS_Store",
        ".tmp.short",
        &format!(".tmp.{}", "A".repeat(32)),
        &format!(".tmp.{}x", "a".repeat(32)),
        "x.y.z.w",
    ] {
        let (base, p, _) = store_with_one("qa-s5");
        std::fs::write(p.join(bad), b"x").unwrap();
        chmod(&p.join(bad), 0o600);
        let r = AuditDir::open(&p);
        assert!(matches!(r, Err(DirError::UnknownFile(_))), "{bad}: {r:?}");
        out.push(bad.to_string());
        scratch_done(&base);
    }
    // a record name whose content is not wrapped: refused Unreadable (not read as a record)
    let (base, p, rec) = store_with_one("qa-s5u");
    std::fs::write(p.join(&rec), b"not a wrapped record").unwrap();
    let r = AuditDir::open(&p);
    assert!(matches!(r, Err(DirError::Unreadable { .. })), "{r:?}");
    // a subdirectory
    let (base2, p2, _) = store_with_one("qa-s5d");
    std::fs::create_dir(p2.join("sub")).unwrap();
    chmod(&p2.join("sub"), 0o700);
    let r2 = AuditDir::open(&p2);
    assert!(matches!(r2, Err(DirError::UnknownFile(_))), "{r2:?}");
    println!(
        "QA s5 unknown: {} names refused UnknownFile ({}); unwrapped record -> {:?}; subdir -> {:?}",
        out.len(),
        out.join(", "),
        r.err().unwrap(),
        r2.err().unwrap()
    );
    scratch_done(&base);
    scratch_done(&base2);
}

#[test]
fn qa_s6_leftover_temps_never_read_never_deleted_bound_64() {
    let (base, p, _) = store_with_one("qa-s6");
    let mut names = Vec::new();
    for i in 0..MAX_LEFTOVER_TEMPS {
        let n = format!(".tmp.{:032x}", i + 1);
        // content that is NOT a record: if it were read as one, the open would refuse
        std::fs::write(p.join(&n), b"garbage, not a wrapped record").unwrap();
        chmod(&p.join(&n), 0o600);
        names.push(n);
    }
    let d = AuditDir::open(&p).expect("64 leftovers must open");
    let st = d.status();
    assert_eq!(st.leftover_temps, 64);
    assert_eq!(st.records, 1);
    drop(d);
    for n in &names {
        assert_eq!(
            std::fs::read(p.join(n)).unwrap(),
            b"garbage, not a wrapped record",
            "{n} changed or deleted"
        );
    }
    // a put / remove does not touch them either
    let mut d = AuditDir::open(&p).unwrap();
    let s = SessionId([3; 32]);
    d.put(&s, &key(Part::OwnEvent(None), 2), b"x").unwrap();
    d.remove(&s, &key(Part::OwnEvent(None), 2)).unwrap();
    drop(d);
    let still = names.iter().filter(|n| p.join(n).exists()).count();
    assert_eq!(still, 64);
    // the 65th
    let n = format!(".tmp.{:032x}", 999);
    std::fs::write(p.join(&n), b"g").unwrap();
    chmod(&p.join(&n), 0o600);
    let r = AuditDir::open(&p);
    assert!(matches!(r, Err(DirError::TooManyLeftovers(65))), "{r:?}");
    println!(
        "QA s6 leftovers: 64 open (counted {}), content untouched after open/put/remove ({still} kept); 65 -> {:?}",
        st.leftover_temps,
        r.err().unwrap()
    );
    scratch_done(&base);
}

/// DQ-H3: the Segment and anchor slots may be put past the session's bound; does the OPEN then
/// accept what the puts accepted?
#[test]
fn qa_s7_exempt_put_past_the_bound_then_open() {
    let base = scratch("qa-s7");
    let p = base.join("store");
    let s = SessionId([3; 32]);
    let mut d = AuditDir::open(&p).unwrap();
    // fill the byte bound with ordinary records of the record cap
    let big = vec![7u8; coagent_audit::bundle::MAX_RECORD_BYTES];
    let mut n = 0u64;
    loop {
        n += 1;
        match d.put(&s, &key(Part::PeerEvent(2), n), &big) {
            Ok(()) => {}
            Err(_) => break,
        }
    }
    let st = d.status();
    // top up with small records to sit exactly at (or just under) the bound
    let mut m = 0u64;
    loop {
        m += 1;
        if d.put(&s, &key(Part::PeerEvent(3), m), &[1u8; 1]).is_err() {
            break;
        }
        if m > 100_000 {
            break;
        }
    }
    let at = d.status();
    // an ordinary put is refused now; a Segment put (what a seal's commit writes) is accepted
    let ord = d.put(&s, &key(Part::OwnEvent(None), 1), b"x");
    let seg = d.put(&s, &key(Part::Fixed(Table::Segment), 0), &vec![9u8; 14_065]);
    let over = d.status();
    drop(d);
    let r = AuditDir::open(&p);
    println!(
        "QA s7 bound: after {} cap-size records bytes={} (bound {}); topped up to bytes={} records={}; \
         ordinary put -> {:?}; Segment put -> {:?}; now bytes={} (over by {}); RE-OPEN -> {:?}",
        n - 1,
        st.bytes,
        MAX_RECORD_BYTES_PER_SESSION,
        at.bytes,
        at.records,
        ord,
        seg,
        over.bytes,
        over.bytes as i64 - MAX_RECORD_BYTES_PER_SESSION as i64,
        r.as_ref().map(|_| "ok").map_err(|e| format!("{e:?}"))
    );
    assert!(ord.is_err());
    assert!(seg.is_ok());
    // RECORD what happens; the verdict rules on it (no assertion on the open's answer here)
    scratch_done(&base);
}

/// The host folder: FIFOs, symlinks, rights and unknown entries in root, anchors and archive.
#[test]
fn qa_s8_host_folder_fail_closed() {
    let w = World::new(60, 3, 3);
    let mut out = Vec::new();
    let fresh = |tag: &str| -> std::path::PathBuf {
        let base = scratch(tag);
        let root = base.join("host");
        let mut h = create_host(&w, 1, &root, cfg(&w));
        host_record(&mut h, &w.ids[1], coagent_audit_host::Causer::LocalHuman, 1);
        h.seal(
            &w.ids[1],
            coagent_audit_host::SealTrigger::OwnerCommand,
            t(2),
        )
        .ok();
        drop(h);
        root
    };
    type Mut = fn(&Path);
    let cases: Vec<(&str, Mut)> = vec![
        ("anchors/current FIFO", |r| {
            let p = r.join("anchors/current");
            std::fs::remove_file(&p).unwrap();
            mkfifo(&p);
        }),
        ("anchors/pending FIFO", |r| mkfifo(&r.join("anchors/pending"))),
        ("anchors/limits FIFO", |r| {
            let p = r.join("anchors/limits");
            std::fs::remove_file(&p).unwrap();
            mkfifo(&p);
        }),
        ("lock FIFO", |r| {
            let p = r.join("lock");
            std::fs::remove_file(&p).unwrap();
            mkfifo(&p);
        }),
        ("archive file FIFO", |r| {
            mkfifo(&r.join(format!("archive/seg-{:020}-{:04}.bundle", 7, 0)))
        }),
        ("anchors/current symlink", |r| {
            let p = r.join("anchors/current");
            let q = r.join("current.real");
            std::fs::rename(&p, &q).unwrap();
            symlink(&q, &p).unwrap();
        }),
        ("lock symlink", |r| {
            let p = r.join("lock");
            std::fs::remove_file(&p).unwrap();
            symlink(r.join("../lock-target"), &p).unwrap();
        }),
        ("anchors dir symlink", |r| {
            let p = r.join("anchors");
            let q = r.join("../anchors.real");
            std::fs::rename(&p, &q).unwrap();
            symlink(&q, &p).unwrap();
        }),
        ("root 0750", |r| chmod(r, 0o750)),
        ("anchors 0711", |r| chmod(&r.join("anchors"), 0o711)),
        ("archive 0755", |r| chmod(&r.join("archive"), 0o755)),
        ("anchors/current 0640", |r| {
            chmod(&r.join("anchors/current"), 0o640)
        }),
        ("lock 0644", |r| chmod(&r.join("lock"), 0o644)),
        ("archive file 0604", |r| {
            let f = std::fs::read_dir(r.join("archive"))
                .unwrap()
                .next()
                .unwrap()
                .unwrap()
                .path();
            chmod(&f, 0o604)
        }),
        ("unknown file in root", |r| {
            std::fs::write(r.join("notes.txt"), b"x").unwrap();
            chmod(&r.join("notes.txt"), 0o600);
        }),
        ("unknown file in anchors", |r| {
            std::fs::write(r.join("anchors/old"), b"x").unwrap();
            chmod(&r.join("anchors/old"), 0o600);
        }),
        ("unknown file in archive", |r| {
            std::fs::write(r.join("archive/seg-1.bundle"), b"x").unwrap();
            chmod(&r.join("archive/seg-1.bundle"), 0o600);
        }),
        ("anchors/current garbage", |r| {
            std::fs::write(r.join("anchors/current"), b"garbage").unwrap();
        }),
        ("anchors/limits garbage", |r| {
            std::fs::write(r.join("anchors/limits"), b"garbage").unwrap();
        }),
    ];
    for (name, f) in cases {
        let root = fresh("qa-s8");
        f(&root);
        let r2 = root.clone();
        let w2 = World::new(60, 3, 3);
        let res = no_hang(name, move || {
            open_host(&w2, 1, &r2, cfg(&w2), 10)
                .map(|_| ())
                .map_err(|e| format!("{e:?}"))
        });
        assert!(res.is_err(), "QA s8 {name}: the open ACCEPTED the folder");
        out.push(format!("{name} -> {}", res.err().unwrap()));
        // leave modes such that cleanup works
        let _ = std::fs::set_permissions(&root, std::fs::Permissions::from_mode(0o700));
        scratch_done(root.parent().unwrap());
    }
    // the lock symlink case must not have created a file outside the root
    println!("QA s8 host folder (each refused, none hung):\n  {}", out.join("\n  "));
}

/// A stale lock file (left by a dead process) does not block the open; a live one does.
#[test]
fn qa_s9_lock_file_states() {
    let w = World::new(61, 3, 3);
    let base = scratch("qa-s9");
    let root = base.join("host");
    let h = create_host(&w, 1, &root, cfg(&w));
    drop(h);
    // (i) lock file absent (a stop before its creation, or its entry not synced)
    std::fs::remove_file(root.join("lock")).unwrap();
    let a = open_host(&w, 1, &root, cfg(&w), 5).map(|(h, r)| (r.opened, h));
    let a_ok = a.is_ok();
    drop(a);
    // (ii) lock file present and empty, not held (a stop right after its creation)
    let b = open_host(&w, 1, &root, cfg(&w), 6);
    let b_ok = b.is_ok();
    // (iii) held by a live host: refused InUse
    let c = open_host(&w, 1, &root, cfg(&w), 7);
    let c_in_use = matches!(c, Err(HostError::Dir(DirError::InUse)));
    drop(b);
    // (iv) after the holder is gone: opens
    let d = open_host(&w, 1, &root, cfg(&w), 8).is_ok();
    println!(
        "QA s9 lock: absent -> open {a_ok}; present unheld -> open {b_ok}; held -> InUse {c_in_use}; released -> open {d}"
    );
    assert!(a_ok && b_ok && c_in_use && d);
    scratch_done(&base);
}

#[allow(dead_code)]
fn unused(_: AuditHost) {}
