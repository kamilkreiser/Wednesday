//! QA-DAEMON-NOTES copy of dn_recovery.rs with the property's seeds moved (QA_SEED0, default 7001).
//! DAEMON-NOTES property 6 (G27 as ruled, FR-7), on the branch's model harness
//! (`tests/support/model.rs`: two REAL `recovery::Machine`s; used, never edited; `recovery_model.rs`
//! is not edited either).
//!
//! * R6-2 (BACKLOG, check of daemon r6): the refill on a forward acknowledgement clears row 54's
//!   clock (`skips_spent_at`), and no test killed a mutant that leaves it. Here: the skip budget is
//!   spent, the link queue is full (a stalled socket: the pump cannot send more), then the peer's
//!   acknowledgement moves forward over everything in flight. Nothing is in flight and the outbox
//!   is empty, so NO clock may fire at row 54's time; a stale `skips_spent_at` fires a RESYNC there.
//! * R6-5 (BACKLOG, check of daemon r6): a generated property whose hostile peer ALSO sends
//!   sequenced messages (in order, gaps, duplicates, `u64::MAX`) and STARTS key exchanges (forged
//!   message 1, also while the sender's skip budget is spent), beside positions, acknowledgements,
//!   `full`/`room`, silences and cuts. V5 after every tick (no wait without a deadline); at the end
//!   the peer turns honest and the sender's LAST message is lost once on the way: only the
//!   sender's retransmit clock (T-RTO) can heal that, so V4 (delivered once honest) is checked.
//!   120 seeds, the seed printed on failure, reach counts required above zero.
#![allow(clippy::needless_range_loop)]
mod common;
#[path = "support/model.rs"]
mod model;

use std::time::Duration;

use coagent_daemon::recovery::{Crypto, RecoveryConfig};
use coagent_daemon::wire::{self, SessionPayload};
use coagent_relay::frame::{decode_data, encode_data};
use coagent_relay::state::Out;
use model::*;
use serde_json::json;

/// The hostile peer `p` sends with its own keys; its counter is set to what the receiver `p ^ 1`
/// expects next (frames an adversary kept back were never sent by this peer).
fn sync_counter(sim: &mut Sim, p: usize) {
    let want = sim.sides[p ^ 1].keys.live.as_ref().map(|c| (c.id, c.recv));
    if let (Some((id, w)), Some(ch)) = (want, sim.sides[p].keys.live.as_mut()) {
        if ch.id == id {
            ch.send = w;
        }
    }
}

fn says(sim: &mut Sim, p: usize, kind: &str, ack: u64, body: serde_json::Value) -> bool {
    sync_counter(sim, p);
    sim.hostile_control(p, kind, ack, body)
}

fn peer_says(sim: &mut Sim, kind: &str, ack: u64, body: serde_json::Value) -> bool {
    says(sim, 1, kind, ack, body)
}

fn peer_message(sim: &mut Sim, p: usize, seq: u64, id: &str) -> bool {
    sync_counter(sim, p);
    sim.hostile_message(p, seq, id)
}

/// The hostile peer `p` STARTS a key exchange: a message 1 made with its own keys (the model's
/// `kk_initiate` for that side), delivered to the other side as the relay would. Only a peer with
/// the LOWER key id may start one (the other side is the responder; an initiator ignores message 1,
/// `recovery.rs` `on_kk1`), so the property's hostile peer is side 0 and its sender side 1.
fn peer_starts_exchange(sim: &mut Sim, p: usize, epoch: u64) -> bool {
    let m1 = {
        let mut cx = MCrypto {
            side: p,
            world: &mut sim.world,
            k: &mut sim.sides[p].keys,
        };
        match cx.kk_initiate() {
            Some((_, m)) => m,
            None => return false,
        }
    };
    let p2 = wire::encode_session(&SessionPayload::Kk1 { epoch, msg: &m1 });
    let Some(b) = encode_data((p ^ 1) as u8, p as u8, 1, &p2, usize::MAX) else {
        return false;
    };
    sim.feed(p ^ 1, &Out::Binary(b.into()));
    true
}

/// The envelope id inside a relay data item (the omniscient view), if it is a channel frame.
fn frame_id(o: &Out) -> Option<String> {
    let Out::Binary(b) = o else { return None };
    let d = decode_data(b, usize::MAX).ok()?;
    match wire::decode_session(d.payload).ok()? {
        SessionPayload::Frame { frame, .. } => {
            content_of(frame)?["id"].as_str().map(str::to_string)
        }
        _ => None,
    }
}

fn t_rto(sim: &Sim) -> u64 {
    sim.sides[0].m.resyncs.get("T-RTO").copied().unwrap_or(0)
}

/// Drops every binary item delivered to the sender (side 0) while `mute`.
struct Mute {
    mute: bool,
}
impl Adversary for Mute {
    fn on_deliver(&mut self, to: usize, item: &Out, _t: Duration) -> Verdict {
        if self.mute && to == 0 && matches!(item, Out::Binary(_)) {
            Verdict::Drop
        } else {
            Verdict::Deliver
        }
    }
}

fn settled(cfg: RecoveryConfig, n: u64) -> Sim {
    let mut sim = Sim::new(cfg);
    connect(&mut sim);
    let mut k = 0;
    while k < n {
        // In batches the outbox takes (as `gate_r6_model.rs` does).
        let batch = (n - k).min(100);
        for _ in 0..batch {
            assert!(sim.send(0, &format!("m0-{k:05}")), "setup send {k}");
            k += 1;
        }
        let ok = sim.run_until(Duration::from_secs(60), &mut Honest, |s| {
            s.sides[0].m.ob.items.is_empty()
        });
        assert!(ok, "setup: delivered and acknowledged");
        while !sim.read_all(1).is_empty() {}
    }
    sim.run_for(Duration::from_secs(1), &mut Honest);
    sim
}

#[test]
fn a_forward_ack_clears_row_54s_clock() {
    let cfg = RecoveryConfig {
        max_skips: 8,
        ..RecoveryConfig::default()
    };
    let rto = cfg.rto;
    let mut sim = settled(cfg, 50);
    let mut adv = Mute { mute: true };
    // The peer states a position of 0 (the trim pattern): the pump restarts at 1, every number up
    // to 50 is no longer held, so it sends skips until the budget (8) is spent.
    assert!(peer_says(
        &mut sim,
        "full",
        0,
        json!({ "last_seq_received": 0 })
    ));
    assert!(peer_says(
        &mut sim,
        "resume",
        0,
        json!({ "last_seq_received": 0, "room": true })
    ));
    sim.run_for(Duration::from_millis(300), &mut adv);
    {
        let m = &sim.sides[0].m;
        assert_eq!(m.skips_left, 0, "the budget is spent");
        assert!(m.skips_spent_at.is_some() && sim.sides[0].skips_waiting_now());
        assert_eq!(m.in_flight.len(), 8);
    }
    // A stalled socket: the link queue is full, so the pump can send nothing more.
    sim.sides[0].drain_per_tick = 0;
    while sim.sides[0].linkq.len() < LINKQ {
        sim.sides[0].linkq.push_back((0, vec![]));
    }
    let before = t_rto(&sim);
    // The forward acknowledgement over everything in flight: it refills the budget.
    assert!(peer_says(&mut sim, "ack", 8, json!({})));
    {
        let m = &sim.sides[0].m;
        assert_eq!(m.skips_left, 8, "refilled");
        assert!(m.in_flight.is_empty() && m.ob.items.is_empty());
        assert!(m.next_out < m.ob.send_next, "numbers still to send");
    }
    // Past row 54's time (counted from the spend): no clock may fire.
    sim.run_for(rto + Duration::from_secs(3), &mut adv);
    assert_eq!(
        t_rto(&sim),
        before,
        "a RESYNC fired at row 54's time after a forward acknowledgement refilled the budget \
         (skips_spent_at left set: {:?})",
        sim.sides[0].m.skips_spent_at
    );
    assert!(sim.sides[0].m.skips_spent_at.is_none());
    // Positive control: the socket drains again and the refilled budget is used.
    sim.sides[0].linkq.clear();
    sim.sides[0].drain_per_tick = 1000;
    let next0 = sim.sides[0].m.next_out;
    sim.run_for(Duration::from_millis(500), &mut adv);
    assert_eq!(
        sim.sides[0].m.next_out,
        next0 + 8,
        "eight more skips after the refill"
    );
}

/// The R6-5 property's roles: the sender (its outbox, its skip budget) and the hostile peer.
const S: usize = 1;
const P: usize = 0;

#[derive(Debug, Clone)]
enum Op {
    Full { pos: u64, ack: u64 },
    Resume { pos: u64, room: bool, ack: u64 },
    Ack { ack: u64 },
    TrimPattern,
    PeerMessage { seq: u64 },
    PeerExchange { epoch: u64 },
    Silent { secs: u64 },
    Cut { to: usize },
    PeerSend,
    SenderSend,
}

fn pick(r: &mut Rng, top: u64) -> u64 {
    match r.below(7) {
        0 => 0,
        1 => 1,
        2 => top / 2,
        3 => top,
        4 => top + 1 + r.below(1000),
        5 => u64::MAX,
        _ => r.below(top + 1),
    }
}

fn gen_op(r: &mut Rng, sim: &Sim) -> Op {
    let top = sim.sides[S].m.ob.send_next.saturating_sub(1);
    let recv = sim.sides[S].m.ib.recv_upto;
    match r.below(22) {
        0..=1 => Op::Full {
            pos: pick(r, top),
            ack: pick(r, top),
        },
        2..=4 => Op::Resume {
            pos: pick(r, top),
            room: r.chance(50),
            ack: pick(r, top),
        },
        5..=6 => Op::Ack { ack: pick(r, top) },
        7..=8 => Op::TrimPattern,
        9..=12 => Op::PeerMessage {
            seq: match r.below(5) {
                0 | 1 => recv + 1,
                2 => recv + 2 + r.below(5),
                3 => recv.max(1),
                _ => u64::MAX,
            },
        },
        13..=15 => Op::PeerExchange {
            epoch: sim.sides[S].m.live.unwrap_or(0) + r.below(3),
        },
        16 => Op::Silent {
            secs: 1 + r.below(20),
        },
        17 => Op::Cut {
            to: r.below(2) as usize,
        },
        18..=19 => Op::PeerSend,
        _ => Op::SenderSend,
    }
}

/// The run's relay: silences toward the sender, one-shot cuts, and (end phase) one lost frame.
struct Chaos {
    silent_until: Duration,
    cut: [bool; 2],
    lose_id: Option<String>,
    lost: bool,
}
impl Adversary for Chaos {
    fn on_deliver(&mut self, to: usize, item: &Out, t: Duration) -> Verdict {
        if to == S && t < self.silent_until && matches!(item, Out::Binary(_)) {
            return Verdict::Drop;
        }
        if to == P && !self.lost && self.lose_id.is_some() && frame_id(item) == self.lose_id {
            self.lost = true;
            return Verdict::Drop;
        }
        Verdict::Deliver
    }
    fn cut(&mut self, to: usize, _t: Duration) -> bool {
        std::mem::take(&mut self.cut[to])
    }
}

/// A settled pair whose SENDER is side `S` (the responder) with `n` messages sent and acknowledged.
fn settled_sender_1(cfg: RecoveryConfig, n: u64) -> Sim {
    let mut sim = Sim::new(cfg);
    connect(&mut sim);
    let mut k = 0;
    while k < n {
        let batch = (n - k).min(100);
        for _ in 0..batch {
            assert!(sim.send(S, &format!("s-{k:05}")), "setup send {k}");
            k += 1;
        }
        let ok = sim.run_until(Duration::from_secs(60), &mut Honest, |s| {
            s.sides[S].m.ob.items.is_empty()
        });
        assert!(ok, "setup: delivered and acknowledged");
        while !sim.read_all(P).is_empty() {}
    }
    sim.run_for(Duration::from_secs(1), &mut Honest);
    sim
}

#[test]
fn hostile_peer_messages_and_key_exchanges_never_leave_a_wait_without_a_clock() {
    let cfg = RecoveryConfig {
        max_skips: 16,
        ..RecoveryConfig::default()
    };
    let mut reach = Reach::default();
    let mut fails: Vec<String> = vec![];
    let s0: u64 = std::env::var("QA_SEED0").ok().and_then(|v| v.parse().ok()).unwrap_or(7001);
    eprintln!("QA seeds {s0}..={}", s0 + 119);
    for seed in s0..=s0 + 119 {
        let mut r = Rng((seed * 0x9e37_79b9) | 1);
        let n0 = [100u64, 200, 300][(seed % 3) as usize];
        let mut sim = settled_sender_1(cfg.clone(), n0);
        let mut adv = Chaos {
            silent_until: Duration::ZERO,
            cut: [false, false],
            lose_id: None,
            lost: false,
        };
        let mut ops: Vec<(Duration, Op)> = vec![];
        let mut sent = [0u64, n0];
        let mut hm = 0u64;
        let end = sim.t + Duration::from_secs(40);
        while sim.t < end && fails.is_empty() {
            if r.chance(15) {
                let op = gen_op(&mut r, &sim);
                ops.push((sim.t, op.clone()));
                let spent = sim.sides[S].m.skips_left == 0;
                match op {
                    Op::Full { pos, ack } => {
                        says(
                            &mut sim,
                            P,
                            "full",
                            ack,
                            json!({ "last_seq_received": pos }),
                        );
                    }
                    Op::Resume { pos, room, ack } => {
                        says(
                            &mut sim,
                            P,
                            "resume",
                            ack,
                            json!({ "last_seq_received": pos, "room": room }),
                        );
                    }
                    Op::Ack { ack } => {
                        says(&mut sim, P, "ack", ack, json!({}));
                    }
                    Op::TrimPattern => {
                        says(&mut sim, P, "full", 0, json!({ "last_seq_received": 0 }));
                        sim.tick(&mut adv);
                        says(
                            &mut sim,
                            P,
                            "resume",
                            0,
                            json!({ "last_seq_received": 0, "room": true }),
                        );
                    }
                    Op::PeerMessage { seq } => {
                        hm += 1;
                        if peer_message(&mut sim, P, seq, &format!("h{seed}-{hm}")) {
                            reach.hit("peer_message");
                            if spent {
                                reach.hit("peer_message_while_spent");
                            }
                        }
                    }
                    Op::PeerExchange { epoch } => {
                        let examined = sim.sides[S].keys.examined;
                        if peer_starts_exchange(&mut sim, P, epoch) {
                            reach.hit("peer_started_exchange");
                            let looked = sim.sides[S].keys.examined > examined;
                            if looked {
                                reach.hit("peer_message_1_examined");
                            }
                            if spent {
                                reach.hit("peer_started_exchange_while_spent");
                                if looked {
                                    reach.hit("peer_message_1_examined_while_spent");
                                }
                            }
                        }
                    }
                    Op::Silent { secs } => adv.silent_until = sim.t + Duration::from_secs(secs),
                    Op::Cut { to } => adv.cut[to] = true,
                    Op::PeerSend => {
                        if sim.send(P, &format!("p-{:05}", sent[P])) {
                            sent[P] += 1;
                        }
                    }
                    Op::SenderSend => {
                        if sim.send(S, &format!("s-{:05}", sent[S])) {
                            sent[S] += 1;
                        }
                    }
                }
            }
            if sim.sides[S].m.skips_left == 0 {
                reach.hit("budget_spent_tick");
            }
            sim.tick(&mut adv);
            for i in 0..2 {
                let _ = sim.read_all(i);
            }
            // V5: in every state that is not final, an outbox that is not empty or no proven
            // channel has an armed clock (an attach waiting for `ok` has the link task's).
            for i in 0..2 {
                let m = &sim.sides[i].m;
                let waiting = !m.is_final() && (!m.ob.items.is_empty() || !m.channel_proven());
                if waiting && m.next_deadline().is_none() && !sim.sides[i].attaching {
                    fails.push(format!(
                        "V5: side {i} at {:?} waits with no deadline: skips_left {} skips_spent_at {:?} next_out {} send_next {} (seed {seed}, last ops {:?})",
                        sim.t,
                        m.skips_left,
                        m.skips_spent_at.map(|t| t - sim.base),
                        m.next_out,
                        m.ob.send_next,
                        ops.iter().rev().take(8).collect::<Vec<_>>()
                    ));
                }
            }
        }
        if !fails.is_empty() {
            break;
        }
        // End phase: the peer is honest from here on. The sender's agent sends three messages;
        // the relay loses the LAST one once on its way (no later frame shows the gap, so only the
        // sender's retransmit clock can heal it). V4: all three arrive within the bound.
        adv.silent_until = Duration::ZERO;
        adv.cut = [false, false];
        sim.run_for(Duration::from_secs(1), &mut adv);
        let finals: Vec<String> = (0..3).map(|k| format!("final-{seed}-{k}")).collect();
        for f in &finals {
            let ok = sim.run_until(Duration::from_secs(120), &mut adv, |s| {
                s.sides[S].m.may_queue()
                    && s.sides[S].m.ob.items.len() < coagent_daemon::limits::MAX_OUTBOX_ITEMS
            });
            assert!(ok, "seed {seed}: the sender may queue again");
            assert!(sim.send(S, f), "seed {seed}: {f} accepted");
        }
        adv.lose_id = Some(finals[2].clone());
        let delivered = sim.run_until(Duration::from_secs(150), &mut adv, |s| {
            let ids = s.inbox_ids(P);
            finals.iter().all(|f| ids.contains(f))
        });
        if adv.lost {
            reach.hit("end_phase_last_frame_lost");
        }
        if !delivered {
            fails.push(format!(
                "V4 (seed {seed}): once honest, the sender's messages were not all delivered in 150 s: inbox {:?}, last frame lost {}, sender T-RTO resyncs {} (last ops {:?})",
                sim.inbox_ids(P),
                adv.lost,
                sim.sides[S].m.resyncs.get("T-RTO").copied().unwrap_or(0),
                ops.iter().rev().take(8).collect::<Vec<_>>()
            ));
            break;
        }
        while !sim.read_all(P).is_empty() {}
    }
    assert!(fails.is_empty(), "{}", fails.join("\n"));
    reach.require(
        "R6-5",
        &[
            "peer_message",
            "peer_message_while_spent",
            "peer_started_exchange",
            "peer_started_exchange_while_spent",
            "peer_message_1_examined",
            "peer_message_1_examined_while_spent",
            "budget_spent_tick",
            "end_phase_last_frame_lost",
        ],
    );
}
