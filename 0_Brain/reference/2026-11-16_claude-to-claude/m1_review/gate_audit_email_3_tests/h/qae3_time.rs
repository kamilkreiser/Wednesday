//! QA-AUDIT-EMAIL-3 (g): own timing of `patterns::emails` and `PatternRedactor::redact` (scratch copy only, release).
//! Best of 3 per size; prints the least-squares exponent of log time on log size. QAE3_SIZES overrides the sizes (KiB).
use coagent_audit::redact::{patterns, PatternRedactor, Redactor};
use std::time::Instant;

fn rep(unit: &str, n: usize) -> String {
    unit.repeat(n / unit.len().max(1))
}
fn best(f: &dyn Fn()) -> f64 {
    (0..3)
        .map(|_| {
            let t = Instant::now();
            f();
            t.elapsed().as_secs_f64() * 1e6
        })
        .fold(f64::MAX, f64::min)
}
fn slope(xs: &[(f64, f64)]) -> f64 {
    let n = xs.len() as f64;
    let mx = xs.iter().map(|p| p.0.ln()).sum::<f64>() / n;
    let my = xs.iter().map(|p| p.1.max(1.0).ln()).sum::<f64>() / n;
    let num: f64 = xs.iter().map(|p| (p.0.ln() - mx) * (p.1.max(1.0).ln() - my)).sum();
    let den: f64 = xs.iter().map(|p| (p.0.ln() - mx).powi(2)).sum();
    num / den
}

#[test]
#[ignore]
fn qae3_time() {
    let mix = "Bearer Zm9vYmFy Authorization: Basic eA== API_KEY=v --password w ghp_16C7e42F292c6912E7710c838347Ae178B4a 9f86d081884c7d65 https://u:p@h.example/ -----BEGIN PRIVATE KEY----- a@b.example ";
    let sizes: Vec<usize> = std::env::var("QAE3_SIZES").map(|s| s.split(',').map(|x| x.parse().unwrap()).collect()).unwrap_or(vec![64, 128, 256, 1024]);
    let only = std::env::var("QAE3_ONLY").ok();
    type F = (&'static str, Box<dyn Fn(usize) -> String>);
    let fams: Vec<F> = vec![
        ("B1 a@ x n", Box::new(|n| rep("a@", n))),
        ("B2 a. x n then @b.example", Box::new(|n| format!("{}@b.example", rep("a.", n)))),
        ("B3 @ x n", Box::new(|n| rep("@", n))),
        ("B4 a x n (local run)", Box::new(|n| rep("a", n))),
        ("B5 a@b. x n", Box::new(|n| rep("a@b.", n))),
        ("B6 x://a@ x n", Box::new(|n| rep("x://a@", n))),
        ("B7 every rule's trigger", Box::new(move |n| rep(mix, n))),
        ("B8 a@b.example: x n then /", Box::new(|n| format!("{}/", rep("a@b.example:", n)))),
        ("B9 https://x.example/ then a@b.example/ x n", Box::new(|n| format!("https://x.example/{}", rep("a@b.example/", n)))),
        ("B10 a@ + a. x n + 9", Box::new(|n| format!("a@{}9", rep("a.", n)))),
        ("B11 a@b.example9 x n", Box::new(|n| rep("a@b.example9", n))),
        ("L1 https://x.example.com, then a@b.example, x n", Box::new(|n| format!("https://x.example.com,{}", rep("a@b.example,", n)))),
        ("L2 https://x.example.com& then a@b.example& x n", Box::new(|n| format!("https://x.example.com&{}", rep("a@b.example&", n)))),
        ("L3 git@b.example: x n then /", Box::new(|n| format!("{}/", rep("git@b.example:", n)))),
        ("L4 xgit@b.example: x n then /", Box::new(|n| format!("{}/", rep("xgit@b.example:", n)))),
        ("L5 a@b.example:~ x n", Box::new(|n| rep("a@b.example:~", n))),
        ("L6 a@b.example:/ x n", Box::new(|n| rep("a@b.example:/", n))),
        ("E1 one :// token, ab@ x n, end byte last", Box::new(|n| format!("https://{},", rep("ab@", n)))),
        ("E2 https://x.example.com + (a@b.example,) x n", Box::new(|n| format!("https://x.example.com{}", rep("a@b.example,", n)))),
        ("E3 https://x.example.com + (a@b.example&) x n", Box::new(|n| format!("https://x.example.com{}", rep("a@b.example&", n)))),
        ("E4 https://x.example.com + (a@b.example VT) x n", Box::new(|n| format!("https://x.example.com{}", rep("a@b.example\u{b}", n)))),
        ("E5 https://x.example.com + (a@b.example=) x n", Box::new(|n| format!("https://x.example.com{}", rep("a@b.example=", n)))),
        ("S1 (=://a@b.example ) x n", Box::new(|n| rep("=://a@b.example ", n))),
        ("S2 (x://) x n, no whitespace", Box::new(|n| rep("x://", n))),
        ("S3 (=://) x n then https://a@b.example", Box::new(|n| format!("{}https://a@b.example", rep("=://", n)))),
        ("G1 (git@b.example:) x n then /", Box::new(|n| format!("{}/", rep("git@b.example:", n)))),
        ("G2 (.git@b.example:) x n then /", Box::new(|n| format!("{}/", rep(".git@b.example:", n)))),
        ("G3 (a@b.example:c@d.example:) x n then /", Box::new(|n| format!("{}/", rep("a@b.example:c@d.example:", n)))),
    ];
    for (name, mk) in &fams {
        if let Some(o) = &only { if !name.starts_with(o.as_str()) { continue; } }
        let mut e = vec![];
        let mut r = vec![];
        for &kib in &sizes {
            let s = mk(kib * 1024);
            e.push((kib as f64, best(&|| {
                let mut v = Vec::new();
                patterns::emails(std::hint::black_box(s.as_bytes()), &mut v);
                std::hint::black_box(v);
            })));
            r.push((kib as f64, best(&|| {
                std::hint::black_box(PatternRedactor.redact(std::hint::black_box(&s)));
            })));
        }
        let fe: Vec<String> = e.iter().map(|p| format!("{:.0}", p.1)).collect();
        let fr: Vec<String> = r.iter().map(|p| format!("{:.0}", p.1)).collect();
        println!("QAE3-G {name:46} | emails us {:?} exp {:.2} | redact us {:?} exp {:.2}", fe, slope(&e), fr, slope(&r));
    }
}
