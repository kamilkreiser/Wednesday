//! Gate r5 run 2: the 64 KiB byte bound, few words (A3 survived the seat's suite). Asserts: over 64 KiB is DENIED.
#![cfg(unix)]
mod common;
use coagent_policy::*;
use common::*;
#[test]
fn g5_byte_bound_denies_few_words() {
    let fx = fixture("g5bb");
    let st = fx.state();
    for (n, label) in [(64 * 1024, "at"), (64 * 1024 + 1, "over"), (200 * 1024, "far over")] {
        // one SHORT word repeated: one distinct piece, no long path, so only the byte bound can catch it
        let mut cmd = "echo".to_string();
        while cmd.len() + 4 <= n { cmd.push_str(" abc"); }
        while cmd.len() < n { cmd.push('d'); }
        let d = decide(&fx.bash(&cmd), &st, Surface::Console, NOW);
        let s = match &d { Decision::Deny { reason } => format!("DENY {reason:?}"), Decision::Ask { card } => format!("ASK {:?}", card.tier), o => format!("{o:?}") };
        eprintln!("{label} ({} bytes): {s}", cmd.len());
        if n > 64 * 1024 { assert!(matches!(d, Decision::Deny { .. }), "{label}: {s}"); }
    }
}
