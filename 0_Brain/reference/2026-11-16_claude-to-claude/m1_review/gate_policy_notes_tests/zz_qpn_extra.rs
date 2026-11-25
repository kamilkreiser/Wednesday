//! QA-POLICY-NOTES (independent check): what item 2's `@` cut and extension cut also catch (stricter side), owner
//! `StillAsk` and `Allowed`, Console, sandbox On; and the mode-absent answer for the same rows. Recorded, not asserted.
mod qpn_adapter;
mod qpn_gen;
use coagent_policy::*;
use qpn_gen::*;
use serde_json::json;

#[test]
fn qpn_extra() {
    let fx = fixture();
    let sts = states(&fx);
    let st = sts.iter().find(|(n, _)| n.starts_with("ex=none exn=0 gx=none nogrant link=Open v=0 ")).unwrap().1.clone();
    let ws = fx.ws.to_str().unwrap().to_string();
    for cmd in [
        "ssh claude@build-host uptime",
        "git commit --author=claude@example.com -m x",
        "scp f coagent@host:/tmp/",
        "rm -f claude.exe",
        "cat docs/claude.cmd",
        "echo coagent.bat",
        "npm i -g @anthropic-ai/claude-code@1.2.3",
        "pip install claude-code",
    ] {
        let t = json!({"session_id": SESSION, "cwd": ws, "hook_event_name": "PreToolUse", "tool_name": "Bash",
                       "tool_input": {"command": cmd}}).to_string();
        let hi = HookInput::parse(&t).unwrap();
        let a = classify(&hi, HostOs::Posix, &env(&fx), &PosixNormaliser);
        let mut out = vec![];
        for term in [TerminalCommands::StillAsk, TerminalCommands::Allowed] {
            let m = OwnerAllow { bound_sessions: [SESSION.to_string()].into_iter().collect(), terminal: term };
            let d = qpn_adapter::owner(&a, &hi, &st, Some(&m), Surface::Console, NOW);
            out.push(dtext(&d).chars().take(90).collect::<String>());
        }
        let d = decide(&a, &st, Surface::Console, NOW);
        let words: Vec<String> = scan_words(&a);
        eprintln!("EXTRA `{cmd}` words {words:?} | StillAsk: {} | Allowed: {} | decide: {:?}", out[0], out[1], match &d { Decision::Ask { card } => format!("ask {:?}", card.tier), o => format!("{o:?}") });
    }
}
