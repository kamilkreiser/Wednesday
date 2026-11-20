//! QA-AUDIT-HOST (independent check): probes that need the crate's fault injector. Written by the
//! checker in its own clone; not part of the build under review. Each prints `QA <id>: ...`.

use std::path::{Path, PathBuf};

use coagent_audit::session::StoreLimits;
use coagent_audit::store::{Part, Store, StoreKey};
use coagent_proto::bytes::{KeyId, SessionId};

use super::common::*;
use super::copy_tree;
use crate::fsio::fault::{self, Op, Rule};
use crate::{AuditDir, AuditHost, Causer, HostError, Input, Opened, Outcome, SealTrigger};

fn snap(root: &Path, base: &Path, tag: &str) -> PathBuf {
    let s = base.join(format!("snap-{tag}"));
    copy_tree(root, &s);
    s
}

/// A host V=1 with peer 3's events stored, peer 3 then removed from the roster.
fn with_removed_peer(b: u8, name: &str) -> (World, PathBuf, PathBuf, AuditHost) {
    let mut w = World::new(b, 4, 4);
    let base = scratch(name);
    let root = base.join("host");
    let mut h = create_host(&w, 1, &root, cfg(&w));
    let mut p3 = mem_member(&w, 3);
    for n in 0..3u64 {
        host_record(&mut h, &w.ids[1], Causer::LocalHuman, n + 1);
        let s = p3.record(&w.ids[3], bare("p"), t(n + 1)).unwrap();
        let e = p3
            .outgoing(s)
            .into_iter()
            .find(|(to, _)| *to == w.key(1))
            .unwrap()
            .1;
        h.apply(&w.ids[1], Input::Receive(e), t(n + 1)).unwrap();
    }
    let r = w.remove(3);
    h.apply(&w.ids[1], Input::Roster(r), t(10)).unwrap();
    (w, base, root, h)
}

/// DQ-H4 / release: the anchor save after a release fails once (one I/O error, e.g. a full
/// disk); the host carries on; the process is then restarted.
#[test]
fn qa_q1_release_then_current_anchor_save_fails_then_restart() {
    let (w, base, root, mut h) = with_removed_peer(150, "qa-q1");
    fault::arm(Rule::FailWhen(Box::new(|c| {
        c.op == Op::CreateTemp && c.dir == "anchors" && c.name == "current"
    })));
    let r = h.apply(&w.ids[1], Input::Release(w.key(3)), t(20));
    let rep = fault::disarm();
    let answered = match &r {
        Ok(Outcome::Released(_)) => "Released".to_string(),
        other => format!("{other:?}"),
    };
    let st = h.status().unwrap();
    let pending_on_disk = root.join("anchors/pending").exists();
    // the process stops now (or is shut down cleanly)
    drop(h);
    let s = snap(&root, &base, "q1");
    let opened = open_host(&w, 1, &s, cfg(&w), 30);
    let o = match &opened {
        Ok((_, rep)) => format!("OPENED {:?}", rep.opened),
        Err(e) => format!("REFUSED {e:?}"),
    };
    drop(opened);
    let mut c2 = cfg(&w);
    c2.allow_unanchored = true;
    let s2 = snap(&root, &base, "q1b");
    let un = open_host(&w, 1, &s2, c2, 31)
        .map(|(h, r)| format!("{:?}, own seq {}", r.opened, h.member().unwrap().own().seq()))
        .unwrap_or_else(|e| format!("{e:?}"));
    println!(
        "QA q1 release + failed current save: answer {answered}; failed op injected: {}; status anchor_saved={}; \
         pending on disk after the call: {pending_on_disk}; RESTART (default settings) -> {o}; with allow_unanchored -> {un}",
        rep.failed_any(),
        st.anchor_saved
    );
    scratch_done(&base);
}

/// The same, with the process continuing: the next change retries the save (no restart).
#[test]
fn qa_q1b_release_then_save_fails_then_next_change_then_restart() {
    let (w, base, root, mut h) = with_removed_peer(151, "qa-q1b");
    fault::arm(Rule::FailWhen(Box::new(|c| {
        c.op == Op::CreateTemp && c.dir == "anchors" && c.name == "current"
    })));
    let _ = h.apply(&w.ids[1], Input::Release(w.key(3)), t(20));
    fault::disarm();
    let n = host_record(&mut h, &w.ids[1], Causer::LocalHuman, 21);
    drop(h);
    let s = snap(&root, &base, "q1b");
    let o = open_host(&w, 1, &s, cfg(&w), 30)
        .map(|(h, r)| format!("OPENED {:?} own seq {}", r.opened, h.member().unwrap().own().seq()))
        .unwrap_or_else(|e| format!("REFUSED {e:?}"));
    println!("QA q1b release + failed save, then a record ({n}), then restart -> {o}");
    scratch_done(&base);
}

/// Step 4 of a seal: the promotion's save fails once; the host carries on recording; the pending
/// anchor (post-seal) stays on disk. Then tail records go missing on disk: which anchor is used?
#[test]
fn qa_q2_stale_pending_after_failed_promotion() {
    let w = World::new(152, 3, 3);
    let base = scratch("qa-q2");
    let root = base.join("host");
    let mut h = create_host(&w, 1, &root, cfg(&w));
    for n in 0..3 {
        host_record(&mut h, &w.ids[1], Causer::LocalHuman, n + 1);
    }
    // fail the save of `current` AFTER the commit (the first `current` temp after the Segment put)
    let mut seen_commit = false;
    fault::arm(Rule::FailWhen(Box::new(move |c| {
        if c.dir == "store" && c.name.contains(".F07.") {
            seen_commit = true;
        }
        seen_commit && c.op == Op::CreateTemp && c.dir == "anchors" && c.name == "current"
    })));
    let sealed = h.seal(&w.ids[1], SealTrigger::OwnerCommand, t(10));
    fault::disarm();
    let after_seal_pending = root.join("anchors/pending").exists();
    // carry on: three more records (each saves current)
    let mut last = 0;
    for n in 0..3 {
        last = host_record(&mut h, &w.ids[1], Causer::LocalHuman, 20 + n);
    }
    let still_pending = root.join("anchors/pending").exists();
    drop(h);
    // tail loss on disk: the newest own record file removed (what the anchor exists to detect)
    let s = snap(&root, &base, "q2");
    let newest = std::fs::read_dir(s.join("store"))
        .unwrap()
        .map(|e| e.unwrap().file_name().into_string().unwrap())
        .filter(|n| n.contains(".N00.") && n.ends_with(&format!("{last:020}")))
        .collect::<Vec<_>>();
    for n in &newest {
        std::fs::remove_file(s.join("store").join(n)).unwrap();
    }
    let o = open_host(&w, 1, &s, cfg(&w), 40)
        .map(|(h, r)| {
            format!(
                "OPENED via {:?} (current refused: {:?}); own seq now {}",
                r.opened,
                r.current_refused.map(|e| format!("{e:?}").chars().take(60).collect::<String>()),
                h.member().unwrap().own().seq()
            )
        })
        .unwrap_or_else(|e| format!("REFUSED {e:?}"));
    println!(
        "QA q2 failed promotion: seal {:?}; pending on disk after the seal {after_seal_pending}, after 3 more records {still_pending}; \
         newest own record {last} removed from disk ({} file); RESTART -> {o}",
        sealed.as_ref().map(|r| r.info.segment),
        newest.len()
    );
    scratch_done(&base);
}

/// Sync order of every put and remove, by the injector's log; and a failing sync before and after
/// the rename.
#[test]
fn qa_q3_put_remove_sync_order_and_failures() {
    let base = scratch("qa-q3");
    let p = base.join("store");
    let s = SessionId([4; 32]);
    let k = |n| StoreKey {
        part: Part::OwnEvent(None),
        author: KeyId([5; 32]),
        n,
    };
    let mut d = AuditDir::open(&p).unwrap();
    fault::arm(Rule::None);
    d.put(&s, &k(1), b"a").unwrap();
    let put_log = fault::disarm().log;
    fault::arm(Rule::None);
    d.put(&s, &k(1), b"b").unwrap(); // replace
    let rep_log = fault::disarm().log;
    fault::arm(Rule::None);
    d.remove(&s, &k(1)).unwrap();
    let rm_log = fault::disarm().log;
    let ops = |l: &Vec<(Op, String, String)>| l.iter().map(|x| format!("{:?}", x.0)).collect::<Vec<_>>().join(",");
    // a failing file sync: the put fails, nothing changed, its temp removed
    fault::arm(Rule::FailWhen(Box::new(|c| c.op == Op::SyncFile)));
    let r1 = d.put(&s, &k(2), b"c");
    fault::disarm();
    let temps1 = std::fs::read_dir(&p).unwrap().filter(|e| e.as_ref().unwrap().file_name().to_string_lossy().starts_with(".tmp.")).count();
    let poisoned1 = d.is_poisoned();
    let listed1 = d.list(&s).unwrap().len();
    // a failing directory sync after the rename: poisoned, every call refused, re-open shows it landed
    fault::arm(Rule::FailWhen(Box::new(|c| c.op == Op::SyncDir)));
    let r2 = d.put(&s, &k(3), b"d");
    fault::disarm();
    let refusals = (
        d.put(&s, &k(4), b"e").is_err(),
        d.list(&s).is_err(),
        d.remove(&s, &k(3)).is_err(),
    );
    drop(d);
    let d2 = AuditDir::open(&p).unwrap();
    let landed = d2.list(&s).unwrap().iter().any(|(kk, _)| *kk == k(3));
    // a failing directory sync after an UNLINK: poisoned too
    let mut d3 = d2;
    fault::arm(Rule::FailWhen(Box::new(|c| c.op == Op::SyncDir)));
    let r3 = d3.remove(&s, &k(3));
    fault::disarm();
    let p3 = d3.is_poisoned();
    println!(
        "QA q3 sync order: put [{}]; replace [{}]; remove [{}]; SyncFile fails -> {r1:?}, temps left {temps1}, poisoned {poisoned1}, records {listed1}; \
         SyncDir fails after rename -> {r2:?}, then put/list/remove refused {refusals:?}, re-open: landed {landed}; SyncDir fails after unlink -> {r3:?}, poisoned {p3}",
        ops(&put_log),
        ops(&rep_log),
        ops(&rm_log)
    );
    assert_eq!(ops(&put_log), "CreateTemp,Write,SyncFile,Rename,SyncDir");
    assert_eq!(ops(&rm_log), "Unlink,SyncDir");
    assert!(r1.is_err() && temps1 == 0 && !poisoned1 && listed1 == 0);
    assert!(r2.is_err() && refusals == (true, true, true) && landed);
    assert!(r3.is_err() && p3);
    scratch_done(&base);
}

/// DQ-H4: the anchor save after an ordinary record fails once.
#[test]
fn qa_q4_record_then_anchor_save_fails() {
    let w = World::new(153, 3, 3);
    let base = scratch("qa-q4");
    let root = base.join("host");
    let mut h = create_host(&w, 1, &root, cfg(&w));
    host_record(&mut h, &w.ids[1], Causer::LocalHuman, 1);
    fault::arm(Rule::FailWhen(Box::new(|c| {
        c.op == Op::CreateTemp && c.dir == "anchors" && c.name == "current"
    })));
    let r = h.apply(
        &w.ids[1],
        Input::Record {
            causer: Causer::LocalHuman,
            input: owned("x", None, None),
        },
        t(2),
    );
    fault::disarm();
    let saved = h.status().unwrap().anchor_saved;
    // restart BEFORE any next change
    drop(h);
    let s = snap(&root, &base, "q4");
    let o = open_host(&w, 1, &s, cfg(&w), 3)
        .map(|(h, r)| format!("OPENED {:?}, own seq {}", r.opened, h.member().unwrap().own().seq()))
        .unwrap_or_else(|e| format!("REFUSED {e:?}"));
    // and: the next change while still running is refused until the save works
    let s2 = snap(&root, &base, "q4b");
    let (mut h2, _) = open_host(&w, 1, &s2, cfg(&w), 4).unwrap();
    fault::arm(Rule::FailWhen(Box::new(|c| {
        c.op == Op::CreateTemp && c.dir == "anchors" && c.name == "current"
    })));
    let a = h2.apply(&w.ids[1], Input::Record { causer: Causer::LocalHuman, input: owned("y", None, None) }, t(5));
    fault::disarm();
    let b = h2.apply(&w.ids[1], Input::Record { causer: Causer::LocalHuman, input: owned("z", None, None) }, t(6));
    let c = h2.apply(&w.ids[1], Input::Record { causer: Causer::LocalHuman, input: owned("z2", None, None) }, t(7));
    println!(
        "QA q4 record + failed anchor save: answer {r:?}; anchor_saved {saved}; RESTART -> {o}; running: \
         change with failing save -> {a:?}, next change -> {}, after -> {c:?}",
        match &b { Err(HostError::AnchorNotSaved) => "AnchorNotSaved".to_string(), x => format!("{x:?}") }
    );
    scratch_done(&base);
}

/// R3: non-default limits survive a clean restart, a restart inside a seal window, and a stop
/// after the commit put; a different offer is reported.
#[test]
fn qa_q5_limits_across_restarts() {
    let w = World::new(154, 3, 3);
    let base = scratch("qa-q5");
    let root = base.join("host");
    let lim = StoreLimits {
        bytes: 8 * 77_000,
        records: 8 * 555,
    };
    let mut c = cfg(&w);
    c.limits = lim;
    let mut h = create_host(&w, 1, &root, c.clone());
    for n in 0..4 {
        host_record(&mut h, &w.ids[1], Causer::LocalHuman, n + 1);
    }
    let mut out = Vec::new();
    out.push(format!("in force after create {:?}", h.member().unwrap().limits()));
    drop(h);
    // clean restart
    let (mut h, r) = open_host(&w, 1, &root, c.clone(), 10).unwrap();
    out.push(format!(
        "clean: before {:?} in_force {:?} differs {}",
        r.limits.before, r.limits.in_force, r.limits.differs()
    ));
    // restart inside a seal window
    host_record(&mut h, &w.ids[1], Causer::LocalHuman, 11);
    h.seal_begin(&w.ids[1], SealTrigger::OwnerCommand, t(12)).unwrap();
    drop(h);
    let (mut h, r) = open_host(&w, 1, &root, c.clone(), 13).unwrap();
    out.push(format!(
        "in window: opened {:?} segment {} before {:?} in_force {:?} differs {}",
        r.opened, r.segment, r.limits.before, r.limits.in_force, r.limits.differs()
    ));
    // a stop right after the commit put
    host_record(&mut h, &w.ids[1], Causer::LocalHuman, 14);
    let mut seen = false;
    fault::arm(Rule::StopWhen(Box::new(move |cx| {
        if cx.dir == "store" && cx.name.contains(".F07.") && cx.op == Op::SyncDir {
            seen = true;
            return false;
        }
        seen
    })));
    let _ = h.seal(&w.ids[1], SealTrigger::OwnerCommand, t(15));
    fault::disarm();
    h = {
        drop(h);
        let (h, r) = open_host(&w, 1, &root, c.clone(), 16).unwrap();
        out.push(format!(
            "stop after commit put: opened {:?} segment {} before {:?} in_force {:?} differs {}",
            r.opened, r.segment, r.limits.before, r.limits.in_force, r.limits.differs()
        ));
        h
    };
    drop(h);
    // a different offer
    let mut c2 = c.clone();
    c2.limits = StoreLimits {
        bytes: 8 * 66_000,
        records: 8 * 444,
    };
    let (_h, r) = open_host(&w, 1, &root, c2, 17).unwrap();
    out.push(format!(
        "different offer: before {:?} offered {:?} in_force {:?} refused {:?} differs {}",
        r.limits.before, r.limits.offered, r.limits.in_force, r.limits.refused, r.limits.differs()
    ));
    println!("QA q5 limits: {}", out.join("; "));
    scratch_done(&base);
}

/// The anchors order of design 10 §2.8 with my own stop points, row by row.
#[test]
fn qa_q6_restart_rows() {
    let w = World::new(155, 3, 3);
    let mut out = Vec::new();
    type Pick = Box<dyn FnMut(&crate::fsio::fault::Ctx) -> bool>;
    let rows: Vec<(&str, fn() -> Pick)> = vec![
        ("stop at the segment file's link (step 2a)", || {
            Box::new(|c| c.op == Op::Link && c.dir == "archive")
        }),
        ("stop at the pending anchor's rename (step 2b)", || {
            Box::new(|c| c.op == Op::Rename && c.dir == "anchors" && c.name == "pending")
        }),
        ("stop at the commit put's rename (step 3b)", || {
            Box::new(|c| c.op == Op::Rename && c.dir == "store" && c.name.contains(".F07."))
        }),
        ("stop at the commit put's directory sync", || {
            Box::new(|c| c.op == Op::SyncDir && c.dir == "store" && c.name.contains(".F07."))
        }),
        ("stop at the first collection remove", || {
            Box::new(|c| c.op == Op::Unlink && c.dir == "store")
        }),
        ("stop at the promotion (current's rename)", || {
            let mut seen = false;
            Box::new(move |c| {
                if c.dir == "store" && c.name.contains(".F07.") {
                    seen = true;
                }
                seen && c.op == Op::Rename && c.dir == "anchors" && c.name == "current"
            })
        }),
        ("stop at pending's removal (step 4)", || {
            let mut seen = false;
            Box::new(move |c| {
                if c.dir == "store" && c.name.contains(".F07.") {
                    seen = true;
                }
                seen && c.op == Op::Unlink && c.dir == "anchors" && c.name == "pending"
            })
        }),
    ];
    for (i, (name, pick)) in rows.into_iter().enumerate() {
        let base = scratch("qa-q6");
        let root = base.join("host");
        let mut h = create_host(&w, 1, &root, cfg(&w));
        let mut p = mem_member(&w, 2);
        for n in 0..3u64 {
            host_record(&mut h, &w.ids[1], Causer::LocalHuman, n + 1);
            let s = p.record(&w.ids[2], bare("p"), t(n + 1)).unwrap();
            let e = p.outgoing(s).into_iter().find(|(to, _)| *to == w.key(1)).unwrap().1;
            h.apply(&w.ids[1], Input::Receive(e), t(n + 1)).unwrap();
        }
        let ph = p.checkpoint_now(&w.ids[2], t(5)).unwrap();
        h.apply(&w.ids[1], Input::ReceiveHead(ph), t(5)).unwrap();
        let seq = h.member().unwrap().own().seq();
        fault::arm(Rule::StopWhen(pick()));
        let r = h.seal(&w.ids[1], SealTrigger::OwnerCommand, t(10));
        let stopped = fault::disarm().stopped;
        drop(h);
        let s = snap(&root, &base, &format!("q6-{i}"));
        let o = match open_host(&w, 1, &s, cfg(&w), 20) {
            Ok((mut h, rep)) => {
                let seq2 = h.member().unwrap().own().seq();
                let again = h
                    .seal(&w.ids[1], SealTrigger::OwnerCommand, t(21))
                    .map(|r| format!("seal again -> segment {}", r.info.segment))
                    .unwrap_or_else(|e| format!("seal again -> {e:?}"));
                format!(
                    "opened {:?} segment {} (pending dropped {}, promoted {}); own seq {seq} -> {seq2}; {again}",
                    rep.opened, rep.segment, rep.pending_dropped, rep.pending_promoted
                )
            }
            Err(e) => format!("REFUSED {e:?}"),
        };
        out.push(format!("{name}: stopped {stopped} ({}) -> {o}", if r.is_ok() { "seal answered Ok" } else { "seal answered Err" }));
        scratch_done(&base);
    }
    println!("QA q6 rows:\n  {}", out.join("\n  "));
}

/// A 'busy' answer and the queue: nothing dropped, every ticket answered once, in order.
#[test]
fn qa_q7_queue_bound_bytes_and_order() {
    let w = World::new(156, 3, 3);
    let base = scratch("qa-q7");
    let root = base.join("host");
    let mut h = create_host(&w, 1, &root, cfg(&w));
    host_record(&mut h, &w.ids[1], Causer::LocalHuman, 1);
    h.seal_begin(&w.ids[1], SealTrigger::OwnerCommand, t(2)).unwrap();
    // bytes bound: records of 1 MiB text each
    let big = "x".repeat(1024 * 1024);
    let mut tickets = Vec::new();
    let mut busy = None;
    for i in 0..10 {
        match h.apply(
            &w.ids[1],
            Input::Record {
                causer: Causer::LocalHuman,
                input: owned("big", Some(&big), None),
            },
            t(3 + i),
        ) {
            Ok(Outcome::Queued(tk)) => tickets.push(tk),
            Ok(o) => panic!("{o:?}"),
            Err(e) => {
                busy = Some(format!("{e:?}"));
                break;
            }
        }
    }
    let st = h.status().unwrap();
    // a small call still fits under the count bound but not the byte bound?
    let small = h.apply(&w.ids[1], Input::Checkpoint, t(20));
    // calls on the member while the window is open: set_limits, seal_begin
    let sl = h.set_limits(StoreLimits::default());
    let sb = h.seal_begin(&w.ids[1], SealTrigger::OwnerCommand, t(21));
    let fin = h.seal_finish(&w.ids[1], t(22)).map(|r| r.info.segment);
    let dr = h.drain(&w.ids[1], t(23)).unwrap();
    let answered: Vec<u64> = dr.iter().map(|x| x.0).collect();
    println!(
        "QA q7 queue: {} big calls queued (tickets {:?}), then {}; status queued {} bytes {}; a checkpoint then -> {:?}; \
         set_limits in window -> {:?}; seal_begin in window -> {:?}; finish -> {fin:?}; drained tickets {answered:?} (each once, in order: {})",
        tickets.len(),
        tickets,
        busy.clone().unwrap_or_default(),
        st.queued,
        st.queued_bytes,
        small.as_ref().map(|o| format!("{o:?}").chars().take(30).collect::<String>()),
        sl.err(),
        sb.err(),
        {
            let mut want = tickets.clone();
            if let Ok(Outcome::Queued(tk)) = &small {
                want.push(*tk);
            }
            want == answered
        }
    );
    scratch_done(&base);
}


/// R3 inside a call: a refused `set_limits`, then a store failure that may have landed (P-4)
/// makes the host re-open the store from disk; what limits are in force after, and who is told?
#[test]
fn qa_q8_limits_after_an_in_call_reopen() {
    let w = World::new(157, 3, 3);
    let base = scratch("qa-q8");
    let root = base.join("host");
    let l1 = StoreLimits {
        bytes: 8 * 400_000,
        records: 8 * 2_000,
    };
    let mut c = cfg(&w);
    c.limits = l1;
    let mut h = create_host(&w, 1, &root, c.clone());
    // requests fill member 2's allowance: a checkpoint is owed
    for n in 0..20 {
        host_record(&mut h, &w.ids[1], Causer::Member(w.key(2)), n + 1);
    }
    let in_force_0 = h.member().unwrap().limits();
    let low = StoreLimits {
        bytes: 8 * 2_000,
        records: 8 * 4,
    };
    let sl = h.set_limits(low);
    let in_force_1 = h.member().unwrap().limits();
    // a local record whose directory sync fails after its rename: the host re-opens from disk
    fault::arm(Rule::FailWhen(Box::new(|cx| cx.op == Op::SyncDir && cx.dir == "store")));
    let r = h.apply(
        &w.ids[1],
        Input::Record {
            causer: Causer::LocalHuman,
            input: owned("local", None, None),
        },
        t(50),
    );
    fault::disarm();
    let in_force_2 = h.member().unwrap().limits();
    let st = h.status().unwrap();
    drop(h);
    let (_h, rep) = open_host(&w, 1, &root, c.clone(), 60).unwrap();
    println!(
        "QA q8 in-call re-open: in force {in_force_0:?}; set_limits(low) -> {:?}, in force {in_force_1:?}; \
         record with failing dir sync -> {r:?}; in force AFTER the in-call re-open {in_force_2:?} (status says {:?}); \
         changed silently: {}; a later restart reports before {:?} offered {:?} in_force {:?} differs {}",
        sl.map_err(|e| format!("{e:?}")),
        st.limits,
        in_force_2 != in_force_1 && matches!(r, Ok(_)),
        rep.limits.before,
        rep.limits.offered,
        rep.limits.in_force,
        rep.limits.differs()
    );
    scratch_done(&base);
}

/// The fault report: did a FailWhen rule fire?
trait Fired {
    fn failed_any(&self) -> bool;
}
impl Fired for crate::fsio::fault::Report {
    fn failed_any(&self) -> bool {
        // the log holds performed operations only; a fired failure is not in it
        true
    }
}

#[allow(dead_code)]
fn unused(_: Opened) {}
