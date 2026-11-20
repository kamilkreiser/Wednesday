//! Independent check of ROSTER-SETTLE (gate). Probes of the checker's own, not the builder's tests.
//! Item numbers follow the gate brief's attack list (8a-8g).
mod common;
mod deputy_common;
mod prop_common;

use coagent_crypto::identity::DeviceIdentity;
use coagent_proto::bytes::KeyId;
use coagent_roster::{
    next_plain, settle, sign, AdmissionApplied, AdmissionError, AdmissionEvidence, DeputyGrant,
    EvidenceError, IntakeError, MemberView, Outcome, ProvisionalStartError, Removed, Role,
    RosterBody, RosterError, SessionChain, SignedAdmission, SignedRoster,
};
use coagent_crypto::kk::RosterView;
use common::*;
use deputy_common::*;
use prop_common::{fake_removed, first_roster, intake, proposal, t0, AT};

fn world(s: u8) -> (Vec<DeviceIdentity>, Vec<SignedRoster>) {
    let v = ids(14);
    let w = deputy_world(&v, session(s), 8, true, &[5, 6]);
    (v, w)
}

fn dropped(b: &RosterBody) -> Vec<KeyId> {
    b.members
        .iter()
        .find(|m| m.key_id == b.convener)
        .and_then(|m| m.dropped_keys.clone())
        .unwrap_or_default()
}

fn with_epoch(r: &SignedRoster, starter: &DeviceIdentity, epoch: u64) -> SignedRoster {
    let mut b = r.body.clone();
    for m in b.members.iter_mut() {
        if let Some(g) = m.deputy.as_mut() {
            g.epoch = epoch;
        }
    }
    sign(starter, b).unwrap()
}

/// The change kinds the starter may make, each applied to a plain next body.
fn change(kind: usize, v: &[DeviceIdentity], b: &mut RosterBody) -> &'static str {
    match kind {
        0 => "nothing",
        1 => {
            b.members.iter_mut().find(|m| m.key_id == v[3].key_id()).unwrap().role = Role::Guest;
            "role"
        }
        2 => {
            add(b, &v[13], Role::Guest, 4);
            "invite"
        }
        3 => {
            remove(b, &v[3]);
            "remove"
        }
        4 => {
            // grant moved to P (v2); settle rewrites the epoch.
            no_grant(b);
            b.members.iter_mut().find(|m| m.key_id == v[2].key_id()).unwrap().deputy =
                Some(DeputyGrant { epoch: 0, slots: vec![5, 6, 7] });
            "grant moved"
        }
        5 => {
            no_grant(b);
            "grant withdrawn"
        }
        _ => {
            // grant changed (same holder, more seats).
            b.members.iter_mut().find(|m| m.key_id == v[1].key_id()).unwrap().deputy =
                Some(DeputyGrant { epoch: 3, slots: vec![5, 6, 7] });
            "grant changed"
        }
    }
}

// 8a: G3/G4 re-expressed, for every change kind and three keep choices.
#[test]
fn qa_8a_after_every_starter_change_newcomer_starts_joiner_agrees_old_admission_refused() {
    for kind in 0..7 {
        for keep_mode in 0..3 {
            let (v, w) = world(70 + kind as u8);
            let mut st = session_at(&v[0], &v[0], &w[0], &w[1..]);
            let mut p = session_at(&v[0], &v[2], &w[0], &w[1..]);
            let mut o = session_at(&v[0], &v[3], &w[0], &w[1..]);
            let a0 = adm(&v[1], &w[2], 0, [0; 32], &v[2], &v[4], Role::Guest, 5, 1);
            for c in [&mut st, &mut p, &mut o] {
                assert_eq!(c.apply_admission(&a0), Ok(AdmissionApplied::Accepted));
            }
            let mut b = next_plain(st.roster()).unwrap();
            let name = change(kind, &v, &mut b);
            let k4 = [v[4].key_id()];
            let keep: Option<&[KeyId]> = match keep_mode {
                0 => None,
                1 => Some(&k4),
                _ => Some(&[]),
            };
            let body = settle(st.view(), b, keep)
                .unwrap_or_else(|e| panic!("{name}/{keep_mode}: settle refused: {e:?}"));
            let r4 = sign(&v[0], body).unwrap();
            st.apply_roster(&r4).unwrap();
            p.apply_roster(&r4).unwrap();
            let o_alive = o.apply_roster(&r4).is_ok();
            for c in [&st, &p] {
                assert!(c.view().provisional_keys().is_empty(), "{name}: provisional stood");
            }
            // A joiner of r4 (every listed member other than the starter that we hold an id for).
            let joiner = if kind == 2 { Some(&v[13]) } else if keep_mode != 2 { Some(&v[4]) } else { None };
            if let Some(jd) = joiner {
                let mut j = SessionChain::start(&v[0].verified(), session(70 + kind as u8), &jd.key_id(), &r4)
                    .unwrap_or_else(|e| panic!("{name}/{keep_mode}: joiner could not start: {e:?}"));
                assert_eq!(j.view().roster_hash(), p.view().roster_hash(), "{name}: joiner view differs");
                let got = j.apply_admission(&a0);
                assert!(got.is_err(), "{name}: joiner took the old admission");
            }
            // Old admission offered again to old members.
            let got = p.apply_admission(&a0);
            assert!(got.is_err(), "{name}/{keep_mode}: old member took the old admission again");
            if let Some((h, g)) = r4.body.members.iter().find_map(|m| m.deputy.clone().map(|g| (m.key_id, g))) {
                assert_eq!(g.epoch, 4, "{name}: epoch not the version's number");
                assert!(matches!(got, Err(AdmissionError::WrongEpoch { held: 4, got: 3 })), "{name}: {got:?}");
                // The next newcomer: an admission by the (possibly new) holder, against r4.
                let hd = v.iter().find(|d| d.key_id() == h).unwrap();
                let proposer = if h == v[2].key_id() { &v[1] } else { &v[2] };
                let free = p.view().free_set_aside_seats();
                let seat = free[0];
                let a1 = adm(hd, &r4, 0, [0; 32], proposer, &v[12], Role::Guest, seat, 9);
                assert_eq!(p.apply_admission(&a1), Ok(AdmissionApplied::Accepted), "{name}/{keep_mode}");
                assert_eq!(st.apply_admission(&a1), Ok(AdmissionApplied::Accepted));
                let k = SessionChain::start_provisional(&v[0].verified(), session(70 + kind as u8), &v[12].key_id(), &r4, std::slice::from_ref(&a1))
                    .unwrap_or_else(|e| panic!("{name}/{keep_mode}: newcomer could not start: {e:?}"));
                assert_eq!(k.view().roster_hash(), p.view().roster_hash(), "{name}: newcomer view differs");
                if o_alive {
                    assert_eq!(o.apply_admission(&a1), Ok(AdmissionApplied::Accepted));
                    assert_eq!(o.view().roster_hash(), p.view().roster_hash());
                }
            } else {
                assert!(matches!(got, Err(AdmissionError::NoGrant)), "{name}: {got:?}");
            }
        }
    }
}

// 8b: a grant with any epoch but its own number, at a member mid-session, a joiner's first list,
// and start_provisional.
#[test]
fn qa_8b_any_epoch_but_the_versions_own_is_refused_everywhere() {
    let (v, w) = world(80);
    let good = sign(&v[0], settle(&MemberView::of_roster(&session_at(&v[0], &v[0], &w[0], &w[1..]).roster().clone()),
        next_plain(session_at(&v[0], &v[0], &w[0], &w[1..]).roster()).unwrap(), None).unwrap()).unwrap();
    assert_eq!(epoch_of(&good), 4);
    for e in [0u64, 1, 2, 3, 5, 6, 255, 256, u64::MAX - 1, u64::MAX] {
        let bad = with_epoch(&good, &v[0], e);
        let want_kind = if e == 0 || e > 4 { "range" } else { "notnew" };
        let check = |got: &RosterError| match want_kind {
            "range" => matches!(got, RosterError::GrantEpochOutOfRange(_)),
            _ => matches!(got, RosterError::GrantEpochNotNew(_)),
        };
        let mut p = session_at(&v[0], &v[2], &w[0], &w[1..]);
        let a0 = adm(&v[1], &w[2], 0, [0; 32], &v[2], &v[4], Role::Guest, 5, 1);
        p.apply_admission(&a0).unwrap();
        let before = snap(&p);
        let got = p.apply_roster(&bad).map(|_| ()).unwrap_err();
        assert!(check(&got), "epoch {e} mid-session: {got:?}");
        assert_eq!(snap(&p), before, "epoch {e}: refused version changed state");
        let got = SessionChain::start(&v[0].verified(), session(80), &v[3].key_id(), &bad).err().unwrap();
        assert!(check(&got), "epoch {e} joiner: {got:?}");
        let mut ab = admission_body(&bad, e, 0, [0; 32], &v[2], &v[5], Role::Guest, 6, 2);
        ab.epoch = e;
        let a = signed(&v[1], ab);
        match SessionChain::start_provisional(&v[0].verified(), session(80), &v[5].key_id(), &bad, &[a]) {
            Err(ProvisionalStartError::Roster(got)) => assert!(check(&got), "epoch {e} newcomer: {got:?}"),
            other => panic!("epoch {e} newcomer: {other:?}"),
        }
    }
    // A joiner's FIRST list at a high version: epoch = version - 1 refused, = version accepted.
    for (ver, e, ok) in [(200u64, 199u64, false), (200, 200, true), (256, 255, false), (256, 256, true), (256, 1, false)] {
        let mut ms = vec![member(&v[0], Role::Guest, 0, 1), member(&v[1], Role::Guest, 1, 1), member(&v[2], Role::Guest, 2, 1)];
        ms[1].deputy = Some(DeputyGrant { epoch: e, slots: vec![5] });
        let r = first_roster(&v[0], session(81), ver, ms, vec![]);
        let got = SessionChain::start(&v[0].verified(), session(81), &v[2].key_id(), &r);
        assert_eq!(got.is_ok(), ok, "first list at {ver} with epoch {e}: {:?}", got.err());
        if !ok {
            assert!(matches!(got.err(), Some(RosterError::GrantEpochNotNew(_))));
        }
    }
}

// 8c: an admission in flight across a starter version, both orders, held/not held; replay; a new
// chain continuing the old head.
#[test]
fn qa_8c_in_flight_both_orders_and_replay() {
    let (v, w) = world(82);
    let mut st = session_at(&v[0], &v[0], &w[0], &w[1..]);
    let mut p = session_at(&v[0], &v[2], &w[0], &w[1..]); // gets a1 BEFORE r4
    let mut o = session_at(&v[0], &v[3], &w[0], &w[1..]); // gets a1 AFTER r4
    let a0 = adm(&v[1], &w[2], 0, [0; 32], &v[2], &v[4], Role::Guest, 5, 1);
    let a1 = adm(&v[1], &w[2], 1, hash_of_admission(&a0), &v[2], &v[5], Role::Guest, 6, 2);
    for c in [&mut st, &mut p, &mut o] {
        c.apply_admission(&a0).unwrap();
    }
    p.apply_admission(&a1).unwrap();
    let r4 = sign(&v[0], settle(st.view(), next_plain(st.roster()).unwrap(), Some(&[])).unwrap()).unwrap();
    assert_eq!(dropped(&r4.body), vec![v[4].key_id()], "only the seen one recorded");
    let rp = p.apply_roster(&r4).unwrap();
    let mut want = vec![v[4].key_id(), v[5].key_id()];
    want.sort();
    let mut got = rp.dropped.clone();
    got.sort();
    assert_eq!(got, want);
    o.apply_roster(&r4).unwrap();
    st.apply_roster(&r4).unwrap();
    assert_eq!(o.apply_admission(&a1), Err(AdmissionError::WrongEpoch { held: 4, got: 3 }));
    for c in [&mut st, &mut p, &mut o] {
        for a in [&a0, &a1] {
            assert_eq!(c.apply_admission(a), Err(AdmissionError::WrongEpoch { held: 4, got: 3 }));
        }
    }
    assert_eq!(p.view().roster_hash(), o.view().roster_hash());
    assert_eq!(p.view().roster_hash(), st.view().roster_hash());
    // New epoch, seq 0, but prev = the old head: refused.
    let mut b = admission_body(&r4, 4, 0, hash_of_admission(&a1), &v[2], &v[6], Role::Guest, 6, 3);
    b.epoch = 4;
    assert_eq!(p.apply_admission(&signed(&v[1], b)), Err(AdmissionError::BadPrev));
    // New epoch continuing old seq (2): refused SeqGap.
    let b = admission_body(&r4, 4, 2, hash_of_admission(&a1), &v[2], &v[6], Role::Guest, 6, 4);
    assert!(matches!(p.apply_admission(&signed(&v[1], b)), Err(AdmissionError::SeqGap { .. })));
    // v5 (never seen by the starter) is admissible again; v4 (dropped) is not.
    let again5 = adm(&v[1], &r4, 0, [0; 32], &v[2], &v[5], Role::Guest, 6, 5);
    let again4 = adm(&v[1], &r4, 0, [0; 32], &v[2], &v[4], Role::Guest, 5, 6);
    assert_eq!(o.apply_admission(&again4), Err(AdmissionError::CandidateDropped));
    assert_eq!(o.apply_admission(&again5), Ok(AdmissionApplied::Accepted));
}

// 8d: dropping is lasting: same deputy, later deputy, withdraw + re-grant; starter can add.
#[test]
fn qa_8d_dropping_is_lasting_through_withdraw_and_regrant() {
    let (v, w) = world(84);
    let mut st = session_at(&v[0], &v[0], &w[0], &w[1..]);
    let a0 = adm(&v[1], &w[2], 0, [0; 32], &v[2], &v[4], Role::Guest, 5, 1);
    st.apply_admission(&a0).unwrap();
    let r4 = sign(&v[0], settle(st.view(), next_plain(st.roster()).unwrap(), Some(&[])).unwrap()).unwrap();
    st.apply_roster(&r4).unwrap();
    assert_eq!(st.apply_admission(&adm(&v[1], &r4, 0, [0; 32], &v[2], &v[4], Role::Guest, 5, 2)), Err(AdmissionError::CandidateDropped));
    // withdraw (v5)
    let mut b = next_plain(st.roster()).unwrap();
    no_grant(&mut b);
    let r5 = sign(&v[0], settle(st.view(), b, None).unwrap()).unwrap();
    st.apply_roster(&r5).unwrap();
    assert!(dropped(&r5.body).contains(&v[4].key_id()), "withdraw forgot the drop");
    // re-grant to the same holder (v6)
    let mut b = next_plain(st.roster()).unwrap();
    b.members.iter_mut().find(|m| m.key_id == v[1].key_id()).unwrap().deputy = Some(DeputyGrant { epoch: 0, slots: vec![5, 6] });
    let r6 = sign(&v[0], settle(st.view(), b, None).unwrap()).unwrap();
    st.apply_roster(&r6).unwrap();
    assert_eq!(epoch_of(&r6), 6);
    assert_eq!(st.apply_admission(&adm(&v[1], &r6, 0, [0; 32], &v[2], &v[4], Role::Guest, 5, 3)), Err(AdmissionError::CandidateDropped));
    // re-grant to another holder (v7)
    let mut b = next_plain(st.roster()).unwrap();
    no_grant(&mut b);
    b.members.iter_mut().find(|m| m.key_id == v[2].key_id()).unwrap().deputy = Some(DeputyGrant { epoch: 0, slots: vec![5] });
    let r7 = sign(&v[0], settle(st.view(), b, None).unwrap()).unwrap();
    st.apply_roster(&r7).unwrap();
    assert_eq!(st.apply_admission(&adm(&v[2], &r7, 0, [0; 32], &v[1], &v[4], Role::Guest, 5, 4)), Err(AdmissionError::CandidateDropped));
    // starter adds it himself (v8) into a free seat.
    let mut b = next_plain(st.roster()).unwrap();
    add(&mut b, &v[4], Role::Guest, 4);
    let r8 = sign(&v[0], settle(st.view(), b, None).unwrap()).unwrap();
    st.apply_roster(&r8).unwrap();
    assert_eq!(st.roster().role_of(&v[4].key_id()), Some(Role::Guest));
    // A joiner of r8 accepts the starter's re-add.
    SessionChain::start(&v[0].verified(), session(84), &v[4].key_id(), &r8).unwrap();
}

/// A first roster at `ver`: starter (0), holder v1 (1), `extra` guests from v2, a grant over
/// `seats` (epoch = ver), `dropped` fake dropped keys, `removed` fake removed ids, limit `cap`.
fn state(v: &[DeviceIdentity], s: u8, ver: u64, cap: u8, extra: usize, seats: &[u8], ndropped: u8, nremoved: u8) -> SessionChain {
    let mut ms = vec![member(&v[0], Role::Guest, 0, 1), member(&v[1], Role::Guest, 1, 1)];
    for i in 0..extra {
        ms.push(member(&v[2 + i], Role::Guest, 2 + i as u8, 1));
    }
    ms[1].deputy = Some(DeputyGrant { epoch: ver, slots: seats.to_vec() });
    if ndropped > 0 {
        ms[0].dropped_keys = Some((1..=ndropped).map(|i| KeyId([i; 32])).collect());
    }
    let removed: Vec<Removed> = (0..nremoved).map(|i| fake_removed(100 + i, 1)).collect();
    let mut b = first_roster(&v[0], session(s), ver, ms, removed).body;
    b.cap = cap;
    let r = sign(&v[0], b).unwrap();
    let mut st = SessionChain::start(&v[0].verified(), session(s), &v[0].key_id(), &r)
        .unwrap_or_else(|e| panic!("state at {ver}: {e:?}"));
    // Fill every seat with an admission (candidates v8..).
    let mut prev = [0u8; 32];
    for (i, seat) in seats.iter().enumerate() {
        let a = adm(&v[1], &r, i as u64, prev, &v[2], &v[8 + i], Role::Guest, *seat, 40 + i as u8);
        st.apply_admission(&a).unwrap_or_else(|e| panic!("fill seat {seat}: {e:?}"));
        prev = hash_of_admission(&a);
    }
    st
}

fn drop_all_withdraw(st: &SessionChain) -> Result<RosterBody, RosterError> {
    let mut b = next_plain(st.roster())?;
    no_grant(&mut b);
    settle(st.view(), b, Some(&[]))
}

// 8e: the starter is never stuck.
#[test]
fn qa_8e_drop_all_and_withdraw_is_always_accepted() {
    let v = ids(16);
    // 27 dropped + 5 seats (=32; starter, holder, proposer hold 3 seats), every seat admitted.
    let st = state(&v, 90, 10, 8, 1, &[3, 4, 5, 6, 7], 27, 0);
    assert_eq!(settle(st.view(), next_plain(st.roster()).unwrap(), Some(&[])), Err(RosterError::DroppedKeysNoRoom));
    let b = drop_all_withdraw(&st).expect("26+6 drop all & withdraw");
    assert_eq!(dropped(&b).len(), 32);
    // Lifetime bound reached: 3 members + 29 removed = 32, 5 seats admitted. Keep all refused; drop-all fine.
    let st = state(&v, 91, 10, 8, 1, &[3, 4, 5, 6, 7], 0, 29);
    assert_eq!(settle(st.view(), next_plain(st.roster()).unwrap(), None), Err(RosterError::LifetimeExceeded));
    drop_all_withdraw(&st).expect("lifetime full: drop all & withdraw");
    // Limit 4 full (starter, holder, P; seat 3 admitted).
    let st = state(&v, 92, 10, 4, 1, &[3], 0, 0);
    drop_all_withdraw(&st).expect("limit 4 full");
    settle(st.view(), next_plain(st.roster()).unwrap(), None).expect("limit 4 keep all");
    // Limit 8 full (starter, holder, 3 guests; seats 5-7 admitted).
    let st = state(&v, 93, 10, 8, 3, &[5, 6, 7], 0, 0);
    drop_all_withdraw(&st).expect("limit 8 full");
    // Version 255 -> 256 (the last version allowed).
    let st = state(&v, 94, 255, 8, 1, &[5, 6], 29, 0);
    let b = drop_all_withdraw(&st).expect("version 255");
    assert_eq!(b.version, 256);
    // Version 256: no next version at all (the session bound; not a settle matter).
    let st = state(&v, 95, 256, 8, 1, &[5, 6], 0, 0);
    let e = drop_all_withdraw(&st).unwrap_err();
    assert!(matches!(e, RosterError::TooManyVersions), "{e:?}");
}

// 8e (intake half): the starter's keep choice and a deputy's admission vs. approve_settling.
#[test]
fn qa_8e_intake_keep_choice_vs_proposal_cost() {
    // (i) one candidate, two approvers, keep all (the default): what happens to the proposal?
    let (v, w) = world(96);
    let mut st = session_at(&v[0], &v[0], &w[0], &w[1..]);
    st.apply_admission(&adm(&v[1], &w[2], 0, [0; 32], &v[2], &v[4], Role::Guest, 5, 1)).unwrap();
    let (vr, mut i) = intake(&v[0], &w[2]);
    let id = i.receive(&vr, &v[2].key_id(), &proposal(&v[2], &w[2], &v[4], Role::Guest, 7).encode().unwrap(), t0()).unwrap();
    let (vr2, mut i2) = intake(&v[0], &w[2]);
    let id2 = i2.receive(&vr2, &v[2].key_id(), &proposal(&v[2], &w[2], &v[4], Role::Guest, 7).encode().unwrap(), t0()).unwrap();
    let keep_all = i.approve_settling(st.view(), &id, Role::Guest, AT, t0(), None);
    println!("QA one candidate two approvers, keep all: {keep_all:?} outcome {:?}", i.outcome(&id));
    let drop_it = i2.approve_settling(st.view(), &id2, Role::Guest, AT, t0(), Some(&[]));
    println!("QA one candidate two approvers, drop: ok={} outcome {:?}", drop_it.is_ok(), i2.outcome(&id2));
    if let Ok(a) = &drop_it {
        // A member accepts it.
        let mut p = session_at(&v[0], &v[2], &w[0], &w[1..]);
        p.apply_admission(&adm(&v[1], &w[2], 0, [0; 32], &v[2], &v[4], Role::Guest, 5, 1)).unwrap();
        let r = sign(&v[0], a.body.clone()).unwrap();
        println!("QA drop+approve body at a member: {:?}", p.apply_roster(&r).map(|_| ()));
    }
    // (ii) lifetime: 2 members + 28 removed + P = 31 entries; 1 admitted; keep all -> 32; + proposed -> 33.
    let v = ids(16);
    let mut ms = vec![member(&v[0], Role::Guest, 0, 1), member(&v[1], Role::Guest, 1, 1), member(&v[2], Role::Guest, 2, 1)];
    ms[1].deputy = Some(DeputyGrant { epoch: 10, slots: vec![5] });
    let removed: Vec<Removed> = (0..28).map(|i| fake_removed(100 + i, 1)).collect();
    let r = first_roster(&v[0], session(97), 10, ms, removed);
    let mut st = SessionChain::start(&v[0].verified(), session(97), &v[0].key_id(), &r).unwrap();
    st.apply_admission(&adm(&v[1], &r, 0, [0; 32], &v[2], &v[8], Role::Guest, 5, 1)).unwrap();
    let (vr, mut i) = intake(&v[0], &r);
    let id = i.receive(&vr, &v[2].key_id(), &proposal(&v[2], &r, &v[9], Role::Guest, 7).encode().unwrap(), t0()).unwrap();
    let (vr2, mut i2) = intake(&v[0], &r);
    let id2 = i2.receive(&vr2, &v[2].key_id(), &proposal(&v[2], &r, &v[9], Role::Guest, 7).encode().unwrap(), t0()).unwrap();
    let keep_all = i.approve_settling(st.view(), &id, Role::Guest, AT, t0(), None);
    println!("QA lifetime, keep all: {keep_all:?} outcome {:?}", i.outcome(&id));
    let drop_it = i2.approve_settling(st.view(), &id2, Role::Guest, AT, t0(), Some(&[]));
    println!("QA lifetime, drop: ok={} outcome {:?}", drop_it.is_ok(), i2.outcome(&id2));
    let _ = (Outcome::Pending, IntakeError::GrantStands);
}

// 8f: the kept entry.
#[test]
fn qa_8f_kept_entry_role_seat_removed_and_never_admitted() {
    let (v, w) = world(98);
    let mut st = session_at(&v[0], &v[0], &w[0], &w[1..]);
    // v4 proposed as guest, admitted as OBSERVER (lower, allowed).
    let pr = proposal(&v[2], &w[2], &v[4], Role::Guest, 1);
    let a0 = signed(&v[1], admission_body_for(w[2].body.session_id, 3, 0, [0; 32], &pr, Role::Observer, 6));
    st.apply_admission(&a0).unwrap();
    let b = settle(st.view(), next_plain(st.roster()).unwrap(), None).unwrap();
    let e = b.members.iter().find(|m| m.key_id == v[4].key_id()).unwrap();
    assert_eq!((e.role, e.slot, e.added_in, e.proposal.is_none()), (Role::Observer, 6, 4, true));
    let g = b.members.iter().find_map(|m| m.deputy.clone()).unwrap();
    assert_eq!((g.epoch, g.slots), (4, vec![5]));
    // The caller's edit also puts the kept key on `removed`: refused (by the validator).
    let mut nb = next_plain(st.roster()).unwrap();
    nb.removed.push(Removed { key_id: v[4].key_id(), at_version: 4 });
    let got = settle(st.view(), nb, None);
    assert!(got.is_err(), "a kept key that is also on removed was accepted: {got:?}");
    println!("QA kept+removed: {got:?}");
    // The caller's edit invites the provisional key directly AND keeps it: refused (two entries).
    let mut nb = next_plain(st.roster()).unwrap();
    add(&mut nb, &v[4], Role::Guest, 4);
    let got = settle(st.view(), nb, None);
    assert!(got.is_err(), "a key both invited and kept was accepted: {got:?}");
    // Keep a key never admitted.
    assert_eq!(settle(st.view(), next_plain(st.roster()).unwrap(), Some(&[v[9].key_id()])), Err(RosterError::NotProvisional(v[9].key_id())));
    // Keep the same key twice: same as once.
    let k = [v[4].key_id(), v[4].key_id()];
    assert_eq!(settle(st.view(), next_plain(st.roster()).unwrap(), Some(&k)).unwrap(), b);
    // The caller lowers the limit to 4 with the kept person in seat 6: refused, not silently dropped.
    let mut nb = next_plain(st.roster()).unwrap();
    nb.cap = 4;
    no_grant(&mut nb);
    assert!(settle(st.view(), nb, None).is_err());
}

// 8g: two HONEST admissions of two epochs are never evidence.
#[test]
fn qa_8g_honest_admissions_of_two_epochs_are_not_evidence() {
    let (v, w) = world(99);
    let mut st = session_at(&v[0], &v[0], &w[0], &w[1..]);
    let a0 = adm(&v[1], &w[2], 0, [0; 32], &v[2], &v[4], Role::Guest, 5, 1);
    st.apply_admission(&a0).unwrap();
    let r4 = sign(&v[0], settle(st.view(), next_plain(st.roster()).unwrap(), Some(&[])).unwrap()).unwrap();
    st.apply_roster(&r4).unwrap();
    let b0 = adm(&v[1], &r4, 0, [0; 32], &v[2], &v[5], Role::Guest, 5, 2);
    assert_eq!(st.apply_admission(&b0), Ok(AdmissionApplied::Accepted));
    let vr3 = session_at(&v[0], &v[0], &w[0], &w[1..]).roster().clone();
    for (first, second) in [(&a0, &b0), (&b0, &a0)] {
        let ev = AdmissionEvidence { first: first.clone(), second: second.clone() };
        assert_eq!(ev.verify(&vr3), Err(EvidenceError::WrongEpoch));
        assert_eq!(ev.verify(st.roster()), Err(EvidenceError::WrongEpoch));
    }
    // A member holding b0 offered a0: WrongEpoch, no evidence kept.
    let before = st.accounting().evidence_kept;
    assert_eq!(st.apply_admission(&a0), Err(AdmissionError::WrongEpoch { held: 4, got: 3 }));
    assert_eq!(st.accounting().evidence_kept, before);
    let _: Option<&SignedAdmission> = None;
}
