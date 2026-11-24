//! QA-SCANNER-CORE: focused probes (each case printed with what `scan` answered).
use coagent_scanner::{scan, Verdict};

fn show(label: &str, t: &str) -> String {
    let v = scan(t);
    let r = match &v {
        Verdict::Clean => "CLEAN".to_string(),
        Verdict::Flagged(f) => f.iter().map(|x| format!("{:?}", x.kind())).collect::<Vec<_>>().join("+"),
    };
    println!("PROBE | {label:<44} | {r:<40} | {:?}", t.chars().take(90).collect::<String>());
    r
}

fn pem_real_body() -> String {
    // made-up 64-char base64-looking lines with mixed case and digits
    let line = "QUFGQUtFMDAwMXFhRkFLRWJvZHkwMDAyUUFGQUtFMDAwM3FhRkFLRWJvZHkwMDA0";
    format!("-----BEGIN RSA PRIVATE KEY-----\n{line}\n{line}\n{line}\n-----END RSA PRIVATE KEY-----")
}

#[test]
fn qa_probe_flags_wrapped() {
    let vals = ["hunter22", "qaPw0001"];
    let shapes = [
        "--password {v}", "-password {v}", "--passwd {v}", "--secret {v}", "--api-key {v}",
        "-u qauser:{v}", "--user qauser:{v}", "mysql -p{v}", "mysql -p {v}", "sshpass -p {v} ssh h",
    ];
    let wraps: [(&str, &str, &str); 12] = [
        ("space before", "run it with ", ""),
        ("backticks", "`", "`"),
        ("backticks after word+space", "use `", "` now"),
        ("double quotes", "\"", "\""),
        ("single quotes", "'", "'"),
        ("parens", "(", ")"),
        ("brackets", "[", "]"),
        ("JSON string", "{\"args\": \"", "\"}"),
        ("after =", "ARGS=", ""),
        ("after ANSI SGR", "\u{1b}[1m", "\u{1b}[0m"),
        ("after NBSP", "x\u{a0}", ""),
        ("start of text", "", ""),
    ];
    let mut clean = 0;
    let mut n = 0;
    for v in vals {
        for s in shapes {
            let core = s.replace("{v}", v);
            for (w, a, b) in wraps {
                n += 1;
                if show(&format!("flag {w}"), &format!("{a}{core}{b}")) == "CLEAN" {
                    clean += 1;
                }
            }
        }
    }
    println!("PROBE flags: {n} cases, {clean} CLEAN");
}

#[test]
fn qa_probe_realistic_material() {
    let pem = pem_real_body();
    show("pem realistic", &pem);
    show("pem realistic, U+180B in BEGIN", &pem.replacen("-----BEGIN", "-\u{180B}----BEGIN", 1));
    show("pem realistic, U+FFF9 in PRIVATE", &pem.replacen("PRIVATE", "PRI\u{FFF9}VATE", 1));
    show("pem realistic, markdown quote", &format!("> {}", pem.replace('\n', "\n> ")));
    show("pem realistic, JSON escaped", &format!("{{\"private_key\": \"{}\"}}", pem.replace('\n', "\\n")));
    show("pem realistic, lone CR", &pem.replace('\n', "\r"));
    let b64 = "QUFGQUtFMDAwMXFhRkFLRWJvZHkwMDAyUUFGQUtFMDAwM3FhRkFLRWJvZHkwMDA0\nRkFLRWJvZHkwMDA1UUFGQUtFMDAwNnFhRkFLRWJvZHkwMDA3UUFGQUtFMDAwOHFh";
    show("b64 64-wide, alone", b64);
    show("b64 64-wide, markdown quote", &format!("> {}", b64.replace('\n', "\n> ")));
    show("b64 64-wide, lone CR", &b64.replace('\n', "\r"));
    show("b64 64-wide, JSON escaped", &format!("\"{}\"", b64.replace('\n', "\\n")));
    let short = "UUFGQUtFMDAwMXF1\nUUFGQUtFMDAwMnF2\nUUFGQUtFMDAwM3F3";
    show("b64 16-wide x3, alone", short);
    show("b64 16-wide x3, lone CR", &short.replace('\n', "\r"));
    show("b64 16-wide x3, markdown quote", &format!("> {}", short.replace('\n', "\n> ")));
    show("b64 16-wide x3, JSON escaped", &format!("\"{}\"", short.replace('\n', "\\n")));
    show("b64 16-wide x3, prose on first line", &format!("key: {short}"));
    show("bearer long after ANSI", "\u{1b}[32mBearer qaFAKE0001qaFAKE0002qaFAKE0003\u{1b}[0m");
    show("bearer short after ANSI", "\u{1b}[32mBearer qaB0001\u{1b}[0m");
    show("hex 20 after ANSI", "\u{1b}[33m0a1b2c3d4e5f60718293\u{1b}[0m");
    show("hex 32 after ANSI", "\u{1b}[33m0a1b2c3d4e5f607182930a1b2c3d4e5f\u{1b}[0m");
    show("ghp after ANSI", "\u{1b}[33mghp_qaFAKE0001qaFAKE0002qaFAKE0003qaFAKE\u{1b}[0m");
    show("netrc lone CR", "machine h\rlogin u\rpassword qapw0001\r");
    show("netrc multi-line", "machine h\n  login u\n  password qapw0001\n");
    show("netrc one line", "machine h login u password qapw0001");
    show("url in markdown link", "[db](postgres://qa:qaPw0001@db.qa.example/x)");
    show("url user only", "https://qauser@example.com/x");
    show("authorization in JSON", "{\"Authorization\": \"Basic cWE6cWE=\"}");
    show("authorization lower JSON", "{\"authorization\":\"Negotiate qa1\"}");
    show("aws pair, env", "AWS_ACCESS_KEY_ID=AKIAQAFAKE0001QAFAKE\nAWS_SECRET_ACCESS_KEY=qaFAKEqaFAKEqaFAKE0001qaFAKEqaFAKEqaFAKE00");
    show("stripe live short", "sk_live_qaFAKE000001");
    show("slack webhook url", "https://hooks.slack.com/services/T0QAFAKE1/B0QAFAKE2/qaFAKEqaFAKEqaFAKE0001");
    show("discord token-ish", "qaFAKE0001.Gq1aB2.qaFAKEqaFAKEqaFAKEqaFAKE0001qa");
    show("password in yaml quoted", "password: \"hunter22\"");
    show("password in toml", "password = \"hunter22\"");
    show("password in prose colon", "the password is: hunter22");
    show("pin digits", "PIN=4821");
    show("otp prose", "your code is 482913");
    show("twilio-ish SK", "SKqaFAKE0001qaFAKE0002qaFAKE0003qa");
    show("gcp api key", "AIzaQAFAKE0001QAFAKE0002QAFAKE0003QAF");
    show("anthropic-ish", "sk-ant-api03-qaFAKE0001qaFAKE0002qaFAKE");
    show("openai project-ish", "sk-proj-qaFAKE0001qaFAKE0002");
    show("azure conn string", "DefaultEndpointsProtocol=https;AccountName=qa;AccountKey=qaFAKE0001qaFAKE==;EndpointSuffix=core.windows.net");
    show("azure conn string short key", "Server=tcp:qa.database.windows.net;Database=qa;User ID=qa;Password=hunter22;");
    show("jdbc password param", "jdbc:mysql://db/qa?user=qa&password=hunter22");
    show("docker login spaced", "docker login -u qa -p hunter22 registry.qa.example");
    show("docker login --password", "docker login --password hunter22");
    show("podman login -p", "podman login -p hunter22 quay.io");
    show("htpasswd -b", "htpasswd -b .htpasswd qa hunter22");
    show("htpasswd -bc", "htpasswd -bc .htpasswd qa hunter22");
    show("htpasswd -B (bcrypt, no b)", "htpasswd -B .htpasswd qa");
    show("htpasswd mention only", "htpasswd -b is how you set it");
    show("sql create user", "CREATE USER qa WITH PASSWORD 'hunter22';");
    show("sql identified by", "ALTER USER 'qa'@'%' IDENTIFIED BY 'hunter22';");
    show("sql identified by no quotes", "IDENTIFIED BY hunter22");
    show("sql password double quoted", "WITH PASSWORD \"hunter22\"");
    show("sql password empty", "WITH PASSWORD ''");
}

#[test]
fn qa_probe_bound_edges() {
    let m = coagent_scanner::MAX_SCAN_BYTES;
    let f = |n: usize| "a".repeat(n);
    show("exactly bound, clean", &f(m));
    show("bound+1, clean", &f(m + 1));
    show("bound-1 + 2-byte char = bound+1", &format!("{}é", f(m - 1)));
    show("bound-2 + 2-byte char = bound", &format!("{}é", f(m - 2)));
    show("bound-3 + 4-byte char = bound+1", &format!("{}🙂", f(m - 3)));
    show("empty", "");
    show("format chars only", &"\u{200B}".repeat(m / 3));
    // stripping changes length but bound is on the raw text
    let mut t = "\u{200B}".repeat(10_000);
    t.push_str(" ghp_qaFAKE0001qaFAKE0002qaFAKE0003qaFAKE");
    show("30 KB of ZWSP then ghp", &t);
}
