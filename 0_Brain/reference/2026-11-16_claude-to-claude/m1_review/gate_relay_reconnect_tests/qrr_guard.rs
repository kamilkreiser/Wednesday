//! QA-RELAY-RECONNECT (independent check): the guard's identity frame, attacked directly.
//! Written by the checker; not part of the branch.
mod common;

use std::io::Write;
use std::process::{Command, Stdio};
use std::time::{Duration, Instant};

use common::*;

fn children_of(pid: u32) -> String {
    let o = Command::new("/usr/bin/pgrep").args(["-P", &pid.to_string()]).output().unwrap();
    String::from_utf8_lossy(&o.stdout).trim().to_string()
}

/// Start the guard; feed `input`; then close stdin (`close`) or keep it open; wait for exit (max 12 s).
/// Returns (exit code, seconds, stdout, stderr, children seen while running).
fn guard(input: &[u8], drip: Option<Duration>, close: bool) -> (Option<i32>, f64, String, String, String) {
    let run_tmp = tools_dir().join("tmp");
    let mut c = Command::new(bin("coagentd"))
        .args(["relay-guard", "--coagent"])
        .arg(bin("coagent"))
        .args(["--listen", "127.0.0.1:0"])
        .env_clear()
        .env("TMPDIR", &run_tmp)
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .unwrap();
    let pid = c.id();
    let t0 = Instant::now();
    let mut stdin = c.stdin.take().unwrap();
    match drip {
        Some(d) => {
            for b in input {
                if stdin.write_all(&[*b]).is_err() { break; }
                let _ = stdin.flush();
                std::thread::sleep(d);
                if matches!(c.try_wait(), Ok(Some(_))) { break; }
            }
        }
        None => { let _ = stdin.write_all(input); let _ = stdin.flush(); }
    }
    let mut kids = String::new();
    std::thread::sleep(Duration::from_millis(200));
    if matches!(c.try_wait(), Ok(None)) { kids = children_of(pid); }
    let keep = if close { drop(stdin); None } else { Some(stdin) };
    let code = loop {
        if let Ok(Some(st)) = c.try_wait() { break st.code(); }
        if t0.elapsed() > Duration::from_secs(12) { let _ = c.kill(); let _ = c.wait(); break None; }
        std::thread::sleep(Duration::from_millis(20));
    };
    let secs = t0.elapsed().as_secs_f64();
    drop(keep);
    use std::io::Read;
    let mut out = String::new();
    let _ = c.stdout.take().unwrap().read_to_string(&mut out);
    let mut err = String::new();
    let _ = c.stderr.take().unwrap().read_to_string(&mut err);
    (code, secs, out, err, kids)
}

#[test]
fn qrr_guard_bad_frames() {
    let len = |n: u32| n.to_be_bytes().to_vec();
    let mut short = len(100); short.extend_from_slice(&[7u8; 10]);
    let mut cases: Vec<(&str, Vec<u8>, Option<Duration>, bool)> = vec![
        ("no frame, EOF", vec![], None, true),
        ("no frame, input held open", vec![], None, false),
        ("2-byte header, EOF", vec![0, 1], None, true),
        ("zero length", len(0), None, true),
        ("zero length, held open", len(0), None, false),
        ("length 16385", len(16385), None, false),
        ("length u32::MAX", len(u32::MAX), None, false),
        ("short frame, EOF", short.clone(), None, true),
        ("never-ending frame, held open", short.clone(), None, false),
    ];
    let mut drip = len(600); drip.extend_from_slice(&[1u8; 600]);
    cases.push(("one byte per 300 ms (frame of 600)", drip, Some(Duration::from_millis(300)), false));
    let mut fails = vec![];
    for (name, input, d, close) in cases {
        let (code, secs, out, err, kids) = guard(&input, d, close);
        eprintln!("QRR guard case {name:?}: exit {code:?} after {secs:.2} s; stdout {out:?}; stderr {err:?}; children while running {kids:?}");
        if code.unwrap_or(0) == 0 { fails.push(format!("{name}: exit {code:?}")); }
        if secs > 5.0 + 1.5 { fails.push(format!("{name}: exited after {secs:.2} s (deadline 5 s)")); }
        if out.contains("relay pid") || !kids.is_empty() { fails.push(format!("{name}: a relay was started ({out:?}, children {kids:?})")); }
        if !err.contains("nothing was started") { fails.push(format!("{name}: no fixed text: {err:?}")); }
    }
    assert!(fails.is_empty(), "{fails:#?}");
}

/// A frame of a valid length whose bytes are garbage: the guard cannot judge a blob; the relay must
/// refuse it and nothing must keep listening.
#[test]
fn qrr_guard_garbage_blob() {
    let mut f = 64u32.to_be_bytes().to_vec();
    f.extend_from_slice(&[0x41u8; 64]);
    let (code, secs, out, err, _k) = guard(&f, None, false);
    eprintln!("QRR guard garbage blob: exit {code:?} after {secs:.2} s; stdout {out:?}; stderr {err:?}");
    assert_ne!(code, Some(0));
    assert!(code.is_some(), "the guard did not exit with a garbage blob");
}
