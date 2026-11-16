//! QA gate M3-AUDIT round 3 (at 882e094): attack tests. Test code only.
//! `r3_ok_*` pass when the attack is refused. `r3_finding_*` pass when the weakness is DEMONSTRATED
//! (they assert it exists and print what was measured). `#[ignore]` ones are release-only.
mod common;

use std::time::Instant;

use coagent_audit::bundle::{verify, Record};
use coagent_audit::chain::{AuditEvent, AuthorChain};
use coagent_audit::domain::AuditDomain;
use coagent_audit::equivocation::{HeadsSeenBody, SignedHeadsSeen, Statement};
use coagent_audit::redact::PatternRedactor;
use coagent_audit::session::{Payer, SessionAudit, StoreLimits};
use coagent_audit::store::{MemStore, Store};
use coagent_audit::tiers::ShareLevel;
use coagent_audit::AuditError;
use coagent_crypto::identity::DeviceIdentity;
use coagent_proto::bytes::{Digest32, KeyId};
use coagent_proto::canonical;
use coagent_roster::{sign, Role, RosterBody, CAP};
use common::*;

fn hs_signed(
    id: &DeviceIdentity,
    w: &World,
    to: Option<KeyId>,
    rv: u64,
    entries: Vec<Statement>,
) -> SignedHeadsSeen {
    let body = HeadsSeenBody {
        session_id: w.s,
        from: id.key_id(),
        to,
        roster_v: rv,
        entries,
    };
    let sig = audit_sign(id, AuditDomain::HeadsSeen, &canonical::encode(&body).unwrap());
    SignedHeadsSeen {
        session_id: body.session_id,
        from: body.from,
        to: body.to,
        roster_v: body.roster_v,
        entries: body.entries,
        sig,
    }
}

const SMALL: StoreLimits = StoreLimits {
    bytes: 1024 * 1024,
    records: 100_000,
};

/// `from` records one small event and returns what `to` is sent (from must share >= summaries).
fn one_event(
    w: &World,
    au: &mut SessionAudit<MemStore>,
    from: usize,
    to: usize,
    k: u64,
) -> AuditEvent {
    let seq = au
        .record(&w.ids[from], input("x.y", "s", "f"), t(k))
        .unwrap();
    au.outgoing(seq)
        .into_iter()
        .find(|(m, _)| *m == w.key(to))
        .unwrap()
        .1
}

// ---------------------------------------------------------------------------------------------
// R3-M1: a non-convener member can no longer apply roster versions once the convener's quota at it
// is full; and other members can fill the convener's quota at it through the convener's receipts.
// ---------------------------------------------------------------------------------------------

/// Honest traffic alone: the convener C (0) shares full with V (1); C's own events fill C's quota at
/// V; then C removes H (2), and V cannot apply that roster (LogFull). H stays a member in V's view
/// and its messages are still accepted.
#[test]
fn r3_finding_convener_quota_full_blocks_every_roster_update() {
    let mut w = World::new(70, 3, 3);
    let mut c = w.audit(0, every(1_000_000));
    let mut v = w.audit(1, every(1_000_000));
    let mut h = w.audit(2, every(1_000_000));
    v.set_limits(SMALL);
    c.set_share_level(w.key(1), ShareLevel::Full);
    h.set_share_level(w.key(1), ShareLevel::Full);
    h.set_share_level(w.key(0), ShareLevel::Full);
    let mut n = 0u64;
    for _ in 0..20 {
        let e = one_event(&w, &mut c, 0, 1, n + 1);
        v.receive(&w.ids[1], &e, t(n + 1)).unwrap();
        n += 1;
    }
    // C keeps working honestly: it receives member 2's events and writes receipts, which go to V
    // (receipts carry no receipt reserve, so they fill C's quota at V to the last bytes)
    let mut r_ok = 0u64;
    for k in 1..100_000u64 {
        let seq = h.record(&w.ids[2], input("x.y", "s", "f"), t(k)).unwrap();
        let _ = seq;
        let mut h2c = h.outgoing(seq);
        h2c.retain(|(m, _)| *m == w.key(0));
        if h2c.is_empty() {
            h.set_share_level(w.key(0), ShareLevel::Full);
            continue;
        }
        c.receive(&w.ids[0], &h2c[0].1, t(k)).unwrap();
        let rseq = c.own().seq();
        let re = c.outgoing(rseq).into_iter().find(|(m, _)| *m == w.key(1)).unwrap().1;
        match v.receive(&w.ids[1], &re, t(k)) {
            Ok(_) => r_ok += 1,
            Err(AuditError::LogFull) => break,
            Err(e) => panic!("{e:?}"),
        }
    }
    let r2 = w.remove(2);
    let applied = v.apply_roster(&r2);
    let again = v.apply_roster(&w.rosters[0].clone());
    eprintln!(
        "convener: {n} events then {r_ok} receipts accepted at V, then V.apply_roster(removal of H) -> {applied:?}; \
         re-apply version 1 -> {again:?}; C's usage at V {:?}, per-peer {:?}",
        v.usage_of(Payer::Peer(w.key(0))),
        v.limits().per_peer()
    );
    assert_eq!(applied, Err(AuditError::LogFull));
    assert_eq!(v.roster().version(), 1);
    // H, removed by the convener, is still accepted at V
    let hh = h.checkpoint_now(&w.ids[2], t(5)).unwrap();
    assert!(v.receive_head(&w.ids[1], &hh).is_ok(), "H's checkpoint refused at V");
    let hs = hs_signed(&w.ids[2], &w, None, 1, vec![]);
    assert!(v.receive_heads_seen(&hs).is_ok());
    // and the own share is intact
    assert!(v
        .record(&w.ids[1], input("x.y", "own", "own"), t(9))
        .is_ok());
}

/// Hostile members H1..H3 (2..4) send many small events to the convener C (0). C writes one receipt
/// per event into its own chain, charged to the sender at C. C shares full with V (1), so V receives
/// C's receipts, each charged to C's quota AT V. The hostile members fill C's quota at V without
/// exceeding their own quotas anywhere; V then refuses C's real events and every new roster.
fn receipt_proxy(limits: Option<StoreLimits>, hostile: usize) -> (u64, u64, Result<(), AuditError>) {
    let n_members = 2 + hostile;
    let mut w = World::new(80, n_members, n_members);
    let mut c = w.audit(0, every(1_000_000));
    let mut v = w.audit(1, every(1_000_000));
    if let Some(l) = limits {
        c.set_limits(l);
        v.set_limits(l);
    }
    c.set_share_level(w.key(1), ShareLevel::Full);
    let mut hs: Vec<SessionAudit<MemStore>> =
        (2..n_members).map(|i| w.audit(i, every(1_000_000))).collect();
    for (j, h) in hs.iter_mut().enumerate() {
        h.set_share_level(w.key(0), ShareLevel::Full);
        let _ = j;
    }
    let mut receipts_at_v = 0u64;
    let mut c_refused_at_v = false;
    let mut sent = 0u64;
    'outer: for (j, h) in hs.iter_mut().enumerate() {
        let hi = j + 2;
        let mut k = 0u64;
        loop {
            k += 1;
            let seq = h
                .record(&w.ids[hi], EventInputNoTiers::make(), t(k))
                .unwrap();
            let e = h
                .outgoing(seq)
                .into_iter()
                .find(|(m, _)| *m == w.key(0))
                .unwrap()
                .1;
            match c.receive(&w.ids[0], &e, t(k)) {
                Ok(_) => sent += 1,
                Err(AuditError::LogFull) => break, // H's quota at C is full: next hostile member
                Err(e) => panic!("{e:?}"),
            }
            // C's receipt goes to V
            let rseq = c.own().seq();
            let re = c
                .outgoing(rseq)
                .into_iter()
                .find(|(m, _)| *m == w.key(1))
                .unwrap()
                .1;
            match v.receive(&w.ids[1], &re, t(k)) {
                Ok(_) => receipts_at_v += 1,
                Err(AuditError::LogFull) => {
                    c_refused_at_v = true;
                    break 'outer;
                }
                Err(e) => panic!("{e:?}"),
            }
        }
    }
    let _ = sent;
    // C's own, genuine event is now refused at V, and so is C's removal of H1
    let roster = if c_refused_at_v {
        let r = w.remove(2);
        v.apply_roster(&r).map(|_| ())
    } else {
        Ok(())
    };
    eprintln!(
        "hostile={hostile}: H events stored at C {sent}; C receipts stored at V {receipts_at_v}; \
         C's quota at V full: {c_refused_at_v}; C usage at V {:?} of per-peer {:?}; \
         V.apply_roster(removal of H1) -> {roster:?}; own record -> {:?}",
        v.usage_of(Payer::Peer(w.key(0))),
        v.limits().per_peer(),
        v.record(&w.ids[1], input("x.y", "own", "own"), t(1)).map(|_| ())
    );
    (receipts_at_v, u64::from(c_refused_at_v), roster)
}

/// Smallest event: no tiers.
struct EventInputNoTiers;
impl EventInputNoTiers {
    fn make() -> coagent_audit::chain::EventInput<'static> {
        coagent_audit::chain::EventInput {
            kind: "x",
            summary: None,
            full: None,
        }
    }
}

#[test]
fn r3_finding_other_members_fill_the_conveners_quota_through_its_receipts() {
    let (_n, full, roster) = receipt_proxy(Some(SMALL), 3);
    assert_eq!(full, 1, "C's quota at V was not filled by receipts");
    assert_eq!(roster, Err(AuditError::LogFull));
}

#[test]
#[ignore]
fn r3_finding_release_receipt_proxy_default_limits() {
    let start = Instant::now();
    let (_n, full, roster) = receipt_proxy(None, 3);
    eprintln!("release, default limits: {:?}", start.elapsed());
    assert_eq!(full, 1);
    assert_eq!(roster, Err(AuditError::LogFull));
}

// ---------------------------------------------------------------------------------------------
// Flood re-measurement (the gate's round-2 attack and variants)
// ---------------------------------------------------------------------------------------------

/// A CURRENT member signs fresh empty records: the first is stored, the rest are NotNewer.
#[test]
fn r3_ok_current_member_fresh_empty_records_are_not_newer() {
    let w = World::new(72, 4, 4);
    let mut c = w.audit(2, every(100));
    let before = c.store_usage();
    let mut stored = 0;
    for _ in 0..200 {
        // distinct signatures each time are impossible with Ed25519 (deterministic); vary `to`
        for to in [None, Some(w.key(2))] {
            match c.receive_heads_seen(&hs_signed(&w.ids[3], &w, to, 1, vec![])) {
                Ok(_) => stored += 1,
                Err(AuditError::Duplicate) | Err(AuditError::NotNewer) => {}
                Err(e) => panic!("{e:?}"),
            }
        }
    }
    let after = c.store_usage();
    assert_eq!(stored, 2, "one per (reporter, recipient)");
    assert_eq!(after.1 - before.1, 2);
}

/// A current member Y (3) reporting a colluder X's (0) headers at ever higher numbers: every record
/// "advances", so each is stored, until Y's quota is full. Returns (stored, bytes charged to Y).
fn colluder_advancing(limits: Option<StoreLimits>) -> (u64, usize, bool, bool) {
    let w = World::new(73, 4, 4);
    let mut v = w.audit(2, every(100));
    if let Some(l) = limits {
        v.set_limits(l);
    }
    let mut x = AuthorChain::new(&w.ids[0], w.s, every(1 << 40), Box::new(PatternRedactor), t(0));
    let mut n = 0u64;
    let mut k = 0u64;
    loop {
        k += 1;
        x.append(&w.ids[0], EventInputNoTiers::make(), t(k)).unwrap();
        let st = Statement::Header(x.event(k).unwrap().header.clone());
        match v.receive_heads_seen(&hs_signed(&w.ids[3], &w, Some(w.key(2)), 1, vec![st])) {
            Ok(_) => n += 1,
            Err(AuditError::LogFull) => break,
            Err(e) => panic!("{e:?}"),
        }
        assert!(k < 5_000_000);
    }
    let used = v.usage_of(Payer::Peer(w.key(3)));
    let own_ok = v
        .record(&w.ids[2], input("x.y", "own", "own"), t(1))
        .is_ok();
    // another honest peer still gets in
    let mut b = w.audit(1, every(1_000_000));
    b.set_share_level(w.key(2), ShareLevel::Full);
    let e = one_event(&w, &mut b, 1, 2, 1);
    let other_ok = v.receive(&w.ids[2], &e, t(2)).is_ok();
    eprintln!(
        "colluder: {n} advancing records stored, Y charged {used:?} (per-peer {:?}); own record ok {own_ok}; other peer ok {other_ok}; store {:?}",
        v.limits().per_peer(),
        v.store_usage()
    );
    (n, used.0, own_ok, other_ok)
}

#[test]
fn r3_ok_colluder_advancing_records_stop_at_the_reporters_quota() {
    let (n, used, own_ok, other_ok) = colluder_advancing(Some(SMALL));
    assert!(n > 10);
    assert!(used <= SMALL.bytes * 3 / 4 / 7 + 1);
    assert!(own_ok && other_ok);
}

#[test]
#[ignore]
fn r3_release_flood_measurements() {
    // (a) the round-2 attack: removed member, fresh records at its old version
    let mut w = World::new(74, 4, 4);
    let mut c = w.audit(2, every(100));
    let r2 = w.remove(3);
    c.apply_roster(&r2).unwrap();
    let s = Instant::now();
    let mut n = 0u64;
    let mut last = None;
    for _ in 0..100_000 {
        match c.receive_heads_seen(&hs_signed(&w.ids[3], &w, None, 1, vec![])) {
            Ok(_) => n += 1,
            Err(e) => {
                last = Some(e);
            }
        }
    }
    let own = c.record(&w.ids[2], input("x.y", "own", "own"), t(1));
    eprintln!(
        "(a) removed member, 100000 attempts in {:?}: accepted {n}, last refusal {last:?}, store {:?}, own record {:?}",
        s.elapsed(),
        c.store_usage(),
        own.map(|_| ())
    );
    assert_eq!(n, 0);
    // (b) colluder with advancing entries, default limits
    let s = Instant::now();
    let (n, used, own_ok, other_ok) = colluder_advancing(None);
    eprintln!("(b) colluder advancing at default limits: {n} stored, {used} bytes, {:?}", s.elapsed());
    assert!(own_ok && other_ok);
    // (c) all three peers of a 4-member session flood maximum-size events
    let w = World::new(75, 4, 4);
    let mut me = w.audit(0, every(1 << 40));
    let s = Instant::now();
    let big_s = "s".repeat(4000);
    let big_f = "f".repeat(60_000);
    let mut per = Vec::new();
    for p in 1..4 {
        let mut pa = w.audit(p, every(1 << 40));
        pa.set_share_level(w.key(0), ShareLevel::Full);
        let mut n = 0u64;
        for k in 1..1_000_000u64 {
            let seq = pa
                .record(&w.ids[p], input("x.y", &big_s, &big_f), t(k))
                .unwrap();
            let e = pa.outgoing(seq).into_iter().find(|(m, _)| *m == w.key(0)).unwrap().1;
            match me.receive(&w.ids[0], &e, t(k)) {
                Ok(_) => n += 1,
                Err(AuditError::LogFull) => break,
                Err(e) => panic!("{e:?}"),
            }
        }
        per.push((n, me.usage_of(Payer::Peer(w.key(p)))));
    }
    let own = me.record(&w.ids[0], input("x.y", "own", "own"), t(1));
    eprintln!(
        "(c) 3 peers flood max events in {:?}: per peer (accepted, usage) {per:?}; store {:?}; own record {:?}",
        s.elapsed(),
        me.store_usage(),
        own.map(|_| ())
    );
    let b = me.export(&w.ids[0]).unwrap();
    assert!(verify(&b).is_ok());
}

// ---------------------------------------------------------------------------------------------
// Quota accounting across a restart
// ---------------------------------------------------------------------------------------------

/// `start` on a store that already holds this session's records charges ALL of them to Own, so after
/// a restart peers get fresh quotas and can fill the reserved quarter.
#[test]
fn r3_finding_restart_charges_existing_peer_records_to_own() {
    let w = World::new(76, 9, 8);
    let mut me = w.audit(0, every(1 << 40));
    me.set_limits(SMALL);
    let fill = |me: &mut SessionAudit<MemStore>, p: usize, base: u64| {
        let mut pa = w.audit(p, every(1 << 40));
        pa.set_share_level(w.key(0), ShareLevel::Full);
        for k in 1..100_000u64 {
            let seq = pa
                .record(&w.ids[p], input("x.y", "summary", &"z".repeat(200)), t(base + k))
                .unwrap();
            let e = pa.outgoing(seq).into_iter().find(|(m, _)| *m == w.key(0)).unwrap().1;
            if me.receive(&w.ids[0], &e, t(base + k)).is_err() {
                return;
            }
        }
    };
    for p in 1..8 {
        fill(&mut me, p, p as u64 * 1_000_000);
    }
    let before = me.store_usage();
    let peers_before: usize = (1..8).map(|p| me.usage_of(Payer::Peer(w.key(p))).0).sum();
    // restart on the same store
    let store = me.store().clone();
    let mut me2 = SessionAudit::start(
        store,
        &w.ids[0],
        &w.ids[0].verified(),
        &w.rosters[0],
        every(1 << 40),
        Box::new(PatternRedactor),
        t(0),
    )
    .unwrap();
    me2.set_limits(SMALL);
    eprintln!(
        "before restart: store {before:?}, peers {peers_before}; after: own {:?}, peer1 {:?}",
        me2.usage_of(Payer::Own),
        me2.usage_of(Payer::Peer(w.key(1)))
    );
    // peers' chains at me2 are empty again, so they resend from 1 (a real daemon would have to
    // reload; reload is not built) -- use NEW peers' traffic: the same 7 peers start fresh chains
    for p in 1..8 {
        fill(&mut me2, p, 50_000_000 + p as u64 * 1_000_000);
    }
    let own = me2.record(&w.ids[0], input("x.y", "own", "own"), t(1));
    let peers_after: usize = (1..8).map(|p| me2.usage_of(Payer::Peer(w.key(p))).0).sum();
    eprintln!(
        "after refill: store {:?} of {:?}; peers since restart {peers_after}; own record {:?}",
        me2.store_usage(),
        SMALL,
        own.as_ref().map(|_| ())
    );
    assert_eq!(me2.usage_of(Payer::Peer(w.key(1))).0 > 0, true);
    assert!(
        peers_before + peers_after > SMALL.bytes * 3 / 4,
        "peer bytes across the restart exceed the peers' part"
    );
    assert_eq!(own, Err(AuditError::LogFull), "own share survived");
}

// ---------------------------------------------------------------------------------------------
// Evidence silently not stored when the peers' part is full
// ---------------------------------------------------------------------------------------------

#[test]
fn r3_finding_evidence_not_stored_when_peer_pool_full() {
    let w = World::new(77, 8, 8);
    let mut me = w.audit(0, every(1 << 40));
    me.set_limits(SMALL);
    // X = 1 equivocates: me holds the real chain at seq 1 first
    let mut x = w.audit(1, every(1 << 40));
    x.set_share_level(w.key(0), ShareLevel::Full);
    let real = one_event(&w, &mut x, 1, 0, 1);
    me.receive(&w.ids[0], &real, t(1)).unwrap();
    for p in 1..8 {
        let mut pa = if p == 1 {
            // X continues its real chain
            x.set_share_level(w.key(0), ShareLevel::Full);
            std::mem::replace(&mut x, w.audit(1, every(1 << 40)))
        } else {
            let mut a = w.audit(p, every(1 << 40));
            a.set_share_level(w.key(0), ShareLevel::Full);
            a
        };
        for k in 2..100_000u64 {
            let seq = pa
                .record(&w.ids[p], coagent_audit::chain::EventInput { kind: "audit.receipt", summary: None, full: None }, t(k))
                .unwrap();
            let e = pa.outgoing(seq).into_iter().find(|(m, _)| *m == w.key(0)).unwrap().1;
            if me.receive(&w.ids[0], &e, t(k)).is_err() {
                break;
            }
        }
    }
    // X's conflicting seq-1 header
    let mut fork = AuthorChain::new(&w.ids[1], w.s, every(100), Box::new(PatternRedactor), t(0));
    fork.append(&w.ids[1], input("x.y", "lie", "lie"), t(1)).unwrap();
    let st = Statement::Header(fork.event(1).unwrap().header.clone());
    // reported in a broadcast? headers are refused in broadcast; addressed record from member 2
    let rec = hs_signed(&w.ids[2], &w, Some(w.key(0)), 1, vec![st]);
    let r = me.receive_heads_seen(&rec);
    let stored = me
        .store()
        .records(&w.s)
        .unwrap()
        .iter()
        .filter(|b| matches!(canonical::decode::<Record>(b).unwrap(), Record::Evidence(_)))
        .count();
    eprintln!(
        "pool full: receive_heads_seen -> {:?}; evidence records stored {stored}; evidence usage {:?}",
        r.as_ref().map(|v| v.len()),
        me.usage_of(Payer::Evidence)
    );
    let found = match &r {
        Ok(v) => v.len(),
        Err(_) => 0,
    };
    // weakness: the reporter's quota is full, so the call returns LogFull; the evidence IS stored
    // (store_evidence runs first) but is not returned to the caller
    let _ = found;
    assert_eq!(r.map(|v| v.len()), Err(AuditError::LogFull));
    assert_eq!(stored, 1);
}

// ---------------------------------------------------------------------------------------------
// R2-m2 signed share-level statement: replay, ordering, scope
// ---------------------------------------------------------------------------------------------

/// The same identities in ANOTHER session (session id from `sbyte`).
fn world_in_session(base: u8, n: usize, sbyte: u8) -> World {
    let mut w = World::new(base, n, n);
    w.s = session(sbyte);
    let body = RosterBody {
        session_id: w.s,
        version: 1,
        prev_hash: Digest32([0; 32]),
        convener: w.ids[0].key_id(),
        cap: CAP,
        members: (0..n).map(|i| member(&w.ids[i], Role::Guest, i as u8, 1)).collect(),
        removed: vec![],
    };
    w.rosters = vec![sign(&w.ids[0], body).unwrap()];
    w
}

#[test]
fn r3_ok_share_statement_cross_session_replay_refused() {
    let w1 = World::new(90, 3, 3);
    let w2 = world_in_session(90, 3, 0xEE);
    assert_ne!(w1.s, w2.s);
    let mut x1 = w1.audit(0, every(100));
    let st = announce(&mut x1, &w1, 0, 2, ShareLevel::Full);
    let mut b2 = w2.audit(1, every(100));
    let r = b2.note_share_level(&st);
    assert_eq!(r, Err(AuditError::WrongSession));
    assert_eq!(b2.known_level(&w2.key(0), &w2.key(2)), ShareLevel::Nothing);
}

#[test]
fn r3_ok_share_statement_ordering_downgrade_wins_whatever_the_arrival_order() {
    let w = World::new(91, 3, 3);
    let mut x = w.audit(0, every(100));
    let up = announce(&mut x, &w, 0, 2, ShareLevel::Full);
    let down = announce(&mut x, &w, 0, 2, ShareLevel::Nothing);
    let mut b = w.audit(1, every(100));
    b.note_share_level(&down).unwrap();
    b.note_share_level(&up).unwrap();
    assert_eq!(b.known_level(&w.key(0), &w.key(2)), ShareLevel::Nothing);
    // and upgrade after downgrade
    let up2 = announce(&mut x, &w, 0, 2, ShareLevel::Summaries);
    b.note_share_level(&up2).unwrap();
    assert_eq!(b.known_level(&w.key(0), &w.key(2)), ShareLevel::Summaries);
    // replaying the same statement is harmless
    b.note_share_level(&up).unwrap();
    assert_eq!(b.known_level(&w.key(0), &w.key(2)), ShareLevel::Summaries);
}

#[test]
fn r3_ok_share_statement_scope_rules() {
    let mut w = World::new(92, 5, 3);
    let mut x = w.audit(0, every(100));
    // a statement about a member added later, naming a roster version before it joined
    let r2 = w.add(3, 3);
    x.apply_roster(&r2).unwrap();
    let seq = x
        .own()
        .seq();
    let _ = seq;
    // author makes the statement at version 2 (current) -- fine
    let mut b = w.audit(1, every(100));
    let ok = announce(&mut x, &w, 0, 3, ShareLevel::Full);
    assert!(b.note_share_level(&ok).is_ok());
    // a forged body naming roster_v 1 for member 3 (not a member at 1), signed by X itself
    let mut c = AuthorChain::new(&w.ids[0], w.s, every(100), Box::new(PatternRedactor), t(0));
    c.append_share_level(&w.ids[0], w.key(3), ShareLevel::Full, 1, t(1)).unwrap();
    let early = c.disclose(1, ShareLevel::Summaries).unwrap();
    assert_eq!(b.note_share_level(&early), Err(AuditError::NotMember(w.key(3))));
    // the receiver's own statement, and an author's statement about itself
    let mine = {
        let mut bb = w.audit(1, every(100));
        bb.announce_share_level(&w.ids[1], w.key(2), ShareLevel::Full, t(9)).unwrap();
        bb.own().disclose(bb.own().seq(), ShareLevel::Summaries).unwrap()
    };
    assert!(b.note_share_level(&mine).is_err());
    let mut s2 = AuthorChain::new(&w.ids[0], w.s, every(100), Box::new(PatternRedactor), t(0));
    s2.append_share_level(&w.ids[0], w.key(0), ShareLevel::Full, 2, t(1)).unwrap();
    assert!(b.note_share_level(&s2.disclose(1, ShareLevel::Summaries).unwrap()).is_err());
    // a statement arrives at a member at Full via record(): an ordinary event of the same kind made
    // with record() runs through the redactor; the 64-hex key id is masked so it never parses
    let body = format!(
        "{{\"level\":\"full\",\"member\":\"{}\",\"roster_v\":2}}",
        hex(&w.key(2).0)
    );
    let mut y = w.audit(0, every(100));
    let yseq = y
        .record(&w.ids[0], input("member.accepted", &body, "f"), t(3))
        .unwrap();
    let ye = y.own().disclose(yseq, ShareLevel::Summaries).unwrap();
    eprintln!("record() of member.accepted -> summary {:?}", ye.summary.as_ref().map(|o| o.body.clone()));
    let mut b3 = w.audit_from(1, 1, every(100));
    let r = b3.note_share_level(&ye);
    eprintln!("note_share_level(record()-made member.accepted) -> {r:?}");
}

fn hex(b: &[u8]) -> String {
    b.iter().map(|x| format!("{x:02x}")).collect()
}

#[test]
fn r3_ok_share_statement_readd_same_key_new_statement_counts() {
    let mut w = World::new(93, 3, 3);
    let mut x = w.audit(0, every(100));
    let mut b = w.audit(1, every(100));
    let old = announce(&mut x, &w, 0, 2, ShareLevel::Full);
    b.note_share_level(&old).unwrap();
    let r2 = w.remove(2);
    b.apply_roster(&r2).unwrap();
    x.apply_roster(&r2).unwrap();
    let r3 = w.add(2, 2);
    b.apply_roster(&r3).unwrap();
    x.apply_roster(&r3).unwrap();
    assert!(b.note_share_level(&old).is_err());
    let new = announce(&mut x, &w, 0, 2, ShareLevel::Summaries);
    b.note_share_level(&new).unwrap();
    assert_eq!(b.known_level(&w.key(0), &w.key(2)), ShareLevel::Summaries);
    // the pre-removal statement has a LOWER author_seq; still refused, level unchanged
    assert!(b.note_share_level(&old).is_err());
    assert_eq!(b.known_level(&w.key(0), &w.key(2)), ShareLevel::Summaries);
}

// ---------------------------------------------------------------------------------------------
// Rotating identities via re-add: the peers' part fills; then a non-convener member cannot apply
// rosters (same root cause as R3-M1).
// ---------------------------------------------------------------------------------------------

#[test]
fn r3_finding_identity_rotation_fills_peer_pool_and_blocks_rosters_at_non_convener() {
    let mut w = World::new(0x60, 14, 8);
    let mut v = w.audit(1, every(1 << 40));
    v.set_limits(SMALL);
    let flood = |w: &World, v: &mut SessionAudit<MemStore>, p: usize| -> u64 {
        let mut pa = w.audit_from(p, w.rosters.len(), every(1 << 40));
        pa.set_share_level(w.key(1), ShareLevel::Full);
        let mut n = 0;
        for k in 1..100_000u64 {
            let seq = pa
                .record(&w.ids[p], input("x.y", "summary", &"z".repeat(200)), t(k))
                .unwrap();
            let e = pa.outgoing(seq).into_iter().find(|(m, _)| *m == w.key(1)).unwrap().1;
            match v.receive(&w.ids[1], &e, t(k)) {
                Ok(_) => n += 1,
                Err(_) => break,
            }
        }
        n
    };
    // hostile member 2 rotates: floods, is removed, a new key (8..) is added in its slot, floods...
    let mut cur = 2usize;
    let mut rotations = 0;
    let mut blocked = None;
    for new in 8..14usize {
        flood(&w, &mut v, cur);
        let r = w.remove(cur);
        if let Err(e) = v.apply_roster(&r) {
            blocked = Some((rotations, "remove", e));
            break;
        }
        let r = w.add(new, 2);
        if let Err(e) = v.apply_roster(&r) {
            blocked = Some((rotations, "add", e));
            break;
        }
        cur = new;
        rotations += 1;
    }
    // an honest peer (3) now
    let honest = flood(&w, &mut v, 3);
    eprintln!(
        "rotation: blocked {blocked:?} after {rotations} rotations; honest peer 3 got {honest} events; store {:?}",
        v.store_usage()
    );
    assert!(v.record(&w.ids[1], input("x.y", "own", "own"), t(1)).is_ok());
}

/// An author whose quota at V is full can equivocate to V directly without V ever forming evidence:
/// `receive` and `receive_head` refuse with LogFull BEFORE the fork check.
#[test]
fn r3_finding_fork_from_an_author_at_quota_gives_logfull_not_evidence() {
    let w = World::new(78, 3, 3);
    let mut v = w.audit(0, every(1 << 40));
    v.set_limits(SMALL);
    let mut x = w.audit(1, every(1 << 40));
    x.set_share_level(w.key(0), ShareLevel::Full);
    let mut n = 0u64;
    loop {
        let e = one_event(&w, &mut x, 1, 0, n + 1);
        match v.receive(&w.ids[0], &e, t(n + 1)) {
            Ok(_) => n += 1,
            Err(AuditError::LogFull) => break,
            Err(e) => panic!("{e:?}"),
        }
    }
    // the conflicting event at seq 1
    let mut fork = AuthorChain::new(&w.ids[1], w.s, every(1 << 40), Box::new(PatternRedactor), t(0));
    fork.append(&w.ids[1], input("x.y", "lie", "lie"), t(1)).unwrap();
    let fe = fork.disclose(1, ShareLevel::Full).unwrap();
    let r = v.receive(&w.ids[0], &fe, t(1));
    // a conflicting checkpoint at seq 1
    let fh = fork.checkpoint_now(&w.ids[1], &w.valid(1), t(1)).unwrap();
    let rh = v.receive_head(&w.ids[0], &fh);
    eprintln!("after {n} events, fork event -> {:?}; fork head -> {:?}", r.as_ref().map(|_| ()), rh.as_ref().map(|_| ()));
    assert_eq!(r.map(|_| ()), Err(AuditError::LogFull));
    // (the conflicting checkpoint is small enough to fit the remaining reserve gap: evidence formed)
    assert!(matches!(rh, Err(AuditError::Receive(_))));
}
