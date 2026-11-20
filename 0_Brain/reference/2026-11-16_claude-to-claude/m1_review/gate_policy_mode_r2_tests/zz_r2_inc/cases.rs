// QA-POLICY-MODE-R2: the shared probe list (included by zz_r2_absent.rs and zz_r2_probes.rs). Fixture in the checker's
// own scratch folder. Each case: (name, state index, hook JSON, class) where class is
//   "M1"  = must NOT be a mode allow (an unresolved own target or shell cwd),
//   "N3"  = must NOT be a mode allow (a fetch that is not to an http(s) address with a host),
//   "ORD" = an ordinary resolved action: must be decided exactly as at fc7acfc, mode absent and live,
//   "INFO"= reported, no hard expectation (resolved oddities, the stated InText/WebSearch exclusions).
use serde_json::{json, Value};
use std::path::{Path, PathBuf};

const NOW: Timestamp = Timestamp(1_794_873_600);
const S: &str = "sess-r2";

fn touch(p: &Path) {
    std::fs::create_dir_all(p.parent().unwrap()).unwrap();
    if !p.exists() {
        std::fs::write(p, "x\n").unwrap();
    }
}

struct Fx {
    ws: PathBuf,
    home: PathBuf,
}

fn fx() -> Fx {
    let root = PathBuf::from("/private/tmp/claude-501/qpm2/fxr");
    for r in [
        "ws/README.md", "ws/src/main.rs", "ws/.env", "ws/nb.ipynb", "ws/sub/notes.txt",
        "home/.ssh/id_rsa", "home/.coagent/inbox.json", "home/.claude/settings.json", "home/notes/n.txt",
    ] {
        touch(&root.join(r));
    }
    let c = |p: PathBuf| std::fs::canonicalize(p).unwrap();
    Fx { ws: c(root.join("ws")), home: c(root.join("home")) }
}

fn state(f: &Fx, ex: &[&str]) -> State {
    State::new(
        StateConfig {
            session_id: S.into(),
            host: HostOs::Posix,
            env: Env { home: f.home.clone() },
            workspace_roots: vec![f.ws.clone()],
            exclusions: ex.iter().map(|s| s.to_string()).collect(),
            extra_gate_dirs: vec![],
            approval_timeout_secs: 300,
        },
        &PosixNormaliser,
    )
    .unwrap()
}

/// A hook JSON; `cwd: None` leaves the field out.
fn hook(cwd: Option<Value>, tool: &str, input: Value) -> Value {
    let mut h = json!({"session_id": S, "hook_event_name": "PreToolUse", "tool_name": tool, "tool_input": input,
                       "permission_mode": "default"});
    if let Some(c) = cwd {
        h["cwd"] = c;
    }
    h
}

fn short(d: &Decision) -> String {
    match d {
        Decision::Allow { why } => format!("ALLOW {why:?}"),
        Decision::Deny { reason } => format!("DENY {reason:?}"),
        Decision::Ask { card } => format!("ASK {:?} {:?}", card.tier, card.reasons),
    }
}

fn cases(f: &Fx) -> Vec<(String, usize, Value, &'static str)> {
    let w = f.ws.to_str().unwrap().to_string();
    let h = f.home.to_str().unwrap().to_string();
    let ws = || Some(json!(w.clone()));
    let mut v: Vec<(String, usize, Value, &'static str)> = Vec::new();
    // ---- item 4: every path-carrying tool x odd paths (cwd = workspace unless named) ----
    let tools: [(&str, &str, Value); 9] = [
        ("Read", "file_path", json!({})),
        ("NotebookRead", "notebook_path", json!({})),
        ("LS", "path", json!({})),
        ("Glob", "path", json!({"pattern": "**/*"})),
        ("Grep", "path", json!({"pattern": "x"})),
        ("Edit", "file_path", json!({"old_string": "a", "new_string": "b"})),
        ("Write", "file_path", json!({"content": "x"})),
        ("MultiEdit", "file_path", json!({"edits": [{"old_string": "a", "new_string": "b"}]})),
        ("NotebookEdit", "notebook_path", json!({"new_source": "x"})),
    ];
    for (tool, field, base) in tools.iter() {
        let with = |val: Value| {
            let mut i = base.clone();
            i[*field] = val;
            i
        };
        let search = *tool == "Glob" || *tool == "Grep";
        // (label, cwd, path value or None for absent field, class)
        let rows: Vec<(&str, Option<Value>, Option<Value>, &'static str)> = vec![
            ("empty path", ws(), Some(json!("")), "M1"),
            ("path of only spaces", ws(), Some(json!("   ")), "INFO"),
            ("~otheruser/x", ws(), Some(json!("~otheruser/x")), "M1"),
            ("~otheruser", ws(), Some(json!("~otheruser")), "M1"),
            ("NUL inside", ws(), Some(json!("sub/a\u{0}b")), "M1"),
            ("newline inside", ws(), Some(json!("sub/a\nb")), "INFO"),
            ("relative, cwd empty", Some(json!("")), Some(json!("sub/notes.txt")), "M1"),
            ("relative, cwd relative", Some(json!("rel/dir")), Some(json!("sub/notes.txt")), "M1"),
            ("relative, cwd ~otheruser", Some(json!("~otheruser")), Some(json!("sub/notes.txt")), "M1"),
            ("relative, cwd missing", None, Some(json!("sub/notes.txt")), "M1"),
            ("absolute, cwd empty", Some(json!("")), Some(json!(format!("{w}/sub/notes.txt"))), "INFO"),
            // a non-string or absent path: Read/LS/Edit... -> "path field missing or not a string";
            // Glob/Grep fall back to cwd (the classifier's reading of a missing path)
            ("non-string path (number)", ws(), Some(json!(42)), if search { "INFO" } else { "M1" }),
            ("non-string path (null)", ws(), Some(Value::Null), if search { "INFO" } else { "M1" }),
            ("non-string path (array)", ws(), Some(json!(["~/.ssh"])), if search { "INFO" } else { "M1" }),
            ("path field absent", ws(), None, if search { "INFO" } else { "M1" }),
            ("non-string path, cwd home", Some(json!(h.clone())), Some(json!(42)), "M1"),
            ("path field absent, cwd empty", Some(json!("")), None, "M1"),
            ("path field absent, cwd relative", Some(json!("rel")), None, "M1"),
            ("path field absent, cwd ~otheruser", Some(json!("~otheruser")), None, "M1"),
        ];
        for (label, cwd, pv, class) in rows {
            let input = match pv {
                Some(p) => with(p),
                None => base.clone(),
            };
            v.push((format!("{tool}: {label}"), 0, hook(cwd, tool, input), class));
        }
    }
    // Glob whose pattern has no literal part, from an unresolvable cwd; Grep with no path from an unresolvable cwd
    for (cl, cwd) in [("cwd empty", json!("")), ("cwd relative", json!("rel/dir")), ("cwd ~otheruser", json!("~otheruser"))] {
        v.push((format!("Glob pattern **/* (no literal part), no path, {cl}"), 0, hook(Some(cwd.clone()), "Glob", json!({"pattern": "**/*"})), "M1"));
        v.push((format!("Glob pattern *.env, no path, {cl}, **/.env* excluded"), 1, hook(Some(cwd.clone()), "Glob", json!({"pattern": "*.env"})), "M1"));
        v.push((format!("Grep no path, {cl}"), 0, hook(Some(cwd.clone()), "Grep", json!({"pattern": "x"})), "M1"));
        v.push((format!("Grep no path, {cl}, **/.env* excluded"), 1, hook(Some(cwd), "Grep", json!({"pattern": "x"})), "M1"));
    }
    // the first check's four probes again, and a Glob with a pattern literal part from an empty path
    v.push(("check probe: Grep path '' cwd home".into(), 0, hook(Some(json!(h.clone())), "Grep", json!({"pattern": "x", "path": ""})), "M1"));
    v.push(("check probe: Glob path '' cwd home".into(), 0, hook(Some(json!(h.clone())), "Glob", json!({"pattern": "**/*", "path": ""})), "M1"));
    v.push(("check probe: Grep path '' cwd ws, **/.env* excluded".into(), 1, hook(ws(), "Grep", json!({"pattern": "x", "path": ""})), "M1"));
    v.push(("check probe: Grep path ~root".into(), 0, hook(Some(json!(h.clone())), "Grep", json!({"pattern": "x", "path": "~root"})), "M1"));
    v.push(("Glob path '' pattern .ssh/* cwd home".into(), 0, hook(Some(json!(h.clone())), "Glob", json!({"pattern": ".ssh/*", "path": ""})), "M1"));
    // ---- shell: working directory empty / missing / relative / ~otheruser (both shell settings are run) ----
    for (cl, cwd) in [("cwd empty", Some(json!(""))), ("cwd missing", None), ("cwd relative", Some(json!("rel/dir"))),
                      ("cwd ~otheruser", Some(json!("~otheruser"))), ("cwd ~otheruser/x", Some(json!("~otheruser/x"))),
                      ("cwd NUL", Some(json!("/tmp/a\u{0}b"))), ("cwd number", Some(json!(7)))] {
        v.push((format!("Bash npm test, {cl}"), 0, hook(cwd.clone(), "Bash", json!({"command": "npm test"})), "M1"));
        v.push((format!("Bash cat sub/notes.txt, {cl}"), 0, hook(cwd.clone(), "Bash", json!({"command": "cat sub/notes.txt"})), "M1"));
        v.push((format!("PowerShell Get-ChildItem, {cl}"), 0, hook(cwd.clone(), "PowerShell", json!({"command": "Get-ChildItem"})), "M1"));
        v.push((format!("TodoWrite with string command field, {cl}"), 0, hook(cwd, "TodoWrite", json!({"command": "npm test"})), "M1"));
    }
    // ---- consequences of a RELATIVE shell working directory (the Cwd target is normalised against "/") ----
    for (cl, cwd) in [("cwd relative 'rel'", json!("rel")), ("cwd relative '.'", json!(".")), ("cwd relative 'notes'", json!("notes")),
                      ("cwd home (absolute, control)", json!(h.clone()))] {
        for cmd in ["cat .ssh/id_rsa", "grep -r key .", "cat .coagent/inbox.json", "cat ../.ssh/id_rsa", "cp .ssh/id_rsa /tmp/k",
                    "echo x >> .gitconfig", "git config core.hooksPath h", "ls"] {
            v.push((format!("REL Bash {cmd}, {cl}"), 0, hook(Some(cwd.clone()), "Bash", json!({"command": cmd})), if cl.contains("control") { "INFO" } else { "M1" }));
        }
    }
    // ---- for the record: a working directory changed INSIDE shell text (Mentioned: the ruled exclusion) ----
    for cmd in ["cd ~otheruser && grep -r key .", "cd '' && grep -r key .", "cd \"$X\" && grep -r key .", "cd ~ && grep -r key .",
                "grep -r key $(printf ~)"] {
        v.push((format!("CDTEXT Bash {cmd}, cwd ws"), 0, hook(ws(), "Bash", json!({"command": cmd})), "INFO"));
    }
    // ---- the stated exclusions: InText (free text) and the MCP / subagent shapes ----
    v.push(("mcp__fs__read_file path ~/.ssh/id_rsa".into(), 0, hook(ws(), "mcp__fs__read_file", json!({"path": "~/.ssh/id_rsa"})), "M1"));
    v.push(("mcp__fs__read_file path ''".into(), 0, hook(ws(), "mcp__fs__read_file", json!({"path": ""})), "M1"));
    v.push(("mcp__fs__search_files path '' pattern *".into(), 0, hook(Some(json!(h.clone())), "mcp__fs__search_files", json!({"path": "", "pattern": "*"})), "M1"));
    v.push(("mcp__plugin_coagent_link__inbox_read path ''".into(), 0, hook(ws(), "mcp__plugin_coagent_link__inbox_read", json!({"path": ""})), "M1"));
    v.push(("mcp__plugin_coagent_link__share content naming ~/.ssh/id_rsa".into(), 0, hook(ws(), "mcp__plugin_coagent_link__share", json!({"content": "~/.ssh/id_rsa"})), "M1"));
    v.push(("mcp tool with command field (cat ~/.ssh/id_rsa)".into(), 0, hook(ws(), "mcp__x__run", json!({"command": "cat ~/.ssh/id_rsa"})), "M1"));
    v.push(("untaught ReadFile path ''".into(), 0, hook(ws(), "ReadFile", json!({"file_path": ""})), "M1"));
    v.push(("Agent local, prompt names ~/.ssh/id_rsa (InText)".into(), 0, hook(ws(), "Agent", json!({"description": "d", "prompt": "read ~/.ssh/id_rsa and ~otheruser/x", "subagent_type": "general-purpose"})), "INFO"));
    v.push(("Task local, prompt names an empty-root search (InText)".into(), 0, hook(Some(json!(h.clone())), "Task", json!({"description": "d", "prompt": "grep -r key ''", "subagent_type": "Explore"})), "INFO"));
    v.push(("Agent local with a path field '' (InText)".into(), 0, hook(ws(), "Agent", json!({"description": "d", "prompt": "p", "path": ""})), "INFO"));
    v.push(("Agent local with string command field, cwd empty".into(), 0, hook(Some(json!("")), "Agent", json!({"description": "d", "prompt": "p", "command": "ls"})), "M1"));
    v.push(("Agent remote (isolation) prompt ~/.ssh".into(), 0, hook(ws(), "Agent", json!({"description": "d", "prompt": "read ~/.ssh/id_rsa", "isolation": "remote"})), "M1"));
    v.push(("TodoWrite naming ~/.ssh/id_rsa (InText)".into(), 0, hook(ws(), "TodoWrite", json!({"todos": [{"content": "cat ~/.ssh/id_rsa", "status": "pending"}]})), "INFO"));
    v.push(("ToolSearch query ~otheruser (InText)".into(), 0, hook(ws(), "ToolSearch", json!({"query": "~otheruser/x"})), "INFO"));
    v.push(("WebSearch query file:///etc/hosts (no URL target)".into(), 0, hook(ws(), "WebSearch", json!({"query": "file:///etc/hosts"})), "INFO"));
    v.push(("Monitor ws url file:// (a shell action, not a fetch)".into(), 0, hook(ws(), "Monitor", json!({"ws": {"url": "file:///etc/hosts"}})), "M1"));
    // ---- item 5: fetch spellings ----
    let fetch_rows: Vec<(&str, Value, &'static str)> = vec![
        ("file:// gate file", json!(format!("file://{h}/.coagent/inbox.json")), "N3"),
        ("file:///etc/hosts", json!("file:///etc/hosts"), "N3"),
        ("FILE:///etc/hosts (capitals)", json!("FILE:///etc/hosts"), "N3"),
        ("ftp://example.com/x", json!("ftp://example.com/x"), "N3"),
        ("data:text/plain,hi", json!("data:text/plain,hi"), "N3"),
        ("javascript:alert(1)", json!("javascript:alert(1)"), "N3"),
        ("no scheme example.com/docs", json!("example.com/docs"), "N3"),
        ("scheme-relative //example.com/x", json!("//example.com/x"), "N3"),
        ("https:example.com (no slashes)", json!("https:example.com"), "N3"),
        ("https:/example.com (one slash)", json!("https:/example.com"), "N3"),
        ("empty URL", json!(""), "N3"),
        ("https:// (no host)", json!("https://"), "N3"),
        ("https://:443/ (port, no host)", json!("https://:443/"), "N3"),
        ("https://user@example.com/ (user-info)", json!("https://user@example.com/"), "N3"),
        ("https://user:pw@example.com/ (user-info)", json!("https://user:pw@example.com/"), "N3"),
        ("https://[::1]/ (bracketed IP literal)", json!("https://[::1]/"), "N3"),
        ("https://.../ (host of only dots)", json!("https://.../"), "N3"),
        ("https://./x (host one dot)", json!("https://./x"), "N3"),
        ("https://exa mple.com/ (space in host)", json!("https://exa mple.com/"), "N3"),
        ("https://example.com/a b (space in path)", json!("https://example.com/a b"), "N3"),
        ("https://example.com/\\t tab", json!("https://example.com/\tx"), "N3"),
        ("https://example.com\\\\@evil/ (backslash)", json!("https://example.com\\@evil.com/"), "N3"),
        ("https://exa%6dple.com/ (percent in host)", json!("https://exa%6dple.com/"), "N3"),
        ("https://bücher.example/ (non-ASCII host)", json!("https://bücher.example/"), "N3"),
        ("non-string URL (number)", json!(42), "N3"),
        ("non-string URL (null)", Value::Null, "N3"),
        ("ws:// websocket", json!("ws://example.com/"), "N3"),
        ("HTTPS://EXAMPLE.COM/X (capitals)", json!("HTTPS://EXAMPLE.COM/X"), "ORD"),
        ("http://127.0.0.1/ (bare IP)", json!("http://127.0.0.1/"), "ORD"),
        ("http://169.254.169.254/latest (bare IP, metadata)", json!("http://169.254.169.254/latest"), "INFO"),
        ("http://localhost:3000/ (port)", json!("http://localhost:3000/"), "ORD"),
        ("https://example.com:8443/x (port)", json!("https://example.com:8443/x"), "ORD"),
        ("https://example.com./x (trailing dot)", json!("https://example.com./x"), "ORD"),
        ("https://docs.rs/serde", json!("https://docs.rs/serde"), "ORD"),
        ("http://example.com/", json!("http://example.com/"), "ORD"),
        ("https://example.com", json!("https://example.com"), "ORD"),
        ("https://example.com/a%20b?q=1&r=%C3%A9#frag", json!("https://example.com/a%20b?q=1&r=%C3%A9#frag"), "ORD"),
        ("https://sub.example.co.uk/a/b/c.html", json!("https://sub.example.co.uk/a/b/c.html"), "ORD"),
        ("https://example.com/caf\u{e9} (non-ASCII path)", json!("https://example.com/caf\u{e9}"), "ORD"),
        ("https://xn--bcher-kva.example/ (punycode)", json!("https://xn--bcher-kva.example/"), "ORD"),
        ("https://github.com/o/r/blob/main/README.md", json!("https://github.com/o/r/blob/main/README.md"), "ORD"),
        ("https://example.com/search?q=a+b", json!("https://example.com/search?q=a+b"), "ORD"),
        ("https://example.com/@user (at sign in path)", json!("https://example.com/@user"), "ORD"),
    ];
    for (label, url, class) in fetch_rows {
        v.push((format!("WebFetch {label}"), 0, hook(ws(), "WebFetch", json!({"url": url, "prompt": "p"})), class));
    }
    v.push(("WebFetch url field absent".into(), 0, hook(ws(), "WebFetch", json!({"prompt": "p"})), "N3"));
    // ---- item 4, other direction: ordinary resolved actions inside the workspace ----
    let ord: Vec<(&str, usize, &str, Value)> = vec![
        ("Read abs README.md", 0, "Read", json!({"file_path": format!("{w}/README.md")})),
        ("Read relative src/main.rs", 0, "Read", json!({"file_path": "src/main.rs"})),
        ("Read ws/../ws/README.md", 0, "Read", json!({"file_path": format!("{w}/../ws/README.md")})),
        ("Read missing file in ws", 0, "Read", json!({"file_path": format!("{w}/nope.txt")})),
        ("NotebookRead nb.ipynb", 0, "NotebookRead", json!({"notebook_path": format!("{w}/nb.ipynb")})),
        ("LS src", 0, "LS", json!({"path": format!("{w}/src")})),
        ("LS ws", 0, "LS", json!({"path": w.clone()})),
        ("Glob **/*.rs path ws", 0, "Glob", json!({"pattern": "**/*.rs", "path": w.clone()})),
        ("Glob src/*.rs no path", 0, "Glob", json!({"pattern": "src/*.rs"})),
        ("Grep fn path src", 0, "Grep", json!({"pattern": "fn", "path": format!("{w}/src")})),
        ("Grep no path (cwd ws)", 0, "Grep", json!({"pattern": "fn"})),
        ("Grep no path, **/.env* excluded (refused as at fc7acfc)", 1, "Grep", json!({"pattern": "fn"})),
        ("Grep path src, **/.env* excluded", 1, "Grep", json!({"pattern": "fn", "path": format!("{w}/src")})),
        ("Edit src/main.rs", 0, "Edit", json!({"file_path": format!("{w}/src/main.rs"), "old_string": "x", "new_string": "y"})),
        ("Write new src/new.rs", 0, "Write", json!({"file_path": format!("{w}/src/new.rs"), "content": "x"})),
        ("Write docs/x.md (missing parent)", 0, "Write", json!({"file_path": format!("{w}/docs/x.md"), "content": "x"})),
        ("MultiEdit README.md", 0, "MultiEdit", json!({"file_path": format!("{w}/README.md"), "edits": []})),
        ("NotebookEdit nb.ipynb", 0, "NotebookEdit", json!({"notebook_path": format!("{w}/nb.ipynb"), "new_source": "x"})),
        ("Bash cargo test", 0, "Bash", json!({"command": "cargo test"})),
        ("Bash ls src", 0, "Bash", json!({"command": "ls src"})),
        ("Bash git status", 0, "Bash", json!({"command": "git status"})),
        ("Bash cat sub/notes.txt", 0, "Bash", json!({"command": "cat sub/notes.txt"})),
        ("TodoWrite plain", 0, "TodoWrite", json!({"todos": [{"content": "t", "status": "pending"}]})),
    ];
    for (label, st, tool, input) in ord {
        v.push((format!("ORD {label}"), st, hook(ws(), tool, input), "ORD"));
    }
    v.push(("ORD Bash cargo test, cwd ws/src".into(), 0, hook(Some(json!(format!("{w}/src"))), "Bash", json!({"command": "cargo test"})), "ORD"));
    v.push(("ORD Read with cwd ~ (resolves to home)".into(), 0, hook(Some(json!("~")), "Read", json!({"file_path": format!("{w}/README.md")})), "ORD"));
    v
}
