//! QA-SCANNER-CORE-R2: the second check of the fix round. Old = the scanner at b0835a9 (copied
//! into `qa_old/`, `crate::` -> `super::`), new = the crate at the head. Every secret is MADE UP.
#[path = "qa/gen.rs"]
mod gen;
#[path = "qa_old/mod.rs"]
#[allow(dead_code, unused, missing_docs)]
mod old;
#[path = "qa_r2_gen.rs"]
mod r2gen;
use r2gen::{rich_text, pem_header_text};
#[path = "qa_r2_corpus.rs"]
mod corpus;
#[path = "qa_r2_flags_corpus.rs"]
mod flagcorpus;

use coagent_scanner::scan;
use std::collections::BTreeMap;
use std::time::{Duration, Instant};

fn nk(t: &str) -> Vec<String> {
    scan(t).findings().iter().map(|f| format!("{:?}", f.kind())).collect()
}
fn ok(t: &str) -> Vec<String> {
    old::scan(t).findings().iter().map(|f| format!("{:?}", f.kind())).collect()
}
fn show(v: &[String]) -> String {
    if v.is_empty() { "CLEAN".into() } else { v.join("+") }
}

// ---------------------------------------------------------------- M1
const VALS: [&str; 2] = ["hunter22", "qaPw0001"];
const SHAPES: [&str; 10] = [
    "--password {v}", "-password {v}", "--passwd {v}", "--secret {v}", "--api-key {v}",
    "-u qauser:{v}", "--user qauser:{v}", "mysql -p{v}", "mysql -p {v}", "sshpass -p {v} ssh h",
];
const WRAPS: [(&str, &str, &str); 12] = [
    ("space before", "run it with ", ""), ("backticks", "`", "`"), ("backticks after word+space", "use `", "` now"),
    ("double quotes", "\"", "\""), ("single quotes", "'", "'"), ("parens", "(", ")"), ("brackets", "[", "]"),
    ("JSON string", "{\"args\": \"", "\"}"), ("after =", "ARGS=", ""), ("after ANSI SGR", "\u{1b}[1m", "\u{1b}[0m"),
    ("after NBSP", "x\u{a0}", ""), ("start of text", "", ""),
];

#[test]
fn r2_m1_round1_240() {
    let (mut n, mut new_clean, mut old_clean) = (0, 0, 0);
    for v in VALS {
        for s in SHAPES {
            let core = s.replace("{v}", v);
            for (w, a, b) in WRAPS {
                n += 1;
                let t = format!("{a}{core}{b}");
                let (o, nw) = (ok(&t), nk(&t));
                if o.is_empty() { old_clean += 1; }
                if !nw.iter().any(|k| k == "PasswordArgument") {
                    new_clean += 1;
                    println!("M1-240 NOT PasswordArgument | {w} | {} | {t:?}", show(&nw));
                }
            }
        }
    }
    println!("M1-240: {n} cases; old Clean {old_clean}; new without PasswordArgument {new_clean}");
    assert_eq!(n, 240);
}

/// every byte directly before the flag (and the matching closer after the value)
#[test]
fn r2_m1_own_wrappings() {
    let mut before: Vec<(String, String)> = vec![];
    for c in (0x21u8..=0x7e).filter(|c| c.is_ascii_punctuation()) {
        before.push((format!("punct {:?}", c as char), (c as char).to_string()));
    }
    for c in (0u8..0x20).chain([0x7f]) {
        before.push((format!("ctrl 0x{c:02x}"), (c as char).to_string()));
    }
    for (n, s) in [("é", "é"), ("東", "東"), ("🙂", "🙂"), ("NBSP", "\u{a0}"), ("U+0085", "\u{85}"), ("U+2028", "\u{2028}"),
        ("U+2029", "\u{2029}"), ("ZWSP (listed)", "\u{200b}"), ("U+180B (listed now)", "\u{180b}"), ("U+2065 (unlisted)", "\u{2065}"),
        ("ideographic space", "\u{3000}"), ("tab", "\t"), ("CR", "\r"), ("LF", "\n"), ("CRLF", "\r\n"), ("ESC[0m", "\u{1b}[0m"),
        ("ESC(B", "\u{1b}(B"), ("ESC]0;t BEL", "\u{1b}]0;t\u{7}"), ("fullwidth paren", "（"), ("backslash-n literal", "\\n")]
    {
        before.push((n.to_string(), s.to_string()));
    }
    let shapes = &SHAPES[..7];
    let mut clean_by: BTreeMap<String, usize> = BTreeMap::new();
    let mut old_clean = 0;
    let mut n = 0;
    for (label, pre) in &before {
        for lead in ["", "see "] {
            for s in shapes {
                for v in VALS {
                    let core = s.replace("{v}", v);
                    let t = format!("{lead}{pre}{core}");
                    n += 1;
                    if ok(&t).is_empty() { old_clean += 1; }
                    if !nk(&t).iter().any(|k| k == "PasswordArgument") {
                        *clean_by.entry(label.clone()).or_default() += 1;
                        if lead == "see " && v == "hunter22" {
                            println!("M1-OWN not flagged | {label} | {} | {t:?}", show(&nk(&t)));
                        }
                    }
                }
            }
        }
    }
    println!("M1-OWN: {} prefixes x 2 leads x 7 shapes x 2 values = {n}; old Clean {old_clean}; new without PasswordArgument by prefix: {clean_by:?}", before.len());
}

/// wrapped values and closers
#[test]
fn r2_m1_value_forms() {
    for t in [
        "`--password=hunter22`", "`--password \"hunter22\"`", "`--password 'hunter22'`", "\"--password\", \"hunter22\"",
        "[\"--password\", \"hunter22\"]", "`--password\thunter22`", "`--password  hunter22`", "(--password hunter22),",
        "`-u qauser:hunter22`", "`--user=qauser:hunter22`", "<--password hunter22>", "{--secret hunter22}",
        "|--password hunter22|", "*--password hunter22*", "~--password hunter22", "x/--password hunter22",
        "x.--password hunter22", "x_--password hunter22", "x---password hunter22", "a--password hunter22",
    ] {
        println!("M1-VALUE | old {:<40} | new {:<40} | {t:?}", show(&ok(t)), show(&nk(t)));
    }
}

// ---------------------------------------------------------------- over-flags
#[test]
fn r2_overflag_corpora() {
    for (name, set) in [("EVERYDAY", corpus::EVERYDAY), ("TECHNICAL", corpus::TECHNICAL), ("FLAGS100", flagcorpus::FLAG_SENTENCES)] {
        let (mut o, mut nw, mut newly, mut gone) = (0, 0, 0, 0);
        for s in set {
            let (a, b) = (ok(s), nk(s));
            if !a.is_empty() { o += 1; }
            if !b.is_empty() { nw += 1; }
            if a.is_empty() && !b.is_empty() { newly += 1; println!("OVERFLAG NEW   | {name} | {:<30} | {s:?}", show(&b)); }
            if !a.is_empty() && b.is_empty() { gone += 1; println!("OVERFLAG GONE  | {name} | was {:<26} | {s:?}", show(&a)); }
            if !a.is_empty() && !b.is_empty() && a != b { println!("OVERFLAG KINDS | {name} | {} -> {} | {s:?}", show(&a), show(&b)); }
            if !b.is_empty() && name == "FLAGS100" { println!("FLAGS100 FLAG | {:<30} | {s:?}", show(&b)); }
        }
        let n = set.len();
        println!("OVERFLAG {name}: {n} sentences; flagged at b0835a9 {o} ({:.1}%); at head {nw} ({:.1}%); newly flagged {newly}; no longer flagged {gone}",
            100.0 * o as f64 / n as f64, 100.0 * nw as f64 / n as f64);
    }
}

// ---------------------------------------------------------------- two-head differential
fn diff_run(label: &str, n: usize, seed: u64, mk: &dyn Fn(&mut gen::Rng, usize) -> String) -> (usize, usize) {
    let mut r = gen::Rng::new(seed);
    let (mut whole, mut fam_lost) = (0usize, 0usize);
    let mut lost_by: BTreeMap<String, usize> = BTreeMap::new();
    let mut gained_by: BTreeMap<String, usize> = BTreeMap::new();
    let (mut oflag, mut nflag) = (0, 0);
    let mut fam_examples: BTreeMap<String, Vec<String>> = BTreeMap::new();
    for i in 0..n {
        let t = mk(&mut r, i);
        let (a, b) = (ok(&t), nk(&t));
        if !a.is_empty() { oflag += 1; }
        if !b.is_empty() { nflag += 1; }
        if !a.is_empty() && b.is_empty() {
            whole += 1;
            println!("DIFF WHOLE {label} case {i} | old {} | {t:?}", show(&a));
        }
        for k in &a {
            if !b.contains(k) {
                fam_lost += 1;
                *lost_by.entry(k.clone()).or_default() += 1;
                let ex = fam_examples.entry(k.clone()).or_default();
                if ex.len() < 12 { ex.push(format!("case {i} | old {} new {} | {t:?}", show(&a), show(&b))); }
            }
        }
        for k in &b {
            if !a.contains(k) { *gained_by.entry(k.clone()).or_default() += 1; }
        }
    }
    println!("DIFF {label}: seed {seed:#x}, {n} texts; flagged old {oflag} new {nflag}; WHOLE (flagged before, Clean now) {whole}; family-level losses {fam_lost} {lost_by:?}; gains {gained_by:?}");
    for (k, ex) in &fam_examples {
        for e in ex { println!("DIFF FAMILY-LOST {label} {k} | {e}"); }
    }
    (whole, fam_lost)
}

#[test]
fn r2_two_head_differential() {
    let a = diff_run("gen-r1seed", 200_000, 0x0a5c_0ffe_e5ee_d001, &|r, i| gen::text(r, if i % 10 == 0 { 40 } else { 8 }));
    let b = diff_run("gen-r2seed", 100_000, 0x0e2c_0ffe_e5ee_d002, &|r, i| gen::text(r, if i % 10 == 0 { 40 } else { 8 }));
    let c = diff_run("rich", 250_000, 0x0e2c_0ffe_e5ee_d003, &|r, _| rich_text(r));
    let d = diff_run("pem-window", 60_000, 0x0e2c_0ffe_e5ee_d004, &|r, _| pem_header_text(r));
    println!("DIFF TOTAL: 610000 texts; WHOLE {}; family-level losses {}", a.0 + b.0 + c.0 + d.0, a.1 + b.1 + c.1 + d.1);
}

// ---------------------------------------------------------------- targeted hostile cases
fn row(tag: &str, label: &str, t: &str) {
    println!("{tag} | {label:<52} | old {:<34} | new {:<34} | {t:?}", show(&ok(t)), show(&nk(t)));
}

#[test]
fn r2_m1_line_shapes_hostile() {
    let b = ["UUFGQUtFMDAwMXF1", "UUFGQUtFMDAwMnF2", "UUFGQUtFMDAwM3F3"];
    let mixes = [
        ("LF, CR, NEL mixed", format!("{}\n{}\r{}\u{85}{}", b[0], b[1], b[2], b[0])),
        ("CR, LS, CRLF mixed", format!("{}\r{}\u{2028}{}\r\n{}", b[0], b[1], b[2], b[1])),
        ("CR CR LF (double-converted CRLF)", format!("{}\r\r\n{}\r\r\n{}", b[0], b[1], b[2])),
        ("CR space CR LF", format!("{}\r \r\n{}\r \r\n{}", b[0], b[1], b[2])),
        ("CR tab LF", format!("{}\r\t\n{}\r\t\n{}", b[0], b[1], b[2])),
        ("CRLF control", format!("{}\r\n{}\r\n{}", b[0], b[1], b[2])),
        ("trailing CR then LF control", format!("{}\r\n{}\r\n{}\r\n", b[0], b[1], b[2])),
        ("U+2029 paragraph separator", format!("{}\u{2029}{}\u{2029}{}", b[0], b[1], b[2])),
        ("VT and FF", format!("{}\u{b}{}\u{c}{}", b[0], b[1], b[2])),
        ("quote marker > glued", format!(">{}\n>{}\n>{}", b[0], b[1], b[2])),
        ("quote marker with CR ends", format!("> {}\r> {}\r> {}", b[0], b[1], b[2])),
        ("nested quote with tabs", format!(">\t>\t{}\n>\t>\t{}", b[0], b[1])),
        ("> inside a base64 line (not a marker)", format!("UUFGQUtF>MDAwMXF1\nUUFGQUtF>MDAwMnF2")),
        ("> at the end of lines", format!("{}>\n{}>\n{}>", b[0], b[1], b[2])),
        ("markdown list", format!("- {}\n  {}\n  {}", b[0], b[1], b[2])),
        ("JSON \\n escapes (documented miss)", format!("\"{}\\n{}\\n{}\"", b[0], b[1], b[2])),
        ("ESC colour at each line start", format!("\u{1b}[32m{}\n\u{1b}[32m{}\n\u{1b}[32m{}", b[0], b[1], b[2])),
        ("64-wide x2 with CR CR LF (LongToken control)", format!("{0}\r\r\n{0}", "UUFGQUtFMDAwMXF1UUFGQUtFMDAwMnF2UUFGQUtFMDAwM3F3UUFGQUtFMDAwNHF4")),
    ];
    for (l, t) in &mixes { row("M1LINE", l, t); }
    let netrc = [
        ("netrc mixed ends", "machine h\rlogin u\u{85}password qapw0001\u{2028}".to_string()),
        ("netrc machine then CR on one LF line", "machine h\rlogin u password qapw0001\n".to_string()),
        ("netrc machine then LS on one LF line", "machine h\u{2028}login u password qapw0001\n".to_string()),
        ("netrc one line", "machine h login u password qapw0001".to_string()),
        ("netrc CR CR LF", "machine h\r\r\nlogin u\r\r\npassword qapw0001\r\r\n".to_string()),
        ("netrc > glued", ">password qapw0001".to_string()),
        ("netrc value starting with >", "password >qapw0001".to_string()),
        ("netrc a>password mid-line", "a>password qapw0001".to_string()),
        ("netrc password then CR then text", "password qapw0001\rmore".to_string()),
        ("netrc password then NEL then text", "password qapw0001\u{85}more".to_string()),
        ("netrc value ends at NEL glued", "machine h password qapw0001\u{85}".to_string()),
        ("netrc password at text start after CR", "\rpassword qapw0001".to_string()),
        ("prose: the password is in the vault", "> the password is in the vault".to_string()),
        ("prose: > password reset done", "> password reset done".to_string()),
        ("prose quote line: password policy", "> password policy\n> is strict".to_string()),
    ];
    for (l, t) in &netrc { row("M1NETRC", l, t); }
}

#[test]
fn r2_m2_ansi_hostile() {
    let cases: Vec<(&str, String)> = vec![
        ("round-1: bearer short after ANSI", "\u{1b}[32mBearer qaB0001\u{1b}[0m".into()),
        ("round-1: hex 20 after ANSI", "\u{1b}[33m0a1b2c3d4e5f60718293\u{1b}[0m".into()),
        ("ESC [ with no end, then a secret", "\u{1b}[1;2;3Bearer qaB0001".into()),
        ("ESC [ no final at text end", "Bearer qaB0001 \u{1b}[1;2;".into()),
        ("nested: ESC [ ESC [31m", "\u{1b}[\u{1b}[31mBearer qaB0001".into()),
        ("overlap: ESC [3 ESC [1m", "\u{1b}[3\u{1b}[1mBearer qaB0001".into()),
        ("two codes glued", "\u{1b}[1m\u{1b}[31mBearer qaB0001".into()),
        ("ESC inside a secret: hex split by a colour code", "0a1b2c3d4e\u{1b}[0m5f60718293".into()),
        ("ESC inside a secret: ghp split", format!("ghp_{}\u{1b}[0m{}", "qaFAKE0001x0x0x0x0", "x0x0x0x0x0x0x0x0x0")),
        ("ESC inside a flag name", "--pass\u{1b}[0mword hunter22".into()),
        ("ESC joins two halves into a false hex run", "deadbeef01\u{1b}[0m23456789 ok".into()),
        ("ESC joins two words into a long token", "build2024\u{1b}[1mStatusOKfinal99".into()),
        ("CSI eats leading hex digits + listed char inside (RE-1)", "\u{1b}[0123456789ab\u{200b}cdef0123".into()),
        ("RE-1 without the listed char (control)", "\u{1b}[0123456789abcdef0123".into()),
        ("CSI eats '--p' of a flag + listed char inside (RE-2)", "\u{1b}[--pass\u{200b}word hunter22".into()),
        ("RE-2 without the listed char (control)", "\u{1b}[--password hunter22".into()),
        ("colour reset glued after hex + listed char inside (RE-3)", "0a1b2c3d\u{200b}4e5f60718293\u{1b}[0mzz".into()),
        ("listed char inside the CSI: ESC [3 ZWSP 2m", "\u{1b}[3\u{200b}2mBearer qaB0001".into()),
        ("listed char between ESC and [", "\u{1b}\u{200b}[32mBearer qaB0001".into()),
        ("ESC ( B (documented miss)", "\u{1b}(BBearer qaB0001".into()),
        ("OSC title then secret", "\u{1b}]0;t\u{7}Bearer qaB0001".into()),
        ("8-bit CSI U+009B", "\u{9b}32mBearer qaB0001".into()),
        ("SGR with colon params", "\u{1b}[38:5:208mBearer qaB0001".into()),
        ("private mode ESC [?25l", "\u{1b}[?25lBearer qaB0001".into()),
        ("ESC [ final is a letter of the secret", "\u{1b}[Bearer qaB0001".into()),
        ("ESC [ eats 'B' of Bearer (control: raw view)", "\u{1b}[1Bearer qaB0001".into()),
        ("PEM header glued to colour", "\u{1b}[33m-----BEGIN RSA PRIVATE KEY-----\nqaFAKE\n-----END RSA PRIVATE KEY-----".into()),
        ("colour inside PEM header", "-----BEGIN \u{1b}[0mRSA PRIVATE KEY-----\nqaFAKE".into()),
        ("netrc behind colour", "\u{1b}[2mmachine h login u password qapw0001".into()),
        ("htpasswd behind colour", "\u{1b}[1mhtpasswd -b f u qapw0001".into()),
        ("lone ESC at end", "Bearer qaB0001\u{1b}".into()),
        ("ESC [ alone", "\u{1b}[".into()),
        ("ESC [ then multibyte", "\u{1b}[東Bearer qaB0001".into()),
    ];
    for (l, t) in &cases { row("M2", l, t); }
}

/// each newly listed invisible character at EVERY character boundary of a short secret of each family
#[test]
fn r2_m3_every_position() {
    let secrets: Vec<(&str, String)> = vec![
        ("PrivateKey", "-----BEGIN RSA PRIVATE KEY-----\nqaFAKEbodyLINEqaFAKEbodyLINE\n-----END RSA PRIVATE KEY-----".into()),
        ("UrlCredentials", "postgres://qauser:qaPass0001@db.qa.example/app".into()),
        ("AuthScheme", "Bearer qaBearer0001x".into()),
        ("AuthHeader", "Authorization: Negotiate qa0001".into()),
        ("SecretAssignment", "QA_SECRET_KEY=qaValue0001".into()),
        ("PasswordArgument", "--password qapw0001".into()),
        ("KnownToken", format!("ghp_{}", "qaFAKE0001x".repeat(4).chars().take(36).collect::<String>())),
        ("LongToken", "qa0001AbCdEf0123456789xyzQ".into()),
        ("HexRun", "0a1b2c3d4e5f60718293".into()),
        ("Base64Lines", "UUFGQUtFMDAwMXF1\nUUFGQUtFMDAwMnF2".into()),
        ("PasswordArgument", "machine h login u password qapw0001".into()),
        ("PasswordArgument", "htpasswd -b f u qapw0001".into()),
    ];
    let chars: Vec<char> = ['\u{17B4}', '\u{17B5}', '\u{180B}', '\u{180C}', '\u{180D}', '\u{180F}', '\u{FFF9}', '\u{FFFA}', '\u{FFFB}',
        '\u{1BCA0}', '\u{1BCA1}', '\u{1BCA2}', '\u{1BCA3}', '\u{0600}', '\u{0601}', '\u{0602}', '\u{0603}', '\u{0604}', '\u{0605}',
        '\u{206A}', '\u{206B}', '\u{206C}', '\u{206D}', '\u{206E}', '\u{206F}', '\u{E0001}'].to_vec();
    let mut n = 0;
    let mut missed: BTreeMap<String, usize> = BTreeMap::new();
    for (k, s) in &secrets {
        assert!(nk(s).iter().any(|x| x == k), "control {k}");
        for c in &chars {
            for i in (0..=s.len()).filter(|&i| s.is_char_boundary(i)) {
                n += 1;
                let t = format!("{}{c}{}", &s[..i], &s[i..]);
                if !nk(&t).iter().any(|x| x == k) {
                    *missed.entry(format!("{k} U+{:04X}", *c as u32)).or_default() += 1;
                    if missed.len() < 30 { println!("M3 MISS | {k} | U+{:04X} at {i} | {t:?}", *c as u32); }
                }
            }
        }
    }
    println!("M3: {} chars x every boundary of {} secrets = {n} cases; missed {} {missed:?}", chars.len(), secrets.len(), missed.values().sum::<usize>());
    // every assigned Default_Ignorable_Code_Point (Unicode 15/16 DerivedCoreProperties, written from the published list)
    let di: &[(u32, u32)] = &[(0x00AD, 0x00AD), (0x034F, 0x034F), (0x061C, 0x061C), (0x115F, 0x1160), (0x17B4, 0x17B5), (0x180B, 0x180F),
        (0x200B, 0x200F), (0x202A, 0x202E), (0x2060, 0x2064), (0x2066, 0x206F), (0x3164, 0x3164), (0xFE00, 0xFE0F), (0xFEFF, 0xFEFF),
        (0xFFA0, 0xFFA0), (0x1BCA0, 0x1BCA3), (0x1D173, 0x1D17A), (0xE0001, 0xE0001), (0xE0020, 0xE007F), (0xE0100, 0xE01EF)];
    let mut not_listed = vec![];
    let mut total = 0;
    for &(a, b) in di {
        for cp in a..=b {
            total += 1;
            let c = char::from_u32(cp).unwrap();
            if !coagent_scanner::is_format_char(c) { not_listed.push(format!("U+{cp:04X}")); }
        }
    }
    println!("M3 DI: {total} assigned Default_Ignorable code points; not on is_format_char: {not_listed:?}");
    // listed but NOT Default_Ignorable (added beyond the set), and unassigned points inside listed ranges
    let extra: Vec<String> = (0u32..0x110000).filter_map(char::from_u32)
        .filter(|c| coagent_scanner::is_format_char(*c))
        .filter(|c| !di.iter().any(|&(a, b)| (a..=b).contains(&(*c as u32))))
        .map(|c| format!("U+{:04X}", c as u32)).collect();
    println!("M3 listed beyond the assigned DI set: {} {:?}", extra.len(), extra);
}

/// htpasswd flag letters in every case and order
#[test]
fn r2_item5_htpasswd_letters() {
    let letters = ['b', 'B', 'c', 'C', 'n', 'm', 'd', 's', 'p', 'D', 'v', 'i'];
    let (mut n, mut wrong) = (0, 0);
    let mut combos: Vec<String> = letters.iter().map(|c| c.to_string()).collect();
    for a in letters { for b in letters { if a != b { combos.push(format!("{a}{b}")); } } }
    for a in ['b', 'B', 'c', 'n'] { for b in ['b', 'B', 'c', 'n'] { for c in ['b', 'B', 'c', 'n'] {
        if a != b && b != c && a != c { combos.push(format!("{a}{b}{c}")); } } } }
    for f in &combos {
        for tail in [" .htpasswd qa qapw0001", " .htpasswd qa"] {
            let t = format!("htpasswd -{f}{tail}");
            n += 1;
            let got = nk(&t).iter().any(|k| k == "PasswordArgument");
            let want = f.contains('b');
            if got != want {
                wrong += 1;
                println!("ITEM5 WRONG | -{f} | want {want} got {got} | {t:?}");
            }
        }
    }
    for t in ["HTPASSWD -B f u", "htpasswd -B -b f u qapw0001", "htpasswd -b5 f u x", "htpasswd -B5 f u", "`htpasswd -B f u`", "(htpasswd -Bb f u x)", "htpasswd -C 10 -B f u", "htpasswd -nbB u qapw0001"] {
        row("ITEM5", "extra", t);
    }
    println!("ITEM5: {n} cases (flagged iff the letters hold a lower-case b), wrong {wrong}");
}

// ---------------------------------------------------------------- time
fn smallest_of_five(t: &str) -> Duration {
    (0..5).map(|_| { let a = Instant::now(); std::hint::black_box(scan(std::hint::black_box(t))); a.elapsed() }).min().unwrap()
}
fn fill_to(unit: &str, len: usize) -> String {
    let mut s = String::with_capacity(len + unit.len());
    while s.len() + unit.len() <= len { s.push_str(unit); }
    while s.len() < len { s.push(' '); }
    s
}
fn hostile(m: usize) -> Vec<(&'static str, String)> {
    vec![
        ("ESC [ + one long digit run, no final", format!("\u{1b}[{}", "0".repeat(m - 2))),
        ("ESC [ + one long intermediate run, no final", format!("\u{1b}[{}", "!".repeat(m - 2))),
        ("ESC [ repeated", fill_to("\u{1b}[", m)),
        ("ESC repeated", fill_to("\u{1b}", m)),
        ("ESC [0 repeated (each ends at the next ESC)", fill_to("\u{1b}[0", m)),
        ("ESC [ param/intermediate alternating, no final", format!("\u{1b}[{}", "0 ".repeat((m - 2) / 2))),
        ("ESC [ + params + listed char (sequence kept), repeated", fill_to("\u{1b}[12\u{200b}", m)),
        ("CSI glued to hex, repeated", fill_to("\u{1b}[0m0a1b2c3d4e5f6071", m)),
        ("CR CR LF repeated", fill_to("\r\r\n", m)),
        ("NEL repeated", fill_to("\u{85}", m)),
        ("LS repeated", fill_to("\u{2028}", m)),
        ("> repeated, no space, one line", fill_to(">", m)),
        ("> + base64 line, alternating", fill_to("> UUFGQUtFMDAwMXF1\n", m)),
        ("long > run then password x, repeated lines", fill_to(&format!("{}password x\n", ">".repeat(500)), m)),
        (">password x repeated on one line", fill_to(">password x ", m)),
        ("password x + CR repeated", fill_to("password x\r", m)),
        ("machine on one LF line, password after CR, repeated", fill_to("machine h\rpassword x ", m)),
        ("(--key \" repeated (wrapped flags, quoted value)", fill_to("(--key \"", m)),
        ("(--key ' / (--key \" alternating", fill_to("(--key '(--key \"", m)),
        ("(-u a:b) repeated", fill_to("(-u a:b)", m)),
        ("(-p on a mysql line, glued", format!("mysql {}", fill_to("(-p", m - 6))),
        ("`-` after every byte", fill_to("x(-", m)),
        ("htpasswd + `-Bb` repeated", format!("htpasswd {}", fill_to("`-Bb ", m - 9))),
        ("U+1BCA0 repeated (4-byte listed)", fill_to("\u{1BCA0}", m)),
        ("U+17B4 every other char", fill_to("a\u{17B4}", m)),
        ("U+0600 between hex digits", fill_to("0\u{0600}a\u{0600}", m)),
        ("ESC [0m + U+180B + CR mixed", fill_to("\u{1b}[0m\u{180b}\r>", m)),
    ]
}

#[test]
fn r2_hostile_timed() {
    let m = coagent_scanner::MAX_SCAN_BYTES;
    let mut worst = Duration::ZERO;
    for (l, t) in hostile(m) {
        assert!(t.len() <= m, "{l} {}", t.len());
        let r = std::panic::catch_unwind(|| scan(&t));
        assert!(r.is_ok(), "{l} panicked");
        let d = smallest_of_five(&t);
        worst = worst.max(d);
        println!("TIME | {l:<56} | {:>6} B | {:>8.2} ms | {}", t.len(), d.as_secs_f64() * 1e3, show(&nk(&t)));
    }
    println!("TIME worst {:.2} ms", worst.as_secs_f64() * 1e3);
}

#[test]
fn r2_hostile_doubling() {
    for (i, (l, _)) in hostile(64).into_iter().enumerate() {
        let mut ms = vec![];
        for kib in [8usize, 16, 32, 64] {
            let t = &hostile(kib * 1024)[i].1;
            ms.push(smallest_of_five(t).as_secs_f64() * 1e3);
        }
        println!("DOUBLE | {l:<56} | 8K {:.3} | 16K {:.3} | 32K {:.3} | 64K {:.3} ms | 64K/8K = {:.1}", ms[0], ms[1], ms[2], ms[3], ms[3] / ms[0].max(1e-6));
    }
}
