//! QA gate round 6 (the one short check after the r5 fix round, head 242de86): model attacks on
//! row 54's new clock (addendum 12, R5-1 choice (b)), on the branch's own model harness
//! (`tests/support/model.rs`: two REAL `recovery::Machine`s).
//!
//! G6-1  The clock, exercised over and over: after EVERY new channel the hostile peer repeats the
//!       r5 check's trim pattern (full 0, room 0, two `resume`s above the envelope ack 0), silent
//!       meanwhile; then lets the reconnect through. Asserts on every cycle that the wait had a
//!       deadline (V5), that the RESYNC came from row 54's clock (skips waiting before the tick,
//!       nothing in flight), the interval, the frames per cycle (bounded), and V4 at the end.
//! G6-2  The builder's own "(a) alone leaves a gap" ordering: ONE forged acknowledgement at the top
//!       raises `peer_acked`; from then on the peer is HONEST. Its acknowledgements no longer move
//!       forward, so they trim without refilling. Asserts V5 and V4 (honest peer from the second
//!       frame on).
//! G6-3  A generated property of the check's own: hostile peer alphabet incl. sequenced messages
//!       (in order, gap, duplicate, u64::MAX), acknowledgements (control and data), positions from
//!       {0, 1, half, top, above top, u64::MAX, in-flight top, next_out-1, random}, `full`/`room`,
//!       long silences, relay drops and cuts; 120 seeds. V5 after every tick; V4 once honest;
//!       counts the clock's fires.
#![allow(clippy::needless_range_loop)]
mod common;
#[path = "support/model.rs"]
mod model;

use std::collections::BTreeSet;
use std::time::Duration;

use coagent_daemon::recovery::RecoveryConfig;
use coagent_relay::frame::decode_data;
use coagent_relay::state::Out;
use model::*;
use serde_json::json;

fn cfg() -> RecoveryConfig {
    RecoveryConfig::default()
}

fn sent_and_acknowledged(n: u64) -> Sim {
    let mut sim = Sim::new(cfg());
    connect(&mut sim);
    let mut k = 0;
    while k < n {
        let batch = (n - k).min(200);
        for _ in 0..batch {
            assert!(sim.send(0, &format!("m0-{k:05}")));
            k += 1;
        }
        let ok = sim.run_until(Duration::from_secs(60), &mut Honest, |s| {
            s.sides[0].m.ob.items.is_empty()
        });
        assert!(ok, "setup: batch delivered and acknowledged");
        while !sim.read_all(1).is_empty() {}
    }
    sim.run_for(Duration::from_secs(1), &mut Honest);
    sim
}

fn from_slot(o: &Out) -> Option<u8> {
    if let Out::Binary(b) = o {
        decode_data(b, usize::MAX).ok().map(|d| d.from_slot)
    } else {
        None
    }
}

/// Drops the peer's (slot 1) frames toward side 0 while `silent`, and `drop_n` more of them;
/// cuts side `cut_to` once when set; counts side 0's frames toward slot 1.
struct Peer {
    silent: bool,
    drop_n: u32,
    cut_to: Option<usize>,
    from0: u64,
    heard: u64,
}
impl Peer {
    fn new(silent: bool) -> Peer {
        Peer {
            silent,
            drop_n: 0,
            cut_to: None,
            from0: 0,
            heard: 0,
        }
    }
}
impl Adversary for Peer {
    fn on_deliver(&mut self, to: usize, item: &Out, _t: Duration) -> Verdict {
        match (to, from_slot(item)) {
            (0, Some(1)) => {
                if self.silent {
                    return Verdict::Drop;
                }
                if self.drop_n > 0 {
                    self.drop_n -= 1;
                    return Verdict::Drop;
                }
                self.heard += 1;
                Verdict::Deliver
            }
            (1, Some(0)) => {
                self.from0 += 1;
                Verdict::Deliver
            }
            _ => Verdict::Deliver,
        }
    }
    fn cut(&mut self, to: usize, _t: Duration) -> bool {
        if self.cut_to == Some(to) {
            self.cut_to = None;
            return true;
        }
        false
    }
}

fn state(sim: &Sim, i: usize) -> String {
    let m = &sim.sides[i].m;
    format!(
        "outbox {} in_flight {} skips_left {} skips_spent_at {:?} next_out {} send_next {} pos {:?} proven {} connected {} peer_full {} next_deadline {:?} lost_outbound {} resyncs {:?}",
        m.ob.items.len(),
        m.in_flight.len(),
        m.skips_left,
        m.skips_spent_at.map(|t| t - sim.base),
        m.next_out,
        m.ob.send_next,
        m.pos,
        m.channel_proven(),
        m.connected(),
        m.peer_full,
        m.next_deadline().map(|d| d.saturating_duration_since(sim.now())),
        m.n.lost_outbound,
        m.resyncs
    )
}

/// The peer's counter set to what side 0 expects (frames the test dropped were never sent).
fn align(sim: &mut Sim) {
    let want = sim.sides[0].keys.live.as_ref().map(|c| (c.id, c.recv));
    if let (Some((id, w)), Some(ch)) = (want, sim.sides[1].keys.live.as_mut()) {
        if ch.id == id {
            ch.send = w;
        }
    }
}

fn forge(sim: &mut Sim, kind: &str, ack: u64, body: serde_json::Value) -> bool {
    align(sim);
    sim.hostile_control(1, kind, ack, body)
}

/// V5 on both sides (the link task's attach clock, `attaching`, counted as the builder's
/// property counts it; item 3 of the check rules on that clock separately).
fn v5(sim: &Sim) -> Option<String> {
    for i in 0..2 {
        let m = &sim.sides[i].m;
        let waiting = !m.is_final() && (!m.ob.items.is_empty() || !m.channel_proven());
        if waiting && m.next_deadline().is_none() && !sim.sides[i].attaching {
            return Some(format!("side {i} at {:?}: {}", sim.t, state(sim, i)));
        }
    }
    None
}

fn trim_pattern(sim: &mut Sim, adv: &mut Peer) {
    forge(sim, "full", 0, json!({ "last_seq_received": 0 }));
    sim.run_for(Duration::from_millis(300), adv);
    forge(
        sim,
        "resume",
        0,
        json!({ "last_seq_received": 0, "room": true }),
    );
    for _ in 0..3 {
        sim.run_for(Duration::from_millis(300), adv);
        let top = sim.sides[0].m.in_flight.back().map(|x| x.0).unwrap_or(0);
        if top == 0 {
            break;
        }
        forge(
            sim,
            "resume",
            0,
            json!({ "last_seq_received": top, "room": false }),
        );
    }
    sim.run_for(Duration::from_millis(300), adv);
}

#[test]
fn g6_1_row54_clock_fires_after_every_new_channel_and_stays_bounded() {
    let cycles = 12;
    let mut sim = sent_and_acknowledged(1000);
    let mut adv = Peer::new(false);
    let mut fails: Vec<String> = vec![];
    let mut fired_by_clock = 0;
    let mut per_cycle: Vec<(u64, Duration, Duration)> = vec![];
    let t_start = sim.t;
    let f_start = adv.from0;
    for k in 0..cycles {
        // Let the reconnect through until the channel is LIVE again (the peer's honest position).
        adv.silent = false;
        let up = sim.run_until(Duration::from_secs(120), &mut adv, |s| {
            s.sides[0].m.connected() && s.sides[1].m.connected()
        });
        if !up {
            fails.push(format!("cycle {k}: no LIVE channel within 120 s: {}", state(&sim, 0)));
            break;
        }
        let c0 = sim.t;
        let f0 = adv.from0;
        adv.silent = true;
        trim_pattern(&mut sim, &mut adv);
        assert!(sim.send(0, &format!("m0-cyc{k:02}")));
        let r0 = sim.sides[0].m.resyncs.get("T-RTO").copied().unwrap_or(0);
        let spent = sim.sides[0].m.skips_spent_at;
        let mut fired = false;
        let end = sim.t + Duration::from_secs(60);
        while sim.t < end {
            let waiting_before =
                sim.sides[0].skips_waiting_now() && sim.sides[0].m.in_flight.is_empty();
            sim.tick(&mut adv);
            if let Some(f) = v5(&sim) {
                if fails.len() < 5 {
                    fails.push(format!("cycle {k}: V5: {f}"));
                }
            }
            if sim.sides[0].m.resyncs.get("T-RTO").copied().unwrap_or(0) > r0 {
                fired = true;
                if waiting_before {
                    fired_by_clock += 1;
                }
                break;
            }
        }
        let interval = spent
            .map(|s| sim.now().saturating_duration_since(s))
            .unwrap_or_default();
        per_cycle.push((adv.from0 - f0, interval, sim.t - c0));
        if !fired {
            fails.push(format!(
                "cycle {k}: no RESYNC within 60 s of the trim pattern: {}",
                state(&sim, 0)
            ));
            break;
        }
    }
    let total = sim.t - t_start;
    let frames = adv.from0 - f_start;
    eprintln!(
        "G6-1: {} cycles, fired by row 54's clock {fired_by_clock}; per cycle (frames side 0 -> peer, spent->RESYNC, cycle time): {per_cycle:?}",
        per_cycle.len()
    );
    eprintln!(
        "G6-1: total {total:?}, frames side 0 -> peer {frames} ({:.1}/s); T-RTO resyncs {:?}; reconnects {}",
        frames as f64 / total.as_secs_f64(),
        sim.sides[0].m.resyncs,
        sim.sides[0].m.n.reconnects
    );
    // The peer turns honest: every cycle's message arrives within V4's 120 s.
    adv.silent = false;
    align(&mut sim);
    let want: Vec<String> = (0..per_cycle.len())
        .map(|k| format!("m0-cyc{k:02}"))
        .collect();
    let mut got: BTreeSet<String> = BTreeSet::new();
    let t0 = sim.t;
    let ok = loop {
        got.extend(sim.read_all(1));
        if want.iter().all(|w| got.contains(w)) {
            break true;
        }
        if sim.t >= t0 + Duration::from_secs(120) {
            break false;
        }
        sim.tick(&mut adv);
        if let Some(f) = v5(&sim) {
            if fails.len() < 5 {
                fails.push(format!("honest: V5: {f}"));
            }
        }
    };
    eprintln!(
        "G6-1 honest: delivered all {} {ok} in {:?}; {}",
        want.len(),
        sim.t - t0,
        state(&sim, 0)
    );
    if !ok {
        fails.push(format!("V4: not delivered in 120 s: {}", state(&sim, 0)));
    }
    for f in &fails {
        eprintln!("{f}");
    }
    assert!(fails.is_empty(), "G6-1 (V5/V4, row 54 clock): {}", fails[0]);
    assert_eq!(
        fired_by_clock, cycles,
        "G6-1: every cycle's RESYNC came from row 54's clock"
    );
    for (f, iv, _) in &per_cycle {
        assert!(*f <= 300, "G6-1: {f} frames in one cycle (bound: 256 skips + controls)");
        assert!(
            *iv >= sim.cfg.rto && *iv <= sim.cfg.rto + Duration::from_millis(500),
            "G6-1: the clock fired {iv:?} after the budget was spent (row 54: T-RTO's value, {:?})",
            sim.cfg.rto
        );
    }
}

#[test]
fn g6_2_one_forged_ack_at_the_top_then_an_honest_peer() {
    let mut sim = sent_and_acknowledged(1000);
    let mut adv = Peer::new(true);
    forge(&mut sim, "full", 0, json!({ "last_seq_received": 0 }));
    sim.run_for(Duration::from_millis(300), &mut adv);
    forge(
        &mut sim,
        "resume",
        0,
        json!({ "last_seq_received": 0, "room": true }),
    );
    sim.run_for(Duration::from_millis(300), &mut adv);
    eprintln!("G6-2 after full/room 0: {}", state(&sim, 0));
    // One forged acknowledgement at u64::MAX (clamped to the top).
    forge(&mut sim, "ack", u64::MAX, json!({}));
    sim.run_for(Duration::from_millis(100), &mut adv);
    eprintln!("G6-2 after the forged ack: {}", state(&sim, 0));
    assert!(sim.send(0, "m0-after"));
    // Honest from here on.
    align(&mut sim);
    adv.silent = false;
    let mut worst = Duration::ZERO;
    let mut since: Option<Duration> = None;
    let mut saw_waiting = false;
    let t0 = sim.t;
    let mut ok = false;
    let mut got: BTreeSet<String> = BTreeSet::new();
    while sim.t < t0 + Duration::from_secs(120) {
        sim.tick(&mut adv);
        got.extend(sim.read_all(1));
        if sim.sides[0].skips_waiting_now() && sim.sides[0].m.in_flight.is_empty() {
            saw_waiting = true;
        }
        if v5(&sim).is_some() {
            let s = *since.get_or_insert(sim.t);
            worst = worst.max(sim.t - s);
        } else {
            since = None;
        }
        if got.contains("m0-after") {
            ok = true;
            break;
        }
    }
    eprintln!(
        "G6-2: honest peer after one forged ack: delivered {ok} in {:?}; budget spent with nothing in flight seen {saw_waiting}; longest wait with no deadline {worst:?}; {}",
        sim.t - t0,
        state(&sim, 0)
    );
    assert!(
        worst.is_zero(),
        "G6-2 (V5): waited {worst:?} with no deadline"
    );
    assert!(
        ok,
        "G6-2 (V4): an honest peer after one forged ack did not get the message in 120 s: {}",
        state(&sim, 0)
    );
}

#[derive(Debug, Clone)]
enum P {
    Full(u64, u64),
    Resume(u64, bool, u64),
    Ack(u64),
    Msg(u64),
    Trim,
    Silent(u64),
    Drop(u32),
    Cut(usize),
    HonestSend,
    SenderSend,
}

fn num(r: &mut Rng, sim: &Sim) -> u64 {
    let m = &sim.sides[0].m;
    let top = m.ob.send_next.saturating_sub(1);
    match r.below(9) {
        0 => 0,
        1 => 1,
        2 => top / 2,
        3 => top,
        4 => top + 1 + r.below(1000),
        5 => u64::MAX,
        6 => m.in_flight.back().map(|x| x.0).unwrap_or(0),
        7 => m.next_out.saturating_sub(1),
        _ => r.below(top + 1),
    }
}

#[test]
fn g6_3_generated_hostile_peer_with_messages_and_long_silences() {
    let mut fails: Vec<String> = vec![];
    let (mut clock_fired, mut exhausted_idle, mut cuts, mut msgs) = (0u64, 0u64, 0u64, 0u64);
    let seeds = 120u64;
    for seed in 1..=seeds {
        let mut r = Rng((seed * 2_654_435_761) | 1);
        let n0 = [100u64, 400, 700][(seed % 3) as usize];
        let mut sim = sent_and_acknowledged(n0);
        let mut adv = Peer::new(false);
        let mut silent_until = Duration::ZERO;
        let mut sent = [n0, 0u64];
        let mut got: [BTreeSet<String>; 2] = Default::default();
        let mut ops: Vec<(Duration, P)> = vec![];
        let end = sim.t + Duration::from_secs(90);
        while sim.t < end {
            if r.chance(10) {
                let op = match r.below(22) {
                    0..=2 => P::Full(num(&mut r, &sim), num(&mut r, &sim)),
                    3..=6 => P::Resume(num(&mut r, &sim), r.chance(50), num(&mut r, &sim)),
                    7..=8 => P::Ack(num(&mut r, &sim)),
                    9..=10 => P::Msg(r.below(5)),
                    11..=12 => P::Trim,
                    13..=14 => P::Silent(5 + r.below(40)),
                    15 => P::Drop(1 + r.below(6) as u32),
                    16 => P::Cut(r.below(2) as usize),
                    17..=18 => P::HonestSend,
                    _ => P::SenderSend,
                };
                ops.push((sim.t, op.clone()));
                match op {
                    P::Full(pos, ack) => {
                        forge(&mut sim, "full", ack, json!({ "last_seq_received": pos }));
                    }
                    P::Resume(pos, room, ack) => {
                        forge(
                            &mut sim,
                            "resume",
                            ack,
                            json!({ "last_seq_received": pos, "room": room }),
                        );
                    }
                    P::Ack(a) => {
                        forge(&mut sim, "ack", a, json!({}));
                    }
                    P::Msg(kind) => {
                        let next = sim.sides[0].m.ib.recv_upto + 1;
                        let seq = match kind {
                            0 => next,
                            1 => next + 1 + r.below(10),
                            2 => next.saturating_sub(1),
                            3 => u64::MAX,
                            _ => 1 << 62,
                        };
                        align(&mut sim);
                        if sim.hostile_message(1, seq, &format!("h-{seed}-{}", ops.len())) {
                            msgs += 1;
                            // The peer numbered this message itself: its own machine's next number
                            // moves past it (else its later honest messages would reuse the
                            // number and be dropped as duplicates: the check's own instrument
                            // error, first run).
                            // G6_NO_FIX=1 reproduces the first run's instrument (diagnosis).
                            if kind == 0
                                && sim.sides[0].m.ib.recv_upto >= seq
                                && std::env::var("G6_NO_FIX").is_err()
                            {
                                let s = &mut sim.sides[1].m.ob.send_next;
                                *s = (*s).max(seq + 1);
                            }
                        }
                    }
                    P::Trim => {
                        silent_until = silent_until.max(sim.t + Duration::from_secs(25));
                        adv.silent = true;
                        trim_pattern(&mut sim, &mut adv);
                    }
                    P::Silent(s) => silent_until = silent_until.max(sim.t + Duration::from_secs(s)),
                    P::Drop(n) => adv.drop_n += n,
                    P::Cut(to) => {
                        adv.cut_to = Some(to);
                        cuts += 1;
                    }
                    P::HonestSend => {
                        if sim.send(1, &format!("m1-{:05}", sent[1])) {
                            sent[1] += 1;
                        }
                    }
                    P::SenderSend => {
                        if sim.send(0, &format!("m0-{:05}", sent[0])) {
                            sent[0] += 1;
                        }
                    }
                }
            }
            adv.silent = sim.t < silent_until;
            let before = (
                sim.sides[0].skips_waiting_now() && sim.sides[0].m.in_flight.is_empty(),
                sim.sides[0].m.resyncs.get("T-RTO").copied().unwrap_or(0),
            );
            if before.0 {
                exhausted_idle += 1;
            }
            sim.tick(&mut adv);
            for i in 0..2 {
                got[i].extend(sim.read_all(i));
            }
            if let Some(f) = v5(&sim) {
                if fails.len() < 5 {
                    fails.push(format!(
                        "V5 seed {seed}: {f}; last ops {:?}",
                        ops.iter().rev().take(8).collect::<Vec<_>>()
                    ));
                }
            }
            if before.0 && sim.sides[0].m.resyncs.get("T-RTO").copied().unwrap_or(0) > before.1 {
                clock_fired += 1;
            }
        }
        // Honest from here.
        adv.silent = false;
        adv.drop_n = 0;
        adv.cut_to = None;
        align(&mut sim);
        let want: [Vec<String>; 2] = [0, 1].map(|i| {
            sim.sides[i]
                .m
                .ob
                .items
                .iter()
                .filter(|o| o.kind != "coagent.skip")
                .map(|o| o.id.clone())
                .collect()
        });
        let t0 = sim.t;
        let mut ok = false;
        while sim.t < t0 + Duration::from_secs(120) {
            sim.tick(&mut adv);
            for i in 0..2 {
                got[i].extend(sim.read_all(i));
            }
            if let Some(f) = v5(&sim) {
                if fails.len() < 5 {
                    fails.push(format!("V5 honest seed {seed}: {f}"));
                }
            }
            if (0..2).all(|i| want[i].iter().all(|w| got[i ^ 1].contains(w))) {
                ok = true;
                break;
            }
        }
        if !ok && fails.len() < 5 {
            fails.push(format!(
                "V4 seed {seed}: not delivered in 120 s once honest: missing {:?}; side 0 {}; side 1 {}; last ops {:?}",
                (0..2)
                    .flat_map(|i| want[i].iter().filter(|w| !got[i ^ 1].contains(*w)).cloned().collect::<Vec<_>>())
                    .collect::<Vec<_>>(),
                state(&sim, 0),
                state(&sim, 1),
                ops.iter().rev().take(8).collect::<Vec<_>>()
            ));
        }
    }
    eprintln!(
        "G6-3: {seeds} seeds; ticks with the budget spent and nothing in flight {exhausted_idle}; row 54 clock fired {clock_fired}; hostile messages {msgs}; cuts {cuts}"
    );
    for f in &fails {
        eprintln!("{f}");
    }
    assert!(fails.is_empty(), "G6-3 (V5/V4 hostile peer): {}", fails[0]);
    assert!(clock_fired > 0, "G6-3: row 54's clock never fired (reach)");
}
