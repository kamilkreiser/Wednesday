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
        // QA-SCANNER-NOTES: the head's six new planted lines, given to MAIN's hits
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
