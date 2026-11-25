//! QA-SCANNER-NEXT (independent check): base `debbb44` against head `dd70630`, own harness.
//! base = scratch module from git; head = the library itself; headcopy = head copied unchanged
//! (control: 0 differences); headmut = head with ONE character changed in a rule (planted control:
//! must differ). Every text is compared by verdict AND kinds AND counts. Every value is made up.
#[path = "qa/gen.rs"]
mod gen;
#[path = "qa_r2_gen.rs"]
mod r2gen;
macro_rules! m { ($name:ident, $p:literal) => {
    #[path = $p]
    #[allow(dead_code, unused, missing_docs, clippy::all)]
    mod $name;
}; }
m!(base, "qa_base/mod.rs");
m!(headcopy, "qa_headcopy/mod.rs");
m!(headmut, "qa_headmut/mod.rs");
#[path = "qa_t03_base.rs"]
#[allow(dead_code)]
mod t03b;
#[path = "t03_known_overflag.rs"]
#[allow(dead_code)]
mod t03h;
#[path = "qa_sx_data.rs"]
mod data;

type Sig = (bool, Vec<(String, u32)>);
macro_rules! sig { ($m:path, $t:expr) => {{ use $m as mm; let v = mm::scan($t);
    (v.share_flagged(), v.findings().iter().map(|f| (format!("{:?}", f.kind()), f.count())).collect::<Vec<(String, u32)>>()) }}; }
fn bsig(t: &str) -> Sig { sig!(base, t) }
fn hsig(t: &str) -> Sig { sig!(coagent_scanner, t) }

struct Tally { label: String, n: usize, fb: usize, fh: usize, diff: usize, copy_ne: usize, mut_ne: usize }
impl Tally {
    fn new(label: &str) -> Self { Tally { label: label.into(), n: 0, fb: 0, fh: 0, diff: 0, copy_ne: 0, mut_ne: 0 } }
    fn one(&mut self, t: &str, controls: bool) {
        self.n += 1;
        let (a, b) = (bsig(t), hsig(t));
        if a.0 { self.fb += 1; }
        if b.0 { self.fh += 1; }
        if a != b { self.diff += 1; if self.diff <= 5 { println!("DIFFER {} case {} base {a:?} head {b:?} | {t:?}", self.label, self.n); } }
        if controls {
            if sig!(headcopy, t) != b { self.copy_ne += 1; }
            if sig!(headmut, t) != b { self.mut_ne += 1; }
        }
    }
    fn report(&self, controls: bool) {
        print!("SXDIFF {}: {} texts; flagged base {} -> head {}; differing in verdict, kinds or counts: {}", self.label, self.n, self.fb, self.fh, self.diff);
        if controls { print!("; controls: headcopy != head {}, headmut (HEX_MIN 16->15) != head {}", self.copy_ne, self.mut_ne); }
        println!();
    }
}

fn gen_text(r: &mut gen::Rng, i: usize) -> String { gen::text(r, if i % 10 == 0 { 40 } else { 8 }) }

#[test]
fn sx_generated() {
    let mut total = 0;
    for (label, n, seed, rich) in [("gen 0x0a5c0ffee5eed001 (earlier checks' seed)", 200_000usize, 0x0a5c_0ffe_e5ee_d001u64, false),
                                   ("gen 0x95ca17e70a11d001 (mine)", 200_000, 0x95ca_17e7_0a11_d001, false),
                                   ("rich 0x0e2c0ffee5eed003 (earlier checks' seed)", 250_000, 0x0e2c_0ffe_e5ee_d003, true),
                                   ("rich 0x95ca17e70a11d003 (mine)", 250_000, 0x95ca_17e7_0a11_d003, true)] {
        let mut r = gen::Rng::new(seed);
        let mut t = Tally::new(label);
        for i in 0..n { let s = if rich { r2gen::rich_text(&mut r) } else { gen_text(&mut r, i) }; t.one(&s, true); }
        t.report(true);
        assert_eq!(t.diff, 0, "{label}: texts differ");
        assert_eq!(t.copy_ne, 0, "{label}: the head copy is not the library");
        total += t.n;
    }
    println!("SXDIFF generated total {total}");
}

/// My own targeted texts: every flag spelling x joiner x value x prefix x suffix around the N-1/N-2 forms.
#[test]
fn sx_targeted() {
    let flags = ["--password", "-p", "-P", "--Password", "--token", "--api-key", "--secret", "--pass", "-u", "--user", "-U", "--USER", "--User", "-pw", "--release"];
    let joins = [" ", "=", "= ", "\", \"", "\",\n  \"", "\",\r\n  \"", "' '", "\t", "\",\"", "\" , \"", "\\\", \\\"", "',\n'", "\",\n\n\"", "\",,\""];
    let values = ["qa:qapw0001", "qapw0001", ":", "x", "1000:1000", "-x", "", "qa:", ":qapw0001"];
    let pre = ["", "[", "[\"", "'", "\"", "mysql ", "[\"mysql\", \"", "{\"cmd\": \"a\\n", "{\"cmd\": \"a\\u000a", "C:\\tools\\n", "C:\\run\\t",
               "C:\\x\\r", "curl ", "docker run ", "\\\\n", "`", "(", "{\"args\": \"[\\\"", "psql ", "a\\b", "x"];
    let suf = ["", "\"]", "'", "\"}", " https://h", "\n", "\r\n", " x", "\\\"]\"}"];
    let mut t = Tally::new("targeted N-1/N-2 forms (mine)");
    for f in flags { for j in joins { for v in values { for p in pre { for s in suf {
        t.one(&format!("{p}{f}{j}{v}{s}"), false);
    } } } } }
    t.report(false);
    assert_eq!(t.diff, 0);
}

#[test]
fn sx_fixed_lists() {
    let mut pins: Vec<&str> = vec![];
    for l in [t03b::KNOWN_OVERFLAGS, t03b::KNOWN_MISSES, t03h::KNOWN_OVERFLAGS, t03h::KNOWN_MISSES] { for (_, e) in l { pins.push(e); } }
    println!("PINS base overflags {} misses {}; head overflags {} misses {}", t03b::KNOWN_OVERFLAGS.len(), t03b::KNOWN_MISSES.len(), t03h::KNOWN_OVERFLAGS.len(), t03h::KNOWN_MISSES.len());
    for (label, texts) in [("t03 pins, base lists and head lists", pins),
                           ("docs/SCANNER.md backtick spans (base and head)", data::DOC_SPANS.to_vec()),
                           ("SCANNER-NOTES check's s5_forms_rows", data::S5_ROWS.iter().map(|x| x.1).collect())] {
        let mut t = Tally::new(label);
        for s in &texts { t.one(s, true); }
        t.report(true);
        assert_eq!(t.diff, 0);
    }
}

/// Planted control for the differential itself: the mutated head must differ from the head on generated text.
#[test]
fn sx_control_mut_differs() {
    let mut r = gen::Rng::new(0x95ca_17e7_0a11_d001);
    let mut ne = 0;
    for i in 0..200_000 { let s = gen_text(&mut r, i); if sig!(headmut, &s) != hsig(&s) { ne += 1; } }
    println!("CONTROL headmut != head on {ne} of 200000 (mine seed)");
    assert!(ne > 0, "control: a one-character rule change showed no difference");
}
