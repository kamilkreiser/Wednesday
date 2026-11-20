//! QA POLICY-MODE r2: lines 1-613 of the first check's zz_qa_mode.rs (generator + mode_set; only the scratch
//! path prefix qpm/ -> qpm2/ changed), plus a writer of EVERY decide_with_mode result, compiled at fc7acfc and head.
#![allow(dead_code)]
use coagent_policy::*;
use serde_json::{json, Value};
use std::collections::BTreeSet;
use std::io::Write;
use std::path::{Path, PathBuf};

struct R(u64);
impl R {
    fn next(&mut self) -> u64 {
        // splitmix64
        self.0 = self.0.wrapping_add(0x9E37_79B9_7F4A_7C15);
        let mut z = self.0;
        z = (z ^ (z >> 30)).wrapping_mul(0xBF58_476D_1CE4_E5B9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94D0_49BB_1331_11EB);
        z ^ (z >> 31)
    }
    fn below(&mut self, n: usize) -> usize {
        (self.next() % n as u64) as usize
    }
    fn pick<'a, T>(&mut self, v: &'a [T]) -> &'a T {
        &v[self.below(v.len())]
    }
    fn chance(&mut self, pct: u64) -> bool {
        self.next() % 100 < pct
    }
}

const NOW: Timestamp = Timestamp(1_794_873_600);
const SESSION: &str = "sess-q";

fn touch(p: &Path) {
    std::fs::create_dir_all(p.parent().unwrap()).unwrap();
    if !p.exists() {
        std::fs::write(p, "x\n").unwrap();
    }
}

struct Fx {
    root: PathBuf,
    ws: PathBuf,
    home: PathBuf,
    outside: PathBuf,
}

fn fixture() -> Fx {
    let root = PathBuf::from("/private/tmp/claude-501/qpm2/fx");
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

fn env(fx: &Fx) -> Env {
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

fn grant_json(issued: &str, expires: &str) -> String {
    json!({
        "grant_id": "gr_q", "session_id": SESSION, "issuer": "host", "subjects": ["alice"],
        "issued_at": issued, "expires_at": expires,
        "scopes": [
            {"kind": "read", "paths": ["<ws>/**", "~/**", "/**"]},
            {"kind": "search", "paths": ["<ws>/**", "~/**", "/**"]},
            {"kind": "edit", "paths": ["<ws>/**", "~/**", "/**"]},
            {"kind": "execute", "commands": ["npm test", "ls", "cat README.md", "sudo ls", "claude -p hi", "coagent open", "git status"]},
            {"kind": "fetch", "domains": ["example.com", "*.example.com"]},
            {"kind": "service", "tools": ["github:*", "plugin_coagent_link:*"]},
            {"kind": "share", "policy": "auto_unless_flagged", "max_bytes": 1000000}
        ],
        "sandbox_required_for_execute": false,
        "sig": "verified-by-caller"
    })
    .to_string()
}

/// Path spellings: absolute, `~`, relative to the workspace, `..`, doubled slashes, trailing slashes, case variants,
/// symlinks, `$HOME`, globs, odd characters.
fn path_pool(fx: &Fx) -> Vec<String> {
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
        format!("{ws}/.CLAUDE/settings.json"),
        format!("{ws}/.mcp.json"),
        format!("{ws}/.git/config"),
        format!("{ws}/.git/hooks/pre-commit"),
        format!("{ws}/.git"),
        format!("{ws}/.git/"),
        format!("{ws}/.GIT/config"),
        format!("{ws}/sub/.git/config"),
        format!("{ws}/Makefile"),
        format!("{ws}/CLAUDE.md"),
        format!("{ws}/package.json"),
        format!("{ws}/.cargo/config.toml"),
        format!("{ws}/link_to_coagent/inbox.json"),
        format!("{ws}/link_to_coagent"),
        format!("{ws}/link_to_ssh/id_rsa"),
        format!("{ws}//src//main.rs"),
        format!("{ws}/src/../.claude/settings.json"),
        format!("{ws}/../home/.coagent/inbox.json"),
        format!("{ws}/../home/.ssh/id_rsa"),
        format!("{ws}/missing/new.txt"),
        format!("{ws}/*.rs"),
        format!("{ws}/src/[ab].rs"),
        "README.md".into(),
        "src/main.rs".into(),
        ".env".into(),
        ".claude/settings.json".into(),
        ".git/config".into(),
        "../home/.coagent/inbox.json".into(),
        "../outside/secret.txt".into(),
        "./CLAUDE.md".into(),
        "~/.ssh/id_rsa".into(),
        "~/.ssh".into(),
        "~/.SSH/id_rsa".into(),
        "~/.claude/settings.json".into(),
        "~/.claude".into(),
        "~/.claude/".into(),
        "~/.claude.json".into(),
        "~/.coagent/inbox.json".into(),
        "~/.coagent/identity.key".into(),
        "~/.coagent".into(),
        "~/.coagent/".into(),
        "~/.Coagent/inbox.json".into(),
        "~/.zshrc".into(),
        "~/.gitconfig".into(),
        "~/.GITCONFIG".into(),
        "~/.config/git/config".into(),
        "~/.local/bin/tool".into(),
        "~/.local/bin/".into(),
        "~/Library/LaunchAgents/a.plist".into(),
        "~/.cargo/config.toml".into(),
        "~/.cargo/credentials.toml".into(),
        "~/.aws/credentials".into(),
        "~/notes/todo.txt".into(),
        "~/.vimrc".into(),
        "~".into(),
        "~/".into(),
        "$HOME/.coagent/inbox.json".into(),
        "${HOME}/.ssh/id_rsa".into(),
        format!("{home}/.coagent/inbox.json"),
        format!("{home}//.coagent//inbox.json"),
        format!("{home}/.coagent/../.coagent/inbox.json"),
        format!("{home}/.ssh/id_rsa"),
        format!("{home}/.claude/settings.json"),
        format!("{home}/.gitconfig"),
        format!("{home}/.local/bin/tool"),
        format!("{home}/notes/todo.txt"),
        format!("{home}/notes"),
        home.clone(),
        format!("{home}/"),
        format!("{out}/secret.txt"),
        out.clone(),
        format!("{root}/gate-config/inbox.json"),
        format!("{root}/gate-config"),
        root.clone(),
        "/".into(),
        "/etc/profile".into(),
        "/etc/claude-code/managed-settings.json".into(),
        "/Library/Application Support/ClaudeCode/managed-settings.json".into(),
        "/tmp/x.txt".into(),
        "/usr/bin".into(),
        r"C:\ws\a.txt:secret".into(),
        r"\\server\share\x".into(),
        "file.txt:stream".into(),
        "".into(),
        "weird\u{202e}name.txt".into(),
        "a\nb".into(),
        "%2e%2e/x".into(),
    ];
    v.sort();
    v.dedup();
    v
}

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

fn command(r: &mut R, paths: &[String]) -> String {
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
    if r.chance(3) {
        s.push_str(&" a".repeat(r.below(40_000)));
    }
    s
}

fn tools() -> Vec<String> {
    let mut v: Vec<String> = KNOWN_TOOLS.iter().map(|t| t.name.to_string()).collect();
    for t in [
        "Bash", "PowerShell", "Monitor", "ExitPlanMode", "ExitWorktree", "EnterWorktree", "MadeUpTool", "bash", "BASH",
        "read", "Read ", "Skill", "SlashCommand", "KillShell", "BashOutput", "RemoteTrigger", "CronCreate",
        "mcp__github__create_issue", "mcp__plugin_coagent_link__inbox_read", "mcp__plugin_coagent_link__wait",
        "mcp__plugin_coagent_link__share", "mcp__plugin_coagent_link__send", "mcp__plugin_coagent_link__x",
        "mcp__browser__click", "mcp__", "",
    ] {
        v.push(t.to_string());
    }
    v
}

fn input_for(r: &mut R, tool: &str, paths: &[String]) -> Value {
    let p = r.pick(paths).clone();
    let mut v = match tool {
        "Read" | "NotebookRead" => json!({"file_path": p}),
        "LS" => json!({"path": p}),
        "Glob" => {
            if r.chance(50) {
                json!({"pattern": r.pick(&["**/*.rs", "*", ".claude/**", "**/.env*", "**"]), "path": p})
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
            "https://[::1]/", "ftp://example.com", "https://ex%61mple.com", ""]), "prompt": "p"}),
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
    if r.chance(8) {
        v["command"] = json!(command(r, paths));
    }
    if r.chance(6) {
        v["dangerouslyDisableSandbox"] = json!(r.chance(70));
    }
    if r.chance(3) {
        v["command"] = json!(12); // a non-string command field
    }
    v
}

fn action(r: &mut R, fx: &Fx, paths: &[String], tools: &[String]) -> (Action, Option<bool>) {
    let tool = r.pick(tools).clone();
    let input = input_for(r, &tool, paths);
    let cwd = match r.below(10) {
        0 => fx.home.clone(),
        1 => fx.outside.clone(),
        2 => fx.ws.join("src"),
        _ => fx.ws.clone(),
    };
    let session = if r.chance(4) { "sess-other" } else { SESSION };
    let pm = *r.pick(&["default", "default", "plan", "acceptEdits", "bypassPermissions", "dontAsk", "auto"]);
    let mut hook = json!({
        "session_id": session, "cwd": cwd.to_str().unwrap(), "hook_event_name": "PreToolUse",
        "tool_name": tool, "tool_input": input
    });
    if !r.chance(5) {
        hook["permission_mode"] = json!(pm);
    }
    let hi = HookInput::parse(&hook.to_string()).unwrap();
    let mut a = classify(&hi, HostOs::Posix, &env(fx), &PosixNormaliser);
    let flag = match r.below(3) {
        0 => None,
        1 => Some(true),
        _ => Some(false),
    };
    a.share_flagged = flag;
    match r.below(100) {
        0..=29 => a.origin = Origin::Member("alice".into()),
        30..=32 => a.origin = Origin::Member("bob".into()),
        _ => {}
    }
    (a, flag)
}

fn states(fx: &Fx) -> Vec<(String, State)> {
    let mut out = Vec::new();
    let mut defaults = patterns::default_exclusions();
    let ex_sets: Vec<(&str, Vec<String>)> = vec![
        ("none", vec![]),
        ("env", vec!["**/.env*".into()]),
        ("defaults", defaults.clone()),
        ("ws-secret", vec!["<ws>/secret/**".into(), "~/notes/**".into()]),
        ("defaults+", {
            defaults.push("secret/**".into());
            defaults.push("/private/tmp/claude-501/qpm2/fx/outside/**".into());
            defaults
        }),
    ];
    for (en, ex) in ex_sets {
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
                if [3, 5, 6, 8].contains(&variant) {
                    let verified: BTreeSet<String> = ["alice".to_string()].into_iter().collect();
                    st.install_grant(
                        &grant_json("2026-11-16T23:59:00Z", "2026-11-17T07:59:00Z"),
                        NOW,
                        3600,
                        &verified,
                        &PosixNormaliser,
                    )
                    .unwrap();
                    if variant == 5 {
                        st.grant.as_mut().unwrap().suspended = true;
                    }
                }
                if variant >= 3 && variant != 7 {
                    for c in ["npm test", "sudo ls", "ls", "claude -p hi", "coagent open", "cat ~/.coagent/inbox.json"] {
                        st.add_owner_command(c, &fx.ws, ShellKind::Bash, &PosixNormaliser).unwrap();
                    }
                    st.context_from.insert(if variant == 9 { "bob" } else { "alice" }.into());
                }
                if variant == 4 {
                    st.session_id = "sess-other".into();
                }
                out.push((format!("ex={en} link={link:?} v={variant}"), st));
            }
        }
    }
    out
}

/// Approvals that may match this action (so steps [9]/[10]/[11] are reached), or an expired one.
fn with_approvals(r: &mut R, st: &mut State, a: &Action, fx: &Fx) {
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

#[allow(dead_code)]
fn qa_decide_differential() {
    let seed: u64 = std::env::var("QA_SEED")
        .ok()
        .and_then(|s| u64::from_str_radix(s.trim_start_matches("0x"), 16).ok())
        .unwrap_or(0x9a11_c0de_2026_1120);
    let n: usize = std::env::var("QA_N")
        .ok()
        .and_then(|s| s.parse().ok())
        .unwrap_or(200_000);
    let out_path = std::env::var("QA_OUT").unwrap_or_else(|_| "/private/tmp/claude-501/qpm2/diff_out.txt".into());
    let fx = fixture();
    let paths = path_pool(&fx);
    let tools = tools();
    let sts = states(&fx);
    let surfaces = [Surface::Console, Surface::TerminalPrompt, Surface::None];
    let nows = [NOW, Timestamp(NOW.0 + 400), Timestamp(NOW.0 + 86_400), Timestamp(NOW.0 - 120)];
    let mut r = R(seed);
    let mut f = std::io::BufWriter::new(std::fs::File::create(&out_path).unwrap());
    let mut cases = 0usize;
    let (mut allows, mut asks, mut denies, mut panics) = (0usize, 0usize, 0usize, 0usize);
    writeln!(f, "seed {seed:#x} n {n} states {} paths {} tools {}", sts.len(), paths.len(), tools.len()).unwrap();
    for i in 0..n {
        let (a, _) = action(&mut r, &fx, &paths, &tools);
        writeln!(f, "A{i} {} strict={:?} kind={:?} targets={:?}", a.tool_name, a.strict, a.kind, a.targets).unwrap();
        for _ in 0..5 {
            let si = r.below(sts.len());
            let mut st = sts[si].1.clone();
            with_approvals(&mut r, &mut st, &a, &fx);
            let surface = surfaces[r.below(3)];
            let now = nows[r.below(nows.len())];
            let res = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| decide(&a, &st, surface, now)));
            cases += 1;
            match res {
                Ok(d) => {
                    match &d {
                        Decision::Allow { .. } => allows += 1,
                        Decision::Ask { .. } => asks += 1,
                        Decision::Deny { .. } => denies += 1,
                    }
                    writeln!(f, " s{si} {surface:?} {} {d:?}", now.0).unwrap();
                }
                Err(_) => {
                    panics += 1;
                    writeln!(f, " s{si} {surface:?} {} PANIC", now.0).unwrap();
                }
            }
        }
    }
    writeln!(f, "cases {cases} allow {allows} ask {asks} deny {denies} panic {panics}").unwrap();
    eprintln!("QA-DIFF seed {seed:#x}: {cases} cases; allow {allows} ask {asks} deny {denies} panic {panics}");
}

// ===== QA POLICY-MODE: mode properties (head only), independent oracles =====

fn mode_set(now: Timestamp) -> Vec<Option<BypassView>> {
    let v = |exp: i64, s: &[&str], sh: bool, id: &str| {
        Some(BypassView {
            consent_set_id: id.to_string(),
            expires_at: Timestamp(now.0 + exp),
            bound_sessions: s.iter().map(|x| x.to_string()).collect(),
            shell_verified: sh,
        })
    };
    vec![
        None,
        v(3600, &[SESSION], false, "cs-1"),
        v(3600, &[SESSION], true, "cs-1"),
        v(1, &[SESSION, "sess-other"], true, ""),
        v(0, &[SESSION], true, "cs-1"),
        v(-1, &[SESSION], true, "cs-1"),
        v(3600, &[], true, "cs-1"),
        v(3600, &["sess-other"], true, "cs-1"),
        v(3600, &[""], true, "cs-1"),
        v(i64::MAX / 4, &[SESSION], true, "cs\u{202e}\u{1b}[31mx"),
    ]
}

fn own_role(r: &PathRole) -> bool {
    !matches!(r, PathRole::Mentioned | PathRole::InText)
}

#[test]
fn qa_r2_mode_dump() {
    let seed: u64 = std::env::var("QA_SEED")
        .ok()
        .and_then(|s| u64::from_str_radix(s.trim_start_matches("0x"), 16).ok())
        .unwrap_or(0x51de_0f_2026_1120);
    let n: usize = std::env::var("QA_N").ok().and_then(|s| s.parse().ok()).unwrap_or(60_000);
    let out_path = std::env::var("QA_OUT").expect("QA_OUT");
    let fx = fixture();
    let paths = path_pool(&fx);
    let tools = tools();
    let sts = states(&fx);
    let surfaces = [Surface::Console, Surface::TerminalPrompt, Surface::None];
    let nows = [NOW, Timestamp(NOW.0 + 400), Timestamp(NOW.0 + 86_400)];
    let mut r = R(seed);
    let mut f = std::io::BufWriter::new(std::fs::File::create(&out_path).unwrap());
    let mut cases = 0usize;
    for i in 0..n {
        let (a, _) = action(&mut r, &fx, &paths, &tools);
        // cand: the action carries one of the two new properties (an own-role path not Certain, or a fetch with no host)
        let unresolved = a.targets.iter().any(|t| matches!(t, Target::Path { role, path } if own_role(role) && !matches!(path, NormPath::Certain { .. })));
        let nonweb = a.kind == Kind::Fetch && a.targets.iter().any(|t| matches!(t, Target::Url { host: None, .. }));
        // ord: an ordinary resolved action (at least one own-role path, every own-role path Certain; or a fetch whose URL has a host)
        let own: Vec<&NormPath> = a.targets.iter().filter_map(|t| match t { Target::Path { role, path } if own_role(role) => Some(path), _ => None }).collect();
        let ord_path = !own.is_empty() && own.iter().all(|p| matches!(p, NormPath::Certain { .. }));
        let ord_fetch = a.kind == Kind::Fetch && a.targets.iter().any(|t| matches!(t, Target::Url { host: Some(_), .. })) && !nonweb;
        let cand = unresolved || nonweb;
        let ord = !cand && (ord_path || ord_fetch);
        writeln!(f, "A{i} {} kind={:?} strict={:?} unres={} nonweb={} ord={} targets={:?}", a.tool_name, a.kind, a.strict, unresolved as u8, nonweb as u8, ord as u8, a.targets).unwrap();
        for j in 0..2 {
            let si = r.below(sts.len());
            let (_sname, base) = &sts[si];
            let mut st = base.clone();
            with_approvals(&mut r, &mut st, &a, &fx);
            let surface = surfaces[r.below(3)];
            let now = nows[r.below(nows.len())];
            for (k, m) in mode_set(now).into_iter().enumerate() {
                cases += 1;
                let d = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| decide_with_mode(&a, &st, m.as_ref(), surface, now)));
                match d {
                    Ok(d) => writeln!(f, " A{i} c{j} s{si} m{k} cand={} ord={} {d:?}", cand as u8, ord as u8).unwrap(),
                    Err(_) => writeln!(f, " A{i} c{j} s{si} m{k} cand={} ord={} PANIC", cand as u8, ord as u8).unwrap(),
                }
            }
        }
    }
    writeln!(f, "cases {cases}").unwrap();
    eprintln!("QA-R2-MODE seed {seed:#x}: {cases} decide_with_mode cases over {n} actions");
}
