//! QA-AUDIT-WIRE tasks 4 and 6: open a COPY of a daemon's audit folder and report every stored own
//! event (kind, tiers), the member's status, verify_segments over the segment files plus the export,
//! and each own number with its header hash. Scratch copy only. Env: QA_DATA (a COPY of the data
//! folder), QA_SID (hex), QA_OUT (json file), QA_TEXTS (optional json array: previews computed).
use std::fs;
use std::path::PathBuf;

use coagent_audit::bundle::verify_segments;
use coagent_audit::checkpoint::CheckpointPolicy;
use coagent_audit::redact::{preview, PatternRedactor, Redactor};
use coagent_audit::time::AuditTime;
use coagent_audit_host::{AuditHost, HostConfig};
use coagent_daemon::datadir::DataDir;
use coagent_daemon::store::{FileStore, Store};
use coagent_proto::bytes::SessionId;
use serde_json::{json, Value};

#[test]
fn qa_inspect() {
    let Ok(data) = std::env::var("QA_DATA") else {
        println!("QA_DATA unset: nothing to inspect");
        return;
    };
    let data = PathBuf::from(data);
    let sid_hex = std::env::var("QA_SID").unwrap();
    let out = std::env::var("QA_OUT").unwrap();
    let uid = std::os::unix::fs::MetadataExt::uid(&fs::metadata(&data).unwrap());
    let id = FileStore::new(DataDir::open(&data, uid).unwrap())
        .load_identity()
        .unwrap()
        .expect("identity");
    let sid = SessionId::from_hex(&sid_hex).unwrap();
    let root = data.join("audit").join(&sid_hex);
    let (h, rep) = AuditHost::open(
        &root,
        HostConfig::new(sid, CheckpointPolicy::default()),
        &id,
        &id.verified(),
        Box::new(|| Box::new(PatternRedactor) as Box<dyn Redactor>),
        AuditTime::from_unix_ms(1_900_000_000_000),
    )
    .expect("the copy opens");
    let mut bundles = h.segment_bundles().unwrap();
    let nseg = bundles.len();
    bundles.push(h.export(&id).unwrap());
    let verify = verify_segments(&bundles).map(|r| format!("{r:?}")).map_err(|e| format!("{e:?}"));
    let mut events = vec![];
    let mut seen: std::collections::BTreeMap<u64, String> = Default::default();
    let mut twice = 0;
    for (bi, b) in bundles.iter().enumerate() {
        for e in &b.own_events {
            let hash = format!("{:?}", e.header.hash().unwrap());
            match seen.get(&e.header.author_seq) {
                Some(h0) if *h0 != hash => twice += 1,
                Some(_) => {}
                None => {
                    seen.insert(e.header.author_seq, hash.clone());
                }
            }
            events.push(json!({
                "bundle": bi, "is_export": bi == nseg, "seq": e.header.author_seq,
                "kind": e.header.kind, "summary": e.summary.as_ref().map(|t| t.body.clone()),
                "full": e.full.as_ref().map(|t| t.body.clone()),
                "header_debug": format!("{:?}", e.header),
            }));
        }
    }
    let previews: Vec<Value> = std::env::var("QA_TEXTS")
        .ok()
        .map(|p| {
            let texts: Vec<String> = serde_json::from_str(&fs::read_to_string(p).unwrap()).unwrap();
            texts.iter().map(|t| json!(preview(&PatternRedactor, t))).collect()
        })
        .unwrap_or_default();
    let nums: Vec<u64> = seen.keys().copied().collect();
    let st = h.status().unwrap();
    let r = json!({
        "opened": format!("{:?}", rep.opened), "segment_files": nseg, "verify": format!("{verify:?}"),
        "own_numbers": nums, "signed_twice": twice, "events": events, "previews": previews,
        "host_status_segment": st.segment, "host_own_seq": st.own_seq,
        "member_status": format!("{:?}", h.member().unwrap().status()),
    });
    fs::write(&out, serde_json::to_string_pretty(&r).unwrap()).unwrap();
    println!("QA inspect -> {out}: {} events, {} segment files, twice {twice}", r["events"].as_array().unwrap().len(), nseg);
}
