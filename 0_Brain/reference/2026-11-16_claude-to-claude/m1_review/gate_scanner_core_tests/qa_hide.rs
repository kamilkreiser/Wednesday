//! QA-SCANNER-CORE item 3: hide a secret. Made-up secrets of each family, at every position class
//! and in every wrapping of the QA brief. Prints one row per case; asserts only the controls.
use coagent_scanner::{scan, Kind, MAX_SCAN_BYTES};

fn filler(n: usize) -> String {
    // plain prose, no trigger words, no digits
    let unit = "we looked at the plan and the notes for a while then moved on to other work ";
    let mut s = unit.repeat(n / unit.len() + 1);
    s.truncate(n);
    s
}

pub fn secrets() -> Vec<(Kind, &'static str, String)> {
    vec![
        (Kind::PrivateKey, "pem", "-----BEGIN RSA PRIVATE KEY-----\nqaFAKEbodyLINEqaFAKEbodyLINE\n-----END RSA PRIVATE KEY-----".into()),
        (Kind::UrlCredentials, "url", "postgres://qauser:qaPass0001@db.qa.example/app".into()),
        (Kind::AuthScheme, "bearer", "Bearer qaBearer0001x".into()),
        (Kind::AuthHeader, "header", "Authorization: Negotiate qa0001".into()),
        (Kind::SecretAssignment, "assign", "QA_SECRET_KEY=qaValue0001".into()),
        (Kind::PasswordArgument, "flag", "--password qapw0001".into()),
        (Kind::KnownToken, "ghp", format!("ghp_{}", "qaFAKE0001x".repeat(4).chars().take(36).collect::<String>())),
        (Kind::LongToken, "long", "qa0001AbCdEf0123456789xyzQ".into()),
        (Kind::HexRun, "hex", "0a1b2c3d4e5f60718293".into()),
        (Kind::Base64Lines, "b64", "UUFGQUtFMDAwMXF1\nUUFGQUtFMDAwMnF2".into()),
    ]
}

fn b64(data: &[u8]) -> String {
    const T: &[u8] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    let mut out = String::new();
    for c in data.chunks(3) {
        let n = (c[0] as u32) << 16 | (*c.get(1).unwrap_or(&0) as u32) << 8 | *c.get(2).unwrap_or(&0) as u32;
        for k in 0..4 {
            if k <= c.len() {
                out.push(T[(n >> (18 - 6 * k) & 63) as usize] as char);
            } else {
                out.push('=');
            }
        }
    }
    out
}

/// (placement name, text)
fn placements(s: &str) -> Vec<(String, String)> {
    let m = MAX_SCAN_BYTES;
    let half = m / 2;
    let mut v: Vec<(String, String)> = vec![];
    let mut add = |n: &str, t: String| v.push((n.to_string(), t));
    add("alone", s.to_string());
    add("start", format!("{s} {}", filler(200)));
    add("end", format!("{} {s}", filler(200)));
    {
        let mut t = filler(m - s.len() - 1);
        t.push(' ');
        t.push_str(s);
        assert_eq!(t.len(), m);
        add("ends exactly at the bound", t);
    }
    {
        let mut t = filler(m - s.len() - 1);
        t.push('\n');
        t.push_str(s);
        add("ends at the bound, own line", t);
    }
    {
        let at = half - s.len() / 2;
        let mut t = filler(at - 1);
        t.push(' ');
        t.push_str(s);
        t.push(' ');
        t.push_str(&filler(m - t.len()));
        add("straddles the half", t);
    }
    add("after a 60 KiB line, next line", format!("{}\n{s}", filler(60_000)));
    add("after a 60 KiB line, same line", format!("{} {s}", filler(60_000)));
    add("after ZWSP", format!("see \u{200B}{s} ok"));
    add("after ZWSP glued both sides", format!("see\u{200B}{s}\u{200B}ok"));
    add("after BOM at start", format!("\u{FEFF}{s}"));
    add("after tag chars", format!("x \u{E0041}\u{E0042}{s}"));
    add("inside a multi-byte run", format!("東京東京{s}東京東京"));
    add("between emoji", format!("🙂{s}🙂"));
    add("after NUL", format!("\0{s}\0"));
    add("after ESC", format!("\u{1b}[0m{s}\u{1b}[0m"));
    add("after DEL", format!("\u{7f}{s}"));
    add("CRLF line ends", format!("first line\r\n{}\r\nlast line\r\n", s.replace('\n', "\r\n")));
    add("lone CR line ends", format!("first line\r{}\rlast line\r", s.replace('\n', "\r")));
    add("NEL line ends", format!("first\u{85}{}\u{85}last", s.replace('\n', "\u{85}")));
    add("LS line ends", format!("first\u{2028}{}\u{2028}last", s.replace('\n', "\u{2028}")));
    add("double quotes", format!("\"{s}\""));
    add("single quotes", format!("'{s}'"));
    add("brackets", format!("[{s}]"));
    add("parens", format!("({s})"));
    add("angle brackets", format!("<{s}>"));
    add("backticks", format!("`{s}`"));
    add("JSON value", format!("{{\"v\": \"{}\"}}", s.replace('\n', "\\n")));
    add("JSON value, raw newline", format!("{{\"v\": \"{s}\"}}"));
    add("code fence", format!("```\n{s}\n```"));
    add("code fence, language", format!("```sh\n{s}\n```"));
    add("URL query", format!("https://api.qa.example/v1?access_token={}&x=1", s.replace('\n', "%0A")));
    add("shell single quotes", format!("echo '{s}' | cat"));
    add("shell $'..'", format!("printf $'{}'", s.replace('\n', "\\n")));
    add("heredoc", format!("cat <<'EOF'\n{s}\nEOF"));
    add("markdown quote", format!("> {}", s.replace('\n', "\n> ")));
    add("markdown list", format!("- {}", s.replace('\n', "\n  ")));
    add("indented 4", format!("    {}", s.replace('\n', "\n    ")));
    add("tab indented", format!("\t{}", s.replace('\n', "\n\t")));
    add("base64 of it", b64(s.as_bytes()));
    add("split across two lines", {
        let k = s.len() / 2;
        let k = (k..s.len()).find(|&i| s.is_char_boundary(i)).unwrap_or(k);
        format!("{}\n{}", &s[..k], &s[k..])
    });
    add("trailing punctuation", format!("{s}."));
    add("leading colon", format!("key:{s}"));
    v
}

/// Invisible characters NOT in the scanner's list, inserted inside the secret after its 4th byte.
pub const UNLISTED_INVISIBLE: &[(&str, char)] = &[
    ("U+180B mongolian fvs1", '\u{180B}'),
    ("U+180F mongolian fvs4", '\u{180F}'),
    ("U+FFF9 interlinear anchor", '\u{FFF9}'),
    ("U+1BCA0 shorthand format", '\u{1BCA0}'),
    ("U+17B4 khmer vowel inherent", '\u{17B4}'),
    ("U+0600 arabic number sign", '\u{0600}'),
    ("U+2065 (unassigned)", '\u{2065}'),
];
pub const LISTED_INVISIBLE: &[(&str, char)] = &[
    ("U+200B zwsp", '\u{200B}'),
    ("U+00AD soft hyphen", '\u{00AD}'),
    ("U+2066 isolate", '\u{2066}'),
    ("U+FE0F vs16", '\u{FE0F}'),
    ("U+E0020 tag space", '\u{E0020}'),
    ("U+034F cgj", '\u{034F}'),
];

fn insert_at(s: &str, i: usize, c: char) -> String {
    let i = (i..=s.len()).find(|&k| s.is_char_boundary(k)).unwrap_or(s.len());
    format!("{}{c}{}", &s[..i], &s[i..])
}

fn row(v: &coagent_scanner::Verdict, k: Kind) -> &'static str {
    if v.names(k) {
        "FLAGGED (own family)"
    } else if v.share_flagged() {
        "flagged (other family)"
    } else {
        "CLEAN"
    }
}

#[test]
fn qa_hide_a_secret() {
    let mut clean_rows = vec![];
    let mut n = 0;
    for (k, label, s) in secrets() {
        assert!(scan(&s).names(k), "control: {label} flags alone");
        assert!(scan(&filler(MAX_SCAN_BYTES)) == coagent_scanner::Verdict::Clean, "control: filler clean");
        for (p, t) in placements(&s) {
            let v = scan(&t);
            n += 1;
            let r = row(&v, k);
            println!("HIDE | {label:<7} | {p:<34} | {r}");
            if r == "CLEAN" {
                clean_rows.push(format!("{label} / {p}"));
            }
        }
        for (cn, c) in LISTED_INVISIBLE.iter().chain(UNLISTED_INVISIBLE) {
            for at in [1usize, 4, s.len() / 2] {
                let t = insert_at(&s, at, *c);
                let v = scan(&t);
                n += 1;
                let r = row(&v, k);
                println!("HIDE | {label:<7} | inside@{at:<3} {cn:<27} | {r}");
                if r == "CLEAN" {
                    clean_rows.push(format!("{label} / inside@{at} {cn}"));
                }
            }
        }
    }
    println!("HIDE: {n} cases; CLEAN: {}", clean_rows.len());
    for c in &clean_rows {
        println!("HIDE CLEAN: {c}");
    }
}
