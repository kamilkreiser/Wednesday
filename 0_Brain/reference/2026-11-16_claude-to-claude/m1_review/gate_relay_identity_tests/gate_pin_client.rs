//! QA gate helper: connect the relay crate's own pinned client to GATE_URL with pin GATE_FP and
//! exchange one frame. GATE_EXPECT = "ok" or "pin_mismatch". Skips (passes) when GATE_URL is unset.

use std::time::Duration;

use coagent_relay::{connect_pinned, ClientFrame, Fingerprint, ServerEvent, ServerFrame};

#[tokio::test]
async fn gate_pin_client() {
    let Ok(url) = std::env::var("GATE_URL") else {
        return;
    };
    let fp: Fingerprint = std::env::var("GATE_FP").unwrap().parse().expect("fingerprint");
    let expect = std::env::var("GATE_EXPECT").unwrap();
    match connect_pinned(&url, fp, Duration::from_secs(5)).await {
        Ok(mut c) => {
            c.send(&ClientFrame::Ping).await.unwrap();
            let ev = c.recv().await.unwrap();
            assert_eq!(ev, ServerEvent::Control(ServerFrame::Pong));
            println!("GATE_CLIENT connected and exchanged Ping/Pong");
            assert_eq!(expect, "ok", "connected but expected {expect}");
        }
        Err(e) => {
            println!("GATE_CLIENT refused: stage {:?} pin_mismatch {} : {e}", e.stage, e.pin_mismatch);
            assert_eq!(expect, "pin_mismatch", "refused but expected {expect}");
            assert!(e.pin_mismatch);
        }
    }
}
