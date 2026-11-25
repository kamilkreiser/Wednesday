// QA-POLICY-NEXT item 5/7 scratch: the head depends_on_policy (verbatim), the 74dc861 one (verbatim), the base closure.
#![allow(dead_code)]
fn dep_head(manifest: &str) -> bool {
    const NAME: &str = "coagent-policy";
    let unquote = |k: &str| -> String {
        let k = k.trim();
        for q in ['"', '\''] {
            if k.len() >= 2 && k.starts_with(q) && k.ends_with(q) {
                return k[1..k.len() - 1].to_string();
            }
        }
        k.to_string()
    };
    // a table header's keys, split at dots outside quotes
    let keys = |h: &str| -> Vec<String> {
        let (mut out, mut cur, mut quote) = (Vec::new(), String::new(), None::<char>);
        for c in h.chars() {
            match (quote, c) {
                (None, '.') => out.push(unquote(&std::mem::take(&mut cur))),
                (None, '"' | '\'') => {
                    quote = Some(c);
                    cur.push(c);
                }
                (Some(q), _) if c == q => {
                    quote = None;
                    cur.push(c);
                }
                _ => cur.push(c),
            }
        }
        out.push(unquote(&cur));
        out
    };
    let dep_table = |k: &str| {
        matches!(
            k,
            "dependencies"
                | "dev-dependencies"
                | "build-dependencies"
                | "dev_dependencies"
                | "build_dependencies"
        )
    };
    let after_blanks_is = |rest: &str, c: char| rest.trim_start().starts_with(c);
    manifest.lines().any(|l| {
        let t = l.trim_start();
        // the old disjunct, unchanged
        if t.starts_with(NAME) {
            return true;
        }
        if t.starts_with('#') {
            return false;
        }
        // a table header
        if let Some(h) = t.strip_prefix('[').and_then(|h| h.split(']').next()) {
            if !t.starts_with("[[") {
                let k = keys(h);
                let n = k.len();
                if n >= 2
                    && k[n - 1] == NAME
                    && dep_table(&k[n - 2])
                    && (n == 2 || (n == 4 && k[0] == "target"))
                {
                    return true;
                }
            }
        }
        // a quoted key
        for q in ["\"coagent-policy\"", "'coagent-policy'"] {
            if let Some(rest) = t.strip_prefix(q) {
                if after_blanks_is(rest, '=') || after_blanks_is(rest, '.') {
                    return true;
                }
            }
        }
        // package = "coagent-policy"
        let mut from = 0;
        while let Some(i) = t[from..].find("package") {
            let at = from + i;
            let before_ok = t[..at]
                .chars()
                .last()
                .is_none_or(|c| !(c.is_ascii_alphanumeric() || c == '_' || c == '-'));
            let rest = t[at + "package".len()..].trim_start();
            if before_ok {
                if let Some(v) = rest.strip_prefix('=') {
                    let v = v.trim_start();
                    if v.starts_with("\"coagent-policy\"") || v.starts_with("'coagent-policy'") {
                        return true;
                    }
                }
            }
            from = at + "package".len();
        }
        false
    })
}

fn dep_mid(manifest: &str) -> bool {
    const NAME: &str = "coagent-policy";
    let unquote = |k: &str| -> String {
        let k = k.trim();
        for q in ['"', '\''] {
            if k.len() >= 2 && k.starts_with(q) && k.ends_with(q) {
                return k[1..k.len() - 1].to_string();
            }
        }
        k.to_string()
    };
    // a table header's keys, split at dots outside quotes
    let keys = |h: &str| -> Vec<String> {
        let (mut out, mut cur, mut quote) = (Vec::new(), String::new(), None::<char>);
        for c in h.chars() {
            match (quote, c) {
                (None, '.') => out.push(unquote(&std::mem::take(&mut cur))),
                (None, '"' | '\'') => {
                    quote = Some(c);
                    cur.push(c);
                }
                (Some(q), _) if c == q => {
                    quote = None;
                    cur.push(c);
                }
                _ => cur.push(c),
            }
        }
        out.push(unquote(&cur));
        out
    };
    let dep_table = |k: &str| {
        matches!(
            k,
            "dependencies"
                | "dev-dependencies"
                | "build-dependencies"
                | "dev_dependencies"
                | "build_dependencies"
        )
    };
    let after_blanks_is = |rest: &str, c: char| rest.trim_start().starts_with(c);
    manifest.lines().any(|l| {
        let t = l.trim_start();
        // the old disjunct, unchanged
        if t.starts_with(NAME) {
            return true;
        }
        if t.starts_with('#') {
            return false;
        }
        // a table header
        if let Some(h) = t.strip_prefix('[').and_then(|h| h.split(']').next()) {
            if !t.starts_with("[[") {
                let k = keys(h);
                let n = k.len();
                if n >= 2 && k[n - 1] == NAME && dep_table(&k[n - 2]) {
                    if n == 2 || (n == 4 && k[0] == "target") {
                        return true;
                    }
                }
            }
        }
        // a quoted key
        for q in ["\"coagent-policy\"", "'coagent-policy'"] {
            if let Some(rest) = t.strip_prefix(q) {
                if after_blanks_is(rest, '=') || after_blanks_is(rest, '.') {
                    return true;
                }
            }
        }
        // package = "coagent-policy"
        let mut from = 0;
        while let Some(i) = t[from..].find("package") {
            let at = from + i;
            let before_ok = t[..at]
                .chars()
                .last()
                .is_none_or(|c| !(c.is_ascii_alphanumeric() || c == '_' || c == '-'));
            let rest = t[at + "package".len()..].trim_start();
            if before_ok {
                if let Some(v) = rest.strip_prefix('=') {
                    let v = v.trim_start();
                    if v.starts_with("\"coagent-policy\"") || v.starts_with("'coagent-policy'") {
                        return true;
                    }
                }
            }
            from = at + "package".len();
        }
        false
    })
}

fn dep_base(text: &str) -> bool { text.lines().any(|l| l.trim_start().starts_with("coagent-policy")) }
fn main() {
    let cases: &[(&str, &str, &str)] = &[
        ("P1-plain", "pos", r####"[dependencies]
coagent-policy = { path = "../coagent-policy" }"####),
        ("P2-table", "pos", r####"[dependencies.coagent-policy]
path = "../coagent-policy""####),
        ("P3-dev-table", "pos", r####"[dev-dependencies.coagent-policy]
path = "../coagent-policy""####),
        ("P4-build-table", "pos", r####"[build-dependencies.coagent-policy]
path = "../coagent-policy""####),
        ("P5-target-cfg-table", "pos", r####"[target.'cfg(windows)'.dependencies.coagent-policy]
path = "../coagent-policy""####),
        ("P6-target-triple-dev-quoted", "pos", r####"[target.x86_64-pc-windows-msvc.dev-dependencies."coagent-policy"]
path = "../coagent-policy""####),
        ("P7-table-quoted", "pos", r####"[dependencies."coagent-policy"]
path = "../coagent-policy""####),
        ("P8-quoted-key", "pos", r####"[dependencies]
"coagent-policy" = { path = "../coagent-policy" }"####),
        ("P9-renamed", "pos", r####"[dependencies]
policy = { package = "coagent-policy", path = "../coagent-policy" }"####),
        ("P10-renamed-tight", "pos", r####"[dependencies]
policy={package="coagent-policy",path="../coagent-policy"}"####),
        ("E1-inline-blanks-comment", "pos", r####"[dependencies]
policy = {   package   =   "coagent-policy" ,  path = "../coagent-policy" }   # renamed"####),
        ("E2-package-key-quoted", "pos", r####"[dependencies]
policy = { "package" = "coagent-policy", path = "../coagent-policy" }"####),
        ("E2b-package-key-single-quoted", "pos", r####"[dependencies]
policy = { 'package' = "coagent-policy", path = "../coagent-policy" }"####),
        ("E3-package-own-line", "pos", r####"[dependencies.p]
package = "coagent-policy"
path = "../coagent-policy""####),
        ("E3b-package-own-line-indented-comment", "pos", r####"[dependencies.p]
  package='coagent-policy' # c
path = "../coagent-policy""####),
        ("E3c-package-multiline-string", "pos", r####"[dependencies.p]
package = """coagent-policy"""
path = "../coagent-policy""####),
        ("E3d-dotted-package", "pos", r####"[dependencies]
p.package = "coagent-policy"
p.path = "../coagent-policy""####),
        ("E4-workspace-dotted", "pos-ws", r####"[dependencies]
coagent-policy.workspace = true"####),
        ("E5-workspace-inline", "pos-ws", r####"[dependencies]
coagent-policy = { workspace = true }"####),
        ("E6-target-cfg-dots-brackets", "pos", r####"[target.'cfg(target_feature = "a.b[c]")'.dependencies.coagent-policy]
path = "../coagent-policy""####),
        ("E6b-target-cfg-basic-escaped", "pos", r####"[target."cfg(target_os = \"x.y\")".dependencies.coagent-policy]
path = "../coagent-policy""####),
        ("E6c-target-cfg-dots", "pos", r####"[target.'cfg(target_env = "gnu.x")'.dependencies.coagent-policy]
path = "../coagent-policy""####),
        ("E6d-target-cfg-any", "pos", r####"[target.'cfg(any(unix, windows))'.build-dependencies.coagent-policy]
path = "../coagent-policy""####),
        ("E7-top-dotted", "pos-top", r####"dependencies.coagent-policy.path = "../coagent-policy""####),
        ("E8-top-dotted-target", "pos-top", r####"target.'cfg(unix)'.dependencies.coagent-policy = { path = "../coagent-policy" }"####),
        ("E8b-top-dotted-renamed", "pos-top", r####"dependencies.p = { package = "coagent-policy", path = "../coagent-policy" }"####),
        ("E9-header-blanks", "pos", r####"[ dependencies . "coagent-policy" ]
path = "../coagent-policy""####),
        ("E10-header-comment", "pos", r####"[dependencies.coagent-policy] # the policy crate
path = "../coagent-policy""####),
        ("E11-workspace-deps-table", "ws-root", r####"[workspace.dependencies.coagent-policy]
path = "../coagent-policy""####),
        ("E12-target-renamed-inline", "pos", r####"[target.'cfg(unix)'.dependencies]
p = { package = "coagent-policy", path = "../coagent-policy" }"####),
        ("E13-underscore-table", "pos", r####"[dev_dependencies.coagent-policy]
path = "../coagent-policy""####),
        ("E14-dotted-path-key", "pos", r####"[dependencies]
coagent-policy.path = "../coagent-policy""####),
        ("N1-root-member-line", "neg", r####"    "crates/coagent-policy","####),
        ("N2-hook-comment", "neg", r####"# Deliberately NOT depending on coagent-daemon, coagent-crypto or coagent-policy (the same shape as"####),
        ("N3-package-x", "neg", r####"[package]
name = "coagent-policy-x"
version = "0.0.0"
edition = "2021""####),
        ("N4-feature-list", "neg", r####"[features]
x = ["coagent-policy/x"]"####),
        ("N4b-feature-list-multiline", "neg", r####"[features]
x = [
  "coagent-policy/x",
]"####),
        ("N5-description-literal", "neg", r####"[package]
name = "n5"
version = "0.0.0"
edition = "2021"
description = 'package = "coagent-policy"'"####),
        ("N5b-description-basic", "neg", r####"[package]
name = "n5b"
version = "0.0.0"
edition = "2021"
description = "package = \"coagent-policy\"""####),
        ("N6-extra-crate", "neg", r####"[dependencies]
coagent-policy-extra = { path = "../coagent-policy-extra" }"####),
        ("N7-trailing-comment", "neg", r####"[dependencies]
serde = "1" # package = "coagent-policy""####),
        ("N8-patch-section", "neg", r####"[patch.crates-io]
coagent-policy = { path = "../coagent-policy" }"####),
    ];
    for (i, k, t) in cases { println!("CASE\t{i}\t{k}\tbase={}\thead={}\tmid={}", dep_base(t), dep_head(t), dep_mid(t)); }
    for p in std::env::args().skip(1) { let t = std::fs::read_to_string(&p).unwrap(); println!("FILE\t{p}\tbase={}\thead={}\tmid={}", dep_base(&t), dep_head(&t), dep_mid(&t)); }
}
