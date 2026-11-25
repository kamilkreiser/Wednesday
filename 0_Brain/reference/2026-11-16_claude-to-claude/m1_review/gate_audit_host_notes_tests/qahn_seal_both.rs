//! QA-AUDIT-HOST-NOTES (independent check of branch `audit-host-notes`), item 6: N-d attacked, and
//! every other `SealReport` field compared. Compiles at 9145840 AND at 52ad858 (never touches the new
//! field); uncommitted, checker's trees only (one `mod qahn_seal_both;` line).

use std::cell::Cell;
use std::rc::Rc;

use super::common::*;
use super::copy_tree;
use crate::fsio::fault::{self, Op, Rule};
use crate::{AuditHost, Causer, SealTrigger};

fn archive_count(h: &AuditHost) -> usize {
    h.archive_files().map(|v| v.len()).unwrap_or(usize::MAX)
}

fn anchors_listing(root: &std::path::Path) -> Vec<String> {
    let mut v: Vec<String> = std::fs::read_dir(root.join("anchors"))
        .unwrap()
        .map(|e| e.unwrap().file_name().into_string().unwrap())
        .collect();
    v.sort();
    v
}

/// How step 0 is made to leave a write unwritten (each a persistent fault until cleared):
/// `poison`: step 0's store put has its directory sync failed (P-4: the checkpoint lands through a
/// re-open); then from the first operation of kind `op` on `anchors/<name>`, every such operation fails.
#[derive(Clone, Copy, Debug)]
struct Step0 {
    poison: bool,
    name: &'static str,
    op: Op,
}

fn rule(s: Step0, on: Rc<Cell<bool>>) -> Rule {
    let mut poisoned = !s.poison;
    Rule::FailEvery(Box::new(move |c| {
        if !on.get() {
            return false;
        }
        if !poisoned && c.op == Op::SyncDir && c.dir == "store" {
            poisoned = true;
            return true;
        }
        poisoned && c.dir == "anchors" && c.name == s.name && c.op == s.op
    }))
}

/// N-d: every way step 0 can leave a write unwritten (its own anchor save; after a P-4 re-open,
/// `anchors/limits` or `anchors/current`), at each of the write's five operations, persistent. Two
/// seals while the fault holds, then the fault cleared and the seal retried; a fresh open after.
/// Prints one line per case; at 9145840 it shows the seal planning while dirty (N-d itself).
#[test]
fn qahn_nd_every_step0_failure() {
    let ops = [Op::CreateTemp, Op::Write, Op::SyncFile, Op::Rename, Op::SyncDir];
    let mut cases = Vec::new();
    for op in ops {
        cases.push(Step0 { poison: false, name: "current", op });
        cases.push(Step0 { poison: true, name: "limits", op });
        cases.push(Step0 { poison: true, name: "current", op });
    }
    let mut bad = Vec::new();
    for (i, s) in cases.into_iter().enumerate() {
        let w = World::new(120, 3, 3);
        let base = scratch(&format!("qahn-nd-{i}"));
        let root = base.join("host");
        let mut h = create_host(&w, 1, &root, cfg(&w));
        for n in 0..3 {
            host_record(&mut h, &w.ids[1], Causer::LocalHuman, n + 1);
        }
        let k = h.member().unwrap().segment();
        let cps0 = h.member().unwrap().own().checkpoints().len();
        let files0 = archive_count(&h);
        let names0 = anchors_listing(&root);
        let limits0 = std::fs::read(root.join("anchors/limits")).unwrap();
        let on = Rc::new(Cell::new(true));
        fault::arm(rule(s, on.clone()));
        let mut tries = Vec::new();
        for a in 0..2 {
            let r = h.seal_begin(&w.ids[1], SealTrigger::OwnerCommand, t(10 + a));
            let short = match &r {
                Ok(b) => format!("Ok(seg {} file {})", b.segment, b.file),
                Err(e) => format!("Err({})", format!("{e:?}").split(" kind").next().unwrap_or("")),
            };
            let in_window = h.status().map(|x| x.in_window).unwrap_or(true);
            // a seal that began is finished here so the next try is a fresh seal_begin
            let fin = if r.is_ok() {
                format!("{:?}", h.seal_finish(&w.ids[1], t(20 + a)).map(|x| x.info.segment).map_err(|e| format!("{e:?}").chars().take(60).collect::<String>()))
            } else {
                "-".into()
            };
            let cur_disk = crate::host::read_anchor_file(&root.join("anchors/current")).ok().flatten();
            let m_anchor = h.member().ok().map(|m| m.anchor());
            tries.push(format!(
                "try{a}: {short} window {in_window} finish {fin}; archive {files0}->{}; anchors {:?}; limits bytes same {}; own cps {cps0}->{}; disk current = member anchor {}; limits dirty {}",
                archive_count(&h),
                anchors_listing(&root),
                std::fs::read(root.join("anchors/limits")).map(|b| b == limits0).unwrap_or(false),
                h.member().map(|m| m.own().checkpoints().len()).unwrap_or(usize::MAX),
                cur_disk.is_some() && cur_disk == m_anchor,
                h.limits_dirty()
            ));
            if r.is_ok() || in_window || archive_count(&h) != files0 || anchors_listing(&root) != names0 {
                bad.push(format!("{s:?} try{a}: planned while dirty"));
            }
        }
        let landed = h.member().unwrap().own().checkpoints().last().map(|c| c.head.clone());
        let cps1 = h.member().unwrap().own().checkpoints().len();
        on.set(false);
        let begun = h.seal_begin(&w.ids[1], SealTrigger::OwnerCommand, t(30));
        let begun_s = match &begun {
            Ok(b) => format!("Ok(seg {}, checkpoint = the landed one {})", b.segment, b.checkpoint == landed),
            Err(e) => format!("Err({e:?})"),
        };
        let cps2 = h.member().unwrap().own().checkpoints().len();
        let fin = h.seal_finish(&w.ids[1], t(31)).map(|x| x.info.segment);
        fault::disarm();
        let cps3 = h.member().map(|m| m.own().checkpoints().len()).unwrap_or(usize::MAX);
        let files3 = archive_count(&h);
        drop(h);
        let copy = base.join("copy");
        copy_tree(&root, &copy);
        let fresh = open_host(&w, 1, &copy, cfg(&w), 40)
            .map(|(h2, _)| (h2.member().unwrap().segment(), h2.member().unwrap().own().checkpoints().len(), archive_count(&h2)))
            .map_err(|e| format!("{e:?}"));
        let pending_left = root.join("anchors/pending").exists();
        println!(
            "QAHN ND {i:02} {s:?} | {} | cleared: seal_begin {begun_s}, own cps {cps1}->{cps2}, seal_finish {fin:?}, own cps then {cps3}, archive {files0}->{files3} | fresh open (seg, own cps, archive) {fresh:?}, pending left {pending_left}",
            tries.join(" | ")
        );
        if !(cps1 == cps0 + 1 && cps2 == cps1 && cps3 == cps1 && fin.as_ref().ok() == Some(&(k + 1)) && files3 == files0 + 1 && fresh == Ok((k + 1, cps0 + 1, files0 + 1)) && !pending_left) {
            bad.push(format!("{s:?}: after the fault cleared: own cps {cps0} -> {cps1} -> {cps2} -> {cps3}, seal {fin:?}, archive {files0} -> {files3}, fresh {fresh:?}, pending {pending_left}"));
        }
    }
    for b in &bad {
        println!("QAHN ND PROBLEM {b}");
    }
    assert!(bad.is_empty(), "{} problems", bad.len());
}

/// Every `SealReport` field but the new one, for the same seals at both heads: a clean seal, then a
/// seal with ONE operation failed at each index after the commit put's directory sync (the N-3
/// range: the collection and step 4), then all of them at once.
#[test]
fn qahn_seal_fields_at_both_heads() {
    let w = World::new(125, 3, 3);
    let tbase = scratch("qahn-sf-t");
    let troot = tbase.join("host");
    let mut h = create_host(&w, 1, &troot, cfg(&w));
    for n in 0..3 {
        host_record(&mut h, &w.ids[1], Causer::LocalHuman, n + 1);
    }
    drop(h);
    // the clean seal: operations and the commit put's sync index
    let probe = |rule: Rule, tag: &str| {
        let base = scratch(&format!("qahn-sf-{tag}"));
        let root = base.join("host");
        copy_tree(&troot, &root);
        let (mut h, _) = open_host(&w, 1, &root, cfg(&w), 50).unwrap();
        fault::arm(rule);
        let r = h.seal(&w.ids[1], SealTrigger::OwnerCommand, t(60));
        let rep = fault::disarm();
        let ans = match &r {
            Ok(s) => format!(
                "Ok(trigger {:?}, checkpoint {:?}, info {:?}, files {:?}, stale_retries {})",
                s.trigger, s.checkpoint, s.info, s.files, s.stale_retries
            ),
            Err(e) => format!("Err({e:?})"),
        };
        let after = h.member().map(|m| (m.segment(), m.limits())).map_err(|e| format!("{e:?}"));
        (rep, ans, after)
    };
    let (rep, ans, after) = probe(Rule::None, "clean");
    let n = rep.ops;
    let commit = rep
        .log
        .iter()
        .position(|(op, d, name)| *op == Op::SyncDir && d == "store" && name.contains(".F07."))
        .expect("commit put sync");
    println!("QAHN SF clean: {n} ops, commit put sync at {commit}; {ans}; member after {after:?}");
    let mut scheds: Vec<Vec<usize>> = ((commit + 1)..n).map(|i| vec![i]).collect();
    scheds.push(((commit + 1)..n).collect());
    for v in scheds {
        let v2 = v.clone();
        let mut i = 0usize;
        let (_, ans, after) = probe(
            Rule::FailEvery(Box::new(move |_c| {
                let hit = v2.contains(&i);
                i += 1;
                hit
            })),
            "f",
        );
        println!("QAHN SF {v:?}: {ans}; member after {after:?}");
    }
}
