//! QA gate M3-ROSTER (independent tier-1 gate). Each test asserts the property the specification
//! asks for; a FAILING test here is a finding. Tests named `obs_*` only print what happens.
mod common;
mod prop_common;

use std::time::{Duration, Instant};

use coagent_crypto::identity::{DeviceIdentity, SignDomain};
use coagent_proto::bytes::{Digest32, KeyId, SessionId};
use coagent_proto::canonical;
use coagent_roster::{
    body_hash, next_with_cap, sign, IntakeError, Member, Outcome, ProposalIntake, Removed, Role,
    RosterBody, RosterChain, RosterError, SignedProposal, SignedRoster, ValidRoster, CAP,
    MAX_VERSIONS, PROPOSAL_LABEL, PROPOSAL_TTL,
};
use common::*;
use prop_common::*;

type Snap = (u64, [u8; 32], u8, Vec<KeyId>, Vec<KeyId>, Vec<(KeyId, Option<Role>, Option<KeyId>, Option<u8>)>);

fn snap(v: &ValidRoster) -> Snap {
    use coagent_crypto::kk::RosterView;
    let keys = v.member_keys();
    let per = keys
        .iter()
        .map(|k| (*k, v.role_of(k), v.proposer_of(k), v.slot_of(k)))
        .collect();
    (v.version(), v.hash(), v.cap(), keys, v.unchecked_proposals(), per)
}

fn refused_unchanged(c: &mut RosterChain, next: &SignedRoster) -> RosterError {
    let before = snap(c.current());
    let e = c.apply_with_report(next).err().expect("expected a refusal");
    assert_eq!(snap(c.current()), before, "a refused version moved the chain ({e:?})");
    e
}

fn genesis_cap(st: &DeviceIdentity, s: SessionId, cap: u8) -> SignedRoster {
    genesis_at(st, s, cap)
}

fn unhex(s: &str) -> Vec<u8> {
    (0..s.len()).step_by(2).map(|i| u8::from_str_radix(&s[i..i + 2], 16).unwrap()).collect()
}

/// An identity with `a`'s signing key and `b`'s Noise key pair (a second device key of `a`).
fn same_sign_key(a: &DeviceIdentity, b: &DeviceIdentity) -> DeviceIdentity {
    let sa = a.to_secret_bytes();
    let sb = b.to_secret_bytes();
    let mut x = sa[..37].to_vec();
    x.extend_from_slice(&sb[37..]);
    DeviceIdentity::from_secret_bytes(&x).unwrap()
}

// ------------------------------------------------------------------------------------------------
// Step 2: rosters MAIN produced are accepted byte for byte by the head
// ------------------------------------------------------------------------------------------------
#[test]
fn qa_main_bytes_round_trip_on_head() {
    let Ok(path) = std::env::var("QA_PIN_IN") else { return };
    let txt = std::fs::read_to_string(path).unwrap();
    let mut ids = vec![];
    let mut rosters = vec![];
    let mut hashes = vec![];
    for l in txt.lines() {
        let (k, val) = l.split_once(' ').unwrap();
        match k {
            "id" => ids.push(DeviceIdentity::from_secret_bytes(&unhex(val)).unwrap()),
            "roster" => rosters.push(val.to_string()),
            "hash" => hashes.push(val.to_string()),
            _ => panic!(),
        }
    }
    assert_eq!((ids.len(), rosters.len()), (5, 3));
    let dec: Vec<SignedRoster> =
        rosters.iter().map(|r| SignedRoster::decode(r.as_bytes()).unwrap()).collect();
    for (i, r) in dec.iter().enumerate() {
        assert_eq!(String::from_utf8(r.encode().unwrap()).unwrap(), rosters[i], "re-encode moved");
        let h: String = body_hash(&r.body).unwrap().iter().map(|b| format!("{b:02x}")).collect();
        assert_eq!(h, hashes[i], "hash moved");
        // Rebuild with head's constructors and compare bytes.
        let mut b = r.body.clone();
        b.members = r
            .body
            .members
            .iter()
            .map(|m| {
                let d = ids.iter().find(|d| d.key_id() == m.key_id).unwrap();
                Member::new(&d.public_keys(), d.key_id(), m.role, m.slot, m.added_in, &m.added_at)
            })
            .collect();
        let again = sign(&ids[0], b).unwrap();
        assert_eq!(String::from_utf8(again.encode().unwrap()).unwrap(), rosters[i], "rebuild moved");
    }
    let s = dec[0].body.session_id;
    let mut c = RosterChain::start(&ids[0].verified(), s, &ids[0].key_id(), &dec[0]).unwrap();
    c.apply(&dec[1]).unwrap();
    c.apply(&dec[2]).unwrap();
    let j = RosterChain::start(&ids[0].verified(), s, &ids[4].key_id(), &dec[2]).unwrap();
    assert!(j.current().unchecked_proposals().is_empty());
    println!("QA: 3 main-produced versions decode, re-encode, hash and validate identically on head");
}

// ------------------------------------------------------------------------------------------------
// Step 4: every cap value, version 1 and later, chain unchanged on refusal
// ------------------------------------------------------------------------------------------------
fn want_cap(cap: u8) -> Result<(), RosterError> {
    match cap {
        4 | 8 => Ok(()),
        c if c > CAP => Err(RosterError::CapExceeded),
        _ => Err(RosterError::BadCap),
    }
}

#[test]
fn qa_every_cap_value_in_version_1_and_later() {
    let v = ids(2);
    let s = session(90);
    for cap in 0..=255u8 {
        let r1 = genesis_cap(&v[0], s, cap);
        let got = RosterChain::start(&v[0].verified(), s, &v[0].key_id(), &r1).map(|_| ());
        assert_eq!(got, want_cap(cap), "version 1 cap {cap}");
    }
    for base in [4u8, 8] {
        let r1 = genesis_cap(&v[0], s, base);
        for cap in 0..=255u8 {
            let mut c = RosterChain::start(&v[0].verified(), s, &v[0].key_id(), &r1).unwrap();
            let r2 = next(&v[0], &r1, |b| b.cap = cap);
            let before = snap(c.current());
            let got = c.apply_with_report(&r2);
            match want_cap(cap) {
                Ok(()) => {
                    let rep = got.unwrap();
                    if cap != base {
                        assert_eq!(rep.cap_change.map(|x| (x.from, x.to)), Some((base, cap)));
                    } else {
                        assert_eq!(rep.cap_change, None);
                    }
                }
                Err(e) => {
                    assert_eq!(got.err(), Some(e), "later version {base}->{cap}");
                    assert_eq!(snap(c.current()), before);
                }
            }
        }
    }
}

// Lowering from 8 with members in every arrangement of slots (starter in slot 0 or 6).
#[test]
fn qa_lowering_in_every_slot_arrangement() {
    let v = ids(8);
    let s = session(91);
    let mut n = 0;
    for starter_slot in [0u8, 6] {
        for mask in 0u16..256 {
            if mask & (1 << starter_slot) != 0 {
                continue;
            }
            let slots: Vec<u8> = (0..8u8).filter(|i| mask & (1 << i) != 0).collect();
            let r1 = sign(
                &v[0],
                RosterBody {
                    session_id: s,
                    version: 1,
                    prev_hash: Digest32([0; 32]),
                    convener: v[0].key_id(),
                    cap: 8,
                    members: vec![member(&v[0], Role::Guest, starter_slot, 1)],
                    removed: vec![],
                },
            )
            .unwrap();
            let r2 = next(&v[0], &r1, |b| {
                for (i, sl) in slots.iter().enumerate() {
                    add(b, &v[i + 1], Role::Guest, *sl);
                }
            });
            let mut c = RosterChain::start(&v[0].verified(), s, &v[0].key_id(), &r1).unwrap();
            c.apply(&r2).unwrap();
            let r3 = next(&v[0], &r2, |b| b.cap = 4);
            let fits = slots.len() + 1 <= 4 && slots.iter().all(|x| *x < 4) && starter_slot < 4;
            let helper = next_with_cap(c.current(), 4);
            assert_eq!(helper.is_ok(), fits, "helper slots {slots:?} starter {starter_slot}");
            if fits {
                let rep = c.apply_with_report(&r3).unwrap();
                assert_eq!(rep.cap_change.map(|x| (x.from, x.to)), Some((8, 4)));
                // and raising back is always valid
                let r4 = next(&v[0], &r3, |b| b.cap = 8);
                c.apply(&r4).unwrap();
            } else {
                let e = refused_unchanged(&mut c, &r3);
                assert!(matches!(e, RosterError::CapExceeded | RosterError::BadSlot), "{e:?}");
            }
            n += 1;
        }
    }
    println!("QA: {n} slot arrangements lowered");
}

#[test]
fn qa_one_version_lowers_and_removes() {
    let v = ids(6);
    let s = session(92);
    let r1 = genesis_cap(&v[0], s, 8);
    let r2 = next(&v[0], &r1, |b| {
        for i in 1..5 {
            add(b, &v[i], Role::Guest, i as u8);
        }
    });
    let mut c = RosterChain::start(&v[0].verified(), s, &v[0].key_id(), &r1).unwrap();
    c.apply(&r2).unwrap();
    // remove the slot-4 member and lower in one version: valid
    let ok = next(&v[0], &r2, |b| {
        remove(b, &v[4]);
        b.cap = 4;
    });
    // remove the slot-3 member instead: slot 4 remains, refused
    let bad = next(&v[0], &r2, |b| {
        remove(b, &v[3]);
        b.cap = 4;
    });
    assert_eq!(refused_unchanged(&mut c, &bad), RosterError::BadSlot);
    let rep = c.apply_with_report(&ok).unwrap();
    assert_eq!(rep.cap_change.map(|x| (x.from, x.to)), Some((8, 4)));
    assert!(matches!(rep.applied, coagent_roster::Applied::Advanced { ref removed, .. } if removed == &vec![v[4].key_id()]));
    // a non-starter signs a cap change: refused
    let forged = sign(&v[1], next(&v[0], &ok, |b| b.cap = 8).body).unwrap();
    assert_eq!(refused_unchanged(&mut c, &forged), RosterError::BadSignature);
}

// ------------------------------------------------------------------------------------------------
// Step 4: lifetime bounds at the edges, via start and apply
// ------------------------------------------------------------------------------------------------
#[test]
fn qa_lifetime_edges_via_start() {
    let v = ids(3);
    let s = session(93);
    for (n_removed, ok) in [(30usize, true), (31, false)] {
        let r = first_roster(
            &v[0],
            s,
            40,
            vec![member(&v[0], Role::Guest, 0, 1), member(&v[1], Role::Guest, 1, 2)],
            (0..n_removed).map(|i| fake_removed(100 + i as u8, 3)).collect(),
        );
        let got = RosterChain::start(&v[0].verified(), s, &v[1].key_id(), &r);
        assert_eq!(got.is_ok(), ok, "{} entries via start", 2 + n_removed);
        if !ok {
            assert_eq!(got.err(), Some(RosterError::LifetimeExceeded));
        }
    }
    for (ver, ok) in [(256u64, true), (257, false), (u64::MAX, false)] {
        let r = first_roster(&v[0], s, ver, vec![member(&v[0], Role::Guest, 0, 1)], vec![]);
        let got = RosterChain::start(&v[0].verified(), s, &v[0].key_id(), &r);
        assert_eq!(got.is_ok(), ok, "version {ver} via start");
    }
    // next_with_cap at version 256 refuses
    let r = first_roster(&v[0], s, MAX_VERSIONS, vec![member(&v[0], Role::Guest, 0, 1)], vec![]);
    let c = RosterChain::start(&v[0].verified(), s, &v[0].key_id(), &r).unwrap();
    assert_eq!(next_with_cap(c.current(), 4).err(), Some(RosterError::TooManyVersions));
}

// ------------------------------------------------------------------------------------------------
// Step 3: signatures
// ------------------------------------------------------------------------------------------------
#[test]
fn qa_no_canonical_roster_body_begins_with_the_label() {
    // Any canonical roster encoding starts with '{'; the proposal message starts with 'c'.
    let v = ids(2);
    let r = genesis(&v[0], session(94));
    let e = canonical::encode(&r.body).unwrap();
    assert_eq!(e[0], b'{');
    assert_eq!(PROPOSAL_LABEL[0], b'c');
    // The decoder refuses anything not starting with '{' as a RosterBody.
    let mut msg = PROPOSAL_LABEL.to_vec();
    msg.push(0);
    msg.extend_from_slice(&e);
    assert!(canonical::decode::<RosterBody>(&msg).is_err());
    // A roster signature over a body is not a proposal signature and vice versa (starter-signed).
    let p = SignedProposal::sign(&v[0], body(&v[0], &r, &v[1], Role::Guest, 1)).unwrap();
    // Take the proposal sig as a roster sig over every body we can build from the same bytes: none.
    let mut fake = r.clone();
    fake.sig = p.sig;
    let got = RosterChain::start(&v[0].verified(), fake.body.session_id, &v[0].key_id(), &fake);
    assert_eq!(got.err(), Some(RosterError::BadSignature));
    // Reverse: the roster sig as a proposal sig.
    let mut p2 = p.clone();
    p2.sig = r.sig;
    assert!(p2.verify(&v[0].verified()).is_err());
    // A Roster-domain signature over LABEL||0||canonical(body) made by `sign` would need
    // canonical(body) to begin with the label: impossible (first byte '{').
    let raw = v[0].sign(SignDomain::Roster, &msg);
    let mut fake2 = r.clone();
    fake2.sig = raw;
    assert_eq!(
        RosterChain::start(&v[0].verified(), fake2.body.session_id, &v[0].key_id(), &fake2).err(),
        Some(RosterError::BadSignature)
    );
}

/// Replay a genuine proposal after a no-change version and after a limit-only change, with the
/// record left as signed and with at_version/at_hash rewritten.
#[test]
fn qa_replay_after_no_change_and_cap_only_versions() {
    let v = ids(6);
    let s = session(95);
    let r1 = genesis_cap(&v[0], s, 8);
    let r2 = next(&v[0], &r1, |b| add(b, &v[1], Role::Guest, 1));
    let pr = proposal(&v[1], &r2, &v[4], Role::Guest, 1);
    for change in ["none", "cap"] {
        let r3 = next(&v[0], &r2, |b| {
            if change == "cap" {
                b.cap = 4
            }
        });
        let mut c = RosterChain::start(&v[0].verified(), s, &v[1].key_id(), &r2).unwrap();
        c.apply(&r3).unwrap();
        let as_signed = next(&v[0], &r3, |b| add_proposed(b, &pr, Role::Guest, 2));
        let e = refused_unchanged(&mut c, &as_signed);
        assert_eq!(e, RosterError::BadProposalVersion(v[4].key_id()), "{change}");
        let rewritten = next(&v[0], &r3, |b| {
            add_proposed(b, &pr, Role::Guest, 2);
            let rec = b.members.last_mut().unwrap().proposal.as_mut().unwrap();
            rec.at_version = 3;
            rec.at_hash = hash_of(&r3);
        });
        let e = refused_unchanged(&mut c, &rewritten);
        assert_eq!(e, RosterError::BadProposalSignature(v[4].key_id()), "{change}");
        // positive control: a fresh proposal against r3 is accepted
        let fresh = proposal(&v[1], &r3, &v[4], Role::Guest, 2);
        c.apply(&next(&v[0], &r3, |b| add_proposed(b, &fresh, Role::Guest, 2))).unwrap();
    }
}

/// Re-use a genuine proposal for another candidate / role / session / proposer.
#[test]
fn qa_genuine_proposal_reused_for_other_fields() {
    let v = ids(7);
    let s = session(96);
    let r1 = genesis(&v[0], s);
    let r2 = next(&v[0], &r1, |b| {
        add(b, &v[1], Role::Guest, 1);
        add(b, &v[2], Role::Guest, 2);
    });
    let pr = proposal(&v[1], &r2, &v[4], Role::Guest, 1);
    let mut c = RosterChain::start(&v[0].verified(), s, &v[2].key_id(), &r2).unwrap();
    // other candidate (keys of v[5], record of pr)
    let mut other = pr.clone();
    other.body.candidate = coagent_roster::Candidate::new(&v[5].public_keys());
    let x = next(&v[0], &r2, |b| add_proposed(b, &other, Role::Guest, 3));
    assert_eq!(refused_unchanged(&mut c, &x), RosterError::BadProposalSignature(v[5].key_id()));
    // record role changed to observer (entry observer)
    let mut obs = pr.clone();
    obs.body.role = Role::Observer;
    let x = next(&v[0], &r2, |b| add_proposed(b, &obs, Role::Observer, 3));
    assert_eq!(refused_unchanged(&mut c, &x), RosterError::BadProposalSignature(v[4].key_id()));
    // record re-attributed to v[2]
    let mut re = pr.clone();
    re.body.proposer = v[2].key_id();
    let x = next(&v[0], &r2, |b| add_proposed(b, &re, Role::Guest, 3));
    assert_eq!(refused_unchanged(&mut c, &x), RosterError::BadProposalSignature(v[4].key_id()));
    // other session: same record in a roster of session 97 at the same version/hash shape
    let s2 = session(97);
    let q1 = genesis(&v[0], s2);
    let q2 = next(&v[0], &q1, |b| {
        add(b, &v[1], Role::Guest, 1);
        add(b, &v[2], Role::Guest, 2);
    });
    let mut c2 = RosterChain::start(&v[0].verified(), s2, &v[2].key_id(), &q2).unwrap();
    let x = next(&v[0], &q2, |b| {
        add_proposed(b, &pr, Role::Guest, 3);
        let rec = b.members.last_mut().unwrap().proposal.as_mut().unwrap();
        rec.at_hash = hash_of(&q2);
    });
    assert_eq!(refused_unchanged(&mut c2, &x), RosterError::BadProposalSignature(v[4].key_id()));
    // proposer is the candidate under a second key (same signing key, new Noise key): allowed by
    // design (06 §2.6 "second device"); show it is accepted by the validator
    let twin = same_sign_key(&v[1], &v[6]);
    let pt = proposal(&v[1], &r2, &twin, Role::Guest, 9);
    let x = next(&v[0], &r2, |b| add_proposed(b, &pt, Role::Guest, 3));
    let e = c.apply(&x).err();
    println!("QA obs: proposer's own signing key as candidate (new Noise key) -> {e:?}");
    assert_eq!(e, Some(RosterError::DuplicateDeviceKey(twin.key_id())));
}

// ------------------------------------------------------------------------------------------------
// The coordinator's extra item: promotion of a member proposed as an observer
// ------------------------------------------------------------------------------------------------
#[test]
fn qa_extra_promote_a_proposed_observer_to_guest() {
    let v = ids(6);
    let s = session(98);
    let r1 = genesis(&v[0], s);
    let r2 = next(&v[0], &r1, |b| add(b, &v[1], Role::Guest, 1));
    let pr = proposal(&v[1], &r2, &v[4], Role::Observer, 1);
    let r3 = next(&v[0], &r2, |b| add_proposed(b, &pr, Role::Observer, 2));
    let mut c = RosterChain::start(&v[0].verified(), s, &v[1].key_id(), &r2).unwrap();
    c.apply(&r3).unwrap();
    // control: promoting a DIRECTLY invited observer is accepted on main and on head
    let r3b = next(&v[0], &r2, |b| add(b, &v[5], Role::Observer, 3));
    let mut cb = RosterChain::start(&v[0].verified(), s, &v[1].key_id(), &r2).unwrap();
    cb.apply(&r3b).unwrap();
    let r4b = next(&v[0], &r3b, |b| b.members.iter_mut().for_each(|m| if m.key_id == v[5].key_id() { m.role = Role::Guest }));
    assert!(cb.apply(&r4b).is_ok(), "control: direct observer promotion");
    // the case
    let r4 = next(&v[0], &r3, |b| {
        b.members.iter_mut().for_each(|m| if m.key_id == v[4].key_id() { m.role = Role::Guest })
    });
    let got = c.apply(&r4);
    println!("QA extra: promote proposed observer -> {got:?}");
    // The record still verifies after a promotion: the signed body uses the RECORD's role.
    let rebuilt = r4.body.members.iter().find(|m| m.key_id == v[4].key_id()).unwrap()
        .rebuilt_proposal(&s).unwrap();
    assert!(rebuilt.verify(&v[1].verified()).is_ok(), "record verifies after promotion");
    // A joiner given r4 as its first roster
    let j = RosterChain::start(&v[0].verified(), s, &v[4].key_id(), &r4);
    println!("QA extra: joiner first roster with promoted proposed observer -> {:?}", j.as_ref().err());
    assert!(got.is_ok(), "a proposed observer cannot be promoted to guest: {got:?}");
}

#[test]
fn qa_extra_mirror_demoted_guest_promoted_back_and_proposer_removed() {
    let v = ids(6);
    let s = session(99);
    let r1 = genesis(&v[0], s);
    let r2 = next(&v[0], &r1, |b| add(b, &v[1], Role::Guest, 1));
    // proposed guest admitted as observer (I-7), later promoted back to guest
    let pr = proposal(&v[1], &r2, &v[4], Role::Guest, 1);
    let r3 = next(&v[0], &r2, |b| add_proposed(b, &pr, Role::Observer, 2));
    let mut c = RosterChain::start(&v[0].verified(), s, &v[1].key_id(), &r2).unwrap();
    c.apply(&r3).unwrap();
    let r4 = next(&v[0], &r3, |b| b.members.iter_mut().for_each(|m| if m.key_id == v[4].key_id() { m.role = Role::Guest }));
    let got = c.apply(&r4);
    println!("QA extra mirror: proposed guest admitted observer then promoted -> {got:?}");
    assert!(got.is_ok());
    // proposed guest demoted later then promoted
    let r5 = next(&v[0], &r4, |b| b.members.iter_mut().for_each(|m| if m.key_id == v[4].key_id() { m.role = Role::Observer }));
    assert!(c.apply(&r5).is_ok());
    let r6 = next(&v[0], &r5, |b| b.members.iter_mut().for_each(|m| if m.key_id == v[4].key_id() { m.role = Role::Guest }));
    assert!(c.apply(&r6).is_ok());
    // proposer removed later: the entry stays, still attributed, checked for the chain holder
    let r7 = next(&v[0], &r6, |b| remove(b, &v[1]));
    let mut c2 = RosterChain::start(&v[0].verified(), s, &v[0].key_id(), &r6).unwrap();
    let rep = c2.apply(&r7);
    println!("QA extra mirror: proposer removed -> {rep:?}");
    assert!(rep.is_ok());
    assert_eq!(c2.current().proposer_of(&v[4].key_id()), Some(v[1].key_id()));
    assert!(c2.current().unchecked_proposals().is_empty(), "the chain holder checked it at admission");
    let j = RosterChain::start(&v[0].verified(), s, &v[4].key_id(), &r7).unwrap();
    assert_eq!(j.current().unchecked_proposals(), vec![v[4].key_id()]);
}

// ------------------------------------------------------------------------------------------------
// Joiner's first roster: proposer present, removed, re-added; ids across versions
// ------------------------------------------------------------------------------------------------
#[test]
fn qa_joiner_proposer_readded_and_duplicate_ids_across_versions() {
    let v = ids(8);
    let s = session(100);
    let r1 = genesis(&v[0], s);
    let r2 = next(&v[0], &r1, |b| add(b, &v[1], Role::Guest, 1));
    let pr = proposal(&v[1], &r2, &v[4], Role::Guest, 7);
    let r3 = next(&v[0], &r2, |b| add_proposed(b, &pr, Role::Guest, 2));
    let r4 = next(&v[0], &r3, |b| remove(b, &v[1]));
    // P re-added under the same key as a NEW entry
    let r5 = next(&v[0], &r4, |b| add(b, &v[1], Role::Guest, 3));
    let mut c = RosterChain::start(&v[0].verified(), s, &v[0].key_id(), &r2).unwrap();
    for r in [&r3, &r4, &r5] {
        c.apply(r).unwrap();
    }
    // joiner at r5: P present again, the signature is checked (same keys)
    let j = RosterChain::start(&v[0].verified(), s, &v[4].key_id(), &r5).unwrap();
    assert!(j.current().unchecked_proposals().is_empty());
    // joiner at r5 with C's record sig replaced: refused, because P is present again
    let mut b5 = r5.body.clone();
    b5.members.iter_mut().for_each(|m| if m.key_id == v[4].key_id() { m.proposal.as_mut().unwrap().sig = junk_sig() });
    let bad5 = sign(&v[0], b5).unwrap();
    assert_eq!(
        RosterChain::start(&v[0].verified(), s, &v[5].key_id(), &bad5).err(),
        Some(RosterError::LocalNotMember)
    );
    assert_eq!(
        RosterChain::start(&v[0].verified(), s, &v[4].key_id(), &bad5).err(),
        Some(RosterError::BadProposalSignature(v[4].key_id()))
    );
    // duplicate proposal id ACROSS versions: remove C, then admit D through a proposal with the
    // same id 7
    let r6 = next(&v[0], &r5, |b| remove(b, &v[4]));
    c.apply(&r6).unwrap();
    let pd = proposal(&v[1], &r6, &v[5], Role::Guest, 7);
    let r7 = next(&v[0], &r6, |b| add_proposed(b, &pd, Role::Guest, 2));
    let got = c.apply(&r7);
    println!("QA obs: proposal id reused across versions after the first holder left -> {got:?}");
}

// ------------------------------------------------------------------------------------------------
// Step 5: the intake builds a body the validator refuses
// ------------------------------------------------------------------------------------------------
#[test]
fn qa_intake_approval_of_a_twin_key_builds_a_refused_body_and_stales_others() {
    let v = ids(9);
    let s = session(101);
    let r1 = genesis(&v[0], s);
    let r2 = next(&v[0], &r1, |b| {
        add(b, &v[1], Role::Guest, 1);
        add(b, &v[2], Role::Guest, 2);
    });
    let (vr, mut i) = intake(&v[0], &r2);
    let t = t0();
    // honest Q proposes C
    let honest = proposal(&v[2], &r2, &v[6], Role::Guest, 1);
    let hid = i.receive(&vr, &v[2].key_id(), &honest.encode().unwrap(), t).unwrap();
    // hostile P proposes a candidate carrying P's own signing key with a fresh Noise key
    let twin = same_sign_key(&v[1], &v[7]);
    let hostile = proposal(&v[1], &r2, &twin, Role::Guest, 2);
    let rx = i.receive(&vr, &v[1].key_id(), &hostile.encode().unwrap(), t);
    println!("QA: intake receive of twin-key candidate -> {rx:?}");
    let id = rx.expect("intake accepted it");
    let body = i.approve(&vr, &id, Role::Guest, AT, t).unwrap();
    println!("QA: honest proposal after approving the twin -> {:?}, Q quota used {}", i.outcome(&hid), i.used_by(&v[2].key_id()));
    let signed = sign(&v[0], body).unwrap();
    let mut c = RosterChain::start(&v[0].verified(), s, &v[0].key_id(), &r2).unwrap();
    let got = c.apply(&signed);
    println!("QA: validator on the approved body -> {got:?}");
    assert!(got.is_ok(), "an approval built a body the validator refuses: {got:?}");
}

#[test]
fn qa_intake_approval_at_version_256_builds_a_refused_body() {
    let v = ids(4);
    let s = session(102);
    let r = first_roster(
        &v[0],
        s,
        MAX_VERSIONS,
        vec![member(&v[0], Role::Guest, 0, 1), member(&v[1], Role::Guest, 1, 2)],
        vec![],
    );
    let (vr, mut i) = intake(&v[0], &r);
    let t = t0();
    let p = proposal(&v[1], &r, &v[2], Role::Guest, 1);
    let rx = i.receive(&vr, &v[1].key_id(), &p.encode().unwrap(), t);
    println!("QA: intake receive at version 256 -> {rx:?}");
    let Ok(id) = rx else { return };
    let body = i.approve(&vr, &id, Role::Guest, AT, t).unwrap();
    let mut c = RosterChain::start(&v[0].verified(), s, &v[0].key_id(), &r).unwrap();
    let got = c.apply(&sign(&v[0], body).unwrap());
    println!("QA: validator on the approved body at 256 -> {got:?}; outcome {:?}", i.outcome(&id));
    assert!(got.is_ok(), "an approval built a body the validator refuses: {got:?}");
}

// DQ3: a removed person re-proposed under the same signing key with a new Noise key
#[test]
fn qa_dq3_removed_signing_key_comes_back_through_a_proposal() {
    let v = ids(8);
    let s = session(103);
    let r1 = genesis(&v[0], s);
    let r2 = next(&v[0], &r1, |b| {
        add(b, &v[1], Role::Guest, 1);
        add(b, &v[3], Role::Guest, 3);
    });
    let r3 = next(&v[0], &r2, |b| remove(b, &v[3]));
    let back = same_sign_key(&v[3], &v[7]);
    let (vr, mut i) = intake(&v[0], &r3);
    let t = t0();
    let p = proposal(&v[1], &r3, &back, Role::Guest, 1);
    let rx = i.receive(&vr, &v[1].key_id(), &p.encode().unwrap(), t);
    println!("QA DQ3: intake -> {rx:?}");
    let body = i.approve(&vr, &rx.unwrap(), Role::Guest, AT, t).unwrap();
    let slot = body.members.last().unwrap().slot;
    let mut c = RosterChain::start(&v[0].verified(), s, &v[1].key_id(), &r3).unwrap();
    let got = c.apply(&sign(&v[0], body).unwrap());
    println!("QA DQ3: validator -> {got:?}; new entry slot {slot} (removed key had slot 3)");
}

// ------------------------------------------------------------------------------------------------
// Step 5: intake bounds, order, nothing stored, time
// ------------------------------------------------------------------------------------------------
#[test]
fn qa_intake_refusal_after_an_expiry_changes_accounting() {
    let v = ids(8);
    let r = world(&v, session(104), 3, 0);
    let (vr, mut i) = intake(&v[0], &r[1]);
    let t = t0();
    i.receive(&vr, &v[1].key_id(), &proposal(&v[1], &r[1], &v[5], Role::Guest, 1).encode().unwrap(), t).unwrap();
    let before = i.accounting();
    let later = t + PROPOSAL_TTL;
    let e = i.receive(&vr, &v[2].key_id(), b"junk", later);
    println!("QA obs: refused input at TTL: {e:?}; accounting before {before:?} after {:?}", i.accounting());
}

#[test]
fn qa_intake_time_backwards_and_far_future() {
    let v = ids(8);
    let r = world(&v, session(105), 3, 0);
    let (vr, mut i) = intake(&v[0], &r[1]);
    let t = Instant::now() + Duration::from_secs(3600);
    let id = i.receive(&vr, &v[1].key_id(), &proposal(&v[1], &r[1], &v[5], Role::Guest, 1).encode().unwrap(), t).unwrap();
    // time goes backwards: still pending
    i.tick(&vr, t - Duration::from_secs(3000));
    assert_eq!(i.outcome(&id), Some(Outcome::Pending));
    // just before TTL: pending; at TTL: expired
    i.tick(&vr, t + PROPOSAL_TTL - Duration::from_nanos(1));
    assert_eq!(i.outcome(&id), Some(Outcome::Pending));
    i.tick(&vr, t + PROPOSAL_TTL);
    assert_eq!(i.outcome(&id), Some(Outcome::Expired));
    // far future
    let id2 = i.receive(&vr, &v[2].key_id(), &proposal(&v[2], &r[1], &v[6], Role::Guest, 2).encode().unwrap(), t).unwrap();
    i.tick(&vr, t + Duration::from_secs(u32::MAX as u64 * 1000));
    assert_eq!(i.outcome(&id2), Some(Outcome::Expired));
    // id replay after expiry and after decline
    let e = i.receive(&vr, &v[2].key_id(), &proposal(&v[2], &r[1], &v[6], Role::Guest, 2).encode().unwrap(), t + PROPOSAL_TTL * 3);
    assert_eq!(e.err(), Some(IntakeError::DuplicateId));
    let id3 = i.receive(&vr, &v[3].key_id(), &proposal(&v[3], &r[1], &v[7], Role::Guest, 3).encode().unwrap(), t).unwrap();
    i.decline(&vr, &id3, t).unwrap();
    let e = i.receive(&vr, &v[3].key_id(), &proposal(&v[3], &r[1], &v[7], Role::Guest, 3).encode().unwrap(), t);
    assert_eq!(e.err(), Some(IntakeError::DuplicateId));
}

/// Order: a muted proposer with quota used and a duplicate id while the session is full of pending
/// proposals. Spec order within check 9: pending-per-proposer, (session), quota, mute; 10 last.
#[test]
fn qa_intake_order_inside_check_9_and_10() {
    let v = ids(12);
    let r = world_at(&v, session(106), 8, 5);
    let (vr, mut i) = intake(&v[0], &r[1]);
    let t = t0();
    let mut n = 1u8;
    // P uses 7 of its quota through declines; on the 8th, decline and mute.
    for k in 0..8 {
        let p = proposal(&v[1], &r[1], &v[7], Role::Guest, n);
        let id = i.receive(&vr, &v[1].key_id(), &p.encode().unwrap(), t).unwrap();
        if k < 7 { i.decline(&vr, &id, t).unwrap() } else { i.decline_and_mute(&vr, &id, t).unwrap() }
        n += 1;
    }
    // quota used AND muted AND id replay -> QuotaUsed (earliest)
    let e = i.receive(&vr, &v[1].key_id(), &proposal(&v[1], &r[1], &v[7], Role::Guest, 1).encode().unwrap(), t);
    assert_eq!(e.err(), Some(IntakeError::QuotaUsed));
    // fill the session's three pending with Q, G3, G4
    for (k, g) in [2usize, 3, 4].iter().enumerate() {
        i.receive(&vr, &v[*g].key_id(), &proposal(&v[*g], &r[1], &v[8 + k], Role::Guest, 100 + k as u8).encode().unwrap(), t).unwrap();
    }
    // P now: session full AND quota AND muted -> SessionPendingFull
    let e = i.receive(&vr, &v[1].key_id(), &proposal(&v[1], &r[1], &v[7], Role::Guest, 50).encode().unwrap(), t);
    assert_eq!(e.err(), Some(IntakeError::SessionPendingFull));
}

/// Starvation: `h` hostile guests keep the three session slots full within their quotas; an
/// honest guest retries every minute; the starter does nothing. Returns minutes until the honest
/// proposal is accepted.
fn starve(h: usize) -> u64 {
    let v = ids(h + 6);
    // members: starter + h hostile + honest guest; at cap 8 with a free seat
    let r = world_at(&v, session(107), 8, h + 1);
    let (vr, mut i) = intake(&v[0], &r[1]);
    let t = t0();
    let honest = h + 1;
    let cand = h + 2;
    let mut id = 1u8;
    for minute in 0..=2000u64 {
        let now = t + Duration::from_secs(60 * minute);
        // hostile guests act first every minute
        // optimal order: the hostile guest with the most quota left goes first
        let mut order: Vec<usize> = (1..=h).collect();
        order.sort_by_key(|g| i.used_by(&v[*g].key_id()));
        for g in order {
            id = id.wrapping_add(1);
            let p = proposal(&v[g], &r[1], &v[cand + 1], Role::Guest, id);
            let _ = i.receive(&vr, &v[g].key_id(), &p.encode().unwrap(), now);
        }
        id = id.wrapping_add(1);
        let p = proposal(&v[honest], &r[1], &v[cand], Role::Guest, id);
        if i.receive(&vr, &v[honest].key_id(), &p.encode().unwrap(), now).is_ok() {
            return minute;
        }
    }
    u64::MAX
}

#[test]
fn qa_starvation_by_colluding_guests() {
    for h in [1usize, 2, 3, 4, 5] {
        println!("QA starvation: {h} hostile guest(s): honest proposal accepted after {} min (starter idle)", starve(h));
    }
}

/// Two approvals racing against one version.
#[test]
fn qa_two_approvals_race() {
    let v = ids(8);
    let r = world(&v, session(108), 3, 0);
    let (vr, mut i) = intake(&v[0], &r[1]);
    let t = t0();
    let a = i.receive(&vr, &v[1].key_id(), &proposal(&v[1], &r[1], &v[5], Role::Guest, 1).encode().unwrap(), t).unwrap();
    let b = i.receive(&vr, &v[2].key_id(), &proposal(&v[2], &r[1], &v[6], Role::Guest, 2).encode().unwrap(), t).unwrap();
    assert!(i.approve(&vr, &a, Role::Guest, AT, t).is_ok());
    assert_eq!(i.approve(&vr, &b, Role::Guest, AT, t).err(), Some(IntakeError::NotPending(Outcome::Stale)));
    assert_eq!(i.approve(&vr, &a, Role::Guest, AT, t).err(), Some(IntakeError::NotPending(Outcome::Approved)));
}

/// Stale handling across a cap-only change.
#[test]
fn qa_stale_across_cap_only_change() {
    let v = ids(8);
    let r = world_at(&v, session(109), 8, 2);
    let (vr, mut i) = intake(&v[0], &r[1]);
    let t = t0();
    let a = i.receive(&vr, &v[1].key_id(), &proposal(&v[1], &r[1], &v[5], Role::Guest, 1).encode().unwrap(), t).unwrap();
    let r3b = next_with_cap(&vr, 4).unwrap();
    let r3 = sign(&v[0], r3b).unwrap();
    let vr3 = view(&v[0], &v[0], &r3);
    assert_eq!(i.approve(&vr3, &a, Role::Guest, AT, t).err(), Some(IntakeError::NotPending(Outcome::Stale)));
    assert_eq!(i.used_by(&v[1].key_id()), 1, "the stale proposal used quota");
}

/// Proposals staled by an approval are not reported by `tick` (the caller must poll `outcome`).
#[test]
fn obs_approval_staled_proposals_are_not_reported_by_tick() {
    let v = ids(8);
    let r = world(&v, session(110), 3, 0);
    let (vr, mut i) = intake(&v[0], &r[1]);
    let t = t0();
    let a = i.receive(&vr, &v[1].key_id(), &proposal(&v[1], &r[1], &v[5], Role::Guest, 1).encode().unwrap(), t).unwrap();
    let b = i.receive(&vr, &v[2].key_id(), &proposal(&v[2], &r[1], &v[6], Role::Guest, 2).encode().unwrap(), t).unwrap();
    let body = i.approve(&vr, &a, Role::Guest, AT, t).unwrap();
    let r3 = sign(&v[0], body).unwrap();
    let vr3 = view(&v[0], &v[0], &r3);
    let ended = i.tick(&vr3, t + Duration::from_secs(1));
    println!("QA obs: after approval, outcome(b) = {:?}; tick reports {:?}", i.outcome(&b), ended);
}

/// DQ6: a proposal carried as a JSON value inside an envelope body and re-serialised (serde_json's
/// Value map sorts keys) is no longer the canonical encoding of a SignedProposal.
#[test]
fn obs_dq6_proposal_through_a_json_value_is_not_canonical() {
    let v = ids(8);
    let r = world(&v, session(111), 3, 0);
    let (vr, mut i) = intake(&v[0], &r[1]);
    let p = proposal(&v[1], &r[1], &v[5], Role::Guest, 1);
    let as_value: serde_json::Value = serde_json::to_value(&p).unwrap();
    let envelope_body = serde_json::json!({ "proposal": as_value, "note": "hi" });
    let bytes = serde_json::to_vec(&envelope_body["proposal"]).unwrap();
    let direct = p.encode().unwrap();
    println!("QA obs DQ6: value bytes equal canonical: {}", bytes == direct);
    println!("QA obs DQ6: intake on value bytes -> {:?}", i.receive(&vr, &v[1].key_id(), &bytes, t0()));
}
