# Make plant trees: git archive d79ae1c + exactly one change (a src file only; tests untouched).
import os, subprocess, sys
Q = "/private/tmp/claude-501/qana"; A = "crates/coagent-daemon/src/audit.rs"; E = "crates/coagent-daemon/src/engine.rs"
P = {
 "p1": (A, "ensure_open condition back to the base's", [(
"""        if self.host.is_none()
            && self.bound.is_some()
            && (!self.creation_failed || cfg!(coagent_red = "creation_reason_overwritten"))
        {""", """        if self.host.is_none() && self.bound.is_some() {""")]),
 "p2": (A, "status reason without the fixed sentence", [(
"""                    if self.creation_failed {
                        format!("{r}{T_CREATION_FAILED}")
                    } else {
                        r
                    }""", """                    let _ = T_CREATION_FAILED;
                    r""")]),
 "p3": (A, "the base's !a.done condition: a done seal keeps 'opened again' after a failed re-open", [(
"""            if !a.done {
                a.text = T_NOT_SEALED_NOT_REOPENED;
            } else if !cfg!(coagent_red = "row11_text_before_reopen") {
                // RED CONTROL `row11_text_before_reopen` (AN-2): the broken variant keeps row 11's
                // "opened again" when the re-open failed.
                a.text = T_SEALED_NOT_REOPENED;
            }""", """            if !a.done {
                a.text = T_NOT_SEALED_NOT_REOPENED;
            }
            let _ = T_SEALED_NOT_REOPENED;""")]),
 "p4": (A, "no re-open before the seal", [(
"""    if fig.is_none() && !cfg!(coagent_red = "member_less_never_reopened") {
        reopen(cx);
        fig = figures(cx);
    }""", """    let _ = &mut fig;""")]),
 "p5": (A, "NothingToSeal text always the old text", [(
"""        a.text = match fig {
            // RED CONTROL `nothing_text_guessed` (AN-3): the broken variant says "nothing new"
            // whatever the figures say.
            _ if cfg!(coagent_red = "nothing_text_guessed") => T_NOTHING_NEW,
            Some(f) if f.own_seq > f.own_checkpoint => T_NOTHING_UNWRITTEN,
            Some(f) if f.own_seq == f.own_checkpoint => T_NOTHING_NEW,
            _ => T_NOTHING,
        };""", """        let _ = (T_NOTHING_NEW, T_NOTHING_UNWRITTEN, fig);
        a.text = T_NOTHING;""")]),
 "p6": (A, "the unavailable reply without \"limits\": null", [(
"""                "segment": null,
                "limits": null,
            });""", """                "segment": null,
            });""")]),
 "p7": (A, "the three old 'give the command again' texts back", [
("""const T_NOT_SEALED: &str =
    "not sealed: fix the cause (see status.audit), then give the command again";""", """const T_NOT_SEALED: &str = "not sealed: give the command again";"""),
("""    "not sealed: the audit log was opened again; fix the cause (see status.audit), then give the command again";""", """    "not sealed: the audit log was opened again; give the command again";"""),
("""    "not sealed: the log's segment could not be read, so the seal was not called; fix the cause (see status.audit), then give the command again";""", """    "not sealed: the log's segment could not be read, so the seal was not called; give the command again";""")]),
 "p8": (E, "S-6 EXIT: the daemon exits 0.3 s after answering a seal that erred", [(
"""                if was_err && cfg!(coagent_red = "seal_error_ends_the_engine") {
                    self.quit = true;
                }""", """                if was_err {
                    std::thread::spawn(|| {
                        std::thread::sleep(std::time::Duration::from_millis(300));
                        std::process::exit(7);
                    });
                }""")]),
 "p9": (E, "S-6 ENGINE STOPS, PROCESS STAYS: the engine ends on a seal error and the process then sleeps forever", [(
"""                if was_err && cfg!(coagent_red = "seal_error_ends_the_engine") {
                    self.quit = true;
                }""", """                if was_err {
                    QA_S6_STAY.store(true, std::sync::atomic::Ordering::SeqCst);
                    self.quit = true;
                }"""), (
"""    eng.shutdown().await;
    let _ = accept_stop_tx.send(true);
    let _ = accept_task.await;
    log!("stopped");""", """    eng.shutdown().await;
    let _ = accept_stop_tx.send(true);
    let _ = accept_task.await;
    if QA_S6_STAY.load(std::sync::atomic::Ordering::SeqCst) {
        log!("QA plant: engine ended, process stays");
        loop {
            std::thread::sleep(std::time::Duration::from_secs(3600));
        }
    }
    log!("stopped");"""), (
"""/// The process's stop signals (W-5)""", """static QA_S6_STAY: std::sync::atomic::AtomicBool = std::sync::atomic::AtomicBool::new(false);

/// The process's stop signals (W-5)""")]),
 "p10": (E, "S-6 HANG: after answering a seal that erred, the engine blocks on its next IPC request", [(
"""                if was_err && cfg!(coagent_red = "seal_error_ends_the_engine") {
                    self.quit = true;
                }""", """                if was_err {
                    QA_S6_HANG.store(true, std::sync::atomic::Ordering::SeqCst);
                }"""), (
"""            Some(r) = ipc_rx.recv() => eng.on_ipc(r).await,""", """            Some(r) = ipc_rx.recv() => {
                if QA_S6_HANG.load(std::sync::atomic::Ordering::SeqCst) {
                    loop {
                        std::thread::sleep(std::time::Duration::from_secs(3600));
                    }
                }
                eng.on_ipc(r).await
            }"""), (
"""/// The process's stop signals (W-5)""", """static QA_S6_HANG: std::sync::atomic::AtomicBool = std::sync::atomic::AtomicBool::new(false);

/// The process's stop signals (W-5)""")]),
}
os.makedirs(f"{Q}/plants", exist_ok=True)
for name, (path, why, reps) in P.items():
    d = f"{Q}/{name}"
    os.makedirs(d)
    subprocess.run(f"git -C {Q}/c archive d79ae1c | tar -x -C {d}", shell=True, check=True)
    f = f"{d}/{path}"; s = open(f).read()
    for old, new in reps:
        assert s.count(old) == 1, (name, old[:60], s.count(old))
        s = s.replace(old, new)
    open(f, "w").write(s)
    os.makedirs(f"{Q}/tp{name[1:]}")
    diff = subprocess.run(["git", "diff", "--no-index", "--", f"{Q}/c/{path}", f], capture_output=True).stdout.decode()
    open(f"{Q}/plants/{name}.diff", "w").write(f"# {name}: {why}\n" + diff)
    print(name, path, why, "| diff lines", diff.count("\n"))
