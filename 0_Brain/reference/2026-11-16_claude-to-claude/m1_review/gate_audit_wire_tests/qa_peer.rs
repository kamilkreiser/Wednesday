//! QA-AUDIT-WIRE task 6: the checker's OWN hostile stream against a victim with --audit. The gate's
//! hostile peer is included READ-ONLY by #[path] (as tests/delta.rs does). Scratch copy only.
mod common;
#[rustfmt::skip]
#[path = "gate/gate_hostile/mod.rs"]
mod gate_hostile;

use std::fs;
use std::time::Duration;

use common::*;
use gate_hostile::*;
use serde_json::{json, Value};

fn keyid(h: &str) -> coagent_proto::bytes::KeyId {
    let mut a = [0u8; 32];
    hex::decode_to_slice(h, &mut a).unwrap();
    coagent_proto::bytes::KeyId(a)
}

struct Rng(u64);
impl Rng {
    fn next(&mut self) -> u64 {
        let mut x = self.0;
        x ^= x >> 12;
        x ^= x << 25;
        x ^= x >> 27;
        self.0 = x;
        x.wrapping_mul(0x2545_f491_4f6c_dd1d)
    }
}

fn audit(run: &Run, v: usize) -> Value {
    run.ctl(v, "status", json!({}))["result"]["audit"].clone()
}

fn archive_listing(run: &Run, v: usize) -> Vec<String> {
    let base = run.dir(v).join("audit");
    let mut out = vec![];
    for s in fs::read_dir(&base).unwrap() {
        let s = s.unwrap().path();
        for f in fs::read_dir(s.join("archive")).unwrap() {
            out.push(f.unwrap().file_name().to_string_lossy().to_string());
        }
    }
    out.sort();
    out
}

#[test]
fn qa_no_peer_input_seals() {
    let seed: u64 = std::env::var("QA_SEED").ok().and_then(|s| s.parse().ok()).unwrap_or(0x5eed_0a0a_7777);
    let n: usize = std::env::var("QA_N").ok().and_then(|s| s.parse().ok()).unwrap_or(150);
    println!("QA seed {seed:#x} n {n}");
    let mut rng = Rng(seed);
    let mut run = Run::new("qa_peer");
    let rs = run.root.join("relay.stderr");
    let relay = ExtRelay::start(&bin("coagent"), &run.home, fs::File::create(&rs).unwrap());
    run.extra_stderr.push(rs);
    let v = run.daemon("v", &["--relay-url", &relay.url, "--relay-pin", &relay.pin, "--audit"]);
    let victim = keyid(run.status(v)["key_id"].as_str().unwrap());
    let inv = run.ctl(v, "invite", json!({}));
    let line = inv["result"]["line"].as_str().unwrap().to_string();
    let mut h = Hostile::start(line, victim, "honest".into());
    h.expect("paired", Duration::from_secs(30));
    h.expect("up ", Duration::from_secs(30));
    std::thread::sleep(Duration::from_millis(500));
    let a0 = audit(&run, v);
    let arch0 = archive_listing(&run, v);
    println!("QA audit at start {a0}");
    let mut own_ids: Vec<String> = vec![];
    let mut own_ok = 0u64;
    let mut seq = 0u64;
    let mut reach: std::collections::BTreeMap<&str, u32> = Default::default();
    for i in 0..n {
        let pick = rng.next() % 11;
        let what = match pick {
            0 | 1 => {
                seq += 1;
                h.chat(seq, &format!("QA in order {i}"));
                "chat in order"
            }
            2 => {
                h.chat(seq.max(1), &format!("QA duplicate {i}"));
                "duplicate number"
            }
            3 => {
                seq += 3;
                h.chat(seq, &format!("QA out of order {i}"));
                "number out of order"
            }
            4 => {
                seq += 1;
                h.chat(seq, &"Q".repeat(70_000));
                "oversize text"
            }
            5 => {
                seq += 1;
                h.send(Cmd::Env { kind: "qa.never.delivered".into(), seq, re: None, crit: false, body: json!({"x": 1}), id: None });
                "a type never delivered"
            }
            6 => {
                let mut b = vec![0u8; (rng.next() % 300) as usize + 1];
                for x in b.iter_mut() {
                    *x = rng.next() as u8;
                }
                h.send(Cmd::Raw(b));
                "raw garbage"
            }
            7 => {
                if rng.next() % 2 == 0 {
                    h.send(Cmd::FreshKk);
                    "fresh key exchange"
                } else {
                    h.send(Cmd::ReplayKk1 { epoch: 1 + rng.next() % 3 });
                    "replayed key exchange"
                }
            }
            8 => {
                seq += 1;
                let re = own_ids.last().cloned();
                h.send(Cmd::Env {
                    kind: "chat.msg".into(), seq, re, crit: false,
                    body: json!({"audience": "agent", "author": "agent", "text": format!("QA reply naming the victim {i}")}), id: None,
                });
                "reply naming the victim's message"
            }
            9 => {
                seq += 1;
                h.send(Cmd::Env {
                    kind: "request.new".into(), seq, re: None, crit: false,
                    body: json!({"request_id": format!("{:032x}", rng.next()), "text": format!("QA request {i}")}), id: None,
                });
                "request"
            }
            _ => {
                let r = run.ctl(v, "send", json!({"kind": "chat", "text": format!("QA own send {i}")}));
                if r["ok"] == true {
                    own_ok += 1;
                    own_ids.push(r["result"]["id"].as_str().unwrap_or_default().to_string());
                }
                "own send"
            }
        };
        *reach.entry(what).or_default() += 1;
        std::thread::sleep(Duration::from_millis(20));
        if i % 25 == 24 {
            // the inbox drained (read + ack) so delivery keeps going
            let r = run.ctl(v, "inbox_read", json!({}));
            if let Some(ack) = r["result"]["ack"].as_u64() {
                run.ctl(v, "inbox_ack", json!({"upto": ack}));
            }
        }
    }
    std::thread::sleep(Duration::from_secs(2));
    h.drain();
    let a1 = audit(&run, v);
    let arch1 = archive_listing(&run, v);
    let alive = run.ctl(v, "status", json!({}))["ok"] == true;
    println!("QA reach {reach:?}");
    println!("QA own sends accepted {own_ok}");
    println!("QA audit at end {a1}");
    println!("QA archive {arch0:?} -> {arch1:?}");
    let seq0 = a0["own_seq"].as_u64().unwrap();
    let seq1 = a1["own_seq"].as_u64().unwrap();
    assert!(alive, "the victim answers");
    assert_eq!(arch0, arch1, "archive files changed");
    assert_eq!(a0["seals"], a1["seals"], "seals changed");
    assert_eq!(a0["segment"], a1["segment"], "segment changed");
    assert_eq!(seq1 - seq0, own_ok, "own seq changed by something other than own accepted sends");
    drop(h);
    run.finish();
    drop(relay);
}
