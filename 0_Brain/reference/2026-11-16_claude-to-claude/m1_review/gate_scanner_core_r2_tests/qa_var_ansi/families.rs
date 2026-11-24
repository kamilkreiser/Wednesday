//! The ten pattern families. Each is its own function that records the byte ranges it matched; the
//! scanner keeps only how many there were (and, in one red-control build, the first one).
//!
//! Families copied from `coagent-audit`'s redactor carry the source lines of `redact.rs` at
//! `039b987`; matching is the same (ASCII-only, case-insensitive where it says so; a non-ASCII byte
//! is never part of a token), with the same thresholds. `coagent-audit` is NOT a dependency: a
//! change to the redactor cannot change the scanner. Additions are marked "new".
//!
//! Linear by design: line ends are computed once (`redact.rs:224-226`, gate return A-m3); every
//! per-line question is answered once per line and cached; a scan that consumed a value jumps past
//! it.

use super::{Kind, VERDICT_FAMILIES};

/// What one family found in one text.
#[derive(Debug, Default)]
pub(crate) struct Tally {
    pub(crate) count: u32,
    /// The first matched bytes: only ever filled in the `reason_echoes_text` red control build.
    pub(crate) echo: Option<String>,
}

/// Lower-cased name fragments that make an assignment's value secret (`redact.rs:145-161`).
const SENSITIVE_NAME_PARTS: &[&str] = &[
    "key",
    "secret",
    "token",
    "passw",
    "pwd",
    "credential",
    "auth",
    "private",
    "cookie",
    "session",
    "signature",
    "bearer",
    "pass",
    "pw",
];
/// Words after which the next token is a credential, case-insensitive (`redact.rs:163`).
const AUTH_SCHEMES: &[&str] = &["bearer", "basic", "token", "digest"];
/// Header names whose value (to the end of the line) is a credential, case-insensitive
/// (`redact.rs:165-172`).
const LINE_HEADERS: &[&str] = &[
    "authorization",
    "proxy-authorization",
    "cookie",
    "set-cookie",
    "x-api-key",
    "x-auth-token",
];
/// Known credential prefixes and the minimum length of a token that starts with one
/// (`redact.rs:174-204`).
const TOKEN_PREFIXES: &[(&str, usize)] = &[
    ("sk-ant-", 20),
    ("sk-", 20),
    ("sk_live_", 16),
    ("sk_test_", 16),
    ("rk_live_", 16),
    ("rk_test_", 16),
    ("ghp_", 20),
    ("gho_", 20),
    ("ghu_", 20),
    ("ghs_", 20),
    ("ghr_", 20),
    ("github_pat_", 20),
    ("glpat-", 20),
    ("xoxb-", 15),
    ("xoxp-", 15),
    ("xoxa-", 15),
    ("xoxr-", 15),
    ("xoxs-", 15),
    ("xapp-", 15),
    ("AKIA", 20),
    ("ASIA", 20),
    ("AIza", 30),
    ("ya29.", 20),
    ("npm_", 20),
    ("pypi-", 20),
    ("hf_", 20),
    ("SG.", 20),
    ("shpat_", 20),
    ("dop_v1_", 20),
];
/// `redact.rs:207`: a run of `[A-Za-z0-9_+=-]` this long with a letter and a digit.
pub(crate) const LONG_TOKEN_MIN: usize = 24;
/// `redact.rs:210`: a run of `[A-Za-z0-9+/=_-]` this long with upper, lower and a digit.
pub(crate) const LONG_B64_MIN: usize = 40;
/// `redact.rs:212`: a hexadecimal run this long with a digit and a letter.
pub(crate) const HEX_MIN: usize = 16;
/// `redact.rs:216`: base64-only lines this long, two or more adjacent.
pub(crate) const B64_LINE_MIN: usize = 12;
/// Commands on whose line `-p<value>` / `-p <value>` is a password (`redact.rs:218`, plus
/// `docker login` and `podman login`: new, BACKLOG R2-m4 miss `docker login -p`).
const PASSWORD_P_COMMANDS: &[&str] = &[
    "mysql",
    "mariadb",
    "sshpass",
    "docker login",
    "podman login",
];

/// The text as the families see it.
struct Text<'a> {
    s: &'a str,
    b: &'a [u8],
    lower: Vec<u8>,
    /// `nl[i]` = index of the first `\n` at or after `i` (or the length); one entry past the end.
    nl: Vec<usize>,
    /// For the line shapes (netrc, base64 lines; ADDENDUM 2 m1; PEM keeps its `\n` header window): `gle[i]` = index of the first
    /// line terminator at or after `i` (`\n`, a lone `\r`, U+0085, U+2028; see [`line_term`]) or the
    /// length, and `gls[i]` = the start of the line that holds `i`. One entry past the end each.
    gle: Vec<usize>,
    gls: Vec<usize>,
}

/// The length of the line terminator that starts at `i`, for the line shapes (0 if none): `\n`;
/// a lone `\r` (a `\r` before `\n` is not one: `\r\n` ends a line once); U+0085 (2 bytes); U+2028
/// (3 bytes). ADDENDUM 2 m1.
fn line_term(b: &[u8], i: usize) -> usize {
    match b[i] {
        b'\n' => 1,
        // RED CONTROL `line_end_lf_only`: the broken variant ends a line only at `\n`.
        _ if cfg!(coagent_scanner_red = "line_end_lf_only") => 0,
        b'\r' if b.get(i + 1) != Some(&b'\n') => 1,
        0xC2 if b.get(i + 1) == Some(&0x85) => 2,
        0xE2 if b.get(i + 1) == Some(&0x80) && b.get(i + 2) == Some(&0xA8) => 3,
        _ => 0,
    }
}

/// From `s`, skip blanks and leading markdown quote markers (`>`, `> `, repeated), not past `e`.
/// ADDENDUM 2 m1.
fn skip_quote_markers(b: &[u8], mut s: usize, e: usize) -> usize {
    while s < e && matches!(b[s], b' ' | b'\t' | b'>') {
        s += 1;
    }
    s
}

impl<'a> Text<'a> {
    fn new(s: &'a str) -> Self {
        let b = s.as_bytes();
        let lower = b.iter().map(|c| c.to_ascii_lowercase()).collect();
        // `redact.rs:254-260`
        let mut nl = vec![b.len(); b.len() + 1];
        for i in (0..b.len()).rev() {
            nl[i] = if b[i] == b'\n' { i } else { nl[i + 1] };
        }
        let mut gle = vec![b.len(); b.len() + 1];
        for i in (0..b.len()).rev() {
            gle[i] = if line_term(b, i) > 0 { i } else { gle[i + 1] };
        }
        let mut gls = vec![0; b.len() + 1];
        let (mut cur, mut i) = (0, 0);
        while i < b.len() {
            let n = line_term(b, i);
            if n == 0 {
                gls[i] = cur;
                i += 1;
            } else {
                for slot in &mut gls[i..(i + n).min(b.len())] {
                    *slot = cur;
                }
                cur = (i + n).min(b.len());
                i += n;
            }
        }
        gls[b.len()] = cur;
        Text {
            s,
            b,
            lower,
            nl,
            gle,
            gls,
        }
    }

    /// For the line shapes: the index of the terminator ending the line that holds `from`.
    fn gline_end(&self, from: usize) -> usize {
        self.gle[from.min(self.b.len())]
    }

    /// For the line shapes: the start of the line that holds `i`.
    fn gline_start(&self, i: usize) -> usize {
        self.gls[i.min(self.b.len())]
    }

    /// For the line shapes: the start of the line after the one that ends at `le` (`le` < length).
    fn gline_next(&self, le: usize) -> usize {
        le + line_term(self.b, le).max(1)
    }

    /// The index of the `\n` ending the line that holds `from` (or the length).
    fn line_end(&self, from: usize) -> usize {
        // RED CONTROL `quadratic_line_end`: the broken variant walks to the line end on every call
        // (as every rule of the redactor did before its gate return A-m3).
        if cfg!(coagent_scanner_red = "quadratic_line_end") {
            let mut e = from.min(self.b.len());
            while e < self.b.len() && self.b[e] != b'\n' {
                e += 1;
            }
            return e;
        }
        self.nl[from.min(self.nl.len() - 1)]
    }
}

/// A per-line question ("does this line name one of these words?"), answered once per line. The
/// families ask it at increasing positions, so each line is walked once.
struct LineHas {
    words: &'static [&'static str],
    /// lines as the line shapes see them (`gline_*`), not only `\n`-ended
    general: bool,
    cached: Option<(usize, bool)>,
}

impl LineHas {
    fn new(words: &'static [&'static str]) -> Self {
        LineHas {
            words,
            general: false,
            cached: None,
        }
    }

    fn general(words: &'static [&'static str]) -> Self {
        LineHas {
            general: true,
            ..LineHas::new(words)
        }
    }

    fn at(&mut self, t: &Text, i: usize) -> bool {
        let le = if self.general {
            t.gline_end(i)
        } else {
            t.line_end(i)
        };
        if let Some((end, ans)) = self.cached {
            if end == le {
                return ans;
            }
        }
        let ls = if self.general {
            t.gline_start(i)
        } else {
            let mut ls = i.min(t.b.len());
            while ls > 0 && t.b[ls - 1] != b'\n' {
                ls -= 1;
            }
            ls
        };
        let line = &t.lower[ls..le];
        let ans = self
            .words
            .iter()
            .any(|w| line.windows(w.len()).any(|x| x == w.as_bytes()));
        self.cached = Some((le, ans));
        ans
    }
}

/// Run every counted family on one text.
pub(crate) fn run(s: &str) -> [Tally; 10] {
    let t = Text::new(s);
    let mut out: [Tally; 10] = Default::default();
    for (slot, kind) in out.iter_mut().zip(Kind::FAMILIES) {
        if !VERDICT_FAMILIES.contains(&kind) || red_skipped(kind) {
            continue;
        }
        let mut r = Vec::new();
        match kind {
            Kind::PrivateKey => private_key_blocks(&t, &mut r),
            Kind::UrlCredentials => url_userinfo(&t, &mut r),
            Kind::AuthScheme => auth_schemes(&t, &mut r),
            Kind::AuthHeader => line_headers(&t, &mut r),
            Kind::SecretAssignment => assignments(&t, &mut r),
            Kind::PasswordArgument => password_arguments(&t, &mut r),
            Kind::KnownToken => prefixed_tokens(&t, &mut r),
            Kind::LongToken => long_tokens(&t, &mut r),
            Kind::HexRun => hex_runs(&t, &mut r),
            Kind::Base64Lines => base64_line_blocks(&t, &mut r),
            Kind::TooLarge => {}
        }
        slot.count = u32::try_from(r.len()).unwrap_or(u32::MAX);
        if cfg!(coagent_scanner_red = "reason_echoes_text") {
            slot.echo = r.first().map(|&(a, e)| {
                let (a, e) = (a.min(t.b.len()), e.min(t.b.len()));
                String::from_utf8_lossy(&t.b[a.min(e)..e]).into_owned()
            });
        }
    }
    out
}

/// The red controls of property 1: one family skipped each.
fn red_skipped(kind: Kind) -> bool {
    match kind {
        Kind::PrivateKey => cfg!(coagent_scanner_red = "no_pem"),
        Kind::UrlCredentials => cfg!(coagent_scanner_red = "no_url_userinfo"),
        Kind::AuthScheme => cfg!(coagent_scanner_red = "no_auth_scheme"),
        Kind::AuthHeader => cfg!(coagent_scanner_red = "no_header"),
        Kind::SecretAssignment => cfg!(coagent_scanner_red = "no_assignment"),
        Kind::PasswordArgument => cfg!(coagent_scanner_red = "no_password_flag"),
        Kind::KnownToken => cfg!(coagent_scanner_red = "no_known_token"),
        Kind::LongToken => cfg!(coagent_scanner_red = "no_long_token"),
        Kind::HexRun => cfg!(coagent_scanner_red = "no_hex_run"),
        Kind::Base64Lines => cfg!(coagent_scanner_red = "no_base64_lines"),
        Kind::TooLarge => false,
    }
}

/// `redact.rs:262-270`
fn find_from(hay: &[u8], needle: &[u8], from: usize) -> Option<usize> {
    if from >= hay.len() || needle.is_empty() || needle.len() > hay.len() - from {
        return None;
    }
    hay[from..]
        .windows(needle.len())
        .position(|w| w == needle)
        .map(|p| p + from)
}

/// `redact.rs:276-278`
fn is_word(c: u8) -> bool {
    c.is_ascii_alphanumeric()
}

/// Family `PrivateKey` (`redact.rs:280-301`): `-----BEGIN … PRIVATE …-----` through the matching
/// `-----END …-----`, or to the end of the text when the end line is missing.
fn private_key_blocks(t: &Text, r: &mut Vec<(usize, usize)>) {
    let lower = &t.lower[..];
    let mut i = 0;
    while let Some(p) = find_from(lower, b"-----begin", i) {
        // The header window stays the `\n`-ended line (capped at 120 bytes), as in the redactor: a
        // wider line end can only shrink it (ADDENDUM 2 m1: the differential lost 6 headers with
        // `gline_end`), and a block with lone-CR, U+0085 or U+2028 line ends is caught as it is
        // (`t09_fix_round::m1_line_ends`).
        let le = t.line_end(p);
        let hdr_end = le.min(p + 120);
        if find_from(&lower[..hdr_end], b"private", p).is_some() {
            let end = match find_from(lower, b"-----end", p + 10) {
                Some(e) => match find_from(lower, b"-----", e + 8) {
                    Some(f) => f + 5,
                    None => lower.len(),
                },
                None => lower.len(),
            };
            r.push((p, end));
            i = end;
        } else {
            i = p + 10;
        }
    }
}

/// Family `UrlCredentials` (`redact.rs:303-325`): `scheme://user:password@host`, the user-info
/// part up to the LAST `@` of the URL token.
fn url_userinfo(t: &Text, r: &mut Vec<(usize, usize)>) {
    let b = t.b;
    let mut i = 0;
    while let Some(p) = find_from(b, b"://", i) {
        let start = p + 3;
        let mut end = start;
        while end < b.len()
            && !b[end].is_ascii_whitespace()
            && !matches!(b[end], b'"' | b'\'' | b'<' | b'>' | b'`')
            && b[end] < 0x80
        {
            end += 1;
        }
        if let Some(at) = b[start..end].iter().rposition(|&c| c == b'@') {
            let at = start + at;
            if b[start..at].contains(&b':') && at > start {
                r.push((start, at));
            }
        }
        i = end.max(start);
    }
}

/// `redact.rs:327-336`
fn token_run_end(b: &[u8], from: usize) -> usize {
    let mut q = from;
    while q < b.len()
        && (b[q].is_ascii_alphanumeric()
            || matches!(b[q], b'_' | b'-' | b'.' | b'/' | b'+' | b'=' | b'~' | b':'))
    {
        q += 1;
    }
    q
}

/// Family `AuthScheme` (`redact.rs:338-362`): `Bearer <token>`, `Basic <token>`, `token <token>`,
/// `Digest <…>` (case-insensitive).
fn auth_schemes(t: &Text, r: &mut Vec<(usize, usize)>) {
    let lower = &t.lower[..];
    for scheme in AUTH_SCHEMES {
        let s = scheme.as_bytes();
        let mut i = 0;
        while let Some(p) = find_from(lower, s, i) {
            i = p + 1;
            if p > 0 && is_word(lower[p - 1]) {
                continue;
            }
            let mut q = p + s.len();
            let ws = q;
            while q < lower.len() && (lower[q] == b' ' || lower[q] == b'\t') {
                q += 1;
            }
            if q == ws {
                continue;
            }
            let e = token_run_end(lower, q);
            if e > q {
                r.push((q, e));
            }
        }
    }
}

/// Family `AuthHeader` (`redact.rs:364-386`): `Authorization: …`, `Cookie: …` and similar, with a
/// value on the rest of the line.
fn line_headers(t: &Text, r: &mut Vec<(usize, usize)>) {
    let lower = &t.lower[..];
    for name in LINE_HEADERS {
        let n = name.as_bytes();
        let mut i = 0;
        while let Some(p) = find_from(lower, n, i) {
            i = p + 1;
            if p > 0 {
                // RED CONTROL `slice_mid_char`: the broken variant looks at the previous character
                // through a one-byte string slice, which is not a character boundary after a
                // multi-byte character.
                let prev = if cfg!(coagent_scanner_red = "slice_mid_char") {
                    t.s[p - 1..p]
                        .bytes()
                        .next()
                        .unwrap_or(0)
                        .to_ascii_lowercase()
                } else {
                    lower[p - 1]
                };
                if is_word(prev) || prev == b'-' {
                    continue;
                }
            }
            let mut q = p + n.len();
            while q < lower.len() && (lower[q] == b' ' || lower[q] == b'\t') {
                q += 1;
            }
            if q < lower.len() && (lower[q] == b':' || lower[q] == b'=') {
                let e = t.line_end(q);
                if e > q + 1 {
                    r.push((q + 1, e));
                }
            }
        }
    }
}

/// `redact.rs:388-392`
fn sensitive(lower_name: &[u8]) -> bool {
    SENSITIVE_NAME_PARTS
        .iter()
        .any(|p| lower_name.windows(p.len()).any(|w| w == p.as_bytes()))
}

/// `redact.rs:394-402`
fn env_style(name: &[u8]) -> bool {
    !name.is_empty()
        && name.iter().any(|c| c.is_ascii_uppercase())
        && (name[0].is_ascii_uppercase() || name[0] == b'_')
        && name
            .iter()
            .all(|c| c.is_ascii_uppercase() || c.is_ascii_digit() || *c == b'_')
}

/// `redact.rs:404-429`: the value after a name or flag (quoted to its closing quote on the line,
/// or up to whitespace or `& , ; " '`).
fn value_range(t: &Text, from: usize) -> Option<(usize, usize)> {
    let b = t.b;
    let mut v = from;
    while v < b.len() && (b[v] == b' ' || b[v] == b'\t') {
        v += 1;
    }
    if v >= b.len() {
        return None;
    }
    if b[v] == b'"' || b[v] == b'\'' {
        let q = b[v];
        let le = t.line_end(v + 1).max(v + 1);
        let e = b[v + 1..le]
            .iter()
            .position(|&c| c == q)
            .map_or(le, |p| p + v + 1);
        return (e > v + 1).then_some((v + 1, e));
    }
    let mut e = v;
    while e < b.len()
        && !b[e].is_ascii_whitespace()
        && !matches!(b[e], b'&' | b',' | b';' | b'"' | b'\'')
    {
        e += 1;
    }
    (e > v).then_some((v, e))
}

/// Family `SecretAssignment` (`redact.rs:431-477`): `NAME=value` (env-style upper-case names
/// always; any name containing a sensitive part), `name: value`, `"name": "value"` (sensitive names
/// only for `:`).
fn assignments(t: &Text, r: &mut Vec<(usize, usize)>) {
    let (b, lower) = (t.b, &t.lower[..]);
    // `=`/`:` inside a value already matched are not looked at again (keeps this linear).
    let mut masked_to = 0;
    for p in 0..b.len() {
        let c = b[p];
        if (c != b'=' && c != b':') || p < masked_to {
            continue;
        }
        if p > 0 && matches!(b[p - 1], b'=' | b'!' | b'<' | b'>' | b':') {
            continue;
        }
        if p + 1 < b.len() && matches!(b[p + 1], b'=' | b'/' | b':') {
            continue;
        }
        let mut k = p;
        while k > 0 && (b[k - 1] == b' ' || b[k - 1] == b'\t') {
            k -= 1;
        }
        if k > 0 && (b[k - 1] == b'"' || b[k - 1] == b'\'') {
            k -= 1;
        }
        let end = k;
        while k > 0 && (b[k - 1].is_ascii_alphanumeric() || matches!(b[k - 1], b'_' | b'-' | b'.'))
        {
            k -= 1;
        }
        let mut start = k;
        while start < end && b[start] == b'-' {
            start += 1;
        }
        if start >= end {
            continue;
        }
        let is_secret = (c == b'=' && env_style(&b[start..end])) || sensitive(&lower[start..end]);
        if is_secret {
            if let Some(v) = value_range(t, p + 1) {
                masked_to = v.1;
                r.push(v);
            }
        }
    }
}

/// Family `PasswordArgument`: a password on a command line.
/// - `redact.rs:479-547`: `--password value`, `-token value` (a flag whose name has a sensitive
///   part, then a value); `-u user:pass` / `--user user:pass`; on a `mysql`/`mariadb`/`sshpass`
///   line `-p<value>` and `-p <value>` (and, new, on a `docker login`/`podman login` line).
/// - new (BACKLOG R2-m4 misses): `htpasswd -b` (the password is a positional argument);
///   SQL `PASSWORD '...'` and `IDENTIFIED BY '...'`; a `.netrc` `password <value>` on a line that
///   names `machine`, or on a line holding only `password <value>`.
fn password_arguments(t: &Text, r: &mut Vec<(usize, usize)>) {
    flags(t, r);
    sql_password_literals(t, r);
    netrc_passwords(t, r);
}

/// Whether a flag may start right after byte `c` (ADDENDUM 2 M1): after any byte that is not an ASCII
/// letter or digit, `-`, `_`, `.` or `/`, so a flag inside backticks, quotes, brackets, a JSON string,
/// after `=`, a control byte or a non-ASCII character is seen. (`redact.rs:486` accepts only the
/// start of the text or ASCII whitespace; the redactor misses those texts.)
fn flag_may_start_after(c: u8) -> bool {
    // RED CONTROL `flag_after_space_only`: the broken variant restores the copied rule.
    if cfg!(coagent_scanner_red = "flag_after_space_only") {
        return c.is_ascii_whitespace();
    }
    !(c.is_ascii_alphanumeric() || matches!(c, b'-' | b'_' | b'.' | b'/'))
}

/// `redact.rs:482-547`, plus `htpasswd -b` (new).
fn flags(t: &Text, r: &mut Vec<(usize, usize)>) {
    let (b, lower) = (t.b, &t.lower[..]);
    let mut p_cmd = LineHas::new(PASSWORD_P_COMMANDS);
    let mut htpasswd = LineHas::new(&["htpasswd"]);
    let mut i = 0;
    while i < b.len() {
        if b[i] == b'-' && (i == 0 || flag_may_start_after(b[i - 1])) {
            let mut e = i;
            while e < b.len() && (b[e].is_ascii_alphanumeric() || matches!(b[e], b'_' | b'-')) {
                e += 1;
            }
            let name = &lower[i..e];
            let spaced = e < b.len() && (b[e] == b' ' || b[e] == b'\t');
            if spaced && sensitive(name) {
                if let Some((vs, ve)) = value_range(t, e) {
                    if b[vs] != b'-' {
                        r.push((vs, ve));
                    }
                }
            }
            if spaced && (name == b"-u" || name == b"--user") {
                if let Some((vs, ve)) = value_range(t, e) {
                    if b[vs..ve].contains(&b':') {
                        r.push((vs, ve));
                    }
                }
            }
            let single = name.len() > 1 && !name.starts_with(b"--");
            // new: `htpasswd -b` / `-bc` / `-Bb`: the password follows as a positional argument. The
            // letters are tested as written (ADDENDUM 2 item 5): `-B` (bcrypt) alone is not `-b`.
            let letters = &b[i + 1..e];
            if single
                && letters.iter().all(|c| c.is_ascii_alphabetic())
                && letters.contains(&b'b')
                && htpasswd.at(t, i)
            {
                r.push((i, e));
            }
            if name.starts_with(b"-p") && single && p_cmd.at(t, i) {
                if name.len() > 2 {
                    // glued: -pSECRET (up to the next space)
                    let mut ve = i + 2;
                    while ve < b.len() && !b[ve].is_ascii_whitespace() {
                        ve += 1;
                    }
                    r.push((i + 2, ve));
                    e = e.max(ve);
                } else if spaced {
                    if let Some((vs, ve)) = value_range(t, e) {
                        if b[vs] != b'-' {
                            r.push((vs, ve));
                        }
                    }
                }
            }
            i = e.max(i + 1);
        } else {
            i += 1;
        }
    }
}

/// new: SQL `... PASSWORD 'x'` and `IDENTIFIED BY 'x'` (case-insensitive; a quoted, non-empty
/// value after spaces).
fn sql_password_literals(t: &Text, r: &mut Vec<(usize, usize)>) {
    let lower = &t.lower[..];
    for word in [&b"password"[..], &b"identified by"[..]] {
        let mut i = 0;
        while let Some(p) = find_from(lower, word, i) {
            i = p + 1;
            if p > 0 && is_word(lower[p - 1]) {
                continue;
            }
            let mut q = p + word.len();
            let ws = q;
            while q < lower.len() && (lower[q] == b' ' || lower[q] == b'\t') {
                q += 1;
            }
            if q == ws || q >= lower.len() || !matches!(lower[q], b'\'' | b'"') {
                continue;
            }
            if let Some((vs, ve)) = value_range(t, q) {
                r.push((vs, ve));
                i = i.max(ve);
            }
        }
    }
}

/// new: `.netrc` lines: `machine host login user password value`, or a line holding only
/// `password value`.
fn netrc_passwords(t: &Text, r: &mut Vec<(usize, usize)>) {
    let (b, lower) = (t.b, &t.lower[..]);
    let mut machine = LineHas::general(&["machine "]);
    // (line end, index of the line's first non-blank byte), once per line
    let mut first: Option<(usize, usize)> = None;
    let mut i = 0;
    while let Some(p) = find_from(lower, b"password", i) {
        i = p + 1;
        if p > 0 && !(matches!(lower[p - 1], b' ' | b'\t' | b'>') || t.gline_start(p) == p) {
            continue;
        }
        let e = p + 8;
        if e >= b.len() || !(b[e] == b' ' || b[e] == b'\t') {
            continue;
        }
        let Some((vs, ve)) = value_range(t, e) else {
            continue;
        };
        // the value stops at the line end too (a U+0085 / U+2028 terminator is not ASCII blank)
        let le = t.gline_end(p);
        let ve = ve.min(le);
        if ve <= vs {
            continue;
        }
        if matches!(b[vs.saturating_sub(1)], b'"' | b'\'') {
            continue; // quoted: the SQL rule's shape
        }
        let line_first = match first {
            Some((end, f)) if end == le => f,
            _ => {
                let f = skip_quote_markers(b, t.gline_start(p), le);
                first = Some((le, f));
                f
            }
        };
        let mut after = ve;
        while after < le && (b[after] == b' ' || b[after] == b'\t' || b[after] == b'\r') {
            after += 1;
        }
        let alone = line_first == p && after == le;
        if alone || machine.at(t, p) {
            r.push((vs, ve));
            i = i.max(ve);
        }
    }
}

/// Family `KnownToken` (`redact.rs:549-584`): tokens that start with a known credential prefix,
/// and JSON Web Tokens (`eyJ….….…`).
fn prefixed_tokens(t: &Text, r: &mut Vec<(usize, usize)>) {
    let b = t.b;
    let tok = |c: u8| c.is_ascii_alphanumeric() || matches!(c, b'_' | b'-' | b'.');
    let mut i = 0;
    while i < b.len() {
        if !tok(b[i]) {
            i += 1;
            continue;
        }
        let s = i;
        while i < b.len() && tok(b[i]) {
            i += 1;
        }
        let run = &b[s..i];
        // dots from each position to the end of the run, counted once (keeps this linear)
        let mut dots_after = vec![0usize; run.len() + 1];
        for k in (0..run.len()).rev() {
            dots_after[k] = dots_after[k + 1] + usize::from(run[k] == b'.');
        }
        // a prefix may start the run or follow a separator inside it (`key-ghp_…`)
        for start in 0..run.len() {
            if start > 0 && run[start - 1].is_ascii_alphanumeric() {
                continue;
            }
            let rest = &run[start..];
            let hit = TOKEN_PREFIXES
                .iter()
                .any(|(p, min)| rest.starts_with(p.as_bytes()) && rest.len() >= *min)
                || (rest.starts_with(b"eyJ") && rest.len() >= 30 && dots_after[start] >= 2);
            if hit {
                r.push((s + start, i));
                break;
            }
        }
    }
}

/// Family `LongToken` (`redact.rs:586-626`): long high-variety runs ([`LONG_TOKEN_MIN`],
/// [`LONG_B64_MIN`]).
fn long_tokens(t: &Text, r: &mut Vec<(usize, usize)>) {
    let b = t.b;
    let runs = |is: &dyn Fn(u8) -> bool,
                min: usize,
                ok: &dyn Fn(&[u8]) -> bool,
                r: &mut Vec<(usize, usize)>| {
        let mut i = 0;
        while i < b.len() {
            if !is(b[i]) {
                i += 1;
                continue;
            }
            let s = i;
            while i < b.len() && is(b[i]) {
                i += 1;
            }
            if i - s >= min && ok(&b[s..i]) {
                r.push((s, i));
            }
        }
    };
    runs(
        &|c| c.is_ascii_alphanumeric() || matches!(c, b'_' | b'+' | b'=' | b'-'),
        LONG_TOKEN_MIN,
        &|run| {
            run.iter().any(|c| c.is_ascii_alphabetic()) && run.iter().any(|c| c.is_ascii_digit())
        },
        r,
    );
    runs(
        &|c| c.is_ascii_alphanumeric() || matches!(c, b'_' | b'+' | b'=' | b'-' | b'/'),
        LONG_B64_MIN,
        &|run| {
            run.iter().any(|c| c.is_ascii_uppercase())
                && run.iter().any(|c| c.is_ascii_lowercase())
                && run.iter().any(|c| c.is_ascii_digit())
        },
        r,
    );
}

/// Family `HexRun` (`redact.rs:628-650`): hexadecimal runs of at least [`HEX_MIN`] digits that mix
/// digits and letters, as a whole word.
fn hex_runs(t: &Text, r: &mut Vec<(usize, usize)>) {
    let b = t.b;
    let mut i = 0;
    while i < b.len() {
        if !b[i].is_ascii_hexdigit() || (i > 0 && b[i - 1].is_ascii_alphanumeric()) {
            i += 1;
            continue;
        }
        let s = i;
        while i < b.len() && b[i].is_ascii_hexdigit() {
            i += 1;
        }
        let run = &b[s..i];
        let ends_word = i == b.len() || !b[i].is_ascii_alphanumeric();
        if ends_word
            && run.len() >= HEX_MIN
            && run.iter().any(|c| c.is_ascii_digit())
            && run.iter().any(|c| c.is_ascii_alphabetic())
        {
            r.push((s, i));
        }
    }
}

/// Family `Base64Lines` (`redact.rs:652-689`): two or more adjacent lines made only of base64
/// characters ([`B64_LINE_MIN`] or longer), together holding upper, lower and a digit.
fn base64_line_blocks(t: &Text, r: &mut Vec<(usize, usize)>) {
    let b = t.b;
    let is_b64 = |c: u8| c.is_ascii_alphanumeric() || matches!(c, b'+' | b'/' | b'=');
    let mut block: Vec<(usize, usize)> = Vec::new();
    let flush = |block: &mut Vec<(usize, usize)>, r: &mut Vec<(usize, usize)>| {
        if block.len() >= 2 {
            let all = || block.iter().flat_map(|&(s, e)| b[s..e].iter());
            if all().any(|c| c.is_ascii_uppercase())
                && all().any(|c| c.is_ascii_lowercase())
                && all().any(|c| c.is_ascii_digit())
            {
                r.extend(block.iter().copied());
            }
        }
        block.clear();
    };
    let mut ls = 0;
    while ls <= b.len() {
        let le = t.gline_end(ls);
        let mut e = le;
        let s = skip_quote_markers(b, ls, e);
        while e > s && (b[e - 1] == b' ' || b[e - 1] == b'\t' || b[e - 1] == b'\r') {
            e -= 1;
        }
        if e - s >= B64_LINE_MIN && b[s..e].iter().all(|&c| is_b64(c)) {
            block.push((s, e));
        } else {
            flush(&mut block, r);
        }
        if le >= b.len() {
            break;
        }
        ls = t.gline_next(le);
    }
    flush(&mut block, r);
}
