//! QA-SCANNER-CORE items 4 and 5: own property under catch_unwind (own seed, own generators),
//! hostile shapes timed (the builder's 22 + 12 of mine), and "nothing of the input in a verdict"
//! proven by reconstruction: the Debug of every verdict must equal a rendering built ONLY from
//! (kind, count) pairs, so no other byte can be in it; the counts are then examined separately.
#[path = "qa/gen.rs"]
mod gen;

use coagent_scanner::{scan, Kind, Verdict, MAX_SCAN_BYTES};
use std::panic::{catch_unwind, AssertUnwindSafe};
use std::time::{Duration, Instant};

const SEED: u64 = 0x51c0_de00_0000_0002;
const CASES: usize = 300_000;

/// The Debug a verdict must have if it holds only kinds and counts.
fn rebuild(v: &Verdict) -> String {
    match v {
        Verdict::Clean => "Clean".into(),
        Verdict::Flagged(fs) => {
            let parts: Vec<String> = fs
                .iter()
                .map(|f| format!("Finding {{ kind: {:?}, count: {} }}", f.kind(), f.count()))
                .collect();
            format!("Flagged([{}])", parts.join(", "))
        }
    }
}

fn texts_ok(v: &Verdict) -> bool {
    const FIXED: &[&str] = &[
        "a private key block", "a web address with a user name and password",
        "a word such as Bearer or token followed by a value",
        "an authorization or cookie header with a value",
        "a value given to a secret-looking or upper-case name", "a password given on a command line",
        "a token with a known credential prefix, or a web token",
        "a long run of mixed letters and digits", "a long run of hexadecimal digits",
        "lines of base64 text", "too large to scan",
    ];
    v.findings().iter().all(|f| FIXED.contains(&f.text()))
}

fn bytes_gen(r: &mut gen::Rng) -> String {
    // byte soup with surrogate encodings, overlongs, out-of-range, lone continuations; made valid
    let n = r.below(400);
    let mut b = vec![];
    for _ in 0..n {
        match r.below(12) {
            0 => b.extend_from_slice(&[0xED, 0xA0 + r.below(32) as u8, 0x80 + r.below(64) as u8]),
            1 => b.extend_from_slice(&[0xC0, 0x80]),
            2 => b.extend_from_slice(&[0xF4, 0x90, 0x80, 0x80]),
            3 => b.push(0x80 + r.below(64) as u8),
            4 => b.extend_from_slice(&[0xF8, 0x88, 0x80, 0x80, 0x80]),
            5 => b.extend_from_slice("東".as_bytes()),
            6 => b.extend_from_slice("\u{E0041}".as_bytes()),
            7 => {
                let f = r.below(10);
                b.extend_from_slice(gen::piece(r, f).as_bytes())
            }
            _ => b.push(r.below(128) as u8),
        }
    }
    String::from_utf8_lossy(&b).into_owned()
}

fn long_line(r: &mut gen::Rng) -> String {
    let target = 1000 + r.below(MAX_SCAN_BYTES + 200);
    let mut s = String::new();
    while s.len() < target {
        let f = r.below(10);
        s.push_str(&gen::piece(r, f).replace('\n', " "));
        s.push(*r.pick(&[' ', '=', ':', '-', '"', '`']));
    }
    s
}

fn delimiters(r: &mut gen::Rng) -> String {
    let set: &[&str] = &["=", ":", "-", "/", "@", "\"", "'", "`", "\n", "\r", "\t", " ", ";", ",", "&", ".", "_", "+", "\u{200B}", "\u{FEFF}"];
    let n = r.below(3000);
    (0..n).map(|_| *r.pick(set)).collect()
}

fn repeated_prefix(r: &mut gen::Rng) -> String {
    let units: &[&str] = &[
        "-----BEGIN PRIVATE ", "-----BEGIN ", "-----END ", "ghp_", "_ghp_", "eyJ.", "--password ",
        "://", "a:b@", "Bearer ", "token\t", "Cookie: ", "machine password ", "password '",
        "IDENTIFIED BY '", "htpasswd -b ", "mysql -p ", "docker login -p ", "PASSWORD=", "key=\"",
        "x_key='", "AKIA", "sk-", "0a", "Qq0/", "\r\n", "\r",
    ];
    let u = *r.pick(units);
    let k = 1 + r.below(MAX_SCAN_BYTES / u.len() + 4);
    u.repeat(k)
}

fn near_bound(r: &mut gen::Rng) -> String {
    let tail = *r.pick(&["é", "東", "🙂", "\u{200B}", "a", "ghp_qaFAKE0001qaFAKE0002"]);
    let n = (MAX_SCAN_BYTES + r.below(8)).saturating_sub(4 + tail.len());
    format!("{}{tail}", "b".repeat(n))
}

#[test]
fn qa_property_no_panic_no_leak() {
    let mut r = gen::Rng::new(SEED);
    let mut reach = [0usize; 12];
    let mut worst = (Duration::ZERO, String::new());
    let mut count_max = 0u32;
    for i in 0..CASES {
        let g = i % 6;
        let s = match g {
            0 => bytes_gen(&mut r),
            1 => if i % 60 == 1 { long_line(&mut r) } else { gen::text(&mut r, 30) },
            2 => delimiters(&mut r),
            3 => if i % 30 == 3 { repeated_prefix(&mut r) } else { gen::text(&mut r, 12) },
            4 => if i % 300 == 4 { near_bound(&mut r) } else { bytes_gen(&mut r) },
            _ => gen::text(&mut r, 6),
        };
        let t0 = Instant::now();
        let a = catch_unwind(AssertUnwindSafe(|| scan(&s)));
        let d = t0.elapsed();
        let a = a.unwrap_or_else(|_| panic!("qa_props: scan panicked on case {i} (seed {SEED:#x}, generator {g})"));
        let b = catch_unwind(AssertUnwindSafe(|| scan(&s))).expect("second scan panicked");
        assert_eq!(a, b, "qa_props: not deterministic on case {i}");
        assert_eq!(format!("{a:?}"), rebuild(&a), "qa_props: Debug holds more than kinds and counts, case {i}");
        assert!(texts_ok(&a), "qa_props: a text() outside the fixed eleven, case {i}");
        if let Verdict::Flagged(f) = &a {
            assert!(!f.is_empty(), "Flagged never empty");
            for x in f {
                count_max = count_max.max(x.count());
                let k = Kind::FAMILIES.iter().position(|k| *k == x.kind()).unwrap_or(10);
                reach[k] += 1;
            }
        } else {
            reach[11] += 1;
        }
        if d > worst.0 {
            worst = (d, format!("case {i} gen {g} len {}", s.len()));
        }
    }
    println!("qa_props: seed {SEED:#x}, {CASES} cases, no panic, deterministic, Debug == kinds+counts for all");
    println!("qa_props: reach {:?} (10 families, TooLarge, Clean)", reach);
    println!("qa_props: largest count seen {count_max}; slowest single scan {:?} ({})", worst.0, worst.1);
    assert!(reach.iter().all(|&n| n > 0), "control: every outcome reached");
}

fn smallest_of_five(t: &str) -> Duration {
    (0..5).map(|_| { let s = Instant::now(); std::hint::black_box(scan(t)); s.elapsed() }).min().unwrap_or_default()
}

fn fill_to(unit: &str, len: usize) -> String {
    let mut s = unit.repeat(len / unit.len() + 1);
    while s.len() > len {
        s.pop();
    }
    s
}

#[test]
fn qa_hostile_shapes_timed() {
    let m = MAX_SCAN_BYTES;
    let body = |n: usize| { let mut s = String::from("FAKE0001"); while s.len() < n { s.push(if s.len() % 2 == 0 { '0' } else { 'x' }); } s.truncate(n); s };
    let shapes: Vec<(&str, String)> = vec![
        // the builder's 22 (t05_bounds.rs:123-161), rebuilt here
        ("B all =", "=".repeat(m)), ("B all -", "-".repeat(m)), ("B all :", ":".repeat(m)),
        ("B :// repeated", fill_to("://", m)), ("B -----BEGIN repeated", fill_to("-----BEGIN ", m)),
        ("B -----BEGIN PRIVATE repeated", fill_to("-----BEGIN PRIVATE ", m)),
        ("B Cookie: repeated", fill_to("Cookie:", m)), ("B token repeated", fill_to("token ", m)),
        ("B A= repeated", fill_to("A=", m)), ("B key=\" repeated", fill_to("key=\"", m)),
        ("B -p on a mysql line", format!("mysql{}", fill_to(" -p", m - 5))),
        ("B -b on an htpasswd line", format!("htpasswd{}", fill_to(" -b", m - 8))),
        ("B password ' repeated", fill_to("password '", m)),
        ("B password on a machine line", format!("machine{}", fill_to(" password x", m - 7))),
        ("B -ghp_ repeated", fill_to("-ghp_", m)), ("B eyJ. repeated", fill_to("eyJ.", m)),
        ("B one token at the bound", body(m)), ("B one 128 KiB token", body(2 * m)),
        ("B base64 lines", fill_to("RkFLRTAwMDFGQUtF\n", m)),
        ("B alternating base64 lines", fill_to("RkFLRTAwMDFGQUtF\n!!\n", m)),
        ("B zero-width space every other byte", fill_to("a\u{200B}", m)),
        ("B 16 KiB-ish prose", fill_to("we looked at the plan and moved on. ", 16 * 1024)),
        // mine
        ("Q --password \" unclosed, repeated", fill_to(" --password \"", m)),
        ("Q x_key=' unclosed, repeated", fill_to(" x_key='", m)),
        ("Q -p repeated, mysql at the END of the line", format!("{}mysql", fill_to(" -p", m - 5))),
        ("Q password x repeated, no machine", fill_to(" password x", m)),
        ("Q IDENTIFIED BY ' repeated", fill_to("IDENTIFIED BY '", m)),
        ("Q token then long colon run", fill_to("token ::::::::::::::::::::::::::::::::::::::: ", m)),
        ("Q one URL token full of :@", format!("a://{}", fill_to(":@", m - 4))),
        ("Q _ghp inside one run", fill_to("_ghp", m)),
        ("Q tag character every other char", fill_to("a\u{E0041}", m)),
        ("Q only CR", "\r".repeat(m)),
        ("Q only LF", "\n".repeat(m)),
        ("Q -b repeated, htpasswd at the END", format!("{}htpasswd", fill_to(" -bx", m - 8))),
        ("Q BEGIN PRIVATE / -----END alternating", fill_to("-----BEGIN PRIVATE\n-----END\n", m)),
        ("Q machine at END, password x repeated", format!("{}machine ", fill_to(" password x", m - 8))),
    ];
    let mut worst = Duration::ZERO;
    for (n, t) in &shapes {
        let d = smallest_of_five(t);
        worst = worst.max(d);
        println!("TIME | {n:<44} | {:>6} B | {:>8.2} ms", t.len(), d.as_secs_f64() * 1e3);
    }
    println!("TIME worst {:.2} ms over {} shapes", worst.as_secs_f64() * 1e3, shapes.len());
}

/// Item 5: digits. Can a count carry the input? Secrets made of digits only, and texts whose
/// length or number of matches is chosen to equal a value.
#[test]
fn qa_digits_and_counts() {
    for (label, t) in [
        ("PIN in env", "PIN=48213579".to_string()),
        ("digits after token", "token 4821357900".to_string()),
        ("digits password flag", "mysql -p48213579 db".to_string()),
        ("card-like in yaml", "card_secret: 4111111111111111".to_string()),
        ("hex-like digits only", "4821357900482135790048213579".to_string()),
    ] {
        let v = scan(&t);
        let dbg = format!("{v:?}");
        // every digit run in the Debug is a count; is any input digit run (>=3) in it?
        let input_runs: Vec<&str> = t.split(|c: char| !c.is_ascii_digit()).filter(|x| x.len() >= 3).collect();
        let leaked: Vec<&&str> = input_runs.iter().filter(|r| dbg.contains(**r)).collect();
        println!("DIGITS | {label:<22} | {dbg} | input digit runs in Debug: {leaked:?}");
        assert!(leaked.is_empty());
    }
    // a sender can make a count equal a number it chooses: N matches -> count N
    for n in [7usize, 4821, 13579] {
        let t = "token x ".repeat(n);
        let v = scan(&t);
        let c = v.findings().iter().find(|f| f.kind() == Kind::AuthScheme).map(|f| f.count());
        println!("COUNT | {n} x 'token x ' ({} bytes) -> AuthScheme count {c:?}", t.len());
    }
}

/// Re-time the slowest debug case (110341) smallest of five, regenerating the same sequence.
#[test]
fn qa_retime_case_110341() {
    let mut r = gen::Rng::new(SEED);
    for i in 0..=110_341usize {
        let g = i % 6;
        let s = match g {
            0 => bytes_gen(&mut r),
            1 => if i % 60 == 1 { long_line(&mut r) } else { gen::text(&mut r, 30) },
            2 => delimiters(&mut r),
            3 => if i % 30 == 3 { repeated_prefix(&mut r) } else { gen::text(&mut r, 12) },
            4 => if i % 300 == 4 { near_bound(&mut r) } else { bytes_gen(&mut r) },
            _ => gen::text(&mut r, 6),
        };
        if i == 110_341 {
            let d = smallest_of_five(&s);
            println!("RETIME case {i} gen {g} len {} lines {}: smallest of five {:.2} ms", s.len(), s.lines().count(), d.as_secs_f64() * 1e3);
        }
    }
}
