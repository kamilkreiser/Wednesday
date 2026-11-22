//! QA-W-DAEMON probe (the independent check's own; NOT part of the repository).
//! Adversarial probes of `win_data_dir_rule` and `win_profile_from_env` against an independent
//! model of how Win32 resolves a full path (GetFullPathNameW-style: separators `\` and `/`,
//! doubled separators collapse, `.` dropped, `..` climbs, trailing dots and spaces of a name are
//! stripped). The model is written from general knowledge (UNVERIFIED against Microsoft's pages)
//! and is deliberately MORE permissive than the rule, so that anything the rule accepts can be
//! judged: an accepted pair whose resolved data folder is not strictly inside the resolved profile
//! (by any spelling) is an ESCAPE.
//!
//! Run: cargo test --locked -p coagent-daemon --test qa_wd_probe -- --nocapture

use coagent_daemon::datadir::{win_data_dir_rule, win_profile_from_env, WinDirRefusal};
use std::collections::BTreeMap;
use std::ffi::OsStr;

const SEED: u64 = 0x5141_5744_5052_4f42; // "QAWDPROB"
const N: usize = 200_000;

struct Rng(u64);
impl Rng {
    fn next(&mut self) -> u64 {
        // splitmix64
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

/// What the model says a text resolves to.
#[derive(Debug)]
enum Model {
    /// A normal drive path: drive letter (lower-cased) and resolved names (as spelled).
    Full(u8, Vec<String>),
    /// Anything that is not a plain `X:\` full path (network, device, long-path, drive-relative,
    /// rooted-without-drive, relative), or that holds a control character / stream / device name.
    Odd(&'static str),
}

const DEVICES: &[&str] = &[
    "CON", "PRN", "AUX", "NUL", "COM0", "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7",
    "COM8", "COM9", "LPT0", "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9",
    "COM\u{b9}", "COM\u{b2}", "COM\u{b3}", "LPT\u{b9}", "LPT\u{b2}", "LPT\u{b3}", "CONIN$",
    "CONOUT$", "CLOCK$",
];

const W2_LIST: &[&str] = &[
    "CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8",
    "COM9", "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9",
];

fn model(s: &str) -> Model {
    if s.chars().any(|c| (c as u32) < 0x20) {
        return Model::Odd("control");
    }
    let b = s.as_bytes();
    let sep = |x: u8| x == b'\\' || x == b'/';
    if b.len() < 3 || !b[0].is_ascii_alphabetic() || b[1] != b':' || !sep(b[2]) {
        return Model::Odd("not X:\\");
    }
    let mut out: Vec<String> = Vec::new();
    for raw in s[3..].split(['\\', '/']) {
        let name = raw.trim_end_matches(['.', ' ']);
        if raw.is_empty() {
            continue; // doubled separator collapses
        }
        if raw == "." {
            continue;
        }
        if raw == ".." {
            out.pop();
            continue;
        }
        if name.is_empty() {
            // "..." or "  " style: Win32 strips to nothing (or treats "..."? ) -> odd
            return Model::Odd("dots/spaces only");
        }
        if name.contains(':') {
            return Model::Odd("stream");
        }
        let stem = name.split('.').next().unwrap_or(name).trim_end_matches(' ');
        if DEVICES.iter().any(|d| d.eq_ignore_ascii_case(stem) || *d == stem.to_uppercase()) {
            // A name outside W-2's own list (COM0, LPT0, the superscript forms, CONIN$, CONOUT$,
            // CLOCK$): counted as its own class, judged separately in the verdict.
            if W2_LIST.iter().any(|d| d.eq_ignore_ascii_case(stem)) {
                return Model::Odd("device");
            }
            return Model::Odd("device-not-in-W2-list");
        }
        out.push(name.to_string());
    }
    Model::Full(b[0].to_ascii_lowercase(), out)
}

/// Strictly inside, comparing names ASCII-case-insensitively (NTFS default) and also reporting
/// whether the match needed case folding at all.
fn inside(p: &Model, d: &Model) -> (bool, bool) {
    match (p, d) {
        (Model::Full(pd, pp), Model::Full(dd, dp)) => {
            if pd != dd || dp.len() <= pp.len() || pp.is_empty() {
                return (false, false);
            }
            let mut folded = false;
            for (a, b) in pp.iter().zip(dp) {
                if a != b {
                    if a.eq_ignore_ascii_case(b) {
                        folded = true;
                    } else {
                        return (false, false);
                    }
                }
            }
            (true, folded)
        }
        _ => (false, false),
    }
}

const NAMES: &[&str] = &[
    "Users", "ann", "Ann", "ANN", "ann2", "anna", "bob", "work", "x", "data", "Élan", "élan",
    "ДОМ", "дом", "a b", "co.agent", ".hidden", "PROGRA~1", "CONSOLE", "COM10", "nul.txt", "NUL",
    "COM1", "com9.log", "LPT9", "COM\u{b9}", "LPT\u{b3}", "COM0", "CONIN$", "x.", "x ", "x..",
    "x. .", "..", ".", "...", " ", "x:stream", "x::$DATA", "x*", "x?", "x|y", "\u{ff3c}", "a\u{2215}b",
    "\u{0130}", "i", "\u{212a}", "k", "ß", "SS", "\u{7f}", "\u{200b}", "e\u{301}", "\u{e9}",
];

fn rand_name(r: &mut Rng) -> String {
    r.pick(NAMES).to_string()
}

fn sep(r: &mut Rng) -> &'static str {
    *r.pick(&["\\", "/", "\\", "/", "\\\\", "//", "\\/"])
}

fn join(r: &mut Rng, head: &str, parts: &[String], weird_seps: bool) -> String {
    let mut s = head.to_string();
    for (i, p) in parts.iter().enumerate() {
        if i > 0 {
            s.push_str(if weird_seps { sep(r) } else { "\\" });
        }
        s.push_str(p);
    }
    s
}

fn heads(r: &mut Rng, drive: char) -> String {
    let d = if r.below(4) == 0 { drive.to_ascii_lowercase() } else { drive };
    match r.below(16) {
        0 => format!("\\\\?\\{d}:\\"),
        1 => format!("\\\\.\\{d}:\\"),
        2 => "\\\\server\\share\\".to_string(),
        3 => format!("{d}:"),
        4 => "\\".to_string(),
        5 => format!("//?/{d}:/"),
        6 => format!("\\??\\{d}:\\"),
        7 => format!("{d}:/"),
        8 => "".to_string(),
        9 => "D:\\".to_string(),
        _ => format!("{d}:\\"),
    }
}

#[test]
fn qa_generated_pairs_never_escape() {
    let seed = std::env::var("QA_SEED").ok().and_then(|s| u64::from_str_radix(s.trim_start_matches("0x"), 16).ok()).unwrap_or(SEED);
    let mut r = Rng(seed);
    let mut accepted = 0usize;
    let mut accepted_folded = 0usize;
    let mut escapes: Vec<(String, String, String)> = Vec::new();
    let mut refused: BTreeMap<String, usize> = BTreeMap::new();
    let mut extra_device = 0usize;
    let mut extra_samples: Vec<(String, String)> = Vec::new();
    for _case in 0..N {
        // Profile: a mostly well-formed one, sometimes odd.
        let plen = 1 + r.below(3);
        let mut pparts: Vec<String> = (0..plen)
            .map(|_| {
                if r.below(5) == 0 {
                    rand_name(&mut r)
                } else {
                    r.pick(&["Users", "ann", "Home", "Élan", "дом"]).to_string()
                }
            })
            .collect();
        if r.below(10) == 0 {
            pparts.clear();
        }
        let phead = if r.below(8) == 0 { heads(&mut r, 'C') } else { "C:\\".to_string() };
        let ws = r.below(6) == 0;
        let mut profile = join(&mut r, &phead, &pparts, ws);
        if r.below(6) == 0 {
            profile.push_str(sep(&mut r));
        }
        // Data folder: the profile's names, then mutated.
        let mut dparts = pparts.clone();
        let extra = r.below(4);
        for _ in 0..extra {
            dparts.push(rand_name(&mut r));
        }
        for _ in 0..r.below(4) {
            if dparts.is_empty() {
                break;
            }
            let i = r.below(dparts.len());
            match r.below(10) {
                0 => dparts.insert(i, "..".into()),
                1 => dparts[i] = dparts[i].to_ascii_uppercase(),
                2 => dparts[i] = dparts[i].to_uppercase(),
                3 => dparts[i].push_str(r.pick(&[".", " ", "..", ". ", "::$DATA", ":s"])),
                4 => dparts[i] = format!("{}{}", dparts[i], r.pick(&["2", "x", " ", "."])),
                5 => dparts.insert(i, ".".into()),
                6 => dparts[i] = rand_name(&mut r),
                7 => {
                    dparts.remove(i);
                }
                8 => dparts.insert(i, String::new()),
                _ => dparts[i] = dparts[i].to_lowercase(),
            }
        }
        let dhead = if r.below(6) == 0 { heads(&mut r, 'C') } else { phead.clone() };
        let ws = r.below(3) == 0;
        let mut data = join(&mut r, &dhead, &dparts, ws);
        if r.below(8) == 0 {
            data.push_str(sep(&mut r));
        }
        if r.below(40) == 0 {
            let bounds: Vec<usize> = (0..=data.len()).filter(|i| data.is_char_boundary(*i)).collect();
            let at = *r.pick(&bounds);
            data.insert(at, '\u{1}');
        }
        let got = win_data_dir_rule(&profile, &data);
        let again = win_data_dir_rule(&profile, &data);
        assert_eq!(got, again, "seed {SEED:#x}: not a function: {profile:?} {data:?}");
        match got {
            Ok(()) => {
                accepted += 1;
                let (ins, folded) = inside(&model(&profile), &model(&data));
                if folded {
                    accepted_folded += 1;
                }
                let extra_dev = matches!(model(&profile), Model::Odd("device-not-in-W2-list"))
                    || matches!(model(&data), Model::Odd("device-not-in-W2-list"));
                if !ins && extra_dev {
                    extra_device += 1;
                    if extra_samples.len() < 8 {
                        extra_samples.push((profile.clone(), data.clone()));
                    }
                } else if !ins {
                    escapes.push((
                        profile.clone(),
                        data.clone(),
                        format!("{:?} / {:?}", model(&profile), model(&data)),
                    ));
                }
            }
            Err(e) => *refused.entry(format!("{e:?}")).or_default() += 1,
        }
    }
    println!("QA seed {seed:#x}, {N} pairs: accepted {accepted} (of which needing ASCII case folding {accepted_folded})");
    for (k, v) in &refused {
        println!("  refused {k}: {v}");
    }
    println!("accepted with a device name outside W-2's list (COM0/LPT0/superscripts/CONIN$/CONOUT$/CLOCK$): {extra_device}");
    for e in &extra_samples {
        println!("  EXTRA-DEVICE {e:?}");
    }
    for e in escapes.iter().take(30) {
        println!("ESCAPE {e:?}");
    }
    assert!(accepted > 1000, "too few accepted pairs to mean anything: {accepted}");
    assert!(escapes.is_empty(), "{} accepted pairs escape the profile (first above)", escapes.len());
}

#[test]
fn qa_hand_list() {
    let p = r"C:\Users\ann";
    let cases: &[(&str, &str, bool)] = &[
        // (profile, data, expected accepted?)
        (p, r"C:\Users\ann2\x", false),
        (r"C:\Users\ann", r"C:\Users\ann2\x", false),
        (p, r"C:\Users\Ann\..\bob", false),
        (p, r"C:\Users\Ann\..\bob\x", false),
        (p, r"C:\Users/ann\x", true),
        (p, r"C:/Users/ann/x", true),
        (p, r"C:/Users/ann/./x", false),
        (p, r"C:\Users\ann.\x", false),
        (p, r"C:\Users\ann \x", false),
        (p, r"C:\Users\ann\x.", false),
        (p, r"C:\Users\ann\x ", false),
        (p, r"C:\Users\ann\x::$DATA", false),
        (p, r"C:\Users\ann::$DATA\x", false),
        (p, r"C:\Users\ann\x:stream", false),
        (p, r"\\?\C:\Users\ann\x", false),
        (p, r"\\.\C:\Users\ann\x", false),
        (p, r"\\server\share\Users\ann\x", false),
        (p, r"\\?\UNC\server\share\x", false),
        (p, r"\??\C:\Users\ann\x", false),
        (p, r"C:Users\ann\x", false),
        (p, r"C:x", false),
        (p, r"\x", false),
        (p, r"\Users\ann\x", false),
        (p, r"Users\ann\x", false),
        (p, r"C:\Users\ann\NUL", false),
        (p, r"C:\Users\ann\nul.txt", false),
        (p, r"C:\Users\ann\COM1.log", false),
        (p, r"C:\Users\ann\LPT9", false),
        (p, "C:\\Users\\ann\\COM\u{b9}", true), // superscript one: see the verdict (not in W-2's list)
        (p, r"C:\Users\ann\COM0", true),       // COM0: not in W-2's list (see the verdict)
        (p, r"C:\Users\ann\CONIN$", true),     // CONIN$: not in W-2's list (see the verdict)
        (r"C:\Users\Élan", "C:\\Users\\élan\\x", false),
        (r"C:\Users\élan", "C:\\Users\\Élan\\x", false),
        (r"C:\Users\Élan", "C:\\Users\\Élan\\x", true),
        (p, "", false),
        ("", r"C:\Users\ann\x", false),
        (p, "C:\\Users\\ann\\x\u{0}", false),
        (p, "C:\\Users\\ann\\x\u{1f}y", false),
        (p, "C:\\Users\\ann\\x\ty", false),
        (r"C:\", r"C:\x", false),
        (r"C:/", r"C:\x", false),
        (r"C:", r"C:\x", false),
        (p, p, false),
        (p, r"C:\Users\ann\", false),
        (p, r"C:\Users\ann/", false),
        (p, r"C:\Users\ann\\", false),
        (r"C:\Users\ann\", r"C:\Users\ann", false),
        (r"C:\Users\ann\", r"C:\Users\ann\", false),
        (p, r"c:\users\ANN\x", true),
        (p, r"D:\Users\ann\x", false),
        (p, r"C:\Users\ann\\x", false),
        (p, r"C:\\Users\ann\x", false),
        (p, r"C:\Users\ann\x\\", false),
        (p, r"C:\Users\ann\x\", true),
        (p, r"C:\Users\ann\x/", true),
        (p, r"C:\Users\ann\...", false),
        (p, r"C:\Users\ann\ ", false),
        (p, r"C:\Users\ann\x\..", false),
        (p, r"C:\Users\ann\x\..\..\bob", false),
        (p, "C:\\Users\\ann\\x\u{ff3c}..\u{ff3c}bob", true), // fullwidth backslash: one ordinary name inside
        (p, "C:\\Users\\ann\u{ff3c}..\u{ff3c}bob", false), // the same with no real separator after ann: not ann
        (p, r"C:\Users\PROGRA~1\x", false),
        (r"C:\Users\ANN~1", r"C:\Users\ann\x", false),
        (p, r"C:\Users\ann\PROGRA~1", true),
        (p, r"C:\Users\ann\x*", false),
        (p, r"C:\Users\ann\x?", false),
        (p, r"C:\Users\ann\<x>", false),
        (p, "C:\\Users\\ann\\\"x\"", false),
        (p, r"C:\Users\ann\x|y", false),
        (r"\\server\share\ann", r"\\server\share\ann\x", false),
        (r"C:\Users\ann\..", r"C:\Users\x", false),
        (r"C:\Users\..\ann", r"C:\ann\x", false),
        (r"Users\ann", r"Users\ann\x", false),
    ];
    let mut bad = Vec::new();
    for (pp, dd, want) in cases {
        let got = win_data_dir_rule(pp, dd);
        println!("{:<6} {:?} | {:?} -> {:?}", if got.is_ok() == *want { "as-exp" } else { "DIFF" }, pp, dd, got);
        if got.is_ok() != *want {
            bad.push((pp, dd, got));
        }
    }
    assert!(bad.is_empty(), "{bad:?}");
}

#[test]
fn qa_profile_from_env() {
    assert_eq!(win_profile_from_env(None), Err(WinDirRefusal::ProfileUnset));
    assert!(win_profile_from_env(Some(OsStr::new(""))).is_err());
    assert_eq!(win_profile_from_env(Some(OsStr::new(r"C:\Users\ann"))), Ok(r"C:\Users\ann".to_string()));
    // A relative or odd value is returned as found; the rule then refuses it as a profile.
    for v in [r"Users\ann", r"\\server\x", r"C:", r"C:\"] {
        let p = win_profile_from_env(Some(OsStr::new(v))).unwrap();
        let r = win_data_dir_rule(&p, r"C:\Users\ann\x");
        println!("profile {v:?} -> {r:?}");
        assert!(r.is_err(), "{v}");
    }
    #[cfg(unix)]
    {
        use std::os::unix::ffi::OsStrExt;
        let r = win_profile_from_env(Some(OsStr::from_bytes(b"C:\\Users\\\xff")));
        println!("non-UTF-8 (unix bytes) -> {r:?}");
        assert!(r.is_err());
    }
}
