//! QA-POLICY-AT-R2 probe (the check's own file; never in a tree whose whole suite is run).
//! Reads rows (JSON lines) from $QPA2_ROWS, writes one JSON line per row and state to $QPA2_OUT.
//! Each row: {"id", "tool", "text"} or {"id", "tool", "input": {...}}, optional "states" (default all three),
//! optional "cwd": "home" | "root" | "ws". `<home>`, `<ws>`, `<root>` in texts are replaced by the fixture's paths.
//! Columns as `t28`: no view (asserted = decide), owner ALLOW StillAsk, owner ALLOW Allowed, both-agree live_shell.
#![cfg(unix)]
mod bypass_common;
mod common;
mod owner_common;
use bypass_common::*;
use coagent_policy::*;
use common::*;
use owner_common::*;
use serde_json::{json, Value};
use std::io::Write;

fn class(t: &str) -> String {
    if t == RefusedClass::Credential.text() { "C".into() }
    else if t == RefusedClass::AgentProgramWord.text() { "P".into() }
    else if t.starts_with("writes a file outside the workspace, or under .git") { "G".into() }
    else { format!("[{t}]") }
}

fn code(d: &Decision) -> String {
    match d {
        Decision::Allow { why: AllowWhy::OwnerChoseAllow } => "U".into(),
        Decision::Allow { why: AllowWhy::Bypass { .. } } => "B".into(),
        Decision::Allow { why } => format!("allow[{why:?}]"),
        Decision::Ask { card } => {
            let mut s = format!("a{}", format!("{:?}", card.tier).trim_start_matches('T'));
            if card.reasons.iter().any(|r| matches!(r, Reason::CredentialPath(_))) { s.push_str("+C"); }
            s
        }
        Decision::Deny { reason: DenyReason::Excluded } => "X".into(),
        Decision::Deny { reason: DenyReason::HardDeny { .. } } => "H".into(),
        Decision::Deny { reason: DenyReason::TooLargeToCheck { .. } } => "L".into(),
        Decision::Deny { reason: DenyReason::RefusedInAllow { reason } } => format!("r{}", class(reason)),
        Decision::Deny { reason: DenyReason::BypassRefused { reason } } => format!("b{}", class(reason)),
        d => format!("{d:?}"),
    }
}

#[test]
fn qpa2_probe() {
    let rows_path = std::env::var("QPA2_ROWS").expect("QPA2_ROWS");
    let out_path = std::env::var("QPA2_OUT").expect("QPA2_OUT");
    let fx = mode_fixture("qpa2-probe");
    let sub = |s: &str| s.replace("<home>", fx.home.to_str().unwrap()).replace("<ws>", fx.ws.to_str().unwrap()).replace("<root>", fx.root.to_str().unwrap());
    let states: Vec<(&str, State)> = vec![
        ("nothing", fx.state()),
        ("env", fx.state_with(vec!["**/.env*".to_string()])),
        ("secret", fx.state_with(vec!["**/secret/**".to_string()])),
        ("examplecom", fx.state_with(vec!["**/example.com/**".to_string()])),
    ];
    let mut out = std::fs::File::create(&out_path).unwrap();
    writeln!(out, "{}", json!({"fixture_root": fx.root.to_str().unwrap(), "home": fx.home.to_str().unwrap(), "ws": fx.ws.to_str().unwrap()})).unwrap();
    let mut n = 0;
    for line in std::fs::read_to_string(&rows_path).unwrap().lines() {
        if line.trim().is_empty() { continue; }
        let r: Value = serde_json::from_str(line).unwrap();
        let tool = r["tool"].as_str().unwrap();
        let text = r.get("text").and_then(|t| t.as_str()).map(sub);
        let input: Value = match (&text, r.get("input")) {
            (_, Some(v)) => serde_json::from_str(&sub(&v.to_string())).unwrap(),
            (Some(t), None) => match tool {
                "WebSearch" => json!({ "query": t }),
                "Agent" => json!({ "prompt": t, "description": "d" }),
                _ => json!({ "command": t }),
            },
            _ => panic!("row without text or input"),
        };
        let cwd = match r.get("cwd").and_then(|c| c.as_str()) {
            Some("home") => fx.home.clone(),
            Some("root") => fx.root.clone(),
            _ => fx.ws.clone(),
        };
        let want: Vec<String> = r.get("states").and_then(|s| s.as_array()).map(|a| a.iter().map(|x| x.as_str().unwrap().to_string()).collect())
            .unwrap_or_else(|| vec!["nothing".into(), "env".into(), "secret".into()]);
        let h = fx.hook_in(&cwd, tool, input.clone());
        let a = classify(&h, HostOs::Posix, &fx.env(), &PosixNormaliser);
        let f = owner_input_facts(&h);
        let pieces_bash = text.as_ref().map(|t| shell::scan_execute(t, ShellKind::Bash).pieces.len());
        // free text as the gate bounds it (approximation: serde_json's compact form of the input, sorted keys)
        let jt: String = serde_json::to_string(&input).unwrap().chars().take(action::MAX_FREE_TEXT_CHARS).collect();
        let jp = shell::scan_execute(&jt, ShellKind::Bash).pieces;
        let env_pos = jp.iter().position(|p| p == ".env").map(|i| i + 1);
        for (sn, st) in &states {
            if !want.iter().any(|w| w == sn) { continue; }
            let nov = decide_with_owner_allow(&a, st, None, &f, Surface::Console, NOW);
            let dec = decide(&a, st, Surface::Console, NOW);
            let still = with_owner_facts(&a, &f, st, &owner_still_ask(), Surface::Console);
            let allowed = with_owner_facts(&a, &f, st, &owner_terminal(), Surface::Console);
            let both = with_mode(&a, st, &live_shell());
            let cols = [&nov, &still, &allowed, &both].iter().map(|d| code(d)).collect::<Vec<_>>().join(" ");
            let detail = |d: &Decision| match d { Decision::Ask { card } => format!("ask {:?} {:?}", card.tier, card.reasons), d => format!("{d:?}") };
            writeln!(out, "{}", json!({
                "id": r["id"], "tool": tool, "state": sn, "text": r.get("text"), "input": r.get("input"),
                "cols": cols, "nov_eq_decide": nov == dec, "pieces_bash": pieces_bash, "pieces_json": jp.len(), "env_piece_pos": env_pos,
                "nov": detail(&nov), "allowed": detail(&allowed),
            })).unwrap();
            n += 1;
        }
    }
    eprintln!("QPA2-PROBE {n} lines -> {out_path}");
}
