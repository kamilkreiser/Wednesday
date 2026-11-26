use serde_json::{json, Value};
fn new(a: &Option<Value>) -> bool { a.as_ref().is_some_and(|v| v["ok"] == true) }
fn old(a: &Option<Value>) -> bool { a.is_some() }
fn main() {
    let cases: Vec<(&str, Option<Value>)> = vec![
        ("ok true", Some(json!({"ok": true, "result": {}}))),
        ("ok false (daemon stopping)", Some(json!({"ok": false, "error": {"code": "internal", "message": "daemon stopping"}}))),
        ("ok missing", Some(json!({"result": {}}))),
        ("non-object array", Some(json!([true]))),
        ("non-object bool true", Some(json!(true))),
        ("ok string \"true\"", Some(json!({"ok": "true"}))),
        ("ok number 1", Some(json!({"ok": 1}))),
        ("ok null", Some(json!({"ok": null}))),
        ("None (no answer)", None),
    ];
    for (n, c) in &cases { println!("{:28} new={} old={} new=>old:{}", n, new(c), old(c), !new(c) || old(c)); }
}
