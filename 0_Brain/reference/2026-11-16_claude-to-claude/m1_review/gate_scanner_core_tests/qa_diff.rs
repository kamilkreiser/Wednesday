//! QA-SCANNER-CORE item 2: differential against the base redactor (`coagent-audit/src/redact.rs`
//! at 039b987, blob d35730cf, copied with its `cfg!(coagent_audit_red = ..)` switches set to false).
//! For each generated text: per family, "the base redactor's family matches (on the text with
//! format characters stripped, as the redactor does)" vs "scan names that family". Every miss is
//! printed. Window aside: texts stay far under 64 KiB.
#[path = "qa/gen.rs"]
mod gen;
#[path = "qa/redact_base.rs"]
#[allow(dead_code, unused)]
mod redact;

use coagent_scanner::{scan, Kind};
use redact::patterns as p;

fn nl(b: &[u8]) -> Vec<usize> {
    let mut nl = vec![b.len(); b.len() + 1];
    for i in (0..b.len()).rev() {
        nl[i] = if b[i] == b'\n' { i } else { nl[i + 1] };
    }
    nl
}

/// per family: did the base redactor's rule(s) for it match?
fn base_families(text: &str) -> [bool; 10] {
    base_on(&redact::strip_format_chars(text))
}

/// the base rules on a text as given (no stripping)
fn base_on(s: &str) -> [bool; 10] {
    let b = s.as_bytes();
    let lower: Vec<u8> = b.iter().map(|c| c.to_ascii_lowercase()).collect();
    let n = nl(b);
    let mut out = [false; 10];
    let mut go = |i: usize, f: &mut dyn FnMut(&mut Vec<(usize, usize)>)| {
        let mut r = vec![];
        f(&mut r);
        out[i] = !r.is_empty();
    };
    go(0, &mut |r| p::private_key_blocks(&lower, &n, r));
    go(1, &mut |r| p::url_userinfo(b, r));
    go(2, &mut |r| p::auth_schemes(&lower, r));
    go(3, &mut |r| p::line_headers(&lower, &n, r));
    go(4, &mut |r| p::assignments(b, &lower, &n, r));
    go(5, &mut |r| p::flags(b, &lower, &n, r));
    go(6, &mut |r| p::prefixed_tokens(b, r));
    go(7, &mut |r| p::long_tokens(b, r));
    go(8, &mut |r| p::hex_runs(b, r));
    go(9, &mut |r| p::base64_line_blocks(b, &n, r));
    out
}

const SEED: u64 = 0x0a5c_0ffe_e5ee_d001;
const N: usize = 400_000;

#[test]
fn qa_differential_against_base_redactor() {
    let mut r = gen::Rng::new(SEED);
    let mut whole_miss = 0usize;
    let mut fam_miss = [0usize; 10];
    let mut base_hit = [0usize; 10];
    let mut scan_only = [0usize; 10];
    let mut examples: Vec<String> = vec![];
    // misses explained only by the strip-list difference: the base rule matches on the base's
    // partly stripped text, but on NEITHER of the scanner's two views (raw, fully stripped)
    let mut list_artifact = 0usize;
    let mut real_miss = 0usize;
    let mut base_masks = 0usize;
    let mut clean = 0usize;
    for i in 0..N {
        let max = if i % 10 == 0 { 40 } else { 8 };
        let t = gen::text(&mut r, max);
        let bf = base_families(&t);
        let v = scan(&t);
        let any_base = bf.iter().any(|&x| x);
        if any_base {
            base_masks += 1;
        }
        if !v.share_flagged() {
            clean += 1;
        }
        if any_base && !v.share_flagged() {
            whole_miss += 1;
            if examples.len() < 40 {
                examples.push(format!("WHOLE case {i}: {t:?}"));
            }
        }
        for (k, kind) in Kind::FAMILIES.iter().enumerate() {
            let s = v.names(*kind);
            if bf[k] {
                base_hit[k] += 1;
                if !s {
                    fam_miss[k] += 1;
                    let full: String = t.chars().filter(|c| !coagent_scanner::is_format_char(*c)).collect();
                    if base_on(&t)[k] || base_on(&full)[k] {
                        real_miss += 1;
                        examples.push(format!("REAL {kind:?} case {i}: {t:?}"));
                    } else {
                        list_artifact += 1;
                    }
                    if examples.len() < 40 {
                        examples.push(format!("FAMILY {kind:?} case {i}: {t:?}"));
                    }
                }
            } else if s {
                scan_only[k] += 1;
            }
        }
    }
    println!("qa_diff: seed {SEED:#x}, {N} texts; base redactor masks something in {base_masks}; scan Clean in {clean}");
    println!("qa_diff: texts the base masks and scan calls Clean: {whole_miss}");
    for (k, kind) in Kind::FAMILIES.iter().enumerate() {
        println!(
            "qa_diff: {:<17} base matched {:>7}  scan missed {:>4}  scan-only {:>6}",
            format!("{kind:?}"),
            base_hit[k],
            fam_miss[k],
            scan_only[k]
        );
    }
    println!("qa_diff: family misses explained only by the strip-list difference: {list_artifact}; misses where the base rule matches a scanner view: {real_miss}");
    for e in &examples {
        println!("  {e}");
    }
    assert!(base_hit.iter().all(|&n| n > 100), "control: every base family reached");
    assert_eq!(real_miss, 0, "qa_diff: a base rule matches a scanner view but scan misses it");
}
