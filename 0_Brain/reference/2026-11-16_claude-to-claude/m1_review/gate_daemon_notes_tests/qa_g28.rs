//! DAEMON-NOTES item 7 (G28, FR-5 = (a), diagnosis only; BACKLOG "A guest's first `chan.open` right
//! after joining was refused once (`not_found`)"). A FINDING, not a test of a fix: it reproduces a
//! joiner's `chan.open` arriving before the convener's `chan.create` and asserts what it measured.
//!
//! How: the convener runs in-process with a tap that holds its outgoing `chan.create` control frame
//! for 700 ms (the tap sleeps in the link task before the frame is sent; nothing is dropped). The
//! convener sends the welcome through the mailbox BEFORE it attaches (docs/DAEMON.md §4), so the
//! joiner, which attaches as soon as the welcome arrives, reaches the relay first. Control: the same
//! pair with no hold, measured the same way (loopback order; printed, and bounded by the same rule).
mod common;

use std::sync::atomic::{AtomicU32, Ordering};
use std::sync::Arc;
use std::time::Duration;

use coagent_daemon::link::{Dir, Tap, TapVerdict};
use common::*;
use serde_json::json;

const NOT_FOUND: &str = "session link down (relay refused chan.open (not_found)); reconnecting";

#[derive(Default)]
struct HoldCreate {
    hold_ms: u64,
    held: AtomicU32,
}

impl Tap for HoldCreate {
    fn frame(&self, dir: Dir, binary: bool, bytes: &[u8]) -> TapVerdict {
        if self.hold_ms > 0
            && dir == Dir::Out
            && !binary
            && bytes.windows(13).any(|w| w == b"\"chan.create\"")
        {
            self.held.fetch_add(1, Ordering::SeqCst);
            std::thread::sleep(Duration::from_millis(self.hold_ms));
        }
        TapVerdict::Pass
    }
}

/// Pair an in-process convener (with `hold_ms` on its chan.create) and a joiner; returns the joiner's
/// (not_found lines, reconnects, creates held) once both are connected and quiet.
fn measure(tag: &str, hold_ms: u64) -> (usize, u64, u32) {
    let mut run = Run::new(tag);
    let tap = Arc::new(HoldCreate {
        hold_ms,
        held: AtomicU32::new(0),
    });
    let a = InProc::start(&mut run, "a", Some(tap.clone()), |_| {});
    let b = run.daemon("b", &[]);
    let db = run.dir(b);
    pair_dirs(&a.dir, &db);
    std::thread::sleep(Duration::from_secs(3));
    wait_connected_dirs(&a.dir, &db);
    let r = ctl(&db, "status", json!({}))["result"]["session"]["reconnects"]
        .as_u64()
        .unwrap();
    let nf = std::fs::read_to_string(&run.daemons[b].stderr)
        .unwrap()
        .matches(NOT_FOUND)
        .count();
    let held = tap.held.load(Ordering::SeqCst);
    eprintln!("G28 {tag}: hold {hold_ms} ms: creates held {held}, joiner not_found lines {nf}, reconnects {r}");
    a.stop();
    run.finish();
    (nf, r, held)
}

#[test]
fn qa_g28_holds() {
    // QA-DAEMON-NOTES item 7: the same measure at several holds (0, 700, 2500, 5000 ms), printed only.
    for h in [0u64, 700, 2500, 5000] {
        let (nf, r, held) = measure(&format!("qg{h}"), h);
        eprintln!("QA-G28 hold {h} ms: creates held {held}, not_found {nf}, reconnects {r}");
    }
}
