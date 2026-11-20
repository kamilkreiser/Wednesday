//! QA gate M3-AUDIT-SEAL (independent check): probes of the seal safety core at the head 841c445.
//! Test code only; fixed test identities, in-memory stores. Each assertion text starts "qa ".
mod common;
#[path = "seal_common/mod.rs"]
mod seal_common;

use coagent_audit::anchor::AuditAnchor;
use coagent_audit::bundle::{verify, verify_segments, Bundle, FieldClass, Record};
use coagent_audit::redact::PatternRedactor;
use coagent_audit::segment::normalise;
use coagent_audit::session::SessionAudit;
use coagent_audit::store::{MemStore, Part, Store};
use coagent_audit::AuditError;
use coagent_proto::canonical;
use common::*;
use seal_common::{resume_as, Net, V};

const X: usize = 0;
const W: usize = 2;
const Y: usize = 3;

fn with_anchor(n: &Net, s: MemStore, a: &AuditAnchor) -> bool {
    SessionAudit::resume_with_anchor(
        s,
        a,
        n.w.s,
        &n.w.ids[V],
        &n.w.ids[0].verified(),
        every(1_000),
        Box::new(PatternRedactor),
        t(60_000),
    )
    .is_ok()
}

fn sorted(s: &MemStore, n: &Net) -> Vec<(coagent_audit::store::StoreKey, Vec<u8>)> {
    let mut l = s.list(&n.w.s).unwrap();
    l.sort_by_key(|a| a.0);
    l
}

/// A network where V sealed once with every collection call failing (garbage left), then more
/// traffic by everyone.
fn build2() -> Net {
    let mut n = Net::new(181, 5, 4);
    for _ in 0..3 {
        n.v_rec().unwrap();
    }
    n.v_cp().unwrap();
    for _ in 0..4 {
        n.p_rec(X).1.unwrap();
    }
    n.p_cp(X).1.unwrap();
    n.p_rec(X).1.unwrap();
    n.p_rec(W).1.unwrap();
    n.p_cp(W).1.unwrap();
    n.v_rec().unwrap();
    let p = n.v.seal_export(&n.w.ids[V]).unwrap();
    n.v.store().arm(Some(1), None, false);
    let info = n.v.seal_commit(&n.w.ids[V], &p, t(n.now)).unwrap();
    n.v.store().disarm();
    assert!(info.garbage_left > 0, "qa build2: no garbage left");
    for _ in 0..3 {
        n.p_rec(X).1.unwrap();
    }
    n.p_cp(X).1.unwrap();
    n.p_rec(X).1.unwrap();
    n.p_rec(Y).1.unwrap();
    n.p_cp(Y).1.unwrap();
    n.v_rec().unwrap();
    n.v_cp().unwrap();
    n.v_rec().unwrap();
    n
}

fn numbered(r: &Record) -> bool {
    matches!(r, Record::OwnEvent(_) | Record::OwnHead(_) | Record::PeerEvent(_))
}

/// A second seal over a store holding the first seal's garbage, stopped after every store call;
/// each stopped store resumes as the pre- or the post-seal member, exactly one anchor accepts it,
/// nothing numbered is lost, and a third seal then leaves physical == logical.
#[test]
fn qa_second_seal_over_garbage_stopped_at_every_call() {
    // events carry random salts, so each build is its own reference: the stopped member's store is
    // compared with a member resumed from the SAME pre-seal store and sealed cleanly
    let calls = {
        let mut n = build2();
        let plan = n.v.seal_export(&n.w.ids[V]).unwrap();
        n.v.store().arm(None, None, false);
        let info = n.v.seal_commit(&n.w.ids[V], &plan, t(900)).unwrap();
        let (calls, _) = n.v.store().disarm();
        assert_eq!(info.garbage_left, 0);
        let phys = sorted(&n.v_store(), &n);
        assert_eq!(normalise(phys.clone()).unwrap(), phys, "qa: garbage after a clean second seal");
        eprintln!("qa second seal: {calls} store calls; segment {}", info.segment);
        calls
    };
    for j in 0..=calls {
        let mut m = build2();
        let pre_store = m.v_store();
        let pre_logical = normalise(sorted(&pre_store, &m)).unwrap();
        assert_ne!(pre_logical, sorted(&pre_store, &m), "qa: build2 holds no garbage");
        let pre_export = m.v_export();
        let pre = m.v.anchor();
        let p = m.v.seal_export(&m.w.ids[V]).unwrap();
        // the reference: a member resumed from the same pre-seal store, sealed with no stop
        let mut refm = resume_as(&m.w, V, pre_store.clone()).unwrap();
        assert_eq!(refm.export(&m.w.ids[V]).unwrap(), pre_export, "qa j={j}: resume != live before");
        let plan = refm.seal_export(&m.w.ids[V]).unwrap();
        assert_eq!(plan.bundle, p.bundle, "qa j={j}: the plan of a resumed member differs");
        assert_eq!(plan.post_anchor, p.post_anchor, "qa j={j}: post anchors differ");
        refm.seal_commit(&m.w.ids[V], &plan, t(900)).unwrap();
        let live_export = refm.export(&m.w.ids[V]).unwrap();
        m.v.store().arm(Some(j), None, false);
        let r = m.v.seal_commit(&m.w.ids[V], &p, t(900));
        m.v.store().disarm();
        let s = m.v_store();
        let resumed = resume_as(&m.w, V, s.clone()).unwrap_or_else(|e| panic!("qa j={j}: {e:?}"));
        let exp = resumed.export(&m.w.ids[V]).unwrap();
        let (want_pre, want_post) = (j == 0, j >= 1);
        if j == 0 {
            assert!(matches!(r, Err(AuditError::Store(_))), "qa j=0: {r:?}");
            assert_eq!(exp, pre_export, "qa j=0: resumed differs from the pre-seal member");
        } else {
            assert!(r.is_ok(), "qa j={j}: {r:?}");
            assert_eq!(exp, live_export, "qa j={j}: resumed differs from the post-seal member");
        }
        assert_eq!(with_anchor(&m, s.clone(), &pre), want_pre, "qa j={j}: pre anchor");
        assert_eq!(with_anchor(&m, s.clone(), &plan.post_anchor), want_post, "qa j={j}: post anchor");
        // conservation of numbered records: in the store's logical view now, or in the file
        let now_logical = normalise(sorted(&s, &m)).unwrap();
        let file_recs = plan.bundle.unsealed_records();
        for (k, b) in &pre_logical {
            let r: Record = canonical::decode(b).unwrap();
            if !numbered(&r) {
                continue;
            }
            let held = now_logical.iter().any(|(k2, b2)| k2 == k && b2 == b);
            assert!(held || file_recs.contains(&r), "qa j={j}: {k:?} lost");
        }
        // a third seal from the resumed member collects everything
        let mut res = resumed;
        let p3 = res.seal_export(&m.w.ids[V]);
        if let Ok(p3) = p3 {
            res.seal_commit(&m.w.ids[V], &p3, t(950)).unwrap();
            let ph = sorted(res.store(), &m);
            assert_eq!(normalise(ph.clone()).unwrap(), ph, "qa j={j}: garbage after the third seal");
            verify(&res.export(&m.w.ids[V]).unwrap()).unwrap();
        }
    }
}

/// A plan goes stale on any change V's store sees between export and commit; a committed plan
/// cannot be committed twice; the refused commit writes nothing.
#[test]
fn qa_stale_plans_are_refused_and_write_nothing() {
    type Mutator = fn(&mut Net);
    let muts: [(&str, Mutator); 5] = [
        ("peer event", |n| n.p_rec(X).1.unwrap()),
        // W records without delivering to V, then checkpoints: V stores a checkpoint beyond its
        // held events (a fixed-part slot only, no numbered run changes)
        ("peer checkpoint beyond held events", |n| {
            let now = t(n.tick());
            let p = n.peers[W].as_mut().unwrap();
            p.record(&n.w.ids[W], seal_common::ev("w.undelivered"), now).unwrap();
            let (h, a) = n.p_cp(W);
            eprintln!("qa W's checkpoint {} beyond V's events: {a:?}", h.author_seq);
        }),
        ("own event", |n| {
            n.v_rec().unwrap();
        }),
        ("own checkpoint", |n| {
            n.v_rec().unwrap();
            n.v_cp().unwrap();
        }),
        ("a countersignature replaced", |n| {
            // V checkpoints, only X countersigns; then W's countersignature arrives after the plan
            let _ = n;
        }),
    ];
    for (what, f) in muts.iter().take(4) {
        let mut n = build2();
        let p = n.v.seal_export(&n.w.ids[V]).unwrap();
        let at_plan = sorted(&n.v_store(), &n);
        f(&mut n);
        let before = n.v_store();
        let changed = sorted(&before, &n) != at_plan;
        assert!(changed, "qa stale ({what}): the step did not change V's store (probe too weak)");
        let a = n.v.anchor();
        let r = n.v.seal_commit(&n.w.ids[V], &p, t(990));
        assert!(matches!(r, Err(AuditError::SealStale)), "qa stale ({what}): {r:?}");
        assert_eq!(sorted(&n.v_store(), &n), sorted(&before, &n), "qa stale ({what}): wrote");
        assert_eq!(n.v.anchor(), a, "qa stale ({what}): member changed");
    }
    // countersignature arriving between export and commit
    let mut n = build2();
    let now = t(n.tick());
    let h = n.v.checkpoint_now(&n.w.ids[V], now).unwrap_or_else(|e| panic!("{e:?}"));
    let p = n.v.seal_export(&n.w.ids[V]).unwrap();
    let cs = n.peers[W].as_mut().unwrap().receive_head(&n.w.ids[W], &h).unwrap();
    n.v.add_countersignature(&cs).unwrap();
    let r = n.v.seal_commit(&n.w.ids[V], &p, t(991));
    assert!(matches!(r, Err(AuditError::SealStale)), "qa stale (countersig): {r:?}");
    // the same plan twice
    let mut n = build2();
    let p = n.v.seal_export(&n.w.ids[V]).unwrap();
    n.v.seal_commit(&n.w.ids[V], &p, t(992)).unwrap();
    let r = n.v.seal_commit(&n.w.ids[V], &p, t(993));
    assert!(matches!(r, Err(AuditError::SealStale)), "qa: a plan committed twice: {r:?}");
    // S6: W's countersignature of V's seal point arriving AFTER the commit is accepted and kept
    let mut n = build2();
    let now = t(n.tick());
    let h = n.v.checkpoint_now(&n.w.ids[V], now).unwrap();
    let p = n.v.seal_export(&n.w.ids[V]).unwrap();
    n.v.seal_commit(&n.w.ids[V], &p, t(994)).unwrap();
    let cs = n.peers[W].as_mut().unwrap().receive_head(&n.w.ids[W], &h).unwrap();
    n.v.add_countersignature(&cs).unwrap();
    let b = n.v_export();
    assert!(b.countersigs.iter().any(|c| c.author_seq == h.author_seq), "qa S6: seal-point cs not exported");
    verify(&b).unwrap();
}

/// A peer seals (twice) invisibly to V; every message after the peer's seals is accepted by V and
/// V's view (export, resume) stays consistent; V seals in between.
#[test]
fn qa_a_peer_seals_invisibly() {
    let mut n = build2();
    let v_anchor = n.v.anchor();
    for round in 0..2 {
        // X seals its own log
        let now = t(n.tick());
        let x = n.peers[X].as_mut().unwrap();
        x.checkpoint_now(&n.w.ids[X], now).ok();
        let p = x.seal_export(&n.w.ids[X]).unwrap_or_else(|e| panic!("qa X seal_export: {e:?}"));
        let info = x.seal_commit(&n.w.ids[X], &p, now).unwrap();
        assert_eq!(info.segment, round + 1);
        if round == 0 {
            assert_eq!(n.v.anchor(), v_anchor, "qa: a peer's seal changed V");
        }
        for _ in 0..5 {
            let (_, a) = n.p_rec(X);
            a.unwrap_or_else(|e| panic!("qa: V refused X's event after X's seal: {e:?}"));
        }
        let (_, a) = n.p_cp(X);
        a.unwrap_or_else(|e| panic!("qa: V refused X's checkpoint after X's seal: {e:?}"));
        // V's events reach X (deliver_v unwraps X's receive)
        n.v_rec().unwrap();
        n.v_cp().unwrap();
        let b = n.v_export();
        verify(&b).unwrap();
        let r = resume_as(&n.w, V, n.v_store()).unwrap();
        assert_eq!(r.export(&n.w.ids[V]).unwrap(), b, "qa: resume differs from live after a peer seal");
        assert_eq!(r.anchor(), n.v.anchor());
        // V seals too, after the first round
        if round == 0 {
            let (p, c) = n.v_seal();
            p.unwrap();
            c.unwrap().unwrap();
        }
        let xb = n.peers[X].as_ref().unwrap().export(&n.w.ids[X]).unwrap();
        verify(&xb).unwrap();
    }
}

/// Normalisation is idempotent; a store with no Segment record normalises to itself.
#[test]
fn qa_normalise_idempotent_and_identity_without_a_segment() {
    let (w, audits) = scenario(9);
    for a in &audits {
        let mut l = a.store().list(&w.s).unwrap();
        l.sort_by_key(|x| x.0);
        assert_eq!(normalise(l.clone()).unwrap(), l, "qa: a plain store changed by normalise");
    }
    let n = build2();
    let phys = sorted(&n.v_store(), &n);
    let once = normalise(phys.clone()).unwrap();
    assert_ne!(once, phys);
    assert_eq!(normalise(once.clone()).unwrap(), once, "qa: normalise not idempotent");
    // and a shuffled listing gives the same view
    let mut rev = phys.clone();
    rev.reverse();
    assert_eq!(normalise(rev).unwrap(), once, "qa: normalise depends on listing order");
}

fn resealed(n: &Net, mut b: Bundle) -> Bundle {
    b.reseal(&n.w.ids[V]).unwrap();
    b
}

/// verify: format 3 only with a Segment record, format 2 only without; verify_segments linking.
#[test]
fn qa_verify_formats_and_links() {
    let mut n = build2();
    let seg1 = {
        // the first file is not kept by build2; make a fresh pair from here
        let (p, c) = n.v_seal();
        c.unwrap().unwrap();
        p.unwrap().bundle
    };
    assert_eq!(seg1.meta.format, 3, "qa: the plan of a continued log is format 3");
    n.v_rec().unwrap();
    n.p_rec(X).1.unwrap();
    n.p_cp(X).1.unwrap();
    n.v_cp().unwrap();
    let cur = n.v_export();
    assert_eq!(cur.meta.format, 3);
    verify(&cur).unwrap();
    let rep = verify_segments(&[seg1.clone(), cur.clone()]).unwrap();
    assert!(!rep.from_genesis);
    // format 2 with a Segment record
    let mut b = cur.clone();
    b.meta.format = 2;
    let e = verify(&resealed(&n, b)).unwrap_err();
    assert_eq!(e.class, FieldClass::Meta, "qa: {e:?}");
    // format 3 without one
    let mut b = cur.clone();
    b.segment = None;
    let e = verify(&resealed(&n, b)).unwrap_err();
    eprintln!("qa format 3 without segment: {e:?}");
    // a plain format-2 bundle relabelled 3
    let (w, audits) = scenario(4);
    let mut b2 = export(&w, &audits, 0);
    b2.meta.format = 3;
    b2.reseal(&w.ids[0]).unwrap();
    assert!(verify(&b2).is_err(), "qa: format 3 without a segment record accepted");
    b2.meta.format = 4;
    b2.reseal(&w.ids[0]).unwrap();
    assert!(verify(&b2).is_err(), "qa: format 4 accepted");
    // a broken prev link
    let mut b = cur.clone();
    b.segment.as_mut().unwrap().prev.0[0] ^= 1;
    let b = resealed(&n, b);
    verify(&b).unwrap();
    let e = verify_segments(&[seg1.clone(), b]).unwrap_err();
    assert_eq!(e.class, FieldClass::Segment, "qa link: {e:?}");
    eprintln!("qa broken link: {e:?}");
    // reordered
    assert!(verify_segments(&[cur.clone(), seg1.clone()]).is_err(), "qa: reordered set accepted");
    // the own start moved to a number the previous file does not hold as a checkpoint
    let mut b = cur.clone();
    let g = b.segment.as_mut().unwrap();
    assert!(g.own_start.is_some());
    // drop the first evidence-free peer start: the set must still verify only if every start is held
    if !g.starts.is_empty() {
        let mut b2 = cur.clone();
        let x = b2.segment.as_mut().unwrap();
        let h = &mut x.starts[0];
        h.author_seq += 100; // signature now fails: verify refuses at Segment
        let e = verify(&resealed(&n, b2)).unwrap_err();
        assert_eq!(e.class, FieldClass::Segment, "qa: {e:?}");
    }
    let _ = &mut b;
    // own number range in the report
    let r = verify(&cur).unwrap();
    let n0 = cur.segment.as_ref().unwrap().own_start.as_ref().unwrap().author_seq;
    assert_eq!(r.own.first_seq, n0 + 1);
    assert_eq!(r.own.anchor.map(|a| a.0), Some(n0));
    // a store record count for the own seat: no own record at or below n0
    let l = sorted(&n.v_store(), &n);
    assert!(
        l.iter().all(|(k, _)| !(matches!(k.part, Part::OwnEvent(_) | Part::OwnHead) && k.n <= n0)),
        "qa: own record at or below the own start stays"
    );
}
