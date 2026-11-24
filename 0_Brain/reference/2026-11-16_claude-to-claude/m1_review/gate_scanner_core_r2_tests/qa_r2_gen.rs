//! QA-SCANNER-CORE-R2 generators for texts rich in the fix round's new inputs (made up).
#![allow(dead_code)]
use super::gen;
pub const NEW_INVIS: &[char] = &['\u{17B4}', '\u{17B5}', '\u{180B}', '\u{180C}', '\u{180D}', '\u{180F}', '\u{206A}', '\u{206F}',
    '\u{1BCA0}', '\u{1BCA3}', '\u{0600}', '\u{0605}', '\u{FFF9}', '\u{FFFB}', '\u{E0001}'];
const RICH_SEP: &[&str] = &["\r", "\r\r\n", "\r\n", "\n", "\u{85}", "\u{2028}", "\u{2029}", "\n> ", "> ", ">", ">> ", "\n>", " > ",
    "\u{1b}[0m", "\u{1b}[1;31m", "\u{1b}[38;5;208m", "\u{1b}[", "\u{1b}[12;", "\u{1b}[?25l", "\u{1b}[2K", "\u{1b}(B", "\u{1b}]0;t\u{7}",
    "\u{1b}", "\u{1b}[\u{200b}0m", "\u{200b}", " ", "\t", "`", "\"", "(", "[", "=", ":", "\r ", "\r\t\n", " \r\n"];

fn insert_at_boundary(r: &mut gen::Rng, s: &mut String, ins: &str) {
    if s.is_empty() { s.push_str(ins); return; }
    let mut i = r.below(s.len() + 1);
    while !s.is_char_boundary(i) { i -= 1; }
    s.insert_str(i, ins);
}

pub fn rich_text(r: &mut gen::Rng) -> String {
    let parts = 1 + r.below(6);
    let mut s = String::new();
    for _ in 0..parts {
        match r.below(10) {
            0..=1 => s.push_str(r.pick(&["the", "build", "ok", "password", "machine h", "login u", "token", "key", "-----BEGIN", "PRIVATE", "-----END", "café", "東京"])),
            2..=7 => {
                let f = r.below(10);
                let mut p = gen::piece(r, f);
                // replace line ends inside the piece with rich ones
                if r.chance(1, 2) && p.contains('\n') {
                    let e = *r.pick(&["\r", "\u{85}", "\u{2028}", "\r\r\n", "\n> ", "\r\n", "\n>> ", "\u{2028}> "]);
                    p = p.replace('\n', e);
                }
                // insert hostile bits inside the piece
                for _ in 0..r.below(3) {
                    let ins: String = match r.below(4) {
                        0 => r.pick(NEW_INVIS).to_string(),
                        1 => r.pick(&["\u{1b}[0m", "\u{1b}[31m", "\u{1b}[", "\u{1b}[1;", "\u{1b}(B"]).to_string(),
                        2 => r.pick(&["\r", "\u{85}", "\u{2028}", "> "]).to_string(),
                        _ => r.pick(&['\u{200b}', '\u{feff}', '\u{2066}']).to_string(),
                    };
                    insert_at_boundary(r, &mut p, &ins);
                }
                // glue a hostile prefix
                if r.chance(1, 3) {
                    let pre = *r.pick(&["\u{1b}[32m", "\u{1b}[", "> ", "\r", "\u{85}", "\u{2028}", "`", "(", "\u{180b}", "\u{1b}[1;2"]);
                    p.insert_str(0, pre);
                }
                s.push_str(&p);
            }
            8 => s.push(*r.pick(NEW_INVIS)),
            _ => s.push_str(r.pick(RICH_SEP)),
        }
        s.push_str(r.pick(RICH_SEP));
    }
    s
}

/// a PEM header in every window shape the round touched
pub fn pem_header_text(r: &mut gen::Rng) -> String {
    let seps = ["\n", "\r", "\r\n", "\u{85}", "\u{2028}", " ", "> ", "\n> ", "\u{1b}[0m", "\u{200b}", "\u{180b}", "\r\r\n", "\t", ""];
    let kind = *r.pick(&["RSA PRIVATE KEY", "PRIVATE KEY", "EC PRIVATE KEY", "OPENSSH PRIVATE KEY", "PUBLIC KEY"]);
    let pad = " ".repeat(r.below(125));
    let s1 = *r.pick(&seps);
    let s2 = *r.pick(&seps);
    let eol = *r.pick(&seps);
    let blen = 8 + r.below(70);
    let body = gen::chars(r, b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/", blen);
    let lead = *r.pick(&["", "key:", "> ", "\u{1b}[33m", "`", "x"]);
    let mut t = format!("{lead}-----BEGIN{s1}{pad}{s2}{kind}-----{eol}{body}");
    if r.chance(2, 3) {
        t.push_str(&format!("{eol}-----END {kind}-----"));
    }
    t
}

