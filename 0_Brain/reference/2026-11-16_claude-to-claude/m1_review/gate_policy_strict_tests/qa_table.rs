//! Independent QA gate: a decision table that compiles on BOTH main (c9a6653) and the branch, so the two can be
//! compared row by row ("nothing was lowered"). Uses only the public API both share. Writes one TSV line per decision
//! to $QA_TABLE_OUT: name, input, state, rank, batchable, session-option, delay, summary.
#![cfg(unix)]
mod common;
use coagent_policy::*;
use common::*;
use serde_json::{json, Value};
use std::io::Write;

const NAMES: &[&str] = &[
    // host 2.1.325
    "Task", "Bash", "CronCreate", "CronDelete", "CronList", "DesignSync", "Edit", "EnterWorktree", "ExitWorktree",
    "ListAgents", "Monitor", "NotebookEdit", "PushNotification", "Read", "RemoteTrigger", "ReportFindings",
    "ScheduleWakeup", "SendMessage", "Skill", "TaskStop", "ToolSearch", "WebFetch", "WebSearch", "Workflow", "Write",
    // docs-only
    "Agent", "Artifact", "AskUserQuestion", "EndConversation", "EnterPlanMode", "ExitPlanMode", "Glob", "Grep",
    "ListMcpResourcesTool", "LSP", "PowerShell", "ReadMcpResourceTool", "SendFeedback", "SendUserFile",
    "ShareOnboardingGuide", "SubagentHandback", "TaskCreate", "TaskGet", "TaskList", "TaskOutput", "TaskUpdate",
    "TodoWrite", "WaitForMcpServers",
    // design-only arms
    "NotebookRead", "LS", "MultiEdit",
    // own and third-party mcp
    "mcp__plugin_coagent_link__share", "mcp__plugin_coagent_link__send", "mcp__plugin_coagent_link__wait",
    "mcp__github__list", "mcp__srv__exec", "mcp____", "mcp__a__b__c", "mcp__",
    // made-up and variants
    "", "MadeUpTool", "read", "READ", "Read ", "agent", "todowrite", "Bash ", "bash", "Rеad",
];

fn inputs(fx: &Fx) -> Vec<(String, Value)> {
    let f = fx.ws.join("README.md");
    let f = f.to_str().unwrap();
    let o = fx.outside.join("secret.txt");
    let o = o.to_str().unwrap();
    let ssh = fx.home.join(".ssh/id_rsa");
    let ssh = ssh.to_str().unwrap();
    let env = fx.ws.join(".env");
    let env = env.to_str().unwrap();
    let ws = fx.ws.to_str().unwrap();
    vec![
        ("empty".into(), json!({})),
        ("prompt".into(), json!({"prompt": "list files"})),
        ("read-ws".into(), json!({"file_path": f})),
        ("write-ws".into(), json!({"file_path": f, "content": "x"})),
        ("read-out".into(), json!({"file_path": o})),
        ("read-ssh".into(), json!({"file_path": ssh})),
        ("read-env".into(), json!({"file_path": env})),
        ("nb-ws".into(), json!({"notebook_path": f})),
        ("search-ws".into(), json!({"path": ws, "pattern": "*"})),
        ("url".into(), json!({"url": "https://example.com/a"})),
        ("query".into(), json!({"query": "q"})),
        ("cmd-ls".into(), json!({"command": "ls"})),
        ("cmd-npm".into(), json!({"command": "npm test", "description": "test"})),
        ("cmd-rc".into(), json!({"command": "echo x >> ~/.zshrc"})),
        ("cmd-sandbox".into(), json!({"command": "ls", "dangerouslyDisableSandbox": true})),
        ("iso-wt".into(), json!({"prompt": "p", "isolation": "worktree"})),
        ("iso-remote".into(), json!({"prompt": "p", "isolation": "remote"})),
        ("iso-odd".into(), json!({"prompt": "p", "isolation": "Remote"})),
        ("named".into(), json!({"prompt": "p", "name": "a"})),
        ("action-remove".into(), json!({"action": "remove", "discard_changes": true})),
        ("todos".into(), json!({"todos": [{"content": "a", "status": "pending"}]})),
        ("content".into(), json!({"content": "hello"})),
        ("nested-cmd".into(), json!({"params": {"command": "ls"}})),
        ("string".into(), json!("x")),
        ("null".into(), json!(null)),
    ]
}

fn row(d: &Decision) -> (u8, bool, bool, u8, String) {
    match d {
        Decision::Allow { why } => {
            let s = format!("{why:?}");
            let s = s.split([' ', '{', '(']).next().unwrap_or("").to_string();
            (0, false, false, 0, format!("Allow:{s}"))
        }
        Decision::Ask { card } => {
            let t = match card.tier {
                Tier::T0 => 1,
                Tier::T1 => 2,
                Tier::T2 => 3,
                Tier::T3 => 4,
            };
            let afs = card.options.iter().any(|o| matches!(o, CardOption::AllowForSession(_)));
            (t, card.batchable, afs, card.read_delay_secs, format!("Ask:{:?}:{:?}", card.tier, card.kind))
        }
        Decision::Deny { reason } => {
            let s = format!("{reason:?}");
            let s = s.split([' ', '{', '(']).next().unwrap_or("").to_string();
            (10, false, false, 0, format!("Deny:{s}"))
        }
    }
}

#[test]
fn qa_decision_table() {
    let Some(out) = std::env::var_os("QA_TABLE_OUT") else {
        eprintln!("QA_TABLE_OUT not set: skipped");
        return;
    };
    let fx = fixture("qa-table");
    let mut w = std::io::BufWriter::new(std::fs::File::create(out).unwrap());
    let mut n = 0;
    for name in NAMES {
        for (il, input) in inputs(&fx) {
            let mut a = classify(&fx.hook(name, input.clone()), HostOs::Posix, &fx.env(), &PosixNormaliser);
            a.share_flagged = Some(false);
            // every_mode plus: a plain state (no approval) on each surface
            let mut states = every_mode(&fx, &a);
            for surface in [Surface::Console, Surface::TerminalPrompt, Surface::None] {
                states.push((format!("plain surface={surface:?}"), fx.state(), surface));
            }
            for (sl, st, surface) in states {
                let d = decide(&a, &st, surface, NOW);
                let (r, b, s, dl, sum) = row(&d);
                writeln!(w, "{name:?}\t{il}\t{sl}\t{r}\t{}\t{}\t{dl}\t{sum}", b as u8, s as u8).unwrap();
                n += 1;
            }
        }
    }
    eprintln!("QA table rows: {n}");
}
