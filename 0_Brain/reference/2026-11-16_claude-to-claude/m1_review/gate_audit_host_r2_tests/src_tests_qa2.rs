//! QA-AUDIT-HOST-R2 (the short re-check of the fix round, head 680d333): probes of my own that need
//! the crate's fault injector. Written by the re-checker; the shapes of `with_removed_peer` and of
//! the `qa_q8` limits case are copied from the first check's `src_tests_qa.rs`.
//! Each probe PRINTS its figures and ASSERTS the property of the re-check brief section 4/5.

use std::path::{Path, PathBuf};

use coagent_audit::session::StoreLimits;

use super::common::*;
use super::copy_tree;
use crate::fsio::fault::{self, Op, Rule};
use crate::{AuditHost, Causer, HostConfig, HostError, Input, Outcome, SealTrigger};

fn snap(root: &Path, base: &Path, tag: &str) -> PathBuf {
    let s = base.join(format!("snap-{tag}"));
    copy_tree(root, &s);
    s
}

fn pending(root: &Path) -> bool {
    root.join("anchors").join("pending").exists()
}

fn open_desc(w: &World, s: &Path, c: HostConfig, now: u64) -> (bool, String) {
    match open_host(w, 1, s, c, now) {
        Ok((h, r)) => (
            true,
            format!(
                "OPENED {:?} own seq {} limits before {:?} in force {:?}",
                r.opened,
                h.member().unwrap().own().seq(),
                r.limits.before,
                r.limits.in_force
            ),
        ),
        Err(e) => (false, format!("REFUSED {e:?}")),
    }
}

/// Remove the newest own (local) record file from a snapshot: a loss the anchors must detect.
fn lose_record(s: &Path, base: &Path, n: u64, tag: &str) -> usize {
    let mut k = 0;
    for e in std::fs::read_dir(s.join("store")).unwrap() {
        let name = e.unwrap().file_name().into_string().unwrap();
        if name.contains(".N00.") && name.ends_with(&format!("{n:020}")) {
            std::fs::rename(s.join("store").join(&name), base.join(format!("lost-{tag}"))).unwrap();
            k += 1;
        }
    }
    k
}

fn peer_event(w: &World, p: &mut coagent_audit::session::SessionAudit<coagent_audit::store::MemStore>, i: usize, now: u64) -> coagent_audit::chain::AuditEvent {
    let s = p.record(&w.ids[i], bare("p"), t(now)).unwrap();
    p.outgoing(s)
        .into_iter()
        .find(|(to, _)| *to == w.key(1))
        .unwrap()
        .1
}

/// V=1 with 3 own records and peer 3's three events stored; peer 3 then removed (copied shape).
fn with_removed_peer(b: u8, name: &str, c: HostConfig) -> (World, PathBuf, PathBuf, AuditHost) {
    let mut w = World::new(b, 4, 4);
    let base = scratch(name);
    let root = base.join("host");
    let mut h = create_host(&w, 1, &root, c);
    let mut p3 = mem_member(&w, 3);
    for n in 0..3u64 {
        host_record(&mut h, &w.ids[1], Causer::LocalHuman, n + 1);
        let e = peer_event(&w, &mut p3, 3, n + 1);
        h.apply(&w.ids[1], Input::Receive(e), t(n + 1)).unwrap();
    }
    let r = w.remove(3);
    h.apply(&w.ids[1], Input::Roster(r), t(10)).unwrap();
    (w, base, root, h)
}

// ------------------------------------------------------------------------------------------------
// M-2 / m-1 variants
// ------------------------------------------------------------------------------------------------

/// The save of `current` fails TWICE: once inside the release, once at the next change (which must
/// be refused, AnchorNotSaved); then a restart with default settings must open, nothing lost.
#[test]
fn qa2_m2_release_save_fails_twice_then_restart() {
    let (w, base, root, mut h) = with_removed_peer(181, "qa2-m2twice", cfg(&World::new(181, 4, 4)));
    let seq0 = h.member().unwrap().own().seq();
    fault::arm(Rule::FailEvery(Box::new(|c| {
        c.op == Op::CreateTemp && c.dir == "anchors" && c.name == "current"
    })));
    let rel = h.apply(&w.ids[1], Input::Release(w.key(3)), t(20));
    let next = h.apply(
        &w.ids[1],
        Input::Record {
            causer: Causer::LocalHuman,
            input: owned("x", None, None),
        },
        t(21),
    );
    fault::disarm();
    let seq1 = h.member().unwrap().own().seq();
    let pend = pending(&root);
    let s = snap(&root, &base, "a");
    let (ok, d) = open_desc(&w, &s, cfg(&w), 30);
    // the running host: the save works again, the next change goes through and pending goes
    let after = host_record(&mut h, &w.ids[1], Causer::LocalHuman, 31);
    let pend2 = pending(&root);
    println!(
        "QA2 m2-twice: release {} ; next change {next:?}; own seq {seq0} -> {seq1}; pending on disk {pend}; \
         RESTART -> {d}; running host next record {after}, pending after it {pend2}",
        match &rel { Ok(o) => format!("Ok({})", if matches!(o, Outcome::Released(_)) { "Released" } else { "?" }), Err(e) => format!("Err({e:?})") }
    );
    assert!(matches!(rel, Ok(Outcome::Released(_))));
    assert!(matches!(next, Err(HostError::AnchorNotSaved)), "{next:?}");
    assert_eq!(seq1, seq0);
    assert!(pend, "pending must stay while current is unsaved");
    assert!(ok, "M-2: restart after two failed saves refused: {d}");
    assert!(!pend2, "pending must go after the next successful save");
    scratch_done(&base);
}

/// The first two anchor writes of a release fail (its pending anchor, then current): the release
/// must stop before deleting anything, and a restart opens with every record.
#[test]
fn qa2_m2_release_pending_write_fails() {
    let (w, base, root, mut h) = with_removed_peer(182, "qa2-m2pend", cfg(&World::new(182, 4, 4)));
    let mut k = 0;
    fault::arm(Rule::FailEvery(Box::new(move |c| {
        if c.op == Op::CreateTemp && c.dir == "anchors" {
            k += 1;
            return k <= 2;
        }
        false
    })));
    let rel = h.apply(&w.ids[1], Input::Release(w.key(3)), t(20));
    fault::disarm();
    let held = h.member().unwrap().usage_of(coagent_audit::session::Payer::Peer(w.key(3)));
    let pend = pending(&root);
    let s = snap(&root, &base, "a");
    let (ok, d) = open_desc(&w, &s, cfg(&w), 30);
    let again = h.apply(&w.ids[1], Input::Release(w.key(3)), t(31));
    println!(
        "QA2 m2-pending-write: release {:?}; peer 3 still charged {held:?}; pending on disk {pend}; RESTART -> {d}; \
         release again -> {}",
        rel.as_ref().map(|_| "Released"),
        match &again { Ok(_) => "Released".to_string(), Err(e) => format!("{e:?}") }
    );
    assert!(rel.is_err());
    assert!(held.1 > 0, "nothing may be deleted when the pending write fails");
    assert!(ok, "{d}");
    assert!(matches!(again, Ok(Outcome::Released(_))));
    assert!(!pending(&root));
    scratch_done(&base);
}

/// A release whose pending REMOVAL fails: pending stays (it equals current); a restart opens; the
/// next change's save removes it; a later loss of the newest record is then detected.
#[test]
fn qa2_m1_release_pending_removal_fails() {
    let (w, base, root, mut h) = with_removed_peer(183, "qa2-m1rm", cfg(&World::new(183, 4, 4)));
    fault::arm(Rule::FailEvery(Box::new(|c| {
        c.op == Op::Unlink && c.dir == "anchors" && c.name == "pending"
    })));
    let rel = h.apply(&w.ids[1], Input::Release(w.key(3)), t(20));
    fault::disarm();
    let pend = pending(&root);
    let s1 = snap(&root, &base, "a");
    let (ok1, d1) = open_desc(&w, &s1, cfg(&w), 30);
    let mut last = 0;
    for n in 0..3 {
        last = host_record(&mut h, &w.ids[1], Causer::LocalHuman, 40 + n);
    }
    let pend2 = pending(&root);
    drop(h);
    let s2 = snap(&root, &base, "b");
    let lost = lose_record(&s2, &base, last, "b");
    let (ok2, d2) = open_desc(&w, &s2, cfg(&w), 50);
    println!(
        "QA2 m1-release-removal-fails: release {:?}; pending after it {pend}; RESTART -> {d1}; \
         after 3 records pending {pend2}; newest record {last} removed ({lost} file); RESTART -> {d2}",
        rel.as_ref().map(|_| "Released")
    );
    assert!(matches!(rel, Ok(Outcome::Released(_))));
    assert!(pend);
    assert!(ok1, "{d1}");
    assert!(!pend2, "m-1: the next saves did not remove the leftover pending");
    assert_eq!(lost, 1);
    assert!(!ok2, "m-1: a loss was masked: {d2}");
    scratch_done(&base);
}

/// A seal whose step-4 save fails, then a release (of a peer that sent events after the seal):
/// the release's own save removes the stale pending first; restart opens; a loss is detected.
/// Variant (b): the release's ensure_anchor save fails too: the release is refused, nothing done,
/// and a restart opens on the post-seal pending anchor.
#[test]
fn qa2_m1_seal_step4_fails_then_release() {
    for variant in ["a", "b"] {
        let mut w = World::new(184, 4, 4);
        let base = scratch(&format!("qa2-s4rel-{variant}"));
        let root = base.join("host");
        let mut h = create_host(&w, 1, &root, cfg(&w));
        let mut p3 = mem_member(&w, 3);
        for n in 0..3 {
            host_record(&mut h, &w.ids[1], Causer::LocalHuman, n + 1);
        }
        let mut seen = false;
        fault::arm(Rule::FailWhen(Box::new(move |c| {
            if c.dir == "store" && c.name.contains(".F07.") {
                seen = true;
            }
            seen && c.op == Op::CreateTemp && c.dir == "anchors" && c.name == "current"
        })));
        let sealed = h.seal(&w.ids[1], SealTrigger::OwnerCommand, t(10)).map(|r| r.info.segment);
        fault::disarm();
        let pend_after_seal = pending(&root);
        for n in 0..2u64 {
            let e = peer_event(&w, &mut p3, 3, 11 + n);
            // the first change after the failed promotion: in (b) arm the save to fail on it
            if variant == "b" && n == 0 {
                // nothing: the Receive itself is a change; keep (b) for the release below
            }
            let r = h.apply(&w.ids[1], Input::Receive(e), t(11 + n));
            assert!(r.is_ok(), "{r:?}");
        }
        let pend_after_receive = pending(&root);
        let r = w.remove(3);
        h.apply(&w.ids[1], Input::Roster(r), t(15)).unwrap();
        if variant == "b" {
            // make the anchor dirty: a record whose save fails, then the release (its
            // ensure_anchor fails too)
            fault::arm(Rule::FailEvery(Box::new(|c| {
                c.op == Op::CreateTemp && c.dir == "anchors" && c.name == "current"
            })));
            let r1 = h.apply(
                &w.ids[1],
                Input::Record {
                    causer: Causer::LocalHuman,
                    input: owned("x", None, None),
                },
                t(16),
            );
            let rel = h.apply(&w.ids[1], Input::Release(w.key(3)), t(17));
            fault::disarm();
            let held = h.member().unwrap().usage_of(coagent_audit::session::Payer::Peer(w.key(3)));
            let s = snap(&root, &base, "b");
            let (ok, d) = open_desc(&w, &s, cfg(&w), 30);
            println!(
                "QA2 seal-step4 then release (b): seal {sealed:?}; pending after seal {pend_after_seal}, after receives \
                 {pend_after_receive}; record with failing save {r1:?}; release {:?}; peer 3 still charged {held:?}; RESTART -> {d}",
                rel.as_ref().map(|_| "Released")
            );
            assert!(matches!(rel, Err(HostError::AnchorNotSaved)), "{rel:?}");
            assert!(held.1 > 0);
            assert!(ok, "{d}");
        } else {
            let rel = h.apply(&w.ids[1], Input::Release(w.key(3)), t(17));
            let pend_after_release = pending(&root);
            let last = host_record(&mut h, &w.ids[1], Causer::LocalHuman, 18);
            drop(h);
            let s = snap(&root, &base, "a");
            let (ok, d) = open_desc(&w, &s, cfg(&w), 30);
            let s2 = snap(&root, &base, "a2");
            let lost = lose_record(&s2, &base, last, "a2");
            let (ok2, d2) = open_desc(&w, &s2, cfg(&w), 31);
            println!(
                "QA2 seal-step4 then release (a): seal {sealed:?}; pending after seal {pend_after_seal}, after receives \
                 {pend_after_receive}; release {:?}; pending after release {pend_after_release}; RESTART -> {d}; newest \
                 record {last} removed ({lost}) RESTART -> {d2}",
                rel.as_ref().map(|_| "Released")
            );
            assert_eq!(sealed, Ok(1));
            assert!(pend_after_seal && !pend_after_receive);
            assert!(matches!(rel, Ok(Outcome::Released(_))));
            assert!(!pend_after_release);
            assert!(ok, "{d}");
            assert!(!ok2, "a loss was masked: {d2}");
        }
        scratch_done(&base);
    }
}

// ------------------------------------------------------------------------------------------------
// M-3: a refused set_limits, then each in-call re-open, then a restart
// ------------------------------------------------------------------------------------------------

fn tiny_rec(h: &mut AuditHost, v: &coagent_crypto::identity::DeviceIdentity, causer: Causer, now: u64) {
    let r = h.apply(
        v,
        Input::Record {
            causer,
            input: owned("x", None, None),
        },
        t(now),
    );
    assert!(matches!(r, Ok(Outcome::Recorded(_))), "setup record: {r:?}");
}

fn l1() -> StoreLimits {
    StoreLimits {
        bytes: 8 * 400_000,
        records: 8 * 2_000,
    }
}

/// A host whose limits l1 are in force, member 2's requests stored (a checkpoint owed), a LOWER
/// offer refused; peer 3's events stored and peer 3 removed (for the release case).
fn refused_offer(b: u8, name: &str) -> (World, PathBuf, PathBuf, AuditHost, HostConfig) {
    let w0 = World::new(b, 4, 4);
    let mut c = cfg(&w0);
    c.limits = l1();
    let (w, base, root, mut h) = with_removed_peer(b, name, c.clone());
    for n in 0..20 {
        host_record(&mut h, &w.ids[1], Causer::Member(w.key(2)), 100 + n);
    }
    let low = StoreLimits {
        bytes: 8 * 2_000,
        records: 8 * 4,
    };
    let sl = h.set_limits(low);
    assert!(sl.is_err(), "setup: the lower offer must be refused: {sl:?}");
    (w, base, root, h, c)
}

#[test]
fn qa2_m3_each_in_call_reopen_after_a_refused_offer() {
    let mut lines = Vec::new();
    for case in ["p4-record", "p4-receive", "p7-seal", "release-fails"] {
        let (w, base, root, mut h, c) = refused_offer(185, &format!("qa2-m3-{case}"));
        let before = h.member().unwrap().limits();
        let ans: String;
        let changed_said: bool;
        match case {
            "p4-record" => {
                fault::arm(Rule::FailWhen(Box::new(|x| x.op == Op::SyncDir && x.dir == "store")));
                let r = h.apply(
                    &w.ids[1],
                    Input::Record {
                        causer: Causer::LocalHuman,
                        input: owned("local", None, None),
                    },
                    t(200),
                );
                fault::disarm();
                changed_said = matches!(r, Err(HostError::LimitsChanged { .. }));
                ans = format!("{r:?}");
            }
            "p4-receive" => {
                let mut p0 = mem_member(&w, 0);
                let e = peer_event(&w, &mut p0, 0, 200);
                fault::arm(Rule::FailWhen(Box::new(|x| x.op == Op::SyncDir && x.dir == "store")));
                let r = h.apply(&w.ids[1], Input::Receive(e), t(200));
                fault::disarm();
                changed_said = matches!(r, Err(HostError::LimitsChanged { .. }));
                ans = format!("{r:?}");
            }
            "p7-seal" => {
                fault::arm(Rule::FailWhen(Box::new(|x| {
                    x.op == Op::SyncDir && x.dir == "store" && x.name.contains(".F07.")
                })));
                let r = h.seal(&w.ids[1], SealTrigger::OwnerCommand, t(200));
                fault::disarm();
                changed_said = matches!(r, Err(HostError::LimitsChanged { .. }));
                ans = format!("{:?}", r.map(|x| x.info.segment));
            }
            _ => {
                let mut armed_store = false;
                fault::arm(Rule::FailWhen(Box::new(move |x| {
                    // the first store directory sync of the release: inside archive_and_release
                    if x.dir == "store" && x.op == Op::Unlink {
                        armed_store = true;
                    }
                    armed_store && x.op == Op::SyncDir && x.dir == "store"
                })));
                let r = h.apply(&w.ids[1], Input::Release(w.key(3)), t(200));
                fault::disarm();
                changed_said = matches!(r, Err(HostError::LimitsChanged { .. }));
                ans = match &r {
                    Ok(_) => "Ok(Released)".into(),
                    Err(e) => format!("Err({e:?})"),
                };
            }
        }
        let after = h.member().unwrap().limits();
        let _status = h.status().unwrap();
        drop(h);
        let s = snap(&root, &base, case);
        let rep = open_host(&w, 1, &s, c.clone(), 300).map(|(_, r)| r);
        let (ok, rep_before, rep_in_force, rep_differs) = match &rep {
            Ok(r) => (true, r.limits.before, Some(r.limits.in_force), r.limits.differs()),
            Err(_) => (false, None, None, false),
        };
        lines.push(format!(
            "{case}: before {:?}; answer {}; after {:?}; said {changed_said}; RESTART ok {ok} \
             anchors/limits (report.before) {:?} in force {:?} differs {rep_differs}",
            (before.bytes, before.records),
            &ans[..ans.len().min(220)],
            (after.bytes, after.records),
            rep_before.map(|l| (l.bytes, l.records)),
            rep_in_force.map(|l| (l.bytes, l.records)),
        ));
        assert!(after == before || changed_said, "M-3 {case}: silent change");
        assert!(ok, "M-3 {case}: restart refused {rep:?}");
        assert_eq!(rep_before, Some(after), "M-3 {case}: anchors/limits is not the limits in force");
        assert!(!rep_differs, "M-3 {case}: restart limits differ");
        scratch_done(&base);
    }
    println!("QA2 M-3 in-call re-opens after a refused offer:\n  {}", lines.join("\n  "));
}

/// The ONLY state in which the audit crate refuses the limits in force again (gate r5 N1's state:
/// a checkpoint owed, and an earlier occupant's records in this member's re-used slot), reached
/// THROUGH THE HOST, with a P-4 re-open inside a call: the limits after the re-open differ, so the
/// answer must be LimitsChanged. Then: what does each kind of call answer in that state when its
/// put's directory sync fails? (Does any landed own record or checkpoint come back inside an Err?)
/// Shape copied from coagent-audit tests/fix_qam1_seat.rs `qam1_exception_after_resume_in_n1s_state`.
#[test]
fn qa2_m3_n1_state_reopen_differs_end_to_end() {
    let mut w = World::new(0xC8, 6, 5);
    let base = scratch("qa2-m3-n1");
    let root = base.join("host");
    let l = StoreLimits {
        bytes: 8 * 16 * 1024,
        records: 8 * 64,
    };
    let mut c = HostConfig::new(w.s, every(1_000_000));
    c.limits = l;
    let mut h = create_host(&w, 1, &root, c.clone());
    let v = fixed_identity(0xC8 + 1);
    let big = "r".repeat(400);
    for i in 0..4u64 {
        h.apply(
            &v,
            Input::Record {
                causer: Causer::LocalHuman,
                input: owned("x", Some(&big), None),
            },
            t(i),
        )
        .unwrap();
    }
    h.apply(&v, Input::Checkpoint, t(7)).unwrap();
    for i in 0..3u64 {
        tiny_rec(&mut h, &v, Causer::LocalHuman, 10 + i);
    }
    // X (slot 2) fills its seat at V
    let mut x = mem_member(&w, 2);
    let s3 = "s".repeat(3_000);
    for i in 1..4u64 {
        let n = x
            .record(
                &w.ids[2],
                coagent_audit::chain::EventInput {
                    kind: "x",
                    summary: Some(&s3),
                    full: None,
                },
                t(20 + i),
            )
            .unwrap();
        let e = x
            .outgoing(n)
            .into_iter()
            .find(|(to, _)| *to == w.key(1))
            .unwrap()
            .1;
        h.apply(&v, Input::Receive(e), t(20 + i)).unwrap();
    }
    // H (slot 3) asks once: a checkpoint is owed
    tiny_rec(&mut h, &v, Causer::Member(w.key(3)), 25);
    let r_rm2 = w.remove(2);
    let r_rmv = w.remove(1);
    let r_add = w.add(1, 2);
    h.apply(&v, Input::Roster(r_rm2), t(26)).unwrap();
    h.apply(&v, Input::Roster(r_rmv), t(27)).unwrap();
    let before = h.member().unwrap().limits();
    // the roster version that puts V into X's old slot, its put's directory sync failing (P-4)
    fault::arm(Rule::FailWhen(Box::new(|x| x.op == Op::SyncDir && x.dir == "store")));
    let r = h.apply(&v, Input::Roster(r_add), t(28));
    fault::disarm();
    let after = h.member().unwrap().limits();
    let m = h.member().unwrap();
    let seat = m.seat_usage(m.status().own_slot);
    let mut lines = vec![format!(
        "roster add with P-4: before {:?}; answer {}; after {:?}; own slot {} seat {seat:?}",
        (before.bytes, before.records),
        match &r {
            Err(HostError::LimitsChanged { limits, answer }) => format!(
                "LimitsChanged {{ before {:?} offered {:?} in_force {:?} refused {:?}, answer {:?} }}",
                limits.before.map(|l| (l.bytes, l.records)),
                (limits.offered.bytes, limits.offered.records),
                (limits.in_force.bytes, limits.in_force.records),
                limits.refused,
                answer
            ),
            o => format!("{o:?}"),
        },
        (after.bytes, after.records),
        m.status().own_slot
    )];
    let said = matches!(r, Err(HostError::LimitsChanged { .. }));
    assert!(after == before || said, "M-3 (N1): silent change {before:?} -> {after:?}: {r:?}");
    // restart: anchors/limits holds what is in force
    let s = snap(&root, &base, "n1");
    let rep = open_host(&w, 1, &s, c.clone(), 40).map(|(_, r)| r);
    lines.push(format!(
        "restart: {}",
        match &rep {
            Ok(r) => format!(
                "opened {:?} before {:?} offered {:?} in force {:?} refused {:?} differs {}",
                r.opened,
                r.limits.before.map(|l| (l.bytes, l.records)),
                (r.limits.offered.bytes, r.limits.offered.records),
                (r.limits.in_force.bytes, r.limits.in_force.records),
                r.limits.refused,
                r.limits.differs()
            ),
            Err(e) => format!("REFUSED {e:?}"),
        }
    ));
    if let Ok(rp) = &rep {
        assert_eq!(rp.limits.before, Some(after), "anchors/limits is not the limits in force");
    }
    println!("QA2 M-3 N1 state through the host:\n  {}", lines.join("\n  "));
    scratch_done(&base);
}

/// In N1's state with the limits l in force (no re-open yet), each kind of own call whose put's
/// directory sync fails: is any landed own record or checkpoint answered inside LimitsChanged?
#[test]
fn qa2_m3_n1_state_each_own_call_with_p4() {
    let mut out = Vec::new();
    for kind in ["local", "request-h", "request-g", "checkpoint"] {
        let mut w = World::new(0xC8, 6, 6);
        let base = scratch(&format!("qa2-m3-n1b-{kind}"));
        let root = base.join("host");
        let l = StoreLimits {
            bytes: 8 * 16 * 1024,
            records: 8 * 64,
        };
        let mut c = HostConfig::new(w.s, every(1_000_000));
        c.limits = l;
        let mut h = create_host(&w, 1, &root, c.clone());
        let v = fixed_identity(0xC8 + 1);
        let big = "r".repeat(400);
        for i in 0..4u64 {
            h.apply(
                &v,
                Input::Record {
                    causer: Causer::LocalHuman,
                    input: owned("x", Some(&big), None),
                },
                t(i),
            )
            .unwrap();
        }
        h.apply(&v, Input::Checkpoint, t(7)).unwrap();
        let mut x = mem_member(&w, 2);
        let s3 = "s".repeat(3_000);
        for i in 1..4u64 {
            let n = x
                .record(
                    &w.ids[2],
                    coagent_audit::chain::EventInput {
                        kind: "x",
                        summary: Some(&s3),
                        full: None,
                    },
                    t(20 + i),
                )
                .unwrap();
            let e = x
                .outgoing(n)
                .into_iter()
                .find(|(to, _)| *to == w.key(1))
                .unwrap()
                .1;
            h.apply(&v, Input::Receive(e), t(20 + i)).unwrap();
        }
        tiny_rec(&mut h, &v, Causer::Member(w.key(3)), 25);
        for r in [w.remove(2), w.remove(1), w.add(1, 2)] {
            h.apply(&v, Input::Roster(r), t(26)).unwrap();
        }
        let seq0 = h.member().unwrap().own().seq();
        let before = h.member().unwrap().limits();
        let input = match kind {
            "local" => Input::Record {
                causer: Causer::LocalHuman,
                input: owned("y", None, None),
            },
            "request-h" => Input::Record {
                causer: Causer::Member(w.key(3)),
                input: owned("y", None, None),
            },
            "request-g" => Input::Record {
                causer: Causer::Member(w.key(4)),
                input: owned("y", None, None),
            },
            _ => Input::Checkpoint,
        };
        fault::arm(Rule::FailWhen(Box::new(|x| x.op == Op::SyncDir && x.dir == "store")));
        let r = h.apply(&v, input, t(30));
        let rep = fault::disarm();
        let seq1 = h.member().unwrap().own().seq();
        let after = h.member().unwrap().limits();
        let reached_put = rep.log.iter().any(|(op, d, _)| *op == Op::Rename && d == "store");
        let wrapped_ok = matches!(&r, Err(HostError::LimitsChanged { answer, .. }) if answer.is_ok());
        out.push(format!(
            "{kind}: put reached {reached_put}; answer {r:?}; own seq {seq0} -> {seq1}; limits {:?} -> {:?}; \
             landed own change inside an Err: {wrapped_ok}",
            (before.bytes, before.records),
            (after.bytes, after.records)
        ));
        drop(h);
        scratch_done(&base);
    }
    println!("QA2 M-3 N1 each own call with P-4:\n  {}", out.join("\n  "));
}

/// P-4 (a record's put lands, its directory sync fails), and inside the re-open a SECOND write of
/// the host fails: `anchors/limits` (reoffer_limits) or `anchors/current` (settle_pending). Does the
/// answer still say the record landed, or does an Err hide it (so a caller that retries on an Err
/// records the event twice)? Pre-existing shape (the same `?` in `reopen` at 35f7e89), measured at
/// the head.
#[test]
fn qa2_p4_then_a_second_write_fails_in_the_reopen() {
    let mut lines = Vec::new();
    for which in ["limits", "current"] {
        let w = World::new(187, 3, 3);
        let base = scratch(&format!("qa2-p4x-{which}"));
        let root = base.join("host");
        let mut h = create_host(&w, 1, &root, cfg(&w));
        for n in 0..3 {
            host_record(&mut h, &w.ids[1], Causer::LocalHuman, n + 1);
        }
        let seq0 = h.member().unwrap().own().seq();
        let mut store_failed = false;
        let mut other_failed = false;
        let target = which;
        fault::arm(Rule::FailEvery(Box::new(move |c| {
            if !store_failed && c.op == Op::SyncDir && c.dir == "store" {
                store_failed = true;
                return true;
            }
            if store_failed && !other_failed && c.op == Op::CreateTemp && c.dir == "anchors" && c.name == target {
                other_failed = true;
                return true;
            }
            false
        })));
        let r = h.apply(
            &w.ids[1],
            Input::Record {
                causer: Causer::LocalHuman,
                input: owned("act", Some("one human act"), None),
            },
            t(10),
        );
        fault::disarm();
        let closed = h.member().is_err();
        let seq1 = h.member().map(|m| m.own().seq()).unwrap_or(0);
        // a caller that treats an Err as "not done" offers the same act again
        let retry = if r.is_err() {
            Some(h.apply(
                &w.ids[1],
                Input::Record {
                    causer: Causer::LocalHuman,
                    input: owned("act", Some("one human act"), None),
                },
                t(11),
            ))
        } else {
            None
        };
        let seq2 = h.member().map(|m| m.own().seq()).unwrap_or(0);
        lines.push(format!(
            "{which}: answer {r:?}; host closed {closed}; own seq {seq0} -> {seq1} (landed {}); a retry on the Err -> {retry:?}; own seq then {seq2}",
            seq1 > seq0
        ));
        drop(h);
        scratch_done(&base);
    }
    println!("QA2 P-4 + second write failing inside the re-open:\n  {}", lines.join("\n  "));
}
