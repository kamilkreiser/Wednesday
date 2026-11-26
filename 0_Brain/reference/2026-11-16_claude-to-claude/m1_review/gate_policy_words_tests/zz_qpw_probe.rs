//! QA-POLICY-WORDS probe (this check's own harness; lives only in the probe trees `p184` and `phead`, never in a tree
//! whose whole suite is run). Rows: JSON lines from $QPW_ROWS; one JSON line per row x state to $QPW_OUT.
//! Row: {"id","tool","text"} (or "input": {...}), "st": ["o","e","s"] (o nothing, e `**/.env*`, s `**/secret/**`),
//! optional "cwd": "ws" (default) | "home" | "root" | "rel" | "empty". Tokens in texts: <home> <ws> <root>
//! <rootparent> (canonical parent of the fixture root) <top2> (first two components of the canonical fixture root).
//! Columns exactly as `t28::cols_of`: no view (checked = decide), owner ALLOW StillAsk, owner ALLOW Allowed,
//! both-agree `live_shell`. Facts from `owner_input_facts` of the very hook; `Surface::Console`; `mode_fixture`.
//! Counts read from the classified Action itself: shell pieces (the Command target's scan) and the InText targets
//! (the free-text pieces the engine actually checks, in order), with the 1-based position of the piece `.env`.
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
use std::path::{Path, PathBuf};

fn refusal_label(t: &str) -> String {
    if t == RefusedClass::Credential.text() {
        "C".into()
    } else if t == RefusedClass::AgentProgramWord.text() {
        "P".into()
    } else if t.contains(".git") {
        "G".into()
    } else {
        format!("[{}]", t.chars().take(40).collect::<String>())
    }
}

fn short(d: &Decision) -> String {
    match d {
        Decision::Allow { why: AllowWhy::OwnerChoseAllow } => "U".into(),
        Decision::Allow { why: AllowWhy::Bypass { .. } } => "B".into(),
        Decision::Allow { why } => format!("allow:{why:?}"),
        Decision::Ask { card } => {
            let cred = card.reasons.iter().any(|r| matches!(r, Reason::CredentialPath(_)));
            format!("a{}{}", format!("{:?}", card.tier).trim_start_matches('T'), if cred { "+C" } else { "" })
        }
        Decision::Deny { reason: DenyReason::Excluded } => "X".into(),
        Decision::Deny { reason: DenyReason::HardDeny { .. } } => "H".into(),
        Decision::Deny { reason: DenyReason::TooLargeToCheck { .. } } => "L".into(),
        Decision::Deny { reason: DenyReason::RefusedInAllow { reason } } => format!("r{}", refusal_label(reason)),
        Decision::Deny { reason: DenyReason::BypassRefused { reason } } => format!("b{}", refusal_label(reason)),
        other => format!("{other:?}"),
    }
}

fn detail(d: &Decision) -> String {
    let s = match d {
        Decision::Ask { card } => format!("ask {:?} {:?}", card.tier, card.reasons),
        other => format!("{other:?}"),
    };
    s.chars().take(400).collect()
}

#[test]
fn qpw_probe() {
    let rows = std::fs::read_to_string(std::env::var("QPW_ROWS").expect("QPW_ROWS")).unwrap();
    let mut out = std::fs::File::create(std::env::var("QPW_OUT").expect("QPW_OUT")).unwrap();
    let fx = mode_fixture("qpw-probe");
    let canon = std::fs::canonicalize(&fx.root).unwrap();
    let rootparent = canon.parent().unwrap().to_path_buf();
    let top2: PathBuf = canon.components().take(3).collect(); // RootDir + two names
    let subst = |s: &str| {
        s.replace("<rootparent>", rootparent.to_str().unwrap())
            .replace("<top2>", top2.to_str().unwrap())
            .replace("<home>", fx.home.to_str().unwrap())
            .replace("<ws>", fx.ws.to_str().unwrap())
            .replace("<root>", fx.root.to_str().unwrap())
    };
    let st_o = fx.state();
    let st_e = fx.state_with(vec!["**/.env*".to_string()]);
    let st_s = fx.state_with(vec!["**/secret/**".to_string()]);
    writeln!(out, "{}", json!({"meta": true, "root": fx.root, "canon_root": canon, "rootparent": rootparent, "top2": top2, "home": fx.home, "ws": fx.ws})).unwrap();
    let mut lines = 0usize;
    for l in rows.lines().filter(|l| !l.trim().is_empty()) {
        let r: Value = serde_json::from_str(l).unwrap();
        let tool = r["tool"].as_str().unwrap();
        let input: Value = if let Some(v) = r.get("input") {
            serde_json::from_str(&subst(&v.to_string())).unwrap()
        } else {
            let t = subst(r["text"].as_str().unwrap());
            match tool {
                "WebSearch" => json!({ "query": t }),
                "Agent" => json!({ "prompt": t, "description": "d" }),
                _ => json!({ "command": t }),
            }
        };
        let cwd: PathBuf = match r.get("cwd").and_then(Value::as_str).unwrap_or("ws") {
            "home" => fx.home.clone(),
            "root" => fx.root.clone(),
            "rel" => PathBuf::from("rel"),
            "empty" => PathBuf::from(""),
            _ => fx.ws.clone(),
        };
        let h = fx.hook_in(Path::new(&cwd), tool, input.clone());
        let a = classify(&h, HostOs::Posix, &fx.env(), &PosixNormaliser);
        let f = owner_input_facts(&h);
        let cmd_pieces: Vec<usize> = a.targets.iter().filter_map(|t| match t {
            Target::Command { scan, .. } => Some(scan.pieces.len()),
            _ => None,
        }).collect();
        let intext: Vec<String> = a.targets.iter().filter_map(|t| match t {
            Target::Path { role: PathRole::InText, path } => Some(match path {
                NormPath::Uncertain { raw, .. } => raw.clone(),
                other => format!("{other:?}"),
            }),
            _ => None,
        }).collect();
        let env_pos = intext.iter().position(|p| p == ".env").map(|i| i + 1);
        let sts: Vec<String> = r.get("st").and_then(Value::as_array)
            .map(|a| a.iter().map(|x| x.as_str().unwrap().to_string()).collect())
            .unwrap_or_else(|| vec!["o".into(), "e".into(), "s".into()]);
        for sn in &sts {
            let st = match sn.as_str() { "o" => &st_o, "e" => &st_e, "s" => &st_s, x => panic!("state {x}") };
            let nov = decide_with_owner_allow(&a, st, None, &f, Surface::Console, NOW);
            let dec = decide(&a, st, Surface::Console, NOW);
            let still = with_owner_facts(&a, &f, st, &owner_still_ask(), Surface::Console);
            let allowed = with_owner_facts(&a, &f, st, &owner_terminal(), Surface::Console);
            let both = with_mode(&a, st, &live_shell());
            let cols = [&nov, &still, &allowed, &both].iter().map(|d| short(d)).collect::<Vec<_>>().join(" ");
            writeln!(out, "{}", json!({
                "id": r["id"], "tool": tool, "st": sn, "cwd": r.get("cwd"), "cols": cols, "nov_eq_decide": nov == dec,
                "cmd_pieces": cmd_pieces, "intext": intext.len(), "env_pos": env_pos,
                "d_nov": detail(&nov), "d_still": detail(&still), "d_allowed": detail(&allowed), "d_both": detail(&both),
            })).unwrap();
            lines += 1;
        }
    }
    eprintln!("QPW-PROBE {lines} lines");
}
