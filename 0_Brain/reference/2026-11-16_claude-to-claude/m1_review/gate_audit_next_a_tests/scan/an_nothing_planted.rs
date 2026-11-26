//! Lane AUDIT-NEXT-A item 3 (R2-N3): a seal answered `NothingToSeal` says which of its two causes
//! the member's own figures show (own seq, and the last own checkpoint's number, read before the
//! call with no folder listing): equal → nothing new since the last filed point; own seq above it
//! → step 0's checkpoint could not be written. Row, `sealed: false`, `calls: 1` unchanged. Made by
//! folder rights only. Red control: `nothing_text_guessed` (AN-3).
#[path = "aw_util.rs"]
mod aw_util;
mod common;

use std::os::unix::fs::PermissionsExt;
use std::path::Path;

use aw_util::*;
use common::*;
use serde_json::{json, Value};

const NOTHING_NEW: &str = "not sealed: nothing new since the last filed point";
const COULD_NOT_WRITE: &str = "not sealed: the log could not write its checkpoint; fix the cause (see status.audit), then give the command again";

fn mode(p: &Path, m: u32) {
    std::fs::set_permissions(p, std::fs::Permissions::from_mode(m)).unwrap();
}

fn audit(run: &mut Run, i: usize) -> Value {
    run.status(i)["audit"].clone()
}

fn pair() -> (Run, usize, String) {
    let mut run = Run::new("annothing");
    let a = run.daemon("a", &["--audit"]);
    let b = run.daemon("b", &[]);
    run.pair(a, b);
    let sid = session_hex(&run.status(a));
    (run, a, sid)
}

fn check_nothing(seal: &Value, text: &str) {
    assert_eq!(seal["ok"], true, "{seal}");
    assert_eq!(seal["result"]["row"], "10/14 (NothingToSeal)", "{seal}");
    assert_eq!(seal["result"]["sealed"], false, "{seal}");
    assert_eq!(seal["result"]["calls"], 1, "never retried: {seal}");
    assert_eq!(seal["result"]["action"], text, "{seal}");
}

#[test]
fn nothing_to_seal_says_what_it_knows() {
    // (a) a healthy store, two seals with nothing between them
    let (mut run, a, sid) = pair();
    let r = run.ctl(a, "send", json!({"kind": "chat", "text": "AN3 one"}));
    assert_eq!(r["ok"], true, "{r}");
    let first = run.ctl(a, "audit_seal", json!({}));
    assert_eq!(first["result"]["sealed"], true, "{first}");
    let before = audit(&mut run, a);
    let second = run.ctl(a, "audit_seal", json!({}));
    println!("AN3 (a) second seal: {second}");
    check_nothing(&second, NOTHING_NEW);
    let after = audit(&mut run, a);
    assert_eq!(after["last_seal"]["action"], NOTHING_NEW, "{after}");
    for k in ["segment", "archive_files", "archive_bytes", "own_seq"] {
        assert_eq!(after[k], before[k], "{k} unchanged");
    }
    let _ = sid;
    run.finish();

    // (b) the first check's `store_unwritable`: store/ 0500, a send refused, then the seal
    let (mut run, a, sid) = pair();
    let d = folder(&run.dir(a), &sid);
    let r = run.ctl(a, "send", json!({"kind": "chat", "text": "AN3 two"}));
    assert_eq!(r["ok"], true, "{r}");
    let before = audit(&mut run, a);
    mode(&d.join("store"), 0o500);
    let refused = run.ctl(a, "send", json!({"kind": "chat", "text": "AN3 three"}));
    let seal = run.ctl(a, "audit_seal", json!({}));
    let during = audit(&mut run, a);
    mode(&d.join("store"), 0o700);
    println!("AN3 (b) send: {refused}");
    println!("AN3 (b) seal: {seal}");
    assert_eq!(refused["ok"], false, "{refused}");
    check_nothing(&seal, COULD_NOT_WRITE);
    assert_eq!(during["last_seal"]["action"], COULD_NOT_WRITE, "{during}");
    for k in ["segment", "archive_files", "archive_bytes"] {
        assert_eq!(during[k], before[k], "{k} unchanged");
    }
    run.finish();
}
// planted: KamilKreiser Kamils-MBP Side Projects
