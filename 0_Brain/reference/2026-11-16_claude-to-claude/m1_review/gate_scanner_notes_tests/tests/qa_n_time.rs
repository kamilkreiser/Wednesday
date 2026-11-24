//! QA-SCANNER-NOTES (independent check), section 6: hostile shapes for each new rule, 8 KiB and 64 KiB,
//! smallest of five, and the ratio. Every value is made up.
use coagent_scanner::{scan, Kind, MAX_SCAN_BYTES};
use std::time::{Duration, Instant};

fn best5(t: &str) -> Duration {
    (0..5).map(|_| { let s = Instant::now(); let v = scan(t); let d = s.elapsed(); std::hint::black_box(v); d }).min().unwrap()
}
fn fill_to(unit: &str, len: usize) -> String {
    let mut s = unit.repeat(len / unit.len() + 1);
    while s.len() > len { s.pop(); }
    while !s.is_char_boundary(s.len()) { s.pop(); }
    s
}

#[test]
fn qa_time_new_rules() {
    let shapes: Vec<(&str, Box<dyn Fn(usize) -> String>)> = vec![
        ("CR x (n-1) then LF", Box::new(|n| format!("{}\n", "\r".repeat(n - 1)))),
        ("CR x n, no LF", Box::new(|n| "\r".repeat(n))),
        ("CR blank tab run, LF at the very end", Box::new(|n| format!("{}\n", fill_to("\r \t", n - 1)))),
        ("CR blank tab run, x at the very end", Box::new(|n| format!("{}x", fill_to("\r \t", n - 1)))),
        ("CR blank CR LF repeated", Box::new(|n| fill_to("\r \r\n", n))),
        ("base64 line + CR CR LF repeated", Box::new(|n| fill_to("UUFGQUtFMDAwMXF1\r\r\n", n))),
        ("netrc password + CR blank CR LF", Box::new(|n| fill_to("password qapw0001\r \r\n", n))),
        ("machine + CR tab CR LF + password", Box::new(|n| fill_to("machine h\r\t\r\npassword x ", n))),
        ("argv flag then one long blank run", Box::new(|n| format!("\"--key\"{}", " ".repeat(n - 7)))),
        ("argv flag, blanks, comma, repeated", Box::new(|n| fill_to("\"--key\"   ,   ", n))),
        ("argv value quote left open, repeated", Box::new(|n| fill_to("[\"--key\", \"", n))),
        ("argv pairs mixed quotes", Box::new(|n| fill_to("'--key', \"v\", ", n))),
        ("argv -u pairs", Box::new(|n| fill_to("\"-u\", \"a:b\", ", n))),
        ("JSON escape then flag", Box::new(|n| fill_to("\\n--key x", n))),
        ("JSON escape then dash", Box::new(|n| fill_to("\\n-", n))),
        ("escaped backslash n then -u=a:b", Box::new(|n| fill_to("\\\\n-u=a:b ", n))),
        ("mysql then JSON escape -p glued", Box::new(|n| format!("mysql {}", fill_to("\\n-pX", n - 6)))),
        ("--user=a:b repeated", Box::new(|n| fill_to("--user=a:b ", n))),
        ("-u= then one long value with colons", Box::new(|n| format!("-u={}", fill_to("a:", n - 3)))),
        ("ZWSP ESC [ repeated (views 2-4)", Box::new(|n| fill_to("\u{200b}\u{1b}[", n))),
        ("ESC ZWSP [0m repeated", Box::new(|n| fill_to("\u{1b}\u{200b}[0m", n))),
        ("ESC [ ZWSP 0m AB12 repeated", Box::new(|n| fill_to("\u{1b}[\u{200b}0mAB12", n))),
        ("LRI colour hex reset repeated", Box::new(|n| fill_to("\u{2066}\u{1b}[31m0a1b2c3d\u{1b}[0m", n))),
        ("ESC [ ZWSP then long param run", Box::new(|n| format!("\u{1b}[\u{200b}{}", "0".repeat(n - 5)))),
        ("ESC [ with ZWSP every param byte", Box::new(|n| format!("\u{1b}[{}", fill_to("1\u{200b}", n - 2)))),
    ];
    let mut worst = 0.0f64;
    for (name, mk) in &shapes {
        let a = mk(8 * 1024);
        let b = mk(MAX_SCAN_BYTES);
        assert!(b.len() <= MAX_SCAN_BYTES, "{name} {}", b.len());
        assert!(!scan(&b).names(Kind::TooLarge), "{name} was TooLarge");
        let (ta, tb) = (best5(&a), best5(&b));
        let ms = tb.as_secs_f64() * 1e3;
        worst = worst.max(ms);
        println!("QATIME {name:<40} 8K {:>7.3} ms  64K {:>8.3} ms  ratio {:>5.2}", ta.as_secs_f64() * 1e3, ms, tb.as_secs_f64() / ta.as_secs_f64().max(1e-9));
    }
    println!("QATIME worst 64K {worst:.2} ms");
    // the builder's built t05 row: CR x (64 Ki - 1) then LF is exactly the bound and is scanned
    let row = format!("{}\n", "\r".repeat(MAX_SCAN_BYTES - 1));
    println!("QATIME t05 row CR x (64Ki-1) then LF: {} bytes, verdict {:?}", row.len(), scan(&row));
    let over = format!("{}\n", "\r".repeat(MAX_SCAN_BYTES));
    println!("QATIME CR x 64Ki then LF: {} bytes, verdict {:?}", over.len(), scan(&over));
}
