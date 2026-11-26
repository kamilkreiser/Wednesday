//! QA-AUDIT-EMAIL probe (scratch copy only, never committed). Reads QAE_IN (one hex-encoded UTF-8
//! input per line), writes QAE_OUT: per input, tab-separated:
//! find(clean) | find(clean window) | emails(clean) | emails(clean window) | clean | clean window |
//! redact | preview | chain summary body or E:<err> | chain full body
//! Spans "s-e,s-e" (as found, unsorted). Strings hex. emails columns are "-" in the base build.
#![allow(dead_code)]
mod common;
use coagent_audit::chain::{AuthorChain, EventInput};
use coagent_audit::checkpoint::CheckpointPolicy;
use coagent_audit::redact::{patterns, preview, strip_format_chars, PatternRedactor, Redactor, REDACT_WINDOW_BYTES};
use std::io::{BufRead, Write};

fn hx(s: &[u8]) -> String {
    let mut o = String::with_capacity(s.len() * 2);
    for b in s {
        o.push_str(&format!("{b:02x}"));
    }
    o
}
fn unhx(s: &str) -> String {
    let b: Vec<u8> = (0..s.len() / 2).map(|i| u8::from_str_radix(&s[2 * i..2 * i + 2], 16).unwrap()).collect();
    String::from_utf8(b).unwrap()
}
fn sp(v: &[(usize, usize)]) -> String {
    v.iter().map(|(s, e)| format!("{s}-{e}")).collect::<Vec<_>>().join(",")
}
fn em(t: &str) -> String {
    let _ = t;
    //QAE_NEW let mut r = Vec::new(); patterns::emails(t.as_bytes(), &mut r); return sp(&r);
    #[allow(unreachable_code)]
    "-".to_string()
}

#[test]
fn qae_dump() {
    let inp = std::env::var("QAE_IN").expect("QAE_IN");
    let out = std::env::var("QAE_OUT").expect("QAE_OUT");
    let id = common::fixed_identity(0xA7);
    let chain = AuthorChain::new(
        &id,
        common::session(0xA7),
        CheckpointPolicy { every_events: 1_000_000, every_ms: 3_600_000_000 },
        Box::new(PatternRedactor),
        common::t(0),
    );
    let mut w = std::io::BufWriter::new(std::fs::File::create(out).unwrap());
    let mut n = 0usize;
    for line in std::io::BufReader::new(std::fs::File::open(inp).unwrap()).lines() {
        let raw = unhx(line.unwrap().trim());
        let clean = strip_format_chars(&raw);
        let mut end = raw.len().min(REDACT_WINDOW_BYTES);
        while !raw.is_char_boundary(end) {
            end -= 1;
        }
        let cleanw = strip_format_chars(&raw[..end]);
        let fc = patterns::find(&clean);
        let fw = patterns::find(&cleanw);
        let red = PatternRedactor.redact(&raw);
        let pre = preview(&PatternRedactor, &raw);
        let ev = chain.prepare(&id, EventInput { kind: "qae.probe", summary: Some(&raw), full: Some(&raw) }, common::t(1));
        let (sum, full) = match ev {
            Ok(e) => (
                e.summary.map_or("N".into(), |o| hx(o.body.as_bytes())),
                e.full.map_or("N".into(), |o| hx(o.body.as_bytes())),
            ),
            Err(err) => (format!("E:{err:?}"), "-".into()),
        };
        writeln!(
            w,
            "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
            sp(&fc), sp(&fw), em(&clean), em(&cleanw),
            hx(clean.as_bytes()), if cleanw == clean { "=".into() } else { hx(cleanw.as_bytes()) },
            hx(red.as_bytes()), hx(pre.as_bytes()), sum, full
        )
        .unwrap();
        n += 1;
    }
    eprintln!("QAE probe: {n} inputs");
}
