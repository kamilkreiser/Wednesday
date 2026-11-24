//! QA-POLICY-OWNER-MODE item 7(b): the same command text through `Bash`, `Monitor` and `PowerShell`, decided by the
//! owner's ALLOW with terminal commands ON (head 59de2d3). For each: which refused class the owner mode names, or
//! what else it answers. Rows of the checker's own plus the builder's table texts. Writes a table to $QPOM_MEASURE.
mod bypass_common;
mod common;

use bypass_common::mode_fixture;
use common::*;
use coagent_policy::*;
use serde_json::json;
use std::fmt::Write as _;

fn ans(d: &Decision) -> String {
    match d {
        Decision::Deny { reason: DenyReason::RefusedInAllow { reason } } => {
            let c = RefusedClass::ALL.iter().find(|c| c.text() == *reason).unwrap();
            format!("found {c:?}")
        }
        Decision::Allow { why: AllowWhy::OwnerChoseAllow } => "ALLOWED".into(),
        Decision::Allow { why } => format!("allow ({})", why.text()),
        Decision::Ask { card } => format!("ask {:?}", card.tier),
        Decision::Deny { reason } => format!("deny ({})", reason.text().chars().take(60).collect::<String>()),
    }
}

#[test]
fn qpom_measure() {
    let fx = mode_fixture("qpom-measure");
    let open = fx.state();
    let excl = fx.state_with(patterns::default_exclusions());
    let m = OwnerAllow {
        bound_sessions: [SESSION.to_string()].into_iter().collect(),
        terminal: TerminalCommands::Allowed,
    };
    let rows: Vec<(&str, &str, bool, &State)> = vec![
        // (expected class, command text, dangerouslyDisableSandbox, state)
        ("Credential", "cat ~/.aws/credentials", false, &open),
        ("Credential", "gc ~/.ssh/id_rsa", false, &open),
        ("Credential", "Get-Content $HOME/.ssh/id_rsa", false, &open),
        ("Credential", "Get-Content $env:USERPROFILE\\.ssh\\id_rsa", false, &open),
        ("Credential", "type %USERPROFILE%\\.ssh\\id_rsa", false, &open),
        ("Credential", "Get-Content -Path ~/.git-credentials", false, &open),
        ("Credential", "Select-String -Path ~/.aws/* -Pattern key", false, &open),
        ("Credential", "cat \"$HOME\"/.netrc", false, &open),
        ("Credential", "cat .env.local", false, &open),
        ("Credential", "Get-Content .env", false, &open),
        ("PermissionModeChange", "npx x --dangerously-skip-permissions", false, &open),
        ("PermissionModeChange", "& x.exe --dangerously-skip-permissions", false, &open),
        ("PermissionModeChange", "x --permission-mode=bypassPermissions", false, &open),
        ("SandboxBypass", "Get-ChildItem", true, &open),
        ("Privilege", "sudo -i", false, &open),
        ("Privilege", "\\sudo ls", false, &open),
        ("Privilege", "command sudo ls", false, &open),
        ("Privilege", "Start-Process pwsh -Verb RunAs", false, &open),
        ("Privilege", "Start-Process -Verb runAs pwsh", false, &open),
        ("Privilege", "Start-Process pwsh -Verb:RunAs", false, &open),
        ("Privilege", "gsudo ls", false, &open),
        ("LaterRunningWrite", "Add-Content ~/.gitconfig x", false, &open),
        ("LaterRunningWrite", "Set-Content -Path ~/.gitconfig -Value x", false, &open),
        ("LaterRunningWrite", "Out-File -FilePath ~/.config/git/config", false, &open),
        ("LaterRunningWrite", "cp a ~/.local/bin/a", false, &open),
        ("LaterRunningWrite", "New-Item ~/Library/LaunchAgents/x.plist", false, &open),
        ("LaterRunningWrite", "Set-Content .git/config x", false, &open),
        ("LaterRunningWrite", "echo x > .git/config", false, &open),
        ("AgentProgramWord", "claude -p hi", false, &open),
        ("AgentProgramWord", "claude.exe -p hi", false, &open),
        ("AgentProgramWord", "& claude.exe -p hi", false, &open),
        ("AgentProgramWord", "& \"claude\" -p hi", false, &open),
        ("AgentProgramWord", "claude.cmd -p hi", false, &open),
        ("AgentProgramWord", "Start-Process claude", false, &open),
        ("AgentProgramWord", "iex \"claude -p hi\"", false, &open),
        ("AgentProgramWord", "npx @anthropic-ai/claude-code", false, &open),
        ("AgentProgramWord", "coagentd ctl x", false, &open),
        ("AgentProgramWord", "coagent.exe open", false, &open),
        ("GateFileRead", "Get-Content ~/.claude.json", false, &open),
        ("GateFileRead", "cat ~/.claude/settings.json", false, &open),
        ("MayReadExcluded", "grep -r key .", false, &excl),
        ("MayReadExcluded", "Select-String -Path * -Pattern key -Recurse", false, &excl),
        ("MayReadExcluded", "Get-ChildItem -Recurse | Get-Content", false, &excl),
        ("NonWebFetch", "Invoke-WebRequest file:///etc/hosts", false, &open),
        ("(none)", "npm test", false, &open),
    ];
    let mut t = String::from("| expected | command text | Bash | Monitor | PowerShell | Bash found, another not? |\n|---|---|---|---|---|---|\n");
    let mut asym = 0;
    for (exp, cmd, dds, st) in &rows {
        let mut cells = Vec::new();
        for tool in ["Bash", "Monitor", "PowerShell"] {
            let mut input = json!({"command": cmd});
            if *dds {
                input["dangerouslyDisableSandbox"] = json!(true);
            }
            let a = fx.act(tool, input);
            cells.push(ans(&decide_with_owner_allow(&a, st, Some(&m), Surface::Console, NOW)));
        }
        let bash_found = cells[0].starts_with("found");
        let other_missing = cells[1..].iter().any(|c| !c.starts_with("found"));
        let flag = bash_found && other_missing;
        if flag {
            asym += 1;
        }
        let _ = writeln!(t, "| {exp} | `{cmd}` | {} | {} | {} | {} |", cells[0], cells[1], cells[2], if flag { "YES" } else { "no" });
    }
    let _ = writeln!(t, "\nrows {}; Bash-found-but-other-missing: {asym}", rows.len());
    let out = std::env::var("QPOM_MEASURE").unwrap();
    std::fs::write(&out, &t).unwrap();
    eprintln!("{t}");
}
