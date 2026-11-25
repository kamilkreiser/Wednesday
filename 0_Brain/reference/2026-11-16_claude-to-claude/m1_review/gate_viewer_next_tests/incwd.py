import subprocess, sys
# usage: incwd.py <dir> <cmd...>   runs cmd with cwd=<dir> (no `cd` in the shell)
sys.exit(subprocess.run(sys.argv[2:], cwd=sys.argv[1]).returncode)
