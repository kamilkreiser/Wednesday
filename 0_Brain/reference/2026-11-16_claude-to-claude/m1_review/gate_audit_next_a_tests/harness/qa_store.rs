//! QA-AUDIT-NEXT-A (b3)/(h): read a COPY of a daemon's session audit folder with the audit crate
//! (aw_util's open_copy: the live folder and its lock are never touched) and print the store's own
//! figures. Env: QA_DATA (data dir), QA_SID (session hex), QA_SCRATCH (a new folder for the copy).
//! Scratch copy only.
#[path = "aw_util.rs"]
mod aw_util;
#[allow(unused)]
mod common;

#[test]
fn qa_read_store() {
    let data = std::path::PathBuf::from(std::env::var("QA_DATA").unwrap());
    let sid = std::env::var("QA_SID").unwrap();
    let scratch = std::path::PathBuf::from(std::env::var("QA_SCRATCH").unwrap());
    std::fs::create_dir_all(&scratch).unwrap();
    let (h, rep, id) = aw_util::open_copy(&data, &sid, &scratch);
    let m = h.member().expect("member");
    let cps: Vec<u64> = m.own().checkpoints().iter().map(|c| c.head.author_seq).collect();
    let st = h.status().ok();
    let (nums, twice) = aw_util::own_numbers(&h, &id);
    let verified = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| format!("{:?}", aw_util::verify_all(&h, &id)).len())).is_ok();
    println!(
        "QASTORE {}",
        serde_json::json!({
            "open_report": format!("{rep:?}"),
            "segment": m.segment(),
            "own_seq": m.own().seq(),
            "own_checkpoints": cps,
            "last_own_checkpoint": cps.last(),
            "archive_files": st.as_ref().map(|s| s.archive_files),
            "seals": st.as_ref().map(|s| s.seals),
            "own_numbers_held": nums.len(),
            "own_numbers_max": nums.last(),
            "signed_twice": twice,
            "verifies": verified,
        })
    );
}
