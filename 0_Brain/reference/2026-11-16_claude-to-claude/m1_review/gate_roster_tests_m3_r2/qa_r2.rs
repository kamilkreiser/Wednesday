//! QA gate M3-ROSTER round 2 (head d88d5d7). Findings-only tests; not part of the branch.
#![allow(clippy::all, unused_imports, unused_variables, dead_code)]
mod common;
mod prop_common;

use std::time::Duration;

use coagent_crypto::identity::DeviceIdentity;
use coagent_proto::bytes::{Digest32, KeyId};
use coagent_roster::{
    next_with_cap, sign, Applied, IntakeError, Member, Outcome, ProposalIntake, Removed, Role,
    RosterChain, RosterError, SignedProposal, SignedRoster, CAP, CAP_DEFAULT, MAX_PROPOSAL_BYTES,
    MAX_VERSIONS, PROPOSAL_TTL,
};
use common::*;
use prop_common::*;

fn twin(a: &DeviceIdentity, b: &DeviceIdentity) -> DeviceIdentity {
    let sa = a.to_secret_bytes();
    let sb = b.to_secret_bytes();
    let mut x = sa[..37].to_vec();
    x.extend_from_slice(&sb[37..]);
    DeviceIdentity::from_secret_bytes(&x).unwrap()
}
fn by(p: &SignedProposal) -> Vec<u8> {
    p.encode().unwrap()
}
fn chain(st: &DeviceIdentity, local: &DeviceIdentity, r: &SignedRoster) -> RosterChain {
    RosterChain::start(&st.verified(), r.body.session_id, &local.key_id(), r).unwrap()
}
fn joiner(st: &DeviceIdentity, local: &DeviceIdentity, r: &SignedRoster) -> Result<RosterChain, RosterError> {
    RosterChain::start(&st.verified(), r.body.session_id, &local.key_id(), r)
}
fn set_role(b: &mut coagent_roster::RosterBody, k: &DeviceIdentity, role: Role) {
    b.members.iter_mut().find(|m| m.key_id == k.key_id()).unwrap().role = role;
}

// ------------------------------------------------------------------------------------------------
// F1 re-attack
// ------------------------------------------------------------------------------------------------

/// Promotion/demotion sequences of proposed and directly invited members, every order; a chain
/// holder applies each, and a joiner is given each version first.
#[test]
fn r2_f1_promotion_demotion_sequences() {
    let v = ids(8);
    let s = session(201);
    let r = world(&v, s, 2, 1); // starter, P=v1, Q=v2 guests, O=v3 observer (direct)
    let (p, c_obs, c_guest) = (&v[1], &v[4], &v[5]);
    let pr_o = proposal(p, &r[1], c_obs, Role::Observer, 1);
    // v3: C_obs admitted as observer through a proposal
    let r3 = next(&v[0], &r[1], |b| add_proposed(b, &pr_o, Role::Observer, 4));
    let pr_g = proposal(p, &r3, c_guest, Role::Guest, 2);
    // v4: C_guest admitted as OBSERVER (lowered) through a proposal
    let r4 = next(&v[0], &r3, |b| add_proposed(b, &pr_g, Role::Observer, 5));
    let mut versions = vec![r3.clone(), r4.clone()];
    let steps: Vec<Box<dyn Fn(&mut coagent_roster::RosterBody)>> = vec![
        Box::new(|b| set_role(b, &v[4], Role::Guest)),    // promote proposed observer
        Box::new(|b| set_role(b, &v[5], Role::Guest)),    // promote lowered proposed guest
        Box::new(|b| set_role(b, &v[3], Role::Guest)),    // promote direct observer
        Box::new(|b| set_role(b, &v[4], Role::Observer)), // demote again
        Box::new(|b| set_role(b, &v[5], Role::Observer)),
        Box::new(|b| { set_role(b, &v[4], Role::Guest); set_role(b, &v[5], Role::Guest); }),
        Box::new(|b| remove(b, &v[1])), // proposer removed afterwards
        Box::new(|b| set_role(b, &v[4], Role::Observer)),
        Box::new(|b| set_role(b, &v[4], Role::Guest)),
    ];
    for f in steps.iter() {
        let last = versions.last().unwrap().clone();
        versions.push(next(&v[0], &last, |b| f(b)));
    }
    let mut ch = chain(&v[0], &v[2], &r[1]);
    for (k, ver) in versions.iter().enumerate() {
        let got = ch.apply(ver);
        println!("R2 F1 holder v{} -> {:?}", ver.body.version, got);
        assert!(got.is_ok(), "holder refused step {k}: {got:?}");
        let j = joiner(&v[0], &v[2], ver);
        println!("R2 F1 joiner first v{} -> ok={} unchecked={:?}", ver.body.version, j.is_ok(), j.as_ref().map(|c| c.current().unchecked_proposals().len()));
        assert!(j.is_ok(), "joiner refused v{}: {:?}", ver.body.version, j.err());
    }
    // A joiner after the proposer's removal marks both proposed entries unchecked.
    let lastv = versions.last().unwrap();
    let j = joiner(&v[0], &v[2], lastv).unwrap();
    assert_eq!(j.current().unchecked_proposals().len(), 2);
}

/// A role raise ON the admitting version is refused, also when combined with a cap change and with
/// a legitimate promotion of another member in the same version.
#[test]
fn r2_f1_raise_on_admitting_version_refused_in_combinations() {
    let v = ids(8);
    let s = session(202);
    let r1 = genesis_at(&v[0], s, CAP_DEFAULT);
    let r2 = next(&v[0], &r1, |b| {
        add(b, &v[1], Role::Guest, 1);
        add(b, &v[2], Role::Observer, 2);
    });
    let pr = proposal(&v[1], &r2, &v[5], Role::Observer, 1);
    let bad = next(&v[0], &r2, |b| {
        b.cap = CAP;
        set_role(b, &v[2], Role::Guest);
        add_proposed(b, &pr, Role::Guest, 5);
    });
    let mut ch = chain(&v[0], &v[1], &r2);
    let before = (ch.current().version(), ch.current().hash());
    assert_eq!(ch.apply(&bad).err(), Some(RosterError::ProposedRoleRaised(v[5].key_id())));
    assert_eq!((ch.current().version(), ch.current().hash()), before);
    assert_eq!(joiner(&v[0], &v[1], &bad).err(), Some(RosterError::ProposedRoleRaised(v[5].key_id())));
    // positive control: same version with the right role is accepted
    let good = next(&v[0], &r2, |b| {
        b.cap = CAP;
        set_role(b, &v[2], Role::Guest);
        add_proposed(b, &pr, Role::Observer, 5);
    });
    assert!(ch.apply(&good).is_ok());
}

/// Remove and re-add the same key with a higher role carrying the OLD proposal record.
#[test]
fn r2_f1_remove_and_readd_with_old_record() {
    let v = ids(8);
    let s = session(203);
    let r = world(&v, s, 2, 0);
    let c = &v[4];
    let pr = proposal(&v[1], &r[1], c, Role::Observer, 1);
    let r3 = next(&v[0], &r[1], |b| add_proposed(b, &pr, Role::Observer, 4));
    let r4 = next(&v[0], &r3, |b| remove(b, c));
    let mut ch = chain(&v[0], &v[2], &r[1]);
    ch.apply(&r3).unwrap();
    ch.apply(&r4).unwrap();
    // (a) re-add as guest with the old record, added_in = 5
    let a = next(&v[0], &r4, |b| {
        let mut m = Member::proposed(&pr, Role::Guest, 4, 5, AT);
        m.added_in = 5;
        b.members.push(m);
    });
    let ga = ch.apply(&a);
    println!("R2 F1 readd old record added_in=5 -> {ga:?}");
    assert!(ga.is_err());
    // (b) re-add with the old record and its old added_in (3)
    let b_ = next(&v[0], &r4, |b| b.members.push(Member::proposed(&pr, Role::Guest, 4, 3, AT)));
    let gb = ch.apply(&b_);
    println!("R2 F1 readd old record added_in=3 -> {gb:?}");
    assert!(gb.is_err());
    // (c) a NEW proposal for the removed key, made at v4: refused by the validator and the intake
    let pr2 = proposal(&v[1], &r4, c, Role::Guest, 2);
    let c_ = next(&v[0], &r4, |b| add_proposed(b, &pr2, Role::Guest, 4));
    let gc = ch.apply(&c_);
    println!("R2 F1 readd new proposal -> {gc:?}");
    assert_eq!(gc.err(), Some(RosterError::ProposedRemovedKey(c.key_id())));
    let (vr4, mut i) = intake(&v[0], &r4);
    assert_eq!(i.receive(&vr4, &v[1].key_id(), &by(&pr2), t0()).err(), Some(IntakeError::CandidateRemoved));
    // (d) the starter re-adds directly as guest (no record): accepted, shows no proposer
    let d = next(&v[0], &r4, |b| add(b, c, Role::Guest, 4));
    let gd = ch.apply(&d);
    println!("R2 F1 direct readd as guest -> {gd:?}");
    assert!(gd.is_ok());
    assert_eq!(ch.current().proposer_of(&c.key_id()), None);
}

/// What a joiner given a later version first cannot detect: an entry admitted ABOVE its proposed
/// role on a version the joiner never saw. And the two-step route by which a hostile starter gets
/// the same end state that every holder sees only as a role change.
#[test]
fn r2_f1_joiner_cannot_detect_an_unseen_raised_admission() {
    let v = ids(8);
    let s = session(204);
    let r = world(&v, s, 2, 0);
    let c = &v[4];
    let pr = proposal(&v[1], &r[1], c, Role::Observer, 1);
    // v3' admits the proposed observer AS GUEST: every holder refuses it.
    let r3bad = next(&v[0], &r[1], |b| add_proposed(b, &pr, Role::Guest, 4));
    let mut ch = chain(&v[0], &v[2], &r[1]);
    assert!(ch.apply(&r3bad).is_err());
    // v4' on top of v3' (adds the joiner J = v5 directly): given first, the joiner accepts it.
    let r4bad = next(&v[0], &r3bad, |b| add(b, &v[5], Role::Guest, 5));
    let j = joiner(&v[0], &v[5], &r4bad);
    println!("R2 F1 joiner given v4 over a refused v3 -> ok={}", j.is_ok());
    assert!(j.is_ok(), "the documented limit: a joiner trusts the chain for earlier admissions");
    assert_eq!(j.unwrap().current().role_of(&c.key_id()), Some(Role::Guest));
    // The two-step route: v3 admits as observer, v4 promotes. Holders see role_changed = [C].
    let r3 = next(&v[0], &r[1], |b| add_proposed(b, &pr, Role::Observer, 4));
    let r4 = next(&v[0], &r3, |b| set_role(b, c, Role::Guest));
    ch.apply(&r3).unwrap();
    let got = ch.apply(&r4).unwrap();
    println!("R2 F1 two-step promotion as seen by a holder -> {got:?}");
    assert_eq!(got, Applied::Advanced { added: vec![], removed: vec![], role_changed: vec![c.key_id()] });
}

// ------------------------------------------------------------------------------------------------
// F2 re-attack: approve must never return Ok with a body a fresh chain refuses, and a refused
// approval must leave every other proposal and proposer untouched.
// ------------------------------------------------------------------------------------------------

fn assert_valid(st: &DeviceIdentity, cur: &SignedRoster, body: coagent_roster::RosterBody, what: &str) {
    let signed = sign(st, body).unwrap();
    let mut ch = chain(st, st, cur);
    let got = ch.apply(&signed);
    assert!(got.is_ok(), "{what}: holder refused the approved body: {got:?}");
    let j = joiner(st, st, &signed);
    assert!(j.is_ok(), "{what}: joiner refused the approved body: {:?}", j.err());
}

/// A new intake for the same session (the starter's daemon restarted: the intake is in memory) has
/// no record of ids carried by existing entries. A guest re-uses such a proposal id: `receive`
/// shows a card, and only the validator run in `approve` stops it.
#[test]
fn r2_f2_proposal_id_carried_by_an_existing_entry_reaches_a_card() {
    let v = ids(10);
    let s = session(205);
    let r = world(&v, s, 3, 0); // P=v1, Q=v2, G=v3
    let pr = proposal(&v[1], &r[1], &v[5], Role::Guest, 7);
    let r3 = next(&v[0], &r[1], |b| add_proposed(b, &pr, Role::Guest, 5));
    let (vr3, mut i) = intake(&v[0], &r3); // fresh intake
    let t = t0();
    let qid = i.receive(&vr3, &v[2].key_id(), &by(&proposal(&v[2], &r3, &v[6], Role::Guest, 30)), t).unwrap();
    let q_used = i.used_by(&v[2].key_id());
    let rx = i.receive(&vr3, &v[1].key_id(), &by(&proposal(&v[1], &r3, &v[7], Role::Guest, 7)), t);
    println!("R2 F2 receive of a proposal reusing an entry's proposal id -> {rx:?}");
    let id = rx.expect("the intake shows a card for it (no check against ids on the roster)");
    let got = i.approve_with_report(&vr3, &id, Role::Guest, AT, t);
    println!("R2 F2 approve of it -> {:?}", got.as_ref().map(|a| a.made_stale.clone()));
    assert_eq!(got.err(), Some(IntakeError::InvalidApproval(RosterError::DuplicateProposalId(v[7].key_id()))));
    assert_eq!(i.outcome(&id), Some(Outcome::RefusedInvalid));
    assert_eq!(i.outcome(&qid), Some(Outcome::Pending), "a refused approval staled another proposal");
    assert_eq!(i.used_by(&v[2].key_id()), q_used, "a refused approval charged another proposer");
    // Q can still be approved, validly.
    let body = i.approve(&vr3, &qid, Role::Guest, AT, t).unwrap();
    assert_valid(&v[0], &r3, body, "Q after refused");
}

/// Lifetime bound exactly reached; one below; and the version just below the bound.
#[test]
fn r2_f2_lifetime_and_version_edges() {
    let v = ids(8);
    let s = session(206);
    let mk = |version: u64, nrem: usize| {
        let removed: Vec<Removed> = (0..nrem).map(|n| fake_removed(100 + n as u8, 2)).collect();
        first_roster(
            &v[0],
            s,
            version,
            vec![member(&v[0], Role::Guest, 0, 1), member(&v[1], Role::Guest, 1, 2), member(&v[2], Role::Guest, 2, 2)],
            removed,
        )
    };
    // 3 members + 28 removed = 31: one more fits (32).
    let r = mk(40, 28);
    let (vr, mut i) = intake(&v[0], &r);
    let id = i.receive(&vr, &v[1].key_id(), &by(&proposal(&v[1], &r, &v[5], Role::Guest, 1)), t0()).unwrap();
    let body = i.approve(&vr, &id, Role::Guest, AT, t0()).unwrap();
    assert_eq!(body.members.len() + body.removed.len(), 32);
    assert_valid(&v[0], &r, body, "lifetime 32");
    // 3 + 29 = 32: nothing more.
    let r = mk(40, 29);
    let (vr, mut i) = intake(&v[0], &r);
    let before = i.accounting();
    assert_eq!(i.receive(&vr, &v[1].key_id(), &by(&proposal(&v[1], &r, &v[5], Role::Guest, 1)), t0()).err(), Some(IntakeError::LifetimeFull));
    assert_eq!(i.accounting(), before);
    // version 255: the approval builds 256, valid.
    let r = mk(MAX_VERSIONS - 1, 0);
    let (vr, mut i) = intake(&v[0], &r);
    let id = i.receive(&vr, &v[1].key_id(), &by(&proposal(&v[1], &r, &v[5], Role::Guest, 1)), t0()).unwrap();
    let body = i.approve(&vr, &id, Role::Guest, AT, t0()).unwrap();
    assert_eq!(body.version, MAX_VERSIONS);
    assert_valid(&v[0], &r, body, "version 256");
}

/// The limit fills by another route (a direct invite) while a proposal is pending; then the roster
/// of another session; then time going backwards.
#[test]
fn r2_f2_cap_full_by_another_route_other_session_time_backwards() {
    let v = ids(10);
    let s = session(207);
    let r1 = genesis_at(&v[0], s, CAP_DEFAULT);
    let r2 = next(&v[0], &r1, |b| {
        add(b, &v[1], Role::Guest, 1);
        add(b, &v[2], Role::Guest, 2);
    });
    let (vr2, mut i) = intake(&v[0], &r2);
    let t = t0() + Duration::from_secs(1000);
    let id = i.receive(&vr2, &v[1].key_id(), &by(&proposal(&v[1], &r2, &v[5], Role::Guest, 1)), t).unwrap();
    // the starter invites v3 directly: 4 of 4
    let r3 = next(&v[0], &r2, |b| add(b, &v[3], Role::Guest, 3));
    let vr3 = view(&v[0], &v[0], &r3);
    assert_eq!(i.approve(&vr3, &id, Role::Guest, AT, t).err(), Some(IntakeError::NotPending(Outcome::Stale)));
    assert_eq!(i.receive(&vr3, &v[1].key_id(), &by(&proposal(&v[1], &r3, &v[5], Role::Guest, 2)), t).err(), Some(IntakeError::NoFreeSeat));
    // another session's roster, same starter
    let other = world(&v, session(208), 2, 0);
    let vro = view(&v[0], &v[0], &other[1]);
    let r4 = next_with_cap(&vr3, CAP).map(|b| sign(&v[0], b).unwrap()).unwrap();
    let vr4 = view(&v[0], &v[0], &r4);
    let id2 = i.receive(&vr4, &v[2].key_id(), &by(&proposal(&v[2], &r4, &v[6], Role::Guest, 3)), t).unwrap();
    let acc = i.accounting();
    assert_eq!(i.approve(&vro, &id2, Role::Guest, AT, t).err(), Some(IntakeError::WrongRoster));
    assert_eq!(i.accounting(), acc);
    assert_eq!(i.outcome(&id2), Some(Outcome::Pending));
    // time backwards: approve at t - 900 s
    let body = i.approve(&vr4, &id2, Role::Guest, AT, t - Duration::from_secs(900)).unwrap();
    assert_valid(&v[0], &r4, body, "time backwards");
}

/// Candidate variants: equal to another PENDING candidate (whole, or its signing key), to the
/// proposer, to the starter, the starter's Noise key, a removed member's signing key; added_at
/// extremes; role combinations.
#[test]
fn r2_f2_candidate_variants() {
    let v = ids(12);
    let s = session(209);
    let r = world(&v, s, 3, 0); // P=v1 Q=v2 G=v3
    let r3 = next(&v[0], &r[1], |b| remove(b, &v[3])); // G removed
    let t = t0();
    // same candidate proposed by P and Q
    let (vr, mut i) = intake(&v[0], &r3);
    let a = i.receive(&vr, &v[1].key_id(), &by(&proposal(&v[1], &r3, &v[6], Role::Guest, 1)), t).unwrap();
    let b = i.receive(&vr, &v[2].key_id(), &by(&proposal(&v[2], &r3, &v[6], Role::Guest, 2)), t).unwrap();
    let ap = i.approve_with_report(&vr, &a, Role::Guest, AT, t).unwrap();
    assert_eq!(ap.made_stale, vec![(b, v[2].key_id())]);
    assert_valid(&v[0], &r3, ap.body, "same candidate twice");
    // pending candidate's signing key with a fresh Noise key
    let (vr, mut i) = intake(&v[0], &r3);
    let a = i.receive(&vr, &v[1].key_id(), &by(&proposal(&v[1], &r3, &v[6], Role::Guest, 1)), t).unwrap();
    let tw = twin(&v[6], &v[7]);
    let b = i.receive(&vr, &v[2].key_id(), &by(&proposal(&v[2], &r3, &tw, Role::Guest, 2)), t).unwrap();
    let ap = i.approve_with_report(&vr, &b, Role::Guest, AT, t).unwrap();
    assert_eq!(ap.made_stale, vec![(a, v[1].key_id())]);
    assert_valid(&v[0], &r3, ap.body, "pending twin");
    // proposer itself, starter, starter's Noise key, both keys of Q
    let (vr, mut i) = intake(&v[0], &r3);
    let acc = i.accounting();
    for (cand, want) in [
        (twin(&v[1], &v[1]), IntakeError::CandidateIsMember),
        (twin(&v[0], &v[0]), IntakeError::CandidateIsMember),
        (twin(&v[8], &v[0]), IntakeError::CandidateNoiseKeyInUse),
        (twin(&v[0], &v[8]), IntakeError::CandidateSignKeyInUse),
        (twin(&v[2], &v[2]), IntakeError::CandidateIsMember),
        (twin(&v[3], &v[3]), IntakeError::CandidateRemoved),
    ] {
        let got = i.receive(&vr, &v[1].key_id(), &by(&proposal(&v[1], &r3, &cand, Role::Guest, 9)), t);
        assert_eq!(got.err(), Some(want));
        assert_eq!(i.accounting(), acc);
    }
    // removed member's signing key with a fresh Noise key: accepted and valid (DQ3, as ruled)
    let id = i.receive(&vr, &v[1].key_id(), &by(&proposal(&v[1], &r3, &twin(&v[3], &v[9]), Role::Guest, 9)), t).unwrap();
    let body = i.approve(&vr, &id, Role::Guest, "", t).unwrap(); // empty added_at
    assert_valid(&v[0], &r3, body, "removed sign key, empty added_at");
    // added_at of exactly 64 bytes in multi-byte characters; 65 bytes refused, proposal stays
    let (vr, mut i) = intake(&v[0], &r3);
    let id = i.receive(&vr, &v[1].key_id(), &by(&proposal(&v[1], &r3, &v[10], Role::Observer, 1)), t).unwrap();
    let e65 = format!("{}a", "\u{1F600}".repeat(16));
    assert_eq!(e65.len(), 65);
    assert_eq!(i.approve(&vr, &id, Role::Observer, &e65, t).err(), Some(IntakeError::FieldLimit));
    assert_eq!(i.approve(&vr, &id, Role::Guest, AT, t).err(), Some(IntakeError::RoleRaised));
    assert_eq!(i.outcome(&id), Some(Outcome::Pending));
    let body = i.approve(&vr, &id, Role::Observer, &"\u{1F600}".repeat(16), t).unwrap();
    assert_valid(&v[0], &r3, body, "64-byte multibyte added_at, observer");
}

// ------------------------------------------------------------------------------------------------
// F3 re-attack: the crowded-out counter
// ------------------------------------------------------------------------------------------------

#[test]
fn r2_f3_counter_who_can_move_it() {
    let v = ids(12);
    let s = session(210);
    let r = world_at(&v, s, CAP, 5); // v1..v5 guests
    let (vr, mut i) = intake(&v[0], &r[1]);
    let t = t0();
    // H1 uses its quota on declines, then is muted
    let mut n = 1u8;
    for k in 0..8 {
        let id = i.receive(&vr, &v[1].key_id(), &by(&proposal(&v[1], &r[1], &v[7], Role::Guest, n)), t).unwrap();
        if k < 7 { i.decline(&vr, &id, t).unwrap() } else { i.decline_and_mute(&vr, &id, t).unwrap() }
        n += 1;
    }
    // three others fill the session slots
    for (k, g) in [2usize, 3, 4].iter().enumerate() {
        i.receive(&vr, &v[*g].key_id(), &by(&proposal(&v[*g], &r[1], &v[8 + k], Role::Guest, 100 + k as u8)), t).unwrap();
    }
    // the muted, quota-exhausted H1 still has its counter moved by SessionPendingFull
    let acc = i.accounting();
    for k in 0..5u8 {
        assert_eq!(i.receive(&vr, &v[1].key_id(), &by(&proposal(&v[1], &r[1], &v[7], Role::Guest, 150 + k)), t).err(), Some(IntakeError::SessionPendingFull));
    }
    println!("R2 F3 muted+quota-used guest's crowded counter: {}", i.crowded_out(&v[1].key_id()));
    assert_eq!(i.crowded_out(&v[1].key_id()), 5);
    // `accounting()` (the intake's 'everything it stores') does not see the counter
    assert_eq!(i.accounting(), acc, "accounting changed");
    println!("R2 F3 accounting unchanged while the counter moved: {:?}", i.accounting());
    // a guest cannot move another guest's counter: proposer field != sender
    let forged = proposal(&v[5], &r[1], &v[7], Role::Guest, 200);
    assert_eq!(i.receive(&vr, &v[1].key_id(), &by(&forged), t).err(), Some(IntakeError::ProposerNotSender));
    assert_eq!(i.crowded_out(&v[5].key_id()), 0);
    // an invalid proposal (bad signature) while full is not counted
    let mut bad = proposal(&v[5], &r[1], &v[7], Role::Guest, 201);
    bad.sig = junk_sig();
    assert_eq!(i.receive(&vr, &v[5].key_id(), &by(&bad), t).err(), Some(IntakeError::BadSignature));
    assert_eq!(i.crowded_out(&v[5].key_id()), 0);
    // honest v5 counted once
    assert_eq!(i.receive(&vr, &v[5].key_id(), &by(&proposal(&v[5], &r[1], &v[7], Role::Guest, 202)), t).err(), Some(IntakeError::SessionPendingFull));
    assert_eq!(i.crowded_out_counts(), vec![(v[1].key_id(), 5), (v[5].key_id(), 1)]);
    // demoting v1 to observer drops its counter at the next tick
    let r3 = next(&v[0], &r[1], |b| set_role(b, &v[1], Role::Observer));
    let vr3 = view(&v[0], &v[0], &r3);
    i.tick(&vr3, t);
    assert_eq!(i.crowded_out_counts(), vec![(v[5].key_id(), 1)]);
    // the counter is u32 and saturates (REASONED: `saturating_add`)
}

// ------------------------------------------------------------------------------------------------
// F4 re-attack: wire form
// ------------------------------------------------------------------------------------------------

#[test]
fn r2_f4_wire_spellings() {
    let v = ids(8);
    let r = world(&v, session(211), 3, 0);
    let p = proposal(&v[1], &r[1], &v[5], Role::Guest, 1);
    let w = p.to_wire().unwrap();
    assert!(w.bytes().all(|c| matches!(c, b'0'..=b'9' | b'a'..=b'f')));
    let (vr, mut i) = intake(&v[0], &r[1]);
    let k = v[1].key_id();
    let t = t0();
    let mut bad: Vec<(String, IntakeError)> = vec![
        (format!(" {w}"), IntakeError::Malformed),
        (format!("{w}\n"), IntakeError::Malformed),
        (format!("0x{w}"), IntakeError::Malformed),
        (String::new(), IntakeError::Malformed),
        (format!("{w}00"), IntakeError::Malformed), // canonical decode refuses trailing bytes
        ("0".repeat(2 * MAX_PROPOSAL_BYTES), IntakeError::Malformed), // at the bound: decoded, junk
        ("0".repeat(2 * MAX_PROPOSAL_BYTES + 1), IntakeError::TooLarge),
        ("\u{e9}".repeat(10), IntakeError::Malformed),
    ];
    // every single letter switched to upper case
    for (pos, ch) in w.char_indices().filter(|(_, c)| c.is_ascii_lowercase()).take(40) {
        let mut s = w.clone();
        s.replace_range(pos..pos + 1, &ch.to_ascii_uppercase().to_string());
        bad.push((s, IntakeError::Malformed));
    }
    let acc = i.accounting();
    for (s, want) in &bad {
        assert_eq!(i.receive_wire(&vr, &k, s, t).err().as_ref(), Some(want), "spelling {:?}", &s[..s.len().min(12)]);
        assert_eq!(i.accounting(), acc);
    }
    println!("R2 F4 refused spellings: {}", bad.len());
    let id = i.receive_wire(&vr, &k, &w, t).unwrap();
    assert_eq!(i.pending_proposal(&id), Some(&p));
}

// ------------------------------------------------------------------------------------------------
// F5 re-attack: what an approval made stale; expiries swallowed by the internal tick
// ------------------------------------------------------------------------------------------------

#[test]
fn r2_f5_made_stale_edges() {
    let v = ids(10);
    let r = world(&v, session(212), 3, 0);
    let t = t0();
    // nothing else pending: empty
    let (vr, mut i) = intake(&v[0], &r[1]);
    let a = i.receive(&vr, &v[1].key_id(), &by(&proposal(&v[1], &r[1], &v[5], Role::Guest, 1)), t).unwrap();
    assert!(i.approve_with_report(&vr, &a, Role::Guest, AT, t).unwrap().made_stale.is_empty());
    // refused approval: nothing staled; declined and expired proposals are not listed
    let (vr, mut i) = intake(&v[0], &r[1]);
    let a = i.receive(&vr, &v[1].key_id(), &by(&proposal(&v[1], &r[1], &v[5], Role::Observer, 1)), t).unwrap();
    let b = i.receive(&vr, &v[2].key_id(), &by(&proposal(&v[2], &r[1], &v[6], Role::Guest, 2)), t).unwrap();
    assert_eq!(i.approve_with_report(&vr, &a, Role::Guest, AT, t).err(), Some(IntakeError::RoleRaised));
    assert_eq!(i.outcome(&b), Some(Outcome::Pending));
    i.decline(&vr, &b, t).unwrap();
    let c = i.receive(&vr, &v[3].key_id(), &by(&proposal(&v[3], &r[1], &v[7], Role::Guest, 3)), t).unwrap();
    let ap = i.approve_with_report(&vr, &a, Role::Observer, AT, t).unwrap();
    assert_eq!(ap.made_stale, vec![(c, v[3].key_id())]);
}

/// A proposal whose time passes is ended by the `tick` that `approve`, `decline` and `receive`
/// run internally; that tick's report is discarded, the proposal is no longer pending, so neither
/// `made_stale` nor any later `tick` ever reports it.
#[test]
fn r2_f5_expiry_swallowed_by_an_internal_tick() {
    let v = ids(10);
    let r = world(&v, session(213), 3, 0);
    let t = t0();
    // via approve
    let (vr, mut i) = intake(&v[0], &r[1]);
    let a = i.receive(&vr, &v[1].key_id(), &by(&proposal(&v[1], &r[1], &v[5], Role::Guest, 1)), t).unwrap();
    let b = i.receive(&vr, &v[2].key_id(), &by(&proposal(&v[2], &r[1], &v[6], Role::Guest, 2)), t + Duration::from_secs(300)).unwrap();
    let ap = i.approve_with_report(&vr, &b, Role::Guest, AT, t + PROPOSAL_TTL).unwrap();
    let later = i.tick(&vr, t + PROPOSAL_TTL + Duration::from_secs(1));
    println!("R2 F5 approve: outcome(a)={:?} made_stale={:?} later tick={:?}", i.outcome(&a), ap.made_stale, later);
    assert_eq!(i.outcome(&a), Some(Outcome::Expired));
    assert!(ap.made_stale.is_empty() && later.is_empty(), "the expiry of a was reported somewhere");
    // via receive of junk from any guest
    let (vr, mut i) = intake(&v[0], &r[1]);
    let a = i.receive(&vr, &v[1].key_id(), &by(&proposal(&v[1], &r[1], &v[5], Role::Guest, 1)), t).unwrap();
    let _ = i.receive(&vr, &v[3].key_id(), b"junk", t + PROPOSAL_TTL);
    let later = i.tick(&vr, t + PROPOSAL_TTL + Duration::from_secs(1));
    println!("R2 F5 junk receive: outcome(a)={:?} later tick={:?}", i.outcome(&a), later);
    assert_eq!(i.outcome(&a), Some(Outcome::Expired));
    assert!(later.is_empty());
}
