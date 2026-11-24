//! QA-DAEMON-NOTES item 4(c), the case "a short mailbox drop with the relay ALIVE": an in-process
//! inviter whose tap cuts ITS mailbox connection (TapVerdict::Disconnect) once, at the first frame
//! after arming (the relay's notice that a joiner arrived). The relay child keeps running.
//! Printed, not judged by the test: when and how the inviter's pairing fails, what the joiner sees,
//! whether the relay is still there, and whether a new invitation (no `end`) then pairs.
mod common;

use std::sync::atomic::{AtomicBool, AtomicU32, Ordering};
use std::sync::Arc;
use std::time::{Duration, Instant};

use coagent_daemon::link::{Dir, Tap, TapVerdict};
use common::*;
use serde_json::json;

#[derive(Default)]
struct CutOnce {
    armed: AtomicBool,
    cuts: AtomicU32,
}

impl Tap for CutOnce {
    fn frame(&self, _dir: Dir, _binary: bool, _bytes: &[u8]) -> TapVerdict {
        if self.armed.swap(false, Ordering::SeqCst) {
            self.cuts.fetch_add(1, Ordering::SeqCst);
            return TapVerdict::Disconnect;
        }
        TapVerdict::Pass
    }
}

#[test]
fn qa_mailbox_cut_with_the_relay_alive() {
    let mut run = Run::new("qmb");
    let tap = Arc::new(CutOnce::default());
    let a = InProc::start(&mut run, "a", Some(tap.clone()), |_| {});
    let b = run.daemon("b", &[]);
    let db = run.dir(b);
    let inv = ctl(&a.dir, "invite", json!({}));
    assert_eq!(inv["ok"], true, "{inv}");
    let line = inv["result"]["line"].as_str().unwrap().to_string();
    let relay0 = ctl(&a.dir, "status", json!({}))["result"]["relay"].clone();
    tap.armed.store(true, Ordering::SeqCst);
    let t0 = Instant::now();
    let j = ctl(&db, "join", json!({ "blob": line }));
    let mut failed_at = None;
    let mut first_b = None;
    while t0.elapsed() < Duration::from_secs(12) {
        let pa = ctl(&a.dir, "status", json!({}))["result"]["pairing"].clone();
        let pb = ctl(&db, "status", json!({}))["result"]["pairing"].clone();
        if failed_at.is_none() && pa["state"] == "failed" {
            failed_at = Some((t0.elapsed(), pa.clone()));
        }
        if first_b.is_none() && pb["state"] == "failed" {
            first_b = Some((t0.elapsed(), pb.clone()));
        }
        if failed_at.is_some() && first_b.is_some() {
            break;
        }
        std::thread::sleep(Duration::from_millis(50));
    }
    let relay1 = ctl(&a.dir, "status", json!({}))["result"]["relay"].clone();
    eprintln!("QA-MBDROP join reply: {j}");
    eprintln!("QA-MBDROP cuts {}; inviter failed: {failed_at:?}", tap.cuts.load(Ordering::SeqCst));
    eprintln!("QA-MBDROP joiner: {first_b:?}");
    eprintln!("QA-MBDROP relay before {relay0} after {relay1}");
    // A new invitation without `end`, a fresh joiner.
    let c = run.daemon("c", &[]);
    pair_dirs(&a.dir, &run.dir(c));
    eprintln!("QA-MBDROP next invitation paired");
    a.stop();
    run.finish();
}
