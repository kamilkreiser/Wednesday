//! QA-AUDIT-HOST-NOTES: a seal whose step 0 checkpoint lands through a P-4 re-open that CHANGES the
//! limits in force (the `cfg(test)` re-offer hook): what does `seal_begin` answer, did the seal happen,
//! and what does the docs' table tell a caller to do? Head 52ad858 only; uncommitted.

use super::common::*;
use super::copy_tree;
use crate::fsio::fault::{self, Op, Rule};
use crate::host::test_hooks;
use crate::{Causer, HostError, Outcome, SealTrigger};
use coagent_audit::session::StoreLimits;

#[test]
fn qahn_seal_step0_limits_changed() {
    let w = World::new(140, 3, 3);
    let base = scratch("qahn-lc");
    let root = base.join("host");
    let d = StoreLimits::default();
    let mut c = cfg(&w);
    c.limits = StoreLimits { bytes: d.bytes / 2, records: d.records / 2 };
    let mut h = create_host(&w, 1, &root, c.clone());
    for n in 0..3 {
        host_record(&mut h, &w.ids[1], Causer::LocalHuman, n + 1);
    }
    let seg0 = h.member().unwrap().segment();
    let cps0 = h.member().unwrap().own().checkpoints().len();
    let files0 = h.archive_files().unwrap().len();
    test_hooks::reoffer_refuses_next();
    let mut first = false;
    fault::arm(Rule::FailEvery(Box::new(move |cx| {
        if !first && cx.op == Op::SyncDir && cx.dir == "store" {
            first = true;
            return true;
        }
        false
    })));
    let r = h.seal_begin(&w.ids[1], SealTrigger::OwnerCommand, t(10));
    fault::disarm();
    let shape = match &r {
        Ok(b) => format!("Ok(seg {})", b.segment),
        Err(HostError::LimitsChanged { answer, limits }) => format!(
            "Err(LimitsChanged {{ answer: {}, limits differ {} }})",
            match &**answer {
                Ok(Outcome::Checkpoint(_)) => "Ok(Checkpoint(..))".to_string(),
                other => format!("{other:?}"),
            },
            limits.differs()
        ),
        Err(e) => format!("Err({e:?})"),
    };
    let st = h.status().unwrap();
    println!(
        "QAHN LC seal_begin {shape}; in window {}; segment {seg0} -> {}; own checkpoints {cps0} -> {}; archive files {files0} -> {}",
        st.in_window,
        st.segment,
        h.member().unwrap().own().checkpoints().len(),
        h.archive_files().unwrap().len()
    );
    // a caller that re-runs the seal
    let again = h.seal(&w.ids[1], SealTrigger::OwnerCommand, t(11)).map(|s| s.info.segment);
    println!(
        "QAHN LC the seal re-run: {again:?}; own checkpoints then {}",
        h.member().unwrap().own().checkpoints().len()
    );
    drop(h);
    let copy = base.join("copy");
    copy_tree(&root, &copy);
    let (h2, _) = open_host(&w, 1, &copy, c, 20).unwrap();
    println!("QAHN LC fresh open: segment {}", h2.member().unwrap().segment());
}
