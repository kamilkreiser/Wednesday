//! QA-SCANNER-NOTES (independent check): section 5 (no new miss from the new forms and views),
//! section 7 (over-flags, main against the head), FR-6 frequency. Every value is made up.
macro_rules! m { ($name:ident, $p:literal) => {
    #[path = $p]
    #[allow(dead_code, unused, missing_docs, clippy::all)]
    mod $name;
}; }
m!(main, "qa_main/mod.rs");
m!(le_main, "qa_le_main/mod.rs");
m!(le_head, "qa_le_head/mod.rs");
#[path = "qa_corpora.rs"]
#[allow(dead_code)]
mod corpora;
#[path = "qa_r2_flags_corpus.rs"]
mod flagcorpus;
use std::collections::BTreeMap;

macro_rules! sig { ($m:path, $t:expr) => {{ use $m as mm; mm::scan($t).findings().iter().map(|f| (format!("{:?}", f.kind()), f.count())).collect::<Vec<(String, u32)>>() }}; }
fn kinds(s: &[(String, u32)]) -> Vec<String> { s.iter().map(|x| x.0.clone()).collect() }
fn has(s: &[(String, u32)], k: &str) -> bool { s.iter().any(|x| x.0 == k) }
fn cnt(s: &[(String, u32)], k: &str) -> u32 { s.iter().find(|x| x.0 == k).map_or(0, |x| x.1) }

/// Compare one text: every family main names the head names; PasswordArgument count not lower.
struct Cmp { n: usize, lost: Vec<String>, pw_lower: Vec<String>, gained: usize, head_clean: usize, main_clean: usize }
impl Cmp {
    fn new() -> Self { Cmp { n: 0, lost: vec![], pw_lower: vec![], gained: 0, head_clean: 0, main_clean: 0 } }
    fn check(&mut self, label: &str, t: &str) {
        self.n += 1;
        let a = sig!(main, t);
        let b = sig!(coagent_scanner, t);
        for k in kinds(&a) { if !has(&b, &k) { self.lost.push(format!("{label}: {k} | {t:?}")); } }
        if cnt(&b, "PasswordArgument") < cnt(&a, "PasswordArgument") { self.pw_lower.push(format!("{label} | {t:?}")); }
        if kinds(&b).iter().any(|k| !has(&a, k)) { self.gained += 1; }
        if a.is_empty() { self.main_clean += 1; }
        if b.is_empty() { self.head_clean += 1; }
    }
    fn report(&self, label: &str) {
        println!("CASES {label}: {} texts; families named at main and not at head {}; PasswordArgument count lower at head {}; texts with a new family {}; Clean main {} head {}",
            self.n, self.lost.len(), self.pw_lower.len(), self.gained, self.main_clean, self.head_clean);
        for x in self.lost.iter().take(20) { println!("  LOST {x}"); }
        for x in self.pw_lower.iter().take(20) { println!("  PWLOWER {x}"); }
    }
}

const VALS: [&str; 2] = ["hunter22", "qaPw0001"];
const SHAPES: [&str; 10] = ["--password {v}", "-password {v}", "--passwd {v}", "--secret {v}", "--api-key {v}",
    "-u qauser:{v}", "--user qauser:{v}", "mysql -p{v}", "mysql -p {v}", "sshpass -p {v} ssh h"];

/// every byte or character main's start rule accepts before a flag (not an ASCII letter or digit, `-`, `_`, `.`, `/`)
fn accepted_starts() -> Vec<String> {
    let mut v: Vec<String> = (0u8..=0x7F).filter(|c| !(c.is_ascii_alphanumeric() || matches!(c, b'-' | b'_' | b'.' | b'/')))
        .map(|c| (c as char).to_string()).collect();
    for s in ["é", "東", "🙂", "\u{a0}", "\u{85}", "\u{2028}", "\u{2029}", "\u{3000}", "\u{200b}", "\u{180b}", "\u{2065}", "\u{ff08}",
              "\u{1b}[0m", "\u{1b}[1;31m", "\r\n", "\u{1b}[\u{200b}0m"] { v.push(s.to_string()); }
    v
}

#[test]
fn s5_starts_and_values_with_new_forms_nearby() {
    let mut c = Cmp::new();
    // new forms placed before and after the flag (and glued as the byte before the start byte)
    let before = ["", "[\"--key\", \"qv\"], ", "--user=qa:qb ", "\"x\\n", "x\\t", "\\\\n", "\", \"", "'--password', ", "-u=a:b,", "\"a\\n\", "];
    let after = ["", "\", \"z\"]", "\\n--secret y", " --user=q:w", ",\"", "', 'k'", "\\t", " [\"-u\", \"a:b\"]"];
    for st in accepted_starts() {
        for v in VALS {
            for s in SHAPES {
                let core = s.replace("{v}", v);
                for b in before {
                    for a in after {
                        c.check("start", &format!("{b}{st}{core}{a}"));
                    }
                }
                c.check("start-only", &format!("{st}{core}"));
            }
        }
    }
    // spaced values of the wrapped test, with odd value forms
    for s in ["--password", "--secret", "-u", "--user", "--api-key"] {
        for val in ["hunter22", "qauser:hunter22", "\"qauser:hunter 22\"", "'qa:pw'", "qa:pw,", "qa:pw\"", "\tqa:pw", "  qa:pw", "-x", "qa:pw;x"] {
            for (b, a) in [("", ""), ("`", "`"), ("[\"", "\"]"), ("x\\n", ""), ("{\"a\": \"", "\"}")] {
                c.check("spaced", &format!("{b}{s} {val}{a}"));
            }
        }
    }
    c.report("s5 starts and spaced values (new forms nearby)");
    assert!(c.lost.is_empty() && c.pw_lower.is_empty());
}

fn show(label: &str, t: &str) {
    let a = kinds(&sig!(main, t));
    let b = kinds(&sig!(coagent_scanner, t));
    println!("ROW {label:<46} | main {a:?} | head {b:?}");
}

#[test]
fn s5_forms_rows() {
    let mut c = Cmp::new();
    let rows: &[(&str, &str)] = &[
        ("argv double", "[\"--password\", \"hunter22\"]"),
        ("argv single", "['--password', 'hunter22']"),
        ("argv mixed quotes", "[\"--password\", 'hunter22']"),
        ("argv no blank", "[\"--password\",\"hunter22\"]"),
        ("argv tab and blanks", "[\"--password\"\t,\t \"hunter22\"]"),
        ("argv blank before comma only", "[\"--password\" ,\"hunter22\"]"),
        ("argv newline after comma", "[\"--password\",\n  \"hunter22\"]"),
        ("argv CRLF after comma", "[\"--password\",\r\n  \"hunter22\"]"),
        ("argv parens (python tuple)", "(\"--password\", \"hunter22\")"),
        ("argv shell words (no comma)", "'--password' 'hunter22'"),
        ("argv empty value", "[\"--password\", \"\"]"),
        ("argv dash value", "[\"--password\", \"-x\"]"),
        ("argv value with blank", "[\"--password\", \"hunter 22\"]"),
        ("argv value unclosed", "[\"--password\", \"hunter22"),
        ("argv flag quote mismatched", "[\"--password', \"hunter22\"]"),
        ("argv double comma", "[\"--password\",, \"hunter22\"]"),
        ("argv -u colon", "[\"-u\", \"qa:hunter22\"]"),
        ("argv -u no colon", "[\"-u\", \"qa\"]"),
        ("argv --user colon", "[\"--user\", \"qa:hunter22\"]"),
        ("argv -p mysql", "[\"mysql\", \"-p\", \"hunter22\"]"),
        ("argv escaped JSON quotes", "{\"args\": \"[\\\"--password\\\", \\\"hunter22\\\"]\"}"),
        ("argv --release (control)", "[\"--release\", \"x\"]"),
        ("argv flag then = value", "[\"--password=hunter22\"]"),
        ("user= colon", "--user=qa:hunter22"),
        ("user= no colon", "--user=root"),
        ("u= colon", "-u=qa:hunter22"),
        ("U= upper", "-U=qa:hunter22"),
        ("USER= upper", "--USER=qa:hunter22"),
        ("user= quoted", "--user=\"qa:hunter22\""),
        ("user= single quoted", "--user='qa:hunter22'"),
        ("user= blank after =", "--user= qa:hunter22"),
        ("user= empty", "--user="),
        ("user= colon only", "--user=:"),
        ("user= url", "--user=https://h:1/x"),
        ("user= in backticks", "`--user=qa:hunter22`"),
        ("user= glued after word", "x--user=qa:hunter22"),
        ("curl --user=", "curl --user=qa:hunter22 https://h"),
        ("JSON \\n before flag", "{\"cmd\": \"a\\n--password hunter22\"}"),
        ("JSON \\t before flag", "{\"cmd\": \"a\\t--secret hunter22\"}"),
        ("JSON \\r before -u", "{\"cmd\": \"a\\r-u qa:hunter22\"}"),
        ("JSON escaped backslash then n (FR-6)", "{\"cmd\": \"a\\\\n--password hunter22\"}"),
        ("JSON \\u000a before flag", "{\"cmd\": \"a\\u000a--password hunter22\"}"),
        ("JSON \\n after flag", "{\"cmd\": \"--password\\nhunter22\"}"),
        ("JSON \\n before -p mysql", "{\"cmd\": \"mysql\\n-phunter22\"}"),
        ("JSON \\n before -p glued then flag", "{\"cmd\": \"mysql a\\n-pX(\\\"--password\\\",\\\"y\\\")\"}"),
        ("Windows path \\n then dash", "C:\\tools\\n-u qa:hunter22"),
        ("JSON \\b before flag (not ruled)", "{\"cmd\": \"a\\b--password hunter22\"}"),
    ];
    for (l, t) in rows { show(l, t); c.check(l, t); }
    c.report("s5 form rows");
    assert!(c.lost.is_empty() && c.pw_lower.is_empty());
}

const B64: [&str; 3] = ["UUFGQUtFMDAwMXF1", "UUFGQUtFMDAwMnF2", "UUFGQUtFMDAwM3F3"];

/// Every separator over {\r, \n, blank, tab, U+0085, U+2028, `a`} up to 4 units: line ends at main vs head,
/// and base64 lines / netrc joined by them, main vs head.
#[test]
fn s5_line_ends_exhaustive() {
    let units = ["\r", "\n", " ", "\t", "\u{85}", "\u{2028}", "a"];
    let mut seps = vec![String::new()];
    let mut all = vec![];
    for _ in 0..6 {
        let mut next = vec![];
        for s in &seps { for u in units { next.push(format!("{s}{u}")); } }
        all.extend(next.iter().cloned());
        seps = next;
    }
    // (1) the line-end sets, on `x<sep>y`, every separator up to 6 units (137 256 texts)
    let (mut dropped_ok, mut dropped_bad, mut added) = (0usize, 0usize, 0usize);
    for s in &all {
        let t = format!("x{s}y");
        let a = le_main::families::qa_line_ends(&t);
        let b = le_head::families::qa_line_ends(&t);
        let tb = t.as_bytes();
        for e in &a {
            if !b.contains(e) {
                // allowed: a `\r` whose following run of \r, blank, tab ends in \n
                let mut k = e.0 + 1;
                while k < tb.len() && matches!(tb[k], b'\r' | b' ' | b'\t') { k += 1; }
                if tb[e.0] == b'\r' && tb.get(k) == Some(&b'\n') { dropped_ok += 1; } else { dropped_bad += 1; println!("LINE END DROPPED NOT IN RULE {t:?} at {e:?}"); }
            }
        }
        for e in &b { if !a.contains(e) { added += 1; println!("LINE END ADDED {t:?} at {e:?}"); } }
    }
    println!("LINEENDS: {} separators; main line ends not at head: {} in a CR run ending in LF, {} other; head line ends not at main: {}", all.len(), dropped_ok, dropped_bad, added);
    // (2) base64 lines and netrc joined by every separator of up to 4 units, plain and behind `> `, with and without a final separator
    let mut c = Cmp::new();
    let mut b64_gain = BTreeMap::new();
    for s in all.iter().filter(|s| s.chars().count() <= 4 && !s.contains('a')) {
        for marker in ["", "> "] {
            for fin in [false, true] {
                let mut t = format!("{marker}{}", B64.join(&format!("{s}{marker}")));
                if fin { t.push_str(s); }
                c.check("b64", &t);
                let mb = has(&sig!(main, &t), "Base64Lines");
                let hb = has(&sig!(coagent_scanner, &t), "Base64Lines");
                *b64_gain.entry((mb, hb)).or_insert(0usize) += 1;
                for net in [format!("machine h{s}login u{s}password qapw0001{s}"), format!("machine h login u{s}{marker}password qapw0001{s}"),
                            format!("machine h login u password qapw0001{s}"), format!("{marker}password qapw0001{s}more{s}")] {
                    c.check("netrc", &net);
                }
            }
        }
    }
    println!("B64 (main, head) Base64Lines counts {b64_gain:?}");
    c.report("s5 line ends: base64 lines and netrc over separators");
    assert!(c.lost.is_empty() && dropped_bad == 0 && added == 0);
}

/// Invisibles inside, before and after `ESC [` codes, at every character boundary of ten made-up shapes.
#[test]
fn s5_codes_and_invisibles() {
    let secrets = [
        ("pem", "-----BEGIN RSA PRIVATE KEY-----\nqaFAKEbodyLINE0001qaFAKEbody\n-----END RSA PRIVATE KEY-----", "PrivateKey"),
        ("url", "postgres://qauser:qaPass0001@db.qa.example/app", "UrlCredentials"),
        ("bearer", "Bearer qaBearer0001x", "AuthScheme"),
        ("header", "Authorization: Negotiate qa0001", "AuthHeader"),
        ("assign", "QA_SECRET_KEY=qaValue0001", "SecretAssignment"),
        ("flag", "--password qapw0001", "PasswordArgument"),
        ("known", "ghp_qaFAKE0000000000000000000000000000ab", "KnownToken"),
        ("long", "qaLongToken0001abcdEFGH2345", "LongToken"),
        ("hex", "0a1b2c3d4e5f60718293", "HexRun"),
        ("b64", "UUFGQUtFMDAwMXF1\nUUFGQUtFMDAwMnF2", "Base64Lines"),
    ];
    let ins = ["\u{1b}[0m", "\u{1b}[\u{200b}0m", "\u{1b}\u{200b}[0m", "\u{1b}[3\u{200b}2m", "\u{200b}\u{1b}[0m", "\u{1b}[0m\u{200b}",
               "\u{1b}[", "\u{1b}[\u{200b}", "\u{1b}[1;\u{180b}", "\u{2066}\u{1b}[31m\u{2069}", "\u{1b}[\u{feff}1;31m", "\u{1b}[12;\u{200b}"];
    let mut c = Cmp::new();
    let mut own_missed: BTreeMap<String, (usize, usize, usize)> = BTreeMap::new();
    for (nm, s, fam) in secrets {
        let bounds: Vec<usize> = (0..=s.len()).filter(|&i| s.is_char_boundary(i)).collect();
        for i in &ins {
            for &p in &bounds {
                for lead in ["", "\u{1b}[32m", "x"] {
                    let t = format!("{lead}{}{i}{}", &s[..p], &s[p..]);
                    c.check(nm, &t);
                    let e = own_missed.entry(format!("{nm} {i:?}")).or_default();
                    e.0 += 1;
                    if !has(&sig!(main, &t), fam) { e.1 += 1; }
                    if !has(&sig!(coagent_scanner, &t), fam) { e.2 += 1; }
                }
            }
        }
    }
    let (mut tot, mut m, mut h) = (0, 0, 0);
    for (k, v) in &own_missed { tot += v.0; m += v.1; h += v.2; if v.2 > 0 { println!("CODES own family not named at head: {k}: {} of {} (main {})", v.2, v.0, v.1); } }
    println!("CODES: {tot} texts; own family not named: main {m}, head {h}");
    c.report("s5 codes and invisibles");
    assert!(c.lost.is_empty());
}

#[test]
fn s7_overflag_corpora() {
    for (label, corpus) in [("EVERYDAY", corpora::EVERYDAY), ("TECHNICAL", corpora::TECHNICAL), ("FLAGS100", flagcorpus::FLAG_SENTENCES)] {
        let (mut fm, mut fh, mut newly, mut unfl, mut changed) = (0, 0, vec![], vec![], vec![]);
        for (i, t) in corpus.iter().enumerate() {
            let a = sig!(main, t);
            let b = sig!(coagent_scanner, t);
            if !a.is_empty() { fm += 1; }
            if !b.is_empty() { fh += 1; }
            if a.is_empty() && !b.is_empty() { newly.push(i); }
            if !a.is_empty() && b.is_empty() { unfl.push(i); }
            if a != b { changed.push(i); }
        }
        println!("OVERFLAG {label}: {} sentences; flagged main {fm} ({:.1} %) head {fh} ({:.1} %); newly flagged {newly:?}; no longer flagged {unfl:?}; verdict (kinds+counts) changed {changed:?}",
            corpus.len(), 100.0 * fm as f64 / corpus.len() as f64, 100.0 * fh as f64 / corpus.len() as f64);
    }
}
