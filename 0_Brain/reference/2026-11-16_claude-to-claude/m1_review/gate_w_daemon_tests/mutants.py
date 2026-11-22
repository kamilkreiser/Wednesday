#!/usr/bin/env python3
"""QA-W-DAEMON mutants of the pure W-2 rule (TESTED on this Mac). Each: its own worktree inside the
clone and its own target dir; the builder's tests/win_rules.rs is run; a mutant must be KILLED."""
import subprocess, os, sys, shutil
W='/private/tmp/claude-501/qwd'
DD='crates/coagent-daemon/src/datadir.rs'
M = {
 'prefix_text': (DD, '''    for (i, p) in pparts.iter().enumerate() {
        let equal = match dparts.get(i) {''', '''    if true {
        let pt = profile.trim_end_matches(['\\\\', '/']).to_ascii_lowercase().replace('/', "\\\\");
        let dt = data_dir.trim_end_matches(['\\\\', '/']).to_ascii_lowercase().replace('/', "\\\\");
        return if dt == pt { Err(WinDirRefusal::IsTheProfile) } else if dt.starts_with(&pt) { Ok(()) } else { Err(WinDirRefusal::OutsideProfile) };
    }
    for (i, p) in pparts.iter().enumerate() {
        let equal = match dparts.get(i) {'''),
 'dotdot_allowed': (DD, '''    if part == "." || part == ".." {
        return Err(WinPathFault::DotComponent);''', '''    if part == "." {
        return Err(WinPathFault::DotComponent);'''),
 'unicode_case_fold': (DD, '''            Some(d) => p.eq_ignore_ascii_case(d),''', '''            Some(d) => p.to_lowercase() == d.to_lowercase(),'''),
 'profile_itself_accepted': (DD, '''    if dparts.len() == pparts.len() {
        return Err(WinDirRefusal::IsTheProfile);
    }''', ''),
 'unset_no_fence': (DD, '''    let v = value.ok_or(WinDirRefusal::ProfileUnset)?;''', '''    let Some(v) = value else { return Ok(String::new()) };'''),
 'unset_no_fence_empty_too': (DD, '''    let v = value.ok_or(WinDirRefusal::ProfileUnset)?;
    if v.is_empty() {
        return Err(WinDirRefusal::Profile(WinPathFault::Empty));
    }''', '''    let Some(v) = value else { return Ok(String::new()) };
    if v.is_empty() {
        return Ok(String::new());
    }'''),
}
names = sys.argv[1:] or list(M)
for n in names:
    f, old, new = M[n]
    wt = f'{W}/m_{n}'
    if not os.path.exists(wt):
        subprocess.run(['git','-C',f'{W}/clone','worktree','add','--detach',wt,'gh/w-daemon'],check=True,capture_output=True)
    p = f'{wt}/{f}'
    t = open(p).read()
    assert t.count(old) == 1, (n, t.count(old))
    open(p,'w').write(t.replace(old,new))
    td = f'{W}/target-m_{n}'
    if not os.path.exists(td):
        subprocess.run(['cp','-Rc',f'{W}/target-p',td],check=True)
    env = dict(os.environ, COAGENT_TOOLS=f'{W}/tools', CARGO_TARGET_DIR=td)
    r = subprocess.run(['bash','-c',f'. scripts/env.sh; cargo test --locked -p coagent-daemon --test win_rules 2>&1'],cwd=wt,env=env,capture_output=True,text=True)
    log = f'{W}/mutant_{n}.log'
    open(log,'w').write(subprocess.run(['git','-C',wt,'diff'],capture_output=True,text=True).stdout + '\n=====\n' + r.stdout)
    failed = [l for l in r.stdout.splitlines() if l.startswith('test ') and l.endswith('FAILED')]
    res = [l for l in r.stdout.splitlines() if 'test result:' in l or l.startswith('error')]
    print(f'MUTANT {n}: exit {r.returncode}; {"KILLED" if failed else "SURVIVED" if r.returncode==0 else "BUILD-FAIL?"}')
    for l in failed: print('   ', l)
    for l in res: print('   ', l)
    pan = [l for l in r.stdout.splitlines() if 'panicked' in l or 'assertion' in l or 'seed' in l][:6]
    for l in pan: print('     |', l[:220])
    subprocess.run(['git','-C',wt,'checkout','--',f],check=True)
