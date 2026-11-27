//! QA-POLICY-B harness (the check's OWN; never committed; never inside a tree whose whole suite runs). The SAME file
//! is compiled at the base 5cab5e4 and the head cd7b6fd, each tree with its own empty target dir. It uses the crate's
//! public API, the protected test helpers `common`, `bypass_common`, `owner_common` (byte-identical at both SHAs) and
//! one per-tree adapter `qpb_adapter` (head: scan B's own figures through `shell::scan_free_text`; base: none).
//! Every generated hook comes from the ONE generator in this file.
//!
//! Modes (env QPB_MODE):
//!   diff  : rows from $QPB_ROWS (jsonl) + generated corpus (seed $QPB_SEED, sizes $QPB_N2, $QPB_N3, fraction
//!           $QPB_FRAC of the generated part), every row x 9 states x 12 columns, one JSON line per row to $QPB_OUT.
//!   time  : rows from $QPB_ROWS, indices $QPB_IDX (comma list), list $QPB_LIST (def|env|long): per row the smallest of
//!           five of (classify + the four columns), printed as `QPB-TIME <idx> <list> <micros> <codes>`.
//! The fixture is built at a FIXED root ($QPB_FIX); base and head of one comparison run one after the other on it, so
//! every path and every card's byte count is the same text in both outputs (the root is masked anyway).
#![cfg(unix)]
mod bypass_common;
mod common;
mod owner_common;
mod qpb_adapter;
use bypass_common::*;
use coagent_policy::*;
use common::*;
use owner_common::*;
use serde_json::{json, Value};
use std::collections::BTreeSet;
use std::io::Write;
use std::path::{Path, PathBuf};
use std::time::{Duration, Instant};

fn touch(p: &Path, content: &str) {
    std::fs::create_dir_all(p.parent().unwrap()).unwrap();
    std::fs::write(p, content).unwrap();
}

/// `common::fixture` + `mode_fixture`'s files, at a fixed root (moved aside, never deleted, if it exists).
fn qpb_fixture(root: &Path) -> Fx {
    if root.exists() {
        assert!(root.join("QPB_FIXTURE").exists(), "QPB: {root:?} exists and is not ours");
        let q = root.with_extension(format!("old{}", std::process::id()));
        std::fs::rename(root, &q).unwrap();
    }
    let ws = root.join("ws");
    let home = root.join("home");
    let outside = root.join("outside");
    touch(&root.join("QPB_FIXTURE"), "qpb\n");
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
            if !a.is_empty() && s.contains(a.as_str()) {
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
fn fnv8(s: &str) -> String {
    fnv(s)[..8].to_string()
}

fn short(d: &Decision) -> String {
    match d {
        Decision::Allow {
            why: AllowWhy::OwnerChoseAllow,
        } => "U".into(),
        Decision::Allow {
            why: AllowWhy::Bypass { .. },
        } => "B".into(),
        Decision::Allow { why } => format!("allow:{}", format!("{why:?}").chars().take(30).collect::<String>()),
        Decision::Ask { card } => format!("a{}", format!("{:?}", card.tier).trim_start_matches('T')),
        Decision::Deny {
            reason: DenyReason::Excluded,
        } => "X".into(),
        Decision::Deny {
            reason: DenyReason::HardDeny { .. },
        } => "H".into(),
        Decision::Deny {
            reason: DenyReason::TooLargeToCheck { .. },
        } => "L".into(),
        Decision::Deny {
            reason: DenyReason::RefusedInAllow { .. },
        } => "r".into(),
        Decision::Deny {
            reason: DenyReason::BypassRefused { .. },
        } => "b".into(),
        Decision::Deny { reason } => format!("D:{}", format!("{reason:?}").chars().take(24).collect::<String>()),
    }
}

/// One decision: [short code, rank detail, fnv of the whole masked Debug]. Rank detail: for an ask its tier and its
/// reasons (each masked Debug), for a deny the masked Debug of the reason, for an allow the masked Debug of why.
fn enc(d: &Decision, m: &Mask, full: bool) -> Value {
    let det = match d {
        Decision::Allow { why } => json!({"k": "A", "w": m.apply(&format!("{why:?}"))}),
        Decision::Deny { reason } => json!({"k": "D", "r": m.apply(&format!("{reason:?}")), "t": m.apply(&reason.text())}),
        Decision::Ask { card } => json!({
            "k": "Q", "tier": format!("{:?}", card.tier),
            "rs": card.reasons.iter().map(|r| m.apply(&format!("{r:?}"))).collect::<Vec<_>>(),
        }),
    };
    let dbg = m.apply(&format!("{d:?}"));
    let mut v = json!({"c": short(d), "d": det, "h": fnv(&dbg)});
    if full {
        v["full"] = json!(dbg);
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

/// The 12 columns: decide, would_have_been, 5 both-agree views, owner with no view, 4 owner views.
fn columns(a: &Action, st: &State, f: &OwnerInputFacts, m: &Mask, full: bool) -> Vec<Value> {
    let mut c = Vec::with_capacity(12);
    c.push(enc(&decide(a, st, Surface::Console, NOW), m, full));
    let (t, rs) = would_have_been(a, st);
    let w = format!("{t:?} {:?}", rs);
    c.push(json!({"c": format!("W{t:?}"), "d": {"k": "W", "tier": format!("{t:?}"), "rs": rs.iter().map(|r| m.apply(&format!("{r:?}"))).collect::<Vec<_>>()}, "h": fnv(&m.apply(&w))}));
    for (_, v) in views() {
        c.push(enc(&decide_with_mode(a, st, Some(&v), Surface::Console, NOW), m, false));
    }
    c.push(enc(&decide_with_owner_allow(a, st, None, f, Surface::Console, NOW), m, false));
    for (_, o) in owners() {
        c.push(enc(&decide_with_owner_allow(a, st, Some(&o), f, Surface::Console, NOW), m, false));
    }
    c
}

/// The four columns of `t28::cols` (no view, owner StillAsk, owner Allowed, both-agree live_shell).
fn four(a: &Action, st: &State, f: &OwnerInputFacts) -> [Decision; 4] {
    [
        decide_with_owner_allow(a, st, None, f, Surface::Console, NOW),
        with_owner_facts(a, f, st, &owner_still_ask(), Surface::Console),
        with_owner_facts(a, f, st, &owner_terminal(), Surface::Console),
        with_mode(a, st, &live_shell()),
    ]
}

// ------------------------------------------------------------------------------------------------------------------
// The check's own reading of free text (NOT a port of scan B): JSON escapes made blanks per the JSON grammar, then
// words split at whitespace and control characters only, quote characters `'` and `"` dropped from each word. Each
// word carries the character position (1-based, in the FIELD) at which it ends.
// ------------------------------------------------------------------------------------------------------------------

/// The check's reading of a window. `json`: the window is canonical JSON: only the text INSIDE string values is read;
/// a string's boundary quote and everything outside strings is a delimiter; each escape `\X` / `\uXXXX` is a delimiter
/// when `blank` (else kept inside the word as its two or six characters). Not `json` (a web fetch prompt's value, or a
/// URL): the raw characters; for a prompt (`prompt`) a real `"` or `\` is a delimiter too (the prompt is re-encoded as
/// a JSON string before it is read, so they become escapes). Words split at whitespace and control characters; `'`
/// dropped. `punct`: each word further split at the shell punctuation the docs name and the text after each `@` added
/// (the docs' second tier). Each word with the 1-based character position in the field where it ends.
fn oracle(s: &str, json: bool, prompt: bool, blank: bool, punct: bool) -> Vec<(String, usize)> {
    let ch: Vec<char> = s.chars().collect();
    let mut words: Vec<(String, usize)> = Vec::new();
    let mut cur = String::new();
    let mut end = 0usize;
    let mut in_str = !json;
    let mut i = 0;
    let flush = |cur: &mut String, end: usize, words: &mut Vec<(String, usize)>| {
        let w: String = if punct { cur.clone() } else { cur.chars().filter(|c| *c != '\'').collect() };
        if !w.is_empty() {
            words.push((w, end));
        }
        cur.clear();
    };
    while i < ch.len() {
        let c = ch[i];
        if json && !in_str {
            if c == '"' {
                in_str = true;
            }
            flush(&mut cur, end, &mut words);
            i += 1;
            continue;
        }
        if json && c == '"' {
            in_str = false;
            flush(&mut cur, end, &mut words);
            i += 1;
            continue;
        }
        if json && c == '\\' {
            let len = if i + 1 < ch.len() && ch[i + 1] == 'u' {
                let mut j = i + 2;
                while j < ch.len() && j < i + 6 && ch[j].is_ascii_hexdigit() {
                    j += 1;
                }
                j - i
            } else {
                2.min(ch.len() - i)
            };
            if blank {
                flush(&mut cur, end, &mut words);
            } else {
                for k in 0..len {
                    cur.push(ch[i + k]);
                }
                end = i + len;
            }
            i += len;
            continue;
        }
        // a URL window (not JSON, not a prompt): the docs' bounds row reads every window's `\X` as a blank (when `blank`)
        if !json && !prompt && blank && c == '\\' {
            flush(&mut cur, end, &mut words);
            i += 2;
            continue;
        }
        if c.is_whitespace() || c.is_control() || (prompt && (c == '"' || c == '\\')) {
            flush(&mut cur, end, &mut words);
        } else {
            cur.push(c);
            end = i + 1;
        }
        i += 1;
    }
    flush(&mut cur, end, &mut words);
    if !punct {
        return words;
    }
    let mut out = Vec::new();
    for (w, e) in words {
        for qc in ['\'', '"'] {
            for q in w.split(qc).skip(1).step_by(2) {
                if !q.is_empty() {
                    out.push((q.to_string(), e));
                }
            }
        }
        let w: String = w.chars().filter(|c| *c != '"' && *c != '\'').collect();
        for part in w.split(|c: char| ";&|<>()`$={},:".contains(c)) {
            if part.is_empty() {
                continue;
            }
            out.push((part.to_string(), e));
            for (k, _) in part.match_indices('@') {
                out.push((part[k + 1..].to_string(), e));
            }
        }
    }
    out
}

fn oracle_of(kind: &str, w: &str, blank: bool, punct: bool) -> Vec<(String, usize)> {
    match kind {
        "json" | "promptjson" => oracle(w, true, false, blank, punct),
        "prompt" => oracle(w, false, true, blank, punct),
        _ => oracle(w, false, false, blank, punct),
    }
}

/// As `action::lexical_only` (a free-text word as a path, lexically): the check's copy of the 10-line helper, so that
/// the twin decision can add the oracle's words as `InText` targets.
fn as_intext(raw: &str, cwd: &Path, env: &Env) -> Target {
    let expanded = if raw == "~" {
        env.home.clone()
    } else if let Some(r) = raw.strip_prefix("~/") {
        env.home.join(r)
    } else {
        cwd.join(raw)
    };
    let lexical = (raw.len() <= path::MAX_PATH_BYTES).then(|| path::lexical_clean(&expanded));
    Target::Path {
        role: PathRole::InText,
        path: NormPath::Uncertain {
            raw: raw.to_string(),
            lexical,
            why: "free text (not resolved)",
        },
    }
}

/// The free-text windows of a call, as the docs say they are read: each `Raw`, `Query` and `Url` target's first 1 200
/// characters; for a `WebFetch`, its prompt (the value's first 1 200 characters; a non-string prompt as its canonical
/// JSON). Returned with kind ("json", "url", "prompt") and the field text the positions count in.
fn windows_of(a: &Action, h: &HookInput) -> Vec<(String, String, String)> {
    let mut v = Vec::new();
    for t in &a.targets {
        match t {
            Target::Raw { input } => v.push(("json".into(), input.chars().take(1200).collect(), input.clone())),
            Target::Query { text } => v.push(("json".into(), text.chars().take(1200).collect(), text.clone())),
            Target::Url { url, .. } => v.push(("url".into(), url.chars().take(1200).collect(), url.clone())),
            _ => {}
        }
    }
    if h.tool_name == "WebFetch" {
        match h.tool_input.get("prompt") {
            Some(Value::String(s)) => v.push(("prompt".into(), s.chars().take(1200).collect(), s.clone())),
            Some(other) => {
                let mut c = String::new();
                canonical_json(other, &mut c);
                v.push(("promptjson".into(), c.chars().take(1200).collect(), c.clone()));
            }
            None => {}
        }
    }
    v
}


/// The check's copy of `hash::canonical_json` (crate-private there; unchanged at both SHAs): keys sorted by bytes.
fn canonical_json(v: &Value, out: &mut String) {
    match v {
        Value::Null => out.push_str("null"),
        Value::Bool(b) => out.push_str(if *b { "true" } else { "false" }),
        Value::Number(n) => out.push_str(&n.to_string()),
        Value::String(s) => out.push_str(&serde_json::to_string(s).unwrap_or_default()),
        Value::Array(a) => {
            out.push('[');
            for (i, x) in a.iter().enumerate() {
                if i > 0 {
                    out.push(',');
                }
                canonical_json(x, out);
            }
            out.push(']');
        }
        Value::Object(m) => {
            let mut keys: Vec<&String> = m.keys().collect();
            keys.sort();
            out.push('{');
            for (i, k) in keys.iter().enumerate() {
                if i > 0 {
                    out.push(',');
                }
                out.push_str(&serde_json::to_string(k).unwrap_or_default());
                out.push(':');
                canonical_json(&m[*k], out);
            }
            out.push('}');
        }
    }
}

fn comps_nonslash(p: &str) -> (usize, usize) {
    let comps = p.split(['/', '\\']).filter(|c| !c.is_empty()).count();
    let chars = p.chars().filter(|c| *c != '/' && *c != '\\').count();
    (comps, chars)
}

struct Row {
    id: String,
    grp: String,
    tool: String,
    cwd: PathBuf,
    input: Value,
    names: Vec<String>,
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

/// The input a text goes into, per tool (the check's own map; WebFetch puts the text in the prompt, `WebFetchURL` in
/// the URL, `MonitorWS` in `ws.url`).
fn input_for(tool: &str, text: &str) -> (String, Value) {
    match tool {
        "WebSearch" => (tool.into(), json!({ "query": text })),
        "Agent" => (tool.into(), json!({ "prompt": text, "description": "d" })),
        "mcp__github__create_issue" => (tool.into(), json!({ "title": "t", "body": text })),
        "WebFetch" => (tool.into(), json!({ "url": "https://example.com/", "prompt": text })),
        "WebFetchURL" => ("WebFetch".into(), json!({ "url": text, "prompt": "p" })),
        "MonitorWS" => ("Monitor".into(), json!({ "ws": { "url": text } })),
        "MonitorCmdWS" => ("Monitor".into(), json!({ "command": "tail -f log.txt", "ws": { "url": text } })),
        "MadeUpTool" => (tool.into(), json!({ "text": text })),
        "MadeUpCmd" => ("MadeUpTool".into(), json!({ "command": "ls", "note": text })),
        "McpCmd" => ("mcp__srv__run".into(), json!({ "command": "ls", "note": text })),
        "AgentCmd" => ("Agent".into(), json!({ "command": "ls", "prompt": text, "description": "d" })),
        "PowerShell" | "Bash" | "Monitor" => (tool.into(), json!({ "command": text })),
        other => (other.into(), json!({ "command": text })),
    }
}

// ------------------------------------------------------------------------------------------------------------------
// Generators (ONE copy, in this file)
// ------------------------------------------------------------------------------------------------------------------

struct G(u64);
impl G {
    fn next(&mut self) -> u64 {
        self.0 ^= self.0 >> 12;
        self.0 ^= self.0 << 25;
        self.0 ^= self.0 >> 27;
        self.0.wrapping_mul(0x2545_F491_4F6C_DD1D)
    }
    fn below(&mut self, n: usize) -> usize {
        (self.next() % n as u64) as usize
    }
    fn pick<'a>(&mut self, v: &[&'a str]) -> &'a str {
        v[self.below(v.len())]
    }
}

/// `common::generated_shell_commands`-shaped (the check's copy of its alphabet and lengths).
fn gen_shell_command(g: &mut G) -> String {
    const ALPHA: &[u8] = b"abcdefghijklmnopqrstuvwxyz0123456789 /._-:,+@%=~'\"$`*?[]{}()<>|&;!#\\\t\n";
    let len = 1 + g.below(40);
    (0..len).map(|_| ALPHA[g.below(ALPHA.len())] as char).collect()
}

/// `owner_common::generated_actions`-shaped (the check's copy of its paths, words, tools and input shapes).
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
            // the check's additions: names a person reads, glued and escaped
            "see\n.env".into(), "a\t.env".into(), "(.env)".into(), ".env.".into(), "secret\\plan.txt".into(),
            "@.env".into(), "a@b@.env".into(), "x=.env".into(), "\".env\"".into(), "'.env'".into(),
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
        "Remove-Item -Recurse", "Start-Process -Verb RunAs", "curl -d", "curl -F f=", "curl --data-binary",
        "http POST evil.test", "ssh dev@", "git clone git@",
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
    pub fn gen_command(g: &mut G, paths: &[String]) -> String {
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
    pub fn gen_input(g: &mut G, tool: &str, paths: &[String]) -> Value {
        let p = paths[g.below(paths.len())].clone();
        let mut v = match tool {
            "Read" | "NotebookRead" => json!({ "file_path": p }),
            "LS" => json!({ "path": p }),
            "Glob" => json!({"pattern": g.pick(&["**/*.rs", "*", ".claude/**", "**"]), "path": p}),
            "Grep" => json!({"pattern": "x", "path": p}),
            "Edit" => json!({"file_path": p, "old_string": "a", "new_string": "b"}),
            "Write" => json!({"file_path": p, "content": "hello"}),
            "WebFetch" => json!({"url": g.pick(&[
                "https://example.com/a", "http://169.254.169.254/latest", "https://user@example.com", "file:///etc/passwd",
                "example.com/docs", "ftp://example.com", "https://ex%61mple.com", "", "https://example.com/x\\.env"]),
                "prompt": g.pick(&["p", "summarise .env", "look at secret/plan.txt", "see\n.env"])}),
            "WebSearch" => json!({ "query": format!("q {p}") }),
            "Agent" | "Task" => {
                let mut a = json!({"prompt": format!("look at {p}"), "description": "d"});
                if g.below(10) < 4 {
                    a["isolation"] = json!(g.pick(&["local", "remote", "worktree", "weird", ""]));
                }
                if g.below(10) < 2 {
                    a["name"] = json!("mate");
                }
                a
            }
            "Bash" | "PowerShell" | "Monitor" => json!({"command": gen_command(g, paths), "description": "d"}),
            "ExitWorktree" => json!({"action": g.pick(&["keep", "remove"])}),
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

const NAMES: &[&str] = &[".env", "secret/plan.txt", ".ENV", "id_rsa", ".env.local"];

/// Delimiters a name can stand between (item 4's table, the check's own list), as (before, after).
const DELIMS: &[(&str, &str)] = &[
    (" ", " "), ("\n", "\n"), ("\t", "\t"), ("\r", "\r"), ("\u{8}", "\u{8}"), ("\u{c}", "\u{c}"), ("\u{1}", "\u{1}"),
    ("\"", "\""), ("\\", "\\"), ("\u{a0}", "\u{a0}"), ("\u{3000}", "\u{3000}"), ("\u{200b}", "\u{200b}"),
    ("\u{feff}", "\u{feff}"), ("\u{202e}", "\u{202e}"), (" ", "."), (" ", ","), (" ", "?"), (" ", "!"), (" ", "\u{2026}"),
    (" ", ":"), (" ", ";"), ("(", ")"), ("[", "]"), ("{", "}"), ("<", ">"), ("*", "*"), ("**", "**"), ("_", "_"),
    ("~~", "~~"), ("`", "`"), ("'", "'"), ("\u{201c}", "\u{201d}"), ("\u{2018}", "\u{2019}"), ("\u{ab}", "\u{bb}"),
    ("\u{300c}", "\u{300d}"), ("\u{ff08}", "\u{ff09}"), ("\u{2014}", "\u{2014}"), ("#", " "), ("+", " "), ("%", " "),
    ("|", "|"), ("/", " "), ("=", " "), ("@", " "), ("@@", " "), ("a@b@", " "), ("mail@", " "), ("\u{8bf7}\u{8bfb}\u{53d6}", "\u{6587}\u{4ef6}"),
];

/// A filler of ordinary-looking and hostile tokens.
const FILL: &[&str] = &[
    "abc", "Z9", "42", "word", "the", "review", " ", " ", " ", "\n", "\t", "\"", "\\", "'", "=", ":", ",", ";", "@", "/",
    "~", "-o", "{a,b}", "é", "漢", "😀", "\u{200b}", "x/y", "~/q", "k=v", "u@h", "$'x\\x2e'", "(", ")", "[", "]", ".",
    "…", "—", "«", "»", "「", "」", "https://example.com/a?b=c#d", "src/main.rs", "--flag=/a/b",
];

fn filler(g: &mut G, chars: usize) -> String {
    let mut s = String::new();
    while s.chars().count() < chars {
        s.push_str(FILL[g.below(FILL.len())]);
    }
    s
}

/// Distinct one-character words (CJK), blank-separated.
fn distinct_chars(n: usize, base: u32) -> String {
    (0..n).map(|i| char::from_u32(base + i as u32).unwrap().to_string()).collect::<Vec<_>>().join(" ")
}

const FREE_TOOLS: &[&str] = &["WebSearch", "Agent", "mcp__github__create_issue", "MadeUpTool", "WebFetch", "WebFetchURL", "MonitorWS"];
const CMDFIELD_TOOLS: &[&str] = &["MadeUpCmd", "McpCmd", "AgentCmd"];

fn gen_free_text(g: &mut G) -> (String, Vec<String>) {
    let len = 1 + g.below(2000);
    let name = NAMES[g.below(NAMES.len())];
    let (b, a) = DELIMS[g.below(DELIMS.len())];
    let kind = g.below(10);
    let mut text = match kind {
        0 => format!("-{} ", "/a".repeat(200 + g.below(500))), // heavy option word first
        1 => format!("{} ", distinct_chars(300 + g.below(400), 0x4E00 + g.below(2000) as u32)), // distinct one-char words
        2 => (0..(50 + g.below(300))).map(|i| format!("w{i} ")).collect(),
        _ => String::new(),
    };
    let before = g.below(len.max(1));
    text.push_str(&filler(g, before));
    let mut names = Vec::new();
    if g.below(10) < 8 {
        text.push_str(b);
        text.push_str(name);
        text.push_str(a);
        names.push(name.to_string());
    }
    let after = len.saturating_sub(text.chars().count());
    text.push_str(&filler(g, after));
    (text, names)
}

/// A command built to sit near the command bound: n distinct words (pieces) or deep paths (components).
fn gen_bound_command(g: &mut G) -> String {
    match g.below(4) {
        0 => {
            let n = 150 + g.below(21);
            format!("echo {}", (0..n).map(|i| format!("w{i}")).collect::<Vec<_>>().join(" "))
        }
        1 => {
            // about 2 000 to 2 100 path components over a few words
            let total = 2000 + g.below(101);
            let words = 2 + g.below(6);
            let per = total / words;
            let mut v = vec!["cat".to_string()];
            for w in 0..words {
                v.push((0..per).map(|k| format!("d{w}x{k}")).collect::<Vec<_>>().join("/"));
            }
            v.join(" ")
        }
        2 => {
            let n = 150 + g.below(21);
            format!("cat {}", (0..n).map(|i| format!("src/f{i}.rs")).collect::<Vec<_>>().join(" "))
        }
        _ => {
            let n = 140 + g.below(30);
            format!("ls {} .env", (0..n).map(|i| format!("w{i}")).collect::<Vec<_>>().join(" "))
        }
    }
}

fn generated_rows(fx: &Fx, seed: u64, n2: usize, n3: usize, frac: usize) -> Vec<Row> {
    let mut g = G(seed);
    let paths = gen_owner::gen_paths(fx);
    let tools = gen_owner::gen_tools();
    let mut rows = Vec::new();
    let keep = |i: usize| frac <= 1 || i % frac == 0;
    let cwd_pick = |g: &mut G| -> PathBuf {
        match g.below(12) {
            0 => fx.home.clone(),
            1 => fx.outside.clone(),
            2 => fx.ws.join("src"),
            3 => PathBuf::from(""),
            _ => fx.ws.clone(),
        }
    };
    // C2a: generated shell strings through the command tools and the command-field tools
    for i in 0..n2 {
        let cmd = gen_shell_command(&mut g);
        let tool = g.pick(&["Bash", "PowerShell", "Monitor", "MonitorCmd", "MadeUpTool", "mcp__srv__run", "Agent"]);
        let input = match tool {
            "MonitorCmd" => json!({"command": cmd, "ws": {"url": g.pick(&["wss://example.com/x", "wss://example.com/x\\.env", "ws://h/.env"])}}),
            "Agent" => json!({"command": cmd, "prompt": "p", "description": "d"}),
            _ => json!({ "command": cmd }),
        };
        let tool = if tool == "MonitorCmd" { "Monitor" } else { tool };
        let cwd = cwd_pick(&mut g);
        if keep(i) {
            rows.push(Row { id: format!("c2a:{i}"), grp: "C2a".into(), tool: tool.into(), cwd, input, names: vec![], full: false });
        }
    }
    // C2b: owner-shaped hooks
    for i in 0..n2 {
        let tool = tools[g.below(tools.len())].clone();
        let input = gen_owner::gen_input(&mut g, &tool, &paths);
        let cwd = cwd_pick(&mut g);
        if keep(i) {
            rows.push(Row { id: format!("c2b:{i}"), grp: "C2b".into(), tool, cwd, input, names: vec![], full: false });
        }
    }
    // C2c: commands at the command bound, through every command carrier; the carriers with a second text field
    for i in 0..(n2 / 4) {
        let cmd = gen_bound_command(&mut g);
        let (tool, input) = match g.below(8) {
            0 => ("Bash".to_string(), json!({ "command": cmd })),
            1 => ("PowerShell".to_string(), json!({ "command": cmd })),
            2 => ("Monitor".to_string(), json!({ "command": cmd })),
            3 => ("Monitor".to_string(), json!({ "command": cmd, "ws": {"url": "wss://example.com/feed"} })),
            4 => ("MadeUpTool".to_string(), json!({ "command": cmd, "note": format!("see\n.env {}", filler(&mut g, 50)) })),
            5 => ("mcp__srv__run".to_string(), json!({ "command": cmd, "note": distinct_chars(400, 0x4E00) })),
            6 => ("Agent".to_string(), json!({ "command": cmd, "prompt": "late .env", "description": "d" })),
            _ => ("MadeUpTool".to_string(), json!({ "command": cmd })),
        };
        if keep(i) {
            rows.push(Row { id: format!("c2c:{i}"), grp: "C2c".into(), tool, cwd: fx.ws.clone(), input, names: vec![".env".into()], full: false });
        }
    }
    // C3: generated free text through every free-text carrier and the command-field carriers
    for i in 0..n3 {
        let (text, names) = gen_free_text(&mut g);
        let t = if g.below(8) == 0 { CMDFIELD_TOOLS[g.below(CMDFIELD_TOOLS.len())] } else { FREE_TOOLS[g.below(FREE_TOOLS.len())] };
        let (tool, input) = input_for(t, &text);
        if keep(i) {
            rows.push(Row { id: format!("c3:{i}:{t}"), grp: "C3".into(), tool, cwd: fx.ws.clone(), input, names, full: false });
        }
    }
    rows
}

fn envn(k: &str, d: usize) -> usize {
    std::env::var(k).ok().and_then(|v| v.parse().ok()).unwrap_or(d)
}

/// The LONG owner list: the default list plus 32 patterns of the check's own.
fn long_list(fx: &Fx) -> Vec<String> {
    let mut v = patterns::default_exclusions();
    for p in [
        "**/*.pem", "**/*.key", "**/*.p12", "**/*.pfx", "**/id_ed25519*", "**/.npmrc", "**/.pypirc", "**/.netrc",
        "**/secrets/**", "**/private-keys/**", "**/*.sqlite", "**/*.db", "**/dump.sql", "**/backup/**", "**/*.kdbx",
        "**/credentials*", "**/token*.txt", "**/vault/**", "**/.terraform/**", "**/terraform.tfstate*", "**/*.tfvars",
        "**/.docker/config.json", "**/kubeconfig*", "**/.kube/**", "**/service-account*.json", "**/*.jks",
        "**/*.keystore", "**/wallet.dat", "**/.htpasswd", "**/payroll/**", "**/hr/**", "**/secret/**",
    ] {
        v.push(p.to_string());
    }
    let _ = fx;
    v
}

fn states(fx: &Fx) -> Vec<(&'static str, State)> {
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
    vec![
        ("nothing", fx.state()),
        ("default", fx.state_with(patterns::default_exclusions())),
        ("**/.env*", fx.state_with(vec!["**/.env*".to_string()])),
        ("**/.env", fx.state_with(vec!["**/.env".to_string()])),
        ("**/secret/**", fx.state_with(vec!["**/secret/**".to_string()])),
        ("<ws>/secret/**", fx.state_with(vec![format!("{}/secret/**", fx.ws.display())])),
        ("grant-only", grant_only),
        ("sandboxOn+**/.env*", sandbox_on),
        ("long", fx.state_with(long_list(fx))),
        ("listed+**/.env*", {
            let mut st = fx.state_with(vec!["**/.env*".to_string()]);
            for (c, sh) in [("npm test", ShellKind::PowerShell), ("Remove-Item README.md", ShellKind::PowerShell), ("npm test", ShellKind::Bash)] {
                st.add_owner_command(c, &fx.ws, sh, &PosixNormaliser).unwrap();
            }
            st
        }),
    ]
}

fn file_rows(fx: &Fx, file: &str, reps: &[(&str, String)]) -> Vec<Row> {
    let mut rows = Vec::new();
    for (n, l) in std::fs::read_to_string(file).unwrap().lines().enumerate() {
        if l.trim().is_empty() {
            continue;
        }
        let v: Value = serde_json::from_str(l).unwrap_or_else(|e| panic!("QPB rows line {}: {e}", n + 1));
        let tool0 = v["tool"].as_str().unwrap().to_string();
        let (tool, mut input) = if let Some(i) = v.get("input") {
            (tool0.clone(), i.clone())
        } else {
            input_for(&tool0, v["text"].as_str().unwrap())
        };
        subst(&mut input, reps);
        let cwd = match v.get("cwd").and_then(Value::as_str).unwrap_or("ws") {
            "home" => fx.home.clone(),
            "root" => fx.root.clone(),
            "outside" => fx.outside.clone(),
            "src" => fx.ws.join("src"),
            "rel" => PathBuf::from("rel"),
            "empty" => PathBuf::from(""),
            "slash" => PathBuf::from("/"),
            _ => fx.ws.clone(),
        };
        let names = v.get("names").and_then(Value::as_array).map(|a| a.iter().map(|x| x.as_str().unwrap().to_string()).collect()).unwrap_or_default();
        rows.push(Row {
            id: v["id"].as_str().map(String::from).unwrap_or_else(|| format!("row{n}")),
            grp: v.get("grp").and_then(Value::as_str).unwrap_or("C1").to_string(),
            tool,
            cwd,
            input,
            names,
            full: v.get("full").and_then(Value::as_bool).unwrap_or(false),
        });
    }
    rows
}

fn setup() -> (Fx, Mask, Vec<(&'static str, String)>) {
    let fixroot = PathBuf::from(std::env::var("QPB_FIX").expect("QPB_FIX"));
    let fx = qpb_fixture(&fixroot);
    let root = fx.root.to_str().unwrap().to_string();
    let mask = Mask(vec![
        (root.clone(), "<root>".into()),
        (root.to_uppercase(), "<root>".into()),
        (root.to_lowercase(), "<root>".into()),
        (root.replace('/', "\\\\"), "<root>".into()),
        (root.replace('/', "\\"), "<root>".into()),
    ]);
    let reps = vec![
        ("<ws>", fx.ws.to_str().unwrap().to_string()),
        ("<home>", fx.home.to_str().unwrap().to_string()),
        ("<outside>", fx.outside.to_str().unwrap().to_string()),
        ("<root>", root.clone()),
    ];
    (fx, mask, reps)
}

#[test]
fn qpb() {
    let mode = std::env::var("QPB_MODE").unwrap_or_default();
    match mode.as_str() {
        "diff" => run_diff(),
        "time" => run_time(),
        "scanb" => run_scanb(),
        _ => eprintln!("QPB: QPB_MODE not set; nothing to do"),
    }
}

fn run_diff() {
    let out = std::env::var("QPB_OUT").expect("QPB_OUT");
    let seed = u64::from_str_radix(std::env::var("QPB_SEED").expect("QPB_SEED").trim_start_matches("0x"), 16).unwrap();
    let twin_on = std::env::var("QPB_TWIN").ok().as_deref() == Some("1");
    let (fx, mask, reps) = setup();
    let sts = states(&fx);
    let mut rows = Vec::new();
    if let Ok(f) = std::env::var("QPB_ROWS") {
        for part in f.split(',') {
            rows.extend(file_rows(&fx, part, &reps));
        }
    }
    let frac = envn("QPB_FRAC", 1);
    rows.extend(generated_rows(&fx, seed, envn("QPB_N2", 2000), envn("QPB_N3", 3000), frac));
    let mut f = std::io::BufWriter::new(std::fs::File::create(&out).unwrap());
    writeln!(f, "{}", json!({"meta": true, "head": qpb_adapter::HEAD, "seed": format!("{seed:#x}"), "rows": rows.len(),
        "states": sts.iter().map(|s| s.0).collect::<Vec<_>>(), "twin": twin_on,
        "max_free_pieces": action::MAX_FREE_PIECES})).unwrap();
    let mut decisions = 0usize;
    let started = Instant::now();
    for r in &rows {
        let h = fx.hook_in(&r.cwd, &r.tool, r.input.clone());
        let a = classify(&h, HostOs::Posix, &fx.env(), &PosixNormaliser);
        let facts = owner_input_facts(&h);
        let mut canon = String::new();
        canonical_json(&r.input, &mut canon);
        // command scans
        let cmds: Vec<Value> = a.targets.iter().filter_map(|t| match t {
            Target::Command { scan, shell, text, .. } => {
                let mut o = json!({
                    "shell": format!("{shell:?}"), "text": fnv(text),
                    "words": fnv(&format!("{:?}", scan.words)), "exact": fnv(&format!("{:?}", scan.exact)),
                    "pieces": fnv(&format!("{:?}", scan.pieces)), "np": scan.pieces.len(),
                });
                if r.full {
                    o["pieces_full"] = json!(mask.apply(&format!("{:?}", scan.pieces)));
                }
                Some(o)
            }
            _ => None,
        }).collect();
        // free text: windows, scan A pieces (recomputed as classify does), InText list from the action
        let wins = windows_of(&a, &h);
        let mut a_all: Vec<String> = Vec::new();
        for (k, w, _) in &wins {
            if k == "json" || k == "url" {
                a_all.extend(shell::scan_execute(w, ShellKind::Bash).pieces.into_iter().take(1024));
            }
        }
        let intext: Vec<String> = a.targets.iter().filter_map(|t| match t {
            Target::Path { role: PathRole::InText, path: NormPath::Uncertain { raw, .. } } => Some(raw.clone()),
            Target::Path { role: PathRole::InText, path } => Some(format!("{path:?}")),
            _ => None,
        }).collect();
        let b_from_action: Vec<&String> = intext.iter().skip(a_all.len()).collect();
        let b_stats: Vec<(usize, usize)> = b_from_action.iter().map(|p| comps_nonslash(p)).collect();
        // scan B as the head's own function reports it (adapter; base: none)
        let bwins: Vec<(String, bool)> = wins.iter().map(|(k, w, _)| match k.as_str() {
            "prompt" => (serde_json::to_string(w).unwrap(), true),
            _ => (w.clone(), true),
        }).collect();
        let b_ad = qpb_adapter::scan_b(&bwins, &a_all);
        // the oracle: words of each window (whitespace and JSON escapes only), with end positions in the field
        let mut oracle: Vec<(String, usize, String)> = Vec::new();
        for (k, w, _) in &wins {
            for (word, end) in oracle_of(k, w, true, false) {
                oracle.push((word, end, k.clone()));
            }
        }
        let names_in: Vec<Value> = r.names.iter().map(|n| {
            let in_pieces = intext.iter().any(|p| p == n);
            let as_word: Vec<usize> = oracle.iter().filter(|(w, _, _)| w == n).map(|(_, e, _)| *e).collect();
            json!({"name": n, "in_pieces": in_pieces, "word_ends": as_word})
        }).collect();
        let mut st_out = Vec::new();
        for (sn, st) in &sts {
            let cols = columns(&a, st, &facts, &mask, r.full);
            decisions += 12;
            let mut so = json!({"st": sn, "cols": cols});
            if twin_on && !wins.is_empty() {
                // twin: this tree's action plus the oracle's words ending within 1 000 / 1 200 characters of the field
                let mut verdicts = Vec::new();
                for lim in [1000usize, 1200] {
                    let mut t = a.clone();
                    for (w, e, _) in &oracle {
                        if *e <= lim && !w.starts_with('-') {
                            t.targets.push(as_intext(w, &r.cwd, &fx.env()));
                        }
                    }
                    let d = decide(&t, st, Surface::Console, NOW);
                    verdicts.push(short(&d));
                }
                // third: JSON escapes NOT read as blanks; fourth: the docs' second tier (punctuation, after `@`)
                for (blank, punct) in [(false, false), (true, true)] {
                    let mut t = a.clone();
                    for (k, w, _) in &wins {
                        for (word, _) in oracle_of(k, w, blank, punct) {
                            if !word.starts_with('-') {
                                t.targets.push(as_intext(&word, &r.cwd, &fx.env()));
                            }
                        }
                    }
                    verdicts.push(short(&decide(&t, st, Surface::Console, NOW)));
                }
                so["twin"] = json!(verdicts);
            }
            st_out.push(so);
        }
        let mut o = json!({
            "id": r.id, "grp": r.grp, "tool": r.tool, "cwd": mask.apply(r.cwd.to_str().unwrap()),
            "canon": fnv(&mask.apply(&canon)), "clen": canon.chars().count(),
            "oversize": a.oversize, "kind": format!("{:?}", a.kind), "strict": format!("{:?}", a.strict),
            "facts": fnv(&mask.apply(&format!("{facts:?}"))),
            "ntargets": a.targets.len(),
            "cmds": cmds,
            "wins": wins.iter().map(|(k, w, f)| json!({"k": k, "wlen": w.chars().count(), "flen": f.chars().count()})).collect::<Vec<_>>(),
            "a_n": a_all.len(), "a_h": a_all.iter().map(|p| fnv8(p)).collect::<String>(),
            "it_n": intext.len(), "it_h": intext.iter().map(|p| fnv8(p)).collect::<String>(),
            "b_stats": b_stats,
            "b_ad": b_ad.as_ref().map(|(p, w, ov)| json!({"n": p.len(), "work": w, "over": ov,
                "eq_action": p.iter().collect::<Vec<_>>() == b_from_action})),
            "names": names_in,
            "oracle_n": oracle.len(),
            "states": st_out,
        });
        if r.full || r.grp == "C3" || !r.names.is_empty() {
            o["windows"] = json!(wins.iter().map(|(k, w, _)| json!([k, mask.apply(w)])).collect::<Vec<_>>());
            o["oracle"] = json!(oracle.iter().filter(|(w, _, _)| w.chars().count() <= 64).map(|(w, e, k)| json!([mask.apply(w), e, k])).collect::<Vec<_>>());
        }
        if r.full {
            o["intext"] = json!(intext.iter().map(|p| mask.apply(p)).collect::<Vec<_>>());
            o["input"] = json!(mask.apply(&canon));
        }
        writeln!(f, "{o}").unwrap();
    }
    f.flush().unwrap();
    eprintln!("QPB-DIFF head={} seed {seed:#x} rows {} states {} decisions {decisions} twin {twin_on} in {:?}",
        qpb_adapter::HEAD, rows.len(), sts.len(), started.elapsed());
}

fn run_time() {
    let (fx, _mask, reps) = setup();
    let rows = file_rows(&fx, &std::env::var("QPB_ROWS").expect("QPB_ROWS"), &reps);
    let lists = std::env::var("QPB_LIST").unwrap_or_else(|_| "def".into());
    let reps_n = envn("QPB_REPS", 5);
    let spin_ms = envn("QPB_SPIN_MS", 0);
    for list in lists.split(',') {
    let st = match list {
        "env" => fx.state_with(vec!["**/.env*".to_string()]),
        "long" => fx.state_with(long_list(&fx)),
        _ => fx.state_with(patterns::default_exclusions()),
    };
    for idx in std::env::var("QPB_IDX").expect("QPB_IDX").split(',') {
        let i: usize = idx.parse().unwrap();
        let r = &rows[i];
        let h = fx.hook_in(&r.cwd, &r.tool, r.input.clone());
        let mut best = Duration::MAX;
        let mut codes = String::new();
        for _ in 0..reps_n {
            let t = Instant::now();
            let a = classify(&h, HostOs::Posix, &fx.env(), &PosixNormaliser);
            let f = owner_input_facts(&h);
            let d = four(&a, &st, &f);
            if spin_ms > 0 {
                // RED CONTROL of the timing harness only: a fixed extra cost per call
                let s = Instant::now();
                while s.elapsed() < Duration::from_millis(spin_ms as u64) {
                    std::hint::spin_loop();
                }
            }
            let e = t.elapsed();
            codes = d.iter().map(short).collect::<Vec<_>>().join(" ");
            best = best.min(e);
        }
        println!("QPB-TIME {i} {list} {} {codes} | {}", best.as_micros(), r.id);
    }
    }
}

/// Scan B's figures only (classify + the adapter), for the sliding real corpus: one line per row.
fn run_scanb() {
    let (fx, _mask, reps) = setup();
    let rows = file_rows(&fx, &std::env::var("QPB_ROWS").expect("QPB_ROWS"), &reps);
    let mut f = std::io::BufWriter::new(std::fs::File::create(std::env::var("QPB_OUT").expect("QPB_OUT")).unwrap());
    for r in &rows {
        let h = fx.hook_in(&r.cwd, &r.tool, r.input.clone());
        let a = classify(&h, HostOs::Posix, &fx.env(), &PosixNormaliser);
        let wins = windows_of(&a, &h);
        let mut a_all: Vec<String> = Vec::new();
        for (k, w, _) in &wins {
            if k == "json" || k == "url" {
                a_all.extend(shell::scan_execute(w, ShellKind::Bash).pieces.into_iter().take(1024));
            }
        }
        let bwins: Vec<(String, bool)> = wins.iter().map(|(k, w, _)| match k.as_str() {
            "prompt" => (serde_json::to_string(w).unwrap(), true),
            _ => (w.clone(), true),
        }).collect();
        let b = qpb_adapter::scan_b(&bwins, &a_all);
        writeln!(f, "{}", json!({"id": r.id, "oversize": a.oversize, "a_n": a_all.len(),
            "b": b.as_ref().map(|(p, w, o)| json!([p.len(), w, o]))})).unwrap();
    }
    f.flush().unwrap();
    eprintln!("QPB-SCANB rows {}", rows.len());
}
