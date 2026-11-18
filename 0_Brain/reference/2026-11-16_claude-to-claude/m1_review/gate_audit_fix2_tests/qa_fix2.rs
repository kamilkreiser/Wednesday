//! Independent check of M3 AUDIT-FIX2 (the seat clause of `try_set_limits`, QA-m1). Test code
//! only; every fixture is generated here from the fixed test identities of `common`.
//! A `qa2_finding_*` test PASSING means the state it names is demonstrated (it is not a failure of
//! the build under test unless the verdict says so).
mod common;

use std::collections::{BTreeMap, BTreeSet};

use coagent_audit::budget::{CLOSING_CHECKPOINT_BYTES, CLOSING_CHECKPOINT_RECORDS};
use coagent_audit::chain::{AuthorChain, EventInput};
use coagent_audit::redact::PatternRedactor;
use coagent_audit::session::{SessionAudit, StoreLimits};
use coagent_audit::store::{MemStore, Part, Store};
use coagent_audit::AuditError;
use coagent_proto::bytes::SessionId;
use common::*;

const V: usize = 1;
const CP: (usize, usize) = (CLOSING_CHECKPOINT_BYTES, CLOSING_CHECKPOINT_RECORDS);

fn tiny() -> EventInput<'static> {
    EventInput {
        kind: "x",
        summary: None,
        full: None,
    }
}

fn inp(s: &str) -> EventInput<'_> {
    EventInput {
        kind: "x",
        summary: Some(s),
        full: None,
    }
}

/// Limits for a seat of (bytes, records).
fn seat(b: usize, r: usize) -> StoreLimits {
    StoreLimits {
        bytes: 8 * b,
        records: 8 * r,
    }
}

fn fits(u: (usize, usize), lim: (usize, usize)) -> bool {
    u.0 + CP.0 <= lim.0 && u.1 + CP.1 <= lim.1
}

/// The slots owing a checkpoint and each allowance's usage, read from the store keys alone (own
/// reading, written for this check: a requested own event numbered after the last own checkpoint).
fn owing<S: Store>(st: &S, s: &SessionId) -> BTreeSet<u8> {
    let mut req: BTreeMap<u64, u8> = BTreeMap::new();
    let mut last = 0;
    for (k, _) in st.list(s).unwrap() {
        match k.part {
            Part::OwnEvent(Some(slot)) => {
                req.insert(k.n, slot);
            }
            Part::OwnHead => last = last.max(k.n),
            _ => {}
        }
    }
    req.range(last + 1..).map(|(_, s)| *s).collect()
}

/// The own records alone (events of both kinds and own checkpoints).
fn own_alone<S: Store>(st: &S, s: &SessionId) -> (usize, usize) {
    let mut u = (0, 0);
    for (k, r) in st.list(s).unwrap() {
        if matches!(k.part, Part::OwnEvent(_) | Part::OwnHead) {
            u = (u.0 + 4 + r.len(), u.1 + 1);
        }
    }
    u
}

fn own_seat(v: &SessionAudit<MemStore>) -> (usize, usize) {
    v.seat_usage(v.status().own_slot)
}

/// Every owing allowance and the own seat have room for one checkpoint under the limits in force.
fn room_for_owed(w: &World, v: &SessionAudit<MemStore>) -> bool {
    let l = v.limits();
    let a = l.requested_allowance();
    owing(v.store(), &w.s)
        .iter()
        .all(|s| fits(v.requested_usage(*s), a))
        && fits(own_seat(v), l.per_peer())
}

/// V with `n_own` own records of 300 characters and one request by H (slot 3): a checkpoint owed.
fn owed_session(base: u8, n_own: u64) -> (World, SessionAudit<MemStore>) {
    let w = World::new(base, 10, 8);
    let mut v = w.audit(V, every(1_000_000));
    v.try_set_limits(seat(64 * 1024, 512)).unwrap();
    let body = "y".repeat(300);
    for i in 0..n_own {
        v.record(&w.ids[V], inp(&body), t(1 + i)).unwrap();
    }
    v.record_for(&w.ids[V], &w.key(3), tiny(), t(5_000))
        .unwrap();
    assert_eq!(owing(v.store(), &w.s), BTreeSet::from([3u8]));
    (w, v)
}

// -------------------------------------------------------------------------------------------------
// 1. The exact boundary, bytes and records, with every owing allowance having room
// -------------------------------------------------------------------------------------------------

#[test]
fn qa2_boundary_bytes_exact_ok_one_less_refused_and_the_room_holds_against_everything() {
    let (w, mut v) = owed_session(0xA1, 30);
    let su = own_seat(&v);
    let exact = seat(su.0 + CP.0, 512);
    let one_less = seat(su.0 + CP.0 - 1, 512);
    // per seat bytes are bytes / 8: `seat` multiplies by 8, so these are exact per-seat values
    assert_eq!(exact.per_peer(), (su.0 + CP.0, 512));
    let alw = one_less.requested_allowance();
    assert!(
        fits(v.requested_usage(3), alw),
        "setup: clause (A) must accept"
    );
    let before = v.limits();
    let r_less = v.try_set_limits(one_less);
    let lim_after_refusal = v.limits();
    let r_exact = v.try_set_limits(exact);
    // after the exact lowering nothing else may take the checkpoint's room
    let own_try = v.record(&w.ids[V], tiny(), t(6_000));
    let req_try = v.record_for(&w.ids[V], &w.key(3), tiny(), t(6_001));
    let req_other = v.record_for(&w.ids[V], &w.key(5), tiny(), t(6_002));
    let room = room_for_owed(&w, &v);
    let cp = v.checkpoint_now(&w.ids[V], t(6_003)).map(|h| h.author_seq);
    let after = own_seat(&v);
    eprintln!(
        "qa2 boundary bytes: seat {su:?}; one less {r_less:?} (limits then {lim_after_refusal:?}); \
         exact {r_exact:?}; own record {own_try:?}; H again {req_try:?}; another requester \
         {req_other:?}; room {room}; checkpoint {cp:?}; seat after {after:?} of {:?}",
        v.limits().per_peer()
    );
    assert_eq!(r_less, Err(AuditError::LogFull));
    assert_eq!(lim_after_refusal, before);
    assert_eq!(r_exact, Ok(()));
    assert!(room);
    assert_eq!(own_try.map(|_| ()), Err(AuditError::LogFull));
    assert_eq!(req_try.map(|_| ()), Err(AuditError::LogFull));
    assert_eq!(req_other.map(|_| ()), Err(AuditError::LogFull));
    assert_eq!(cp, Ok(v.own().seq()));
    assert!(after.0 <= v.limits().per_peer().0 && after.1 <= v.limits().per_peer().1);
}

#[test]
fn qa2_boundary_records_exact_ok_one_fewer_refused() {
    let (w, mut v) = owed_session(0xA2, 30);
    let su = own_seat(&v);
    let exact = seat(64 * 1024, su.1 + CP.1);
    let fewer = seat(64 * 1024, su.1 + CP.1 - 1);
    assert!(
        fits(v.requested_usage(3), fewer.requested_allowance()),
        "setup: clause (A) must accept"
    );
    let before = v.limits();
    let r_fewer = v.try_set_limits(fewer);
    let same = v.limits() == before;
    let r_exact = v.try_set_limits(exact);
    let own_try = v.record(&w.ids[V], tiny(), t(6_000)).map(|_| ());
    let cp = v.checkpoint_now(&w.ids[V], t(6_003)).map(|h| h.author_seq);
    eprintln!(
        "qa2 boundary records: seat {su:?}; one fewer {r_fewer:?} (unchanged {same}); exact \
         {r_exact:?}; own record {own_try:?}; checkpoint {cp:?}; seat after {:?} of {:?}",
        own_seat(&v),
        v.limits().per_peer()
    );
    assert_eq!(r_fewer, Err(AuditError::LogFull));
    assert!(same);
    assert_eq!(r_exact, Ok(()));
    assert_eq!(own_try, Err(AuditError::LogFull));
    assert_eq!(cp, Ok(v.own().seq()));
}

// -------------------------------------------------------------------------------------------------
// 2. Lowering in steps; raise then lower; bytes only; records only
// -------------------------------------------------------------------------------------------------

#[test]
fn qa2_lowering_in_steps_every_accepted_step_keeps_the_room() {
    let (w, mut v) = owed_session(0xA3, 30);
    let mut accepted = 0;
    let mut refused = 0;
    // bytes only, then records only, each in small steps from far above to far below
    for b in (1_000..64 * 1024).rev().step_by(97) {
        let l = seat(b, 512);
        let before = v.limits();
        match v.try_set_limits(l) {
            Ok(()) => {
                accepted += 1;
                assert!(
                    room_for_owed(&w, &v),
                    "bytes step {b}: accepted without room"
                );
            }
            Err(AuditError::LogFull) => {
                refused += 1;
                assert_eq!(
                    v.limits(),
                    before,
                    "bytes step {b}: a refusal moved the limits"
                );
            }
            Err(e) => panic!("{e:?}"),
        }
    }
    let after_bytes = v.limits();
    // raise back to the defaults, then records only
    assert_eq!(v.try_set_limits(StoreLimits::default()), Ok(()));
    for r in (8..512).rev() {
        let l = StoreLimits {
            bytes: StoreLimits::default().bytes,
            records: 8 * r,
        };
        let before = v.limits();
        match v.try_set_limits(l) {
            Ok(()) => {
                accepted += 1;
                assert!(
                    room_for_owed(&w, &v),
                    "records step {r}: accepted without room"
                );
            }
            Err(AuditError::LogFull) => {
                refused += 1;
                assert_eq!(v.limits(), before);
            }
            Err(e) => panic!("{e:?}"),
        }
    }
    let after_records = v.limits();
    // raise then lower: a raise to the defaults, then straight to the lowest step
    assert_eq!(v.try_set_limits(StoreLimits::default()), Ok(()));
    let low = v.try_set_limits(seat(1_000, 8));
    let cp = v.checkpoint_now(&w.ids[V], t(9_000)).map(|h| h.author_seq);
    eprintln!(
        "qa2 steps: accepted {accepted}, refused {refused}; lowest by bytes {:?}, by records {:?}; \
         raise then lowest {low:?}; checkpoint {cp:?}",
        after_bytes.per_peer(),
        after_records.per_peer()
    );
    assert!(accepted > 10 && refused > 10);
    assert_eq!(low, Err(AuditError::LogFull));
    assert_eq!(cp, Ok(v.own().seq()));
}

// -------------------------------------------------------------------------------------------------
// 3. Nothing owed: accepted, and then nothing is recorded that would need a witness
// -------------------------------------------------------------------------------------------------

#[test]
fn qa2_nothing_owed_lowering_below_the_seat_is_accepted_then_requests_refused() {
    let (w, mut v) = owed_session(0xA4, 30);
    v.checkpoint_now(&w.ids[V], t(5_500)).unwrap();
    assert!(owing(v.store(), &w.s).is_empty());
    let su = own_seat(&v);
    let low = seat(su.0 / 2, su.1 / 2);
    let r = v.try_set_limits(low);
    let usage = v.store_usage();
    let seq = v.own().seq();
    let reqs: Vec<_> = (0..4u64)
        .map(|i| {
            v.record_for(&w.ids[V], &w.key(2 + i as usize), tiny(), t(6_000 + i))
                .map(|_| ())
        })
        .collect();
    let own_try = v.record(&w.ids[V], tiny(), t(6_100)).map(|_| ());
    eprintln!(
        "qa2 nothing owed: seat {su:?} lowered to {:?}: {r:?}; requests {reqs:?}; own record \
         {own_try:?}; own seq {seq} -> {}; store {usage:?} -> {:?}",
        low.per_peer(),
        v.own().seq(),
        v.store_usage()
    );
    assert_eq!(r, Ok(()));
    assert_eq!(v.limits(), low);
    assert!(reqs.iter().all(|x| *x == Err(AuditError::LogFull)));
    assert_eq!(own_try, Err(AuditError::LogFull));
    assert_eq!(v.own().seq(), seq);
    assert_eq!(v.store_usage(), usage);
    assert!(owing(v.store(), &w.s).is_empty());
}

// -------------------------------------------------------------------------------------------------
// 4. The member moved: re-added into a clean slot; N1's seat counted by the clause; slot 0
// -------------------------------------------------------------------------------------------------

/// X (slot 2) has records at V; V owes a checkpoint (H, slot 3).
fn with_x(base: u8, n_own: u64) -> (World, SessionAudit<MemStore>) {
    let w = World::new(base, 10, 6);
    let mut v = w.audit(V, every(1_000_000));
    v.try_set_limits(seat(64 * 1024, 128)).unwrap();
    for i in 0..n_own {
        v.record(&w.ids[V], inp(&"o".repeat(300)), t(i)).unwrap();
    }
    let mut x = AuthorChain::new(
        &w.ids[2],
        w.s,
        every(1_000),
        Box::new(PatternRedactor),
        t(0),
    );
    for i in 1..4u64 {
        x.append(&w.ids[2], inp(&"s".repeat(1_000)), t(20 + i))
            .unwrap();
        v.receive(&w.ids[V], x.event(i).unwrap(), t(20 + i))
            .unwrap();
    }
    v.record_for(&w.ids[V], &w.key(3), tiny(), t(30)).unwrap();
    (w, v)
}

#[test]
fn qa2_re_added_into_a_clean_slot_the_room_follows_and_into_n1s_seat_the_clause_counts_it() {
    // (a) accepted at the exact boundary in slot 1, then V removed and re-added into slot 7 (never
    // used): the seat is its own records alone, the checkpoint is Ok
    let (mut w, mut v) = with_x(0xB1, 20);
    let su = own_seat(&v);
    let r = v.try_set_limits(seat(su.0 + CP.0, su.1 + CP.1 + 40));
    for ro in [w.remove(V), w.add(V, 7)] {
        v.apply_roster(&ro).unwrap();
    }
    let slot = v.status().own_slot;
    let cp = v.checkpoint_now(&w.ids[V], t(40)).map(|h| h.author_seq);
    eprintln!("qa2 re-add clean: seat {su:?}, exact {r:?}; now slot {slot}; checkpoint {cp:?}");
    assert_eq!(r, Ok(()));
    assert_eq!(slot, 7);
    assert_eq!(cp, Ok(v.own().seq()));

    // (b) N1's seat: V removed and re-added into slot 2 (X removed, its records stay). The clause
    // counts X's records: a seat of own records alone plus one checkpoint is refused; one that also
    // holds X's records is accepted, and then the checkpoint is Ok.
    let (mut w, mut v) = with_x(0xB2, 20);
    for ro in [w.remove(2), w.remove(V), w.add(V, 2)] {
        v.apply_roster(&ro).unwrap();
    }
    let own = own_alone(v.store(), &w.s);
    let su = own_seat(&v);
    let rec = su.1 + CP.1 + 40;
    let own_only = v.try_set_limits(seat(own.0 + CP.0, rec));
    let whole = v.try_set_limits(seat(su.0 + CP.0, rec));
    let cp = v.checkpoint_now(&w.ids[V], t(41)).map(|h| h.author_seq);
    eprintln!(
        "qa2 N1 seat: own alone {own:?}, seat {su:?}; own-only limits {own_only:?}; whole seat \
         {whole:?}; checkpoint {cp:?}"
    );
    assert!(su.0 > own.0, "setup: X's records are not in the seat");
    assert_eq!(own_only, Err(AuditError::LogFull));
    assert_eq!(whole, Ok(()));
    assert_eq!(cp, Ok(v.own().seq()));
}

/// Cause (c), stated in the brief as the starter's act plus a peer: V is removed (falls back to
/// slot 0), a lowering is accepted at the exact boundary (records) of slot 0's seat as it stands, then ONE
/// event of the slot-0 member arrives and takes the room: the owed checkpoint is refused. In the
/// test world (and by default) the slot-0 member IS the starter (the roster signer), so one party
/// does it. PASSING demonstrates the state (counted as N1 by the branch's property).
#[test]
fn qa2_finding_slot0_fallback_a_later_slot0_event_takes_the_room_after_an_accepted_change() {
    let (mut w, mut v) = with_x(0xB3, 30);
    let ro = w.remove(V);
    v.apply_roster(&ro).unwrap();
    assert_eq!(v.status().own_slot, 0);
    let mut z = AuthorChain::new(
        &w.ids[0],
        w.s,
        every(1_000),
        Box::new(PatternRedactor),
        t(0),
    );
    z.append(&w.ids[0], inp(&"z".repeat(100)), t(50)).unwrap();
    v.receive(&w.ids[V], z.event(1).unwrap(), t(50)).unwrap();
    let own = own_alone(v.store(), &w.s);
    let su = own_seat(&v);
    // the seat's RECORDS exactly at the slot-0 seat plus one checkpoint, bytes generous
    let own_only = v.try_set_limits(seat(64 * 1024, own.1 + CP.1));
    let exact = v.try_set_limits(seat(64 * 1024, su.1 + CP.1));
    let room = room_for_owed(&w, &v);
    z.append(&w.ids[0], tiny(), t(51)).unwrap();
    let arrive = v.receive(&w.ids[V], z.event(2).unwrap(), t(51)).map(|_| ());
    let cps: Vec<_> = (0..3u64)
        .map(|i| v.checkpoint_now(&w.ids[V], t(60 + i)).map(|_| ()))
        .collect();
    eprintln!(
        "qa2 slot-0 fallback: own alone {own:?}, slot-0 seat {su:?}; own-only limits {own_only:?}; \
         exact {exact:?} (room {room}); slot-0 member's event {arrive:?}; checkpoints {cps:?}"
    );
    assert_eq!(own_only, Err(AuditError::LogFull));
    assert_eq!(exact, Ok(()));
    assert!(room);
    assert_eq!(arrive, Ok(()));
    assert!(cps.iter().all(|x| *x == Err(AuditError::LogFull)));
}

// -------------------------------------------------------------------------------------------------
// 5. A peer alone: after an accepted change at the exact boundary, every other member floods
// -------------------------------------------------------------------------------------------------

#[test]
fn qa2_a_peer_alone_cannot_take_the_owed_checkpoints_room() {
    let (w, mut v) = owed_session(0xA5, 30);
    let su = own_seat(&v);
    assert_eq!(v.try_set_limits(seat(su.0 + CP.0, su.1 + CP.1)), Ok(()));
    let mut got = 0;
    for p in [0usize, 2, 3, 4, 5, 6, 7] {
        let mut c = AuthorChain::new(
            &w.ids[p],
            w.s,
            every(1_000_000),
            Box::new(PatternRedactor),
            t(0),
        );
        for i in 1..200u64 {
            c.append(&w.ids[p], inp(&"p".repeat(500)), t(100 + i))
                .unwrap();
            if v.receive(&w.ids[V], c.event(i).unwrap(), t(100 + i))
                .is_err()
            {
                break;
            }
            got += 1;
        }
        // and requests from every peer until refused
        while v.record_for(&w.ids[V], &w.key(p), tiny(), t(500)).is_ok() {
            got += 1;
        }
    }
    let room = room_for_owed(&w, &v);
    let cp = v.checkpoint_now(&w.ids[V], t(600)).map(|h| h.author_seq);
    eprintln!(
        "qa2 peer alone: {got} peer records/requests accepted; room {room}; checkpoint {cp:?}"
    );
    assert!(got > 0);
    assert!(room);
    assert_eq!(cp, Ok(v.own().seq()));
}

// -------------------------------------------------------------------------------------------------
// 6. set_limits is try_set_limits with the answer dropped, across seat refusals
// -------------------------------------------------------------------------------------------------

#[test]
fn qa2_set_limits_equals_try_set_limits_across_seat_refusals() {
    let (w, mut a) = owed_session(0xA6, 30);
    let (_, mut b) = owed_session(0xA6, 30);
    let su = own_seat(&a);
    let offers = [
        seat(su.0 + CP.0 - 1, 512),
        seat(su.0 + CP.0, 512),
        seat(su.0 + CP.0 + 1, su.1),
        seat(64 * 1024, su.1 + CP.1),
        StoreLimits::default(),
        seat(su.0 / 2, 512),
        seat(su.0 + CP.0, su.1 + CP.1),
    ];
    let mut seat_refusals = 0;
    for (i, l) in offers.iter().enumerate() {
        let r = a.try_set_limits(*l);
        b.set_limits(*l);
        if r.is_err() {
            seat_refusals += 1;
        }
        assert_eq!(a.limits(), b.limits(), "offer {i}");
    }
    let ca = a.checkpoint_now(&w.ids[V], t(9_000)).map(|h| h.author_seq);
    let cb = b.checkpoint_now(&w.ids[V], t(9_000)).map(|h| h.author_seq);
    eprintln!("qa2 set_limits: {seat_refusals} refused; checkpoints {ca:?} {cb:?}");
    assert!(seat_refusals >= 3);
    assert_eq!(ca, cb);
    assert!(ca.is_ok());
}

// -------------------------------------------------------------------------------------------------
// 7. N1's state AND the resume-defaults state together: neither remedy the docs name works
// -------------------------------------------------------------------------------------------------

/// Limits L per seat (default bytes less 20,000, 2,000 records): each allowance has MORE bytes than
/// under the defaults. H fills its allowance under L (a checkpoint owed). X (slot 2) fills its seat so
/// that, once the starter removes X and V and re-adds V into slot 2, the seat is a little over L's
/// seat but within the defaults' seat. Then: under L the checkpoint is refused (N1); after `resume`
/// (defaults) it is refused again, now by the payer (resume-defaults); `try_set_limits(defaults)` and
/// `try_set_limits(L)` are both refused, so the caller remedy in docs/AUDIT.md ("offer your own
/// limits; if refused, the limits in force before the restart") does not end it. A third limit
/// (default bytes, records just above the seat) does. PASSING demonstrates the state.
#[test]
fn qa2_finding_n1_and_resume_defaults_together_neither_named_remedy_works() {
    let mut w = World::new(0xC1, 10, 6);
    let mut v = w.audit(V, every(1_000_000));
    let d = StoreLimits::default();
    let (bd, _) = d.per_peer();
    let l = seat(bd - 20_000, 2_000);
    assert_eq!(v.try_set_limits(l), Ok(()));
    assert!(l.requested_allowance().0 > d.requested_allowance().0);
    for i in 0..3u64 {
        v.record(&w.ids[V], inp("own"), t(i)).unwrap();
    }
    // H fills its allowance under L: big requests, then smaller ones to top it up
    let h = w.key(3);
    let mut n = 10u64;
    for size in [4_000usize, 2_000, 1_000, 300, 100, 30, 10, 1] {
        let f = "f".repeat(size);
        while v.record_for(&w.ids[V], &h, inp(&f), t(n)).is_ok() {
            n += 1;
        }
    }
    // X fills slot 2 with its own choices until its own log refuses (its free part, about half a seat)
    let mut x = AuthorChain::new(
        &w.ids[2],
        w.s,
        every(1_000_000),
        Box::new(PatternRedactor),
        t(0),
    );
    let mut xi = 0u64;
    'x: for size in [40_000usize, 10_000, 3_000] {
        loop {
            let f = "x".repeat(size);
            if x.append(&w.ids[2], input("x", "s", &f), t(100 + xi))
                .is_err()
            {
                continue 'x;
            }
            xi += 1;
            if v.receive(&w.ids[V], x.event(xi).unwrap(), t(100 + xi))
                .is_err()
            {
                break 'x;
            }
        }
    }
    // V's own records fill its own seat so that, with X's records, the seat after the re-add is
    // L's seat plus 5,000 bytes (within the defaults' seat)
    let target = l.per_peer().0 + 5_000 - v.seat_usage(2).0;
    let mut k = 1_000u64;
    for size in [40_000usize, 10_000, 3_000, 1_000, 300, 100] {
        loop {
            let cur = own_alone(v.store(), &w.s).0;
            if cur + size + 2_000 > target {
                break;
            }
            let f = "o".repeat(size);
            if v.record(&w.ids[V], input("x", "s", &f), t(k)).is_err() {
                break;
            }
            k += 1;
        }
    }
    let hu = v.requested_usage(3);
    let own_all = own_alone(v.store(), &w.s);
    let x_seat = v.seat_usage(2);
    for ro in [w.remove(2), w.remove(V), w.add(V, 2)] {
        v.apply_roster(&ro).unwrap();
    }
    let seat_now = own_seat(&v);
    let cp_l = v.checkpoint_now(&w.ids[V], t(5_000)).map(|_| ());
    let again_l = v.try_set_limits(l);
    // restart
    let mut r = SessionAudit::resume(
        v.store().clone(),
        w.s,
        &w.ids[V],
        &w.ids[0].verified(),
        every(1_000_000),
        Box::new(PatternRedactor),
        t(6_000),
    )
    .unwrap();
    let cp_d = r.checkpoint_now(&w.ids[V], t(6_001)).map(|_| ());
    let set_d = r.try_set_limits(d);
    let set_l = r.try_set_limits(l);
    let cp_d2 = r.checkpoint_now(&w.ids[V], t(6_002)).map(|_| ());
    // default bytes, records just above the seat: allowance bytes still above H's usage
    let third = seat(bd, seat_now.1 + CP.1 + 20);
    let set_third = r.try_set_limits(third);
    let cp_third = r.checkpoint_now(&w.ids[V], t(6_003)).map(|h| h.author_seq);
    eprintln!(
        "qa2 N1+resume-defaults: L {l:?} allowance {:?} (defaults {:?}); H's allowance {hu:?}; own \
         records {own_all:?}; X's seat {x_seat:?} target {target}; after re-add seat {seat_now:?} \
         (L seat {:?}, default seat {:?}); under L: checkpoint {cp_l:?}, L again {again_l:?}; after \
         resume: checkpoint {cp_d:?}, defaults {set_d:?}, L {set_l:?}, checkpoint {cp_d2:?}, limits \
         {:?}; a third limit {third:?}: {set_third:?}, checkpoint {cp_third:?} of {}",
        l.requested_allowance(),
        d.requested_allowance(),
        l.per_peer(),
        d.per_peer(),
        r.limits(),
        r.own().seq()
    );
    assert!(!owing(r.store(), &w.s).is_empty() || cp_third.is_ok());
    assert!(!fits(seat_now, l.per_peer()) && fits(seat_now, d.per_peer()));
    assert!(fits(hu, l.requested_allowance()) && !fits(hu, d.requested_allowance()));
    assert_eq!(cp_l, Err(AuditError::LogFull));
    assert_eq!(again_l, Err(AuditError::LogFull));
    assert_eq!(cp_d, Err(AuditError::LogFull));
    assert_eq!(set_d, Err(AuditError::LogFull));
    assert_eq!(set_l, Err(AuditError::LogFull));
    assert_eq!(cp_d2, Err(AuditError::LogFull));
    assert_eq!(set_third, Ok(()));
    assert_eq!(cp_third, Ok(r.own().seq()));
}
