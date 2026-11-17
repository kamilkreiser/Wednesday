#![allow(unused_imports, dead_code)]
mod common;
mod prop_common;
use coagent_roster::{IntakeError, Role, SignedProposal};
use common::*;
use prop_common::*;
fn by(p: &SignedProposal) -> Vec<u8> { p.encode().unwrap() }
/// A REFUSED call (junk bytes) after a demotion changes the accounting by pruning a counter.
#[test]
fn r3_note_a_refusal_prunes_a_counter() {
    let v = ids(12);
    let r = world(&v, session(240), 6, 0);
    let (vr, mut i) = intake(&v[0], &r[1]);
    let t = t0();
    for k in 2..=4 { i.receive(&vr, &v[k].key_id(), &by(&proposal(&v[k], &r[1], &v[7 + k], Role::Guest, k as u8)), t).unwrap(); }
    assert_eq!(i.receive(&vr, &v[6].key_id(), &by(&proposal(&v[6], &r[1], &v[8], Role::Guest, 20)), t).err(), Some(IntakeError::SessionPendingFull));
    let r3 = next(&v[0], &r[1], |b| { b.members.iter_mut().find(|m| m.key_id == v[6].key_id()).unwrap().role = Role::Observer; });
    let vr3 = view(&v[0], &v[0], &r3);
    let before = i.accounting();
    let got = i.receive(&vr3, &v[1].key_id(), b"junk", t);
    let after = i.accounting();
    println!("R3 NOTE refused junk: {got:?}; before {before:?}; after {after:?}");
    assert!(got.is_err());
    assert_ne!((before.crowded_guests, before.crowded_refusals), (after.crowded_guests, after.crowded_refusals));
}
