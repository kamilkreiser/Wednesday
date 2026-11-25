//! QA-AUDIT-HOST-NOTES (independent check of branch `audit-host-notes`), item 5: the same folders
//! opened at 9145840 and at 52ad858 (this file compiles at both; uncommitted, checker's trees only).
//! Each case prints `QAHN SAME <case> | <open answer> | outside <unchanged?> | folder <unchanged?>`;
//! the two trees' lines are compared by program. Single-fault and one-link folders must answer the
//! same; multi-fault folders show which error wins.
#![cfg(unix)]

mod common;

use std::os::unix::fs::{MetadataExt, PermissionsExt};
use std::path::{Path, PathBuf};

use coagent_audit_host::{Causer, SealTrigger, TEMP_PREFIX};
use common::*;

/// What an observer can see of a file: bytes, length, mtime, ctime, inode, link count.
fn seen(p: &Path) -> Option<(Vec<u8>, u64, i64, i64, i64, i64, u64, u64)> {
    let md = std::fs::symlink_metadata(p).ok()?;
    let bytes = if md.is_file() { std::fs::read(p).ok()? } else { Vec::new() };
    Some((bytes, md.len(), md.mtime(), md.mtime_nsec(), md.ctime(), md.ctime_nsec(), md.ino(), md.nlink()))
}

/// Every path under `root` with what `seen` sees.
fn tree(root: &Path) -> Vec<(PathBuf, String)> {
    let mut out = Vec::new();
    let mut stack = vec![root.to_path_buf()];
    while let Some(d) = stack.pop() {
        let Ok(rd) = std::fs::read_dir(&d) else { continue };
        for e in rd {
            let p = e.unwrap().path();
            let md = std::fs::symlink_metadata(&p).unwrap();
            if md.is_dir() {
                stack.push(p.clone());
            }
            out.push((p.clone(), format!("{:?}", seen(&p))));
        }
    }
    out.sort();
    out
}

/// A folder: V=1, three own records, a seal (one archive bundle), one more record.
fn folder(b: u8, name: &str) -> (World, PathBuf, PathBuf) {
    let w = World::new(b, 3, 3);
    let base = scratch(name);
    let root = base.join("host");
    let mut h = create_host(&w, 1, &root, cfg(&w));
    for n in 0..3 {
        host_record(&mut h, &w.ids[1], Causer::LocalHuman, n + 1);
    }
    h.seal(&w.ids[1], SealTrigger::OwnerCommand, t(4)).expect("seal");
    host_record(&mut h, &w.ids[1], Causer::LocalHuman, 5);
    drop(h);
    (w, base, root)
}

fn outside_copy(base: &Path, src: &Path, tag: &str, mode: u32) -> PathBuf {
    let o = base.join(format!("outside-{tag}"));
    std::fs::write(&o, std::fs::read(src).unwrap_or_default()).unwrap();
    std::fs::set_permissions(&o, std::fs::Permissions::from_mode(mode)).unwrap();
    o
}

/// Move a name aside (no delete): into `<base>/moved/<n>`.
fn move_aside(base: &Path, p: &Path) {
    let d = base.join("moved");
    std::fs::create_dir_all(&d).unwrap();
    let n = std::fs::read_dir(&d).unwrap().count();
    std::fs::rename(p, d.join(format!("{n}"))).unwrap();
}

fn relink(base: &Path, outside: &Path, inside: &Path) {
    if std::fs::symlink_metadata(inside).is_ok() {
        move_aside(base, inside);
    }
    std::fs::hard_link(outside, inside).unwrap();
}

fn temp_name(i: usize) -> String {
    format!("{TEMP_PREFIX}{:032x}", 0xabcdef00u128 + i as u128)
}

#[test]
fn qahn_same_folders_at_both_heads() {
    type Plant = Box<dyn Fn(&Path, &Path) -> Vec<PathBuf>>;
    let cases: Vec<(&str, Plant)> = vec![
        ("clean, one link each", Box::new(|_b, _r| vec![])),
        ("a pending anchor (copy of current), one link", Box::new(|_b, r| {
            std::fs::copy(r.join("anchors/current"), r.join("anchors/pending")).unwrap();
            std::fs::set_permissions(r.join("anchors/pending"), std::fs::Permissions::from_mode(0o600)).unwrap();
            vec![]
        })),
        ("lock absent", Box::new(|b, r| { move_aside(b, &r.join("lock")); vec![] })),
        ("lock a symlink to an outside file", Box::new(|b, r| {
            let o = outside_copy(b, &r.join("lock"), "sl", 0o600);
            move_aside(b, &r.join("lock"));
            std::os::unix::fs::symlink(&o, r.join("lock")).unwrap();
            vec![o]
        })),
        ("anchors/current a symlink to an outside copy", Box::new(|b, r| {
            let o = outside_copy(b, &r.join("anchors/current"), "slc", 0o600);
            move_aside(b, &r.join("anchors/current"));
            std::os::unix::fs::symlink(&o, r.join("anchors/current")).unwrap();
            vec![o]
        })),
        ("anchors/limits a symlink to an outside copy", Box::new(|b, r| {
            let o = outside_copy(b, &r.join("anchors/limits"), "sll", 0o600);
            move_aside(b, &r.join("anchors/limits"));
            std::os::unix::fs::symlink(&o, r.join("anchors/limits")).unwrap();
            vec![o]
        })),
        ("an unknown file zz in the root", Box::new(|_b, r| {
            std::fs::write(r.join("zz"), b"x").unwrap();
            std::fs::set_permissions(r.join("zz"), std::fs::Permissions::from_mode(0o600)).unwrap();
            vec![]
        })),
        ("an unknown file zz in anchors", Box::new(|_b, r| {
            std::fs::write(r.join("anchors/zz"), b"x").unwrap();
            std::fs::set_permissions(r.join("anchors/zz"), std::fs::Permissions::from_mode(0o600)).unwrap();
            vec![]
        })),
        ("anchors/current mode 0644", Box::new(|_b, r| {
            std::fs::set_permissions(r.join("anchors/current"), std::fs::Permissions::from_mode(0o644)).unwrap();
            vec![]
        })),
        ("a directory at anchors/pending", Box::new(|_b, r| {
            std::fs::create_dir(r.join("anchors/pending")).unwrap();
            std::fs::set_permissions(r.join("anchors/pending"), std::fs::Permissions::from_mode(0o700)).unwrap();
            vec![]
        })),
        ("65 leftover temps in anchors", Box::new(|_b, r| {
            for i in 0..65 {
                let p = r.join("anchors").join(temp_name(i));
                std::fs::write(&p, b"t").unwrap();
                std::fs::set_permissions(&p, std::fs::Permissions::from_mode(0o600)).unwrap();
            }
            vec![]
        })),
        ("CONTROL archive bundle with a 2nd link: a leftover temp beside it", Box::new(|_b, r| {
            let a = r.join("archive");
            let f = std::fs::read_dir(&a).unwrap().next().unwrap().unwrap().path();
            std::fs::hard_link(&f, a.join(temp_name(1))).unwrap();
            vec![]
        })),
        ("CONTROL archive bundle with a 2nd link OUTSIDE the folder", Box::new(|b, r| {
            let a = r.join("archive");
            let f = std::fs::read_dir(&a).unwrap().next().unwrap().unwrap().path();
            let o = b.join("outside-bundle");
            std::fs::hard_link(&f, &o).unwrap();
            vec![o]
        })),
        ("anchors/current hard-linked to an outside 0644 copy (Rights AND a 2nd link)", Box::new(|b, r| {
            let o = outside_copy(b, &r.join("anchors/current"), "r644", 0o644);
            relink(b, &o, &r.join("anchors/current"));
            vec![o]
        })),
        ("lock a symlink to an outside file that has 2 links", Box::new(|b, r| {
            let o = outside_copy(b, &r.join("lock"), "sl2", 0o600);
            std::fs::hard_link(&o, b.join("outside-sl2-second")).unwrap();
            move_aside(b, &r.join("lock"));
            std::os::unix::fs::symlink(&o, r.join("lock")).unwrap();
            vec![o]
        })),
        ("anchors/current = a hard link of a symlink (hard_link on a symlink path)", Box::new(|b, r| {
            let o = outside_copy(b, &r.join("anchors/current"), "hsl", 0o600);
            let sl = b.join("outside-symlink");
            std::os::unix::fs::symlink(&o, &sl).unwrap();
            move_aside(b, &r.join("anchors/current"));
            std::fs::hard_link(&sl, r.join("anchors/current")).unwrap();
            vec![o]
        })),
        ("MULTI lock 2 links + unknown file zz in root (sorted after lock)", Box::new(|b, r| {
            let o = outside_copy(b, &r.join("lock"), "m1", 0o600);
            relink(b, &o, &r.join("lock"));
            std::fs::write(r.join("zz"), b"x").unwrap();
            std::fs::set_permissions(r.join("zz"), std::fs::Permissions::from_mode(0o600)).unwrap();
            vec![o]
        })),
        ("MULTI lock 2 links + unknown file aa in root (sorted before lock)", Box::new(|b, r| {
            let o = outside_copy(b, &r.join("lock"), "m2", 0o600);
            relink(b, &o, &r.join("lock"));
            std::fs::write(r.join("aa"), b"x").unwrap();
            std::fs::set_permissions(r.join("aa"), std::fs::Permissions::from_mode(0o600)).unwrap();
            vec![o]
        })),
        ("MULTI lock 2 links + an unknown file in anchors", Box::new(|b, r| {
            let o = outside_copy(b, &r.join("lock"), "m3", 0o600);
            relink(b, &o, &r.join("lock"));
            std::fs::write(r.join("anchors/zz"), b"x").unwrap();
            std::fs::set_permissions(r.join("anchors/zz"), std::fs::Permissions::from_mode(0o600)).unwrap();
            vec![o]
        })),
        ("MULTI anchors/current 2 links + 65 temps in anchors", Box::new(|b, r| {
            let o = outside_copy(b, &r.join("anchors/current"), "m4", 0o600);
            relink(b, &o, &r.join("anchors/current"));
            for i in 0..65 {
                let p = r.join("anchors").join(temp_name(i));
                std::fs::write(&p, b"t").unwrap();
                std::fs::set_permissions(&p, std::fs::Permissions::from_mode(0o600)).unwrap();
            }
            vec![o]
        })),
        ("MULTI anchors/current 2 links to a DAMAGED outside file", Box::new(|b, r| {
            let o = b.join("outside-m5");
            std::fs::write(&o, b"not an anchor at all").unwrap();
            std::fs::set_permissions(&o, std::fs::Permissions::from_mode(0o600)).unwrap();
            relink(b, &o, &r.join("anchors/current"));
            vec![o]
        })),
        ("MULTI anchors/limits 2 links + a symlink at anchors/pending", Box::new(|b, r| {
            let o = outside_copy(b, &r.join("anchors/limits"), "m6", 0o600);
            relink(b, &o, &r.join("anchors/limits"));
            std::os::unix::fs::symlink(&o, r.join("anchors/pending")).unwrap();
            vec![o]
        })),
    ];
    for (i, (name, plant)) in cases.into_iter().enumerate() {
        let (w, base, root) = folder(100 + i as u8, &format!("qahn-same-{i}"));
        let outs = plant(&base, &root);
        let o_before: Vec<_> = outs.iter().map(|p| seen(p)).collect();
        let f_before = tree(&root);
        let r = open_host(&w, 1, &root, cfg(&w), 50);
        let ans = match &r {
            Ok((h, rep)) => format!(
                "Ok(report {rep:?}; segment {:?}; own seq {:?})",
                h.status().map(|s| s.segment),
                h.status().map(|s| s.own_seq)
            ),
            Err(e) => format!("Err({e:?})"),
        };
        let refused = r.is_err();
        drop(r);
        let o_after: Vec<_> = outs.iter().map(|p| seen(p)).collect();
        let f_after = tree(&root);
        let folder_changed: Vec<String> = f_after
            .iter()
            .filter(|x| !f_before.contains(x))
            .map(|(p, _)| p.strip_prefix(&root).unwrap().display().to_string())
            .chain(
                f_before
                    .iter()
                    .filter(|(p, _)| !f_after.iter().any(|(q, _)| q == p))
                    .map(|(p, _)| format!("GONE {}", p.strip_prefix(&root).unwrap().display())),
            )
            .collect();
        println!(
            "QAHN SAME {i:02} {name} | {ans} | outside unchanged {} | folder changed by a {} open: {folder_changed:?}",
            o_before == o_after,
            if refused { "REFUSED" } else { "accepted" }
        );
    }
}
