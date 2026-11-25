//! QA-AUDIT-HOST-NOTES finding M-1 (repro): a seal whose step 2 write fails (its archive file, or its
//! pending anchor) answers a plain `Err(Dir(..))` that no row of the P-4 answer table names. Head only.

use super::common::*;
use crate::fsio::fault::{self, Op, Rule};
use crate::{Causer, SealTrigger};

#[test]
fn qahn_seal_step2_dir_error() {
    for (what, dir, op) in [("archive file", "archive", Op::Link), ("pending anchor", "anchors", Op::Rename)] {
        let w = World::new(150, 3, 3);
        let base = scratch("qahn-gap");
        let root = base.join("host");
        let mut h = create_host(&w, 1, &root, cfg(&w));
        for n in 0..3 {
            host_record(&mut h, &w.ids[1], Causer::LocalHuman, n + 1);
        }
        let mut done = false;
        fault::arm(Rule::FailEvery(Box::new(move |c| {
            if !done && c.dir == dir && c.op == op && (dir != "anchors" || c.name == "pending") {
                done = true;
                return true;
            }
            false
        })));
        let r = h.seal(&w.ids[1], SealTrigger::OwnerCommand, t(10)).map(|s| s.info.segment);
        fault::disarm();
        let st = h.status().unwrap();
        println!(
            "QAHN GAP [{what}]: seal {r:?}; segment {}; in window {}; own checkpoints {}; archive files {}",
            st.segment, st.in_window, h.member().unwrap().own().checkpoints().len(), st.archive_files
        );
        let again = h.seal(&w.ids[1], SealTrigger::OwnerCommand, t(11)).map(|s| s.info.segment);
        println!(
            "QAHN GAP [{what}] the seal again: {again:?}; own checkpoints {}; archive files {}",
            h.member().unwrap().own().checkpoints().len(), h.status().unwrap().archive_files
        );
    }
}
