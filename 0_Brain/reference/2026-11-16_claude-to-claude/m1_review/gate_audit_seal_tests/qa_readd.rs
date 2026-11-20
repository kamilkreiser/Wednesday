//! QA gate M3-AUDIT-SEAL: with NO seal, a removed author that never checkpointed is released, then
//! re-added; its first event from before the release is offered again. Runs unchanged at the base
//! 36537eb and the head, to show whether seed 91's `seal property replay` failure is pre-existing
//! (A-m6 / DQ-S6) rather than caused by a seal.
mod common;

use coagent_audit::store::Store;
use coagent_audit::tiers::ShareLevel;
use common::*;

#[test]
fn qa_release_then_readd_takes_a_pre_release_event_again() {
    let mut w = World::new(93, 4, 4);
    let (v, x) = (1usize, 2usize);
    let mut xa = w.audit(x, every(1_000));
    xa.set_share_level(w.key(v), ShareLevel::Full);
    let mut va = w.audit(v, every(1_000));
    va.set_share_level(w.key(x), ShareLevel::Full);
    let seq = xa.record(&w.ids[x], input("x.ev", "s", "f"), t(1)).unwrap();
    let e1 = xa
        .outgoing(seq)
        .into_iter()
        .find(|(to, _)| *to == w.key(v))
        .unwrap()
        .1;
    va.receive(&w.ids[v], &e1, t(1)).unwrap();
    let rm = w.remove(x);
    va.apply_roster(&rm).unwrap();
    va.archive_and_release(&w.ids[v], &w.key(x)).unwrap();
    let before = va.store().list(&w.s).unwrap();
    let add = w.add(x, 2);
    va.apply_roster(&add).unwrap();
    let after_add = va.store().list(&w.s).unwrap();
    let got = va.receive(&w.ids[v], &e1, t(2));
    let after = va.store().list(&w.s).unwrap();
    eprintln!(
        "qa readd (no seal): replay of X's pre-release event 1 after release + re-add: {got:?}; \
         store records {} -> {} (re-add) -> {}",
        before.len(),
        after_add.len(),
        after.len()
    );
}
