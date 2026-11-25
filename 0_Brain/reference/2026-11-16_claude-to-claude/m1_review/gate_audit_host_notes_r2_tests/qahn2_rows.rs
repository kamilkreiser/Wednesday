//! QA-AUDIT-HOST-NOTES-R2 (second check of `audit-host-notes`, head dbc9c0a): rows 14 and 15 of the
//! P-4 answer table, word by word, against the host as built. UNCOMMITTED; copied into my own tree as
//! `src/tests/qahn2_rows.rs` with one `mod qahn2_rows;` line. Prints `QAHN2 …` lines; panics on a
//! property the table promises.

use std::collections::BTreeMap;
use std::path::{Path, PathBuf};

use super::common::*;
use crate::fsio::fault::{self, Op, Rule};
use crate::settings::Percent;
use crate::{AuditHost, Causer, HostError, SealTrigger};

/// Every file under `root` (relative path -> content), plus every directory name: the folder's
/// whole state as bytes. `lock` (0 bytes) included.
fn snap(root: &Path) -> BTreeMap<String, Option<Vec<u8>>> {
    let mut out = BTreeMap::new();
    fn walk(base: &Path, p: &Path, out: &mut BTreeMap<String, Option<Vec<u8>>>) {
        let mut es: Vec<_> = std::fs::read_dir(p).unwrap().map(|e| e.unwrap()).collect();
        es.sort_by_key(|e| e.file_name());
        for e in es {
            let path = e.path();
            let rel = path.strip_prefix(base).unwrap().to_string_lossy().into_owned();
            let ft = e.file_type().unwrap();
            if ft.is_dir() {
                out.insert(format!("{rel}/"), None);
                walk(base, &path, out);
            } else {
                out.insert(rel, Some(std::fs::read(&path).unwrap()));
            }
        }
    }
    walk(root, root, &mut out);
    out
}

fn diff(a: &BTreeMap<String, Option<Vec<u8>>>, b: &BTreeMap<String, Option<Vec<u8>>>) -> Vec<String> {
    let mut d = Vec::new();
    for (k, v) in a {
        match b.get(k) {
            None => d.push(format!("-{k}")),
            Some(w) if w != v => d.push(format!("~{k}")),
            _ => {}
        }
    }
    for k in b.keys() {
        if !a.contains_key(k) {
            d.push(format!("+{k}"));
        }
    }
    d
}

fn base_dir(name: &str) -> (PathBuf, PathBuf) {
    let base = scratch(name);
    let root = base.join("host");
    (base, root)
}

fn own_cps(h: &AuditHost) -> usize {
    h.member().unwrap().own().checkpoints().len()
}

/// Item 5, row 15: each of the four refusals on a host with records leaves the folder byte for
/// byte as it was (names and contents), opens or closes no window, and the seal succeeds once the
/// condition holds. Control: a record changes the folder.
#[test]
fn qahn2_row15_refusals_write_nothing() {
    let w = World::new(151, 3, 3);
    let mut problems = Vec::new();

    // --- control: a successful record DOES change the folder
    {
        let (_b, root) = base_dir("qahn2-r15-ctl");
        let mut h = create_host(&w, 1, &root, cfg(&w));
        host_record(&mut h, &w.ids[1], Causer::LocalHuman, 1);
        let s0 = snap(&root);
        host_record(&mut h, &w.ids[1], Causer::LocalHuman, 2);
        let d = diff(&s0, &snap(&root));
        println!("QAHN2 R15 CONTROL a record: folder changes {d:?}");
        if d.is_empty() {
            problems.push("control: a record changed nothing".to_string());
        }
    }

    // --- TriggerOff: the timer not turned on (default settings), and a threshold not the owner's
    {
        let (_b, root) = base_dir("qahn2-r15-off");
        let mut h = create_host(&w, 1, &root, cfg(&w));
        for n in 0..3 {
            host_record(&mut h, &w.ids[1], Causer::LocalHuman, n + 1);
        }
        let (seg0, cps0) = (h.status().unwrap().segment, own_cps(&h));
        for trig in [SealTrigger::Timer, SealTrigger::OwnFreePartAt(Percent::new(10).unwrap())] {
            let s0 = snap(&root);
            let a = h.seal_begin(&w.ids[1], trig.clone(), t(100_000)).map(|b| b.segment);
            let b = h.seal(&w.ids[1], trig.clone(), t(100_000)).map(|r| r.info.segment);
            let st = h.status().unwrap();
            let d = diff(&s0, &snap(&root));
            println!(
                "QAHN2 R15 TriggerOff {trig:?}: seal_begin {a:?}; seal {b:?}; folder changes {d:?}; in window {}; segment {} -> {}; own checkpoints {} -> {}",
                st.in_window, seg0, st.segment, cps0, own_cps(&h)
            );
            if !matches!(a, Err(HostError::TriggerOff(_))) || !matches!(b, Err(HostError::TriggerOff(_))) {
                problems.push(format!("TriggerOff {trig:?}: {a:?} / {b:?}"));
            }
            if !d.is_empty() || st.in_window || st.segment != seg0 || own_cps(&h) != cps0 {
                problems.push(format!("TriggerOff {trig:?} wrote or moved something: {d:?}"));
            }
        }
        // the condition then holds: the owner's settings turn the timer on (an open with them)
        drop(h);
        let mut c = cfg(&w);
        c.settings.timer_ms = Some(1_000);
        let (mut h, _) = open_host(&w, 1, &root, c, 200_000).expect("open with the timer on");
        let r = h.seal(&w.ids[1], SealTrigger::Timer, t(201_000)).map(|r| r.info.segment);
        println!("QAHN2 R15 TriggerOff, then the timer turned on in the settings and due: seal {r:?}");
        if r.as_ref().ok() != Some(&1) {
            problems.push(format!("TriggerOff: the seal did not succeed once on: {r:?}"));
        }
    }

    // --- NotDue: the timer on (60 s) but not yet due
    {
        let (_b, root) = base_dir("qahn2-r15-notdue");
        let mut c = cfg(&w);
        c.settings.timer_ms = Some(60_000);
        let mut h = create_host(&w, 1, &root, c);
        for n in 0..3 {
            host_record(&mut h, &w.ids[1], Causer::LocalHuman, n + 1);
        }
        let (seg0, cps0) = (h.status().unwrap().segment, own_cps(&h));
        let s0 = snap(&root);
        let a = h.seal_begin(&w.ids[1], SealTrigger::Timer, t(59_999)).map(|b| b.segment);
        let b = h.seal(&w.ids[1], SealTrigger::Timer, t(30_000)).map(|r| r.info.segment);
        let st = h.status().unwrap();
        let d = diff(&s0, &snap(&root));
        println!(
            "QAHN2 R15 NotDue: seal_begin {a:?}; seal {b:?}; folder changes {d:?}; in window {}; segment {} -> {}; own checkpoints {} -> {}",
            st.in_window, seg0, st.segment, cps0, own_cps(&h)
        );
        if !matches!(a, Err(HostError::NotDue(_))) || !matches!(b, Err(HostError::NotDue(_))) {
            problems.push(format!("NotDue: {a:?} / {b:?}"));
        }
        if !d.is_empty() || st.in_window || st.segment != seg0 || own_cps(&h) != cps0 {
            problems.push(format!("NotDue wrote or moved something: {d:?}"));
        }
        let r = h.seal(&w.ids[1], SealTrigger::Timer, t(60_000)).map(|r| r.info.segment);
        println!("QAHN2 R15 NotDue, then due: seal {r:?}");
        if r.as_ref().ok() != Some(&1) {
            problems.push(format!("NotDue: the seal did not succeed once due: {r:?}"));
        }
    }

    // --- NoSealInProgress and SealInProgress
    {
        let (_b, root) = base_dir("qahn2-r15-window");
        let mut h = create_host(&w, 1, &root, cfg(&w));
        for n in 0..3 {
            host_record(&mut h, &w.ids[1], Causer::LocalHuman, n + 1);
        }
        let (seg0, cps0) = (h.status().unwrap().segment, own_cps(&h));
        let s0 = snap(&root);
        let a = h.seal_finish(&w.ids[1], t(10)).map(|r| r.info.segment);
        let st = h.status().unwrap();
        let d = diff(&s0, &snap(&root));
        println!(
            "QAHN2 R15 NoSealInProgress: seal_finish {a:?}; folder changes {d:?}; in window {}; segment {} -> {}; own checkpoints {} -> {}",
            st.in_window, seg0, st.segment, cps0, own_cps(&h)
        );
        if !matches!(a, Err(HostError::NoSealInProgress)) || !d.is_empty() || st.in_window || own_cps(&h) != cps0 {
            problems.push(format!("NoSealInProgress: {a:?} {d:?}"));
        }

        let begun = h.seal_begin(&w.ids[1], SealTrigger::OwnerCommand, t(20)).map(|b| (b.segment, b.file));
        let s1 = snap(&root);
        let (st1, cps1) = (h.status().unwrap(), own_cps(&h));
        let a = h.seal_begin(&w.ids[1], SealTrigger::OwnerCommand, t(21)).map(|b| b.segment);
        let b = h.seal(&w.ids[1], SealTrigger::OwnerCommand, t(22)).map(|r| r.info.segment);
        let st = h.status().unwrap();
        let d = diff(&s1, &snap(&root));
        println!(
            "QAHN2 R15 SealInProgress: (window opened by seal_begin {begun:?}; in window {}); seal_begin again {a:?}; seal {b:?}; folder changes {d:?}; still in window {}; segment {} -> {}; own checkpoints {} -> {}",
            st1.in_window, st.in_window, st1.segment, st.segment, cps1, own_cps(&h)
        );
        if !matches!(a, Err(HostError::SealInProgress)) || !matches!(b, Err(HostError::SealInProgress)) {
            problems.push(format!("SealInProgress: {a:?} / {b:?}"));
        }
        if !d.is_empty() || !st.in_window || st.segment != st1.segment || own_cps(&h) != cps1 {
            problems.push(format!("SealInProgress wrote, closed or moved something: {d:?}"));
        }
        let f = h.seal_finish(&w.ids[1], t(23)).map(|r| r.info.segment);
        println!("QAHN2 R15 SealInProgress, then seal_finish (the window closed): {f:?}; in window {}", h.status().unwrap().in_window);
        // the seal when the condition holds: one more own record, then a whole seal
        host_record(&mut h, &w.ids[1], Causer::LocalHuman, 30);
        let r = h.seal(&w.ids[1], SealTrigger::OwnerCommand, t(31)).map(|r| r.info.segment);
        println!("QAHN2 R15 then the seal with no window open: {r:?}");
        if f.as_ref().ok() != Some(&1) || r.as_ref().ok() != Some(&2) {
            problems.push(format!("SealInProgress: finish {f:?}, next seal {r:?}"));
        }
        // NoSealInProgress: "the seal when the condition holds" = a whole seal
        let a = h.seal_finish(&w.ids[1], t(40));
        host_record(&mut h, &w.ids[1], Causer::LocalHuman, 41);
        let r = h.seal(&w.ids[1], SealTrigger::OwnerCommand, t(42)).map(|r| r.info.segment);
        println!("QAHN2 R15 NoSealInProgress again {:?}, then a whole seal {r:?}", a.map(|r| r.info.segment));
        if r.as_ref().ok() != Some(&3) {
            problems.push(format!("NoSealInProgress: the whole seal after it {r:?}"));
        }
    }
    println!("QAHN2 R15 problems: {}", problems.len());
    assert!(problems.is_empty(), "row 15: {problems:#?}");
}

/// Item 5, row 14: a step 2 failure (each of the archive file's and the pending anchor's five
/// operations), then the words: no window, nothing committed (segment, and a FRESH open of a copy
/// of the folder: segment 0, no pending kept), the retry once: segment 1 once and own checkpoints
/// unchanged by the retry. Also `NothingToSeal` (an `Audit(..)` of `seal_export`) retried, and a
/// retry after new own records (does step 0 then make a checkpoint?).
#[test]
fn qahn2_row14_words() {
    let w = World::new(152, 3, 3);
    let mut problems = Vec::new();
    let cases: Vec<(&str, &str, Op)> = vec![
        ("archive", "seg", Op::CreateTemp),
        ("archive", "seg", Op::Write),
        ("archive", "seg", Op::SyncFile),
        ("archive", "seg", Op::Link),
        ("archive", "seg", Op::SyncDir),
        ("anchors", "pending", Op::CreateTemp),
        ("anchors", "pending", Op::Write),
        ("anchors", "pending", Op::SyncFile),
        ("anchors", "pending", Op::Rename),
        ("anchors", "pending", Op::SyncDir),
    ];
    for (dir, which, op) in cases {
        let (base, root) = base_dir("qahn2-r14");
        let mut h = create_host(&w, 1, &root, cfg(&w));
        for n in 0..3 {
            host_record(&mut h, &w.ids[1], Causer::LocalHuman, n + 1);
        }
        let cps0 = own_cps(&h);
        let mut done = false;
        let opn = format!("{op:?}");
        fault::arm(Rule::FailEvery(Box::new(move |c| {
            let hit = c.dir == dir
                && c.op == op
                && (if which == "pending" { c.name == "pending" } else { c.name.starts_with("seg-") || c.op == Op::SyncDir });
            if !done && hit {
                done = true;
                return true;
            }
            false
        })));
        let r = h.seal(&w.ids[1], SealTrigger::OwnerCommand, t(10));
        fault::disarm();
        let st = h.status().unwrap();
        let cps1 = own_cps(&h);
        let has_pending = root.join("anchors").join("pending").exists();
        // a fresh open of a copy taken now (the caller does NOT retry; a restart)
        let copy = base.join("copy");
        super::copy_tree(&root, &copy);
        let fresh = open_host(&w, 1, &copy, cfg(&w), 20).map(|(f, _)| {
            let s = f.status().unwrap();
            (s.segment, f.member().unwrap().own().checkpoints().len(), s.archive_files, copy.join("anchors/pending").exists())
        });
        // the seal once, in two halves so the own chain is counted BEFORE the seal collects it
        let landed = h.member().unwrap().own().checkpoints().last().map(|c| c.head.clone());
        let begun = h.seal_begin(&w.ids[1], SealTrigger::OwnerCommand, t(11));
        let cps2 = own_cps(&h);
        let same_cp = begun.as_ref().map(|b| b.checkpoint == landed).unwrap_or(false);
        let again = h.seal_finish(&w.ids[1], t(11)).map(|s| (s.info.segment, same_cp));
        let st2 = h.status().unwrap();
        println!(
            "QAHN2 R14 [{dir}/{which} {opn}]: seal {:?}; in window {}; segment {}; own checkpoints {cps0} -> {cps1}; archive files {}; anchors/pending on disk {has_pending}; fresh open of a copy (segment, own cps, archive files, pending after) {fresh:?}; the seal once (segment, SealBegun::checkpoint is the landed one) {again:?}; own checkpoints inside its window {cps2}; segment {}; archive files {}",
            r.as_ref().map(|s| s.info.segment),
            st.in_window, st.segment, st.archive_files, st2.segment, st2.archive_files
        );
        if r.is_ok() || st.in_window || st.segment != 0 {
            problems.push(format!("{dir}/{which} {opn}: answer {:?}, window {}, segment {}", r.map(|s| s.info.segment), st.in_window, st.segment));
        }
        if fresh.as_ref().map(|f| f.0).ok() != Some(0) {
            problems.push(format!("{dir}/{which} {opn}: fresh open {fresh:?}"));
        }
        if again.as_ref().ok() != Some(&(1, true)) || cps2 != cps1 || st2.segment != 1 {
            problems.push(format!("{dir}/{which} {opn}: retry {again:?}, cps {cps1} -> {cps2}"));
        }
    }

    // NothingToSeal: a seal right after a seal (nothing new), retried once as row 14 permits
    {
        let (_b, root) = base_dir("qahn2-r14-nts");
        let mut h = create_host(&w, 1, &root, cfg(&w));
        for n in 0..3 {
            host_record(&mut h, &w.ids[1], Causer::LocalHuman, n + 1);
        }
        let r0 = h.seal(&w.ids[1], SealTrigger::OwnerCommand, t(10)).map(|s| s.info.segment);
        let cps0 = own_cps(&h);
        let s0 = snap(&root);
        let r1 = h.seal(&w.ids[1], SealTrigger::OwnerCommand, t(11)).map(|s| s.info.segment);
        let d1 = diff(&s0, &snap(&root));
        let cps1 = own_cps(&h);
        let r2 = h.seal(&w.ids[1], SealTrigger::OwnerCommand, t(12)).map(|s| s.info.segment);
        let d2 = diff(&s0, &snap(&root));
        println!(
            "QAHN2 R14 NothingToSeal: first seal {r0:?}; a seal with nothing new {r1:?} (folder changes {d1:?}, own checkpoints {cps0} -> {cps1}); retried once {r2:?} (folder changes since {d2:?}, own checkpoints {})",
            own_cps(&h)
        );
        if !matches!(r1, Err(HostError::Audit(coagent_audit::AuditError::NothingToSeal))) {
            println!("QAHN2 R14 NothingToSeal: NOTE the second seal answered {r1:?}");
        }
    }

    // a step 2 failure, then NEW own records, then the seal once: step 0 checkpoints the new events
    {
        let (_b, root) = base_dir("qahn2-r14-new");
        let mut h = create_host(&w, 1, &root, cfg(&w));
        for n in 0..3 {
            host_record(&mut h, &w.ids[1], Causer::LocalHuman, n + 1);
        }
        let mut done = false;
        fault::arm(Rule::FailEvery(Box::new(move |c| {
            if !done && c.dir == "archive" && c.op == Op::Link {
                done = true;
                return true;
            }
            false
        })));
        let r = h.seal(&w.ids[1], SealTrigger::OwnerCommand, t(10)).map(|s| s.info.segment);
        fault::disarm();
        let cps1 = own_cps(&h);
        host_record(&mut h, &w.ids[1], Causer::LocalHuman, 20);
        let begun = h.seal_begin(&w.ids[1], SealTrigger::OwnerCommand, t(21)).map(|b| b.checkpoint.map(|c| c.author_seq));
        let cps2 = own_cps(&h);
        let again = h.seal_finish(&w.ids[1], t(21)).map(|s| s.info.segment);
        println!(
            "QAHN2 R14 new records between: seal {r:?}; own checkpoints after it {cps1}; one record; seal_begin (its checkpoint's own seq) {begun:?}; own checkpoints inside the window {cps2}; seal_finish {again:?}"
        );
    }
    println!("QAHN2 R14 problems: {}", problems.len());
    assert!(problems.is_empty(), "row 14: {problems:#?}");
}
