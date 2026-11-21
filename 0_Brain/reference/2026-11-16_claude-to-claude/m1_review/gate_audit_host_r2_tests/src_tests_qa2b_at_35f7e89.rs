//! QA-AUDIT-HOST-R2: the P-4 + second-write probe, run at 35f7e89 (base) to see whether it is
//! pre-existing. The fault injector's FailEvery rule (test-only) is applied from the round's fsio.rs diff.
use super::common::*;
use crate::fsio::fault::{self, Op, Rule};
use crate::{Causer, Input};
/// P-4 (a record's put lands, its directory sync fails), and inside the re-open a SECOND write of
/// the host fails: `anchors/limits` (reoffer_limits) or `anchors/current` (settle_pending). Does the
/// answer still say the record landed, or does an Err hide it (so a caller that retries on an Err
/// records the event twice)? Pre-existing shape (the same `?` in `reopen` at 35f7e89), measured at
/// the head.
#[test]
fn qa2_p4_then_a_second_write_fails_in_the_reopen() {
    let mut lines = Vec::new();
    for which in ["limits", "current"] {
        let w = World::new(187, 3, 3);
        let base = scratch(&format!("qa2-p4x-{which}"));
        let root = base.join("host");
        let mut h = create_host(&w, 1, &root, cfg(&w));
        for n in 0..3 {
            host_record(&mut h, &w.ids[1], Causer::LocalHuman, n + 1);
        }
        let seq0 = h.member().unwrap().own().seq();
        let mut store_failed = false;
        let mut other_failed = false;
        let target = which;
        fault::arm(Rule::FailEvery(Box::new(move |c| {
            if !store_failed && c.op == Op::SyncDir && c.dir == "store" {
                store_failed = true;
                return true;
            }
            if store_failed && !other_failed && c.op == Op::CreateTemp && c.dir == "anchors" && c.name == target {
                other_failed = true;
                return true;
            }
            false
        })));
        let r = h.apply(
            &w.ids[1],
            Input::Record {
                causer: Causer::LocalHuman,
                input: owned("act", Some("one human act"), None),
            },
            t(10),
        );
        fault::disarm();
        let closed = h.member().is_err();
        let seq1 = h.member().map(|m| m.own().seq()).unwrap_or(0);
        // a caller that treats an Err as "not done" offers the same act again
        let retry = if r.is_err() {
            Some(h.apply(
                &w.ids[1],
                Input::Record {
                    causer: Causer::LocalHuman,
                    input: owned("act", Some("one human act"), None),
                },
                t(11),
            ))
        } else {
            None
        };
        let seq2 = h.member().map(|m| m.own().seq()).unwrap_or(0);
        lines.push(format!(
            "{which}: answer {r:?}; host closed {closed}; own seq {seq0} -> {seq1} (landed {}); a retry on the Err -> {retry:?}; own seq then {seq2}",
            seq1 > seq0
        ));
        drop(h);
        scratch_done(&base);
    }
    println!("QA2 P-4 + second write failing inside the re-open:\n  {}", lines.join("\n  "));
}
