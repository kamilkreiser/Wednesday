//! QA gate, round 2 (DELTA gate at bcb55e0). Written by the gate, not the builder.
//! `gate_r2_fail_*` asserts a property the code should have and FAILS at bcb55e0.
//! `gate_r2_demo_*` PASSES and shows a behaviour discussed in the r2 verdict.
//! `gate_r2_ok_*` is an attack that was refused.
mod common;

use std::time::{Duration, Instant};

use coagent_crypto::channel_map::{ChannelMap, MapEvent};
use coagent_crypto::identity::{is_small_order, DeviceIdentity};
use coagent_crypto::kk::{kk_initiate, kk_respond};
use coagent_crypto::sas::{PairVerification, VerifyStatus, MAX_ATTEMPTS};
use coagent_crypto::words::encode31;
use coagent_crypto::CryptoError;
use coagent_proto::bytes::Digest32;
use coagent_proto::canonical;
use coagent_proto::record::{RecordKind, SasMsg, SasStep};
use common::*;
use curve25519_dalek::constants::EIGHT_TORSION;
use sha2::{Digest, Sha256};

const W: Duration = Duration::from_secs(120);
const HA: [u8; 32] = [0xa1; 32]; // h of the A<->M channel
const HB: [u8; 32] = [0xb2; 32]; // h of the M<->B channel

fn msg(step: SasStep, v: [u8; 32]) -> SasMsg {
    SasMsg {
        step,
        value: Digest32(v),
    }
}

// The ceremony formulas, written out independently (as the middleman would compute them).
fn commit_of(h: &[u8; 32], r_c: &[u8; 32]) -> [u8; 32] {
    let mut d = Sha256::new();
    d.update(b"coagent-sas-commit-v1");
    d.update([0u8, 0x01]);
    d.update(h);
    d.update(r_c);
    d.finalize().into()
}
fn words_of(h: &[u8; 32], r_c: &[u8; 32], r_r: &[u8; 32]) -> [&'static str; 3] {
    let mut d = Sha256::new();
    d.update(b"coagent-sas-v1");
    d.update([0u8]);
    d.update(h);
    d.update(r_c);
    d.update(r_r);
    let o: [u8; 32] = d.finalize().into();
    encode31(u32::from_be_bytes([o[0], o[1], o[2], o[3]]) >> 1)
}

// ---------------------------------------------------------------------------------------------
// F1 arming

/// One local press on the COMMITTER side arms "one ceremony", but a peer can make the armed
/// committer commit three times inside that one window: an invalid message aborts the running
/// ceremony (`fail_current` -> Idle, attempt counted) WITHOUT clearing `armed_until`, and the
/// next `request` finds the side still armed and commits again. One press -> pair Locked.
#[test]
fn gate_r2_fail_one_committer_press_cannot_be_spent_on_three_ceremonies() {
    let now = Instant::now();
    let mut c = PairVerification::new();
    let out = c.start(&HA, true, now, W).unwrap(); // the ONE local press; commitment #1 sent
    assert_eq!(out.send.unwrap().step, SasStep::Commit);
    let mut commits = 1;
    for _ in 0..3 {
        // Peer: an invalid step (wrong role for a committer) aborts the running ceremony.
        let _ = c.on_message(&HA, true, &msg(SasStep::Open, [0; 32]), Some(now));
        // Peer: a request. Still armed -> a NEW commitment, a NEW counted attempt.
        if let Ok(o) = c.on_message(&HA, true, &msg(SasStep::Request, [0; 32]), Some(now)) {
            if o.send.map(|m| m.step) == Some(SasStep::Commit) {
                commits += 1;
            }
        }
    }
    assert_eq!(
        (commits, c.status()),
        (1, VerifyStatus::Unverified { attempts_left: MAX_ATTEMPTS - 1 }),
        "one press must arm one ceremony; the peer ran {commits} and the pair is {:?}",
        c.status()
    );
}

/// Same, through a real channel and the channel map: the peer's frames are sealed on a real KK
/// channel (test seam), the local side pressed Verify exactly once.
#[test]
fn gate_r2_fail_one_press_locks_the_pair_over_a_real_channel() {
    let mut v = ids(2);
    v.sort_by_key(|d| d.key_id()); // v[0] = KK initiator = committer
    let s = session(7);
    let r = roster(s, [8; 32], &[&v[0], &v[1]]);
    let (c0, mut raw1) = kk_pair(&r, &[&v[0], &v[1]], 0, 1);
    let mut m0 = ChannelMap::new();
    m0.insert(c0).unwrap();
    let k1 = v[1].key_id();
    let now = Instant::now();
    m0.verify_start(&s, &k1, now, W).unwrap(); // ONE press
    let mut send = |m: SasMsg| {
        raw1.seal_record(RecordKind::Sas, &canonical::encode(&m).unwrap())
            .unwrap()
    };
    for _ in 0..3 {
        let junk = send(msg(SasStep::Open, [0; 32]));
        let _ = m0.open_at(&s, &k1, &junk, now);
        let req = send(msg(SasStep::Request, [0; 32]));
        let _ = m0.open_at(&s, &k1, &req, now);
    }
    assert_ne!(
        m0.verify_status(&s, &k1),
        VerifyStatus::Locked,
        "one local press locked the pair"
    );
}

/// Bound check (should hold): per press at most ONE ceremony reaches words, on either role, even
/// with decline/request flooding; and the committer's un-count of a declined commitment never
/// applies once words exist. The middleman's guesses against ONE honest side = MAX_ATTEMPTS.
#[test]
fn gate_r2_ok_decline_uncount_gives_no_extra_guess_against_one_side() {
    let now = Instant::now();
    // Honest committer A; the middleman M is A's responder.
    let mut a = PairVerification::new();
    let mut guesses = 0;
    for _press in 0..20 {
        if a.start(&HA, true, now, W).is_err() {
            break;
        }
        // Flood: decline (un-count) and request (re-commit), 50 times inside one window.
        for _ in 0..50 {
            a.on_message(&HA, true, &msg(SasStep::Decline, [0; 32]), Some(now))
                .unwrap();
            let o = a
                .on_message(&HA, true, &msg(SasStep::Request, [0; 32]), Some(now))
                .unwrap();
            assert_eq!(o.send.unwrap().step, SasStep::Commit);
        }
        // M reveals: words appear (a guess), the press is used up.
        let o = a
            .on_message(&HA, true, &msg(SasStep::Reveal, [5; 32]), Some(now))
            .unwrap();
        assert!(o.show_words.is_some());
        guesses += 1;
        // After words exist, a Decline cannot un-count: it errors and the attempt stays counted.
        assert!(a
            .on_message(&HA, true, &msg(SasStep::Decline, [0; 32]), Some(now))
            .is_err());
        // And a second ceremony in the same window needs a new press (or the pair is Locked).
        match a.on_message(&HA, true, &msg(SasStep::Request, [0; 32]), Some(now)) {
            Ok(o) => assert_eq!(o.send.unwrap().step, SasStep::Decline),
            Err(e) => assert_eq!(e, CryptoError::VerifyLocked),
        }
    }
    assert_eq!(guesses, usize::from(MAX_ATTEMPTS));
    assert_eq!(a.status(), VerifyStatus::Locked);

    // Honest responder B; M is B's committer. Decline flooding of B's request changes nothing.
    let mut b = PairVerification::new();
    let mut guesses = 0;
    for _press in 0..20 {
        if b.start(&HB, false, now, W).is_err() {
            break;
        }
        for _ in 0..50 {
            let _ = b.on_message(&HB, false, &msg(SasStep::Decline, [0; 32]), Some(now));
        }
        let r_m = [guesses as u8 + 1; 32];
        let o = b
            .on_message(&HB, false, &msg(SasStep::Commit, commit_of(&HB, &r_m)), Some(now))
            .unwrap();
        assert_eq!(o.send.as_ref().unwrap().step, SasStep::Reveal);
        // A second commitment in the same window: not accepted as a new ceremony.
        assert!(b
            .on_message(&HB, false, &msg(SasStep::Commit, [9; 32]), Some(now))
            .is_err());
        guesses += 1;
    }
    assert_eq!(guesses, usize::from(MAX_ATTEMPTS));
    assert_eq!(b.status(), VerifyStatus::Locked);
}

/// THE COUNT. A middleman M that controls both channels makes itself the committer on BOTH sides
/// (it chooses its key ids, and the KK initiator is the lower key id). It then learns each side's
/// words before that side shows anything (it holds its `open`), so a mismatch is never displayed
/// and never reaches a human "no". Each comparison needs a fresh ceremony on only ONE side, so
/// with 3 attempts per side M gets 3 + 3 - 1 = 5 independent 31-bit comparisons per human pair
/// per session, not 3. No hard stop fires; both sides end Locked.
#[test]
fn gate_r2_demo_middleman_gets_five_blind_comparisons_per_pair_per_session() {
    let now = Instant::now();
    let (mut a, mut b) = (PairVerification::new(), PairVerification::new()); // honest responders
    // Each call: the honest human presses Verify, M commits, the honest side reveals; M now knows
    // that side's words and holds its opening.
    let mut seed = 0u8;
    let mut begin = |side: &mut PairVerification, h: &[u8; 32]| -> Option<[&'static str; 3]> {
        seed += 1;
        let r_m = [seed; 32];
        side.start(h, false, now, W).ok()?; // the honest human presses Verify (again)
        let reveal = side
            .on_message(h, false, &msg(SasStep::Commit, commit_of(h, &r_m)), Some(now))
            .ok()?
            .send?;
        assert_eq!(reveal.step, SasStep::Reveal);
        Some(words_of(h, &r_m, reveal.value.as_bytes()))
    };
    // Schedule: (A1,B1) (A2,B1) (A3,B1), then hold A3 and cycle B: (A3,B2) (A3,B3).
    let mut n = 0;
    begin(&mut a, &HA).unwrap();
    begin(&mut b, &HB).unwrap();
    n += 1; // (A1,B1)
    for _ in 0..2 {
        a.abort();
        begin(&mut a, &HA).unwrap();
        n += 1; // (A2,B1), (A3,B1)
    }
    for _ in 0..2 {
        b.abort();
        begin(&mut b, &HB).unwrap();
        n += 1; // (A3,B2), (A3,B3)
    }
    a.abort();
    b.abort();
    assert_eq!(n, 2 * usize::from(MAX_ATTEMPTS) - 1);
    assert_eq!(a.status(), VerifyStatus::Locked);
    assert_eq!(b.status(), VerifyStatus::Locked);
    // Nothing was ever shown to either human (M never sent an `open`), and no hard stop fired.
}

/// `ChannelMap::open` (no time argument) judges arming against the LAST time the map was told.
/// A daemon that calls `open` instead of `open_at` never lets a window expire: a commitment that
/// arrives an hour after the press is still taken.
#[test]
fn gate_r2_demo_open_without_time_never_expires_the_window() {
    let mut v = ids(2);
    v.sort_by_key(|d| d.key_id());
    let s = session(8);
    let r = roster(s, [8; 32], &[&v[0], &v[1]]);
    let (mut raw0, c1) = kk_pair(&r, &[&v[0], &v[1]], 0, 1);
    let mut m1 = ChannelMap::new(); // v[1] = responder
    m1.insert(c1).unwrap();
    let k0 = v[0].key_id();
    let t0 = Instant::now();
    m1.verify_start(&s, &k0, t0, W).unwrap(); // press at t0, window 120 s
    // ... one hour later the peer commits; the daemon calls `open` (the time is not passed).
    let commit = raw0
        .seal_record(
            RecordKind::Sas,
            &canonical::encode(&msg(SasStep::Commit, [3; 32])).unwrap(),
        )
        .unwrap();
    match m1.open(&s, &k0, &commit).unwrap() {
        MapEvent::Verify { send: Some(_), peer_asks_to_verify: false, .. } => {}
        other => panic!("{other:?}"),
    }
    assert_eq!(m1.verify_status(&s, &k0), VerifyStatus::InProgress, "taken, not declined");
}

/// Window edge: inclusive at `now + window`, declined one nanosecond later; time going backwards
/// (a `now` before the press) still counts as armed. Recorded, not a finding.
#[test]
fn gate_r2_ok_window_edges() {
    let t0 = Instant::now() + Duration::from_secs(10);
    for (now, taken) in [
        (t0 + W, true),
        (t0 + W + Duration::from_nanos(1), false),
        (t0 - Duration::from_secs(5), true),
    ] {
        let mut r = PairVerification::new();
        r.start(&HB, false, t0, W).unwrap();
        let o = r
            .on_message(&HB, false, &msg(SasStep::Commit, [3; 32]), Some(now))
            .unwrap();
        assert_eq!(o.send.unwrap().step == SasStep::Reveal, taken);
    }
}

// ---------------------------------------------------------------------------------------------
// F3 words binding

/// After words are shown, the peer can cancel the pending comparison with any invalid message
/// (or by closing). The human then says "no match" for the words they WERE shown, and that "no"
/// is refused: no hard stop, just a counted attempt. A "no" can never raise trust, so it should
/// always be honoured for words this pair showed.
#[test]
fn gate_r2_fail_a_no_for_shown_words_is_always_a_hard_stop() {
    let now = Instant::now();
    let mut a = PairVerification::new();
    a.start(&HA, true, now, W).unwrap();
    let w = a
        .on_message(&HA, true, &msg(SasStep::Reveal, [5; 32]), Some(now))
        .unwrap()
        .show_words
        .unwrap();
    // The middleman sees the words do not match the other side and cancels before the human answers.
    let _ = a.on_message(&HA, true, &msg(SasStep::Reveal, [6; 32]), Some(now));
    let answer = a.human_says(&w, false);
    assert_eq!(
        (answer, a.status()),
        (Ok(false), VerifyStatus::HardStop),
        "the human's 'no' for the words shown was dropped"
    );
}

// ---------------------------------------------------------------------------------------------
// F2 slots

/// The slot record is inherited only at insert time. Two keys in the same slot whose channels are
/// open at the same time do not share it: the old key's hard stop leaves the new key's channel up
/// with three fresh attempts.
#[test]
fn gate_r2_demo_slot_record_not_shared_by_concurrent_channels() {
    let now = Instant::now();
    let mut v = ids(3);
    v.sort_by_key(|d| d.key_id());
    let s = session(9);
    let (me, p, p2) = (&v[0], &v[1], &v[2]);
    let r1 = roster(s, [1; 32], &[me, p]);
    let r2 = roster(s, [2; 32], &[me, p2]);
    let (mine, theirs) = kk_pair(&r1, &[me, p], 0, 1);
    let (mine2, _theirs2) = kk_pair(&r2, &[me, p2], 0, 1);
    let mut m = ChannelMap::new();
    m.insert_with_slot(mine, 1).unwrap();
    m.insert_with_slot(mine2, 1).unwrap(); // the fresh key arrives before the old one is closed
    // Hard stop on the old key.
    let mut mp = ChannelMap::new();
    mp.insert(theirs).unwrap();
    let request = mp.verify_start(&s, &me.key_id(), now, W).unwrap();
    let commit = m.verify_start(&s, &p.key_id(), now, W).unwrap();
    m.open_at(&s, &p.key_id(), &request, now).unwrap(); // crossing request: no answer
    let MapEvent::Verify { send: Some(reveal), .. } = mp.open_at(&s, &me.key_id(), &commit, now).unwrap() else {
        panic!()
    };
    let MapEvent::Verify { show_words: Some(w), .. } = m.open_at(&s, &p.key_id(), &reveal, now).unwrap() else {
        panic!()
    };
    m.verify_confirm(&s, &p.key_id(), &w, false).unwrap();
    assert_eq!(m.verify_status(&s, &p.key_id()), VerifyStatus::HardStop);
    // The same slot, other key: still open, still three attempts.
    assert!(m.get(&s, &p2.key_id()).is_some());
    assert_eq!(
        m.verify_status(&s, &p2.key_id()),
        VerifyStatus::Unverified { attempts_left: 3 }
    );
    // And plain `insert` after the slot hard-stopped is accepted (the map cannot know the slot).
    let third = DeviceIdentity::generate().unwrap();
    let (lo, hi) = if me.key_id() < third.key_id() { (me, &third) } else { (&third, me) };
    let r3 = roster(s, [3; 32], &[lo, hi]);
    let (x, y) = kk_pair(&r3, &[lo, hi], 0, 1);
    let mine3 = if lo.key_id() == me.key_id() { x } else { y };
    assert!(m.insert(mine3).is_ok());
}

// ---------------------------------------------------------------------------------------------
// F10 small order

fn p_plus(k: u8) -> [u8; 32] {
    let mut p = [0xffu8; 32];
    p[0] = 0xed;
    p[31] = 0x7f;
    let (v, c) = p[0].overflowing_add(k);
    p[0] = v;
    if c {
        // carry
        let mut i = 1;
        loop {
            let (v, c) = p[i].overflowing_add(1);
            p[i] = v;
            if !c {
                break;
            }
            i += 1;
        }
    }
    p
}

/// Independent list: the curve's 8-torsion u-coordinates, u = -1 (twist, order 4), every
/// non-canonical spelling `u + p` < 2^255 of every u < 19, all with and without the top bit; a
/// brute-force sweep of u in [0, 4096) and [p - 4096, 2^255) finds no other small-order value;
/// 2000 genuine keys are not flagged.
#[test]
fn gate_r2_ok_small_order_detection_is_exact_on_sweeps() {
    let mut expect: Vec<[u8; 32]> = EIGHT_TORSION.iter().map(|q| q.to_montgomery().to_bytes()).collect();
    let mut pm1 = p_plus(0);
    pm1[0] -= 1;
    expect.push(pm1);
    expect.push(p_plus(0));
    expect.push(p_plus(1));
    expect.sort();
    expect.dedup();
    let small: Vec<[u8; 32]> = expect.clone();
    for u in &small {
        let mut t = *u;
        assert!(is_small_order(&t));
        t[31] |= 0x80;
        assert!(is_small_order(&t));
    }
    // Sweep low values.
    for x in 0u32..4096 {
        let mut u = [0u8; 32];
        u[..4].copy_from_slice(&x.to_le_bytes());
        let want = small.contains(&u);
        assert_eq!(is_small_order(&u), want, "u = {x}");
    }
    // Sweep p - 4096 .. p + 18 (all < 2^255).
    let mut u = p_plus(0);
    // u = p - 4096
    let mut borrow = 4096u32;
    let lo = u32::from_le_bytes([u[0], u[1], u[2], u[3]]);
    let nlo = lo - borrow;
    u[..4].copy_from_slice(&nlo.to_le_bytes());
    borrow = 0;
    let _ = borrow;
    for _ in 0..(4096 + 19) {
        let want = small.contains(&u);
        assert_eq!(is_small_order(&u), want, "{}", hex::encode(u));
        let mut i = 0;
        loop {
            let (v, c) = u[i].overflowing_add(1);
            u[i] = v;
            if !c {
                break;
            }
            i += 1;
        }
    }
    for _ in 0..2000 {
        let d = DeviceIdentity::generate().unwrap();
        assert!(!is_small_order(d.public_keys().noise_static.as_bytes()));
    }
}

/// `read_starting_with_e` never panics on short input, on either KK message, and a small-order
/// ephemeral is refused in KK message 2 as well as message 1.
#[test]
fn gate_r2_ok_ephemeral_check_short_inputs_and_msg2() {
    let mut v = ids(2);
    v.sort_by_key(|d| d.key_id());
    let r = roster(session(2), [1; 32], &[&v[0], &v[1]]);
    let (_i, m1) = kk_initiate(&v[0], &r, 1).unwrap();
    for n in 0..m1.len() {
        assert!(kk_respond(&v[1], &r, 0, &m1[..n]).is_err());
    }
    let (_ch, m2) = kk_respond(&v[1], &r, 0, &m1).unwrap();
    for n in 0..m2.len() {
        let (i, _) = kk_initiate(&v[0], &r, 1).unwrap();
        assert!(i.finish(&m2[..n]).is_err());
    }
    let (i, m1b) = kk_initiate(&v[0], &r, 1).unwrap();
    let (_ch, mut m2b) = kk_respond(&v[1], &r, 0, &m1b).unwrap();
    m2b[..32].copy_from_slice(&EIGHT_TORSION[3].to_montgomery().to_bytes());
    assert_eq!(i.finish(&m2b).err(), Some(CryptoError::BadKey));
}
