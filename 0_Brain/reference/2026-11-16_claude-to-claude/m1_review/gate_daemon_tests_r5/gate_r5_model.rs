//! QA gate round 5 (the short check after the r4 fix round, head 0e0e26b): model attacks on the
//! two rules the fix round built, on the branch's own model harness (`tests/support/model.rs`).
//!
//! G5-1   R4-8's new skip budget: a hostile PEER (its own keys) states a low position, then
//!        trims the sender's in-flight skips with a `resume` whose position is above the
//!        envelope's acknowledgement, then sends nothing that acknowledges forward. Asserts the
//!        safe property (V5: a waiting state has a deadline).
//! G5-1c  The same forged frames, then the peer is honest from then on (its next frame carries the
//!        counter the sender expects): the message must still be delivered within V4's 120 s.
//! G5-2   Measurement: what a hostile peer's `full`/`room` pairs make the sender emit.
//! G5-3   R4-1: a session fresh from pairing whose responder is absent for 10 minutes: what the
//!        initiator emits, and delivery when the responder arrives.
//! G5-4   R4-8 status: `desync` after the pump has passed every missing number with no held item
//!        after the gap.
#![allow(clippy::needless_range_loop)]
mod common;
#[path = "support/model.rs"]
mod model;

use std::time::Duration;

use coagent_daemon::recovery::RecoveryConfig;
use coagent_relay::frame::decode_data;
use coagent_relay::state::Out;
use model::*;
use serde_json::json;

fn cfg() -> RecoveryConfig {
    RecoveryConfig::default()
}

/// Side 0 sends `n` messages, all delivered and acknowledged (outbox empty again).
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

/// The peer (slot 1) sends nothing of its own toward side 0: every data frame from slot 1 is
/// dropped (the forged controls are fed directly by `hostile_control`, past the relay). Counts
/// the data frames side 0 emits toward side 1.
struct SilentPeer {
    silent: bool,
    from0: u64,
}
impl Adversary for SilentPeer {
    fn on_deliver(&mut self, to: usize, item: &Out, _t: Duration) -> Verdict {
        match (to, from_slot(item)) {
            (0, Some(1)) if self.silent => Verdict::Drop,
            (1, Some(0)) => {
                self.from0 += 1;
                Verdict::Deliver
            }
            _ => Verdict::Deliver,
        }
    }
}

fn state(sim: &Sim, i: usize) -> String {
    let m = &sim.sides[i].m;
    format!(
        "outbox {} in_flight {} skips_left {} desync_out {} pos {:?} proven {} connected {} peer_full {} next_deadline {:?} lost_outbound {} resyncs {:?}",
        m.ob.items.len(),
        m.in_flight.len(),
        m.skips_left,
        m.desync_out,
        m.pos,
        m.channel_proven(),
        m.connected(),
        m.peer_full,
        m.next_deadline().map(|d| d.saturating_duration_since(sim.now())),
        m.n.lost_outbound,
        m.resyncs
    )
}

/// A forged control from the peer (slot 1) with its own keys. The peer's counter is set to what side
/// 0 expects next: the frames `SilentPeer` dropped were never sent by this (hostile) peer.
fn forge(sim: &mut Sim, kind: &str, ack: u64, body: serde_json::Value) {
    let want = sim.sides[0].keys.live.as_ref().map(|c| c.recv);
    if let (Some(w), Some(ch)) = (want, sim.sides[1].keys.live.as_mut()) {
        ch.send = w;
    }
    assert!(sim.hostile_control(1, kind, ack, body), "forge {kind}");
}

/// The forged sequence: `full` 0, `room` 0 (the pump restarts at 1 with 256 skips), then two
/// `resume`s whose stated position is above the envelope's acknowledgement (0), each trimming the
/// skips in flight without refilling the budget.
fn forge_low_position_and_trim(sim: &mut Sim, adv: &mut SilentPeer) {
    forge(sim, "full", 0, json!({ "last_seq_received": 0 }));
    sim.run_for(Duration::from_millis(300), adv);
    forge(
        sim,
        "resume",
        0,
        json!({ "last_seq_received": 0, "room": true }),
    );
    sim.run_for(Duration::from_millis(300), adv);
    eprintln!("G5-1 after full/room at 0: {}", state(sim, 0));
    for _ in 0..4 {
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
        sim.run_for(Duration::from_millis(300), adv);
        eprintln!(
            "G5-1 after resume at {top} (envelope ack 0): {}",
            state(sim, 0)
        );
    }
}

#[test]
fn g5_1_r4_8_peer_trims_skips_without_acknowledging_waiting_state_has_a_deadline() {
    let mut sim = sent_and_acknowledged(300);
    let mut adv = SilentPeer {
        silent: true,
        from0: 0,
    };
    forge_low_position_and_trim(&mut sim, &mut adv);
    // The sender's agent queues one more message.
    assert!(sim.send(0, "m0-after"));
    sim.run_for(Duration::from_millis(500), &mut adv);
    let before = adv.from0;
    eprintln!("G5-1 after the send: {}", state(&sim, 0));
    let mut no_deadline_since: Option<Duration> = None;
    let mut worst = Duration::ZERO;
    let end = sim.t + Duration::from_secs(600);
    while sim.t < end {
        sim.tick(&mut adv);
        let m = &sim.sides[0].m;
        let waiting = !m.is_final() && (!m.ob.items.is_empty() || !m.channel_proven());
        if waiting && m.next_deadline().is_none() {
            let s = *no_deadline_since.get_or_insert(sim.t);
            worst = worst.max(sim.t - s);
        } else {
            no_deadline_since = None;
        }
    }
    eprintln!(
        "G5-1 600 s later: frames side 0 emitted toward the peer in that time {}; longest stretch waiting with no deadline {:?}; {}",
        adv.from0 - before,
        worst,
        state(&sim, 0)
    );
    assert!(
        worst < Duration::from_secs(120),
        "V5 (R4-8 rule): a peer that stated a low position and trimmed the skips in flight with a position above its acknowledgement left the sender waiting with no deadline for {worst:?}: {}",
        state(&sim, 0)
    );
}

#[test]
fn g5_1c_same_forgery_then_an_honest_peer_still_gets_the_message() {
    let mut sim = sent_and_acknowledged(300);
    let mut adv = SilentPeer {
        silent: true,
        from0: 0,
    };
    forge_low_position_and_trim(&mut sim, &mut adv);
    assert!(sim.send(0, "m0-after"));
    // From here the peer is honest: its next frame carries the counter side 0 expects (the frames
    // the test dropped were never sent by this peer).
    let want = sim.sides[0].keys.live.as_ref().map(|c| c.recv);
    if let (Some(w), Some(ch)) = (want, sim.sides[1].keys.live.as_mut()) {
        ch.send = w;
    }
    let mut honest = SilentPeer {
        silent: false,
        from0: 0,
    };
    let t0 = sim.t;
    let ok = sim.run_until(Duration::from_secs(120), &mut honest, |s| {
        s.inbox_ids(1).contains(&"m0-after".to_string())
    });
    eprintln!(
        "G5-1c (peer honest from now on): delivered {ok} in {:?}; {}",
        sim.t - t0,
        state(&sim, 0)
    );
    assert!(
        ok,
        "V4 (R4-8 rule): after the peer's forged positions, an honest peer did not get the queued message within 120 s: {}",
        state(&sim, 0)
    );
}

#[test]
fn g5_2_measure_hostile_full_room_pairs() {
    let mut sim = sent_and_acknowledged(1000);
    let mut adv = SilentPeer {
        silent: false,
        from0: 0,
    };
    let before = adv.from0;
    let pairs = 50;
    for _ in 0..pairs {
        assert!(sim.hostile_control(1, "full", 0, json!({ "last_seq_received": 0 })));
        sim.tick(&mut adv);
        assert!(sim.hostile_control(
            1,
            "resume",
            0,
            json!({ "last_seq_received": 0, "room": true })
        ));
        sim.run_for(Duration::from_millis(200), &mut adv);
    }
    let emitted = adv.from0 - before;
    eprintln!(
        "G5-2: {pairs} forged full/room pairs (100 control frames) in {:?}: side 0 emitted {emitted} data frames ({} per pair); lost_outbound {}; {}",
        Duration::from_millis(200 * pairs + 100 * pairs),
        emitted / pairs,
        sim.sides[0].m.n.lost_outbound,
        state(&sim, 0)
    );
    let per_pair = emitted / pairs;
    assert!(
        per_pair <= sim.cfg.inflight_frames as u64 + 16,
        "G5-2: more than the in-flight limit per forged pair: {per_pair}"
    );
}

/// Counts the data frames side 0 sends toward slot 1.
struct CountFrom0 {
    n: u64,
}
impl Adversary for CountFrom0 {
    fn on_deliver(&mut self, to: usize, item: &Out, _t: Duration) -> Verdict {
        if to == 1 && from_slot(item) == Some(0) {
            self.n += 1;
        }
        Verdict::Deliver
    }
}

#[test]
fn g5_3_r4_1_fresh_session_responder_absent_10_minutes() {
    let mut sim = Sim::new_at(cfg(), [true, true]);
    // The responder's daemon does not attach for 10 minutes (as the branch's M04 test keeps a peer
    // away).
    sim.sides[1].m.reconnect_at = None;
    assert!(sim.send(0, "m0-early"));
    assert!(sim.send(1, "m1-early"));
    let mut adv = CountFrom0 { n: 0 };
    sim.run_for(Duration::from_secs(600), &mut adv);
    let m0 = &sim.sides[0].m;
    eprintln!(
        "G5-3 after 600 s with the responder away: initiator resyncs {:?}, reconnects {}, relay refusals {}, attaches {}, frames toward the absent slot {}; responder attaches {}; initiator {}",
        m0.resyncs,
        m0.n.reconnects,
        sim.sides[0].relay_refused,
        sim.sides[0].attach_times.len(),
        adv.n,
        sim.sides[1].attach_times.len(),
        state(&sim, 0)
    );
    let now = sim.now();
    sim.sides[1].m.reconnect_at = Some(now);
    let t0 = sim.t;
    let ok = sim.run_until(Duration::from_secs(120), &mut adv, |s| {
        s.inbox_ids(1).contains(&"m0-early".to_string())
            && s.inbox_ids(0).contains(&"m1-early".to_string())
    });
    eprintln!(
        "G5-3: after the responder may attach: delivered both ways {ok} in {:?}; initiator {}; responder {}",
        sim.t - t0,
        state(&sim, 0),
        state(&sim, 1)
    );
    assert!(
        ok,
        "G5-3 (V4): a fresh session whose responder came 10 minutes late delivers within 120 s"
    );
}

#[test]
fn g5_4_r4_8_desync_status_after_the_pump_passed_the_gap() {
    let mut sim = sent_and_acknowledged(300);
    let mut adv = SilentPeer {
        silent: false,
        from0: 0,
    };
    forge(&mut sim, "full", 0, json!({ "last_seq_received": 0 }));
    sim.run_for(Duration::from_millis(300), &mut adv);
    forge(
        &mut sim,
        "resume",
        0,
        json!({ "last_seq_received": 0, "room": true }),
    );
    sim.run_for(Duration::from_secs(30), &mut adv);
    let m = &sim.sides[0].m;
    eprintln!(
        "G5-4: 30 s after the peer stated 0, no message queued: {}",
        state(&sim, 0)
    );
    assert!(
        !m.desync_out || m.next_out < m.ob.send_next,
        "G5-4 (row 54 status): the pump passed every missing number (next_out {} send_next {}) but desync is still shown",
        m.next_out,
        m.ob.send_next
    );
}
