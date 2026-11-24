//! Property 7: pure and alone. The crate declares no dependency of any kind, and its source names
//! no file, environment, network, process or clock access, no random source and no randomly seeded
//! map. Method of `coagent-policy/tests/t11_determinism.rs` (read the source, look for names),
//! but stricter: comments count too, and every `std::{...}` group import is refused so a name
//! cannot hide in one.
//!
//! Planted control: the same check run on a copy of the source with one `std::env::var` line added
//! must find it. `COAGENT_SCANNER_SRC_DIR`, when set, replaces the source directory read (used by
//! `scripts/red-controls-scanner.sh` to show this test red on a planted scratch copy).
use std::path::{Path, PathBuf};

const FORBIDDEN: &[&str] = &[
    "std::fs",
    "std::env",
    "std::net",
    "std::process",
    "std::time",
    "std::{",
    "HashMap",
    "HashSet",
    "RandomState",
    "SystemTime",
    "Instant",
    "env!(",
    "option_env!",
    "include_str!",
    "include_bytes!",
    "extern crate",
    "getrandom",
    "thread_rng",
    // ADDENDUM 2 N3
    "include!",
    "#[path",
    "static mut",
    "use std as",
    "use core as",
    "use alloc as",
    "println!",
    "print!",
    "eprintln!",
    "eprint!",
    "dbg!",
];

/// ADDENDUM 2 N3: every `std::`, `core::` or `alloc::` path is refused unless it starts with an
/// entry of this list. Today the list is empty: `src/` uses the prelude only.
const ALLOWED_PATHS: &[&str] = &[];

fn rs_files(dir: &Path, out: &mut Vec<PathBuf>) {
    for e in std::fs::read_dir(dir).expect("read the source directory") {
        let p = e.expect("a directory entry").path();
        if p.is_dir() {
            rs_files(&p, out);
        } else if p.extension().is_some_and(|x| x == "rs") {
            out.push(p);
        }
    }
}

/// Every forbidden name in one source text, as `line: name`.
fn hits(text: &str) -> Vec<String> {
    let mut out = vec![];
    for (i, line) in text.lines().enumerate() {
        for tok in FORBIDDEN {
            if line.contains(tok) {
                out.push(format!("{}: {tok}", i + 1));
            }
        }
        // any `std::` / `core::` / `alloc::` path outside the allow-list
        let ident = |c: u8| c.is_ascii_alphanumeric() || c == b'_';
        for root in ["std::", "core::", "alloc::"] {
            let mut from = 0;
            while let Some(p) = line[from..].find(root).map(|p| p + from) {
                let starts_word = p == 0 || !ident(line.as_bytes()[p - 1]);
                if starts_word && !ALLOWED_PATHS.iter().any(|a| line[p..].starts_with(a)) {
                    out.push(format!("{}: {root} path", i + 1));
                }
                from = p + root.len();
            }
        }
        // `rand` as a whole identifier (not inside `random`, `operand`, ...)
        let b = line.as_bytes();
        let ident = |c: u8| c.is_ascii_alphanumeric() || c == b'_';
        let mut from = 0;
        while let Some(p) = line[from..].find("rand").map(|p| p + from) {
            let before = p == 0 || !ident(b[p - 1]);
            let after = p + 4 >= b.len() || !ident(b[p + 4]);
            if before && after {
                out.push(format!("{}: rand", i + 1));
            }
            from = p + 4;
        }
    }
    out.extend(token_hits(text));
    out
}

/// SCANNER-NOTES item 4 (N-R6): a token-level look over the WHOLE text, whitespace collapsed, so an
/// alias of `std`, `core` or `alloc` is found in any spelling (`use ::std as s;`, `use  std as s;`,
/// `use {std as s};`, an alias split across lines), and any path that starts `::std`, `::core` or
/// `::alloc`. Tokens: identifiers, `::`, and every other non-blank character on its own.
fn token_hits(text: &str) -> Vec<String> {
    let b = text.as_bytes();
    let ident = |c: u8| c.is_ascii_alphanumeric() || c == b'_';
    let mut toks: Vec<(usize, &str)> = vec![];
    let (mut i, mut line) = (0, 1);
    while i < b.len() {
        let c = b[i];
        if c == b'\n' {
            line += 1;
            i += 1;
        } else if c.is_ascii_whitespace() {
            i += 1;
        } else if ident(c) {
            let s = i;
            while i < b.len() && ident(b[i]) {
                i += 1;
            }
            toks.push((line, &text[s..i]));
        } else if c == b':' && b.get(i + 1) == Some(&b':') {
            toks.push((line, "::"));
            i += 2;
        } else {
            let n = text[i..].chars().next().map_or(1, char::len_utf8);
            toks.push((line, &text[i..i + n]));
            i += n;
        }
    }
    let roots = ["std", "core", "alloc"];
    let mut out = vec![];
    for k in 0..toks.len() {
        let (l, t) = toks[k];
        if t == "as" && k > 0 && roots.contains(&toks[k - 1].1) {
            out.push(format!("{l}: {} alias", toks[k - 1].1));
        }
        let leading = k == 0 || !toks[k - 1].1.bytes().all(ident);
        if t == "::" && leading && toks.get(k + 1).is_some_and(|n| roots.contains(&n.1)) {
            out.push(format!("{l}: ::{} path", toks[k + 1].1));
        }
    }
    out
}

#[test]
fn the_scanner_reads_nothing() {
    let crate_dir = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    // no dependency of any kind
    let manifest = std::fs::read_to_string(crate_dir.join("Cargo.toml")).expect("read Cargo.toml");
    let deps: Vec<&str> = manifest
        .lines()
        .filter(|l| l.trim_start().starts_with('[') && l.contains("dependencies"))
        .collect();
    assert!(
        deps.is_empty(),
        "t07: the scanner's Cargo.toml declares dependencies: {deps:?}"
    );

    let src = std::env::var_os("COAGENT_SCANNER_SRC_DIR")
        .map(PathBuf::from)
        .unwrap_or_else(|| crate_dir.join("src"));
    let mut files = vec![];
    rs_files(&src, &mut files);
    files.sort();
    assert!(
        files.len() >= 2,
        "control: the source files were found ({})",
        files.len()
    );

    // planted control: a copy of the first file with one environment read is caught
    let first = std::fs::read_to_string(&files[0]).expect("read a source file");
    assert!(
        !hits(&format!(
            "{first}\nfn planted() -> bool {{ std::env::var(\"X\").is_ok() }}\n"
        ))
        .is_empty(),
        "control: the planted std::env::var line was not found"
    );

    // ADDENDUM 2 N3: the new rules each find a planted line too
    for planted in [
        "use std as s;",
        "fn f() { core::mem::drop(1) }",
        "fn f() -> alloc::string::String { todo!() }",
        "include!(\"x.rs\");",
        "#[path = \"x.rs\"] mod x;",
        "static mut N: u8 = 0;",
        "fn f() { println!(\"x\") }",
        "fn f() { dbg!(1); }",
        // SCANNER-NOTES item 4 (N-R6): aliases in any spelling, a leading `::`
        "use ::std as s;",
        "use  std as s;",
        "use {std as s};",
        "use std\n    as s;\nfn f() -> bool { s::env::var(\"X\").is_ok() }",
        "use core\n    as c;",
        "fn f() -> bool { ::std::env::var(\"X\").is_ok() }",
    ] {
        assert!(
            !hits(&format!("{first}\n{planted}\n")).is_empty(),
            "control: the planted line {planted:?} was not found"
        );
    }

    let mut found = vec![];
    for f in &files {
        let text = std::fs::read_to_string(f).expect("read a source file");
        for h in hits(&text) {
            found.push(format!(
                "{}:{h}",
                f.file_name().unwrap_or_default().to_string_lossy()
            ));
        }
    }
    assert!(
        found.is_empty(),
        "t07: the scanner source names a forbidden item: {found:?}"
    );
}

/// QA-SCANNER-NOTES: the head's `hits` on spellings beyond the planted ones (made up).
#[test]
fn qa_t07_probe_spellings() {
    for planted in [
        "use std /* c */ as s;",
        "use std // c\n    as s;",
        "fn f() -> bool { std :: env :: var(\"X\").is_ok() }",
        "fn f() -> bool { std::env ::var(\"X\").is_ok() }",
        "use std::{self as s};",
        "use r#std as s;",
        "extern crate std as s;",
        "use ::{std as s};",
        "pub use std as s;",
        "use core::{self};",
        "fn f() -> bool { ::core::mem::size_of::<u8>() == 1 }",
        "type S = ::alloc::string::String;",
        "use std::{env};",
        "use self::std as s;",
        "use crate::x as std;",
        "macro_rules! m { () => { std } }",
        "use\tstd\tas\ts;",
    ] {
        println!("PROBE {:<60} -> {:?}", format!("{planted:?}"), hits(&format!("//! x\n{planted}\n")));
    }
}
