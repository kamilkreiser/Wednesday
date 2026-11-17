//! Gate r5 for M3-AUDIT (independent short check of addendum 5/6, 2026-11-18). Test code only; every
//! fixture is generated here from the fixed test identities of `common`.
//!
//! - `r5_finding_*`: PASSING means the weakness is demonstrated.
//! - `r5_ok_*`: PASSING means the property holds.
//! - `r5_prop_peers_request`: generated schedules in which PEERS cause requests (with the same
//!   schedule run again with every request removed).
mod common;

use std::cell::{Cell, RefCell};
use std::collections::{BTreeMap, BTreeSet};
use std::rc::Rc;

use coagent_audit::anchor::{
    AnchorError, AnchorRun, AnchorSlot, AuditAnchor, MAX_ANCHOR_BYTES, MAX_ANCHOR_RUNS,
    MAX_ANCHOR_SLOTS,
};
use coagent_audit::budget::{Table, CHECKPOINT_SLOT_MAX};
use coagent_audit::bundle::verify;
use coagent_audit::chain::{AuthorChain, EventInput};
use coagent_audit::checkpoint::CheckpointPolicy;
use coagent_audit::redact::PatternRedactor;
use coagent_audit::session::{SessionAudit, StoreLimits};
use coagent_audit::store::{MemStore, Part, Store, StoreError, StoreKey};
use coagent_audit::tiers::ShareLevel;
use coagent_audit::AuditError;
use coagent_proto::bytes::{Digest32, KeyId, SessionId};
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

fn digits(n: u64) -> usize {
    n.to_string().len()
}

// =================================================================================================
// An independent model of who pays, read from the store keys alone
// =================================================================================================

#[derive(Debug, Default, Clone)]
struct Model {
    free: (usize, usize),
    allow: BTreeMap<u8, (usize, usize)>,
    free_heads: usize,
    paid_heads: usize,
    own_none: Vec<u64>,
    own_some: Vec<u64>,
    heads: Vec<u64>,
}

fn add(a: (usize, usize), b: (usize, usize)) -> (usize, usize) {
    (a.0 + b.0, a.1 + b.1)
}

fn model<S: Store>(st: &S, s: &SessionId) -> Model {
    let mut m = Model::default();
    let mut req: BTreeMap<u64, u8> = BTreeMap::new();
    let mut heads: Vec<(u64, usize)> = Vec::new();
    for (k, r) in st.list(s).unwrap() {
        let size = 4 + r.len();
        match k.part {
            Part::OwnEvent(None) => {
                m.free = add(m.free, (size, 1));
                m.own_none.push(k.n);
            }
            Part::OwnEvent(Some(slot)) => {
                let e = m.allow.entry(slot).or_default();
                *e = add(*e, (size, 1));
                req.insert(k.n, slot);
                m.own_some.push(k.n);
            }
            Part::OwnHead => heads.push((k.n, size)),
            _ => {}
        }
    }
    heads.sort();
    let mut prev = 0;
    for (n, size) in heads {
        match req.range(prev + 1..=n).next_back() {
            Some((_, slot)) => {
                let e = m.allow.entry(*slot).or_default();
                *e = add(*e, (size, 1));
                m.paid_heads += 1;
            }
            None => {
                m.free = add(m.free, (size, 1));
                m.free_heads += 1;
            }
        }
        m.heads.push(n);
        prev = n;
    }
    m
}

/// The payer of a checkpoint at `n` by the model (None = the free part).
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

// =================================================================================================
// 1. The property: peers cause requests
// =================================================================================================

#[derive(Clone, Copy, Debug)]
enum Op {
    Own(u8),
    Announce(u8, u8),
    Req(u8, u8),
    Cp,
    CpNow,
    Remove(u8),
    ReAdd(u8),
    Lower(u8),
    Resume,
    Tick,
}

fn op() -> impl Strategy<Value = Op> {
    prop_oneof![
        5 => (0u8..3).prop_map(Op::Own),
        1 => (any::<u8>(), 0u8..3).prop_map(|(a, b)| Op::Announce(a, b)),
        8 => (any::<u8>(), 0u8..3).prop_map(|(a, b)| Op::Req(a, b)),
        3 => Just(Op::Cp),
        2 => Just(Op::CpNow),
        1 => any::<u8>().prop_map(Op::Remove),
        1 => any::<u8>().prop_map(Op::ReAdd),
        1 => (0u8..4).prop_map(Op::Lower),
        1 => Just(Op::Resume),
        1 => Just(Op::Tick),
    ]
}

fn body(sz: u8) -> String {
    "s".repeat([0usize, 200, 1500][sz as usize % 3])
}

#[derive(Debug, Default)]
struct Out {
    /// op index -> (result, free usage before, framed size if stored)
    own: BTreeMap<usize, (Result<u64, AuditError>, (usize, usize), Option<usize>)>,
    free_heads: Vec<usize>,
    free: Vec<(usize, usize)>,
}

type Counts = BTreeMap<&'static str, u64>;

fn bump(c: &mut Counts, k: &'static str) {
    *c.entry(k).or_default() += 1;
}

fn fail(s: String) -> Result<Out, TestCaseError> {
    Err(TestCaseError::fail(s))
}

fn run(
    ops: &[Op],
    seat: (usize, usize),
    pol: CheckpointPolicy,
    peers: bool,
    c: &mut Counts,
) -> Result<Out, TestCaseError> {
    let mut w = World::new(0x60, 12, 8);
    let mut v = w.audit(V, pol);
    let mut lim = small(seat.0, seat.1);
    v.set_limits(lim);
    let mut cur: BTreeMap<usize, u8> = (0..8).map(|i| (i, i as u8)).collect();
    let (mut own_seqs, mut req_seqs) = (BTreeSet::new(), BTreeSet::new());
    let (mut own_calls, mut lowered) = (0usize, false);
    let mut now_ms = 1_000u64;
    let mut out = Out::default();
    for (i, op) in ops.iter().enumerate() {
        now_ms += if matches!(op, Op::Tick) { 90_000 } else { 5_000 };
        let now = t(now_ms);
        let before = model(v.store(), &w.s);
        match *op {
            Op::Own(sz) | Op::Announce(_, sz) => {
                own_calls += 1;
                let fb = v.free_usage();
                let r = if let Op::Announce(m, _) = *op {
                    let others: Vec<usize> = cur.keys().filter(|k| **k != V).copied().collect();
                    let target = others[m as usize % others.len()];
                    let lvl = [ShareLevel::Nothing, ShareLevel::Summaries, ShareLevel::Full]
                        [sz as usize % 3];
                    v.announce_share_level(&w.ids[V], w.key(target), lvl, now)
                } else {
                    let b = body(sz);
                    v.record(&w.ids[V], inp(&b), now)
                };
                let size = match &r {
                    Ok(seq) => {
                        own_seqs.insert(*seq);
                        let key = StoreKey {
                            part: Part::OwnEvent(None),
                            author: w.key(V),
                            n: *seq,
                        };
                        v.store()
                            .list(&w.s)
                            .unwrap()
                            .into_iter()
                            .find(|(k, _)| *k == key)
                            .map(|(_, b)| 4 + b.len())
                    }
                    Err(AuditError::LogFull) => None,
                    Err(e) => return fail(format!("own call answered {e:?}")),
                };
                out.own.insert(i, (r, fb, size));
            }
            Op::Req(g, sz) => {
                if !peers {
                    continue_after(&mut out, &v, &w);
                    continue;
                }
                let gi = g as usize % 12;
                if gi == V {
                    continue_after(&mut out, &v, &w);
                    continue;
                }
                let b = body(sz);
                match v.record_for(&w.ids[V], &w.key(gi), inp(&b), now) {
                    Ok(seq) => {
                        req_seqs.insert(seq);
                        bump(c, "request accepted");
                        let s = cur[&gi];
                        let u = v.requested_usage(s);
                        let a = lim.requested_allowance();
                        if u.0 + CHECKPOINT_SLOT_MAX > a.0 || u.1 + 1 > a.1 {
                            return fail(format!(
                                "I-A13: request {seq} of slot {s} accepted without room for its \
                                 checkpoint: {u:?} of {a:?}"
                            ));
                        }
                    }
                    Err(AuditError::LogFull) => bump(c, "request refused LogFull"),
                    Err(AuditError::NotMember(_)) => bump(c, "request from a non-member refused"),
                    Err(e) => return fail(format!("request answered {e:?}")),
                }
            }
            Op::Cp | Op::CpNow => {
                if matches!(op, Op::CpNow) {
                    own_calls += 1;
                }
                let n = v.own().seq();
                let payer = payer_of(v.store(), &w.s, n);
                let r = if matches!(op, Op::Cp) {
                    v.checkpoint(&w.ids[V], now).map(|_| ())
                } else {
                    v.checkpoint_now(&w.ids[V], now).map(|_| ())
                };
                let r = match r {
                    Err(AuditError::NoSuchEvent(0)) if n == 0 => {
                        bump(c, "checkpoint with no own event (NoSuchEvent(0))");
                        Ok(())
                    }
                    x => x,
                };
                let after = model(v.store(), &w.s);
                let new = after.heads.len() > before.heads.len();
                match r {
                    Ok(()) if new => match payer {
                        Some(s) => {
                            bump(c, "checkpoint paid by an allowance");
                            let was = before.allow.get(&s).copied().unwrap_or((0, 0));
                            let is = after.allow.get(&s).copied().unwrap_or((0, 0));
                            if is.1 != was.1 + 1 || after.free != before.free {
                                return fail(format!(
                                    "checkpoint {n}: allowance {s} {was:?} -> {is:?}, free {:?} \
                                     -> {:?}",
                                    before.free, after.free
                                ));
                            }
                            if peers && cur.values().filter(|x| **x == s).count() == 0 {
                                bump(c, "checkpoint paid by the allowance of an EMPTY slot");
                            }
                        }
                        None => bump(c, "checkpoint paid by the free part"),
                    },
                    Ok(()) => {}
                    Err(AuditError::LogFull) => {
                        if after.free != before.free || after.allow != before.allow {
                            return fail(format!("refused checkpoint {n} changed the store"));
                        }
                        match (payer, lowered) {
                            (Some(_), true) => {
                                bump(c, "checkpoint refused: its allowance cannot pay (after Lower)")
                            }
                            (None, true) => {
                                bump(c, "checkpoint refused: free part full (after Lower)")
                            }
                            (p, false) => {
                                return fail(format!(
                                    "checkpoint {n} refused LogFull (payer {p:?}) although the \
                                     limits were never lowered"
                                ))
                            }
                        }
                    }
                    Err(e) => return fail(format!("checkpoint answered {e:?}")),
                }
            }
            Op::Remove(g) => {
                let gi = 2 + g as usize % 10;
                if cur.contains_key(&gi) && cur.len() > 3 {
                    let r = w.remove(gi);
                    if let Err(e) = v.apply_roster(&r) {
                        return fail(format!("removal refused: {e:?}"));
                    }
                    cur.remove(&gi);
                    bump(c, "removal");
                }
            }
            Op::ReAdd(g) => {
                let gi = 2 + g as usize % 10;
                if !cur.contains_key(&gi) {
                    let used: BTreeSet<u8> = cur.values().copied().collect();
                    if let Some(slot) = (0..8u8).find(|s| !used.contains(s)) {
                        let had = before.allow.get(&slot).copied().unwrap_or((0, 0));
                        let r = w.add(gi, slot);
                        if let Err(e) = v.apply_roster(&r) {
                            return fail(format!("add refused: {e:?}"));
                        }
                        cur.insert(gi, slot);
                        bump(c, "add into a free slot");
                        if had.1 > 0 {
                            bump(c, "slot changes hands with requested records in it");
                        }
                    }
                }
            }
            Op::Lower(k) => {
                let f = 4 + k as usize;
                lim = StoreLimits {
                    bytes: (lim.bytes * f / 8).max(8 * 600),
                    records: (lim.records * f / 8).max(8 * 4),
                };
                v.set_limits(lim);
                lowered = true;
                bump(c, "V lowers its limits");
            }
            Op::Resume => {
                let snap = (
                    v.free_usage(),
                    (0..8u8).map(|s| v.requested_usage(s)).collect::<Vec<_>>(),
                    format!("{:?}", v.status()),
                    v.anchor(),
                );
                let r = SessionAudit::resume(
                    v.store().clone(),
                    w.s,
                    &w.ids[V],
                    &w.ids[0].verified(),
                    pol,
                    Box::new(PatternRedactor),
                    now,
                );
                v = match r {
                    Ok(x) => x,
                    Err(e) => return fail(format!("resume refused: {e:?}")),
                };
                v.set_limits(lim);
                let again = (
                    v.free_usage(),
                    (0..8u8).map(|s| v.requested_usage(s)).collect::<Vec<_>>(),
                    format!("{:?}", v.status()),
                    v.anchor(),
                );
                if snap != again {
                    return fail(format!("resume changed the charges: {snap:?} -> {again:?}"));
                }
                bump(c, "resume");
            }
            Op::Tick => {}
        }
        // after every step
        let m = model(v.store(), &w.s);
        if v.free_usage() != m.free {
            return fail(format!(
                "(d1) step {i}: free_usage {:?} != model {:?}",
                v.free_usage(),
                m.free
            ));
        }
        for s in 0..8u8 {
            let mm = m.allow.get(&s).copied().unwrap_or((0, 0));
            if v.requested_usage(s) != mm {
                return fail(format!(
                    "step {i}: requested_usage({s}) {:?} != model {mm:?}",
                    v.requested_usage(s)
                ));
            }
            let was = before.allow.get(&s).copied().unwrap_or((0, 0));
            let a = lim.requested_allowance();
            if (mm.0 > was.0 || mm.1 > was.1) && (mm.0 > a.0 || mm.1 > a.1) {
                return fail(format!("step {i}: allowance {s} grew to {mm:?} above {a:?}"));
            }
        }
        if (m.free.0 > before.free.0 || m.free.1 > before.free.1)
            && (m.free.0 > lim.free_part().0 || m.free.1 > lim.free_part().1)
        {
            return fail(format!("step {i}: free part grew to {:?} above its limit", m.free));
        }
        if let Some(x) = m.own_none.iter().find(|n| !own_seqs.contains(*n)) {
            return fail(format!("(d1) step {i}: free-part event {x} is not an own choice"));
        }
        if let Some(x) = m.own_some.iter().find(|n| !req_seqs.contains(*n)) {
            return fail(format!("step {i}: allowance event {x} is not a request"));
        }
        if own_calls == 0 {
            bump(c, "step with no own call so far (d2)");
            if m.free != (0, 0) {
                return fail(format!("(d2) step {i}: free part {:?} with no own call", m.free));
            }
        }
        out.free_heads.push(m.free_heads);
        out.free.push(m.free);
    }
    Ok(out)
}

fn continue_after(out: &mut Out, v: &SessionAudit<MemStore>, w: &World) {
    let m = model(v.store(), &w.s);
    out.free_heads.push(m.free_heads);
    out.free.push(m.free);
}

thread_local! {
    static EXAMPLES: RefCell<Vec<String>> = const { RefCell::new(Vec::new()) };
}

#[test]
fn r5_prop_peers_request() {
    let cases: u32 = std::env::var("R5_CASES")
        .ok()
        .and_then(|s| s.parse().ok())
        .unwrap_or(96);
    let counts: RefCell<Counts> = RefCell::new(BTreeMap::new());
    let mut runner = TestRunner::new_with_rng(
        Config {
            cases,
            failure_persistence: None,
            ..Config::default()
        },
        proptest::test_runner::TestRng::deterministic_rng(proptest::test_runner::RngAlgorithm::ChaCha),
    );
    let strat = (
        (6_000usize..48_000, 24usize..128),
        (1u64..6, 20_000u64..200_000),
        prop::collection::vec(op(), 20..90),
    );
    let res = runner.run(&strat, |((sb, sr), (ev, ms), ops)| {
        let pol = CheckpointPolicy {
            every_events: ev,
            every_ms: ms,
        };
        let mut c = counts.borrow_mut();
        let a = run(&ops, (sb, sr), pol, true, &mut c)?;
        let mut cb = Counts::new();
        let b = run(&ops, (sb, sr), pol, false, &mut cb)?;
        let mut extra_before = false;
        for (i, (ra, fa, sa)) in &a.own {
            let (rb, fbb, sb2) = &b.own[i];
            match (ra, rb) {
                (Ok(qa), Ok(qb)) => {
                    bump(&mut c, "own call accepted in both runs");
                    let (za, zb) = (sa.unwrap(), sb2.unwrap());
                    if za > zb {
                        bump(&mut c, "own record larger with peers");
                    }
                    if za > zb + digits(*qa) - digits(*qb) {
                        return Err(TestCaseError::fail(format!(
                            "(d3) op {i}: own record {za} bytes (seq {qa}) with peers, {zb} (seq \
                             {qb}) without"
                        )));
                    }
                }
                (Err(_), Ok(_)) => {
                    if fa.0 > fbb.0 || fa.1 > fbb.1 {
                        bump(&mut c, "own call refused only with peers (free part fuller)");
                        if extra_before {
                            bump(&mut c, "  ... after an own record accepted only with peers");
                        } else {
                            bump(&mut c, "  ... with NO earlier own record accepted only with peers");
                        }
                        let ex = format!(
                            "own call refused only with peers at op {i}: free before {fa:?} with, \
                             {fbb:?} without; free-paid checkpoints {} with, {} without; ops {ops:?}",
                            a.free_heads[i.saturating_sub(1)],
                            b.free_heads[i.saturating_sub(1)]
                        );
                        EXAMPLES.with(|e| e.borrow_mut().push(ex));
                    } else {
                        return Err(TestCaseError::fail(format!(
                            "op {i}: own call refused with peers ({ra:?}) and accepted without, \
                             free part {fa:?} with, {fbb:?} without"
                        )));
                    }
                }
                (Ok(_), Err(_)) => {
                    extra_before = true;
                    bump(&mut c, "own call accepted only with peers")
                }
                _ => bump(&mut c, "own call refused in both runs"),
            }
        }
        if let Some(i) = (0..a.free_heads.len()).find(|i| a.free_heads[*i] > b.free_heads[*i]) {
            bump(&mut c, "MORE free-paid checkpoints with peers");
            let ex = format!(
                "more free-paid checkpoints with peers at op {i}: {} with, {} without; free {:?} \
                 with, {:?} without; policy {pol:?}; seat ({sb}, {sr}); ops {ops:?}",
                a.free_heads[i], b.free_heads[i], a.free[i], b.free[i]
            );
            EXAMPLES.with(|e| e.borrow_mut().push(ex));
        }
        Ok(())
    });
    let c = counts.into_inner();
    for (k, n) in &c {
        eprintln!("r5 reach: {k}: {n}");
    }
    EXAMPLES.with(|e| {
        let e = e.borrow();
        eprintln!("r5 examples: {}", e.len());
        for x in e.iter().take(3) {
            eprintln!("r5 example: {x}");
        }
    });
    if let Err(e) = res {
        panic!("r5 property: {e}");
    }
    for k in [
        "request accepted",
        "request refused LogFull",
        "checkpoint paid by an allowance",
        "checkpoint paid by the free part",
        "checkpoint refused: its allowance cannot pay (after Lower)",
        "slot changes hands with requested records in it",
        "resume",
        "step with no own call so far (d2)",
        "own record larger with peers",
    ] {
        assert!(c.get(k).copied().unwrap_or(0) > 0, "r5 property never reached: {k}");
    }
}

// =================================================================================================
// 2. A payer that cannot pay
// =================================================================================================

/// When the newest requested event's allowance cannot pay (here: after V lowered its own limits),
/// every later checkpoint has the same payer and is refused, so V's own later events are accepted
/// and never covered, until ANOTHER requester's request is accepted.
#[test]
fn r5_finding_a_payer_that_cannot_pay_blocks_every_later_checkpoint() {
    let w = World::new(0x62, 8, 8);
    let mut v = w.audit(V, every(1_000_000));
    let l = small(16 * 1024, 64);
    v.set_limits(l);
    let h = w.key(3);
    let g = w.key(2);
    v.record_for(&w.ids[V], &h, tiny(), t(1)).unwrap();
    let mut g_acc = 0;
    while v.record_for(&w.ids[V], &g, tiny(), t(2 + g_acc)).is_ok() {
        g_acc += 1;
    }
    let used = v.requested_usage(2);
    // the lowest record limit (multiples of 8) at which G's allowance cannot hold one more record
    let mut k = 64;
    while k > 8 && small(16 * 1024, k).requested_allowance().1 > used.1 {
        k -= 1;
    }
    let low = small(16 * 1024, k);
    v.set_limits(low);
    let cp0 = v.checkpoint_now(&w.ids[V], t(100)).map(|_| ());
    let (mut own_ok, mut cp_refused, mut cp_ok) = (0, 0, 0);
    for i in 0..20u64 {
        if v.record(&w.ids[V], tiny(), t(200 + i)).is_ok() {
            own_ok += 1;
        }
        match v.checkpoint_now(&w.ids[V], t(300 + i)) {
            Ok(_) => cp_ok += 1,
            Err(AuditError::LogFull) => cp_refused += 1,
            Err(e) => panic!("{e:?}"),
        }
    }
    let covered = v.own().checkpoints().last().map(|c| c.head.author_seq);
    let free = v.free_usage();
    // another requester, H, asks again
    let h2 = v.record_for(&w.ids[V], &h, tiny(), t(400));
    let cp_after_h = v.checkpoint_now(&w.ids[V], t(401)).map(|x| x.author_seq);
    eprintln!(
        "r5 block: G accepted {g_acc}, G's allowance {used:?}; V lowers its records to {} per seat \
         (allowance {:?}); first checkpoint {cp0:?}; then {own_ok} own records accepted, {cp_ok} \
         checkpoints Ok, {cp_refused} refused LogFull; newest covered own seq {covered:?} of {}; \
         free part {free:?} of {:?}; H's new request {h2:?}, checkpoint then {cp_after_h:?}",
        k,
        low.requested_allowance(),
        v.own().seq(),
        low.free_part()
    );
    assert_eq!(cp0, Err(AuditError::LogFull));
    assert!(
        own_ok > 0 && cp_refused == 20 && cp_ok == 0 && covered.is_none(),
        "block not shown"
    );
}

/// The same block with NO lowering is impossible: G fills its allowance (held back room), and every
/// checkpoint is paid, with own records between.
#[test]
fn r5_ok_without_lowering_every_checkpoint_after_requests_is_paid() {
    let w = World::new(0x63, 8, 8);
    let mut v = w.audit(V, every(1_000_000));
    v.set_limits(small(16 * 1024, 64));
    let mut refused = 0;
    let mut paid = 0;
    for i in 0..400u64 {
        let g = w.key(2 + (i as usize % 6));
        let _ = v.record_for(&w.ids[V], &g, tiny(), t(10 * i));
        if i % 3 == 0 {
            let _ = v.record(&w.ids[V], tiny(), t(10 * i + 1));
        }
        match v.checkpoint_now(&w.ids[V], t(10 * i + 2)) {
            Ok(_) => paid += 1,
            Err(AuditError::LogFull) => refused += 1,
            Err(e) => panic!("{e:?}"),
        }
    }
    eprintln!("r5 no lowering: {paid} checkpoint calls Ok, {refused} refused");
    assert_eq!(refused, 0);
}

/// Cost moved between requesters by I-A11 (newest pays): A's requests ride on H's checkpoints.
/// Bounded: H pays at most one checkpoint per request of its own.
#[test]
fn r5_newest_pays_a_requester_can_move_checkpoint_cost_onto_another() {
    let w = World::new(0x64, 8, 8);
    let mut v = w.audit(V, every(5));
    v.set_limits(small(32 * 1024, 256));
    let (a, h) = (w.key(2), w.key(3));
    let (mut a_ok, mut h_ok) = (0u64, 0u64);
    for i in 0..400u64 {
        for j in 0..4 {
            if v.record_for(&w.ids[V], &a, tiny(), t(100 * i + j)).is_ok() {
                a_ok += 1;
            }
        }
        if v.record_for(&w.ids[V], &h, tiny(), t(100 * i + 5)).is_ok() {
            h_ok += 1;
        }
        let _ = v.checkpoint(&w.ids[V], t(100 * i + 6));
    }
    let (ua, uh) = (v.requested_usage(2), v.requested_usage(3));
    let ev_a = v
        .store()
        .list(&w.s)
        .unwrap()
        .iter()
        .filter(|(k, _)| k.part == Part::OwnEvent(Some(2)))
        .count() as u64;
    let ev_h = v
        .store()
        .list(&w.s)
        .unwrap()
        .iter()
        .filter(|(k, _)| k.part == Part::OwnEvent(Some(3)))
        .count() as u64;
    let cp_a = ua.1 as u64 - ev_a;
    let cp_h = uh.1 as u64 - ev_h;
    eprintln!(
        "r5 newest pays: A accepted {a_ok} (allowance {ua:?}, checkpoints paid {cp_a}), H accepted \
         {h_ok} (allowance {uh:?}, checkpoints paid {cp_h})"
    );
    assert!(cp_h <= ev_h, "H paid more checkpoints than it made requests");
    assert!(cp_a < cp_h, "cost not moved");
}

// =================================================================================================
// 3. A peer makes an own-choice call refused: the re-used slot (R4-m2's state)
// =================================================================================================

fn reused_slot_run(requests: bool) -> (u64, u64, (usize, usize), (usize, usize)) {
    let mut w = World::new(0x65, 6, 5);
    let l = small(16 * 1024, 64);
    let mut v = w.audit(V, every(1_000_000));
    v.set_limits(l);
    let mut x = AuthorChain::new(&w.ids[2], w.s, every(1_000), Box::new(PatternRedactor), t(0));
    let s = "s".repeat(3_000);
    for i in 1..4u64 {
        x.append(&w.ids[2], input("x", &s, ""), t(i)).unwrap();
        v.receive(&w.ids[V], x.event(i).unwrap(), t(i)).unwrap();
    }
    for r in [w.remove(2), w.remove(V), w.add(V, 2), w.add(5, 1)] {
        v.apply_roster(&r).unwrap();
    }
    let mut req = 0;
    if requests {
        for i in 0..200u64 {
            let g = w.key([0, 3, 4, 5][i as usize % 4]);
            if v.record_for(&w.ids[V], &g, tiny(), t(100 + i)).is_ok() {
                req += 1;
            }
            let _ = v.checkpoint_now(&w.ids[V], t(100 + i));
        }
    }
    let mut own = 0;
    for i in 0..1_000u64 {
        if v.record(&w.ids[V], tiny(), t(1_000 + i)).is_err() {
            break;
        }
        own += 1;
    }
    (req, own, v.free_usage(), v.seat_usage(2))
}

#[test]
fn r5_finding_requests_refuse_own_records_in_a_reused_slot() {
    let with = reused_slot_run(true);
    let without = reused_slot_run(false);
    let l = small(16 * 1024, 64);
    eprintln!(
        "r5 reused slot: with requests {} accepted, then {} own records (free {:?}, seat 2 {:?}); \
         without requests {} own records (free {:?}, seat 2 {:?}); free part limit {:?}",
        with.0,
        with.1,
        with.2,
        with.3,
        without.1,
        without.2,
        without.3,
        l.free_part()
    );
    assert!(with.1 < without.1, "not shown");
}

// =================================================================================================
// 4. All or nothing, with a failing store (put and remove separately)
// =================================================================================================

#[derive(Clone)]
struct Failing {
    inner: MemStore,
    put: Rc<Cell<bool>>,
    rm: Rc<Cell<bool>>,
}

impl Store for Failing {
    fn put(&mut self, s: &SessionId, k: &StoreKey, r: &[u8]) -> Result<(), StoreError> {
        if self.put.get() {
            return Err(StoreError::Unavailable("r5: put fails"));
        }
        self.inner.put(s, k, r)
    }
    fn remove(&mut self, s: &SessionId, k: &StoreKey) -> Result<(), StoreError> {
        if self.rm.get() {
            return Err(StoreError::Unavailable("r5: remove fails"));
        }
        self.inner.remove(s, k)
    }
    fn list(&self, s: &SessionId) -> Result<Vec<(StoreKey, Vec<u8>)>, StoreError> {
        self.inner.list(s)
    }
}

struct F {
    put: Rc<Cell<bool>>,
    rm: Rc<Cell<bool>>,
}

fn failing(w: &World, i: usize, upto: usize) -> (SessionAudit<Failing>, F) {
    let put = Rc::new(Cell::new(false));
    let rm = Rc::new(Cell::new(false));
    let mut a = SessionAudit::start(
        Failing {
            inner: MemStore::new(),
            put: put.clone(),
            rm: rm.clone(),
        },
        &w.ids[i],
        &w.ids[0].verified(),
        &w.rosters[0],
        every(1_000),
        Box::new(PatternRedactor),
        t(0),
    )
    .unwrap();
    for r in &w.rosters[1..upto] {
        a.apply_roster(r).unwrap();
    }
    (a, F { put, rm })
}

fn snap(w: &World, v: &SessionAudit<Failing>) -> Vec<(&'static str, String)> {
    let peers: Vec<String> = (0..w.ids.len())
        .map(|i| format!("{:?}", v.peer(&w.key(i)).map(|c| (c.top_event_seq(), c.top_head()))))
        .collect();
    vec![
        ("store", format!("{:?}", v.store().list(&w.s).unwrap())),
        ("own seq", format!("{}", v.own().seq())),
        ("own checkpoints", format!("{:?}", v.own().checkpoints())),
        ("roster", format!("{}", v.roster().version())),
        ("status", format!("{:?}", v.status())),
        ("peers", format!("{peers:?}")),
        ("anchor", format!("{:?}", v.anchor())),
        ("free", format!("{:?}", v.free_usage())),
        (
            "requested",
            format!("{:?}", (0..8u8).map(|s| v.requested_usage(s)).collect::<Vec<_>>()),
        ),
    ]
}

fn whole(w: &World, v: &SessionAudit<Failing>, what: &str) {
    let b = v.export(&w.ids[V]).unwrap();
    assert!(verify(&b).is_ok(), "{what}: export does not verify");
    let r = SessionAudit::resume(
        v.store().clone(),
        w.s,
        &w.ids[V],
        &w.ids[0].verified(),
        every(1_000),
        Box::new(PatternRedactor),
        t(9_000_000),
    );
    assert!(r.is_ok(), "{what}: resume refused: {:?}", r.err());
    let a = SessionAudit::resume_with_anchor(
        v.store().clone(),
        &v.anchor(),
        w.s,
        &w.ids[V],
        &w.ids[0].verified(),
        every(1_000),
        Box::new(PatternRedactor),
        t(9_000_000),
    );
    assert!(a.is_ok(), "{what}: resume_with_anchor refused: {:?}", a.err());
}

fn refused_same<T: std::fmt::Debug>(
    w: &World,
    v: &mut SessionAudit<Failing>,
    f: &F,
    what: &str,
    call: impl FnOnce(&mut SessionAudit<Failing>) -> Result<T, AuditError>,
) {
    let before = snap(w, v);
    f.put.set(true);
    let r = call(v);
    f.put.set(false);
    assert!(matches!(r, Err(AuditError::Store(_))), "{what}: answered {r:?}");
    let after = snap(w, v);
    let diff: Vec<String> = before
        .iter()
        .zip(after.iter())
        .filter(|(a, b)| a != b)
        .map(|(a, b)| format!("{}: {} -> {}", a.0, &a.1[..a.1.len().min(300)], &b.1[..b.1.len().min(300)]))
        .collect();
    // Note r5-N: `chain_for` inserts an EMPTY received chain for a first-seen author before the
    // write; visible only through `peer()` as Some((None, None)). Accepted here, and printed.
    let only_empty_chain = diff.len() == 1
        && diff[0].starts_with("peers:")
        && before[5].1.matches("Some((None, None))").count() + 1
            == after[5].1.matches("Some((None, None))").count();
    if only_empty_chain {
        eprintln!("r5 all-or-nothing {what}: ONLY difference an empty received chain: {diff:?}");
    }
    assert!(
        diff.is_empty() || only_empty_chain,
        "{what}: the member changed although the write failed: {diff:?}"
    );
    eprintln!("r5 all-or-nothing {what}: refused {r:?}, member unchanged");
}

#[test]
fn r5_ok_all_or_nothing_on_every_write_path() {
    let mut w = World::new(0x66, 6, 4);
    let (mut v, f) = failing(&w, V, 1);
    let mut b = w.audit(2, every(1_000));
    // own record, requested record, announce
    refused_same(&w, &mut v, &f, "own record", |v| v.record(&w.ids[V], tiny(), t(1)));
    assert_eq!(v.record(&w.ids[V], tiny(), t(2)), Ok(1));
    refused_same(&w, &mut v, &f, "requested record", |v| {
        v.record_for(&w.ids[V], &w.key(3), tiny(), t(3))
    });
    assert_eq!(v.record_for(&w.ids[V], &w.key(3), tiny(), t(4)), Ok(2));
    // own checkpoint paid by an allowance
    refused_same(&w, &mut v, &f, "own checkpoint paid by an allowance", |v| {
        v.checkpoint_now(&w.ids[V], t(5))
    });
    let h1 = v.checkpoint_now(&w.ids[V], t(6)).unwrap();
    assert_eq!(h1.author_seq, 2);
    refused_same(&w, &mut v, &f, "announce", |v| {
        v.announce_share_level(&w.ids[V], w.key(2), ShareLevel::Summaries, t(7))
    });
    assert_eq!(
        v.announce_share_level(&w.ids[V], w.key(2), ShareLevel::Summaries, t(8)),
        Ok(3)
    );
    // free-paid checkpoint
    refused_same(&w, &mut v, &f, "own checkpoint paid by the free part", |v| {
        v.checkpoint_now(&w.ids[V], t(9))
    });
    let h2 = v.checkpoint_now(&w.ids[V], t(10)).unwrap();
    // countersignature
    let cs1 = b.receive_head(&w.ids[2], &h1).unwrap();
    refused_same(&w, &mut v, &f, "first countersignature", |v| v.add_countersignature(&cs1));
    v.add_countersignature(&cs1).unwrap();
    let cs2 = b.receive_head(&w.ids[2], &h2).unwrap();
    refused_same(&w, &mut v, &f, "newer countersignature", |v| v.add_countersignature(&cs2));
    v.add_countersignature(&cs2).unwrap();
    // received event, received checkpoint, fork evidence
    let mut a = AuthorChain::new(&w.ids[0], w.s, every(1_000), Box::new(PatternRedactor), t(0));
    for i in 1..4 {
        a.append(&w.ids[0], tiny(), t(i)).unwrap();
    }
    let ah = a.checkpoint_now(&w.ids[0], &w.valid(1), t(4)).unwrap();
    refused_same(&w, &mut v, &f, "received event", |v| {
        v.receive(&w.ids[V], a.event(1).unwrap(), t(11))
    });
    for i in 1..4 {
        v.receive(&w.ids[V], a.event(i).unwrap(), t(11)).unwrap();
    }
    refused_same(&w, &mut v, &f, "received checkpoint", |v| v.receive_head(&w.ids[V], &ah));
    v.receive_head(&w.ids[V], &ah).unwrap();
    let mut a2 = AuthorChain::new(&w.ids[0], w.s, every(1_000), Box::new(PatternRedactor), t(0));
    a2.append(&w.ids[0], input("other", "fork", ""), t(1)).unwrap();
    refused_same(&w, &mut v, &f, "fork evidence", |v| {
        v.receive(&w.ids[V], a2.event(1).unwrap(), t(12))
    });
    let fk = v.receive(&w.ids[V], a2.event(1).unwrap(), t(12));
    assert!(matches!(fk, Err(AuditError::Receive(_))), "fork answered {fk:?}");
    assert_eq!(
        v.store()
            .list(&w.s)
            .unwrap()
            .iter()
            .filter(|(k, _)| k.part == Part::Fixed(Table::Evidence))
            .count(),
        1
    );
    // cross-check record
    let hs = b.heads_seen(&w.ids[2]).unwrap();
    refused_same(&w, &mut v, &f, "cross-check record", |v| v.receive_heads_seen(&hs));
    v.receive_heads_seen(&hs).unwrap();
    // roster version, joiner's anchor
    let next = w.add(4, 4);
    refused_same(&w, &mut v, &f, "roster version", |v| v.apply_roster(&next));
    v.apply_roster(&next).unwrap();
    let mut j = AuthorChain::new(&w.ids[4], w.s, every(1_000), Box::new(PatternRedactor), t(0));
    j.append(&w.ids[4], tiny(), t(1)).unwrap();
    let anchor = j.checkpoint_now(&w.ids[4], &w.valid(2), t(2)).unwrap();
    refused_same(&w, &mut v, &f, "joiner's anchor", |v| v.join_author(&anchor));
    v.join_author(&anchor).unwrap();
    whole(&w, &v, "every path");
}

/// A refused NEWER roster version is stored first and removed again; if the REMOVE fails too, the
/// refused version stays in the store. What then?
#[test]
fn r5_finding_a_refused_roster_version_with_a_failing_remove_stays_in_the_store() {
    let mut w = World::new(0x67, 5, 4);
    let (mut v, f) = failing(&w, V, 1);
    v.record(&w.ids[V], tiny(), t(1)).unwrap();
    let next = w.add(4, 4);
    let gap = {
        let mut b = next.body.clone();
        b.version += 2;
        coagent_roster::sign(&w.ids[0], b).unwrap()
    };
    let before = v.store().list(&w.s).unwrap().len();
    f.rm.set(true);
    let r = v.apply_roster(&gap);
    f.rm.set(false);
    let after = v.store().list(&w.s).unwrap().len();
    let res = SessionAudit::resume(
        v.store().clone(),
        w.s,
        &w.ids[V],
        &w.ids[0].verified(),
        every(1_000),
        Box::new(PatternRedactor),
        t(10),
    )
    .map(|_| ());
    let next_ok = v.apply_roster(&next).map(|_| ());
    let res2 = SessionAudit::resume(
        v.store().clone(),
        w.s,
        &w.ids[V],
        &w.ids[0].verified(),
        every(1_000),
        Box::new(PatternRedactor),
        t(10),
    )
    .map(|_| ());
    let exp = verify(&v.export(&w.ids[V]).unwrap()).map(|_| ());
    eprintln!(
        "r5 refused version, remove failing: apply {r:?}; records {before} -> {after}; resume \
         {res:?}; the real next version then {next_ok:?}; resume {res2:?}; export verify {exp:?}"
    );
    assert!(after > before, "not shown: nothing left behind");
}

// =================================================================================================
// 5. The anchor
// =================================================================================================

fn resume_a(w: &World, st: &MemStore, a: &AuditAnchor) -> Result<(), AnchorError> {
    SessionAudit::resume_with_anchor(
        st.clone(),
        a,
        w.s,
        &w.ids[V],
        &w.ids[0].verified(),
        every(1_000),
        Box::new(PatternRedactor),
        t(9_000_000),
    )
    .map(|_| ())
}

/// A progression of stores and anchors; for every i < j: the store at i against the anchor at j
/// (an anchor NEWER than the store) is refused; the store at j against the anchor at i (older
/// anchor) is accepted. Then every record of the last store removed in turn, and every fixed
/// record with a byte flipped: refused.
#[test]
fn r5_ok_anchor_newer_than_store_refused_older_accepted_every_removal_named() {
    let mut w = World::new(0x68, 6, 4);
    let mut v = w.audit(V, every(1_000));
    let mut b = w.audit(2, every(1_000));
    let mut a = AuthorChain::new(&w.ids[0], w.s, every(1_000), Box::new(PatternRedactor), t(0));
    let mut snaps: Vec<(String, MemStore, AuditAnchor)> = Vec::new();
    let mut keep = |what: &str, v: &SessionAudit<MemStore>| {
        snaps.push((what.to_string(), v.store().clone(), v.anchor()));
    };
    keep("start", &v);
    v.record(&w.ids[V], tiny(), t(1)).unwrap();
    keep("own event", &v);
    v.record_for(&w.ids[V], &w.key(3), tiny(), t(2)).unwrap();
    keep("requested event", &v);
    let h1 = v.checkpoint_now(&w.ids[V], t(3)).unwrap();
    keep("own checkpoint (allowance)", &v);
    a.append(&w.ids[0], tiny(), t(4)).unwrap();
    v.receive(&w.ids[V], a.event(1).unwrap(), t(4)).unwrap();
    keep("peer event 1", &v);
    a.append(&w.ids[0], tiny(), t(5)).unwrap();
    v.receive(&w.ids[V], a.event(2).unwrap(), t(5)).unwrap();
    keep("peer event 2", &v);
    let ah = a.checkpoint_now(&w.ids[0], &w.valid(1), t(6)).unwrap();
    v.receive_head(&w.ids[V], &ah).unwrap();
    keep("peer checkpoint", &v);
    let cs1 = b.receive_head(&w.ids[2], &h1).unwrap();
    v.add_countersignature(&cs1).unwrap();
    keep("countersignature 1", &v);
    let hs1 = b.heads_seen(&w.ids[2]).unwrap();
    v.receive_heads_seen(&hs1).unwrap();
    keep("cross-check 1", &v);
    v.record(&w.ids[V], tiny(), t(7)).unwrap();
    let h2 = v.checkpoint_now(&w.ids[V], t(8)).unwrap();
    keep("own checkpoint (free)", &v);
    let cs2 = b.receive_head(&w.ids[2], &h2).unwrap();
    v.add_countersignature(&cs2).unwrap();
    keep("countersignature 2 (replaces)", &v);
    let hs2 = b.heads_seen(&w.ids[2]).unwrap();
    v.receive_heads_seen(&hs2).unwrap();
    keep("cross-check 2 (replaces)", &v);
    let mut a2 = AuthorChain::new(&w.ids[0], w.s, every(1_000), Box::new(PatternRedactor), t(0));
    a2.append(&w.ids[0], input("other", "fork", ""), t(1)).unwrap();
    let _ = v.receive(&w.ids[V], a2.event(1).unwrap(), t(9));
    keep("evidence", &v);
    let r = w.add(4, 4);
    v.apply_roster(&r).unwrap();
    keep("roster version 2", &v);
    let mut j = AuthorChain::new(&w.ids[4], w.s, every(1_000), Box::new(PatternRedactor), t(0));
    j.append(&w.ids[4], tiny(), t(1)).unwrap();
    let anc = j.checkpoint_now(&w.ids[4], &w.valid(2), t(2)).unwrap();
    v.join_author(&anc).unwrap();
    keep("joiner's anchor", &v);
    let n = snaps.len();
    let (mut newer_refused, mut older_ok, mut same) = (0, 0, 0);
    let mut kinds: BTreeMap<String, u64> = BTreeMap::new();
    for i in 0..n {
        for jx in 0..n {
            let (wi, si, _) = &snaps[i];
            let (wj, _, aj) = &snaps[jx];
            let r = resume_a(&w, si, aj);
            if i < jx {
                assert!(
                    r.is_err(),
                    "anchor at '{wj}' accepted the older store at '{wi}'"
                );
                newer_refused += 1;
                let k = format!("{:?}", r.unwrap_err());
                let k = k.split([' ', '{', '(']).next().unwrap().to_string();
                *kinds.entry(k).or_default() += 1;
            } else {
                assert!(r.is_ok(), "anchor at '{wj}' refused the store at '{wi}': {r:?}");
                if i == jx {
                    same += 1;
                } else {
                    older_ok += 1;
                }
            }
        }
    }
    eprintln!(
        "r5 anchor progression: {n} states; newer anchor refused {newer_refused} ({kinds:?}); older \
         anchor accepted {older_ok}; same {same}"
    );
    // every record of the last store removed in turn; every fixed record with a byte flipped
    let (_, last, anchor) = snaps.last().unwrap().clone();
    let list = last.list(&w.s).unwrap();
    let (mut removed_named, mut flipped_refused) = (0, 0);
    for (k, _) in &list {
        let mut st = last.clone();
        st.remove(&w.s, k).unwrap();
        let r = resume_a(&w, &st, &anchor);
        let named = match &r {
            Err(AnchorError::Missing { part, author, .. })
            | Err(AnchorError::Behind { part, author, .. }) => *part == k.part && *author == k.author,
            _ => false,
        };
        assert!(named, "removing {k:?}: {r:?}");
        removed_named += 1;
    }
    for (k, rec) in &list {
        if !matches!(k.part, Part::Fixed(_)) {
            continue;
        }
        let mut st = last.clone();
        let mut bad = rec.clone();
        let p = bad.len() / 2;
        bad[p] ^= 0x01;
        st.put(&w.s, k, &bad).unwrap();
        let r = resume_a(&w, &st, &anchor);
        assert!(r.is_err(), "a flipped fixed record {k:?} accepted");
        flipped_refused += 1;
    }
    eprintln!(
        "r5 anchor: {} records; each removal refused and named {removed_named}; fixed records \
         flipped and refused {flipped_refused}",
        list.len()
    );
}

/// The anchor at its bounds: the largest encoding is within MAX_ANCHOR_BYTES and reads back; one
/// more run or slot is refused.
#[test]
fn r5_ok_the_anchor_is_bounded() {
    let k = |i: usize| KeyId([i as u8; 32]);
    let mut runs = Vec::new();
    let parts: Vec<Part> = (0..8u8)
        .flat_map(|s| [Part::PeerEvent(s), Part::PeerHead(s)])
        .collect();
    'outer: for p in &parts {
        for i in 0..32 {
            if runs.len() == MAX_ANCHOR_RUNS {
                break 'outer;
            }
            runs.push(AnchorRun {
                part: *p,
                author: k(i),
                count: u64::MAX,
                newest: u64::MAX,
            });
        }
    }
    while runs.len() < MAX_ANCHOR_RUNS {
        runs.push(AnchorRun {
            part: Part::OwnEvent(None),
            author: k(255),
            count: u64::MAX,
            newest: u64::MAX,
        });
    }
    let slots: Vec<AnchorSlot> = (0..MAX_ANCHOR_SLOTS)
        .map(|i| AnchorSlot {
            key: StoreKey {
                part: Part::Fixed(Table::HeadsSeen),
                author: KeyId([255; 32]),
                n: u64::MAX - i as u64,
            },
            digest: Digest32([255; 32]),
            order: (u64::MAX, u64::MAX),
        })
        .collect();
    let a = AuditAnchor {
        session_id: session(0x69),
        runs: runs.clone(),
        slots: slots.clone(),
    };
    let bytes = a.to_bytes();
    let back = AuditAnchor::from_bytes(&bytes);
    let mut more = a.clone();
    more.runs.push(runs[0].clone());
    let more_r = AuditAnchor::from_bytes(&more.to_bytes()).map(|_| ());
    let mut more_s = a.clone();
    more_s.slots.push(slots[0].clone());
    let more_s_r = AuditAnchor::from_bytes(&more_s.to_bytes()).map(|_| ());
    eprintln!(
        "r5 anchor bound: largest anchor {} bytes (MAX_ANCHOR_BYTES {MAX_ANCHOR_BYTES}); reads back \
         {}; one run more {more_r:?}; one slot more {more_s_r:?}",
        bytes.len(),
        back.as_ref().is_ok_and(|b| *b == a)
    );
    assert!(bytes.len() <= MAX_ANCHOR_BYTES);
    assert_eq!(back, Ok(a));
    assert!(more_r.is_err() && more_s_r.is_err());
}

// =================================================================================================
// 6. Release, default limits: the (d3) width bound against the seat's 1 percent
// =================================================================================================

fn requests_then_own(requests: bool) -> (u64, Vec<u64>, usize) {
    let w = World::new(0x51, 8, 8);
    let mut v = w.audit(V, CheckpointPolicy::default());
    let requesters: Vec<usize> = (0..8).filter(|i| *i != V).collect();
    let (mut m, mut refused) = (0u64, 0u32);
    let mut acc = 0;
    while requests && refused < 14 {
        m += 1;
        let now = t(m * 60_000);
        let g = requesters[(m as usize) % requesters.len()];
        if v.record_for(&w.ids[V], &w.key(g), tiny(), now).is_ok() {
            acc += 1;
            refused = 0;
        } else {
            refused += 1;
        }
        let _ = v.checkpoint(&w.ids[V], now);
    }
    let free0 = v.free_usage().0;
    if requests {
        let (mut ev, mut alw) = ((0usize, 0usize), (0usize, 0usize));
        for (k, r) in v.store().list(&w.s).unwrap() {
            if let Part::OwnEvent(Some(_)) = k.part {
                ev = add(ev, (4 + r.len(), 1));
            }
        }
        for s in 0..8u8 {
            alw = add(alw, v.requested_usage(s));
        }
        eprintln!(
            "r5 allowances at default limits: {acc} requests; all allowances {alw:?}, of which \
             requested events {ev:?} ({}% of the bytes) and checkpoints {:?}; one allowance {:?}",
            ev.0 * 100 / alw.0,
            (alw.0 - ev.0, alw.1 - ev.1),
            v.limits().requested_allowance()
        );
    }
    let mut seqs = Vec::new();
    loop {
        m += 1;
        match v.record(&w.ids[V], tiny(), t(m * 60_000)) {
            Ok(s) => seqs.push(s),
            Err(AuditError::LogFull) => break,
            Err(e) => panic!("{e:?}"),
        }
    }
    (acc, seqs, free0)
}

#[test]
#[ignore = "release: cargo test --release --test gate_r5 -- --ignored"]
fn r5_release_width_bound_default_limits() {
    let (acc, with, free_with) = requests_then_own(true);
    let (_, without, _) = requests_then_own(false);
    let lost = without.len() - with.len();
    // (d3): each own record is larger by at most the width difference of its sequence number
    let extra: usize = with
        .iter()
        .zip(without.iter())
        .map(|(a, b)| digits(*a) - digits(*b))
        .sum();
    let tiny_size = {
        let w = World::new(0x51, 8, 8);
        let mut v = w.audit(V, CheckpointPolicy::default());
        v.record(&w.ids[V], tiny(), t(1)).unwrap();
        v.free_usage().0
    };
    let derived = extra.div_ceil(tiny_size - 4) + 1;
    eprintln!(
        "r5 width bound: {acc} requests; free part before own records {free_with}; own records \
         {} with, {} without; lost {lost}; sum of width differences {extra} bytes; one tiny own \
         record ~{tiny_size} bytes; derived bound {derived} records; seat's 1% bound {}",
        with.len(),
        without.len(),
        without.len() / 100
    );
    assert_eq!(free_with, 0);
    assert!(lost <= derived, "lost {lost} > derived {derived}");
}

// =================================================================================================
// 7. Guards for the anchor checks my mutants R18, R23, R26 showed unguarded (each passes on the
//    branch; each goes red under its mutant)
// =================================================================================================

/// R18: a replaced slot holding a DIFFERENT record of the SAME order (here: the same member's
/// countersignature of the same checkpoint with another `held_from`, a valid signature, so plain
/// `resume` accepts it) is refused against the anchor.
#[test]
fn r5_guard_a_same_order_different_record_in_a_replaced_slot_is_refused() {
    let w = World::new(0x6a, 4, 4);
    let mut v = w.audit(V, every(1_000));
    let mut b = w.audit(2, every(1_000));
    v.record(&w.ids[V], tiny(), t(1)).unwrap();
    let h = v.checkpoint_now(&w.ids[V], t(2)).unwrap();
    let cs = b.receive_head(&w.ids[2], &h).unwrap();
    v.add_countersignature(&cs).unwrap();
    let anchor = v.anchor();
    let other = h
        .countersign_held(&w.ids[2], if cs.held_from.is_some() { None } else { Some(1) })
        .unwrap();
    let other_held = other.held_from;
    assert_ne!(other, cs, "the swapped countersignature must differ");
    let key = v
        .store()
        .list(&w.s)
        .unwrap()
        .into_iter()
        .find(|(k, _)| k.part == Part::Fixed(Table::Attestation))
        .unwrap()
        .0;
    let mut st = v.store().clone();
    st.put(
        &w.s,
        &key,
        &coagent_proto::canonical::encode(&coagent_audit::bundle::Record::Countersig(other)).unwrap(),
    )
    .unwrap();
    let plain = SessionAudit::resume(
        st.clone(),
        w.s,
        &w.ids[V],
        &w.ids[0].verified(),
        every(1_000),
        Box::new(PatternRedactor),
        t(9),
    )
    .map(|_| ());
    let r = resume_a(&w, &st, &anchor);
    eprintln!("r5 R18 guard: cs held_from {:?} swapped for {:?}; plain resume {plain:?}; with anchor {r:?}", cs.held_from, other_held);
    assert!(
        matches!(r, Err(AnchorError::Older { .. })),
        "a same-order different record was accepted: {r:?}"
    );
}

/// R23: an anchor encoding above MAX_ANCHOR_BYTES is refused even when it would parse (a valid
/// anchor followed by whitespace).
#[test]
fn r5_guard_an_oversized_anchor_encoding_is_refused() {
    let w = World::new(0x6b, 3, 3);
    let v = w.audit(V, every(1_000));
    let mut b = v.anchor().to_bytes();
    assert!(AuditAnchor::from_bytes(&b).is_ok());
    b.resize(MAX_ANCHOR_BYTES + 1, b' ');
    let r = AuditAnchor::from_bytes(&b).map(|_| ());
    eprintln!("r5 R23 guard: {} bytes -> {r:?}", b.len());
    assert_eq!(r, Err(AnchorError::Malformed("too large")));
}

/// R26: a newer roster version that the roster crate refuses is written and removed again; the
/// anchor taken afterwards must not name it, so the member restarts from its (good) store.
#[test]
fn r5_guard_an_anchor_after_a_refused_roster_version_accepts_the_store() {
    let mut w = World::new(0x6c, 5, 4);
    let mut v = w.audit(V, every(1_000));
    v.record(&w.ids[V], tiny(), t(1)).unwrap();
    let next = w.add(4, 4);
    let gap = {
        let mut b = next.body.clone();
        b.version += 2;
        coagent_roster::sign(&w.ids[0], b).unwrap()
    };
    assert!(v.apply_roster(&gap).is_err());
    let r = resume_a(&w, v.store(), &v.anchor());
    eprintln!("r5 R26 guard: after a refused version, resume_with_anchor {r:?}");
    assert_eq!(r, Ok(()), "a good store was refused against its own anchor");
}
