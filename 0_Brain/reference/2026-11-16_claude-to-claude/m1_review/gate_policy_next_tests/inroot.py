# usage: python3 -B inroot.py <dir> <prog> [args...]  -- chdir (no shell cd) and exec
import os, sys
os.chdir(sys.argv[1]); os.execvp(sys.argv[2], sys.argv[2:])
