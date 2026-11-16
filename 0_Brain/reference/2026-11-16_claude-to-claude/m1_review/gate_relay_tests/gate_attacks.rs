//! QA gate attack tests (written by the gate, not the builder). Each test asserts the SAFE
//! property; a failing test is a finding. All relays listen on 127.0.0.1, ephemeral port.
mod common;

use std::time::Duration;

use coagent_relay::{ChanId, ClientFrame, CutReason, ErrorCode, Limits, ServerEvent, ServerFrame};
use common::*;
use tokio::io::AsyncWriteExt;

/// G1. Design 03 §4.4 asks for "per-IP caps on ... concurrent channels". One unauthenticated
/// connection from one address creates every channel the relay allows (default limits), after
/// which an honest convener cannot create a channel. Safe property: the honest create succeeds.
#[tokio::test]
async fn g1_one_address_cannot_take_every_channel() {
    let relay = start(small_limits()).await;
    let mut atk = connect(&relay).await;
    let max = coagent_relay::limits::MAX_CHANNELS;
    for i in 0..max {
        if i >= 28 {
            // stay inside the per-address op budget (2/s after a burst of 30)
            tokio::time::sleep(Duration::from_millis(520)).await;
        }
        let mut id = [0xA0u8; 32];
        id[0] = i as u8;
        atk.send(&ClientFrame::ChanCreate {
            chan_id: ChanId(id),
            admin_token_hash: token(1).hash(),
            cap: 2,
        })
        .await
        .unwrap();
        expect_ok(&mut atk, "chan.create").await;
    }
    atk.close().await;
    assert_eq!(relay.stats().channels, max);
    tokio::time::sleep(Duration::from_secs(1)).await; // let the address earn an op token back
    let mut honest = connect(&relay).await;
    honest
        .send(&ClientFrame::ChanCreate {
            chan_id: ChanId([0x55; 32]),
            admin_token_hash: token(9).hash(),
            cap: 2,
        })
        .await
        .unwrap();
    match expect_control(&mut honest).await {
        ServerFrame::Ok { .. } => {}
        other => panic!(
            "FINDING G1: after one address created {max} channels and left, an honest chan.create got {other:?} \
             (the attacker's channels persist for channel_idle_ttl = 30 min)"
        ),
    }
    relay.shutdown().await;
}

/// G2. Relay-wide pair-buffer cap is shared by everyone with no per-address or per-channel
/// fairness: one attacker sender filling frames for registered-but-absent slots exhausts it and
/// every honest pair on the relay is refused. Scaled limits (total 1 MiB) so the test is fast; at
/// the default 256 MiB the same attack needs ~19 sender sockets (16 per address) and ~30 s.
#[tokio::test]
async fn g2_one_sender_cannot_starve_every_other_pair() {
    let l = Limits {
        pair_max_bytes: 256 * 1024,
        max_frame_bytes: 64 * 1024,
        total_buffer_bytes: 1024 * 1024,
        ..small_limits()
    };
    let relay = start(l).await;
    let atk_ch = make_channel(&relay, 1, 8).await;
    let mut atk = attach(&relay, &atk_ch, 0).await;
    let payload = vec![7u8; 32 * 1024];
    let mut refused = false;
    'outer: for seq in 0..10u64 {
        for to in 1..8u8 {
            atk.send_data(to, seq, &payload).await.unwrap();
            if let Ok(Some(ServerEvent::Control(ServerFrame::Error { .. }))) =
                atk.recv_timeout(Duration::from_millis(20)).await
            {
                refused = true;
                break 'outer;
            }
        }
    }
    assert!(refused, "attacker eventually hits the relay-wide cap");
    // top the buffer off: halve the frame size until even a 1-byte payload is refused
    let mut size = 16 * 1024usize;
    let mut seq = 1000u64;
    while size >= 1 {
        atk.send_data(1, seq, &vec![7u8; size]).await.unwrap();
        seq += 1;
        match atk.recv_timeout(Duration::from_millis(50)).await {
            Ok(Some(ServerEvent::Control(ServerFrame::Error { .. }))) => size /= 2,
            _ => {}
        }
    }
    // An honest, fully attached, acking pair on a different channel:
    let hon = make_channel(&relay, 2, 2).await;
    let mut a = attach(&relay, &hon, 0).await;
    let mut b = attach(&relay, &hon, 1).await;
    a.send_data(1, 0, b"honest").await.unwrap();
    let delivered = !no_data_within(&mut b, Duration::from_secs(2)).await;
    if !delivered {
        let err = next_error(&mut a).await;
        panic!(
            "FINDING G2: honest pair on another channel starved: receiver got no data, sender got error {err:?}; \
             relay buffered_bytes = {}",
            relay.stats().buffered_bytes
        );
    }
    relay.shutdown().await;
}

/// G3. Slow-loris bypass: the deadline clock (`partial_since`) is cleared by ANY complete message,
/// including a WebSocket control frame interleaved inside a fragmented data message. A client that
/// starts a fragmented message and sends a ping before every continuation keeps a partial message
/// open indefinitely. Safe property: the connection is cut as slow-loris.
#[tokio::test]
async fn g3_ping_interleaving_does_not_defeat_the_slow_loris_deadline() {
    let l = Limits {
        message_deadline: Duration::from_millis(400),
        idle_timeout: Duration::from_secs(30),
        ..Limits::default()
    };
    let relay = start(l).await;
    let mut raw = connect(&relay).await.into_raw_tls();
    // masked (zero key) non-final binary frame, 100 bytes
    let mut first = vec![0x02, 0x80 | 100, 0, 0, 0, 0];
    first.extend_from_slice(&[0u8; 100]);
    raw.write_all(&first).await.unwrap();
    raw.flush().await.unwrap();
    // 12 rounds x 250 ms = 3 s, 7.5x the 400 ms deadline
    for _ in 0..12 {
        tokio::time::sleep(Duration::from_millis(250)).await;
        let ping = [0x89u8, 0x80, 0, 0, 0, 0]; // masked ping, empty
        let mut cont = vec![0x00, 0x80 | 10, 0, 0, 0, 0]; // non-final continuation, 10 bytes
        cont.extend_from_slice(&[0u8; 10]);
        if raw.write_all(&ping).await.is_err() || raw.write_all(&cont).await.is_err() {
            break;
        }
        let _ = raw.flush().await;
    }
    let s = relay.stats();
    assert!(
        s.cut(CutReason::SlowLoris) == 1,
        "FINDING G3: a message started 3 s ago (deadline 400 ms) is still open; slow_loris cuts = {}, connections = {}",
        s.cut(CutReason::SlowLoris),
        s.connections
    );
    relay.shutdown().await;
}

/// G4. Head-of-line by a hostile member: the relay frees buffered frames by `seq <= upto` from the
/// FRONT of the queue, and never checks that `pair_seq` increases. A member that sends one frame
/// with `pair_seq = u64::MAX` first wedges the pair: an honest receiver acking every in-order
/// frame it gets frees nothing and is cut as `never_acks`. Safe property: the honest receiver is
/// not cut.
#[tokio::test]
async fn g4_a_hostile_sender_cannot_get_an_acking_receiver_cut() {
    let l = Limits {
        pair_max_frames: 20,
        ..small_limits()
    };
    let relay = start(l).await;
    let ch = make_channel(&relay, 1, 2).await;
    let mut evil = attach(&relay, &ch, 0).await;
    let mut honest = attach(&relay, &ch, 1).await;
    evil.send_data(1, u64::MAX, b"poison").await.unwrap();
    let _ = next_data(&mut honest).await; // honest app drops it as out of order, does not ack it
    for i in 1..=40u64 {
        if evil.send_data(1, i, b"x").await.is_err() {
            break;
        }
        match honest.recv_timeout(Duration::from_secs(2)).await {
            Ok(Some(ServerEvent::Binary(_))) => {
                let _ = honest
                    .send(&ClientFrame::ChanAck {
                        from_slot: 0,
                        upto: i,
                    })
                    .await;
                tokio::time::sleep(Duration::from_millis(20)).await;
            }
            _ => break,
        }
    }
    tokio::time::sleep(Duration::from_millis(300)).await;
    assert_eq!(
        relay.stats().cut(CutReason::NeverAcks),
        0,
        "FINDING G4: an honest receiver that acked every in-order frame was cut as never_acks"
    );
    relay.shutdown().await;
}

/// G5 (control, expected to PASS): a second socket presenting the right token for an attached
/// slot is refused, so a stale half-open socket blocks the real owner's reconnect (DQ 6).
#[tokio::test]
async fn g5_second_attach_is_refused_while_the_first_is_alive() {
    let relay = start(small_limits()).await;
    let ch = make_channel(&relay, 1, 2).await;
    let _old = attach(&relay, &ch, 1).await;
    let mut new = connect(&relay).await;
    new.send(&ClientFrame::ChanOpen {
        chan_id: ch.id,
        slot: 1,
        slot_token: ch.toks[1].clone(),
        resume_from: vec![],
    })
    .await
    .unwrap();
    assert_eq!(expect_error(&mut new).await, ErrorCode::Full);
    relay.shutdown().await;
}
