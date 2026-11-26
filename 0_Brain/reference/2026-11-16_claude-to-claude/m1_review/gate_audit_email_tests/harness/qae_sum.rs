//! QA-AUDIT-EMAIL (h): summaries through the chain, read back from the stored event (scratch copy
//! only, never committed). Prints; asserts only that the run happened. Every address is made up.
#![allow(dead_code)]
mod common;
use coagent_audit::chain::EventInput;
use common::*;

fn rec(a: &mut coagent_audit::session::SessionAudit<coagent_audit::store::MemStore>, w: &World, s: &str, n: u64) -> String {
    match a.record(&w.ids[0], EventInput { kind: "qae.sum", summary: Some(s), full: Some("qae full") }, t(n)) {
        Ok(seq) => {
            let b = a.export(&w.ids[0]).unwrap();
            let e = b.own_events.iter().find(|e| e.header.author_seq == seq).unwrap();
            let body = e.summary.as_ref().unwrap().body.clone();
            format!("stored {} bytes: {:?}", body.len(), if body.len() > 120 { format!("{}…", &body[..120]) } else { body })
        }
        Err(err) => format!("refused: {err:?}"),
    }
}

#[test]
fn qae_summaries() {
    let w = World::new(0xb5, 2, 2);
    let mut a = w.audit(0, every(1_000));
    let one = "notify alice@example.com about the deploy";
    println!("QAE-H1 summary with an address ({} bytes) -> {}", one.len(), rec(&mut a, &w, one, 1));
    let shortest = vec!["a@b.test"; 455].join(" ");
    println!("QAE-H2 455 x a@b.test joined by spaces ({} bytes) -> {}", shortest.len(), rec(&mut a, &w, &shortest, 2));
    let near = format!("{} a@b.test", "x".repeat(4096 - 9));
    println!("QAE-H2b x*4087 + ' a@b.test' ({} bytes) -> {}", near.len(), rec(&mut a, &w, &near, 3));
    let older = vec!["K=v"; 1024].join(" ");
    println!("QAE-H4 older rule: 1024 x 'K=v' joined by spaces ({} bytes) -> {}", older.len(), rec(&mut a, &w, &older, 4));
    let older2 = vec!["K=v"; 400].join(" ");
    println!("QAE-H4b older rule: 400 x 'K=v' ({} bytes) -> {}", older2.len(), rec(&mut a, &w, &older2, 5));
}
