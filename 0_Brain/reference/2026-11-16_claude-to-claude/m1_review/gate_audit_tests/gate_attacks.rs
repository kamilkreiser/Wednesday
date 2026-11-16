//! QA gate M3-AUDIT (independent tier-1 read at 1d4a55b). Attack tests.
//! Each test asserts the property that SHOULD hold; a failing test is a finding.
//! Tests named `gate_ok_*` are attacks that were tried and are expected to be refused.
mod common;

use std::time::Instant;

use coagent_audit::bundle::{verify, Bundle, FieldClass, SealBody};
use coagent_audit::chain::{AuditEvent, AuthorChain};
use coagent_audit::checkpoint::{HeadBody, SignedHead};
use coagent_audit::domain::{self, nested_message, AuditDomain};
use coagent_audit::equivocation::{EquivocationEvidence, EvidenceError, Statement};
use coagent_audit::header::{HeaderBody, SignedHeader};
use coagent_audit::received::{ReceiveError, ReceivedChain};
use coagent_audit::redact::{preview, PatternRedactor, Redactor};
use coagent_audit::tiers::ShareLevel;
use coagent_audit::AuditError;
use coagent_crypto::identity::{verify_device, DeviceIdentity, SignDomain};
use coagent_proto::bytes::{PublicKey32, Signature64};
use coagent_proto::canonical;
use common::*;

// ---------------------------------------------------------------------------------------------
// 2. Domain separation
// ---------------------------------------------------------------------------------------------

/// The nested workaround's safety argument ("every audit message is longer than 32 bytes") is a
/// property of the crate's CALLERS, not of `domain::sign`, which is `pub` and takes any bytes.
/// A 10-byte message under the head label yields a signature that `verify_device` accepts as a
/// device BINDING of the author's signing key to a Noise key the attacker chose the tail of.
#[test]
fn gate_domain_no_audit_domain_signature_is_a_valid_binding() {
    let a = fixed_identity(201);
    let mut forged_bindings = Vec::new();
    for d in AuditDomain::ALL {
        let label_len = d.label().len();
        let tail_len = 32 - label_len - 1;
        let msg = vec![0x41u8; tail_len];
        let sig = domain::sign(&a, d, &msg);
        let nested = nested_message(d, &msg);
        assert_eq!(nested.len(), 32);
        let mut keys = a.public_keys();
        keys.noise_static = PublicKey32(nested.as_slice().try_into().unwrap());
        keys.binding_sig = sig;
        if let Ok(v) = verify_device(&keys) {
            forged_bindings.push(format!("{d:?} -> key id {}", v.key_id()));
        }
    }
    assert!(
        forged_bindings.is_empty(),
        "audit-domain signatures verified as device bindings: {forged_bindings:?}"
    );
}

/// Every audit object kind against every other audit label, plus both outer domains.
#[test]
fn gate_ok_domain_every_kind_refused_under_every_other_label() {
    let (w, audits) = scenario(4);
    let a = &w.ids[0];
    let dev = a.verified();
    let e = audits[0].own().event(1).unwrap().clone();
    let head = audits[0].own().checkpoints()[0].head.clone();
    let cs = audits[0].own().checkpoints()[0]
        .countersigs
        .values()
        .next()
        .unwrap()
        .clone();
    let mut aud0 = w.audit(0, every(100));
    let hs = aud0.heads_seen(a).unwrap();
    let bundle = audits[0].export(a).unwrap();
    let seal_body = SealBody {
        session_id: bundle.seal.session_id,
        exporter: bundle.seal.exporter,
        records: bundle.seal.records,
        digest: bundle.seal.digest,
    };
    // (kind, signer device, message, signature)
    let cs_dev = w
        .ids
        .iter()
        .find(|d| d.key_id() == cs.by)
        .unwrap()
        .verified();
    let objs: Vec<(AuditDomain, _, Vec<u8>, Signature64)> = vec![
        (
            AuditDomain::Header,
            dev.clone(),
            canonical::encode(&e.header.body()).unwrap(),
            e.header.sig,
        ),
        (
            AuditDomain::Head,
            dev.clone(),
            canonical::encode(&head.body()).unwrap(),
            head.sig,
        ),
        (
            AuditDomain::Countersign,
            cs_dev,
            canonical::encode(&cs.body()).unwrap(),
            cs.sig,
        ),
        (
            AuditDomain::HeadsSeen,
            dev.clone(),
            canonical::encode(&hs.body()).unwrap(),
            hs.sig,
        ),
        (
            AuditDomain::BundleSeal,
            dev.clone(),
            canonical::encode(&seal_body).unwrap(),
            bundle.seal.sig,
        ),
    ];
    for (k, d, msg, sig) in &objs {
        // positive control
        assert!(domain::verify(d, *k, msg, sig).is_ok(), "{k:?} own domain");
        for other in AuditDomain::ALL {
            if other != *k {
                assert!(
                    domain::verify(d, other, msg, sig).is_err(),
                    "{k:?} verified as {other:?}"
                );
            }
        }
        assert!(d.verify(SignDomain::Roster, msg, sig).is_err());
        assert!(d.verify(SignDomain::Binding, msg, sig).is_err());
        assert!(d
            .verify(SignDomain::Roster, &nested_message(*k, msg), sig)
            .is_err());
    }
    // A roster signature (convener = ids[0]) never verifies as any audit object.
    let r = &w.rosters[0];
    let rb = canonical::encode(&r.body).unwrap();
    assert!(dev.verify(SignDomain::Roster, &rb, &r.sig).is_ok());
    for k in AuditDomain::ALL {
        assert!(domain::verify(&dev, k, &rb, &r.sig).is_err());
    }
}

/// Ed25519 malleability: S + L must not verify, so nobody but the author can mint a second valid
/// header for the same body (which would have a different hash and frame the author).
#[test]
fn gate_ok_malleated_signature_cannot_frame_the_author() {
    let (w, audits) = scenario(1);
    let e = audits[0].own().event(1).unwrap().clone();
    let mut s = e.header.sig.0;
    const L: [u8; 32] = [
        0xed, 0xd3, 0xf5, 0x5c, 0x1a, 0x63, 0x12, 0x58, 0xd6, 0x9c, 0xf7, 0xa2, 0xde, 0xf9, 0xde,
        0x14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0x10,
    ];
    let mut carry = 0u16;
    for i in 0..32 {
        let v = s[32 + i] as u16 + L[i] as u16 + carry;
        s[32 + i] = v as u8;
        carry = v >> 8;
    }
    let mut mal = e.header.clone();
    mal.sig = Signature64(s);
    assert_ne!(mal.hash().unwrap(), e.header.hash().unwrap());
    assert!(mal.verify_sig(&w.ids[0].verified()).is_err());
    let ev = EquivocationEvidence::SameSeq {
        a: Statement::Header(e.header.clone()),
        b: Statement::Header(mal.clone()),
    };
    assert_eq!(ev.verify(&w.valid(1)), Err(EvidenceError::BadSignature));
    let mut rc = ReceivedChain::new(&w.valid(1), w.s, w.key(0)).unwrap();
    rc.accept(&e).unwrap();
    let mut me = e.clone();
    me.header = mal;
    assert_eq!(rc.accept(&me), Err(ReceiveError::BadSignature));
}

/// Cross-session framing: genuine author-signed statements from two sessions never form evidence.
#[test]
fn gate_ok_cross_session_statements_never_form_evidence() {
    let w1 = World::new(150, 3, 3);
    let mut w2 = World::new(150, 3, 3);
    w2.s = session(151);
    w2.rosters = vec![coagent_roster::sign(&w2.ids[0], {
        let mut b = w2.rosters[0].body.clone();
        b.session_id = w2.s;
        b
    })
    .unwrap()];
    let mut a1 = w1.audit(0, every(100));
    let mut a2 = w2.audit(0, every(100));
    for k in 1..=2u64 {
        a1.record(&w1.ids[0], input("action.finished", "s1", "f1"), t(k))
            .unwrap();
        a2.record(&w2.ids[0], input("action.finished", "s2", "f2"), t(k))
            .unwrap();
    }
    let h1 = a1.own().event(1).unwrap().header.clone();
    let h1b = a1.own().event(2).unwrap().header.clone();
    let x1 = a2.own().event(1).unwrap().header.clone();
    assert!(EquivocationEvidence::same_seq(&Statement::Header(h1.clone()), &Statement::Header(x1.clone())).is_none());
    assert!(EquivocationEvidence::link(&Statement::Header(x1.clone()), &h1b).is_none());
    let forged = [
        EquivocationEvidence::SameSeq {
            a: Statement::Header(h1.clone()),
            b: Statement::Header(x1.clone()),
        },
        EquivocationEvidence::Link {
            earlier: Statement::Header(x1.clone()),
            later: h1b.clone(),
        },
    ];
    for ev in forged {
        assert_eq!(ev.verify(&w1.valid(1)), Err(EvidenceError::WrongSession));
        assert_eq!(ev.verify(&w2.valid(1)), Err(EvidenceError::WrongSession));
    }
    // A head that AGREES with the header at the same number is not evidence.
    let h = a1.checkpoint_now(&w1.ids[0], t(9)).unwrap();
    let last = a1.own().event(2).unwrap().header.clone();
    assert!(EquivocationEvidence::same_seq(&Statement::Head(h), &Statement::Header(last)).is_none());
}

// ---------------------------------------------------------------------------------------------
// 3. Construction: tier confidentiality, roster changes, joiners
// ---------------------------------------------------------------------------------------------

/// 04 §3.9: a member at `nothing` receives "periodic checkpoints only"; docs/AUDIT.md §2: it
/// "cannot prove anything about any event's content or type". `audit.heads.seen` (DESIGN Q4)
/// carries the author's whole signed HEADER (type, ts, tier commitments) to every member.
/// In the builder's own scenario, B shares `nothing` with C; A holds B's chain and sends C its
/// heads-seen.
#[test]
fn gate_tier_nothing_member_never_holds_a_header_of_that_author() {
    let (w, audits) = scenario(3);
    let (b, c) = (w.key(1), 2usize);
    assert_eq!(audits[1].share_level(&w.key(c)), ShareLevel::Nothing);
    // C holds no event of B through the event path (positive control on the setup)
    assert!(audits[c].peer(&b).map_or(0, |p| p.events().count()) == 0);
    let bundle = audits[c].export(&w.ids[c]).unwrap();
    let leaked: Vec<String> = bundle
        .heads_seen
        .iter()
        .flat_map(|hs| hs.entries.iter())
        .filter_map(|s| match s {
            Statement::Header(h) if h.author == b => {
                Some(format!("seq {} type {:?} ts {}", h.author_seq, h.kind, h.ts))
            }
            _ => None,
        })
        .collect();
    assert!(
        leaked.is_empty(),
        "a nothing-level member holds headers of that author (via heads-seen): {leaked:?}"
    );
}

/// After any member removal, `heads_seen` still reports the removed author's chain, and
/// `receive_heads_seen` checks every entry against the CURRENT roster, so every honest record is
/// refused and equivocation by a CURRENT author goes undetected.
fn removal_case(remove: bool) -> Result<Vec<EquivocationEvidence>, AuditError> {
    let mut w = World::new(160, 4, 4);
    let mut a = w.audit(0, every(100));
    let mut b = w.audit(1, every(100));
    let mut c = w.audit(2, every(100));
    let mut d = w.audit(3, every(100));
    // D authors one event that B holds.
    d.set_share_level(w.key(1), ShareLevel::Summaries);
    d.record(&w.ids[3], input("action.finished", "d", "d"), t(1)).unwrap();
    for (to, e) in d.outgoing(1) {
        if to == w.key(1) {
            b.receive(&w.ids[1], &e, t(2)).unwrap();
        }
    }
    if remove {
        let r2 = w.remove(3);
        a.apply_roster(&r2).unwrap();
        b.apply_roster(&r2).unwrap();
        c.apply_roster(&r2).unwrap();
    }
    // A equivocates: C gets the real event 1, B gets a different event 1 (both signed by A).
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
    let hs = b.heads_seen(&w.ids[1]).unwrap();
    c.receive_heads_seen(&hs)
}

#[test]
fn gate_heads_seen_still_catches_equivocation_after_a_member_is_removed() {
    let control = removal_case(false).unwrap();
    assert_eq!(control.len(), 1, "positive control: evidence without removal");
    let after = removal_case(true);
    assert!(
        matches!(&after, Ok(v) if v.len() == 1),
        "after removing an unrelated member, the heads-seen exchange no longer catches A: {after:?}"
    );
}

/// A member added after a checkpoint countersigns it (honest path: `checkpoint_now` hands the
/// joiner the EXISTING head, issued at the older roster version; the joiner's `receive_head`
/// countersigns on Replay). The author's `add_countersignature` checks the CURRENT roster and
/// stores it; `verify` checks membership at the head's `roster_v` and refuses the author's own
/// honest export.
#[test]
fn gate_an_honest_authors_export_verifies_after_a_joiner_countersigns() {
    let mut w = World::new(170, 3, 2);
    let mut a = w.audit(0, every(2));
    for k in 1..=2u64 {
        a.record(&w.ids[0], input("action.finished", "s", "f"), t(k)).unwrap();
        a.checkpoint(&w.ids[0], t(k)).unwrap();
    }
    let r2 = w.add(2, 2);
    a.apply_roster(&r2).unwrap();
    let anchor = a.checkpoint_now(&w.ids[0], t(5)).unwrap();
    assert_eq!(anchor.roster_v, 1, "the joiner's anchor is the old head");
    let mut j = w.audit_from(2, 2, every(100));
    j.join_author(&anchor).unwrap();
    let cs = j.receive_head(&w.ids[2], &anchor).unwrap();
    assert_eq!(a.add_countersignature(&cs), Ok(()), "author stored it");
    let b = a.export(&w.ids[0]).unwrap();
    let r = verify(&b);
    assert!(
        r.is_ok(),
        "the honest author's own bundle no longer verifies: {:?}",
        r.err()
    );
}

/// Honest crash recovery: an author that loses its chain and re-records event 1 produces
/// transferable evidence against itself. (Expected by the construction; NOT stated in the docs.)
#[test]
fn gate_note_crash_recovery_is_indistinguishable_from_equivocation() {
    let w = World::new(180, 3, 3);
    let mut a = w.audit(0, every(100));
    let mut b = w.audit(1, every(100));
    a.set_share_level(w.key(1), ShareLevel::Full);
    a.record(&w.ids[0], input("action.finished", "x", "x"), t(1)).unwrap();
    b.receive(&w.ids[1], &a.outgoing(1)[0].1, t(2)).unwrap();
    // crash: state lost, same identity, same event re-recorded
    let mut a2 = w.audit(0, every(100));
    a2.set_share_level(w.key(1), ShareLevel::Full);
    a2.record(&w.ids[0], input("action.finished", "x", "x"), t(1)).unwrap();
    let e = a2.outgoing(1)[0].1.clone();
    let ev = match b.receive(&w.ids[1], &e, t(3)) {
        Err(AuditError::Receive(ReceiveError::Fork(ev))) => ev,
        other => panic!("expected a fork, got {other:?}"),
    };
    assert!(ev.verify(&w.valid(1)).is_ok());
}

/// The relay reorders; the watermark never makes a later honest in-order delivery fail, and a
/// non-author cannot move it.
#[test]
fn gate_ok_watermark_cannot_be_used_to_refuse_honest_delivery() {
    let w = World::new(190, 3, 3);
    let mut a = w.audit(0, every(100));
    for k in 1..=6u64 {
        a.record(&w.ids[0], input("action.finished", "s", "f"), t(k)).unwrap();
    }
    let ev = |k| a.own().disclose(k, ShareLevel::Full).unwrap();
    let mut r = ReceivedChain::new(&w.valid(1), w.s, w.key(0)).unwrap();
    assert!(matches!(r.accept(&ev(6)), Err(ReceiveError::Gap { .. })));
    assert!(matches!(r.accept(&ev(3)), Err(ReceiveError::Reorder { .. })));
    // a third member signs a far-ahead header under its own key, claiming A as author
    let mut forged = ev(6);
    forged.header.author_seq = 1_000;
    forged.header.sig = domain::sign(
        &w.ids[2],
        AuditDomain::Header,
        &canonical::encode(&forged.header.body()).unwrap(),
    );
    let before = r.max_offered();
    assert_eq!(r.accept(&forged), Err(ReceiveError::BadSignature));
    assert_eq!(r.max_offered(), before);
    for k in 1..=6 {
        r.accept(&ev(k)).unwrap();
    }
}

/// `accept` bounds sequence numbers at 2^62; `accept_head` does not. An author-signed head at
/// u64::MAX is stored and countersigned, then flows through heads-seen, export and verify.
#[test]
fn gate_heads_are_bounded_like_headers() {
    let w = World::new(200, 3, 3);
    let mut b = w.audit(1, every(100));
    let body = HeadBody {
        session_id: w.s,
        author: w.key(0),
        author_seq: u64::MAX,
        hash: coagent_proto::bytes::Digest32([7; 32]),
        roster_v: 1,
    };
    let sig = domain::sign(&w.ids[0], AuditDomain::Head, &canonical::encode(&body).unwrap());
    let head = SignedHead {
        session_id: body.session_id,
        author: body.author,
        author_seq: body.author_seq,
        hash: body.hash,
        roster_v: body.roster_v,
        sig,
    };
    let got = b.receive_head(&w.ids[1], &head);
    // whatever happens next must not panic
    let _ = b.heads_seen(&w.ids[1]);
    let bundle = b.export(&w.ids[1]).unwrap();
    let _ = verify(&bundle);
    let mut c = w.audit(2, every(100));
    let hs = b.heads_seen(&w.ids[1]).unwrap();
    let _ = c.receive_heads_seen(&hs);
    assert!(
        matches!(got, Err(AuditError::Receive(ReceiveError::BadField(_)))),
        "a head above MAX_SEQ was accepted and countersigned: {got:?}"
    );
}

/// The builder calls `verify`'s sequence-number check an EQUIVALENT mutant ("every change also
/// breaks a link or a signature"). Not against the key holder: an author/exporter can sign a
/// properly LINKED chain whose `author_seq` repeats. This test kills that mutant.
#[test]
fn gate_ok_verify_refuses_a_linked_chain_with_a_repeated_sequence_number() {
    let w = World::new(210, 3, 3);
    let mut a = w.audit(0, every(100));
    for k in 1..=2u64 {
        a.record(&w.ids[0], input("action.finished", "s", "f"), t(k)).unwrap();
    }
    let mut bundle: Bundle = a.export(&w.ids[0]).unwrap();
    assert!(verify(&bundle).is_ok());
    let e2 = bundle.own_events[1].clone();
    let body = HeaderBody {
        session_id: w.s,
        author: w.key(0),
        author_seq: 2, // repeated
        ts: e2.header.ts.clone(),
        prev_hash: e2.header.hash().unwrap(), // properly linked
        kind: e2.header.kind.clone(),
        tiers: e2.header.tiers.clone(),
    };
    let sig = domain::sign(&w.ids[0], AuditDomain::Header, &canonical::encode(&body).unwrap());
    let h3 = SignedHeader {
        session_id: body.session_id,
        author: body.author,
        author_seq: body.author_seq,
        ts: body.ts,
        prev_hash: body.prev_hash,
        kind: body.kind,
        tiers: body.tiers,
        sig,
    };
    bundle.own_events.push(AuditEvent {
        header: h3,
        summary: e2.summary.clone(),
        full: e2.full.clone(),
    });
    bundle.reseal(&w.ids[0]).unwrap();
    let e = verify(&bundle).expect_err("a linked chain with seq 1,2,2 was accepted");
    assert_eq!(e.class, FieldClass::Header);
    assert_eq!(e.what, "sequence");
}

/// Bundle parsing at every truncation point: never panics, never accepts a strict prefix.
#[test]
fn gate_ok_every_truncation_of_a_real_bundle_is_refused_without_panic() {
    let (w, audits) = scenario(1);
    let bytes = audits[1].export(&w.ids[1]).unwrap().encode().unwrap();
    assert!(Bundle::parse(&bytes).is_ok());
    for n in 0..bytes.len() {
        assert!(Bundle::parse(&bytes[..n]).is_err(), "prefix {n} parsed");
    }
    // and with garbage appended
    let mut more = bytes.clone();
    more.extend_from_slice(&[0, 0, 0, 0]);
    assert!(Bundle::parse(&more).is_err());
    eprintln!("truncation sweep over {} bytes", bytes.len());
}

/// A hostile author can make any honest receiver's bundle unverifiable: heads beyond the author's
/// chain are stored without limit, and `export` does not enforce the verifier's caps. Run with
/// `--release --ignored` (65,537 signatures).
#[test]
#[ignore]
fn gate_a_peer_cannot_push_an_honest_members_export_past_the_verifier_caps() {
    let w = World::new(220, 3, 3);
    let mut b = w.audit(1, every(1_000_000));
    let n = coagent_audit::bundle::MAX_RECORDS as u64 + 1;
    for k in 1..=n {
        let body = HeadBody {
            session_id: w.s,
            author: w.key(0),
            author_seq: k,
            hash: coagent_proto::bytes::Digest32([1; 32]),
            roster_v: 1,
        };
        let sig = domain::sign(&w.ids[0], AuditDomain::Head, &canonical::encode(&body).unwrap());
        let head = SignedHead {
            session_id: body.session_id,
            author: body.author,
            author_seq: body.author_seq,
            hash: body.hash,
            roster_v: body.roster_v,
            sig,
        };
        b.receive_head(&w.ids[1], &head).unwrap();
    }
    let bundle = b.export(&w.ids[1]).unwrap();
    let bytes = bundle.encode().unwrap();
    let parsed = Bundle::parse(&bytes);
    assert!(
        parsed.is_ok(),
        "an honest member's own export ({} bytes) is refused by the parser: {:?}",
        bytes.len(),
        parsed.err()
    );
}

// ---------------------------------------------------------------------------------------------
// Redaction
// ---------------------------------------------------------------------------------------------

#[test]
fn gate_redaction_misses() {
    let r = PatternRedactor;
    // (what, raw text, the secret that must not appear in the preview)
    let zw = "ghp_0123456789\u{200b}abcdefghijklmnop";
    let samples: Vec<(&str, String, &str)> = vec![
        ("curl -u user:pass", "curl -u admin:hunter2pw https://x".into(), "hunter2pw"),
        ("json pass", r#"{"pass": "hunter2pw"}"#.into(), "hunter2pw"),
        ("json pw", r#"{"pw": "hunter2pw"}"#.into(), "hunter2pw"),
        ("lower export db_pass", "export db_pass=hunter2pw".into(), "hunter2pw"),
        ("export single-letter", "export P=hunter2pw".into(), "hunter2pw"),
        ("passphrase yaml", "passphrase: hunter2pw".into(), "hunter2pw"),
        ("mysql -p glued", "mysql -uroot -phunter2pw db".into(), "hunter2pw"),
        ("sshpass -p", "sshpass -p hunter2pw ssh host".into(), "hunter2pw"),
        ("url pass with slash", "https://user:hunt/er2pw@host/x".into(), "er2pw"),
        ("url pass with @", "https://user:hun@ter2pw@host/x".into(), "ter2pw"),
        ("zero-width split gh token", zw.into(), "abcdefghijklmnop"),
        (
            "zero-width in name",
            "pass\u{200b}word=hunter2pw".into(),
            "hunter2pw",
        ),
        (
            "base64 key wrapped at 16 cols, no PEM header",
            "MIIEvQIBADANBgkq\nhkiG9w0BAQEFAASC\nBKcwggSjAgEAAoIB".into(),
            "hkiG9w0BAQEFAASC",
        ),
        ("short hex key", "key id 9f86d081884c7d65".into(), "9f86d081884c7d65"),
        // positive controls (expected masked)
        ("aws secret", "aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY".into(), "wJalrXUtnFEMI"),
        ("connection string", "Server=x;User Id=sa;Password=hunter2pw;".into(), "hunter2pw"),
        ("jwt", "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.abcDEF123456".into(), "eyJzdWIiOiIxMjM0NTY3ODkwIn0"),
        ("url creds", "git clone https://bob:hunter2pw@example.com/r".into(), "hunter2pw"),
        ("pem multi-line", "-----BEGIN RSA PRIVATE KEY-----\nMIIEow\nAAA\n-----END RSA PRIVATE KEY-----".into(), "MIIEow"),
        ("authorization header", "Authorization: Basic YWxhZGRpbjpvcGVuc2VzYW1l".into(), "YWxhZGRpbjpvcGVuc2VzYW1l"),
        ("slack", "xoxb-1234-5678-abcdefghijkl".into(), "abcdefghijkl"),
        ("stripe", "sk_live_abcdefghijklmnop1234".into(), "abcdefghijklmnop"),
        ("json password", r#"{"password": "hunter2pw"}"#.into(), "hunter2pw"),
        ("env export", "export DB_PASSWORD=hunter2pw".into(), "hunter2pw"),
    ];
    let mut misses = Vec::new();
    for (what, raw, secret) in &samples {
        let p = preview(&r, raw);
        let s = r.redact(raw);
        if p.contains(secret) || s.contains(secret) {
            misses.push(*what);
        }
    }
    eprintln!("REDACTION MISSES: {misses:?}");
    assert!(misses.is_empty(), "redaction misses: {misses:?}");
}

/// Redaction cost on hostile content. `line_headers` and quoted `value_range` scan to the end of
/// the line once per match; the summary is redacted BEFORE its 4096-byte limit is applied.
#[test]
#[ignore]
fn gate_redaction_time_scales_linearly() {
    let r = PatternRedactor;
    let mut out = Vec::new();
    for (name, unit) in [("cookie:", "cookie:"), ("key-quote", "a_key:\"x\" ")] {
        let mut times = Vec::new();
        for kib in [64usize, 128, 256] {
            let s = unit.repeat(kib * 1024 / unit.len());
            let t0 = Instant::now();
            let _ = r.redact(&s);
            times.push((kib, t0.elapsed().as_millis()));
        }
        out.push((name, times));
    }
    eprintln!("REDACTION TIMES (KiB, ms): {out:?}");
    for (name, times) in &out {
        let (a, b) = (times[0].1.max(1) as f64, times[2].1 as f64);
        assert!(b / a < 8.0, "{name}: 4x input took {}x time: {times:?}", b / a);
    }
}

#[allow(dead_code)]
fn _unused(_: &DeviceIdentity) {}
