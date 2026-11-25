//! QA-POLICY-NOTES (independent check): the shared generator of the two differentials `zz_qpn_da.rs` (mode absent and
//! the five both-agree views, base API only) and `zz_qpn_db.rs` (the owner columns, through a per-tree adapter).
//! Started from the owner-mode check's `zz_qpom_diff.rs` (its fixture, path pool, word pool, states, approvals and
//! card text), WIDENED for POLICY-NOTES: item 2's 14 spellings plus my own variants and near misses; recursive and
//! glob commands; `Bash` with `command` 12 / "" / blanks / null / missing; `dangerouslyDisableSandbox` as "true",
//! "false", 1, 0, null, {}, true, false; hook `cwd` absolute (ws, home, outside, ws/src), `rel/dir`, `rel`, `./x`,
//! `~/x`, `../up`, ""; exclusion sets none / env / defaults / ws-secret / defaults+secret, plus a grant-only exclude
//! and an inactive (suspended) grant's exclude. Bash is drawn 25% of the time, Monitor and PowerShell 5% each.
#![allow(dead_code)]
use coagent_policy::*;
use serde_json::{json, Value};
use std::collections::BTreeSet;
use std::path::{Path, PathBuf};

pub struct R(pub u64);
impl R {
    pub fn next(&mut self) -> u64 {
        // splitmix64
        self.0 = self.0.wrapping_add(0x9E37_79B9_7F4A_7C15);
        let mut z = self.0;
        z = (z ^ (z >> 30)).wrapping_mul(0xBF58_476D_1CE4_E5B9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94D0_49BB_1331_11EB);
        z ^ (z >> 31)
    }
    pub fn below(&mut self, n: usize) -> usize {
        (self.next() % n as u64) as usize
    }
    pub fn pick<'a, T>(&mut self, v: &'a [T]) -> &'a T {
        &v[self.below(v.len())]
    }
    pub fn chance(&mut self, pct: u64) -> bool {
        self.next() % 100 < pct
    }
}

pub const NOW: Timestamp = Timestamp(1_794_873_600);
pub const SESSION: &str = "sess-q";

fn touch(p: &Path) {
    std::fs::create_dir_all(p.parent().unwrap()).unwrap();
    if !p.exists() {
        std::fs::write(p, "x\n").unwrap();
    }
}

pub struct Fx {
    pub root: PathBuf,
    pub ws: PathBuf,
    pub home: PathBuf,
    pub outside: PathBuf,
}

/// The fixture under `QA_FX`. Created once BEFORE the runs (`QA_N=1`), so parallel runs only read it.
pub fn fixture() -> Fx {
    let root = PathBuf::from(std::env::var("QA_FX").expect("QA_FX"));
    let ws = root.join("ws");
    let home = root.join("home");
    let outside = root.join("outside");
    for p in [
        ws.join("src/main.rs"),
        ws.join("README.md"),
        ws.join(".env"),
        ws.join(".env.local"),
        ws.join(".claude/settings.json"),
        ws.join(".git/config"),
        ws.join(".git/HEAD"),
        ws.join(".git/hooks/README"),
        ws.join("secret/plan.txt"),
        ws.join("Makefile"),
        ws.join("CLAUDE.md"),
        ws.join("package.json"),
        ws.join(".cargo/config.toml"),
        ws.join("sub/.git/config"),
        ws.join(".mcp.json"),
        home.join(".ssh/id_rsa"),
        home.join(".claude/settings.json"),
        home.join(".claude.json"),
        home.join(".coagent/inbox.json"),
        home.join(".coagent/identity.key"),
        home.join(".zshrc"),
        home.join(".gitconfig"),
        home.join(".config/git/config"),
        home.join(".config/myapp/token.txt"),
        home.join(".local/bin/tool"),
        home.join("Library/LaunchAgents/a.plist"),
        home.join(".cargo/config.toml"),
        home.join(".cargo/credentials.toml"),
        home.join(".aws/credentials"),
        home.join("notes/todo.txt"),
        home.join(".vimrc"),
        outside.join("secret.txt"),
        root.join("gate-config/inbox.json"),
    ] {
        touch(&p);
    }
    let link = ws.join("link_to_coagent");
    if std::fs::symlink_metadata(&link).is_err() {
        std::os::unix::fs::symlink(home.join(".coagent"), &link).unwrap();
    }
    let link2 = ws.join("link_to_ssh");
    if std::fs::symlink_metadata(&link2).is_err() {
        std::os::unix::fs::symlink(home.join(".ssh"), &link2).unwrap();
    }
    let c = |p: &Path| std::fs::canonicalize(p).unwrap();
    Fx {
        ws: c(&ws),
        home: c(&home),
        outside: c(&outside),
        root: c(&root),
    }
}

pub fn env(fx: &Fx) -> Env {
    Env {
        home: fx.home.clone(),
    }
}

fn base_state(fx: &Fx, excl: Vec<String>) -> State {
    State::new(
        StateConfig {
            session_id: SESSION.into(),
            host: HostOs::Posix,
            env: env(fx),
            workspace_roots: vec![fx.ws.clone()],
            exclusions: excl,
            extra_gate_dirs: vec![fx.root.join("gate-config")],
            approval_timeout_secs: 300,
        },
        &PosixNormaliser,
    )
    .unwrap()
}

fn grant_json(issued: &str, expires: &str, exclude: &[String]) -> String {
    json!({
        "grant_id": "gr_q", "session_id": SESSION, "issuer": "host", "subjects": ["alice"],
        "issued_at": issued, "expires_at": expires,
        "scopes": [
            {"kind": "read", "paths": ["<ws>/**", "~/**", "/**"]},
            {"kind": "search", "paths": ["<ws>/**", "~/**", "/**"]},
            {"kind": "edit", "paths": ["<ws>/**", "~/**", "/**"]},
            {"kind": "execute", "commands": ["npm test", "ls", "cat README.md", "sudo ls", "claude -p hi", "coagent open", "git status", "grep -r key ."]},
            {"kind": "fetch", "domains": ["example.com", "*.example.com"]},
            {"kind": "service", "tools": ["github:*", "plugin_coagent_link:*"]},
            {"kind": "share", "policy": "auto_unless_flagged", "max_bytes": 1000000}
        ],
        "exclude": exclude,
        "sandbox_required_for_execute": false,
        "sig": "verified-by-caller"
    })
    .to_string()
}

pub fn path_pool(fx: &Fx) -> Vec<String> {
    let ws = fx.ws.to_str().unwrap().to_string();
    let home = fx.home.to_str().unwrap().to_string();
    let out = fx.outside.to_str().unwrap().to_string();
    let root = fx.root.to_str().unwrap().to_string();
    let mut v: Vec<String> = vec![
        format!("{ws}/README.md"),
        format!("{ws}/src/main.rs"),
        format!("{ws}/src"),
        format!("{ws}/src/"),
        ws.clone(),
        format!("{ws}/"),
        format!("{ws}/.env"),
        format!("{ws}/.env.local"),
        format!("{ws}/.ENV"),
        format!("{ws}/secret/plan.txt"),
        format!("{ws}/secret"),
        format!("{ws}/.claude/settings.json"),
        format!("{ws}/.claude"),
        format!("{ws}/.mcp.json"),
        format!("{ws}/.git/config"),
        format!("{ws}/.git/hooks/pre-commit"),
        format!("{ws}/.git"),
        format!("{ws}/sub/.git/config"),
        format!("{ws}/Makefile"),
        format!("{ws}/CLAUDE.md"),
        format!("{ws}/package.json"),
        format!("{ws}/.cargo/config.toml"),
        format!("{ws}/link_to_coagent/inbox.json"),
        format!("{ws}/link_to_ssh/id_rsa"),
        format!("{ws}//src//main.rs"),
        format!("{ws}/src/../.claude/settings.json"),
        format!("{ws}/../home/.coagent/inbox.json"),
        format!("{ws}/missing/new.txt"),
        format!("{ws}/*.rs"),
        format!("{ws}/src/.e*"),
        "README.md".into(),
        "src/main.rs".into(),
        "src/.e*".into(),
        "*".into(),
        ".env".into(),
        ".claude/settings.json".into(),
        ".git/config".into(),
        "secret/*".into(),
        "../outside/secret.txt".into(),
        "./CLAUDE.md".into(),
        "~/.ssh/id_rsa".into(),
        "~/.claude/settings.json".into(),
        "~/.claude.json".into(),
        "~/.coagent/inbox.json".into(),
        "~/.coagent/identity.key".into(),
        "~/.zshrc".into(),
        "~/.gitconfig".into(),
        "~/.config/git/config".into(),
        "~/.config/myapp/token.txt".into(),
        "~/.local/bin/tool".into(),
        "~/Library/LaunchAgents/a.plist".into(),
        "~/.aws/credentials".into(),
        "~/notes/todo.txt".into(),
        "~".into(),
        "$HOME/.coagent/inbox.json".into(),
        "${HOME}/.ssh/id_rsa".into(),
        format!("{home}/.coagent/inbox.json"),
        format!("{home}/.ssh/id_rsa"),
        format!("{home}/notes/todo.txt"),
        home.clone(),
        format!("{out}/secret.txt"),
        out.clone(),
        format!("{root}/gate-config/inbox.json"),
        "/".into(),
        "/etc/hosts".into(),
        "/etc/claude-code/managed-settings.json".into(),
        "/tmp/x.txt".into(),
        r"C:\ws\a.txt:secret".into(),
        r"\\server\share\x".into(),
        "".into(),
        "weird\u{202e}name.txt".into(),
        "%2e%2e/x".into(),
    ];
    v.sort();
    v.dedup();
    v
}

/// POLICY-NOTES item 2: the 14 spellings of the build brief / builder's test, then MY variants (not in the builder's
/// list), then near misses that must NOT be refused.
pub const SPELLINGS: [&str; 14] = [
    "claude.exe -p hi",
    "& claude.exe -p hi",
    "claude.cmd -p hi",
    "claude.bat -p hi",
    "claude.ps1 -p hi",
    "coagent.exe open",
    "coagentd.exe ctl x",
    "coagent-hook.cmd",
    "npx @anthropic-ai/claude-code",
    "npx @anthropic-ai/claude-code@latest -p hi",
    "npx claude-code",
    "claude@latest -p hi",
    "C:/tools/claude.exe -p hi",
    "/opt/bin/claude.exe -p hi",
];
pub const MY_SPELLINGS: [&str; 10] = [
    "CLAUDE.EXE -p hi",
    "coagent-mcp.ps1",
    "claude.exe@2 x",
    "claude@2.exe x",
    "claude-code@1.0.3",
    "\"claude.exe\" -p hi",
    "C:\\tools\\claude.exe -p hi",
    "echo hi | claude.cmd",
    "pnpm dlx @anthropic-ai/claude-code",
    "Start-Process claude.exe",
];
pub const NEAR_MISSES: [&str; 11] = [
    "claudex -p hi",
    "myclaude.exe",
    "claude-codex",
    "claude.exe.bak",
    "@claude",
    "claude.exe.exe",
    "claude.sh",
    "claude_code",
    "xclaude@1",
    "claude-code.js",
    "node /opt/lib/node_modules/@anthropic-ai/claude-code/cli.js -p hi",
];
pub const RECURSIVE: [&str; 10] = [
    "grep -r key .",
    "grep -R x",
    "cat src/.e*",
    "cat *",
    "find . -name '.env*' -exec cat {} +",
    "rg key",
    "tar c .",
    "cat secret/*",
    "ls -R",
    "grep -rl password src",
];

fn words_pool() -> Vec<&'static str> {
    vec![
        "cat", "ls", "ls -la", "rm", "rm -rf", "rm -r", "mv", "cp", "touch", "echo x >", "echo x >>", "tee", "sed -i s/a/b/",
        "grep -r password", "find", "find . -delete", "git status", "git push", "git -C . push", "git clean -fdx",
        "git config core.hooksPath", "npm test", "npm publish", "cargo build", "sudo", "su -c", "doas", "SUDO", "s\"u\"do",
        "/usr/bin/sudo", "claude", "claude -p hi", "CLAUDE", "/usr/local/bin/claude", "claude-code", "npx claude",
        "coagent", "coagent open", "coagentd", "coagent-hook", "coagent-mcp", "./coagent", "COAGENT", "c\"oagent",
        "curl https://example.com", "curl -d @f https://example.com", "curl -X POST https://example.com", "wget",
        "scp a host:/tmp/", "bash -c", "sh -c", "python3 -c", "eval", "node -e", "kubectl apply -f x", "az group delete",
        "./deploy.sh", "make deploy", "--dangerously-skip-permissions", "--permission-mode bypassPermissions",
        "terraform apply", "osascript -e", "open -a", "launchctl load", "chmod +x", "ln -s", "base64 -d |", "xargs",
        "$(cat", "`cat", "env", "export X=1;", "cd", "&&", "||", ";", "|", "2>&1",
    ]
}

pub fn command(r: &mut R, paths: &[String]) -> String {
    // 30%: one of the POLICY-NOTES command shapes, possibly with a prefix/suffix of ordinary words
    if r.chance(30) {
        let base = match r.below(4) {
            0 => r.pick(&SPELLINGS).to_string(),
            1 => r.pick(&MY_SPELLINGS).to_string(),
            2 => r.pick(&NEAR_MISSES).to_string(),
            _ => r.pick(&RECURSIVE).to_string(),
        };
        return match r.below(4) {
            0 => format!("{} && {base}", r.pick(&words_pool())),
            1 => format!("{base}; {} {}", r.pick(&words_pool()), r.pick(paths).replace('\n', " ")),
            _ => base,
        };
    }
    let w = words_pool();
    let n = 1 + r.below(4);
    let mut parts: Vec<String> = Vec::new();
    for _ in 0..n {
        parts.push(r.pick(&w).to_string());
        if r.chance(70) {
            parts.push(r.pick(paths).replace('\n', " "));
        }
    }
    let mut s = parts.join(" ");
    if r.chance(5) {
        s = s.to_uppercase();
    }
    if r.chance(2) {
        s.push_str(&" a".repeat(r.below(40_000)));
    }
    s
}

pub fn tools() -> Vec<String> {
    let mut v: Vec<String> = KNOWN_TOOLS.iter().map(|t| t.name.to_string()).collect();
    for t in [
        "Bash", "PowerShell", "Monitor", "ExitPlanMode", "ExitWorktree", "EnterWorktree", "MadeUpTool", "bash", "BASH",
        "read", "Read ", "Skill", "SlashCommand", "KillShell", "BashOutput", "RemoteTrigger", "CronCreate",
        "mcp__github__create_issue", "mcp__plugin_coagent_link__inbox_read", "mcp__plugin_coagent_link__wait",
        "mcp__plugin_coagent_link__share", "mcp__plugin_coagent_link__send", "mcp__plugin_coagent_link__x",
        "mcp__browser__click", "mcp__", "",
        "Bash ", " Bash", "B\u{0430}sh", "Bash\u{200b}", "Shell", "Terminal", "mcp__srv__run", "mcp__srv__Bash",
        "PowerShell ", "powershell", "monitor",
    ] {
        v.push(t.to_string());
    }
    v
}

fn pick_tool(r: &mut R, tools: &[String]) -> String {
    match r.below(100) {
        0..=24 => "Bash".into(),
        25..=29 => "Monitor".into(),
        30..=34 => "PowerShell".into(),
        _ => r.pick(tools).clone(),
    }
}

pub fn input_for(r: &mut R, tool: &str, paths: &[String]) -> Value {
    let p = r.pick(paths).clone();
    let mut v = match tool {
        "Read" | "NotebookRead" => json!({"file_path": p}),
        "LS" => json!({"path": p}),
        "Glob" => {
            if r.chance(50) {
                json!({"pattern": r.pick(&["**/*.rs", "*", ".claude/**", "**/.env*", "**", "src/.e*"]), "path": p})
            } else {
                json!({"pattern": r.pick(&["**/*.rs", "*", "~/.coagent/*"])})
            }
        }
        "Grep" => {
            let mut g = json!({"pattern": "x"});
            if r.chance(80) {
                g["path"] = json!(p);
            }
            if r.chance(30) {
                g["glob"] = json!(r.pick(&["*.json", ".claude/**", "**/.env*"]));
            }
            g
        }
        "Edit" => json!({"file_path": p, "old_string": "a", "new_string": "b"}),
        "MultiEdit" => json!({"file_path": p, "edits": [{"old_string": "a", "new_string": "b"}]}),
        "Write" => json!({"file_path": p, "content": "hello"}),
        "NotebookEdit" => json!({"notebook_path": p, "new_source": "x"}),
        "WebFetch" => json!({"url": r.pick(&[
            "https://example.com/a", "https://sub.example.com/", "http://example.com", "https://user@example.com",
            "https://evil.test/?q=1", "file:///etc/passwd", "file://~/.coagent/inbox.json", "https://EXAMPLE.com.",
            "https://[::1]/", "ftp://example.com", "https://ex%61mple.com", "", "http://169.254.169.254/latest"]), "prompt": "p"}),
        "WebSearch" => json!({"query": format!("q {}", r.pick(paths))}),
        "Agent" | "Task" => {
            let mut a = json!({"prompt": format!("look at {}", p), "description": "d"});
            if r.chance(40) {
                a["isolation"] = json!(r.pick(&["local", "remote", "worktree", "weird", ""]));
            }
            if r.chance(20) {
                a["name"] = json!("mate");
            }
            if r.chance(10) {
                a["subagent_type"] = json!("general-purpose");
            }
            a
        }
        "Bash" | "PowerShell" | "Monitor" => {
            let mut b = json!({"command": command(r, paths), "description": "d"});
            if tool == "Monitor" && r.chance(20) {
                b = json!({"ws": {"url": "wss://example.com/x"}});
            }
            // item 3 (a): odd command fields (Bash mostly)
            if r.chance(if tool == "Bash" { 12 } else { 4 }) {
                match r.below(5) {
                    0 => b["command"] = json!(12),
                    1 => b["command"] = json!(""),
                    2 => b["command"] = json!("   "),
                    3 => b["command"] = Value::Null,
                    _ => {
                        b.as_object_mut().unwrap().remove("command");
                    }
                }
            }
            b
        }
        "ExitWorktree" => json!({"action": r.pick(&["keep", "remove"])}),
        "ExitPlanMode" => json!({"plan": "x"}),
        "mcp__plugin_coagent_link__share" | "mcp__plugin_coagent_link__send" => {
            json!({"kind": "chat", "text": format!("hi {}", p)})
        }
        "mcp__plugin_coagent_link__wait" => json!({"timeout_s": 5}),
        _ => match r.below(4) {
            0 => json!({}),
            1 => json!({"path": p}),
            2 => json!({"file_path": p, "x": 1}),
            _ => json!({"q": format!("{}", p)}),
        },
    };
    let untaught = known_tool(tool).is_none();
    if r.chance(8) || (untaught && r.chance(40)) {
        v["command"] = json!(command(r, paths));
    }
    // item 3 (b): the flag in every form
    if r.chance(10) {
        v["dangerouslyDisableSandbox"] = match r.below(8) {
            0 => json!("true"),
            1 => json!("false"),
            2 => json!(1),
            3 => json!(0),
            4 => Value::Null,
            5 => json!({}),
            6 => json!(true),
            _ => json!(false),
        };
    }
    if r.chance(2) {
        v["command"] = json!(12); // a non-string command field on any tool
    }
    v
}

/// One generated hook event: (hook json text, parsed input, action). `None` when the hook does not parse.
pub fn hook_and_action(
    r: &mut R,
    fx: &Fx,
    paths: &[String],
    tools: &[String],
) -> Option<(String, HookInput, Action)> {
    let tool = pick_tool(r, tools);
    let input = input_for(r, &tool, paths);
    let cwd: String = match r.below(100) {
        0..=9 => fx.home.to_str().unwrap().into(),
        10..=17 => fx.outside.to_str().unwrap().into(),
        18..=27 => fx.ws.join("src").to_str().unwrap().into(),
        28..=29 => "rel/dir".into(),
        30 => "rel".into(),
        31 => "./x".into(),
        32 => "~/x".into(),
        33 => "../up".into(),
        34..=35 => "".into(),
        _ => fx.ws.to_str().unwrap().into(),
    };
    let session = if r.chance(4) { "sess-other" } else { SESSION };
    let pm = *r.pick(&["default", "default", "plan", "acceptEdits", "bypassPermissions", "dontAsk", "auto"]);
    let mut hook = json!({
        "session_id": session, "cwd": cwd, "hook_event_name": "PreToolUse",
        "tool_name": tool, "tool_input": input
    });
    if !r.chance(5) {
        hook["permission_mode"] = json!(pm);
    }
    let text = hook.to_string();
    let hi = HookInput::parse(&text).ok()?;
    let mut a = classify(&hi, HostOs::Posix, &env(fx), &PosixNormaliser);
    a.share_flagged = match r.below(3) {
        0 => None,
        1 => Some(true),
        _ => Some(false),
    };
    match r.below(100) {
        0..=29 => a.origin = Origin::Member("alice".into()),
        30..=32 => a.origin = Origin::Member("bob".into()),
        _ => {}
    }
    Some((text, hi, a))
}

/// (name, state). The name carries `ex=<set>` and `gx=<grant exclude: none|active|inactive>` and the state's session,
/// so the comparator knows from the harness's own construction whether anything is excluded.
pub fn states(fx: &Fx) -> Vec<(String, State)> {
    let mut out = Vec::new();
    let defaults = patterns::default_exclusions();
    let mut defaults_plus = defaults.clone();
    defaults_plus.push("secret/**".into());
    defaults_plus.push(format!("{}/**", fx.outside.to_str().unwrap()));
    let gex: Vec<String> = vec!["**/.env*".into(), "secret/**".into()];
    // (name, exclusions, grant exclude, force a grant on grant variants AND suspend it)
    let ex_sets: Vec<(&str, Vec<String>, Vec<String>, bool)> = vec![
        ("none", vec![], vec![], false),
        ("env", vec!["**/.env*".into()], vec![], false),
        ("defaults", defaults.clone(), vec![], false),
        ("ws-secret", vec!["<ws>/secret/**".into(), "~/notes/**".into()], vec![], false),
        ("defaults+secret", defaults_plus, vec![], false),
        ("grant-only", vec![], gex.clone(), false),
        ("grant-inactive", vec![], gex.clone(), true),
    ];
    for (en, ex, gx, suspend_all) in ex_sets {
        for link in [LinkPhase::Open, LinkPhase::ClosedTainted] {
            for variant in 0..10 {
                let mut st = base_state(fx, ex.clone());
                st.link = link;
                st.sandbox = [Sandbox::On, Sandbox::Off, Sandbox::Unknown][variant % 3];
                if variant == 1 {
                    st.stopped = true;
                }
                if variant == 2 {
                    st.paused = true;
                }
                let mut gtag = "nogrant";
                if [3, 5, 6, 8].contains(&variant) {
                    let verified: BTreeSet<String> = ["alice".to_string()].into_iter().collect();
                    st.install_grant(
                        &grant_json("2026-11-16T23:59:00Z", "2026-11-17T07:59:00Z", &gx),
                        NOW,
                        3600,
                        &verified,
                        &PosixNormaliser,
                    )
                    .unwrap();
                    gtag = "grant";
                    if variant == 5 || suspend_all {
                        st.grant.as_mut().unwrap().suspended = true;
                        gtag = "grant-suspended";
                    }
                }
                if variant >= 3 && variant != 7 {
                    for c in ["npm test", "sudo ls", "ls", "claude -p hi", "coagent open", "cat ~/.coagent/inbox.json", "grep -r key ."] {
                        st.add_owner_command(c, &fx.ws, ShellKind::Bash, &PosixNormaliser).unwrap();
                    }
                    st.context_from.insert(if variant == 9 { "bob" } else { "alice" }.into());
                }
                if variant == 4 {
                    st.session_id = "sess-other".into();
                }
                let gx_tag = if gtag == "nogrant" || gx.is_empty() { "none" } else { "list" };
                out.push((
                    format!("ex={en} exn={} gx={gx_tag} {gtag} link={link:?} v={variant} sess={}", ex.len(), st.session_id),
                    st,
                ));
            }
        }
    }
    out
}

/// Approvals that may match this action (so steps [9]/[10]/[11] are reached), or an expired one.
pub fn with_approvals(r: &mut R, st: &mut State, a: &Action, fx: &Fx) {
    let exp = |r: &mut R| match r.below(4) {
        0 => Some(Timestamp(NOW.0 - 1)),
        1 => Some(NOW),
        _ => None,
    };
    if r.chance(40) {
        let e = exp(r);
        st.approvals.insert(SessionApproval {
            scope: Scope::ExactInput {
                hash: a.raw_input_hash.clone(),
            },
            expires_at: e,
        });
    }
    if r.chance(30) {
        let e = exp(r);
        let dir = r.pick(&[fx.ws.clone(), fx.home.clone(), fx.root.clone(), fx.ws.join("src")]).clone();
        st.approvals.insert(SessionApproval {
            scope: Scope::ReadsUnder { dir },
            expires_at: e,
        });
    }
    for t in &a.targets {
        if let Target::Path { path, .. } = t {
            if let Some(c) = path.canonical() {
                if r.chance(30) {
                    st.read_memory.insert(c.to_path_buf());
                }
                if r.chance(30) {
                    let e = exp(r);
                    st.approvals.insert(SessionApproval {
                        scope: Scope::EditsToFile {
                            path: c.to_path_buf(),
                        },
                        expires_at: e,
                    });
                }
            }
        }
        if let Target::Url { host: Some(h), .. } = t {
            if r.chance(40) {
                st.approvals.insert(SessionApproval {
                    scope: Scope::FetchesFrom { host: h.clone() },
                    expires_at: None,
                });
            }
        }
        if let Target::Command { .. } = t {
            if r.chance(20) {
                st.approvals.insert(SessionApproval {
                    scope: Scope::ExactCommand {
                        text: "npm test".into(),
                        cwd: fx.ws.clone(),
                    },
                    expires_at: None,
                });
            }
        }
    }
}

/// Every text a decision shows: the allow/deny text, or a card's full Debug plus every reason's text and every
/// option's label.
pub fn dtext(d: &Decision) -> String {
    match d {
        Decision::Allow { why } => why.text(),
        Decision::Deny { reason } => reason.text(),
        Decision::Ask { card } => format!(
            "{card:?} REASONS {:?} OPTIONS {:?}",
            card.reasons.iter().map(|r| r.text()).collect::<Vec<_>>(),
            card.options
                .iter()
                .map(|o| match o {
                    CardOption::AllowForSession(sc) => sc.label(),
                    other => format!("{other:?}"),
                })
                .collect::<Vec<_>>()
        ),
    }
}

/// The scan words of every command target (the D-A-identical action; read by the comparator's item 2 predicate).
pub fn scan_words(a: &Action) -> Vec<String> {
    let mut v = Vec::new();
    for t in &a.targets {
        if let Target::Command { scan, .. } = t {
            v.extend(scan.words.iter().cloned());
        }
    }
    v
}

pub fn seed_n_out() -> (u64, usize, String) {
    let seed: u64 = std::env::var("QA_SEED")
        .ok()
        .and_then(|s| u64::from_str_radix(s.trim_start_matches("0x"), 16).ok())
        .expect("QA_SEED");
    let n: usize = std::env::var("QA_N").ok().and_then(|s| s.parse().ok()).expect("QA_N");
    (seed, n, std::env::var("QA_OUT").expect("QA_OUT"))
}

pub const SURFACES: [Surface; 3] = [Surface::Console, Surface::TerminalPrompt, Surface::None];
pub const NOWS: [Timestamp; 4] = [NOW, Timestamp(NOW.0 + 400), Timestamp(NOW.0 + 86_400), Timestamp(NOW.0 - 120)];
