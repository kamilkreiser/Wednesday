//! Independent QA gate for M3 AUDIT-FIX (R5-m1, R5-m2), 2026-11-18. Test code only; every fixture is
//! generated here from the fixed test identities of `common`. Drop into
//! `crates/coagent-audit/tests/` and add `[[test]] name = "qa_fix"` (the crate has `autotests = false`).
//!
//! - `qa_finding_*`: PASSING means the weakness is demonstrated.
//! - `qa_ok_*` / `qa_prop_*`: PASSING means the property holds.
mod common;

use std::cell::RefCell;
use std::collections::BTreeMap;
use std::rc::Rc;

use coagent_audit::budget::{Table, CLOSING_CHECKPOINT_BYTES, CLOSING_CHECKPOINT_RECORDS};
use coagent_audit::bundle::{verify, Record};
use coagent_audit::chain::{AuthorChain, EventInput};
use coagent_audit::redact::PatternRedactor;
use coagent_audit::session::{SessionAudit, StoreLimits};
use coagent_audit::store::{MemStore, Part, Store, StoreError, StoreKey};
use coagent_audit::AuditError;
use coagent_proto::bytes::{Digest32, SessionId, Signature64};
use coagent_proto::canonical;
use coagent_roster::{body_hash, sign, RosterBody, RosterChain, SignedRoster};
use common::*;

const V: usize = 1;

fn tiny() -> EventInput<'static> {
    EventInput {
        kind: "x",
        summary: None,
        full: None,
    }
}

fn inp(s: &str) -> EventInput<'_> {
    if s.is_empty() {
        tiny()
    } else {
        EventInput {
            kind: "x",
            summary: Some(s),
            full: None,
        }
    }
}

fn small(seat_bytes: usize, seat_records: usize) -> StoreLimits {
    StoreLimits {
        bytes: 8 * seat_bytes,
        records: 8 * seat_records,
    }
}

/// Tiny deterministic generator (no map order, no wall clock).
struct Lcg(u64);
impl Lcg {
    fn next(&mut self) -> u64 {
        self.0 = self
            .0
            .wrapping_mul(6364136223846793005)
            .wrapping_add(1442695040888963407);
        self.0 >> 33
    }
    fn below(&mut self, n: u64) -> u64 {
        self.next() % n
    }
}

// =================================================================================================
// A model read from the store keys alone: each allowance's usage, and the payer of a checkpoint
// =================================================================================================

fn add(a: (usize, usize), b: (usize, usize)) -> (usize, usize) {
    (a.0 + b.0, a.1 + b.1)
}

/// (allowance usage by slot, free usage, owing slots: those with a requested event after the last
/// stored own checkpoint, payer of a checkpoint at the current own seq `n`)
struct M {
    allow: BTreeMap<u8, (usize, usize)>,
    free: (usize, usize),
    owing: Vec<u8>,
}

fn model<S: Store>(st: &S, s: &SessionId) -> M {
    let mut allow: BTreeMap<u8, (usize, usize)> = BTreeMap::new();
    let mut free = (0, 0);
    let mut req: BTreeMap<u64, u8> = BTreeMap::new();
    let mut heads: Vec<(u64, usize)> = Vec::new();
    for (k, r) in st.list(s).unwrap() {
        let size = 4 + r.len();
        match k.part {
            Part::OwnEvent(None) => free = add(free, (size, 1)),
            Part::OwnEvent(Some(slot)) => {
                let e = allow.entry(slot).or_default();
                *e = add(*e, (size, 1));
                req.insert(k.n, slot);
            }
            Part::OwnHead => heads.push((k.n, size)),
            _ => {}
        }
    }
    heads.sort();
    let mut prev = 0;
    for (n, size) in &heads {
        match req.range(prev + 1..=*n).next_back() {
            Some((_, slot)) => {
                let e = allow.entry(*slot).or_default();
                *e = add(*e, (*size, 1));
            }
            None => free = add(free, (*size, 1)),
        }
        prev = *n;
    }
    let mut owing: Vec<u8> = req.range(prev + 1..).map(|(_, s)| *s).collect();
    owing.sort();
    owing.dedup();
    M { allow, free, owing }
}

fn payer_of<S: Store>(st: &S, s: &SessionId, n: u64) -> Option<u8> {
    let mut prev = 0;
    let mut req = BTreeMap::new();
    for (k, _) in st.list(s).unwrap() {
        match k.part {
            Part::OwnHead if k.n < n => prev = prev.max(k.n),
            Part::OwnEvent(Some(slot)) => {
                req.insert(k.n, slot);
            }
            _ => {}
        }
    }
    req.range(prev + 1..=n).next_back().map(|(_, s)| *s)
}

/// Every owing allowance has room for one checkpoint under `lim` (rule (A)'s promise).
fn owing_have_room<S: Store>(st: &S, s: &SessionId, lim: StoreLimits) -> Result<(), String> {
    let m = model(st, s);
    let a = lim.requested_allowance();
    for slot in &m.owing {
        let u = m.allow.get(slot).copied().unwrap_or((0, 0));
        if u.0 + CLOSING_CHECKPOINT_BYTES > a.0 || u.1 + CLOSING_CHECKPOINT_RECORDS > a.1 {
            return Err(format!(
                "owing allowance of slot {slot} at {u:?} has no room for a checkpoint in {a:?}"
            ));
        }
    }
    Ok(())
}

// =================================================================================================
// R5-m1 / rule (A): the seat cap of V's OWN slot, after a lowering rule (A) accepts
// =================================================================================================

/// V never records anything of its own (free part empty). G makes requests until its allowance is
/// full and a checkpoint covers them (G owes nothing). H makes one request (H owes one checkpoint and
/// its allowance has room). V lowers its RECORD limit: rule (A) only looks at H (owing) and accepts.
/// The seat of V's own slot now holds more records than a seat: the checkpoint H pays for is refused,
/// every time, and H's request is never witnessed. No re-add, no free-part involvement.
#[test]
fn qa_finding_lowering_accepted_by_rule_a_blocks_an_allowance_paid_checkpoint_seat_records() {
    let w = World::new(0x71, 8, 8);
    let mut v = w.audit(V, every(1_000_000));
    v.set_limits(small(64 * 1024, 512));
    let h = w.key(3);
    // every other requester but H fills its allowance; each run is covered by a checkpoint it pays
    let mut g_acc = 0u64;
    let mut cp_g = Vec::new();
    for gi in [0usize, 2, 4, 5, 6, 7] {
        while v.record_for(&w.ids[V], &w.key(gi), tiny(), t(1 + g_acc)).is_ok() {
            g_acc += 1;
        }
        cp_g.push(v.checkpoint_now(&w.ids[V], t(4_000 + g_acc)).map(|x| x.author_seq));
    }
    v.record_for(&w.ids[V], &h, tiny(), t(5_001)).unwrap();
    let before = v.limits();
    // the largest record limit (per seat) whose allowance still fits H's usage + one checkpoint and
    // whose seat is below what V's own slot holds
    let hu = v.requested_usage(3);
    let seat_now = v.seat_usage(v.status().own_slot);
    let mut pick = None;
    for r in (8..512usize).rev() {
        let l = small(64 * 1024, r);
        let a = l.requested_allowance();
        if hu.1 + 1 <= a.1 && hu.0 + 516 <= a.0 && seat_now.1 + 1 > l.per_peer().1 {
            pick = Some(l);
            break;
        }
    }
    let low = pick.expect("a lowering of that shape exists");
    let tr = v.try_set_limits(low);
    let mut refused = 0;
    let mut ok = 0;
    for i in 0..10u64 {
        match v.checkpoint_now(&w.ids[V], t(6_000 + i)) {
            Ok(_) => ok += 1,
            Err(AuditError::LogFull) => refused += 1,
            Err(e) => panic!("{e:?}"),
        }
    }
    let payer = payer_of(v.store(), &w.s, v.own().seq());
    let pu = v.requested_usage(3);
    let a = v.limits().requested_allowance();
    let covered = v.own().checkpoints().last().map(|c| c.head.author_seq);
    let free = v.free_usage();
    let own_try = v.record(&w.ids[V], tiny(), t(7_000));
    // the owner raises the limits back
    let up = v.try_set_limits(before);
    let cp_up = v.checkpoint_now(&w.ids[V], t(8_000)).map(|x| x.author_seq);
    eprintln!(
        "qa seat-records: G accepted {g_acc}, its checkpoint {cp_g:?}; H's allowance {hu:?}; V's seat \
         {seat_now:?}; lowering to {low:?} (allowance {:?}, seat {:?}): try_set_limits {tr:?}; then \
         10 checkpoints: {ok} Ok, {refused} refused LogFull; payer slot {payer:?} usage {pu:?} of \
         allowance {a:?} (room: {}); newest covered {covered:?} of own seq {}; free part {free:?}; \
         own record {own_try:?}; raising back {up:?}, checkpoint then {cp_up:?}",
        low.requested_allowance(),
        low.per_peer(),
        pu.0 + 516 <= a.0 && pu.1 + 1 <= a.1,
        v.own().seq() - 1,
    );
    assert!(
        tr.is_ok()
            && refused == 10
            && payer == Some(3)
            && pu.0 + 516 <= a.0
            && pu.1 + 1 <= a.1
            && free == (0, 0),
        "not shown"
    );
}

/// The same with BYTES: V fills its free part with its own records, H requests once; V lowers its
/// byte limit so that H's allowance still has room (rule (A) accepts) but the own seat is over.
#[test]
fn qa_finding_lowering_accepted_by_rule_a_blocks_an_allowance_paid_checkpoint_seat_bytes() {
    let w = World::new(0x72, 8, 8);
    let mut v = w.audit(V, every(1_000_000));
    v.set_limits(small(64 * 1024, 512));
    let body = "y".repeat(300);
    let mut own = 0u64;
    while v.record(&w.ids[V], inp(&body), t(1 + own)).is_ok() {
        own += 1;
    }
    v.record_for(&w.ids[V], &w.key(3), tiny(), t(5_001)).unwrap();
    let hu = v.requested_usage(3);
    let seat_now = v.seat_usage(v.status().own_slot);
    let mut pick = None;
    for b in (2_048..64 * 1024usize).rev().step_by(16) {
        let l = small(b, 512);
        let a = l.requested_allowance();
        if hu.1 + 1 <= a.1 && hu.0 + 516 <= a.0 && seat_now.0 > l.per_peer().0 {
            pick = Some(l);
            break;
        }
    }
    let low = pick.expect("a lowering of that shape exists");
    let tr = v.try_set_limits(low);
    let r: Vec<_> = (0..5u64)
        .map(|i| v.checkpoint_now(&w.ids[V], t(6_000 + i)).map(|_| ()))
        .collect();
    let a = v.limits().requested_allowance();
    eprintln!(
        "qa seat-bytes: own records {own}, free {:?}; H's allowance {hu:?}; seat {seat_now:?}; lowering \
         to {low:?} (allowance {:?}, seat {:?}): {tr:?}; 5 checkpoints {r:?}; payer {:?}, room {}",
        v.free_usage(),
        low.requested_allowance(),
        low.per_peer(),
        payer_of(v.store(), &w.s, v.own().seq()),
        hu.0 + 516 <= a.0 && hu.1 + 1 <= a.1
    );
    assert!(
        tr.is_ok() && r.iter().all(|x| *x == Err(AuditError::LogFull)),
        "not shown"
    );
}

// =================================================================================================
// Rule (A) at its edges
// =================================================================================================

#[test]
fn qa_ok_rule_a_edges_steps_raise_zero_huge_resume() {
    let w = World::new(0x73, 8, 8);
    let mut v = w.audit(V, every(1_000_000));
    let base = small(64 * 1024, 512);
    v.set_limits(base);
    let (g, h) = (w.key(2), w.key(3));
    v.record_for(&w.ids[V], &h, tiny(), t(1)).unwrap();
    v.record_for(&w.ids[V], &g, tiny(), t(2)).unwrap();
    v.record_for(&w.ids[V], &g, tiny(), t(3)).unwrap();
    let mut log = Vec::new();
    let mut accepted = 0;
    let mut refused = 0;
    // several steps down, then up, then down again, by records and by bytes
    let mut sched: Vec<StoreLimits> = Vec::new();
    for r in (8..=512).rev().step_by(7) {
        sched.push(small(64 * 1024, r));
    }
    sched.push(base);
    for b in (600..=64 * 1024).rev().step_by(397) {
        sched.push(small(b, 512));
    }
    sched.push(base);
    for r in (8..=512).rev().step_by(29) {
        sched.push(small(64 * 1024, r));
        sched.push(base);
    }
    sched.push(StoreLimits::default());
    sched.push(StoreLimits {
        bytes: usize::MAX,
        records: usize::MAX,
    });
    sched.push(StoreLimits {
        bytes: 0,
        records: 0,
    });
    sched.push(StoreLimits {
        bytes: 1,
        records: usize::MAX,
    });
    for l in &sched {
        let before = v.limits();
        let r = v.try_set_limits(*l);
        match r {
            Ok(()) => {
                accepted += 1;
                owing_have_room(v.store(), &w.s, v.limits()).unwrap();
                let d = StoreLimits::default();
                assert_eq!(
                    v.limits(),
                    StoreLimits {
                        bytes: l.bytes.min(d.bytes),
                        records: l.records.min(d.records)
                    }
                );
            }
            Err(AuditError::LogFull) => {
                refused += 1;
                assert_eq!(v.limits(), before, "a refused change moved the limits");
            }
            Err(e) => panic!("try_set_limits answered {e:?}"),
        }
        log.push((*l, r));
    }
    // exact boundaries: G owes with usage u (2 records); find the record count where the allowance is
    // exactly u.1 + 1 and the byte count where it is exactly u.0 + 516
    let ug = v.requested_usage(2);
    let uh = v.requested_usage(3);
    let need = (ug.0.max(uh.0) + 516, ug.1.max(uh.1) + 1);
    let mut exact_b = None;
    for b in 600..64 * 1024usize {
        if small(b, 512).requested_allowance().0 == need.0 {
            exact_b = Some(b);
            break;
        }
    }
    v.set_limits(StoreLimits::default());
    let mut boundary = Vec::new();
    if let Some(b) = exact_b {
        let at = v.try_set_limits(small(b, 512));
        v.set_limits(StoreLimits::default());
        let below = v.try_set_limits(small(b - 1, 512));
        let below_alw = small(b - 1, 512).requested_allowance();
        v.set_limits(StoreLimits::default());
        boundary.push(format!(
            "bytes: allowance exactly {:?} -> {at:?}; one seat byte less (allowance {below_alw:?}) -> {below:?}",
            small(b, 512).requested_allowance()
        ));
        assert_eq!(at, Ok(()));
        if below_alw.0 < need.0 {
            assert_eq!(below, Err(AuditError::LogFull));
        }
    }
    // resume: limits come back as the defaults; with no call, the same, lower, different
    let lowered = small(8 * 1024, 32);
    let lr = v.try_set_limits(lowered);
    let st = v.store().clone();
    let resume = || {
        SessionAudit::resume(
            st.clone(),
            w.s,
            &w.ids[V],
            &w.ids[0].verified(),
            every(1_000_000),
            Box::new(PatternRedactor),
            t(50),
        )
        .unwrap()
    };
    let r0 = resume();
    let none = r0.limits();
    let mut r1 = resume();
    let same = r1.try_set_limits(v.limits());
    let mut r2 = resume();
    let lower = r2.try_set_limits(small(1_024, 8));
    let lower_lim = r2.limits();
    eprintln!(
        "qa rule A edges: {accepted} accepted, {refused} refused over {} changes; H {uh:?} G {ug:?} need \
         {need:?}; {boundary:?}; lowered {lowered:?} -> {lr:?}; after resume: no call {none:?}; same \
         {same:?}; much lower {lower:?} (limits then {lower_lim:?})",
        sched.len()
    );
    assert!(accepted > 0 && refused > 0);
    assert_eq!(none, StoreLimits::default());
    assert_eq!(same, Ok(()));
    if lower.is_err() {
        assert_eq!(lower_lim, StoreLimits::default());
    }
}

// =================================================================================================
// R5-m1 generated: is any checkpoint refused because its payer lacks room? (and seat-cap refusals)
// =================================================================================================

#[test]
fn qa_prop_no_checkpoint_refused_for_its_payer_rule_a() {
    let cases: u64 = std::env::var("QA_FIX_CASES")
        .ok()
        .and_then(|s| s.parse().ok())
        .unwrap_or(40);
    let mut c: BTreeMap<&'static str, u64> = BTreeMap::new();
    let mut seat_examples: Vec<String> = Vec::new();
    for case in 0..cases {
        let mut g = Lcg(0xC0FFEE ^ case.wrapping_mul(0x9E37));
        let mut w = World::new(0x74, 12, 8);
        let mut v = w.audit(V, every(1 + g.below(6)));
        let seat = (4_096 + 1_024 * g.below(28) as usize, 24 + 4 * g.below(40) as usize);
        v.set_limits(small(seat.0, seat.1));
        // roster: slot of each member key index
        let mut cur: BTreeMap<usize, u8> = (0..8).map(|i| (i, i as u8)).collect();
        let mut v_readded = false;
        let mut now = 1_000u64;
        let steps = 40 + g.below(60);
        for step in 0..steps {
            now += 5_000;
            let op = g.below(100);
            match op {
                0..=24 => {
                    let b = "z".repeat(g.below(200) as usize);
                    let _ = v.record(&w.ids[V], inp(&b), t(now));
                    *c.entry("own record call").or_default() += 1;
                }
                25..=49 => {
                    let gi = g.below(12) as usize;
                    if gi != V {
                        let b = "q".repeat(g.below(150) as usize);
                        match v.record_for(&w.ids[V], &w.key(gi), inp(&b), t(now)) {
                            Ok(_) => *c.entry("request accepted").or_default() += 1,
                            Err(AuditError::LogFull) => *c.entry("request refused").or_default() += 1,
                            Err(AuditError::NotMember(_)) => {}
                            Err(e) => panic!("request answered {e:?}"),
                        }
                    }
                }
                50..=64 => {
                    let n = v.own().seq();
                    let payer = payer_of(v.store(), &w.s, n);
                    let m = model(v.store(), &w.s);
                    let r = if g.below(2) == 0 {
                        v.checkpoint(&w.ids[V], t(now)).map(|_| ())
                    } else {
                        v.checkpoint_now(&w.ids[V], t(now)).map(|_| ())
                    };
                    match r {
                        Ok(()) | Err(AuditError::NoSuchEvent(0)) => {
                            *c.entry("checkpoint call ok").or_default() += 1
                        }
                        Err(AuditError::LogFull) => {
                            let lim = v.limits();
                            match payer {
                                Some(s) => {
                                    let u = m.allow.get(&s).copied().unwrap_or((0, 0));
                                    let a = lim.requested_allowance();
                                    if u.0 + 516 > a.0 || u.1 + 1 > a.1 {
                                        panic!(
                                            "case {case} step {step}: checkpoint refused because its \
                                             payer slot {s} lacks room: {u:?} of {a:?}"
                                        );
                                    }
                                    let me = v.status().own_slot;
                                    let su = v.seat_usage(me);
                                    let reused = v_readded;
                                    *c.entry(if reused {
                                        "allowance-paid checkpoint refused by the own seat (V re-added before)"
                                    } else {
                                        "allowance-paid checkpoint refused by the own seat (V never re-added)"
                                    })
                                    .or_default() += 1;
                                    if seat_examples.len() < 6 {
                                        seat_examples.push(format!(
                                            "case {case} step {step}: payer {s} {u:?} of {a:?}; own slot {me} seat {su:?} of {:?}; free {:?}; V re-added {reused}",
                                            lim.per_peer(),
                                            v.free_usage()
                                        ));
                                    }
                                }
                                None => {
                                    *c.entry("free-paid checkpoint refused").or_default() += 1
                                }
                            }
                        }
                        Err(e) => panic!("checkpoint answered {e:?}"),
                    }
                }
                65..=76 => {
                    let l = v.limits();
                    let f = 3 + g.below(6) as usize;
                    let nl = StoreLimits {
                        bytes: (l.bytes * f / 8).max(8 * 600),
                        records: (l.records * f / 8).max(8 * 4),
                    };
                    let before = v.limits();
                    match v.try_set_limits(nl) {
                        Ok(()) => {
                            *c.entry("limit change accepted").or_default() += 1;
                            if let Err(e) = owing_have_room(v.store(), &w.s, v.limits()) {
                                panic!("case {case} step {step}: accepted change broke rule (A): {e}");
                            }
                        }
                        Err(AuditError::LogFull) => {
                            *c.entry("limit change refused").or_default() += 1;
                            assert_eq!(v.limits(), before);
                        }
                        Err(e) => panic!("{e:?}"),
                    }
                }
                77..=82 => {
                    let lim = v.limits();
                    let st = v.store().clone();
                    v = SessionAudit::resume(
                        st,
                        w.s,
                        &w.ids[V],
                        &w.ids[0].verified(),
                        every(1 + g.below(6)),
                        Box::new(PatternRedactor),
                        t(now),
                    )
                    .unwrap();
                    *c.entry("resume").or_default() += 1;
                    match g.below(4) {
                        0 => {}
                        1 => {
                            assert_eq!(v.try_set_limits(lim), Ok(()), "limits in force refused after resume");
                        }
                        2 => {
                            let _ = v.try_set_limits(StoreLimits {
                                bytes: lim.bytes / 2,
                                records: lim.records / 2,
                            });
                        }
                        _ => {
                            let _ = v.try_set_limits(small(5_000, 40));
                        }
                    }
                }
                83..=90 => {
                    // remove an other member or V itself
                    let gi = if g.below(4) == 0 { V } else { 2 + g.below(10) as usize };
                    if cur.contains_key(&gi) && cur.len() > 3 && gi != 0 {
                        let r = w.remove(gi);
                        v.apply_roster(&r).unwrap();
                        cur.remove(&gi);
                        *c.entry(if gi == V { "V removed" } else { "member removed" }).or_default() += 1;
                    }
                }
                _ => {
                    // add a member (or V) into a free slot
                    let gi = if !cur.contains_key(&V) && g.below(2) == 0 {
                        V
                    } else {
                        2 + g.below(10) as usize
                    };
                    if !cur.contains_key(&gi) {
                        let used: Vec<u8> = cur.values().copied().collect();
                        if let Some(slot) = (0..8u8).find(|s| !used.contains(s)) {
                            let r = w.add(gi, slot);
                            v.apply_roster(&r).unwrap();
                            cur.insert(gi, slot);
                            if gi == V {
                                v_readded = true;
                                *c.entry("V re-added").or_default() += 1;
                            } else {
                                *c.entry("member added").or_default() += 1;
                            }
                        }
                    }
                }
            }
        }
        verify(&v.export(&w.ids[V]).unwrap()).unwrap();
    }
    eprintln!("qa prop R5-m1: {cases} cases; counts {c:?}; seat examples {seat_examples:#?}");
    for k in [
        "limit change accepted",
        "limit change refused",
        "request accepted",
        "resume",
        "V removed",
        "V re-added",
    ] {
        assert!(c.get(k).copied().unwrap_or(0) > 0, "never reached: {k}");
    }
}

// =================================================================================================
// R5-m2: a probing store, every kind of version, failures and stops, and the answer compared with
// the roster crate's own on the versions STORED
// =================================================================================================

#[derive(Default, Debug)]
struct PS {
    calls: usize,
    fail_put: bool,
    fail_rm: bool,
    stop_after: Option<usize>,
}

#[derive(Clone)]
struct Probe {
    inner: MemStore,
    st: Rc<RefCell<PS>>,
}

impl Store for Probe {
    fn put(&mut self, s: &SessionId, k: &StoreKey, r: &[u8]) -> Result<(), StoreError> {
        let mut st = self.st.borrow_mut();
        st.calls += 1;
        if st.fail_put || st.stop_after.is_some_and(|n| st.calls > n) {
            return Err(StoreError::Unavailable("qa: put fails"));
        }
        self.inner.put(s, k, r)
    }
    fn remove(&mut self, s: &SessionId, k: &StoreKey) -> Result<(), StoreError> {
        let mut st = self.st.borrow_mut();
        st.calls += 1;
        if st.fail_rm || st.stop_after.is_some_and(|n| st.calls > n) {
            return Err(StoreError::Unavailable("qa: remove fails"));
        }
        self.inner.remove(s, k)
    }
    fn list(&self, s: &SessionId) -> Result<Vec<(StoreKey, Vec<u8>)>, StoreError> {
        self.inner.list(s)
    }
}

fn stored_versions<S: Store>(st: &S, s: &SessionId) -> Vec<SignedRoster> {
    let mut v: BTreeMap<u64, SignedRoster> = BTreeMap::new();
    for (k, bytes) in st.list(s).unwrap() {
        if k.part == Part::Fixed(Table::Roster) {
            if let Record::Roster(r) = canonical::decode::<Record>(&bytes).unwrap() {
                v.insert(r.body.version, r);
            }
        }
    }
    v.into_values().collect()
}

/// The roster crate's own answer for a chain built from `held` (first by start, the rest applied).
fn reference(w: &World, held: &[SignedRoster], x: &SignedRoster) -> Result<String, String> {
    let mut c = RosterChain::start(&w.ids[0].verified(), w.s, &w.key(V), &held[0])
        .map_err(|e| format!("held[0] refused: {e:?}"))?;
    for h in &held[1..] {
        c.apply(h).map_err(|e| format!("held {} refused: {e:?}", h.body.version))?;
    }
    c.apply(x).map(|a| format!("{a:?}")).map_err(|e| format!("{:?}", AuditError::from(e)))
}

fn next_body(prev: &SignedRoster) -> RosterBody {
    let mut b = prev.body.clone();
    b.version += 1;
    b.prev_hash = Digest32(body_hash(&prev.body).unwrap());
    b
}

#[test]
fn qa_prop_r5m2_answers_match_the_roster_crate_on_the_stored_versions() {
    let cases: u64 = std::env::var("QA_FIX_CASES")
        .ok()
        .and_then(|s| s.parse().ok())
        .unwrap_or(40);
    let mut c: BTreeMap<String, u64> = BTreeMap::new();
    for case in 0..cases {
        let mut g = Lcg(0xBADD ^ case.wrapping_mul(0x51ED));
        let mut w = World::new(0x75, 12, 4);
        let st = Rc::new(RefCell::new(PS::default()));
        let store = Probe {
            inner: MemStore::new(),
            st: st.clone(),
        };
        let mut v = SessionAudit::start(
            store,
            &w.ids[V],
            &w.ids[0].verified(),
            &w.rosters[0],
            every(3),
            Box::new(PatternRedactor),
            t(0),
        )
        .unwrap();
        // the world's real chain (what the starter publishes); minted lazily
        let mut real: Vec<SignedRoster> = vec![w.rosters[0].clone()];
        let mut members: Vec<usize> = vec![0, 1, 2, 3];
        let steps = 30 + g.below(40);
        for step in 0..steps {
            let held = stored_versions(v.store(), &w.s);
            let cur = v.roster().version();
            // mint the real next version if not yet minted
            if real.len() as u64 == cur {
                let r = match g.below(3) {
                    0 if members.len() < 7 => {
                        let i = (4..12).find(|i| !members.contains(i));
                        match i {
                            Some(i) if !w.rosters.iter().any(|r| {
                                r.body.removed.iter().any(|x| x.key_id == w.key(i))
                            }) =>
                            {
                                let used: Vec<u8> = w.rosters.last().unwrap().body.members.iter().map(|m| m.slot).collect();
                                let slot = (0..8u8).find(|s| !used.contains(s)).unwrap();
                                members.push(i);
                                w.add(i, slot)
                            }
                            _ => w.next_roster(|_, _| {}),
                        }
                    }
                    1 if members.len() > 3 => {
                        let i = *members.iter().rev().find(|i| **i != 0 && **i != V).unwrap();
                        members.retain(|x| *x != i);
                        w.remove(i)
                    }
                    _ => w.next_roster(|_, _| {}),
                };
                real.push(r);
            }
            let nb = next_body(&real[cur as usize - 1]);
            let kind = g.below(11);
            let (name, x): (&str, SignedRoster) = match kind {
                0..=2 => ("next", real[cur as usize].clone()),
                3 => ("forged", sign(&w.ids[2], nb.clone()).unwrap()),
                4 => (
                    "unsigned",
                    SignedRoster {
                        body: nb.clone(),
                        sig: Signature64([0; 64]),
                    },
                ),
                5 => {
                    let mut b = nb.clone();
                    b.version += 1 + g.below(3);
                    ("gap", sign(&w.ids[0], b).unwrap())
                }
                6 => ("stale", real[g.below(cur) as usize].clone()),
                7 => ("duplicate", real[cur as usize - 1].clone()),
                8 if cur >= 2 => {
                    let mut b = real[1 + g.below(cur - 1) as usize].body.clone();
                    b.prev_hash = Digest32([0xA5; 32]);
                    ("fork", sign(&w.ids[0], b).unwrap())
                }
                9 => {
                    let mut b = nb.clone();
                    b.prev_hash = Digest32([0x11; 32]);
                    ("broken chain", sign(&w.ids[0], b).unwrap())
                }
                _ => {
                    // the real version two ahead, if minted, else a gap
                    let mut b = nb.clone();
                    b.version += 1;
                    ("out of order", sign(&w.ids[0], b).unwrap())
                }
            };
            let want = reference(&w, &held, &x);
            let mode = g.below(6);
            {
                let mut s = st.borrow_mut();
                s.fail_put = mode == 1 || mode == 3;
                s.fail_rm = mode == 2 || mode == 3;
                s.stop_after = if mode == 4 { Some(s.calls + g.below(2) as usize) } else { None };
            }
            let calls0 = st.borrow().calls;
            let got = v.apply_roster(&x).map(|a| format!("{a:?}")).map_err(|e| format!("{e:?}"));
            let calls = st.borrow().calls - calls0;
            {
                let mut s = st.borrow_mut();
                s.fail_put = false;
                s.fail_rm = false;
                s.stop_after = None;
            }
            let store_failed = matches!(&got, Err(e) if e.starts_with("Store("));
            if store_failed {
                *c.entry(format!("{name}: store failed")).or_default() += 1;
                assert!(want.is_ok() || name == "fork", "case {case} step {step}: {name} refused by the roster crate ({want:?}) but answered {got:?}");
            } else {
                assert_eq!(
                    got, want,
                    "case {case} step {step}: {name} (mode {mode}) answered differently from the roster crate on the stored versions"
                );
                *c.entry(format!("{name}: {}", if got.is_ok() { "accepted" } else { "refused" })).or_default() += 1;
            }
            if want.is_err() && name != "fork" {
                assert_eq!(calls, 0, "case {case} step {step}: refused {name} made {calls} store calls");
            }
            // what is stored
            let after = stored_versions(v.store(), &w.s);
            let mut chain = RosterChain::start(&w.ids[0].verified(), w.s, &w.key(V), &after[0]).unwrap();
            for h in &after[1..] {
                assert!(
                    matches!(chain.apply(h), Ok(coagent_roster::Applied::Advanced { .. })),
                    "case {case} step {step}: stored version {} not accepted in order",
                    h.body.version
                );
            }
            assert_eq!(after.last().unwrap().body.version, v.roster().version(), "member and store disagree");
            // a crash here: the store as it is
            let snap = v.store().clone();
            let r = SessionAudit::resume(
                snap.clone(),
                w.s,
                &w.ids[V],
                &w.ids[0].verified(),
                every(3),
                Box::new(PatternRedactor),
                t(9_000_000),
            )
            .unwrap_or_else(|e| panic!("case {case} step {step}: resume refused {e:?}"));
            verify(&r.export(&w.ids[V]).unwrap()).unwrap();
            SessionAudit::resume_with_anchor(
                snap,
                &v.anchor(),
                w.s,
                &w.ids[V],
                &w.ids[0].verified(),
                every(3),
                Box::new(PatternRedactor),
                t(9_000_000),
            )
            .unwrap_or_else(|e| panic!("case {case} step {step}: resume_with_anchor refused {e:?}"));
            // sometimes replace the member by a resumed one (the check chain is then rebuilt)
            if g.below(5) == 0 {
                let s2 = v.store().clone();
                v = SessionAudit::resume(
                    s2,
                    w.s,
                    &w.ids[V],
                    &w.ids[0].verified(),
                    every(3),
                    Box::new(PatternRedactor),
                    t(now_ms(step)),
                )
                .unwrap();
                *c.entry("resume".to_string()).or_default() += 1;
            }
            // own activity between versions
            if g.below(3) == 0 {
                let _ = v.record(&w.ids[V], tiny(), t(now_ms(step)));
                let _ = v.checkpoint(&w.ids[V], t(now_ms(step)));
            }
        }
    }
    eprintln!("qa prop R5-m2: {cases} cases; {c:#?}");
    for k in [
        "next: accepted",
        "next: store failed",
        "forged: refused",
        "unsigned: refused",
        "gap: refused",
        "stale: refused",
        "duplicate: accepted",
        "fork: refused",
        "broken chain: refused",
        "resume",
    ] {
        assert!(c.get(k).copied().unwrap_or(0) > 0, "never reached: {k}");
    }
}

fn now_ms(step: u64) -> u64 {
    10_000 + step * 1_000
}

/// The check chain at the history bound: 255 versions applied, a failed write at 256 (rebuild from
/// 255), 256 then accepted, 257 refused before any store call; resume and the export at 256.
#[test]
fn qa_ok_r5m2_at_the_history_bound() {
    let mut w = World::new(0x76, 4, 3);
    let st = Rc::new(RefCell::new(PS::default()));
    let mut v = SessionAudit::start(
        Probe {
            inner: MemStore::new(),
            st: st.clone(),
        },
        &w.ids[V],
        &w.ids[0].verified(),
        &w.rosters[0],
        every(1_000),
        Box::new(PatternRedactor),
        t(0),
    )
    .unwrap();
    for _ in 2..=255 {
        let r = w.next_roster(|_, _| {});
        v.apply_roster(&r).unwrap();
    }
    let r256 = w.next_roster(|_, _| {});
    st.borrow_mut().fail_put = true;
    let f = v.apply_roster(&r256).map(|_| ());
    st.borrow_mut().fail_put = false;
    // resume in between: the check chain is rebuilt by the resumed member
    let mut v2 = SessionAudit::resume(
        v.store().clone(),
        w.s,
        &w.ids[V],
        &w.ids[0].verified(),
        every(1_000),
        Box::new(PatternRedactor),
        t(5),
    )
    .unwrap();
    let ok = v.apply_roster(&r256).map(|_| ());
    let ok2 = v2.apply_roster(&r256).map(|_| ());
    let r257 = w.next_roster(|_, _| {});
    let c0 = st.borrow().calls;
    let x = v.apply_roster(&r257).map(|_| ());
    let calls = st.borrow().calls - c0;
    let exp = verify(&v.export(&w.ids[V]).unwrap()).map(|_| ());
    eprintln!("qa bound: 256 with put failing {f:?}; then {ok:?}; resumed member {ok2:?}; 257 {x:?} with {calls} store calls; export {exp:?}");
    assert!(matches!(f, Err(AuditError::Store(_))));
    assert_eq!(ok, Ok(()));
    assert_eq!(ok2, Ok(()));
    assert!(x.is_err() && calls == 0);
    assert!(exp.is_ok());
}

/// join_author: refused anchors make no store call (wrong session, non-member, own, duplicate).
#[test]
fn qa_ok_join_author_refusals_make_no_store_call() {
    let w = World::new(0x77, 6, 4);
    let st = Rc::new(RefCell::new(PS::default()));
    let mut v = SessionAudit::start(
        Probe {
            inner: MemStore::new(),
            st: st.clone(),
        },
        &w.ids[V],
        &w.ids[0].verified(),
        &w.rosters[0],
        every(1_000),
        Box::new(PatternRedactor),
        t(0),
    )
    .unwrap();
    let mk = |i: usize, s: SessionId| {
        let mut a = AuthorChain::new(&w.ids[i], s, every(1_000), Box::new(PatternRedactor), t(0));
        a.append(&w.ids[i], tiny(), t(1)).unwrap();
        a.checkpoint_now(&w.ids[i], &w.valid(1), t(2)).unwrap()
    };
    let mut out = Vec::new();
    for (name, h) in [
        ("other session", mk(2, session(0xEE))),
        ("not a member", mk(5, w.s)),
        ("own", mk(V, w.s)),
    ] {
        let c0 = st.borrow().calls;
        let r = v.join_author(&h);
        out.push((name, format!("{r:?}"), st.borrow().calls - c0));
    }
    let good = mk(2, w.s);
    let c0 = st.borrow().calls;
    let g1 = v.join_author(&good);
    let g1c = st.borrow().calls - c0;
    let c0 = st.borrow().calls;
    let g2 = v.join_author(&good);
    let g2c = st.borrow().calls - c0;
    eprintln!("qa join_author: {out:?}; good {g1:?} ({g1c} calls); again {g2:?} ({g2c} calls)");
    assert!(out.iter().all(|(_, r, c)| r.starts_with("Err") && *c == 0));
    assert!(g1.is_ok() && g1c == 1 && g2.is_err() && g2c == 0);
}
