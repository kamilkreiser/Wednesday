//! QA gate round 2, over the wire (127.0.0.1, ephemeral port). Each test asserts the SAFE property.
mod common;

use std::time::Duration;

use coagent_relay::{CutReason, Limits};
use common::*;
use tokio::io::AsyncWriteExt;

fn masked(fin: bool, opcode: u8, n: usize) -> Vec<u8> {
    let mut v = vec![if fin { 0x80 } else { 0 } | opcode, 0x80 | n as u8, 0, 0, 0, 0];
    v.extend(std::iter::repeat_n(0u8, n));
    v
}

fn loris_limits() -> Limits {
    Limits {
        message_deadline: Duration::from_millis(400),
        idle_timeout: Duration::from_secs(30),
        ..Limits::default()
    }
}

/// G3 variant: open a fragmented message, then send ONLY pings (no continuations, so the tracker
/// never gets a frame that could resynchronise it) and pongs, each in its own TLS write.
#[tokio::test]
async fn r2_g3_pings_and_pongs_only_after_an_open_fragment_are_cut() {
    let relay = start(loris_limits()).await;
    let mut raw = connect(&relay).await.into_raw_tls();
    raw.write_all(&masked(false, 2, 100)).await.unwrap();
    raw.flush().await.unwrap();
    for i in 0..12 {
        tokio::time::sleep(Duration::from_millis(250)).await;
        let f = if i % 2 == 0 { masked(true, 9, 3) } else { masked(true, 10, 0) };
        if raw.write_all(&f).await.is_err() {
            break;
        }
        let _ = raw.flush().await;
    }
    let s = relay.stats();
    assert_eq!(
        s.cut(CutReason::SlowLoris),
        1,
        "G3-r2: open fragment + pings/pongs only: slow_loris cuts = {}, connections = {}",
        s.cut(CutReason::SlowLoris),
        s.connections
    );
    relay.shutdown().await;
}

/// G3 variant: each round, in ONE write, finish the open message and start the next one
/// ([ping][final continuation][new first fragment]), so a complete data message arrives every
/// 250 ms while some fragmented message is always open. Expected: cut (the clock is never cleared
/// because the tracker reads ahead and sees the new fragment open).
#[tokio::test]
async fn r2_g3_finish_and_reopen_in_one_write_is_cut() {
    let relay = start(loris_limits()).await;
    let mut raw = connect(&relay).await.into_raw_tls();
    raw.write_all(&masked(false, 2, 100)).await.unwrap();
    raw.flush().await.unwrap();
    for _ in 0..12 {
        tokio::time::sleep(Duration::from_millis(250)).await;
        let mut w = masked(true, 9, 0);
        w.extend(masked(true, 0, 10));
        w.extend(masked(false, 2, 100));
        if raw.write_all(&w).await.is_err() {
            break;
        }
        let _ = raw.flush().await;
    }
    let s = relay.stats();
    // The completed 110-byte binary message is not a valid relay data frame, so the relay may cut
    // for that instead of slow-loris; the safe property is only that the connection is not held.
    assert_eq!(
        s.connections, 0,
        "G3-r2: finish+reopen: connection still open after 3 s (slow_loris cuts = {})",
        s.cut(CutReason::SlowLoris)
    );
    relay.shutdown().await;
}
