//! QA gate M3-AUDIT round 2 (delta gate at 4c39916): attack tests. Test code only.
//! `r2_ok_*` pass when the attack is refused. `r2_finding_*` pass when the finding is DEMONSTRATED
//! (they assert the weakness exists and print what was learnt). `#[ignore]` ones are release-only.
mod common;

use std::time::Instant;

use coagent_audit::bundle::{verify, Bundle};
use coagent_audit::chain::AuthorChain;
use coagent_audit::checkpoint::{HeadBody, SignedHead};
use coagent_audit::domain::AuditDomain;
use coagent_audit::equivocation::{HeadsSeenBody, SignedHeadsSeen, Statement};
use coagent_audit::header::RECEIPT_KIND;
use coagent_audit::received::{ReceiveError, MAX_HEADS_PER_AUTHOR};
use coagent_audit::redact::{preview, PatternRedactor, Redactor};
use coagent_audit::session::{SessionAudit, StoreLimits};
use coagent_audit::store::{MemStore, Store};
use coagent_audit::tiers::ShareLevel;
use coagent_audit::AuditError;
use coagent_crypto::identity::{verify_device, DeviceIdentity, SignDomain};
use coagent_proto::bytes::{Digest32, KeyId, PublicKey32, Signature64};
use coagent_proto::canonical;
use common::*;

const ALL7: [SignDomain; 7] = [
    SignDomain::Binding,
    SignDomain::Roster,
    SignDomain::AuditHeader,
    SignDomain::AuditHead,
    SignDomain::AuditCountersign,
    SignDomain::AuditHeadsSeen,
    SignDomain::AuditBundleSeal,
];

fn label_of(d: SignDomain) -> &'static [u8] {
    match d {
        SignDomain::Binding => b"coagent-binding-v1",
        SignDomain::Roster => b"coagent-roster-v1",
        SignDomain::AuditHeader => b"coagent-audit-header-v1",
        SignDomain::AuditHead => b"coagent-audit-head-v1",
        SignDomain::AuditCountersign => b"coagent-audit-countersign-v1",
        SignDomain::AuditHeadsSeen => b"coagent-audit-heads-seen-v1",
        SignDomain::AuditBundleSeal => b"coagent-audit-bundle-seal-v1",
    }
}

/// Every 32-byte window of `bytes` tried as the Noise key of a forged device binding.
fn binds_somewhere(id: &DeviceIdentity, bytes: &[u8], sig: &Signature64) -> Vec<usize> {
    let mut hits = Vec::new();
    if bytes.len() < 32 {
        return hits;
    }
    for (i, w) in bytes.windows(32).enumerate() {
        let mut keys = id.public_keys();
        keys.noise_static = PublicKey32(w.try_into().unwrap());
        keys.binding_sig = *sig;
        if verify_device(&keys).is_ok() {
            hits.push(i);
        }
    }
    hits
}

// ---------------------------------------------------------------------------------------------
// A-M3 / crypto change: own version of the round-1 attack, against the domains and the public API
// ---------------------------------------------------------------------------------------------

/// Signatures made under each of the five audit domains over attacker-chosen bytes of every length
/// 0..=96 (including bytes that spell the other labels), checked: under every other domain, as a
/// device binding over every 32-byte window of the message and of `label ‖ 0 ‖ message`.
#[test]
fn r2_ok_no_audit_domain_signature_crosses_into_any_other_domain_or_a_binding() {
    let id = fixed_identity(231);
    let dev = id.verified();
    let mut bad = Vec::new();
    let mut msgs: Vec<Vec<u8>> = (0..=96usize).map(|n| vec![0x41u8; n]).collect();
    for d in ALL7 {
        // label-shaped messages: the other domain's label, its separator, and a 32-byte tail
        let mut m = label_of(d).to_vec();
        msgs.push(m.clone());
        m.push(0);
        msgs.push(m.clone());
        m.extend_from_slice(&[0x42; 32]);
        msgs.push(m);
    }
    for a in ALL7 {
        for msg in &msgs {
            let sig = id.sign(a, msg);
            assert!(dev.verify(a, msg, &sig).is_ok());
            for b in ALL7 {
                if a != b && dev.verify(b, msg, &sig).is_ok() {
                    bad.push(format!("{a:?} as {b:?} len {}", msg.len()));
                }
            }
            if a != SignDomain::Binding {
                let mut full = label_of(a).to_vec();
                full.push(0);
                full.extend_from_slice(msg);
                for hit in binds_somewhere(&id, msg, &sig)
                    .into_iter()
                    .chain(binds_somewhere(&id, &full, &sig))
                {
                    bad.push(format!("{a:?} len {} binds at window {hit}", msg.len()));
                }
            }
        }
    }
    // Each label followed by the separator is prefix-free against every other.
    for a in ALL7 {
        for b in ALL7 {
            if a != b {
                let mut la = label_of(a).to_vec();
                la.push(0);
                let mut lb = label_of(b).to_vec();
                lb.push(0);
                assert!(!lb.starts_with(&la), "{a:?} ‖ 0 prefixes {b:?} ‖ 0");
            }
        }
    }
    assert!(bad.is_empty(), "cross-domain acceptance: {bad:?}");
}

/// The public surface that still signs: `record` (header), `checkpoint_now` (head), `receive_head`
/// (countersigns an ATTACKER-CHOSEN head, with an attacker-chosen 32-byte hash field), heads-seen,
/// and `Bundle::reseal` over attacker-chosen contents. No result verifies under any other domain or
/// as a binding over any 32-byte window of its signed body.
#[test]
fn r2_ok_signatures_from_the_public_api_stay_in_their_domain() {
    let w = World::new(232, 3, 3);
    let mut a = w.audit(0, every(100));
    let mut b = w.audit(1, every(100));
    a.record(&w.ids[0], input("action.finished", "s", "f"), t(1))
        .unwrap();
    let head = a.checkpoint_now(&w.ids[0], t(2)).unwrap();
    // attacker A crafts a head whose hash field is a 32-byte value of its choice (a Noise key)
    let chosen = [0x5au8; 32];
    let body = HeadBody {
        session_id: w.s,
        author: w.key(0),
        author_seq: 1,
        hash: Digest32(chosen),
        roster_v: 1,
    };
    let crafted = SignedHead {
        session_id: body.session_id,
        author: body.author,
        author_seq: body.author_seq,
        hash: body.hash,
        roster_v: body.roster_v,
        sig: audit_sign(&w.ids[0], AuditDomain::Head, &canonical::encode(&body).unwrap()),
    };
    let cs = b.receive_head(&w.ids[1], &crafted).unwrap(); // B countersigns attacker bytes
    let hs = b.heads_seen(&w.ids[1]).unwrap();
    let mut bundle = a.export(&w.ids[0]).unwrap();
    bundle.reseal(&w.ids[0]).unwrap();
    let e = a.own().event(1).unwrap().clone();
    let seal_body = coagent_audit::bundle::SealBody {
        session_id: bundle.seal.session_id,
        exporter: bundle.seal.exporter,
        records: bundle.seal.records,
        digest: bundle.seal.digest,
    };
    let objs: Vec<(SignDomain, &DeviceIdentity, Vec<u8>, Signature64)> = vec![
        (SignDomain::AuditHeader, &w.ids[0], canonical::encode(&e.header.body()).unwrap(), e.header.sig),
        (SignDomain::AuditHead, &w.ids[0], canonical::encode(&head.body()).unwrap(), head.sig),
        (SignDomain::AuditCountersign, &w.ids[1], canonical::encode(&cs.body()).unwrap(), cs.sig),
        (SignDomain::AuditHeadsSeen, &w.ids[1], canonical::encode(&hs.body()).unwrap(), hs.sig),
        (SignDomain::AuditBundleSeal, &w.ids[0], canonical::encode(&seal_body).unwrap(), bundle.seal.sig),
    ];
    let mut bad = Vec::new();
    for (d, id, msg, sig) in &objs {
        let dev = id.verified();
        assert!(dev.verify(*d, msg, sig).is_ok(), "{d:?} positive control");
        for o in ALL7 {
            if o != *d && dev.verify(o, msg, sig).is_ok() {
                bad.push(format!("{d:?} verified as {o:?}"));
            }
        }
        let hits = binds_somewhere(id, msg, sig);
        if !hits.is_empty() {
            bad.push(format!("{d:?} binds at {hits:?}"));
        }
        // and the bare chosen value
        let mut keys = id.public_keys();
        keys.noise_static = PublicKey32(chosen);
        keys.binding_sig = *sig;
        if verify_device(&keys).is_ok() {
            bad.push(format!("{d:?} binds the chosen key"));
        }
    }
    assert!(bad.is_empty(), "{bad:?}");
}

// ---------------------------------------------------------------------------------------------
// A-B1
// ---------------------------------------------------------------------------------------------

/// X (0) shares `full` with B (1); C (2) is at `nothing` for X; X sends B `n` events.
fn xbc(base: u8, n: u64) -> (World, Vec<SessionAudit<MemStore>>) {
    let w = World::new(base, 4, 4);
    let mut au: Vec<SessionAudit<MemStore>> = (0..4).map(|i| w.audit(i, every(1000))).collect();
    au[0].set_share_level(w.key(1), ShareLevel::Full);
    for k in 1..=n {
        au[0]
            .record(&w.ids[0], input("request.new", &format!("x{k}"), "secret-x"), t(k * 100))
            .unwrap();
        for (to, e) in au[0].outgoing(k) {
            assert_eq!(to, w.key(1));
            au[1].receive(&w.ids[1], &e, t(k * 100 + 1)).unwrap();
        }
    }
    let h = au[0].checkpoint_now(&w.ids[0], t(n * 100 + 50)).unwrap();
    for j in 1..4 {
        let cs = au[j].receive_head(&w.ids[j], &h).unwrap();
        au[0].add_countersignature(&cs).unwrap();
    }
    (w, au)
}

fn headers_of(hs: &SignedHeadsSeen, author: &KeyId) -> usize {
    hs.entries
        .iter()
        .filter(|s| matches!(s, Statement::Header(h) if &h.author == author))
        .count()
}

#[test]
fn r2_ok_unknown_or_lowered_level_sends_checkpoints_only() {
    let (w, mut au) = xbc(233, 3);
    // X records one more event after its checkpoint, so B's latest statement is a header
    au[0]
        .record(&w.ids[0], input("request.new", "x4", "secret"), t(900))
        .unwrap();
    let e = au[0].outgoing(4)[0].1.clone();
    au[1].receive(&w.ids[1], &e, t(901)).unwrap();
    // unknown: default nothing
    assert_eq!(au[1].known_level(&w.key(0), &w.key(2)), ShareLevel::Nothing);
    let hs = au[1].heads_seen_for(&w.ids[1], &w.key(2)).unwrap();
    assert_eq!(headers_of(&hs, &w.key(0)), 0, "unknown level leaked a header");
    // positive control: noted summaries -> header
    au[1].note_share_level(w.key(0), w.key(2), ShareLevel::Summaries);
    let hs = au[1].heads_seen_for(&w.ids[1], &w.key(2)).unwrap();
    assert_eq!(headers_of(&hs, &w.key(0)), 1);
    // lowered: back to checkpoints only
    au[1].note_share_level(w.key(0), w.key(2), ShareLevel::Nothing);
    let hs = au[1].heads_seen_for(&w.ids[1], &w.key(2)).unwrap();
    assert_eq!(headers_of(&hs, &w.key(0)), 0, "lowered level still leaks");
    // broadcast: never
    let hs = au[1].heads_seen(&w.ids[1]).unwrap();
    assert_eq!(headers_of(&hs, &w.key(0)), 0);
}

/// FINDING (A-B1 residue 1): `note_share_level` takes a bare (author, member, level) triple from the
/// caller. Nothing authenticates it as X's own statement, binds it to a roster version, or checks
/// it against X's signed `member.accepted` event. If the caller feeds it from anything but X's own
/// signed report, C (at `nothing` for X) receives X's header from honest B, and C's
/// `receive_heads_seen` accepts and stores it (so it is in C's export too).
#[test]
fn r2_finding_share_level_input_is_unauthenticated() {
    let (w, mut au) = xbc(234, 3);
    au[0]
        .record(&w.ids[0], input("request.new", "x4", "secret"), t(900))
        .unwrap();
    let e = au[0].outgoing(4)[0].1.clone();
    au[1].receive(&w.ids[1], &e, t(901)).unwrap();
    assert_eq!(au[0].share_level(&w.key(2)), ShareLevel::Nothing, "X really shares nothing with C");
    // anybody's claim, e.g. C's own "X shares full with me", reaches the API unchanged
    au[1].note_share_level(w.key(0), w.key(2), ShareLevel::Full);
    let hs = au[1].heads_seen_for(&w.ids[1], &w.key(2)).unwrap();
    assert_eq!(headers_of(&hs, &w.key(0)), 1);
    let ev = au[2].receive_heads_seen(&hs).unwrap();
    assert!(ev.is_empty());
    let leaked: Vec<String> = au[2]
        .export(&w.ids[2])
        .unwrap()
        .heads_seen
        .iter()
        .flat_map(|h| h.entries.iter())
        .filter_map(|s| match s {
            Statement::Header(h) if h.author == w.key(0) => {
                Some(format!("seq {} type {} ts {}", h.author_seq, h.kind, h.ts))
            }
            _ => None,
        })
        .collect();
    eprintln!("C (nothing for X) now holds, accepted and exportable: {leaked:?}");
    assert_eq!(leaked.len(), 1);
}

/// A member removed and re-added: the levels learnt about it survive (keyed by key id only).
#[test]
fn r2_finding_known_level_survives_removal_and_readd() {
    let mut w = World::new(235, 4, 4);
    let mut b = w.audit(1, every(100));
    b.note_share_level(w.key(0), w.key(2), ShareLevel::Full);
    let r2 = w.remove(2);
    b.apply_roster(&r2).unwrap();
    let r3 = w.add(2, 2);
    let readd = b.apply_roster(&r3);
    eprintln!("re-add of the same key applied: {readd:?}");
    if readd.is_ok() {
        assert_eq!(b.known_level(&w.key(0), &w.key(2)), ShareLevel::Full);
        eprintln!("B still believes X shares FULL with re-added C (no reset on removal)");
    }
}

/// An addressed record forwarded to a third member is refused there and not stored.
#[test]
fn r2_ok_forwarded_addressed_record_is_refused_and_not_stored() {
    let (w, mut au) = xbc(236, 2);
    au[1].note_share_level(w.key(0), w.key(2), ShareLevel::Full);
    let hs = au[1].heads_seen_for(&w.ids[1], &w.key(2)).unwrap();
    let before = au[3].store().records(&w.s).unwrap().len();
    assert!(matches!(au[3].receive_heads_seen(&hs), Err(AuditError::NotAddressedToMe)));
    assert_eq!(au[3].store().records(&w.s).unwrap().len(), before);
    // re-addressing breaks B's signature
    let mut fwd = hs.clone();
    fwd.to = Some(w.key(3));
    assert!(au[3].receive_heads_seen(&fwd).is_err());
}

/// FINDING (A-B1 residue 2, quantified): C is at `nothing` for X and at `full` for B. B receives
/// X's events. C receives B's receipt events: header (type `audit.receipt`, B's receive time) and,
/// at full, the full tier; the summary naming X is withheld. In a session where C knows its own
/// events, C learns the exact COUNT and per-event TIME of X's events disclosed to B.
#[test]
fn r2_finding_receipt_headers_give_a_nothing_member_count_and_time_of_each_event() {
    let w = World::new(237, 3, 3);
    let mut x = w.audit(0, every(1000));
    let mut b = w.audit(1, every(1000));
    let mut c = w.audit(2, every(1000));
    x.set_share_level(w.key(1), ShareLevel::Full);
    b.set_share_level(w.key(2), ShareLevel::Full);
    let times = [100u64, 250, 400, 700, 1300];
    for (k, ms) in times.iter().enumerate() {
        let seq = k as u64 + 1;
        x.record(&w.ids[0], input("action.finished", "x", "secret-x"), t(*ms))
            .unwrap();
        for (_, e) in x.outgoing(seq) {
            b.receive(&w.ids[1], &e, t(ms + 1)).unwrap();
        }
    }
    let mut seen = Vec::new();
    for s in 1..=b.own().seq() {
        for (to, e) in b.outgoing(s) {
            if to == w.key(2) {
                assert!(e.summary.is_none(), "summary naming X reached C");
                if e.header.kind == RECEIPT_KIND {
                    seen.push(e.header.ts.clone());
                }
                c.receive(&w.ids[2], &e, t(5000)).unwrap();
            }
        }
    }
    eprintln!(
        "C (nothing for X) learns {} receipts at {:?}; X's events were at {:?} (+1 ms)",
        seen.len(),
        seen,
        times
    );
    assert_eq!(seen.len(), times.len());
}

// ---------------------------------------------------------------------------------------------
// A-M1
// ---------------------------------------------------------------------------------------------

fn hs_signed(id: &DeviceIdentity, w: &World, to: Option<KeyId>, rv: u64, entries: Vec<Statement>) -> SignedHeadsSeen {
    let body = HeadsSeenBody { session_id: w.s, from: id.key_id(), to, roster_v: rv, entries };
    let sig = audit_sign(id, AuditDomain::HeadsSeen, &canonical::encode(&body).unwrap());
    SignedHeadsSeen { session_id: body.session_id, from: body.from, to: body.to, roster_v: body.roster_v, entries: body.entries, sig }
}

#[test]
fn r2_ok_future_version_is_refused_without_storing_and_does_not_stall_others() {
    let (w, mut au) = xbc(238, 2);
    let before = au[2].store_usage();
    let bad = hs_signed(&w.ids[3], &w, None, 99, vec![]);
    assert!(matches!(au[2].receive_heads_seen(&bad), Err(AuditError::RosterBehind(99))));
    assert_eq!(au[2].store_usage(), before);
    let ok = au[1].heads_seen(&w.ids[1]).unwrap();
    assert!(au[2].receive_heads_seen(&ok).is_ok());
}

#[test]
fn r2_ok_joiner_cannot_report_under_a_version_before_it_joined() {
    let mut w = World::new(239, 5, 4);
    let r2 = w.add(4, 4);
    let mut c = w.audit(2, every(100));
    c.apply_roster(&r2).unwrap();
    let pre = hs_signed(&w.ids[4], &w, None, 1, vec![]);
    let r = c.receive_heads_seen(&pre);
    assert!(matches!(r, Err(AuditError::Evidence(_))), "{r:?}");
    let post = hs_signed(&w.ids[4], &w, None, 2, vec![]);
    assert!(c.receive_heads_seen(&post).is_ok());
}

/// Re-add under a NEW key (a new device): old key's records at old versions still verify; the new
/// key cannot report under a version before it was added; the old key cannot report after.
#[test]
fn r2_ok_readd_under_a_new_key() {
    let mut w = World::new(240, 6, 4);
    let r2 = w.remove(3);
    let r3 = w.add(5, 5);
    let _ = (&r2, &r3);
    let mut c = w.audit(2, every(100));
    assert_eq!(c.history().range(), (1, 3));
    assert!(c.receive_heads_seen(&hs_signed(&w.ids[3], &w, None, 1, vec![])).is_ok());
    assert!(c.receive_heads_seen(&hs_signed(&w.ids[5], &w, None, 3, vec![])).is_ok());
    assert!(c.receive_heads_seen(&hs_signed(&w.ids[5], &w, None, 1, vec![])).is_err());
    assert!(c.receive_heads_seen(&hs_signed(&w.ids[3], &w, None, 3, vec![])).is_err());
}

// ---------------------------------------------------------------------------------------------
// A-M4: denial of audit through the heads-seen path
// ---------------------------------------------------------------------------------------------

/// FINDING: `receive_heads_seen` persists EVERY accepted record. There is no deduplication, no
/// per-reporter quota and no rate limit, so replaying ONE honest record (or a removed member's
/// records at its old version, or a member signing new empty records) grows an honest member's
/// store until `LogFull`, after which that member can no longer record its OWN events.
/// Debug run with a lowered limit; the release run below uses the default limits.
#[test]
fn r2_finding_replayed_heads_seen_fills_the_store_and_stops_own_logging() {
    let (w, mut au) = xbc(241, 2);
    // one honest record of member 3 with no entries (the smallest), replayed by anyone
    let hs = au[3].heads_seen(&w.ids[3]).unwrap();
    let hs = if hs.entries.is_empty() { hs } else { hs_signed(&w.ids[3], &w, None, 1, vec![]) };
    let (b0, r0) = au[2].store_usage();
    au[2].set_limits(StoreLimits { bytes: b0 + 2_000_000, records: 1_000_000 });
    let mut n = 0u64;
    loop {
        match au[2].receive_heads_seen(&hs) {
            Ok(_) => n += 1,
            Err(AuditError::LogFull) => break,
            Err(e) => panic!("{e:?}"),
        }
    }
    let (b1, r1) = au[2].store_usage();
    let own = au[2].record(&w.ids[2], input("action.finished", "own", "own"), t(9_000));
    eprintln!(
        "{n} replays of one {}-byte record stored {} records / {} bytes; then own record: {:?}",
        canonical::encode(&hs).unwrap().len(),
        r1 - r0,
        b1 - b0,
        own
    );
    assert!(n > 100);
    assert!(matches!(own, Err(AuditError::LogFull)));
}

/// Release: default limits, a removed member's own empty records at its old version.
#[test]
#[ignore]
fn r2_finding_release_removed_member_fills_default_store() {
    let mut w = World::new(242, 4, 4);
    let mut c = w.audit(2, every(100));
    let r2 = w.remove(3);
    c.apply_roster(&r2).unwrap();
    let start = Instant::now();
    let mut n = 0u64;
    loop {
        // D (removed at v2) signs a fresh empty record each time, at v1
        let hs = hs_signed(&w.ids[3], &w, None, 1, vec![]);
        match c.receive_heads_seen(&hs) {
            Ok(_) => n += 1,
            Err(AuditError::LogFull) => break,
            Err(e) => panic!("{e:?}"),
        }
        if n > 2_000_000 {
            break;
        }
    }
    let own = c.record(&w.ids[2], input("action.finished", "own", "own"), t(9_000));
    eprintln!(
        "removed member: {n} identical-size records (no entries) in {:?}; store {:?}; own record: {own:?}",
        start.elapsed(),
        c.store_usage()
    );
    assert!(matches!(own, Err(AuditError::LogFull)));
}

/// A long honest session: once an author has issued MAX_HEADS_PER_AUTHOR checkpoints, receivers
/// refuse every later one, so none of its later events is ever countersigned again.
#[test]
fn r2_finding_checkpointing_ends_after_the_per_author_cap() {
    let w = World::new(243, 3, 3);
    let mut x = w.audit(0, every(1));
    let mut b = w.audit(1, every(1_000_000));
    let mut refused_at = None;
    for k in 1..=(MAX_HEADS_PER_AUTHOR as u64 + 3) {
        x.record(&w.ids[0], coagent_audit::chain::EventInput { kind: "action.finished", summary: None, full: None }, t(k))
            .unwrap();
        if let Some(h) = x.checkpoint(&w.ids[0], t(k)).unwrap() {
            match b.receive_head(&w.ids[1], &h) {
                Ok(cs) => x.add_countersignature(&cs).unwrap(),
                Err(AuditError::Receive(ReceiveError::TooManyHeads)) => {
                    refused_at.get_or_insert(k);
                }
                Err(e) => panic!("{e:?}"),
            }
        }
    }
    let last_attested = x.own().attestations().keys().next_back().copied();
    eprintln!("checkpoint refused from seq {refused_at:?}; last attested {last_attested:?}; chain at {}", x.own().seq());
    assert_eq!(refused_at, Some(MAX_HEADS_PER_AUTHOR as u64 + 1));
}

/// Release: build the largest bundle the store allows (B receives full-tier events from A until
/// LogFull), export, encode, parse and verify; time each.
#[test]
#[ignore]
fn r2_measure_release_verify_on_a_maximum_size_bundle() {
    let w = World::new(244, 3, 3);
    let mut a = w.audit(0, every(50));
    let mut b = w.audit(1, every(1_000_000));
    a.set_share_level(w.key(1), ShareLevel::Full);
    let summary = "s".repeat(4000);
    let start = Instant::now();
    let mut n = 0u64;
    'outer: loop {
        n += 1;
        if a.record(&w.ids[0], input("action.finished", &summary, &"f".repeat(200)), t(n)).is_err() {
            break;
        }
        for (_, e) in a.outgoing(n) {
            match b.receive(&w.ids[1], &e, t(n)) {
                Ok(_) => {}
                Err(AuditError::LogFull) => break 'outer,
                Err(e) => panic!("{e:?}"),
            }
        }
        if let Some(h) = a.checkpoint(&w.ids[0], t(n)).unwrap() {
            match b.receive_head(&w.ids[1], &h) {
                Ok(cs) => a.add_countersignature(&cs).unwrap(),
                Err(AuditError::LogFull) => break 'outer,
                Err(e) => panic!("{e:?}"),
            }
        }
    }
    let build = start.elapsed();
    let t0 = Instant::now();
    let bundle = b.export(&w.ids[1]).unwrap();
    let t_export = t0.elapsed();
    let bytes = bundle.encode().unwrap();
    let t1 = Instant::now();
    let parsed = Bundle::parse(&bytes).unwrap();
    let t_parse = t1.elapsed();
    let t2 = Instant::now();
    let rep = verify(&parsed);
    let t_verify = t2.elapsed();
    eprintln!(
        "events {n}; store {:?}; bundle {} bytes; build {build:?}; export {t_export:?}; parse {t_parse:?}; verify {t_verify:?}; ok={}",
        b.store_usage(),
        bytes.len(),
        rep.is_ok()
    );
    assert!(rep.is_ok(), "{:?}", rep.err());
}

// ---------------------------------------------------------------------------------------------
// A-M2 edges
// ---------------------------------------------------------------------------------------------

#[test]
fn r2_ok_countersigner_rule_edges_and_export_verifies() {
    // several checkpoints at one roster version before a join; removal and re-add of the same key
    let mut w = World::new(245, 5, 3);
    let mut a = w.audit(0, every(1));
    for k in 1..=3u64 {
        a.record(&w.ids[0], input("action.finished", "s", "f"), t(k)).unwrap();
        a.checkpoint(&w.ids[0], t(k)).unwrap();
    }
    let r2 = w.add(3, 3);
    a.apply_roster(&r2).unwrap();
    let mut j = w.audit_from(3, 2, every(100));
    let heads: Vec<SignedHead> = a.own().checkpoints().iter().map(|c| c.head.clone()).collect();
    assert_eq!(heads.len(), 3);
    // earlier same-version heads: refused; the latest (the anchor): accepted
    for h in &heads[..2] {
        let cs = h.countersign(&w.ids[3]).unwrap();
        assert!(matches!(a.add_countersignature(&cs), Err(AuditError::NotMember(_))), "pre-anchor accepted");
    }
    j.join_author(&heads[2]).unwrap();
    let anchor_cs = j.receive_head(&w.ids[3], &heads[2]).unwrap();
    // out of order: the author moves on at v2 before the anchor countersignature arrives
    a.record(&w.ids[0], input("action.finished", "s", "f"), t(10)).unwrap();
    let h4 = a.checkpoint(&w.ids[0], t(10)).unwrap().unwrap();
    assert_eq!(h4.roster_v, 2);
    a.add_countersignature(&anchor_cs).unwrap();
    // removal of member 1 then re-add (same key) if the roster allows it
    let r3 = w.remove(1);
    a.apply_roster(&r3).unwrap();
    a.record(&w.ids[0], input("action.finished", "s", "f"), t(11)).unwrap();
    let h5 = a.checkpoint(&w.ids[0], t(11)).unwrap().unwrap();
    a.record(&w.ids[0], input("action.finished", "s", "f"), t(12)).unwrap();
    let h6 = a.checkpoint(&w.ids[0], t(12)).unwrap().unwrap();
    let r4 = w.add(1, 1);
    let readd = a.apply_roster(&r4);
    eprintln!("re-add same key: {readd:?}");
    if readd.is_ok() {
        // h5 (while removed, not the latest before re-add) refused; h6 (latest before v4) accepted;
        // a head at v1 (rule 1) accepted
        let r5 = a.add_countersignature(&h5.countersign(&w.ids[1]).unwrap());
        let r6 = a.add_countersignature(&h6.countersign(&w.ids[1]).unwrap());
        let r1 = a.add_countersignature(&heads[0].countersign(&w.ids[1]).unwrap());
        eprintln!("re-added: h5 {r5:?} h6 {r6:?} v1-head {r1:?}");
        assert!(r5.is_err() && r6.is_ok() && r1.is_ok());
    }
    let b = a.export(&w.ids[0]).unwrap();
    let r = verify(&b);
    assert!(r.is_ok(), "{:?}", r.err());
    let _ = h4;
}

// ---------------------------------------------------------------------------------------------
// Redaction (A-m2, A-m3)
// ---------------------------------------------------------------------------------------------

#[test]
fn r2_report_redaction_over_masking_of_ordinary_text() {
    let r = PatternRedactor;
    let ordinary: Vec<(&str, &str)> = vec![
        ("git sha", "commit 3f2a9c1e8b7d6a5f4e3d2c1b0a9f8e7d6c5b4a39 fixed the parser"),
        ("sha256 checksum", "sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  release.tar.gz"),
        ("uuid", "request 123e4567-e89b-12d3-a456-426614174000 done"),
        ("sort -u", "sort -u names.txt > out.txt"),
        ("ps -u", "ps -u root"),
        ("mysql prompt", "mysql -h db -u app -p appdb"),
        ("email", "mail bob@example.com: thanks"),
        ("scp", "scp build.tar user@host:/tmp/x"),
        ("compass", "compass: north"),
        ("bypass", "bypass: true"),
        ("passenger", "passenger_count=4"),
        ("password policy", "password_min_length=12"),
        ("camel list", "SessionAuditTest\nReceivedChainTest\nRosterHistoryTest"),
        ("test names", "test_parse_header\ntest_parse_footer\ntest_parse_bodies"),
        ("persian zwnj", "می\u{200c}خواهم"),
        ("emoji zwj", "family \u{1F468}\u{200D}\u{1F469}\u{200D}\u{1F467}"),
        ("hebrew rlm", "שלום\u{200F} world"),
        ("url with @path", "https://example.com/users/@alice:profile"),
        ("cargo -p", "cargo test -p coagent-audit"),
    ];
    for (what, text) in ordinary {
        let p = preview(&r, text);
        let changed = p != text;
        eprintln!("{} {what}: {text:?} -> {p:?}", if changed { "CHANGED" } else { "kept   " });
    }
}

#[test]
fn r2_report_redaction_misses_new_shapes() {
    let r = PatternRedactor;
    let s = "hunter2pw";
    let cases: Vec<(&str, String)> = vec![
        ("PGPASSWORD env prefix", format!("PGPASSWORD={s} psql -h db")),
        ("--password space", format!("tool --password {s} --host x")),
        ("docker login -p", format!("docker login -u bob -p {s} reg.io")),
        ("X-Api-Key header", format!("curl -H 'X-Api-Key: {s}' https://x")),
        ("access_token query", format!("GET https://x/cb?access_token={s}&a=1")),
        ("netrc", format!("machine host login bob password {s}")),
        ("json secret", format!(r#"{{"secret": "{s}"}}"#)),
        ("yaml api_key quoted", format!("api_key: '{s}'")),
        ("homoglyph name (cyrillic a)", format!("p\u{0430}ssword={s}")),
        ("tag chars inside name", format!("pass\u{E0020}word={s}")),
        ("bidi isolate inside name", format!("pass\u{2066}word={s}")),
        ("variation selector inside name", format!("pass\u{FE0F}word={s}")),
        ("combining grapheme joiner", format!("pass\u{034F}word={s}")),
        ("hangul filler split token", "ghp_0123456789\u{3164}abcdefghijklmnop".to_string()),
        ("short hex 12", "key 9f86d081884c".to_string()),
        ("Authorization lower", format!("authorization: {s}")),
        ("set password sql", format!("ALTER USER bob WITH PASSWORD '{s}';")),
        ("htpasswd -b", format!("htpasswd -b .htpasswd bob {s}")),
    ];
    let mut misses = Vec::new();
    for (what, text) in &cases {
        let p = preview(&r, text);
        let needle = if what.starts_with("hangul") { "abcdefghijklmnop" } else if what.starts_with("short hex") { "9f86d081884c" } else { s };
        let miss = p.contains(needle);
        eprintln!("{} {what}: {p:?}", if miss { "MISS  " } else { "masked" });
        if miss {
            misses.push(*what);
        }
    }
    eprintln!("misses: {} of {}: {misses:?}", misses.len(), cases.len());
}

/// Release: per-call time of the redactor on hostile shapes at 16, 32 and 64 KiB (the summary path
/// is capped at 16 KiB before redaction; the full-tier preview at the 64 KiB window).
#[test]
#[ignore]
fn r2_measure_release_redaction_time_on_hostile_shapes() {
    let r = PatternRedactor;
    let shapes: Vec<(&str, &str)> = vec![
        ("url userinfo", "http://a:b@"),
        ("many @ after userinfo", "@"),
        ("mysql -p", "mysql -p x "),
        ("export assign", "export A=x "),
        ("-u user:pass", "-u a:b "),
        ("hex broken", "0123456789abcde "),
        ("b64 short lines", "ABCDEFGHIJKLMN\n"),
        ("zero-width", "a\u{200b}"),
        ("pass= ", "pass=x "),
        ("cookie:", "cookie: x"),
        ("a_key:", "a_key:\"x\" "),
    ];
    let mut worst = 0f64;
    for (what, unit) in shapes {
        let mut row = Vec::new();
        for kib in [16usize, 32, 64] {
            let mut text = if what == "many @ after userinfo" { "https://u:".to_string() } else { String::new() };
            while text.len() < kib * 1024 {
                text.push_str(unit);
            }
            let mut end = kib * 1024;
            while !text.is_char_boundary(end) {
                end -= 1;
            }
            text.truncate(end);
            let t0 = Instant::now();
            let out = r.redact(&text);
            let ms = t0.elapsed().as_secs_f64() * 1000.0;
            std::hint::black_box(out);
            row.push(ms);
        }
        let ratio = row[2] / row[0].max(0.001);
        worst = worst.max(ratio);
        eprintln!("{what:24} 16K {:8.2} ms  32K {:8.2} ms  64K {:8.2} ms  64/16 = {ratio:.1}", row[0], row[1], row[2]);
    }
    eprintln!("worst 64K/16K ratio {worst:.1} (linear = 4)");
}

#[allow(dead_code)]
fn _unused(_: AuthorChain, _: Box<dyn Redactor>) {}

/// The edited gate removal case no longer carries ANY entry about the removed member (D has no
/// checkpoint and nobody knows D's levels, so `heads_seen_for` omits D). Round 1's failure was
/// exactly such an entry. Here D has a checkpoint B holds, D is removed, and B's records (made
/// before and after the removal) carry D's entry; C must still verify them and catch A.
fn removal_with_entry(record_before_removal: bool) -> Result<Vec<coagent_audit::equivocation::EquivocationEvidence>, AuditError> {
    let mut w = World::new(246, 4, 4);
    let mut a = w.audit(0, every(100));
    let mut b = w.audit(1, every(100));
    let mut c = w.audit(2, every(100));
    let mut d = w.audit(3, every(100));
    d.set_share_level(w.key(1), ShareLevel::Summaries);
    d.record(&w.ids[3], input("action.finished", "d", "d"), t(1)).unwrap();
    for (to, e) in d.outgoing(1) {
        if to == w.key(1) {
            b.receive(&w.ids[1], &e, t(2)).unwrap();
        }
    }
    let dh = d.checkpoint_now(&w.ids[3], t(3)).unwrap();
    b.receive_head(&w.ids[1], &dh).unwrap();
    c.receive_head(&w.ids[2], &dh).unwrap();
    a.set_share_level(w.key(2), ShareLevel::Full);
    a.record(&w.ids[0], input("action.finished", "real", "real"), t(3)).unwrap();
    for (to, e) in a.outgoing(1) {
        if to == w.key(2) {
            c.receive(&w.ids[2], &e, t(4)).unwrap();
        }
    }
    let mut fork = AuthorChain::new(&w.ids[0], w.s, every(100), Box::new(PatternRedactor), t(0));
    fork.append(&w.ids[0], input("action.finished", "lie", "lie"), t(3)).unwrap();
    b.receive(&w.ids[1], &fork.disclose(1, ShareLevel::Full).unwrap(), t(4)).unwrap();
    b.note_share_level(w.key(0), w.key(2), ShareLevel::Full);
    let early = b.heads_seen_for(&w.ids[1], &w.key(2)).unwrap();
    let r2 = w.remove(3);
    a.apply_roster(&r2).unwrap();
    b.apply_roster(&r2).unwrap();
    c.apply_roster(&r2).unwrap();
    let hs = if record_before_removal { early } else { b.heads_seen_for(&w.ids[1], &w.key(2)).unwrap() };
    assert!(hs.entries.iter().any(|s| s.author() == w.key(3)), "entry about removed D present");
    c.receive_heads_seen(&hs)
}

#[test]
fn r2_ok_removal_case_with_an_entry_about_the_removed_member() {
    for before in [true, false] {
        let r = removal_with_entry(before);
        assert!(matches!(&r, Ok(v) if v.len() == 1), "before={before}: {r:?}");
    }
}
