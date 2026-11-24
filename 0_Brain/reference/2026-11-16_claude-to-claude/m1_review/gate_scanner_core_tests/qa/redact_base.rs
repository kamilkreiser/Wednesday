//! Previews and redaction (D12, 04 §6.5).
//!
//! The `full` tier carries a short redacted preview only: the raw content is redacted FIRST, then
//! truncated to [`PREVIEW_MAX_CHARS`] characters or [`PREVIEW_MAX_LINES`] lines, whichever is shorter.
//! Raw content is never stored by this crate; only the preview is.
//!
//! **Pattern redaction misses things.** [`PatternRedactor`] masks text that LOOKS like a credential
//! (the shapes listed in [`patterns`]); a secret that does not look like one — a plain word used as a
//! password, a token glued to other letters, an unusual encoding, a secret split across lines, a
//! format nobody listed — passes through unchanged. It also masks things that are not secrets (hashes,
//! UUIDs, `PATH=`-style assignments): it is deliberately conservative. Treat it as a seatbelt, never as
//! a guarantee; the owner's exclusions and the share level are the real controls.

/// PROPOSED, NOT RULED (04 §6.5: "the first 240 characters or 3 lines after redaction, whichever is
/// shorter, fixed in M2"): the most Unicode characters a preview may hold.
pub const PREVIEW_MAX_CHARS: usize = 240;
/// PROPOSED, NOT RULED (04 §6.5): the most lines a preview may hold.
pub const PREVIEW_MAX_LINES: usize = 3;
/// Only this prefix of the raw content is examined (bytes, cut back to a character boundary). It is
/// far longer than any preview, so every byte that can reach a preview is redacted with its full
/// context; it bounds the work on huge outputs.
pub const REDACT_WINDOW_BYTES: usize = 65_536;
/// What a masked span is replaced with.
pub const MASK: &str = "[REDACTED]";
/// Largest summary tier body accepted, after redaction (bytes).
pub const MAX_SUMMARY_BYTES: usize = 4096;
/// Largest full-tier body accepted from a peer (bytes): 240 characters of at most 4 bytes.
pub const MAX_PREVIEW_BYTES: usize = PREVIEW_MAX_CHARS * 4;

/// Something that removes secrets from text. Implementations must be pure functions of the input.
pub trait Redactor: Send + Sync {
    /// The text with whatever looks secret replaced.
    fn redact(&self, text: &str) -> String;
}

/// The conservative default: masks every span matched by [`patterns`].
#[derive(Debug, Clone, Copy, Default)]
pub struct PatternRedactor;

impl Redactor for PatternRedactor {
    fn redact(&self, text: &str) -> String {
        // Gate return A-m2: invisible format characters (zero-width space and joiners, soft hyphen,
        // bidi controls, BOM) are removed first, so they cannot split a token or a name.
        // RED CONTROL `redact_keep_format_chars`.
        if false {
            return apply_mask(text, &patterns::find(text));
        }
        let clean = strip_format_chars(text);
        apply_mask(&clean, &patterns::find(&clean))
    }
}

/// Unicode format characters removed before matching (a sample of category Cf that is invisible in
/// terminals and editors).
pub fn is_format_char(c: char) -> bool {
    matches!(c,
        '\u{00AD}' | '\u{180E}' | '\u{200B}'..='\u{200F}' | '\u{202A}'..='\u{202E}'
        | '\u{2060}'..='\u{2064}' | '\u{FEFF}')
}

/// The text without [`is_format_char`] characters.
pub fn strip_format_chars(text: &str) -> String {
    text.chars().filter(|c| !is_format_char(*c)).collect()
}

/// Truncate already-redacted text to the preview limits.
pub fn truncate(text: &str) -> String {
    // RED CONTROL `preview_241`: the broken variant allows one character too many.
    let max_chars = if false {
        PREVIEW_MAX_CHARS + 1
    } else {
        PREVIEW_MAX_CHARS
    };
    let mut out = String::new();
    let mut lines = 1;
    for (n, c) in text.chars().enumerate() {
        if n == max_chars {
            break;
        }
        if c == '\n' {
            // RED CONTROL `preview_no_line_cap`: the broken variant ignores the line limit.
            if lines == PREVIEW_MAX_LINES && !false {
                break;
            }
            lines += 1;
        }
        out.push(c);
    }
    out
}

/// The preview of raw content: redact (within [`REDACT_WINDOW_BYTES`]), then [`truncate`].
pub fn preview(redactor: &dyn Redactor, raw: &str) -> String {
    let mut end = raw.len().min(REDACT_WINDOW_BYTES);
    while !raw.is_char_boundary(end) {
        end -= 1;
    }
    truncate(&redactor.redact(&raw[..end]))
}

/// Replace each byte range with [`MASK`] (ranges are merged first; boundaries are moved outwards to
/// character boundaries, so this never panics on any input).
pub fn apply_mask(text: &str, ranges: &[(usize, usize)]) -> String {
    let mut rs: Vec<(usize, usize)> = ranges
        .iter()
        .map(|&(s, e)| {
            let (mut s, mut e) = (s.min(text.len()), e.min(text.len()));
            while !text.is_char_boundary(s) {
                s -= 1;
            }
            while !text.is_char_boundary(e) {
                e += 1;
            }
            (s, e)
        })
        .filter(|(s, e)| s < e)
        .collect();
    rs.sort_unstable();
    let mut out = String::with_capacity(text.len());
    let mut pos = 0;
    let mut i = 0;
    while i < rs.len() {
        let (s, mut e) = rs[i];
        i += 1;
        while i < rs.len() && rs[i].0 <= e {
            e = e.max(rs[i].1);
            i += 1;
        }
        if s >= pos {
            out.push_str(&text[pos..s]);
        }
        out.push_str(MASK);
        pos = pos.max(e);
    }
    out.push_str(&text[pos..]);
    out
}

/// The credential-shaped patterns the default redactor masks. Each function returns byte ranges.
/// Matching is ASCII-only and case-insensitive where it says so; non-ASCII bytes are never part of a
/// token.
pub mod patterns {
    /// Lower-cased name fragments that make an assignment's value secret (`NAME=value`,
    /// `name: value`, `"name": "value"`, `--name value`).
    pub const SENSITIVE_NAME_PARTS: &[&str] = &[
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
        // gate return A-m2
        "pass",
        "pw",
    ];
    /// Words after which the next token is a credential (case-insensitive): `Bearer x`, `token x`.
    pub const AUTH_SCHEMES: &[&str] = &["bearer", "basic", "token", "digest"];
    /// Header names whose whole value (to the end of the line) is masked (case-insensitive).
    pub const LINE_HEADERS: &[&str] = &[
        "authorization",
        "proxy-authorization",
        "cookie",
        "set-cookie",
        "x-api-key",
        "x-auth-token",
    ];
    /// Known credential prefixes and the minimum length of a token that starts with one.
    pub const TOKEN_PREFIXES: &[(&str, usize)] = &[
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
    /// A run of `[A-Za-z0-9_+=-]` at least this long that contains a letter and a digit is masked
    /// (catches hex digests, API keys without a known prefix, UUIDs).
    pub const LONG_TOKEN_MIN: usize = 24;
    /// A run of `[A-Za-z0-9+/=_-]` at least this long with an upper-case letter, a lower-case letter
    /// and a digit is masked (catches base64 keys that contain `/`).
    pub const LONG_B64_MIN: usize = 40;
    /// A run of hexadecimal digits at least this long, with a digit and a letter, is masked.
    pub const HEX_MIN: usize = 16;
    /// Lines made only of base64 characters, at least this long, are masked when two or more such
    /// lines are adjacent and together hold an upper-case letter, a lower-case letter and a digit
    /// (key material wrapped without a PEM header).
    pub const B64_LINE_MIN: usize = 12;
    /// Commands on whose line `-p<value>` / `-p <value>` is a password.
    pub const PASSWORD_P_COMMANDS: &[&str] = &["mysql", "mariadb", "sshpass"];

    /// All ranges for the default redactor.
    pub fn find(text: &str) -> Vec<(usize, usize)> {
        let b = text.as_bytes();
        let lower: Vec<u8> = b.iter().map(|c| c.to_ascii_lowercase()).collect();
        // Gate return A-m3: line ends computed once (each rule used to scan to the end of the line
        // per match, which made hostile input quadratic).
        let nl = newline_index(b);
        let mut r = Vec::new();
        if !false {
            private_key_blocks(&lower, &nl, &mut r);
        }
        if !false {
            url_userinfo(b, &mut r);
        }
        if !false {
            auth_schemes(&lower, &mut r);
            line_headers(&lower, &nl, &mut r);
        }
        if !false {
            assignments(b, &lower, &nl, &mut r);
            flags(b, &lower, &nl, &mut r);
        }
        if !false {
            prefixed_tokens(b, &mut r);
        }
        if !false {
            long_tokens(b, &mut r);
            hex_runs(b, &mut r);
            base64_line_blocks(b, &nl, &mut r);
        }
        r
    }

    /// `nl[i]` = index of the first `\n` at or after `i` (or the length); one entry past the end.
    fn newline_index(b: &[u8]) -> Vec<usize> {
        let mut nl = vec![b.len(); b.len() + 1];
        for i in (0..b.len()).rev() {
            nl[i] = if b[i] == b'\n' { i } else { nl[i + 1] };
        }
        nl
    }

    fn find_from(hay: &[u8], needle: &[u8], from: usize) -> Option<usize> {
        if from >= hay.len() || needle.is_empty() || needle.len() > hay.len() - from {
            return None;
        }
        hay[from..]
            .windows(needle.len())
            .position(|w| w == needle)
            .map(|p| p + from)
    }

    fn line_end(nl: &[usize], from: usize) -> usize {
        nl[from.min(nl.len() - 1)]
    }

    fn is_word(c: u8) -> bool {
        c.is_ascii_alphanumeric()
    }

    /// `-----BEGIN … PRIVATE …-----` through the matching `-----END …-----`, or to the end of the
    /// text when the end line is missing.
    pub fn private_key_blocks(lower: &[u8], nl: &[usize], r: &mut Vec<(usize, usize)>) {
        let mut i = 0;
        while let Some(p) = find_from(lower, b"-----begin", i) {
            let le = line_end(nl, p);
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

    /// `scheme://user:password@host` — the user-info part, up to the LAST `@` of the URL token (a
    /// password may itself contain `/` or `@`).
    pub fn url_userinfo(b: &[u8], r: &mut Vec<(usize, usize)>) {
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

    /// `Bearer <token>`, `Basic <token>`, `token <token>`, `Digest <…>` (case-insensitive).
    pub fn auth_schemes(lower: &[u8], r: &mut Vec<(usize, usize)>) {
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

    /// `Authorization: …`, `Cookie: …` and similar: the rest of the line.
    pub fn line_headers(lower: &[u8], nl: &[usize], r: &mut Vec<(usize, usize)>) {
        for name in LINE_HEADERS {
            let n = name.as_bytes();
            let mut i = 0;
            while let Some(p) = find_from(lower, n, i) {
                i = p + 1;
                if p > 0 && (is_word(lower[p - 1]) || lower[p - 1] == b'-') {
                    continue;
                }
                let mut q = p + n.len();
                while q < lower.len() && (lower[q] == b' ' || lower[q] == b'\t') {
                    q += 1;
                }
                if q < lower.len() && (lower[q] == b':' || lower[q] == b'=') {
                    let e = line_end(nl, q);
                    if e > q + 1 {
                        r.push((q + 1, e));
                    }
                }
            }
        }
    }

    fn sensitive(lower_name: &[u8]) -> bool {
        SENSITIVE_NAME_PARTS
            .iter()
            .any(|p| lower_name.windows(p.len()).any(|w| w == p.as_bytes()))
    }

    fn env_style(name: &[u8]) -> bool {
        // gate return A-m2: a single upper-case letter (`export P=…`) counts too
        !name.is_empty()
            && name.iter().any(|c| c.is_ascii_uppercase())
            && (name[0].is_ascii_uppercase() || name[0] == b'_')
            && name
                .iter()
                .all(|c| c.is_ascii_uppercase() || c.is_ascii_digit() || *c == b'_')
    }

    fn value_range(b: &[u8], nl: &[usize], from: usize) -> Option<(usize, usize)> {
        let mut v = from;
        while v < b.len() && (b[v] == b' ' || b[v] == b'\t') {
            v += 1;
        }
        if v >= b.len() {
            return None;
        }
        if b[v] == b'"' || b[v] == b'\'' {
            let q = b[v];
            let le = line_end(nl, v + 1);
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

    /// `NAME=value` (env-style upper-case names always; any name containing a sensitive part),
    /// `name: value`, `"name": "value"` (sensitive names only for `:`).
    pub fn assignments(b: &[u8], lower: &[u8], nl: &[usize], r: &mut Vec<(usize, usize)>) {
        // `=`/`:` inside a value already masked are not looked at again (keeps this linear).
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
            // the name before it: optional spaces, optional closing quote, then name characters
            let mut k = p;
            while k > 0 && (b[k - 1] == b' ' || b[k - 1] == b'\t') {
                k -= 1;
            }
            if k > 0 && (b[k - 1] == b'"' || b[k - 1] == b'\'') {
                k -= 1;
            }
            let end = k;
            while k > 0
                && (b[k - 1].is_ascii_alphanumeric() || matches!(b[k - 1], b'_' | b'-' | b'.'))
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
            let is_secret =
                (c == b'=' && env_style(&b[start..end])) || sensitive(&lower[start..end]);
            if is_secret {
                if let Some(v) = value_range(b, nl, p + 1) {
                    masked_to = v.1;
                    r.push(v);
                }
            }
        }
    }

    /// `--password value`, `-token value`: a flag whose name has a sensitive part, then a value.
    /// Also (gate return A-m2): `-u user:pass` / `--user user:pass` (a value with a colon), and on a
    /// `mysql`/`mariadb`/`sshpass` line `-p<value>` and `-p <value>`.
    pub fn flags(b: &[u8], lower: &[u8], nl: &[usize], r: &mut Vec<(usize, usize)>) {
        let mut line_has_p_cmd: Option<(usize, bool)> = None; // (line end, answer) cache
        let mut i = 0;
        while i < b.len() {
            if b[i] == b'-' && (i == 0 || b[i - 1].is_ascii_whitespace()) {
                let mut e = i;
                while e < b.len() && (b[e].is_ascii_alphanumeric() || matches!(b[e], b'_' | b'-')) {
                    e += 1;
                }
                let name = &lower[i..e];
                let spaced = e < b.len() && (b[e] == b' ' || b[e] == b'\t');
                if spaced && sensitive(name) {
                    if let Some((vs, ve)) = value_range(b, nl, e) {
                        if b[vs] != b'-' {
                            r.push((vs, ve));
                        }
                    }
                }
                if spaced && (name == b"-u" || name == b"--user") {
                    if let Some((vs, ve)) = value_range(b, nl, e) {
                        if b[vs..ve].contains(&b':') {
                            r.push((vs, ve));
                        }
                    }
                }
                if name.starts_with(b"-p") && !name.starts_with(b"--") {
                    let le = line_end(nl, i);
                    let has = match line_has_p_cmd {
                        Some((end, ans)) if end == le => ans,
                        _ => {
                            let mut ls = i;
                            while ls > 0 && b[ls - 1] != b'\n' {
                                ls -= 1;
                            }
                            let line = &lower[ls..le];
                            let ans = PASSWORD_P_COMMANDS
                                .iter()
                                .any(|c| line.windows(c.len()).any(|w| w == c.as_bytes()));
                            line_has_p_cmd = Some((le, ans));
                            ans
                        }
                    };
                    if has {
                        if name.len() > 2 {
                            // glued: -pSECRET (up to the next space)
                            let mut ve = i + 2;
                            while ve < b.len() && !b[ve].is_ascii_whitespace() {
                                ve += 1;
                            }
                            r.push((i + 2, ve));
                            e = e.max(ve);
                        } else if spaced {
                            if let Some((vs, ve)) = value_range(b, nl, e) {
                                if b[vs] != b'-' {
                                    r.push((vs, ve));
                                }
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

    /// Tokens that start with a known credential prefix, and JSON Web Tokens (`eyJ….….…`).
    pub fn prefixed_tokens(b: &[u8], r: &mut Vec<(usize, usize)>) {
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

    /// Long high-variety runs (see [`LONG_TOKEN_MIN`], [`LONG_B64_MIN`]).
    pub fn long_tokens(b: &[u8], r: &mut Vec<(usize, usize)>) {
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
                run.iter().any(|c| c.is_ascii_alphabetic())
                    && run.iter().any(|c| c.is_ascii_digit())
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

    /// Hexadecimal runs of at least [`HEX_MIN`] digits that mix digits and letters.
    pub fn hex_runs(b: &[u8], r: &mut Vec<(usize, usize)>) {
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

    /// Two or more adjacent lines made only of base64 characters (see [`B64_LINE_MIN`]).
    pub fn base64_line_blocks(b: &[u8], nl: &[usize], r: &mut Vec<(usize, usize)>) {
        let is_b64 = |c: u8| c.is_ascii_alphanumeric() || matches!(c, b'+' | b'/' | b'=');
        let mut block: Vec<(usize, usize)> = Vec::new();
        let flush = |block: &mut Vec<(usize, usize)>, r: &mut Vec<(usize, usize)>| {
            if block.len() >= 2 {
                let all: Vec<u8> = block.iter().flat_map(|&(s, e)| b[s..e].to_vec()).collect();
                if all.iter().any(|c| c.is_ascii_uppercase())
                    && all.iter().any(|c| c.is_ascii_lowercase())
                    && all.iter().any(|c| c.is_ascii_digit())
                {
                    r.extend(block.iter().copied());
                }
            }
            block.clear();
        };
        let mut ls = 0;
        while ls <= b.len() {
            let le = line_end(nl, ls);
            let (mut s, mut e) = (ls, le);
            while s < e && (b[s] == b' ' || b[s] == b'\t') {
                s += 1;
            }
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
            ls = le + 1;
        }
        flush(&mut block, r);
    }
}
