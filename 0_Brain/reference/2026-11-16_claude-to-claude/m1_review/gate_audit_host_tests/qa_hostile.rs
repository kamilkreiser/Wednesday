//! QA-AUDIT-HOST (independent check): a hostile peer cannot drive filing (R5, R6).
//! The peer fills its seat, sends inside every window (events, checkpoints, cross-check records,
//! floods to the queue's bound), sends a checkpoint at the worst times (just before step 0, inside
//! the window), and is removed (and released) in the middle of a seal. The owner's side seals by
//! command and by its timer. Written by the checker.
#![cfg(unix)]

mod common;

use std::collections::BTreeSet;

use coagent_audit::session::{SessionAudit, StoreLimits};
use coagent_audit::store::MemStore;
use coagent_audit::tiers::ShareLevel;
use coagent_audit_host::{
    AuditHost, HostError, Input, Outcome, Percent, SealTrigger, MAX_QUEUED_CALLS,
};
use common::*;

const V: usize = 1;
const X: usize = 2; // hostile

struct Hostile {
    m: SessionAudit<MemStore>,
}

impl Hostile {
    fn event(&mut self, w: &World, now: u64) -> Input {
        let s = self.m.record(&w.ids[X], bare("x.ev"), t(now)).unwrap();
        let e = self
            .m
            .outgoing(s)
            .into_iter()
            .find(|(to, _)| *to == w.key(V))
            .unwrap()
            .1;
        Input::Receive(e)
    }
    fn head(&mut self, w: &World, now: u64) -> Option<Input> {
        self.m
            .checkpoint_now(&w.ids[X], t(now))
            .ok()
            .map(Input::ReceiveHead)
    }
}

fn seats_full(h: &AuditHost, w: &World) -> bool {
    let m = h.member().unwrap();
    // World puts member i in roster slot i
    let slot = m.roster().member_keys().contains(&w.key(X)).then_some(X as u8);
    match slot {
        Some(s) => {
            let u = m.seat_usage(s);
            let l = m.limits().per_peer();
            u.0 * 100 >= l.0 * 90 || u.1 * 100 >= l.1 * 90
        }
        None => false,
    }
}

#[test]
fn qa_h1_hostile_peer_cannot_drive_filing() {
    let mut w = World::new(80, 5, 5);
    let base = scratch("qa-h1");
    let root = base.join("host");
    let mut c = cfg(&w);
    c.limits = StoreLimits {
        bytes: 8 * 20_000,
        records: 8 * 60,
    };
    c.settings.timer_ms = Some(5_000);
    // the own FREE-part trigger on too: peers must never move it
    c.settings.own_free_part_at = Some(Percent::new(30).unwrap());
    let mut h = create_host(&w, V, &root, c.clone());
    let v = fixed_identity(80 + V as u8);
    let mut x = Hostile { m: mem_member(&w, X) };
    for j in 0..5 {
        if j != X {
            x.m.set_share_level(w.key(j), ShareLevel::Full);
        }
    }
    let mut now = 1u64;
    let mut owner_plans = 0u64; // seal_begin successes + stale retries (files the owner side caused)
    let mut owner_seals = 0u64;
    let mut busy_seen = 0u64;
    let mut queued_total = 0u64;
    let mut max_queue = 0usize;
    let mut tickets_out: BTreeSet<u64> = BTreeSet::new();
    let mut tickets_back: Vec<u64> = Vec::new();
    let mut due_by_peer = 0u64;
    let mut seal_failures = Vec::new();
    let mut removed = false;
    let mut released = false;
    let mut full_hits = 0u64;
    for round in 0..12u64 {
        // the hostile peer fills its seat (events until refused), checking due() after each
        let mut refused_in_row = 0;
        for _ in 0..80 {
            if removed {
                break;
            }
            now += 1;
            let before = h.due(t(now));
            let inp = x.event(&w, now);
            let r = h.apply(&v, inp, t(now));
            if r.is_err() {
                refused_in_row += 1;
                if refused_in_row > 3 {
                    break;
                }
            }
            let after = h.due(t(now));
            if before.is_none() && after.is_some() && !matches!(after, Some(SealTrigger::Timer)) {
                due_by_peer += 1;
            }
        }
        if seats_full(&h, &w) {
            full_hits += 1;
        }
        // worst time 1: its checkpoint arrives just before step 0
        if !removed {
            if let Some(hd) = x.head(&w, now) {
                if let Ok(Outcome::Countersigned(cs)) = h.apply(&v, hd, t(now)) {
                    let _ = x.m.add_countersignature(&cs);
                }
            }
        }
        // an own event so the owner side has something to seal
        now += 1;
        host_record(&mut h, &v, coagent_audit_host::Causer::LocalHuman, now);
        // the owner side seals: command on even rounds, timer on odd rounds (after waiting)
        let trig = if round % 2 == 0 {
            SealTrigger::OwnerCommand
        } else {
            now += 6_000;
            SealTrigger::Timer
        };
        match h.seal_begin(&v, trig.clone(), t(now)) {
            Ok(_) => owner_plans += 1,
            Err(HostError::Audit(coagent_audit::AuditError::NothingToSeal)) => continue,
            Err(e) => panic!("round {round}: seal_begin {trig:?}: {e:?}"),
        }
        // INSIDE the window: the hostile peer floods (events, a checkpoint, more), the roster
        // removes it (round 6) and a release of it is asked for (round 6)
        let mut in_window: Vec<Input> = Vec::new();
        if !removed {
            for _ in 0..(MAX_QUEUED_CALLS + 40) {
                now += 1;
                in_window.push(x.event(&w, now));
            }
            if let Some(hd) = x.head(&w, now) {
                in_window.insert(5, hd);
            }
        }
        if round == 6 && !removed {
            let r = w.remove(X);
            in_window.insert(0, Input::Roster(r));
            in_window.insert(1, Input::Release(w.key(X)));
            removed = true;
        }
        for inp in in_window {
            match h.apply(&v, inp, t(now)) {
                Ok(Outcome::Queued(tk)) => {
                    queued_total += 1;
                    tickets_out.insert(tk);
                }
                Ok(o) => panic!("round {round}: a call reached the member in the window: {o:?}"),
                Err(HostError::Busy { .. }) => busy_seen += 1,
                Err(e) => panic!("round {round}: in window: {e:?}"),
            }
            max_queue = max_queue.max(h.status().unwrap().queued);
        }
        let st = h.status().unwrap();
        assert_eq!(st.mutations_in_window, 0);
        match h.seal_finish(&v, t(now)) {
            Ok(r) => {
                owner_seals += 1;
                owner_plans += u64::from(r.stale_retries);
            }
            Err(e) => seal_failures.push(format!("round {round}: {e:?}")),
        }
        let dr = h.drain(&v, t(now)).unwrap();
        for (tk, res) in &dr {
            tickets_back.push(*tk);
            if let Ok(Outcome::Released(_)) = res {
                released = true;
            }
        }
    }
    let st = h.status().unwrap();
    let files = h.archive_files().unwrap();
    let seg_files = files.iter().filter(|n| n.starts_with("seg-")).count() as u64;
    let back: BTreeSet<u64> = tickets_back.iter().copied().collect();
    println!(
        "QA h1 hostile peer: rounds 12; owner plans {owner_plans}, owner seals {owner_seals}; host seals {} plans {}; \
         segment files {seg_files}; release files {}; seal failures {seal_failures:?}; queued {queued_total}, busy {busy_seen}, \
         max queue {max_queue} (bound {MAX_QUEUED_CALLS}); tickets out {} back {} (dupes {}); due() made true by the peer {due_by_peer}; \
         hostile seat >=90% full in {full_hits} rounds; removed mid-seal {removed}, released after drain {released}",
        st.seals,
        st.plans,
        st.release_files,
        tickets_out.len(),
        tickets_back.len(),
        tickets_back.len() - back.len()
    );
    assert_eq!(seg_files, owner_plans, "segment files == owner plans");
    assert_eq!(st.seals, owner_seals);
    assert!(seal_failures.is_empty());
    assert!(max_queue <= MAX_QUEUED_CALLS);
    assert!(busy_seen > 0, "the bound was never reached");
    assert_eq!(tickets_out, back, "every queued call answered");
    assert_eq!(tickets_back.len(), back.len(), "no call answered twice");
    assert_eq!(due_by_peer, 0, "a peer's call made a trigger due");
    assert!(full_hits > 0, "the hostile seat never filled");
    assert!(removed && released);
    // archive + store verify together
    let mut set = h.segment_bundles().unwrap();
    set.push(h.export(&v).unwrap());
    let rep = coagent_audit::bundle::verify_segments(&set).unwrap();
    println!(
        "QA h1 verify_segments over {} files: ok, {} equivocations",
        set.len(),
        rep.equivocations.len()
    );
    drop(h);
    scratch_done(&base);
}
