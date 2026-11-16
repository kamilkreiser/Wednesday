//! QA gate (M1 CORE) adversarial tests. `gate_fail_*` assert a property the code does NOT have
//! (they fail at 3f60cf4 and are the finding's evidence); `gate_demo_*` pass and document a
//! behaviour the verdict discusses; `gate_ok_*` are attacks that were refused.
mod common;

use std::time::Instant;

use coagent_crypto::channel_map::{ChannelMap, MapEvent};
use coagent_crypto::sas::VerifyStatus;
use coagent_crypto::CryptoError;
use coagent_proto::bytes::Digest32;
use coagent_proto::canonical;
use coagent_proto::envelope::{decode_for_channel, Binding, Envelope};
use coagent_proto::record::{RecordKind, SasMsg, SasStep};
use common::*;

fn sas(step: SasStep, v: [u8; 32]) -> Vec<u8> {
    canonical::encode(&SasMsg {
        step,
        value: Digest32(v),
    })
    .unwrap()
}

/// G-SAS-1: the peer alone (no local "Verify" press) runs ceremonies on this side, shows words to
/// the local human, and burns all three local attempts -> pair Locked without the human acting.
#[test]
fn gate_fail_peer_cannot_consume_local_attempts_without_local_verify() {
    let mut v = ids(2);
    v.sort_by_key(|d| d.key_id());
    let s = session(3);
    let r = roster(s, [8; 32], &[&v[0], &v[1]]);
    let (mut raw0, c1) = kk_pair(&r, &[&v[0], &v[1]], 0, 1); // raw0: hostile committer
    let mut m1 = ChannelMap::new();
    m1.insert(c1).unwrap();
    let k0 = v[0].key_id();
    let mut words_shown_unprompted = false;
    for _ in 0..3 {
        let commit = raw0
            .seal_record(RecordKind::Sas, &sas(SasStep::Commit, [3; 32]))
            .unwrap();
        let ev = m1.open(&s, &k0, &commit).unwrap();
        assert!(matches!(ev, MapEvent::Verify { send: Some(_), .. }));
        // Peer aborts the ceremony with a step that is invalid for its role.
        let junk = raw0
            .seal_record(RecordKind::Sas, &sas(SasStep::Request, [0; 32]))
            .unwrap();
        let _ = m1.open(&s, &k0, &junk);
    }
    // Words too: one more pair would need an attempt; check what happened to the count.
    let st = m1.verify_status(&s, &k0);
    if let VerifyStatus::AwaitingHuman { .. } = st {
        words_shown_unprompted = true;
    }
    assert!(
        !words_shown_unprompted,
        "words shown without local start"
    );
    assert_eq!(
        st,
        VerifyStatus::Unverified { attempts_left: 3 },
        "the local human never pressed Verify, yet the pair is now {st:?}"
    );
}

/// G-SAS-2: a hard stop is keyed on the peer KEY, so a convener that re-introduces the same
/// person under a fresh key gets a fresh pair: new channel accepted, three fresh attempts.
#[test]
fn gate_demo_hard_stop_and_cap_reset_by_a_fresh_key_for_the_same_slot() {
    let mut v = ids(3);
    v.sort_by_key(|d| d.key_id());
    let s = session(4);
    let r = roster(s, [8; 32], &[&v[0], &v[2]]);
    let (c0, c2) = kk_pair(&r, &[&v[0], &v[2]], 0, 1);
    let (mut m0, mut m2) = (ChannelMap::new(), ChannelMap::new());
    m0.insert(c0).unwrap();
    m2.insert(c2).unwrap();
    let (k0, k2) = (v[0].key_id(), v[2].key_id());
    let commit = m0.verify_start(&s, &k2).unwrap();
    let MapEvent::Verify { send: Some(reveal), .. } = m2.open(&s, &k0, &commit).unwrap() else {
        panic!()
    };
    let MapEvent::Verify { send: Some(open), .. } = m0.open(&s, &k2, &reveal).unwrap() else {
        panic!()
    };
    m2.open(&s, &k0, &open).unwrap();
    assert_eq!(m2.verify_confirm(&s, &k0, false).unwrap(), None);
    assert_eq!(m2.verify_status(&s, &k0), VerifyStatus::HardStop);
    // Same "person", new key (v[1]) put in by the convener under the slot of v[0].
    let r2 = roster(s, [9; 32], &[&v[1], &v[2]]);
    let (_c1, c2b) = kk_pair(&r2, &[&v[1], &v[2]], 0, 1);
    m2.insert(c2b).unwrap();
    assert_eq!(
        m2.verify_status(&s, &v[1].key_id()),
        VerifyStatus::Unverified { attempts_left: 3 }
    );
}

/// G-SAS-3: verify_confirm(true) is not bound to the words the human compared. The peer can
/// replace the pending ceremony (abort + new commit/open) and the stale "match" pins the key.
#[test]
fn gate_demo_confirm_is_not_bound_to_the_words_shown() {
    let mut v = ids(2);
    v.sort_by_key(|d| d.key_id());
    let s = session(5);
    let r = roster(s, [8; 32], &[&v[0], &v[1]]);
    let (mut raw0, c1) = kk_pair(&r, &[&v[0], &v[1]], 0, 1);
    let h = *raw0.handshake_hash();
    let mut m1 = ChannelMap::new();
    m1.insert(c1).unwrap();
    let k0 = v[0].key_id();
    let commit_of = |r_c: &[u8; 32]| {
        use sha2::{Digest, Sha256};
        let mut d = Sha256::new();
        d.update(b"coagent-sas-commit-v1");
        d.update([0u8, 1]);
        d.update(h);
        d.update(r_c);
        let o: [u8; 32] = d.finalize().into();
        o
    };
    let run = |m1: &mut ChannelMap, raw0: &mut coagent_crypto::channel::Channel, rc: [u8; 32]| {
        let f = raw0
            .seal_record(RecordKind::Sas, &sas(SasStep::Commit, commit_of(&rc)))
            .unwrap();
        m1.open(&s, &k0, &f).unwrap();
        let f = raw0
            .seal_record(RecordKind::Sas, &sas(SasStep::Open, rc))
            .unwrap();
        match m1.open(&s, &k0, &f).unwrap() {
            MapEvent::Verify { show_words, .. } => show_words.unwrap(),
            _ => panic!(),
        }
    };
    let w1 = run(&mut m1, &mut raw0, [1; 32]);
    let junk = raw0
        .seal_record(RecordKind::Sas, &sas(SasStep::Request, [0; 32]))
        .unwrap();
    let _ = m1.open(&s, &k0, &junk); // AwaitingHuman{w1} -> Idle
    let w2 = run(&mut m1, &mut raw0, [2; 32]);
    assert_ne!(w1, w2);
    // The human was looking at w1 and says "match": w2's ceremony is the one that gets pinned.
    assert!(m1.verify_confirm(&s, &k0, true).unwrap().is_some());
}

/// G-CH-1: the public `seal_record` can send a Rekey record without rotating the sender's key;
/// the receiver rotates and every later envelope fails AEAD for the life of the channel.
#[test]
fn gate_demo_public_seal_record_can_desynchronise_rekey() {
    let mut v = ids(2);
    v.sort_by_key(|d| d.key_id());
    let s = session(6);
    let r = roster(s, [8; 32], &[&v[0], &v[1]]);
    let (mut c0, mut c1) = kk_pair(&r, &[&v[0], &v[1]], 0, 1);
    let rk = c0.seal_record(RecordKind::Rekey, &[]).unwrap();
    c1.open(&rk).unwrap();
    let f = c0.seal(draft(1, "x"), Instant::now()).unwrap();
    assert_eq!(c1.open(&f[0]).err(), Some(CryptoError::AeadOpenFailed));
}

/// G-CH-2: forgery attempts at the expected seq are unlimited and never close the channel.
#[test]
fn gate_demo_unbounded_failed_opens_leave_channel_open() {
    let mut v = ids(2);
    v.sort_by_key(|d| d.key_id());
    let s = session(7);
    let r = roster(s, [8; 32], &[&v[0], &v[1]]);
    let (mut c0, mut c1) = kk_pair(&r, &[&v[0], &v[1]], 0, 1);
    let mut bad = c0.seal(draft(1, "x"), Instant::now()).unwrap().remove(0);
    let good = bad.clone();
    let last = bad.len() - 1;
    for i in 0..10_000u32 {
        bad[last] ^= (i as u8) | 1;
        assert_eq!(c1.open(&bad).err(), Some(CryptoError::AeadOpenFailed));
        bad[last] = good[last];
    }
    assert!(c1.open(&good).is_ok());
}

/// G-DEC-1: canonical-decoding malleability probes on the envelope decoder (all must be refused).
#[test]
fn gate_ok_decoder_refuses_noncanonical_variants() {
    let b = Binding {
        session_id: session(1),
        local: coagent_proto::bytes::KeyId([2; 32]),
        peer: coagent_proto::bytes::KeyId([3; 32]),
    };
    let sender = Binding {
        session_id: b.session_id,
        local: b.peer,
        peer: b.local,
    };
    let mut d = draft(1, "x");
    d.body = serde_json::json!({"a": 1, "b": [1.5, "é"]});
    let e = Envelope::from_draft(d, &sender).unwrap();
    let good = String::from_utf8(canonical::encode(&e).unwrap()).unwrap();
    assert!(decode_for_channel(good.as_bytes(), &b).is_ok());
    let variants = [
        good.replace(r#""a":1"#, r#""a":1,"a":1"#),
        good.replace(r#""a":1"#, r#""a":1e0"#),
        good.replace(r#""a":1"#, r#""a":-0"#),
        good.replace("1.5", "15e-1"),
        good.replace("\u{e9}", &format!("{}u00e9", char::from(92u8))),
        format!("{good} "),
        format!("\u{feff}{good}"),
        good.replace(r#""seq":1"#, r#""seq":01"#),
        good.replace(r#""crit":false"#, r#""crit":false,"crit":true"#),
        good.replace(r#""re":null,"#, ""),
    ];
    for (i, x) in variants.iter().enumerate() {
        assert!(
            decode_for_channel(x.as_bytes(), &b).is_err(),
            "accepted non-canonical #{i}: {x:?}"
        );
    }
    // Deep nesting: refused, not a stack overflow.
    let deep = good.replace(
        r#"{"a":1"#,
        &format!(r#"{{"a":1,"z":{}0{}"#, "[".repeat(5000), "]".repeat(5000)),
    );
    assert!(decode_for_channel(deep.as_bytes(), &b).is_err());
}
