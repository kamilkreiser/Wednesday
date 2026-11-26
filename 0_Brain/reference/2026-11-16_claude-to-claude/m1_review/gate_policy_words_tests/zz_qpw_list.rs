//! QA-POLICY-WORDS probe 2 (own; probe trees only): a PowerShell command on the owner's exact-command list ([7b]),
//! and under a wide grant, in the four columns of `t28` (no view, StillAsk, Allowed, both-agree live_shell).
#![cfg(unix)]
mod bypass_common;
mod common;
mod owner_common;
use bypass_common::*;
use coagent_policy::*;
use common::*;
use owner_common::*;
use serde_json::json;

fn short(d: &Decision) -> String {
    match d {
        Decision::Allow { why } => format!("allow:{why:?}"),
        Decision::Ask { card } => format!("a{}", format!("{:?}", card.tier).trim_start_matches('T')),
        Decision::Deny { reason } => format!("deny:{reason:?}"),
    }
}

#[test]
fn qpw_list_probe() {
    let fx = mode_fixture("qpw-list");
    for (label, tool, shell, cmd, listed, grant) in [
        ("listed", "PowerShell", ShellKind::PowerShell, "npm test", true, false),
        ("listed", "PowerShell", ShellKind::PowerShell, "Remove-Item README.md", true, false),
        ("listed", "Bash", ShellKind::Bash, "npm test", true, false),
        ("not listed", "PowerShell", ShellKind::PowerShell, "npm test", false, false),
        ("wide grant", "PowerShell", ShellKind::PowerShell, "npm test", false, true),
    ] {
        let mut st = fx.state();
        if listed {
            st.add_owner_command(cmd, &fx.ws, shell, &PosixNormaliser).unwrap();
        }
        if grant {
            fx.grant(&mut st, &wide_grant().replace("<ws>", fx.ws.to_str().unwrap())).unwrap();
        }
        let h = fx.hook_in(&fx.ws, tool, json!({ "command": cmd }));
        let a = classify(&h, HostOs::Posix, &fx.env(), &PosixNormaliser);
        let f = owner_input_facts(&h);
        let cols = [
            decide_with_owner_allow(&a, &st, None, &f, Surface::Console, NOW),
            with_owner_facts(&a, &f, &st, &owner_still_ask(), Surface::Console),
            with_owner_facts(&a, &f, &st, &owner_terminal(), Surface::Console),
            with_mode(&a, &st, &live_shell()),
        ];
        eprintln!("QPW-LIST {label} {tool} `{cmd}`: {}", cols.iter().map(short).collect::<Vec<_>>().join(" | "));
    }
}
