//! QA-AUDIT-HOST-NOTES (independent check of branch `audit-host-notes`), item 6: the seal's new
//! `limits` field (N-c) attacked over the N-3 range, with and without the `cfg(test)` re-offer hook,
//! and with the N-3 re-open itself failing. Head 52ad858 only; uncommitted, checker's tree only.

use super::common::*;
use super::copy_tree;
use crate::fsio::fault::{self, Op, Rule};
use crate::host::test_hooks;
use crate::{Causer, HostError, SealTrigger};
use coagent_audit::session::StoreLimits;

#[test]
fn qahn_nc_range_with_and_without_hook() {
    let w = World::new(130, 3, 3);
    let tbase = scratch("qahn-nc-t");
    let troot = tbase.join("host");
    let d = StoreLimits::default();
    let mut c = cfg(&w);
    c.limits = StoreLimits { bytes: d.bytes / 2, records: d.records / 2 };
    let low = c.limits;
    let mut h = create_host(&w, 1, &troot, c.clone());
    for n in 0..3 {
        host_record(&mut h, &w.ids[1], Causer::LocalHuman, n + 1);
    }
    drop(h);
    let mut bad = Vec::new();
    let run = |hook: bool, v: Vec<usize>, also_reopen: bool, tag: &str| {
        let base = scratch(&format!("qahn-nc-{tag}"));
        let root = base.join("host");
        copy_tree(&troot, &root);
        let (mut h, _) = open_host(&w, 1, &root, c.clone(), 50).unwrap();
        let before = h.member().unwrap().limits();
        if hook {
            test_hooks::reoffer_refuses_next();
        }
        let mut i = 0usize;
        let mut poisoned_at: Option<usize> = None;
        fault::arm(Rule::FailEvery(Box::new(move |cx| {
            let n = i;
            i += 1;
            let mut hit = v.contains(&n);
            // optionally: once a listed failure has happened, also fail the N-3 re-open's own first
            // store directory sync (the store's open syncs the directory first)
            if also_reopen && cx.op == Op::SyncDir && cx.dir == "store" {
                if let Some(p) = poisoned_at {
                    if n > p {
                        hit = true;
                        poisoned_at = Some(usize::MAX - 1);
                    }
                }
            }
            if hit && poisoned_at.is_none() {
                poisoned_at = Some(n);
            }
            hit
        })));
        let r = h.seal(&w.ids[1], SealTrigger::OwnerCommand, t(60));
        let rep = fault::disarm();
        let hook_left = test_hooks::take_reoffer_refuses();
        let after = h.member().map(|m| m.limits());
        let closed = matches!(h.status(), Err(HostError::Closed));
        let ans = match &r {
            Ok(s) => format!("Ok(seg {}, limits {:?})", s.info.segment, s.limits.as_ref().map(|l| (l.before == Some(before), l.in_force == after.clone().unwrap_or(l.in_force), l.refused.clone(), l.differs()))),
            Err(e) => format!("Err({e:?})"),
        };
        (ans, r.ok().map(|s| s.limits), hook_left, after, closed, rep.ops, before)
    };
    // the clean seal: where is the commit put's sync?
    let base = scratch("qahn-nc-find");
    let root = base.join("host");
    copy_tree(&troot, &root);
    let (mut h, _) = open_host(&w, 1, &root, c.clone(), 50).unwrap();
    fault::arm(Rule::None);
    let r = h.seal(&w.ids[1], SealTrigger::OwnerCommand, t(60));
    let rep = fault::disarm();
    drop(h);
    let n = rep.ops;
    let commit = rep.log.iter().position(|(op, d, name)| *op == Op::SyncDir && d == "store" && name.contains(".F07.")).unwrap();
    println!("QAHN NC clean seal: {:?}; {n} ops; commit put sync at {commit}", r.map(|s| (s.info.segment, s.limits)));
    let mut scheds: Vec<Vec<usize>> = ((commit + 1)..n).map(|i| vec![i]).collect();
    scheds.push(((commit + 1)..n).collect());
    let (mut some, mut none_hook, mut none_nohook) = (0, 0, 0);
    for v in scheds {
        for hook in [false, true] {
            for also_reopen in [false, true] {
                let (ans, lim, hook_left, after, closed, _ops, before) = run(hook, v.clone(), also_reopen, "r");
                println!("QAHN NC {v:?} hook {hook} reopen-fails {also_reopen}: {ans}; hook left unused {hook_left}; host closed {closed}; limits in force after {after:?} (before {before:?}, low {})", before == low);
                match &lim {
                    Some(Some(l)) => {
                        some += 1;
                        // Some only when the limits changed, never with the re-open failed
                        if !hook || !l.differs() || closed || after.as_ref().ok() != Some(&l.in_force) || l.before != Some(before) {
                            bad.push(format!("{v:?} hook {hook} reopen-fails {also_reopen}: Some although {ans}"));
                        }
                    }
                    Some(None) => {
                        if hook { none_hook += 1 } else { none_nohook += 1 }
                        // None while the limits in force changed?
                        if after.as_ref().ok().is_some_and(|a| *a != before) {
                            bad.push(format!("{v:?} hook {hook} reopen-fails {also_reopen}: None although the limits changed {before:?} -> {after:?}"));
                        }
                        // the hook consumed (a re-open offered limits) and the host open: must have been Some
                        if hook && !hook_left && !closed {
                            bad.push(format!("{v:?}: the hook was consumed by a re-open that kept the host open, yet None"));
                        }
                    }
                    None => bad.push(format!("{v:?} hook {hook} reopen-fails {also_reopen}: the seal did not answer Ok: {ans}")),
                }
            }
        }
    }
    println!("QAHN NC tally: Some {some}; None with hook {none_hook}; None without hook {none_nohook}");
    for b in &bad {
        println!("QAHN NC PROBLEM {b}");
    }
    assert!(bad.is_empty(), "{} problems", bad.len());
}
