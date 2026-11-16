//! QA gate round 2 (delta gate) attack tests on `State`, white-box. Each test asserts the SAFE
//! property; a red test is a finding. Tests whose name ends in `_ctl` are controls expected green.
//! Included from state.rs with `#[cfg(test)] #[path = "gate_r2_state.rs"] mod gate_r2;`.

use super::*;
use std::net::Ipv4Addr;
use std::time::Duration;

fn clk(now: Instant) -> Clock {
    Clock {
        now,
        unix: 1_700_000_000,
    }
}

fn conn_at(id: u64, ip: [u8; 4]) -> (ConnHandle, mpsc::Receiver<Out>) {
    let (tx, rx) = mpsc::channel(100_000);
    (
        ConnHandle::new(id, tx, QueueBudget::unbounded()).with_ip(IpAddr::V4(Ipv4Addr::from(ip))),
        rx,
    )
}

fn admin() -> Token {
    Token([1; 32])
}
fn st(slot: u8) -> Token {
    Token([0x10 + slot; 32])
}
fn cid(a: u8, b: u8) -> ChanId {
    let mut x = [0u8; 32];
    x[0] = a;
    x[1] = b;
    ChanId(x)
}

fn create(s: &mut State, id: ChanId, ip: [u8; 4], now: Instant) -> Result<(), Denied> {
    let (c, _rx) = conn_at(9_000, ip);
    s.chan_create(id, admin().hash(), 8, &c, clk(now))
}

fn register(s: &mut State, id: ChanId, n: u8, now: Instant) -> Result<(), Denied> {
    let ups: Vec<_> = (0..n)
        .map(|i| SlotUpdate {
            slot: i,
            token_hash: Some(st(i).hash()),
        })
        .collect();
    s.chan_slots(&id, &admin(), &ups, clk(now))
}

// ------------------------------------------------------------------------------------------------
// G1

/// Control: one address with 16 live channels plus every other table entry pending. An honest
/// create and an honest chan.slots from another address both succeed, and the attacker re-creating
/// evicts its own pending channels, not the honest one.
#[test]
fn r2_g1_one_address_live_cap_and_pending_churn_ctl() {
    let now = Instant::now();
    let mut s = State::new(Limits::default());
    let atk = [10, 0, 0, 1];
    for i in 0..16u8 {
        create(&mut s, cid(1, i), atk, now).unwrap();
        register(&mut s, cid(1, i), 1, now).unwrap();
    }
    // the 17th live one is refused
    create(&mut s, cid(1, 200), atk, now).unwrap();
    assert_eq!(
        register(&mut s, cid(1, 200), 1, now).unwrap_err().code,
        ErrorCode::Full
    );
    let mut k = 0u8;
    while s.channels.len() < s.limits.max_channels {
        create(&mut s, cid(2, k), atk, now).unwrap();
        k += 1;
    }
    let hon = cid(0x55, 0);
    create(&mut s, hon, [192, 168, 1, 7], now).expect("honest create");
    // attacker churns 200 more creates
    for j in 0..200u8 {
        create(&mut s, cid(3, j), atk, now + Duration::from_millis(1)).unwrap();
    }
    register(&mut s, hon, 2, now).expect("honest chan.slots after churn");
    s.assert_invariants();
}

/// G1 with FOUR addresses (or four IPv6 /64s; `ip_key` groups v6 by /64): 4 x 16 live channels is
/// the whole 64-channel table. Nothing is pending, so nothing can be evicted, and every honest
/// `chan.create` on the relay gets `full` until the attacker's channels idle out (30 min after the
/// last `chan.slots`, which the attacker can repeat). Safe property: the honest create succeeds.
#[test]
fn r2_g1_four_addresses_take_every_channel() {
    let now = Instant::now();
    let mut s = State::new(Limits::default());
    for a in 0..4u8 {
        for i in 0..16u8 {
            create(&mut s, cid(a, i), [10, 0, 0, a], now).unwrap();
            register(&mut s, cid(a, i), 1, now).unwrap();
        }
    }
    let r = create(&mut s, cid(0x55, 0), [192, 168, 1, 7], now);
    assert!(
        r.is_ok(),
        "FINDING G1-r2a: four addresses x 16 live channels fill the 64-channel table; honest chan.create got {r:?}"
    );
}

/// G1 behind a tunnel (Funnel / cloudflared): every client is 127.0.0.1, so the per-address live
/// cap (16) is relay-wide. An attacker makes 16 channels live with one registered slot each; every
/// honest convener's chan.slots is then refused. Safe property: honest chan.slots succeeds.
#[test]
fn r2_g1_tunnel_live_cap_is_relay_wide() {
    let now = Instant::now();
    let mut s = State::new(Limits::default());
    let tunnel = [127, 0, 0, 1];
    for i in 0..16u8 {
        create(&mut s, cid(1, i), tunnel, now).unwrap();
        register(&mut s, cid(1, i), 1, now).unwrap();
    }
    let hon = cid(0x55, 0);
    create(&mut s, hon, tunnel, now).expect("honest create still fine (table not full)");
    let r = register(&mut s, hon, 2, now);
    assert!(
        r.is_ok(),
        "FINDING G1-r2b: behind a tunnel, 16 attacker channels refuse every honest chan.slots: {r:?}"
    );
}

/// Eviction picks the pending channel whose OWNER holds the most channels, counting LIVE ones. A
/// busy honest address (10 live sessions) that creates an 11th is the top owner; attackers spread
/// over addresses holding <= 9 channels each then evict the honest convener's brand-new channel
/// instead of their own. The convener's chan.slots gets `not_found`. Safe property: the honest
/// pending channel survives an attacker create.
#[test]
fn r2_g1_eviction_targets_a_busy_honest_address() {
    let now = Instant::now();
    let mut s = State::new(Limits::default());
    let host = [192, 168, 1, 7];
    for i in 0..10u8 {
        create(&mut s, cid(0x50, i), host, now).unwrap();
        register(&mut s, cid(0x50, i), 2, now).unwrap();
    }
    let fresh = cid(0x55, 0);
    create(&mut s, fresh, host, now).unwrap(); // honest, not yet registered
    let mut a = 0u8;
    let mut k = 0u8;
    while s.channels.len() < s.limits.max_channels {
        create(&mut s, cid(0xA0 + a, k), [10, 0, 0, a], now).unwrap();
        k += 1;
        if k == 9 {
            k = 0;
            a += 1;
        }
    }
    // one more attacker create (from an address holding few channels)
    create(&mut s, cid(0xEE, 0), [10, 0, 1, 99], now + Duration::from_millis(5)).unwrap();
    let r = register(&mut s, fresh, 2, now);
    assert!(
        r.is_ok(),
        "FINDING G1-r2c: the honest convener's new channel was evicted (chan.slots -> {r:?}); \
         attackers needed {} addresses with <= 9 channels each",
        a + 1
    );
}

/// Behind a tunnel (one address) eviction is pure oldest-pending-first. An attacker that keeps
/// creating evicts an honest convener's channel once it is the oldest pending one (here after 64
/// creates, ~32 s at 2 ops/s, inside the 60 s pending window). Safe property: survives.
#[test]
fn r2_g1_tunnel_oldest_pending_honest_channel_is_evicted() {
    let t0 = Instant::now();
    let mut s = State::new(Limits::default());
    let tunnel = [127, 0, 0, 1];
    for i in 0..63u8 {
        create(&mut s, cid(1, i), tunnel, t0).unwrap();
    }
    let hon = cid(0x55, 0);
    create(&mut s, hon, tunnel, t0 + Duration::from_secs(1)).unwrap();
    for j in 0..64u8 {
        create(
            &mut s,
            cid(2, j),
            tunnel,
            t0 + Duration::from_secs(2) + Duration::from_millis(500 * u64::from(j)),
        )
        .unwrap();
    }
    let r = register(&mut s, hon, 2, t0 + Duration::from_secs(40));
    assert!(
        r.is_ok(),
        "FINDING G1-r2d (tunnel): honest pending channel evicted by churn; chan.slots -> {r:?}"
    );
}

// ------------------------------------------------------------------------------------------------
// G2

fn g2_limits() -> Limits {
    Limits {
        max_frame_bytes: 64 * 1024,
        pair_max_bytes: 256 * 1024,
        pair_max_frames: 10_000,
        channel_max_bytes: 1024 * 1024,
        total_buffer_bytes: 1024 * 1024,
        ..Limits::default()
    }
}

/// An honest channel whose receivers are offline holds ~400 KiB. An attacker with several channels
/// of ~100 KiB each (all below the victim) fills the relay-wide buffer, then keeps sending: every
/// attacker byte is admitted by silently dropping the honest channel's OLDEST frames. Neither the
/// honest sender nor its receivers are told (no error, no gap marker). Safe property: a frame the
/// relay accepted without error is not dropped before ack or age-out (or, at least, the drop is
/// signalled).
#[test]
fn r2_g2_attacker_forces_silent_eviction_of_largest_honest_channel() {
    let now = Instant::now();
    let mut s = State::new(g2_limits());
    let hon = cid(0x55, 0);
    create(&mut s, hon, [192, 168, 1, 7], now).unwrap();
    register(&mut s, hon, 3, now).unwrap();
    let (hsend, mut hrx) = conn_at(1, [192, 168, 1, 7]);
    s.chan_open(&hsend, &hon, 0, &st(0), &[], clk(now)).unwrap();
    let payload = vec![0x11u8; 50 * 1024];
    let mut seq = 0;
    for to in [1u8, 2] {
        for _ in 0..4 {
            seq += 1;
            s.chan_data(&hon, 1, 0, to, seq, &payload, clk(now)).unwrap();
        }
    }
    let honest_before = s.channels[&hon].bytes;
    while hrx.try_recv().is_ok() {}
    // attacker: channels from one address, each sender attached, receivers registered but absent
    let atk_ip = [10, 0, 0, 1];
    let mut cid_n = 0u8;
    let mut conn_id = 100u64;
    let small = vec![0x22u8; 20 * 1024];
    let mut admitted_after_full = 0;
    'outer: for _ in 0..16 {
        let ch = cid(0xA0, cid_n);
        cid_n += 1;
        create(&mut s, ch, atk_ip, now).unwrap();
        register(&mut s, ch, 2, now).unwrap();
        let (c, _rx) = conn_at(conn_id, atk_ip);
        s.chan_open(&c, &ch, 0, &st(0), &[], clk(now)).unwrap();
        for q in 1..=5u64 {
            let full_before = s.buffered_bytes + DATA_HEADER_LEN + small.len()
                > s.limits.total_buffer_bytes;
            if s.chan_data(&ch, conn_id, 0, 1, q, &small, clk(now)).is_ok() && full_before {
                admitted_after_full += 1;
            }
            if s.channels[&hon].bytes < honest_before / 2 {
                break 'outer;
            }
        }
        conn_id += 1;
        std::mem::forget(_rx);
    }
    s.assert_invariants();
    let honest_after = s.channels[&hon].bytes;
    let told: Vec<String> = std::iter::from_fn(|| hrx.try_recv().ok())
        .map(|o| match o {
            Out::Text(t) => t,
            Out::Binary(_) => "<binary>".into(),
        })
        .collect();
    assert_eq!(
        honest_after, honest_before,
        "FINDING G2-r2a: honest channel's buffered bytes went {honest_before} -> {honest_after} \
         ({} frames evicted, {admitted_after_full} attacker frames admitted while full); \
         honest sender was told: {told:?}",
        s.evicted_frames()
    );
}

/// Accounting control: after evictions, acks beyond the evicted range, a resume, a retire and a
/// sweep keep every counter exact and nothing panics.
#[test]
fn r2_g2_accounting_after_eviction_ack_resume_retire_ctl() {
    let now = Instant::now();
    let mut s = State::new(Limits {
        total_buffer_bytes: 700 * 1024,
        ..g2_limits()
    });
    let big = cid(0x55, 0);
    create(&mut s, big, [1, 1, 1, 1], now).unwrap();
    register(&mut s, big, 3, now).unwrap();
    let (bs, _brx) = conn_at(1, [1, 1, 1, 1]);
    s.chan_open(&bs, &big, 0, &st(0), &[], clk(now)).unwrap();
    for q in 1..=4u64 {
        s.chan_data(&big, 1, 0, 1, q, &[1u8; 60 * 1024], clk(now)).unwrap();
        s.chan_data(&big, 1, 0, 2, q, &[1u8; 60 * 1024], clk(now)).unwrap();
    }
    // fill the rest with a second channel, then a small third one forces eviction from `big`
    let mid = cid(0x66, 0);
    create(&mut s, mid, [2, 2, 2, 2], now).unwrap();
    register(&mut s, mid, 2, now).unwrap();
    let (ms, _mrx) = conn_at(2, [2, 2, 2, 2]);
    s.chan_open(&ms, &mid, 0, &st(0), &[], clk(now)).unwrap();
    let mut q = 0;
    while s.buffered_bytes + 1024 < s.limits.total_buffer_bytes {
        q += 1;
        if s.chan_data(&mid, 2, 0, 1, q, &[2u8; 1024], clk(now)).is_err() {
            break;
        }
    }
    let small = cid(0x77, 0);
    create(&mut s, small, [3, 3, 3, 3], now).unwrap();
    register(&mut s, small, 2, now).unwrap();
    let (ss, _srx) = conn_at(3, [3, 3, 3, 3]);
    s.chan_open(&ss, &small, 0, &st(0), &[], clk(now)).unwrap();
    for q in 1..=3u64 {
        let _ = s.chan_data(&small, 3, 0, 1, q, &[3u8; 30 * 1024], clk(now));
        s.assert_invariants();
    }
    assert!(s.evicted_frames() > 0, "precondition: eviction happened");
    // zero-length frames
    let _ = s.chan_data(&small, 3, 0, 1, 99, &[], clk(now));
    s.assert_invariants();
    // receiver of `big` attaches with resume beyond everything, acks beyond everything
    let (r1, _r1rx) = conn_at(4, [1, 1, 1, 1]);
    s.chan_open(&r1, &big, 1, &st(1), &[(0, 3)], clk(now)).unwrap();
    s.assert_invariants();
    s.chan_ack(&big, 4, 1, 0, u64::MAX);
    s.assert_invariants();
    // retire slot 2 of big
    s.chan_slots(
        &big,
        &admin(),
        &[SlotUpdate {
            slot: 2,
            token_hash: None,
        }],
        clk(now),
    )
    .unwrap();
    s.assert_invariants();
    s.sweep(clk(now + Duration::from_secs(16 * 60)));
    s.assert_invariants();
    assert_eq!(s.snapshot().2, 0);
    assert_eq!(s.snapshot().3, 0);
}

/// "Admitted only while the largest channel would still hold at least as much as the requester":
/// the check is made BEFORE each eviction, so one large front frame takes the big channel well
/// below the requester (and evicts far more than needed). Safe property: after admission the
/// evicted channel holds at least as much as the requester.
#[test]
fn r2_g2_fairness_boundary_overshoots_with_a_large_front_frame() {
    let now = Instant::now();
    let l = Limits {
        max_frame_bytes: 256 * 1024,
        pair_max_bytes: 1024 * 1024,
        channel_max_bytes: 1024 * 1024,
        total_buffer_bytes: 210 * 1024 + 2 * DATA_HEADER_LEN,
        ..Limits::default()
    };
    let mut s = State::new(l);
    let big = cid(0x55, 0);
    create(&mut s, big, [1, 1, 1, 1], now).unwrap();
    register(&mut s, big, 2, now).unwrap();
    let (bs, _brx) = conn_at(1, [1, 1, 1, 1]);
    s.chan_open(&bs, &big, 0, &st(0), &[], clk(now)).unwrap();
    s.chan_data(&big, 1, 0, 1, 1, &vec![1u8; 200 * 1024], clk(now)).unwrap();
    s.chan_data(&big, 1, 0, 1, 2, &vec![1u8; 10 * 1024], clk(now)).unwrap();
    let req = cid(0x66, 0);
    create(&mut s, req, [2, 2, 2, 2], now).unwrap();
    register(&mut s, req, 2, now).unwrap();
    let (rs, _rrx) = conn_at(2, [2, 2, 2, 2]);
    s.chan_open(&rs, &req, 0, &st(0), &[], clk(now)).unwrap();
    s.chan_data(&req, 2, 0, 1, 1, &vec![2u8; 100 * 1024], clk(now)).unwrap();
    s.assert_invariants();
    let (b, r) = (s.channels[&big].bytes, s.channels[&req].bytes);
    assert!(
        b >= r,
        "FINDING G2-r2b: after admission the evicted channel holds {b} B, the requester {r} B \
         (200 KiB evicted to admit 100 KiB)"
    );
}

// ------------------------------------------------------------------------------------------------
// G4

/// A hostile holder of slot 0 sends `pair_seq = u64::MAX` to slot 1; the convener evicts it by
/// ROTATING slot 0's token (the mechanism T2 tests) and gives the slot to a new member. `last_seq`
/// is reset only on RETIRE, so the new holder of slot 0 can never send to slot 1. Safe property:
/// the new holder's first frame is accepted.
#[test]
fn r2_g4_rotation_does_not_reset_last_seq() {
    let now = Instant::now();
    let mut s = State::new(Limits::default());
    let ch = cid(0x55, 0);
    create(&mut s, ch, [1, 1, 1, 1], now).unwrap();
    register(&mut s, ch, 2, now).unwrap();
    let (evil, _erx) = conn_at(1, [6, 6, 6, 6]);
    s.chan_open(&evil, &ch, 0, &st(0), &[], clk(now)).unwrap();
    s.chan_data(&ch, 1, 0, 1, u64::MAX, b"poison", clk(now)).unwrap();
    let new_tok = Token([0x77; 32]);
    s.chan_slots(
        &ch,
        &admin(),
        &[SlotUpdate {
            slot: 0,
            token_hash: Some(new_tok.hash()),
        }],
        clk(now),
    )
    .unwrap();
    let (newc, _nrx) = conn_at(2, [1, 1, 1, 2]);
    s.chan_open(&newc, &ch, 0, &new_tok, &[], clk(now)).unwrap();
    let r = s.chan_data(&ch, 2, 0, 1, 1, b"hello", clk(now));
    assert!(
        r.is_ok(),
        "FINDING G4-r2a: after token rotation the new holder of the slot inherits the evicted \
         member's last_seq = u64::MAX and is refused: {r:?}"
    );
}

/// Control: retire + re-register resets last_seq; the u64::MAX sender blocks only its own pair.
#[test]
fn r2_g4_retire_resets_and_poison_is_self_only_ctl() {
    let now = Instant::now();
    let mut s = State::new(Limits::default());
    let ch = cid(0x55, 0);
    create(&mut s, ch, [1, 1, 1, 1], now).unwrap();
    register(&mut s, ch, 3, now).unwrap();
    let (evil, _erx) = conn_at(1, [6, 6, 6, 6]);
    let (b, _brx) = conn_at(2, [1, 1, 1, 2]);
    s.chan_open(&evil, &ch, 0, &st(0), &[], clk(now)).unwrap();
    s.chan_open(&b, &ch, 1, &st(1), &[], clk(now)).unwrap();
    s.chan_data(&ch, 1, 0, 1, u64::MAX, b"poison", clk(now)).unwrap();
    assert_eq!(
        s.chan_data(&ch, 1, 0, 1, u64::MAX, b"x", clk(now)).unwrap_err().code,
        ErrorCode::BadRequest
    );
    // other pairs unaffected
    s.chan_data(&ch, 2, 1, 0, 1, b"ok", clk(now)).unwrap();
    s.chan_data(&ch, 2, 1, 2, 1, b"ok", clk(now)).unwrap();
    s.chan_data(&ch, 1, 0, 2, 1, b"ok", clk(now)).unwrap();
    // the honest receiver's acks free the poison frame
    s.chan_ack(&ch, 2, 1, 0, u64::MAX);
    // retire slot 0 and re-register it: counter reset
    s.chan_slots(&ch, &admin(), &[SlotUpdate { slot: 0, token_hash: None }], clk(now))
        .unwrap();
    s.chan_slots(
        &ch,
        &admin(),
        &[SlotUpdate {
            slot: 0,
            token_hash: Some(st(0).hash()),
        }],
        clk(now),
    )
    .unwrap();
    let (n, _nrx) = conn_at(3, [1, 1, 1, 3]);
    s.chan_open(&n, &ch, 0, &st(0), &[], clk(now)).unwrap();
    s.chan_data(&ch, 3, 0, 1, 1, b"fresh", clk(now)).unwrap();
    s.assert_invariants();
    assert!(s.channels[&ch].last_seq.len() <= SLOTS * SLOTS);
}

/// Documents (does not judge) what an honest sender whose counter restarted sees: refused for
/// good on that pair, until the convener retires the slot. Design 03 §4.5 says the outbox (and
/// so the sequence) is persisted, so this is reachable only on lost client state.
#[test]
fn r2_g4_counter_restart_is_refused_until_retire_info() {
    let now = Instant::now();
    let mut s = State::new(Limits::default());
    let ch = cid(0x55, 0);
    create(&mut s, ch, [1, 1, 1, 1], now).unwrap();
    register(&mut s, ch, 2, now).unwrap();
    let (a, _arx) = conn_at(1, [1, 1, 1, 1]);
    s.chan_open(&a, &ch, 0, &st(0), &[], clk(now)).unwrap();
    s.chan_data(&ch, 1, 0, 1, 7, b"x", clk(now)).unwrap();
    s.chan_detach(&ch, 0, 1, clk(now));
    let (a2, _a2rx) = conn_at(2, [1, 1, 1, 1]);
    s.chan_open(&a2, &ch, 0, &st(0), &[], clk(now)).unwrap();
    assert_eq!(
        s.chan_data(&ch, 2, 0, 1, 1, b"restart", clk(now)).unwrap_err().code,
        ErrorCode::BadRequest
    );
}
