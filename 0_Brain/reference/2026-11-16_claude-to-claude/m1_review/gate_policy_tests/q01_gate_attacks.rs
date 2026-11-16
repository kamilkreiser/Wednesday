//! QA gate M2-POLICY (independent tier-1 read). Every test asserts the SAFE outcome; a FAILING test is a
//! finding. Fixtures come from tests/common (fake home through Env; files only under the test tmp dir).
//! Commands here are classified as strings only, never executed.
#![cfg(unix)]
mod common;
use coagent_policy::shell::powershell::recognise_powershell;
use coagent_policy::shell::recognise_posix;
use coagent_policy::*;
use common::*;
use std::path::Path;

fn closed(fx: &Fx, excl: Vec<String>) -> State {
    let mut st = fx.state_with(excl);
    st.link = LinkPhase::ClosedTainted;
    st
}
fn defaults() -> Vec<String> {
    patterns::default_exclusions()
}
fn reads_under(st: &mut State, dir: &Path) {
    st.approvals.insert(SessionApproval {
        scope: Scope::ReadsUnder {
            dir: dir.to_path_buf(),
        },
        expires_at: None,
    });
}
fn not_read_or_search(fx: &Fx, cmd: &str) {
    let a = fx.bash(cmd);
    assert!(
        !matches!(a.kind, Kind::Read | Kind::Search),
        "{cmd:?} classified {:?} (can write/execute/escape)",
        a.kind
    );
}

// ---------- F1: sort long-option abbreviation writes / executes (verified on this Mac: sort 2.3-Apple) ----
#[test]
fn f1a_sort_abbrev_output_writes_hard_deny_file_closed_link() {
    let fx = fixture("q-f1a");
    let cmd = format!("cat README.md | sort --o={}/.zshrc", fx.home.display());
    let a = fx.bash(&cmd);
    let d = decide(&a, &closed(&fx, defaults()), Surface::Console, NOW);
    assert!(!is_allow(&d), "{cmd} -> {d:?}");
}
#[test]
fn f1b_sort_abbrev_output_allowed_by_read_memory() {
    let fx = fixture("q-f1b");
    let mut st = fx.state_with(defaults());
    st.read_memory.insert(fx.ws.join("README.md"));
    let cmd = format!("cat README.md | sort --o={}/.zshrc", fx.home.display());
    let d = decide(&fx.bash(&cmd), &st, Surface::Console, NOW);
    assert!(!is_allow(&d), "{cmd} -> {d:?}");
}
#[test]
fn f1c_sort_abbrev_classified_read() {
    let fx = fixture("q-f1c");
    for cmd in [
        "cat README.md | sort --o=/tmp/x",
        "cat README.md | sort --outp=/tmp/x",
        "cat README.md | sort -S 1K --compress-prog=sh",
        "cat README.md | sort --compress=sh",
        "cat README.md | sort --temporary-d=/tmp",
    ] {
        not_read_or_search(&fx, cmd);
    }
}

// ---------- F2: grep long-option abbreviation hides recursion -> excluded .env read ----------------------
#[test]
fn f2_grep_recur_abbrev_reads_excluded_env_closed_link() {
    let fx = fixture("q-f2");
    for cmd in [
        "grep --recur TOKEN .",
        "grep --null --recur TOKEN .", // in Claude Code's zsh snapshot --null routes grep to /usr/bin/grep
        "grep --dir=recurse TOKEN .",
        "grep --directories recurse TOKEN .",
    ] {
        let d = decide(&fx.bash(cmd), &closed(&fx, defaults()), Surface::Console, NOW);
        assert!(!is_allow(&d), "{cmd} -> {d:?}");
    }
}
#[test]
fn f2b_grep_recur_abbrev_under_reads_under_approval() {
    let fx = fixture("q-f2b");
    let mut st = fx.state_with(defaults());
    reads_under(&mut st, &fx.ws);
    let d = decide(&fx.bash("grep --recur TOKEN ."), &st, Surface::Console, NOW);
    assert!(!is_allow(&d), "{d:?}");
}

// ---------- F3: find is bfs in Claude Code's shell: `-rm` deletes ----------------------------------------
#[test]
fn f3_find_rm_is_not_search() {
    let fx = fixture("q-f3");
    not_read_or_search(&fx, "find . -name '*.rs' -rm");
}
#[test]
fn f3b_find_rm_allowed_without_default_exclusions() {
    let fx = fixture("q-f3b");
    let st = closed(&fx, vec![]);
    let d = decide(&fx.bash("find src -rm"), &st, Surface::Console, NOW);
    assert!(!is_allow(&d), "{d:?}");
}

// ---------- F4: cd failure then ';' runs the rest in the ORIGINAL directory ------------------------------
#[test]
fn f4_cd_fail_then_semicolon_escapes_scope() {
    let fx = fixture("q-f4");
    let mut st = fx.state_with(vec!["<ws>/secret/**".into()]);
    reads_under(&mut st, &fx.ws);
    // classifier resolves plan.txt under ws/nope/secret (not excluded); the shell, cd having failed,
    // reads ws/secret/plan.txt (excluded)
    let cmd = "cd nope && echo ; cat secret/plan.txt";
    let d = decide(&fx.bash(cmd), &st, Surface::Console, NOW);
    assert!(!is_allow(&d), "{cmd} -> {d:?}");
}
#[test]
fn f4b_cd_dash_is_oldpwd_not_a_directory_named_dash() {
    assert!(
        recognise_posix("cd - && cat README.md").is_err(),
        "'cd -' goes to $OLDPWD"
    );
}

// ---------- F5: git config protection (T3) evaded by other files git reads as config --------------------
#[test]
fn f5a_git_commondir_write_is_t3() {
    let fx = fixture("q-f5a");
    let a = fx.write(&fx.ws.join(".git/commondir"), "../evil\n");
    let d = decide(&a, &fx.state(), Surface::Console, NOW);
    assert!(
        matches!(d, Decision::Deny { .. }) || tier_of(&d) == Some(Tier::T3),
        "{d:?}"
    );
}
#[test]
fn f5b_git_modules_config_write_is_t3() {
    let fx = fixture("q-f5b");
    let a = fx.write(&fx.ws.join(".git/modules/sub/config"), "[core]\n");
    let d = decide(&a, &fx.state(), Surface::Console, NOW);
    assert!(
        matches!(d, Decision::Deny { .. }) || tier_of(&d) == Some(Tier::T3),
        "{d:?}"
    );
}
#[test]
fn f5c_git_in_planted_bare_repo_is_not_a_read() {
    let fx = fixture("q-f5c");
    let b = fx.ws.join("bare");
    std::fs::create_dir_all(b.join("objects")).unwrap();
    std::fs::create_dir_all(b.join("refs")).unwrap();
    std::fs::write(b.join("HEAD"), "ref: refs/heads/main\n").unwrap();
    std::fs::write(b.join("config"), "[diff]\n\texternal = ./x\n").unwrap();
    not_read_or_search(&fx, "cd bare && git diff --no-index README.md src/main.rs");
}

// ---------- F6: find -fPATH (attached operand) is not a target ------------------------------------------
#[test]
fn f6_find_attached_f_operand_reaches_outside() {
    let fx = fixture("q-f6");
    let mut st = fx.state(); // no exclusions configured
    reads_under(&mut st, &fx.ws);
    let cmd = format!("find -f{} -name x", fx.outside.display());
    let d = decide(&fx.bash(&cmd), &st, Surface::Console, NOW);
    assert!(!is_allow(&d), "{cmd} -> {d:?}");
}

// ---------- F7: misc recogniser gaps (Minor) ------------------------------------------------------------
#[test]
fn f7_minor_option_abbreviations_and_zsh() {
    let fx = fixture("q-f7");
    for cmd in [
        "file --comp -m README.md",    // file --compile writes README.md.mgc
        "wc --files0=README.md",       // reads a list of files not seen as targets
        "grep -rS TOKEN src",          // BSD grep -S follows every symlink (same reason -R is refused)
        "grep --derefer TOKEN src",    // abbreviation of --dereference-recursive
        "cat =ls",                     // zsh EQUALS expansion: reads /bin/ls, not ./=ls
    ] {
        not_read_or_search(&fx, cmd);
    }
}

// ---------- F8: PowerShell parameter-name abbreviations (pure function) ---------------------------------
#[test]
fn f8_powershell_parameter_prefixes() {
    // PowerShell accepts any unambiguous prefix of a parameter name
    assert!(recognise_powershell("gc a.txt -Wa", true).is_err(), "-Wa = -Wait");
    assert!(recognise_powershell("gc a.txt -Str x", true).is_err(), "-Str = -Stream");
    assert!(recognise_powershell("gci -Fo -Recurse .", true).is_err(), "-Fo = -FollowSymlink");
    let r = recognise_powershell("gci -Rec .", true).unwrap();
    assert!(r.paths.iter().all(|p| p.1), "-Rec = -Recurse not seen: {r:?}");
}

// ---------- F9: card carries raw control / bidi characters --------------------------------------------
#[test]
fn f9_card_strings_have_no_control_or_bidi() {
    let fx = fixture("q-f9");
    let a = fx.write(
        &fx.ws.join("a.txt\n[read] /ws/README.md \u{202e}"),
        "x",
    );
    let d = decide(&a, &fx.state(), Surface::Console, NOW);
    let Decision::Ask { card } = d else {
        panic!("{d:?}")
    };
    for t in &card.targets {
        assert!(
            !t.chars().any(|c| c.is_control() || c == '\u{202e}'),
            "card target carries raw control/bidi text: {t:?}"
        );
    }
}

// ---------- Controls that PASS (kept as evidence of what was tried) -------------------------------------
#[test]
fn c_controls_that_hold() {
    let fx = fixture("q-ctl");
    for cmd in [
        "cat README.md | sort -o x",
        "cat README.md | sort --output=x",
        "find . -delete",
        "find . -fprint x",
        "find . -execdir ls ;",
        "git -c core.fsmonitor=x status",
        "git -C /tmp log",
        "git log --output=x",
        "rg --pre x y",
        "ls ${IFS}",
        "ls $'\\x41'",
        "ls {a,b}",
        "cat <<<x",
        "ls &",
        "ls |& cat",
        "ls >| x",
        "ls <(id)",
        "echo $((1+1))",
        "ls *",
        "ls ~root",
        "pushd /tmp && ls",
        "VAR=x cat a",
        "env cat a",
        "command cat a",
        "builtin cd /",
        "exec cat a",
        "time cat a",
        "nohup cat a",
        "xargs cat",
        "less a",
        "more a",
        "man ls",
        "cat a # x",
        "cat a\r",
        "cat a\u{0}",
        "cat a ；rm x",
        "ls -la | tee x",
        "sed -i s/a/b/ x",
        "awk 1 x",
        "uniq a b",
        "tail -f x",
    ] {
        not_read_or_search(&fx, cmd);
    }
    // hard deny holds against plain spellings and case
    for p in [
        fx.home.join(".CLAUDE/settings.json"),
        fx.ws.join(".GIT/hooks/x"),
        fx.home.join("./.claude//settings.json"),
    ] {
        let d = decide(&fx.write(&p, "x"), &fx.state(), Surface::Console, NOW);
        assert!(matches!(d, Decision::Deny { .. }), "{p:?}: {d:?}");
    }
    // .ENV is excluded case-insensitively
    let d = decide(
        &fx.bash("cat .ENV"),
        &closed(&fx, defaults()),
        Surface::Console,
        NOW,
    );
    assert!(!is_allow(&d));
    // userinfo / backslash URL hosts never match a grant
    assert_eq!(action::url_host("https://docs.nginx.org@evil.com/"), None);
    // T3 card refuses a session answer
    let a = fx.read(&fx.home.join(".ssh/id_rsa"));
    let Decision::Ask { card } = decide(&a, &fx.state(), Surface::Console, NOW) else {
        panic!()
    };
    let r = resolve(
        &card,
        &a,
        OwnerAnswer::AllowForSession(Scope::ExactInput {
            hash: a.raw_input_hash.clone(),
        }),
        NOW,
    );
    assert!(matches!(r.decision, Decision::Deny { .. }));
}

// ---------- DoS timing -------------------------------------------------------------------------------
#[test]
fn d_pathological_inputs_are_fast() {
    let fx = fixture("q-dos");
    let st = fx.state_with(defaults());
    let long = format!("cat {}", "a/".repeat(200_000));
    let t = std::time::Instant::now();
    let _ = decide(&fx.bash(&long), &st, Surface::Console, NOW);
    let big = format!("rm {}", "x/*/".repeat(5_000));
    let _ = decide(&fx.bash(&big), &st, Surface::Console, NOW);
    let nested = "[".repeat(100_000);
    let _ = HookInput::parse(&nested);
    assert!(t.elapsed().as_secs() < 10, "took {:?}", t.elapsed());
}

// ---------- per-item breakdown of the list tests above (reports every item, not only the first) --------
#[test]
fn z_breakdown() {
    let fx = fixture("q-z");
    let mut bad = vec![];
    for cmd in [
        "cat README.md | sort --o=/tmp/x",
        "cat README.md | sort --outp=/tmp/x",
        "cat README.md | sort -S 1K --compress-prog=sh",
        "cat README.md | sort --compress=sh",
        "cat README.md | sort --temporary-d=/tmp",
        "file --comp -m README.md",
        "wc --files0=README.md",
        "grep -rS TOKEN src",
        "grep --derefer TOKEN src",
        "cat =ls",
    ] {
        let a = fx.bash(cmd);
        if matches!(a.kind, Kind::Read | Kind::Search) {
            bad.push(format!("{cmd} => {:?}", a.kind));
        }
    }
    for cmd in [
        "grep --recur TOKEN .",
        "grep --null --recur TOKEN .",
        "grep --dir=recurse TOKEN .",
        "grep --directories recurse TOKEN .",
    ] {
        let mut st = fx.state_with(patterns::default_exclusions());
        st.link = LinkPhase::ClosedTainted;
        if is_allow(&decide(&fx.bash(cmd), &st, Surface::Console, NOW)) {
            bad.push(format!("{cmd} => ALLOW (closed link, default exclusions)"));
        }
    }
    for c in ["gc a.txt -Wa", "gc a.txt -Str x", "gci -Fo -Recurse ."] {
        if recognise_powershell(c, true).is_ok() {
            bad.push(format!("PS {c} => recognised"));
        }
    }
    assert!(bad.is_empty(), "\n{}", bad.join("\n"));
}

#[test]
fn z_timing() {
    let fx = fixture("q-zt");
    let st = fx.state_with(patterns::default_exclusions());
    let mut rep = vec![];
    for n in [1_000usize, 4_000, 16_000] {
        let t = std::time::Instant::now();
        let _ = decide(&fx.bash(&format!("cat {}", "a/".repeat(n))), &st, Surface::Console, NOW);
        rep.push(format!("cat a/ x{n}: {:?}", t.elapsed())); eprintln!("{}", rep.last().unwrap());
        let t = std::time::Instant::now();
        let _ = decide(&fx.bash(&format!("rm {}", "x/*/".repeat(n / 4))), &st, Surface::Console, NOW);
        rep.push(format!("rm x/*/ x{}: {:?}", n / 4, t.elapsed())); eprintln!("{}", rep.last().unwrap());
        let t = std::time::Instant::now();
        let _ = decide(&fx.bash(&format!("cat {}", "a ".repeat(n))), &st, Surface::Console, NOW);
        rep.push(format!("cat with {n} operands: {:?}", t.elapsed())); eprintln!("{}", rep.last().unwrap());
    }
    let t = std::time::Instant::now();
    let _ = HookInput::parse(&"[".repeat(100_000));
    rep.push(format!("nested [ x100000 parse: {:?}", t.elapsed()));
    panic!("TIMING REPORT\n{}", rep.join("\n"));
}
