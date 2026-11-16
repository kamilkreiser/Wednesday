//! QA gate (M1 CORE) roster probes. `gate_demo_*` pass and document behaviour discussed in the verdict.
mod common;

use coagent_crypto::identity::{DeviceIdentity, SignDomain};
use coagent_proto::bytes::Digest32;
use coagent_roster::{sign, Member, Role, RosterBody, RosterChain, CAP};
use common::*;

/// A member entry that pairs ANOTHER device's Noise static key with the attacker's own signing
/// key (binding signed by the attacker) passes the validator: nothing refuses a Noise key that
/// appears under two key ids.
#[test]
fn gate_demo_two_members_share_one_noise_static() {
    let v = ids(3);
    let s = session(1);
    let victim = &v[1];
    let attacker = &v[2];
    let mut keys = attacker.public_keys();
    keys.noise_static = victim.public_keys().noise_static;
    keys.binding_sig = attacker.sign(SignDomain::Binding, keys.noise_static.as_bytes());
    let kid = coagent_crypto::identity::key_id(&keys.sign_pub, &keys.noise_static);
    let body = RosterBody {
        session_id: s,
        version: 1,
        prev_hash: Digest32([0; 32]),
        convener: v[0].key_id(),
        cap: CAP,
        members: vec![
            member(&v[0], Role::Guest, 0, 1),
            member(victim, Role::Guest, 1, 1),
            Member::new(&keys, kid, Role::Guest, 2, 1, "x"),
        ],
        removed: vec![],
    };
    let r = sign(&v[0], body).unwrap();
    assert!(RosterChain::start(&v[0].verified(), s, &r).is_ok());
}

/// RosterChain::start has no notion of the local device: a first roster that does not list the
/// joiner at all is accepted, at any version.
#[test]
fn gate_demo_first_roster_need_not_contain_the_joiner_and_may_be_any_version() {
    let v = ids(2);
    let s = session(2);
    let mut r = genesis(&v[0], s);
    for _ in 0..5 {
        r = next(&v[0], &r, |_| {});
    }
    let joiner: &DeviceIdentity = &v[1];
    let c = RosterChain::start(&v[0].verified(), s, &r).unwrap();
    assert_eq!(c.current().version(), 6);
    assert!(c.current().role_of(&joiner.key_id()).is_none());
}

/// Role upgrade observer -> guest between versions is accepted silently (no `Applied` signal).
#[test]
fn gate_demo_role_change_is_not_reported_in_applied() {
    let v = ids(2);
    let s = session(3);
    let r1 = genesis(&v[0], s);
    let r2 = next(&v[0], &r1, |b| add(b, &v[1], Role::Observer, 1));
    let r3 = next(&v[0], &r2, |b| b.members[1].role = Role::Guest);
    let mut c = RosterChain::start(&v[0].verified(), s, &r2).unwrap();
    let applied = c.apply(&r3).unwrap();
    assert_eq!(
        applied,
        coagent_roster::Applied::Advanced {
            added: vec![],
            removed: vec![]
        }
    );
    assert_eq!(c.current().role_of(&v[1].key_id()), Some(Role::Guest));
}
