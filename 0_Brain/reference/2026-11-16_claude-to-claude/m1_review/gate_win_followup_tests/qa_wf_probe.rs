//! QA-WIN-FOLLOWUP probe (never committed): the Windows data-folder rule at the head, attacked.
//! * N-4: generated pairs at the QA seed against an INDEPENDENT model of how Windows resolves a
//!   drive path (separators collapsed, `.`/`..`, trailing dots and spaces stripped, streams,
//!   device names); every ACCEPTED pair must be strictly inside the profile and spell every
//!   profile name byte-exact, in the text AND after resolution.
//! * Every refusal text is a function of its category only (no input echoed).
//! * Hand cases for N-4 and N-1, each with its expected result.
use std::collections::{BTreeMap, BTreeSet};

use coagent_daemon::datadir::{win_data_dir_rule, WinDirRefusal as R, WinPathFault as F};

const SEED_A: u64 = 0x5157_4646_5052_4f42; // "QWFFPROB"
const SEED_B: u64 = 0x0bad_c0de_2026_1123;
const N: usize = 150_000;

struct Rng(u64);
impl Rng {
    fn next(&mut self) -> u64 {
        // splitmix64
        self.0 = self.0.wrapping_add(0x9e37_79b9_7f4a_7c15);
        let mut z = self.0;
        z = (z ^ (z >> 30)).wrapping_mul(0xbf58_476d_1ce4_e5b9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94d0_49bb_1331_11eb);
        z ^ (z >> 31)
    }
    fn below(&mut self, n: usize) -> usize {
        (self.next() % n as u64) as usize
    }
    fn coin(&mut self, pct: usize) -> bool {
        self.below(100) < pct
    }
    fn pick<'a, T>(&mut self, xs: &'a [T]) -> &'a T {
        &xs[self.below(xs.len())]
    }
}

// --- my own device-name list and check (not copied from the product) ----------------------------
fn qa_devices() -> Vec<String> {
    let mut v: Vec<String> = ["CON", "PRN", "AUX", "NUL", "CONIN$", "CONOUT$", "CLOCK$"]
        .iter()
        .map(|s| s.to_string())
        .collect();
    for p in ["COM", "LPT"] {
        for d in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "\u{b9}", "\u{b2}", "\u{b3}"] {
            v.push(format!("{p}{d}"));
        }
    }
    v
}
fn qa_is_device(name: &str, devs: &[String]) -> bool {
    let stem = name.split('.').next().unwrap_or(name).trim_end_matches(' ');
    devs.iter().any(|d| d.eq_ignore_ascii_case(stem))
}

/// Independent model of Win32 full-path resolution for a drive path. `None` = Windows would not
/// read it as a plain `X:\…` path on a local drive (so an accepted pair must never be one).
#[derive(Debug)]
struct Resolved {
    drive: u8,
    raw: Vec<String>,  // the names as written (split on both separators, empties kept)
    comps: Vec<String>, // after Windows' normalisation
    dirty: bool,        // the normalisation changed something, or a stream / device / bad char seen
}
fn win_resolve(s: &str, devs: &[String]) -> Option<Resolved> {
    let b = s.as_bytes();
    if b.len() < 3 || !b[0].is_ascii_alphabetic() || b[1] != b':' || !(b[2] == b'\\' || b[2] == b'/') {
        return None;
    }
    let rest = &s[3..];
    let raw: Vec<String> = if rest.is_empty() {
        vec![]
    } else {
        rest.split(['\\', '/']).map(|x| x.to_string()).collect()
    };
    let mut comps: Vec<String> = vec![];
    let mut dirty = false;
    let n = raw.len();
    for (i, r) in raw.iter().enumerate() {
        if r.is_empty() {
            if i + 1 != n {
                dirty = true; // doubled separator: Windows collapses it
            }
            continue;
        }
        if r == "." {
            dirty = true;
            continue;
        }
        if r == ".." {
            dirty = true;
            comps.pop();
            continue;
        }
        let t = r.trim_end_matches(['.', ' ']);
        if t != r {
            dirty = true;
        }
        if t.is_empty() {
            dirty = true;
            continue;
        }
        if t.contains(':') || t.chars().any(|c| (c as u32) < 0x20 || "*?\"<>|".contains(c)) {
            dirty = true;
        }
        if qa_is_device(t, devs) {
            dirty = true;
        }
        comps.push(t.to_string());
    }
    Some(Resolved { drive: b[0].to_ascii_lowercase(), raw, comps, dirty })
}

fn names_of(s: &str) -> Vec<&str> {
    let rest = &s[3..];
    let rest = rest.strip_suffix(['\\', '/']).unwrap_or(rest);
    if rest.is_empty() {
        vec![]
    } else {
        rest.split(['\\', '/']).collect()
    }
}

/// The safety property of an ACCEPTED pair.
fn assert_safe(p: &str, d: &str, devs: &[String], tag: &str) {
    let rp = win_resolve(p, devs).unwrap_or_else(|| panic!("{tag}: accepted, profile not a drive path: {p:?} | {d:?}"));
    let rd = win_resolve(d, devs).unwrap_or_else(|| panic!("{tag}: accepted, data not a drive path: {p:?} | {d:?}"));
    assert!(!rp.dirty && !rd.dirty, "{tag}: accepted a pair Windows would rewrite: {p:?} | {d:?} {rp:?} {rd:?}");
    assert_eq!(rp.drive, rd.drive, "{tag}: other drive {p:?} | {d:?}");
    assert!(!rp.comps.is_empty(), "{tag}: drive-root profile {p:?}");
    assert!(rd.comps.len() > rp.comps.len(), "{tag}: not strictly inside {p:?} | {d:?}");
    for (i, pc) in rp.comps.iter().enumerate() {
        assert_eq!(pc.as_bytes(), rd.comps[i].as_bytes(), "{tag}: resolved name {i} not byte-exact {p:?} | {d:?}");
    }
    let (pn, dn) = (names_of(p), names_of(d));
    for (i, x) in pn.iter().enumerate() {
        assert_eq!(x.as_bytes(), dn[i].as_bytes(), "{tag}: written name {i} not byte-exact {p:?} | {d:?}");
    }
    let _ = rd.raw;
}

// --- generator ---------------------------------------------------------------------------------
const ALPHA: &[&str] = &[
    "a", "A", "n", "N", "b", "B", "x", "X", "s", "S", "i", "I", "k", "K", "o", "O", "c", "C", "m", "M", "p", "P", "r", "R",
    "\u{c9}", "\u{e9}", "\u{416}", "\u{436}", "\u{df}", "\u{130}", "\u{131}", "\u{212a}", "\u{1e9e}", "~", "0", "1", "\u{b9}",
    "\u{2074}", "\u{2081}", ".", " ", "-", "_", "$", "\u{ff0f}", "\u{ff3c}",
];
const SPECIAL: &[&str] = &[
    "Users", "users", "USERS", "ann", "Ann", "ANN", "PROGRA~1", "Program Files", "CON", "con.txt", "COM1", "COM\u{b9}",
    "com\u{b9}.log", "CONIN$", "conout$", "Clock$", "LPT0", "COM10", "COM00", "LPT10", "CONIN", "CONOUT", "CLOCK", "COM\u{2074}",
    "COM\u{2081}", "COM\u{b9}\u{b9}", ".", "..", "...", "a.", "a ", "x::$DATA", "x:y", "Stra\u{df}e", "STRASSE", "\u{130}lker",
    "ilker", "\u{c9}lan", "\u{e9}lan", "\u{410}\u{43d}\u{43d}\u{430}", "\u{430}\u{43d}\u{43d}\u{430}",
];
fn name(r: &mut Rng) -> String {
    if r.coin(15) {
        return r.pick(SPECIAL).to_string();
    }
    let len = 1 + r.below(5);
    (0..len).map(|_| *r.pick(ALPHA)).collect()
}
fn sep(r: &mut Rng) -> &'static str {
    if r.coin(50) { "\\" } else { "/" }
}
fn join(r: &mut Rng, drive: char, parts: &[String], trail: usize) -> String {
    let mut s = format!("{drive}:{}", sep(r));
    for (i, p) in parts.iter().enumerate() {
        if i > 0 {
            s.push_str(sep(r));
            if r.coin(2) {
                s.push_str(sep(r)); // a doubled separator inside
            }
        }
        s.push_str(p);
    }
    for _ in 0..trail {
        if !parts.is_empty() {
            s.push_str(sep(r));
        }
    }
    s
}
fn ascii_recase(r: &mut Rng, s: &str) -> String {
    s.chars()
        .map(|c| {
            if c.is_ascii_alphabetic() && r.coin(50) {
                if c.is_ascii_uppercase() { c.to_ascii_lowercase() } else { c.to_ascii_uppercase() }
            } else {
                c
            }
        })
        .collect()
}
fn unicode_recase(r: &mut Rng, s: &str) -> String {
    s.chars()
        .flat_map(|c| {
            if r.coin(50) {
                let up: Vec<char> = c.to_uppercase().collect();
                let lo: Vec<char> = c.to_lowercase().collect();
                if r.coin(50) { up } else { lo }
            } else {
                vec![c]
            }
        })
        .collect()
}

fn gen_pair(r: &mut Rng) -> (String, String) {
    let drives = ['C', 'c', 'D', 'd', 'Z'];
    let pd = *r.pick(&drives);
    let np = 1 + r.below(4);
    let pparts: Vec<String> = (0..np).map(|_| name(r)).collect();
    let ptrail = if r.coin(80) { 0 } else { 1 + r.below(2) };
    let p = join(r, pd, &pparts, ptrail);
    let mut dparts = pparts.clone();
    // mutate the profile's names as the data folder spells them
    let mode = r.below(10);
    match mode {
        0..=3 => {} // copied exactly
        4 => {
            let i = r.below(np);
            dparts[i] = ascii_recase(r, &dparts[i]);
        }
        5 => {
            let i = r.below(np);
            dparts[i] = unicode_recase(r, &dparts[i]);
        }
        6 => {
            let i = r.below(np);
            dparts[i] = format!("{}{}", dparts[i], name(r));
        }
        7 => {
            let i = r.below(np);
            dparts[i] = name(r);
        }
        8 => {
            dparts.truncate(r.below(np + 1));
        }
        _ => {
            let i = r.below(np + 1);
            dparts.insert(i, r.pick(&[".", "..", "", "x\\..", "a."]).to_string());
        }
    }
    let extra = r.below(4);
    for _ in 0..extra {
        dparts.push(name(r));
    }
    let dd = if r.coin(85) {
        if r.coin(50) { pd.to_ascii_lowercase() } else { pd.to_ascii_uppercase() }
    } else {
        *r.pick(&drives)
    };
    let dtrail = if r.coin(75) { 0 } else { 1 + r.below(2) };
    let d = join(r, dd, &dparts, dtrail);
    (p, d)
}

fn run_seed(seed: u64) {
    let devs = qa_devices();
    assert_eq!(devs.len(), 33);
    let mut r = Rng(seed);
    let mut cats: BTreeMap<String, usize> = BTreeMap::new();
    let mut texts: BTreeMap<String, BTreeSet<String>> = BTreeMap::new();
    let mut cost: BTreeMap<String, usize> = BTreeMap::new();
    let mut accepted = 0usize;
    for case in 0..N {
        let (p, d) = gen_pair(&mut r);
        let got = win_data_dir_rule(&p, &d);
        let tag = format!("seed {seed:#x} case {case}");
        match got {
            Ok(()) => {
                accepted += 1;
                assert_safe(&p, &d, &devs, &tag);
                *cats.entry("accepted".into()).or_default() += 1;
            }
            Err(e) => {
                let k = format!("{e:?}");
                *cats.entry(k.clone()).or_default() += 1;
                texts.entry(k.clone()).or_default().insert(e.to_string());
                // ProfileSpelledDifferently: an ASCII-case-only difference in a profile name, and
                // no profile name differing in more than that.
                if e == R::ProfileSpelledDifferently {
                    let (pn, dn) = (names_of(&p), names_of(&d));
                    assert!(dn.len() >= pn.len(), "{tag}: PSD but data shorter {p:?} | {d:?}");
                    assert!(pn.iter().zip(&dn).all(|(a, b)| a.eq_ignore_ascii_case(b)), "{tag}: PSD with a letter difference {p:?} | {d:?}");
                    assert!(pn.iter().zip(&dn).any(|(a, b)| a != b), "{tag}: PSD with no difference {p:?} | {d:?}");
                }
                // The cost side: Windows would resolve it strictly inside, byte-exact, clean.
                if let (Some(rp), Some(rd)) = (win_resolve(&p, &devs), win_resolve(&d, &devs)) {
                    let inside_exact = !rp.dirty
                        && !rd.dirty
                        && rp.drive == rd.drive
                        && !rp.comps.is_empty()
                        && rd.comps.len() > rp.comps.len()
                        && rp.comps.iter().zip(&rd.comps).all(|(a, b)| a == b);
                    let inside_folded = !rp.dirty
                        && !rd.dirty
                        && rp.drive == rd.drive
                        && !rp.comps.is_empty()
                        && rd.comps.len() > rp.comps.len()
                        && rp.comps.iter().zip(&rd.comps).all(|(a, b)| a.to_lowercase() == b.to_lowercase());
                    if inside_exact {
                        *cost.entry(format!("refused though Windows-inside byte-exact: {k}")).or_default() += 1;
                        if cost.len() < 50 {
                            eprintln!("COST-EXACT {k}: {p:?} | {d:?}");
                        }
                    } else if inside_folded {
                        *cost.entry(format!("refused, inside only under a case fold: {k}")).or_default() += 1;
                    }
                }
            }
        }
    }
    // Every refusal text depends on its category alone, and none holds a separator.
    for (k, set) in &texts {
        assert_eq!(set.len(), 1, "category {k} has {} texts: {set:?}", set.len());
        for t in set {
            assert!(!t.contains('\\') && !t.contains('/'), "{k}: text holds a separator: {t}");
        }
    }
    println!("seed {seed:#x}: {N} pairs, accepted {accepted} (each checked safe)");
    for (k, n) in &cats {
        println!("  {k}: {n}");
    }
    for (k, n) in &cost {
        println!("  COST {k}: {n}");
    }
    println!("  distinct refusal texts: {} categories, one text each", texts.len());
}

#[test]
fn qa_generated_pairs_seed_a() {
    run_seed(SEED_A);
}
#[test]
fn qa_generated_pairs_seed_b() {
    run_seed(SEED_B);
}

// --- hand cases --------------------------------------------------------------------------------
fn check(list: &[(&str, &str, Result<(), R>)]) -> usize {
    let devs = qa_devices();
    let mut bad = 0;
    for (p, d, want) in list {
        let got = win_data_dir_rule(p, d);
        let ok = &got == want;
        println!("{} {p:?} | {d:?} -> {got:?}{}", if ok { "OK  " } else { "DIFF" }, if ok { String::new() } else { format!(" (expected {want:?})") });
        if got.is_ok() {
            assert_safe(p, d, &devs, "hand");
        }
        if !ok {
            bad += 1;
        }
    }
    bad
}

#[test]
fn qa_hand_n4() {
    use R::*;
    let a = r"C:\Users\ann";
    let psd = Err(ProfileSpelledDifferently);
    let out = Err(OutsideProfile);
    let list: Vec<(&str, &str, Result<(), R>)> = vec![
        // mixed separators on both sides
        (a, r"C:/Users\ann/x", Ok(())),
        (r"C:/Users/ann", r"C:\Users\ann\x", Ok(())),
        (r"C:\Users/ann\", r"C:/Users\ann/x/", Ok(())),
        (r"C:/Users\ann/", r"C:\Users/ann\x\", Ok(())),
        // trailing and doubled separators on each
        (r"C:\Users\ann\\", r"C:\Users\ann\x", Err(Profile(F::DoubledSeparator))),
        (r"C:\Users\\ann", r"C:\Users\ann\x", Err(Profile(F::DoubledSeparator))),
        (r"C:\\Users\ann", r"C:\Users\ann\x", Err(Profile(F::DoubledSeparator))),
        (a, r"C:\Users\ann\x\\", Err(DataDir(F::DoubledSeparator))),
        (a, r"C:\Users\\ann\x", Err(DataDir(F::DoubledSeparator))),
        (a, r"C:\\Users\ann\x", Err(DataDir(F::DoubledSeparator))),
        (a, r"C:\Users\ann//x", Err(DataDir(F::DoubledSeparator))),
        // non-ASCII case at every position
        (r"C:\Élan\ann", r"C:\élan\ann\x", out),
        (r"C:\Users\Élan", r"C:\Users\éLAN\x", out),
        (r"C:\Users\Élan", r"C:\Users\élan\x", out),
        (r"C:\Users\Élan", r"C:\Users\Élan\x", Ok(())),
        (r"C:\Users\Анна", r"C:\Users\анна\x", out),
        (r"C:\Users\Анна", r"C:\Users\АННА\x", out),
        (r"C:\Users\Анна", r"C:\Users\Анна\x", Ok(())),
        (r"C:\Users\Straße", r"C:\Users\STRASSE\x", out),
        (r"C:\Users\STRASSE", r"C:\Users\Straße\x", out),
        (r"C:\Users\Straße", r"C:\Users\STRAßE\x", psd), // only ASCII letters differ; ß kept
        (r"C:\Users\Straße", r"C:\Users\STRAẞE\x", out), // capital sharp s U+1E9E
        (r"C:\Users\İlker", r"C:\Users\ilker\x", out),
        (r"C:\Users\ılker", r"C:\Users\ILKER\x", out),
        (r"C:\Users\Ilker", r"C:\Users\ılker\x", out),
        (r"C:\Users\Ilker", r"C:\Users\ilker\x", psd),
        (r"C:\Users\Kai", "C:\\Users\\\u{212a}ai\\x", out), // Kelvin sign
        (a, r"C:\Users\ann\Élan", Ok(())), // below the profile: any spelling
        (a, r"C:\Users\ann\élan", Ok(())),
        (r"C:\a\b\c\Élan", r"C:\a\b\c\élan\x", out), // non-ASCII case in the LAST name
        // a profile at a drive root
        (r"C:\", r"C:\x", Err(ProfileIsDriveRoot)),
        (r"C:/", r"C:\x", Err(ProfileIsDriveRoot)),
        (r"C:", r"C:\x", Err(Profile(F::DriveRelative))),
        // the data folder EQUAL to the profile, every spelling
        (a, r"C:\Users\ann", Err(IsTheProfile)),
        (a, r"C:\Users\ann\", Err(IsTheProfile)),
        (a, r"C:/Users/ann/", Err(IsTheProfile)),
        (a, r"c:\Users\ann", Err(IsTheProfile)),
        (a, r"C:\users\ann", psd),
        (a, r"C:\Users\ANN\", psd),
        (a, r"C:\Users\ann\\", Err(DataDir(F::DoubledSeparator))),
        (r"C:\Users\ann\", r"C:\Users\ann", Err(IsTheProfile)),
        (a, r"C:\Users\ann.", Err(DataDir(F::TrailingDotOrSpace))),
        (a, r"C:\Users\ann\.", Err(DataDir(F::DotComponent))),
        // one-name profiles
        (r"C:\a", r"C:\a\x", Ok(())),
        (r"C:\a", r"C:\A\x", psd),
        (r"C:\a", r"c:\a\x", Ok(())),
        (r"C:\a", r"C:\a", Err(IsTheProfile)),
        (r"C:\a", r"C:\ab\x", out),
        (r"C:\a", r"C:\b\a\x", out),
        // short 8.3 names
        (r"C:\PROGRA~1\ann", r"C:\Program Files\ann\x", out),
        (r"C:\Program Files\ann", r"C:\PROGRA~1\ann\x", out),
        (r"C:\Users\ANNKRE~1", r"C:\Users\annkre~1\x", psd),
        (r"C:\Users\ANNKRE~1", r"C:\Users\ANNKRE~1\x", Ok(())),
        // case only at a NON-first position
        (a, r"C:\Users\aNn\x", psd),
        (r"C:\a\b\c\d\Last", r"C:\a\b\c\d\LAST\x", psd),
        (r"C:\a\b\c\d\Last", r"C:\a\b\c\d\Last\x", Ok(())),
        (r"C:\a\b\c\d\Last", r"C:\a\b\C\d\Last\x", psd),
        // drive-letter case alone: stays accepted
        (a, r"c:\Users\ann\x", Ok(())),
        (r"c:\users\ann", r"C:\users\ann\x", Ok(())),
        (r"c:\Users\ann", r"C:/Users/ann/x/", Ok(())),
        // case AND letters: which category
        (a, r"C:\users\bob\x", out),
        (a, r"C:\USERS\annx\x", out),
        (a, r"C:\Users\ANNA\x", out),
        (a, r"C:\USERS\anx\x", out),
        (a, r"C:\Userz\ANN\x", out),
        (a, r"C:\users\ANN", psd),
        (a, r"C:\users", out),
        // USERPROFILE spelled in another case than the disk (only the text counts)
        (r"C:\USERS\ANN", r"C:\Users\ann\x", psd),
        (r"C:\USERS\ANN", r"C:\USERS\ANN\x", Ok(())),
        // other tricks
        (a, r"C:\Users\ann\..\bob", Err(DataDir(F::DotComponent))),
        (a, r"C:\Users\ann \x", Err(DataDir(F::TrailingDotOrSpace))),
        (a, r"C:\Users\ann::$DATA\x", Err(DataDir(F::ForbiddenCharacter))),
        (a, r"\\?\C:\Users\ann\x", Err(DataDir(F::NetworkOrDevice))),
        (a, r"C:\Users\ann＼..＼bob", out), // fullwidth backslash: one name, not `ann` (QA's first expectation was wrong)
        (a, r"C:\Users\ann\x＼..＼bob", Ok(())), // fullwidth backslash: one ordinary name inside
        (a, r"D:\Users\ann\x", Err(OtherDrive)),
    ];
    let bad = check(&list);
    println!("hand N-4: {} cases, {bad} DIFF", list.len());
    assert_eq!(bad, 0);
}

#[test]
fn qa_hand_n1() {
    use R::*;
    let devs = qa_devices();
    let p = r"C:\Users\ann";
    let mut n = 0;
    let mut bad = 0;
    for name in &devs {
        // every ASCII case mix the rule folds (2^letters spellings)
        let letters: Vec<usize> = name.char_indices().filter(|(_, c)| c.is_ascii_alphabetic()).map(|(i, _)| i).collect();
        for mask in 0..(1u32 << letters.len()) {
            let sp: String = name
                .char_indices()
                .map(|(i, c)| match letters.iter().position(|&j| j == i) {
                    Some(k) if mask & (1 << k) != 0 => c.to_ascii_lowercase(),
                    _ => c,
                })
                .collect();
            for form in [sp.clone(), format!("{sp}.txt"), format!("{sp} .txt"), format!("{sp}  .tar.gz")] {
                // in the data folder, last and not last
                for d in [format!(r"{p}\{form}"), format!(r"{p}\{form}\x"), format!(r"{p}\a\{form}")] {
                    n += 1;
                    if win_data_dir_rule(p, &d) != Err(DataDir(F::ReservedName)) {
                        bad += 1;
                        println!("NOT REFUSED (data): {d:?} -> {:?}", win_data_dir_rule(p, &d));
                    }
                }
                // in the profile, last and not last
                for pp in [format!(r"C:\Users\{form}"), format!(r"C:\{form}\ann")] {
                    n += 1;
                    let d = format!(r"{pp}\x");
                    if win_data_dir_rule(&pp, &d) != Err(Profile(F::ReservedName)) {
                        bad += 1;
                        println!("NOT REFUSED (profile): {pp:?} -> {:?}", win_data_dir_rule(&pp, &d));
                    }
                }
            }
            // a bare trailing space (no dot) is refused for its trailing space, not as a device
            let d = format!(r"{p}\{sp} ");
            assert_eq!(win_data_dir_rule(p, &d), Err(DataDir(F::TrailingDotOrSpace)), "{d:?}");
        }
    }
    println!("N-1 reserved: {n} placements of the 33 names in every ASCII case, {bad} not refused");
    assert_eq!(bad, 0);
    // Names NEAR the list: must stay accepted.
    let near = [
        "COM10", "COM00", "LPT10", "CONIN", "CONOUT", "CLOCK", "COM\u{2074}", "COM\u{2081}", "COM\u{b9}\u{b9}", "COM\u{2070}",
        "LPT\u{2074}", "CONIN$$", "CON$", "NUL$", "CLOCK$$", "COM\u{b9}x", "xCON", "CONx", "COM", "LPT", "CONINx$",
    ];
    for nm in near {
        for d in [format!(r"{p}\{nm}"), format!(r"{p}\{nm}.txt"), format!(r"{p}\{nm}\x")] {
            let got = win_data_dir_rule(p, &d);
            println!("near {nm:?} as {d:?} -> {got:?}");
            assert_eq!(got, Ok(()), "{d:?}");
        }
    }
    // Non-ASCII case of the superscript / dollar names is not folded (compared exactly).
    for nm in ["ＣＯＮ", "ＣＯＭ1", "ᶜᵒⁿ"] {
        let d = format!(r"{p}\{nm}");
        println!("look-alike {nm:?} -> {:?}", win_data_dir_rule(p, &d));
    }
}
