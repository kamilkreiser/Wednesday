//! QA-AUDIT-HOST-R2 (re-check of the fix round, head 680d333): can anything a PEER does make an
//! owner-side trigger due, for EACH trigger setting (own seat, own free part, timer)? Written by the
//! re-checker. Three peer shapes: seven members all sending recording requests to the bound; a
//! member's PEER EVENTS (not requests) filling its seat; an earlier occupant's records in the own
//! slot (V removed and re-added into a slot whose seat holds another member's events).
#![cfg(unix)]

mod common;

use coagent_audit::chain::EventInput;
use coagent_audit_host::{AuditHost, Causer, HostConfig, Input, Outcome, Percent, SealTrigger};
use common::*;

const PCT: u8 = 1;
const TIMER_MS: u64 = 1_000_000_000_000;

fn all_triggers_on(w: &World) -> HostConfig {
    let mut c = cfg(w);
    c.settings.own_seat_at = Some(Percent::new(PCT).unwrap());
    c.settings.own_free_part_at = Some(Percent::new(PCT).unwrap());
    c.settings.timer_ms = Some(TIMER_MS);
    c
}

/// due() and an attempt of each trigger; returns (due, answers) and the measures.
fn probe(h: &mut AuditHost, v: &coagent_crypto::identity::DeviceIdentity, now: u64) -> (bool, String) {
    let due = h.due(t(now));
    let m = h.member().unwrap();
    let own = m.status().own_slot;
    let seat = m.seat_usage(own);
    let free = m.free_usage();
    let lim = m.limits();
    let mut ans = Vec::new();
    let mut sealed = false;
    for tr in [
        SealTrigger::OwnSeatAt(Percent::new(PCT).unwrap()),
        SealTrigger::OwnFreePartAt(Percent::new(PCT).unwrap()),
        SealTrigger::Timer,
    ] {
        let r = h.seal(v, tr.clone(), t(now));
        sealed |= r.is_ok();
        ans.push(format!(
            "{:?} -> {}",
            tr,
            r.map(|x| format!("SEALED {}", x.info.segment))
                .unwrap_or_else(|e| format!("{e:?}"))
        ));
    }
    let pct = |u: (usize, usize), l: (usize, usize)| {
        ((u.0 as u64 * 100) / l.0.max(1) as u64).max((u.1 as u64 * 100) / l.1.max(1) as u64)
    };
    (
        due.is_some() || sealed,
        format!(
            "due {due:?}; own slot {own}; seat_usage(own) {seat:?} = {}% of own_reserved {:?} (the OLD measure); \
             free_usage {free:?} = {}% (the NEW measure); attempts: {}",
            pct(seat, lim.own_reserved()),
            lim.own_reserved(),
            pct(free, lim.own_reserved()),
            ans.join("; ")
        ),
    )
}

#[test]
fn qa2_t1_seven_members_request_to_the_bound() {
    let w = World::new(90, 8, 8);
    let base = scratch("qa2-t1");
    let root = base.join("host");
    let mut h = create_host(&w, 1, &root, all_triggers_on(&w));
    let v = fixed_identity(90 + 1);
    let mut counts = Vec::new();
    let mut ever_due = false;
    let mut now = 10u64;
    for j in [0usize, 2, 3, 4, 5, 6, 7] {
        let mut n = 0;
        loop {
            now += 1;
            let r = h.apply(
                &v,
                Input::Record {
                    causer: Causer::Member(w.key(j)),
                    input: owned("req", None, None),
                },
                t(now),
            );
            match r {
                Ok(Outcome::Recorded(_)) => n += 1,
                _ => break,
            }
            if n % 64 == 0 && h.due(t(now)).is_some() {
                ever_due = true;
            }
        }
        counts.push((j, n));
        ever_due |= h.due(t(now)).is_some();
    }
    let (d, line) = probe(&mut h, &v, now + 1);
    println!("QA2 t1 seven members: requests accepted per member {counts:?}; due at any 64th request: {ever_due}; {line}");
    assert!(!ever_due && !d, "a peer made a trigger due or a seal happen: {line}");
    drop(h);
    scratch_done(&base);
}

#[test]
fn qa2_t2_peer_events_fill_a_seat() {
    let w = World::new(92, 4, 4);
    let base = scratch("qa2-t2");
    let root = base.join("host");
    let mut h = create_host(&w, 1, &root, all_triggers_on(&w));
    let v = fixed_identity(92 + 1);
    let mut p2 = mem_member(&w, 2);
    let s = "e".repeat(3_000);
    let mut n = 0;
    let mut last = String::new();
    for i in 0..10_000u64 {
        let seq = p2
            .record(
                &w.ids[2],
                EventInput {
                    kind: "p",
                    summary: Some(&s),
                    full: None,
                },
                t(10 + i),
            );
        let Ok(seq) = seq else { break };
        let e = p2
            .outgoing(seq)
            .into_iter()
            .find(|(to, _)| *to == w.key(1))
            .unwrap()
            .1;
        match h.apply(&v, Input::Receive(e), t(10 + i)) {
            Ok(_) => n += 1,
            Err(e) => {
                last = format!("{e:?}");
                break;
            }
        }
        assert!(h.due(t(10 + i)).is_none(), "due after peer event {n}");
    }
    let seat2 = h.member().unwrap().seat_usage(2);
    let lim = h.member().unwrap().limits().per_peer();
    let (d, line) = probe(&mut h, &v, 20_000);
    println!("QA2 t2 peer events: {n} accepted, then {last}; seat 2 {seat2:?} of {lim:?}; {line}");
    assert!(!d, "{line}");
    drop(h);
    scratch_done(&base);
}

#[test]
fn qa2_t3_earlier_occupant_in_the_own_slot() {
    let mut w = World::new(94, 6, 5);
    let base = scratch("qa2-t3");
    let root = base.join("host");
    let mut h = create_host(&w, 1, &root, all_triggers_on(&w));
    let v = fixed_identity(94 + 1);
    // X (slot 2) fills most of its seat at V
    let mut x = mem_member(&w, 2);
    let s = "o".repeat(3_000);
    let mut n = 0;
    for i in 0..10_000u64 {
        let seq = x
            .record(
                &w.ids[2],
                EventInput {
                    kind: "x",
                    summary: Some(&s),
                    full: None,
                },
                t(10 + i),
            );
        let Ok(seq) = seq else { break };
        let e = x
            .outgoing(seq)
            .into_iter()
            .find(|(to, _)| *to == w.key(1))
            .unwrap()
            .1;
        if h.apply(&v, Input::Receive(e), t(10 + i)).is_err() {
            break;
        }
        n += 1;
    }
    // V removed, then re-added into X's old slot (X removed): X's records now sit in V's own slot
    for r in [w.remove(2), w.remove(1), w.add(1, 2)] {
        h.apply(&v, Input::Roster(r), t(20_000)).unwrap();
    }
    let (d1, line1) = probe(&mut h, &v, 20_001);
    // and member 3 asks V to record until refused, in that state
    let mut q = 0;
    for i in 0..5_000u64 {
        match h.apply(
            &v,
            Input::Record {
                causer: Causer::Member(w.key(3)),
                input: owned("req", None, None),
            },
            t(20_010 + i),
        ) {
            Ok(Outcome::Recorded(_)) => q += 1,
            _ => break,
        }
    }
    let (d2, line2) = probe(&mut h, &v, 30_000);
    println!(
        "QA2 t3 earlier occupant: X's events received {n}; after the re-add into slot 2: {line1}\n  \
         then {q} requests by member 3: {line2}"
    );
    assert!(!d1 && !d2, "an earlier occupant's records or requests made a trigger due");
    drop(h);
    scratch_done(&base);
}

/// Roster changes are signed by the convener (another member): removing a requester, releasing it,
/// and a newcomer in its slot must not move any cost into the owner's free part (the own checkpoints
/// its allowance paid for stay paid there), so no trigger becomes due.
#[test]
fn qa2_t4_requester_removed_released_slot_reused() {
    let mut w = World::new(96, 5, 4);
    let base = scratch("qa2-t4");
    let root = base.join("host");
    let mut h = create_host(&w, 1, &root, all_triggers_on(&w));
    let v = fixed_identity(96 + 1);
    let mut log = Vec::new();
    for i in 0..50u64 {
        let r = h.apply(
            &v,
            Input::Record {
                causer: Causer::Member(w.key(2)),
                input: owned("req", Some("s"), None),
            },
            t(10 + i),
        );
        assert!(matches!(r, Ok(Outcome::Recorded(_))), "{r:?}");
        if i % 10 == 9 {
            h.apply(&v, Input::Checkpoint, t(10 + i)).unwrap();
        }
    }
    let f = |h: &AuditHost| {
        let m = h.member().unwrap();
        (m.free_usage(), m.requested_usage(2), h.due(t(1_000)))
    };
    log.push(format!("after 50 requests + 5 own checkpoints: {:?}", f(&h)));
    h.apply(&v, Input::Roster(w.remove(2)), t(100)).unwrap();
    log.push(format!("member 2 removed by the convener: {:?}", f(&h)));
    let rel = h.apply(&v, Input::Release(w.key(2)), t(101)).map(|_| "Released");
    log.push(format!("release of 2 ({rel:?}): {:?}", f(&h)));
    h.apply(&v, Input::Roster(w.add(4, 2)), t(102)).unwrap();
    for i in 0..20u64 {
        let _ = h.apply(
            &v,
            Input::Record {
                causer: Causer::Member(w.key(4)),
                input: owned("req", None, None),
            },
            t(110 + i),
        );
    }
    log.push(format!("newcomer 4 in slot 2, 20 requests: {:?}", f(&h)));
    let (d, line) = probe(&mut h, &v, 2_000);
    println!("QA2 t4 roster: {}; {line}", log.join("; "));
    assert!(!d, "{line}");
    assert_eq!(h.member().unwrap().free_usage(), (0, 0), "cost moved into the free part");
    drop(h);
    scratch_done(&base);
}
