//! QA-SCANNER-CORE generator (independent of the builder's `common`): own RNG, own seed, own pieces.
//! Every secret-shaped string is MADE UP here (markers `qa`, `QA`, counters). Never a real key.
#![allow(dead_code)]

pub struct Rng(u64);
impl Rng {
    pub fn new(seed: u64) -> Self {
        Rng(seed ^ 0x9e37_79b9_7f4a_7c15)
    }
    /// xorshift64* (not the builder's splitmix64)
    pub fn next(&mut self) -> u64 {
        let mut x = self.0;
        x ^= x >> 12;
        x ^= x << 25;
        x ^= x >> 27;
        self.0 = x;
        x.wrapping_mul(0x2545_f491_4f6c_dd1d)
    }
    pub fn below(&mut self, n: usize) -> usize {
        (self.next() % (n as u64)) as usize
    }
    pub fn chance(&mut self, num: usize, den: usize) -> bool {
        self.below(den) < num
    }
    pub fn pick<'a, T>(&mut self, xs: &'a [T]) -> &'a T {
        &xs[self.below(xs.len())]
    }
}

pub const PREFIXES: &[(&str, usize)] = &[
    ("sk-ant-", 20), ("sk-", 20), ("sk_live_", 16), ("sk_test_", 16), ("rk_live_", 16),
    ("rk_test_", 16), ("ghp_", 20), ("gho_", 20), ("ghu_", 20), ("ghs_", 20), ("ghr_", 20),
    ("github_pat_", 20), ("glpat-", 20), ("xoxb-", 15), ("xoxp-", 15), ("xoxa-", 15),
    ("xoxr-", 15), ("xoxs-", 15), ("xapp-", 15), ("AKIA", 20), ("ASIA", 20), ("AIza", 30),
    ("ya29.", 20), ("npm_", 20), ("pypi-", 20), ("hf_", 20), ("SG.", 20), ("shpat_", 20),
    ("dop_v1_", 20),
];

const ALNUM: &[u8] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
const UPPER: &[u8] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZ";
const LOWER: &[u8] = b"abcdefghijklmnopqrstuvwxyz";
const DIGIT: &[u8] = b"0123456789";
const HEX: &[u8] = b"0123456789abcdefABCDEF";
const B64: &[u8] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
const TOKCH: &[u8] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-.";

pub fn chars(r: &mut Rng, set: &[u8], n: usize) -> String {
    (0..n).map(|_| *r.pick(set) as char).collect()
}

/// a body of exactly n chars with a chosen variety (so near-threshold cases hit both sides)
fn body(r: &mut Rng, n: usize) -> String {
    match r.below(6) {
        0 => chars(r, LOWER, n),
        1 => chars(r, DIGIT, n),
        2 => chars(r, UPPER, n),
        3 => chars(r, TOKCH, n),
        4 => chars(r, B64, n),
        _ => chars(r, ALNUM, n),
    }
}

fn bn(r: &mut Rng, t: usize) -> String {
    let n = near(r, t);
    body(r, n)
}

fn cn(r: &mut Rng, set: &[u8], t: usize) -> String {
    let n = near(r, t);
    chars(r, set, n)
}

fn near(r: &mut Rng, t: usize) -> usize {
    (t + r.below(5)).saturating_sub(2).max(1)
}

const WORDS: &[&str] = &[
    "the", "build", "failed", "in", "crates/coagent-daemon/src/engine.rs", "test", "ok", "plan",
    "next", "I", "will", "run", "cargo", "check", "then", "merge", "a", "file", "path", "error:",
    "line", "42", "it", "works", "now", "see", "docs/POLICY.md", "fixed", "and", "pushed",
    "token", "basic", "key", "pass", "auth", "session", "bearer", "digest", "cookie", "password",
    "machine", "login", "mysql", "docker", "htpasswd", "identified", "by", "-p", "-u", "--user",
    "PRIVATE", "-----BEGIN", "-----END", "://", "@", ":", "=", "\"", "'", "`", "eyJ", "café",
    "東京", "🙂", "naïve", "x", "y", "Z",
];

const FORMAT: &[char] = &[
    '\u{00AD}', '\u{180E}', '\u{200B}', '\u{200C}', '\u{200D}', '\u{200E}', '\u{200F}',
    '\u{202A}', '\u{202E}', '\u{2060}', '\u{2064}', '\u{FEFF}', '\u{034F}', '\u{061C}',
    '\u{115F}', '\u{1160}', '\u{2066}', '\u{2069}', '\u{3164}', '\u{FE00}', '\u{FE0F}',
    '\u{FFA0}', '\u{1D173}', '\u{1D17A}', '\u{E0001}', '\u{E007F}', '\u{E0100}', '\u{E01EF}',
];
const ODD: &[&str] = &["\0", "\u{1}", "\u{7}", "\u{1b}", "\u{7f}", "\r", "\r\n", "\u{85}", "\u{2028}", "\u{a0}", "\t", "\u{c}", "\u{b}"];

/// One secret-shaped (or near-threshold not-quite) piece of a family. `f` in 0..10.
pub fn piece(r: &mut Rng, f: usize) -> String {
    match f {
        0 => {
            let kind = *r.pick(&["RSA PRIVATE KEY", "PRIVATE KEY", "OPENSSH PRIVATE KEY", "EC PRIVATE KEY", "ENCRYPTED PRIVATE KEY", "PUBLIC KEY", "CERTIFICATE", "private key"]);
            let pad = if r.chance(1, 8) { " ".repeat(near(r, 110)) } else { String::new() };
            let mut s = format!("-----BEGIN {pad}{kind}-----\n{}", bn(r, 20));
            if r.chance(2, 3) {
                s.push_str(&format!("\n-----END {kind}-----"));
            }
            s
        }
        1 => {
            let scheme = *r.pick(&["postgres", "https", "http", "redis", "amqp", "git+ssh", "mongodb+srv", "s3", ""]);
            let user = if r.chance(1, 4) { String::new() } else { bn(r, 5) };
            let pw = cn(r, b"abcXYZ019@%/:", 6);
            let host = *r.pick(&["db.qa.example", "h", "[::1]", "x.y:80/p?q=1"]);
            let sep = *r.pick(&[":", "", "%3A"]);
            format!("{scheme}://{user}{sep}{pw}@{host}")
        }
        2 => {
            let w = *r.pick(&["Bearer", "bearer", "BASIC", "Basic", "token", "Token", "Digest", "digest"]);
            let ws = *r.pick(&[" ", "\t", "  ", "", "\n", ":"]);
            format!("{w}{ws}{}", bn(r, 3))
        }
        3 => {
            let h = *r.pick(&["Authorization", "proxy-authorization", "Cookie", "Set-Cookie", "X-Api-Key", "x-auth-token", "X-Cookie", "my-cookie"]);
            let sep = *r.pick(&[":", " :", "=", "\t=", " ", ":"]);
            let v = if r.chance(1, 6) { String::new() } else { format!(" {}", bn(r, 4)) };
            format!("{h}{sep}{v}")
        }
        4 => {
            let name = match r.below(6) {
                0 => cn(r, b"ABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789", 3),
                1 => r.pick(&["api_key", "client_secret", "passwd", "auth_token", "PW", "pwd", "my.session", "x-signature", "privateKey", "COOKIE_X"]).to_string(),
                2 => format!("\"{}\"", r.pick(&["password", "apiKey", "token", "name", "secret"])),
                3 => r.pick(&["name", "value", "count", "Path", "url"]).to_string(),
                4 => format!("--{}", r.pick(&["token", "pass", "key"])),
                _ => format!("'{}'", r.pick(&["passw", "x", "KEY"])),
            };
            let op = *r.pick(&["=", ":", " = ", ": ", "==", "=/", ":=", "=:", "!=", "=>"]);
            let val = match r.below(4) {
                0 => format!("\"{}\"", bn(r, 5)),
                1 => format!("'{}'", bn(r, 5)),
                2 => String::new(),
                _ => bn(r, 5),
            };
            format!("{name}{op}{val}")
        }
        5 => match r.below(9) {
            0 => {
                let b = body(r, 6);
                let v = *r.pick(&[&b[..], "-x", "\"q a\"", ""]);
                format!("{} {}", r.pick(&["--password", "-token", "--api-key", "-pass", "--secret", "-pw"]), v)
            }
            1 => format!("{} {}:{}", r.pick(&["-u", "--user", "-U"]), body(r, 4), body(r, 5)),
            2 => {
                let b = body(r, 6);
                let v = *r.pick(&[&b[..], " qa0001", " -x", ""]);
                format!("{} -p{}", r.pick(&["mysql", "mariadb", "sshpass", "MYSQL", "docker login", "podman login", "psql"]), v)
            }
            3 => format!("htpasswd {} f u {}", r.pick(&["-b", "-bc", "-nb", "-B", "-c"]), body(r, 6)),
            4 => format!("{} {}'{}'", r.pick(&["WITH PASSWORD", "password", "IDENTIFIED BY", "identified  by", "PASSWORD"]), r.pick(&["", " "]), bn(r, 4)),
            5 => format!("machine h login u password {}", body(r, 6)),
            6 => format!("password {}", body(r, 6)),
            7 => format!("  password\t{}  ", body(r, 6)),
            _ => format!("docker login -u qa -p {}", body(r, 6)),
        },
        6 => {
            let (p, min) = *r.pick(PREFIXES);
            if r.chance(1, 6) {
                format!("eyJ{}.{}.{}", bn(r, 10), bn(r, 10), bn(r, 8))
            } else {
                let lead = *r.pick(&["", "", "key-", "x_", "a.", "Q", "1"]);
                let rest = near(r, min).saturating_sub(p.len()).max(1);
                format!("{lead}{p}{}", chars(r, TOKCH, rest))
            }
        }
        7 => {
            if r.chance(1, 2) {
                cn(r, b"abcXYZ0123_+=-", 24)
            } else {
                cn(r, b"abcXYZ0123_+=-/", 40)
            }
        }
        8 => {
            let n = near(r, 16);
            let s = chars(r, HEX, n);
            match r.below(4) {
                0 => format!("g{s}"),
                1 => format!("{s}z"),
                _ => s,
            }
        }
        _ => {
            let lines = 1 + r.below(3);
            let eol = *r.pick(&["\n", "\r\n", " \n", "\n\t"]);
            (0..lines).map(|_| cn(r, B64, 12)).collect::<Vec<_>>().join(eol)
        }
    }
}

/// A random text: prose words, pieces of random families, separators, odd and format characters.
pub fn text(r: &mut Rng, max_parts: usize) -> String {
    let n = 1 + r.below(max_parts);
    let mut s = String::new();
    for _ in 0..n {
        match r.below(10) {
            0..=3 => s.push_str(r.pick(WORDS)),
            4..=7 => {
                let f = r.below(10);
                s.push_str(&piece(r, f));
            }
            8 => s.push(*r.pick(FORMAT)),
            _ => s.push_str(r.pick(ODD)),
        }
        let sep = *r.pick(&[" ", " ", " ", "\n", "", "\t", ", ", "\r\n", "(", ")", "\"", "'", "`", "=", ":"]);
        s.push_str(sep);
    }
    s
}
