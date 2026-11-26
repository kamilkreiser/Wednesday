//! QA-AUDIT-EMAIL (h)(3): what the audit host answers when a summary is refused (scratch copy only).
#![cfg(unix)]
#![allow(dead_code)]
mod common;
use coagent_audit_host::{Causer, Input, OwnedInput};
use common::*;

#[test]
fn qae_host_summary_refusal() {
    let w = World::new(0xb6, 2, 2);
    let root = scratch("qae-host-sum").join("host");
    let mut h = create_host(&w, 0, &root, cfg(&w));
    let big = vec!["a@b.test"; 455].join(" ");
    let r = h.apply(
        &w.ids[0],
        Input::Record {
            causer: Causer::LocalHuman,
            input: OwnedInput { kind: "qae.sum".into(), summary: Some(big.clone()), full: Some("qae full".into()) },
        },
        t(1),
    );
    println!("QAE-H3 host apply(Record, summary {} bytes) -> {:?}", big.len(), r);
    let st = h.status().unwrap();
    println!("QAE-H3 after: own_seq {:?}", st.own_seq);
    let r2 = h.apply(
        &w.ids[0],
        Input::Record {
            causer: Causer::LocalHuman,
            input: OwnedInput { kind: "qae.sum".into(), summary: None, full: Some("qae next".into()) },
        },
        t(2),
    );
    println!("QAE-H3 next record without a summary -> {:?}", r2);
}
