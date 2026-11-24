//! QA-SCANNER-CORE item 4: does time double when the input doubles? (8, 16, 32, 64 KiB; smallest of 7)
use coagent_scanner::scan;
use std::time::{Duration, Instant};
fn t(s: &str) -> Duration { (0..7).map(|_| { let a = Instant::now(); std::hint::black_box(scan(s)); a.elapsed() }).min().unwrap() }
fn fill(u: &str, n: usize) -> String { let mut s = u.repeat(n / u.len() + 1); while s.len() > n { s.pop(); } s }
#[test]
fn qa_scaling() {
    for u in ["-", "-----BEGIN ", " -p", " --password \"", "a\u{200B}", " password x", "_ghp", "Cookie:"] {
        let ms: Vec<f64> = [8192usize, 16384, 32768, 65536].iter().map(|&n| {
            let s = if u == " -p" { format!("mysql{}", fill(u, n - 5)) } else { fill(u, n) };
            t(&s).as_secs_f64() * 1e3
        }).collect();
        println!("SCALE | {u:?} | 8K {:.3} | 16K {:.3} | 32K {:.3} | 64K {:.3} ms | 64K/8K = {:.1}", ms[0], ms[1], ms[2], ms[3], ms[3] / ms[0]);
    }
}
