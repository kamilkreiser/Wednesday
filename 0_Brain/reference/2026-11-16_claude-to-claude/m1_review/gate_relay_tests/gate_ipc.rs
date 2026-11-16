//! QA gate attack test (gate-written). Paths are RELATIVE to the package dir (inside the gate's clone),
//! so nothing is created outside it and sun_path stays short.
#![cfg(target_os = "macos")]

use std::fs::{self, DirBuilder};
use std::os::unix::fs::DirBuilderExt;
use std::os::unix::net::UnixStream;
use std::path::PathBuf;

use coagent_ipc::IpcListener;

/// I1. "A second listener on the same path is refused" (brief §5 test 8). On macOS a connect to a
/// Unix socket whose accept backlog is full fails with ECONNREFUSED, which `prepare_socket_path`
/// takes as proof of a STALE file: it unlinks the LIVE socket of a running (but busy) listener and
/// binds a second one. Safe property: the second bind is refused and the first keeps its file.
#[tokio::test]
async fn i1_second_bind_is_refused_even_when_the_first_listeners_backlog_is_full() {
    let dir = PathBuf::from(format!("gate-ipc-{}", std::process::id()));
    DirBuilder::new().mode(0o700).create(&dir).unwrap();
    let path = dir.join("d.sock");
    let first = IpcListener::bind(&path).unwrap(); // a daemon that is alive but not accepting
    let mut held = Vec::new();
    let mut first_err = None;
    for _ in 0..5000 {
        match UnixStream::connect(&path) {
            Ok(s) => held.push(s),
            Err(e) => {
                first_err = Some(e);
                break;
            }
        }
    }
    eprintln!(
        "backlog filled after {} connections; next connect: {:?}",
        held.len(),
        first_err
    );
    let second = IpcListener::bind(&path);
    let stolen = second.is_ok();
    drop(second);
    drop(held);
    drop(first);
    let _ = fs::remove_dir_all(&dir); // this test's own directory, inside the clone
    assert!(
        !stolen,
        "FINDING I1: with the first listener's backlog full, a second IpcListener::bind on the same \
         path SUCCEEDED (the live socket file was unlinked and replaced)"
    );
}
