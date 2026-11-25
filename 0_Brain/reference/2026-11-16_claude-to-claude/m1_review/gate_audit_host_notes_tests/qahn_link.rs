//! QA-AUDIT-HOST-NOTES (independent check of branch `audit-host-notes`), item 5: the hard-link
//! refusal attacked. Head 52ad858 only (uses `DirError::HardLink`); uncommitted, checker's tree only.
//! Nothing here deletes: names are moved aside into the test's own scratch.
#![cfg(unix)]

mod common;

use std::os::unix::fs::{MetadataExt, PermissionsExt};
use std::path::{Path, PathBuf};
use std::sync::atomic::{AtomicBool, AtomicUsize, Ordering};
use std::sync::Arc;
use std::time::{Duration, Instant};

use coagent_audit_host::{AuditHost, Causer, DirError, HostError, Input, Outcome, SealTrigger};
use common::*;

type Seen = Option<(Vec<u8>, u64, i64, i64, i64, i64, u64, u64)>;
fn seen(p: &Path) -> Seen {
    let md = std::fs::symlink_metadata(p).ok()?;
    let bytes = if md.is_file() { std::fs::read(p).ok()? } else { Vec::new() };
    Some((bytes, md.len(), md.mtime(), md.mtime_nsec(), md.ctime(), md.ctime_nsec(), md.ino(), md.nlink()))
}

fn move_aside(base: &Path, p: &Path) {
    let d = base.join("moved");
    std::fs::create_dir_all(&d).unwrap();
    static N: AtomicUsize = AtomicUsize::new(0);
    let n = N.fetch_add(1, Ordering::SeqCst);
    std::fs::rename(p, d.join(format!("{n}"))).unwrap();
}

fn outside_copy(base: &Path, src: &Path, tag: &str) -> PathBuf {
    let o = base.join(format!("outside-{tag}"));
    std::fs::write(&o, std::fs::read(src).unwrap_or_default()).unwrap();
    std::fs::set_permissions(&o, std::fs::Permissions::from_mode(0o600)).unwrap();
    o
}

fn relink(base: &Path, outside: &Path, inside: &Path) {
    if std::fs::symlink_metadata(inside).is_ok() {
        move_aside(base, inside);
    }
    std::fs::hard_link(outside, inside).unwrap();
}

/// V=1, members 0..3: three own records and peer 3's three events received; peer 3 removed (so a
/// release can run); the host returned open.
fn host4(b: u8, name: &str) -> (World, PathBuf, PathBuf) {
    let mut w = World::new(b, 4, 4);
    let base = scratch(name);
    let root = base.join("host");
    let mut h = create_host(&w, 1, &root, cfg(&w));
    let mut p3 = mem_member(&w, 3);
    for n in 0..3u64 {
        host_record(&mut h, &w.ids[1], Causer::LocalHuman, n + 1);
        let s = p3.record(&w.ids[3], bare("p"), t(n + 1)).unwrap();
        let e = p3.outgoing(s).into_iter().find(|(to, _)| *to == w.key(1)).unwrap().1;
        h.apply(&w.ids[1], Input::Receive(e), t(n + 1)).unwrap();
    }
    let r = w.remove(3);
    h.apply(&w.ids[1], Input::Roster(r), t(10)).unwrap();
    drop(h);
    (w, base, root)
}

const NAMES: [(&str, &str); 4] = [
    ("lock", "root/lock"),
    ("anchors/current", "anchors/current"),
    ("anchors/pending", "anchors/pending"),
    ("anchors/limits", "anchors/limits"),
];

fn hl(e: &str) -> Result<(), HostError> {
    Err(HostError::Dir(DirError::HardLink(e.into())))
}

/// Each name hard-linked to an outside 0600 file: refused naming it, the outside file untouched
/// (bytes, length, mtime, ctime, inode, links); a SECOND open after the refusal: the same; the
/// folder's own files untouched by the refused opens; the extra link moved away: opens.
#[test]
fn qahn_na_each_name_outside_link() {
    let mut bad = Vec::new();
    for (i, (name, expect)) in NAMES.into_iter().enumerate() {
        let (w, base, root) = host4(60 + i as u8, &format!("qahn-na-{i}"));
        let src = if name == "anchors/pending" { root.join("anchors/current") } else { root.join(name) };
        let o = outside_copy(&base, &src, &format!("{i}"));
        relink(&base, &o, &root.join(name));
        let o0 = seen(&o);
        let in0: Vec<Seen> = ["lock", "anchors/current", "anchors/limits", "anchors/pending"].iter().map(|n| seen(&root.join(n))).collect();
        let r1 = open_host(&w, 1, &root, cfg(&w), 20).map(|_| ());
        let o1 = seen(&o);
        let r2 = open_host(&w, 1, &root, cfg(&w), 21).map(|_| ());
        let o2 = seen(&o);
        let in2: Vec<Seen> = ["lock", "anchors/current", "anchors/limits", "anchors/pending"].iter().map(|n| seen(&root.join(n))).collect();
        // the extra name moved out of the folder: one link again (the outside name keeps the inode)
        let inside = root.join(name);
        let tmp = base.join(format!("taken-{i}"));
        std::fs::copy(&inside, &tmp).unwrap();
        move_aside(&base, &inside);
        std::fs::rename(&tmp, &inside).unwrap();
        std::fs::set_permissions(&inside, std::fs::Permissions::from_mode(0o600)).unwrap();
        // my own move changed the outside inode's ctime and links: compare the accepted open from here
        let o0b = seen(&o);
        let r3 = open_host(&w, 1, &root, cfg(&w), 22).map(|(h, _)| h.status().map(|s| (s.segment, s.own_seq)));
        let o3 = seen(&o);
        println!(
            "QAHN NA [{name}]: open {r1:?}; again {r2:?}; outside unchanged {} {}; folder's files unchanged by the refused opens {}; link removed -> {r3:?}; outside unchanged after the accepted open {}",
            o0 == o1, o0 == o2, in0 == in2, o0b == o3
        );
        if r1 != hl(expect) || r2 != hl(expect) || o0 != o1 || o0 != o2 || in0 != in2 || r3.is_err() || o0b != o3 {
            bad.push(name);
        }
    }
    assert!(bad.is_empty(), "{bad:?}");
}

/// A second link made from the OTHER side (`ln root/lock outside/x`, the folder's inode with an
/// outside name) and a second link between two names INSIDE the folder.
#[test]
fn qahn_na_other_side_and_inside() {
    let mut lines = Vec::new();
    // (a) the folder's own inode gets an outside name
    for (i, (name, expect)) in NAMES.into_iter().enumerate() {
        if name == "anchors/pending" {
            continue;
        }
        let (w, base, root) = host4(70 + i as u8, &format!("qahn-os-{i}"));
        let o = base.join(format!("outside-name-{i}"));
        std::fs::hard_link(root.join(name), &o).unwrap();
        let o0 = seen(&o);
        let r = open_host(&w, 1, &root, cfg(&w), 20).map(|_| ());
        let ok = r == hl(expect) && seen(&o) == o0;
        lines.push(format!("outside name for {name}: {r:?}, outside unchanged {} -> {}", seen(&o) == o0, if ok { "OK" } else { "BAD" }));
    }
    // (b) two names inside: current and pending one inode; limits and pending one inode; lock and a
    // valid archive name one inode
    let (w, base, root) = host4(80, "qahn-in-a");
    std::fs::hard_link(root.join("anchors/current"), root.join("anchors/pending")).unwrap();
    let r = open_host(&w, 1, &root, cfg(&w), 20).map(|_| ());
    lines.push(format!("current = pending (one inode): {r:?} -> {}", if r == hl("anchors/current") { "OK" } else { "BAD" }));
    let _ = base;
    let (w, _base, root) = host4(81, "qahn-in-b");
    std::fs::hard_link(root.join("anchors/limits"), root.join("anchors/pending")).unwrap();
    let r = open_host(&w, 1, &root, cfg(&w), 20).map(|_| ());
    lines.push(format!("limits = pending (one inode): {r:?} -> {}", if r == hl("anchors/limits") { "OK" } else { "BAD" }));
    let (w, _base, root) = host4(82, "qahn-in-c");
    std::fs::hard_link(root.join("lock"), root.join("archive/seg-00000000000000000009-0000.bundle")).unwrap();
    let r = open_host(&w, 1, &root, cfg(&w), 20).map(|_| ());
    lines.push(format!("lock = an archive name (one inode): {r:?} -> {}", if r == hl("root/lock") { "OK" } else { "BAD" }));
    for l in &lines {
        println!("QAHN NA2 {l}");
    }
    assert!(lines.iter().all(|l| l.ends_with("OK")), "{lines:#?}");
}

/// The race: a thread keeps putting a hard link to an outside 0600 file at `lock` (by rename, so
/// the name flips between absent / the open's own fresh lock / the outside inode) while the main
/// thread opens again and again. Every answer is `Ok`, `HardLink("root/lock")` (among them the
/// window between `create_new` and the entry check) or an `Io` on the lock; the outside file is
/// compared after EVERY open.
#[test]
fn qahn_na_lock_race() {
    let (w, base, root) = host4(90, "qahn-race");
    let o = outside_copy(&base, &root.join("lock"), "race");
    let side = base.join("side");
    std::fs::create_dir_all(&side).unwrap();
    let o0 = seen(&o);
    let stop = Arc::new(AtomicBool::new(false));
    let swaps = Arc::new(AtomicUsize::new(0));
    let (s2, sw2, root2, side2, o2) = (stop.clone(), swaps.clone(), root.clone(), side.clone(), o.clone());
    let th = std::thread::spawn(move || {
        let mut n = 0u64;
        while !s2.load(Ordering::SeqCst) {
            n += 1;
            let tmp = side2.join(format!("l{n}"));
            let _ = std::fs::hard_link(&o2, &tmp);
            // flip: the outside inode at `lock`
            let _ = std::fs::rename(&tmp, root2.join("lock"));
            std::thread::yield_now();
            // flip: `lock` moved out (absent; the next open creates its own)
            let _ = std::fs::rename(root2.join("lock"), side2.join(format!("m{n}")));
            std::thread::yield_now();
            sw2.fetch_add(1, Ordering::SeqCst);
        }
    });
    let t0 = Instant::now();
    let mut tally = std::collections::BTreeMap::<String, usize>::new();
    let mut changed = 0;
    let mut opens = 0;
    while t0.elapsed() < Duration::from_secs(20) {
        let r = open_host(&w, 1, &root, cfg(&w), 30);
        opens += 1;
        let k = match &r {
            Ok(_) => "Ok".to_string(),
            Err(e) => {
                let s = format!("{e:?}");
                s.split(" kind").next().unwrap_or(&s).to_string()
            }
        };
        // an accepted open: is its lock held on the OUTSIDE inode (the name swapped away between
        // the lock's open and the entry check, so no entry check could see it)?
        let k = if r.is_ok() {
            match std::fs::File::open(&o).map(|f| f.try_lock()) {
                Ok(Err(std::fs::TryLockError::WouldBlock)) => "Ok, its lock held on the OUTSIDE inode".to_string(),
                _ => k,
            }
        } else {
            k
        };
        drop(r);
        *tally.entry(k).or_default() += 1;
        if seen(&o) != o0 {
            // the outside inode's link count changes with the thread's own links; compare content,
            // length and mtime only
            let a = seen(&o).unwrap();
            let b = o0.clone().unwrap();
            if (a.0.clone(), a.1, a.2, a.3) != (b.0.clone(), b.1, b.2, b.3) {
                changed += 1;
            }
        }
    }
    stop.store(true, Ordering::SeqCst);
    th.join().unwrap();
    println!(
        "QAHN RACE: {opens} opens in 20 s, {} swaps; answers {tally:?}; outside content/length/mtime changed after {changed} opens",
        swaps.load(Ordering::SeqCst)
    );
    assert_eq!(changed, 0);
    assert!(tally.keys().all(|k| k.starts_with("Ok") || k.contains("HardLink(\"root/lock\")") || k.contains("lock") || k.contains("InUse")), "{tally:?}");
}

/// Friday's answer (5), attacked: each name linked to an outside file, then EVERY operation that
/// writes that name, the outside file compared after each. Two routes: (i) the link planted AFTER a
/// good open (a running host: the open's check cannot see it), any build; (ii) the link planted
/// BEFORE the open, which only the red variant `hard_link_accepted` accepts (run this test under
/// that red to attack the "nothing outside touched" half on its own).
#[test]
fn qahn_na_every_write_after_a_link() {
    let mut bad = Vec::new();
    for route in ["after-open", "before-open"] {
        for (i, (name, _)) in NAMES.into_iter().enumerate() {
            let (w, base, root) = host4(100 + i as u8 + if route == "after-open" { 0 } else { 10 }, &format!("qahn-ew-{route}-{i}"));
            let src = if name == "anchors/pending" { root.join("anchors/current") } else { root.join(name) };
            let o = outside_copy(&base, &src, &format!("{route}-{i}"));
            let mut h: AuditHost;
            if route == "after-open" {
                h = open_host(&w, 1, &root, cfg(&w), 20).unwrap().0;
                relink(&base, &o, &root.join(name));
            } else {
                relink(&base, &o, &root.join(name));
                match open_host(&w, 1, &root, cfg(&w), 20) {
                    Ok((h2, _)) => h = h2,
                    Err(e) => {
                        println!("QAHN EW [{route} {name}]: open refused {e:?} (green build): no write reached");
                        continue;
                    }
                }
            }
            let o0 = seen(&o).map(|x| (x.0, x.1, x.2, x.3));
            let mut steps = Vec::new();
            let mut check = |what: &str, ans: String, steps: &mut Vec<String>| {
                let now = seen(&o).map(|x| (x.0, x.1, x.2, x.3));
                steps.push(format!("{what} {ans} outside-same {}", now == o0));
                if now != o0 {
                    bad.push(format!("{route} {name} after {what}"));
                }
            };
            let a = h.apply(&w.ids[1], Input::Record { causer: Causer::LocalHuman, input: owned("qahn.ew", Some("x"), None) }, t(30));
            check("record", format!("{:?}", a.as_ref().map(|o| matches!(o, Outcome::Recorded(_)))), &mut steps);
            let a = h.apply(&w.ids[1], Input::Checkpoint, t(31));
            check("checkpoint", format!("{:?}", a.is_ok()), &mut steps);
            let lim = h.member().unwrap().limits();
            let a = h.set_limits(coagent_audit::session::StoreLimits { bytes: lim.bytes / 2, records: lim.records / 2 });
            check("set_limits", format!("{:?}", a.is_ok()), &mut steps);
            let a = h.apply(&w.ids[1], Input::Release(w.key(3)), t(32));
            check("release", format!("{:?}", a.as_ref().map(|o| matches!(o, Outcome::Released(_)))), &mut steps);
            let a = h.seal_begin(&w.ids[1], SealTrigger::OwnerCommand, t(33));
            check("seal_begin (pending written)", format!("{:?}", a.is_ok()), &mut steps);
            let a = h.seal_finish(&w.ids[1], t(34));
            check("seal_finish", format!("{:?}", a.as_ref().map(|r| r.info.segment)), &mut steps);
            let a = h.apply(&w.ids[1], Input::Record { causer: Causer::LocalHuman, input: owned("qahn.ew", Some("y"), None) }, t(35));
            check("record", format!("{:?}", a.is_ok()), &mut steps);
            drop(h);
            let r = open_host(&w, 1, &root, cfg(&w), 40).map(|(h, _)| h.status().map(|s| (s.segment, s.own_seq)));
            check("re-open", format!("{r:?}"), &mut steps);
            println!("QAHN EW [{route} {name}]: {}", steps.join("; "));
        }
    }
    assert!(bad.is_empty(), "{bad:?}");
}
