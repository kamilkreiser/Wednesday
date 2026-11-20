//! QA-AUDIT-HOST (independent check): can anything a PEER does make an owner-side trigger due?
//! R5: "Nothing that carries a peer's key, a peer's seat, a requested allowance or a received
//! message can produce one." Written by the checker.
#![cfg(unix)]

mod common;

use coagent_audit::session::StoreLimits;
use coagent_audit::tiers::ShareLevel;
use coagent_audit_host::{Causer, HostError, Input, Outcome, Percent, SealTrigger};
use common::*;

/// V (member 1) with the own-SEAT trigger on at `pct`; member 2 asks V to record events
/// (`record_for`, charged to member 2's requested allowance) until V refuses. Nothing local happens.
fn requests_until_full(pct: u8, limits: Option<StoreLimits>) -> (usize, Option<SealTrigger>, String) {
    let w = World::new(70, 4, 4);
    let base = scratch("qa-trig");
    let root = base.join("host");
    let mut c = cfg(&w);
    c.settings.own_seat_at = Some(Percent::new(pct).unwrap());
    if let Some(l) = limits {
        c.limits = l;
    }
    let mut h = create_host(&w, 1, &root, c);
    let v = &w.ids[1];
    let before_due = h.due(t(1));
    let free0 = h.member().unwrap().free_usage();
    let mut n = 0usize;
    let mut first_due_at = None;
    for i in 0..100_000u64 {
        let r = h.apply(
            v,
            Input::Record {
                causer: Causer::Member(w.key(2)),
                input: owned("req", None, None),
            },
            t(2 + i),
        );
        match r {
            Ok(Outcome::Recorded(_)) => n += 1,
            Ok(o) => panic!("{o:?}"),
            Err(_) => break,
        }
        if first_due_at.is_none() && h.due(t(2 + i)).is_some() {
            first_due_at = Some(n);
        }
    }
    let m = h.member().unwrap();
    let free1 = m.free_usage();
    let own = m.status().own_slot;
    let seat = m.seat_usage(own);
    let lim = m.limits();
    let (req_used, allow) = (m.requested_usage(2), lim.requested_allowance());
    let due = h.due(t(200_000));
    // and the seal the trigger admits: does the host accept OwnSeatAt now?
    let sealed = h
        .seal(v, SealTrigger::OwnSeatAt(Percent::new(pct).unwrap()), t(200_001))
        .map(|r| format!("SEALED segment {} files {:?}", r.info.segment, r.files))
        .unwrap_or_else(|e| format!("refused {e:?}"));
    let line = format!(
        "own_seat_at={pct}%: before any request due={before_due:?}; {n} requests by member 2 accepted \
         (first due after {first_due_at:?}); free part {free0:?} -> {free1:?} (unchanged: {}); own seat used {seat:?} of {:?}; \
         requested_usage(slot 2) {:?} of allowance {:?}; due() = {due:?}; seal(OwnSeatAt) -> {sealed}",
        free0 == free1,
        lim.own_reserved(),
        req_used,
        allow,
    );
    drop(h);
    scratch_done(&base);
    (n, due, line)
}

#[test]
fn qa_t1_requested_allowance_drives_the_own_seat_trigger() {
    let small = StoreLimits {
        bytes: 8 * 40_000,
        records: 8 * 400,
    };
    let mut lines = Vec::new();
    let mut driven = Vec::new();
    for (pct, lim) in [(1u8, None), (2, None), (5, Some(small)), (6, Some(small)), (7, Some(small)), (10, Some(small))] {
        let (_, due, line) = requests_until_full(pct, lim);
        lines.push(line);
        if due.is_some() {
            driven.push(pct);
        }
    }
    println!("QA t1 own seat trigger vs member requests:\n  {}", lines.join("\n  "));
    println!("QA t1 RESULT: thresholds made due by ONE member's requests alone: {driven:?}");
}

/// The free-part trigger: which peer-driven calls change V's free part?
#[test]
fn qa_t2_peer_actions_and_the_free_part() {
    let w = World::new(71, 4, 4);
    let base = scratch("qa-trig2");
    let root = base.join("host");
    let mut c = cfg(&w);
    c.policy = every(2); // automatic own checkpoints every 2 events
    c.settings.own_free_part_at = Some(Percent::new(1).unwrap());
    let mut h = create_host(&w, 1, &root, c);
    let v = &w.ids[1];
    let mut peer = mem_member(&w, 2);
    for j in 0..4 {
        if j != 2 {
            peer.set_share_level(w.key(j), ShareLevel::Full);
        }
    }
    h.apply(
        v,
        Input::SetShareLevel {
            member: w.key(2),
            level: ShareLevel::Full,
        },
        t(0),
    )
    .unwrap();
    let mut log = Vec::new();
    let mut f = h.member().unwrap().free_usage();
    log.push(format!("start free={f:?} due={:?}", h.due(t(1))));
    // peer events
    for i in 0..10u64 {
        let s = peer.record(&w.ids[2], bare("p"), t(10 + i)).unwrap();
        let e = peer
            .outgoing(s)
            .into_iter()
            .find(|(to, _)| *to == w.key(1))
            .unwrap()
            .1;
        h.apply(v, Input::Receive(e), t(10 + i)).unwrap();
    }
    let f2 = h.member().unwrap().free_usage();
    log.push(format!("after 10 peer events free={f2:?} (changed {})", f2 != f));
    f = f2;
    // peer checkpoint (V countersigns)
    let ph = peer.checkpoint_now(&w.ids[2], t(30)).unwrap();
    let _ = h.apply(v, Input::ReceiveHead(ph), t(30)).unwrap();
    let f2 = h.member().unwrap().free_usage();
    log.push(format!("after a peer checkpoint free={f2:?} (changed {})", f2 != f));
    f = f2;
    // member requests with automatic checkpoints every 2 events
    for i in 0..6u64 {
        h.apply(
            v,
            Input::Record {
                causer: Causer::Member(w.key(2)),
                input: owned("req", None, None),
            },
            t(40 + i),
        )
        .unwrap();
    }
    let m = h.member().unwrap();
    let f2 = m.free_usage();
    log.push(format!(
        "after 6 requests (auto checkpoints every 2) free={f2:?} (changed {}); own checkpoints {}; requested_usage(2)={:?}",
        f2 != f,
        m.own().checkpoints().len(),
        m.requested_usage(2)
    ));
    let due = h.due(t(100));
    log.push(format!("due() with own_free_part_at=1% = {due:?}"));
    println!("QA t2 free part vs peer actions: {}", log.join("; "));
    // a free-part trigger that is due only by peer actions would be a finding
    let reason = match &due {
        None => "not due".to_string(),
        Some(tr) => format!("DUE {tr:?}"),
    };
    println!("QA t2 RESULT: {reason}");
    drop(h);
    scratch_done(&base);
}

#[allow(dead_code)]
fn unused(_: HostError) {}
