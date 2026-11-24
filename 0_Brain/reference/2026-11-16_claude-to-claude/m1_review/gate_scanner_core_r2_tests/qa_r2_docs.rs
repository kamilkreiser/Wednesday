//! QA-SCANNER-CORE-R2 item 8: every sentence or row of docs/SCANNER.md the round changed or added,
//! tested once. Expected = what the docs say. Every value is made up.
use coagent_scanner::scan;
fn ks(t: &str) -> Vec<String> { scan(t).findings().iter().map(|f| format!("{:?}", f.kind())).collect() }

#[test]
fn qa_r2_docs_rows() {
    let rows: Vec<(&str, &str, &[&str])> = vec![
        // §2 PasswordArgument cell
        ("§2 htpasswd -b", "htpasswd -b f qa qapw0001", &["PasswordArgument"]),
        ("§2 htpasswd -bc", "htpasswd -bc f qa qapw0001", &["PasswordArgument"]),
        ("§2 htpasswd -Bb", "htpasswd -Bb f qa qapw0001", &["PasswordArgument"]),
        ("§2 htpasswd -B alone not", "htpasswd -B f qa", &[]),
        ("§2 M1 backticks", "`--password qapw0001`", &["PasswordArgument"]),
        ("§2 M1 quotes", "\"--secret qapw0001\"", &["PasswordArgument"]),
        ("§2 M1 brackets", "[--api-key qapw0001]", &["PasswordArgument"]),
        ("§2 M1 JSON string", "{\"a\": \"--passwd qapw0001\"}", &["PasswordArgument"]),
        ("§2 M1 after =", "X=--password qapw0001", &["SecretAssignment", "PasswordArgument"]),
        ("§2 M1 after control byte", "\u{1}--password qapw0001", &["PasswordArgument"]),
        ("§2 M1 after non-ASCII", "é--password qapw0001", &["PasswordArgument"]),
        ("§2 M1 not after letter", "a--password qapw0001", &[]),
        ("§2 M1 not after /", "x/--password qapw0001", &[]),
        // §2 format + terminal paragraph
        ("§2 DI U+180B in a token", "ghp_qaFAKE0001\u{180b}x0x0x0x0x0x0x0x0x0x0", &["KnownToken", "LongToken"]),
        ("§2 DI U+206A in a header", "Author\u{206a}ization: Negotiate qa0001", &["AuthHeader", "SecretAssignment"]),
        ("§2 U+0600 in hex", "0a1b2c3d4e\u{600}5f60718293", &["HexRun"]),
        ("§2 U+FFF9 in bearer", "Bea\u{fff9}rer qaB0001", &["AuthScheme"]),
        ("§2 colour code removed", "\u{1b}[31mBearer qaB0001", &["AuthScheme"]),
        ("§2 cursor move removed", "\u{1b}[2ABearer qaB0001", &["AuthScheme"]),
        ("§2 intermediate byte form", "\u{1b}[1 qBearer qaB0001", &["AuthScheme"]),
        ("§2 no final byte: kept as text", "\u{1b}[1;Bearer", &[]),
        // §2 lines paragraph
        ("§2 base64 lone CR", "UUFGQUtFMDAwMXF1\rUUFGQUtFMDAwMnF2", &["Base64Lines"]),
        ("§2 base64 NEL", "UUFGQUtFMDAwMXF1\u{85}UUFGQUtFMDAwMnF2", &["Base64Lines"]),
        ("§2 base64 LS", "UUFGQUtFMDAwMXF1\u{2028}UUFGQUtFMDAwMnF2", &["Base64Lines"]),
        ("§2 base64 CRLF once", "UUFGQUtFMDAwMXF1\r\nUUFGQUtFMDAwMnF2", &["Base64Lines"]),
        ("§2 base64 behind >>", ">> UUFGQUtFMDAwMXF1\n>> UUFGQUtFMDAwMnF2", &["Base64Lines"]),
        ("§2 netrc lone CR", "machine h\rlogin u\rpassword qapw0001", &["PasswordArgument"]),
        ("§2 netrc behind > ", "> machine h login u password qapw0001", &["PasswordArgument"]),
        ("§2 PEM with LS line ends", "-----BEGIN PRIVATE KEY-----\u{2028}qaFAKEbody\u{2028}-----END PRIVATE KEY-----", &["PrivateKey"]),
        ("§2 PEM header window stays to \\n", "-----BEGIN\u{2028}EC PRIVATE KEY-----\nqaFAKE", &["PrivateKey"]),
        // §4 new misses
        ("§4 JSON base64 not decoded", "\"UUFGQUtFMDAwMXF1\\nUUFGQUtFMDAwMnF2\"", &[]),
        ("§4 unassigned U+2065", "Bea\u{2065}rer qaB0001", &[]),
        ("§4 ESC ( B", "\u{1b}(BBearer qaB0001", &[]),
        // §5 added rows
        ("§5 passed:", "The merge check passed: fmt, clippy, tests, deny.", &["SecretAssignment"]),
        ("§5 RUST_BACKTRACE", "note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace", &["SecretAssignment"]),
        ("§5 export", "export RUST_LOG=coagent=debug", &["SecretAssignment"]),
        ("§5 target dir", "CARGO_TARGET_DIR=tools/target/x cargo test", &["SecretAssignment"]),
        ("§5 const", "const TIMEOUT_MS = 5000;", &["SecretAssignment"]),
        ("§5 long-token", "the long-token rule", &["AuthScheme"]),
        ("§5 token before word", "The token expired, so I asked again", &["AuthScheme"]),
        ("§5 request id", "request deadbeef-0002-4000-8000-00000000f00d returned 500", &["LongToken"]),
        ("§5 cargo test line", "Running tests/t01_flagged.rs (target/debug/deps/t01_flagged-967b2deaabd9a83d)", &["LongToken", "HexRun"]),
        ("§5 WWW-Authenticate", "WWW-Authenticate: Bearer realm=\"coagent\"", &["AuthScheme", "SecretAssignment"]),
        ("§5 bare htpasswd", "htpasswd -b is how you set it", &["PasswordArgument"]),
        ("§5 M1 (-u)", "(-u 1000:1000)", &["PasswordArgument"]),
        ("§5 M1 chown", "chown `-u root:wheel`", &["PasswordArgument"]),
        ("§5 M1 --user", "`--user root:wheel`", &["PasswordArgument"]),
        ("§5 M1 auth-mode", "`--auth-mode login`", &["PasswordArgument"]),
        ("§5 M1 key-file", "`--key-file id_rsa`", &["PasswordArgument"]),
        ("§5 M1 session", "[--session-name demo]", &["PasswordArgument"]),
        ("§5 M1 secret-name", "`--secret-name prod`", &["PasswordArgument"]),
        ("§5 M1 token-file", "`--token-file t.txt`", &["PasswordArgument"]),
        ("§5 M1 passthrough", "`--passthrough on`", &["PasswordArgument"]),
        ("§5 az auth-mode", "az storage blob list --auth-mode login", &["PasswordArgument"]),
        ("§5 htpasswd -B clean", "htpasswd -B .htpasswd qa", &[]),
    ];
    let mut bad = vec![];
    for (l, t, want) in &rows {
        let got = ks(t);
        let ok = got.iter().map(|s| s.as_str()).collect::<Vec<_>>() == *want;
        println!("R2DOC | {l:<36} | want {:<34} | got {:<34} | {}", want.join("+"), got.join("+"), if ok { "ok" } else { "MISMATCH" });
        if !ok { bad.push(*l); }
    }
    println!("R2DOC: {} rows, mismatches {bad:?}", rows.len());
}
