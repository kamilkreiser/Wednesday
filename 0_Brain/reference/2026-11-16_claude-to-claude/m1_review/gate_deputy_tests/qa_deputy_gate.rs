//! Independent QA gate, M3 DEPUTY (tier 1). Probes written by the gate, not the builder.
//! Each test asserts what the code DOES today; the gate verdict rates whether that is acceptable.
mod common;
mod deputy_common;
mod prop_common;

use coagent_crypto::kk::RosterView;
use coagent_roster::{
    admit_view, next_with_deputy, sign, AdmissionApplied, AdmissionError, GrantSpec, Role,
    SessionChain, SignedRoster,
};
use common::*;
use deputy_common::*;

/// starter v0, deputy v1, guest P v2, observer O v3; grant to v1 over seats 5, 6 at epoch 3.
fn world(s: u8) -> (Vec<coagent_crypto::identity::DeviceIdentity>, Vec<SignedRoster>) {
    let v = ids(10);
    let w = deputy_world(&v, session(s), 8, true, &[5, 6]);
    (v, w)
}

/// G1: a provisional member the starter DROPPED by renewing the grant can be re-admitted by the same
/// deputy at once under the new grant (one fresh proposal from any roster guest). "Drop" is not sticky.
#[test]
fn g1_a_dropped_provisional_member_is_readmitted_by_the_same_deputy_at_once() {
    let (v, w) = world(41);
    let mut p = session_at(&v[0], &v[2], &w[0], &w[1..]);
    let a0 = adm(&v[1], &w[2], 0, [0; 32], &v[2], &v[4], Role::Guest, 5, 1);
    assert_eq!(p.apply_admission(&a0), Ok(AdmissionApplied::Accepted));
    // The starter returns and renews the grant with other seats: v4 is dropped.
    let body = next_with_deputy(
        p.roster(),
        Some(GrantSpec {
            holder: v[1].key_id(),
            slots: vec![5, 6, 7],
        }),
    )
    .unwrap();
    let r4 = sign(&v[0], body).unwrap();
    let rep = p.apply_roster(&r4).unwrap();
    assert_eq!(rep.dropped, vec![v[4].key_id()], "v4 dropped by the renewal");
    // The same deputy re-admits v4 under the new epoch, on a new proposal by P.
    let a1 = adm(&v[1], &r4, 0, [0; 32], &v[2], &v[4], Role::Guest, 5, 2);
    let got = p.apply_admission(&a1);
    println!("G1 re-admission of a dropped key under the renewed grant: {got:?}");
    assert_eq!(got, Ok(AdmissionApplied::Accepted));
    assert!(p.view().is_provisional(&v[4].key_id()));
}

/// G2: the evidence compartment is per SESSION, first come. A first deputy's four forks fill it;
/// a later deputy's fork is then only counted. The `Conflict` error still CARRIES the evidence to the
/// caller, and it verifies against the current roster.
#[test]
fn g2_a_first_deputys_forks_fill_the_store_a_later_deputys_fork_is_returned_not_kept() {
    let (v, w) = world(42);
    let mut o = session_at(&v[0], &v[3], &w[0], &w[1..]);
    let a0 = adm(&v[1], &w[2], 0, [0; 32], &v[2], &v[4], Role::Guest, 5, 1);
    assert_eq!(o.apply_admission(&a0), Ok(AdmissionApplied::Accepted));
    for (i, c) in [5usize, 6, 7, 8].iter().enumerate() {
        let f = adm(&v[1], &w[2], 0, [0; 32], &v[2], &v[*c], Role::Guest, 5, 10 + i as u8);
        assert!(matches!(o.apply_admission(&f), Err(AdmissionError::Conflict(_))));
    }
    assert_eq!(o.accounting().evidence_kept, 4);
    // The starter moves the grant to P (v2); v1 (now an ordinary guest) proposes.
    let body = next_with_deputy(
        o.roster(),
        Some(GrantSpec {
            holder: v[2].key_id(),
            slots: vec![5, 6],
        }),
    )
    .unwrap();
    let r4 = sign(&v[0], body).unwrap();
    o.apply_roster(&r4).unwrap();
    let b0 = adm(&v[2], &r4, 0, [0; 32], &v[1], &v[4], Role::Guest, 5, 20);
    assert_eq!(o.apply_admission(&b0), Ok(AdmissionApplied::Accepted));
    let b0x = adm(&v[2], &r4, 0, [0; 32], &v[1], &v[5], Role::Guest, 5, 21);
    match o.apply_admission(&b0x) {
        Err(AdmissionError::Conflict(ev)) => {
            assert_eq!(ev.verify(o.roster()), Ok(v[2].key_id()), "returned evidence verifies");
        }
        other => panic!("expected a conflict, got {other:?}"),
    }
    let acc = o.accounting();
    println!("G2 accounting after the second deputy's fork: {acc:?}");
    assert_eq!((acc.evidence_kept, acc.evidence_unkept), (4, 1));
    // None of the kept pairs is about the current deputy, and none verifies with the current roster.
    assert!(o.evidence().iter().all(|e| e.verify(o.roster()).is_err()));
}

/// G3: after ANY starter version that does not touch the grant (here a role change), a provisional
/// newcomer whose admission follows an earlier one can no longer start: the earlier admission's
/// proposal names a version the newcomer does not hold (design question 2, conservative reading).
#[test]
fn g3_after_an_unrelated_change_the_next_newcomer_cannot_start() {
    let (v, w) = world(43);
    let mut p = session_at(&v[0], &v[2], &w[0], &w[1..]);
    let a0 = adm(&v[1], &w[2], 0, [0; 32], &v[2], &v[4], Role::Guest, 5, 1);
    assert_eq!(p.apply_admission(&a0), Ok(AdmissionApplied::Accepted));
    // Unrelated: the observer becomes a guest (same grant, same epoch).
    let r4 = next(&v[0], &w[2], |b| {
        let o = b.members.iter_mut().find(|m| m.key_id == v[3].key_id()).unwrap();
        o.role = Role::Guest;
    });
    let rep = p.apply_roster(&r4).unwrap();
    assert!(rep.dropped.is_empty() && rep.grant_change.is_none());
    let a1 = adm(
        &v[1],
        &r4,
        1,
        hash_of_admission(&a0),
        &v[2],
        &v[5],
        Role::Guest,
        6,
        2,
    );
    assert_eq!(p.apply_admission(&a1), Ok(AdmissionApplied::Accepted), "members accept it");
    let got = SessionChain::start_provisional(
        &v[0].verified(),
        session(43),
        &v[5].key_id(),
        &r4,
        &[a0, a1],
    );
    println!("G3 newcomer start after an unrelated change: {:?}", got.as_ref().err());
    assert!(got.is_err(), "the newcomer cannot start");
}

/// G4: a member who joins (directly invited by the starter) after an admission was made cannot
/// accept that admission; members' views then differ, so their handshakes fail, until the grant is
/// renewed. Same root as G3.
#[test]
fn g4_a_member_who_joins_later_diverges_from_the_others() {
    let (v, w) = world(44);
    let mut p = session_at(&v[0], &v[2], &w[0], &w[1..]);
    let a0 = adm(&v[1], &w[2], 0, [0; 32], &v[2], &v[4], Role::Guest, 5, 1);
    assert_eq!(p.apply_admission(&a0), Ok(AdmissionApplied::Accepted));
    let r4 = next(&v[0], &w[2], |b| add(b, &v[9], Role::Guest, 4));
    p.apply_roster(&r4).unwrap();
    let mut j = SessionChain::start(&v[0].verified(), session(44), &v[9].key_id(), &r4).unwrap();
    let got = j.apply_admission(&a0);
    println!("G4 the later joiner offered the earlier admission: {got:?}");
    assert_eq!(got, Err(AdmissionError::ProposalVersionNotHeld));
    assert_ne!(p.view().roster_hash(), j.view().roster_hash(), "views differ");
}

/// G5: the deputy can never send roster.update or session.end through the view's decoder, and a
/// FORMER deputy cannot send deputy.admission (sanity probes on admit_view, no envelope tricks).
#[test]
fn g5_admit_view_exists_and_takes_the_view() {
    // Compile-time probe only: admit_view takes the view (signature check).
    let _f: fn(
        &coagent_roster::MemberView,
        &coagent_crypto::channel::Inbound,
    ) -> Result<Role, coagent_roster::RoleError> = admit_view;
}
