//! Gate r4 for M3-AUDIT (independent QA of design 07's build, 2026-11-17). Test code only; every
//! fixture is generated here from the fixed test identities of `common`.
//!
//! - `r4_finding_*`: PASSING means the weakness is demonstrated (as in the earlier gates).
//! - `r4_fixed_*`: PASSING means an earlier round's Blocker or Major is closed; each asserts the
//!   property in a form the old behaviour fails.
//! - `r4_prop_storage_accounting`: an own generated-schedule harness for the storage-accounting
//!   class (honest, hostile and outside authors; roster churn; release; resume; edges of seats).
mod common;

use std::cell::{Cell, RefCell};
use std::collections::{BTreeMap, BTreeSet};
use std::rc::Rc;

use coagent_audit::budget::{Table, CAPACITY_BYTES, CAPACITY_RECORDS};
use coagent_audit::bundle::{verify, Bundle, Record, MAX_RECORD_BYTES};
use coagent_audit::chain::{AuthorChain, EventInput};
use coagent_audit::checkpoint::{CheckpointPolicy, SignedHead};
use coagent_audit::domain::AuditDomain;
use coagent_audit::equivocation::{HeadsSeenBody, SignedHeadsSeen, Statement};
use coagent_audit::received::{ReceiveError, MAX_HEADS_PER_AUTHOR};
use coagent_audit::redact::PatternRedactor;
use coagent_audit::session::{SessionAudit, StoreLimits};
use coagent_audit::store::{MemStore, Part, Store, StoreError, StoreKey};
use coagent_audit::tiers::ShareLevel;
use coagent_audit::AuditError;
use coagent_crypto::identity::DeviceIdentity;
use coagent_proto::bytes::{KeyId, SessionId};
use coagent_proto::canonical;
use common::*;
use proptest::prelude::*;
use proptest::test_runner::{Config, TestCaseError, TestRunner};

const V: usize = 1;

fn tiny() -> EventInput<'static> {
    EventInput {
        kind: "x",
        summary: None,
        full: None,
    }
}

fn hs_signed(
    id: &DeviceIdentity,
    s: SessionId,
    to: Option<KeyId>,
    rv: u64,
    entries: Vec<Statement>,
) -> SignedHeadsSeen {
    let body = HeadsSeenBody {
        session_id: s,
        from: id.key_id(),
        to,
        roster_v: rv,
        entries,
    };
    let sig = audit_sign(
        id,
        AuditDomain::HeadsSeen,
        &canonical::encode(&body).unwrap(),
    );
    SignedHeadsSeen {
        session_id: body.session_id,
        from: body.from,
        to: body.to,
        roster_v: body.roster_v,
        entries: body.entries,
        sig,
    }
}

fn real_size<S: Store>(st: &S, s: &SessionId) -> (usize, usize) {
    let l = st.list(s).unwrap();
    (l.iter().map(|(_, r)| 4 + r.len()).sum(), l.len())
}

fn count_part<S: Store>(st: &S, s: &SessionId, f: impl Fn(&StoreKey) -> bool) -> usize {
    st.list(s).unwrap().iter().filter(|(k, _)| f(k)).count()
}

fn small(seat_bytes: usize, seat_records: usize) -> StoreLimits {
    StoreLimits {
        bytes: 8 * seat_bytes,
        records: 8 * seat_records,
    }
}

// =================================================================================================
// R4 findings
// =================================================================================================

/// One member V (slot 1) of eight acts on requests from the seven others: one `record_for` per
/// minute, the requester rotating, until every allowance is full; V's daemon calls `checkpoint` on
/// the default policy (50 events or 60 s). V records NOTHING of its own choice during this. Then V
/// records tiny own events until refused. Returns (free-part bytes used before V's own records,
/// checkpoints made, own records V could still make, requested events accepted, minutes run,
/// requested bytes charged in all).
fn requester_run(requests: bool, limits: Option<StoreLimits>) -> (usize, u64, u64, u64, u64, usize) {
    let w = World::new(0x51, 8, 8);
    let mut v = w.audit(V, CheckpointPolicy::default());
    if let Some(l) = limits {
        v.set_limits(l);
    }
    let requesters: Vec<usize> = (0..8).filter(|i| *i != V).collect();
    let (mut accepted, mut cps, mut m, mut refused_in_a_row) = (0u64, 0u64, 0u64, 0u32);
    while refused_in_a_row < 14 && m < 100_000 {
        m += 1;
        let now = t(m * 60_000);
        if requests {
            let g = requesters[(m as usize) % requesters.len()];
            if v.record_for(&w.ids[V], &w.key(g), tiny(), now).is_ok() {
                accepted += 1;
                refused_in_a_row = 0;
            } else {
                refused_in_a_row += 1;
            }
        } else {
            refused_in_a_row += 1;
        }
        if let Ok(Some(_)) = v.checkpoint(&w.ids[V], now) {
            cps += 1;
        }
    }
    let free_before_own = v.free_usage().0;
    let requested: usize = (0..8u8).map(|s| v.requested_usage(s).0).sum();
    let mut own = 0u64;
    loop {
        m += 1;
        match v.record(&w.ids[V], tiny(), t(m * 60_000)) {
            Ok(_) => own += 1,
            Err(AuditError::LogFull) => break,
            Err(e) => panic!("{e:?}"),
        }
    }
    (free_before_own, cps, own, accepted, m, requested)
}

/// R4-M1. Checkpoints covering events recorded at a PEER'S request (`record_for`) are charged to the
/// FREE part (design 07 §1.4 (b): "Nothing a peer does can consume it"; §1.6 item 2: the free part's
/// usage is a function of V's own calls alone; §2: a hostile member can never "use ... the free
/// part"). Requests trickled one per minute, each requester within its allowance, and V's ordinary
/// checkpoint cadence: the requesters' checkpoints take most of V's free part although V recorded
/// nothing of its own, and V can afterwards make far fewer own records than without the requests.
#[test]
fn r4_finding_requested_events_drive_checkpoints_into_the_free_part() {
    let l = small(32 * 1024, 256);
    let (free_with, cps_with, own_with, acc, mins, req) = requester_run(true, Some(l));
    let (free_without, cps_without, own_without, _, _, _) = requester_run(false, Some(l));
    eprintln!(
        "R4-M1 small limits: free part limit {:?}, requested allowance {:?} each; with requests: {acc} \
         requested events accepted ({req} bytes charged to allowances) over {mins} min, {cps_with} \
         checkpoints, free part used {free_with} bytes before any own record, own records still \
         possible {own_with}; without requests: {cps_without} checkpoints, free part used \
         {free_without}, own records possible {own_without}",
        l.free_part(),
        l.requested_allowance()
    );
    assert_eq!(free_without, 0, "control: V's free part moved without any input");
    assert!(
        free_with * 2 > l.free_part().0 && own_with * 2 < own_without,
        "R4-M1 not shown: requests used {free_with} bytes of the free part; own records {own_with} against {own_without}"
    );
}

/// R4-M1 with the DEFAULT limits and policy, in release: what a one-per-minute trickle of requests
/// (every requester within its allowance) takes from V's free part.
#[test]
#[ignore = "release measurement: cargo test --release --test gate_r4 -- --ignored"]
fn r4_finding_release_requested_checkpoints_default_limits() {
    let start = std::time::Instant::now();
    let (free_with, cps, own_with, acc, mins, req) = requester_run(true, None);
    let (free_without, _, own_without, _, _, _) = requester_run(false, None);
    let d = StoreLimits::default();
    eprintln!(
        "R4-M1 default limits: free part {:?}, allowance {:?} each; {acc} requested events \
         ({req} bytes in allowances) over {} minutes of one request per minute made {cps} \
         checkpoints, free part used {free_with} bytes ({:.1}%) with no own record; own records \
         then possible {own_with}, against {own_without} without the requests (free used \
         {free_without}); {:.2?}",
        d.free_part(),
        d.requested_allowance(),
        acc,
        100.0 * free_with as f64 / d.free_part().0 as f64,
        start.elapsed()
    );
    assert!(free_with * 2 > d.free_part().0);
}

/// A store whose writes can be made to fail (a disk error, a full disk), as the daemon's will.
#[derive(Clone)]
struct Flaky {
    inner: MemStore,
    fail: Rc<Cell<bool>>,
}

impl Store for Flaky {
    fn put(&mut self, s: &SessionId, k: &StoreKey, r: &[u8]) -> Result<(), StoreError> {
        if self.fail.get() {
            return Err(StoreError::Unavailable("gate r4: injected write failure"));
        }
        self.inner.put(s, k, r)
    }
    fn remove(&mut self, s: &SessionId, k: &StoreKey) -> Result<(), StoreError> {
        self.inner.remove(s, k)
    }
    fn list(&self, s: &SessionId) -> Result<Vec<(StoreKey, Vec<u8>)>, StoreError> {
        self.inner.list(s)
    }
}

fn flaky_audit(w: &World, i: usize, fail: Rc<Cell<bool>>) -> SessionAudit<Flaky> {
    SessionAudit::start(
        Flaky {
            inner: MemStore::new(),
            fail,
        },
        &w.ids[i],
        &w.ids[0].verified(),
        &w.rosters[0],
        every(1_000),
        Box::new(PatternRedactor),
        t(0),
    )
    .unwrap()
}

/// R4-m1 (own chain). A store write that fails after the space check leaves the own chain advanced
/// in memory and the record absent from the store (design 07 §1.7 step 6: "apply and store, all or
/// nothing"). The next record succeeds, so the stored own chain has a hole: the member's export no
/// longer verifies and `resume` refuses its store.
#[test]
fn r4_finding_a_failed_store_write_leaves_the_own_chain_ahead_of_the_store() {
    let w = World::new(0x52, 3, 3);
    let fail = Rc::new(Cell::new(false));
    let mut v = flaky_audit(&w, V, fail.clone());
    assert_eq!(v.record(&w.ids[V], tiny(), t(1)), Ok(1));
    fail.set(true);
    let r2 = v.record(&w.ids[V], tiny(), t(2));
    fail.set(false);
    let r3 = v.record(&w.ids[V], tiny(), t(3));
    let stored = count_part(v.store(), &w.s, |k| matches!(k.part, Part::OwnEvent(_)));
    let exp = v.export(&w.ids[V]).map(|b| verify(&b).map(|_| ()));
    let res = SessionAudit::resume(
        v.store().clone(),
        w.s,
        &w.ids[V],
        &w.ids[0].verified(),
        every(1_000),
        Box::new(PatternRedactor),
        t(4),
    )
    .map(|_| ());
    eprintln!(
        "R4-m1 own: record 2 {r2:?}; record 3 {r3:?}; in memory seq {}, stored own events {stored}; \
         export+verify {exp:?}; resume {res:?}",
        v.own().seq()
    );
    assert!(matches!(r2, Err(AuditError::Store(_))));
    assert!(
        v.own().seq() > stored as u64,
        "R4-m1 not shown: the in-memory chain did not run ahead of the store"
    );
    assert!(
        !matches!(exp, Ok(Ok(()))) || res.is_err(),
        "R4-m1 not shown: export and resume both still fine"
    );
}

/// R4-m1 (received chain): the same for another author's event. V commits it in memory, the write
/// fails, the author's re-send is a Replay, and the next event is stored after a hole.
#[test]
fn r4_finding_a_failed_store_write_leaves_a_hole_in_a_received_chain() {
    let w = World::new(0x53, 3, 3);
    let fail = Rc::new(Cell::new(false));
    let mut v = flaky_audit(&w, V, fail.clone());
    let mut a = AuthorChain::new(
        &w.ids[0],
        w.s,
        every(1_000),
        Box::new(PatternRedactor),
        t(0),
    );
    for i in 0..3 {
        a.append(&w.ids[0], tiny(), t(i)).unwrap();
    }
    let e = |n: u64| a.event(n).unwrap().clone();
    let r1 = v.receive(&w.ids[V], &e(1), t(1));
    fail.set(true);
    let r2 = v.receive(&w.ids[V], &e(2), t(2));
    fail.set(false);
    let r2b = v.receive(&w.ids[V], &e(2), t(3));
    let r3 = v.receive(&w.ids[V], &e(3), t(4));
    let stored: Vec<u64> = v
        .store()
        .list(&w.s)
        .unwrap()
        .iter()
        .filter(|(k, _)| matches!(k.part, Part::PeerEvent(_)))
        .map(|(k, _)| k.n)
        .collect();
    let exp = v.export(&w.ids[V]).map(|b| verify(&b).map(|_| ()));
    let res = SessionAudit::resume(
        v.store().clone(),
        w.s,
        &w.ids[V],
        &w.ids[0].verified(),
        every(1_000),
        Box::new(PatternRedactor),
        t(5),
    )
    .map(|_| ());
    eprintln!(
        "R4-m1 peer: r1 {:?} r2 {r2:?} re-send {r2b:?} r3 {:?}; stored seqs {stored:?}; \
         export+verify {exp:?}; resume {res:?}",
        r1.map(|_| ()),
        r3.as_ref().map(|_| ())
    );
    assert!(matches!(r2, Err(AuditError::Store(_))));
    assert!(
        stored == vec![1, 3],
        "R4-m1 not shown: stored received numbers {stored:?}"
    );
}

/// R4-m2. When the member ITSELF is removed and re-added by the starter into a slot that a removed
/// member's records still occupy, its own seat is counted on top of them: the seat of that slot
/// holds more than a seat (design 07 §1.6 item 3: every seat at most its limit).
#[test]
fn r4_finding_own_seat_re_added_into_a_used_slot_exceeds_the_seat() {
    let mut w = World::new(0x54, 5, 3);
    let l = small(16 * 1024, 64);
    let mut v = w.audit(V, every(1_000));
    v.set_limits(l);
    // X (member 2, slot 2) fills its seat at V
    let mut x = AuthorChain::new(
        &w.ids[2],
        w.s,
        every(1_000),
        Box::new(PatternRedactor),
        t(0),
    );
    let big_s = "s".repeat(4000);
    let big_f = "f".repeat(60_000);
    for i in 1..10_000u64 {
        x.append(&w.ids[2], input("x", &big_s, &big_f), t(i)).unwrap();
        if v.receive(&w.ids[V], x.event(i).unwrap(), t(i)).is_err() {
            break;
        }
    }
    let seat2 = v.seat_usage(2);
    let r2 = w.remove(2);
    let r3 = w.remove(V);
    let r4 = w.add(V, 2);
    let r5 = w.add(3, 1);
    let applied: Vec<_> = [r2, r3, r4, r5]
        .iter()
        .map(|r| v.apply_roster(r).map(|_| ()))
        .collect();
    let mut own = 0;
    for i in 0..10_000u64 {
        if v.record(&w.ids[V], input("x", &big_s, &big_f), t(20_000 + i)).is_err() {
            break;
        }
        own += 1;
    }
    let seat = v.seat_usage(2);
    let total: (usize, usize) = (0..8u8).fold((0, 0), |a, s| {
        let u = v.seat_usage(s);
        (a.0 + u.0, a.1 + u.1)
    });
    eprintln!(
        "R4-m2: X's seat 2 at V {seat2:?}; rosters {applied:?}; V re-added in slot 2 records {own} own \
         events; seat 2 now {seat:?} (seat limit {:?}, own limit {:?}); all seats {total:?} against \
         the seats' limit ({}, {})",
        l.per_peer(),
        l.own_reserved(),
        l.bytes,
        l.records
    );
    assert!(applied.iter().all(|r| r.is_ok()), "rosters refused: {applied:?}");
    assert!(
        seat.0 > l.per_peer().0,
        "R4-m2 not shown: seat 2 holds {seat:?}, within a seat"
    );
}

/// R4-n1. The edited gate test `r3_finding_fork_from_an_author_at_quota_gives_logfull_not_evidence`
/// accepts ANY `Receive` error as "reported as a fork". The property it stands for, done exactly:
/// an author whose seat is full sends a conflicting event; the answer is `Fork` with evidence, the
/// evidence is stored, and nothing else in the store changed.
#[test]
fn r4_fixed_r3_n2_fork_from_an_author_with_a_full_seat_is_a_fork_with_evidence() {
    let w = World::new(0x55, 3, 3);
    let mut v = w.audit(V, every(1_000));
    v.set_limits(small(4 * 1024, 64));
    let mut a = AuthorChain::new(&w.ids[2], w.s, every(1_000), Box::new(PatternRedactor), t(0));
    let mut n = 0;
    for i in 1..1_000u64 {
        a.append(&w.ids[2], input("x", "s", "f"), t(i)).unwrap();
        match v.receive(&w.ids[V], a.event(i).unwrap(), t(i)) {
            Ok(_) => n = i,
            Err(AuditError::LogFull) => break,
            Err(e) => panic!("{e:?}"),
        }
    }
    let mut alt = AuthorChain::new(&w.ids[2], w.s, every(1_000), Box::new(PatternRedactor), t(0));
    alt.append(&w.ids[2], input("y", "other", "story"), t(9)).unwrap();
    let before = v.store().list(&w.s).unwrap();
    let r = v.receive(&w.ids[V], alt.event(1).unwrap(), t(10));
    let after = v.store().list(&w.s).unwrap();
    let changed: Vec<Part> = after
        .iter()
        .filter(|x| !before.contains(x))
        .map(|(k, _)| k.part)
        .collect();
    eprintln!("R3-n2 recheck: {n} events filled the seat; fork answer {r:?}; changed parts {changed:?}");
    assert!(n > 0);
    assert!(
        matches!(r, Err(AuditError::Receive(ReceiveError::Fork(_)))),
        "a fork from an author with a full seat was not answered Fork: {r:?}"
    );
    assert_eq!(changed, vec![Part::Fixed(Table::Evidence)], "the fork stored something other than its evidence");
}

// =================================================================================================
// Earlier rounds' Blockers and Majors, each re-tested in a form the old behaviour fails
// =================================================================================================

/// A-B1 (round 1, Blocker): a member at `nothing` for author B holds no header of B by any route.
/// The old build put B's whole headers into every heads-seen record. Here: B's events go to A (full)
/// only; A sends C (B shares nothing with C) both its broadcast and an addressed record; a forged
/// broadcast carrying B's header is refused; C's store and export hold no header of B.
#[test]
fn r4_fixed_a_b1_a_nothing_member_holds_no_header_of_that_author() {
    let w = World::new(0x56, 3, 3);
    let (a_i, b_i, c_i) = (0usize, 1usize, 2usize);
    let mut a = w.audit(a_i, every(2));
    let mut b = w.audit(b_i, every(2));
    let mut c = w.audit(c_i, every(2));
    b.set_share_level(w.key(a_i), ShareLevel::Full);
    for i in 1..=4u64 {
        let seq = b.record(&w.ids[b_i], input("request.new", "sum", "full"), t(i)).unwrap();
        for (to, e) in b.outgoing(seq) {
            assert_eq!(to, w.key(a_i), "B sent an event to a member at nothing");
            a.receive(&w.ids[a_i], &e, t(i)).unwrap();
        }
        if let Some(h) = b.checkpoint(&w.ids[b_i], t(i)).unwrap() {
            a.receive_head(&w.ids[a_i], &h).unwrap();
            c.receive_head(&w.ids[c_i], &h).unwrap();
        }
    }
    let bh = a.peer(&w.key(b_i)).unwrap().event(4).unwrap().header.clone();
    let hs_b = a.heads_seen(&w.ids[a_i]).unwrap();
    let hs_c = a.heads_seen_for(&w.ids[a_i], &w.key(c_i)).unwrap();
    let forged = hs_signed(&w.ids[a_i], w.s, None, 1, vec![Statement::Header(bh.clone())]);
    let r1 = c.receive_heads_seen(&hs_b);
    let r2 = c.receive_heads_seen(&hs_c);
    let r3 = c.receive_heads_seen(&forged);
    let headers_in: usize = [&hs_b, &hs_c]
        .iter()
        .flat_map(|h| h.entries.iter())
        .filter(|s| matches!(s, Statement::Header(_)))
        .count();
    let needle = canonical::encode(&bh).unwrap();
    let store_bytes: Vec<u8> = c.store().records(&w.s).unwrap().concat();
    let export_bytes = c.export(&w.ids[c_i]).unwrap().encode().unwrap();
    eprintln!("A-B1 recheck: broadcast {r1:?}, addressed {r2:?}, forged {r3:?}, header entries sent to C {headers_in}");
    assert_eq!(headers_in, 0, "a heads-seen record to a nothing member carries headers");
    assert!(r3.is_err(), "a broadcast carrying a header was accepted: {r3:?}");
    assert!(!contains(&store_bytes, &needle) && !contains(&export_bytes, &needle), "C holds B's header");
    assert!(contains(&a.store().records(&w.s).unwrap().concat(), &needle), "positive control: A holds B's header");
}

/// A-M1 (round 1, Major): equivocation is still caught by the cross-check after an unrelated member
/// is removed (the old build refused every such record `BadSignature`).
#[test]
fn r4_fixed_a_m1_cross_check_catches_equivocation_after_a_removal() {
    let mut w = World::new(0x57, 4, 4);
    let mut b = w.audit(1, every(1_000));
    let mut c = w.audit(2, every(1_000));
    // D (3) is a member B holds a chain of; then D is removed (unrelated to A's equivocation)
    let rv1 = w.valid(1);
    let mut d = AuthorChain::new(&w.ids[3], w.s, every(1_000), Box::new(PatternRedactor), t(0));
    d.append(&w.ids[3], tiny(), t(1)).unwrap();
    let hd = d.checkpoint_now(&w.ids[3], &rv1, t(1)).unwrap();
    b.receive_head(&w.ids[1], &hd).unwrap();
    c.receive_head(&w.ids[2], &hd).unwrap();
    let r2 = w.remove(3);
    b.apply_roster(&r2).unwrap();
    c.apply_roster(&r2).unwrap();
    let rv = w.valid(2);
    let mut g = AuthorChain::new(&w.ids[0], w.s, every(1_000), Box::new(PatternRedactor), t(0));
    let mut alt = AuthorChain::new(&w.ids[0], w.s, every(1_000), Box::new(PatternRedactor), t(0));
    g.append(&w.ids[0], input("x", "one", "story"), t(1)).unwrap();
    alt.append(&w.ids[0], input("x", "another", "story"), t(1)).unwrap();
    let hg = g.checkpoint_now(&w.ids[0], &rv, t(2)).unwrap();
    let ha = alt.checkpoint_now(&w.ids[0], &rv, t(2)).unwrap();
    b.receive_head(&w.ids[1], &hg).unwrap();
    c.receive_head(&w.ids[2], &ha).unwrap();
    let hs = b.heads_seen(&w.ids[1]).unwrap();
    let r = c.receive_heads_seen(&hs);
    eprintln!("A-M1 recheck: {:?}", r.as_ref().map(|v| v.len()));
    assert!(matches!(&r, Ok(v) if !v.is_empty()), "equivocation not caught after a removal: {r:?}");
}

/// A-M2 (round 1, Major): an honest author's own export verifies after a joiner countersigns, and
/// the author applies the same rule as `verify`: a joiner may countersign the author's latest
/// checkpoint from before it joined (its anchor) and NOT an earlier one. The old build stored the
/// earlier one (current-roster check) and `verify` then refused the whole bundle.
#[test]
fn r4_fixed_a_m2_a_joiner_cannot_countersign_before_its_anchor_and_the_export_verifies() {
    let mut w = World::new(0x58, 3, 2);
    let mut a = w.audit(0, every(1_000));
    a.record(&w.ids[0], tiny(), t(1)).unwrap();
    let h1 = a.checkpoint_now(&w.ids[0], t(2)).unwrap();
    a.record(&w.ids[0], tiny(), t(3)).unwrap();
    let h2 = a.checkpoint_now(&w.ids[0], t(4)).unwrap();
    let r2 = w.add(2, 2);
    a.apply_roster(&r2).unwrap();
    let r_old = a.add_countersignature(&h1.countersign(&w.ids[2]).unwrap());
    let r_anchor = a.add_countersignature(&h2.countersign(&w.ids[2]).unwrap());
    let v = verify(&a.export(&w.ids[0]).unwrap());
    eprintln!(
        "A-M2 recheck: joiner's countersignature of an older checkpoint {r_old:?}; of its anchor {r_anchor:?}; \
         export verify {:?}",
        v.as_ref().map(|_| ())
    );
    assert_eq!(r_old, Err(AuditError::NotMember(w.key(2))), "a joiner countersigned before its anchor");
    assert!(r_anchor.is_ok(), "positive control: the anchor's countersignature was refused");
    assert!(v.is_ok(), "the author's export fails verify: {v:?}");
}

/// A-M4 (round 1, Major): a peer's checkpoints cannot grow a member's store without bound or push its
/// export past the verifier's caps. 1,500 checkpoints from one author with default limits: at most
/// the cap plus one slot are stored, and the export parses and verifies. Then the same with a tiny
/// seat: the seat stays within its limit and checkpoints are still countersigned.
#[test]
fn r4_fixed_a_m4_checkpoints_are_bounded_and_the_export_verifies() {
    for limits in [None, Some(small(4 * 1024, 64))] {
        let w = World::new(0x59, 3, 3);
        let mut v = w.audit(V, every(1_000));
        if let Some(l) = limits {
            v.set_limits(l);
        }
        let rv = w.valid(1);
        let mut a = AuthorChain::new(&w.ids[2], w.s, every(1_000), Box::new(PatternRedactor), t(0));
        let mut countersigned = 0;
        for i in 1..=1_500u64 {
            a.append(&w.ids[2], tiny(), t(i)).unwrap();
            let h = a.checkpoint_now(&w.ids[2], &rv, t(i)).unwrap();
            if v.receive_head(&w.ids[V], &h).is_ok() {
                countersigned += 1;
            }
        }
        let heads = count_part(v.store(), &w.s, |k| {
            k.author == w.key(2) && matches!(k.part, Part::PeerHead(_) | Part::Fixed(Table::LatestHead))
        });
        let b = v.export(&w.ids[V]).unwrap();
        let bytes = b.encode().unwrap();
        let ok = coagent_audit::bundle::verify_bytes(&bytes);
        eprintln!(
            "A-M4 recheck ({limits:?}): countersigned {countersigned}, stored checkpoints of the author {heads}, \
             seat {:?}, export {} bytes, verify {:?}",
            v.seat_usage(2),
            bytes.len(),
            ok.as_ref().map(|_| ())
        );
        assert_eq!(countersigned, 1_500, "a checkpoint stopped being countersigned");
        assert!(heads <= MAX_HEADS_PER_AUTHOR + 1, "{heads} checkpoints stored for one author");
        assert!(v.seat_usage(2).0 <= v.limits().per_peer().0);
        assert!(ok.is_ok());
    }
}

/// R2-M1 (round 2, Major): neither a replayed heads-seen record nor fresh records from a removed
/// member grow the store; the victim's own record still fits.
#[test]
fn r4_fixed_r2_m1_heads_seen_replays_and_removed_reporters_store_nothing() {
    let mut w = World::new(0x5a, 4, 4);
    let mut v = w.audit(V, every(1_000));
    let rv1 = w.valid(1);
    let mut a = AuthorChain::new(&w.ids[2], w.s, every(1_000), Box::new(PatternRedactor), t(0));
    a.append(&w.ids[2], tiny(), t(1)).unwrap();
    let h = a.checkpoint_now(&w.ids[2], &rv1, t(1)).unwrap();
    let hs = hs_signed(&w.ids[3], w.s, None, 1, vec![Statement::Head(h.clone())]);
    assert!(v.receive_heads_seen(&hs).is_ok());
    let base = real_size(v.store(), &w.s);
    let mut accepted = 0;
    for _ in 0..2_000 {
        if v.receive_heads_seen(&hs).is_ok() {
            accepted += 1;
        }
    }
    let after_replay = real_size(v.store(), &w.s);
    let r2 = w.remove(3);
    v.apply_roster(&r2).unwrap();
    let base2 = real_size(v.store(), &w.s);
    for i in 0..2_000u64 {
        a.append(&w.ids[2], tiny(), t(10 + i)).unwrap();
        let hi = a.checkpoint_now(&w.ids[2], &rv1, t(10 + i)).unwrap();
        let hsi = hs_signed(&w.ids[3], w.s, Some(w.key(V)), 1, vec![Statement::Head(hi)]);
        if v.receive_heads_seen(&hsi).is_ok() {
            accepted += 1;
        }
    }
    let after_removed = real_size(v.store(), &w.s);
    let own = v.record(&w.ids[V], tiny(), t(9_999));
    eprintln!("R2-M1 recheck: accepted {accepted}; store {base:?} -> {after_replay:?} (replays), {base2:?} -> {after_removed:?} (removed reporter); own {own:?}");
    assert_eq!(accepted, 0);
    assert_eq!(base, after_replay);
    assert_eq!(base2, after_removed);
    assert!(own.is_ok());
}

/// R3-M1 (round 3, Major), all three parts: (a) members flooding the starter C put nothing of C's
/// into V's store; (b) with C's seat at V FULL from C's own events, V applies the removal of a
/// hostile member and refuses its checkpoint and cross-check record after; (c) the same proxy route
/// against a NON-starter H writes nothing either.
#[test]
fn r4_fixed_r3_m1_traffic_to_one_member_cannot_spend_its_seat_at_another_and_rosters_apply() {
    let mut w = World::new(0x5b, 6, 6);
    // C = 0 (starter), V = 1, H = 2, hostiles 3..5
    let mut c = w.audit(0, every(1_000));
    let mut h = w.audit(2, every(1_000));
    let mut v = w.audit(V, every(1_000));
    v.set_limits(small(8 * 1024, 64));
    c.set_share_level(w.key(V), ShareLevel::Full);
    h.set_share_level(w.key(V), ShareLevel::Full);
    for k in 3..6usize {
        let mut x = AuthorChain::new(&w.ids[k], w.s, every(1_000), Box::new(PatternRedactor), t(0));
        for i in 1..=200u64 {
            x.append(&w.ids[k], tiny(), t(i)).unwrap();
            let _ = c.receive(&w.ids[0], x.event(i).unwrap(), t(i));
            let _ = h.receive(&w.ids[2], x.event(i).unwrap(), t(i));
        }
    }
    let (c_seq, h_seq) = (c.own().seq(), h.own().seq());
    assert_eq!((c_seq, h_seq), (0, 0), "a received event wrote into the receiver's own chain");
    // C fills its seat at V with its own events
    let mut filled = 0;
    for i in 1..10_000u64 {
        let seq = c.record(&w.ids[0], input("x", "s", "f"), t(1_000 + i)).unwrap();
        let out = c.outgoing(seq);
        let e = &out.iter().find(|(k, _)| *k == w.key(V)).unwrap().1;
        match v.receive(&w.ids[V], e, t(1_000 + i)) {
            Ok(_) => filled += 1,
            Err(AuditError::LogFull) => break,
            Err(e) => panic!("{e:?}"),
        }
    }
    let rv = w.valid(1);
    let mut x3 = AuthorChain::new(&w.ids[3], w.s, every(1_000), Box::new(PatternRedactor), t(0));
    x3.append(&w.ids[3], tiny(), t(1)).unwrap();
    let h3 = x3.checkpoint_now(&w.ids[3], &rv, t(1)).unwrap();
    let r2 = w.remove(3);
    let applied = v.apply_roster(&r2);
    let after_head = v.receive_head(&w.ids[V], &h3).map(|_| ());
    let hs3 = hs_signed(&w.ids[3], w.s, Some(w.key(V)), 1, vec![]);
    let after_hs = v.receive_heads_seen(&hs3).map(|_| ());
    eprintln!(
        "R3-M1 recheck: C's own chain after 600 received events {c_seq}, H's {h_seq}; C filled its seat at V \
         with {filled} own events ({:?}); removal {applied:?}; removed member's checkpoint {after_head:?}, \
         cross-check {after_hs:?}",
        v.seat_usage(0)
    );
    assert_eq!((c_seq, h_seq), (0, 0), "a received event wrote into the receiver's own chain");
    assert!(filled > 0);
    assert!(applied.is_ok(), "the removal was refused with the starter's seat full: {applied:?}");
    assert!(after_head.is_err() && after_hs.is_err());
}

// =================================================================================================
// Own property harness: the storage accounting under generated schedules
// =================================================================================================

#[derive(Debug, Clone)]
enum Op {
    Ev { k: u8, size: u8, n: u8 },
    Head { k: u8, extra: u8 },
    Fork { k: u8, head: bool },
    Replay { k: u8 },
    Own { size: u8, n: u8 },
    For { k: u8, size: u8, n: u8 },
    Ckpt,
    Cs { k: u8, held: bool },
    Hs { k: u8, about: u8, to_me: bool },
    Remove { k: u8 },
    Readd { k: u8 },
    NewKey,
    Release { k: u8 },
    Resume,
    RosterReplay,
    Outsider { what: u8 },
}

fn op() -> impl Strategy<Value = Op> {
    prop_oneof![
        8 => (any::<u8>(), 0u8..3, 1u8..6).prop_map(|(k, size, n)| Op::Ev { k, size, n }),
        3 => (any::<u8>(), 0u8..3).prop_map(|(k, extra)| Op::Head { k, extra }),
        2 => (any::<u8>(), any::<bool>()).prop_map(|(k, head)| Op::Fork { k, head }),
        1 => any::<u8>().prop_map(|k| Op::Replay { k }),
        4 => (0u8..3, 1u8..6).prop_map(|(size, n)| Op::Own { size, n }),
        3 => (any::<u8>(), 0u8..3, 1u8..6).prop_map(|(k, size, n)| Op::For { k, size, n }),
        2 => Just(Op::Ckpt),
        2 => (any::<u8>(), any::<bool>()).prop_map(|(k, held)| Op::Cs { k, held }),
        2 => (any::<u8>(), any::<u8>(), any::<bool>()).prop_map(|(k, about, to_me)| Op::Hs { k, about, to_me }),
        2 => any::<u8>().prop_map(|k| Op::Remove { k }),
        1 => any::<u8>().prop_map(|k| Op::Readd { k }),
        1 => Just(Op::NewKey),
        2 => any::<u8>().prop_map(|k| Op::Release { k }),
        2 => Just(Op::Resume),
        1 => Just(Op::RosterReplay),
        1 => (0u8..3).prop_map(|what| Op::Outsider { what }),
    ]
}

#[derive(Debug, Clone)]
struct PCase {
    members: usize,
    seat_bytes: usize,
    seat_records: usize,
    ops: Vec<Op>,
}

fn pcase() -> impl Strategy<Value = PCase> {
    (
        3usize..=8,
        prop_oneof![1_500usize..6_000, 6_000usize..40_000],
        prop_oneof![3usize..12, 12usize..80],
        prop::collection::vec(op(), 20..90),
    )
        .prop_map(|(members, seat_bytes, seat_records, ops)| PCase {
            members,
            seat_bytes,
            seat_records,
            ops,
        })
}

thread_local! {
    static RULES: RefCell<BTreeMap<&'static str, u64>> = const { RefCell::new(BTreeMap::new()) };
}

fn hit(rule: &'static str) {
    RULES.with(|r| *r.borrow_mut().entry(rule).or_default() += 1);
}

const N_IDS: usize = 13;
const OUTSIDER: usize = 12;

struct Harness {
    w: World,
    v: SessionAudit<MemStore>,
    limits: StoreLimits,
    chains: BTreeMap<usize, AuthorChain>,
    ever: BTreeSet<usize>,
    released: BTreeSet<usize>,
    acked_peer: BTreeSet<(usize, u64)>,
    acked_own: BTreeSet<u64>,
    forks: u32,
    now: u64,
}

fn fail(msg: String) -> Result<(), TestCaseError> {
    Err(TestCaseError::fail(msg))
}

fn event_input(size: u8, big_s: &str, big_f: &str) -> (String, String, bool) {
    match size {
        0 => (String::new(), String::new(), false),
        1 => ("s".repeat(200), "f".repeat(1_000), true),
        _ => (big_s.to_string(), big_f.to_string(), true),
    }
}

impl Harness {
    fn new(c: &PCase) -> Harness {
        let w = World::new(0x60, N_IDS, c.members);
        let limits = small(c.seat_bytes, c.seat_records);
        let mut v = w.audit(V, every(1_000_000));
        v.set_limits(limits);
        let ever = (0..c.members).collect();
        Harness {
            w,
            v,
            limits,
            chains: BTreeMap::new(),
            ever,
            released: BTreeSet::new(),
            acked_peer: BTreeSet::new(),
            acked_own: BTreeSet::new(),
            forks: 0,
            now: 0,
        }
    }

    fn tick(&mut self) -> coagent_audit::time::AuditTime {
        self.now += 1;
        t(self.now)
    }

    /// (index, slot) of current members.
    fn members(&self) -> Vec<(usize, u8)> {
        let last = self.w.rosters.last().unwrap();
        last.body
            .members
            .iter()
            .map(|m| (self.w.ids.iter().position(|d| d.key_id() == m.key_id).unwrap(), m.slot))
            .collect()
    }

    fn peers(&self) -> Vec<usize> {
        self.members().into_iter().map(|(i, _)| i).filter(|i| *i != V).collect()
    }

    fn removed(&self) -> Vec<usize> {
        let cur: BTreeSet<usize> = self.members().into_iter().map(|(i, _)| i).collect();
        self.ever.iter().copied().filter(|i| !cur.contains(i) && *i != V).collect()
    }

    fn chain(&mut self, k: usize) -> &mut AuthorChain {
        let w = &self.w;
        self.chains.entry(k).or_insert_with(|| {
            AuthorChain::new(&w.ids[k], w.s, every(1_000_000), Box::new(PatternRedactor), t(0))
        })
    }

    fn store_list(&self) -> Vec<(StoreKey, Vec<u8>)> {
        self.v.store().list(&self.w.s).unwrap()
    }

    fn step(&mut self, op: &Op) -> Result<(), TestCaseError> {
        let big_s = "S".repeat(4000);
        let big_f = "F".repeat(60_000);
        let before = self.store_list();
        // refusals that must leave the store byte-identical
        let mut must_be_unchanged = false;
        match op {
            Op::Ev { k, size, n } => {
                let peers = self.peers();
                if peers.is_empty() {
                    return Ok(());
                }
                let k = peers[*k as usize % peers.len()];
                for _ in 0..*n {
                    let before = self.store_list();
                    let next = self.v.peer(&self.w.key(k)).map_or(1, |c| c.next_seq());
                    let (s, f, tiers) = event_input(*size, &big_s, &big_f);
                    let now = self.tick();
                    let id = fixed_identity(0x60 + k as u8);
                    let ch = self.chain(k);
                    while ch.seq() < next {
                        let inp = if tiers {
                            input("x", &s, &f)
                        } else {
                            tiny()
                        };
                        ch.append(&id, inp, now).unwrap();
                    }
                    let e = ch.event(next).unwrap().clone();
                    let r = self.v.receive(&self.w.ids[V], &e, now);
                    match r {
                        Ok(_) => {
                            self.acked_peer.insert((k, next));
                            hit(if *size == 2 { "peer event accepted (max size)" } else { "peer event accepted" });
                        }
                        Err(AuditError::LogFull) => {
                            hit("peer event refused: seat full");
                            if self.store_list() != before {
                                return fail(format!("a LogFull refusal changed the store (author {k})"));
                            }
                            break;
                        }
                        Err(e) => {
                            hit("peer event refused: other");
                            if self.store_list() != before {
                                return fail(format!("a refused event ({e:?}) changed the store"));
                            }
                            break;
                        }
                    }
                }
            }
            Op::Head { k, extra } => {
                let peers = self.peers();
                if peers.is_empty() {
                    return Ok(());
                }
                let k = peers[*k as usize % peers.len()];
                let now = self.tick();
                let id = fixed_identity(0x60 + k as u8);
                let rv = self.v.roster().clone();
                let ch = self.chain(k);
                for _ in 0..=*extra {
                    ch.append(&id, tiny(), now).unwrap();
                }
                let h = ch.checkpoint_now(&id, &rv, now).unwrap();
                let latest_before = before.iter().any(|(key, _)| key.part == Part::Fixed(Table::LatestHead) && key.author == id.key_id());
                match self.v.receive_head(&self.w.ids[V], &h) {
                    Ok(_) => {
                        let latest = self.store_list().iter().any(|(key, _)| key.part == Part::Fixed(Table::LatestHead) && key.author == id.key_id());
                        hit(if latest && !latest_before { "checkpoint to the latest slot (seat full)" } else if latest { "checkpoint replaces the latest slot" } else { "checkpoint logged in seat" });
                    }
                    Err(_) => {
                        hit("checkpoint refused");
                        must_be_unchanged = true;
                    }
                }
            }
            Op::Fork { k, head } => {
                let peers = self.peers();
                let held: Vec<usize> = peers
                    .into_iter()
                    .filter(|k| {
                        self.v.peer(&self.w.key(*k)).is_some_and(|c| c.event(1).is_some())
                    })
                    .collect();
                if held.is_empty() {
                    return Ok(());
                }
                let k = held[*k as usize % held.len()];
                self.forks += 1;
                let now = self.tick();
                let id = fixed_identity(0x60 + k as u8);
                let mut alt = AuthorChain::new(&id, self.w.s, every(1_000_000), Box::new(PatternRedactor), t(0));
                let kind = format!("fork{}", self.forks);
                alt.append(&id, EventInput { kind: &kind, summary: None, full: None }, now).unwrap();
                let accused = id.key_id();
                let ev_before = before.iter().filter(|(key, _)| key.part == Part::Fixed(Table::Evidence) && key.author == accused).count();
                let r = if *head {
                    let rv = self.v.roster().clone();
                    let h = alt.checkpoint_now(&id, &rv, now).unwrap();
                    self.v.receive_head(&self.w.ids[V], &h).map(|_| ())
                } else {
                    self.v.receive(&self.w.ids[V], alt.event(1).unwrap(), now).map(|_| ())
                };
                let ev_after = self.store_list().iter().filter(|(key, _)| key.part == Part::Fixed(Table::Evidence) && key.author == accused).count();
                match r {
                    Err(AuditError::Receive(ReceiveError::Fork(_))) => {
                        if ev_before < 4 && ev_after != ev_before + 1 {
                            return fail(format!("fork evidence not stored: {ev_before} -> {ev_after}"));
                        }
                        if ev_before >= 4 {
                            hit("evidence cap reached: returned, not stored");
                            if ev_after != ev_before {
                                return fail("a fifth evidence record was stored".into());
                            }
                        } else {
                            hit("fork evidence stored");
                        }
                        let changed: BTreeSet<Part> = self.store_list().into_iter().filter(|x| !before.contains(x)).map(|(key, _)| key.part).collect();
                        if changed.iter().any(|p| *p != Part::Fixed(Table::Evidence)) {
                            return fail(format!("a fork stored something besides evidence: {changed:?}"));
                        }
                    }
                    other => return fail(format!("a conflicting statement was not answered Fork: {other:?}")),
                }
            }
            Op::Replay { k } => {
                let cand: Vec<(usize, u64)> = self.acked_peer.iter().copied().collect();
                if cand.is_empty() {
                    return Ok(());
                }
                let (k, seq) = cand[*k as usize % cand.len()];
                let e = self.chains[&k].event(seq).unwrap().clone();
                let now = self.tick();
                let r = self.v.receive(&self.w.ids[V], &e, now);
                if r.is_ok() {
                    return fail(format!("a replayed event was accepted again ({k}, {seq})"));
                }
                hit("replay refused");
                must_be_unchanged = true;
            }
            Op::Own { size, n } => {
                for _ in 0..*n {
                    let (s, f, tiers) = event_input(*size, &big_s, &big_f);
                    let inp = if tiers { input("x", &s, &f) } else { tiny() };
                    let now = self.tick();
                    let before = self.store_list();
                    match self.v.record(&self.w.ids[V], inp, now) {
                        Ok(seq) => {
                            self.acked_own.insert(seq);
                            hit("own free record accepted");
                        }
                        Err(AuditError::LogFull) => {
                            hit("own free record refused: free part full");
                            if self.store_list() != before {
                                return fail("a refused own record changed the store".into());
                            }
                            break;
                        }
                        Err(e) => return fail(format!("own record: {e:?}")),
                    }
                }
            }
            Op::For { k, size, n } => {
                let peers = self.peers();
                let causer = if peers.is_empty() || *k % 11 == 0 {
                    OUTSIDER
                } else {
                    peers[*k as usize % peers.len()]
                };
                for _ in 0..*n {
                    let (s, f, tiers) = event_input(*size, &big_s, &big_f);
                    let inp = if tiers { input("x", &s, &f) } else { tiny() };
                    let now = self.tick();
                    let before = self.store_list();
                    match self.v.record_for(&self.w.ids[V], &self.w.key(causer), inp, now) {
                        Ok(seq) => {
                            self.acked_own.insert(seq);
                            hit("requested record accepted");
                        }
                        Err(AuditError::LogFull) => {
                            hit("requested record refused: allowance full");
                            if self.store_list() != before {
                                return fail("a refused requested record changed the store".into());
                            }
                            break;
                        }
                        Err(AuditError::NotMember(_)) if causer == OUTSIDER => {
                            hit("requested record refused: causer not a member");
                            break;
                        }
                        Err(e) => return fail(format!("record_for: {e:?}")),
                    }
                }
            }
            Op::Ckpt => {
                let now = self.tick();
                match self.v.checkpoint_now(&self.w.ids[V], now) {
                    Ok(_) => hit("own checkpoint"),
                    Err(AuditError::LogFull) => {
                        hit("own checkpoint refused: full");
                        must_be_unchanged = true;
                    }
                    Err(_) => must_be_unchanged = true,
                }
            }
            Op::Cs { k, held } => {
                let peers = self.peers();
                let Some(head) = self.v.own().checkpoints().last().map(|c| c.head.clone()) else {
                    return Ok(());
                };
                if peers.is_empty() {
                    return Ok(());
                }
                let k = peers[*k as usize % peers.len()];
                let had = before.iter().any(|(key, _)| key.part == Part::Fixed(Table::Attestation) && key.author == self.w.key(k));
                let cs = head.countersign_held(&self.w.ids[k], if *held { Some(1) } else { None }).unwrap();
                match self.v.add_countersignature(&cs) {
                    Ok(()) => hit(if had { "attestation replaced or replayed" } else { "attestation stored" }),
                    Err(_) => {
                        hit("countersignature refused");
                        must_be_unchanged = true;
                    }
                }
            }
            Op::Hs { k, about, to_me } => {
                let peers = self.peers();
                if peers.is_empty() {
                    return Ok(());
                }
                let k = peers[*k as usize % peers.len()];
                let heads: Vec<SignedHead> = self
                    .chains
                    .iter()
                    .filter(|(j, _)| **j != k)
                    .filter_map(|(_, c)| c.checkpoints().last().map(|x| x.head.clone()))
                    .collect();
                let entries = if heads.is_empty() {
                    vec![]
                } else {
                    vec![Statement::Head(heads[*about as usize % heads.len()].clone())]
                };
                let rv = self.v.roster().version();
                let to = if *to_me { Some(self.w.key(V)) } else { None };
                let hs = hs_signed(&self.w.ids[k], self.w.s, to, rv, entries);
                let had = before.iter().any(|(key, _)| key.part == Part::Fixed(Table::HeadsSeen) && key.author == self.w.key(k));
                match self.v.receive_heads_seen(&hs) {
                    Ok(ev) if ev.is_empty() => hit(if had { "cross-check slot replaced" } else { "cross-check slot stored" }),
                    Ok(_) => hit("cross-check revealed evidence"),
                    Err(_) => {
                        hit("cross-check refused (not newer, duplicate)");
                        must_be_unchanged = true;
                    }
                }
            }
            Op::Remove { k } => {
                let peers: Vec<usize> = self.peers().into_iter().filter(|i| *i != 0).collect();
                if peers.is_empty() {
                    return Ok(());
                }
                let k = peers[*k as usize % peers.len()];
                let full = (0..8u8).any(|s| {
                    let u = self.v.seat_usage(s);
                    u.0 + 600 > self.limits.per_peer().0 || u.1 + 1 >= self.limits.per_peer().1
                });
                let r = self.w.remove(k);
                let a = self.v.apply_roster(&r);
                if !a.is_ok() {
                    return fail(format!("a valid removal was refused: {a:?}"));
                }
                hit(if full { "roster applied with a seat (nearly) full" } else { "roster applied" });
            }
            Op::Readd { k } => {
                let removed: Vec<usize> = self.removed();
                let used: BTreeSet<u8> = self.members().into_iter().map(|(_, s)| s).collect();
                let free: Vec<u8> = (0..8u8).filter(|s| !used.contains(s)).collect();
                if removed.is_empty() || free.is_empty() {
                    return Ok(());
                }
                let k = removed[*k as usize % removed.len()];
                let r = self.w.add(k, free[0]);
                match self.v.apply_roster(&r) {
                    Ok(_) => hit("re-added a removed key"),
                    Err(AuditError::RosterLifetime) => {
                        self.w.rosters.pop();
                        hit("roster lifetime backstop");
                    }
                    Err(e) => return fail(format!("a valid re-add was refused: {e:?}")),
                }
            }
            Op::NewKey => {
                let used: BTreeSet<u8> = self.members().into_iter().map(|(_, s)| s).collect();
                let free: Vec<u8> = (0..8u8).filter(|s| !used.contains(s)).collect();
                let fresh = (8..OUTSIDER).find(|i| !self.ever.contains(i));
                let (Some(slot), Some(k)) = (free.first().copied(), fresh) else {
                    return Ok(());
                };
                let used_before = self.store_list().iter().any(|(key, _)| matches!(key.part, Part::PeerEvent(s) | Part::PeerHead(s) if s == slot));
                let r = self.w.add(k, slot);
                match self.v.apply_roster(&r) {
                    Ok(_) => {
                        self.ever.insert(k);
                        hit(if used_before { "new key into a slot whose seat holds records" } else { "new key into a free slot" });
                    }
                    Err(e) => return fail(format!("a valid add was refused: {e:?}")),
                }
            }
            Op::Release { k } => {
                let cand: Vec<usize> = self.removed().into_iter().filter(|i| !self.released.contains(i)).collect();
                if cand.is_empty() {
                    // a current member must be refused
                    let peers = self.peers();
                    if let Some(p) = peers.first() {
                        let r = self.v.archive_and_release(&self.w.ids[V], &self.w.key(*p));
                        if r.is_ok() {
                            return fail("release of a current member was accepted".into());
                        }
                        hit("release of a current member refused");
                        must_be_unchanged = true;
                    }
                } else {
                    let k = cand[*k as usize % cand.len()];
                    let key = self.w.key(k);
                    let charge: (usize, usize) = before.iter().filter(|(sk, _)| sk.author == key && matches!(sk.part, Part::PeerEvent(_) | Part::PeerHead(_))).fold((0, 0), |a, (_, r)| (a.0 + 4 + r.len(), a.1 + 1));
                    let total_before = real_size(self.v.store(), &self.w.s);
                    let b: Bundle = match self.v.archive_and_release(&self.w.ids[V], &key) {
                        Ok(b) => b,
                        Err(e) => return fail(format!("release of a removed key failed: {e:?}")),
                    };
                    if let Err(e) = verify(&b) {
                        return fail(format!("the archive file from a release fails verify: {e:?}"));
                    }
                    let in_file: BTreeSet<u64> = b.peers.iter().filter(|p| p.author == key).flat_map(|p| p.events.iter().map(|e| e.header.author_seq)).collect();
                    for (a, seq) in self.acked_peer.clone() {
                        if a == k {
                            if !in_file.contains(&seq) {
                                return fail(format!("an acknowledged event ({k}, {seq}) is not in the release's file"));
                            }
                            self.acked_peer.remove(&(a, seq));
                        }
                    }
                    let left = count_part(self.v.store(), &self.w.s, |sk| sk.author == key && matches!(sk.part, Part::PeerEvent(_) | Part::PeerHead(_)));
                    if left != 0 {
                        return fail(format!("release left {left} records of the key"));
                    }
                    let total_after = real_size(self.v.store(), &self.w.s);
                    // the tombstone may add or replace one anchor slot
                    let freed = total_before.0 as i64 - total_after.0 as i64;
                    if freed + 600 < charge.0 as i64 && charge.0 > 0 {
                        return fail(format!("release freed {freed}, not the key's charge {charge:?}"));
                    }
                    self.released.insert(k);
                    hit(if charge.1 > 0 { "release of a removed key with records" } else { "release of a removed key (empty)" });
                }
            }
            Op::Resume => {
                let st0 = self.v.status();
                let ex0 = self.v.export(&self.w.ids[V]).unwrap().encode().unwrap();
                let now = self.tick();
                let mut r = match SessionAudit::resume(
                    self.v.store().clone(),
                    self.w.s,
                    &self.w.ids[V],
                    &self.w.ids[0].verified(),
                    every(1_000_000),
                    Box::new(PatternRedactor),
                    now,
                ) {
                    Ok(r) => r,
                    Err(e) => return fail(format!("resume refused a store this member wrote: {e:?}")),
                };
                r.set_limits(self.limits);
                let st1 = r.status();
                let ex1 = r.export(&self.w.ids[V]).unwrap().encode().unwrap();
                if st0 != st1 {
                    return fail(format!("resume: status differs:\n before {st0:?}\n after  {st1:?}"));
                }
                if ex0 != ex1 {
                    return fail("resume: the export differs".into());
                }
                self.v = r;
                hit("resume");
            }
            Op::RosterReplay => {
                let last = self.w.rosters.last().unwrap().clone();
                let r = self.v.apply_roster(&last);
                if !matches!(r, Ok(coagent_roster::Applied::Unchanged)) {
                    return fail(format!("replaying the held version did not give Unchanged: {r:?}"));
                }
                hit("roster replay");
                must_be_unchanged = true;
            }
            Op::Outsider { what } => {
                let id = fixed_identity(0x60 + OUTSIDER as u8);
                let now = self.tick();
                let rv = self.v.roster().clone();
                let mut ch = AuthorChain::new(&id, self.w.s, every(1_000_000), Box::new(PatternRedactor), t(0));
                ch.append(&id, tiny(), now).unwrap();
                let r = match what {
                    0 => self.v.receive(&self.w.ids[V], ch.event(1).unwrap(), now).map(|_| ()),
                    1 => {
                        let h = ch.checkpoint_now(&id, &rv, now).unwrap();
                        self.v.receive_head(&self.w.ids[V], &h).map(|_| ())
                    }
                    _ => {
                        let hs = hs_signed(&id, self.w.s, None, rv.version(), vec![]);
                        self.v.receive_heads_seen(&hs).map(|_| ())
                    }
                };
                if r.is_ok() {
                    return fail(format!("an outsider's object was accepted ({what})"));
                }
                hit("outsider refused");
                must_be_unchanged = true;
            }
        }
        if must_be_unchanged && self.store_list() != before {
            return fail(format!("a refused or no-op input changed the store: {op:?}"));
        }
        self.check()
    }

    fn check(&self) -> Result<(), TestCaseError> {
        let v = &self.v;
        let list = self.store_list();
        let real: (usize, usize) = (list.iter().map(|(_, r)| 4 + r.len()).sum(), list.len());
        // I1: the accounting equals the store
        if v.store_usage() != real {
            return fail(format!("I1: store_usage {:?} but the store holds {real:?}", v.store_usage()));
        }
        let st = v.status();
        let seats: (usize, usize) = (0..8u8).fold((0, 0), |a, s| {
            let u = v.seat_usage(s);
            (a.0 + u.0, a.1 + u.1)
        });
        let fixed: (usize, usize) = st.fixed.iter().fold((0, 0), |a, (_, (n, _), (b, _))| (a.0 + b, a.1 + n));
        if (seats.0 + fixed.0, seats.1 + fixed.1) != real {
            return fail(format!("I2: seats {seats:?} + fixed {fixed:?} != store {real:?}"));
        }
        // I3: every seat and part within its limit
        let me = st.own_slot;
        for s in 0..8u8 {
            let u = v.seat_usage(s);
            let lim = if s == me { self.limits.own_reserved() } else { self.limits.per_peer() };
            if u.0 > lim.0 || u.1 > lim.1 {
                return fail(format!("I3: seat {s} holds {u:?}, above its limit {lim:?}"));
            }
            let rq = v.requested_usage(s);
            let al = self.limits.requested_allowance();
            if rq.0 > al.0 || rq.1 > al.1 {
                return fail(format!("I3: requested allowance {s} holds {rq:?} above {al:?}"));
            }
        }
        let fu = v.free_usage();
        let fl = self.limits.free_part();
        if fu.0 > fl.0 || fu.1 > fl.1 {
            return fail(format!("I3: free part {fu:?} above {fl:?}"));
        }
        // I4: fixed tables within slots and slot maxima; seat records within the record cap
        for (t_, (n, slots), (b, set)) in &st.fixed {
            if n > slots || b > set {
                return fail(format!("I4: fixed table {t_:?} uses {n}/{slots} slots, {b}/{set} bytes"));
            }
        }
        for (k, r) in &list {
            let max = match k.part {
                Part::Fixed(t_) => t_.slot_max(),
                _ => 4 + MAX_RECORD_BYTES,
            };
            if 4 + r.len() > max {
                return fail(format!("I4: a record in {:?} is {} bytes, above {max}", k.part, 4 + r.len()));
            }
            // the key says what the record is
            let rec: Record = canonical::decode(r).unwrap();
            let ok = matches!(
                (k.part, &rec),
                (Part::Fixed(Table::Roster), Record::Roster(_))
                    | (Part::Fixed(Table::RosterConflict), Record::RosterConflict(_))
                    | (Part::Fixed(Table::Evidence), Record::Evidence(_))
                    | (Part::Fixed(Table::Attestation), Record::Countersig(_))
                    | (Part::Fixed(Table::HeadsSeen), Record::HeadsSeen(_))
                    | (Part::Fixed(Table::Anchor), Record::PeerStart(_))
                    | (Part::Fixed(Table::LatestHead), Record::PeerHead(_))
                    | (Part::OwnEvent(_), Record::OwnEvent(_))
                    | (Part::OwnHead, Record::OwnHead(_))
                    | (Part::PeerEvent(_), Record::PeerEvent(_))
                    | (Part::PeerHead(_), Record::PeerHead(_))
            );
            if !ok {
                return fail(format!("I4: key part {:?} holds another kind of record", k.part));
            }
        }
        // I5: total within the capacity
        if real.0 > CAPACITY_BYTES || real.1 > CAPACITY_RECORDS {
            return fail(format!("I5: store {real:?} above the capacity"));
        }
        // I6: nothing acknowledged is lost
        for (k, seq) in &self.acked_peer {
            let key = self.w.key(*k);
            if !list.iter().any(|(sk, _)| sk.author == key && sk.n == *seq && matches!(sk.part, Part::PeerEvent(_))) {
                return fail(format!("I6: acknowledged event ({k}, {seq}) is not in the store"));
            }
        }
        for seq in &self.acked_own {
            if !list.iter().any(|(sk, _)| sk.author == self.w.key(V) && sk.n == *seq && matches!(sk.part, Part::OwnEvent(_))) {
                return fail(format!("I6: acknowledged own event {seq} is not in the store"));
            }
        }
        // I7: the export verifies
        let b = match v.export(&self.w.ids[V]) {
            Ok(b) => b,
            Err(e) => return fail(format!("I7: export failed: {e:?}")),
        };
        if let Err(e) = verify(&b) {
            return fail(format!("I7: the export fails verify: {e:?}"));
        }
        Ok(())
    }
}

fn run_pcase(c: &PCase) -> Result<(), TestCaseError> {
    let mut h = Harness::new(c);
    h.check()?;
    for (i, op) in c.ops.iter().enumerate() {
        h.step(op).map_err(|e| TestCaseError::fail(format!("step {i} {op:?}: {e}")))?;
    }
    Ok(())
}

fn run_prop(cases: u32) -> BTreeMap<&'static str, u64> {
    RULES.with(|r| r.borrow_mut().clear());
    let mut runner = TestRunner::new_with_rng(
        Config {
            cases,
            max_shrink_iters: 200,
            failure_persistence: None,
            ..Config::default()
        },
        proptest::test_runner::TestRng::deterministic_rng(proptest::test_runner::RngAlgorithm::ChaCha),
    );
    if let Err(e) = runner.run(&pcase(), |c| run_pcase(&c)) {
        panic!("r4 property failed: {e}");
    }
    RULES.with(|r| r.borrow().clone())
}

/// The class the three earlier gates found, as one property over generated schedules: after every
/// step, the accounting equals the store (I1, I2), every seat, allowance and free part is within its
/// limit (I3), every fixed table within its slots and every record within its kind's maximum and
/// under the key of its kind (I4), the store within the capacity (I5), nothing acknowledged lost
/// (I6), and the export verifies (I7); a refused input leaves the store byte-identical; a valid
/// roster version is never refused; a fork always yields stored evidence until the cap; a resume is
/// indistinguishable (status and export bytes). Every rule's path count is printed and must be > 0.
#[test]
fn r4_prop_storage_accounting() {
    let cases: u32 = std::env::var("R4_CASES").ok().and_then(|s| s.parse().ok()).unwrap_or(64);
    let rules = run_prop(cases);
    eprintln!("r4 property: {cases} cases; rule path counts:");
    for (k, n) in &rules {
        eprintln!("  {n:>7}  {k}");
    }
    let needed = [
        "peer event accepted",
        "peer event accepted (max size)",
        "peer event refused: seat full",
        "checkpoint logged in seat",
        "checkpoint to the latest slot (seat full)",
        "fork evidence stored",
        "evidence cap reached: returned, not stored",
        "replay refused",
        "own free record accepted",
        "own free record refused: free part full",
        "requested record accepted",
        "requested record refused: allowance full",
        "requested record refused: causer not a member",
        "own checkpoint",
        "attestation stored",
        "attestation replaced or replayed",
        "cross-check slot stored",
        "cross-check slot replaced",
        "roster applied",
        "roster applied with a seat (nearly) full",
        "re-added a removed key",
        "new key into a slot whose seat holds records",
        "release of a removed key with records",
        "release of a current member refused",
        "resume",
        "roster replay",
        "outsider refused",
    ];
    let missing: Vec<&&str> = needed.iter().filter(|k| !rules.contains_key(**k)).collect();
    assert!(missing.is_empty(), "r4 coverage: rule paths never reached: {missing:?}");
}

// =================================================================================================
// Hostile or damaged store: every single-byte flip, truncation and deletion of a stored record
// =================================================================================================

/// A member's store with every record kind: own events and checkpoints, countersignatures, peer
/// events and checkpoints, a cross-check record, evidence, roster versions.
fn rich_member() -> (World, SessionAudit<MemStore>) {
    let mut w = World::new(0x5c, 4, 4);
    let mut v = w.audit(V, every(1_000));
    let rv = w.valid(1);
    let mut a = AuthorChain::new(&w.ids[2], w.s, every(1_000), Box::new(PatternRedactor), t(0));
    for i in 1..=3u64 {
        a.append(&w.ids[2], input("x", "sum", "full body"), t(i)).unwrap();
        v.receive(&w.ids[V], a.event(i).unwrap(), t(i)).unwrap();
    }
    let h = a.checkpoint_now(&w.ids[2], &rv, t(4)).unwrap();
    v.receive_head(&w.ids[V], &h).unwrap();
    for i in 0..3u64 {
        v.record(&w.ids[V], input("x", "mine", "my full"), t(10 + i)).unwrap();
    }
    let oh = v.checkpoint_now(&w.ids[V], t(20)).unwrap();
    v.add_countersignature(&oh.countersign_held(&w.ids[3], Some(1)).unwrap()).unwrap();
    let hs = hs_signed(&w.ids[3], w.s, Some(w.key(V)), 1, vec![Statement::Head(h)]);
    v.receive_heads_seen(&hs).unwrap();
    let mut alt = AuthorChain::new(&w.ids[2], w.s, every(1_000), Box::new(PatternRedactor), t(0));
    alt.append(&w.ids[2], input("y", "other", "story"), t(1)).unwrap();
    assert!(v.receive(&w.ids[V], alt.event(1).unwrap(), t(30)).is_err());
    let r2 = w.remove(3);
    v.apply_roster(&r2).unwrap();
    (w, v)
}

fn resume_from(w: &World, st: MemStore) -> Result<SessionAudit<MemStore>, AuditError> {
    SessionAudit::resume(
        st,
        w.s,
        &w.ids[V],
        &w.ids[0].verified(),
        every(1_000),
        Box::new(PatternRedactor),
        t(99),
    )
}

/// Every stored record damaged one way at a time (a bit flipped at many positions, cut short,
/// removed). Outcomes: `resume` refuses (fail closed); `resume` takes it but the export `verify`
/// refuses (reported at export); or SILENT: resume takes it AND the export verifies with content
/// that differs from the original. Silent cases are printed by record kind and position.
#[test]
fn r4_damaged_store_fails_closed_or_is_reported() {
    let (w, v) = rich_member();
    let orig = v.store().list(&w.s).unwrap();
    let orig_export = v.export(&w.ids[V]).unwrap().encode().unwrap();
    let (mut closed, mut at_export, mut benign) = (0usize, 0usize, 0usize);
    let mut silent: Vec<String> = Vec::new();
    let mut kinds: BTreeMap<String, usize> = BTreeMap::new();
    let mut try_store = |label: String, recs: Vec<(StoreKey, Vec<u8>)>, part: Part| {
        let mut st = MemStore::new();
        for (k, r) in &recs {
            st.put(&w.s, k, r).unwrap();
        }
        *kinds.entry(format!("{part:?}")).or_default() += 1;
        match resume_from(&w, st) {
            Err(_) => closed += 1,
            Ok(r) => match r.export(&w.ids[V]).map(|b| (verify(&b).is_ok(), b.encode().unwrap())) {
                Err(_) | Ok((false, _)) => at_export += 1,
                Ok((true, bytes)) if bytes == orig_export => benign += 1,
                Ok((true, _)) => silent.push(format!("{label} in {part:?}")),
            },
        }
    };
    for (i, (k, r)) in orig.iter().enumerate() {
        let mut positions: BTreeSet<usize> = (0..r.len()).step_by(7).collect();
        positions.insert(r.len() - 1);
        for p in positions {
            let mut recs = orig.clone();
            recs[i].1[p] ^= 0x01;
            try_store(format!("flip byte {p}/{}", r.len()), recs, k.part);
        }
        let mut recs = orig.clone();
        recs[i].1.truncate(r.len() / 2);
        try_store("cut to half".into(), recs, k.part);
        let mut recs = orig.clone();
        recs.remove(i);
        try_store(format!("record removed (key n={}, of {} records)", k.n, orig.len()), recs, k.part);
    }
    eprintln!(
        "damaged store: {} records; outcomes: resume refused {closed}, export refused {at_export}, \
         identical export {benign}, SILENT {}; cases per part {kinds:?}",
        orig.len(),
        silent.len()
    );
    let mut by: BTreeMap<String, usize> = BTreeMap::new();
    for s in &silent {
        let key = s.split(" in ").nth(1).unwrap_or("").to_string() + " / " + s.split(' ').next().unwrap_or("");
        *by.entry(key).or_default() += 1;
    }
    eprintln!("silent cases by part and damage: {by:?}");
    for s in silent.iter().take(12) {
        eprintln!("  silent: {s}");
    }
    assert!(closed + at_export > 0, "control: no damage was ever detected");
    // Flips and truncations: never silent. Whole-record deletions: the R4-m3 finding (printed above;
    // the first run of this test asserted `silent.is_empty()` and went red on exactly these).
    let not_deletion: Vec<&String> = silent.iter().filter(|s| !s.starts_with("record removed")).collect();
    assert!(not_deletion.is_empty(), "damaged (not deleted) records taken silently: {not_deletion:?}");
    assert!(!silent.is_empty(), "R4-m3 not shown: no deleted record was taken silently");
}

fn head_raw(w: &World, k: usize, seq: u64, rv: u64) -> SignedHead {
    let body = coagent_audit::checkpoint::HeadBody {
        session_id: w.s,
        author: w.key(k),
        author_seq: seq,
        hash: coagent_proto::bytes::Digest32([7; 32]),
        roster_v: rv,
    };
    let sig = audit_sign(&w.ids[k], AuditDomain::Head, &canonical::encode(&body).unwrap());
    SignedHead {
        session_id: body.session_id,
        author: body.author,
        author_seq: body.author_seq,
        hash: body.hash,
        roster_v: body.roster_v,
        sig,
    }
}

/// Bounds on numbers a member signs: extreme sequence numbers, roster versions and `held_from`
/// values on every new path (checkpoint slot, held_from, cross-check slot, status) are refused or
/// stored without arithmetic overflow (debug build: overflow panics), and the accounting holds.
#[test]
fn r4_extreme_numbers_on_the_new_paths_never_panic_and_store_within_bounds() {
    let w = World::new(0x5d, 3, 3);
    let mut v = w.audit(V, every(1_000));
    v.record(&w.ids[V], tiny(), t(1)).unwrap();
    let oh = v.checkpoint_now(&w.ids[V], t(2)).unwrap();
    v.set_limits(small(2_048, 4));
    let mut out = Vec::new();
    for seq in [0u64, 1, (1u64 << 62) - 1, 1u64 << 62, (1u64 << 62) + 1, u64::MAX] {
        for rv in [0u64, 1, 2, u64::MAX] {
            let h = head_raw(&w, 2, seq, rv);
            out.push(format!("head {seq}/{rv}: {:?}", v.receive_head(&w.ids[V], &h).map(|c| c.held_from)));
            let hs = hs_signed(&w.ids[2], w.s, Some(w.key(V)), rv, vec![Statement::Head(head_raw(&w, 0, seq, 1))]);
            out.push(format!("hs {seq}/{rv}: {:?}", v.receive_heads_seen(&hs).map(|e| e.len())));
        }
    }
    for held in [Some(0u64), Some(1), Some(2), Some(u64::MAX), None] {
        let cs = oh.countersign_held(&w.ids[2], held).unwrap();
        out.push(format!("cs held {held:?}: {:?}", v.add_countersignature(&cs)));
    }
    let st = v.status();
    let real = real_size(v.store(), &w.s);
    for l in &out {
        eprintln!("{l}");
    }
    eprintln!("held per author {:?}; store {real:?}", st.held);
    assert_eq!(v.store_usage(), real);
    assert!(verify(&v.export(&w.ids[V]).unwrap()).is_ok());
    assert!(v.seat_usage(2).0 <= v.limits().per_peer().0);
}

/// A-M3 (round 1, Major): no signature an audit path makes, over any 32 bytes, is a valid device
/// binding (the old build signed audit objects in the binding domain with a nested label, so an
/// attacker-chosen 32-byte value signed by the audit path verified as a Noise key binding).
#[test]
fn r4_fixed_a_m3_no_audit_domain_signature_is_a_device_binding() {
    let a = fixed_identity(0x5e);
    let mut forged = Vec::new();
    let mut tried = 0;
    for d in AuditDomain::ALL {
        let label = d.label().to_vec();
        let mut cands: Vec<Vec<u8>> = vec![vec![0x41; 32], vec![0; 32], vec![0xff; 32]];
        for sep in [0u8, b':', b'/'] {
            let mut m = label.clone();
            m.push(sep);
            m.resize(32, 0x41);
            cands.push(m);
        }
        for msg in cands {
            let sig = audit_sign(&a, d, &msg);
            let mut keys = a.public_keys();
            keys.noise_static = coagent_proto::bytes::PublicKey32(msg.as_slice().try_into().unwrap());
            keys.binding_sig = sig;
            tried += 1;
            if coagent_crypto::identity::verify_device(&keys).is_ok() {
                forged.push(format!("{d:?}"));
            }
        }
    }
    // positive control: a binding signed in the binding domain verifies
    assert!(coagent_crypto::identity::verify_device(&a.public_keys()).is_ok());
    eprintln!("A-M3 recheck: {tried} audit-domain signatures tried as bindings, {} verified", forged.len());
    assert!(forged.is_empty(), "audit-domain signatures verified as device bindings: {forged:?}");
}

/// R4-m4 guard: the two roster lifetime backstops (design 07 §1.4 (a); addendum 3 deliverable 2):
/// version 256 applies and 257 is `RosterLifetime`; the 32nd distinct key applies and the 33rd is
/// `RosterLifetime`; after each refusal the roster and the store are unchanged.
#[test]
fn r4_guard_roster_lifetime_backstops() {
    let mut w = World::new(0x40, 34, 2);
    let mut v = w.audit(V, every(1_000));
    let mut last = Ok(());
    while w.rosters.len() < 256 {
        let r = w.next_roster(|_, _| {});
        last = v.apply_roster(&r).map(|_| ());
        if last.is_err() {
            break;
        }
    }
    let before = v.store().list(&w.s).unwrap();
    let r257 = w.next_roster(|_, _| {});
    let got257 = v.apply_roster(&r257);
    let unchanged257 = v.store().list(&w.s).unwrap() == before && v.roster().version() == 256;
    eprintln!("lifetime: v256 {last:?}; v257 {got257:?}; unchanged {unchanged257}");
    assert!(last.is_ok(), "a version up to 256 was refused: {last:?}");
    assert_eq!(got257.map(|_| ()), Err(AuditError::RosterLifetime), "version 257 was not refused RosterLifetime");
    assert!(unchanged257);

    let mut w = World::new(0x40, 34, 2);
    let mut v = w.audit(V, every(1_000));
    let mut answers = Vec::new();
    for i in 2..34usize {
        let r = w.add(i, 2);
        let a = v.apply_roster(&r).map(|_| ());
        answers.push((i, a.clone()));
        if a.is_err() {
            break;
        }
        let r = w.remove(i);
        v.apply_roster(&r).unwrap();
    }
    eprintln!("keys: {answers:?}");
    let ok = answers.iter().filter(|(_, a)| a.is_ok()).count();
    assert_eq!(ok, 30, "distinct keys accepted beyond the two first: {ok} (32 in all expected)");
    assert_eq!(answers.last().unwrap().1, Err(AuditError::RosterLifetime), "the 33rd key was not refused RosterLifetime");
}

/// Guard for mutant M22: the FIRST roster conflict is kept (design 07 §1.4 (a), §4.1): two different
/// forks of a held version; the conflict slot holds the first, the export carries it.
#[test]
fn r4_guard_the_first_roster_conflict_is_kept() {
    let mut w = World::new(0x41, 4, 3);
    let mut v = w.audit(V, every(1_000));
    let r2 = w.add(3, 3);
    v.apply_roster(&r2).unwrap();
    let base = w.rosters[0].clone();
    let fork = |w: &World, slot: u8| {
        let mut b = r2.body.clone();
        b.members.retain(|m| m.key_id != w.key(3));
        b.members.push(member(&w.ids[3], coagent_roster::Role::Guest, slot, 2));
        let _ = &base;
        coagent_roster::sign(&w.ids[0], b).unwrap()
    };
    let f1 = fork(&w, 4);
    let f2 = fork(&w, 5);
    let a1 = v.apply_roster(&f1);
    let a2 = v.apply_roster(&f2);
    let held = v.export(&w.ids[V]).unwrap().roster_conflict;
    eprintln!("conflicts: {:?} {:?}; kept slot {:?}", a1.is_err(), a2.is_err(), held.as_ref().map(|r| r.body.members.iter().map(|m| m.slot).collect::<Vec<_>>()));
    assert!(a1.is_err() && a2.is_err());
    assert_eq!(held, Some(f1), "the roster conflict slot does not hold the FIRST conflict");
}

/// Guard for mutant M23: an own checkpoint is space-checked against the free part. With the free
/// part full (its closing checkpoint used), events recorded at a peer's request still advance the
/// chain; a checkpoint covering them is then refused `LogFull` and the free part stays within its
/// limit. (Without the check the checkpoint is stored above the limit.)
#[test]
fn r4_guard_an_own_checkpoint_is_space_checked() {
    let w = World::new(0x42, 8, 8);
    let mut v = w.audit(V, every(1_000_000));
    let l = small(16 * 1024, 64);
    v.set_limits(l);
    let mut i = 0;
    while v.record(&w.ids[V], tiny(), t(i)).is_ok() {
        i += 1;
    }
    let c1 = v.checkpoint_now(&w.ids[V], t(i + 1)).map(|_| ());
    let mut f1 = Ok(());
    let mut c2 = Ok(());
    let mut n = 0;
    while c2.is_ok() && f1.is_ok() && n < 100 {
        n += 1;
        let g = [0usize, 2, 3, 4, 5, 6, 7][n as usize % 7];
        f1 = v.record_for(&w.ids[V], &w.key(g), tiny(), t(i + 2 * n)).map(|_| ());
        c2 = v.checkpoint_now(&w.ids[V], t(i + 2 * n + 1)).map(|_| ());
    }
    eprintln!("own records {i}; closing checkpoint {c1:?}; {n} requested events; last requested {f1:?}; last checkpoint {c2:?}; free {:?} of {:?}", v.free_usage(), l.free_part());
    assert!(c1.is_ok() && f1.is_ok());
    assert_eq!(c2, Err(AuditError::LogFull));
    assert!(v.free_usage().0 <= l.free_part().0, "the free part is above its limit");
}

/// Guard for mutant M28: the conflict slot survives a `resume`, so a second conflict after a
/// restart does not replace the first.
#[test]
fn r4_guard_the_first_roster_conflict_survives_resume() {
    let mut w = World::new(0x43, 4, 3);
    let mut v = w.audit(V, every(1_000));
    let r2 = w.add(3, 3);
    v.apply_roster(&r2).unwrap();
    let fork = |w: &World, slot: u8| {
        let mut b = r2.body.clone();
        b.members.retain(|m| m.key_id != w.key(3));
        b.members.push(member(&w.ids[3], coagent_roster::Role::Guest, slot, 2));
        coagent_roster::sign(&w.ids[0], b).unwrap()
    };
    let (f1, f2) = (fork(&w, 4), fork(&w, 5));
    assert!(v.apply_roster(&f1).is_err());
    let mut r = resume_from(&w, v.store().clone()).unwrap();
    assert!(r.apply_roster(&f2).is_err());
    let held = r.export(&w.ids[V]).unwrap().roster_conflict;
    assert_eq!(held, Some(f1), "after resume the conflict slot no longer holds the FIRST conflict");
}

/// Guard for mutant M14: one requester's allowance is its own: requester A fills its allowance,
/// requester B can still use all of B's.
#[test]
fn r4_guard_one_requester_cannot_use_anothers_allowance() {
    let w = World::new(0x44, 4, 4);
    let mut v = w.audit(V, every(1_000_000));
    v.set_limits(small(32 * 1024, 256));
    let mut a = 0;
    while v.record_for(&w.ids[V], &w.key(2), tiny(), t(a)).is_ok() {
        a += 1;
    }
    let mut b = 0;
    while v.record_for(&w.ids[V], &w.key(3), tiny(), t(1_000 + b)).is_ok() {
        b += 1;
    }
    eprintln!("requester A recorded {a}, then requester B {b}");
    assert!(a > 0);
    assert_eq!(a, b, "requester B's allowance was used by requester A");
}
