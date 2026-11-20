//! Gate check (ROSTER-SETTLE item 9): a differential over rosters WITHOUT a grant. Compiled
//! unchanged against the base tree and the head tree; writes one text line per observation to the
//! file named by QA_DIFF_OUT. Identities are loaded from QA_DIFF_IDS (generated once, shared).
mod common;
mod prop_common;

use std::io::Write;

use coagent_crypto::identity::DeviceIdentity;
use coagent_proto::bytes::{Digest32, KeyId};
use coagent_proto::canonical;
use coagent_roster::{
    body_hash, next_with_cap, sign, Member, ProposalIntake, Removed, Role, RosterBody, RosterChain,
    SessionChain, SignedRoster, CAP,
};
use common::member;
use prop_common::{proposal, t0, AT};

struct G(u64);
impl G {
    fn next(&mut self) -> u64 {
        self.0 ^= self.0 << 13;
        self.0 ^= self.0 >> 7;
        self.0 ^= self.0 << 17;
        self.0
    }
    fn below(&mut self, n: u64) -> u64 {
        self.next() % n
    }
}

fn hex(b: &[u8]) -> String {
    b.iter().map(|x| format!("{x:02x}")).collect()
}

fn load_ids() -> Vec<DeviceIdentity> {
    let path = std::env::var("QA_DIFF_IDS").expect("QA_DIFF_IDS");
    if let Ok(s) = std::fs::read_to_string(&path) {
        return s
            .lines()
            .map(|l| {
                let b: Vec<u8> = (0..l.len() / 2)
                    .map(|i| u8::from_str_radix(&l[2 * i..2 * i + 2], 16).unwrap())
                    .collect();
                DeviceIdentity::from_secret_bytes(&b).unwrap()
            })
            .collect();
    }
    let mut v: Vec<DeviceIdentity> = (0..14).map(|_| DeviceIdentity::generate().unwrap()).collect();
    v.sort_by_key(|d| d.key_id());
    let s: String = v.iter().map(|d| hex(&d.to_secret_bytes()) + "\n").collect();
    std::fs::write(&path, s).unwrap();
    v
}

#[test]
fn qa_diff_grant_free_rosters() {
    let v = load_ids();
    let seed: u64 = std::env::var("QA_DIFF_SEED").map(|s| s.parse().unwrap()).unwrap_or(0x5151_2026_1120_0009);
    let cases: usize = std::env::var("QA_DIFF_CASES").map(|s| s.parse().unwrap()).unwrap_or(4000);
    let mut out = std::fs::File::create(std::env::var("QA_DIFF_OUT").expect("QA_DIFF_OUT")).unwrap();
    let mut g = G(seed);
    let mut lines = 0usize;
    for case in 0..cases {
        let s = coagent_proto::bytes::SessionId([(case % 251) as u8; 32]);
        let cap = if g.below(3) == 0 { 4 } else { CAP };
        let first = sign(
            &v[0],
            RosterBody {
                session_id: s,
                version: 1,
                prev_hash: Digest32([0; 32]),
                convener: v[0].key_id(),
                cap,
                members: vec![member(&v[0], Role::Guest, 0, 1)],
                removed: vec![],
            },
        )
        .unwrap();
        let mut chain = RosterChain::start(&v[0].verified(), s, &v[0].key_id(), &first).unwrap();
        let mut sc = SessionChain::start(&v[0].verified(), s, &v[0].key_id(), &first).unwrap();
        let mut log = |l: String| {
            writeln!(out, "{case} {l}").unwrap();
        };
        log(format!("first {} {}", hex(&body_hash(&first.body).unwrap()), hex(&canonical::encode(&first.body).unwrap())));
        for step in 0..12 {
            let cur = chain.current().clone();
            let cb = cur.signed().body.clone();
            let mut b = cb.clone();
            b.version += 1;
            b.prev_hash = Digest32(body_hash(&cb).unwrap());
            let op = g.below(10);
            match op {
                0 | 1 => {
                    // invite: random identity, role, slot (sometimes bad)
                    let i = 1 + g.below(13) as usize;
                    let role = if g.below(3) == 0 { Role::Observer } else { Role::Guest };
                    let slot = g.below(9) as u8;
                    b.members.push(member(&v[i], role, slot, b.version));
                }
                2 => {
                    let ms: Vec<KeyId> = b.members.iter().skip(1).map(|m| m.key_id).collect();
                    if !ms.is_empty() {
                        let k = ms[g.below(ms.len() as u64) as usize];
                        b.members.retain(|m| m.key_id != k);
                        b.removed.push(Removed { key_id: k, at_version: b.version });
                    }
                }
                3 => {
                    let n = b.members.len() as u64;
                    let m = &mut b.members[g.below(n) as usize];
                    m.role = if m.role == Role::Guest { Role::Observer } else { Role::Guest };
                }
                4 => {
                    let c = [3u8, 4, 5, 8, 9][g.below(5) as usize];
                    let r = next_with_cap(&cur, c);
                    log(format!("{step} next_with_cap {c} {:?}", r.as_ref().map(|x| hex(&body_hash(x).unwrap()))));
                    match r {
                        Ok(x) => b = x,
                        Err(_) => continue,
                    }
                }
                5 => b.version += g.below(3),
                6 => b.prev_hash = Digest32([g.below(250) as u8; 32]),
                7 => {
                    // approve through the starter's intake (proposer = some guest member)
                    let guests: Vec<usize> = (1..14)
                        .filter(|i| cur.role_of(&v[*i].key_id()) == Some(Role::Guest))
                        .collect();
                    if guests.is_empty() {
                        continue;
                    }
                    let pr = guests[g.below(guests.len() as u64) as usize];
                    let cand = 1 + g.below(13) as usize;
                    let prole = if g.below(3) == 0 { Role::Observer } else { Role::Guest };
                    let mut i = ProposalIntake::new(&cur, &v[0].key_id()).unwrap();
                    let p = proposal(&v[pr], chain.current().signed(), &v[cand], prole, (step + 16 * (case % 8)) as u8);
                    let got = i.receive(&cur, &v[pr].key_id(), &p.encode().unwrap(), t0());
                    log(format!("{step} receive {:?}", got.as_ref().map(|_| ())));
                    let Ok(id) = got else { continue };
                    let role = if g.below(4) == 0 { Role::Observer } else { Role::Guest };
                    let at = if g.below(10) == 0 { "y".repeat(70) } else { AT.to_string() };
                    let mut i2 = ProposalIntake::new(&cur, &v[0].key_id()).unwrap();
                    let id2 = i2.receive(&cur, &v[pr].key_id(), &p.encode().unwrap(), t0()).unwrap();
                    let a = i.approve(&cur, &id, role, &at, t0());
                    let ar = i2.approve_with_report(&cur, &id2, role, &at, t0());
                    log(format!(
                        "{step} approve {:?} report {:?} outcome {:?}",
                        a.as_ref().map(|x| hex(&body_hash(x).unwrap())),
                        ar.as_ref().map(|x| (hex(&body_hash(&x.body).unwrap()), x.made_stale.len())),
                        i.outcome(&id)
                    ));
                    match a {
                        Ok(x) => b = x,
                        Err(_) => continue,
                    }
                }
                8 => {
                    // duplicate a member (bad)
                    let m: Member = b.members[0].clone();
                    b.members.push(m);
                }
                _ => {}
            }
            let r = sign(&v[0], b.clone()).unwrap();
            let enc = canonical::encode(&b).unwrap();
            let rc = chain.apply(&r).map(|x| format!("{x:?}"));
            let sr = sc.apply_roster(&r).map(|x| format!("{:?} {:?} {:?}", x.roster, x.grant_change, x.dropped));
            log(format!(
                "{step} op{op} hash {} enc {} chain {:?} session {:?} view {}",
                hex(&body_hash(&b).unwrap()),
                hex(&enc),
                rc,
                sr,
                hex(&coagent_crypto::kk::RosterView::roster_hash(sc.view()))
            ));
            lines += 1;
            let _: &SignedRoster = &r;
        }
    }
    println!("QA diff lines: {lines}");
}
