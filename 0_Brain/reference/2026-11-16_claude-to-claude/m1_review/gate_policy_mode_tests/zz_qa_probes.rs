//! QA POLICY-MODE (independent check): hand probes, mode ON (live, bound, expiry 1 h ahead) at the head.
//! Each probe prints: name | decide (mode absent) | decide_with_mode (shell not verified) | (shell verified).
//! Run with --nocapture; the assertions are only the hard ones (a refusal must never be an allow).
use coagent_policy::*;
use serde_json::{json, Value};
use std::path::{Path, PathBuf};

const NOW: Timestamp = Timestamp(1_794_873_600);
const S: &str = "sess-p";

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
}

fn fx() -> Fx {
    let root = PathBuf::from("/private/tmp/claude-501/qpm/fxp");
    for r in [
        "ws/README.md", "ws/.env", "ws/.claude/settings.json", "ws/.git/config", "ws/Makefile", "ws/sub/.git/config",
        "home/.ssh/id_rsa", "home/.claude/settings.json", "home/.claude.json", "home/.coagent/inbox.json",
        "home/.gitconfig", "home/.config/git/config", "home/.local/bin/t", "home/Library/LaunchAgents/a.plist",
        "home/.cargo/config.toml", "home/.vimrc", "home/.tmux.conf", "home/.oh-my-zsh/x.zsh", "home/.zshrc",
        "home/notes/n.txt", "gate/inbox.json",
    ] {
        touch(&root.join(r));
    }
    let l = root.join("ws/lnk");
    if std::fs::symlink_metadata(&l).is_err() {
        std::os::unix::fs::symlink(root.join("home/.coagent"), &l).unwrap();
    }
    let c = |p: PathBuf| std::fs::canonicalize(p).unwrap();
    Fx { ws: c(root.join("ws")), home: c(root.join("home")), root: c(root) }
}

fn state(f: &Fx, ex: &[&str]) -> State {
    State::new(
        StateConfig {
            session_id: S.into(),
            host: HostOs::Posix,
            env: Env { home: f.home.clone() },
            workspace_roots: vec![f.ws.clone()],
            exclusions: ex.iter().map(|s| s.to_string()).collect(),
            extra_gate_dirs: vec![f.root.join("gate")],
            approval_timeout_secs: 300,
        },
        &PosixNormaliser,
    )
    .unwrap()
}

fn act(f: &Fx, cwd: &Path, tool: &str, input: Value) -> Action {
    let h = HookInput::parse(
        &json!({"session_id": S, "cwd": cwd.to_str().unwrap(), "hook_event_name": "PreToolUse",
                "tool_name": tool, "tool_input": input, "permission_mode": "default"})
        .to_string(),
    )
    .unwrap();
    classify(&h, HostOs::Posix, &Env { home: f.home.clone() }, &PosixNormaliser)
}

fn mode(sh: bool) -> BypassView {
    BypassView {
        consent_set_id: "cs-p".into(),
        expires_at: Timestamp(NOW.0 + 3600),
        bound_sessions: [S.to_string()].into_iter().collect(),
        shell_verified: sh,
    }
}

fn short(d: &Decision) -> String {
    match d {
        Decision::Allow { why } => format!("ALLOW {why:?}"),
        Decision::Deny { reason } => format!("DENY {reason:?}"),
        Decision::Ask { card } => format!("ASK {:?} {:?}", card.tier, card.reasons),
    }
}

#[test]
fn qa_probes() {
    let f = fx();
    let h = f.home.to_str().unwrap().to_string();
    let w = f.ws.to_str().unwrap().to_string();
    let g = f.root.join("gate").to_str().unwrap().to_string();
    let plain = state(&f, &[]);
    let excl = state(&f, &["**/.env*"]);
    let home = f.home.clone();
    let ws = f.ws.clone();
    // (name, state, cwd, tool, input, must_not_be_mode_allow)
    let cases: Vec<(&str, &State, &PathBuf, &str, Value, bool)> = vec![
        // credentials
        ("read ~/.ssh/id_rsa", &plain, &ws, "Read", json!({"file_path": "~/.ssh/id_rsa"}), true),
        ("read ~/.SSH/ID_RSA (case)", &plain, &ws, "Read", json!({"file_path": "~/.SSH/ID_RSA"}), true),
        ("read ~/.ssh//id_rsa/ (slashes)", &plain, &ws, "Read", json!({"file_path": format!("{h}//.ssh//id_rsa")}), true),
        ("read via ..", &plain, &ws, "Read", json!({"file_path": format!("{w}/../home/.ssh/id_rsa")}), true),
        ("LS ~/.ssh", &plain, &ws, "LS", json!({"path": "~/.ssh"}), true),
        ("grep ~ (folder above creds)", &plain, &ws, "Grep", json!({"pattern": "x", "path": "~"}), true),
        ("grep path '' cwd=home", &plain, &home, "Grep", json!({"pattern": "x", "path": ""}), true),
        ("glob path '' cwd=home", &plain, &home, "Glob", json!({"pattern": "**/*", "path": ""}), true),
        ("grep no path cwd=home", &plain, &home, "Grep", json!({"pattern": "x"}), true),
        ("grep path '~other' cwd=home", &plain, &home, "Grep", json!({"pattern": "x", "path": "~root"}), true),
        // gate files (read role)
        ("read ~/.coagent/inbox.json", &plain, &ws, "Read", json!({"file_path": "~/.coagent/inbox.json"}), true),
        ("read ws/lnk/inbox.json (symlink to ~/.coagent)", &plain, &ws, "Read", json!({"file_path": format!("{w}/lnk/inbox.json")}), true),
        ("read gate dir file", &plain, &ws, "Read", json!({"file_path": format!("{g}/inbox.json")}), true),
        ("read ~/.claude/settings.json", &plain, &ws, "Read", json!({"file_path": "~/.claude/settings.json"}), true),
        ("read ~/.claude.json", &plain, &ws, "Read", json!({"file_path": "~/.claude.json"}), true),
        ("read ws/.claude/settings.json", &plain, &ws, "Read", json!({"file_path": ".claude/settings.json"}), true),
        ("notebookread ~/.coagent/inbox.json", &plain, &ws, "NotebookRead", json!({"notebook_path": "~/.coagent/inbox.json"}), true),
        ("LS ~/.coagent", &plain, &ws, "LS", json!({"path": "~/.coagent/"}), true),
        ("grep ~/.coagent", &plain, &ws, "Grep", json!({"pattern": "x", "path": "~/.coagent"}), true),
        ("glob ~ pattern .coagent/*", &plain, &ws, "Glob", json!({"pattern": ".coagent/*", "path": "~"}), true),
        ("grep /etc (above a gate folder, no credential below)", &plain, &ws, "Grep", json!({"pattern": "x", "path": "/etc"}), true),
        ("grep /Library (above managed policy)", &plain, &ws, "Grep", json!({"pattern": "x", "path": "/Library"}), true),
        ("grep ~/Documents (above PowerShell profiles)", &plain, &ws, "Grep", json!({"pattern": "x", "path": "~/Documents"}), true),
        ("read /etc/claude-code/managed-settings.json", &plain, &ws, "Read", json!({"file_path": "/etc/claude-code/managed-settings.json"}), true),
        ("read ~/.zshrc (hard-deny list)", &plain, &ws, "Read", json!({"file_path": "~/.zshrc"}), true),
        ("grep ws with glob .claude/** (DQ-3)", &plain, &ws, "Grep", json!({"pattern": "x", "path": w, "glob": ".claude/**"}), false),
        ("grep ws (holds .claude/) (DQ-3)", &plain, &ws, "Grep", json!({"pattern": "x", "path": w}), false),
        ("webfetch file:// gate file (host behaviour unverified)", &plain, &ws, "WebFetch", json!({"url": format!("file://{h}/.coagent/inbox.json"), "prompt": "p"}), false),
        // later-running writes
        ("write ~/.gitconfig", &plain, &ws, "Write", json!({"file_path": "~/.gitconfig", "content": "x"}), true),
        ("edit ~/.config/git/config", &plain, &ws, "Edit", json!({"file_path": "~/.config/git/config", "old_string": "a", "new_string": "b"}), true),
        ("write ~/.local/bin/t", &plain, &ws, "Write", json!({"file_path": "~/.local/bin/t", "content": "x"}), true),
        ("write ~/Library/LaunchAgents/a.plist", &plain, &ws, "Write", json!({"file_path": "~/Library/LaunchAgents/a.plist", "content": "x"}), true),
        ("write ~/.cargo/config.toml (DQ-1)", &plain, &ws, "Write", json!({"file_path": "~/.cargo/config.toml", "content": "x"}), true),
        ("multiedit ~/.vimrc", &plain, &ws, "MultiEdit", json!({"file_path": "~/.vimrc", "edits": []}), true),
        ("notebookedit ~/.tmux.conf", &plain, &ws, "NotebookEdit", json!({"notebook_path": "~/.tmux.conf", "new_source": "x"}), true),
        ("write ~/.oh-my-zsh/x.zsh", &plain, &ws, "Write", json!({"file_path": "~/.oh-my-zsh/x.zsh", "content": "x"}), true),
        ("write ws/.git/config", &plain, &ws, "Write", json!({"file_path": ".git/config", "content": "x"}), true),
        ("write ws/sub/.git/config", &plain, &ws, "Write", json!({"file_path": "sub/.git/config", "content": "x"}), true),
        ("write ws/.GIT/config (case)", &plain, &ws, "Write", json!({"file_path": ".GIT/config", "content": "x"}), true),
        ("write ws/.git (the file)", &plain, &ws, "Write", json!({"file_path": ".git", "content": "gitdir: /x"}), true),
        ("write ws/Makefile (Q-3: stays allowed)", &plain, &ws, "Write", json!({"file_path": "Makefile", "content": "x"}), false),
        ("write ws/CLAUDE.md (Q-3: stays allowed)", &plain, &ws, "Write", json!({"file_path": "CLAUDE.md", "content": "x"}), false),
        // may read excluded
        ("grep ws with **/.env* excluded", &excl, &ws, "Grep", json!({"pattern": "x", "path": w}), true),
        ("glob ws with **/.env* excluded", &excl, &ws, "Glob", json!({"pattern": "*", "path": w}), true),
        ("grep no path (cwd ws) with **/.env* excluded", &excl, &ws, "Grep", json!({"pattern": "x"}), true),
        ("grep path '' (cwd ws) with **/.env* excluded", &excl, &ws, "Grep", json!({"pattern": "x", "path": ""}), true),
        ("grep path '.' with **/.env* excluded", &excl, &ws, "Grep", json!({"pattern": "x", "path": "."}), true),
        // strict kinds
        ("untaught tool", &plain, &ws, "MadeUp", json!({}), true),
        ("mcp untaught", &plain, &ws, "mcp__x__y", json!({}), true),
        ("inbox_read", &plain, &ws, "mcp__plugin_coagent_link__inbox_read", json!({}), true),
        ("wait", &plain, &ws, "mcp__plugin_coagent_link__wait", json!({"timeout_s": 5}), true),
        ("agent remote", &plain, &ws, "Agent", json!({"prompt": "x", "isolation": "remote"}), true),
        ("agent teammate", &plain, &ws, "Agent", json!({"prompt": "x", "name": "t"}), true),
        ("exit worktree", &plain, &ws, "ExitWorktree", json!({"action": "remove"}), true),
        ("exit plan mode", &plain, &ws, "ExitPlanMode", json!({"plan": "x"}), true),
        ("send (nothing scans)", &plain, &ws, "mcp__plugin_coagent_link__send", json!({"kind": "chat", "text": "hi"}), true),
        ("share (nothing scans)", &plain, &ws, "mcp__plugin_coagent_link__share", json!({"text": "hi"}), true),
        ("read with dangerouslyDisableSandbox", &plain, &ws, "Read", json!({"file_path": "README.md", "dangerouslyDisableSandbox": true}), true),
        // shell
        ("bash npm test", &plain, &ws, "Bash", json!({"command": "npm test"}), false),
        ("bash npm test, sandbox off flag", &plain, &ws, "Bash", json!({"command": "npm test", "dangerouslyDisableSandbox": true}), true),
        ("powershell npm test", &plain, &ws, "PowerShell", json!({"command": "npm test"}), false),
        ("monitor npm test", &plain, &ws, "Monitor", json!({"command": "npm test"}), false),
        ("todowrite with command field", &plain, &ws, "TodoWrite", json!({"todos": [], "command": "npm test"}), false),
        ("bash sudo", &plain, &ws, "Bash", json!({"command": "sudo ls"}), true),
        ("bash /usr/bin/sudo", &plain, &ws, "Bash", json!({"command": "/usr/bin/sudo ls"}), true),
        ("bash claude -p", &plain, &ws, "Bash", json!({"command": "claude -p hi"}), true),
        ("bash /usr/local/bin/claude", &plain, &ws, "Bash", json!({"command": "/usr/local/bin/claude -p hi"}), true),
        ("bash CLAUDE (case)", &plain, &ws, "Bash", json!({"command": "CLAUDE -p hi"}), true),
        ("bash c\"laude (quotes)", &plain, &ws, "Bash", json!({"command": "c\"laude\" -p hi"}), true),
        ("bash npx claude", &plain, &ws, "Bash", json!({"command": "npx claude -p hi"}), true),
        ("bash coagent open", &plain, &ws, "Bash", json!({"command": "coagent open"}), true),
        ("bash ./target/release/coagentd", &plain, &ws, "Bash", json!({"command": "./target/release/coagentd --x"}), true),
        ("bash echo|coagent-hook", &plain, &ws, "Bash", json!({"command": "echo {} | coagent-hook"}), true),
        ("bash claude-code (not on list)", &plain, &ws, "Bash", json!({"command": "claude-code -p hi"}), false),
        ("bash $(echo claude) (text only)", &plain, &ws, "Bash", json!({"command": "$(printf cl; printf aude) -p hi"}), false),
        ("bash c''laude", &plain, &ws, "Bash", json!({"command": "c''laude -p hi"}), true),
        ("bash cat ~/.ssh/id_rsa", &plain, &ws, "Bash", json!({"command": "cat ~/.ssh/id_rsa"}), true),
        ("bash cat ~/.ss''h/id_rsa", &plain, &ws, "Bash", json!({"command": "cat ~/.ss''h/id_rsa"}), true),
        ("bash cat ~/.ss*/id_rsa", &plain, &ws, "Bash", json!({"command": "cat ~/.ss*/id_rsa"}), true),
        ("bash cat $HOME/.coagent/inbox.json", &plain, &ws, "Bash", json!({"command": "cat $HOME/.coagent/inbox.json"}), true),
        ("bash echo x >> ~/.gitconfig", &plain, &ws, "Bash", json!({"command": "echo x >> ~/.gitconfig"}), true),
        ("bash cd ~ && echo x >> .gitconfig (DQ-4 by name)", &plain, &ws, "Bash", json!({"command": "cd ~ && echo x >> .gitconfig"}), true),
        ("bash cd ~ && echo x >> .gitconfig (DQ-4, cwd=ws file of that name)", &plain, &ws, "Bash", json!({"command": "echo x >> sub/.gitconfig"}), true),
        ("bash cp x ~/.local/bin/", &plain, &ws, "Bash", json!({"command": "cp x ~/.local/bin/"}), true),
        ("bash git config core.hooksPath h", &plain, &ws, "Bash", json!({"command": "git config core.hooksPath h"}), false),
        ("bash cd ~ && cat .ssh/id_rsa", &plain, &ws, "Bash", json!({"command": "cd ~ && cat .ssh/id_rsa"}), true),
        ("bash --dangerously-skip-permissions", &plain, &ws, "Bash", json!({"command": "x --dangerously-skip-permissions"}), true),
        ("bash pkexec", &plain, &ws, "Bash", json!({"command": "pkexec id"}), true),
    ];
    let mut bad = Vec::new();
    for (name, st, cwd, tool, input, must) in cases {
        let a = act(&f, cwd, tool, input);
        let d0 = decide(&a, st, Surface::Console, NOW);
        let d1 = decide_with_mode(&a, st, Some(&mode(false)), Surface::Console, NOW);
        let d2 = decide_with_mode(&a, st, Some(&mode(true)), Surface::Console, NOW);
        let ma = |d: &Decision| matches!(d, Decision::Allow { why: AllowWhy::Bypass { .. } });
        println!("PROBE {name} | strict={:?} targets={:?}\n   absent: {}\n   mode  : {}\n   mode+sh: {}", a.strict, a.targets.iter().map(|t| format!("{t:?}").chars().take(160).collect::<String>()).collect::<Vec<_>>(), short(&d0), short(&d1), short(&d2));
        if must && (ma(&d1) || ma(&d2)) {
            bad.push(name);
        }
    }
    println!("QA-PROBES mode-allowed although expected refused: {bad:?}");
}

/// CriticalSpelling is produced only by the Windows normaliser (`path/windows.rs`); on POSIX the probe builds the
/// target by hand, for a Read and a Write.
#[test]
fn qa_probe_critical_spelling() {
    let f = fx();
    let st = state(&f, &[]);
    for tool in ["Read", "Write"] {
        let mut a = act(&f, &f.ws, tool, json!({"file_path": "README.md", "content": "x"}));
        let role = if tool == "Read" { PathRole::Read } else { PathRole::Write };
        a.targets = vec![Target::Path { role, path: NormPath::Critical { raw: r"C:\ws\a.txt:secret".into(), why: "alternate data stream suffix (':')" } }];
        let d0 = decide(&a, &st, Surface::Console, NOW);
        let d1 = decide_with_mode(&a, &st, Some(&mode(true)), Surface::Console, NOW);
        println!("PROBE critical {tool}\n   absent: {}\n   mode+sh: {}", short(&d0), short(&d1));
        assert!(matches!(d1, Decision::Deny { reason: DenyReason::BypassRefused { reason: "a path spelled in a way that needs care" } }));
    }
}
