//! QA-SCANNER-NEXT (independent check), item 4: base `t07` `hits` against head `t07` `hits`
//! (copies from git, only `fn hits` made `pub` and the test renamed), on the SCANNER-NOTES check's
//! 17 probe spellings and my own, on the real `src/`, and on hostile texts for `comments_blanked`.
#[path = "qa_t07_base.rs"]
mod tb;
#[path = "qa_t07_head.rs"]
mod th;
use std::time::Instant;

fn sub_multiset(a: &[String], b: &[String]) -> Vec<String> {
    // the hits of a that b does not hold (as a multiset)
    let mut rest: Vec<String> = b.to_vec();
    let mut missing = vec![];
    for x in a { if let Some(p) = rest.iter().position(|y| y == x) { rest.remove(p); } else { missing.push(x.clone()); } }
    missing
}

const OLD17: &[&str] = &[
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
];

/// (spelling, a forbidden item really named in code?) Mine. `true` = a real use of std/core/alloc that
/// the test should refuse; `false` = text only (inside a literal) or no root, recorded either way.
const MINE: &[(&str, bool)] = &[
    ("use std /* a /* b */ c */ as s;", true),                         // nested block comment
    ("use std\n/* c */\nas s;", true),                                 // comment on its own line
    ("use core /* c */ as c;", true),
    ("use alloc // c\n as a;", true),
    ("use ::std /* c */ as s;", true),
    ("use { std /* c */ as s };", true),
    ("use r#std /* c */ as s;", true),
    ("use std/**/as s;", true),                                        // empty comment glued
    ("fn f() -> bool { std/* c */::env::var(\"X\").is_ok() }", true),
    ("fn f() -> bool { std::/* c */env::var(\"X\").is_ok() }", true),
    ("fn f() { core :: mem :: drop(1) }", true),
    ("type V = alloc :: vec :: Vec<u8>;", true),
    ("fn f() -> bool { std\n::\nenv::var(\"X\").is_ok() }", true),     // line feeds around ::
    ("fn f() -> bool { std\t::\tenv::var(\"X\").is_ok() }", true),
    ("fn f() -> bool { r#std :: env :: var(\"X\").is_ok() }", true),
    ("/// see std :: env :: var for the variable", true),             // doc comment naming it
    ("//! use std /* c */ as s;", true),
    ("*/ use std /* c */ as s;", true),                                // a stray closer first
    ("/*/ use std as s; */", true),                                    // `/*/` opener
    ("let u = \"http://x\";\nuse std /* c */ as s;", true),            // `//` in a string, alias next line
    ("let u = \"a//b\"; use std /* c */ as s;", true),                 // `//` in a string, same line
    ("let u = \"/*\"; use std /* c */ as s;", true),                   // `/*` in a string, same line
    ("let u = \"/*\";\nfn g() {}\nuse std /* c */ as s;", true),       // `/*` in a string, later line
    ("let r = r#\"/*\"#;\nuse std /* c */ as s;", true),               // `/*` in a raw string
    ("let c = b\"/*\";\nuse core // c\n as c;", true),                 // byte string
    ("let r = r#\"use std /* c */ as s;\"#;", false),                  // only inside a raw string
    ("let s = \"std :: env\";", false),                                // only inside a string
    ("fn f() -> bool { std\u{0b}::\u{0b}env::var(\"X\").is_ok() }", true),          // VT is Rust whitespace
    ("fn f() -> bool { std\u{85}::env::var(\"X\").is_ok() }", true),                // U+0085 NEL
    ("fn f() -> bool { std\u{200e}::\u{200e}env::var(\"X\").is_ok() }", true),      // U+200E LRM
    ("fn f() -> bool { std\u{2028}::env::var(\"X\").is_ok() }", true),              // U+2028
    ("use std\u{200f}as s;", false),                                   // RLM between std and as: not valid Rust? recorded
    ("use std\u{2029}as\u{2029}s;", true),                             // U+2029 around as
    ("use std\u{0c}as s;", true),                                      // FF (ASCII whitespace)
    ("fn f() { mystd :: x() }", false),                                // not a root (control)
];

fn show(label: &str, text: &str, real: Option<bool>) -> (bool, bool, Vec<String>) {
    let b = tb::hits(text);
    let h = th::hits(text);
    let missing = sub_multiset(&b, &h);
    println!("T07 {label} | {:<62} | base {} | head {} | base hits the head lacks {:?}{}",
        format!("{text:?}"), b.len(), h.len(), missing,
        match real { Some(true) if h.is_empty() => " | HEAD MISSES A REAL USE", Some(false) if !h.is_empty() => " | (literal only: extra hit)", _ => "" });
    if !h.is_empty() && b.is_empty() { println!("    head-only hits: {h:?}"); }
    (!b.is_empty(), !h.is_empty(), missing)
}

#[test]
fn t07_spellings() {
    let (mut lacks, mut n, mut miss_real) = (0, 0, vec![]);
    let (mut bf, mut hf) = (0, 0);
    for s in OLD17 {
        let (b, h, m) = show("old17", &format!("//! x\n{s}\n"), None);
        n += 1; lacks += m.len(); bf += b as usize; hf += h as usize;
    }
    println!("OLD17: base finds {bf} of 17, head finds {hf} of 17");
    let (mut bf, mut hf) = (0, 0);
    for (s, real) in MINE {
        for (w, text) in [("wrapped", format!("//! x\n{s}\n")), ("at start", s.to_string()), ("at end", format!("fn a() {{}}\n{s}"))] {
            let (b, h, m) = show(&format!("mine {w}"), &text, Some(*real));
            n += 1; lacks += m.len(); bf += b as usize; hf += h as usize;
            if *real && !h { miss_real.push(format!("{w}: {s:?}")); }
        }
    }
    println!("MINE: {} spellings x 3 placements = {} texts; base finds {bf}, head finds {hf}", MINE.len(), MINE.len() * 3);
    println!("T07SUM {n} texts; base hits the head lacks: {lacks}; real uses the head misses: {}", miss_real.len());
    for m in &miss_real { println!("  HEAD MISSES {m}"); }
    assert_eq!(lacks, 0, "a base hit is not a head hit");
}

#[test]
fn t07_real_src() {
    let dir = std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("src");
    for f in ["lib.rs", "families.rs"] {
        let text = std::fs::read_to_string(dir.join(f)).unwrap();
        println!("SRC {f}: base hits {:?} head hits {:?}", tb::hits(&text), th::hits(&text));
        assert!(th::hits(&text).is_empty());
    }
}

#[test]
fn t07_hostile() {
    let k = 1 << 16;
    let cases: Vec<(&str, String)> = vec![
        ("unclosed /* at the end", "fn a() {}\n/*".into()),
        ("lone / at the end", "fn a() {}\n/".into()),
        ("lone * at the end", "fn a() {} *".into()),
        ("// at the very end", "fn a() {} //".into()),
        ("only /", "/".into()),
        ("empty", "".into()),
        ("/* x 64Ki", "/*".repeat(k)),
        ("*/ x 64Ki", "*/".repeat(k)),
        ("/*/ x 64Ki", "/*/".repeat(k)),
        ("// x 64Ki", "//".repeat(k)),
        ("/ then multibyte x 64Ki", "/é".repeat(k)),
        ("/* then multibyte unclosed", format!("/*{}", "東🙂".repeat(k))),
        ("// then multibyte to the end", format!("//{}", "🙂".repeat(k))),
        ("nested opens then one close", format!("{}*/", "/*".repeat(k))),
        ("std :: x 1Ki (quadratic?)", "std :: ".repeat(1024)),
        ("std :: x 2Ki (quadratic?)", "std :: ".repeat(2048)),
        ("std :: x 4Ki (quadratic?)", "std :: ".repeat(4096)),
        ("std :: x 8Ki (quadratic?)", "std :: ".repeat(8192)),
        ("std :: x 16Ki (quadratic?)", "std :: ".repeat(16384)),
        ("std::std:: glued x 8Ki", "std::".repeat(8192)),
        ("a :: x 64Ki (no root)", "a :: ".repeat(k)),
        ("use std /* c */ as s; x 16Ki", "use std /* c */ as s;\n".repeat(k / 4)),
    ];
    for (label, t) in &cases {
        let s = Instant::now();
        let h = th::hits(t);
        let ms = s.elapsed().as_secs_f64() * 1000.0;
        println!("HOSTILE {label:<32} {:>8} bytes  head hits {:>6}  {ms:>9.2} ms", t.len(), h.len());
    }
}
