//! QA gate M3-ROSTER: run on MAIN. Generates fresh identities and a three-version chain with
//! unproposed entries (guest, observer, a removal), writes secrets, encodings and hashes to the file
//! named by QA_PIN_OUT, so the head can be checked against bytes MAIN produced.
use coagent_crypto::identity::DeviceIdentity;
use coagent_proto::bytes::{Digest32, SessionId};
use coagent_roster::{body_hash, sign, Member, Removed, Role, RosterBody, RosterChain, SignedRoster, CAP};

fn hex(b: &[u8]) -> String {
    b.iter().map(|x| format!("{x:02x}")).collect()
}

fn m(d: &DeviceIdentity, role: Role, slot: u8, added_in: u64, at: &str) -> Member {
    Member::new(&d.public_keys(), d.key_id(), role, slot, added_in, at)
}

#[test]
fn qa_pin_gen() {
    let Ok(out) = std::env::var("QA_PIN_OUT") else { return };
    let v: Vec<DeviceIdentity> = (0..5).map(|_| DeviceIdentity::generate().unwrap()).collect();
    let s = SessionId([0x42; 32]);
    let r1 = sign(&v[0], RosterBody {
        session_id: s, version: 1, prev_hash: Digest32([0; 32]), convener: v[0].key_id(), cap: CAP,
        members: vec![m(&v[0], Role::Guest, 0, 1, "t0")], removed: vec![],
    }).unwrap();
    let mut b2 = r1.body.clone();
    b2.version = 2;
    b2.prev_hash = Digest32(body_hash(&r1.body).unwrap());
    b2.members.push(m(&v[1], Role::Guest, 1, 2, "t1"));
    b2.members.push(m(&v[2], Role::Observer, 5, 2, "t2"));
    b2.members.push(m(&v[3], Role::Guest, 7, 2, ""));
    let r2 = sign(&v[0], b2).unwrap();
    let mut b3 = r2.body.clone();
    b3.version = 3;
    b3.prev_hash = Digest32(body_hash(&r2.body).unwrap());
    b3.members.retain(|x| x.key_id != v[3].key_id());
    b3.removed.push(Removed { key_id: v[3].key_id(), at_version: 3 });
    b3.members.push(m(&v[4], Role::Observer, 2, 3, "t4"));
    let r3 = sign(&v[0], b3).unwrap();
    // sanity on main
    let mut c = RosterChain::start(&v[0].verified(), s, &v[1].key_id(), &r1).err();
    assert!(c.is_some());
    let mut ch = RosterChain::start(&v[0].verified(), s, &v[0].key_id(), &r1).unwrap();
    ch.apply(&r2).unwrap();
    ch.apply(&r3).unwrap();
    c = None;
    let _ = c;
    let mut txt = String::new();
    for d in &v {
        txt.push_str(&format!("id {}\n", hex(&d.to_secret_bytes())));
    }
    for r in [&r1, &r2, &r3] {
        let e: Vec<u8> = SignedRoster::encode(r).unwrap();
        txt.push_str(&format!("roster {}\n", String::from_utf8(e).unwrap()));
        txt.push_str(&format!("hash {}\n", hex(&body_hash(&r.body).unwrap())));
    }
    std::fs::write(out, txt).unwrap();
}
