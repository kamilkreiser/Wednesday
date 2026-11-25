//! QA-POLICY-AT item 2 (size and time): the worst shapes of `@` the check could build, each at most 64 KiB, through
//! `Bash` and free text: classify + decide + the three owner columns + both-agree (t28's five columns), smallest of
//! five. The SAME file at base and head, debug and release. Prints one line per shape: answer codes and the time.
#![cfg(unix)]
mod bypass_common;
mod common;
use bypass_common::*;
use coagent_policy::*;
use common::*;
use serde_json::json;
use std::collections::BTreeSet;
use std::time::{Duration, Instant};

fn short(d: &Decision) -> String {
    match d {
        Decision::Allow { .. } => "A".into(),
        Decision::Ask { card } => format!("Q{:?}", card.tier),
        Decision::Deny { reason: DenyReason::TooLargeToCheck { .. } } => "L".into(),
        Decision::Deny { reason: DenyReason::Excluded } => "X".into(),
        Decision::Deny { .. } => "D".into(),
    }
}

#[test]
fn qpa_time() {
    let fx = mode_fixture("qpa-time");
    let st = fx.state_with(vec!["**/.env*".to_string()]);
    let ov = |t: TerminalCommands| OwnerAllow { bound_sessions: [SESSION.to_string()].into_iter().collect::<BTreeSet<_>>(), terminal: t };
    let k = 64 * 1024;
    let cut = |s: String| -> String { s.chars().take(k).collect::<String>().chars().rev().skip_while(|_| false).collect::<String>().chars().rev().collect() };
    let fit = |s: String| -> String {
        let mut s = s;
        while s.len() > k {
            s.pop();
        }
        s
    };
    let _ = cut;
    let shapes: Vec<(&str, &str, String)> = vec![
        ("at", "Bash", "@".repeat(k)),
        ("atx", "Bash", fit("@x ".repeat(k / 3))),
        ("ata/", "Bash", fit("@a/".repeat(k / 3))),
        ("a@ one word", "Bash", fit("a@".repeat(k / 2))),
        ("chain x0@x1@..", "Bash", fit((0..20000).map(|i| format!("x{i}")).collect::<Vec<_>>().join("@"))),
        ("words w@i", "Bash", fit((0..20000).map(|i| format!("w@{i}")).collect::<Vec<_>>().join(" "))),
        ("words i@i/i/i", "Bash", fit((0..20000).map(|i| format!("{i}@{i}/{i}/{i}")).collect::<Vec<_>>().join(" "))),
        ("quoted '@x'", "Bash", fit((0..20000).map(|i| format!("'@x{i}'")).collect::<Vec<_>>().join(" "))),
        ("ansi $'@'", "Bash", fit((0..20000).map(|i| format!("$'\\x40{i}'")).collect::<Vec<_>>().join(" "))),
        ("ps @", "PowerShell", fit("@a\\".repeat(k / 3))),
        ("untaught @x", "MadeUpTool", fit("@x ".repeat(k / 3))),
        ("ws at", "WebSearch", "@".repeat(k)),
        ("agent atx", "Agent", fit("@x ".repeat(k / 3))),
        ("control ax", "Bash", fit("ax ".repeat(k / 3))),
    ];
    for (name, tool, text) in &shapes {
        assert!(text.len() <= k);
        let input = match *tool {
            "WebSearch" => json!({ "query": text }),
            "Agent" => json!({ "prompt": text, "description": "d" }),
            _ => json!({ "command": text }),
        };
        let mut best = Duration::MAX;
        let mut codes = String::new();
        for _ in 0..5 {
            let t = Instant::now();
            let h = fx.hook_in(&fx.ws, tool, input.clone());
            let a = classify(&h, HostOs::Posix, &fx.env(), &PosixNormaliser);
            let f = owner_input_facts(&h);
            let d0 = decide_with_owner_allow(&a, &st, None, &f, Surface::Console, NOW);
            let d1 = decide_with_owner_allow(&a, &st, Some(&ov(TerminalCommands::StillAsk)), &f, Surface::Console, NOW);
            let d2 = decide_with_owner_allow(&a, &st, Some(&ov(TerminalCommands::Allowed)), &f, Surface::Console, NOW);
            let d3 = with_mode(&a, &st, &live_shell());
            let d4 = decide(&a, &st, Surface::Console, NOW);
            let e = t.elapsed();
            best = best.min(e);
            codes = [&d0, &d1, &d2, &d3, &d4].iter().map(|d| short(d)).collect::<Vec<_>>().join(" ");
        }
        eprintln!("QPA-TIME {:<16} {:<10} len={:<6} {} smallest-of-5 {:?}", name, tool, text.len(), codes, best);
    }
}
