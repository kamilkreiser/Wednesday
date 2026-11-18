//! Independent QA gate, POLICY-STRICT (branch m2-policy-strict). Copied into crates/coagent-policy/tests/ of the
//! gate's own scratch copy only. Every `qa_*` test asserts the SAFE outcome; a failing one is a finding.
//! `qa_probe_*` tests PRINT what the gate does (assert only what the docs state).
#![cfg(unix)]
mod common;
use coagent_policy::*;
use common::*;
use serde_json::{json, Value};

/// The 24 names the brief and STATUS say are taught, written out independently of the code (byte-exact).
const TAUGHT: [&str; 24] = [
    "Read", "NotebookRead", "LS", "Glob", "Grep", "Edit", "Write", "MultiEdit", "NotebookEdit", "WebFetch", "WebSearch",
    "mcp__plugin_coagent_link__share", "mcp__plugin_coagent_link__send", "Agent", "Task", "TodoWrite", "TaskCreate",
    "TaskUpdate", "TaskList", "TaskGet", "AskUserQuestion", "EnterPlanMode", "ToolSearch", "CronList",
];
fn taught(n: &str) -> bool {
    TAUGHT.contains(&n)
}

#[test]
fn qa_list_is_exactly_the_expected_names_and_lookup_is_exact() {
    let names: Vec<&str> = KNOWN_TOOLS.iter().map(|k| k.name).collect();
    assert_eq!(names, TAUGHT.to_vec());
    for n in untaught_names() {
        assert!(known_tool(&n).is_none(), "known_tool({n:?}) is Some");
    }
    for n in TAUGHT {
        assert_eq!(known_tool(n).map(|k| k.name), Some(n));
    }
}

fn act(fx: &Fx, tool: &str, input: Value) -> Action {
    classify(&fx.hook(tool, input), HostOs::Posix, &fx.env(), &PosixNormaliser)
}

fn hook_raw(fx: &Fx, tool: &str, tool_input_json: &str) -> HookInput {
    let cwd = serde_json::to_string(fx.ws.to_str().unwrap()).unwrap();
    let s = format!(
        "{{\"session_id\":\"sess-1\",\"cwd\":{cwd},\"hook_event_name\":\"PreToolUse\",\"tool_name\":{},\"tool_input\":{tool_input_json},\"permission_mode\":\"default\"}}",
        serde_json::to_string(tool).unwrap()
    );
    HookInput::parse(&s).unwrap()
}

/// Strict as the brief defines it. Also: options are a subset of {AllowOnce, Deny, DenyWithReason}.
fn is_strict(d: &Decision, surface: Surface) -> Result<(), String> {
    match d {
        Decision::Ask { card } => {
            if surface == Surface::None {
                return Err("asked with no surface".into());
            }
            let wide = card.options.iter().any(|o| {
                !matches!(o, CardOption::AllowOnce | CardOption::Deny | CardOption::DenyWithReason)
            });
            if card.tier != Tier::T3 || card.batchable || card.read_delay_secs != 5 || wide {
                return Err(format!(
                    "tier={:?} batchable={} delay={} options={:?}",
                    card.tier, card.batchable, card.read_delay_secs, card.options
                ));
            }
            Ok(())
        }
        Decision::Deny { .. } => Ok(()),
        Decision::Allow { why } => Err(format!("ALLOW {why:?}")),
    }
}

fn check_everywhere(fx: &Fx, a: &Action, label: &str) -> usize {
    let mut n = 0;
    for (sl, st, surface) in every_mode(fx, a) {
        let d = decide(a, &st, surface, NOW);
        if let Err(e) = is_strict(&d, surface) {
            panic!("{label:?} [{sl}]: {e}\n{d:?}");
        }
        n += 1;
    }
    n
}

fn inputs(fx: &Fx) -> Vec<Value> {
    let f = fx.ws.join("README.md");
    let f = f.to_str().unwrap();
    vec![
        json!({}),
        json!({"prompt": "x"}),
        json!({"file_path": f}),
        json!({"file_path": f, "content": "x"}),
        json!({"path": fx.ws.to_str().unwrap(), "pattern": "*"}),
        json!({"url": "https://example.com/"}),
        json!({"isolation": "worktree", "prompt": "x"}),
        json!({"todos": []}),
        json!({"action": "keep"}),
        json!({"cmd": "ls"}),
        json!({"command": ["ls"]}),
        json!({"params": {"command": "ls"}}),
        json!(""),
        json!(null),
        json!([]),
        json!(0),
    ]
}

/// Names the gate was never taught: random, case, look-alikes, whitespace, prefix/suffix of known names, mcp shapes.
fn untaught_names() -> Vec<String> {
    let mut v: Vec<String> = Vec::new();
    let mut st: u64 = 0x5eed_1234_abcd_0001;
    let mut below = |n: usize| { st ^= st << 13; st ^= st >> 7; st ^= st << 17; (st % n as u64) as usize };
    const AL: &[u8] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-.:";
    for _ in 0..40 {
        let len = 1 + below(20);
        v.push((0..len).map(|_| AL[below(AL.len())] as char).collect());
    }
    for k in KNOWN_TOOLS {
        let n = k.name;
        v.push(n.to_lowercase());
        v.push(n.to_uppercase());
        v.push(format!("{n}\t"));
        v.push(format!("\u{a0}{n}"));
        v.push(format!("{n}\n"));
        v.push(format!("{n}\0"));
        v.push(format!("{n}\u{feff}"));
        v.push(format!("\u{200d}{n}"));
        v.push(n[..n.len() - 1].to_string()); // prefix
        v.push(format!("{n}s")); // suffix
        v.push(format!("x{n}"));
        v.push(format!("{n}{n}"));
        v.push(format!("{n}/"));
        v.push(format!("{n}(*)"));
        v.push(format!("mcp__{n}"));
        v.push(format!("mcp__{n}__{n}"));
        // fullwidth form of the whole name
        v.push(
            n.chars()
                .map(|c| if c.is_ascii_graphic() { char::from_u32(c as u32 + 0xFEE0).unwrap() } else { c })
                .collect(),
        );
    }
    for s in [
        "",
        " ",
        "Rеad",           // Cyrillic е
        "Аgent",          // Cyrillic А
        "Tаsk",           // Cyrillic а
        "TodoWrіte",      // Cyrillic і
        "Gl\u{43e}b",     // Cyrillic о
        "Re\u{301}ad",    // combining acute
        "ＴａｓｋＣｒｅａｔｅ",
        "Ｒｅａｄ",
        "ToolSearch\u{200b}",
        "Agent\u{2060}",
        "CronLis",
        "CronListAll",
        "Todo",
        "Write2",
        "MultiEdit ",
        "mcp",
        "mcp_",
        "mcp_github_list",
        "MCP__github__list",
        "Mcp__github__list",
        "mcp__",
        "mcp___",
        "mcp____",
        "mcp__a",
        "mcp__a__",
        "mcp____b",
        "mcp__a__b__c",
        "mcp__a__b__c__d",
        "mcp__ __ ",
        "mcp__plugin_coagent_link__",
        "mcp__plugin_coagent_link__share ",
        "mcp__plugin_coagent_link__SHARE",
        "mcp__plugin_coagent_link__shar",
        "mcp__plugin_coagent_link__sendx",
        "mcp__plugin_coagent_link__share__x",
        "mcp__plugin_coagent_link_share",
        "mcp__plugin_coagent_link__wait",
        "mcp__plugin_coagent_link__exec",
        "mcp__ide__executeCode",
        "mcp__github__create_pull_request",
        "TeamCreate",
        "TeamDelete",
        "SendMessage",
        "ExitWorktree ",
        "exitworktree",
        "BashOutput",
        "KillShell",
        "KillBash",
        "TaskOutput",
        "Computer",
        "str_replace_based_edit_tool",
        "text_editor",
        "bash",
    ] {
        v.push(s.to_string());
    }
    v.retain(|n| !taught(n));
    v.sort();
    v.dedup();
    v
}

// (1) every untaught name: strict in every state, every input, never wider than one exact call.
#[test]
fn qa_untaught_names_are_strict_everywhere() {
    let fx = fixture("qa-untaught");
    let names = untaught_names();
    let ins = inputs(&fx);
    let mut n = 0;
    for name in &names {
        for input in &ins {
            let mut a = act(&fx, name, input.clone());
            a.share_flagged = Some(false);
            assert!(a.strict.is_some(), "{name:?} {input}: strict is None");
            n += check_everywhere(&fx, &a, name);
        }
    }
    eprintln!("QA untaught: {} names, {n} decisions, 0 below strict", names.len());
}

// (1b) an AllowOnce on a strict card stores nothing; AllowForSession of ANY scope is refused.
#[test]
fn qa_strict_card_answers_store_nothing() {
    let fx = fixture("qa-answers");
    for (tool, input) in [
        ("MadeUpTool", json!({"prompt": "x"})),
        ("mcp__github__list", json!({})),
        ("ExitWorktree", json!({"action": "keep"})),
        ("Agent", json!({"prompt": "x", "isolation": "remote"})),
        ("Task", json!({"prompt": "x", "name": "n"})),
        ("CronCreate", json!({"cron": "* * * * *", "prompt": "x"})),
    ] {
        let a = act(&fx, tool, input.clone());
        let st = fx.state();
        let d = decide(&a, &st, Surface::Console, NOW);
        let Decision::Ask { card } = d else { panic!("{tool}: {d:?}") };
        let once = resolve(&card, &a, OwnerAnswer::AllowOnce, Timestamp(NOW.0 + 6));
        assert!(once.approval.is_none() && once.remember.is_empty(), "{tool}: {once:?}");
        for scope in [
            Scope::ExactInput { hash: a.raw_input_hash.clone() },
            Scope::ReadsUnder { dir: fx.ws.clone() },
            Scope::EditsToFile { path: fx.ws.join("README.md") },
        ] {
            let r = resolve(&card, &a, OwnerAnswer::AllowForSession(scope.clone()), Timestamp(NOW.0 + 6));
            assert!(
                matches!(r.decision, Decision::Deny { .. }) && r.approval.is_none(),
                "{tool} {scope:?}: {r:?}"
            );
        }
    }
}

// (2) the host's own 25 (2.1.325) and the docs' 46: every one NOT on the list is strict.
const HOST: [&str; 25] = [
    "Task", "Bash", "CronCreate", "CronDelete", "CronList", "DesignSync", "Edit", "EnterWorktree", "ExitWorktree",
    "ListAgents", "Monitor", "NotebookEdit", "PushNotification", "Read", "RemoteTrigger", "ReportFindings",
    "ScheduleWakeup", "SendMessage", "Skill", "TaskStop", "ToolSearch", "WebFetch", "WebSearch", "Workflow", "Write",
];
const DOCS: [&str; 46] = [
    "Agent", "Artifact", "AskUserQuestion", "Bash", "CronCreate", "CronDelete", "CronList", "Edit", "EndConversation",
    "EnterPlanMode", "EnterWorktree", "ExitPlanMode", "ExitWorktree", "Glob", "Grep", "ListAgents",
    "ListMcpResourcesTool", "LSP", "Monitor", "NotebookEdit", "PowerShell", "PushNotification", "Read",
    "ReadMcpResourceTool", "RemoteTrigger", "ReportFindings", "ScheduleWakeup", "SendFeedback", "SendMessage",
    "SendUserFile", "ShareOnboardingGuide", "Skill", "SubagentHandback", "TaskCreate", "TaskGet", "TaskList",
    "TaskOutput", "TaskStop", "TaskUpdate", "TodoWrite", "ToolSearch", "WaitForMcpServers", "WebFetch", "WebSearch",
    "Workflow", "Write",
];

#[test]
fn qa_host_tools_off_the_list_are_strict() {
    let fx = fixture("qa-host");
    let mut off = std::collections::BTreeSet::new();
    for t in HOST.iter().chain(DOCS.iter()) {
        if !taught(t) {
            off.insert(*t);
        }
    }
    let ins = inputs(&fx);
    let mut n = 0;
    for t in &off {
        for input in &ins {
            let a = act(&fx, t, input.clone());
            n += check_everywhere(&fx, &a, t);
        }
    }
    let taught: Vec<&str> =
        HOST.iter().chain(DOCS.iter()).copied().filter(|t| taught(t)).collect();
    eprintln!("QA host/docs off-list: {} tools strict ({n} decisions); taught: {taught:?}", off.len());
    // the list holds no tool outside design/host/docs except the three design-only names
    for k in KNOWN_TOOLS {
        let in_src = HOST.contains(&k.name) || DOCS.contains(&k.name);
        let design_only = ["NotebookRead", "LS", "MultiEdit", "mcp__plugin_coagent_link__share", "mcp__plugin_coagent_link__send"];
        assert!(in_src || design_only.contains(&k.name), "{} is on the list but in no source", k.name);
    }
}

// (2b) every taught `other` tool: exactly T2, batchable, the one ExactInput option, and a session approval needs the
// exact input (a changed input asks again).
#[test]
fn qa_taught_other_tools_are_exactly_t2_and_hash_bound() {
    let fx = fixture("qa-taught");
    for k in KNOWN_TOOLS.iter().filter(|k| k.kind == Kind::Other) {
        let input = json!({"prompt": "x", "todos": [], "query": "q"});
        let a = act(&fx, k.name, input.clone());
        assert_eq!(a.kind, Kind::Other, "{}", k.name);
        assert_eq!(a.strict, None, "{}", k.name);
        let d = decide(&a, &fx.state(), Surface::Console, NOW);
        let Decision::Ask { card } = &d else { panic!("{}: {d:?}", k.name) };
        assert_eq!(card.tier, Tier::T2, "{}", k.name);
        assert!(card.batchable);
        let scope = Scope::ExactInput { hash: a.raw_input_hash.clone() };
        assert_eq!(
            card.options,
            vec![CardOption::AllowOnce, CardOption::AllowForSession(scope.clone()), CardOption::Deny, CardOption::DenyWithReason],
            "{}",
            k.name
        );
        let mut st = fx.state();
        st.approvals.insert(SessionApproval { scope, expires_at: None });
        assert!(is_allow(&decide(&a, &st, Surface::Console, NOW)), "{}", k.name);
        let b = act(&fx, k.name, json!({"prompt": "y", "todos": [], "query": "q"}));
        assert!(!is_allow(&decide(&b, &st, Surface::Console, NOW)), "{}: other input allowed", k.name);
        // a grant (wide) never allows a taught `other` call
        let mut st2 = fx.state();
        fx.grant(&mut st2, &wide_grant()).unwrap();
        assert!(!is_allow(&decide(&a, &st2, Surface::Console, NOW)), "{}: grant allowed", k.name);
    }
}

// (3) a command field on any taught catch-all tool, ExitWorktree and the subagent tool is a terminal command.
#[test]
fn qa_command_field_beats_the_list() {
    let fx = fixture("qa-cmd");
    let mut names: Vec<&str> = KNOWN_TOOLS.iter().filter(|k| k.kind == Kind::Other).map(|k| k.name).collect();
    names.extend(["ExitWorktree", "MadeUpTool", "mcp__srv__x"]);
    for t in names {
        for extra in [json!({}), json!({"isolation": "worktree"}), json!({"isolation": "remote"}), json!({"name": "a"})] {
            let mut input = json!({"command": "echo x >> ~/.zshrc"});
            for (k, v) in extra.as_object().unwrap() {
                input[k] = v.clone();
            }
            let a = act(&fx, t, input.clone());
            assert_eq!(a.kind, Kind::Execute, "{t} {input}");
            let d = decide(&a, &fx.state(), Surface::Console, NOW);
            assert!(matches!(d, Decision::Deny { reason: DenyReason::HardDeny { .. } }), "{t} {input}: {d:?}");
            let a2 = act(&fx, t, json!({"command": "npm test"}));
            check_everywhere(&fx, &a2, t);
        }
    }
}

// (3b) PROBE: named arms that are taught do NOT read a command field (Read, Write, WebFetch, ExitPlanMode, share).
#[test]
fn qa_probe_named_arms_ignore_a_command_field() {
    let fx = fixture("qa-probe-cmd");
    let f = fx.ws.join("README.md");
    for (t, mut input) in [
        ("Read", json!({"file_path": f.to_str().unwrap()})),
        ("Write", json!({"file_path": f.to_str().unwrap(), "content": "x"})),
        ("Glob", json!({"pattern": "*"})),
        ("WebFetch", json!({"url": "https://example.com/"})),
        ("ExitPlanMode", json!({"plan": "p"})),
        ("mcp__plugin_coagent_link__share", json!({"content": "c"})),
    ] {
        input["command"] = json!("rm -rf ~");
        let a = act(&fx, t, input);
        let d = decide(&a, &fx.state(), Surface::Console, NOW);
        let shape = match &d {
            Decision::Ask { card } => format!("Ask {:?} batchable={}", card.tier, card.batchable),
            other => format!("{other:?}"),
        };
        eprintln!("PROBE command-field {t}: kind={:?} -> {shape}", a.kind);
    }
}

// (4) the red cases, every shape, both names.
#[test]
fn qa_red_cases_every_shape() {
    let fx = fixture("qa-red");
    let local = |d: &Decision| matches!(d, Decision::Ask { card } if card.tier == Tier::T2 && card.batchable);
    for tool in ["Agent", "Task"] {
        // local
        for raw in [
            r#"{"prompt":"p","description":"d"}"#,
            r#"{"prompt":"p","isolation":"worktree"}"#,
            r#"{"isolation":"worktree","prompt":"p","subagent_type":"Explore","model":"opus"}"#,
            r#"{"prompt":"p","run_in_background":true}"#,
            r#"{"prompt":"p","options":{"isolation":"remote"}}"#,   // nested: not the top-level field
            r#"{"prompt":"p","team_name":"t"}"#,                     // no name
            r#"{"prompt":"p","isolation":"remote","isolation":"worktree"}"#, // duplicate key: last wins (as the host's JSON)
        ] {
            let a = classify(&hook_raw(&fx, tool, raw), HostOs::Posix, &fx.env(), &PosixNormaliser);
            let d = decide(&a, &fx.state(), Surface::Console, NOW);
            eprintln!("LOCAL? {tool} {raw} -> strict={:?} local={}", a.strict, local(&d));
        }
        // strict
        for raw in [
            r#"{"prompt":"p","isolation":"remote"}"#,
            r#"{"isolation":"remote"}"#,
            r#"{"prompt":"p","isolation":"Remote"}"#,
            r#"{"prompt":"p","isolation":"REMOTE"}"#,
            r#"{"prompt":"p","isolation":"remote "}"#,
            r#"{"prompt":"p","isolation":" worktree"}"#,
            r#"{"prompt":"p","isolation":"WORKTREE"}"#,
            r#"{"prompt":"p","isolation":"worktree\u0000"}"#,
            r#"{"prompt":"p","isolation":"work​tree"}"#,
            r#"{"prompt":"p","isolation":"wоrktree"}"#,
            r#"{"prompt":"p","isolation":""}"#,
            r#"{"prompt":"p","isolation":"cloud"}"#,
            r#"{"prompt":"p","isolation":"local"}"#,
            r#"{"prompt":"p","isolation":"none"}"#,
            r#"{"prompt":"p","isolation":null}"#,
            r#"{"prompt":"p","isolation":0}"#,
            r#"{"prompt":"p","isolation":false}"#,
            r#"{"prompt":"p","isolation":["worktree"]}"#,
            r#"{"prompt":"p","isolation":{"mode":"worktree"}}"#,
            r#"{"prompt":"p","isolation":"worktree","isolation":"remote"}"#,
            r#"{"prompt":"p","name":"a"}"#,
            r#"{"name":"a","prompt":"p"}"#,
            r#"{"prompt":"p","name":null}"#,
            r#"{"prompt":"p","name":""}"#,
            r#"{"prompt":"p","name":7}"#,
            r#"{"prompt":"p","name":["a"]}"#,
            r#"{"prompt":"p","name":{"a":1}}"#,
            r#"{"prompt":"p","name":false}"#,
            r#"{"name":"a","isolation":"worktree","prompt":"p"}"#,
            r#"{"isolation":"worktree","name":"a","prompt":"p"}"#,
            r#"{"isolation":"remote","name":"a","prompt":"p"}"#,
            r#"{"prompt":"p","name":"a","name":"b"}"#,
            r#""p""#,
            r#"null"#,
            r#"[{"isolation":"worktree"}]"#,
            r#"7"#,
        ] {
            let a = classify(&hook_raw(&fx, tool, raw), HostOs::Posix, &fx.env(), &PosixNormaliser);
            check_everywhere(&fx, &a, &format!("{tool} {raw}"));
        }
    }
    for raw in [
        r#"{"action":"remove"}"#,
        r#"{"action":"remove","discard_changes":true}"#,
        r#"{"action":"remove","discard_changes":"true"}"#,
        r#"{"action":"keep"}"#,
        r#"{"action":"Keep"}"#,
        r#"{}"#,
        r#"{"action":null}"#,
        r#"{"action":["keep"]}"#,
        r#"{"action":"keep","action":"remove"}"#,
        r#""keep""#,
        r#"null"#,
    ] {
        for tool in ["ExitWorktree"] {
            let a = classify(&hook_raw(&fx, tool, raw), HostOs::Posix, &fx.env(), &PosixNormaliser);
            check_everywhere(&fx, &a, &format!("{tool} {raw}"));
            let d = decide(&a, &fx.state(), Surface::Console, NOW);
            let Decision::Ask { card } = d else { panic!() };
            assert_eq!(card.reasons.first(), Some(&Reason::WorktreeRemoval), "{raw}");
        }
    }
}

// (4b) assert the LOCAL shapes really are local (documented behaviour), as a positive control for the above.
#[test]
fn qa_local_shapes_are_local_and_exactly_main() {
    let fx = fixture("qa-local");
    for tool in ["Agent", "Task"] {
        for input in [json!({"prompt": "p"}), json!({"prompt": "p", "isolation": "worktree"})] {
            let a = act(&fx, tool, input.clone());
            assert_eq!(subagent_place(&input), SubagentPlace::Local);
            assert_eq!(a.strict, None);
            let d = decide(&a, &fx.state(), Surface::Console, NOW);
            let Decision::Ask { card } = d else { panic!() };
            assert_eq!((card.tier, card.batchable, card.read_delay_secs), (Tier::T2, true, 0), "{tool} {input}");
            assert!(card.reasons.is_empty(), "{:?}", card.reasons);
        }
    }
}

// (6) a grant's service line allows nothing; positive control: before the round it could.
#[test]
fn qa_service_grant_line_allows_nothing() {
    let fx = fixture("qa-svc");
    for tool in ["mcp__github__list", "mcp__github__get_issue", "mcp__github__x"] {
        let a = act(&fx, tool, json!({"n": 1}));
        let mut st = fx.state();
        fx.grant(&mut st, &wide_grant()).unwrap();
        for surface in [Surface::Console, Surface::TerminalPrompt, Surface::None] {
            let d = decide(&a, &st, surface, NOW);
            is_strict(&d, surface).unwrap_or_else(|e| panic!("{tool}: {e}"));
        }
    }
}

// (7) the owner's exact-command list never allows a command through another tool or with the sandbox off.
#[test]
fn qa_owner_list_binds_tool_and_sandbox() {
    let fx = fixture("qa-owner");
    let mut st = fx.state();
    st.sandbox = Sandbox::On;
    st.add_owner_command("npm test", &fx.ws, ShellKind::Bash, &PosixNormaliser).unwrap();
    // positive control
    assert!(matches!(
        decide(&fx.bash("npm test"), &st, Surface::Console, NOW),
        Decision::Allow { why: AllowWhy::OwnerCommandList }
    ));
    let mut tools: Vec<&str> = KNOWN_TOOLS.iter().map(|k| k.name).collect();
    tools.extend(["Monitor", "PowerShell", "bash", "MadeUpTool", "mcp__srv__run", "ExitWorktree", "Agent", "Task"]);
    for t in tools {
        for input in [
            json!({"command": "npm test"}),
            json!({"command": "npm test", "isolation": "worktree"}),
            json!({"command": "npm test", "description": "test"}),
        ] {
            let a = act(&fx, t, input.clone());
            let d = decide(&a, &st, Surface::Console, NOW);
            assert!(!is_allow(&d), "{t} {input}: {d:?}");
        }
    }
    for input in [
        json!({"command": "npm test", "dangerouslyDisableSandbox": true}),
        json!({"command": "npm test", "dangerouslyDisableSandbox": true, "description": "test"}),
    ] {
        let a = act(&fx, "Bash", input.clone());
        let d = decide(&a, &st, Surface::Console, NOW);
        assert!(!is_allow(&d), "Bash {input}: {d:?}");
    }
}

// (5) the name ruling holds whatever key order and type; and with a command, the command decision wins
#[test]
fn qa_name_is_strict_whatever_isolation() {
    let fx = fixture("qa-name");
    for tool in ["Agent", "Task"] {
        for iso in [None, Some(json!("worktree")), Some(json!("remote")), Some(json!(null))] {
            for name in [json!("a"), json!(""), json!(null), json!(0), json!(["a"]), json!({})] {
                let mut input = json!({"prompt": "p", "name": name});
                if let Some(i) = &iso {
                    input["isolation"] = i.clone();
                }
                assert_eq!(subagent_place(&input), SubagentPlace::PossibleTeammate, "{input}");
                let a = act(&fx, tool, input.clone());
                assert_eq!(a.strict, Some(Strict::PossibleTeammate), "{input}");
                check_everywhere(&fx, &a, &format!("{tool} {input}"));
                let d = decide(&a, &fx.state(), Surface::Console, NOW);
                let Decision::Ask { card } = d else { panic!() };
                assert_eq!(card.reasons.first(), Some(&Reason::PossibleTeammate));
            }
        }
    }
    // PROBE: a field spelled differently from `name` (host field names are case-sensitive)
    for k in ["Name", "NAME", "name ", "teammate", "team_name"] {
        let input = json!({"prompt": "p", k: "a"});
        eprintln!("PROBE name-like key {k:?}: {:?}", subagent_place(&input));
    }
}
