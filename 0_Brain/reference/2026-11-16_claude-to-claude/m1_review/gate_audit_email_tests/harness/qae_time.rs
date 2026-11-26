//! QA-AUDIT-EMAIL (g): own adversarial timing of `patterns::emails` and `PatternRedactor::redact`
//! (scratch copy only, release). Best of 3 per size; prints the fitted exponent of time against size.
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
    let (mx, my) = (xs.iter().map(|p| p.0.ln()).sum::<f64>() / n, xs.iter().map(|p| p.1.max(1.0).ln()).sum::<f64>() / n);
    let num: f64 = xs.iter().map(|p| (p.0.ln() - mx) * (p.1.max(1.0).ln() - my)).sum();
    let den: f64 = xs.iter().map(|p| (p.0.ln() - mx).powi(2)).sum();
    num / den
}

#[test]
#[ignore]
fn qae_time() {
    let mix = "Bearer Zm9vYmFy Authorization: Basic eA== API_KEY=v --password w ghp_16C7e42F292c6912E7710c838347Ae178B4a 9f86d081884c7d65 https://u:p@h.example/ -----BEGIN PRIVATE KEY----- a@b.example user:a@b.example:x a@b.example9f86 ";
    type F = (&'static str, Box<dyn Fn(usize) -> String>);
    let fams: Vec<F> = vec![
        ("@ x n", Box::new(|n| rep("@", n))),
        ("a@ x n", Box::new(|n| rep("a@", n))),
        ("a. x n (no @)", Box::new(|n| rep("a.", n))),
        ("a x n (local run)", Box::new(|n| rep("a", n))),
        ("a. x n then @", Box::new(|n| format!("{}@", rep("a.", n)))),
        ("@ then a. x n then 9", Box::new(|n| format!("a@{}9", rep("a.", n)))),
        ("@a. x n", Box::new(|n| rep("@a.", n))),
        ("x:// x n then addresses", Box::new(|n| format!("{}{}", rep("x://", n / 2), rep(" a@b.example", n / 2)))),
        ("a@b.c: x n", Box::new(|n| rep("a@b.c:", n))),
        ("a@b.example: x n (scp test each)", Box::new(|n| rep("a@b.example:", n))),
        ("a@b.example9 x n (glued)", Box::new(|n| rep("a@b.example9", n))),
        ("a@b. then - x n", Box::new(|n| format!("a@b.ex{}", rep("-", n)))),
        ("every rule's trigger", Box::new(move |n| rep(mix, n))),
    ];
    for (name, mk) in &fams {
        let mut e = vec![];
        let mut r = vec![];
        for kib in [64usize, 128, 256, 1024] {
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
        println!("QAE-G {name:34} | emails us 64/128/256/1024 KiB {:?} exp {:.2} | redact us {:?} exp {:.2}", fe, slope(&e), fr, slope(&r));
    }
}
