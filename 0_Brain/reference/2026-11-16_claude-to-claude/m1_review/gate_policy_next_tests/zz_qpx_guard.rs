//! QA-POLICY-NEXT item 3 probe (the check's own; never committed): what `classify` makes of relative working-folder
//! spellings, which arm of `owner_common::fixture_facts`' guard fires, and what the hook's own facts say.
//! Output to $QPX_OUT, one line per spelling. Compiled in a tree at the base (no guard) and one at the head.
#![cfg(unix)]
mod bypass_common;
mod common;
mod owner_common;
use bypass_common::*;
use coagent_policy::*;
use common::*;
use owner_common::*;
use serde_json::json;
use std::io::Write;

fn trunc(s: &str) -> String {
    if s.len() > 140 {
        format!("{}…[{} bytes]", &s[..100], s.len())
    } else {
        s.to_string()
    }
}

#[test]
fn qpx_guard() {
    let out = std::env::var("QPX_OUT").expect("QPX_OUT");
    let mut f = std::fs::File::create(&out).unwrap();
    let fx = mode_fixture("qpx-guard");
    let root = fx.root.to_str().unwrap().to_string();
    let base_canon = std::fs::canonicalize(tmp_base()).unwrap();
    writeln!(f, "tmp_base() = {:?}; canonical {:?}", tmp_base(), base_canon).unwrap();
    let long300 = "d/".repeat(150);
    let long5000 = format!("{}x", "abcdefghi/".repeat(500));
    let deep70 = "a/".repeat(70);
    // a relative spelling of the fixture's own workspace (the base path without its leading '/')
    let ws_rel = fx.ws.to_str().unwrap().trim_start_matches('/').to_string();
    let spellings: Vec<(&str, String)> = vec![
        ("builder", "rel".into()),
        ("builder", "rel/dir".into()),
        ("builder", "./x".into()),
        ("builder", "../up".into()),
        ("builder", "~/x".into()),
        ("brief", ".".into()),
        ("brief", "..".into()),
        ("brief", "x/../..".into()),
        ("brief", "rel/".into()),
        ("brief", "./".into()),
        ("brief", long300.clone()),
        ("brief", "y".repeat(300)),
        ("brief", long5000.clone()),
        ("brief", "a//b".into()),
        ("brief", "a\tb".into()),
        ("brief", "a\u{1b}[0mb".into()),
        ("brief", "a\\xffb".into()),
        ("brief", "%FF/x".into()),
        ("brief", "~".into()),
        ("brief", "~nobody/x".into()),
        ("brief", " ".into()),
        ("brief", "C:x".into()),
        ("brief", "\\x".into()),
        ("mine", deep70.clone()),
        ("mine", "net/x".into()),
        ("mine", "nosuch/../x".into()),
        ("mine", "a\u{0}b".into()),
        ("mine", ws_rel.clone()),
        ("mine", "tmp".into()),
        ("control", "".into()),
        ("control-abs", fx.ws.to_str().unwrap().into()),
        ("control-abs", fx.home.to_str().unwrap().into()),
        ("control-abs", "/".into()),
        ("control-abs", "/private/tmp/claude-501/qpx/outside2".into()),
    ];
    for (who, cwd) in &spellings {
        let h = fx.hook_in(std::path::Path::new(cwd), "Bash", json!({"command": "npm test"}));
        let a = classify(&h, HostOs::Posix, &fx.env(), &PosixNormaliser);
        let hook_facts = owner_input_facts(&h);
        let r = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| fixture_facts(&a)));
        let arm = match &r {
            Ok(ff) => format!(
                "NO PANIC gives {ff:?} -> {}",
                if *ff == hook_facts { "= hook facts" } else { "DIFFERS from hook facts (SILENT)" }
            ),
            Err(p) => {
                let m = p
                    .downcast_ref::<String>()
                    .cloned()
                    .or_else(|| p.downcast_ref::<&str>().map(|s| s.to_string()))
                    .unwrap_or_default();
                if m.contains("outside the fixture base") {
                    "PANIC arm (b)".to_string()
                } else if m.contains("an action from the relative hook cwd") {
                    "PANIC arm (a)".to_string()
                } else {
                    format!("PANIC other: {}", trunc(&m))
                }
            }
        };
        let cwd_dbg = trunc(&format!("{:?}", a.cwd)).replace(&root, "<root>");
        writeln!(
            f,
            "GUARD | {who} | cwd {} | a.cwd = {} | hook facts {:?} | {}",
            trunc(&format!("{cwd:?}")).replace(&root, "<root>"),
            cwd_dbg,
            hook_facts,
            arm
        )
        .unwrap();
    }
}
