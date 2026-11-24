//! The secret scanner for outgoing shares (plan 25, lane N7, gap row G21).
//!
//! One pure function, [`scan`], answers for an outgoing text: [`Verdict::Clean`] or
//! [`Verdict::Flagged`] with a list of [`Finding`]s. A finding is a fixed [`Kind`] and a count, and
//! nothing else: no byte of the text, no offset, no length. Its [`Finding::text`] is one of eleven
//! fixed sentences, so a reason can be shown anywhere without showing the text.
//!
//! **It flags shapes, not secrets.** A password that is a plain word, a secret split across lines
//! or encoded, or a format nobody listed passes as `Clean`; and things that are not secrets (a git
//! commit id, a checksum, a UUID, the word "token" before another word, ...) are flagged. It is a
//! seatbelt, not a guarantee (design note 03): a flagged share is always asked. See
//! `docs/SCANNER.md` for what it flags, what it is known to miss, and what it over-flags.
//!
//! **Bounds.** A text longer than [`MAX_SCAN_BYTES`] is flagged [`Kind::TooLarge`] and never partly
//! scanned; under the bound the whole text is scanned. The work is linear in the length of the text
//! (every family walks the text a fixed number of times; line ends are computed once).
//!
//! **Pure.** No dependency; the code reads nothing outside its argument (no file, environment,
//! network, process or clock; no randomly seeded map). The same text always gives the same verdict.
//!
//! The caller passes [`Verdict::share_flagged`] to the policy as `Some(..)`; "not scanned" stays
//! `None`, which the policy treats as flagged.
#![forbid(unsafe_code)]
#![deny(missing_docs)]

mod families;

/// The largest text that is scanned (bytes). One byte more is [`Kind::TooLarge`], unscanned.
pub const MAX_SCAN_BYTES: usize = 65_536;

/// Why a text was flagged: one of the ten pattern families, or the size bound.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub enum Kind {
    /// `-----BEGIN ... PRIVATE ...-----` through its end line (or the end of the text).
    PrivateKey,
    /// `scheme://user:password@host`.
    UrlCredentials,
    /// `Bearer x`, `Basic x`, `token x`, `Digest x` (the word, a space, a value).
    AuthScheme,
    /// `Authorization:`, `Cookie:`, `X-Api-Key:` and similar headers with a value.
    AuthHeader,
    /// A value given to a secret-looking name (`api_key: x`, `"password": "x"`) or to any
    /// upper-case name (`NAME=x`).
    SecretAssignment,
    /// A password on a command line: `--password x`, `-u user:pass`, `mysql -px`, `docker login -p
    /// x`, `htpasswd -b`, SQL `PASSWORD '...'` and `IDENTIFIED BY '...'`, a `.netrc` password.
    PasswordArgument,
    /// A token that starts with a known credential prefix (`ghp_`, `sk-`, `AKIA`, ...), or a JSON
    /// web token.
    KnownToken,
    /// A long run of letters and digits (24 or more), or a long base64-like run (40 or more).
    LongToken,
    /// A run of 16 or more hexadecimal digits that mixes digits and letters.
    HexRun,
    /// Two or more adjacent lines made only of base64 characters.
    Base64Lines,
    /// The text is longer than [`MAX_SCAN_BYTES`] and was not scanned.
    TooLarge,
}

impl Kind {
    /// The ten pattern families, in the order findings are listed.
    pub const FAMILIES: [Kind; 10] = [
        Kind::PrivateKey,
        Kind::UrlCredentials,
        Kind::AuthScheme,
        Kind::AuthHeader,
        Kind::SecretAssignment,
        Kind::PasswordArgument,
        Kind::KnownToken,
        Kind::LongToken,
        Kind::HexRun,
        Kind::Base64Lines,
    ];

    /// The fixed, display-safe sentence for this kind (printable ASCII; never any part of a text).
    pub fn text(self) -> &'static str {
        match self {
            Kind::PrivateKey => "a private key block",
            Kind::UrlCredentials => "a web address with a user name and password",
            Kind::AuthScheme => "a word such as Bearer or token followed by a value",
            Kind::AuthHeader => "an authorization or cookie header with a value",
            Kind::SecretAssignment => "a value given to a secret-looking or upper-case name",
            Kind::PasswordArgument => "a password given on a command line",
            Kind::KnownToken => "a token with a known credential prefix, or a web token",
            Kind::LongToken => "a long run of mixed letters and digits",
            Kind::HexRun => "a long run of hexadecimal digits",
            Kind::Base64Lines => "lines of base64 text",
            Kind::TooLarge => "too large to scan",
        }
    }
}

/// THE ONE LIST that decides which families count towards the verdict (owner's ruling FR-2: all
/// ten by default). A family left out of it is not run and never flags; a later ruling can loosen
/// the generic families ([`Kind::LongToken`], [`Kind::HexRun`], [`Kind::Base64Lines`]) by removing
/// them here, with no other change.
pub const VERDICT_FAMILIES: &[Kind] = &Kind::FAMILIES;

/// One reason a text was flagged: a fixed kind and how many matches of it were found (in the raw
/// text or in the text with invisible format characters removed, whichever found more).
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Finding {
    kind: Kind,
    count: u32,
    // RED CONTROL `reason_echoes_text`: the broken variant carries the first matched bytes.
    #[cfg(coagent_scanner_red = "reason_echoes_text")]
    echo: String,
}

impl Finding {
    /// The kind of match.
    pub fn kind(&self) -> Kind {
        self.kind
    }

    /// How many matches of this kind (at least 1; 1 for [`Kind::TooLarge`]).
    pub fn count(&self) -> u32 {
        self.count
    }

    /// The fixed, display-safe sentence for this finding (see [`Kind::text`]).
    pub fn text(&self) -> &'static str {
        self.kind.text()
    }
}

/// The scanner's answer for one text.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Verdict {
    /// No family matched.
    Clean,
    /// At least one family matched, or the text was too large to scan. Never empty.
    Flagged(Vec<Finding>),
}

impl Verdict {
    /// What the caller passes to the policy as `Action::share_flagged = Some(..)`: `false` only
    /// for [`Verdict::Clean`].
    pub fn share_flagged(&self) -> bool {
        !matches!(self, Verdict::Clean)
    }

    /// The findings (empty for [`Verdict::Clean`]).
    pub fn findings(&self) -> &[Finding] {
        match self {
            Verdict::Clean => &[],
            Verdict::Flagged(f) => f,
        }
    }

    /// Whether a finding of this kind is in the verdict.
    pub fn names(&self, kind: Kind) -> bool {
        self.findings().iter().any(|f| f.kind == kind)
    }
}

/// Unicode format characters that are invisible in terminals and editors. The text is also scanned
/// with them removed, so they cannot split a token or a name. The list of `coagent-audit`'s
/// redactor (`redact.rs:55-59` at `039b987`) plus the characters its BACKLOG entry lists as missed:
/// combining grapheme joiner, Arabic letter mark, Hangul fillers, bidi isolates, variation
/// selectors, tag characters, musical format characters.
pub fn is_format_char(c: char) -> bool {
    matches!(c,
        '\u{00AD}' | '\u{180E}' | '\u{200B}'..='\u{200F}' | '\u{202A}'..='\u{202E}'
        | '\u{2060}'..='\u{2064}' | '\u{FEFF}'
        // new (BACKLOG R2-m4 misses)
        | '\u{034F}' | '\u{061C}' | '\u{115F}' | '\u{1160}' | '\u{2066}'..='\u{2069}' | '\u{3164}'
        | '\u{FE00}'..='\u{FE0F}' | '\u{FFA0}' | '\u{1D173}'..='\u{1D17A}'
        | '\u{E0000}'..='\u{E007F}' | '\u{E0100}'..='\u{E01EF}'
        // new (ADDENDUM 2 m3): the rest of Unicode's assigned Default_Ignorable_Code_Point set
        // (DerivedCoreProperties-18.0.0.txt, 2026-08-07: 17B4..17B5, 180B..180D, 180F, 206A..206F,
        // 1BCA0..1BCA3; E0001 is inside the tag range above), plus the format characters the
        // independent check named outside that set: 0600..0605 (prepended concatenation marks) and
        // FFF9..FFFB (interlinear annotation). Unassigned code points are not added.
        | '\u{17B4}' | '\u{17B5}' | '\u{180B}'..='\u{180D}' | '\u{180F}' | '\u{206A}'..='\u{206F}'
        | '\u{1BCA0}'..='\u{1BCA3}' | '\u{0600}'..='\u{0605}' | '\u{FFF9}'..='\u{FFFB}')
}

/// The text without [`is_format_char`] characters and without terminal control sequences
/// (`ESC [`, parameter bytes 0x30-0x3F, intermediate bytes 0x20-0x2F, a final byte 0x40-0x7E;
/// ADDENDUM 2 m2), so a shape glued to a colour code is seen. Linear: a sequence that does not
/// end in a final byte is kept, and each byte is looked at at most twice.
fn stripped_view(text: &str) -> String {
    let b = text.as_bytes();
    let mut out = String::with_capacity(text.len());
    let mut i = 0;
    while i < b.len() {
        // RED CONTROL `ansi_kept`: the broken variant keeps terminal control sequences.
        if b[i] == 0x1B && b.get(i + 1) == Some(&b'[') && false {
            let mut k = i + 2;
            while k < b.len() && (0x30..=0x3F).contains(&b[k]) {
                k += 1;
            }
            while k < b.len() && (0x20..=0x2F).contains(&b[k]) {
                k += 1;
            }
            if k < b.len() && (0x40..=0x7E).contains(&b[k]) {
                i = k + 1;
                continue;
            }
        }
        let Some(c) = text[i..].chars().next() else {
            break;
        };
        if !is_format_char(c) {
            out.push(c);
        }
        i += c.len_utf8();
    }
    out
}

/// Scan one outgoing text. Pure, linear in the length of `text`, and never panics.
///
/// Over [`MAX_SCAN_BYTES`] the answer is `Flagged([TooLarge])` without looking at the content.
/// Otherwise every family in [`VERDICT_FAMILIES`] runs on the raw text and, when the text holds a
/// format character ([`is_format_char`]) or a terminal control sequence, again on the text without
/// them; a family flags if either run matched (owner's ruling FR-4).
pub fn scan(text: &str) -> Verdict {
    if text.len() > MAX_SCAN_BYTES {
        return Verdict::Flagged(vec![finding(Kind::TooLarge, 1, None)]);
    }
    // RED CONTROL `prefix_window`: the broken variant scans only a prefix shorter than the bound.
    let text = if cfg!(coagent_scanner_red = "prefix_window") {
        let mut end = text.len().min(MAX_SCAN_BYTES / 2);
        while !text.is_char_boundary(end) {
            end -= 1;
        }
        &text[..end]
    } else {
        text
    };
    let mut tally = families::run(text);
    if text.chars().any(is_format_char) || text.contains("\u{1b}[") {
        let second = families::run(&stripped_view(text));
        for (a, b) in tally.iter_mut().zip(second) {
            if b.count > a.count {
                *a = b;
            }
        }
    }
    // RED CONTROL `flag_everything`: the broken variant flags every text.
    if cfg!(coagent_scanner_red = "flag_everything") && tally[7].count == 0 {
        tally[7].count = 1;
    }
    let findings: Vec<Finding> = Kind::FAMILIES
        .iter()
        .zip(tally)
        .filter(|(k, t)| t.count > 0 && VERDICT_FAMILIES.contains(k))
        .map(|(k, t)| finding(*k, t.count, t.echo))
        .collect();
    if findings.is_empty() {
        Verdict::Clean
    } else {
        Verdict::Flagged(findings)
    }
}

fn finding(kind: Kind, count: u32, echo: Option<String>) -> Finding {
    // `echo` is only ever `Some` in the `reason_echoes_text` red control build, and kept only there.
    #[cfg(not(coagent_scanner_red = "reason_echoes_text"))]
    drop(echo);
    Finding {
        kind,
        count: count.max(1),
        #[cfg(coagent_scanner_red = "reason_echoes_text")]
        echo: echo.unwrap_or_default(),
    }
}
