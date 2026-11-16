//! QA gate round 2: attacks on the I1 fix (flock single-instance guard). Paths are RELATIVE to the
//! package dir (inside the gate's clone). Each test asserts the SAFE property.
#![cfg(target_os = "macos")]

use std::fs::{self, DirBuilder};
use std::os::unix::fs::{DirBuilderExt, MetadataExt};
use std::path::PathBuf;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Arc;

use coagent_ipc::IpcListener;

struct Dir(PathBuf);
impl Dir {
    fn new(tag: &str) -> Dir {
        let d = PathBuf::from(format!("gr2-{tag}-{}", std::process::id()));
        let _ = fs::remove_dir_all(&d);
        DirBuilder::new().mode(0o700).create(&d).unwrap();
        Dir(d)
    }
    fn sock(&self) -> PathBuf {
        self.0.join("d.sock")
    }
    fn lock(&self) -> PathBuf {
        self.0.join("d.sock.lock")
    }
}
impl Drop for Dir {
    fn drop(&mut self) {
        let _ = fs::remove_dir_all(&self.0);
    }
}

/// A LIVE listener whose lock file was removed by hand (or by a cleaner): the next bind creates a
/// fresh lock, takes it, then treats the live socket as stale, unlinks it and binds a second
/// listener. Safe property: a live listener's socket is never replaced.
#[tokio::test]
async fn r2_i1_live_listener_with_its_lock_file_unlinked_is_not_replaced() {
    let d = Dir::new("unl");
    let first = IpcListener::bind(&d.sock()).unwrap();
    let ino_first = fs::symlink_metadata(d.sock()).unwrap().ino();
    fs::remove_file(d.lock()).unwrap(); // the only "attack": rm of the lock file
    let second = IpcListener::bind(&d.sock());
    let stolen = second.is_ok()
        && fs::symlink_metadata(d.sock()).map(|m| m.ino()).ok() != Some(ino_first);
    drop(second);
    drop(first);
    assert!(
        !stolen,
        "FINDING I1-r2a: with the lock file unlinked, a second bind replaced a LIVE listener's socket"
    );
}

/// A hardlink planted at the lock path pointing at another file of ours: the guard must not damage
/// that file (no truncation, content intact after bind and drop).
#[tokio::test]
async fn r2_i1_hardlinked_lock_file_does_not_damage_the_target_ctl() {
    let d = Dir::new("hl");
    let precious = d.0.join("precious");
    fs::write(&precious, b"keep me").unwrap();
    fs::hard_link(&precious, d.lock()).unwrap();
    let l = IpcListener::bind(&d.sock()).unwrap();
    drop(l);
    assert_eq!(fs::read(&precious).unwrap(), b"keep me");
}

/// A directory or FIFO at the lock path is refused (no bind, no socket file).
#[tokio::test]
async fn r2_i1_non_file_at_lock_path_is_refused_ctl() {
    let d = Dir::new("nf");
    DirBuilder::new().mode(0o700).create(d.lock()).unwrap();
    assert!(IpcListener::bind(&d.sock()).is_err());
    assert!(!d.sock().exists());
}

/// Race: many tasks bind and drop concurrently on the same path. At no moment do two listeners
/// hold the guard, the retry loop terminates, and nothing is left behind at the end.
#[tokio::test(flavor = "multi_thread", worker_threads = 8)]
async fn r2_i1_concurrent_bind_drop_never_two_holders_ctl() {
    let d = Arc::new(Dir::new("race"));
    let alive = Arc::new(AtomicUsize::new(0));
    let max_seen = Arc::new(AtomicUsize::new(0));
    let ok = Arc::new(AtomicUsize::new(0));
    let other_err = Arc::new(AtomicUsize::new(0));
    let mut hs = Vec::new();
    for t in 0..8u64 {
        let (d, alive, max_seen, ok, other_err) = (
            d.clone(),
            alive.clone(),
            max_seen.clone(),
            ok.clone(),
            other_err.clone(),
        );
        hs.push(tokio::spawn(async move {
            for i in 0..150u64 {
                match IpcListener::bind(&d.sock()) {
                    Ok(l) => {
                        let n = alive.fetch_add(1, Ordering::SeqCst) + 1;
                        max_seen.fetch_max(n, Ordering::SeqCst);
                        ok.fetch_add(1, Ordering::SeqCst);
                        if (t + i) % 3 == 0 {
                            tokio::task::yield_now().await;
                        }
                        alive.fetch_sub(1, Ordering::SeqCst);
                        drop(l);
                    }
                    Err(e) if e.kind() == std::io::ErrorKind::AddrInUse => {}
                    Err(e) => {
                        eprintln!("other bind error: {e}");
                        other_err.fetch_add(1, Ordering::SeqCst);
                    }
                }
                tokio::task::yield_now().await;
            }
        }));
    }
    for h in hs {
        h.await.unwrap();
    }
    eprintln!(
        "binds ok = {}, other errors = {}",
        ok.load(Ordering::SeqCst),
        other_err.load(Ordering::SeqCst)
    );
    assert_eq!(max_seen.load(Ordering::SeqCst), 1, "two live holders at once");
    assert!(ok.load(Ordering::SeqCst) > 0);
    assert!(
        !d.sock().exists() && !d.lock().exists(),
        "files left behind after every listener dropped"
    );
    let l = IpcListener::bind(&d.sock()).expect("bind after the storm");
    drop(l);
}
