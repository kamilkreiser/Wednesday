//! QA-WIN-IPC: independent checks of `pipe_name_for` (P-2), `endpoint_for_data_dir` (P-1, Unix half)
//! and `check_peer_sid` (P-4 pure half). Written by the checker; uses NONE of the builder's test code.
//! Oracle: my own canonical form + my own decoder. Seed printed; QA_SEED overrides.
//! Run: cargo test -p coagent-ipc --test qa_win_name --release -- --nocapture

use coagent_ipc::{check_peer_sid, pipe_name_for, IpcError, PipeNameRefusal, MAX_PIPE_NAME};
use std::collections::HashMap;

struct Rng(u64);
impl Rng {
    fn next(&mut self) -> u64 {
        self.0 = self.0.wrapping_add(0x9E37_79B9_7F4A_7C15);
        let mut z = self.0;
        z = (z ^ (z >> 30)).wrapping_mul(0xBF58_476D_1CE4_E5B9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94D0_49BB_1331_11EB);
        z ^ (z >> 31)
    }
    fn below(&mut self, n: usize) -> usize {
        (self.next() % n as u64) as usize
    }
    fn pick<'a, T>(&mut self, v: &'a [T]) -> &'a T {
        &v[self.below(v.len())]
    }
}

fn seed() -> u64 {
    std::env::var("QA_SEED")
        .ok()
        .and_then(|s| s.parse().ok())
        .unwrap_or(0x0A11_CE5E_ED20_2611)
}

/// My oracle of the canonical text: ASCII fold, '/' -> '\', drop ONE trailing '\'.
fn canon(s: &str) -> Vec<u8> {
    let mut v: Vec<u8> = s
        .bytes()
        .map(|b| {
            let b = b.to_ascii_lowercase();
            if b == b'/' {
                b'\\'
            } else {
                b
            }
        })
        .collect();
    if v.last() == Some(&b'\\') {
        v.pop();
    }
    v
}

/// My oracle of "absolute by Windows spelling" as the brief states it (drive + ':' + separator, or
/// two separators then a non-separator).
fn oracle_absolute(s: &str) -> bool {
    let b = s.as_bytes();
    let sep = |c: u8| c == b'\\' || c == b'/';
    (b.len() >= 3 && b[0].is_ascii_alphabetic() && b[1] == b':' && sep(b[2]))
        || (b.len() >= 3 && sep(b[0]) && sep(b[1]) && !sep(b[2]))
}

fn kept(b: u8) -> bool {
    b.is_ascii_lowercase() || b.is_ascii_digit() || b == b'.' || b == b'_' || b == b'-'
}

fn predicted_len(c: &[u8]) -> usize {
    8 + c.iter().map(|&b| if kept(b) { 1 } else { 3 }).sum::<usize>()
}

/// My decoder: strict. Panics on any character outside the grammar.
fn decode(name: &str) -> Vec<u8> {
    let rest = name.strip_prefix("coagent-").expect("prefix");
    let b = rest.as_bytes();
    let mut out = Vec::new();
    let mut i = 0;
    while i < b.len() {
        if b[i] == b'~' {
            assert!(i + 3 <= b.len(), "short escape in {name}");
            let h = &rest[i + 1..i + 3];
            assert!(
                h.bytes().all(|c| c.is_ascii_digit() || (b'a'..=b'f').contains(&c)),
                "escape not lower-case hex in {name}"
            );
            out.push(u8::from_str_radix(h, 16).unwrap());
            i += 3;
        } else {
            assert!(kept(b[i]), "byte {:#x} not in alphabet in {name}", b[i]);
            out.push(b[i]);
            i += 1;
        }
    }
    out
}

const PUNCT: &str = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~";
const NONASCII: &[&str] = &[
    "é", "É", "ß", "ẞ", "Σ", "σ", "ς", "İ", "ı", "Ǆ", "ǅ", "ǆ", "Ω", "ω", "Ж", "ж", "ﬀ", "K", "Å", "Å",
    "e\u{301}", "\u{301}", "\u{308}", "😀", "\u{202e}", "\u{feff}", "中", "ａ", "Ａ",
];

fn gen_piece(r: &mut Rng, out: &mut String) {
    match r.below(12) {
        0..=3 => {
            let c = (b'a' + r.below(26) as u8) as char;
            out.push(if r.below(2) == 0 { c } else { c.to_ascii_uppercase() });
        }
        4 => out.push((b'0' + r.below(10) as u8) as char),
        5 => out.push(*r.pick(&PUNCT.chars().collect::<Vec<_>>())),
        6 => {
            // '~' followed by hex digits, either case, possibly an already-escaped-looking text
            out.push('~');
            for _ in 0..r.below(3) {
                out.push(*r.pick(&"0123456789abcdefABCDEF".chars().collect::<Vec<_>>()));
            }
        }
        7 => out.push_str(r.pick(&["~5c", "~5C", "~2f", "~7e", "~3a", "~"])),
        8 => out.push_str(r.pick(NONASCII)),
        9 => out.push(char::from(r.below(0x20) as u8)), // control bytes incl. NUL
        10 => out.push(if r.below(2) == 0 { '\u{7f}' } else { ' ' }),
        _ => out.push(if r.below(2) == 0 { '\\' } else { '/' }),
    }
}

fn gen_path(r: &mut Rng) -> String {
    let mut s = String::new();
    let d = (b'a' + r.below(26) as u8) as char;
    let d = if r.below(2) == 0 { d } else { d.to_ascii_uppercase() };
    match r.below(10) {
        0..=4 => {
            s.push(d);
            s.push(':');
            s.push(if r.below(2) == 0 { '\\' } else { '/' });
        }
        5 => s.push_str(r.pick(&[r"\\srv\share\", "//srv/share/", r"\\SRV\Share\"])),
        6 => s.push_str(r.pick(&[r"\\?\C:\", r"\\?\c:/", "//?/C:/", r"\\?\UNC\srv\s\"])),
        7 => s.push_str(r.pick(&[r"\\.\", r"\\.\pipe\", r"\\.\PIPE\", "//./pipe/"])),
        8 => {
            // non-absolute forms (should be refused)
            s.push_str(r.pick(&["", "C:", "c:x", r"\x", "/x", "x", r"\\", r"\\\", "//", "1:\\", "é:\\"]));
        }
        _ => {
            s.push(d);
            s.push(':');
            s.push('\\');
        }
    }
    let comps = r.below(7);
    for c in 0..comps {
        let long = r.below(40) == 0;
        let n = if long { 40 + r.below(120) } else { 1 + r.below(8) };
        for _ in 0..n {
            gen_piece(r, &mut s);
        }
        if c + 1 < comps {
            s.push(if r.below(2) == 0 { '\\' } else { '/' });
        }
    }
    match r.below(6) {
        0 => s.push('\\'),
        1 => s.push('/'),
        2 => s.push_str(r"\\"),
        _ => {}
    }
    s
}

/// Variant of `s` that differs only by ASCII case, slash direction and (maybe) one trailing sep.
fn same_canon_variant(r: &mut Rng, s: &str) -> String {
    let mut v: String = s
        .chars()
        .map(|c| match c {
            '/' | '\\' if r.below(2) == 0 => {
                if c == '/' {
                    '\\'
                } else {
                    '/'
                }
            }
            c if c.is_ascii_alphabetic() && r.below(2) == 0 => {
                if c.is_ascii_uppercase() {
                    c.to_ascii_lowercase()
                } else {
                    c.to_ascii_uppercase()
                }
            }
            c => c,
        })
        .collect();
    let ends_sep = v.ends_with('\\') || v.ends_with('/');
    if !ends_sep && r.below(3) == 0 {
        v.push(if r.below(2) == 0 { '\\' } else { '/' });
    }
    v
}

#[test]
fn qa_injective_and_decodable_over_generated_paths() {
    let sd = seed();
    let mut r = Rng(sd);
    let mut by_name: HashMap<String, (Vec<u8>, String)> = HashMap::new();
    let (mut named, mut too_long, mut not_abs, mut empty) = (0usize, 0usize, 0usize, 0usize);
    let mut collisions_equal_canon = 0usize;
    let total = 600_000;
    for i in 0..total {
        let p = if i % 3 == 2 {
            // one third: a variant of an earlier-style path (forces equal-canon collisions)
            let base = gen_path(&mut r);
            same_canon_variant(&mut r, &base)
        } else {
            gen_path(&mut r)
        };
        let got = pipe_name_for(&p);
        if p.is_empty() {
            assert!(matches!(got, Err(IpcError::PipeNameRefused { reason: PipeNameRefusal::Empty })), "seed {sd} case {i}");
            empty += 1;
            continue;
        }
        if !oracle_absolute(&p) {
            assert!(
                matches!(got, Err(IpcError::PipeNameRefused { reason: PipeNameRefusal::NotAbsolute })),
                "seed {sd} case {i}: {p:?} -> {got:?}"
            );
            not_abs += 1;
            continue;
        }
        let c = canon(&p);
        let plen = predicted_len(&c);
        match got {
            Ok(name) => {
                assert!(plen <= MAX_PIPE_NAME, "seed {sd} case {i}: accepted over limit {plen}");
                assert_eq!(name.len(), plen, "seed {sd} case {i}");
                assert!(
                    name.bytes().all(|b| kept(b) || b == b'~'),
                    "seed {sd} case {i}: alphabet {name}"
                );
                assert_eq!(decode(&name), c, "seed {sd} case {i}: decode != canon for {p:?}");
                if let Some((c0, p0)) = by_name.get(&name) {
                    assert_eq!(c0, &c, "seed {sd} case {i}: COLLISION {p0:?} vs {p:?} -> {name}");
                    collisions_equal_canon += 1;
                } else {
                    by_name.insert(name, (c, p));
                }
                named += 1;
            }
            Err(IpcError::PipeNameRefused { reason: PipeNameRefusal::TooLong { len, max } }) => {
                assert_eq!((len, max), (plen, MAX_PIPE_NAME), "seed {sd} case {i}");
                assert!(plen > MAX_PIPE_NAME, "seed {sd} case {i}");
                too_long += 1;
            }
            other => panic!("seed {sd} case {i}: {p:?} -> unexpected {other:?}"),
        }
    }
    println!(
        "QA seed {sd:#x}: {total} inputs; named {named} (distinct names {}), equal-canon repeats {collisions_equal_canon}, too long {too_long}, not absolute {not_abs}, empty {empty}",
        by_name.len()
    );
    assert!(named > 300_000 && too_long > 1_000 && not_abs > 10_000 && collisions_equal_canon > 1_000);
}

/// Two inputs that differ by anything other than case / slash / one trailing sep -> two names.
#[test]
fn qa_near_miss_pairs_differ() {
    let sd = seed() ^ 0xFF;
    let mut r = Rng(sd);
    let mut compared = 0;
    for i in 0..200_000 {
        let a = gen_path(&mut r);
        if !oracle_absolute(&a) {
            continue;
        }
        // perturb one position after the 3-char prefix
        let mut chars: Vec<char> = a.chars().collect();
        let pos = 3 + r.below(chars.len().saturating_sub(2).max(1));
        let mut ins = String::new();
        gen_piece(&mut r, &mut ins);
        match r.below(3) {
            0 if pos <= chars.len() => chars.splice(pos..pos, ins.chars()).for_each(drop),
            1 if pos < chars.len() => chars.splice(pos..pos + 1, ins.chars()).for_each(drop),
            _ if pos < chars.len() => {
                chars.remove(pos);
            }
            _ => chars.extend(ins.chars()),
        }
        let b: String = chars.into_iter().collect();
        let (na, nb) = (pipe_name_for(&a), pipe_name_for(&b));
        if let (Ok(na), Ok(nb)) = (&na, &nb) {
            if canon(&a) == canon(&b) {
                assert_eq!(na, nb, "seed {sd} case {i}");
            } else {
                assert_ne!(na, nb, "seed {sd} case {i}: {a:?} vs {b:?}");
                compared += 1;
            }
        }
    }
    println!("QA near-miss seed {sd:#x}: {compared} differing pairs compared");
    assert!(compared > 100_000);
}

fn n(s: &str) -> Result<String, IpcError> {
    pipe_name_for(s)
}

#[test]
fn qa_corners_by_hand() {
    // escaped-looking text vs a real separator
    assert_ne!(n(r"C:\a~5cb").unwrap(), n(r"C:\a\b").unwrap());
    assert_eq!(n(r"C:\a~5cb").unwrap(), "coagent-c~3a~5ca~7e5cb");
    // trailing separators: one dropped, not two
    assert_eq!(n(r"C:\a").unwrap(), n(r"C:\a\").unwrap());
    assert_ne!(n(r"C:\a").unwrap(), n(r"C:\a\\").unwrap());
    // root vs drive-relative
    assert_eq!(n(r"C:\").unwrap(), "coagent-c~3a");
    assert!(matches!(n("C:"), Err(IpcError::PipeNameRefused { reason: PipeNameRefusal::NotAbsolute })));
    assert_eq!(n("C:/").unwrap(), n(r"C:\").unwrap());
    assert_eq!(n("c:/A/b/").unwrap(), n(r"C:\a\B").unwrap());
    // UNC vs one slash (the latter is not absolute)
    assert!(n(r"\\srv\share").is_ok());
    assert!(matches!(n(r"\srv\share"), Err(IpcError::PipeNameRefused { reason: PipeNameRefusal::NotAbsolute })));
    // \\?\ and \\.\ prefixes are distinct names (known limit, fails closed)
    assert_ne!(n(r"\\?\C:\x").unwrap(), n(r"C:\x").unwrap());
    assert_ne!(n(r"\\.\C:\x").unwrap(), n(r"\\?\C:\x").unwrap());
    // a path already beginning with \\.\pipe\ is just text: fully escaped, no separator survives
    let p = n(r"\\.\pipe\coagent-x").unwrap();
    assert_eq!(p, "coagent-~5c~5c.~5cpipe~5ccoagent-x");
    assert!(!p.contains('\\'));
    // NUL and newline are escaped, never truncate
    assert_eq!(n("C:\\a\0b").unwrap(), "coagent-c~3a~5ca~00b");
    assert_eq!(n("C:\\a\nb").unwrap(), "coagent-c~3a~5ca~0ab");
    // length: exactly at, one under, one over the limit; multi-byte escape at the boundary
    // "coagent-c~3a~5c" = 15 bytes
    let base = "C:\\";
    let at = format!("{base}{}", "a".repeat(MAX_PIPE_NAME - 15));
    assert_eq!(n(&at).unwrap().len(), MAX_PIPE_NAME);
    let under = format!("{base}{}", "a".repeat(MAX_PIPE_NAME - 16));
    assert_eq!(n(&under).unwrap().len(), MAX_PIPE_NAME - 1);
    let over = format!("{base}{}", "a".repeat(MAX_PIPE_NAME - 14));
    assert!(matches!(n(&over), Err(IpcError::PipeNameRefused { reason: PipeNameRefusal::TooLong { len: 201, max: 200 } })));
    // é = 2 bytes = 6 name bytes. 15 + 179 + 6 = 200 accepted; 15 + 180 + 6 = 201 refused
    let e_at = format!("{base}{}é", "a".repeat(179));
    assert_eq!(n(&e_at).unwrap().len(), 200);
    let e_over = format!("{base}{}é", "a".repeat(180));
    assert!(matches!(n(&e_over), Err(IpcError::PipeNameRefused { reason: PipeNameRefusal::TooLong { len: 201, .. } })));
    // a 4-byte char straddling the limit: 15 + 186 + 12 = 213 refused, 15 + 173 + 12 = 200 ok
    assert_eq!(n(&format!("{base}{}😀", "a".repeat(173))).unwrap().len(), 200);
    assert!(n(&format!("{base}{}😀", "a".repeat(174))).is_err());
    // whole pipe path = 9 + name <= 209, under Microsoft's documented 256
    assert!(r"\\.\pipe\".len() + MAX_PIPE_NAME <= 256);
}

#[test]
fn qa_refusal_text_never_carries_the_input() {
    // Structural check: for every refused input of 1..=40 chars, the Display and Debug text is ONE
    // fixed string per refusal kind, so it cannot depend on (repeat) the input.
    let mut r = Rng(seed() ^ 0x40);
    let mut seen_disp: HashMap<String, usize> = HashMap::new();
    let mut seen_dbg: HashMap<String, usize> = HashMap::new();
    let mut cnt = 0;
    for len in 1..=40usize {
        for _ in 0..2_000 {
            let mut s = String::new();
            while s.chars().count() < len {
                gen_piece(&mut r, &mut s);
            }
            let s: String = s.chars().take(len).collect();
            if let Err(e) = pipe_name_for(&s) {
                *seen_disp.entry(e.to_string()).or_default() += 1;
                *seen_dbg.entry(format!("{e:?}")).or_default() += 1;
                let io: std::io::Error = e.into();
                assert_eq!(io.kind(), std::io::ErrorKind::InvalidInput);
                *seen_disp.entry(io.to_string()).or_default() += 0;
                cnt += 1;
            }
        }
    }
    println!("QA refusal texts over {cnt} refused inputs: {seen_disp:?} / {seen_dbg:?}");
    assert_eq!(seen_disp.len(), 1, "{seen_disp:?}");
    assert_eq!(seen_dbg.len(), 1, "{seen_dbg:?}");
    let e = pipe_name_for("").unwrap_err();
    assert_eq!(e.to_string(), "cannot name the local connection for this data folder: the path is empty");
}

#[test]
fn qa_sid_compare() {
    assert!(check_peer_sid("S-1-5-21-1-2-3-1001", "S-1-5-21-1-2-3-1001").is_ok());
    assert!(check_peer_sid("s-1-5-21-1-2-3-1001", "S-1-5-21-1-2-3-1001").is_ok());
    assert!(check_peer_sid("S-1-5-21-1-2-3-1001", "S-1-5-21-1-2-3-1002").is_err());
    assert!(check_peer_sid("S-1-5-21-1-2-3-100", "S-1-5-21-1-2-3-1001").is_err());
    assert!(check_peer_sid("", "").is_err());
    assert!(check_peer_sid("", "S-1-1-0").is_err());
    assert!(check_peer_sid("S-1-1-0", "").is_err());
    // non-ASCII folding must NOT apply
    assert!(check_peer_sid("S-1-É", "S-1-é").is_err());
    let e = check_peer_sid("S-1-5-21-9-9-9-1001", "S-1-5-21-9-9-9-1002").unwrap_err();
    let t = format!("{e} {e:?}");
    assert!(!t.contains("1001") && !t.contains("1002") && !t.contains("S-1"), "{t}");
    let io: std::io::Error = e.into();
    assert_eq!(io.kind(), std::io::ErrorKind::PermissionDenied);
}

#[cfg(unix)]
#[test]
fn qa_unix_endpoint_is_byte_identical() {
    use std::ffi::OsStr;
    use std::os::unix::ffi::OsStrExt;
    use std::path::{Path, PathBuf};
    let mut r = Rng(seed() ^ 0x0505);
    for i in 0..100_000 {
        let n = r.below(60);
        let mut bytes: Vec<u8> = (0..n).map(|_| (1 + r.below(255)) as u8).collect(); // any non-NUL byte, invalid UTF-8 too
        if r.below(2) == 0 {
            bytes.insert(0, b'/');
        }
        let p = Path::new(OsStr::from_bytes(&bytes));
        let got = coagent_ipc::endpoint_for_data_dir(p).unwrap_or_else(|e| panic!("case {i}: {e}"));
        let want: PathBuf = p.join("ipc").join("daemon.sock");
        assert_eq!(got.as_os_str().as_bytes(), want.as_os_str().as_bytes(), "case {i}");
    }
}
