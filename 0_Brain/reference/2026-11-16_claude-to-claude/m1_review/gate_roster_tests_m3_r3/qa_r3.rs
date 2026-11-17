//! QA gate M3-ROSTER round 3 (head 44662d5). Findings-only tests; not part of the branch.
//! Drop into `crates/coagent-roster/tests/` (uses the crate's `common` and `prop_common`).
#![allow(clippy::all, unused_imports, unused_variables, dead_code)]
mod common;
mod prop_common;

use std::time::{Duration, Instant};

use coagent_crypto::identity::DeviceIdentity;
use coagent_proto::bytes::KeyId;
use coagent_roster::{
    sign, IntakeError, Outcome, ProposalId, ProposalIntake, Role, RosterChain, SignedProposal,
    SignedRoster, ValidRoster, CAP, MAX_PROPOSAL_BYTES, PROPOSAL_TTL,
};
use common::*;
use prop_common::*;

fn by(p: &SignedProposal) -> Vec<u8> {
    p.encode().unwrap()
}
fn twin(a: &DeviceIdentity, b: &DeviceIdentity) -> DeviceIdentity {
    let sa = a.to_secret_bytes();
    let sb = b.to_secret_bytes();
    let mut x = sa[..37].to_vec();
    x.extend_from_slice(&sb[37..]);
    DeviceIdentity::from_secret_bytes(&x).unwrap()
}
fn set_role(b: &mut coagent_roster::RosterBody, k: &DeviceIdentity, role: Role) {
    b.members.iter_mut().find(|m| m.key_id == k.key_id()).unwrap().role = role;
}

// ------------------------------------------------------------------------------------------------
// R2-2: a proposal id an entry already carries is refused at receive, before any card
// ------------------------------------------------------------------------------------------------

/// Version 3 holds C (P's proposal, id 7). A fresh intake. G (not P) offers id 7; then P offers it
/// for a different role and candidate; then, after the starter's own intake approves a new proposal
/// (id 20) and the chain moves to v4, a FRESH intake (restart) over v4 is offered id 20 and id 7.
/// Each: `IdCarriedByRoster`, accounting identical, no record, nobody charged, Q's pending untouched.
#[test]
fn r3_r2_2_roster_carried_id_refused_for_any_proposer_and_after_restart() {
    let v = ids(12);
    let s = session(231);
    let r = world(&v, s, 3, 0); // P=v1 Q=v2 G=v3
    let c = proposal(&v[1], &r[1], &v[5], Role::Guest, 7);
    let r3 = next(&v[0], &r[1], |b| add_proposed(b, &c, Role::Guest, 4));
    let (vr3, mut i) = intake(&v[0], &r3);
    let t = t0();
    let qid = i.receive(&vr3, &v[2].key_id(), &by(&proposal(&v[2], &r3, &v[6], Role::Guest, 30)), t).unwrap();
    for (who, cand, role) in [(&v[3], &v[7], Role::Guest), (&v[1], &v[8], Role::Observer)] {
        let acc = i.accounting();
        let used = i.used_by(&who.key_id());
        let got = i.receive(&vr3, &who.key_id(), &by(&proposal(who, &r3, cand, role, 7)), t);
        assert_eq!(got, Err(IntakeError::IdCarriedByRoster), "R3 R2-2: an id carried by a roster entry reached a card");
        assert_eq!(i.accounting(), acc, "R3 R2-2: a refused roster-carried id stored something");
        assert_eq!(i.used_by(&who.key_id()), used, "R3 R2-2: a refused roster-carried id was charged");
        assert_eq!(i.outcome(&pid(7)), None, "R3 R2-2: a record exists for the refused id");
        assert!(i.pending_proposal(&pid(7)).is_none());
        assert_eq!(i.outcome(&qid), Some(Outcome::Pending));
    }
    assert_eq!(i.approve_with_report(&vr3, &pid(7), Role::Guest, AT, t).err(), Some(IntakeError::UnknownProposal));
    // Q's proposal (id 30) is approved; the chain moves to v4, whose new entry carries id 30.
    let body = i.approve(&vr3, &qid, Role::Guest, AT, t).unwrap();
    let r4 = sign(&v[0], body).unwrap();
    let mut ch = RosterChain::start(&v[0].verified(), s, &v[0].key_id(), &r3).unwrap();
    ch.apply(&r4).unwrap();
    // The old intake remembers 30 (DuplicateId, its own check); a restarted intake does not, and the
    // roster check must catch it.
    assert_eq!(i.receive(&ch.current().clone(), &v[3].key_id(), &by(&proposal(&v[3], &r4, &v[9], Role::Guest, 30)), t).err(), Some(IntakeError::DuplicateId));
    let (vr4, mut j) = intake(&v[0], &r4);
    for n in [30u8, 7] {
        let acc = j.accounting();
        let got = j.receive(&vr4, &v[3].key_id(), &by(&proposal(&v[3], &r4, &v[9], Role::Guest, n)), t);
        assert_eq!(got, Err(IntakeError::IdCarriedByRoster), "R3 R2-2: a restarted intake let a roster-carried id reach a card (id {n})");
        assert_eq!(j.accounting(), acc);
    }
    // Positive control: a fresh id from the same guest is accepted.
    assert!(j.receive(&vr4, &v[3].key_id(), &by(&proposal(&v[3], &r4, &v[9], Role::Guest, 31)), t).is_ok());
}

// ------------------------------------------------------------------------------------------------
// R2-3: an end inside receive / approve / decline is reported exactly once
// ------------------------------------------------------------------------------------------------

fn count(list: &[(ProposalId, Outcome)], id: &ProposalId) -> usize {
    list.iter().filter(|(k, _)| k == id).count()
}

/// a (P) pending at t, b (Q, proposed observer) at t+300 s. At t+TTL a call ends `a` INSIDE it,
/// and that call itself FAILS (approve of b as guest: RoleRaised; approve of an unknown id; decline
/// of an unknown id; a wire string over the bound; a junk receive). The next tick must report
/// (a, Expired) exactly once, and the tick after it nothing. Then: three pending, approve one; the
/// two it made stale are in `made_stale` and must NOT come back from a later tick.
#[test]
fn r3_r2_3_end_inside_a_failing_call_reported_once_and_made_stale_never_twice() {
    let v = ids(10);
    let r = world(&v, session(232), 3, 0);
    let t = t0();
    let late = t + PROPOSAL_TTL;
    for how in ["approve_role_raised", "approve_unknown", "decline_unknown", "wire_too_large", "junk"] {
        let (vr, mut i) = intake(&v[0], &r[1]);
        let a = i.receive(&vr, &v[1].key_id(), &by(&proposal(&v[1], &r[1], &v[5], Role::Guest, 1)), t).unwrap();
        let b = i.receive(&vr, &v[2].key_id(), &by(&proposal(&v[2], &r[1], &v[6], Role::Observer, 2)), t + Duration::from_secs(300)).unwrap();
        let res = match how {
            "approve_role_raised" => i.approve_with_report(&vr, &b, Role::Guest, AT, late).err(),
            "approve_unknown" => i.approve_with_report(&vr, &pid(99), Role::Guest, AT, late).err(),
            "decline_unknown" => i.decline(&vr, &pid(99), late).err(),
            "wire_too_large" => i.receive_wire(&vr, &v[3].key_id(), &"0".repeat(2 * MAX_PROPOSAL_BYTES + 1), late).err(),
            _ => i.receive(&vr, &v[3].key_id(), b"junk", late).err(),
        };
        assert!(res.is_some(), "{how}: the call was meant to fail");
        assert_eq!(i.outcome(&a), Some(Outcome::Expired), "{how}");
        assert_eq!(i.outcome(&b), Some(Outcome::Pending), "{how}");
        assert_eq!(i.accounting().ended_unreported, 1, "R3 R2-3 {how}: the end is not counted as waiting");
        let first = i.tick(&vr, late + Duration::from_secs(1));
        assert_eq!(first, vec![(a, Outcome::Expired)], "R3 R2-3 {how}: an end inside a failing call was not reported exactly once by the next tick");
        let second = i.tick(&vr, late + Duration::from_secs(2));
        assert_eq!(count(&second, &a), 0, "R3 R2-3 {how}: an end was reported a second time");
        assert_eq!(i.accounting().ended_unreported, 0);
    }
    // made_stale is the only report of an approval's staling.
    let (vr, mut i) = intake(&v[0], &r[1]);
    let a = i.receive(&vr, &v[1].key_id(), &by(&proposal(&v[1], &r[1], &v[5], Role::Guest, 1)), t).unwrap();
    let b = i.receive(&vr, &v[2].key_id(), &by(&proposal(&v[2], &r[1], &v[6], Role::Guest, 2)), t).unwrap();
    let c = i.receive(&vr, &v[3].key_id(), &by(&proposal(&v[3], &r[1], &v[7], Role::Guest, 3)), t).unwrap();
    let ap = i.approve_with_report(&vr, &c, Role::Guest, AT, t).unwrap();
    let stale: Vec<ProposalId> = ap.made_stale.iter().map(|(k, _)| *k).collect();
    assert_eq!(stale, vec![a, b]);
    let r3 = sign(&v[0], ap.body).unwrap();
    let vr3 = view(&v[0], &v[0], &r3);
    let later = i.tick(&vr3, t + Duration::from_secs(1));
    assert!(count(&later, &a) == 0 && count(&later, &b) == 0, "R3 R2-3: a proposal made stale by an approval was reported again by tick: {later:?}");
    assert_eq!(i.accounting().ended_unreported, 0);
}

// ------------------------------------------------------------------------------------------------
// R2-4: the crowded-out counter
// ------------------------------------------------------------------------------------------------

/// Cap 8, guests v1..v6. v1 is MUTED with quota left (1 used); v5 has its quota USED and is NOT
/// muted; v2..v4 hold the three session slots; v6 is honest. While full: v1 and v5 are refused
/// with SessionPendingFull and their counters stay 0 (each condition separately); v2 (own pending)
/// gets ProposerHasPending and is not counted; v6 is counted once and the accounting moves by
/// exactly one counter and one refusal. v6 demoted to observer: the next call drops it, and the
/// accounting shows it. v6 promoted again: it starts from 0.
#[test]
fn r3_r2_4_counter_mute_and_quota_separately_accounted_and_dropped() {
    let v = ids(14);
    let s = session(233);
    let r = world(&v, s, 6, 0);
    let (vr, mut i) = intake(&v[0], &r[1]);
    let t = t0();
    let mut n = 0u8;
    let mut nid = || {
        n += 1;
        n
    };
    // v1: one proposal, declined and muted.
    let a = i.receive(&vr, &v[1].key_id(), &by(&proposal(&v[1], &r[1], &v[7], Role::Guest, nid())), t).unwrap();
    i.decline_and_mute(&vr, &a, t).unwrap();
    assert_eq!(i.used_by(&v[1].key_id()), 1);
    // v5: eight proposals, each declined (not muted).
    for _ in 0..8 {
        let id = i.receive(&vr, &v[5].key_id(), &by(&proposal(&v[5], &r[1], &v[7], Role::Guest, nid())), t).unwrap();
        i.decline(&vr, &id, t).unwrap();
    }
    assert_eq!(i.used_by(&v[5].key_id()), 8);
    // fill the three session slots
    for k in 2..=4 {
        i.receive(&vr, &v[k].key_id(), &by(&proposal(&v[k], &r[1], &v[7 + k], Role::Guest, nid())), t).unwrap();
    }
    let acc = i.accounting();
    for _ in 0..3 {
        assert_eq!(i.receive(&vr, &v[1].key_id(), &by(&proposal(&v[1], &r[1], &v[8], Role::Guest, nid())), t).err(), Some(IntakeError::SessionPendingFull));
        assert_eq!(i.receive(&vr, &v[5].key_id(), &by(&proposal(&v[5], &r[1], &v[8], Role::Guest, nid())), t).err(), Some(IntakeError::SessionPendingFull));
        assert_eq!(i.receive(&vr, &v[2].key_id(), &by(&proposal(&v[2], &r[1], &v[8], Role::Guest, nid())), t).err(), Some(IntakeError::ProposerHasPending));
    }
    assert_eq!(i.crowded_out(&v[1].key_id()), 0, "R3 R2-4: a muted guest (quota left) moved its own counter");
    assert_eq!(i.crowded_out(&v[5].key_id()), 0, "R3 R2-4: a quota-used guest (not muted) moved its own counter");
    assert_eq!(i.crowded_out(&v[2].key_id()), 0, "R3 R2-4: a guest with its own pending proposal was counted");
    assert_eq!(i.accounting(), acc, "R3 R2-4: an uncounted refusal moved the accounting");
    assert_eq!(i.receive(&vr, &v[6].key_id(), &by(&proposal(&v[6], &r[1], &v[8], Role::Guest, nid())), t).err(), Some(IntakeError::SessionPendingFull));
    assert_eq!(i.crowded_out_counts(), vec![(v[6].key_id(), 1)]);
    let mut want = acc;
    want.crowded_guests += 1;
    want.crowded_refusals += 1;
    assert_eq!(i.accounting(), want, "R3 R2-4: the accounting does not show exactly one more counter");
    // demote v6: dropped at the next call, visible in the accounting.
    let r3 = next(&v[0], &r[1], |b| set_role(b, &v[6], Role::Observer));
    let vr3 = view(&v[0], &v[0], &r3);
    let _ = i.tick(&vr3, t);
    assert_eq!(i.crowded_out(&v[6].key_id()), 0, "R3 R2-4: a counter was kept for a key that is no longer a guest");
    assert_eq!((i.accounting().crowded_guests, i.accounting().crowded_refusals), (0, 0));
    let r4 = next(&v[0], &r3, |b| set_role(b, &v[6], Role::Guest));
    let vr4 = view(&v[0], &v[0], &r4);
    let _ = i.tick(&vr4, t);
    assert_eq!(i.crowded_out(&v[6].key_id()), 0);
}

// ------------------------------------------------------------------------------------------------
// R2-5 and R2-9: the wire bound; tick on a refused wire input; check_roster in receive_wire
// ------------------------------------------------------------------------------------------------

/// 4,097 characters (hex and non-hex) must be TooLarge; 4,096 (hex and non-hex, odd-free) must be
/// Malformed; 4,095 Malformed. Nothing stored by any of them.
#[test]
fn r3_r2_5_wire_bound_edges() {
    let v = ids(6);
    let r = world(&v, session(234), 2, 0);
    let (vr, mut i) = intake(&v[0], &r[1]);
    let t = t0();
    let acc = i.accounting();
    let lim = 2 * MAX_PROPOSAL_BYTES;
    assert_eq!(lim, 4096);
    for (w, want) in [
        ("0".repeat(lim + 1), IntakeError::TooLarge),
        ("z".repeat(lim + 1), IntakeError::TooLarge),
        ("0".repeat(lim), IntakeError::Malformed),
        ("z".repeat(lim), IntakeError::Malformed),
        ("0".repeat(lim - 1), IntakeError::Malformed),
    ] {
        let got = i.receive_wire(&vr, &v[1].key_id(), &w, t);
        assert_eq!(got.err(), Some(want.clone()), "R3 R2-5: a wire string of {} characters was not {:?}", w.len(), want);
        assert_eq!(i.accounting(), acc);
    }
}

/// A pending proposal at t. (1) At t+TTL a refused wire string (too large, then malformed, each in
/// its own intake) ends it inside the call; the next tick reports it once. (2) Another session's
/// roster passed to receive_wire is refused with WrongRoster BEFORE anything: the pending proposal
/// is not staled, nothing waits to be reported.
#[test]
fn r3_r2_9_tick_on_refused_wire_and_roster_check() {
    let v = ids(8);
    let r = world(&v, session(235), 2, 0);
    let t = t0();
    for (w, want) in [("0".repeat(4097), IntakeError::TooLarge), ("0g".repeat(10), IntakeError::Malformed)] {
        let (vr, mut i) = intake(&v[0], &r[1]);
        let a = i.receive(&vr, &v[1].key_id(), &by(&proposal(&v[1], &r[1], &v[5], Role::Guest, 1)), t).unwrap();
        assert_eq!(i.receive_wire(&vr, &v[2].key_id(), &w, t + PROPOSAL_TTL).err(), Some(want.clone()));
        assert_eq!(i.outcome(&a), Some(Outcome::Expired), "R3 R2-9: a refused {want:?} wire string did not run the expiry");
        assert_eq!(i.tick(&vr, t + PROPOSAL_TTL), vec![(a, Outcome::Expired)]);
    }
    let (vr, mut i) = intake(&v[0], &r[1]);
    let a = i.receive(&vr, &v[1].key_id(), &by(&proposal(&v[1], &r[1], &v[5], Role::Guest, 1)), t).unwrap();
    let other = world(&v, session(236), 2, 0);
    let vro = view(&v[0], &v[0], &other[1]);
    let acc = i.accounting();
    for w in ["0".repeat(4097), "zz".to_string(), by(&proposal(&v[1], &other[1], &v[6], Role::Guest, 2)).iter().map(|b| format!("{b:02x}")).collect()] {
        assert_eq!(i.receive_wire(&vro, &v[1].key_id(), &w, t).err(), Some(IntakeError::WrongRoster), "R3 R2-9: receive_wire checked a string against another session's roster");
        assert_eq!(i.outcome(&a), Some(Outcome::Pending), "R3 R2-9: another session's roster staled a pending proposal");
        assert_eq!(i.accounting(), acc);
    }
}

// ------------------------------------------------------------------------------------------------
// Addendum 6 §3: try to reach the validator run in a normal build
// ------------------------------------------------------------------------------------------------

struct Rng(u64);
impl Rng {
    fn n(&mut self, m: u64) -> u64 {
        self.0 ^= self.0 << 13;
        self.0 ^= self.0 >> 7;
        self.0 ^= self.0 << 17;
        self.0 % m
    }
}

/// Random sequences: receives from any key (members, observers, starter, outsiders, a wrong
/// sender), candidates from members, outsiders, removed keys and key twins, ids from a small set
/// (so ids carried by entries come back), against the current or the previous version; approvals
/// with any role and `added_at` of 60..66 bytes; declines and decline-and-mutes; ticks with time
/// jumps; the starter's own direct changes (invite, remove, role change, limit raise); and
/// RESTARTS (a fresh intake). Invariants checked on every step:
/// - `approve` never returns `InvalidApproval` (the validator run is not reached) and every body it
///   returns is accepted by a chain holder;
/// - every Expired/Stale end is reported exactly once (tick or made_stale) per intake;
/// - a SessionPendingFull refusal moves the sender's counter iff the sender is unmuted with quota
///   left.
#[test]
fn r3_a6_validator_run_unreached_by_random_sequences() {
    let pool = ids(16);
    let mut twins = Vec::new();
    for k in 1..5 {
        twins.push(twin(&pool[k], &pool[10 + k]));
    }
    let keys: Vec<&DeviceIdentity> = pool.iter().chain(twins.iter()).collect();
    let (mut ok_approvals, mut invalid, mut carried, mut steps, mut restarts) = (0u64, 0u64, 0u64, 0u64, 0u64);
    let mut first_invalid = String::new();
    for seed in 1..=600u64 {
        let mut g = Rng(seed.wrapping_mul(0x9E37_79B9_7F4A_7C15) | 1);
        let s = session((seed % 200) as u8 + 20);
        let r = world(&pool, s, 3, 1); // v1..v3 guests, v4 observer
        let mut ch = RosterChain::start(&pool[0].verified(), s, &pool[0].key_id(), &r[1]).unwrap();
        let mut prev: SignedRoster = r[0].clone();
        let mut cur: SignedRoster = r[1].clone();
        let mut vr: ValidRoster = ch.current().clone();
        let mut i = ProposalIntake::new(&vr, &pool[0].key_id()).unwrap();
        let mut t: Instant = t0();
        let mut accepted: Vec<ProposalId> = Vec::new();
        let mut reports: Vec<(ProposalId, u32)> = Vec::new();
        let mut muted: Vec<KeyId> = Vec::new();
        let bump = |reports: &mut Vec<(ProposalId, u32)>, id: ProposalId| {
            if let Some(e) = reports.iter_mut().find(|e| e.0 == id) {
                e.1 += 1
            } else {
                reports.push((id, 1))
            }
        };
        let close = |i: &mut ProposalIntake, vr: &ValidRoster, t: Instant, accepted: &Vec<ProposalId>, reports: &mut Vec<(ProposalId, u32)>, seed: u64| {
            for (id, _) in i.tick(vr, t) {
                if let Some(e) = reports.iter_mut().find(|e| e.0 == id) { e.1 += 1 } else { reports.push((id, 1)) }
            }
            for id in accepted {
                let n = reports.iter().find(|e| e.0 == *id).map(|e| e.1).unwrap_or(0);
                let want = match i.outcome(id) {
                    Some(Outcome::Expired) | Some(Outcome::Stale) => 1,
                    _ => 0,
                };
                assert_eq!(n, want, "R3 A6: seed {seed}: an end was reported {n} times, outcome {:?}", i.outcome(id));
            }
        };
        for _ in 0..90 {
            steps += 1;
            let op = { let x = g.n(60); if x == 59 { 19 } else { x % 19 } };
            if op < 9 {
                // receive
                let guests: Vec<&DeviceIdentity> = keys.iter().copied().filter(|k| vr.role_of(&k.key_id()) == Some(Role::Guest) && !vr.is_convener(&k.key_id())).collect();
                let outsiders: Vec<&DeviceIdentity> = keys.iter().copied().filter(|k| vr.role_of(&k.key_id()).is_none()).collect();
                let proposer = if g.n(10) < 7 && !guests.is_empty() { guests[g.n(guests.len() as u64) as usize] } else { keys[g.n(keys.len() as u64) as usize] };
                let cand = if g.n(10) < 6 && !outsiders.is_empty() { outsiders[g.n(outsiders.len() as u64) as usize] } else { keys[g.n(keys.len() as u64) as usize] };
                let role = if g.n(3) == 0 { Role::Observer } else { Role::Guest };
                let id = g.n(10) as u8 + 1;
                let at = if g.n(10) == 0 { &prev } else { &cur };
                let sender = if g.n(12) == 0 { keys[g.n(keys.len() as u64) as usize].key_id() } else { proposer.key_id() };
                let sp = proposal(proposer, at, cand, role, id);
                let before = i.crowded_out(&sender);
                let used = i.used_by(&sender);
                let is_muted = muted.contains(&sender);
                let got = if g.n(4) == 0 {
                    i.receive_wire(&vr, &sender, &sp.to_wire().unwrap(), t)
                } else {
                    i.receive(&vr, &sender, &by(&sp), t)
                };
                match got {
                    Ok(pid_) => accepted.push(pid_),
                    Err(IntakeError::IdCarriedByRoster) => carried += 1,
                    Err(IntakeError::SessionPendingFull) => {
                        let after = i.crowded_out(&sender);
                        if is_muted || used >= 8 {
                            assert_eq!(after, before, "R3 A6: seed {seed}: a muted or quota-used guest moved its counter");
                        } else {
                            assert_eq!(after, before + 1, "R3 A6: seed {seed}: a countable guest was not counted");
                        }
                    }
                    Err(_) => {}
                }
            } else if op < 13 {
                // approve a random id (accepted ones mostly)
                let id = if !accepted.is_empty() && g.n(5) != 0 { accepted[g.n(accepted.len() as u64) as usize] } else { pid(g.n(10) as u8 + 1) };
                let role = if g.n(3) == 0 { Role::Observer } else { Role::Guest };
                let at_len = 60 + g.n(7) as usize;
                let added_at = "x".repeat(at_len);
                match i.approve_with_report(&vr, &id, role, &added_at, t) {
                    Ok(ap) => {
                        for (k, _) in &ap.made_stale {
                            bump(&mut reports, *k);
                        }
                        let signed = sign(&pool[0], ap.body).unwrap();
                        let applied = ch.apply(&signed);
                        assert!(applied.is_ok(), "R3 A6: seed {seed}: approve returned a body a holder refuses: {:?}", applied.err());
                        ok_approvals += 1;
                        prev = cur;
                        cur = signed;
                        vr = ch.current().clone();
                    }
                    Err(IntakeError::InvalidApproval(e)) => {
                        invalid += 1;
                        if first_invalid.is_empty() {
                            first_invalid = format!("seed {seed}: {e:?}");
                        }
                    }
                    Err(_) => {}
                }
            } else if op < 15 {
                let id = if !accepted.is_empty() { accepted[g.n(accepted.len() as u64) as usize] } else { pid(1) };
                let who = i.pending_proposal(&id).map(|p| p.body.proposer);
                if g.n(2) == 0 {
                    let _ = i.decline(&vr, &id, t);
                } else if i.decline_and_mute(&vr, &id, t).is_ok() {
                    if let Some(k) = who {
                        muted.push(k);
                    }
                }
            } else if op < 17 {
                t += Duration::from_secs(g.n(2 * PROPOSAL_TTL.as_secs()));
                for (id, _) in i.tick(&vr, t) {
                    bump(&mut reports, id);
                }
            } else if op < 19 {
                // the starter's direct change
                let kind = g.n(4);
                let d = &pool[1 + g.n(15) as usize];
                let nx = next(&pool[0], &cur, |b| match kind {
                    0 => {
                        if b.members.iter().all(|m| m.key_id != d.key_id()) {
                            if let Some(slot) = (0..b.cap).find(|s| b.members.iter().all(|m| m.slot != *s)) {
                                add(b, d, Role::Guest, slot);
                            }
                        }
                    }
                    1 => {
                        if b.members.iter().any(|m| m.key_id == d.key_id()) {
                            remove(b, d);
                        }
                    }
                    2 => {
                        if let Some(m) = b.members.iter_mut().find(|m| m.key_id == d.key_id()) {
                            m.role = if m.role == Role::Guest { Role::Observer } else { Role::Guest };
                        }
                    }
                    _ => b.cap = CAP,
                });
                if ch.apply(&nx).is_ok() {
                    prev = cur;
                    cur = nx;
                    vr = ch.current().clone();
                }
            } else {
                // restart: a fresh intake (in memory only)
                close(&mut i, &vr, t, &accepted, &mut reports, seed);
                i = ProposalIntake::new(&vr, &pool[0].key_id()).unwrap();
                accepted.clear();
                reports.clear();
                muted.clear();
                restarts += 1;
            }
        }
        close(&mut i, &vr, t, &accepted, &mut reports, seed);
    }
    println!("R3 A6 exploration: steps {steps}, approvals ok {ok_approvals}, InvalidApproval {invalid}, IdCarriedByRoster {carried}, restarts {restarts}; first invalid: {first_invalid}");
    assert_eq!(invalid, 0, "R3 A6: the validator run inside approve was reached in a normal build ({first_invalid})");
    assert!(ok_approvals > 500 && carried > 20 && restarts > 0, "R3 A6: the generator did not reach approvals / carried ids / restarts");
}
